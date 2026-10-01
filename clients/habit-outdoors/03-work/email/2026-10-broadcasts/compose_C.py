"""compose_C.py - October 2026 Broadcasts, Designer C: every asset of email 05 Shadow Series (assets/o5-*).

Imports the kit's compose.py (never edited) and redirects its output folder to this batch's assets/,
so nothing in the shared kit is written and nothing collides with compose_A.py / compose_B.py.
Kit textures are read from email-kit/assets; o5-* files are written and read here.

Run from anywhere:
    python clients/habit-outdoors/03-work/email/2026-10-broadcasts/compose_C.py
    python .../compose_C.py --only hero icons

Jobs (run "tex" before "products" and "edges": they bake the water tile):
    tex       o5-tex-water.jpg        Patriot Blue water tile, fine ripples only (round 2 recipe of r2-04-tex-water)
    hero      o5-hero.jpg             E24 hero, orig-hunt40 graded cold and dark, tears into kit topo-tapshoe
    edges     o5-edge-topo-water.jpg, o5-edge-water-footer.jpg   E18 textured torn edges with paper rim
    products  o5-prod-*.jpg           product bleeding off the email edge, on the water tile (ref C rows)
    icons     o5-icon-*.png           4 thin-line icons, 2px stroke at 48px (96px file), #FEF4C6 + orange
  round 2 (rev-oct-05, 2026-09-25; the HTML now uses these + tex, icons and o5-edge-water-footer):
    grad      o5-tex-topo-grad.jpg    Tap Shoe -> Patriot Blue gradient with the kit topo lines (attribute band)
    hero2     o5-hero-r2.jpg          same photo, hunter above the label, base continues into the grad band
    packs     o5-pack-*.jpg           checkerboard packshots on flat panels sampled from rev-oct-05
    edge2     o5-edge-water-footer-r2.jpg   water -> footer tear as drawn in rev-oct-05 (no paper rim)

Mechanics kept from round 2 (../2026-broadcasts/compose_03-04.py, not imported: it rewires compose.py
at import time): band tds use background-size:100% auto; images baked on a texture only sit on a
fine-grain tile (the kit Patriot tile has 13-level patches, so the water tile is regenerated without
them); a tear always has the lower sheet over the upper one (shadow above, light fibre rim below).
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
KIT_ASSETS = c.KIT / "assets"
c.ASSETS = OUT                                     # compose.py writes to c.ASSETS at call time

PATRIOT, TAPSHOE = c.PATRIOT, c.TAPSHOE
CREAM, ORANGE = "#FEF4C6", "#FF6400"
MAX_IMG = 150 * 1024
PACK = {  # products.json email "05", variant packshots (Mossy Oak Terra Coyote / M)
    "midlayer": "men-s-mid-layer-jacket--45471499518234",
    "pant": "men-s-windproof-fleece-pant--45471564824858",
    "jacket": "men-s-windproof-fleece-jacket--45471553618202",
}


def _tex_path(name: str) -> Path:
    f = c.TEXTURES[name][0]
    return (OUT if f.startswith("o5-") else KIT_ASSETS) / f


c.tex_path = _tex_path                             # load_tile -> tex_path at call time
c.TEXTURES["o5-water"] = ("o5-tex-water.jpg", PATRIOT, "tile", "white, #E2DDD9 body, orange 24px+")


def pn(w, h, lx, seed, ly=None):
    return c.periodic_noise(w, h, lx, ly or lx, seed)


def save(arr_or_img, name, limit=MAX_IMG, q=76, floor=50, sub=2):
    img = arr_or_img if isinstance(arr_or_img, Image.Image) else c.to_image(arr_or_img)
    p = c.save_jpg_under(img, OUT / name, limit, q=q, floor=floor, subsampling=sub)
    print(f"  {p.name:34s} {Image.open(p).size}  {p.stat().st_size / 1024:6.1f} KB")
    return p


def tile(name, h, y0=0, w=1200):
    t = c.load_tile(name)
    reps = math.ceil((y0 + h) / t.shape[0]) + 1
    return np.concatenate([t] * reps, axis=0)[y0:y0 + h, :w].copy()


def widths(w, seed, lo=1.5, hi=5.5):
    rng = np.random.default_rng(seed)
    n = np.convolve(rng.normal(0, 1, w + 60), np.exp(-np.linspace(-2.5, 2.5, 41) ** 2) / 14.9, "same")[30:30 + w]
    n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    return lo + (hi - lo) * n


def rim(arr, ys, y_off, seed, alpha=0.55, color=(228, 223, 216)):
    """Light paper-fibre rim just below a torn line (the lower sheet's edge)."""
    h, w = arr.shape[:2]
    yy = np.arange(h, dtype=np.float32)[:, None]
    d = yy - (np.array(ys, np.float32)[None, :] + y_off)
    m = ((d >= -0.5) & (d <= widths(w, seed)[None, :])).astype(np.float32)
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255
    m = (m * (0.7 + 0.3 * np.random.default_rng(seed + 9).random((h, w)).astype(np.float32)) * alpha)[:, :, None]
    return arr * (1 - m) + np.array(color, np.float32) * m


def torn_join(up, lo, ys, seed, shadow=(7.0, 0.4), rim_alpha=0.55):
    """lower sheet over the upper one along ys: shadow above the line, rim below, a few specks."""
    h, w = up.shape[:2]
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon([(0, h)] + [(x, y) for x, y in enumerate(ys)] + [(w, h)], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[:, :, None] / 255
    yy = np.arange(h, dtype=np.float32)[:, None]
    d = np.array(ys, np.float32)[None, :] - yy
    up = up * (1 - np.where(d > 0, np.exp(-d / shadow[0]), 0) * shadow[1])[:, :, None]
    out = rim(up * (1 - a) + lo * a, ys, 0, seed, alpha=rim_alpha)
    img = c.to_image(out)
    dr, rnd = ImageDraw.Draw(img), random.Random(seed + 3)
    spot = tuple(int(v) for v in np.median(lo.reshape(-1, 3), 0))
    for _ in range(w // 40):
        x = rnd.randrange(w)
        y, r = ys[x] - rnd.uniform(3, 10), rnd.choice((1.2, 1.6, 2.2))
        dr.ellipse((x - r, y - r, x + r, y + r), fill=spot + (255,))
    return np.asarray(img.convert("RGB"), np.float32)


# ---------------------------------------------------------------- jobs

def job_tex():
    """o5-tex-water.jpg: Patriot Blue, fine horizontal streaks bent by a slow warp + sparse glints, no patches."""
    W, H = c.TEX_W, c.TEX_H
    wv = np.broadcast_to(np.array(c.rgb(PATRIOT), np.float32), (H, W, 3)).copy()
    rip = pn(W, H, 44, 151, 1.6) * 2.6 + pn(W, H, 16, 152, 1.0) * 1.3
    warp = pn(W, H, 60, 153, 40) * 6.0
    yy = (np.arange(H)[:, None] + np.rint(warp).astype(int)) % H
    rip = rip[yy, np.broadcast_to(np.arange(W)[None, :], (H, W))]
    glint = np.clip(pn(W, H, 5, 154, 0.8) - 2.9, 0, None) * 14
    wv += (rip + glint)[:, :, None] * np.array([0.72, 0.88, 1.15], np.float32) + (pn(W, H, 0.75, 155) * 2.6)[:, :, None]
    wv += np.array(c.rgb(PATRIOT), np.float32) - wv.reshape(-1, 3).mean(0)
    p = save(wv, "o5-tex-water.jpg", limit=92 * 1024, q=70)
    print("     ", c.contrast_report(p, ["#FFFFFF", "#E2DDD9", ORANGE], blur=0))


def job_hero():
    """o5-hero.jpg: orig-hunt40 (bowhunter from behind, forest), graded late season: desaturated, cold, dark
    canopy for the headline; bottom melts into Tap Shoe paper and tears into the kit topo-tapshoe tile."""
    ph = c.lifestyle("orig-hunt40-hunter-forest-back.jpg")
    a = np.asarray(ph, np.float32)
    grey = a.mean(2, keepdims=True)
    a = (a * 0.55 + grey * 0.45) * np.array([0.86, 0.93, 1.02], np.float32) * 0.82    # gold fall -> cold late season
    a = 255 * (np.clip(a / 255, 0, 1) ** 1.12)                                          # a bit more contrast in the shadows
    # the backlit canopy above the hunter (original rows 0..~900, the head is at ~980) becomes a dark
    # pre-dawn wood: highlights soft-clipped to ~100, fading out before the head, so the live headline
    # (white) keeps AA on the whole text area
    h = a.shape[0]
    yy = np.arange(h, dtype=np.float32)[:, None, None]
    m = 1 - c.smooth(np.clip((yy - 800) / 220, 0, 1))
    clip = 84 * np.tanh(a / 84)
    a = a * (1 - m) + (clip * 0.9) * m
    soft = np.asarray(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3.2)), np.float32)
    a = a * (1 - m * 0.85) + soft * m * 0.85                                            # dim wood goes soft (mist, weight)
    ph = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    size, tear_y, seed = (1200, 1600), 1572, 501
    ys = c.torn_line(size[0], 12, amp=9, seed=seed + 2)
    y_off = tear_y - 24
    orig = c.save_jpg_under

    def patched(im, path, limit, **k):              # paper-fibre rim on compose.py's own baked tear
        arr = rim(np.asarray(im.convert("RGB"), np.float32), ys, y_off, 505)
        return orig(c.to_image(arr), path, limit, **k)

    c.save_jpg_under = patched
    try:
        p = c.compose_full_bleed_hero(ph, "o5-hero.jpg", size=size, photo_w=1500, photo_y=40,
                                      extend_top="fog", top_shade=(880, 0.6), fade=(1360, 1540),
                                      base="paper-tapshoe", tear_y=tear_y, next_tex="topo-tapshoe",
                                      grain_sd=1.5, seed=seed,
                                      text_boxes={"desktop": (80, 150, 1120, 860), "mobile": (60, 120, 1140, 1000)})
    finally:
        c.save_jpg_under = orig
    return p


def edge(top, bottom, out, h=80, seed=0, amp=10):
    up = c.tile_rows(top, h, end=True)
    lo = c.tile_rows(bottom, h, end=c._continues(bottom))
    ys = c.torn_line(1200, h * 0.45, amp=amp, seed=seed)
    return save(torn_join(up, lo, ys, seed), out, limit=30 * 1024, q=78, sub=0)


def job_edges():
    """E18 textured torn edges: kit topo-tapshoe -> o5 water, o5 water -> flat Tap Shoe footer."""
    edge("topo-tapshoe", "o5-water", "o5-edge-topo-water.jpg", seed=511)
    edge("o5-water", "flat:#2A2B2D", "o5-edge-water-footer.jpg", seed=512)


def haze(arr, cx, cy, rx, ry, color, strength, seed, window=200):
    h, w = arr.shape[:2]
    yy = (np.arange(h, dtype=np.float32)[:, None] - cy) / ry
    xx = (np.arange(w, dtype=np.float32)[None, :] - cx) / rx
    m = np.exp(-(xx ** 2 + yy ** 2))
    ys_, xs_ = np.arange(h, dtype=np.float32), np.arange(w, dtype=np.float32)
    m = m * c.smooth(np.clip(np.minimum(ys_, h - 1 - ys_) / window, 0, 1))[:, None]
    m = m * np.clip(1 + (pn(w, h, 90, seed) * 0.5 + pn(w, h, 30, seed + 1) * 0.25) * 0.6, 0, 1.6)
    m = np.clip(m * strength, 0, 1)[:, :, None]
    return arr * (1 - m) + np.array(c.rgb(color), np.float32) * m


def bleed_card(key, out, *, bleed, height, cx, cy, angle, seed, size=(600, 820)):
    """One product big on a mist glow over the water tile, cut by the image side that touches the email
    edge (`bleed`); the other three sides fade back to the plain tile (fine grain only, tile mean), so the
    image border never shows on the td background."""
    W, H = size
    x0 = 0 if bleed == "left" else 1200 - W          # same tile columns the td shows behind this cell
    base = tile("o5-water", H, w=1200)[:, x0:x0 + W]
    low = np.asarray(c.to_image(base).convert("RGB").filter(ImageFilter.GaussianBlur(40)), np.float32)
    base = base - low + c.load_tile("o5-water").reshape(-1, 3).mean(0)
    arr = haze(base.copy(), cx if bleed != "left" else cx + 40, cy, W * 0.42, H * 0.34, "#46527A", 0.55, seed)
    img = c.to_image(arr)
    c.place(img, c.fit(c.load_packshot(PACK[key]), h=height), cx, cy, angle, shadow=(10, 22, 28, 0.6))
    arr = np.asarray(img.convert("RGB"), np.float32)
    ht, wt = np.arange(H, dtype=np.float32), np.arange(W, dtype=np.float32)
    wgt = (c.smooth(np.clip(ht / 80, 0, 1)) * c.smooth(np.clip((H - 1 - ht) / 80, 0, 1)))[:, None]
    far = c.smooth(np.clip(((W - 1 - wt) if bleed == "left" else wt) / 110, 0, 1))[None, :]
    wgt = (wgt * far)[:, :, None]
    return save(arr * wgt + base * (1 - wgt), out, limit=110 * 1024, q=78)


def job_products():
    """Ref C rows, client order: Mid Layer Hooded Jacket (bleeds left), Windproof Fleece Pant (bleeds right),
    Windproof Fleece Jacket (bleeds left). 600x820 files, shown 300x410."""
    bleed_card("midlayer", "o5-prod-midlayer.jpg", bleed="left", height=700, cx=230, cy=410, angle=-4, seed=521)
    bleed_card("pant", "o5-prod-pant.jpg", bleed="right", height=760, cx=390, cy=410, angle=5, seed=522)
    bleed_card("jacket", "o5-prod-jacket.jpg", bleed="left", height=680, cx=220, cy=410, angle=-5, seed=523)


# ---- icons: drawn at 4x (384px, 16px stroke) and reduced to 96px (= 2px stroke at 48px)

S = 4
SW = 4 * S


def _canvas():
    return Image.new("RGBA", (96 * S, 96 * S), (0, 0, 0, 0))


def _line(d, pts, col, w=SW):
    pts = [(x * S, y * S) for x, y in pts]
    d.line(pts, fill=col, width=w, joint="curve")
    r = w / 2
    for x, y in (pts[0], pts[-1]):
        d.ellipse((x - r, y - r, x + r, y + r), fill=col)


def _arc_pts(cx, cy, r, a0, a1, n=48):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in np.linspace(a0, a1, n)]


