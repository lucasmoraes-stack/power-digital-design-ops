"""Build the Katapult social templates (the Design System's Templates section) from the Figma source.

Source: Figma "Progressive Global - LAB", section "/templates - Katapult" (node 547:1042), 10 layouts x 4 ratios.
`figma/<slug>.jsx` is get_design_context output saved verbatim (assets in figma/assets/, Figma renders in figma/ref/).

Usage:
  python build_templates.py          -> html/<slug>.html (one standalone frame each, native size, for production
                                        and PNG export) + ds-templates-section.html (section#templates, injected
                                        into the Design System by inject_ds.py)
  python build_templates.py check    -> also renders every frame as Figma has it (Inter, original weights) next to
                                        the Figma render, into qa/<slug>.png, to check the rebuild by eye.

Type: the Figma frames use Inter as a stand-in because the Figma plugin cannot load Aktiv Grotesk. Every page here
renders in Aktiv Grotesk (the brand face, embedded from the Design System page) and can switch to Inter to compare
against Figma.
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import html
import io
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

from tw2css import jsx_to_html

HERE = Path(__file__).resolve().parent
FIG = HERE / "figma"
OUT_HTML = HERE / "html"
SECTION_OUT = HERE / "ds-templates-section.html"
DS_FILE = HERE.parent / "katapult-social-system.html"
LOGO = HERE.parent / "identity" / "logo-katapuklt.svg"
FIGMA_URL = "https://www.figma.com/design/D8FpNuKI3uPGjCPqonIn3C/Progressive-Global---LAB?node-id=547-1042"
DS = "https://claude.ai/code/artifact/ee8bd24b-c2e4-4f39-b14b-4523c87c4704"
HUB = "https://claude.ai/code/artifact/2abbbef7-4ac3-4e9c-a431-7c37b8e05dcf"
LIB = "https://claude.ai/code/artifact/bc252c47-7c82-4376-ba50-383a10c1a576"
PDHUB = "https://claude.ai/code/artifact/91b3a212-4b8f-4cb4-ade3-0ae3b6122be6"
CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]

RATIOS = [("1x1", "1:1", 1200, 1200, "Feed square"), ("4x5", "4:5", 1080, 1350, "Feed portrait"),
          ("16x9", "16:9", 1920, 1080, "Landscape, video and display"), ("9x16", "9:16", 1080, 1920, "Stories and Reels")]
NODES = {
    "t01": ["547:1043", "547:1295", "547:1309", "547:1323"], "t02": ["547:1057", "547:1337", "547:1352", "547:1367"],
    "t03": ["547:1072", "547:1382", "547:1400", "547:1418"], "t04": ["547:1090", "547:1202", "547:1218", "547:1234"],
    "t05": ["547:1106", "547:1436", "547:1450", "547:1464"], "t06": ["547:1120", "547:1250", "547:1265", "547:1280"],
    "t07": ["547:1135", "547:1478", "547:1493", "547:1508"], "t08": ["547:1150", "547:1523", "547:1537", "547:1551"],
    "t09": ["547:1164", "547:1565", "547:1579", "547:1593"], "t10": ["547:1178", "547:1607", "547:1631", "547:1655"],
}
TEMPLATES = [
    ("t01", "full-image", "Full image",
     "A full-bleed lifestyle photo with a dark fade at the bottom. Headline, subline and CTA centered over the fade; disclaimer left and logo right in the footer.",
     "One strong lifestyle photo whose lower third is calm enough to carry white type.",
     "Lifestyle photo (full bleed, people as the focal point)"),
    ("t02", "split-panel-image", "Split panel, image",
     "Dark Blue panel with a stacked, left-aligned headline beside a photo panel. In 9:16 the panels stack, copy on top.",
     "A short, punchy three-beat headline and a lifestyle photo that works as a tall crop.",
     "Lifestyle photo (half frame)"),
    ("t03", "split-phone-hand", "Split, phone in hand",
     "Pink panel with a hand holding the Katapult app, overlapping a Dark Blue copy column with logo, centered headline, subline and CTA.",
     "App and how-it-works messages: download, apply, browse retailers.",
     "Hand holding a phone with the app screen"),
    ("t04", "product-row-3up", "Product row, 3-up",
     "Dark Blue with the Bounce arc. Logo, headline, subline and CTA top left; three product cutouts in a row below.",
     "Category or gear messages that show several products at once.",
     "Three product cutouts on transparent backgrounds"),
    ("t05", "hero-product-bleed-card", "Hero product, bleed",
     "Cream background, big Dark Blue headline across the top, one product bleeding off the bottom edge, subline and CTA beside it.",
     "One hero product and a warm, conversational headline.",
     "One large product cutout"),
    ("t06", "top-block-rounded-card", "Top block, photo card",
     "Pink background, centered logo, headline, subline and a Dark Blue CTA, over a rounded photo card.",
     "Home and lifestyle messages where the photo is the proof.",
     "Lifestyle photo (rounded card)"),
    ("t07", "top-block-product-circle", "Top block, product on circle",
     "Pink background, centered copy block, one product sitting on a soft Dark Blue to Pink circle.",
     "A single product launch or tech message.",
     "One product cutout"),
    ("t08", "typographic-statement", "Typographic statement",
     "Dark Blue, a four-line statement with the last line in Pink, subline and CTA; logo and disclaimer in the footer.",
     "Brand and manifesto messages with no product or photo.",
     "None, type only"),
    ("t09", "hero-photo-full-width", "Hero photo, full width",
     "Dark Blue top block with logo, headline (last word in Pink) and subline; photo across the bottom with the CTA over it.",
     "Lifestyle messages that need a big photo and a short headline.",
     "Lifestyle photo (bottom half)"),
    ("t10", "product-trio-circles", "Product trio, circles",
     "Dark Blue, centered headline and subline, three products on soft circles (center one larger), CTA below.",
     "Gear and category roundups with exactly three products.",
     "Three product cutouts"),
]


class Assets:
    """Dedupe assets by content and keep one compressed data URI per unique file."""

    def __init__(self):
        self.by_path: dict[str, str] = {}
        self.uri: dict[str, str] = {}

    def __call__(self, rel: str) -> str:
        if rel in self.by_path:
            return self.by_path[rel]
        data = (FIG / rel).read_bytes()
        key = "a" + hashlib.sha1(data).hexdigest()[:10]
        self.by_path[rel] = key
        if key not in self.uri:
            if rel.endswith(".svg"):
                self.uri[key] = "data:image/svg+xml;base64," + base64.b64encode(data).decode()
            else:
                im = Image.open(io.BytesIO(data))
                im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
                im.thumbnail((2400, 2400), Image.LANCZOS)
                buf = io.BytesIO()
                im.save(buf, "WEBP", quality=84, method=6)
                self.uri[key] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
        return key


REGULAR = HERE / "fonts" / "aktiv-grotesk-400.woff"
# Headlines are set in Aktiv Grotesk Regular (decision 2026-10-13). In this Figma set the only Bold/SemiBold
# text is the headline, so every 600/700 weight becomes 400.
HEADLINE_WEIGHT = "400"


def regular_face() -> str:
    b64 = base64.b64encode(REGULAR.read_bytes()).decode()
    return ('@font-face{font-family:"Aktiv Grotesk";font-weight:400;font-style:normal;font-display:swap;'
            f'src:url(data:font/woff;base64,{b64}) format("woff")}}')


def fonts() -> str:
    """Light, Medium and Bold come from the DS head; Regular from templates/fonts."""
    seen, out = set(), []
    for l in DS_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r'@font-face\{font-family:"Aktiv Grotesk";font-weight:(\d+)', l)
        if m and m.group(1) in ("300", "500", "700") and m.group(1) not in seen:
            seen.add(m.group(1))
            out.append(l)
    return "\n".join(out + [regular_face()])


def regular_headlines(body: str) -> str:
    return re.sub(r"font-weight:(600|700)", "font-weight:" + HEADLINE_WEIGHT, body)


INTER = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">'
FRAME_CSS = """
.art{position:relative;overflow:hidden;--kfont:"Aktiv Grotesk","Inter","Helvetica Neue",Arial,sans-serif;font-family:var(--kfont)}
.art p{margin:0}
.art[data-font="inter"],[data-font="inter"] .art{--kfont:"Inter","Helvetica Neue",Arial,sans-serif}
"""

BTN_JS = """function fitButtons(root){(root||document).querySelectorAll('[data-name="Button"]').forEach(b=>{
if(b.dataset.t===undefined){b.dataset.t=b.style.top||'';b.dataset.l=b.style.left||'';}
b.style.zoom=1;const z=446/b.offsetWidth;b.style.zoom=z;
if(b.style.position==='absolute'){['t','l'].forEach(k=>{const v=b.dataset[k],p=k==='t'?'top':'left';
if(/^-?[\\d.]+px$/.test(v))b.style[p]=(parseFloat(v)/z)+'px';});}});}
document.fonts.ready.then(()=>fitButtons());fitButtons();"""


def standalone(slug: str, w: int, h: int, body: str, assets: Assets) -> str:
    # Standalone frames point at the saved Figma assets on disk so they stay light and editable.
    rev = {v: k for k, v in assets.by_path.items()}
    body = re.sub(r'data-a="(\w+)"', lambda m: f'src="../figma/{rev[m.group(1)]}"', body)
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Katapult {slug}</title>{INTER}
<style>{fonts()}
html,body{{margin:0;background:#888}}{FRAME_CSS}</style></head>
<body><div class="art" id="art" style="width:{w}px;height:{h}px">{body}</div>
<script>if(location.hash==='#inter')document.getElementById('art').dataset.font='inter';
{BTN_JS}</script></body></html>"""


