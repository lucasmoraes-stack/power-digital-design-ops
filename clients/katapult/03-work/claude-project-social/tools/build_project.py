"""Assemble the Katapult Social Studio Claude Project package (instructions, knowledge, skills).

Usage: python tools/build_project.py

Reads
  src/project-instructions.md, src/knowledge/*.md           written for the project
  src/kit-head.md + studio/catalog.json                     -> knowledge/02-studio-kit.md (layout catalogue)
  src/library-head.md + studio/catalog.json                 -> knowledge/03-image-library.md
  src/skills/<name>/SKILL.md                                -> knowledge/05-banner-craft.md, 06-katapult-patterns.md
                                                               and dist/skills/<name>.zip (upload as claude.ai skills)
Writes dist/ (flat knowledge folder, as the Project needs it) and refuses to finish if another client's name,
an internal path or a long dash appears in it.
"""
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SRC = HERE / "src"
DIST = HERE / "dist"
CAT = json.loads((HERE / "studio" / "catalog.json").read_text(encoding="utf-8"))
BOXES = json.loads((HERE / "studio" / "boxes.json").read_text(encoding="utf-8"))

BLOCKED = [
    "roku", "tom's of maine", "toms of maine", "habit outdoors", "truly nolen", "canadian insulin", "cdi",
    "vazio", "matarasso", "progressive global", "clients/", "03-work", "01-brand/", ".claude", "claude code",
    "copywriter agent", "designer agent", "brand guardian", "email-ops",
]
SKILLS = {"katapult-banner-craft": "05-banner-craft.md", "katapult-patterns": "06-katapult-patterns.md"}


def lines_of(s):
    if s.get("lines"):
        return s["lines"]
    d = s["default"]
    top = re.findall(r'<span(?: class="t[12]")?>', d)
    if s.get("mode") == "markup" and d.startswith("<span"):
        depth, n = 0, 0
        for tok in re.findall(r"</?span[^>]*>", d):
            if tok.startswith("</"):
                depth -= 1
            else:
                n += depth == 0
                depth += 1
        return n + d.count("<br")
    return d.count("<br") + 1 if "<br" in d else None


def catalogue():
    out, fam = [], None
    for code, L in CAT["layouts"].items():
        if L["family"] != fam:
            fam = L["family"]
            out += ["", f"### {fam} · {L['name']}", ""]
        out.append(f"**{code}** ({L['w']}x{L['h']})")
        order = ["headline", "sub", "cta", "photo", "phone", "product1", "product2", "product3"]
        for n, s in sorted(L["slots"].items(), key=lambda kv: order.index(kv[0]) if kv[0] in order else 99):
            if s["kind"] == "image":
                note = "optional, keep the approved mockup" if n == "phone" else ("cutout, fits inside its box" if s["fit"] == "contain" else "photo, fills its box")
                b = BOXES.get(code, {}).get(n)
                if b:
                    shape = "landscape" if b["w"] > b["h"] * 1.15 else ("portrait" if b["h"] > b["w"] * 1.15 else "square")
                    note += f", box {b['w']}x{b['h']} {shape} at x {b['x']}, y {b['y']}"
                out.append(f"- `{n}`: {note}")
                continue
            sample = re.sub(r"<br\s*/?>", "<br>", s["default"])
            ln = lines_of(s)
            meta = []
            if n == "cta" and L["group"] == "template":
                meta.append("the pill scales to fit, keep it to two or three words")
            elif ln:
                meta.append(f"{ln} line{'s' if ln > 1 else ''}")
            elif s["mode"] != "markup":
                meta.append("wraps in its box")
            if s.get("size"):
                meta.append(f"{round(s['size'])}px")
            plain = [re.sub(r"<[^>]+>", "", x) for x in re.split(r"<br\s*/?>|</span>\s*<span[^>]*>", s["default"])]
            longest = max((len(x.strip()) for x in plain), default=0)
            if longest and not (n == "cta" and L["group"] == "template"):
                meta.append(f"longest line {longest} characters")
            out.append(f"- `{n}` ({', '.join(meta)}): `{sample}`")
        out.append("")
    return (SRC / "kit-head.md").read_text(encoding="utf-8") + "\n".join(out).strip() + "\n"


def library():
    cell = lambda s: (s or "").replace("|", "/").replace("\n", " ")
    rows = [f"| `{p['id']}` | {p['size']} | {cell(p['subject'])} | {cell(p.get('people'))} | {p.get('face') or 'none'} | {cell(p['text_space'])} | {cell(p['use'])} | {cell(p['fit'])} | {cell(p['notes'])} |"
            for p in CAT["library"]]
    prods = ["", "## Product cutouts", "", "Transparent cutouts for product slots (T04, T05, T07, T10). `front` view sits upright; `top-down` view was shot from above for flat-lays and reads oddly upright in a template.", "",
             "| id | what it is | view |", "|---|---|---|"]
    prods += [f"| `{p['id']}` | {cell(p['label'])} | {p['view']} |" for p in CAT["products"]]
    return (SRC / "library-head.md").read_text(encoding="utf-8") + "\n".join(rows) + "\n" + "\n".join(prods) + "\n"


def strip_front(text):
    return re.sub(r"^---\n.*?\n---\n+", "", text, flags=re.S)


def scan(root):
    hits = []
    pats = [re.compile(r"(?<![\w-])" + re.escape(t) + (r"(?![\w])" if t[-1].isalnum() else ""), re.I) for t in BLOCKED]
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.suffix == ".zip":
            continue
        text = f.read_text(encoding="utf-8")
        for n, line in enumerate(text.splitlines(), 1):
            for p in pats:
                m = p.search(line)
                if m:
                    hits.append(f"{f.relative_to(root)}:{n}: '{m.group(0)}' in: {line.strip()[:110]}")
            if "—" in line or "–" in line:
                hits.append(f"{f.relative_to(root)}:{n}: long dash in: {line.strip()[:110]}")
    return hits


def main():
    for f in DIST.rglob("*") if DIST.exists() else []:
        if f.is_file():
            f.unlink()
    (DIST / "knowledge").mkdir(parents=True, exist_ok=True)
    (DIST / "skills").mkdir(exist_ok=True)
    shutil.copy(SRC / "project-instructions.md", DIST / "project-instructions.md")
    for f in sorted((SRC / "knowledge").glob("*.md")):
        shutil.copy(f, DIST / "knowledge" / f.name)
    (DIST / "knowledge" / "02-studio-kit.md").write_text(catalogue(), encoding="utf-8")
    (DIST / "knowledge" / "03-image-library.md").write_text(library(), encoding="utf-8")
    for name, kn in SKILLS.items():
        body = (SRC / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        (DIST / "knowledge" / kn).write_text(strip_front(body), encoding="utf-8")
        with zipfile.ZipFile(DIST / "skills" / f"{name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr(f"{name}/SKILL.md", body)
    hits = scan(DIST)
    if hits:
        print("BLOCKED: the package mentions names or characters that must not leave the studio:")
        print("\n".join(hits))
        shutil.rmtree(DIST)
        return 1
    files = sorted(p.relative_to(DIST).as_posix() for p in DIST.rglob("*") if p.is_file())
    words = sum(len((DIST / f).read_text(encoding="utf-8").split()) for f in files if not f.endswith(".zip"))
    print(f"OK: {len(files)} files, about {words * 1.4 / 1000:.0f}k tokens of knowledge, no blocked terms")
    for f in files:
        print(f"  {f}  {(DIST / f).stat().st_size / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
