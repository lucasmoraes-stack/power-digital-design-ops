# Roku — client of Power Digital

Client onboarded under PowerDigital Lab. Roku's advertiser-facing product ("Roku Ads Manager") is promoted to B2B media buyers through holiday-season CTV ad campaigns — the work here is production support on that ad creative, not brand strategy or copywriting.

## Current scope

First deliverable: reframe already-approved 16:9 ad creative into 9:16 and 1:1, across every section of one Figma file. Copy and layout are fixed (client-approved); the job was recomposing backgrounds, text, and decorative elements to the new aspect ratios, not rewriting anything.

- **Figma file:** [Claude Design Ops - Lab](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab) (`pcf9QNPjvBBzqDPnBLefVS`)
- **Sections reframed** (all 5, done):

  | Section | Format | Scenes |
  |---|---|---|
  | V1: MOF Ad - MOBITE | video storyboard | 23 |
  | V1: MOF Ad - CAROUSEL | static carousel | 7 |
  | V1: MOF Ad - CAROUSEL - Version 2 | static carousel | 7 |
  | V2: BOF Retargeting Ad - MOBITE | video storyboard | 17 |
  | V2: BOF Retargeting Ad - CAROUSEL | static carousel | 7 |

  61 scenes × 2 new formats = 122 new frames, built directly in the Figma file (no local export — Figma is the deliverable).

- **New frame sizes:** 9:16 at 1440×2560, 1:1 at 1440×1440 (kept on the same "1440" scale as the 2560×1440 16:9 masters, no resampling factor between formats).
- **Safe text margin (9:16 only):** nothing may sit in y=0–267 (top) or y=2227–2560 (bottom) — scaled up from the client's 250px-bottom/200px-top brief at 1080-wide convention. 1:1 has no mandated margin.
- Inside each section, the two new frame rows sit directly below the original 16:9 row, named `9x16 - Scene NN (src {original-node-id})` / `1x1 - Scene NN (src {original-node-id})`, so the source scene for every new frame is traceable from the name alone.

## Structure

```
roku/
├── README.md                              this file
├── 00-inbox/                               (empty — no client-supplied files yet)
├── 01-brand/
│   └── identity/
│       └── brand-notes.md                 visual identity observed while reframing (not a full ingestion)
└── 03-work/
    └── figma-reframe-playbook.md          technique playbook from the reframe session — font-lock workarounds,
                                             Figma Plugin API bugs and fixes, composition judgment calls, orchestration notes
```

## Status / next steps

- [x] All 5 sections reframed to 9:16 and 1:1, validated with screenshots scene by scene.
- [ ] Open the file in the Figma desktop app with the real "Roku Display" font installed and spot-check the text — every text node in the reframe was only repositioned/rescaled, never had `characters`/font edited, precisely because that font isn't loadable in the plugin sandbox this session ran in. It should render correctly, but hasn't been visually confirmed with the real typeface.
- [ ] A handful of scenes required an art-direction judgment call (which of two overlapping texts is the "active" one, whether a decorative element is intentional or transition leftover, etc.) — worth a human pass. Each call is documented inline in this session's chat history; nothing was left ambiguous without a documented reason.
- [ ] If this reframe pattern gets reused for another client, consider promoting the reusable parts of `03-work/figma-reframe-playbook.md` into a shared, client-agnostic location (e.g. a `playbooks/` folder at the root of this repo) — it's currently filed under Roku only because it's only been used on this one client so far.
