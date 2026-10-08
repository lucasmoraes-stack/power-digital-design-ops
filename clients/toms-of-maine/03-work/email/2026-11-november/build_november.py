"""Build the 8 Tom's of Maine November broadcast emails from one shared block set.

Usage: python build_november.py            -> writes every email HTML next to this file
       python build_november.py 05 06      -> only emails whose slug starts with these numbers
Render: python ../render_email.py <file.html> [--slices]

Copy: "Tom's _November Broadcast - Copy 2026.pdf", pages 65 to 73 (pre-approved, verbatim; headings in sentence case as in the
approved October emails). Measures: inventory/figma-modules.md (T..) and figma-lab-modules.md (L..), product cards from
LAB 407:3817. Product packshots are real (./assets, built by prep_assets.py); every other image is a marked placeholder
(class "ph") until the owner picks images.
"""
import os, sys
import build_0103_concepts as c0103

HERE = os.path.dirname(os.path.abspath(__file__))
K = '../../../01-brand/email-kit/assets'
F = '../../../01-brand/identity/fonts'
P = '../../../01-brand/photos/figma-lab'
A = 'assets'
WAVE_D = ('M0 33.0894V125.73H1207.16V33.0894C962.957 174.077 779.274 107.999 499.706 33.0894C276.052 -26.8387 '
          '73.3793 8.11935 0 33.0894Z')

