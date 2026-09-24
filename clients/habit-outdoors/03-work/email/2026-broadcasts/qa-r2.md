# QA rodada 2 · 2026-09-24 · Email QA Reviewer

Escopo: o que mudou na rodada 2 (art-direction-r2.md). Mesmas regras de contexto da rodada 1: sem endereço/descadastro no corpo (Omnisend, conferir no envio), sem merge field, entrega via Figma, placeholders esperados, módulos v0.3/v0.4 pendentes são esperados, E-X1 no 04 e a antítese do 03 já registradas.
Renders: 680 / 375 / --dark em `scratchpad/habit/qa2/`. Contraste medido por pixel no render, na área do texto (mediana do fundo, sem os pixels do texto).

Veredito: **PASS nos 4 como rascunho de revisão. Nenhum BLOCK técnico. Nenhum liberado para envio** (kit v0.4 e as pendências da rodada 1 continuam abertos). Nenhuma correção aplicada: nada do que foi encontrado é mecânico.

| E-mail | HTML | Imagens | Maior imagem | Botão do hero a 375 |
|---|---|---|---|---|
| 01 | 27,9 KB | 575 KB claro (+87 KB textura dm só no dark) | hero 145,6 KB | y 332 a 384 |
| 02 | 26,9 KB | 572 KB | hero 148,0 KB | y 560 a 611 |
| 03 | 24,4 KB | 658 KB | hero 149,6 KB | y 305 a 355 |
| 04 | 27,3 KB | 600 KB | hero 134,4 KB | y 352 a 404 (o problema do botão abaixo da dobra da rodada 1 está resolvido) |

---

## 01 Memorial Day · PASS (rascunho)

**BLOCK:** nenhum.

