# Notas do Designer B · E3 e E4

> Decisões de construção de `03-heavy-weight-hoodie.html` e `04-crater-valley.html` (2026-09-25), para o responsável consolidar no `brief.md`. Assets: `assets/o3-*` e `assets/o4-*`, todos gerados por `compose_B.py` (importa `email-kit/tools/compose.py` sem editá-lo; rodar de novo refaz tudo igual).

## Decisões registradas

- 2026-09-25 · **E3, foto do hero:** `orig-hunt50-hunter-oaks-autumn.jpg`, só a metade direita (carvalhos e capim, **sem o caçador**), com a cor esfriada, neblina baixa e a névoa de cima gerada da própria foto. O hoodie Major Brown (packshot da variante) fica **de pé na frente das árvores**, como produto sobre paisagem (princípio 4 da rodada 2). Motivo: as fotos de modelo da loja são de estúdio (o kit proíbe estúdio como hero), e compor um modelo de estúdio numa paisagem seria falso lifestyle. O Designer C usa a hunt40 e o A usa a hunt22, então a hunt50 não se repete no lote.
- 2026-09-25 · **E3, painéis (ref A):** um painel por cor, no tom da cor: Major Brown em `tex-grain-brown`, Gunmetal em `tex-paper-tapshoe` (a paleta não tem cinza-grafite; o Tap Shoe é o mais próximo), Loden Green em `tex-grain-ivy`, sobre papel claro. O hoodie **sobe para fora do painel** (44px acima da borda de cima). Linha 1 = cor, linha 2 = `Men's Heavy Weight Full Zip Hoodie` (nome da loja), preço sublinhado linkado na variante.
- 2026-09-25 · **E3, emendas:** a parte do painel que está na imagem é assada **na mesma fase do tile** que a `<td>` do texto mostra (`background-position:left top`, 600px), para a junção imagem/texto não aparecer. Cada painel tem 4 arquivos: desktop, mobile, e as gêmeas `-dm` (papel escuro no dark mode). O Outlook desktop mostra a metade do texto em cor lisa (`bgcolor`), sem grão.
- 2026-09-25 · **E4, hero (ref D):** headline, subtítulo, botão e logo **à esquerda**; o Full Zip Fleece no modelo (foto 05 da loja) sangra pela direita e é **cortado pela borda de cima do e-mail**. O corte da coxa fica escondido embaixo do rasgo para o Major Brown. No desktop é uma imagem dividida em coluna direita + faixa de largura total; no mobile vem texto, depois uma gêmea com uma **tira de papel rasgada por cima do corte** (as fotos de modelo da loja vêm cortadas na testa; desde o QA r1 o corte é abaixo do queixo). Sem o círculo de retrato da ref D (opcional no brief; não há pessoa real para o círculo).
- 2026-09-25 · **E4, molduras (ref D):** contorno 1px `#FEF4C6`, raio 12. Na imagem ficam a linha de cima, a de baixo e o lado de fora; o lado do texto fecha com borda CSS na `<td>` (conferido no render: as linhas batem no mesmo pixel). **Quebra da moldura** conforme a foto: o Performance Hoodie (capuz inteiro na foto 08) sai por cima da linha; o Full Zip Fleece (foto 06) fica **cortado pelas linhas de cima (na gola, QA r1) e de baixo**, com o cotovelo passando da linha lateral; o Sweater Fleece ¼ Zip sai por cima. Os dois traços laranja ficam no canto de fora, do lado da imagem, uma vez por moldura. No mobile a imagem tem a moldura fechada e o texto vem embaixo, sem moldura.
- 2026-09-25 · **E4, ¼ Zip sem foto de modelo:** a loja não tem foto de modelo no Realtree APX (a variante do link); as de modelo são Mossy Oak New Bottomland e Realtree Excape. Na moldura usei o **packshot APX** (a imagem mostra o que o link vende). No GIF, que não aponta para variante, entra o modelo em Bottomland.
- 2026-09-25 · ~~**E4, GIF (D4)**~~ (versão 1, substituída pela entrada "QA r1, GIF" abaixo): `o4-lifestyle.gif`, 600x380 (arquivo 1x), **344,5 KB**, 8 quadros em loop: as três peças juntas (2,6 s, é o quadro que o Outlook desktop mostra e funciona sozinho), depois hoodie, fleece e quarter zip um de cada vez (1,8 s), com um quadro de crossfade de 110 ms entre eles. Fotos de modelo da loja numa janela rasgada no papel Ivy (as tiras escondem os cortes da testa e da coxa). Fundo de cor chapada por cena (manhã fria, dia, fogueira): degradê em GIF vira faixas. Para caber: paleta única de 104 cores, sem dither, filtro mediano 3 e cada quadro depois do primeiro só carrega os pixels que mudaram. A 2x ou com mais quadros de crossfade passava de 1 MB. O fallback JPG estático (`o4-lifestyle-still.jpg`, 29 KB) está gerado e sem link.
- 2026-09-25 · **E4, texturas por banda:** hero em Tap Shoe paper, molduras em Major Brown (laranja permitido no destaque grande: `LAYERING`), estilo de vida em Ivy (sem laranja, destaque `FIRST LIGHT` em branco), rodapé Tap Shoe liso. Nenhuma vizinha repete. Borda nova `o4-edge-brown-ivy.jpg` (o kit não tinha o par brown/ivy).
- 2026-09-25 · **QA r1, rostos (E4):** nenhum rosto cortado entre a testa e a boca. As fotos de modelo da loja são cortadas **abaixo do queixo / na gola** (`CHIN` no `compose_B.py`, linha da foto original por imagem), e o corte fica sempre numa borda: a borda de cima do e-mail no hero desktop, a tira de papel rasgado no hero mobile e no GIF, a linha de cima da moldura no Full Zip Fleece. Rosto inteiro só onde a foto tem a cabeça inteira: o Performance Hoodie de capuz (moldura 1 e cena 2 do GIF).
- 2026-09-25 · **QA r1, GIF (E4), substitui a entrada D4 acima:** `o4-lifestyle.gif` refeito com **3 cenas, 244,9 KB**, 600x380 (1x), loop, corte seco entre as cenas: (1) as três peças juntas, 2,6 s, é o quadro do Outlook desktop e funciona sozinho; (2) o Performance Hoodie de capuz, rosto inteiro, 2 s; (3) o Sweater Fleece ¼ Zip em Realtree Excape, 2 s. O fundo deixou de ser cor chapada: é a mata e o campo **desfocados de uma foto real da Habit** (`crop-sent-sep10-utv-hunters.jpg`, só a faixa da esquerda, sem pessoa; nenhum outro e-mail do lote usa essa foto). Menos posterização: 152 cores, paleta própria por quadro, suavização de 0,8 px, e cada quadro depois do primeiro só leva os pixels que mudam. O dither foi testado e saiu: pesava mais e deixava granulado. Arquivo 2x não coube: 3 quadros fotográficos em 1200x760 dão cerca de 3 vezes o limite. O crossfade saiu porque um quadro de transição por troca dobrava o peso. O estático de reserva (`o4-lifestyle-still.jpg`, 32 KB) foi recomposto com a cena 1 nova, sem link.
- 2026-09-25 · **QA r1, corpo das molduras (E4):** 15px/23px passou para 16px/25px (kit).
- 2026-09-25 · **Palavra de destaque em laranja:** E4 hero (`CRATER VALLEY`, sobre Tap Shoe) e E4 banda 3 (`LAYERING`, Major Brown, só grande). E3 hero fica branco (texto sobre névoa de foto, não sobre Tap Shoe) e E3 banda 3 em `#2A2B2D` (papel claro).
- 2026-09-25 · **Rodapé D3:** igual ao A e ao C: copyright do kit, `[[CONFIRMAR: endereço físico da Habit]]` e `Unsubscribe` em `{{UNSUBSCRIBE_URL}}`.

