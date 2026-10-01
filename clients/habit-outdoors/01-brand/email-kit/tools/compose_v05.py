"""compose_v05.py - Habit Outdoors email kit v0.5 (draft): new surfaces and the images of E27-E34.

Built on top of compose.py (imported, never edited: other scripts import it too). Every helper
of compose.py is reused; the new textures are registered in compose.TEXTURES at import time
(runtime only) so compose.tile_rows / compose_full_bleed_hero can bake them.

Run (from anywhere):
    python clients/habit-outdoors/01-brand/email-kit/tools/compose_v05.py              # every v0.5 job
    python .../compose_v05.py --only surfaces e28 e29                                   # some
    python .../compose_v05.py --list

Run "surfaces" first: e30/e33 bake the new textures in.

Source direction: the owner's revised October emails (email-kit/references/rev-oct-01..05-*.png,
03-work/email/2026-10-broadcasts/revision-r2.md). Photos only from photos/lifestyle (INDEX.md) and
store packshots from photos/products; nothing is cropped from another brand.

Panel colors are brand palette colors (guide p.17) nearest to the ones measured on the revision:
  Aluminum #A39A8C (measured #A69A89), Dusk #ACB1B3 (measured #ABB1B3), Turkish Coffee #5C5249
  (measured #5A4538), Ivy Green #595442 (measured #575441). The rust (#794928) and slate (#4F5B5E)
  panels of rev-oct-02 are outside the palette: open question in the kit README, not used here.
"""
from __future__ import annotations

import argparse
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compose as C  # noqa: E402  (the v0.3/v0.4 library, read-only here)

ASSETS = C.ASSETS
TAPSHOE, BROWN, LIGHT, DM_BAND, PATRIOT, IVY = C.TAPSHOE, C.BROWN, C.LIGHT, C.DM_BAND, C.PATRIOT, C.IVY
ALUMINUM = "#A39A8C"
DUSK = "#ACB1B3"
TURKISH = "#5C5249"
ORANGE = "#FF6400"
W, H = C.TEX_W, C.TEX_H

# New v0.5 surfaces, same record shape as compose.TEXTURES (file, fallback, kind, text on it).
V05_TEXTURES = {
    "paper-camo":      ("tex-paper-camo.jpg",       LIGHT,   "tile",    "#2A2B2D titles/body; labels: see measured contrast"),
    "paper-camo-dm":   ("tex-paper-camo-dm.jpg",    DM_BAND, "tile",    "dark-mode swap of paper-camo"),
    "halftone-brown":  ("tex-halftone-brown.jpg",   BROWN,   "tile",    "white, #E2DDD9 body, orange only large"),
    "grad-tapshoe-patriot-topo": ("grad-tapshoe-to-patriot-topo.jpg", TAPSHOE, "stretch", "white, #E2DDD9 body"),
}
C.TEXTURES.update(V05_TEXTURES)


# ---------------------------------------------------------------- surfaces

def camo_paper(base: str, tones: tuple[str, str], seed: int) -> np.ndarray:
    """Light paper with large camo splotches (rev-oct-03): two splotch layers with crisp, slightly
    soft edges (a printed camo, not a blur), both periodic, then the paper grain of paper_surface."""
    arr = C.paper_surface(base, grain_sd=2.6, mottle=0.8, fibre=4, fibre_sign=-1 if base == LIGHT else 1, seed=seed)
    b = np.array(C.rgb(base), np.float32)
    # layer 1: mid splotches with small satellites
    n1 = C.periodic_noise(W, H, 26, 26, seed + 10) * 0.7 + C.periodic_noise(W, H, 80, 80, seed + 11) * 0.6
    m1 = np.clip((n1 - 0.80) / 0.10, 0, 1)
    # layer 2: a few large patches, a touch deeper
    n2 = C.periodic_noise(W, H, 60, 60, seed + 12) * 0.8 + C.periodic_noise(W, H, 14, 14, seed + 13) * 0.35
    m2 = np.clip((n2 - 1.25) / 0.10, 0, 1)
    # layer 3: small specks scattered around (the busy edge of a printed camo)
    n3 = C.periodic_noise(W, H, 6, 6, seed + 14)
    m3 = np.clip((n3 - 2.3) / 0.15, 0, 1) * np.clip((n1 + 0.2) / 0.4, 0, 1)
    d1 = np.array(C.rgb(tones[0]), np.float32) - b
    d2 = np.array(C.rgb(tones[1]), np.float32) - b
    m1 = np.maximum(m1, m3)
    arr += (m1 * (1 - m2))[:, :, None] * d1 + m2[:, :, None] * d2      # layers never stack
    return arr


