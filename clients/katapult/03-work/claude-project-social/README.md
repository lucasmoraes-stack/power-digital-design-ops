# Katapult Social Studio · Claude Project package

A Claude Project where any designer on the team takes a Katapult job from the brief PDF to review-ready PNGs: Meta and Instagram posts (the ten social templates) and PMAX and Google programmatic banners (the four approved banner patterns), with no setup on their side. Same model as the CDI Email and Social Studios.

| Piece | Role | Who changes it |
|---|---|---|
| **Katapult Social Studio** artifact, https://claude.ai/code/artifact/5a137796-2f13-4690-8ce2-45fd9f4c8cdc | Make PNG (drop the post file, read the checks, download PNG or .zip), every layout rendered, every photo and product id. Holds the layouts, fonts, logo and the 93 images as artifact assets | Lucas only (teammates: Viewer) |
| **Katapult Social Studio** Claude Project (this package) | Where the designer works: attaches the brief PDF, approves plan and copy, gets the post file | Lucas updates instructions and knowledge; teammates only chat |
| Katapult Design System, Image Library, Deliverables Hub | References; finished jobs go to the Hub for review | Lucas |

## How a job flows

1. The designer opens the Project, attaches the brief PDF (`KAT26xxx - Name.pdf`) and says "new job".
2. Claude returns the brief card (sizes, copy verbatim, open items), then the plan (one pattern across the eight sizes, or a template per post), the line breaks per size and the photos. The designer approves each step (or all at once).
3. Claude hands over one post file, `KAT26xxx-Name.html`: one `<section data-use="P2-1200x1200">` per frame, with only the slots filled (headline, sub, cta, photo, products).
4. The designer drops the file in the Studio (Make PNG) with any `upload:` images, reads the checks on every frame (slots filled, wrapped lines, off-frame text, overlaps), and downloads the .zip.
5. The PNGs go to review in the Deliverables Hub.

What the Project does not do: new layouts, new patterns, animation, image generation. Those come back to Lucas as a written request from the Project.

## What is in the package

| dist/ file | Source | Note |
|---|---|---|
| `project-instructions.md` | `src/project-instructions.md` | the six-step flow, revisions, commands, hard rules |
| `knowledge/01-brand.md` | `src/knowledge/` | voice, copy-is-law, legal line, colour, logo, photography |
| `knowledge/02-studio-kit.md` | `src/kit-head.md` + `studio/catalog.json` + `studio/boxes.json` | post file format, slot rules, the 88 layouts with sample copy, line counts, sizes, characters per line, photo box sizes |
| `knowledge/03-image-library.md` | `src/library-head.md` + `studio/catalog.json` + `studio/subjects.json` | 44 photos with face position, 15 product cutouts |
| `knowledge/04-brief-intake.md` | `src/knowledge/` | reading a KAT brief PDF, sizes, naming, V1/V2, open items, past jobs |
| `knowledge/05-banner-craft.md`, `06-katapult-patterns.md` | `src/skills/*/SKILL.md` | the banner-craft and katapult-banners skills, rewritten for the Project |
| `knowledge/07-review-checklist.md` | `src/knowledge/` | the Brand Guardian pass, as a checklist |
| `skills/katapult-banner-craft.zip`, `skills/katapult-patterns.zip` | same skills | optional: upload as claude.ai Skills (Settings, Capabilities, Skills) for people who work outside the Project |

## Set up the Project (once, about 10 minutes)

1. claude.ai, Projects, **Create project**. Name `Katapult Social Studio`. Description: `Take a Katapult brief PDF to review-ready social posts and PMAX/programmatic banners.`
2. **Instructions**: paste `dist/project-instructions.md`.
3. **Knowledge**: upload the seven files in `dist/knowledge/`.
4. **Share** the Project with each designer as **Can use**.
5. Open the **Katapult Social Studio** artifact, Share, add the designers as **Viewer** (they need it to make PNGs). Do the same for the Design System, Image Library and Deliverables Hub.
6. Optional: upload the two zips in `dist/skills/` as Skills.

## Build and test

```
python tools/build_kit.py          # layouts, slots, images -> studio/kit.json, catalog.json, assets/
python tools/dump_boxes.py         # photo and product box sizes per layout -> studio/boxes.json (needs a --local build)
python tools/build_studio.py       # the artifact page, asset urls from studio/asset-map.json
python tools/build_studio.py --local && python tools/autotest.py <post.html>   # render a post file locally, PNGs + checks in studio/_test/
python tools/make_testpost.py      # one frame per layout, for a full regression with autotest.py
python tools/build_project.py      # dist/, stops on another client's name, an internal path or a long dash
```

Images are artifact assets, uploaded once with the Artifact tool (`upload_asset`, 25 per call) and mapped in `studio/asset-map.json` (`asset-map-sha.json` records what was uploaded; `build_studio.py` refuses to build when an image changed or is new and was not uploaded).

Tested 2026-10-13: all 88 layouts render and export identical to the source frames with real photos and products swapped in; a dry run of the Project (an isolated agent with only `dist/`) took a mock KAT26024 brief to a 16-frame P2 file that rendered with every check passing after two Studio fixes (P2 bars grow upward; overlap check measures bars and pills).

## Keep in sync

- **Template or banner pattern changed** (Figma, then `01-brand/templates/` or the job folders in `03-work/banners/`): `build_kit.py`, upload any new image the build reports, `build_studio.py`, publish the Studio, `dump_boxes.py`, `build_project.py`, replace `02-studio-kit.md` in the Project.
- **New photo in the Image Library**: add it to `01-brand/photos/library/catalog.md` and its face position to `studio/subjects.json`, `build_kit.py`, upload the new file, `build_studio.py`, publish, `build_project.py`, replace `03-image-library.md`.
- **A new approved banner job** becomes a pattern: add it to `PATTERNS` in `build_kit.py`, to `src/skills/katapult-patterns/SKILL.md` and to `04-brief-intake.md` past jobs, then rebuild everything above.
- Rules changed (voice, legal, photography): edit `src/`, `build_project.py`, replace the changed file in the Project.