CSS = """
@font-face{font-family:"New Kansas";font-weight:500;src:url("%(F)s/New Kansas Medium.otf");}
@font-face{font-family:"New Kansas";font-weight:600;src:url("%(F)s/New Kansas SemiBold.otf");}
@font-face{font-family:"New Kansas";font-weight:700;src:url("%(F)s/New Kansas Bold.otf");}
@font-face{font-family:"Rubik";font-weight:700;src:url("%(F)s/rubik/Rubik-Bold.ttf");}
/* Gotham not available yet: Montserrat stand-in */
@font-face{font-family:"Gotham";font-weight:700;src:url("%(F)s/gotham/Gotham-Bold.otf"),url("%(F)s/montserrat/Montserrat-Bold.ttf");}
@font-face{font-family:"Gotham";font-weight:500;src:url("%(F)s/gotham/Gotham-Medium.otf"),url("%(F)s/montserrat/Montserrat-Medium.ttf");}

:root{--deep:#05453D;--deep2:#044D44;--accent:#008D83;--nav:#00867D;--navy:#295791;--navy-bar:#24436F;
  --sheen:linear-gradient(225deg,#FFFFFF 2.07%%,#C8EEEB 55.4%%,#FFFFFF 106.72%%);--panel:linear-gradient(180deg,#FFFFFF 0%%,#E8E8E8 100%%)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
html{overflow-x:hidden}
body{width:600px;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
img{display:block}
.nk{font-family:"New Kansas",Georgia,serif}
.rb{font-family:"Rubik",Arial,sans-serif;font-weight:700}
.gt{font-family:"Gotham","Montserrat",Arial,sans-serif}
.trim{text-box:trim-both cap alphabetic}
section{position:relative;width:600px}
.abs{position:absolute}

/* placeholders: concept images to be chosen by the owner */
.ph{position:absolute;inset:0;background:#3C5A52 repeating-linear-gradient(135deg,rgba(255,255,255,.07) 0 14px,rgba(255,255,255,0) 14px 28px)}
.ph.light{background:#DCE8E5 repeating-linear-gradient(135deg,rgba(5,69,61,.06) 0 14px,rgba(5,69,61,0) 14px 28px)}
.ph .tag{position:absolute;left:14px;top:14px;max-width:300px;padding:7px 10px;border-radius:6px;background:rgba(0,0,0,.45);color:#fff;font:700 11px/1.35 "Rubik",Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase}
.ph.light .tag{background:rgba(5,69,61,.85)}
.ph.br .tag{left:auto;top:auto;right:14px;bottom:14px}
.ph.tr .tag{left:auto;right:14px}
.ph.round{border-radius:50%%}
.ph.round .tag{left:50%%;top:50%%;transform:translate(-50%%,-50%%);text-align:center;max-width:180px}
.missing{width:100%%;height:100%%;border:2px dashed #7FB8B1;border-radius:12px;display:flex;align-items:center;justify-content:center;text-align:center;padding:10px;color:#2F6E66;font:700 11px/1.35 "Rubik",Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase}

/* T01 header */
.header{height:110.5px;background:#fff}
.header .logo{position:absolute;left:43.2px;top:7.5px;width:126.5px;height:102.5px}
.header .nav{position:absolute;left:252.2px;top:53.5px;width:325.5px;height:22.5px;font-weight:700;font-size:14px;color:var(--nav);text-transform:uppercase;white-space:pre;line-height:22.5px}

/* L02 announcement bar */
.topbar{height:50.5px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:23.5px;line-height:1;text-transform:uppercase;white-space:nowrap}

/* B01 / B02 buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;height:50.3px;padding:0 17.55px;border-radius:11.7px;font-size:20.72px;line-height:29.6px;text-transform:uppercase;white-space:nowrap;flex:none}
.btn span{text-box:trim-both cap alphabetic}
.btn.white{background:#fff;color:var(--deep)}
.btn.dark{background:var(--deep);color:#fff}
.btn.sm{width:139px;height:42.8px;padding:0;border-radius:10.07px;font-size:18.11px;line-height:1}

/* waves and domes */
.wave{position:absolute;z-index:3;left:-1.8px;bottom:-1px;width:603.6px;height:62.9px}
.wave.down{transform:scaleX(-1)}
.wave.top{bottom:auto;top:-1px;transform:scale(-1,-1)}
.dome{position:absolute;z-index:1;left:-1166.75px;width:2933.5px;height:2933.5px;border-radius:50%%}

/* T03 section heading + intro */
.band{display:flex;flex-direction:column;align-items:center;gap:40px;padding:55px 0 48px}
.hgroup{display:flex;flex-direction:column;align-items:center;gap:24px;text-align:center}
.h2{font-weight:700;font-size:42px;line-height:1.05;text-wrap:balance;text-box:trim-both cap alphabetic}
.lead{font-weight:500;font-size:19.5px;line-height:1.2;letter-spacing:-.01em;text-wrap:balance;text-box:trim-both cap alphabetic}
.light-t{color:var(--deep)}
.dark-t{color:#fff}

/* hero text pieces */
.h1{font-weight:600;font-size:64px;line-height:.9;letter-spacing:-.02em;text-box:trim-both cap alphabetic}
.kick{font-size:20.31px;line-height:1;text-transform:uppercase;white-space:nowrap}
.ruled{width:fit-content;display:flex;flex-direction:column;align-items:center;gap:14.6px;font-size:25.2px;line-height:1;text-transform:uppercase;white-space:nowrap}
.ruled::before,.ruled::after{content:"";display:block;height:1.7px;width:100%%;background:currentColor}
.body{font-weight:500;font-size:19.5px;line-height:1.2;letter-spacing:-.01em;text-wrap:balance;text-box:trim-both cap alphabetic}
.stack{position:absolute;z-index:4;display:flex;flex-direction:column;align-items:center;gap:24px;text-align:center}
.stack.left{align-items:flex-start;text-align:left}

/* L05 / LAB 407:3817 product card */
.grid{display:grid;grid-template-columns:253px 253px;gap:15px}
.pcard{width:253px;padding:26.5px 6.5px;border-radius:20px;background:var(--sheen);display:flex;flex-direction:column;align-items:center;justify-content:flex-start;gap:20px}
.pcard .img{width:169.5px;height:167.5px;display:flex;align-items:center;justify-content:center}
.pcard .img.wide{width:212px}
.pcard .img img{max-width:100%%;max-height:100%%;object-fit:contain}
.pcard .txt{display:flex;flex-direction:column;align-items:center;gap:10.76px;width:240px}
/* Card names: always a 2-line box, one size per email: the largest of 24/22/20/18 that fits every name in 2 lines (script in page()) */
.pcard .pname,.wcard .pname,.split .pname,.lrow .pname,.brow .pname{font-size:var(--pn,24px);height:2.4em;width:100%%;display:flex;align-items:center;justify-content:center;text-box:none}
.pname{font-weight:600;font-size:24px;line-height:1.2;letter-spacing:-.01em;color:var(--deep);text-align:center;text-wrap:balance;text-box:trim-both cap alphabetic}
.mult{mix-blend-mode:multiply}

/* T09 category rows (10/27 height) */
.rows{width:498.5px;display:flex;flex-direction:column;gap:15px}
.row{position:relative;height:200px;border-radius:40px;overflow:hidden}
.row .phot{position:absolute;bottom:0;height:255.6px}
.row .pan{position:absolute;top:0;height:200px;background:var(--panel);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10.76px}
.row .pname{width:200px;height:2.4em;display:flex;align-items:center;justify-content:center;text-box:none}

/* T08 label pill */
.pill{width:521px;padding:18px 32px;border-radius:20px;border:3px solid #91FFF5;background:#0C9389;color:#fff;text-align:center}
.pill .pname{color:#fff}

/* L09 wide card */
.wcard{width:521px;height:220.5px;border-radius:20px;background:var(--sheen);display:flex;align-items:center;gap:14px;padding:0 20px 0 20px}
.wcard.rev{flex-direction:row-reverse}
.wcard .img{width:190px;height:190px;display:flex;align-items:center;justify-content:center;flex:none}
.wcard .img img{max-width:100%%;max-height:100%%;object-fit:contain}
.wcard .txt{width:277px;display:flex;flex-direction:column;align-items:center;gap:10.76px;flex:none}

/* outline card (T06) */
.ocard{border:2px solid var(--accent);border-radius:20px;padding:30px 24px;display:flex;align-items:center;justify-content:center;text-align:center}
.cap{font-weight:500;font-size:21px;line-height:1.2;letter-spacing:-.02em;color:var(--deep);text-wrap:balance;text-box:trim-both cap alphabetic}

/* decor */
.sprig{position:absolute;width:163.5px;height:194.3px;background:url("%(K)s/leaf-sprig-008d83.png") center/100%% 100%% no-repeat}
.sprig.deep{background-image:url("%(K)s/leaf-sprig-05453d.png")}
.fern{position:absolute;width:128.7px;height:195.8px;background:url("%(K)s/leaf-sprig-fern-ccfffa.png") center/100%% 100%% no-repeat;mix-blend-mode:soft-light;opacity:.9}
.shadow{filter:drop-shadow(4px 5px 7px rgba(0,0,0,.3)) drop-shadow(16px 20px 13px rgba(0,0,0,.22)) drop-shadow(36px 45px 17px rgba(0,0,0,.1))}

/* T08 split card as checkerboard (11/9) */
.split{width:521px;height:210px;border-radius:20px;overflow:hidden;display:flex}
.split .half{width:260.5px;height:100%%;display:flex;flex-direction:column;align-items:center;justify-content:center}
.split .half img{height:172px;width:auto}
.split .half.dark{background:var(--deep);gap:12px;padding:0 6px}
.split .pname{color:#fff}

/* editorial persona list (11/18) */
.persona{width:521px;display:flex;flex-direction:column}
.plabel{font-size:18.1px;line-height:1;text-transform:uppercase;color:var(--accent);padding-bottom:14px;border-bottom:1.5px solid var(--accent);letter-spacing:.02em}
.lrow{display:flex;align-items:center;gap:20px;padding:16px 0;border-bottom:1px solid #B9DCD7}
.lrow .txt{flex:1;display:flex;flex-direction:column;align-items:flex-start;gap:10.76px}
.lrow .pname{text-align:left;justify-content:flex-start}
.lrow .tile{width:170px;height:150px;border-radius:16px;background:var(--sheen);display:flex;align-items:center;justify-content:center;padding:12px;flex:none}
.lrow .tile img{max-width:100%%;max-height:100%%}

/* bundle rows (11/28) */
.brow{width:521px;border-radius:20px;background:var(--sheen);display:flex;align-items:center;gap:20px;padding:18px 22px 18px 18px}
.brow.dark{background:var(--deep)}
.brow.dark .pname,.brow.dark .desc{color:#fff}
.brow .tile{width:180px;height:170px;border-radius:14px;background:#fff;display:flex;align-items:center;justify-content:center;padding:10px;flex:none}
.brow .tile img{max-width:100%%;max-height:100%%}
.brow .txt{flex:1;display:flex;flex-direction:column;align-items:flex-start;gap:10px}
.brow .pname{text-align:left;justify-content:flex-start}
.brow .desc{font-weight:500;font-size:16px;line-height:1.25;letter-spacing:-.01em;color:var(--deep);text-wrap:pretty}

/* T18 footer */
.footer{height:587px;background:var(--navy-bar)}
.footer .main{position:absolute;left:0;top:0;width:600px;height:455.5px;background:var(--navy)}
.footer .t{position:absolute;left:0;width:600px;text-align:center;color:#fff;font-weight:700}
.footer .learn{top:79px;font-size:14px;line-height:20px;text-decoration:underline;text-underline-offset:2px}
.footer .flogo{position:absolute;left:249.8px;top:126.5px;width:101.4px;height:82px}
.footer .social{position:absolute;left:220.3px;top:238.5px;width:160px;height:32px}
.footer .navlist{top:294px;font-size:14px;line-height:28px}
.footer .legal{font-size:10px;line-height:28px;white-space:pre}
""" % dict(F=F, K=K)


