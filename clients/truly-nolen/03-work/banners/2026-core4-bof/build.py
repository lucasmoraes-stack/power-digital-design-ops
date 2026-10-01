"""Truly Nolen, 2026 Core-4 BOF iteration ($50 OFF spotlight).

Builds every piece of the brief from one layout table:
  2 copy variants (V1 Rodents, V2 Bugs) x 7 sizes (2 Meta + 5 programmatic)
  x 2 iterations (Static, MOBITE/HTML5) = 28 deliverables.
  Static ships as PNG. MOBITE/HTML5 ships as a 3-scene storyboard per size
  (no video, no animated build, per the owner).

  python build.py                       -> HTML for every static piece and frame
  python build.py --png                 -> renders all of them to PNG (headless Chrome)
  python build.py --png --static-only   -> only the 14 statics
  python build.py --figma               -> clean HTML per static and per scene, for Figma import

Design system source: Figma Progressive-Global LAB, node 216:656 (delivered TN pieces).
Fonts are read from the local Windows font folder and embedded as subset WOFF.
"""
import base64, io, math, os, subprocess, sys
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
BRAND = HERE.parents[2]                      # clients/truly-nolen
OUT = BRAND / "04-deliverables" / "banners" / "2026-core4-bof"
BUILD = HERE / "_build"                      # HTML intermediates (embed licensed fonts): gitignored
FONT_DIR = Path(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts"))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ---- brand tokens (measured in Figma 216:656) ---------------------------------
YELLOW, RED, BLACK, WHITE = "#FFE300", "#ED2524", "#000000", "#FFFFFF"

# ---- copy (verbatim from the brief) ------------------------------------------
COPY = {
    "V1": dict(slug="V1-Rodents", pest="rat", stack=["Off", "Rodent", "Control"],
               sub="Rodents can\u2019t hide from us", cta="Book an inspection"),
    "V2": dict(slug="V2-Bugs", pest="roach", stack=["Off", "Pest", "Control"],
               sub="Rodents can\u2019t hide from us", cta="Book an inspection"),
}

# ---- layout table -------------------------------------------------------------
# offer: x,y,u (u = font-size of "50"), c = centered on x
# disc: cx,cy,r   src: pivot of the beam (off-canvas)   hz: floor line
# pest: cx, w (floor = hz)   logo: x,y,h (c = centered)
# search: where the pool sits in storyboard scene 1 (dx, dy), clear of the pest
SIZES = {
    "1080x1080": dict(search=(-720, 0), W=1080, H=1080, platform="Meta", ratio="1x1",
        logo=dict(x=64, y=878, h=150), offer=dict(x=64, y=76, u=430),
        sub=dict(x=64, y=448, fs=46), cta=dict(x=64, y=540, fs=40),
        disc=dict(cx=800, cy=960, r=430), src=(1180, -380), hz=1004, pest=dict(cx=790, w=520)),
    "1080x1920": dict(search=(-200, -700), W=1080, H=1920, platform="Meta", ratio="9x16",
        logo=dict(x=540, y=264, h=170, c=1), offer=dict(x=540, y=500, u=400, c=1),
        sub=dict(x=540, y=852, fs=50, c=1), cta=dict(x=540, y=952, fs=44, c=1),
        disc=dict(cx=560, cy=1600, r=520), src=(1460, 660), hz=1660, pest=dict(cx=560, w=560)),
    "300x600": dict(search=(-60, -240), W=300, H=600, platform="Programmatic",
        logo=dict(x=150, y=14, h=66, c=1), offer=dict(x=150, y=100, u=118, c=1),
        sub=dict(x=150, y=206, fs=17, c=1), cta=dict(x=150, y=242, fs=14, c=1),
        disc=dict(cx=156, cy=486, r=166), src=(380, 170), hz=516, pest=dict(cx=154, w=220)),
    "300x250": dict(search=(-180, 0), W=300, H=250, platform="Programmatic",
        logo=dict(x=14, y=178, h=58), offer=dict(x=14, y=16, u=100),
        sub=dict(x=14, y=104, fs=13), cta=dict(x=14, y=130, fs=11),
        disc=dict(cx=230, cy=226, r=94), src=(330, -60), hz=240, pest=dict(cx=226, w=136)),
    "1600x600": dict(search=(-560, 0), W=1600, H=600, platform="Programmatic",
        logo=dict(x=1470, y=32, h=124), offer=dict(x=80, y=84, u=300),
        sub=dict(x=80, y=354, fs=42), cta=dict(x=80, y=438, fs=34),
        disc=dict(cx=1080, cy=440, r=330), src=(1700, -320), hz=520, pest=dict(cx=1080, w=400)),
    "728x90": dict(search=(-140, 0), W=728, H=90, platform="Programmatic",
        logo=dict(x=12, y=6, h=78), offer=dict(x=86, y=16, u=82),
        sub=None, cta=dict(x=548, y=29, fs=13),
        disc=dict(cx=442, cy=58, r=72), src=(620, -260), hz=74, pest=dict(cx=440, w=104)),
    "320x50": dict(search=(-56, 0), W=320, H=50, platform="Programmatic",
        logo=dict(x=6, y=4, h=42), offer=dict(x=46, y=11, u=40),
        sub=None, cta=dict(x=222, y=14, fs=8, pad=.75),
        disc=dict(cx=194, cy=34, r=26), src=(260, -120), hz=42, pest=dict(cx=193, w=44)),
}

# ---- pest silhouettes (side view, facing left, floor at y=182, 490x190) ------
PESTS = {
    "rat": """
<path d="M22 150C30 140 48 128 70 120C88 100 112 88 140 86C170 70 215 62 255 70C300 78 336 108 344 146C348 166 336 180 312 182L140 182C110 178 88 172 70 166C52 162 32 158 22 150Z"/>
<ellipse cx="120" cy="90" rx="25" ry="31" transform="rotate(-22 120 90)"/>
<path d="M336 150C370 166 392 176 420 175C450 174 470 160 480 138C476 166 454 186 420 187C388 188 358 178 330 170Z"/>
<path d="M84 160L94 184L116 184L106 164Z"/>
<path d="M262 158C280 168 292 176 296 184L324 184C314 170 300 160 288 152Z"/>
<g fill="none" stroke="#000" stroke-width="2.6" stroke-linecap="round"><path d="M34 146L2 134"/><path d="M34 150L0 152"/><path d="M36 154L6 168"/></g>""",
    "roach": """
<path d="M130 140C150 92 230 76 305 80C385 84 440 108 462 138C446 152 400 156 330 156L180 156C152 156 132 152 130 140Z"/>
<path d="M96 142C98 112 124 100 150 106C164 120 164 144 152 156C128 160 104 156 96 142Z"/>
<ellipse cx="88" cy="150" rx="17" ry="14"/>
<g fill="none" stroke="#000" stroke-linecap="round" stroke-linejoin="round">
<path stroke-width="3.6" d="M84 142C64 104 46 56 14 10"/><path stroke-width="3.6" d="M80 146C52 124 26 100 2 86"/>
<path stroke-width="8" d="M156 150L130 166L112 184"/><path stroke-width="7" d="M170 152L162 170L150 184"/>
<path stroke-width="8" d="M236 154L222 170L200 184"/><path stroke-width="7" d="M254 155L262 170L276 184"/>
<path stroke-width="8" d="M322 154L356 168L404 184"/><path stroke-width="7" d="M304 155L318 172L340 184"/>
<path stroke-width="3.4" d="M458 138L482 130"/><path stroke-width="3.4" d="M456 146L482 148"/></g>""",
}
PEST_VB = (490, 190, 182)   # viewBox w, h, floor y

# ---- fonts --------------------------------------------------------------------
FONTS = [("TN Display", "FuturaDisplayBQ.otf"), ("TN Medium", "FuturaStd-Medium.otf"),
         ("TN Heavy", "FuturaStd-Heavy.otf")]
BASIC = "".join(chr(c) for c in range(32, 127)) + "\u2019\u2018\u201c\u201d\u00b7\u00d7\u2192\u00b0"

# Figma export: real family names and weights, so imported text layers map to the local fonts
FIGMA_FONTS = {"TN Display": ("Futura Display BQ", 400), "TN Medium": ("Futura Std", 500), "TN Heavy": ("Futura Std", 650)}

def font_face(text, figma=False):
    css = []
    for fam, fn in FONTS:
        f = TTFont(FONT_DIR / fn)
        opts = subset.Options(); opts.flavor = "woff"; opts.layout_features = ["kern", "liga"]
        s = subset.Subsetter(opts); s.populate(text=text); s.subset(f)
        buf = io.BytesIO(); f.flavor = "woff"; f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        fam, wt = FIGMA_FONTS[fam] if figma else (fam, 400)
        css.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};src:url(data:font/woff;base64,{b64}) format('woff');font-display:block}}")
    return "\n".join(css)

