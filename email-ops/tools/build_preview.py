#!/usr/bin/env python3
"""
build_preview.py - monta UMA pagina de revisao autocontida para um fluxo de e-mails.

Uso:
    python build_preview.py <pasta_do_fluxo> [--out arquivo.html] [--title "..."]
                            [--notes notas.md]

O que faz:
  - Junta todos os *.html da pasta (ordenados pelo nome do arquivo).
  - Embute cada imagem com caminho relativo como data: URI (atributo src,
    atributo background e url() de CSS). A pagina final abre sozinha, pode ir
    por e-mail, chat ou virar Artifact sem quebrar imagem.
  - Le o comentario do topo de cada e-mail (Subject, Preheader, Modules, Button)
    e mostra numa faixa de metadados, com contagem de caracteres do assunto.
  - Uma aba por e-mail; em cada aba, desktop (640px) e mobile (375px) lado a
    lado, em iframes que ajustam a altura ao conteudo.
  - --notes: arquivo com linhas "- item" (o que mudou / decisoes em aberto),
    mostrado numa caixa destacada no topo. Outras linhas sao ignoradas.

Saida padrao: <pasta_do_fluxo>/preview.html. Avisa (stderr) se passar de 15 MB.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SIZE_WARN_BYTES = 15 * 1024 * 1024
DESKTOP_WIDTH = 640
MOBILE_WIDTH = 375
META_KEYS = ("Subject", "Preheader", "Modules", "Button")
SKIP_PREFIXES = ("http:", "https:", "data:", "cid:", "mailto:", "tel:", "#", "{{", "{%", "//")

mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/svg+xml", ".svg")

SRC_RE = re.compile(r'(\b(?:src|background)\s*=\s*)(["\'])(.*?)\2', re.I | re.S)
URL_RE = re.compile(r'(url\(\s*)(["\']?)([^"\')]+)\2(\s*\))', re.I)


# --------------------------------------------------------------------------
# Leitura dos e-mails
# --------------------------------------------------------------------------

def parse_meta(source: str) -> dict[str, str]:
    """Extrai Subject/Preheader/Modules/Button do primeiro comentario HTML."""
    meta: dict[str, str] = {}
    m = re.search(r"<!--(.*?)-->", source, re.S)
    if not m:
        return meta
    for line in m.group(1).splitlines():
        km = re.match(r"\s*([A-Za-z][A-Za-z ]*?)\s*:\s*(.+?)\s*$", line)
        if km and km.group(1) in META_KEYS:
            meta[km.group(1)] = km.group(2)
    return meta


class Inliner:
    """Troca caminhos relativos de imagem por data: URI, com cache por arquivo."""

    def __init__(self) -> None:
        self.cache: dict[Path, str] = {}
        self.missing: set[str] = set()

    def data_uri(self, ref: str, base: Path) -> str | None:
        clean = html.unescape(ref.strip())
        if not clean or clean.lower().startswith(SKIP_PREFIXES):
            return None
        clean = unquote(clean.split("#", 1)[0].split("?", 1)[0])
        path = (base / clean).resolve()
        if path in self.cache:
            return self.cache[path]
        if not path.is_file():
            self.missing.add(f"{ref} (em {base})")
            return None
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        uri = f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"
        self.cache[path] = uri
        return uri

    def inline(self, source: str, base: Path) -> str:
        def attr(m: re.Match) -> str:
            uri = self.data_uri(m.group(3), base)
            return f"{m.group(1)}{m.group(2)}{uri}{m.group(2)}" if uri else m.group(0)

        def css(m: re.Match) -> str:
            uri = self.data_uri(m.group(3), base)
            return f"{m.group(1)}'{uri}'{m.group(4)}" if uri else m.group(0)

        return URL_RE.sub(css, SRC_RE.sub(attr, source))


def read_notes(path: Path) -> list[str]:
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*[-*]\s+(.+)", line)
        if m:
            items.append(m.group(1).strip())
    return items


def inline_md(text: str) -> str:
    """Markdown minimo em linha: `codigo`, **negrito**."""
    out = html.escape(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    return out


# --------------------------------------------------------------------------
# Pagina
# --------------------------------------------------------------------------

CSS = """
:root{
  --bg:#f4f4f2; --surface:#ffffff; --surface-2:#ecece8; --border:#d9d9d4;
  --text:#1b1b1a; --muted:#62625d; --accent:#1f5fbf; --accent-soft:#e6eefb;
  --note-bg:#fff8e1; --note-border:#e3c766; --warn:#a4460f; --frame:#e2e2dd;
  --focus:#1f5fbf; color-scheme:light;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#141414; --surface:#1d1d1c; --surface-2:#262625; --border:#363634;
    --text:#ececea; --muted:#a3a39e; --accent:#7fb0ff; --accent-soft:#1d2a40;
    --note-bg:#2b2615; --note-border:#6f5f24; --warn:#f0a36b; --frame:#2a2a28;
    --focus:#7fb0ff; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#141414; --surface:#1d1d1c; --surface-2:#262625; --border:#363634;
  --text:#ececea; --muted:#a3a39e; --accent:#7fb0ff; --accent-soft:#1d2a40;
  --note-bg:#2b2615; --note-border:#6f5f24; --warn:#f0a36b; --frame:#2a2a28;
  --focus:#7fb0ff; color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
  font:14px/1.5 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding-inline:24px;padding-block:28px 64px}
