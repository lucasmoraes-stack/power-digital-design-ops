"""Builder B: prepare images for posts 03, 06, 09, 10, 12, 13, 14 into build/img/ (prefix b-).
Cutouts: trimmed to alpha bbox, max 1000px. Photos: resized to max 1800px long edge."""
import pathlib
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[6]  # repo root
K = ROOT / "clients/katapult"
OUT = pathlib.Path(__file__).parent / "img"
FIG = pathlib.Path(r"C:/Users/lucas/AppData/Local/Temp/claude/c--Users-lucas-OneDrive-Desktop-VAZIO-power-digital-ops/94ca49aa-5d72-4c5b-9379-1bead8075d5a/scratchpad/figdl")
STUDIO = K / "03-work/claude-project-social/studio/assets/products"
LIB = K / "01-brand/photos/library"
cutouts = {  # October finals (Figma raw images) and Studio set
    "b-fridge": FIG / "a01_6", "b-monitor": FIG / "a01_1", "b-couch-green": FIG / "a03s4_3",
    "b-headphones": FIG / "a03s4_7", "b-tablets": FIG / "a03s4_8", "b-tire-stack": FIG / "a11_3",
    "b-bed": FIG / "a11_6", "b-armchair-pink": FIG / "a11_7", 
    "b-tv": STUDIO / "tv.webp", "b-washer": STUDIO / "washer.webp", "b-tire": STUDIO / "tire.webp",
    "b-laptop-open": STUDIO / "laptop-open.webp", "b-nightstand": STUDIO / "nightstand.webp",
}
photos = ["together-couple-sofa-phone-laptop-01", "together-friends-cooking-07", "together-family-homework-sofa-03",
          "together-couple-tablet-mug-05", "phone-man-call-tablet-sofa-06", "at-home-woman-dishwasher-05"]  # ai-*.jpg in img/ are generated, not prepped here
for name, src in cutouts.items():
    if not src.exists(): print("missing", src); continue
    im = Image.open(src).convert("RGBA")
    a = im.getchannel("A").point(lambda v: 255 if v > 8 else 0)
    im = im.crop(a.getbbox()); im.thumbnail((1000, 1000), Image.LANCZOS)
    im.save(OUT / f"{name}.png", optimize=True); print(name, im.size)
for p in photos:
    im = Image.open(LIB / f"{p}.jpg").convert("RGB"); im.thumbnail((1800, 1800), Image.LANCZOS)
    im.save(OUT / f"b-{p}.jpg", quality=88); print(p, im.size)
