"""build_emails.py - Habit Outdoors, November 2026 broadcasts: writes the 5 email HTML files.

Run:  python build_emails.py            (after compose_assets.py)

One component set for the whole batch, so the button, the Product Info Box (E27), the two-voice headline,
the torn edges and the footer (E13 + E14) are identical in the five emails (October QA G1-G3).
Copy: copy-source.md, verbatim (only real uppercase on headline / subheadline / button / item title and
&nbsp; against widows). Prices: products.json (store, 2026-10-07). Links: exactly as in the client's copy;
collection CTAs without a URL in the copy use named placeholders ({{...}}), listed in brief.md.
"""
from __future__ import annotations

import html
from pathlib import Path

HERE = Path(__file__).resolve().parent
K = "../../../01-brand/email-kit/assets/"      # kit assets, relative to the email file
A = "assets/"

ORANGE, TAP, WHITE, BODY_D, MUTED_L = "#FF6400", "#2A2B2D", "#FFFFFF", "#E2DDD9", "#5C5249"
F_SANS = "'Prompt',Arial,Helvetica,sans-serif"
F_BTN = "'Prompt',Helvetica,Arial,sans-serif"
F_SERIF = "'Playfair Display',Georgia,'Times New Roman',serif"

TEX = {  # name: (file, fallback, kind)
    "ivy": (K + "tex-grain-ivy.jpg", "#595442", "tile"),
    "paper": (K + "tex-paper-light.jpg", "#E2DDD9", "tile"),
    "camo": (K + "tex-paper-camo.jpg", "#E2DDD9", "tile"),
    "brown": (K + "tex-grain-brown.jpg", "#483F39", "tile"),
    "halftone": (K + "tex-halftone-brown.jpg", "#483F39", "tile"),
    "tapshoe": (K + "tex-paper-tapshoe.jpg", "#2A2B2D", "tile"),
    "patriot": (K + "tex-grain-patriot-water.jpg", "#202944", "tile"),
    "topo": (K + "tex-topo-tapshoe.jpg", "#2A2B2D", "tile"),
    "patriotflat": (None, "#202944", "flat"),     # round 4: flat Patriot (kit colour), 05 tier UNDER $120
    "tapflat": (None, "#2A2B2D", "flat"),         # round 6: flat Tap Shoe (kit colour), 05 tier UNDER $100
}
LIGHT_TEX = {"paper": "dm-tex", "camo": "dm-tex-camo"}


def esc(t: str) -> str:
    """Escape and make apostrophes typographic (typographic treatment only)."""
    return html.escape(t, quote=False).replace("'", "&rsquo;")


def nb(t: str) -> str:
    """Escaped text with the last space as &nbsp; (no widow)."""
    t = esc(t)
    parts = t.split(" ")
    if len(parts) < 2:
        return t
    return " ".join(parts[:-2]) + (" " if len(parts) > 2 else "") + '<span style="white-space:nowrap;">' + parts[-2] + " " + parts[-1] + "</span>"


def up(t: str) -> str:
    return t.upper()


def price(p: str) -> str:
    return f"${p} USD"


# ---------------------------------------------------------------- head and frame

CSS = """
    :root { color-scheme: light dark; supported-color-schemes: light dark; }
    body { margin: 0 !important; padding: 0 !important; width: 100% !important; background-color: #EFECE9; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
    table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-collapse: collapse; }
    img { -ms-interpolation-mode: bicubic; border: 0; outline: none; text-decoration: none; }
    a[x-apple-data-detectors] { color: inherit !important; text-decoration: none !important; }
    u + #body a { color: inherit; text-decoration: none; }
    .img-dark { display: none; max-height: 0; overflow: hidden; }

    @media screen and (max-width: 620px) {
      .container { width: 100% !important; }
      .px { padding-left: 24px !important; padding-right: 24px !important; }
      .btn-full { width: 100% !important; }
      .btn-full a { display: block !important; padding-left: 12px !important; padding-right: 12px !important; }
      .nav-td { padding: 0 9px !important; }
      .nav-a { font-size: 13px !important; letter-spacing: 1.5px !important; }
      .legal { font-size: 12px !important; letter-spacing: 0.5px !important; }
      .r2-tex { background-size: 100% auto !important; }
      .fluid { width: 100% !important; max-width: 100% !important; height: auto !important; }
      .stack { display: block !important; width: 100% !important; max-width: 100% !important; box-sizing: border-box !important; }
      .desk-only { display: none !important; max-height: 0 !important; overflow: hidden !important; }
      .mob-only { display: block !important; max-height: none !important; overflow: visible !important; }
      .sub { font-size: 14px !important; line-height: 22px !important; letter-spacing: 1.5px !important; }
      .lead { font-size: 22px !important; line-height: 26px !important; }
      .k-xl { font-size: 60px !important; line-height: 58px !important; }
      .k { font-size: 60px !important; line-height: 56px !important; }
      .k-col { font-size: 56px !important; line-height: 54px !important; }
      .bodyp { font-size: 16px !important; line-height: 23px !important; }
      .box { width: 100% !important; }
      .center-m { text-align: center !important; }
      .center-m h1, .center-m h2, .center-m p { text-align: center !important; }
      .center-m table { margin-left: auto !important; margin-right: auto !important; }
      .center-m p { margin-left: auto !important; margin-right: auto !important; }
      .mc { margin: 0 auto !important; }
      .fr-img img.fr-full { width: 100% !important; max-width: 100% !important; height: auto !important; }
      .fr-img img.fr-cen { margin: 0 auto !important; }
      .fr-pad { height: auto !important; padding: 18px 24px 48px 24px !important; }
@@EXTRA@@
    }

    /* Dark mode. Apple Mail / iOS via prefers-color-scheme; Outlook app via [data-ogsc]/[data-ogsb].
       Dark textured bands are fixed; the light paper bands swap texture and text colours; product and
       detail images on light paper are transparent PNG (serve both); torn edges touching light paper
       swap to their -dm twin (img-light / img-dark). */
    @media (prefers-color-scheme: dark) {
      :root:not([data-theme="light"]) .dm-page { background-color: #1E1F21 !important; }
      :root:not([data-theme="light"]) .dm-band { background-color: #34353A !important; }
      :root:not([data-theme="light"]) .dm-h { color: #F1EEEB !important; }
      :root:not([data-theme="light"]) .dm-p { color: #D6D0CA !important; }
      :root:not([data-theme="light"]) .dm-muted { color: #B0A89C !important; }
      :root:not([data-theme="light"]) .img-light { display: none !important; max-height: 0 !important; overflow: hidden !important; }
      :root:not([data-theme="light"]) .img-dark { display: block !important; max-height: none !important; overflow: visible !important; }
      :root:not([data-theme="light"]) .dm-tex { background-color: #34353A !important; background-image: url('@@K@@tex-paper-light-dm.jpg') !important; }
      :root:not([data-theme="light"]) .dm-tex-camo { background-color: #34353A !important; background-image: url('@@K@@tex-paper-camo-dm.jpg') !important; }
    }
    :root[data-theme="dark"] .dm-page { background-color: #1E1F21 !important; }
    :root[data-theme="dark"] .dm-band { background-color: #34353A !important; }
    :root[data-theme="dark"] .dm-h { color: #F1EEEB !important; }
    :root[data-theme="dark"] .dm-p { color: #D6D0CA !important; }
    :root[data-theme="dark"] .dm-muted { color: #B0A89C !important; }
    :root[data-theme="dark"] .img-light { display: none !important; max-height: 0 !important; overflow: hidden !important; }
    :root[data-theme="dark"] .img-dark { display: block !important; max-height: none !important; overflow: visible !important; }
    :root[data-theme="dark"] .dm-tex { background-color: #34353A !important; background-image: url('@@K@@tex-paper-light-dm.jpg') !important; }
    :root[data-theme="dark"] .dm-tex-camo { background-color: #34353A !important; background-image: url('@@K@@tex-paper-camo-dm.jpg') !important; }
    [data-ogsb] .dm-page { background-color: #1E1F21 !important; }
    [data-ogsb] .dm-band { background-color: #34353A !important; }
    [data-ogsb] .dm-tex { background-color: #34353A !important; background-image: url('@@K@@tex-paper-light-dm.jpg') !important; }
    [data-ogsb] .dm-tex-camo { background-color: #34353A !important; background-image: url('@@K@@tex-paper-camo-dm.jpg') !important; }
    [data-ogsc] .dm-h { color: #F1EEEB !important; }
    [data-ogsc] .dm-p { color: #D6D0CA !important; }
    [data-ogsc] .dm-muted { color: #B0A89C !important; }
"""


def page(meta: dict, rows: list[str], extra_css: str = "", post_css: str = "") -> str:
    comment = "\n".join(f"  {k}: {v}" for k, v in meta.items())
    title = esc(meta["Subject"])
    pre = esc(meta["Preheader"])
    return f"""<!DOCTYPE html>
<!--
{comment}
-->
<html lang="en-US" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="format-detection" content="telephone=no, date=no, address=no, email=no, url=no">
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  <title>{title}</title>
  <!--[if mso]>
  <noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
  <style>body, table, td, p, a, h1, h2, h3, span {{ font-family: Arial, sans-serif !important; }} .serif {{ font-family: Georgia, 'Times New Roman', serif !important; }}</style>
  <![endif]-->
  <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;800&family=Playfair+Display:wght@900&display=swap" rel="stylesheet">
  <style>{CSS.replace("@@EXTRA@@", extra_css).replace("@@K@@", K)}{post_css}  </style>
</head>
<body id="body" class="dm-page" style="margin:0; padding:0; background-color:#EFECE9;">

  <div style="display:none; max-height:0; overflow:hidden; mso-hide:all; font-size:1px; line-height:1px; color:#EFECE9;">
    {pre}
    &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" class="dm-page" style="background-color:#EFECE9;">
    <tr>
      <td align="center" style="padding:32px 0 64px 0;">
        <!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
        <table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px; max-width:600px;">
{"".join(rows)}
        </table>
        <!--[if mso]></td></tr></table><![endif]-->
      </td>
    </tr>
  </table>
</body>
</html>
"""


# ---------------------------------------------------------------- components

def band(tex: str, inner: str, module: str, cls: str = "", height: int | None = None) -> str:
    """E25 Textured Band: ONE cell per band (another cell restarts the tile), bgcolor fallback + VML tile."""
    f, fb, kind = TEX[tex]
    dm = LIGHT_TEX.get(tex, "")
    vh = f"height:{height}px;" if height else ""
    if kind == "flat":
        return f"""
          <!-- MODULE:{module} -->
          <tr>
            <td align="center" valign="top" class="{cls}" data-tex="{TEXN[tex]}" bgcolor="{fb}" style="padding:0; background-color:{fb}; vertical-align:top;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{inner}
              </table>
            </td>
          </tr>
          <!-- /MODULE:{module.split(' ')[0]} -->
"""
    return f"""
          <!-- MODULE:{module} -->
          <tr>
            <td align="center" valign="top" class="r2-tex {dm} {cls}" data-tex="{TEXN[tex]}" background="{f}" bgcolor="{fb}" style="mso-padding-alt:0px; padding:0; background-color:{fb}; background-image:url('{f}'); background-size:600px auto; background-repeat:repeat-y; background-position:center top; vertical-align:top;">
              <!--[if gte mso 9]><v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px;{vh}"><v:fill type="tile" src="{f}" color="{fb}" /><v:textbox style="mso-fit-shape-to-text:true;" inset="0,0,0,0"><div><![endif]-->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{inner}
              </table>
              <!--[if gte mso 9]></div></v:textbox></v:rect><![endif]-->
            </td>
          </tr>
          <!-- /MODULE:{module.split(' ')[0]} -->
"""


