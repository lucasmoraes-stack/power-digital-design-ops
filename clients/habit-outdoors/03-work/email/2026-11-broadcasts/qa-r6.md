# QA rodada 6 · 02 Gift Guide #1 (2026-10-08)

Email QA Reviewer. Escopo: só o 02, depois das duas mudanças da rodada 6 (`brief.md`: "Rodada 6 (feedback do Lucas, 2026-10-08)", colagem-pilha de 5 fotos e R8 nova; "Rodada 6 (02 cards)", banda de produtos sem cards em Patriot liso). Renders 680 / 375, claro e escuro, refeitos por mim. Rodadas anteriores: `qa-r2.md`, `qa-r4.md`.

**Veredito: 02 BLOCK.** São dois bloqueios de foto, os dois mecânicos e nenhum de conteúdo. O resto do e-mail chegou onde o Lucas pediu: a cara de catálogo sumiu, os recortes estão limpos e o R8 é respeitado.

## Base técnica

- `lint_layout.py`: OK em 600 e 375.
- Copy literal contra `copy-source.md`: **35/35** (headline, subheadline, copy, 6 títulos, 6 linhas, 7 CTAs e URLs). Preços **6/6** iguais a `products.json`. Zero travessão, zero hex fora do kit, zero `href="#"`.
- HTML 48,0 KB. Imagens no modo claro **643 KB** (gêmeos `-dm` à parte); nenhuma imagem acima de 150 KB (a colagem tem 136 KB), todas a 2x, nenhum PNG em paleta. As duas células texturizadas têm `bgcolor`, `mso-padding-alt:0px`, VML e `mso-fit-shape-to-text`.

## Contra o pedido

| Critério | Resultado |
|---|---|
| Cara de catálogo | **Some.** São 6 linhas alternadas, com recortes grandes direto no Patriot liso, sem card e sem painel. O bomber sangra pela esquerda, as botas são grandes e o gorro aparece no chão diante de uma foto de gente. Em 680 a seção lê como a do 05 e a de outubro |
| Recortes, inclusive vãos internos | **Limpos.** Sem aro nem caixa no zoom 2x: camisas, bomber (o vão entre manga e corpo é Patriot puro, medido 32/41/68 igual à banda), hoodie, botas, gorro |
| Sombras | **Coerentes.** A luz vem de cima à esquerda; camisas, bomber e hoodie têm só a sombra projetada, e botas e gorro têm sombra de contato justa |
| R8 (sem degradê) | **Respeitado.** A colagem sai do papel por rasgo, a foto do gorro é cópia rasgada e o cartão-presente fica numa moldura reta. Não há derretido em lugar nenhum |
| Rasgos e emendas, 680 e 375 | Bons: Patriot→papel, papel→rodapé e as bordas da foto do gorro. A colagem não tem degrau no topo. Ver o WARN 1 sobre a base da colagem |
| Celular | Cada linha empilha imagem e depois texto centralizado; nada estoura, botões a 44px. A linha do gorro mantém foto e gorro juntos. No escuro só o papel do fechamento troca, e certo |

## BLOCK

1. **Mesmo caçador, mesma cena, duas vezes no e-mail.** A foto nova da linha do gorro (`crop-sent-sep10-utv-hunter-standing`) mostra o homem de boné laranja e Realtree ao lado do UTV. É a mesma pessoa, no mesmo momento e no mesmo UTV da foto de cima à esquerda da colagem (`crop-sent-sep10-utv-hunters`). Em 680 as duas ficam a uma tela de distância e leem como imagem repetida, o que quebra a R10 no espírito e é o tipo de coisa "robótica" que o Lucas apontou. **Fix (escolher um):**
   - trocar a foto da linha do gorro por uma foto do banco (`photos/lifestyle/INDEX.md`) que não esteja em nenhum dos 5 e-mails de novembro;
   - ou trocar a foto do UTV da colagem por outra.
2. **Mancha clara estourada voltou na foto do blind** (colagem, embaixo à esquerda, canto inferior direito da foto). São cerca de 3.900 px quase brancos no render 680, um primeiro plano desfocado e claro ao lado da arma, visível em 680 e 375. É o bloqueio 7 da rodada 1, que tinha sido resolvido subindo o recorte. **Fix:** recortar a `crop-sent-sep2-hunter-blind` mais acima e à esquerda, como na rodada 2, ou deixar a moldura vizinha cobrir esse canto.

