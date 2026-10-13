"""RKU26013 V3 (2026-10-12): split layout, CTV 16:9 only. Meta sizes stay V2 (make.py).

Light lilac panel on the left with lockup, headline and CTA; the room (same V2 plates, city and
TV ad) fills the rest. The headline is set per line and shrunk to fit; then the panel is cut down
so the space right of the longest line equals the left margin. The square plate (same as the
Meta 1:1) is scaled to the frame height and centered in the space right of the panel, so the
whole scene shows (dog, table, plant); it is scaled up only if that space is wider than the photo.

    python -I split.py            -> all industries
    python -I split.py pet        -> one industry
"""
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "01-brand"))
sys.path.insert(0, str(HERE))
from rk_common import font_face, img_data, lockup  # noqa: E402
from compose import city  # noqa: E402
from detect import detect  # noqa: E402
from make import CHROME, CTV_PLATE, EXPORT, IND, PLATE_FOR, RAW, glass_mask, put_screen, recolor_top  # noqa: E402

BG, BUILD = HERE / "img" / "split", HERE / "build" / "split"
PLATE = "{ind}-plate-1x1.png"   # storyboard.py switches this to the one-room spot plates (spot.py)

# 2560x1440 to match the CTV boards in the Figma file (Lucas, 2026-10-12); was 1920x1080, all sizes x 4/3
W, H = 2560, 1440
PADX, PADY = 149, 139        # panel margins; the panel's right margin is set to PADX too
HL, CTA, LK = 146, 45, 440   # headline (same size in every industry, sized so "wellness brand" fits), CTA, lockup
SLACK = 1.12                 # headline box is this much wider than its longest line in the static
                             # HTML, so a Figma import (font measured slightly wider) never re-wraps
T = {"bg": "#EFE6FF", "ink": "#20004C", "hi": "#4F01A3", "rk": "#4F01A3", "am": "#646464",
     "btn": "#4F01A3", "btn_ink": "#FFFFFF", "shadow": "rgba(32,0,76,.24)"}


def plate(ind, tv_on=True):
    """Square plate with the city keyed into the glass and (tv_on) the ad on the TV, plate resolution."""
    path = RAW / PLATE.format(ind=ind)
    if PLATE.endswith("-1x1.png") and ind in PLATE_FOR:          # the industry's one room
        path = RAW / f"{ind}-plate-{CTV_PLATE.get(ind, PLATE_FOR[ind])}.png"
    tv = detect(path)["tv"]
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    if a.shape[0] > a.shape[1]:                                   # tall room (Food): square crop with
        top = int(np.clip((tv[1] + tv[3]) / 2 - 0.416 * a.shape[1], 0, a.shape[0] - a.shape[1]))
        a = a[top:top + a.shape[1]]                               # the TV where the 1:1 rooms have it
        tv = (tv[0], tv[1] - top, tv[2], tv[3] - top)
    k, (gx0, gy0, gx1, gy1) = glass_mask(a, tv)
    art = np.full_like(a, 255)
    art[gy0:gy1, gx0:gx1] = np.asarray(city(gx1 - gx0, gy1 - gy0)).astype(np.float32)
    raw = a.copy()
    recolor_top(a, tv, k)
    a = a + k[..., None] * (art - 255)
    if tv_on:
        put_screen(a, raw, tv, ind)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)), tv


def photo(ind, tv_on=True):
    im, tv = plate(ind, tv_on)
    s = H / im.height
    out = im.resize((round(im.width * s), H), Image.LANCZOS)
    BG.mkdir(parents=True, exist_ok=True)
    p = BG / f"{ind}-16x9{'' if tv_on else '-off'}.png"
    out.save(p)
    return p, out.width, tuple(round(v * s) for v in tv)