# ---------- blocks ----------

def header():
    return f"""<section class="header" data-slice="header">
  <img class="logo" src="{K}/logo-light.png" alt="Tom's of Maine">
  <div class="nav gt">OUR MISSION      PRODUCTS      SHOP NOW</div>
</section>"""


def footer():
    return f"""<section class="footer" data-slice="footer">
  <div class="main"></div>
  <div class="t gt learn">Learn what we mean by natural on our website.</div>
  <img class="flogo" src="{K}/logo-dark.png" alt="Tom's of Maine">
  <img class="social" src="{K}/social-row.png" alt="">
  <div class="t gt navlist">Our Mission<br>Products<br>Shop Now<br>Blog</div>
  <div class="t gt legal" style="top:470px">Tom’s of Maine · 2 Storer Street, Suite 302 · Kennebunk, ME 04043 · USA</div>
  <div class="t gt legal" style="top:503.5px">©%%= v(@CurrentYear) =%% Tom's of Maine, Inc.</div>
  <div class="t gt legal" style="top:541px">Privacy Policy  l  Terms of Sale  l   Terms of Use  l  Unsubscribe</div>
</section>"""


def topbar(text, bg='#008D83'):
    return f'<section class="topbar rb" data-slice="topbar" style="background:{bg}"><span class="trim">{text}</span></section>'


def wave(fill, cls=''):
    return (f'<svg class="wave {cls}" viewBox="0 0 1207.16 125.73" preserveAspectRatio="none">'
            f'<path d="{WAVE_D}" fill="{fill}"/></svg>')


def ph(label, cls='', style=''):
    return f'<div class="ph {cls}" style="{style}"><span class="tag">Image placeholder · {label}</span></div>'


def btn(label, skin='dark', extra='', style=''):
    return f'<span class="btn {skin} {extra} rb" style="{style}"><span>{label}</span></span>'


def hgroup(h2, lead=None, theme='light-t', h2w=498.5, leadw=470):
    lead_html = f'<p class="lead nk" style="width:{leadw}px">{lead}</p>' if lead else ''
    return f'<div class="hgroup {theme}" data-slice="intro"><h2 class="h2 nk" style="width:{h2w}px">{h2}</h2>{lead_html}</div>'


def img_tag(img, mult=False, style=''):
    if not img:
        return '<div class="missing">Packshot needed</div>'
    return f'<img src="{A}/{img}" class="{"mult" if mult else ""}" style="{style}" alt="">'


