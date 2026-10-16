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
| `phone-man-street-phone-01` | 4000x6000 | Man in a dark jacket smiling at his phone on a city street | one man, face upper middle | 55% 18% | none (brick and storefront behind) | story or portrait post, person-led static | on-brand |  |
| `laptop-woman-sofa-laptop-01` | 6552x4396 | Woman on a white sofa with a laptop, bright living room | one woman, right third | 73% 22% | left (white room) | landscape banner with copy left, blog header | on-brand |  |
| `phone-woman-dog-phone-02` | 8639x4860 | Woman in glasses and an orange top laughing at her phone, dog on the sofa | one woman centre, dog bottom left | 50% 22% | top (white wall, narrow) | wide banner, organic static | on-brand | orange top echoes Katapult Orange |
| `phone-man-green-sofa-phone-03` | 4096x2160 | Man in a light blue shirt on a green sofa, smiling at his phone | one man centre, high | 48% 18% | top left (shelves, soft) | wide banner (4096 x 2160) | on-brand | light blue shirt echoes Light Blue |
| `phone-woman-lamps-phone-04` | 4881x6101 | Curly-haired woman in a blue striped shirt checking her phone, warm lamps | one woman centre | 45% 25% | top left | portrait post, story | on-brand | foreground leaf blur bottom right |
| `at-home-woman-sofa-coffee-01` | 6000x4000 | Woman in a striped tee with coffee on a cream sofa, eyes closed, warm light | one woman, right third, eyes closed | 72% 35% | left and top (sofa, wall) | furniture post, calm moment | with care | eyes closed, calm rather than fun |
| `laptop-woman-desk-laptop-02` | 6240x4160 | Woman smiling over a laptop and mug at a home desk | one woman centre, laptop in front | 50% 22% | both sides (shelves, plant) | square or 4:5 crop centered | on-brand |  |
| `together-couple-sofa-phone-laptop-01` | 5333x3000 | Couple on a sofa, she on her phone, he on a laptop, mugs on the table | two people right of centre, wall above | 62% 42% | top (wide white wall) | banner or post with copy on top | on-brand | strong text space |
| `retail-man-tire-dealership-01` | 6000x4000 | Man crouching to check a car tire in a dealership | one man right, car left | 63% 25% | none (busy showroom) | tires and wheels category | with care | looks down, face partly turned |
| `together-friends-gaming-sofa-02` | 5930x2541 | Two friends laughing on a green sofa with game controllers | two people small, right of centre | 62% 23% | left (large wall) | wide banner with copy left, gaming and electronics | on-brand | people small in frame |
| `phone-woman-card-phone-05` | 8192x5464 | Woman in glasses holding her phone and a payment card, big smile | one woman left third, close-up, phone and card in hands | 35% 30% | right (soft background) | checkout and payment moment, hero | on-brand | top pick for checkout copy |
| `laptop-woman-blanket-laptop-03` | 4004x6006 | Blonde woman with a laptop on the sofa under a yellow blanket, lamp behind | one woman left of centre | 40% 25% | top (lamp, wall) | portrait post, story | on-brand |  |
| `retail-shop-owners-tablet-02` | 4672x7008 | Two shop owners in aprons with a tablet in a kitchenware store | two people centre, high | 52% 20% | none (busy shelves) | retailer and merchant posts | with care | busy background |
| `at-home-senior-woman-armchair-02` | 2572x3430 | Older woman in green pajamas relaxing in an armchair, smiling | one woman centre | 50% 25% | top right (white wall) | furniture and comfort posts | on-brand | age range |
| `phone-man-call-tablet-sofa-06` | 8924x4706 | Grey-haired man on a phone call holding a tablet on a white sofa | one man left third | 35% 20% | none strong | wide banner, electronics | on-brand | age range |
| `at-home-woman-pendant-lamp-03` | 4324x6487 | Woman from behind adjusting a pendant lamp in a living room | one woman from behind, face not visible | 42% 20% | top left (white wall) | home decor and lighting | with care | face not visible |
| `room-leather-sofa-room-01` | 6000x7200 | Brown leather sofa with a plant in a sunny room, no people | no people | none | top (wall) | furniture product background only | no people | guideline: never the main image |
| `phone-man-kitchen-phone-07` | 9504x6336 | Man in a denim jacket smiling at his phone in a kitchen | one man right of centre | 55% 25% | left (shelves, soft) | landscape post, banner | on-brand |  |
| `laptop-woman-tablet-counter-04` | 4096x2160 | Woman with a tablet at a kitchen counter, warm low sun, dark cabinets | one woman centre | 48% 30% | top left (dark cabinets) | banner with light text on dark | with care | darker scene |
| `phone-man-window-phone-08` | 3397x5095 | Bearded man in a green shirt with his phone by a window, looking away smiling | one man centre, looking away | 45% 20% | top (dark wall) | portrait post, story | with care | low light, close to moody |
| `phone-woman-headphones-selfie-09` | 4672x7008 | Woman in a red sweater and headphones laughing at a yellow phone, outdoors | one woman right of centre | 65% 22% | top (blurred street) | story, fun organic post | on-brand | most energetic photo |
| `at-home-woman-beanbag-mug-04` | 5472x3648 | Woman in a beanbag holding a mug by a window, warm light | one woman right, mid height | 65% 45% | left (blinds, curtain) | comfort and furniture posts | with care | darker, calm |
| `laptop-man-sofa-coffee-laptop-05` | 5760x3840 | Man with coffee and a laptop on a grey sofa, bright window | one man centre | 53% 30% | left and top (window) | wide banner with copy left | on-brand | duplicate download removed |
| `together-family-homework-sofa-03` | 6720x4480 | Parents helping their daughter with homework at a coffee table, orange sofa | three people centre | 55% 30% | top right (wall, narrow) | family posts, back to school | on-brand | orange sofa |
| `together-couple-hug-laptop-04` | 4480x6720 | Couple hugging on a sofa with a laptop, kitchen lights behind | two people centre, mid height | 55% 42% | top (ceiling, lights) | portrait post, relationship moment | on-brand |  |
| `laptop-woman-window-desk-06` | 6720x4480 | Woman writing at a desk with a laptop, bright window, profile view | one woman right of centre, profile | 62% 33% | left (window) | banner with copy left | on-brand | profile, face visible |
| `at-home-woman-dishwasher-05` | 7952x5304 | Woman loading a dishwasher in a blue kitchen, smiling | one woman right of centre, very high | 60% 15% | top left (tiles) | appliances category | on-brand | appliance in use |
| `phone-senior-woman-call-10` | 8192x5464 | Older woman in glasses laughing on a phone call, tablet on the table | one woman right of centre | 58% 25% | none strong | landscape post, age range | on-brand |  |
| `unboxing-kids-moving-box-01` | 6720x4480 | Kids playing in a moving box while a parent carries a lamp | kids centre, parent's face cropped | 50% 40% | none (busy) | moving and new home posts | on-brand | parent face cropped, kids lead |
| `unboxing-woman-unboxing-sofa-02` | 6720x4480 | Woman in an orange tee thrilled while opening a box on her sofa | one woman centre, box bottom left | 52% 28% | top (shelves, soft) | delivery and unboxing hero | on-brand | top pick, orange echoes the palette |
| `at-home-woman-daybed-plants-06` | 6240x4160 | Woman lounging on a daybed among plants, soft lamp light | one woman small, left | 35% 45% | top (window, plants) | wide banner, home decor | with care | subject small, dim |
| `laptop-woman-tablet-orange-sofa-07` | 5472x3648 | Curly-haired woman in a yellow striped sweater laughing at a tablet, orange sofa | one woman right of centre, close | 58% 30% | top left (window) | landscape post, story crop | on-brand |  |
| `together-couple-tablet-mug-05` | 4739x3164 | Couple close on a sofa, he reads a tablet, she holds a mug | two people right of centre | 62% 30% | top (window) | relationship moment | with care | soft foreground blur |
| `together-senior-couple-kitchen-06` | 7934x5292 | Older couple chatting in a blue kitchen, fridge and oven visible | two people small, centre | 55% 25% | top (shelves) | appliances category, age range | on-brand | people small in frame |
| `at-home-woman-headphones-relax-07` | 5760x3840 | Woman in headphones relaxing in a chair, eyes closed | one woman left, eyes closed | 30% 25% | right (wall) | audio and electronics | with care | eyes closed |
| `room-orange-armchair-room-02` | 3456x5184 | Orange armchair and floor lamp against a brick wall, no people | no people | none | top (wall) | furniture product background only | no people | guideline: never the main image |
| `laptop-woman-tablet-laughing-08` | 6118x4032 | Woman laughing with a tablet on a grey sofa, orange pants | one woman centre | 50% 35% | top right (shelves) | landscape post, banner | on-brand |  |
| `laptop-man-glasses-laptop-09` | 6720x4480 | Man in glasses smiling with a laptop on a sofa, flowers in the foreground | one man centre | 52% 25% | top (wall, plant) | landscape post | on-brand |  |
| `together-friends-cooking-07` | 7934x5292 | Friends cooking together in a kitchen, rolling dough | three people across the frame | 55% 25% | none (busy) | kitchen and appliances, group | on-brand | busy frame |
| `retail-business-owner-workshop-03` | 4096x2160 | Small business owner in a blue blazer, arms crossed, in her workshop | one woman centre, very high | 48% 15% | none (busy) | retailer and merchant posts | on-brand |  |
| `room-blue-fridge-kitchen-03` | 6000x4000 | Light blue retro fridge in a white kitchen, no people | no people, fridge centre left | none | right (white wall) | appliance product background only | no people | fridge matches Light Blue; never the main image |
| `phone-senior-man-phone-11` | 4565x6847 | Grey-haired man in a green shirt smiling at his phone on a sofa | one man centre | 45% 40% | top (white wall) | portrait post, story, age range | on-brand |  |
| `phone-woman-kitchen-phone-12` | 6000x4000 | Woman in a kitchen smiling at her phone, holding a juice | one woman centre | 50% 25% | left (dark cabinets) | landscape post, banner | on-brand |  |
| `laptop-man-bed-laptop-10` | 3693x5539 | Young man in glasses lying on a bed with a laptop and earbuds, brick wall | one man centre, lying down | 45% 45% | top (brick wall) | portrait post, story | on-brand |  |

## Product cutouts

Transparent cutouts for product slots (T04, T05, T07, T10). `front` view sits upright; `top-down` view was shot from above for flat-lays and reads oddly upright in a template.

| id | what it is | view |
|---|---|---|
| `headphones` | Over-ear headphones, lilac | front |
| `tablets` | Three tablets in a row, purple | front |
| `laptop-open` | Open laptop, green screen | front |
| `laptop` | Open laptop, silver | top-down |
| `fridge` | French-door fridge, steel | front |
| `washer` | Front-load washer, white | front |
| `tv` | Flat TV | front |
| `tire` | Tire on alloy wheel | front |
| `console` | Game console and controller | top-down |
| `vacuum` | Stick vacuum | front |
| `nightstand` | Wooden nightstand | front |
| `necklace` | Gold necklace | top-down |
| `couch` | Three-seat couch, grey | top-down |
| `bed` | Bed with green throw | top-down |
| `grill` | Kettle grill | top-down |
