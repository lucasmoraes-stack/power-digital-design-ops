# November 2026 Broadcasts · brief

> Brief do lote (playbook, etapa 3), montado em 2026-10-07 pelo Email Designer. 5 broadcasts avulsos de novembro, sem gatilho nem cadência, lista inteira. Construção (etapa 4) e conferência de render (etapa 5, sem publicação) feitas no mesmo dia; QA (etapa 6) e publicação ficam com o responsável.

**Fontes:** copy `copy-source.md` (PDF do cliente, literal; 01, 03 e 04 "Approved", 02 e 05 "Needs Edit") · produtos `products.json` (variante exata, preço da loja em 2026-10-07, todas as imagens da loja) · kit `clients/habit-outdoors/01-brand/email-kit/` **v0.5 tratado como kit vigente deste lote** (pedido do responsável; no README do kit a v0.5 ainda está como rascunho) · visual aprovado: os 5 e-mails de outubro rodada 2 (`../2026-10-broadcasts/`) e as revisões do responsável `email-kit/references/rev-oct-01..05-*.png` · estrutura: as 7 referências Duck Camp em `references/` (renders em `references/renders/`).

**Arquivos:** `01-womens-cedar-branch.html` · `02-gift-guide-1.html` · `03-buck-hollow-2.html` · `04-heavyweight-flannel.html` · `05-gift-guide-2.html` · imagens em `assets/` (todas geradas por `compose_assets.py`) · HTML gerado por `build_emails.py` · `lint_layout.py` · renders em `renders/` (680, 375, e as duas em `-dark`).

---

## Regra-mestra do lote: o conteúdo do cliente não muda

Decisão do responsável (2026-10-07): "não é para alterar nada no conteúdo". Toda headline, subheadline, copy, nome de produto, linha de produto e CTA entra **exatamente** como está em `copy-source.md`, inclusive o que parece erro (lista "Pontos para o cliente" abaixo). Nada foi cortado, acrescentado ou reordenado. Só o tratamento tipográfico que o kit manda:

- maiúsculas reais em headline, subheadline, botão e título de item;
- apóstrofo tipográfico (`'` vira `’`);
- as duas últimas palavras de cada parágrafo presas (sem viúva);
- quebra de linha da headline em duas vozes (as palavras e a ordem são as do cliente; só a divisão em linha sans e linha serifada é nossa);
- o travessão do título "Men's Summit Park Performance Hoodie — $39.99" sai porque o nome vai na linha de título e `$39.99 USD` vai na linha de preço (regra da operação: nenhum travessão em texto de marketing);
- o colchete da linha "[Available in Basecamp Plaid Rifle Green and Basecamp Plaid Major Brown]" sai; a frase entra como texto (ver ponto 12).

Nome de produto em cada card = o nome que o cliente escreveu no copy (não o da loja). Preço = o da loja em `products.json`, no formato do kit (`$29.99 USD`, sem sublinhado, sem preço riscado).

## Decisões do lote (2026-10-07)

1. **Kit v0.5 como régua:** headline em duas vozes (Playfair 900 + Prompt 800), corpo em Prompt, botão `#FF6400` com texto branco (exceção AA do responsável, 2,97:1), caixa de produto E27, texturas e rasgos texturizados (E18), rodapé E13 + E14.
2. **Um conjunto de componentes para os 5** (`build_emails.py`): botão, botão pequeno de card, caixa E27, headline, rasgo e rodapé saem da mesma função nos 5 e-mails. Resolve os achados G1, G2 e G3 do QA de outubro (botão, caixa e rodapé diferentes entre e-mails). Botão: Prompt 800 17px, tracking 2px, raio 4px, padding 16px, 52px de altura, largura por botão. Botão pequeno: 13px, padding 14px 22px, 44px.
3. **Rodapé:** E13 + E14 do kit v0.5 (logo empilhado, menu MEN'S | WOMEN'S | YOUTH | SALE, ícone do Instagram 44px, copyright). O rodapé do PDF (`[Social Icons]`, `Copyright © [Year]`, `[Address] [Unsubscribe]`) **não** entra: endereço e descadastro vêm do rodapé do Omnisend (decisão do kit; conferir num envio de teste, CAN-SPAM).
4. **Nenhum review, kicker, selo ou texto que o cliente não escreveu.** O copy de novembro não traz review; o E32 não foi usado.
5. **Serifa da headline com fallback Georgia no Outlook** (classe `serif` em todo span da Playfair): resolve o G4 do QA de outubro.
6. **Rasgos casados com a textura de cima:** cada rasgo (E18) é gerado depois de o HTML ser montado: o script mede no Chrome a altura da banda de cima (coluna de 600px) e começa a textura do rasgo na mesma linha do tile em que a banda termina. Com isso, camo, retícula, água e linhas topográficas continuam sem degrau logo acima do rasgo. No celular a textura escala e a emenda pode aparecer (grão fino, quase invisível; camo e retícula, discreta).
7. **Dark mode** (Apple Mail / app do Outlook): bandas escuras fixas; as bandas de papel claro e de papel camo trocam textura e cor de texto; todo produto e detalhe sobre papel claro é PNG transparente (serve nos dois modos); os rasgos que tocam papel claro têm gêmeo `-dm`; logo escuro do 04 escondido inline e revelado no dark.
8. **Um hero diferente por e-mail e nenhum layout de bloco repetido entre os 5** (tabela abaixo).
9. **Bandas:** nenhum e-mail passa de 5 bandas (contando preheader e rodapé). Nenhuma vizinha com a mesma superfície.

### Hero e blocos por e-mail (nada se repete entre os 5)

| E-mail | Hero | Bloco de estrutura | Bloco de fechamento |
|---|---|---|---|
| 01 | grupo de produtos sobre Ivy Green (headline, grupo, subtítulo, botão) | pilha de produtos, um por faixa escura (Major Brown / papel Tap Shoe / Major Brown, rodada 2), separados por rasgos | as três peças de costas à esquerda sobre Ivy, texto à direita, botão largo (rodada 2) |
| 02 | colagem de 4 fotos emolduradas, rasgando na banda seguinte | grade 2-up de cards emoldurados (painel chapado + E27) | headline em largura total, foto inclinada (cartão-presente) ao lado do texto (rodada 2) |
| 03 | dividido: texto à esquerda, modelo recortado à direita cortado pelo rasgo (papel Tap Shoe, rodada 2) | sistema jaqueta + calça com 4 rótulos de texto (rodada 2, sem círculos); depois tabuleiro E28 | (sem bloco de fechamento no copy) |
| 04 | headline serifada em cima de uma foto emoldurada reta | história de produto: mosaico de detalhes, par de cores, linha de disponibilidade, caixa E27 | (sem bloco de fechamento no copy) |
| 05 | foto em tela cheia com texto embaixo (E24B), recorte próprio no celular (rodada 2) | lista de preços em 3 faixas de linhas de produto (E07), em zigue-zague (rodada 2) | foto rasgada (caçador entre carvalhos) em cima, texto centralizado embaixo (rodada 2) |

## Referências: o que foi usado de cada uma (só estrutura)

Proposta de `references/README.md` revista. Nunca levado da Duck Camp: cor, fonte, logo, copy, rodapé (Get First Shot, fotos de loja, pato), selo NEW, bolinhas de cor.

