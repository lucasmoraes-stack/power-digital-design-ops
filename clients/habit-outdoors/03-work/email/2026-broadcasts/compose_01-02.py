"""compose_01-02.py - 2026 Broadcasts, Designer A: assets for emails 01 and 02 (jobs A1 to A3 of brief.md).

Imports the kit's compose.py (never edited) and writes every output into this batch's own
assets/ folder, so the kit assets and Designer B's files are never touched.

Run from anywhere:
    python clients/habit-outdoors/03-work/email/2026-broadcasts/compose_01-02.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "01-brand" / "email-kit" / "tools"))
import compose as c  # noqa: E402

BATCH_ASSETS = Path(__file__).resolve().parent / "assets"
BATCH_ASSETS.mkdir(exist_ok=True)

# compose.py saves into its own ASSETS (the kit folder) and also reads texture-light.jpg from there.
# Redirect only the two save functions to the batch folder, so reads still come from the kit.
_orig_jpg, _orig_png = c.save_jpg, c.save_png_quant


def _in_batch(fn):
    def wrapped(*a, **k):
        kit = c.ASSETS
        c.ASSETS = BATCH_ASSETS
        try:
            return fn(*a, **k)
        finally:
            c.ASSETS = kit
    return wrapped


c.save_jpg = _in_batch(_orig_jpg)
c.save_png_quant = _in_batch(_orig_png)

# Some store cutouts keep a full-width white strip of background at the top or bottom edge
# (men-s-roaring-springs-packable-rain-jacket--39299390472243: rows 0-19). It shows as a white bar
# over the model's head on the brown card. Clear the full-width edge rows that belong to that strip,
# then let compose.py trim to the opaque bounds as usual. Other packshots have no such rows.
_orig_load = c.load_packshot


def _load_clean(name):
    p = c.PRODUCTS / name
    if not p.suffix:
        p = p.with_suffix(".png")
    im = c.Image.open(p).convert("RGBA")
    a = c.np.asarray(im).copy()
    w = a.shape[1]

    def bad(y):
        # the strip spans the whole width (white core + a faint antialiased row under it);
        # a real garment or head row this close to the edge is far narrower
        return (a[y, :, 3] > 8).sum() > w * 0.5 and (a[max(y - 1, 0):y + 2, :, :3].min(axis=2) > 230).any()

    for rows in (range(a.shape[0]), reversed(range(a.shape[0]))):
        for y in rows:
            if not bad(y):
                break
            a[y, :, 3] = 0
    im = c.Image.fromarray(a, "RGBA")
    m = im.getchannel("A").point(lambda v: 255 if v > 8 else 0)
    return im.crop(m.getbbox())


c.load_packshot = _load_clean


def job_a1():
    """A1 packs E1 (3 PNG 400x400)."""
    c.product_png("mlf-1-4-zip-camo-performance-layer--47952634413338", 400,
                  "pack-mlf-1-4-zip-camo-performance-layer-400.png")
    c.product_png("mens-flushing-bay-short-sleeve-river-shirt--49918052925722", 400,
                  "pack-mens-flushing-bay-short-sleeve-river-shirt-400.png")
    c.product_png("men-s-roaring-springs-packable-rain-jacket--39299390472243", 400,
                  "pack-men-s-roaring-springs-packable-rain-jacket-400.png")


def job_a2():
    """A2 packs E2 (3 PNG 400 + fallback E04 PNG 360)."""
    c.product_png("habit-mens-wj657-cedar-branch-insulated-waterproof-bomber--51265344733466", 400,
                  "pack-habit-mens-wj657-cedar-branch-insulated-waterproof-bomber-400.png")
    c.product_png("mens-performance-fleece-hoodie--45600303677722", 400,
                  "pack-mens-performance-fleece-hoodie-400.png")
    c.product_png("men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt--32728036802611", 400,
                  "pack-men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt-400.png")
    c.product_png("men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt--32728036802611", 360,
                  "pack-men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt-360.png")


def job_a3():
    """A3 E19 hero E2: 1200x720, top #2A2B2D, bottom #483F39. Geometry = kit sample x0.857 (brief),
    except the front shirt: the store packshot is a model cropped at the nose and mid-thigh, so at the
    brief's 607/374 both cuts float inside the image as hard edges. At height 700 / cy 352 the two cuts
    land on the image's top and bottom edge rows and fade into Tap Shoe / Major Brown (logged in brief)."""
    c.compose_cluster([
        {"file": "habit-mens-wj657-cedar-branch-insulated-waterproof-bomber--51265344733466",
         "height": 569, "cx": 378, "cy": 345, "angle": 8, "darken": 0.8},
        {"file": "mens-performance-fleece-hoodie--45600303677722",
         "height": 506, "cx": 832, "cy": 336, "angle": -8, "darken": 0.8},
        {"file": "men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt--32728036802611",
         "height": 700, "cx": 600, "cy": 352, "angle": 0},
    ], "e19-cluster-stain-odor-reset.jpg", size=(1200, 720))


