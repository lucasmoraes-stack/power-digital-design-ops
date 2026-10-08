"""Build the Tom's of Maine module catalogue page (screenshots + specs) from the two Figma inventories.

Usage: python tools/build_module_catalog.py <out.html>
Reads inventory/figma-modules.md (October, T ids), inventory/figma-lab-modules.md (Jul to Sep, L ids),
references/figma-*.png and references/lab-*.png, and HANDOFF.md (open questions).
"""
import base64, glob, io, os, re, sys, html
import markdown
from PIL import Image

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(KIT, 'references')
NK = os.path.join(KIT, '..', 'identity', 'fonts', 'New Kansas Bold.otf')

FAMILIES = [
    ('Header and announcement', ['T01', 'L01', 'L02']),
    ('Heroes', ['T02', 'L03']),
    ('Section intro and headings', ['T03', 'L04', 'L16', 'L24']),
    ('Product cards and grids', ['T04', 'T05', 'L05', 'L06', 'L07', 'L08', 'L09', 'L10']),
    ('Feature and highlight bands', ['T06', 'T07', 'T08', 'T09', 'L11', 'L12', 'L15', 'L17']),
    ('Values, claims and reviews', ['T10', 'T11', 'L13', 'L14']),
    ('Closing, offer details and signup', ['T12', 'L18', 'L19', 'L20']),
    ('Seals, dividers and decor', ['T13', 'T14', 'T15', 'T16', 'T17', 'L21', 'L22', 'L23']),
    ('Footer', ['T18', 'L25']),
    ('Buttons', ['B01', 'B02', 'B03']),
]

def sections(path, src):
    md = open(path, encoding='utf-8').read()
    out = {}
    parts = re.split(r'(?m)^(##+) ', md)
    # parts: [pre, '##', 'title\nbody', '###', ...]
    for i in range(1, len(parts), 2):
        level, rest = parts[i], parts[i + 1]
        title, _, body = rest.partition('\n')
        m = re.match(r'([TLB]\d{2}[a-z]?)\b', title)
        if not m: continue
        mid = m.group(1)
        out.setdefault(src + ':' + mid, dict(id=mid, title=title.strip(), body=body.strip(), level=len(level), src=src))
    return out

def thumb(path):
    im = Image.open(path).convert('RGB')
    if im.width > 600: im = im.resize((600, round(im.height * 600 / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=74, method=4)
    return base64.b64encode(b.getvalue()).decode(), im.width, im.height

def shots_for(mid, src):
    pre = 'figma-' if src == 'Oct' else 'lab-'
    files = sorted(glob.glob(os.path.join(REF, f'{pre}{mid}-*.png')))
    if len(mid) == 3:  # family id: include lettered variants only if the family has no own sections
        files += []
    return files

def label(f):
    b = os.path.basename(f)[:-4]
    b = re.sub(r'^(figma|lab)-[TLB]\d{2}[a-z]?-', '', b)
    m = re.search(r'-(\d{2})-(\d{2})$', b)
    date = f'{int(m.group(1))}/{int(m.group(2))}' if m else ''
    name = b[:m.start()] if m else b
    return name.replace('-', ' '), date

def main(out_path):
    secs = {}
    secs.update(sections(os.path.join(KIT, 'inventory', 'figma-modules.md'), 'Oct'))
    secs.update(sections(os.path.join(KIT, 'inventory', 'figma-lab-modules.md'), 'Jul to Sep'))
    mdc = markdown.Markdown(extensions=['tables'])
    fam_html, toc = [], []
    used_files = set()
    for fam, ids in FAMILIES:
        blocks = []
        for base in ids:
            for key, s in secs.items():
                if not re.fullmatch(base + r'[a-z]?', s['id']): continue
                files = [f for f in shots_for(s['id'], s['src'] if s['src'] == 'Oct' else 'LAB') if f not in used_files]
                # family heading (e.g. T02, L03) with lettered children: skip shots here
                used_files.update(files)
                imgs = []
                for f in files:
                    b64, w, h = thumb(f)
                    name, date = label(f)
                    imgs.append(f'<figure><img loading="lazy" src="data:image/webp;base64,{b64}" width="{w}" height="{h}" alt="{html.escape(s["id"] + " " + name)}"><figcaption>{html.escape(name)}{" · " + date if date else ""}</figcaption></figure>')
                mdc.reset()
                body = mdc.convert(s['body'])
                anchor = (s['src'][:3] + '-' + s['id']).lower().replace(' ', '')
                src_lbl = 'October · VAZIO DRAFT' if s['src'] == 'Oct' else 'July to September · LAB'
                ttl = html.escape(re.sub(r'^[TLB]\d{2}[a-z]?\s*', '', s['title']).replace('`', ''))
                shots_html = ''.join(imgs) or '<p class="none">No screenshot for this entry; see the spec.</p>'
                sid = html.escape(s['id'])
                blocks.append(f'''<article class="mod" id="{anchor}"><header><span class="mid">{sid}</span><h3>{ttl}</h3><span class="src">{src_lbl}</span></header>
<div class="cols"><div class="shots">{shots_html}</div><div class="spec">{body}</div></div></article>''')
                toc.append((fam, anchor, s['id']))
        fid = re.sub(r'\W+', '-', fam.lower()).strip('-')
        fam_html.append(f'<section class="fam" id="{fid}"><h2>{html.escape(fam)}</h2>{"".join(blocks)}</section>')
    nav = ''.join('<a href="#%s">%s</a>' % (re.sub(r'\W+', '-', fam.lower()).strip('-'), html.escape(fam)) for fam, _ in FAMILIES)
    ho = open(os.path.join(KIT, 'HANDOFF.md'), encoding='utf-8').read()
    oq = ho[ho.index('## Open questions'):]
    oq = oq.split('\n', 1)[1]
    mdc.reset(); oq_html = mdc.convert(oq)
    left = ho[ho.index('## Left to do'):ho.index('## Waiting on the owner')].split('\n', 1)[1]
    mdc.reset(); left_html = mdc.convert(left)
    tpl = open(os.path.join(KIT, 'tools', 'module-catalog.tpl.html'), encoding='utf-8').read()
    # New Kansas Bold subset for headings
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
        opt = subset.Options(); opt.flavor = 'woff'
        ft = TTFont(NK); ss = subset.Subsetter(opt)
        ss.populate(text=''.join(chr(c) for c in range(32, 127)) + '’'); ss.subset(ft)
        bb = io.BytesIO(); ft.flavor = 'woff'; ft.save(bb); nk = base64.b64encode(bb.getvalue()).decode()
    except Exception:
        nk = ''
    page = (tpl.replace('__NK700__', nk).replace('__NAV__', nav).replace('__BODY__', ''.join(fam_html))
               .replace('__OPEN__', oq_html).replace('__LEFT__', left_html)
               .replace('__COUNT__', str(len(toc))).replace('__SHOTS__', str(len(used_files))))
    open(out_path, 'w', encoding='utf-8').write(page)
    print(out_path, len(page) // 1024, 'KB', len(toc), 'entries', len(used_files), 'screenshots')

if __name__ == '__main__':
    main(sys.argv[1])
