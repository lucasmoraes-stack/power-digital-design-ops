# Habit Outdoors · Email kit

> Kit criado em 2026-09-24 com `build_kit.py --init`. **Etapa 1 em andamento**: v0.2.1 aprovado; v0.3, v0.4, v0.5 (2026-09-25) e **v0.6 (rascunho adicionado em 2026-10-07, aprendizados do lote de novembro)** aguardam revisão módulo a módulo; a v0.6 aguarda aprovação junto com a v0.5. Fluxo: `email-ops/playbook.md` · Regras: `email-ops/rules.md` · Checklist: `email-ops/CHECKLIST.md`, parte C.

## Status

| | |
|---|---|
| Status | **aprovado v0.2** em 2026-09-24 pelo responsável (módulos E01 a E18), com os ajustes **v0.2.1** do QA (E15, E17). **Em rascunho, aguardando aprovação:** v0.3 E19 a E23 (módulos rústicos Duck Camp) e **v0.4 E24 a E26 + conjunto de texturas + bordas E18 texturizadas** (rodada 2, `03-work/email/2026-broadcasts/art-direction-r2.md`) e **v0.5 (2026-09-25): mudanças globais em todos os módulos + E27 a E34 + 3 superfícies**, a partir dos e-mails de outubro revisados pelo responsável (`references/rev-oct-01..05-*.png`, `03-work/email/2026-10-broadcasts/revision-r2.md`); não usar em e-mail de envio antes de aprovados. **v0.6 (rascunho adicionado em 2026-10-07, pendente de aprovação junto com a v0.5): E35 a E41 + bloco "Production rules learned (v0.6)"**, a partir do lote de novembro (`03-work/email/2026-11-broadcasts/`, QA r1 a r3). **Atenção:** as mudanças globais da v0.5 (botão, fonte do corpo, headline) já estão aplicadas também nos módulos aprovados E01 a E18; se a v0.5 for recusada, voltar pelo git (commit bd51089) |
| Responsável pelo projeto | Lucas Moraes [[CONFIRMAR]] |
| Fonte visual oficial | Brand Identity Guide PDF (atualização 2026-02-04), resumo em `clients/habit-outdoors/01-brand/identity/brand-guidelines.md` |
| Oficial ou extraído | cor e tipografia **oficiais** (PDF); HEX **amostrado** do vetor do PDF, aguardando aprovação; valores do site são **extraídos** |
| ESP | Omnisend (detectado no site, [[CONFIRMAR]]) · merge: [[CONFIRMAR: sintaxe de first_name com fallback no Omnisend]] |
| Destino da entrega | HTML do kit → cópia editável no Figma (playbook etapa 7, `generate_figma_design`); o responsável finaliza tipografia e detalhes no Figma e exporta de lá |
| Idioma do conteúdo | inglês, mercado dos EUA |
| Página de revisão do kit | **Design System: https://claude.ai/code/artifact/f33018ee-a734-4183-83d0-79d046c9c60d** (gerada por `tools/build_ds_page.py` → `design-system.html`) · antiga: https://claude.ai/artifact/NaEqLoLezs7y5EvUeJRFBf (v0.2) · teste de fonte: https://claude.ai/artifact/5gRnMYHKZAHUCKPneuPXpo |

## Precedência das fontes nesta marca (decisão do responsável, 2026-09-24)

**Os e-mails enviados recentemente (`references/`) são a fonte da verdade das informações da marca**: cor em uso, rodapé, menu, tratamento do logo, caixa de texto, botão, linguagem. Quando divergem do Brand Identity Guide ou do site, vale o e-mail. O guia entra onde os e-mails não dizem nada (tecnologias, voz, fotografia, história). Continuam acima de tudo: régua legal (CAN-SPAM: endereço e descadastro) e contraste AA (rules §2).


## Aprendizados de novembro (v0.6)

Tirados do lote de novembro de 2026 (`03-work/email/2026-11-broadcasts/`: `brief.md` rodadas 2 e 3, `qa-r1.md`, `qa-r2.md`). São regras de produção, não decisões de visual do responsável: valem para todo módulo, antigo ou novo, e para todo e-mail montado com este kit. O mesmo texto, em inglês, está no bloco "Production rules learned (v0.6)" logo depois da KIT SHEET no `components.html`.

1. **Emenda de composição (R1).** Toda composição assada sobre o tile de uma banda (grupo de produto, recorte, sistema, colagem) começa na linha e coluna do tile em que fica no layout de 600px, **medidas no Chrome** (o hero do 01 estava em 251, não 235), e toda luz assada (poça de luz, chão escurecido, sombra de chão, sombra de rasgo) é multiplicada por uma janela que **chega a zero nos últimos 40px de cada borda** (`border_window` do `compose_assets.py`): a borda da imagem é o tile intacto. Medir, não olhar: `seam_check` (borda do arquivo contra o tile) e degrau no render de 680 em faixas sem produto e sem texto, **os dois até 1,5 nível**. O 01 passou com uma linha de 21 níveis atravessando o hero antes desta regra.
2. **Título de produto (R2).** As duas últimas palavras de todo título de produto ficam presas (`&nbsp;` ou `<span style="white-space:nowrap">`), em card, caixa E27, linha e pilha, desktop e celular. Headline segue a regra das rules (sem viúva); palavra serifada que ficaria sozinha vai em par de linhas (SIT / ALL&nbsp;DAY).
3. **Cards 2-up (R3).** Célula de título com **altura fixa** = o título mais longo da grade (80px = 4 linhas de 20px; 60px quebrou a linha 3 em novembro), célula de descrição fixa (84px = 4 linhas de 21px), preço + botão numa terceira célula `valign="bottom"`: preço e botão alinhados entre as duas colunas em toda linha. No celular as alturas são liberadas (`height:auto`). Conferir o título mais longo a 258px antes de escolher a altura (E40).
4. **Laranja sobre Major Brown (R4).** Título laranja sobre Major Brown ou retícula fica em **19px 800** (texto grande) no desktop **e** no celular. Override de tamanho no celular só nas bandas Tap Shoe e Patriot, por classe da banda (E41 `.e41-t-sm`); um `.title{17px}` global quebrou isso no 05.
5. **Nada de PNG em paleta (R5).** Nunca PNG de 8 bits (modo P): camo posteriza e sombra suave vira degrau. Recorte sobre banda lisa ou texturizada = JPG assado nela (+ gêmeo `-dm` em papel claro); PNG-24 só onde precisa de transparência de verdade e o arquivo fica leve. A v0.6 regravou três packshots do kit em PNG-24; quatro continuam em paleta (Em aberto).
6. **Farelos do rasgo (R6).** Farelo fino: raio 0,6 a 1,3px a 2x, de 0,5 a 4,5px da linha (grão da rev-oct-03). Nada de pontos de 3 a 5px a 10 ou 25px da linha. A v0.6 refez todas as bordas E18 texturizadas do kit assim (`tools/compose_v06.py edges`); os rasgos assados dentro de E21, E24, E24B, E26, E30 e E33 ainda têm os pontos grandes (Em aberto).
7. **Círculo de detalhe (R7).** Só quando o detalhe lê com cerca de 40% do círculo (puxador de zíper, borda de bolso, aba do passa-cinto). Em camo, recorte de catálogo lê só como tecido: aí vai o sistema inteiro com rótulos em texto vivo e filetes laranja (E38), e pede-se ao cliente a foto de detalhe original.
8. **Hero de foto e transições de foto (R8). Decisão do responsável, 2026-10-08** (substitui a regra anterior do degradê de 120 a 160px, que fazia a foto derreter na banda). **Nenhuma transição de foto para banda é degradê de alfa nem derretido com desfoque.** Toda borda de foto que encontra uma banda é **rasgo ou outra textura orgânica**: a foto como cópia rasgada sobre a banda (linha rasgada irregular, o miolo branco do papel aparecendo ao longo do rasgo, sombra projetada da luz única do lote, de cima à esquerda) ou a folha da banda seguinte rasgada por cima da foto (E18 assado, farelo fino da R6). Escurecer de leve, **dentro da foto**, a área ou o canto onde fica o texto vivo é permitido (não é transição): só o necessário para o AA do texto, com a foto ainda lendo clara; o resto da foto fica como foi tirada. Hero de foto em tela cheia: a foto cobre a banda de ponta a ponta (600 de largura) até o rasgo para a banda seguinte, texto vivo por cima (imagem de fundo + VML + `bgcolor` de fallback). Quando o `cover` corta rosto ou põe o logo num boné a 375px, o hero ganha **recorte próprio de celular** (trocado por regra de media query, gravado a 2x do tamanho CSS do celular, não mais), seguindo a mesma regra: rasgo, nunca degradê. Gerador de registro: `torn_sheet`, `tear_into`, `burn_weight` e `photo_hero` do `compose_assets.py` do lote de novembro.
9. **Hero de estúdio (R9).** Grupo de packshots abre o e-mail (E35) só quando não existe foto de uso da linha no banco nem nas imagens da loja; registrar no brief. O padrão do kit continua sendo hero com foto de uso.
10. **Sem repetição (R10).** Nenhuma imagem aparece duas vezes no mesmo lote (o 05 reaproveitou o cartão-presente e o pescador do 02 na rodada 1); cada e-mail do lote abre com tratamento de hero diferente e nenhum layout de bloco se repete.
11. **Moldura de colagem (R11).** Foto emoldurada perto de rasgo assado ou fica livre dele (moldura termina 30px ou mais acima da linha) ou o atravessa de vez (40px ou mais além). Moldura cortada por 15px parece erro (E36).
12. **Copy do cliente (R12).** Entra literal: headline, subheadline, corpo, nome de produto, linha, CTA, ordem. Só muda o tratamento tipográfico do kit (caixa-alta real, apóstrofo tipográfico, palavras presas, divisão da headline em duas vozes). O que parece erro (CTA que não bate, preço fora da faixa, subheadline repetida, ponto duplo) vai para a lista do brief para o cliente, nunca corrigido em silêncio.
13. **Referências (R13).** E-mail de referência dá só estrutura (ordem, ritmo, recurso). Nunca cor, fonte, copy, selo ou bolinha de cor.
14. **Peso (R14).** Cerca de 800 KB de imagem por e-mail no modo claro, contando cada composição no tamanho real; gêmeos `-dm` contados à parte (parte dos clientes baixa). No máximo 4 texturas diferentes e uma composição pesada (acima de 100 KB) além do hero; hero só de celular conta no celular.
15. **Portão de QA (R15).** `lint_layout.py` (do lote de novembro: largura, imagem, rasgo, foto, margem, texto, corte, a 600 e 375) limpo, depois passada visual do Email QA Reviewer nos renders 680 / 375 / escuro, **antes** de o responsável ver qualquer layout. O lint não enxerga defeito de imagem (emenda, farelo, recorte): isso é do revisor.

