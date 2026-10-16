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

### T01 · Full image

**T01-1x1** (1200x1200)
- `headline` (wraps in its box, 112px, longest line 34 characters): `The upgrade your kitchen deserves.`
- `sub` (wraps in its box, 40px, longest line 47 characters): `No credit needed. Just fair terms and your yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1200x1200 square at x 0, y 0

**T01-4x5** (1080x1350)
- `headline` (wraps in its box, 112px, longest line 34 characters): `The upgrade your kitchen deserves.`
- `sub` (wraps in its box, 40px, longest line 47 characters): `No credit needed. Just fair terms and your yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1080x1350 portrait at x 0, y 0

**T01-16x9** (1920x1080)
- `headline` (wraps in its box, 112px, longest line 34 characters): `The upgrade your kitchen deserves.`
- `sub` (wraps in its box, 40px, longest line 47 characters): `No credit needed. Just fair terms and your yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1920x1080 landscape at x 0, y 0

**T01-9x16** (1080x1920)
- `headline` (wraps in its box, 112px, longest line 34 characters): `The upgrade your kitchen deserves.`
- `sub` (wraps in its box, 40px, longest line 47 characters): `No credit needed. Just fair terms and your yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1080x1920 portrait at x 0, y 0


### T02 · Split panel, image

**T02-1x1** (1200x1200)
- `headline` (3 lines, 143px, longest line 13 characters): `Your home.<br>Your upgrade.<br>Your move.`
- `sub` (wraps in its box, 40px, longest line 60 characters): `New couch, new laptop, new fridge. No credit score required.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 550x1200 portrait at x 650, y 0

**T02-4x5** (1080x1350)
- `headline` (3 lines, 88px, longest line 13 characters): `Your home.<br>Your upgrade.<br>Your move.`
- `sub` (wraps in its box, 40px, longest line 60 characters): `New couch, new laptop, new fridge. No credit score required.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 495x1350 portrait at x 585, y 0

**T02-16x9** (1920x1080)
- `headline` (3 lines, 146px, longest line 13 characters): `Your home.<br>Your upgrade.<br>Your move.`
- `sub` (wraps in its box, 40px, longest line 60 characters): `New couch, new laptop, new fridge. No credit score required.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 880x1080 portrait at x 1040, y 0

**T02-9x16** (1080x1920)
- `headline` (3 lines, 146px, longest line 13 characters): `Your home.<br>Your upgrade.<br>Your move.`
- `sub` (wraps in its box, 40px, longest line 60 characters): `New couch, new laptop, new fridge. No credit score required.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1080x920 landscape at x 0, y 1000


### T03 · Split, phone in hand

**T03-1x1** (1200x1200)
- `headline` (3 lines, 82px, longest line 14 characters): `Open the app<br>Find it fast<br>Make it yours.`
- `sub` (wraps in its box, 40px, longest line 56 characters): `Browse, apply, and start shopping right from your phone.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `phone`: optional, keep the approved mockup, box 663x1052 portrait at x 0, y 148

**T03-4x5** (1080x1350)
- `headline` (3 lines, 82px, longest line 14 characters): `Open the app<br>Find it fast<br>Make it yours.`
- `sub` (wraps in its box, 40px, longest line 56 characters): `Browse, apply, and start shopping right from your phone.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `phone`: optional, keep the approved mockup, box 597x1217 portrait at x 0, y 133

**T03-16x9** (1920x1080)
- `headline` (3 lines, 82px, longest line 14 characters): `Open the app<br>Find it fast<br>Make it yours.`
- `sub` (wraps in its box, 40px, longest line 56 characters): `Browse, apply, and start shopping right from your phone.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `phone`: optional, keep the approved mockup, box 873x1061 portrait at x 0, y 19

**T03-9x16** (1080x1920)
- `headline` (3 lines, 82px, longest line 14 characters): `Open the app<br>Find it fast<br>Make it yours.`
- `sub` (wraps in its box, 40px, longest line 56 characters): `Browse, apply, and start shopping right from your phone.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `phone`: optional, keep the approved mockup, box 543x1398 portrait at x 0, y 261


### T04 · Product row, 3-up

