"""Review page for the owner (published as an Artifact): the 6 deliverables of the
Mosquito Season concept as 5-scene storyboards, with copy, motion notes, safe zones
and the photo slots still waiting for plates.

  python review.py   -> _build/review/mosquito.html  (run build.py --png first)
"""
import base64, io, re
from PIL import Image
from build import (BUILD, OUT, BRAND, VERSIONS, SIZES, SHOTS, BASIC, font_face, piece_name, plate)

OUTDIR = BUILD / "review"
LATIN1 = "".join(chr(c) for c in range(0xC0, 0x100))

PAGE_CSS = """
/* Layout: one reading column; the frames sit on a warm near-black light table, as in the BOF review. Single dark world by choice. */
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
.wrap{max-width:1240px;margin:0 auto;display:flex;flex-direction:column;gap:64px}
h1,h2,h3{margin:0;text-wrap:balance;font-weight:400}
h1{font-family:var(--display);text-transform:uppercase;font-size:clamp(44px,7vw,84px);line-height:.86;letter-spacing:-.01em}
h1 em{font-style:normal;color:var(--yellow)}
h2{font-family:var(--display);text-transform:uppercase;font-size:clamp(28px,3.6vw,40px);line-height:.9;color:var(--yellow)}
h3{font-family:var(--heavy);font-size:17px;line-height:1.3}
p{margin:0;max-width:68ch}
.lede{color:var(--muted);font-size:18px}
.eyebrow{font-family:var(--heavy);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.head{display:flex;gap:28px;align-items:flex-end;flex-wrap:wrap}
.head img{width:92px;height:auto}
.head .t{display:flex;flex-direction:column;gap:14px;flex:1;min-width:260px}
.meta{display:flex;flex-wrap:wrap;gap:8px 18px;color:var(--muted);font-size:14px}
section{display:flex;flex-direction:column;gap:22px}
.sec-head{display:flex;flex-direction:column;gap:8px;border-top:1px solid var(--line);padding-top:22px}
.sec-head .row{display:flex;gap:14px;align-items:baseline;flex-wrap:wrap}
.tag{font-family:var(--heavy);font-size:12px;letter-spacing:.1em;text-transform:uppercase;background:var(--yellow);color:#000;border-radius:999px;padding:3px 10px 1px}
.tabs{display:flex;gap:8px;flex-wrap:wrap}
.tabs button{font:inherit;font-family:var(--heavy);font-size:14px;background:transparent;color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:6px 16px;cursor:pointer}
.tabs button[aria-pressed=true]{background:var(--yellow);color:#000;border-color:var(--yellow)}
.toolbar{display:flex;gap:18px;align-items:center;flex-wrap:wrap;justify-content:space-between}
.toggle{display:flex;gap:8px;align-items:center;font-size:14px;color:var(--muted);cursor:pointer}
.toggle input{accent-color:var(--yellow);width:16px;height:16px}
.strip{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:14px}
@media (max-width:860px){.strip{grid-template-columns:repeat(2,minmax(0,1fr))}}
.frame{display:flex;flex-direction:column;gap:10px;min-width:0}
.frame .n{display:flex;gap:8px;align-items:center;font-family:var(--display);text-transform:uppercase;font-size:20px;line-height:1}
.frame .n b{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;background:var(--ink);color:var(--ground);font-family:var(--heavy);font-weight:400;font-size:13px;flex:none}
.shot{position:relative;border-radius:6px;overflow:hidden;background:#000}
.shot img{display:block;width:100%;height:auto}
.shot .safe{position:absolute;inset:0;pointer-events:none;display:none}
.show-safe .shot .safe{display:block}
.safe i{position:absolute;left:0;right:0;background:repeating-linear-gradient(45deg,rgba(237,37,36,.34) 0 6px,rgba(237,37,36,.14) 6px 12px)}
.safe .s{top:0;bottom:0;width:6%;left:auto;right:auto}
.frame .copy{font-size:14px;line-height:1.35}
.frame .mo{font-size:13px;line-height:1.4;color:var(--muted)}
.frame .ph{font-size:12px;font-family:var(--heavy);letter-spacing:.06em;text-transform:uppercase;color:var(--yellow)}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}
.note{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px;display:flex;flex-direction:column;gap:6px}
.note .k{font-family:var(--heavy);font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--yellow)}
.note p{font-size:15px}
.note p+p{color:var(--muted)}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;min-width:720px;font-size:14px}
th,td{text-align:left;vertical-align:top;padding:12px 14px;border-bottom:1px solid var(--line)}
th{font-family:var(--heavy);font-weight:400;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
tr:last-child td{border-bottom:0}
code,.mono{font-family:ui-monospace,'Cascadia Mono',Consolas,monospace;font-size:13px}
.st{font-family:var(--heavy);font-size:12px;border-radius:999px;padding:2px 9px 1px;white-space:nowrap}
.st.wait{background:#3a2f12;color:var(--yellow)}.st.ok{background:#16341c;color:#9fe2a9}
button:focus-visible,input:focus-visible{outline:2px solid var(--yellow);outline-offset:3px}
"""

