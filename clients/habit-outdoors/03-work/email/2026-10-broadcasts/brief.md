# October 2026 Broadcasts · brief

## Rodada 2 (2026-09-25)

A direção de arte da rodada 2 está em [`revision-r2.md`](revision-r2.md) (imagens `email-kit/references/rev-oct-01..05-*.png`) e **vale acima deste brief** onde divergir. QA da rodada: [`qa-r2.md`](qa-r2.md). Decisões do responsável registradas aqui:

- **Botão com texto branco** `#FFFFFF` sobre `#FF6400` (2,97:1, abaixo do AA): exceção pedida pelo responsável; substitui o texto Tap Shoe de 2026-09-24. Um estilo só nos 5 (kit v0.5): Prompt 800, 17px, tracking 2px, raio 4px, padding vertical 16px, 52px de altura, largura fixa por botão. Botão pequeno de card (04): 13px, padding 14px 22px, 44px.
- **Endereço e descadastro fora do HTML:** vêm do rodapé do Omnisend (CAN-SPAM, conferir num envio de teste). Substitui a regra de rodapé com `[[CONFIRMAR: endereço]]` e `{{UNSUBSCRIBE_URL}}` deste brief. Rodapé E13 + E14 idêntico nos 5 (logo empilhado, menu, ícone do Instagram 44px, copyright).
- **Um review só no 01** (Ryan And L.); saem Matthew B. e Andrew C.
- **01, Bloco 2: sai o "CTA: Shop Now"** do copy do cliente (a imagem revisada não tem botão nessa banda). Registro de corte de copy (rules §7).
- **04: sai o GIF** (resolve a D4) e o e-mail fica com **5 botões** (hero, SHOP HOODIE / SHOP FLEECE / SHOP QUARTER ZIP nos cards, SHOP NOW no fim), todos para a família Crater Valley. Substitui o X5 e o limite de 3 botões para este e-mail.
- **Fotos provisórias 1x** recortadas das rev-oct (`o1-rev-archer`, `o2-rev-boy`, `o3-rev-hero`, `o4-rev-sunset`); trocar pelos originais antes do envio. Hero do 05 mantém a foto da rodada 1 (a da revisão não é recuperável).
- **Cores de painel:** 02 mantém ferrugem `#774727` e ardósia `#4F5C5F` (desenho revisado do responsável), agora no kit v0.5 como cor de painel de produto (`color.panel_rust`, `color.panel_slate`). Os painéis do 05 seguem as cores medidas da rev-oct-05, ainda para aprovação junto com o kit v0.5.

> Brief do lote (playbook, etapa 3), montado em 2026-09-25. 5 broadcasts avulsos de outubro, sem gatilho nem cadência. Três Email Designers constroem em paralelo **só a partir deste arquivo**: **A** = 01 e 02 · **B** = 03 e 04 · **C** = 05. Tudo que for decidido depois volta pra cá, com data.

Copy-fonte: `copy-source.md` (PDF do cliente, literal, 5 e-mails "Approved") · Produtos: `products.json` (variante exata, preço de 2026-09-25, packshot, **todas** as imagens da loja em `all_images`, descrição em `body_text`) · Kit: `clients/habit-outdoors/01-brand/email-kit/` v0.2 aprovado + v0.3/v0.4 rascunho (texturas, E24 a E26, bordas texturizadas) · Visual de partida: os 4 e-mails da **rodada 2** em `../2026-broadcasts/*.html` e `../2026-broadcasts/art-direction-r2.md` · Estrutura: as 4 referências do cliente (abaixo).

## O pedido, em uma frase

O cliente mandou 4 e-mails de outras marcas **como referência de estrutura**. Manter o **nosso visual** (o da rodada 2: texturas com grão, rasgos, hero de foto em tela cheia com logo branco por cima, duas vozes na headline, botão laranja, rodapé Tap Shoe) e o **conteúdo do cliente**, e trocar o esqueleto das bandas pelo das referências.

## As 4 referências de estrutura (só estrutura)

Arquivos em `email-kit/references/struct-r3-*.png`. **Nunca** levar delas cor, fonte, logo, pastel, cantos de "bolha" ou copy.

