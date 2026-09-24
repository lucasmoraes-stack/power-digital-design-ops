# 2026 Broadcasts · brief

> Brief do lote (playbook, etapa 3), montado em 2026-09-24 pelo Email Designer. Lote de broadcasts avulsos: sem gatilho nem cadência. Dois designers constroem em paralelo (Designer A: e-mails 01 e 02 · Designer B: e-mails 03 e 04) **só a partir deste arquivo**. Tudo que for decidido depois volta pra cá, com data.

Copy-fonte: `copy-source.md` (PDF do cliente, literal) · Assunto/preheader e checagem de claims: `subject-lines.md` (Copywriter) · Produtos: `products.json` (variante exata, preço de 2026-09-24, packshot) · Kit: `clients/habit-outdoors/01-brand/email-kit/` **v0.2 aprovado** (E01 a E18) + **v0.3 rascunho** (E19 a E23, pendente de aprovação) · Referências: e-mails enviados da Habit (fonte da verdade) + Duck Camp (estrutura rústica), ver `email-kit/references/README.md`.

## Como ler este brief (para os dois designers)

1. Ler antes: `email-ops/rules.md`, `email-kit/README.md` (tokens, regra de caixa, contraste do laranja), os módulos no `components.html` (copiar **verbatim** entre `<!-- MODULE:Exx -->` e `<!-- /MODULE:Exx -->`, sem as linhas `kit-label`).
2. Partir do `<head>` do `components.html` (tokens, fontes, dark mode, media queries). Caminho das imagens: relativo ao e-mail, `../../../01-brand/email-kit/assets/{arquivo}`.
3. Módulo marcado **(v0.3, pendente de aprovação)**: construir com ele (é o plano), mas cada uso tem um **fallback aprovado** escrito ao lado. Se o responsável não aprovar a v0.3 antes da revisão, trocar pelo fallback: a sequência de cores do fallback também está escrita e já foi conferida.
4. Texto: usar o texto da coluna "Conteúdo" **exatamente** como está aqui (já com os desvios obrigatórios aplicados). Não reescrever nada. `[[CONFIRMAR]]` fica visível.
5. Cada designer só cria os assets da sua metade, num script próprio (seção "Jobs de composição"), pra ninguém editar o mesmo arquivo ao mesmo tempo.
6. Render check (680, 375, `--dark`) antes de devolver; relatório no formato do agente.

## Triagem (rules §1)

| | |
|---|---|
| Tipo | Broadcast sazonal / educativo de produto, **4 e-mails** (o responsável falou em 5: [[CONFIRMAR: existe um quinto e-mail?]]) |
| Público / gatilho | Lista inteira, envio manual por e-mail [[CONFIRMAR: segmento]] · sem gatilho, sem cadência · datas de envio [[CONFIRMAR]] (ver "Em aberto") |
| Oferta | Nenhuma. O copy não traz desconto, código nem prazo. Sem urgência |
| CTA | Um por bloco, texto do cliente, em caixa-alta no botão. Destinos: placeholders nomeados por e-mail (abaixo) + URL real da variante nos cards de produto |
| ESP / merge | Omnisend (não necessário nesta etapa) · **sem merge field** (decisão do responsável: os e-mails enviados não têm) |
| Destino | HTML do kit → cópia editável no Figma (playbook etapa 7, `generate_figma_design`); o responsável finaliza a tipografia e exporta de lá |
| Rodapé | E13 + E14 exatamente como no kit: logo empilhado, MEN'S \| WOMEN'S \| YOUTH \| SALE, Instagram @HABITOUTDOORS, "© 2026, Habit Outdoors. Built By Wilde Creative." **Sem endereço e sem linha de motivo** (decisão do responsável 2026-09-24); endereço e descadastro vêm do rodapé do Omnisend [[CONFIRMAR: Omnisend acrescenta, CAN-SPAM]] |
| Atendimento | Nenhum canal no rodapé (padrão dos e-mails enviados) |
| Dados de operação | Preços de `products.json` (loja, 2026-09-24), em USD, formato do kit `$29.99 USD` sublinhado. **Reconfirmar no dia do envio.** Frete grátis acima de $100 existe no site, mas o copy não cita: não entra |

## Sistema do lote

### Regras que valem para os 4

- **Botão:** um estilo só, o do kit: `#FF6400` com texto `#2A2B2D`, caixa-alta, tracking 2px, raio 6px, 52px de altura (hero 16px 64px de padding, demais 16px 36px). Nenhuma variante.
- **Caixa:** headline, subtítulo, botão e linha 1 do card de produto em **maiúsculas reais no HTML**. Corpo, linha 2 do card e link em texto, como o cliente escreveu.
- **Subtítulo do cliente (subheadline)** = papel "Subtítulo espaçado" do kit (Prompt 500, 14/22, tracking 2px, caixa-alta), logo abaixo da headline. E16 e E17 já têm essa linha: usar a do módulo. Nos módulos que não têm (E02, E05, E15, E19), a linha entra com o estilo copiado do `<p>` de subtítulo do E16 (cor do texto conforme o fundo: `#2A2B2D` com classe `dm-h` em fundo claro, `#FFFFFF` em fundo escuro). Ver decisão D1.
- **Palavra de destaque:** uma por headline, Playfair Display 900 caixa-alta (span do próprio módulo). Laranja só em Tap Shoe / Patriot Blue (e grande em Major Brown); em fundo claro fica `#2A2B2D` (classe `dm-accent`). A palavra está indicada em cada tabela.
- **Viúva:** `&nbsp;` entre as duas últimas palavras de toda headline e subtítulo.
- **Linha de pesca desenhada:** **nenhum** e-mail do lote usa. O único asset com a linha é `hero-fishing.jpg` (E02) e ele não entra no lote; o E4 usa a versão sem linha (`card-fishing.jpg`).
- **E18 Torn Edge:** linha com `td bgcolor` = cor da banda de CIMA (com a classe `dm-surface`/`dm-band` se ela for clara) e `img` = borda na cor da banda de BAIXO. Não conta como banda. Não existe borda em Patriot Blue no kit: a fronteira para Patriot Blue é reta.
- **E17 Product Cards com 3 produtos:** linha 1 do grid com 2 cards (como no kit); linha 2 com **1 card**, a mesma célula `card-cell` com `width:50%`, centralizada (`<td colspan="2" align="center">` com a célula dentro). No mobile os 3 empilham. Um botão só, embaixo do grid. Ver decisão D2.
- **Card de produto:** linha 1 (Prompt 800 20/24 caixa-alta) + linha 2 (16/22) + preço como link sublinhado + packshot 200x200 (arquivo 400x400), tudo linkado na URL real da variante. Sem preço riscado (C7).
- **Topo do HTML:** comentário com `Subject:`, `Preheader:`, `Modules:`, `Button: #FF6400 / #2A2B2D`.
- **Peso:** HTML < 90KB, imagens ~800KB no máximo por e-mail; cada composição < 150KB (o script checa).

### Hero de cada e-mail (dois seguidos nunca iguais)

| E-mail | Hero | Imagem | Fallback aprovado |
|---|---|---|---|
| 01 Memorial Day | **E16** Hero Photo Block (foto grande arredondada, texto embaixo em claro quente) | `feature-family.jpg` (família no acampamento) | já é aprovado |
| 02 Stain & Odor | **E19** Product Cluster como hero (v0.3, pendente de aprovação) | composição nova `e19-cluster-stain-odor-reset.jpg` (3 packshots do e-mail) | **E04** Hero Product com `pack-men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt-360.png` |
| 03 Art of Being Unseen | **E02** Hero Photo (foto de largura total + headline em duas vozes + filetes laranja em Tap Shoe) | recorte novo `hero-family-walk.jpg` (família de camo entrando na mata) | já é aprovado |
| 04 Shoreline vs. Deep Water | **E15** Hero Photo Card (headline sobre o topo escuro da foto) | `card-fishing.jpg` (pescador na margem do rio, sem a linha) | já é aprovado |

Sequência: E16, E19 (ou E04), E02, E15. Com ou sem fallback, nenhum par seguido repete tratamento.

**Fotos (não existe banco de originais ainda):** cada foto aparece em **um único e-mail** do lote. `feature-family.jpg` (E1), `hero-family-walk.jpg` (E3, recorte novo de `references/Septemeber 10.png`), `card-fishing.jpg` (E4). O E2 não usa foto (hero de produto). Todas são recortes de e-mails já enviados, **substituir pelos originais do banco** quando chegarem. Foram descartadas: `hero-fishing.jpg` (mesma foto do E4, com a linha), as fotos de flanela do E22 (tema de outono/flanela, fora do lote) e o homem no blind do Sep 2 (boné laranja e rifle à mostra, contradiz "unseen" e o "não só caça").

