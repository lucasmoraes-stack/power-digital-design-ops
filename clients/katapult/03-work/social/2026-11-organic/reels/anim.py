"""Katapult November 2026 organic: the two Reels (1080x1920, 30 fps, silent), built in code.

One HyperFrames composition per video, driven by a deterministic seek(t) (common.js + t07.js / t15.js).
Pipeline copied from RKU26012 (clients/roku/03-work/ads/2026-rku26012-tv-ads-3-steps).

    python anim.py                -> hf/compositions/07.html, 15.html (+ hf/assets)
    python render.py stills 07 15 -> review/<id>-t<sec>.png + review/_sheet-<id>.jpg
    python render.py video 07 15  -> 04-deliverables/social/2026-11-organic/reels/*.mp4 + poster .png

07 Katapult at checkout (15 s)            15 Cyber Monday finds (10.8 s)
  0.0  cover: headline + products           0.0  logo + headline, cart docked, bag disc
  2.5  wipe to step 1, phone in             1.25 disc to badge; 1.6 product 1, every 1.3 s:
  4.2  tap Katapult, 5.1 tap Continue            shape swipes off, cutout shrinks into the next slot
  5.35 step 2: mobile number + code         8.5 check, 8.55 headline to centre, 9.0 logo top
  9.0  step 3: review, 10.5 Place order    10.8 end
 12.0  wipe to end card + logo; 15.0 end

Look: October finals (Figma "kat os"): sentence-case Regular headlines with one Pink word, White
rounded cards on a solid offset plate, line icons in Pink discs, cutouts on flat palette shapes,
one thick Pink line that turns a rounded corner and runs on as dots. No gradients, shadows or blur.
"""
import json
import math
import re
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
KAT = HERE.parents[3]                                   # clients/katapult
IDENT = KAT / "01-brand" / "identity"
PRODUCTS = KAT / "03-work" / "claude-project-social" / "studio" / "assets" / "products"
HF = HERE / "hf"
BUILD = HF / "compositions"
W, H, FPS = 1080, 1920, 30
SAFE = {"top": 250, "bottom": 340, "side": 90}         # Reels UI-safe area
VIDEOS = {"07": {"dur": 15.0, "slug": "07-katapult-at-checkout"}, "15": {"dur": 10.8, "slug": "15-cyber-monday"}}

PINK, LOGO_PINK, DBLUE, BLUE, LBLUE = "#ED5370", "#EC5370", "#131540", "#365488", "#9EB5C0"
ORANGE, CREAM, SURFACE, WHITE = "#E48027", "#D4A574", "#EAEAE8", "#FFFFFF"
GREY_L, GREY_XL, GREY_M = "#D8D8D8", "#F0F0F0", "#A4A4A4"

# line icons (stroke = currentColor)
def _ic(d, sw=2):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'
ICON = {
    "card": _ic('<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 9.5h19M6 15h4"/>'),
    "bank": _ic('<path d="M3 9.5 12 4l9 5.5M4.5 10v8M9.5 10v8M14.5 10v8M19.5 10v8M3 20h18"/>'),
    "phone": _ic('<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>'),
    "check": _ic('<path d="m5 12.5 4.5 4.5L19 7.5"/>', 3),
    "chev": _ic('<path d="m14.5 5-7 7 7 7"/>', 2.6),
    "lock": _ic('<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8.5 10.5V7.5a3.5 3.5 0 0 1 7 0v3"/>'),
    "bag": _ic('<path d="M5 8h14l-1 12.5H6z"/><path d="M9 10.5V7a3 3 0 0 1 6 0v3.5"/>'),
}


def logo(color, id_, width, left=0, top=0):
    """Katapult wordmark from the supplied artwork, recolored (Pink, Dark Blue or White only)."""
    svg = (IDENT / "logo-katapuklt.svg").read_text(encoding="utf8")
    paths = re.findall(r"<path [^>]*/>", svg)
    paths = [re.sub(r'fill="[^"]*"', f'fill="{color}"', p) for p in paths]
    return (f'<svg id="{id_}" class="logo" viewBox="0 0 521 116" style="left:{left}px;top:{top}px;width:{width}px;height:{width * 116 / 521:.1f}px">'
            + "".join(paths) + "</svg>")


