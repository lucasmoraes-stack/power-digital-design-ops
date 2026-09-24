"""compose_03-04.py - 2026 Broadcasts, Designer B: assets for emails 03 and 04 (brief jobs B1 to B5).

Imports the kit's compose.py (never edited) and redirects its output folder to this batch's
assets/ folder, so nothing in the shared kit is touched and nothing collides with the 01-02 script.

Run from anywhere:
    python clients/habit-outdoors/03-work/email/2026-broadcasts/compose_03-04.py
    python .../compose_03-04.py --only b1 b3
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "01-brand" / "email-kit" / "tools"))
import compose as c  # noqa: E402

BATCH_ASSETS = HERE / "assets"
BATCH_ASSETS.mkdir(exist_ok=True)
c.ASSETS = BATCH_ASSETS          # save_jpg / save_png_quant write to c.ASSETS at call time

PATRIOT = "#202944"


def b1():
    """E3 hero photo: family walking into the woods, crop of the Sep 10 card photo."""
    img = c.ref_crop("Septemeber 10.png", (155, 3738, 1045, 4128))
    p = c.save_jpg(c.fit(img, w=1200), "hero-family-walk.jpg")
    c.report(p)


def b2():
    """E3 packshots (E17 cards)."""
    c.product_png("knit-camo-stocking-cap--39479198580787", 400, "pack-knit-camo-stocking-cap-400.png")
    c.product_png("youth-bear-cave-long-sleeve-camo-tee--51763673661722", 400, "pack-youth-bear-cave-long-sleeve-camo-tee-400.png")
    c.product_png("all-purpose-camo-leather-gloves--47156168098074", 400, "pack-all-purpose-camo-leather-gloves-400.png")


def b3():
    """E3 E21: Youth Bear Cave Tee crossing Tap Shoe -> light warm (+ -dm twin on #34353A)."""
    c.compose_band_cross("youth-bear-cave-long-sleeve-camo-tee--51763673661722", "e21-cross-youth-bear-cave.jpg",
                         top=c.TAPSHOE, bottom=c.LIGHT, size=(1200, 660), seam=370, product_h=520, cx=330, angle=-5)


def b4():
    """E4 packshots (both E17 bands; the boot serves both)."""
    for f, out in (
        ("copy-of-mens-all-weather-boot--39916249776179", "pack-copy-of-mens-all-weather-boot-400.png"),
        ("habit-mens-roaring-springs-packable-rain-pant-1--31820086575155", "pack-habit-mens-roaring-springs-packable-rain-pant-1-400.png"),
        ("habit-mens-roaring-springs-packable-rain-pant--31746549415987", "pack-habit-mens-roaring-springs-packable-rain-pant-400.png"),
        ("mlf-hooded-performance-layer-with-gaiter--40557557448755", "pack-mlf-hooded-performance-layer-with-gaiter-400.png"),
        ("men-s-roaring-springs-packable-rain-pant--39299401875507", "pack-men-s-roaring-springs-packable-rain-pant-400.png"),
    ):
        c.product_png(f, 400, out)


# The variant packshot of the MLF Hooded (products.json image_src, PT10299SHARKSKINFRONT) is a model photo
# that the store crops at the eyes and at the jeans: over the E21 seam it floats as a face cut by a hard
# line in the middle of the brown band. The same product page has a garment-only image in the same color
# (first catalog image, PT10299Sharkskin.png, catalog.json). B5 uses that one; the E17 card keeps the
# variant packshot. Cached in _src/ (source only, never linked from an email), trimmed and 1200px tall.
SRC = HERE / "_src"
MLF_FLAT_URL = "https://cdn.shopify.com/s/files/1/1483/3388/files/PT10299Sharkskin.png?v=1689347849"
MLF_FLAT = "mlf-hooded-performance-layer-with-gaiter--sharkskin-flat.png"


def _mlf_flat() -> None:
    SRC.mkdir(exist_ok=True)
    p = SRC / MLF_FLAT
    if p.exists():
        return
    import io
    import urllib.request
    from PIL import Image
    raw = urllib.request.urlopen(MLF_FLAT_URL, timeout=60).read()
    im = Image.open(io.BytesIO(raw)).convert("RGBA")
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
    c.fit(im, h=1200).save(p, optimize=True)


def b5():
    """E4 E21: MLF Hooded Performance Layer crossing Major Brown -> Patriot Blue (no -dm twin)."""
    _mlf_flat()
    # compose.py only corrects the seam for its own band hexes; add Patriot Blue for this call.
    old_def, old_products = c.save_jpg.__defaults__, c.PRODUCTS
    c.save_jpg.__defaults__ = (c.MAX_JPG, c.BAND_HEXES + (PATRIOT,))
    c.PRODUCTS = SRC
    try:
        # product_h 560 (brief: 600): the garment-only image is taller than the model crop; at 600 and -5 deg
        # the hem touched the bottom edge rows.
        c.compose_band_cross(MLF_FLAT, "e21-cross-mlf-hooded.jpg",
                             top=c.BROWN, bottom=PATRIOT, dm_bottom=None, size=(1200, 660), seam=370,
                             product_h=560, cx=300, angle=-5)
    finally:
        c.save_jpg.__defaults__, c.PRODUCTS = old_def, old_products


# =====================================================================================================
# ROUND 2 (2026-09-24) · art-direction-r2.md · outputs r2-03-* / r2-04-* in this batch's assets/
# Kit files are read, never written: kit textures resolve from email-kit/assets, r2-* files from here.
# Mechanics that keep baked images seamless on the textured <td> backgrounds:
#   * every band td uses background-size:100% auto (tile scales with the fluid images on mobile);
#   * images baked on a texture only sit on FINE-GRAIN tiles (grain looks the same at any phase);
#     the big atmosphere (fog, haze, photo) lives inside the composites and fades out at their edges;
#   * blurred camo (large blobs) only carries live text, nothing baked over it;
#   * a tear always has the lower sheet over the upper one: soft shadow + light paper-fibre rim.
# =====================================================================================================
import math as _math
import random as _random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

KIT_ASSETS = c.KIT / "assets"
PHOTOS = c.PHOTOS
IVY, BROWN, TAPSHOE = c.IVY, c.BROWN, c.TAPSHOE
MAX_IMG = 150 * 1024


def _tex_path(name: str) -> Path:
    f = c.TEXTURES[name][0]
    return (BATCH_ASSETS if f.startswith("r2-") else KIT_ASSETS) / f


c.tex_path = _tex_path          # compose.py looks this up at call time (load_tile -> tex_path)
c.TEXTURES["r2-earth"] = ("r2-04-tex-earth.jpg", BROWN, "tile", "white, #E2DDD9 body, orange only large")
c.TEXTURES["r2-water"] = ("r2-04-tex-water.jpg", PATRIOT, "tile", "white, #E2DDD9 body, orange 24px+")


def _pn(w, h, l, seed, ly=None):
    return c.periodic_noise(w, h, l, ly or l, seed)


def save(img, name, limit=MAX_IMG, q=76, floor=50, sub=2):
    p = c.save_jpg_under(img if isinstance(img, Image.Image) else c.to_image(img), BATCH_ASSETS / name, limit,
                         q=q, floor=floor, subsampling=sub)
    print(f"  {p.name:40s} {Image.open(p).size}  {p.stat().st_size / 1024:6.1f} KB")
    return p


def crop_rows(arr, h, y0=0):
    return arr[y0:y0 + h].copy()


def tile(name, h, y0=0, w=1200):
    """h rows of a tile starting at row y0 (wraps), first w columns."""
    t = c.load_tile(name)
    reps = _math.ceil((y0 + h) / t.shape[0]) + 1
    tt = np.concatenate([t] * reps, axis=0)
    return tt[y0:y0 + h, :w].copy()


def haze(arr, cx, cy, rx, ry, color, strength, seed=1, breakup=0.35, window=0):
    """Soft light mist (radial, broken by slow noise), blended toward `color`. window=px forces the
    mist to zero at the image border (so a composite never shows its rectangle)."""
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
        n = _pn(w, h, 90, seed) * 0.5 + _pn(w, h, 30, seed + 1) * 0.25
        m = m * np.clip(1 + n * breakup, 0, 1.6)
    m = np.clip(m * strength, 0, 1)[:, :, None]
    col = np.array(c.rgb(color), np.float32)
    return arr * (1 - m) + col * m


def edge_fade(arr, base, sides=("top", "bottom", "left", "right"), px=60):
    """Blend the composite back into `base` (the plain tile) near the chosen edges."""
    h, w = arr.shape[:2]
    wt = np.ones((h, w), np.float32)
    ys, xs = np.arange(h, dtype=np.float32), np.arange(w, dtype=np.float32)
    if "top" in sides:
        wt *= c.smooth(np.clip(ys / px, 0, 1))[:, None]
    if "bottom" in sides:
        wt *= c.smooth(np.clip((h - 1 - ys) / px, 0, 1))[:, None]
    if "left" in sides:
        wt *= c.smooth(np.clip(xs / px, 0, 1))[None, :]
    if "right" in sides:
        wt *= c.smooth(np.clip((w - 1 - xs) / px, 0, 1))[None, :]
    return arr * wt[:, :, None] + base * (1 - wt[:, :, None])


def _widths(w, seed, lo=1.5, hi=5.5):
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, w + 60)
    k = np.exp(-np.linspace(-2.5, 2.5, 41) ** 2)
    n = np.convolve(n, k / k.sum(), "same")[30:30 + w]
    n = (n - n.min()) / (n.max() - n.min() + 1e-6)
    return lo + (hi - lo) * n


