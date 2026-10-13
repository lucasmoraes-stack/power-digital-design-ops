"""QA for the glass key: find white glass the key left behind (halos on fur/leaves, streaks).

    python -I qa_key.py            -> every plate in use, report + crops in img/review/qa/

A pixel is flagged when it sits inside the window area (glass bbox), is bright and neutral like
the blown-out glass (min channel >= 200, saturation < 22) and touches the drawn city
(within 3 px of a pixel that took >= 50% of the illustration). Clusters are boxed and cropped.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from compose import city  # noqa: E402
from detect import detect  # noqa: E402
from make import IND, RAW, glass_mask  # noqa: E402

OUT = HERE / "img" / "review" / "qa"


def composite(path):
    tv = detect(path)["tv"]
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    k, (gx0, gy0, gx1, gy1) = glass_mask(a, tv)
    art = np.full_like(a, 255)
    art[gy0:gy1, gx0:gx1] = np.asarray(city(gx1 - gx0, gy1 - gy0)).astype(np.float32)
    out = a + k[..., None] * (art - 255)
    return out.clip(0, 255), k, (gx0, gy0, gx1, gy1), tv


def flags(out, k, box, tv):
    gx0, gy0, gx1, gy1 = box
    mn = out.min(2); sat = out.max(2) - mn
    bright = (mn >= 200) & (sat < 22)
    near = np.asarray(Image.fromarray(((k >= .5) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))) > 0
    f = bright & near & (k < .9)          # fully keyed pixels are the drawing itself (clouds)
    m = np.zeros_like(f); m[gy0:gy1, gx0:gx1] = True
    x0, y0, x1, y1 = tv
    m[y0 - 2:y1 + 2, x0 - 2:x1 + 2] = False      # the TV glass gets the ad, not the city
    return f & m


def report(path):
    out, k, box, tv = composite(path)
    f = flags(out, k, box, tv)
    n = int(f.sum())
    name = path.stem
    if n:
        OUT.mkdir(parents=True, exist_ok=True)
        im = Image.fromarray(out.astype(np.uint8))
        d = ImageDraw.Draw(im)
        ys, xs = np.where(f)
        for y, x in zip(ys[::7], xs[::7]):
            d.point((x, y), fill=(255, 0, 0))
        im.save(OUT / f"{name}.png")
    return name, n


if __name__ == "__main__":
    files = [RAW / f"{i}-plate-{p}.png" for i in IND for p in ("1x1", "tall")]
    total = 0
    for f in files:
        name, n = report(f)
        total += n
        print(f"{name:24s} {n:6d} flagged px")
    print("total", total)