def halftone_brown(seed: int = 141) -> np.ndarray:
    """Major Brown with halftone dot splotches (rev-oct-01): a hex grid of dots (16px pitch at 2x,
    periodic in both axes: 75 x 100 cells), dot radius driven by a slow density field, so the dots
    grow in clusters and fade out; a sparse dark spray inside the densest areas; grain on top."""
    arr = C.paper_surface(BROWN, grain_sd=2.0, mottle=1.2, fibre=3, fibre_sign=1, seed=seed)
    pitch = 16
    # darker worn patches under the densest dots (the "spray" areas of rev-oct-01)
    patch = C.periodic_noise(W, H, 90, 70, seed + 4)
    pm = np.clip((patch - 1.0) / 0.8, 0, 1) * 0.16
    arr = arr * (1 - pm[:, :, None])
    dens = C.periodic_noise(W, H, 120, 120, seed + 1) * 0.75 + C.periodic_noise(W, H, 40, 40, seed + 2) * 0.45
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    row = np.floor(yy / pitch)
    off = (row % 2) * (pitch / 2)
    cx = (np.floor((xx - off) / pitch) + 0.5) * pitch + off
    cy = (row + 0.5) * pitch
    # nearest centre is either this cell or the neighbour row; for a 16px hex grid with small dots
    # the own cell is enough (max radius < pitch / 2)
    dist = np.hypot(xx - cx, yy - cy)
    ci = np.clip(cy.astype(int), 0, H - 1)
    cj = (cx.astype(int)) % W
    r = np.clip((dens[ci, cj] + 0.35) * 5.6, 0, 7.8)
    a = np.clip(r - dist + 0.5, 0, 1) * (r > 0.6)
    dot = np.array(C.rgb("#1B1511"), np.float32)
    arr = arr * (1 - a[:, :, None] * 0.88) + dot * (a[:, :, None] * 0.88)
    spray = C.periodic_noise(W, H, 4, 4, seed + 3)
    sm = np.clip((spray - 2.1) / 0.3, 0, 1) * np.clip((dens - 0.9) / 0.3, 0, 1)
    arr = arr * (1 - sm[:, :, None] * 0.8) + dot * (sm[:, :, None] * 0.8)
    return arr


def grad_topo(top: str, bottom: str, seed: int = 151) -> np.ndarray:
    """Stretch gradient Tap Shoe -> Patriot Blue with the topographic lines (rev-oct-05 attribute band)."""
    arr = C.gradient_surface(top, bottom, haze=6, seed=seed)
    arr += (C.topo_lines((W, H)) * 11)[:, :, None]
    return arr


def job_surfaces():
    """tex-paper-camo.jpg (+ -dm), tex-halftone-brown.jpg, grad-tapshoe-to-patriot-topo.jpg (< 90KB each)."""
    jobs = {
        "paper-camo":    (lambda: camo_paper(LIGHT, ("#D5CFC8", "#D0CAC2"), seed=201),
                          ["#2A2B2D", "#5C5249"]),
        "paper-camo-dm": (lambda: camo_paper(DM_BAND, ("#38393E", "#3A3B40"), seed=202),
                          ["#F1EEEB", "#D6D0CA", "#B0A89C"]),
        "halftone-brown": (halftone_brown, ["#FFFFFF", "#E2DDD9", ORANGE]),
        "grad-tapshoe-patriot-topo": (lambda: grad_topo(TAPSHOE, PATRIOT), ["#FFFFFF", "#E2DDD9", ORANGE]),
    }
    for name, (fn, texts) in jobs.items():
        f, fallback, kind, _ = V05_TEXTURES[name]
        # stretched gradients: 4:4:4 (4:2:0 bands the dark blue in visible chroma steps)
        p = C.save_jpg_under(C.to_image(fn()), ASSETS / f, C.MAX_TEX, q=70, subsampling=0 if kind == "stretch" else 2)
        arr = np.asarray(Image.open(p).convert("RGB"), np.int16)
        seam = float(np.abs(arr[:4].mean(0) - arr[-4:].mean(0)).mean()) if kind == "tile" else -1
        mean = "#%02X%02X%02X" % tuple(int(v) for v in arr.reshape(-1, 3).mean(0))
        print(f"  {f:34s} {p.stat().st_size / 1024:5.1f} KB  fallback {fallback}  mean {mean}  "
              f"{'wrap diff %.1f' % seam if seam >= 0 else 'stretch'}  {C.contrast_report(p, texts, blur=0)}")
    # E18 textured edges for the new surfaces (compose.compose_torn_edge_textured, same recipe as v0.4)
    for i, (top, bottom, dm) in enumerate((("paper-tapshoe", "paper-camo", True), ("paper-camo", "paper-tapshoe", True),
                                           ("halftone-brown", "paper-tapshoe", False),
                                           ("paper-tapshoe", "halftone-brown", False),
                                           ("halftone-brown", "flat:#2A2B2D", False))):
        swap = lambda n: "paper-camo-dm" if n == "paper-camo" else n
        short = lambda n: "footer" if n.startswith("flat:") else n.replace("paper-", "paper").replace("-brown", "brown").replace("-", "")
        C.compose_torn_edge_textured(top, bottom, f"edge-tex-{short(top)}-{short(bottom)}.jpg", h=80, seed=300 + i,
                                     dm={"top": swap(top), "bottom": swap(bottom)} if dm else None)


