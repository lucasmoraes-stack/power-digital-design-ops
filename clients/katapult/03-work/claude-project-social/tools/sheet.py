import sys
from PIL import Image
from pathlib import Path
names, out, H = sys.argv[2:], sys.argv[1], 420
ims = [Image.open(n).convert("RGB") for n in names]
ims = [i.resize((max(1, round(i.width * H / i.height)), H)) if i.height > 120 else i for i in ims]
rows, row, w = [], [], 0
for i in ims:
    if w + i.width > 2000 and row:
        rows.append(row); row, w = [], 0
    row.append(i); w += i.width + 12
rows.append(row)
W = max(sum(i.width + 12 for i in r) for r in rows); Ht = sum(max(i.height for i in r) + 12 for r in rows)
s = Image.new("RGB", (W, Ht), "#777"); y = 0
for r in rows:
    x = 0
    for i in r: s.paste(i, (x, y)); x += i.width + 12
    y += max(i.height for i in r) + 12
s.save(out)