### Sequência de fundos por e-mail (nenhuma banda vizinha da mesma cor)

| E-mail | Sequência (↯ = E18 borda rasgada, ⤵ = E21 travessia) |
|---|---|
| 01 | branco (E01) → claro quente `#E2DDD9` (E16) → branco (E05) ↯ Major Brown `#483F39` (E17) ↯ Tap Shoe `#2A2B2D` (E13+E14) |
| 02 | branco (E01) → Tap Shoe → Major Brown (E19, degradê) ↯ claro quente (E05) ↯ Major Brown (E17) ↯ Tap Shoe (rodapé) |
| 02 fallback | branco (E01) → claro quente (E04) → branco (E05) ↯ Major Brown (E17) ↯ Tap Shoe (rodapé) |
| 03 | branco (E01) → foto → Tap Shoe (E02) ⤵ claro quente (E05) ↯ Major Brown (E17) ↯ Tap Shoe (rodapé) |
| 03 fallback | igual, com ↯ E18 `edge-light` no lugar do ⤵ E21 |
| 04 | branco (E01) → claro quente (E15, troca de superfície) ↯ Major Brown (E17 Shoreline) ⤵ Patriot Blue `#202944` (E17 Open Water, troca de superfície) ↯ Tap Shoe (rodapé) |
| 04 fallback | igual, com fronteira reta no lugar do ⤵ E21 |

### Dependência da v0.3

| Módulo v0.3 | Onde | Fallback aprovado |
|---|---|---|
| E19 Product Cluster | E2, hero | E04 Hero Product (sequência "02 fallback") |
| E21 Band-Crossing Product | E3, entre hero e E05 · E4, entre Shoreline e Open Water | E3: E18 `edge-light` · E4: fronteira reta |

E1 não depende da v0.3. Nenhum e-mail usa E20, E22 ou E23.

### Links

| Placeholder | Onde | Destino |
|---|---|---|
| `{{CTA_URL}}` | todos os botões e links de texto de E1, E2 e E3; hero de E4 | [[CONFIRMAR: URL da coleção de cada e-mail]] (um destino por e-mail, rules §6) |
| `{{SHORELINE_URL}}` · `{{OPEN_WATER_URL}}` | botões das duas bandas de produto de E4 | [[CONFIRMAR]]; mesma família (pesca) que `{{CTA_URL}}` do E4 |
| URL da variante | card de produto (nome, preço e packshot) | a `url` de `products.json`, exatamente (tabelas abaixo) |
| `{{HOME_URL}}`, `{{MENS_URL}}`, `{{WOMENS_URL}}`, `{{YOUTH_URL}}`, `{{SALE_URL}}`, `{{INSTAGRAM_URL}}` | E01 e rodapé | como no kit |

---

## E1 · Memorial Day · `01-memorial-day.html` · Designer A

- **ICP:** The Weekend Outdoor Adventurer (Diagnostic Report) · teme comprar roupa "técnica demais" que só serve no mato e pagar caro por algo que não usa sempre (inferido) · precisa de conforto com tempo instável, peças que vão do mato ao dia a dia, wicking/cooling
- **Mensagem-chave (Strategy Report):** "We're hunters, but that's not all we do" (pesca, camping, fim de semana em família) · condição cumprida? **sim** (todo e-mail de marca)
- **Mensagem única:** para o fim de semana longo de Memorial Day, um kit leve que acompanha do píer ao acampamento.
- **Assunto:** Memorial Day prep: pack once, go all weekend (44) · copy nova, revisar
- **Preheader:** UPF layers and a packable rain jacket for when the weather changes its mind. (76) · copy nova, revisar
- **Botão:** `#FF6400` / `#2A2B2D`

| Banda | Módulo | Conteúdo |
|---|---|---|
| 1 Preheader | | acima |
| 2 Logo | E01 Header | como no kit |
| 3 Hero | **E16** Hero Photo Block (claro quente) | Foto: `feature-family.jpg` 560x327, alt "A family in Habit camo relaxing in camp chairs at the edge of a field" · Eyebrow: `MEMORIAL DAY PREP` · H1: `GEAR FOR THE LONG&nbsp;WEEKEND` (destaque: WEEKEND) · Subtítulo (linha do módulo): `FROM SUNRISE FISHING TRIPS TO NIGHTS BY THE FIRE, VERSATILE GEAR MAKES EVERY STOP&nbsp;EASIER.` · Botão: `SHOP MEMORIAL DAY GEAR` → `{{CTA_URL}}` |
| 4 Ângulo (Bloco 2) | **E05** Text Block (branco, padrão) | H2: `PACK ONCE. ADVENTURE ALL&nbsp;WEEKEND.` (destaque: ONCE.) · Subtítulo (D1): `LIGHTWEIGHT LAYERS AND SUN PROTECTION FOR WHEREVER THE WEEKEND TAKES&nbsp;YOU.` · Corpo: "A long weekend outdoors means changing weather, changing plans, and gear that has to keep up. Whether you're setting up camp or casting lines at sunrise, dependable performance matters. Explore breathable UPF hoodies, quick-dry fishing shirts, utility shorts, and lightweight outerwear designed for comfort from dock to campsite." · Link (2º parágrafo do módulo, sozinho): "Gear Up for the Weekend" → `{{CTA_URL}}` |
| | E18 | `td bgcolor="#FFFFFF" class="dm-surface"` + `edge-brown.png` |
| 5 Produto (Bloco 3) | **E17** Product Cards (Major Brown, 3 cards, D2) | H2: `YOUR LONG WEEKEND CHECKLIST STARTS&nbsp;HERE` (destaque: HERE, laranja) · Subtítulo: `DURABLE ESSENTIALS MADE FOR WATER, TRAILS, AND EVERYTHING IN&nbsp;BETWEEN.` · Cards: tabela abaixo · Botão: `SHOP THE COLLECTION` → `{{CTA_URL}}` |
| | E18 | `td bgcolor="#483F39"` + `edge-tapshoe.png` |
| 6 Rodapé | E13 + E14 | como no kit |

| Card | Linha 1 | Linha 2 | Preço | Packshot (assets/) | Alt | URL |
|---|---|---|---|---|---|---|
| 1 | MLF MEN&rsquo;S 1/4 ZIP CAMO | Performance Layer | $29.99 USD | `pack-mlf-1-4-zip-camo-performance-layer-400.png` | Habit MLF Men's 1/4 Zip Camo Performance Layer in Marlin Blue | https://www.habitoutdoors.com/products/mlf-1-4-zip-camo-performance-layer?variant=47952634413338 |
| 2 | MEN&rsquo;S FLUSHING BAY | Short Sleeve Fishing Shirt | $29.99 USD | `pack-mens-flushing-bay-short-sleeve-river-shirt-400.png` | Habit Men's Flushing Bay Short Sleeve Fishing Shirt in Marlin Blue | https://www.habitoutdoors.com/products/mens-flushing-bay-short-sleeve-river-shirt?variant=49918052925722 |
| 3 | MEN&rsquo;S ROARING SPRINGS | Packable Rain Jacket | $59.99 USD | `pack-men-s-roaring-springs-packable-rain-jacket-400.png` | Habit Men's Roaring Springs Packable Rain Jacket in Peacoat and Marlin Blue | https://www.habitoutdoors.com/products/men-s-roaring-springs-packable-rain-jacket?variant=39299390472243 |

Bandas: 6. Uma banda de estrutura (E17). v0.3: nenhuma.

**Desvios do copy-fonte:**
- Bloco 1 headline "Memorial Day Prep: Gear for the Long Weekend" dividida em eyebrow `MEMORIAL DAY PREP` + H1 `GEAR FOR THE LONG WEEKEND`: mesma ordem e mesmas palavras, sai só os dois-pontos. Motivo: o E16 tem eyebrow acima da headline e o gancho sazonal vai na frente (rules §6). Responsável pode pedir a headline inteira no H1.
- Bloco 3 "Highlighted Categories & Products:" **cortado** (A3): nota de produção, não copy. Os links viraram os 3 cards.
- Nomes de produto nos cards: título da loja (`products.json`), dividido em linha 1 / linha 2 no padrão do E17.

