# Notas do Designer C · E5 Shadow Series

Decisões de construção de `05-shadow-series.html` (script `compose_C.py`, assets `assets/o5-*`). Para o responsável consolidar no `brief.md`; o brief não foi editado.

## Decisões de construção (2026-09-25)

- 2026-09-25 · **Bandas (5 com preheader e rodapé):** 1 preheader · 2 hero E24 · 3 E25 em `tex-topo-tapshoe` do kit com a faixa de atributos (ref B) · 4 linhas de produto (ref C) em textura de água Patriot · 5 E13 + E14 + D3. E18 texturizado entre 3/4 e 4/rodapé; o rasgo hero/3 está assado na imagem do hero. Nenhuma vizinha com a mesma textura. 2 botões (hero, fim da banda 4), os dois para `{{CTA_URL}}`.
- 2026-09-25 · **Hero:** `orig-hunt40-hunter-forest-back.jpg` (e não hunt50): é vertical, o caçador está de costas e fica logo abaixo do botão, e as copas dão uma área para o texto. Tratamento "late season": 45% dessaturado, mais frio, 18% mais escuro, e o contraluz dourado das copas (acima da cabeça) comprimido até quase noite, com um leve desfoque. Base derrete em papel Tap Shoe e rasga para o topográfico. Contraste medido na área do texto no desktop: branco 4,66:1 no pior ponto, `#E2DDD9` 3,46 (o hero só usa branco). Arquivo 1200x1600, 148 KB.
- 2026-09-25 · **Headline do hero:** `FOR THE MORNINGS&nbsp;THAT` em Prompt 36px + `BITE&nbsp;BACK` em Playfair 88px, branco (é foto: laranja só em textura lisa). No mobile a linha sans quebra em "FOR THE / MORNINGS THAT" (26px) e a serifada fica numa linha a 54px. `LATE-SEASON` preso com `white-space:nowrap` nos dois subtítulos (o navegador quebrava no hífen).
- 2026-09-25 · **Banda 3, faixa de atributos:** 2x2 no desktop e 1 coluna no mobile, como o brief pede. Moldura 1px `#FEF4C6`, raio 12px, sem os traços laranja (a ref B não tem balão nessas células; o acento laranja fica na base do ícone). Palavra de destaque `OUTLASTS` em laranja 72px sobre o Tap Shoe topográfico (laranja 3,9:1 no pior ponto da textura, é texto grande).
- 2026-09-25 · **Ícones (novos, propor ao kit):** `o5-icon-rain` (gota), `o5-icon-scent` (folha com nervura), `o5-icon-grid` (quadro com grade 3x3), `o5-icon-wind` (três rajadas com volta). Traço 2px a 48px (arquivo 96px, PNG transparente, 3 a 4 KB), creme `#FEF4C6`, com a base de 2 traços laranja dos ícones de tecnologia do guia (p.21). `alt=""`: o nome do atributo é texto vivo ao lado.
- 2026-09-25 · **Nomes das tecnologias com ® (ajuste do QA):** `RAIN-FACTOR®` e `SCENT-FACTOR®` nas células de atributo. O copy do cliente escreve sem ®; vale a regra do kit (nome com ® / ™ como na p.21), o mesmo desvio A2 da rodada 2. Render 680 e 375 conferido: o ® não quebra a linha em nenhuma das duas larguras.
- 2026-09-25 · **Banda 4, linhas de produto (ref C):** 3 linhas na ordem dos links do cliente, alternando: Mid Layer (imagem à esquerda), Windproof Fleece Pant (à direita, `dir="rtl"`, então no mobile a imagem vem primeiro), Windproof Fleece Jacket (à esquerda). O produto sai cortado pela borda do e-mail; a imagem (600x820, exibida 300x410) é assada sobre a textura de água com um brilho suave atrás do produto, e as outras 3 bordas voltam para a textura lisa. Caixa emoldurada `#FEF4C6` com os dois traços laranja no canto de cima (no lugar das aspas da ref C, conforme o brief). Na caixa: linha 1 = nome da loja em caixa-alta, linha 2 = `Mossy Oak Terra Coyote`, preço `$69.98 USD` sublinhado e linkado na variante. Sem preço riscado (C3). Mobile: a imagem fica a 260px encostada no lado da sangria, a caixa ocupa a largura toda com 16px de margem.
- 2026-09-25 · **Banda 4 sem headline:** o copy do cliente não tem título para a grade de produtos (título e subtítulo do Bloco 2 ficaram na banda 3). Nada foi inventado.
- 2026-09-25 · **Packshot da variante (produto no manequim), não a foto de modelo:** nas páginas do Mid Layer e da calça as fotos de modelo são da cor Veil Wideland Wolf, e o link é da Mossy Oak Terra Coyote. Para não mostrar uma cor diferente da que está linkada, as 3 linhas usam o packshot da variante (`image_file`, `for_this_variant: true`). A imagem da calça na loja vem com uma blusa cinza de meia manga no manequim, e ela aparece na imagem.
- 2026-09-25 · **Textura de água nova, `o5-tex-water.jpg` (89 KB):** mesma receita da `r2-04-tex-water` da rodada 2 (estrias finas, sem manchas). A `tex-grain-patriot-water` do kit tem manchas de cerca de 13 níveis, e uma imagem assada sobre ela mostraria um degrau na borda. Contraste: branco 12,7 · `#E2DDD9` 9,4 · laranja 4,3. Candidata a entrar no kit no lugar da atual.
- 2026-09-25 · **Bordas novas:** `o5-edge-topo-water.jpg` e `o5-edge-water-footer.jpg` (1200x80, exibidas 600x40, cerca de 10 KB cada), com a folha de baixo por cima (sombra acima do rasgo, borda clara de fibra abaixo), mesma mecânica da rodada 2.
- 2026-09-25 · **Rodapé:** E13 + E14 do kit + D3: `[[CONFIRMAR: endereço físico da Habit]]` visível e link `Unsubscribe` em `{{UNSUBSCRIBE_URL}}`, nessa ordem, depois do copyright (a ordem do copy do cliente).
- 2026-09-25 · **Dark mode:** todas as bandas já são texturas escuras fixas, então nada troca; só a página em volta da coluna vai para `#1E1F21` (mesmo esquema do 03 da rodada 2). Os dois logos já são brancos.
- 2026-09-25 · **Peso:** HTML 31,7 KB · imagens 635 KB no total (hero 148, textura topo do kit 88, água 89, produtos 102 + 61 + 99, bordas 11 + 9, ícones 14, logos 13). Todas abaixo de 150 KB.