| Ref | Arquivo | Estrutura que interessa |
|---|---|---|
| **A** | `struct-r3-a-zigzag-panels.png` | pilha de **painéis separados** (cada produto num painel próprio, com respiro entre eles e margem lateral), produto e texto **alternando de lado**; no texto: título curto, 1 a 2 linhas, link sublinhado em caixa-alta. Cada painel com um tom próprio |
| **B** | `struct-r3-b-checkerboard.png` | título + subtítulo centralizados; **tabuleiro de 2 colunas**: bloco de imagem de produto ao lado de bloco de texto emoldurado (contorno fino, como balão), invertendo a cada linha; nome do produto grande no bloco de imagem; depois uma **faixa de 4 colunas** de serviços/atributos com ícone de traço fino |
| **C** | `struct-r3-c-label-boxes.png` | hero de foto com a headline **em caixas de etiqueta** (faixas chapadas atrás de cada linha, encostando na borda da foto); abaixo, texto e botão centralizados; segunda foto com pergunta em etiquetas; linhas de **produto sangrando + caixa emoldurada de review** (aspas grandes, 5 estrelas, citação, nome); fecha com **faixa dividida** (texto à esquerda, botão à direita, entre dois filetes) |
| **D** | `struct-r3-d-framed-rows.png` | hero com headline **alinhada à esquerda**, botão à esquerda, produto sangrando pela direita; **retrato em círculo** com anel de cor; linhas de produto dentro de **molduras abertas** (contorno fino arredondado com respiro), o produto **quebrando a moldura**, aspas nos cantos, alternando de lado; texto curto + link sublinhado "SHOP X" |

### Como cada estrutura vira Habit (vale para os 5)

- **Painel (A)** = placa de textura da paleta (grão), raio 12px (raio do card do kit), sobre a textura da banda, 24px de margem lateral e 16px entre painéis. Tons dos painéis só da paleta do kit.
- **Moldura / balão (B, D)** = contorno 1px `#FEF4C6` (`color.card_outline`, o contorno dos cards dos e-mails enviados), raio 12px. **No lugar das aspas da ref D**, os **dois traços laranja** do guia nos cantos (só em moldura sobre Tap Shoe, Patriot Blue ou Major Brown). Aspas grandes só onde o texto **é** citação de cliente (E1).
- **Etiqueta (C)** = faixa `#E2DDD9` com grão (`tex-paper-light`) atrás de cada linha da headline, texto `#2A2B2D` em Prompt 800 caixa-alta e a palavra de destaque na Playfair 900. Texto vivo em `<td bgcolor>` sobre a foto de fundo (VML), cada linha numa tabela alinhada, encostando numa borda.
- **Produto quebrando moldura / sangrando** = imagem composta por script (a moldura e o produto na mesma imagem, com a textura da banda nas bordas), nome/tipo/preço **vivos** ao lado.
- **Link sublinhado por produto (A, D)** = o preço sublinhado do kit (`$29.99 USD`) linkado na variante, e, só onde o cliente escreveu CTA por produto (E4), o texto dele em caixa-alta sublinhado. **Não criar "SHOP NOW" por produto** onde o cliente não escreveu.
- **Mobile:** toda linha de 2 colunas empilha, **imagem sempre primeiro** (`dir="rtl"` na tabela das linhas invertidas, `dir="ltr"` nas células). Painéis e molduras viram largura total com 16px de margem.
- **Nosso visual continua:** nenhuma banda chapada (textura em toda banda, VML + `bgcolor`), rasgo em toda fronteira de banda (E18 texturizada ou produto atravessando), hero de foto em tela cheia com logo branco `logo-dark.png` por cima (sem E01), headline em duas vozes, botão único `#FF6400` / texto `#2A2B2D`, rodapé E13 + E14.

## Mapa: referência × e-mail

