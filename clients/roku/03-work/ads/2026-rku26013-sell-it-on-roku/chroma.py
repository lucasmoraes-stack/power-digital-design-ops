"""Chroma-key a prop group generated on flat green (Figma AI) into an RGBA cut-out plus a shadow map.

The key works on the red/green ratio, which stays near 0.04 on the green floor in light and in
shadow alike, while every object (lilac, white, wood, fruit, even green-bounced undersides) sits
far above it:
    alpha  = clip((R/G - lo) / (hi - lo))
    despill: G is pulled down to max(R, B) * keep  (keep > 1 lets real greens, e.g. leaves, survive)
    shadow = how much darker the floor is than the clean floor (G / G_ref), only near the objects,
             with a small floor so the floor's own gradient never shows as a box
"""
import cv2
import numpy as np
from PIL import Image


def key(path, lo=0.10, hi=0.30, keep=1.0):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    ratio = (r + 4) / (g + 4)
    # the backdrop's own R/G drifts per image (0.02-0.25): measure it on the image border
    border = np.concatenate([ratio[:12].ravel(), ratio[-12:].ravel(), ratio[:, :12].ravel(), ratio[:, -12:].ravel()])
    lo = max(lo, np.percentile(border, 99) + 0.06)
    hi = lo + 0.2
    alpha = np.clip((ratio - lo) / (hi - lo), 0, 1)
    alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))    # speckle
    out = a.copy()
    # despill: green bounce (also the teal it makes on lilac and white) is pulled back to the red
    # level; keep > 1 for prop groups with real greens (leaves)
    out[..., 1] = np.minimum(g, np.maximum(r, b * 0.85) * keep)
    bg = (alpha < 0.01).astype(np.float32)
    k = 121
    num = cv2.blur(g * bg, (k, k))
    den = cv2.blur(bg, (k, k))
    clean = np.percentile(g[bg > 0], 80)
    gref = np.where(den > 0.2, num / np.maximum(den, 1e-3), clean)
    gref = np.maximum(gref, clean * 0.97)
    shadow = np.clip(1 - g / gref - 0.05, 0, 1) / 0.95 * (1 - alpha)
    near = cv2.dilate((alpha > 0.5).astype(np.uint8), np.ones((1, 1), np.uint8))
    dist = cv2.distanceTransform(1 - near, cv2.DIST_L2, 5)
    shadow *= np.clip(1 - dist / 90, 0, 1)
    return np.dstack([out / 255, alpha]), shadow


