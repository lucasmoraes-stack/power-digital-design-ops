"""RKU26013 V4 (2026-10-13): one ChatGPT room per industry, panel layout in every size.

Plates: img/raw/<ind>-plate-gpt.png (Lucas generated them in ChatGPT from img/gpt-refs/<ind>/:
same locked room, props per industry, the TV ad already on the screen, glass blown-out white).

Per industry:
  1. find the TV screen (the purple rectangle) on the plate
  2. key the drawn city (compose.city) into the glass with make.glass_mask (no recolor_top: these
     rooms already show the sideboard almost straight on, and it broke the TV foot here)
  3. every size = a lilac panel with lockup, headline and CTA (the V3 16:9 strategy) + the room,
     cropped closer on the TV but keeping the plant, the table props and the armchair
  4. on-screen ad copy (headline, line, button, "Ad · 0:15") set in HTML on the screen's empty left

    python -I v4.py                 -> all industries, all sizes
    python -I v4.py pet             -> one industry
    python -I v4.py pet 1x1         -> one industry, one size
"""
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "01-brand"))
sys.path.insert(0, str(HERE))
from rk_common import font_face, img_data, lockup  # noqa: E402
from compose import city  # noqa: E402
from make import CHROME, EXPORT, IND, RAW, glass_mask  # noqa: E402

BG, BUILD = HERE / "img" / "v4", HERE / "build" / "v4"
T = {"bg": "#EFE6FF", "ink": "#20004C", "hi": "#4F01A3", "rk": "#4F01A3", "am": "#646464",
     "btn": "#4F01A3", "shadow": "rgba(32,0,76,.24)"}


