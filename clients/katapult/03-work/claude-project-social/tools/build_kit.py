"""Build the Katapult Social Studio kit: the exact markup of every layout the Studio can render, with its slots.

Usage: python tools/build_kit.py

Reads
  01-brand/templates/html/tNN-<ratio>.html            the 10 social templates x 4 ratios (rebuilt 1:1 from Figma)
  04-deliverables/banners/<job>/html*/...V1...html   the 4 approved banner patterns x 8 sizes (V1 statics)
  01-brand/photos/library/*.jpg + catalog.md         the Image Library
  03-work/banners/2026-kat26019-top-items/img-knolling/*.png + template product cutouts
  01-brand/identity/AktivGrotesk-*.otf              fonts, subset to Latin
Writes
  studio/assets/<kind>/<name>                         every raster the Studio serves (photos, products, layout art)
  studio/kit.json                                     layouts {code: {w, h, group, html, css, slots}}, fonts, svg art
  studio/catalog.json                                 what the Project knowledge lists (codes, slots, defaults)

A slot is the only thing a post file may change. Templates: headline / sub / cta (text), photo / phone /
product1..3 (images). Banner patterns: headline / sub / cta (class-based inner markup), photo. Legal lines,
logos and every position stay locked.
"""
import base64
import hashlib
import io
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from PIL import Image

HERE = Path(__file__).resolve().parents[1]
KAT = HERE.parents[1]                                   # clients/katapult
TPL = KAT / "01-brand" / "templates"
BAN = KAT / "04-deliverables" / "banners"
LIB = KAT / "01-brand" / "photos" / "library"
KNOLL = KAT / "03-work" / "banners" / "2026-kat26019-top-items" / "img-knolling"
FONTS = KAT / "01-brand" / "identity"
OUT = HERE / "studio"
ASSETS = OUT / "assets"

RATIOS = {"1x1": (1200, 1200), "4x5": (1080, 1350), "16x9": (1920, 1080), "9x16": (1080, 1920)}
TEMPLATE_NAMES = {
    1: "Full image", 2: "Split panel, image", 3: "Split, phone in hand", 4: "Product row, 3-up",
    5: "Hero product, bleed", 6: "Top block, photo card", 7: "Top block, product on circle",
    8: "Typographic statement", 9: "Hero photo, full width", 10: "Product trio, circles",
}
SIZES = ["1200x1200", "1200x628", "960x1200", "300x600", "300x250", "160x600", "728x90", "320x50"]
PATTERNS = [  # code, name, file glob per size, frame class prefix
    ("P1", "Knolling flat-lay", "2026-kat26019-top-items/html-knolling/V1/KAT26019-TopItems-{s}-*-V1-Knolling.html"),
    ("P2", "Photo + highlight bars", "2026-kat26020-holiday-disaster/html/V1/KAT26020-HolidayDisaster-{s}-*-V1.html"),
    ("P3A", "Flat brand type, Dark Blue", "2026-kat26021-flat-brand-type/html/V1/KAT26021-FlatBrandType-{s}-*-V1.html"),
    ("P3B", "Flat brand type, Cream", "2026-kat26021-flat-brand-type/html/V2/KAT26021-FlatBrandType-{s}-*-V2.html"),
    ("P4A", "Proof badge, centered", "2026-kat26022-trusted/html/KAT26022-Trusted-{s}-*-V1-OptionA.html"),
    ("P4B", "Proof badge, photo seam", "2026-kat26022-trusted/html/KAT26022-Trusted-{s}-*-V1-OptionB.html"),
]
LEGAL = "Lease-purchase service"

# product cutouts the templates and posts may use: id -> (source, label, view)
PRODUCTS = {
    "headphones": (TPL / "figma/assets/079f3780-b549-4acd-89d1-eec41531e78c.png", "Over-ear headphones, lilac", "front"),
    "tablets": (TPL / "figma/assets/13839e03-4bb4-45ee-b7a8-9a6330319e2d.png", "Three tablets in a row, purple", "front"),
    "laptop-open": (TPL / "figma/assets/c12554d2-04ca-4efc-866b-cb11b0b67db4.png", "Open laptop, green screen", "front"),
    "laptop": (KNOLL / "laptop.png", "Open laptop, silver", "top-down"),
    "fridge": (KNOLL / "fridge.png", "French-door fridge, steel", "front"),
    "washer": (KNOLL / "washer.png", "Front-load washer, white", "front"),
    "tv": (KNOLL / "tv.png", "Flat TV", "front"),
    "tire": (KNOLL / "tire.png", "Tire on alloy wheel", "front"),
    "console": (KNOLL / "console.png", "Game console and controller", "top-down"),
    "vacuum": (KNOLL / "vacuum.png", "Stick vacuum", "front"),
    "nightstand": (KNOLL / "nightstand.png", "Wooden nightstand", "front"),
    "necklace": (KNOLL / "necklace.png", "Gold necklace", "top-down"),
    "couch": (KNOLL / "couch.png", "Three-seat couch, grey", "top-down"),
    "bed": (KNOLL / "bed.png", "Bed with green throw", "top-down"),
    "grill": (KNOLL / "grill.png", "Kettle grill", "top-down"),
}

