# QA rodada 2 · lote de outubro 2026 · 2026-09-25 · Email QA Reviewer

Escopo: os 5 HTML reconstruídos na rodada 2, contra `revision-r2.md` (vale acima do brief), as imagens `email-kit/references/rev-oct-01..05-*.png`, `brief.md`, `copy-source.md`, `products.json`, `notes-A/B/C.md` (seções "Rodada 2"), `qa-r1.md`, kit v0.5 (README) e `email-ops/rules.md` / `CHECKLIST.md`.
Renders 680 / 375 / `--dark` (altura 9000) em `scratchpad/qa2/` (`light/`, `dark/`), lado a lado com a rev-oct em `sbs/` (imagem do responsável | render claro | render dark) e mobile claro | dark em `mob/`. Largura real da coluna medida por pixel em cada render.

**Exceções aceitas (aponto, não bloqueio):** texto branco no botão `#FF6400` (2,97:1, escolha do responsável); endereço e descadastro fora do HTML (vêm do rodapé do Omnisend); fotos provisórias 1x recortadas das rev-oct (`o1-rev-archer`, `o2-rev-boy`, `o3-rev-hero`, `o4-rev-sunset`) e a foto do hero do 05 diferente da revisão; um review só no 01. Também não bloqueia nesta rodada (rascunho para o responsável): kit v0.5 ainda sem aprovação, placeholders `{{...}}`.

## Resumo

| E-mail | Veredito | HTML | Imagens (desktop claro) | Todas as referenciadas | Bloqueios |
|---|---|---|---|---|---|
| 01 Cedar Branch Bibs | **PASSA** (rascunho, depois da correção aplicada) | 32,0 KB | 716 KB | 716 KB | 0 (1 corrigido) |
| 02 Youth | **BLOQUEIA** | 34,5 KB | 517 KB | 619 KB | 1 |
| 03 Heavy Weight Hoodie | **PASSA** (rascunho) | 31,1 KB | 543 KB | 765 KB | 0 |
| 04 Crater Valley | **BLOQUEIA** | 34,8 KB | ~731 KB | **1.026 KB** | 2 (+1 corrigido) |
| 05 Shadow Series | **PASSA** (rascunho) | 30,3 KB | 548 KB | 548 KB | 0 |

**Conferido nos 5, sem achado:** nenhum travessão, meia-risca nem emoji (varredura de caractere e de entidade); nenhum `#` em href; todo `<img>` com `width`, `border:0` e `alt` (os sem `display:block` inline são os gêmeos mobile/dark escondidos com `display:none` inline, certo); todos os arquivos de imagem referenciados existem; HTML abaixo de 90 KB e toda imagem abaixo de 150 KB; container 600 com tabela fantasma MSO; VML com `mso-padding-alt:0px` e `mso-fit-shape-to-text:true` em toda célula com fundo (o 05 põe o padding no `inset` do textbox, certo); preheader com espaçador; meta `color-scheme`; logo branco sobre foto; comentário de topo com Subject / Preheader / Modules / Button; assuntos até 50 caracteres (25, 31, 26, 25, 35), preheader estende o assunto.

**Copy e produto conferidos palavra por palavra:** headline, subtítulo, corpo e botão de todos os blocos batem com o `copy-source.md` (com os desvios X1, X2, X6, X7 e o ® do brief). Nomes, variantes, preços e URLs batem com o `products.json` (01 $89.99 / $99.99 · 02 $79.99 / $29.99 / $29.99 · 03 3x $44.99 nas 3 variantes · 04 $29.99 / $49.99 / $54.99 · 05 3x $69.98, Mossy Oak Terra Coyote). **Os dois erros de copy das imagens não aparecem:** o primeiro card do 04 diz `CRATER VALLEY PERFORMANCE HOODIE` (não "YOUTH CEDAR BRANCH", linha 170) e a terceira caixa do 05 não tem a linha "Insulated Bib" (linhas 220 a 222).

**Fidelidade às rev-oct:** os 5 seguem a imagem do responsável em ordem de bandas, hierarquia, escala, cor e posição (conferido lado a lado). As diferenças que sobram são as que os designers registraram (Prompt mais estreita que a fonte da imagem, quebras de linha do corpo, retícula mais suave no 01, foto do hero do 05) e as apontadas abaixo.

