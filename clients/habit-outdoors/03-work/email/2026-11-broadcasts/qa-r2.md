# QA rodada 2 · November 2026 broadcasts (2026-10-07)

Email QA Reviewer, sobre a rodada 2 do Email Designer (`brief.md`, seção "Rodada 2 (QA r1)"). Renders refeitos nesta rodada (`renders/`, 680 e 375, claro e escuro), `lint_layout.py` **OK nos 5 em 600 e 375**, copy conferida string a string contra `copy-source.md` (**132/132 literais**: headline, subheadline, copy, nome, linha, CTA e URL de cada produto), preços **26/26 iguais a `products.json`** (inclusive $49.99 do Hybrid Hoodie e $111.98 promocional do Insulated Bib), nenhum travessão, nenhum hex fora do kit, nenhum `#` em href, placeholders só os nomeados. Conteúdo do cliente intacto, como mandado.

**Veredito:** 01 BLOCK · 02 BLOCK · 03 PASS · 04 PASS · 05 BLOCK. Os três bloqueios restantes são mecânicos (um script, uma altura de célula, uma regra de media query); nenhum pede mudança de conteúdo.

| E-mail | Veredito | HTML | Imagens (modo claro) | Com gêmeos `-dm` baixados |
|---|---|---|---|---|
| 01 | **BLOCK** | 40,2 KB | 751 KB | ~853 KB |
| 02 | **BLOCK** | 50,8 KB | 663 KB | ~799 KB |
| 03 | PASS | 40,1 KB | 593 KB | ~795 KB |
| 04 | PASS | 28,0 KB | 525 KB | ~621 KB |
| 05 | **BLOCK** | 68,4 KB | 945 KB no celular (807 KB no desktop, que não baixa `n5-hero-m.jpg`) | ~1.156 KB |

Nos totais "com gêmeos" descontei a textura `-dm` que o CSS de cada arquivo declara mas nenhum elemento usa (`tex-paper-camo-dm` em 01/02/03, `tex-paper-light-dm` em 04/05): cliente de e-mail não baixa fundo de regra sem elemento. Nenhuma imagem acima de 150 KB; todas a 2x ou mais do tamanho exibido (cards do 02 a 2,56x, por causa dos 327px do celular).

## Os 9 bloqueios da rodada 1

| # | Bloqueio r1 | Estado | Como conferi |
|---|---|---|---|
| 1 | 03 hero (faixa fantasma, PNG em paleta, manga cortada) | **Corrigido** | `n3-hero-model.jpg` 520x621 JPG sobre papel Tap Shoe; as duas mangas inteiras, mãos visíveis, ombros fundidos na banda (zoom 2x), pernas cortadas pelo rasgo; lint sem clip em 600 e 375 |
| 2 | 03 círculos só com camo | **Corrigido** | círculos fora; sistema `n3-system.jpg` + 4 rótulos vivos com filete laranja (desktop) e lista 2x2 (celular); frases exatas do copy |
| 3 | 03 E28 painéis a 258px, caixas encostadas | **Corrigido** | painéis medem 300x330 no render (x 40-340 e 340-640); caixa E27 de 250px com 24px de folga por lado |
| 4 | 01 fechamento com 3 molduras de tecido | **Corrigido no conteúdo** (as três peças de costas, reconhecíveis), **mas a imagem nova abriu um defeito de emenda**: ver bloqueio A abaixo |
| 5 | 02 cards 2-up desalinhados | **Parcial**: linhas 1 e 2 alinhadas (preço e botão na mesma altura nas duas colunas); **linha 3 ainda desalinha 20px**: ver bloqueio B |
| 6 | 02 cartão-presente (vazio, 110px no celular) | **Corrigido** | headline em largura total; cartão ao lado de subtítulo + copy + botão; celular com 32px entre cartão e texto |
| 7 | 02 colagem (mancha estourada, rasgo cortando 15px) | **Corrigido** | foto do blind recortada acima da mancha; as duas molduras de baixo terminam cerca de 30px acima do rasgo, inteiras (zoom 2x) |
| 8 | 05 hero (sem degradê, braços e rosto cortados) | **Corrigido** | degradê dentro da foto; no celular `n5-hero-m.jpg` com os dois rostos inteiros e bonés longe do logo; botão fecha dentro dos 667px (termina em ~655px) |
| 9 | 04 mosaico (fragmentos brancos, cavalo cortado) | **Corrigido** | `n4-m-stable.jpg` só com o homem, topo limpo (zoom 2x); prega das costas visível no tile |

