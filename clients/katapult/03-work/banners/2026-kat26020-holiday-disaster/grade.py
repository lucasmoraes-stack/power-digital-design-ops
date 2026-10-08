"""Lighten the two client-approved photos (brief: "they do need to be lightened/brightened some").

Usage: python grade.py

img/raw/{kitchen-turkey,livingroom-tree}.png -> img/{kitchen,livingroom}.jpg
Same pictures, no retouching of content: a midtone/shadow lift, a touch of contrast
back on top so the Eggleston flatness doesn't turn to haze, and a slight warm-cast
cut (the raws lean orange) so whites read as white. Highlights are protected.
"""
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).parent
JOBS = {
    # name: (source, gamma, shadow lift, blue gain, red gain, saturation)
    "kitchen": ("kitchen-turkey.png", .74, .05, 1.04, .985, 1.04),
    "livingroom": ("livingroom-tree.png", .72, .07, 1.05, .98, 1.03),
}

for name, (src, gamma, lift, bg, rg, sat) in JOBS.items():
    im = Image.open(HERE / "img" / "raw" / src).convert("RGB")
    a = np.asarray(im, np.float32) / 255
    a[..., 0] *= rg
    a[..., 2] *= bg
    a = np.clip(a, 0, 1)
    # midtones up, shadows lifted, highlights pinned at 1
    a = a ** gamma
    a = lift + (1 - lift) * a
    # gentle S-curve to keep some bite after the lift
    a = a + .10 * (a - .5) * (1 - np.abs(2 * a - 1))
    # saturation around luma
    y = (a * [.2126, .7152, .0722]).sum(-1, keepdims=True)
    a = y + (a - y) * sat
    out = Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))
    out.save(HERE / "img" / f"{name}.jpg", quality=92, optimize=True)
    print(name, out.size, f"mean {np.asarray(im).mean():.0f} -> {np.asarray(out).mean():.0f}")