def build(check: bool = False) -> None:
    assets = Assets()
    OUT_HTML.mkdir(exist_ok=True)
    data = []
    for tid, tslug, name, what, when, needs in TEMPLATES:
        frames = []
        for (rk, rlabel, w, h, use), node in zip(RATIOS, NODES[tid]):
            slug = f"{tid}-{rk}"
            src = (FIG / f"{slug}.jsx").read_text(encoding="utf-8")
            body, _ = jsx_to_html(src, assets)
            raw = body
            body = regular_headlines(body)
            (OUT_HTML / f"{slug}.html").write_text(standalone(slug, w, h, body, assets), encoding="utf-8")
            if check:
                (OUT_HTML / f"_figma-{slug}.html").write_text(standalone(slug, w, h, raw, assets), encoding="utf-8")
            frames.append({"slug": slug, "ratio": rlabel, "w": w, "h": h, "use": use, "node": node, "body": body})
        data.append({"id": tid, "slug": tslug, "name": name, "what": what, "when": when, "needs": needs,
                     "frames": frames})
    SECTION_OUT.write_text(render_section(data, assets), encoding="utf-8")
    print(f"{SECTION_OUT.name} · {SECTION_OUT.stat().st_size / 1e6:.2f} MB · "
          f"{sum(len(t['frames']) for t in data)} frames · {len(assets.uri)} unique assets")
    if check:
        qa(data)