## BLOCK (restantes, mais grave primeiro)

**A. 01 · emendas das duas composições sobre o grão Ivy (`n1-hero-group.jpg`, L128; `n1-closing-details.jpg`, L313)**
Medido no render 680 claro, em área sem peça: o hero termina em y=660 com degrau de **21 níveis** em toda a largura (dentro da imagem RGB 65/62/43, banda logo abaixo 86/83/64): a sombra de chão assada na imagem é cortada reta, e lê como uma linha horizontal atravessando o hero na primeira tela (zoom `renders`: linha visível em 680 e 375, claro e escuro). O fechamento repete o defeito: fundo da imagem 71/68/49 contra banda 86/83/64 (**15 níveis**) e o grão da imagem **5 a 7 níveis mais claro** que a banda (92/89/70 contra 85/82/63), com a borda direita visível em x=300: a imagem lê como um retângulo colado atrás das peças. O padrão do próprio kit para composição é desvio 0 a 1 na borda ("checagem de emenda" do `compose.py`); as outras composições deste lote cumprem (packshots do 01 sobre brown/tapshoe desvio 3 a 8; `n3-system` 7; cartão do 02 1 a 4).
*Fix (compose_assets.py, sem mexer em HTML):* nas duas imagens, fazer a sombra de chão voltar ao valor do tile nas últimas 30 a 40 linhas (ou terminar a imagem onde o chão já voltou ao grão) e gerar o grão da imagem a partir das mesmas linhas do tile `tex-grain-ivy.jpg`, sem deslocamento de tom (checar que a média das bordas fica a ≤1 nível da banda, como nos jobs antigos). Aproveitar e dar o mesmo tratamento à borda direita do fechamento. Regerar e reconferir o render.

**B. 02 · cards 2-up, linha 3 (L274-315)**
O título "MEN'S 800GRAM INSULATED 15" WATERPROOF RUBBER BOOTS" cabe em **4 linhas** a 258px, e a célula `.ct` está fixa em `height="60"` (3 linhas de 20px): a célula cresce 20px e o preço e o botão da coluna esquerda ficam **20px abaixo** dos da direita ($89.99 em y=2852 contra $12.99 em y=2832; SHOP BOOTS contra SHOP NOW idem). Linhas 1 e 2 estão certas.
*Fix:* `height="80"` / `height:80px` na célula `.ct` dos 6 cards (4 linhas, o máximo da grade), ou pelo menos nos dois cards da linha 3. Celular continua `height:auto`.

**C. 05 · título laranja a 17px sobre a retícula Major Brown no celular (CSS L70, faixa UNDER $30, L174/195/216/237)**
A regra `.row-txt .ititle { font-size:17px !important }` vale para as três faixas. O kit v0.5 manda **19px obrigatório** para o título laranja sobre Major Brown e retícula (3,1:1 no pior caso; só passa como texto grande, e 17px 800 não é texto grande). As faixas UNDER $100 (Tap Shoe) e UNDER $120 (Patriot) passam em qualquer tamanho; a UNDER $30 reprova no celular.
*Fix:* limitar o override de 17px às faixas Tap Shoe e Patriot (classe própria na faixa da retícula, ou simplesmente manter 19px nas três: a coluna de texto do celular aguenta, só quebra uma linha a mais no "SIESTA CAPE LONG SLEEVE PERFORMANCE TEE").