**Confirmar antes do envio:** preços dos 3 produtos · data de envio (o e-mail inteiro depende do Memorial Day: o último foi 2026-05-25, o próximo é 2027-05-31) · C1: o corpo cita "UPF hoodies" e "utility shorts", e nenhum dos 3 produtos é hoodie ou short; UPF confirmado em 2 dos 3 (MLF 1/4 Zip, Flushing Bay) · links de variante pré-selecionam tamanho (L, S, S).

---

## E2 · Stain & Odor Reset · `02-stain-odor-reset.html` · Designer A

- **ICP:** The Passionate Hunter & Weekend Angler (Diagnostic Report) · teme equipamento que falha no campo e pagar preço de marca top sem precisar (inferido) · precisa de desempenho confiável a preço inteligente; valoriza anti-microbial e anti-stain
- **Mensagem-chave (Strategy Report):** "Our products work hard, and so do we" (tecnologia: Scent-Factor®) · condição cumprida? **sim para a mensagem**, mas o claim que a sustenta está em aberto (C2: Scent-Factor® só no Cedar Branch Bomber; nenhum dos 3 produtos cita resistência a mancha)
- **Mensagem única:** depois de uma temporada de pesca, renove as peças que já viram de tudo, com roupa que controla odor e limpa fácil.
- **Assunto:** Fish slime, sweat, bait, smoke (30) · copy nova, revisar
- **Preheader:** Your favorite shirts have seen it all. Maybe it's time for a fresh rotation. (76) · copy nova, revisar
- **Botão:** `#FF6400` / `#2A2B2D`

| Banda | Módulo | Conteúdo |
|---|---|---|
| 1 Preheader | | acima |
| 2 Logo | E01 Header | como no kit |
| 3 Hero | **E19** Product Cluster **(v0.3, pendente de aprovação)**, usado como hero | Linha de título (Tap Shoe): eyebrow do módulo **sai** (o cliente não tem eyebrow) · headline no `<h2>` do módulo trocado por `<h1>` (só a tag, mesmo estilo): `THE &ldquo;STAIN &amp; ODOR&rdquo;&nbsp;RESET` (destaque: RESET, laranja) · Imagem: `e19-cluster-stain-odor-reset.jpg` 600x360 (job A3), linkada em `{{CTA_URL}}`, alt "Habit Cedar Branch bomber in Realtree APX, Performance Fleece Hoodie and Fourche Mountain fishing shirt" · Linha de corpo (Major Brown): no lugar do parágrafo do módulo, o subtítulo (D1) em branco: `FISH SLIME, SWEAT, BAIT, SMOKE. SPRING FISHING LEAVES A&nbsp;MARK.` · Botão: `REFRESH YOUR FAVORITES` → `{{CTA_URL}}` |
| | E18 | `td bgcolor="#483F39"` + `edge-light.png` (troca `edge-light-dm.png` no dark mode, como no kit) |
| 4 Ângulo (Bloco 2) | **E05** Text Block, superfície trocada para claro quente `#E2DDD9` (classe `dm-band` no lugar de `dm-surface`) | H2: `TOUGH ON ODOR. EASY ON&nbsp;CARE.` (destaque: CARE.) · Subtítulo (D1): `PERFORMANCE APPAREL DESIGNED TO FIGHT ODOR AND CLEAN UP EASILY AFTER EVERY&nbsp;TRIP.` · Corpo: "By mid-season, your favorite shirts have seen it all. That's why Scent-Factor&reg; technology helps keep odors under control while lightweight performance fabrics make cleanup simple after long days on the water. Stay fresher between washes and ready for whatever tomorrow's forecast looks like." · Link: "Shop Fresh Performance Gear" → `{{CTA_URL}}` |
| | E18 | `td bgcolor="#E2DDD9" class="dm-band"` + `edge-brown.png` |
| 5 Produto (Bloco 3) | **E17** Product Cards (Major Brown, 3 cards, D2) | H2: `YOUR GEAR HAS BEEN THROUGH&nbsp;IT` (destaque: THROUGH, laranja) · Subtítulo: `SIGNS IT MIGHT BE TIME TO REFRESH YOUR ROTATION WITH PERFORMANCE GEAR BUILT FOR&nbsp;MORE.` · Cards: tabela abaixo · Botão: `SHOP PERFORMANCE ESSENTIALS` → `{{CTA_URL}}` |
| | E18 | `td bgcolor="#483F39"` + `edge-tapshoe.png` |
| 6 Rodapé | E13 + E14 | como no kit |

**Fallback sem v0.3 (hero E04):** banda 3 = **E04** Hero Product (claro quente): eyebrow do módulo sai · H1 `THE &ldquo;STAIN &amp; ODOR&rdquo;&nbsp;RESET` (destaque RESET, `#2A2B2D`) · parágrafo do módulo = subtítulo (D1, `#2A2B2D`) `FISH SLIME, SWEAT, BAIT, SMOKE. SPRING FISHING LEAVES A&nbsp;MARK.` · botão `REFRESH YOUR FAVORITES` · packshot `pack-men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt-360.png` 180x180, alt "Habit Men's Fourche Mountain Long Sleeve River Guide Fishing Shirt in black". Banda 4 E05 volta ao branco (`dm-surface`) e a borda E18 entre hero e E05 sai (claro para branco, fronteira reta). Resto igual.

| Card | Linha 1 | Linha 2 | Preço | Packshot (assets/) | Alt | URL |
|---|---|---|---|---|---|---|
| 1 | MEN&rsquo;S CEDAR BRANCH | Insulated Waterproof Bomber | $74.99 USD | `pack-habit-mens-wj657-cedar-branch-insulated-waterproof-bomber-400.png` | Habit Men's Cedar Branch Insulated Waterproof Bomber in Realtree APX camo | https://www.habitoutdoors.com/products/habit-mens-wj657-cedar-branch-insulated-waterproof-bomber?variant=51265344733466 |
| 2 | MEN&rsquo;S PERFORMANCE | Fleece Hoodie | $49.99 USD | `pack-mens-performance-fleece-hoodie-400.png` | Habit Men's Performance Fleece Hoodie in Flint Stone | https://www.habitoutdoors.com/products/mens-performance-fleece-hoodie?variant=45600303677722 |
| 3 | MEN&rsquo;S FOURCHE MOUNTAIN | Long Sleeve River Guide Fishing Shirt | $34.99 USD | `pack-men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt-400.png` | Habit Men's Fourche Mountain Long Sleeve River Guide Fishing Shirt in black | https://www.habitoutdoors.com/products/men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt?variant=32728036802611 |

Bandas: 6. Uma banda de estrutura (E17); o hero E19 mostra os mesmos 3 produtos como imagem (é a cara do "reset"), o E17 dá nome e preço. v0.3: E19.

**Desvios do copy-fonte:**
- A1 · Bloco 1 subheadline: "Fish slime, sweat, bait, smoke—spring fishing leaves a mark." → "Fish slime, sweat, bait, smoke. Spring fishing leaves a mark." Motivo: travessão proibido (rules §7, regra da operação). A estação fica como está até a data de envio ser decidida.
- A2 · Bloco 2 copy: "Scent-Factor™technology" → "Scent-Factor&reg; technology". Motivo: o guia (p.21) registra Scent-Factor® com ®, e faltava o espaço.
- A3 · Bloco 3 "Highlighted Categories & Products:" **cortado**: nota de produção. Os links viraram os 3 cards.
- Tipográfico: aspas retas de `The "Stain & Odor" Reset` viram curvas (&ldquo; &rdquo;). Sem mudança de texto.

**Confirmar antes do envio:** preços dos 3 produtos · data de envio ("spring fishing" e "By mid-season" amarram o e-mail à primavera) · **C2** (principal do lote): "Stain & Odor", "fight odor", Scent-Factor® em camisas; Scent-Factor® só existe no Cedar Branch Bomber (caça) e nenhum produto cita mancha · C3: o subtítulo do Bloco 3 promete "signs" e a banda só traz produtos · link do Fourche Mountain pré-seleciona o tamanho **4XL** (e M, M nos outros).

---

## E3 · The Art of Being Unseen · `03-art-of-being-unseen.html` · Designer B

