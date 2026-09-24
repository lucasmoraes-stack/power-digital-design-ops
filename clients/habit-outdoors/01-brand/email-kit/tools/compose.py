"""compose.py - Habit Outdoors email kit: pre-built image compositions and textures (kit v0.3 + v0.4).

Why this exists
---------------
Overlap, fan, bleed, collage and band-crossing cannot be done with CSS in email
(no position, no reliable negative margin in Outlook). Each one is built here as
ONE image, with the band colors baked into its edges, so it sits seamlessly
between live-text rows in the HTML. Text never goes inside these images.

Run (from the project root or anywhere):
    python clients/habit-outdoors/01-brand/email-kit/tools/compose.py            # rebuild every v0.3 sample
    python .../compose.py --only e19 e21                                          # rebuild some
    python .../compose.py --list                                                  # show what each job makes
    python .../compose.py --only textures04 edges04 e24 e26                       # v0.4: textures first, the rest bakes them in

To regenerate with other products: edit the SAMPLES block below (packshot file
names = the product handle in 01-brand/photos/products, fetched with
email-ops/tools/fetch_shopify_catalog.py) and run again. Every job prints the
output size and a seam check (edge rows vs. the band color they must match).

Rules baked in (email-ops/rules.md + kit README):
  - 2x resolution (1200px wide for full-width images), JPG q72 4:4:4 when no
    transparency is needed, each file < 150KB; packshot PNGs quantized < 80KB.
  - Edge rows of every JPG are the exact band hex, so the <td bgcolor> above and
    below continues the image with no visible seam.
  - Only Habit palette colors: Tap Shoe #2A2B2D, Major Brown #483F39,
    light warm #E2DDD9, dark-mode band #34353A.

Inputs: packshots in 01-brand/photos/products (transparent 1200x1200 PNG, out
of git), photo crops from the sent emails in email-kit/references, the Aluminum
topographic texture in email-kit/assets/texture-light.jpg (guide p.24).
Needs Pillow and numpy.
"""
from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

KIT = Path(__file__).resolve().parents[1]           # .../01-brand/email-kit
ASSETS = KIT / "assets"
REFS = KIT / "references"
PRODUCTS = KIT.parent / "photos" / "products"

TAPSHOE = "#2A2B2D"
BROWN = "#483F39"
LIGHT = "#E2DDD9"
DM_BAND = "#34353A"          # dark-mode swap of the light warm band (kit dark palette)
FRAME = "#E2DDD9"            # thin light photo frame (the kit's light warm)

JPG_Q = 72
MAX_JPG = 150 * 1024
MAX_PACK = 80 * 1024


# ---------------------------------------------------------------- basics

def rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def load_packshot(name: str) -> Image.Image:
    """Open a store packshot (file name = handle, optional -N suffix) and trim it to its opaque bounds."""
    p = PRODUCTS / name
    if not p.suffix:
        p = p.with_suffix(".png")
    im = Image.open(p).convert("RGBA")
    a = im.getchannel("A").point(lambda v: 255 if v > 8 else 0)
    return im.crop(a.getbbox())


def fit(im: Image.Image, w: int | None = None, h: int | None = None) -> Image.Image:
    """Resize keeping ratio to a target width or height (LANCZOS)."""
    if h is not None:
        w = round(im.width * h / im.height)
    else:
        h = round(im.height * w / im.width)
    return im.resize((w, h), Image.LANCZOS)


def darken(im: Image.Image, f: float) -> Image.Image:
    """Multiply RGB by f (keeps alpha). Used to push back-row products behind the front one."""
    r, g, b, a = im.split()
    r, g, b = (c.point(lambda v: int(v * f)) for c in (r, g, b))
    return Image.merge("RGBA", (r, g, b, a))


def place(canvas: Image.Image, im: Image.Image, cx: float, cy: float, angle: float = 0,
          shadow: tuple[int, int, int, float] | None = (0, 18, 22, 0.45)) -> None:
    """Alpha-composite `im` centred at (cx, cy), rotated `angle` degrees (counter-clockwise),
    with a soft drop shadow (dx, dy, blur, opacity) drawn from its own alpha."""
    if angle:
        im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    x, y = round(cx - im.width / 2), round(cy - im.height / 2)
    if shadow:
        dx, dy, blur, op = shadow
        pad = blur * 3
        a = im.getchannel("A")
        sh = Image.new("L", (im.width + pad * 2, im.height + pad * 2), 0)
        sh.paste(a.point(lambda v: int(v * op)), (pad, pad))
        sh = sh.filter(ImageFilter.GaussianBlur(blur))
        black = Image.new("RGBA", sh.size, (0, 0, 0, 255))
        black.putalpha(sh)
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        layer.paste(black, (x - pad + dx, y - pad + dy), black)
        canvas.alpha_composite(layer)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(im, (x, y), im)
    canvas.alpha_composite(layer)


# ---------------------------------------------------------------- surfaces

