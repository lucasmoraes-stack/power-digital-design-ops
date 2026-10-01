"""Review pages for the owner (published as Artifacts).

  ad-kit.html     Truly Nolen ad design system, read from the delivered pieces
                  (Figma 216:656) plus the new components this brief adds.
  spotlight.html  The 28 deliverables of the 2026 Core-4 BOF brief: 14 statics
                  and the 3-scene storyboard of each MOBITE/HTML5 iteration.

  python review.py   -> writes both into _build/review/
"""
import base64
from build import (BUILD, BRAND, COPY, SIZES, FRAMES, PIECE_CSS, BASIC, YELLOW, RED,
                   font_face, logo_uri, piece_html, name, LOGO_RATIO)

OUTDIR = BUILD / "review"
FLAT_SVG = BRAND / "01-brand" / "identity" / "assets" / "tn-logo-flat.svg"
LATIN1 = "".join(chr(c) for c in range(0xC0, 0x100))
FIGMA = "https://www.figma.com/design/D8FpNuKI3uPGjCPqonIn3C/Progressive-Global---LAB?node-id=216-656"

PAGE_CSS = """
/* Layout: one reading column that widens for the ad sheets; the pieces sit on a warm near-black ground like a light table */
:root{
  --ground:#12110C; --panel:#1B1912; --line:#2F2C20; --ink:#F3F0E4; --muted:#A8A28A;
  --yellow:#FFE300; --red:#ED2524;
  --display:'TN Display','Arial Black',Impact,sans-serif;
  --body:'TN Medium',Futura,'Century Gothic','Trebuchet MS',sans-serif;
  --heavy:'TN Heavy',Futura,'Century Gothic','Trebuchet MS',sans-serif;
  color-scheme:dark;
}
html{background:var(--ground)}
body{background:var(--ground);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.55;padding-inline:clamp(16px,4vw,48px);padding-block:40px 80px}
.wrap{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:64px}
h1,h2,h3{margin:0;text-wrap:balance}
h1{font-family:var(--display);font-weight:400;text-transform:uppercase;font-size:clamp(44px,7vw,84px);line-height:.86;letter-spacing:-.01em}
h1 em{font-style:normal;color:var(--yellow)}
h2{font-family:var(--display);font-weight:400;text-transform:uppercase;font-size:clamp(28px,3.6vw,40px);line-height:.9;color:var(--yellow)}
h3{font-family:var(--heavy);font-weight:400;font-size:17px;line-height:1.3}
p{margin:0;max-width:65ch}
.lede{color:var(--muted);font-size:18px}
.eyebrow{font-family:var(--heavy);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
a{color:var(--yellow)}
a:focus-visible,button:focus-visible,input:focus-visible+label{outline:2px solid var(--yellow);outline-offset:3px}
code,.mono{font-family:ui-monospace,'Cascadia Mono',Consolas,monospace;font-size:13px}
.head{display:flex;gap:28px;align-items:flex-end;flex-wrap:wrap}
.head img{width:92px;height:auto}
.head .t{display:flex;flex-direction:column;gap:14px;flex:1;min-width:260px}
.meta{display:flex;flex-wrap:wrap;gap:8px 18px;color:var(--muted);font-size:14px}
section{display:flex;flex-direction:column;gap:22px}
.sec-head{display:flex;flex-direction:column;gap:8px;border-top:1px solid var(--line);padding-top:22px}
.grid{display:grid;gap:18px}
.g2{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.g4{grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}
.note{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px;display:flex;flex-direction:column;gap:6px}
.note .k{font-family:var(--heavy);font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--yellow)}
.note p{color:var(--ink);font-size:15px}
.note p+p{color:var(--muted)}
ul.rules{margin:0;padding-left:1.1em;display:flex;flex-direction:column;gap:8px;max-width:75ch}
ul.rules li::marker{color:var(--yellow)}
.fit{position:relative;overflow:hidden;max-width:100%}
.fit>.tn{position:absolute;left:0;top:0;transform-origin:0 0}
.piece{display:flex;flex-direction:column;gap:8px}
.cap-row{display:flex;justify-content:space-between;gap:12px;font-size:13px;color:var(--muted);flex-wrap:wrap}
.cap-row b{font-family:var(--heavy);font-weight:400;color:var(--ink)}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
"""

