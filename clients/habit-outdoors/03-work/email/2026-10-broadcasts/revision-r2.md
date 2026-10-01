# Lote de outubro · rodada 2 (revisão do responsável) · 2026-09-25

O responsável refinou os 5 e-mails e mandou as versões melhoradas (export de 600px):
`clients/habit-outdoors/01-brand/email-kit/references/rev-oct-{01..05}-*.png`.

**Essas imagens são agora a direção de arte aprovada do lote e do kit (v0.5).** Reconstruir os 5 HTML para ficarem iguais a elas (layout, hierarquia, escala, cor, ordem das bandas), em HTML de e-mail com texto vivo. Onde esta página diverge do `brief.md`, vale esta página. O que não é citado aqui continua como no `brief.md` e nas regras do kit.

## Decisões do responsável expressas nas imagens (valem para o lote e para o kit)

1. **Botão:** `#FF6400` com **texto branco** `#FFFFFF`, Prompt 700/800 caixa-alta, tracking 2px, raio 4px, ~17px. Substitui a decisão de 2026-09-24 (texto Tap Shoe). **Contraste 2,97:1, abaixo do AA (4,5 e 3,0).** Registrado como exceção pedida pelo responsável; o QA aponta, não bloqueia. Botão pequeno dentro de card (04): mesma cor, ~13px, padding 12px 22px.
2. **Headline em duas vozes, serifa dominante:** a palavra (ou as palavras) em Playfair Display 900 caixa-alta é a protagonista: **96 a 110px desktop, entrelinha 0,88 a 0,92**, pode quebrar em 2 linhas (BITE / BACK, STARTS / HERE, CEDAR / BRANCH, LAST / CALL). Linha sans (Prompt 800 caixa-alta) menor: 26 a 32px, entrelinha 1,05. Mobile: serifa 64 a 72px, sans 22 a 24px. Cor da serifa: branco, laranja (só sobre Tap Shoe, Patriot Blue, Major Brown ou foto escura), Tap Shoe em papel claro, ou Aluminum claro `#CFC8BF` (04, CRATER VALLEY).
3. **Corpo na sans geométrica:** todo corpo, card e rodapé em **Prompt 400/500** (substituto da Sweet Sans), fallback Helvetica, Arial. Corpo de banda 17px/1,4, **centralizado** sob a headline, branco `#FFFFFF` ou `#E2DDD9` no escuro, `#2A2B2D` no claro. **Nas bandas internas não há subtítulo espaçado**: headline e logo abaixo o corpo. O subtítulo espaçado caixa-alta (15px, tracking 2px) fica **só no hero** e no 01/02 onde a imagem mostra.
4. **Caixa de produto (Product Info Box):** contorno 1px `#FEF4C6` (a ~70%), raio 10px, padding 22px 20px, **texto centralizado**: título Prompt 800 caixa-alta **laranja** `#FF6400` (**19px** / 21px, para contar como texto grande: sobre Major Brown o laranja dá 3,46:1, só passa como grande), linha 2 branca Prompt 500 15px, variante `#B0A89C`/`#CFC8BF` 13px, preço **Prompt 800 20px branco, sem sublinhado**, a caixa inteira linkada na `url` do produto. **Sem os dois traços laranja** nos cantos e sem o "=" laranja.
5. **Rodapé:** logo empilhado, menu MEN'S | WOMEN'S | YOUTH | SALE, ícone colorido do Instagram (`email-kit/assets/icon-instagram.png`, exibido 44x44 (medido na imagem; padronizado no fim da rodada)) ao lado de "Follow us on Instagram" / **@HABITOUTDOORS**, copyright "© 2026, Habit Outdoors. Built By Wilde Creative." **Sem** a linha `[[CONFIRMAR: endereço]]` e sem "Unsubscribe" no HTML (o responsável tirou; endereço e descadastro vêm do rodapé do Omnisend, CAN-SPAM: pendência de envio, não do HTML). Tudo em Prompt.
6. **Rasgos e texturas continuam** (bordas rasgadas entre bandas, grão). Novas superfícies: **papel claro com manchas de camo** (manchas grandes `#D2CCC4` a `#CFC8BF` sobre o papel `#E2DDD9`, 03) e **Major Brown com retícula** (manchas de pontos pretos em meio-tom, 01). Fundo do 05 na banda de atributos: degradê Tap Shoe → Patriot Blue com linhas topográficas.

