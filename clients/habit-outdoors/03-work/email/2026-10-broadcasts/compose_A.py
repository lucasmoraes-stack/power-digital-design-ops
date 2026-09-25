"""compose_A.py - October 2026 Broadcasts, Designer A: assets for emails 01 (Cedar Branch Bibs) and 02 (Youth).

Imports the kit's compose.py (never edited) and redirects its output folder to this batch's assets/,
so nothing in the shared kit is written and nothing collides with compose_B.py / compose_C.py.
Kit textures are read from email-kit/assets; every file written here is assets/o1-* or assets/o2-*.

    python clients/habit-outdoors/03-work/email/2026-10-broadcasts/compose_A.py
    python .../compose_A.py --only o1-hero o2-packs
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

TAUPE = "#7F7064"                            # color.line_youth
c.TEXTURES["o2-taupe"] = ("o2-tex-taupe.jpg", TAUPE, "tile", "white (large text), youth panels")


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


def bleed_card(items, out, *, size, tex, bleed, haze_c, haze_s=0.55, seed=0, limit=110 * 1024, dm_tex=None, fade_px=50):
    """Products big on a soft glow over a fine-grain tile, cut by the `bleed` side (that side touches the
    email edge); the other sides fade back into the plain tile. items: [{file|img, h, cx, cy, angle}]."""
    W, H = size
    outs = []
    for suffix, t in [("", tex)] + ([("-dm", dm_tex)] if dm_tex else []):
        base = fine_base(t, W, H)
        arr = haze(base.copy(), W * 0.5, H * 0.5, W * 0.36, H * 0.32, haze_c if not suffix else "#4A4B50",
                   haze_s, seed=seed)
        img = c.to_image(arr)
        for it in items:
            p = it["img"] if "img" in it else c.load_packshot(it["file"])
            p = c.fit(p, h=it["h"])
            c.place(img, p, it["cx"], it["cy"], it.get("angle", 0), shadow=it.get("shadow", (10, 22, 26, 0.5)))
        keep = bleed if isinstance(bleed, tuple) else (bleed,)
        sides = [s for s in ("top", "bottom", "left", "right") if s not in keep]
        arr = edge_fade(np.asarray(img.convert("RGB"), np.float32), base, sides, px=fade_px)
        outs.append(save(arr, out.replace(".jpg", f"{suffix}.jpg"), limit=limit, q=78))
    return outs


def detail_photo(src, box, out, *, tex="paper-tapshoe", size=(600, 560), photo_w=560, angle=-1.5,
                 sides=("bottom", "right"), seed=0, limit=70 * 1024):
    """D2: detail crop of a store image, flattened, in a thin paper frame torn on 1-2 sides, rotated,
    soft shadow, baked on the band tile with faded borders (it sits beside a review box)."""
    im = Image.open(PRODUCTS / src).convert("RGBA")
    bg = Image.new("RGBA", im.size, (200, 198, 196, 255))
    bg.alpha_composite(im)
    ph = bg.convert("RGB").crop(box)
    fr = c.framed_photo_multi(ph, photo_w, frame=12, sides=sides, frame_color="#E2DDD9", seed=seed)
    W, H = size
    base = fine_base(tex, W, H)
    img = c.to_image(base)
    c.place(img, fr, W / 2, H / 2, angle, shadow=(6, 16, 20, 0.55))
    arr = edge_fade(np.asarray(img.convert("RGB"), np.float32), base, ("top", "bottom", "left", "right"), px=24)
    return save(arr, out, limit=limit, q=78)


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


# ---------------------------------------------------------------- 01 Cedar Branch Bibs

BIB = "ahabit-sup-sup-mens-insulated-bib--49451798790426"
PARKA = "habit-mens-cedar-branch-insulated-waterproof-parka--49451818385690"


def o1_hero():
    """E24 hero 01: three hunters walking up the field at sunrise (orig-hunt22). Sky grown up as a fog and
    pulled toward Tap Shoe paper for the white logo; label boxes (live text) sit over the upper area;
    the grass melts into Tap Shoe paper for subtitle + button, then tears into Major Brown grain."""
    ph = c.fit(c.lifestyle("orig-hunt22-three-hunters-field-sunrise.jpg"), w=1200).filter(ImageFilter.GaussianBlur(0.45))
    a = np.asarray(ph, np.float32)
    a = a * np.array([1.0, 0.97, 0.92], np.float32) * 0.92          # a touch warmer and lower: first light
    ph = soften_top(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 200)
    p = c.compose_full_bleed_hero(ph, "o1-hero.jpg", size=(1200, 1400), photo_w=1200, photo_y=260,
                                  extend_top="fog", top_shade=(620, 0.72), fade=(860, 1050),
                                  tear_y=1350, next_tex="grain-brown", grain_sd=1.8, seed=501,
                                  text_boxes={"logo": (440, 50, 760, 130), "sub+button": (100, 1060, 1100, 1320)})
    return p


def o1_label():
    """Label-box paper for the hero headline: a 720x180 crop of the kit paper-light tile (cells are at most
    360x90 px, shown at background-size 360px), so the email does not download the 88 KB tile for three labels."""
    save(tile("paper-light", 180, w=720), "o1-tex-label.jpg", limit=20 * 1024, q=76)


def o1_products():
    """E1 band 3 (QA r1): bib and parka at about 1.5x, 20 to 30% of each garment out through the email edge
    (bib left, parka right); what passes the bottom of the image dissolves into the grain over 110px."""
    # bib: 1500px tall (2x the r0 740px; the garment itself is about 405px wide), about 25% out on the left (the trimmed store PNG is wider than the garment: legs splay), chest, straps, logo and thighs in frame
    bleed_card([{"file": BIB, "h": 1500, "cx": 206, "cy": 776, "angle": 3}], "o1-prod-bibs.jpg",
               size=(600, 720), tex="grain-brown", bleed="left", haze_c="#7A6C60", haze_s=0.3, seed=511,
               fade_px=110)
    # parka: 840px tall (541 wide), 25% out on the right (sleeve cut), hem dissolves at the bottom
    bleed_card([{"file": PARKA, "h": 840, "cx": 466, "cy": 440, "angle": -4}], "o1-prod-parka.jpg",
               size=(600, 720), tex="grain-brown", bleed="right", haze_c="#7A6C60", haze_s=0.3, seed=512,
               fade_px=110)


def detail_cutout(src, box, out, *, tex="paper-tapshoe", size=(600, 560), height=520, angle=-4, top_fade=0.18,
                  seed=0, limit=70 * 1024):
    """D2 for a store image that is already cut out (transparent studio background): the garment itself on
    the band paper with a soft shadow, no frame and no studio backdrop. The source's own top edge (a straight
    cut through the garment) fades out over `top_fade` of the height."""
    im = Image.open(PRODUCTS / src).convert("RGBA").crop(box)
    a = np.asarray(im.getchannel("A"), np.float32)
    ys = np.arange(a.shape[0], dtype=np.float32)[:, None]
    a *= c.smooth(np.clip(ys / (top_fade * a.shape[0]), 0, 1))
    im.putalpha(Image.fromarray(a.astype(np.uint8)))
    im = c.fit(im.crop(im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()), h=height)
    W, H = size
    base = fine_base(tex, W, H)
    img = c.to_image(base)
    c.place(img, im, W / 2, H / 2 + 6, angle, shadow=(8, 18, 22, 0.55))
    arr = edge_fade(np.asarray(img.convert("RGB"), np.float32), base, ("top", "bottom", "left", "right"), px=24)
    return save(arr, out, limit=limit, q=78)


def o1_details():
    """E1 band 4 (D2, QA r1): parka chest pocket (Matthew B.), hand on the bib's front zipper (Ryan And L.),
    leg zipper over the whole boot (Andrew C.). Each reads as garment construction at a glance."""
    detail_photo("habit-mens-cedar-branch-insulated-waterproof-parka/06.png", (0, 250, 1080, 1060),
                 "o1-detail-pocket.jpg", angle=-1.8, sides=("bottom", "right"), seed=521)   # label below y 1090 cut off
    detail_photo("ahabit-sup-sup-mens-insulated-bib/08.png", (60, 0, 1200, 910),
                 "o1-detail-zipper.jpg", angle=1.6, sides=("top", "left"), seed=522)
    detail_cutout("ahabit-sup-sup-mens-insulated-bib/07.png", (0, 0, 1200, 1200), "o1-detail-legzip.jpg",
                  height=520, angle=-6, top_fade=0.07, seed=523)


def o1_edges():
    """E18 textured edge: Tap Shoe paper (reviews) -> Ivy grain (split band). Kit edges cover the rest."""
    # Same drawing as compose.compose_torn_edge_textured, but the upper sheet is the tile with its slow
    # mottle removed (fine_base): the reviews band ends at an arbitrary tile phase, and the tile's last
    # rows sat 1.7 levels darker than the band above them (a visible step in the render).
    import random
    from PIL import ImageDraw
    h, W = 80, 1200
    up = fine_base("paper-tapshoe", W, h) + 0.6
    lo = c.tile_rows("grain-ivy", h, end=True)
    ys = c.torn_line(W, h * 0.45, amp=8, seed=531)
    m = Image.new("L", (W, h), 0)
    ImageDraw.Draw(m).polygon([(0, h)] + [(x, y) for x, y in enumerate(ys)] + [(W, h)], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[:, :, None] / 255
    c.tear_shadow(up, ys)
    canvas = c.to_image(up * (1 - a) + lo * a)
    rnd, d = random.Random(532), ImageDraw.Draw(canvas)
    spot = tuple(int(v) for v in np.median(lo.reshape(-1, 3), 0))
    for _ in range(30):
        x = rnd.randrange(W)
        y = ys[x] - rnd.uniform(3, 10)
        r = rnd.choice((1.2, 1.6, 2.2))
        d.ellipse((x - r, y - r, x + r, y + r), fill=spot + (255,))
    save(canvas, "o1-edge-papertapshoe-ivy.jpg", limit=30 * 1024, q=80, sub=0)


# ---------------------------------------------------------------- 02 Youth

YBIB = "youth-cedar-branch-insulated-bib--52632814518554"
YHOOD = "habit-youth-summit-park-performance-hoodie--51341422592282"
YPANT = "youth-bear-cave-6-pocket-camo-pant--39568503668787"


def o2_hero():
    """E24 hero 02: family in camp chairs, the kid in the middle (crop-sent-sep15). Calm area grown above
    as fog for logo + two-voice headline; melts into Tap Shoe paper, tears into Major Brown grain."""
    ph = soften_top(c.lifestyle("crop-sent-sep15-camp-chairs-family.jpg"), 110)
    p = c.compose_full_bleed_hero(ph, "o2-hero.jpg", size=(1200, 1500), photo_w=1300, photo_y=830,
                                  extend_top="fog", top_shade=(880, 0.55), fade=(1250, 1385),
                                  tear_y=1450, next_tex="grain-brown", grain_sd=2.4, seed=601,
                                  text_boxes={"desktop": (100, 160, 1100, 820), "mobile": (190, 130, 1010, 830)})
    return p


def o2_texture():
    """Taupe (color.line_youth) paper grain tile for the youth product panels, 600x600, periodic."""
    arr = c.paper_surface(TAUPE, size=(600, 600), grain_sd=3.0, mottle=1.0, fibre=5, fibre_sign=1, seed=611)
    p = save(arr, "o2-tex-taupe.jpg", limit=40 * 1024, q=74)
    print("     ", c.contrast_report(p, ["#FFFFFF"], blur=0))


def o2_packs():
    """E2 band 3 packshots (transparent PNG, sit on the taupe panel td)."""
    c.product_png(YBIB, 480, "o2-pack-bib.png", pad=0.02, limit=90 * 1024)
    im = clean_hoodie()
    im = c.fit(im, w=430) if im.width >= im.height else c.fit(im, h=430)
    cv = Image.new("RGBA", (480, 480), (0, 0, 0, 0))
    cv.alpha_composite(im, ((480 - im.width) // 2, (480 - im.height) // 2))
    c.report(c.save_png_quant(cv, "o2-pack-hoodie.png", limit=90 * 1024), limit=90 * 1024)
    c.product_png(YPANT, 480, "o2-pack-pant.png", pad=0.02, limit=90 * 1024)


def clean_hoodie() -> Image.Image:
    """Youth Summit Park hoodie packshot without the faint full-frame alpha haze of the store PNG
    (alpha under 40 is dropped, then trimmed): placed as is, the haze shows as a pale rectangle."""
    im = Image.open(PRODUCTS / (YHOOD + ".png")).convert("RGBA")
    a = im.getchannel("A").point(lambda v: 0 if v < 40 else v)
    im.putalpha(a)
    return im.crop(a.getbbox())


def o2_layer():
    """E2 band 4: Summit Park Hoodie behind the Cedar Branch Bib (layered), transparent PNG with soft shadow:
    it sits on the light paper td in light mode and on the dark paper in dark mode (no -dm twin, no seam)."""
    cv = Image.new("RGBA", (600, 800), (0, 0, 0, 0))
    c.place(cv, c.fit(clean_hoodie(), h=450), 215, 285, 7, shadow=(10, 22, 26, 0.45))
    c.place(cv, c.fit(c.load_packshot(YBIB), h=650), 330, 420, -3, shadow=(10, 22, 26, 0.45))
    c.report(c.save_png_quant(cv, "o2-layer.png", limit=110 * 1024), limit=110 * 1024)


JOBS = {"o1-hero": o1_hero, "o1-label": o1_label, "o1-products": o1_products, "o1-details": o1_details, "o1-edges": o1_edges,
        "o2-hero": o2_hero, "o2-texture": o2_texture, "o2-packs": o2_packs, "o2-layer": o2_layer}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="*", choices=sorted(JOBS))
    a = ap.parse_args()
    for k in a.only or JOBS:
        print(f"[{k}] {JOBS[k].__doc__.strip().splitlines()[0]}")
        JOBS[k]()


if __name__ == "__main__":
    main()