FIT_JS = """<script>
function fitAll(){document.querySelectorAll('.fit').forEach(function(el){
  var w=+el.dataset.w,h=+el.dataset.h,s=Math.min(1,el.clientWidth/w);
  el.style.height=(h*s)+'px';el.firstElementChild.style.transform='scale('+s+')';});}
window.addEventListener('resize',fitAll);document.fonts&&document.fonts.ready.then(fitAll);fitAll();
</script>"""

def fit(size, var, maxw, frame=None, extra=""):
    cfg = SIZES[size]
    return (f'<div class="fit" data-w="{cfg["W"]}" data-h="{cfg["H"]}" style="width:{maxw}px">'
            f'{piece_html(size, var, "__LOGO__", frame, extra)}</div>')

def small_logo():
    from PIL import Image
    import io
    im = Image.open(BRAND / "01-brand" / "identity" / "assets" / "tn-logo-sticker.png")
    im = im.resize((208, 260), Image.LANCZOS); buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def page(title, body, fonts):
    body = body.replace('src="__LOGO__"', 'src="data:," data-l')
    return f"""<title>{title}</title>
<style>{fonts}
{PIECE_CSS}
{PAGE_CSS}</style>
<div class="wrap">{body}</div>
<script>var TNL="{small_logo()}";document.querySelectorAll('img[data-l]').forEach(function(i){{i.src=TNL}});</script>
{FIT_JS}"""

