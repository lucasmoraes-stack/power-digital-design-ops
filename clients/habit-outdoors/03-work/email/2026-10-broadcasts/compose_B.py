"""compose_B.py - October 2026 Broadcasts, Designer B: assets for emails 03 (Heavy Weight Hoodie) and 04 (Crater Valley).

Imports the kit's compose.py (never edited) and redirects its output folder to this batch's assets/,
so nothing in the shared kit is touched and nothing collides with compose_A.py / compose_C.py.
Every output is prefixed o3- or o4-.

Run from anywhere:
    python clients/habit-outdoors/03-work/email/2026-10-broadcasts/compose_B.py
    python .../compose_B.py --only o3-hero o4-gif

Mechanics kept from round 2 (../2026-broadcasts/compose_03-04.py):
  * images baked on a texture only sit on FINE-GRAIN tiles, with the crop's slow mottle removed and
    re-centred on the tile average, so every image border meets the <td> background level;
  * a tear always has the lower sheet over the upper one (shadow above, paper-fibre rim below), unless
    a paper strip is laid OVER a photo on purpose (it hides the store crop of model shots);
  * store model shots are cut at the forehead and at the thighs: those cuts always sit on an edge
    (the email top edge, a frame line or under a torn paper strip), never floating on a texture.
"""
from __future__ import annotations

import argparse
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "01-brand" / "email-kit" / "tools"))
import compose as c  # noqa: E402

OUT = HERE / "assets"
OUT.mkdir(exist_ok=True)
c.ASSETS = OUT                     # compose.py writes to c.ASSETS at call time; kit textures are read below
KIT_ASSETS = c.KIT / "assets"
c.tex_path = lambda name: KIT_ASSETS / c.TEXTURES[name][0]
PROD = c.PRODUCTS
PHOTOS = c.PHOTOS

TAPSHOE, BROWN, IVY, LIGHT, DM_BAND = c.TAPSHOE, c.BROWN, c.IVY, c.LIGHT, c.DM_BAND
OUTLINE = "#FEF4C6"
ORANGE = "#FF6400"
RIM = (228, 223, 216)


# ---------------------------------------------------------------- helpers

def save(arr, name, limit=150 * 1024, q=76, floor=50, sub=2):
    img = arr if isinstance(arr, Image.Image) else c.to_image(arr)
    p = c.save_jpg_under(img, OUT / name, limit, q=q, floor=floor, subsampling=sub)
    print(f"  {p.name:40s} {Image.open(p).size}  {p.stat().st_size / 1024:6.1f} KB")
    return p


def pn(w, h, l, seed, ly=None):
    return c.periodic_noise(w, h, l, ly or l, seed)


def tile(name, h, y0=0, w=1200, x0=0):
    """h x w of a tile starting at row y0 / column x0 (both wrap), as a background-repeat would show it."""
    t = c.load_tile(name)
    t = np.roll(t, -(x0 % t.shape[1]), axis=1)
    t = np.concatenate([t] * (math.ceil(w / t.shape[1]) + 1), axis=1)
    y0 %= t.shape[0]
    reps = math.ceil((y0 + h) / t.shape[0]) + 1
    tt = np.concatenate([t] * reps, axis=0)
    return tt[y0:y0 + h, :w].copy()


def fine(name, h, w=1200, y0=0, x0=0):
    """Tile crop with its slow mottle removed, centred on the tile average (fine grain only)."""
    base = tile(name, h, y0=y0, w=w, x0=x0)
    low = np.asarray(c.to_image(base).convert("RGB").filter(ImageFilter.GaussianBlur(40)), np.float32)
    return base - low + c.load_tile(name).reshape(-1, 3).mean(0)


def haze(arr, cx, cy, rx, ry, color, strength, seed=1, breakup=0.35, window=0):
    h, w = arr.shape[:2]
    yy = (np.arange(h, dtype=np.float32)[:, None] - cy) / ry
    xx = (np.arange(w, dtype=np.float32)[None, :] - cx) / rx
    m = np.exp(-(xx ** 2 + yy ** 2))
    if window:
        ys_, xs_ = np.arange(h, dtype=np.float32), np.arange(w, dtype=np.float32)
        wy = c.smooth(np.clip(np.minimum(ys_, h - 1 - ys_) / window, 0, 1))[:, None]
        wx = c.smooth(np.clip(np.minimum(xs_, w - 1 - xs_) / window, 0, 1))[None, :]
        m = m * wy * wx
    if breakup:
        n = pn(w, h, 90, seed) * 0.5 + pn(w, h, 30, seed + 1) * 0.25
        m = m * np.clip(1 + n * breakup, 0, 1.6)
    m = np.clip(m * strength, 0, 1)[:, :, None]
    return arr * (1 - m) + np.array(c.rgb(color), np.float32) * m