def thumb(png, w):
    im = Image.open(png).convert("RGB")
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=80, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def safe_overlay(ratio):
    if ratio != "9x16":
        return ""
    return ('<div class="safe"><i style="top:0;height:14%"></i><i style="bottom:0;height:35%"></i>'
            '<i class="s" style="left:0"></i><i class="s" style="right:0"></i></div>')

def text(sc):
    if sc["kind"] == "end":
        return f'{sc["hl"]} <b>[{sc["cta"]}]</b>'.replace("<em>", "").replace("</em>", "")
    parts = [sc.get("eyebrow"), sc.get("hl"), sc.get("hl2"), sc.get("sub")]
    return re.sub("</?em>", "", " / ".join(p for p in parts if p))

def version_section(var, v):
    blocks = []
    for ratio in SIZES:
        frames = []
        for i, sc in enumerate(v["scenes"], 1):
            png = OUT / "storyboard" / piece_name(var, ratio) / f"{piece_name(var, ratio)}-S{i:02d}.png"
            ph = ""
            if sc["kind"] == "photo":
                own, si = plate(sc["shot"], ratio, own=True), SHOTS[sc["shot"]].get("stand_in")
                state = "" if own else (f" (provisória: {si})" if si and plate(si, ratio) else " (pendente)")
                ph = f'<span class="ph">Foto: {sc["shot"]}{state}</span>'
            frames.append(f'''<div class="frame"><div class="n"><b>{i}</b>{sc["title"]}</div>
<div class="shot"><img src="{thumb(png, 300 if ratio == "9x16" else 320)}" alt="Cena {i} de {var} em {ratio}" loading="lazy">{safe_overlay(ratio)}</div>
<p class="copy">{text(sc)}</p><p class="mo">{sc["motion"]}</p>{ph}</div>''')
        blocks.append(f'<div class="rs" data-ratio="{ratio}"{" hidden" if ratio != "9x16" else ""}>'
                      f'<div class="strip">{"".join(frames)}</div>'
                      f'<p class="mono" style="color:var(--muted)">{piece_name(var, ratio)}</p></div>')
    return f'''<section id="{var}"><div class="sec-head"><div class="row"><span class="tag">{var}</span><h2>{v["angle"]}</h2></div></div>
{"".join(blocks)}</section>'''

def shots_table():
    uses = {}
    for var, v in VERSIONS.items():
        for i, sc in enumerate(v["scenes"], 1):
            if sc.get("shot"):
                uses.setdefault(sc["shot"], []).append(f"{var} S{i:02d}")
    rows = []
    for shot, meta in SHOTS.items():
        ok = plate(shot, "9x16", own=True)
        st = "Recebida" if ok else (f"Faltando, usando {meta['stand_in']}" if meta.get("stand_in") else "Aguardando")
        rows.append(f'<tr><td class="mono">img/{shot}.png</td><td>{meta["label"]}</td><td>{", ".join(uses.get(shot, []))}</td>'
                    f'<td><span class="st {"ok" if ok else "wait"}">{st}</span></td></tr>')
    return "".join(rows)