LOGO_PNG = BRAND / "01-brand" / "identity" / "assets" / "tn-logo-sticker.png"
def logo_uri():
    return "data:image/png;base64," + base64.b64encode(LOGO_PNG.read_bytes()).decode()
LOGO_RATIO = 522 / 654

# ---- piece CSS (shared by standalone files and review pages) -----------------
# Display font metrics: cap .706, ascent .935, descent .25 -> with line-height 1em
# the cap top sits .1365em below the line box top.
PIECE_CSS = """
.tn{position:relative;overflow:hidden;background:#000;color:#fff;font-family:'TN Medium',Futura,'Century Gothic',sans-serif}
.tn *{box-sizing:border-box}
.tn .scene{position:absolute;inset:0;display:block}
.tn .offer{position:absolute;display:flex;align-items:flex-start;font-family:'TN Display','Arial Black',sans-serif;text-transform:uppercase;color:#FFE300;white-space:nowrap}
.tn .offer.c{transform:translateX(-50%)}
.tn .cap{display:block;height:.706em;line-height:1em}
.tn .cap>i{display:block;font-style:normal;transform:translateY(-.1365em)}
.tn .dol{font-size:.42em;margin-right:.03em}
.tn .num{font-size:1em;letter-spacing:-.02em}
.tn .stk{display:flex;flex-direction:column;justify-content:space-between;height:.706em;margin-left:.06em;font-size:1em}
.tn .stk .cap{font-size:.2976em;letter-spacing:-.005em}
.tn .stk .w{color:#fff}
.tn .sub{position:absolute;font-family:'TN Medium',Futura,sans-serif;color:#fff;line-height:1.1;letter-spacing:-.01em;white-space:nowrap}
.tn .sub.wrap{white-space:normal}
.tn .sub.c,.tn .cta.c,.tn .logo.c{transform:translateX(-50%)}
.tn .cta{position:absolute;display:flex;align-items:center;justify-content:center;height:2.4em;padding:0 var(--pad,1.6em);border-radius:999px;background:#FFE300;color:#000;font-family:'TN Heavy',Futura,sans-serif;letter-spacing:-.01em;white-space:nowrap;text-decoration:none}
.tn .cta>i{font-style:normal;transform:translateY(.05em)}
.tn .logo{position:absolute;display:block}
/* storyboard frames: elements not yet on screen */
.tn .off{visibility:hidden}
.tn .startle{transform-box:fill-box;transform-origin:50% 100%}
.tn .caught .startle{transform:translateY(-6%) scaleY(1.04)}
"""