def pcard(name, img, wide=False, mult=False, slice_=True):
    return (f'<div class="pcard"{" data-slice=card" if slice_ else ""}><div class="img{" wide" if wide else ""}">{img_tag(img, mult)}</div>'
            f'<div class="txt"><div class="pname nk">{name}</div>{btn("shop now", "dark", "sm")}</div></div>')


def wcard(name, img, rev=False, mult=False):
    return (f'<div class="wcard{" rev" if rev else ""}" data-slice="card"><div class="img">{img_tag(img, mult)}</div>'
            f'<div class="txt"><div class="pname nk">{name}</div>{btn("shop now", "dark", "sm")}</div></div>')


def grid(cards):
    return '<div class="grid">' + ''.join(cards) + '</div>'


def category_rows(names):
    """T09 rows, exact Figma shelf crops of 10/8, top-cropped to 200 as in 10/27."""
    imgs = ['row1-oral-care', 'row2-bath-body', 'row3-deodorant', 'row4-value-bundles']
    out = []
    for i, (img, name) in enumerate(zip(imgs, names)):
        rev = i % 2 == 1
        photo = (f'<img class="phot" src="{K}/source/figma-10-08/{img}.png" style="' +
                 ('left:264.25px;width:264.5px' if rev else 'left:-15.25px;width:279.5px') + '" alt="">')
        pan = (f'<div class="pan" style="' + ('left:-.25px;width:264.5px' if rev else 'left:264.25px;width:234.25px') +
               f'"><div class="pname nk">{name}</div>{btn("shop now", "dark", "sm")}</div>')
        out.append(f'<div class="row" data-slice="row">{photo}{pan}</div>')
    return '<div class="rows">' + ''.join(out) + '</div>'


def category_cards(names):
    """2x2 category cards: shelf photo on top, name + button on the sheen."""
    imgs = ['row1-oral-care', 'row2-bath-body', 'row3-deodorant', 'row4-value-bundles']
    pos = ['30% 100%', '50% 100%', '35% 100%', '50% 100%']
    cards = []
    for img, name, p in zip(imgs, names, pos):
        cards.append(f'<div class="pcard" data-slice="card" style="padding:0 0 26.5px;overflow:hidden;justify-content:flex-start">'
                     f'<div style="width:253px;height:190px;background:url(\'{K}/source/figma-10-08/{img}.png\') {p}/cover no-repeat"></div>'
                     f'<div class="txt"><div class="pname nk">{name}</div>{btn("shop now", "dark", "sm")}</div></div>')
    return grid(cards)


def page(title, comment, sections, extra_css=''):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title} · Tom's of Maine</title>
<!-- {comment} -->
<style>{CSS}{extra_css}</style>
</head>
<body>
{chr(10).join(sections)}
<script>
document.fonts.ready.then(() => {{
  const names = [...document.querySelectorAll('.pcard .pname, .wcard .pname, .split .pname, .lrow .pname, .brow .pname')];
  if (!names.length) return;
  for (const px of [24, 22, 20, 18]) {{
    document.documentElement.style.setProperty('--pn', px + 'px');
    if (names.every(n => n.scrollHeight <= n.clientHeight + 1)) {{ document.documentElement.dataset.pn = px; break; }}
  }}
}});
</script>
</body>
</html>
"""


# ---------- emails ----------

ROWS_0103 = ['Oral Care', 'Bath &amp; Body', 'Deodorant &amp; Antiperspirant', 'Bundles']


def e01(concept):
    c = c0103.CONCEPTS[concept]
    hero = '<section class="hero" data-slice="hero">' + c['html'] + '\n</section>'
    band = f"""<section class="band" style="background:linear-gradient(180deg,#3DA79D 0%,#C8EEEB 100%)">
  {hgroup('Proud of every ingredient', "Every Tom's formula is made with naturally sourced and derived ingredients. One less thing to worry about.", 'light-t', 420, 450)}
  {category_rows(ROWS_0103)}
  <div data-slice="cta">{btn('Shop Naturally Sourced', 'white')}</div>