## WARN (corrigir, não bloqueiam)

- **05 · peso acima do teto de ~800 KB do kit.** Não é bloqueio técnico: o teto do kit é orientação ("~800KB"), não há limite duro de cliente, o HTML tem 68 KB e nenhuma imagem passa de 150 KB. **Decisão do responsável**, com o custo claro: no celular em rede móvel o e-mail baixa 945 KB (1.156 KB nos clientes que baixam os gêmeos escuros). Três cortes mecânicos que o QA recomenda, nesta ordem: (1) `n5-hero-m.jpg` está em 1200x2300 para 375x719 CSS (3,2x); em 750x1438 (2x) cai de 138 para cerca de 70 KB; (2) faixa UNDER $100 em Tap Shoe liso `#2A2B2D` (superfície do kit, a mesma do rodapé) em vez de `tex-paper-tapshoe.jpg`: menos 87 KB; (3) `n5-closing-oaks.jpg` recomprimida para cerca de 75 KB. (1)+(2) deixam o celular em cerca de 790 KB sem tirar produto nem textura de faixa visível.
- **02, 03 e 05 · título laranja sobre a textura `tex-grain-patriot-water`** (cards do 02 a 17px, caixas E28 do 03 a 19px, faixa UNDER $120 do 05 a 19px/17px). A tabela de texturas do kit diz "laranja só com 24px ou mais" nessa textura (4,0 no pior caso, percentil 1), mas o próprio E28 do kit (rev-oct-05 do responsável) põe a caixa E27 laranja sobre Patriot com água. Registrar a exceção no kit como a do botão, ou subir para o Patriot liso; não bloqueio porque é decisão já tomada no kit.
- **03 · celular, recorte do modelo alinhado à direita** (L136, `margin:0 0 0 auto`): na coluna de 375px sobram 115px vazios à esquerda da figura de 260px. Centralizar (`class="mc"`, como no fechamento do 01) ou levar a 100%. Baixa.
- **03 · rótulos no celular** viram lista 2x2 sem apontar para nada (filete decorativo em cima de cada um). Aceitável; só registro para o responsável saber que o "callout" só existe no desktop.
- **04 · tiles da prega e do bolso** continuam com o fundo cinza do packshot (desvio 65 a 108 contra a retícula); a prega agora aparece (aviso r1 atendido na metade). Leem como tiles de foto de produto; aceitável.
- **Regras de dark mode sem uso** (`.dm-tex-camo` em 01/02/03, `.dm-tex` em 04/05): inofensivas, só limpeza. Comentário do topo de cada HTML contém o texto `[[CONFIRMAR]]` (aponta para o brief): tirar o comentário na exportação, senão o lint de arquivo final acusa.
- **Comprimento no celular:** 02 com 5.453px e 05 com 5.549px (6 cards em 1 coluna; 11 linhas). Já aceito na r1; fica o registro.
- **Dark mode no app do Gmail** (texto escuro sobre papel claro e camo: 01 banda 2, 02 fechamento, 03 banda 2, 04 hero, 05 fechamento): só teste real resolve; Apple Mail/Outlook app estão certos nos renders escuros (texturas e rasgos trocam, logo do 04 vira branco).

## OK