def cone_points(sx, sy, cx, cy, r):
    dx, dy = cx - sx, cy - sy
    d = math.hypot(dx, dy); a = math.atan2(dy, dx); t = math.asin(min(.999, r / d))
    L = math.sqrt(max(d * d - r * r, 1))
    return [(sx + L * math.cos(a + s * t), sy + L * math.sin(a + s * t)) for s in (-1, 1)]

def scene_svg(cfg, pest, uid, shift=(0, 0)):
    W, H = cfg["W"], cfg["H"]; d = cfg["disc"]; sx, sy = cfg["src"]; hz = cfg["hz"]
    cx, cy, r = d["cx"] + shift[0], d["cy"] + shift[1], d["r"]
    (x1, y1), (x2, y2) = cone_points(sx, sy, cx, cy, r)
    pw = cfg["pest"]["w"]; vw, vh, fy = PEST_VB; s = pw / vw
    px, py = cfg["pest"]["cx"] - pw / 2, hz - fy * s
    shadow_w = pw * .56
    return f"""<svg class="scene" viewBox="0 0 {W} {H}" width="{W}" height="{H}" aria-hidden="true">
<defs>
<radialGradient id="d{uid}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#FFF38A"/><stop offset=".55" stop-color="{YELLOW}"/><stop offset=".93" stop-color="{YELLOW}"/><stop offset="1" stop-color="{YELLOW}" stop-opacity="0"/></radialGradient>
<radialGradient id="h{uid}" cx="{cx}" cy="{cy}" r="{r*1.22:.1f}" gradientUnits="userSpaceOnUse">
<stop offset=".7" stop-color="{YELLOW}" stop-opacity=".22"/><stop offset="1" stop-color="{YELLOW}" stop-opacity="0"/></radialGradient>
<linearGradient id="c{uid}" x1="{sx}" y1="{sy}" x2="{cx}" y2="{cy}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="{YELLOW}" stop-opacity="0"/><stop offset="1" stop-color="{YELLOW}" stop-opacity=".26"/></linearGradient>
</defs>
<g class="beam"><g class="light">
<polygon points="{sx},{sy} {x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f}" fill="url(#c{uid})"/>
<circle cx="{cx}" cy="{cy}" r="{r*1.22:.1f}" fill="url(#h{uid})"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#d{uid})"/></g></g>
<rect x="0" y="{hz}" width="{W}" height="{H-hz}" fill="#000" fill-opacity=".13"/>
<ellipse cx="{cfg['pest']['cx']}" cy="{hz+pw*.012:.1f}" rx="{shadow_w/2:.1f}" ry="{pw*.035:.1f}" fill="#000" fill-opacity=".28"/>
<g transform="translate({px:.1f} {py:.1f}) scale({s:.4f})"><g class="startle">{PESTS[pest]}</g></g>
</svg>"""

