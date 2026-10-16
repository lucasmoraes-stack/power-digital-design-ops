"""Stills review sheet (beats) for one reel: python sheet.py 07 [cols]"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

R = Path(__file__).resolve().parent / "review"
SAFE = (90, 250, 990, 1580)   # Reels safe area, drawn as a thin guide on the sheet


def sheet(vid, cols=6):
    fs = sorted(R.glob(f"{vid}-t*.png"))
    ims = [Image.open(f).convert("RGB") for f in fs]
    w = 360
    h = round(ims[0].height * w / ims[0].width)
    k = w / ims[0].width
    rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (cols * w + (cols + 1) * 10, rows * (h + 34) + 10), "#1b1b1b")
    d = ImageDraw.Draw(sh)
    for i, (f, im) in enumerate(zip(fs, ims)):
        x, y = 10 + (i % cols) * (w + 10), 10 + (i // cols) * (h + 34)
        sh.paste(im.resize((w, h), Image.LANCZOS), (x, y + 24))
        d.rectangle([x + SAFE[0] * k, y + 24 + SAFE[1] * k, x + SAFE[2] * k, y + 24 + SAFE[3] * k], outline="#30C0FF")
        d.text((x, y + 6), f.stem.replace(f"{vid}-t", f"{vid} · t=") + " s", fill="#ddd")
    p = R / f"_sheet-{vid}.jpg"
    sh.save(p, quality=88)
    return p


if __name__ == "__main__":
    print(sheet(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 6))
