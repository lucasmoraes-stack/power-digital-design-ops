# November organic · photo audit

Date: 2026-10-16. Read-only audit. No frame, build file or Figma node was changed.

## Method

- **Library**: the 44 JPGs in `clients/katapult/01-brand/photos/library/`.
- **October organic (Figma `D8FpNuKI3uPGjCPqonIn3C`, page "kat os")**: `download_assets` on all 15 section ids from `04-deliverables/social/2026-10-organic/frames.json`. Section 05 hit the 20-image cap, so its frames were pulled one by one. Sections 07, 08, 09 and 12 have no raw images. 163 raw image fills were downloaded.
- **Banners**: every jpg/png/webp under `03-work/banners/*/` and `04-deliverables/banners/*/`, plus every base64 image (over 20 KB) embedded in `04-deliverables/deliverables-hub.html` (K22_PHOTO, K20_PHOTOS, KN_PHOTOS, PHOTOS) and in the banner HTML files (36 unique images).
- **Comparison**: SIFT features (OpenCV 5.0), Lowe ratio 0.7, RANSAC homography. This handles Figma crops and resizes. A dHash distance was also recorded for each pair. The scores split cleanly. True matches had **129 to 1,883** geometric inliers, with the runner-up library photo at 37 or less. Non-matches peaked at **63**. Borderline pairs from 30 to 63 inliers (KAT26020 turkey/oven scenes, KAT26019 product cutouts) were checked side by side, and none was a real match.
- **Visible vs. hidden**: a raw fill in a Figma section can sit on a hidden layer. Every matched library photo was also checked against the fresh Figma section exports and the local October final PNGs (`04-deliverables/social/2026-10-organic/png`). Only photos visible in the finals count as past use.

## (a) Library photos already used in past work (30)

| Library photo | Where (visible) |
|---|---|
| phone-man-green-sofa-phone-03 | Oct 01 What Is Lease-to-Own, slide 3 |
| phone-senior-woman-call-10 | Oct 02 LTO vs Traditional Credit, slide 1 (also a hidden fill in Oct 06) |
| laptop-man-sofa-coffee-laptop-05 | Oct 02, slide 3 |
| at-home-woman-daybed-plants-06 | Oct 02, slide 4 |
| phone-man-kitchen-phone-07 | Oct 02, slide 5 |
| phone-woman-dog-phone-02 | Oct 04 When You Need It, slide 1 |
| retail-man-tire-dealership-01 | Oct 04, slide 3 (also a hidden fill in Oct 15) |
| laptop-woman-window-desk-06 | Oct 04, slide 4 · **KAT26022 Trusted banners** (job img + hub K22_PHOTO) |
| laptop-woman-sofa-laptop-01 | Oct 05 Your Next Chapter, slide 1 |
| unboxing-kids-moving-box-01 | Oct 05, slide 1 |
| at-home-woman-pendant-lamp-03 | Oct 05, slide 1 |
| room-blue-fridge-kitchen-03 | Oct 05, slide 2 |
| room-orange-armchair-room-02 | Oct 05, slide 2 |
| phone-man-window-phone-08 | Oct 05, slide 5 |
| laptop-woman-tablet-counter-04 | Oct 06 More Choices, slide 1 (also a hidden fill in Oct 13) |
| phone-woman-headphones-selfie-09 | Oct 06, slide 2 (photo grid) |
| phone-man-street-phone-01 | Oct 06, slide 2 |
| together-couple-hug-laptop-04 | Oct 06, slide 2 |
| phone-woman-lamps-phone-04 | Oct 06, slide 2 |
| phone-senior-man-phone-11 | Oct 06, slide 2 |
| at-home-senior-woman-armchair-02 | Oct 06, slide 2 |
| at-home-woman-headphones-relax-07 | Oct 10 Get What You Need (static) |
| at-home-woman-sofa-coffee-01 | Oct 13 More Than a Payment Option, slide 1 |
| laptop-man-glasses-laptop-09 | Oct 13, slide 4 |
| laptop-woman-tablet-laughing-08 | Oct 13, slide 5 |
| laptop-woman-tablet-orange-sofa-07 | Oct 14 Built for Shoppers, slide 1 (small circle) |
| laptop-man-bed-laptop-10 | Oct 14, slide 2 |
| retail-shop-owners-tablet-02 | Oct 14, slide 3 |
| at-home-woman-beanbag-mug-04 | Oct 15 Why Katapult Exists, slide 3 |
| together-friends-gaming-sofa-02 | Oct 15, slide 5 |

Hidden only, not counted as used: **unboxing-woman-unboxing-sofa-02** is a fill inside the Oct 14 section, but it does not show in any rendered October frame.

Banners: KAT26019 (product cutouts, knolling ground), KAT26020 (generated kitchen and living-room scenes) and KAT26021 contain no library photo. KAT26022 uses laptop-woman-window-desk-06 only.

Some October photos are not in the library, for example the two people photos on Oct 14 slide 5 and the other raw fills that matched nothing.

## (b) November frames (`build/frames/*/*.html`)

Product cutouts (`*.webp`, `b-*.png` products) are Social Studio cutouts, not library photos, and are marked NOT-LIBRARY.

