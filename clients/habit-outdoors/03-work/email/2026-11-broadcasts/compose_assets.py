"""compose_assets.py - Habit Outdoors, November 2026 broadcasts: every image of the 5 emails.

Run (round 6):  python build_emails.py && python compose_assets.py && python build_emails.py
      python compose_assets.py n2 bake edges      (some jobs)

Jobs
  n1..n5   images whose position does not depend on the layout (photos in frames, flat-panel packshots,
           the 02 collage, the 05 hero and closing, mobile-only crops)
  bake     every <img data-bake="..."> of the built HTML: Chrome measures, at the 600px layout, where the
           image sits inside its band cell (x, y) and how tall the band ABOVE is; the composite is then built
           from exactly those tile rows and columns (R1), and, for a "rise" image, from the band above at its
           measured phase, a torn line, and the band's own tile below it, so a product can cross the torn
           edge into the band above (the text column next to it carries the other half of the same torn line,
           a separate image "<id>~t"). Light-paper bands get a -dm twin automatically.
  edges    E18 torn edges between bands, phase-matched to the measured band heights (as in round 3)
  clean    removes assets no HTML references

Round 4 (owner's review 2026-10-07): people in every email, products scaled up and breaking the grid
(crossing torn edges, cut by the email edge, rising out of panels), clean cut-outs (alpha eroded 2px and the
fringe colour decontaminated from the garment interior, so no grey studio halo), one light direction for the
whole batch (upper left: cast shadow offset right/down, contact shadow tight under the hem, none for garments
that bleed off an edge). No text is baked into any image.

Round 6 (owner's review 2026-10-08): no alpha fade and no blur melt anywhere (melt() and the hero fade are gone):
every photo-to-band transition is a ripped edge (torn_sheet: ripped print with white paper core and cast shadow;
tear_into: the next band torn over the photo). photo_hero: the 03 full-bleed photo hero (desktop + own mobile
crop, soft darkening INSIDE the photo under the text only, -dm twins); paper_hero: the 05 hero (torn print on the
paper). New: the 02 collage as one overlapping pile, the 03 staggered pair, the 05 tier composites (grid, lead,
group, set, highlight) and the torn label ends (tag_end, PNG-24 alpha).

Sources: only Habit material (products.json + 01-brand/photos). Built on the kit library
(01-brand/email-kit/tools/compose.py + compose_v05.py, imported read-only).
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
KIT_TOOLS = ROOT / "clients/habit-outdoors/01-brand/email-kit/tools"
sys.path.insert(0, str(KIT_TOOLS))
import compose as C  # noqa: E402
import compose_v05 as V  # noqa: E402,F401  (registers paper-camo, halftone-brown, grad textures)

OUT = HERE / "assets"
OUT.mkdir(exist_ok=True)
PROD = ROOT / "clients/habit-outdoors/01-brand/photos/products"
LIFE = ROOT / "clients/habit-outdoors/01-brand/photos/lifestyle"
PRODUCTS = json.loads((HERE / "products.json").read_text(encoding="utf-8"))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

TAPSHOE, BROWN, LIGHT, PATRIOT, IVY = C.TAPSHOE, C.BROWN, C.LIGHT, C.PATRIOT, C.IVY
ALUMINUM, DUSK, TURKISH = "#A39A8C", "#ACB1B3", "#5C5249"
RUST, SLATE = "#774727", "#4F5C5F"           # kit v0.5 panel colours (rev-oct-02)
FRAME = "#F1EEEB"                             # photo frame: kit dark-mode title tone, a warm off-white
DM_OF = {"paper-light": "paper-light-dm", "paper-camo": "paper-camo-dm"}

# One light for the whole batch: upper left. Cast shadow offset (file px at 2x), blur, opacity.
CAST = (10, 8, 16, 0.24)


# ================================================================ basics

def o(name: str) -> str:
    return str(OUT / name)


def box_blur(a: np.ndarray, r: int) -> np.ndarray:
    """Separable box blur, edges clamped (no scipy on this machine)."""
    for ax in (0, 1):
        p = [(0, 0)] * a.ndim
        p[ax] = (r + 1, r)
        c = np.cumsum(np.pad(a, p, mode="edge"), axis=ax, dtype=np.float64)
        n = a.shape[ax]
        a = (np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=ax) - np.take(c, np.arange(0, n), axis=ax)) / (2 * r + 1)
    return a.astype(np.float32)


def clean_cut(im: Image.Image, erode: int = 2, feather: float = 0.8, decon: int = 4, trapped: bool = True) -> Image.Image:
    """Store PNG -> clean cut-out. The store alpha keeps a 1-3px rim of the grey studio backdrop, which reads
    as a light halo on a dark band (owner, round 4). Hard alpha at 50%, eroded `erode` px, feathered; the RGB
    of every edge pixel is re-estimated from the garment interior (push-pull from a core eroded `decon` px
    more), so no studio grey survives along the silhouette. Trimmed to the opaque bounds."""
    im = im.convert("RGBA")
    a = np.asarray(im.getchannel("A")).copy()
    # Round 5 (QA r4): studio backdrop trapped INSIDE the silhouette (the opaque white sliver between sleeve and
    # body of the 04 flannel). Near-white, near-neutral opaque pixels connected to the transparent background
    # (directly or through other such pixels) are backdrop, not garment: flood from the background edge.
    rgb8 = np.asarray(im.convert("RGB")).astype(np.int16)
    white = (rgb8.min(2) >= 225) & ((rgb8.max(2) - rgb8.min(2)) <= 14) & (a > 128) & trapped
    # only THIN white (a sliver under 15 px wide squeezed between two parts of the garment)
    wi = Image.fromarray(white.astype(np.uint8) * 255)
    opened = np.asarray(wi.filter(ImageFilter.MinFilter(15)).filter(ImageFilter.MaxFilter(15))) > 0
    white &= ~opened
    bgm = Image.fromarray(((a <= 128) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
    reach = np.asarray(bgm) > 0
    wimg = white.astype(np.uint8) * 255
    grow = (reach & white).astype(np.uint8) * 255
    for _ in range(600):                                     # grows 2 px per step: long slivers need many
        nxt = np.minimum(np.asarray(Image.fromarray(grow).filter(ImageFilter.MaxFilter(5))), wimg)
        if (nxt == grow).all():
            break
        grow = nxt
    trapped = grow > 0
    if trapped.any():
        t = np.asarray(Image.fromarray(trapped.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))) > 0
        a[t] = 0                                            # one extra px: the anti-aliased rim of the sliver
    clean_cut.last_trapped = int(trapped.sum())
    hard = Image.fromarray(((a > 128) * 255).astype(np.uint8))
    m = hard
    for _ in range(erode):
        m = m.filter(ImageFilter.MinFilter(3))
    alpha = np.asarray(m.filter(ImageFilter.GaussianBlur(feather)), np.float32)
    core = hard
    for _ in range(erode + decon):
        core = core.filter(ImageFilter.MinFilter(3))
    core = np.asarray(core) > 0
    rgb = np.asarray(im.convert("RGB"), np.float32)
    w = core.astype(np.float32)
    fill = rgb * w[..., None]
    need = (alpha > 0) & ~core
    est = np.zeros_like(rgb)
    have = np.zeros(core.shape, bool)
    for r in (2, 4, 8, 16, 32):
        fb, wb = box_blur(fill, r), box_blur(w, r)
        ok = (wb > 0.01) & ~have
        est[ok] = fb[ok] / wb[ok][:, None]
        have |= ok
    out = rgb.copy()
    out[need] = est[need]
    res = Image.fromarray(np.dstack([np.clip(out, 0, 255), alpha]).astype(np.uint8), "RGBA")
    return res.crop(Image.fromarray(((alpha > 8) * 255).astype(np.uint8)).getbbox())


_CUTS: dict = {}


def packshot(email: str, handle: str, color: str | None = None) -> Image.Image:
    """Clean cut-out of the variant packshot from products.json."""
    for p in PRODUCTS:
        if p["email"] == email and p["handle"] == handle and (color is None or color in p["variant_title"]):
            key = p["image_file"]
            if key not in _CUTS:
                _CUTS[key] = clean_cut(Image.open(ROOT / key))
                print(f"      cut {Path(key).name}: {clean_cut.last_trapped} trapped backdrop px removed")
            return _CUTS[key]
    raise KeyError(handle)


def store(handle: str, n: str) -> Image.Image:
    return Image.open(PROD / handle / n).convert("RGBA")


WHITE_PRINT = {"men-s-angler-s-bluff-rain-bib"}     # white wave print reaches the silhouette: no trapped-backdrop pass


def store_cut(handle: str, n: str, component: bool = False) -> Image.Image:
    key = f"{handle}/{n}/{component}"
    if key not in _CUTS:
        im = store(handle, n)
        if component:
            im = largest_component(im)
        _CUTS[key] = clean_cut(im, trapped=handle not in WHITE_PRINT)
        print(f"      cut {key}: {clean_cut.last_trapped} trapped backdrop px removed")
    return _CUTS[key]


def largest_component(im: Image.Image) -> Image.Image:
    """Keep only the biggest opaque blob (drops printed spec text such as 'Model is 6'1"...')."""
    from collections import deque
    small = im.getchannel("A").resize((im.width // 4, im.height // 4), Image.BOX)
    a = np.asarray(small) > 20
    h, w = a.shape
    lab = np.zeros((h, w), np.int32)
    best, best_n, cur = 0, 0, 0
    for y0 in range(h):
        for x0 in range(w):
            if a[y0, x0] and not lab[y0, x0]:
                cur += 1
                q, n = deque([(y0, x0)]), 0
                lab[y0, x0] = cur
                while q:
                    y, x = q.popleft(); n += 1
                    for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= yy < h and 0 <= xx < w and a[yy, xx] and not lab[yy, xx]:
                            lab[yy, xx] = cur; q.append((yy, xx))
                if n > best_n:
                    best, best_n = cur, n
    keep = Image.fromarray(((lab == best) * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).resize(im.size, Image.NEAREST)
    arr = np.asarray(im).copy()
    arr[..., 3] = np.where(np.asarray(keep) > 0, arr[..., 3], 0)
    return Image.fromarray(arr, "RGBA")


def border_window(w: int, h: int, edge: int = 40, sides=("top", "bottom", "left", "right")) -> np.ndarray:
    """H x W weight: 1 inside, smooth to 0 over the last `edge` px of each listed side. Every baked shadow is
    multiplied by it, so the image border rows and columns are the untouched tile (R1)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    win = np.ones((h, w), np.float32)
    if "top" in sides:
        win *= C.smooth(np.clip(yy / edge, 0, 1))
    if "bottom" in sides:
        win *= C.smooth(np.clip((h - 1 - yy) / edge, 0, 1))
    if "left" in sides:
        win *= C.smooth(np.clip(xx / edge, 0, 1))
    if "right" in sides:
        win *= C.smooth(np.clip((w - 1 - xx) / edge, 0, 1))
    return win


def shade(canvas: Image.Image, alpha: np.ndarray, win: np.ndarray | None = None) -> None:
    """Composite black with an (H x W, 0..1) alpha, windowed."""
    if win is not None:
        alpha = alpha * win
    black = Image.new("RGBA", canvas.size, (0, 0, 0, 255))
    black.putalpha(Image.fromarray(np.clip(alpha * 255, 0, 255).astype(np.uint8), "L"))
    canvas.alpha_composite(black)


def put(canvas: Image.Image, cut: Image.Image, x: float, y: float, *, ground: bool = True, cast: bool = True,
        win: np.ndarray | None = None, contact: float = 0.55) -> tuple[int, int, int, int]:
    """Paste a clean cut-out with its top-left at (x, y) (may run past the canvas: cut by the border).
    Shadows (batch light, upper left): a cast shadow from the cut-out's own alpha, offset right and down,
    soft and light; and, when the product stands on a ground line, a tight contact shadow under every part
    of the hem (one thin ellipse per leg or hem segment, no wider than the hem). Both windowed."""
    W, H = canvas.size
    x, y = round(x), round(y)
    a = np.asarray(cut.getchannel("A"), np.float32) / 255
    if cast:
        dx, dy, blur, op = CAST
        layer = Image.new("L", (W, H), 0)
        layer.paste(Image.fromarray((a * 255 * op).astype(np.uint8), "L"), (x + dx, y + dy))
        sh = np.asarray(layer.filter(ImageFilter.GaussianBlur(blur)), np.float32) / 255
        shade(canvas, sh, win)
    if ground:
        hh = cut.height
        band = a[int(hh * 0.965):] > 0.5
        cols = band.any(axis=0)
        segs, s = [], None
        for i, v in enumerate(list(cols) + [False]):
            if v and s is None:
                s = i
            if not v and s is not None:
                if i - s > 6:
                    segs.append((s, i))
                s = None
        layer = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(layer)
        by = y + hh
        for s0, s1 in segs:
            cx = x + (s0 + s1) / 2 + 4
            rx = (s1 - s0) / 2 * 0.98
            d.ellipse((cx - rx, by - 7, cx + rx, by + 7), fill=int(255 * contact))
        sh = np.asarray(layer.filter(ImageFilter.GaussianBlur(5)), np.float32) / 255
        layer2 = Image.new("L", (W, H), 0)
        d2 = ImageDraw.Draw(layer2)
        for s0, s1 in segs:
            cx = x + (s0 + s1) / 2 + 8
            rx = (s1 - s0) / 2 * 1.08
            d2.ellipse((cx - rx, by - 12, cx + rx, by + 16), fill=int(255 * 0.20))
        sh2 = np.asarray(layer2.filter(ImageFilter.GaussianBlur(14)), np.float32) / 255
        shade(canvas, np.maximum(sh, sh2), win)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.paste(cut, (x, y), cut)
    canvas.alpha_composite(layer)
    return x, y, x + cut.width, y + cut.height


def fit(im: Image.Image, w: int | None = None, h: int | None = None) -> Image.Image:
    return C.fit(im, w=w, h=h)


def save_jpg(im: Image.Image, name: str, match=(), limit: int = 150 * 1024) -> Path:
    p = C.save_jpg(im.convert("RGB"), o(name), limit=limit, match=match)
    C.report(Path(p), None, None, limit)
    return Path(p)


def save_q(im: Image.Image, name: str, limit: int, q: int = 74, floor: int = 52) -> Path:
    """JPG 4:2:0 stepping down until under `limit` (photo composites, product rows)."""
    p = C.save_jpg_under(im, OUT / name, limit, q=q, floor=floor, subsampling=2)
    print(f"  {p.name:40s} {im.width}x{im.height}  {p.stat().st_size / 1024:5.1f} KB")
    return p


def tex_region(tex: str, x0: int, y0: int, w: int, h: int) -> np.ndarray:
    """Float RGB rows y0..y0+h, columns x0..x0+w of a kit tile (both wrapped), or a flat colour."""
    if tex.startswith("flat:"):
        return np.broadcast_to(np.array(C.rgb(tex[5:]), np.float32), (h, w, 3)).copy()
    T = C.load_tile(tex)
    ys = np.arange(y0, y0 + h) % T.shape[0]
    xs = np.arange(x0, x0 + w) % T.shape[1]
    return T[ys][:, xs].copy()


def tile_canvas(tex: str, w: int, h: int, y0: int = 0, x0: int = 0) -> Image.Image:
    return C.to_image(tex_region(tex, x0, y0, w, h))


def framed(photo: Image.Image, width: int, frame: int = 12, color: str = FRAME) -> Image.Image:
    ph = C.fit(photo.convert("RGB"), w=width - 2 * frame)
    out = Image.new("RGBA", (ph.width + 2 * frame, ph.height + 2 * frame), C.rgb(color) + (255,))
    out.paste(ph, (frame, frame))
    return out


def cover(photo: Image.Image, w: int, h: int, fx: float = 0.5, fy: float = 0.5) -> Image.Image:
    s = max(w / photo.width, h / photo.height)
    im = photo.resize((round(photo.width * s), round(photo.height * s)), Image.LANCZOS)
    x0 = int(min(max(im.width * fx - w / 2, 0), im.width - w))
    y0 = int(min(max(im.height * fy - h / 2, 0), im.height - h))
    return im.crop((x0, y0, x0 + w, y0 + h))


def place_rot(canvas: Image.Image, im: Image.Image, cx: float, cy: float, angle: float, win=None) -> None:
    """Framed photo / card rotated, with the batch cast shadow (light upper left)."""
    im = im.convert("RGBA").rotate(angle, resample=Image.BICUBIC, expand=True)
    put(canvas, im, cx - im.width / 2, cy - im.height / 2, ground=False, cast=True, win=win)


# Round 6 (owner, 2026-10-08): no alpha fade and no blur melt anywhere in the batch. Every photo-to-band
# transition is a ripped edge: the photo is a torn print lying on the band (ripped line, the white paper core
# showing along the rip, a soft cast shadow from the batch light), or the next band's sheet is torn over the
# photo (tear_into, E18). A soft darkening INSIDE a photo, under live text, is not a transition (burn()).
FIBRE = (244, 241, 237)          # paper core exposed by a rip (same off-white as the kit's torn-photo rim)


def rip_mask(w: int, h: int, sides, depth: float = 9.0, amp: float = 7.0, seed: int = 500) -> Image.Image:
    """L mask, 255 inside, 0 beyond a ripped line `depth` px inside each listed side (slow waves, fine jitter)."""
    m = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(m)
    rnd = random.Random(seed)
    for k, side in enumerate(sides):
        s = seed + 17 * k
        n = w if side in ("top", "bottom") else h
        line = [v + rnd.uniform(-1.1, 1.1) for v in C.torn_line(n, depth, amp, s)]      # fibrous micro-jags
        if side == "top":
            d.polygon([(0, 0)] + [(x, y) for x, y in enumerate(line)] + [(w, 0)], fill=0)
        elif side == "bottom":
            d.polygon([(0, h)] + [(x, h - 1 - y) for x, y in enumerate(line)] + [(w, h)], fill=0)
        elif side == "left":
            d.polygon([(0, 0)] + [(x, y) for y, x in enumerate(line)] + [(0, h)], fill=0)
        else:
            d.polygon([(w, 0)] + [(w - 1 - x, y) for y, x in enumerate(line)] + [(w, h)], fill=0)
    return m.filter(ImageFilter.GaussianBlur(0.7))


def fibre_rim(mask: Image.Image, seed: int, widths=(1, 3, 5)) -> np.ndarray:
    """0..1 alpha of the white paper core along every RIPPED edge of `mask` (straight borders of the array are
    treated as continuing, so they get no rim). Width varies along the edge between `widths` (px)."""
    hard = mask.point(lambda v: 255 if v > 127 else 0)
    pad = max(widths) + 4
    big = Image.new("L", (hard.width + 2 * pad, hard.height + 2 * pad), 255)
    big.paste(hard, (pad, pad))
    box = (pad, pad, pad + hard.width, pad + hard.height)
    ers = [np.asarray(big.filter(ImageFilter.MinFilter(2 * r + 1)).crop(box)) > 0 for r in widths]
    nz = C.periodic_noise(hard.width, hard.height, 26, 26, seed)
    lvl = np.digitize(nz, [-0.5, 0.5])                      # 0, 1, 2: thin, medium, wide rim
    inner = np.choose(lvl, ers)
    rim = (np.asarray(hard) > 0) & ~inner
    rim_img = Image.fromarray((rim * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    return np.asarray(rim_img, np.float32) / 255


def torn_sheet(cv: Image.Image, photo: Image.Image, x: int, y: int, sides, seed: int, *, depth: float = 9,
               amp: float = 7, rim: bool = True, shadow=(6, 9, 7, 0.42), win: np.ndarray | None = None,
               tone: float = 1.0) -> Image.Image:
    """Paste `photo` at (x, y) as a torn print: ripped on `sides` (the other sides stay straight: they run off
    the canvas or under another sheet), white paper core along the rip, cast shadow (batch light, upper left)
    on the band below. Returns the mask used."""
    ph = photo.convert("RGB")
    w, h = ph.size
    m = rip_mask(w, h, sides, depth, amp, seed)
    arr = np.asarray(ph, np.float32) * tone
    if rim and sides:
        r = fibre_rim(m, seed + 3)[:, :, None] * 0.92
        arr = arr * (1 - r) + np.array(FIBRE, np.float32) * r
    if shadow and sides:
        dx, dy, blur, op = shadow
        a = np.asarray(m, np.float32) / 255
        layer = Image.new("L", cv.size, 0)
        layer.paste(Image.fromarray((a * 255 * op).astype(np.uint8), "L"), (x + dx, y + dy))
        sh = np.asarray(layer.filter(ImageFilter.GaussianBlur(blur)), np.float32) / 255
        shade(cv, sh, win)
    rgba = Image.fromarray(np.dstack([np.clip(arr, 0, 255), np.asarray(m, np.float32)]).astype(np.uint8), "RGBA")
    layer = Image.new("RGBA", cv.size, (0, 0, 0, 0))
    layer.paste(rgba, (x, y), rgba)
    cv.alpha_composite(layer)
    return m


def burn_weight(h: int, w: int, *, rx: float, ry: float, cx: float = 0.0, cy: float = 0.0, core: float = 0.55,
                p: float = 2.0) -> np.ndarray:
    """0..1 weight of a soft local darkening INSIDE a photo, under live text (not a transition): a superellipse
    (exponent p: 2 = ellipse, 3-4 = rounded rectangle) centred at (cx, cy) with radii rx, ry, full inside
    `core` of the radii, easing to 0 at the radii. cx = cy = 0 = the top-left corner; a huge rx = a top band."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = (np.abs((xx - cx) / rx) ** p + np.abs((yy - cy) / ry) ** p) ** (1 / p)
    return 1 - C.smooth(np.clip((d - core) / (1 - core), 0, 1))


def burn(arr: np.ndarray, weight: np.ndarray, strength: float, soften: float = 0.0) -> np.ndarray:
    """Darken by `strength` x weight; `soften` (px) blurs the photo under the text a little more (glyphs read
    cleaner over quiet leaves, and the file stays under the weight cap)."""
    if soften:
        bl = np.asarray(C.to_image(arr).convert("RGB").filter(ImageFilter.GaussianBlur(soften)), np.float32)
        arr = arr * (1 - weight[:, :, None]) + bl * weight[:, :, None]
    return arr * (1 - strength * weight)[:, :, None]


def specks(canvas: Image.Image, ys: list[float], up_rgb, lo_rgb, seed: int, y_off: int = 0, n: int = 70, x_off: int = 0):
    """Fine paper crumbs along a tear (rev-oct-03 grain, R6): radius 0.6-1.3 px at 2x. Generated over the full
    1200 px width (so two pieces of one torn line carry the same crumbs) and shifted by x_off."""
    rnd, d = random.Random(seed), ImageDraw.Draw(canvas)
    lo = tuple(int(v) for v in lo_rgb) + (255,)
    up = tuple(int(v) for v in up_rgb) + (255,)
    for _ in range(n):
        x = rnd.randrange(len(ys))
        y = y_off + ys[x] - rnd.uniform(0.5, 4.5)
        r = rnd.choice((0.6, 0.8, 1.0, 1.3))
        d.ellipse((x - x_off - r, y - r, x - x_off + r, y + r), fill=lo)
    for _ in range(n // 3):
        x = rnd.randrange(len(ys))
        y = y_off + ys[x] + rnd.uniform(1.0, 4.0)
        r = rnd.choice((0.6, 0.8, 1.0))
        d.ellipse((x - x_off - r, y - r, x - x_off + r, y + r), fill=up)


def remove_callout(im: Image.Image, box: tuple[int, int, int, int], thr: int = 28) -> Image.Image:
    """Erase a store callout mark (pure black dot + line) inside `box` with the median of its neighbourhood."""
    arr = np.asarray(im.convert("RGB")).copy()
    x0, y0, x1, y1 = box
    sub = arr[y0:y1, x0:x1]
    mask = sub.max(axis=2) < thr
    mask = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
    med = np.asarray(Image.fromarray(sub).filter(ImageFilter.MedianFilter(15)))
    for _ in range(3):
        sub[mask] = med[mask]
        med = np.asarray(Image.fromarray(sub).filter(ImageFilter.MedianFilter(15)))
    arr[y0:y1, x0:x1] = sub
    return Image.fromarray(arr, "RGB")


def tear_into(arr: np.ndarray, next_tex: str, tear_y: int, seed: int, strip: int = 90, amp: float = 8,
              rough: float = 0) -> Image.Image:
    """Bottom of a 1200-wide float RGB array torn into the next band (the 02 collage, the 05 hero)."""
    H, W = arr.shape[:2]
    lo = C.tile_rows(next_tex, H - tear_y + strip, end=C._continues(next_tex))
    top_rows = H - lo.shape[0]
    ys = C.torn_line(W, strip, amp=amp, seed=seed)
    if rough:                                     # round 6b: irregular profile (ragged bites, not a soft wave)
        rnd = random.Random(seed + 7)
        bumps = np.zeros(W, np.float32)
        x = 0
        while x < W:
            wd = rnd.randint(14, 60)
            bumps[x:x + wd] = rnd.uniform(-rough, rough)
            x += wd
        k = np.ones(9, np.float32) / 9
        bumps = np.convolve(bumps, k, mode="same") + np.array([rnd.uniform(-1.6, 1.6) for _ in range(W)], np.float32)
        # the pile hides the middle of this tear; only ~40 px show at each email edge, so give those
        # stretches their own ragged bites (a soft wave reads straight over 40 px)
        for x0 in (0, W - 70):
            xx = x0
            while xx < x0 + 70:
                wd = rnd.randint(5, 14)
                bumps[xx:xx + wd] += rnd.uniform(-rough * 1.6, rough * 1.6)
                xx += wd
        ys = [y + float(b) for y, b in zip(ys, bumps)]
    m = Image.new("L", (W, lo.shape[0]), 0)
    ImageDraw.Draw(m).polygon([(0, lo.shape[0])] + [(x, y) for x, y in enumerate(ys)] + [(W, lo.shape[0])], fill=255)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[:, :, None] / 255
    part = arr[top_rows:].copy()
    C.tear_shadow(part, ys)
    up_rgb = np.median(part[: strip // 2].reshape(-1, 3), 0)
    arr[top_rows:] = part * (1 - m) + lo * m
    img = C.to_image(arr)
    specks(img, ys, up_rgb, np.median(lo.reshape(-1, 3), 0), seed + 1, y_off=top_rows)
    return img


def paper_hero(photo: Image.Image, name: str, *, size, photo_w, crop_x=0, photo_y, photo_h, sides, base,
               next_tex, tear_y, text_box, seed, limit=150 * 1024, scale=1.0, q=70):
    """E24B hero image (05), round 6: the photo is a torn print on the base paper (ripped on `sides`, white
    core, cast shadow; no fade), the live text sits on the paper below it, then the paper tears into the next
    band (E18 baked). Built at the 1200 px tile scale; `scale` resizes the result (mobile crop)."""
    W, H = size
    cv = C.to_image(C.tile_rows(base, H))
    ph = C.fit(photo.convert("RGB"), w=photo_w)
    ph = ph.crop((crop_x, 0, crop_x + W, min(ph.height, photo_h)))
    torn_sheet(cv, ph, 0, photo_y, sides, seed, depth=11, amp=8, shadow=(6, 10, 9, 0.5))
    arr = np.asarray(cv.convert("RGB"), np.float32)
    img = tear_into(arr, next_tex, tear_y, seed + 2)
    if scale != 1.0:
        W, H = round(W * scale), round(H * scale)
        img = img.resize((W, H), Image.LANCZOS)
        text_box = tuple(round(v * scale) for v in text_box)
    p = C.save_jpg_under(img, OUT / name, limit, q=q, floor=46, subsampling=2)
    print(f"  {p.name:40s} {W}x{H}  {p.stat().st_size / 1024:5.1f} KB")
    print(f"      text area {C.contrast_report(p, ['#FFFFFF', '#E2DDD9'], text_box)}")
    return p


def photo_hero(photo: Image.Image, name: str, *, scale: float, crop_x: int, crop_y: int, H: int, tear_y: int,
               burn_ellipse: dict, strength: float, next_tex: str, dm_tex: str | None, seed: int, boxes: dict,
               out_w: int = 1200, limit: int = 140 * 1024, q: int = 72, soften: float = 0.7, soften_text: float = 1.4):
    """03 hero, round 6: full-bleed photo (no split, no fade) at 1200 px tile scale, a soft local darkening
    under the live text (burn_weight ellipse, strength), torn at tear_y into the next band (its tile's last
    rows, so the next <td> continues). dm_tex writes the -dm twin. out_w < 1200 resizes (mobile crop: the
    tile then matches the mobile band, whose 1200 px tile is shown at 375 css). `soften` px blur at 2x on the
    whole photo (weight cap, as the kit's E30), `soften_text` more under the text."""
    W = 1200
    ph = photo.convert("RGB")
    ph = ph.resize((round(ph.width * scale), round(ph.height * scale)), Image.LANCZOS)
    ph = ph.crop((crop_x, crop_y, crop_x + W, crop_y + H))
    assert ph.size == (W, H), f"photo crop too small: {ph.size}"
    if soften:
        ph = ph.filter(ImageFilter.GaussianBlur(soften))
    arr = np.asarray(ph, np.float32)
    wgt = burn_weight(H, W, **burn_ellipse)
    arr = burn(arr, wgt, strength, soften=soften_text)
    out = []
    for suffix, tex in [("", next_tex)] + ([("-dm", dm_tex)] if dm_tex else []):
        img = tear_into(arr.copy(), tex, tear_y, seed, strip=60)
        k = out_w / W
        if out_w != W:
            img = img.resize((out_w, round(H * k)), Image.LANCZOS)
        p = C.save_jpg_under(img, OUT / name.replace(".jpg", f"{suffix}.jpg"), limit, q=q, floor=44, subsampling=2)
        print(f"  {p.name:40s} {img.width}x{img.height}  {p.stat().st_size / 1024:5.1f} KB")
        if not suffix:
            for lab, (hexes, b) in boxes.items():
                bb = tuple(round(v * k) for v in b)
                print(f"      {lab:9s} {C.contrast_report(p, hexes, bb, blur=2)}")
        out.append(p)
    return out


def torn_photo(photo: Image.Image, name: str, *, band: str, dm_band: str | None, size=(1200, 820), photo_w=980,
               cx=600, cy=410, angle=-1.5, sides=("bottom", "right"), seed=111):
    return C.compose_torn_photo(photo, o(name), band=band, size=size, photo_w=photo_w, cx=cx, cy=cy, angle=angle,
                                sides=sides, frame=12, frame_color=FRAME, dm_band=dm_band, seed=seed)


def panel_card(cut: Image.Image, panel: str, fill: str, size: tuple[int, int], box: tuple[int, int, int, int],
               prod_h: int, bottom: int, name: str, cx: float | None = None, limit: int = 60 * 1024,
               ground: bool = True, radius: int = 20, top: int | None = None) -> Path:
    """Product RISING OUT of a flat rounded panel (rev-oct-03 hoodie): flat `fill` all round (the card's own
    flat colour, so the image is invisible at any width), panel rectangle `box`, the product scaled to
    `prod_h` and standing at `bottom` (contact shadow) or cut by the panel / image border (top given)."""
    W, H = size
    cv = Image.new("RGBA", size, C.rgb(fill) + (255,))
    ImageDraw.Draw(cv).rounded_rectangle(box, radius=radius, fill=C.rgb(panel) + (255,))
    p = fit(cut, h=prod_h)
    cx = W / 2 if cx is None else cx
    y = (bottom - p.height) if top is None else top
    put(cv, p, cx - p.width / 2, y, ground=ground)
    return save_jpg(cv, name, match=(fill, panel), limit=limit)


# ================================================================ static jobs (layout-independent)

def n1():
    print("01 Women's: everything is baked on measured positions (job bake)")


def n2():
    print("02 Gift Guide #1")
    # Hero collage, round 6 (owner: "um buraco aqui no meio"): one tight overlapping pile like ref2 (Fall '26),
    # no bare ground between the prints. Five prints (a fifth, the angler wading the river, not used anywhere
    # else in November, fills the centre); the pile runs off both email edges; the paper tears into the
    # Patriot water FIRST and the three bottom prints lie over the tear, crossing it by 40 css px or more (R11),
    # so no dead strip is left between the pile and the next band. Tile phase: paper rows from 942 (the collage
    # opens 471 css into the hero cell, measured in Chrome on 2026-10-08).
    W, H, Y0, TEAR = 1200, 1000, 942, 820
    cv = tile_canvas("paper-tapshoe", W, H, Y0)
    arr = np.asarray(cv.convert("RGB"), np.float32)
    cv = tear_into(arr, "flat:#202944", TEAR, seed=21, strip=90, amp=12, rough=9)   # round 6b: ragged, not straight
    win = border_window(W, H, 36, ("top", "bottom"))
    utv = Image.open(LIFE / "crop-sent-sep10-utv-hunters.jpg")
    tackle = Image.open(LIFE / "crop-sent-sep22-angler-tackle-box.jpg")
    blind = Image.open(LIFE / "crop-sent-sep2-hunter-blind.jpg")
    trout = Image.open(LIFE / "crop-sent-sep22-trout-in-hand.jpg")
    wade = Image.open(LIFE / "crop-sent-sep22-wading-river.jpg")
    # back to front: tackle, UTV, wading (centre), blind, trout
    place_rot(cv, framed(cover(tackle, 640, 330, 0.60, 0.5), 640, 12), 905, 212, 2.6, win=win)
    place_rot(cv, framed(cover(utv, 680, 372, 0.55, 0.5), 680, 12), 318, 220, -3.2, win=win)
    place_rot(cv, framed(cover(wade, 360, 560, 0.5, 0.55), 360, 12), 600, 615, 1.8, win=win)
    # round 6b (QA r6): cropped above the blurred bright foreground (y > 860 of 1276) again, as in round 2
    # and the daylight in the blind opening behind him rolled off (highlights above 190 compressed 0.45x), so
    # no pure-white patch is left in the print
    bl = np.asarray(blind.convert("RGB").crop((200, 0, 1081, 880)), np.float32)
    bl = np.where(bl > 190, 190 + (bl - 190) * 0.45, bl)
    bl = Image.fromarray(np.clip(bl, 0, 255).astype(np.uint8), "RGB")
    place_rot(cv, framed(cover(bl, 400, 500, 0.50, 0.40), 400, 12), 232, 650, 4.0, win=win)
    place_rot(cv, framed(cover(trout, 380, 520, 0.5, 0.55), 380, 12), 992, 640, -3.4, win=win)
    save_q(cv, "n2-hero-collage.jpg", 140 * 1024, q=76)

    return
    # (round 4 cards, replaced in round 6 by baked rows n2-p-1..6)
    # Cards, round 4: the card has its own flat Patriot fill; the packshot rises out of a rounded panel
    # (rev-oct-03), scaled up so it owns the card. The stocking cap is shown worn (store model photo 02,
    # the only store image with a face in the batch): a person in the grid. 660x588 = 2x of 330x294 (mobile).
    cards = [
        ("mens-flushing-bay-short-sleeve-river-shirt", ALUMINUM, None),
        ("mens-flushing-bay-long-sleeve-river-shirt", SLATE, None),
        ("habit-mens-wj657-cedar-branch-insulated-waterproof-bomber", DUSK, None),
        ("habit-mens-summit-park-performance-hoodie-1", TURKISH, None),
        ("mens-insulated-boot", IVY, None),
        ("knit-camo-stocking-cap", RUST, "02.png"),
    ]
    W, H = 660, 588
    for i, (h, col, alt) in enumerate(cards, 1):
        if alt:
            cut = store_cut(h, alt)
            # model portrait: head and shoulders cut by the panel bottom (no ground), face rising out of it
            panel_card(cut, col, PATRIOT, (W, H), (34, 250, W - 34, H), prod_h=580, bottom=H, top=H - 560,
                       name=f"n2-card-{i}.jpg", ground=False, radius=22)
        else:
            cut = packshot("02", h)
            ph = 530 if h != "mens-insulated-boot" else 470
            panel_card(cut, col, PATRIOT, (W, H), (34, 270, W - 34, H - 24), prod_h=ph, bottom=H - 50,
                       name=f"n2-card-{i}.jpg", radius=22)


def n3():
    print("03 Buck Hollow 2.0")
    # Round 6 (owner): the split hero (photo cut at the bottom and fading out on the left) becomes a FULL-BLEED
    # photo hero (ref1 New Terrain Guard: title set over the photo; ref6: lifestyle hero). orig-hunt40 kept:
    # it works full-bleed. The canopy above the hunter takes the live text; it is darkened locally (burn, inside
    # the photo) for AA, the hunter below stays untouched. The hero ends in a torn edge into the light paper of
    # the system band (-dm twin for the dark paper). Desktop and mobile have their own crops (mobile: tighter,
    # the hunter's head just under the button). Background image of the hero cell (VML + bgcolor fallback).
    ph = Image.open(LIFE / "orig-hunt40-hunter-forest-back.jpg").convert("RGB")
    W = ["#FFFFFF"]
    O = ["#FF6400"]
    # desktop 600 x 820 css: live text LEFT-aligned in the top-left corner (logo, kicker label, BUCK / HOLLOW 2.0,
    # subheadline, button: x 0-440, y 30-400 css); the darkening is a rounded corner patch over exactly that
    # block, easing out before the bow and the hunter's head (470 css); the right canopy and the hunter stay as
    # shot. 1:1 source pixels. The kicker sits on a dark label, so only white text is measured here.
    photo_hero(ph, "n3-hero.jpg", scale=1.0, crop_x=420, crop_y=0, H=1640, tear_y=1600,
               burn_ellipse=dict(rx=1300, ry=960, cx=0, cy=0, core=0.7, p=3), strength=0.66,
               next_tex="paper-light", dm_tex="paper-light-dm", seed=331, soften=1.35, soften_text=1.8, q=68,
               boxes={"logo": (W, (88, 80, 408, 132)), "headline": (W, (88, 324, 866, 556)),
                      "sub": (W, (88, 588, 808, 634))},
               limit=140 * 1024)
    # mobile 375 x 750 css, text left-aligned across the top (logo 28, label 80, headline 134-234, sub 246-290,
    # button 308-360 css), darkened as a top band easing out before the head (385 css); built at the 1200 px
    # tile scale (3.2 build px per css px) then written at 750 px.
    photo_hero(ph, "n3-hero-m.jpg", scale=1.316, crop_x=837, crop_y=0, H=2400, tear_y=2360,
               burn_ellipse=dict(rx=4000, ry=1220, cx=0, cy=0, core=0.7, p=3), strength=0.6,
               next_tex="paper-light", dm_tex="paper-light-dm", seed=332, soften=1.3, soften_text=1.8, q=68,
               boxes={"logo": (W, (77, 90, 589, 173)), "headline": (W, (77, 429, 1069, 749)),
                      "sub": (W, (77, 787, 1056, 928))},
               out_w=750, limit=100 * 1024)
    n3_tags()


def n4():
    print("04 Flannel")
    barn = Image.open(LIFE / "crop-sent-sep24-barn-door-feed-bag.jpg")
    save_jpg(framed(cover(barn, 1000, 760, 0.5, 0.40), 1000, 14), "n4-hero-photo.jpg", match=())
    stable = Image.open(LIFE / "crop-sent-sep24-stable-horse.jpg").convert("RGB")
    save_jpg(stable.crop((560, 14, 1200, 614)), "n4-m-stable.jpg", limit=70 * 1024)
    # Detail tiles, round 4: fabric only (no grey studio backdrop in the tile): the back yoke and pleat
    # cropped inside the garment, the pocket close-up cropped inside the fabric.
    back = store("mens-heavyweight-soft-flannel", "03.png")
    box = (480, 214, 780, 514)                     # yoke seam and the pleat under it, inside the fabric
    assert (np.asarray(back.crop(box).getchannel("A")) > 250).mean() > 0.995, "pleat tile must be fabric only"
    tile = remove_callout(back.convert("RGB"), (560, 170, 860, 320)).crop(box)
    save_jpg(tile.resize((288, 288), Image.LANCZOS), "n4-m-pleat.jpg", limit=40 * 1024)
    pocket = store("mens-heavyweight-soft-flannel", "06.png")
    pk = pocket.convert("RGB").crop((160, 300, 960, 1100))
    save_jpg(pk.resize((288, 288), Image.LANCZOS), "n4-m-pocket.jpg", limit=40 * 1024)


def tag_end(name: str, w: int, h: int, tone: str, side: str, seed: int) -> Path:
    """Torn end of a paper label (E33 device, round 6 tier headers and the 03 kicker): PNG-24 with real
    transparency (R5: it sits on any band, grain or flat, at any width, with no seam). The label body is a flat
    cell of the same colour; this file is its ripped end: paper up to a torn vertical line, the paper core
    showing along the rip, transparent beyond. side = 'r' (paper on the left) or 'l'."""
    base = {"light": (226, 221, 217), "dark": (42, 43, 45)}[tone]
    core = {"light": FIBRE, "dark": (92, 89, 86)}[tone]
    rnd = random.Random(seed)
    xs = [v + rnd.uniform(-0.9, 0.9) for v in C.torn_line(h, w * 0.42, amp=w * 0.22, seed=seed)]
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon([(0, 0)] + [(w - 1 - x, y) for y, x in enumerate(xs)] + [(0, h)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(0.6))
    rim = fibre_rim(m, seed + 1, widths=(1, 2, 3))
    rgb = np.broadcast_to(np.array(base, np.float32), (h, w, 3)).copy()
    r = rim[:, :, None] * 0.9
    rgb = rgb * (1 - r) + np.array(core, np.float32) * r
    arr = np.dstack([np.clip(rgb, 0, 255), np.asarray(m, np.float32)]).astype(np.uint8)
    im = Image.fromarray(arr, "RGBA")
    if side == "l":
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    p = OUT / name
    im.save(p, optimize=True)
    print(f"  {p.name:40s} {w}x{h}  {p.stat().st_size / 1024:5.1f} KB  (PNG-24, alpha)")
    return p


def n5():
    print("05 Gift Guide #2")
    utv = Image.open(LIFE / "orig-twofisted-utv-two-men.jpg")
    # Round 6 (owner: no blur/fade transitions): the photo is a torn print on the Tap Shoe paper (desktop:
    # ripped at the bottom, the logo stays on the dark UTV roof; mobile: ripped top and bottom, the logo sits
    # on the paper above it), the live text on the paper below, then the paper tears into the UNDER $30 band.
    paper_hero(utv, "n5-hero.jpg", size=(1200, 1680), photo_w=1200, photo_y=0, photo_h=806, sides=("bottom",),
               base="paper-tapshoe", next_tex="grain-brown", tear_y=1610, text_box=(60, 930, 1140, 1560),
               seed=95, limit=140 * 1024)
    paper_hero(utv, "n5-hero-m.jpg", size=(1200, 2300), photo_w=1440, crop_x=60, photo_y=196, photo_h=960,
               sides=("top", "bottom"), base="paper-tapshoe", next_tex="grain-brown", tear_y=2230,
               text_box=(60, 1260, 1140, 2160), seed=96, limit=90 * 1024, scale=0.625)
    oaks = Image.open(LIFE / "orig-hunt50-hunter-oaks-autumn.jpg").convert("RGB")
    oaks = cover(oaks, 1400, 840, 0.42, 0.55).resize((860, 516), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.15))
    torn_photo(oaks, "n5-closing-oaks.jpg", band="paper-camo", dm_band="paper-camo-dm",
               size=(1200, 620), photo_w=860, cx=600, cy=302, angle=-1.6, sides=("bottom", "right"), seed=117)
    for n in ("n5-closing-oaks.jpg", "n5-closing-oaks-dm.jpg"):      # round 6: weight, 05 back toward 800 KB
        save_q(Image.open(o(n)).convert("RGB"), n, 76 * 1024, q=74, floor=50)
    # Tier labels (round 6): light paper label ends, label 148 css tall on desktop (2x file).
    tag_end("n5-tag-light-r.png", 32, 296, "light", "r", 521)
    tag_end("n5-tag-light-l.png", 32, 296, "light", "l", 522)


def n3_tags():
    # 03 kicker label (NEW FOR 2026:), dark paper, 44 css tall, anchored on the left edge: right end only.
    tag_end("n3-tag-dark-r.png", 24, 88, "dark", "r", 531)


# ================================================================ bake: measured composites

BAKE_PROBE = r"""<script>window.addEventListener('load',()=>document.fonts.ready.then(()=>setTimeout(()=>{
document.querySelectorAll('img[width][height]').forEach(i=>{i.style.width=i.getAttribute('width')+'px';i.style.height=i.getAttribute('height')+'px';});
document.documentElement.setAttribute('data-theme','light');
const out=[...document.querySelectorAll('img[data-bake]')].map(e=>{const band=e.closest('td[data-tex]');
 const r=e.getBoundingClientRect(), b=band.getBoundingClientRect();
 let tr=band.closest('tr'); let p=tr.previousElementSibling; let ptd=p?p.firstElementChild:null;
 return {id:e.dataset.bake, src:e.getAttribute('src'), x:r.left-b.left, y:r.top-b.top, w:r.width, h:r.height,
  tex:band.dataset.tex, ptex:(ptd&&ptd.dataset)?(ptd.dataset.tex||null):null, ph:p?p.getBoundingClientRect().height:0};});
document.title='BAKE'+JSON.stringify(out);},400)));</script>"""


def measure(html_path: Path, probe_js: str, tag: str) -> list:
    import html as H, re, subprocess
    src = html_path.read_text(encoding="utf-8").replace("</body>", probe_js + "</body>")
    probe = html_path.with_name("_probe.html")
    probe.write_text(src, encoding="utf-8")
    try:
        dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                              "--hide-scrollbars", "--window-size=680,3000", "--force-prefers-color-scheme=light",
                              "--virtual-time-budget=10000", "--dump-dom", probe.as_uri()],
                             capture_output=True, text=True, encoding="utf-8").stdout
    finally:
        probe.unlink()
    m = re.search(rf"<title>{tag}(.*?)</title>", dom, re.S)
    return json.loads(H.unescape(m.group(1)))


def variants(rec: dict) -> list[tuple[str, str, str | None]]:
    """("", tex, ptex) and, when a light paper is involved, ("-dm", dm tex, dm ptex)."""
    v = [("", rec["tex"], rec.get("ptex"))]
    if rec["tex"] in DM_OF or (rec.get("rise") and rec.get("ptex") in DM_OF):
        v.append(("-dm", DM_OF.get(rec["tex"], rec["tex"]), DM_OF.get(rec.get("ptex"), rec.get("ptex"))))
    return v


def base_canvas(rec: dict, tex: str, ptex: str | None, under=None) -> tuple[Image.Image, dict]:
    """The band's own tile at the measured place; for a rise image, the band above (measured phase) torn
    over it at css row rec['hu']. `under(canvas, info)` draws what lies BELOW the torn sheet (a photo)."""
    W, H = round(rec["w"] * 2), round(rec["h"] * 2)
    x0, y0 = round(rec["x"] * 2), round(rec["y"] * 2)
    info = {"W": W, "H": H, "x0": x0, "y0": y0}
    lower = tex_region(tex, x0, y0, W, H)
    if not rec.get("rise"):
        cv = C.to_image(lower)
        if under:
            under(cv, info)
        return cv, info
    assert y0 == 0, f"{rec['id']}: a rise image must open its band cell (y={rec['y']})"
    assert ptex, f"{rec['id']}: no band above"
    hu2 = rec["hu"] * 2
    strip = hu2 + 40
    seed = rec["seed"]
    lo_full = tex_region(tex, 0, 0, 1200, strip)
    up_full = tex_region(ptex, 0, round(rec["ph"] * 2), 1200, strip)
    ys_full = C.torn_line(1200, hu2, amp=8, seed=seed)
    m = Image.new("L", (1200, strip), 0)
    ImageDraw.Draw(m).polygon([(0, strip)] + [(x, y) for x, y in enumerate(ys_full)] + [(1200, strip)], fill=255)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(0.8)), np.float32)[:, :, None] / 255
    up_rgb = np.median(up_full[: hu2 // 2].reshape(-1, 3), 0)
    lo_rgb = np.median(lo_full[hu2 + 8:].reshape(-1, 3), 0)
    C.tear_shadow(up_full, ys_full)
    # lower sheet = the band's tile with whatever lies under the tear (a photo) drawn on it
    low = C.to_image(lower)
    if under:
        under(low, info)
    low_arr = np.asarray(low.convert("RGB"), np.float32)
    s = min(strip, H)
    arr = low_arr.copy()
    mp = m[:s, x0:x0 + W]
    arr[:s] = up_full[:s, x0:x0 + W] * (1 - mp) + low_arr[:s] * mp
    cv = C.to_image(arr)
    specks(cv, ys_full, up_rgb, lo_rgb, seed + 1, x_off=x0)
    info["tear_y"] = hu2
    return cv, info


# Rise images: css height of the band above that the image keeps (torn line at hu), seed of the torn line.
# Round 6: n3-sys no longer rises (the 03 hero is a full-bleed photo whose torn edge is baked in it).
RISE = {
    "n1-p-parka": (64, 401), "n1-p-sherpa": (64, 402), "n1-close": (34, 403),
    "n3-strip": (40, 432),
    "n4-pair": (64, 441),
    "n5-lead": (56, 451),
}


def J(fn, limit=95 * 1024, sides=("top", "bottom", "left", "right"), under=None, q=None):
    return {"fn": fn, "limit": limit, "sides": sides, "under": under, "q": q}


# ---- 01

def b_n1_hero(cv, i, win):
    pass


def u_n1_hero(cv, i):
    """Women's line in use: crop-sent-sep15 (woman in Realtree, with her family, walking into the woods).
    Round 6: no melt. The photo is a full-width torn print lying on the Ivy grain, ripped along its top and
    bottom (white paper core, cast shadow below); the band's own tile shows above and below it (R1)."""
    ph = Image.open(LIFE / "crop-sent-sep15-family-forest-walk.jpg").convert("RGB")      # 1200 x 610
    ph = ph.crop((0, 0, 1200, min(ph.height, i["H"] - 40)))
    win = border_window(i["W"], i["H"], 18, ("top", "bottom"))
    torn_sheet(cv, ph, 0, 16, ("top", "bottom"), 611, depth=7, amp=5, shadow=(5, 8, 7, 0.45), win=win, tone=0.97)


def b_n1_bib(cv, i, win):
    p = fit(packshot("01", "womens-cedar-branch-insulated-bib"), h=900)
    put(cv, p, i["W"] / 2 - p.width / 2 - 10, i["H"] - 44 - p.height, win=win)


def b_n1_parka(cv, i, win):
    """Parka rises over the torn edge into the brown band and is cut by the email's right edge."""
    p = fit(packshot("01", "habit-womens-cedar-branch-insulated-parka"), h=960)
    put(cv, p, 48, 28, ground=False, win=win)


def b_n1_sherpa(cv, i, win):
    p = fit(packshot("01", "womens-early-dawn-sherpa-shell-jacket"), h=800)
    put(cv, p, i["W"] / 2 - p.width / 2 + 4, 40, win=win)


def u_n1_close(cv, i):
    """Last call: crop-sent-sep15 camp chairs, the woman in the Women's Cedar Branch parka, bleeding off the
    email's left edge under the torn brown sheet. Round 6: no melt; the print is ripped on its right and
    bottom sides (white core, cast shadow on the Ivy grain)."""
    ph = Image.open(LIFE / "crop-sent-sep15-camp-chairs-family.jpg").convert("RGB").crop((0, 0, 560, 514))
    ph = fit(ph, w=640).crop((0, 0, 560, 548))
    win = border_window(i["W"], i["H"], 30, ("bottom", "right"))
    torn_sheet(cv, ph, -24, 52, ("right", "bottom"), 612, depth=9, amp=7, win=win, tone=0.96)


# ---- 02

def b_n2_gift(cv, i, win):
    """Gift card over a framed photo of a hunter (crop-sent-sep10 truck hunter): people + the card."""
    truck = Image.open(LIFE / "crop-sent-sep10-truck-hunter.jpg").convert("RGB").crop((520, 30, 1200, 670))
    gc = Image.open(ROOT / [p for p in PRODUCTS if p["handle"] == "gift-card"][0]["image_file"]).convert("RGB")
    W, H = i["W"], i["H"]
    place_rot(cv, framed(truck, int(W * 0.56), 12), W * 0.34, H * 0.33, 4.0, win=win)
    place_rot(cv, framed(gc, int(W * 0.70), 10), W * 0.56, H * 0.66, -4.0, win=win)


N2 = ["mens-flushing-bay-short-sleeve-river-shirt", "mens-flushing-bay-long-sleeve-river-shirt",
      "habit-mens-wj657-cedar-branch-insulated-waterproof-bomber", "habit-mens-summit-park-performance-hoodie-1",
      "mens-insulated-boot", "knit-camo-stocking-cap"]


def b_n2_row(k):
    """Round 6: 02 product rows on the Patriot water (05 pattern). 1, 2, 4 standing big on a ground line;
    3 bomber cut by the email's left edge (no ground); 5 boots big; 6 the cap on a ground line in front of a
    people photo that bleeds off the right edge (grouped, so the small cap does not float)."""
    def fn(cv, i, win):
        W, H = i["W"], i["H"]
        cut = packshot("02", N2[k])
        if k == 2:                                                # bomber, bleeds left
            p = fit(cut, h=H - 50)
            put(cv, p, -70, 26, ground=False, win=win)
        elif k == 5:                                              # cap + people photo
            p = fit(cut, w=int(W * 0.50))
            put(cv, p, 30, H - 44 - p.height, win=win)
        else:
            p = fit(cut, h=H - 60)
            if p.width > W - 20:
                p = fit(cut, w=W - 20)
            # tops get only the cast shadow; the boots stand on a ground (contact shadow)
            put(cv, p, W / 2 - p.width / 2, H - 34 - p.height, win=win, ground=(k == 4))
    return fn


def u_n2_cap(cv, i):
    """People photo behind the cap. Round 6b (QA r6): crop-sent-sep22-boat-anglers (three anglers on a boat,
    fly fishing; not used anywhere else in November, a different scene from every collage print) instead of the
    UTV hunter, which repeated the collage's UTV scene one screen above. Landscape torn print (ripped left, top
    and bottom, R8: no gradient) in the upper right, running off the right edge; the cap stands in front of its
    lower-left corner."""
    ph = Image.open(LIFE / "crop-sent-sep22-boat-anglers.jpg").convert("RGB")       # 594 x 254
    W, H = i["W"], i["H"]
    pw, phh = 470, 300
    crop = cover(ph, pw, phh, 0.42, 0.45)
    win = border_window(W, H, 18, ("top", "bottom", "left"))
    torn_sheet(cv, crop, W - pw, 236, ("left", "top", "bottom"), 621, depth=8, amp=6, win=win, tone=0.97)


# ---- 03

def b_n3_sys(cv, i, win):
    """System shot: jacket worn over the pant (store packshots), big, standing on the light paper. Round 6:
    no longer crosses into the hero (the hero is a full-bleed photo with its torn edge baked in)."""
    pt = fit(packshot("03", "mens-buck-hollow-2-0-pant"), h=760)
    jk = fit(store_cut("mens-buck-hollow-2-0-jacket", "02.png"), h=600)
    cx = i["W"] / 2 + 6
    gy = i["H"] - 40
    put(cv, pt, cx - pt.width / 2, gy - pt.height, win=win)
    put(cv, jk, cx - jk.width / 2, max(30, gy - pt.height - 470), ground=False, win=win)


def u_n3_strip(cv, i):
    """Full-bleed people strip, orig-hunt22 (three hunters walking up the field at sunrise), under the torn light
    paper at the top (rise). Round 6: no melt at the bottom; the print is ripped there (white core, shadow on
    the Patriot water)."""
    ph = Image.open(LIFE / "orig-hunt22-three-hunters-field-sunrise.jpg").convert("RGB")
    W, H = i["W"], i["H"]
    crop = cover(ph, W, H - 44, 0.40, 0.58).filter(ImageFilter.GaussianBlur(0.8))
    win = border_window(W, H, 16, ("bottom",))
    torn_sheet(cv, crop, 0, 0, ("bottom",), 613, depth=10, amp=8, win=win, tone=0.97)


def b_n3_jacket(cv, i, win):
    """Round 6 stagger (ref4): jacket big, inside the column (about 24 css from the email edge, no bleed),
    standing on its ground line."""
    p = fit(store_cut("mens-buck-hollow-2-0-jacket", "02.png"), w=i["W"] - 2 * 40)
    put(cv, p, 44, i["H"] - 36 - p.height, win=win, ground=False)


def b_n3_pant(cv, i, win):
    """Round 6 stagger: pant big, standing, centred in its column (no bleed)."""
    p = fit(packshot("03", "mens-buck-hollow-2-0-pant"), h=i["H"] - 80)
    put(cv, p, i["W"] / 2 - p.width / 2 - 6, i["H"] - 40 - p.height, win=win)


# ---- 04

def b_n4_pair(cv, i, win):
    """The two colours, big, overlapping on one ground line: Major Brown behind, Rifle Green in front with its
    collar crossing the torn edge into the halftone band."""
    br = fit(packshot("04", "mens-heavyweight-soft-flannel", "Major Brown"), h=700)
    g = fit(packshot("04", "mens-heavyweight-soft-flannel", "Rifle Green"), h=780)
    ground = i["H"] - 40
    put(cv, br, 700, ground - br.height, win=win)
    put(cv, g, 250, ground - g.height, win=win)


# ---- 05 (round 6: one layout per price tier, see build_emails.email_05)

P5 = {   # key: (handle, alternative store image or None)
    "breaking": ("mens-breaking-dawn-camp-short-sleeve-fishing-shirt", None),
    "siesta": ("mens-siesta-cape-long-sleeve-performance-tee-1", None),
    "hybrid": ("mens-outdoor-hybrid-hoodie", None),
    "gloves": ("all-purpose-camo-leather-gloves", None),
    "bomber": ("mens-3-season-bomber-jacket", None),
    "zip": ("mens-heavy-weight-full-zip-hoodie", None),
    "sherpa": ("mens-sherpa-lined-canvas-jacket", None),
    "rainbib": ("men-s-angler-s-bluff-rain-bib", "01.png"),
    "ssbib": ("mens-shadow-series-anglers-bluff-rain-bib", None),
    "ssjacket": ("mens-shadow-series-anglers-bluff-rain-jacket", None),
    "insbib": ("men-s-waterproof-insulated-bib", None),
}


def cut5(k: str) -> Image.Image:
    h, alt = P5[k]
    return store_cut(h, alt) if alt else packshot("05", h)


def b_n5_grid(k):
    """UNDER $30, 2x2 grid cell: the product big on the brown grain, standing on one ground line."""
    def fn(cv, i, win):
        W, H = i["W"], i["H"]
        p = fit(cut5(k), h=H - 70)
        if p.width > W - 60:
            p = fit(cut5(k), w=W - 60)
        # tops and gloves hang / lie: cast shadow only, no contact blobs under the hem (round 4-5 lesson)
        put(cv, p, W / 2 - p.width / 2, H - 34 - p.height, win=win, ground=False)
    return fn


def b_n5_lead(cv, i, win):
    """UNDER $100 lead: the bomber, big, rising over the torn edge into the UNDER $30 band (inside the column,
    no bleed: about 24 css from the email edge)."""
    W, H = i["W"], i["H"]
    p = fit(cut5("bomber"), w=W - 96)
    put(cv, p, 52, H - 40 - p.height, win=win, ground=False)


def b_n5_group(cv, i, win):
    """UNDER $100 secondary picks, grouped (ref5): the full zip hoodie, the sherpa canvas jacket and the
    Angler's Bluff rain bib on one ground line, left to right in the order of the list under them, the
    jacket overlapping the hoodie and the bib in front of the jacket's sleeve."""
    W, H = i["W"], i["H"]
    g = H - 50
    zh = fit(cut5("zip"), h=560)
    sj = fit(cut5("sherpa"), h=580)
    rb = fit(cut5("rainbib"), h=700)
    total = zh.width + sj.width + rb.width - 110 - 40
    x = W / 2 - total / 2
    put(cv, zh, x, g - zh.height, win=win, ground=False)
    x += zh.width - 110
    put(cv, sj, x, g - sj.height, win=win, ground=False)
    x += sj.width - 40
    put(cv, rb, x, g - rb.height, win=win)


def b_n5_set(cv, i, win):
    """UNDER $120 set (ref3 pair): the Shadow Series rain bib and its matching rain jacket, big, overlapping
    on one ground line; bib on the left (first in the copy), jacket on the right."""
    W, H = i["W"], i["H"]
    g = H - 46
    bib = fit(cut5("ssbib"), h=H - 110)
    jk = fit(cut5("ssjacket"), h=H - 210)
    x0 = W / 2 - (bib.width + jk.width - 70) / 2
    put(cv, bib, x0, g - bib.height, win=win)
    put(cv, jk, x0 + bib.width - 70, g - jk.height, win=win, ground=False)


def b_n5_top(cv, i, win):
    """UNDER $120 highlight ('The top-shelf gift'): the insulated bib, tall, standing."""
    W, H = i["W"], i["H"]
    p = fit(cut5("insbib"), h=H - 90)
    put(cv, p, W / 2 - p.width / 2, H - 40 - p.height, win=win)


BAKERS = {
    "n2-p-1": J(b_n2_row(0), limit=40 * 1024), "n2-p-2": J(b_n2_row(1), limit=40 * 1024),
    "n2-p-3": J(b_n2_row(2), limit=60 * 1024, sides=("top", "bottom", "right")),
    "n2-p-4": J(b_n2_row(3), limit=45 * 1024), "n2-p-5": J(b_n2_row(4), limit=55 * 1024),
    "n2-p-6": J(b_n2_row(5), limit=60 * 1024, sides=("top", "bottom", "left"), under=u_n2_cap, q=74),
    "n1-hero": J(b_n1_hero, limit=88 * 1024, under=u_n1_hero, q=72),
    "n1-p-bib": J(b_n1_bib, limit=56 * 1024, sides=("top", "bottom", "right")),
    "n1-p-parka": J(b_n1_parka, limit=82 * 1024, sides=("top", "bottom", "left")),
    "n1-p-sherpa": J(b_n1_sherpa, limit=76 * 1024, sides=("top", "bottom", "right")),
    "n1-close": J(lambda cv, i, w: None, limit=80 * 1024, under=u_n1_close, q=72),
    "n2-gift": J(b_n2_gift, limit=90 * 1024),
    "n3-sys": J(b_n3_sys, limit=98 * 1024),
    "n3-strip": J(lambda cv, i, w: None, limit=98 * 1024, under=u_n3_strip, q=72),
    "n3-p-jacket": J(b_n3_jacket, limit=80 * 1024),
    "n3-p-pant": J(b_n3_pant, limit=70 * 1024),
    "n4-pair": J(b_n4_pair, limit=120 * 1024),
    "n5-g-1": J(b_n5_grid("breaking"), limit=40 * 1024),
    "n5-g-2": J(b_n5_grid("siesta"), limit=40 * 1024),
    "n5-g-3": J(b_n5_grid("hybrid"), limit=40 * 1024),
    "n5-g-4": J(b_n5_grid("gloves"), limit=40 * 1024),
    "n5-lead": J(b_n5_lead, limit=56 * 1024),
    "n5-group": J(b_n5_group, limit=80 * 1024),
    "n5-set": J(b_n5_set, limit=72 * 1024),
    "n5-top": J(b_n5_top, limit=48 * 1024),
}


def bake(only: set[str] | None = None):
    print("bake: composites on measured band positions")
    import os
    pick = os.environ.get("BAKE_ONLY")                    # e.g. BAKE_ONLY=02 bakes one email
    for f in sorted(HERE.glob("0*.html")):
        if pick and not f.name.startswith(pick):
            continue
        recs = measure(f, BAKE_PROBE, "BAKE")
        for rec in recs:
            rid = rec["id"]
            if only and rid.split("~")[0][:2] not in only:
                continue
            piece = rid.endswith("~t")
            key = rid[:-2] if piece else rid
            if key in RISE:
                rec["rise"] = True
                rec["hu"], rec["seed"] = RISE[key]
            job = BAKERS.get(key) if not piece else J(lambda cv, i, w: None, limit=30 * 1024)
            if job is None:
                raise KeyError(f"no baker for {rid}")
            for suffix, tex, ptex in variants(rec):
                cv, info = base_canvas(rec, tex, ptex, under=job["under"])
                if rec.get("rise"):
                    info["tear_y"] = rec["hu"] * 2
                win = border_window(info["W"], info["H"], 40, job["sides"])
                job["fn"](cv, info, win)
                name = Path(rec["src"]).name.replace(".jpg", f"{suffix}.jpg")
                if job["q"] or piece:
                    save_q(cv, name, job["limit"], q=job["q"] or 76)
                else:
                    save_q(cv, name, job["limit"], q=80, floor=54)
                print(f"      {rid}{suffix}: {tex} at css x {rec['x']:.0f} y {rec['y']:.0f}"
                      + (f", rises over {ptex} (band above {rec['ph']:.0f}px, tear at {rec['hu']})" if rec.get("rise") else ""))
                seam(name, tex, info, rec)


def seam(name: str, tex: str, info: dict, rec: dict) -> None:
    """R1 check: mean deviation (levels) of the saved file's border rows and columns against the tile they
    continue, on the sides that touch the band (rise images: the bottom and the inner side below the tear)."""
    im = np.asarray(Image.open(o(name)).convert("RGB"), np.float32)
    H, W = im.shape[:2]
    x0, y0 = info["x0"], info["y0"]
    if tex.startswith("flat:"):
        ref = lambda r0, r1, c0, c1: np.broadcast_to(np.array(C.rgb(tex[5:]), np.float32), (r1 - r0, c1 - c0, 3))
    else:
        ref = lambda r0, r1, c0, c1: tex_region(tex, x0 + c0, y0 + r0, c1 - c0, r1 - r0)
    out = []
    ty = info.get("tear_y", 0) + 40
    out.append(("bottom", abs(im[-2:].mean() - ref(H - 2, H, 0, W).mean())))
    if ty < H - 10 and x0 > 0:                       # a side on the email edge is not a seam
        out.append(("left", abs(im[ty:, :2].mean() - ref(ty, H, 0, 2).mean())))
    if ty < H - 10 and x0 + W < 1200:
        out.append(("right", abs(im[ty:, -2:].mean() - ref(ty, H, W - 2, W).mean())))
    if not rec.get("rise"):
        out.append(("top", abs(im[:2].mean() - ref(0, 2, 0, W).mean())))
    print("      seam " + "  ".join(f"{k} {v:.1f}" for k, v in out))


# ================================================================ torn edges, driven by the built HTML

EDGE_PROBE = r"""<script>window.addEventListener('load',()=>document.fonts.ready.then(()=>setTimeout(()=>{
document.querySelectorAll('img[width][height]').forEach(i=>{i.style.width=i.getAttribute('width')+'px';i.style.height=i.getAttribute('height')+'px';});
document.documentElement.setAttribute('data-theme','light');
const out=[...document.querySelectorAll('img.edge[data-edge-top]')].map(e=>{const tr=e.closest('tr'); let p=tr.previousElementSibling;
 return [e.getAttribute('src'), e.dataset.edgeTop, e.dataset.edgeBottom, p?p.getBoundingClientRect().height:0];});
document.title='EDGES'+JSON.stringify(out);},400)));</script>"""


def phased_edge(top: str, bottom: str, out: Path, band_h: float, seed: int, dm: dict | None = None):
    """E18 textured torn edge whose upper texture rows continue the band above at its tile phase."""
    h = 80
    variants_ = [("", top, bottom)]
    if dm:
        variants_.append(("-dm", dm.get("top", top), dm.get("bottom", bottom)))
    for suffix, tname, bname in variants_:
        up = tex_region(tname, 0, int(round(band_h * 2)), C.TEX_W, h)
        lo = C.tile_rows(bname, h, end=True)
        ys = C.torn_line(C.TEX_W, h * 0.45, amp=8, seed=seed)
        m = Image.new("L", (C.TEX_W, h), 0)
        ImageDraw.Draw(m).polygon([(0, h)] + [(x, y) for x, y in enumerate(ys)] + [(C.TEX_W, h)], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(0.8))
        a = np.asarray(m, np.float32)[:, :, None] / 255
        up_rgb = np.median(up.reshape(-1, 3), 0)
        C.tear_shadow(up, ys)
        canvas = C.to_image(up * (1 - a) + lo * a)
        specks(canvas, ys, up_rgb, np.median(lo.reshape(-1, 3), 0), seed + 1)
        p = C.save_jpg_under(canvas, out.with_name(out.stem + suffix + ".jpg"), 30 * 1024, q=76, subsampling=0)
        print(f"  {p.name:40s} band above {band_h:6.1f}px  {p.stat().st_size / 1024:5.1f} KB  {tname} / {bname}")


def edges():
    print("torn edges (phase-matched to the measured band heights)")
    for f in sorted(HERE.glob("0*.html")):
        for i, (src, top, bottom, h) in enumerate(measure(f, EDGE_PROBE, "EDGES")):
            dm = None
            if top in DM_OF or bottom in DM_OF:
                dm = {"top": DM_OF.get(top, top), "bottom": DM_OF.get(bottom, bottom)}
            phased_edge(top, bottom, HERE / src, h, seed=int(f.name[:2]) * 10 + i, dm=dm)


def clean():
    """Remove every file in assets/ that none of the five built HTML files references."""
    import re
    html = "".join(f.read_text(encoding="utf-8") for f in sorted(HERE.glob("0*.html")))
    used = set(re.findall(r"assets/(n\d-[\w.~-]+)", html))
    used |= {u.replace(".jpg", "-dm.jpg") for u in used}
    for p in sorted(OUT.glob("*")):
        if p.name not in used:
            p.unlink()
            print(f"  removed {p.name}")


JOBS = {"n1": n1, "n2": n2, "n3": n3, "n4": n4, "n5": n5, "bake": bake, "edges": edges, "clean": clean}

if __name__ == "__main__":
    for k in (sys.argv[1:] or ["n1", "n2", "n3", "n4", "n5", "bake", "edges"]):
        JOBS[k]()