**WARN**
- [#24 / AD princípio 2 e 3] Hero E24: a foto termina numa linha reta e fica uma faixa chapada Tap Shoe de uns 24px antes do rasgo para o Patriot (680: y 750 a 775; 375: y 640 a 660). Fica como um corte de imagem sem querer, não um degradê. Correção: recompor `r2-01-hero-camp.jpg` (job `r2_01`) levando a foto, ou um degradê que nasce dela, até o rasgo.
- [#9] App do Gmail: a banda de papel claro (E25 `dm-tex`) é o único plano claro do lote. O Gmail inverte o `bgcolor` e o texto `#2A2B2D`, mas não a imagem de fundo: headline, nomes e preços podem ficar claros sobre papel claro. A troca por `dm-tex` só funciona no Apple Mail e no Outlook.com, e o render de dark mode confirma que lá fica certo. Correção: testar no Gmail iOS e no Android antes do envio. Se falhar, a decisão de kit é aplicar a técnica de mix-blend do Gmail no texto da banda, ou deixar a banda sem imagem de fundo quando o dark mode está ativo.

**OK:** VML íntegro nas 3 células (a do hero com `height`, `mso-padding-alt`, `fit-shape-to-text`, cor do `v:fill` igual ao `bgcolor`) · fallbacks `#2A2B2D` / `#202944` / `#E2DDD9` com texto AA sozinho (branco 13:1 e 14:1, `#2A2B2D` sobre `#E2DDD9` 10:1) · contraste sobre a textura: subtítulo do hero 11,7:1, eyebrow 15,6:1, "WEEKEND" laranja 4,3:1 (texto grande), corpo `#E2DDD9` sobre a água do Patriot 10,4:1, "ONCE." 4,6:1 · sem emenda nas bordas E18 a 680 e 375 · as bordas trocam no dark (`img-light`/`img-dark`, escondidas inline com `mso-hide`) · copy igual à rodada 1 (eyebrow/H1, A3) · preços e URLs batem com o products.json · sem travessão, `[[CONFIRMAR]]` ou `#`.

## 02 Stain & Odor Reset · PASS (rascunho)

**BLOCK:** nenhum.

**WARN**
- [#10] A 375, o botão final "SHOP PERFORMANCE ESSENTIALS" quebra em 2 linhas. A altura continua acima de 44px, então é só estética. Correção: no mobile, `letter-spacing:1px` em `.btn-full a`, ou aceitar.
- [#4] O hero tem 148,0 KB (151,5 kB decimal), sem folga nenhuma no limite de 150. Correção opcional: baixar a qualidade do JPG 2 ou 3 pontos.

**OK:** VML em 3 células · fallbacks `#2A2B2D` / `#483F39` com branco AA (13:1 e 10,3:1) · contraste: H1 do hero sobre a transição foto → marrom 10,3:1 (mobile 10,1:1), subtítulo 10,4:1, corpo sobre o papel Tap Shoe 10,5:1, nomes e tipos sobre o grão marrom 7,6:1, "THROUGH" laranja 3,4:1 (texto grande, 56px) · sem emenda entre Tap Shoe → pilha → marrom a 680 e 375 (o `r2-tex` com 100% no mobile funciona) · dark mode idêntico ao claro (bandas escuras fixas) · copy com A1 e A2 (Scent-Factor®) e `<br>` registrado · preços e URLs batem.

## 03 The Art of Being Unseen · PASS (rascunho)

**BLOCK:** nenhum.

**WARN**
- [#18] Ordem dos produtos: camiseta, gorro, luvas. No copy-fonte é gorro, camiseta, luvas, e a troca não está registrada como desvio (a nota do Designer B só descreve o zigue-zague). Correção: registrar no brief, com o motivo (camiseta sangrando na borda abre a sequência), ou voltar à ordem do cliente.
- [#4] O hero tem 149,6 KB (153,2 kB decimal), no limite. Mesma correção opcional do 02.

**OK:** VML em 3 células · fallbacks `#483F39` / `#595442` com branco AA (10,3:1 e 7,6:1) · os rasgos PNG dentro da `<td>` camo resolvem a emenda (conferido a 680 e 375) · os blocos JPG dos produtos sobre o grão Ivy têm degrau de luminância ≤ 2 níveis na borda, invisível sem ampliar · contraste: subtítulo do hero 12,5:1, subtítulo sobre o camo 10,3:1, corpo sobre o camo 12:1 (mobile 10,6:1), link 11,9:1, legendas sobre o Ivy 7,8:1 · dark mode idêntico · copy igual à rodada 1 (antítese mantida) · preços e URLs batem (camiseta $24.99 sem riscado, C7).

## 04 Shoreline vs. Deep Water · PASS (rascunho)

**BLOCK:** nenhum.

**WARN**
- [#23 / emendas] Topo do `r2-04-shore-pants.jpg`: degrau de uns 1,5 nível de luminância a 680, e o pedrisco assado tem outra fase. Só aparece ampliado ou com contraste forçado. Aceitável como está. Se quiser zerar: recompor com a textura de terra na mesma fase do fundo.

**OK:** VML em 4 células · a travessia (E21) usa `v:textbox` sem `fit-shape-to-text` **de propósito**: a altura é fixa em 360, e o fit encolheria o retângulo até a legenda e cortaria a bota · fallbacks `#483F39` / `#202944` com branco e `#E2DDD9` AA · contraste: subtítulo do hero 17:1; sobre a terra, subtítulo 10,3:1, corpo `#E2DDD9` 7,5:1, legendas 10,2:1, "READY" laranja 3,2:1 (serifada de 90px, texto grande); legenda da travessia 10,1:1 (a 680 e a 375); sobre a água, subtítulo 14,2:1, corpo 10,6:1, legendas 14,4:1, "WATER" 4,6:1 · emenda terra → travessia → água limpa a 680 e 375 · legenda da bota cabe a 375 · dark mode idêntico · os 3 placeholders de destino estão registrados (mesma família, E-X1) · a bota aparece uma vez só (registrado, C6) · preços e URLs batem (MLF Hooded $34.99 sem riscado, C7).

---

## Resumo do lote

- **Outlook (item 1 do foco):** as 13 células com imagem de fundo têm VML íntegro (abre e fecha), `bgcolor` e `v:fill color` iguais, `mso-padding-alt:0px` e `fit-shape-to-text` (exceto a travessia do 04, justificada acima). Com as imagens desligadas ou sem VML, todo texto continua AA só com o `bgcolor`. **WARN do lote:** o `v:fill type="frame"` estica a textura de 1200x1600 até a altura da banda (a Ivy do 03 chega a uns 1.480px). No Outlook desktop o grão fica alongado, e as imagens com textura assada (rasgos, janelas, fotos rasgadas) vão mostrar emenda contra o fundo esticado. É a degradação esperada, e a legibilidade está garantida. Conferir no Litmus (Outlook 2016/365) antes do envio.
- **Contraste (2):** todo texto de corpo e legenda ≥ 7,5:1 onde está de fato. Laranja ≥ 3,2:1, e só em serifada de 56 a 90px (texto grande, o mínimo é 3:1). O mais justo é "READY" no 04.
- **Emendas (3):** a correção de mobile dos designers (`background-size:100% auto`, PNG de rasgo dentro da td) funciona. Nenhuma emenda visível a 680 nem a 375. Restam só o hero do 01 (faixa chapada, WARN) e o degrau sutil do 04.
- **Peso (4):** todos abaixo de 90 KB de HTML e de 800 KB de imagem. Nenhuma imagem passa de 150 KB, mas os heroes do 02 e do 03 estão colados no limite.
- **Dark mode (5):** 02, 03 e 04 são escuros fixos, com render dark idêntico ao claro. O 01 troca certo no Apple Mail e no Outlook.com. Risco no app do Gmail só na banda de papel do 01 (teste obrigatório).
- **Copy e dados (6):** texto igual à rodada 1 com os desvios registrados. Nenhum travessão, `[[CONFIRMAR]]` no HTML ou `#`. Todo hex está no kit. Os 15 preços e as URLs de variante batem com o products.json. Pendência nova: registrar a ordem dos produtos do 03.
- **Mobile (7):** os 4 botões de hero dentro dos primeiros 667px. Sem overflow a 375.

**Correções aplicadas:** nenhuma.

**Pendente antes do envio (sem bloquear agora):** tudo da rodada 1 (CAN-SPAM no rodapé do Omnisend, URLs dos placeholders, preços reconferidos, tamanhos nos links) + teste no Litmus/Outlook das texturas VML + teste do 01 no app do Gmail (iOS e Android) em dark mode.

**Precisa do responsável ou do cliente:** C1, C2, C4, C5, C6, C7, E-X1, frase do 03, datas de envio e aprovação do kit v0.3/v0.4 (sem mudança desde a rodada 1) + **novos:** hero do 01 (recompor até o rasgo?) e ordem dos produtos do 03 (registrar ou voltar à do cliente).
