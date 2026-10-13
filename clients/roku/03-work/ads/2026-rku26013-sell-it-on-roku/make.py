"""RKU26013 Sell it on Roku, V2: build every industry in every size.

    python -I make.py                 -> all industries, all sizes
    python -I make.py pet 1x1         -> one industry, one size

Per frame:
  1. room plate (Figma AI, blown-out white glass, TV off)  img/raw/<ind>-plate-{1x1|tall|wide}.png
  2. the glass is found by flood-filling white from the panes above the TV, and the flat
     illustrated city (compose.city) is keyed in with a soft despill key
  3. the TV ad (img/raw/<ind>-screen.png) goes on the TV glass
  4. the plate is scaled and placed so the window top lands where the layout wants it;
     missing wall above is extended from the plate's own top rows
  5. HTML on top: lockup, headline, on-screen ad copy, CTA; Chrome exports the PNG
"""
import hashlib

import cv2
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from pymatting import estimate_alpha_cf

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "01-brand"))
sys.path.insert(0, str(HERE))
from rk_common import font_face, img_data, lockup  # noqa: E402
from compose import city  # noqa: E402
from detect import detect  # noqa: E402

RAW, BG, BUILD, EXPORT = HERE / "img" / "raw", HERE / "img" / "bg", HERE / "build", HERE / "export"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Copy: headlines are the client's, verbatim. On-screen ad copy is ours (fictional advertiser), short and plain.
IND = {
    "pet":      {"code": "Pet", "word": "pet brand", "ad": ("More tail wags.<br>Better days.", "Premium nutrition<br>for happy, healthy dogs.", "Shop now")},
    "beauty":   {"code": "Beauty", "word": "beauty brand", "ad": ("Glow that<br>lasts all day.", "Clean skincare made<br>for real routines.", "Shop now")},
    "food":     {"code": "FoodBev", "word": "products", "ad": ("Fresh from the oven.<br>At your door by 8.", "Small batch bakes,<br>delivered every morning.", "Order now")},
    "wellness": {"code": "Wellness", "word": "wellness brand", "ad": ("Your calm<br>starts here.", "Mats, gear and classes<br>for every body.", "Try it free")},
    "tech":     {"code": "Fashion-Tech", "word": "latest tech", "ad": ("Hear every<br>detail.", "Wireless sound built<br>for all day listening.", "Shop now")},
    "home":     {"code": "Homegoods", "word": "home brand", "ad": ("Comfort,<br>styled your way.", "Furniture and decor<br>made to last.", "Shop now")},
}

# Layouts in canvas px. win_top = where the top of the window glass should land.
# Layouts in canvas px. The top block stacks lockup, headline and CTA; the window glass starts at
# win_top, right under the block, and the TV top lands `sky` px below the glass top (the plate's
# empty sky band above the TV is cut down to that).
# Lucas 2026-10-13: ONE room per industry, cropped for every size (1:1, 4:5, 9:16, CTV): the square
# plate; Food uses its 4:5 room cut square around the TV (food-plate-master.png)
PLATE_FOR = {"pet": "1x1", "beauty": "1x1", "food": "tall", "wellness": "1x1", "tech": "1x1", "home": "1x1"}
# the CTV split has no wall above the window, so Food's room there is the square cut of the same plate
CTV_PLATE = {"food": "master"}

SIZES = {
    "1x1":  {"w": 1440, "h": 1440, "plate": "1x1",  "plat": "Meta", "win_top": 492, "sky": 64, "zoom": 1.14,
             "lk": (60, 340), "hl": (118, 104, 2), "cta": (370, 34), "safe": (0, 0)},
    "4x5":  {"w": 1440, "h": 1800, "plate": "tall", "plat": "Meta", "win_top": 470, "sky": 84, "zoom": 1.25, "zoom_tall": 1.08,
             "lk": (72, 360), "hl": (136, 112, 2), "cta": (402, 36), "safe": (0, 0)},
    "9x16": {"w": 1440, "h": 2560, "plate": "tall", "plat": "Meta", "win_top": 800, "sky": 110, "cover_h": True,
             "lk": (300, 420), "hl": (372, 120, 2), "cta": (660, 42), "safe": (267, 333)},
    "16x9": {"w": 1920, "h": 1080, "plate": "wide", "plat": "CTV", "win_top": 262, "sky": 46,
             "lk": (48, 250), "hl": (84, 66, 1), "cta": (176, 24), "safe": (54, 54)},
}
CANVAS = {"1x1": "1440x1440", "4x5": "1440x1800", "9x16": "1440x2560", "16x9": "1920x1080"}


def _grow(m, px):
    """Binary dilation by px pixels (square)."""
    return np.asarray(Image.fromarray(m.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(2 * px + 1))) > 0


def _box(x, px):
    """Box blur of a float array, radius px."""
    c = np.pad(x, ((px + 1, px), (px + 1, px)), mode="edge").cumsum(0).cumsum(1)
    n = 2 * px + 1
    return (c[n:, n:] - c[:-n, n:] - c[n:, :-n] + c[:-n, :-n]) / (n * n)


