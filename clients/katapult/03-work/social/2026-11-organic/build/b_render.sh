#!/bin/sh
# Builder B: build + render posts to $1 (default: deliverables png folder)
cd "$(dirname "$0")/.."
OUT=${1:-C:/Users/lucas/OneDrive/Desktop/VAZIO/power-digital-ops/clients/katapult/04-deliverables/social/2026-11-organic/png}
python build/b_build.py
for p in 03-holiday-wishlist 06-customer-testimonial 09-q-and-a 10-discover-where-you-can-shop 12-thanksgiving 13-black-friday 14-more-ways-to-shop; do
  python build/render.py build/frames/$p "$OUT/$p" >/dev/null
done
echo rendered to $OUT
