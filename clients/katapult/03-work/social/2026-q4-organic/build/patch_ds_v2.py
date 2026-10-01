"""DS v2: retire every Bounce line piece, add the v2 components. Applies the same edit to both DS copies
(only lines 3 to 5, the font faces, differ between them and are never touched)."""
import io, os, re
D = os.path.dirname(os.path.abspath(__file__))
FILES = [os.path.join(D, "katapult-ds-src.html"), os.path.join(D, "katapult-ds", "index.html")]
V2CSS = io.open(os.path.join(D, "kp_v2.css"), encoding="utf-8").read().rstrip() + "\n"

CHECK_SVG = '<svg viewBox="0 0 48 48" aria-hidden="true"><use href="#k-check"/></svg>'
SEND_SVG = ('<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 24 H 38 M26 12 L 38 24 L 26 36" fill="none" '
            'stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def demo(cls, inner, cap, sub):
    return (f'<figure class="preview"><div class="kp-frame f-4x5" style="--s:.25"><article class="kp-post kp-r-4x5 kp-v2 {cls}">'
            f'{inner}</article></div><figcaption><b>{cap}</b><span class="mono">{sub}</span></figcaption></figure>')

LAY = lambda stage, top="": f'<div class="kp-lay">{top}<div class="kp-stage">{stage}</div></div>'
ICO = lambda t, d, lab: f'<div class="kp-ico t-{t}" style="--d:{d}px" role="img" aria-label="Icon placeholder">{lab}</div>'
DEMOS = "\n".join([
    demo("kp-theme-pink", LAY(
        '<div class="kp-fan" style="--f:var(--k-dark-blue);left:27cqw;bottom:14cqh;width:46cqw;height:44cqh;transform:rotate(-6deg)"></div>'
        '<div class="kp-a kp-ui" style="left:0;right:0;top:34cqh">'
        '<div class="kp-row"><div class="kp-field kp-grow"><span class="kp-caret"></span></div>'
        f'<span class="kp-send">{SEND_SVG}</span></div><div class="kp-btn"></div></div>'),
        "UI input card", ".kp-ui · .kp-field · .kp-caret · .kp-send · .kp-btn"),
    demo("kp-theme-light", LAY(
        '<div class="kp-grid" style="inset:0;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr)">'
        + "".join(f'<div class="kp-cell{" sel" if i == 1 else ""}"><div class="kp-cut">Cutout</div>'
                  + (f'<span class="kp-dot corner">{CHECK_SVG}</span>' if i == 1 else "") + '</div>' for i in range(6))
        + '</div>'), "Product picker", ".kp-grid · .kp-cell.sel · .kp-cut · .kp-dot"),
    demo("kp-theme-darkblue", LAY(
        '<div class="kp-venn" style="--vd:min(64cqw,92cqh);--vw:min(100cqw,150cqh)">'
        '<div class="c l" style="--f:var(--k-blue)"></div><div class="c r" style="--f:var(--k-pink)">'
        '<div class="lens" style="--f:var(--k-cream);right:calc(var(--vw) - var(--vd))"></div></div></div>'),
        "Venn", ".kp-venn > .c.l, .c.r > .lens"),
    demo("kp-theme-cream", LAY(
        '<div class="kp-tri" style="--f:var(--k-blue);left:8cqw;right:8cqw;top:8cqh;bottom:8cqh"></div>'
        + f'<div class="kp-a" style="left:50%;top:0;transform:translateX(-50%)">{ICO("db", 150, "Icon")}</div>'
        + f'<div class="kp-a" style="left:0;bottom:0">{ICO("w", 150, "Icon")}</div>'
        + f'<div class="kp-a" style="right:0;bottom:0">{ICO("p", 150, "Icon")}</div>'),
        "Triangle", ".kp-tri · .kp-ico corners"),
    demo("kp-theme-blue", LAY(
        '<div class="kp-a kp-ui" style="left:0;right:0;top:10cqh;gap:34px">'
        '<div class="kp-row"><span class="kp-box on">' + CHECK_SVG + '</span><div class="kp-bar kp-grow"></div><span class="kp-tog on"></span></div>'
        '<div class="kp-row"><span class="kp-radio on"></span><div class="kp-bar kp-grow"></div><span class="kp-tog"></span></div>'
        '<div class="kp-segs"><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i></div></div>',
        '<div class="kp-track"><i class="on"></i><i class="on"></i><i></i><i></i><i></i></div>'),
        "Controls and track", ".kp-box · .kp-radio · .kp-tog · .kp-segs · .kp-track"),
    demo("kp-theme-orange", LAY(
        '<div class="kp-ph lb" style="left:0;top:0;width:100cqw;height:62cqh;border-radius:36px"><span>Photo slot</span></div>'
        '<div class="kp-a kp-ui plate-p" style="left:6cqw;right:6cqw;bottom:0;height:38cqh"></div>'),
        "Photo with a floating card", ".kp-ph · .kp-ui over the photo"),
])

SECTION = f'''<section class="block" id="shapes">
  <div class="wrap">
    <div class="block-head">
      <span class="label">Graphic language · updated 2026-09-28</span>
      <h2>Shapes and interaction, no line graphics</h2>
      <p class="prose muted">The Bounce line graphics are retired: no Super graphic, no dotted and solid support arcs, no carousel seam arcs, no dotted swipe arrow. Katapult does not use them in current creative, and the June 2022 guideline is outdated on this point (account lead review, 2026-09-28). Forward motion now comes from composition: stepping tiles, progress squares, cards that stack and fan, and color blocks that change slide to slide.</p>
      <p class="prose muted">The v2 components rebuild the client's engaging-format references in Katapult's own palette and flat shapes: UI input cards, product pickers, bingo and tic-tac-toe grids, a Venn, a triangle, board-game tracks, checklists, calendars, icon grids, photos with a floating UI card and color-blocked panels. They carry no words of their own. Fields are empty shapes, diagram corners hold icons, and every string on a post is client copy.</p>
    </div>
    <div class="status">
      <div class="status-item"><h3>Slide skeleton</h3><p><code>.kp-v2</code> on the article, then <code>.kp-bg</code> for full-bleed layers and <code>.kp-lay</code> for the safe area: optional <code>.kp-track</code> and logo, <code>.kp-copy</code>, and <code>.kp-stage</code>, which fills the room the copy leaves. Stage pieces are placed in <code>cqw</code>/<code>cqh</code>, so a composition rescales to any copy length. <code>.bl-b</code>, <code>.bl-t</code>, <code>.bl-x</code> and <code>.bl-r</code> let a stage bleed off an edge.</p></div>
      <div class="status-item"><h3>Text on images</h3><p>Never on a photo. Copy that has to sit over a photo goes in a solid White <code>.kp-ui</code> card, in Dark Blue. The card's flat offset plate (<code>.plate-*</code>) gives depth without a shadow or a tint. The logo never sits on a photo.</p></div>
      <div class="status-item"><h3>New grounds</h3><p><code>.kp-theme-blue</code>: White text on Blue (7.55 : 1). <code>.kp-theme-orange</code>: Dark Blue text on Orange (6.13 : 1). Light Blue and Orange appear otherwise only as shapes, photo backgrounds and icon discs, never behind text.</p></div>
      <div class="status-item"><h3>Icon discs</h3><p><code>.kp-ico</code> in the approved icon pairings: <code>t-w</code>, <code>t-s</code>, <code>t-c</code> (Dark Blue icon, Pink accent), <code>t-p</code> (White icon on Pink), <code>t-db</code> (Light Blue icon, Pink accent). The dashed ring marks where the supplied line icon goes.</p></div>
    </div>
    <div class="preview-row">
{DEMOS}
    </div>
  </div>
</section>'''

HANDOFF_ROWS = '''          <tr><td class="mono">.kp-v2 · .kp-bg · .kp-lay · .kp-copy · .kp-stage</td><td>v2 slide skeleton</td><td>Stage fills what the copy leaves, container units inside; .bl-b / .bl-t / .bl-x / .bl-r bleed an edge</td></tr>
          <tr><td class="mono">.kp-ui (.plate-*)</td><td>Solid White UI card, Dark Blue text, flat offset plate</td><td>The only place copy may sit over a photo</td></tr>
          <tr><td class="mono">.kp-field · .kp-caret · .kp-send · .kp-btn</td><td>Empty input field, cursor, send disc, empty button</td><td>No placeholder text, ever</td></tr>
          <tr><td class="mono">.kp-box · .kp-radio · .kp-tog · .kp-segs · .kp-bar</td><td>Checkbox, radio, toggle, progress segments, empty bar</td><td>.on for the selected state (Pink)</td></tr>
          <tr><td class="mono">.kp-track</td><td>Board-game progress squares</td><td>One .on per step, no numbers</td></tr>
          <tr><td class="mono">.kp-join &gt; .kp-li</td><td>One multi-sentence copy line set as stacked rows</td><td>Characters and order unchanged; the text check reads the joined line</td></tr>
          <tr><td class="mono">.kp-grid &gt; .kp-cell (.sel)</td><td>Bingo, tic-tac-toe, icon grid, product picker</td><td>--f cell fill, --gap, --cr radius</td></tr>
          <tr><td class="mono">.kp-pick &gt; .kp-opt · .kp-tiles &gt; .kp-tile</td><td>Story option rows with a cutout thumb; 2x2 priority tiles</td><td>Option text exactly as written</td></tr>
          <tr><td class="mono">.kp-venn · .kp-tri · .kp-fan · .kp-print · .kp-phone · .kp-sh</td><td>Venn, triangle, fanned cards, photo prints, drawn phone, flat shapes</td><td>Palette fills only</td></tr>
          <tr><td class="mono">.kp-ico (t-w, t-s, t-c, t-p, t-db) · .kp-ph · .kp-cut</td><td>Icon disc, photo and cutout placeholders</td><td>Placeholder text is removed with the real asset</td></tr>
          <tr><td class="mono">.kp-theme-blue / -orange</td><td>Two more grounds</td><td>White on Blue; Dark Blue on Orange</td></tr>'''

BOUNCE_SYMS = r"(?:support|super|seam-out|seam-in|seam-start|seam-end|arrow)"

def patch(t):
    n0 = len(t)
    # 1. symbols (with their comment line) out of the defs
    t, n = re.subn(r'\n[ \t]*<!--[^\n]*-->\n[ \t]*<symbol id="k-' + BOUNCE_SYMS + r'".*?</symbol>', "", t, flags=re.S); c1 = n
    t, n = re.subn(r'\n[ \t]*<symbol id="k-' + BOUNCE_SYMS + r'".*?</symbol>', "", t, flags=re.S); c1 += n
    # 2. every use of them (inline svgs), plus the flow hop paths and the icon sample arcs
    t, c2 = re.subn(r'<svg[^>]*>\s*<use href="#k-' + BOUNCE_SYMS + r'"/>\s*</svg>', "", t)
    t, c3 = re.subn(r'<svg viewBox="0 0 920 470".*?</svg>', "", t, flags=re.S)
    t, c4 = re.subn(r'\s*<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M6 38 C[^"]*"[^>]*/><path d="M24 32 C[^"]*"[^>]*/></svg>', "", t)
    t, c4b = re.subn(r'<svg viewBox="0 0 400 300" preserveAspectRatio="none".*?</svg>', "", t, flags=re.S)
    # 3. swipe cue: the word and the arrow go together
    t, c5 = re.subn(r'\s*<p class="kp-swipe">.*?</p>', "", t, flags=re.S)
    # 4. CSS: rules that only style the retired pieces
    css_kill = [r"\.kp-bounce", r"\.kp-super", r"\.kp-seam", r"\.kp-swipe", r"svg\.mast-arc", r"\.kp-flow > svg", r"\.bounce-", r"\.conn\{", r"\.q4-row-bounce"]
    lines, out, c6 = t.split("\n"), [], 0
    for l in lines:
        if not l.startswith("@font-face") and re.search("|".join(css_kill), l) and "{" in l and "<" not in l:
            c6 += 1; continue
        out.append(l)
    t = "\n".join(out)
    t, c7 = re.subn(r";?--kp-bounce:var\(--k-[a-z-]+\)", "", t)
    # 5. insert the v2 CSS once, before the reduced-motion block's closing of the style
    assert "V2 COMPONENTS" not in t
    t = t.replace("\n@media (max-width:640px){", "\n" + V2CSS + "\n@media (max-width:640px){", 1)
    # 6. the Bounce section becomes the shapes section
    t, c8 = re.subn(r'<section class="block" id="bounce">.*?</section>', SECTION, t, count=1, flags=re.S)
    t = t.replace('<li><a href="#bounce">The Bounce</a></li>', '<li><a href="#shapes">Shapes</a></li>')
    # 7. wording that described the Bounce
    rep = {
        "the Bounce, safe zones, four post templates, and nine carousel and Story patterns built to be cloned for the 15-post run.":
            "shapes and interactive components, safe zones, four post templates, and carousel and Story patterns. The Bounce line graphics are retired (2026-09-28).",
        "Logo, CTA fill, pill strokes, the Bounce, pink background variation.": "Logo, CTA fill, pill strokes, selected states, pink background variation.",
        "Logo, pill stroke, Bounce only.": "Logo, pill stroke and shapes only.",
        "Movement, gesture and connection drawn with arrows, arcs and dotted lines. One line weight per icon, matched across a set. Two colors at most.":
            "Line icons: one line weight per icon, matched across a set. Two colors at most.",
        "<h3>The Bounce across slide edges</h3>": "<h3>No line graphics</h3>",
        "Each seam carries one hop: the dotted half closes slide n at the right edge, the solid half opens slide n+1 at the left edge, so every arc stays dotted on its left and solid on its right. The band sits at 1000 to 1170px on every slide so both halves always meet.":
            "Seams, support arcs, the Super graphic and the swipe arrow are retired (2026-09-28). Patterns N1 to N9 below keep their layouts without them; new work builds on the v2 components in the Shapes section.",
        "and every slide of one carousel carries the same theme class, so the swipe reads as one piece.":
            "and a carousel may alternate or color-block themes when it serves the rhythm, as long as the post keeps one stated color rule.",
        "N1 Cover: type-led or photo split, the Bounce leaves through the right edge": "N1 Cover: type-led or photo split",
        "N2 Step: numeral, icon, title, subtext, Bounce in and out": "N2 Step: numeral, icon, title, subtext",
        "N4 Statement: type only, Super graphic across the top": "N4 Statement: type only (retired for carousels, 2026-09-28: every slide needs a visual idea)",
        "N6 Flow: the whole journey on one slide": "N6 Flow: the whole journey on one slide, nodes only",
        "N7 Close: logo, headline, CTA pill, the Bounce lands": "N7 Close: logo, headline, CTA pill",
        "Example carousel: five slides, one theme, one Bounce": "Example carousel: five slides, one theme",
        "Scroll sideways to follow the Bounce across the four seams.": "Scroll sideways.",
        "Copy sits on the bottom safe line; no seam, the Super graphic carries the Bounce.": "Copy sits on the bottom safe line.",
        "Same panel, same weight; the seam joins the pair.": "Same panel, same weight.",
        "Every pattern keeps room for <code>.kp-disclaimer</code> at the bottom safe line, clear of the seam band;": "Every pattern keeps room for <code>.kp-disclaimer</code> at the bottom safe line;",
    }
    miss = [k for k in rep if k not in t]
    for k, v in rep.items():
        t = t.replace(k, v)
    # handoff rows that describe retired pieces, then the v2 rows
    t = re.sub(r'\n[ \t]*<tr><td class="mono">\.kp-seam--in / --out</td>.*?</tr>', "", t)
    t = t.replace("<td>Subtext body, swipe cue, icon placeholder</td><td>Body 36px on 4:5, 38px on 9:16, Light. Swipe cue uses #k-arrow</td>",
                  "<td>Subtext body, icon placeholder</td><td>Body 36px on 4:5, 38px on 9:16, Light</td>")
    t = t.replace('<td class="mono">.kp-text / .kp-swipe / .kp-icon-slot</td>', '<td class="mono">.kp-text / .kp-icon-slot</td>')
    t = t.replace("\n        </tbody>", "\n" + HANDOFF_ROWS + "\n        </tbody>", 1)
    # remaining seam / bounce mentions in the handoff code samples
    t = re.sub(r'\n&lt;svg class="kp-(?:bounce|seam)[^\n]*', "", t)
    t = re.sub(r'\n  &lt;svg class="kp-(?:bounce|seam)[^\n]*', "", t)
    return t, dict(syms=c1, uses=c2, flow=c3, iconarcs=c4 + c4b, swipe=c5, css=c6, tokens=c7, section=c8, missing=miss)

for f in FILES:
    t = io.open(f, encoding="utf-8").read()
    t2, stats = patch(t)
    io.open(f, "w", encoding="utf-8", newline="\n").write(t2)
    print(os.path.basename(os.path.dirname(f)) or "", os.path.basename(f), stats)