def torn_over(upper, lower, ys, y_off=0, seed=0, lower_on_top=True, rim=(228, 223, 216), rim_alpha=0.55,
              shadow=(6.0, 0.34), specks=True):
    """Join two sheets along a torn line ys (+y_off). lower_on_top=True: the lower sheet lies over the
    upper one (shadow above the line, rim on the lower sheet's edge); False: the upper sheet lies over."""
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
        rm = np.asarray(Image.fromarray((rm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)),
                        np.float32) / 255
        fib = 0.7 + 0.3 * np.random.default_rng(seed + 9).random((h, w)).astype(np.float32)
        rm = (rm * fib * rim_alpha)[:, :, None]
        out = out * (1 - rm) + np.array(rim, np.float32) * rm
    if specks:
        img = c.to_image(out)
        d, rnd = ImageDraw.Draw(img), _random.Random(seed + 3)
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
    """E18 textured torn edge with paper rim (1200 x h). Bottom = last rows of the next tile."""
    up = c.tile_rows(top, h, end=True)
    lo = c.tile_rows(bottom, h, end=c._continues(bottom))
    ys = c.torn_line(1200, h * 0.45, amp=amp, seed=seed)
    return save(torn_over(up, lo, ys, seed=seed), out, limit=30 * 1024, q=78, sub=0)


