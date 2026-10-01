"""Figma export for the Mosquito Season storyboards.

  python figma.py   -> 04-deliverables/banners/2026-core4-mosquito/html/
                       {V}/{ratio}/{frame name}.html  (30 files) + TN-Mosquito-Core4-HTML-Figma.zip

Same scenes as the PNGs, made safe for an HTML-to-Figma import (lessons from 2026-core4-bof):
- laid out natively at 1440 wide (every px value scaled from the 1080 layout);
- real font family names and weights, so the text layers map to the local Futura fonts;
- the photo plate is pre-cropped, faded and baked to one JPEG per frame (importers ignore CSS masks
  and object-position);
- headline and subhead are re-laid in headless Chrome as absolute, no-wrap text runs, one per line
  and color, so Figma never re-wraps them. The DOM is dumped after that, with no script left.
Frame names follow the TN26020 pattern: TN-Core4Mosquito-{ratio}-TakeBackYourYard-Motion-Meta-V{n}-{Angle}-S0{n}
"""
import base64, io, re, shutil, subprocess, zipfile
from PIL import Image
from build import (placement, OUT, IMG, CHROME, SIZES, SHOTS, VERSIONS, PIECE_CSS, BASIC,
                   font_face, logo_uri, scene_html)

K = 1440 / 1080
ROOT = OUT / "html"
FIGMA_FONTS = {"TN Display": ("Futura Display BQ", 400), "TN Medium": ("Futura Std", 500), "TN Heavy": ("Futura Std", 650)}
FIGMA_CSS = (".tn,.tn .sub{font-weight:500}.tn .hl,.tn .clock{font-weight:400}"
             ".tn .cta,.tn .chip,.tn .eyebrow,.tn .ph-tag{font-weight:650}.tn .ph-tag small{font-weight:500}")

def figma_fonts():
    css = font_face(BASIC)
    for tn, (fam, wt) in FIGMA_FONTS.items():
        css = css.replace(f"font-family:'{tn}';", f"font-family:'{fam}';font-weight:{wt};")
    return css

def scale_px(html):
    return re.sub(r"(-?\d+(?:\.\d+)?)px", lambda m: f"{float(m.group(1)) * K:.2f}".rstrip("0").rstrip(".") + "px", html)

def find_plate(shot, ratio):
    sh = SHOTS[shot]
    for name in (f"{shot}-{ratio}", f"{shot}-9x16", shot):
        for ext in ("png", "jpg", "jpeg", "webp"):
            p = IMG / f"{name}.{ext}"
            if p.exists():
                return p, name == f"{shot}-{ratio}"
    if sh.get("stand_in"):
        return find_plate(sh["stand_in"], ratio)
    return None, False

