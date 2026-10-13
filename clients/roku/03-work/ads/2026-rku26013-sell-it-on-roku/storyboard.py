"""RKU26013 CTV spot storyboard (15 s, 2560x1440, split layout), 2026-10-12.

One frame per beat, built with split.py on ONE static room for the whole spot (spot.py: same
camera, window, TV and furniture; only the props on the coffee table and the TV ad change, so
nothing jumps between frames; Lucas, 2026-10-12). The panel
keeps one width for the whole spot (the widest headline, Wellness) so the split never jumps when
the industry word swaps. Each frame is a static HTML for Figma import plus a PNG; the animatic MP4
is cut from the frames on the storyboard timing.

    python -I storyboard.py
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import split  # noqa: E402
from split import BUILD, EXPORT, IND, build  # noqa: E402

split.PLATE = "spot-plate-{ind}.png"   # one static room for the whole spot (spot.py)

PFX = "RKU26013-SellItOnRoku-2560x1440-Storyboard-CTV"

# (industry, start s, hold s, build options, scene, action)
FRAMES = [
    ("pet", 0.0, 1.0, dict(show=1, cta="off", tv_on=False), "Open",
     "The living room fades up, TV off. The panel slides in from the left and 'Put your' writes on. The room stays locked for the whole spot: same camera, window, TV and furniture."),
    ("pet", 1.0, 2.0, dict(), "TV on · Pet",
     "The TV switches on and the pet ad plays. 'pet brand' drops in, then 'in their living room.' line by line. Learn more pops in. The rope toy and food bowl are on the table. Window lights in the city start to blink on."),
    ("beauty", 3.0, 2.4, dict(), "Beauty",
     "Word swap: 'pet brand' slides up and out, 'beauty brand' slides in. Only the table props swap (a quick dissolve to the skincare tray and candle) and the TV cuts to the beauty ad. Room, panel and the rest of the headline hold still."),
    ("food", 5.4, 2.4, dict(), "Food & Bev",
     "Same swap: 'products', breakfast props on the table and the Food & Bev ad. Steam rises from the cups (subtle loop)."),
    ("wellness", 7.8, 2.4, dict(), "Wellness",
     "Same swap: 'wellness brand', bottle, dumbbells and fruit bowl on the table, and the Wellness ad."),
    ("tech", 10.2, 2.4, dict(), "Tech",
     "Same swap: 'latest tech', tablet, controller, watch and box on the table, and the tech ad."),
    ("home", 12.6, 1.6, dict(), "Home",
     "Same swap: 'home brand', lilac vase, books and candle on the table, and the Homegoods ad. The candle flickers."),
    ("home", 14.2, 0.8, dict(cta="pressed"), "End · Learn more",
     "Learn more presses in and glows. Hold to the end of the spot."),
]


def panel_width():
    t = (BUILD / "wellness-16x9.html").read_text(encoding="utf8")
    return int(re.search(r'class="p" style="width:(\d+)px', t).group(1))


def main():
    pw = panel_width()
    out = []
    for n, (ind, t0, hold, opts, scene, action) in enumerate(FRAMES, 1):
        name = f"{PFX}-F{n:02d}-V3"
        png = build(ind, name=f"storyboard-F{n:02d}.html", png_name=f"{name}.png", panel=pw, **opts)
        out.append((name, png, ind, t0, hold, scene, action))
        print(name, f"{t0:.1f}s", scene)
    # animatic on the storyboard timing: hold each frame, 0.4 s crossfades
    xf, args, chain, off, last = 0.4, [], [], 0.0, "0"
    for i, (_, png, *_r) in enumerate(out):
        hold = out[i][4] + (xf if i < len(out) - 1 else 0)
        args += ["-loop", "1", "-t", f"{hold:.2f}", "-framerate", "30", "-i", str(png)]
    for i in range(1, len(out)):
        off += out[i - 1][4]
        lab = f"v{i}"
        chain.append(f"[{last}][{i}]xfade=transition=fade:duration={xf}:offset={off:.2f}[{lab}]")
        last = lab
    mp4 = EXPORT / "RKU26013-SellItOnRoku-2560x1440-Animatic-CTV-AllIndustries-V3.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args, "-filter_complex", ";".join(chain) + f";[{last}]format=yuv420p",
                    "-c:v", "libx264", "-crf", "18", "-r", "30", str(mp4)], check=True)
    return out, mp4


if __name__ == "__main__":
    main()