def find_screen(a):
    """The lit TV screen: the largest dark-purple rectangle. Returns (x0, y0, x1, y1), plate px."""
    a = a.astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = ((b - g > 45) & (a.mean(2) < 170)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    i = max(range(1, n), key=lambda i: st[i, 4])
    x, y, w, h = st[i, :4]
    sub = lab[y:y + h, x:x + w] == i                     # trim to rows/cols that are mostly screen
    rows = np.where(sub.mean(1) > .6)[0]; cols = np.where(sub.mean(0) > .6)[0]
    x0, y0, x1, y1 = int(x + cols.min()), int(y + rows.min()), int(x + cols.max() + 1), int(y + rows.max() + 1)
    # products on the right (croissants, a cream armchair) are not purple: the screen's real right
    # edge is where the black top bezel ends, just above the screen
    mx = a.max(2)
    for yy in range(y0 - 1, y0 - 8, -1):
        if (mx[yy, x0 + 4:x0 + 40] < 70).mean() > .9:
            e = x0 + 4
            while e < a.shape[1] and (mx[yy - 1:yy + 2, e] < 70).any():
                e += 1
            x1 = max(x1, e - 4)
            break
    return x0, y0, x1, y1


def bezel(a, s):
    """The TV body around the screen: grow outwards while the edge row/column is dark."""
    x0, y0, x1, y1 = s
    mn = a.max(2)
    def dark(v):
        return (v < 70).mean() > .8
    while dark(mn[y0 - 1, x0:x1]): y0 -= 1
    while dark(mn[y1, x0:x1]): y1 += 1
    while dark(mn[y0:y1, x0 - 1]): x0 -= 1
    while dark(mn[y0:y1, x1]) or dark(mn[y0:y0 + 20, x1]): x1 += 1
    return x0, y0, x1, y1


def fix_stand_ends(a, k, tv):
    """Lucas 2026-10-13: at both ends of the sideboard a triangle of white glass was left next to
    the top's slanted end (make.top_geometry sits 6-8 px high on these rooms, so its 'no key below
    the top' rule covered glass). In a band around the top, glass is re-found from the pixels: bright
    neutral glass (min >= 246) connected to the open glass above, never the top surface (<= 244)
    nor the bright lip on the top's front edge, then a soft edge on its border."""
    import make
    g = make.top_geometry(a, tv)
    if g is None:
        return k
    _, ls, _, fx0, fx1 = g
    h, w = k.shape
    mn = a.min(2); sat = a.max(2) - mn
    y0, y1 = max(0, ls - 12), min(h, ls + 45)
    x0, x1 = max(0, fx0 - 60), min(w, fx1 + 60)
    bright = ((mn >= 246) & (sat < 12))[y0:y1, x0:x1].astype(np.uint8)
    # the top's bright front lip: within the face span, from 2 rows above the dark front face down
    face = np.full(x1 - x0, y1 - y0)
    for j, x in enumerate(range(x0, x1)):
        col = mn[ls:y1, x] < 180
        for i in range(len(col) - 2):
            if col[i:i + 3].all():
                face[j] = ls + i - y0
                break
    for j, x in enumerate(range(x0, x1)):
        if fx0 + 3 <= x < fx1 - 3:
            bright[max(0, face[j] - 2):, j] = 0
    n, lab = cv2.connectedComponents(bright, connectivity=4)
    seeds = set(np.unique(lab[:4][bright[:4] > 0]))
    glass = np.isin(lab, list(seeds - {0}))
    soft = cv2.dilate(glass.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    neutral = np.clip((30 - sat[y0:y1, x0:x1]) / 12, 0, 1)
    alpha = np.where(glass, 1.0, soft * np.clip((mn[y0:y1, x0:x1] - 228) / 20, 0, 1) * neutral)
    k = k.copy()
    k[y0:y1, x0:x1] = np.maximum(k[y0:y1, x0:x1], alpha)
    return k


def fill_slivers(a, k, box, tv, r=4):
    """Lucas 2026-10-13: thin white lines left in the city (pane edges and frame bevels catch the
    light, so the matte read them as objects). A light, neutral pixel that is less than ~2 px thick
    and has the city on both sides (above and below; or left and right, where one side may be a
    black window post: the bevel highlight beside the post) within r px is glass."""
    gx0, gy0, gx1, gy1 = box
    mn = a.min(2); sat = a.max(2) - mn
    light = (mn >= 195) & (sat < 26) & (k < .95)
    kk = k > .5
    def near(m, dy, dx):                                  # any of m within r px in one direction
        out = np.zeros_like(m)
        for i in range(1, r + 1):
            out |= np.roll(m, (dy * i, dx * i), (0, 1))
        return out
    dark = mn < 90                                        # the black window posts
    edge = kk | dark
    vert = (near(kk, 0, 1) & near(edge, 0, -1)) | (near(edge, 0, 1) & near(kk, 0, -1))  # city one side,
                                                          # city or a post the other: vertical sliver
    horz = near(kk, 1, 0) & near(kk, -1, 0)               # city above and below: horizontal sliver
    thin_v = light & ~cv2.morphologyEx(light.astype(np.uint8), cv2.MORPH_OPEN, np.ones((1, 4), np.uint8)).astype(bool)
    thin_h = light & ~cv2.morphologyEx(light.astype(np.uint8), cv2.MORPH_OPEN, np.ones((4, 1), np.uint8)).astype(bool)
    fix = (thin_v & vert) | (thin_h & horz)
    win = np.zeros_like(fix); win[gy0 - 4:gy1 + 4, gx0 - 4:gx1 + 4] = True
    win[tv[1] - 2:tv[3] + 2, tv[0] - 2:tv[2] + 2] = False
    fix &= win
    k = k.copy()
    k[fix] = 1
    return k


def close_posts(o, box, tv, r=4):
    """The window posts are a double profile (black, a 2 px light seam, black); in the ad the seam
    reads as white glass left in the city (Lucas 2026-10-13). A light pixel run of 3 px or less
    with the black post on both sides takes the post's own colour from its neighbours."""
    gx0, gy0, gx1, gy1 = box
    mn = o.min(2)
    sat = o.max(2) - mn
    dark = (mn < 90) & (sat < 30)                         # black post, not the dark purple city
    light = mn >= 110
    out = o.copy()
    ys, xs = np.where(light[gy0:gy1, gx0:gx1])
    for y, x in zip(ys + gy0, xs + gx0):
        if tv[1] - 2 <= y < tv[3] + 2 and tv[0] - 2 <= x < tv[2] + 2:
            continue
        L = [x - i for i in range(1, r + 1) if x - i >= 0 and dark[y, x - i]]
        R = [x + i for i in range(1, r + 1) if x + i < o.shape[1] and dark[y, x + i]]
        if L and R and R[0] - L[0] <= 5:                  # gap between the dark sides <= 3 px
            out[y, x] = (o[y, L[0]] + o[y, R[0]]) / 2
            continue
        # a white rim on the post's edge: post on one side, the coloured city 2-3 px on the other
        if sat[y, x] < 22 and mn[y, x] >= 150:
            for d in (-1, 1):
                p = [x + d * i for i in (1, 2) if 0 <= x + d * i < o.shape[1] and dark[y, x + d * i]]
                q = x - d * 3
                if p and 0 <= q < o.shape[1] and sat[y, q] > 30:
                    out[y, x] = o[y, p[0]]
                    break
    return out


def plate(ind):
    """City keyed into the glass, ad untouched. Returns (image, screen box) at plate px."""
    a = np.asarray(Image.open(RAW / f"{ind}-plate-gpt.png").convert("RGB")).astype(np.float32)
    scr = find_screen(a)
    tv = bezel(a, scr)
    k, (gx0, gy0, gx1, gy1) = glass_mask(a, tv)
    k = fix_stand_ends(a, k, tv)
    k = fill_slivers(a, k, (gx0, gy0, gx1, gy1), tv)
    art = np.full_like(a, 255)
    art[gy0:gy1, gx0:gx1] = np.asarray(city(gx1 - gx0, gy1 - gy0)).astype(np.float32)
    keep = a[tv[1]:tv[3], tv[0]:tv[2]].copy()
    a = a + k[..., None] * (art - 255)
    a = close_posts(a, (gx0, gy0, gx1, gy1), tv)
    a[tv[1]:tv[3], tv[0]:tv[2]] = keep                   # the TV itself is never touched
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)), scr


