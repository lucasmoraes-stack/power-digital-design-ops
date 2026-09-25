"""Fetch the exact product variants linked in the October 2026 Broadcast Copy (client PDF,
00-inbox/2026-10-broadcast-copy.pdf) from habitoutdoors.com.

Writes products.json next to this file. For each product, downloads the variant packshot to
01-brand/photos/products/<handle>--<variant>.png and every store image to
01-brand/photos/products/<handle>/NN.<ext> (model shots, detail crops). Outside git.
Links without a variant id in the copy (Heavy Weight Hoodie Gunmetal / Loden Green) are
resolved by colour name and flagged "resolved_by_color". Rerun before send.
"""
import json
import os
import urllib.request

STORE = "https://www.habitoutdoors.com"
HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "01-brand", "photos", "products"))
UA = {"User-Agent": "Mozilla/5.0 (email-ops)"}

# (email, band, handle, variant id or colour name) exactly as linked in the copy doc
LINKS = [
    ("01", "grid", "ahabit-sup-sup-mens-insulated-bib", 49451798790426),
    ("01", "grid", "habit-mens-cedar-branch-insulated-waterproof-parka", 49451818385690),
    ("02", "grid", "youth-cedar-branch-insulated-bib", 52632814518554),
    ("02", "grid", "habit-youth-summit-park-performance-hoodie", 51341422592282),
    ("02", "grid", "youth-bear-cave-6-pocket-camo-pant", 39568503668787),
    ("03", "colors", "mens-heavy-weight-full-zip-hoodie", 45636943249690),
    ("03", "colors", "mens-heavy-weight-full-zip-hoodie", "Gunmetal"),
    ("03", "colors", "mens-heavy-weight-full-zip-hoodie", "Loden Green"),
    ("04", "rows", "mens-crater-valley-performance-hoodie", 52423312867610),
    ("04", "rows", "mens-crater-valley-full-zip-fleece-jacket", 52630367076634),
    ("04", "rows", "mens-crater-valley-sweater-fleece-zip-jacket", 52630359834906),
    ("05", "grid", "men-s-mid-layer-jacket", 45471499518234),
    ("05", "grid", "men-s-windproof-fleece-pant", 45471564824858),
    ("05", "grid", "men-s-windproof-fleece-jacket", 45471553618202),
]


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def save(url, path):
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(get(url + ("&" if "?" in url else "?") + "width=1200"))


def main():
    os.makedirs(PHOTOS, exist_ok=True)
    out = []
    for email, band, handle, key in LINKS:
        row = {"email": email, "band": band, "handle": handle}
        try:
            p = json.loads(get(f"{STORE}/products/{handle}.json"))["product"]
        except Exception as e:
            row["error"] = f"product not found: {e}"
            out.append(row)
            print(f"[{email}] {handle}: NOT FOUND")
            continue
        if isinstance(key, int):
            v = next((x for x in p["variants"] if x["id"] == key), None)
            if v is None:
                row["error"] = "variant id not on the product anymore; first variant used"
                v = p["variants"][0]
        else:
            v = next((x for x in p["variants"] if key.lower() in (x.get("title") or "").lower()), None)
            row["resolved_by_color"] = key
            if v is None:
                row["error"] = f"no variant with colour {key}; first variant used"
                v = p["variants"][0]
        vid = v["id"]
        row.update({"variant_id": vid, "url": f"{STORE}/products/{handle}?variant={vid}",
                    "title": p["title"], "product_type": p.get("product_type", ""),
                    "variant_title": v.get("title"), "price": v.get("price"),
                    "compare_at_price": v.get("compare_at_price"),
                    "available": v.get("available")})
        img = None
        if v.get("image_id"):
            img = next((i["src"] for i in p["images"] if i["id"] == v["image_id"]), None)
        img = img or (p["images"][0]["src"] if p["images"] else None)
        row["image_src"] = img
        if img:
            ext = os.path.splitext(img.split("?")[0])[1].lower() or ".png"
            fname = f"{handle}--{vid}{ext}"
            save(img, os.path.join(PHOTOS, fname))
            row["image_file"] = f"clients/habit-outdoors/01-brand/photos/products/{fname}"
        folder = os.path.join(PHOTOS, handle)
        os.makedirs(folder, exist_ok=True)
        allimgs = []
        for n, i in enumerate(p["images"], 1):
            ext = os.path.splitext(i["src"].split("?")[0])[1].lower() or ".png"
            fn = f"{n:02d}{ext}"
            try:
                save(i["src"], os.path.join(folder, fn))
            except Exception as e:
                print("   image fail", fn, e)
                continue
            vids = i.get("variant_ids") or []
            allimgs.append({"file": f"clients/habit-outdoors/01-brand/photos/products/{handle}/{fn}",
                            "src_name": os.path.basename(i["src"].split("?")[0]),
                            "alt": i.get("alt"), "for_this_variant": vid in vids})
        row["all_images"] = allimgs
        row["options"] = [o.get("name") for o in p.get("options", [])]
        row["body_text"] = (p.get("body_html") or "")[:1500]
        out.append(row)
        flag = f"  !! {row['error']}" if "error" in row else ""
        print(f"[{email}] {p['title']} | {row['variant_title']} | ${row['price']}"
              + (f" (compare ${row['compare_at_price']})" if row.get('compare_at_price') else "")
              + f" | {len(allimgs)} imgs" + flag)
    with open(os.path.join(HERE, "products.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
