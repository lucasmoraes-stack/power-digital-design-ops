"""RKU26012 TV Advertising in 3 Steps: 20 s animated explainer, 4 sizes.

One HTML page per size, driven by a deterministic timeline: seek(t) sets every element for time
t (seconds), so render.py can step through frames and pipe them to ffmpeg.

Beats (s):  0.0 intro (headline + the three steps)       2.4 step 1 budget ($5,000)
            6.0 step 2 audience (interest, 25-34, 90210)   10.8 step 3 upload (0-100%) + launch
           15.0 the ad playing on a living-room TV         17.4 CTA end frame

Reusable pieces (also on the Roku Design System page): Roku City silhouette
(01-brand/roku_city.py), glass card with purple inner shadows, field, dropdown, age pills,
upload bar, cursor + click ring, caret.

    python -I anim.py            -> hf/compositions/<size>.html for 16x9, 1x1, 4x5, 9x16 (+ hf/assets)
    cd hf && npx hyperframes render -c compositions/16x9.html -o ../export/<name>.mp4
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAND = HERE.parents[2] / "01-brand"
sys.path.insert(0, str(BRAND))
from rk_common import lockup  # noqa: E402
from roku_city import blimp_svg, city_svg  # noqa: E402

HF = HERE / "hf"                      # HyperFrames project: compositions/<size>.html + assets/
BUILD = HF / "compositions"
FONTS = BRAND / "identity" / "fonts"
DUR = 20

# Room: RKU26013 V4 Homegoods room (city keyed in the glass). Screen = the TV glass in plate px.
ROOM = {"img": "../assets/room-home.png", "ad": "../assets/tv-ad-home.png", "size": 1254, "screen": [392, 398, 865, 647]}

# Per size: stage, card scale k and position, copy position. Card is designed 860 px wide.
SIZES = {
    "16x9": {"W": 1920, "H": 1080, "k": 1.0, "cardX": 930, "anchor": "center", "cy": 568,
             "copyX": 130, "pillY": 352, "hl": 132, "hlLines": 2, "lk": [130, 84, 330],
             "intro": {"hl": 132, "y": 300, "chips": "row"}, "cta": {"hl": 132, "y": 330}, "safe": [0, 0],
             "blimp": [1600, 1230, 44, 350]},
    "1x1": {"W": 1440, "H": 1440, "k": 1.08, "cardX": 256, "anchor": "top", "top": 452,
            "copyX": 256, "pillY": 196, "hl": 104, "hlLines": 1, "lk": [256, 92, 300],
            "intro": {"hl": 124, "y": 400, "chips": "row"}, "cta": {"hl": 124, "y": 430}, "safe": [0, 0],
            "blimp": [1120, 940, 96, 270]},
    "4x5": {"W": 1440, "H": 1800, "k": 1.24, "cardX": 187, "anchor": "top", "top": 662,
            "copyX": 187, "pillY": 236, "hl": 132, "hlLines": 2, "lk": [187, 100, 340],
            "intro": {"hl": 132, "y": 520, "chips": "col"}, "cta": {"hl": 132, "y": 560}, "safe": [0, 0],
            "blimp": [1110, 960, 112, 300]},
    "9x16": {"W": 1440, "H": 2560, "k": 1.44, "cardX": 101, "anchor": "group", "top": 920, "minTop": 430,
             "copyX": 101, "pillY": 432, "hl": 156, "hlLines": 2, "lk": [101, 300, 420],
             "intro": {"hl": 150, "y": 760, "chips": "col"}, "cta": {"hl": 150, "y": 860}, "safe": [267, 333],
             "blimp": [1110, 1000, 292, 300]},
}
CANVAS = {"16x9": "1920x1080", "1x1": "1440x1440", "4x5": "1440x1800", "9x16": "1440x2560"}
PLAT = {"16x9": "CTV", "1x1": "Meta", "4x5": "Meta", "9x16": "Meta"}

STEPS = [("Set Your", "Budget"), ("Pick Your", "Audience"), ("Upload Your", "Content")]

ICON = {
    "dollar": '<svg viewBox="0 0 24 24"><path d="M12 2v20M17 6.5c-.8-1.5-2.6-2.5-5-2.5-3 0-4.8 1.5-4.8 3.6 0 4.9 10 2.8 10 8 0 2.2-2 3.9-5.2 3.9-2.6 0-4.5-1.1-5.3-2.8" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>',
    "people": '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="7.5" r="3.6"/><path d="M5 20c.4-4 3.3-6.4 7-6.4s6.6 2.4 7 6.4z"/><circle cx="5" cy="9.5" r="2.5" opacity=".75"/><path d="M0 18.5c.3-2.8 2-4.5 4.6-4.6-1 1.2-1.6 2.7-1.8 4.6z" opacity=".75"/><circle cx="19" cy="9.5" r="2.5" opacity=".75"/><path d="M24 18.5c-.3-2.8-2-4.5-4.6-4.6 1 1.2 1.6 2.7 1.8 4.6z" opacity=".75"/></svg>',
    "cloud": '<svg viewBox="0 0 24 24"><path d="M7 18H6.2A4.2 4.2 0 0 1 6 9.6 6 6 0 0 1 17.6 8.4 4.8 4.8 0 0 1 18 18h-1M12 21v-9M8.6 15.2 12 11.8l3.4 3.4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "chev": '<svg viewBox="0 0 24 24"><path d="m6 9 6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "up": '<svg viewBox="0 0 24 24"><path d="m6 15 6-6 6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7.5 7.5 0 0 0-7.5 7.5C4.5 15 12 22 12 22s7.5-7 7.5-12.5A7.5 7.5 0 0 0 12 2zm0 10.3a2.8 2.8 0 1 1 0-5.6 2.8 2.8 0 0 1 0 5.6z"/></svg>',
    "check": '<svg viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "file": '<svg viewBox="0 0 24 24"><path d="M14 2.5H6.5a2 2 0 0 0-2 2v15a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V8z" fill="none" stroke="currentColor" stroke-width="2"/><path d="m10 10.5 5 3-5 3z" fill="currentColor"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}
CURSOR = ('<svg viewBox="0 0 40 48"><path d="M4 3 L4 37 L13 29 L19.5 43.5 L26 40.5 L19.6 26.6 L31.5 26.2 Z" '
          'fill="#fff" stroke="#20004C" stroke-width="2.6" stroke-linejoin="round"/></svg>')


def font_face():
    out = []
    for w, n in [(400, "Regular"), (500, "Medium"), (700, "Bold"), (900, "Black")]:
        out.append(f'@font-face{{font-family:"Roku Display";font-weight:{w};src:url("../assets/fonts/RokuDisplay-{n}.otf") format("opentype")}}')
    return "\n".join(out)


CSS = """
*{box-sizing:border-box}
html,body{margin:0;background:#20004C}
#st{position:relative;width:%(W)spx;height:%(H)spx;overflow:hidden;font-family:"Roku Display",sans-serif;color:#fff;
  background:radial-gradient(120%% 80%% at 85%% 0%%,#5B12B8 0%%,rgba(79,1,163,0) 60%%),linear-gradient(180deg,#3B0886 0%%,#26045C 55%%,#1A0440 100%%)}
.abs{position:absolute;left:0;top:0}
#glow{position:absolute;width:%(G)spx;height:%(G)spx;border-radius:50%%;background:radial-gradient(circle,rgba(133,61,255,.55),rgba(133,61,255,0) 65%%);filter:blur(10px)}
#glow2{position:absolute;width:%(G)spx;height:%(G)spx;border-radius:50%%;background:radial-gradient(circle,rgba(236,74,240,.28),rgba(236,74,240,0) 65%%)}
#city{position:absolute;left:0;bottom:0;opacity:.9}
#blimp{position:absolute;left:0;top:0;opacity:.95;filter:drop-shadow(0 10px 24px rgba(10,0,30,.35))}
#blimp svg{display:block;width:100%%;height:auto}
#city svg{display:block;width:100%%;height:100%%}
.lk{position:absolute;display:block;height:auto}
/* step copy */
.pill{position:absolute;display:inline-flex;align-items:center;padding:.62em 1.5em;border-radius:999px;border:2px solid rgba(178,145,255,.7);
  background:rgba(32,0,76,.45);box-shadow:inset 0 0 18px rgba(133,61,255,.45);font-weight:700;letter-spacing:.28em;color:#fff;white-space:nowrap}
.hl{position:absolute;margin:0;font-weight:400;line-height:1.02;letter-spacing:-.02em;white-space:nowrap}
.hl span{display:block}
.hl em{font-style:normal;background:linear-gradient(90deg,#C9A6FF,#EC4AF0);-webkit-background-clip:text;background-clip:text;color:transparent}
/* card */
#card{position:absolute;left:0;top:0;width:860px;transform-origin:0 0;border-radius:40px;overflow:hidden;
  background:linear-gradient(160deg,rgba(91,26,186,.62),rgba(32,0,76,.78));
  border:2px solid rgba(178,145,255,.55);
  box-shadow:inset 0 0 60px rgba(133,61,255,.35),inset 0 2px 0 rgba(255,255,255,.12),0 40px 120px rgba(10,0,30,.6),0 0 80px rgba(133,61,255,.25);
  backdrop-filter:blur(18px)}
.stepper{position:absolute;left:48px;top:44px;width:764px;height:60px}
.stepper .it{position:absolute;top:0;display:flex;align-items:center;gap:12px;font-size:21px;font-weight:500;color:rgba(233,222,255,.55)}
.stepper .n{width:32px;height:32px;border-radius:50%%;border:2px solid rgba(178,145,255,.55);display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:700;color:rgba(233,222,255,.7)}
.stepper .n svg{width:18px;height:18px}
.stepper .it.on{color:#fff}.stepper .it.on .n{background:#853DFF;border-color:#B391FF;color:#fff;box-shadow:0 0 16px rgba(133,61,255,.8)}
.stepper .it.done .n{background:rgba(133,61,255,.35);border-color:#B391FF;color:#fff}
.stepper .tr{position:absolute;left:0;top:50px;width:764px;height:6px;border-radius:3px;background:rgba(178,145,255,.2)}
.stepper .fi{position:absolute;left:0;top:50px;height:6px;border-radius:3px;background:linear-gradient(90deg,#853DFF,#EC4AF0);box-shadow:0 0 12px rgba(236,74,240,.6)}
.pane{position:absolute;left:0;top:0;width:860px;height:100%%}
.head{position:absolute;left:48px;top:134px;display:flex;align-items:center;gap:22px;font-size:38px;font-weight:700}
.ic{width:68px;height:68px;border-radius:50%%;background:radial-gradient(circle at 35%% 30%%,#A46BFF,#853DFF 55%%,#6A1FE0);display:flex;align-items:center;justify-content:center;color:#fff;
  box-shadow:0 0 24px rgba(133,61,255,.7),inset 0 -4px 10px rgba(32,0,76,.35)}
.ic svg{width:36px;height:36px}
.lab{position:absolute;left:48px;font-size:23px;font-weight:500;color:rgba(233,222,255,.82)}
.fld{position:absolute;left:48px;width:764px;border-radius:22px;background:rgba(20,0,52,.55);
  box-shadow:inset 0 0 0 2px rgba(178,145,255,.4),inset 0 8px 26px rgba(133,61,255,.38),inset 0 -2px 10px rgba(32,0,76,.6)}
.fld.focus{box-shadow:inset 0 0 0 3px #C9A6FF,inset 0 8px 26px rgba(133,61,255,.55),0 0 0 6px rgba(133,61,255,.28),0 0 34px rgba(236,74,240,.35)}
.fld .tx{position:absolute;top:50%%;transform:translateY(-50%%);white-space:nowrap;display:flex;align-items:center}
.ph{color:rgba(201,166,255,.45)}
.caret{display:inline-block;width:3px;margin-left:4px;background:#fff;border-radius:2px}
.btn{position:absolute;height:74px;border-radius:999px;display:flex;align-items:center;justify-content:center;gap:12px;font-size:27px;font-weight:700;color:#fff;
  background:linear-gradient(180deg,#9A5CFF,#853DFF 50%%,#6E22E8);box-shadow:inset 0 2px 0 rgba(255,255,255,.3),inset 0 -6px 14px rgba(32,0,76,.35),0 10px 30px rgba(133,61,255,.55)}
.btn svg{width:28px;height:28px}
.pills .p{position:absolute;height:80px;width:241px;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:29px;font-weight:500;background:rgba(20,0,52,.55);
  box-shadow:inset 0 0 0 2px rgba(178,145,255,.4),inset 0 8px 22px rgba(133,61,255,.3)}
.pills .p.sel{background:linear-gradient(180deg,#A46BFF,#853DFF);font-weight:700;box-shadow:inset 0 0 0 3px #D9C2FF,inset 0 -6px 14px rgba(32,0,76,.3),0 0 30px rgba(133,61,255,.75)}
.menu{position:absolute;left:48px;top:354px;width:764px;border-radius:20px;background:#2A0868;padding:10px;
  box-shadow:inset 0 0 0 2px rgba(178,145,255,.5),0 24px 60px rgba(10,0,30,.65);transform-origin:50%% 0}
.menu .o{height:62px;border-radius:12px;display:flex;align-items:center;padding:0 22px;font-size:26px;font-weight:500;color:rgba(255,255,255,.9)}
.menu .o.hov{background:rgba(133,61,255,.55)}
.drop{position:absolute;left:48px;top:226px;width:764px;height:300px;border-radius:26px;border:3px dashed rgba(178,145,255,.55);background:rgba(20,0,52,.35);
  box-shadow:inset 0 8px 30px rgba(133,61,255,.25)}
.drop .cl{position:absolute;left:50%%;top:42px;width:84px;height:84px;margin-left:-42px;color:#C9A6FF}
.bar{position:absolute;left:48px;width:764px;height:16px;border-radius:8px;background:rgba(20,0,52,.6);box-shadow:inset 0 0 0 2px rgba(178,145,255,.35),inset 0 3px 8px rgba(133,61,255,.4);overflow:hidden}
.bar i{position:absolute;left:0;top:0;height:100%%;border-radius:8px;background:linear-gradient(90deg,#853DFF,#C06BFF,#EC4AF0);box-shadow:0 0 14px rgba(236,74,240,.8)}
.frow{position:absolute;left:48px;width:764px;display:flex;align-items:center;gap:14px;font-size:26px;font-weight:500}
.frow svg{width:32px;height:32px;color:#C9A6FF}
.frow .pc{margin-left:auto;font-weight:700;font-variant-numeric:tabular-nums}
.frow .ok{width:30px;height:30px;border-radius:50%%;background:#1BCECB;color:#20004C;display:flex;align-items:center;justify-content:center}
.frow .ok svg{width:20px;height:20px;color:#20004C}
/* cursor */
#cur{position:absolute;left:0;top:0;width:%(CU)spx;height:%(CUH)spx;filter:drop-shadow(0 6px 10px rgba(10,0,30,.5));z-index:30}
#cur svg{width:100%%;height:100%%;display:block}
#ring{position:absolute;border-radius:50%%;border:%(RB)spx solid #fff;z-index:29}
/* intro + cta */
.center{position:absolute;left:0;width:100%%;display:flex;flex-direction:column;align-items:center;text-align:center}
.chips{display:flex;gap:22px}
.chips.col{flex-direction:column;align-items:flex-start}
.chip{display:flex;align-items:center;gap:.6em;padding:.55em 1.1em .55em .6em;border-radius:999px;background:rgba(32,0,76,.5);font-weight:500;white-space:nowrap;
  box-shadow:inset 0 0 0 2px rgba(178,145,255,.45),inset 0 6px 18px rgba(133,61,255,.35)}
.chip b{width:1.7em;height:1.7em;border-radius:50%%;background:#853DFF;display:flex;align-items:center;justify-content:center;font-weight:700;box-shadow:0 0 14px rgba(133,61,255,.8)}
.ctab{display:inline-flex;align-items:center;gap:.5em;border-radius:999px;font-weight:700;color:#4F01A3;background:#fff;padding:.7em 1.4em .7em 1.6em;
  box-shadow:0 0 0 8px rgba(255,255,255,.12),0 18px 50px rgba(133,61,255,.6)}
.ctab svg{width:1.05em;height:1.05em}
/* tv */
#tv{position:absolute;left:0;top:0;width:100%%;height:100%%;overflow:hidden;background:#20004C}
#world{position:absolute;left:0;top:0;width:%(RS)spx;height:%(RS)spx;transform-origin:0 0}
#world img.room{position:absolute;left:0;top:0;width:%(RS)spx;height:%(RS)spx}
.scr{position:absolute;overflow:hidden;background:#3A0A7A center/cover no-repeat}
.scr .t{position:absolute;left:6.5%%;top:22%%;display:flex;flex-direction:column;gap:8px;color:#fff}
.scr h2{margin:0;font-weight:700;font-size:27px;line-height:1.06;letter-spacing:-.01em}
.scr p{margin:0;font-size:13px;line-height:1.3;color:#E9DEFF}
.scr .b{align-self:flex-start;margin-top:6px;background:#fff;color:#4F01A3;font-weight:700;font-size:12px;padding:6px 13px;border-radius:999px}
.scr .ad{position:absolute;right:3%%;top:5%%;font-size:9px;font-weight:500;background:rgba(0,0,0,.35);padding:3px 7px;border-radius:4px}
.scr .pg{position:absolute;left:3%%;right:3%%;bottom:5%%;height:3px;border-radius:2px;background:rgba(255,255,255,.3)}
.scr .pg i{position:absolute;left:0;top:0;height:100%%;border-radius:2px;background:#fff}
#flash{position:absolute;left:0;top:0;width:100%%;height:100%%;background:#fff;pointer-events:none;z-index:40}
"""


def page(size):
    S = SIZES[size]
    W, H = S["W"], S["H"]
    u = W / 1440 if W >= H else 1.0           # UI unit for stage-level pieces (cursor, chips)
    cu = 46 * max(S["k"], .9)
    css = CSS % {"W": W, "H": H, "G": round(max(W, H) * .9), "CU": round(cu), "CUH": round(cu * 1.2),
                 "RB": round(4 * S["k"]), "RS": ROOM["size"]}
    # Roku City band: full width, height ~ 38% of the shorter side, a touch wider for the drift
    cw, ch = round(W * 1.08), round(min(W, H) * (.42 if H > W else .40))
    city = city_svg(3840, round(3840 * ch / cw), uid="rc")

    hl = S["hl"]
    copy = []
    for i, (a, b) in enumerate(STEPS):
        lines = f"<span>{a}</span><span><em>{b}</em></span>" if S["hlLines"] == 2 else f"<span>{a} <em>{b}</em></span>"
        copy.append(f'<div class="pill" id="pill{i}" style="left:{S["copyX"]}px;top:{S["pillY"]}px;font-size:{round(hl * .21)}px">STEP {i + 1} OF 3</div>'
                    f'<h2 class="hl" id="hl{i}" style="left:{S["copyX"] - hl * .04:.0f}px;top:{S["pillY"] + hl * .82:.0f}px;font-size:{hl}px">{lines}</h2>')

    stepper = "".join(
        f'<div class="it" id="si{i}" style="left:{i * 262}px"><span class="n" id="sn{i}">{i + 1}</span>{n}</div>'
        for i, n in enumerate(["Budget", "Audience", "Content"])) + '<div class="tr"></div><div class="fi" id="sfi"></div>'

    p1 = (f'<div class="pane" id="pane0"><div class="head"><span class="ic">{ICON["dollar"]}</span>Your Budget</div>'
          '<div class="lab" style="top:232px">Campaign budget</div>'
          '<div class="fld" id="f-budget" style="top:270px;height:124px">'
          '<div class="tx" style="left:34px;font-size:56px;font-weight:500;color:rgba(201,166,255,.8)">$</div>'
          '<div style="position:absolute;left:96px;top:26px;width:2px;height:72px;background:rgba(178,145,255,.35)"></div>'
          '<div class="tx" style="left:126px;font-size:70px;font-weight:700;letter-spacing:-.01em"><span id="v-budget"></span><i class="caret" id="c-budget" style="height:66px"></i></div>'
          f'<div style="position:absolute;right:26px;top:16px;width:36px;color:rgba(201,166,255,.8)">{ICON["up"]}{ICON["chev"]}</div>'
          '</div>'
          f'<div class="btn" id="b-next0" style="left:592px;top:440px;width:220px">Next{ICON["arrow"]}</div></div>')
    pills = "".join(f'<div class="p" id="age{i}" style="left:{48 + i * 261.5:.0f}px;top:430px">{a}</div>'
                    for i, a in enumerate(["18–24", "25–34", "35–50"]))
    opts = ["Food & Drink", "Home & Garden", "Pets", "Sports & Fitness", "Travel"]
    p2 = (f'<div class="pane" id="pane1"><div class="head"><span class="ic">{ICON["people"]}</span>Your Audience</div>'
          '<div class="lab" style="top:226px">Interests</div>'
          '<div class="fld" id="f-int" style="top:262px;height:84px">'
          '<div class="tx" style="left:30px;font-size:29px;font-weight:500" id="v-int"></div>'
          f'<div style="position:absolute;right:26px;top:24px;width:36px;color:#C9A6FF" id="int-chev">{ICON["chev"]}</div></div>'
          '<div class="lab" style="top:392px">Age range</div>'
          f'<div class="pills">{pills}</div>'
          '<div class="lab" style="top:548px">ZIP code</div>'
          '<div class="fld" id="f-zip" style="top:584px;height:84px">'
          f'<div style="position:absolute;left:26px;top:22px;width:38px;color:#C9A6FF">{ICON["pin"]}</div>'
          '<div class="tx" style="left:82px;font-size:36px;font-weight:700;letter-spacing:.02em"><span id="v-zip"></span><i class="caret" id="c-zip" style="height:38px"></i></div></div>'
          f'<div class="btn" id="b-next1" style="left:592px;top:714px;width:220px">Next{ICON["arrow"]}</div>'
          '<div class="menu" id="menu">' + "".join(f'<div class="o" id="mo{i}">{o}</div>' for i, o in enumerate(opts)) + '</div></div>')
    p3 = (f'<div class="pane" id="pane2"><div class="head"><span class="ic">{ICON["cloud"]}</span>Your Content</div>'
          f'<div class="drop"><div class="cl">{ICON["cloud"]}</div>'
          f'<div class="btn" id="b-up" style="left:202px;top:150px;width:354px">Upload Content</div></div>'
          f'<div class="frow" id="frow" style="top:560px">{ICON["file"]}<span>TV_Ad.mp4</span><span class="pc" id="v-pc">0%</span>'
          f'<span class="ok" id="okc">{ICON["check"]}</span></div>'
          '<div class="bar" id="bar" style="top:610px"><i id="bar-i"></i></div>'
          f'<div class="btn" id="b-launch" style="left:472px;top:670px;width:340px">Launch Campaign</div></div>')

    ih, ch_ = S["intro"]["hl"], S["cta"]["hl"]
    chips = "".join(f'<div class="chip" id="chip{i}"><b>{i + 1}</b>{a} {b}</div>' for i, (a, b) in enumerate(STEPS))
    chip_fs = round(ih * .27)
    lk_w = S["lk"][2]

    def big_lk(id_, mb):
        return lockup("", "#FFFFFF", "#C9A6FF").replace("<svg ", f'<svg id="{id_}" style="width:{round(lk_w * 1.15)}px;height:auto;margin-bottom:{mb}px" ', 1)
    intro = (f'<div class="center" id="intro" style="top:{S["intro"]["y"]}px">'
             f'{big_lk("ilk", round(ih * .5))}'
             f'<h1 class="hl" style="position:relative;font-size:{ih}px;text-align:center" id="ihl"><span id="ih0">Advertise on TV in</span><span id="ih1"><em>3 Simple Steps</em></span></h1>'
             f'<div class="chips {S["intro"]["chips"]}" style="margin-top:{round(ih * .5)}px;font-size:{chip_fs}px">{chips}</div></div>')
    cta = (f'<div class="center" id="cta" style="top:{S["cta"]["y"]}px">'
           f'{big_lk("clk", round(ch_ * .5))}'
           f'<h1 class="hl" style="position:relative;font-size:{ch_}px;text-align:center" id="chl"><span>Advertise on TV in</span><span><em>3 Simple Steps</em></span></h1>'
           f'<div style="margin-top:{round(ch_ * .55)}px;font-size:{round(ch_ * (.4 if size == "9x16" else .34))}px"><div class="ctab" id="ctab">Start your first campaign{ICON["arrow"]}</div></div></div>')

    x0, y0, x1, y1 = ROOM["screen"]
    sw = x1 - x0
    tv = (f'<div id="tv"><div id="world"><img class="room" src="{ROOM["img"]}">'
          f'<div class="scr" style="left:{x0}px;top:{y0}px;width:{sw}px;height:{y1 - y0}px;background-image:url({ROOM["ad"]})">'
          '<span class="ad">Ad · 0:15</span><div class="t"><h2>Comfort,<br>styled your way.</h2><p>Furniture and decor<br>made to last.</p><span class="b">Shop now</span></div>'
          '<div class="pg"><i id="tvpg"></i></div></div></div></div>')

    cfg = dict(S, size=size, room=ROOM, cw=cw, ch=ch, comp=f"rku26012-{size}", dur=DUR)
    lk = lockup("lk", "#FFFFFF", "#C9A6FF").replace('class="lk"', f'class="lk" id="slk" style="left:{S["lk"][0]}px;top:{S["lk"][1]}px;width:{S["lk"][2]}px"', 1)
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>RKU26012 {size}</title>
<style>{font_face()}{css}</style></head><body>
<div id="st" data-composition-id="rku26012-{size}" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}" data-fps="30">
  <div id="glow"></div><div id="glow2"></div>
  <div id="city" style="width:{cw}px;height:{ch}px">{city}</div>
  <div id="blimp" style="width:{S["blimp"][3]}px">{blimp_svg(S["blimp"][3])}</div>
  {intro}
  <div id="steps">{lk}{''.join(copy)}
    <div id="card"><div class="stepper">{stepper}</div>{p1}{p2}{p3}</div>
  </div>
  {tv}
  {cta}
  <div id="ring"></div>
  <div id="cur">{CURSOR}</div>
  <div id="flash"></div>
</div>
<script>const CFG={json.dumps(cfg)};</script>
<script src="../assets/gsap.min.js"></script>
<script src="../assets/timeline.js"></script>
</body></html>"""


def assets():
    """Everything a composition loads, copied into the HyperFrames project (renders serve this folder)."""
    import shutil
    a = HF / "assets"
    (a / "fonts").mkdir(parents=True, exist_ok=True)
    for n in ("Regular", "Medium", "Bold", "Black"):
        shutil.copy2(FONTS / f"RokuDisplay-{n}.otf", a / "fonts")
    shutil.copy2(HERE / "img" / "room-home.png", a / "room-home.png")
    shutil.copy2(HERE / "img" / "tv-ad-home.png", a / "tv-ad-home.png")
    shutil.copy2(HERE / "timeline.js", a / "timeline.js")
    shutil.copy2(HF / "node_modules" / "gsap" / "dist" / "gsap.min.js", a / "gsap.min.js")


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    assets()
    for s in SIZES:
        p = BUILD / f"{s}.html"
        p.write_text(page(s), encoding="utf8")
        print(p.name)


if __name__ == "__main__":
    main()