- **ICP:** The Weekend Outdoor Adventurer (Diagnostic Report), aqui quem observa: fotógrafo de fauna, quem faz trilha e explora · teme roupa técnica demais que só serve na caça (inferido) · precisa de conforto, versatilidade e peças que vão do mato ao dia a dia. Secundário: The Passionate Hunter & Weekend Angler (camo que ele já conhece, fora da temporada)
- **Mensagem-chave (Strategy Report):** "We're hunters, but that's not all we do" · condição cumprida? **sim**. Red flag 2 (clube fechado de caçador) evitada também na imagem: nenhuma foto com arma
- **Mensagem única:** camuflagem também é para quem quer observar a natureza em silêncio.
- **Assunto:** The art of being unseen (23) · copy nova, revisar
- **Preheader:** Camo for wildlife photographers, scouts and anyone who likes to watch quietly. (78) · copy nova, revisar
- **Botão:** `#FF6400` / `#2A2B2D`

| Banda | Módulo | Conteúdo |
|---|---|---|
| 1 Preheader | | acima |
| 2 Logo | E01 Header | como no kit |
| 3 Hero | **E02** Hero Photo (Tap Shoe, padrão) | Foto: `hero-family-walk.jpg` 600x263 (job B1; `height` do `<img>` = 263), linkada em `{{CTA_URL}}`, alt "A family in Habit camo walking into the woods, seen from behind" · H1 em duas vozes: linha sans `THE ART OF BEING` + palavra serif `UNSEEN` · dois filetes laranja (do módulo) · Subtítulo (D1), no lugar do parágrafo do módulo, branco: `CAMO ISN'T JUST FOR THE HUNT. IT'S FOR EVERY MOMENT NATURE REWARDS&nbsp;PATIENCE.` (antítese mantida, ver "Em aberto") · Botão: `SHOP CAMO GEAR` → `{{CTA_URL}}` |
| | **E21** Band-Crossing Product **(v0.3, pendente de aprovação)** | Linha `td bgcolor="#2A2B2D"` com `e21-cross-youth-bear-cave.jpg` 600x330 (+ `e21-cross-youth-bear-cave-dm.jpg` com `img-light`/`img-dark`, como no kit), job B3, linkado na URL da Youth Bear Cave Tee, alt "Habit Youth Bear Cave Long Sleeve Camo Tee in Realtree APX" · **Fallback:** E18 `td bgcolor="#2A2B2D"` + `edge-light.png` (troca `edge-light-dm.png`) |
| 4 Ângulo (Bloco 2) | **E05** Text Block, superfície trocada para claro quente `#E2DDD9` (`dm-band`) | H2: `BLEND IN. SEE&nbsp;MORE.` (destaque: MORE.) · Subtítulo (D1): `BUILT FOR WILDLIFE PHOTOGRAPHERS, SCOUTS, AND ANYONE WHO PREFERS TO OBSERVE WITHOUT&nbsp;INTERRUPTION.` · Corpo: "The outdoors changes when you slow down enough to disappear into it. Quiet fabrics, natural patterns, and lightweight layers help you move unnoticed whether you're tracking wildlife with a camera or simply soaking in the stillness of the woods." · Link: "Explore Camo Essentials" → `{{CTA_URL}}` |
| | E18 | `td bgcolor="#E2DDD9" class="dm-band"` + `edge-brown.png` |
| 5 Produto (Bloco 3) | **E17** Product Cards (Major Brown, 3 cards, D2) | H2: `MADE FOR THE QUIET&nbsp;MOMENTS` (destaque: QUIET, laranja) · Subtítulo: `LIGHTWEIGHT PERFORMANCE GEAR DESIGNED TO KEEP YOU COMFORTABLE WITHOUT STANDING&nbsp;OUT.` · Cards: tabela abaixo · Botão: `STAY HIDDEN OUTDOORS` → `{{CTA_URL}}` |
| | E18 | `td bgcolor="#483F39"` + `edge-tapshoe.png` |
| 6 Rodapé | E13 + E14 | como no kit |

Cor do E17: linha mista (acessório + Youth). Fica o Major Brown padrão do E17; o taupe de Youth `#7F7064` seria só para bloco inteiro de Youth.

| Card | Linha 1 | Linha 2 | Preço | Packshot (assets/) | Alt | URL |
|---|---|---|---|---|---|---|
| 1 | KNIT CAMO | Stocking Cap | $12.99 USD | `pack-knit-camo-stocking-cap-400.png` | Habit Knit Camo Stocking Cap in brown camo | https://www.habitoutdoors.com/products/knit-camo-stocking-cap?variant=39479198580787 |
| 2 | YOUTH BEAR CAVE | Long Sleeve Camo Tee | $24.99 USD | `pack-youth-bear-cave-long-sleeve-camo-tee-400.png` | Habit Youth Bear Cave Long Sleeve Camo Tee in Realtree APX | https://www.habitoutdoors.com/products/youth-bear-cave-long-sleeve-camo-tee?variant=51763673661722 |
| 3 | ALL-PURPOSE CAMO | Leather Gloves | $19.99 USD | `pack-all-purpose-camo-leather-gloves-400.png` | Habit All-Purpose Camo Leather Gloves in green camo | https://www.habitoutdoors.com/products/all-purpose-camo-leather-gloves?variant=47156168098074 |

Bandas: 6. Uma banda de estrutura (E17). v0.3: E21.

**Desvios do copy-fonte:**
- A3 · Bloco 3 "Highlighted Categories & Products:" **cortado**: nota de produção. Os links viraram os 3 cards.
- Nenhum outro. A antítese do Bloco 1 fica como o cliente escreveu (decisão pendente, "Em aberto").

**Confirmar antes do envio:** preços (Youth Bear Cave tem `compare_at_price` 22.99 menor que o preço 24.99: mostrar só $24.99, nunca riscado, C7) · data de envio · C4: "Quiet fabrics" não conferido nos 3 produtos · links pré-selecionam tamanho (S na camiseta, M nas luvas).

---

## E4 · Shoreline vs. Deep Water · `04-shoreline-deep-water.html` · Designer B

- **ICP:** The Hardcore Hunter & Devoted Angler (Diagnostic Report), o pescador que passa o dia na água ou na margem · teme equipamento que não aguenta uso pesado e marca "de loja de departamento" que não entende a prática (inferido) · precisa de precisão técnica: waterproof, wicking, tração. Secundário: The Passionate Hunter & Weekend Angler (pesca de margem)
- **Mensagem-chave (Strategy Report):** "Our products work hard, and so do we" (história de produto) · condição cumprida? **sim**
- **Mensagem única:** escolha o kit de pesca pelo lugar de onde você arremessa, margem ou barco.
- **Assunto:** Shoreline or deep water? Pick your kit (38) · copy nova, revisar
- **Preheader:** Your setup should match where you cast from. Mud and brush, or a slick deck. (76) · copy nova, revisar
- **Botão:** `#FF6400` / `#2A2B2D`

| Banda | Módulo | Conteúdo |
|---|---|---|
| 1 Preheader | | acima |
| 2 Logo | E01 Header | como no kit |
| 3 Hero | **E15** Hero Photo Card, superfície trocada para claro quente `#E2DDD9` (as duas células `dm-surface` do módulo viram `dm-band`, pra não encostar branco no branco do E01) | Foto: `card-fishing.jpg` (a do kit, fundo do card + VML) · eyebrow do módulo **sai** · H1 sobre o topo escuro da foto, branco: `SHORELINE VS. DEEP WATER:<br>CHOOSING YOUR&nbsp;KIT` (destaque: KIT, laranja) · Linha de corpo: subtítulo (D1) em `#2A2B2D`: `YOUR SETUP SHOULD MATCH WHERE YOU CAST&nbsp;FROM.` · Botão: `FIND YOUR FISHING KIT` → `{{CTA_URL}}` |
| | E18 | `td bgcolor="#E2DDD9" class="dm-band"` + `edge-brown.png` |
| 4 Produto 1 (Bloco 2) | **E17** Product Cards (Major Brown, 3 cards, D2 + D3) | H2: `SHORELINE&nbsp;READY` (destaque: READY, laranja) · Subtítulo: `DURABLE LAYERS AND RUGGED FOOTWEAR BUILT FOR MUDDY BANKS, BRUSH, AND UNEVEN&nbsp;TRAILS.` · Parágrafo de corpo (D3), branco 16/26, entre o subtítulo e o grid: "Fishing from shore means movement, rough terrain, and changing conditions. Utility pants, waterproof boots, and durable outer layers help you navigate brush, mud, and rocky edges without slowing down. Built for anglers who have ground to cover before they ever make a cast." · Cards: tabela "Shoreline" · Botão: `SHOP SHORELINE GEAR` → `{{SHORELINE_URL}}` |
| | **E21** Band-Crossing Product **(v0.3, pendente de aprovação)** | Linha `td bgcolor="#483F39"` com `e21-cross-mlf-hooded.jpg` 600x330 (job B5, duas cores escuras fixas, **sem** versão `-dm`), linkado na URL do MLF Hooded Performance Layer, alt "Habit MLF Men's Hooded Performance Layer with Gaiter in Sharkskin" · **Fallback:** fronteira reta (o kit não tem borda em Patriot Blue) |
| 5 Produto 2 (Bloco 3) | **E17** Product Cards, superfície trocada para Patriot Blue `#202944` (D2 + D3) | H2: `BUILT FOR OPEN&nbsp;WATER` (destaque: WATER, laranja: 4,84:1 em Patriot Blue) · Subtítulo: `LIGHTWEIGHT COMFORT AND GRIP-FOCUSED ESSENTIALS MADE FOR LONG DAYS ON&nbsp;DECK.` · Parágrafo de corpo (D3): "Boat days call for breathable performance. Stay cool with moisture-wicking hoodies, lightweight fishing shirts, and high-traction footwear designed to keep you steady on slick surfaces. When the sun stays high and the water stays rough, comfort matters." · Cards: tabela "Open Water" · Botão: `SHOP BOAT-READY GEAR` → `{{OPEN_WATER_URL}}` |
| | E18 | `td bgcolor="#202944"` + `edge-tapshoe.png` |
| 6 Rodapé | E13 + E14 | como no kit |