TEXN = {"ivy": "grain-ivy", "paper": "paper-light", "camo": "paper-camo", "brown": "grain-brown", "halftone": "halftone-brown",
        "tapshoe": "paper-tapshoe", "patriot": "grain-patriot", "topo": "topo-tapshoe", "footer": "flat:#2A2B2D",
        "patriotflat": "flat:#202944", "tapflat": "flat:#2A2B2D"}
FALLBACK = {"ivy": "#595442", "paper": "#E2DDD9", "camo": "#E2DDD9", "brown": "#483F39", "halftone": "#483F39",
            "tapshoe": "#2A2B2D", "patriot": "#202944", "topo": "#2A2B2D", "patriotflat": "#202944",
            "tapflat": "#2A2B2D"}


def edge(top: str, bottom: str, n: str) -> str:
    """E18 torn edge row (textured JPG 1200x80 shown 600x40). The file is generated by compose_assets.py
    (job "edges") from the data-edge attributes: the upper texture continues the band above at its exact
    tile phase (band height measured in Chrome at 600px), the lower texture continues into the next cell."""
    file = f"{A}n{n}-edge-{top}-{bottom}.jpg"
    light = top in LIGHT_TEX or bottom in LIGHT_TEX
    fb = FALLBACK[top]
    data = f'data-edge-top="{TEXN[top]}" data-edge-bottom="{TEXN[bottom]}"'
    dmimg, light_cls = "", ""
    if light:
        light_cls = "img-light"
        dmf = file.replace(".jpg", "-dm.jpg")
        dmimg = ('\n              ' + f'<!--[if !mso]><!--><img class="edge fluid img-dark" src="{dmf}" width="600" height="40" alt="" '
                 f'style="display:none; max-height:0; overflow:hidden; mso-hide:all; width:600px; max-width:100%; height:auto; border:0;"><!--<![endif]-->')
    return f"""
          <!-- MODULE:E18 Torn Edge ({top} to {bottom}) -->
          <tr>
            <td bgcolor="{fb}" style="padding:0; background-color:{fb}; font-size:0; line-height:0;">
              <img class="edge fluid {light_cls}" {data} src="{file}" width="600" height="40" alt="" style="display:block; width:600px; max-width:100%; height:auto; border:0;">{dmimg}
            </td>
          </tr>
          <!-- /MODULE:E18 -->
"""


def headline(parts: list, tag: str = "h2", align: str = "center", sans_color: str = WHITE,
             key_color: str = WHITE, dm: bool = False, margin: str = "0 0 14px 0") -> str:
    """Two-voice headline (kit v0.5): parts = [("s", text) | ("k", text, cls)], each its own line.
    s = Prompt 800 caps (lead), k = Playfair 900 caps (k-xl hero / k band / k-col column)."""
    out = []
    sizes = {"k-xl": (98, 90), "k": (96, 86), "k-col": (56, 54), "k-sm": (80, 74), "k-col50": (50, 50)}
    for i, part in enumerate(parts):
        pad_top = "padding-top:6px; " if i else ""
        if part[0] == "s":
            fs = part[2] if len(part) > 2 else 30
            out.append(f'<span class="lead{" dm-h" if dm else ""}" style="display:block; {pad_top}font-size:{fs}px; line-height:{fs + 4}px; '
                       f'mso-line-height-rule:exactly; letter-spacing:1.5px; color:{sans_color};">{part[1]}</span>')
        else:
            cls = part[2]
            fs, lh = sizes[cls]
            mcls = {"k-sm": "k", "k-col50": "k-col"}.get(cls, cls)
            out.append(f'<span class="{mcls} serif{" dm-h" if dm else ""}" style="display:block; {pad_top}font-family:{F_SERIF}; font-size:{fs}px; '
                       f'line-height:{lh}px; mso-line-height-rule:exactly; font-weight:900; letter-spacing:2px; color:{key_color};">{part[1]}</span>')
    return (f'<{tag} style="margin:{margin}; font-family:{F_SANS}; font-weight:800; color:{sans_color}; text-align:{align};">'
            + "".join(out) + f"</{tag}>")


def sub(text: str, color: str = WHITE, maxw: int = 460, align: str = "center", dm: bool = False, margin: str = "0 auto 18px auto") -> str:
    return (f'<p class="sub{" dm-muted" if dm else ""}" style="margin:{margin}; max-width:{maxw}px; font-family:{F_SANS}; font-size:15px; line-height:23px; '
            f'mso-line-height-rule:exactly; font-weight:500; letter-spacing:2.5px; color:{color}; text-align:{align};">{text}</p>')


def body(text: str, color: str = WHITE, maxw: int = 460, align: str = "center", dm: bool = False, margin: str = "0 auto 26px auto") -> str:
    return (f'<p class="bodyp{" dm-p" if dm else ""}" style="margin:{margin}; max-width:{maxw}px; font-family:{F_SANS}; font-size:17px; line-height:24px; '
            f'mso-line-height-rule:exactly; font-weight:400; letter-spacing:0.4px; color:{color}; text-align:{align};">{text}</p>')


def button(label: str, href: str, width: int = 320, align: str = "center", full_m: bool = True) -> str:
    """The one button of the batch (kit v0.5): #FF6400, white Prompt 800 17px, tracking 2px, radius 4px, 52px."""
    al = ' align="center"' if align == "center" else ""
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0"{al} class="btn{' btn-full' if full_m else ''}" style="margin:0{' auto' if align == 'center' else ''};">
                      <tr><td align="center" width="{width}" bgcolor="#FF6400" style="width:{width}px; border-radius:4px; background-color:#FF6400;">
                        <a href="{href}" target="_blank" style="display:block; padding:16px 12px; font-family:{F_BTN}; font-size:17px; line-height:20px; mso-line-height-rule:exactly; font-weight:800; letter-spacing:2px; color:#FFFFFF; text-decoration:none; border-radius:4px; text-align:center; white-space:nowrap;">{esc(up(label))}</a>
                      </td></tr>
                    </table>"""


def small_button(label: str, href: str, align: str = "center") -> str:
    """Small in-card variant (kit v0.5 E27/E29): 13px, padding 14px 22px, 44px tall, same colour."""
    m = "0 auto" if align == "center" else "0"
    al = ' align="center"' if align == "center" else ""
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0"{al} class="btn" style="margin:{m};">
                          <tr><td align="center" bgcolor="#FF6400" style="border-radius:4px; background-color:#FF6400;">
                            <a href="{href}" target="_blank" style="display:block; padding:14px 22px; font-family:{F_BTN}; font-size:13px; line-height:16px; mso-line-height-rule:exactly; font-weight:800; letter-spacing:2px; color:#FFFFFF; text-decoration:none; border-radius:4px; text-align:center; white-space:nowrap;">{esc(up(label))}</a>
                          </td></tr>
                        </table>"""


def item_text(p: dict, dark: bool = True, align: str = "center", title_px: int = 19) -> str:
    """Product text in the E27 pattern: title (client's product name) orange on dark / Tap Shoe on light,
    client's line, price 20px bold without underline, small button with the client's CTA."""
    tc = ORANGE if dark else TAP
    dc = WHITE if dark else TAP
    dmh = "" if dark else " dm-h"
    dmp = "" if dark else " dm-p"
    u = p["url"]
    return f"""<p class="ititle{dmh}" style="margin:0 0 8px 0; font-family:{F_SANS}; font-size:{title_px}px; line-height:{title_px + 3}px; mso-line-height-rule:exactly; font-weight:800; letter-spacing:1.2px; color:{tc}; text-align:{align};"><a href="{u}" target="_blank" class="{dmh.strip()}" style="color:{tc}; text-decoration:none;">{nb(up(p["name"]))}</a></p>
                        <p class="idesc{dmp}" style="margin:0 0 10px 0; font-family:{F_SANS}; font-size:15px; line-height:21px; mso-line-height-rule:exactly; font-weight:500; color:{dc}; text-align:{align};">{nb(p['desc'])}</p>
                        <p class="iprice{dmh}" style="margin:0 0 16px 0; font-family:{F_SANS}; font-size:20px; line-height:24px; mso-line-height-rule:exactly; font-weight:800; color:{dc}; text-align:{align};"><a href="{u}" target="_blank" class="{dmh.strip()}" style="color:{dc}; text-decoration:none;">{price(p['price'])}</a></p>
                        {small_button(p['cta'], u, align)}"""


def info_box(p: dict, width: int = 260, pad: str = "26px 18px 24px 18px", title_px: int = 19, with_desc: bool = True,
             with_btn: bool = True) -> str:
    """E27 Product Info Box (dark bands): 1px #FEF4C6 at 70%, radius 10px, centred."""
    u = p["url"]
    desc = (f'<p class="idesc" style="margin:0 0 10px 0; font-family:{F_SANS}; font-size:15px; line-height:21px; mso-line-height-rule:exactly; '
            f'font-weight:500; color:#FFFFFF;">{nb(p["desc"])}</p>') if with_desc else ""
    btn = small_button(p["cta"], u) if with_btn else ""
    pm = "16px" if with_btn else "0"
    return f"""<table role="presentation" class="box" width="{width}" cellpadding="0" cellspacing="0" border="0" align="center" style="width:{width}px; border:1px solid #FEF4C6; border-color:rgba(254,244,198,0.7); border-radius:10px; border-collapse:separate;">
                          <tr>
                            <td align="center" style="padding:{pad}; text-align:center; font-family:{F_SANS};">
                              <p class="ititle" style="margin:0 0 8px 0; font-size:{title_px}px; line-height:{title_px + 3}px; mso-line-height-rule:exactly; font-weight:800; letter-spacing:1.2px; color:#FF6400;"><a href="{u}" target="_blank" style="color:#FF6400; text-decoration:none;">{nb(up(p["name"]))}</a></p>
                              {desc}
                              <p class="iprice" style="margin:0 0 {pm} 0; font-size:20px; line-height:24px; mso-line-height-rule:exactly; font-weight:800; color:#FFFFFF;"><a href="{u}" target="_blank" style="color:#FFFFFF; text-decoration:none;">{price(p['price'])}</a></p>
                              {btn}
                            </td>
                          </tr>
                        </table>"""


def img(src: str, w: int, h: int, alt: str, cls: str = "", style: str = "", href: str | None = None, attrs: str = "") -> str:
    tag = (f'<img class="{cls}"{" " + attrs if attrs else ""} src="{src}" width="{w}" height="{h}" alt="{alt}" style="display:block; width:{w}px; max-width:100%; '
           f'height:auto; border:0; margin:0 auto; font-family:Helvetica,Arial,sans-serif; font-size:14px; line-height:20px; color:#B0A89C;{style}">')
    return f'<a href="{href}" target="_blank" style="text-decoration:none;">{tag}</a>' if href else tag


def bimg(key: str, w: int, h: int, alt: str, cls: str = "pk", style: str = "", href: str | None = None, dm: bool = False) -> str:
    """Baked image (compose_assets.py job "bake" measures where it sits and builds it from those tile rows).
    dm=True: light-paper band, so the -dm twin follows (img-light / img-dark, only the light one is measured)."""
    src = f"{A}{key}.jpg"
    if not dm:
        return img(src, w, h, alt, cls=cls, style=style, href=href, attrs=f'data-bake="{key}"')
    return (img(src, w, h, alt, cls=f"{cls} img-light", style=style, href=href, attrs=f'data-bake="{key}"') + '<!--[if !mso]><!-->'
            + img(src.replace(".jpg", "-dm.jpg"), w, h, alt, cls=f"{cls} img-dark",
                  style=style + " display:none; max-height:0; overflow:hidden; mso-hide:all;", href=href) + '<!--<![endif]-->')