**T04-1x1** (1200x1200)
- `headline` (2 lines, 98px, longest line 20 characters): `Level up your setup<br>and never look back.`
- `sub` (wraps in its box, 40px, longest line 52 characters): `No credit required. Just the tech you actually need.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 256x267 square at x 50, y 772
- `product2`: cutout, fits inside its box, box 239x344 portrait at x 314, y 697
- `product3`: cutout, fits inside its box, box 603x404 landscape at x 569, y 637

**T04-4x5** (1080x1350)
- `headline` (2 lines, 98px, longest line 20 characters): `Level up your setup<br>and never look back.`
- `sub` (wraps in its box, 40px, longest line 52 characters): `No credit required. Just the tech you actually need.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 236x246 square at x 24, y 874
- `product2`: cutout, fits inside its box, box 220x316 portrait at x 267, y 805
- `product3`: cutout, fits inside its box, box 556x372 landscape at x 501, y 750

**T04-16x9** (1920x1080)
- `headline` (2 lines, 98px, longest line 20 characters): `Level up your setup<br>and never look back.`
- `sub` (wraps in its box, 40px, longest line 52 characters): `No credit required. Just the tech you actually need.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 750x502 landscape at x 1097, y 289
- `product2`: cutout, fits inside its box, box 341x352 square at x 1046, y 701
- `product3`: cutout, fits inside its box, box 274x360 portrait at x 1589, y 669

**T04-9x16** (1080x1920)
- `headline` (2 lines, 98px, longest line 20 characters): `Level up your setup<br>and never look back.`
- `sub` (wraps in its box, 40px, longest line 52 characters): `No credit required. Just the tech you actually need.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 784x525 landscape at x 148, y 786
- `product2`: cutout, fits inside its box, box 352x363 square at x 203, y 1219
- `product3`: cutout, fits inside its box, box 282x371 portrait at x 595, y 1186


### T05 · Hero product, bleed

**T05-1x1** (1200x1200)
- `headline` (3 lines, 118px, longest line 14 characters): `Say yes to the<br>thing you've<br>been eyeing.`
- `sub` (wraps in its box, 40px, longest line 62 characters): `No credit history required. Just a little good karma to spare.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 576x726 portrait at x 83, y 474

**T05-4x5** (1080x1350)
- `headline` (3 lines, 118px, longest line 14 characters): `Say yes to the<br>thing you've<br>been eyeing.`
- `sub` (wraps in its box, 40px, longest line 62 characters): `No credit history required. Just a little good karma to spare.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 518x745 portrait at x 75, y 474

**T05-16x9** (1920x1080)
- `headline` (3 lines, 118px, longest line 14 characters): `Say yes to the<br>thing you've<br>been eyeing.`
- `sub` (wraps in its box, 40px, longest line 62 characters): `No credit history required. Just a little good karma to spare.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 518x653 portrait at x 495, y 427

**T05-9x16** (1080x1920)
- `headline` (3 lines, 118px, longest line 14 characters): `Say yes to the<br>thing you've<br>been eyeing.`
- `sub` (wraps in its box, 40px, longest line 62 characters): `No credit history required. Just a little good karma to spare.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 778x826 square at x 151, y 1094


### T06 · Top block, photo card

**T06-1x1** (1200x1200)
- `headline` (2 lines, 112px, longest line 17 characters): `Time for the home<br>upgrade you want.`
- `sub` (wraps in its box, 40px, longest line 57 characters): `No credit score needed. Just fair, straightforward terms.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1136x507 landscape at x 32, y 605

**T06-4x5** (1080x1350)
- `headline` (2 lines, 112px, longest line 17 characters): `Time for the home<br>upgrade you want.`
- `sub` (wraps in its box, 40px, longest line 57 characters): `No credit score needed. Just fair, straightforward terms.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1020x480 landscape at x 30, y 663

**T06-16x9** (1920x1080)
- `headline` (2 lines, 112px, longest line 17 characters): `Time for the home<br>upgrade you want.`
- `sub` (wraps in its box, 40px, longest line 57 characters): `No credit score needed. Just fair, straightforward terms.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 840x930 square at x 1060, y 75

**T06-9x16** (1080x1920)
- `headline` (2 lines, 112px, longest line 17 characters): `Time for the home<br>upgrade you want.`
- `sub` (wraps in its box, 40px, longest line 57 characters): `No credit score needed. Just fair, straightforward terms.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1020x693 landscape at x 30, y 868


### T07 · Top block, product on circle

**T07-1x1** (1200x1200)
- `headline` (2 lines, 120px, longest line 12 characters): `Your upgrade<br>starts here.`
- `sub` (wraps in its box, 40px, longest line 45 characters): `No credit score needed. Just tap and say yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 726x487 landscape at x 237, y 636

