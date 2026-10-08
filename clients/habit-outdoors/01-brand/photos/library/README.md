# Habit Outdoors · Image library

The approved image library for Habit emails. One catalogue (`catalog.md`) indexes every usable photo,
and one page (the **Image Library** artifact, https://claude.ai/code/artifact/4006b37f-7efb-4d33-9d00-99c119d08a88) shows them as a filterable contact sheet. Republish to that same URL after every rebuild.

## How to add images

1. **Drop the selected files in `_inbox/`**, as they are (any name, full resolution, JPG/PNG/TIFF/HEIC).
2. Ask Claude to "process the Habit image inbox". It will:
   - rename each file to the convention below and move it to `library/`;
   - keep the full-resolution file, plus a 2400px JPG (q88) when the original is larger than 8 MB;
   - add one row per image to `catalog.md` (subject, category, calm area, best use, rights);
   - rebuild and republish the Image Library page (`python ../build_image_library.py`).
3. Anything Claude cannot tell from the image (who shot it, usage rights, season, product names) is written as `[[CONFIRMAR]]` in the row.

## Naming

`{category}-{subject}-{nn}.jpg`, lowercase, hyphens, no spaces or accents.
Examples: `hunting-treestand-sunrise-01.jpg`, `fishing-wading-river-02.jpg`, `camp-family-fire-01.jpg`.

Categories: `hunting`, `fishing`, `camp` (camp and family), `farm` (farm and workwear), `detail` (product in use, close-up), `landscape` (no people, backgrounds).

## Rules

- Photos only from Habit / Mahco or shot for them. Never another brand's imagery (no Duck Camp, no reference screenshots).
- No text, logo or button baked into the image. Brand marks printed on the product are fine.
- Files in this folder stay **out of git** (they are on disk and OneDrive). `catalog.md`, this README and the page are tracked.
- Email modules never use these files directly: crops for each module are made into `email-kit/assets/`.