| E-mail | Estrutura principal | Por quê |
|---|---|---|
| **01** Cedar Branch Bibs · 6/10 | **C** (etiquetas no hero, produto + caixa de review, faixa dividida no fim) | é o único com reviews de cliente de verdade, e a ref C é construída em volta de review |
| **02** Youth · 9/10 | **B** (tabuleiro produto × texto emoldurado) | 3 produtos diferentes, cada um com nome forte; o tabuleiro dá peso a cada peça sem grade 3-up |
| **03** Heavy Weight Hoodie · 13/10 | **A** (painéis alternando, um por cor) | um produto em 3 cores: cada cor ganha um painel no tom da própria cor, como a ref A faz com o tom de cada produto |
| **04** Crater Valley · 22/10 | **D** (hero à esquerda, molduras abertas com produto quebrando, link por produto) | o copy do cliente já vem em linhas alternadas com texto e CTA por produto, exatamente a ref D; "showcase model wearing images" = modelo quebrando a moldura |
| **05** Shadow Series · 29/10 | **B** (faixa de 4 atributos) + **C** (produto sangrando + caixa emoldurada) | os 4 atributos do cliente são a faixa de 4 colunas da ref B; os 3 produtos em linhas de produto sangrando |

## Regras do lote

- **Caixa:** headline, subtítulo, botão e linha 1 do card em maiúsculas reais no HTML (regra do kit). Corpo, linha 2 do card, citações e links de texto como o cliente escreveu.
- **Palavra de destaque:** uma por headline, Playfair 900 (indicada em cada tabela). Laranja só sobre Tap Shoe, Patriot Blue ou Major Brown (grande); em claro fica `#2A2B2D`.
- **Viúva:** `&nbsp;` entre as duas últimas palavras de headline e subtítulo.
- **Botão:** um estilo só, o do kit. No máximo 3 botões por e-mail, todos para a mesma família de produto (rules §6).
- **Bandas:** até 7 contando preheader e rodapé; nenhuma vizinha com a mesma textura.
- **Card de produto:** linha 1 = nome da loja (Prompt 800, caixa-alta), linha 2 = variante/tipo, preço sublinhado `$XX.XX USD` linkado na `url` do `products.json`. Packshot da variante (PNG transparente). **Sem preço riscado** (ver C3, C4).
- **Fotos:** preferir as **originais** novas `photos/lifestyle/orig-*.jpg` (INDEX.md, seção "Originais da Habit") e as fotos de modelo da loja (`all_images` no `products.json`, já baixadas em `photos/products/<handle>/`). `crop-sent-*` só se faltar. Cada foto num único e-mail do lote. Foto de referência externa **nunca** entra.
- **Rodapé (decisão nova, pedido do cliente):** E13 + E14 do kit **mais** uma linha de endereço e o link de descadastro, porque o copy do cliente pede `[Address] [Unsubscribe]` (e o CAN-SPAM também). Endereço = `[[CONFIRMAR: endereço físico da Habit]]` visível; descadastro = `{{UNSUBSCRIBE_URL}}` (tag do Omnisend a confirmar). "© 2026, Habit Outdoors. Built By Wilde Creative." como no kit. `[Social Icons]`: o kit só tem Instagram em texto (@HABITOUTDOORS); manter e deixar `[[CONFIRMAR: outras redes, com ícone]]` no brief, **não** no HTML.
- **Topo do HTML:** comentário com `Subject:`, `Preheader:`, `Modules:`, `Button:` (a ferramenta de preview lê).
- **Peso:** HTML < 90KB; imagens até ~150KB cada e ~800KB por e-mail. Exceção pedida: o GIF do E4 (ver D4).
- **Imagens:** 2x (arquivo 1200px para 600px), JPG 70-80, PNG só com transparência; todas com `alt`.
- **Assets:** `2026-10-broadcasts/assets/o{nn}-*` (o1-, o2-...). Um script de composição por designer (`compose_A.py`, `compose_B.py`, `compose_C.py`) que importa as funções do `email-kit/tools/compose.py` **sem editá-lo** (mesmo esquema de `../2026-broadcasts/compose_03-04.py`). Caminho das imagens no HTML: `assets/...` para as do lote, `../../../01-brand/email-kit/assets/...` para as do kit.
- **Render check** 680, 375 e `--dark` antes de devolver (`python email-ops/tools/render.py <html> --out <pasta> --height 9000`), olhando cada fronteira de banda nas duas larguras.

## Desvios de copy obrigatórios (rules §7, registrados)

