"""Power Digital Hub builder.

  python hub/build_hub.py                      build hub/power-digital-hub.html from artifacts.json + thumbs/
  python hub/build_hub.py thumb <slug> <html>  screenshot a saved artifact HTML into thumbs/<slug>.jpg

The HTML for `thumb` is the file the Artifact tool saves on `read` (the live published version).
"""
import base64
import html
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REG = HERE / "artifacts.json"
THUMBS = HERE / "thumbs"
OUT = HERE / "power-digital-hub.html"
CHROME = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
TYPE_ORDER = ["deliverables", "design-system", "library", "studio", "board"]
TYPE_CODE = {"design-system": "DS", "deliverables": "HUB", "library": "LIB", "studio": "STU", "board": "BRD"}


def thumb(slug, src):
    from PIL import Image

    chrome = next((c for c in CHROME if Path(c).exists()), None)
    if not chrome:
        sys.exit("Chrome/Edge not found")
    text = Path(src).read_text(encoding="utf-8", errors="replace")
    # Force the light palette so every thumbnail matches, whatever the OS theme.
    text = text.replace("<html>", '<html data-theme="light">', 1)
    tmp = Path(tempfile.mkdtemp())
    page, raw = tmp / "page.html", tmp / "raw.png"
    page.write_text(text, encoding="utf-8")
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-color-profile=srgb", "--blink-settings=preferredColorScheme=1",
                    "--virtual-time-budget=8000", "--window-size=1440,900",
                    f"--screenshot={raw}", page.as_uri()], check=True, capture_output=True)
    THUMBS.mkdir(exist_ok=True)
    Image.open(raw).convert("RGB").resize((720, 450), Image.LANCZOS).save(
        THUMBS / f"{slug}.jpg", quality=78, optimize=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"thumbs/{slug}.jpg")


def e(s):
    return html.escape(str(s), quote=True)


def thumb_uri(slug):
    p = THUMBS / f"{slug}.jpg"
    if not p.exists():
        return ""
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()


def fmt_date(d):
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    y, m, dd = d.split("-")
    return f"{int(dd)} {months[int(m) - 1]}"


def card(a, types, statuses):
    uri = thumb_uri(a["slug"])
    img = (f'<img src="{uri}" alt="Top of {e(a["title"])}" loading="lazy">' if uri
           else '<span class="nothumb">No thumbnail yet</span>')
    tags = "".join(f"<li>{e(s)}</li>" for s in a.get("sections", [])[:8])
    search = " ".join([a["title"], a["description"], " ".join(a.get("sections", [])),
                       types[a["type"]]["label"]]).lower()
    return f'''
<article class="card" data-type="{a["type"]}" data-status="{a["status"]}" data-search="{e(search)}">
  <a class="shot" href="{e(a["url"])}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">{img}</a>
  <div class="body">
    <div class="meta">
      <span class="code t-{a["type"]}">{TYPE_CODE[a["type"]]}</span>
      <span class="tlabel">{e(types[a["type"]]["label"])}</span>
      <span class="status s-{a["status"]}">{e(statuses[a["status"]])}</span>
    </div>
    <h3><a href="{e(a["url"])}" target="_blank" rel="noopener">{e(a["title"])}</a></h3>
    <p>{e(a["description"])}</p>
    <ul class="tags">{tags}</ul>
    <div class="foot">
      <span class="counts">{e(a.get("counts", ""))}</span>
      <span class="date">Updated {fmt_date(a["updated"])}</span>
    </div>
    <div class="actions">
      <a class="open" href="{e(a["url"])}" target="_blank" rel="noopener">Open<span aria-hidden="true"> ↗</span></a>
      <button type="button" class="copy" data-url="{e(a["url"])}">Copy link</button>
    </div>
  </div>
</article>'''


def map_chip(a, c, statuses):
    # In the map the client is already the row, so drop its name from the title.
    short = a["title"].replace(c["name"], "").strip(" ·") or a["title"]
    flag = "" if a["status"] == "live" else f' <em>{e(statuses[a["status"]])}</em>'
    return (f'<a class="chip s-{a["status"]}" href="{e(a["url"])}" target="_blank" '
            f'rel="noopener">{e(short)}{flag}</a>')


