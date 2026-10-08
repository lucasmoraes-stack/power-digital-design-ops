"""Build the Habit Outdoors Image Library page (self-contained HTML, published as an Artifact).

Usage: python build_image_library.py      -> writes image-library.html next to this file

Reads library/catalog.md (one row per image, paths relative to this folder), lists anything waiting in
library/_inbox/ and any file in library/ that has no catalogue row yet. Thumbnails (480px) and previews
(1400px) are embedded as WebP; the originals stay on disk.
"""
from __future__ import annotations

import base64
import datetime as dt
import html
import io
import json
import re
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
LIB = HERE / "library"
INBOX = LIB / "_inbox"
OUT = HERE / "image-library.html"
LOGO = HERE.parent / "identity" / "logo" / "habit-logotype-white.svg"
HUB = "https://claude.ai/code/artifact/70778e63-a022-4658-9d99-3c68be5815ee"
DS = "https://claude.ai/code/artifact/f33018ee-a734-4183-83d0-79d046c9c60d"
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
        im = ImageOps.exif_transpose(Image.open(path))
        im.load()
    except Exception:
        return None
    alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    return im.convert("RGBA" if alpha else "RGB")


def entry(path: Path, meta: dict) -> dict:
    im = load(path)
    w, h = im.size if im else (0, 0)
    orient = "square" if im and abs(w - h) < 0.08 * max(w, h) else ("landscape" if w > h else "portrait")
    return {**meta,
            "px": f"{w}x{h}" if im else "unreadable", "w": w, "orient": orient if im else "",
            "mb": round(path.stat().st_size / 1e6, 1),
            "thumb": webp(im, 480, 72) if im else "", "big": webp(im, 1400, 78) if im else ""}


def build() -> None:
    catalogue = rows((LIB / "catalog.md").read_text(encoding="utf-8"))
    items, known = [], set()
    for r in catalogue:
        p = (HERE / r["file"]).resolve()
        known.add(p)
        if not p.is_file():
            print("missing:", r["file"])
            continue
        items.append(entry(p, {"file": r["file"], "collection": r.get("collection", ""), "subject": r.get("subject", ""),
                               "category": r.get("category", ""), "calm": r.get("calm area", ""),
                               "use": r.get("best use", ""), "rights": r.get("rights", ""), "notes": r.get("notes", "")}))
    for p in sorted(LIB.glob("*")):
        if p.is_file() and p.suffix.lower() in EXTS and p.resolve() not in known:
            items.append(entry(p, {"file": str(p.relative_to(HERE)).replace("\\", "/"), "collection": "selected",
                                   "subject": "Not catalogued yet", "category": "", "calm": "", "use": "",
                                   "rights": "to confirm", "notes": "no row in catalog.md"}))
    inbox = []
    if INBOX.is_dir():
        for p in sorted(INBOX.iterdir()):
            if p.is_file() and p.suffix.lower() in EXTS:
                inbox.append(entry(p, {"file": str(p.relative_to(HERE)).replace("\\", "/"), "collection": "inbox",
                                       "subject": p.name, "category": "", "calm": "", "use": "",
                                       "rights": "to confirm", "notes": "waiting to be processed"}))
    logo = "data:image/svg+xml;base64," + base64.b64encode(LOGO.read_bytes()).decode()
    page = (PAGE.replace("__LOGO__", logo).replace("__HUB__", HUB).replace("__DS__", DS)
            .replace("__UPDATED__", dt.date.today().isoformat())
            .replace("__DATA__", json.dumps({"items": items, "inbox": inbox}, ensure_ascii=False).replace("</", "<\\/")))
    OUT.write_text(page, encoding="utf-8")
    print(f"{OUT} · {OUT.stat().st_size / 1e6:.2f} MB · {len(items)} catalogued · {len(inbox)} in inbox")


