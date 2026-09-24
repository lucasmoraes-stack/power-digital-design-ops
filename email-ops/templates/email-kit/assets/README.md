# Assets do kit de e-mail

Os arquivos desta pasta no template são **amostras neutras**: faixas cinza com um rótulo em monospace (`HERO 600x380`, `PORTRAIT 1`...) e um logo de texto `BRAND`. Existem só para o template renderizar. Num kit de marca, todos são substituídos por arquivos reais antes de o kit ir para aprovação.

Para trocar um asset: salvar o arquivo real com o mesmo nome **ou** salvar com outro nome e atualizar o caminho no grupo `assets` do `tokens.json`. Depois rodar `build_kit.py` de novo.

## Lista obrigatória

Tamanho do arquivo sempre em **2x** do tamanho de exibição.

| Token (`assets.`) | Arquivo de amostra | Exibição | Arquivo (2x) | Formato | Peso máx. | Usado em |
|---|---|---|---|---|---|---|
| `logo_light` | `logo-light.png` | 120x50 | 240x100 ou maior, mesma proporção | PNG transparente | 30 KB | E01 (fundo claro) |
| `logo_dark` | `logo-dark.png` | 120x50 e 200x84 | 400x167 | PNG transparente | 30 KB | E01 no dark mode, E13 |
| `hero_photo` | `sample-hero.jpg` | 600x380 | 1200x760 | JPG 70-80 | 150 KB | E02 |
| `hero_photo_card` | `sample-card.jpg` | 560x600 | 1120x1200 | JPG 70-80 | 150 KB | E15 |
| `feature_photo` | `sample-feature.jpg` | 600x350 | 1200x700 | JPG 70-80 | 150 KB | E10 |
| `texture_light` | `texture-light.jpg` | 600x440 | 1200x880 | JPG 70-80 | 60 KB | E03 |
| `texture_dark` | `texture-dark.jpg` | 600x400 | 1200x800 | JPG 70-80 | 60 KB | E13 |
| `portrait_1..3` | `portrait-1.jpg` ... `portrait-3.jpg` | 112x112 e 44x44 | 240x240, quadrado | JPG 70-80 | 20 KB | E07, E12 |
| `product_1` | `product-1.png` | 180x180 e 104x104 | 400x400, quadrado | PNG transparente | 80 KB | E04, E07 |

Teto do e-mail inteiro: cerca de **800 KB** somando todas as imagens. Se um e-mail passar disso, recomprimir antes de cortar módulo.

## Logo claro e logo escuro

- Sempre as duas versões, rasterizadas do **vetor oficial** (nunca de um print ou JPG).
- `logo_light`: a cor do logo para fundo claro. `logo_dark`: a versão para fundo escuro (normalmente branca ou a cor clara oficial).
- Mesma largura, altura e área de respiro nas duas, para a troca no dark mode não mexer no layout.
- Fundo transparente, sem sombra, sem borda. O Gmail inverte cores sozinho: um logo escuro transparente sem versão clara some no dark mode.
- Proporção diferente de 120x50: ajustar `logo_width`, `logo_height`, `logo_large_width` e `logo_large_height` no `tokens.json`.

## Fotografia

- Só fotos do banco aprovado da marca, seguindo a regra de fotografia registrada no README do kit (fonte: style guide ou toolbox).
- Sem banco de imagem genérico com cara de IA, sem ilustração decorativa, sem clip-art.
- Recortar no tamanho exato do módulo. O E15 precisa de uma foto com área calma no topo (céu, parede, fundo liso), porque a headline fica em cima dela.
- Texto nunca embutido na imagem. Exceção única: o logo sobre a foto do E02, com o nome da marca no `alt`.
- Todo `alt` descreve a foto real (token `*_alt` no `tokens.json`); retrato decorativo no E12 usa `alt=""`.
- Sem foto aprovada ainda: manter o placeholder listrado com rótulo, nunca uma foto "de exemplo" que possa ir ao ar.

## Texturas e gradientes

- Gradiente de marca vira **JPG** (nunca `linear-gradient` em CSS). Cada textura tem uma cor sólida de fallback no `tokens.json` (`color.texture_fallback`, `color.texture_dark_fallback`) que mantém o texto legível sozinha.

## Nomes

- kebab-case, em inglês, sem espaço nem acento: `logo-light.png`, `hero-welcome.jpg`, `portrait-2.jpg`, `product-starter-kit.png`.
- Apagar os arquivos `sample-*` quando os reais entrarem, para nenhum placeholder ser exportado por engano.
- Na exportação para o ESP, os caminhos relativos `assets/...` viram URL absoluta da CDN do ESP.