Troca do E17 para Patriot Blue: só o `bgcolor`/`background-color` da célula externa. Conferido: texto branco, contorno `#FEF4C6` e laranja da headline passam em `#202944`. Patriot Blue é banda do kit (E02, E11) e a cor de água dos e-mails enviados (Sep 22).

**Shoreline**

| Card | Linha 1 | Linha 2 | Preço | Packshot (assets/) | Alt | URL |
|---|---|---|---|---|---|---|
| 1 | MEN&rsquo;S 15&quot; WATERPROOF | All-Weather Rubber Boots | $69.99 USD | `pack-copy-of-mens-all-weather-boot-400.png` | Habit Men's 15 inch Waterproof All-Weather Rubber Boots in Mossy Oak Country DNA | https://www.habitoutdoors.com/products/copy-of-mens-all-weather-boot?variant=39916249776179 |
| 2 | MEN&rsquo;S ROARING SPRINGS | Packable Rain Pant, Gray Waves | $34.99 USD | `pack-habit-mens-roaring-springs-packable-rain-pant-1-400.png` | Habit Men's Roaring Springs Packable Rain Pant in Gray Waves | https://www.habitoutdoors.com/products/habit-mens-roaring-springs-packable-rain-pant-1?variant=31820086575155 |
| 3 | MEN&rsquo;S ROARING SPRINGS | Packable Rain Pant, Realtree Edge | $59.99 USD | `pack-habit-mens-roaring-springs-packable-rain-pant-400.png` | Habit Men's Roaring Springs Packable Rain Pant in Realtree Edge camo | https://www.habitoutdoors.com/products/habit-mens-roaring-springs-packable-rain-pant?variant=31746549415987 |

**Open Water**

| Card | Linha 1 | Linha 2 | Preço | Packshot (assets/) | Alt | URL |
|---|---|---|---|---|---|---|
| 1 | MLF MEN&rsquo;S HOODED | Performance Layer with Gaiter | $34.99 USD | `pack-mlf-hooded-performance-layer-with-gaiter-400.png` | Habit MLF Men's Hooded Performance Layer with Gaiter in Sharkskin | https://www.habitoutdoors.com/products/mlf-hooded-performance-layer-with-gaiter?variant=40557557448755 |
| 2 | MEN&rsquo;S 15&quot; WATERPROOF | All-Weather Rubber Boots | $69.99 USD | `pack-copy-of-mens-all-weather-boot-400.png` (o mesmo do Shoreline) | Habit Men's 15 inch Waterproof All-Weather Rubber Boots in Mossy Oak Country DNA | https://www.habitoutdoors.com/products/copy-of-mens-all-weather-boot?variant=39916249776179 |
| 3 | MEN&rsquo;S ROARING SPRINGS | Packable Rain Pant, Marlin Blue | $44.99 USD | `pack-men-s-roaring-springs-packable-rain-pant-400.png` | Habit Men's Roaring Springs Packable Rain Pant in Marlin Blue | https://www.habitoutdoors.com/products/men-s-roaring-springs-packable-rain-pant?variant=39299401875507 |

Bandas: 6 (preheader, logo, hero, Shoreline, Open Water, rodapé). **Exceção E-X1: duas bandas de estrutura** (rules §3 pede uma), porque o copy-fonte do cliente tem duas listas de produto que são o conteúdo do e-mail. **Pendente de aprovação do responsável.** Alternativa, se recusar: dividir em dois e-mails (Shoreline / Open Water). v0.3: E21.

**Desvios do copy-fonte:**
- A3 · Blocos 2 e 3 "Highlighted Categories & Products:" **cortado** nas duas bandas: nota de produção. Os links viraram os cards.
- Hero: headline inteira no H1, quebrada em duas linhas depois dos dois-pontos. Sem mudança de texto.
- Linha 2 dos cards de calça com a cor da variante ("Gray Waves", "Realtree Edge", "Marlin Blue", de `products.json`): as três calças têm o mesmo nome na loja e ficariam indistinguíveis. Dado da loja, não copy nova.

**Confirmar antes do envio:** preços (MLF Hooded tem `compare_at_price` 29.99 menor que o preço 34.99: mostrar só $34.99, C7) · data de envio · C5: o corpo do Shoreline diz "Utility pants" e as calças são rain pants; duas calças com o mesmo nome ($34.99 e $59.99) na mesma banda · C6: o corpo do Open Water cita "lightweight fishing shirts" e nenhuma camisa está na banda; a mesma bota aparece nas duas bandas · links pré-selecionam tamanho (bota **7**, calças M/L/S, hoodie L).

---

## Jobs de composição (assets novos)

Todos gravam em `clients/habit-outdoors/01-brand/email-kit/assets/` usando as funções de `email-kit/tools/compose.py` (Pillow + numpy). **Não editar o `compose.py`**: cada designer cria o seu script na pasta do lote, importando o módulo, e roda a partir da raiz do projeto. Todo job imprime peso e checagem de emenda; aceitar só desvio 0 ou 1 nas bordas e JPG < 150KB, PNG de produto < 80KB.

Cabeçalho comum dos dois scripts:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "01-brand" / "email-kit" / "tools"))
import compose as c
```

### Designer A · `clients/habit-outdoors/03-work/email/2026-broadcasts/compose_01-02.py`

| Job | Chamada | Saída |
|---|---|---|
| A1 packs E1 | `c.product_png("mlf-1-4-zip-camo-performance-layer--47952634413338", 400, "pack-mlf-1-4-zip-camo-performance-layer-400.png")` · `c.product_png("mens-flushing-bay-short-sleeve-river-shirt--49918052925722", 400, "pack-mens-flushing-bay-short-sleeve-river-shirt-400.png")` · `c.product_png("men-s-roaring-springs-packable-rain-jacket--39299390472243", 400, "pack-men-s-roaring-springs-packable-rain-jacket-400.png")` | 3 PNG 400x400 |
| A2 packs E2 | `c.product_png("habit-mens-wj657-cedar-branch-insulated-waterproof-bomber--51265344733466", 400, "pack-habit-mens-wj657-cedar-branch-insulated-waterproof-bomber-400.png")` · `c.product_png("mens-performance-fleece-hoodie--45600303677722", 400, "pack-mens-performance-fleece-hoodie-400.png")` · `c.product_png("men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt--32728036802611", 400, "pack-men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt-400.png")` · fallback E04: a mesma camisa com `360` → `pack-men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt-360.png` | 3 PNG 400 + 1 PNG 360 |
| A3 E19 hero E2 | `c.compose_cluster([{"file": "habit-mens-wj657-cedar-branch-insulated-waterproof-bomber--51265344733466", "height": 569, "cx": 378, "cy": 345, "angle": 8, "darken": 0.8}, {"file": "mens-performance-fleece-hoodie--45600303677722", "height": 506, "cx": 832, "cy": 336, "angle": -8, "darken": 0.8}, {"file": "men-s-fourche-mountain-long-sleeve-river-guide-fishing-shirt--32728036802611", "height": 607, "cx": 600, "cy": 374, "angle": 0}], "e19-cluster-stain-odor-reset.jpg", size=(1200, 720))` | JPG 1200x720, topo `#2A2B2D`, base `#483F39` |

