"""Convert the React+Tailwind code that Figma's get_design_context returns into plain HTML with inline CSS.

Only the subset of Tailwind that Figma emits is handled; anything unknown raises, so a silent drop
can never change a layout. Used by build_templates.py.
"""
from __future__ import annotations

import html
import re

SIDES = {"left": "left", "right": "right", "top": "top", "bottom": "bottom"}
NAMED = {"black": "#000", "white": "#fff", "transparent": "transparent"}
WEIGHTS = {"font-thin": 100, "font-light": 300, "font-normal": 400, "font-medium": 500,
           "font-semibold": 600, "font-bold": 700, "font-extrabold": 800, "font-black": 900}
ALIGN = {"items-center": "center", "items-start": "flex-start", "items-end": "flex-end", "items-stretch": "stretch"}
JUSTIFY = {"justify-center": "center", "justify-between": "space-between", "justify-start": "flex-start",
           "justify-end": "flex-end"}
IGNORE = {"content-stretch", "not-italic", "shrink-0"}


def val(v: str) -> str:
    """Tailwind length token -> CSS."""
    if v.startswith("[") and v.endswith("]"):
        v = v[1:-1].replace("_", " ")
        if "calc(" in v:
            v = re.sub(r"(?<=[\d%a-z)])([+-])(?=[\d(.])", r" \1 ", v)
        return v
    if v == "0":
        return "0"
    if v == "full":
        return "100%"
    if re.fullmatch(r"\d+/\d+", v):
        a, b = v.split("/")
        return f"{int(a) / int(b) * 100:g}%"
    if v == "px":
        return "1px"
    if re.fullmatch(r"\d+(\.\d+)?", v):
        return f"{float(v) * 4:g}px"
    raise ValueError(f"length {v!r}")


def color(v: str) -> str:
    if v.startswith("["):
        return v[1:-1].replace("_", " ")
    if v in NAMED:
        return NAMED[v]
    raise ValueError(f"color {v!r}")


def is_color(v: str) -> bool:
    inner = v[1:-1] if v.startswith("[") else v
    return inner.startswith(("#", "rgb", "hsl")) or v in NAMED