## Para decisão do responsável

1. **Duas bandas de estrutura** (atributos + produtos). O brief já pede assim, mas pelas rules §3 isso é exceção e precisa de ok explícito registrado no brief.
2. **Windproof Fleece Pant na loja:** "This item cannot be shipped to the states of California or New York" e aviso de Prop 65 (PFOS). Se a lista inclui CA e NY, avaliar com o cliente (segmentar, ou trocar o produto nesse envio). O e-mail não diz nada disso.
3. **Claims conferidos no `body_text`:** "Grid Fleece Interior" só existe no Mid Layer (a calça e a jaqueta Windproof são forradas de sherpa); "Windproof Construction" só existe na calça e na jaqueta Windproof. A faixa fala da linha inteira, então cada claim vale para parte dos produtos (brief C5). Ficou como o cliente escreveu.
4. **Novos módulos para o kit:** faixa de atributos 2x2 com ícone de traço fino, linha de produto sangrando + caixa emoldurada com os traços laranja, os 4 ícones e a textura de água sem manchas.
5. Continuam em aberto: `{{CTA_URL}}` (coleção Shadow Series), endereço, tag de descadastro do Omnisend, preço no dia 29/10 (C3), liberação da foto original (C9).

## Rodada 2 (2026-09-25)

Reconstrução de `05-shadow-series.html` pela revisão do responsável (`email-kit/references/rev-oct-05-shadow-series.png` + `revision-r2.md`). Script: `compose_C.py`, jobs novos `grad`, `hero2`, `packs`, `edge2` (os jobs da rodada 1 continuam no script). Conferido lado a lado com a revisão no render 680, e também em 375 e `--dark`.

### O que mudou

