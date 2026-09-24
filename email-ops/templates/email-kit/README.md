# {Marca} · Email kit

> Molde de kit. `python email-ops/tools/build_kit.py --init {pasta da marca}/email-kit` copia esta pasta; depois preencher cada seção abaixo **na ordem**. Apagar esta nota e os textos entre `{ }` quando preenchido. Fluxo: `email-ops/playbook.md` · Regras: `email-ops/rules.md` · Checklist: `email-ops/CHECKLIST.md`, parte C.

## Status

| | |
|---|---|
| Status | **rascunho** · {aprovado em aaaa-mm-dd por {nome}} |
| Responsável pelo projeto | {nome} |
| Fonte visual oficial | {Figma: arquivo, fileKey, página e node / PDF de guideline / site} |
| Oficial ou extraído | {oficial / extraído do site, confirmar com o cliente} |
| ESP | {nome} · merge: {ex.: `{{ first_name \| default: "there" }}`} |
| Idioma do conteúdo | {ex.: inglês, mercado dos EUA} |
| Página de revisão do kit | {link} |

## Mapa da marca

**Os agentes leem esta tabela primeiro.** Caminho real de cada item neste projeto (relativo à raiz do projeto). Linha vazia = item não existe ainda; se for **[trava]**, parar.

| Item | Caminho | Status |
|---|---|---|
| Diagnostic Report **[trava]** | {ex.: marcas/x/strategy/diagnostic-report.md} | {refinado em data / rascunho} |
| Strategy Report **[trava]** | {…} | {…} |
| Style guide / toolbox **[trava]** | {arquivo ou link + node} | {oficial / extraído} |
| Voz e compliance {**[trava]** em marca regulada} | {…} | |
| Contexto geral da marca | {…} | |
| Banco de fotos aprovado | {pasta} | |
| Packshots de produto | {pasta} | |
| Logo vetorial | {arquivo} | |
| Pasta de e-mails (trabalho) | {ex.: marcas/x/emails/} | |
| Pasta de entregas (final) | {ex.: marcas/x/entregas/emails/} | |

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

Valores em `tokens.json`. Esta tabela registra **de onde veio** cada um.

### Cor

| Token | Hex | Uso | Fonte | Contraste |
|---|---|---|---|---|
| `color.primary` | | botão padrão, link, destaque | | sobre branco: |
| `color.text` | | título | | |
| `color.text_muted` | | corpo | derivado | |
| `color.surface` / `color.surface_alt` | | bandas claras | | |
| `color.dark` | | banda escura, rodapé | | |
| `color.accent_1` / `color.accent_2` | | acento por e-mail | | com texto: |
| `color.line` / `color.page` | | filete, fundo da página | derivado | |

Dark mode: {valores, todos derivados da paleta}.

### Tipografia

| Papel | Tamanho desktop / mobile | Peso | Nota |
|---|---|---|---|
| Display (hero) | | | {itálico de destaque?} |
| Título de banda | | | |
| Título de item | | | |
| Corpo | 16/26 | | |
| Label / eyebrow | 12/16, tracking 2px, caixa-alta | | |
| Legal | 12/18 | | |

Família e fallback: {web font + pilha inline + fallback do Outlook}. **Regra de caixa:** {sentence case / Title Case}.

### Botão e espaçamento

Botão: {raio, padding, altura, cor padrão e variantes}. **Uma cor de botão por e-mail.** Espaçamento: escala 8pt, gutter 40px desktop / 24px mobile, banda 48-64px vertical (40px mobile).

## Assets

| Arquivo | Uso | Origem |
|---|---|---|
| `assets/logo-light.png` · `logo-dark.png` | header claro / fundo escuro e dark mode | vetor {arquivo} |
| | | |

## Módulos → as 7 bandas

| Banda (rules §3) | Módulos |
|---|---|
| 2 · Logo | E01 Header |
| 3 · Hero | E02 Hero Photo · E03 Hero Statement · E04 Hero Product · E15 Hero Photo Card · E16 Hero Photo Block |
| 4 · Prova ou estrutura (só uma) | E06 Steps · E07 Photo Rows · E08 Proof · E09 Detail Lines |
| 5 · Mudança de ângulo | E12 Letter · E10 Feature Photo · E05 Text Block |
| 6 · Última chamada | E11 CTA |
| 7 · Rodapé | E13 Closing Band + E14 Legal Footer (sempre juntos) |

Remover da tabela o que a marca não usa; módulo novo entra aqui só depois de aprovado.

## Estratégia aplicada ao e-mail (obrigatório)

Fontes: {links pro Diagnostic Report e Strategy Report, com data da versão}.

- **ICPs:** {nome do arquétipo → o que precisa, o que teme, que e-mails serve, o que o e-mail pra ele sempre mostra}
- **Mensagens-chave:** {texto → quando pode ser usada; condição cumprida hoje? sim/não}
- **Frase-âncora:** {texto} · status {validada / proposta}
- **Tom:** {we do / we don't}
- **Red flags:** {o que o e-mail nunca pode parecer}
- **Provas que existem hoje:** {dado + fonte + data}
- **Provas que ainda não existem:** {o que não pode ser dito ainda}

## Regras só desta marca

Complementam `email-ops/rules.md`. Apontar pro documento de origem.

- **Foto:** {regra}
- **Moeda / preço / prazo:** {regra}
- **Assinatura:** {equipe ou pessoa real confirmada}
- **Rede social:** {ativas}
- **Revisão jurídica:** {quem, quando}
- {outras}

## Em aberto

- [[CONFIRMAR]] {item}

## Changelog

- {aaaa-mm-dd}: {mudança}