def _save_icon(img, name):
    img = img.resize((96, 96), Image.LANCZOS)
    p = OUT / name
    img.save(p, optimize=True)
    print(f"  {p.name:34s} {img.size}  {p.stat().st_size / 1024:6.1f} KB")


def job_icons():
    """o5-icon-rain / scent / grid / wind.png: thin-line pictograms (guide p.21 idea: line icon on a base of
    2 strokes), cream #FEF4C6 with one orange stroke each. Transparent, for the Patriot water band."""
    cr, orr = c.rgb(CREAM) + (255,), c.rgb(ORANGE) + (255,)

    def base(d):                                   # the 2-stroke base of the guide's tech icons
        _line(d, [(30, 86), (66, 86)], orr)
        _line(d, [(38, 92), (58, 92)], orr, w=3 * S)

    # rain: a drop, with a highlight arc inside
    im = _canvas(); d = ImageDraw.Draw(im)
    drop = [(48, 10)] + [(48 + 22 * math.cos(math.radians(a)), 52 + 22 * math.sin(math.radians(a)))
                         for a in np.linspace(-38, 218, 60)] + [(48, 10)]
    _line(d, drop, cr)
    _line(d, _arc_pts(48, 52, 12, 100, 170, 20), cr, w=3 * S)
    base(d); _save_icon(im, "o5-icon-rain.png")

    # scent: a leaf with its vein
    im = _canvas(); d = ImageDraw.Draw(im)
    left = _arc_pts(74, 64, 42, 180, 262, 40)             # from the tip down to the stem, both sides
    right = _arc_pts(22, 22, 42, 0, 82, 40)
    _line(d, [(p[0], p[1]) for p in left], cr)
    _line(d, [(p[0], p[1]) for p in right], cr)
    _line(d, [(24, 72), (70, 24)], cr, w=3 * S)
    _line(d, [(14, 80), (26, 70)], cr)
    base(d); _save_icon(im, "o5-icon-scent.png")

    # grid fleece: rounded square with a 3x3 grid
    im = _canvas(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20 * S, 14 * S, 76 * S, 70 * S), radius=8 * S, outline=cr, width=SW)
    for v in (38.7, 57.3):
        _line(d, [(v, 18), (v, 66)], cr, w=3 * S)
        _line(d, [(24, v - 4.7), (72, v - 4.7)], cr, w=3 * S)
    base(d); _save_icon(im, "o5-icon-grid.png")

    # wind: three gusts with curls
    im = _canvas(); d = ImageDraw.Draw(im)
    _line(d, [(12, 26), (58, 26)], cr)
    _line(d, _arc_pts(58, 18, 8, 90, -150, 36), cr)
    _line(d, [(12, 44), (74, 44)], cr)
    _line(d, _arc_pts(74, 36, 8, 90, -150, 36), cr)
    _line(d, [(12, 62), (52, 62)], cr)
    _line(d, _arc_pts(52, 70, 8, -90, 150, 36), cr)
    base(d); _save_icon(im, "o5-icon-wind.png")


