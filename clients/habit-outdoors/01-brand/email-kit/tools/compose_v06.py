"""compose_v06.py - Habit Outdoors email kit v0.6 draft (2026-10-07): what the November 2026 batch taught.

Run:  python compose_v06.py                 (all jobs)
      python compose_v06.py copy edges      (some jobs)

Jobs
  copy    copy the November composites the v0.6 modules use (E35-E41) into ../assets/ under e35-...e41- names.
          They are built by 03-work/email/2026-11-broadcasts/compose_assets.py (the generator of record: seam_check,
          border_window, floor_shadow, phased edges); rerun that script to swap a product or photo, then this job.
  edges   regenerate every E18 textured edge of v0.4 and v0.5 (edge-tex-*.jpg, + -dm) with the FINE crumbs of the
          November batch (radius 0.6-1.3 px at 2x, 0.5-4.5 px above the line: the rev-oct-03 paper grain) instead of
          the 2.4-4.4 px dots up to 10 px above the line (QA r1 of the November batch). Same textures, same seeds,
          same torn line, same file names: only the crumbs change.
  packs   rewrite the palette (P mode) packshot PNGs as PNG-24 (RGBA) where the file stays under 90 KB; the heavy
          ones are reported and left as they are (open item in the README: they need a JPG on the band + -dm twin).

compose.py and compose_v05.py are imported read-only (not modified).
"""
from __future__ import annotations

import random
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compose as C  # noqa: E402
import compose_v05 as V  # noqa: E402,F401  (registers paper-camo, halftone-brown and the v0.5 gradient)

ASSETS = HERE.parent / "assets"
NOV = HERE.parents[2] / "03-work/email/2026-11-broadcasts/assets"

# kit name <- November file (module, what it is)
COPY = [
    ("e35-hero-group-womens-cedar-branch.jpg", "n1-hero-group.jpg"),       # E35 grouped product hero (Ivy grain)
    ("e36-hero-collage-field-water.jpg", "n2-hero-collage.jpg"),            # E36 framed collage hero, torn into Patriot water
    ("e37-hero-model-buck-hollow.jpg", "n3-hero-model.jpg"),                # E37 split hero, store model cut-out
    ("e37-edge-tapshoe-paperlight.jpg", "n3-edge-tapshoe-paper.jpg"),       # E37 E18 edge phased to the E37 band height
    ("e37-edge-tapshoe-paperlight-dm.jpg", "n3-edge-tapshoe-paper-dm.jpg"),
    ("e38-system-buck-hollow.jpg", "n3-system.jpg"),                        # E38 system shot on light paper
    ("e38-system-buck-hollow-dm.jpg", "n3-system-dm.jpg"),
    ("e39-mosaic-stable.jpg", "n4-m-stable.jpg"),                           # E39 straight detail mosaic
    ("e39-mosaic-pleat.jpg", "n4-m-pleat.jpg"),
    ("e39-mosaic-pocket.jpg", "n4-m-pocket.jpg"),
    ("e39-colourways-flannel.jpg", "n4-pair.jpg"),                          # E39 colourways side by side (Aluminum panel)
    ("e40-card-insulated-boot.jpg", "n2-card-5.jpg"),                       # E40 2-up vertical card (Ivy panel)
    ("e40-card-stocking-cap.jpg", "n2-card-6.jpg"),                         # E40 (Dusk panel)
    ("e41-row-siesta-cape-tee.jpg", "n5-under30-2.jpg"),                    # E41 price-tier rows (flat panels)
    ("e41-row-camo-gloves.jpg", "n5-under30-4.jpg"),
    ("e41-row-3-season-bomber.jpg", "n5-under100-1.jpg"),
]


def job_copy():
    print("v0.6 assets copied from the November batch")
    total = 0
    for dst, src in COPY:
        s = NOV / src
        d = ASSETS / dst
        shutil.copyfile(s, d)
        im = Image.open(d)
        kb = d.stat().st_size / 1024
        total += kb
        print(f"  {dst:42s} {im.size[0]}x{im.size[1]}  {im.mode}  {kb:6.1f} KB  <- {src}")
    print(f"  total {total:.1f} KB")


# ---------------------------------------------------------------- fine crumbs (November recipe)

