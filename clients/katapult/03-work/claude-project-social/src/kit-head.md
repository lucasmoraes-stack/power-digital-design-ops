# Katapult studio kit: the post file and every layout

Every Katapult frame is built **only** from the layouts below. The layouts live inside Katapult Social Studio, exact to the approved Figma files: positions, sizes, colours, logo, pill, legal line. A post file names a layout and fills its **slots**. Nothing else can change, so nothing else can go wrong.

See every layout rendered: Katapult Social Studio, Layouts tab, https://claude.ai/code/artifact/5a137796-2f13-4690-8ce2-45fd9f4c8cdc

## 1. Slots

| Slot | What it holds | How to write it |
|---|---|---|
| `headline` | the headline | text; `<br>` between lines. Banner patterns use their spans (section 5) |
| `sub` | the subhead | text; `<br>` between lines when the layout breaks it |
| `cta` | the button label | text |
| `photo` | a Library photo | `data-img="library:ID"`, optional `data-pos="X% Y%"` |
| `product1` to `product3` | product cutouts | `data-img="product:ID"`, optional `data-scale` (0.4 to 1) and `data-pos` |
| `phone` | T03's hand and phone | leave it out to keep the approved mockup; `upload:FILE` only for a client-supplied replacement |

- **Every slot listed for a layout must be filled.** A missing slot shows the template's sample copy or photo, and the Studio flags it.
- **Line breaks:** each layout below lists its sample, how many lines it was approved with, its type size, and its longest sample line in characters. Break on meaning: "Time for the home / upgrade you want.", never "Time for / the home upgrade / you want."
- **Fitting copy that is longer than the sample** (in this order):
  1. Rebreak. A line can hold about as many characters as the longest sample line at the same size. Tall sizes (960x1200, 300x600, 160x600, 4x5, 9x16) can take one or two more lines than the sample. In P2 the bars grow upward from the CTA, so extra bars are safe on every size.
  2. Then `data-size="N"` (px) on the slot. It scales the whole slot together (every line, every bar, the bar padding). Never under 70% of the size listed.
  3. Still too long: client copy is never cut. Say which sizes will not fit and propose the next pattern or template that does; it is an open item.
- **You cannot measure text.** Estimate with the character counts, then the Studio measures: it flags a wrapped line, text off the frame and any overlap. Tell the person which frames are tight so they check those first.
- **`data-pos="X% Y%"`** sets which point of the photo stays in view: the point at X% across and Y% down the photo lands at the same X% and Y% of the box. When you leave it out, the Studio uses the face position listed in `03-image-library.md`, which keeps the face in frame. To show more of the top of a photo (move it down in the box), lower Y; to keep a face clear of bars at the bottom, keep Y at or below the face's own Y.
- **`data-scale`** shrinks a product inside its box so a set reads at true relative scale (a fridge bigger than headphones). 1 fills the box.
- **Images:** `library:ID` and `product:ID` from `03-image-library.md`, or `upload:FILE.png` for an image the person drops in the Studio with the file (a client photo, a new cutout). Nothing else.
- **T09** marks its pink words with `<em>`: `Your next upgrade <em>awaits.</em>`. No other template has an accent; `<em>` is ignored there.
- **T08** sets its last headline line in Pink automatically. Plan the copy so the last line is the payoff.

## 2. The post file

One file per job: every frame, every size, every iteration, in order. Start from this skeleton exactly.

```html
<!DOCTYPE html>
<!--
  Katapult post file
  Job: {KAT26023 Back to School | Organic, 2026-10-20 home upgrade}
  Frames: {count} ({layout codes})
  Copy: {client copy, verbatim | written here, approved on yyyy-mm-dd}
  Open: {every open item, or "none"}
-->
<html lang="en"><head><meta charset="utf-8"><title>{Job name}</title></head><body>

<section data-use="T06-4x5" data-file="2026-10-20-home-upgrade-4x5">
  <div data-slot="headline">Time for the home<br>upgrade you want.</div>
  <div data-slot="sub">No credit score needed. Just fair, straightforward terms.</div>
  <div data-slot="cta">Leap Forward</div>
  <div data-slot="photo" data-img="library:unboxing-woman-unboxing-sofa-02" data-pos="50% 35%"></div>
</section>

<section data-use="P3A-300x250" data-file="KAT26023-BackToSchool-300x250-Static-Programmatic-V1">
  <div data-slot="headline"><span class="t1">Back to <span class="ta">school</span></span><span class="t1">is back on.</span><span class="t2">Lease what</span><span class="t2">they need.</span></div>
  <div data-slot="cta"><span>Shop School Deals</span></div>
</section>

</body></html>
```