def frow(key: str, w: int, h: int, alt: str, href: str | None, text: str, side: str = "left", rise: bool = False,
         mob: str = "full", tpad: str = "0 40px 0 12px", hu: int = 64, valign: str = "middle", dm: bool = False,
         tcls: str = "") -> str:
    """Round 4 feature row: a big baked image beside a text column (image cell first in the DOM, so on mobile
    the image comes first). side="right" mirrors it with dir=rtl. rise=True: the image opens the band cell
    and carries, above css row `hu`, the band ABOVE torn over this one (the product crosses that torn edge);
    the text column starts with the other half of the same torn line (desktop only, ~t piece). mob="full":
    the image spans the mobile width (bleeds and tears keep reaching the edge); "cen": desktop size, centred."""
    d = ' dir="rtl"' if side == "right" else ""
    tw = 600 - w
    mcls = "fr-full" if mob == "full" else "fr-cen"
    image = bimg(key, w, h, alt, cls=f"pk {mcls}", style=" margin:0;", href=href, dm=dm)
    tear, th = "", h
    if rise:
        ph = hu + 24
        tsrc = f"{A}{key}-t.jpg"
        piece = (f'<img class="edge img-light" data-bake="{key}~t" src="{tsrc}" width="{tw}" height="{ph}" alt="" style="display:block; width:{tw}px; height:{ph}px; border:0;">'
                 if dm else f'<img class="edge" data-bake="{key}~t" src="{tsrc}" width="{tw}" height="{ph}" alt="" style="display:block; width:{tw}px; height:{ph}px; border:0;">')
        if dm:
            piece += ('<!--[if !mso]><!-->' + f'<img class="edge img-dark" src="{tsrc.replace(".jpg", "-dm.jpg")}" width="{tw}" height="{ph}" alt="" '
                      f'style="display:none; max-height:0; overflow:hidden; mso-hide:all; width:{tw}px; height:{ph}px; border:0;">' + '<!--<![endif]-->')
        tear = f"""
                            <tr><td class="desk-only" height="{ph}" style="height:{ph}px; padding:0; font-size:0; line-height:0;">{piece}</td></tr>"""
        th = h - ph
    return f"""
                <tr>
                  <td style="padding:0;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"{d} style="table-layout:fixed; width:100%;">
                      <tr>
                        <td width="{w}" class="stack fr-img" dir="ltr" valign="top" style="width:{w}px; padding:0; vertical-align:top; font-size:0; line-height:0;">
                          {image}
                        </td>
                        <td width="{tw}" class="stack fr-txt" dir="ltr" valign="top" style="width:{tw}px; padding:0; vertical-align:top;">
                          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{tear}
                            <tr><td class="fr-pad {tcls}" valign="{valign}" height="{th}" style="height:{th}px; padding:{tpad}; vertical-align:{valign}; text-align:left;">
                              {text}
                            </td></tr>
                          </table>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>"""


def tag(body_html: str, key: str, anchor: str, tone: str, h: int, ew: int, pad: str = "0 24px 0 26px") -> str:
    """Round 6: paper label (the kit's E33 label device) as a torn label: a flat cell in a kit colour (light
    #E2DDD9 with Tap Shoe text, or Tap Shoe with orange text) holding live text, plus the ripped end as a small
    transparent PNG (assets/{key}-tag-{tone}-{l|r}.png, compose_assets.py) on the free side(s). anchor: "left" /
    "right" (the label runs into the email edge, torn on the other side) or "center" (torn on both sides).
    Height fixed (h px) so the torn end matches; the mobile height is set per key in the media query."""
    bg = "#E2DDD9" if tone == "light" else "#2A2B2D"

    def end(side):
        return (f'<td class="tag-endc-{key}" width="{ew}" align="{"right" if side == "l" else "left"}" valign="top" style="width:{ew}px; padding:0; font-size:0; line-height:0; vertical-align:top;">'
                f'<img class="tag-end-{key}" src="{A}{key}-tag-{tone}-{side}.png" width="{ew}" height="{h}" alt="" '
                f'style="display:block; width:{ew}px; height:{h}px; border:0;"></td>')
    cells = ((end("l") if anchor in ("center", "right") else "")
             + f'<td class="tag-body-{key}" bgcolor="{bg}" height="{h}" valign="middle" style="height:{h}px; padding:{pad}; '
               f'background-color:{bg}; vertical-align:middle; text-align:left; white-space:nowrap;">{body_html}</td>'
             + (end("r") if anchor in ("center", "left") else ""))
    m = "0 auto" if anchor == "center" else "0"
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="{anchor}" class="tag tag-{anchor}" '
            f'style="margin:{m}; border-collapse:collapse;"><tr>{cells}</tr></table>')


def tier_tag(amount: str, anchor: str) -> str:
    """05 price-tier header (round 6): UNDER (Prompt 800) over the amount (Playfair 900), Tap Shoe on a light
    torn label; the words are the client's tier titles ('UNDER $30' ...)."""
    body = (f'<h2 style="margin:0; font-family:{F_SANS}; font-weight:800; color:{TAP}; text-align:left;">'
            f'<span class="tag-s" style="display:block; font-size:22px; line-height:26px; mso-line-height-rule:exactly; letter-spacing:3px; color:{TAP};">UNDER</span>'
            f'<span class="tag-k serif" style="display:block; font-family:{F_SERIF}; font-size:96px; line-height:100px; mso-line-height-rule:exactly; '
            f'font-weight:900; letter-spacing:2px; color:{TAP};">{amount}</span></h2>')
    return tag(body, "n5", anchor, "light", 148, 16)


TAG_CSS_05 = """      .tag-body-n5 { height: 112px !important; padding: 0 24px 0 22px !important; }
      .tag-end-n5 { height: 112px !important; width: 12px !important; }
      .tag-endc-n5 { width: 12px !important; }
      .tag-s { font-size: 17px !important; line-height: 20px !important; letter-spacing: 2.5px !important; }
      .tag-k { font-size: 68px !important; line-height: 72px !important; }"""


def logo(dark_bg: bool = True, pad: str = "36px 40px 0 40px") -> str:
    if dark_bg:
        return f"""
                <tr>
                  <td align="center" class="px" style="padding:{pad};">
                    <a href="{{{{HOME_URL}}}}" target="_blank" style="text-decoration:none;"><img src="{K}logo-dark.png" width="160" height="26" alt="Habit" style="display:block; width:160px; height:26px; border:0; margin:0 auto; font-family:Helvetica,Arial,sans-serif; font-size:16px; color:#FFFFFF;"></a>
                  </td>
                </tr>"""
    return f"""
                <tr>
                  <td align="center" class="px" style="padding:{pad};">
                    <a href="{{{{HOME_URL}}}}" target="_blank" style="text-decoration:none;"><img class="img-light" src="{K}logo-light.png" width="160" height="26" alt="Habit" style="display:block; width:160px; height:26px; border:0; margin:0 auto; font-family:Helvetica,Arial,sans-serif; font-size:16px; color:#2A2B2D;"><!--[if !mso]><!--><img class="img-dark" src="{K}logo-dark.png" width="160" height="26" alt="Habit" style="display:none; max-height:0; overflow:hidden; mso-hide:all; width:160px; height:26px; border:0; margin:0 auto;"><!--<![endif]--></a>
                  </td>
                </tr>"""


def row(inner: str, pad: str = "0 40px", cls: str = "px", align: str = "center", extra: str = "") -> str:
    return f"""
                <tr>
                  <td align="{align}" class="{cls}" style="padding:{pad}; text-align:{align};{extra}">
                    {inner}
                  </td>
                </tr>"""


def footer() -> str:
    """E13 Closing Band + E14 Legal Footer, kit v0.5 (address and unsubscribe come from the Omnisend footer)."""
    nav = ""
    for i, (lab, ph) in enumerate((("MEN&rsquo;S", "MENS_URL"), ("WOMEN&rsquo;S", "WOMENS_URL"), ("YOUTH", "YOUTH_URL"), ("SALE", "SALE_URL"))):
        bl = " border-left:1px solid #FFFFFF;" if i else ""
        nav += (f'\n                  <td class="nav-td" style="padding:0 25px;{bl}"><a href="{{{{{ph}}}}}" target="_blank" class="nav-a" style="font-family:{F_BTN}; '
                f'font-size:16px; line-height:20px; mso-line-height-rule:exactly; font-weight:500; letter-spacing:2.5px; color:#FFFFFF; text-decoration:none; white-space:nowrap;">{lab}</a></td>')
    return f"""
          <!-- MODULE:E13 Closing Band (kit v0.5, identical in the five emails) -->
          <tr>
            <td align="center" class="px" bgcolor="#2A2B2D" style="padding:35px 40px 0 40px; background-color:#2A2B2D; font-family:{F_BTN};">
              <a href="{{{{HOME_URL}}}}" target="_blank" style="text-decoration:none;"><img src="{K}logo-footer.png" width="136" height="61" alt="Habit" style="display:block; width:136px; height:61px; border:0; margin:0 auto; font-family:Helvetica,Arial,sans-serif; font-size:16px; color:#FFFFFF;"></a>
            </td>
          </tr>
          <!-- /MODULE:E13 -->
          <!-- MODULE:E14 Legal Footer (kit v0.5: menu, Instagram icon row 44px, copyright; address and unsubscribe from the Omnisend footer) -->
          <tr>
            <td align="center" class="px footer" bgcolor="#2A2B2D" style="padding:30px 40px 60px 40px; background-color:#2A2B2D; font-family:{F_BTN};">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:0 auto 44px auto;">
                <tr>{nav}
                </tr>
              </table>
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center" style="margin:0 auto 32px auto;">
                <tr>
                  <td width="44" valign="middle" style="width:44px; padding:0 14px 0 0; vertical-align:middle;"><a href="{{{{INSTAGRAM_URL}}}}" target="_blank" style="text-decoration:none;"><img src="{K}icon-instagram.png" width="44" height="44" alt="Instagram" style="display:block; width:44px; height:44px; border:0; font-family:Helvetica,Arial,sans-serif; font-size:12px; color:#FFFFFF;"></a></td>
                  <td valign="middle" align="left" style="vertical-align:middle; text-align:left; font-family:{F_BTN};">
                    <p style="margin:0 0 3px 0; font-family:{F_BTN}; font-size:13px; line-height:18px; mso-line-height-rule:exactly; font-weight:500; letter-spacing:1px; color:#FFFFFF;">Follow us on Instagram</p>
                    <p style="margin:0; font-size:15px; line-height:20px; mso-line-height-rule:exactly;"><a href="{{{{INSTAGRAM_URL}}}}" target="_blank" style="font-family:{F_BTN}; font-size:15px; line-height:20px; font-weight:800; letter-spacing:2px; color:#FFFFFF; text-decoration:none;">@HABITOUTDOORS</a></p>
                  </td>
                </tr>
              </table>
              <p class="legal" style="margin:0; font-family:{F_BTN}; font-size:13px; line-height:18px; mso-line-height-rule:exactly; font-weight:400; letter-spacing:1px; color:#E2DDD9;">&copy; 2026, Habit Outdoors. Built By Wilde Creative.</p>
            </td>
          </tr>
          <!-- /MODULE:E14 -->
"""


def P(name, desc, url, cta, pr):
    return {"name": name, "desc": desc, "url": url, "cta": cta, "price": pr}