**T07-4x5** (1080x1350)
- `headline` (2 lines, 120px, longest line 12 characters): `Your upgrade<br>starts here.`
- `sub` (wraps in its box, 40px, longest line 45 characters): `No credit score needed. Just tap and say yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 479x321 landscape at x 300, y 632

**T07-16x9** (1920x1080)
- `headline` (2 lines, 120px, longest line 12 characters): `Your upgrade<br>starts here.`
- `sub` (wraps in its box, 40px, longest line 45 characters): `No credit score needed. Just tap and say yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 450x302 landscape at x 1247, y 279

**T07-9x16** (1080x1920)
- `headline` (2 lines, 120px, longest line 12 characters): `Your upgrade<br>starts here.`
- `sub` (wraps in its box, 40px, longest line 45 characters): `No credit score needed. Just tap and say yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 582x391 landscape at x 248, y 857


### T08 · Typographic statement

**T08-1x1** (1200x1200)
- `headline` (4 lines, 160px, longest line 15 characters): `You want it.<br>You need it.<br>You deserve it.<br>Go. Get it.`
- `sub` (wraps in its box, 40px, longest line 61 characters): `Fair terms, no credit score needed. Just show up and say yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`

**T08-4x5** (1080x1350)
- `headline` (4 lines, 145px, longest line 15 characters): `You want it.<br>You need it.<br>You deserve it.<br>Go. Get it.`
- `sub` (wraps in its box, 40px, longest line 61 characters): `Fair terms, no credit score needed. Just show up and say yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`

**T08-16x9** (1920x1080)
- `headline` (4 lines, 160px, longest line 15 characters): `You want it.<br>You need it.<br>You deserve it.<br>Go. Get it.`
- `sub` (wraps in its box, 40px, longest line 61 characters): `Fair terms, no credit score needed. Just show up and say yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`

**T08-9x16** (1080x1920)
- `headline` (4 lines, 145px, longest line 15 characters): `You want it.<br>You need it.<br>You deserve it.<br>Go. Get it.`
- `sub` (wraps in its box, 40px, longest line 61 characters): `Fair terms, no credit score needed. Just show up and say yes.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`


### T09 · Hero photo, full width

**T09-1x1** (1200x1200)
- `headline` (wraps in its box, 108px, longest line 25 characters): `Your next upgrade <em>awaits.</em>`
- `sub` (wraps in its box, 36px, longest line 57 characters): `No credit required. Just the upgrade you've been wanting.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1200x685 landscape at x 0, y 515

**T09-4x5** (1080x1350)
- `headline` (wraps in its box, 108px, longest line 25 characters): `Your next upgrade <em>awaits.</em>`
- `sub` (wraps in its box, 36px, longest line 57 characters): `No credit required. Just the upgrade you've been wanting.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1080x831 landscape at x 0, y 519

**T09-16x9** (1920x1080)
- `headline` (wraps in its box, 108px, longest line 25 characters): `Your next upgrade <em>awaits.</em>`
- `sub` (wraps in its box, 36px, longest line 57 characters): `No credit required. Just the upgrade you've been wanting.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 940x1000 square at x 940, y 40

**T09-9x16** (1080x1920)
- `headline` (wraps in its box, 108px, longest line 25 characters): `Your next upgrade <em>awaits.</em>`
- `sub` (wraps in its box, 36px, longest line 57 characters): `No credit required. Just the upgrade you've been wanting.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `photo`: photo, fills its box, box 1080x1201 square at x 0, y 719


### T10 · Product trio, circles

**T10-1x1** (1200x1200)
- `headline` (2 lines, 119px, longest line 14 characters): `Upgrade your<br>everyday gear.`
- `sub` (wraps in its box, 40px, longest line 50 characters): `No credit needed. Just the gear you actually want.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 180x260 portrait at x 46, y 543
- `product2`: cutout, fits inside its box, box 458x307 landscape at x 372, y 518
- `product3`: cutout, fits inside its box, box 231x241 square at x 949, y 552

