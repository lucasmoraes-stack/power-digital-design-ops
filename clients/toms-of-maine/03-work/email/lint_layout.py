"""Layout lint for the Tom's email HTML: catches collisions before anyone sees a render.

Usage: python lint_layout.py <email.html> [...]
Checks (600px CSS coordinates):
  1. text or button touching a wave box or inside a dome circle (wave/dome must clear text by 12px)
  2. text or button overlapping decor (sprig, fern), a packshot, or a seal (decor never over text, kit T15)
  3. text or button closer than 20px to the left/right edge of the email, or cut by its section
  4. two text blocks overlapping each other
Exit code 1 when anything is found.
"""
import json, os, re, subprocess, sys, html as H, pathlib

EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROBE = r"""<script>window.addEventListener('load',()=>document.fonts.ready.then(()=>setTimeout(()=>{
const R=e=>{const b=e.getBoundingClientRect();return{x0:b.left,y0:b.top+scrollY,x1:b.right,y1:b.bottom+scrollY}};
const lab=e=>(e.className&&e.className.baseVal===undefined?e.className:'')+' "'+(e.textContent||'').trim().slice(0,40)+'"';
const T=[...document.querySelectorAll('h1,h2,p,.btn,.kick,.kicker,.ruled,.plabel,.desc,.topbar span,.footer .t')].filter(e=>e.getBoundingClientRect().width>0);
const textOnly=T.filter(e=>!e.closest('.btn')||e.classList.contains('btn'));
const out=[];const pad=12;
const clip=(e)=>{const r=R(e);const s=e.closest('section');if(!s)return r;const b=R(s);return{x0:Math.max(r.x0,0),y0:Math.max(r.y0,b.y0),x1:Math.min(r.x1,600),y1:Math.min(r.y1,b.y1)}};
const same=(a,b)=>a.closest('section')===b.closest('section');
const hit=(a,b,m=0)=>a.x0<b.x1+m&&a.x1>b.x0-m&&a.y0<b.y1+m&&a.y1>b.y0-m;
const waves=[...document.querySelectorAll('svg.wave')];
const domes=[...document.querySelectorAll('.dome')];
const decor=[...document.querySelectorAll('.sprig,.fern,.pk,img.shadow,.cluster img,.cluster-a img,.seal,.abs>img')];
for(const t of textOnly){const a=R(t);
  for(const w of waves){const b=R(w); if(hit(a,b,pad)) out.push(['wave',lab(t),Math.round(a.y1),Math.round(b.y0)]);}
  for(const d of domes){if(!same(d,t))continue;const b=R(d);const cx=(b.x0+b.x1)/2,cy=(b.y0+b.y1)/2,r=(b.x1-b.x0)/2+pad;
    for(const [x,y] of [[a.x0,a.y1],[a.x1,a.y1],[(a.x0+a.x1)/2,a.y1]]) if((x-cx)**2+(y-cy)**2<r*r){out.push(['dome',lab(t),Math.round(a.y1),Math.round(b.y0)]);break;}}
  for(const d of decor){if(d.contains(t)||t.contains(d))continue;const b=clip(d); if(b.x1-b.x0<4||b.y1-b.y0<4)continue; if(hit(a,b,4)) out.push(['decor',lab(t),d.className||d.getAttribute('src'),Math.round(a.y0)]);}
  if(!t.closest('.footer')&&(a.x0<20||a.x1>580)) out.push(['edge',lab(t),Math.round(a.x0),Math.round(a.x1)]);
  const s=t.closest('section'); if(s){const b=R(s); if(a.y0<b.y0-1||a.y1>b.y1+1) out.push(['cut',lab(t),Math.round(a.y0),Math.round(b.y1)]);}
}
for(let i=0;i<textOnly.length;i++)for(let j=i+1;j<textOnly.length;j++){const p=textOnly[i],q=textOnly[j];
  if(p.contains(q)||q.contains(p))continue; if(hit(R(p),R(q),-1)) out.push(['text',lab(p),lab(q),Math.round(R(p).y0)]);}
document.title='LINT'+JSON.stringify(out);},300)));</script>"""


def lint(path):
    src = open(path, encoding='utf-8').read()
    probe = os.path.join(os.path.dirname(os.path.abspath(path)), '_lint_probe.html')
    open(probe, 'w', encoding='utf-8').write(src.replace('</body>', PROBE + '</body>'))
    try:
        dom = subprocess.run([EXE, '--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--window-size=600,3000',
                              '--virtual-time-budget=8000', '--dump-dom', pathlib.Path(probe).as_uri()],
                             capture_output=True, text=True, encoding='utf-8').stdout
    finally:
        os.remove(probe)
    m = re.search(r'<title>LINT(.*?)</title>', dom, re.S)
    return json.loads(H.unescape(m.group(1))) if m else [['error', 'probe did not run', '', '']]


def main(paths):
    bad = 0
    for p in paths:
        issues = lint(p)
        print(f'{os.path.basename(p)}: {"OK" if not issues else str(len(issues)) + " issue(s)"}')
        for kind, a, b, c in issues:
            print(f'   [{kind}] {a} | {b} | {c}')
        bad += len(issues)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main(sys.argv[1:])