def build():
    reg = json.loads(REG.read_text(encoding="utf-8"))
    types, statuses = reg["types"], reg["statuses"]
    clients, arts = reg["clients"], reg["artifacts"]
    rank = {t: i for i, t in enumerate(TYPE_ORDER)}

    def order(a):
        return (a["status"] == "superseded", rank[a["type"]], a["title"])

    # Map: one row per client, one column per type.
    map_rows = []
    for c in clients:
        cells = []
        for t in TYPE_ORDER:
            items = [a for a in arts if a["client"] == c["id"] and a["type"] == t]
            if items:
                links = "".join(map_chip(a, c, statuses) for a in sorted(items, key=order))
            else:
                links = '<span class="gap">Not created yet</span>'
            cells.append(f'<td data-label="{e(types[t]["label"])}">{links}</td>')
        sw = "".join(f'<i style="background:{x}"></i>' for x in c["colors"][:4])
        map_rows.append(
            f'<tr><th scope="row"><a href="#c-{c["id"]}"><span class="sw">{sw}</span>{e(c["name"])}</a></th>{"".join(cells)}</tr>')

    steps = "".join(
        f'''<li><span class="code t-{t}">{TYPE_CODE[t]}</span><h3>{e(types[t]["label"])}</h3>
<p>{e(types[t]["what"])}</p><p class="when">{e(types[t]["when"])}</p></li>'''
        for t in ["design-system", "library", "studio", "board", "deliverables"])

    sections = []
    for c in clients:
        items = sorted([a for a in arts if a["client"] == c["id"]], key=order)
        swatches = "".join(
            f'<li><i style="background:{x}"></i><code>{x}</code></li>' for x in c["colors"])
        chans = " · ".join(e(x) for x in c["channels"])
        sections.append(f'''
<section class="client" id="c-{c["id"]}" style="--brand:{c["colors"][0]}">
  <header class="chead">
    <div class="band" aria-hidden="true">{"".join(f'<i style="background:{x}"></i>' for x in c["colors"])}</div>
    <div class="ctitle">
      <h2>{e(c["name"])}</h2>
      <p class="csub">{e(c["sub"])} <span>·</span> {chans}</p>
    </div>
    <div class="cinfo">
      <p>{e(c["note"])}</p>
      <p class="repo">Repo <code>{e(c["repo"])}</code> <span>·</span> {len(items)} artifact{"s" if len(items) != 1 else ""}</p>
    </div>
    <ul class="swatches" aria-label="{e(c["name"])} brand colors">{swatches}</ul>
  </header>
  <div class="grid">{"".join(card(a, types, statuses) for a in items)}</div>
  <p class="empty" hidden>No {e(c["name"])} artifacts match this filter.</p>
</section>''')

    cname = {c["id"]: c["name"] for c in clients}
    legacy = "".join(
        f'<li><span class="lc">{e(cname.get(l["client"], ""))}</span><a href="{e(l["url"])}" target="_blank" rel="noopener">{e(l["title"])}</a><span class="ln">{e(l["note"])}</span></li>'
        for l in reg.get("legacy", []))

    n_live = sum(a["status"] == "live" for a in arts)
    n_rev = sum(a["status"] in ("in-review", "draft") for a in arts)
    page = TEMPLATE
    for k, v in {
        "{{TITLE}}": e(reg["hub"]["title"]),
        "{{UPDATED}}": fmt_date(reg["hub"]["updated"]) + " " + reg["hub"]["updated"][:4],
        "{{N_CLIENTS}}": str(len(clients)),
        "{{N_ARTS}}": str(len(arts)),
        "{{N_LIVE}}": str(n_live),
        "{{N_REV}}": str(n_rev),
        "{{STEPS}}": steps,
        "{{MAP}}": "".join(map_rows),
        "{{MAP_HEAD}}": "".join(f'<th scope="col">{e(types[t]["label"])}</th>' for t in TYPE_ORDER),
        "{{JUMP}}": "".join(f'<a href="#c-{c["id"]}"><i style="background:{c["colors"][0]}"></i>{e(c["name"])}</a>' for c in clients),
        "{{SECTIONS}}": "".join(sections),
        "{{LEGACY}}": legacy,
    }.items():
        page = page.replace(k, v)
    OUT.write_text(page, encoding="utf-8")
    print(f"{OUT.name}: {len(arts)} artifacts, {OUT.stat().st_size // 1024} KB")


TEMPLATE = (HERE / "template.html").read_text(encoding="utf-8") if (HERE / "template.html").exists() else ""

if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "thumb":
        thumb(sys.argv[2], sys.argv[3])
    else:
        build()
