"""Render a Tom's email HTML (600px) to a 1200px JPG with headless Chrome.

Usage: python render_email.py <email.html> [--quality 85]
Writes <email>.png (full, lossless) and <email>.jpg next to the HTML, trimmed to the content height.
"""
import argparse, os, subprocess, sys
from PIL import Image

CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html'); ap.add_argument('--quality', type=int, default=85); ap.add_argument('--height', type=int, default=6000); ap.add_argument('--slices', action='store_true')
    a = ap.parse_args()
    html = os.path.abspath(a.html); base = os.path.splitext(html)[0]
    exe = next(p for p in CHROME if os.path.exists(p))
    png = base + '.png'
    subprocess.run([exe, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--force-device-scale-factor=2', f'--window-size=600,{a.height}', '--virtual-time-budget=6000',
                    f'--screenshot={png}', 'file:///' + html.replace('\\', '/')], check=True, capture_output=True)
    im = Image.open(png).convert('RGB')
    w, h = im.size
    px = im.load()
    bottom = h - 1
    while bottom > 0 and all(px[x, bottom] == (255, 255, 255) for x in range(0, w, 40)):
        bottom -= 1
    im = im.crop((0, 0, w, bottom + 1))
    im.save(png)
    jpg = base + '.jpg'
    im.save(jpg, 'JPEG', quality=a.quality, optimize=True, progressive=True)
    print(f'{jpg}  {im.size[0]}x{im.size[1]}  {os.path.getsize(jpg)//1024} KB')
    if a.slices:
        slice_jpg(exe, html, im, base, a.quality)

def slice_jpg(exe, html, im, base, quality):
    """Cut the full render at the midpoints between [data-slice] elements (top to bottom)."""
    probe = os.path.join(os.path.dirname(html), '_probe.html')
    src = open(html, encoding='utf-8').read()
    js = ("<script>window.addEventListener('load',()=>{const r=[...document.querySelectorAll('[data-slice]')]"
          ".map(e=>{const b=e.getBoundingClientRect();return [e.dataset.slice,b.top+scrollY,b.bottom+scrollY]});"
          "document.title='SLICES'+JSON.stringify(r)})</script>")
    open(probe, 'w', encoding='utf-8').write(src.replace('</body>', js + '</body>'))
    try:
        out = subprocess.run([exe, '--headless=new', '--disable-gpu', '--allow-file-access-from-files', '--window-size=600,3000',
                              '--virtual-time-budget=6000', '--dump-dom', 'file:///' + probe.replace(os.sep, '/')],
                             capture_output=True, text=True, encoding='utf-8').stdout
    finally:
        os.remove(probe)
    import json, re, html as h
    rects = json.loads(h.unescape(re.search(r'<title>SLICES(.*?)</title>', out, re.S).group(1)))
    rects.sort(key=lambda r: r[1])
    cuts = [0]
    for (n1, t1, b1), (n2, t2, b2) in zip(rects, rects[1:]):
        cuts.append(round((b1 + t2) / 2 * 2))
    cuts.append(im.size[1])
    d = base + '_slices'; os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    stem = os.path.basename(base)
    for i, (y0, y1) in enumerate(zip(cuts, cuts[1:]), 1):
        p = os.path.join(d, f'{stem}_{i:02d}_{rects[i-1][0]}.jpg')
        im.crop((0, y0, im.size[0], y1)).save(p, 'JPEG', quality=quality, optimize=True, progressive=True)
    print(f'{len(cuts)-1} slices -> {d}')

if __name__ == '__main__':
    main()
