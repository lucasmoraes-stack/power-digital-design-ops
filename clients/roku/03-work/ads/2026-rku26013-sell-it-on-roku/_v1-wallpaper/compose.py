"""RKU26013 background compositor (mixed media, per the concept deck refs, slide 7).

Real layer:  Figma AI room plate (img/raw/<ind>-plate-*.png) + TV screen ad (img/raw/<ind>-screen-*.png)
Drawn layer: our own lilac city skyline, painted only on the wall pixels so it sits
             behind the sofa, like the deck reference. Same skyline for every industry.

    python -I compose.py            -> img/<ind>-bg-1440x1440.png + frame html in build/
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
RAW = HERE / "img" / "raw"
OUT = HERE / "img"

# per-plate measurements in the plate's own 1024 space
PLATES = {
    "pet": {
        "plate": "pet-plate-v1.png", "screen": "pet-screen-v1.png",
        "screen_box": (359, 296, 870, 576),          # inner glass of the TV
        "wall_right": 352, "baseboard": 722,          # skyline lives left of the TV, above the floor
        "exclude": [(0, 452), (34, 456), (62, 498), (172, 508), (172, 1024), (0, 1024)],  # sofa + pillow
    },
}


def skyline(w, h, base):
    """Generic city silhouette in two lilac depths, drawn at plate scale (1024). Our own drawing,
    no Roku City art: varied towers, stepped crowns, a spire, a water tower, sparse lit windows."""
    import random
    rnd = random.Random(26013)
    far = Image.new("L", (w, h), 0)
    near = Image.new("L", (w, h), 0)
    win = Image.new("L", (w, h), 0)
    f, n, wd = ImageDraw.Draw(far), ImageDraw.Draw(near), ImageDraw.Draw(win)

    def tower(d, x, bw, top, crown):
        d.rectangle([x, top, x + bw, base], fill=255)
        if crown == "step":
            d.rectangle([x + bw * .18, top - 18, x + bw * .82, top], fill=255)
            d.rectangle([x + bw * .36, top - 32, x + bw * .64, top - 18], fill=255)
        elif crown == "spire":
            d.polygon([(x + bw * .2, top), (x + bw / 2, top - 46), (x + bw * .8, top)], fill=255)
            d.rectangle([x + bw / 2 - 1.5, top - 80, x + bw / 2 + 1.5, top - 46], fill=255)
        elif crown == "slope":
            d.polygon([(x, top), (x + bw, top - 26), (x + bw, top)], fill=255)
        elif crown == "antenna":
            d.rectangle([x + bw * .7, top - 34, x + bw * .7 + 3, top], fill=255)

    x = -8
    for bw, top, cr in [(38, 352, "antenna"), (30, 398, "step"), (46, 378, "step"), (26, 450, ""), (40, 330, "spire"),
                        (34, 420, "slope"), (48, 395, "step"), (28, 455, ""), (42, 410, "antenna"), (44, 445, "")]:
        tower(f, x, bw, top, cr); x += bw - 4
    x = -6
    for bw, top, cr in [(54, 545, ""), (40, 505, "slope"), (62, 568, ""), (36, 520, "antenna"), (70, 585, ""), (48, 540, "step"), (60, 575, "")]:
        tower(n, x, bw, top, cr)
        for cx in range(int(x) + 8, int(x + bw) - 8, 13):
            for cy in range(top + 14, base - 20, 22):
                if rnd.random() < .22:
                    wd.rectangle([cx, cy, cx + 5, cy + 8], fill=255)
        x += bw - 2
    # water tower on the near roofline
    n.rectangle([150, 512, 176, 540], fill=255); n.polygon([(146, 512), (163, 498), (180, 512)], fill=255)
    n.rectangle([153, 540, 156, 552], fill=255); n.rectangle([170, 540, 173, 552], fill=255)
    win = Image.fromarray(np.minimum(np.asarray(win), np.asarray(near)))
    return far, near, win


def compose(key, size=1440, drop=110):
    P = PLATES[key]
    plate = Image.open(RAW / P["plate"]).convert("RGB")
    pw, ph = plate.size
    s = size / pw

    # 1. skyline painted onto the wall pixels only (multiply, so wall light and shading stay)
    a = np.asarray(plate).astype(np.float32)
    lum = a.mean(2)
    sat = a.max(2) - a.min(2)
    wall = ((lum > 140) & (sat < 34)).astype(np.uint8) * 255
    geo = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(geo).rectangle([0, 0, P["wall_right"], P["baseboard"]], fill=255)
    ImageDraw.Draw(geo).polygon(P["exclude"], fill=0)
    mask = Image.fromarray(np.minimum(wall, np.asarray(geo))).filter(ImageFilter.GaussianBlur(1.2))
    far, near, win = skyline(pw, ph, P["baseboard"])
    # fade toward the TV and toward the top so it reads as a soft wall graphic, like the ref
    fade = np.ones((ph, pw), np.float32)
    xs = np.arange(pw)[None, :]
    fade *= np.clip((P["wall_right"] - 8 - xs) / 30.0, 0, 1)
    tint = np.asarray(plate).astype(np.float32)
    for layer, col, op in [(far, (228, 219, 251), 1.0), (near, (208, 192, 246), 1.0), (win, (246, 242, 255), 0.9)]:
        m = (np.asarray(layer).astype(np.float32) / 255) * (np.asarray(mask).astype(np.float32) / 255) * fade * op
        m = m[..., None]
        mult = tint * (np.array(col, np.float32) / 255) if layer is not win else np.broadcast_to(np.array(col, np.float32), tint.shape)
        tint = tint * (1 - m) + mult * m
    plate = Image.fromarray(tint.clip(0, 255).astype(np.uint8))

    # 2. TV screen: the ad image, cover-fit into the glass, with a faint sheen
    x0, y0, x1, y1 = P["screen_box"]
    scr = Image.open(RAW / P["screen"]).convert("RGB")
    sw, sh = x1 - x0, y1 - y0
    k = max(sw / scr.width, sh / scr.height)
    scr = scr.resize((round(scr.width * k), round(scr.height * k)), Image.LANCZOS)
    scr = scr.crop(((scr.width - sw) // 2, (scr.height - sh) // 2, (scr.width - sw) // 2 + sw, (scr.height - sh) // 2 + sh))
    plate.paste(scr, (x0, y0))

    # 3. scale to the frame, drop the room to open a headline zone, extend the wall upward
    big = plate.resize((size, round(ph * s)), Image.LANCZOS)
    canvas = Image.new("RGB", (size, size))
    top_row = np.asarray(big)[0:6].mean(0)  # wall color per column at the plate's top edge
    ext = np.repeat(top_row[None], drop, 0)
    shade = np.linspace(0.985, 1.0, drop)[:, None, None]  # wall darkens slightly toward the ceiling, as in the plate
    canvas.paste(Image.fromarray((ext * shade).clip(0, 255).astype(np.uint8)), (0, 0))
    canvas.paste(big, (0, drop))
    out = OUT / f"{key}-bg-{size}x{size}.png"
    canvas.save(out)
    box = [round(v * s) for v in (x0, y0, x1, y1)]
    box[1] += drop; box[3] += drop
    return out, box


if __name__ == "__main__":
    for key in (sys.argv[1:] or PLATES):
        out, box = compose(key)
        print(out.name, "screen box at 1440:", box)
