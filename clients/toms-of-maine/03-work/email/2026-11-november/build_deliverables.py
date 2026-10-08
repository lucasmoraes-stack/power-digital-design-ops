"""Build the Tom's November deliverables page (self-contained HTML) from the rendered emails.

Usage: python build_deliverables.py <out.html>
Edit EMAILS below as emails get built; a built email needs <slug>.jpg and <slug>_slices/ next to this file.
"""
import base64, io, os, sys, html
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

EMAILS = [
    dict(date='11/3', slug='01-rooted-in-nature-a', name='Rooted in Nature', sl="What's Inside Matters 🌿", ph='Transparency looks good on us', status='layout for review',
         notes=['Hero A (chosen): glass card on the autumn leaf; the three products now stand as one group on the teal wave, centred on the text axis, one shared shadow (10/20 cluster).',
                'Category rows: exact Figma shelf crops (10/8); names in the product-card type, 2-line box.']),
    dict(date='11/9', slug='02-the-deo-that-actually-works', name='The Deo That Actually Works', sl='Yes, Natural Deo Actually Works 😏', ph='Fresh all day. naturally.', status='layout for review',
         notes=['Hero: full-bleed photo (placeholder) with the text at the bottom; the subheadline "48 Hours. Zero Aluminum." rides on the approved starburst seal (8/6, 8/15, 9/11). Ref: Each & Every badge.',
                'Scents: the 10/13 split product card used as a checkerboard, sides and tints alternating. Ref: Each & Every checkerboard.',
                'Copy fix: added the missing space in "protection. This is".']),
    dict(date='11/18', slug='03-gifts-for-the-people-at-your-table', name='Gifts for the People at Your Table', sl='We Solved Holiday Gifting For You 🎁', ph='For every person at your table', status='layout for review',
         notes=['Hero: framed photo (placeholder) on #05453D, headline over the top of the frame, ruled kicker below. Ref: Kinship framed hero.',
                'Gift guide: persona label in Rubik teal + editorial product rows with hairlines and packshot tiles. Ref: Kinship "Get to know" list. Persona emojis left out of the image text.',
                'Closing teaser band "Something big is coming" on #05453D.']),
    dict(date='11/24', slug='04-something-is-coming', name='Something Is Coming', sl='Thankful For You (Seriously) 💚', ph="Stay close, you'll want to see this", status='layout for review',
         notes=['Hero: circle portrait with ring (10/2 family), placeholder portrait. The copy has no CTA in the thank-you section, so the hero has none.',
                'Teaser band on the deep-to-teal gradient, then the SMS signup band (8/15, 8/20 family) with a placeholder phone image.']),
    dict(date='11/27', slug='05-bfcm-announcement', name='BFCM Announcement', sl="Happy Friday! Here's 30% Off 🌿", ph="The moment we've been hinting at", status='layout for review',
         notes=['Hero: price-led (7.3 family) on #05453D, the subheadline "Enjoy 30% Off Sitewide" set as the big price; soap and toothpaste as a pair resting on the dome, with the thin arc line.',
                'Categories as a 2x2 packshot card grid (one product per category, none repeated from the hero), so it does not repeat the 11/3 shelf rows.']),
    dict(date='11/28', slug='06-gifts-that-actually-get-used', name='Gifts That Actually Get Used', sl="Gifts They'll Use Every Single Day 🎁", ph='Still time to shop 30% off sitewide', status='layout for review',
         notes=['Top banner + hero: photo on top (placeholder) and a light panel with the text, no seal (the top bar already carries the offer). Ref: Burt’s Bees.',
                'Bundles: one card per bundle with name, description and button together, light and deep alternating. Ref: Burt’s Bees product rows.',
                'Packshots needed: Everyday Essentials Starter Pack and Whole Care Oral Health Bundle (not in any approved email).']),
    dict(date='11/30', slug='07-last-full-day', name='Last Full Day', sl='Final Hours To Save 30% Sitewide 🚨', ph='Your last chance to stock up', status='layout for review',
         notes=['Hero: type-led urgency (9/7 family): ghost "30%" behind the headline. No photo needed, and no product trio (11/3 already has the product group).',
                'Six bundles in a 2x3 grid; same two packshots needed as 11/28.']),
    dict(date='12/1', slug='08-extended-24-hours', name='Extended 24 Hours', sl='Surprise! 30% Off Extended 24h ⏳', ph='Final hours, we mean it', status='layout for review',
         notes=['Top banner + hero built around a clock dial (drawn, no photo, no hands) with the headline inside.',
                'Four bundles as wide cards (9/27 wide-card family), image side alternating.']),
]