# ================================================================ 01 Women's Cedar Branch

def email_01():
    W1 = [
        P("Women's Cedar Branch Insulated Waterproof Bibs", "Rain-Factor waterproofing with quiet tricot fabric and a 2-way front zipper.",
          "https://www.habitoutdoors.com/products/womens-cedar-branch-insulated-bib?variant=52632803705114", "Shop Bibs", "99.99"),
        P("Women's Cedar Branch Insulated Parka", "The matching top half. Insulated, waterproof, and built to pair with the bibs for complete protection.",
          "https://www.habitoutdoors.com/collections/womens/products/habit-womens-cedar-branch-insulated-parka?variant=51265331855642", "Shop Parka", "89.99"),
        P("Women's Early Dawn Sherpa Shell Jacket", "SherpaShell exterior with fleece-lined interior, windproof and water-resistant with a harness pass-through.",
          "https://www.habitoutdoors.com/collections/womens/products/womens-early-dawn-sherpa-shell-jacket?variant=52697130893594", "Shop Sherpa Shell", "69.99"),
    ]
    # Round 4 (owner): people in the hero and in the last call; the three products scaled up so each owns its
    # band, alternating sides with the text beside them: the bib stands large on the left (one ground line),
    # the parka rises over the torn edge into the brown band and is cut by the email's right edge, the sherpa
    # shell rises over the torn edge into the Tap Shoe band. Every image is baked on its measured position.
    alts = ["Habit Women&rsquo;s Cedar Branch Insulated Waterproof Bibs in Realtree APX",
            "Habit Women&rsquo;s Cedar Branch Insulated Parka in Realtree APX",
            "Habit Women&rsquo;s Early Dawn Sherpa Shell Jacket in Realtree APX"]
    rows = []
    hero = logo(True) + row(headline([("s", "COLD WEATHER"), ("k", "COVERED", "k-xl")], tag="h1"), pad="28px 40px 0 40px") \
        + row(bimg("n1-hero", 600, 330, "A woman in Habit Realtree outerwear walking into the autumn woods with her family",
                   cls="photo fluid", href="{{WOMENS_URL}}"), pad="4px 0 0 0", cls="") \
        + row(sub("WOMEN&rsquo;S OUTERWEAR WITH REAL FIELD&nbsp;TECH"), pad="6px 40px 0 40px") \
        + row(button("Shop Women's", "{{WOMENS_URL}}", 300), pad="6px 40px 52px 40px")
    rows.append(band("ivy", hero, "E24 Hero on Ivy Green grain (women&rsquo;s line colour) · headline, in-use photo of the women&rsquo;s line as a torn print on the band (round 6: ripped top and bottom, no fade), subheadline, button", height=None))
    rows.append(edge("ivy", "paper", "1"))

    def ptext(i):
        return item_text(W1[i], dark=True, align="left", title_px=20)

    def product(i):
        if i == 0:
            return frow("n1-p-bib", 300, 500, alts[0], W1[0]["url"], ptext(0), side="left", mob="cen",
                        tpad="0 44px 0 4px", tcls="center-m")
        if i == 1:
            return frow("n1-p-parka", 300, 520, alts[1], W1[1]["url"], ptext(1), side="right", rise=True,
                        tpad="0 8px 24px 44px", tcls="center-m")
        return frow("n1-p-sherpa", 300, 460, alts[2], W1[2]["url"], ptext(2), side="left", rise=True,
                    tpad="0 44px 24px 8px", tcls="center-m")

    b2 = row(headline([("s", "THREE WAYS TO OWN THE"), ("k", "SEASON", "k")], sans_color=TAP, key_color=TAP, dm=True), pad="44px 40px 0 40px") \
        + row(sub("FROM INSULATED BIBS TO SHERPA&nbsp;SHELLS", color=MUTED_L, dm=True), pad="0 40px") \
        + row(body(nb("The Cedar Branch Bibs pair with the Parka for full waterproof coverage and the Early Dawn Sherpa Shell adds windproof warmth when temperatures really drop."), color=TAP, dm=True, maxw=470, margin="0 auto 0 auto"), pad="0 40px 48px 40px")
    rows.append(band("paper", b2, "E25 Textured Band light paper · two-voice headline, subheadline, body (intro of the product stack)"))
    rows.append(edge("paper", "brown", "1"))
    rows.append(band("brown", product(0), "E25 Major Brown grain · product 1/3: the bib standing large on the left (one ground line), text right"))
    rows.append(band("tapshoe", product(1), "E25 Tap Shoe paper · product 2/3: the parka rising over the torn edge into the brown band, cut by the email&rsquo;s right edge, text left (torn edge baked in the image and the text column)"))
    rows.append(band("brown", product(2), "E25 Major Brown grain · product 3/3: the sherpa shell rising over the torn edge into the Tap Shoe band, text right"))

    # Closing on Ivy grain (women's line colour; the kit allows white text only on it, so the serif is white).
    # Round 4: a person instead of the garments from the back: the woman in the camp chair, bleeding off the
    # left edge under the torn brown sheet.
    ctext = (headline([("s", "EXPLORE THE", 28), ("k", "FULL", "k-sm"), ("s", "COLLECTION", 28)], align="left")
             + body(nb("Hunting tops, fishing apparel, and cold weather outerwear all built with the same performance tech. Browse the full women's collection and gear up for the season."), align="left", maxw=268, margin="0"))
    b3 = frow("n1-close", 300, 360, "A woman in the Habit Women&rsquo;s Cedar Branch parka relaxing in a camp chair with her family at the edge of a field",
              "{{WOMENS_COLLECTION_URL}}", ctext, side="left", rise=True, hu=34, tpad="18px 40px 0 22px", tcls="center-m") \
        + row(button("Shop Women's Collection", "{{WOMENS_COLLECTION_URL}}", 440), pad="28px 40px 56px 40px")
    rows.append(band("ivy", b3, "E26-style photo + E25 on Ivy grain · in-use photo left (bleeds off the left edge, under the torn brown sheet, round 6: ripped on its right and bottom sides, no fade), two-voice headline and body right, wide button (last call)"))
    rows.append(edge("ivy", "footer", "1"))
    rows.append(footer())
    meta = {
        "Habit Outdoors": "November 2026 Broadcasts · 01 Women's Cedar Branch Bib + Parka (send Thu Nov 5) · built 2026-10-08 (round 6: torn edges instead of fades)",
        "Subject": "Her Gear Is Field Ready \U0001F98C",
        "Preheader": "Insulated and waterproof from head to toe",
        "Modules": "E24-style hero on tex-grain-ivy (logo, two-voice headline, in-use photo as a torn print ripped top and bottom, subheadline, button) / E18 / E25 light paper (headline, subheadline, body) / E18 / 3 feature rows on grain-brown / paper-tapshoe / grain-brown, alternating sides, products 2 and 3 crossing the torn edge above / in-use photo (torn print, ripped right and bottom) + E25 on grain-ivy crossing under the torn brown edge (headline, body, button) / E18 / E13 + E14",
        "Button": "#FF6400 / #FFFFFF",
        "Reference": "ref1 Duck Camp New Terrain Guard (product stack separated by torn edges) + October Oct 6 (bib standing large, parka cut by the edge) and Oct 22 (people, products breaking the band). Structure only.",
        "Bands": "preheader, hero, products (structure), full collection (last call), footer = 5",
        "Source": "copy-source.md Email 1 (verbatim), products.json (store prices 2026-10-07), brief.md",
        "Links": "product URLs exactly as in the copy; {{WOMENS_URL}} and {{WOMENS_COLLECTION_URL}} have no URL in the copy ([[CONFIRMAR]] in brief.md); address and unsubscribe come from the Omnisend footer",
    }
    return page(meta, rows)


# ================================================================ 02 Gift Guide #1