JOBS = {"tex": job_tex, "hero": job_hero, "edges": job_edges, "products": job_products, "icons": job_icons}


# ---------------------------------------------------------------- round 2 (2026-09-25, rev-oct-05-shadow-series.png)
# Owner's revised layout: hero text lower on the photo (dark label + BITE / BACK), attribute band on a Tap Shoe ->
# Patriot Blue topo gradient that flows from the hero with no tear, checkerboard 300+300 (packshot on a flat
# panel sampled from the revision image, info box on the o5 water tile). Same topo line detail in hero base and band
# (kit tex-topo-tapshoe rows: hero ends on the tile's last rows, the band starts at row 0), so the join is seamless.

R2_H = 1400                                        # hero file height (700 shown) and band texture height
PANELS = {"midlayer": "#A69A89", "pant": "#ABB1B3", "jacket": "#5A4538"}   # medians of the rev-oct-05 panels


def topo_detail(rows: slice) -> np.ndarray:
    """Topo line detail of the kit tex-topo-tapshoe tile (tile minus its mean), rows `rows`."""
    t = c.load_tile("topo-tapshoe")
    return t[rows] - t.reshape(-1, 3).mean(0)


def job_grad():
    """o5-tex-topo-grad.jpg: Tap Shoe -> Patriot Blue gradient with the kit topo lines (1200x1400, shown 600 wide,
    background-size:100% auto, no repeat, bgcolor Patriot: the image bottom is already Patriot)."""
    W, H = 1200, R2_H
    t = c.smooth(np.clip(np.arange(H, dtype=np.float32) / (H * 0.86), 0, 1))[:, None, None]
    top, bot = np.array(c.rgb(TAPSHOE), np.float32), np.array(c.rgb(PATRIOT), np.float32)
    arr = top * (1 - t) + bot * t
    arr = np.broadcast_to(arr, (H, W, 3)).copy()
    arr += topo_detail(slice(0, H)) * 0.85
    arr += (pn(W, H, 0.75, 561) * 1.8)[:, :, None]
    p = save(arr, "o5-tex-topo-grad.jpg", limit=90 * 1024, q=72)
    print("     ", c.contrast_report(p, ["#FFFFFF", "#E2DDD9", ORANGE], blur=0))