---

## Achados que valem para o lote todo (WARN)

- **G1 · [#15 / #22] O botão não é idêntico nos 5.** O kit v0.5 diz Prompt 800 17px, tracking 2px, 52px de altura. Hoje: 01 e 02 com 18px, tracking 3px, 54px (linhas 143/257 do 01, 130/233/270 do 02); 03 com 17px / 2px, mas o hero tem padding de 18px e 56px de altura (linha 119); 04 hero com tracking 1,5px (linha 106); 05 com 18px, tracking 2,5px no hero e 4px no SHOP NOW (linhas 110 e 236). **Correção:** igualar ao kit (17px, tracking 2px, padding vertical 16px), variando só a largura. A largura fixa copiada de cada imagem pode continuar.
- **G2 · [#14 / #15] A caixa de produto (E27) muda de e-mail para e-mail.** Na linha 2: 01 mostra só o tipo em `#CFC8BF` 15px, sem variante; 02 mostra o tipo em branco 16px mais a variante 13px `#B0A89C`; 05 mostra o nome inteiro no título e a variante 14px `#CFC8BF`; 04 usa descrição. O contorno também muda: 05 usa `#FEF4C6` sólido, 04 e agora 01/02 usam `#FEF4C6` com rgba a 70% (ver correções aplicadas). O título de 16px no 02 é permitido pelo kit sobre Tap Shoe. **Correção:** fechar um padrão só no kit (título / nome ou tipo 15px branco / variante 13px / preço 20px, contorno com rgba 70% e `#FEF4C6` de fallback) e aplicar nos 5. O 05 precisa só acrescentar `border-color:rgba(254,244,198,0.7);` nas linhas 180, 199 e 218. O 01 continua sem a variante (Realtree APX), como na imagem (já era WARN na r1).
- **G3 · [#15] Rodapé com dois desenhos.** 01 e 02 usam menu 16px peso 500 e copyright 13px `#FFFFFF`; 03, 04 e 05 usam menu 17px peso 400 e copyright 14px `#E2DDD9`, com outro espaçamento. O ícone do Instagram já está em 44px nos 5 (as notas do C falavam em 36px, mas o HTML está em 44). **Correção:** um E14 só, copiado do `components.html`.
- **G4 · [#15 / Outlook] A serifa vira Arial no Outlook desktop no 03, 04 e 05.** O `<style>` MSO (linha 25/26) força `span { font-family: Arial !important }` e os spans da Playfair não têm a classe `serif`. Com isso COLDEST, WARM, CRATER VALLEY, LAST CALL, BITE BACK e THE WEATHER saem em Arial. O 01 e o 02 caem em Georgia, como o kit pede. **Correção:** acrescentar `class="serif"` nos spans da Playfair e `.serif { font-family: Georgia, 'Times New Roman', serif !important; }` no `<style>` MSO, como no 01/02.
- **G5 · [#18 / rules §7] O brief não registra as decisões da rodada 2.** Faltam: um review só no 01 (saem Matthew B. e Andrew C.); o **"CTA: Shop Now" do Bloco 2 do 01 saiu** (a imagem não tem, e as notas do A também não citam); o texto branco no botão (exceção 2,97:1); o rodapé sem endereço e sem descadastro; os 5 botões do 04 (substitui o X5); as cores de painel do 02 e do 05. **Correção:** uma seção "Rodada 2" em `brief.md`, com data, listando cada uma.
- **G6 · [#9] Gmail app no dark mode:** as etiquetas claras do hero do 01, o papel claro do 02 e o papel camo do 03 podem ter o `bgcolor` invertido sem a imagem. Testar no Gmail iOS/Android (mesmo WARN da r1).

---

## 01 Cedar Branch Bibs · PASSA (rascunho)

**BLOQUEIO corrigido nesta rodada**
- ~~[#13] Hex fora do kit `#E4DBB3` no contorno das duas caixas (linhas 177 e 200).~~ Trocado por `border:1px solid #FEF4C6; border-color:rgba(254,244,198,0.7);`, a mesma solução do 04: o hex do kit fica de fallback (Outlook) e o 70% da imagem vale onde o rgba funciona. Re-render conferido: só a área das caixas mudou.

**WARN**
- **[#10] Banda 2 no mobile (linha 165, `.bib-img`):** o bib fica com 210px, alinhado à esquerda, e sobram uns 165px de retícula vazia à direita por cerca de 560px de altura antes do título. Sugestão: centralizar (`.bib-img { margin: 0 auto }`) ou deixar o bib menor no mobile. Assim a banda não fica com cara de espaço sobrando.
- **[#27] Banda de fechamento (linha 244, `o1-rev-archer.jpg`):** a passagem da foto para o quase preto é seca, perto da linha 340. É limite do recorte provisório e se resolve com o original.
- **[#24] Hero a 375px:** o botão termina a cerca de 663px, dentro dos 667px, mas no limite. Se o texto crescer, reduzir `.o1-space` (linha 51).
- **[#18] G5:** o "Shop Now" do Bloco 2 saiu e isso não está registrado.
- **[#15] G1 (botão 18px / 3px), G2 (sem variante), G3 (rodapé).**

**OK:** 1 a 9, 10 (empilha com a imagem primeiro), 11, 12 (exceção aceita), 13 (depois da correção), 14 (v0.5 pendente), 16, 17 (a linha de pesca só no 01), 19, 20, 20b, 21, 22 (3 botões, um destino), 23 (6 bandas, uma de estrutura), 24, 25, 26, 27. Dark: tudo fixo escuro, correto no Apple Mail.

---

## 02 Youth · BLOQUEIA

**BLOQUEIO**
1. **[#13] Cores de painel fora do kit: `#774727` (ferrugem, linha 186) e `#4F5C5F` (ardósia, linha 210),** que também estão assadas em `o2-panel-hoodie.jpg` e `o2-panel-pant.jpg`. O kit v0.5 deixa essas duas cores como **pergunta em aberto ao responsável** ("Em aberto", e com outros valores: `#794928` e `#4F5B5E`). Hoje o HTML usa um terceiro par de valores, que não está nem no `tokens.json`.
   **Correção (depois da decisão do responsável):** (a) se ficam, registrar **um** hex de cada no `tokens.json` e no README (`color.panel_*`) e usar exatamente esse hex no `bgcolor` e no JPG (`compose_A.py`); ou (b) trocar pelos painéis do kit (Turkish Coffee `#5C5249` e Dusk `#ACB1B3`, ou Aluminum `#A39A8C`) e regerar os dois JPG.

**Corrigido nesta rodada:** `#E4DBB3` nos 6 contornos (cards e caixas, linhas 160, 166, 184, 190, 208 e 214), com a mesma troca do 01.

**WARN**
- **[#9] G6:** papel claro no Gmail dark. No Apple Mail a troca `dm-tex`, `dm-h`, `dm-p` e `dm-accent` funciona (COLD MORNING fica laranja sobre `#34353A`, texto grande).
- **[#15] G1, G2, G3.**
- **[#16]** A foto do hero continua sendo o recorte `crop-sent-sep15-camp-chairs-family` já usado em maio (WARN da r1).

**OK:** 1 a 12, 14, 16, 17, 18 (copy literal), 19 a 27. Renders 680 e 375 fiéis à rev-oct-02; cards empilham com o painel primeiro, e as quebras SMALLER / SIZES e COLD / MORNING cabem a 375.

---

## 03 Heavy Weight Hoodie · PASSA (rascunho)

**BLOQUEIOS:** nenhum.

**WARN**
- **[#27] Hero (linha 100, `o3-rev-hero.jpg`):** a parte "espelho desfocado" abaixo da linha 470 da foto aparece como uma faixa borrada com emenda horizontal atrás de YOUR / COLDEST (desktop, entre y 440 e 610; mobile, perto de y 400, cortando o COLDEST ao meio). É recorte provisório e se resolve com o original. Até lá, um degradê mais cedo para Tap Shoe esconderia a emenda.
- **[#9] Dark mode:** o painel Gunmetal (`#2A2B2D`) quase some sobre o papel camo escuro `#34353A` (mesmo WARN da r1, continua). Correção: no dark, dar ao painel Gunmetal um contorno `#45464A` ou escurecer o papel.
- **[#4]** 765 KB somando os gêmeos mobile e o papel `-dm` (o Gmail baixa imagem escondida): dentro dos 800 KB, mas perto.
- **[#6 / Outlook]** Linha 135: `v:fill type="frame"` estica o tile de camo na altura da banda (cerca de 1.250px), e as manchas ficam alongadas no Outlook. É aceitável (o `bgcolor` segura a leitura), mas conferir no Litmus.
- **[#15] G1 (hero com 56px de altura), G3, G4 (serifa em Arial no Outlook).**
- **[C5]** "handwarmer pockets" contra "hand pockets" na loja: copy do cliente, já está no brief.

**OK:** 1 a 5, 7, 8, 10, 11 a 14, 16 a 26, 27 (fora o hero). O camo claro corre sem emenda sob os rasgos PNG, e os painéis empilham com a imagem primeiro.

---

## 04 Crater Valley · BLOQUEIA

**BLOQUEIOS**
1. **[#1 / #10] A coluna tem 624px no desktop, não 600.** Medido por pixel no render 680: o e-mail inteiro vai de x 28 a 651. Achei a causa por eliminação de módulo: são os **cards de produto** (linhas 166, 200 e 234). A célula de texto tem `width:288px` mais `padding-right:41px` (329px), somada à foto de 240, ao contorno e aos 35+35 de margem. Além disso, `PERFORMANCE&nbsp;HOODIE` (linha 170) não quebra dentro da caixa. O Gmail e o Apple Mail mostram o e-mail mais largo que 600, com a borda direita cortada ou com rolagem lateral em janela estreita.
   **Correção testada numa cópia temporária** (voltou para 600, x 40 a 639, sem outra mudança de layout): nas linhas 166, 200 e 234, `width:288px; padding:0 41px 0 0;` vira `width:247px; padding:0 41px 0 0;`, e na linha 170 `PERFORMANCE&nbsp;HOODIE` vira `PERFORMANCE HOODIE` (o título quebra em "CRATER VALLEY PERFORMANCE / HOODIE"). Outra opção: título a 18px, mantendo o `&nbsp;`, e conferir de novo a medida.
2. **[#6 / Outlook] Banda do pôr do sol (linha 263): o espaço acima do texto é `padding-top:296px` na própria `<td>` que tem `mso-padding-alt:0px`.** No Outlook desktop esse padding zera, e FROM FIRST LIGHT TO / LAST CALL sobem para cima da foto: branco e laranja sobre o sol laranja e a silhueta, ilegível. O VML também tem `height:329px`, menor que a banda.
   **Correção:** tirar o `padding-top:296px` da `<td>` e pôr uma linha espaçadora dentro da tabela (`<tr><td class="o4-sun-space" height="296" style="height:296px; font-size:0; line-height:0;">&nbsp;</td></tr>`, com `.o4-sun-space { height:182px !important }` no mobile, no lugar do `.o4-sun`), como o 01 faz no fechamento (`o1-photo-space`). Acertar o `height` do `v:rect` para a altura real da banda.

**BLOQUEIO corrigido nesta rodada**
- ~~[#7] Os 3 botões pequenos (SHOP HOODIE / FLEECE / QUARTER ZIP, linhas 175, 209 e 243) tinham 40px de altura (12 + 16 + 12).~~ O padding passou de `12px 22px` para `14px 22px`, que é o valor do kit v0.5 (E27/E29, 44px). A revision-r2 fala em 12px, mas o kit já registrou a subida para os 44px mínimos. Re-render: o mobile cresceu 12px, e nada mais mudou.

**WARN**
- **[#4] 1.026 KB somando tudo o que o HTML referencia** (hero mobile de 88 KB mais as 3 fotos de card mobile, escondidas no desktop, que o Gmail baixa mesmo assim). O desktop claro fica em cerca de 731 KB. Correção sugerida: usar a mesma foto de card no desktop e no mobile (`width:100%`), o que tira cerca de 150 a 200 KB.
- **[#10] Descrição da caixa em 15px** (linhas 171, 205 e 239): o kit permite 15px em card, e o checklist pede 16px de corpo. Aceitável; subir para 16px se couber depois da correção 1.
- **[#22] 5 botões** (hero, 3 pequenos, fim), todos para a família Crater Valley. É o que a imagem pede e substitui o X5. Registrar no brief (G5).
- **[#25]** Preheader com 31 caracteres (texto do cliente, mantido).
- **[#15] G1, G3, G4.** O contorno em rgba cai para `#FEF4C6` cheio no Outlook, mais claro que na imagem (já está nas notas do B).

**OK:** 2, 3, 5, 8, 9 (tudo fixo escuro), 11, 12, 13, 14, 16 (sem rosto cortado nos olhos: a pendência da r1 resolvida), 17, 18 (X4 aplicado, nomes sem "Men's" como o brief pede, `¼` literal), 19 a 21, 23, 24 (hero a 375 com o botão em cerca de 500px), 25, 26, 27 (fora os bloqueios).

---

## 05 Shadow Series · PASSA (rascunho)

**BLOQUEIOS:** nenhum.

**WARN**
- **[#10] Descrição dos atributos em 14px `#E2DDD9`** (linhas 135, 141, 149 e 155). É o piso absoluto. Subir para 15px, se a quebra da imagem aguentar.
- **[#15] G2:** contorno das caixas e dos cards de atributo em `#FEF4C6` sólido (linhas 132, 138, 146, 152, 180, 199 e 218), enquanto 01, 02 e 04 usam 70%. Igualar.
- **[#23]** Duas bandas de estrutura (atributos e tabuleiro): a exceção ainda precisa do ok do responsável, com data, no brief (pendente desde a r1).
- **[#16]** A foto do hero não é a da revisão (exceção aceita); pedir o original do homem sentado.
- **[C3 / C5]** $69.98 promocional sem preço riscado (reconfirmar no dia 29/10). "Grid Fleece Interior" só existe no Mid Layer. A calça não é enviada para CA/NY.
- **[#15] G1 (18px, tracking 2,5 e 4px), G3, G4.**

**OK:** 1 a 9, 10 (tabuleiro empilha com a imagem primeiro, os 4 atributos em 1 coluna), 11 a 14, 16 a 22, 24 a 27. A banda de atributos e o tabuleiro batem com a rev-oct-05; o ® fica pequeno e sem quebra.

---

## Correções aplicadas por este QA

1. `01-cedar-branch-bibs.html` linhas 177 e 200 e `02-youth-season.html` linhas 160, 166, 184, 190, 208 e 214: `border:1px solid #E4DBB3;` virou `border:1px solid #FEF4C6; border-color:rgba(254,244,198,0.7);` (hex fora do kit trocado pelo token do kit, 70% como no 04 e na imagem).
2. `04-crater-valley.html` linhas 175, 209 e 243: botão pequeno com `padding:14px 22px` (antes 12px 22px), 44px de altura como no kit v0.5.

Nada mais foi editado. A correção do 624px do 04 foi testada numa cópia temporária, que já foi apagada, e fica para o Designer B.

## Pendente antes do envio (não bloqueia agora)

- Aprovação do kit v0.5 (E27 a E34, superfícies, mudanças globais) e das cores de painel do 02 e do 05.
- Rodapé do Omnisend com endereço físico e descadastro (CAN-SPAM), conferido num envio de teste.
- `{{CTA_URL}}` dos 5, `{{HOME_URL}}`, menu, `{{INSTAGRAM_URL}}`, com UTM; imagens no CDN com URL absoluta.
- Originais das fotos provisórias (arqueiro, menino, homem no capim, pôr do sol, hero do 05) e liberação das `orig-*` (C9) e da citação com nome (C6).
- Preços e variantes reconfirmados na data de cada envio (C3, C4, C8).
- Testes reais: Outlook 2016/365 (Litmus: VML, serifa, cantos, pôr do sol do 04), Gmail iOS/Android no dark (G6), Apple Mail.

## Precisa do responsável

- Cores dos painéis do 02 (ferrugem e ardósia): entram no kit, e com qual hex exato, ou saem.
- Um padrão único para a caixa de produto (G2) e para o botão (G1): aceitar o valor do kit v0.5 nos 5.
- Ok com data para as duas bandas de estrutura do 05 e registro das decisões da rodada 2 no brief (G5).