def shoot(file_or_img, h=None, w=None):
    im = file_or_img if isinstance(file_or_img, Image.Image) else c.load_packshot(file_or_img)
    return c.fit(im, w=w, h=h)


def framed(img, width, frame=12, sides=("bottom",), color="#E2DDD9", seed=5):
    return c.framed_photo_multi(img, width, frame=frame, sides=sides, frame_color=color, seed=seed)


def contrast(p, box, texts=("#FFFFFF", "#E2DDD9")):
    print(f"      text area {box}: {c.contrast_report(p, list(texts), box)}")


# ---------------------------------------------------------------- textures (04 only; 03 uses kit tiles)

def r2_textures():
    """r2-04-tex-earth.jpg (Major Brown soil, fine grain only) + r2-04-tex-water.jpg (Patriot Blue, fine ripples)."""
    W, H = c.TEX_W, c.TEX_H
    # Earth: soil grit and small dark clumps over the brown paper; mottle kept at ~1 level so a td
    # restart or a baked image never shows a step (compose.py note on paper-light).
    e = c.paper_surface(BROWN, grain_sd=4.0, mottle=1.0, fibre=7, fibre_sign=1, seed=141)
    clump = -np.clip(_pn(W, H, 4, 142) - 1.5, 0, None) * 10
    grit = np.clip(_pn(W, H, 1.0, 143) - 2.6, 0, None) * 16
    pebble = -np.clip(_pn(W, H, 9, 144) - 2.2, 0, None) * 7
    e += (clump + grit + pebble)[:, :, None] * np.array([1.0, 0.95, 0.88], np.float32)
    e += np.array(c.rgb(BROWN), np.float32) - e.reshape(-1, 3).mean(0)
    p = save(e, "r2-04-tex-earth.jpg", limit=92 * 1024, q=70)
    print("     ", c.contrast_report(p, ["#FFFFFF", "#E2DDD9", "#FF6400"], blur=0))
    # Water: fine horizontal streaks bent by a slow warp + sparse glints; no large patches (a baked
    # composite must not show a step at its border).
    wv = np.broadcast_to(np.array(c.rgb(PATRIOT), np.float32), (H, W, 3)).copy()
    rip = _pn(W, H, 44, 151, 1.6) * 2.6 + _pn(W, H, 16, 152, 1.0) * 1.3
    warp = _pn(W, H, 60, 153, 40) * 6.0
    yy = (np.arange(H)[:, None] + np.rint(warp).astype(int)) % H
    xx = np.broadcast_to(np.arange(W)[None, :], (H, W))
    rip = rip[yy, xx]
    glint = np.clip(_pn(W, H, 5, 154, 0.8) - 2.9, 0, None) * 14
    g = _pn(W, H, 0.75, 155) * 2.6
    tint = np.array([0.72, 0.88, 1.15], np.float32)
    wv += (rip + glint)[:, :, None] * tint + g[:, :, None]
    wv += np.array(c.rgb(PATRIOT), np.float32) - wv.reshape(-1, 3).mean(0)
    p = save(wv, "r2-04-tex-water.jpg", limit=92 * 1024, q=70)
    print("     ", c.contrast_report(p, ["#FFFFFF", "#E2DDD9", "#FF6400"], blur=0))


