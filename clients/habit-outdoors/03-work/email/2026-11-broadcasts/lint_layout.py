"""Layout lint for the Habit Outdoors November 2026 broadcast HTML: catches collisions before anyone sees a render.
Adapted from clients/toms-of-maine/03-work/email/lint_layout.py (same idea: headless Chrome measures the DOM).

Usage: python lint_layout.py <email.html> [...]        (no argument: every 0*.html next to this file)
Runs each email twice: desktop (680px window, 600px column) and mobile (mobile media rules forced, 375px column).

Markup contract (build_emails.py):
  img.pk     packshot / product composition      img.photo  photo or photo composition
  img.edge   E18 torn edge row                    img.decor  decoration (none in this batch; kept for the kit rule)
  text       h1, h2, p, and button links (table.btn a)
  td[data-safe-top="N"] (+ data-safe-top-m)  background photo cell: no text above N px from the top of the cell

Checks (CSS px):
  1. width    the email column is wider than 600 (desktop) / 375 (mobile), or any element overflows the column
  2. image    text or button overlapping a .pk / .photo / .decor image (or within 4px of it)
  3. edge     text or button closer than 12px to a torn edge (.edge)
  4. photo    text placed over the photo part of a background-photo cell (data-safe-top)
  5. margin   text or button closer than 20px to the left/right edge of the email (footer excluded)
  6. text     two text blocks overlapping each other
  7. decor    decor less than 60% visible inside the column
  8. clip     a .pk image cut by the column edge (bleed is never intended in this batch)
Exit code 1 when anything is found.
"""
import glob
import html as H
import json
import os
import pathlib
import re
import subprocess
import sys

EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PROBE = r"""<script>window.addEventListener('load',()=>document.fonts.ready.then(()=>setTimeout(()=>{
const MOB=__MOB__;
document.documentElement.setAttribute('data-theme','light');   // headless Chrome here ignores --force-prefers-color-scheme: pin the light theme
const R=e=>{const b=e.getBoundingClientRect();return{x0:b.left,y0:b.top+scrollY,x1:b.right,y1:b.bottom+scrollY,w:b.width,h:b.height}};
const vis=e=>{const b=e.getBoundingClientRect(); if(b.width<1||b.height<1) return false; let n=e; while(n&&n.nodeType===1){const s=getComputedStyle(n); if(s.display==='none'||s.visibility==='hidden') return false; n=n.parentElement;} return true;};
const lab=e=>(e.tagName.toLowerCase())+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\s+/).join('.'):'')+' "'+(e.textContent||e.getAttribute('alt')||e.getAttribute('src')||'').trim().replace(/\s+/g,' ').slice(0,42)+'"';
const out=[]; const W=MOB?375:600;
const box=document.querySelector('table.container'); const C=R(box);
if(Math.round(C.w)>W) out.push(['width','column is '+Math.round(C.w)+'px wide',W,'']);
const all=[...document.querySelectorAll('table.container *')].filter(vis);
for(const e of all){const r=R(e); if(r.x1>C.x0+W+1||r.x0<C.x0-1){ if(e.closest('.mob-only')&&!MOB) continue; out.push(['width','overflows column',lab(e),Math.round(r.x0-C.x0)+'..'+Math.round(r.x1-C.x0)]); break;}}
const T=[...document.querySelectorAll('table.container h1, table.container h2, table.container p, table.container table.btn a')].filter(vis).filter(e=>(e.textContent||'').trim().length>0);
const imgs=[...document.querySelectorAll('img.pk, img.photo, img.decor')].filter(vis);
const edges=[...document.querySelectorAll('img.edge')].filter(vis);
const hit=(a,b,m=0)=>a.x0<b.x1+m&&a.x1>b.x0-m&&a.y0<b.y1+m&&a.y1>b.y0-m;
const inner=e=>{ // text box = the glyph area: for p/h use a Range so block width does not count
  if(e.tagName==='A') return R(e);
  const rg=document.createRange(); rg.selectNodeContents(e); const rs=[...rg.getClientRects()].filter(r=>r.width>0);
  if(!rs.length) return R(e);
  const b=R(e); return {x0:Math.min(...rs.map(r=>r.left)),x1:Math.max(...rs.map(r=>r.right)),y0:b.y0,y1:b.y1};};  // x = glyphs, y = line boxes
for(const t of T){const a=inner(t);
  for(const im of imgs){ if(im.contains(t)||t.contains(im)) continue; const b=R(im); if(hit(a,b,4)) out.push(['image',lab(t),lab(im),Math.round(a.y0-C.y0)]);}
  for(const ed of edges){const b=R(ed); if(hit(a,b,12)) out.push(['edge',lab(t),'torn edge at y '+Math.round(b.y0-C.y0),Math.round(a.y0-C.y0)]);}
  const cell=t.closest('[data-safe-top]'); if(cell){const s=+(MOB&&cell.dataset.safeTopM?cell.dataset.safeTopM:cell.dataset.safeTop); const b=R(cell); if(a.y0<b.y0+s) out.push(['photo',lab(t),'starts '+Math.round(a.y0-b.y0)+'px into the photo cell, safe from '+s,'']);}
  if(!t.closest('.footer')&&(a.x0<C.x0+20||a.x1>C.x0+W-20)) out.push(['margin',lab(t),Math.round(a.x0-C.x0),Math.round(a.x1-C.x0)]);
}
for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){const p=T[i],q=T[j]; if(p.contains(q)||q.contains(p))continue; if(hit(inner(p),inner(q),-1)) out.push(['text',lab(p),lab(q),Math.round(inner(p).y0-C.y0)]);}
for(const d of [...document.querySelectorAll('img.decor')].filter(vis)){const b=R(d); const vx=Math.max(0,Math.min(b.x1,C.x0+W)-Math.max(b.x0,C.x0)), vy=b.y1-b.y0; if(vx*vy<0.6*(b.x1-b.x0)*vy) out.push(['decor',lab(d),'visible '+Math.round(100*vx/(b.x1-b.x0))+'%','']);}
for(const im of [...document.querySelectorAll('img.pk')].filter(vis)){const b=R(im); if(b.x0<C.x0-1||b.x1>C.x0+W+1) out.push(['clip',lab(im),Math.round(b.x0-C.x0),Math.round(b.x1-C.x0)]);}
document.title='LINT'+JSON.stringify(out);},400)));</script>"""