# ---------------------------------------------------------------- round 2 (art-direction-r2.md), outputs r2-01-* / r2-02-*
#
# The v0.4 functions of compose.py save to `ASSETS / out`. Passing an ABSOLUTE path as `out` makes
# pathlib return that path, so they write into this batch's assets/ while the texture tiles are still
# read from the kit (tex_path uses ASSETS). compose.py itself is never edited.

import numpy as np  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402


def out_r2(name):
    return str(BATCH_ASSETS / name)


def cut_model(file, top, bottom, seed=7):
    """Store packshot worn by a model (face at the top, jeans/hands at the bottom): keep the garment
    rows top..bottom (fractions of the trimmed height) and tear both cuts like a clipped catalog page,
    so the cut reads as collage, not as a hard crop."""
    im = c.load_packshot(file)
    h = im.height
    im = im.crop((0, round(h * top), im.width, round(h * bottom)))
    a = im.getchannel("A")
    for i, side in enumerate(("top", "bottom")):
        a = ImageChops.multiply(a, c.torn_mask(im.size, side, depth=34, amp=10, seed=seed + i))
    im.putalpha(a)
    m = im.getchannel("A").point(lambda v: 255 if v > 8 else 0)
    return im.crop(m.getbbox())


def pile_png(items, out, size=(1200, 900), limit=150 * 1024):
    """Products with weight, as ONE transparent PNG laid over the band texture of its <td> (any
    texture, light or dark mode, no seam). items back to front: {"img" or "file", "height", "cx",
    "cy", "angle", "darken"}; cx beyond 0..width = the product bleeds off the email edge."""
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    for it in items:
        im = it["img"] if "img" in it else c.load_packshot(it["file"])
        im = c.fit(im, h=it["height"])
        if it.get("darken"):
            im = c.darken(im, it["darken"])
        c.place(canvas, im, it["cx"], it["cy"], it.get("angle", 0), shadow=it.get("shadow", (8, 22, 26, 0.5)))
    p = BATCH_ASSETS / out
    for colors in (256, 224, 192, 160, 128):
        q = canvas.quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
        q.save(p, optimize=True)
        if p.stat().st_size <= limit:
            break
    print(f"  {p.name:42s} {size[0]}x{size[1]}  {p.stat().st_size / 1024:5.1f} KB  ({colors} colors)")
    return p


def collage_on(band, out, photos, size=(1200, 900), dm_band=None, limit=150 * 1024):
    """Torn, framed photos overlapping on the band texture (tile rows from 0: the image OPENS its
    <td>, like E26). photos back to front: {"img", "width", "cx", "cy", "angle", "sides", "frame_color"}."""
    variants = [("", band)] + ([("-dm", dm_band)] if dm_band else [])
    paths = []
    for suffix, bname in variants:
        canvas = c.to_image(c.tile_rows(bname, size[1]))
        for i, ph in enumerate(photos):
            fr = c.framed_photo_multi(ph["img"], ph["width"], frame=ph.get("frame", 14), sides=ph.get("sides", ("bottom",)),
                                      frame_color=ph.get("frame_color", c.FRAME), seed=ph.get("seed", 140 + i * 7))
            c.place(canvas, fr, ph["cx"], ph["cy"], ph.get("angle", 0), shadow=(8, 20, 24, 0.55))
        p = c.save_jpg_under(canvas, BATCH_ASSETS / out.replace(".jpg", f"{suffix}.jpg"), limit, q=74, floor=56)
        print(f"  {p.name:42s} {size[0]}x{size[1]}  {p.stat().st_size / 1024:5.1f} KB  on {bname}")
        paths.append(p)
    return paths