## WARN

1. **Base da colagem:** as fotos cobrem quase todo o rasgo papel→Patriot. Nos poucos pontos visíveis, nas bordas do e-mail e nos vãos entre fotos, a linha fica quase reta (y 914 a 919) e lê como corte, não como rasgo. Baixa; deixar alguns centímetros de rasgo à mostra numa borda, ou acentuar o recorte do papel.
2. **`crop-sent-sep22-wading-river`** tem 304 px de origem e aparece a cerca de 180 CSS: no zoom fica mais mole que as vizinhas. Aceitável no tamanho atual; não aumentar.
3. **Cartão-presente:** a foto de baixo do par (pescador de boné com o logo) vem da imagem da loja e ainda parece da mesma sessão do pescador da colagem (WARN antigo, baixo).
4. **Outlook desktop:** a cópia rasgada do gorro e a colagem são imagens comuns, sem risco. Confirmar em teste real a alternância de lados das linhas (tabela com `dir`).

## Fotos no lote (R10)

Conferi as referências do `compose_assets.py` contra o brief. Nenhum arquivo de foto aparece em dois e-mails de novembro:
- 01: `family-forest-walk`, `camp-chairs-family`
- 02: `utv-hunters`, `angler-tackle-box`, `wading-river`, `hunter-blind`, `trout-in-hand`, `utv-hunter-standing`, `truck-hunter`
- 03: `orig-hunt40`, `orig-hunt22`
- 04: `barn-door-feed-bag`, `stable-horse`
- 05: `orig-twofisted`, `orig-hunt50`

O único problema é o par da mesma cena dentro do 02 (bloqueio 1).

## Pendente / responsável

Continuam valendo as listas de `qa-r4.md`: placeholders e UTMs, rodapé do Omnisend, preços na data, liberação das fotos (inclusive `wading-river` e `utv-hunter-standing`), testes Outlook e Gmail, módulos novos para o kit e pontos do cliente ("inbox..", "top 5" com 6 produtos, 02 ainda "Needs Edit").

## Próximo passo

Email Designer corrige os bloqueios 1 e 2 no `compose_assets.py`, roda lint e os renders do 02; QA reconfere só esses dois pontos.

---

## Reconferência (2026-10-08, depois da nota "QA r6, 02" no brief)

Renders 680 / 375, claro e escuro, refeitos por mim. `lint_layout.py` OK em 600 e 375. Copy **35/35** contra `copy-source.md`, preços 6/6, zero travessão. Imagens do 02 no modo claro: 626 KB.

**Veredito: 02 PASS.**

| # | Conferência | Resultado |
|---|---|---|
| 1 | Foto da linha do gorro, agora `crop-sent-sep22-boat-anglers` | **Resolvido como bloqueio.** É uma cena diferente de tudo na colagem (barco, pesca de mosca, plano aberto horizontal), e a repetição de momento sumiu. **WARN alto:** o pescador da frente (camisa azul, boné marinho Habit, óculos escuros, barba) parece ser o mesmo modelo, com a mesma roupa, da foto de cima à direita da colagem (`sep22-angler-tackle-box`). Quem olha com atenção reconhece a pessoa, mas como ação e enquadramento são outros, lê como "a mesma sessão de fotos", não como imagem duplicada. Fica com o Lucas; se ele quiser zero repetição de pessoa, a troca é por uma foto do banco sem esse modelo |
| 2 | Mancha clara na foto do blind | **Corrigido.** O primeiro plano desfocado saiu do recorte e a luz da abertura do blind foi contida. No render só sobra o branco da moldura e o claro da janela, que é natural da foto |
| 3 | Rasgo da colagem para o Patriot | **Corrigido.** Nos trechos que aparecem nas bordas do e-mail o perfil agora é irregular, com mordidas visíveis, e lê como rasgo nas duas larguras e no escuro |

Os demais WARN e pendências desta rodada e de `qa-r4.md` continuam valendo. **02 liberado para o preview.**