# =============================================================================
def ad_kit(fonts):
    flat = "data:image/svg+xml;base64," + base64.b64encode(FLAT_SVG.read_bytes()).decode()
    sticker = logo_uri()
    sw = lambda hexv, nm, role, dark=False: (
        f'<div class="sw"><div class="chip" style="background:{hexv};{"box-shadow:inset 0 0 0 1px var(--line);" if dark else ""}"></div>'
        f'<div class="sw-t"><b>{nm}</b><span class="mono">{hexv}</span><p>{role}</p></div></div>')
    css = """
.sw{display:flex;flex-direction:column;gap:12px}
.sw .chip{height:120px;border-radius:10px}
.sw-t{display:flex;flex-direction:column;gap:4px}.sw-t b{font-family:var(--heavy);font-weight:400}
.sw-t .mono{color:var(--muted)}.sw-t p{font-size:14px;color:var(--muted)}
.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.demo{border-radius:10px;padding:28px 26px;display:flex;flex-direction:column;gap:18px;align-items:flex-start}
.demo.y{background:var(--yellow);color:#000}.demo.k{background:#000;color:#fff;box-shadow:inset 0 0 0 1px var(--line)}
.demo .hl{font-family:var(--display);text-transform:uppercase;font-size:clamp(40px,5vw,56px);line-height:.8;letter-spacing:-.01em}
.demo.y .hl em{font-style:normal;color:var(--red)}.demo.k .hl{color:var(--yellow)}.demo.k .hl em{font-style:normal;color:#fff}
.demo .sb{font-family:var(--body);font-size:18px;line-height:1.2}
.demo .pill{font-family:var(--heavy);font-size:17px;border-radius:999px;height:2.4em;padding:0 1.6em;display:inline-flex;align-items:center}
.demo.y .pill{background:#000;color:#fff}.demo.k .pill{background:var(--yellow);color:#000}
.demo .tag{font-family:var(--heavy);font-size:11px;letter-spacing:.12em;text-transform:uppercase;opacity:.6}
.type-row{display:grid;grid-template-columns:minmax(150px,220px) 1fr;gap:18px;align-items:baseline;border-bottom:1px solid var(--line);padding-block:18px}
.type-row .spec{display:flex;flex-direction:column;gap:2px;font-size:13px;color:var(--muted)}
.type-row .spec b{font-family:var(--heavy);font-weight:400;color:var(--ink);font-size:15px}
.s-disp{font-family:var(--display);text-transform:uppercase;font-size:clamp(40px,6vw,72px);line-height:.8;letter-spacing:-.01em;color:var(--yellow)}
.s-med{font-family:var(--body);font-size:28px;line-height:1.15}
.s-hvy{font-family:var(--heavy);font-size:24px}
@media (max-width:560px){.type-row{grid-template-columns:1fr}}
.logos{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}
.logo-card{border-radius:10px;padding:26px;display:flex;gap:22px;align-items:center}
.logo-card img{height:150px;width:auto}
.logo-card .t{display:flex;flex-direction:column;gap:6px;font-size:14px}
.logo-card .t b{font-family:var(--heavy);font-weight:400;font-size:15px}
.lc-y{background:var(--yellow);color:#000}.lc-k{background:#000;color:#fff;box-shadow:inset 0 0 0 1px var(--line)}
.lc-k .t span{color:var(--muted)}
.pat{display:flex;flex-direction:column;gap:10px}
.pat .fig{background:var(--panel);border:1px solid var(--line);border-radius:10px;height:190px;display:flex;align-items:center;justify-content:center;padding:18px}
.wf{background:var(--yellow);position:relative;border-radius:3px;overflow:hidden}
.wf i{position:absolute;display:block;background:#000;border-radius:2px}
.wf i.p{background:#000;border-radius:99px}.wf i.ph{background:#6d6a58;border-radius:0}.wf i.lg{background:var(--red);border-radius:50% 50% 40% 40%}
.pat p{font-size:14px;color:var(--muted)}
.sizes{width:100%;border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums}
.sizes th,.sizes td{text-align:left;padding:10px 12px;border-bottom:1px solid var(--line)}
.sizes th{font-family:var(--heavy);font-weight:400;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.tbl{overflow-x:auto}
.new{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}
.new .card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px;display:flex;flex-direction:column;gap:12px}
.new .card p{font-size:14px;color:var(--muted)}
.pests{display:flex;gap:14px}
.pests svg{flex:1;min-width:0;height:auto;background:var(--yellow);border-radius:8px;padding:10px}
"""
    from build import PESTS, PEST_VB
    vw, vh, fy = PEST_VB
    pest_svg = lambda k: f'<svg viewBox="-10 -10 {vw+20} {vh+20}" role="img" aria-label="{k}">{PESTS[k]}<rect x="-10" y="{fy+2}" width="{vw+20}" height="3" fill="#000" fill-opacity=".2"/></svg>'
    body = f"""
<header class="head"><img src="{sticker}" alt="Truly Nolen" width="92" height="115">
<div class="t"><span class="eyebrow">Design system de mídia paga</span>
<h1>Truly Nolen <em>Ad Kit</em></h1>
<p class="lede">O que as peças já entregues da marca repetem, peça por peça, virou regra aqui. É a base de todo criativo novo de Meta e programática, a começar pelo BOF $50 OFF.</p>
<div class="meta"><span>Fonte: <a href="{FIGMA}">Figma LAB, node 216:656</a></span><span>26 peças lidas: TN26014, TN26016, TN26017, TN26020, TN26021</span><span>Levantado em 29/09/2026</span></div></div></header>

<section><div class="sec-head"><span class="eyebrow">Cor</span><h2>Amarelo, preto e um vermelho que só aparece no amarelo</h2></div>
<div class="grid g4">
{sw(YELLOW, "Amarelo Truly", "Fundo principal e a cor da oferta quando o fundo é preto.")}
{sw("#000000", "Preto", "Fundo alternativo, texto sobre amarelo, pílula do CTA no amarelo.", True)}
{sw(RED, "Vermelho", "Só a palavra de destaque do headline sobre amarelo. Nunca fundo, nunca no preto.")}
{sw("#FFFFFF", "Branco", "Palavra de destaque sobre preto, texto do CTA na pílula preta.")}
</div></section>

<section><div class="sec-head"><span class="eyebrow">Os dois fundos</span><h2>Cada fundo tem seu par de cores</h2>
<p class="lede">O headline sempre tem duas cores. A segunda cor marca o final da frase, que é a virada da mensagem.</p></div>
<div class="pair">
<div class="demo y"><span class="tag">Fundo amarelo</span><div class="hl">Arizona pests? <em>We’re on it.</em></div><span class="pill">Book an inspection</span></div>
<div class="demo k"><span class="tag">Fundo preto</span><div class="sb" style="color:var(--yellow)">Every Home Has Rules.</div><div class="hl">Pests ignore them <em>all.</em></div><span class="pill">Book an inspection</span></div>
</div></section>

<section><div class="sec-head"><span class="eyebrow">Tipografia</span><h2>Três pesos, cada um com uma função</h2></div>
<div>
<div class="type-row"><div class="spec"><b>Futura Display BQ</b><span>Headline e oferta. Caixa alta, entrelinha 0.8, tracking −1%.</span></div><div class="s-disp">Show them the door</div></div>
<div class="type-row"><div class="spec"><b>Futura Std Medium</b><span>Linha de apoio e eyebrow. Caixa normal, entrelinha 1.2.</span></div><div class="s-med">Truly Nolen helps take back your home from unwanted pests.</div></div>
<div class="type-row"><div class="spec"><b>Futura Std Heavy</b><span>Só o CTA. Tracking −1%.</span></div><div class="s-hvy">Book an inspection</div></div>
</div></section>

<section><div class="sec-head"><span class="eyebrow">Logo</span><h2>Duas versões, escolhidas pelo fundo</h2></div>
<div class="logos">
<div class="logo-card lc-y"><img src="{flat}" alt="Logo Truly Nolen, versão chapada" height="150" width="107"><div class="t"><b>Chapado</b><span>Em fundo amarelo liso. Centralizado acima do headline nos formatos verticais.</span></div></div>
<div class="logo-card lc-k"><img src="{sticker}" alt="Logo Truly Nolen, versão adesivo" height="150" width="{150*LOGO_RATIO:.0f}"><div class="t"><b>Adesivo</b><span>Com a borda amarela. Em fundo preto ou foto, geralmente no canto inferior direito.</span></div></div>
</div></section>

<section><div class="sec-head"><span class="eyebrow">Composição</span><h2>Três arranjos cobrem todos os tamanhos</h2></div>
<div class="grid g3">
<div class="pat"><div class="fig"><div class="wf" style="width:84px;height:150px"><i class="lg" style="left:36px;top:12px;width:12px;height:16px"></i><i style="left:12px;top:38px;width:60px;height:9px"></i><i style="left:18px;top:51px;width:48px;height:9px"></i><i class="p" style="left:16px;top:68px;width:52px;height:9px"></i><i class="ph" style="left:0;top:92px;width:84px;height:58px"></i></div></div>
<h3>Pilha centralizada</h3><p>9:16 e 300x600. Logo, headline, apoio e CTA empilhados no centro. Foto ou ilustração ocupa a base.</p></div>
<div class="pat"><div class="fig"><div class="wf" style="width:130px;height:130px"><i class="lg" style="left:10px;top:10px;width:12px;height:16px"></i><i style="left:10px;top:44px;width:48px;height:12px"></i><i style="left:10px;top:60px;width:40px;height:12px"></i><i class="p" style="left:10px;top:86px;width:44px;height:9px"></i><i class="ph" style="left:65px;top:0;width:65px;height:130px"></i></div></div>
<h3>Divisão texto e imagem</h3><p>1:1, 1600x600 e 300x250. Metade texto, metade imagem, ou faixa de texto em cima e foto embaixo.</p></div>
<div class="pat"><div class="fig"><div class="wf" style="width:200px;height:26px"><i class="lg" style="left:6px;top:4px;width:14px;height:18px"></i><i style="left:28px;top:7px;width:70px;height:12px"></i><i class="p" style="left:126px;top:8px;width:64px;height:10px"></i></div></div>
<h3>Faixa</h3><p>728x90 e 320x50. Logo, headline e CTA da esquerda pra direita. O apoio sai.</p></div>
</div></section>

<section><div class="sec-head"><span class="eyebrow">Tamanhos</span><h2>A grade padrão de entregas</h2></div>
<div class="tbl"><table class="sizes"><thead><tr><th>Plataforma</th><th>Formato</th><th>Export</th><th>Observação</th></tr></thead><tbody>
<tr><td>Meta</td><td>1:1</td><td>1440 × 1440</td><td>Feed</td></tr>
<tr><td>Meta</td><td>9:16</td><td>1440 × 2560</td><td>Stories e Reels. Texto fora dos 14% de cima e dos 35% de baixo</td></tr>
<tr><td>Programática</td><td>300x600 · 300x250 · 1600x600</td><td>1×</td><td>Com linha de apoio</td></tr>
<tr><td>Programática</td><td>728x90 · 320x50</td><td>1×</td><td>Sem linha de apoio</td></tr>
</tbody></table></div></section>

<section><div class="sec-head"><span class="eyebrow">Novo neste briefing</span><h2>Componentes que o BOF $50 OFF acrescenta</h2>
<p class="lede">Entram no kit porque vão se repetir nas próximas iterações de oferta.</p></div>
<div class="new">
<div class="card"><h3>Lockup da oferta</h3>{fit_lockup()}<p>O $50 é o maior elemento da peça. $ pequeno no topo, OFF e o serviço empilhados na altura exata do número. OFF segue o amarelo e o serviço vai em branco.</p></div>
<div class="card"><h3>Holofote</h3>{fit_spot()}<p>Círculo amarelo com borda suave, feixe fraco vindo de fora do quadro e uma linha de chão. A praga é preta, então fica invisível fora da luz.</p></div>
<div class="card"><h3>Silhuetas de praga</h3><div class="pests">{pest_svg("rat")}{pest_svg("roach")}</div><p>Vetor próprio, de perfil, virado pra esquerda. Rato no V1 (roedores), barata no V2 (insetos).</p></div>
</div></section>

<section><div class="sec-head"><span class="eyebrow">Regras</span><h2>O que não muda</h2></div>
<ul class="rules">
<li>O CTA é sempre “Book an inspection”, em pílula, e a pílula contrasta com o fundo.</li>
<li>Vermelho só aparece no amarelo, e só na palavra de destaque.</li>
<li>Headline em caixa alta na Futura Display BQ. Apoio em caixa normal.</li>
<li>Nenhum travessão ou meia-risca na copy.</li>
<li>Faixas pequenas (728x90, 320x50) perdem a linha de apoio antes de perder tamanho de headline.</li>
<li>Nos arquivos do Figma, os frames 1x1 e 9x16 do TN26021 estão com os nomes trocados. Na nomenclatura nova, o nome segue a proporção real.</li>
</ul></section>
"""
    return page("Truly Nolen Ad Kit", body, fonts).replace("</style>", css + "</style>", 1)

