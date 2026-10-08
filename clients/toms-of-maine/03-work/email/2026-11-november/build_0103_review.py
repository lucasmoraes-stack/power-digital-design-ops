"""Build the review page for the 11/3 hero concepts + the 10/8 fidelity calibration (self-contained HTML).

Usage: python build_0103_review.py <out.html>
Needs: 01-rooted-in-nature-{a,b,c}.png here, and ../_fidelity/10-08-ingredient-spotlight.png + figma/10-08-ingredient-spotlight-figma.png.
"""
import base64, io, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
FID = os.path.join(HERE, '..', '_fidelity')


def uri(path, width=600, q=78, crop=None):
    im = Image.open(path).convert('RGB')
    if crop: im = im.crop(crop)
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


CONCEPTS = [
    ('A', 'Autumn glass', '01-rooted-in-nature-a.png',
     'Glass card from the 10/8 hero, now calibrated against Figma, placed on the autumn leaf macro used in 10/20. North Woods deodorant and the Whiten+ Coconut Oil box float at the bottom edge.',
     ['Seasonal for November; warmest of the three.', 'Glass effect is a CSS approximation of the Figma GLASS effect.']),
    ('B', 'Still life on top', '01-rooted-in-nature-b.png',
     'Scene on top and a big headline below, the 10/13 structure. Whiten+ Deep Clean among mint leaves, fading into deep green, with the ruled kicker and soft-light fern sprigs.',
     ['Most literal read of "Rooted in Nature".', 'Tallest hero (960); the photo is a still life already approved in the LAB file.']),
    ('C', 'Forest and lineup', '01-rooted-in-nature-c.png',
     'Text on photo with a product cluster across an arc, the 10/20 structure. Forest trail at golden light; one product per category (deodorant, mouthwash, toothpaste, soap) previews the rows below.',
     ['Arc color is the teal of the band below, so the hero flows into the category rows.', 'Sea Salt mouthwash only exists at 600px; it renders slightly soft at this size.']),
]

CSS = """
/* Layout: a working review sheet. Three equal email columns, then a two-up calibration strip. */
:root{
  --ground:#F3F6F4; --surface:#FFFFFF; --ink:#0E2B27; --muted:#4F6863; --line:#D3E0DC;
  --deep:#05453D; --accent:#008D83; --chip:#E3F2EF;
  --display:"Literata",Georgia,serif; --ui:"Rubik",system-ui,sans-serif;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --ground:#0C1715; --surface:#13221F; --ink:#E4EFEC; --muted:#9AB3AD; --line:#26403B;
  --deep:#7FD3C7; --accent:#4CC3B6; --chip:#1A3330; color-scheme:dark}}
:root[data-theme="dark"]{
  --ground:#0C1715; --surface:#13221F; --ink:#E4EFEC; --muted:#9AB3AD; --line:#26403B;
  --deep:#7FD3C7; --accent:#4CC3B6; --chip:#1A3330; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font:400 15px/1.55 var(--ui);padding-inline:20px;padding-block:40px 64px}
.wrap{max-width:1240px;margin:0 auto;display:flex;flex-direction:column;gap:56px}
h1,h2{font-family:var(--display);color:var(--deep);text-wrap:balance;margin:0}
h1{font-size:clamp(30px,4vw,42px);line-height:1.1;font-weight:600}
h2{font-size:26px;line-height:1.2;font-weight:600}
h3{font:600 17px/1.3 var(--ui);margin:0}
p{margin:0;max-width:68ch}
.eyebrow{font:600 12px/1 var(--ui);letter-spacing:.08em;text-transform:uppercase;color:var(--accent)}
header{display:flex;flex-direction:column;gap:14px}
.meta{display:flex;flex-wrap:wrap;gap:8px}
.chip{background:var(--chip);color:var(--deep);border-radius:999px;padding:4px 12px;font-size:13px}
section{display:flex;flex-direction:column;gap:20px}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;align-items:start}
.concept{display:flex;flex-direction:column;gap:12px}
.concept .head{display:flex;align-items:baseline;gap:10px}
.letter{font:600 28px/1 var(--display);color:var(--accent)}
.concept ul{margin:0;padding-left:18px;color:var(--muted);font-size:14px;display:flex;flex-direction:column;gap:4px}
.concept p{color:var(--muted);font-size:14px}
.shot{background:var(--surface);border:1px solid var(--line);border-radius:6px;overflow:hidden}
.shot img{display:block;width:100%;height:auto}
.scroll{max-height:1100px;overflow-y:auto}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;align-items:start}
.cap{font-size:13px;color:var(--muted);margin-top:8px}
table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;color:var(--muted);font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.tablewrap{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:6px}
.ok{color:var(--accent);font-weight:600}
.stats{display:flex;flex-wrap:wrap;gap:32px}
.stat{display:flex;flex-direction:column;gap:2px}
.stat b{font:600 30px/1 var(--display);color:var(--deep);font-variant-numeric:tabular-nums}
.stat span{font-size:13px;color:var(--muted)}
@media (max-width:900px){.grid3{grid-template-columns:1fr}.scroll{max-height:none}}
@media (max-width:640px){.grid2{grid-template-columns:1fr}}
"""


