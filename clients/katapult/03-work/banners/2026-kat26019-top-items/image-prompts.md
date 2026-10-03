# KAT26019 Top Items: prompts dos recortes (ChatGPT)

Knolling = objetos vistos de cima (ou de frente, reto), alinhados em ângulo reto, sem sombra dramática. Cada item sai como **um PNG separado, fundo transparente**, pra o V2 poder trocar os itens de célula.

Regras pra todos: mesma luz, mesma câmera, mesma escala relativa. Sem texto, sem marca, sem logo de varejista. Salvar em `img/{item}.png`, quadrado 1200x1200.

## Prompt base (colar e trocar só o `[ITEM]`)

```
Product cutout photograph of [ITEM], shot straight-on, perfectly level and centered, as part of a knolling flat-lay set. Clean studio lighting from the top left, soft and even, a very soft contact shadow only. True colors, no filters, no heavy color grading. Transparent background (PNG with alpha). The object fills about 80% of the square frame with even margin on every side, nothing cropped. No text, no logos, no brand names, no price tags, no people, no props.
```

## Itens

| Arquivo | [ITEM] |
|---|---|
| `sofa.png` | a modern three-seat fabric sofa in warm light grey with two seat cushions, slim wooden legs, front view |
| `tv.png` | a large flat-screen TV with a thin black bezel on a slim stand, screen off with a subtle reflection, front view |
| `tire.png` | a new car tire on a silver alloy wheel, side view so the full circle and tread edge show |
| `fridge.png` | a stainless steel French-door refrigerator with bottom freezer drawer, front view |
| `mattress.png` | a white quilted queen mattress seen from a low three-quarter front angle, clean and new |
| `laptop.png` | an open silver laptop, screen on with a plain soft-blue gradient, front three-quarter view |
| `washer.png` | a white front-load washing machine with a round glass door, front view |
| `console.png` | a black video game console with one matching wireless controller beside it, top-down view |
| `grill.png` | a black kettle charcoal grill with lid on and three legs, front view |

Quando os PNGs chegarem, o `build.py` troca o placeholder de cada célula pelo recorte (mesmo nome do item).
