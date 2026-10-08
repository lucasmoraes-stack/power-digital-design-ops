# QA rodada 4 · November 2026 broadcasts (2026-10-07)

Email QA Reviewer, sobre a rodada 4 do Email Designer (`brief.md`, "Rodada 4"), julgada primeiro contra a revisão do Lucas: faltam pessoas, seções "certinhas" de catálogo, sombras erradas, recorte com fundo de estúdio sujando a textura, produto pequeno e centralizado; régua = outubro (`../2026-10-broadcasts/`, `email-kit/references/rev-oct-*.png`). Renders refeitos por mim (680 e 375, claro e escuro). Rodadas anteriores em `qa-r2.md`.

**Veredito: 01 PASS · 02 PASS · 03 BLOCK · 04 BLOCK · 05 BLOCK.** O salto em relação à rodada 3 é grande: produto grande, sangrando e atravessando o rasgo em 01, 03, 04 e 05, recortes limpos, foto de gente em todo e-mail. O que sobra são quatro defeitos pontuais, todos de imagem ou superfície, nenhum de conteúdo.

## Base técnica (sem achados)

- `lint_layout.py`: OK nos 5 em 600 e 375.
- Copy literal contra `copy-source.md`: **132/132** (21 / 35 / 14 / 8 / 54). Preços: **26/26** iguais a `products.json` ($49.99 do Hybrid Hoodie e $111.98 promocional incluídos). Zero travessão, zero hex fora do kit, zero `href="#"`.
- HTML 42,8 / 51,5 / 36,4 / 29,7 / 67,4 KB. Nenhuma imagem acima de 150 KB, nenhuma abaixo de 2x, nenhum PNG em paleta. Toda célula com imagem de fundo tem `bgcolor`, `mso-padding-alt:0px`, `v:fill` e `mso-fit-shape-to-text:true`.
- Imagens no modo claro: 764 / 727 / 626 (+76 só celular) / 640 / **843** KB (05 no desktop; ~781 no celular).

## Contra a revisão do Lucas

| Critério | 01 | 02 | 03 | 04 | 05 |
|---|---|---|---|---|---|
| (1) duas imagens fortes de gente, sem repetir no lote | sim: família na mata (hero), mulher na cadeira (fechamento) | sim: colagem (3 com gente), caçador no carro (fechamento); gorro no modelo é foto de estúdio | **não**: só o hero é forte; o segundo "humano" é o tronco sem cabeça do modelo da loja em painel de estúdio | sim: celeiro, estábulo | sim: UTV, caçador nos carvalhos |
| (2) seção de catálogo (produto pequeno no vazio) | não; pilha agora grande e alternada | os 6 cards continuam grade, mas produto grande saindo do painel (padrão Oct 13); aceitável para gift guide | **E28**: calça pequena num painel cinza chapado de 300x330 é exatamente o "catálogo" | não | rain bib (UNDER $100) e luvas pequenas no vazio; o resto bom |
| (3) recorte limpo, sombra crível, uma luz | ok | ok (sombra suave à direita) | ok | **franja branca** na camisa verde | **manchas de sombra soltas** sob o bomber |
| (4) produto atravessando o rasgo, 680 e 375 | parka e Sherpa: intencionais nas duas larguras, sem emenda, sem colisão | n/a | capuz no rasgo: ok nas duas | gola verde no rasgo: ok nas duas | líderes $100 e $120: ok nas duas |
| (5) chega na régua de outubro | sim | sim | quase (E28) | sim, fora o defeito | sim, fora o defeito |

## BLOCK (mais grave primeiro)

1. **04 · duas bandas vizinhas da mesma cor (banda do par de camisas → rodapé).** A banda nova do par está em papel Tap Shoe e o rodapé é Tap Shoe liso: medido 41/42/46 contra 42/43/45; o rasgo entre as duas quase não aparece (zoom 2x) e a banda do par se funde no rodapé. Checklist item 23 / rules §5 ("nunca duas bandas vizinhas da mesma cor"). *Fix:* trocar a superfície da banda do par por uma do kit que não seja marrom (a de cima é a retícula): Patriot liso `#202944` ou `tex-grain-patriot-water` (caixa E27 laranja sobre Patriot já é o padrão do E28), regerando o rasgo retícula→Patriot e Patriot→rodapé e o assado do par.
2. **04 · franja branca no recorte da camisa verde** (`n4` par, banda do par): 160 px quase brancos (RGB > 215) numa faixa vertical de x 175-224, y 1907-2005 no render 680, entre a manga esquerda e o corpo: é o fundo de estúdio que ficou preso no vão entre braço e tronco (o `clean_cut` só limpa a borda externa). Visível a olho nu em 680 e em 375. É o defeito que o Lucas apontou. *Fix:* no `clean_cut`, tratar também os buracos internos do alfa (região clara fechada entre braço e corpo) como fundo; regerar e conferir com zoom.
3. **05 · manchas de sombra soltas sob o bomber líder (UNDER $100).** Três manchas escuras separadas (nível 21 a 26 contra banda 43) em y 2440-2445 no render 680, uns 15 px abaixo da barra, e na mesma posição a 375: lê como "— — —" flutuando, não como sombra de contato. O próprio brief diz "nenhuma sombra de chão para peça que sangra pela borda", e o bomber sangra pela esquerda. *Fix:* tirar a sombra de contato dessa peça (ou uma elipse única, justa, colada na barra). Conferir as outras peças que sangram (parka do 01, camisa marrom do 04): nelas não há mancha.
4. **03 · E28 e segunda imagem de gente.** A banda E28 é a única seção do lote que ainda lê como catálogo: calça pequena num painel cinza chapado e jaqueta num retângulo de estúdio com mãos e sem cabeça. E o 03 fica com uma única imagem forte de gente (o hero), contra o pedido explícito do Lucas. *Fix (escolher um):* (a) trocar o painel da jaqueta por uma foto de uso do banco ainda não usada no lote, como `orig-hunt22-three-hunters-field-sunrise.jpg` (já preparada no kit para o E33) ou `crop-sent-sep2-hunter-blind.jpg`, e a calça grande sangrando pelo painel como nas outras bandas; ou (b) refazer o E28 no padrão do 05 (recortes grandes sobre a superfície, alternando, sem painel) e pôr uma faixa de foto de uso entre o sistema e os produtos. Sem mudar texto.