def main(out):
    cols = []
    for letter, name, png, desc, notes in CONCEPTS:
        cols.append(f"""
      <article class="concept">
        <div class="head"><span class="letter">{letter}</span><h3>{name}</h3></div>
        <p>{desc}</p>
        <ul>{''.join(f'<li>{n}</li>' for n in notes)}</ul>
        <div class="shot scroll"><img src="{uri(os.path.join(HERE, png), 600)}" alt="11/3 concept {letter}, full email"></div>
      </article>""")
    figma = uri(os.path.join(FID, 'figma', '10-08-ingredient-spotlight-figma.png'), 560, 74)
    html_ = uri(os.path.join(FID, '10-08-ingredient-spotlight.png'), 560, 74)
    page = f"""<title>Rooted in Nature Heroes</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,600&family=Rubik:wght@400;600&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <header>
    <span class="eyebrow">Tom's of Maine · November broadcast</span>
    <h1>11/3 Rooted in Nature: pick a hero</h1>
    <p>Three hero directions for the same email. Everything below the hero is identical, so only the hero changes between columns. Each one reuses a hero family from the approved October emails. Copy is verbatim from the November copy doc.</p>
    <div class="meta"><span class="chip">SL: What's Inside Matters</span><span class="chip">PH: Transparency looks good on us</span><span class="chip">1200px JPG, sliced</span></div>
  </header>

  <section>
    <h2>Hero concepts</h2>
    <div class="grid3">{''.join(cols)}
    </div>
    <p class="cap">Shared below the hero: section intro and four category rows on the teal band (10/27 layout), now using the exact Figma crops of the shelf photos. Nav, footer and the CTA stand-in font are Montserrat until the Gotham files arrive.</p>
  </section>

  <section>
    <span class="eyebrow">Calibration</span>
    <h2>10/8 Ingredient Spotlight, rebuilt in HTML</h2>
    <p>Before redoing 11/3 we rebuilt an approved email from the Figma values and compared it pixel by pixel with the Figma export. It matches closely enough to build the November emails in HTML with confidence.</p>
    <div class="stats">
      <div class="stat"><b>8165 px</b><span>same total height as Figma (2x)</span></div>
      <div class="stat"><b>3.4 / 255</b><span>mean pixel difference, whole email</span></div>
      <div class="stat"><b>0 px</b><span>offset on headings, images, buttons, rows</span></div>
    </div>
    <div class="tablewrap"><table>
      <thead><tr><th>Finding</th><th>What we did</th><th>Status</th></tr></thead>
      <tbody>
        <tr><td>Outline cards: Figma's inside stroke does not push the padding; CSS does (text sat 2px low)</td><td>Padding set to 38/30 for a 2px border</td><td class="ok">Fixed</td></tr>
        <tr><td>Hero background is rotated 90° inside the Figma crop</td><td>Found the crop by image matching; exported a rotated copy</td><td class="ok">Fixed</td></tr>
        <tr><td>Glass effect only exists in Figma</td><td>CSS blur + tint, tuned to the Figma colors (hero mean difference 7.2)</td><td>Close match</td></tr>
        <tr><td>Nav and footer sit 1 to 2px off</td><td>Gotham is missing; Montserrat stands in</td><td>Waiting on Gotham .otf</td></tr>
      </tbody></table></div>
    <div class="grid2">
      <div><div class="shot scroll"><img src="{figma}" alt="10/8 Figma export"></div><p class="cap">Figma export (approved)</p></div>
      <div><div class="shot scroll"><img src="{html_}" alt="10/8 HTML rebuild"></div><p class="cap">HTML rebuild</p></div>
    </div>
  </section>
</div>
"""
    open(out, 'w', encoding='utf-8').write(page)
    print(out, os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    main(sys.argv[1])