# ---------------------------------------------------------------- 03 The Art of Being Unseen

def _hero(photo, out, *, next_tex, seed, rim_seed, **kw):
    """compose.py E24 hero, plus the paper-fibre rim on its baked tear (compose.py builds the tear at
    tear_y - 24 with torn_line(W, 12, amp=9, seed=seed+2); the rim is drawn on the same line just
    before the file is written)."""
    size, tear_y = kw["size"], kw["tear_y"]
    ys = c.torn_line(size[0], 12, amp=9, seed=seed + 2)
    y_off = size[1] - (size[1] - tear_y + 24)
    orig = c.save_jpg_under

    def patched(im, path, limit, **k):
        arr = np.asarray(im.convert("RGB"), np.float32)
        h, w = arr.shape[:2]
        yy = np.arange(h, dtype=np.float32)[:, None]
        line = np.array(ys, np.float32)[None, :] + y_off
        wv = _widths(w, rim_seed)[None, :]
        d = yy - line
        rm = ((d >= -0.5) & (d <= wv)).astype(np.float32)
        rm = np.asarray(Image.fromarray((rm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)),
                        np.float32) / 255
        fib = 0.7 + 0.3 * np.random.default_rng(rim_seed).random((h, w)).astype(np.float32)
        rm = (rm * fib * 0.55)[:, :, None]
        arr = arr * (1 - rm) + np.array((228, 223, 216), np.float32) * rm
        return orig(c.to_image(arr), path, limit, **k)

    c.save_jpg_under = patched
    try:
        return c.compose_full_bleed_hero(photo, out, next_tex=next_tex, seed=seed, **kw)
    finally:
        c.save_jpg_under = orig


