---
name: figma-banner-sync
description: How to bring visual changes Lucas made in Figma back into the HTML banner jobs and republish them in a client's Deliverables Hub without losing anyone's edits. Load when asked to "update the creatives with what we did in Figma", sync a hub with a Figma page, or rebuild a banner job from Figma frames.
---

# Figma → HTML banner sync

Proven on Katapult 2026-10-13 (4 jobs, 64 frames, matched to within ~1px).

## 1. Map the Figma page

- `get_metadata` on the page node; the dump is big, so save it and list sections and frames by name (`KAT260NN - <job> - V1 - 1x1`, etc.). Note duplicates stacked at the same position (the top-most is the live one) and hidden layers (`hidden="true"` stays out).
- `get_screenshot` per section, then render the current hub/export for the same frames and put them side by side. Write down the visible differences per job before touching code.

## 2. One agent per job, in parallel

Each job owns separate files (`kNN.css/html/js`, `build.py`, `export.py`, its `img/`), so jobs can run in parallel without conflicts. Give each agent: the Figma node ids for every frame of its job, the visible differences, the published hub file to test on, and a scratch output folder. Rules for the agent:

- Read `skill://figma/figma-design-to-code/SKILL.md` before `get_design_context`; take exact values per frame (drill into children if sparse) and download every image asset Figma uses (new cutouts, the real photo, textures).
- Keep the job's architecture; translate Figma values into its per-size layout. Don't paste Figma's React/Tailwind.
- Never touch `04-deliverables/` or publish; build and export into scratch.
- **Match the render, not the node tree.** Compare rendered ink row by row with the Figma screenshot; node coordinates and browser glyph placement can be off by up to 11px.
- Report files changed, per-size before → after, what could not be matched, and generalizable LEARNINGS (they feed `banner-craft` and the brand's banner skill).

## 3. Assemble on the newest published hub

The published artifact is the source of truth and other sessions may be editing it.

1. `read` the hub artifact right before building. Diff it against the version you started from; carry anything new.
2. Run the builds in a chain on that file, each output feeding the next (Katapult: `build_kn.py` → KAT26020 `build.py` → KAT26021 `build.py` → KAT26022 `build.py`). Every build replaces only its own marked blocks; check that tab counts, job order and nav came through untouched.
3. Export every job from the final hub into scratch, make a contact sheet, look at it.
4. `read` again immediately before publishing. If it changed, rebuild on the new version. Never `force`.
5. Publish to the same URL. Copy the published HTML back to `04-deliverables/deliverables-hub.html` and replace each job's `html/` folder and zip in `04-deliverables/banners/<job>/` with the new exports (delete the old folder first so renamed frames don't linger).

## 4. Close the loop

- Update the hub entry in `hub/artifacts.json` (counts, date) and the Power Digital Hub if counts changed.
- Fold the agents' learnings into `.claude/skills/banner-craft` (general) and the brand's banner skill (brand-specific values), and list open questions for Lucas instead of guessing (palette conflicts, stretched assets in Figma, copy differences against the brief).