**T10-4x5** (1080x1350)
- `headline` (2 lines, 119px, longest line 14 characters): `Upgrade your<br>everyday gear.`
- `sub` (wraps in its box, 40px, longest line 50 characters): `No credit needed. Just the gear you actually want.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 162x234 portrait at x 41, y 589
- `product2`: cutout, fits inside its box, box 412x276 landscape at x 335, y 567
- `product3`: cutout, fits inside its box, box 208x217 square at x 855, y 597

**T10-16x9** (1920x1080)
- `headline` (2 lines, 119px, longest line 14 characters): `Upgrade your<br>everyday gear.`
- `sub` (wraps in its box, 40px, longest line 50 characters): `No credit needed. Just the gear you actually want.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 123x177 portrait at x 1059, y 452
- `product2`: cutout, fits inside its box, box 312x209 landscape at x 1285, y 435
- `product3`: cutout, fits inside its box, box 157x164 square at x 1681, y 458

**T10-9x16** (1080x1920)
- `headline` (2 lines, 119px, longest line 14 characters): `Upgrade your<br>everyday gear.`
- `sub` (wraps in its box, 40px, longest line 50 characters): `No credit needed. Just the gear you actually want.`
- `cta` (the pill scales to fit, keep it to two or three words, 74px): `Leap Forward`
- `product1`: cutout, fits inside its box, box 133x191 portrait at x 130, y 1071
- `product2`: cutout, fits inside its box, box 337x226 landscape at x 372, y 1052
- `product3`: cutout, fits inside its box, box 170x177 square at x 799, y 1077


### P1 · Knolling flat-lay

**P1-1200x1200** (1200x1200)
- `headline` (2 lines, 95px, longest line 19 characters): `Your Whole Wish<br>List, Lease-to-Own.`
- `sub` (2 lines, 36px, longest line 59 characters): `From couches to TVs to tires, lease-to-own the big stuff at<br>thousands of retailers this Cyber Week.`
- `cta` (36px, longest line 31 characters): `Shop Cyber Deals. Lease to Own.`

**P1-1200x628** (1200x628)
- `headline` (2 lines, 62px, longest line 19 characters): `Your Whole Wish<br>List, Lease-to-Own.`
- `sub` (3 lines, 26px, longest line 44 characters): `From couches to TVs to tires, lease-to-own<br>the big stuff at thousands of retailers this<br>Cyber Week.`
- `cta` (28px, longest line 31 characters): `Shop Cyber Deals. Lease to Own.`

**P1-960x1200** (960x1200)
- `headline` (2 lines, 76px, longest line 19 characters): `Your Whole Wish<br>List, Lease-to-Own.`
- `sub` (2 lines, 34px, longest line 56 characters): `From couches to TVs to tires, lease-to-own the big stuff<br>at thousands of retailers this Cyber Week.`
- `cta` (34px, longest line 31 characters): `Shop Cyber Deals. Lease to Own.`

**P1-300x600** (300x600)
- `headline` (2 lines, 30px, longest line 19 characters): `Your Whole Wish<br>List, Lease-to-Own.`
- `sub` (3 lines, 15px, longest line 39 characters): `From couches to TVs to tires,<br>lease-to-own the big stuff at thousands<br>of retailers this Cyber Week.`
- `cta` (2 lines, 20px, longest line 17 characters): `Shop Cyber Deals.<br>Lease to Own.`

**P1-300x250** (300x250)
- `headline` (3 lines, 22px, longest line 13 characters): `Your Whole<br>Wish List,<br>Lease-to-Own.`
- `sub` (4 lines, 10px, longest line 29 characters): `From couches to TVs to tires,<br>lease-to-own the big stuff at<br>thousands of retailers this<br>Cyber Week.`
- `cta` (2 lines, 12px, longest line 17 characters): `Shop Cyber Deals.<br>Lease to Own.`

**P1-160x600** (160x600)
- `headline` (3 lines, 20px, longest line 13 characters): `Your Whole<br>Wish List,<br>Lease-to-Own.`
- `sub` (5 lines, 12px, longest line 23 characters): `From couches to TVs to<br>tires, lease-to-own the<br>big stuff at thousands<br>of retailers this<br>Cyber Week.`
- `cta` (2 lines, 13px, longest line 17 characters): `Shop Cyber Deals.<br>Lease to Own.`

**P1-728x90** (728x90)
- `headline` (2 lines, 25px, longest line 19 characters): `Your Whole Wish<br>List, Lease-to-Own.`
- `cta` (2 lines, 13px, longest line 17 characters): `Shop Cyber Deals.<br>Lease to Own.`