1 (600px, fluido, tabela fantasma), 2 (só tabela; nada de flex/JS/SVG), 3 (inline; dark logo escondido inline no 04), 4 (HTML 28 a 68 KB; imagens ≤150 KB; 01 a 04 abaixo de ~800 KB no modo claro), 5 (todo `<img>` com width, display:block, border:0, alt), 6 (as 19 células texturizadas com `bgcolor`, `mso-padding-alt:0px`, VML `v:fill` e `mso-fit-shape-to-text:true`; hero do 05 com frame de 840px), 7 (botão td + a, 52px hero / 44px card, placeholders nomeados), 8 (preheader + espaçador nos 5), 9 (meta tags, swap de logo, sem plano #000/#FFF), 10 (tudo empilha a 375px sem overflow; headline ≥60px; corpo 16px no celular), 11 (sem merge field, decisão do kit), 13 (zero hex fora do `tokens.json`), 15 (Prompt + Playfair com pilha inline e fallback MSO Arial/Georgia), 16 (banco aprovado + imagens da loja; liberações pendentes abaixo), 17 (cinco heroes diferentes: grupo de produto, colagem, dividido com recorte, foto emoldurada, foto em tela cheia), 18 (copy literal, 132/132), 19 (nenhum dado inventado; `[[CONFIRMAR]]` só no comentário), 20 (marca não regulada; claims vêm do copy do cliente e da ficha da loja), 20b (ICP e mensagem-chave por e-mail como no brief; frase-âncora não usada; sem urgência nem número sem fonte), 21 (sem travessão, antítese ou emoji no corpo; emoji só nos assuntos aprovados pelo cliente, ponto 14 do brief), 22 (um formato e uma cor de botão nos 5), 24 (hero converte na primeira tela de 375px nos 5: botão termina em 610 / 410 / 460 / 640 / 655px), 25 (assuntos 25 a 32 caracteres; preheaders estendem), 26 (caixa-alta real em headline, título e botão; sem "elevate/unlock"; sem exclamação).

Itens 12 e 23 ficam em "Pendente" e "Precisa do responsável".

## Pendente antes do envio (não bloqueia agora)

- Placeholders: 01 `{{WOMENS_URL}}`, `{{WOMENS_COLLECTION_URL}}`; 02 `{{GIFT_GUIDE_URL}}`; 03 `{{BUCK_HOLLOW_URL}}`; 04 `{{FLANNEL_URL}}`; 05 `{{CTA_URL}}`; nos 5 `{{HOME_URL}}`, `{{MENS_URL}}`, `{{WOMENS_URL}}`, `{{YOUTH_URL}}`, `{{SALE_URL}}`, `{{INSTAGRAM_URL}}`. UTMs.
- Rodapé legal (item 12): endereço físico e descadastro vêm do rodapé do Omnisend por decisão do kit; conferir num envio de teste (CAN-SPAM) antes do primeiro disparo (5/11).
- Preços e variantes reconfirmados em cada data (5, 10, 19, 27, 30/11); o $111.98 do Insulated Bib é promocional (de $159.99) e sai da faixa "under $120" se a promoção acabar.
- Teste real: Outlook desktop (VML das 19 células, fonte Georgia na serifa) e Gmail iOS/Android (dark mode sobre papel claro e camo).
- Exportação: imagens para URL absoluta, comentário do topo removido.

## Precisa do responsável / cliente

1. **05 acima do teto de peso** (945 KB no celular): aceitar como está ou aplicar os cortes (1) e (2) do WARN acima.
2. **Kit v0.5** aprovado como régua do lote, e as **variantes novas** para o kit: grupo de produtos no hero (01), colagem como hero (02), hero dividido com recorte (03), **sistema com rótulos e filetes** (03, substitui os círculos do brief), mosaico reto (04), card vertical 2-up (02).
3. **Título laranja sobre Patriot com água** a 17 a 19px (02, 03, 05): registrar como exceção do kit, como o botão.
4. **Contagem de bandas** (item 23): 05 com as três faixas de preço como uma estrutura só; 01 com a pilha de produtos em três superfícies; 03 com sistema + E28 na mesma banda. Nenhum tem exceção datada no brief ainda.
5. **01 hero de estúdio** (não há foto de uso feminina no banco) e **Violet Dusk** fora do kit: aceitar Ivy Green ou buscar foto/cor.
6. **Liberação de fotos:** recortes `crop-sent-*` (celeiro, estábulo, UTV, caixa de iscas, blind, truta), `orig-twofisted-utv-two-men.jpg` (hero do 05) e `orig-hunt50-hunter-oaks-autumn.jpg` (fechamento do 05); fotos de detalhe originais do Buck Hollow, se existirem.
7. **Pontos do cliente** (brief, lista "Pontos para o cliente", 17 itens): principalmente o CTA "Shop Flannel" no hero do 05, o Hybrid Hoodie a $49.99 na faixa "under $30", a subheadline do 04 igual à do 03, o "inbox.." do 02 e os emojis nos assuntos. Entram como vieram, por decisão do responsável; o cliente ainda pode editar 02 e 05 ("Needs Edit").

## Próximo passo

Email Designer aplica A, B e C (mais os cortes de peso do 05, se o responsável aprovar), roda `lint_layout.py` e os renders de novo; QA confere só os três pontos (emendas do 01 medidas no render, linha 3 do 02, faixa UNDER $30 do 05 no celular) e libera o preview em Artifact para o Lucas.

---

## Rodada 3 · reconferência (2026-10-07)

Email QA Reviewer, sobre a rodada 3 (`brief.md`, "Rodada 3 (QA r2)"). Escopo: só os bloqueios A, B e C, mais lint, diff literal e o hero do 05 no celular. Renders 680/375 claros refeitos por mim antes de medir.

**Veredito: 01 PASS · 02 PASS · 03 PASS · 04 PASS · 05 PASS.** Nenhum bloqueio restante.

| # | Conferência | Resultado |
|---|---|---|
| A | 01 · emendas de `n1-hero-group.jpg` e `n1-closing-details.jpg` (render 680, tiras sem peça e sem texto) | **Corrigido.** Hero: degrau 0,3 no topo e 1,1 na base (era 21). Fechamento: 1,4 na borda direita e 0,9 na base (era 15). Zoom 2x: nenhuma linha reta nem retângulo atrás das peças. O miolo da imagem do fechamento continua 5 a 8 níveis mais claro que a banda (poça de luz atrás das peças, por desenho); como agora morre no tile antes da borda, não lê como emenda |
| B | 02 · cards 2-up, linha 3 | **Corrigido.** `.ct` com `height="80"` nos 6 cards; no render 680 os preços ficam em y 1811 / 2346 / 2880 e os botões em 1851 / 2386 / 2920 nas duas colunas (as três linhas alinhadas, zoom conferido). Celular segue `height:auto` |
| C | 05 · título laranja sobre a retícula no celular | **Corrigido.** Override de 17px agora só em `.t-under100 .ititle, .t-under120 .ititle` (CSS L70); `font-size` computado no Chrome a 375px: os 4 títulos do UNDER $30 a **19px**, UNDER $100 e UNDER $120 a 17px (Tap Shoe e Patriot passam em qualquer tamanho) |
| | `lint_layout.py` | OK nos 5, em 600 e 375 |
| | Diff literal contra `copy-source.md` | 132/132 (21 / 35 / 14 / 8 / 54); zero travessão; zero hex fora do kit; HTML 40,2 / 50,8 / 40,1 / 28,0 / 68,5 KB |
| | 05 · hero do celular `n5-hero-m.jpg` | 750x1438, 86,6 KB (era 1200x2300, 137,7 KB): exatamente 2x dos 375x719 CSS, mesmo padrão dos outros assets; no render a 375 os dois rostos e o logo continuam nítidos, sem serrilhado nos bonés nem no logo |

**Peso do 05 depois do corte 1:** cerca de 894 KB no celular no modo claro (807 no desktop, ~1.192 com gêmeos `-dm`). Continua acima dos ~800 KB de orientação do kit; o corte 2 (faixa UNDER $100 em Tap Shoe liso, menos 87 KB) não foi aplicado e **fica como decisão do responsável**, não bloqueia.

Os WARN da rodada 2 não tocados (recorte do 03 à direita no celular, tiles cinza do 04, regras dark sem uso, laranja sobre Patriot com água, comentário do topo) seguem como registrados: nenhum bloqueia. Lista "Pendente antes do envio" e "Precisa do responsável / cliente" da rodada 2 continuam valendo.

**Liberado para o preview em Artifact para o Lucas.**