def accent(id_, edge, corner, end, r=110, sw=18, dots=6, gap=53, dr=10):
    """Pink line from a frame edge to a rounded corner, then on to `end`; dots continue past `end`.
    Points are stage px. Segments must be axis-aligned (edge->corner, corner->end)."""
    (ex, ey), (cx, cy), (sx, sy) = edge, corner, end
    d1 = (math.copysign(1, cx - ex) if cx != ex else 0, math.copysign(1, cy - ey) if cy != ey else 0)
    d2 = (math.copysign(1, sx - cx) if sx != cx else 0, math.copysign(1, sy - cy) if sy != cy else 0)
    a = (cx - d1[0] * r, cy - d1[1] * r)
    b = (cx + d2[0] * r, cy + d2[1] * r)
    sweep = 1 if d1[0] * d2[1] - d1[1] * d2[0] > 0 else 0
    path = f"M{ex} {ey} L{a[0]} {a[1]} A{r} {r} 0 0 {sweep} {b[0]} {b[1]} L{sx} {sy}"
    length = abs(ex - cx) + abs(ey - cy) - 2 * r + math.pi * r / 2 + abs(sx - cx) + abs(sy - cy)
    circ = "".join(f'<circle id="{id_}-d{i}" data-r="{dr}" cx="{sx + d2[0] * gap * (i + 1)}" cy="{sy + d2[1] * gap * (i + 1)}" r="0" fill="{PINK}"/>'
                   for i in range(dots))
    return (f'<svg class="acc" id="{id_}" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<path id="{id_}-l" d="{path}" fill="none" stroke="{PINK}" stroke-width="{sw}" stroke-linecap="butt" '
            f'stroke-dasharray="{length:.1f}" stroke-dashoffset="{length:.1f}" data-len="{length:.1f}" data-n="{dots}"/>{circ}</svg>')


def font_face():
    return "\n".join(f'@font-face{{font-family:"Aktiv Grotesk";font-weight:{w};src:url("../assets/fonts/AktivGrotesk-{n}.otf") format("opentype")}}'
                     for w, n in [(400, "Regular"), (500, "Medium"), (700, "Bold")])


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#131540}
#st{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"Aktiv Grotesk",sans-serif;color:#131540;background:#EAEAE8;
  -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
