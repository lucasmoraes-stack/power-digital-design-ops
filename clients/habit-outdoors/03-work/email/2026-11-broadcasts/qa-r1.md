# QA rodada 1 · November 2026 broadcasts (2026-10-07)

Email QA Reviewer. Veredito: **BLOCK nos 5**. Copy literal ao copy-source.md (126 strings OK), preços OK com products.json, links nas variantes certas, sem travessão, lint_layout.py OK em 600 e 375 (o lint não pega os defeitos abaixo, que são de imagem/composição). HTML 39/46/38/28/67 KB. Conteúdo NÃO deve ser alterado (decisão do Lucas).

## Bloqueios (mais grave primeiro)

1. **03 hero (L111-146)**: `assets/n3-hero-model.png` com faixa semitransparente retangular no topo (fantasma de ombro/gola), PNG em paleta 256 cores (camo posterizado), manga direita cortada pela borda. Refazer recorte em PNG-24 com alfa limpo; corpo termina no rasgo, 20px+ da borda direita, ou sangra de propósito.
2. **03 círculos de detalhe (L156-223)**: `n3-c-*.png` só mostram textura de camo. Recortar mais aberto (elemento ocupando ~40% do círculo) ou tirar os círculos e deixar o sistema com rótulos. Alinhar pares pelo topo (`valign="top"`); círculo direito de baixo sobe 15px.
3. **03 E28 (L233-307)**: tabuleiro não fica 300+300 (painéis encolhem para 258px); caixas E27 encostam na emenda e quase se tocam no centro. `table-layout:fixed` ou caixa ~252px; 28-32px de padding vertical na célula de texto.
4. **01 fechamento E26 (L286-320, `n1-closing-details.jpg`)**: 3 molduras só de tecido (sherpa parece carpete), nada mostra o harness pass-through do alt, recortes moles. Trocar por foto que leia sozinha ou colagem de produto inteiro; se detalhes, no máximo 2, reconhecíveis e a 2x real.
5. **02 cards 2-up (L152-287)**: preço e botão desalinhados entre colunas (linha 2: SHOP BOMBER 20px abaixo; linha 3: $89.99 62px abaixo). Separar título+linha e preço+botão em duas `<tr>`, a de baixo `valign="bottom"`, ou altura fixa de 3 linhas no título.
6. **02 cartão-presente E31 (L297-328)**: imagem `valign="middle"` deixa vazio grande; no mobile ~110px entre cartão e headline. `valign="top"` alinhado a "SURE", ou headline em largura total e linha imagem+texto embaixo; mobile 32px.
7. **02 colagem do hero (`n2-hero-collage.jpg`)**: mancha branca estourada na foto do blind sobre o rasgo; rasgo corta as fotos de baixo por só ~15px. Subir recorte; molduras inteiras acima do rasgo ou cruzando 40px+.
8. **05 hero E24B (L117-152, `n5-hero.jpg`)**: foto termina em linha reta a ~400/840px, sem degradê para Tap Shoe; braços cortados; no mobile o cover corta o rosto do homem da esquerda e o logo encosta no boné. Degradê de 120-160px; background-position/recorte mobile com os dois rostos inteiros.
9. **04 mosaico (L190, `n4-m-stable.jpg`)**: fragmentos brancos no topo (resto de recorte) e cavalo cortado ao meio na borda esquerda. Cortar ~6px do topo e deslocar o recorte para a direita.

## Avisos (corrigir, não bloqueiam)

- **Todos:** farelos do rasgo (`n*-edge-*.jpg`) grandes demais (3-5px até 25px acima da linha): reduzir para o grão fino da rev-oct-03. Viúvas nos títulos de produto (01 PARKA/JACKET/BIBS; 02 SHIRT/CAP/BOOTS; 03 JACKET/PANT mobile; 05 HOODIE/JACKET/BIB/GLOVES): `&nbsp;` nas duas últimas palavras. PNGs em paleta (`n1-p-*`, `n2-giftcard`, `n3-*`, `n4-pair`): PNG-24 ou JPG com cor da banda.
- **01:** hero de packshot de estúdio (kit: nada de estúdio como hero; outubro abre com foto de uso); e-mail claro e com cara de catálogo (3 faixas iguais), o mais distante de outubro; imagens 796 KB.
- **02:** mobile empilha 6 cards em 1 coluna (5.472px), imagens a 1,5x; colagem com moldura branca repete o tratamento do fechamento do 01.
- **03:** sistema com círculos + E28 na mesma banda sem exceção registrada; "DAY" sozinho na linha serifada.
- **04:** tile da prega das costas não mostra a prega e tem faixas cinza do fundo do packshot; espaços desiguais no mobile (8px / 3px).
- **05:** imagem do cartão-presente igual à do 02 (e o pescador aparece na colagem do 02); 11 linhas idênticas, 5.345px; miniaturas de 120px no mobile.
- **Dark mode:** testar no Gmail app o texto escuro sobre papel claro e camo (01 banda 2, 04 hero, 02 e 05 fechamento).

## Pendente antes do envio

- Placeholders: 01 `{{WOMENS_URL}}`, `{{WOMENS_COLLECTION_URL}}`; 02 `{{GIFT_GUIDE_URL}}`; 03 `{{BUCK_HOLLOW_URL}}`; 04 `{{FLANNEL_URL}}`; 05 `{{CTA_URL}}`; todos `{{HOME_URL}}`, `{{MENS_URL}}`, `{{WOMENS_URL}}`, `{{YOUTH_URL}}`, `{{SALE_URL}}`, `{{INSTAGRAM_URL}}`.
- Endereço e descadastro pelo rodapé do Omnisend (conferir em envio de teste). Preços reconfirmados na data (sobretudo $111.98 promocional do 05). Teste real Outlook desktop e Gmail iOS/Android.

## Precisa do Lucas / cliente

- Aprovar kit v0.5 e as 6 variantes novas (grupo no hero, colagem-hero, hero dividido, sistema com círculos, mosaico reto, card vertical 2-up).
- Fotos de detalhe originais do Buck Hollow; liberação das `crop-sent-*` e `orig-twofisted-utv-two-men.jpg`.
- Hero de estúdio no 01 (sem foto de uso feminina no banco): aceitar ou buscar foto.
- 05 com as 3 faixas como uma banda só; 03 com sistema + E28 na mesma banda.

## Próximo passo

Email Designer aplica os 9 bloqueios + avisos (sem tocar no conteúdo), roda lint e renders; QA rodada 2; só então preview em Artifact para o Lucas.