## WARN (não bloqueiam)

- **05 · peso no desktop: 843 KB, decisão do responsável, não bloqueio.** Mesmo critério das rodadas anteriores: ~800 KB é orientação do kit, HTML 67 KB, nenhuma imagem acima de 150 KB; o celular baixa ~781 KB. Se o Lucas quiser abaixo de 800: faixa UNDER $100 em Tap Shoe liso (menos ~87 KB).
- **05 · rain bib e luvas pequenos** (o bib ocupa uns 50 px de largura a 680): subir para a escala dos vizinhos; o padrão "produto grande" vale para a lista toda.
- **01 · hero de um e-mail Women's puxado pelo homem no centro** (família de costas; a mulher é a da direita). Não há foto feminina melhor no banco; fechamento compensa. Registro para o Lucas.
- **02 · gorro em close de estúdio** (rosto sorrindo para a câmera sobre painel ferrugem): é a única imagem "de passarela" do lote (red flag 5 do Strategy Report). Aceitável num card; alternativa é o gorro só como produto. Decisão do responsável.
- **02 · cartão-presente da loja** mostra um pescador de boné e camisa azul que parece da mesma sessão do pescador da colagem do hero. Baixa.
- **03 · celular:** faixa de ~70 px de Tap Shoe vazio entre a foto do hero e o rasgo. Baixa.
- **Outlook desktop:** (a) as peças `~t` do rasgo na coluna de texto (01, 03, 04, 05) dependem da fase do tile do VML; pode haver degrau de 1 a 2 px; (b) as linhas em zigue-zague do 05 usam `dir="rtl"` na tabela; Outlook respeita, mas confirmar; (c) serifa cai em Georgia. Só teste real.
- **Gmail app dark mode:** texto escuro sobre papel claro e camo (01 banda 2, 02 fechamento, 03 sistema, 04 hero, 05 fechamento): teste real.

## OK (itens do checklist)

1, 2, 3, 4 (fora o peso do 05, decisão), 5, 6, 7, 8, 9, 10, 11, 13, 15, 16 (liberações pendentes abaixo), 17, 18, 19, 20, 20b, 21, 22, 24, 25, 26. Item 23 bloqueado no 04 (bandas vizinhas); contagem de bandas do 01 e do 05 segue como decisão do responsável (ver `qa-r2.md`). Item 12 em "Pendente".

## Pendente antes do envio

Placeholders e UTMs (`{{WOMENS_URL}}`, `{{WOMENS_COLLECTION_URL}}`, `{{GIFT_GUIDE_URL}}`, `{{BUCK_HOLLOW_URL}}`, `{{FLANNEL_URL}}`, `{{CTA_URL}}`, menu, `{{HOME_URL}}`, `{{INSTAGRAM_URL}}`); rodapé do Omnisend com endereço e descadastro conferido em envio de teste (CAN-SPAM); preços reconfirmados em cada data (sobretudo o $111.98 promocional); testes Outlook desktop e Gmail iOS/Android; URLs absolutas e comentário do topo removido na exportação.

## Precisa do responsável / cliente

1. Peso do 05 no desktop (843 KB): aceitar ou cortar a textura da faixa UNDER $100.
2. 03: qual saída para o E28 (foto de uso no painel ou E28 no padrão do 05 + faixa de foto).
3. Gorro em close de estúdio no 02; hero do 01 com o homem no centro.
4. Liberação de fotos: `crop-sent-*` (inclusive `sep15-family-forest-walk`, `sep15-camp-chairs-family`, `sep10-truck-hunter`), `orig-twofisted`, `orig-hunt40`, `orig-hunt50`, fotos de modelo da loja (gorro, jaqueta Buck Hollow).
5. Módulos novos para o kit: linha de destaque com produto atravessando o rasgo, card com produto saindo do painel, hero dividido com foto sangrando, mais as variantes já listadas em `qa-r2.md`.
6. Os pontos do cliente do brief (CTA "Shop Flannel" no 05, hoodie $49.99 em "under $30", subheadline do 04, "inbox..", emojis), como vieram.

