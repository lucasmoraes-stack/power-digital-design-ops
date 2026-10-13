"""RKU26013 frame builder: background (compose.py) + on-screen ad copy + headline + logo.

    python -I build.py            -> build/<ind>-1440x1440.html and export/<file>.png
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "01-brand"))
sys.path.insert(0, str(HERE))
from rk_common import ID, font_face, img_data, lockup  # noqa: E402

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

IND = {
    "pet": {"code": "Pet", "word": "pet brand",
            "screen": ("More tail wags.<br>Better days.", "Premium nutrition<br>for happy, healthy dogs.", "Shop now")},
}


def marks():
    wm = re.findall(r'<path d="[^"]+"[^>]*/>', (ID / "roku-wordmark.svg").read_text(encoding="utf8"))
    am = re.findall(r'<path d="[^"]+"[^>]*/>', (ID / "roku-ads-manager.svg").read_text(encoding="utf8"))[1]
    am = re.sub(r'fill="[^"]+"', 'fill="currentColor"', am).replace(' class="am"', '')
    roku = '<svg class="lk-r" viewBox="0 0 628 196" aria-hidden="true">' + "".join(wm) + "</svg>"
    ads = '<svg class="lk-a" viewBox="181 7 318 50" aria-hidden="true">' + am + "</svg>"
    return f'<div class="lk" role="img" aria-label="Roku Ads Manager">{roku}{ads}</div>'


def frame(key, box):
    d = IND[key]
    x0, y0, x1, y1 = box
    sw = x1 - x0
    h1, sub, cta = d["screen"]
    bg = img_data(HERE / "img" / f"{key}-bg-1440x1440.png", "image/png")
    return f"""<!doctype html><meta charset="utf-8"><title>RKU26013 {key} 1x1</title>
<style>
{font_face()}
html,body{{margin:0;background:#fff}}
.f{{position:relative;width:1440px;height:1440px;overflow:hidden;background:url({bg}) 0 0/1440px 1440px;font-family:"Roku Display",sans-serif}}
.lk{{position:absolute;top:72px;left:50%;transform:translateX(-50%);width:380px;height:auto;display:block}}
.hl{{position:absolute;left:0;right:0;top:150px;margin:0;text-align:center;font-weight:700;font-size:112px;line-height:1.08;letter-spacing:-.018em;color:#14082B}}
.hl b{{font-weight:700;color:#4F01A3}}
.scr{{position:absolute;left:{x0}px;top:{y0}px;width:{sw}px;height:{y1 - y0}px}}
.scr .t{{position:absolute;left:{round(sw * .065)}px;top:{round((y1 - y0) * .2)}px;display:flex;flex-direction:column;gap:{round(sw * .022)}px;color:#fff}}
.scr h2{{margin:0;font-weight:700;font-size:{round(sw * .062)}px;line-height:1.08;letter-spacing:-.01em}}
.scr p{{margin:0;font-weight:400;font-size:{round(sw * .03)}px;line-height:1.3;color:#E9DEFF}}
.scr .b{{align-self:flex-start;margin-top:{round(sw * .012)}px;background:#fff;color:#4F01A3;font-weight:700;font-size:{round(sw * .026)}px;padding:{round(sw * .013)}px {round(sw * .028)}px;border-radius:999px}}
.scr .ad{{position:absolute;right:{round(sw * .03)}px;top:{round(sw * .025)}px;font-size:{round(sw * .019)}px;font-weight:500;color:#fff;background:rgba(0,0,0,.35);padding:4px 10px;border-radius:6px}}
</style>
<div class="f">
  {lockup("lk", "#4F01A3", "#646464")}
  <h1 class="hl">Put your <b>{d["word"]}</b><br>in their living room.</h1>
  <div class="scr"><span class="ad">Ad · 0:15</span><div class="t"><h2>{h1}</h2><p>{sub}</p><span class="b">{cta}</span></div></div>
</div>"""


def export(html, png, w, h):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={w},{h}", f"--screenshot={png}", html.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    from compose import compose
    (HERE / "build").mkdir(exist_ok=True)
    (HERE / "export").mkdir(exist_ok=True)
    for key in (sys.argv[1:] or IND):
        _, box, _win = compose(key)
        html = HERE / "build" / f"{key}-1440x1440.html"
        html.write_text(frame(key, box), encoding="utf8")
        png = HERE / "export" / f"RKU26013-SellItOnRoku-1440x1440-Static-Meta-{IND[key]['code']}-V1.png"
        export(html, png, 1440, 1440)
        print(png.name)
