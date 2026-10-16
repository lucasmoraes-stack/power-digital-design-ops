"""Build the Katapult Image Library page (self-contained HTML, published as an Artifact).

Usage: python build_image_library.py      -> writes image-library.html next to this file

Reads library/catalog.md (one row per image, paths relative to this folder), lists anything waiting in
library/_inbox/ and any file in library/ that has no catalogue row yet. Thumbnails (480px) and previews
(1400px) are embedded as WebP; the originals stay on disk. Aktiv Grotesk is taken from the Design System
page (katapult-social-system.html, the local copy of the published DS), so both pages share one face.
"""
from __future__ import annotations

import base64
import datetime as dt
import io
import json
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
LIB = HERE / "library"
INBOX = LIB / "_inbox"
OUT = HERE / "image-library.html"
LOGO = HERE.parent / "identity" / "logo-katapuklt.svg"
DS_FILE = HERE.parent / "katapult-social-system.html"
DS = "https://claude.ai/code/artifact/ee8bd24b-c2e4-4f39-b14b-4523c87c4704"
HUB = "https://claude.ai/code/artifact/2abbbef7-4ac3-4e9c-a431-7c37b8e05dcf"
PD_HUB = "https://claude.ai/code/artifact/91b3a212-4b8f-4cb4-ade3-0ae3b6122be6"
EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".heic"}


def rows(md: str) -> list[dict]:
    out, hdr = [], None
    for line in md.splitlines():
        if not line.startswith("|"):
            hdr = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if hdr is None:
            hdr = [c.lower() for c in cells]
        elif not set("".join(cells)) <= set("-: "):
            out.append(dict(zip(hdr, cells)))
    return out