def main():
    fonts = font_face(BASIC + LATIN1)
    im = Image.open(BRAND / "01-brand" / "identity" / "assets" / "tn-logo-sticker.png"); im = im.resize((184, round(im.height * 184 / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True); logo = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    body = f'''
<header class="head"><img src="{logo}" alt="Truly Nolen">
<div class="t"><span class="eyebrow">Truly Nolen · 2026 Core-4 · Meta Motion Graphics</span>
<h1>Mosquito <em>Season</em></h1>
<p class="lede">PC Platinum / Mosquito Season Starts Now. Três ângulos de mensagem (V1 Outcome, V2 Problem, V3 Service) em 1:1 e 9:16, cada um como storyboard de 5 cenas pro motion. A cena 5 é o end card.</p>
<div class="meta"><span>6 entregas · 30 quadros</span><span>Export 1440 px</span><span>9 fotos aplicadas · copy conferida com o brief, linha a linha</span></div></div></header>

<section><div class="sec-head"><span class="eyebrow">Decisões que precisam do seu ok</span></div>
<div class="grid2">
<div class="note"><p class="k">CTA</p><p>O brief pede <b>Learn More</b>, no lugar do Book an inspection que o BOF usa. Segui o brief. O botão ficou pill preta sobre o amarelo, como no ad kit. O vermelho do storyboard de referência ficou de fora.</p></div>
<div class="note"><p class="k">5 cenas, não 3</p><p>A regra da casa pra motion é storyboard de 3 cenas, mas aqui o cliente mandou uma referência de 5 quadros e pediu pra seguir frame a frame. Segui a do cliente.</p></div>
<div class="note"><p class="k">PC Platinum no V1</p><p>A copy do V1 não cita PC Platinum, mas o visual detail pede pra apresentar o serviço. Coloquei como etiqueta pequena na cena 4. Se quiser o V1 sem esse nome, sai sem afetar o resto.</p></div>
<div class="note"><p class="k">Brief com foco trocado</p><p>Na tabela "Testing Variable", o foco do V1 descreve serviço e o texto do V2 se repete no V3. Tomei como certos o nome de cada ângulo e os visual details, que batem com a copy. Vale confirmar com o cliente.</p></div>
<div class="note"><p class="k">Callouts do V3</p><p>Rótulos tirados da lista do brief: shaded foliage, under decks/patios, standing water, shrubs. Nada de pulverizador nem comedouro de pássaro. O logo é o elemento de marca.</p></div>
<div class="note"><p class="k">Vetor por cima da foto</p><p>Relógio, mosquitos, escudo, callouts e o ícone do end card são vetor. Assim o texto não sai torto e o mosquito não sai deformado, e o motion anima cada peça em separado.</p></div>
</div></section>

<div class="toolbar"><div class="tabs" role="group" aria-label="Formato">
<button type="button" id="r916" data-r="9x16" aria-pressed="true">9:16</button>
<button type="button" id="r11" data-r="1x1" aria-pressed="false">1:1</button></div>
<label class="toggle"><input type="checkbox" id="safe"> Mostrar safe zones do 9:16 (14% topo, 35% base, 6% laterais)</label></div>

{"".join(version_section(k, v) for k, v in VERSIONS.items())}

<section><div class="sec-head"><span class="eyebrow">Fotos pro ChatGPT</span><h2>3 momentos por versão, 9 imagens</h2>
<p class="lede">Gere em 4:5, com margem larga, e salve com o nome da primeira coluna em <span class="mono">03-work/banners/2026-core4-mosquito/img/</span>. O 1:1 e o 9:16 são recortados automaticamente. Os prompts estão em <span class="mono">image-prompts.md</span>. Em cada versão, gere o momento 1 primeiro e use ele de referência nos outros dois.</p></div>
<div class="tbl"><table><thead><tr><th>Arquivo</th><th>Cena</th><th>Usado em</th><th>Status</th></tr></thead><tbody>{shots_table()}</tbody></table></div></section>
'''
    js = """<script>
(function(){var b=document.querySelectorAll('.tabs button');
b.forEach(function(x){x.addEventListener('click',function(){var r=x.dataset.r;
b.forEach(function(y){y.setAttribute('aria-pressed',y===x)});
document.querySelectorAll('.rs').forEach(function(s){s.hidden=s.dataset.ratio!==r});
document.getElementById('safe').disabled=r!=='9x16';});});
var s=document.getElementById('safe');s.addEventListener('change',function(){document.body.classList.toggle('show-safe',s.checked)});})();
</script>"""
    OUTDIR.mkdir(parents=True, exist_ok=True)
    p = OUTDIR / "mosquito.html"
    p.write_text(f"<title>Mosquito Season</title>\n<style>{fonts}\n{PAGE_CSS}</style>\n<div class=\"wrap\">{body}</div>\n{js}", encoding="utf-8")
    print(p, round(p.stat().st_size / 1024), "KB")

if __name__ == "__main__":
    main()
