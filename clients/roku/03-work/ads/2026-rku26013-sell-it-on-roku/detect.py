"""Find the window glass and the TV glass in a generated room plate (numpy only).

Plates are generated with blown-out white glass, thin black steel window frames and a
switched-off black TV:
  TV     = the tallest block of rows holding one long dark run
  window = between the last thin frame bar above the TV and the first one below its middle,
           and between the outer frame posts measured above the TV
"""
import numpy as np
from PIL import Image


def _blocks(flags):
    """Contiguous True runs as (start, end_exclusive)."""
    out, start = [], None
    for i, f in enumerate(list(flags) + [False]):
        if f and start is None:
            start = i
        elif not f and start is not None:
            out.append((start, i)); start = None
    return out


def detect(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    h, w, _ = a.shape
    lum = a.mean(2)

    # TV
    dark = lum < 70
    runs = {}
    for y in range(int(h * .12), int(h * .9)):
        best = max(((e - s, s, e) for s, e in _blocks(dark[y])), default=(0, 0, 0))
        if best[0] > w * .25:
            runs[y] = best
    flags = np.zeros(h, bool); flags[list(runs)] = True
    ty0, ty1 = max(_blocks(flags), key=lambda b: b[1] - b[0])
    tx0 = int(np.median([runs[y][1] for y in range(ty0, ty1)]))
    tx1 = int(np.median([runs[y][2] for y in range(ty0, ty1)]))
    i = 3  # step inside the bezel
    tv = (tx0 + i, ty0 + i, tx1 - i, ty1 - i)

    # window frame
    frame = lum < 95
    bars = [b for b in _blocks(frame.mean(1) > 0.55) if b[1] - b[0] <= h * .03]
    above = [b for b in bars if b[1] <= ty0 - 4]
    y0 = above[-1][1] if above else int(h * .1)
    below = [b for b in bars if b[0] >= (ty0 + ty1) / 2]
    y1 = below[0][0] if below else ty1
    band = frame[y0:max(y0 + 8, ty0 - 4)]
    posts = np.where(band.mean(0) > 0.6)[0]
    x0 = int(posts.min()) if len(posts) else 0
    x1 = int(posts.max()) + 1 if len(posts) else w
    return {"size": (w, h), "window": (x0, y0, x1, y1), "tv": tv}


if __name__ == "__main__":
    import glob, sys
    for f in sorted(glob.glob(sys.argv[1] if len(sys.argv) > 1 else "img/raw/*-plate-*.png")):
        try:
            print(f.replace("\\", "/").split("/")[-1], detect(f))
        except Exception as e:  # noqa: BLE001
            print(f, "FAILED", e)
