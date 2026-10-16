# Reading a Katapult brief

Katapult jobs arrive as a client brief PDF named like `KAT26022 - Trusted`. One PDF per job. Sometimes the file name is wrong (a job arrived as "KAT26005 - Katapult is For" but was KAT26020 Holiday Disaster): trust the job code and title inside the PDF, and say when they differ.

## 1. What a brief PDF carries

| Field | Where it goes |
|---|---|
| Job code and name (`KAT26022`, "Trusted") | file names, post file title |
| Channel (PMAX, Google programmatic, Meta) and funnel (TOF, MOF, BOF) | brief card |
| Hypothesis | brief card; decides the pattern |
| Creative description | brief card; decides the pattern and the imagery |
| Focus ("lean on volume of reviews first") | brief card |
| Sizes table and iterations ("8 sizes x 2 iterations = 16 deliverables") | the frame list |
| Testing variable (none, imagery, static vs animated, copy) | what V1 and V2 differ in |
| Copy per iteration: headline, subhead, CTA, sometimes a disclaimer | slots, verbatim |
| Reference image or concept deck crop | which pattern it is closest to |

## 2. The brief card (Step 1)

Return it in this shape:

```
KAT26023 Back to School · PMAX + Google programmatic · TOF
Hypothesis: ...
Creative: ...
Focus: ...
Deliverables: 8 sizes x 2 iterations = 16. Static. Testing variable: imagery (V1 kitchen, V2 dorm).
Sizes: PMAX 1200x1200, 1200x628, 960x1200 · Programmatic 300x600, 300x250, 160x600, 728x90, 320x50
Copy (verbatim):
  V1 headline: ...   subhead: ...   CTA: ...
  V2 headline: ...   subhead: ...   CTA: ...
Closest pattern: P2 Photo + highlight bars, because ...
Open items:
  1. ...
```

## 3. Sizes and names

Standard Katapult banner set: PMAX static `1200x1200` (1:1), `1200x628` (1.91:1), `960x1200` (4:5); Google programmatic static `300x600`, `300x250`, `160x600`, `728x90`, `320x50`.

File name per frame: `{JOB}-{Name}-{W}x{H}-Static-{PMAX|Programmatic}-V{n}`, Name in CamelCase without spaces. Examples: `KAT26019-TopItems-1200x1200-Static-PMAX-V1`, `KAT26022-Trusted-300x250-Static-Programmatic-V1`. Two layout options for the same iteration add `-OptionA` / `-OptionB`.

Meta and Instagram sizes use the templates: feed `4x5` (1080x1350) or `1x1`, Stories and Reels `9x16`, landscape `16x9`.

## 4. Iterations

- **Two copy or imagery iterations (V1, V2):** same pattern, every size twice, the slot that the testing variable names changes. When the brief gives different copy per iteration, use it: the brief's copy wins over its stated testing variable. Mention the mismatch once in the open items, without blocking the job.
- **Static vs animated (V1 static, V2 animated):** this project builds statics. For V2, build the storyboard as separate statics per scene, named `-Animated-...-V2-S01`, `-S02`, `-S03`: S01 bare ground and copy, S02 the elements arriving, S03 equals the V1 static. Nothing moves position between scenes. The motion itself is built by the art director's team; say so in the hand-off.
- **Option A / Option B** (two layouts, the account lead picks one): only when the brief or the account lead asks.

## 5. Open items you must raise, never fill

- A review wall, quotes, a TrustScore or a review count: needs the real, approved content from the client. Without it, use P4 as is (stars only, no quote, no number) and list it.
- A photo the brief shows but the Library does not have: ask the account lead for the file; it comes in as `upload:`.
- A disclaimer the brief carries on a pattern without a legal slot: ask the account lead. The legal line that P2 and the templates already carry is part of the approved layout; it is not an open item.
- Copy missing for a size or iteration, or a subhead that cannot be read at 728x90 and 320x50: the default drops it there (see `01-brand.md` 2.2); ask only when the brief says otherwise.
- A concept the four patterns cannot answer (new illustration, a different product grid, animation): say which pattern is closest, and pass the gap to the art director.

## 6. Past jobs (worked examples)

**KAT26019 Top Items** · PMAX + programmatic · TOF. Hypothesis: a clear Cyber headline over an array of items educates people about lease-to-own. Creative: Cyber Week headline plus a knolling grid of popular items. 8 sizes x 2 (V1 static, V2 animated). Copy: "Your Whole Wish List, Lease-to-Own." / "From couches to TVs to tires, lease-to-own the big stuff at thousands of retailers this Cyber Week." / "Shop Cyber Deals. Lease to Own." → pattern **P1**. Subhead kept on 160x600 and 300x250 after client review; dropped on 728x90 and 320x50.

**KAT26020 Holiday Disaster** · MOF/BOF. Hypothesis: a relatable holiday appliance disaster plus an immediate lease-to-own fix beats benefit-led creative. Creative: a slightly comedic headline over holiday chaos, CTA pivots from panic to relief. 8 sizes x 2, testing variable imagery (V1 kitchen, V2 living room). Copy V1: "The turkey's fine. The oven isn't." / "Shop Appliances. Lease to Own." → pattern **P2**, setup line on the Cream bar, punchline on the Dark Blue bar. The legal line on the three PMAX sizes was the account lead's call.

**KAT26021 Flat Brand Type, Cyber** · MOF/BOF. Hypothesis: a bold text-only Cyber lockup in brand colours earns the highest thumb-stop. No imagery. 8 sizes x 1. Copy: "The deals won't wait. And now you don't have to." / "Lease-to-own on thousands of Cyber Week deals" / "Shop Cyber Deals Now" → pattern **P3A** (V2 Cream is **P3B**). Accent words: "deals", "now".

**KAT26022 Trusted** · TOF. Hypothesis: third-party social proof beats brand-voiced creative with first-time prospects. Creative: bold headline over a wall of real 5-star Trustpilot reviews. Copy: "Don't take our word for it." / "Real people, real reviews. There's a reason why thousands rate Katapult 5 stars." / "See Why Shoppers Love Katapult" → pattern **P4A** or **P4B**. Blocked item: real review quotes, the TrustScore and the official badge were never supplied, so the frames carry stars only. That is the correct behaviour.

**Q4 2026 organic** (Facebook and Instagram). Client sheet with titles and slide copy, pre-approved: copy went on the art verbatim, Title Case kept, no edits. Carousels 4:5, statics 4:5, Stories 9:16.