def fit_lockup():
    cfg = SIZES["300x250"]
    cp = COPY["V1"]
    stack = "".join(f'<span class="cap{" w" if i else ""}"><i>{t}</i></span>' for i, t in enumerate(cp["stack"]))
    return ('<div class="tn" style="width:100%;height:150px;border-radius:8px;display:flex;align-items:center;justify-content:center">'
            '<div class="offer" style="position:relative;font-size:130px">'
            f'<span class="cap dol"><i>$</i></span><span class="cap num"><i>50</i></span><span class="stk">{stack}</span></div></div>')

def fit_spot():
    return f'<div style="border-radius:8px;overflow:hidden">{fit("300x250", "V1", 600, FRAMES[2], "kit")}</div>'

# =============================================================================
DISPLAY = {"1080x1080": 420, "1080x1920": 236, "300x600": 210, "300x250": 300,
           "1600x600": 1120, "728x90": 728, "320x50": 320}
LABEL = {"1080x1080": "Meta 1:1", "1080x1920": "Meta 9:16", "300x600": "300x600", "300x250": "300x250",
         "1600x600": "1600x600", "728x90": "728x90", "320x50": "320x50"}

def spotlight(fonts):
    css = """
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font-family:var(--heavy);font-size:13px;border:1px solid var(--line);border-radius:999px;padding:6px 12px;color:var(--ink)}
.chip.y{background:var(--yellow);border-color:var(--yellow);color:#000}
.nav{display:flex;flex-wrap:wrap;gap:10px 22px;font-family:var(--heavy);font-size:14px}
.flags{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.sheet{display:flex;flex-wrap:wrap;gap:28px 24px;align-items:flex-end}
.sheet .piece{max-width:100%}
.guides{position:absolute;inset:0;pointer-events:none;display:none}
.guides i{position:absolute;left:0;right:0;background:repeating-linear-gradient(45deg,rgba(237,37,36,.30) 0 6px,rgba(237,37,36,.12) 6px 12px);border:0 dashed var(--red)}
.guides i.t{top:0;height:14%;border-bottom-width:2px}.guides i.b{bottom:0;height:35%;border-top-width:2px}
body.sz .guides{display:block}
.toggle{display:flex;align-items:center;gap:10px;font-size:14px;color:var(--muted)}
.toggle input{accent-color:var(--yellow);width:18px;height:18px}
.legend{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.legend .note .n{font-family:var(--display);font-size:34px;line-height:.8;color:var(--yellow)}
.sb-row{display:flex;flex-direction:column;gap:10px;padding-block:18px;border-top:1px solid var(--line)}
.sb-row .scenes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;align-items:start}
.sb-row .scene{display:flex;flex-direction:column;gap:6px}
.sb-row .scene>span{font-size:12px;color:var(--muted);font-family:var(--heavy);letter-spacing:.08em;text-transform:uppercase}
.files{font-size:14px;color:var(--muted);display:flex;flex-direction:column;gap:6px}
@media (max-width:640px){.legend{grid-template-columns:1fr}.sb-row .scenes{gap:8px}}
"""
    def static_sheet(var):
        out = []
        for size in SIZES:
            cfg = SIZES[size]; w = DISPLAY[size]
            g = '<div class="guides"><i class="t"></i><i class="b"></i></div>' if size == "1080x1920" else ""
            px = "1440 × 2560" if size == "1080x1920" else ("1440 × 1440" if size == "1080x1080" else size.replace("x", " × "))
            html = fit(size, var, w)
            if g:
                html = html[:-6] + g + "</div>"
            out.append(f'<div class="piece" style="width:{w}px"><div class="cap-row"><b>{LABEL[size]}</b><span class="mono">{px}</span></div>{html}</div>')
        return '<div class="sheet">' + "".join(out) + "</div>"

    def storyboard(var):
        rows = []
        for size in SIZES:
            cfg = SIZES[size]
            maxw = min(cfg["W"], int(300 * cfg["W"] / cfg["H"]), 380)
            scenes = "".join(f'<div class="scene">{fit(size, var, maxw, fr, "sb")}<span>{fr["id"]} · {fr["title"]}</span></div>' for fr in FRAMES)
            rows.append(f'<div class="sb-row"><div class="cap-row"><b>{LABEL[size]}</b><span class="mono">{name(size, var, "anim")}</span></div><div class="scenes">{scenes}</div></div>')
        return "".join(rows)

    legend = "".join(f'<div class="note"><span class="n">{fr["id"]}</span><span class="k">{fr["title"]}</span><p>{fr["note"]}</p></div>' for fr in FRAMES)

    blocks = []
    for var, label, pestpt in (("V1", "V1 · Roedores", "rato"), ("V2", "V2 · Insetos", "barata")):
        cp = COPY[var]
        blocks.append(f"""
<section id="{var.lower()}-static"><div class="sec-head"><span class="eyebrow">{label} · Estático</span>
<h2>$50 Off {cp['stack'][1]} Control</h2><p class="lede">Praga já pega no feixe ({pestpt}). 7 tamanhos, PNG.</p></div>
{static_sheet(var)}</section>
<section id="{var.lower()}-story"><div class="sec-head"><span class="eyebrow">{label} · MOBITE / HTML5</span>
<h2>Storyboard em 3 cenas</h2><p class="lede">Mesmo layout do estático, montado em etapas. A cena 03 é o quadro final.</p></div>
{storyboard(var)}</section>""")

    body = f"""
<header class="head"><img src="{logo_uri()}" alt="Truly Nolen" width="92" height="115">
<div class="t"><span class="eyebrow">Truly Nolen · 2026 Core-4 · BOF</span>
<h1>Spotlight <em>$50 Off</em></h1>
<p class="lede">Iteração do anúncio de oferta top performer com layout novo: fundo preto, o $50 como maior foco e um holofote amarelo que encontra a praga. Teste de copy e praga entre V1 (roedores) e V2 (insetos).</p>
<div class="chips"><span class="chip y">28 entregas</span><span class="chip">14 estáticos</span><span class="chip">14 storyboards MOBITE/HTML5</span><span class="chip">Meta 1:1 · 9:16</span><span class="chip">300x600 · 300x250 · 1600x600 · 728x90 · 320x50</span></div></div></header>

<nav class="nav" aria-label="Seções"><a href="#check">Pra confirmar</a><a href="#v1-static">V1 estático</a><a href="#v1-story">V1 storyboard</a><a href="#v2-static">V2 estático</a><a href="#v2-story">V2 storyboard</a><a href="#files">Arquivos</a></nav>

<section id="check"><div class="sec-head"><span class="eyebrow">Antes de aprovar</span><h2>Pontos pra confirmar</h2></div>
<div class="flags">
<div class="note"><span class="k">Subhead do V2</span><p>O briefing repete “Rodents can’t hide from us” no V2, que é o de insetos.</p><p>Usei como está no briefing. A referência top performer do V2 usa “We’ll spot any bug.” Troco se for o caso.</p></div>
<div class="note"><span class="k">Código do job</span><p>Os arquivos estão como TN-BOF-Core4, sem número TN26xxx.</p><p>Me passa o código que eu renomeio tudo de uma vez.</p></div>
<div class="note"><span class="k">Faixas pequenas</span><p>728x90 e 320x50 saem sem o subhead, como nas peças já entregues.</p><p>Oferta, praga e CTA ficam.</p></div>
<div class="note"><span class="k">Safe zone Meta</span><p>No 9:16 todo o texto está entre os 14% de cima e os 35% de baixo.</p><p><span class="toggle"><input type="checkbox" id="sz"><label for="sz">Mostrar as faixas no 9:16</label></span></p></div>
</div></section>

<section><div class="sec-head"><span class="eyebrow">Como o storyboard monta</span><h2>As 3 cenas</h2></div><div class="legend">{legend}</div></section>
{"".join(blocks)}

<section id="files"><div class="sec-head"><span class="eyebrow">Arquivos</span><h2>Onde está cada entrega</h2></div>
<div class="files"><span class="mono">clients/truly-nolen/04-deliverables/banners/2026-core4-bof/static/</span><span>14 PNGs. Meta em 1440 px, programática em 1×.</span>
<span class="mono">clients/truly-nolen/04-deliverables/banners/2026-core4-bof/storyboard/&lt;peça&gt;/frame-01..03.png</span><span>3 cenas por peça animada, 42 PNGs.</span>
<span class="mono">clients/truly-nolen/03-work/banners/2026-core4-bof/build.py</span><span>Gera tudo de novo a partir de uma tabela de layout por tamanho.</span></div></section>
<script>document.getElementById('sz').addEventListener('change',function(e){{document.body.classList.toggle('sz',e.target.checked)}});</script>
"""
    return page("Spotlight $50 Off", body, fonts).replace("</style>", css + "</style>", 1)

if __name__ == "__main__":
    OUTDIR.mkdir(parents=True, exist_ok=True)
    fonts = font_face(BASIC + LATIN1 + "−×")
    (OUTDIR / "ad-kit.html").write_text(ad_kit(fonts), encoding="utf-8")
    (OUTDIR / "spotlight.html").write_text(spotlight(fonts), encoding="utf-8")
    for f in ("ad-kit.html", "spotlight.html"):
        print(f, round((OUTDIR / f).stat().st_size / 1024), "KB")
