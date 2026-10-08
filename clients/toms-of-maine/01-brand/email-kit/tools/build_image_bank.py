import re, io, base64, json, html, glob, os
from PIL import Image

ROOT = 'c:/Users/lucas/OneDrive/Desktop/VAZIO/power-digital-ops/clients/toms-of-maine/01-brand/'
LAB = ROOT + 'photos/figma-lab/'
OCT = ROOT + 'email-kit/assets/'
SCR = os.path.dirname(os.path.abspath(__file__)) + '/'

def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]

def tables(md):
    out, sec, hdr = [], None, None
    for line in md.splitlines():
        if line.startswith('## '):
            sec, hdr = line[3:].strip(), None
        elif line.startswith('|'):
            c = cells(line)
            if hdr is None: hdr = c
            elif set(''.join(c)) <= set('-: '): pass
            else: out.append((sec, dict(zip(hdr, c))))
        else:
            hdr = None if not line.strip() else hdr
    return out

def tick(s): return re.sub(r'`', '', s or '').strip()

DATE = re.compile(r'(?<![\d:])(\d{1,2})[./](\d{1,2})(?![\d:])')
def months(used):
    ms = set()
    for m, d in DATE.findall(used or ''):
        if 7 <= int(m) <= 10 and 1 <= int(d) <= 31: ms.add(int(m))
    if re.search(r'all (\d+ )?(6|20|26)', used or '') or 'all 6' in (used or ''):
        ms |= {10} if '6' in used else {7, 8, 9}
    return sorted(ms)

def clean_used(u):
    u = tick(u)
    u = re.sub(r'\(?e\.g\.[^)]*\)?', '', u)
    u = re.sub(r'\b\d{3,4}:\d+\b', '', u)
    u = re.sub(r'\s*,\s*(,\s*)+', ', ', u)
    u = re.sub(r'\(\s*…?\s*\)', '', u)
    u = re.sub(r'\s{2,}', ' ', u).strip(' ,·')
    return u

KIND_MAP = [
    ('logo', 'Logos and icons'), ('icon', 'Logos and icons'),
    ('packshot transparent', 'Packshots, transparent'),
    ('packshot white', 'Packshots on white'), ('packshot in package', 'Packshots on white'), ('packshot', 'Packshots on white'),
    ('lifestyle cut', 'Lifestyle cut-outs'), ('lifestyle', 'Lifestyle and scenes'), ('scene', 'Lifestyle and scenes'),
    ('still life', 'Product still life'), ('texture', 'Textures'),
    ('seal', 'Seals, badges and decor'), ('badge', 'Seals, badges and decor'), ('decorative', 'Seals, badges and decor'),
]
def group(kind, sec):
    k = (kind or '').lower()
    if 'transparent' in k and 'packshot' in k: return 'Packshots, transparent'
    if sec and sec.startswith('Packshots on white'): return 'Packshots on white'
    if sec and sec.startswith('Lifestyle cut'): return 'Lifestyle cut-outs'
    if sec and sec.startswith('Product still'): return 'Product still life'
    for key, g in KIND_MAP:
        if key in k: return g
    return 'Seals, badges and decor'

items = {}
# LAB
for sec, r in tables(open(LAB + 'index.md', encoding='utf-8').read()):
    f = tick(r.get('File', ''))
    if not f or sec.startswith('Not exported'): continue
    png = [x.strip() for x in f.split('/') if x.strip().endswith(('.png', '.jpg', '.jpeg'))]
    if not png: continue
    fn = png[0]
    key = tick(r.get('Hash', '')) or 'lab:' + fn
    note = tick(r.get('Note', ''))
    items[key] = dict(file=fn, path='01-brand/photos/figma-lab/' + fn, abs=LAB + fn,
        subject=re.split(r',\s', tick(r.get('Product / subject', '') or r.get('Subject', '')))[0] if r.get('Subject') else tick(r.get('Product / subject', '')), kind=tick(r.get('Kind', '')), group=group(r.get('Kind'), sec),
        px=tick(r.get('Original px', '') or r.get('PNG px (2x)', '')), transparent=tick(r.get('Transparent', '')).startswith('yes'),
        used=[clean_used(r.get('Used in (email · node)', ''))], months=set(months(r.get('Used in (email · node)', ''))),
        covered='covered' in (note + tick(r.get('Used in (email · node)', ''))).lower(), hidden=False, note=note,
        source='LAB', octname=tick(r.get('Also in Oct export', '')))
