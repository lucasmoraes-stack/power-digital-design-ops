# Designer A · notas de construção (E1 e E2)

> Decisões tomadas na construção de `01-cedar-branch-bibs.html` e `02-youth-season.html`, para o responsável consolidar no `brief.md` ("Decisões registradas"). Assets: `assets/o1-*` e `assets/o2-*`, todos gerados por `compose_A.py` (importa `email-kit/tools/compose.py` sem editá-lo; nada escrito no kit). Render check 680, 375 e dark em `scratchpad/oct/A/`.

## Peso

| E-mail | HTML | Imagens (light) | Só dark mode | Maior imagem |
|---|---|---|---|---|
| 01 Cedar Branch Bibs | 37,5 KB | 725 KB | 0 | `o1-hero.jpg` 149,8 KB |
| 02 Youth | 35,1 KB | 619 KB (717 KB contando o dark) | 98 KB (`tex-paper-light-dm` + 2 bordas -dm) | `o2-hero.jpg` 149,6 KB |

Pesos depois das correções do QA r1 (2026-09-25).

## Decisões registradas

- 2026-09-25 · **E1 hero, foto:** `orig-hunt22-three-hunters-field-sunrise.jpg` a 1200px, um pouco mais quente e escura; céu "crescido" para cima como névoa (`extend_top="fog"`) e puxado para Tap Shoe no topo para o logo branco (contraste medido na área do logo: branco 5,25:1). As linhas de cima da foto foram suavizadas antes (`soften_top`), senão as copas viravam listras verticais na névoa. Designer A.
- 2026-09-25 · **E1 etiquetas (ref C):** três tabelas encostadas na borda direita da foto, uma por linha (`READY WHEN THE` / `WEATHER` em Playfair 900 / `TURNS`), texto vivo `#2A2B2D` em `<td bgcolor="#E2DDD9">` com papel granulado. O papel é `o1-tex-label.jpg`, um recorte de 720x180 do `tex-paper-light` do kit (8 KB): o tile inteiro custava 88 KB só para três etiquetas e levava o e-mail a 789 KB. O conjunto vai num `<div role="heading" aria-level="1">` (h1 não pode conter tabela). No dark mode as etiquetas **não trocam** (ficam papel claro sobre a foto, como um elemento da imagem). Designer A.
- 2026-09-25 · **E1 subtítulo e botão** ficam abaixo dos caçadores, onde o capim derrete em papel Tap Shoe (contraste do branco 13,3:1), e não sobre a foto. Designer A.
- 2026-09-25 · **E1 banda 3:** Major Brown grain. Bibs cortado pela borda esquerda do e-mail, parka pela direita (imagens compostas, hoje 600x720 com a textura da banda, bordas sem sangria esfumadas no tile). Caixa emoldurada `#FEF4C6` com raio 12px (precisa `border-collapse:separate` na tabela da moldura, senão o raio some). Card: linha 1 `MEN'S CEDAR BRANCH`, linha 2 o tipo (`Insulated Waterproof Bibs` / `Insulated Waterproof Parka`), preço sublinhado linkado na variante. Designer A.
- 2026-09-25 · **E1 banda 4 (D1, D2):** Tap Shoe paper, com um detalhe de roupa ao lado de cada review (ver a correção do QA r1 abaixo para os recortes atuais). Banda sem headline: o cliente não escreveu nenhuma para o bloco de reviews. Designer A.
- 2026-09-25 · **X7 · E1, citações:** aspas retas removidas nas citações do Matthew B. e do Ryan And L. (a do Andrew C. já veio sem aspas). A aspa grande laranja (Playfair, `aria-hidden`) marca a citação, convenção de citação em destaque; as palavras não mudaram. Cada citação vai num `<blockquote style="margin:0; padding:0; border:0;">` para o leitor de tela anunciar citação. Se o cliente pedir as aspas no texto, voltam sem mexer no layout. `&nbsp;` entre as duas últimas palavras de cada citação para não deixar palavra sozinha no mobile. Estrelas `★★★★★` em 24px (o piso do laranja no Tap Shoe paper), com `role="img"` e `aria-label="5 out of 5 stars"`. Designer A.
- 2026-09-25 · **QA r1, E1 banda 3 (bloqueio 1):** produtos recompostos. Bib em 1500px de altura (2x os 740 de antes), com cerca de 20% da peça para fora pela esquerda; peitilho, alças, logo e coxas no quadro, e as pernas se dissolvendo na textura na base da imagem. Parka em 840px, 25% para fora pela direita (manga cortada), barra dissolvendo embaixo. As imagens caíram de 600x760 para 600x720 (300x360 no e-mail), e o padding de baixo da linha da parka foi de 64 para 40px. Largura visível a 680: bib cerca de 160px, parka cerca de 190px. O bib não chega aos 200px pedidos porque a peça é estreita (a PNG da loja mede 0,38 de largura por altura): com zoom maior só o peitilho caberia no quadro. Designer A.
- 2026-09-25 · **QA r1, E1 banda 4 (bloqueio 2):** detalhes trocados. Matthew B.: bolso de peito da parka com a mão e o logo HABIT bordado (`parka/06.png`, recortado em y 250 a 1060, sem o rótulo "Zippered Chest Pocket" e sem o canto transparente) → `o1-detail-pocket.jpg`, e esse é **Realtree APX**, a mesma estampa do produto. Ryan And L.: mão abrindo o zíper de 2 vias no peitilho marrom do bib (`bib/08.png`) → `o1-detail-zipper.jpg`. Andrew C.: `bib/07.png` inteiro, com mão, zíper da perna e bota. É PNG recortado (o "cinza de estúdio" da versão anterior era o fundo que eu tinha aplicado), então agora vai sem moldura, direto sobre o papel com sombra, e o corte reto de cima da foto da loja some num degradê → `o1-detail-legzip.jpg` (Realtree Edge). `04.png` e `05.png` saíram do e-mail, e os arquivos `o1-detail-fabric.jpg` e `o1-detail-insulation.jpg` foram apagados. Designer A.
- 2026-09-25 · **® nas tecnologias (A2 da rodada 2, QA r1):** `Rain-Factor®` no corpo da banda 3 do E1 e da banda 3 do E2. `Scent-Factor` não aparece no copy do E1 nem do E2. Designer A.
- 2026-09-25 · **E1 banda 5, faixa dividida:** Ivy Green grain, que não aceita laranja: o destaque `SEASON` fica branco. No mobile empilha com o botão largura total; a tabela do botão perde o `align="right"` (float) no mobile, senão ela encostava no filete de baixo. Designer A.
- 2026-09-25 · **E1 borda Tap Shoe paper → Ivy** (`o1-edge-papertapshoe-ivy.jpg`) é nova e não usa o `compose_torn_edge_textured` direto: as últimas linhas do tile Tap Shoe paper ficavam 1,7 nível abaixo do fim da banda de reviews e apareciam como degrau no render. A parte de cima usa o tile sem a mancha lenta, no nível médio. Candidata a entrar em `EDGES_V04` do kit. Designer A.
- 2026-09-25 · **E2 hero, foto:** não há foto de modelo youth em locação na loja (as 3 peças só têm packshot em forma). Usada `crop-sent-sep15-camp-chairs-family.jpg` (criança no centro, sorrindo), com névoa gerada acima para logo e headline em duas vozes (`THEIR` / `SEASON` laranja / `STARTS HERE`), rasgando para Major Brown. É recorte provisório, já usado no hero do 01 de maio (`r2-01-hero-camp.jpg`); no lote de outubro aparece só aqui. Designer A.
- 2026-09-25 · **E2 tabuleiro (ref B):** painel de produto = `<td>` com textura taupe gerada (`o2-tex-taupe.jpg`, `#7F7064` com grão, 600x600, 24 KB) e packshot PNG transparente por cima, nome da loja em caixa-alta no alto do painel (branco, 21px: texto grande, 4,27:1 no pior pixel, passa 3:1). Bloco de texto = moldura `#FEF4C6` com os dois traços laranja no canto de cima (tabelas de 3px com 5px de vão), tipo, cor da variante (`Realtree APX` / `Realtree Edge`, do `products.json`) e preço sublinhado. **Sem rabicho de balão:** a moldura arredondada já lê como balão, e o rabicho seria mais uma imagem. Alterna lado com `dir="rtl"`; no mobile, painel sempre antes da moldura. Designer A.
- 2026-09-25 · **E2 packshot do hoodie:** o PNG da loja tem um véu de alpha quase invisível no quadro todo, que diminuía o recorte e aparecia como retângulo claro sobre o papel. Recortado a partir de alpha 40 (`clean_hoodie`). Designer A.
- 2026-09-25 · **E2 banda 4:** papel claro (`dm-tex`), duas colunas: hoodie atrás do bib numa PNG transparente com sombra (`o2-layer.png`, 97 KB), serve no claro e no dark sem gêmea `-dm` e sem emenda de textura; texto vivo à direita (`BUILT FOR EVERY` / `COLD` / `MORNING`), botão `SHOP YOUTH`. Designer A.
- 2026-09-25 · **Rodapé (D3)** nos dois: E13 + E14 + copyright + `[[CONFIRMAR: endereço físico da Habit]]` + `Unsubscribe` em `{{UNSUBSCRIBE_URL}}`. Designer A.