def glass_mask(a, tv):
    """How much of each pixel is the blown-out window glass (1 = all glass), and the glass bbox.

    Pass 3 (2026-10-12, after a white halo on the Pet dog). The first key ramped on brightness
    from 208 up: it put a ghost of the city on the light wall beside the window (233) and left
    white rims on fur, leaves and mullion bevels. Now a trimap goes to closed-form matting
    (pymatting), which splits every edge pixel into foreground and glass from its neighbourhood:
      glass    = truly blown-out glass (min >= 242, neutral) connected to the panes above the TV,
                 plus glass seen through gaps in leaves (min >= 246, within 40 px, inside the window
                 opening; never the floor, sill or wall around it)
      unknown  = 6 px around that glass, plus shaded glass up to 14 px away (light, neutral,
                 smooth and cool, e.g. the strip under the TV; cream furniture is warm or textured)
      fg       = everything else
    Then two fixes on the unknown band (see below): a per-pixel unmix caps the matte on light
    objects and flat wood, and solid light surfaces (a white sideboard top) get a crisp cut.
    Check with qa_key.py. Results are cached per plate in img/cache/.
    """
    key = hashlib.sha1(a.astype(np.uint8).tobytes() + bytes(str(tv) + "v4", "ascii")).hexdigest()[:16]
    cache = HERE / "img" / "cache" / f"{key}.npz"
    if cache.exists():
        z = np.load(cache)
        return z["k"], tuple(int(v) for v in z["box"])
    h, w, _ = a.shape
    mn = a.min(2); sat = a.max(2) - mn
    cand = (mn >= 242) & (sat < 14)
    seed = np.zeros_like(cand)
    ty0 = tv[1]
    # seeds: glass in the rows from just above the TV down to its bottom, so panes that a big leaf
    # cuts in two still get their lower part (Tech tall had a whole pane piece left white)
    sy0, sy1 = max(0, ty0 - int(h * .12)), tv[3]
    seed[sy0:sy1] = cand[sy0:sy1]
    x0t, x1t = tv[0], tv[2]
    seed[ty0 - 2:sy1, x0t:x1t] = False                        # not the TV glass itself
    c2 = cand[::2, ::2]; r = seed[::2, ::2].copy()        # geodesic flood fill at half resolution
    while True:
        g = r.copy()
        g[1:] |= r[:-1]; g[:-1] |= r[1:]; g[:, 1:] |= r[:, :-1]; g[:, :-1] |= r[:, 1:]
        g &= c2
        if (g == r).all():
            break
        r = g
    glass = np.repeat(np.repeat(r, 2, 0), 2, 1)[:h, :w] & cand
    ys, xs = np.where(glass)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    win = np.zeros_like(glass); win[y0:y1, x0:x1] = True      # the window opening
    gap = (mn >= 246) & (sat < 10) & win                      # glass in the gaps between leaves
    glass |= gap & _grow(glass, 40)
    lum = a.mean(2)
    rough = np.sqrt(np.maximum(_box(lum * lum, 1) - _box(lum, 1) ** 2, 0))
    soft = (mn >= 205) & (sat < 22) & (a[..., 2] >= a[..., 0] + 2) & (rough < 5) & win
    unknown = (_grow(glass, 6) | (soft & _grow(glass, 14))) & ~glass
    tri = np.zeros((h, w)); tri[glass] = 1; tri[unknown] = .5
    m = 12                                                    # matte only the window area
    cy0, cy1, cx0, cx1 = max(0, y0 - m), min(h, y1 + m), max(0, x0 - m), min(w, x1 + m)
    k = np.zeros((h, w), np.float32)
    k[cy0:cy1, cx0:cx1] = estimate_alpha_cf(np.ascontiguousarray(a[cy0:cy1, cx0:cx1] / 255.0, np.float64), np.ascontiguousarray(tri[cy0:cy1, cx0:cx1]))
    # Closed-form matting interpolates alpha across flat areas of the unknown band, which bleeds a
    # lilac haze onto white pots and cream sofas and tints wood next to the glass. Cap it with a
    # per-pixel unmix against the object's own colour (mean of sure-foreground pixels within 7 px):
    # a pixel can't be more glass than its colour says.
    fgf = (tri == 0).astype(np.float32)
    wsum = _box(fgf, 7)
    F = np.stack([_box(a[..., i] * fgf, 7) for i in range(3)], -1) / np.maximum(wsum, 1e-3)[..., None]
    wcol = np.median(a[glass], 0)
    d = F - wcol
    dd = (d * d).sum(-1)
    ku = 1 - np.clip(((a - wcol) * d).sum(-1) / np.maximum(dd, 1), 0, 1)
    # where: light objects (the matte can't tell them from glass), and pixels that are already
    # almost all object (flat wood next to the glass). Mixed rims of fur and leaves keep the matte.
    cap = unknown & (wsum > .05) & (dd > 10 ** 2) & ((F.mean(-1) > 185) | (ku < .15))
    k[cap] = np.minimum(k[cap], ku[cap])
    # light neutral surfaces against the glass (a white sideboard top, a lacquered shelf) differ
    # from it only by a few levels: decide those crisply, glass at >= 250, surface at <= 244
    surf = (mn >= 225) & (mn <= 245) & (sat < 16) & (a[..., 2] < a[..., 0] + 2)  # light, not glass, not cool
    surf = _grow(~_grow(~surf, 3), 3)                         # only solid surfaces, 7 px or thicker:
    pale = _grow(surf, 2) & unknown & (sat < 16)              # fur and leaf rims stay with the matte
    k[pale] = np.clip((mn[pale] - 244) / 6, 0, 1)
    _stand_line(a, mn, k, tv)
    # Lucas 2026-10-13: cream sofas got a smoky lilac rim (their fuzzy edge is lighter than their
    # body, so the matte called it half glass). Next to light, unsaturated objects the edge is cut
    # crisp; leaves and fur (darker or coloured) keep the soft matte.
    lightobj = unknown & (wsum > .05) & (F.mean(-1) > 150) & ((F.max(-1) - F.min(-1)) < 45)
    k[lightobj] = np.clip((k[lightobj] - 0.55) / 0.25, 0, 1)
    k[k < .02] = 0
    box = (int(x0), int(y0), int(x1), int(y1))
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache, k=k, box=np.array(box))
    return k, box


def _stand_line(a, mn, k, tv):
    """The sideboard top meets the blown-out glass with almost no contrast, so the matte smeared
    lilac over the top and its reflection (Lucas, 2026-10-12). Beside the TV the glass (254) steps
    down to the top surface (230-242) on one clean row: find it, key nothing below it across the
    sideboard, and key the thin glass strip under the TV crisply (dark feet stay)."""
    h, w = mn.shape
    tx0, ty0, tx1, ty1 = tv
    rows = []
    # columns right beside the TV only: the sideboard is always wider than the TV, but not by much
    for x in list(range(max(0, tx0 - 60), max(0, tx0 - 6), 2)) + list(range(min(w, tx1 + 6), min(w, tx1 + 60), 2)):
        if mn[ty1 - 6, x] < 250:
            continue                                          # not glass beside the TV bottom here
        col = mn[ty1 - 6:min(h, ty1 + 90), x] < 248
        for i in range(len(col) - 3):
            if col[i:i + 4].all():
                rows.append(ty1 - 6 + i)
                break
    if len(rows) < 4:
        return
    ls = int(np.median(rows))
    sat = a.max(2) - mn
    band = slice(ls + 1, min(h, ls + 10))                     # sideboard columns: not glass in the top's
    probe = ((mn[band] < 248) & (sat[band] < 32)).any(0)      # rows (its front edge can flash to 254),
                                                              # and not fur or leaves in front of it
    sx0 = tx0                                                 # the TV width is always sideboard;
    while sx0 > 0 and probe[max(0, sx0 - 4):sx0].any():       # grow outwards while the top continues
        sx0 -= 1
    sx1 = tx1
    while sx1 < w and probe[sx1:sx1 + 4].any():
        sx1 += 1
    # Pass 4 (Lucas, 2026-10-12): the top is a clean quad (top_geometry); recolor_top paints it.
    # Inside the quad and below it nothing is keyed; around its ends and above its back edge, light
    # neutral pixels are glass and get the city, with the quad's anti-aliased edge as the cut.
    neutral = np.clip((30 - sat) / 12, 0, 1)
    g = top_geometry(a, tv)
    if g is not None:
        quad, ls_, f, fx0, fx1 = g
        top = quad_mask(k.shape, quad)
        e0, e1 = max(0, fx0 - 60), min(w, fx1 + 60)
        rows = slice(max(0, ls_ - 30), min(h, f + 1))
        glass = np.clip((mn[rows, e0:e1] - 222) / 18, 0, 1) * neutral[rows, e0:e1]
        k[rows, e0:e1] = np.maximum(k[rows, e0:e1], glass) * (1 - top[rows, e0:e1])
        k[f:, fx0:fx1] = 0
        k *= 1 - top
    else:
        k[ls:, sx0:sx1] = 0
    lum = a[ty1:ls, tx0:tx1].mean(2)                          # glass strip under the TV: light and
    k[ty1:ls, tx0:tx1] = np.minimum(k[ty1:ls, tx0:tx1], np.clip((lum - 110) / 80, 0, 1) * neutral[ty1:ls, tx0:tx1])


