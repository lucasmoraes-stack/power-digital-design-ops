"""Trim and downsize the packshots used in the November emails into ./assets/ (2x of the largest use).

Usage: python prep_assets.py
Transparent packshots are trimmed on alpha; packshots on white are trimmed on non-white pixels and keep their white
ground (the emails place them with mix-blend-mode: multiply on light cards).
"""
import os
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..', '01-brand')
SRC = os.path.join(ROOT, 'email-kit', 'assets', 'source')
LAB = os.path.join(ROOT, 'photos', 'figma-lab')
OUT = os.path.join(HERE, 'assets')

PACKSHOTS = {
    # deodorants: exact files from the LAB scent grid (407:3817)
    'deo-mountain-spring': f'{SRC}/figma-lab-407-3817/deo-mountain-spring.png',
    'deo-north-woods': f'{SRC}/figma-lab-407-3817/deo-north-woods.png',
    'deo-moonlit-meadow': f'{SRC}/figma-lab-407-3817/deo-moonlit-meadow.png',
    'deo-twilight-breeze': f'{SRC}/figma-lab-407-3817/deo-twilight-breeze.png',
    'deo-tropical-island': f'{SRC}/figma-lab-407-3817/deo-tropical-island.png',
    'deo-unscented': f'{SRC}/figma-lab-407-3817/deo-unscented.png',
    'tp-whiten-deep-clean-peppermint': f'{LAB}/packshot-whiten-plus-deep-clean-peppermint-carton.png',
    'tp-whiten-coconut': f'{SRC}/packshot-whiten-plus-coconut-oil-gentle-mint-toothpaste-box.png',
    'mw-whole-care-fresh-mint': f'{LAB}/packshot-fresh-mint-whole-care-mouthwash-b.png',
    'mw-sea-salt': f'{SRC}/packshot-sea-salt-mouthwash.png',
    'soap-lavender-shea': f'{LAB}/packshot-lavender-shea-bar-soap.png',
    'soap-lemon-bergamot': f'{SRC}/packshot-lemon-bergamot-bar-soap.png',
    # bundles (on white)
    'bundle-most-loved-deodorant': f'{LAB}/packshot-most-loved-deodorant-bundle.png',
    'bundle-back-to-nature': f'{LAB}/packshot-back-to-nature-bundle-white-bg.png',
    'bundle-sensitive-skin-smile': f'{LAB}/packshot-sensitive-skin-smile-bundle-white-bg.png',
    'bundle-best-sellers-bar-trio': f'{LAB}/packshot-best-sellers-bar-trio-white-bg.png',
}
MAX = 760  # px on the long side


def trim(im):
    if im.mode == 'RGBA' and im.getchannel('A').getextrema()[0] < 250:
        bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
        return im.crop(bb), False
    rgb = im.convert('RGB')
    diff = ImageChops.difference(rgb, Image.new('RGB', rgb.size, (255, 255, 255))).convert('L').point(lambda v: 255 if v > 12 else 0)
    bb = diff.getbbox()
    pad = 6
    bb = (max(bb[0] - pad, 0), max(bb[1] - pad, 0), min(bb[2] + pad, rgb.width), min(bb[3] + pad, rgb.height))
    return rgb.crop(bb), True


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, path in PACKSHOTS.items():
        im, white = trim(Image.open(path))
        s = min(1, MAX / max(im.size))
        if s < 1: im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        ext = 'jpg' if white else 'png'
        p = os.path.join(OUT, f'{name}.{ext}')
        im.save(p, quality=90) if white else im.save(p, optimize=True)
        print(f'{name}.{ext}', im.size, 'on white' if white else 'transparent')


if __name__ == '__main__':
    main()