def r2_03_hero():
    """E24 hero 03: forest walk, cooler and greener grade, a mist bank drifting through the family,
    fog grown above for the headline, bottom melts into Tap Shoe and tears into blurred camo."""
    ph = c.lifestyle("crop-sent-sep15-family-forest-walk.jpg")
    a = np.asarray(ph, np.float32)
    grey = a.mean(2, keepdims=True)
    a = (a * 0.78 + grey * 0.22) * np.array([0.93, 1.0, 0.94], np.float32)       # quiet, cooler, green
    h, w = a.shape[:2]
    # mist bank behind and through the family: rows 40..330 of the photo (heads sit at ~15..100),
    # zero at the top rows, so the fog grown ABOVE the photo (from rows 2..14) stays dark for white text.
    yy = np.arange(h, dtype=np.float32)[:, None]
    band = np.exp(-((yy - 170) / 120) ** 2) * c.smooth(np.clip((yy - 16) / 60, 0, 1))
    n = _pn(w, h, 140, 311, 50) * 0.55 + _pn(w, h, 40, 312, 18) * 0.3
    m = np.clip(band * (0.55 + n * 0.5), 0, 0.62)[:, :, None]
    a = a * (1 - m) + np.array((150, 152, 138), np.float32) * m
    ph = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    # the tear into the camo lives in the camo td (r2-03-tear-hero-camo.png), so the hero only melts
    # into Tap Shoe paper: next_tex = the base paper makes compose.py's own tear invisible.
    p = c.compose_full_bleed_hero(ph, "r2-03-hero.jpg", next_tex="paper-tapshoe", seed=301,
              size=(1200, 1520), photo_w=1500, photo_y=830, extend_top="fog", top_shade=(900, 0.55),
              fade=(1290, 1470), tear_y=1500, grain_sd=2.6,
              text_boxes={"desktop": (100, 160, 1100, 800), "mobile": (190, 130, 1010, 830)})
    return p


def tear_png(name, *, top=None, bottom=None, h=80, seam=0.5, seed=0, amp=10, shadow=(8.0, 0.42),
             rim_alpha=0.6, colors=96):
    """Torn edge as a PNG that sits INSIDE a td whose background must show through (blurred camo:
    its blobs do not match across two tds). Exactly one of top/bottom is a texture (opaque side);
    the other side is transparent. The lower sheet always lies over the upper one: shadow above the
    line (baked into the opaque top, or as translucent black over the transparent top), light fibre
    rim just below the line."""
    W = 1200
    ys = np.array(c.torn_line(W, h * seam, amp=amp, seed=seed), np.float32)[None, :]
    yy = np.arange(h, dtype=np.float32)[:, None]
    below = np.clip(yy - ys + 0.5, 0, 1)                         # 1 below the line (lower sheet)
    below = np.asarray(Image.fromarray((below * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)),
                       np.float32) / 255
    d = ys - yy
    sh = np.where(d > 0, np.exp(-d / shadow[0]), 0) * shadow[1]
    wv = _widths(W, seed)[None, :]
    rm = ((yy - ys >= -0.5) & (yy - ys <= wv)).astype(np.float32)
    rm = np.asarray(Image.fromarray((rm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)),
                    np.float32) / 255
    rm *= (0.7 + 0.3 * np.random.default_rng(seed + 9).random((h, W)).astype(np.float32)) * rim_alpha
    rimc = np.array((228, 223, 216), np.float32)
    rgb_ = np.zeros((h, W, 3), np.float32)
    alpha = np.zeros((h, W), np.float32)
    if top:                                                       # opaque above, td shows below
        up = tile(top, h) if not top.startswith("flat:") else c.tile_rows(top, h)
        up = up * (1 - sh)[:, :, None]
        rgb_ = up * (1 - below)[:, :, None] + rimc * below[:, :, None]
        a_rim = rm * below
        alpha = (1 - below) + a_rim
        rgb_ = np.where((below > 0.5)[:, :, None], rimc, rgb_)
    else:                                                         # td shows above, opaque below
        lo = c.tile_rows(bottom, h, end=c._continues(bottom))
        lo = lo * (1 - rm[:, :, None]) + rimc * rm[:, :, None]
        rgb_ = lo * below[:, :, None]
        alpha = below + sh * (1 - below)
    alpha = np.clip(alpha, 0, 1)
    img = Image.fromarray(np.clip(np.rint(np.dstack([rgb_, alpha * 255])), 0, 255).astype(np.uint8), "RGBA")
    p = BATCH_ASSETS / name
    img.quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG).save(p, optimize=True)
    print(f"  {p.name:40s} {img.size}  {p.stat().st_size / 1024:6.1f} KB")
    return p