.L{position:absolute;left:0;top:0;width:1080px;height:1920px}
.abs{position:absolute}
.acc{position:absolute;left:0;top:0;overflow:visible}
.logo{position:absolute;display:block}
.hl{position:absolute;font-weight:400;letter-spacing:-.015em;line-height:1.04}
.hl em{font-style:normal;color:#ED5370}
.hl span{display:block}
.shape{position:absolute;border-radius:56px}
.prod{position:absolute;display:block;object-fit:contain}
/* phone */
#phone{position:absolute;left:270px;top:600px;width:540px;height:1000px}
#phone .plate{position:absolute;left:26px;top:26px;width:540px;height:1000px;border-radius:78px;background:#ED5370}
#phone .body{position:absolute;left:0;top:0;width:540px;height:1000px;border-radius:78px;background:#131540}
#screen{position:absolute;left:18px;top:18px;width:504px;height:964px;border-radius:60px;background:#fff;overflow:hidden}
.notch{position:absolute;z-index:5;left:192px;top:16px;width:120px;height:32px;border-radius:16px;background:#131540}
.sb{position:absolute;z-index:5;top:26px;height:12px;border-radius:6px;background:#131540}
.scr{position:absolute;left:0;top:0;width:504px;height:964px}
.hd{position:absolute;left:24px;top:76px;display:flex;align-items:center;gap:14px;font-size:32px;font-weight:500;color:#131540}
.hd svg{width:34px;height:34px}
.row{position:absolute;left:28px;width:448px;height:112px}
.tile{position:absolute;left:0;top:0;width:112px;height:112px;border-radius:20px;background:#F0F0F0}
.tile img{position:absolute;left:10px;top:10px;width:92px;height:92px;object-fit:contain}
.bar{position:absolute;height:16px;border-radius:8px;background:#D8D8D8}
.bar.d{background:#131540}
.lab{position:absolute;left:28px;font-size:26px;font-weight:500;color:#4D4D4D}
.opt{position:absolute;left:28px;width:448px;height:84px;border-radius:20px;border:2px solid #D8D8D8;background:#fff}
.opt.sel{border:3px solid #ED5370;background:#FDEBEF}
.radio{position:absolute;left:22px;top:25px;width:30px;height:30px;border-radius:50%;border:3px solid #A4A4A4;background:#fff}
.opt.sel .radio{border-color:#ED5370}
.radio i{position:absolute;left:4px;top:4px;width:16px;height:16px;border-radius:50%;background:#ED5370}
.opt .oi{position:absolute;left:70px;top:23px;width:34px;height:34px;color:#131540}
.opt .ot{position:absolute;left:70px;top:22px;font-size:30px;font-weight:500;color:#131540}
.btn{position:absolute;left:28px;top:852px;width:448px;height:84px;border-radius:42px;background:#D8D8D8;color:#fff;
  display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:500}
.btn.on{background:#ED5370}
.btn svg{width:44px;height:44px}
.disc{position:absolute;border-radius:50%;background:#ED5370;color:#fff;display:flex;align-items:center;justify-content:center}
.fld{position:absolute;left:28px;width:448px;height:92px;border-radius:20px;border:2px solid #D8D8D8;background:#fff}
.fld.focus{border:3px solid #ED5370}
.dots{position:absolute;left:28px;top:0;height:100%;display:flex;align-items:center;gap:12px}
.dots i{width:14px;height:14px;border-radius:50%;background:#131540;flex:none}
.dots i.gap{width:6px;background:none}
.caret{position:absolute;top:26px;width:3px;height:40px;border-radius:2px;background:#ED5370}
.box{position:absolute;width:62px;height:80px;border-radius:16px;border:2px solid #D8D8D8;background:#fff}
.box.focus{border:3px solid #ED5370}
.box i{position:absolute;left:24px;top:33px;width:14px;height:14px;border-radius:50%;background:#131540}
.chk{position:absolute;width:38px;height:38px;border-radius:10px;border:3px solid #A4A4A4;background:#fff;color:#fff}
.chk.on{border-color:#ED5370;background:#ED5370}
.chk svg{position:absolute;left:3px;top:3px;width:26px;height:26px}
.sq{position:absolute;width:56px;height:40px;border-radius:12px;background:#D8D8D8}
.sq.p{background:#ED5370}
#touch{position:absolute;left:0;top:0;width:68px;height:68px;border-radius:50%;background:rgba(255,255,255,.75);border:5px solid #131540;z-index:30}
#ring{position:absolute;left:0;top:0;border-radius:50%;border:5px solid #ED5370;z-index:29}
.stepn{position:absolute;left:120px;top:262px;width:76px;height:76px;font-size:38px;font-weight:500}
.stepn span{position:absolute;left:0;top:0;width:76px;height:76px;display:flex;align-items:center;justify-content:center}
/* 15: full height. Headline 364-622, product shape 650-1290, cart card 1330-1564 (+16 plate) */
.cart{position:absolute;left:93px;top:1330px;width:894px;height:234px}
.cart .plate{position:absolute;left:16px;top:16px;width:894px;height:234px;border-radius:44px;background:#131540}
.cart .face{position:absolute;left:0;top:0;width:894px;height:234px;border-radius:44px;background:#fff}
.slot{position:absolute;top:52px;width:150px;height:150px;border-radius:28px;background:#F0F0F0;border:2px solid #D8D8D8}
.slot.on{background:#fff;border:3px solid #ED5370}
.pshape{position:absolute;left:220px;top:650px;width:640px;height:640px}
"""


def page(vid, body, script):
    v = VIDEOS[vid]
    cfg = {"comp": f"kat-reel-{vid}", "dur": v["dur"], "W": W, "H": H, "safe": SAFE, "p15": P15, "slot": SLOT}
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Katapult reel {vid}</title>
<style>{font_face()}{CSS}</style></head><body>
<div id="st" data-composition-id="kat-reel-{vid}" data-start="0" data-duration="{v['dur']}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
{body}
</div>
<script>const CFG={json.dumps(cfg)};</script>
<script src="../assets/gsap.min.js"></script>
<script src="../assets/common.js"></script>
<script src="../assets/{script}"></script>
</body></html>"""


def img(name, cls="prod", style="", id_=""):
    i = f' id="{id_}"' if id_ else ""
    return f'<img{i} class="{cls}" src="../assets/products/{name}.webp" style="{style}">'


# ---------------------------------------------------------------- 07 Katapult at checkout
def status_bar():
    return ('<div class="notch"></div><div class="sb" style="left:44px;width:58px"></div>'
            '<div class="sb" style="left:386px;width:22px;height:14px;top:25px;border-radius:3px"></div>'
            '<div class="sb" style="left:414px;width:40px;height:18px;top:23px;border-radius:5px;background:none;border:3px solid #131540"></div>'
            '<div class="sb" style="left:419px;width:24px;height:8px;top:28px;border-radius:2px"></div>')


def order_rows(prods, y0=150):
    out = ""
    for i, p in enumerate(prods):
        out += (f'<div class="row" style="top:{y0 + i * 140}px"><div class="tile">{img(p, cls="")}</div>'
                f'<div class="bar d" style="left:140px;top:30px;width:{220 - i * 40}px"></div>'
                f'<div class="bar" style="left:140px;top:66px;width:{150 + i * 30}px;height:14px"></div></div>')
    return out


def cluster(p):
    """Three cutouts on flat shapes, each centred on its shape at about 75 to 80% (box 840x680 from 120,870)."""
    return (f'<div class="shape" id="{p}s0" style="left:120px;top:870px;width:400px;height:400px;background:{LBLUE};transform:rotate(-5deg)"></div>'
            f'<div class="shape" id="{p}s1" style="left:560px;top:930px;width:400px;height:400px;border-radius:50%;background:{PINK}"></div>'
            f'<div class="shape" id="{p}s2" style="left:300px;top:1200px;width:340px;height:340px;background:{CREAM}"></div>'
            f'{img("couch", style="left:160px;top:910px;width:320px;height:320px", id_=p + "p0")}'
            f'{img("tv", style="left:610px;top:980px;width:300px;height:300px", id_=p + "p1")}'
            f'{img("washer", style="left:342px;top:1242px;width:256px;height:256px", id_=p + "p2")}')


def body07():
    prods = ["couch", "headphones"]
    # screen A: checkout + payment options
    scrA = (f'<div class="scr" id="scrA"><div class="hd">{ICON["chev"]}Checkout</div>{order_rows(prods)}'
            '<div class="abs" style="left:28px;top:420px;width:448px;height:2px;background:#F0F0F0"></div>'
            '<div class="lab" style="top:446px">Payment</div>'
            f'<div class="opt" id="o0" style="top:486px"><div class="radio"></div><div class="oi">{ICON["card"]}</div>'
            '<div class="bar" style="left:124px;top:33px;width:170px;height:14px"></div></div>'
            f'<div class="opt" id="o1" style="top:598px"><div class="radio"></div><div class="oi">{ICON["bank"]}</div>'
            '<div class="bar" style="left:124px;top:33px;width:130px;height:14px"></div></div>'
            '<div class="opt" id="o2" style="top:710px"><div class="radio"><i id="o2r"></i></div><div class="ot">Katapult</div></div>'
            '<div class="btn" id="bA">Continue</div></div>')
    # screen B: apply, mobile number + code
    dots = "".join('<i class="gap"></i>' * (i in (3, 6)) + f'<i id="md{i}"></i>' for i in range(10))
    boxes = "".join(f'<div class="box" id="cb{i}" style="left:{28 + i * 77.2:.1f}px;top:560px"><i id="cd{i}"></i></div>' for i in range(6))
    scrB = (f'<div class="scr" id="scrB"><div class="hd">{ICON["chev"]}</div>'
            f'<div class="disc" style="left:192px;top:120px;width:120px;height:120px"><div style="width:62px;height:62px">{ICON["phone"]}</div></div>'
            '<div class="lab" style="top:300px">Mobile number</div>'
            f'<div class="fld" id="fM" style="top:344px"><div class="dots">{dots}</div><div class="caret" id="cM"></div></div>'
            '<div class="lab" style="top:514px">Code</div>'
            f'<div class="disc" id="vok" style="left:420px;top:500px;width:56px;height:56px"><div style="width:32px;height:32px">{ICON["check"]}</div></div>'
            f'{boxes}<div class="abs" style="left:28px;top:700px;width:34px;height:34px;color:#131540">{ICON["lock"]}</div>'
            '<div class="bar" style="left:80px;top:702px;width:330px;height:14px"></div>'
            '<div class="bar" style="left:80px;top:728px;width:220px;height:14px"></div>'
            '<div class="btn" id="bB">Continue</div></div>')
    # screen C: review + submit, then success
    sqs = "".join(f'<div class="sq" id="sq{i}" style="left:{24 + i * 68}px;top:76px"></div>' for i in range(6))
    scrC = (f'<div class="scr" id="scrC"><div class="hd">{ICON["chev"]}Review order</div>{order_rows(prods)}'
            '<div class="abs" style="left:28px;top:420px;width:448px;height:2px;background:#F0F0F0"></div>'
            f'<div class="abs" style="left:28px;top:448px;width:448px;height:196px;border-radius:20px;background:#fff;border:2px solid #D8D8D8">'
            f'<div class="bar d" style="left:24px;top:30px;width:180px"></div>{sqs}'
            '<div class="bar" style="left:24px;top:144px;width:150px;height:14px"></div>'
            '<div class="bar" style="left:316px;top:144px;width:106px;height:14px"></div></div>'
            f'<div class="chk" id="chk" style="left:28px;top:690px">{ICON["check"]}</div>'
            '<div class="bar" style="left:90px;top:694px;width:300px;height:14px"></div>'
            '<div class="bar" style="left:90px;top:720px;width:200px;height:14px"></div>'
            f'<div class="btn" id="bC"><span id="bCt">Place order</span><span id="bCk" class="abs" style="width:44px;height:44px">{ICON["check"]}</span></div>'
            f'<div class="scr" id="okv" style="background:#fff">'
            f'<div class="disc" id="okd" style="left:142px;top:280px;width:220px;height:220px"><div style="width:120px;height:120px">{ICON["check"]}</div></div>'
            '<div class="bar d" id="okb1" style="left:142px;top:560px;width:220px;height:18px;border-radius:9px"></div>'
            '<div class="bar" id="okb2" style="left:172px;top:600px;width:160px;height:14px"></div></div></div>')
    phone = (f'<div id="phone"><div class="plate"></div><div class="body"></div>'
             f'<div id="screen">{status_bar()}{scrA}{scrB}{scrC}</div></div>')

    steps = ["Select <em>Katapult</em><br>at checkout.", "<em>Apply</em> and verify<br>your information", "Review and <em>submit</em><br>your order"]
    hls = "".join(f'<h2 class="hl" id="sh{i}" style="left:116px;top:378px;width:860px;font-size:80px">{s}</h2>' for i, s in enumerate(steps))
    stepn = '<div class="disc stepn" id="sn">' + "".join(f'<span id="sn{i}">{i + 1}</span>' for i in range(3)) + "</div>"

    # cover (Dark Blue panel that wipes up): logo, headline (40 below), sub (20 below), cluster (56 below)
    cover = (f'<div class="L" id="dk1" style="background:{DBLUE};z-index:20">'
             f'{accent("acc1", (1080, 1720), (760, 1720), (760, 1560), r=90, dots=3)}'
             f'{logo(LOGO_PINK, "lg1", 260, 120, 270)}'
             '<h1 class="hl" id="ch" style="left:114px;top:368px;font-size:118px;color:#fff">'
             '<span id="ch0">How to use</span><span id="ch1">Katapult at</span><span id="ch2"><em>checkout</em></span></h1>'
             '<div class="abs" id="csub" style="left:120px;top:756px;font-size:44px;color:#fff">A step-by-step walkthrough</div>'
             f'{cluster("c")}</div>')
    # end card: statement centred, the same cluster (0.8), logo centred at the foot
    end = (f'<div class="L" id="dk2" style="background:{DBLUE};z-index:20">'
           f'{accent("acc3", (1080, 470), (990, 470), (990, 700), r=90, dots=4)}'
           '<h1 class="hl" id="eh" style="left:0;top:290px;width:1080px;text-align:center;font-size:140px;color:#fff">'
           '<span id="eh0">Apply.</span><span id="eh1">Shop.</span><span id="eh2"><em>Enjoy.</em></span></h1>'
           f'<div class="L" style="transform-origin:0 0;transform:translate(108px,87px) scale(.8)">{cluster("e")}</div>'
           f'{logo(LOGO_PINK, "lg3", 280, 400, 1367)}'
           '</div>')
    stage = (f'<div class="shape" style="left:700px;top:-90px;width:520px;height:300px;background:{PINK};transform:rotate(-7deg)"></div>'
             f'<div class="shape" style="left:-160px;top:1700px;width:520px;height:360px;background:{DBLUE};transform:rotate(6deg)"></div>'
             f'{accent("acc2", (1080, 760), (950, 760), (950, 1200), dots=6)}'
             f'{stepn}{hls}{phone}<div id="ring"></div><div id="touch"></div>')
    return stage + cover + end


# ---------------------------------------------------------------- 15 Cyber Monday finds
# One product at a time, big and centred on its own shape (cutout box 390 = 78% of the 500 shape);
# it swipes off and the cutout shrinks into the next slot of the cart card. Slots fill left to right.
BG15 = "#EAD0B6"                                        # light Cream ground (Lucas, 2026-10-16)
P15 = [("tv", LBLUE, "50%"), ("headphones", PINK, "64px"), ("laptop", DBLUE, "50%"),
       ("console", LBLUE, "64px"), ("couch", PINK, "50%")]   # product, shape color, shape radius
SLOT = {"x0": 200, "dx": 170, "y": 1457, "box": 500, "in": 132}   # slot centres (stage px), product box, size in slot


def body15():
    shapes = "".join(f'<div class="pshape" id="ps{i}"><div class="shape" style="left:0;top:0;width:640px;height:640px;'
                     f'border-radius:{"50%" if r == "50%" else "88px"};background:{c}"></div></div>' for i, (p, c, r) in enumerate(P15))
    prods = "".join(img(p, style="left:0;top:0;width:500px;height:500px;z-index:20", id_=f"p{i}") for i, (p, _, _) in enumerate(P15))
    slots = "".join(f'<div class="slot" id="sl{i}" style="left:{32 + i * SLOT["dx"]}px"></div>' for i in range(5))
    cart = f'<div class="cart" id="cart"><div class="plate"></div><div class="face"></div>{slots}</div>'
    # badges on the card's top edge: bag (left) and the closing check (right); the big bag disc opens frame 1
    bag = (f'<div class="disc" id="bagd" style="left:0;top:0;width:360px;height:360px;z-index:25">'
           f'<div style="width:190px;height:190px">{ICON["bag"]}</div></div>')
    cok = (f'<div class="disc" id="cok" style="left:890px;top:1290px;width:80px;height:80px;z-index:25">'
           f'<div style="width:46px;height:46px">{ICON["check"]}</div></div>')
    return (f'<div class="L" style="background:{BG15}"></div>'
            f'{logo(LOGO_PINK, "lg1", 250, 415, 268)}'
            '<h1 class="hl" id="hl" style="left:0;top:364px;width:1080px;text-align:center;font-size:124px;color:#131540">'
            '<span id="h0">Cyber Monday</span><span id="h1"><em>finds</em></span></h1>'
            f'{shapes}{cart}{bag}{cok}{prods}')


def assets():
    a = HF / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    (a / "products").mkdir(parents=True, exist_ok=True)
    for n in ("Regular", "Medium", "Bold"):
        shutil.copy2(IDENT / f"AktivGrotesk-{n}.otf", a / "fonts")
    for p in {"couch", "headphones", "tv", "washer", "laptop", "console"}:
        shutil.copy2(PRODUCTS / f"{p}.webp", a / "products")
    for js in ("common.js", "t07.js", "t15.js"):
        shutil.copy2(HERE / js, a / js)
    shutil.copy2(HF / "node_modules" / "gsap" / "dist" / "gsap.min.js", a / "gsap.min.js")


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    assets()
    for vid, body, js in (("07", body07(), "t07.js"), ("15", body15(), "t15.js")):
        p = BUILD / f"{vid}.html"
        p.write_text(page(vid, body, js), encoding="utf8")
        print(p.name)


if __name__ == "__main__":
    main()
