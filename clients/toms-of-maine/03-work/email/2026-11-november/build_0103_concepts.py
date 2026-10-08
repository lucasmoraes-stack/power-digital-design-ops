"""11/3 Rooted in Nature hero concepts (A, B, C). Superseded as a builder: build_november.py imports CONCEPTS and
SHARED_CSS from here and builds the full emails. Running this file directly does nothing.

Original note: built the concepts from 01-rooted-in-nature.html.

Usage: python build_0103_concepts.py   -> writes 01-rooted-in-nature-{a,b,c}.html next to this file
Only the hero changes between concepts; header, category band and footer are shared with the base file.
Render each with: python ../render_email.py 01-rooted-in-nature-a.html --slices
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '01-rooted-in-nature.html')
K = '../../../01-brand/email-kit/assets'
P = '../../../01-brand/photos/figma-lab'
A = 'assets'
WAVE = ('<svg class="wave" viewBox="0 0 1207.16 125.73" preserveAspectRatio="none"><path d="M0 33.0894V125.73H1207.16V33.0894C962.957 '
        '174.077 779.274 107.999 499.706 33.0894C276.052 -26.8387 73.3793 8.11935 0 33.0894Z" fill="#3DA79D"/></svg>')

COPY = dict(
    h1='Every ingredient<br>has a purpose',  # forced break: two balanced lines
    kicker='Care You Can Feel Good About',
    body='The holidays are coming, routines are about to get chaotic, and your bathroom shelf should be the last thing you overthink.',
    cta="See What's Inside",
)

# Shared hero pieces (all measures from the approved October heroes, see inventory/figma-modules.md T02)
SHARED_CSS = """
.hero{overflow:hidden}
.hero .stack{position:absolute;z-index:2;display:flex;flex-direction:column;align-items:center;gap:24px;color:#fff;text-align:center}
.hero h1{font-weight:600;font-size:64px;line-height:.9;letter-spacing:-.02em;text-box:trim-both cap alphabetic}
.hero .kicker{font-size:20.31px;line-height:1;text-transform:uppercase;white-space:nowrap}
.hero .body{font-weight:500;font-size:19.5px;line-height:1.2;letter-spacing:-.01em;text-box:trim-both cap alphabetic}
.hero .ruled{display:flex;flex-direction:column;align-items:center;gap:14.6px;font-size:25.2px;line-height:1;text-transform:uppercase;white-space:nowrap}
.hero .ruled::before,.hero .ruled::after{content:"";display:block;height:1.7px;width:100%;background:currentColor}
.btn span{text-box:trim-both cap alphabetic}
.pk{position:absolute;display:block}
"""

CONCEPTS = {
    # A: T02b glass card (10/8, calibrated in _fidelity/) on the autumn leaf macro (10/20 background), floating packshots
    'a': dict(
        label='A · Autumn glass',
        css="""
.hero{height:860px;background:#8a3f0e url("%(K)s/source/bg-autumn-leaf-macro-orange.jpg") center 42%%/600px auto no-repeat}
.glass{position:absolute;left:40.5px;top:48px;width:521px;padding:44px 0;border-radius:20px;display:flex;flex-direction:column;align-items:center;gap:25px;color:#fff;text-align:center;
  backdrop-filter:blur(22px) saturate(1.05) brightness(.72);
  background:linear-gradient(135deg,rgba(255,255,255,.10) 0%%,rgba(255,255,255,0) 40%%,rgba(0,0,0,.10) 100%%);
  box-shadow:inset 1.5px 1.5px 0 rgba(255,255,255,.28),inset -1px -1px 0 rgba(255,255,255,.10)}
.glass h1{width:470px;font-size:56px}
.glass .body{width:430px}
.cluster-a{position:absolute;z-index:4;inset:0;filter:drop-shadow(0 4px 6px rgba(0,0,0,.28)) drop-shadow(0 16px 18px rgba(0,0,0,.18))}
.cluster-a img{position:absolute;display:block}
""" % dict(K=K),
        html=f"""
  <div class="glass">
    <h1 class="nk">{COPY['h1']}</h1>
    <div class="kicker rb">{COPY['kicker']}</div>
    <p class="body nk">{COPY['body']}</p>
    <span class="btn white rb"><span>{COPY['cta']}</span></span>
  </div>
  <!-- product group standing on the teal wave (10/20 T02d cluster), one shared shadow -->
  <div class="cluster-a">
    <img src="{A}/deo-north-woods.png" style="left:121px;top:570px;height:258px" alt="">
    <img src="{A}/mw-sea-salt.png" style="left:193px;top:532px;height:294px" alt="">
    <img src="{A}/box-coconut.png" style="left:233px;top:745px;width:246px" alt="">
  </div>
  {WAVE}"""),

    # B: T02c scene on top, big headline below (10/13 family); still life of Whiten+ among leaves fading into deep green
    'b': dict(
        label='B · Still life on top',
        css="""
.hero{height:960px;background:#05453D}
.hero .scene{position:absolute;left:0;top:0;width:600px;height:500px;background:url("%(P)s/still-life-whiten-plus-toothpaste-leaves.png") center 30%%/auto 520px no-repeat}
.hero .scene::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,69,61,0) 55%%,rgba(5,69,61,.75) 82%%,#05453D 100%%)}
.hero .stack{left:30px;width:540px;top:500px}
.hero h1{width:540px}
.hero .ruled{width:390px}
.hero .body{font-size:20px;width:430px}
.fern{position:absolute;width:128.7px;height:195.8px;background:url("%(K)s/leaf-sprig-fern-ccfffa.png") center/100%% 100%% no-repeat;mix-blend-mode:soft-light;opacity:.9}
""" % dict(K=K, P=P),
        html=f"""
  <div class="scene"></div>
  <div class="stack">
    <h1 class="nk">{COPY['h1']}</h1>
    <div class="ruled rb">{COPY['kicker']}</div>
    <p class="body nk">{COPY['body']}</p>
    <span class="btn white rb"><span>{COPY['cta']}</span></span>
  </div>
  <div class="fern" style="left:-38px;top:610px;transform:rotate(-108deg)"></div>
  <div class="fern" style="left:500px;top:720px;transform:rotate(2deg)"></div>
  {WAVE}"""),

    # C: T02d text on photo + product cluster across an arc (10/20 family); forest trail, one product per category below
    'c': dict(
        label='C · Forest + lineup on arc',
        css="""
.hero{height:900px;background:#1b1a10 url("%(P)s/lifestyle-forest-trail-golden-light.jpg") center 58%%/600px auto no-repeat}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,14,8,.62) 0%%,rgba(10,14,8,.35) 45%%,rgba(10,14,8,0) 70%%)}
.hero .stack{left:30px;width:540px;top:66px}
.hero h1{width:540px}
.hero .ruled{width:400px}
.hero .body{width:424px}
.hero .arc{position:absolute;z-index:1;left:-1166.75px;top:700px;width:2933.5px;height:2933.5px;border-radius:50%%;background:#3DA79D}
.cluster{position:absolute;z-index:2;inset:0;filter:drop-shadow(4px 5px 9.5px rgba(0,0,0,.29)) drop-shadow(16px 20px 17.5px rgba(0,0,0,.2)) drop-shadow(36px 45px 24px rgba(0,0,0,.12))}
""" % dict(P=P),
        html=f"""
  <div class="stack">
    <h1 class="nk">{COPY['h1']}</h1>
    <div class="ruled rb">{COPY['kicker']}</div>
    <p class="body nk">{COPY['body']}</p>
    <span class="btn white rb"><span>{COPY['cta']}</span></span>
  </div>
  <div class="arc"></div>
  <div class="cluster">
    <img class="pk" src="{A}/deo-north-woods.png" style="left:150px;top:540px;height:265px" alt="">
    <img class="pk" src="{A}/soap-lemon.png" style="left:362px;top:690px;width:180px" alt="">
    <img class="pk" src="{A}/mw-sea-salt.png" style="left:234px;top:500px;height:320px" alt="">
    <img class="pk" src="{A}/box-coconut.png" style="left:60px;top:760px;width:250px" alt="">
  </div>"""),
}


def main():
    src = open(BASE, encoding='utf-8').read()
    # category rows: exact Figma crops of the 10/8 rows, cropped from the top to 200 as in 10/27
    rows = [('row1-oral-care', 'Oral Care', False), ('row2-bath-body', 'Bath &amp; Body', True),
            ('row3-deodorant', 'Deodorant &amp; Antiperspirant', False), ('row4-value-bundles', 'Bundles', True)]
    row_html = []
    for img, name, rev in rows:
        ph = (f'<img class="ph" src="{K}/source/figma-10-08/{img}.png" style="' +
              ('left:264.25px;width:264.5px' if rev else 'left:-15.25px;width:279.5px') + '" alt="">')
        panel = ('<div class="panel" style="' + ('left:-.25px;width:264.5px' if rev else 'left:264.25px;width:234.25px') +
                 f'"><div class="name nk">{name}</div><span class="btn dark sm rb"><span>shop now</span></span></div>')
        row_html.append(f'    <div class="row" data-slice="row">{ph}{panel}</div>')
    src = re.sub(r'  <div class="rows">.*?\n  </div>\n', '  <div class="rows">\n' + '\n'.join(row_html) + '\n  </div>\n', src, flags=re.S)
    src = re.sub(r'\.row\{.*?\n\.row \.name\{[^\n]*\n',
                 '.row{position:relative;height:200px;border-radius:40px;overflow:hidden}\n'
                 '.row .ph{position:absolute;bottom:0;height:255.6px}\n'
                 '.row .panel{position:absolute;top:0;height:200px;background:linear-gradient(180deg,#FFFFFF 0%,#E8E8E8 100%);'
                 'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:15.76px}\n'
                 '.row .name{font-weight:700;font-size:24px;line-height:1.2;letter-spacing:-.01em;color:var(--deep2);text-align:center;width:200px;text-box:trim-both cap alphabetic}\n',
                 src, flags=re.S)
    # Rubik SemiBold is not in the repo: keep only the Bold face so nothing falls back to Arial
    src = re.sub(r'@font-face\{font-family:"Rubik";font-weight:600;[^\n]*\n', '', src)
    # drop the v1 hero rules (T02f) and the v1 hero markup
    src = re.sub(r'/\* T02f hero.*?\n(?=\.wave)', '', src, flags=re.S)
    for key, c in CONCEPTS.items():
        out = src.replace('</style>', SHARED_CSS + c['css'] + '</style>')
        out = re.sub(r'<section class="hero" data-slice="hero">.*?</section>',
                     '<section class="hero" data-slice="hero">' + c['html'] + '\n</section>', out, flags=re.S)
        out = out.replace("<title>11/3 Rooted in Nature", f"<title>11/3 Rooted in Nature {c['label']}")
        path = os.path.join(HERE, f'01-rooted-in-nature-{key}.html')
        open(path, 'w', encoding='utf-8').write(out)
        print(path)


if __name__ == '__main__':
    print('Superseded: run build_november.py 01')