def r2_03_edges():
    """03 torn edges: Tap Shoe paper -> camo and camo -> Ivy as transparent PNGs inside the camo td;
    Ivy grain -> flat Tap Shoe footer as JPG (grain on both sides, a td restart does not show)."""
    tear_png("r2-03-tear-hero-camo.png", top="paper-tapshoe", h=64, seam=0.42, seed=320)
    tear_png("r2-03-tear-camo-ivy.png", bottom="grain-ivy", h=80, seam=0.5, seed=321)
    edge("grain-ivy", "flat:#2A2B2D", "r2-03-edge-ivy-footer.jpg", seed=322)


def r2_03_canoe():
    """E26 in the Ivy band: canoe on a still green river, torn top and right, -2 deg, in a mist glow,
    baked on tex-grain-ivy rows from 0 (the image opens its td)."""
    W, H = 1200, 860
    base = tile("grain-ivy", H)
    arr = haze(base.copy(), 600, 430, 520, 300, "#9A9A86", 0.8, seed=331, window=160, breakup=0.6)
    img = c.to_image(arr)
    ph = c.lifestyle("crop-sent-sep22-canoe-river.jpg")
    fr = framed(ph, 600, frame=14, sides=("top", "right"), color="#E2DDD9", seed=333)
    c.place(img, fr, 600, 440, -2.0, shadow=(8, 20, 26, 0.55))
    arr = edge_fade(np.asarray(img.convert("RGB"), np.float32), base, px=70)
    return save(arr, "r2-03-torn-canoe.jpg", q=76)


def _product_card(file, out, *, size, height, cx, cy, angle, tex, haze_c="#9A9A86", haze_s=0.8,
                  bleed=None, y0=0, seed=0, shadow=(10, 26, 30, 0.55)):
    """One product, big, on a mist glow over a fine-grain tile; edges fade back to the plain tile
    except the `bleed` side (the product is cut by the image edge, which touches the email edge)."""
    W, H = size
    base = tile(tex, H, y0=y0, w=W)
    # the crop's slow mottle drifts 1 to 2.5 levels off the tile average the td shows around it:
    # keep only the fine grain, centred on the tile average, so every image border meets the td level.
    low = np.asarray(c.to_image(base).convert("RGB").filter(ImageFilter.GaussianBlur(40)), np.float32)
    base = base - low + c.load_tile(tex).reshape(-1, 3).mean(0)
    arr = haze(base.copy(), cx, cy, W * 0.32, H * 0.30, haze_c, haze_s, seed=seed, window=230, breakup=0.6)
    img = c.to_image(arr)
    c.place(img, shoot(file, h=height), cx, cy, angle, shadow=shadow)
    sides = [s for s in ("top", "bottom", "left", "right") if s != bleed]
    arr = edge_fade(np.asarray(img.convert("RGB"), np.float32), base, sides=sides, px=60)
    return save(arr, out, limit=110 * 1024, q=78)


def r2_03_products():
    """03 products in the client order, one per row, zigzag on Ivy grain: cap (left), tee (right, cut by the
    right email edge), gloves (left)."""
    _product_card("youth-bear-cave-long-sleeve-camo-tee--51763673661722", "r2-03-prod-tee.jpg",
                  size=(660, 640), height=620, cx=470, cy=330, angle=6, tex="grain-ivy", bleed="right", seed=341)
    _product_card("knit-camo-stocking-cap--39479198580787", "r2-03-prod-cap.jpg",
                  size=(660, 560), height=400, cx=340, cy=285, angle=7, tex="grain-ivy", seed=342)
    _product_card("all-purpose-camo-leather-gloves--47156168098074", "r2-03-prod-gloves.jpg",
                  size=(660, 560), height=390, cx=330, cy=280, angle=-9, tex="grain-ivy", seed=343)


# ---------------------------------------------------------------- 04 Shoreline vs. Deep Water

