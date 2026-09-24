#!/usr/bin/env python3
"""
render.py - gera capturas PNG de e-mails HTML em varias larguras.

Uso:
    python render.py <email.html|pasta> [--out PASTA] [--widths 680,375] [--dark]
                     [--height 6000] [--browser CAMINHO] [--wait 2500]

O que faz:
  - Encontra Chrome ou Edge instalado (Windows, macOS, Linux). Para forcar um
    navegador especifico use --browser ou a variavel de ambiente EMAIL_OPS_BROWSER.
  - Cada e-mail e renderizado dentro de uma pagina "moldura" temporaria com um
    <iframe width=W>. Isso contorna a largura minima de janela do Chrome headless
    (~500px): 375px vira 375px de verdade, sem cortar nem esticar.
  - Largura "desktop" padrao e 680 (uma janela de 600 dispara media queries
    mobile do tipo max-width:620px, comuns em e-mail).
  - Tema claro e forcado por padrao; --dark forca prefers-color-scheme: dark.
  - Recorte final: se Pillow estiver instalado ele e usado; senao um recortador
    PNG em Python puro (stdlib) corta a largura para W e remove as linhas finais
    de fundo uniforme. Se o PNG tiver formato incomum, a imagem fica inteira.

Saida: {nome}-{largura}[-dark].png na pasta --out (padrao: pasta "renders" ao
lado do e-mail). Os caminhos gerados sao impressos no terminal.
"""

from __future__ import annotations

import argparse
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

HEADLESS_MIN_WIDTH = 500
DEFAULT_WIDTHS = "680,375"
DEFAULT_HEIGHT = 6000
# Cor de fundo da moldura: distinta de qualquer e-mail real, facilita o recorte.
FRAME_BG = (255, 0, 255)


# --------------------------------------------------------------------------
# Localizacao do navegador
# --------------------------------------------------------------------------

def browser_candidates() -> list[str]:
    """Lista caminhos provaveis de Chrome/Edge para o sistema atual."""
    out: list[str] = []
    if sys.platform.startswith("win"):
        roots = [
            os.environ.get("PROGRAMFILES", r"C:\Program Files"),
            os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
            os.environ.get("LOCALAPPDATA", ""),
        ]
        rels = [
            r"Google\Chrome\Application\chrome.exe",
            r"Microsoft\Edge\Application\msedge.exe",
            r"Chromium\Application\chrome.exe",
        ]
        for root in roots:
            if root:
                out += [os.path.join(root, rel) for rel in rels]
    elif sys.platform == "darwin":
        apps = [
            "Google Chrome.app/Contents/MacOS/Google Chrome",
            "Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "Chromium.app/Contents/MacOS/Chromium",
        ]
        for base in ["/Applications", os.path.expanduser("~/Applications")]:
            out += [os.path.join(base, a) for a in apps]
    names = [
        "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
        "microsoft-edge", "microsoft-edge-stable", "chrome", "msedge",
    ]
    for name in names:
        found = shutil.which(name)
        if found:
            out.append(found)
    return out


def find_browser(explicit: str | None = None) -> str:
    """Retorna o executavel do navegador ou encerra com mensagem clara."""
    for choice in (explicit, os.environ.get("EMAIL_OPS_BROWSER")):
        if choice:
            if Path(choice).is_file() or shutil.which(choice):
                return shutil.which(choice) or choice
            sys.exit(f"Navegador informado nao encontrado: {choice}")
    for path in browser_candidates():
        if Path(path).is_file():
            return path
    sys.exit(
        "Nenhum Chrome/Edge encontrado. Instale um deles ou informe o caminho "
        "com --browser ou a variavel EMAIL_OPS_BROWSER."
    )


# --------------------------------------------------------------------------
# Moldura e captura
# --------------------------------------------------------------------------

