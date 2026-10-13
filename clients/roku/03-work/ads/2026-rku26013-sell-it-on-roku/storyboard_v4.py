"""RKU26013 CTV spot storyboard + animatic on the V4 rooms (2026-10-13).

Same beats and timing as storyboard.py (V3), but every frame uses the industry's V4 ChatGPT room
(v4.keyed: city keyed, ad on the TV). The six rooms share one camera, window, TV and furniture,
so between frames only the props, the TV ad and the industry word change. The panel keeps the
Wellness width for the whole spot so the split never jumps. Frame F01 shows the TV off (the lit
screen is replaced by the black glass).

    python -I storyboard_v4.py
"""
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import split  # noqa: E402
import v4  # noqa: E402
from storyboard import FRAMES  # noqa: E402

PFX = "RKU26013-SellItOnRoku-2560x1440-Storyboard-CTV"
EXPORT = split.EXPORT


def plate(ind, tv_on=True):
    im, scr = v4.keyed(ind)
    if tv_on:
        return im, scr
    a = np.asarray(im).astype(np.float32).copy()
    x0, y0, x1, y1 = scr
    h = y1 - y0
    glass = np.linspace(26, 12, h)[:, None, None] * np.ones((1, x1 - x0, 3))   # switched-off glass,
    glass[..., 2] += 4                                                         # faint cool sheen at the top
    a[y0:y1, x0:x1] = glass
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)), scr


def main():
    split.BG, split.BUILD = v4.BG, v4.BUILD
    split.plate = plate
    pw = int(re.search(r'class="p" style="width:(\d+)px',
                       (v4.BUILD / "wellness-16x9.html").read_text(encoding="utf8")).group(1))
    out = []
    for n, (ind, t0, hold, opts, scene, action) in enumerate(FRAMES, 1):
        name = f"{PFX}-F{n:02d}-V4"
        png = split.build(ind, name=f"storyboard-F{n:02d}.html", png_name=f"{name}.png", panel=pw, **opts)
        out.append((name, png, hold))
        print(name, f"{t0:.1f}s", scene)
    xf, args, chain, off, last = 0.4, [], [], 0.0, "0"
    for i, (_, png, hold) in enumerate(out):
        args += ["-loop", "1", "-t", f"{hold + (xf if i < len(out) - 1 else 0):.2f}", "-framerate", "30", "-i", str(png)]
    for i in range(1, len(out)):
        off += out[i - 1][2]
        chain.append(f"[{last}][{i}]xfade=transition=fade:duration={xf}:offset={off:.2f}[v{i}]")
        last = f"v{i}"
    mp4 = EXPORT / "RKU26013-SellItOnRoku-2560x1440-Animatic-CTV-AllIndustries-V4.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args, "-filter_complex", ";".join(chain) + f";[{last}]format=yuv420p",
                    "-c:v", "libx264", "-crf", "18", "-r", "30", str(mp4)], check=True)
    print(mp4.name)


if __name__ == "__main__":
    main()