- **Bandas:** preheader · hero · banda de atributos · tabuleiro + botão · rasgo · rodapé. Sai o rasgo entre o hero e a banda 2 e entre a banda 2 e os produtos: como na imagem, o hero derrete na banda e a banda termina em Patriot, que continua na água.
- **Hero (`o5-hero-r2.jpg`, 1200x1400, exibido 600x700, 147 KB):** **mesma foto da rodada 1** (`orig-hunt40`; a foto da revisão não é recuperável porque o texto cobre o sujeito). Reposicionada: cabeça e mochila do caçador ficam entre o logo e a etiqueta, e a metade de baixo puxa para Tap Shoe para o texto vivo. A base são as últimas linhas do tile topográfico do kit, e a banda 2 começa na linha 0 do mesmo tile, então a junção não aparece. Texto novo: etiqueta `#2A2B2D` com "FOR THE MORNINGS THAT" em laranja Prompt 800 23px, **BITE / BACK** Playfair 900 branco 120px / 98px (mobile 72 / 66), subtítulo espaçado 16px, botão. Contraste medido: branco 7,6:1 no pior ponto da headline, 10,0:1 no subtítulo, 4,6:1 no logo.
- **Banda de atributos (`o5-tex-topo-grad.jpg`, 90 KB):** degradê Tap Shoe → Patriot Blue com as linhas topográficas do kit, `background-size:100% auto`, sem repetição, bgcolor `#202944` (igual ao pé da imagem; no mobile, onde a banda fica mais alta, o resto é Patriot liso). THE LINE THAT OUTLASTS (Prompt 800 28px) / **THE WEATHER** (Playfair 900 64px), corpo 18px em caixa normal (como na imagem, sem subtítulo espaçado). 4 cards com moldura `#FEF4C6` raio 10px, títulos laranja Prompt 800 17px, ® menor em `<sup>`, os mesmos ícones da rodada 1 a 44px.
- **Tabuleiro 300 + 300 sem margem:** packshot da variante (Mossy Oak Terra Coyote, `image_file` do `products.json`) sobre painel chapado com as cores medidas na imagem: taupe `#A69A89`, cinza `#ABB1B3`, marrom `#5A4538` (`o5-pack-*.jpg`, 600x670, exibidos 300x335; 76 + 47 + 61 KB). Caixa de produto em cima da água: contorno 1px, raio 10px, texto centralizado, título laranja 19px/20px, variante `#CFC8BF` 14px, preço Prompt 800 20px branco sem sublinhado, a caixa inteira num link só para a variante. Sem os dois traços laranja. Linhas 1 e 3 com `dir="rtl"` e a imagem primeiro no código: no mobile empilha sempre com a imagem em cima.
- **Botões:** `#FF6400` com texto **branco**, Prompt 800, raio 4px (hero 18px, SHOP NOW 18px com tracking 4px e 300px de largura).
- **Rodapé:** logo empilhado 136px, menu com filetes, **ícone do Instagram** (`email-kit/assets/icon-instagram.png`, 36x36) ao lado de "Follow us on Instagram" / @HABITOUTDOORS, copyright. **Saíram** a linha `[[CONFIRMAR: endereço]]` e o link Unsubscribe (item 5 da revisão).
- **Rasgo novo `o5-edge-water-footer-r2.jpg`** (6 KB): mais fundo e serrilhado, sem a borda clara de papel, como na imagem.
- **Copy:** a linha "Insulated Bib" da terceira caixa **não** foi copiada (erro da imagem). Nomes, variantes, preços e URLs do `products.json`. Headline, corpo e botões iguais ao `copy-source.md`.
- **Peso:** HTML 30,3 KB · imagens 549 KB (hero 147, degradê 90, água 89, packshots 183, ícones 14, logos 13, Instagram 7, rasgo 6).

### Desvios e por quê

1. **Foto do hero:** não é a da revisão (homem sentado nas pedras), é a da rodada 1 com o layout de texto novo. O sujeito fica acima da etiqueta, não por baixo do texto como na imagem.
2. **Serifa do hero a 120px (a revisão pede 96 a 110):** a BITE/BACK da imagem mede cerca de 315px de largura por 80px de altura de caixa-alta. A Playfair 900 a 110px ficava 15% mais estreita; a 120px a largura chega perto e a altura fica 10% maior. A fonte da imagem é mais larga que a Playfair; não tem como igualar as duas medidas ao mesmo tempo.
3. **Contorno da caixa em `#FEF4C6` sólido** (a revisão diz "a ~70%"): rgba em borda não funciona no Outlook, e um hex misturado sairia da paleta do kit.
4. **Ícone do Instagram a 36x36** como o texto da revisão pede; na imagem ele mede uns 45px. Se valer a imagem, o arquivo de 72px aguenta até 44px.
5. **Títulos das caixas a 19px** (texto da revisão); na imagem eles parecem ter uns 17px. Mantive 19px pelo contraste de texto grande. Por isso a quebra de linha é um pouco diferente ("MEN'S SHADOW / SERIES / WINDPROOF / FLEECE PANT").
6. **Fonte da sans:** a imagem usa uma geométrica mais larga (Sweet Sans). No HTML vale a Prompt, então textos espaçados e botões ficam um pouco mais estreitos, mesmo com tracking maior.

### Pendências

- **Original da foto do hero da revisão** (homem sentado com o boné HABIT): pedir ao cliente/responsável; com ela, refazer `hero2` trocando só a foto.
- Endereço físico e descadastro agora dependem do **rodapé do Omnisend** (CAN-SPAM): conferir no envio.
- Contraste do botão branco sobre `#FF6400` 2,97:1, abaixo do AA: exceção pedida pelo responsável (revision-r2 item 1), fica registrada.
- Continuam em aberto da rodada 1: `{{CTA_URL}}` e os demais merge fields, preço $69.98 no dia 29/10 (C3), restrição de envio da calça para CA/NY, claims da faixa (C5), duas bandas de estrutura como exceção registrada no brief.
- Assets da rodada 1 sem uso agora no HTML (`o5-hero.jpg`, `o5-prod-*.jpg`, `o5-edge-topo-water.jpg`, `o5-edge-water-footer.jpg`): ficaram na pasta; dá para apagar quando a rodada 2 for aprovada.
