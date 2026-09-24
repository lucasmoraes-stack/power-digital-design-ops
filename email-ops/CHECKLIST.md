# Checklist da operação de e-mail

Tudo que precisa existir pra montar uma operação de e-mail numa marca nova, do setup ao envio. Copiar esta lista pro README do kit ou pro gerenciador de tarefas do projeto e ir marcando. O fluxo explicado está em [`playbook.md`](playbook.md); as regras, em [`rules.md`](rules.md).

**Legenda:** **[trava]** = sem isso a etapa seguinte não começa. Quem: **R** = responsável pelo projeto, **C** = cliente, **D** = Email Designer (agente), **Q** = Email QA Reviewer (agente), **S** = Email Marketing Strategist (agente).

---

## A. Setup da operação (uma vez por projeto ou máquina)

- [ ] Pacote `email-ops/` presente no projeto (no repo do estúdio: `_studio/email-ops/`; em outro projeto: `python export.py <projeto>`) · R
- [ ] Agentes em `.claude/agents/`: `design-email-designer.md`, `design-email-qa-reviewer.md`, `marketing-email-strategist.md` · R
- [ ] Trecho de `install/CLAUDE-snippet.md` colado no `CLAUDE.md` do projeto · R
- [ ] Python 3 instalado (`python --version`); Pillow opcional (`pip install pillow`, usado pra recortar imagem e aparar render) · R
- [ ] Chrome ou Edge instalado (render e preview). Caminho diferente do padrão: variável `EMAIL_OPS_BROWSER` · R
- [ ] Acesso ao Figma MCP, se o style guide da marca está no Figma · R
- [ ] Onde publicar o preview pra revisão (página compartilhável) definido · R

## B. Insumos da marca (antes do kit)