def job_hero2():
    """o5-hero-r2.jpg: same photo as round 1 (orig-hunt40, graded late season), placed so the hunter's head and
    pack sit between the logo and the label; lower half pulled toward Tap Shoe for the live text; bottom rows are
    Tap Shoe + the last rows of the topo tile, so the attribute band (row 0) continues it with no tear."""
    W, H = 1200, R2_H
    ph = c.fit(c.lifestyle("orig-hunt40-hunter-forest-back.jpg"), w=W)
    a = np.asarray(ph, np.float32)[380:380 + H]
    grey = a.mean(2, keepdims=True)
    a = (a * 0.55 + grey * 0.45) * np.array([0.86, 0.93, 1.02], np.float32) * 0.80
    a = 255 * (np.clip(a / 255, 0, 1) ** 1.12)
    a = 84 * np.tanh(a / 84) * 0.35 + a * 0.65                          # tame the backlit canopy highlights
    h = a.shape[0]
    base = np.broadcast_to(np.array(c.rgb(TAPSHOE), np.float32), (H, W, 3)).copy()
    base += topo_detail(slice(1600 - H, 1600)) * 0.85
    layer = base.copy()
    layer[:h] = a
    y = np.arange(H, dtype=np.float32)
    top = (1 - c.smooth(np.clip(y / 240, 0, 1))) * 0.5                 # logo on the canopy
    low = c.smooth(np.clip((y - 430) / 420, 0, 1)) * 0.62              # text area (label to button)
    fade = c.smooth(np.clip((y - 1020) / 300, 0, 1))                   # photo -> base
    k = np.clip(top + low * (1 - fade) + fade, 0, 1)[:, None, None]
    arr = layer * (1 - k) + base * k
    soft = np.asarray(c.to_image(arr).convert("RGB").filter(ImageFilter.GaussianBlur(2.0)), np.float32)
    m = c.smooth(np.clip((y - 560) / 300, 0, 1))[:, None, None] * 0.6    # a little mist under the headline
    arr = arr * (1 - m) + soft * m
    arr += (pn(W, H, 0.75, 562) * 1.6)[:, :, None]
    p = save(arr, "o5-hero-r2.jpg", limit=150 * 1024, q=74)
    for lab, box in {"headline": (60, 620, 1140, 1000), "subtitle": (160, 1040, 1040, 1200),
                     "logo": (400, 50, 800, 130)}.items():
        print(f"      {lab:9s}", c.contrast_report(p, ["#FFFFFF"], box))


