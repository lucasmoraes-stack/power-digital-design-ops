"""RKU26013 CTV spot: one static room for the whole spot (Lucas, 2026-10-12: no jumps or framing
breaks between storyboard frames; only the scene props and the TV change).

Base room: img/raw/spot-plate-base.png (Figma AI, same style as the industry plates, empty coffee
table and armchair, TV off, blown-out glass). For each industry the props are cut out of its own
1x1 plate (GrabCut on a hand-set rectangle, edges refined with closed-form matting, colours
unmixed with estimate_foreground_ml), given a soft contact shadow and placed on the base table.
The result img/raw/spot-plate-<ind>.png then goes through the normal pipeline (glass key, city,
TV ad) in split.py.

    python -I spot.py            -> all industries + img/review/spot-props.jpg contact sheet
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from pymatting import estimate_alpha_cf, estimate_foreground_ml

HERE = Path(__file__).resolve().parent
RAW = HERE / "img" / "raw"
BASE = RAW / "spot-plate-base.png"

# industry: list of (source rect x0,y0,x1,y1 in its 1x1 plate, scale, target bottom-centre x,y on base)
# Items are listed back to front; each anchor is where the item's base sits on the base table
# (table top spans about x 40-620, y 690 back to 805 front at the centre).
S = 1.25
PROPS = {
    "pet":      [((40, 752, 272, 806), 1.3, (320, 770))],
    "beauty":   [((86, 676, 312, 824), S, (330, 795))],     # tray (the lavender vase didn't cut cleanly)
    "food":     [((488, 675, 578, 735), S, (505, 748)),     # cup, right
                 ((355, 650, 452, 714), S, (395, 742)),     # pastry box
                 ((175, 662, 357, 752), S, (240, 772)),     # croissant basket
                 ((366, 702, 452, 762), S, (420, 780)),     # berries
                 ((276, 720, 380, 793), S, (335, 800)),     # cup, front
                 ((176, 758, 306, 816), S, (200, 806))],    # napkin
    "wellness": [((330, 712, 452, 798), 1.3, (420, 780), (345, 758, 438, 792)),   # fruit bowl
                 ((162, 668, 214, 802), 1.3, (215, 785)),   # bottle
                 ((216, 745, 330, 822), 1.3, (300, 800))],  # dumbbells
    "tech":     [((252, 708, 402, 790), S, (450, 768)),     # box
                 ((0, 748, 150, 812), S, (180, 790)),       # tablet
                 ((148, 762, 258, 818), S, (320, 795)),     # controller
                 ((212, 803, 292, 846), S, (380, 805))],    # watch
    "home":     [((110, 560, 275, 750), S, (240, 780), (190, 665, 262, 742)),   # lilac vase
                 ((268, 660, 436, 774), S, (410, 790), (342, 668, 376, 712))],  # books and candle
}
# wood-coloured pixels above this plate row are background for sure (sideboard, floor, table top);
# not for Pet, whose dog-food bowl is wood
WOOD_ABOVE = {"beauty": 690, "food": 2000, "home": 2000, "wellness": 2000, "tech": 2000}
# extras placed off the table: the dog on the armchair for Pet
EXTRAS = {
    # the dog was tried on the armchair, but the spot crops the chair at the frame edge and only a
    # brown blob showed: Pet keeps the rope toy and food bowl on the table

}


def cutout(src, rect, wood_above=None, fg_rect=None):
    """RGBA cut-out of the objects inside rect (plate px)."""
    x0, y0, x1, y1 = rect
    pad = 24
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(src.shape[1], x1 + pad), min(src.shape[0], y1 + pad)
    crop = src[Y0:Y1, X0:X1].copy()
    mask = np.zeros(crop.shape[:2], np.uint8)
    bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    r = (x0 - X0, y0 - Y0, x1 - x0, y1 - y0)
    if wood_above or fg_rect:
        mask[:] = cv2.GC_BGD
        mask[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] = cv2.GC_PR_FGD
        if fg_rect:
            fx0, fy0, fx1, fy1 = fg_rect
            mask[fy0 - Y0:fy1 - Y0, fx0 - X0:fx1 - X0] = cv2.GC_FGD
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV).astype(int)
        wood = (hsv[..., 0] >= 8) & (hsv[..., 0] <= 24) & (hsv[..., 1] >= 50) & (hsv[..., 1] <= 120) & (hsv[..., 2] > 130) & (hsv[..., 2] < 240)
        rows = np.arange(crop.shape[0])[:, None] + Y0 < (wood_above or 0)
        mask[wood & rows & (mask != cv2.GC_FGD)] = cv2.GC_BGD
        cv2.grabCut(crop, mask, None, bgd, fgd, 8, cv2.GC_INIT_WITH_MASK)
    else:
        cv2.grabCut(crop, mask, r, bgd, fgd, 8, cv2.GC_INIT_WITH_RECT)
    fg = ((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)).astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(fg)          # drop specks
    keep = np.zeros_like(fg)
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] > 120:
            keep[lab == i] = 1
    sure = cv2.erode(keep, np.ones((5, 5), np.uint8))
    maybe = cv2.dilate(keep, np.ones((7, 7), np.uint8))
    if sure.sum() < 50 and wood_above:          # the wood rule ate a wood-coloured item (box, basket)
        return cutout(src, rect, None, fg_rect)
    tri = np.where(sure > 0, 1.0, np.where(maybe > 0, 0.5, 0.0))
    img = crop[..., ::-1].astype(np.float64) / 255
    alpha = estimate_alpha_cf(img, tri)
    fgc = estimate_foreground_ml(img, alpha)
    rgba = np.dstack([fgc, alpha])
    ys, xs = np.where(alpha > 0.3)
    return rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def paste(base, rgba, scale, anchor, shadow=True):
    """Alpha-composite rgba onto base (float RGB 0-1) with its bottom-centre at anchor."""
    h, w = rgba.shape[:2]
    rgba = cv2.resize(rgba, (round(w * scale), round(h * scale)), interpolation=cv2.INTER_AREA)
    h, w = rgba.shape[:2]
    ax, ay = anchor
    x0, y0 = ax - w // 2, ay - h
    a = rgba[..., 3:]
    if shadow:   # soft contact shadow: the alpha squashed onto the table plane, blurred, multiplied
        sh = np.zeros(base.shape[:2], np.float64)
        foot = cv2.resize(a[..., 0], (w, max(2, h // 6)))
        sy = ay - foot.shape[0] // 2 + 4
        ys, ye = max(0, sy), min(base.shape[0], sy + foot.shape[0])
        xs, xe = max(0, x0 + 6), min(base.shape[1], x0 + 6 + w)
        sh[ys:ye, xs:xe] = foot[ys - sy:ye - sy, xs - x0 - 6:xe - x0 - 6]
        sh = cv2.GaussianBlur(sh, (0, 0), 7) * 0.38
        base *= (1 - sh[..., None] * np.array([0.55, 0.62, 0.7]))
    Y0, Y1, X0, X1 = max(0, y0), min(base.shape[0], y0 + h), max(0, x0), min(base.shape[1], x0 + w)
    part = rgba[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    base[Y0:Y1, X0:X1] = base[Y0:Y1, X0:X1] * (1 - part[..., 3:]) + part[..., :3] * part[..., 3:]
    return base


def build(ind):
    base = np.asarray(Image.open(BASE).convert("RGB")).astype(np.float64) / 255
    src = cv2.imread(str(RAW / f"{ind}-plate-1x1.png"))
    for rect, scale, anchor in EXTRAS.get(ind, []):
        base = paste(base, cutout(src, rect), scale, anchor, shadow=False)
    for rect, scale, anchor, *fg in PROPS[ind]:
        base = paste(base, cutout(src, rect, WOOD_ABOVE.get(ind), fg[0] if fg else None), scale, anchor)
    out = RAW / f"spot-plate-{ind}.png"
    Image.fromarray((base.clip(0, 1) * 255).round().astype(np.uint8)).save(out)
    return out


if __name__ == "__main__":
    inds = sys.argv[1:] or list(PROPS)
    outs = [build(i) for i in inds]
    sheet = Image.new("RGB", (1536, 1024), "white")
    for n, p in enumerate(outs):
        sheet.paste(Image.open(p).resize((512, 512)), ((n % 3) * 512, (n // 3) * 512))
    sheet.save(HERE / "img" / "review" / "spot-props.jpg", quality=88)
    print([p.name for p in outs])
