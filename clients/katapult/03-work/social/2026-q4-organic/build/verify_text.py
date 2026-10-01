"""Independent text check: on-art strings vs copy.md, both directions, plus dash scan."""
import re, pathlib, html
from html.parser import HTMLParser

S = pathlib.Path(r"C:/Users/lucas/AppData/Local/Temp/claude/c--Users-lucas-OneDrive-Desktop-VAZIO-power-digital-ops/93dbe328-a65f-4b12-958f-086bc971a00c/scratchpad")
COPY = pathlib.Path(r"C:/Users/lucas/OneDrive/Desktop/VAZIO/power-digital-ops/clients/katapult/03-work/social/2026-q4-organic/copy.md")
page = (S / "katapult-q4" / "index.html").read_text(encoding="utf-8")
copy = COPY.read_text(encoding="utf-8")

# ---- expected on-art strings, per post, parsed independently ----
LABELS = {"Title:", "Subtext:", "SUBTEXT:", "Question:", "CTA:", "Prompt:"}
expected, ref_headline, all_copy_lines = {}, {}, set()
for m in re.finditer(r"^## Post (\d\d): .+?\n\nFormat: (.+?)\n\n```\n(.*?)\n```", copy, re.S | re.M):
    num, fmt, body = m.group(1), m.group(2), m.group(3)
    lines = body.split("\n")
    exp = []
    for l in lines[1:]:
        s = l.strip()
        all_copy_lines.add(s)
        if not s or s in LABELS or s.startswith("CONCEPT:") or re.fullmatch(r"Slide \d+", s):
            continue
        if s.startswith("HEADLINE: "):
            v = s[len("HEADLINE: "):]
            all_copy_lines.add(v)
            if fmt.startswith("Carousel"):
                ref_headline[num] = v      # carousel HEADLINE is a reference field, not a slide
            else:
                exp.append(v)
            continue
        exp.append(s)
    expected[num] = exp

# ---- on-art strings from the page ----
EXCL = ("kp-slot", "kp-logo", "kp-icon-slot", "kp-sticker-zone", "kp-ph", "kp-cut", "kp-ico")   # placeholder labels, never art copy
GROUP_TAGS = {"h4", "h5", "p", "li"}
class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []   # (tag, is_group, excluded)
        self.art = None; self.depth_art = 0
        self.groups = {}; self.stray = []
        self.gstack = []
        self.excl = 0; self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = a.get("class", "") or ""
        if tag == "article" and "kp-post" in cls:
            self.art = a.get("id"); self.groups[self.art] = []
        if self.art is None or tag in ("br","img","input","hr","wbr"):
            return
        ex = any(c in cls.split() for c in EXCL)
        sk = tag in ("svg", "script", "style")
        grp = (tag in GROUP_TAGS or (tag == "span" and ("kp-cta" in cls or "kp-flow-label" in cls))) and not self.excl
        self.stack.append((tag, grp, ex, sk))
        if ex: self.excl += 1
        if sk: self.skip += 1
        if grp: self.gstack.append([])
    def handle_endtag(self, tag):
        if self.art is None: return
        if tag == "article" and not self.stack:
            self.art = None; return
        if not self.stack: return
        t, grp, ex, sk = self.stack.pop()
        if ex: self.excl -= 1
        if sk: self.skip -= 1
        if grp:
            txt = "".join(self.gstack.pop()).strip()
            if txt: self.groups[self.art].append(txt)
        if not self.stack and tag == "article":
            self.art = None
    def handle_data(self, d):
        if self.art is None or self.excl or self.skip: return
        if self.gstack: self.gstack[-1].append(d)
        elif d.strip(): self.stray.append((self.art, d.strip()))
p = P(); p.feed(page)

problems = 0
print(f"articles found: {len(p.groups)}")
for num in sorted(expected):
    arts = {k: v for k, v in p.groups.items() if k.startswith(f"p{num}-")}
    onart = [s for v in arts.values() for s in v]
    # on-art -> copy.md (exact line match)
    for s in onart:
        if s not in all_copy_lines:
            problems += 1; print(f"  [NOT IN COPY] post {num}: {s!r}")
    # copy.md -> on-art (every expected string placed at least once in this post)
    for s in expected[num]:
        if s not in onart:
            problems += 1; print(f"  [MISSING ON ART] post {num}: {s!r}")
    # extra occurrences beyond the copy (repeats)
    extra = [s for s in set(onart) if onart.count(s) > expected[num].count(s)]
    for s in extra:
        problems += 1; print(f"  [REPEATED ON ART] post {num}: {s!r} x{onart.count(s)} (copy has it x{expected[num].count(s)})")
    print(f"post {num}: {len(arts)} canvas(es), {len(onart)} on-art strings, {len(expected[num])} copy strings")
for a, d in p.stray:
    problems += 1; print(f"  [STRAY TEXT] {a}: {d!r}")
print("\ncarousel HEADLINE reference fields:")
for num, h in sorted(ref_headline.items()):
    onart = [s for k, v in p.groups.items() if k.startswith(f"p{num}-") for s in v]
    print(f"  {num}: {'on art' if h in onart else 'NOT on art'} : {h!r}")

# ---- dashes ----
for name, txt in (("copy.md", copy), ("page", page)):
    print(f"{name}: em dash {txt.count(chr(0x2014))}, en dash {txt.count(chr(0x2013))}")
for m in re.finditer("[\u2013\u2014]", page):
    print("  dash at", m.start(), repr(page[max(0, m.start()-40):m.start()+40]))

# ---- text-transform on copy classes ----
css = page.split("<style>", 1)[1].split("</style>", 1)[0]
copy_cls = ["kp-headline", "kp-text", "kp-sub", "kp-option", "kp-cta", "kp-flow-label", "kp-prompt-line", "q4-question", "kp-join", "kp-li", "kp-opt", "kp-tile"]
for rule in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
    sel, body = rule
    if "text-transform" in body and any(re.search(rf"\.{c}\b", sel) for c in copy_cls):
        problems += 1; print("  [TEXT-TRANSFORM ON COPY]", sel.strip())

# ---- Bounce line graphics: none may remain (static scan of the page and both DS copies) ----
DS = [S / "katapult-ds-src.html", S / "katapult-ds" / "index.html"]
BOUNCE_ID = re.compile(r'k-(?:support|super|seam-(?:in|out|start|end)|arrow)\b')
BOUNCE_CLS = re.compile(r'class="[^"]*\bkp-(?:bounce|super|seam|swipe|flow)\b')
print("\nBounce scan:")
for name, txt in [("page", page)] + [(str(f.relative_to(S)), f.read_text(encoding="utf-8")) for f in DS]:
    body = "\n".join(l for l in txt.split("\n") if not l.startswith("@font-face"))
    n_ids = len(BOUNCE_ID.findall(body))
    cls = BOUNCE_CLS.findall(body) if name == "page" else [c for c in BOUNCE_CLS.findall(body) if "kp-flow" not in c]
    arts = re.findall(r'<article class="kp-post.*?</article>', body, re.S)
    curves = dash = 0
    for a in arts:
        for d in re.findall(r'<path[^>]*\sd="([^"]*)"', a):
            if re.search(r"[CcSsQqTtAa]", d): curves += 1
        dash += len(re.findall(r'stroke-dasharray', a))
    bad = n_ids + len(cls) + curves + dash
    problems += bad
    print(f"  {name}: {len(arts)} articles | Bounce symbol ids/hrefs {n_ids} | Bounce classes {len(cls)} | curved svg paths in posts {curves} | dotted strokes in posts {dash} -> {'OK' if not bad else 'FAIL'}")
print("\nproblems:", problems)