### B1. Estratégia **[trava]**
- [ ] **Diagnostic Report** refinado, no projeto (texto ou retrato datado): objetivo, ICPs com medo e necessidade, diferenciais, provas existentes e provas que ainda não existem, pontos de atenção · R/C
- [ ] **Strategy Report** refinado, no projeto: promessa, personalidade e valores (we do / we don't), red flags, mensagens-chave com condição de uso, posicionamento · R/C
- [ ] **Status da frase-âncora** (validada ou proposta) anotado · R
- [ ] Mensagens condicionadas listadas, com a condição ("só quando X existir") e se ela está cumprida hoje · R

### B2. Visual **[trava]**
- [ ] **Style guide / toolbox oficial** localizado (Figma com arquivo e node, PDF de guideline ou site no ar). Anotar se é oficial ou extraído · R/C
- [ ] Paleta com hex exato e nome de cada cor · C
- [ ] Tipografia: família, pesos, se é Google Font ou licenciada (licenciada = fallback é o que aparece na maioria das caixas) · C
- [ ] Logo em **vetor** (SVG/PDF), pra gerar versão clara e escura · C
- [ ] Regra de fotografia da marca (o que a foto precisa mostrar, o que evitar) · C
- [ ] Banco de fotos aprovado (pasta) e packshots de produto com fundo transparente · C
- [ ] Recursos visuais recorrentes: palavra em itálico, textura, gradiente, formato de label, raio de canto · R
- [ ] Formato e raio do botão do site no ar · R

### B3. Voz e legal **[trava em marca regulada]**
- [ ] Documento de voz (léxico, caixa de texto, idioma do conteúdo) · R/C
- [ ] Régua legal da marca: o que não pode prometer, claims permitidos, urgência permitida ou não, disclaimers obrigatórios · C
- [ ] Linha legal fixa de rodapé (se houver) · C
- [ ] Quem faz a revisão jurídica do cliente e em quanto tempo · C

### B4. Operação e dados
- [ ] **ESP** (Klaviyo, Mailchimp, HubSpot...) e sintaxe de merge field · C
- [ ] Endereço físico pro rodapé (CAN-SPAM / LGPD / GDPR) · C
- [ ] Canais de atendimento reais (telefone, e-mail, chat) e se há prazo de resposta prometível · C
- [ ] URLs: home, loja/catálogo, ajuda, pedidos, contato, descadastro, preferências, privacidade · C
- [ ] Redes sociais ativas (link de conta morta não entra) · C
- [ ] Provas numéricas com fonte e data (nota, número de reviews, anos de operação) · C
- [ ] Moeda, preço, frete e prazo de entrega verificados com a operação, quando o e-mail fala disso · C
- [ ] Domínio de envio autenticado (SPF, DKIM, DMARC) e aquecido, se é conta nova · C/S

## C. Kit da marca (etapa 1)

- [ ] `build_kit.py --init {pasta da marca}/email-kit` rodado · D/R
- [ ] **Mapa da marca** preenchido no README do kit (caminho de cada fonte e das pastas de e-mail) · R
- [ ] `tokens.json` preenchido do style guide, com a fonte de cada valor registrada no README · D
- [ ] Contraste checado: texto corrido AA 4.5:1, texto grande 3:1, texto sobre botão · D
- [ ] Neutros derivados da paleta (texto secundário, filete, fundo da página), sem cor nova de marca · D
- [ ] Dark mode definido (fundo, superfície, título, corpo, link, filete) · D
- [ ] Logo claro e escuro em PNG 2x transparente, a partir do vetor · D
- [ ] Fotos recortadas no tamanho de cada módulo (2x), comprimidas, com fallback de cor anotado · D
- [ ] Gradiente e textura exportados como JPG, com cor sólida de fallback · D
- [ ] Seção "Estratégia aplicada ao e-mail" preenchida (ICPs, mensagens e condições, frase-âncora e status, tom, red flags, provas que existem e que não existem) · D/R
- [ ] Regras só da marca (foto, moeda, prazo, assinatura, rede social, revisão jurídica) · D/R
- [ ] Texto fixo dos módulos (frase do rodapé, eyebrow padrão) conferido contra red flags e mensagens condicionadas · D/R
- [ ] `build_kit.py {pasta}/email-kit` rodado sem token pendente; módulos lapidados pra marca · D
- [ ] Render do `components.html` conferido em 680px, 375px e dark · D
- [ ] Página do kit publicada e revisada módulo por módulo · R
- [ ] **Status "aprovado", data e quem aprovou** no README do kit **[trava]** · R

## D. Referências (etapa 2)

- [ ] 2 a 4 e-mails de referência salvos em `email-kit/references/` (arquivo, não colado no chat) · R
- [ ] Renderizados com `render.py` e estudados pela imagem · D
- [ ] Uma linha por referência no README: o que aproveitar (estrutura, ritmo, módulo) e o que não aproveitar (paleta, tipo, layout) · D

## E. Por fluxo (etapa 3)

- [ ] Estratégia do fluxo, se não veio do cliente: gatilho, cadência, segmento, condição de saída · S
- [ ] `brief.md` copiado de `templates/flow-brief.md` · D
- [ ] Triagem completa (tipo, público, oferta, CTA, ESP, destino, copy-fonte) · D
- [ ] Sistema do fluxo: hero diferente em e-mails seguidos, uma cor de botão por e-mail, alternância de fundo · D
- [ ] Por e-mail: ICP, mensagem-chave e condição, mensagem única, assunto (até 50) + preheader, CTA + URL, bandas com módulo · D
- [ ] Desvios do copy-fonte previstos, com motivo · D
- [ ] Claims a confirmar e itens pra revisão jurídica listados · D
- [ ] Brief aprovado pelo responsável · R

## F. Por e-mail (etapa 4)

- [ ] Só módulos do kit; módulo novo volta pro kit antes · D
- [ ] Comentário no topo: Subject, Preheader, Modules, Button · D
- [ ] Copy-fonte exato; cada mudança registrada no brief · D
- [ ] Nenhum dado inventado; `[[CONFIRMAR]]` visível onde falta · D
- [ ] Sem travessão, sem emoji, no máximo um ponto de exclamação · D
- [ ] Abre com imagem ou visual forte; hero converte sozinho em 375px · D
- [ ] Viúvas de título presas com `&nbsp;` · D
- [ ] Render em 680px, 375px e dark conferido pelo próprio Designer · D
- [ ] HTML < 90KB, imagens < 150KB cada e ~800KB no total · D
- [ ] **Primeiro e-mail do fluxo aprovado antes dos outros** · R

## G. Revisão (etapa 5)

- [ ] `build_preview.py {fluxo} --notes notas.md` gerado e publicado · D/R
- [ ] Comentários do responsável aplicados só na seção apontada · D
- [ ] Notas da rodada atualizadas (o que mudou, o que está aberto) · D
- [ ] Decisões de exceção (ex.: duas bandas de estrutura) registradas no brief com data · R

## H. QA (etapa 6)

- [ ] Email QA Reviewer rodado nos e-mails do fluxo · Q
- [ ] Veredito PASS em todos, ou BLOCK resolvido · Q/D
- [ ] Correções técnicas que valem pra marca inteira levadas pro kit · D
- [ ] Lista "pendente antes do envio" separada dos bloqueios · Q

## I. Antes do envio (etapa 7)

- [ ] Revisão jurídica do cliente concluída (marca regulada) **[trava]** · C
- [ ] Provas numéricas reconfirmadas na data de envio · C
- [ ] Endereço físico no rodapé; nenhum `[[CONFIRMAR]]` no arquivo final **[trava]** · R
- [ ] Imagens no ESP/CDN, caminhos relativos trocados por URL absoluta · R
- [ ] Placeholders de link (`{{CTA_URL}}`...) trocados pelas URLs reais, com UTM · R
- [ ] Merge field na sintaxe do ESP, com fallback · R
- [ ] Descadastro e preferências funcionando · R
- [ ] Teste enviado pra Gmail (web e app), Outlook desktop, Apple Mail e app do Outlook · R
- [ ] Preview em serviço de teste (Litmus / Email on Acid) quando há fundo com imagem ou VML · R
- [ ] Dark mode real conferido no Gmail app (texto sobre foto) · R
- [ ] Gatilho, cadência e segmento configurados no ESP e testados com um contato de teste · R/S
- [ ] Versão final copiada pra pasta de entregas · R

## J. Depois do envio (etapa 8)

- [ ] Data de envio e versão registradas no brief · R
- [ ] Métricas da primeira semana (abertura com ressalva do Apple MPP, clique, CTOR, descadastro, reclamação) · S
- [ ] Aprendizados levados pro kit e pro changelog · D/R

---

## Armadilhas conhecidas

Coisas que já custaram retrabalho e agora fazem parte do checklist:

| Armadilha | Como evitar |
|---|---|
| Cor de placeholder de wireframe usada como cor da marca | Token só vale se bate com o style guide oficial; registrar a fonte de cada hex |
| Construir e-mail direto na ferramenta de layout | Construir em HTML; Figma só no fim, se o cliente exigir |
| Página salva de galeria de e-mail colada no chat estoura o prompt | Salvar em `references/` e renderizar com `render.py` |
| Render em 375px parece estourado à direita | Limite de largura mínima do Chrome headless; o `render.py` usa iframe, não janela estreita |
| Render sai em dark mode sem querer | O `render.py` força modo claro; `--dark` pra conferir o escuro |
| Janela de 600px ativa a regra de mobile | Desktop é renderizado em 680px |
| Fundo com imagem corta ou alarga no Outlook | VML com `mso-padding-alt:0px` e `mso-fit-shape-to-text:true` |
| Logo escuro aparece duplicado quando o cliente remove o `<style>` | Esconder o logo escuro inline, revelar só no CSS de dark mode |
| Frase de rodapé do kit promete o que a estratégia ainda não liberou | Conferir texto fixo do kit contra red flags e mensagens condicionadas |
| Retrato de banco ao lado de "fale com a equipe" parece a equipe real | Decisão explícita do responsável; nunca em assinatura sem pessoa real |
| Assinatura de equipe escrita em "I" | Equipe fala em "we" |
| E-mail que abre com texto grande e sem imagem | Abrir com foto ou visual forte; recorte fechado, sem vão entre título e pessoa |
| Produto pequeno dentro de círculo ou quadrado fica ruim | Packshot recortado no limite do objeto; se continuar pequeno, usar foto |
| Motivo de recebimento do rodapé errado pro público | Lead que ainda não comprou recebe "because you signed up", não "because you ordered" |
| Botão de cor clara sobre fundo branco some | Botão claro só sobre banda escura ou de cor |