Rules:
- `data-use` is a layout code from section 6 exactly (`T06-4x5`, `P2-728x90`).
- `data-file` is the PNG name: banners `{JOB}-{Name}-{W}x{H}-Static-{PMAX|Programmatic}-V{n}`; organic `{yyyy-mm-dd}-{slug}-{ratio}` (carousel slides add `-s1`, `-s2`).
- Only `section` and `div data-slot` elements. No `<style>`, no classes except the banner spans in section 5, no scripts, no images other than through `data-img`.

## 3. Choosing a social template

Pick by the imagery you have, then by the message. Ratios: `1x1` (1200x1200 feed and PMAX square), `4x5` (1080x1350 feed), `16x9` (1920x1080), `9x16` (1080x1920 Stories and Reels: the layouts already keep copy inside the safe band).

| Code | Layout | Use it for | Imagery |
|---|---|---|---|
| T01 | Full image | A strong lifestyle photo with a calm lower third | Library photo, full bleed |
| T02 | Split panel, image | A three-beat headline and a tall photo crop | Library photo, half frame |
| T03 | Split, phone in hand | App and how-it-works messages | The approved hand and phone |
| T04 | Product row, 3-up | Category or gear messages with several products | Three product cutouts |
| T05 | Hero product, bleed | One hero product, warm conversational headline (Cream) | One product cutout |
| T06 | Top block, photo card | Home and lifestyle messages, photo as proof (Pink) | Library photo in a rounded card |
| T07 | Top block, product on circle | One product launch or tech message (Pink) | One product cutout |
| T08 | Typographic statement | Brand or manifesto messages | None |
| T09 | Hero photo, full width | Big photo, short headline, last words in Pink | Library photo, bottom half |
| T10 | Product trio, circles | Roundups with exactly three products | Three product cutouts |

Carousels: one template per slide, all slides in one file, same ratio. Open with a strong cover (T08 or T01), alternate grounds slide to slide (never two neighbours on the same ground colour), close with a CTA slide.

## 4. Choosing a banner pattern

All four come in the eight sizes every Katapult banner job ships: PMAX `1200x1200`, `1200x628`, `960x1200`; programmatic `300x600`, `300x250`, `160x600`, `728x90`, `320x50`. See `06-katapult-patterns.md` for when each fits.

| Code | Pattern | Slots |
|---|---|---|
| P1 | Knolling flat-lay (salmon paper ground, 11 products at true scale, copy top left) | headline, sub, cta |
| P2 | Photo + highlight bars (full-bleed photo, setup bar Cream, punchline bar Dark Blue with Pink type, legal on PMAX) | photo, headline, cta |
| P3A | Flat brand type on Dark Blue | headline, sub, cta |
| P3B | Flat brand type on Cream | headline, sub, cta |
| P4A | Proof badge, centered (Trustpilot card, blurred review cards with stars only) | headline, sub, cta |
| P4B | Proof badge, photo seam (photo band, badge on its edge) | photo, headline, sub, cta |

Sizes without a `sub` slot drop the subhead (see the per-size list in section 6).

## 5. Banner slot markup

Banner text keeps the pattern's own spans. Copy the sample's structure and change only the words.

- **P1** headline, sub, cta: plain text, `<br>` between lines.
- **P2** headline: one `<span>` per bar (one bar per line). `class="t1"` bars carry the setup sentence (Cream bar), `class="t2"` bars the punchline (Dark Blue bar, Pink type). Most sizes have one bar each; 160x600 stacks five (`The` / `turkey's` / `fine.` / `The oven` / `isn't.`). cta: text, `<br>` to wrap on narrow sizes; keep the sample's `<span>` when it has one.
- **P3A / P3B** headline: one `<span>` per line. `class="t1"` for lines of the first sentence, `class="t2"` for the second sentence; inside a line, `<span class="ta">word</span>` marks the one accent word of each sentence. sub and cta: one `<span>` per line.
- **P4A / P4B** headline, sub, cta: one `<span>` per line.

## 6. Layout catalogue

Each entry: the code, the canvas, and each slot with its approved sample, its line count and its type size. Your copy should land on the same number of lines.