def trim(rgba, shadow, pad=8):
    m = (rgba[..., 3] > 0.02) | (shadow > 0.03)
    ys, xs = np.where(m)
    y0, y1 = max(0, ys.min() - pad), min(m.shape[0], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(m.shape[1], xs.max() + pad + 1)
    return rgba[y0:y1, x0:x1], shadow[y0:y1, x0:x1]


def woodkey(path, thr=26):
    """Key a prop group shot on light oak (table and wall both oak, so the bounce is wood-coloured
    and leftovers vanish on our oak table). The backdrop is estimated by inpainting the objects
    out and blurring; objects = pixels that differ from it (colour distance), refined by GrabCut
    and closed-form matting. shadow = how much darker than the clean backdrop the wood is."""
    from pymatting import estimate_alpha_cf, estimate_foreground_ml
    bgr = cv2.imread(str(path))
    h, w = bgr.shape[:2]
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    # first backdrop guess: big median of the image (objects are a minority)
    # backdrop guess: per-row median (wood fills most of every row), smoothed down the rows
    rowmed = np.median(lab, axis=1)
    rowmed = cv2.GaussianBlur(rowmed[:, None, :], (0, 0), sigmaX=0.1, sigmaY=4)[:, 0, :]
    lab0 = np.repeat(rowmed[:, None, :], w, 1)
    d = np.sqrt(((lab[..., 1:] - lab0[..., 1:]) ** 2).sum(-1) * 2.0 + ((lab[..., 0] - lab0[..., 0]) * 0.6) ** 2)
    cand = (d > thr).astype(np.uint8)
    cand = cv2.morphologyEx(cand, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab_cc, st, _ = cv2.connectedComponentsWithStats(cand)
    keep = np.zeros_like(cand)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 1500:
            keep[lab_cc == i] = 1
    # backdrop without the objects
    hole = cv2.dilate(keep, np.ones((31, 31), np.uint8))
    small = cv2.resize(bgr, (w // 4, h // 4)); hs = cv2.resize(hole * 255, (w // 4, h // 4))
    bgi = cv2.inpaint(small, hs, 9, cv2.INPAINT_TELEA)
    bgi = cv2.resize(cv2.GaussianBlur(bgi, (0, 0), 6), (w, h)).astype(np.float32)
    labb = cv2.cvtColor(bgi.astype(np.uint8), cv2.COLOR_BGR2LAB).astype(np.float32)
    # GrabCut seeded by the colour difference
    d2 = np.sqrt(((lab[..., 1:] - labb[..., 1:]) ** 2).sum(-1) * 2.0 + ((lab[..., 0] - labb[..., 0]) * 0.6) ** 2)
    gc = np.full((h, w), cv2.GC_BGD, np.uint8)
    near = cv2.dilate(keep, np.ones((41, 41), np.uint8)) > 0
    gc[near] = cv2.GC_PR_BGD
    gc[(d2 > thr * 0.7) & near] = cv2.GC_PR_FGD
    gc[cv2.erode(keep, np.ones((9, 9), np.uint8)) > 0] = cv2.GC_FGD
    m1, m2 = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(bgr, gc, None, m1, m2, 6, cv2.GC_INIT_WITH_MASK)
    fg = ((gc == cv2.GC_FGD) | (gc == cv2.GC_PR_FGD)).astype(np.uint8)
    n, lab_cc, st, _ = cv2.connectedComponentsWithStats(fg)
    fg2 = np.zeros_like(fg)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 1500:
            fg2[lab_cc == i] = 1
    sure = cv2.erode(fg2, np.ones((5, 5), np.uint8)); maybe = cv2.dilate(fg2, np.ones((5, 5), np.uint8))
    tri = np.where(sure > 0, 1.0, np.where(maybe > 0, 0.5, 0.0))
    img = bgr[..., ::-1].astype(np.float64) / 255
    alpha = estimate_alpha_cf(img, tri)
    # wood that GrabCut swept in (the table/wall seam, shadows): where a pixel is the backdrop's
    # colour and not deep inside an object, it is backdrop
    core = cv2.erode((alpha > 0.95).astype(np.uint8), np.ones((15, 15), np.uint8)) > 0
    woodlike = np.clip((d2 - 12) / 14, 0, 1)
    alpha = np.where(core, alpha, alpha * woodlike)
    alpha = cv2.morphologyEx((alpha > 0.5).astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) * 0 + alpha
    n, lab_cc, st, _ = cv2.connectedComponentsWithStats((alpha > 0.5).astype(np.uint8))
    big = np.zeros(alpha.shape, bool)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 1500:
            big |= lab_cc == i
    alpha = alpha * cv2.dilate(big.astype(np.uint8), np.ones((5, 5), np.uint8))
    fgc = estimate_foreground_ml(img, alpha)
    # contact shadow: darkening of the wood relative to the clean backdrop, near the objects only
    lum = bgr.astype(np.float32).mean(2); lumb = bgi.mean(2)
    shadow = np.clip(1 - lum / np.maximum(lumb, 1) - 0.02, 0, 1) * (1 - alpha)
    dist = cv2.distanceTransform((1 - (alpha > 0.5)).astype(np.uint8), cv2.DIST_L2, 5)
    shadow *= np.clip(1 - dist / 70, 0, 1)
    # only on the table under/around each object's foot (the source's table/wall seam is not shadow)
    obj = alpha > 0.5
    foot = np.zeros_like(shadow)
    cols = np.where(obj.any(0))[0]
    for x in cols:
        yb = np.where(obj[:, x])[0].max()
        foot[max(0, yb - 12):min(h, yb + 50), x] = 1
    foot = cv2.GaussianBlur(cv2.dilate(foot, np.ones((1, 41), np.uint8)), (0, 0), 6)
    shadow *= foot
    return np.dstack([fgc, alpha]).astype(np.float32), shadow.astype(np.float32)


def whitekey(path):
    """Key a prop group shot on a white seamless backdrop (neutral bounce, like the bright room).
    alpha from the distance to the local backdrop (white falling off to soft grey in the shadows):
    chroma counts fully, lightness only where it is clearly darker than any shadow could be;
    edges by closed-form matting with backdrop-free colours (estimate_foreground_ml).
    shadow = darkening of the backdrop near the objects' feet."""
    from pymatting import estimate_alpha_cf, estimate_foreground_ml
    bgr = cv2.imread(str(path))
    h, w = bgr.shape[:2]
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    L, A, B = lab[..., 0], lab[..., 1] - 128, lab[..., 2] - 128
    chroma = np.sqrt(A ** 2 + B ** 2)
    # the backdrop is ~253 L; its shadows only reach that low right at the objects' feet, so a pixel
    # is object if it has colour, or is darker than 225 anywhere except a thin band at the foot
    tex = cv2.GaussianBlur(np.abs(cv2.Laplacian(L, cv2.CV_32F)), (0, 0), 3)
    # shadows on white pick up a warm/coloured bounce (chroma 9-15) but stay smooth
    obj = ((chroma > 16) | (L < 150) | ((chroma > 7) & (tex > 4.0))).astype(np.uint8)
    # neutral parts (sage vase, metal caps, a white controller) vs soft grey shadows: shadows are
    # smooth and above ~195; object greys are darker or textured
    grey = ((L < 150) | ((L < 215) & (tex > 4.0))).astype(np.uint8)
    obj0 = obj.copy()
    for x in np.where(obj0.any(0))[0]:
        ys = np.where(obj0[:, x])[0]
        grey[ys.max() + 1:, x] = 0                              # below a coloured object: shadow
    # grey parts connected to the coloured objects from above or the side (vase, metal caps)
    obj = obj | grey
    obj = cv2.morphologyEx(obj, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    obj = cv2.morphologyEx(obj, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, cc, st, _ = cv2.connectedComponentsWithStats(obj)
    keep = np.zeros_like(obj)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 1500:
            keep[cc == i] = 1
    # holes inside objects (highlights) are object too
    ff = keep.copy(); m = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(ff, m, (0, 0), 1)
    keep = keep | (1 - ff)
    sure = cv2.erode(keep, np.ones((5, 5), np.uint8)); maybe = cv2.dilate(keep, np.ones((3, 3), np.uint8))
    tri = np.where(sure > 0, 1.0, np.where(maybe > 0, 0.5, 0.0))
    # nothing below an object's own silhouette is object (that is its grey shadow on the white)
    strict = keep & (((chroma > 16) | (L < 150) | ((chroma > 7) & (tex > 4.0)) | grey.astype(bool)))
    strict = cv2.morphologyEx(strict.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    for x in np.where(keep.any(0))[0]:
        col = np.where(strict[:, x])[0]
        if not len(col):
            tri[:, x] = np.minimum(tri[:, x], 0.0)
            continue
        yb = col.max()
        tri[yb - 1:, x] = np.minimum(tri[yb - 1:, x], 0.0)
        tri[max(0, yb - 4):yb - 1, x] = np.minimum(tri[max(0, yb - 4):yb - 1, x], 0.5)
    img = bgr[..., ::-1].astype(np.float64) / 255
    alpha = estimate_alpha_cf(img, tri)
    # the foot of each object fades into its own grey shadow on white: the matte leaves a pale tick
    # or ring there. Cut the bottom 2 px of every column crisply (the drawn contact shadow covers it)
    alpha[alpha < 0.08] = 0
    fgc = estimate_foreground_ml(img, alpha)
    # edge pixels: their colour estimate drifts toward the white backdrop -> faint white rims.
    # Pull partially transparent pixels toward the colour of the nearest solid object pixel.
    solid = (alpha > 0.97).astype(np.uint8)
    if solid.any():
        _, idx = cv2.distanceTransformWithLabels(1 - solid, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
        ys, xs = np.where(solid)
        lut = np.zeros((idx.max() + 1, 3)); lut[idx[ys, xs]] = fgc[ys, xs]
        near = lut[idx]
        edge = (alpha > 0) & (alpha <= 0.97)
        fgc[edge] = near[edge] * 0.85 + fgc[edge] * 0.15
    lum = bgr.astype(np.float32).mean(2)
    ref = np.percentile(lum[keep == 0], 90)
    shadow = np.clip(1 - lum / ref - 0.03, 0, 1) * (1 - alpha)
    o = alpha > 0.5
    foot = np.zeros_like(shadow)
    for x in np.where(o.any(0))[0]:
        yb = np.where(o[:, x])[0].max()
        foot[max(0, yb - 12):min(h, yb + 50), x] = 1
    foot = cv2.GaussianBlur(cv2.dilate(foot, np.ones((1, 41), np.uint8)), (0, 0), 6)
    shadow *= foot
    return np.dstack([fgc, alpha]).astype(np.float32), shadow.astype(np.float32)



def aikey(path):
    """Prop cut-out by BiRefNet (rembg 'birefnet-general'), run once and cached as <name>-cut.png;
    edges decontaminated with estimate_foreground_ml. shadow = the darkening of the white backdrop
    near the objects' feet (the soft contact shadows the generator rendered)."""
    from pathlib import Path
    from pymatting import estimate_foreground_ml
    path = Path(path)
    cut = path.with_name(path.stem + "-cut.png")
    if not cut.exists():
        from rembg import new_session, remove
        remove(Image.open(path).convert("RGB"), session=new_session("birefnet-general")).save(cut)
    rgba = np.asarray(Image.open(cut).convert("RGBA")).astype(np.float64) / 255
    img = np.asarray(Image.open(path).convert("RGB")).astype(np.float64) / 255
    alpha = rgba[..., 3]
    alpha[alpha < 0.04] = 0
    fgc = estimate_foreground_ml(img, alpha)
    h = alpha.shape[0]
    lum = img.mean(2) * 255
    ref = np.percentile(lum[alpha < 0.01], 90)
    shadow = np.clip(1 - lum / ref - 0.03, 0, 1) * (1 - alpha)
    o = alpha > 0.5
    foot = np.zeros_like(shadow)
    for x in np.where(o.any(0))[0]:
        yb = np.where(o[:, x])[0].max()
        foot[max(0, yb - 12):min(h, yb + 50), x] = 1
    foot = cv2.GaussianBlur(cv2.dilate(foot.astype(np.float32), np.ones((1, 41), np.uint8)), (0, 0), 6)
    return np.dstack([fgc, alpha]).astype(np.float32), (shadow * foot).astype(np.float32)
