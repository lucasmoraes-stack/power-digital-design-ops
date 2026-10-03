# KAT26021 Flat Brand Type, Cyber: brief

Brand: Katapult. Channel: PMAX + Google programmatic banners. Funnel: MOF/BOF. Triage: 2026-10-02.
Source: client brief PDF "KAT26021 - Flat Brand Type - Cyber" (sent in chat 2026-10-02, not saved in the repo). Concept deck (Google Slides, Concept 3) not accessible from here, only the reference crop in the PDF.

## The ask

Hypothesis: a bold, text-only Cyber lockup in brand colors earns the highest thumb-stop in a crowded Cyber Week feed. Shoppers scan for deal signals, and loud type reads faster than product imagery.
Creative: flat, full-bleed brand-color background, oversized high-contrast type stack, no imagery. Short lease-to-own subhead and a clear CTA button underneath.
Focus: testing type and brand colors only.

8 sizes x 1 iteration = 8 deliverables. Static only. Testing variable: none.

| Platform | Sizes |
|---|---|
| PMAX static | 1200x628 (1.91:1), 1200x1200 (1:1), 960x1200 (4:5) |
| Google programmatic static | 300x600, 320x50, 300x250, 160x600, 728x90 |

## Copy (client, verbatim, no edits)

- Headline: The deals won't wait. And now you don't have to.
- Subhead: Lease-to-own on thousands of Cyber Week deals
- CTA: Shop Cyber Deals Now

No em/en dash in the copy. "Lease-to-own" uses hyphens, which is fine. Apostrophes kept straight, as the brief has them. The subhead has no final period in the brief and stays that way.

## What each size carries

Copy is law: whatever appears is verbatim, nothing added (no disclaimer, the brief has none).
Headline, subhead and CTA on the three PMAX sizes and 300x600. 160x600, 300x250, 728x90 and 320x50 carry headline + CTA only, following the Katapult banner default approved on KAT26019 (2026-10-02).
The headline is only broken into lines; each sentence starts on its own line so the two sentences can take two colors.

## Design

- Ground: Dark Blue #131540, full bleed.
- Headline: Aktiv Grotesk Bold, tight leading, sized per format to fill the space between logo and subhead. Sentence 1 White, sentence 2 Pink #ED5370 (5.02:1 on Dark Blue, per the Brand Guardian ruling).
- Subhead: Aktiv Grotesk Medium, Light Blue #9EB5C0.
- CTA: Katapult pink pill, white text, medium weight (house banner rule). This is why the ground is Dark Blue and not Pink: on Pink the pill would disappear.
- Logo: Katapult pink, top left; in strips, at the left edge.
- Safe zones: 5% inset on PMAX, 4 to 12px on programmatic.

## Build

Generator: [build.py](build.py) injects k21.css / k21.html / k21.js into a fresh read of the Katapult Deliverables Hub, as a second job inside the Banners channel (above KAT26019).