</section>"""
    # the concept CSS targets .hero .stack/.h1 etc. from build_0103_concepts; keep it scoped to .hero
    return page(f"11/3 Rooted in Nature {c['label']}",
                "SL: What's Inside Matters · PH: Transparency looks good on us. Hero concept from build_0103_concepts.py; band T03 + T09 rows (10/27).",
                [header(), hero, band, footer()],
                '.hero{position:relative;width:600px}' + c0103.SHARED_CSS + c['css'])


def seal(text, size=150, rot=-12, left=0, top=0, z=6):
    """L21 starburst seal (8/6, 8/15, 9/11): 24-point star, deep-teal gradient, inner outline, NK SemiBold white."""
    import math
    def star(r1, r2, n=24):
        pts = []
        for i in range(n * 2):
            r = r1 if i % 2 == 0 else r2
            a = math.pi * i / n - math.pi / 2
            pts.append(f'{50 + r * math.cos(a):.2f},{50 + r * math.sin(a):.2f}')
        return ' '.join(pts)
    gid = f'sg{left}{top}'.replace('.', '').replace('-', 'm')
    return (f'<div class="abs seal" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px;z-index:{z};transform:rotate({rot}deg)">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" style="position:absolute;inset:0">'
            f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset=".24" stop-color="#05453D"/>'
            f'<stop offset=".48" stop-color="#0CAB97"/><stop offset=".68" stop-color="#05453D"/></linearGradient></defs>'
            f'<polygon points="{star(50, 45)}" fill="url(#{gid})"/>'
            f'<polygon points="{star(42, 38)}" fill="none" stroke="#3DA79D" stroke-width=".9"/></svg>'
            f'<div class="nk" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;'
            f'color:#fff;font-weight:600;font-size:{size * .125:.1f}px;line-height:.92;letter-spacing:-.04em;padding:0 {size * .2:.0f}px">{text}</div></div>')


SPLIT_TINTS = ['#A0E0FB', '#C8EEEB']


def split_card(name, img, rev=False, tint='#A0E0FB'):
    """T08 split product card (10/13), alternating sides, used as a checkerboard (Each & Every rhythm)."""
    pack = f'<div class="half" style="background:{tint}"><img src="{A}/{img}" alt=""></div>'
    txt = f'<div class="half dark"><div class="pname nk">{name}</div>{btn("shop now", "white", "sm")}</div>'
    return f'<div class="split" data-slice="card">{txt + pack if rev else pack + txt}</div>'


def e02():
    deos = [('Mountain Spring<br>Aluminum Free Deodorant', 'deo-mountain-spring.png'),
            ('North Woods<br>Aluminum Free Deodorant', 'deo-north-woods.png'),
            ('Moonlit Meadow<br>Aluminum Free Deodorant', 'deo-moonlit-meadow.png'),
            ('Twilight Breeze<br>Aluminum Free Deodorant', 'deo-twilight-breeze.png'),
            ('Tropical Island<br>Aluminum Free Deodorant', 'deo-tropical-island.png'),
            ('Unscented<br>Aluminum Free Deodorant', 'deo-unscented.png')]
    hero = f"""<section data-slice="hero" style="height:810px;overflow:hidden">
  {ph('Close-up: hand holding North Woods deodorant, outdoors, fresh light; subject in the upper half', 'tr')}
  <div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(3,19,17,0) 45%,rgba(3,19,17,.78) 70%,rgba(3,19,17,.92) 100%)"></div>
  {seal('48 Hours.<br>Zero Aluminum.', 150, -12, 410, 245)}
  <div class="stack" style="left:30px;width:540px;top:430px;color:#fff">
    <h1 class="h1 nk" style="width:540px">Protection<br>that shows up</h1>
    <p class="body nk" style="width:470px">Let's skip the part where you wonder if natural deodorant actually works. Ours delivers 48 hour odor protection. This is the one you'll want a backup of.</p>
    {btn('Shop Deodorant', 'white')}
  </div>
  {wave('#FFFFFF')}
</section>"""
    cards = ''.join(split_card(n, i, rev=k % 2 == 1, tint=SPLIT_TINTS[k % 2]) for k, (n, i) in enumerate(deos))
    band = f"""<section class="band" style="background:var(--panel);padding-top:40px">
  {hgroup('A scent for every vibe', None, 'light-t')}
  <div style="display:flex;flex-direction:column;gap:12px">{cards}</div>
  <div data-slice="cta">{btn('Shop All Deodorant', 'dark')}</div>
</section>"""
    return page('11/9 The Deo That Actually Works',
                'SL: Yes, Natural Deo Actually Works · PH: Fresh all day. naturally. Hero: full-bleed photo, text at the bottom, L21 seal carrying the subheadline. Scents: T08 split cards as a checkerboard (ref Each & Every), tints alternating.',
                [header(), hero, band, footer()])


def lrow(name, img, mult=False):
    """Editorial list row (ref Kinship): name + button left, packshot tile right, hairline below."""
    return (f'<div class="lrow" data-slice="card"><div class="txt"><div class="pname nk">{name}</div>{btn("shop now", "dark", "sm")}</div>'
            f'<div class="tile">{img_tag(img, mult)}</div></div>')


def e03():
    groups = [
        ('For the smile enthusiast', [('Whiten Plus Deep Clean Whitening Peppermint Natural Toothpaste', 'tp-whiten-deep-clean-peppermint.png'),
                                      ('Fresh Mint Whole Care Anticavity Natural Mouthwash', 'mw-whole-care-fresh-mint.png')]),
        ('For the one who loves a good scent', [('North Woods Aluminum Free Deodorant', 'deo-north-woods.png'),
                                                ('Moonlit Meadow Aluminum Free Deodorant', 'deo-moonlit-meadow.png')]),
        ("For the hostess (or yourself, we won't tell)", [('Lavender &amp; Shea Natural Beauty Bar Soap For Women and Men', 'soap-lavender-shea.png'),
                                                          ('Lemon Bergamot Natural Beauty Bar Soap For Women and Men', 'soap-lemon-bergamot.png')]),
    ]
    blocks = ''.join(
        f'<div class="persona"><div class="plabel rb" data-slice="pill"><span class="trim">{label}</span></div>'
        + ''.join(lrow(n, i) for n, i in items) + '</div>' for label, items in groups)
    hero = f"""<section data-slice="hero" style="height:890px;overflow:hidden;background:var(--deep)">
  <div class="abs" style="left:20px;top:20px;width:560px;height:500px;border-radius:20px;overflow:hidden">
    {ph('Holiday table: people gathering, warm light, Tom’s on the table; keep the top third calm for the headline', 'br')}
    <div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(3,19,17,.75) 0%,rgba(3,19,17,0) 50%)"></div>
  </div>
  <div class="stack" style="left:30px;width:540px;top:62px;color:#fff">
    <h1 class="h1 nk" style="width:540px;font-size:52px;white-space:nowrap">Care worth sharing<br>this season</h1>
  </div>
  <div class="stack" style="left:30px;width:540px;top:556px;color:#fff">
    <div class="ruled rb" style="font-size:22px">Natural Care For Your Favorite People</div>
    <p class="body nk" style="width:470px">You're hosting, gathering, and showing up for the people who matter. Skip the generic gift aisle, make a practical gift that people actually reach for every day.</p>
    {btn('Shop The Gift Guide', 'white')}
  </div>
  {wave('#FFFFFF')}