# ---------------------------------------------------------------- product panels

def panel_packshot(file: str, out: str, color: str, size=(600, 660), product_h: int | None = None,
                   product_w: int | None = None, cy_shift: int = 0) -> Path:
    """Packshot centred on a flat palette color panel, soft drop shadow (E28 checkerboard, E29 card)."""
    im = C.load_packshot(file)
    if product_w and (product_h is None or im.width / im.height * (product_h or 0) > product_w):
        im = C.fit(im, w=product_w)
    else:
        im = C.fit(im, h=product_h or round(size[1] * 0.86))
    canvas = Image.new("RGBA", size, C.rgb(color) + (255,))
    C.place(canvas, im, size[0] / 2, size[1] / 2 + cy_shift, 0, shadow=(0, 12, 16, 0.32))
    p = C.save_jpg(canvas.convert("RGB"), out, match=(color,))
    C.report(p, color, color)
    return p


def panel_model(file: str, crop: tuple[int, int, int, int], out: str, size=(400, 660),
                color: str = TURKISH) -> Path:
    """Store model photo (transparent studio cut-out, printed spec text cropped off) on a FLAT palette
    color, cover-cropped to the panel (E29 photo variant, rev-oct-04). Flat, not a gradient: on mobile
    the panel cell is wider than the image and its bgcolor must continue the image edges."""
    im = Image.open(C.PRODUCTS / file).convert("RGBA").crop(crop)
    s = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x0 = (im.width - size[0]) // 2
    im = im.crop((x0, 0, x0 + size[0], size[1]))
    bg = Image.new("RGBA", size, C.rgb(color) + (255,))
    bg.alpha_composite(im)
    p = C.save_jpg(bg.convert("RGB"), out, match=(color,))
    C.report(p, color, None)
    return p


def job_e28():
    """E28 Checkerboard Product Row: e28-panel-*.jpg (600x660, shown 300x330), packshot on flat palette color."""
    # Men's Shadow Series Mid Layer Hooded Jacket (Mossy Oak Terra Coyote) on Aluminum;
    # Men's Shadow Series Windproof Fleece Pant on Dusk.
    panel_packshot("men-s-mid-layer-jacket", "e28-panel-mid-layer-jacket.jpg", ALUMINUM, product_h=560)
    panel_packshot("men-s-windproof-fleece-pant", "e28-panel-windproof-pant.jpg", DUSK, product_h=580)


def job_e29():
    """E29 Framed Product Card: e29-panel-*.jpg (400x660, shown 200x330)."""
    # Packshot variant: Youth Cedar Branch Insulated Bib (Realtree APX) on Ivy Green.
    panel_packshot("youth-cedar-branch-insulated-bib", "e29-panel-youth-bib.jpg", IVY, size=(400, 660),
                   product_h=600, product_w=360)
    # Photo variant: Men's Crater Valley Full Zip Fleece Jacket, store model image 4 (spec text at x > 860 cut off).
    panel_model("mens-crater-valley-full-zip-fleece-jacket-4.png", (0, 0, 860, 1200), "e29-panel-crater-fleece-model.jpg")


# ---------------------------------------------------------------- photo bands

def soft(name: str, width: int, radius: float = 0.8) -> Image.Image:
    """Lifestyle photo resized to the composition width and softened a touch: foliage detail is what
    pushes a full-bleed JPG past 150KB; at email scale a 0.8px blur at 2x is not visible."""
    im = C.fit(C.lifestyle(name), w=width)
    return im.filter(ImageFilter.GaussianBlur(radius))


