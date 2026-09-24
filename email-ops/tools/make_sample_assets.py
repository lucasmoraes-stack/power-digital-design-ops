#!/usr/bin/env python3
"""
make_sample_assets.py · gera os assets de AMOSTRA do template de kit de e-mail.

Requer Pillow (pip install pillow). Não faz parte do fluxo de uma marca: serve só
para recriar os placeholders neutros de _studio/email-ops/templates/email-kit/assets/,
que existem para o template renderizar. Cada placeholder leva um rótulo em
monospace com o tamanho de exibição, para ninguém confundir com fotografia real.

  python make_sample_assets.py            # escreve em ../templates/email-kit/assets/
  python make_sample_assets.py <pasta>    # escreve em outra pasta
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "templates" / "email-kit" / "assets"

INK = (31, 42, 51)          # sample dark
GREY = (211, 217, 222)      # sample photo fallback
STRIPE = (199, 206, 212)
LABEL_BG = (255, 255, 255)

SANS_BOLD = ["C:/Windows/Fonts/arialbd.ttf", "/Library/Fonts/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
MONO = ["C:/Windows/Fonts/consola.ttf", "/Library/Fonts/Menlo.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]


def font(candidates, size):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def stripes(img, color, step=56, width=22):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for x in range(-h, w, step):
        draw.line([(x, h), (x + h, 0)], fill=color, width=width)


def label(img, text, size=28, pos="center"):
    draw = ImageDraw.Draw(img)
    f = font(MONO, size)
    box = draw.textbbox((0, 0), text, font=f)
    tw, th = box[2] - box[0], box[3] - box[1]
    pad_x, pad_y = size, size // 2
    w, h = img.size
    x = (w - tw) // 2
    y = (h - th) // 2 if pos == "center" else int(h * 0.72) - th // 2
    draw.rectangle([x - pad_x, y - pad_y, x + tw + pad_x, y + th + pad_y + 4], fill=LABEL_BG)
    draw.text((x - box[0], y - box[1]), text, font=f, fill=INK)


def placeholder(name, size, text, label_size=28, pos="center"):
    img = Image.new("RGB", size, GREY)
    stripes(img, STRIPE)
    label(img, text, label_size, pos)
    img.save(OUT / name, "JPEG", quality=68, optimize=True)


def gradient(name, size, inner, outer, center=(0.5, 1.0)):
    grad = Image.radial_gradient("L").resize((size[0] * 2, size[1] * 2))
    cx, cy = int(size[0] * center[0]), int(size[1] * center[1])
    grad = grad.crop((size[0] - cx, size[1] - cy, size[0] - cx + size[0], size[1] - cy + size[1]))
    img = Image.composite(Image.new("RGB", size, outer), Image.new("RGB", size, inner), grad)
    img.save(OUT / name, "JPEG", quality=75, optimize=True)


def logo(name, color):
    img = Image.new("RGBA", (400, 167), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    f = font(SANS_BOLD, 96)
    box = draw.textbbox((0, 0), "BRAND", font=f)
    tw, th = box[2] - box[0], box[3] - box[1]
    draw.text(((400 - tw) // 2 - box[0], (167 - th) // 2 - box[1]), "BRAND", font=f, fill=color)
    img.save(OUT / name, "PNG", optimize=True)


def product(name):
    img = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([110, 60, 290, 340], radius=36, fill=GREY + (255,))
    draw.rounded_rectangle([150, 30, 250, 80], radius=12, fill=STRIPE + (255,))
    f = font(MONO, 22)
    text = "PRODUCT 180x180"
    box = draw.textbbox((0, 0), text, font=f)
    tw = box[2] - box[0]
    draw.rectangle([(400 - tw) // 2 - 12, 188, (400 + tw) // 2 + 12, 222], fill=LABEL_BG + (255,))
    draw.text(((400 - tw) // 2 - box[0], 194 - box[1]), text, font=f, fill=INK)
    img.save(OUT / name, "PNG", optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    logo("logo-light.png", INK + (255,))
    logo("logo-dark.png", (255, 255, 255, 255))
    placeholder("sample-hero.jpg", (1200, 760), "HERO 600x380")
    placeholder("sample-card.jpg", (1120, 1200), "HERO CARD 560x600 · calm top area", pos="low")
    placeholder("sample-feature.jpg", (1200, 700), "FEATURE 600x350")
    for i in (1, 2, 3):
        placeholder(f"portrait-{i}.jpg", (240, 240), f"PORTRAIT {i}", label_size=18)
    product("product-1.png")
    gradient("texture-light.jpg", (1200, 880), inner=(214, 224, 231), outer=(240, 242, 244))
    gradient("texture-dark.jpg", (1200, 800), inner=(58, 76, 90), outer=(31, 42, 51), center=(0.5, 0.5))
    for path in sorted(OUT.iterdir()):
        if path.suffix in (".png", ".jpg"):
            print(f"{path.name:22} {path.stat().st_size / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