## Erros de copy nas imagens que NÃO devem ser copiados

- 04, primeiro card: a imagem diz "YOUTH CEDAR BRANCH". O produto é o **Crater Valley Performance Hoodie** ($29.99): usar o nome da loja (`products.json`).
- 05, terceiro card: a imagem tem uma linha "Insulated Bib" a mais na Windproof Fleece Jacket. Tirar; a caixa fica igual às outras duas (nome, variante, preço).
- Nomes, variantes e preços sempre do `products.json`. Copy de headline, corpo e botão: o da imagem (que é o do `copy-source.md`); se divergir do copy-source, anotar nas notas e seguir a imagem.

## E-mail por e-mail (o que mudou)

### 01 Cedar Branch Bibs (`rev-oct-01-cedar-branch-bibs.png`)
- Hero: igual ao nosso (foto dos três caçadores, etiquetas), mas a **última etiqueta "TURNS" é escura** (`#2A2B2D`) com a serifa **laranja**; READY WHEN THE e WEATHER em etiquetas claras. Subtítulo espaçado + botão sobre a base escura.
- Banda Major Brown com retícula: bib grande à esquerda (sangrando, ~45% da largura), à direita THE / **CEDAR BRANCH** (serifa laranja, 2 linhas) / COLLECTION, subtítulo espaçado, corpo, caixa de produto do bib; embaixo, caixa do parka à esquerda e parka sangrando pela direita.
- **Um review só** (Ryan And L.), em banda Tap Shoe: aspas laranja, 5 estrelas laranja, citação centralizada, nome em caixa-alta espaçada `#B0A89C`; parka sangrando pela direita. Os outros dois reviews saem (decisão do responsável; registrar no brief).
- Fim: **banda de foto cheia** (arqueiro de camo), com a linha de pesca desenhada branca, LAYER UP FOR THE / **SEASON** (serifa laranja enorme), corpo, botão SHOP HUNTING largo (~420px), texto sobre a parte escura da foto (degradê para Tap Shoe). Sai a faixa dividida em oliva.

### 02 Youth (`rev-oct-02-youth-season.png`)
- Hero: THEIR SEASON (sans branco) / **STARTS HERE** (serifa laranja, 2 linhas), subtítulo espaçado, botão, foto das cadeiras embaixo.
- Banda Tap Shoe (não marrom): REAL GEAR IN / **SMALLER SIZES** (laranja), subtítulo espaçado, corpo.
- **Card emoldurado grande** por produto (contorno 1px, raio 14px, 24px de margem lateral): metade com packshot sobre **painel de cor chapada** (oliva `#595442`, ferrugem `#8A4B2A` a conferir com a imagem, ardósia `#5E6770`), a outra metade com a caixa de produto centralizada; alternando de lado. Botão SHOP NOW depois.
- Fim em papel claro com rasgo: **foto emoldurada inclinada** (moldura branca ~6px, ~-4°, sombra) do menino à esquerda, BUILT FOR EVERY / **COLD MORNING** (serifa Tap Shoe) à direita, corpo alinhado à esquerda, botão SHOP YOUTH.

### 03 Heavy Weight Hoodie (`rev-oct-03-heavy-weight-hoodie.png`)
- Hero: **foto de pessoa** (homem de boné camo no capim) no lugar do packshot sobre a mata; YOUR / **COLDEST** (serifa branca) / MORNINGS COVERED, subtítulo espaçado, botão.
- Banda papel claro **com manchas de camo**: **WARM** (serifa Tap Shoe enorme) / ENOUGH TO SKIP THE JACKET (sans 30px), corpo centralizado.
- Painéis por cor como já temos (Major Brown, Gunmetal, Loden), com: nome da cor laranja caixa-alta, nome do produto branco em 2 linhas, preço branco negrito **sem sublinhado**. Packshot quebrando o topo do painel como na imagem.

