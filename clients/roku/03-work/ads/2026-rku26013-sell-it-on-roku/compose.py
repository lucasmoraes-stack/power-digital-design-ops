"""RKU26013 background compositor, V2 (2026-10-12).

Real layer:  Figma AI room plate with blown-out white window glass (img/raw/<key>-plate-*.png)
             + TV ad image (img/raw/<key>-screen-*.png)
Drawn layer: a pure flat illustration of the city outside (our own drawing, no Roku City art),
             keyed into the glass only. Frames, plant and furniture stay in front of it.
V1 (skyline multiplied onto the wall) is archived in _v1-wallpaper/.

    python -I compose.py [key]     -> img/<key>-bg-1440x1440.png
"""
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
RAW = HERE / "img" / "raw"
OUT = HERE / "img"

PLATES = {
    "pet": {
        "plate": "pet-plate-v2.png", "screen": "pet-screen-v1.png",
        "screen_box": (309, 373, 715, 589),   # TV glass, plate px (1024)
        "window": (18, 168, 1006, 680),       # glass area incl. frames, plate px
        "drop": 200,                          # wall added above the plate at 1440, for the headline
    },
}

# city palette: light purples per the brief, one warm note
SKY_TOP, SKY_BOT = (236, 226, 255), (255, 226, 214)
SUN = (255, 205, 186)
CLOUD = (250, 247, 255)
FAR, MID, NEAR = (214, 198, 252), (176, 148, 246), (128, 92, 226)
LIT = (255, 232, 170)


def city(w, h, seed=26013, ss=2):
    """Flat vector city at w x h (window area). Drawn at ss x then downsampled for clean edges."""
    W, H = w * ss, h * ss
    rnd = random.Random(seed)
    sky = np.zeros((H, W, 3), np.float32)
    t = np.linspace(0, 1, H)[:, None]
    for i in range(3):
        sky[..., i] = SKY_TOP[i] * (1 - t) + SKY_BOT[i] * t
    img = Image.fromarray(sky.astype(np.uint8))
    d = ImageDraw.Draw(img)
    # sun and clouds: flat shapes
    d.ellipse([W * .70, H * .30, W * .70 + H * .26, H * .56], fill=SUN)
    for cx, cy, cw in [(.16, .16, .16), (.55, .10, .12), (.86, .22, .10)]:
        x0, y0, cw, ch = W * cx, H * cy, W * cw, H * .055
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], radius=ch / 2, fill=CLOUD)
        d.ellipse([x0 + cw * .18, y0 - ch * .7, x0 + cw * .55, y0 + ch * .6], fill=CLOUD)
        d.ellipse([x0 + cw * .45, y0 - ch * .45, x0 + cw * .78, y0 + ch * .7], fill=CLOUD)

    def layer(color, base_h, var, wmin, wmax, lit=0.0, details=False):
        x = -rnd.uniform(0, wmin)
        while x < W:
            bw = rnd.uniform(wmin, wmax)
            top = H - (base_h + rnd.uniform(-var, var)) * H
            d.rectangle([x, top, x + bw, H], fill=color)
            kind = rnd.random()
            if details and kind < .22:      # stepped crown
                d.rectangle([x + bw * .2, top - H * .03, x + bw * .8, top], fill=color)
                d.rectangle([x + bw * .38, top - H * .055, x + bw * .62, top], fill=color)
            elif details and kind < .34:    # spire
                d.polygon([(x + bw * .25, top), (x + bw / 2, top - H * .09), (x + bw * .75, top)], fill=color)
                d.rectangle([x + bw / 2 - ss, top - H * .14, x + bw / 2 + ss, top], fill=color)
            elif details and kind < .44:    # water tower
                tx = x + bw * .3
                d.rectangle([tx, top - H * .05, tx + bw * .3, top - H * .02], fill=color)
                d.polygon([(tx - bw * .03, top - H * .05), (tx + bw * .15, top - H * .075), (tx + bw * .33, top - H * .05)], fill=color)
                d.rectangle([tx + bw * .04, top - H * .02, tx + bw * .07, top], fill=color)
                d.rectangle([tx + bw * .23, top - H * .02, tx + bw * .26, top], fill=color)
            elif details and kind < .52:    # antenna
                d.rectangle([x + bw * .7, top - H * .06, x + bw * .7 + ss * 1.5, top], fill=color)
            if lit:
                cw, chh = max(3 * ss, bw * .09), H * .018
                for wx in np.arange(x + bw * .15, x + bw * .85 - cw, cw * 2.2):
                    for wy in np.arange(top + H * .03, H - chh, chh * 2.4):
                        if rnd.random() < lit:
                            d.rectangle([wx, wy, wx + cw, wy + chh], fill=LIT)
            x += bw + rnd.uniform(-bw * .15, bw * .05)

    layer(FAR, .56, .12, W * .035, W * .07, details=True)
    layer(MID, .40, .10, W * .045, W * .085, lit=.10, details=True)
    layer(NEAR, .22, .07, W * .06, W * .11, lit=.18, details=True)
    return img.resize((w, h), Image.LANCZOS)


