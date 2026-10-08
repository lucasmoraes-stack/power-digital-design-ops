"""Silhouette the knolling shots (img-knolling/raw/*.png, AI-generated top-down on white)
into cutouts that keep their own soft contact shadow: img-knolling/{item}.png.

Usage: python cutout.py

Background = the bright, neutral pixels connected to the image border (flood fill), so
light parts inside a product (a white washer door ring, a duvet) stay solid. On that
background, the grey of the original shadow becomes black at matching opacity, so the
shadow survives on any ground colour instead of carrying a white box with it.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).parent
RAW, OUT = HERE / "img-knolling" / "raw", HERE / "img-knolling"
WHITE, FLOOR, SHADOW = 250.0, 110.0, 0.8   # pure bg, darkest shadow tone, max shadow opacity
FEATHER = 40.0  # px over which a shadow fades out before the frame edge
EDGE = 9.0  # luminance step (per 2px) that counts as a product outline: shadows ramp softer than that


# one-piece products with a convex silhouette: a light, smooth face (duvet, washer body)
# can leak into the flood through a soft outline, so everything inside the product's
# convex hull is product. The console set is two pieces and stays out of this.
SOLID = {"fridge", "laptop", "mattress", "sofa", "tire", "tv", "washer"}


def hull_mask(item):
    ys, xs = np.nonzero(item)
    pts = sorted(set(zip(xs[::7].tolist(), ys[::7].tolist())) | set(zip(xs[-1:].tolist(), ys[-1:].tolist())))

    def half(points):
        h = []
        for p in points:
            while len(h) >= 2 and (h[-1][0] - h[-2][0]) * (p[1] - h[-2][1]) - (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0]) <= 0:
                h.pop()
            h.append(p)
        return h

    hull = half(pts)[:-1] + half(pts[::-1])[:-1]
    m = Image.new("L", (item.shape[1], item.shape[0]), 0)
    ImageDraw.Draw(m).polygon(hull, fill=255)
    return np.asarray(m) == 255


def cut(src: Path, dst: Path):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    lum = a.mean(axis=2)
    chroma = a.max(axis=2) - a.min(axis=2)
    # shadows are neutral and ramp smoothly; a product outline is a hard step, so the
    # flood from the border runs through shadow but stops at the outline
    bl = np.asarray(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)
    grad = np.zeros_like(bl)
    grad[:, 2:-2] = np.maximum(grad[:, 2:-2], np.abs(bl[:, 4:] - bl[:, :-4]) / 2)
    grad[2:-2, :] = np.maximum(grad[2:-2, :], np.abs(bl[4:, :] - bl[:-4, :]) / 2)
    cand = (lum > FLOOR) & (chroma < 14) & (grad < EDGE)

    m = Image.fromarray(np.where(cand, 255, 0).astype(np.uint8)).copy()  # own buffer, or floodfill is a no-op
    w, h = m.size
    seeds = [(x, 0) for x in range(0, w, 8)] + [(x, h - 1) for x in range(0, w, 8)] + \
            [(0, y) for y in range(0, h, 8)] + [(w - 1, y) for y in range(0, h, 8)]
    for s in seeds:
        if m.getpixel(s) == 255:
            ImageDraw.floodfill(m, s, 128)
    bg = np.asarray(m) == 128
    if src.stem in SOLID:
        bg &= ~hull_mask(~bg)

    item = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    ia = np.asarray(item).astype(np.float32) / 255.0
    sa = np.clip((WHITE - lum) / (WHITE - FLOOR), 0, 1) * SHADOW
    sa = np.where(bg, sa, 0.0)
    # a shadow that runs into the edge of the generated frame would end in a hard line:
    # fade it out over the last FEATHER px instead
    yy, xx = np.mgrid[0:h, 0:w]
    edge = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)).astype(np.float32)
    sa *= np.clip(edge / FEATHER, 0, 1) ** 1.5
    out_a = ia + sa * (1 - ia)
    rgb = np.where(out_a[..., None] > 0, a * ia[..., None] / np.maximum(out_a, 1e-6)[..., None], 0)

    rgba = np.dstack([rgb, out_a * 255]).clip(0, 255).astype(np.uint8)
    res = Image.fromarray(rgba, "RGBA")
    res = res.crop(Image.fromarray((out_a > 0.03).astype(np.uint8) * 255).getbbox())
    res.save(dst)
    return res.size


if __name__ == "__main__":
    for p in sorted(RAW.glob("*.png")):
        print(p.stem, cut(p, OUT / p.name))