def qa(data) -> None:
    """Figma render next to the frame as Figma has it (Inter, original weights): checks the rebuild itself."""
    chrome = next(c for c in CHROME if Path(c).exists())
    qdir = HERE / "qa"
    qdir.mkdir(exist_ok=True)
    for t in data:
        for f in t["frames"]:
            shot = qdir / f"{f['slug']}-html.png"
            page = OUT_HTML / f"_figma-{f['slug']}.html"
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                            f"--window-size={f['w']},{f['h']}", "--virtual-time-budget=5000",
                            f"--screenshot={shot}", page.as_uri() + "#inter"], capture_output=True, timeout=120)
            page.unlink()
            ref = Image.open(FIG / "ref" / f"{f['slug']}.png").convert("RGB")
            got = Image.open(shot).convert("RGB")
            hh = 900
            ref = ref.resize((round(ref.width * hh / ref.height), hh))
            got = got.resize((round(got.width * hh / got.height), hh))
            sheet = Image.new("RGB", (ref.width + got.width + 20, hh), "white")
            sheet.paste(ref, (0, 0))
            sheet.paste(got, (ref.width + 20, 0))
            sheet.save(qdir / f"{f['slug']}.png")
            shot.unlink()
    print("qa sheets in", qdir)


def render_section(data, assets: Assets) -> str:
    blocks = []
    for t in data:
        frames = "".join(
            f"""<figure class="kt-fr" data-ratio="{f['ratio']}">
  <div class="kt-stage" style="aspect-ratio:{f['w']}/{f['h']}"><div class="art" data-w="{f['w']}" style="width:{f['w']}px;height:{f['h']}px">{f['body']}</div></div>
  <figcaption><b>{f['ratio']}</b> {f['w']}×{f['h']} <span class="muted">{html.escape(f['use'])}</span>
  <a href="{FIGMA_URL.split('?')[0]}?node-id={f['node'].replace(':', '-')}" target="_blank" rel="noopener">Figma {f['node']}</a>
  <span class="mono muted">html/{f['slug']}.html</span></figcaption></figure>""" for f in t["frames"])
        blocks.append(f"""    <div class="tpl-block" id="tpl-{t['id']}">
      <div class="tpl-head"><h3><span class="kt-num">{t['id'].upper()}</span> {html.escape(t['name'])}</h3><span class="mono muted">template-{t['id'][1:]}-{t['slug']}</span></div>
      <div class="kt-spec"><p>{html.escape(t['what'])}</p>
        <dl><dt>Use it for</dt><dd>{html.escape(t['when'])}</dd><dt>Imagery</dt><dd>{html.escape(t['needs'])}</dd></dl></div>
      <div class="kt-frames">{frames}</div>
    </div>""")
    index = "".join(f'<a href="#tpl-{t["id"]}"><b>{t["id"].upper()}</b> {html.escape(t["name"])}</a>' for t in data)
    amap = json.dumps(assets.uri).replace("</", "<\\/")
    frame_css = "\n".join("#templates " + l for l in FRAME_CSS.strip().splitlines())
    return SECTION.replace("__REGULAR__", regular_face()).replace("__INTER__", INTER).replace("__FRAMECSS__", frame_css) \
        .replace("__FIGMA__", FIGMA_URL).replace("__INDEX__", index).replace("__BLOCKS__", "\n".join(blocks)) \
        .replace("__ASSETS__", amap).replace("__BTNJS__", BTN_JS)