def compose(key, size=1440):
    P = PLATES[key]
    plate = Image.open(RAW / P["plate"]).convert("RGB")
    pw, ph = plate.size
    a = np.asarray(plate).astype(np.float32)

    # 1. key the blown-out glass and put the illustration behind it
    x0, y0, x1, y1 = P["window"]
    # soft key: how much of each pixel is the white glass (1 = pure glass). Edge pixels (leaves, fur,
    # TV rim) are part glass, so we remove that share of white and add the same share of the city.
    mn = a.min(2)
    sat = a.max(2) - mn
    k = np.clip((mn - 208) / (248 - 208), 0, 1) * np.clip((24 - sat) / 12, 0, 1)
    region = np.zeros(k.shape, np.float32); region[y0:y1, x0:x1] = 1
    for poly in P.get("protect", []):
        pm = Image.new("L", (pw, ph), 0); ImageDraw.Draw(pm).polygon(poly, fill=255)
        region *= 1 - np.asarray(pm, np.float32) / 255
    k = (k * region)[..., None]
    art = np.full_like(a, 255)
    art[y0:y1, x0:x1] = np.asarray(city(x1 - x0, y1 - y0)).astype(np.float32)
    a = a + k * (art - 255)

    # 2. TV ad on the glass
    sx0, sy0, sx1, sy1 = P["screen_box"]
    scr = Image.open(RAW / P["screen"]).convert("RGB")
    sw, sh = sx1 - sx0, sy1 - sy0
    k = max(sw / scr.width, sh / scr.height)
    scr = scr.resize((round(scr.width * k), round(scr.height * k)), Image.LANCZOS)
    scr = scr.crop(((scr.width - sw) // 2, (scr.height - sh) // 2, (scr.width - sw) // 2 + sw, (scr.height - sh) // 2 + sh))
    a[sy0:sy1, sx0:sx1] = np.asarray(scr).astype(np.float32)

    # 3. scale, drop the room, extend the wall upward for the headline
    s = size / pw
    big = Image.fromarray(a.clip(0, 255).astype(np.uint8)).resize((size, round(ph * s)), Image.LANCZOS)
    drop = P["drop"]
    canvas = Image.new("RGB", (size, size))
    top_row = np.asarray(big)[2:8].mean(0)
    canvas.paste(Image.fromarray(np.repeat(top_row[None], drop, 0).clip(0, 255).astype(np.uint8)), (0, 0))
    canvas.paste(big, (0, drop))
    out = OUT / f"{key}-bg-{size}x{size}.png"
    canvas.save(out)
    box = [round(v * s) for v in P["screen_box"]]
    box[1] += drop; box[3] += drop
    win = [round(v * s) for v in P["window"]]
    win[1] += drop; win[3] += drop
    return out, box, win


if __name__ == "__main__":
    for key in (sys.argv[1:] or PLATES):
        out, box, win = compose(key)
        print(out.name, "screen", box, "window", win)