def top_geometry(a, tv):
    """Sideboard top as a perspective quad: back edge row ls (glass/top line beside the TV), front
    edge row f (where the wood front face starts), front corners = the face's ends, back corners =
    front corners pulled toward the centre (measured where the back end is darker than glass,
    else 0.6 x the top's depth). Returns (quad, ls, f, face_x0, face_x1) or None."""
    sp = _stand_span(a, tv)
    if sp is None:
        return None
    (sx0, sx1), ls = sp
    h, w = a.shape[:2]
    mn = a.min(2); sat = a.max(2) - mn
    fs = []
    for x in range(sx0 + 4, sx1 - 4, 3):
        col = sat[ls:min(h, ls + 70), x] >= 14
        for i in range(len(col) - 4):
            if col[i:i + 5].all():
                fs.append(ls + i)
                break
    if len(fs) < 10:
        return None
    f = int(round(np.median(fs)))
    # the wood front face: the run of "wood" columns (warm, saturated, mid-light) that contains the
    # TV centre, small gaps (handles, a vase in front) bridged; armchairs and plants are not wood
    fr = a[f + 4:f + 20].astype(np.float32)
    r_, g_, b_ = fr[..., 0], fr[..., 1], fr[..., 2]
    woodpx = (r_ > g_) & (g_ > b_) & ((r_ - b_) > 25) & (fr.mean(2) > 90) & (fr.mean(2) < 230)
    face = woodpx.mean(0) > 0.5
    face = cv2.morphologyEx(face.astype(np.uint8)[None], cv2.MORPH_CLOSE, np.ones((1, 15), np.uint8))[0] > 0
    c = (tv[0] + tv[2]) // 2
    if not face[c]:
        return None
    fx0 = c
    while fx0 > 0 and face[fx0 - 1]:
        fx0 -= 1
    fx1 = c
    while fx1 < w and face[fx1]:
        fx1 += 1
    # the sideboard is centred on the TV: if flowers or a chair hide one end, mirror the other
    l_, r_ = c - fx0, fx1 - c
    if l_ < 0.85 * r_:
        fx0 = max(0, c - r_)
    elif r_ < 0.85 * l_:
        fx1 = min(w, c + l_)
    depth = f - ls
    def back(side):
        row = mn[ls + 2] if ls + 2 < h else mn[ls]
        rng = range(fx0, fx0 + depth * 2) if side < 0 else range(fx1 - 1, fx1 - 1 - depth * 2, -1)
        for x in rng:
            if 0 <= x < w and row[x] < 246:
                return x
        return None
    b0, b1 = back(-1), back(1)
    inset = 0.6 * depth
    bx0 = b0 if b0 is not None and 0 <= b0 - fx0 <= depth * 1.5 else fx0 + inset
    bx1 = b1 if b1 is not None and 0 <= fx1 - b1 <= depth * 1.5 else fx1 - inset
    # the bright front lip between the top and the wood face (it mirrors the window): include it
    lips = []
    for x in range(fx0 + 10, fx1 - 10, 4):
        y = f
        while y < min(h, f + 16):
            p = a[y, x].astype(np.float32)
            if p[0] > p[1] > p[2] and p[0] - p[2] > 25 and p.mean() < 230:
                break
            y += 1
        lips.append(y - f)
    lip = int(np.median(lips)) if lips else 0
    quad = np.array([[bx0, ls], [bx1, ls], [fx1, f + lip], [fx0, f + lip]], np.float32)
    return quad, ls, f + lip, fx0, fx1


def quad_mask(shape, quad, ss=4):
    h, w = shape
    m = np.zeros((h * ss, w * ss), np.uint8)
    cv2.fillPoly(m, [np.round(quad * ss).astype(np.int32)], 255)
    return cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255


def sideboard_top(a, tv, span=None, ls=None):
    g = top_geometry(a, tv)
    if g is None:
        return np.zeros(a.shape[:2], np.float32)
    return quad_mask(a.shape[:2], g[0])