| # | Onde | Cliente | No e-mail | Motivo |
|---|---|---|---|---|
| X1 | E1 e E3, assunto | `Gear Up with Cedar Branch 🏔️` · `Stay Warm Without the Bulk ❄️` | sem o emoji | rules §7 proíbe emoji. Responsável pode devolver o emoji se o cliente insistir (é só o assunto) |
| X2 | E1, reviews | `— Matthew B.` · `— Ryan And L.` · `- Andrew C` | nome numa linha própria, sem traço: `Matthew B.` · `Ryan And L.` · `Andrew C.` | proibido travessão/meia-risca; o ponto em "Andrew C." só iguala aos outros dois |
| X3 | E1, reviews | "as gif" | 3 citações em **texto vivo**, uma por caixa, estrelas como caractere `★★★★★` em laranja (não emoji) | texto em imagem é proibido (rules §8) e GIF de review é "carrossel de estrelas" (rules §6). Texto vivo lê com imagem bloqueada, no leitor de tela e no dark mode |
| X4 | E4, lista de produto | `Crater Valley Performance Hoodie — $29.99` | nome e preço em linhas separadas | travessão |
| X5 | E4 e E5, Blocos | vários "CTA: Shop Now" | botão só no hero e no fim; CTAs por produto do E4 (`Shop Hoodie`, `Shop Fleece`, `Shop Quarter Zip`) viram **link de texto** sublinhado; "Shop Now" do Bloco 2 do E4 sai (o Bloco 3 fecha com "Shop Now") | máximo 2 a 3 botões por e-mail (rules §6) |
| X6 | E1, Bloco 2 | `The Cedar Branch collection` | `THE CEDAR BRANCH COLLECTION` | só caixa (regra do kit) |

**Não mexer**, só sinalizar ao responsável: o review do Andrew C. tem 3 pontos de exclamação (rules §7 permite um por e-mail), mas é citação literal de cliente e não se edita citação. Opções: manter, ou o cliente escolhe outro review da página.

## Decisões de construção (pendentes de ok do responsável)

- **D1 · Reviews em texto vivo** (X3). Fallback: GIF com as 3 citações + as mesmas citações em texto vivo embaixo (pesado e repetido; não recomendado).
- **D2 · Detalhe de tecido no E1** ("Texture/detail crops"): recortes de detalhe **das imagens da loja** (zíper de perna, placa de reforço, bolso, tecido), um ao lado de cada review, no lugar do produto da ref C. Sem imagem de detalhe utilizável na loja, usar o packshot recortado de perto.
- **D3 · Rodapé com endereço e descadastro** (acima).
- **D4 · GIF do E4** ("LIFESTYLE GIF OF THE PRODUCTS"): GIF animado de 3 a 4 quadros com as fotos de modelo da loja, crossfade curto, loop, 600px (arquivo 600 ou 1200 conforme o peso), **até ~350KB** (exceção ao limite de 150KB). O **primeiro quadro** precisa funcionar sozinho (Outlook desktop só mostra ele). Fallback: JPG estático.
- **D5 · Bota/produto repetido:** o E5 lista o Mid Layer Hooded Jacket duas vezes em "Product to Feature"; os links são 3 produtos diferentes. Construir com os **3 links**.

## Para revisão do cliente (nada foi mudado)

- **C1 · Datas:** o PDF diz "Tuesday" nos 5, mas **9/10 é sexta, 22/10 é quinta e 29/10 é quinta** em 2026. Só 6/10 e 13/10 são terça.
- **C2 · Títulos x produtos:** E2 se chama "Youth Country Trek Bib + Jacket", mas os produtos são Cedar Branch Bib, Summit Park Hoodie e Bear Cave Pant (nenhum Country Trek, nenhuma jaqueta). E5 se chama "Shadow Series Insulated Jacket + Bib", mas os produtos são Mid Layer Hooded Jacket, Windproof Fleece Pant e Windproof Fleece Jacket (nenhum bib). O título não aparece no e-mail; só confirmar que os produtos estão certos.
- **C3 · Shadow Series em promoção:** os 3 estão a **$69.98** na loja (compare_at $99.99). O copy fala em "highest-ticket items" e não cita desconto. Construído com $69.98 e sem preço riscado. Confirmar preço do dia 29/10 e se o cliente quer mostrar a oferta.
- **C4 · Parka:** preço $99.99 com compare_at $89.99 (menor). Mostrado só $99.99.
- **C5 · Claims:** conferidos no `body_text` da loja e batem (Rain-Factor, Scent-Factor, tricot silencioso, isolamento, windproof, bambu anti-odor, sherpa com gola alta e bolso de pressão, cós com bainha, spandex). Atenção: "Grid Fleece Interior" só aparece no Mid Layer (a calça e a jaqueta Windproof são forradas de sherpa); "handwarmer pockets" do E3 na loja é "hand pockets"; "Rain-Factor waterproofing" do E1/E2 bate, mas no Shadow Series é "water repellent" (o copy do E5 já diz repellent, ok).
- **C6 · Reviews:** confirmar que as 3 citações são da página do produto e podem ser usadas com o nome (o copy diz "from the page").
- **C7 · Heavy Weight Hoodie:** o cliente mandou Gunmetal e Loden Green sem variante; resolvidas por cor (tamanho M, como a Major Brown). Links com `/collections/mens/` no PDF; usamos `/products/...?variant=` (mesma página).
- **C8 · Variantes:** todos os links levam ao tamanho M pré-selecionado (Youth: S). Confirmar.
- **C9 · Fotos originais** `orig-*` (HabitHuntFinals, TwoFisted): confirmar liberação para e-mail.