**P1-320x50** (320x50)
- `headline` (12px, longest line 35 characters): `Your Whole Wish List, Lease-to-Own.`
- `cta` (8px, longest line 31 characters): `Shop Cyber Deals. Lease to Own.`


### P2 · Photo + highlight bars

**P2-1200x1200** (1200x1200)
- `headline` (2 lines, 119px, longest line 18 characters): `<span class="t1">The turkey's fine.</span><span class="t2">The oven isn't.</span>`
- `cta` (44px, longest line 30 characters): `Shop Appliances. Lease to Own.`
- `photo`: photo, fills its box, box 1200x1200 square at x 0, y 0

**P2-1200x628** (1200x628)
- `headline` (2 lines, 88px, longest line 18 characters): `<span class="t1">The turkey's fine.</span><span class="t2">The oven isn't.</span>`
- `cta` (31px, longest line 30 characters): `Shop Appliances. Lease to Own.`
- `photo`: photo, fills its box, box 1200x628 landscape at x 0, y 0

**P2-960x1200** (960x1200)
- `headline` (2 lines, 95px, longest line 18 characters): `<span class="t1">The turkey's fine.</span><span class="t2">The oven isn't.</span>`
- `cta` (46px, longest line 30 characters): `Shop Appliances. Lease to Own.`
- `photo`: photo, fills its box, box 960x1200 portrait at x 0, y 0

**P2-300x600** (300x600)
- `headline` (2 lines, 33px, longest line 18 characters): `<span class="t1">The turkey's fine.</span><span class="t2">The oven isn't.</span>`
- `cta` (2 lines, 19px, longest line 16 characters): `Shop Appliances.<br>Lease to Own.`
- `photo`: photo, fills its box, box 300x600 portrait at x 0, y 0

**P2-300x250** (300x250)
- `headline` (2 lines, 30px, longest line 18 characters): `<span class="t1">The turkey's fine.</span><span class="t2">The oven isn't.</span>`
- `cta` (1 line, 12px, longest line 30 characters): `<span>Shop Appliances. Lease to Own.</span>`
- `photo`: photo, fills its box, box 300x250 landscape at x 0, y 0

**P2-160x600** (160x600)
- `headline` (5 lines, 31px, longest line 8 characters): `<span class="t1">The</span><span class="t1">turkey's</span><span class="t1">fine.</span><span class="t2">The oven</span><span class="t2">isn't.</span>`
- `cta` (2 lines, 12px, longest line 16 characters): `<span>Shop Appliances.<br>Lease to Own.</span>`
- `photo`: photo, fills its box, box 160x600 portrait at x 0, y 0

**P2-728x90** (728x90)
- `headline` (2 lines, 32px, longest line 18 characters): `<span class="t1">The turkey's fine.</span><span class="t2">The oven isn't.</span>`
- `cta` (2 lines, 18px, longest line 16 characters): `Shop Appliances.<br>Lease to Own.`
- `photo`: photo, fills its box, box 278x90 landscape at x 450, y 0

**P2-320x50** (320x50)
- `headline` (2 lines, 14px, longest line 18 characters): `<span class="t1">The turkey's fine.</span><span class="t2">The oven isn't.</span>`
- `cta` (2 lines, 8px, longest line 16 characters): `Shop Appliances.<br>Lease to Own.`
- `photo`: photo, fills its box, box 122x50 landscape at x 198, y 0


### P3A · Flat brand type, Dark Blue

**P3A-1200x1200** (1200x1200)
- `headline` (4 lines, 151px, longest line 14 characters): `<span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span> you</span><span class="t2">don't have to.</span>`
- `sub` (2 lines, 63px, longest line 25 characters): `<span>Lease-to-own on thousands</span><span>of Cyber Week deals.</span>`
- `cta` (1 line, 45px, longest line 20 characters): `<span>Shop Cyber Deals Now</span>`

**P3A-1200x628** (1200x628)
- `headline` (3 lines, 100px, longest line 21 characters): `<span class="t1">The <span class="ta">deals</span> won't wait.</span><span class="t2">And <span class="ta">now</span> you</span><span class="t2">don't have to.</span>`
- `sub` (2 lines, 48px, longest line 25 characters): `<span>Lease-to-own on thousands</span><span>of Cyber Week deals.</span>`
- `cta` (1 line, 42px, longest line 20 characters): `<span>Shop Cyber Deals Now</span>`