def jpg_uri(path, width=1200, q=80):
    im = Image.open(path).convert('RGB')
    if im.width > width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode(), im.size

def main(out):
    cards, previews = [], []
    for i, e in enumerate(EMAILS, 1):
        jpg = os.path.join(HERE, e['slug'] + '.jpg')
        built = os.path.exists(jpg)
        esc = html.escape
        cls = 'built' if built else 'todo'
        cards.append(f'<a class="card {cls}" href="#e{i}"><span class="d">{esc(e["date"])}</span><span class="n">{esc(e["name"])}</span><span class="st">{esc(e["status"])}</span></a>')
        if not built:
            previews.append(f'<section class="email todo" id="e{i}"><header><span class="d">{esc(e["date"])}</span><h2>{esc(e["name"])}</h2><span class="st">{esc(e["status"])}</span></header><dl class="meta"><dt>Subject</dt><dd>{esc(e["sl"])}</dd><dt>Preheader</dt><dd>{esc(e["ph"])}</dd></dl></section>')
            continue
        uri, (w, h) = jpg_uri(jpg)
        if e.get('variants'):
            figs = ''.join(f'<figure class="var"><figcaption>{esc(lbl)}</figcaption><img src="{jpg_uri(os.path.join(HERE, sl + ".jpg"), 600, 72)[0]}" alt="{esc(lbl)}"></figure>' for lbl, sl in e['variants'])
            notes = ''.join(f'<li>{esc(n)}</li>' for n in e.get('notes', []))
            previews.append(f'''<section class="email" id="e{i}"><header><span class="d">{esc(e["date"])}</span><h2>{esc(e["name"])}</h2><span class="st">{esc(e["status"])}</span></header>
<div class="side"><dl class="meta"><dt>Subject</dt><dd>{esc(e["sl"])}</dd><dt>Preheader</dt><dd>{esc(e["ph"])}</dd></dl><ul class="notes">{notes}</ul></div>
<div class="vars">{figs}</div></section>''')
            continue
        sdir = os.path.join(HERE, e['slug'] + '_slices')
        slices = sorted(os.listdir(sdir)) if os.path.isdir(sdir) else []
        srows = ''.join(f'<li><code>{esc(s)}</code> <span>{os.path.getsize(os.path.join(sdir, s))//1024} KB</span></li>' for s in slices)
        total = os.path.getsize(jpg) // 1024
        notes = ''.join(f'<li>{esc(n)}</li>' for n in e.get('notes', []))
        previews.append(f'''<section class="email" id="e{i}"><header><span class="d">{esc(e["date"])}</span><h2>{esc(e["name"])}</h2><span class="st">{esc(e["status"])}</span></header>
<div class="cols"><figure class="shot"><img src="{uri}" width="600" height="{round(h/2)}" alt="{esc(e["name"])} email, full render"></figure>
<div class="side"><dl class="meta"><dt>Subject</dt><dd>{esc(e["sl"])}</dd><dt>Preheader</dt><dd>{esc(e["ph"])}</dd><dt>Export</dt><dd>1200 × {h} JPG, {total} KB{f', {len(slices)} slices' if slices else ', slices after layout approval'}</dd></dl>
<h3>Decisions to check</h3><ul class="notes">{notes}</ul>{"<h3>Slices</h3><ol class=slices>" + srows + "</ol>" if slices else ""}</div></div></section>''')
    tpl = open(os.path.join(HERE, 'deliverables.tpl.html'), encoding='utf-8').read()
    page = tpl.replace('__CARDS__', ''.join(cards)).replace('__EMAILS__', ''.join(previews))
    open(out, 'w', encoding='utf-8').write(page)
    print(out, len(page) // 1024, 'KB')

if __name__ == '__main__':
    main(sys.argv[1])