def job_e30():
    """E30 Photo Closing Band: e30-closing-hunter.jpg (1200x1500, shown 600x750), text over the dark bottom."""
    # Bow hunter from behind in the golden forest (orig-hunt40, a Habit original). The photo melts into
    # Tap Shoe paper under the live text and tears into the flat Tap Shoe footer (E13).
    C.compose_full_bleed_hero(soft("orig-hunt40-hunter-forest-back.jpg", 1200, 1.1), "e30-closing-hunter.jpg",
                              size=(1200, 1500), photo_w=1200, photo_y=0, photo_rows=(240, 1140),
                              fade=(600, 900), base="paper-tapshoe", tear_y=1450, next_tex="flat:#2A2B2D",
                              text_boxes={"desktop": (100, 880, 1100, 1400), "mobile": (170, 860, 1030, 1420)},
                              grain_sd=0, seed=171)


def job_e33():
    """E33 Label Hero: e33-label-hero-field.jpg (1200x1400, shown 600x700), labels live on top."""
    # Three hunters walking up the field at sunrise (orig-hunt22). Sky pulled toward Tap Shoe for the
    # white logotype; grass melts into Tap Shoe paper for the subtitle and button; tears into the
    # halftone Major Brown (the band that follows in the kit sample, as in rev-oct-01).
    C.compose_full_bleed_hero(soft("orig-hunt22-three-hunters-field-sunrise.jpg", 1500, 0.95), "e33-label-hero-field.jpg",
                              size=(1200, 1400), photo_w=1500, photo_y=0, photo_rows=(0, 1000), top_shade=(340, 0.95),
                              fade=(700, 990), base="paper-tapshoe", tear_y=1350, next_tex="halftone-brown",
                              text_boxes={"logo": (440, 50, 760, 130), "sub+button": (100, 1000, 1100, 1320)},
                              grain_sd=0, seed=181)


def tilted_photo(photo: Image.Image, out: str, *, band: str, dm_band: str | None, size=(520, 700),
                 photo_w: int = 400, frame: int = 12, angle: float = 4.0, seed: int = 191) -> list[Path]:
    """E31 Tilted Framed Photo: photo in a WHITE frame (6px shown), rotated `angle`, drop shadow,
    baked on the band texture (tile rows from 0) + a -dm twin on the dark paper."""
    ph = C.fit(photo.convert("RGB"), w=photo_w - frame * 2)
    fr = Image.new("RGBA", (ph.width + frame * 2, ph.height + frame * 2), (255, 255, 255, 255))
    fr.paste(ph, (frame, frame))
    paths = []
    for suffix, bname in [("", band)] + ([("-dm", dm_band)] if dm_band else []):
        canvas = C.to_image(C.tile_rows(bname, size[1])[:, : size[0]])
        C.place(canvas, fr, size[0] / 2, size[1] / 2, angle, shadow=(6, 14, 16, 0.45))
        p = C.save_jpg_under(canvas, ASSETS / out.replace(".jpg", f"{suffix}.jpg"), C.MAX_JPG, q=76, floor=56, subsampling=2)
        print(f"  {p.name:42s} {size[0]}x{size[1]}  {p.stat().st_size / 1024:5.1f} KB  on {bname}")
        paths.append(p)
    return paths


def job_e31():
    """E31 Tilted Framed Photo: e31-tilt-blind.jpg + -dm.jpg (480x646, shown 240x323) on light paper."""
    # Hunter in an orange Habit cap stepping out of the blind (crop of Sep 2, stand-in until the original).
    tilted_photo(C.lifestyle("crop-sent-sep2-hunter-blind.jpg"), "e31-tilt-blind.jpg", band="paper-light",
                 dm_band="paper-light-dm", size=(480, 646), photo_w=388, frame=12, angle=4.0)


def bleed_on_texture(file: str, out: str, *, band: str, size=(360, 800), product_h: int = 780,
                     left: int = 24, cy: float | None = None) -> Path:
    """E32: packshot cut by the RIGHT edge, baked on the band texture (the cell touches the email edge).
    The product is scaled to product_h and starts `left` px from the image's left edge; whatever is
    wider than the image is cut by the email edge."""
    im = C.fit(C.load_packshot(file), h=product_h)
    canvas = C.to_image(C.tile_rows(band, size[1])[:, : size[0]])
    C.place(canvas, im, left + im.width / 2, cy or size[1] / 2, 0, shadow=(0, 14, 18, 0.4))
    print(f"      visible share of the product width: {min(1, (size[0] - left) / im.width):.0%}")
    p = C.save_jpg_under(canvas, ASSETS / out, C.MAX_JPG, q=76, floor=56, subsampling=2)
    print(f"  {p.name:42s} {size[0]}x{size[1]}  {p.stat().st_size / 1024:5.1f} KB  on {band}")
    return p