## Diferente do brief

- **E3, `Men's` na linha 2:** o brief diz "nome do produto na linha 2"; usei o nome da loja com `Men's` (o copy do E3 também diz "Men's Heavy Weight Full Zip Hoodie"). A regra "sem Men's" do brief é só do E4.
- **E4, botão do hero:** `SHOP CRATER VALLEY` com padding lateral 18px (kit: 36px) e `white-space:nowrap`, porque na coluna de texto de 286px o rótulo quebrava em duas linhas ou alargava a coluna e desalinhava a imagem. Cor, fonte, tracking, raio e altura iguais aos outros botões.
- **E4, ordem na banda 4:** segui o copy (headline, GIF, texto, botão); o brief põe o GIF primeiro.
- **E4, GIF:** 3 cenas com corte seco, sem crossfade (D4 pedia crossfade curto), em arquivo 1x, para caber em 250 KB (QA r1).
- **Peso do E4 acima de ~800 KB** por causa do GIF, dentro do teto de ~900 KB do QA r1 (tabela abaixo).

## Peso

| | HTML | Imagens vistas no desktop claro | Mobile claro | Arquivos referenciados (todas as variantes) |
|---|---|---|---|---|
| E3 | 32,1 KB | ~646 KB (hero 144, 4 texturas 351, painéis 120, bordas e logos 31) | ~648 KB | 1.102 KB (inclui gêmeas mobile e `-dm`) |
| E4 | 33,2 KB | ~887 KB (GIF 245; sem ele ~642) | ~859 KB | 1.208 KB |