def dusk_sky(photo, sky_h, stops, blend=150, seed=301):
    """Generated calm area ABOVE a photo whose subjects touch its top edge: an evening sky graded
    through `stops` [(row, hex), ...] with grain and a soft horizon glow; the photo's own top rows
    (tree bokeh) fade up into it over `blend` rows. Returns one tall RGB image for
    compose_full_bleed_hero (photo_y=0)."""
    ph = np.asarray(photo.convert("RGB"), np.float32)
    W = ph.shape[1]
    H = sky_h + ph.shape[0]
    rows = np.arange(H, dtype=np.float32)
    xs = [r for r, _ in stops]
    cols = np.array([c.rgb(h) for _, h in stops], np.float32)
    sky = np.stack([np.interp(rows, xs, cols[:, k]) for k in range(3)], 1)[:, None, :]
    sky = np.broadcast_to(sky, (H, W, 3)).copy()
    sky += (c.periodic_noise(W, H, 60, 30, seed) * 3.0 + c.periodic_noise(W, H, 0.8, 0.8, seed + 1) * 2.4)[:, :, None]
    out = sky.copy()
    t = c.smooth(np.clip((rows[sky_h - blend:] - (sky_h - blend)) / (blend * 1.6), 0, 1))[:, None, None]
    y0 = sky_h - blend
    # blend zone: the photo's top rows (above every head) averaged and blurred sideways into a soft
    # tree-line glow, so the bokeh dissolves into the sky with no mirrored shapes
    from PIL import ImageFilter
    band = np.broadcast_to(ph[2:16].mean(0), (blend, W, 3)).copy()
    band = np.asarray(Image.fromarray(np.clip(band, 0, 255).astype(np.uint8)).filter(ImageFilter.BoxBlur(40))
                      .filter(ImageFilter.GaussianBlur(24)), np.float32)
    ext = np.concatenate([band, ph], 0)
    out[y0:] = sky[y0:] * (1 - t) + ext[: H - y0] * t
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def cross_pile(top_tex, bottom_tex, items, out, size=(1200, 900), seam=150, limit=150 * 1024, seed=41):
    """Products thrown across a torn band border (E21 with several products, over textures): upper
    part = LAST rows of the upper band tile, torn line at `seam`, lower part = LAST rows of the lower
    band tile (the next <td> starts its background at row 0 and continues it)."""
    W, H = size
    up = c.tile_rows(top_tex, H, end=True)
    lo = c.tile_rows(bottom_tex, H, end=True)
    ys = c.torn_line(W, seam, amp=9, seed=seed)
    from PIL import ImageDraw, ImageFilter
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([(0, H)] + [(x, y) for x, y in enumerate(ys)] + [(W, H)], fill=255)
    a = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[:, :, None] / 255
    up = up.copy()
    c.tear_shadow(up, ys)
    canvas = c.to_image(up * (1 - a) + lo * a)
    for it in items:
        im = it["img"] if "img" in it else c.load_packshot(it["file"])
        im = c.fit(im, h=it["height"])
        if it.get("darken"):
            im = c.darken(im, it["darken"])
        c.place(canvas, im, it["cx"], it["cy"], it.get("angle", 0), shadow=it.get("shadow", (10, 24, 28, 0.6)))
    p = c.save_jpg_under(canvas, BATCH_ASSETS / out, limit, q=76, floor=56)
    print(f"  {p.name:42s} {W}x{H}  {p.stat().st_size / 1024:5.1f} KB  {top_tex} / {bottom_tex}")
    return p