## Para decisão do responsável

1. Aprovar as estruturas novas deste par: etiqueta (E1 hero), linha de produto sangrando + caixa emoldurada, caixa de review, faixa dividida (E1), tabuleiro painel taupe + moldura com traços (E2).
2. Etiquetas do E1 ficam claras também no dark mode (proposta). Alternativa: trocar para o papel escuro com texto claro.
3. X7: aprovar a remoção das aspas retas (as citações estão em `<blockquote>`).
4. Dois dos três detalhes do E1 (zíper do peitilho e zíper da perna) são Realtree Edge ou peitilho liso; o bolso da parka é APX. A variante vendida é Realtree APX.
5. E1 está em 725 KB de imagem (hero 150 KB + 4 texturas); não cabe mais nenhuma composição pesada nele.
6. Bib do E1 com cerca de 160px de largura visível (abaixo dos 200px do QA): aceitar ou trocar por uma foto do bib vestido, que a loja só tem em Realtree Edge.

## Rodada 2 (2026-09-25)

Reconstrução de `01-cedar-branch-bibs.html` e `02-youth-season.html` sobre as imagens revisadas do responsável (`email-kit/references/rev-oct-01-cedar-branch-bibs.png` e `rev-oct-02-youth-season.png`) e o `revision-r2.md`. Medidas tiradas das próprias imagens (posição das bandas, altura de cada etiqueta, tamanho de cada linha de texto, cores por amostragem) e conferidas lado a lado com o render 680 até bater; 375 e `--dark` conferidos. Renders em `scratchpad/r2A/rend/`. Script: `compose_A.py` reescrito (importa `email-kit/tools/compose.py` sem editar; não depende de `compose_v05.py`). As seções acima valem como histórico da rodada 1; o que conflita com esta seção fica valendo esta.

