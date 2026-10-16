"""RKU26012 motion notes for the editors: what moves in each storyboard frame, when and how.

Juan (2026-10-16, Figma comments on the storyboard): "Add specific motion notes about these elements
and how to transition them, so the editors get it right. Apply to all." He also read the blimp as a
logo with a background, so every frame where it shows gets its flight path drawn.

Timings are the ones in timeline.js (seek(t)); keep both in sync. Each note: (element ids the marker
points at, title, text). The marker is drawn only where the element is visible at the frame's time.

    python -I motion_notes.py   -> build/motion_notes.json (notes + marker boxes per size and frame, in Figma
                                   frame px: 16x9 is 2560 wide on the board, so x4/3), pasted into the Figma
                                   board by the use_figma script in the session log.
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from anim import SIZES  # noqa: E402
from storyboard_html import BEATS, load  # noqa: E402

BOARD_W = {"16x9": 2560, "1x1": 1440, "4x5": 1440, "9x16": 1440}

ALWAYS = [
    (["blimp"], "Roku blimp", "Part of the scene, not a logo lockup. Flies right to left across the top for the "
     "whole 20 s (linear), with a slow bob of 7 px and a 1.4° tilt. Never stops, never fades."),
    ([], "Background", "Roku City silhouette slides left the full 20 s (linear, very slow). Two purple glows drift with it."),
]

# frame: (span, notes)
NOTES = {
    1: ((0.0, 2.4), [
        (["ilk"], "Roku Ads Manager lockup", "Fades in and rises 40 px, 0.10 → 0.60 s, ease out."),
        (["ih0", "ih1"], "Headline", "Two lines, each fades in and rises 60 px: line 1 at 0.25 → 0.80 s, line 2 at 0.45 → 1.00 s, ease out."),
        (["chip0", "chip1", "chip2"], "Step chips", "Pop in one after the other, 0.18 s apart (1.00 / 1.18 / 1.36 s): "
         "scale 80 → 100% with a small overshoot over 0.42 s, fade in over 0.2 s."),
        ([], "Out", "The whole intro fades out and lifts 40 px, 2.05 → 2.45 s, while step 1 comes in."),
    ]),
    2: ((2.4, 3.9), [
        (["slk", "pill0", "hl0"], "Lockup, step pill, headline", "Fade in and rise 40 px, 2.40 → 2.95 s, ease out "
         "(the headline travels a bit more than the pill)."),
        (["card"], "Card", "Fades in, rises 70 px and scales 94 → 100%, 2.50 → 3.10 s, ease out."),
        (["si0", "si1", "si2"], "Stepper", "Step 1 active, progress line at one third."),
        (["cur"], "Cursor", "Enters from the bottom right at 3.0 s and glides to the budget field in a slight arc, 3.00 → 3.60 s, ease in-out."),
        (["f-budget"], "Click on the field", "3.68 s: cursor dips to 86% for 0.14 s and a white ring expands and fades (0.45 s). "
         "The field lights up (focus glow) and the caret starts blinking."),
    ]),
    3: ((3.9, 6.25), [
        (["f-budget"], "Typing", "5 → 50 → 500 → 5,000 at 3.95 / 4.10 / 4.25 / 4.40 s, one key every 0.15 s. Caret blinks after the last key."),
        (["b-next0"], "Next", "Cursor glides to Next 4.70 → 5.35 s, click at 5.45 s: the button presses in 7% and springs back in 0.26 s, ring on the click."),
        (["card"], "Transition to step 2", "5.75 → 6.25 s: the step 1 panel slides 70 px left and fades, step 2 slides in from 70 px right; "
         "the card grows taller (ease in-out)."),
        (["pill0", "hl0"], "Headline swap", "Old pill and headline lift 40 px and fade; the new ones rise 40 px from below, same 0.5 s window."),
        (["si0", "si1"], "Stepper", "Step 1 turns into a check, step 2 goes active, the progress line fills to two thirds."),
    ]),
    4: ((6.25, 8.0), [
        (["f-int"], "Interests field", "Cursor glides over 6.35 → 6.95 s, click at 7.00 s."),
        (["menu"], "Dropdown", "Opens 7.00 → 7.18 s: fades in and unfolds down from the field (scale Y 85 → 100%), the chevron turns 180°. "
         "The hover highlight follows the cursor down the list."),
        (["mo1"], "Pick", "Click on Home & Garden at 7.62 s; the menu folds up and fades 7.66 → 7.75 s and the value fills the field."),
    ]),
    5: ((8.0, 8.85), [
        (["age1"], "Age 25-34", "Cursor glides over 7.80 → 8.25 s, click at 8.32 s: the pill fills purple and pops 108 → 100% in 0.25 s."),
    ]),
    6: ((8.85, 11.05), [
        (["f-zip"], "ZIP code", "Cursor glides over 8.40 → 8.85 s, click at 8.92 s, focus glow. Typing 9 → 90 → 902 → 9021 → 90210 at "
         "9.10 / 9.23 / 9.36 / 9.49 / 9.62 s (one key every 0.13 s)."),
        (["b-next1"], "Next", "Cursor glides to Next 9.75 → 10.30 s, click at 10.38 s with the same press and ring."),
        (["card"], "Transition to step 3", "10.55 → 11.05 s: same move as step 1 → 2 (panels slide 70 px, headline and pill swap, "
         "card height eases). Step 2 turns into a check, step 3 goes active, progress line full."),
    ]),
    7: ((11.05, 13.25), [
        (["b-up"], "Upload Content", "Cursor glides over 11.10 → 11.60 s, click at 11.68 s, press and ring."),
        (["frow"], "File row", "TV_Ad.mp4 fades in and rises 16 px, 11.75 → 12.03 s."),
        (["bar"], "Progress", "Bar fills 0 → 100% from 11.80 to 13.20 s, ease in-out; the % counts up with it."),
        (["okc"], "Done check", "At 13.20 s the check pops in with a small overshoot (0.35 s)."),
    ]),
    8: ((13.25, 15.0), [
        (["b-launch"], "Launch Campaign", "Cursor glides over 13.25 → 13.80 s, click at 13.90 s: press, ring, and the button brightens 25% over 0.3 s."),
        (["card"], "Exit", "14.55 → 14.95 s: the card scales up to 105% and fades; lockup, pill, headline and cursor fade with it."),
        ([], "Flash", "White flash builds from 14.70 s to 15.00 s (up to 92%), the cut to the TV happens under it."),
    ]),
    9: ((15.0, 15.35), [
        ([], "Cut", "Hard cut under the flash at 15.00 s: the ad fills the frame. The flash fades out 15.00 → 15.40 s."),
        ([], "TV ad playing", "The ad's progress line on the TV grows from 18% to 46% (15.0 → 17.8 s) so it reads as playing."),
    ]),
    10: ((15.35, 17.4), [
        ([], "Camera pull back", "One continuous zoom out from the TV glass (full frame) to the whole living room, 15.35 → 17.50 s, "
         "ease in-out, centred on the TV. No cut."),
        ([], "Out", "The room fades into the purple end frame, 17.40 → 17.75 s."),
    ]),
    11: ((17.4, 20.0), [
        (["clk"], "Lockup", "Fades in and rises 40 px, 17.60 → 18.10 s, ease out."),
        (["chl"], "Headline", "Fades in and rises 60 px, 17.72 → 18.27 s, ease out."),
        (["ctab"], "CTA button", "Pops 80 → 100% with a small overshoot, 18.00 → 18.40 s."),
        (["cur"], "Cursor", "Enters from the bottom right at 18.05 s, reaches the button at 18.75 s, click at 18.85 s (press and ring). Hold to 20.0 s."),
    ]),
}

JS_BOX = """(ids) => {
  const s = document.getElementById('st').getBoundingClientRect();
  let b = null;
  for (const id of ids) {
    const el = document.getElementById(id); if (!el) continue;
    let v = el, ok = true;
    while (v && v.id !== 'st') { const cs = getComputedStyle(v);
      if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < .05) { ok = false; break; } v = v.parentElement; }
    if (!ok) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    const x0 = r.left - s.left, y0 = r.top - s.top, x1 = r.right - s.left, y1 = r.bottom - s.top;
    b = b ? [Math.min(b[0], x0), Math.min(b[1], y0), Math.max(b[2], x1), Math.max(b[3], y1)] : [x0, y0, x1, y1];
  }
  return b;
}"""


def main():
    out = {"always": [[a, b] for _, a, b in ALWAYS], "sizes": {}}
    with sync_playwright() as p:
        br = p.chromium.launch(channel="chrome", args=["--allow-file-access-from-files"])
        for size, S in SIZES.items():
            k = BOARD_W[size] / S["W"]
            sc = lambda b: [round(v * k) for v in b] if b else None  # noqa: E731
            pg = br.new_page(viewport={"width": S["W"], "height": S["H"]})
            frames = []
            for n, (t, beat) in enumerate(BEATS, 1):
                load(pg, size, t)
                span, notes = NOTES[n]
                rows = [{"title": ti, "text": tx, "box": sc(pg.evaluate(JS_BOX, ids)) if ids else None} for ids, ti, tx in notes]
                tv = pg.evaluate(JS_BOX, ["tv"])                 # TV shot covers the sky
                blimp = None if tv else sc(pg.evaluate(JS_BOX, ["blimp"]))
                path = None
                if blimp:                                   # where the blimp is at 0 s and 20 s, same frame
                    pg.evaluate("seek(0)"); a = pg.evaluate(JS_BOX, ["blimp"])
                    pg.evaluate("seek(20)"); b = pg.evaluate(JS_BOX, ["blimp"])
                    pg.evaluate(f"seek({t})")
                    path = {"start": sc(a), "end": sc(b)}
                frames.append({"n": n, "t": t, "beat": beat, "span": span, "notes": rows, "blimp": blimp, "path": path})
            pg.close()
            out["sizes"][size] = frames
            print(size, "ok")
        br.close()
    (HERE / "build" / "motion_notes.json").write_text(json.dumps(out, ensure_ascii=False), encoding="utf8")


if __name__ == "__main__":
    main()
