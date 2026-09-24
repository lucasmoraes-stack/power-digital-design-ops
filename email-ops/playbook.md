# Playbook: operação de e-mail

Como a operação faz qualquer e-mail (campanha, fluxo de boas-vindas, recompra, newsletter), pra qualquer marca. **Todo pedido de e-mail segue este fluxo.** Regras técnicas e de craft em [`rules.md`](rules.md). A lista de tudo que precisa existir, item por item, está em [`CHECKLIST.md`](CHECKLIST.md).

## A ideia em uma frase

O e-mail é desenhado em **HTML de e-mail de verdade**, a partir de um **kit da marca aprovado uma vez**, alimentado por **três fontes da marca** (Diagnostic Report, Strategy Report, style guide), com **referências** e **regras** anexadas. Ferramenta de layout (Figma) é destino opcional no fim, se o cliente precisar.

## As três fontes obrigatórias da marca

Nada avança sem as três. Sem uma delas, parar e avisar o responsável pelo projeto.

| Fonte | O que o e-mail tira dela | Alimenta no kit |
|---|---|---|
| **Diagnostic Report** (Negócio, Audiência, Valor, Estória) | Objetivo do projeto, ICPs (quem cada e-mail serve, o que teme, o que precisa), diferenciais reais, provas que existem e as que não existem, pontos de atenção (regulatório, dívida técnica do site/checkout) | README do kit, seção "Estratégia aplicada ao e-mail": ICPs, provas |
| **Strategy Report** (promessa, personalidade e valores, oportunidades e mensagens, posicionamento) | Tom (we do / we don't), red flags, mensagens-chave e **quando cada uma pode ser usada**, frase-âncora e o status de validação dela | README do kit: mensagens, frase-âncora, tom, red flags; texto de amostra dos módulos |
| **Style guide / toolbox visual** (Figma, PDF de guideline, site no ar) | Cor, tipografia, logo vetorial, regra de fotografia, banco de fotos aprovado, recursos visuais recorrentes | `tokens.json`, `assets/`, regra de foto no README do kit |

Mais uma fonte, obrigatória em marca regulada: o **documento de voz e compliance** (régua legal). Ele manda acima de tudo (rules §0).

Regras de uso das fontes:
- Report que só existe numa ferramenta de design: salvar um retrato datado (`{marca}/strategy/reports/{report}-{aaaa-mm-dd}.png`) ou o texto de registro, pra o agente ler do repo.
- **Frase-âncora ou mensagem marcada como "proposta/não validada" não vira headline**, nem texto fixo do kit (ex.: frase do rodapé): entra só como direção de tom.
- **Mensagem condicionada** ("use só quando o sistema pós-compra existir") respeita a condição.
- Report x kit: o report manda na mensagem e no tom, o kit manda no visual. Report x régua legal: a régua manda.

## Onde cada coisa mora

A operação (este pacote) e as marcas ficam separadas. O pacote nunca contém dado de marca.

```
email-ops/                        o pacote (no repo do estúdio: _studio/email-ops/)
  README.md                       comece aqui: onboarding, agentes, instalação
  CHECKLIST.md                    tudo que precisa existir, do setup ao envio
  playbook.md                     este fluxo
  rules.md                        regras de todo e-mail
  templates/email-base.html       esqueleto HTML de e-mail
  templates/flow-brief.md         molde do brief de fluxo
  templates/email-kit/            molde de kit: README, tokens.json, components.template.html, assets/, references/
  tools/                          build_kit.py, render.py, build_preview.py, export.py
  install/CLAUDE-snippet.md       trecho pra colar no CLAUDE.md de outro projeto

{pasta da marca}/                 onde a marca mora no projeto (qualquer caminho)
  ...Diagnostic Report, Strategy Report, style guide, voz e compliance
  email-kit/                      o kit da marca (copiado do molde e preenchido)
    README.md                     porta de entrada: status, Mapa da marca, tokens, estratégia, regras só da marca
    tokens.json                   valores da marca
    components.html               biblioteca de módulos + página de revisão (gerada e depois lapidada)
    assets/                       logo claro/escuro, fotos recortadas, texturas, produtos
    references/                   e-mails de referência + README do que aproveitar
  {pasta de e-mails}/{fluxo}/
    brief.md                      brief do fluxo
    {nn}-{slug}.html              os e-mails
  {pasta de entregas}/{fluxo}/    versão final pro ESP
```

O **Mapa da marca** (tabela no topo do `email-kit/README.md`) diz o caminho real de cada item acima naquela marca. Os agentes leem o mapa primeiro; por isso o pacote funciona em qualquer estrutura de projeto.

## Quem faz o quê

| Agente | Papel |
|---|---|
| **Email Designer** (`design-email-designer`) | Monta o kit da marca (etapa 1) e constrói os e-mails a partir dele (etapa 4) |
| **Email QA Reviewer** (`design-email-qa-reviewer`) | Gate técnico, de marca e de compliance antes de qualquer e-mail sair (etapa 6) |
| **Email Marketing Strategist** (`marketing-email-strategist`) | Só quando o pedido envolve estratégia de fluxo: gatilho, cadência, segmento, métricas |
| Content Creator (`marketing-content-creator`), se existir no projeto | Só quando o copy não veio pronto do cliente. Sempre com o documento de voz da marca |
| Legal Compliance Checker (`support-legal-compliance-checker`), se existir no projeto | Marca regulada, junto da régua da marca |

O **responsável pelo projeto** (a pessoa que toca a marca) aprova o kit, o primeiro e-mail de cada fluxo e as exceções de regra, e fala com o cliente.

---

## Etapa 0: entrada

- **O que fazer:** triagem da §1 das regras (marca, tipo, mensagem única, oferta, CTA, público, assets, ESP e destino) e confirmar de onde vem o copy (cliente, nosso, a escrever). O que faltar, perguntar antes de desenhar.
- **Por quê:** o ESP define a sintaxe de merge field; o destino define se precisa de slices; a mensagem única define o hero.
- **Trava em:** marca sem as três fontes. Aí para e pede.

## Etapa 1: kit da marca (uma vez por marca)

- **O que fazer:**
  1. `python email-ops/tools/build_kit.py --init {pasta da marca}/email-kit` copia o molde.
  2. Preencher o **Mapa da marca** no README do kit.
  3. Preencher `tokens.json` a partir do style guide (cor, fonte, raio, caminhos de asset), registrando a fonte de cada valor no README.
  4. Preparar `assets/` conforme `assets/README.md` (logo claro e escuro rasterizado do vetor, fotos recortadas 2x, texturas em JPG).
  5. Preencher "Estratégia aplicada ao e-mail" a partir dos dois reports.
  6. `python email-ops/tools/build_kit.py {pasta da marca}/email-kit` gera o `components.html`.
  7. Lapidar os módulos pra marca (texto de amostra no tom do Strategy Report, recursos visuais próprios). O Email Designer faz isso no Modo A.
- **Revisão:** o `components.html` é publicado como página e o responsável revisa módulo por módulo ("ok" / "ajustar").
- **Por quê:** é o passo que mais economiza retrabalho. Kit bem feito = e-mail sai certo na primeira.
- **Trava em:** fonte oficial da marca. Nunca usar token de componente genérico ou de wireframe como se fosse a cor real. Sem style guide: extrair do site no ar e marcar "extraído, não oficial" no README do kit.
- **Saída:** README do kit com status **aprovado**, data e quem aprovou. Sem isso, não existe etapa 4.

## Etapa 2: referências

- **O que fazer:** 2 a 4 e-mails de referência em `email-kit/references/` (print ou HTML), com uma linha cada no README dizendo **o que aproveitar**: estrutura, ritmo, tipo de módulo.
- **Não colar o HTML da referência no chat** (páginas salvas de galerias de e-mail passam de 1MB e estouram o prompt). Salvar na pasta e renderizar com `tools/render.py` pra estudar a imagem.
- **Regra de ouro:** referência de outra marca é referência de **estrutura**, nunca de paleta, tipografia ou layout copiado.

## Etapa 3: brief do fluxo

- **O que fazer:** copiar `templates/flow-brief.md` pra `{pasta de e-mails}/{fluxo}/brief.md` e preencher: por e-mail, **ICP** (com medo e necessidade), **mensagem-chave** do Strategy Report (e se a condição dela está cumprida), mensagem única, tipo, gatilho, **assunto (até 50 caracteres) + preheader**, copy (fonte ou texto), CTA + URL, cor de botão, bandas planejadas com o módulo do kit de cada uma, desvios do copy-fonte, dados a confirmar.
- **Por quê:** deixa claro antes de desenhar o que cada e-mail faz de diferente dos outros do fluxo, e é o registro de cada decisão.
- **Trava em:** copy com claim sem fonte. Fica `[[CONFIRMAR]]`.

## Etapa 4: construção

- **O que fazer:** o Email Designer recebe kit aprovado + regras + referências + brief e monta `{fluxo}/{nn}-{slug}.html`, **só com módulos do kit**, partindo de `templates/email-base.html` ou do `<head>` do `components.html` da marca. Um e-mail por vez; o primeiro do fluxo é aprovado antes dos outros.
- **Por quê:** o primeiro e-mail aprovado vira a régua dos seguintes.
- **Trava em:** módulo que não existe no kit. Aí o módulo entra no kit primeiro (volta à revisão da etapa 1, só daquele módulo).

## Etapa 5: revisão por seção

- **O que fazer:** `python email-ops/tools/build_preview.py {pasta de e-mails}/{fluxo} --notes notas.md` gera uma página única (desktop 600px + mobile 375px lado a lado, aba por e-mail, assunto e preheader). Publicar como página e o responsável comenta seção por seção; o ajuste é feito na seção apontada, sem refazer o resto. Cada rodada registra o que mudou nas notas.
- **Por quê:** o arquivo continua no repo e o que se revisa é o que se envia.

## Etapa 6: QA

- **O que fazer:** o Email QA Reviewer roda o checklist completo (técnico, marca, compliance) e o render de verificação (`tools/render.py` em 680px, 375px e `--dark`). Marca regulada: régua legal + revisão jurídica do cliente antes de enviar.
- **Trava em:** qualquer item bloqueante. E-mail não passa com pendência "depois a gente vê". Pendência de envio (endereço, URL, jurídico) fica listada à parte e trava a etapa 7.

## Etapa 7: exportação e envio

Duas rotas; o padrão é a (a).

- **(a) HTML direto pro ESP** (recomendada): copiar pra `{pasta de entregas}/{fluxo}/`, subir as imagens no ESP/CDN, trocar caminhos relativos por URLs absolutas, trocar os placeholders de link e o merge field pela sintaxe do ESP, zerar `[[CONFIRMAR]]`, enviar teste pra Gmail (web + app), Outlook desktop e Apple Mail, e rodar num serviço de preview (Litmus ou Email on Acid) quando houver fundo com imagem.
- **Cópia editável no Figma** (pra o cliente ou o time editar/aprovar lá, sem mudar a rota de envio): via Figma MCP, `generate_figma_design`.
  1. Fazer cópias de trabalho dos e-mails fora do repo, com as imagens embutidas (data URI) e `<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>` antes do `</head>`.
  2. Servir a pasta localmente (`python -m http.server 8765`); `file://` não funciona.
  3. Pedir um capture ID por e-mail (`generate_figma_design` com o `fileKey`; IDs são de uso único).
  4. Abrir cada e-mail com `#figmacapture={id}&figmaendpoint={endpoint}&figmadelay=2500&figmaselector=.container` numa janela de 680px (Chrome headless serve). O seletor `.container` captura só o bloco de 600px, sem o fundo da página.
  5. Consultar o mesmo ID até `completed`.
  6. Organizar no arquivo: página própria, frames lado a lado, blocos renomeados com o ID do módulo, rótulo com assunto e preheader.
  - Resultado: frames com texto, cor e imagem editáveis, mas estrutura de "Table Cell" e sem componentes nem auto-layout. É cópia de revisão: **o HTML continua sendo a fonte**, e mudança feita no Figma precisa voltar pro HTML.
- **(b) Figma + slices** (quando o cliente exige editar no Figma ou o ESP só aceita imagem): importar o HTML no Figma (como acima, ou plugin html.to.design), fatiar com a ferramenta Slice (cada fatia até **1000px de altura**, corte novo sempre que o link de destino mudar), exportar em 2x, comprimir, subir no ESP como imagens sem padding, com link em cada fatia. Custa acessibilidade e dark mode: avisar o cliente.

## Etapa 8: depois do envio

- Registrar no brief: data de envio, versão enviada, métricas da primeira semana (abertura com ressalva do Apple MPP, clique, CTOR, descadastro, reclamação).
- Levar pro kit o que o fluxo ensinou (módulo novo aprovado, variante, correção técnica) e anotar no changelog do kit.

---

## Checklist rápido pra quem pede "faz um e-mail"

0. A marca tem Diagnostic Report, Strategy Report e style guide no projeto? Se não, parar e avisar.
1. A marca tem `email-kit/` **aprovado**? Se não, etapa 1 primeiro.
2. Tem referências no kit? Se não, pedir 2-4.
3. Existe brief do fluxo? Se não, escrever antes de desenhar.
4. Construir o primeiro e-mail, gerar o preview, iterar, QA, e só então os próximos.
