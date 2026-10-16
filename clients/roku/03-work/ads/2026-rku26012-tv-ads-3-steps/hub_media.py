"""Media for the Roku Deliverables Hub view #rku26012.

    python -I hub_media.py   -> review/sb/*.jpg (storyboard, posters, Victor refs) + review/preview/<size>.mp4
Run render.py stills all and render.py video all first.
"""
import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
REVIEW, EXPORT = HERE / "review", HERE / "export"
INBOX = HERE.parents[2] / "00-inbox" / "2026-10-15-rku26012-concept"
SB, PRE = REVIEW / "sb", REVIEW / "preview"


def jpg(src, dst, w):
    im = Image.open(src).convert("RGB")
    im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(dst, quality=84, optimize=True)


def main():
    SB.mkdir(parents=True, exist_ok=True); PRE.mkdir(parents=True, exist_ok=True)
    # storyboard cards = the delivered storyboard frames (camera guide included), 16:9
    for f in sorted((HERE.parents[2] / "04-deliverables" / "ads" / HERE.name / "storyboard" / "16x9").glob("*-F??-*.png")):
        jpg(f, SB / f"16x9-{f.stem.split('-')[-2]}.jpg", 960)
    for size, w in [("16x9", 960), ("1x1", 600), ("4x5", 520), ("9x16", 420)]:
        jpg(REVIEW / f"{size}-t04.80.png", SB / f"{size}-poster.jpg", w)
        src = sorted(EXPORT.glob(f"*-{ {'16x9': '1920x1080', '1x1': '1440x1440', '4x5': '1440x1800', '9x16': '1440x2560'}[size]}-*.mp4"))[-1]
        vw = {"16x9": 1280, "1x1": 720, "4x5": 720, "9x16": 540}[size]
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", f"scale={vw}:-2:flags=lanczos",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "25", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an",
                        str(PRE / f"{size}.mp4")], check=True)
    for n, f in [("budget", "victor-ai-ref-step1-budget.png"), ("audience", "victor-ai-ref-step2-audience.png"), ("upload", "victor-ai-ref-step3-upload.png")]:
        jpg(INBOX / f, SB / f"ref-{n}.jpg", 720)
    for f in sorted(PRE.glob("*.mp4")):
        print(f.name, round(f.stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
