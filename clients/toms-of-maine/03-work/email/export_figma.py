"""Make self-contained copies of the email HTML for importing into Figma (html.to.design or similar).

Usage: python export_figma.py <out_dir> <email.html> [...]
- every local image (src="..." and url(...)) is inlined as a data URI, downsized to at most 1200px wide (2x of 600);
- every local font is inlined as base64;
- the product-name size chosen by the in-page script is read from a headless Chrome render and baked into the CSS
  (importers do not run JavaScript), and the script is removed.
"""
import base64, io, os, re, subprocess, sys, pathlib
from PIL import Image

EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
MIME = {'.otf': 'font/otf', '.ttf': 'font/ttf', '.woff2': 'font/woff2', '.svg': 'image/svg+xml'}


def name_size(path):
    dom = subprocess.run([EXE, '--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--virtual-time-budget=6000',
                          '--dump-dom', pathlib.Path(os.path.abspath(path)).as_uri()], capture_output=True, text=True, encoding='utf-8').stdout
    m = re.search(r'data-pn="(\d+)"', dom)
    return m.group(1) if m else None


def data_uri(abs_path, cache):
    if abs_path in cache: return cache[abs_path]
    ext = os.path.splitext(abs_path)[1].lower()
    if ext in ('.otf', '.ttf', '.woff2', '.svg'):
        uri = f'data:{MIME[ext]};base64,' + base64.b64encode(open(abs_path, 'rb').read()).decode()
    else:
        im = Image.open(abs_path)
        if im.width > 1200: im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        b = io.BytesIO()
        alpha = im.convert('RGBA').getchannel('A') if im.mode in ('RGBA', 'LA', 'P') else None
        # photos with only a sliver of transparency (clipped by a rounded container anyway) go out as JPEG
        sliver = (alpha is not None and alpha.width >= 1000  # large photos only, never cut-out packshots
                  and alpha.point(lambda v: 255 if v < 250 else 0).histogram()[255] < 0.05 * alpha.width * alpha.height)
        if alpha is not None and ext == '.png' and alpha.getextrema()[0] < 255 and not sliver:
            im.convert('RGBA').save(b, 'PNG', optimize=True); mime = 'image/png'
        else:
            im.convert('RGB').save(b, 'JPEG', quality=86, optimize=True, progressive=True); mime = 'image/jpeg'
        uri = f'data:{mime};base64,' + base64.b64encode(b.getvalue()).decode()
    cache[abs_path] = uri
    return uri


def export(src, out_dir, cache):
    base = os.path.dirname(os.path.abspath(src))
    html = open(src, encoding='utf-8').read()
    missing = []

    def inline(m):
        q, ref = m.group(1), m.group(2)
        if ref.startswith(('data:', 'http')): return m.group(0)
        p = os.path.normpath(os.path.join(base, ref))
        if not os.path.exists(p):
            missing.append(ref); return m.group(0)
        return m.group(0).replace(ref, data_uri(p, cache))

    html = re.sub(r'''url\((["']?)([^"')]+)\1\)''', inline, html)
    html = re.sub(r'''src=(["'])([^"']+)\1''', inline, html)
    # drop font sources that do not exist (Gotham stand-in chain keeps Montserrat)
    html = re.sub(r'url\("(?!data:)[^"]+"\),', '', html)
    px = name_size(src)
    html = re.sub(r'<script>.*?</script>\s*', '', html, flags=re.S)
    if px:
        html = html.replace('</style>', f':root{{--pn:{px}px}}</style>', 1)
    out = os.path.join(out_dir, os.path.basename(src))
    open(out, 'w', encoding='utf-8').write(html)
    real_missing = [m for m in missing if 'gotham' not in m.lower()]
    print(f'{os.path.basename(out)}  {os.path.getsize(out) // 1024} KB  names {px or "-"}px' + (f'  MISSING {real_missing}' if real_missing else ''))


if __name__ == '__main__':
    out_dir = sys.argv[1]; os.makedirs(out_dir, exist_ok=True)
    cache = {}
    for f in sys.argv[2:]:
        export(f, out_dir, cache)
