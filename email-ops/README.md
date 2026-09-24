# Operação de e-mail

Pacote completo pra desenhar e entregar e-mail (campanha, fluxo, newsletter) pra **qualquer marca**, em **qualquer projeto**. Tem o método, as regras, os moldes, as ferramentas e os agentes. Não tem dado de marca nenhuma: cada marca entra com o próprio kit, alimentado pelas fontes dela.

## Comece aqui (pessoa nova na operação)

Leia nesta ordem, uns 30 minutos:

1. Este README.
2. [`playbook.md`](playbook.md): o fluxo em 8 etapas, quem faz o quê.
3. [`CHECKLIST.md`](CHECKLIST.md): tudo que precisa existir, do setup ao envio. É a sua lista de trabalho.
4. [`rules.md`](rules.md): as regras de todo e-mail. Os agentes seguem; você revisa com elas.
5. [`templates/email-kit/README.md`](templates/email-kit/README.md): o molde do kit, com as regras de como alimentá-lo.

## Como a operação funciona

```
Diagnostic Report ─┐
Strategy Report ───┼──►  EMAIL KIT da marca  ──►  brief do fluxo  ──►  e-mails HTML  ──►  preview  ──►  QA  ──►  ESP
Style guide ───────┘     (tokens, assets,         (1 por fluxo)        (só módulos       (revisão por
(+ voz e compliance)      módulos, estratégia)                          do kit)           seção)
```

- **As três fontes da marca são obrigatórias.** Sem Diagnostic Report, Strategy Report e style guide, a operação não começa: o kit depende das três.
- **O kit é montado uma vez por marca** e aprovado pelo responsável. Depois disso, todo e-mail sai dele.
- **O e-mail é HTML de verdade**: o que se revisa é o que vai pro ESP.
- **O README do kit é a porta de entrada da marca.** A tabela "Mapa da marca" diz onde está cada fonte naquele projeto. É por isso que o pacote funciona em qualquer estrutura de pastas.

## O que tem no pacote

| Caminho | O que é |
|---|---|
| `README.md` | este onboarding |
| `CHECKLIST.md` | checklist completo, com o que trava cada etapa e quem faz |
| `playbook.md` | o fluxo, etapa por etapa |
| `rules.md` | regras técnicas, de estrutura, conversão e copy |
| `templates/email-base.html` | esqueleto HTML de e-mail |
| `templates/flow-brief.md` | molde do brief de fluxo |
| `templates/email-kit/` | molde de kit: `README.md` (com as regras de alimentação), `tokens.json`, `components.template.html` (15 módulos), `assets/` (amostras neutras + especificação), `references/` |
| `tools/` | scripts (abaixo) |
| `install/CLAUDE-snippet.md` | trecho pra colar no `CLAUDE.md` de outro projeto |

## Agentes

Ficam em `.claude/agents/` do projeto (um arquivo por agente, compartilhados por todas as marcas; o que muda de marca pra marca é o kit, nunca o agente).

| Agente | Arquivo | Quando chamar |
|---|---|---|
| **Email Designer** | `design-email-designer.md` | Montar o kit (Modo A) e construir os e-mails (Modo B) |
| **Email QA Reviewer** | `design-email-qa-reviewer.md` | Antes de qualquer e-mail sair: veredito PASS/BLOCK com correção por linha |
| **Email Marketing Strategist** | `marketing-email-strategist.md` | Estratégia de fluxo: gatilho, cadência, segmento, métricas, entregabilidade |

Opcionais, se existirem no projeto: um agente de copy (quando o texto não vem do cliente) e um de compliance legal (marca regulada).

Como pedir, na prática:
- "Monta o kit de e-mail da marca X. As fontes estão em …" → Email Designer, Modo A.
- "Constrói o e-mail 1 do fluxo de boas-vindas da marca X a partir do brief" → Email Designer, Modo B.
- "Roda o QA nos e-mails do fluxo" → Email QA Reviewer.

## Ferramentas

Python 3, só biblioteca padrão (Pillow opcional). Chrome ou Edge instalado pra render e preview.

| Comando | Faz |
|---|---|
| `python tools/build_kit.py --init <pasta>/email-kit` | Cria o kit de uma marca nova a partir do molde (não sobrescreve nada) |
| `python tools/build_kit.py <pasta>/email-kit` | Gera o `components.html` do kit a partir do `tokens.json`; falha se sobrar token sem valor |
| `python tools/render.py <email.html\|pasta> --out <pasta> [--dark]` | PNG em 680px e 375px (light, ou dark com `--dark`) |
| `python tools/build_preview.py <pasta do fluxo> [--notes notas.md]` | Página única de revisão: aba por e-mail, desktop e mobile lado a lado, assunto e preheader |
| `python tools/fetch_shopify_catalog.py <loja> <pasta> [--images]` | Catálogo e packshots da loja Shopify da marca, com preço e nome reais |
| `python tools/export.py <outro projeto>` | Copia o pacote e os 3 agentes pra outro projeto (`--dry-run` pra só listar) |

Detalhes em [`tools/README.md`](tools/README.md).

## Levar a operação pra outro projeto (ou pra outra pessoa)

1. `python tools/export.py <caminho do projeto>`. Cria `<projeto>/email-ops/` e `<projeto>/.claude/agents/` com os 3 agentes. Não sobrescreve arquivo existente sem `--force`.
2. Colar o conteúdo de `email-ops/install/CLAUDE-snippet.md` no `CLAUDE.md` do projeto (criar o arquivo se não existir).
3. Abrir o projeto no VS Code com o Claude Code. Pra cada marca, criar o kit: `python email-ops/tools/build_kit.py --init <pasta da marca>/email-kit`.
4. Seguir o `CHECKLIST.md` a partir da parte B.

Pra passar a operação pra alguém da equipe: mandar o link do repo (ou a pasta exportada) e pedir pra começar pela seção "Comece aqui". O responsável de cada marca é quem aprova o kit, o primeiro e-mail de cada fluxo e as exceções de regra.

## Regras de ouro

1. Três fontes da marca antes de tudo. Sem elas, parar e avisar.
2. Sem kit aprovado, não existe e-mail de cliente.
3. Só módulos do kit. Módulo novo entra no kit, é aprovado, e só então é usado.
4. Nunca inventar número, nome, prazo, preço ou depoimento: `[[CONFIRMAR]]` visível.
5. Nunca levar cor, frase, número ou regra de uma marca pra outra. Referência de outra marca é só estrutura.
6. Frase ou mensagem "proposta / não validada" nunca vira headline nem texto fixo.
7. Nada sai sem PASS do QA e, em marca regulada, sem revisão jurídica do cliente.

## Manter o pacote

- Este pacote não guarda dado de marca. Aprendizado específico de uma marca vai pro kit dela; aprendizado que vale pra todas vira regra (`rules.md`), item de checklist (`CHECKLIST.md`, "Armadilhas conhecidas") ou módulo do molde (`templates/email-kit/components.template.html`).
- Mudou o molde de módulos? Rodar `build_kit.py` num kit de teste e renderizar antes de publicar a mudança.
