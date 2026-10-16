"""Contact sheet of review stills: python -I sheet.py <size> [cols]"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
R = Path(__file__).resolve().parent / "review"
size = sys.argv[1]; cols = int(sys.argv[2]) if len(sys.argv) > 2 else 4
fs = sorted(R.glob(f"{size}-t*.png"))
ims = [Image.open(f).convert("RGB") for f in fs]
w = 640; h = round(ims[0].height * w / ims[0].width)
rows = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (cols * w + (cols + 1) * 8, rows * (h + 30) + 8), "#111")
d = ImageDraw.Draw(sh)
for i, (f, im) in enumerate(zip(fs, ims)):
    x, y = 8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 30)
    sh.paste(im.resize((w, h), Image.LANCZOS), (x, y + 22)); d.text((x, y + 4), f.stem, fill="#ddd")
sh.save(R / f"_sheet-{size}.jpg", quality=88); print(R / f"_sheet-{size}.jpg")
