"""Fetch the exact product variants linked in the November 2026 Broadcast Copy (client PDF,
00-inbox/2026-11-broadcast-copy.pdf, transcribed in copy-source.md) from habitoutdoors.com.

Writes products.json next to this file. For each product, downloads the variant packshot to
01-brand/photos/products/<handle>--<variant>.png and every store image to
01-brand/photos/products/<handle>/NN.<ext> (model shots, detail crops). Outside git.
Flannel colours named in the copy without a variant id (Rifle Green / Major Brown) are
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
    ("01", "grid", "womens-cedar-branch-insulated-bib", 52632803705114),
    ("01", "grid", "habit-womens-cedar-branch-insulated-parka", 51265331855642),
    ("01", "grid", "womens-early-dawn-sherpa-shell-jacket", 52697130893594),
    ("02", "grid", "mens-flushing-bay-short-sleeve-river-shirt", 51114509599002),
    ("02", "grid", "mens-flushing-bay-long-sleeve-river-shirt", 51745607516442),
    ("02", "grid", "habit-mens-wj657-cedar-branch-insulated-waterproof-bomber", 51265344733466),
    ("02", "grid", "habit-mens-summit-park-performance-hoodie-1", 52713641804058),
    ("02", "grid", "mens-insulated-boot", 39941172592691),
    ("02", "grid", "knit-camo-stocking-cap", 39479198580787),
    ("02", "giftcard", "gift-card", 16072202977331),
    ("03", "system", "mens-buck-hollow-2-0-jacket", 52600921129242),
    ("03", "system", "mens-buck-hollow-2-0-pant", 52630349775130),
    ("04", "colors", "mens-heavyweight-soft-flannel", 52630375956762),
    ("04", "colors", "mens-heavyweight-soft-flannel", "Rifle Green"),
    ("04", "colors", "mens-heavyweight-soft-flannel", "Major Brown"),
    ("05", "under30", "mens-breaking-dawn-camp-short-sleeve-fishing-shirt", 52257642447130),
    ("05", "under30", "mens-siesta-cape-long-sleeve-performance-tee-1", 40597362475059),
    ("05", "under30", "mens-outdoor-hybrid-hoodie", 47786979295514),
    ("05", "under30", "all-purpose-camo-leather-gloves", 47156168098074),
    ("05", "under100", "mens-3-season-bomber-jacket", 45557982757146),
    ("05", "under100", "mens-heavy-weight-full-zip-hoodie", 45636943249690),
    ("05", "under100", "mens-sherpa-lined-canvas-jacket", 45637255463194),
    ("05", "under100", "men-s-angler-s-bluff-rain-bib", 39898163445811),
    ("05", "under120", "mens-shadow-series-anglers-bluff-rain-bib", 47791648899354),
    ("05", "under120", "mens-shadow-series-anglers-bluff-rain-jacket", 47791547908378),
    ("05", "under120", "men-s-waterproof-insulated-bib", 45471466946842),
    ("05", "giftcard", "gift-card", 16072202977331),
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