## Próximo passo

Email Designer corrige 1 a 4 (superfície da banda do par e franja no 04, sombra do bomber no 05, E28 do 03) e, se quiser, os produtos pequenos do 05; roda lint e renders; QA reconfere só esses pontos.

---

## Rodada 5 · reconferência (2026-10-07)

Email QA Reviewer, sobre a rodada 5 (`brief.md`, "Rodada 5 (QA r4)"). Escopo: os quatro bloqueios da rodada 4, os dois extras do 05, o R14 do 03, lint e diff literal. Renders 680 / 375, claro e escuro, refeitos por mim antes de medir.

**Veredito: 01 PASS · 02 PASS · 03 PASS · 04 PASS · 05 PASS.** Nenhum bloqueio restante.

| # | Conferência | Resultado |
|---|---|---|
| 1 | 04 · banda do par contra o rodapé | **Corrigido.** Banda em `tex-grain-patriot-water`, medida 36/45/76 contra rodapé 42/43/45; o rasgo Patriot→rodapé lê claro em 680 e 375 (zoom 2x); o rasgo retícula→Patriot dentro do par também. Claro e escuro iguais (bandas escuras fixas) |
| 2 | 04 · franja branca na camisa verde | **Corrigido.** Na área da rodada 4 sobram 24 px quase brancos (eram 160), em costura e botão da xadrez; zoom 1,4x limpo entre manga e corpo. Conferidos por amostra os outros recortes (bota, gorro, Breaking Dawn, hoodie Summit, Angler's Bluff com estampa branca, jaqueta e calça Buck Hollow): sem aro, sem caixa cinza |
| 3 | 05 · manchas sob o bomber | **Corrigido.** Abaixo da barra o mínimo da linha vai de 24 a 38, igual ao grão do Tap Shoe; sem as manchas soltas nas duas larguras |
| 4 | 03 · banda de produtos e segunda foto de gente | **Corrigido.** Faixa em largura total `orig-hunt22` (três caçadores subindo o campo) com rasgo do papel em cima e degradê para o Patriot embaixo; jaqueta e calça grandes, cortadas pela borda, alternando com as caixas E27. Nada de painel de estúdio. O 03 agora tem duas imagens fortes de gente. Escuro: a faixa e o rasgo trocam certo (gêmeo `-dm`) |
| | 03 · vazio sob o hero no celular | **Corrigido.** A foto vai até a borda e o capuz do sistema encosta nela; sobra só o fade |
| | 05 · extras (rain bib, Insulated Bib, luvas) | **Atendido.** Os três na escala dos vizinhos a 680 e 375 |
| | `lint_layout.py` | OK nos 5, em 600 e 375 |
| | Diff literal / preços | 132/132 contra `copy-source.md`; 26/26 preços iguais a `products.json`; zero travessão; zero hex fora do kit; HTML 42,8 / 51,5 / 37,4 / 29,8 / 67,4 KB |

**R14 no 03 (sistema 108 KB + faixa 108 KB além do hero): decisão do responsável, não bloqueio.** O motivo da regra é o teto de ~800 KB, e o 03 fica em 754 KB no modo claro, 3 texturas (limite 4), nenhuma imagem acima de 150 KB. A regra é do kit e está violada por 16 KB no total, então fica registrada; o conserto é mecânico e o QA recomenda fazer antes do envio sem precisar de decisão: recomprimir `n3-strip.jpg` e `n3-sys.jpg` para abaixo de 100 KB cada (q menor ou leve suavização a 2x, como no E30 do kit).

**Peso do 05:** 871 KB no desktop (~809 no celular) depois dos bibs e luvas maiores. Continua **decisão do responsável**: o corte que sobra é a faixa UNDER $100 em Tap Shoe liso (menos ~87 KB, fica abaixo de 800).

**WARN novos (baixos):**
- 03 · farelos escuros de ~1,5 px ao longo do rasgo no topo da faixa de foto (contra as copas): visíveis só com zoom; trocar por farelo claro de papel, como nos outros rasgos.
- 03 · `orig-hunt22` não repete em novembro, mas foi o hero do e-mail de 6/10 (outubro): quem recebe os dois vê a mesma foto com um mês de diferença. Registro para o Lucas.

Os outros WARN, a lista "Pendente antes do envio" e a "Precisa do responsável / cliente" da rodada 4 continuam valendo (peso do 05, gorro em close no 02, hero do 01, liberação das fotos, módulos novos para o kit, pontos do cliente).

**Liberado para o preview em Artifact para o Lucas.**
