"""compose_A.py - October 2026 Broadcasts, Designer A: assets for emails 01 (Cedar Branch Bibs) and 02 (Youth).

Round 2 (2026-09-25): rebuilt for the owner's revised designs (email-kit/references/rev-oct-01/02-*.png).
Files named o{nn}-rev-* are PROVISIONAL 1x crops taken from those revised PNGs (the original photos are
not on this machine): replace them with the originals before send.

Imports the kit's compose.py (never edited) and redirects its output folder to this batch's assets/,
so nothing in the shared kit is written and nothing collides with compose_B.py / compose_C.py.
Kit textures are read from email-kit/assets; every file written here is assets/o1-* or assets/o2-*.

    python clients/habit-outdoors/03-work/email/2026-10-broadcasts/compose_A.py
    python .../compose_A.py --only o1-hero o2-panels
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "01-brand" / "email-kit" / "tools"))
import compose as c  # noqa: E402

BATCH_ASSETS = HERE / "assets"
BATCH_ASSETS.mkdir(exist_ok=True)
KIT_ASSETS = c.KIT / "assets"
c.ASSETS = BATCH_ASSETS                      # compose.py writers resolve c.ASSETS at call time

# Round 2 surface: Major Brown grain with halftone dot splotches (rev-oct-01 band 2). Its first rows are the kit
# grain-brown first rows, so the hero tear (kit grain-brown last rows) runs into it without a step.
c.TEXTURES["o1-halftone"] = ("o1-tex-halftone.jpg", c.BROWN, "tile", "white, #E2DDD9 body, orange only large")


def _tex_path(name: str) -> Path:
    f = c.TEXTURES[name][0]
    return (BATCH_ASSETS if f.startswith("o") and f[1] in "12" else KIT_ASSETS) / f


c.tex_path = _tex_path                        # load_tile / tile_rows look this up at call time

MAX_IMG = 150 * 1024
PRODUCTS = c.PRODUCTS


# ---------------------------------------------------------------- helpers

def save(img, name, limit=MAX_IMG, q=76, floor=50, sub=2):
    im = img if isinstance(img, Image.Image) else c.to_image(img)
    p = c.save_jpg_under(im, BATCH_ASSETS / name, limit, q=q, floor=floor, subsampling=sub)
    print(f"  {p.name:36s} {Image.open(p).size}  {p.stat().st_size / 1024:6.1f} KB")
    return p


def tile(name, h, y0=0, w=1200):
    t = c.load_tile(name)
    reps = math.ceil((y0 + h) / t.shape[0]) + 1
    tt = np.concatenate([t] * reps, axis=0)
    reps_x = math.ceil(w / tt.shape[1])
    tt = np.concatenate([tt] * reps_x, axis=1)
    return tt[y0:y0 + h, :w].copy()


def fine_base(name, w, h, y0=0):
    """Tile crop with its slow mottle removed and re-centred on the tile mean: any image border then
    meets the <td> background (same tile, other phase) without a visible step."""
    base = tile(name, h, y0=y0, w=w)
    low = np.asarray(c.to_image(base).convert("RGB").filter(ImageFilter.GaussianBlur(40)), np.float32)
    return base - low + c.load_tile(name).reshape(-1, 3).mean(0)


def haze(arr, cx, cy, rx, ry, color, strength, seed=1, window=200):
    h, w = arr.shape[:2]
    yy = (np.arange(h, dtype=np.float32)[:, None] - cy) / ry
    xx = (np.arange(w, dtype=np.float32)[None, :] - cx) / rx
    m = np.exp(-(xx ** 2 + yy ** 2))
    ys_, xs_ = np.arange(h, dtype=np.float32), np.arange(w, dtype=np.float32)
    wy = c.smooth(np.clip(np.minimum(ys_, h - 1 - ys_) / window, 0, 1))[:, None]
    wx = c.smooth(np.clip(np.minimum(xs_, w - 1 - xs_) / window, 0, 1))[None, :]
    n = c.periodic_noise(w, h, 90, 90, seed) * 0.5 + c.periodic_noise(w, h, 30, 30, seed + 1) * 0.25
    m = np.clip(m * wy * wx * np.clip(1 + n * 0.6, 0, 1.6) * strength, 0, 1)[:, :, None]
    return arr * (1 - m) + np.array(c.rgb(color), np.float32) * m


def edge_fade(arr, base, sides, px=60):
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


def soften_top(ph, rows, blur=60):
    """Blend the top `rows` of a photo toward a heavy horizontal blur of themselves (weight 1 at row 0,
    0 at `rows`): compose.py grows the fog from rows 2-14, and branches or trunks there turn into
    vertical streaks; softened rows give an even mist instead."""
    a = np.asarray(ph.convert("RGB"), np.float32)
    top = Image.fromarray(np.clip(a[:rows], 0, 255).astype(np.uint8))
    bl = np.asarray(top.filter(ImageFilter.BoxBlur(blur)).filter(ImageFilter.GaussianBlur(blur / 2)), np.float32)
    w = (1 - c.smooth(np.clip(np.arange(rows, dtype=np.float32) / rows, 0, 1)))[:, None, None]
    a[:rows] = a[:rows] * (1 - w) + bl * w
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def contrast(p, box, texts=("#FFFFFF", "#E2DDD9")):
    print(f"      text area {box}: {c.contrast_report(p, list(texts), box)}")


def rrect_mask(size, r, corners=(True, True, True, True)):
    """L mask of a rounded rectangle; corners = (tl, tr, br, bl)."""
    from PIL import ImageDraw
    W, H = size
    m = Image.new("L", (W * 4, H * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, W * 4 - 1, H * 4 - 1), r * 4, fill=255, corners=corners)
    return m.resize((W, H), Image.LANCZOS)


def _band_crop(name, box, s=2):
    """Exact crop of a batch/kit tile at a desktop band position (display box, file = 2x): the image then
    continues the <td> background of its band with no seam on desktop."""
    t = c.load_tile(name)
    x0, y0, x1, y1 = [v * s for v in box]
    reps = math.ceil(y1 / t.shape[0]) + 1
    tt = np.concatenate([t] * reps, axis=0)
    return tt[y0:y1, x0:x1].copy()


# ---------------------------------------------------------------- 01 Cedar Branch Bibs (round 2)

BIB = "ahabit-sup-sup-mens-insulated-bib--49451798790426"
PARKA = "habit-mens-cedar-branch-insulated-waterproof-parka--49451818385690"

# band 2 geometry, display px (file = 2x): row A = bib 210 x 600 at x 0; row B = parka 270 x 480 at x 330
O1_BAND_H = 1080
O1_BIB_BOX = (0, 0, 210, 600)
O1_PARKA_BOX = (330, 600, 600, 1080)
O1_REVIEW_H = 374                      # review band height (its image cell fixes it)


def o1_hero():
    """E24 hero 01 (round 2): orig-hunt22 framed like rev-oct-01 (x1.24, hunters left of centre, sky from the
    top), label boxes over the trees, photo melts into Tap Shoe paper for subtitle + button, tears into the
    Major Brown halftone band at 717px."""
    src = c.lifestyle("orig-hunt22-three-hunters-field-sunrise.jpg")
    ph = c.fit(src, w=1488).filter(ImageFilter.GaussianBlur(0.8))
    ph = ph.crop((288, 0, 1488, ph.height))
    a = np.asarray(ph, np.float32)
    a = a * 0.82 + a.mean(2, keepdims=True) * 0.18                 # a little muted, like the revised image
    a = a * np.array([0.98, 0.97, 0.95], np.float32) * 0.86
    ph = soften_top(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 90)
    p = c.compose_full_bleed_hero(ph, "o1-hero.jpg", size=(1200, 1480), photo_w=1200, photo_y=90,
                                     extend_top="fog", top_shade=(300, 0.45), fade=(935, 1075),
                                     tear_y=1434, next_tex="grain-brown", grain_sd=1.8, seed=501,
                                     text_boxes={"logo": (440, 60, 760, 120), "sub+button": (140, 1100, 1060, 1390)})
    # compose.py stops at q52; the new 1480-row hero needs a little more to stay under 150 KB
    return save(Image.open(p).convert("RGB"), "o1-hero.jpg", limit=150 * 1024, q=60, floor=40)


def o1_label():
    """Label-box paper for the hero headline (light boxes): 720x180 crop of the kit paper-light tile."""
    save(tile("paper-light", 180, w=720), "o1-tex-label.jpg", limit=20 * 1024, q=76)


def _halftone_density(W, H, s):
    """Density field 0..1 for the dot splotches, laid out on the desktop band (display px * s)."""
    yy = np.arange(H, dtype=np.float32)[:, None] / s
    xx = np.arange(W, dtype=np.float32)[None, :] / s
    d = np.zeros((H, W), np.float32)

    def blob(cx, cy, rx, ry, k, rot=0.0):
        nonlocal d
        cr, sr = math.cos(rot), math.sin(rot)
        u = ((xx - cx) * cr + (yy - cy) * sr) / rx
        v = (-(xx - cx) * sr + (yy - cy) * cr) / ry
        d = np.maximum(d, k * np.exp(-(u ** 2 + v ** 2) ** 1.4))

    # rev-oct-01 band 2, in band-cell px (the tile starts at the band <td> top, page y 740). No dots within
    # ~30px of the parka image rectangle (x 330-600, y 600-1080): on mobile that image lands at another place
    # of the tile. The bib image (x 0-210, y 0-600) stays seamless on mobile too (left-aligned, tile unscaled).
    blob(10, 400, 45, 150, 1.15)                      # dark patch on the left edge beside the bib legs
    blob(215, 425, 45, 110, 0.75)                     # right of the bib legs
    blob(200, 600, 230, 62, 0.95, rot=-0.35)          # diagonal sweep under the bib, rising to the right
    blob(80, 690, 140, 60, 0.95, rot=-0.2)
    blob(190, 955, 90, 50, 0.95, rot=0.1)             # cluster under the parka card
    blob(25, 940, 50, 60, 0.55)
    blob(585, 90, 30, 50, 0.45)                       # small touch top right
    n = c.periodic_noise(W, H, 40 * s, 40 * s, 707) * 0.18 + c.periodic_noise(W, H, 14 * s, 14 * s, 708) * 0.08
    d = np.clip(d * (1 + n) - 0.05, 0, 1)
    x0, y0 = (O1_PARKA_BOX[0] - 30) * s, (O1_PARKA_BOX[1] - 30) * s
    ramp = 80 * s                                     # keep the parka rectangle and its margin clean, soft edge
    kx = c.smooth(np.clip((x0 - np.arange(W, dtype=np.float32)) / ramp, 0, 1))[None, :]
    ky = c.smooth(np.clip((y0 - np.arange(H, dtype=np.float32)) / ramp, 0, 1))[:, None]
    d *= 1 - (1 - kx) * (1 - ky)
    return d


def o1_halftone():
    """Major Brown grain + halftone dot splotches, 1200 x 2160 (the whole desktop band 2, 600 x 1080).
    Grain = kit grain-brown rows 0..2159 (wrapping at 1600), so its top continues the hero tear; dots are
    irregular ellipses on a jittered hex grid, radius from a density field, merged into solid patches where
    dense, in a darker brown at ~80%."""
    from PIL import ImageDraw
    import random
    s = 2
    W, H = 1200, O1_BAND_H * s
    base = tile("grain-brown", H, w=W)
    dens = _halftone_density(W, H, s)
    step = 10.0 * s
    m = Image.new("L", (W * 2, H * 2), 0)            # 2x supersampled mask
    dr = ImageDraw.Draw(m)
    rnd = random.Random(711)
    row, y = 0, 0.0
    while y < H:
        x = (step / 2) if row % 2 else 0.0
        while x < W:
            jx, jy = x + rnd.uniform(-2.5, 2.5) * s, y + rnd.uniform(-2.5, 2.5) * s
            xi, yi = int(min(W - 1, max(0, jx))), int(min(H - 1, max(0, jy)))
            k = dens[yi, xi]
            if k > 0.08:
                r = step * 0.46 * k ** 0.85 * rnd.uniform(0.85, 1.15)
                ex, ey = r * rnd.uniform(0.9, 1.25), r * rnd.uniform(0.8, 1.05)
                dr.ellipse(((jx - ex) * 2, (jy - ey) * 2, (jx + ex) * 2, (jy + ey) * 2), fill=255)
            x += step
        y += step * 0.866
        row += 1
    m = m.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.35))
    a = np.asarray(m, np.float32)[:, :, None] / 255 * 0.92
    ink = np.array(c.rgb("#28201A"), np.float32)
    arr = base * (1 - a) + (base * 0.35 + ink * 0.65) * a
    p = save(arr, "o1-tex-halftone.jpg", limit=150 * 1024, q=70, floor=45)
    print("     ", c.contrast_report(p, ["#FFFFFF", "#FF6400"], blur=0))
    return p


def o1_products():
    """E1 band 2 (round 2): bib standing whole at the left (row A), parka cut by the right email edge (row B).
    Each image is the exact halftone-band crop under its desktop cell, so desktop shows no seam at all."""
    img = c.to_image(_band_crop("o1-halftone", O1_BIB_BOX))
    c.place(img, c.fit(c.load_packshot(BIB), h=1110), 222, 80 + 555, 0, shadow=(10, 22, 26, 0.5))
    save(img, "o1-prod-bibs.jpg", limit=110 * 1024, q=78)
    img = c.to_image(_band_crop("o1-halftone", O1_PARKA_BOX))
    c.place(img, c.fit(c.load_packshot(PARKA), h=1000), 344, 16 + 500, 0, shadow=(10, 22, 26, 0.5))
    save(img, "o1-prod-parka.jpg", limit=110 * 1024, q=78)


def o1_review_parka():
    """E1 review band: the parka close (hood + chest), cut by the right edge and the band bottom, on the exact
    Tap Shoe paper crop under its desktop cell (x 350-600, y 0-374); left side dissolves into the paper."""
    box = (350, 0, 600, O1_REVIEW_H)
    base = _band_crop("paper-tapshoe", box)
    img = c.to_image(base)
    c.place(img, c.fit(c.load_packshot(PARKA), h=1300), 300, 24 + 650, 0, shadow=(10, 22, 26, 0.5))
    arr = edge_fade(np.asarray(img.convert("RGB"), np.float32), base, ("left",), px=70)
    save(arr, "o1-review-parka.jpg", limit=90 * 1024, q=78)


def o1_rev_archer():
    """PROVISIONAL 1x: rev-oct-01 closing photo (archer in camo with the drawn white line), page rows 2171-2517
    (clean: no live text over them), grown down to 731 rows by fading into near black for the live text."""
    ref = Image.open(c.REFS / "rev-oct-01-cedar-branch-bibs.png").convert("RGB")
    top = np.asarray(ref.crop((0, 2171, 600, 2517)), np.float32)
    H = 731
    dark = np.array(c.rgb("#141414"), np.float32)
    arr = np.broadcast_to(dark, (H, 600, 3)).copy()
    arr[:top.shape[0]] = top
    ys = np.arange(H, dtype=np.float32)
    t = c.smooth(np.clip((ys - 250) / (346 - 250), 0, 1))[:, None, None]
    arr = arr * (1 - t * 0.78) + dark * (t * 0.78)
    t2 = c.smooth(np.clip((ys - 330) / 30, 0, 1))[:, None, None]
    arr = arr * (1 - t2) + dark * t2
    arr += (c.periodic_noise(600, H, 0.75, 0.75, 721) * 2.0)[:, :, None]
    p = save(arr, "o1-rev-archer.jpg", limit=90 * 1024, q=80)
    contrast(p, (60, 340, 540, 700))


# ---------------------------------------------------------------- 02 Youth (round 2)

YBIB = "youth-cedar-branch-insulated-bib--52632814518554"
YHOOD = "habit-youth-summit-park-performance-hoodie--51341422592282"
YPANT = "youth-bear-cave-6-pocket-camo-pant--39568503668787"

# flat panel colours measured on rev-oct-02 (olive = kit Ivy Green)
PANEL = {"bib": "#595442", "hoodie": "#774727", "pant": "#4F5C5F"}


def o2_hero():
    """E24 hero 02 (round 2): family in camp chairs low in the frame (rev-oct-02), fog above for the two-voice
    headline + button; the grass melts into Tap Shoe paper and the last rows ARE the kit tile's last rows, so
    the Tap Shoe band below continues it (straight cut, no tear)."""
    W, H = 1200, 1344
    ph = soften_top(c.lifestyle("crop-sent-sep15-camp-chairs-family.jpg"), 110)
    tmp = c.compose_full_bleed_hero(ph, "o2-hero-tmp.jpg", size=(W, H + 120), photo_w=1300, photo_y=770,
                                    extend_top="fog", top_shade=(820, 0.50), fade=(1180, 1300),
                                    tear_y=H + 60, next_tex="paper-tapshoe", grain_sd=2.4, seed=601)
    arr = np.asarray(Image.open(tmp).convert("RGB"), np.float32)[:H]
    tmp.unlink()
    end = c.tile_rows("paper-tapshoe", 140, end=True)
    w = c.smooth(np.clip((np.arange(140, dtype=np.float32)) / 90, 0, 1))[:, None, None]
    arr[H - 140:] = arr[H - 140:] * (1 - w) + end * w
    p = save(arr, "o2-hero.jpg", limit=150 * 1024, q=74)
    contrast(p, (120, 200, 1080, 900))
    return p


def clean_hoodie() -> Image.Image:
    """Youth Summit Park hoodie packshot without the faint full-frame alpha haze of the store PNG
    (alpha under 40 is dropped, then trimmed): placed as is, the haze shows as a pale rectangle."""
    im = Image.open(PRODUCTS / (YHOOD + ".png")).convert("RGBA")
    a = im.getchannel("A").point(lambda v: 0 if v < 40 else v)
    im.putalpha(a)
    return im.crop(a.getbbox())


def o2_panels():
    """E2 framed cards: packshot on a flat colour panel, 196 x 330 (file 392 x 660). Bib and pant are cut by the
    card bottom as in rev-oct-02; the hoodie sits whole. Flat colour = the td bgcolor, so on mobile the panel
    widens with the same colour and no seam."""
    jobs = [("bib", c.load_packshot(YBIB), 820, 196, 62 + 410),
            ("hoodie", clean_hoodie(), 470, 184, 100 + 235),
            ("pant", c.load_packshot(YPANT), 712, 188, 60 + 356)]
    for key, im, h, cx, cy in jobs:
        base = np.broadcast_to(np.array(c.rgb(PANEL[key]), np.float32), (660, 392, 3)).copy()
        base += (c.periodic_noise(392, 660, 0.75, 0.75, 731) * 1.4)[:, :, None]
        img = c.to_image(base)
        c.place(img, c.fit(im, h=h), cx, cy, 0, shadow=(8, 18, 22, 0.45))
        save(img, f"o2-panel-{key}.jpg", limit=60 * 1024, q=80)


def o2_edges():
    """Tap Shoe paper band -> gradient into Major Brown -> torn into light paper (rev-oct-02, under SHOP NOW),
    1200 x 120 (600 x 60). -dm twin: the light paper below is the kit dark-mode paper."""
    import random
    from PIL import ImageDraw
    W, h = 1200, 120
    up = fine_base("paper-tapshoe", W, h)
    brown = np.array(c.rgb("#443A33"), np.float32)
    t = c.smooth(np.clip(np.arange(h, dtype=np.float32) / 96, 0, 1))[:, None, None]
    up = up * (1 - t) + (up - up.mean((0, 1)) + brown) * t
    ys = c.torn_line(W, 94, amp=7, seed=741)
    for suffix, tex in (("", "paper-light"), ("-dm", "paper-light-dm")):
        u = up.copy()
        lo = c.tile_rows(tex, h, end=True)
        m = Image.new("L", (W, h), 0)
        ImageDraw.Draw(m).polygon([(0, h)] + [(x, y) for x, y in enumerate(ys)] + [(W, h)], fill=255)
        a = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[:, :, None] / 255
        c.tear_shadow(u, ys)
        canvas = c.to_image(u * (1 - a) + lo * a)
        rnd, d = random.Random(742), ImageDraw.Draw(canvas)
        spot = tuple(int(v) for v in np.median(lo.reshape(-1, 3), 0))
        for _ in range(40):
            x = rnd.randrange(W)
            y = ys[x] - rnd.uniform(3, 10)
            r = rnd.choice((1.2, 1.6, 2.2))
            d.ellipse((x - r, y - r, x + r, y + r), fill=spot + (255,))
        save(canvas, f"o2-edge-tapshoe-paperlight{suffix}.jpg", limit=30 * 1024, q=80, sub=0)


def o2_rev_boy():
    """PROVISIONAL 1x: the boy photo inside the tilted frame of rev-oct-02 (page ~0-220 x 2283-2612), rotated
    back upright and cut inside the white frame, then re-framed (6px white), tilted 5.8 degrees like the
    image, soft shadow, on a TRANSPARENT canvas: it sits on the light paper and on the dark-mode paper."""
    ref = Image.open(c.REFS / "rev-oct-02-youth-season.png").convert("RGB")
    crop = ref.crop((0, 2250, 280, 2650))                    # frame centre ~ (110, 2447) -> (110, 197)
    up = crop.rotate(-5.8, resample=Image.BICUBIC, center=(110, 197))
    ph = up.crop((110 - 84, 197 - 145, 110 + 84, 197 + 145))  # inside the 7px frame, a few px of margin
    fw = 6
    fr = Image.new("RGBA", (ph.width + fw * 2, ph.height + fw * 2), (255, 255, 255, 255))
    fr.paste(ph, (fw, fw))
    cv = Image.new("RGBA", (240, 350), (0, 0, 0, 0))
    c.place(cv, fr, 104, 172, 5.8, shadow=(4, 8, 10, 0.45))
    c.report(c.save_png_quant(cv, "o2-rev-boy.png", limit=110 * 1024), limit=110 * 1024)


JOBS = {"o1-hero": o1_hero, "o1-label": o1_label, "o1-halftone": o1_halftone, "o1-products": o1_products,
        "o1-review": o1_review_parka, "o1-archer": o1_rev_archer,
        "o2-hero": o2_hero, "o2-panels": o2_panels, "o2-edges": o2_edges, "o2-boy": o2_rev_boy}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="*", choices=sorted(JOBS))
    a = ap.parse_args()
    for k in a.only or JOBS:
        print(f"[{k}] {JOBS[k].__doc__.strip().splitlines()[0]}")
        JOBS[k]()


if __name__ == "__main__":
    main()
