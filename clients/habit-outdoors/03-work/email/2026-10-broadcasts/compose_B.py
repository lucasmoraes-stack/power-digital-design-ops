"""compose_B.py - October 2026 Broadcasts, Designer B: assets for emails 03 (Heavy Weight Hoodie) and 04 (Crater Valley).

Round 2 (2026-09-25): rebuilt to the owner's revised designs
    email-kit/references/rev-oct-03-heavy-weight-hoodie.png and rev-oct-04-crater-valley.png
(revision-r2.md). The round-1 jobs (oak hero, textured panel stack on plain paper, open frames, GIF) are gone.

Imports the kit's compose.py (never edited) and redirects its output folder to this batch's assets/,
so nothing in the shared kit is touched and nothing collides with compose_A.py / compose_C.py.
Every output is prefixed o3- or o4-. Crops taken from the rev-oct PNGs are named o3-rev-* / o4-rev-*
(provisional 1x crops: the originals are not on this machine; swap for the originals when they arrive).

Run from anywhere:
    python clients/habit-outdoors/03-work/email/2026-10-broadcasts/compose_B.py
    python .../compose_B.py --only o3-hero o4-cards

Mechanics:
  * 03 band = light paper with large camo splotches (o3-tex-paper-camo, + -dm twin). Splotches are big
    shapes, so nothing opaque may carry that paper baked in (the tile phase in the <td> is unknown):
    the torn edges and the hoodie that rises out of each panel are TRANSPARENT PNGs laid over the band
    <td>, and the panel JPGs hold only the panel. The panel text <td> continues the panel tile at the
    phase the JPG was baked with (background-position:left top, 600px), as in round 1.
  * 04 cards: the photo column (store backdrop + model) is one JPG per card with the rounded outer
    corners baked on the fine brown grain; the card outline is CSS.
  * store model shots are cut at the forehead: a face is never cut between forehead and mouth (QA r1).
    The cut sits on an edge: the email top edge, a card top line or a torn paper strip.
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
REFS = c.REFS

TAPSHOE, BROWN, LIGHT, DM_BAND = c.TAPSHOE, c.BROWN, c.LIGHT, c.DM_BAND
NIGHT = "#1E1F21"                  # 04 closing band under the sunset photo (kit dark page colour)
RIM = (228, 223, 216)
REV3 = REFS / "rev-oct-03-heavy-weight-hoodie.png"
REV4 = REFS / "rev-oct-04-crater-valley.png"


# ---------------------------------------------------------------- helpers

def save(arr, name, limit=150 * 1024, q=76, floor=50, sub=2):
    img = arr if isinstance(arr, Image.Image) else c.to_image(arr)
    p = c.save_jpg_under(img, OUT / name, limit, q=q, floor=floor, subsampling=sub)
    print(f"  {p.name:40s} {Image.open(p).size}  {p.stat().st_size / 1024:6.1f} KB")
    return p


def save_png(im: Image.Image, name: str, limit=40 * 1024):
    """RGBA PNG; quantized (soft alpha kept) only if the truecolor file is over `limit`."""
    p = OUT / name
    im.save(p, optimize=True)
    if p.stat().st_size > limit:
        for colors in (256, 192, 128):
            q = im.quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
            q.save(p, optimize=True)
            if p.stat().st_size <= limit:
                break
    print(f"  {p.name:40s} {im.size}  {p.stat().st_size / 1024:6.1f} KB")
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


def haze(arr, cx, cy, rx, ry, color, strength, seed=1, breakup=0.35):
    h, w = arr.shape[:2]
    yy = (np.arange(h, dtype=np.float32)[:, None] - cy) / ry
    xx = (np.arange(w, dtype=np.float32)[None, :] - cx) / rx
    m = np.exp(-(xx ** 2 + yy ** 2))
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


def torn_over(upper, lower, ys, y_off=0, seed=0, rim_alpha=0.55, shadow=(6.0, 0.34), specks=True):
    """Join two opaque sheets along torn line ys, the lower sheet lying over the upper one."""
    h, w = upper.shape[:2]
    line = np.array(ys, np.float32)[None, :] + y_off
    yy = np.arange(h, dtype=np.float32)[:, None]
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon([(0, h)] + [(x, y + y_off) for x, y in enumerate(ys)] + [(w, h)], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[:, :, None] / 255
    up = upper.copy()
    d = line - yy
    up *= (1 - np.where(d > 0, np.exp(-d / shadow[0]), 0) * shadow[1])[:, :, None]
    out = up * (1 - a) + lower * a
    if rim_alpha:
        wv = _widths(w, seed)[None, :]
        dd = yy - line
        rm = ((dd >= -0.5) & (dd <= wv)).astype(np.float32)
        rm = np.asarray(Image.fromarray((rm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255
        fib = 0.7 + 0.3 * np.random.default_rng(seed + 9).random((h, w)).astype(np.float32)
        rm = (rm * fib * rim_alpha)[:, :, None]
        out = out * (1 - rm) + np.array(RIM, np.float32) * rm
    if specks:
        img = c.to_image(out)
        dr, rnd = ImageDraw.Draw(img), random.Random(seed + 3)
        spot = tuple(int(v) for v in np.median(lower.reshape(-1, 3), 0))
        for _ in range(int(w / 40)):
            x = rnd.randrange(w)
            y = ys[x] + y_off - rnd.uniform(3, 10)
            r = rnd.choice((1.2, 1.6, 2.2))
            dr.ellipse((x - r, y - r, x + r, y + r), fill=spot + (255,))
        out = np.asarray(img.convert("RGB"), np.float32)
    return out


def torn_png(out, *, upper=None, lower=None, w=1200, h=80, seed=0, amp=9, rim=RIM, rim_alpha=0.75,
             shadow=(6.0, 0.4), speck_color=None, specks=34):
    """Transparent torn edge (E18 look) for a row INSIDE a textured band <td>: the band shows through the
    transparent sheet. upper / lower = flat hex of the opaque sheet, the other one is None (transparent).
    The lower sheet always lies over the upper one (shadow above the line, fibre rim under it)."""
    ys = c.torn_line(w, h * 0.5, amp=amp, seed=seed)
    yy = np.arange(h, dtype=np.float32)[:, None]
    line = np.array(ys, np.float32)[None, :]
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon([(0, h)] + [(x, y) for x, y in enumerate(ys)] + [(w, h)], fill=255)
    below = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255      # 1 under the line
    rgba = np.zeros((h, w, 4), np.float32)
    if upper:
        rgba[..., :3] = c.rgb(upper)
        rgba[..., 3] = 1 - below
        d = line - yy
        s = np.where(d > 0, np.exp(-d / shadow[0]), 0) * shadow[1]
        rgba[..., :3] *= (1 - s)[:, :, None]
    else:                                            # paper above: only the shadow of the lower sheet
        d = line - yy
        s = np.where(d > 0, np.exp(-d / shadow[0]), 0) * shadow[1]
        rgba[..., 3] = s * (1 - below)
    wv = _widths(w, seed)[None, :]
    dd = yy - line
    rm = ((dd >= -0.5) & (dd <= wv)).astype(np.float32)
    rm = np.asarray(Image.fromarray((rm * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)), np.float32) / 255
    fib = 0.7 + 0.3 * np.random.default_rng(seed + 9).random((h, w)).astype(np.float32)
    rm = rm * fib * rim_alpha
    if lower:
        lo = np.array(c.rgb(lower), np.float32)
        col = lo * (1 - rm[..., None]) + np.array(rim, np.float32) * rm[..., None]
        rgba[..., :3] = rgba[..., :3] * (1 - below[..., None]) + col * below[..., None]
        rgba[..., 3] = np.maximum(rgba[..., 3], below)
    else:                                            # transparent lower sheet: the rim is the only thing drawn
        rgba[..., :3] = rgba[..., :3] * (1 - rm[..., None]) + np.array(rim, np.float32) * rm[..., None]
        rgba[..., 3] = np.clip(rgba[..., 3] * (1 - below) + rm, 0, 1)
    img = Image.fromarray(np.clip(np.rint(rgba * [1, 1, 1, 255]), 0, 255).astype(np.uint8), "RGBA")
    if speck_color and specks:
        dr, rnd = ImageDraw.Draw(img), random.Random(seed + 3)
        for _ in range(specks):
            x = rnd.randrange(w)
            y = ys[x] - rnd.uniform(3, 10)
            r = rnd.choice((1.2, 1.6, 2.2))
            dr.ellipse((x - r, y - r, x + r, y + r), fill=c.rgb(speck_color) + (255,))
    return save_png(img, out, limit=30 * 1024)


def rrect_mask(size, box, r, corners=("tl", "tr", "bl", "br"), ss=4):
    """Anti-aliased rounded-rectangle mask; corners not listed stay square."""
    w, h = size
    m = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(m)
    x0, y0, x1, y1 = [v * ss for v in box]
    d.rounded_rectangle((x0, y0, x1, y1), r * ss, fill=255,
                        corners=tuple(k in corners for k in ("tl", "tr", "br", "bl")))
    return np.asarray(m.resize((w, h), Image.LANCZOS), np.float32) / 255


CHIN = {   # source row (1200px store image) just under the chin / on the collar (QA r1)
    "mens-crater-valley-full-zip-fleece-jacket/05.png": 150,
    "mens-crater-valley-full-zip-fleece-jacket/06.png": 182,
}


def model(rel, chin=False):
    """Store image (transparent PNG) from photos/products/<handle>/NN.png, trimmed."""
    im = Image.open(PROD / rel).convert("RGBA")
    if chin:
        im = im.crop((0, CHIN[rel], im.width, im.height))
    return im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())


def fade_alpha(im: Image.Image, top=0, bottom=0):
    """Fade an RGBA image's alpha over its first `top` / last `bottom` rows."""
    a = np.asarray(im.getchannel("A"), np.float32)
    h = a.shape[0]
    yy = np.arange(h, dtype=np.float32)[:, None]
    k = np.ones_like(yy)
    if top:
        k *= c.smooth(np.clip(yy / top, 0, 1))
    if bottom:
        k *= c.smooth(np.clip((h - 1 - yy) / bottom, 0, 1))
    im = im.copy()
    im.putalpha(Image.fromarray(np.clip(a * k, 0, 255).astype(np.uint8)))
    return im


