# Fotos do Mosquito Season: prompts pro ChatGPT (v2, com continuidade)

Na primeira rodada cada imagem foi gerada do zero, e quintal, casa e família mudavam de uma cena pra outra. Agora tudo sai de **2 imagens-mestre**, uma por cenário. As outras são **edições** da mestre. Anexe a imagem indicada e cole o prompt: o cenário, a câmera e as pessoas se mantêm, e só o momento muda.

- **Cenário A, o pátio** (V1 e V2). Mestre: `v2-curfew`.
- **Cenário B, a casa** (V3). Mestre: `v3-house`, a que já existe. Ela fica.

Todas em 4:5. Salve em `img/` com o nome indicado, substituindo o arquivo antigo.

## Ordem

| # | Arquivo | Anexar | Momento |
|---|---|---|---|
| 1 | `v2-curfew` | nada (é a mestre) | pátio vazio, mesa posta, entardecer |
| 2 | `v1-dinner` | v2-curfew | a família chega e janta |
| 3 | `v1-lawn` | v1-dinner | crianças no gramado, pais à mesa |
| 4 | `v1-night` | v1-dinner | mesma cena, já de noite |
| 5 | `v2-retreat` | v1-dinner | jantar abandonado, família entrando em casa |
| 6 | `v2-night` | v1-night | família de volta à mesa, de noite |
| 7 | `v3-shrubs` | v3-house | mesmo quintal, câmera nos arbustos |
| — | `v3-night` | v3-house | opcional: a atual já bate com a casa |

## Cenário A: o pátio

**1. v2-curfew (mestre, gerar do zero)**
```
Photorealistic lifestyle photograph, vertical 4:5. Suburban American backyard patio just after sunset, amber and deep blue sky. Fixed set, simple and readable: a stone paver patio in the center with one round wooden dining table and four cushioned wooden armchairs; the table set for dinner with four plates, glasses and a black lantern with a candle in the center. On the right, a wooden pergola attached to the back of a light cream house, with a glass French door under it. Warm string lights run from the pergola across the patio to a wooden post on the left. A tall wooden privacy fence in the background with shrubs and white hydrangeas. A strip of green lawn in the lower left foreground. Nobody in the scene. Camera at standing eye level, slightly elevated, facing the table. Center the table with at least 12% clear margin on every edge, nothing important touching or cropped. Leave a clean dark area of sky in the upper third for a clock graphic. No text, no clocks, no logos, no insects, no spray equipment.
```

**2. v1-dinner (anexar v2-curfew)**
```
Edit the attached image. Keep the exact same backyard, camera angle, time of day, lighting, furniture, table setting, pergola, French door, fence and string lights. Change only: add this family of four seated at the table, eating and laughing, glasses raised, food on the plates. A father in his late 30s with a short dark beard and a navy button-up shirt; a mother in her late 30s with long wavy light-brown hair and a white sleeveless dress; a girl about 8 with a brown ponytail and a yellow top; a boy about 10 with short dark hair and a light blue T-shirt. Warm, carefree, nobody swatting. Vertical 4:5. At least 12% clear margin on every edge, nothing important touching or cropped by the frame. Photorealistic, natural, cinematic. No text, no clocks, no logos, no insects, no spray equipment.
```

**3. v1-lawn (anexar v1-dinner)**
```
Edit the attached image. Same backyard, same family, same clothes, same time of day and lighting. Change the moment: the girl and the boy are now playing with a soccer ball on the lawn in the lower left foreground, running and laughing; the parents stay at the table in the background, relaxed with drinks. Turn the camera slightly to the left to show more of the lawn, same height. Vertical 4:5. At least 12% clear margin on every edge, nothing important touching or cropped by the frame. Photorealistic, natural, cinematic. No text, no clocks, no logos, no insects, no spray equipment.
```

**4. v1-night (anexar v1-dinner)**
```
Edit the attached image. Same backyard, same framing, same family and clothes. Change only the time: it is now full night, deep blue sky with a few stars, string lights and lantern glowing brighter. The family is still at the table, relaxed, with dessert and drinks. Keep a clean open area of night sky in the upper center for a shield icon. Vertical 4:5. At least 12% clear margin on every edge, nothing important touching or cropped by the frame. Photorealistic, natural, cinematic. No text, no clocks, no logos, no insects, no spray equipment.
```

**5. v2-retreat (anexar v1-dinner)**
```
Edit the attached image. Same backyard, same framing, same furniture. Change the moment: the dinner has been abandoned. Nobody at the table; plates half finished, one chair pushed back, a napkin on the patio floor, a red cup tipped over. The French door under the pergola is open with warm light inside, and the same family is seen from behind walking into the house through it. The sky is a little darker than in the attached image. Keep a clean dark area of sky in the upper third for a clock graphic. Vertical 4:5. At least 12% clear margin on every edge, nothing important touching or cropped by the frame. Photorealistic, natural, cinematic. No text, no clocks, no logos, no insects, no spray equipment.
```

**6. v2-night (anexar v1-night)**
```
Edit the attached image. Same backyard, same framing, same night lighting, same family and clothes. Change only the family's poses: they are back outside after a while, the father refilling glasses, the mother laughing with the kids, fresh candles on the table, relaxed and comfortable. Keep a clean open area of night sky in the upper center for a shield icon. Vertical 4:5. At least 12% clear margin on every edge, nothing important touching or cropped by the frame. Photorealistic, natural, cinematic. No text, no clocks, no logos, no insects, no spray equipment.
```

## Cenário B: a casa

**7. v3-shrubs (anexar v3-house)**
```
Edit the attached image. Same yard, same house, same dusk light and sky. Move the camera closer to the left side of the yard: frame the big shaded tree, the dense shrubs and hydrangeas along the fence and the stone birdbath, with the house and deck softly out of focus in the right background. Humid summer evening feeling. Keep open space above the shrubs for mosquito graphics. No people. Vertical 4:5. At least 12% clear margin on every edge, nothing important touching or cropped by the frame. Photorealistic, natural, cinematic. No text, no clocks, no logos, no insects, no spray equipment.
```

**v3-night (opcional, anexar v3-house)**
```
Edit the attached image. Same house, same yard, same framing. Change only the time: full night, deep blue sky with a few stars, warm window light, string lights and landscape lights glowing. No people. Keep a clean open area of night sky in the upper center for a shield icon. Vertical 4:5. At least 12% clear margin on every edge, nothing important touching or cropped by the frame. Photorealistic, natural, cinematic. No text, no clocks, no logos, no insects, no spray equipment.
```

## Dica

Faça todas as edições na mesma conversa do ChatGPT e anexe sempre a imagem indicada, mesmo que ela já esteja na conversa. Se a edição mudar o rosto de alguém, peça "keep the faces exactly as in the attached image".