def email_02():
    G = [
        P("Men's Flushing Bay Short Sleeve Fishing Shirt", "UPF 50+ sun protection with moisture-wicking and quick-dry fabric. The go-to warm-weather fishing shirt.",
          "https://www.habitoutdoors.com/collections/outdoor-apparel/products/mens-flushing-bay-short-sleeve-river-shirt?variant=51114509599002", "Shop Now", "29.99"),
        P("Men's Flushing Bay Long Sleeve River Fishing Shirt", "Same performance with full arm coverage. Built for long days on the water when the sun won't quit.",
          "https://www.habitoutdoors.com/collections/mens/products/mens-flushing-bay-long-sleeve-river-shirt?variant=51745607516442", "Shop Now", "34.99"),
        P("Men's Cedar Branch Insulated Waterproof Bomber", "Rain-Factor waterproofing with full insulation in a bomber cut. Cold weather covered.",
          "https://www.habitoutdoors.com/collections/mens/products/habit-mens-wj657-cedar-branch-insulated-waterproof-bomber?variant=51265344733466", "Shop Bomber", "74.99"),
        P("Men's Summit Park Performance Hoodie", "Soft polyester fleece with Scent-Factor tech and a kangaroo pocket. Layer it or wear it solo.",
          "https://www.habitoutdoors.com/collections/mens/products/habit-mens-summit-park-performance-hoodie-1?variant=52713641804058", "Shop Hoodie", "39.99"),
        P("Men's 800gram Insulated 15\" Waterproof Rubber Boots", "Insulated and waterproof from the ground up. Built for mud, cold, and long sits in the stand.",
          "https://www.habitoutdoors.com/collections/outdoor/products/mens-insulated-boot?variant=39941172592691", "Shop Boots", "89.99"),
        P("Knit Camo Stocking Cap", "The easy add-on. Warm, simple, and always appreciated.",
          "https://www.habitoutdoors.com/collections/outdoor/products/knit-camo-stocking-cap?variant=39479198580787", "Shop Now", "12.99"),
    ]
    alts = ["Habit Men&rsquo;s Flushing Bay Short Sleeve Fishing Shirt in Sedona Sage",
            "Habit Men&rsquo;s Flushing Bay Long Sleeve River Fishing Shirt in Peach Nectar",
            "Habit Men&rsquo;s Cedar Branch Insulated Waterproof Bomber in Realtree APX",
            "Habit Men&rsquo;s Summit Park Performance Hoodie in Woodland Ghost Khaki",
            "Habit Men&rsquo;s 800gram Insulated 15 inch Waterproof Rubber Boots in Realtree Edge",
            "Habit Knit Camo Stocking Cap in Brown Camo, in front of a photo of three anglers fly fishing from a boat"]
    rows = []
    hero = logo(True) + row(headline([("s", "THE OUTDOOR LOVER&rsquo;S"), ("k", "GIFT<br>LIST", "k-xl")], tag="h1", key_color=ORANGE), pad="28px 40px 0 40px") \
        + row(sub("TOP PICKS FROM THE FIELD TO THE&nbsp;WATER", maxw=420), pad="4px 40px 0 40px") \
        + row(button("Shop Gift Guide", "{{GIFT_GUIDE_URL}}", 320), pad="6px 40px 0 40px") \
        + row(img(A + "n2-hero-collage.jpg", 600, 500, "Collage of five overlapping framed photos: hunters by a UTV, an angler at his tackle box, an angler wading a river, a hunter leaving a blind and a trout in hand",
                  cls="photo fluid"), pad="44px 0 0 0", cls="")
    rows.append(band("tapshoe", hero, "Hero on Tap Shoe paper · two-voice headline, subheadline, button, framed photo collage, round 6: five prints in one tight overlapping pile (ref2 polaroid collage), the paper tears into the next band under the two bottom prints"))

    # Round 6 (owner direction, 02 moved least): no boxed cards, no grey panels. Big clean cut-outs on the
    # Patriot water, alternating sides, text beside each (05 pattern), scale varied: the bomber cut by the left
    # edge, the boots big, the cap grouped with a people photo (crop-sent-sep22-boat-anglers since round 6b)
    # that bleeds off the right edge. Same order, literal content.
    SIZES = [(260, 280), (260, 300), (300, 360), (260, 300), (300, 320), (300, 380)]

    def prow2(i):
        p = G[i]
        w, h = SIZES[i]
        right = i % 2 == 1
        d = ' dir="rtl"' if right else ""
        tpad = "20px 20px 20px 40px" if right else "20px 40px 20px 20px"
        return f"""
                <tr>
                  <td style="padding:0 0 4px 0;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"{d} style="table-layout:fixed; width:100%;">
                      <tr>
                        <td width="{w}" class="stack r2-img" dir="ltr" valign="middle" style="width:{w}px; padding:0; vertical-align:middle; font-size:0; line-height:0;">
                          {bimg(f"n2-p-{i + 1}", w, h, alts[i], cls="pk r2-pic", style=" margin:0;", href=p["url"])}
                        </td>
                        <td class="stack center-m r2-txt" dir="ltr" valign="middle" style="padding:{tpad}; vertical-align:middle; text-align:left;">
                        {item_text(p, dark=True, align="left", title_px=19)}
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>"""

    grid = "".join(prow2(i) for i in range(6))
    b2 = row(headline([("s", "OUR"), ("k", "TOP<br>PICKS", "k"), ("s", "THIS SEASON")], key_color=ORANGE), pad="20px 40px 0 40px") \
        + row(sub("FROM FISHING SHIRTS TO INSULATED&nbsp;BOOTS", maxw=420), pad="0 40px") \
        + row(body(nb("From UPF 50+ fishing shirts that keep them cool on the water to insulated boots and bombers that handle the coldest mornings, these are the pieces they'll use all year."), maxw=480, margin="0 auto 36px auto"), pad="0 40px") \
        + grid + row("", pad="0 0 24px 0", cls="")
    rows.append(band("patriotflat", b2, "E25 flat Patriot (round 6: was the water texture, which scales on mobile and boxed every baked product) · two-voice headline, subheadline, body + 6 product rows, round 6: big cut-outs on the band alternating sides (bomber cut by the left edge, cap grouped with a people photo bleeding off the right edge), title, line, price, CTA"))
    rows.append(edge("patriotflat", "paper", "2"))
    gcu = "https://www.habitoutdoors.com/products/gift-card?variant=16072202977331"
    # Round 2 (QA r1): headline across the full width, then the tilted gift card beside subheadline, body and
    # button (no tall void beside the card); the card is baked on light paper with a dark-mode twin.
    # Round 4: the gift card overlaps a framed photo of a hunter (people in the angle shift), baked on the
    # paper at its measured position, with the dark-mode twin.
    gc_alt = "Habit Outdoors gift card over a framed photo of a hunter by his truck"
    gcimg = bimg("n2-gift", 266, 240, gc_alt, cls="pk", style=" margin:0;", href=gcu, dm=True)
    b3 = row(headline([("k", "NOT SURE", "k-sm"), ("s", "WHAT TO GET&nbsp;THEM", 26)], align="left", sans_color=TAP, key_color=TAP, dm=True, margin="0"), pad="48px 40px 0 40px", align="left") + f"""
                <tr>
                  <td style="padding:0;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td width="300" class="stack gc-img" valign="middle" style="width:280px; padding:12px 0 40px 20px; vertical-align:middle; font-size:0; line-height:0;">
                          {gcimg}
                        </td>
                        <td width="300" class="stack px center-m gc-txt" valign="middle" style="width:260px; padding:24px 40px 52px 0; vertical-align:middle; text-align:left;">
                          {sub("A HABIT GIFT CARD ALWAYS FITS&nbsp;RIGHT", color=MUTED_L, align="left", maxw=260, dm=True, margin="0 0 14px 0")}
                          {body(nb("A Habit Outdoors gift card lets them choose exactly what they need for their next trip. Available in any amount and delivered straight to their inbox.."), color=TAP, align="left", maxw=260, dm=True, margin="0 0 24px 0")}
                          {button("Shop Gift Cards", gcu, 260, align="left")}
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>"""
    rows.append(band("paper", b3, "E31 Tilted Framed Photo on light paper · headline serif first across the band, then the store gift card (tilted, baked on paper + dark twin) beside subheadline, body, button (angle shift)"))
    rows.append(edge("paper", "footer", "2"))
    rows.append(footer())
    meta = {
        "Habit Outdoors": "November 2026 Broadcasts · 02 Gift Guide #1 (send Tue Nov 10) · built 2026-10-08 (round 6) · copy marked Needs Edit by the client",
        "Subject": "The Outdoor Gift Guide Is Here \U0001F381",
        "Preheader": "Gear they'll reach for all season long",
        "Modules": "Hero on tex-paper-tapshoe (logo, two-voice headline, subheadline, button, round 6 photo collage: five overlapping prints, the bottom two lying over the torn edge into Patriot) / E25 Patriot water (headline, subheadline, body) + 2-up framed product cards x3 on a flat Patriot fill, each product rising out of its panel (the cap shown worn) / E18 / E31 on light paper (headline, then the gift card over a framed photo of a hunter beside subheadline, body, button) / E18 / E13 + E14",
        "Button": "#FF6400 / #FFFFFF",
        "Reference": "ref2 Duck Camp Fall '26 (collage of overlapping framed photos) for the hero. Structure only.",
        "Bands": "preheader, hero, top picks (structure), gift card (angle shift), footer = 5",
        "Source": "copy-source.md Email 2 (verbatim, including 'inbox..'), products.json (store prices 2026-10-07), brief.md",
        "Links": "product and gift card URLs exactly as in the copy; {{GIFT_GUIDE_URL}} has no URL in the copy ([[CONFIRMAR]] in brief.md)",
    }
    extra = """      .r2-img { text-align: center !important; }
      .r2-pic { margin: 0 auto !important; }
      .r2-txt { padding: 4px 32px 36px 32px !important; }
      .gc-img { padding: 32px 24px 0 24px !important; text-align: center !important; }
      .gc-img img { margin: 0 auto !important; }
      .gc-txt { padding: 32px 24px 52px 24px !important; }"""
    return page(meta, rows, extra)


# ================================================================ 03 Buck Hollow 2.0