Por que 1200x720 e não 840 como a amostra do kit: como hero, o botão precisa ficar perto da primeira tela de 375px (o kit-label do E19 avisa). Geometria = amostra do kit escalada 0,857. Se um packshot sair cortado ou a camisa da frente não dominar, ajustar `height`/`cx`/`cy` e registrar aqui.

### Designer B · `clients/habit-outdoors/03-work/email/2026-broadcasts/compose_03-04.py`

| Job | Chamada | Saída |
|---|---|---|
| B1 foto hero E3 | `img = c.ref_crop("Septemeber 10.png", (155, 3738, 1045, 4128))` · `c.save_jpg(c.fit(img, w=1200), "hero-family-walk.jpg")` | JPG ~1200x526. Recorte da foto dentro do card "GET OUT THERE" do Sep 10, sem texto e sem os cantos arredondados. Nativo 890px: ampliado 1,35x, fica abaixo de 2x (aceito como provisório). Exibir 600x263 (ajustar ao tamanho real que o job imprimir) |
| B2 packs E3 | `c.product_png("knit-camo-stocking-cap--39479198580787", 400, "pack-knit-camo-stocking-cap-400.png")` · `c.product_png("youth-bear-cave-long-sleeve-camo-tee--51763673661722", 400, "pack-youth-bear-cave-long-sleeve-camo-tee-400.png")` · `c.product_png("all-purpose-camo-leather-gloves--47156168098074", 400, "pack-all-purpose-camo-leather-gloves-400.png")` | 3 PNG 400 |
| B3 E21 E3 | `c.compose_band_cross("youth-bear-cave-long-sleeve-camo-tee--51763673661722", "e21-cross-youth-bear-cave.jpg", top=c.TAPSHOE, bottom=c.LIGHT, size=(1200, 660), seam=370, product_h=520, cx=330, angle=-5)` | JPG 1200x660 + `-dm.jpg` (base `#34353A`). A camiseta é mais larga que a jaqueta da amostra: `product_h` 520 e `cx` 330 pra não cortar na borda esquerda |
| B4 packs E4 | `c.product_png("copy-of-mens-all-weather-boot--39916249776179", 400, "pack-copy-of-mens-all-weather-boot-400.png")` · `c.product_png("habit-mens-roaring-springs-packable-rain-pant-1--31820086575155", 400, "pack-habit-mens-roaring-springs-packable-rain-pant-1-400.png")` · `c.product_png("habit-mens-roaring-springs-packable-rain-pant--31746549415987", 400, "pack-habit-mens-roaring-springs-packable-rain-pant-400.png")` · `c.product_png("mlf-hooded-performance-layer-with-gaiter--40557557448755", 400, "pack-mlf-hooded-performance-layer-with-gaiter-400.png")` · `c.product_png("men-s-roaring-springs-packable-rain-pant--39299401875507", 400, "pack-men-s-roaring-springs-packable-rain-pant-400.png")` | 5 PNG 400 (a bota serve às duas bandas) |
| B5 E21 E4 | antes: `c.save_jpg.__defaults__ = (c.MAX_JPG, c.BAND_HEXES + ("#202944",))` (o `compose.py` só corrige a emenda de Tap Shoe, Major Brown e claros; sem isso o Patriot Blue pode decodificar 1 a 3 níveis fora e mostrar uma caixa) · depois: `c.compose_band_cross("mlf-hooded-performance-layer-with-gaiter--40557557448755", "e21-cross-mlf-hooded.jpg", top=c.BROWN, bottom="#202944", dm_bottom=None, size=(1200, 660), seam=370, product_h=600, cx=300, angle=-5)` | JPG 1200x660, topo `#483F39`, base `#202944`, sem `-dm` (as duas bandas são escuras fixas) |

### Peso estimado por e-mail (imagens)

| E-mail | Imagens | Estimativa |
|---|---|---|
| 01 | `feature-family.jpg` 133KB + 3 packs + 2 edges + logos | ~300KB |
| 02 | E19 ~150KB + 3 packs + 3 edges (+ `edge-light-dm`) + logos | ~330KB (fallback ~220KB) |
| 03 | `hero-family-walk.jpg` ~100KB + E21 x2 ~190KB + 3 packs + 2 edges + logos | ~420KB |
| 04 | `card-fishing.jpg` 80KB + 5 packs + E21 ~100KB + 2 edges + logos | ~400KB |

O E4 tem 6 cards: conferir o HTML abaixo de 90KB.

---

## Decisões de construção (valem para o lote, pendentes de ok do responsável na revisão da etapa 5)

Os designers constroem assim; se o responsável recusar, o fallback está ao lado.

- **D1 · Subtítulo do cliente em módulo sem linha de subtítulo** (E02, E05, E15, E19): entra com o estilo "Subtítulo espaçado" do kit (o `<p>` de subtítulo do E16), logo abaixo da headline, no lugar do parágrafo de corpo quando o módulo só tem um. Mesmo padrão dos e-mails enviados (Sep 22: "COOLER MORNINGS. CHANGING CONDITIONS." sob a headline). Fallback: o subtítulo vai no parágrafo de corpo do módulo, em sentence case.
- **D2 · E17 com 3 cards** (2 + 1 centralizado, repetição da célula existente). Fallback: o kit precisa de um módulo "Product Cards 3" (volta ao Modo A, só esse módulo).
- **D3 · E17 com parágrafo de corpo** (só no E4, as duas bandas): o corpo do cliente entra entre o subtítulo e o grid, estilo de corpo do kit em branco. Fallback: dividir o E4 em dois e-mails, ou o cliente corta o parágrafo.
- **D4 · Eyebrow sem texto do cliente sai** (E19 no E2, E04 fallback, E15 no E4). Não se inventa eyebrow. No E1 o eyebrow vem da própria headline (desvio registrado).
- **D5 · CTA do Bloco 2 como link de texto** (E05 não tem botão): texto do cliente como está, sublinhado, no parágrafo final do E05. O botão laranja aparece no hero e na banda de produto (2 botões + 1 link por e-mail; E4 tem 3 botões).
- **D6 · Trocas de superfície** (permitidas, rules §5): E05 para claro quente (E2, E3), E15 para claro quente (E4), E17 para Patriot Blue (E4 Open Water). Elementos internos conferidos acima.
- **D7 · Corpo com 3 frases** (E1 B2, E2 B2, E4 B2 e B3) passa da régua de "no máximo duas frases antes de um CTA ou visual" (rules §6). Mantido: é copy aprovado do cliente e o E05 do kit prevê "2 or 3 sentences". Responsável decide se pede corte ao cliente.

## Para revisão do cliente (claims, do Copywriter; nada foi mudado)

- **C1** (E1, Bloco 2): "breathable UPF hoodies, quick-dry fishing shirts, utility shorts, and lightweight outerwear". UPF confirmado em 2 dos 3 produtos (MLF 1/4 Zip: Solar-Factor UPF 40+; Flushing Bay: Solar-Factor UPF 50+, Quick Dry). Nenhum hoodie nem short entre os produtos: confirmar que a coleção do CTA tem.
- **C2** (E2, headline, Bloco 2): "Stain & Odor", "fight odor", Scent-Factor® em "your favorite shirts". Scent-Factor® só no Cedar Branch Bomber (caça); Performance Fleece Hoodie e Fourche Mountain não têm controle de odor; nenhum dos 3 cita mancha. **O principal do lote:** trocar/adicionar produto com Scent-Factor® no contexto, ou suavizar o claim.
- **C3** (E2, Bloco 3): "Signs it might be time to refresh your rotation" promete uma lista que não vem. Ok como tom; avisar.
- **C4** (E3, Bloco 2): "Quiet fabrics" não conferido no gorro, na camiseta e nas luvas.
- **C5** (E4, Shoreline): "Utility pants, waterproof boots": bota waterproof confirmada; as calças são rain pants. Duas calças com o mesmo nome ($34.99 e $59.99) na mesma banda: intencional?
- **C6** (E4, Open Water): "high-traction footwear" sustentado pela bota; "moisture-wicking hoodies" confirmado no MLF Hooded; nenhuma "fishing shirt" na banda; a bota se repete nas duas bandas.
- **C7** (E3, E4): `compare_at_price` menor que o preço (Youth Bear Cave 24.99 / 22.99; MLF Hooded 34.99 / 29.99). Não mostrar preço riscado; reconfirmar.
- Links de variante levam a um tamanho pré-selecionado (ex.: Fourche Mountain 4XL, bota tamanho 7). Confirmar se o cliente quer esses links ou a página sem variante.