## Decisões do responsável (2026-09-25, e-mails de outubro revisados · v0.5)

Expressas nas imagens `references/rev-oct-01..05-*.png` e listadas em `03-work/email/2026-10-broadcasts/revision-r2.md`. **Onde divergem das decisões de 2026-09-24, valem estas** (as antigas estão marcadas "substituída" abaixo e nas tabelas).

- **Botão:** `#FF6400` com **texto branco** `#FFFFFF`, Prompt 800 caixa-alta 17px, tracking 2px, **raio 4px**. Contraste **2,97:1, abaixo do AA** (4,5 e 3,0): **exceção pedida pelo responsável em 2026-09-25**, registrada; o QA aponta, não bloqueia. Botão pequeno dentro de card: 13px, padding 14px 22px (a revisão mostra 12px, o que dá 40px de altura; subido para os 44px mínimos das regras).
- **Corpo em Prompt:** todo corpo, card e rodapé em Prompt 400/500 (substituto da Sweet Sans), fallback Helvetica, Arial; Outlook desktop cai em Arial.
- **Headline em duas vozes, serifa dominante:** Playfair Display 900 caixa-alta 96 a 110px desktop (entrelinha cerca de 0,9, pode quebrar em 2 linhas), 64 a 72px mobile; linha sans Prompt 800 caixa-alta 26 a 32px (mobile 22 a 24), acima ou abaixo da serifa. Cor da serifa: branco, laranja (só em Tap Shoe, Patriot Blue, Major Brown ou foto escura), Tap Shoe em papel claro, ou Aluminum claro `#CFC8BF`.
- **Corpo centralizado logo abaixo da headline** nas bandas internas, 17/24, sentence case. **Subtítulo espaçado caixa-alta só no hero.**
- **Caixa de produto (E27):** centralizada, contorno 1px `#FEF4C6`, raio 10px; título laranja Prompt 800, **19px obrigatório sobre Major Brown e retícula** (só passa como texto grande), 16 a 17px permitido sobre Tap Shoe e Patriot Blue (4,8:1, passa em qualquer tamanho; é o que a rev-oct-02 mostra), nome branco 15px, variante apagada 13px, preço 20px branco em negrito **sem sublinhado**; sem os traços laranja nos cantos.
- **Rodapé:** ícone colorido do Instagram (`assets/icon-instagram.png`, 72px exibido em 44) ao lado de "Follow us on Instagram" / @HABITOUTDOORS; sem linha de endereço e sem descadastro no HTML (confirmação da decisão de 2026-09-24).
- **Um review só por e-mail** (E32), com nome e nota reais.
- **Superfícies novas:** papel claro com manchas de camo, Major Brown com retícula de meio-tom, degradê Tap Shoe → Patriot Blue com linhas topográficas.

## Decisões do responsável (2026-09-24)

- **Linha de pesca desenhada** (traço branco solto sobre a foto): recurso da marca, **no máximo um e-mail sim, outro não**, e nunca mais de uma vez no mesmo e-mail.
- **Item que os e-mails enviados não têm, o kit não usa.** Por isso ficam fora: endereço e linha de motivo no rodapé, merge de primeiro nome, qualquer personalização por nome. Endereço e descadastro vêm do rodapé do próprio ESP (conferir no Omnisend: CAN-SPAM).
- **Item que os e-mails têm, o kit segue igual:** Instagram @HABITOUTDOORS, menu MEN'S | WOMEN'S | YOUTH | SALE, copyright "Built By Wilde Creative".
- **Produto:** nome, preço e packshot sempre do catálogo da loja (`01-brand/photos/products/catalog.json`, gerado por `email-ops/tools/fetch_shopify_catalog.py`), reconfirmados na data do e-mail.
- **Textura escura** apagada (rodapé é Tap Shoe liso).

## Mapa da marca

**Os agentes leem esta tabela primeiro.** Caminhos relativos à raiz do projeto.