def webp(im: Image.Image, side: int, q: int) -> str:
    im = im.copy()
    im.thumbnail((side, side), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=q, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def load(path: Path):
    try:
        im = Image.open(path)
        im.draft("RGB", (2800, 2800))
        im = ImageOps.exif_transpose(im)
        im.load()
    except Exception:
        return None, (0, 0)
    size = Image.open(path).size
    alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    return im.convert("RGBA" if alpha else "RGB"), size


def entry(path: Path, meta: dict) -> dict:
    im, (w, h) = load(path)
    orient = ""
    if im:
        orient = "square" if abs(w - h) < 0.08 * max(w, h) else ("landscape" if w > h else "portrait")
    return {**meta,
            "px": f"{w} × {h}" if im else "unreadable", "orient": orient,
            "mb": round(path.stat().st_size / 1e6, 1),
            "thumb": webp(im, 520, 72) if im else "", "big": webp(im, 1400, 76) if im else ""}


def fonts() -> str:
    if not DS_FILE.is_file():
        return ""
    return "\n".join(l for l in DS_FILE.read_text(encoding="utf-8").splitlines() if l.startswith("@font-face"))


def build() -> None:
    items, known = [], set()
    for r in rows((LIB / "catalog.md").read_text(encoding="utf-8")):
        p = (HERE / r["file"]).resolve()
        known.add(p)
        if not p.is_file():
            print("missing:", r["file"])
            continue
        items.append(entry(p, {"file": r["file"], "collection": r.get("collection", ""), "source": r.get("source", ""),
                               "subject": r.get("subject", ""), "category": r.get("category", ""),
                               "calm": r.get("text space", ""), "use": r.get("best use", ""),
                               "fit": r.get("brand fit", ""), "rights": r.get("rights", ""), "notes": r.get("notes", "")}))
    for p in sorted(LIB.glob("*")):
        if p.is_file() and p.suffix.lower() in EXTS and p.resolve() not in known:
            items.append(entry(p, {"file": str(p.relative_to(HERE)).replace("\\", "/"), "collection": "stock",
                                   "subject": "Not catalogued yet", "category": "", "fit": "", "rights": "to confirm",
                                   "notes": "no row in catalog.md"}))
    inbox = []
    if INBOX.is_dir():
        for p in sorted(INBOX.iterdir()):
            if p.is_file() and p.suffix.lower() in EXTS:
                inbox.append(entry(p, {"file": str(p.relative_to(HERE)).replace("\\", "/"), "collection": "inbox",
                                       "subject": p.name, "rights": "to confirm", "notes": "waiting to be processed"}))
    logo = "data:image/svg+xml;base64," + base64.b64encode(LOGO.read_bytes()).decode()
    page = (PAGE.replace("__FONTS__", fonts()).replace("__LOGO__", logo)
            .replace("__DS__", DS).replace("__HUB__", HUB).replace("__PDHUB__", PD_HUB)
            .replace("__UPDATED__", dt.date.today().isoformat())
            .replace("__DATA__", json.dumps({"items": items, "inbox": inbox}, ensure_ascii=False).replace("</", "<\\/")))
    OUT.write_text(page, encoding="utf-8")
    print(f"{OUT} · {OUT.stat().st_size / 1e6:.2f} MB · {len(items)} catalogued · {len(inbox)} in inbox")


PAGE = r"""<title>Katapult Image Library</title>
<style>
__FONTS__
/* Layout: the Katapult family masthead (same Dark Blue band as the Design System and Deliverables Hub),
   a sticky filter bar, then one contact-sheet grid per scene category. Tokens follow the Katapult DS. */
:root{
  --k-pink:#ED5370; --k-dark-blue:#131540; --k-blue:#365488; --k-light-blue:#9EB5C0; --k-orange:#E48027; --k-cream:#D4A574;
  --k-white:#FFFFFF; --k-grey-light:#D8D8D8;
  --font-brand:"Aktiv Grotesk","Helvetica Neue",Helvetica,Arial,sans-serif;
  --font-mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --bg:#F5F5F3; --panel:#FFFFFF; --panel-2:#F0F0F0; --ink:#131540; --ink-2:#4D4D4D; --rule:#D8D8D8; --rule-strong:#A4A4A4;
  --accent:#ED5370; --focus:#131540; --thumb:#E4E5EA;
  --ok-bg:#E3EEE6; --ok-ink:#1E4D2B; --lg-bg:#F4E8D6; --lg-ink:#6B4210; --no-bg:#F7DDE2; --no-ink:#7A1F31;
  --chip-on-bg:#131540; --chip-on-ink:#FFFFFF;
  --gutter:clamp(16px,4vw,48px);
  color-scheme:light;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#0D0E2C; --panel:#131540; --panel-2:#171A4A; --ink:#F0F0F0; --ink-2:#C8C9CF; --rule:#2B2E62; --rule-strong:#4A4E86;
    --focus:#ED5370; --thumb:#0A0B24;
    --ok-bg:#16382A; --ok-ink:#BFE5CB; --lg-bg:#3E2E14; --lg-ink:#F2D7A8; --no-bg:#43182A; --no-ink:#F7C4CF;
    --chip-on-bg:#ED5370; --chip-on-ink:#131540;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --bg:#0D0E2C; --panel:#131540; --panel-2:#171A4A; --ink:#F0F0F0; --ink-2:#C8C9CF; --rule:#2B2E62; --rule-strong:#4A4E86;
  --focus:#ED5370; --thumb:#0A0B24;
  --ok-bg:#16382A; --ok-ink:#BFE5CB; --lg-bg:#3E2E14; --lg-ink:#F2D7A8; --no-bg:#43182A; --no-ink:#F7C4CF;
  --chip-on-bg:#ED5370; --chip-on-ink:#131540;
}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:300 16px/1.55 var(--font-brand);-webkit-font-smoothing:antialiased}
h1,h2,h3{font-weight:500;margin:0;text-wrap:balance;line-height:1.1}
p{margin:0}
button,input{font:inherit}
code{font-family:var(--font-mono);font-size:.84em;background:var(--panel-2);border-radius:3px;padding:1px 5px}
:focus-visible{outline:3px solid var(--focus);outline-offset:3px;border-radius:2px}
.wrap{max-width:1240px;margin-inline:auto;padding-inline:var(--gutter)}
.label{font-size:12px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2)}

.masthead{background:var(--k-dark-blue);color:var(--k-white)}
.masthead .wrap{padding-block:28px 40px;display:grid;gap:18px}
.family{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 20px}
.family img{height:26px;width:auto;display:block}
.family nav{display:flex;flex-wrap:wrap;gap:6px}
.family a,.family button{font:500 13px/1 var(--font-brand);color:var(--k-grey-light);text-decoration:none;border:1px solid rgba(158,181,192,.35);border-radius:999px;padding:7px 13px;background:transparent;cursor:pointer}
.family a:hover,.family button:hover{border-color:var(--k-pink);color:var(--k-white)}
.family a[aria-current="page"]{background:var(--k-pink);border-color:var(--k-pink);color:var(--k-dark-blue);font-weight:700}
.masthead .eyebrow{color:var(--k-light-blue)}
.masthead h1{font-size:clamp(36px,6vw,60px);letter-spacing:-.015em;line-height:1}
.masthead h1 span{color:var(--k-pink)}
.lede{max-width:64ch;color:var(--k-grey-light);font-size:17px}
.counts{display:flex;flex-wrap:wrap;gap:8px 22px;list-style:none;padding:0;margin:0;font-size:14px;color:var(--k-light-blue);font-weight:500}
.counts b{color:var(--k-white);font-weight:700;font-variant-numeric:tabular-nums}

.rules{margin-top:28px;display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))}
.rule-card{background:var(--panel);border:1px solid var(--rule);border-radius:4px;padding:16px 18px;display:grid;gap:6px;align-content:start;font-size:14.5px;color:var(--ink-2)}
.rule-card h3{font-size:16px;color:var(--ink)}
.rule-card.inbox.has{border-color:var(--accent)}

.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-block:1px solid var(--rule);padding-block:12px;margin-top:28px}
.bar .wrap{display:grid;gap:10px}
.row{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.lbl{min-width:84px;margin-right:4px}
.chip{font:500 13px/1 var(--font-brand);border:1px solid var(--rule-strong);background:var(--panel);color:var(--ink);border-radius:999px;padding:7px 12px;cursor:pointer}
.chip:hover{border-color:var(--accent)}
.chip[aria-pressed="true"]{background:var(--chip-on-bg);border-color:var(--chip-on-bg);color:var(--chip-on-ink)}
.chip .n{opacity:.7;margin-left:5px;font-variant-numeric:tabular-nums}
input[type=search]{padding:8px 12px;border:1px solid var(--rule-strong);border-radius:4px;background:var(--panel);color:var(--ink);flex:1 1 240px;max-width:420px;min-width:0}
.count{margin-left:auto;font-size:13px;color:var(--ink-2);font-variant-numeric:tabular-nums}

main{padding-block:8px 64px}
section.grp{padding-top:34px;display:grid;gap:14px}
.grp-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 14px}
.grp-head h2{font-size:clamp(24px,3vw,32px)}
.grp-head h2 small{font-size:.55em;color:var(--accent);font-weight:700;margin-left:6px;font-variant-numeric:tabular-nums}
.grp-head p{color:var(--ink-2);font-size:15px;max-width:70ch}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(min(100%,240px),1fr))}
.tile{display:flex;flex-direction:column;text-align:left;background:var(--panel);color:inherit;border:1px solid var(--rule);border-radius:4px;overflow:hidden;padding:0;cursor:zoom-in;transition:border-color .15s,transform .15s}
.tile:hover{border-color:var(--accent);transform:translateY(-2px)}
.thumb{aspect-ratio:4/5;background:var(--thumb);display:block;overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.info{padding:11px 13px 14px;display:grid;gap:7px;font-size:13px}
.subj{font-weight:500;font-size:14.5px;line-height:1.35;color:var(--ink)}
.facts{display:flex;flex-wrap:wrap;gap:4px}
.f{font:500 11.5px/1 var(--font-brand);padding:4px 7px;border-radius:3px;background:var(--panel-2);color:var(--ink-2);font-variant-numeric:tabular-nums}
.f.ok{background:var(--ok-bg);color:var(--ok-ink)}
.f.care{background:var(--lg-bg);color:var(--lg-ink)}
.f.no{background:var(--no-bg);color:var(--no-ink)}
.use{color:var(--ink-2)}
.path{font:11.5px/1.35 var(--font-mono);color:var(--ink-2);overflow-wrap:anywhere}
.empty{border:1px dashed var(--rule-strong);border-radius:4px;padding:22px;color:var(--ink-2);background:var(--panel)}

dialog{border:0;border-radius:6px;padding:0;max-width:min(1080px,94vw);width:100%;background:var(--panel);color:var(--ink)}
dialog::backdrop{background:rgba(13,14,44,.78)}
.dlg{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr)}
.dlg .big{background:var(--thumb);display:flex;align-items:center;justify-content:center;min-height:320px}
.dlg .big img{max-width:100%;max-height:80vh;object-fit:contain;display:block}
.dlg .side{padding:20px 22px;display:grid;gap:12px;align-content:start;font-size:14px}
.dlg h3{font-size:20px}
.dlg dl{display:grid;grid-template-columns:auto 1fr;gap:7px 14px;margin:0}
.dlg dt{font:700 11px/1.7 var(--font-brand);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.dlg dd{margin:0;overflow-wrap:anywhere}
.close{justify-self:end;background:var(--panel-2);border:1px solid var(--rule);border-radius:999px;padding:6px 14px;color:var(--ink);cursor:pointer}
footer{border-top:1px solid var(--rule);padding-block:20px 40px;color:var(--ink-2);font-size:13px}
@media (max-width:760px){.dlg{grid-template-columns:1fr}.lbl{min-width:0;width:100%}}
@media (prefers-reduced-motion:reduce){.tile{transition:none}.tile:hover{transform:none}}
</style>

<header class="masthead">
  <div class="wrap">
    <div class="family">
      <img src="__LOGO__" alt="Katapult">
      <nav aria-label="Katapult pages">
        <a href="__DS__" target="_blank" rel="noopener">Design System</a>
        <a href="__HUB__" target="_blank" rel="noopener">Deliverables Hub</a>
        <a href="#" aria-current="page">Image Library</a>
        <a href="https://claude.ai/code/artifact/5a137796-2f13-4690-8ce2-45fd9f4c8cdc" target="_blank" rel="noopener">Social Studio</a>
        <a href="__PDHUB__" target="_blank" rel="noopener">Power Digital Hub</a>
        <button id="theme-btn" type="button">Switch theme</button>
      </nav>
    </div>
    <span class="label eyebrow">Katapult · Photography for social and banners</span>
    <h1>Katapult <span>Image Library</span></h1>
    <p class="lede">Lifestyle photos of people at home with what they bought: phones, laptops, sofas, appliances, deliveries. Each one is graded against the photography rules in the Design System, with where copy can sit. Click a photo for a large preview, its Adobe Stock ID and its file path. Updated __UPDATED__.</p>
    <ul class="counts" id="counts"></ul>
  </div>
</header>

<div class="wrap">
  <div class="rules">
    <div class="rule-card"><h3>On-brand</h3><p>A real person is the focal point, face visible, smiling or engaged, bright and natural. Use as the main image.</p></div>
    <div class="rule-card"><h3>With care</h3><p>Eyes closed, dim light, busy frame or face turned away. Fine as a supporting image or after a re-crop; not as the hero.</p></div>
    <div class="rule-card"><h3>No people</h3><p>Rooms and products only. The guideline never allows them as the main image; use them behind a product or in a collage.</p></div>
    <div class="rule-card inbox" id="inbox"></div>
  </div>
</div>

<div class="bar" role="region" aria-label="Filters"><div class="wrap">
  <div class="row" id="f-cat"><span class="label lbl">Scene</span></div>
  <div class="row" id="f-fit"><span class="label lbl">Brand fit</span></div>
  <div class="row" id="f-or"><span class="label lbl">Shape</span></div>
  <div class="row"><input type="search" id="q" placeholder="Search, e.g. sofa, checkout, appliance, 1976453745" aria-label="Search photos"><span class="count" id="count"></span></div>
</div></div>

<main class="wrap" id="out"></main>
<footer><div class="wrap">Previews are compressed. Use the original at the path shown, under <code>clients/katapult/01-brand/photos/</code> (on disk and OneDrive, outside git). Built by <code>photos/build_image_library.py</code> from <code>library/catalog.md</code>.</div></footer>

<dialog id="dlg" aria-label="Photo details"><div class="dlg"><div class="big"><img id="d-img" alt=""></div>
  <div class="side"><button class="close" id="d-close" type="button">Close</button><h3 id="d-title"></h3><dl id="d-list"></dl></div></div></dialog>

<script type="application/json" id="lib-data">__DATA__</script>
<script>
(function(){
  const D = JSON.parse(document.getElementById('lib-data').textContent);
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const CATS = [
    ['phone', 'On the phone', 'Shopping, checking a balance or paying from a phone. The closest match to the Katapult app moment.'],
    ['laptop', 'Laptop and tablet', 'Browsing and buying online at home.'],
    ['together', 'Together', 'Couples, families and friends sharing the things they bought.'],
    ['unboxing', 'Delivery and moving', 'The box arrives, the new place gets set up.'],
    ['at-home', 'At home', 'Comfort, furniture and appliances in use.'],
    ['retail', 'Retailers', 'Merchants, small business owners, tires and auto.'],
    ['room', 'Rooms, no people', 'Product context only. Never the main image.'],
  ];
  const FITS = [['on-brand','On-brand'],['with care','With care'],['no people','No people']];
  const ORS = [['landscape','Landscape'],['portrait','Portrait'],['square','Square']];
  const fitClass = f => f === 'on-brand' ? 'ok' : f === 'with care' ? 'care' : f === 'no people' ? 'no' : '';
  let st = {cat: null, fit: null, or: null, q: ''};

  try { const t = localStorage.getItem('kat-lib-theme'); if (t) document.documentElement.dataset.theme = t; } catch(e) {}
  document.getElementById('theme-btn').addEventListener('click', () => {
    const cur = document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('kat-lib-theme', next); } catch(e) {}
  });
  document.querySelector('a[aria-current="page"]').addEventListener('click', e => { e.preventDefault(); scrollTo({top: 0}); });

  const cnt = (k, v) => D.items.filter(i => i[k] === v).length;
  document.getElementById('counts').innerHTML =
    `<li><b>${D.items.length}</b> photos</li><li><b>${cnt('fit','on-brand')}</b> on-brand</li><li><b>${cnt('fit','with care')}</b> with care</li><li><b>${cnt('fit','no people')}</b> no people</li><li><b>${D.inbox.length}</b> in inbox</li>`;

  const ib = document.getElementById('inbox');
  ib.classList.toggle('has', D.inbox.length > 0);
  ib.innerHTML = `<h3>${D.inbox.length ? D.inbox.length + ' new file' + (D.inbox.length > 1 ? 's' : '') + ' waiting' : 'Add photos'}</h3>
    <p>Drop the files, full resolution, in <code>photos/library/_inbox/</code> and ask Claude to “process the Katapult image inbox”. Each one is renamed, graded and added here at the same link.</p>`;

  function chips(id, opts, key){
    const box = document.getElementById(id);
    box.insertAdjacentHTML('beforeend', opts.filter(([v]) => cnt(key, v) > 0).map(([v, l]) =>
      `<button class="chip" type="button" data-v="${v}" aria-pressed="false">${esc(l)}<span class="n">${cnt(key, v)}</span></button>`).join(''));
    box.addEventListener('click', e => {
      const b = e.target.closest('.chip'); if (!b) return;
      const k = {'f-cat':'cat','f-fit':'fit','f-or':'or'}[id];
      st[k] = st[k] === b.dataset.v ? null : b.dataset.v;
      box.querySelectorAll('.chip').forEach(x => x.setAttribute('aria-pressed', x.dataset.v === st[k] ? 'true' : 'false'));
      render();
    });
  }
  chips('f-cat', CATS.map(([v, l]) => [v, l]), 'category');
  chips('f-fit', FITS, 'fit');
  chips('f-or', ORS, 'orient');
  document.getElementById('q').addEventListener('input', e => { st.q = e.target.value.trim().toLowerCase(); render(); });

  function tile(i){
    const fc = fitClass(i.fit);
    return `<button class="tile" type="button" data-file="${esc(i.file)}" aria-label="${esc(i.subject)}">
      <span class="thumb">${i.thumb ? `<img src="${i.thumb}" alt="" loading="lazy">` : ''}</span>
      <span class="info">
        <span class="subj">${esc(i.subject)}</span>
        <span class="facts">${i.fit ? `<span class="f ${fc}">${esc(i.fit)}</span>` : ''}${i.orient ? `<span class="f">${esc(i.orient)}</span>` : ''}<span class="f">${esc(i.px)}</span></span>
        ${i.calm ? `<span class="use"><b style="font-weight:500">Copy:</b> ${esc(i.calm)}</span>` : ''}
        <span class="path">${esc(i.file)}</span>
      </span></button>`;
  }

  function render(){
    const match = i => (!st.cat || i.category === st.cat) && (!st.fit || i.fit === st.fit) && (!st.or || i.orient === st.or) &&
      (!st.q || [i.subject, i.use, i.notes, i.file, i.category, i.source, i.calm].join(' ').toLowerCase().includes(st.q));
    const shown = D.items.filter(match);
    document.getElementById('count').textContent = `${shown.length} of ${D.items.length} photos`;
    const known = CATS.map(c => c[0]);
    const groups = CATS.concat([['', 'Not catalogued', 'Files in library/ with no catalogue row yet.']]);
    const html = groups.map(([key, title, desc]) => {
      const list = shown.filter(i => key ? i.category === key : !known.includes(i.category));
      if (!list.length) return '';
      return `<section class="grp"><div class="grp-head"><h2>${esc(title)}<small>${list.length}</small></h2><p>${esc(desc)}</p></div><div class="grid">${list.map(tile).join('')}</div></section>`;
    }).join('');
    document.getElementById('out').innerHTML = html || `<section class="grp"><div class="empty">No photo matches these filters. Clear a filter or the search.</div></section>`;
  }
  render();

  const dlg = document.getElementById('dlg');
  document.addEventListener('click', e => {
    const t = e.target.closest('.tile'); if (!t) return;
    const i = D.items.concat(D.inbox).find(x => x.file === t.dataset.file); if (!i) return;
    document.getElementById('d-img').src = i.big;
    document.getElementById('d-img').alt = i.subject;
    document.getElementById('d-title').textContent = i.subject;
    document.getElementById('d-list').innerHTML = [['File', i.file], ['Source', i.source], ['Size', `${i.px} px · ${i.mb} MB`], ['Scene', i.category],
      ['Brand fit', i.fit], ['Copy space', i.calm], ['Best use', i.use], ['Rights', i.rights], ['Notes', i.notes]]
      .filter(([, v]) => v).map(([k, v]) => `<dt>${k}</dt><dd>${esc(v)}</dd>`).join('');
    dlg.showModal();
  });
  document.getElementById('d-close').addEventListener('click', () => dlg.close());
  dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
})();
</script>
"""

if __name__ == "__main__":
    build()