SECTION = r"""<section class="block" id="templates">
__INTER__
<style>
__REGULAR__
/* Social templates: ten layouts x four ratios, rebuilt from Figma 547:1042. Scoped to #templates. */
#templates .kt-index{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:14px}
#templates .kt-index a{text-decoration:none;border-bottom:1px solid var(--rule);padding-bottom:1px}
#templates .kt-index a:hover{border-color:var(--accent)}
#templates .kt-index b,#templates .kt-num{color:var(--accent);font-weight:700}
#templates .kt-bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:4;background:var(--bg);display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;padding-block:10px;border-block:1px solid var(--rule)}
#templates .kt-row{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
#templates .kt-chip{font:500 13px/1 var(--font-brand);border:1px solid var(--rule-strong);background:var(--panel);color:var(--ink);border-radius:999px;padding:7px 12px;cursor:pointer}
#templates .kt-chip:hover{border-color:var(--accent)}
#templates .kt-chip[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:var(--bg)}
#templates .kt-spec{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:8px 32px;font-size:15px;color:var(--ink-2)}
#templates .kt-spec p{margin:0}
#templates .kt-spec dl{display:grid;grid-template-columns:auto 1fr;gap:4px 14px;margin:0}
#templates .kt-spec dt{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;line-height:2}
#templates .kt-spec dd{margin:0;color:var(--ink)}
#templates .kt-frames{display:grid;gap:18px;grid-template-columns:1fr 0.8fr 1.78fr 0.5625fr;align-items:end}
#templates .kt-fr{margin:0;display:grid;gap:8px;min-width:0}
#templates .kt-stage{width:100%;max-width:100%;background:var(--code-bg);position:relative;overflow:hidden;border-radius:2px}
#templates .kt-stage .art{position:absolute;left:0;top:0;transform-origin:0 0}
#templates figcaption{display:flex;flex-wrap:wrap;gap:2px 10px;font-size:12.5px;line-height:1.4}
#templates.kt-only .kt-fr{display:none}
#templates.kt-only .kt-fr.on{display:grid}
#templates.kt-only .kt-frames{grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),640px))}
#templates [contenteditable="true"]{outline:2px dashed rgba(237,83,112,.7);outline-offset:4px;cursor:text}
@media (max-width:900px){#templates .kt-frames{grid-template-columns:1fr 1fr}#templates .kt-spec{grid-template-columns:1fr}}
@media (max-width:520px){#templates .kt-frames{grid-template-columns:1fr}}
__FRAMECSS__
</style>
  <div class="wrap">
    <div class="block-head">
      <span class="label">Social templates</span>
      <h2>Ten layouts, four ratios: start every post here</h2>
      <p class="prose muted">Every Katapult social piece starts from one of these. Pick the layout by the imagery you have, then swap the copy and the photo or product; keep every position, size and spacing, the pill CTA, the logo and the disclaimer. Rebuilt one to one from the <a href="__FIGMA__" target="_blank" rel="noopener">Figma template set</a> (node 547:1042). Headlines are Aktiv Grotesk Regular. Product and photo slots hold the Figma placeholders.</p>
      <p class="prose muted">Long copy: rebreak the lines first, then widen the box if the layout has room, and only then step the size down. Each frame also exists as a standalone file in <code>clients/katapult/01-brand/templates/html/</code> for production and PNG export.</p>
      <nav class="kt-index" aria-label="Templates">__INDEX__</nav>
    </div>
    <div class="kt-bar" role="region" aria-label="Template view options">
      <div class="kt-row" id="kt-ratio"><span class="label">Ratio</span>
        <button class="kt-chip" type="button" data-v="" aria-pressed="true">All</button>
        <button class="kt-chip" type="button" data-v="1:1" aria-pressed="false">1:1</button>
        <button class="kt-chip" type="button" data-v="4:5" aria-pressed="false">4:5</button>
        <button class="kt-chip" type="button" data-v="16:9" aria-pressed="false">16:9</button>
        <button class="kt-chip" type="button" data-v="9:16" aria-pressed="false">9:16</button>
      </div>
      <div class="kt-row" id="kt-font"><span class="label">Type</span>
        <button class="kt-chip" type="button" data-v="aktiv" aria-pressed="true">Aktiv Grotesk</button>
        <button class="kt-chip" type="button" data-v="inter" aria-pressed="false">Inter (as in Figma)</button>
      </div>
      <div class="kt-row"><button class="kt-chip" type="button" id="kt-edit" aria-pressed="false">Edit copy</button></div>
    </div>
__BLOCKS__
  </div>
<script type="application/json" id="kt-assets">__ASSETS__</script>
<script>
(function(){
  __BTNJS__
  var sec = document.getElementById('templates');
  var A = JSON.parse(document.getElementById('kt-assets').textContent);
  sec.querySelectorAll('img[data-a]').forEach(function(i){ i.src = A[i.dataset.a]; });
  function fit(){ sec.querySelectorAll('.kt-stage').forEach(function(s){
    var a = s.firstElementChild; a.style.transform = 'scale(' + (s.clientWidth / +a.dataset.w) + ')'; }); }
  fit(); new ResizeObserver(fit).observe(sec);
  function press(box, b){ box.querySelectorAll('.kt-chip').forEach(function(x){ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); }
  document.getElementById('kt-ratio').addEventListener('click', function(e){
    var b = e.target.closest('.kt-chip'); if (!b) return; press(e.currentTarget, b);
    sec.classList.toggle('kt-only', !!b.dataset.v);
    sec.querySelectorAll('.kt-fr').forEach(function(f){ f.classList.toggle('on', f.dataset.ratio === b.dataset.v); });
    fit();
  });
  document.getElementById('kt-font').addEventListener('click', function(e){
    var b = e.target.closest('.kt-chip'); if (!b) return; press(e.currentTarget, b);
    sec.querySelectorAll('.art').forEach(function(a){ if (b.dataset.v === 'inter') a.dataset.font = 'inter'; else delete a.dataset.font; });
    document.fonts.ready.then(function(){ fitButtons(sec); });
  });
  document.getElementById('kt-edit').addEventListener('click', function(e){
    var on = e.currentTarget.getAttribute('aria-pressed') !== 'true';
    e.currentTarget.setAttribute('aria-pressed', on ? 'true' : 'false');
    sec.querySelectorAll('.art p').forEach(function(p){ if (on) p.setAttribute('contenteditable', 'true'); else p.removeAttribute('contenteditable'); });
  });
})();
</script>
</section>"""

if __name__ == "__main__":
    build(check="check" in sys.argv[1:])