def r2_04_hero():
    """E24 hero 04: angler over his tackle box, dark river grown up into a blue-black fog for the
    stacked headline; bottom melts into Tap Shoe and tears into the earth texture (the shore)."""
    ph = c.lifestyle("crop-sent-sep22-angler-tackle-box.jpg")
    a = np.asarray(ph, np.float32)
    a = a * np.array([0.92, 0.98, 1.06], np.float32)                 # cooler, toward the water
    ph = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return _hero(ph, "r2-04-hero.jpg", next_tex="r2-earth", seed=401, rim_seed=405,
                 size=(1200, 1640), photo_w=2000, photo_y=860, extend_top="fog", top_shade=(900, 0.5),
                 fade=(1420, 1560), tear_y=1590, grain_sd=2.6,
                 text_boxes={"desktop": (100, 150, 1100, 960), "mobile": (150, 120, 1050, 1000)})


def _cut(im, frac, feather=6):
    """Erase the bottom of a packshot below `frac` of its height (store model shots: shoes)."""
    if not frac:
        return im
    im = im.copy()
    h = im.height
    a = np.asarray(im.getchannel("A"), np.float32)
    ys = np.arange(h, dtype=np.float32)[:, None]
    k = np.clip((frac * h - ys) / feather, 0, 1)
    im.putalpha(Image.fromarray((a * k).astype(np.uint8)))
    return im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())