def recolor_top(a, tv, k=None):
    """Repaint the sideboard top as a clean light-oak plane (the source top mirrors the window and
    carried ghost reflections and white patches). Dark or coloured things standing on it (TV feet,
    vases, plants) are kept. Returns a (modified in place).
    With k (the glass key, modified in place; Lucas 2026-10-13: the top surface kept causing small
    problems in every frame, so it is not shown at all, as if the sideboard were seen from the
    front): the front face is extended up over the top, with a flat line at the edge."""
    g = top_geometry(a, tv)
    if g is None:
        return a
    quad, ls, f, fx0, fx1 = g
    h, w = a.shape[:2]
    top = quad_mask((h, w), quad)
    mn = a.min(2); sat = a.max(2) - mn
    face = a[f + 3:f + 15, fx0 + (fx1 - fx0) // 4: fx1 - (fx1 - fx0) // 4].reshape(-1, 3)
    face = face[(face.max(1) - face.min(1)) > 12]
    if len(face) < 50:
        return a
    wood = np.median(face, 0)
    lightw = wood + (np.array([238, 228, 214.0]) - wood) * 0.5      # top catches the window light
    # oak grain from the sideboard's own front face: a strip of it, its variation around its mean,
    # tiled along the top (grain runs left-right on both), compressed a little in height
    # sample only the middle of the face (under the TV: never hidden by flowers or a chair), tiled
    c0, c1 = tv[0] + 10, tv[2] - 10
    strip = a[f + 3:f + 3 + 40, c0:c1].astype(np.float32)
    r3, g3, b3 = strip[..., 0], strip[..., 1], strip[..., 2]
    clean = ((r3 > g3) & (g3 > b3) & (r3 - b3 > 25) & (strip.mean(2) > 90) & (strip.mean(2) < 230)).mean(0) > 0.95
    clean = cv2.erode(clean.astype(np.uint8)[None], np.ones((1, 9), np.uint8))[0] > 0
    if clean.sum() > 40:
        strip = strip[:, clean]                                # only pure wood columns (no candle, petals)
    var = strip / np.maximum(strip.mean((0, 1), keepdims=True), 1)
    # drop the drawer seams and handles (thin vertical darks): per row, clamp to a wide median
    med = cv2.medianBlur((np.clip(var, 0, 2) * 127).astype(np.uint8), 31).astype(np.float32) / 127
    var = np.clip(var, med - 0.06, med + 0.06)
    yy = np.arange(h)[:, None]; xx = np.arange(w)[None, :]
    ty = ((yy - ls) * 2) % var.shape[0]
    tx = (xx - fx0) % var.shape[1]
    tex = var[np.clip(ty, 0, var.shape[0] - 1), np.broadcast_to(tx, (h, w))]
    tex = 1 + (tex - 1) * 0.6
    t = np.clip((yy - ls) / max(1, f - ls), 0, 1).astype(np.float32)
    # window light: brighter sheen toward the back edge, slightly darker toward the front
    shade = (1.04 - 0.07 * t)
    plane = lightw[None, None, :] * tex * shade[..., None]
    # anything standing on the top is kept: dark or coloured things (TV feet, plants), and anything
    # that rises above the top's back edge into the window (vases, bowls, books, lamps), down to
    # 70% of the top's depth (their bases sit toward the back). Reflections never rise above the
    # back edge, so they are repainted.
    b_, g_ = a[..., 2], a[..., 1]
    stand = ((mn < 110) | (sat > 45)).astype(np.uint8)
    # reflections of fur or decor on the glossy source top (warm, mid-dark, but not reaching the
    # top's front edge) are not objects
    n_, cc_, st_, _ = cv2.connectedComponentsWithStats(stand)
    for q in range(1, n_):
        bot_ = st_[q, cv2.CC_STAT_TOP] + st_[q, cv2.CC_STAT_HEIGHT]
        if bot_ < f - 1 and st_[q, cv2.CC_STAT_TOP] > ls + 1:
            stand[cc_ == q] = 0
    # flowers in front of the top: only clearly saturated lilac petals (the glossy source top also
    # mirrored the bouquet, faintly: those ghost reflections stay below the threshold)
    lilac = ((b_ > g_ + 18) & (mn < 200)).astype(np.uint8)
    stand |= cv2.dilate(lilac, np.ones((3, 3), np.uint8))
    # window posts end behind the top: a dark column that continues 40+ px up into the window is a
    # post, not something standing on the top (outside the TV only; the TV stand is kept)
    up = max(0, ls - 45)
    post = (mn[up:ls - 2] < 110).mean(0) > 0.8
    post[tv[0] - 4:tv[2] + 4] = False
    stand[:, post] = 0
    band_ = a[max(0, ls - 8):ls - 1]
    flowerish = (band_[..., 2] > band_[..., 1] + 4) | ((band_.max(2) - band_.min(2)) > 30)
    above = ((band_.min(2) < 247) & ~flowerish).mean(0) > 0.6     # neutral objects only (vases)
    above = cv2.morphologyEx(above.astype(np.uint8)[None], cv2.MORPH_OPEN, np.ones((1, 5), np.uint8))[0] > 0
    above[tv[0] - 4:tv[2] + 4] = False                        # under the TV: only its stand, dark
    depth = int((f - ls) * 0.7)
    for x in np.where(above)[0]:
        stand[ls - 1:ls + depth, x] = 1
    stand = cv2.morphologyEx(stand, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    keep = cv2.GaussianBlur(stand.astype(np.float32), (0, 0), 0.8)
    if k is not None:
        # seen from the front: the wood front face rises to the top's back edge (ls), so no top
        # surface shows; a flat 2 px line in the top's light tone marks the edge. Nothing else in
        # the plate changes (the glass/city around it stays as it was).
        # the old front lip mirrors the window as a light line right above the face: cover it too
        span = slice(fx0 + 10, fx1 - 10)
        fm = np.median(a[f + 4:f + 12, span].mean(2))
        # per column (the lip tilts a little with the perspective): its last bright row, smoothed
        lum_ = a[f:min(h, f + 16)].mean(2)
        bright = lum_ > fm + 18
        bright[1:-1] |= bright[:-2] & bright[2:]              # bridge one-row gaps
        run = np.cumprod(bright, 0).sum(0)                    # bright rows from f down, contiguous
        idx = cv2.medianBlur(np.clip(run, 0, 15).astype(np.uint8)[None], 31)[0].astype(int)
        base = int(np.median(idx[fx0 + 10:fx1 - 10]))
        idx[fx0:fx1] = np.maximum(idx[fx0:fx1], base)
        lipb = f + idx + 2                                    # first row below the lip, per column
        fb = int(lipb[fx0:fx1].max())
        yy_ = np.arange(h)[:, None]
        rect = quad_mask((h, w), np.array([[fx0, ls], [fx1, ls], [fx1, fb], [fx0, fb]], np.float32))
        # below the per-column lip end, down to the lowest one: only leftover light lip pixels
        light_ = (a.mean(2) > fm + 15).astype(np.float32)
        rect *= np.maximum((yy_ < lipb[None, :]).astype(np.float32), light_)
        # columns where something stands in front of the sideboard (flowers, a pot, the armchair, fur)
        # are left as they were: there the face just below the top is not wood
        fr = a[fb + 2:fb + 14].astype(np.float32)
        r4, g4, b4 = fr[..., 0], fr[..., 1], fr[..., 2]
        wd = ((r4 > g4) & (g4 > b4) & (r4 - b4 > 20) & (fr.mean(2) > 70) & (fr.mean(2) < 235)).mean(0) > 0.5
        # drawer seams and handles are thin: bridge them; only wide non-wood runs are occluders
        wd = cv2.morphologyEx(wd.astype(np.uint8)[None], cv2.MORPH_CLOSE, np.ones((1, 25), np.uint8))[0]
        wd[fx0:fx0 + 12] = wd[fx0 + 12]; wd[fx1 - 12:fx1] = wd[fx1 - 13]
        wd = cv2.erode(wd[None], np.ones((1, 5), np.uint8))[0].astype(np.float32)
        wd = cv2.GaussianBlur(wd[None], (0, 0), sigmaX=1.5)[0]
        # the TV stand is the only thing kept on the top (vases and bowls sit behind the edge now)
        # (only dark pixels connected to the TV itself: the glossy old top also mirrored the TV)
        tx0, tx1 = max(0, tv[0] - 4), min(w, tv[2] + 4)
        r0 = max(0, min(tv[3], ls) - 4)
        dk = (mn[r0:fb + 1, tx0:tx1] < 110).astype(np.uint8)
        n_, cc_, st_, _ = cv2.connectedComponentsWithStats(dk, connectivity=4)
        touch = set(np.unique(cc_[0][cc_[0] > 0]).tolist())
        stand_tv = np.zeros((h, w), np.float32)
        stand_tv[r0:fb + 1, tx0:tx1] = np.isin(cc_, list(touch)) if touch else 0
        stand_tv[:max(0, ls - 2)] = 0
        stand_tv = cv2.GaussianBlur(stand_tv, (0, 0), 0.7)
        # the rail is one smooth oak tone per column (the face's own colour right below it, blurred
        # sideways): no tiled grain, so no seams or blocks
        band4 = a[fb + 4:fb + 20].astype(np.float32)
        okc = ((band4[..., 0] > band4[..., 1]) & (band4[..., 1] > band4[..., 2])).astype(np.float32)
        colc = (band4 * okc[..., None]).sum(0) / np.maximum(okc.sum(0), 1)[:, None]
        colc = np.where(okc.sum(0)[:, None] > 3, colc, wood[None, :])
        # columns where something else stands in front of the face (a brown dog is "wood" too) fall
        # back to the face colour under the TV
        ref = np.median(colc[tv[0]:tv[2]], 0)
        colc = np.where((np.abs(colc - ref[None, :]).max(1) > 25)[:, None], ref[None, :], colc)
        wsm = cv2.GaussianBlur(np.ascontiguousarray(colc[None]), (0, 0), sigmaX=25)[0]
        face_c = np.broadcast_to(wsm[None], (h, w, 3))
        # things in front of the sideboard (fur, leaves, petals) rise into the window above the top line
        # and carry on down over the front face; things standing on the top stop at it and are cut by
        # the rail, as seen from the front. Candidates: dark or saturated pixels away from the oak
        # colour, outside the TV span (the TV, its stand and its mirror image are handled above).
        # (no post filter: a dog is tall too; dark neutrals, i.e. the TV, its stand, its mirror image
        # and the window posts, never count, so the TV span needs no exception)
        lap_ = cv2.GaussianBlur(np.abs(cv2.Laplacian(a.mean(2).astype(np.float32), cv2.CV_32F)), (0, 0), 2)
        boucle = (lap_ > 3.5) & (sat < 40) & (a.mean(2) > 150) & (a.mean(2) < 240)   # armchairs, throws
        fg = ((sat > 40) | ((a[..., 2] > a[..., 1] + 18) & (mn < 200)) | boucle) & ~((mn < 120) & (sat < 35))
        fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        fg &= (np.abs(a - ref[None, None, :]).max(2) > 40).astype(np.uint8)
        n_, cc_, st_, _ = cv2.connectedComponentsWithStats(fg)
        front = np.zeros((h, w), np.float32)
        for q in range(1, n_):
            t_, b_ = st_[q, cv2.CC_STAT_TOP], st_[q, cv2.CC_STAT_TOP] + st_[q, cv2.CC_STAT_HEIGHT]
            if t_ < ls - 1 and b_ > fb + 4 and st_[q, cv2.CC_STAT_AREA] > 20:
                front[cc_ == q] = 1
        # light fur and petals are only partly saturated: close the gaps inside each kept region
        front = cv2.morphologyEx(front, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
        front = cv2.GaussianBlur(cv2.dilate(front, np.ones((3, 3), np.uint8)), (0, 0), 0.8)
        # inside those regions only the object's own pixels (petals, fur, leaves) stay: the old light
        # top seen between the petals is replaced like everywhere else
        own = ((sat > 25) | (mn < 140) | boucle).astype(np.uint8)
        own = cv2.GaussianBlur(cv2.dilate(own, np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 0.7)
        front = front * own
        # Lucas 2026-10-13: like a straight-on shot, the TV foot rests right on the sideboard's top
        # edge and the top surface is not seen. The real front face (with its thin lit edge) is lifted
        # so its top edge meets the TV foot: rows from the lip down are resampled, per column, onto
        # the taller span foot..Y. What was the far part of the top above that line is window again.
        # Lucas 2026-10-13: every TV gets the Food 4:5 stand (flat plate, short neck), scaled to the
        # TV width and hung from the TV body's bottom row; the sideboard edge meets its plate.
        a0 = a.copy()                                          # untouched plate, for colours
        dark_ = (mn[:, tv[0]:tv[2]] < 60).mean(1)
        body = tv[3] - 15
        while body + 1 < h and dark_[body + 1] > 0.85:
            body += 1
        # the TV body's real extent on its bottom rows (the detected box can run wide)
        rowd = (mn[max(0, body - 4):body + 1] < 60).mean(0) > 0.6
        cx_ = (tv[0] + tv[2]) // 2
        if rowd[cx_]:
            bx0 = cx_
            while bx0 > 0 and rowd[bx0 - 1]:
                bx0 -= 1
            bx1 = cx_
            while bx1 < w - 1 and rowd[bx1 + 1]:
                bx1 += 1
        else:
            bx0, bx1 = tv[0], tv[2]
        top_tv0 = tv[1]
        while top_tv0 < body and (mn[top_tv0, bx0:bx1] < 60).mean() < 0.85:
            top_tv0 += 1
        st_rgba = _ref_stand(bx1 - bx0 + 1)
        sh_, sw_ = st_rgba.shape[:2]
        sx_ = (bx0 + bx1 + 1) // 2 - sw_ // 2
        foot = body + sh_                                      # first row under the plate's top half
        foot = int(np.clip(foot, body + 2, h - 2))
        stand_tv = np.zeros((h, w), np.float32)                # the old stand goes (it becomes glass)
        src0 = max(f, int(np.median(lipb[fx0 + 10:fx1 - 10])) - 3)   # keep ~1-2 px of the lit edge
        Y = min(h - 1, src0 + 4 * (src0 - foot) + 40)
        n_dst = Y - foot
        ys_src = src0 + (np.arange(n_dst) + 0.5) * (Y - src0) / n_dst - 0.5
        y0i = np.clip(np.floor(ys_src).astype(int), 0, h - 1); y1i = np.clip(y0i + 1, 0, h - 1)
        t_ = (ys_src - y0i)[:, None, None]
        lifted = a[y0i] * (1 - t_) + a[y1i] * t_
        # every column of the sideboard is lifted; what stands in front of it (flowers, fur) is put back
        # pixel by pixel through `front`
        cols = (np.arange(w) >= fx0) & (np.arange(w) < fx1)
        m = np.zeros((h, w), np.float32)
        m[foot:Y, cols] = 1
        m *= (1 - stand_tv) * (1 - front)
        new_ = a.copy()
        new_[foot:Y] = lifted
        # the far part of the top (ls..foot) becomes glass, except what stands on it (TV foot, vases)
        far = np.zeros((h, w), np.float32)
        far[max(0, ls - 1):foot, cols] = 1
        far[body + 1:foot, max(0, tv[0] - 6):min(w, tv[2] + 6)] = 1   # old stand, also above the top
        # what stands on the top or comes down from above (vases, books, plants, window posts) carries
        # on into this strip: non-glass pixels connected to something above the old top line stay
        # per column, what is just above the old top line carries on down to the new edge: a window
        # post (dark, neutral) is extended straight down; an object standing on the top (vase, books,
        # plant pot) keeps its own column as it was, so it still sits on the sideboard
        obj = np.zeros((h, w), np.float32)
        yr = max(0, ls - 3)
        for x in range(fx0, fx1):
            if mn[yr, x] >= 236 and sat[yr, x] <= 22:
                continue                                        # glass just above: nothing to carry
            if tx0 <= x < tx1:
                continue                                        # the TV and its stand: handled above
            if (mn[max(0, ls - 45):yr + 1, x] < 120).mean() > 0.9 and sat[yr, x] < 35:
                continue                                        # window post: handled below
            obj[yr:foot, x] = 1
        obj = cv2.morphologyEx(obj, cv2.MORPH_OPEN, np.ones((1, 3), np.uint8))
        obj[:, tx0:tx1] = 0
        obj = cv2.GaussianBlur(cv2.dilate(obj, np.ones((3, 3), np.uint8)), (0, 0), 0.7)
        far *= (1 - obj) * (1 - stand_tv) * (1 - front)
        # the lit edge on top of the face: one flat tone per row (the lifted lip was patchy where the
        # old top mirrored the window unevenly)
        mc = m[foot:foot + 1].ravel() > 0.5
        if mc.sum() > 20:
            facel = np.median(new_[foot + 10:foot + 16][:, mc].mean(2))
            nl = 0
            while nl < 8 and np.median(new_[foot + nl][mc].mean(1)) > facel + 15:
                nl += 1
            for r in range(foot, foot + max(nl, 2)):
                new_[r, mc] = np.median(new_[r, mc], 0) if r < foot + nl else np.median(new_[foot + nl, mc], 0)
        a[:] = a * (1 - m[..., None]) + new_ * m[..., None]
        a[:] = a * (1 - far[..., None]) + 255 * far[..., None]
        k[:] = np.maximum(k * (1 - m), far)
        # leftovers just above the new edge (the old top's back lip, shadows and reflections on the
        # glass right behind it): light neutral pixels there are glass, outside objects and fur
        r_g = max(0, ls - 16)
        clean = np.zeros((h, w), np.float32)
        clean[r_g:foot, fx0:fx1] = ((mn[r_g:foot, fx0:fx1] > 110) & (sat[r_g:foot, fx0:fx1] < 30))
        clean[max(0, foot - 4):foot, fx0:fx1] = 1               # the rows right above the edge
        clean *= (1 - obj) * (1 - front)
        clean[:body + 1] = 0
        a[:] = a * (1 - clean[..., None]) + 255 * clean[..., None]
        k[:] = np.maximum(k, clean)
        # window posts run down behind the sideboard to the new edge: a post is a narrow column that
        # is dark and neutral over a band of window above the old top (beside the TV) or under the
        # TV body (behind the TV); it is painted in its own tone from where it is seen down to the edge
        bt = max(0, ls - 70), max(1, ls - 20)
        dk = (mn < 120) & (sat < 35)
        postcol = np.zeros(w, bool)
        pcolor = np.zeros((w, 3), np.float32)
        ptop = np.zeros(w, int)
        top_tv = tv[1]
        while top_tv < body and (mn[top_tv, bx0:bx1] < 60).mean() < 0.85:
            top_tv += 1                                         # the TV body's top row
        y0a, y1a = max(0, top_tv - 45), max(1, top_tv - 6)       # window band above the TV: no objects
        for x in range(fx0, fx1):
            if y1a - y0a >= 4 and dk[y0a:y1a, x].mean() > 0.85:
                postcol[x] = True
                pcolor[x] = np.median(a0[y0a:y1a, x], 0)
                ptop[x] = body + 1 if bx0 - 3 <= x <= bx1 + 3 else y1a   # never over the TV
        run = postcol.astype(np.uint8)
        n_r, lab_r, st_r, _ = cv2.connectedComponentsWithStats(run[None], connectivity=4)
        for q in range(1, n_r):
            if st_r[q, cv2.CC_STAT_WIDTH] > 40:
                postcol[lab_r[0] == q] = False                  # too wide: the TV stand, not a post
        # Lucas 2026-10-13: nothing stands on the sideboard but the TV. Vases, lamps, bowls, books and
        # pot plants on it go (glass/city); posts and what stands in front of the sideboard stay.
        tall_ = int(0.7 * max(10, body - top_tv0))
        clr = np.zeros((h, w), np.float32)
        clr[max(0, ls - tall_):foot, fx0:fx1] = 1
        clr[:body + 1, max(0, bx0 - 3):bx1 + 4] = 0             # the TV itself
        clr *= (1 - front)
        clr[:, postcol] = 0                                     # posts are repainted below
        clr = cv2.GaussianBlur(clr, (0, 0), 0.6)
        a[:] = a * (1 - clr[..., None]) + 255 * clr[..., None]
        k[:] = np.maximum(k, clr)
        for x in np.where(postcol)[0]:
            a[ptop[x]:foot, x] = pcolor[x]
            k[ptop[x]:foot, x] = 0
        # the reference stand, its plate's bottom row overlapping the edge by one row
        y0s = foot - sh_ + 1
        reg = a[y0s:y0s + sh_, sx_:sx_ + sw_]
        al = st_rgba[..., 3:4]
        reg[:] = reg * (1 - al) + st_rgba[..., :3] * al
        k[y0s:y0s + sh_, sx_:sx_ + sw_] *= 1 - al[..., 0]
        return a
    wgt = top * (1 - keep)
    a[:] = a * (1 - wgt[..., None]) + plane * wgt[..., None]
    return a


_REF = {}


def _ref_stand(tv_w):
    """The TV stand of food-plate-tall (Lucas 2026-10-13: the model for every TV), as RGBA scaled
    so its TV is tv_w wide. Rows from just under the TV body down to the plate's bottom; colour
    unmixed from the white glass behind it."""
    if "src" not in _REF:
        p = RAW / "food-plate-tall.png"
        tv = detect(p)["tv"]
        a = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
        mn = a.min(2)
        dark = (mn[:, tv[0]:tv[2]] < 60).mean(1)
        body = tv[3] - 15
        while dark[body + 1] > 0.85:
            body += 1
        y = body + 1
        c0, c1 = tv[0] + (tv[2] - tv[0]) // 5, tv[2] - (tv[2] - tv[0]) // 5
        while (mn[y, c0:c1] < 60).mean() > 0.01:
            y += 1
        cut = a[body + 1:y + 1, tv[0]:tv[2]]
        lum = cut.mean(2, keepdims=True)
        al = np.clip((215 - lum) / 150, 0, 1)
        # only the stand itself (dark, plus a 1 px anti-aliased rim): no glare or shadow on the glass
        core = (cut.min(2) < 110).astype(np.uint8)
        al *= cv2.dilate(core, np.ones((3, 3), np.uint8))[..., None]
        col = np.where(al > 0.02, (cut - (1 - al) * 255) / np.maximum(al, 0.02), 0).clip(0, 255)
        xs = np.where(al[..., 0].max(0) > 0.1)[0]
        rgba = np.dstack([col, al])[:, xs.min():xs.max() + 1]
        _REF["src"] = (rgba.astype(np.float32), tv[2] - tv[0], xs.min(), xs.max())
    rgba, w0, _, _ = _REF["src"]
    s = tv_w / w0
    out = np.dstack([cv2.resize(np.ascontiguousarray(rgba[..., i]), None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
                     for i in range(4)])
    out[..., 3] = out[..., 3].clip(0, 1)
    return out


def _stand_span(a, tv):
    """(sideboard x span, glass/top row beside the TV) as found by _stand_line, or None."""
    mn = a.min(2); h, w = mn.shape
    tx0, ty0, tx1, ty1 = tv
    rows = []
    for x in list(range(max(0, tx0 - 60), max(0, tx0 - 6), 2)) + list(range(min(w, tx1 + 6), min(w, tx1 + 60), 2)):
        if mn[ty1 - 6, x] < 250:
            continue
        col = mn[ty1 - 6:min(h, ty1 + 90), x] < 248
        for i in range(len(col) - 3):
            if col[i:i + 4].all():
                rows.append(ty1 - 6 + i)
                break
    if len(rows) < 4:
        return None
    ls = int(np.median(rows))
    sat = a.max(2) - mn
    band = slice(ls + 1, min(h, ls + 10))
    probe = ((mn[band] < 248) & (sat[band] < 32)).any(0)
    sx0 = tx0
    while sx0 > 0 and probe[max(0, sx0 - 4):sx0].any():
        sx0 -= 1
    sx1 = tx1
    while sx1 < w and probe[sx1:sx1 + 4].any():
        sx1 += 1
    return (sx0, sx1), ls


def screen_mask(a, tv):
    """Where the ad goes: the switched-off (black) TV glass only, so whatever stands in front of
    the TV (the dog's head, leaves) stays in front of the ad. Soft edge over 60-110 luminance."""
    x0, y0, x1, y1 = tv
    lum = a[y0:y1, x0:x1].mean(2)
    dark = lum < 60
    sub = dark[::2, ::2]; g = np.zeros_like(sub); g[sub.shape[0] // 2, sub.shape[1] // 2] = True
    while True:                                               # dark region connected to the centre
        n = g.copy()
        n[1:] |= g[:-1]; n[:-1] |= g[1:]; n[:, 1:] |= g[:, :-1]; n[:, :-1] |= g[:, 1:]
        n &= sub
        if (n == g).all():
            break
        g = n
    reg = np.repeat(np.repeat(g, 2, 0), 2, 1)[:dark.shape[0], :dark.shape[1]]
    reg = _grow(reg, 2)
    return (np.clip((110 - lum) / 50, 0, 1) * reg).astype(np.float32)


def put_screen(a, raw, tv, ind):
    """Paste the TV ad into a (in place), masked by screen_mask on the untouched plate raw."""
    sx0, sy0, sx1, sy1 = tv
    scr = Image.open(RAW / f"{ind}-screen.png").convert("RGB")
    sw, sh = sx1 - sx0, sy1 - sy0
    f = max(sw / scr.width, sh / scr.height)
    scr = scr.resize((round(scr.width * f), round(scr.height * f)), Image.LANCZOS)
    scr = scr.crop(((scr.width - sw) // 2, (scr.height - sh) // 2, (scr.width - sw) // 2 + sw, (scr.height - sh) // 2 + sh))
    m = screen_mask(raw, tv)[..., None]
    a[sy0:sy1, sx0:sx1] = a[sy0:sy1, sx0:sx1] * (1 - m) + np.asarray(scr).astype(np.float32) * m


def background(ind, size):
    S = SIZES[size]
    path = RAW / f"{ind}-plate-{PLATE_FOR.get(ind, S['plate'])}.png"
    det = detect(path)
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    ph, pw, _ = a.shape
    tv = list(det["tv"])
    W, H = S["w"], S["h"]
    s = H / ph if S.get("cover_h") and ph * W / pw < H else W / pw
    zoom = S.get("zoom", 1.0) if ph <= pw else S.get("zoom_tall", 1.0)   # tall rooms are framed closer already
    s = max(s, W / pw) * zoom
    # cut the empty sky band above the TV down to S["sky"] canvas px (rows are removed, so the
    # vertical window posts stay continuous; the city is drawn afterwards on the shorter glass)
    _, (_, gy0, _, _) = glass_mask(a, tv)
    keep_top = int(ph * .02)
    cut = (tv[1] - gy0) - round(S["sky"] / s)
    if cut > 0:
        r0 = gy0 + keep_top
        a = np.concatenate([a[:r0], a[r0 + cut:]], 0)
        tv[1] -= cut; tv[3] -= cut
        ph = a.shape[0]
    k, (gx0, gy0, gx1, gy1) = glass_mask(a, tv)
    art = np.full_like(a, 255)
    art[gy0:gy1, gx0:gx1] = np.asarray(city(gx1 - gx0, gy1 - gy0)).astype(np.float32)
    raw = a.copy()
    recolor_top(a, tv, k)
    a = a + k[..., None] * (art - 255)
    put_screen(a, raw, tv, ind)

    big = Image.fromarray(a.clip(0, 255).astype(np.uint8)).resize((round(pw * s), round(ph * s)), Image.LANCZOS)
    ox = (W - big.width) // 2
    oy = round(S["win_top"] - gy0 * s)
    oy = max(min(oy, H), H - big.height)        # never leave a gap at the bottom
    canvas = Image.new("RGB", (W, H))
    if oy > 0:                                  # extend the wall above the plate
        top = np.asarray(big)[2:8].mean(0)
        canvas.paste(Image.fromarray(np.repeat(top[None], oy, 0).clip(0, 255).astype(np.uint8)), (ox, 0))
    canvas.paste(big, (ox, oy))
    BG.mkdir(parents=True, exist_ok=True)
    out = BG / f"{ind}-{size}.png"
    canvas.save(out)
    box = [round(v * s) for v in tv]
    return out, (box[0] + ox, box[1] + oy, box[2] + ox, box[3] + oy)


def html(ind, size, bg, box):
    S, d = SIZES[size], IND[ind]
    W, H = S["w"], S["h"]
    x0, y0, x1, y1 = box
    sw, sh = x1 - x0, y1 - y0
    h1, sub, adcta = d["ad"]
    lk_top, lk_w = S["lk"]
    hl_top, hl_fs, lines = S["hl"]
    cta_top, cta_fs = S["cta"]
    br = "<br>" if lines == 2 else " "
    return f"""<!doctype html><meta charset="utf-8"><title>RKU26013 {ind} {size}</title>
<style>
{font_face()}
html,body{{margin:0;background:#fff}}
.f{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:url({img_data(bg, "image/png")}) 0 0/{W}px {H}px;font-family:"Roku Display",sans-serif}}
.lk{{position:absolute;top:{lk_top}px;left:50%;transform:translateX(-50%);width:{lk_w}px;height:auto;display:block}}
.hl{{position:absolute;left:0;right:0;top:{hl_top}px;margin:0;text-align:center;font-weight:700;font-size:{hl_fs}px;line-height:1.08;letter-spacing:-.018em;color:#14082B}}
.hl b{{font-weight:700;color:#4F01A3}}
.scr{{position:absolute;left:{x0}px;top:{y0}px;width:{sw}px;height:{sh}px}}
.scr .t{{position:absolute;left:{round(sw * .065)}px;top:{round(sh * .2)}px;display:flex;flex-direction:column;gap:{round(sw * .022)}px;color:#fff}}
.scr h2{{margin:0;font-weight:700;font-size:{round(sw * .058)}px;line-height:1.08;letter-spacing:-.01em}}
.scr p{{margin:0;font-weight:400;font-size:{round(sw * .028)}px;line-height:1.3;color:#E9DEFF}}
.scr .b{{align-self:flex-start;margin-top:{round(sw * .012)}px;background:#fff;color:#4F01A3;font-weight:700;font-size:{round(sw * .025)}px;padding:{round(sw * .012)}px {round(sw * .027)}px;border-radius:999px}}
.scr .ad{{position:absolute;right:{round(sw * .03)}px;top:{round(sw * .025)}px;font-size:{round(sw * .018)}px;font-weight:500;color:#fff;background:rgba(0,0,0,.35);padding:{round(sw * .006)}px {round(sw * .014)}px;border-radius:6px}}
.cta{{position:absolute;left:50%;top:{cta_top}px;transform:translateX(-50%);display:flex;align-items:center;gap:{round(cta_fs * .5)}px;background:#4F01A3;color:#fff;font-weight:700;font-size:{cta_fs}px;line-height:1;padding:{round(cta_fs * .62)}px {round(cta_fs * 1.25)}px;border-radius:{round(cta_fs * .35)}px;box-shadow:0 {round(cta_fs * .3)}px {round(cta_fs * .9)}px rgba(32,0,76,.28);white-space:nowrap}}
.cta svg{{width:{round(cta_fs * .5)}px;height:{round(cta_fs * .8)}px}}
</style>
<div class="f">
  {lockup("lk", "#4F01A3", "#646464")}
  <h1 class="hl">Put your <b>{d["word"]}</b>{br}in their living room.</h1>
  <div class="scr"><span class="ad">Ad · 0:15</span><div class="t"><h2>{h1}</h2><p>{sub}</p><span class="b">{adcta}</span></div></div>
  <div class="cta">Learn more<svg viewBox="0 0 10 16" aria-hidden="true"><path d="M2 1.5 8.5 8 2 14.5" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
</div>"""


def fname(ind, size):
    S = SIZES[size]
    kind = "Static"
    return f"RKU26013-SellItOnRoku-{CANVAS[size]}-{kind}-{S['plat']}-{IND[ind]['code']}-V2"


def build(ind, size):
    bg, box = background(ind, size)
    BUILD.mkdir(exist_ok=True); EXPORT.mkdir(exist_ok=True)
    page = BUILD / f"{ind}-{size}.html"
    page.write_text(html(ind, size, bg, box), encoding="utf8")
    png = EXPORT / f"{fname(ind, size)}.png"
    S = SIZES[size]
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={S['w']},{S['h']}", f"--screenshot={png}", page.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return png


if __name__ == "__main__":
    inds = [sys.argv[1]] if len(sys.argv) > 1 else list(IND)
    sizes = [sys.argv[2]] if len(sys.argv) > 2 else list(SIZES)
    for i in inds:
        for z in sizes:
            print(build(i, z).name)