Todas as imagens abaixo de 150 KB, exceto o GIF.

## Precisa de decisão do responsável

1. **D4:** registrar no brief a exceção do GIF (244,9 KB; E4 com ~887 KB no desktop) ou trocar pelo JPG estático recomposto (E4 cai para ~674 KB). Pedir ao cliente foto ou vídeo real da linha Crater Valley em uso para um GIF de lifestyle de verdade.
2. **E3 hero:** aprovar produto sobre paisagem, em vez de foto do hoodie em uso (não existe foto em locação desse produto no banco nem na loja).
3. **E4, ¼ Zip:** packshot APX na moldura e modelo Bottomland no GIF. Outra opção: trocar o link para uma variante que tenha foto de modelo (mudaria o `products.json`, então é decisão do cliente).
4. **Módulos novos para o kit** (quando aprovar): Panel Stack (ref A), Open Frame Rows (ref D), hero com texto à esquerda e modelo sangrando, e Lifestyle GIF.
5. **Outlook app / Gmail no dark mode:** a troca de imagens `-dm` do E3 só acontece no Apple Mail/iOS (mesmo comportamento do E01 da rodada 2). No app do Outlook o papel troca (`dm-tex`) mas as peças dos painéis continuam claras nos cantos. Testar no Litmus antes do envio.
6. Os mesmos pendentes do brief: `{{CTA_URL}}` dos dois e-mails, endereço, tag de descadastro, C7/C8 (variantes M).

## Rodada 2 (2026-09-25)

> Reconstrução de `03-heavy-weight-hoodie.html` e `04-crater-valley.html` pelas imagens do responsável (`email-kit/references/rev-oct-03-heavy-weight-hoodie.png` e `rev-oct-04-crater-valley.png`), seguindo `revision-r2.md`, que vale acima do `brief.md` e das decisões da rodada 1 acima. Render 680, 375 e `--dark` conferido lado a lado com as duas imagens. `compose_B.py` foi reescrito (importa `email-kit/tools/compose.py` sem editar, não depende de `compose_v05.py`); os assets da rodada 1 que saíram (hero de carvalhos, gêmeas `-dm` dos painéis, molduras, `o4-hero-a/b`, borda brown-ivy, GIF e o still) foram apagados de `assets/`.

### O que mudou