# Meta sizes: lilac panel on top (lockup, headline, CTA, left-aligned like the 16:9), room below.
# The room is the plate cropped around the TV: `zoom` trims the sides, `bottom` = plate rows kept
# under the TV bottom (enough for the coffee-table props), the rest of the height goes above the
# TV (window and city). safe = Meta UI zones (9:16) the copy stays out of.
SIZES = {   # 2026-10-13 (Lucas): bigger 2-line headlines, shorter room, closer on the TV (dog stays partly in)
    "1x1":  {"w": 1440, "h": 1440, "panel": 600, "pad": 88, "hl": 118, "lines": 2, "cta": 36, "lk": 340, "zoom": 1.25, "bottom": 300, "safe": (0, 0)},
    "4x5":  {"w": 1440, "h": 1800, "panel": 630, "pad": 96, "hl": 118, "lines": 2, "cta": 38, "lk": 360, "zoom": 1.25, "bottom": 380, "safe": (0, 0)},
    "9x16": {"w": 1440, "h": 2560, "panel": 1090, "pad": 112, "padt": 40, "hl": 142, "lines": 3, "cta": 48, "lk": 480, "zoom": 1.35, "shift": 30, "bottom": 450, "safe": (267, 333)},
}
CANVAS = {"1x1": "1440x1440", "4x5": "1440x1800", "9x16": "1440x2560"}
_PLATES = {}


def keyed(ind):
    if ind not in _PLATES:
        BG.mkdir(parents=True, exist_ok=True)
        p = BG / f"{ind}-plate.png"
        im, scr = plate(ind)
        im.save(p)
        _PLATES[ind] = (im, scr)
    return _PLATES[ind]


def room(ind, size):
    """Room crop for a Meta size. Returns (image path, screen box in canvas px)."""
    S = SIZES[size]
    im, scr = keyed(ind)
    pw, ph = im.size
    rw, rh = S["w"], S["h"] - S["panel"]
    if S["zoom"]:
        cw = pw / S["zoom"]
    else:                                                    # tall: plate height under the ceiling band
        cw = min(pw, (ph - S["y0"]) * rw / rh)                # (rows from y0 down), sides trimmed
    ch = cw * rh / rw
    cx = (scr[0] + scr[2]) / 2 + S.get("shift", 0)            # shift: plate px right, to keep the dog's head
    x0 = min(max(cx - cw / 2, 0), pw - cw)
    y1 = min(ph, scr[3] + S["bottom"])
    y0 = max(0, y1 - ch); y1 = y0 + ch
    if y1 > ph:
        y0, y1 = ph - ch, ph
    s = rw / cw
    out = im.crop((round(x0), round(y0), round(x0 + cw), round(y1))).resize((rw, rh), Image.LANCZOS)
    path = BG / f"{ind}-{size}.png"
    out.save(path)
    box = (round((scr[0] - x0) * s), round((scr[1] - y0) * s + S["panel"]),
           round((scr[2] - x0) * s), round((scr[3] - y0) * s + S["panel"]))
    return path, box


def screen_html(box):
    x0, y0, x1, y1 = box
    sw, sh = x1 - x0, y1 - y0
    css = f""".scr{{position:absolute;left:{x0}px;top:{y0}px;width:{sw}px;height:{sh}px}}
.scr .t{{position:absolute;left:{round(sw * .065)}px;top:{round(sh * .2)}px;display:flex;flex-direction:column;gap:{round(sw * .022)}px;color:#fff}}
.scr h2{{margin:0;font-weight:700;font-size:{round(sw * .058)}px;line-height:1.08;letter-spacing:-.01em}}
.scr p{{margin:0;font-weight:400;font-size:{round(sw * .028)}px;line-height:1.3;color:#E9DEFF}}
.scr .b{{align-self:flex-start;margin-top:{round(sw * .012)}px;background:#fff;color:#4F01A3;font-weight:700;font-size:{round(sw * .025)}px;padding:{round(sw * .012)}px {round(sw * .027)}px;border-radius:999px}}
.scr .ad{{position:absolute;right:{round(sw * .03)}px;top:{round(sw * .025)}px;font-size:{round(sw * .018)}px;font-weight:500;color:#fff;background:rgba(0,0,0,.35);padding:{round(sw * .006)}px {round(sw * .014)}px;border-radius:6px}}"""
    return css