### Peso

| E-mail | HTML | Imagens (claro) | Com gêmeas dark | Maior imagem |
|---|---|---|---|---|
| 01 Cedar Branch Bibs | 31,9 KB | 717 KB | 717 KB (nada troca no dark) | `o1-hero.jpg` 149 KB |
| 02 Youth | 34,3 KB | 517 KB | 619 KB | `o2-hero.jpg` 138 KB |

### O que mudou

- **Nos dois:** botão `#FF6400` com texto branco, Prompt 800 18px, tracking 3px, raio 4px, 54px de altura (01: 418px de largura como na imagem; 02: cerca de 302 / 268 / 258px). Corpo em Prompt 400 17/24 branco, centralizado. Headline em duas vozes com a serifa dominante em 2 linhas (STARTS / HERE 110px, SEASON 106px, CEDAR / BRANCH, SMALLER / SIZES, COLD / MORNING 62 a 64px), caixa-alta real no HTML. Product Info Box nova (contorno 1px, raio 10px, texto centralizado, título laranja, linha 2 `#CFC8BF`, preço branco 800 sem sublinhado; título, linha 2 e preço linkados na `url` do produto), sem os traços laranja. Rodapé v0.5: logo empilhado 136px, menu com filetes brancos, ícone do Instagram + "Follow us on Instagram" / @HABITOUTDOORS, copyright; **sem** endereço e sem Unsubscribe (vêm do rodapé do Omnisend). ® em sobrescrito pequeno, com `Rain-Factor®` sem quebra.
- **01:** hero recomposto do original `orig-hunt22` no enquadramento da imagem (x1,24, caçadores à esquerda, céu desde o topo, um pouco mais apagado); etiquetas `READY WHEN THE` (Prompt 30, caixa de 56px) e `WEATHER` claras, `TURNS` escura em Tap Shoe paper com a serifa laranja (caixas de 88px, 4px entre elas, encostadas na borda direita). Banda 2 nova em **Major Brown com retícula** (`o1-tex-halftone.jpg`, gerada no script: grão do kit + manchas de pontos em grade hexagonal, posições copiadas da imagem): bib inteiro à esquerda; THE / CEDAR BRANCH / COLLECTION, subtítulo, corpo e caixa à direita; caixa do parka à esquerda e parka cortado pela borda direita. Banda de review Tap Shoe com **um review só** (Ryan And L.): aspas e estrelas laranja, citação centralizada, nome `#B0A89C` em caixa-alta espaçada, parka de perto cortado à direita e embaixo. Fecha com a **banda de foto cheia** (arqueiro, com a linha branca desenhada), LAYER UP FOR THE / SEASON, corpo e SHOP HUNTING largo. Saíram a faixa dividida em oliva, os detalhes D2 e os reviews do Matthew B. e do Andrew C. (decisão do responsável; registrar no brief).
- **02:** hero com THEIR SEASON / STARTS HERE, subtítulo e botão em cima e a família nas cadeiras embaixo, corte reto para a banda (sem rasgo, como na imagem). Banda **Tap Shoe** (não mais marrom) com REAL GEAR IN / SMALLER SIZES, subtítulo e corpo; **3 cards emoldurados grandes** (530x331, contorno 1px, raio 14px, 35px de margem): painel de cor chapada de 196px com o packshot (bib e calça cortados pela base do card, hoodie inteiro) e a caixa de produto centralizada no resto, alternando de lado; SHOP NOW. A banda termina num degradê para Major Brown e rasga para o papel claro (`o2-edge-tapshoe-paperlight.jpg` + `-dm`). Fechamento em papel claro: foto emoldurada inclinada do menino à esquerda; BUILT FOR EVERY / COLD MORNING (serifa Tap Shoe), corpo e SHOP YOUTH alinhados à esquerda.
- **Mobile:** tudo empilha com a imagem primeiro. No 01 o fundo de retícula fica sem escala e à esquerda no mobile (o bib continua sem emenda); o retângulo do parka ficou sem pontos na borda para não aparecer emenda quando ele muda de lugar. No 02 o painel vira largura total na mesma cor chapada, com o packshot centralizado e os cantos de cima arredondados.
- **Dark mode:** 01 inteiro fixo escuro (só a página em volta troca), etiquetas claras continuam claras. 02 troca só o papel claro (fundo, texto, as duas bordas); a foto emoldurada é PNG transparente e serve nos dois.