# ---- storyboard (MOBITE / HTML5 iterations): the sweep, frame by frame -----
# Each scene is a state of the same layout. Scene 03 is the static end frame.
ALL = {"dol", "num", "stack", "sub", "cta", "logo"}
FRAMES = [
    dict(id="01", title="Busca", note="Tudo escuro. O holofote varre o quadro procurando.", beam="search", show=set()),
    dict(id="02", title="Pegou", note="O feixe para em cima da praga e o $50 OFF entra.", beam="0", show={"dol", "num", "stack"}, caught=True),
    dict(id="03", title="Quadro final", note="Entram subhead, CTA e logo. Igual ao estático.", beam="0", show=ALL),
]
def piece_html(size, var, logo_src, frame=None, uid_extra="", cfg=None):
    """frame=None -> static final piece; otherwise a storyboard state from FRAMES.
    Elements a scene has not brought in yet are left out of the markup."""
    cfg = cfg or SIZES[size]; cp = COPY[var]; W, H = cfg["W"], cfg["H"]
    show = frame["show"] if frame else ALL
    on = lambda k, html: html if k in show else ""
    hide = lambda k: ""
    uid = f"{var}{size}{frame['id'] if frame else 's'}{uid_extra}".replace("x", "_")
    o = cfg["offer"]; c = " c" if o.get("c") else ""
    stack = "".join(f'<span class="cap{" w" if i else ""}"><i>{t}</i></span>' for i, t in enumerate(cp["stack"]))
    offer = (f'<div class="offer{c}" style="left:{o["x"]}px;top:{o["y"]}px;font-size:{o["u"]}px">'
             + on("dol", '<span class="cap dol"><i>$</i></span>') + on("num", '<span class="cap num"><i>50</i></span>')
             + on("stack", f'<span class="stk">{stack}</span>') + '</div>')
    if not show & {"dol", "num", "stack"}:
        offer = ""
    sub = ""
    if cfg["sub"]:
        s = cfg["sub"]; cls = ("sub c" if s.get("c") else "sub") + (" wrap" if s.get("w") else "")
        wd = f"width:{s['w']}px;" if s.get("w") else ""
        sub = f'<div class="{cls}{hide("sub")}" style="left:{s["x"]}px;top:{s["y"]}px;font-size:{s["fs"]}px;{wd}">{cp["sub"]}</div>'
    t = cfg["cta"]; pad = f"--pad:{t['pad']}em;" if t.get("pad") else ""
    cta = (f'<span class="cta{" c" if t.get("c") else ""}{hide("cta")}" style="left:{t["x"]}px;top:{t["y"]}px;font-size:{t["fs"]}px;{pad}">'
           f'<i>{cp["cta"]}</i></span>')
    lg = cfg["logo"]
    logo = (f'<img class="logo{" c" if lg.get("c") else ""}{hide("logo")}" src="{logo_src}" alt="Truly Nolen" '
            f'style="left:{lg["x"]}px;top:{lg["y"]}px;height:{lg["h"]}px;width:{lg["h"]*LOGO_RATIO:.1f}px">')
    shift = cfg["search"] if frame and frame["beam"] == "search" else (0, 0)
    caught = " caught" if frame and frame.get("caught") else ""
    sub, cta, logo = on("sub", sub), on("cta", cta), on("logo", logo)
    return (f'<div class="tn{caught}" style="width:{W}px;height:{H}px">'
            f'{scene_svg(cfg, cp["pest"], uid, shift)}{offer}{sub}{cta}{logo}</div>')

