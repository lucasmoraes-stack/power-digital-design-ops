"""Render RKU26012 frames with headless Chromium (Playwright) and encode with ffmpeg.

    python -I render.py stills 16x9 1x1        -> review/<size>-t<sec>.png at the beat times
    python -I render.py video 16x9 [fps]       -> export/RKU26012-...-Animation-....mp4 (HyperFrames)
    python -I render.py video all
"""
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from anim import CANVAS, PLAT, SIZES  # noqa: E402

BUILD, EXPORT, REVIEW = HERE / "hf" / "compositions", HERE / "export", HERE / "review"
STILLS = [1.4, 3.3, 4.8, 7.4, 8.6, 9.8, 12.4, 14.2, 15.1, 16.6, 19.0]
VER = "V2"


def fname(size):
    return f"RKU26012-TVAdvertising3Steps-{CANVAS[size]}-Animation-{PLAT[size]}-20s-{VER}"


def open_page(p, size):
    S = SIZES[size]
    b = p.chromium.launch(channel="chrome", args=["--allow-file-access-from-files", "--force-color-profile=srgb"])
    pg = b.new_page(viewport={"width": S["W"], "height": S["H"]}, device_scale_factor=1)
    pg.goto((BUILD / f"{size}.html").as_uri())
    pg.evaluate("window.ready")
    pg.wait_for_timeout(300)
    return b, pg


def stills(sizes, times=STILLS):
    REVIEW.mkdir(exist_ok=True)
    with sync_playwright() as p:
        for size in sizes:
            b, pg = open_page(p, size)
            for t in times:
                pg.evaluate(f"seek({t})")
                pg.screenshot(path=str(REVIEW / f"{size}-t{t:05.2f}.png"), clip={"x": 0, "y": 0, "width": SIZES[size]["W"], "height": SIZES[size]["H"]})
            b.close()
            print(size, "stills")


def video(size, fps=30, dur=20.0):
    """Final MP4 through HyperFrames (Apache 2.0, local Chrome + FFmpeg, parallel workers)."""
    EXPORT.mkdir(exist_ok=True)
    out = EXPORT / f"{fname(size)}.mp4"
    npx = "npx.cmd" if sys.platform == "win32" else "npx"
    subprocess.run([npx, "hyperframes", "render", "-c", f"compositions/{size}.html", "-q", "delivery", "-f", str(fps),
                    "--quiet", "-o", str(out)], cwd=HERE / "hf", check=True)
    print(out.name)


if __name__ == "__main__":
    mode, args = sys.argv[1], sys.argv[2:]
    sizes = list(SIZES) if not args or args[0] == "all" else [a for a in args if a in SIZES]
    if mode == "stills":
        stills(sizes)
    else:
        fps = int(args[-1]) if args and args[-1].isdigit() else 30
        for s in sizes:
            video(s, fps)