def html(ind, img, iw, box, show=4, cta="on", tv_on=True, panel=0):
    """show = headline lines visible (hidden ones keep their space), cta = on | off | pressed,
    tv_on = ad on the TV, panel = fixed panel width (storyboard: same split in every frame)."""
    d = IND[ind]
    x0, y0, x1, y1 = box
    sw, sh = x1 - x0, y1 - y0
    h1, sub, adcta = d["ad"]
    hide = ' style="visibility:hidden"'
    hl = "".join(f'<span{"" if n < show else hide}>{t}</span>'
                 for n, t in enumerate(["Put your", f'<b>{d["word"]}</b>', "in their", "living room."]))
    cta_style = {"on": "", "off": ' style="visibility:hidden"',
                 "pressed": ' style="background:#20004C;box-shadow:0 0 0 10px rgba(133,61,255,.35)"'}[cta]
    scr = (f'<div class="scr"><span class="ad">Ad · 0:15</span><div class="t"><h2>{h1}</h2><p>{sub}</p>'
           f'<span class="b">{adcta}</span></div></div>') if tv_on else ""
    return f"""<!doctype html><meta charset="utf-8"><title>RKU26013 {ind} 16x9 V3</title>
<style>
{font_face()}
html,body{{margin:0;background:#fff}}
.f{{position:relative;width:{W}px;height:{H}px;overflow:hidden;font-family:"Roku Display",sans-serif}}
.i{{position:absolute;left:{W - iw}px;top:0;width:{iw}px;height:{H}px;background:url({img_data(img, "image/png")}) 0 0/{iw}px {H}px}}
.p{{position:absolute;left:0;top:0;width:{W // 2}px;height:{H}px;box-sizing:border-box;padding:{PADY}px {PADX}px;background:{T["bg"]};
   display:flex;flex-direction:column;justify-content:center;gap:{round(HL * .42)}px}}
.p>*{{flex-shrink:0}}
.lk{{width:{LK}px;height:auto;display:block}}
.hl{{margin:0;font-weight:700;font-size:{HL}px;line-height:1.02;letter-spacing:-.025em;color:{T["ink"]}}}
.hl span{{display:block;white-space:nowrap;width:max-content}}
.hl b{{font-weight:700;color:{T["hi"]}}}
.cta{{align-self:flex-start;display:flex;align-items:center;gap:{round(CTA * .5)}px;background:{T["btn"]};color:{T["btn_ink"]};font-weight:700;font-size:{CTA}px;line-height:1;
     padding:{round(CTA * .66)}px {round(CTA * 1.3)}px;border-radius:{round(CTA * .35)}px;box-shadow:0 {round(CTA * .3)}px {round(CTA * .9)}px {T["shadow"]};white-space:nowrap}}
.cta svg{{width:{round(CTA * .5)}px;height:{round(CTA * .8)}px}}
.scr{{position:absolute;left:{x0}px;top:{y0}px;width:{sw}px;height:{sh}px}}
.scr .t{{position:absolute;left:{round(sw * .065)}px;top:{round(sh * .2)}px;display:flex;flex-direction:column;gap:{round(sw * .022)}px;color:#fff}}
.scr h2{{margin:0;font-weight:700;font-size:{round(sw * .058)}px;line-height:1.08;letter-spacing:-.01em}}
.scr p{{margin:0;font-weight:400;font-size:{round(sw * .028)}px;line-height:1.3;color:#E9DEFF}}
.scr .b{{align-self:flex-start;margin-top:{round(sw * .012)}px;background:#fff;color:#4F01A3;font-weight:700;font-size:{round(sw * .025)}px;padding:{round(sw * .012)}px {round(sw * .027)}px;border-radius:999px}}
.scr .ad{{position:absolute;right:{round(sw * .03)}px;top:{round(sw * .025)}px;font-size:{round(sw * .018)}px;font-weight:500;color:#fff;background:rgba(0,0,0,.35);padding:{round(sw * .006)}px {round(sw * .014)}px;border-radius:6px}}
</style>
<div class="f">
  <div class="i">{scr}</div>
  <div class="p">
    {lockup("lk", T["rk"], T["am"])}
    <h1 class="hl">{hl}</h1>
    <div class="cta"{cta_style}>Learn more<svg viewBox="0 0 10 16" aria-hidden="true"><path d="M2 1.5 8.5 8 2 14.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
  </div>
</div>
<script>
// fit the headline to the half-width panel, then cut the panel to the text: right margin = left margin
document.fonts.ready.then(() => {{
  const p = document.querySelector('.p'), h = document.querySelector('.hl');
  const widest = () => Math.max(...[...h.children].map(s => s.getBoundingClientRect().width));
  let fs = {HL};
  while (fs > 40 && widest() > {W // 2 - 2 * PADX}) h.style.fontSize = (fs -= 2) + 'px';
  const inner = Math.max(widest(), document.querySelector('.lk').getBoundingClientRect().width);
  const pw = {panel} || Math.ceil(inner + 2 * {PADX});
  p.style.width = pw + 'px';
  const i = document.querySelector('.i'), room = {W} - pw;
  i.style.left = (pw + (room - {iw}) / 2) + 'px';
  const sc = room > {iw} ? room / {iw} : 1;
  document.body.setAttribute('data-fit', [pw, pw + (room - {iw}) / 2, sc, fs, widest()].join(','));
}});
</script>"""