def email_03():
    J = P("Men's Buck Hollow 2.0 Jacket", "Uninsulated, all-season waterproof shell with quiet tricot fabric and a high standing hood.",
          "https://www.habitoutdoors.com/products/mens-buck-hollow-2-0-jacket?variant=52600921129242", "Shop Jacket", "74.99")
    PT = P("Men's Buck Hollow 2.0 Pant", "Same Rain-Factor waterproofing with knee articulation, bottom leg zippers, and a reinforced seat for long sits.",
           "https://www.habitoutdoors.com/products/mens-buck-hollow-2-0-pant?variant=52630349775130", "Shop Pant", "79.99")
    rows = []
    # Round 6 (owner): full-bleed photo hero (ref1 New Terrain Guard, ref6). orig-hunt40 covers the whole band,
    # 600 wide, down to the torn edge into the system band (baked in the image, -dm twin for the dark paper).
    # Live text in the top-left corner, over a soft local darkening inside the photo; the kicker sits on a
    # dark torn label (kit E33 device: orange on Tap Shoe, AA whatever the leaves do). Headline BUCK /
    # HOLLOW&nbsp;2.0: "2.0" never alone on a line. Mobile: its own crop (n3-hero-m, 375 x 750), same principle.
    kicker = (f'<p class="k3" style="margin:0; font-family:{F_SANS}; font-size:20px; line-height:24px; mso-line-height-rule:exactly; '
              f'font-weight:800; letter-spacing:2px; color:{ORANGE}; white-space:nowrap;">NEW FOR 2026:</p>')
    title = (f'<h1 style="margin:0; font-family:{F_SANS}; font-weight:800; color:{WHITE}; text-align:left;">'
             f'<span class="h3k serif" style="display:block; font-family:{F_SERIF}; font-size:60px; line-height:58px; mso-line-height-rule:exactly; '
             f'font-weight:900; letter-spacing:2px; color:{WHITE};">BUCK</span>'
             f'<span class="h3k serif" style="display:block; font-family:{F_SERIF}; font-size:60px; line-height:58px; mso-line-height-rule:exactly; '
             f'font-weight:900; letter-spacing:2px; color:{WHITE}; white-space:nowrap;">HOLLOW&nbsp;2.0</span></h1>')
    hero = f"""
                <tr><td class="h3-px h3-logo" style="padding:40px 40px 0 44px; text-align:left;"><a href="{{{{HOME_URL}}}}" target="_blank" style="text-decoration:none;"><img src="{K}logo-dark.png" width="160" height="26" alt="Habit" style="display:block; width:160px; height:26px; border:0; margin:0; font-family:Helvetica,Arial,sans-serif; font-size:16px; color:#FFFFFF;"></a></td></tr>
                <tr><td class="h3-tag" style="padding:34px 0 0 0; text-align:left;">{tag(kicker, "n3", "left", "dark", 44, 12, pad="0 16px 0 44px")}</td></tr>
                <tr><td class="h3-px h3-h1" style="padding:18px 40px 0 44px; text-align:left;">{title}</td></tr>
                <tr><td class="h3-px h3-sub" style="padding:16px 40px 0 44px; text-align:left;">{sub("JACKET AND PANT THAT WORK AS&nbsp;ONE", align="left", maxw=380, margin="0")}</td></tr>
                <tr><td class="h3-px h3-btn" style="padding:24px 40px 0 44px; text-align:left;">{button("Shop Buck Hollow 2.0", "{{BUCK_HOLLOW_URL}}", 288, align="left")}</td></tr>
                <tr><td class="h3-bottom" height="427" style="height:427px; font-size:0; line-height:0;">&nbsp;</td></tr>"""
    rows.append(f"""
          <!-- MODULE:E24 Full-Bleed Photo Hero, round 6 (n3-hero.jpg 600x820: orig-hunt40, bowhunter in the golden woods, soft darkening in the top-left corner under the text, torn edge into the light paper baked at the bottom, -dm twin; mobile swaps to n3-hero-m.jpg 375x750 via .hero3); fallback #2A2B2D -->
          <tr>
            <td align="left" valign="top" class="hero3" background="{A}n3-hero.jpg" bgcolor="#2A2B2D" style="mso-padding-alt:0px; padding:0; background-color:#2A2B2D; background-image:url('{A}n3-hero.jpg'); background-size:cover; background-position:center bottom; background-repeat:no-repeat; vertical-align:top;">
              <!--[if gte mso 9]><v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px;height:820px;"><v:fill type="frame" src="{A}n3-hero.jpg" color="#2A2B2D" /><v:textbox style="mso-fit-shape-to-text:true;" inset="0,0,0,0"><div><![endif]-->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{hero}
              </table>
              <!--[if gte mso 9]></div></v:textbox></v:rect><![endif]-->
            </td>
          </tr>
          <!-- /MODULE:E24 -->
""")

    def callout(label):
        return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" class="co" style="margin:0 0 12px 0;"><tr>'
                f'<td width="26" valign="middle" style="width:26px; padding:0 10px 0 0; vertical-align:middle;"><table role="presentation" width="26" cellpadding="0" cellspacing="0" border="0" style="width:26px;">'
                f'<tr><td height="2" bgcolor="#FF6400" style="height:2px; font-size:0; line-height:0; background-color:#FF6400;"></td></tr></table></td>'
                f'<td valign="middle" style="vertical-align:middle;"><p class="clabel dm-h" style="margin:0; font-family:{F_SANS}; font-size:13px; line-height:17px; mso-line-height-rule:exactly; '
                f'font-weight:800; letter-spacing:1.5px; color:#2A2B2D; text-align:left;">{label}</p></td></tr></table>')

    L1, L2, L3, L4 = "FLEECE HAND&#8209;WARMER POCKETS", "HARNESS PASS&#8209;THRU", "KNEE ARTICULATION", "BOTTOM LEG ZIPPERS"
    sys_alt = "Habit Men&rsquo;s Buck Hollow 2.0 Jacket worn over the Buck Hollow 2.0 Pant, Realtree APX, as one system"
    stext = (headline([("s", "QUIET ENOUGH TO", 24), ("k", "SIT<br>ALL&nbsp;DAY", "k-col")], align="left", sans_color=TAP, key_color=TAP, dm=True)
             + sub("RAIN-FACTOR TECH MEETS SOFT&nbsp;TRICOT", color=MUTED_L, dm=True, align="left", maxw=260, margin="0 0 16px 0")
             + body(nb("Rain-Factor waterproofing, Scent-Factor tech, fleece hand-warmer pockets, and a harness pass-thru on the jacket. Knee articulation and leg zippers on the pant."), color=TAP, dm=True, align="left", maxw=260, margin="0 0 22px 0")
             + callout(L1) + callout(L2) + callout(L3) + callout(L4))
    b2 = frow("n3-sys", 300, 600, sys_alt, None, stext, side="left", dm=True, tpad="34px 36px 0 4px",
              valign="top", tcls="center-m")
    rows.append(band("paper", b2, "E25 light paper · system shot left (jacket over pant, standing) + two-voice headline, subheadline, body and four live-text feature labels right (client&rsquo;s reference: full system shot with feature callouts)"))
    # Round 6 (owner: "imagem colado na borda e um PUTA buraco entre"): the products are no longer cut by the
    # email edge and the empty rows are gone. A staggered pair (ref4 3L Rain Shell mosaic, ref3 product pair):
    # jacket top-left with its E27 box beside it, pant lower right with its box beside it, the two image cells
    # spanning two rows each (rowspan), so the pant starts while the jacket is still on screen. Stacks on mobile
    # in copy order: jacket, box, pant, box. Above it the people strip, now ripped at the bottom (no melt).
    stagger = f"""
                <tr>
                  <td style="padding:0;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="table-layout:fixed; width:100%;">
                      <tr>
                        <td width="320" rowspan="2" class="stack st-img" valign="top" style="width:320px; padding:0; vertical-align:top; font-size:0; line-height:0;">
                          {bimg("n3-p-jacket", 320, 400, "Habit Men&rsquo;s Buck Hollow 2.0 Jacket in Realtree APX", cls="pk st-jk", style=" margin:0;", href=J["url"])}
                        </td>
                        <td width="280" height="290" class="stack st-box st-box1" valign="middle" style="width:250px; height:290px; padding:0 22px 0 8px; vertical-align:middle;">
                          {info_box(J, width=250)}
                        </td>
                      </tr>
                      <tr>
                        <td width="280" rowspan="2" class="stack st-img" valign="bottom" style="width:280px; padding:0; vertical-align:bottom; font-size:0; line-height:0;">
                          {bimg("n3-p-pant", 280, 470, "Habit Men&rsquo;s Buck Hollow 2.0 Pant in Realtree APX", cls="pk st-pt", style=" margin:0;", href=PT["url"])}
                        </td>
                      </tr>
                      <tr>
                        <td width="320" height="360" class="stack st-box st-box2" valign="middle" style="width:256px; height:360px; padding:0 14px 0 50px; vertical-align:middle;">
                          {info_box(PT, width=250)}
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>"""
    b3 = row(bimg("n3-strip", 600, 300, "Three hunters in Habit camo walking up a field at sunrise", cls="photo fluid", href="{{BUCK_HOLLOW_URL}}", dm=True),
             pad="0", cls="", extra=" font-size:0; line-height:0;") + stagger + row("", pad="0 0 40px 0", cls="")
    rows.append(band("patriotflat", b3, "E25 flat Patriot (round 6: was the water texture; flat keeps the baked product cells seamless on mobile, where a texture rescales) · full-bleed people strip under the torn light paper, ripped at the bottom (orig-hunt22); then a staggered pair (ref4): jacket top-left + E27 box, pant lower right + E27 box, products inside the margins, image cells spanning two rows"))
    rows.append(edge("patriotflat", "footer", "3"))
    rows.append(footer())
    meta = {
        "Habit Outdoors": "November 2026 Broadcasts · 03 Buck Hollow 2.0 Jacket & Pant (send Thu Nov 19) · built 2026-10-08 (round 6)",
        "Subject": "Buck Hollow 2.0 Is Here \U0001F98C",
        "Preheader": "Waterproof, quiet, and built as a set",
        "Modules": "E24 full-bleed photo hero, round 6 (orig-hunt40 edge to edge, soft darkening in the top-left text corner, logo, kicker on a dark torn label, headline BUCK / HOLLOW 2.0, subheadline, button; torn edge into the paper baked in; own mobile crop) / E25 light paper: system shot + headline, subheadline, body, four feature labels / E25 flat Patriot: people strip ripped at the bottom, staggered pair (jacket + E27 box, pant + E27 box, rowspan mosaic) / E18 / E13 + E14",
        "Button": "#FF6400 / #FFFFFF",
        "Reference": "ref1 Duck Camp New Terrain Guard + ref6 Brush Overalls (full photo hero, title over the photo) + ref4 3L Rain Shell and ref3 Deck System (staggered product/photo mosaic, product pair) + the client's Meta reference (full system shot with feature callouts). Structure only.",
        "Bands": "preheader, hero, system + products (structure), footer = 4",
        "Source": "copy-source.md Email 3 (verbatim), products.json (store prices 2026-10-07), brief.md",
        "Links": "product URLs exactly as in the copy; {{BUCK_HOLLOW_URL}} has no URL in the copy ([[CONFIRMAR]] in brief.md)",
    }
    extra = """      .hero3 { background-image: url('assets/n3-hero-m.jpg') !important; }
      .h3-px { padding-left: 24px !important; padding-right: 24px !important; }
      .h3-logo { padding-top: 28px !important; }
      .h3-tag { padding-top: 26px !important; }
      .tag-body-n3 { height: 38px !important; padding: 0 14px 0 24px !important; }
      .tag-end-n3 { height: 38px !important; width: 10px !important; }
      .tag-endc-n3 { width: 10px !important; }
      .k3 { font-size: 17px !important; line-height: 20px !important; }
      .h3-h1 { padding-top: 16px !important; }
      .h3k { font-size: 50px !important; line-height: 50px !important; letter-spacing: 0.5px !important; }
      .h3-sub { padding-top: 12px !important; }
      .h3-btn { padding-top: 18px !important; }
      .h3-bottom { height: 412px !important; }
      .st-img { text-align: center !important; }
      .st-img img { margin: 0 auto !important; }
      .st-jk { width: 320px !important; height: auto !important; }
      .st-pt { width: 230px !important; height: auto !important; }
      .st-box { height: auto !important; padding: 8px 24px 28px 24px !important; }
      .clabel { font-size: 13px !important; }"""
    post = """
    @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .hero3 { background-image: url('assets/n3-hero-dm.jpg') !important; } }
    :root[data-theme="dark"] .hero3 { background-image: url('assets/n3-hero-dm.jpg') !important; }
    [data-ogsb] .hero3 { background-image: url('assets/n3-hero-dm.jpg') !important; }
    @media screen and (max-width: 620px) and (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .hero3 { background-image: url('assets/n3-hero-m-dm.jpg') !important; } }
    @media screen and (max-width: 620px) { :root[data-theme="dark"] .hero3 { background-image: url('assets/n3-hero-m-dm.jpg') !important; } [data-ogsb] .hero3 { background-image: url('assets/n3-hero-m-dm.jpg') !important; } }
"""
    return page(meta, rows, extra, post)


# ================================================================ 04 Heavyweight Flannel

def email_04():
    FL = P("Men's Heavyweight Soft Flannel", "", "https://www.habitoutdoors.com/products/mens-heavyweight-soft-flannel?variant=52630375956762", "Shop Now", "34.99")
    rows = []
    hero = logo(False) + row(headline([("k", "FLANNEL", "k-xl"), ("s", "THAT GOES EVERYWHERE")], tag="h1", sans_color=TAP, key_color=TAP, dm=True), pad="28px 40px 0 40px") \
        + row(img(A + "n4-hero-photo.jpg", 500, 384, "Man in a green plaid Habit flannel carrying a feed bag out of a red barn", cls="photo fluid", href="{{FLANNEL_URL}}"), pad="12px 50px 0 50px") \
        + row(sub("HEAVYWEIGHT COMFORT FOR ANY PLAN YOU&rsquo;VE&nbsp;GOT", color=MUTED_L, dm=True, maxw=440), pad="30px 40px 0 40px") \
        + row(button("Shop Flannel", "{{FLANNEL_URL}}", 300), pad="6px 40px 52px 40px")
    rows.append(band("camo", hero, "Hero on camo paper · serif-first headline, framed lifestyle photo, subheadline, button (ref6 single-product story)"))
    rows.append(edge("camo", "halftone", "4"))
    mosaic = f"""
                <tr>
                  <td align="center" class="mos-wrap" style="padding:8px 62px 0 62px;">
                    <table role="presentation" width="476" cellpadding="0" cellspacing="0" border="0" class="mos" align="center" style="width:476px;">
                      <tr>
                        <td width="320" class="stack mos-l" valign="top" style="width:320px; padding:0; font-size:0; line-height:0; vertical-align:top;">
                          {img(A + "n4-m-stable.jpg", 320, 300, "Man in a brown plaid flannel in a horse stable", cls="photo fluid", style=" border-radius:4px;")}
                        </td>
                        <td width="12" class="desk-only" style="width:12px; font-size:0; line-height:0;">&nbsp;</td>
                        <td width="144" class="stack mos-r" valign="top" style="width:144px; padding:0; font-size:0; line-height:0; vertical-align:top;">
                          {img(A + "n4-m-pleat.jpg", 144, 144, "Back of the Habit Heavyweight Soft Flannel in Rifle Green, yoke and back pleat", cls="photo mos-sq", style=" border-radius:4px;")}
                          <div class="desk-only" style="height:12px; line-height:12px; font-size:0;">&nbsp;</div>
                          {img(A + "n4-m-pocket.jpg", 144, 144, "Chest patch pocket of the Habit Heavyweight Soft Flannel in Rifle Green", cls="photo mos-sq", style=" border-radius:4px;")}
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>"""
    b2 = row(headline([("k", "WARM", "k"), ("s", "WITHOUT GETTING IN THE&nbsp;WAY")], key_color=ORANGE), pad="44px 40px 0 40px") \
        + row(sub("RAIN-FACTOR TECH MEETS SOFT&nbsp;TRICOT"), pad="0 40px") \
        + row(body(nb("Soft brushed heavyweight cotton with a back pleat for mobility and dual chest patch pockets. Wear it over a tee or under your jacket when the cold calls for more."), maxw=470, margin="0 auto 30px auto"), pad="0 40px") \
        + mosaic + row("", pad="0 0 56px 0", cls="")
    rows.append(band("halftone", b2, "E25 on Major Brown halftone · serif-first headline, subheadline, body, detail mosaic (lifestyle + back pleat + chest pocket, fabric-only tiles)"))
    # Round 4: the two colours big and overlapping on one ground line, the green collar crossing the torn edge
    # into the halftone band (the image opens the Tap Shoe cell and carries the torn edge; full width, so it
    # scales with the band on mobile); availability line, E27 box and button under it.
    b3 = row(bimg("n4-pair", 600, 440, "Habit Men&rsquo;s Heavyweight Soft Flannel in Basecamp Plaid Rifle Green, in front, and Basecamp Plaid Major Brown",
                  cls="pk fluid", href=FL["url"]), pad="0", cls="", extra=" font-size:0; line-height:0;") \
        + row(body(nb("Available in Basecamp Plaid Rifle Green and Basecamp Plaid Major Brown"), maxw=420, margin="0 auto 22px auto"), pad="10px 40px 0 40px") \
        + row(info_box(FL, width=300, with_desc=False, with_btn=False, pad="22px 18px 22px 18px"), pad="0 40px 28px 40px") \
        + row(button("Shop Now", FL["url"], 300), pad="0 40px 56px 40px")
    rows.append(band("patriot", b3, "E25 on Patriot water (round 5: was Tap Shoe paper, same colour as the footer) · the two colours, big, overlapping on one ground line, crossing the torn edge into the halftone band; availability line, E27 box, button (last call)"))
    rows.append(edge("patriot", "footer", "4"))
    rows.append(footer())
    meta = {
        "Habit Outdoors": "November 2026 Broadcasts · 04 Heavyweight Flannel (send Fri Nov 27) · built 2026-10-07",
        "Subject": "The Flannel You'll Live In \U0001F525",
        "Preheader": "Heavyweight comfort for inside and out",
        "Modules": "Hero on tex-paper-camo (logo, serif-first headline, framed lifestyle photo, subheadline, button) / E18 / E25 on tex-halftone-brown (headline, subheadline, body, photo mosaic) / E25 on tex-grain-patriot-water (colour pair crossing the torn edge, availability line, E27 box, button) / E18 / E13 + E14",
        "Button": "#FF6400 / #FFFFFF",
        "Reference": "ref6 Duck Camp Brush Overalls + ref7 Brush Field Apron (single-product story: title over a lifestyle photo, product beside its details, photo mosaic). Structure only.",
        "Bands": "preheader, hero, flannel story (structure), colours + box + button (last call), footer = 5",
        "Source": "copy-source.md Email 4 (verbatim, including the subheadline 'Rain-Factor tech meets soft tricot'), products.json (store price 2026-10-07), brief.md",
        "Links": "Block 2 URL exactly as in the copy (Rifle Green variant); {{FLANNEL_URL}} for the hero CTA, no URL in the copy ([[CONFIRMAR]] in brief.md)",
    }
    extra = """      .mos-wrap { padding: 8px 24px 0 24px !important; }
      .mos { width: 100% !important; }
      .mos-l img { width: 100% !important; height: auto !important; margin: 0 0 8px 0 !important; }
      .mos-r { text-align: center !important; font-size: 0 !important; }
      .mos-sq { display: inline-block !important; width: 48.75% !important; height: auto !important; margin: 0 !important; }
      .mos-sq + .mos-sq { margin-left: 2.5% !important; }"""
    return page(meta, rows, extra)