def _torn_window(name, *, tex, photo, photo_box, win, products, seed, blur=0.0, dim=0.85, size=(1200, 820),
                 y0=0, photo_haze=None, limit=MAX_IMG):
    """Collage: a torn window in the band paper shows a photo. Order, back to front: photo, the paper
    below the window (torn top edge, lies over the photo), products with layer "under" (they cross the
    lower tear onto the paper), the paper strip above the window (torn bottom edge, hides the store
    crop of model shots: waist, hands), products with layer "over" (flat garments, cross both tears).
    products: [{file|img, height, cx, cy, angle, darken, cut, layer}]."""
    W, H = size
    base = tile(tex, H, y0=y0, w=W)
    x0, py0, x1, py1 = photo_box
    bw, bh = x1 - x0, py1 - py0
    im = photo.convert("RGB")
    s = max(bw / im.width, bh / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    ox, oy = (im.width - bw) // 2, (im.height - bh) // 2
    im = im.crop((ox, oy, ox + bw, oy + bh))
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    pa = np.asarray(im, np.float32) * dim
    if photo_haze:
        pa = haze(pa, *photo_haze, seed=seed)
    mid = base.copy()
    mid[py0:py1, x0:x1] = pa
    yb = c.torn_line(W, 0, amp=11, seed=seed + 2)
    arr = torn_over(mid, base, yb, y_off=win[1], seed=seed + 2, lower_on_top=True, rim_alpha=0.6,
                    shadow=(9.0, 0.45))

    def draw(arr, layer):
        img = c.to_image(arr)
        for it in products:
            if it.get("layer", "under") != layer:
                continue
            p = it["img"] if "img" in it else c.load_packshot(it["file"])
            p = shoot(_cut(p, it.get("cut")), h=it["height"])
            if it.get("darken"):
                p = c.darken(p, it["darken"])
            c.place(img, p, it["cx"], it["cy"], it.get("angle", 0), shadow=it.get("shadow", (10, 24, 28, 0.6)))
        return np.asarray(img.convert("RGB"), np.float32)

    arr = draw(arr, "under")
    ya = c.torn_line(W, 0, amp=11, seed=seed + 1)
    arr = torn_over(base, arr, ya, y_off=win[0], seed=seed + 1, lower_on_top=False, rim_alpha=0.6,
                    shadow=(10.0, 0.5))
    arr = draw(arr, "over")
    arr = edge_fade(arr, base, sides=("top", "bottom"), px=20)
    return save(arr, name, limit=limit, q=76)


def r2_04_shoreline():
    """04 Shoreline collage: torn window in the earth paper onto the wading angler's bank (blurred:
    it is a 304px crop). Gray Waves pant (flat shot) over both tears; Realtree Edge pant (model shot)
    with its waist and hands under the upper strip and the shoes trimmed, crossing the lower tear."""
    _torn_window("r2-04-shore-pants.jpg", tex="r2-earth",
                 photo=c.lifestyle("crop-sent-sep22-wading-river.jpg"), photo_box=(0, 100, 1200, 600),
                 win=(150, 470), blur=4, dim=0.8, size=(1200, 720), seed=411,
                 photo_haze=(600, 260, 700, 220, "#6E6254", 0.22),
                 products=[
                     {"file": "habit-mens-roaring-springs-packable-rain-pant--31746549415987", "height": 700,
                      "cx": 790, "cy": 256, "angle": -3, "cut": 0.88, "layer": "under"},
                     {"file": "habit-mens-roaring-springs-packable-rain-pant-1--31820086575155", "height": 660,
                      "cx": 400, "cy": 410, "angle": 6, "layer": "over"},
                 ])


def r2_04_openwater():
    """04 Open Water collage: torn window in the water paper onto the three anglers on the boat.
    MLF Hooded Performance Layer (garment-only store image, same Sharkskin, _src/) over both tears;
    Marlin Blue rain pant (model shot) with sleeves and hands under the upper strip, shoes trimmed."""
    _mlf_flat()
    _torn_window("r2-04-water-hood-pant.jpg", tex="r2-water",
                 photo=c.lifestyle("crop-sent-sep22-boat-anglers.jpg"), photo_box=(0, 100, 1200, 600),
                 win=(150, 470), blur=1.6, dim=0.82, size=(1200, 720), seed=421,
                 photo_haze=(600, 260, 800, 220, "#2E3A5C", 0.25),
                 products=[
                     {"file": "men-s-roaring-springs-packable-rain-pant--39299401875507", "height": 720,
                      "cx": 810, "cy": 242, "angle": -3, "cut": 0.86, "layer": "under"},
                     {"img": Image.open(SRC / MLF_FLAT).convert("RGBA"), "height": 640,
                      "cx": 390, "cy": 400, "angle": 5, "layer": "over"},
                 ])


def r2_04_cross():
    """04 E21 on textures: the 15-inch boot (in both kits) standing on the shoreline tear, earth above,
    water below (last water-tile rows: the Open Water td continues it). Right half calm for the live
    label (the image is the td background)."""
    W, H = 1200, 720
    seam = 430
    up = tile("r2-earth", H, y0=300)
    lo = c.tile_rows("r2-water", H, end=True)
    up = haze(up, 330, 300, 420, 260, "#5E5248", 0.35, seed=431)
    ys = c.torn_line(W, 0, amp=14, seed=432)
    arr = torn_over(up, lo, ys, y_off=seam, seed=432, lower_on_top=True, rim_alpha=0.65, shadow=(10.0, 0.5))
    img = c.to_image(arr)
    c.place(img, shoot("copy-of-mens-all-weather-boot--39916249776179", h=560), 300, 400, -7,
            shadow=(14, 26, 30, 0.6))
    arr = np.asarray(img.convert("RGB"), np.float32)
    top = tile("r2-earth", 24, y0=300)
    arr[:4] = top[:4]
    p = save(arr, "r2-04-cross-boot.jpg", q=76)
    contrast(p, (640, 60, 1160, 400))
    return p


def r2_04_edges():
    """04 torn edge: water -> flat Tap Shoe footer."""
    edge("r2-water", "flat:#2A2B2D", "r2-04-edge-water-footer.jpg", seed=441)


R2_JOBS = {
    "r2tex": r2_textures,
    "r2-03-hero": r2_03_hero, "r2-03-edges": r2_03_edges, "r2-03-canoe": r2_03_canoe,
    "r2-03-products": r2_03_products,
    "r2-04-hero": r2_04_hero, "r2-04-shore": r2_04_shoreline, "r2-04-water": r2_04_openwater,
    "r2-04-cross": r2_04_cross, "r2-04-edges": r2_04_edges,
}

JOBS = {"b1": b1, "b2": b2, "b3": b3, "b4": b4, "b5": b5, **R2_JOBS}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="*", choices=sorted(JOBS))
    a = ap.parse_args()
    for k in a.only or JOBS:
        print(f"[{k}] {JOBS[k].__doc__.strip()}")
        JOBS[k]()


if __name__ == "__main__":
    main()