def fine_crumbs(canvas: Image.Image, ys, up_rgb, lo_rgb, seed: int, y_off: int = 0, n: int = 70):
    """Fine paper crumbs along a tear (rev-oct-03 grain): dots of the lower sheet's colour 0.5-4.5 px above
    the line, a few of the upper sheet's colour 1-4 px below it. Radius 0.6-1.3 px at 2x."""
    rnd, d = random.Random(seed), ImageDraw.Draw(canvas)
    W = canvas.width
    lo = tuple(int(v) for v in lo_rgb) + (255,)
    up = tuple(int(v) for v in up_rgb) + (255,)
    for _ in range(n):
        x = rnd.randrange(W)
        y = y_off + ys[x] - rnd.uniform(0.5, 4.5)
        r = rnd.choice((0.6, 0.8, 1.0, 1.3))
        d.ellipse((x - r, y - r, x + r, y + r), fill=lo)
    for _ in range(n // 3):
        x = rnd.randrange(W)
        y = y_off + ys[x] + rnd.uniform(1.0, 4.0)
        r = rnd.choice((0.6, 0.8, 1.0))
        d.ellipse((x - r, y - r, x + r, y + r), fill=up)


def torn_edge_fine(top: str, bottom: str, out: str, h: int = 80, seed: int = 3, dm: dict | None = None):
    """compose.compose_torn_edge_textured with the fine crumbs: identical textures, torn line and shadow."""
    seam = h * 0.45
    variants = [("", top, bottom)]
    if dm:
        variants.append(("-dm", dm.get("top", top), dm.get("bottom", bottom)))
    for suffix, tname, bname in variants:
        up = C.tile_rows(tname, h, end=True)
        lo = C.tile_rows(bname, h, end=C._continues(bname))
        ys = C.torn_line(C.TEX_W, seam, amp=8, seed=seed)
        m = Image.new("L", (C.TEX_W, h), 0)
        ImageDraw.Draw(m).polygon([(0, h)] + [(x, y) for x, y in enumerate(ys)] + [(C.TEX_W, h)], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(0.8))
        a = np.asarray(m, np.float32)[:, :, None] / 255
        up = up.copy()
        up_rgb = np.median(up.reshape(-1, 3), 0)
        C.tear_shadow(up, ys)
        canvas = C.to_image(up * (1 - a) + lo * a)
        fine_crumbs(canvas, ys, up_rgb, np.median(lo.reshape(-1, 3), 0), seed + 1)
        p = C.save_jpg_under(canvas, ASSETS / out.replace(".jpg", f"{suffix}.jpg"), 30 * 1024, q=76, subsampling=0)
        print(f"  {p.name:46s} {p.stat().st_size / 1024:5.1f} KB  {tname} / {bname}")


def job_edges():
    print("E18 textured edges, fine crumbs (v0.4 + v0.5 sets, same seeds)")
    for i, (top, bottom, dm) in enumerate(C.EDGES_V04):
        swap = lambda n: "paper-light-dm" if n == "paper-light" else n
        torn_edge_fine(top, bottom, C.edge_name(top, bottom), seed=30 + i,
                       dm={"top": swap(top), "bottom": swap(bottom)} if dm else None)
    v05 = (("paper-tapshoe", "paper-camo", True), ("paper-camo", "paper-tapshoe", True),
           ("halftone-brown", "paper-tapshoe", False), ("paper-tapshoe", "halftone-brown", False),
           ("halftone-brown", "flat:#2A2B2D", False))
    for i, (top, bottom, dm) in enumerate(v05):
        swap = lambda n: "paper-camo-dm" if n == "paper-camo" else n
        short = lambda n: "footer" if n.startswith("flat:") else n.replace("paper-", "paper").replace("-brown", "brown").replace("-", "")
        torn_edge_fine(top, bottom, f"edge-tex-{short(top)}-{short(bottom)}.jpg", seed=300 + i,
                       dm={"top": swap(top), "bottom": swap(bottom)} if dm else None)


# ---------------------------------------------------------------- PNG-24 packshots

PACKS = [  # (file, store packshot, px, pad)  same recipe as compose.product_png, without quantize
    ("pack-mens-heavyweight-soft-flannel-200.png", "mens-heavyweight-soft-flannel", 200, 0.03),
    ("pack-mens-crater-valley-full-zip-200.png", "mens-crater-valley-full-zip-fleece-jacket", 200, 0.03),
    ("pack-mens-cedar-branch-bib-400.png", "mens-cedar-branch-insulated-bib", 400, 0.03),
    ("pack-mens-heavyweight-soft-flannel-360.png", "mens-heavyweight-soft-flannel", 360, 0.03),
    ("pack-mens-cedar-branch-parka-400.png", "habit-mens-cedar-branch-insulated-waterproof-parka", 400, 0.03),
    ("e23-crater-valley-hoodie.png", "mens-crater-valley-performance-hoodie-2", 800, 0.04),
    ("e23-cedar-branch-bib.png", "mens-cedar-branch-insulated-bib", 800, 0.04),
]
PNG24_LIMIT = 90 * 1024


def job_packs():
    import io
    print("palette packshots -> PNG-24 where it stays under 90 KB")
    for out, src, px, pad in PACKS:
        im = C.load_packshot(src)
        inner = round(px * (1 - pad * 2))
        im = C.fit(im, h=inner) if im.height >= im.width else C.fit(im, w=inner)
        cv = Image.new("RGBA", (px, px), (0, 0, 0, 0))
        cv.alpha_composite(im, ((px - im.width) // 2, (px - im.height) // 2))
        buf = io.BytesIO()
        cv.save(buf, "PNG", optimize=True)
        kb = len(buf.getvalue()) / 1024
        if len(buf.getvalue()) <= PNG24_LIMIT:
            (ASSETS / out).write_bytes(buf.getvalue())
            print(f"  {out:46s} PNG-24  {kb:6.1f} KB  rewritten")
        else:
            print(f"  {out:46s} PNG-24 would be {kb:6.1f} KB: LEFT AS PALETTE (open item)")


JOBS = {"copy": job_copy, "edges": job_edges, "packs": job_packs}

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(JOBS)):
        JOBS[k]()