</section>"""
    band = f"""<section class="band" style="background:var(--panel);padding:30px 0 110px">
  {hgroup('A pick for every person', "From the fresh breath friend to the bar soap snob,<br>there's a Tom's for everyone on your list.", 'light-t', 498.5, 480)}
  {blocks}
  {wave('#C8EEEB')}
</section>"""
    teaser = f"""<section class="band" data-slice="teaser" style="background:#C8EEEB;padding:40px 0 55px">
  {hgroup('Something big is coming', "Our biggest event of the year is almost here. Stay tuned, you'll want to be ready for this one.", 'light-t', 460, 430)}
  {btn('Shop Everyday Essentials', 'dark')}
</section>"""
    return page('11/18 Gifts for the People at Your Table',
                'SL: We Solved Holiday Gifting For You · PH: For every person at your table. Hero: framed photo on #05453D (ref Kinship). Gift guide: persona label + editorial product rows (ref Kinship). Teaser band.',
                [header(), hero, band, teaser, footer()])


def e04():
    hero = f"""<section data-slice="hero" style="height:830px;overflow:hidden;background:linear-gradient(180deg,#FFFFFF 0%,#C8EEEB 100%)">
  <div class="stack" style="left:30px;width:540px;top:64px">
    <h1 class="h1 nk" style="color:var(--deep);width:540px">We're grateful<br>you're here</h1>
  </div>
  <div class="abs" style="left:160.35px;top:226px;width:279.3px;height:279.3px;border-radius:50%;border:6.5px solid var(--nav)"></div>
  <div class="abs" style="left:177.35px;top:243px;width:245.3px;height:245.3px;border-radius:50%;overflow:hidden">{ph('Portrait: family or founders, warm and candid', 'round')}</div>
  <div class="sprig deep" style="left:-52px;top:330px;transform:rotate(-11deg)"></div>
  <div class="sprig deep" style="left:458px;top:250px;transform:rotate(169deg)"></div>
  <div class="stack" style="left:69.5px;width:461px;top:545px">
    <div class="ruled rb" style="color:var(--deep)">From Our Family To Yours</div>
    <p class="body nk" style="color:var(--deep);font-size:20px;width:461px">Before the holiday rush took over, we wanted to pause and say thank you. For choosing transparency. For caring about what's in your routine. For being part of this with us.</p>
  </div>
  {wave('#05453D')}
</section>"""
    teaser = f"""<section class="band" data-slice="teaser" style="background:linear-gradient(180deg,#05453D 0%,#0CAB97 100%);padding:60px 0 150px;overflow:hidden">
  <div class="fern" style="left:-6px;top:266px;transform:scaleX(-1) rotate(2deg)"></div>
  <div class="fern" style="left:478px;top:266px;transform:rotate(2deg)"></div>
  {hgroup('Something big is almost here', "Our biggest event of the year is right around the corner. We can't say more yet, but trust us, you'll want to be ready. Keep your eyes on your inbox.", 'dark-t', 440, 440)}
  {btn('Stay Tuned', 'white')}
  {wave('#EAF7F5')}
</section>"""
    sms = f"""<section class="band" data-slice="sms" style="background:#EAF7F5;padding:30px 0 50px;gap:28px">
  <div class="hgroup light-t">
    <img src="{P}/icon-phone-008d83.png" style="width:47.7px;height:47.7px" alt="">
    <h2 class="nk trim" style="font-weight:700;font-size:57.85px;line-height:.8;width:520px">First dibs?<br>Join our text list</h2>
    <p class="lead nk" style="width:480px">Want to be the first to know when it drops? Join our SMS list for early access, exclusive offers, and zero spam. Just the good stuff, straight to your phone.</p>
    {btn('Sign Up For SMS', 'dark')}
  </div>
  <div style="position:relative;width:521px;height:300px;border-radius:20px;overflow:hidden">{ph('Phone in hand showing a Tom’s text, light background', 'light')}</div>
