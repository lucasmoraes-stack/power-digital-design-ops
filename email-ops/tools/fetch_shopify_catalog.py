"""fetch_shopify_catalog.py - baixa o catalogo publico de uma loja Shopify.

Uso:
  python tools/fetch_shopify_catalog.py https://www.loja.com <pasta>              # so o catalogo (catalog.json)
  python tools/fetch_shopify_catalog.py https://www.loja.com <pasta> --images     # + 1a imagem de cada produto
  python tools/fetch_shopify_catalog.py https://www.loja.com <pasta> --images --match "cedar branch" --all-images

- Le /products.json (endpoint publico do Shopify), pagina ate acabar.
- Escreve <pasta>/catalog.json: titulo, handle, tipo, preco da 1a variante, URL do produto, URLs das imagens.
- Com --images, baixa em <pasta>/<handle>.png (ou <handle>-2.png... com --all-images), largura --width (padrao 1200).
  Nao baixa de novo o que ja existe. --match filtra por texto no titulo (varios --match = OU).
- Preco e nome saem da loja no dia: reconfirmar na data de envio do e-mail.
So biblioteca padrao.
"""
import argparse
import json
import os
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (email-ops catalog fetch)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def fetch_products(store):
    products, page = [], 1
    while True:
        data = json.loads(get(f"{store}/products.json?limit=250&page={page}"))
        batch = data.get("products", [])
        if not batch:
            return products
        products += batch
        page += 1


def main():
    ap = argparse.ArgumentParser(description="Baixa o catalogo publico de uma loja Shopify.")
    ap.add_argument("store", help="URL da loja, ex.: https://www.habitoutdoors.com")
    ap.add_argument("out", help="pasta de destino (ex.: clients/<marca>/01-brand/photos/products)")
    ap.add_argument("--images", action="store_true", help="baixar imagens")
    ap.add_argument("--all-images", action="store_true", help="todas as imagens de cada produto, nao so a 1a")
    ap.add_argument("--match", action="append", default=[], help="filtra por texto no titulo (case-insensitive)")
    ap.add_argument("--width", type=int, default=1200)
    a = ap.parse_args()

    store = a.store.rstrip("/")
    os.makedirs(a.out, exist_ok=True)
    try:
        products = fetch_products(store)
    except Exception as e:
        sys.exit(f"Nao consegui ler {store}/products.json: {e}")

    catalog = []
    for p in products:
        catalog.append({
            "title": p["title"],
            "handle": p["handle"],
            "type": p.get("product_type", ""),
            "price": p["variants"][0]["price"] if p.get("variants") else None,
            "url": f"{store}/products/{p['handle']}",
            "images": [i["src"] for i in p.get("images", [])],
        })
    with open(os.path.join(a.out, "catalog.json"), "w", encoding="utf-8") as f:
        json.dump({"store": store, "count": len(catalog), "products": catalog}, f, ensure_ascii=False, indent=1)
    print(f"catalog.json: {len(catalog)} produtos")

    if not a.images:
        return
    terms = [m.lower() for m in a.match]
    n = 0
    for p in catalog:
        if terms and not any(t in p["title"].lower() for t in terms):
            continue
        srcs = p["images"] if a.all_images else p["images"][:1]
        for k, src in enumerate(srcs, 1):
            ext = os.path.splitext(src.split("?")[0])[1].lower() or ".png"
            name = p["handle"] + ("" if k == 1 else f"-{k}") + ext
            path = os.path.join(a.out, name)
            if os.path.exists(path):
                continue
            sep = "&" if "?" in src else "?"
            try:
                with open(path, "wb") as f:
                    f.write(get(f"{src}{sep}width={a.width}"))
                n += 1
            except Exception as e:
                print(f"falhou {name}: {e}")
    print(f"{n} imagem(ns) baixada(s) em {a.out}")


if __name__ == "__main__":
    main()
