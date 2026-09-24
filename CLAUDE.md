# PowerDigital Lab

Idioma com o responsável: PT-BR. Conteúdo das peças: no idioma definido pela marca (kit ou brand section).

Regra de copy da operação inteira, todas as marcas e formatos: nenhum travessão ou meia-risca (— –) em texto de marketing.

## Dois times de agentes

| Formato | Time | Porta de entrada |
|---|---|---|
| Meta / Instagram, banner programático | Briefing Analyst → Copywriter / Designer → Brand Guardian | [README.md](README.md) |
| **Qualquer e-mail** (campanha, fluxo, newsletter, lote mensal) | Email Designer · Email QA Reviewer · Email Marketing Strategist | [email-ops/README.md](email-ops/README.md) |

Designer não faz e-mail. Pedido de e-mail vai sempre pra operação de e-mail.

## Todo pedido de e-mail segue a operação de e-mail

Sempre que a tarefa for **desenhar ou montar e-mail** (campanha, fluxo de boas-vindas/recompra/winback, newsletter), de qualquer marca, seguir [`email-ops/playbook.md`](email-ops/playbook.md) do começo, com as regras de [`email-ops/rules.md`](email-ops/rules.md) e o checklist de [`email-ops/CHECKLIST.md`](email-ops/CHECKLIST.md):

triagem → kit da marca aprovado (`email-kit/` da marca) → referências → brief do fluxo → construção em **HTML de e-mail** (não em ferramenta de layout) → preview e revisão por seção → QA → exportação.

- **Fontes obrigatórias da marca:** Diagnostic Report, Strategy Report e style guide/toolbox visual (mais o documento de voz e compliance, se a marca é regulada). Sem as três, parar e avisar.
- **Porta de entrada da marca:** o `email-kit/README.md` dela. A tabela "Mapa da marca" diz onde está cada fonte e cada pasta de e-mail.
- **Sem kit aprovado**, o primeiro passo é montar o kit (`python email-ops/tools/build_kit.py --init clients/<marca>/01-brand/email-kit`), nunca improvisar o e-mail.
- **Agentes:** Email Designer (`design-email-designer`) constrói o kit e os e-mails; Email QA Reviewer (`design-email-qa-reviewer`) aprova; Email Marketing Strategist (`marketing-email-strategist`) só pra estratégia de fluxo.
- Nunca levar cor, frase, número ou regra de uma marca pra outra.

### Onde cada coisa da marca mora neste repo

O pacote aceita qualquer estrutura; neste repo o padrão é este (e é o que vai no "Mapa da marca" de cada kit):

```
clients/<marca>/
  00-inbox/                          demandas e materiais recebidos, como chegaram
  01-brand/
    identity/                        style guide / guideline (PDF + digest brand-guidelines.md), logo vetorial
    strategy/
      diagnostic-report.md           [trava] (ou retrato datado: diagnostic-report-aaaa-mm-dd.png)
      strategy-report.md             [trava]
      voice-compliance.md            [trava em marca regulada]
    photos/                          banco de fotos aprovado, packshots
    email-kit/                       o kit (build_kit.py --init)
  03-work/email/<fluxo>/             brief.md + {nn}-{slug}.html + notas de revisão
  04-deliverables/email/<fluxo>/     versão final pro ESP
```

### Papéis opcionais que o playbook cita

- **Content Creator** (copy quando não vem do cliente) → neste repo é o **Copywriter**, lendo o Strategy Report e o kit da marca.
- **Legal Compliance Checker** → não existe aqui. Marca regulada: régua legal do cliente + revisão jurídica do cliente, sem substituto por agente.
- **Brand Guardian** confere o kit contra o guideline uma vez, antes da aprovação do kit. O gate de cada e-mail é o Email QA Reviewer.

### Ferramentas

Python 3.11 + Pillow, Chrome e Edge já instalados nesta máquina (conferido em 2026-09-24). Preview de revisão e página do kit: publicar como Artifact e mandar o link pro responsável.