def baked_plate(shot, ratio):
    """The frame's background exactly as the PNG render shows it, as one JPEG at 1440."""
    c = SIZES[ratio]; W, H = round(c["W"] * K), round(c["H"] * K)
    p, own = find_plate(shot, ratio)
    if not p:
        return None
    im = Image.open(p).convert("RGB")
    pl = placement(shot, ratio)
    canvas = Image.new("RGB", (W, H), (20, 13, 8))          # .tn background
    if pl is not None and not own:
        top, z, fx = pl; w = round(W * z)
        h = round(im.height * w / im.width); im = im.resize((w, h), Image.LANCZOS)
        mask = Image.new("L", (w, h), 255); fade0 = round(h * .85)
        for y in range(fade0, h):
            mask.paste(round(255 * (1 - (y - fade0) / (h - fade0))), (0, y, w, y + 1))
        canvas.paste(im, (round(-(w - W) * fx), round(top * K)), mask)
    else:                                                   # object-fit: cover at 50% fy
        s = max(W / im.width, H / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        fy = .5 if own else SHOTS[shot]["fy"]
        x, y = (im.width - W) // 2, round((im.height - H) * fy)
        canvas = im.crop((x, y, x + W, y + H))
    buf = io.BytesIO(); canvas.save(buf, "JPEG", quality=88, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# Re-lays every .hl / .sub as absolute text runs: one div per line and per color,
# at the position Chrome measured, with spare width so Figma never wraps them.
FLATTEN_JS = """
document.fonts.ready.then(function(){
var tn=document.querySelector('.tn'),R=tn.getBoundingClientRect(),out=[];
tn.querySelectorAll('.hl,.sub').forEach(function(el){
  var cs=getComputedStyle(el),lines=[],w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
  while(w.nextNode()){var n=w.currentNode,col=getComputedStyle(n.parentElement).color,re=/[^\\s-]+-?|-/g,m,prevHy=false;
    while((m=re.exec(n.data))){var rg=document.createRange();rg.setStart(n,m.index);rg.setEnd(n,m.index+m[0].length);
      var r=rg.getClientRects()[0];if(!r)continue;
      var L=lines.find(function(l){return Math.abs(l.top-r.top)<r.height*.4});
      if(!L){L={top:r.top,h:r.height,runs:[]};lines.push(L)}
      var last=L.runs[L.runs.length-1];
      // "mosquito-" + "imposed": glue the pieces of a hyphenated word on the same line
      var glue=(last&&prevHy)?'':' ';
      if(last&&last.col===col){last.txt+=glue+m[0];last.right=r.right}
      else L.runs.push({col:col,txt:(last?glue:'')+m[0],x:r.left,right:r.right});
      prevHy=m[0].slice(-1)==='-';}}
  lines.forEach(function(L){L.runs.forEach(function(u){
    var d=document.createElement('div');d.textContent=u.txt.replace(/^ /,'');
    var x=u.txt.charAt(0)===' '?u.x:u.x;
    d.style.cssText='position:absolute;margin:0;white-space:nowrap;left:'+(x-R.left).toFixed(2)+'px;top:'+(L.top-R.top).toFixed(2)+'px;'+
      'width:'+Math.ceil((u.right-u.x)*1.15+4)+'px;height:'+L.h.toFixed(2)+'px;line-height:'+L.h.toFixed(2)+'px;'+
      'font-family:'+cs.fontFamily+';font-weight:'+cs.fontWeight+';font-size:'+cs.fontSize+';letter-spacing:'+cs.letterSpacing+';'+
      'text-transform:'+cs.textTransform+';color:'+u.col+';text-align:left';
    out.push(d);});});
  el.style.visibility='hidden';el.setAttribute('data-flat','');
});
// hidden originals keep the flex stacks (end card, brand beat) in place; drop their text afterwards
out.forEach(function(d){tn.appendChild(d)});
tn.querySelectorAll('[data-flat]').forEach(function(el){var r=el.getBoundingClientRect(),
  s=document.createElement('div');s.style.cssText='width:'+r.width+'px;height:'+r.height+'px;flex:none';el.replaceWith(s)});
document.documentElement.setAttribute('data-flat','1');
});
"""

def frame_name(var, ratio, i):
    n, angle = VERSIONS[var]["slug"].split("-")
    return f"TN-Core4Mosquito-{ratio}-TakeBackYourYard-Motion-Meta-{n}-{angle}-S{i:02d}"

def figma_html(var, ratio, i, sc, fonts):
    c = SIZES[ratio]; W, H = round(c["W"] * K), round(c["H"] * K)
    piece = scene_html(ratio, sc, "__LOGO__")
    if sc["kind"] == "photo":
        bg = baked_plate(sc["shot"], ratio)
        if bg:   # swap the live plate (and its mask/offset) for the baked frame background
            piece = re.sub(r'<img class="bg"[^>]*>', '<img class="bg" src="__BG__" alt="" style="top:0;height:100%">', piece)
    piece = scale_px(piece).replace("__LOGO__", logo_uri())
    if sc["kind"] == "photo" and bg:
        piece = piece.replace("__BG__", bg)
    css = scale_px(PIECE_CSS)
    for tn, (fam, _) in FIGMA_FONTS.items():
        css = css.replace(f"'{tn}'", f"'{fam}'")
    title = frame_name(var, ratio, i)
    return title, f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
<style>{fonts}
html,body{{margin:0;padding:0;background:#000;width:{W}px;height:{H}px;overflow:hidden}}
{css}{FIGMA_CSS}</style></head><body>
{piece}
<script>{FLATTEN_JS}</script>
</body></html>"""

def bake(p, W, H):
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--window-size={W},{H}",
                          "--virtual-time-budget=4000", "--dump-dom", p.as_uri()],
                         check=True, capture_output=True, text=True, encoding="utf-8").stdout
    assert 'data-flat="1"' in dom, f"flatten did not run: {p.name}"
    dom = re.sub(r"<script>.*?</script>", "", dom, flags=re.S)
    p.write_text("<!doctype html>" + dom, encoding="utf-8")

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    for old in list(ROOT.glob("*/*/*.html")) + list(ROOT.glob("*.zip")):
        old.unlink()
    (ROOT / ".gitignore").write_text("# embeds licensed fonts: keep local, never commit\n*\n", encoding="utf-8")
    fonts = figma_fonts(); files = []
    for var, v in VERSIONS.items():
        for ratio, c in SIZES.items():
            d = ROOT / v["slug"] / ratio; d.mkdir(parents=True, exist_ok=True)
            for i, sc in enumerate(v["scenes"], 1):
                title, html = figma_html(var, ratio, i, sc, fonts)
                p = d / f"{title}.html"; p.write_text(html, encoding="utf-8")
                bake(p, round(c["W"] * K), round(c["H"] * K)); files.append(p)
                print("html", p.relative_to(ROOT))
    z = ROOT / "TN-Mosquito-Core4-HTML-Figma.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            zf.write(p, p.relative_to(ROOT))
    print(len(files), "files,", z.name, round(z.stat().st_size / 1e6, 1), "MB")
    return files

if __name__ == "__main__":
    main()