def contrast(p, box, texts=("#FFFFFF", "#E2DDD9")):
    print(f"      text area {box}: {c.contrast_report(p, list(texts), box)}")


# ================================================================ 03 Heavy Weight Hoodie

HOODIE = {
    "brown": "mens-heavy-weight-full-zip-hoodie--45636943249690",
    "gunmetal": "mens-heavy-weight-full-zip-hoodie--45636943446298",
    "loden": "mens-heavy-weight-full-zip-hoodie--45636943642906",
}
O3_HERO_H = 800          # css = file (1x)
O3_CUT = 470             # last clean row of the rev-oct-03 photo (the headline "YOUR" starts at 482)


def o3_tex():
    """Light paper with large camo splotches (rev-oct-03 band 2) + dark-mode twin, seamless 1200x1600 tiles
    shown at 600px. Splotches #D2CCC4..#CFC8BF on the kit paper #E2DDD9 (about -18 levels)."""
    w, h = c.TEX_W, c.TEX_H
    big = pn(w, h, 70, 301) * 1.0 + pn(w, h, 22, 302) * 0.5 + pn(w, h, 7, 303) * 0.28
    clus = pn(w, h, 260, 304)                                  # clusters: dense areas and calm areas
    field = big + clus * 0.55
    m = (field > 1.05).astype(np.float32)
    m = c.periodic_blur(m, 1.0)
    m = np.clip((m - 0.5) * 3 + 0.5, 0, 1)
    for suffix, base, delta in (("", "paper-light", -18.0), ("-dm", "paper-light-dm", 7.0)):
        arr = c.load_tile(base) + (m * delta)[:, :, None]
        p = c.save_jpg_under(c.to_image(arr), OUT / f"o3-tex-paper-camo{suffix}.jpg", 95 * 1024, q=72)
        a = np.asarray(Image.open(p).convert("RGB"), np.int16)
        print(f"  {p.name:40s} {p.stat().st_size / 1024:6.1f} KB  mean #%02X%02X%02X  wrap diff %.1f"
              % (*[int(v) for v in a.reshape(-1, 3).mean(0)], float(np.abs(a[:4].mean(0) - a[-4:].mean(0)).mean())))
        print(f"      {c.contrast_report(p, ['#2A2B2D'] if not suffix else ['#F1EEEB', '#D6D0CA'], blur=0)}")


