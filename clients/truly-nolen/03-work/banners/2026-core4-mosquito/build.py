"""Truly Nolen, 2026 Core-4 concept: PC Platinum / Mosquito Season Starts Now.

Meta motion graphics, messaging test:
  3 iterations (V1 Outcome, V2 Problem, V3 Service) x 2 sizes (1x1, 9x16) = 6 deliverables.
  Each deliverable ships as a 5-scene storyboard (frames the animator builds from),
  following the client's reference storyboard. Scene 05 is the branded end card.

  python build.py         -> HTML per scene into _build/
  python build.py --png   -> renders every scene to PNG + one storyboard sheet per piece

Photos: the backyard/house plates are generated outside (ChatGPT) and dropped into img/
as {shot}.png, 4:5 with wide margins (optionally {shot}-9x16.png / {shot}-1x1.png to override
the automatic crop, which uses the shot's focal point). See image-prompts.md. Until a plate exists the
scene renders a dusk placeholder with the shot name, so layout and copy can be reviewed now.
Everything that must be exact (copy, clock, mosquitoes, callouts, shield, end card) is
vector, drawn here, never baked into the photo.

Design system: same tokens and fonts as 2026-core4-bof (Figma 216:656).
"""
import base64, io, os, subprocess, sys
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
BRAND = HERE.parents[2]                      # clients/truly-nolen
OUT = BRAND / "04-deliverables" / "banners" / "2026-core4-mosquito"
BUILD = HERE / "_build"                      # HTML intermediates embed licensed fonts: gitignored
IMG = HERE / "img"
FONT_DIR = Path(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts"))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

YELLOW, RED, BLACK, WHITE = "#FFE300", "#ED2524", "#000000", "#FFFFFF"

# ---- sizes (laid out at 1080 wide, exported at 1440 like every TN Meta piece) ----
# 9x16 safe zone (brief, Meta Reels/Stories): 14% top, 35% bottom, 6% sides.
SIZES = {
    "1x1":  dict(W=1080, H=1080, m=72, top=72,  bottom=1008, hl=112, sub=46, logo=150, clock=(72, 72, 1)),
    "9x16": dict(W=1080, H=1920, m=72, top=269, bottom=1248, hl=128, sub=52, logo=170, clock=(540, 330, 1.35)),
}

# ---- photo plates: one per shot, shared across versions for backyard continuity ----
# fy = focal point (0 top .. 1 bottom) used to crop 1x1 from the 9x16 plate
SHOTS = {
    "v1-dinner":  dict(fy=.50, label="V1 moment 1: family dinner on the patio at dusk", src=(1122, 1402), place={"9x16": -240, "1x1": -420}),
    "v1-lawn":    dict(fy=.50, label="V1 moment 2: kids on the lawn, parents relaxing", src=(1122, 1402), place={"9x16": -240, "1x1": -420}),
    "v1-night":   dict(fy=.50, label="V1 moment 3: same patio at night, still outside", src=(1122, 1402),
                       place={"9x16": dict(top=-236, zoom=1.3, fx=.58), "1x1": dict(top=-515, zoom=1.25, fx=.58)}),
    "v2-curfew":  dict(fy=.50, label="V2 moment 1: patio set for dinner, dusk, curfew begins", src=(1122, 1402), place={"9x16": -240, "1x1": -420}),
    "v2-retreat": dict(fy=.50, label="V2 moment 2: abandoned table, everyone heading inside", src=(1122, 1402), place={"9x16": -240, "1x1": -420}),
    "v2-night":   dict(fy=.50, label="V2 moment 3: same patio at night, back outside", src=(1122, 1402),
                       place={"9x16": dict(top=-285, zoom=1.3, fx=.8), "1x1": dict(top=-440, zoom=1.25, fx=.58)}),
    "v3-shrubs":  dict(fy=.50, label="V3 moment 1: yard edge, shrubs and shaded foliage"),
    # place: fit to width and shift up by this many px (1080 space), so the tree, deck,
    # shrubs and birdbath all sit above the copy; edges fade into the scrim.
    "v3-house":   dict(fy=.45, label="V3 moment 2: house and yard with the 4 mosquito areas",
                       src=(1122, 1402), place={"9x16": -290, "1x1": -340}),
    "v3-night":   dict(fy=.50, label="V3 moment 3: home and yard at night, protected", src=(1122, 1402), place={"9x16": -290, "1x1": -340}),
}

# ---- copy (verbatim from the brief; <em> = accent color) ------------------------
# kind: photo | brand | end.  fx: overlays drawn on top of the plate.
END = dict(kind="end", title="End card", hl="Take back your <em>yard.</em>", cta="Learn More",
           cap="Take back your yard.", motion="Hard cut to yellow. No-mosquito icon stamps in, headline and logo rise, CTA pops last.")
VERSIONS = {
    "V1": dict(slug="V1-Outcome", angle="Outcome led", scenes=[
        dict(kind="photo", shot="v1-dinner", title="Summer nights",
             hl="Take back your <em>summer nights.</em>",
             motion="Slow push-in on the lit patio. String lights twinkle. Headline builds line by line."),
        dict(kind="photo", shot="v1-lawn", title="More time outside",
             hl="More time outside.", hl2="Less time swatting.",
             motion="Gentle pan across the lawn. Line 1 in, then line 2 lands on the beat."),
        dict(kind="brand", title="Brand beat",
             hl="Truly Nolen knows <em>mosquitoes.</em>",
             motion="Yellow wipe from the side. Logo drops in with a small bounce, then the headline."),
        dict(kind="photo", shot="v1-night", title="Monthly treatment", fx=["shield"], eyebrow="PC Platinum",
             sub="Monthly mosquito treatment helps reduce activity around your yard.",
             motion="Shield draws on over the yard and settles. Support line fades up under it."),
        END]),
    "V2": dict(slug="V2-Problem", angle="Problem led", scenes=[
        dict(kind="photo", shot="v2-curfew", title="Curfew begins", fx=["clock:7:42"],
             hl="The mosquito-imposed <em>curfew begins.</em>",
             motion="Clock flips to 7:42 PM. First mosquito drifts into frame. Headline slams in."),
        dict(kind="photo", shot="v2-curfew", title="The buzzing starts", fx=["mosq:swarm"],
             hl="The buzzing starts.", hl2="<em>Then come the bites.</em>",
             motion="Same plate as scene 1, clock gone. Mosquitoes multiply and jitter across frame. Quick shake on line 2."),
        dict(kind="photo", shot="v2-retreat", title="The retreat", fx=["clock:7:58", "mosq:few"],
             hl="Right when you want to <em>stay outside.</em>",
             motion="Clock jumps to 7:58 PM. Table left behind, door closes. Mosquitoes linger."),
        dict(kind="photo", shot="v2-night", title="Relief", fx=["shield", "logo"],
             hl="Truly Nolen knows <em>mosquitoes.</em>", sub="Less buzzing in your backyard.",
             motion="Mosquitoes clear out, shield draws on, logo pops in the corner."),
        END]),
    "V3": dict(slug="V3-Service", angle="Service led", scenes=[
        dict(kind="photo", shot="v3-shrubs", title="Mosquito season", fx=["mosq:swarm", "logo"],
             hl="Mosquito season <em>is here.</em>",
             motion="Logo already in the corner. Mosquitoes rise from the shrubs. Headline stamps in."),
        dict(kind="photo", shot="v3-house", title="PC Platinum", fx=["logo"],
             hl="Get ahead of mosquito activity with <em>PC Platinum.</em>",
             motion="Wide reveal of the house and yard. PC Platinum lands in yellow on the last beat."),
        dict(kind="photo", shot="v3-house", title="Treats the source", fx=["callouts", "logo"],
             hl="Truly Nolen knows <em>mosquitoes.</em>",
             sub="Monthly mosquito treatment helps reduce activity around your yard.",
             motion="Same plate. Callouts pin one by one to the mosquito spots, with dashed leader lines."),
        dict(kind="photo", shot="v3-night", title="Home and yard", fx=["shield", "logo"],
             hl="Mosquito control + <em>pest protection</em>", sub="for your home and yard.",
             motion="Shield draws on over the lit yard. Headline, then support line."),
        END]),
}

# ---- vector art --------------------------------------------------------------------
MOSQ = """<g>
<ellipse cx="150" cy="38" rx="58" ry="13" transform="rotate(-14 150 38)" fill="#fff" fill-opacity=".38" stroke="#fff" stroke-opacity=".55" stroke-width="2"/>
<ellipse cx="138" cy="48" rx="50" ry="11" transform="rotate(-4 138 48)" fill="#fff" fill-opacity=".24" stroke="#fff" stroke-opacity=".4" stroke-width="2"/>
<path d="M112 66C140 58 190 62 226 80C232 86 228 92 220 92C186 92 140 84 114 78Z" fill="#0d0b08"/>
<ellipse cx="100" cy="68" rx="20" ry="15" fill="#0d0b08"/>
<circle cx="74" cy="72" r="10" fill="#0d0b08"/>
<g fill="none" stroke="#0d0b08" stroke-linecap="round" stroke-linejoin="round">
<path stroke-width="3" d="M66 76L14 100"/><path stroke-width="2" d="M72 64L52 40M76 63L64 36"/>
<path stroke-width="3" d="M92 80L70 112L46 156"/><path stroke-width="3" d="M100 82L94 118L86 158"/><path stroke-width="3" d="M108 80L128 112L150 156"/>
<path stroke-width="3" d="M90 58L60 28L30 20"/></g></g>"""
MOSQ_VB = "0 0 240 170"

def mosquito(x, y, w, rot=0, flip=False, op=1):
    sx = -1 if flip else 1
    return (f'<svg class="mq" viewBox="{MOSQ_VB}" style="left:{x}px;top:{y}px;width:{w}px;'
            f'transform:rotate({rot}deg) scaleX({sx});opacity:{op}">{MOSQ}</svg>')

# (x, y, width, rotation, flip) as fractions of W / the photo zone above the copy
SWARMS = {
    "swarm": [(.08, .10, .15, -8, 0), (.62, .06, .12, 10, 1), (.78, .30, .17, -4, 1), (.30, .26, .10, 16, 0),
              (.48, .44, .13, -12, 0), (.14, .52, .09, 6, 1), (.86, .60, .08, -18, 0), (.56, .70, .07, 8, 1)],
    "few":   [(.70, .18, .13, 8, 1), (.16, .40, .10, -10, 0), (.80, .56, .08, 14, 1)],
}

SHIELD = """<svg class="shield" viewBox="0 0 120 130" aria-hidden="true">
<path d="M60 6L108 24V60C108 92 86 114 60 124C34 114 12 92 12 60V24Z" fill="#000" fill-opacity=".35" stroke="#FFE300" stroke-width="7" stroke-linejoin="round"/>
<path d="M38 64L54 80L84 48" fill="none" stroke="#FFE300" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

BAN = f"""<svg class="ban" viewBox="0 0 300 300" aria-hidden="true">
<circle cx="150" cy="150" r="134" fill="#fff" stroke="{RED}" stroke-width="26"/>
<g transform="translate(40 70) scale(.92)">{MOSQ.replace('#fff', '#000').replace('fill-opacity=".38"', 'fill-opacity=".12"').replace('fill-opacity=".24"', 'fill-opacity=".08"')}</g>
<path d="M58 58L242 242" stroke="{RED}" stroke-width="26" stroke-linecap="round"/></svg>"""

# callout icons, 24x24 line style
ICONS = {
    "foliage": '<path d="M12 21V11M12 11C7 11 5 7 6 3C10 3 13 6 12 11ZM12 14C16 14 19 11 18 7C14 7 12 10 12 14Z"/>',
    "deck":    '<path d="M3 9H21M5 9V20M19 9V20M9 9V16M15 9V16M3 16H21"/>',
    "water":   '<path d="M12 3C9 8 7 11 7 14A5 5 0 0 0 17 14C17 11 15 8 12 3Z"/>',
    "shrubs":  '<path d="M4 20C2 14 6 11 9 13C9 8 15 8 15 13C18 11 22 14 20 20Z"/>',
}
# label, icon, spot on the v3-house plate (source px), then per ratio the chip (x, y, side).
CALLOUTS = [
    ("Shaded foliage", "foliage", (300, 560), {"9x16": (72, 300, "L"), "1x1": (72, 250, "L")}),
    ("Around shrubs", "shrubs",   (1010, 850), {"9x16": (1008, 400, "R"), "1x1": (1008, 370, "R")}),
    ("Standing water", "water",   (140, 995), {"9x16": (72, 510, "L"), "1x1": (72, 480, "L")}),
    ("Under decks / patios", "deck", (470, 885), {"9x16": (1008, 600, "R"), "1x1": (1008, 560, "R")}),
]
CALLOUT_SHOT = "v3-house"

# ---- fonts -----------------------------------------------------------------------
FONTS = [("TN Display", "FuturaDisplayBQ.otf"), ("TN Medium", "FuturaStd-Medium.otf"),
         ("TN Heavy", "FuturaStd-Heavy.otf")]
BASIC = "".join(chr(c) for c in range(32, 127)) + "\u2019\u2018\u201c\u201d\u00b7\u00d7\u2192\u00b0"

def font_face(text=BASIC):
    css = []
    for fam, fn in FONTS:
        f = TTFont(FONT_DIR / fn)
        opts = subset.Options(); opts.flavor = "woff"; opts.layout_features = ["kern", "liga"]
        s = subset.Subsetter(opts); s.populate(text=text); s.subset(f)
        buf = io.BytesIO(); f.flavor = "woff"; f.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:'{fam}';src:url(data:font/woff;base64,{b64}) format('woff');font-display:block}}")
    return "\n".join(css)

LOGO_PNG = BRAND / "01-brand" / "identity" / "assets" / "tn-logo-sticker.png"
LOGO_RATIO = 522 / 654
def logo_uri():
    return "data:image/png;base64," + base64.b64encode(LOGO_PNG.read_bytes()).decode()

def placement(shot, ratio):
    """(top, zoom, fx) for a plate fitted to width, or None for object-fit cover.
    place values are a top offset, or dict(top=, zoom=, fx=) to punch in: the plate is
    scaled to zoom x width and slid so fx (0 left .. 1 right) of the overflow is cropped."""
    v = SHOTS[shot].get("place", {}).get(ratio)
    if v is None:
        return None
    return (v, 1, .5) if not isinstance(v, dict) else (v["top"], v.get("zoom", 1), v.get("fx", .5))

def plate(shot, ratio, own=False):
    """Photo plate for a shot as (uri, object-position) or None if not generated yet.
    A shot still missing borrows its stand_in plate, unless own=True."""
    for name in (f"{shot}-{ratio}", f"{shot}-9x16", shot):
        for ext in ("png", "jpg", "jpeg", "webp"):
            p = IMG / f"{name}.{ext}"
            if p.exists():
                mime = "jpeg" if ext in ("jpg", "jpeg") else ext
                pos = f"50% {SHOTS[shot]['fy']*100:.0f}%" if name != f"{shot}-{ratio}" else "50% 50%"
                return f"data:image/{mime};base64," + base64.b64encode(p.read_bytes()).decode(), pos
    if not own and SHOTS[shot].get("stand_in"):
        return plate(SHOTS[shot]["stand_in"], ratio)
    return None

# ---- piece CSS -------------------------------------------------------------------
PIECE_CSS = """
.tn{position:relative;overflow:hidden;background:#140d08;color:#fff;font-family:'TN Medium',Futura,'Century Gothic',sans-serif}
.tn *{box-sizing:border-box}
.tn .bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.tn .ph{position:absolute;inset:0;background:
  radial-gradient(120% 60% at 50% 38%,#b7652a 0,#6b3418 30%,#2a160c 60%,#0d0a0c 100%)}
.tn .ph::after{content:'';position:absolute;left:0;right:0;top:58%;bottom:0;background:linear-gradient(#1a120b,#070605)}
.tn .ph-tag{position:absolute;left:50%;transform:translateX(-50%);border:3px dashed rgba(255,255,255,.45);border-radius:14px;
  padding:.5em .9em;font-family:'TN Heavy',sans-serif;color:rgba(255,255,255,.75);text-align:center;white-space:nowrap;line-height:1.25;z-index:1}
.tn .ph-tag small{display:block;font-family:'TN Medium',sans-serif;font-size:.62em;opacity:.8}
.tn .scrim{position:absolute;inset:0}
.tn .copy{position:absolute;display:flex;flex-direction:column;align-items:flex-start;gap:0}
.tn .hl{font-family:'TN Display','Arial Black',sans-serif;text-transform:uppercase;line-height:1;letter-spacing:-.005em;margin:0;text-wrap:balance}
.tn .hl em{font-style:normal;color:#FFE300}
.tn .hl2{margin-top:0}
.tn .sub{font-family:'TN Medium',Futura,sans-serif;line-height:1.24;letter-spacing:-.01em;text-wrap:balance;max-width:17em}
.tn .eyebrow{margin-bottom:.35em;font-family:'TN Heavy',sans-serif;background:#FFE300;color:#000;border-radius:999px;padding:.28em .8em .2em;letter-spacing:.02em}
.tn .logo{position:absolute;display:block;filter:drop-shadow(0 6px 14px rgba(0,0,0,.35))}
.tn .mq{position:absolute;overflow:visible;filter:drop-shadow(0 0 2px rgba(255,236,200,.9)) drop-shadow(0 0 12px rgba(255,210,140,.55))}
.tn .clock{position:absolute;display:flex;align-items:flex-end;gap:.12em;background:rgba(0,0,0,.82);border:3px solid rgba(255,227,0,.35);
  border-radius:.22em;padding:.14em .28em .1em;font-family:'TN Display',sans-serif;color:#FFE300;line-height:.8;
  box-shadow:0 0 40px rgba(255,190,60,.25)}
.tn .clock b{font-weight:400;font-size:1em}.tn .clock span{font-size:.36em;padding-bottom:.08em}
.tn .shield{position:absolute;filter:drop-shadow(0 0 30px rgba(255,227,0,.45))}
.tn .co{position:absolute;inset:0;overflow:visible}
.tn .chip{position:absolute;display:flex;align-items:center;gap:.5em;background:rgba(0,0,0,.84);border:2px solid rgba(255,227,0,.6);
  border-radius:999px;padding:.3em .9em .3em .3em;font-family:'TN Heavy',sans-serif;white-space:nowrap}
.tn .chip i{display:flex;align-items:center;justify-content:center;width:1.9em;height:1.9em;border-radius:50%;background:#FFE300}
.tn .chip svg{width:1.2em;height:1.2em;fill:none;stroke:#000;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
/* brand beat + end card: yellow */
.tn.y{background:radial-gradient(90% 70% at 50% 45%,#FFF38A 0,#FFE300 55%,#F5D800 100%);color:#000}
.tn.y .hl{color:#000;text-align:center}.tn.y .hl em{color:#ED2524}
.tn.y .stack{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.tn.y .logo{position:static;filter:none}
.tn .ban{display:block}
.tn .cta{display:flex;align-items:center;justify-content:center;height:2.4em;padding:0 1.6em;border-radius:999px;background:#000;color:#fff;
  font-family:'TN Heavy',Futura,sans-serif;letter-spacing:-.01em;white-space:nowrap}
.tn .cta>i{font-style:normal;transform:translateY(.05em)}
"""

def scene_html(ratio, sc, logo_src):
    c = SIZES[ratio]; W, H, m = c["W"], c["H"], c["m"]
    tall = ratio == "9x16"
    if sc["kind"] == "brand":
        lh = c["logo"] * (1.55 if tall else 1.25)
        return (f'<div class="tn y" style="width:{W}px;height:{H}px">'
                f'<div class="stack" style="top:{c["top"]}px;height:{c["bottom"]-c["top"]}px;gap:{56 if tall else 44}px;padding:0 {m}px">'
                f'<img class="logo" src="{logo_src}" alt="Truly Nolen" style="height:{lh:.0f}px;width:{lh*LOGO_RATIO:.0f}px">'
                f'<h2 class="hl" style="font-size:{c["hl"]*1.12:.0f}px">{sc["hl"]}</h2></div></div>')
    if sc["kind"] == "end":
        ban = 300 if tall else 250; lh = c["logo"] * (1.05 if tall else .95)
        return (f'<div class="tn y" style="width:{W}px;height:{H}px">'
                f'<div class="stack" style="top:{c["top"]}px;height:{c["bottom"]-c["top"]}px;gap:{38 if tall else 26}px;padding:0 {m}px">'
                f'<div style="width:{ban}px;height:{ban}px">{BAN}</div>'
                f'<h2 class="hl" style="font-size:{c["hl"]*(1.45 if tall else 1.18):.0f}px;max-width:6.4em">{sc["hl"]}</h2>'
                f'<img class="logo" src="{logo_src}" alt="Truly Nolen" style="height:{lh:.0f}px;width:{lh*LOGO_RATIO:.0f}px">'
                f'<span class="cta" style="font-size:{60 if tall else 44}px"><i>{sc["cta"]}</i></span></div></div>')

    # photo scene
    p = plate(sc["shot"], ratio)
    if p:
        pl = placement(sc["shot"], ratio)
        if pl is not None:
            top, z, fx = pl; left = -(W * z - W) * fx
            bg = (f'<img class="bg" src="{p[0]}" alt="" style="top:{top}px;left:{left:.0f}px;width:{W*z:.0f}px;height:auto;'
                  f'-webkit-mask-image:linear-gradient(#000 85%,transparent);mask-image:linear-gradient(#000 85%,transparent)">')
        else:
            bg = f'<img class="bg" src="{p[0]}" style="object-position:{p[1]}" alt="">'
    else:
        bg = (f'<div class="ph"></div><div class="ph-tag" style="top:{120 if tall else 18}px;font-size:{30 if tall else 22}px">'
              f'FOTO: {sc["shot"]}<small>{SHOTS[sc["shot"]]["label"]}</small></div>')
    # scrim: copy sits at the bottom of the safe zone
    if tall:
        scrim = ("linear-gradient(180deg,rgba(0,0,0,.45) 0,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 36%,"
                 "rgba(0,0,0,.66) 56%,rgba(0,0,0,.8) 70%,rgba(0,0,0,.84) 100%)")
    else:
        scrim = "linear-gradient(180deg,rgba(0,0,0,.35) 0,rgba(0,0,0,0) 20%,rgba(0,0,0,0) 50%,rgba(0,0,0,.72) 78%,rgba(0,0,0,.88) 100%)"
    fx = sc.get("fx", [])
    parts = [bg, f'<div class="scrim" style="background:{scrim}"></div>']
    # photo zone = where overlays may live: from top safe line to where the copy starts (approx)
    zone_top, zone_bot = c["top"], c["bottom"] - (430 if tall else 400)
    zh = zone_bot - zone_top
    for f in fx:
        if f.startswith("mosq:"):
            for (x, y, w, r, fl) in SWARMS[f[5:]]:
                parts.append(mosquito(round(x * W), round(zone_top + y * zh), round(w * W * (1 if tall else .85)), r, fl))
        elif f.startswith("clock:"):
            t = f[6:]; x, y, k = c["clock"]; fs = 150 * k
            style = f"top:{y}px;font-size:{fs:.0f}px;" + (f"left:{x}px;transform:translateX(-50%)" if tall else f"left:{x}px")
            parts.append(f'<div class="clock" style="{style}"><b>{t}</b><span>PM</span></div>')
        elif f == "shield":
            s = 250 if tall else 190          # up in the sky, clear of the people
            parts.append(f'<div class="shield" style="left:{(W-s)/2:.0f}px;top:{zone_top + (30 if tall else 0):.0f}px;width:{s}px;height:{s*1.08:.0f}px">{SHIELD}</div>')
        elif f == "callouts":
            parts.append(callouts(c, ratio, tall))
        elif f == "logo":
            lh = c["logo"] * (.8 if tall else .72)
            parts.append(f'<img class="logo" src="{logo_src}" alt="Truly Nolen" style="right:{m}px;top:{c["top"] if tall else 56}px;height:{lh:.0f}px;width:{lh*LOGO_RATIO:.0f}px">')
    # copy block, anchored to the bottom of the safe zone
    body = ""
    if sc.get("eyebrow"):
        body += f'<span class="eyebrow" style="font-size:{c["sub"]*.72:.0f}px">{sc["eyebrow"]}</span>'
    if sc.get("hl"):
        body += f'<h2 class="hl" style="font-size:{c["hl"]}px">{sc["hl"]}</h2>'
    if sc.get("hl2"):
        body += f'<h2 class="hl hl2" style="font-size:{c["hl"]}px">{sc["hl2"]}</h2>'
    if sc.get("sub"):
        big = not sc.get("hl")
        body += f'<p class="sub" style="font-size:{c["sub"]*(1.3 if big else 1):.0f}px;margin:{".55em" if not big else "0"} 0 0">{sc["sub"]}</p>'
    parts.append(f'<div class="copy" style="left:{m}px;right:{m}px;bottom:{H-c["bottom"]}px">{body}</div>')
    return f'<div class="tn" style="width:{W}px;height:{H}px">{"".join(parts)}</div>'

def callouts(c, ratio, tall):
    fs = 30 if tall else 24; ch = fs * 2.5; out = []; lines = []
    sh = SHOTS[CALLOUT_SHOT]; k = c["W"] / sh["src"][0]; T = sh["place"][ratio]
    for label, icon, (px, py), pos in CALLOUTS:
        cx, cy, side = pos[ratio]
        x, y = round(px * k), round(py * k + T)
        anchor = f"left:{cx}px" if side == "L" else f"right:{c['W']-cx}px"
        out.append(f'<div class="chip" style="{anchor};top:{cy}px;font-size:{fs}px">'
                   f'<i><svg viewBox="0 0 24 24">{ICONS[icon]}</svg></i>{label}</div>')
        sx = cx + fs * 1.25 if side == "L" else cx - fs * 1.25
        sy = cy + ch if y > cy + ch else cy          # leave from the edge that faces the spot
        lines.append(f'<path d="M{sx:.0f} {sy:.0f}L{x} {y}" stroke="#FFE300" stroke-width="3" stroke-dasharray="8 8" fill="none"/>'
                     f'<circle cx="{x}" cy="{y}" r="{16 if tall else 13}" fill="#FFE300" fill-opacity=".3"/>'
                     f'<circle cx="{x}" cy="{y}" r="{8 if tall else 6}" fill="#FFE300"/>')
    return (f'<svg class="co" viewBox="0 0 {c["W"]} {c["H"]}" aria-hidden="true">{"".join(lines)}</svg>' + "".join(out))

# ---- naming ----------------------------------------------------------------------
def piece_name(var, ratio):
    return f"TN-Mosquito-Core4-{VERSIONS[var]['slug']}-Motion-Meta-{ratio}"

def standalone(ratio, sc, fonts, title):
    c = SIZES[ratio]
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>{fonts}
html,body{{margin:0;padding:0;background:#000;width:{c['W']}px;height:{c['H']}px;overflow:hidden}}
{PIECE_CSS}</style></head><body>{scene_html(ratio, sc, logo_uri())}</body></html>"""

def build():
    fonts = font_face(); files = []
    for var, v in VERSIONS.items():
        for ratio in SIZES:
            d = BUILD / "scenes" / piece_name(var, ratio); d.mkdir(parents=True, exist_ok=True)
            for i, sc in enumerate(v["scenes"], 1):
                p = d / f"scene-{i:02d}.html"
                p.write_text(standalone(ratio, sc, fonts, f"{piece_name(var, ratio)} S{i:02d}"), encoding="utf-8")
                files.append((var, ratio, i, p))
    return files

def chrome_png(html, png, W, H, scale=1):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", f"--window-size={W},{H}",
                    "--virtual-time-budget=3000", f"--screenshot={png}", html.as_uri()],
                   check=True, capture_output=True)

def render(files):
    for var, ratio, i, p in files:
        c = SIZES[ratio]
        png = OUT / "storyboard" / piece_name(var, ratio) / f"{piece_name(var, ratio)}-S{i:02d}.png"
        png.parent.mkdir(parents=True, exist_ok=True)
        chrome_png(p, png, c["W"], c["H"], 1440 / 1080)
        print("png", png.relative_to(OUT))
    boards()

# ---- storyboard sheets (like the client's reference: numbered frames + captions) ----
def scene_caption(sc):
    import re
    if sc["kind"] == "end":
        return sc["cap"]
    t = " ".join(x for x in (sc.get("hl"), sc.get("hl2"), sc.get("sub")) if x)
    return re.sub("<[^>]+>", "", t)

def boards():
    from PIL import Image, ImageDraw, ImageFont
    disp = ImageFont.truetype(str(FONT_DIR / "FuturaDisplayBQ.otf"), 34)
    med = ImageFont.truetype(str(FONT_DIR / "FuturaStd-Medium.otf"), 21)
    hv = ImageFont.truetype(str(FONT_DIR / "FuturaStd-Heavy.otf"), 22)
    for var, v in VERSIONS.items():
        for ratio in SIZES:
            n = len(v["scenes"]); fw = 360; fh = 640 if ratio == "9x16" else 360
            pad, head, foot = 28, 96, 150
            sheet = Image.new("RGB", (pad + n * (fw + pad), head + fh + foot + pad), "white")
            d = ImageDraw.Draw(sheet)
            for i, sc in enumerate(v["scenes"], 1):
                x = pad + (i - 1) * (fw + pad)
                src = OUT / "storyboard" / piece_name(var, ratio) / f"{piece_name(var, ratio)}-S{i:02d}.png"
                sheet.paste(Image.open(src).convert("RGB").resize((fw, fh), Image.LANCZOS), (x, head))
                d.ellipse((x, 30, x + 40, 70), fill="black")
                d.text((x + 20, 51), str(i), font=hv, fill="white", anchor="mm")
                d.text((x + 54, 50), sc["title"].upper(), font=disp, fill="black", anchor="lm")
                d.rectangle((x, head + fh, x + fw, head + fh + foot), fill="#F4F4F2")
                y = head + fh + 16
                for line in wrap(d, scene_caption(sc), med, fw - 28):
                    d.text((x + fw / 2, y), line, font=med, fill="#222", anchor="ma"); y += 27
            out = OUT / "storyboard" / f"{piece_name(var, ratio)}-storyboard.png"
            sheet.save(out, optimize=True); print("board", out.relative_to(OUT))

def wrap(d, text, font, w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= w: cur = t
        else: lines.append(cur); cur = wd
    return lines + [cur] if cur else lines

if __name__ == "__main__":
    files = build(); print(f"{len(files)} scenes written to {BUILD}")
    if "--png" in sys.argv:
        render(files)