| E-mail | Referência | O que veio dela | Por que esta e não a proposta |
|---|---|---|---|
| 01 | **ref1** (New Terrain Guard) + **ref5** (Pheasants Forever) | ref1: pilha de produtos centralizada, um por faixa, separados por rasgo de papel; ref5: hero com os produtos agrupados entre a headline e o texto | mantém a proposta para a pilha; o hero de grupo da ref5 entra aqui (em vez de no 05) porque o 01 apresenta "as coleções feitas para ela" e não temos foto de uso feminina no banco |
| 02 | **ref2** (Fall '26) | colagem de fotos emolduradas fora do eixo, sobrepostas | igual à proposta: o gift guide pede clima de "momentos ao ar livre", e a colagem mostra campo e água como o subtítulo ("from the field to the water") |
| 03 | **ref4** (3L Rain Shell) + **ref3** (Deck System) + **referência do cliente** (anúncio de Meta, PDF p.5) | ref4: hero de lançamento; ref3: rótulos curtos de característica ao lado das fotos; cliente: sistema inteiro com 4 detalhes em círculo | a referência do próprio cliente manda no bloco 2; as Duck Camp só no hero |
| 04 | **ref6** (Brush Overalls) + **ref7** (Brush Field Apron) | história de um produto só: título sobre foto de uso, produto ao lado dos detalhes, mosaico de fotos | igual à proposta |
| 05 | **ref1** (pilha de produtos com rasgos, aqui como faixas de preço) + **ref5** (texto centralizado com um CTA no fechamento) | lista vertical separada por rasgos; fechamento centralizado | a proposta punha a ref5 no hero do 05; o hero de grupo foi para o 01, e o 05 abre com foto em tela cheia (único hero de foto do lote) |

---

## E-mail 01 · qui 5/11 · Women's Cedar Branch Bib + Parka

- **ICP:** *Passionate Hunter & Weekend Angler* (mulher que caça) · medo: roupa feminina que é só versão menor da masculina, sem tecnologia de verdade · precisa: desempenho confiável a preço justo. **Mensagem-chave** (Strategy Report): "products work hard" (sem condição pendente). **Mensagem única:** tem linha feminina completa, impermeável e isolada, da cabeça aos pés.
- **Assunto:** Her Gear Is Field Ready 🦌 (25 caracteres) · **Preheader:** Insulated and waterproof from head to toe
- **Botão:** `#FF6400` / `#FFFFFF` · hero SHOP WOMEN'S → `{{WOMENS_URL}}` · fechamento SHOP WOMEN'S COLLECTION → `{{WOMENS_COLLECTION_URL}}` · produtos SHOP BIBS / SHOP PARKA / SHOP SHERPA SHELL → URLs do copy.

| # | Banda | Módulo | Superfície | Conteúdo |
|---|---|---|---|---|
| 1 | preheader | | | texto do cliente |
| 2+3 | hero | E24 (logo sobre a banda) + grupo de produtos (variante do E19, ver "Módulos para o kit") | `tex-grain-ivy` (linha Women's) | COLD WEATHER / **COVERED**, grupo (parka, bib atrás, sherpa) num só chão com sombra comum, subtítulo, botão |
| — | rasgo | E18 | ivy → papel claro | |
| 4 | estrutura | E25 + pilha de 3 produtos | papel claro / papel camo / papel claro, com rasgos | THREE WAYS TO OWN THE / **SEASON**, subtítulo, copy; cada produto: packshot, título (nome do cliente), linha, preço, botão pequeno |
| — | rasgo | E18 | papel claro → Major Brown | |
| 6 | última chamada | E26 + E25 | `tex-grain-brown` | 3 detalhes de tecido emoldurados (exterior Realtree APX, passa-cinto, interior sherpa do Early Dawn), EXPLORE THE / **FULL** / COLLECTION, copy, botão largo |
| 7 | rodapé | E18 + E13 + E14 | | |

| Produto (nome do cliente) | Variante | Preço (loja 2026-10-07) | Imagem |
|---|---|---|---|
| Women's Cedar Branch Insulated Waterproof Bibs | Realtree APX / S | $99.99 USD | packshot da variante |
| Women's Cedar Branch Insulated Parka | Realtree APX / S | $89.99 USD (compare-at igual) | packshot da variante |
| Women's Early Dawn Sherpa Shell Jacket | Realtree APX / S | $69.99 USD (compare-at igual) | packshot da variante; detalhes = imagens 03, 04 (recortada sem os selos impressos) e 05 da loja |

Assets: `n1-hero-group.jpg`, `n1-p-bib.png`, `n1-p-parka.png`, `n1-p-sherpa.png`, `n1-closing-details.jpg`, rasgos `n1-edge-*`. Cor da linha: Ivy Green (`color.line_womens` do kit). O Violet Dusk do guia (cor de Women's, p.17) não está no kit, por isso não foi usado (pergunta abaixo).

## E-mail 02 · ter 10/11 · Gift Guide #1 (copy "Needs Edit")

- **ICP:** quem compra presente para o *Weekend Outdoor Adventurer* / *Passionate Hunter & Weekend Angler* · medo: errar o presente · precisa: escolhas certas e fáceis. **Mensagem-chave:** "products work hard" + "outstanding value" (sem número). **Mensagem única:** seis peças certeiras para presentear, e o cartão-presente para quem não sabe.
- **Assunto:** The Outdoor Gift Guide Is Here 🎁 (32) · **Preheader:** Gear they'll reach for all season long
- **Botão:** hero SHOP GIFT GUIDE → `{{GIFT_GUIDE_URL}}` · cards com o CTA do cliente → URLs do copy · SHOP GIFT CARDS → URL do copy (com variante).

| # | Banda | Módulo | Superfície | Conteúdo |
|---|---|---|---|---|
| 1 | preheader | | | |
| 2+3 | hero | colagem (E22 usado como hero, ver "Módulos para o kit") | `tex-paper-tapshoe`, a colagem rasga direto na banda 4 | THE OUTDOOR LOVER'S / **GIFT LIST** (laranja), subtítulo, botão, colagem: caçadores no UTV, pescador na caixa de iscas, caçador saindo do blind, truta na mão |
| 4 | estrutura | E25 + cards 2-up (moldura do E17/E29, texto do E27), 3 linhas | `tex-grain-patriot-water` | OUR / **TOP PICKS** / THIS SEASON, subtítulo, copy, 6 cards (painel chapado + packshot, título laranja 17px, linha, preço, botão pequeno) |
| — | rasgo | E18 | Patriot → papel claro | |
| 5 | mudança de ângulo | E31 | `tex-paper-light` | cartão-presente inclinado 4° (imagem da loja), **NOT SURE** / WHAT TO GET THEM, subtítulo, copy, botão |
| 7 | rodapé | E18 + E13 + E14 | | |

| Produto (nome do cliente) | Variante | Preço | Painel |
|---|---|---|---|
| Men's Flushing Bay Short Sleeve Fishing Shirt | Sedona Sage / M | $29.99 USD | Aluminum |
| Men's Flushing Bay Long Sleeve River Fishing Shirt | Peach Nectar / M | $34.99 USD | ardósia `#4F5C5F` |
| Men's Cedar Branch Insulated Waterproof Bomber | Realtree APX / M | $74.99 USD | Dusk |
| Men's Summit Park Performance Hoodie | Woodland Ghost Khaki / M | $39.99 USD (bate com o "$39.99" do copy) | Turkish Coffee |
| Men's 800gram Insulated 15" Waterproof Rubber Boots | Realtree Edge / 7 | $89.99 USD | Ivy Green |
| Knit Camo Stocking Cap | Brown Camo | $12.99 USD | Dusk |
| Habit Outdoors Gift Card | (variante $50 no link) | sem preço no e-mail (o copy não mostra valor; "any amount") | imagem da loja |

## E-mail 03 · qui 19/11 · Buck Hollow 2.0 Jacket & Pant

- **ICP:** *Hardcore Hunter & Devoted Angler* · medo: barulho e água no fim de temporada · precisa: precisão técnica, conjunto que funciona junto. **Mensagem-chave:** "products work hard". **Mensagem única:** jaqueta e calça Buck Hollow 2.0, impermeáveis e silenciosas, feitas como sistema.
- **Assunto:** Buck Hollow 2.0 Is Here 🦌 (25) · **Preheader:** Waterproof, quiet, and built as a set
- **Botão:** hero SHOP BUCK HOLLOW 2.0 → `{{BUCK_HOLLOW_URL}}` · SHOP JACKET / SHOP PANT → URLs do copy.

| # | Banda | Módulo | Superfície | Conteúdo |
|---|---|---|---|---|
| 1 | preheader | | | |
| 2+3 | hero | hero dividido (variante do E04 em coluna) | `tex-topo-tapshoe` | NEW FOR 2026: (laranja) / **BUCK HOLLOW 2.0**, subtítulo, botão à esquerda; modelo da loja (jaqueta e calça Buck Hollow 2.0) à direita, rosto fora do quadro, cortado pelo rasgo |
| — | rasgo | E18 | topo → papel claro | |
| 4 | estrutura | E25 + sistema com 4 círculos (módulo novo, ver "Módulos para o kit") + E28 | papel claro, depois Patriot | QUIET ENOUGH TO / **SIT ALL DAY**, subtítulo, copy; jaqueta vestida sobre a calça, 4 círculos de detalhe com rótulo; tabuleiro: packshot em Aluminum / Dusk + caixa E27 (título, linha do cliente, preço, botão pequeno) |
| 7 | rodapé | E18 + E13 + E14 | | |

**Rótulos dos círculos** = frases exatas do copy do cliente em maiúsculas: FLEECE HAND-WARMER POCKETS e HARNESS PASS-THRU (copy do bloco 2), KNEE ARTICULATION (copy do bloco 2, "Knee articulation"), BOTTOM LEG ZIPPERS (linha da calça). São os mesmos 4 detalhes da referência do cliente. Imagens dos círculos: recortes das imagens Realtree APX da loja (jaqueta 02 frente, jaqueta 05 costas, calça 08 frente), no ponto que as imagens de callout da loja indicam (jaqueta 04 e 06, calça 03). Em camo, o detalhe lê como textura de tecido: com as fotos de detalhe originais do cliente, os círculos ficam mais claros (pedido abaixo).

| Produto | Variante | Preço | Painel |
|---|---|---|---|
| Men's Buck Hollow 2.0 Jacket | Realtree APX / M | $74.99 USD | Aluminum |
| Men's Buck Hollow 2.0 Pant | Realtree APX / M | $79.99 USD | Dusk |

## E-mail 04 · sex 27/11 · Heavyweight Flannel

- **ICP:** *Weekend Outdoor Adventurer* · medo: camisa que não aguenta o dia inteiro dentro e fora · precisa: conforto e versatilidade. **Mensagem-chave:** "hunters but not only" + "products work hard". **Mensagem única:** a flanela pesada que vai a qualquer lugar.
- **Assunto:** The Flannel You'll Live In 🔥 (28) · **Preheader:** Heavyweight comfort for inside and out
- **Botão:** hero SHOP FLANNEL → `{{FLANNEL_URL}}` · SHOP NOW → URL do copy (variante Rifle Green).

| # | Banda | Módulo | Superfície | Conteúdo |
|---|---|---|---|---|
| 1 | preheader | | | |
| 2+3 | hero | E01 (logo escuro sobre papel claro) + foto emoldurada reta | `tex-paper-camo` | **FLANNEL** / THAT GOES EVERYWHERE, foto do homem de flanela verde na porta do celeiro, subtítulo, botão |
| — | rasgo | E18 | papel camo → retícula Major Brown | |
| 4 | estrutura | E25 + mosaico (E22 reto) + par de cores + E27 | `tex-halftone-brown` | **WARM** / WITHOUT GETTING IN THE WAY, subtítulo (do cliente, ver ponto 4), copy; mosaico: foto no estábulo + pala/prega das costas + bolso de peito (os detalhes que o copy cita); as duas cores lado a lado no mesmo chão; "Available in…"; caixa E27 com nome e preço; botão |
| 7 | rodapé | E18 + E13 + E14 | | |

| Produto | Variante | Preço |
|---|---|---|
| Men's Heavyweight Soft Flannel (nome do "Product to Feature") | Basecamp Plaid Rifle Green / M (link do copy) · Major Brown só na imagem | $34.99 USD |

A caixa E27 mostra nome e preço (padrão do kit para produto) e nenhuma outra linha, porque o bloco 2 do cliente não traz linha de produto.

## E-mail 05 · seg 30/11 · Gift Guide #2, por preço (copy "Needs Edit")

- **ICP:** quem compra presente dentro de um orçamento · medo: gastar demais ou errar · precisa: opções por faixa de preço. **Mensagem-chave:** "outstanding value" (sem número). **Mensagem única:** presente certo em três faixas de preço.
- **Assunto:** Gifts at Every Price Point 🎁 (28) · **Preheader:** Gifts under $30, $100, and $120
- **Botão:** hero SHOP FLANNEL (como o cliente escreveu, ver ponto 1) → `{{CTA_URL}}` · produtos com o CTA do cliente → URLs do copy · SHOP GIFT CARDS → URL do copy (sem variante).

| # | Banda | Módulo | Superfície | Conteúdo |
|---|---|---|---|---|
| 1 | preheader | | | |
| 2+3 | hero | E24B (texto embaixo da foto) | foto → papel Tap Shoe, rasgo assado para a retícula | foto dos dois homens no UTV (logo branco sobre o teto escuro), GIFTS BY / **BUDGET,** (laranja) / NO GUESSWORK, subtítulo, botão |
| 4 | estrutura (uma lista de produtos em 3 faixas) | E07 Product Rows | retícula Major Brown / papel Tap Shoe / Patriot, com rasgos | UNDER / **$30**, **$100**, **$120**; cada linha: packshot em painel chapado + título (nome do cliente), linha, preço, botão pequeno |
| — | rasgo | E18 | Patriot → papel camo | |
| 5 | mudança de ângulo | E25 | `tex-paper-camo` | cartão-presente reto e emoldurado, **STILL** / NOT SURE WHAT TO GET?, copy, botão |
| 7 | rodapé | E18 + E13 + E14 | | |

**Uma banda de estrutura:** as três faixas de preço são tratadas como uma única lista de produtos (rules §3), com superfície própria por faixa para a leitura. Se o responsável considerar três bandas de estrutura, é exceção que precisa de ok com data aqui.

| Faixa | Produto (nome do cliente) | Variante | Preço (loja 2026-10-07) |
|---|---|---|---|
| UNDER $30 | Men's Breaking Dawn Camp | Lagoon Leaves Blue / S | $29.99 USD |
| | Men's Siesta Cape Long Sleeve Performance Tee | Mossy Oak Bottomland / M | $29.99 USD |
| | Men's Outdoor Hybrid Hoodie | Goblin Blue Heather / M | **$49.99 USD** (ver ponto 2) |
| | All-Purpose Camo Leather Gloves | Green Camo / M | $19.99 USD |
| UNDER $100 | Men's 3 Season Bomber Jacket | Major Brown / M | $74.99 USD |
| | Men's Heavy Weight Full Zip Hoodie | Major Brown / M | $44.99 USD |
| | Men's Sherpa Lined Canvas Jacket | Major Brown / M | $89.99 USD |
| | Men's Angler's Bluff Rain Bib | Dark Gray Waves / L | $99.99 USD |
| UNDER $120 | Men's Shadow Series Angler's Bluff Rain Bib | Black / Asphalt / L | $119.99 USD |
| | Men's Shadow Series Angler's Bluff Rain Jacket | Black / Asphalt / M | $119.99 USD |
| | Men's Waterproof Insulated Bib | Mossy Oak Terra Coyote / M | **$111.98 USD** (promoção, compare-at $159.99; ver ponto 3) |

Imagem do Angler's Bluff Rain Bib: a imagem da variante na loja é num modelo com a cabeça no quadro; foi usada a imagem 01 da mesma página (mesma estampa, Grey Waves, num manequim).

---

## Pontos para o cliente (não corrigidos, entram como vieram)

1. **05, hero:** o CTA "Shop Flannel" não tem relação com o gift guide (provável cópia do 04). Está no e-mail como SHOP FLANNEL, com destino `{{CTA_URL}}` a definir.
2. **05, UNDER $30:** o Men's Outdoor Hybrid Hoodie custa **$49.99** na loja (2026-10-07). Está na faixa "under $30" com o preço real da loja.
3. **05, UNDER $120:** o Men's Waterproof Insulated Bib está **em promoção** na loja: $111.98 (de $159.99). O e-mail mostra $111.98 USD, sem preço riscado. Se a promoção acabar antes de 30/11, o preço cheio ($159.99) sai da faixa "under $120". Na loja o nome é "Men's Shadow Series Waterproof Insulated Bib" (o copy diz "Men's Waterproof Insulated Bib"; usamos o do copy).
4. **04, subheadline do bloco 2:** "Rain-Factor tech meets soft tricot" é idêntica à do Buck Hollow (03) e não descreve uma flanela de algodão. Está no e-mail como veio.
5. **02, bloco 3:** "delivered straight to their inbox.." termina com ponto duplo. Está como veio.
6. **02, descrição:** o PDF fala em "top 5 apparel", a lista tem 6 produtos (mais o cartão-presente). Os 6 estão no e-mail.
7. **02, Summit Park:** o título veio com "— $39.99" no nome. O preço da loja bate ($39.99); no e-mail o nome fica na linha de título e o preço na linha de preço, sem o travessão.
8. **02 e 05 estão "Needs Edit"** no PDF: o cliente ainda pode mudar a copy desses dois.
9. **05, Men's Breaking Dawn Camp:** o nome do copy é curto (na loja: "Men's Breaking Dawn Camp Short Sleeve Fishing Shirt") e a linha fala em "camp layer for cool mornings and fire-lit nights" para uma camisa de pesca de manga curta. Está como veio.
10. **Nomes do copy diferentes da loja** (usamos os do copy): "Women's Cedar Branch Insulated **Waterproof Bibs**" (loja: "Insulated Bib"); "Angler's Bluff" com apóstrofo (loja: "Anglers Bluff" nos dois Shadow Series).
11. **Tecnologias sem ®:** o copy escreve Rain-Factor e Scent-Factor sem ®; o guia da marca (p.21) e o kit pedem o nome com ®. Não acrescentamos.
12. **04, "[Available in Basecamp Plaid Rifle Green and Basecamp Plaid Major Brown]":** entrou como frase no e-mail, sem os colchetes. Se era só instrução de layout (mostrar as duas cores), a frase sai e as duas cores continuam na imagem.
13. **04, um link só:** o copy dá o link da variante Rifle Green; as duas cores aparecem e as duas levam a esse link. A variante Major Brown existe (`variant=52630375989530`, em `products.json`) se o cliente quiser um link por cor.
14. **Assuntos com emoji** (🦌 🎁 🔥): as regras da operação não usam emoji decorativo; os assuntos vieram aprovados pelo cliente e estão como vieram.
15. **CTAs sem URL no copy:** Shop Women's e Shop Women's Collection (01), Shop Gift Guide (02), Shop Buck Hollow 2.0 (03), Shop Flannel (hero do 04 e do 05). Estão com placeholder nomeado `{{...}}` até o cliente mandar o destino.
16. **01 x 03, grafia:** "harness pass-through" (01, Early Dawn) e "harness pass-thru" (03). Cada um como veio.
17. **Cartão-presente:** o link do 02 tem variante (`?variant=16072202977331`, $50), o do 05 não tem. Cada um como veio.

## Dados a confirmar antes do envio ([[CONFIRMAR]])

- URLs dos CTAs da lista 15 (com UTM), `{{HOME_URL}}`, menu do rodapé, `{{INSTAGRAM_URL}}`.
- Preços e variantes reconfirmados na data de cada envio (5, 10, 19, 27 e 30/11), principalmente o $111.98 do ponto 3.
- Fotos de uso: os recortes `crop-sent-*` (celeiro, estábulo, UTV, caixa de iscas, blind, truta) são provisórios, tirados de e-mails enviados (`photos/lifestyle/INDEX.md`); `orig-twofisted-utv-two-men.jpg` (hero do 05) é original da Habit, ainda sem confirmação de liberação para e-mail.
- Rodapé do Omnisend com endereço físico e descadastro (CAN-SPAM), conferido num envio de teste.
- Salvar o PDF do cliente em `00-inbox/2026-11-broadcast-copy.pdf` (pendência do `copy-source.md`).

## Módulos para o kit (o kit precisa aprovar antes do envio)

Pela regra "só módulos do kit", o que abaixo não existe igual no kit v0.5 foi construído como variante e precisa entrar no kit (etapa 1, só estes módulos) quando o responsável aprovar:

- **Grupo de produtos no hero (01):** variante do E19 com a regra de outubro do responsável (produtos alinhados, num chão só, sombra comum, sem rotação), no lugar do leque.
- **Colagem como hero (02):** o E22 usado na abertura, rasgando direto na banda seguinte.
- **Hero dividido com modelo recortado (03):** coluna de texto à esquerda, modelo da loja à direita, cortado pelo rasgo (parecido com o hero do 04 de outubro, mas com recorte em vez de foto).
- **Sistema com círculos de detalhe (03):** **módulo novo** (pedido explícito do cliente: "full system shot with feature callouts"). Desktop em 3 colunas (2 círculos | sistema | 2 círculos), celular com o sistema e os círculos em 2x2. Rótulos só com frases do copy.
- **Mosaico reto de detalhes (04):** variante do E22 sem rotação (uma foto grande e dois quadrados).
- **Card emoldurado vertical 2-up (02):** moldura do E17/E29 com painel chapado em cima e texto E27 embaixo.

## Pesos (2026-10-07)

| E-mail | HTML | Imagens no modo claro | Total referenciado (com os gêmeos do dark mode) |
|---|---|---|---|
| 01 | 39,4 KB | cerca de 796 KB | 1.000 KB |
| 02 | 46,8 KB | cerca de 596 KB | 783 KB |
| 03 | 38,6 KB | cerca de 738 KB | 928 KB |
| 04 | 28,2 KB | cerca de 544 KB | 727 KB |
| 05 | 67,2 KB | cerca de 777 KB | 964 KB |

Todo HTML abaixo de 90 KB (Gmail corta em 102 KB). Nenhuma imagem acima de 150 KB. Os gêmeos `-dm` (texturas de papel trocadas por CSS e rasgos escondidos) contam no total porque parte dos clientes baixa imagem escondida; no modo claro do Apple Mail só a coluna do meio vale. 01 e 05 estão no teto de cerca de 800 KB do kit (4 texturas cada).

## Perguntas para o responsável

1. **Violet Dusk no 01:** o guia reserva o Violet Dusk `#C9B4CF` para a linha Women's, mas ele não está no kit. Usei o Ivy Green do kit (`color.line_womens`). Entra no kit como superfície ou painel do Women's?
2. **05:** ok para tratar as três faixas de preço como uma banda de estrutura só?
3. **03:** o cliente tem as fotos de detalhe originais (bolso, passa-cinto, joelho, zíper)? Em camo, o recorte da imagem de catálogo lê como tecido; foto de detalhe deixaria os círculos mais claros.
4. **Módulos novos/variantes** da lista acima: aprovar para o kit (principalmente o sistema com círculos do 03).
5. **Fotos provisórias** (`crop-sent-*`) e `orig-twofisted`: há originais e liberação?

---

## Rodada 2 (QA r1, 2026-10-07)

Email Designer, a partir de `qa-r1.md`. Regra mantida: **nenhum conteúdo do cliente mudou** (headline, copy, nome, linha, preço, CTA, ordem). Tudo foi feito nos scripts (`compose_assets.py`, `build_emails.py`); o HTML continua gerado. `lint_layout.py` limpo nos 5 (600 e 375); renders novos em `renders/` (680, 375, claro e escuro), conferidos seção a seção.

### Bloqueios

| # | Bloqueio | O que mudou |
|---|---|---|
| 1 | 03 hero (recorte com faixa fantasma, PNG em paleta, manga cortada) | Recorte refeito: só o maior componente do PNG da loja (sem o texto de ficha), cortado abaixo do queixo, ombros escurecidos para a cor da banda nas 130 primeiras linhas (sem transparência, logo sem faixa fantasma), **figura inteira dentro da coluna de 260px** (as duas mangas inteiras, 10px da borda), pernas cortadas pelo rasgo. Salvo como **JPG** assado sobre o papel Tap Shoe (sem posterização). A banda do hero passou de `tex-topo-tapshoe` para **`tex-paper-tapshoe`** (troca de superfície do kit): as linhas topográficas não fecham fase no celular, onde a textura escala e a imagem não; o grão do papel esconde a emenda. `n3-hero-model.jpg` 520x621, 70 KB |
| 2 | 03 círculos de detalhe (só textura de camo) | **Círculos retirados.** O sistema (jaqueta sobre calça, `n3-system.jpg` + gêmeo `-dm`, assado no papel claro) fica com os **4 rótulos em texto vivo** ao lado, cada um com um filete laranja de 30px apontando para a peça (frases exatas do copy: FLEECE HAND-WARMER POCKETS, HARNESS PASS-THRU, KNEE ARTICULATION, BOTTOM LEG ZIPPERS). Celular: sistema e rótulos em 2x2. Volta aos círculos só com as fotos de detalhe originais do cliente (pergunta 3) |
| 3 | 03 E28 (painéis em 258px, caixas encostadas) | Tabela do tabuleiro com `table-layout:fixed`; célula de texto com 252px de conteúdo + 24px de padding lateral = 300 (a largura 300 + padding dava 348 e alargava a coluna para 648), padding vertical 28/36px; caixa E27 de 250px. Painéis em 300x330 |
| 4 | 01 fechamento (3 molduras de tecido) | Molduras de tecido fora. A imagem passou a ser **as três peças do e-mail vistas de costas** (imagens "back on form" da loja, recortes transparentes, inteiras e reconhecíveis; a de costas da Sherpa Shell mostra o passa-cinto no contexto da peça), sobre o grão Ivy que abre a célula. `n1-closing-details.jpg` 520x660, 61 KB. Serifa "FULL" em branco (o kit só permite branco sobre Ivy) |
| 5 | 02 cards 2-up desalinhados | Título e linha em células de altura fixa (60px = 3 linhas de 20; 84px = 4 linhas de 21, o máximo da grade), preço + botão numa terceira célula `valign="bottom"`: nas 3 linhas o preço e o botão ficam na mesma altura nas duas colunas. No celular as alturas são liberadas (`.ct, .cd { height:auto }`) |
| 6 | 02 cartão-presente (vazio ao lado da imagem, 110px no celular) | Headline NOT SURE / WHAT TO GET THEM em **largura total** acima; abaixo, o cartão (268x180, assado no papel claro + gêmeo `-dm`, `img-light`/`img-dark`) ao lado de subtítulo, copy e botão. Celular: cartão centralizado, 32px até o texto |
| 7 | 02 colagem (mancha estourada, rasgo cortando 15px) | Colagem mais alta (600x440 css): a foto do blind recortada mais acima (o primeiro plano desfocado e claro ficou fora), as duas molduras de baixo terminam **30px+ acima da linha do rasgo**, inteiras |
| 8 | 05 hero (sem degradê, braços cortados, rosto cortado no celular) | Degradê refeito dentro da foto (linhas 470 a 790 de 1680; antes terminava fora da foto e deixava a linha reta). **Imagem própria para o celular** `n5-hero-m.jpg` (375x719 css, recorte mais fechado com os dois rostos inteiros, bonés longe do logo, degradê e rasgo assados), trocada pela regra `.hero5` da media query; espaçadores do celular ajustados para a banda fechar na altura da imagem (330 + 103px) |
| 9 | 04 mosaico (fragmentos brancos, cavalo cortado) | Recorte do estábulo 1:1 a partir de x 560, y 14 (`n4-m-stable.jpg` 640x600): só o homem, sem o cavalo e sem os restos do retoque no topo. Prega das costas: marca de callout da loja apagada e recorte centrado na pala e na prega |

### Avisos atendidos

- **Farelos do rasgo:** todos os `n*-edge-*.jpg` regerados com farelos de 0,6 a 1,3px em 2x (grão da rev-oct-03), em vez dos pontos de 3 a 5px; os rasgos assados (colagem do 02, hero do 05) seguem a mesma receita.
- **Viúvas nos títulos de produto:** `nb()` nas duas últimas palavras de todo título (card, caixa E27, linhas do 05, pilha do 01).
- **PNGs em paleta:** nenhum PNG sobrou em `assets/`. Produto sobre banda escura = JPG assado com as linhas da textura no ponto onde a imagem fica no desktop (grão esconde o deslocamento de fase no celular); produto sobre papel claro = JPG + gêmeo `-dm`; par de cores do 04 = JPG sobre painel Aluminum chapado.
- **01 com cara de catálogo:** a pilha saiu do papel claro para **Major Brown / papel Tap Shoe / Major Brown**, com título laranja (20px 800 = texto grande, 3,0:1 sobre brown como o kit permite) e fechamento sobre Ivy: 7 bandas escuras e claras alternadas, mais perto de outubro. O hero continua de estúdio (grupo de packshots): **não existe foto de uso da linha feminina** no banco nem nas imagens da loja (`all_images` conferidas: só "on form", callouts e tabela de medidas). Pergunta mantida para o responsável.
- **02 celular:** miniaturas em largura total do card (327px, arquivos a 2x de 330). Os 6 cards continuam em 1 coluna (2 colunas a 155px não cabem o título de 17px).
- **03 "DAY" sozinho:** serifa dividida em SIT / ALL DAY (mesmas palavras, mesma ordem).
- **04 celular:** quadrados do mosaico em 48,75% + 2,5% de margem = 8px, igual ao espaço vertical.
- **05:** cartão-presente do 02 não repetido: fechamento com foto rasgada E26 do original Habit `orig-hunt50-hunter-oaks-autumn.jpg` (caçador entre carvalhos) sobre o papel camo (+ gêmeo `-dm`), copy intacta. Linhas em **zigue-zague** dentro de cada faixa (imagem à esquerda, depois à direita, via `dir="rtl"` na tabela da linha, células de volta a `ltr`) para quebrar a monotonia das 11 linhas; miniaturas de 136px no celular (eram 120).
- **03 sistema + E28 na mesma banda:** continua como está; o bloco do sistema agora é foto com rótulos (não é segunda estrutura), mas a decisão fica com o responsável (pergunta 4 do QA).

### Não feito / fica aberto

- **Dark mode no app do Gmail** (texto escuro sobre papel claro e camo): só teste real, não dá para resolver por render.
- **05 acima do teto de ~800 KB do kit:** 11 produtos + 4 texturas (348 KB só nelas) + hero com duas versões. Desktop baixa cerca de 805 KB (sem o hero do celular, que só a media query carrega); celular cerca de 945 KB. Para baixar: tirar uma textura de faixa (a faixa UNDER $100 em Tap Shoe liso) ou o gêmeo `-dm` do fechamento. Decisão do responsável.
- A `orig-hunt50` (fechamento do 05) entra na mesma pendência de liberação das outras originais.

### Pesos (rodada 2)

| E-mail | HTML | Imagens no modo claro | Com os gêmeos do dark mode |
|---|---|---|---|
| 01 | 40,2 KB | cerca de 750 KB | cerca de 940 KB |
| 02 | 50,8 KB | cerca de 665 KB | cerca de 890 KB |
| 03 | 40,1 KB | cerca de 595 KB | cerca de 885 KB |
| 04 | 28,0 KB | cerca de 525 KB | cerca de 710 KB |
| 05 | 68,4 KB | cerca de 945 KB (805 KB no desktop, que não baixa `n5-hero-m.jpg`) | cerca de 1.245 KB |

Nenhuma imagem acima de 150 KB. Todo HTML abaixo de 90 KB.

---

## Rodada 3 (QA r2, 2026-10-07)

Email Designer, a partir de `qa-r2.md` (03 e 04 PASS; A, B, C abaixo). Sem mudança de conteúdo; tudo pelos scripts. `lint_layout.py` OK nos 5 (600 e 375); 20 renders refeitos em `renders/`.

| # | Bloqueio | O que mudou | Medido |
|---|---|---|---|
| A | 01 · emendas de `n1-hero-group.jpg` e `n1-closing-details.jpg` contra o grão Ivy | `compose_assets.py`: `border_window()` (1 no miolo, 0 nos últimos 40 px de cada borda) multiplica a poça de luz, o chão escurecido e a sombra de chão (`floor_shadow(win=)`) das duas composições, então as bordas são o tile intacto; o hero passou a sair das linhas certas do tile (y = 251 css medido no Chrome, não 235); `seam_check()` imprime o desvio contra o tile a cada geração | Arquivo contra tile: hero 0,4 / 0,6 / 0,3 / 1,2 (topo / base / esq. / dir.), fechamento 0,3 / 0,1 / 0,3 / 0,6. **No render 680** (tiras sem peça e sem texto): hero degrau máximo 0,7 no topo e 1,0 na base (era 21); fechamento 0,4 na borda direita e 1,5 na base (era 15); mesmo no escuro |
| B | 02 · linha 3 desalinhada 20px | `.ct` dos 6 cards com `height="80"` / `height:80px` (4 linhas de 20px; o título das botas ocupa 4). Celular continua `height:auto` | Render 680: preços em y 1811 / 2346 / 2880 nas duas colunas; botões em y 1851 / 2386 / 2920 nas duas colunas (as 3 linhas alinhadas) |
| C | 05 · título laranja a 17px sobre a retícula no celular | A célula de texto de cada linha leva a classe `t-{faixa}`; o override de 17px vale só para `.t-under100` e `.t-under120` (Tap Shoe, Patriot). A faixa UNDER $30 (retícula Major Brown) fica em 19px no celular | Chrome a 375px, `font-size` computado dos 11 títulos: UNDER $30 **19px** (4 linhas), UNDER $100 17px (4), UNDER $120 17px (3) |

**Peso do 05 (corte 1 do WARN):** `n5-hero-m.jpg` composto a 3,2x e gravado a **750x1438** (2x de 375x719; `scale=0.625` no `full_bleed_hero`): 86,6 KB (era 137,7). Celular ≈ **894 KB** no modo claro, desktop ≈ 807 KB (não baixa o hero do celular), ≈ 1.192 KB com os gêmeos `-dm`. O corte 2 (faixa UNDER $100 em Tap Shoe liso) **não foi aplicado**: decisão do responsável.

Não mexido nesta rodada, de propósito (WARN de baixa prioridade ou decisão do responsável): recorte do modelo alinhado à direita no celular do 03, tiles cinza do 04, regras de dark mode sem uso, laranja sobre Patriot com água (registro de exceção no kit), comentário do topo (sai na exportação).

---

## Rodada 4 (feedback do Lucas, 2026-10-07)

Email Designer, a partir da revisão do Lucas: "faltou mais imagens de seres humanos", seções "muito certinhas e comportadas", sombras erradas, packshots com fundo sujando a textura, produto pequeno e centralizado; referência: os e-mails de outubro no Deliverables Hub (Oct 6 bib grande + parka cortada pela borda, Oct 13 moletom saindo do painel, Oct 22 modelo sangrando pela borda e pelo topo, Oct 9 cards com produto grande, foto de gente em todo e-mail). **Nenhum conteúdo do cliente mudou** (diff de texto contra a rodada 3: idêntico nos 5; no 03 só saiu a cópia duplicada dos 4 rótulos que existia para o celular, agora um conjunto só serve as duas larguras). Tudo pelos scripts; HTML gerado.

### O que mudou no pipeline (vale para os 5)

- **Recorte limpo** (`compose_assets.py clean_cut`): todo packshot e foto de modelo da loja sai do PNG da loja com alfa a 50%, erodido 2 px e suavizado, e a cor da borda reestimada a partir do miolo da peça (push-pull). Sai o aro cinza do fundo de estúdio que sujava a textura (o defeito da Sherpa Shell que o Lucas apontou).
- **Uma luz para o lote** (de cima à esquerda): sombra projetada da própria silhueta, deslocada para baixo e à direita, suave e leve; sombra de contato justa sob cada barra ou perna (uma elipse por segmento, nunca mais larga que a barra); nenhuma sombra de chão para peça que sangra pela borda. Sem elipse cinza grande, sem sombra em caixa.
- **Job `bake`**: cada imagem com `data-bake` é medida no Chrome no layout de 600 px (posição dentro da célula da banda, altura da banda de cima) e montada exatamente com aquelas linhas e colunas do tile (R1). Seam medido arquivo x tile em todas as bordas que encostam na banda: **0,0 a 0,9 nível** (máx. 1,5 pela R1); as únicas leituras altas são bordas que coincidem com a borda do e-mail (sangria intencional, não emenda).
- **Produto atravessando o rasgo** (`frow(..., rise=True)`): a imagem abre a célula da banda e carrega, até a linha `hu`, a banda de cima na fase medida, o rasgo e os farelos finos (R6); a coluna de texto ao lado começa com a outra metade da mesma linha rasgada (peça `~t`, só desktop). No celular a imagem ocupa a largura toda e o rasgo continua de ponta a ponta.
- **Lint**: limpo nos 5 em 600 e 375, sem whitelist (as sobreposições são dentro da própria imagem, não imagem sobre texto). Correção no `lint_layout.py`: o Chrome headless desta máquina ignorava `--force-prefers-color-scheme=light` e media a imagem `img-dark` (fantasma); o probe agora fixa `data-theme="light"`.

### Por e-mail

| E-mail | O que mudou | Pessoas |
|---|---|---|
| 01 | Hero: sai o grupo de packshots de estúdio, entra a foto de uso da linha feminina derretendo no grão Ivy (fades terminam dentro da foto, R8). Pilha vira 3 linhas de destaque alternando lados: bib grande em pé à esquerda (um chão), parka atravessando o rasgo para a banda marrom e cortada pela borda direita do e-mail, Sherpa Shell atravessando o rasgo para a banda Tap Shoe; os rasgos entre as faixas de produto agora estão dentro das imagens (E18 separados saíram). Fechamento: a mulher na cadeira de camping sangrando pela borda esquerda, sob o rasgo marrom | `crop-sent-sep15-family-forest-walk` (hero: a mulher de Realtree com a família), `crop-sent-sep15-camp-chairs-family` (fechamento, recortada na mulher com a parka Women's) |
| 02 | Cards: fundo Patriot liso próprio do card, produto maior saindo do painel arredondado (Oct 13); o gorro aparece usado (foto de modelo da loja 02, recorte limpo). Mudança de ângulo: o cartão-presente sobre uma foto emoldurada de caçador, as duas inclinadas e sobrepostas, assadas no papel + gêmeo `-dm`. Colagem do hero igual (já tinha 3 fotos de gente) | colagem (UTV, pescador, blind, truta, como antes), `knit-camo-stocking-cap/02.png` (modelo da loja), `crop-sent-sep10-truck-hunter` (fechamento) |
| 03 | Hero na estrutura do Oct 22: logo e texto à esquerda, foto de uso à direita sangrando pelo topo e pela borda direita, derretendo no papel; no celular, recorte próprio paisagem embaixo do botão (`n3-hero-m.jpg`). Sistema solto e grande à esquerda, o capuz atravessando o rasgo para o hero; headline, subtítulo, copy e os 4 rótulos (com filete laranja) à direita. E28: a jaqueta agora vestida no modelo (foto da loja 07, recorte limpo, cortada pelo painel como moldura), calça maior | `orig-hunt40-hunter-forest-back` (hero, original Habit), `mens-buck-hollow-2-0-jacket/07.png` (modelo da loja, painel da jaqueta) |
| 04 | Tiles do mosaico só com tecido (sem o cinza de estúdio: o WARN do QA r2). O par de cores saiu do painel Aluminum e virou banda própria em papel Tap Shoe: as duas camisas grandes, sobrepostas num chão só, a gola verde atravessando o rasgo para a retícula; disponibilidade, caixa E27 e botão embaixo (5 bandas, sem exceção) | `crop-sent-sep24-barn-door-feed-bag` (hero) e `crop-sent-sep24-stable-horse` (mosaico), como antes |
| 05 | Linhas sem painel: cada produto é recorte limpo grande na superfície da faixa, alternando lados. As faixas UNDER $100 e UNDER $120 abrem com o produto-líder atravessando o rasgo para a faixa de cima, título da faixa ao lado. Superfícies: grão Major Brown (era a retícula), papel Tap Shoe, Patriot liso (era a água): grão e cor lisa não mostram a emenda no celular. Foto do fechamento recomprimida (corte 3 do QA r2) | `orig-twofisted-utv-two-men` (hero), `orig-hunt50-hunter-oaks-autumn` (fechamento), como antes |

Nenhuma foto repete entre os 5 (R10). Duas imagens fortes de gente por e-mail: 01 (2 fotos), 02 (colagem + cartão com caçador + gorro no modelo), 03 (hero + jaqueta no modelo), 04 (2 fotos), 05 (2 fotos).

### Pesos (rodada 4)

| E-mail | HTML | Imagens, modo claro | Só celular | Gêmeos `-dm` |
|---|---|---|---|---|
| 01 | 43,2 KB | 764 KB | | 191 KB |
| 02 | 52,0 KB | 727 KB | | 233 KB |
| 03 | 36,7 KB | 626 KB | +76 KB (`n3-hero-m`) | 297 KB |
| 04 | 30,0 KB | 640 KB | | 183 KB |
| 05 | 67,9 KB | 843 KB no desktop (celular ≈ 781 KB: troca o hero de 148 pelo de 86) | | 280 KB |

Nenhuma imagem acima de 150 KB; todo HTML abaixo de 90 KB. **05 no desktop fica ~40 KB acima dos ~800 KB** (11 produtos + hero de foto): o corte que sobra é a faixa UNDER $100 em Tap Shoe liso (menos ~87 KB), decisão do responsável como antes. Os totais `-dm` incluem a textura escura declarada no CSS, que nem todo cliente baixa.

### Aberto / para o responsável

- **Rasgo dentro da imagem no Outlook desktop**: a peça `~t` da coluna de texto é `img` normal; no Outlook o VML da banda pode deslocar 1 a 2 px a fase do tile. Só teste real confirma.
- **No celular** a parte de cima das imagens que atravessam o rasgo (01 parka/sherpa/fechamento, 03 sistema, 05 líderes) escala com a coluna; a banda de cima é grão ou cor lisa, a emenda não aparece nos renders a 375, mas a fase exata só bate a 600.
- **Fotos de modelo da loja** (gorro do 02, jaqueta do 03) e as `crop-sent-*` continuam na pendência de liberação; o gorro é a única imagem do lote com rosto de estúdio em close.
- Módulos novos desta rodada para o kit, se aprovados: linha de destaque com produto atravessando o rasgo (`frow rise`), card com produto saindo do painel sobre fundo liso, hero dividido com foto sangrando (Oct 22 em coluna).

---

## Rodada 5 (QA r4)

Email Designer, a partir de `qa-r4.md` (01 e 02 PASS; 03, 04, 05 BLOCK). Sem mudança de conteúdo; tudo pelos scripts. `lint_layout.py` OK nos 5 em 600 e 375; renders 680 / 375, claro e escuro, refeitos e conferidos nos pontos abaixo.

| # | Bloqueio | O que mudou | Medido |
|---|---|---|---|
| 1 | 04 · banda do par em Tap Shoe colada no rodapé Tap Shoe | Banda do par passou para **`tex-grain-patriot-water`** (caixa E27 laranja sobre Patriot = padrão do E28). Par regerado nas linhas do tile Patriot, rasgo retícula→Patriot dentro da imagem, E18 novo **Patriot→rodapé** (`n4-edge-patriot-footer.jpg`) | Render 680: banda do par RGB **36/45/76**, rodapé **42/43/45**; seam do par 0,2 |
| 2 | 04 · franja branca entre manga e corpo da camisa verde | `clean_cut` ganhou o passe de **fundo preso**: pixels opacos quase brancos e neutros (mín. ≥ 225, croma ≤ 14), finos (abaixo de 15 px de largura) e ligados ao fundo transparente são fundo de estúdio e saem do alfa (+2 px da borda). Rodado em **todos os 28 recortes do lote**, com o total impresso por recorte | Removidos: camisa verde 1.234 px, camisa marrom 1.424, bota 844, modelo Buck Hollow 133, hoodie Summit 78, Breaking Dawn 31, calça Buck Hollow 28, jaqueta Buck Hollow 20, Angler's Bluff bib 18, bomber Cedar Branch 13, Flushing Bay LS 2; os outros 17 com 0. O Angler's Bluff Rain Bib (estampa branca de ondas até a silhueta) fica fora do passe (`WHITE_PRINT`), conferido no zoom. Branco puro restante em `n4-pair.jpg`: 39 px (costuras e botões da xadrez, não franja); zoom 2x da área da QA limpo |
| 3 | 05 · manchas soltas sob o bomber (UNDER $100) | Peça-líder que sangra pela borda **não leva sombra de contato** (`put(..., ground=not bleed)`) | 36 linhas abaixo da barra: p1 35 / mediana 43, igual ao tile Tap Shoe (p1 36 / mediana 43); antes 21 a 26 |
| 4 | 03 · E28 de catálogo e uma só imagem forte de gente | E28 removido. A banda de produtos (Patriot água) abre com uma **faixa de foto em largura total** `orig-hunt22-three-hunters-field-sunrise` (três caçadores subindo o campo; não usada em nenhum outro e-mail de novembro), sob o papel claro rasgado no topo (gêmeo `-dm`) e derretendo no Patriot embaixo; depois **jaqueta** (recorte limpo, grande, manga cortada pela borda esquerda) e **calça** (grande, perna cortada pela borda direita) alternando lados com as caixas E27. Sistema com os 4 rótulos mantido. O E18 papel→Patriot saiu (o rasgo está na faixa de foto) | Seams: faixa 0,6, jaqueta 0,6 / 0,2 / 0,5, calça 0,0 / 0,1 / 0,0 |

**Também pedido:** 05 · rain bib (UNDER $100) e Waterproof Insulated Bib (UNDER $120) com imagem mais alta (230x340 em vez de 230x240) e luvas sem o fator 0,78: os três agora na escala dos vizinhos. 03 · celular: a faixa vazia sob a foto do hero fechou: `n3-hero-m.jpg` com a foto até a borda de baixo (fade de 36 px) e o rasgo do sistema baixou para 40 px css (`hu=40`), o capuz encosta na foto.

**Pessoas por e-mail:** 01: 2 (família na mata, mulher na cadeira) · 02: colagem com 3 fotos de gente + caçador no cartão-presente + gorro no modelo · 03: **2** (arqueiro no hero, três caçadores na faixa) · 04: 2 (celeiro, estábulo) · 05: 2 (UTV, caçador nos carvalhos). Nenhuma foto repete no lote (`orig-hunt22` foi o hero de 6/10, mês anterior).

### Pesos (rodada 5)

| E-mail | HTML | Imagens, modo claro | Só celular | Gêmeos `-dm` |
|---|---|---|---|---|
| 01 | 43,2 KB | 764 KB | | 191 KB |
| 02 | 52,0 KB | 727 KB | | 233 KB |
| 03 | 37,7 KB | 754 KB | +83 KB | 399 KB |
| 04 | 30,1 KB | 640 KB | | 183 KB |
| 05 | 67,9 KB | **871 KB** no desktop (celular ≈ 809 KB) | | 280 KB |

O 05 subiu 28 KB com os bibs e as luvas maiores e fica ~70 KB acima dos ~800 KB no desktop; o corte continua sendo a faixa UNDER $100 em Tap Shoe liso (menos ~87 KB), decisão do responsável. O 03 ganhou um composto pesado a mais (a faixa de foto, 108 KB): passa da regra "um composto acima de 100 KB além do hero" (sistema 108 + faixa 108), registro para o responsável.

---

## Rodada 6 (feedback do Lucas, 2026-10-08)

Email Designer, a partir da revisão do Lucas sobre a rodada 5 (cinco pontos, prints dele: colagem do 02, hero do 03, faixa e linha da jaqueta do 03, linha da calça do 03, e o 05 inteiro). **Nenhum conteúdo do cliente mudou:** a sequência de palavras visíveis dos 5 e-mails é idêntica à da rodada 5, palavra por palavra (180 / 276 / 137 / 102 / 319 palavras), ou seja, os mesmos 132/132 que o QA conferiu; só a divisão de linha da headline do 03 e o tratamento visual mudaram. Tudo pelos scripts (`compose_assets.py`, `build_emails.py`); HTML gerado. `lint_layout.py` OK nos 5 em 600 e 375. Os 20 renders refeitos (680 / 375, claro e `-dark`, altura total) e conferidos ponto a ponto, com recorte e zoom.

### O que mudou, por ponto

| # | Pedido | O que mudou | Onde ver (render 680, y aprox.) |
|---|---|---|---|
| 1 | 02 · buraco escuro no meio da colagem | Colagem refeita como **uma pilha só, sobreposta, como a ref2** (Fall '26): 5 fotos emolduradas em vez de 4, todas maiores e mais inclinadas (-3,2° a +4°), encostando e passando umas sobre as outras, a pilha saindo pelas duas bordas do e-mail. A 5ª foto, `crop-sent-sep22-wading-river` (pescador entrando no rio), ainda não usada em novembro, fecha o miolo. O papel rasga para a água Patriot **antes** das fotos serem coladas, e as três fotos de baixo ficam **por cima do rasgo**, atravessando 40 px css ou mais (R11): não sobra faixa morta entre a colagem e a banda seguinte. Imagem 600x500 (era 440); a fase do tile foi medida no Chrome (colagem começa a 471 css na célula, linha 942 do tile; antes estava em 1000: degrau no topo agora 0,4 nível) | `02-gift-guide-1-680.png` y 503 a 1003; `-375.png` y 452 a 765 |
| 2 | 03 · "2.0" sozinho e foto cortada/derretendo | **Hero de foto em tela cheia** (ref1 New Terrain Guard: título sobre a foto; ref6: hero de foto de uso): `orig-hunt40` (mantida, funciona cheia) cobre a banda de ponta a ponta, 600x820, até o rasgo para o papel claro do sistema, assado na base da imagem (gêmeo `-dm` para o papel escuro). Texto vivo no canto superior esquerdo: logo, **kicker NEW FOR 2026: numa etiqueta escura rasgada** (dispositivo E33 do kit, laranja sobre Tap Shoe, 4,8:1 independente das folhas), headline **BUCK / HOLLOW&nbsp;2.0** (Playfair 60/58, "HOLLOW 2.0" preso com `&nbsp;` e `nowrap`: o "2.0" nunca fica sozinho, desktop e celular), subtítulo numa linha, botão. **Escurecimento local dentro da foto** só no canto do texto (superelipse x 0 a 440, y 30 a 400 css, sumindo antes do arco e da cabeça do caçador a 470 css; a copa da direita e o caçador ficam como foram fotografados). Contraste medido no arquivo (pior caso, percentis 1/99): logo 7,5:1, headline 7,1:1, subtítulo 4,6:1. Imagem de fundo da célula + VML `v:fill frame` 600x820 + `bgcolor` #2A2B2D. **Celular:** recorte próprio `n3-hero-m.jpg` (375x750), mesmo princípio: texto à esquerda sobre o topo escurecido da foto, a cabeça do caçador logo abaixo do botão (385 css), rasgo para o papel; headline 50/50 com tracking 0,5 (HOLLOW 2.0 cabe em 327). Medido: logo 6,0:1, headline 5,8:1, subtítulo 5,4:1. Troca por media query (`.hero3`), e no escuro por regras `prefers-color-scheme` / `data-theme` / `[data-ogsb]` (desktop e celular) | `03-buck-hollow-2-680.png` y 32 a 852; `-375.png` y 32 a 782; escuros iguais com o papel escuro abaixo do rasgo |
| 3 | Lote · transições em degradê/blur | **Nenhuma transição de foto para banda é mais degradê ou derretido.** `melt()` e o `fade` do `full_bleed_hero` saíram do script. Novos: `torn_sheet` (a foto como cópia rasgada sobre a banda: linha rasgada irregular, miolo branco do papel ao longo do rasgo, sombra projetada da luz do lote), `paper_hero` (05) e `photo_hero` (03, foto cheia rasgando para a banda seguinte com `tear_into`). Aplicado em: **01 hero** (foto da família rasgada em cima e embaixo sobre o grão Ivy), **01 fechamento** (mulher na cadeira rasgada à direita e embaixo, continua sob a folha marrom rasgada em cima), **03 hero** desktop e `n3-hero-m` (foto cheia, rasga para o papel), **03 faixa dos três caçadores** (rasgada embaixo sobre o Patriot), **05 hero** desktop (foto rasgada embaixo sobre o papel Tap Shoe) e `n5-hero-m` (rasgada em cima e embaixo, logo no papel acima). O escurecimento dentro da foto do 03 é o único "escurecer" do lote e não é transição. **R8 do kit reescrita** (abaixo) | 01: y 270 a 600 e y 2734 a 3094 · 03: y 852 e y 1486 a 1786 · 05: y 32 a 432 |
| 4 | 03 · produtos colados na borda, buraco entre as linhas | Bloco refeito como **par em escada** (ref4 3L Rain Shell, mosaico escalonado; ref3, par de produtos): jaqueta em cima à esquerda com a caixa E27 dela ao lado, calça embaixo à direita com a caixa dela ao lado; as células de imagem ocupam duas linhas cada (`rowspan`), então a calça começa enquanto a jaqueta ainda está na tela (sobreposição de 75 css) e não sobra linha vazia. **Nenhum produto cortado pela borda:** jaqueta 280 css de largura com 22 css de margem, calça em pé centrada na coluna. Caixas E27 com o conteúdo exato (nome, linha, preço, botão). Celular: empilha na ordem do copy (jaqueta, caixa, calça, caixa). A banda passou de água Patriot para **Patriot liso** (`#202944`, cor do kit): textura reescala no celular e marcava um retângulo em volta de cada produto assado; liso não tem emenda em largura nenhuma (e tira 87 KB) | `03-buck-hollow-2-680.png` y 1786 a 2580; `-375.png` y 2276 a 3700 |
| 5 | 05 · repetitivo, produtos pequenos | Seção de ofertas redesenhada com **um layout por faixa** e um **cabeçalho de faixa novo**: etiqueta de papel claro rasgada (dispositivo E33 do kit: célula `#E2DDD9` + ponta rasgada em PNG-24 transparente), UNDER em Prompt 800 sobre o valor em Playfair 96 (68 no celular), Tap Shoe 10,5:1. Produtos bem maiores (antes 230x240 com o produto em cerca de 200 px de altura; agora 235 a 435 px de altura no desktop, 300 a 375 de largura no celular). Ver a lista abaixo. Preço do Insulated Bib continua `$111.98 USD`, sem riscado nem selo | `05-gift-guide-2-680.png` y 872 a 4930 |

**As três faixas do 05 (uma linha cada):**
- **UNDER $30** (grão Major Brown): etiqueta centralizada rasgada dos dois lados + **grade aberta 2x2** dos quatro "stocking stuffers", recorte grande direto no grão (sem moldura nem painel, diferente dos cards do 02), título, linha, preço e botão centralizados embaixo, células de altura fixa (R3) · ref5 (produtos agrupados).
- **UNDER $100** (Tap Shoe liso): **um produto-líder grande** (o bomber, atravessando o rasgo para a faixa de $30, ref1) com a etiqueta encostada na borda direita ao lado; depois os outros três **agrupados numa foto só** (hoodie, jaqueta sherpa e rain bib num chão, da esquerda para a direita na ordem da lista, ref5) sobre uma **lista de preços com filetes** (título + linha | preço + botão, ref6).
- **UNDER $120** (Patriot liso): etiqueta centralizada; o Shadow Series Rain Bib e a Rain Jacket **juntos como conjunto** ("The matching top half", ref3 par de produtos) com as duas caixas lado a lado (contorno E27 na célula, mesma altura); depois o Waterproof Insulated Bib ("The top-shelf gift") **como destaque próprio**: texto à esquerda, bib alto à direita.

Uma banda de estrutura só (as três faixas), 5 bandas no total, como antes. Superfícies: grão Major Brown / Tap Shoe liso / Patriot liso (a faixa de $100 lisa era o corte de peso que o QA vinha sugerindo; com layouts diferentes, a cor deixou de ser a única diferença).

### Sombras e recortes (lições das rodadas 4 e 5)

Roupa de cima (camisas, jaquetas, moletons, luvas) não leva sombra de contato: só a sombra projetada da própria silhueta. O bomber do 05 tinha voltado a ter os riscos soltos sob a barra no primeiro render desta rodada; corrigido (`ground=False` para toda peça de cima no 03 e no 05). Bibs e calças em pé mantêm a sombra de contato justa. Recortes pelo `clean_cut` de sempre.

### Fotos por e-mail (rodada 6)

| E-mail | Fotos de uso | Mudou? |
|---|---|---|
| 01 | `crop-sent-sep15-family-forest-walk` (hero), `crop-sent-sep15-camp-chairs-family` (fechamento) | mesmas fotos, só as bordas viraram rasgo |
| 02 | colagem: `crop-sent-sep10-utv-hunters`, `crop-sent-sep22-angler-tackle-box`, **`crop-sent-sep22-wading-river` (nova)**, `crop-sent-sep2-hunter-blind`, `crop-sent-sep22-trout-in-hand`; fechamento: `crop-sent-sep10-truck-hunter` + cartão-presente da loja; gorro no modelo da loja | +1 foto na colagem |
| 03 | `orig-hunt40-hunter-forest-back` (hero, recorte desktop e celular), `orig-hunt22-three-hunters-field-sunrise` (faixa) | mesmas, hero agora cheio |
| 04 | `crop-sent-sep24-barn-door-feed-bag`, `crop-sent-sep24-stable-horse` | não mexido |
| 05 | `orig-twofisted-utv-two-men` (hero), `orig-hunt50-hunter-oaks-autumn` (fechamento) | mesmas |

Nenhuma foto repete em novembro (R10). A `wading-river` não aparece em outubro; só tinha sido usada num rascunho de setembro (`2026-broadcasts`, 04 Shoreline). É recorte de 304 px de largura: na colagem fica a cerca de 180 css (quase 1:1 no 2x), lê bem; entra na mesma pendência de liberação dos `crop-sent-*`.

### Pesos (rodada 6)

| E-mail | HTML | Imagens, modo claro (desktop) | Só celular | Gêmeos `-dm` e texturas do CSS escuro |
|---|---|---|---|---|
| 01 | 43,4 KB | 775 KB | | 191 KB |
| 02 | 52,2 KB | 733 KB | | 233 KB |
| 03 | 37,2 KB | **592 KB** (era 754) | +103 KB (`n3-hero-m`, troca o hero de 138) | 609 KB (inclui os dois heroes `-dm`) |
| 04 | 30,1 KB | 640 KB | | 183 KB |
| 05 | 70,7 KB | **787 KB** (era 871) | +90 KB (`n5-hero-m`, troca o hero de 139) | 262 KB |

Nenhuma imagem acima de 150 KB; todo HTML abaixo de 90 KB. **05 abaixo dos ~800 KB** pela primeira vez (Tap Shoe liso na faixa de $100, produtos em fundo liso, fechamento recomprimido de 95 para 75 KB). **03**: sem textura Tap Shoe nem água (hero é foto de fundo, banda de produtos lisa); nenhum composto acima de 100 KB além do hero (sistema 97, faixa 96: o R14 que o QA registrou na rodada 5 fica resolvido).

### Conferências

- `lint_layout.py`: OK nos 5, 600 e 375.
- Copy: sequência de palavras visíveis idêntica à rodada 5 nos 5 e-mails (= 132/132 do QA). Conferência própria contra `copy-source.md` com outro critério (assunto, preheader, toda headline, subheadline, copy, CTA, nome, linha, título de faixa, linha de disponibilidade e **cada URL**): 143/143.
- Preços: os 23 preços exibidos (`$xx.xx USD`, cada um no link do seu produto) iguais a `products.json` e iguais aos da rodada 5 (o QA contou 26/26 com outro critério; nenhum preço mudou). `$111.98 USD` sem riscado, sem "was", sem selo.
- Zero travessão e meia-risca (texto e alt). Hex novo só `#FEF4C6` no 05 (contorno de card do kit, agora nas caixas do conjunto e nos filetes da lista).
- Emendas (R1): todos os assados novos 0,0 a 0,7 nível contra o tile; no render, degrau de 0,4 no topo da colagem do 02 e abaixo de 1 nível na emenda hero→papel do 03 (claro e escuro, 680 e 375) e hero→grão do 05.

### Kit: R8 reescrita

`email-kit/README.md`, "Hero de foto e transições de foto (R8)", **decisão do responsável de 2026-10-08**: nenhuma transição de foto para banda em degradê de alfa ou derretido; toda borda de foto que encontra banda é rasgo ou textura orgânica (cópia rasgada com miolo branco e sombra, ou a folha da banda seguinte rasgada por cima); escurecer de leve dentro da foto sob o texto é permitido, só o necessário para o AA; hero de foto cheio de ponta a ponta até o rasgo; recorte próprio de celular mantido, com a mesma regra. Espelhada no rótulo R8 do `components.html` (só o texto) e registrada no changelog. Os módulos E24, E24B e E30 do kit ainda assam derretido: ficam em "Em aberto" do kit para a próxima revisão (esta rodada não mexe em módulo do kit).

### Para o responsável

1. **03, escurecimento:** no canto do texto ele é mais que "leve" nos buracos de céu mais claros da copa (o subtítulo de 15 px precisa de 4,5:1); fora do canto a foto está como foi fotografada. Se quiser mais leve, o caminho é subtítulo maior ou numa etiqueta como o kicker.
2. **03, kicker em etiqueta escura rasgada** (o laranja direto sobre as folhas não passa de 3:1 sem escurecer muito mais a foto). Ok?
3. **03, banda dos produtos em Patriot liso** (era a água): sem emenda no celular e 87 KB a menos. Ok?
4. **05, etiquetas de faixa claras também no modo escuro** (de propósito, como um adesivo; só o papel das bandas claras troca no escuro). E a foto agrupada da faixa de $100 não tem link próprio: os três produtos levam ao link pela lista logo abaixo dela.
5. **Módulos para o kit, se aprovados:** colagem-pilha (E36 revisto: 5 fotos, as de baixo sobre o rasgo), hero de foto cheia com canto escurecido e kicker em etiqueta (E24 novo, substitui o hero dividido E37 no lote), par em escada com `rowspan`, etiqueta de faixa rasgada (E33 como etiqueta de preço), grade aberta 2x2, líder + grupo + lista de preços, conjunto + destaque.
6. **Outlook desktop (teste real):** `rowspan` do par em escada do 03, pontas PNG das etiquetas (alpha) e o hero do 03 em VML com texto por cima; Gmail app escuro sobre o papel claro, como antes.
7. Continuam valendo as pendências anteriores: liberação das fotos (`crop-sent-*`, inclusive a `wading-river` nova, `orig-*`, modelo da loja), placeholders de URL, preços reconfirmados na data (sobretudo o $111.98 promocional), pontos do cliente.

---

## Rodada 6 (02 cards)

Email Designer, pedido do coordenador (2026-10-08): o 02 era o que menos tinha mudado (grade 2-up de cards com produto em painel cinza, gorro em close de estúdio). Só o 02 foi mexido; conteúdo literal, mesma ordem (diff de texto contra a rodada 3: idêntico). Regras do kit vigentes respeitadas, inclusive a R8 reescrita hoje (nenhuma transição em degradê: a foto nova é cópia rasgada).

| Antes | Agora |
|---|---|
| 3 linhas de cards 2-up com contorno, packshot saindo de painel cinza/colorido | **6 linhas no padrão do 05**, sem card e sem painel: recorte limpo grande direto na banda, alternando lados, texto (título, linha, preço, botão) ao lado. Escala variada: camisas 260x280 e 260x300, **bomber 300x360 cortado pela borda esquerda**, moletom 260x300, **botas 300x320 grandes**, gorro menor **agrupado com uma foto de gente** |
| Gorro em close de estúdio no rosto de um modelo | Gorro como recorte limpo, no chão, na frente de uma **cópia rasgada de `crop-sent-sep10-utv-hunter-standing`** (caçador em Realtree ao lado do UTV; não usada em nenhum outro e-mail de novembro), rasgada à esquerda, em cima e embaixo, saindo pela borda direita do e-mail |
| Banda em água Patriot | **Patriot liso** `#202944` (kit): a textura de água reescala no celular e marcava um retângulo em volta de cada produto assado (visto no render 375 do primeiro passe); liso não tem emenda em largura nenhuma. A colagem do hero agora rasga direto para o Patriot liso; E18 novo Patriot liso→papel |

**Sombras:** uma luz (de cima à esquerda). Camisas, bomber e moletom só com a sombra projetada da silhueta, sem sombra de contato; botas e gorro (no chão) com sombra de contato justa. Recortes pelo `clean_cut` da rodada 5 (fundo preso incluído; bota com 844 px removidos).

**Celular:** cada linha empilha (imagem centralizada na largura do desktop, depois texto centralizado), em vez de miniatura de 150 px ao lado do texto: no primeiro passe o título do bomber estourava a coluna e o do moletom encostava na imagem.

**Pessoas no 02:** colagem do hero (5 fotos, 4 com gente), caçador ao lado do UTV (linha do gorro), caçador da caminhonete (cartão-presente). Nenhuma repete no lote. O close de estúdio saiu.

**Medidas:** seams dos 6 assados 0,3 a 0,7 nível contra o Patriot liso; `lint_layout.py` OK em 600 e 375; renders 680/375, claro e escuro, refeitos. Peso do 02: HTML 48,4 KB, imagens no modo claro **643 KB** (era 733; sem a textura de água), gêmeos `-dm` 231 KB. Nenhuma imagem acima de 150 KB.

**Nota (QA r6, 02):** (1) a foto da linha do gorro trocou de `crop-sent-sep10-utv-hunter-standing` (mesma cena de UTV e caçador de boné laranja da colagem, uma tela acima) para **`crop-sent-sep22-boat-anglers`** (três pescadores no barco, pesca de mosca; não usada em nenhum outro e-mail de novembro, cena diferente de toda foto da colagem): cópia rasgada horizontal no canto de cima à direita, saindo pela borda direita, sem degradê (R8); o gorro fica na frente do canto de baixo à esquerda dela (sobreposição de cerca de 65 css). (2) Foto do blind recortada acima do primeiro plano claro desfocado de novo (recorte x 200-1081, y 0-880 da fonte, como na rodada 2) e a luz do dia na abertura do blind comprimida acima de 190 (só dentro da foto): branco puro (≥ 244) na foto do blind caiu para 159 px na metade de baixo e 211 na de cima (a QA mediu cerca de 3.900 perto de branco). (3) O rasgo da colagem para o Patriot ganhou perfil irregular (`tear_into(..., amp=12, rough=9)`, com mordidas próprias nos trechos de cerca de 40 px que aparecem nas bordas do e-mail). Lint OK em 600 e 375; renders 680/375 claro e escuro refeitos; imagens do 02 no modo claro **626 KB**, HTML 48,5 KB.
