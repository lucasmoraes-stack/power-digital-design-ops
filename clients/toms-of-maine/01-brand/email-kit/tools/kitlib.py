"""kitlib.py - shared code for the Tom's of Maine email module library.

Used by compose.py, build_library.py, export_jpg.py and fidelity.py. Nothing here
is a command; import it.

Main pieces
-----------
- Paths: KIT (email-kit folder), BRAND (01-brand), CLIENT (clients/toms-of-maine).
- Images: resolve_image(name) finds a file by name in IMAGE_DIRS and, when the
  original is heavy, writes a web-sized derivative to assets/img/ (cached).
- SVG: inline_svg(name, color) inlines an SVG asset recolored (leaf sprigs,
  waves, seals), so the composed HTML stays layered and editable after a Figma
  page-capture import.
- Renderer: a Jinja2 environment over modules/*.j2 with the filters the
  templates use, plus render_email(spec, out_path).

Spec format and module slots: see tools/README.md and modules/registry.json.
Requires Jinja2 and Pillow (both installed on this machine, checked 2026-10-06).
"""
from __future__ import annotations

import copy
import hashlib
import html
import json
import math
import os
import re
from pathlib import Path

from PIL import Image

KIT = Path(__file__).resolve().parents[1]
BRAND = KIT.parent
CLIENT = BRAND.parent
REPO = CLIENT.parents[1]
FONTS = BRAND / "identity" / "fonts"
MODULES = KIT / "modules"
RENDER = KIT / "render"
DERIV = KIT / "assets" / "img"
WORK = CLIENT / "03-work" / "email"
DELIVER = CLIENT / "04-deliverables" / "email"

IMAGE_DIRS = [
    KIT / "assets",
    KIT / "assets" / "img",
    KIT / "assets" / "source",
    BRAND / "photos" / "figma-lab",
]

# Derivative policy: originals above these limits get a resized copy in assets/img/.
# 2400 px on the long edge keeps 2x detail for any crop up to ~2x zoom of a 600 layout.
DERIV_MAX_EDGE = 2400
DERIV_MAX_BYTES = 900_000


# ----------------------------------------------------------------------------
# small helpers
# ----------------------------------------------------------------------------

def load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def deep_merge(base, over):
    """Merge dict `over` into a copy of `base` (lists and scalars are replaced)."""
    if not isinstance(base, dict) or not isinstance(over, dict):
        return copy.deepcopy(over)
    out = copy.deepcopy(base)
    for k, v in over.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def relpath(target: Path, start: Path) -> str:
    return Path(os.path.relpath(Path(target).resolve(), Path(start).resolve())).as_posix()


def num(v):
    """Format a number for CSS: 12.0 -> '12', 12.345 -> '12.345'."""
    if isinstance(v, (int, float)):
        return f"{round(v, 3):g}"
    return str(v)