def pack_panel(key, out, *, h=None, w=None, cx=300, cy=335, top=None):
    """Checkerboard packshot cell: variant packshot on the flat panel color (600x670, shown 300x335)."""
    W, H = 600, 670
    img = Image.new("RGBA", (W, H), c.rgb(PANELS[key]) + (255,))
    pk = c.fit(c.load_packshot(PACK[key]), w=w, h=h)
    if top is not None:
        cy = top + pk.height / 2
    c.place(img, pk, cx, cy, 0, shadow=(0, 8, 14, 0.22))
    return save(img.convert("RGB"), out, limit=90 * 1024, q=80)


def job_packs():
    """o5-pack-midlayer / pant / jacket.jpg, sizes measured on rev-oct-05 (1x: jacket 290 tall, pant 190 wide
    and cut by the cell bottom, fleece jacket 257 tall)."""
    pack_panel("midlayer", "o5-pack-midlayer.jpg", h=580, cx=300, cy=335)
    pack_panel("pant", "o5-pack-pant.jpg", w=380, cx=300, top=20)
    pack_panel("jacket", "o5-pack-jacket.jpg", h=514, cx=300, cy=318)


def job_edge2():
    """o5-edge-water-footer-r2.jpg: water -> flat Tap Shoe footer as drawn in rev-oct-05: deeper, jagged tear
    (two torn_line octaves), dark shadow, no light paper rim."""
    h = 80
    up = c.tile_rows("o5-water", h, end=True)
    lo = c.tile_rows("flat:#2A2B2D", h)
    a1 = c.torn_line(1200, h * 0.5, amp=14, seed=531)
    a2 = c.torn_line(1200, 0, amp=5, seed=532)
    ys = [y1 + y2 for y1, y2 in zip(a1, a2)]
    return save(torn_join(up, lo, ys, 531, shadow=(6.0, 0.3), rim_alpha=0.0), "o5-edge-water-footer-r2.jpg",
                limit=30 * 1024, q=78, sub=0)


JOBS.update({"grad": job_grad, "hero2": job_hero2, "packs": job_packs, "edge2": job_edge2})


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="*", choices=sorted(JOBS))
    a = ap.parse_args()
    for k in a.only or JOBS:
        print(f"[{k}] {JOBS[k].__doc__.strip().splitlines()[0]}")
        JOBS[k]()


if __name__ == "__main__":
    main()