def o3_hero():
    """Hero 03: provisional 1x crop of the rev-oct-03 photo (man in camo cap in the grass), rows 0..470, the
    baked HABIT logo retouched out (the live logo goes on top); below, the photo runs into flat Tap Shoe
    under the live headline."""
    ref = np.asarray(Image.open(REV3).convert("RGB"), np.float32)
    ph = ref[:O3_CUT + 30].copy()
    # retouch the baked logo: per column, interpolate the calm sky between a row above and a row below
    x0, x1, y0, y1 = 206, 392, 20, 70
    top_row = ph[y0 - 4:y0].mean(0)
    bot_row = ph[y1:y1 + 4].mean(0)
    t = np.linspace(0, 1, y1 - y0, dtype=np.float32)[:, None, None]
    patch = top_row[None] * (1 - t) + bot_row[None] * t
    patch = np.asarray(c.to_image(patch).convert("RGB").filter(ImageFilter.GaussianBlur(1.2)), np.float32)
    patch += np.random.default_rng(7).normal(0, 1.1, patch.shape).astype(np.float32)
    xs = np.arange(ph.shape[1])
    feather = np.broadcast_to(c.smooth(np.clip(np.minimum(xs - x0, x1 - xs) / 8, 0, 1))[None, :], (y1 - y0, ph.shape[1]))
    ph[y0:y1] = ph[y0:y1] * (1 - feather[..., None]) + patch * feather[..., None]
    # canvas: photo on top, the rows under it melt into Tap Shoe (blurred continuation, then flat)
    W, H = 600, O3_HERO_H
    tap = np.array(c.rgb(TAPSHOE), np.float32)
    out = np.broadcast_to(tap, (H, W, 3)).copy()
    # continuation under the clean rows: the last 150 rows mirrored and blurred (reads as the grass and the
    # jacket going dark), never a new subject; everything is pushed into Tap Shoe behind the headline
    out[:O3_CUT] = ph[:O3_CUT]
    mir = ph[O3_CUT - 150:O3_CUT][::-1]
    mir = np.asarray(c.to_image(mir).convert("RGB").filter(ImageFilter.GaussianBlur(9)), np.float32)
    out[O3_CUT:O3_CUT + 150] = mir
    # long cross-fade: the last clean rows melt into their blurred mirror (no visible line at the cut)
    B = 110
    blur_ph = np.asarray(c.to_image(ph[:O3_CUT + 30]).convert("RGB").filter(ImageFilter.GaussianBlur(9)), np.float32)
    k = c.smooth(np.clip((np.arange(O3_CUT - B, O3_CUT) - (O3_CUT - B)) / B, 0, 1))[:, None, None]
    out[O3_CUT - B:O3_CUT] = ph[O3_CUT - B:O3_CUT] * (1 - k) + blur_ph[O3_CUT - B:O3_CUT] * k
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    d = c.smooth(np.clip((yy - 330) / 240, 0, 1)) * 0.82 + c.smooth(np.clip((yy - 520) / 90, 0, 1)) * 0.2
    out = out * (1 - d) + tap * d
    out[610:] = tap
    p = save(out, "o3-rev-hero.jpg", limit=110 * 1024, q=80)
    contrast(p, (100, 478, 500, 630), ("#FFFFFF",))
    contrast(p, (100, 636, 500, 710), ("#FFFFFF",))