def name(size, var, fmt="Static"):
    cfg = SIZES[size]; cp = COPY[var]
    if fmt != "Static":
        fmt = "MOBITE" if cfg["platform"] == "Meta" else "HTML5"
    return f"TN-BOF-Core4-{cp['slug']}-{fmt}-{cfg['platform']}-{cfg.get('ratio', size)}"

def needed_text():
    t = set("$50 ")
    for cp in COPY.values():
        t |= set("".join(cp["stack"]).upper() + "".join(cp["stack"]) + cp["sub"] + cp["cta"])
    return "".join(sorted(t))

def standalone(size, var, fonts_css, frame=None, title=None):
    cfg = SIZES[size]; W, H = cfg["W"], cfg["H"]
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{title or name(size, var)}</title>
<style>{fonts_css}
html,body{{margin:0;padding:0;background:#000;width:{W}px;height:{H}px;overflow:hidden}}
{PIECE_CSS}</style></head><body>
{piece_html(size, var, logo_uri(), frame)}
</body></html>"""

# ---- build --------------------------------------------------------------------
def build():
    fonts_small = font_face(needed_text())
    files = []   # (size, var, frame, html path)
    for var in COPY:
        for size in SIZES:
            d = BUILD / "static"; d.mkdir(parents=True, exist_ok=True)
            p = d / f"{name(size, var)}.html"
            p.write_text(standalone(size, var, fonts_small), encoding="utf-8")
            files.append((size, var, None, p))
            sb = BUILD / "storyboard" / name(size, var, "anim"); sb.mkdir(parents=True, exist_ok=True)
            for fr in FRAMES:
                p = sb / f"frame-{fr['id']}.html"
                p.write_text(standalone(size, var, fonts_small, fr, f"{name(size, var, 'anim')} frame {fr['id']}"), encoding="utf-8")
                files.append((size, var, fr, p))
    return files

def chrome_png(html, png, W, H, scale=1):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", f"--window-size={W},{H}",
                    "--virtual-time-budget=3000", f"--screenshot={png}", html.as_uri()],
                   check=True, capture_output=True)

def render_pngs(files, only_static=False):
    for size, var, fr, p in files:
        if only_static and fr:
            continue
        cfg = SIZES[size]
        png = OUT / p.relative_to(BUILD).with_suffix(".png"); png.parent.mkdir(parents=True, exist_ok=True)
        # Meta pieces are laid out at 1080 and exported at 1440, like the delivered TN pieces
        chrome_png(p, png, cfg["W"], cfg["H"], 1440 / 1080 if cfg["platform"] == "Meta" else 1)
        print("png", png.relative_to(OUT))

# ---- Figma export --------------------------------------------------------------
# Same pieces as the PNGs, as clean HTML for an HTML-to-Figma import:
# real font names, Meta laid out natively at 1440, one file per static and per scene.
def scale_cfg(cfg, k):
    def sc(key, v):
        if key in ("c", "pad", "platform", "ratio"):
            return v
        if isinstance(v, dict):
            return {kk: sc(kk, vv) for kk, vv in v.items()}
        if isinstance(v, tuple):
            return tuple(round(x * k, 2) for x in v)
        if isinstance(v, (int, float)):
            return round(v * k, 2)
        return v
    out = {key: sc(key, v) for key, v in cfg.items()}
    out["W"], out["H"] = round(cfg["W"] * k), round(cfg["H"] * k)
    return out

FIGMA_CSS = (".tn,.tn .sub{font-weight:500}.tn .offer{font-weight:400}.tn .cta{font-weight:650}")

def figma_html(size, var, fonts_css, frame=None):
    cfg = SIZES[size]
    if cfg["platform"] == "Meta":
        cfg = scale_cfg(cfg, 1440 / 1080)
    W, H = cfg["W"], cfg["H"]
    css = PIECE_CSS
    for tn, (fam, _) in FIGMA_FONTS.items():
        css = css.replace(f"'{tn}'", f"'{fam}'")
    title = figma_name(size, var, frame)
    return title, f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<style>{fonts_css}
html,body{{margin:0;padding:0;background:#000;width:{W}px;height:{H}px;overflow:hidden}}
{css}{FIGMA_CSS}</style></head><body>
{piece_html(size, var, logo_uri(), frame, cfg=cfg)}
<script>{FLATTEN_JS}</script>
</body></html>"""

def figma_name(size, var, frame=None):
    """Figma frame name, patterned on the delivered TN26020 pieces:
    TN-Core4BOF-{dim}-SpotlightOffer-{Static|Mobite|HTML5}-{Meta|Programmatic}-V{n}-{Rodents|Bugs}[-S0n]"""
    cfg = SIZES[size]; v, pest = COPY[var]["slug"].split("-")
    fmt = "Static" if not frame else ("Mobite" if cfg["platform"] == "Meta" else "HTML5")
    out = f"TN-Core4BOF-{cfg.get('ratio', size)}-SpotlightOffer-{fmt}-{cfg['platform']}-{v}-{pest}"
    return out + (f"-S{frame['id']}" if frame else "")

# HTML-to-Figma importers drop the cap-crop transforms and re-wrap text boxes that are
# measured to the pixel (CONTROL broke into CONT/ROL). Before export, every headline
# line and the subhead are re-laid as absolute, no-wrap text at the position the
# browser measured, with a little spare width so Figma never wraps them.
FLATTEN_JS = """
document.fonts.ready.then(function(){
var tn=document.querySelector('.tn'),R=tn.getBoundingClientRect(),out=[];
function add(el,box,txt,center){var cs=getComputedStyle(el),rg=document.createRange();rg.selectNodeContents(el);
 var t=rg.getBoundingClientRect(),w=Math.ceil(t.width*1.15+4),x=t.left-R.left-(center?(w-t.width)/2:0);
 out.push({txt:txt,x:x,y:box.top-R.top,w:w,center:center,cs:cs});}
tn.querySelectorAll('.offer .cap>i').forEach(function(i){add(i,i.getBoundingClientRect(),i.textContent,false)});
var sub=tn.querySelector('.sub');
if(sub)add(sub,sub.getBoundingClientRect(),sub.textContent,sub.classList.contains('c'));
out.forEach(function(o){var d=document.createElement('div'),cs=o.cs;d.textContent=o.txt;
 d.style.cssText='position:absolute;margin:0;white-space:nowrap;left:'+o.x.toFixed(2)+'px;top:'+o.y.toFixed(2)+'px;width:'+o.w+'px;'+
 'font-family:'+cs.fontFamily+';font-weight:'+cs.fontWeight+';font-size:'+cs.fontSize+';line-height:'+cs.lineHeight+';'+
 'letter-spacing:'+cs.letterSpacing+';color:'+cs.color+';text-transform:'+cs.textTransform+';text-align:'+(o.center?'center':'left');
 tn.insertBefore(d,tn.querySelector('.cta'));});
var of=tn.querySelector('.offer');if(of)of.remove();if(sub)sub.remove();
document.documentElement.setAttribute('data-flat','1');
});
"""

def bake(p, cfg):
    """Runs FLATTEN_JS in headless Chrome and saves the resulting static DOM, so any
    importer (html.to.design, Figma capture) reads plain absolute text."""
    k = 1440 / 1080 if cfg["platform"] == "Meta" else 1
    W, H = round(cfg["W"] * k), round(cfg["H"] * k)
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--window-size={W},{H}",
                          "--virtual-time-budget=3000", "--dump-dom", p.as_uri()],
                         check=True, capture_output=True, text=True, encoding="utf-8").stdout
    assert 'data-flat="1"' in dom, f"flatten did not run: {p.name}"
    dom = dom.replace(f"<script>{FLATTEN_JS}</script>", "")
    p.write_text("<!doctype html>" + dom, encoding="utf-8")

def export_figma():
    fonts = font_face(needed_text(), figma=True)
    root = OUT / "html"
    for old in root.glob("*/*.html"):
        old.unlink()
    (root / "static").mkdir(parents=True, exist_ok=True); (root / "storyboard").mkdir(parents=True, exist_ok=True)
    (root / ".gitignore").write_text("# embeds licensed fonts: keep local, never commit\n*\n", encoding="utf-8")
    n = 0
    for var in COPY:
        for size in SIZES:
            for fr in [None] + FRAMES:
                title, html = figma_html(size, var, fonts, fr)
                p = root / ("storyboard" if fr else "static") / f"{title}.html"
                p.write_text(html, encoding="utf-8")
                bake(p, SIZES[size])
                n += 1
    print(f"{n} Figma HTML files in {root}")
    return root

if __name__ == "__main__":
    if "--figma" in sys.argv:
        export_figma(); sys.exit()
    files = build()
    print(f"{len(files)} files written to {BUILD}")
    if "--png" in sys.argv:
        render_pngs(files, only_static="--static-only" in sys.argv)
