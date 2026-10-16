"""Round 5 client feedback (2026-10-14): lighten the Figma photos.

Usage: python grade_r5.py

img/{kitchen,livingroom}-figma.jpg -> img/{kitchen,livingroom}-r5.jpg

- V1 kitchen: slight overall brighten, plus a masked lift of mids and shadows on the
  oven and, stronger, on the turkey, so the cutdowns that show mostly the turkey don't
  read too dark. Highlights stay pinned; the turkey stays burnt, just readable.
- V2 living room: slight overall brighten only.
The originals are kept; export.py and build.py read the -r5 files.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).parent / "img"


def lift(a, gamma, shadow, sat=1.0):
    """Mids up (gamma < 1) and shadows raised, highlights pinned at 1; sat puts back the
    color a lift washes out."""
    a = a ** gamma
    a = shadow + (1 - shadow) * a
    y = (a * [.2126, .7152, .0722]).sum(-1, keepdims=True)
    return y + (a - y) * sat


def soft_mask(size, box, blur):
    """Rectangle with rounded falloff, 0..1."""
    m = Image.new("L", size, 0)
    m.paste(255, box)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(blur)), np.float32)[..., None] / 255


def grade(name, overall, local=()):
    im = Image.open(HERE / f"{name}-figma.jpg").convert("RGB")
    a = np.asarray(im, np.float32) / 255
    a = lift(a, *overall)
    for box, blur, *curve in local:
        m = soft_mask(im.size, box, blur)
        a = a * (1 - m) + lift(a, *curve) * m
    out = Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))
    out.save(HERE / f"{name}-r5.jpg", quality=93, optimize=True)
    print(name, out.size, f"mean {np.asarray(im).mean():.0f} -> {np.asarray(out).mean():.0f}")


# kitchen-figma.jpg is 1856x2304: oven ~ (90, 260)-(1000, 1800), turkey ~ (290, 900)-(720, 1180)
grade("kitchen", (.88, .015), [
    ((80, 250, 1010, 1800), 90, .80, .015, 1.04),  # oven: mids and shadows
    ((270, 880, 740, 1200), 70, .78, .008, 1.10),  # turkey: on top of the oven lift
])
grade("livingroom", (.88, .015))
