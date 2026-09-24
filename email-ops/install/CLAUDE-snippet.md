## Todo pedido de e-mail segue a operação de e-mail

Sempre que a tarefa for **desenhar ou montar e-mail** (campanha, fluxo de boas-vindas/recompra/winback, newsletter), de qualquer marca, seguir [`email-ops/playbook.md`](email-ops/playbook.md) do começo, com as regras de [`email-ops/rules.md`](email-ops/rules.md) e o checklist de [`email-ops/CHECKLIST.md`](email-ops/CHECKLIST.md):

triagem → kit da marca aprovado (`email-kit/` da marca) → referências → brief do fluxo → construção em **HTML de e-mail** (não em ferramenta de layout) → preview e revisão por seção → QA → exportação.

- **Fontes obrigatórias da marca:** Diagnostic Report, Strategy Report e style guide/toolbox visual (mais o documento de voz e compliance, se a marca é regulada). Sem as três, parar e avisar.
- **Porta de entrada da marca:** o `email-kit/README.md` dela. A tabela "Mapa da marca" diz onde está cada fonte e cada pasta de e-mail.
- **Sem kit aprovado**, o primeiro passo é montar o kit (`python email-ops/tools/build_kit.py --init {pasta da marca}/email-kit`), nunca improvisar o e-mail.
- **Agentes:** Email Designer (`design-email-designer`) constrói o kit e os e-mails; Email QA Reviewer (`design-email-qa-reviewer`) aprova; Email Marketing Strategist (`marketing-email-strategist`) só pra estratégia de fluxo.
- Nunca levar cor, frase, número ou regra de uma marca pra outra.