def grain(size: tuple[int, int], sigma: float, seed: int = 7) -> np.ndarray:
    """Monochrome film grain, zero-mean, in 0-255 units."""
    rng = np.random.default_rng(seed)
    g = rng.normal(0, sigma, (size[1], size[0])).astype(np.float32)
    gi = Image.fromarray(np.clip(g + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    return (np.asarray(gi, np.float32) - 128) * 1.6


def topo_lines(size: tuple[int, int]) -> np.ndarray:
    """0..1 mask of the Habit topographic lines, lifted from assets/texture-light.jpg (guide p.24)
    and mirror-tiled to `size`."""
    src = Image.open(ASSETS / "texture-light.jpg").convert("L")
    g = np.asarray(src, np.float32)
    b = np.asarray(src.filter(ImageFilter.GaussianBlur(6)), np.float32)
    m = np.clip((b - g - 2) / 14, 0, 1)
    tile = np.concatenate([m, m[::-1]], axis=0)
    tile = np.concatenate([tile, tile[:, ::-1]], axis=1)
    reps_y = math.ceil(size[1] / tile.shape[0])
    reps_x = math.ceil(size[0] / tile.shape[1])
    return np.tile(tile, (reps_y, reps_x))[: size[1], : size[0]]


def smooth(t: np.ndarray) -> np.ndarray:
    return t * t * (3 - 2 * t)


def band_surface(size: tuple[int, int], top: str, bottom: str | None = None, *, sigma: float = 5.0,
                 topo: float = 0.0, haze: float = 0.0, seed: int = 7) -> np.ndarray:
    """Float RGB array: vertical gradient top->bottom (eased), optional light haze across the
    middle (atmosphere), grain and topographic lines lightened into the color."""
    w, h = size
    bottom = bottom or top
    t = smooth(np.linspace(0, 1, h, dtype=np.float32))[:, None, None]
    a, b = np.array(rgb(top), np.float32), np.array(rgb(bottom), np.float32)
    arr = np.broadcast_to(a + (b - a) * t, (h, w, 3)).copy()
    if haze:
        yy = np.linspace(-1, 1, h, dtype=np.float32)[:, None]
        xx = np.linspace(-1, 1, w, dtype=np.float32)[None, :]
        glow = np.exp(-((yy / 0.55) ** 2) - ((xx / 1.1) ** 2)) * haze
        arr += glow[:, :, None] * np.array([1.0, 0.95, 0.88], np.float32)
    if topo:
        arr += (topo_lines(size) * topo)[:, :, None]
    if sigma:
        arr += grain(size, sigma, seed)[:, :, None]
    return arr


def flat_edges(arr: np.ndarray, top: str | None, bottom: str | None, flat: int = 24, feather: int = 90) -> np.ndarray:
    """Force the first/last `flat` rows to the exact band hex and blend into it over `feather` rows,
    so the image meets the <td bgcolor> rows above/below with no seam."""
    h = arr.shape[0]
    out = arr.copy()
    ramp = np.ones(h, np.float32)
    if top:
        c = np.array(rgb(top), np.float32)
        wt = np.clip((np.arange(h) - flat) / feather, 0, 1)
        out = out * wt[:, None, None] + c * (1 - wt[:, None, None])
    if bottom:
        c = np.array(rgb(bottom), np.float32)
        wb = np.clip((h - 1 - np.arange(h) - flat) / feather, 0, 1)
        out = out * wb[:, None, None] + c * (1 - wb[:, None, None])
    del ramp
    return out


def to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(np.rint(arr), 0, 255).astype(np.uint8), "RGB").convert("RGBA")


def torn_line(width: int, base: float, amp: float = 7, seed: int = 3) -> list[float]:
    """y of a ripped-paper edge for every x: slow waves + fine jitter (same feel as edge-*.png, E18)."""
    rnd = random.Random(seed)
    ys, v = [], 0.0
    phases = [rnd.random() * 6.28 for _ in range(3)]
    for x in range(width):
        v = v * 0.86 + rnd.uniform(-1.4, 1.4)
        slow = (math.sin(x / 61 + phases[0]) * amp * 0.6 + math.sin(x / 23 + phases[1]) * amp * 0.3
                + math.sin(x / 9 + phases[2]) * amp * 0.12)
        ys.append(base + slow + v)
    return ys


def torn_mask(size: tuple[int, int], side: str, depth: int = 18, amp: float = 6, seed: int = 5) -> Image.Image:
    """L mask 255 = keep, with a deckled/torn edge `depth` px deep on one side ('top', 'bottom', 'left', 'right')."""
    w, h = size
    m = Image.new("L", size, 255)
    d = ImageDraw.Draw(m)
    if side in ("top", "bottom"):
        ys = torn_line(w, depth / 2, amp, seed)
        if side == "top":
            d.polygon([(0, 0)] + [(x, y) for x, y in enumerate(ys)] + [(w, 0)], fill=0)
        else:
            d.polygon([(0, h)] + [(x, h - y) for x, y in enumerate(ys)] + [(w, h)], fill=0)
    else:
        xs = torn_line(h, depth / 2, amp, seed)
        if side == "left":
            d.polygon([(0, 0)] + [(x, y) for y, x in enumerate(xs)] + [(0, h)], fill=0)
        else:
            d.polygon([(w, 0)] + [(w - x, y) for y, x in enumerate(xs)] + [(w, h)], fill=0)
    return m.filter(ImageFilter.GaussianBlur(0.7))


def framed_photo(img: Image.Image, width: int, frame: int = 10, deckle: str | None = None, seed: int = 5) -> Image.Image:
    """Photo resized to `width`, inside a thin light frame (#E2DDD9), optional torn edge on one side
    (the tear cuts through frame and photo, like a ripped print)."""
    img = fit(img.convert("RGB"), w=width - frame * 2)
    out = Image.new("RGBA", (img.width + frame * 2, img.height + frame * 2), rgb(FRAME) + (255,))
    out.paste(img, (frame, frame))
    if deckle:
        m = torn_mask(out.size, deckle, depth=frame * 3, amp=frame * 0.9, seed=seed)
        out.putalpha(m)
        # paper fibre: a thin light rim along the tear
        rim = m.filter(ImageFilter.MaxFilter(1)).point(lambda v: 255 if 40 < v < 250 else 0)
        light = Image.new("RGBA", out.size, (244, 241, 237, 255))
        out.paste(light, (0, 0), rim)
    return out


# ---------------------------------------------------------------- saving + checks

BAND_HEXES = (TAPSHOE, BROWN, LIGHT, DM_BAND)


def save_jpg(im: Image.Image, name: str, limit: int = MAX_JPG, match=BAND_HEXES) -> Path:
    """JPG 4:4:4 under `limit`, with the band colors decoding exactly.
    A flat color decodes 1-3 levels off at some qualities (e.g. #E2DDD9 at q72, #2A2B2D at q65),
    which shows as a faint box against the <td bgcolor>. So: try qualities near q72 and keep the
    first one that is under `limit` and exact on every band hex present; if none is exact, take the
    best one and run a correction pass that nudges the flat pixels by the measured decode error."""
    p = ASSETS / name
    src = np.asarray(im.convert("RGB"), np.int16)
    masks = []
    rows = np.arange(src.shape[0])[:, None]
    for h in match:
        c = np.array(rgb(h), np.int16)
        eq = np.all(src == c, axis=2)
        top, bot = eq & (rows < 16), eq & (rows >= src.shape[0] - 16)
        masks += [(top, c), (bot, c), (eq & ~top & ~bot, c)]      # edge strips corrected on their own
    masks = [(m, c) for m, c in masks if m.sum() > 500]

    def score(dec):
        return sum(int(np.abs(np.median(dec[m], axis=0) - c).sum()) for m, c in masks)

    def enc(arr, q):
        Image.fromarray(arr.astype(np.uint8), "RGB").save(p, "JPEG", quality=q, subsampling=0,
                                                          optimize=True, progressive=True)
        return p.stat().st_size, score(np.asarray(Image.open(p).convert("RGB"), np.int16))

    tried = []
    for q in (JPG_Q, 74, 70, 68, 76, 66, 65, 62):
        size, sc = enc(src, q)
        if size <= limit:
            tried.append((sc, -q))
            if sc == 0:
                return p
    if not tried:
        return p                                              # over limit even at q62: report flags it
    q = -min(tried)[1]
    enc(src, q)
    if not masks:
        return p

    work = src.copy()
    best_bytes, best = p.read_bytes(), score(np.asarray(Image.open(p).convert("RGB"), np.int16))
    for _ in range(6):
        if best == 0:
            break
        dec = np.asarray(Image.open(p).convert("RGB"), np.int16)
        for m, c in masks:
            err = np.median(dec[m], axis=0).astype(np.int16) - c
            work[m] = np.clip(work[m] - err, 0, 255)
        Image.fromarray(work.astype(np.uint8), "RGB").save(p, "JPEG", quality=q, subsampling=0,
                                                           optimize=True, progressive=True)
        s = score(np.asarray(Image.open(p).convert("RGB"), np.int16))
        if s < best:
            best, best_bytes = s, p.read_bytes()
    p.write_bytes(best_bytes)
    return p


def save_png_quant(im: Image.Image, name: str, limit: int = MAX_PACK) -> Path:
    """Quantized RGBA PNG (keeps soft alpha edges and shadows). Drops colors until under `limit`."""
    p = ASSETS / name
    for colors in (256, 192, 128, 96, 64):
        q = im.quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
        q.save(p, optimize=True)
        if p.stat().st_size <= limit:
            break
    return p


def seam_report(p: Path, top: str | None, bottom: str | None) -> str:
    """Median and max deviation of the first/last 2 rows from the band hex they must continue."""
    im = np.asarray(Image.open(p).convert("RGB"), np.int16)
    out = []
    for label, row, hexc in (("top", im[0:2], top), ("bottom", im[-2:], bottom)):
        if hexc:
            diff = np.abs(row - np.array(rgb(hexc), np.int16)).reshape(-1, 3)
            med = int(np.median(diff, axis=0).max())
            out.append(f"{label} vs {hexc}: median dev {med}, max {int(diff.max())}")
    return "; ".join(out)


def report(p: Path, top: str | None = None, bottom: str | None = None, limit: int = MAX_JPG) -> None:
    kb = p.stat().st_size / 1024
    flag = "" if p.stat().st_size <= limit else "  OVER LIMIT"
    w, h = Image.open(p).size
    s = seam_report(p, top, bottom) if (top or bottom) else ""
    print(f"  {p.name:42s} {w}x{h:<5d} {kb:6.1f} KB{flag}  {s}")


# ---------------------------------------------------------------- compositions

def make_textures() -> None:
    """Two dark surfaces, also usable alone as <td background> with a solid bgcolor fallback:
       tex-tapshoe-grain.jpg   Tap Shoe + subtle grain + topo lines   fallback #2A2B2D
       grad-tapshoe-brown.jpg  Tap Shoe -> Major Brown, haze + grain   fallback #2A2B2D (top) / #483F39 (bottom)"""
    size = (1200, 1200)
    p = save_jpg(to_image(band_surface(size, TAPSHOE, sigma=3.2, topo=11, seed=11)), "tex-tapshoe-grain.jpg")
    report(p)
    arr = band_surface(size, TAPSHOE, BROWN, sigma=3.6, haze=14, topo=5, seed=12)
    p = save_jpg(to_image(flat_edges(arr, TAPSHOE, BROWN, flat=16, feather=120)), "grad-tapshoe-brown.jpg")
    report(p, TAPSHOE, BROWN)


def compose_cluster(items: list[dict], out: str, size=(1200, 900), top=TAPSHOE, bottom=BROWN,
                    photo: dict | None = None) -> Path:
    """E19 Product Cluster. Packshots in a fan over the grainy Tap Shoe -> Major Brown gradient
    (or over a photo that fades into it, if `photo` = {"src": Image, "height": px}).
    items: back to front, each {"file", "height", "cx", "cy", "angle", "darken"}.
    Edge rows = `top` / `bottom` hex, so the headline row above (bgcolor top) and the body row
    below (bgcolor bottom) continue it."""
    arr = band_surface(size, top, bottom, sigma=2.4, haze=16, topo=6, seed=21)
    canvas = to_image(arr)
    if photo:
        ph = fit(photo["src"].convert("RGB"), w=size[0]).crop((0, 0, size[0], photo["height"])).convert("RGBA")
        fade = np.clip(1 - (np.arange(ph.height) - ph.height * 0.45) / (ph.height * 0.55), 0, 1)
        a = Image.fromarray((np.tile(smooth(fade)[:, None], (1, ph.width)) * 255).astype(np.uint8))
        ph.putalpha(a)
        canvas.alpha_composite(ph)
    for it in items:
        im = fit(load_packshot(it["file"]), h=it["height"])
        if it.get("darken"):
            im = darken(im, it["darken"])
        place(canvas, im, it["cx"], it["cy"], it.get("angle", 0), shadow=(0, 20, 26, 0.55))
    arr = flat_edges(np.asarray(canvas.convert("RGB"), np.float32), top, bottom, flat=20, feather=70)
    p = save_jpg(to_image(arr), out)
    report(p, top, bottom)
    return p


def compose_tech_bleed(file: str, out: str, width: int = 480, visible: float = 0.65, band=LIGHT,
                       dm_band=DM_BAND, pad_y: int = 40) -> list[Path]:
    """E20 Technology Bleed. Packshot cut by the RIGHT edge of the image; the HTML cell touches the
    right edge of the email, so the product bleeds off the email. `visible` = share of the product
    width left in frame. Baked on the band color (left, top and bottom edge rows = band hex) and
    written twice: `out` on the light warm band and `-dm` on the dark-mode band #34353A (swap with
    img-light/img-dark). A transparent PNG of a camo packshot at this size cannot get under 150KB."""
    im = fit(load_packshot(file), w=round(width / visible))
    h = im.height + pad_y * 2
    paths = []
    for color, name in ((band, out), (dm_band, out.replace(".jpg", "-dm.jpg"))):
        if color is None:
            continue
        canvas = Image.new("RGBA", (width, h), rgb(color) + (255,))
        place(canvas, im, im.width / 2 + 10, h / 2 - 6, 0, shadow=(0, 14, 18, 0.35))
        arr = flat_edges(np.asarray(canvas.convert("RGB"), np.float32), color, color, flat=4, feather=1)
        arr[:, :4] = np.array(rgb(color), np.float32)          # left edge rows too
        p = save_jpg(to_image(arr), name)
        report(p, color, color)
        paths.append(p)
    return paths


def compose_band_cross(file: str, out: str, top=TAPSHOE, bottom=LIGHT, dm_bottom=DM_BAND, size=(1200, 700),
                       seam: int = 400, product_h: int = 620, cx: int = 330, cy: int | None = None,
                       angle: float = -4) -> list[Path]:
    """E21 Band-Crossing Product. One image holding both band colors, a torn edge between them and the
    packshot over the seam (Habit Sep 2 pattern). Writes `out` and, when the lower band is light,
    an `-dm` twin whose lower color is the dark-mode band #34353A (swap with img-light/img-dark,
    same as E18)."""
    paths = []
    im = fit(load_packshot(file), h=product_h)
    ys = torn_line(size[0], seam, amp=8, seed=9)
    for low, name in ((bottom, out), (dm_bottom, out.replace(".jpg", "-dm.jpg"))):
        if low is None:
            continue
        canvas = Image.new("RGBA", size, rgb(top) + (255,))
        lower = Image.new("RGBA", size, rgb(low) + (255,))
        m = Image.new("L", size, 0)
        ImageDraw.Draw(m).polygon([(0, size[1])] + [(x, y) for x, y in enumerate(ys)] + [(size[0], size[1])], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(0.8))
        canvas.paste(lower, (0, 0), m)
        # a few paper specks along the tear, as in edge-*.png
        rnd, d = random.Random(4), ImageDraw.Draw(canvas)
        for _ in range(26):
            x = rnd.randrange(size[0])
            y = ys[x] - rnd.uniform(3, 9)
            r = rnd.choice((1.2, 1.6, 2.2))
            d.ellipse((x - r, y - r, x + r, y + r), fill=rgb(low))
        place(canvas, im, cx, cy or seam - 20, angle, shadow=(6, 22, 24, 0.5))
        arr = flat_edges(np.asarray(canvas.convert("RGB"), np.float32), top, low, flat=6, feather=1)
        p = save_jpg(to_image(arr), name)
        report(p, top, low)
        paths.append(p)
    return paths


def compose_collage(photos: list[dict], out: str, size=(1200, 960), color=TAPSHOE) -> Path:
    """E22 Photo Collage. Framed photos, slightly off-axis, overlapping, one or more with a torn edge,
    on the grainy Tap Shoe topo surface (same recipe as tex-tapshoe-grain.jpg), whose grain fades
    to flat Tap Shoe at the top and bottom edges so live-text rows in #2A2B2D continue it.
    photos: back to front, each {"img": Image, "width", "cx", "cy", "angle", "deckle": side|None}."""
    canvas = to_image(band_surface(size, color, sigma=3.2, topo=11, seed=31))
    for i, ph in enumerate(photos):
        fr = framed_photo(ph["img"], ph["width"], frame=10, deckle=ph.get("deckle"), seed=40 + i)
        place(canvas, fr, ph["cx"], ph["cy"], ph.get("angle", 0), shadow=(4, 16, 18, 0.55))
    arr = flat_edges(np.asarray(canvas.convert("RGB"), np.float32), color, color, flat=18, feather=80)
    p = save_jpg(to_image(arr), out)
    report(p, color, color)
    return p


def product_png(file: str, px: int, out: str, pad: float = 0.03, limit: int = MAX_PACK) -> Path:
    """Square transparent packshot for the product modules (E04, E07, E17, E23): trimmed,
    centred in px x px with `pad` margin, quantized under `limit`."""
    im = load_packshot(file)
    inner = round(px * (1 - pad * 2))
    im = fit(im, h=inner) if im.height >= im.width else fit(im, w=inner)
    canvas = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    canvas.alpha_composite(im, ((px - im.width) // 2, (px - im.height) // 2))
    p = save_png_quant(canvas, out, limit=limit)
    report(p, limit=limit)
    return p


def swatch(file: str) -> str:
    """Color dot for a variant: median RGB of the opaque pixels of its packshot, as hex."""
    im = np.asarray(Image.open(PRODUCTS / file).convert("RGBA"))
    px = im[im[:, :, 3] > 200][:, :3]
    return "#%02X%02X%02X" % tuple(int(v) for v in np.median(px, axis=0))


def ref_crop(ref: str, box: tuple[int, int, int, int]) -> Image.Image:
    """Photo crop from a sent-email print in references/ (1200px = 2x). Stand-in until the
    original is in the approved photo bank."""
    return Image.open(REFS / ref).convert("RGB").crop(box)


def pack_photo(file: str, box: tuple[int, int, int, int]) -> Image.Image:
    """Crop from a full-frame store image (detail close-up), flattened on the light warm color."""
    im = Image.open(PRODUCTS / file).convert("RGBA")
    bg = Image.new("RGBA", im.size, rgb(LIGHT) + (255,))
    bg.alpha_composite(im)
    return bg.convert("RGB").crop(box)


# ---------------------------------------------------------------- v0.4: texture set, full-bleed hero, torn photo, textured edges
#
# Tiles are 1200x1600 and PERIODIC top/bottom (and left/right): every noise field is built in the
# Fourier domain, so row 1599 continues into row 0. A band of any height can repeat the tile
# (CSS background-repeat: repeat-y, background-size: 600px auto). Gradients are not tiles: they are
# stretched to the band (background-size: 100% 100%, VML type="frame"), see TEXTURES below.

PATRIOT = "#202944"
IVY = "#595442"
ALUMINUM = "#A39A8C"
PHOTOS = KIT.parent / "photos" / "lifestyle"
TEX_W, TEX_H = 1200, 1600
MAX_TEX = 90 * 1024

# name: (file, fallback bgcolor, kind, text on it). kind "tile" = seamless repeat-y, "stretch" = gradient.
TEXTURES = {
    "paper-light":    ("tex-paper-light.jpg",         LIGHT,   "tile",    "#2A2B2D titles/body, #5C5249 labels"),
    "paper-light-dm": ("tex-paper-light-dm.jpg",      DM_BAND, "tile",    "dark-mode swap of paper-light (Apple Mail / iOS)"),
    "paper-tapshoe":  ("tex-paper-tapshoe.jpg",       TAPSHOE, "tile",    "white, #E2DDD9 body, orange text OK"),
    "grain-brown":    ("tex-grain-brown.jpg",         BROWN,   "tile",    "white, #E2DDD9 body, orange only large"),
    "grain-patriot":  ("tex-grain-patriot-water.jpg", PATRIOT, "tile",    "white, #E2DDD9 body, orange text OK"),
    "grain-ivy":      ("tex-grain-ivy.jpg",           IVY,     "tile",    "white only, no orange text"),
    "camo-blur":      ("tex-camo-blur.jpg",           BROWN,   "tile",    "white only, no orange text"),
    "topo-tapshoe":   ("tex-topo-tapshoe.jpg",        TAPSHOE, "tile",    "white, #E2DDD9 body, orange text OK"),
    "grad-tapshoe-brown":   ("grad-tapshoe-to-brown.jpg",   TAPSHOE, "stretch", "white; fallback = top color"),
    "grad-patriot-tapshoe": ("grad-patriot-to-tapshoe.jpg", PATRIOT, "stretch", "white; fallback = top color"),
    "grad-paper-aluminum":  ("grad-paper-to-aluminum.jpg",  LIGHT,   "stretch", "#2A2B2D only (#5C5249 fails on Aluminum)"),
}


def periodic_noise(w: int, h: int, lx: float, ly: float, seed: int) -> np.ndarray:
    """Zero-mean, unit-std noise, Gaussian-correlated over lx x ly px, periodic in both axes (FFT)."""
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (h, w)).astype(np.float32)
    fy = np.fft.fftfreq(h)[:, None]
    fx = np.fft.rfftfreq(w)[None, :]
    g = np.exp(-2 * np.pi ** 2 * ((fx * lx) ** 2 + (fy * ly) ** 2))
    out = np.fft.irfft2(np.fft.rfft2(n) * g, s=(h, w)).astype(np.float32)
    return out / (out.std() + 1e-6)


def periodic_blur(arr: np.ndarray, sigma: float) -> np.ndarray:
    """Gaussian blur that wraps around (keeps a tile seamless). arr: HxW or HxWx3."""
    h, w = arr.shape[:2]
    fy = np.fft.fftfreq(h)[:, None]
    fx = np.fft.rfftfreq(w)[None, :]
    g = np.exp(-2 * np.pi ** 2 * sigma ** 2 * (fx ** 2 + fy ** 2))
    if arr.ndim == 2:
        return np.fft.irfft2(np.fft.rfft2(arr) * g, s=(h, w)).astype(np.float32)
    return np.stack([np.fft.irfft2(np.fft.rfft2(arr[:, :, c]) * g, s=(h, w)) for c in range(3)], 2).astype(np.float32)


def paper_surface(base: str, size=(TEX_W, TEX_H), *, grain_sd: float = 3.0, mottle: float = 2.6,
                  fibre: float = 5.0, fibre_sign: float = 1.0, seed: int = 1) -> np.ndarray:
    """Seamless paper: base hex + soft mottling (low frequency, kept at about 1 level: every <td>
    restarts the tile at row 0, and a larger mottle showed as a straight step on light paper) + sparse fibres/dust + fine grain. fibre_sign +1 lighter specks (dark
    paper), -1 darker fibres (light paper)."""
    w, h = size
    arr = np.broadcast_to(np.array(rgb(base), np.float32), (h, w, 3)).copy()
    m = periodic_noise(w, h, 70, 70, seed) * mottle + periodic_noise(w, h, 16, 16, seed + 1) * mottle * 0.45
    f1 = periodic_noise(w, h, 11, 1.1, seed + 2)
    f2 = periodic_noise(w, h, 1.1, 11, seed + 3)
    fib = (np.clip(np.abs(f1) - 2.5, 0, None) + np.clip(np.abs(f2) - 2.6, 0, None)) * fibre * fibre_sign
    g = periodic_noise(w, h, 0.75, 0.75, seed + 4) * grain_sd
    arr += (m + fib + g)[:, :, None]
    return arr


def water_surface(base: str, size=(TEX_W, TEX_H), seed: int = 51) -> np.ndarray:
    """Patriot Blue with a subtle water feel: horizontal ripple streaks bent by a slow wave field
    (sampled with wrap-around, so still seamless), large soft light patches (the cloudy navy of the
    Sep 22 email) and grain."""
    w, h = size
    arr = np.broadcast_to(np.array(rgb(base), np.float32), (h, w, 3)).copy()
    rip = periodic_noise(w, h, 70, 3.0, seed) * 2.2 + periodic_noise(w, h, 30, 1.6, seed + 1) * 1.0
    warp = periodic_noise(w, h, 90, 60, seed + 4) * 7.0
    yy = (np.arange(h)[:, None] + np.rint(warp).astype(int)) % h
    xx = np.broadcast_to(np.arange(w)[None, :], (h, w))
    rip = rip[yy, xx]
    patch = np.clip(periodic_noise(w, h, 150, 110, seed + 2), 0, None) * 6.5
    g = periodic_noise(w, h, 0.75, 0.75, seed + 3) * 2.6
    tint = np.array([0.72, 0.88, 1.15], np.float32)                 # lighten toward blue, stay in hue
    arr += (rip + patch)[:, :, None] * tint + g[:, :, None]
    return arr


def topo_tile(size=(TEX_W, TEX_H)) -> np.ndarray:
    """0..1 topo-line mask (guide p.24, from texture-light.jpg), resized to half the tile height and
    mirrored, so the tile repeats with no seam (mirror joints are continuous)."""
    src = Image.open(ASSETS / "texture-light.jpg").convert("L")
    g = np.asarray(src, np.float32)
    b = np.asarray(src.filter(ImageFilter.GaussianBlur(6)), np.float32)
    m = np.clip((b - g - 2) / 14, 0, 1)
    half = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).resize((size[0], size[1] // 2), Image.LANCZOS),
                      np.float32) / 255
    return np.concatenate([half, half[::-1]], axis=0)


def camo_surface(size=(TEX_W, TEX_H), src="habit-mens-cedar-branch-insulated-waterproof-parka-6.png",
                 box=(540, 560, 880, 1040), overlap: int = 160, blur: float = 9.0, desat: float = 0.3,
                 max_lum: float = 0.12, seed: int = 61) -> np.ndarray:
    """Blurred camo from the store packshot fabric (Realtree APX close-up of the Cedar Branch parka,
    a clean area with no logo, hand or printed label): crop, enlarge to the tile width, cross-fade the
    extra `overlap` rows into the top so the tile repeats with no seam (no mirror, no symmetry),
    blur, desaturate a little, then darken until the brightest 1% stays under `max_lum` relative
    luminance (white text >= 6:1 everywhere). Light grain on top."""
    w, h = size
    im = Image.open(PRODUCTS / src).convert("RGB").crop(box).resize((w, h + overlap), Image.LANCZOS)
    a = np.asarray(im, np.float32)
    t = smooth(np.linspace(0, 1, overlap, dtype=np.float32))[:, None, None]
    tile = a[:h].copy()
    tile[:overlap] = a[h:h + overlap] * (1 - t) + a[:overlap] * t      # row 0 continues row h-1
    tile = periodic_blur(tile, blur)
    grey = tile.mean(2, keepdims=True)
    tile = tile * (1 - desat) + grey * desat
    k = 1.0
    for _ in range(40):                                     # scale RGB until the 99th pct meets max_lum
        if lum_stats(np.clip(tile * k, 0, 255))[2] <= max_lum:
            break
        k *= 0.96
    tile = tile * k
    tile += (periodic_noise(w, h, 0.75, 0.75, seed) * 2.4)[:, :, None]
    return tile


def gradient_surface(top: str, bottom: str, size=(TEX_W, TEX_H), haze: float = 10, grain_sd: float = 3.0,
                     seed: int = 71) -> np.ndarray:
    """Atmospheric gradient: eased top->bottom, a soft light haze across the middle, paper grain."""
    arr = band_surface(size, top, bottom, sigma=0, haze=haze, seed=seed)
    w, h = size
    arr += (periodic_noise(w, h, 0.75, 0.75, seed) * grain_sd + periodic_noise(w, h, 70, 70, seed + 1) * 2.0)[:, :, None]
    return arr


def save_jpg_under(im: Image.Image, path: Path, limit: int, q: int = 70, floor: int = 50,
                   subsampling: int = 2) -> Path:
    """JPG at quality q, stepping down until under `limit` bytes (textures and heroes)."""
    im = im.convert("RGB")
    for qq in range(q, floor - 1, -2):
        im.save(path, "JPEG", quality=qq, subsampling=subsampling, optimize=True, progressive=True)
        if path.stat().st_size <= limit:
            break
    return path


def lum_stats(arr: np.ndarray) -> tuple[float, float, float]:
    """(1st, 50th, 99th percentile) WCAG relative luminance of an RGB array."""
    lin = np.clip(np.asarray(arr, np.float32) / 255, 0, 1)
    lin = np.where(lin <= 0.04045, lin / 12.92, ((lin + 0.055) / 1.055) ** 2.4)
    L = 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]
    return tuple(float(np.percentile(L, p)) for p in (1, 50, 99))


def _L(hexc: str) -> float:
    return lum_stats(np.array([[rgb(hexc)]], np.float32))[1]


def contrast(l1: float, l2: float) -> float:
    a, b = max(l1, l2), min(l1, l2)
    return (a + 0.05) / (b + 0.05)


def contrast_report(p: Path, texts: list[str], box: tuple[int, int, int, int] | None = None,
                    blur: float = 3.0) -> str:
    """Worst-case contrast of each text hex against the area where text sits. The area is blurred a
    little first (a glyph covers several px), then the 1st and 99th luminance percentiles are used."""
    im = Image.open(p).convert("RGB")
    if box:
        im = im.crop(box)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    lo, med, hi = lum_stats(np.asarray(im))
    out = []
    for t in texts:
        lt = _L(t)
        out.append(f"{t} {min(contrast(lt, lo), contrast(lt, hi)):.2f}:1")
    return "worst " + ", ".join(out)


def tex_path(name: str) -> Path:
    return ASSETS / TEXTURES[name][0]


def _continues(name: str) -> bool:
    """Rows to use when an image hands over to a <td> with this background: a tile continues from its
    last rows into row 0; a stretched gradient starts with its first rows."""
    return name.startswith("flat:") or TEXTURES[name][2] == "tile"


def load_tile(name: str) -> np.ndarray:
    """Texture tile as float RGB (1200x1600), for baking into compositions."""
    return np.asarray(Image.open(tex_path(name)).convert("RGB"), np.float32)


def tile_rows(name: str, h: int, end: bool = False) -> np.ndarray:
    """h rows of a tile (repeated if needed). end=True returns the LAST h rows, so an image whose
    bottom is this texture continues seamlessly into the next <td> (its background starts at row 0).
    "flat:#RRGGBB" gives a flat color (e.g. the flat Tap Shoe footer)."""
    if name.startswith("flat:"):
        return np.broadcast_to(np.array(rgb(name[5:]), np.float32), (h, TEX_W, 3)).copy()
    t = load_tile(name)
    reps = math.ceil(h / t.shape[0]) + 1
    tt = np.concatenate([t] * reps, axis=0)
    return (tt[-h:] if end else tt[:h]).copy()


def make_texture_set(only: list[str] | None = None) -> None:
    """Every v0.4 texture (1200x1600, JPG q70 or lower until < 90KB), with contrast check of the
    kit text colors against the texture (1st and 99th luminance percentile)."""
    jobs = {
        "paper-light":    lambda: paper_surface(LIGHT, grain_sd=3.0, mottle=1.0, fibre=5, fibre_sign=-1, seed=1),
        "paper-light-dm": lambda: paper_surface(DM_BAND, grain_sd=2.6, mottle=1.0, fibre=4, fibre_sign=1, seed=2),
        "paper-tapshoe":  lambda: paper_surface(TAPSHOE, grain_sd=2.8, mottle=1.2, fibre=5, fibre_sign=1, seed=3),
        "grain-brown":    lambda: paper_surface(BROWN, grain_sd=3.4, mottle=1.3, fibre=6, fibre_sign=1, seed=4),
        "grain-patriot":  lambda: water_surface(PATRIOT),
        "grain-ivy":      lambda: paper_surface(IVY, grain_sd=3.2, mottle=1.3, fibre=5, fibre_sign=1, seed=6),
        "camo-blur":      lambda: camo_surface(),
        "topo-tapshoe":   lambda: paper_surface(TAPSHOE, grain_sd=2.6, mottle=1.0, fibre=4, seed=8) + (topo_tile() * 13)[:, :, None],
        "grad-tapshoe-brown":   lambda: gradient_surface(TAPSHOE, BROWN, haze=12, seed=81),
        "grad-patriot-tapshoe": lambda: gradient_surface(PATRIOT, TAPSHOE, haze=10, seed=82),
        "grad-paper-aluminum":  lambda: gradient_surface(LIGHT, ALUMINUM, haze=6, seed=83),
    }
    texts = {"paper-light": ["#2A2B2D", "#5C5249"], "paper-light-dm": ["#F1EEEB", "#D6D0CA", "#B0A89C"],
             "paper-tapshoe": ["#FFFFFF", "#E2DDD9", "#FF6400"], "grain-brown": ["#FFFFFF", "#E2DDD9", "#FF6400"],
             "grain-patriot": ["#FFFFFF", "#E2DDD9", "#FF6400"], "grain-ivy": ["#FFFFFF", "#E2DDD9"],
             "camo-blur": ["#FFFFFF", "#E2DDD9"], "topo-tapshoe": ["#FFFFFF", "#E2DDD9", "#FF6400"],
             "grad-tapshoe-brown": ["#FFFFFF", "#E2DDD9"], "grad-patriot-tapshoe": ["#FFFFFF", "#E2DDD9"],
             "grad-paper-aluminum": ["#2A2B2D", "#5C5249"]}
    for name, fn in jobs.items():
        if only and name not in only:
            continue
        f, fallback, kind, _ = TEXTURES[name]
        p = save_jpg_under(to_image(fn()), ASSETS / f, MAX_TEX, q=70)
        arr = np.asarray(Image.open(p).convert("RGB"), np.int16)
        seam = float(np.abs(arr[:4].mean(0) - arr[-4:].mean(0)).mean()) if kind == "tile" else -1
        mean = "#%02X%02X%02X" % tuple(int(v) for v in arr.reshape(-1, 3).mean(0))
        print(f"  {f:30s} {p.stat().st_size / 1024:5.1f} KB  fallback {fallback}  mean {mean}  "
              f"{'wrap diff %.1f' % seam if seam >= 0 else 'stretch'}  {contrast_report(p, texts[name], blur=0)}")


# ---- E18 textured torn edge

def tear_shadow(arr: np.ndarray, ys: list[float], y_off: int = 0, depth: float = 5.0, strength: float = 0.28) -> None:
    """In place: soft shadow just ABOVE a torn line (the lower sheet lies over the upper one), so a
    tear stays readable when the two band colors are close (brown over camo, ivy over camo)."""
    h = arr.shape[0]
    yy = np.arange(h, dtype=np.float32)[:, None]
    line = np.array(ys, np.float32)[None, :] + y_off
    d = line - yy                                               # > 0 above the line
    s = np.where(d > 0, np.exp(-d / depth), 0.0) * strength
    arr *= (1 - s)[:, :, None]



def compose_torn_edge_textured(top: str, bottom: str, out: str, h: int = 80, seam: float | None = None,
                               seed: int = 3, dm: dict | None = None) -> list[Path]:
    """E18 torn edge carrying textures: upper part = texture `top`, lower part = texture `bottom`,
    torn line between, paper specks along it. The LAST rows of the bottom tile are used, so the
    edge continues into the next band's <td> (whose background tile starts at row 0). JPG (no
    transparency needed: the upper band's texture is baked too; tile phase of a noise texture does
    not show). dm = {"top": name, "bottom": name} also writes a -dm twin (light paper -> dark paper)."""
    seam = seam if seam is not None else h * 0.45
    variants = [("", top, bottom)]
    if dm:
        variants.append(("-dm", dm.get("top", top), dm.get("bottom", bottom)))
    paths = []
    for suffix, tname, bname in variants:
        up = tile_rows(tname, h, end=True)
        lo = tile_rows(bname, h, end=_continues(bname))
        ys = torn_line(TEX_W, seam, amp=8, seed=seed)
        m = Image.new("L", (TEX_W, h), 0)
        ImageDraw.Draw(m).polygon([(0, h)] + [(x, y) for x, y in enumerate(ys)] + [(TEX_W, h)], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(0.8))
        a = np.asarray(m, np.float32)[:, :, None] / 255
        up = up.copy()
        tear_shadow(up, ys)
        canvas = to_image(up * (1 - a) + lo * a)
        rnd, d = random.Random(seed + 1), ImageDraw.Draw(canvas)
        spot = tuple(int(v) for v in np.median(lo.reshape(-1, 3), 0))
        for _ in range(30):
            x = rnd.randrange(TEX_W)
            y = ys[x] - rnd.uniform(3, 10)
            r = rnd.choice((1.2, 1.6, 2.2))
            d.ellipse((x - r, y - r, x + r, y + r), fill=spot + (255,))
        p = save_jpg_under(canvas, ASSETS / out.replace(".jpg", f"{suffix}.jpg"), 30 * 1024, q=76, subsampling=0)
        print(f"  {p.name:42s} {TEX_W}x{h}  {p.stat().st_size / 1024:5.1f} KB  top {tname} / bottom {bname}")
        paths.append(p)
    return paths


# ---- E24 full-bleed photo hero

def compose_full_bleed_hero(photo: Image.Image, out: str, *, size=(1200, 1560), photo_w: int = 1200,
                            photo_y: int = 0, photo_rows: tuple[int, int] | None = None,
                            extend_top: str | bool = False, top_shade: tuple[int, float] = (0, 0.0),
                            fade: tuple[int, int] = (1200, 1400), fade_strength: float = 1.0,
                            base: str = "paper-tapshoe", tear_y: int = 1500, next_tex: str = "grain-brown",
                            text_boxes: dict | None = None, grain_sd: float = 2.0, limit: int = MAX_JPG,
                            seed: int = 91) -> Path:
    """E24 Full-Bleed Photo Hero: ONE background image for a live-text hero cell (600 wide, file 2x).
       photo        crop from photos/lifestyle, scaled to photo_w (centre-cropped to 1200) at photo_y
       photo_rows   keep only these rows of the scaled photo (e.g. cut the legs off)
       extend_top   "fog" or "stretch": grow a calm area ABOVE the photo from its own top rows, the
                    "gradient strip born from the photo" of art direction #2 (fog = blurred mist,
                    stretch = columns pulled up, reads as siding or trunks)
       top_shade    (height, strength): pull the top toward the base texture, for logo + headline
       fade         (start, end) rows: photo alpha 1 -> 0 over the base texture (Tap Shoe paper), so
                    the bottom of the photo melts into the band color before the tear
       tear_y       torn edge; below it the NEXT band texture (last tile rows: the next <td> continues it)
       text_boxes   {"label": (x0, y0, x1, y1)} in file px, where live text sits: contrast is printed."""
    W, H = size
    canvas = tile_rows(base, H)
    ph = fit(photo.convert("RGB"), w=photo_w)
    if photo_w > W:
        x0 = (photo_w - W) // 2
        ph = ph.crop((x0, 0, x0 + W, ph.height))
    if photo_rows:
        ph = ph.crop((0, photo_rows[0], W, photo_rows[1]))
    pa = np.asarray(ph, np.float32)
    layer = canvas.copy()
    alpha = np.zeros(H, np.float32)
    y1 = min(H, photo_y + pa.shape[0])
    layer[photo_y:y1] = pa[: y1 - photo_y]
    alpha[photo_y:y1] = 1
    if extend_top and photo_y > 0:
        # grow the calm area from the photo's own top rows (above every subject):
        #   "fog"     heavy horizontal blur of those rows, soft bokeh, sharp only in the last `join` rows
        #   "stretch" each column stretched up (reads as siding, trunks, a door frame), lightly blurred
        join = 70
        src = pa[2:14].mean(0)
        sharp = np.broadcast_to(src, (photo_y, W, 3)).copy()
        if extend_top == "stretch":
            far = np.asarray(Image.fromarray(np.clip(sharp, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)),
                             np.float32)
            join = photo_y // 2
        else:
            row = np.asarray(Image.fromarray(np.clip(src[None].repeat(8, 0), 0, 255).astype(np.uint8))
                             .filter(ImageFilter.BoxBlur(60)).filter(ImageFilter.GaussianBlur(40)), np.float32)[4]
            far = np.broadcast_to(row, (photo_y, W, 3)).copy()
            far += (periodic_noise(W, photo_y, 38, 38, seed) * 5 + periodic_noise(W, photo_y, 120, 160, seed + 7) * 5)[:, :, None]
        dist = (photo_y - np.arange(photo_y, dtype=np.float32))[:, None, None]      # rows above the photo
        t = smooth(np.clip(dist / join, 0, 1))
        layer[:photo_y] = sharp * (1 - t) + far * t
        alpha[:photo_y] = 1
    f0, f1 = fade
    ramp = smooth(np.clip((np.arange(H) - f0) / max(1, f1 - f0), 0, 1)) * fade_strength
    alpha = alpha * (1 - ramp)
    a = alpha[:, None, None]
    arr = layer * a + canvas * (1 - a)
    sh, st = top_shade
    if sh:
        s = (1 - smooth(np.clip(np.arange(H) / sh, 0, 1))) * st
        arr = arr * (1 - s[:, None, None]) + canvas * s[:, None, None]
    arr += (periodic_noise(W, H, 0.75, 0.75, seed + 1) * grain_sd)[:, :, None]
    # torn bottom edge: the next band's paper lies over the photo
    lo = tile_rows(next_tex, H - tear_y + 24, end=_continues(next_tex))
    top_rows = H - lo.shape[0]
    ys = torn_line(W, 12, amp=9, seed=seed + 2)
    m = Image.new("L", (W, lo.shape[0]), 0)
    ImageDraw.Draw(m).polygon([(0, lo.shape[0])] + [(x, y) for x, y in enumerate(ys)] + [(W, lo.shape[0])], fill=255)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[:, :, None] / 255
    part = arr[top_rows:].copy()
    tear_shadow(part, ys)
    arr[top_rows:] = part * (1 - m) + lo * m
    img = to_image(arr)
    d, rnd = ImageDraw.Draw(img), random.Random(seed + 3)
    spot = tuple(int(v) for v in np.median(lo.reshape(-1, 3), 0))
    for _ in range(34):
        x = rnd.randrange(W)
        y = top_rows + ys[x] - rnd.uniform(3, 11)
        r = rnd.choice((1.3, 1.8, 2.4))
        d.ellipse((x - r, y - r, x + r, y + r), fill=spot + (255,))
    p = save_jpg_under(img, ASSETS / out, limit, q=72, floor=52, subsampling=2)
    print(f"  {p.name:42s} {W}x{H}  {p.stat().st_size / 1024:5.1f} KB")
    for label, box in (text_boxes or {}).items():
        print(f"      text area {label:14s} {contrast_report(p, ['#FFFFFF', '#E2DDD9'], box)}")
    return p


# ---- E26 torn photo

def framed_photo_multi(img: Image.Image, width: int, frame: int = 12, sides=("bottom",), frame_color: str = FRAME,
                       seed: int = 5) -> Image.Image:
    """Photo in a thin paper frame, torn on 1-2 sides (the tear cuts through frame and photo)."""
    img = fit(img.convert("RGB"), w=width - frame * 2)
    out = Image.new("RGBA", (img.width + frame * 2, img.height + frame * 2), rgb(frame_color) + (255,))
    out.paste(img, (frame, frame))
    m = Image.new("L", out.size, 255)
    for i, side in enumerate(sides):
        m = ImageChops.multiply(m, torn_mask(out.size, side, depth=frame * 3, amp=frame * 0.9, seed=seed + i))
    out.putalpha(m)
    rim = m.point(lambda v: 255 if 40 < v < 250 else 0)
    out.paste(Image.new("RGBA", out.size, (244, 241, 237, 255)), (0, 0), rim)
    return out


def compose_torn_photo(photo: Image.Image, out: str, *, band: str = "grain-brown", size=(1200, 860),
                       photo_w: int = 980, cx: float = 600, cy: float = 430, angle: float = -1.5,
                       sides=("bottom", "right"), frame: int = 12, frame_color: str = FRAME,
                       dm_band: str | None = None, seed: int = 111) -> list[Path]:
    """E26 Torn Photo: framed photo, torn on `sides`, rotated `angle`, soft shadow, baked on the band
    texture (tile rows from 0, the same rows the <td> background shows when the image opens the cell).
    dm_band also writes a -dm twin (for a light paper band, swap with img-light / img-dark)."""
    fr = framed_photo_multi(photo, photo_w, frame=frame, sides=sides, frame_color=frame_color, seed=seed)
    variants = [("", band)] + ([("-dm", dm_band)] if dm_band else [])
    paths = []
    for suffix, bname in variants:
        canvas = to_image(tile_rows(bname, size[1]))
        place(canvas, fr, cx, cy, angle, shadow=(6, 16, 20, 0.5))
        p = save_jpg_under(canvas, ASSETS / out.replace(".jpg", f"{suffix}.jpg"), MAX_JPG, q=74, floor=56, subsampling=2)
        print(f"  {p.name:42s} {size[0]}x{size[1]}  {p.stat().st_size / 1024:5.1f} KB  on {bname}")
        paths.append(p)
    return paths


def lifestyle(name: str) -> Image.Image:
    """Photo from photos/lifestyle (crop-sent-* are stand-ins cropped from the sent emails)."""
    return Image.open(PHOTOS / name).convert("RGB")


# ---------------------------------------------------------------- SAMPLES (edit and rerun)

def job_textures():
    """tex-tapshoe-grain.jpg + grad-tapshoe-brown.jpg (dark grain surface, atmospheric gradient)."""
    make_textures()


def job_e19():
    """E19 Product Cluster: e19-cluster-cedar-branch.jpg (3 Cedar Branch packshots in a fan)."""
    # Men's Cedar Branch Insulated Waterproof Parka (front), Men's Cedar Branch Insulated Bib (back left),
    # Women's Cedar Branch Insulated Parka (back right). All Realtree APX packshots from the store.
    compose_cluster([
        {"file": "mens-cedar-branch-insulated-bib", "height": 664, "cx": 378, "cy": 402, "angle": 8, "darken": 0.8},
        {"file": "habit-womens-cedar-branch-insulated-parka", "height": 590, "cx": 832, "cy": 392, "angle": -8, "darken": 0.8},
        {"file": "habit-mens-cedar-branch-insulated-waterproof-parka", "height": 708, "cx": 600, "cy": 436, "angle": 0},
    ], "e19-cluster-cedar-branch.jpg", size=(1200, 840))


def job_e20():
    """E20 Technology Bleed: e20-bleed-buck-hollow.jpg + -dm.jpg (Buck Hollow 2.0 cut by the right edge)."""
    # Men's Buck Hollow 2.0 Jacket, Mossy Oak New Bottomland (first store image).
    compose_tech_bleed("mens-buck-hollow-2-0-jacket", "e20-bleed-buck-hollow.jpg", width=480, visible=0.64)


def job_e21():
    """E21 Band-Crossing Product: e21-cross-buck-hollow.jpg + -dm.jpg (Tap Shoe to light warm)."""
    # Men's Buck Hollow 2.0 Jacket, Realtree APX (store image 2), crossing Tap Shoe -> light warm.
    compose_band_cross("mens-buck-hollow-2-0-jacket-2", "e21-cross-buck-hollow.jpg",
                       top=TAPSHOE, bottom=LIGHT, size=(1200, 660), seam=370, product_h=600, cx=236, angle=-5)


def job_e22():
    """E22 Photo Collage: e22-collage-a.jpg, e22-collage-b.jpg (framed, off-axis, torn edges)."""
    hay = ref_crop("September 24.png", (66, 2672, 436, 3268))       # man on hay bale, Sep 24
    barn = ref_crop("September 24.png", (0, 4100, 1200, 4690))       # man in the barn, Sep 24
    pocket = pack_photo("mens-heavyweight-soft-flannel-6.png", (40, 150, 1160, 1190))   # chest pocket close-up, store
    compose_collage([
        {"img": hay, "width": 470, "cx": 350, "cy": 420, "angle": 2.2},
        {"img": pocket, "width": 480, "cx": 820, "cy": 540, "angle": -3, "deckle": "right"},
    ], "e22-collage-a.jpg", size=(1200, 900))
    compose_collage([
        {"img": barn, "width": 1000, "cx": 600, "cy": 350, "angle": -1.4, "deckle": "bottom"},
    ], "e22-collage-b.jpg", size=(1200, 700))


def job_e23():
    """E23 One Product Per Band: e23-*.png packshots + printed swatch hexes for the color dots."""
    product_png("mens-crater-valley-performance-hoodie-2", 800, "e23-crater-valley-hoodie.png", pad=0.04, limit=MAX_JPG)
    product_png("mens-cedar-branch-insulated-bib", 800, "e23-cedar-branch-bib.png", pad=0.04, limit=MAX_JPG)
    print("  swatches (variant: packshot -> hex)")
    for label, f in (("Crater Valley: Woodland Ghost Khaki", "mens-crater-valley-performance-hoodie-2.png"),
                     ("Crater Valley: Woodland Vintage Wren", "mens-crater-valley-performance-hoodie.png"),
                     ("Crater Valley: Woodland Helix Major Brown", "mens-crater-valley-performance-hoodie-9.png"),
                     ("Crater Valley: Fallen Rock", "mens-crater-valley-performance-hoodie-10.png"),
                     ("Crater Valley: Ivy Green", "mens-crater-valley-performance-hoodie-11.png"),
                     ("Cedar Branch Bib: Realtree APX", "mens-cedar-branch-insulated-bib.png"),
                     ("Cedar Branch Bib: Mossy Oak New Bottomland", "mens-cedar-branch-insulated-bib-2.png"),
                     ("Cedar Branch Bib: Turkish Coffee", "mens-cedar-branch-insulated-bib-8.png")):
        print(f"    {label:45s} {f:48s} {swatch(f)}")


def job_packs():
    """Packshot PNGs for the approved E04, E07, E17 (content swap only)."""
    # Sample-content swaps in the approved modules (structure unchanged).
    product_png("mens-heavyweight-soft-flannel", 360, "pack-mens-heavyweight-soft-flannel-360.png")          # E04
    product_png("mens-heavyweight-soft-flannel", 200, "pack-mens-heavyweight-soft-flannel-200.png")          # E07
    product_png("mens-crater-valley-full-zip-fleece-jacket", 200, "pack-mens-crater-valley-full-zip-200.png")  # E07
    product_png("habit-mens-cedar-branch-insulated-waterproof-parka", 400, "pack-mens-cedar-branch-parka-400.png")  # E17
    product_png("mens-cedar-branch-insulated-bib", 400, "pack-mens-cedar-branch-bib-400.png")                # E17


def job_textures_v04():
    """v0.4 texture set: paper, grains, water, camo, topo, gradients (1200x1600, < 90KB, seamless tiles)."""
    make_texture_set()


EDGES_V04 = [   # (top texture, bottom texture, dark-mode twin?)  file: edge-tex-{top}-{bottom}.jpg
    ("paper-light", "paper-tapshoe", True), ("paper-tapshoe", "paper-light", True),
    ("paper-light", "grain-patriot", True), ("grain-patriot", "paper-light", True),
    ("paper-tapshoe", "grain-brown", False), ("grain-brown", "paper-tapshoe", False),
    ("grain-brown", "paper-light", True), ("grain-brown", "grain-patriot", False),
    ("grain-patriot", "grain-brown", False), ("grain-brown", "camo-blur", False), ("camo-blur", "grain-ivy", False),
    ("grain-ivy", "camo-blur", False), ("grain-ivy", "paper-tapshoe", False),
    ("paper-light", "flat:#2A2B2D", True), ("grain-patriot", "flat:#2A2B2D", False),
    ("grain-brown", "flat:#2A2B2D", False), ("grain-ivy", "flat:#2A2B2D", False),
    ("camo-blur", "flat:#2A2B2D", False),
]


def edge_name(top: str, bottom: str) -> str:
    short = lambda n: "footer" if n.startswith("flat:") else n.replace("grain-", "").replace("paper-", "paper").replace("-blur", "")
    return f"edge-tex-{short(top)}-{short(bottom)}.jpg"


def job_edges_v04():
    """E18 textured torn edges (edge-tex-*.jpg, 1200x80 shown 600x40): the texture of the band below
    carries into the edge; -dm twins where a light paper band is involved."""
    for i, (top, bottom, dm) in enumerate(EDGES_V04):
        swap = lambda n: "paper-light-dm" if n == "paper-light" else n
        compose_torn_edge_textured(top, bottom, edge_name(top, bottom), h=80, seed=30 + i,
                                   dm={"top": swap(top), "bottom": swap(bottom)} if dm else None)


def job_e24():
    """E24 Full-Bleed Photo Hero: e24-hero-forest.jpg (text top) + e24-hero-barn.jpg (text bottom)."""
    # Text top: family walking into the woods (crop of Sep 15), calm area grown from the photo's own
    # dark top rows. Heads sit at file y 849-930 (display 425-465), right under the button (display 398).
    compose_full_bleed_hero(lifestyle("crop-sent-sep15-family-forest-walk.jpg"), "e24-hero-forest.jpg",
                            size=(1200, 1560), photo_w=1500, photo_y=830, extend_top="fog",
                            top_shade=(900, 0.5), fade=(1290, 1470), tear_y=1500, next_tex="grain-ivy",
                            text_boxes={"desktop": (100, 180, 1100, 800), "mobile": (190, 140, 1010, 830)},
                            seed=91)
    # Text bottom: man carrying feed at the barn door (crop of Sep 24). The crop starts at his head, so
    # the barn siding and door frame are pulled up 190 rows for the logo; legs cut, bottom melts into
    # Tap Shoe paper where the live text sits.
    compose_full_bleed_hero(lifestyle("crop-sent-sep24-barn-door-feed-bag.jpg"), "e24-hero-barn.jpg",
                            size=(1200, 1560), photo_w=1200, photo_y=190, photo_rows=(0, 720), extend_top="stretch",
                            top_shade=(300, 0.5), fade=(650, 900), tear_y=1500, next_tex="grain-brown",
                            text_boxes={"logo": (440, 50, 760, 130), "desktop": (100, 810, 1100, 1430),
                                        "mobile": (170, 760, 1030, 1430)}, seed=95)


def job_e26():
    """E26 Torn Photo: e26-torn-stable.jpg (+ -dm) on light paper, e26-torn-camp.jpg on Major Brown grain."""
    compose_torn_photo(lifestyle("crop-sent-sep24-stable-horse.jpg"), "e26-torn-stable.jpg", band="paper-light",
                       dm_band="paper-light-dm", size=(1200, 820), photo_w=1000, cx=600, cy=410, angle=-1.6,
                       sides=("bottom", "right"), frame=14, frame_color="#F4F1ED", seed=121)
    compose_torn_photo(lifestyle("crop-sent-sep15-camp-chairs-family.jpg"), "e26-torn-camp.jpg", band="grain-brown",
                       size=(1200, 600), photo_w=1040, cx=600, cy=300, angle=1.4, sides=("top", "left"),
                       frame=14, frame_color=FRAME, seed=131)


JOBS = {"textures": job_textures, "e19": job_e19, "e20": job_e20, "e21": job_e21,
        "e22": job_e22, "e23": job_e23, "packs": job_packs,
        "textures04": job_textures_v04, "edges04": job_edges_v04, "e24": job_e24, "e26": job_e26}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="*", choices=sorted(JOBS), help="run only these jobs")
    ap.add_argument("--list", action="store_true", help="list jobs and exit")
    a = ap.parse_args()
    if a.list:
        for k, f in JOBS.items():
            print(f"{k:9s} {(f.__doc__ or '').strip() or f.__name__}")
        return
    for k in a.only or JOBS:
        print(f"[{k}]")
        JOBS[k]()


if __name__ == "__main__":
    main()