**P3A-960x1200** (960x1200)
- `headline` (5 lines, 156px, longest line 11 characters): `<span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span></span><span class="t2">you don't</span><span class="t2">have to.</span>`
- `sub` (2 lines, 51px, longest line 25 characters): `<span>Lease-to-own on thousands</span><span>of Cyber Week deals.</span>`
- `cta` (1 line, 43px, longest line 20 characters): `<span>Shop Cyber Deals Now</span>`

**P3A-300x600** (300x600)
- `headline` (5 lines, 50px, longest line 11 characters): `<span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span></span><span class="t2">you don't</span><span class="t2">have to.</span>`
- `sub` (3 lines, 22px, longest line 20 characters): `<span>Lease-to-own</span><span>on thousands</span><span>of Cyber Week deals.</span>`
- `cta` (1 line, 18px, longest line 20 characters): `<span>Shop Cyber Deals Now</span>`

**P3A-300x250** (300x250)
- `headline` (4 lines, 39px, longest line 14 characters): `<span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span> you</span><span class="t2">don't have to.</span>`
- `cta` (1 line, 13px, longest line 20 characters): `<span>Shop Cyber Deals Now</span>`

**P3A-160x600** (160x600)
- `headline` (5 lines, 29px, longest line 11 characters): `<span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span></span><span class="t2">you don't</span><span class="t2">have to.</span>`
- `sub` (3 lines, 16px, longest line 17 characters): `<span>Lease-to-own</span><span>on thousands of</span><span>Cyber Week deals.</span>`
- `cta` (2 lines, 16px, longest line 10 characters): `<span>Shop Cyber</span><span>Deals Now</span>`

**P3A-728x90** (728x90)
- `headline` (2 lines, 33px, longest line 26 characters): `<span class="t1">The <span class="ta">deals</span> won't wait.</span><span class="t2">And <span class="ta">now</span> you don't have to.</span>`
- `cta` (2 lines, 16px, longest line 10 characters): `<span>Shop Cyber</span><span>Deals Now</span>`

**P3A-320x50** (320x50)
- `headline` (2 lines, 14px, longest line 26 characters): `<span class="t1">The <span class="ta">deals</span> won't wait.</span><span class="t2">And <span class="ta">now</span> you don't have to.</span>`
- `cta` (2 lines, 10px, longest line 10 characters): `<span>Shop Cyber</span><span>Deals Now</span>`


### P3B · Flat brand type, Cream

**P3B-1200x1200** (1200x1200)
- `headline` (4 lines, 151px, longest line 14 characters): `<span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span> you</span><span class="t2">don't have to.</span>`
- `sub` (2 lines, 63px, longest line 25 characters): `<span>Lease-to-own on thousands</span><span>of Cyber Week deals.</span>`
- `cta` (1 line, 45px, longest line 20 characters): `<span>Shop Cyber Deals Now</span>`

**P3B-1200x628** (1200x628)
- `headline` (3 lines, 100px, longest line 21 characters): `<span class="t1">The <span class="ta">deals</span> won't wait.</span><span class="t2">And <span class="ta">now</span> you</span><span class="t2">don't have to.</span>`
- `sub` (2 lines, 48px, longest line 25 characters): `<span>Lease-to-own on thousands</span><span>of Cyber Week deals.</span>`
- `cta` (1 line, 42px, longest line 20 characters): `<span>Shop Cyber Deals Now</span>`

**P3B-960x1200** (960x1200)
- `headline` (5 lines, 156px, longest line 11 characters): `<span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span></span><span class="t2">you don't</span><span class="t2">have to.</span>`
- `sub` (2 lines, 55px, longest line 25 characters): `<span>Lease-to-own on thousands</span><span>of Cyber Week deals.</span>`
- `cta` (1 line, 43px, longest line 20 characters): `<span>Shop Cyber Deals Now</span>`

**P3B-300x600** (300x600)
- `headline` (5 lines, 50px, longest line 11 characters): `<span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span></span><span class="t2">you don't</span><span class="t2">have to.</span>`
- `sub` (3 lines, 22px, longest line 20 characters): `<span>Lease-to-own</span><span>on thousands</span><span>of Cyber Week deals.</span>`
- `cta` (1 line, 18px, longest line 20 characters): `<span>Shop Cyber Deals Now</span>`

**P3B-300x250** (300x250)
- `headline` (4 lines, 39px, longest line 14 characters): `<span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span> you</span><span class="t2">don't have to.</span>`
- `cta` (1 line, 15px, longest line 20 characters): `<span>Shop Cyber Deals Now</span>`