def fit(page):
    """Run the fit script in Chrome: panel width, room left, room scale, headline size, widest line."""
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=3000",
                          f"--window-size={W},{H}", "--dump-dom", page.as_uri()],
                         capture_output=True, text=True, encoding="utf8").stdout
    return re.search(r'data-fit="([^"]+)"', dom).group(1).split(",")


def bake(page):
    """Write the fit result as plain CSS (no script), so the HTML imports into Figma exactly as
    rendered. The room must already be at scale 1 (see build): Figma ignores CSS transforms, which
    left the TV copy offset and oversized on the screen (Lucas, 2026-10-12)."""
    pw, il, sc, fs, widest = fit(page)
    assert abs(float(sc) - 1) < 1e-6, sc
    t = page.read_text(encoding="utf8")
    t = re.sub(r"<script>.*?</script>", "", t, flags=re.S)
    t = t.replace('<div class="p">', f'<div class="p" style="width:{pw}px">')
    t = t.replace('<div class="i">', f'<div class="i" style="left:{il}px">')
    t = t.replace('<h1 class="hl">', f'<h1 class="hl" style="font-size:{fs}px;width:{math.ceil(float(widest) * SLACK)}px">')
    return t


def build(ind, name=None, png_name=None, **kw):
    tv_on = kw.get("tv_on", True)
    img, iw, box = photo(ind, tv_on)
    BUILD.mkdir(parents=True, exist_ok=True)
    page = BUILD / (name or f"{ind}-16x9.html")
    page.write_text(html(ind, img, iw, box, **kw), encoding="utf8")
    sc = float(fit(page)[2])
    if sc > 1:                                   # room wider than the photo: enlarge the photo itself
        im = Image.open(img)
        big = im.resize((math.ceil(iw * sc), math.ceil(H * sc)), Image.LANCZOS)
        off = (big.height - H) // 2
        big.crop((0, off, big.width, off + H)).save(img)
        iw = big.width
        box = (round(box[0] * sc), round(box[1] * sc) - off, round(box[2] * sc), round(box[3] * sc) - off)
        page.write_text(html(ind, img, iw, box, **kw), encoding="utf8")
    page.write_text(bake(page), encoding="utf8")
    png = EXPORT / (png_name or f"RKU26013-SellItOnRoku-{W}x{H}-Static-CTV-{IND[ind]['code']}-V3.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--virtual-time-budget=3000", f"--window-size={W},{H}", f"--screenshot={png}", page.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return png


if __name__ == "__main__":
    for i in (sys.argv[1:] or IND):
        print(build(i).name)