## E1 · Cedar Branch Bibs · `01-cedar-branch-bibs.html` · Designer A · estrutura **C**

Subject: `Gear Up with Cedar Branch` (X1) · Preheader: `Waterproof, insulated, and built for what the season brings.`
Clima: primeira manhã fria de caça, sol nascendo, capim. Destino: `{{CTA_URL}}` (coleção Cedar Branch / hunting, [[CONFIRMAR]]).

| Banda | Estrutura (ref) | Conteúdo |
|---|---|---|
| 1 Preheader | escondido | preheader |
| 2 Hero | **C: foto em tela cheia** `orig-hunt22-three-hunters-field-sunrise.jpg`, logo branco em cima, headline em **etiquetas** `#E2DDD9` encostadas numa borda da foto, uma linha por etiqueta: `READY WHEN THE` / `WEATHER` (destaque Playfair) / `TURNS`. Abaixo da foto (ou na base escurecida dela), subtítulo e botão centralizados. Rasga para a banda 3 | H1 `READY WHEN THE WEATHER&nbsp;TURNS` (destaque: WEATHER) · sub `WATERPROOF, WINDPROOF, AND BREATHABLE INSULATION BUILT TO HANDLE WHATEVER THE SEASON THROWS AT&nbsp;YOU.` · botão `SHOP CEDAR BRANCH` |
| 3 Produtos | **C: linhas de produto sangrando + caixa emoldurada**, 2 linhas alternando (Bibs com imagem à esquerda, Parka à direita), na caixa: nome, tipo, preço. Textura Major Brown ou Tap Shoe | H2 `THE CEDAR BRANCH COLLECTION` (destaque: CEDAR BRANCH) · sub `QUIET FABRIC WITH WEATHER&nbsp;PROTECTION.` · corpo `Soft tricot fabric, Rain-Factor waterproofing, and full insulation make the Cedar Branch your go-to when temperatures drop and conditions get rough.` · 2 cards (products.json email 01) |
| 4 Prova | **C: detalhe + caixa de review**, 3 linhas alternando: recorte de detalhe (D2) ao lado de uma caixa emoldurada com aspas grandes, `★★★★★` laranja, citação e nome. Textura diferente da banda 3. Botão no fim | 3 reviews literais (X2, X3) · botão `SHOP NOW` |
| 5 Fechamento | **C: faixa dividida** entre dois filetes `#FEF4C6`: à esquerda headline + corpo, à direita botão (no mobile empilha, botão largura total) | H2 `LAYER UP FOR THE&nbsp;SEASON` (destaque: SEASON) · corpo `Pair the bibs with the Cedar Branch Parka or Bomber for full coverage from stand to field. Waterproof, windproof, and warm enough for the worst mornings of the year.` · botão `SHOP HUNTING` |
| 6 Rodapé | E13 + E14 + D3 | |

3 botões (hero, prova, fechamento). Se ficar pesado, o botão da banda 4 vira link de texto `Shop Now`.

## E2 · Youth · `02-youth-season.html` · Designer A · estrutura **B**