| Frame | Photo (build/img) | Library original | Status |
|---|---|---|---|
| 01 how-katapult-works static | phone-woman-kitchen-phone-12.jpg | phone-woman-kitchen-phone-12 | OK |
| 02 why-choose-LTO _01 | couch.webp, fridge.webp, headphones-trim.webp | n/a (cutouts) | NOT-LIBRARY |
| 02 _02 | laptop-woman-sofa-laptop-01.jpg | laptop-woman-sofa-laptop-01 | **PAST-USED** (Oct 05 s1) |
| 02 _03 | couch, fridge, headphones-trim, laptop-open, tv, washer (.webp) | n/a (cutouts) | NOT-LIBRARY |
| 02 _04 | unboxing-woman-unboxing-sofa-02.jpg | unboxing-woman-unboxing-sofa-02 | OK (only a hidden fill in Oct 14 Figma) |
| 02 _05 | together-couple-hug-laptop-04.jpg | together-couple-hug-laptop-04 | **PAST-USED** (Oct 06 s2) |
| 03 holiday-wishlist story | b-bed, b-couch-green, b-fridge, b-headphones, b-tire-stack (.png) | n/a (cutouts) | NOT-LIBRARY |
| 04 pay-over-time _01 | phone-woman-card-phone-05.jpg | phone-woman-card-phone-05 | OK |
| 04 _02 | phone-woman-dog-phone-02.jpg | phone-woman-dog-phone-02 | **PAST-USED** (Oct 04 s1) |
| 04 _03 | laptop-woman-blanket-laptop-03.jpg | laptop-woman-blanket-laptop-03 | OK |
| 04 _04 | laptop-woman-desk-laptop-02.jpg | laptop-woman-desk-laptop-02 | OK |
| 05 pov static | together-senior-couple-kitchen-06.jpg | together-senior-couple-kitchen-06 | OK |
| 06 customer-testimonial story | b-tire.png | n/a (cutout) | NOT-LIBRARY |
| 08 more-ways-to-buy static | (no photo) | n/a | n/a |
| 09 q-and-a _01 | b-phone-man-kitchen-phone-07.jpg | phone-man-kitchen-phone-07 | **PAST-USED** (Oct 02 s5) |
| 09 _02 | (no photo) | n/a | n/a |
| 10 discover-where-you-can-shop | b-couch-green, b-headphones, b-tire, b-tv, b-washer (.png) | n/a (cutouts) | NOT-LIBRARY |
| 11 did-you-know static | (no photo) | n/a | n/a |
| 12 thanksgiving static | b-phone-senior-woman-call-10.jpg | phone-senior-woman-call-10 | **PAST-USED** (Oct 02 s1) |
| | b-together-couple-tablet-mug-05.jpg | together-couple-tablet-mug-05 | OK |
| | b-together-family-homework-sofa-03.jpg | together-family-homework-sofa-03 | OK |
| | b-together-friends-cooking-07.jpg | together-friends-cooking-07 | OK |
| 13 black-friday _01 | b-bed, b-headphones, b-laptop-open, b-tv (.png) | n/a (cutouts) | NOT-LIBRARY |
| 13 _02 | b-together-friends-gaming-sofa-02.jpg | together-friends-gaming-sofa-02 | **PAST-USED** (Oct 15 s5) |
| | b-couch-green, b-headphones, b-tv (.png) | n/a (cutouts) | NOT-LIBRARY |
| 13 _03 | b-laptop-man-bed-laptop-10.jpg | laptop-man-bed-laptop-10 | **PAST-USED** (Oct 14 s2) |
| | b-headphones, b-laptop-open, b-monitor (.png) | n/a (cutouts) | NOT-LIBRARY |
| 13 _04 | b-at-home-senior-woman-armchair-02.jpg | at-home-senior-woman-armchair-02 | **PAST-USED** (Oct 06 s2) |
| | b-bed, b-nightstand (.png) | n/a (cutouts) | NOT-LIBRARY |
| 14 more-ways-to-shop _01 | b-together-couple-sofa-phone-laptop-01.jpg | together-couple-sofa-phone-laptop-01 | OK |
| 14 _02 | (no photo) | n/a | n/a |
| 14 _03 | b-phone-man-street-phone-01.jpg | phone-man-street-phone-01 | **PAST-USED** (Oct 06 s2) |

Every `build/img` people photo matched the library file of the same name (654 to 1,722 inliers), so filenames are reliable. `fridge-friends.jpg` and `fig/oct04s2-a.jpg` match no library photo, and no November frame references them.

**Summary: 9 November frames reuse an October photo.** They are 02_02, 02_05, 04_02, 09_01, 12 (one of four photos), 13_02, 13_03, 13_04 and 14_03. Another 10 library photos are fresh (OK).

## (c) Library photos never used anywhere (past or November) (4)

| Photo | Catalog subject | Brand fit |
|---|---|---|
| at-home-woman-dishwasher-05 | Woman loading a dishwasher in a blue kitchen, smiling (appliances) | on-brand |
| phone-man-call-tablet-sofa-06 | Grey-haired man on a phone call holding a tablet on a white sofa | on-brand |
| retail-business-owner-workshop-03 | Small business owner in a blue blazer, arms crossed, in her workshop | on-brand |
| room-leather-sofa-room-01 | Brown leather sofa with a plant in a sunny room, no people | no people (background only, never the main image) |

If unboxing-woman-unboxing-sofa-02 were dropped from November, it would join this list (October only has it as a hidden fill).

## (d) Photos used twice within November

- **Library photos**: none. Each of the 19 library photos appears in exactly one November frame.
- **Product cutouts (not library)** repeat: b-headphones in 5 frames (03, 10, 13_01, 13_02, 13_03). b-bed, b-couch-green and b-tv in 3 frames each. b-tire and b-laptop-open in 2 each. couch, fridge and headphones-trim (.webp) appear in both 02_01 and 02_03.