served = {}        # local relative path -> sha (for dedupe report)
svg_art = {}       # key -> data uri (small vector art, kept inside the page)


def save_raster(kind, name, im, fmt):
    path = ASSETS / kind / f"{name}.{'jpg' if fmt == 'JPEG' else 'webp'}"
    path.parent.mkdir(parents=True, exist_ok=True)
    b = io.BytesIO()
    if fmt == "JPEG":
        im.convert("RGB").save(b, "JPEG", quality=82, optimize=True, progressive=True)
    else:
        im.save(b, "WEBP", quality=86, method=6)
    data = b.getvalue()
    if not path.is_file() or path.read_bytes() != data:
        path.write_bytes(data)
    rel = path.relative_to(OUT).as_posix()
    served[rel] = hashlib.sha1(data).hexdigest()
    return rel


def fit(im, long_side):
    s = min(1.0, long_side / max(im.size))
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS) if s < 1 else im


def has_alpha(im):
    return im.mode in ("RGBA", "LA") and im.getextrema()[-1][0] < 255


raster_cache = {}


def raster(data, kind, hint):
    """Store a raster once by content; photos as JPEG (long side 2400), cutouts as WebP (long side 1800)."""
    key = hashlib.sha1(data).hexdigest()[:10]
    if key in raster_cache:
        return raster_cache[key]
    im = Image.open(io.BytesIO(data))
    im.load()
    if has_alpha(im.convert("RGBA")):
        rel = save_raster(kind, f"{hint}-{key}", fit(im.convert("RGBA"), 1800), "WEBP")
    else:
        rel = save_raster(kind, f"{hint}-{key}", fit(im.convert("RGB"), 2400), "JPEG")
    raster_cache[key] = rel
    return rel


def svg_uri(data):
    key = "svg-" + hashlib.sha1(data).hexdigest()[:10]
    svg_art.setdefault(key, "data:image/svg+xml;base64," + base64.b64encode(data).decode())
    return key


def px(style, prop):
    m = re.search(r"(?:^|;)\s*" + prop + r"\s*:\s*([\d.]+)px", style or "")
    return float(m.group(1)) if m else None


# ---------------------------------------------------------------- templates
def text_nodes(root):
    """Top-level text blocks: a <p>, or a <div> whose element children are all <p>."""
    out = []
    for el in root.find_all(["p", "div"]):
        if el.find_parent(lambda t: t in out):
            continue
        if el.name == "p" and el.get_text(strip=True):
            if el.parent.name == "div" and all(c.name == "p" for c in el.parent.find_all(recursive=False)) \
                    and len(el.parent.find_all("p", recursive=False)) > 1 and el.parent not in out:
                out.append(el.parent)
            elif el.parent not in out:
                out.append(el)
    return out


def font_size(el):
    for node in [el] + el.find_all(["p", "span"]):
        v = px(node.get("style"), "font-size")
        if v:
            return v
    return 0


def image_role(img):
    anc = img
    while anc is not None and not (isinstance(anc, Tag) and anc.get("data-name")):
        anc = anc.parent
    name = (anc.get("data-name") if anc is not None else "") or ""
    n = name.lower()
    if "photo" in n or n.startswith("template-09"):
        return "photo"
    if "hand" in n:
        return "phone"
    if n == "ipad" or n.startswith("adobestock"):
        return "product"
    return None


