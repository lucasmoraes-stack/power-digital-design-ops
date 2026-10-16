# Katapult branding

Brand source of truth, fed from the Katapult Brand Guidelines (v1.3, June 2022) and, for tokens and basic elements, the [Figma Library style guide](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab?node-id=74-7772) — which wins where the two disagree.

**Social layouts start here (2026-10-13):** every Katapult social piece is built from the ten approved templates in [`templates/`](templates/README.md) (Figma "Progressive Global - LAB", node 547:1042, 10 layouts x 1:1/4:5/16:9/9:16, rebuilt one to one in HTML and shown in the Templates section of the Design System, headlines in Aktiv Grotesk Regular). The template sets below are history.

The same Figma Library also holds ready-made design templates for Katapult, under [node 251:480](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab?node-id=251-480) ("/templates - Katapult") — 11 branded layout patterns, on-brand with real approved copy already in place. Designer's brand section links to this. (An older node, `178:1377`, was cited here previously — confirmed gone as of 2026-09-10, don't use it.)

A second, separate batch of generic 1:1 templates lives under [node 234:192](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab?node-id=234-192) ("templates" section) — 11 layout patterns modeled directly on real top-performing competitor ads sourced from the Meta Ad Library (Affirm, Klarna, Snap Finance, Progressive Leasing, Afterpay), each frame named `template-NN-<pattern-slug>`. A parallel reference row below the templates keeps the original competitor screenshot each one was modeled on; a shared assets row (node 234:191) holds the placeholder product cutouts, hand+phone shot, and lifestyle photo the templates duplicate from. Only 1:1 exists so far in this generic batch — other aspect ratios are a future pass. (The separate Katapult-branded copy at `251:480` got its first reframe test on 2026-09-10: `template-04-product-row-3up` now also exists at 4:5/16:9/9:16 — see `designer.md`'s Figma-execution discipline notes for what that surfaced.) Known gaps: all text added by agents in this batch used Inter as a stand-in (Aktiv Grotesk isn't loadable via the Figma plugin API in this tooling) and needs a manual font swap in Figma desktop before use; no full-person/torso lifestyle photo exists yet in the shared assets (template-07 substitutes the hand+phone shot for it).

## Team production: Katapult Social Studio

Designers outside this repo make Katapult posts and banner jobs in the **Katapult Social Studio** Claude Project (brief PDF in, post file out) and render them in the Social Studio artifact (https://claude.ai/code/artifact/5a137796-2f13-4690-8ce2-45fd9f4c8cdc). The package, its builders and the upkeep steps are in [`../03-work/claude-project-social/`](../03-work/claude-project-social/README.md). Templates, banner patterns and Image Library photos feed it: change one, rebuild the package.

## Files

- `identity/brand-guidelines.md` — master digest of the full guidelines. Brand Guardian reads this directly.
- `references/` — layout references. Holds the ad banner templates (1:1 and 9:16) and `banner-layout.md`, the spec for the banner sequence. (Separate from the Figma Library templates above — these are the original IAB-banner-specific spec, from a different Figma file.)

## Where Katapult's rules live in the agent team

Katapult isn't cut into separate per-agent brief files — its rules are baked directly into the "## Katapult" section of each relevant agent, in [.claude/agents/](../../../.claude/agents/):

- **Brand Guardian** reads this folder's `identity/brand-guidelines.md` in full.
- **Copywriter** carries Katapult's voice, message, proof points, and testing angles in its own "## Katapult" section.
- **Designer** carries Katapult's palette, photography rules, graphic language, and banner production spec in its own "## Katapult" section.

The `brand-guidelines.md` digest is the operation's working source. To keep the original on hand, drop the source PDF (Katapult Brand Guidelines v1.3, June 2022) into a `source/` folder here when available.