def job_e32():
    """E32 Single Review: e32-review-bib.jpg (300x800, shown 150x400) on Tap Shoe paper."""
    # Men's Cedar Branch Insulated Bib (Realtree APX): the product the sample review talks about
    # (rev-oct-01 shows the parka next to a bib review; the kit pairs the review with its own product).
    bleed_on_texture("mens-cedar-branch-insulated-bib", "e32-review-bib.jpg",
                     band="paper-tapshoe", size=(300, 800), product_h=780, left=130)


# ---------------------------------------------------------------- attribute icons (official, guide p.21)

GUIDE_PDF = C.KIT.parent / "identity" / "Habit_BrandIdentityGuide_Booklet 2.4.26 Update.pdf"
# page index 20 = printed p.18 "Technologies" (the kit README cites it as p.21, the PDF page number)
ICON_BOXES = {                      # PDF points (792x612 page): icon only, no label text
    "icon-rain-factor-waterproof.png": (16, 136, 50, 176),
    "icon-scent-factor.png": (15, 310, 50, 342),
    "icon-windproof.png": (406, 313, 448, 343),
    "icon-breathable.png": (411, 254, 448, 293),
}


def _components(mask: np.ndarray) -> list[np.ndarray]:
    """4-connected components of a boolean mask (small images only; no scipy on this machine)."""
    seen = np.zeros_like(mask, bool)
    out = []
    H_, W_ = mask.shape
    for y0, x0 in zip(*np.nonzero(mask)):
        if seen[y0, x0]:
            continue
        stack, pts = [(y0, x0)], []
        seen[y0, x0] = True
        while stack:
            y, x = stack.pop()
            pts.append((y, x))
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < H_ and 0 <= xx < W_ and mask[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True
                    stack.append((yy, xx))
        out.append(np.array(pts))
    return out


def official_icon(box: tuple[float, float, float, float], out: str, px: int = 128, pad: int = 10) -> Path:
    """Guide p.21 pictogram rendered from the vector PDF at 600 dpi, recolored for dark bands: the
    pictogram white, its straight "fabric" bars orange (the owner's rev-oct-05 treatment: icon over
    two orange rules). Transparent PNG px x px (shown px/2)."""
    import pymupdf
    doc = pymupdf.open(GUIDE_PDF)
    pix = doc[20].get_pixmap(dpi=600, clip=pymupdf.Rect(*box))
    g = np.asarray(Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("L"), np.float32)
    alpha = np.clip((190 - g) / 120, 0, 1)                 # pictogram is near black; topo lines are light grey
    solid = alpha > 0.5
    rgba = np.zeros(g.shape + (4,), np.float32)
    rgba[..., :3] = 255
    for comp in _components(solid):
        ys, xs = comp[:, 0], comp[:, 1]
        h_, w_ = np.ptp(ys) + 1, np.ptp(xs) + 1
        fill = len(comp) / (h_ * w_)
        if len(comp) > 200 and fill > 0.72 and max(h_, w_) / min(h_, w_) > 3.2:
            y0, y1, x0, x1 = ys.min() - 3, ys.max() + 4, xs.min() - 3, xs.max() + 4
            rgba[max(0, y0):y1, max(0, x0):x1, :3] = C.rgb(ORANGE)      # bar + its antialiased rim
    rgba[..., 3] = alpha * 255
    im = Image.fromarray(rgba.astype(np.uint8), "RGBA")
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox())
    im.thumbnail((px - pad * 2, px - pad * 2), Image.LANCZOS)
    canvas = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    canvas.alpha_composite(im, ((px - im.width) // 2, (px - im.height) // 2))
    p = ASSETS / out
    canvas.save(p, optimize=True)
    print(f"  {p.name:42s} {px}x{px}  {p.stat().st_size / 1024:5.1f} KB  from guide PDF page 21")
    return p


def job_icons():
    """E34 Attribute Grid icons: official tech pictograms of guide p.21 (PDF vector), white + orange bars, 128x128 shown 64."""
    for out, box in ICON_BOXES.items():
        official_icon(box, out)


JOBS = {"surfaces": job_surfaces, "e28": job_e28, "e29": job_e29, "e30": job_e30, "e31": job_e31,
        "e32": job_e32, "e33": job_e33, "icons": job_icons}


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