def build_template(t, ratio):
    src = TPL / "html" / f"t{t:02d}-{ratio}.html"
    soup = BeautifulSoup(src.read_text(encoding="utf-8"), "html.parser")
    art = soup.find(id="art")
    del art["id"]
    w, h = RATIOS[ratio]
    slots = {}
    for img in art.find_all("img"):
        p = (TPL / "html" / img["src"]).resolve()
        data = p.read_bytes()
        role = image_role(img)
        if p.suffix == ".svg":
            img["src"] = "svg:" + svg_uri(data)
            continue
        kind = "products" if role == "product" else "layout"
        img["src"] = raster(data, kind, {"photo": "photo", "phone": "phone", "product": "product"}.get(role, "art"))
        if role == "product":
            n = sum(1 for s in slots if s.startswith("product")) + 1
            role = f"product{n}"
        if role:
            img["data-slot"] = role
            fit_mode = "contain" if role.startswith("product") or role == "phone" else "cover"
            slots[role] = {"kind": "image", "fit": fit_mode, "default": img["src"]}
    for el in art.find_all(True):
        for a in ("data-node-id",):
            if a in el.attrs:
                del el[a]
    blocks = text_nodes(art)
    legal = [b for b in blocks if LEGAL in b.get_text()]
    cta = [b for b in blocks if b.find_parent(attrs={"data-name": "Button"})]
    rest = sorted([b for b in blocks if b not in legal and b not in cta], key=font_size, reverse=True)
    for b in legal:
        b["data-lock"] = "legal"
    if cta:
        cta[0]["data-slot"] = "cta"
        slots["cta"] = {"kind": "text", "mode": "plain", "default": cta[0].get_text(" ", strip=True), "size": font_size(cta[0])}
    names = ["headline", "sub"]
    for name, b in zip(names, rest):
        b["data-slot"] = name
        lines = [p.get_text("", strip=False).strip() for p in b.find_all("p", recursive=False)] if b.name == "div" else None
        spans = b.find_all("span", recursive=False) if b.name == "p" else []
        accent = None
        if len(spans) > 1 and spans[0].get("style") != spans[-1].get("style"):
            accent = "last span"
            default = "".join(s.get_text() for s in spans[:-1]) + "<em>" + spans[-1].get_text() + "</em>"
        elif lines:
            default = "<br>".join(lines)
        else:
            default = re.sub(r"\s+", " ", b.get_text()).strip()
        slots[name] = {"kind": "text", "mode": "lines" if lines else ("accent" if accent else "plain"),
                       "default": default, "size": font_size(b), "lines": len(lines) if lines else None}
    if len(rest) > 2:
        print(f"  note t{t:02d}-{ratio}: {len(rest) - 2} extra text block(s) left locked:",
              [x.get_text(" ", strip=True)[:30] for x in rest[2:]])
    html = str(art)
    return {"w": w, "h": h, "group": "template", "html": html, "slots": slots}


# ---------------------------------------------------------------- banner patterns
BAN_SLOTS = [
    ("headline", ".k20-h, .k21-h, .k22-h, .kn-h"),
    ("sub", ".k21-s2, .k22-s2, .kn-s"),
    ("cta", ".k20-cta, .k21-cta, .k22-cta, .kn-cta"),
]
CSS_DROP = re.compile(r"@font-face\{[^}]*\}|html,body\{[^}]*\}|:root\{[^}]*\}")


def build_banner(code, pattern_glob, size):
    hits = sorted(BAN.glob(pattern_glob.format(s=size)))
    if len(hits) != 1:
        sys.exit(f"{code} {size}: expected one file, got {hits}")
    soup = BeautifulSoup(hits[0].read_text(encoding="utf-8"), "html.parser")
    css = CSS_DROP.sub("", soup.style.get_text()).strip()
    frame = soup.body.find(recursive=False)
    w, h = map(int, size.split("x"))
    slots = {}
    for img in frame.find_all("img"):
        s = img["src"]
        m = re.match(r"data:image/([a-z+]+);base64,(.*)", s, re.S)
        if not m:
            sys.exit(f"{code} {size}: unexpected img src {s[:40]}")
        data = base64.b64decode(m.group(2))
        if m.group(1).startswith("svg"):
            img["src"] = "svg:" + svg_uri(data)
            continue
        is_photo = img.find_parent(class_=re.compile(r"-pic$")) is not None
        img["src"] = raster(data, "layout", "photo" if is_photo else "art")
        if is_photo:
            img["data-slot"] = "photo"
            slots["photo"] = {"kind": "image", "fit": "cover", "default": img["src"]}
    for name, sel in BAN_SLOTS:
        el = frame.select_one(sel)
        if el is None:
            continue
        target = el.find("span", class_="trim") or el
        target["data-slot"] = name
        inner = "".join(str(c) for c in target.contents)
        inner = re.sub(r'\s+style="[^"]*"', "", inner)
        slots[name] = {"kind": "text", "mode": "markup", "default": inner, "size": px(el.get("style"), "font-size")}
    for el in frame.select("[class$=-disc]"):
        el["data-lock"] = "legal"
    return {"w": w, "h": h, "group": "banner", "html": str(frame), "css": css, "slots": slots}


