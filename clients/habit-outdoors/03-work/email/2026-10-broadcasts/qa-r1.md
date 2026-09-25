# QA rodada 1 · lote de outubro 2026 · 2026-09-25 · Email QA Reviewer

Escopo: os 5 e-mails de `2026-10-broadcasts/` (playbook etapa 6), contra `brief.md` (E1 a E5, X1 a X6, D1 a D5, C1 a C9), `copy-source.md`, `products.json`, `notes-A/B/C.md`, `email-ops/rules.md`, `CHECKLIST.md`, kit (README + tokens + components) e as referências `struct-r3-*`.
Renders 680 / 375 / `--dark` (altura 9000) em `scratchpad/oct/qa/` (`light/`, `dark/`, fatias em `sl/` e `sld/`). Contraste medido por pixel no render, mediana do fundo sem os pixels do texto.
Nenhum HTML editado.

Contexto que **não** conta como bloqueio nesta rodada (é rascunho para o responsável): módulos v0.4 e as estruturas novas do lote ainda sem aprovação no kit, `{{CTA_URL}}` e demais placeholders, `[[CONFIRMAR: endereço]]` no rodapé, tag de descadastro do Omnisend. Tudo isso está em "Pendências de envio".

## Resumo

| E-mail | Veredito | HTML | Imagens (desktop claro) | Todas as referenciadas | Bloqueios |
|---|---|---|---|---|---|
| 01 Cedar Branch Bibs | **BLOQUEIA** | 37,5 KB | 709 KB | 709 KB | 2 |
| 02 Youth | PASSA (rascunho) | 35,5 KB | 619 KB | 717 KB | 0 |
| 03 Heavy Weight Hoodie | PASSA (rascunho) | 32,1 KB | 647 KB | 1.102 KB | 0 |
| 04 Crater Valley | **BLOQUEIA** | 33,1 KB | **978 KB** | 1.289 KB | 2 |
| 05 Shadow Series | PASSA (rascunho) | 31,0 KB | 634 KB | 634 KB | 0 |

Conferido nos 5 e sem achado: nenhum travessão ou meia-risca, nenhum emoji (X1 aplicado nos assuntos do E1 e do E3), nenhum `#` em href, todos os `<img>` com `width`, `display:block`, `border:0` e `alt`; todo hex do HTML existe no kit (nenhum hex solto); todas as URLs de produto e todos os preços batem exatamente com o `products.json` (E1 $89.99 / $99.99 · E2 $79.99 / $29.99 / $29.99 · E3 3x $44.99 · E4 $29.99 / $49.99 / $54.99 · E5 3x $69.98), nenhuma URL de produto fora dele; copy conferido palavra por palavra contra as tabelas E1 a E5 do brief e o `copy-source.md` (headline, subtítulo, corpo, botão, cards, citações), com X1 a X6 aplicados; comentário de topo com Subject / Preheader / Modules / Button; preheader com espaçador; meta `color-scheme`; container 600 com tabela fantasma MSO; VML com `mso-padding-alt:0px` e `mso-fit-shape-to-text:true` em toda célula com imagem de fundo; botões `#FF6400` / `#2A2B2D`, 52px de altura, até 3 por e-mail; bandas ≤ 7, nenhuma vizinha com a mesma textura; texto do hero AA nos 5 (branco sobre a área do texto: E1 14,1:1 · E2 10,6:1 · E3 9,9:1 · E4 14,1:1 · E5 11,6:1).

---

## 01 Cedar Branch Bibs · BLOQUEIA

**BLOQUEIOS**