### 04 Crater Valley (`rev-oct-04-crater-valley.png`)
- Hero à esquerda: MEET THE (sans) / **CRATER VALLEY** (serifa Aluminum claro) / **LINE** (serifa laranja), subtítulo espaçado, botão; modelo sangrando pela direita.
- Faixa de **foto de detalhe** (mão no bolso do tricô) com cantos arredondados, logo abaixo do hero.
- Banda escura/marrom: YOUR BEST LAYERING MOVE / **THIS FALL** (serifa branca), corpo.
- **Card emoldurado grande** por produto: foto de modelo à esquerda ocupando a altura toda do card (fundo da foto da loja), caixa de produto à direita com **título laranja, descrição, preço e botão pequeno** (SHOP HOODIE / SHOP FLEECE / SHOP QUARTER ZIP). Todos com a foto à esquerda. **Sem GIF** (sai o GIF; resolve o peso da D4).
- Fim: **banda de foto cheia** da silhueta com cachorro no pôr do sol laranja (com retícula), FROM FIRST LIGHT TO / **LAST CALL** (serifa laranja), corpo, botão, rasgo para o rodapé.

### 05 Shadow Series (`rev-oct-05-shadow-series.png`)
- Hero: foto cheia; **etiqueta escura** "FOR THE MORNINGS THAT" (texto laranja, sans 22px) e **BITE / BACK** (serifa branca ~110px, 2 linhas) sobre a foto; subtítulo espaçado, botão.
- Banda de atributos: THE LINE THAT OUTLASTS / **THE WEATHER** (serifa branca), corpo; os 4 cards como hoje, com **título laranja** e ícone de traço fino com os dois filetes laranja embaixo; fundo degradê Tap Shoe → Patriot Blue topográfico.
- **Tabuleiro**: cada linha 300 + 300, sem margem: metade com packshot sobre **painel chapado** (taupe `#A69A8C`, cinza `#AEB5B8`, marrom `#6B5543`: conferir as cores na imagem), outra metade Patriot Blue com água e a caixa de produto. Alternando. Mobile: empilha, imagem primeiro.
- Botão SHOP NOW em Patriot Blue, depois o rodapé.

## Fotos novas

Os originais das fotos novas não estão na máquina (conferido em Downloads, Desktop, Pictures em 2026-09-25). **Provisório:** recortar das próprias imagens `rev-oct-*` só onde a foto aparece **limpa** (sem texto nem logo por cima; logo sobre céu/fundo calmo pode ser retocado), com o nome `o{nn}-rev-*.jpg`, e anotar "recorte provisório 1x, trocar pelo original" nas notas. Resolução: são 600px, então exibir no máximo em 600px (1x).

- 03 hero (homem no capim): topo da imagem até antes do "YOUR"; retocar o logo HABIT do topo; completar embaixo com degradê para Tap Shoe, texto vivo por cima.
- 01 fim (arqueiro): parte de cima da foto até antes de "LAYER UP" (inclui a linha desenhada); abaixo degradê para Tap Shoe com o texto vivo.
- 04 detalhe do bolso e 04 silhueta no pôr do sol (acima do texto).
- 02 menino: recortar a foto de dentro da moldura, desrotacionar e recompor moldura + inclinação + sombra sobre o nosso papel.
- 05 hero (homem sentado nas pedras): **não recuperável** (o texto cobre o sujeito). Manter a foto atual do 05 com o novo layout de texto, e anotar para pedir o original.

## Entrega de cada designer

HTML atualizado no mesmo nome de arquivo, script de composição próprio atualizado, render 680, 375 e `--dark` conferido lado a lado com a `rev-oct-*` correspondente, notas `notes-{A,B,C}.md` com uma seção "Rodada 2" (o que mudou, desvios, pendências). Peso HTML < 90KB, e-mail < 800KB.
