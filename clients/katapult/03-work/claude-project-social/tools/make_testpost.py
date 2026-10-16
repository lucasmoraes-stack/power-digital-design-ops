"""Write studio/_all-<group>.html: one frame per layout, default copy, real photos and products. For tools/autotest.py."""
import json
from pathlib import Path

ST = Path(__file__).resolve().parents[1] / "studio"
cat = json.loads((ST / "catalog.json").read_text(encoding="utf-8"))
photos = ["phone-woman-card-phone-05", "unboxing-woman-unboxing-sofa-02", "together-couple-sofa-phone-laptop-01", "laptop-woman-sofa-laptop-01"]
prods = ["fridge", "washer", "tv"]
files = {}
for i, (code, L) in enumerate(cat["layouts"].items()):
    key = "T" + str((int(L["family"][1:]) - 1) // 3) if L["group"] == "template" else L["family"]
    out = files.setdefault(key, [])
    out.append(f'<section data-use="{code}" data-file="{code}">')
    pi = 0
    for n, s in L["slots"].items():
        if s["kind"] == "image":
            if n == "phone":
                continue
            ref = f"library:{photos[i % 4]}" if n == "photo" else f"product:{prods[pi % 3]}"
            pi += n != "photo"
            out.append(f'<div data-slot="{n}" data-img="{ref}"></div>')
        else:
            out.append(f'<div data-slot="{n}">{s["default"]}</div>')
    out.append("</section>")
for k, out in files.items():
    (ST / f"_all-{k}.html").write_text("<!DOCTYPE html><html><body>" + "\n".join(out) + "</body></html>", encoding="utf-8")
print(len(cat["layouts"]), "frames in", len(files), "files:", ", ".join(files))