**P3B-160x600** (160x600)
- `headline` (5 lines, 29px, longest line 11 characters): `<span class="t1">The <span class="ta">deals</span></span><span class="t1">won't wait.</span><span class="t2">And <span class="ta">now</span></span><span class="t2">you don't</span><span class="t2">have to.</span>`
- `sub` (3 lines, 16px, longest line 17 characters): `<span>Lease-to-own</span><span>on thousands of</span><span>Cyber Week deals.</span>`
- `cta` (2 lines, 16px, longest line 10 characters): `<span>Shop Cyber</span><span>Deals Now</span>`

**P3B-728x90** (728x90)
- `headline` (2 lines, 33px, longest line 26 characters): `<span class="t1">The <span class="ta">deals</span> won't wait.</span><span class="t2">And <span class="ta">now</span> you don't have to.</span>`
- `cta` (2 lines, 16px, longest line 10 characters): `<span>Shop Cyber</span><span>Deals Now</span>`

**P3B-320x50** (320x50)
- `headline` (2 lines, 14px, longest line 26 characters): `<span class="t1">The <span class="ta">deals</span> won't wait.</span><span class="t2">And <span class="ta">now</span> you don't have to.</span>`
- `cta` (2 lines, 10px, longest line 10 characters): `<span>Shop Cyber</span><span>Deals Now</span>`


### P4A · Proof badge, centered

**P4A-1200x1200** (1200x1200)
- `headline` (2 lines, 124px, longest line 16 characters): `<span>Don't take</span><span>our word for it.</span>`
- `sub` (2 lines, 42px, longest line 43 characters): `<span>Real people, real reviews. There's a reason</span><span>why thousands rate Katapult 5 stars.</span>`
- `cta` (1 line, 42px, longest line 30 characters): `<span>See Why Shoppers Love Katapult</span>`

**P4A-1200x628** (1200x628)
- `headline` (2 lines, 76px, longest line 16 characters): `<span>Don't take</span><span>our word for it.</span>`
- `sub` (3 lines, 28px, longest line 32 characters): `<span>Real people, real reviews.</span><span>There's a reason why</span><span>thousands rate Katapult 5 stars.</span>`
- `cta` (1 line, 25px, longest line 30 characters): `<span>See Why Shoppers Love Katapult</span>`

**P4A-960x1200** (960x1200)
- `headline` (2 lines, 112px, longest line 16 characters): `<span>Don't take</span><span>our word for it.</span>`
- `sub` (2 lines, 42px, longest line 43 characters): `<span>Real people, real reviews. There's a reason</span><span>why thousands rate Katapult 5 stars.</span>`
- `cta` (1 line, 42px, longest line 30 characters): `<span>See Why Shoppers Love Katapult</span>`

**P4A-300x600** (300x600)
- `headline` (3 lines, 53px, longest line 10 characters): `<span>Don't take</span><span>our word</span><span>for it.</span>`
- `sub` (3 lines, 17px, longest line 32 characters): `<span>Real people, real reviews.</span><span>There's a reason why</span><span>thousands rate Katapult 5 stars.</span>`
- `cta` (2 lines, 17px, longest line 16 characters): `<span>See Why Shoppers</span><span>Love Katapult</span>`

**P4A-300x250** (300x250)
- `headline` (1 line, 23px, longest line 27 characters): `<span>Don't take our word for it.</span>`
- `sub` (2 lines, 10px, longest line 43 characters): `<span>Real people, real reviews. There's a reason</span><span>why thousands rate Katapult 5 stars.</span>`
- `cta` (1 line, 12px, longest line 30 characters): `<span>See Why Shoppers Love Katapult</span>`

**P4A-160x600** (160x600)
- `headline` (3 lines, 28px, longest line 12 characters): `<span>Don't</span><span>take our</span><span>word for it.</span>`
- `sub` (4 lines, 14px, longest line 22 characters): `<span>Real people, real</span><span>reviews. There's a</span><span>reason why thousands</span><span>rate Katapult 5 stars.</span>`
- `cta` (2 lines, 12px, longest line 16 characters): `<span>See Why Shoppers</span><span>Love Katapult</span>`

**P4A-728x90** (728x90)
- `headline` (2 lines, 35px, longest line 14 characters): `<span>Don't take our</span><span>word for it.</span>`
- `cta` (2 lines, 12px, longest line 16 characters): `<span>See Why Shoppers</span><span>Love Katapult</span>`