# October
oct_md = open(OCT + 'figma-export.md', encoding='utf-8').read()
oct_sec = oct_md[oct_md.index('## 4.'):]
for sec, r in tables(oct_sec):
    fn = tick(r.get('File (`source/`)', '') or r.get('File (source/)', ''))
    if not fn:
        fn = tick(next((v for k, v in r.items() if k.startswith('File')), ''))
    if not fn.endswith(('.png', '.jpg', '.jpeg')): continue
    h = tick(r.get('Hash', ''))
    used = r.get('Used in (node, email, display box)', '')
    hidden = 'hidden fill' in used.lower()
    covered = 'covered' in used.lower()
    if h in items:
        it = items[h]; it['used'].append(clean_used(used)); it['months'].add(10)
        it['hidden'] = it['hidden'] and hidden
    else:
        items[h] = dict(file=fn, path='01-brand/email-kit/assets/source/' + fn, abs=OCT + 'source/' + fn,
            subject=tick(r.get('Product / subject', '')), kind=tick(r.get('Kind', '')), group=group(r.get('Kind'), None),
            px=tick(r.get('Original px', '')), transparent=None, used=[clean_used(used)], months={10},
            covered=covered, hidden=hidden, note='', source='Oct', octname=fn)
# October decorative PNGs (rendered for the kit)
for p in sorted(glob.glob(OCT + '*.png')):
    b = os.path.basename(p)
    if re.match(r'(sample|portrait|product-1|texture-(light|dark)|logo)', b): continue
    if b.startswith(('icon-x', 'icon-facebook', 'icon-instagram', 'icon-tiktok', 'icon-pinterest', 'social-row')):
        g = 'Logos and icons'
    else:
        g = 'Seals, badges and decor'
    subj = b[:-4].replace('-', ' ')
    items['oct:' + b] = dict(file=b, path='01-brand/email-kit/assets/' + b, abs=p, subject=subj, kind='decorative (kit render)',
        group=g, px='', transparent=True, used=['October emails'], months={10}, covered=False, hidden=False, note='', source='Oct')
for b in ['logo-light.png', 'logo-dark.png']:
    p = OCT + b
    items['oct:' + b] = dict(file=b, path='01-brand/email-kit/assets/' + b, abs=p,
        subject='Header logo, teal (kit crop, 253x205)' if 'light' in b else 'Footer logo, white (kit, 203x164)',
        kind='logo', group='Logos and icons', px='', transparent=True, used=['all 26 emails'], months={7, 8, 9, 10},
        covered=False, hidden=False, note='ready-to-use kit file', source='Oct')

# drop raw logo/icon duplicates of the kit files
items = {k: v for k, v in items.items() if not (v['group'] == 'Logos and icons' and v['file'].endswith('-source.png') is False and v['source'] == 'LAB' and v['kind'] in ('logo', 'icon'))}

out, missing = [], []
for k, it in items.items():
    if not os.path.exists(it['abs']):
        missing.append(it['abs']); continue
    im = Image.open(it['abs'])
    if not it['px']: it['px'] = f'{im.width}x{im.height}'
    if it['transparent'] is None:
        it['transparent'] = im.mode in ('RGBA', 'LA') and im.getchannel('A').getextrema()[0] < 250
    im.draft('RGB', (720, 720)) if im.format == 'JPEG' else None
    im.thumbnail((360, 360))
    if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGBA')
    buf = io.BytesIO(); im.save(buf, 'WEBP', quality=72, method=4)
    it['thumb'] = base64.b64encode(buf.getvalue()).decode()
    it['months'] = sorted(it['months'])
    it['used'] = ' · '.join(u for u in it['used'] if u)
    it.pop('abs')
    out.append(it)

order = ['Packshots, transparent', 'Packshots on white', 'Product still life', 'Lifestyle and scenes', 'Lifestyle cut-outs', 'Textures', 'Seals, badges and decor', 'Logos and icons']
out.sort(key=lambda x: (order.index(x['group']), x['subject'].lower()))
json.dump(out, open(SCR + 'bank.json', 'w', encoding='utf-8'))
print(len(out), 'items', len(missing), 'missing')
for m in missing[:10]: print('missing', m)
from collections import Counter
print(Counter(x['group'] for x in out))
print(sum(len(x['thumb']) for x in out) // 1024, 'KB thumbs')