</section>"""
    return page('11/24 Something Is Coming',
                'SL: Thankful For You (Seriously) · PH: Stay close, you\'ll want to see this. Hero T02a circle portrait (no CTA in copy); teaser band; L18 SMS band.',
                [header(), hero, teaser, sms, footer()])


def e05():
    hero = f"""<section data-slice="hero" style="height:880px;overflow:hidden;background:var(--deep)">
  <img class="abs shadow" src="{A}/soap-lemon-bergamot.png" style="z-index:3;left:60px;top:705px;width:200px;transform:rotate(-6deg)" alt="">
  <img class="abs shadow" src="{A}/tp-whiten-coconut.png" style="z-index:3;left:300px;top:735px;width:240px;transform:rotate(-4deg)" alt="">
  <div class="stack" style="left:30px;width:540px;top:72px;color:#fff;gap:22px">
    <h1 class="nk trim" style="font-weight:600;font-size:40px;line-height:1;letter-spacing:-.03em;width:330px">Natural care<br>for everyone</h1>
    <div class="nk trim" style="font-weight:600;font-size:120px;line-height:1;letter-spacing:-.04em">Enjoy<br>30% OFF<br><span style="display:block;font-size:96px;margin-top:-18px">sitewide</span></div>
    <p class="body nk" style="width:430px">All month we said thank you, now here's the proof. 30% off sitewide on everyday essentials. For you and everyone at your table.</p>
    {btn('Shop 30% Off', 'white')}
  </div>
  <div class="dome" style="top:800px;background:#008D83"></div>
  <div class="dome" style="top:821.5px;background:none;border:1px solid rgba(255,255,255,.7);z-index:2"></div>
</section>"""
    band = f"""<section class="band" style="background:#008D83;padding-top:30px">
  {hgroup('Favorites for every routine', "If you're restocking your own routine or grabbing something for the people in your life, these are the products people come back to again and again.", 'dark-t', 470, 490)}
  {grid([pcard('Oral Care', 'tp-whiten-deep-clean-peppermint.png', wide=True), pcard('Bath &amp; Body', 'soap-lavender-shea.png', wide=True), pcard('Deodorant &amp; Antiperspirant', 'deo-mountain-spring.png'), pcard('Bundles', 'bundle-most-loved-deodorant.jpg', wide=True, mult=True)])}
  <div data-slice="cta">{btn('Explore The Sale', 'white')}</div>