Subject: `Gear The Kids Up for the Season` · Preheader: `Youth outerwear built to the same standards as the adult line.`
Clima: família, criança no campo, outono. Youth usa o tom `color.line_youth` `#7F7064` (taupe, texto branco) do kit. Destino: `{{CTA_URL}}` (coleção Youth, [[CONFIRMAR]]).

| Banda | Estrutura (ref) | Conteúdo |
|---|---|---|
| 1 Preheader | | |
| 2 Hero | foto em tela cheia **centralizada** (abertura da ref B: título e subtítulo centralizados). Foto com criança: `crop-sent-sep15-family-forest-walk.jpg` ou `crop-sent-sep15-camp-chairs-family.jpg` (conferir no INDEX; se houver foto de modelo youth na loja em locação, preferir) | H1 `THEIR SEASON STARTS&nbsp;HERE` (destaque: SEASON) · sub `YOUTH OUTDOOR GEAR BUILT FOR REAL DAYS IN THE&nbsp;FIELD.` · botão `SHOP YOUTH` |
| 3 Estrutura | **B: título centralizado + tabuleiro**: 3 linhas, cada uma = bloco de produto (packshot grande sobre painel taupe com grão, nome em cima em caixa-alta) + bloco de texto (moldura `#FEF4C6` tipo balão com tipo, preço sublinhado), alternando lado. Botão embaixo | H2 `REAL GEAR IN SMALLER&nbsp;SIZES` (destaque: SMALLER) · sub `BUILT FOR KIDS WHO TAKE THE OUTDOORS&nbsp;SERIOUSLY.` · corpo `The Cedar Branch Bib gives them the same Rain-Factor waterproofing and quiet tricot fabric you trust in the adult version.` · 3 produtos (email 02) · botão `SHOP NOW` |
| 4 Fechamento | banda curta de texto sobre textura, com um visual (Summit Park Hoodie + Cedar Branch Bib juntos, composição "um por baixo do outro", ou foto) | H2 `BUILT FOR EVERY COLD&nbsp;MORNING` (destaque: COLD) · corpo `Layer the Summit Park Hoodie under the Cedar Branch Bib. They're covered from the stand to the truck.` · botão `SHOP YOUTH` |
| 5 Rodapé | E13 + E14 + D3 | |

## E3 · Heavy Weight Hoodie · `03-heavy-weight-hoodie.html` · Designer B · estrutura **A**

Subject: `Stay Warm Without the Bulk` (X1) · Preheader: `Heavyweight warmth in three colors for whatever fall throws at you.`
Clima: manhã gelada, conforto, camada única. Destino: `{{CTA_URL}}` (página do hoodie, [[CONFIRMAR]]).

| Banda | Estrutura (ref) | Conteúdo |
|---|---|---|
| 1 Preheader | | |
| 2 Hero | foto em tela cheia com o hoodie em uso (foto de modelo da loja em `photos/products/mens-heavy-weight-full-zip-hoodie/`, ou foto original + o hoodie composto); logo branco em cima | H1 `YOUR COLDEST MORNINGS&nbsp;COVERED` (destaque: COLDEST) · sub `A HEAVYWEIGHT FULL ZIP HOODIE THAT KEEPS YOU OUTSIDE WHEN THE TEMPERATURE SAYS&nbsp;OTHERWISE.` · botão `SHOP THE HOODIE` |
| 3 Estrutura | **A: pilha de painéis** alternando lado, **um painel por cor, no tom da cor**: Major Brown `#483F39` (tex-grain-brown), Gunmetal (tom cinza-grafite da paleta, Tap Shoe `#2A2B2D` ou `#34353A` com grão), Loden Green (Ivy Green `#595442`, tex-grain-ivy). No painel: packshot da cor saindo do painel, nome da cor como título do painel (`MAJOR BROWN`), nome do produto, preço sublinhado. Banda de fundo em textura clara (papel) para os painéis escuros aparecerem. Botão embaixo | H2 `WARM ENOUGH TO SKIP THE&nbsp;JACKET` (destaque: WARM) · corpo `Soft heavyweight fabric with just enough stretch to move with you, plus handwarmer pockets and a banded hem that cuts the bulk.` · 3 variantes (email 03) · botão `SHOP NOW` |
| 4 Rodapé | E13 + E14 + D3 | |