def o3_edges():
    """03 torn edges as transparent PNG rows inside the camo band: hero Tap Shoe -> paper (the paper lies over
    the Tap Shoe, white specks on the dark), and paper -> flat Tap Shoe footer (footer sheet over the paper)."""
    torn_png("o3-edge-hero-paper.png", upper=TAPSHOE, lower=None, seed=331, speck_color="#E2DDD9", rim_alpha=0.85)
    torn_png("o3-edge-paper-footer.png", upper=None, lower=TAPSHOE, seed=332, rim=(70, 71, 74), rim_alpha=0.6,
             shadow=(5.0, 0.3), speck_color=TAPSHOE)


# Panels: row = margin 24 + image cell 276 + text cell 252 + margin 24 (desktop). The hoodie rises O3_RISE css
# above the panel into a transparent PNG strip (band paper shows through), the panel is O3_PANEL css tall.
O3_RISE, O3_PANEL = 40, 248
O3_MW = 343


def _panel_set(key, tex, glow, side, seed):
    f = HOODIE[key]
    hd = c.fit(c.load_packshot(f), h=520)
    for mob in (False, True):
        W = O3_MW * 2 if mob else 552
        PH = 500 if mob else O3_PANEL * 2
        RH = O3_RISE * 2
        if mob:
            tx, ty = 0, -PH                      # the text <td> under it starts the tile at (0, 0)
            cx = W / 2
        elif side == "left":
            tx, ty = -W, 0                       # text td is right of the image: piece col W = tile col 0
            cx = 262
        else:
            tx, ty = 552, 0                      # text td (276 css) is left of the image
            cx = 290
        plain = tile(tex, PH, y0=ty, w=W, x0=tx)
        pan = haze(plain.copy(), cx, PH * 0.55, 230, 190, glow, 0.5, seed=seed, breakup=0.5)
        xs = np.arange(W, dtype=np.float32)[None, :]
        ys = np.arange(PH, dtype=np.float32)[:, None]
        if mob:
            ramp = c.smooth(np.clip((PH - 1 - ys) / 110, 0, 1)) + xs * 0
        elif side == "left":
            ramp = c.smooth(np.clip((W - 1 - xs) / 110, 0, 1)) + ys * 0
        else:
            ramp = c.smooth(np.clip(xs / 110, 0, 1)) + ys * 0
        pan = plain * (1 - ramp[:, :, None]) + pan * ramp[:, :, None]
        canvas = Image.new("RGBA", (W, RH + PH), (0, 0, 0, 0))
        canvas.paste(c.to_image(pan), (0, RH))
        c.place(canvas, hd, cx, 6 + hd.height / 2, 0, shadow=(8, 18, 24, 0.5))
        top = canvas.crop((0, 0, W, RH))
        body = canvas.crop((0, RH, W, RH + PH)).convert("RGB")
        suf = "-m" if mob else ""
        save_png(top, f"o3-panel-{key}{suf}-top.png", limit=16 * 1024)
        save(body, f"o3-panel-{key}{suf}.jpg", limit=80 * 1024, q=78)


