"""Package the November frames for Figma HTML import.

usage: python figma_export.py
Writes ../../../../04-deliverables/social/2026-11-organic/figma-import/:
  <post>/<frame>.html   self-contained (CSS, fonts and images inlined), page width = frame width
  img/                  every image the frames use, for swaps in Figma
  reels/                storyboard PNGs + MP4 (the Reels are code animations, not importable as layers)
Figma-import fixes (see memory figma-storyboard-board): fixed body size, no outer margin,
logo SVG without its clip-path id.
"""
import base64, mimetypes, pathlib, re, shutil

HERE = pathlib.Path(__file__).resolve().parent
FRAMES = HERE / "frames"
OUT = HERE.parents[3] / "04-deliverables" / "social" / "2026-11-organic" / "figma-import"
DELIV = HERE.parents[3] / "04-deliverables" / "social" / "2026-11-organic"
MIME = {".otf": "font/otf", ".woff": "font/woff", ".woff2": "font/woff2", ".webp": "image/webp", ".svg": "image/svg+xml"}

def data_uri(p: pathlib.Path) -> str:
    mt = MIME.get(p.suffix.lower()) or mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    return f"data:{mt};base64," + base64.b64encode(p.read_bytes()).decode()

used = set()

def inline_urls(text: str, base: pathlib.Path) -> str:
    def rep(m):
        ref = m.group(2)
        if ref.startswith(("data:", "http", "#")):
            return m.group(0)
        p = (base / ref).resolve()
        if not p.exists():
            raise SystemExit(f"missing {ref} from {base}")
        if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            used.add(p)
        return f"url({m.group(1)}{data_uri(p)}{m.group(1)})"
    return re.sub(r"url\((['\"]?)([^'\")]+)\1\)", rep, text)

def strip_logo_clip(html: str) -> str:
    html = re.sub(r'\s*clip-path="url\(#clip0_[^)]*\)"', "", html)
    return re.sub(r"<defs>\s*<clipPath id=\"clip0_[^\"]*\">.*?</clipPath>\s*</defs>", "", html, flags=re.S)

def export_frame(f: pathlib.Path):
    html = f.read_text(encoding="utf-8")
    css = []
    for href in re.findall(r'<link rel="stylesheet" href="([^"]+)">', html):
        p = (f.parent / href).resolve()
        css.append(inline_urls(p.read_text(encoding="utf-8"), p.parent))
    html = re.sub(r'<link rel="stylesheet" href="[^"]+">', "", html)
    w, h = 1080, (1920 if "9x16" in f.name else 1350)
    fix = f"html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden;background:transparent}}"
    html = html.replace("</head>", "<style>\n" + "\n".join(css) + "\n" + fix + "\n</style>\n</head>", 1)

    def img_rep(m):
        ref = m.group(1)
        if ref.startswith("data:"):
            return m.group(0)
        p = (f.parent / ref).resolve()
        used.add(p)
        return f'src="{data_uri(p)}"'
    html = re.sub(r'src="([^"]+)"', img_rep, html)
    html = inline_urls(html, f.parent)          # inline style="background:url(...)"
    html = strip_logo_clip(html)
    out = OUT / f.parent.name / f.name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out

if __name__ == "__main__":
    if OUT.exists():
        shutil.rmtree(OUT)
    files = sorted(FRAMES.rglob("*.html"))
    for f in files:
        export_frame(f)
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    for p in sorted(used):
        shutil.copy2(p, OUT / "img" / p.name)
    for post in ("07-katapult-at-checkout", "15-cyber-monday"):
        d = OUT / "reels" / post
        d.mkdir(parents=True, exist_ok=True)
        for png in sorted((DELIV / "png" / post).glob("*.png")):
            shutil.copy2(png, d / png.name)
        md = DELIV / "png" / post / "storyboard.md"
        if md.exists():
            shutil.copy2(md, d / "storyboard.md")
        for mp4 in (DELIV / "reels").glob(f"{post[:2]}-*.mp4"):
            shutil.copy2(mp4, d / mp4.name)
    print(f"{len(files)} frames, {len(used)} images -> {OUT}")