## Decisões registradas

- 2026-09-24: lote planejado com hero E16 / E19 (fallback E04) / E02 / E15; nenhuma foto repetida no lote; nenhuma linha de pesca desenhada. Email Designer, a aprovar pelo responsável.
- 2026-09-24 (decisões anteriores do responsável, do kit): sem merge field, sem endereço nem linha de motivo no rodapé, botão único `#FF6400`/`#2A2B2D`, produto sempre da loja.
- 2026-09-24 (Designer A, E1 e E2, construção): assets de A1 a A3 gravados em `2026-broadcasts/assets/` (instrução do responsável para este lote), não em `email-kit/assets/`; o `compose_01-02.py` só redireciona as funções de salvar do `compose.py`, sem editá-lo. E2 usa E19 (v0.3) com o fallback E04 escrito no comentário do topo.
- 2026-09-24 (Designer A, job A3): camisa da frente do E19 em `height` 700 / `cy` 352 (não 607 / 374). O packshot da loja é um modelo cortado no nariz e no meio da coxa; na geometria do brief os dois cortes ficavam soltos no meio da imagem como bordas duras. Assim eles caem nas linhas de borda e se fundem no Tap Shoe e no Major Brown. Emendas: topo desvio 0, base desvio 1.
- 2026-09-24 (Designer A, job A1): o packshot da loja `men-s-roaring-springs-packable-rain-jacket--39299390472243` tem uma faixa branca opaca nas 20 primeiras linhas (sobra do recorte), que aparecia como barra branca sobre a cabeça no card marrom. O script limpa as linhas de borda de largura total antes do recorte; o arquivo da loja não foi mexido.
- 2026-09-24 (Designer A, E2): E01 com a classe `dm-band` no lugar de `dm-surface` (só muda o dark mode: `#34353A`). Com `dm-surface` o cabeçalho vira `#2A2B2D` no dark e encosta no Tap Shoe do hero E19. No claro continua branco. O E3 (hero E02 Tap Shoe) tem a mesma fronteira.
- 2026-09-24 (Designer A, D1 e D2 como construídos): subtítulo D1 no E05 com o estilo do `<p>` do E16, mas `margin:0 0 20px 0` e sem `max-width`/`auto` (o E05 é alinhado à esquerda). D2: linha 2 do grid = `<td colspan="2" align="center">` com tabela de 50% (classe `fluid`, pra ocupar 100% no mobile) e dentro a célula `card-cell` com `padding:16px 4px 0 4px` (mesma largura dos cards da linha 1; no mobile vira `0 0 16px 0` como os outros).
- 2026-09-24 (Designer A): botão do E17 com o padding do próprio módulo (16px 64px), não 16px 36px como diz "Regras que valem para os 4": o kit vem antes do brief (rules §0). Apóstrofos do corpo e do preheader em `&rsquo;` (tipográfico, sem mudança de texto). A foto do E16 fica sem link, como no módulo.
- 2026-09-24 (Designer A): E1 e E2 não carregam `[[CONFIRMAR]]`. Preços reais de `products.json` (2026-09-24); a reconferência de preço e data de envio fica em "Confirmar antes do envio" de E1 e E2, neste brief.
- 2026-09-24 (Designer B, job B5): o E21 do E4 usa a imagem da loja só da peça (`PT10299Sharkskin.png`, 1ª imagem do produto no `catalog.json`, mesma cor Sharkskin), guardada em `2026-broadcasts/_src/` (só fonte, nenhum e-mail aponta para ela), com `product_h` 560 (não 600). O packshot da variante é um modelo cortado nos olhos e nos jeans: sobre a emenda, o rosto ficava cortado por uma linha dura no meio do Major Brown. O card do Open Water continua com o packshot da variante (`products.json`). Emendas do B5 com desvio 1 nas duas bordas: `#483F39` e `#202944` não voltam exatos de nenhum JPEG (nem em q100, arredondamento YCbCr); o PNG exato pesaria 113KB contra 32KB, então fica o JPG. B3 com desvio 0.
- 2026-09-24 (Designer B, E3 e E4 como construídos): E01 do E3 com `dm-band` (mesma correção do E2); o E4 fica com `dm-surface`, porque o hero E15 já é `dm-band` no dark e o cabeçalho encostaria nele. D1 e D2 iguais aos do Designer A (subtítulo do E05 com `margin:0 0 20px 0`; 3º card do mesmo jeito). D3: o subtítulo do E17 passa de `margin-bottom` 32px para 16px e o parágrafo de corpo leva os 32px até o grid. E21 do E4 sem a gêmea `-dm` e sem a classe `img-light` (senão o dark mode esconderia a única imagem). Tipográfico, sem mudança de texto: `&nbsp;` em `DEEP&nbsp;WATER:` (evita "WATER:" sozinho numa linha) e antes da cor na linha 2 dos cards das calças (`Gray&nbsp;Waves` etc.); apóstrofos em `&rsquo;` no subtítulo e no corpo do E3.
- 2026-09-24 (Designer A, rodada 2, E1): refeito pela `art-direction-r2.md` com kit v0.4 **rascunho** (não é versão de envio). 5 bandas: E24 hero de tela cheia (logo branco sobre a foto, sem E01) com `crop-sent-sep15-camp-chairs-family.jpg` e céu de fim de tarde gerado acima da foto (Patriot escuro até âmbar na linha das árvores; a foto não tem área calma), rasgando para água Patriot · E26 foto rasgada `crop-sent-sep10-utv-hunters.jpg` + E25 em `tex-grain-patriot-water` · E18 texturizada · E25 em papel claro com leque de 3 produtos (PNG transparente, sangrando nas duas bordas) e nome/tipo/preço vivos embaixo de cada peça · E18 · rodapé. Os produtos são Marlin Blue: por isso ficaram no papel claro e o Patriot virou a banda de apoio do ângulo. Descartada a `sep10-truck-hunter` (rifle à mostra).
- 2026-09-24 (Designer A, rodada 2, E2): E24B com o celeiro recomposto (`r2-02-hero-barn.jpg`: base Major Brown com grão 4,2 em vez do papel Tap Shoe do kit, rasgando para `tex-paper-tapshoe`), colagem estábulo + fardo de feno rasgados em `tex-paper-tapshoe`, E21 com os 3 produtos jogados atravessando o rasgo Tap Shoe → Major Brown (imagem única), banda `tex-grain-brown` com headline, nomes vivos e botão, E18 para o rodapé. 5 bandas (a travessia é divisor).
- 2026-09-24 (Designer A, rodada 2, E1 e E2): copy igual à rodada 1, mesmos desvios (A1, A2, A3 e divisão eyebrow/H1 do E1). Só tipográfico: `<br>` antes de "EASY ON CARE." no H2 do E2. Packshots de modelo (Roaring Springs Jacket, Fourche Mountain) recortados abaixo do queixo e acima das mãos com borda rasgada (recorte de catálogo), para não aparecer rosto cortado no leque/pilha. Assets em `2026-broadcasts/assets/r2-01-*` e `r2-02-*` (jobs `r2_01`, `r2_02` do `compose_01-02.py`; as funções v0.4 do `compose.py` recebem caminho absoluto de saída, sem editar o kit).
- 2026-09-24 (Designer A, rodada 2, achado de kit v0.4): no mobile, imagem que abre a `<td>` (E26) encolhe com a tela e a textura de fundo fica em 600px, criando emenda visível logo abaixo da foto. Nos e-mails 01/02 a `<td>` texturizada leva a classe `r2-tex` com `background-size:100% auto` no mobile. Propor a mesma regra no E25/E26 do kit (não mexi no kit).
- 2026-09-24 (Designer B, rodada 2, E3): refeito pela `art-direction-r2.md` com kit v0.4 **rascunho** (não é versão de envio). 5 bandas: E24 hero de tela cheia (logo branco sobre a foto, sem E01) com `crop-sent-sep15-family-forest-walk.jpg` recomposto (`r2-03-hero.jpg`: tom mais frio e verde, banco de neblina gerado atravessando a família, céu em névoa escura para o texto, branco 9,3:1) · E25 em `tex-camo-blur` só com texto vivo e muito espaço (104/120px) · E26 canoa no rio fechado de mata (`crop-sent-sep22-canoe-river.jpg`, rasgada em cima e à direita, -2°, em névoa) abrindo a banda `tex-grain-ivy` · 3 produtos grandes, um por linha em zigue-zague (camiseta cortada pela borda esquerda do e-mail, gorro, luvas), névoa atrás de cada peça, nome/tipo/preço vivos ao lado · E18 com fibra de papel para o rodapé. Botão no hero e no fim da banda Ivy; "Explore Camo Essentials" continua link (D5).
- 2026-09-24 (Designer B, rodada 2, E4): 5 bandas + travessia. E24 hero com `crop-sent-sep22-angler-tackle-box.jpg` ampliada (névoa azul-escura gerada do próprio rio, branco 13:1), rasgando para a terra · "Shoreline" em textura de terra nova `r2-04-tex-earth.jpg` com colagem de janela rasgada (foto do pescador na margem `sep22-wading-river`, desfocada por ser recorte de 304px) e as duas Roaring Springs por cima, legendas vivas embaixo · E21 em textura: a bota (que o cliente pôs nas duas listas) em pé sobre o rasgo terra → água, como imagem de fundo da célula, legenda viva à direita · "Open Water" em textura de água nova `r2-04-tex-water.jpg` com janela rasgada sobre os três pescadores no barco (`sep22-boat-anglers`), MLF Hooded + calça Marlin Blue por cima · E18 para o rodapé. Exceção E-X1 (duas bandas de estrutura) continua pendente.
- 2026-09-24 (Designer B, rodada 2, E3 e E4, copy): texto igual à rodada 1, mesmos desvios (A3; antítese do E3 mantida; E4 com headline inteira no H1). Só hierarquia e tipografia: H1 do E4 empilhado em "SHORELINE / VS. / DEEP WATER: / CHOOSING YOUR KIT" com **"VS." como palavra de destaque** (serifada laranja 84px; na rodada 1 era "KIT"); H2 do E3 "MADE FOR THE / QUIET / MOMENTS" e "BLEND IN. SEE / MORE." em duas vozes; `&nbsp;` em "Camo&nbsp;Tee", "Gray&nbsp;Waves", "Realtree&nbsp;Edge", "Marlin&nbsp;Blue", "Rubber&nbsp;Boots", "with&nbsp;Gaiter". **E4: a bota aparece uma vez só** (na travessia, entre as duas bandas), não duas como na rodada 1: é o mesmo produto e a mesma URL nas duas listas do cliente (C6). Se o responsável quiser a bota repetida dentro do Open Water, volta como legenda extra.
- 2026-09-24 (Designer B, rodada 2, técnica): (1) toda `<td>` texturizada com `background-size:100% auto` em todas as larguras (a textura escala junto com as imagens fluidas no mobile; mesmo achado do Designer A). (2) Imagem com textura assada só sobre textura de **grão fino** (papel, terra, água novas): a fase do grão não aparece; a atmosfera grande (névoa, foto) fica dentro da composição e some nas bordas. (3) Camo desfocado tem manchas grandes que não casam entre duas `<td>`: os dois rasgos da banda camo do E3 são **PNG transparente dentro da própria `<td>` camo** (`r2-03-tear-hero-camo.png`, `r2-03-tear-camo-ivy.png`), e o hero do E3 não tem rasgo próprio (derrete em papel Tap Shoe). Conferido em 680 e 375: sem emenda. (4) Todo rasgo meu leva sombra do papel de cima e uma **fibra clara de papel** (#E4DFD8, 55 a 65%) na borda rasgada, que é o efeito que a rodada 1 não tinha; as bordas do kit (`edge-tex-*`) não têm fibra, então os e-mails 03/04 usam bordas próprias `r2-0x-edge-*`. (5) Packshots de modelo (calças Realtree Edge e Marlin Blue): cintura e mãos escondidas sob a tira de papel de cima da janela rasgada, sapatos cortados por script (`_cut`); MLF Hooded com a imagem da loja só da peça (`_src/`, mesma Sharkskin, como no B5).
- 2026-09-24 (Designer B, rodada 2, contraste e peso): texto sobre textura medido na área do texto (1º/99º percentil, grão desfocado 3px): terra branco 9,6 · `#E2DDD9` 7,2 · laranja 3,25 (só nas serifadas de 90px, texto grande) · água branco 13,4 · `#E2DDD9` 10,0 · laranja 4,5 · legenda sobre a travessia branco 9,6. Peso: **E3 HTML 24,7 KB, imagens 658 KB** (maior: hero 149,6 KB) · **E4 HTML 27,3 KB, imagens 600 KB** (maior: hero 134 KB). Nenhuma imagem acima de 150 KB. Assets `2026-broadcasts/assets/r2-03-*`, `r2-04-*`, jobs `r2*` no `compose_03-04.py` (o `compose.py` do kit não foi editado: o script só redireciona `tex_path` e registra as texturas novas em tempo de execução). Assets da rodada 1 do E3/E4 continuam na pasta, sem uso.
- 2026-09-24 (Designer B, rodada 2, proposta de kit): `r2-04-tex-earth.jpg` (Major Brown com terra, pedrisco e torrão, grão fino, fallback `#483F39`) e `r2-04-tex-water.jpg` (Patriot Blue com estrias finas e brilhos, sem manchas grandes, fallback `#202944`) como texturas novas do v0.4; a `tex-grain-patriot-water` do kit tem manchas grandes que mostram emenda sob imagem assada. Também propor: fibra de papel nas bordas E18 texturizadas e o "rasgo PNG dentro da `<td>`" para qualquer textura de manchas grandes.
- 2026-09-24 (Designer A, correção QA rodada 2, E1): hero `r2-01-hero-camp.jpg` recomposto (job `r2_01`): a foto terminava em linha reta com uma faixa lisa de Tap Shoe de cerca de 24px antes do rasgo. Agora a foto é ampliada para 1500px e recortada a 1200 (x 60 a 1260, mantendo a mulher à esquerda), vai até o rasgo sem degradê e o rasgo morde a própria foto, com a água Patriot da banda seguinte dentro dele. 149,0 KB; branco 7,6:1 ou mais na área do texto. Conferido em 680/375/dark. Efeito colateral: o homem da direita fica mais cortado pela borda.
- 2026-09-24 (Designer B, correção QA rodada 2, E3): produtos de volta à ordem do cliente (Knit Camo Stocking Cap, Youth Bear Cave Tee, All-Purpose Camo Gloves). O zigue-zague continua (imagem à esquerda, direita, esquerda), e a sangria passou para a camiseta da linha do meio, agora cortada pela borda **direita** do e-mail (`r2-03-prod-tee.jpg` refeito, espelhado, +6°). No mesmo job, as três composições de produto ganharam uma base só de grão fino na média do `tex-grain-ivy` (a mancha lenta do recorte ficava de 1 a 2,5 níveis fora e mostrava o retângulo da imagem) e névoa com janela de 230px. Bordas agora a até 0,5 nível da textura, sem retângulo visível em 680/375/dark. Nada mais mudou; imagens 658 KB.

## Em aberto

- [[CONFIRMAR]] **Quinto e-mail:** o responsável falou em 5; o PDF tem 4.
- [[CONFIRMAR]] **Datas de envio.** Hoje é 2026-09-24. E1 é Memorial Day (próximo: 2027-05-31); E2 fala em "spring fishing" e "mid-season". Nenhuma estação foi reescrita. As fotos disponíveis são de outono (recortes dos e-mails de setembro): para um envio em maio, pedir originais de primavera/verão ao cliente.
- **Antítese do E3** (Bloco 1, subheadline): "Camo isn't just for the hunt. It's for every moment nature rewards patience." rules §7 proíbem "não é X, é Y"; mantida como o cliente escreveu. Alternativa do Copywriter, que também corrige o "when" que falta: "Camo for the hunt, the camera and every moment that rewards patience." O responsável decide e, se trocar, pede ok ao cliente.
- **Aprovação da v0.3** (E19, E21) antes da revisão da etapa 5; sem ela, os designers trocam pelos fallbacks escritos acima.
- **Exceção E-X1** (E4, duas bandas de estrutura): aprovar ou dividir o e-mail.
- **D1 a D7** acima.
- [[CONFIRMAR]] URLs de destino: `{{CTA_URL}}` de cada e-mail, `{{SHORELINE_URL}}`, `{{OPEN_WATER_URL}}`.
- [[CONFIRMAR]] Omnisend acrescenta endereço físico e descadastro (CAN-SPAM).
- Fotos provisórias (recortes de e-mails enviados): `feature-family.jpg`, `card-fishing.jpg`, `hero-family-walk.jpg`. Pedir os originais ao cliente.

## Envio

- (vazio)
