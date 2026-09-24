"""Fetch the exact product variants linked in the 2026 Broadcast Copy (client doc) from habitoutdoors.com.

Writes products.json next to this file and downloads each variant's packshot into
clients/habit-outdoors/01-brand/photos/products/<handle>--<variant>.png (outside git).
Rerun before send: prices and availability change.
"""
import json
import os
import urllib.request

STORE = "https://www.habitoutdoors.com"
HERE = os.path.dirname(os.path.abspath(__file__))
PHOTOS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "01-brand", "photos", "products"))
UA = {"User-Agent": "Mozilla/5.0 (email-ops)"}

# (email, band, handle, variant id) exactly as linked in the copy doc
LINKS = [
    ("01", "checklist", "mlf-1-4-zip-camo-performance-layer", 47952634413338),
    ("01", "checklist", "mens-flushing-bay-short-sleeve-river-shirt", 49918052925722),
    ("01", "checklist", "men-s-roaring-springs-packable-rain-jacket", 39299390472243),
    ("02", "rotation", "habit-mens-wj657-cedar-branch-insulated-waterproof-bomber", 51265344733466),
    ("02", "rotation", "mens-performance-fleece-hoodie", 45600303677722),
    ("02", "rotation", "men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt", 32728036802611),
    ("03", "quiet", "knit-camo-stocking-cap", 39479198580787),
    ("03", "quiet", "youth-bear-cave-long-sleeve-camo-tee", 51763673661722),
    ("03", "quiet", "all-purpose-camo-leather-gloves", 47156168098074),
    ("04", "shoreline", "copy-of-mens-all-weather-boot", 39916249776179),
    ("04", "shoreline", "habit-mens-roaring-springs-packable-rain-pant-1", 31820086575155),
    ("04", "shoreline", "habit-mens-roaring-springs-packable-rain-pant", 31746549415987),
    ("04", "open-water", "mlf-hooded-performance-layer-with-gaiter", 40557557448755),
    ("04", "open-water", "copy-of-mens-all-weather-boot", 39916249776179),
    ("04", "open-water", "men-s-roaring-springs-packable-rain-pant", 39299401875507),
]


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def main():
    os.makedirs(PHOTOS, exist_ok=True)
    out = []
    for email, band, handle, vid in LINKS:
        row = {"email": email, "band": band, "handle": handle, "variant_id": vid,
               "url": f"{STORE}/products/{handle}?variant={vid}"}
        try:
            p = json.loads(get(f"{STORE}/products/{handle}.json"))["product"]
        except Exception as e:
            row["error"] = f"product not found: {e}"
            out.append(row)
            print(f"[{email}] {handle}: NOT FOUND")
            continue
        v = next((x for x in p["variants"] if x["id"] == vid), None)
        row["title"] = p["title"]
        row["product_type"] = p.get("product_type", "")
        if v is None:
            row["error"] = "variant id not on the product anymore; first variant used"
            v = p["variants"][0]
        row["variant_title"] = v.get("title")
        row["price"] = v.get("price")
        row["compare_at_price"] = v.get("compare_at_price")
        img = None
        if v.get("image_id"):
            img = next((i["src"] for i in p["images"] if i["id"] == v["image_id"]), None)
        img = img or (p["images"][0]["src"] if p["images"] else None)
        row["image_src"] = img
        if img:
            ext = os.path.splitext(img.split("?")[0])[1].lower() or ".png"
            fname = f"{handle}--{vid}{ext}"
            path = os.path.join(PHOTOS, fname)
            if not os.path.exists(path):
                with open(path, "wb") as f:
                    f.write(get(img + ("&" if "?" in img else "?") + "width=1200"))
            row["image_file"] = f"clients/habit-outdoors/01-brand/photos/products/{fname}"
        out.append(row)
        flag = f"  !! {row['error']}" if "error" in row else ""
        print(f"[{email}] {p['title']} | {row['variant_title']} | ${row['price']}"
              + (f" (was ${row['compare_at_price']})" if row.get('compare_at_price') else "") + flag)
    with open(os.path.join(HERE, "products.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