# ================================================================ 05 Gift Guide #2

def email_05():
    T = {
        "under30": ("$30", [
            P("Men's Breaking Dawn Camp", "The easy camp layer for cool mornings and fire-lit nights.",
              "https://www.habitoutdoors.com/products/mens-breaking-dawn-camp-short-sleeve-fishing-shirt?variant=52257642447130", "Shop Now", "29.99"),
            P("Men's Siesta Cape Long Sleeve Performance Tee", "Lightweight performance for warm days on the water or the trail.",
              "https://www.habitoutdoors.com/products/mens-siesta-cape-long-sleeve-performance-tee-1?variant=40597362475059", "Shop Now", "29.99"),
            P("Men's Outdoor Hybrid Hoodie", "Part hoodie, part performance top. Versatile enough for anything outside.",
              "https://www.habitoutdoors.com/products/mens-outdoor-hybrid-hoodie?variant=47786979295514", "Shop Now", "49.99"),
            P("All-Purpose Camo Leather Gloves", "Durable leather palms built for the field, the truck, and everything between.",
              "https://www.habitoutdoors.com/collections/outdoor/products/all-purpose-camo-leather-gloves?variant=47156168098074", "Shop Now", "19.99"),
        ], ["Lagoon Leaves Blue", "Mossy Oak Bottomland", "Goblin Blue Heather", "Green Camo"]),
        "under100": ("$100", [
            P("Men's 3 Season Bomber Jacket", "Rain-Factor and stain resistant in a bomber cut that works three seasons straight.",
              "https://www.habitoutdoors.com/collections/mens/products/mens-3-season-bomber-jacket?variant=45557982757146", "Shop Bomber", "74.99"),
            P("Men's Heavy Weight Full Zip Hoodie", "Heavyweight cotton-poly with stretch and handwarmer pockets. The cold weather go-to.",
              "https://www.habitoutdoors.com/collections/outdoor-apparel/products/mens-heavy-weight-full-zip-hoodie?variant=45636943249690", "Shop Hoodie", "44.99"),
            P("Men's Sherpa Lined Canvas Jacket", "Canvas shell with a sherpa-lined interior. Tough outside, warm inside.",
              "https://www.habitoutdoors.com/collections/mens/products/mens-sherpa-lined-canvas-jacket?variant=45637255463194", "Shop Jacket", "89.99"),
            P("Men's Angler's Bluff Rain Bib", "Waterproof rain protection for long days on the water. Pack it and go.",
              "https://www.habitoutdoors.com/collections/mens/products/men-s-angler-s-bluff-rain-bib?variant=39898163445811", "Shop Rain Bib", "99.99"),
        ], ["Major Brown", "Major Brown", "Major Brown", "Dark Gray Waves"]),
        "under120": ("$120", [
            P("Men's Shadow Series Angler's Bluff Rain Bib", "Shadow Series waterproofing with full-leg coverage for the worst weather on the water.",
              "https://www.habitoutdoors.com/collections/mens/products/mens-shadow-series-anglers-bluff-rain-bib?variant=47791648899354", "Shop Now", "119.99"),
            P("Men's Shadow Series Angler's Bluff Rain Jacket", "The matching top half. Full waterproof protection in the Shadow Series build.",
              "https://www.habitoutdoors.com/collections/mens/products/mens-shadow-series-anglers-bluff-rain-jacket?variant=47791547908378", "Shop Jacket", "119.99"),
            P("Men's Waterproof Insulated Bib", "Insulated and waterproof for the coldest seats of the season. The top-shelf gift.",
              "https://www.habitoutdoors.com/collections/mens/products/men-s-waterproof-insulated-bib?variant=45471466946842", "Shop Bib", "111.98"),
        ], ["Black / Asphalt", "Black / Asphalt", "Mossy Oak Terra Coyote"]),
    }
    rows = []
    hero = logo(True, pad="32px 40px 0 40px") + f"""
                <tr><td class="h5-space" height="405" style="height:405px; font-size:0; line-height:0;">&nbsp;</td></tr>""" \
        + row(headline([("s", "GIFTS BY"), ("k", "BUDGET,", "k-xl"), ("s", "NO GUESSWORK")], tag="h1", key_color=ORANGE), pad="0 40px") \
        + row(sub("THREE TIERS TO FIT ANY GIFT&nbsp;LIST", maxw=420), pad="0 40px") \
        + row(button("Shop Flannel", "{{CTA_URL}}", 300), pad="6px 40px 0 40px") \
        + f"""
                <tr><td class="h5-bottom" height="94" style="height:94px; font-size:0; line-height:0;">&nbsp;</td></tr>"""
    rows.append(f"""
          <!-- MODULE:E24B Full-Bleed Photo Hero, text below, round 6 (n5-hero.jpg 600x840: two men laughing in a UTV as a torn print on the Tap Shoe paper, ripped at the bottom, no fade; the paper tears into the Major Brown grain; mobile swaps to n5-hero-m.jpg 375x719, the print ripped top and bottom under the logo, via the .hero5 media rule); fallback #2A2B2D -->
          <tr>
            <td align="center" valign="top" class="hero5" data-safe-top="400" data-safe-top-m="370" background="{A}n5-hero.jpg" bgcolor="#2A2B2D" style="mso-padding-alt:0px; padding:0; background-color:#2A2B2D; background-image:url('{A}n5-hero.jpg'); background-size:cover; background-position:center bottom; background-repeat:no-repeat; vertical-align:top;">
              <!--[if gte mso 9]><v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px;height:840px;"><v:fill type="frame" src="{A}n5-hero.jpg" color="#2A2B2D" /><v:textbox style="mso-fit-shape-to-text:true;" inset="0,0,0,0"><div><![endif]-->
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{hero}
              </table>
              <!--[if gte mso 9]></div></v:textbox></v:rect><![endif]-->
            </td>
          </tr>
          <!-- /MODULE:E24B -->
""")

    def alt(p, variant):
        return "Habit " + esc(p["name"]) + " in " + esc(variant)

    def title_p(p, px=19, align="center", cls=""):
        u = p["url"]
        return (f'<p class="ititle{cls}" style="margin:0; font-family:{F_SANS}; font-size:{px}px; line-height:{px + 3}px; mso-line-height-rule:exactly; '
                f'font-weight:800; letter-spacing:1.2px; color:{ORANGE}; text-align:{align};"><a href="{u}" target="_blank" style="color:{ORANGE}; text-decoration:none;">{nb(up(p["name"]))}</a></p>')

    def desc_p(p, align="center", margin="0"):
        return (f'<p class="idesc" style="margin:{margin}; font-family:{F_SANS}; font-size:15px; line-height:21px; mso-line-height-rule:exactly; '
                f'font-weight:500; color:{WHITE}; text-align:{align};">{nb(p["desc"])}</p>')

    def price_p(p, align="center", margin="0 0 14px 0"):
        u = p["url"]
        return (f'<p class="iprice" style="margin:{margin}; font-family:{F_SANS}; font-size:20px; line-height:24px; mso-line-height-rule:exactly; '
                f'font-weight:800; color:{WHITE}; text-align:{align};"><a href="{u}" target="_blank" style="color:{WHITE}; text-decoration:none;">{price(p["price"])}</a></p>')

    # ---- UNDER $30 (grain brown): a centred torn label, then an open 2x2 grid of the four stocking-stuffer picks,
    # big cut-outs standing on the grain (no frame, no panel: unlike the 02 cards), centred text under each,
    # title / line in fixed-height cells so prices and buttons line up (R3). Mobile: one column, copy order.
    amount, items, variants = T["under30"]

    def gcell(i):
        p = items[i]
        return f"""<td width="300" class="stack g5" valign="top" style="width:300px; padding:0; vertical-align:top;">
                          {bimg(f"n5-g-{i + 1}", 300, 270, alt(p, variants[i]), cls="pk g5-img", style=" margin:0;", href=p["url"])}
                          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr><td class="g5-t" height="72" valign="top" style="height:72px; padding:4px 26px 0 26px; vertical-align:top; text-align:center;">{title_p(p)}</td></tr>
                            <tr><td class="g5-d" height="88" valign="top" style="height:88px; padding:0 26px; vertical-align:top; text-align:center;">{desc_p(p)}</td></tr>
                            <tr><td valign="bottom" style="padding:4px 26px 34px 26px; vertical-align:bottom; text-align:center;">{price_p(p)}{small_button(p["cta"], p["url"])}</td></tr>
                          </table>
                        </td>"""

    grid = ""
    for r in range(2):
        grid += f"""
                <tr>
                  <td style="padding:0;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="table-layout:fixed; width:100%;">
                      <tr>
                        {gcell(2 * r)}
                        {gcell(2 * r + 1)}
                      </tr>
                    </table>
                  </td>
                </tr>"""
    t30 = row(tier_tag(amount, "center"), pad="46px 0 6px 0", cls="", align="center") + grid + row("", pad="0 0 8px 0", cls="")
    rows.append(band("brown", t30, "Tier UNDER $30 on Major Brown grain, round 6 · centred torn price label (E33 label device) + open 2x2 grid: four big cut-outs on the grain, title, client line, price, CTA under each (ref5 grouped picks)"))

    # ---- UNDER $100 (flat Tap Shoe): ONE lead product big (the bomber, rising over the torn edge into the
    # $30 band, ref1 big product per band), the torn label anchored on the right edge beside it; then the other
    # three GROUPED in one picture on one ground line (ref5), left to right in list order, and a short price
    # list under it (title + line | price + button), thin rules between (ref6 underlined list).
    amount, items, variants = T["under100"]
    lead = items[0]
    ltext = (tier_tag(amount, "right")
             + f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="lead-txt" style="padding:26px 36px 0 10px; text-align:left;">"""
             + title_p(lead, 19, "left", "") + desc_p(lead, "left", "8px 0 10px 0") + price_p(lead, "left", "0 0 16px 0")
             + small_button(lead["cta"], lead["url"], align="left") + "</td></tr></table>")
    t100 = frow("n5-lead", 300, 470, alt(lead, variants[0]), lead["url"], ltext, side="left", rise=True, hu=56,
                tpad="10px 0 0 0", valign="top", tcls="t-under100 lead5")
    group_alt = ("Habit Men&rsquo;s Heavy Weight Full Zip Hoodie in Major Brown, Men&rsquo;s Sherpa Lined Canvas Jacket in Major Brown "
                 "and Men&rsquo;s Angler&rsquo;s Bluff Rain Bib in Dark Gray Waves, side by side")
    t100 += row(bimg("n5-group", 600, 380, group_alt, cls="pk fluid", style=" margin:0;"), pad="0", cls="", extra=" font-size:0; line-height:0;")
    plist = ""
    for i, p in enumerate(items[1:], 1):
        plist += f"""
                <tr>
                  <td class="pl-wrap" style="padding:0 40px;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid #FEF4C6; border-top-color:rgba(254,244,198,0.35);">
                      <tr>
                        <td class="stack pl-t" valign="middle" style="padding:20px 18px 20px 0; vertical-align:middle; text-align:left;">
                          {title_p(p, 17, "left", " pl-title")}
                          {desc_p(p, "left", "6px 0 0 0")}
                        </td>
                        <td width="168" class="stack pl-b" valign="middle" style="width:168px; padding:20px 0; vertical-align:middle; text-align:right;">
                          {price_p(p, "right", "0 0 10px 0")}
                          <table role="presentation" cellpadding="0" cellspacing="0" border="0" align="right" class="pl-btn" style="margin:0;"><tr><td>{small_button(p["cta"], p["url"], align="left")}</td></tr></table>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>"""
    t100 += plist + row("", pad="0 0 40px 0", cls="")
    rows.append(band("tapflat", t100, "Tier UNDER $100 on flat Tap Shoe, round 6 · lead product big, rising over the torn edge into the $30 band, torn price label on the right edge + text; the other three grouped in one picture (ref5) over a short price list with rules (ref6)"))

    # ---- UNDER $120 (flat Patriot): centred torn label; the Shadow Series bib and jacket shown TOGETHER as a set
    # (ref3 product pair; the client calls the jacket "The matching top half") with their two boxes side by side
    # (E27 frame on the cell, equal height); then the Waterproof Insulated Bib ("The top-shelf gift") as its own
    # highlight: text left, the bib tall on the right.
    amount, items, variants = T["under120"]
    set_alt = "Habit Men&rsquo;s Shadow Series Angler&rsquo;s Bluff Rain Bib and Rain Jacket in Black / Asphalt, shown together as a set"

    def sbox(p):
        u = p["url"]
        return f"""<td width="258" class="stack sbox" valign="top" style="width:256px; padding:0; vertical-align:top; border:1px solid #FEF4C6; border-color:rgba(254,244,198,0.7); border-radius:10px;">
                          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr><td class="sb-t" height="72" valign="top" style="height:72px; padding:24px 18px 0 18px; vertical-align:top; text-align:center;">{title_p(p, 17)}</td></tr>
                            <tr><td class="sb-d" height="92" valign="top" style="height:92px; padding:8px 18px 0 18px; vertical-align:top; text-align:center;">{desc_p(p)}</td></tr>
                            <tr><td valign="bottom" style="padding:6px 18px 24px 18px; vertical-align:bottom; text-align:center;">{price_p(p)}{small_button(p["cta"], u)}</td></tr>
                          </table>
                        </td>"""

    t120 = row(tier_tag(amount, "center"), pad="44px 0 0 0", cls="", align="center") \
        + row(bimg("n5-set", 600, 430, set_alt, cls="pk fluid", style=" margin:0;"), pad="8px 0 0 0", cls="", extra=" font-size:0; line-height:0;") \
        + f"""
                <tr>
                  <td class="set-wrap" style="padding:0 34px 12px 34px;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate; table-layout:fixed;">
                      <tr>
                        {sbox(items[0])}
                        <td width="16" class="desk-only" style="width:16px; font-size:0; line-height:0;">&nbsp;</td>
                        {sbox(items[1])}
                      </tr>
                    </table>
                  </td>
                </tr>"""
    top = items[2]
    ttext = title_p(top, 19, "left") + desc_p(top, "left", "8px 0 10px 0") + price_p(top, "left", "0 0 16px 0") + small_button(top["cta"], top["url"], align="left")
    t120 += frow("n5-top", 300, 460, alt(top, variants[2]), top["url"], ttext, side="right", mob="cen", tpad="0 10px 0 40px", tcls="center-m t-under120") \
        + row("", pad="0 0 36px 0", cls="")
    rows.append(band("patriotflat", t120, "Tier UNDER $120 on flat Patriot, round 6 · centred torn price label; the matching bib and jacket together as a set (ref3 pair) with two framed boxes side by side; the top-shelf bib as its own highlight (text left, bib right)"))
    rows.append(edge("patriotflat", "camo", "5"))
    gcu = "https://www.habitoutdoors.com/products/gift-card"
    oaks_alt = "Hunter in Habit camo checking his gear among autumn oaks"
    oaks = (img(A + "n5-closing-oaks.jpg", 600, 310, oaks_alt, cls="photo fluid img-light", style=" margin:0;", href=gcu) + '<!--[if !mso]><!-->'
            + img(A + "n5-closing-oaks-dm.jpg", 600, 310, oaks_alt, cls="photo fluid img-dark", style=" display:none; max-height:0; overflow:hidden; mso-hide:all; margin:0;", href=gcu) + '<!--<![endif]-->')
    b5 = row(oaks, pad="0", cls="", extra=" font-size:0; line-height:0;") \
        + row(headline([("k", "STILL", "k"), ("s", "NOT SURE WHAT TO GET?")], sans_color=TAP, key_color=TAP, dm=True), pad="28px 40px 0 40px") \
        + row(body(nb("A Habit Outdoors gift card lets them pick the gear that fits their season, from fishing shirts to insulated bibs. Available in any amount and delivered straight to their inbox."), color=TAP, dm=True, maxw=470), pad="0 40px") \
        + row(button("Shop Gift Cards", gcu, 300), pad="0 40px 56px 40px")
    rows.append(band("camo", b5, "E26 Torn Photo + E25 on camo paper · torn lifestyle photo opening the cell, serif-first headline, body, button (angle shift)"))
    rows.append(edge("camo", "footer", "5"))
    rows.append(footer())
    meta = {
        "Habit Outdoors": "November 2026 Broadcasts · 05 Gift Guide #2, gifts by price (send Mon Nov 30) · built 2026-10-08 (round 6) · copy marked Needs Edit by the client",
        "Subject": "Gifts at Every Price Point \U0001F381",
        "Preheader": "Gifts under $30, $100, and $120",
        "Modules": "E24B photo hero, text below (torn print on Tap Shoe paper, no fade; own mobile crop) / gifts by price, one structure band in three tiers, each with its own layout under a torn price label (E33 device): UNDER $30 on grain brown = open 2x2 grid of big cut-outs; UNDER $100 on flat Tap Shoe = lead product rising over the torn edge + grouped picture of the other three over a ruled price list; UNDER $120 on flat Patriot = the matching bib and jacket as a set with two framed boxes + the top-shelf bib as a highlight / E18 / E26 + E25 camo paper (torn lifestyle photo, headline, body, button) / E18 / E13 + E14",
        "Button": "#FF6400 / #FFFFFF",
        "Reference": "ref1 New Terrain Guard (one big product crossing the torn edge), ref3 Deck System (product pair), ref5 Pheasants Forever (grouped products), ref6 Brush Overalls (product beside a ruled list), and the kit's E33 label for the tier headers. Structure only.",
        "Bands": "preheader, hero, gifts by price (one structure band in three tiers), gift card (angle shift), footer = 5",
        "Source": "copy-source.md Email 5 (verbatim, including the hero CTA 'Shop Flannel' and the Hybrid Hoodie under UNDER $30), products.json (store prices 2026-10-07), brief.md",
        "Links": "product and gift card URLs exactly as in the copy; {{CTA_URL}} for the hero CTA, no URL in the copy ([[CONFIRMAR]] in brief.md)",
    }
    extra = """      .hero5 { background-image: url('assets/n5-hero-m.jpg') !important; }
      .h5-space { height: 330px !important; }
      .h5-bottom { height: 97px !important; }
""" + TAG_CSS_05 + """
      .g5 { padding: 0 0 8px 0 !important; }
      .g5-img { width: 300px !important; height: auto !important; margin: 0 auto !important; }
      .g5-t, .g5-d { height: auto !important; padding-left: 24px !important; padding-right: 24px !important; }
      .g5-d { padding-bottom: 12px !important; }
      .lead5 { padding: 24px 0 8px 0 !important; }
      .lead-txt { padding: 22px 24px 0 24px !important; }
      .pl-wrap { padding: 0 24px !important; }
      .pl-t { padding: 20px 0 10px 0 !important; }
      .pl-b { padding: 0 0 22px 0 !important; text-align: left !important; }
      .pl-b p { text-align: left !important; }
      .pl-btn { float: none !important; margin: 0 !important; }
      .pl-title { font-size: 17px !important; }
      .set-wrap { padding: 0 24px 4px 24px !important; }
      .sbox { margin: 0 0 16px 0 !important; border-radius: 10px !important; }
      .sb-t, .sb-d { height: auto !important; }
      .t-under120 .ititle { font-size: 17px !important; line-height: 21px !important; }"""
    return page(meta, rows, extra)


FILES = {
    "01-womens-cedar-branch.html": email_01,
    "02-gift-guide-1.html": email_02,
    "03-buck-hollow-2.html": email_03,
    "04-heavyweight-flannel.html": email_04,
    "05-gift-guide-2.html": email_05,
}

if __name__ == "__main__":
    for name, fn in FILES.items():
        s = fn()
        (HERE / name).write_text(s, encoding="utf-8")
        print(f"{name:32s} {len(s.encode('utf-8')) / 1024:6.1f} KB")