def px(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return f"{num(v)}px"
    return str(v)


# ----------------------------------------------------------------------------
# images
# ----------------------------------------------------------------------------

class ImageNotFound(FileNotFoundError):
    pass


def find_image(name: str) -> Path:
    p = Path(name)
    if p.is_absolute() and p.exists():
        return p
    for d in IMAGE_DIRS:
        cand = d / name
        if cand.exists():
            return cand
    raise ImageNotFound(f"image '{name}' not found in: " + ", ".join(str(d) for d in IMAGE_DIRS))


def has_alpha(im: Image.Image) -> bool:
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        a = im.convert("RGBA").getchannel("A")
        return a.getextrema()[0] < 255
    return False


def resolve_image(name: str) -> Path:
    """Path of the file to use in HTML: the original, or a cached derivative."""
    src = find_image(name)
    if src.suffix.lower() == ".svg":
        return src
    size = src.stat().st_size
    with Image.open(src) as im:
        w, h = im.size
        if max(w, h) <= DERIV_MAX_EDGE and size <= DERIV_MAX_BYTES:
            return src
        alpha = has_alpha(im)
        ext = ".png" if alpha else ".jpg"
        DERIV.mkdir(parents=True, exist_ok=True)
        out = DERIV / f"{src.stem}{ext}"
        if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
            return out
        im = im.convert("RGBA" if alpha else "RGB")
        scale = min(1.0, DERIV_MAX_EDGE / max(w, h))
        if scale < 1:
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        if alpha:
            im.save(out, optimize=True)
        else:
            im.save(out, quality=90, optimize=True, progressive=True)
        return out


def image_size(name: str) -> tuple[int, int]:
    p = find_image(name)
    if p.suffix.lower() == ".svg":
        m = re.search(rb'width="([\d.]+)"\s+height="([\d.]+)"', p.read_bytes()[:400])
        return (float(m.group(1)), float(m.group(2))) if m else (100, 100)
    with Image.open(p) as im:
        return im.size


# ----------------------------------------------------------------------------
# SVG inlining (recolorable decor, dividers, seals)
# ----------------------------------------------------------------------------

_svg_cache: dict[str, str] = {}


def inline_svg(name: str, color: str | None = None, cls: str = "", style: str = "",
               drop_fill: str | None = None, uid: str = "") -> str:
    """Return the SVG markup of asset `name`, recolored.

    color: replaces the single solid fill color of the drawing (white or a hex)
    drop_fill: remove every element filled with this color (e.g. a baked numeral)
    uid: suffix added to ids (gradients) so two copies of a seal can coexist.
    """
    p = find_image(name)
    if name not in _svg_cache:
        _svg_cache[name] = p.read_text(encoding="utf-8")
    svg = _svg_cache[name]
    svg = re.sub(r"<\?xml[^>]*>", "", svg).strip()
    if drop_fill:
        svg = re.sub(r'<path[^>]*fill="%s"[^>]*/>' % re.escape(drop_fill), "", svg, flags=re.I)
    if color:
        fills = [f for f in re.findall(r'fill="(#[0-9A-Fa-f]{3,8}|white|black)"', svg)]
        solid = [f for f in dict.fromkeys(fills) if f.lower() != "none"]
        if len(solid) == 1:
            svg = svg.replace(f'fill="{solid[0]}"', f'fill="{color}"')
        strokes = list(dict.fromkeys(re.findall(r'stroke="(#[0-9A-Fa-f]{3,8}|white)"', svg)))
        if len(strokes) == 1 and not solid:
            svg = svg.replace(f'stroke="{strokes[0]}"', f'stroke="{color}"')
    if uid:
        ids = set(re.findall(r'id="([^"]+)"', svg))
        for i in ids:
            if "paint" in i or "clip" in i or "filter" in i or "pattern" in i or "image" in i:
                svg = svg.replace(f'id="{i}"', f'id="{i}{uid}"').replace(f"url(#{i})", f"url(#{i}{uid})").replace(f'href="#{i}"', f'href="#{i}{uid}"')
    # drop Figma group ids (noise for import) but keep defs ids
    svg = re.sub(r'\s+id="(?!paint|clip|filter|pattern|image)[^"]*"', "", svg)
    attrs = ' preserveAspectRatio="none"' if "preserveAspectRatio" not in svg[:300] else ""
    svg = re.sub(r"<svg\b", f'<svg class="{cls}" style="{style}"{attrs} aria-hidden="true"', svg, count=1)
    svg = re.sub(r'(<svg[^>]*?)\s(width|height)="[^"]*"', r"\1", svg, count=1)
    svg = re.sub(r'(<svg[^>]*?)\s(width|height)="[^"]*"', r"\1", svg, count=1)
    return svg


# ----------------------------------------------------------------------------
# geometry helpers
# ----------------------------------------------------------------------------

def figma_gradient(w: float, h: float, p0, p1, stops) -> str:
    """CSS linear-gradient equivalent of a Figma linear gradient given by its
    handle positions p0 -> p1 (fractions of the layer box, as read in Figma) and
    stops [(color, position 0..1), ...]. Exact for any aspect ratio."""
    x0, y0 = p0[0] * w, p0[1] * h
    x1, y1 = p1[0] * w, p1[1] * h
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy or 1.0
    ang = math.degrees(math.atan2(dx, -dy)) % 360
    ux, uy = math.sin(math.radians(ang)), -math.cos(math.radians(ang))
    css_len = abs(w * ux) + abs(h * uy)
    cx, cy = w / 2, h / 2
    t_center = ((cx - x0) * dx + (cy - y0) * dy) / L2
    # figma t grows by 1 over distance sqrt(L2) along u
    out = []
    for color, pos in stops:
        dist = (pos - t_center) * math.sqrt(L2)
        css_pos = 50 + 100 * dist / css_len
        out.append(f"{color} {css_pos:.2f}%")
    return f"linear-gradient({ang:.2f}deg,{','.join(out)})"


# ----------------------------------------------------------------------------
# style builders used by the templates
# ----------------------------------------------------------------------------

FAMILIES = {
    "nk": "var(--font-display-family-css)",
    "rubik": "var(--font-label-family-css)",
    "gotham": "var(--font-gotham-family-css)",
}


def tracking(v):
    """-2 -> '-0.02em' (Figma percent); strings pass through."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return f"{v / 100:g}em"
    return str(v)


def _clean(d) -> dict:
    return {k: v for k, v in dict(d or {}).items() if _present(v)}


def text_style(it: dict) -> str:
    it = _clean(it)
    s = {}
    if it.get("family"):
        s["font-family"] = FAMILIES.get(it["family"], it["family"])
    if it.get("weight"):
        s["font-weight"] = str(it["weight"])
    if it.get("size"):
        s["font-size"] = px(it["size"])
    if it.get("line"):
        line = it["line"]
        s["line-height"] = px(line) if isinstance(line, (int, float)) and line > 3 else num(line)
    if it.get("tr") is not None:
        s["letter-spacing"] = tracking(it["tr"])
    if it.get("color"):
        s["color"] = it["color"]
    if it.get("w"):
        s["width"] = px(it["w"])
    if it.get("maxw"):
        s["max-width"] = px(it["maxw"])
    if it.get("align"):
        s["text-align"] = it["align"]
    if it.get("upper") is True:
        s["text-transform"] = "uppercase"
    if it.get("upper") is False:
        s["text-transform"] = "none"
    if it.get("italic"):
        s["font-style"] = "italic"
    if it.get("underline"):
        s["text-decoration"] = "underline"
        s["text-underline-offset"] = px(it.get("underline_offset", 2.5))
        s["text-decoration-thickness"] = px(it.get("underline_thickness", 1.4))
    if it.get("opacity") is not None:
        s["opacity"] = num(it["opacity"])
    if it.get("shadow"):
        s["text-shadow"] = it["shadow"]
    if it.get("gradient"):
        s["background-image"] = it["gradient"]
        s["-webkit-background-clip"] = "text"
        s["background-clip"] = "text"
        s["color"] = "transparent"
    if it.get("trim") is False:
        s["text-box"] = "normal"
    if it.get("nowrap"):
        s["white-space"] = "nowrap"
    if it.get("x") is not None:  # horizontal offset inside a stack
        s["position"] = "relative"
        s["left"] = px(it["x"])
    return ";".join(f"{k}:{v}" for k, v in s.items() if v is not None)


def box_style(l: dict, extra: dict | None = None) -> str:
    """Absolute layer box. Rotation `rot` uses the Figma sign (positive =
    counterclockwise) and turns about the box center."""
    l = _clean(l)
    extra = _clean(extra)
    s = {"left": px(l.get("x", 0)), "top": px(l.get("y", 0))}
    if l.get("bottom") is not None:
        s.pop("top")
        s["bottom"] = px(l["bottom"])
    if l.get("right") is not None:
        s.pop("left")
        s["right"] = px(l["right"])
    if l.get("w") is not None:
        s["width"] = px(l["w"])
    if l.get("h") is not None:
        s["height"] = px(l["h"])
    t = []
    if l.get("rot"):
        t.append(f"rotate({num(-l['rot'])}deg)")
    if l.get("flipx"):
        t.append("scaleX(-1)")
    if l.get("flipy"):
        t.append("scaleY(-1)")
    if t:
        s["transform"] = " ".join(t)
    if l.get("z") is not None:
        s["z-index"] = str(l["z"])
    if l.get("opacity") is not None:
        s["opacity"] = num(l["opacity"])
    if l.get("blend"):
        s["mix-blend-mode"] = l["blend"]
    if l.get("blur"):
        s["filter"] = f"blur({num(l['blur'])}px)"
    if l.get("radius") is not None:
        s["border-radius"] = px(l["radius"])
    if extra:
        s.update(extra)
    return ";".join(f"{k}:{v}" for k, v in s.items() if v is not None)


SHADOWS = {
    # 5-layer floating packshot shadow (10/8 hero mouthwash), black 29/26/15/4/1 %
    # Figma drop-shadow blur == CSS drop-shadow blur radius; values at 600.
    "float": "drop-shadow(4px 5px 14.5px rgba(0,0,0,.29)) drop-shadow(16.5px 20px 26px rgba(0,0,0,.26)) drop-shadow(36.5px 45.5px 35px rgba(0,0,0,.15)) drop-shadow(65.5px 80.5px 41.5px rgba(0,0,0,.04)) drop-shadow(102px 126px 45.5px rgba(0,0,0,.01))",
    # heavier variant (10/8 hero carton) black 54/47/28/8/1 %
    "float-strong": "drop-shadow(4px 5px 13.5px rgba(0,0,0,.54)) drop-shadow(16.5px 20px 24.5px rgba(0,0,0,.47)) drop-shadow(36.5px 45.5px 33px rgba(0,0,0,.28)) drop-shadow(65.5px 80.5px 39.5px rgba(0,0,0,.08)) drop-shadow(102px 126px 43px rgba(0,0,0,.01))",
    # July sale packshots (7.1, 7.3), shadow toward bottom-left
    "float-left": "drop-shadow(-2.8px 3.4px 9.5px rgba(0,0,0,.30)) drop-shadow(-11.1px 13.4px 17.2px rgba(0,0,0,.20)) drop-shadow(-24.5px 30px 23.3px rgba(0,0,0,.10)) drop-shadow(-43.9px 53.4px 27.8px rgba(0,0,0,.04)) drop-shadow(-68.4px 83.4px 30px rgba(0,0,0,.01))",
    # grounding shadow under product trios (8/20, 8/24)
    "ground": "drop-shadow(0 2.5px 6px rgba(0,0,0,.30)) drop-shadow(0 10px 11px rgba(0,0,0,.26)) drop-shadow(0 22.5px 15px rgba(0,0,0,.15)) drop-shadow(0 40px 17.5px rgba(0,0,0,.04)) drop-shadow(0 67.5px 19px rgba(0,0,0,.01))",
    # 10/20 hero cluster: blur 9.5/17.5/24/28/31, black 29/26/15/4/1 %
    "cluster": "drop-shadow(2px 2.5px 9.5px rgba(0,0,0,.29)) drop-shadow(8.25px 10px 17.5px rgba(0,0,0,.26)) drop-shadow(18.25px 22.75px 24px rgba(0,0,0,.15)) drop-shadow(32.75px 40.25px 28px rgba(0,0,0,.04)) drop-shadow(51px 63px 31px rgba(0,0,0,.01))",
}


def img_style(l: dict) -> str:
    """Style of the <img> inside a layer box: fit (cover|contain|fill|crop)."""
    l = _clean(l)
    fit = l.get("fit", "contain")
    s = {}
    if fit == "crop":
        c = l.get("crop") or {}
        s.update({"position": "absolute", "left": px(c.get("x", 0)), "top": px(c.get("y", 0)),
                  "width": px(c.get("w")), "height": px(c.get("h")) if c.get("h") else "auto",
                  "max-width": "none"})
    else:
        s.update({"width": "100%", "height": "100%", "object-fit": fit})
        if l.get("pos"):
            s["object-position"] = l["pos"]
    if l.get("shadow"):
        s["filter"] = SHADOWS.get(l["shadow"], l["shadow"])
    if l.get("img_radius") is not None:
        s["border-radius"] = px(l["img_radius"])
    return ";".join(f"{k}:{v}" for k, v in s.items() if v is not None)


def _present(v) -> bool:
    import jinja2
    return v is not None and v != "" and not isinstance(v, jinja2.Undefined)


UNITLESS_CSS = ("opacity", "z-index", "font-weight", "flex", "flex-grow", "order")


def style(d: dict | None) -> str:
    """dict -> 'k:v;k:v' (numbers get px except unitless properties; empty values skipped)."""
    if not d:
        return ""
    out = []
    for k, v in d.items():
        if not _present(v):
            continue
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            v = num(v) if k in UNITLESS_CSS else px(v)
        out.append(f"{k}:{v}")
    return ";".join(out)


def merge(d, over):
    out = dict(d or {})
    out.update(over or {})
    return out


# ----------------------------------------------------------------------------
# renderer
# ----------------------------------------------------------------------------

class Renderer:
    """Jinja2 renderer bound to an output folder (image paths are made relative
    to it). Use inline_images=True to embed every image as a data URI."""

    def __init__(self, out_dir: Path, inline_images: bool = False, image_transform=None):
        import jinja2
        self.out_dir = Path(out_dir)
        self.inline_images = inline_images
        self.image_transform = image_transform
        self.registry = load_json(MODULES / "registry.json")
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(MODULES)),
            autoescape=False, trim_blocks=True, lstrip_blocks=True,
            undefined=jinja2.ChainableUndefined,
        )
        self._uid = 0
        f = self.env.filters
        f["img"] = self.img_url
        f["px"] = px
        f["num"] = num
        f["tstyle"] = text_style
        f["bstyle"] = box_style
        f["istyle"] = img_style
        f["style"] = style
        f["merge"] = merge
        f["e"] = lambda s: html.escape(str(s), quote=True)
        g = self.env.globals
        g["svg"] = self.svg
        g["uid"] = self.uid
        g["figma_gradient"] = figma_gradient
        g["shadow"] = lambda k: SHADOWS.get(k, k)
        g["registry"] = self.registry
        g["image_size"] = image_size

    def uid(self) -> str:
        self._uid += 1
        return f"u{self._uid}"

    def img_url(self, name: str) -> str:
        if not name:
            return ""
        path = resolve_image(name)
        if self.image_transform:
            return self.image_transform(path)
        return relpath(path, self.out_dir)

    def svg(self, name, color=None, cls="", style_="", drop_fill=None):
        return inline_svg(name, color=color, cls=cls, style=style_, drop_fill=drop_fill, uid=self.uid())

    # -- modules ------------------------------------------------------------
    def module_defaults(self, mid: str, variant: str | None) -> dict:
        reg = self.registry["modules"].get(mid)
        if not reg:
            raise KeyError(f"unknown module id {mid}")
        base = copy.deepcopy(reg.get("defaults", {}))
        if variant:
            vs = reg.get("variants", {})
            if variant not in vs:
                raise KeyError(f"{mid}: unknown variant '{variant}' (known: {', '.join(vs)})")
            base = deep_merge(base, vs[variant].get("defaults", {}))
        return base

    def prepare(self, m: dict) -> dict:
        mid = m["module"]
        merged = deep_merge(self.module_defaults(mid, m.get("variant")), m)
        if "children" in merged:
            merged["children"] = [self.prepare(c) for c in merged["children"]]
        return merged

    def render_module(self, m: dict) -> str:
        m = self.prepare(m)
        reg = self.registry["modules"][m["module"]]
        tpl = self.env.get_template(reg["template"])
        return tpl.render(m=m, r=self)

    def render_child(self, m: dict) -> str:
        reg = self.registry["modules"][m["module"]]
        return self.env.get_template(reg["template"]).render(m=m, r=self)

    def css_bundle(self) -> str:
        fonts_rel = relpath(FONTS, self.out_dir)
        parts = []
        for name in ("fonts.css", "tokens.css", "kit.css"):
            css = (RENDER / name).read_text(encoding="utf-8")
            parts.append(css.replace("__FONTS__", fonts_rel))
        return "\n".join(parts)

    def render_email(self, spec: dict) -> str:
        body = "\n".join(self.render_module(m) for m in spec["modules"])
        tpl = self.env.get_template("_email.j2")
        return tpl.render(spec=spec, body=body, css=self.css_bundle())