</section>"""
    return page('11/27 BFCM Announcement',
                "SL: Happy Friday! Here's 30% Off · PH: The moment we've been hinting at. Hero L03b price-led on #05453D with packshots + dome and arc line; category cards 2x2.",
                [header(), hero, band, footer()])


BUNDLES = [
    ('Most-Loved Deodorant Bundle', 'bundle-most-loved-deodorant.jpg',
     'Three fan-favorite scents in one box. The "I don\'t know what they like" problem, solved.'),
    ('Everyday Essentials Starter Pack', None, 'Oral care, body care, all in one pack. The gift that covers every bathroom shelf.'),
    ('Back to Nature Bundle', 'bundle-back-to-nature.jpg', 'For the nature lover who also appreciates smelling great.'),
    ('Sensitive Skin &amp; Smile Bundle', 'bundle-sensitive-skin-smile.jpg',
     "Two sensitive toothpastes and a gentle beauty bar. For the person who's picky in the best way."),
    ('Best Sellers Beauty Bar Trio', 'bundle-best-sellers-bar-trio.jpg', 'Three bar soaps, three scents. The hostess gift that impresses.'),
    ('Whole Care Oral Health Bundle', None, 'Toothpaste, mouthwash, and floss in one click. The complete smile routine, gifted.'),
]


def brow(name, img, desc, dark=False):
    """Bundle row (ref Burt's Bees): white packshot tile left, name + description + button inside one card; fills alternate."""
    return (f'<div class="brow{" dark" if dark else ""}" data-slice="card"><div class="tile">{img_tag(img, True)}</div>'
            f'<div class="txt"><div class="pname nk">{name}</div><p class="desc nk">{desc}</p>'
            f'{btn("shop now", "white" if dark else "dark", "sm")}</div></div>')


def e06():
    rows = ''.join(brow(n, i, d, dark=k % 2 == 1) for k, (n, i, d) in enumerate(BUNDLES))
    hero = f"""<section data-slice="hero" style="height:960px;overflow:hidden;background:var(--sheen)">
  <div class="abs" style="left:0;top:0;width:600px;height:430px">{ph('Gift scene: Tom’s bundles wrapped in kraft paper and twine, overhead', '')}</div>
  <div class="stack" style="left:30px;width:540px;top:492px;color:var(--deep)">
    <h1 class="h1 nk" style="width:540px">Practical care<br>gifts they'll love</h1>
    <div class="ruled rb">Give Something They'll Reach For</div>
    <p class="body nk" style="font-size:20px;width:461px">The best gifts are the ones people actually use. Everyday essentials made with naturally sourced and derived ingredients. 30% off right now.</p>
    {btn('Shop Gifts At 30% Off', 'dark')}
  </div>
  {wave('#FFFFFF')}
</section>"""
    band = f"""<section class="band" style="background:#fff;padding-top:40px">
  {hgroup('Ready-made gifts, wrapped up', 'Bundles take the guesswork out of gifting. Each one pairs favorites together so you can give a complete routine and still have time to enjoy the weekend.', 'light-t', 440, 480)}
  <div style="display:flex;flex-direction:column;gap:14px">{rows}</div>
  <div data-slice="cta">{btn('Shop All Bundles', 'dark')}</div>
</section>"""
    return page("11/28 Gifts That Actually Get Used",
                "SL: Gifts They'll Use Every Single Day · PH: Still time to shop 30% off sitewide. Top banner L02; hero: photo on top + light panel (ref Burt's Bees) with L21 seal; bundles as one-card rows with description inside, light/deep alternating (ref Burt's Bees).",
                [header(), topbar('30% Off Sitewide, Still Going'), hero, band, footer()])


def e07():
    hero = f"""<section data-slice="hero" style="height:540px;overflow:hidden;background:radial-gradient(120% 80% at 50% 0%,#0CAB97 0%,#05453D 72%)">
  <div class="abs nk" style="left:0;width:600px;top:40px;text-align:center;font-weight:600;font-size:260px;line-height:.8;letter-spacing:-.05em;color:rgba(255,255,255,.08)">30%</div>
  <div class="stack" style="left:30px;width:540px;top:62px;color:#fff">
    <div class="kick rb">Your Shelf Will Thank You Later</div>
    <div style="width:45.8px;height:2px;border-radius:36px;background:#fff;margin-top:-10px"></div>
    <h1 class="h1 nk" style="font-size:76.4px;letter-spacing:-.05em;width:540px">Last full day<br>at 30% off</h1>
    <p class="body nk" style="width:440px">This is it, your last full day to enjoy 30% off sitewide. The best price of the year. Tomorrow it's gone.</p>
    {btn("Shop 30% Off Before It's Gone", 'white')}
  </div>
  {wave('#FFFFFF')}
</section>"""
    band = f"""<section class="band" style="background:var(--panel);padding-top:40px">
  {hgroup('Stock up smart', 'Why restock one thing when you can restock everything? Bundles pair your favorites together so you save more and shop less.', 'light-t', 420, 460)}
  {grid([pcard(n, i, wide=True, mult=True) for n, i, _ in BUNDLES])}
  <div data-slice="cta">{btn('Last Chance 30% Off', 'dark')}</div>
</section>"""
    return page('11/30 Last Full Day',
                "SL: Final Hours To Save 30% Sitewide · PH: Your last chance to stock up. Hero L03m (ghost price, product trio on a dome); bundles grid 2x3.",
                [header(), hero, band, footer()])


def dial():
    ticks = ''.join(
        f'<line x1="180" y1="{14 if i % 3 == 0 else 20}" x2="180" y2="34" stroke="#CCFFFA" stroke-width="{4 if i % 3 == 0 else 2}" stroke-linecap="round" transform="rotate({i * 30} 180 180)"/>'
        for i in range(12))
    return (f'<svg class="abs" style="left:120px;top:58px;z-index:2" width="360" height="360" viewBox="0 0 360 360">'
            f'<circle cx="180" cy="180" r="172" fill="rgba(255,255,255,.06)" stroke="#CCFFFA" stroke-width="3"/>{ticks}'
            f'</svg>')


def e08():
    cards = []
    for i, (name, img, _) in enumerate(BUNDLES[:4]):
        cards.append(wcard(name, img, rev=i % 2 == 1, mult=True))
    hero = f"""<section data-slice="hero" style="height:790px;overflow:hidden;background:linear-gradient(180deg,#008D83 0%,#05453D 75%)">
  {dial()}
  <div class="stack" style="left:150px;width:300px;top:186px;color:#fff">
    <h1 class="h1 nk" style="font-size:46px;letter-spacing:-.03em;width:300px">One final chance at 30% off</h1>
  </div>
  <div class="stack" style="left:69.5px;width:461px;top:458px;color:#fff">
    <div class="ruled rb">The Clock Runs Out At Midnight</div>
    <p class="body nk" style="width:461px">We weren't planning on this, but here we are. 30% off sitewide has been extended for exactly 24 more hours. Midnight ET tonight is the real, actual, no-more-extensions deadline.</p>
    {btn('Shop 30% Off, Final Hours', 'white')}
  </div>
  {wave('#FFFFFF')}
</section>"""
    band = f"""<section class="band" style="background:var(--panel);padding-top:40px">
  {hgroup('Stock up smart', 'Bundles are still the smartest way to stock up. Pair your favorites together at 30% off and skip restocking until spring. After midnight, the full price is back.', 'light-t', 420, 470)}
  <div style="display:flex;flex-direction:column;gap:15px">{''.join(cards)}</div>
  <div data-slice="cta">{btn('Last Chance', 'dark')}</div>
</section>"""
    return page('12/1 Extended 24 Hours',
                'SL: Surprise! 30% Off Extended 24h · PH: Final hours, we mean it. Top banner L02; hero with clock dial (type-led); 4 bundles as L09 wide cards, alternating.',
                [header(), topbar('Final Chance Right Now!', '#05453D'), hero, band, footer()])


EMAILS = {
    '01-rooted-in-nature-a': lambda: e01('a'),
    '01-rooted-in-nature-b': lambda: e01('b'),
    '01-rooted-in-nature-c': lambda: e01('c'),
    '02-the-deo-that-actually-works': e02,
    '03-gifts-for-the-people-at-your-table': e03,
    '04-something-is-coming': e04,
    '05-bfcm-announcement': e05,
    '06-gifts-that-actually-get-used': e06,
    '07-last-full-day': e07,
    '08-extended-24-hours': e08,
}


def main(only):
    for slug, fn in EMAILS.items():
        if only and not any(slug.startswith(o) for o in only): continue
        p = os.path.join(HERE, slug + '.html')
        open(p, 'w', encoding='utf-8').write(fn())
        print(p)


if __name__ == '__main__':
    main(sys.argv[1:])