def classes_to_css(cls: str) -> str:
    css: dict[str, str] = {}
    tx = ty = rot = None
    grad = {"dir": None, "from": None, "fromPos": "", "to": None, "toPos": ""}
    for c in cls.split():
        if c in IGNORE:
            continue
        if c == "absolute":
            css["position"] = "absolute"
        elif c == "relative":
            css["position"] = "relative"
        elif c == "block":
            css["display"] = "block"
        elif c == "flex":
            css["display"] = "flex"
        elif c == "flex-none":
            css["flex"] = "none"
        elif c == "flex-col":
            css["flex-direction"] = "column"
        elif c in ALIGN:
            css["align-items"] = ALIGN[c]
        elif c in JUSTIFY:
            css["justify-content"] = JUSTIFY[c]
        elif c == "size-full":
            css["width"] = css["height"] = "100%"
        elif c == "inset-0":
            css.update(top="0", right="0", bottom="0", left="0")
        elif c == "pointer-events-none":
            css["pointer-events"] = "none"
        elif c == "max-w-none":
            css["max-width"] = "none"
        elif c == "min-w-full":
            css["min-width"] = "100%"
        elif c == "object-cover":
            css["object-fit"] = "cover"
        elif c in ("overflow-hidden", "overflow-clip"):
            css["overflow"] = "hidden" if c == "overflow-hidden" else "clip"
        elif c == "whitespace-nowrap":
            css["white-space"] = "nowrap"
        elif c == "text-center":
            css["text-align"] = "center"
        elif c == "text-left":
            css["text-align"] = "left"
        elif c == "text-right":
            css["text-align"] = "right"
        elif c == "mix-blend-soft-light":
            css["mix-blend-mode"] = "soft-light"
        elif c == "mb-0":
            css["margin-bottom"] = "0"
        elif c in WEIGHTS:
            css["font-weight"] = str(WEIGHTS[c])
        elif c.startswith("font-['"):
            css["font-family"] = "var(--kfont)"
        elif c == "leading-none":
            css["line-height"] = "1"
        elif c.startswith("leading-["):
            css["line-height"] = val(c[8:])
        elif c.startswith("tracking-["):
            css["letter-spacing"] = val(c[9:])
        elif c.startswith("rounded-["):
            css["border-radius"] = val(c[8:])
        elif c == "rounded-full":
            css["border-radius"] = "9999px"
        elif c.startswith("gap-"):
            css["gap"] = val(c[4:])
        elif re.match(r"^p[xytrbl]?-", c):
            k, v = c.split("-", 1)
            v = val(v)
            m = {"p": ["padding"], "px": ["padding-left", "padding-right"], "py": ["padding-top", "padding-bottom"],
                 "pt": ["padding-top"], "pb": ["padding-bottom"], "pl": ["padding-left"], "pr": ["padding-right"]}[k]
            for p in m:
                css[p] = v
        elif c.startswith("size-"):
            css["width"] = css["height"] = val(c[5:])
        elif c.startswith("min-w-["):
            css["min-width"] = val(c[6:])
        elif c.startswith("w-"):
            css["width"] = val(c[2:])
        elif c.startswith("h-"):
            css["height"] = val(c[2:])
        elif c.startswith("inset-["):
            parts = val(c[6:]).split()
            t, r, b, l = (parts * 4)[:4] if len(parts) == 1 else (parts + parts[:2])[:4] if len(parts) == 2 else parts
            css.update(top=t, right=r, bottom=b, left=l)
        elif re.match(r"^-?(left|right|top|bottom)-", c):
            neg = c.startswith("-")
            side, v = c.lstrip("-").split("-", 1)
            v = val(v)
            css[SIDES[side]] = f"-{v}" if neg else v
        elif re.match(r"^-?translate-[xy]-", c):
            neg = c.startswith("-")
            axis, v = c.lstrip("-").split("-")[1], c.lstrip("-").split("-", 2)[2]
            v = val(v)
            v = f"-{v}" if neg else v
            if axis == "x":
                tx = v
            else:
                ty = v
        elif re.match(r"^-?rotate-", c):
            neg = c.startswith("-")
            v = c.lstrip("-")[7:]
            v = v[1:-1] if v.startswith("[") else f"{v}deg"
            rot = f"-{v}" if neg else v
        elif c.startswith("text-"):
            v = c[5:]
            if is_color(v):
                css["color"] = color(v)
            else:
                css["font-size"] = val(v)
        elif c == "bg-gradient-to-b":
            grad["dir"] = "to bottom"
        elif c.startswith("bg-"):
            css["background-color"] = color(c[3:])
        elif c.startswith("from-"):
            v = c[5:]
            if is_color(v):
                grad["from"] = color(v)
            else:
                grad["fromPos"] = " " + val(v)
        elif c.startswith("to-"):
            v = c[3:]
            if is_color(v):
                grad["to"] = color(v)
            else:
                grad["toPos"] = " " + val(v)
        elif c.startswith("[") and c.endswith("]") and ":" in c:
            k, v = c[1:-1].split(":", 1)
            css[k] = v.replace("_", " ")
        else:
            raise ValueError(f"unknown class {c!r}")
    parts = []
    if tx or ty:
        parts.append(f"translate({tx or 0}, {ty or 0})")
    if rot:
        parts.append(f"rotate({rot})")
    if parts:
        css["transform"] = " ".join(parts)
    if grad["dir"]:
        css["background-image"] = (f"linear-gradient({grad['dir']}, {grad['from']}{grad['fromPos']}, "
                                   f"{grad['to']}{grad['toPos']})")
    # text-box-edge/trim need the shorthand order Chrome ships: text-box: trim-both cap alphabetic
    if "text-box-trim" in css or "text-box-edge" in css:
        trim = css.pop("text-box-trim", "trim-both")
        edge = css.pop("text-box-edge", "cap alphabetic")
        css["text-box"] = f"{trim} {edge}"
    return ";".join(f"{k}:{v}" for k, v in css.items())


def jsx_to_html(src: str, asset) -> tuple[str, list[str]]:
    """Return (html, asset keys used). `asset(path)` maps a saved asset path to a key."""
    consts = dict(re.findall(r'const (\w+) = "([^"]+)";', src))
    m = re.search(r"return \(\s*(.*)\s*\);\s*\}\s*$", src, re.S)
    if not m:
        raise ValueError("no JSX return block")
    j = m.group(1)
    used: list[str] = []

    def src_attr(mm):
        key = asset(consts[mm.group(1)])
        used.append(key)
        return f'data-a="{key}"'

    j = re.sub(r"src=\{(\w+)\}", src_attr, j)
    j = re.sub(r'className="([^"]*)"', lambda mm: f'style="{html.escape(classes_to_css(mm.group(1)))}"', j)
    j = re.sub(r"\{`([^`]*)`\}", lambda mm: html.escape(mm.group(1), quote=False), j)
    j = re.sub(r'\{"([^"]*)"\}', lambda mm: html.escape(mm.group(1), quote=False), j)
    j = re.sub(r"\baria-hidden(?=[\s>])", 'aria-hidden="true"', j)
    j = re.sub(r"<img([^>]*?)\s*/>",
               lambda mm: "<img" + mm.group(1) + ("" if "alt=" in mm.group(1) else ' alt=""') + ">", j)
    j = re.sub(r"<(\w+)([^<>]*?)\s*/>", r"<\1\2></\1>", j)
    if "{" in re.sub(r'style="[^"]*"', "", j):
        raise ValueError("unconverted JSX expression left: " + re.search(r".{40}\{.{40}", j, re.S).group(0))
    return j, used