### Desvios da imagem, e por quê

- **Fonte:** a sans da imagem é mais larga que a Prompt (substituta da Sweet Sans). Compensei com tracking (títulos, caixa, botão, rodapé) para as linhas terem o mesmo comprimento; algumas quebras de linha do corpo e da citação ficam diferentes. A Playfair do navegador sai uns 10% mais estreita que a da imagem: usei 62 a 110px com 1 a 4px de tracking para igualar a largura.
- **Tamanhos da caixa de produto:** título 19px (01) e 16px (02: a caixa é mais estreita e o título quebra em 2 linhas como na imagem, com `<br>`), preço 21px (01) / 20px (02), variante 13px `#B0A89C`. O `revision-r2.md` fala em título 19px; no 02 segui a imagem. No 02 o laranja fica sobre Tap Shoe (4,8:1, AA em qualquer tamanho).
- **Contorno** `#E4DBB3`: é o `#FEF4C6` medido na imagem sobre o escuro (hex derivado do token, não cor nova de marca).
- **Cores dos painéis do 02** medidas na imagem: oliva = `#595442` (Ivy Green do kit), ferrugem `#774727` e ardósia `#4F5C5F` (o `revision-r2.md` sugeria `#8A4B2A` e `#5E6770`, "a conferir"). Precisam entrar no kit se ficarem.
- **01 banda 2:** o bib ficou um pouco menor que na imagem (cerca de 150x555 contra 170x635) e o parka começa uns 20px mais abaixo: em tabela, bib e parka não podem se sobrepor na vertical, então a linha do bib termina em 600px antes da linha do parka. Pela mesma razão a caixa do parka fica em x 48 a 320 (não invade o parka).
- **01 retícula:** sem pontos em volta do parka (ver Mobile); a mancha embaixo à direita, junto à barra do parka, saiu. Os pontos são um pouco mais suaves que os da imagem.
- **01 fim:** abaixo da faixa limpa do recorte a foto vira quase preto (`#141414`) atrás do texto; na imagem o corpo do arqueiro continua escuro atrás de SEASON, mas essas linhas têm texto por cima e não dá para recortar.
- **Alturas:** 01 fica 21px mais longo que a imagem (o rasgo do hero precisa de algumas linhas da banda seguinte dentro da imagem). 02 bate (3053 contra 3049).
- **Ícone do Instagram** exibido 44x44 (a imagem mostra cerca de 45px; o `revision-r2.md` diz 36x36). Segui a imagem; trocar é só o `width`/`height`.
- **Mobile:** etiquetas do hero do 01 em 22px / 48px (a serifa de 62px não cabe em 375px); SMALLER e MORNING em 58px, abaixo dos 64 a 72px do `revision-r2.md`, porque a palavra não cabe em 327px com mais.
- **01 cards:** linha 2 = `Insulated Waterproof Bibs` / `Parka`, sem a variante, como na imagem (o QA r1 tinha pedido a variante; a imagem do responsável não a mostra).