def frame_html(email_uri: str, width: int, height: int) -> str:
    """Pagina temporaria que carrega o e-mail num iframe da largura pedida."""
    r, g, b = FRAME_BG
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
html,body{{margin:0;padding:0;background:rgb({r},{g},{b});overflow:hidden}}
iframe{{display:block;border:0;margin:0;padding:0;width:{width}px;height:{height}px}}
</style></head>
<body>
<iframe id="f" src="{email_uri}" width="{width}" height="{height}" scrolling="no"></iframe>
<script>
(function(){{
  var f=document.getElementById('f');
  function fit(){{
    try{{
      var d=f.contentDocument; if(!d) return;
      var h=Math.max(d.documentElement.scrollHeight, d.body?d.body.scrollHeight:0);
      if(h>0) f.style.height=h+'px';
    }}catch(e){{}}
  }}
  f.addEventListener('load',function(){{fit();setTimeout(fit,600);setTimeout(fit,1500);}});
}})();
</script>
</body></html>
"""


def capture(browser: str, frame_path: Path, png_path: Path, win_w: int,
            win_h: int, dark: bool, wait_ms: int) -> None:
    """Roda o navegador headless e grava o screenshot."""
    scheme = 0 if dark else 1  # Blink: 0 = dark, 1 = light
    profile = tempfile.mkdtemp(prefix="email-render-profile-")
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--allow-file-access-from-files",
        f"--user-data-dir={profile}",
        f"--blink-settings=preferredColorScheme={scheme}",
        "--force-device-scale-factor=1",
        f"--window-size={win_w},{win_h}",
        f"--virtual-time-budget={wait_ms}",
        f"--screenshot={png_path}",
        frame_path.resolve().as_uri(),
    ]
    if dark:
        cmd.insert(1, "--force-dark-mode")
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=120, check=False)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    if not png_path.is_file():
        raise RuntimeError(f"o navegador nao gerou {png_path.name}")


# --------------------------------------------------------------------------
# Recorte (Pillow se houver; senao PNG em Python puro)
# --------------------------------------------------------------------------

def _trim_rows(rows: list[bytes], width: int, bpp: int) -> list[bytes]:
    """Remove linhas finais iguais a ultima linha (fundo uniforme)."""
    if not rows:
        return rows
    last = rows[-1]
    first_px = last[:bpp]
    if last != first_px * width:
        return rows  # ultima linha nao e uniforme: nada a cortar
    end = len(rows)
    while end > 1 and rows[end - 1] == last:
        end -= 1
    return rows[:end]


def crop_with_pillow(path: Path, width: int) -> bool:
    try:
        from PIL import Image  # type: ignore
    except ImportError:
        return False
    img = Image.open(path)
    img.load()
    w = min(width, img.width)
    img = img.crop((0, 0, w, img.height))
    mode = img.mode
    bpp = {"RGB": 3, "RGBA": 4}.get(mode)
    if bpp is None:
        img = img.convert("RGBA")
        bpp = 4
    raw = img.tobytes()
    stride = w * bpp
    rows = [raw[i:i + stride] for i in range(0, len(raw), stride)]
    kept = _trim_rows(rows, w, bpp)
    if len(kept) != img.height:
        img = img.crop((0, 0, w, len(kept)))
    img.save(path, optimize=True)
    return True


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def crop_pure(path: Path, width: int) -> bool:
    """Recorta PNG 8 bits RGB/RGBA nao entrelacado usando so a stdlib."""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return False
    pos, ihdr, idat = 8, None, bytearray()
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", body)
        elif ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            break
    if not ihdr:
        return False
    w, h, depth, color, _, _, interlace = ihdr
    bpp = {2: 3, 6: 4}.get(color)
    if depth != 8 or bpp is None or interlace:
        return False
    raw = zlib.decompress(bytes(idat))
    stride = w * bpp
    new_w = min(width, w)
    new_stride = new_w * bpp
    prev = bytearray(stride)
    rows: list[bytes] = []
    i = 0
    for _ in range(h):
        ftype = raw[i]
        line = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        if ftype == 1:
            for x in range(bpp, stride):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif ftype == 2:
            line = bytearray((a + b) & 255 for a, b in zip(line, prev))
        elif ftype == 3:
            for x in range(stride):
                left = line[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + ((left + prev[x]) >> 1)) & 255
        elif ftype == 4:
            for x in range(stride):
                a = line[x - bpp] if x >= bpp else 0
                c = prev[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + _paeth(a, prev[x], c)) & 255
        prev = line
        rows.append(bytes(line[:new_stride]))
    rows = _trim_rows(rows, new_w, bpp)

    def chunk(tag: bytes, payload: bytes) -> bytes:
        crc = zlib.crc32(tag + payload) & 0xFFFFFFFF
        return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", crc)

    body = b"".join(b"\x00" + r for r in rows)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", new_w, len(rows), 8, color, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(body, 6))
           + chunk(b"IEND", b""))
    path.write_bytes(png)
    return True


def crop(path: Path, width: int) -> str:
    """Recorta a captura; retorna qual metodo foi usado."""
    try:
        if crop_with_pillow(path, width):
            return "pillow"
        if crop_pure(path, width):
            return "stdlib"
    except Exception as exc:  # recorte nunca deve derrubar a renderizacao
        print(f"  aviso: recorte falhou em {path.name}: {exc}", file=sys.stderr)
    return "sem recorte"


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def collect_emails(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    if target.is_dir():
        return sorted(p for p in target.glob("*.html") if p.is_file())
    sys.exit(f"Nao encontrado: {target}")


def parse_widths(value: str) -> list[int]:
    try:
        widths = [int(v) for v in value.split(",") if v.strip()]
    except ValueError:
        raise argparse.ArgumentTypeError("use numeros separados por virgula, ex.: 680,375")
    if not widths or any(w < 200 or w > 2000 for w in widths):
        raise argparse.ArgumentTypeError("larguras entre 200 e 2000 px")
    return widths


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Gera PNGs de e-mails HTML (desktop e mobile) com Chrome/Edge headless.")
    ap.add_argument("target", help="arquivo .html de e-mail ou pasta com varios")
    ap.add_argument("--out", help="pasta de saida (padrao: renders/ ao lado do e-mail)")
    ap.add_argument("--widths", type=parse_widths, default=parse_widths(DEFAULT_WIDTHS),
                    help=f"larguras em px separadas por virgula (padrao {DEFAULT_WIDTHS})")
    ap.add_argument("--dark", action="store_true",
                    help="forca prefers-color-scheme: dark (padrao: claro)")
    ap.add_argument("--height", type=int, default=DEFAULT_HEIGHT,
                    help=f"altura maxima da captura em px (padrao {DEFAULT_HEIGHT})")
    ap.add_argument("--wait", type=int, default=2500,
                    help="tempo virtual em ms para carregar imagens e ajustar altura (padrao 2500)")
    ap.add_argument("--browser", help="caminho do Chrome/Edge (ou use EMAIL_OPS_BROWSER)")
    args = ap.parse_args(argv)

    browser = find_browser(args.browser)
    emails = collect_emails(Path(args.target))
    if not emails:
        sys.exit("Nenhum .html encontrado.")

    produced: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="email-render-") as tmp:
        tmpdir = Path(tmp)
        for email in emails:
            email = email.resolve()
            out_dir = Path(args.out) if args.out else email.parent / "renders"
            out_dir.mkdir(parents=True, exist_ok=True)
            for width in args.widths:
                suffix = "-dark" if args.dark else ""
                png = (out_dir / f"{email.stem}-{width}{suffix}.png").resolve()
                frame = tmpdir / f"frame-{email.stem}-{width}.html"
                frame.write_text(frame_html(email.as_uri(), width, args.height),
                                 encoding="utf-8")
                win_w = max(width, HEADLESS_MIN_WIDTH)
                try:
                    capture(browser, frame, png, win_w, args.height, args.dark, args.wait)
                except Exception as exc:
                    print(f"ERRO {email.name} @ {width}px: {exc}", file=sys.stderr)
                    continue
                method = crop(png, width)
                produced.append(png)
                print(f"{png}  ({method})")
    if not produced:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
