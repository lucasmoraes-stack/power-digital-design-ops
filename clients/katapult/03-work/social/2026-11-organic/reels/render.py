"""Render the Katapult November reels.

    python render.py stills 07 15        -> review/<id>-t<sec>.png at the beats + review/_sheet-<id>.jpg
    python render.py video 07 15         -> 04-deliverables/.../reels/<slug>_reel-9x16.mp4 (HyperFrames) + poster .png
    python render.py storyboard 07 15    -> 04-deliverables/.../png/<slug>/<slug>_reel-storyboard-9x16_NN.png
    python render.py frames 07 4.9 5.6   -> review/frames-<id>/ frames pulled from the MP4 with ffmpeg (transition check)

HyperFrames telemetry is off (HYPERFRAMES_NO_TELEMETRY=1, DO_NOT_TRACK=1, and ~/.hyperframes/config.json).
"""
import os
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from anim import BUILD, H, VIDEOS, W  # noqa: E402

REVIEW = HERE / "review"
EXPORT = HERE.parents[3] / "04-deliverables" / "social" / "2026-11-organic" / "reels"
STILLS = {
    "07": [.9, 2.2, 2.8, 3.6, 4.4, 5.2, 5.6, 6.9, 7.8, 8.4, 9.25, 9.8, 10.6, 11.6, 12.3, 14.5],
    "15": [1.15, 2.3, 3.6, 4.9, 6.2, 7.5, 10.5],
}
POSTER = {"07": 4.6, "15": 10.5}
# storyboard: one key frame per beat (where the beat reads best); see png/<post>/storyboard.md
BOARD = {"07": [2.2, 4.6, 8.4, 10.2, 11.8, 14.5], "15": [1.15, 2.3, 3.6, 4.9, 6.2, 7.5, 10.5]}
PNG = HERE.parents[3] / "04-deliverables" / "social" / "2026-11-organic" / "png"
ENV = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1")


def out_path(vid, ext):
    return EXPORT / f"{VIDEOS[vid]['slug']}_reel-9x16.{ext}"


def shoot(vid, times, dest):
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", args=["--allow-file-access-from-files", "--force-color-profile=srgb"])
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto((BUILD / f"{vid}.html").as_uri())
        pg.evaluate("window.ready")
        pg.wait_for_timeout(300)
        for t, path in zip(times, dest):
            pg.evaluate(f"seek({t})")
            pg.screenshot(path=str(path), clip={"x": 0, "y": 0, "width": W, "height": H})
        b.close()


def stills(vid):
    REVIEW.mkdir(exist_ok=True)
    for f in REVIEW.glob(f"{vid}-t*.png"):
        f.unlink()
    ts = STILLS[vid]
    shoot(vid, ts, [REVIEW / f"{vid}-t{t:05.2f}.png" for t in ts])
    from sheet import sheet
    print(sheet(vid))


def video(vid):
    EXPORT.mkdir(parents=True, exist_ok=True)
    out = out_path(vid, "mp4")
    npx = "npx.cmd" if sys.platform == "win32" else "npx"
    subprocess.run([npx, "hyperframes", "render", "-c", f"compositions/{vid}.html", "-q", "delivery", "-f", "30",
                    "--quiet", "-o", str(out)], cwd=HERE / "hf", check=True, env=ENV)
    shoot(vid, [POSTER[vid]], [out_path(vid, "png")])
    print(out.name)


def storyboard(vid):
    d = PNG / VIDEOS[vid]["slug"]
    d.mkdir(parents=True, exist_ok=True)
    ts = BOARD[vid]
    shoot(vid, ts, [d / f"{VIDEOS[vid]['slug']}_reel-storyboard-9x16_{i + 1:02d}.png" for i in range(len(ts))])
    print(d)


def frames(vid, a, b, fps=15):
    d = REVIEW / f"frames-{vid}"
    d.mkdir(parents=True, exist_ok=True)
    for f in d.glob(f"{a:05.2f}-*.png"):
        f.unlink()
    subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-to", str(b), "-i", str(out_path(vid, "mp4")),
                    "-vf", f"fps={fps},scale=270:-1,tile=8x2", str(d / f"{a:05.2f}-%02d.png")], check=True)
    print(d)


if __name__ == "__main__":
    mode, args = sys.argv[1], sys.argv[2:]
    if mode == "frames":
        frames(args[0], float(args[1]), float(args[2]))
    else:
        for v in [a for a in args if a in VIDEOS] or list(VIDEOS):
            {"stills": stills, "video": video, "storyboard": storyboard}[mode](v)