PAGE = r"""<title>Habit Outdoors Image Library</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Prompt:wght@400;500;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: Tap Shoe masthead (same family as the Deliverables Hub), an inbox strip, a sticky filter bar,
   then one contact-sheet grid per collection: Selected, Habit originals, provisional crops. */
:root{
  --tapshoe:#2A2B2D; --orange:#FF6400; --paper:#E2DDD9; --aluminum:#A39A8C; --brown:#483F39;
  --bg:#EFECE9; --panel:#FFFFFF; --panel-2:#F6F4F1; --ink:#2A2B2D; --ink-2:#5C5249; --rule:#DCD6CF; --rule-strong:#B9B0A5;
  --mast:#2A2B2D; --mast-ink:#FFFFFF; --mast-2:#CFC8BF; --mast-rule:rgba(207,200,191,.28);
  --ok-bg:#E4E8D8; --ok-ink:#3F4A1F; --warn-bg:#FBE3C9; --warn-ink:#7A3A00; --info-bg:#DDE1EE; --info-ink:#202944;
  --thumb:#2A2B2D; --focus:#FF6400;
  --f-serif:"Playfair Display",Georgia,"Times New Roman",serif;
  --f-sans:"Prompt",Helvetica,Arial,sans-serif;
  --f-mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
  --gutter:clamp(16px,4vw,40px);
  color-scheme:light;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#1B1C1E; --panel:#25262A; --panel-2:#2D2E33; --ink:#F1EEEB; --ink-2:#C2BAB0; --rule:#3A3B40; --rule-strong:#55565C;
    --mast:#121315; --mast-rule:rgba(207,200,191,.18);
    --ok-bg:#2F3524; --ok-ink:#D3DDB4; --warn-bg:#3E2A16; --warn-ink:#FFC48C; --info-bg:#262C42; --info-ink:#C9D1F0;
    --thumb:#151618; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#1B1C1E; --panel:#25262A; --panel-2:#2D2E33; --ink:#F1EEEB; --ink-2:#C2BAB0; --rule:#3A3B40; --rule-strong:#55565C;
  --mast:#121315; --mast-rule:rgba(207,200,191,.18);
  --ok-bg:#2F3524; --ok-ink:#D3DDB4; --warn-bg:#3E2A16; --warn-ink:#FFC48C; --info-bg:#262C42; --info-ink:#C9D1F0;
  --thumb:#151618; color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 15px/1.55 var(--f-sans);-webkit-font-smoothing:antialiased}
h1,h2,h3{margin:0;text-wrap:balance;line-height:1.05}
p{margin:0}
button,input{font:inherit}
.wrap{max-width:1320px;margin-inline:auto;padding-inline:var(--gutter)}
.eyebrow{font:700 12px/1.3 var(--f-sans);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-2)}
:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
code{font-family:var(--f-mono);font-size:12.5px;background:var(--panel-2);border-radius:4px;padding:1px 5px}

.mast{background:var(--mast);color:var(--mast-ink)}
.mast .wrap{padding-block:30px 30px;display:grid;gap:16px}
.mast-top{display:flex;align-items:center;justify-content:space-between;gap:12px 16px;flex-wrap:wrap}
.mast-top img{height:28px;width:auto;display:block}
.links{display:flex;gap:8px;flex-wrap:wrap}
.pill-btn{color:var(--mast-2);background:transparent;border:1px solid var(--mast-rule);border-radius:999px;padding:5px 12px;font-size:12.5px;cursor:pointer;text-decoration:none}
.pill-btn:hover{color:var(--mast-ink);border-color:var(--orange)}
.mast h1{display:grid;gap:4px}
.mast h1 .sans{font:800 clamp(16px,2.2vw,24px)/1 var(--f-sans);letter-spacing:.06em;text-transform:uppercase;color:var(--mast-2)}
.mast h1 .serif{font:900 clamp(42px,7vw,86px)/.92 var(--f-serif);text-transform:uppercase}
.mast h1 .serif em{font-style:normal;color:var(--orange)}
.lede{max-width:64ch;color:var(--mast-2);font-size:16px}
.counts{display:flex;flex-wrap:wrap;gap:8px 10px;list-style:none;padding:0;margin:0}
.counts li{font-size:13.5px;font-weight:500;border:1px solid var(--mast-rule);border-radius:999px;padding:3px 12px;color:var(--mast-2)}
.counts b{color:var(--mast-ink);font-weight:800;font-variant-numeric:tabular-nums}

.inbox{margin-block:28px 8px;border:2px dashed var(--rule-strong);border-radius:14px;padding:20px 22px;display:grid;gap:14px;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);align-items:start;background:var(--panel)}
.inbox.has{border-style:solid;border-color:var(--orange)}
.inbox h2{font:900 clamp(24px,2.6vw,32px)/1 var(--f-serif);text-transform:uppercase}
.inbox ol{margin:0;padding-left:20px;display:grid;gap:6px;color:var(--ink-2);font-size:14.5px}
.inbox ol b{color:var(--ink);font-weight:500}
.inbox .state{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:13px;border-radius:999px;padding:4px 12px 4px 10px;justify-self:start;background:var(--info-bg);color:var(--info-ink)}
.inbox.has .state{background:var(--warn-bg);color:var(--warn-ink)}
.inbox .state::before{content:"";width:8px;height:8px;border-radius:50%;background:currentColor}
.inbox-left{display:grid;gap:10px}

.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-block:1px solid var(--rule);padding-block:12px;margin-top:20px}
.bar .wrap{display:grid;gap:10px}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.lbl{font:700 11px/1 var(--f-sans);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-2);margin-right:4px;min-width:72px}
.chip{font:500 13px/1 var(--f-sans);border:1px solid var(--rule-strong);background:var(--panel);color:var(--ink);border-radius:999px;padding:7px 12px;cursor:pointer}
.chip:hover{border-color:var(--orange)}
.chip[aria-pressed="true"]{background:var(--tapshoe);border-color:var(--tapshoe);color:#fff}
.chip .n{opacity:.7;margin-left:5px;font-variant-numeric:tabular-nums}
input[type=search]{padding:8px 12px;border:1px solid var(--rule-strong);border-radius:8px;background:var(--panel);color:var(--ink);flex:1 1 240px;max-width:420px;min-width:0}
.count{margin-left:auto;font-size:13px;color:var(--ink-2);font-variant-numeric:tabular-nums}

main{padding-block:10px 64px}
section.grp{padding-top:30px;display:grid;gap:14px}
.grp-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px}
.grp-head h2{font:900 clamp(26px,3vw,36px)/1 var(--f-serif);text-transform:uppercase}
.grp-head p{color:var(--ink-2);font-size:14.5px;max-width:70ch}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(min(100%,230px),1fr))}
.tile{display:flex;flex-direction:column;text-align:left;background:var(--panel);color:inherit;border:1px solid var(--rule);border-radius:12px;overflow:hidden;padding:0;cursor:zoom-in;transition:border-color .15s,transform .15s}
.tile:hover{border-color:var(--orange);transform:translateY(-2px)}
.thumb{aspect-ratio:4/3;background:var(--thumb);display:flex;align-items:center;justify-content:center;overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.info{padding:11px 13px 13px;display:grid;gap:6px;font-size:13px}
.subj{font-weight:500;font-size:14px;line-height:1.35}
.facts{display:flex;flex-wrap:wrap;gap:4px}
.f{font:500 11.5px/1 var(--f-sans);padding:4px 7px;border-radius:4px;background:var(--panel-2);color:var(--ink-2);font-variant-numeric:tabular-nums}
.f.ok{background:var(--ok-bg);color:var(--ok-ink)}
.f.warn{background:var(--warn-bg);color:var(--warn-ink)}
.use{color:var(--ink-2)}
.path{font:11.5px/1.35 var(--f-mono);color:var(--ink-2);overflow-wrap:anywhere}
.empty{border:1px dashed var(--rule-strong);border-radius:12px;padding:28px 22px;color:var(--ink-2);background:var(--panel);display:grid;gap:6px;max-width:70ch}
.empty b{color:var(--ink);font-weight:700}

dialog{border:0;border-radius:14px;padding:0;max-width:min(1040px,94vw);width:100%;background:var(--panel);color:var(--ink)}
dialog::backdrop{background:rgba(20,20,22,.72)}
.dlg{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr)}
.dlg .big{background:var(--thumb);display:flex;align-items:center;justify-content:center;min-height:320px}
.dlg .big img{max-width:100%;max-height:78vh;object-fit:contain;display:block}
.dlg .side{padding:20px 22px;display:grid;gap:12px;align-content:start;font-size:14px}
.dlg h3{font:900 24px/1.05 var(--f-serif);text-transform:uppercase}
.dlg dl{display:grid;grid-template-columns:auto 1fr;gap:7px 14px;margin:0}
.dlg dt{font:700 11px/1.6 var(--f-sans);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.dlg dd{margin:0;overflow-wrap:anywhere}
.close{justify-self:end;background:var(--panel-2);border:1px solid var(--rule);border-radius:999px;padding:6px 14px;color:var(--ink);cursor:pointer}
footer{border-top:1px solid var(--rule);padding-block:20px 40px;color:var(--ink-2);font-size:13px}
@media (max-width:760px){.inbox{grid-template-columns:1fr}.dlg{grid-template-columns:1fr}.lbl{min-width:0}}
@media (prefers-reduced-motion:reduce){.tile{transition:none}.tile:hover{transform:none}}
</style>

<header class="mast">
  <div class="wrap">
    <div class="mast-top">
      <img src="__LOGO__" alt="Habit Outdoors">
      <span class="links">
        <a class="pill-btn" href="__DS__" target="_blank" rel="noopener">← Design System</a>
        <a class="pill-btn" href="__HUB__" target="_blank" rel="noopener">Deliverables Hub →</a>
        <button class="pill-btn" id="theme-btn" type="button">Switch page theme</button>
      </span>
    </div>
    <h1><span class="sans">Approved photography</span><span class="serif">Image <em>Library</em></span></h1>
    <p class="lede">Every photo cleared or queued for Habit emails, with where text can sit on it and what it is good for. Click a photo for a large preview and its file path. Updated __UPDATED__.</p>
    <ul class="counts" id="counts"></ul>
  </div>
</header>

<div class="wrap"><section class="inbox" id="inbox"></section></div>

<div class="bar" role="region" aria-label="Filters"><div class="wrap">
  <div class="row" id="f-cat"><span class="lbl">Category</span></div>
  <div class="row" id="f-calm"><span class="lbl">Text area</span></div>
  <div class="row"><input type="search" id="q" placeholder="Search subject or use, e.g. sunrise, angler, collage" aria-label="Search photos"><span class="count" id="count"></span></div>
</div></div>

<main class="wrap" id="out"></main>
<footer><div class="wrap">Previews are compressed. Use the original file at the path shown, under <code>clients/habit-outdoors/01-brand/photos/</code>. Built by <code>photos/build_image_library.py</code> from <code>library/catalog.md</code>.</div></footer>

<dialog id="dlg" aria-label="Photo details"><div class="dlg"><div class="big"><img id="d-img" alt=""></div>
  <div class="side"><button class="close" id="d-close" type="button">Close</button><h3 id="d-title"></h3><dl id="d-list"></dl></div></div></dialog>

<script type="application/json" id="lib-data">__DATA__</script>
<script>
(function(){
  const D = JSON.parse(document.getElementById('lib-data').textContent);
  const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const GROUPS = [
    ['selected', 'Selected', 'The curated library. Photos land here after you drop them in the inbox and they are catalogued.'],
    ['original', 'Habit originals', 'Full-resolution Habit photos found on 2026-09-25. Release for email still to confirm with the client.'],
    ['crop', 'Provisional crops', 'Cut from the September sent emails at 1200px. Fine for collages; replace with originals for heroes.'],
  ];
  const CATS = ['hunting','fishing','camp','farm','detail','landscape'];
  const CALM = [['top','Top'],['bottom','Bottom'],['none','None']];
  const calmKey = s => { s = (s||'').toLowerCase(); return s.startsWith('top') ? 'top' : s.startsWith('bottom') ? 'bottom' : s.includes('top') ? 'top' : 'none'; };
  let st = {cat: null, calm: null, q: ''};

  try { const t = localStorage.getItem('habit-lib-theme'); if (t) document.documentElement.dataset.theme = t; } catch(e) {}
  document.getElementById('theme-btn').addEventListener('click', () => {
    const cur = document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('habit-lib-theme', next); } catch(e) {}
  });

  const n = c => D.items.filter(i => i.collection === c).length;
  document.getElementById('counts').innerHTML =
    `<li><b>${D.items.length}</b> photos</li><li><b>${n('selected')}</b> selected</li><li><b>${n('original')}</b> originals</li><li><b>${n('crop')}</b> provisional crops</li><li><b>${D.inbox.length}</b> in inbox</li>`;

  const ib = document.getElementById('inbox');
  ib.classList.toggle('has', D.inbox.length > 0);
  ib.innerHTML = `
    <div class="inbox-left">
      <span class="state">${D.inbox.length ? D.inbox.length + ' file' + (D.inbox.length > 1 ? 's' : '') + ' waiting' : 'Inbox empty'}</span>
      <h2>Add photos</h2>
      <p class="use">Drop the selected files, as they are, in <code>photos/library/_inbox/</code>.</p>
    </div>
    <ol>
      <li><b>Drop the files</b> in the inbox folder on OneDrive, any name, full resolution.</li>
      <li><b>Ask Claude</b> to “process the Habit image inbox”.</li>
      <li><b>Each photo is renamed, catalogued</b> (subject, category, text area, best use, rights) and moved to the library.</li>
      <li><b>This page is rebuilt</b> at the same link. Anything unknown, like rights or the photographer, is marked to confirm.</li>
    </ol>
    ${D.inbox.length ? `<div class="grid" style="grid-column:1/-1">${D.inbox.map(tile).join('')}</div>` : ''}`;

  function chips(id, opts, key){
    const box = document.getElementById(id);
    box.insertAdjacentHTML('beforeend', opts.map(([v, l]) => {
      const c = D.items.filter(i => (key === 'cat' ? i.category : calmKey(i.calm)) === v).length;
      return `<button class="chip" type="button" data-v="${v}" aria-pressed="false">${esc(l)}<span class="n">${c}</span></button>`;
    }).join(''));
    box.addEventListener('click', e => {
      const b = e.target.closest('.chip'); if (!b) return;
      st[key] = st[key] === b.dataset.v ? null : b.dataset.v;
      box.querySelectorAll('.chip').forEach(x => x.setAttribute('aria-pressed', x.dataset.v === st[key] ? 'true' : 'false'));
      render();
    });
  }
  chips('f-cat', CATS.map(c => [c, c[0].toUpperCase() + c.slice(1)]), 'cat');
  chips('f-calm', CALM, 'calm');
  document.getElementById('q').addEventListener('input', e => { st.q = e.target.value.trim().toLowerCase(); render(); });

  function tile(i){
    const rights = (i.rights||'').toLowerCase();
    const rc = rights === 'released' ? 'ok' : 'warn';
    return `<button class="tile" type="button" data-file="${esc(i.file)}" aria-label="${esc(i.subject)}">
      <span class="thumb">${i.thumb ? `<img src="${i.thumb}" alt="" loading="lazy">` : ''}</span>
      <span class="info">
        <span class="subj">${esc(i.subject)}</span>
        <span class="facts"><span class="f">${esc(i.px)}</span>${i.orient ? `<span class="f">${esc(i.orient)}</span>` : ''}${i.category ? `<span class="f">${esc(i.category)}</span>` : ''}<span class="f ${rc}">${esc(i.rights || 'to confirm')}</span></span>
        ${i.use ? `<span class="use">${esc(i.use)}</span>` : ''}
        <span class="path">${esc(i.file)}</span>
      </span></button>`;
  }

  function render(){
    const match = i => (!st.cat || i.category === st.cat) && (!st.calm || calmKey(i.calm) === st.calm) &&
      (!st.q || [i.subject, i.use, i.notes, i.file, i.category].join(' ').toLowerCase().includes(st.q));
    const shown = D.items.filter(match);
    document.getElementById('count').textContent = `${shown.length} of ${D.items.length} photos`;
    document.getElementById('out').innerHTML = GROUPS.map(([key, title, desc]) => {
      const list = shown.filter(i => i.collection === key);
      const total = D.items.filter(i => i.collection === key).length;
      let body;
      if (list.length) body = `<div class="grid">${list.map(tile).join('')}</div>`;
      else if (!total && key === 'selected') body = `<div class="empty"><b>No selected photos yet.</b><span>They appear here once the files you drop in <code>photos/library/_inbox/</code> are processed.</span></div>`;
      else if (!total) return '';
      else body = `<div class="empty">No photo in this collection matches the filters.</div>`;
      return `<section class="grp"><div class="grp-head"><h2>${esc(title)}</h2><p>${esc(desc)}</p></div>${body}</section>`;
    }).join('');
  }
  render();

  const dlg = document.getElementById('dlg');
  document.addEventListener('click', e => {
    const t = e.target.closest('.tile'); if (!t) return;
    const i = D.items.concat(D.inbox).find(x => x.file === t.dataset.file); if (!i) return;
    document.getElementById('d-img').src = i.big;
    document.getElementById('d-title').textContent = i.subject;
    const rowsHtml = [['File', i.file], ['Size', `${i.px} · ${i.mb} MB`], ['Collection', i.collection], ['Category', i.category], ['Text area', i.calm], ['Best use', i.use], ['Rights', i.rights], ['Notes', i.notes]]
      .filter(([, v]) => v).map(([k, v]) => `<dt>${k}</dt><dd>${esc(v)}</dd>`).join('');
    document.getElementById('d-list').innerHTML = rowsHtml;
    dlg.showModal();
  });
  document.getElementById('d-close').addEventListener('click', () => dlg.close());
  dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
})();
</script>
"""

if __name__ == "__main__":
    build()