header.top{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:8px 24px;margin-bottom:20px}
h1{font-size:22px;font-weight:600;margin:0;letter-spacing:-.01em}
.sub{color:var(--muted);font:12px/1.4 "IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.theme-btn{font:inherit;font-size:12px;color:var(--muted);background:var(--surface);border:1px solid var(--border);
  border-radius:6px;padding:4px 10px;cursor:pointer}
.theme-btn:hover{color:var(--text)}
.notes{background:var(--note-bg);border:1px solid var(--note-border);border-radius:8px;padding:14px 18px;margin-bottom:22px}
.notes h2{font-size:12px;text-transform:uppercase;letter-spacing:.08em;margin:0 0 6px;color:var(--muted);font-weight:600}
.notes ul{margin:0;padding-left:18px}
.notes li{margin:3px 0}
code{font-family:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;font-size:.92em;background:var(--surface-2);padding:1px 4px;border-radius:3px}
.tabs{display:flex;flex-wrap:wrap;gap:6px;border-bottom:1px solid var(--border);margin-bottom:18px}
.tab{font:inherit;font-size:13px;color:var(--muted);background:transparent;border:1px solid transparent;border-bottom:0;
  border-radius:6px 6px 0 0;padding:8px 14px;margin-bottom:-1px;cursor:pointer;text-align:left}
.tab .n{font-family:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;font-size:11px;margin-right:6px;opacity:.8}
.tab:hover{color:var(--text)}
.tab[aria-selected="true"]{color:var(--text);background:var(--surface);border-color:var(--border);font-weight:600}
.tab:focus-visible,.theme-btn:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
[hidden]{display:none!important}
.meta{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:14px 18px;margin-bottom:18px;
  display:grid;grid-template-columns:max-content 1fr;gap:6px 18px}