def job_r2_01():
    """01 Memorial Day r2: full-bleed camp-chairs hero (dusk fog, tears into Patriot water), torn UTV
    photo on Patriot water, product fan on light paper (transparent)."""
    fam = c.lifestyle("crop-sent-sep15-camp-chairs-family.jpg")
    # QA r2: the photo must run into the torn edge (no flat Tap Shoe strip before the tear), so it is
    # scaled to 1500 (643 rows: 880 + 643 > tear at 1500) and cropped to 1200 keeping the woman on the left
    fam = c.fit(fam, w=1500).crop((60, 0, 1260, round(514 * 1500 / 1200)))
    # evening over the field: Patriot-dark top (logo + headline), warming to an amber glow at the tree line
    tall = dusk_sky(fam, 880, blend=230, stops=[(0, "#1B2034"), (420, "#2A2C3E"), (660, "#4A3B40"), (800, "#7A5540"), (880, "#A87445")])
    c.compose_full_bleed_hero(tall, out_r2("r2-01-hero-camp.jpg"), size=(1200, 1560), photo_w=1200, photo_y=0,
                              top_shade=(0, 0), fade=(1600, 1601), tear_y=1500,
                              next_tex="grain-patriot", grain_sd=2.2,
                              text_boxes={"desktop": (100, 150, 1100, 780), "mobile": (190, 120, 1010, 800),
                                          "headline": (100, 250, 1100, 560)},
                              seed=201)
    utv = c.lifestyle("crop-sent-sep10-utv-hunters.jpg")
    collage_on("grain-patriot", "r2-01-torn-utv.jpg", [
        {"img": utv, "width": 1060, "cx": 610, "cy": 330, "angle": -1.8, "sides": ("bottom", "right"),
         "frame_color": "#F4F1ED"},
    ], size=(1200, 660))
    jacket = cut_model("men-s-roaring-springs-packable-rain-jacket--39299390472243", 0.095, 0.86, seed=11)
    pile_png([
        {"file": "mlf-1-4-zip-camo-performance-layer--47952634413338", "height": 640, "cx": 190, "cy": 380, "angle": 9, "darken": 0.9},
        {"img": jacket, "height": 600, "cx": 1010, "cy": 380, "angle": -8, "darken": 0.9},
        {"file": "mens-flushing-bay-short-sleeve-river-shirt--49918052925722", "height": 600, "cx": 600, "cy": 450, "angle": -2},
    ], "r2-01-fan-weekend.png", size=(1200, 820))


def job_r2_02():
    """02 Stain & Odor r2: barn hero rebuilt on heavy Major Brown grain (tears into Tap Shoe paper),
    torn stable + hay-bale collage on Tap Shoe paper, products thrown in a pile (transparent)."""
    barn = c.lifestyle("crop-sent-sep24-barn-door-feed-bag.jpg")
    c.compose_full_bleed_hero(barn, out_r2("r2-02-hero-barn.jpg"), size=(1200, 1560), photo_w=1200, photo_y=190,
                              photo_rows=(0, 740), extend_top="stretch", top_shade=(300, 0.5), fade=(660, 920),
                              base="grain-brown", tear_y=1500, next_tex="paper-tapshoe", grain_sd=4.2,
                              text_boxes={"logo": (440, 50, 760, 130), "desktop": (100, 820, 1100, 1430),
                                          "mobile": (170, 770, 1030, 1430)}, seed=205)
    stable = c.lifestyle("crop-sent-sep24-stable-horse.jpg")
    hay = c.lifestyle("crop-sent-sep24-hay-bale-seated.jpg")
    collage_on("paper-tapshoe", "r2-02-collage-stable.jpg", [
        {"img": stable, "width": 820, "cx": 460, "cy": 360, "angle": -2.4, "sides": ("bottom", "left"),
         "frame_color": "#E2DDD9"},
        {"img": hay, "width": 360, "cx": 925, "cy": 420, "angle": 3.8, "sides": ("top",), "frame_color": "#F4F1ED"},
    ], size=(1200, 780))
    shirt = cut_model("men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt--32728036802611", 0.12, 0.86, seed=21)
    # thrown down like work clothes at the end of the day, across the tear from Tap Shoe paper into
    # Major Brown grain; the bomber sleeve and the hoodie hem run off the email edges
    cross_pile("paper-tapshoe", "grain-brown", [
        {"file": "habit-mens-wj657-cedar-branch-insulated-waterproof-bomber--51265344733466", "height": 620,
         "cx": 290, "cy": 440, "angle": 24},
        {"file": "mens-performance-fleece-hoodie--45600303677722", "height": 600, "cx": 955, "cy": 455, "angle": -19},
        {"img": shirt, "height": 650, "cx": 615, "cy": 510, "angle": -9},
    ], "r2-02-pile-reset.jpg", size=(1200, 880), seam=170, seed=43)


if __name__ == "__main__":
    import sys as _s
    jobs = {"a1": job_a1, "a2": job_a2, "a3": job_a3, "r2_01": job_r2_01, "r2_02": job_r2_02}
    for k in (_s.argv[1:] or ["a1", "a2", "a3"]):
        print(k); jobs[k]()