# ---------------------------------------------------------------- library, products, fonts
def library():
    subj = json.loads((OUT / "subjects.json").read_text(encoding="utf-8")) if (OUT / "subjects.json").is_file() else {}
    rows = []
    for line in (LIB / "catalog.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| library/([^|]+?)\.jpg \|(.*)", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        file, coll, source, subject, cat, space, use, fitb, rights = cells[:9]
        pid = m.group(1)
        im = Image.open(LIB / f"{pid}.jpg")
        rel = save_raster("library", pid, fit(im.convert("RGB"), 2400), "JPEG")
        rows.append({"id": pid, "path": rel, "size": f"{im.width}x{im.height}", "subject": subject, "category": cat,
                     "text_space": space, "use": use, "fit": fitb, "rights": rights, "notes": cells[9] if len(cells) > 9 else "",
                     "face": subj.get(pid, {}).get("face"), "people": subj.get(pid, {}).get("subject", "")})
    return rows


def products():
    out = []
    for pid, (src, label, view) in PRODUCTS.items():
        im = Image.open(src).convert("RGBA")
        bbox = im.getchannel("A").getbbox()
        im = im.crop(bbox) if bbox else im
        rel = save_raster("products", pid, fit(im, 1800), "WEBP")
        out.append({"id": pid, "path": rel, "label": label, "view": view, "size": f"{im.width}x{im.height}"})
    return out


def fonts():
    from fontTools import subset
    from fontTools.ttLib import TTFont
    out = {}
    text = "".join(chr(c) for c in range(0x20, 0x7F)) + " ’‘“”…•·★–—©®™°×€£¢¡¿áàâãäåçéèêëíìîïñóòôõöúùûüÁÀÂÃÄÅÇÉÈÊËÍÌÎÏÑÓÒÔÕÖÚÙÛÜ%&@#$"
    for w, name in ((300, "Light"), (400, "Regular"), (500, "Medium"), (700, "Bold")):
        f = TTFont(FONTS / f"AktivGrotesk-{name}.otf")
        opts = subset.Options()
        opts.flavor = "woff"
        opts.layout_features = ["kern", "liga", "calt", "tnum", "lnum"]
        sub = subset.Subsetter(opts)
        sub.populate(text=text)
        sub.subset(f)
        b = io.BytesIO()
        f.flavor = "woff"
        f.save(b)
        out[str(w)] = "data:font/woff;base64," + base64.b64encode(b.getvalue()).decode()
    return out


def logos():
    svg = (FONTS / "logo-katapuklt.svg").read_text(encoding="utf-8")
    out = {}
    for name, col in (("pink", "#ED5370"), ("dark-blue", "#131540"), ("white", "#FFFFFF")):
        s = re.sub(r'fill="(?!none)[^"]*"', f'fill="{col}"', svg)
        out[name] = "data:image/svg+xml;base64," + base64.b64encode(s.encode()).decode()
    return out


def main():
    layouts, css = {}, {}
    print("templates")
    for t in range(1, 11):
        for ratio in RATIOS:
            layouts[f"T{t:02d}-{ratio}"] = dict(build_template(t, ratio), name=TEMPLATE_NAMES[t], family=f"T{t:02d}")
    print("banner patterns")
    for code, name, g in PATTERNS:
        for size in SIZES:
            lay = build_banner(code, g, size)
            fam_css = lay.pop("css")
            prev = css.setdefault(code[:2], fam_css)
            if prev != fam_css:
                # same job, different per-size css: keep the longest (they only add size rules)
                css[code[:2]] = max(prev, fam_css, key=len)
            layouts[f"{code}-{size}"] = dict(lay, name=name, family=code)
    lib = library()
    prods = products()
    kit = {"layouts": layouts, "css": css, "svg": svg_art, "fonts": fonts(), "logos": logos(),
           "library": lib, "products": prods}
    (OUT / "kit.json").write_text(json.dumps(kit, ensure_ascii=False), encoding="utf-8")
    cat = {"layouts": {k: {"name": v["name"], "family": v["family"], "w": v["w"], "h": v["h"], "group": v["group"],
                           "slots": v["slots"]} for k, v in layouts.items()},
           "library": lib, "products": prods}
    (OUT / "catalog.json").write_text(json.dumps(cat, ensure_ascii=False, indent=1), encoding="utf-8")
    files = sorted(served)
    size = sum((OUT / f).stat().st_size for f in files)
    print(f"OK: {len(layouts)} layouts, {len(files)} served rasters ({size / 1e6:.1f} MB), {len(svg_art)} svg, "
          f"kit.json {(OUT / 'kit.json').stat().st_size / 1e6:.2f} MB")
    (OUT / "served.json").write_text(json.dumps(served, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