def _widths(w, seed, lo=1.5, hi=5.5):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, w + 60)
    k = np.exp(-np.linspace(-2.5, 2.5, 41) ** 2)
    n = np.convolve(n, k / k.sum(), "same")[30:30 + w]
    n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    return lo + (hi - lo) * n


def torn_over(upper, lower, ys, y_off=0, seed=0, lower_on_top=True, rim_alpha=0.55, shadow=(6.0, 0.34), specks=True):
    """Join two sheets along torn line ys. lower_on_top: lower sheet over the upper one (default)."""
    h, w = upper.shape[:2]
    line = np.array(ys, np.float32)[None, :] + y_off
    yy = np.arange(h, dtype=np.float32)[:, None]
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon([(0, h)] + [(x, y + y_off) for x, y in enumerate(ys)] + [(w, h)], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[:, :, None] / 255
    up, lo = upper.copy(), lower.copy()
    depth, strength = shadow
    if lower_on_top:
        d = line - yy
        up *= (1 - np.where(d > 0, np.exp(-d / depth), 0) * strength)[:, :, None]
    else:
        d = yy - line
        lo *= (1 - np.where(d > 0, np.exp(-d / depth), 0) * strength)[:, :, None]
    out = up * (1 - a) + lo * a
    if rim_alpha:
        wv = _widths(w, seed)[None, :]
        d = (yy - line) if lower_on_top else (line - yy)
        rm = ((d >= -0.5) & (d <= wv)).astype(np.float32)
        rm = np.asarray(Image.fromarray((rm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255
        fib = 0.7 + 0.3 * np.random.default_rng(seed + 9).random((h, w)).astype(np.float32)
        rm = (rm * fib * rim_alpha)[:, :, None]
        out = out * (1 - rm) + np.array(RIM, np.float32) * rm
    if specks:
        img = c.to_image(out)
        d, rnd = ImageDraw.Draw(img), random.Random(seed + 3)
        src = lo if lower_on_top else up
        spot = tuple(int(v) for v in np.median(src.reshape(-1, 3), 0))
        for _ in range(int(w / 40)):
            x = rnd.randrange(w)
            y = ys[x] + y_off + (-rnd.uniform(3, 10) if lower_on_top else rnd.uniform(3, 10))
            r = rnd.choice((1.2, 1.6, 2.2))
            d.ellipse((x - r, y - r, x + r, y + r), fill=spot + (255,))
        out = np.asarray(img.convert("RGB"), np.float32)
    return out


def edge(top, bottom, out, h=80, seed=0, amp=10):
    """E18 textured torn edge 1200 x h (shown 600 x h/2). Bottom = last rows of the next tile."""
    up = c.tile_rows(top, h, end=True)
    lo = c.tile_rows(bottom, h, end=c._continues(bottom))
    ys = c.torn_line(1200, h * 0.45, amp=amp, seed=seed)
    return save(torn_over(up, lo, ys, seed=seed), out, limit=30 * 1024, q=78, sub=0)


# QA r1 (2026-09-25): the store shots are cut at the forehead; a face must never be cut between the
# forehead and the mouth. CHIN = source row (1200px image) just under the chin / on the collar, where
# the image is cut instead. The cut always sits on an edge: email top, a frame line or under a torn strip.
CHIN = {
    "mens-crater-valley-full-zip-fleece-jacket/04.png": 150,
    "mens-crater-valley-full-zip-fleece-jacket/05.png": 150,
    "mens-crater-valley-full-zip-fleece-jacket/06.png": 182,
    "mens-crater-valley-sweater-fleece-zip-jacket/04.png": 165,
    "mens-crater-valley-sweater-fleece-zip-jacket/09.png": 175,
    "mens-crater-valley-performance-hoodie/07.png": 150,
}


def model(rel, keep_largest=False, chin=False):
    """Store image (transparent PNG) from photos/products/<handle>/NN.png, trimmed. keep_largest drops
    loose opaque islands (the store's 'Model is 6'3"' caption is a separate component)."""
    im = Image.open(PROD / rel).convert("RGBA")
    if chin:
        im = im.crop((0, CHIN[rel], im.width, im.height))
    if keep_largest:
        a = np.asarray(im.getchannel("A")) > 8
        from collections import deque
        lab = np.zeros(a.shape, np.int32)
        sizes, n = {}, 0
        small = Image.fromarray((a * 255).astype(np.uint8)).resize((a.shape[1] // 4, a.shape[0] // 4), Image.NEAREST)
        sa = np.asarray(small) > 0
        H, W = sa.shape
        for y in range(H):
            for x in range(W):
                if sa[y, x] and not lab[y, x]:
                    n += 1
                    q, cnt = deque([(y, x)]), 0
                    lab[y, x] = n
                    while q:
                        yy, xx = q.popleft()
                        cnt += 1
                        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                            ny, nx = yy + dy, xx + dx
                            if 0 <= ny < H and 0 <= nx < W and sa[ny, nx] and not lab[ny, nx]:
                                lab[ny, nx] = n
                                q.append((ny, nx))
                    sizes[n] = cnt
        big = max(sizes, key=sizes.get)
        keep = Image.fromarray(((lab[:H, :W] == big) * 255).astype(np.uint8)).resize(im.size, Image.NEAREST)
        keep = keep.filter(ImageFilter.MaxFilter(9))
        al = np.minimum(np.asarray(im.getchannel("A")), np.asarray(keep))
        im.putalpha(Image.fromarray(al.astype(np.uint8)))
    return im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())


def shadowed(canvas, im, cx, cy, angle=0, shadow=(10, 22, 26, 0.55), clip=None):
    """c.place, optionally clipped to rows clip=(y0, y1) of the canvas (model cut on a frame line)."""
    if clip is None:
        c.place(canvas, im, cx, cy, angle, shadow=shadow)
        return
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    c.place(layer, im, cx, cy, angle, shadow=shadow)
    a = np.asarray(layer.getchannel("A"), np.float32)
    y0, y1 = clip
    a[:max(0, y0)] = 0
    a[y1:] = 0
    layer.putalpha(Image.fromarray(a.astype(np.uint8)))
    canvas.alpha_composite(layer)


def rrect_mask(size, box, r, corners=("tl", "tr", "bl", "br"), ss=4):
    """Anti-aliased rounded-rectangle mask; corners not listed stay square."""
    w, h = size
    m = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(m)
    x0, y0, x1, y1 = [v * ss for v in box]
    R = r * ss
    d.rounded_rectangle((x0, y0, x1, y1), R, fill=255,
                        corners=tuple(k in corners for k in ("tl", "tr", "br", "bl")))
    return np.asarray(m.resize((w, h), Image.LANCZOS), np.float32) / 255


def outline(img, box, r, width=2, corners=("tl", "tr", "bl", "br"), open_side=None, color=OUTLINE, ss=4):
    """Draw a rounded outline (the open frame). open_side ('left'/'right') leaves that side off: the
    frame continues in the text <td> as a CSS border."""
    w, h = img.size
    m = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(m)
    x0, y0, x1, y1 = [v * ss for v in box]
    d.rounded_rectangle((x0, y0, x1, y1), r * ss, outline=255, width=width * ss,
                        corners=tuple(k in corners for k in ("tl", "tr", "br", "bl")))
    if open_side == "right":
        d.rectangle((x1 - width * ss - 1, y0 + width * ss, x1 + ss, y1 - width * ss), fill=0)
    if open_side == "left":
        d.rectangle((x0 - ss, y0 + width * ss, x0 + width * ss + 1, y1 - width * ss), fill=0)
    m = m.resize((w, h), Image.LANCZOS)
    layer = Image.new("RGBA", (w, h), c.rgb(color) + (255,))
    layer.putalpha(m)
    img.alpha_composite(layer)


def dashes(img, x, y, length=56, color=ORANGE):
    """The guide's two orange strokes (3px, 5px gap at 1x; file is 2x)."""
    d = ImageDraw.Draw(img)
    d.rectangle((x, y, x + length, y + 5), fill=c.rgb(color) + (255,))
    d.rectangle((x, y + 16, x + length, y + 21), fill=c.rgb(color) + (255,))


def contrast(p, box, texts=("#FFFFFF", "#E2DDD9")):
    print(f"      text area {box}: {c.contrast_report(p, list(texts), box)}")


# ================================================================ 03 Heavy Weight Hoodie

HOODIE = {
    "brown": "mens-heavy-weight-full-zip-hoodie--45636943249690",
    "gunmetal": "mens-heavy-weight-full-zip-hoodie--45636943446298",
    "loden": "mens-heavy-weight-full-zip-hoodie--45636943642906",
}


def o3_hero():
    """E24 hero 03: an oak edge at first light (orig-hunt50, the right half with no person), graded
    cold with a ground mist, fog grown above for the headline, the Major Brown hoodie standing in
    front of the trees; bottom melts into Tap Shoe paper (the tear to the light band is its own E18)."""
    ph = c.lifestyle("orig-hunt50-hunter-oaks-autumn.jpg")
    ph = ph.crop((1300, 0, 2400, 1600))                              # right part: oaks and grass, no hunter
    a = np.asarray(ph, np.float32)
    grey = a.mean(2, keepdims=True)
    a = (a * 0.55 + grey * 0.45) * np.array([0.90, 0.97, 1.05], np.float32) * 0.82   # cold, early, quiet
    h, w = a.shape[:2]
    yy = np.arange(h, dtype=np.float32)[:, None]
    band = np.exp(-((yy - h * 0.72) / (h * 0.16)) ** 2)                # ground mist over the grass line
    n = pn(w, h, 160, 31, 60) * 0.5 + pn(w, h, 50, 32, 20) * 0.3
    m = np.clip(band * (0.5 + n * 0.5), 0, 0.55)[:, :, None]
    a = a * (1 - m) + np.array((150, 156, 160), np.float32) * m
    # the fog is grown from the photo's top rows: soften them first (leaves made vertical streaks at the join)
    soft = np.asarray(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(28)), np.float32)
    k = c.smooth(np.clip((yy - 380) / 260, 0, 1))[:, :, None]                     # rows 380.. are the ones kept
    a = soft * (1 - k) + a * k
    ph = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

    orig = c.save_jpg_under

    def with_hoodie(im, path, limit, **k):
        im = im.convert("RGBA")
        hd = c.fit(c.load_packshot(HOODIE["brown"]), h=660)
        c.place(im, hd, 600, 1250, -3, shadow=(10, 26, 34, 0.6))
        return orig(im.convert("RGB"), path, limit, **k)

    c.save_jpg_under = with_hoodie
    try:
        p = c.compose_full_bleed_hero(ph, "o3-hero.jpg", next_tex="paper-tapshoe", seed=331,
                                      size=(1200, 1640), photo_w=1250, photo_y=840, photo_rows=(380, 1220),
                                      extend_top="fog", top_shade=(1000, 0.74), fade=(1450, 1600),
                                      tear_y=1630, grain_sd=2.4,
                                      text_boxes={"desktop": (100, 150, 1100, 930), "mobile": (150, 120, 1050, 1000)})
    finally:
        c.save_jpg_under = orig
    return p


# Panels (ref A): desktop row = image td 300 (24 margin + 276 of panel) + text td 276 + margin 24.
# The panel starts O3_TOP css px below the row top: the hoodie rises out of the panel into that gap.
O3_PANEL_H = 250
O3_TOP = 44
O3_MOBILE_W = 343                     # 375 - 2 x 16


def _panel_img(file, out, *, tex, band, W, H, panel_box, corners, cx, cy, angle, height, seed, haze_c, open_edge, tx, ty):
    """One panel piece: band paper (fine grain) outside, panel texture (fine grain) + glow inside,
    rounded outer corners, hoodie over both (rising out of the panel top). The glow is gone at
    `open_edge` ('left'/'right'/'bottom'), where the panel continues in the text <td>."""
    base = fine(band, H, w=W)
    # the panel continues in the text <td> (background-position:left top, 600px wide): bake the tile
    # at the phase that td shows, so the join is invisible (tx, ty = tile column/row of piece pixel 0,0)
    plain = tile(tex, H, y0=ty, w=W, x0=tx)
    x0, y0, x1, y1 = panel_box
    pcy = (max(y0, 0) + min(y1, H)) / 2
    pan = haze(plain.copy(), cx, pcy + 10, 230, 200, haze_c, 0.55, seed=seed, breakup=0.5)
    xs, ys = np.arange(W, dtype=np.float32)[None, :], np.arange(H, dtype=np.float32)[:, None]
    ramp = {"right": c.smooth(np.clip((W - 1 - xs) / 120, 0, 1)) + ys * 0,
            "left": c.smooth(np.clip(xs / 120, 0, 1)) + ys * 0,
            "bottom": c.smooth(np.clip((H - 1 - ys) / 120, 0, 1)) + xs * 0}[open_edge][:, :, None]
    pan = plain * (1 - ramp) + pan * ramp
    m = rrect_mask((W, H), panel_box, 24, corners=corners)[:, :, None]
    img = c.to_image(base * (1 - m) + pan * m)
    hd = c.fit(c.load_packshot(file), h=height)
    c.place(img, hd, cx, cy, angle, shadow=(10, 22, 28, 0.55))
    return save(img, out, limit=90 * 1024, q=78)


def o3_panels():
    """3 panel pieces x (desktop, mobile) x (light, dark) for the colour panels band."""
    rows = [  # colour, panel texture, glow, image side
        ("brown", "grain-brown", "#8C7E70", "left", 331),
        ("gunmetal", "paper-tapshoe", "#6E6F72", "right", 332),
        ("loden", "grain-ivy", "#9A9477", "left", 333),
    ]
    for key, tex, glow, side, seed in rows:
        f = HOODIE[key]
        # desktop: 600 x 588 file (300 x 294 css); panel from y = 2*O3_TOP to bottom
        W, H = 600, (O3_TOP + O3_PANEL_H) * 2
        if side == "left":
            box, corners, cx, ang = (48, O3_TOP * 2, W + 40, H + 40), ("tl", "bl"), 318, -4
        else:
            box, corners, cx, ang = (-40, O3_TOP * 2, W - 48, H + 40), ("tr", "br"), 282, 4
        # the panel ends on the image bottom (round outer corners) and runs past the inner edge
        box = (box[0], box[1], box[2], H - 1)
        for suffix, band in (("", "paper-light"), ("-dm", "paper-light-dm")):
            _panel_img(f, f"o3-panel-{key}{suffix}.jpg", tex=tex, band=band, W=W, H=H,
                       panel_box=box, corners=corners, cx=cx, cy=12 + 260, angle=ang, height=520,
                       seed=seed, haze_c=glow, open_edge="right" if side == "left" else "left",
                       tx=600 if side == "left" else 552, ty=-O3_TOP * 2)
        # mobile: 686 x 560 file (343 x 280 css): 40 css of paper, then the panel with rounded top corners
        W, H = O3_MOBILE_W * 2, 560
        box = (0, 80, W - 1, H + 40)
        for suffix, band in (("", "paper-light"), ("-dm", "paper-light-dm")):
            _panel_img(f, f"o3-panel-{key}-m{suffix}.jpg", tex=tex, band=band, W=W, H=H,
                       panel_box=box, corners=("tl", "tr"), cx=W / 2, cy=10 + 255,
                       angle=-4 if side == "left" else 4, height=510, seed=seed + 10, haze_c=glow, open_edge="bottom",
                       tx=0, ty=-H)


def o3_edges():
    """03 torn edge: Tap Shoe paper (hero bottom) -> light paper is the kit's edge-tex-papertapshoe-paperlight(+dm);
    the light paper -> footer is the kit's edge-tex-paperlight-footer(+dm). Nothing to generate."""
    print("  (kit edges reused)")


# ================================================================ 04 Crater Valley

CV = {
    "hoodie": "mens-crater-valley-performance-hoodie--52423312867610",
    "fleece": "mens-crater-valley-full-zip-fleece-jacket--52630367076634",
    "qzip": "mens-crater-valley-sweater-fleece-zip-jacket--52630359834906",
}
O4_A_W, O4_A_H = 270, 620           # hero row A image column (css)
O4_B_H = 150                        # hero row B strip (css)
O4_TEAR_B = 104                     # tear line inside the strip (css)


def o4_hero():
    """Hero 04 (ref D): headline left on Tap Shoe paper, the Full Zip Fleece on model bleeding off the
    right edge and cut by the email top edge; one canvas split into row A (right column) and row B
    (full-width strip that tears into the Major Brown band). Mobile twin: the same model under a torn
    strip of the hero paper (it hides the store's forehead cut), tearing into the brown band."""
    W = 1200
    HA, HB = O4_A_H * 2, O4_B_H * 2
    H = HA + HB
    canvas = tile("paper-tapshoe", H, w=W)          # raw tile at the td phase (background-position left top)
    canvas = haze(canvas, 1000, 760, 380, 620, "#5B524A", 0.55, seed=401, breakup=0.5)
    # the glow must vanish at the left edge of the image column (x = 660) where the text td continues
    xs = np.arange(W, dtype=np.float32)[None, :, None]
    wx = c.smooth(np.clip((xs - 700) / 160, 0, 1))
    canvas = tile("paper-tapshoe", H, w=W) * (1 - wx) + canvas * wx
    img = c.to_image(canvas)
    # cut under the chin, cut on row 0 (email top edge); tall enough that the thigh cut stays under the tear
    fl = c.fit(model("mens-crater-valley-full-zip-fleece-jacket/05.png", chin=True), h=HA + O4_TEAR_B * 2 + 40)
    cx = 1060
    while True:                                   # nothing of the model may cross into the text column (x < 660)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        c.place(lay, fl, cx, fl.height / 2, 0, shadow=None)
        if not (np.asarray(lay.getchannel("A"))[:HA, :672] > 0).any():
            break
        cx += 10
    print(f"      hero model centre x {cx}")
    c.place(img, fl, cx, fl.height / 2, 0, shadow=(14, 20, 34, 0.5))
    arr = np.asarray(img.convert("RGB"), np.float32)
    # tear into the brown band (lower sheet over)
    lo = c.tile_rows("grain-brown", H, end=True)
    ys = c.torn_line(W, 0, amp=10, seed=402)
    arr = torn_over(arr, lo, ys, y_off=HA + O4_TEAR_B * 2, seed=402, rim_alpha=0.6, shadow=(9.0, 0.45))
    # row A = right column only (x >= 660); the text td left of it shows the same tile as the td background
    save(arr[:HA, 660:], "o4-hero-a.jpg", limit=110 * 1024, q=78)
    save(arr[HA:], "o4-hero-b.jpg", limit=60 * 1024, q=78)
    # mobile twin: 750 x 900 (375 x 450 css), shown full width under the text
    MW, MH = 750, 900
    top_strip = fine("paper-tapshoe", MH, w=MW)
    back = haze(fine("paper-tapshoe", MH, w=MW), 470, 470, 330, 380, "#5B524A", 0.6, seed=403, window=120, breakup=0.5)
    mi = c.to_image(back)
    fl2 = c.fit(model("mens-crater-valley-full-zip-fleece-jacket/05.png", chin=True), h=880)
    c.place(mi, fl2, 470, 84 + fl2.height / 2, 0, shadow=(12, 18, 30, 0.5))   # chin cut under the strip (tear at 110 +- 9)
    marr = np.asarray(mi.convert("RGB"), np.float32)
    ya = c.torn_line(MW, 0, amp=9, seed=404)
    marr = torn_over(top_strip, marr, ya, y_off=110, seed=404, lower_on_top=False, rim_alpha=0.6, shadow=(9.0, 0.5))
    lo = c.tile_rows("grain-brown", MH, end=True)[:, :MW]
    yb = c.torn_line(MW, 0, amp=9, seed=405)
    marr = torn_over(marr, lo, yb, y_off=MH - 70, seed=405, rim_alpha=0.6, shadow=(9.0, 0.45))
    save(marr, "o4-hero-m.jpg", limit=110 * 1024, q=76)


# Frames (ref D): desktop row = image td 300 (24 margin + 276 of frame) + text td 276 + margin td 24.
O4_ROW_H = 330                      # css
O4_FT = 44                          # frame top line (css)
O4_FB = 318                         # frame bottom line (css)
O4_R = 12


def _frame_piece(out, *, W, H, frame_box, corners, open_side, items, seed, glow_c, dash_at, band="grain-brown"):
    """Frame piece on the brown band: glow, items (pop-out or clipped on the frame lines), outline,
    orange strokes. items: [{img, h, cx, cy, angle, clip, over_line}] (clip = keep between the lines)."""
    base = fine(band, H, w=W)
    x0, y0, x1, y1 = frame_box
    arr = haze(base.copy(), (x0 + x1) / 2 if open_side is None else (x0 + 300 if open_side == "right" else x1 - 300),
               (y0 + y1) / 2, 240, 230, glow_c, 0.45, seed=seed, window=90, breakup=0.5)
    img = c.to_image(arr)
    # items clipped on the frame lines go under the outline; pop-outs go over it
    for it in items:
        if it.get("clip"):
            shadowed(img, c.fit(it["img"], h=it["h"]), it["cx"], it["cy"], it.get("angle", 0),
                     shadow=(8, 18, 24, 0.5), clip=(y0 + 1, y1 - 1))
    outline(img, frame_box, O4_R * 2, width=2, corners=corners, open_side=open_side)
    for it in items:
        if not it.get("clip"):
            shadowed(img, c.fit(it["img"], h=it["h"]), it["cx"], it["cy"], it.get("angle", 0),
                     shadow=(10, 22, 28, 0.55))
    if dash_at:
        dashes(img, *dash_at)
    return save(img, out, limit=100 * 1024, q=78)


def o4_frames():
    """3 frame pieces (desktop + mobile), client order and sides: hoodie img left, fleece img right, quarter zip img left."""
    hood = model("mens-crater-valley-performance-hoodie/08.png")       # hood up: the hood is whole, it can pop out
    fleece = model("mens-crater-valley-full-zip-fleece-jacket/06.png", chin=True)  # cut on the collar = frame top line
    qzip = c.load_packshot(CV["qzip"])                                 # no model shot in Realtree APX: garment pops out
    W, H = 600, O4_ROW_H * 2
    ft, fb = O4_FT * 2, O4_FB * 2
    left = dict(frame_box=(48, ft, W + 40, fb), corners=("tl", "bl"), open_side="right", dash_at=(20, ft - 34))
    right = dict(frame_box=(-40, ft, W - 48, fb), corners=("tr", "br"), open_side="left", dash_at=(W - 76, ft - 34))
    # the hood photo stops at the hips: it pops out at the top and is cut on the bottom line
    _hood_piece(hood, W, H, ft, fb, left, "o4-frame-hoodie.jpg", seed=411)
    _frame_piece("o4-frame-fleece.jpg", W=W, H=H, seed=412, glow_c="#8A7C6E", **right,
                 items=[{"img": fleece, "h": 698, "cx": 300, "cy": ft + 349, "angle": 0, "clip": True}])
    _frame_piece("o4-frame-qzip.jpg", W=W, H=H, seed=413, glow_c="#8A7C6E", **left,
                 items=[{"img": qzip, "h": 560, "cx": 320, "cy": 20 + 280 + 8, "angle": -5, "clip": False}])
    # mobile: 750 x 640 (375 x 320 css): closed frame inset 16 css, text sits below (no frame on mobile)
    MW, MH = 750, 640
    box = (32, 88, MW - 32, MH - 24)
    _hood_piece(hood, MW, MH, box[1], box[3], dict(frame_box=box, corners=("tl", "tr", "bl", "br"), open_side=None,
                dash_at=(32, box[1] - 34)), "o4-frame-hoodie-m.jpg", seed=421, cx=MW / 2)
    _frame_piece("o4-frame-fleece-m.jpg", W=MW, H=MH, seed=422, glow_c="#8A7C6E", frame_box=box,
                 corners=("tl", "tr", "bl", "br"), open_side=None, dash_at=(MW - 88, box[1] - 34),
                 items=[{"img": fleece, "h": 698, "cx": MW / 2, "cy": box[1] + 349, "clip": True}])
    _frame_piece("o4-frame-qzip-m.jpg", W=MW, H=MH, seed=423, glow_c="#8A7C6E", frame_box=box,
                 corners=("tl", "tr", "bl", "br"), open_side=None, dash_at=(32, box[1] - 34),
                 items=[{"img": qzip, "h": 560, "cx": MW / 2, "cy": 20 + 280 + 8, "angle": -5, "clip": False}])


def _hood_piece(hood, W, H, ft, fb, geo, out, seed, cx=330):
    """Hoodie on model with the hood up: it rises out of the frame top (the hood is whole) and is cut
    by the frame bottom line (the store photo stops at the hips)."""
    base = fine("grain-brown", H, w=W)
    x0, y0, x1, y1 = geo["frame_box"]
    arr = haze(base.copy(), cx, (y0 + y1) / 2, 240, 230, "#8A7C6E", 0.45, seed=seed, window=90, breakup=0.5)
    img = c.to_image(arr)
    hd = c.fit(hood, h=700)
    outline(img, geo["frame_box"], O4_R * 2, width=2, corners=geo["corners"], open_side=geo["open_side"])
    shadowed(img, hd, cx, 14 + hd.height / 2, 0, shadow=(10, 22, 28, 0.55), clip=(0, y1 - 1))
    # redraw the bottom line over the cut
    outline_bottom = Image.new("RGBA", img.size, (0, 0, 0, 0))
    outline(outline_bottom, geo["frame_box"], O4_R * 2, width=2, corners=geo["corners"], open_side=geo["open_side"])
    a = np.asarray(outline_bottom.getchannel("A"), np.float32)
    a[: y1 - 40] = 0
    outline_bottom.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(outline_bottom)
    if geo.get("dash_at"):
        dashes(img, *geo["dash_at"])
    return save(img, out, limit=100 * 1024, q=78)


def o4_edges():
    """04 torn edges: brown -> Ivy (not in the kit), Ivy -> footer is the kit's edge-tex-ivy-footer.jpg."""
    edge("grain-brown", "grain-ivy", "o4-edge-brown-ivy.jpg", seed=441)


# ---- D4 lifestyle GIF (QA r1, 2026-09-25: 3 scenes, <= 250 KB, faces cut under the chin, softer and
# less posterised; one crossfade frame would double the weight, so the scenes cut straight)

GIF_W, GIF_H = 600, 380             # 1x file: a 2x file (1200x760) of 3 photographic frames is ~3x the budget
WIN = (44, 340)                     # torn window rows
GIF_BACK = ("crop-sent-sep10-utv-hunters.jpg", (0, 40, 230, 540))   # trees and field left of the hunters, no person
GIF_COLORS, GIF_DITHER, GIF_SMOOTH = 152, False, 0.8   # dither added noise and weight: 160+ smooth colours read better


def _gif_backdrop():
    """Out-of-focus tree line and field (a real Habit photo, heavily blurred), shared by every scene, so it
    is encoded once. Only the models change from frame to frame."""
    ph = c.lifestyle(GIF_BACK[0]).crop(GIF_BACK[1]).filter(ImageFilter.GaussianBlur(10))
    ph = ph.resize((GIF_W, WIN[1] - WIN[0] + 60), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    a = np.asarray(ph, np.float32)
    grey = a.mean(2, keepdims=True)
    a = (a * 0.7 + grey * 0.3) * 0.62
    out = np.zeros((GIF_H, GIF_W, 3), np.float32)
    y0 = WIN[0] - 30
    out[y0:y0 + a.shape[0]] = a[: GIF_H - y0]
    return out


def _gif_scene(items):
    W, H = GIF_W, GIF_H
    ivy = fine("grain-ivy", H * 2, w=W * 2)
    ivy = np.asarray(c.to_image(ivy).convert("RGB").resize((W, H), Image.LANCZOS), np.float32)
    img = c.to_image(_gif_backdrop())
    for it in items:
        m = c.fit(it["img"], h=it["h"])
        c.place(img, m, it["cx"], it["top"] + m.height / 2, 0, shadow=(6, 10, 16, 0.5))
    mid = np.asarray(img.convert("RGB"), np.float32)
    yb = c.torn_line(W, 0, amp=6, seed=462)
    arr = torn_over(mid, ivy, yb, y_off=WIN[1], seed=462, rim_alpha=0.6, shadow=(5.0, 0.45), specks=False)
    ya = c.torn_line(W, 0, amp=6, seed=461)
    arr = torn_over(ivy, arr, ya, y_off=WIN[0], seed=461, lower_on_top=False, rim_alpha=0.6, shadow=(6.0, 0.5), specks=False)
    return arr


def o4_gif():
    """D4: 3 scenes in a loop; scene 1 (the one Outlook desktop shows) = the three layers together.
    Frame 1 is the whole image; frames 2 and 3 carry only the pixels that change (the rest is the
    transparent index), each with its own 255-colour palette and dither, so the strips and the
    backdrop are paid once."""
    hood7 = model("mens-crater-valley-performance-hoodie/07.png", chin=True)
    fl4 = model("mens-crater-valley-full-zip-fleece-jacket/04.png", keep_largest=True, chin=True)  # caption removed
    qz4 = model("mens-crater-valley-sweater-fleece-zip-jacket/04.png", chin=True)
    hood8 = model("mens-crater-valley-performance-hoodie/08.png")                # hood up, head whole
    qz9 = model("mens-crater-valley-sweater-fleece-zip-jacket/09.png", chin=True)
    top = WIN[0] - 9                                   # chin cut under the upper strip (tear at WIN[0] +- 6)
    scenes = [
        _gif_scene([{"img": hood7, "h": 330, "cx": 140, "top": top},
                    {"img": qz4, "h": 330, "cx": 462, "top": top},
                    {"img": fl4, "h": 340, "cx": 300, "top": top}]),
        _gif_scene([{"img": hood8, "h": 420, "cx": 300, "top": WIN[0] + 12}]),
        _gif_scene([{"img": qz9, "h": 400, "cx": 300, "top": top}]),
    ]
    if GIF_SMOOTH:
        scenes = [np.asarray(c.to_image(s).convert("RGB").filter(ImageFilter.GaussianBlur(GIF_SMOOTH)), np.float32)
                  for s in scenes]
    dith = Image.Dither.FLOYDSTEINBERG if GIF_DITHER else Image.Dither.NONE
    ims = []
    for i, s in enumerate(scenes):
        rgb = Image.fromarray(np.clip(np.rint(s), 0, 255).astype(np.uint8))
        # Pillow only dithers when it maps onto a given palette: build the palette, then map with dither
        q = rgb.quantize(palette=rgb.quantize(colors=GIF_COLORS, method=Image.Quantize.MEDIANCUT), dither=dith)
        if i:
            diff = np.abs(s - scenes[i - 1]).max(2) > 3
            diff = np.asarray(Image.fromarray((diff * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
            # palette from the changing pixels only, so the colours go where the new model is
            sub = rgb.copy()
            sub_arr = np.asarray(sub).copy()
            sub_arr[~diff] = sub_arr[diff][0] if diff.any() else 0
            q = rgb.quantize(palette=Image.fromarray(sub_arr).quantize(colors=GIF_COLORS, method=Image.Quantize.MEDIANCUT),
                             dither=dith)
            idx = np.asarray(q).copy()
            idx[~diff] = 255
            pal = q.getpalette()[:GIF_COLORS * 3] + [0, 0, 0] * (256 - GIF_COLORS)
            q = Image.fromarray(idx.astype(np.uint8), "P")
            q.putpalette(pal)
        ims.append(q)
    p = OUT / "o4-lifestyle.gif"
    ims[0].save(p, save_all=True, append_images=ims[1:], duration=[2600, 2000, 2000], loop=0,
                optimize=False, disposal=1, transparency=255)
    print(f"  {p.name:40s} {ims[0].size}  {len(ims)} frames  {p.stat().st_size / 1024:6.1f} KB")
    save(c.to_image(scenes[0]), "o4-lifestyle-still.jpg", limit=60 * 1024, q=82)   # D4 fallback, recomposed


JOBS = {
    "o3-hero": o3_hero, "o3-panels": o3_panels, "o3-edges": o3_edges,
    "o4-hero": o4_hero, "o4-frames": o4_frames, "o4-edges": o4_edges, "o4-gif": o4_gif,
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="*", choices=sorted(JOBS))
    a = ap.parse_args()
    for k in a.only or JOBS:
        print(f"[{k}] {JOBS[k].__doc__.strip().splitlines()[0]}")
        JOBS[k]()


if __name__ == "__main__":
    main()
