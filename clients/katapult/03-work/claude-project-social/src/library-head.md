# Katapult photos and product cutouts

Every image a Katapult frame may use. You cannot see them: choose by the description, then give the person the id so they can check it in Katapult Social Studio (Photos and products tab) or in the Image Library (https://claude.ai/code/artifact/bc252c47-7c82-4376-ba50-383a10c1a576).

In a post file a photo is `data-img="library:ID"` and a cutout `data-img="product:ID"`. Anything else is `upload:FILE` with a file the person drops in the Studio.

## Rules

1. **Only these ids, or an `upload:` file the person has.** Never generate, source or link another image. A missing image is a request to the client or the art director.
2. **People lead.** Pick photos where a real person is uplifted by, or using, what they got. Match the subject to the message: appliances with a kitchen or dishwasher photo, electronics with a laptop or phone photo, furniture with a sofa photo.
3. **Brand fit.** `on-brand` first. `with care` only when the description fits the message better than any on-brand photo, and say why. `no people` rooms never as the main image.
4. **Copy space.** Each photo lists where copy can sit. Full-bleed layouts (T01, T09, P2) need the face clear of the copy zone: set `data-pos` to move the crop.
5. **Crop per size.** The same photo can serve every size of a job (one master image per concept), each with its own `data-pos`. Wide sizes (1200x628, 728x90, 16x9) need the subject near the centre or set with `data-pos`.
6. **Products at true scale.** A fridge is taller than a washer, headphones are small. Use `data-scale` so a set of three reads at believable relative sizes.
7. **Rights:** the photos are Adobe Stock; the licence is being confirmed. Note "stock licence to confirm" in the hand-off for paid media.

## Library photos

`face at` is where the main face sits in the photo (X% across, Y% down). The Studio uses it as the default crop; see `data-pos` in `02-studio-kit.md`.

| id | size | what it shows | people | face at | copy space | best use | brand fit | notes |
|---|---|---|---|---|---|---|---|---|