Curto (2 blocos): tudo bem, é o copy do cliente. Linha 1 do painel = cor (é o que diferencia os 3); nome do produto na linha 2.

## E4 · Crater Valley · `04-crater-valley.html` · Designer B · estrutura **D**

Subject: `One Line That Does It All` · Preheader: `Three layers that work together` (curto, 31 caracteres; manter)
Clima: dia inteiro, trilha, cidade, fogueira; mais leve e versátil que os de caça. Destino: `{{CTA_URL}}` (coleção Crater Valley, [[CONFIRMAR]]).

| Banda | Estrutura (ref) | Conteúdo |
|---|---|---|
| 1 Preheader | | |
| 2 Hero | **D: headline alinhada à esquerda, botão à esquerda, as 3 peças (ou modelo) sangrando pela direita**, sobre foto/textura; logo branco em cima. Pode ter o **círculo** da ref D com uma foto de modelo, anel `#FEF4C6` ou laranja | H1 `MEET THE CRATER VALLEY&nbsp;LINE` (destaque: CRATER VALLEY) · sub `A HOODIE, A FLEECE, AND A QUARTER ZIP THAT PAIR TOGETHER AND HANDLE ANYTHING THE DAY&nbsp;THROWS.` · botão `SHOP CRATER VALLEY` |
| 3 Estrutura | **D: 3 molduras abertas**, uma por produto, alternando lado **na ordem e no lado que o cliente pôs** (hoodie: imagem esquerda/texto direita · fleece: texto esquerda · quarter zip: imagem esquerda). Foto de modelo da loja quebrando a moldura; traços laranja nos cantos. Texto: nome, preço, frase do cliente, link sublinhado com o CTA do cliente | H2 `YOUR BEST LAYERING MOVE THIS&nbsp;FALL` (destaque: LAYERING) · sub `SOLO ON MILD DAYS OR STACKED TOGETHER WHEN THE COLD HITS&nbsp;HARDER.` · linhas: `CRATER VALLEY PERFORMANCE HOODIE` / `$29.99 USD` / `Bamboo-blend fabric with moisture-wicking and anti-odor tech. Your base layer for everything.` / `SHOP HOODIE` · `CRATER VALLEY FULL ZIP FLEECE JACKET` / `$49.99 USD` / `Sherpa fleece with a high standing collar and snap chest pocket. Warmth you can throw on fast.` / `SHOP FLEECE` · `CRATER VALLEY SWEATER FLEECE ¼ ZIP JACKET` / preço da loja `$54.99 USD` (o PDF não traz) / `Clean enough for town, warm enough for the trail. A quarter zip that goes anywhere.` / `SHOP QUARTER ZIP` (X4, X5) |
| 4 Estilo de vida | **GIF (D4)** de largura total, rasgado em cima/embaixo, e texto + botão | H2 `FROM FIRST LIGHT TO LAST&nbsp;CALL` (destaque: FIRST LIGHT) · corpo `Trail in the morning, lunch in town, campfire after dark. Crater Valley layers handle the whole day without a change.` · botão `SHOP NOW` |
| 5 Rodapé | E13 + E14 + D3 | |

Nome dos produtos: o do copy do cliente (sem "Men's"), que é o que ele aprovou; o da loja tem "Men's" na frente.

## E5 · Shadow Series · `05-shadow-series.html` · Designer C · estrutura **B + C**

Subject: `Late Season Calls for Shadow Series` · Preheader: `The gear that keeps you hunting when everyone else heads home.`
Clima: fim de temporada, frio duro, mata escura, silêncio. O mais escuro do lote. Destino: `{{CTA_URL}}` (coleção Shadow Series, [[CONFIRMAR]]).