**P4A-320x50** (320x50)
- `headline` (2 lines, 15px, longest line 14 characters): `<span>Don't take our</span><span>word for it.</span>`
- `cta` (2 lines, 5px, longest line 16 characters): `<span>See Why Shoppers</span><span>Love Katapult</span>`


### P4B · Proof badge, photo seam

**P4B-1200x1200** (1200x1200)
- `headline` (2 lines, 110px, longest line 16 characters): `<span>Don't take</span><span>our word for it.</span>`
- `sub` (2 lines, 39px, longest line 43 characters): `<span>Real people, real reviews. There's a reason</span><span>why thousands rate Katapult 5 stars.</span>`
- `cta` (1 line, 39px, longest line 30 characters): `<span>See Why Shoppers Love Katapult</span>`
- `photo`: photo, fills its box, box 1200x600 landscape at x 0, y 0

**P4B-1200x628** (1200x628)
- `headline` (2 lines, 83px, longest line 16 characters): `<span>Don't take</span><span>our word for it.</span>`
- `sub` (2 lines, 28px, longest line 43 characters): `<span>Real people, real reviews. There's a reason</span><span>why thousands rate Katapult 5 stars.</span>`
- `cta` (1 line, 28px, longest line 30 characters): `<span>See Why Shoppers Love Katapult</span>`
- `photo`: photo, fills its box, box 544x628 portrait at x 656, y 0

**P4B-960x1200** (960x1200)
- `headline` (2 lines, 95px, longest line 16 characters): `<span>Don't take</span><span>our word for it.</span>`
- `sub` (2 lines, 36px, longest line 43 characters): `<span>Real people, real reviews. There's a reason</span><span>why thousands rate Katapult 5 stars.</span>`
- `cta` (1 line, 34px, longest line 30 characters): `<span>See Why Shoppers Love Katapult</span>`
- `photo`: photo, fills its box, box 960x560 landscape at x 0, y 0

**P4B-300x600** (300x600)
- `headline` (2 lines, 40px, longest line 16 characters): `<span>Don't take</span><span>our word for it.</span>`
- `sub` (3 lines, 17px, longest line 32 characters): `<span>Real people, real reviews.</span><span>There's a reason why</span><span>thousands rate Katapult 5 stars.</span>`
- `cta` (2 lines, 13px, longest line 16 characters): `<span>See Why Shoppers</span><span>Love Katapult</span>`
- `photo`: photo, fills its box, box 300x230 landscape at x 0, y 0

**P4B-300x250** (300x250)
- `headline` (1 line, 21px, longest line 27 characters): `<span>Don't take our word for it.</span>`
- `sub` (2 lines, 10px, longest line 43 characters): `<span>Real people, real reviews. There's a reason</span><span>why thousands rate Katapult 5 stars.</span>`
- `cta` (1 line, 10px, longest line 30 characters): `<span>See Why Shoppers Love Katapult</span>`
- `photo`: photo, fills its box, box 300x103 landscape at x 0, y 0

**P4B-160x600** (160x600)
- `headline` (3 lines, 30px, longest line 10 characters): `<span>Don't take</span><span>our word</span><span>for it.</span>`
- `sub` (4 lines, 13px, longest line 22 characters): `<span>Real people, real</span><span>reviews. There's a</span><span>reason why thousands</span><span>rate Katapult 5 stars.</span>`
- `cta` (2 lines, 12px, longest line 16 characters): `<span>See Why Shoppers</span><span>Love Katapult</span>`
- `photo`: photo, fills its box, box 160x221 portrait at x 0, y 0

**P4B-728x90** (728x90)
- `headline` (2 lines, 37px, longest line 14 characters): `<span>Don't take our</span><span>word for it.</span>`
- `cta` (2 lines, 12px, longest line 16 characters): `<span>See Why Shoppers</span><span>Love Katapult</span>`
- `photo`: photo, fills its box, box 180x78 landscape at x 373, y 0

**P4B-320x50** (320x50)
- `headline` (2 lines, 16px, longest line 14 characters): `<span>Don't take our</span><span>word for it.</span>`
- `cta` (2 lines, 5px, longest line 16 characters): `<span>See Why Shoppers</span><span>Love Katapult</span>`
- `photo`: photo, fills its box, box 79x39 landscape at x 164, y 0