def o3_panels():
    """3 colour panels (Major Brown / Gunmetal / Loden Green), desktop + mobile: rise PNG + panel JPG."""
    _panel_set("brown", "grain-brown", "#7A6B5E", "left", 331)
    _panel_set("gunmetal", "paper-tapshoe", "#55565A", "right", 332)
    _panel_set("loden", "grain-ivy", "#7C7760", "left", 333)


# ================================================================ 04 Crater Valley

CV = {
    "hoodie": "mens-crater-valley-performance-hoodie--52423312867610",
    "fleece": "mens-crater-valley-full-zip-fleece-jacket--52630367076634",
    "qzip": "mens-crater-valley-sweater-fleece-zip-jacket--52630359834906",
}
O4_HX, O4_HW, O4_HH = 330, 270, 610      # hero image column (css): x, width, height


def o4_hero():
    """Hero 04 (rev-oct-04): headline left on Tap Shoe paper, the Full Zip Fleece on model bleeding off the
    right edge, cut under the chin by the email top edge, fading out at the bottom. Mobile twin: the same
    model under a torn strip of the hero paper (it hides the chin cut), fading into Tap Shoe."""
    W, H = O4_HW * 2, O4_HH * 2
    canvas = tile("paper-tapshoe", H, w=W, x0=O4_HX * 2)      # the tile at the td phase (left top, 600px)
    img = c.to_image(canvas)
    fl = c.fit(model("mens-crater-valley-full-zip-fleece-jacket/05.png", chin=True), h=int(H * 1.55))
    fl = fade_alpha(fl, bottom=0)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c.place(lay, fl, W * 0.93, fl.height / 2, 0, shadow=(14, 20, 34, 0.5))
    lay = fade_alpha(lay, bottom=260)
    # nothing of the model may cross into the text column: fade the left 30px of the piece too
    a = np.asarray(lay.getchannel("A"), np.float32)
    xs = np.arange(W, dtype=np.float32)[None, :]
    a *= c.smooth(np.clip(xs / 30, 0, 1))
    lay.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(lay)
    save(img, "o4-hero.jpg", limit=120 * 1024, q=78)
    # mobile twin 750 x 820 (375 x 410 css)
    MW, MH = 750, 820
    top_strip = fine("paper-tapshoe", MH, w=MW)
    mi = c.to_image(fine("paper-tapshoe", MH, w=MW))
    fl2 = c.fit(model("mens-crater-valley-full-zip-fleece-jacket/05.png", chin=True), h=1000)
    lay = Image.new("RGBA", (MW, MH), (0, 0, 0, 0))
    c.place(lay, fl2, MW * 0.62, 70 + fl2.height / 2, 0, shadow=(12, 18, 30, 0.5))
    lay = fade_alpha(lay, bottom=220)
    mi.alpha_composite(lay)
    marr = np.asarray(mi.convert("RGB"), np.float32)
    ya = c.torn_line(MW, 0, amp=9, seed=404)
    # paper strip over the chin cut: the strip is the UPPER sheet lying over the photo
    ys = np.array(ya) + 96
    m = Image.new("L", (MW, MH), 0)
    ImageDraw.Draw(m).polygon([(0, 0)] + [(x, y) for x, y in enumerate(ys)] + [(MW, 0)], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[:, :, None] / 255
    yy = np.arange(MH, dtype=np.float32)[:, None]
    d = yy - ys[None, :]
    marr *= (1 - np.where(d > 0, np.exp(-d / 9.0), 0) * 0.5)[:, :, None]
    out = marr * (1 - a) + top_strip * a
    save(out, "o4-hero-m.jpg", limit=110 * 1024, q=76)


def o4_detail():
    """Detail strip under the hero (rev-oct-04): hand in the pocket of the Sweater Fleece 1/4 Zip. Taken from
    the store original (sweater-fleece 08.png, 1200px, so 2x) instead of the rev-oct crop. 544 x 252 css,
    rounded top corners, torn bottom edge, on the Tap Shoe paper; file 1200 x 540 (600 x 270 css)."""
    W, H = 1200, 540
    x0, y0, x1, y1 = 56, 0, W - 56, 504             # photo box in the file (28 css side margins)
    base = fine("paper-tapshoe", H, w=W)
    src = Image.open(PROD / "mens-crater-valley-sweater-fleece-zip-jacket/08.png").convert("RGBA")
    bg = Image.new("RGBA", src.size, (38, 36, 36, 255))            # transparent studio corner -> dark studio
    bg.alpha_composite(src)
    ph = bg.convert("RGB")
    bw, bh = x1 - x0, y1 - y0
    crop_h = round(src.width * bh / bw)
    top = 320
    ph = ph.crop((0, top, src.width, top + crop_h)).resize((bw, bh), Image.LANCZOS)
    pa = np.asarray(ph, np.float32)
    arr = base.copy()
    mask = rrect_mask((W, H), (x0, y0, x1, y1 + 60), 24, corners=("tl", "tr"))
    ys = np.array(c.torn_line(W, y1 - 18, amp=8, seed=451))
    mm = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mm).polygon([(0, 0)] + [(x, y) for x, y in enumerate(ys)] + [(W, 0)], fill=255)
    tear = np.asarray(mm.filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255
    full = np.zeros_like(arr)
    full[y0:y1, x0:x1] = pa
    m = (mask * tear)[:, :, None]
    arr = arr * (1 - m) + full * m
    # soft shadow under the torn edge (the photo lies over the paper)
    yy = np.arange(H, dtype=np.float32)[:, None]
    d = yy - ys[None, :]
    inside = (np.arange(W)[None, :] > x0) & (np.arange(W)[None, :] < x1)
    arr *= (1 - np.where((d > 0) & inside, np.exp(-d / 7.0), 0) * 0.35)[:, :, None]
    save(arr, "o4-detail-pocket.jpg", limit=120 * 1024, q=78)


# Cards: table 530 css incl. 1px CSS border at x 35..564; inside: photo cell 240 (store backdrop 196 +
# 44 of brown where the model overlaps), text cell 288 with the product box. Inner height 330 css.
O4_CW, O4_CH, O4_PW = 240, 330, 196
O4_MW, O4_MH = 341, 300                  # mobile photo inside the 343 card (1px border each side)
BACKDROPS = {"hoodie": ("#A0958F", "#6E6461"), "fleece": ("#B8AEA5", "#8C9199"), "qzip": ("#6E655E", "#48403B")}


def _backdrop(w, h, top, bot, seed):
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    xx = np.linspace(0, 1, w, dtype=np.float32)[None, :, None]
    t = np.clip(yy * 0.75 + xx * 0.35, 0, 1)
    arr = np.array(c.rgb(top), np.float32) * (1 - t) + np.array(c.rgb(bot), np.float32) * t
    arr += (pn(w, h, 1.0, seed) * 1.6)[:, :, None]
    return arr


def _card(key, im, out, *, W, H, pw, corners, place_at, h, clip_top=False, seed=0):
    """One photo piece: backdrop box (x 0..pw) with the given rounded corners, rest brown fine grain, the
    model/garment over both, clipped at the top when the cut must sit on the card top line."""
    base = fine("grain-brown", H, w=W)
    back = _backdrop(W, H, *BACKDROPS[key], seed=seed)
    m = rrect_mask((W, H), (0, 0, pw - 1, H - 1), 26, corners=corners)[:, :, None]
    img = c.to_image(base * (1 - m) + back * m)
    # rounded outer corners: outside the curve the brown shows (the CSS border draws the line there)
    fit_im = c.fit(im, h=h)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c.place(lay, fit_im, place_at[0], (fit_im.height / 2 if clip_top else place_at[1]), 0, shadow=(8, 14, 22, 0.45))
    if corners == ("tl", "tr"):                  # mobile: rounded top corners, open at the bottom
        outer = rrect_mask((W, H), (0, 0, W - 1, H + 40), 26, corners=corners)
    else:                                        # desktop: rounded left corners, open to the right
        outer = rrect_mask((W, H), (0, 0, W + 40, H - 1), 26, corners=corners)
    a = np.asarray(lay.getchannel("A"), np.float32) * outer
    lay.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(lay)
    return save(img, out, limit=90 * 1024, q=78)


def o4_cards():
    """3 card photos (desktop + mobile). Client order: Performance Hoodie, Full Zip Fleece, Sweater Fleece 1/4 Zip,
    all with the photo on the left (rev-oct-04). Hoodie: model 08 hood up (head whole). Fleece: model 06 cut
    under the chin on the card top line (QA r1; the rev image shows the store forehead cut). 1/4 Zip: the APX
    packshot (the link variant; the store has no APX model shot), collar cut on the card top line."""
    W, H = O4_CW * 2, O4_CH * 2
    MW, MH = O4_MW * 2, O4_MH * 2
    hood = model("mens-crater-valley-performance-hoodie/08.png")
    fleece = model("mens-crater-valley-full-zip-fleece-jacket/06.png", chin=True)
    qzip = c.load_packshot(CV["qzip"])
    L = ("tl", "bl")
    _card("hoodie", hood, "o4-card-hoodie.jpg", W=W, H=H, pw=O4_PW * 2, corners=L, place_at=(236, 372), h=600, seed=1)
    _card("fleece", fleece, "o4-card-fleece.jpg", W=W, H=H, pw=O4_PW * 2, corners=L, place_at=(222, 0), h=720,
          clip_top=True, seed=2)
    qz = qzip.crop((0, int(qzip.height * 0.07), qzip.width, qzip.height))
    _card("qzip", qz, "o4-card-qzip.jpg", W=W, H=H, pw=O4_PW * 2, corners=L, place_at=(214, 0), h=640,
          clip_top=True, seed=3)
    T = ("tl", "tr")
    _card("hoodie", hood, "o4-card-hoodie-m.jpg", W=MW, H=MH, pw=MW, corners=T, place_at=(MW / 2, 318), h=580, seed=4)
    _card("fleece", fleece, "o4-card-fleece-m.jpg", W=MW, H=MH, pw=MW, corners=T, place_at=(MW / 2, 0), h=700,
          clip_top=True, seed=5)
    _card("qzip", qz, "o4-card-qzip-m.jpg", W=MW, H=MH, pw=MW, corners=T, place_at=(MW / 2, 0), h=640,
          clip_top=True, seed=6)


def o4_sunset():
    """Closing band photo (rev-oct-04): provisional 1x crop of the sunset silhouette (hunter and dog, halftone),
    from under the torn top edge to just above "FROM FIRST LIGHT TO"; a new tear from the Major Brown band on
    top (the photo sheet lies over the brown), bottom fading into NIGHT under the live headline."""
    ref = np.asarray(Image.open(REV4).convert("RGB"), np.float32)
    brown = np.array((72, 63, 57), np.float32)
    col_top = []
    for x in range(600):
        col = ref[2180:2260, x]
        diff = np.abs(col - brown).sum(1)
        idx = np.where(diff > 60)[0]
        col_top.append(2180 + (idx[0] if len(idx) else 40))
    y0 = max(col_top) + 3
    y1 = 2494
    ph = ref[y0:y1]
    Hp = ph.shape[0]
    TOP = 26                                            # brown rows above the new tear
    H = TOP + Hp + 40
    night = np.array(c.rgb(NIGHT), np.float32)
    arr = np.broadcast_to(night, (H, 600, 3)).copy()
    arr[TOP:TOP + Hp] = ph
    # the photo sheet starts with its own torn edge: extend the photo up with its first rows under the tear
    arr[:TOP] = ph[4:5]
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    k = c.smooth(np.clip((yy - (TOP + Hp - 90)) / 100, 0, 1))
    arr = arr * (1 - k) + night * k
    up = fine("grain-brown", H * 2, w=1200)
    up = np.asarray(c.to_image(up).convert("RGB").resize((600, H), Image.LANCZOS), np.float32)
    ys = c.torn_line(600, TOP - 8, amp=5, seed=471)
    out = torn_over(up, arr, ys, seed=471, rim_alpha=0.7, shadow=(4.0, 0.3), specks=False)
    print(f"      crop rows {y0}..{y1} of the rev image")
    p = save(out, "o4-rev-sunset.jpg", limit=90 * 1024, q=82)
    return p


def o4_edges():
    """04 torn edge NIGHT -> flat Tap Shoe footer (footer sheet over the night band)."""
    up = np.broadcast_to(np.array(c.rgb(NIGHT), np.float32), (80, 1200, 3)).copy()
    lo = np.broadcast_to(np.array(c.rgb(TAPSHOE), np.float32), (80, 1200, 3)).copy()
    ys = c.torn_line(1200, 44, amp=20, seed=481)
    out = torn_over(up, lo, ys, seed=481, rim_alpha=0.12, shadow=(6.0, 0.3))
    save(out, "o4-edge-night-footer.jpg", limit=20 * 1024, q=80, sub=0)


JOBS = {
    "o3-tex": o3_tex, "o3-hero": o3_hero, "o3-edges": o3_edges, "o3-panels": o3_panels,
    "o4-hero": o4_hero, "o4-detail": o4_detail, "o4-cards": o4_cards, "o4-sunset": o4_sunset, "o4-edges": o4_edges,
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