.meta dt{font:11px/1.9 "IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.meta dd{margin:0;overflow-wrap:anywhere}
.meta .subject{font-weight:600}
.count{font:11px "IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;color:var(--muted);margin-left:8px;white-space:nowrap}
.count.long{color:var(--warn)}
.mono{font-family:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;font-size:12px}
.missing{color:var(--muted);font-style:italic}
.views{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}
.view{min-width:0;max-width:100%}
.view h3{font:11px "IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 8px;font-weight:500}
.scroller{overflow-x:auto;max-width:100%;border:1px solid var(--border);border-radius:8px;background:var(--frame)}
/* O iframe herda o color-scheme do elemento <iframe>: sem isto, uma pagina de preview em tema escuro
   ativa o dark mode dos e-mails. Padrao: e-mail em modo claro; o botao "ver dark mode" troca. */
.scroller iframe{display:block;border:0;background:#fff;height:800px;color-scheme:light}
.email-dark .scroller iframe{color-scheme:dark;background:#000}
.btns{display:flex;flex-wrap:wrap;gap:8px}
footer{margin-top:40px;color:var(--muted);font-size:12px}
@media (max-width:640px){
  .wrap{padding-inline:16px;padding-block:20px 48px}
  .meta{grid-template-columns:1fr;gap:2px}
  .meta dd{margin-bottom:8px}
  .views{gap:18px}
}
"""

JS = """
(function(){
  var tabs=[].slice.call(document.querySelectorAll('.tab'));
  function fit(f){
    try{
      var d=f.contentDocument; if(!d||!d.documentElement) return;
      var h=Math.max(d.documentElement.scrollHeight, d.body?d.body.scrollHeight:0);
      if(h>0) f.style.height=h+'px';
    }catch(e){}
  }
  function fitAll(panel){
    [].forEach.call(panel.querySelectorAll('iframe'),function(f){fit(f);setTimeout(function(){fit(f)},600);});
  }
  [].forEach.call(document.querySelectorAll('iframe'),function(f){
    f.addEventListener('load',function(){fit(f);setTimeout(function(){fit(f)},600);});
    var src=document.getElementById('src-'+f.getAttribute('data-src'));
    if(src){ try{ f.srcdoc=JSON.parse(src.textContent); }catch(e){} }
  });
  function select(i,focus,push){
    tabs.forEach(function(t,j){
      var on=(i===j);
      t.setAttribute('aria-selected',on?'true':'false');
      t.tabIndex=on?0:-1;
      var p=document.getElementById(t.getAttribute('aria-controls'));
      p.hidden=!on;
      if(on){fitAll(p);}
    });
    if(focus) tabs[i].focus();
    if(push){ try{history.replaceState(null,'','#e'+(i+1))}catch(e){} }
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){select(i,false,true)});
    t.addEventListener('keydown',function(e){
      var k=e.key, n=tabs.length, j=null;
      if(k==='ArrowRight') j=(i+1)%n;
      else if(k==='ArrowLeft') j=(i-1+n)%n;
      else if(k==='Home') j=0;
      else if(k==='End') j=n-1;
      if(j!==null){e.preventDefault();select(j,true,true);}
    });
  });
  var m=/^#e(\d+)$/.exec(location.hash), start=m?Math.min(tabs.length,Math.max(1,+m[1]))-1:0;
  if(tabs.length) select(start,false,false);
  var em=document.getElementById('emailmode');
  if(em){
    em.addEventListener('click',function(){
      var on=document.body.classList.toggle('email-dark');
      em.setAttribute('aria-pressed',on?'true':'false');
      em.textContent=on?'E-mails: dark mode · voltar ao claro':'E-mails: modo claro · ver dark mode';
      [].forEach.call(document.querySelectorAll('iframe'),function(f){fit(f);setTimeout(function(){fit(f)},600);});
    });
  }
  var btn=document.getElementById('theme');
  if(btn){
    btn.addEventListener('click',function(){
      var r=document.documentElement, cur=r.getAttribute('data-theme');
      var dark=cur?cur==='dark':matchMedia('(prefers-color-scheme: dark)').matches;
      r.setAttribute('data-theme',dark?'light':'dark');
    });
  }
})();
"""


def json_for_script(text: str) -> str:
    """JSON seguro dentro de <script>: nenhum "</" fecha a tag antes da hora."""
    return json.dumps(text).replace("</", "<\\/")


def meta_row(label: str, value: str | None, extra: str = "", cls: str = "") -> str:
    if value:
        body = f'<span class="{cls}">{html.escape(value)}</span>{extra}'
    else:
        body = '<span class="missing">nao informado no comentario do topo</span>'
    return f"<dt>{label}</dt><dd>{body}</dd>"


def build_page(title: str, emails: list[dict], notes: list[str]) -> str:
    tabs, panels = [], []
    for i, e in enumerate(emails):
        tid, pid = f"tab-{i + 1}", f"panel-{i + 1}"
        meta = e["meta"]
        subject = meta.get("Subject", "")
        n = len(subject)
        count = (f'<span class="count{" long" if n > 50 else ""}">{n} caracteres</span>'
                 if subject else "")
        label = subject or e["name"]
        tabs.append(
            f'<button class="tab" role="tab" id="{tid}" aria-controls="{pid}" '
            f'aria-selected="false" tabindex="-1"><span class="n">{i + 1:02d}</span>'
            f'{html.escape(label)}</button>')
        n_src = i + 1
        rows = "".join([
            meta_row("Assunto", subject, count, "subject"),
            meta_row("Preheader", meta.get("Preheader")),
            meta_row("Botao", meta.get("Button")),
            meta_row("Modulos", meta.get("Modules"), cls="mono"),
            meta_row("Arquivo", e["name"], cls="mono"),
        ])
        panels.append(f"""
<section class="panel" role="tabpanel" id="{pid}" aria-labelledby="{tid}" hidden>
  <dl class="meta">{rows}</dl>
  <div class="views">
    <div class="view"><h3>Desktop · {DESKTOP_WIDTH}px</h3>
      <div class="scroller"><iframe title="{html.escape(label)} desktop" width="{DESKTOP_WIDTH}" style="width:{DESKTOP_WIDTH}px" data-src="{n_src}"></iframe></div></div>
    <div class="view"><h3>Mobile · {MOBILE_WIDTH}px</h3>
      <div class="scroller"><iframe title="{html.escape(label)} mobile" width="{MOBILE_WIDTH}" style="width:{MOBILE_WIDTH}px" data-src="{n_src}"></iframe></div></div>
  </div>
</section>""")

    # Cada e-mail e guardado uma unica vez (JSON) e o JS preenche os dois iframes.
    sources = "".join(
        f'<script type="application/json" id="src-{i + 1}">{json_for_script(e["html"])}</script>\n'
        for i, e in enumerate(emails))
    notes_html = ""
    if notes:
        items = "".join(f"<li>{inline_md(x)}</li>" for x in notes)
        notes_html = (f'<aside class="notes" aria-label="Notas da revisao">'
                      f'<h2>O que mudou / decisoes em aberto</h2><ul>{items}</ul></aside>')

    count = len(emails)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div>
      <h1>{html.escape(title)}</h1>
      <div class="sub">{count} e-mail{"s" if count != 1 else ""} · desktop {DESKTOP_WIDTH}px + mobile {MOBILE_WIDTH}px</div>
    </div>
    <span class="btns"><button class="theme-btn" id="emailmode" type="button" aria-pressed="false">E-mails: modo claro · ver dark mode</button>
    <button class="theme-btn" id="theme" type="button">Alternar tema da pagina</button></span>
  </header>
  {notes_html}
  <div class="tabs" role="tablist" aria-label="E-mails do fluxo">{"".join(tabs)}</div>
  {"".join(panels)}
  <footer>O tema da pagina nao altera o e-mail; os e-mails seguem o tema do sistema de quem abre. Setas do teclado trocam de aba.</footer>
</div>
{sources}<script>{JS}</script>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Monta uma pagina HTML autocontida para revisar um fluxo de e-mails.")
    ap.add_argument("folder", help="pasta do fluxo com os arquivos .html dos e-mails")
    ap.add_argument("--out", help="arquivo de saida (padrao: <pasta>/preview.html)")
    ap.add_argument("--title", help="titulo da pagina (padrao: nome da pasta)")
    ap.add_argument("--notes", help="arquivo com linhas '- item' mostradas no topo")
    args = ap.parse_args(argv)

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        sys.exit(f"Pasta nao encontrada: {folder}")
    out = Path(args.out).resolve() if args.out else folder / "preview.html"

    files = sorted(p for p in folder.glob("*.html") if p.is_file() and p.resolve() != out)
    files = [p for p in files if p.name.lower() != "preview.html"]
    if not files:
        sys.exit(f"Nenhum e-mail .html em {folder}")

    inliner = Inliner()
    emails = []
    for path in files:
        source = path.read_text(encoding="utf-8")
        emails.append({
            "name": path.name,
            "meta": parse_meta(source),
            "html": inliner.inline(source, path.parent),
        })

    notes = read_notes(Path(args.notes)) if args.notes else []
    title = args.title or f"Revisao · {folder.name}"
    page = build_page(title, emails, notes)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")

    for ref in sorted(inliner.missing):
        print(f"aviso: imagem nao encontrada: {ref}", file=sys.stderr)
    size = out.stat().st_size
    if size > SIZE_WARN_BYTES:
        print(f"aviso: a pagina tem {size / 1048576:.1f} MB (acima de 15 MB). "
              "Comprima as imagens antes de compartilhar.", file=sys.stderr)
    print(f"{out}  ({len(emails)} e-mails, {size / 1048576:.2f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