**Nos dois**
- Botão `#FF6400` com texto **branco**, Prompt 800 caixa-alta, tracking 2px, raio 4px, 17px; largura fixa medida na imagem (03: 326 e 258px; 04: 290 e 300px). Botão pequeno dos cards do 04: 13px, padding 12px 22px.
- Corpo, cards e rodapé em Prompt (400/500/700/800 carregados). Headlines em duas vozes, em caixa-alta real no HTML.
- Rodapé v0.5: logo empilhado 136px, menu com filetes brancos, ícone do Instagram (`email-kit/assets/icon-instagram.png`) + "Follow us on Instagram" / @HABITOUTDOORS, copyright. **Sem** `[[CONFIRMAR: endereço]]` e sem Unsubscribe no HTML (revision-r2 #5).

**03 Heavy Weight Hoodie**
- Hero com **foto de pessoa** (homem de boné camo no capim), logo vivo `logo-light.png` sobre o céu, YOUR / **COLDEST** (Playfair 98px, branco) / MORNINGS COVERED, subtítulo espaçado e botão sobre a foto escurecendo para Tap Shoe.
- Banda nova de **papel claro com manchas de camo** (`o3-tex-paper-camo.jpg`, gêmea `-dm` para o dark mode), gerada no `compose_B.py`: **WARM** (Playfair 96px, Tap Shoe) / ENOUGH TO SKIP / THE JACKET (Prompt 800 30px), corpo centralizado 18px.
- Painéis Major Brown / Gunmetal / Loden Green, 552px com 24px de margem, 62px entre eles, hoodie subindo 40px acima do painel. Texto: cor em laranja, `Men’s Heavy Weight / Full Zip Hoodie` em branco, `$44.99 USD` Prompt 800 20px **sem sublinhado** (linkado na variante).
- Mecânica nova: como as manchas de camo são grandes, nada opaco carrega o papel. As bordas rasgadas (`o3-edge-hero-paper.png`, `o3-edge-paper-footer.png`) e o topo do hoodie (`o3-panel-*-top.png`) são **PNG transparentes** dentro da `<td>` da banda, e o JPG do painel só tem o painel. Assim o papel corre sem emenda, e as gêmeas `-dm` dos painéis deixaram de existir (a pendência 5 da rodada 1 cai).

**04 Crater Valley**
- Hero à esquerda: MEET THE / **CRATER VALLEY** (Playfair 68px, `#CFC8BF`) / **LINE** (laranja), subtítulo, botão; o Full Zip Fleece no modelo sangra pela direita, cortado abaixo do queixo pela borda de cima do e-mail e sumindo embaixo. Logo abaixo, a **faixa de detalhe** (mão no bolso do tricô) com cantos de cima arredondados e base rasgada.
- Banda em degradê Tap Shoe → Major Brown: YOUR BEST / LAYERING MOVE / **THIS FALL** (Playfair 60px branco), corpo.
- **Cards emoldurados** (contorno 1px `#FEF4C6` a 70% com `rgba`, raio 14): foto da loja à esquerda no fundo de estúdio, a altura toda do card; à direita a caixa de produto (contorno 1px, raio 10, centralizada) com título laranja, descrição, preço e botão pequeno SHOP HOODIE / SHOP FLEECE / SHOP QUARTER ZIP. Mobile: foto em cima, caixa embaixo, dentro do mesmo contorno.
- **Sem GIF.** Fim em banda de foto (silhueta com cachorro no pôr do sol, retícula): FROM FIRST LIGHT TO / **LAST CALL** (Playfair 98px laranja), corpo, SHOP NOW, rasgo para o rodapé.

### Desvios da imagem, e por quê

1. **04, primeiro card:** a imagem diz "YOUTH CEDAR BRANCH"; está `CRATER VALLEY PERFORMANCE HOODIE` / $29.99 (revision-r2). Os três títulos sem "Men's", como os outros dois da imagem e a regra do brief para o E4; o nome da loja tem "Men's" na frente.
2. **Título laranja da caixa de produto em 19px** (03 e 04), onde a imagem mostra uns 16px: é o tamanho que a revision-r2 #4 pede para o laranja contar como texto grande sobre Major Brown (3,46:1). No 03 a caixa fica um pouco mais pesada que na imagem.
3. **04, Full Zip Fleece no card:** a imagem mostra o rosto a partir da testa (corte da loja). Mantive o corte **abaixo do queixo na linha de cima do card** (regra do QA r1: nunca cortar entre a testa e a boca). Card 3 com o packshot APX (a variante do link), como na imagem.
4. **04, faixa de detalhe:** em vez do recorte da imagem, usei a **foto original da loja** (`photos/products/mens-crater-valley-sweater-fleece-zip-jacket/08.png`, 1200px, então 2x). O canto transparente da foto virou estúdio escuro. É a mesma foto da imagem.
5. **04, fundo da banda final:** a imagem é preto chapado; usei `#1E1F21` (cor escura do kit) porque plano grande de `#000` é proibido (rules §2, inversão do Gmail). A foto do pôr do sol esmaece para essa cor.
6. **Ícone do Instagram em 44px**, que é o que a imagem mostra (a revision-r2 diz 36). O arquivo tem 72px (1,6x).
7. **Tipos menores que a faixa da revision-r2 #2 onde a imagem é menor:** THIS FALL 60px e CRATER VALLEY 68px (a imagem manda; a coluna do hero tem 330px).
8. **Fonte:** Prompt (substituto da Sweet Sans) desenha mais estreita que a fonte da imagem, então quebras de linha do corpo e do subtítulo não são idênticas; ajustei larguras para ficar perto (3 linhas onde a imagem tem 3).
9. **Botões por produto no 04** (3 pequenos + hero + fim = 5 botões): é o que a imagem pede e substitui o X5 do brief (links sublinhados). Registrar no brief; rules §6 fala em 2 a 3 CTAs, todos vão para a mesma família.

### Fotos provisórias (recorte 1x, trocar pelo original)

- `assets/o3-rev-hero.jpg`: recorte provisório 1x da `rev-oct-03`, linhas 0 a 470 (antes do "YOUR"), **logo HABIT retocado** (interpolação do céu) e o logo vivo por cima. Abaixo da linha 470 a foto é um espelho desfocado escurecendo para Tap Shoe, porque o texto da imagem cobre o resto do corpo. **Pedir o original** (sessão HabitHunt?): com ele o homem continua atrás da headline como na imagem.
- `assets/o4-rev-sunset.jpg`: recorte provisório 1x da `rev-oct-04`, linhas 2231 a 2494 (entre o rasgo e o "FROM FIRST LIGHT TO"), com rasgo novo sobre o marrom e base esmaecendo para `#1E1F21`. **Pedir o original.**
- Não são provisórias: hero do 04 e cards (fotos da loja em `photos/products/`), faixa de detalhe (loja, 2x), painéis do 03 (packshots da loja).

### Pesos (medidos 2026-09-25)

| | HTML | Desktop claro | Todos os arquivos referenciados |
|---|---|---|---|
| E3 | 31,4 KB | ~544 KB | 765 KB (inclui as peças mobile e o papel `-dm`) |
| E4 | 35,1 KB | ~731 KB | 1.027 KB (inclui hero e cards mobile) |

Maior imagem: `o4-detail-pocket.jpg` 117 KB; todas abaixo de 150 KB. Sem GIF, o E4 volta para dentro dos 800 KB.

### Pendências

1. **Contraste do botão** (texto branco no laranja, 2,97:1, abaixo do AA): exceção pedida pelo responsável, registrar no brief.
2. **Originais das duas fotos provisórias** (acima).
3. **Rodapé sem endereço e sem descadastro no HTML:** conferir no Omnisend que o rodapé automático entra (CAN-SPAM), antes do envio.
4. **Módulos para o kit v0.5:** papel claro com manchas de camo, borda rasgada em PNG transparente, Panel Stack com topo em PNG, Framed Card Row com Product Info Box, rodapé com ícone do Instagram.
5. **Outlook desktop:** cantos arredondados de cards, painéis e fotos ficam retos; o contorno `rgba` cai para `#FEF4C6` cheio (mais claro que na imagem). Testar no Litmus. Gmail app no dark mode: o papel camo claro do 03 pode inverter o `bgcolor` e não a imagem (mesmo WARN da rodada 1).
6. Continuam do brief: `{{CTA_URL}}` dos dois e-mails, URLs do menu e do Instagram, C7/C8 (variantes M).