| Banda | Estrutura (ref) | Conteúdo |
|---|---|---|
| 1 Preheader | | |
| 2 Hero | foto em tela cheia `orig-hunt40-hunter-forest-back.jpg` (vertical, mata) ou `orig-hunt50-hunter-oaks-autumn.jpg`, escurecida e mais fria para "late season"; logo branco | H1 `FOR THE MORNINGS THAT BITE&nbsp;BACK` (destaque: BITE BACK) · sub `SHADOW SERIES IS BUILT FOR THE LATE-SEASON DAYS THAT TEST EVERYTHING YOU'RE&nbsp;WEARING.` · botão `SHOP SHADOW SERIES` |
| 3 Estrutura | **B: faixa de atributos** em 2x2 no desktop (4 colunas não cabem o texto do cliente em 600px; 2x2 é a mesma faixa dobrada) e 1 coluna no mobile: cada célula com moldura `#FEF4C6`, um ícone de traço fino desenhado por script em `#FEF4C6`/laranja (gota, folha/nariz, grade, vento), nome em caixa-alta e a frase | H2 `THE LINE THAT OUTLASTS THE&nbsp;WEATHER` (destaque: OUTLASTS) · sub `SHADOW SERIES HANDLES THE WORST LATE-SEASON WEATHER SO YOU CAN STAY OUT&nbsp;LONGER.` · `RAIN-FACTOR` Water repellent protection that keeps you dry · `SCENT-FACTOR` Scent inhibitor tech that keeps you undetected · `GRID FLEECE INTERIOR` Trapped warmth without the weight or bulk · `WINDPROOF CONSTRUCTION` Blocks cold wind so you can sit longer |
| 4 Produtos | **C: linhas de produto sangrando + caixa emoldurada**, 3 linhas alternando, na caixa nome, tipo/cor (Mossy Oak Terra Coyote), preço | 3 produtos (email 05) · botão `SHOP NOW` |
| 5 Rodapé | E13 + E14 + D3 | |

Ícones: não existem no kit. Gerar por script, traço 2px, 48px (arquivo 96px PNG transparente), e propor como assets do kit.

## Decisões registradas

- 2026-09-25: lote de outubro confirmado pelo responsável ("são 5 e-mails"; é o PDF (2), não os 4 do lote de maio em `../2026-broadcasts/`, que ficam como estão). Referências do cliente = estrutura; visual = rodada 2; conteúdo = PDF. Email Designer (orquestração).
- 2026-09-25: 4 fotos originais da Habit encontradas em Downloads e levadas para `photos/lifestyle/orig-*` (2400px).
- 2026-09-25 (construção): E1 e E2 pelo Designer A (`notes-A.md`), E3 e E4 pelo B (`notes-B.md`), E5 pelo C (`notes-C.md`). As decisões de cada um estão nesses arquivos e valem como parte deste brief. Fotos do lote sem repetir: E1 `orig-hunt22`, E2 `crop-sent-sep15-camp-chairs-family`, E3 metade direita da `orig-hunt50` sem o caçador, E4 fundo do GIF com a faixa esquerda da `crop-sent-sep10-utv-hunters`, E5 `orig-hunt40`.
- 2026-09-25 (QA r1, `qa-r1.md`): o QA bloqueou o E1 (produtos pequenos e detalhes D2 que não liam) e o E4 (rostos cortados na altura dos olhos e peso de 978 KB). Os dois foram corrigidos pelos designers. O ® entrou em Rain-Factor® e Scent-Factor® no E1, no E2 e no E5 (regra do kit, igual ao A2 da rodada 2).
- **X7** (E1, reviews): tiradas as aspas retas das citações do Matthew B. e do Ryan And L., porque a aspa grande laranja já marca a citação. As palavras não mudaram. Cada review está num `<blockquote>`.
- **D4 como construído:** o GIF do E4 tem 3 cenas, pesa 245 KB e troca de cena sem crossfade. Com ele, o E4 fica em cerca de 887 KB de imagem, **acima dos 800 KB: exceção a aprovar**. O JPG estático de reserva (`o4-lifestyle-still.jpg`) deixa o e-mail em cerca de 674 KB.
- **Pendente de ok do responsável:** duas bandas de estrutura no E5 (atributos e produtos, rules §3). E3 com o hero de packshot sobre paisagem, porque a loja não tem foto do hoodie em uso.

## Em aberto

- D1 a D5 · X1 a X6 · C1 a C9 acima.
- [[CONFIRMAR]] URLs de destino (`{{CTA_URL}}` de cada e-mail), endereço físico, tag de descadastro do Omnisend, outras redes sociais.
- Aprovação do kit v0.4 (texturas, E24 a E26) e dos módulos novos que saírem deste lote (etiqueta, tabuleiro, painel, moldura aberta, faixa dividida, faixa de atributos, caixa de review).

## Envio

- (vazio)
