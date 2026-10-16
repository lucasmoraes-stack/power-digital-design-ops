# Katapult social templates

The base for every Katapult social piece (Meta, Instagram). Ten approved layouts, each in four ratios, rebuilt one to one from Figma.

- **Source of truth:** Figma "Progressive Global - LAB", section "/templates - Katapult", [node 547:1042](https://www.figma.com/design/D8FpNuKI3uPGjCPqonIn3C/Progressive-Global---LAB?node-id=547-1042).
- **Published in:** the Templates section of the Katapult Design System, https://claude.ai/code/artifact/ee8bd24b-c2e4-4f39-b14b-4523c87c4704#templates (headlines in Aktiv Grotesk Regular). The old standalone page https://claude.ai/code/artifact/2b191289-c639-44c6-9dfd-a71ec98df407 now only points there.
- **Ratios:** 1:1 (1200x1200), 4:5 (1080x1350), 16:9 (1920x1080), 9:16 (1080x1920).

| ID | Layout | Use it for | Imagery |
|---|---|---|---|
| T01 | Full image | A strong lifestyle photo with a calm lower third | Lifestyle photo, full bleed |
| T02 | Split panel, image | A three-beat headline and a tall photo crop | Lifestyle photo, half frame |
| T03 | Split, phone in hand | App and how-it-works messages | Hand holding the app |
| T04 | Product row, 3-up | Category or gear messages with several products | Three product cutouts |
| T05 | Hero product, bleed | One hero product, warm conversational headline (Cream) | One large product cutout |
| T06 | Top block, photo card | Home and lifestyle messages, photo as proof (Pink) | Lifestyle photo, rounded card |
| T07 | Top block, product on circle | One product launch or tech message (Pink) | One product cutout |
| T08 | Typographic statement | Brand or manifesto messages | None |
| T09 | Hero photo, full width | Big photo, short headline, last word in Pink | Lifestyle photo, bottom half |
| T10 | Product trio, circles | Roundups with exactly three products | Three product cutouts |

## How to make a piece

1. Pick the template by the imagery you have and the message.
2. Copy `html/<tNN>-<ratio>.html` into the job folder (`03-work/social/<job>/`), swap the copy and the image `src`. Keep every position, size and spacing, the pill CTA, the logo and the disclaimer where the template puts them.
3. Long copy: rebreak lines, then widen the box if there is room, and only then step the size down.
4. Export at native size: `chrome --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=<w>,<h> --screenshot=out.png file:///.../frame.html`.

Type: the Figma frames use Inter only because the Figma plugin cannot load Aktiv Grotesk. The HTML renders in Aktiv Grotesk; add `#inter` to a frame URL to compare with Figma.

## Files

- `figma/<slug>.jsx`: get_design_context output, saved verbatim. `figma/assets/` and `figma/ref/` (Figma renders) stay on disk, outside git.
- `tw2css.py`: converts that code to HTML with inline CSS (fails loudly on any unknown class).
- `build_templates.py`: writes `html/` and `ds-templates-section.html` (headlines set to Regular 400); `inject_ds.py <ds_in> <ds_out>` puts that section into the DS page; `python build_templates.py check` puts Figma and HTML side by side in `qa/`.
- Figma's Button instances are scaled to 446px wide; the builder applies that scale with `zoom` (and compensates absolute offsets).

## Downstream: Katapult Social Studio

These frames are also the layouts of the Katapult Social Studio (Claude Project + Make PNG artifact), in `../../03-work/claude-project-social/`. After any template change, rebuild that package as its README says (`build_kit.py`, upload new images, `build_studio.py`, publish, `build_project.py`, replace `02-studio-kit.md` in the Project).