def html(ind, size, img, box):
    S, d = SIZES[size], IND[ind]
    W, H, P = S["w"], S["h"], S["panel"]
    h1, sub, adcta = d["ad"]
    words = ["Put your", f'<b>{d["word"]}</b>', "in their", "living room."]
    hl = {2: f'<span>{words[0]} {words[1]}</span><span>{words[2]} {words[3]}</span>',
          3: f'<span>{words[0]}</span><span>{words[1]}</span><span>{words[2]} {words[3]}</span>'}[S["lines"]]
    top, bot = S["safe"]
    cta = S["cta"]
    return f"""<!doctype html><meta charset="utf-8"><title>RKU26013 {ind} {size} V4</title>
<style>
{font_face()}
html,body{{margin:0;background:#fff}}
.f{{position:relative;width:{W}px;height:{H}px;overflow:hidden;font-family:"Roku Display",sans-serif}}
.i{{position:absolute;left:0;top:{P}px;width:{W}px;height:{H - P}px;background:url({img_data(img, "image/png")}) 0 0/{W}px {H - P}px}}
.p{{position:absolute;left:0;top:0;width:{W}px;height:{P}px;box-sizing:border-box;padding:{top + S.get("padt", S["pad"])}px {S["pad"]}px {S.get("padt", S["pad"]) + 24 if top else S["pad"]}px;background:{T["bg"]};
   display:flex;flex-direction:column;justify-content:center;gap:{round(S["hl"] * .4)}px}}
.p>*{{flex-shrink:0}}
.lk{{width:{S["lk"]}px;height:auto;display:block}}
.hl{{margin:0;font-weight:700;font-size:{S["hl"]}px;line-height:1.04;letter-spacing:-.025em;color:{T["ink"]}}}
.hl span{{display:block;white-space:nowrap}}
.hl b{{font-weight:700;color:{T["hi"]}}}
.cta{{align-self:flex-start;display:flex;align-items:center;gap:{round(cta * .5)}px;background:{T["btn"]};color:#fff;font-weight:700;font-size:{cta}px;line-height:1;
     padding:{round(cta * .66)}px {round(cta * 1.3)}px;border-radius:{round(cta * .35)}px;box-shadow:0 {round(cta * .3)}px {round(cta * .9)}px {T["shadow"]};white-space:nowrap}}
.cta svg{{width:{round(cta * .5)}px;height:{round(cta * .8)}px}}
{screen_html(box)}
</style>
<div class="f">
  <div class="i"></div>
  <div class="scr"><span class="ad">Ad · 0:15</span><div class="t"><h2>{h1}</h2><p>{sub}</p><span class="b">{adcta}</span></div></div>
  <div class="p">
    {lockup("lk", T["rk"], T["am"])}
    <h1 class="hl">{hl}</h1>
    <div class="cta">Learn more<svg viewBox="0 0 10 16" aria-hidden="true"><path d="M2 1.5 8.5 8 2 14.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
  </div>
</div>"""


def fname(ind, size):
    return f"RKU26013-SellItOnRoku-{CANVAS[size]}-Static-Meta-{IND[ind]['code']}-V4"


def build(ind, size):
    S = SIZES[size]
    img, box = room(ind, size)
    BUILD.mkdir(parents=True, exist_ok=True); EXPORT.mkdir(exist_ok=True)
    page = BUILD / f"{ind}-{size}.html"
    page.write_text(html(ind, size, img, box), encoding="utf8")
    png = EXPORT / f"{fname(ind, size)}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--virtual-time-budget=3000", f"--window-size={S['w']},{S['h']}", f"--screenshot={png}", page.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return png


def build_ctv(ind):
    """16:9 = the V3 split (split.py) on the V4 room."""
    import split
    split.BG, split.BUILD = BG, BUILD
    split.plate = lambda i, tv_on=True: keyed(i)
    return split.build(ind, name=f"{ind}-16x9.html",
                       png_name=f"RKU26013-SellItOnRoku-{split.W}x{split.H}-Static-CTV-{IND[ind]['code']}-V4.png")


if __name__ == "__main__":
    inds = [sys.argv[1]] if len(sys.argv) > 1 else list(IND)
    sizes = [sys.argv[2]] if len(sys.argv) > 2 else list(SIZES) + ["16x9"]
    for ind in inds:
        for size in sizes:
            print((build_ctv(ind) if size == "16x9" else build(ind, size)).name)