### Fotos provisórias (recorte 1x, trocar pelo original)

- `assets/o1-rev-archer.jpg` (600x731, 47 KB): linhas 2171 a 2517 da `rev-oct-01`, com a linha branca desenhada; abaixo, degradê para quase preto gerado.
- `assets/o2-rev-boy.png` (240x350, 34 KB): foto de dentro da moldura da `rev-oct-02`, desrotacionada 5,8°, recortada dentro do branco e remontada (moldura branca 6px, 5,8°, sombra) em PNG transparente.
- As duas são 1x (600px de origem): um pouco moles em tela retina. Pedir os originais.

### Assets

Novos ou refeitos: `o1-hero.jpg`, `o1-tex-halftone.jpg`, `o1-prod-bibs.jpg`, `o1-prod-parka.jpg` (os dois com o recorte exato da retícula embaixo da célula no desktop), `o1-review-parka.jpg`, `o1-rev-archer.jpg`, `o2-hero.jpg`, `o2-panel-{bib,hoodie,pant}.jpg`, `o2-edge-tapshoe-paperlight(-dm).jpg`, `o2-rev-boy.png`. Mantido: `o1-tex-label.jpg`. Apagados (sem uso em nenhum HTML ou script): `o1-detail-*`, `o1-edge-papertapshoe-ivy.jpg`, `o2-tex-taupe.jpg`, `o2-pack-*.png`, `o2-layer.png`.

### Pendências

1. Originais do arqueiro (01) e do menino (02).
2. Registrar no `brief.md`: um review só no 01; rodapé sem endereço e sem descadastro no HTML (conferir que o rodapé do Omnisend traz os dois antes do envio, CAN-SPAM); texto branco no botão (2,97:1, exceção pedida).
3. Aprovar no kit v0.5: retícula Major Brown, Product Info Box nova, card emoldurado com painel chapado (e as cores ferrugem e ardósia), etiqueta escura, banda de foto cheia de fechamento, rodapé com ícone.
4. Tamanho do ícone do Instagram: 44 (imagem) ou 36 (texto da revisão).
5. Testes reais continuam: Gmail iOS/Android no dark (etiquetas claras do 01, papel do 02), Outlook (VML das bandas e retícula em `type="tile"`; raio some nos cards).
6. `{{CTA_URL}}` dos dois e a URL de SHOP HUNTING seguem `[[CONFIRMAR]]` no brief.