MOBILE_STYLE = "<style>html,body{width:375px!important;max-width:375px!important;overflow-x:hidden!important}</style>"


def lint(path, mobile):
    src = open(path, encoding="utf-8").read()
    if mobile:
        src = src.replace("@media screen and (max-width: 620px)", "@media screen")
        src = src.replace("</head>", MOBILE_STYLE + "</head>")
    src = src.replace("</body>", PROBE.replace("__MOB__", "true" if mobile else "false") + "</body>")
    probe = os.path.join(os.path.dirname(os.path.abspath(path)), "_lint_probe.html")
    open(probe, "w", encoding="utf-8").write(src)
    try:
        dom = subprocess.run([EXE, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", "--hide-scrollbars",
                              "--window-size=680,3000", "--force-prefers-color-scheme=light", "--virtual-time-budget=10000",
                              "--dump-dom", pathlib.Path(probe).as_uri()],
                             capture_output=True, text=True, encoding="utf-8").stdout
    finally:
        os.remove(probe)
    m = re.search(r"<title>LINT(.*?)</title>", dom, re.S)
    return json.loads(H.unescape(m.group(1))) if m else [["error", "probe did not run", "", ""]]


def main(paths):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if not paths:
        here = os.path.dirname(os.path.abspath(__file__))
        paths = sorted(glob.glob(os.path.join(here, "0*.html")))
    bad = 0
    for p in paths:
        for mobile in (False, True):
            issues = lint(p, mobile)
            tag = "375" if mobile else "600"
            print(f'{os.path.basename(p)} @{tag}: {"OK" if not issues else str(len(issues)) + " issue(s)"}')
            for kind, a, b, c in issues:
                print(f"   [{kind}] {a} | {b} | {c}")
            bad += len(issues)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