| Item | Caminho | Status |
|---|---|---|
| Diagnostic Report **[trava]** | clients/habit-outdoors/01-brand/strategy/diagnostic-report.md | derivado do Brand Identity Guide em 2026-09-24, validar partes "(inferido)" |
| Strategy Report **[trava]** | clients/habit-outdoors/01-brand/strategy/strategy-report.md | derivado do Brand Identity Guide em 2026-09-24, red flags a validar |
| Style guide / toolbox **[trava]** | clients/habit-outdoors/01-brand/identity/brand-guidelines.md + Habit_BrandIdentityGuide_Booklet 2.4.26 Update.pdf | oficial; HEX amostrado do vetor da p.17 |
| Voz e compliance | clients/habit-outdoors/01-brand/strategy/strategy-report.md (tom) | marca não regulada; claims de desempenho seguem a ficha do produto |
| Contexto geral da marca | clients/habit-outdoors/README.md | |
| Banco de fotos aprovado | clients/habit-outdoors/01-brand/photos/lifestyle/ (fotos de uso, catálogo em **lifestyle/INDEX.md**) · regras em photos/README.md | 17 recortes provisórios `crop-sent-*` dos e-mails enviados (2026-09-24, `email-kit/tools/crop_sent.py`); aguardando originais. Texturas moram em `email-kit/assets/` (tex-*, grad-*) |
| Biblioteca de imagens (seleção) | clients/habit-outdoors/01-brand/photos/library/ (catalog.md = índice único; entrada em `_inbox/`; página: photos/build_image_library.py → https://claude.ai/code/artifact/4006b37f-7efb-4d33-9d00-99c119d08a88) | criada em 2026-10-07; 21 fotos atuais catalogadas, seleção do responsável entra a partir de 2026-10-08 |
| Packshots de produto | clients/habit-outdoors/01-brand/photos/products/ (catalog.json + PNG transparente 1200px) | 169 produtos no catálogo, 39 packshots baixados em 2026-09-24 (fora do git) |
| Logo vetorial | clients/habit-outdoors/01-brand/identity/logo/ (svg, pdf, png 600dpi: aluminum, white, black) | extraído do vetor do PDF p.14 em 2026-09-24 |
| E-mails já enviados (referência) | clients/habit-outdoors/01-brand/email-kit/references/ | 5 e-mails de setembro 2026, analisados em references/README.md |
| Pasta de e-mails (trabalho) | clients/habit-outdoors/03-work/email/ | |
| Pasta de entregas (final) | clients/habit-outdoors/04-deliverables/email/ | |

## Como alimentar este kit (regras pra quem toca o projeto)

Cada seção tem uma fonte certa. Nunca preencher uma seção com a fonte errada, nunca inventar valor, nunca trazer valor de outra marca.

| Seção do kit | Fonte | Regra |
|---|---|---|
| `tokens.json` → cor, fonte, raio | **Style guide** | Hex exato do guia oficial. Token de componente ou de wireframe não conta. Sem guia: extrair do site no ar e marcar "extraído". Registrar a fonte de cada valor na tabela de tokens abaixo |
| `tokens.json` → neutros e dark mode | Derivados da paleta | Tons da paleta (ex.: cor de texto a 70%), nunca cor nova. Checar contraste |
| `assets/` | Style guide + banco de fotos | Logo sempre rasterizado do vetor, versão clara e escura. Foto só do banco aprovado, seguindo a regra de foto. Tamanhos em `assets/README.md` |
| Regra de caixa, itálico, formato de botão | Style guide + site no ar | O que a marca usa de verdade; o padrão das regras gerais é só ponto de partida |
| Estratégia aplicada → ICPs, provas | **Diagnostic Report** | ICP como arquétipo (medo, necessidade, que e-mail serve). Provas: só as que existem hoje, com fonte; listar também as que ainda não existem |
| Estratégia aplicada → mensagens, frase-âncora, tom, red flags | **Strategy Report** | Copiar a mensagem e a **condição de uso**. Frase-âncora com status; "proposta" nunca vira headline nem texto fixo |
| Regras só da marca | Voz e compliance + reports | Apontar pro documento, não duplicar. Régua legal manda acima de tudo |
| Texto de amostra dos módulos | Strategy Report | No tom da marca, sem claim, sem número inventado, conferido contra red flags |
| Referências | Responsável pelo projeto | Arquivos em `references/`, uma linha cada sobre o que aproveitar |

Quando uma fonte muda (report refinado de novo, guia atualizado): atualizar a seção correspondente, rodar `build_kit.py` de novo se mexeu em token, anotar no changelog e voltar o status pra "rascunho" até nova aprovação.

## Tokens

Valores em `tokens.json`. Esta tabela registra **de onde veio** cada um. Desde a v0.2 o `components.html` é **lapidado à mão** (valores inline); **não rodar `build_kit.py` de novo** sobre ele, senão a lapidação se perde. Mudou um token: editar o `tokens.json` (registro) **e** o valor inline no `components.html`.

### Cor

| Token | Hex | Uso | Fonte | Contraste |
|---|---|---|---|---|
| `color.primary` | `#FF6400` | preenchimento de botão; texto só em banda escura | e-mails enviados (medido; fora da paleta do guia) | como texto: 4,77 em Tap Shoe, 4,84 em Patriot Blue, **3,46 em Major Brown (só texto grande)**, reprova em claro |
| `color.on_primary` | **`#FFFFFF`** (v0.5) | texto do botão | **decisão do responsável 2026-09-25** (e-mails revisados); ~~`#2A2B2D`, decisão de 2026-09-24~~ **substituída** | **2,97:1, abaixo do AA: exceção registrada** (Tap Shoe dava 4,77:1) |
| `color.text` / `color.dark` | `#2A2B2D` | título, texto, link em fundo claro, rodapé | e-mails enviados = Tap Shoe do guia (p.17) | 10,5 em `#E2DDD9`; branco sobre ela 14,2 |
| `color.text_muted` | `#5C5249` | corpo, eyebrow em fundo claro | Turkish Coffee do guia (p.17) | 7,6 em branco, 5,65 em `#E2DDD9`, **2,65 na textura** (lá usar `#2A2B2D`) |
| `color.surface` / `color.surface_alt` | `#FFFFFF` / `#E2DDD9` | bandas claras | branco; `#E2DDD9` medido nos e-mails (fora da paleta) | |
| `color.accent_1` | `#202944` | banda escura, última chamada | Patriot Blue do guia; e-mails medem `#233052` a `#2C3955` (com textura) | laranja 4,84 |
| `color.accent_2` / `color.line_mens` | `#483F39` | banda, cards Men's | Major Brown do guia; e-mails `#4A4038` | laranja 3,46 (só grande) |
| `color.line_womens` | `#595442` | cards Women's | Ivy Green do guia; e-mails `#5A5540` | branco 7,6 |
| `color.line_youth` | `#7F7064` | cards Youth | e-mails enviados (fora da paleta) | branco 4,77; `#E2DDD9` reprova (3,5), por isso texto branco |
| `color.card_outline` | `#FEF4C6` | contorno 1px dos cards | e-mails enviados (fora da paleta) | decorativo |
| `color.texture_fallback` | `#A39A8C` | fallback da textura Aluminum | derivado (média da textura `#9F9888`) | `#2A2B2D` 5,1 |
| `color.line` / `color.page` | `#CFC8BF` / `#EFECE9` | filete, fundo da página | derivados | |
| `color.aluminum_light` (v0.5) | `#CFC8BF` | cor da serifa em banda escura (rev-oct-04, CRATER VALLEY) | o mesmo hex de `color.line` | sobre Tap Shoe 8,5 |
| `color.info_box_*` (v0.5) | contorno `#FEF4C6`, título `#FF6400`, variante `#B0A89C` (Tap Shoe, Patriot) ou `#CFC8BF` (Major Brown) | E27 | revisão do responsável | título 19px 800 = texto grande: 4,8 Tap Shoe, 4,8 Patriot, 3,5 Major Brown, 3,1 retícula (pior caso); `#B0A89C` em Major Brown daria 4,4, por isso `#CFC8BF` (6,1) |
| `color.panel_*` (v0.5) | Aluminum `#A39A8C`, Dusk `#ACB1B3`, Turkish Coffee `#5C5249`, Ivy Green `#595442` | painel chapado atrás do packshot (E28, E29) | cores do guia (p.17) mais próximas das medidas na revisão (`#A69A89`, `#ABB1B3`, `#5A4538`, `#575441`) | sem texto em cima |
| `color.panel_rust` / `color.panel_slate` (v0.5, "product panel") | ferrugem `#774727`, ardósia `#4F5C5F` | painel chapado atrás do packshot (E29), como no 02 Youth | **rev-oct-02, medido** (valores do `02-youth-season.html` e dos JPG `o2-panel-hoodie` / `o2-panel-pant`); fora da paleta do guia, mantidas por decisão do responsável (2026-09-25) | sem texto em cima |

Dark mode (Apple Mail / app do Outlook), tudo derivado de Tap Shoe: página `#1E1F21`, superfície `#2A2B2D`, banda `#34353A`, título `#F1EEEB`, corpo `#D6D0CA`, muted `#B0A89C` (era `#A39A8C`, dava 4,4:1 na banda), link `#F1EEEB` sublinhado (laranja na banda dá 4,1:1), laranja só na palavra de destaque grande.

### Tipografia (provisória: o responsável fecha a tipografia no Figma)

| Papel | Tamanho desktop / mobile | Peso | Nota |
|---|---|---|---|
| **Headline em duas vozes (v0.5, todo hero e toda banda)** | serifa **100/90** (hero 104/94; faixa 96 a 110) · **64/58**; linha sans **30/32** (faixa 26 a 32) · **22/24** | Playfair 900 + Prompt 800, caixa-alta | a serifa é a protagonista, pode quebrar em 2 linhas; cabe cerca de 7 letras por linha a 100px numa banda de 520px e a 64px no celular (Playfair 900 caixa-alta mede cerca de 0,66em por letra) |
| Headline em coluna dividida (v0.5: E04, E06, E09, E20, E31) | serifa 64/60 · 60/56; sans 30/32 (E31: 26/28) · 22/24 | idem | |
| ~~Display (hero) 46/50 com uma palavra serifada no meio~~ | | | **substituída pela headline em duas vozes (v0.5)** |
| ~~Hero em duas vozes (E02) sans 34/38 + serif 88/90~~ | | | **substituída: 30/32 + 104/94** (os dois filetes laranja do E02 continuam; a revisão não os usa, ver "Em aberto") |
| ~~Título de banda 34/38 · 28/32~~ | | | **substituído pela headline em duas vozes** |
| Subtítulo espaçado | 15/22 no hero (14/22 antes), tracking 2px | Prompt 500, caixa-alta | **v0.5: só no hero**; banda interna vai headline e corpo |
| Título de item | 18/22 | 800, caixa-alta | |
| Caixa de produto (E27, v0.5) | título 19/21 · nome 15/20 · variante 13/18 · preço 20/24 | Prompt 800 / 500 / 400 / 800 | título laranja, preço sem sublinhado |
| Corpo de banda (v0.5) | **17/24**, centralizado sob a headline | **Prompt 400** | sentence case; ~~Helvetica/Arial 16/26~~ substituído |
| Corpo de card, lista, rodapé | 15 ou 16px | Prompt 400/500 | |
| Label / eyebrow | 13/20, tracking 2,4px, caixa-alta | 500 | acima da headline |
| Etiqueta do Label Hero (E33, v0.5) | sans 30/40 · 22/28; serifa 72/80 · 48/56 | Prompt 800 / Playfair 900 | |
| Legal | 12 a 13/18 | 400 | |

Família e fallback: Prompt + Playfair Display via Google Fonts (substitutos da Sweet Sans e da serifada licenciadas), pesos Prompt 400, 500 e 800 (v0.5 acrescentou o 400). **v0.5: corpo também em Prompt**, fallback Helvetica, Arial; Outlook cai em Arial. **Regra de caixa:** headline, título de item, subtítulo e botão em **maiúsculas reais no HTML** (não só CSS); corpo em sentence case.

### Botão e espaçamento

Botão (**v0.5**): `#FF6400` com **texto branco `#FFFFFF`** (2,97:1, exceção do responsável, 2026-09-25), Prompt 800 caixa-alta **17px**, tracking 2px, **raio 4px**, padding 16px 36px (hero 16px 64px), 52px de altura, `<td bgcolor>` + `<a>`. Pequeno em card (E27/E29): 13px, padding 14px 22px, 44px. Largo de fechamento (E30): 420px, largura total no mobile. ~~Texto `#2A2B2D`, raio 6px, 16px Helvetica~~ (2026-09-24) **substituído**. **Uma cor de botão só**: os e-mails enviados nunca usam outra, então o kit não tem variante de cor. Espaçamento: escala 8pt, gutter 40px desktop / 24px mobile, banda 56-72px vertical (40px mobile). Card de produto: raio 12px, contorno 1px `#FEF4C6`. v0.5: caixa de produto (E27) raio 10px; card emoldurado (E29) raio 14px, 24px de margem lateral.

## Assets

| Arquivo | Uso | Origem |
|---|---|---|
| `assets/logo-light.png` · `logo-dark.png` (320x52, exibido 160x26) | logotipo HABIT® no header claro / versão branca pra dark mode e foto escura | vetor do PDF p.13-14 |
| `assets/logo-footer.png` (320x143, exibido 160x71) | logo completo empilhado, branco, no rodapé E13 | vetor do PDF p.13-14 |
| `assets/hero-fishing.jpg` (1200x760) | E02 | recorte de e-mail enviado, trocar pelo original do banco (ainda tem a linha de pesca desenhada) |
| `assets/card-fishing.jpg` (1120x1200) | E15 | recorte de e-mail enviado, trocar pelo original do banco (Sep 22, abaixo do botão SHOP FISHING; linha desenhada removida, topo estendido a partir do fundo escuro pra headline; nativo 1031x1105 ampliado 1,09x) |
| `assets/feature-family.jpg` (1200x700) | E10, E16 | recorte de e-mail enviado, trocar pelo original do banco |
| `assets/pack-mens-heavyweight-soft-flannel-360.png` (360, exibido 180) · `-200.png` (exibido 100) | E04, E07 (v0.3: troca de conteúdo) | packshot da loja, handle `mens-heavyweight-soft-flannel` (Basecamp Plaid Rifle Green), `tools/compose.py` job_packs |
| `assets/pack-mens-crater-valley-full-zip-200.png` (exibido 100) | E07 | packshot da loja, handle `mens-crater-valley-full-zip-fleece-jacket` (Woodland Deadwood Khaki) |
| `assets/pack-mens-cedar-branch-parka-400.png` · `pack-mens-cedar-branch-bib-400.png` (exibidos 200) | E17 | packshots da loja, handles `habit-mens-cedar-branch-insulated-waterproof-parka` e `mens-cedar-branch-insulated-bib` (Realtree APX) |
| `assets/texture-light.jpg` (1200x880) | E03, fallback `#A39A8C`; fonte das linhas topográficas do `compose.py` | padrão topográfico do PDF p.24 |
| `assets/texture-dark.jpg` (1200x800) | **sem uso desde a v0.2** (rodapé dos e-mails é Tap Shoe liso) | padrão topográfico do PDF p.24 |
| `assets/edge-tapshoe.png` · `edge-brown.png` · `edge-light.png` (1200x60, exibido 600x30, ~9KB cada) | E18, borda rasgada `#2A2B2D` / `#483F39` / `#E2DDD9` | gerado com Pillow, imitando a transição dos e-mails enviados |
| `assets/edge-light-dm.png` | E18, troca do `edge-light` no dark mode (`#34353A`, mesmo contorno) | gerado com Pillow |

Apagados na v0.2: `card-barn.jpg`, `portrait-1..3.jpg`, `sample-*.jpg`, `product-1.png` (placeholders sem uso). Apagado na v0.3: `product-flannel.png` (nenhuma referência depois da troca por packshots reais).

### Assets da v0.3 (rascunho, E19 a E23)

Todos gerados por `tools/compose.py` (rodar de novo troca produto ou foto; cada job imprime peso e checagem de emenda). JPG 4:4:4, qualidade escolhida entre q62 e q76 para que a cor da banda decodifique exata nas bordas; o fallback é o `bgcolor` da célula.

| Arquivo | Uso | Origem | Fallback / borda |
|---|---|---|---|
| `tex-tapshoe-grain.jpg` (1200x1200, 110KB) | superfície escura com grão + linhas topográficas; receita usada no fundo do E22; pode ir como `<td background>` | gerado: Tap Shoe + grão + linhas extraídas de `texture-light.jpg` (p.24) | `#2A2B2D` |
| `grad-tapshoe-brown.jpg` (1200x1200, 103KB) | degradê atmosférico granulado; receita usada no fundo do E19 | gerado: Tap Shoe → Major Brown, névoa clara no meio, grão | `#2A2B2D` em cima, `#483F39` embaixo |
| `e19-cluster-cedar-branch.jpg` (1200x840, 147KB) | E19 | packshots `mens-cedar-branch-insulated-bib`, `habit-womens-cedar-branch-insulated-parka`, `habit-mens-cedar-branch-insulated-waterproof-parka` (Realtree APX) sobre o degradê | topo `#2A2B2D`, base `#483F39` (desvio 0 / 1) |
| `e20-bleed-buck-hollow.jpg` + `-dm.jpg` (480x1114, 103KB + 98KB) | E20, claro e dark mode | packshot `mens-buck-hollow-2-0-jacket` (Mossy Oak New Bottomland), 64% da largura visível | `#E2DDD9` / `#34353A` (desvio 0) |
| `e21-cross-buck-hollow.jpg` + `-dm.jpg` (1200x660, 96KB + 88KB) | E21, claro e dark mode | packshot `mens-buck-hollow-2-0-jacket-2` (Realtree APX), borda rasgada no mesmo desenho do E18 | topo `#2A2B2D`, base `#E2DDD9` / `#34353A` (desvio 0) |
| `e22-collage-a.jpg` (1200x900, 144KB) · `e22-collage-b.jpg` (1200x700, 91KB) | E22 | fotos: homem no fardo de feno e homem no estábulo, **recortes de `references/September 24.png`** (substituir pelos originais do banco); close do bolso = imagem da loja `mens-heavyweight-soft-flannel-6` (rótulo "Dual Chest Pockets" cortado fora) | `#2A2B2D` (desvio 0) |
| `e23-crater-valley-hoodie.png` (800x800, 111KB) · `e23-cedar-branch-bib.png` (800x800, 67KB) | E23, transparentes (servem no claro e no dark) | imagens da loja `mens-crater-valley-performance-hoodie-2` (Woodland Ghost Khaki) e `mens-cedar-branch-insulated-bib` (Realtree APX) | transparente |

Bolinhas de cor do E23 (mediana dos pixels opacos do packshot de cada variante, `compose.py swatch`): Crater Valley Performance Hoodie · Woodland Ghost Khaki `#A59C99` (`-2`), Woodland Vintage Wren `#887E75` (1ª imagem), Woodland Helix Major Brown `#968A88` (`-9`), Fallen Rock `#AC9D8B` (`-10`), Ivy Green `#7E7A68` (`-11`). Cedar Branch Insulated Bib · Realtree APX `#493B32`, Mossy Oak New Bottomland `#5B4B44` (`-2`), Turkish Coffee `#291E19` (`-8`).

**Peso por e-mail:** as composições pesam 90 a 150KB cada. Um e-mail com E19 + E22 já leva cerca de 380KB só nelas; somando hero e produtos, o teto de ~800KB comporta no máximo duas composições pesadas por e-mail. As versões `-dm` são baixadas também em parte dos clientes (mesma situação do `edge-light-dm.png`).

### Assets da v0.4 (rascunho: texturas, E24 a E26, bordas texturizadas)

Tudo gerado por `tools/compose.py` (jobs `textures04`, `edges04`, `e24`, `e26`; rodar `textures04` primeiro, os outros assam as texturas dentro). Fotos de `photos/lifestyle/` (INDEX.md).

**Texturas** (1200x1600, JPG q70, todas abaixo de 90 KB). *Tile* = periódica em cima e embaixo (ruído gerado no domínio de Fourier): `background-size:600px auto; background-repeat:repeat-y`, **qualquer altura de banda**. *Stretch* = degradê esticado na banda (`background-size:100% 100%`), bom de 300 a 1200px de altura. Outlook desktop: VML `v:fill type="frame"` estica todas na banda (é grão, a distorção não aparece). Contraste = pior caso medido nos pixels da textura (percentis 1 e 99 de luminância, sem suavizar), ou seja, conservador.

| Arquivo | Tipo | Fallback `bgcolor` | Texto permitido | Pior contraste medido |
|---|---|---|---|---|
| `tex-paper-light.jpg` | tile | `#E2DDD9` | `#2A2B2D`, label `#5C5249`; dark mode: classe `dm-tex` troca para `tex-paper-light-dm.jpg` (`#34353A`) | `#2A2B2D` 9,8 · `#5C5249` 5,3 |
| `tex-paper-light-dm.jpg` | tile | `#34353A` | só dark mode (dm-h, dm-p, dm-muted) | `#F1EEEB` 9,5 · `#D6D0CA` 7,2 · `#B0A89C` 4,7 |
| `tex-paper-tapshoe.jpg` | tile | `#2A2B2D` | branco, corpo `#E2DDD9`, laranja só com 24px ou mais | branco 12,8 · `#E2DDD9` 9,5 · laranja 4,3 |
| `tex-grain-brown.jpg` | tile | `#483F39` | branco, corpo `#E2DDD9`, laranja só no destaque serifado grande | branco 8,9 · `#E2DDD9` 6,6 · laranja 3,0 |
| `tex-grain-patriot-water.jpg` | tile | `#202944` | branco, corpo `#E2DDD9`, laranja só com 24px ou mais | branco 11,8 · `#E2DDD9` 8,7 · laranja 4,0 |
| `tex-grain-ivy.jpg` | tile | `#595442` | branco (corpo `#E2DDD9` passa raspando), sem laranja | branco 6,7 · `#E2DDD9` 5,0 |
| `tex-camo-blur.jpg` | tile | `#483F39` (média da textura `#403530`) | branco, sem laranja | branco 6,5 · `#E2DDD9` 4,8 |
| `tex-topo-tapshoe.jpg` | tile | `#2A2B2D` | branco, corpo `#E2DDD9`, laranja só com 24px ou mais | branco 11,7 · `#E2DDD9` 8,7 · laranja 3,9 |
| `grad-tapshoe-to-brown.jpg` | stretch | `#2A2B2D` | branco, corpo `#E2DDD9` | branco 9,2 · `#E2DDD9` 6,8 |
| `grad-patriot-to-tapshoe.jpg` | stretch | `#202944` | branco, corpo `#E2DDD9` | branco 11,7 · `#E2DDD9` 8,7 |
| `grad-paper-to-aluminum.jpg` | stretch | `#E2DDD9` | só `#2A2B2D` (`#5C5249` reprova no Aluminum); dark mode `dm-tex` | `#2A2B2D` 4,9 · `#5C5249` 2,6 |
| **v0.5** `tex-paper-camo.jpg` (rev-oct-03) | tile | `#E2DDD9` | `#2A2B2D`, label `#5C5249`; dark mode: classe **`dm-tex-camo`** troca para `tex-paper-camo-dm.jpg` (`#34353A`) | `#2A2B2D` 8,5 · `#5C5249` 4,6 |
| **v0.5** `tex-paper-camo-dm.jpg` | tile | `#34353A` | só dark mode (dm-h, dm-p, dm-muted) | `#F1EEEB` 9,2 · `#D6D0CA` 7,0 · `#B0A89C` 4,5 |
| **v0.5** `tex-halftone-brown.jpg` (rev-oct-01) | tile | `#483F39` | branco, corpo `#E2DDD9`, laranja só grande (título da caixa 19px 800 incluso) | branco 9,3 · `#E2DDD9` 6,9 · laranja 3,1 |
| **v0.5** `grad-tapshoe-to-patriot-topo.jpg` (rev-oct-05) | stretch | `#2A2B2D` | branco, corpo `#E2DDD9`, laranja só grande | branco 11,6 · `#E2DDD9` 8,6 · laranja 3,9 |

Origem: papel e grãos gerados (grão fino, mancha de cerca de 1 nível, fibras; a mancha caiu de 2,6 para 1 nível porque cada `<td>` reinicia o tile e a mancha maior aparecia como degrau reto no papel claro). Água: estrias horizontais dobradas por um campo de ondas lento, mais manchas claras (o azul nublado de Sep 22). Camo: tecido Realtree APX do packshot da loja `habit-mens-cedar-branch-insulated-waterproof-parka-6` (área sem logo, mão nem rótulo), ampliado, emendado por cross-fade (sem espelho), desfocado, 30% dessaturado e escurecido até o 1% mais claro ficar abaixo de 0,12 de luminância. Topo: linhas da p.24 (via `texture-light.jpg`), espelhadas na metade do tile. As texturas da v0.3 (`tex-tapshoe-grain.jpg`, `grad-tapshoe-brown.jpg`) continuam para E19 e E22.

**Bordas E18 texturizadas** `edge-tex-{acima}-{abaixo}.jpg` (1200x80, exibidas 600x40, 4 a 11 KB): a parte de baixo usa as **últimas** linhas do tile da banda de baixo, então continua sem emenda na `<td>` seguinte (que começa na linha 0); sombra suave acima do rasgo (papel sobreposto), para o rasgo ler entre cores próximas. `td bgcolor` = fallback da banda de cima. Prontas: paperlight/papertapshoe (os dois sentidos), paperlight/patriot (os dois sentidos), papertapshoe/brown (os dois sentidos), brown para paperlight, brown/patriot (os dois sentidos), brown para camo, camo/ivy (os dois sentidos), ivy para papertapshoe, e `-footer` (para o Tap Shoe liso do E13) a partir de paperlight, patriot, brown, ivy e camo. Toda borda com papel claro tem gêmea `-dm`. Outro par: acrescentar em `EDGES_V04` no `compose.py`.

| Arquivo | Uso | Origem | Peso |
|---|---|---|---|
| `e24-hero-forest.jpg` (1200x1560) | E24, texto em cima; rasga para Ivy grain | `crop-sent-sep15-family-forest-walk.jpg` ampliada 1,25x, topo em neblina gerado das linhas de cima da própria foto | 147 KB |
| `e24-hero-barn.jpg` (1200x1560) | E24B, texto embaixo; rasga para Major Brown grain | `crop-sent-sep24-barn-door-feed-bag.jpg`, fachada do celeiro puxada 190 linhas para cima (logo), pernas cortadas | 143 KB |
| `e26-torn-stable.jpg` + `-dm.jpg` (1200x820) | E26 em papel claro | `crop-sent-sep24-stable-horse.jpg`, moldura `#F4F1ED`, rasgo embaixo e à direita, -1,6° | 94 + 94 KB |
| `e26-torn-camp.jpg` (1200x600) | E26 em Major Brown grain (asset pronto, fora da página) | `crop-sent-sep15-camp-chairs-family.jpg`, moldura `#E2DDD9`, rasgo em cima e à esquerda, +1,4° | 107 KB |

**Peso por e-mail na rodada 2:** hero E24 de cerca de 145 KB, mais 3 ou 4 texturas de 87 a 90 KB (cada textura baixa uma vez, mesmo repetida em várias bandas), mais bordas de cerca de 8 KB: perto de 500 KB antes de produto e colagem. Para caber em cerca de 800 KB: no máximo **4 texturas diferentes** por e-mail e **uma** composição pesada além do hero (E19, E22 ou E26).

### Assets da v0.5 (rascunho: E27 a E34, superfícies novas, ícones)

Tudo gerado por **`tools/compose_v05.py`** (arquivo novo que importa `compose.py`; o `compose.py` não mudou). Jobs: `surfaces` (rodar primeiro), `e28`, `e29`, `e30`, `e31`, `e32`, `e33`, `icons`. Fotos só de `photos/lifestyle/` (INDEX.md) e packshots de `photos/products/`; nada recortado de outra marca.

| Arquivo | Uso | Origem | Fallback | Peso |
|---|---|---|---|---|
| `tex-paper-camo.jpg` + `-dm.jpg` (1200x1600) | superfície papel claro com camo (tabela de texturas) | gerado: papel claro + 3 camadas periódicas de manchas `#D5CFC8` / `#D0CAC2` (dark: `#38393E` / `#3A3B40`) | `#E2DDD9` / `#34353A` | 86,9 + 88,3 KB |
| `tex-halftone-brown.jpg` (1200x1600) | superfície Major Brown com retícula; E27 | gerado: grão Major Brown + grade hexagonal de pontos (16px a 2x, periódica) com raio pelo campo de densidade + spray escuro | `#483F39` | 86,3 KB |
| `grad-tapshoe-to-patriot-topo.jpg` (1200x1600, stretch, 4:4:4) | E34 | gerado: degradê Tap Shoe → Patriot Blue + linhas topográficas da p.24 | `#2A2B2D` | 87,2 KB |
| `edge-tex-papertapshoe-papercamo.jpg` (+ `-dm`) · `edge-tex-papercamo-papertapshoe.jpg` (+ `-dm`) · `edge-tex-halftonebrown-papertapshoe.jpg` · `edge-tex-papertapshoe-halftonebrown.jpg` · `edge-tex-halftonebrown-footer.jpg` (1200x80) | E18 texturizado para as superfícies novas | `compose.compose_torn_edge_textured` | banda de cima | 5 a 10 KB cada |
| `e28-panel-mid-layer-jacket.jpg` · `e28-panel-windproof-pant.jpg` (600x660, exibidos 300x330) | E28 | packshots `men-s-mid-layer-jacket` (Veil Wideland Wolf) em Aluminum, `men-s-windproof-fleece-pant` (Mossy Oak Coyote) em Dusk | `#A39A8C` / `#ACB1B3` | 76,5 + 31,9 KB |
| `e29-panel-youth-bib.jpg` · `e29-panel-crater-fleece-model.jpg` (400x660, exibidos 200x330) | E29 | packshot `youth-cedar-branch-insulated-bib` (Realtree APX) em Ivy Green; imagem de modelo da loja `mens-crater-valley-full-zip-fleece-jacket-4` (texto de ficha cortado fora) em Turkish Coffee chapado | `#595442` / `#5C5249` | 26,8 + 43,7 KB |
| `e30-closing-hunter.jpg` (1200x1500) | E30 | `orig-hunt40-hunter-forest-back.jpg` (original Habit), suavizada 1,1px a 2x para caber em 150 KB, derrete em papel Tap Shoe e rasga para o rodapé liso | `#2A2B2D` | 148,6 KB |
| `e31-tilt-blind.jpg` + `-dm.jpg` (480x646, exibidos 240x323) | E31 | `crop-sent-sep2-hunter-blind.jpg` (recorte provisório) em moldura branca, 4°, sombra, sobre papel claro / escuro | `#E2DDD9` / `#34353A` | 38,6 + 38,8 KB |
| `e32-review-bib.jpg` (300x800, exibido 150x400) | E32 | packshot `mens-cedar-branch-insulated-bib` (Realtree APX) cortado pela borda direita, sobre papel Tap Shoe | `#2A2B2D` | 33,5 KB |
| `e33-label-hero-field.jpg` (1200x1400) | E33 | `orig-hunt22-three-hunters-field-sunrise.jpg` (original Habit), céu escurecido para o logo, rasga para a retícula | `#2A2B2D` | 146,3 KB |
| `icon-rain-factor-waterproof.png` · `icon-scent-factor.png` · `icon-windproof.png` · `icon-breathable.png` (128x128, exibidos 64) | E34 | **pictogramas oficiais da p.21** renderizados do vetor do PDF do guia, brancos, com as barras de "tecido" em laranja (tratamento da rev-oct-05) | transparente | 3,5 a 4,5 KB |
| `icon-instagram.png` (72x72, exibido 44) | E14 | ícone colorido do Instagram (já criado antes desta rodada) | transparente | 6,7 KB |

Total das imagens novas: cerca de 1.009 KB (a página do kit carrega todas; um e-mail usa só as dos módulos escolhidos). **Peso por e-mail:** E30 e E33 são composições pesadas (cerca de 147 KB cada); a regra da v0.4 continua: no máximo 4 texturas diferentes e uma composição pesada além do hero.

### Assets da v0.6 (rascunho: E35 a E41)

Gerados por **`03-work/email/2026-11-broadcasts/compose_assets.py`** (o gerador de registro: `seam_check`, `border_window`, `floor_shadow`, bordas com fase medida) e copiados para cá com prefixo `e35-` a `e41-` por **`tools/compose_v06.py copy`**. Trocar produto ou foto: rodar o `compose_assets.py` do lote (ou uma cópia dele para o lote novo) e depois o job `copy`. Todos JPG (nenhum PNG novo): assados na cor ou no tile da banda onde ficam, ou num painel chapado da paleta. Fotos `crop-sent-*` continuam provisórias ([[CONFIRMAR]] originais).

| Arquivo | Uso | Origem | Fundo / fallback | Peso |
|---|---|---|---|---|
| `e35-hero-group-womens-cedar-branch.jpg` (1200x760, exibido 600x380) | E35 | packshots `habit-womens-cedar-branch-insulated-parka`, `womens-cedar-branch-insulated-bib`, `womens-early-dawn-sherpa-shell-jacket` (Realtree APX), um chão, uma sombra, poça de luz; `n1-hero-group.jpg` | tile `tex-grain-ivy` a partir da linha 502 (css 251), bordas = tile (emenda medida no kit: 0,0 topo, 0,9 base) / `#595442` | 121,2 KB |
| `e36-hero-collage-field-water.jpg` (1200x880, exibido 600x440) | E36 | `crop-sent-sep10-utv-hunters`, `sep22-angler-tackle-box`, `sep2-hunter-blind`, `sep22-trout-in-hand`, molduras `#F1EEEB`, rasga para a água Patriot; `n2-hero-collage.jpg` | papel Tap Shoe a partir da linha 1000, base = últimas linhas de `tex-grain-patriot-water` (emenda no kit: 0,9 topo, 1,1 base) / `#2A2B2D` | 130,9 KB |
| `e37-hero-model-buck-hollow.jpg` (520x621, exibido 260x311) | E37 | imagem da loja `mens-buck-hollow-2-0-jacket` 07 (modelo, maior componente, sem rosto), ombros escurecidos; `n3-hero-model.jpg` | papel Tap Shoe, coluna 680 / linha 172 do tile / `#2A2B2D` | 69,7 KB |
| `e37-edge-tapshoe-paperlight.jpg` + `-dm.jpg` (1200x80, exibidos 600x40) | E37 (borda E18 que faz parte do módulo) | `phased_edge` com a altura da banda do E37 (478px a 600, medida igual à banda de novembro); farelo fino | Tap Shoe paper / papel claro (dark: papel escuro); emenda medida no kit: 0,2 | 11,2 + 6,9 KB |
| `e38-system-buck-hollow.jpg` + `-dm.jpg` (480x1040, exibidos 240x520) | E38, claro e dark mode | imagens da loja `mens-buck-hollow-2-0-jacket` 02 e `mens-buck-hollow-2-0-pant` 08, jaqueta sobre a calça, uma sombra; `n3-system*.jpg` | `tex-paper-light` / `-dm` | 100,6 + 100,4 KB |
| `e39-mosaic-stable.jpg` (640x600, exibido 320x300) | E39 | `crop-sent-sep24-stable-horse.jpg`, só o homem (recorte provisório); `n4-m-stable.jpg` | foto (raio 4px) | 50,1 KB |
| `e39-mosaic-pleat.jpg` · `e39-mosaic-pocket.jpg` (288x288, exibidos 144) | E39 | imagens da loja `mens-heavyweight-soft-flannel` 03 (pala e prega, marca de callout apagada) e 06 (bolso, rótulo cortado fora) | foto | 19,3 + 22,1 KB |
| `e39-colourways-flannel.jpg` (1000x560, exibido 500x280) | E39 | packshots `mens-heavyweight-soft-flannel` Basecamp Plaid Rifle Green e Major Brown, um chão, uma sombra; `n4-pair.jpg` | painel Aluminum chapado `#A39A8C` | 97,4 KB |
| `e40-card-insulated-boot.jpg` · `e40-card-stocking-cap.jpg` (660x528, exibidos 258x206; 2x dos 330px do celular) | E40 | packshots `mens-insulated-boot` (Realtree Edge) e `knit-camo-stocking-cap` (Brown Camo); `n2-card-5/6.jpg` | painel Ivy Green `#595442` / Dusk `#ACB1B3` | 42,1 + 34,3 KB |
| `e41-row-siesta-cape-tee.jpg` · `e41-row-camo-gloves.jpg` · `e41-row-3-season-bomber.jpg` (360x360, exibidos 170, 136 no celular) | E41 | packshots `mens-siesta-cape-long-sleeve-performance-tee-1`, `all-purpose-camo-leather-gloves`, `mens-3-season-bomber-jacket`; `n5-under30-2/4.jpg`, `n5-under100-1.jpg` | painel Aluminum / Dusk / Dusk (raio 8px) | 23,5 + 17,0 + 11,0 KB |

Total das imagens novas da v0.6: **857,8 KB** (16 arquivos; nenhum acima de 150 KB). Um e-mail usa só os dos módulos escolhidos: E35 ou E36 como hero (cerca de 125 KB) + E38 (100 KB no claro, mais 100 KB do gêmeo) é o caso mais pesado de dois módulos novos.

**Também regravados pela v0.6 (mesmo nome de arquivo, sem mudança de markup):** as 31 bordas E18 texturizadas `edge-tex-*.jpg` (+ `-dm`) da v0.4 e da v0.5, com farelo fino (R6; mesmas texturas, mesma semente, mesma linha de rasgo, conferido pixel a pixel: só os farelos e os blocos JPG em volta deles mudaram; 4 a 11,5 KB cada, como antes); e três packshots em PNG-24 no lugar do PNG em paleta (R5): `pack-mens-heavyweight-soft-flannel-200.png` 60,9 KB, `pack-mens-crater-valley-full-zip-200.png` 57,6 KB, `pack-mens-cedar-branch-bib-400.png` 85,5 KB.

## Módulos → as 7 bandas

| Banda (rules §3) | Módulos |
|---|---|
| 2 · Logo | E01 Header |
| 3 · Hero | E02 Hero Photo (duas vozes + filetes) · E03 Hero Statement · E04 Hero Product · E15 Hero Photo Card · E16 Hero Photo Block |
| 4 · Prova ou estrutura (só uma) | E17 Product Cards · E07 Product Rows · E06 Steps · E09 Detail Lines |
| 5 · Mudança de ângulo | E05 Text Block · E10 Feature Photo |
| 6 · Última chamada | E11 CTA |
| 7 · Rodapé | E13 Closing Band + E14 Legal Footer (sempre juntos) |
| Entre bandas | E18 Torn Edge (divisor, não conta como banda) |

**v0.3, rascunho aguardando aprovação** (não usar em e-mail antes do ok do responsável):

| Módulo | Banda | O que é | Referência |
|---|---|---|---|
| E19 Product Cluster | 4 (ou 3, depois do E01) | 3 packshots em leque (o da frente maior e centralizado, dois atrás escurecidos e inclinados, sombra suave) numa imagem única sobre degradê granulado Tap Shoe → Major Brown; título vivo acima em Tap Shoe, corpo + botão abaixo em Major Brown | Duck Camp #3 |
| E20 Technology Bleed | 4 | packshot cortado pela borda direita do e-mail + 3 linhas de tecnologia à esquerda (nome com ® como na p.21, descrição da p.21), filete entre linhas, banda clara quente; no mobile a imagem vem antes (dir=rtl), alinhada à direita, ainda cortada, 220px | Duck Camp #1 |
| E21 Band-Crossing Product | entre bandas (não conta como banda) | produto metade numa banda, metade na seguinte, sobre borda rasgada, tudo numa imagem; amostra Tap Shoe → claro quente (+ gêmea dark) | Habit Sep 2, Duck Camp #4 |
| E22 Photo Collage | 4 ou 5 | fotos em molduras finas claras, fora do eixo 1,4 a 3°, sobrepostas, borda rasgada em duas, sobre Tap Shoe granulado com linhas topográficas; alterna com painéis de texto vivo (título em caixa-alta + 1 ou 2 linhas, filete laranja) | Duck Camp #3 |
| E23 One Product Per Band | 4 | um packshot grande por banda, nome em caixa-alta, bolinhas de cor (células de tabela), 1 linha, preço "$99.99 USD" sublinhado; bandas alternando claro quente e branco | Duck Camp #2 (sem selo NEW: os e-mails da Habit não têm) |

**v0.4, rascunho aguardando aprovação** (rodada 2; não usar em e-mail de envio antes do ok do responsável):

| Módulo | Banda | O que é | Referência |
|---|---|---|---|
| E24 Full-Bleed Photo Hero (texto em cima) | 2 + 3 (abre o e-mail **sem E01**: logo branco `logo-dark.png` sobre a foto, como nos e-mails enviados) | foto de ponta a ponta 600x780, sem card nem raio, texto vivo sobre a área calma: eyebrow, headline em duas vozes (Prompt 800 40/44 + Playfair 900 90/88), subtítulo espaçado, botão; sujeito logo abaixo do botão; base da foto derrete em papel Tap Shoe e rasga para a textura da banda seguinte (assado na imagem). Mobile: 26/30 + 58/60, botão largura total, espaçador 310px, botão termina em cerca de 330px (dentro dos 667). Bloco de texto até cerca de 450px desktop / 380px mobile, senão aumentar o espaçador | Habit Sep 15 e Sep 24, Duck Camp #4 |
| E24B Full-Bleed Photo Hero (texto embaixo) | 2 + 3 | mesma mecânica, para foto cujo sujeito ocupa o topo: logo no topo, texto vivo sobre o degradê da foto para Tap Shoe, rasgo embaixo. Espaçador 350px desktop / 280px mobile; botão dentro dos 667px | Habit Sep 24 |
| E25 Textured Band | 4, 5 ou 6 (substitui o E05 chapado) | banda genérica: eyebrow, headline, subtítulo, 1 ou 2 frases, botão ou link, sobre qualquer textura da tabela de texturas (imagem de fundo + VML + bgcolor). **Uma `<td>` por banda** (outra `<td>` reinicia o tile). Papel claro leva `dm-tex` + classes dm de texto | princípio 1 da rodada 2 |
| E26 Torn Photo | 4 ou 5 (vale como momento de colagem do princípio 5) | foto em moldura fina de papel, rasgada em 1 ou 2 lados, girada 1 a 2°, sombra suave, assada sobre a textura da banda; a imagem **abre** a `<td>` (as linhas da textura coincidem com o fundo), título + 1 linha + link abaixo; gêmea `-dm` em papel claro | Duck Camp #1 e #3 |

O E18 ganhou a versão texturizada (`edge-tex-*.jpg`, tabela de assets da v0.4); a versão lisa (`edge-*.png`) continua para bandas lisas.

**v0.5, rascunho aguardando aprovação** (2026-09-25; e-mails de outubro revisados pelo responsável). Não usar em e-mail de envio antes do ok.

*Mudanças globais aplicadas nos módulos existentes (E01 a E26):*

| Mudança | Onde | O que a revisão substituiu |
|---|---|---|
| Botão texto branco, raio 4px, Prompt 800 17px | os 13 botões da página (E02, E03, E04, E11, E15, E16, E17, E19, E24, E24B, E25 x2, folha) | texto Tap Shoe, raio 6px, Helvetica 16px |
| Corpo, card e rodapé em Prompt 400/500 (fallback Helvetica, Arial) | página inteira | Helvetica/Arial |
| Headline em duas vozes com serifa dominante | E02, E03, E15, E16, E24, E24B (hero 104/94); E05 (serifa primeiro, como WARM / ENOUGH TO SKIP THE JACKET), E11, E17, E19, E22, E25 x3, E26 (100/90); E04, E06, E09, E20 (coluna dividida, 64/60) | palavra serifada no meio de uma headline sans de 34 a 46px |
| Corpo centralizado 17/24 logo abaixo da headline, sem subtítulo espaçado nas bandas internas | E05 (centralizado, um parágrafo + link), E17 (subtítulo virou corpo), E19, E25 x3 (subtítulos tirados, texto fundido no corpo), E26; heroes E02, E03, E04, E15 com corpo 17/24 | subtítulo espaçado em caixa-alta nas bandas internas; corpo 16/26 à esquerda no E05 |
| Texto do card no padrão da caixa de produto | E17 (título laranja 19px, nome 15px, preço 20px branco sem sublinhado) | título branco 20px, preço 16px sublinhado |
| Rodapé com ícone colorido do Instagram | E14 | linha de texto "Follow us on Instagram" sem ícone |
| Amostras de palavra serifada trocadas para caber (≤ 7 letras por linha) | E04 e E24B "FAVORITE" → "FLANNEL", E20 "WEATHER" → "RAIN" | |

*Módulos novos:*

| Módulo | Banda | O que é | Referência |
|---|---|---|---|
| E27 Product Info Box | dentro de E28, E29 ou de qualquer banda escura | caixa centralizada, contorno 1px `#FEF4C6` raio 10px, título laranja 19px, nome branco 15px, variante 13px, preço 20px branco sem sublinhado, bloco inteiro linkado; botão pequeno opcional; amostra 2-up sobre a retícula Major Brown | rev-oct-01 a 05 |
| E28 Checkerboard Product Row | 4 | linhas 300 + 300 sem margem: packshot sobre painel chapado da paleta / caixa E27 sobre Patriot com água, alternando; botão em Patriot depois; mobile empilha com a imagem primeiro | rev-oct-05 |
| E29 Framed Product Card | 4 | card grande de contorno 1px raio 14px: painel de foto 200x330 (packshot em painel chapado ou foto de modelo da loja) + caixa E27, com descrição e botão pequeno opcionais; alterna lado ou tudo à esquerda; mobile empilha, foto em cima | rev-oct-02, rev-oct-04 |
| E30 Photo Closing Band | 6 (última chamada, logo antes do rodapé) | foto de ponta a ponta que derrete em papel Tap Shoe; headline + corpo + botão largo de 420px sobre a parte escura; rasgo assado para o rodapé liso | rev-oct-01, rev-oct-04 |
| E31 Tilted Framed Photo | 5 | foto em moldura branca, 4°, sombra, sobre papel claro; headline em duas vozes à esquerda (serifa Tap Shoe), corpo, botão; gêmea dark | rev-oct-02 |
| E32 Single Review | 5 | um review real (aspas laranja, 5 estrelas, citação centralizada, nome espaçado `#B0A89C`) em papel Tap Shoe, produto sangrando pela direita | rev-oct-01 |
| E33 Label Hero | 2 + 3 (abre o e-mail sem E01) | variante do E24: headline em etiquetas de papel encostadas na borda direita, a última escura com a serifa laranja; subtítulo e botão sobre a base escura; rasgo para a retícula | rev-oct-01 |
| E34 Attribute Grid | 4 | 2x2 cards de contorno com o pictograma oficial da p.21, título laranja com ® exato, descrição da p.21, sobre o degradê Tap Shoe → Patriot Blue topográfico; mobile em 1 coluna | rev-oct-05 |

**v0.6, rascunho aguardando aprovação** (2026-10-07; lote de novembro, aprovado pelo Email QA Reviewer na rodada 3). Não usar em e-mail de envio antes do ok (o lote de novembro usou estes desenhos como variantes, com a ressalva registrada no brief dele).

| Módulo | Banda | O que é | Fonte |
|---|---|---|---|
| E35 Grouped Product Hero | 2 + 3 (abre sem E01) | logo branco, headline em duas vozes, **uma imagem** com 2 a 4 packshots alinhados num chão só, sombra comum e poça de luz (sem leque, sem rotação), subtítulo espaçado, botão; sobre grão (amostra Ivy). Só sem foto de uso da linha (R9) | 01 Women's Cedar Branch (5/11) |
| E36 Framed Collage Hero | 2 + 3 (abre sem E01) | headline, subtítulo, botão, depois colagem de 3 ou 4 fotos emolduradas fora do eixo em papel Tap Shoe que **rasga direto** na banda seguinte (amostra água Patriot), molduras livres do rasgo ou atravessando 40px+ (R11) | 02 Gift Guide #1 (10/11) |
| E37 Split Hero with Model Cut-out | 2 + 3 (abre sem E01) | texto à esquerda (288px), modelo da loja recortado à direita (260px, sem rosto, figura inteira na coluna), pernas cortadas pela borda E18 que faz parte do módulo (fase medida na altura da banda); celular centraliza texto e figura | 03 Buck Hollow 2.0 (19/11) |
| E38 System Shot with Callouts | 4 | headline + corpo, conjunto inteiro como vestido numa imagem em papel claro (+ `-dm`), 4 rótulos em texto vivo com filete laranja apontando a peça; celular: imagem e lista 2x2. Substitui círculo de detalhe quando o detalhe não lê (R7) | 03 Buck Hollow 2.0 (19/11), referência do próprio cliente |
| E39 Detail Mosaic + Colourways | 4 | headline serifa primeiro + corpo, mosaico **reto** (foto de uso 320x300 + 2 detalhes 144), as cores lado a lado num painel Aluminum, legenda das cores, caixa E27, botão | 04 Heavyweight Flannel (27/11) |
| E40 2-up Vertical Product Card | 4 | card 258px de contorno, painel chapado com packshot em cima, título em célula de **altura fixa**, descrição fixa, preço + botão alinhados embaixo (R3); celular empilha | 02 Gift Guide #1 (10/11) |
| E41 Price-Tier Zig-Zag List | 4 (todas as faixas = uma banda de estrutura) | uma banda por faixa de preço, cabeçalho UNDER / $NN, linhas packshot + texto alternando lado (`dir="rtl"`), filete entre linhas; título 19px na retícula também no celular, 17px só em Tap Shoe e Patriot (R4) | 05 Gift Guide #2 (30/11) |

Classes novas de celular (no `<style>` do `<head>`): `v6-tex`, `v6-stack`, `v6-desk` / `v6-mob`, `v6-center`, `v6-mc`, `v6-lead`, `v6-key`, `v6-key-b`, `v6-key-col`, `v6-sub`, `v6-body`, e as `e39-*`, `e40-*`, `e41-*`. A serifa dos módulos novos leva a classe `serif` (Georgia no Outlook, regra acrescentada no bloco MSO do `<head>`).

O que a revisão **substituiu** em módulos antigos (continuam no kit, mas a direção nova prefere o módulo novo): a faixa dividida oliva de fim de e-mail → **E30**; os três reviews → **E32** (um só); o GIF de produto do 04 → **E29** com foto de modelo; a linha de corpo à esquerda do E05 → corpo centralizado.

Composições (leque, sangria, travessia de banda, colagem) são imagem única gerada por `tools/compose.py`, com a cor da banda nas bordas; texto sempre vivo no HTML. A linha de pesca desenhada não entrou em nenhum módulo novo (continua só no E02).

Removidos na v0.2:
- **E08 Proof**: a marca não tem nota nem número de reviews verificado (Diagnostic: "provas que ainda não existem"). Volta só com número e fonte.
- **E12 Letter**: não há pessoa real pra assinar, e retrato de banco sugeriria equipe real (rules §5). Volta só com pessoa confirmada.

Todo texto nos módulos é **amostra**, adaptada dos e-mails enviados e do Strategy Report; cada kit-label diz "SAMPLE COPY, not approved".

## Estratégia aplicada ao e-mail (obrigatório)

Fontes: `strategy/diagnostic-report.md` e `strategy/strategy-report.md`, ambos derivados do Brand Identity Guide (2.4.26) em 2026-09-24.

- **ICPs:**
  - *Weekend Outdoor Adventurer* → quer conforto e versatilidade do mato ao dia a dia; o e-mail mostra uso em família, trilha, camping, e a tecnologia simples (DWR, stretch, wicking).
  - *Passionate Hunter & Weekend Angler* → quer desempenho confiável a preço inteligente; o e-mail mostra campo real, durabilidade, valor.
  - *Hardcore Hunter & Devoted Angler* → quer precisão técnica; o e-mail mostra tecnologia com marca (Rain-Factor®, Scent-Factor®) e uso pesado.
- **Mensagens-chave:** products work hard · outstanding value (sem "figures to prove it") · we listen and respond · hunters but not only · conservationists (ação concreta só com confirmação) · customers are our brand. Tabela com condições no Strategy Report.
- **Frase-âncora:** "Our Gear, Your Adventure." · status **em uso** (etiquetas), caixa a confirmar. Variações "Our Gear, your {x}." são **propostas**.
- **Tom:** de igual pra igual, direto, concreto, humor seco; nunca por cima, nunca se gabando, nunca fresco.
- **Red flags:** marca de preço baixo, clube fechado de caçador, arrogância técnica ou número sem fonte, jargão, lifestyle de estúdio, imprudência ambiental, urgência falsa.
- **Provas que existem hoje:** nomes e textos das tecnologias (p.21), presença no varejo dos EUA (qualitativo), história do fundador, frete grátis acima de $100 (site em 2026-09-24).
- **Provas que ainda não existem:** qualquer número de desempenho, "selling out nationwide", comparação com concorrente, **nota média e número de reviews**, detalhe atual da parceria de conservação.
- **Prova que passou a existir (2026-09-25):** reviews individuais reais, com nome e 5 estrelas, no copy-source de outubro do cliente (`03-work/email/2026-10-broadcasts/copy-source.md`). Uso no E32: texto e nome exatos, um por e-mail, só o que o cliente mandar. Nota média e contagem continuam proibidas.

## Regras só desta marca

Complementam `email-ops/rules.md`.

- **Foto:** produto em uso real em paisagem natural, pessoas espontâneas; close de detalhe e plano aberto (guia p.19). Nada de estúdio como hero.
- **Logo:** Aluminum em fundo claro, branco em fundo escuro ou foto escura e limpa; nunca recolorido, nunca sobre foto carregada (p.13-16). Laranja do site: [[CONFIRMAR]].
- **Cor por linha:** Violet Dusk só em e-mail/bloco Women's; Yellow Plum só em Youth (p.17, p.23).
- **Tecnologia:** nome com ® / ™ exatamente como na p.21, descrição curta da p.21. Número (UPF 50+) só por produto, com a ficha.
- **Moeda / preço / prazo:** USD; preço e frete só da loja no dia do envio.
- **Assinatura:** "The Habit team" (equipe fala em "we"). Pessoa real só com confirmação.
- **Rede social:** Facebook (facebook.com/HabitOutdoors) e Instagram (@habitoutdoors), ambos linkados no site. Checar se estão ativos.
- **Revisão jurídica:** não regulada; o cliente aprova claims de produto.
- **Recursos visuais candidatos a módulo:** padrão topográfico sobre Aluminum, faixa diagonal laranja/marrom/oliva como divisor de rodapé, "//" em rótulo, ícones de tecnologia.

## Em aberto

- [[CONFIRMAR]] **Aprovar os HEX amostrados** do PDF (tabela em `identity/brand-guidelines.md`).
- ~~Laranja do botão~~: decidido 2026-09-24, `#FF6400` com texto Tap Shoe `#2A2B2D`. **Substituído em 2026-09-25:** texto branco (exceção AA registrada, v0.5).
- **v0.5, perguntas para o responsável:**
  - ~~Painéis ferrugem e ardósia da rev-oct-02~~: **fechado em 2026-09-25.** O desenho revisado do responsável usa as duas; entram no kit como cor de painel de produto (só atrás de packshot, sem texto) com os valores medidos usados no e-mail, `#774727` e `#4F5C5F` (a anotação anterior, `#794928` / `#4F5B5E`, fica substituída). Tabela de cor e `tokens.json` atualizados.
  - **Ícones do E34:** a revisão desenhou ícones de traço fino; o kit usa os pictogramas oficiais da p.21 do guia (mais grossos), com as barras em laranja. Qual vale?
  - **Filetes laranja duplos do E02:** nenhum dos 5 e-mails revisados usa. Saem do E02?
  - **Variantes do E28** ("Veil Wideland Wolf", "Mossy Oak Terra Coyote") lidas do código do arquivo de imagem da loja (`VEIL_WIDELAND_WOLF`, `MO_COYOTE`): conferir o rótulo exato da loja.
  - Fotos originais `orig-hunt22` e `orig-hunt40` (E33, E30): [[CONFIRMAR]] liberadas para e-mail.
  - E32: a rev-oct-01 põe a parka ao lado de um review do bib; o kit usa o bib (o produto de que o review fala). Confirmar.
  - As mudanças globais já estão nos módulos aprovados E01 a E18. Aprovar a v0.5 também reaprova esses módulos com o botão branco e a headline nova.
- **v0.6, perguntas e pendências para o responsável:**
  - Aprovar E35 a E41 (as variantes que o lote de novembro usou) e o bloco de regras R1 a R15.
  - **Subtítulo espaçado em banda interna:** a v0.5 diz "só no hero", mas o copy do cliente traz subheadline em bandas internas e o lote de novembro a colocou como caixa-alta espaçada (copy literal, R12). As amostras E38 e E39 seguem a v0.5 (sem subtítulo). Qual vale quando o cliente manda subheadline?
  - **Título laranja sobre a água Patriot a 17 a 19px** (E28, E40, E41): a tabela de texturas pede 24px nessa textura (4,0:1 no pior caso), mas o próprio E28 da rev-oct-05 usa. Registrar como exceção do responsável, como o botão?
  - **PNG em paleta que sobrou (R5):** `pack-mens-heavyweight-soft-flannel-360.png` (E04) e `pack-mens-cedar-branch-parka-400.png` (E17) dariam 192 e 184 KB em PNG-24; `e23-crater-valley-hoodie.png` e `e23-cedar-branch-bib.png` (E23) dariam 657 e 300 KB. Solução: JPG assado na cor da banda (+ `-dm` onde a banda troca no escuro), o que muda o `src` (e o markup do E23): pede ok por mexer em módulo aprovado.
  - **Farelos grandes dentro de composições (R6):** os rasgos assados em E21, E24, E24B, E26, E30 e E33 ainda têm os pontos de 2,4 a 4,8px. Refazer exige rodar de novo os jobs de foto do `compose.py` / `compose_v05.py` com o farelo fino.
  - **E35 no e-mail 01 de novembro:** o `<img>` do hero declara `height="350"`, mas o arquivo é 1200x760 (exibe 380): o Outlook achata a imagem. Corrigido no kit (E35 com `height="380"`); no lote de novembro, corrigir no `build_emails.py` antes da exportação.
  - Liberação das fotos `crop-sent-*` (colagem do E36, estábulo do E39) e originais de detalhe do Buck Hollow (para voltar aos círculos com R7).
- **R8 de 2026-10-08 nos módulos antigos:** E24, E24B e E30 (e as amostras `e24-hero-*.jpg`, `e30-closing-hunter.jpg`) ainda descrevem e assam a foto derretendo em papel Tap Shoe. O lote de novembro já segue a R8 nova (rodada 6); refazer esses módulos do kit com rasgo na próxima revisão do kit (não feito: a rodada 6 não mexe em módulo do kit).
- **Tipografia:** provisória no kit (Prompt 800 + Playfair Display 900 + Helvetica); o responsável fecha a tipografia no Figma.
- [[CONFIRMAR]] ESP (Omnisend?) e sintaxe de merge.
- [[CONFIRMAR]] Endereço físico do rodapé (Mahco, 1202 Melissa Drive, Bentonville, AR 72712?).
- [[CONFIRMAR]] Banco de fotos aprovado e packshots.
- [[CONFIRMAR]] Endereço e descadastro no rodapé: não aparecem nos prints. O ESP acrescenta?
- [[CONFIRMAR]] Headline em imagem (exceção) ou texto vivo.

## Changelog

- 2026-10-08: **R8 reescrita (decisão do responsável na rodada 6 do lote de novembro):** fim do degradê/derretido de foto para banda; toda transição de foto é rasgo ou textura orgânica; escurecimento leve dentro da foto sob o texto permitido; recorte próprio de celular mantido. Espelhada no rótulo R8 do bloco "Production rules learned (v0.6)" do `components.html` (só o texto do rótulo). Módulos E24, E24B e E30 ficam em "Em aberto" para refazer.
- 2026-10-07: **v0.6 draft: E35-E41 + "Production rules learned (v0.6)", pending approval with v0.5.** Fonte: lote de novembro (`03-work/email/2026-11-broadcasts/`, brief rodadas 2 e 3, `qa-r1.md`, `qa-r2.md`). `components.html` (editado à mão por script de inserção entre os marcadores, sem `build_kit.py`): bloco de regras R1 a R15 logo depois da KIT SHEET (só revisão); cabeçalho "V0.6 DRAFT · PENDING APPROVAL" depois do E34 com E35 Grouped Product Hero, E36 Framed Collage Hero, E37 Split Hero with Model Cut-out (com a borda E18 de fase medida), E38 System Shot with Callouts, E39 Detail Mosaic + Colourways, E40 2-up Vertical Product Card, E41 Price-Tier Zig-Zag List; classes de celular `v6-*`, `e39-*`, `e40-*`, `e41-*`; `.serif` (Georgia) no bloco MSO; eyebrow da KIT SHEET e comentário do topo atualizados. Melhorias sobre o e-mail de origem: E37 com a figura centralizada no celular (WARN do QA r2), E35 com `height="380"` correto (o 01 declara 350), E39 com a margem do segundo quadrado em classe própria. Correções de defeito descritas pelas regras, **sem mudar estrutura**: R2 `&nbsp;` nas duas últimas palavras dos títulos de produto do E07 e do E17 (aprovados) e do E27, E28 e E29 (v0.5); R6 as 31 bordas `edge-tex-*` regravadas com farelo fino; R5 três packshots (`pack-mens-heavyweight-soft-flannel-200`, `pack-mens-crater-valley-full-zip-200`, `pack-mens-cedar-branch-bib-400`) em PNG-24, usados no E07 e E17 aprovados. Script novo `tools/compose_v06.py` (jobs `copy`, `edges`, `packs`; importa `compose.py` e `compose_v05.py` sem alterar). 16 imagens novas, 857,8 KB. `lint_layout.py` do lote limpo nos módulos novos a 600 e 375; renders 680 / 375 / escuro conferidos. `tokens.json` sem mudança (nenhum valor novo: os módulos usam só cores e texturas já registradas).

- 2026-09-25: **v0.5, cores de painel.** `color.panel_rust` `#774727` e `color.panel_slate` `#4F5C5F` (rev-oct-02, medidas) entram como cor de painel de produto; pergunta em aberto fechada. `tokens.json` espelhado. Ícone do Instagram do E14 registrado em 44px (era 36 no texto).
- 2026-09-25: **v0.5 draft: mudanças globais + E27-E34 + 3 superfícies, pending approval.** Fonte: e-mails de outubro revisados pelo responsável (`references/rev-oct-01..05-*.png`, `03-work/email/2026-10-broadcasts/revision-r2.md`). Globais em todos os módulos do `components.html`: botão texto branco `#FFFFFF`, raio 4px, Prompt 800 17px (exceção AA 2,97:1 registrada como escolha do responsável, substitui a decisão de 2026-09-24); corpo, card e rodapé em Prompt 400/500 (Google Fonts agora com o peso 400); headline em duas vozes com Playfair 900 dominante (100/90, hero 104/94, coluna 64/60; mobile 64/58, sans 30/32 e 22/24; classes `hl-lead`, `hl-key`, `hl-key-s`); corpo de banda 17/24 centralizado, subtítulo espaçado só no hero; E17 no padrão da caixa de produto; E14 com o ícone do Instagram; folha do kit atualizada. Novos E27 Product Info Box, E28 Checkerboard Product Row, E29 Framed Product Card, E30 Photo Closing Band, E31 Tilted Framed Photo, E32 Single Review, E33 Label Hero, E34 Attribute Grid. Superfícies novas `tex-paper-camo.jpg` (+ `-dm`, classe `dm-tex-camo`), `tex-halftone-brown.jpg`, `grad-tapshoe-to-patriot-topo.jpg`, com fallback e contraste medido; 7 bordas E18 novas. Script novo `tools/compose_v05.py` (importa `compose.py`, que ficou intocado). `tokens.json`: `meta.kit_version` 0.5, `color.on_primary` `#FFFFFF`, `font.family_css` Prompt, grupos novos em `type`, `button`, `radius`, `assets.v05_draft`, `textures_v05`. Para voltar à v0.4: git (commit bd51089).

- 2026-09-24: **v0.4 draft: E24-E26 + texture set pending approval.** Rodada 2 (art-direction-r2.md). Banco de fotos: 17 recortes `crop-sent-*` em `photos/lifestyle/` + INDEX.md (`tools/crop_sent.py`; imagens extras da loja revisadas, nenhuma em locação). 11 texturas 1200x1600 abaixo de 90 KB (8 tiles sem emenda, 3 degradês) com fallback e contraste registrados; 24 bordas E18 texturizadas com gêmeas -dm; novos E24 e E24B Full-Bleed Photo Hero, E25 Textured Band, E26 Torn Photo; folha de texturas na página do kit; dark mode `.dm-tex`. `compose.py`: `make_texture_set`, `compose_full_bleed_hero`, `compose_torn_photo`, `compose_torn_edge_textured`, `tear_shadow` (jobs antigos inalterados, saída idêntica). `tokens.json` ganhou `textures_v04`.
- 2026-09-24: **v0.2.1** (QA rodada 1). E17: o contorno do card passou para a própria célula da linha (cards da mesma linha sempre com a mesma altura, conferido com nome em 2 linhas) + célula de gutter de 16px. E15: o card mede 600px nos navegadores (height 552 + padding 48), então o VML de 600 estava certo; o atributo `height` da célula passou a 600 para o Outlook (que zera o padding); mobile com 392px renderizados (356 + 36) e 24px acima do corpo, botão a cerca de 654px contando o E01.

- 2026-09-24: **v0.3 draft: E19-E23 pending approval.** Novos E19 Product Cluster, E20 Technology Bleed, E21 Band-Crossing Product, E22 Photo Collage, E23 One Product Per Band; texturas `tex-tapshoe-grain.jpg` e `grad-tapshoe-brown.jpg`; script `tools/compose.py`. Troca só de conteúdo nos aprovados: E04, E07 e E17 com packshots, nomes e preços reais do catálogo (E09 não mostra preço, ficou igual); `product-flannel.png` apagado; `tokens.json` → `assets` atualizado. Estrutura de E01 a E18 inalterada.
- 2026-09-24: kit v0.2 lapidado à mão (não regenerar com build_kit.py). Caixa-alta real em headline e botão (tracking 2px); texto de amostra no tom Habit; E02 com headline em duas vozes + dois filetes laranja; regra de contraste do laranja aplicada (só texto em Tap Shoe/Patriot Blue, grande em Major Brown); E15 com foto nova `card-fishing.jpg` e texto branco; E07 só produto; novos E17 Product Cards e E18 Torn Edge; rodapé no padrão dos e-mails (logo empilhado, menu com SALE, Instagram, um copyright); E08 e E12 removidos; E11 sem variantes de cor, em Patriot Blue; dark mode: muted `#B0A89C`, link claro sublinhado.

- 2026-09-24: kit v0.2 aprovado. Rodapé termina no copyright, sem merge de nome, textura escura apagada, catálogo da loja como fonte de produto. 4 referências Duck Camp analisadas.
- 2026-09-24: tokens.json v0.1 preenchido (cores dos e-mails enviados, botão #FF6400 com texto Tap Shoe, caixa-alta, raio 6px); fonte provisória combo A até a escolha na página de teste https://claude.ai/artifact/5gRnMYHKZAHUCKPneuPXpo.
- 2026-09-24: 5 e-mails enviados analisados; botão 6px de raio, logo só logotipo no header, rodapé Tap Shoe.
- 2026-09-24: HEX amostrados do vetor da p.17 e logo extraído do vetor da p.14 para `identity/logo/`.
- 2026-09-24: kit criado; Mapa, Estratégia aplicada e Regras preenchidos a partir do Brand Identity Guide e do site.