1. **[#27 / AD r2 princípio 4 "produto com peso" / armadilha "produto pequeno fica ruim"] Banda de produtos, linhas 171 e 194 (`o1-prod-bibs.jpg`, `o1-prod-parka.jpg`).** Os packshots ocupam pouco das imagens de 600x760: o bib ocupa cerca de 37% da largura e aparece com uns 110px de largura a 680 (a 375, a mesma coisa, porque `.bleed-l` mostra a imagem a 80%). A "sangria" é só a borda da perna encostando no limite do e-mail, então não lê como corte intencional da ref C. Embaixo da parka sobram uns 100px de textura vazia, mais os 64px de padding da linha 190. A banda fica com cara de espaço sobrando e produto perdido.
   **Correção (compose_A.py):** recompor as duas imagens com o produto ocupando cerca de 90% da altura e cortado de verdade pela borda do e-mail (20 a 30% da peça para fora, como a ref C e como o E5 já faz: lá o Mid Layer aparece com uns 250px de largura). Bib: ampliar cerca de 1,5x e deixar sair pela esquerda e por baixo (peitilho, alças, logo e coxas visíveis; a barra da calça pode sair do quadro). Parka: ampliar até uns 240px visíveis, com a manga cortada pela direita. Cortar a altura morta da imagem (o card de 300px de largura não precisa de 380px de imagem vazia) e baixar o padding de baixo da linha 190 para 40px. Alvo: nenhuma peça abaixo de 200px de largura visível a 680.

2. **[#16 / D2 / regra de foto do kit "close de detalhe"] Banda de reviews, linhas 236 e 260.** Dois dos três recortes de detalhe não comunicam tecido nem técnica:
   - `o1-detail-fabric.jpg` (loja `04.png`, acima dos selos): cordão branco e parte do logo "Realtree" sobre camuflagem lavada. Sem saber de onde veio, não se reconhece roupa, é um objeto não identificável.
   - `o1-detail-insulation.jpg` (loja `05.png`): o forro bege acolchoado, sem nenhuma referência de peça. Lê como travesseiro.
   - `o1-detail-legzip.jpg` (loja `07.png`, linha 284) funciona como ideia (zíper de perna sobre a bota), mas o recorte cortou a mão puxando o cursor e deixou o fundo cinza de estúdio aparecendo em cerca de 30% do quadro.
   **Troca recomendada** (todas já baixadas em `photos/products/`):
   - Review 1, Matthew B. ("jacket and bibs", "quiet"): `habit-mens-cedar-branch-insulated-waterproof-parka/06.png`, mão no bolso de peito com zíper, cursor laranja e logo HABIT bordado. Recortar acima do rótulo "Zippered Chest Pocket" (texto em imagem não entra). Lê na hora como jaqueta camuflada e construção.
   - Review 2, Ryan And L. ("insulated", "waterproof", "silent tech"): `ahabit-sup-sup-mens-insulated-bib/08.png`, mão abrindo o zíper central no peitilho marrom, logo HABIT laranja e a fita do zíper com HABIT. Lê como bib e acabamento.
   - Review 3, Andrew C. ("warm in the stand", "wear to work"): manter o `07.png`, mas recortar mais alto e mais aberto, com a mão puxando o cursor e a bota inteira no quadro, e fechar o recorte para o cinza de estúdio ficar numa faixa mínima.
   - Tirar do lote o `04.png` (fabric) e o `05.png` (isolamento).
   Os `alt` mudam junto. Todas as fotos de detalhe da loja são Realtree Edge e a variante vendida é APX (ver WARN abaixo).

**WARN**

- **[#18 / rules §7] Aspas retas removidas das citações (linhas 244 e 268).** Minha avaliação: **aceitável** para citação literal. Em citação destacada (pull quote, bloco de depoimento), a aspa grande de abertura substitui as aspas do texto, e isso é convenção tipográfica. As palavras não mudaram, e o Andrew já veio sem aspas. Três condições: (a) registrar como desvio no brief (X7: "aspas retas removidas nas citações do Matthew B. e do Ryan And L.; a aspa grande laranja marca a citação"), porque rules §7 pede que toda mudança fique no brief, e hoje ela está só no `notes-A.md`; (b) o marcador tem `aria-hidden="true"`, então no leitor de tela nada indica que é citação: envolver cada texto em `<blockquote style="margin:0;">` resolve sem mexer no visual; (c) se o cliente pedir as aspas de volta, elas entram sem mexer no layout.
- **[#20b / rules §7] 3 pontos de exclamação** na citação do Andrew C. (linha 292). É citação literal e o brief já manda sinalizar, não editar. Decisão do responsável ou do cliente (ver "Precisa do responsável").
- **[#16] Detalhe em Realtree Edge ao lado de produto vendido em APX.** Todas as fotos de detalhe da loja são Edge. Num close de tecido, o padrão é o assunto da foto, então o leitor vê uma camuflagem que o link não vende. Os `alt` já dizem Edge. Aceitável se o responsável concordar; senão, recortar o detalhe do próprio packshot APX (`...--49451798790426.png`, resolução baixa para close) ou pedir fotos de detalhe APX ao cliente.
- **[#15 / brief "Card de produto"] Cards das linhas 177-178 e 200-201:** linha 1 = `MEN'S CEDAR BRANCH`, linha 2 = `Insulated Waterproof Bibs`. O brief pede linha 1 = nome da loja inteiro e linha 2 = variante/tipo. Do jeito que está, a variante (Realtree APX) não aparece no card. Correção: linha 1 `MEN'S CEDAR BRANCH INSULATED WATERPROOF BIBS` (e a parka igual), linha 2 `Realtree APX`, como no E2 e no E5; ou registrar a divisão no brief.
- **[#20 / kit "Tecnologia com ® como na p.21"] `Rain-Factor waterproofing` (linha 162)** sem ®. A rodada 2 aplicou o ® como desvio registrado (A2). Decisão única para o lote todo (E1, E2, E5): ver "Precisa do responsável".
- **[a11y] Estrelas (linhas 243, 267, 291):** `aria-label` em `<p>` sem `role` é ignorado por boa parte dos leitores, que leem "black star" cinco vezes. Correção mecânica: `role="img"` no `<p>`.
- **[#15] Botão da faixa dividida (linha 344):** padding 16px 28px. O kit pede 16px 36px. Aceitável pela coluna estreita; registrar ou voltar para 36px.
- **[#22 / pendência] `SHOP HUNTING` e `SHOP CEDAR BRANCH` vão para o mesmo `{{CTA_URL}}`.** Se o destino for a coleção Cedar Branch, o rótulo "Hunting" promete outra página. É a mesma família (rules §6 permite), mas o responsável precisa decidir a URL do botão final (coleção hunting ou Cedar Branch).
- **[#9] Etiquetas do hero claras também no dark mode** (proposta do Designer A). No Apple Mail fica certo. No app do Gmail o `bgcolor` `#E2DDD9` pode inverter e o papel da imagem de fundo não. Testar no Gmail iOS/Android.

**OK:** 1, 2, 3, 5, 6, 7, 8, 10 (empilha, imagem primeiro; botão do hero a 375 termina em y 638 sem contar a margem da página), 11, 12 (pendências à parte), 13, 14 (estruturas novas pendentes de kit), 15 (tipografia e fallback), 17, 18 (X1, X2, X3, X6 aplicados; fora o X7 acima), 19, 21, 22, 23 (6 bandas, uma de estrutura, reviews como mudança de ângulo), 24, 25 (assunto 25 caracteres, preheader estende), 26.

---

## 02 Youth · PASSA (rascunho)

**BLOQUEIOS:** nenhum.

**WARN**

- **[#27 / armadilha "produto pequeno dentro de quadrado"] Packshots do tabuleiro (linhas 164 e 234).** O bib e a calça são peças altas e estreitas num quadro de 220x220: o bib aparece com uns 70px de largura dentro de um painel de 260px e sobra painel taupe dos dois lados. O hoodie (linha 199) está bem. Correção: recortar os PNG no limite do objeto e usar uma imagem mais alta (220x280, por exemplo) para a peça ocupar a altura do painel, ou ampliar 1,2 a 1,3x deixando a barra da calça encostar na base do painel.
- **[brief "Palavra de destaque"] `SEASON` laranja sobre a foto do hero (linha 120).** Mediana de 3,4:1 na área (passa 3:1 para texto grande, igual ao Major Brown), mas o brief limita o laranja a Tap Shoe, Patriot Blue e Major Brown, e o E3 e o E5 deixaram o destaque do hero branco pelo mesmo motivo. Decidir uma regra só para o lote: branco nos heróis de foto, ou laranja liberado na névoa escura medida.
- **[#20 / kit ®] `Rain-Factor waterproofing` (linha 151)**, mesma decisão do E1.
- **[#16 / C9] Hero** é o `crop-sent-sep15-camp-chairs-family.jpg`, o mesmo recorte do hero do 01 de maio. O brief permite (não há foto youth em locação), mas quem recebeu o de maio vai reconhecer a foto. Pedir ao cliente uma foto original com criança.
- **[#9] Banda 4 em papel claro:** no app do Gmail, o `bgcolor` e o texto `#2A2B2D` invertem e a imagem de fundo não. Testar no Gmail iOS/Android (mesmo WARN da rodada 2).
- **[#10] Subtítulo do hero a 680** quebra em `...REAL DAYS IN / THE FIELD.` Opcional: `IN&nbsp;THE&nbsp;FIELD.` para equilibrar.

**OK:** 1 a 9, 10 (tabuleiro empilha com o painel primeiro, `dir="rtl"` certo), 11 a 15, 17, 18 (copy literal, apóstrofo tipográfico em "They're" sem mudar palavra), 19, 21 a 26. Dark: a banda clara troca para `tex-paper-light-dm`, `COLD` fica laranja grande sobre `#34353A`, e as bordas trocam pelas gêmeas `-dm`.

---

## 03 Heavy Weight Hoodie · PASSA (rascunho)

**BLOQUEIOS:** nenhum.

**WARN**

- **[#16 / kit "nada de estúdio como hero"] Hero (linha 112):** packshot do hoodie "de pé" na frente dos carvalhos, sem pessoa. Não existe foto do produto em uso no banco nem na loja, e o Designer B já levou isso para o responsável. A imagem lê como montagem, não como produto em uso. Decisão do responsável; o melhor caminho é pedir ao cliente uma foto do hoodie vestido em locação.
- **[#4] Peso real acima do que a tabela sugere.** São 647 KB no desktop claro, mas cada painel tem 4 JPG (desktop, mobile e as gêmeas `-dm`) e o Gmail baixa todo `<img>`, mesmo escondido. Total referenciado: 1.102 KB. Correção sugerida: usar a imagem desktop também no mobile (`width:100%`) e aceitar o corte de 343 a 375px, ou cortar as gêmeas `-dm` do mobile. Isso tira cerca de 240 KB.
- **[#9] Dark mode (Apple Mail):** o painel Gunmetal (`#2A2B2D`) sobre o papel escuro `#34353A` quase some; a borda do painel não aparece. Correção: no dark mode, trocar o fundo da banda de papel para `#1E1F21`, ou dar ao painel Gunmetal um filete `#45464A`.
- **[#27] Mobile, painéis Gunmetal e Loden:** degrau de 1 a 2px na borda direita, onde a imagem encontra a `<td>` do texto (a imagem de 343px não chega à largura da célula). Só aparece ampliado. Correção: imagem mobile a 100% da célula, ou célula com a mesma largura da imagem.
- **[C5] "handwarmer pockets"** no corpo; na loja é "hand pockets". Copy do cliente, fica como está e vai para confirmação dele (já está no brief).

**OK:** 1 a 3, 5 a 8, 10 (painel empilha com a imagem primeiro, troca `d-/m-` certa), 11 a 15 (linha 2 com "Men's": diferença registrada no `notes-B.md`, ok pelo copy do E3), 17 a 19, 21 a 26 (4 bandas, uma de estrutura, assunto 26 caracteres).

---

## 04 Crater Valley · BLOQUEIA

**BLOQUEIOS**

1. **[#4 / D4] Peso: 978 KB no desktop claro (limite de cerca de 800 KB), e o GIF não compensa os 344,5 KB.** A exceção D4 (GIF até cerca de 350 KB) está pendente de ok e nunca incluiu o e-mail passar de 800 KB. O que aparece no render (linha 269, quadros extraídos do arquivo):
   - não é "lifestyle": são recortes de modelo de estúdio sobre cor chapada (cinza, azul, marrom, vermelho escuro). O kit proíbe estúdio como hero e o Strategy Report tem "lifestyle de estúdio" como red flag; aqui não é hero, mas é a banda que o cliente chamou de lifestyle;
   - paleta de 104 cores sem dither: posterização visível em pele, jeans e sherpa, e contorno de recorte nas bordas;
   - arquivo 1x (600px) numa tela 2x: fica mole no iPhone;
   - os rostos cortados na altura dos olhos pela tira de papel nos 4 cenários (bloqueio 2).
   **Correção, dois caminhos para o responsável escolher:**
   (a) **recomendado para este envio:** trocar pelo JPG estático (`o4-lifestyle-still.jpg`, 29 KB, recomposto por causa do bloqueio 2). O e-mail cai para cerca de 665 KB. Pedir ao cliente fotos ou vídeo reais da linha Crater Valley em uso e fazer o GIF quando existirem;
   (b) se o cliente insistir no GIF agora: refazer com 3 cenários, sem os quadros de crossfade de 110 ms, com dither, rostos resolvidos, até cerca de 250 KB, e o e-mail até cerca de 880 KB, com a exceção registrada no brief com data e ok do responsável.

2. **[#27 / #16] Rostos cortados na altura dos olhos em quatro lugares.** As fotos da loja vêm cortadas na testa, e o corte caiu no pior lugar:
   - hero desktop (linha 110, `o4-hero-a.jpg`): a borda de cima do e-mail corta o modelo no nariz. É a primeira coisa que se vê;
   - hero mobile (linha 121, `o4-hero-m.jpg`): a tira de papel rasgada cobre do nariz para cima;
   - moldura do Full Zip Fleece (linhas 185-186): a linha de cima da moldura passa pelos olhos;
   - GIF / still (linha 269): nos 4 cenários, a tira de papel tapa os olhos.
   Rosto cortado nos olhos lê como erro, e o modelo vira anônimo. **Correção (compose_B.py):** ou cortar abaixo da boca, na linha do queixo ou da gola (vira recorte de torso, lê como intencional e continua mostrando a peça), ou usar só fotos com a cabeça inteira (a `08` do Performance Hoodie tem, e é por isso que a moldura 1 funciona). Nunca cortar entre a testa e a boca.

**WARN**

- **[#10] Corpo das molduras a 15px** (linhas 166, 196, 226). Checklist #10 e kit: corpo 16px. Correção mecânica: 16px / 25px.
- **[#15] Botão do hero com padding 18px** (linha 105; kit: 36px, hero 64px). Justificado no `notes-B.md` (coluna de 286px). Aceitável, mas registrar no brief.
- **[#18] Ordem da banda 4:** headline, GIF, texto, botão (segue o copy). O brief põe o GIF primeiro. O designer seguiu o cliente, está certo; registrar no brief.
- **[#16 / C8] ¼ Zip:** packshot APX na moldura (é o que o link vende) e modelo Mossy Oak Bottomland no GIF. Decisão do responsável (ver notes-B #3).
- **[#25] Preheader com 31 caracteres** (rules §3 pede 40 a 90). É o texto do cliente e o brief manda manter; só sinalizar.
- **[#9] Dark:** nada troca, bandas escuras fixas. OK no Apple Mail.

**OK:** 1 a 3, 5 a 8, 10 (texto antes da imagem no mobile, e o botão do hero termina em y 452 a 375), 11 a 14, 17, 18 (X4, X5 aplicados; nomes sem "Men's" como o brief pede; `¼` literal), 19, 21 a 24, 26.

---

## 05 Shadow Series · PASSA (rascunho)

**BLOQUEIOS:** nenhum.

**WARN**

- **[#23 / rules §3] Duas bandas de estrutura** (faixa de atributos, linhas 121-160, e linhas de produto, linhas 174-264). O brief planeja assim, mas a exceção precisa de ok explícito do responsável registrado no brief com data (o Designer C levantou a mesma coisa).
- **[#20 / kit ®] `RAIN-FACTOR` / `SCENT-FACTOR` sem ®** (linhas 133 e 139). Mesma decisão do E1 e do E2. A rodada 2 aplicou o ® como desvio A2.
- **[#16] Windproof Fleece Pant (linha 207):** o packshot da variante mostra uma blusa cinza de meia-zip no manequim, que não é vendida junto. Correção: recortar a imagem na cintura/suspensórios, ou deixar como está e confirmar com o cliente.
- **[#15] Preço sem negrito** (linhas 195, 219, 243). Nos outros 4 e-mails o preço sublinhado é 700 com tracking 1px. Igualar para o lote ler como um sistema.
- **[C5] Claims da faixa:** "Grid Fleece Interior" só existe no Mid Layer; "Windproof Construction" só na calça e na jaqueta Windproof. É copy do cliente e já está no C5; confirmar com ele.
- **[C3] Preço promocional $69.98** (compare_at $99.99) sem preço riscado: reconfirmar no dia 29/10.

**OK:** 1 a 13, 14 (estruturas novas pendentes de kit), 15, 17 a 19, 21, 22, 24 a 26. Produtos com peso de verdade (é a referência de correção para a banda de produtos do E1). Contraste: `OUTLASTS` laranja 72px sobre o topográfico passa como texto grande (3,9:1 medido pelo Designer C).

---

## Pendências de envio (não bloqueiam a revisão do responsável)

- `{{CTA_URL}}` dos 5 (coleção Cedar Branch/hunting, Youth, página do hoodie, Crater Valley, Shadow Series) e `{{HOME_URL}}`, `{{MENS_URL}}`, `{{WOMENS_URL}}`, `{{YOUTH_URL}}`, `{{SALE_URL}}`, `{{INSTAGRAM_URL}}`, com UTM.
- Endereço físico: `[[CONFIRMAR]]` visível nos 5 rodapés (linha 386 no E1, 347 no E2, 311 no E3, 316 no E4, 295 no E5). Sai antes do envio (trava de CAN-SPAM e de rules §8).
- `{{UNSUBSCRIBE_URL}}`: confirmar a tag do Omnisend e se o ESP já acrescenta rodapé próprio (senão o descadastro sai duplicado).
- Aprovação do kit v0.4 e das estruturas novas do lote (etiqueta, linha sangrando + caixa, caixa de review, faixa dividida, tabuleiro, painéis, moldura aberta, faixa de atributos, ícones, GIF): rules §5 "só módulos do kit".
- Preços e variantes reconfirmados na data de cada envio (C3, C4, C8); datas "Tuesday" do PDF (C1).
- Imagens no CDN do Omnisend, com caminho absoluto.
- Testes reais: Gmail iOS/Android no dark mode (etiquetas do E1, papel claro do E2 e do E3), Outlook 2016/365 no Litmus (VML estica as texturas; painéis do E3 lisos no Outlook), Apple Mail.
- Liberação das fotos originais `orig-*` (C9) e das citações com nome (C6).

## Precisa do responsável / cliente

1. **E1 aspas:** aprovar a remoção das aspas retas (recomendo aceitar, registrar como X7 e envolver em `<blockquote>`).
2. **E1 Andrew C.:** 3 exclamações numa citação literal. Manter (a citação não se edita) ou o cliente escolhe outro review da página.
3. **E1 detalhe em Realtree Edge** ao lado do produto APX: aceitar ou pedir detalhes APX.
4. **® nas tecnologias** (E1, E2, E5): seguir o kit e a rodada 2 (A2, com ®) ou o copy do cliente (sem).
5. **E4 D4:** caminho (a) JPG estático agora ou (b) GIF refeito com exceção de peso registrada. E pedir ao cliente material lifestyle real de Crater Valley.
6. **E3 hero** produto sobre paisagem, sem pessoa (pedir foto do hoodie em uso).
7. **E5:** registrar a exceção de duas bandas de estrutura; restrição de envio da calça para CA/NY (notes-C #3).
8. **E2 e E3:** regra única para o laranja no destaque de hero de foto.
9. **E1 `SHOP HUNTING`:** URL própria da coleção hunting ou a mesma da Cedar Branch.

---

## Re-conferência r1b (2026-09-25)

Escopo: só os bloqueantes da rodada 1 no E1 e no E4, mais o ® no E2 e no E5, contra `notes-A.md`, `notes-B.md` e `notes-C.md`. Renders próprios 680 / 375 (altura 9000) em `scratchpad/oct/qa2/`, quadros do GIF extraídos um a um. Nenhum HTML editado.

| E-mail | Veredito r1b | HTML | Imagens desktop claro | Mobile claro | Todas as referenciadas |
|---|---|---|---|---|---|
| 01 Cedar Branch Bibs | **PASSA (rascunho)** | 37,5 KB | 725 KB | 725 KB | 725 KB |
| 02 Youth | PASSA (rascunho) | 35,5 KB | sem mudança | | |
| 04 Crater Valley | **PASSA (rascunho), condicionado ao ok da D4** | 32,8 KB | 887 KB | 859 KB | 1.208 KB |
| 05 Shadow Series | PASSA (rascunho) | 31,0 KB | sem mudança | | |

### 01 Cedar Branch Bibs · PASSA (rascunho)

- **Bloqueio 1, produtos (linhas 171 e 194): resolvido, com WARN.** As duas peças agora ocupam a altura da imagem e saem de verdade pela borda (bib pela esquerda, parka com a manga cortada pela direita), a altura morta caiu (300x360) e o padding de baixo da parka está em 40px. Medido no render a 680: bib com cerca de 145px de largura visível, parka com cerca de 185px; a 375, bib cerca de 160px e parka cerca de 210px. O alvo de 200px da rodada 1 não é possível para o bib num quadro de 360px de altura (a peça mede 0,38 de largura por altura); o bib lê como produto, com peitilho, alças e logo. WARN: a parka ainda caberia uns 10% maior, e o vão entre o card do bib e a parka segue generoso a 680. Não bloqueia. A opção de trocar pelo bib vestido (só existe em Realtree Edge) fica com o responsável (`notes-A.md`, item 6).
- **Bloqueio 2, detalhes D2 (linhas 236, 260, 284): resolvido.** `o1-detail-pocket.jpg` lê na hora como bolso de jaqueta camuflada com a mão e o logo bordado, e é Realtree APX. `o1-detail-zipper.jpg` lê como peitilho do bib com o zíper e o logo HABIT. `o1-detail-legzip.jpg` mostra zíper de perna e bota inteira, sem o cinza de estúdio. WARN menor: no legzip só as pontas dos dedos entram, cortadas pela borda de cima; lê como gesto, não como erro. `o1-detail-fabric.jpg` e `o1-detail-insulation.jpg` saíram do HTML e da pasta.
- **`<blockquote>` (linhas 244, 268, 292): OK.** `margin:0; padding:0; border:0` inline, visual igual. Estrelas com `role="img"` e `aria-label`. X7 registrado no `notes-A.md`; falta o responsável levar para o `brief.md`.
- **`Rain-Factor®` (linha 162): OK**, como `&reg;`.

### 04 Crater Valley · PASSA (rascunho), condicionado ao ok da D4

- **Rostos (bloqueio 2): resolvido.** Hero desktop (`o4-hero-a.jpg`): a borda de cima corta no pescoço, abaixo do queixo. Hero mobile (`o4-hero-m.jpg`): a tira rasgada cai no pescoço. Moldura do Full Zip Fleece (linhas 185-186), desktop e mobile: a linha de cima passa na gola. GIF `o4-lifestyle.gif`, 3 quadros conferidos: quadro 1 (2,6 s, as três peças) com os três cortados no pescoço; quadro 2 (2 s) Performance Hoodie com o rosto inteiro dentro da janela; quadro 3 (2 s) ¼ Zip Excape cortado na gola. Nenhum corte entre a testa e a boca. WARN menor: no hero mobile, logo abaixo da tira rasgada, há alguns pontos escuros sobre a pele do pescoço (resíduo da sombra da tira); só aparece ampliado.
- **Peso (bloqueio 1): dentro do teto de ~900 KB.** GIF em 244,9 KB (3 cenas, corte seco, 152 cores, 1x); desktop claro 887 KB, mobile claro 859 KB. Continua acima dos ~800 KB da regra: passa **só com a exceção D4 registrada no `brief.md` com data e ok do responsável**. Sem esse ok, volta o caminho (a): `o4-lifestyle-still.jpg` (32 KB) no lugar do GIF, e o e-mail cai para cerca de 674 KB. O Gmail baixa todas as variantes (1.208 KB referenciados): WARN, como no E3.
- **Corpo das molduras (linhas 166, 196, 226): OK**, 16px / 25px.
- WARN (fora do escopo desta re-conferência, só registro): o GIF continua sendo modelo de estúdio recortado sobre um fundo desfocado de foto real. Resolve a "cor chapada" da rodada 1, mas não é lifestyle de verdade; o pedido de material real de Crater Valley ao cliente continua de pé.

### 02 Youth e 05 Shadow Series · ®

- E2, linha 151: `Rain-Factor&reg;`. OK.
- E5, linhas 133 e 139: `RAIN-FACTOR&reg;` e `SCENT-FACTOR&reg;`. OK. O WARN de ® da rodada 1 sai dos três e-mails; a decisão "kit com ® contra copy do cliente sem ®" (item 4 de "Precisa do responsável") foi aplicada pelos designers a favor do kit (A2); falta o ok do responsável no brief.

### Continua pendente (não bloqueia)

Tudo de "Pendências de envio" e de "Precisa do responsável" da rodada 1, com duas mudanças: os itens 1 (X7) e 4 (®) já estão aplicados nos HTMLs e só falta o ok do responsável no brief; o item 5 (D4) passou a ser a condição do E4.
