# Regras de design de e-mail

O "cérebro" de todo e-mail da operação. Ler inteiro antes de escrever uma linha de HTML. Vale pra qualquer marca; o visual de cada uma vem do kit de e-mail dela (`email-kit/`, caminho no Mapa da marca do README do kit). Fluxo completo em [`playbook.md`](playbook.md). Checklist de ponta a ponta em [`CHECKLIST.md`](CHECKLIST.md).

---

## 0. Ordem de precedência

Quando duas fontes discordam, vale a de cima:

1. **Régua legal/regulatória da marca** (documento de voz e compliance da marca: saúde, finanças, jurídico, bebida, publicidade de serviço profissional)
2. **Diagnostic Report + Strategy Report da marca** (obrigatórios; mandam em público, mensagem, tom, red flags e status de validação da frase-âncora)
3. **Kit de e-mail aprovado da marca** (é lei pra cor, tipo, botão, foto, caixa de texto)
4. **Brief do fluxo** (`{fluxo}/brief.md`)
5. **Estas regras**
6. **E-mails de referência** (direção de estrutura e ambição, nunca de visual)

---

## 1. Triagem, antes de desenhar

Se faltar algum destes itens, perguntar. Não chutar, e nunca inventar nome de produto, preço, ingrediente, prazo ou claim.

1. **Marca**, seus dois reports (Diagnostic + Strategy) e o kit aprovado (sem kit, ver §9; sem reports, parar)
2. **Tipo de e-mail**: promo, newsletter, lançamento, boas-vindas, carrinho abandonado, pós-compra, recompra, winback, reposição, educativo, sazonal
3. **A mensagem única**: a única coisa que esse e-mail existe pra dizer
4. **Oferta**, se houver: desconto, prazo, código, mínimo, exatos
5. **CTA principal**: texto do botão e destino
6. **Público**: lista inteira, novos, VIP, inativos, carrinho abandonado
7. **Assets**: foto real de produto/lifestyle, ou placeholder rotulado
8. **ESP** (define a sintaxe de merge field) e **destino da entrega** (HTML pro ESP ou Figma fatiado)

Com e-mail de referência anexado: estudar antes de perguntar. Mapear ordem das seções, ritmo de cor, par tipográfico e padrão de CTA, e adaptar isso à marca. Nunca clonar copy nem layout exato. Sem referência: partir dos padrões da §4.

Melhor perguntar a mais do que entregar o e-mail errado.

---

## 2. Base técnica (serve pra qualquer ESP)

O HTML precisa colar limpo em qualquer ESP (Klaviyo, Mailchimp, HubSpot, Braze, Omnisend, RD Station...). Ou seja, HTML de e-mail no mínimo denominador comum:

### Estrutura
- **Tabela pra layout, sempre** (`<table role="presentation">`). Sem flexbox, grid, `position`, `float` pra layout, variável CSS, `@import`. Assumir que o Outlook vai abrir.
- **600px de largura**, centralizado, sobre um fundo neutro de página, pra o preview parecer e-mail e não site. Fluido no mobile (`width:100%; max-width:600px`), com tabela fantasma `<!--[if mso]>` pro Outlook.
- **Estilo inline** em tudo que precisa sobreviver. O `<style>` do `<head>` existe só pra media query, carga de fonte e dark mode. O e-mail tem que continuar legível com o `<style>` removido (alguns clientes removem).
- **Coluna única.** Exceções: grade de produto 2-up, tabela comparativa de 2 colunas, e linha mídia + texto (foto ou produto ao lado de texto curto). Todas empilham no mobile.
- **Cada banda é seu próprio bloco de tabela**, pra mapear limpo no editor drag-and-drop do ESP.
- Sem JavaScript, formulário, vídeo embutido, SVG, fonte de ícone.
- HTML final abaixo de **90KB** (o Gmail corta em 102KB e esconde o resto, inclusive o descadastro).

### Tipografia
- No máximo **2 famílias**, carregadas por `<link>` como melhoria progressiva, cada uma com pilha de fallback declarada inline (`Helvetica, Arial, sans-serif` / `Georgia, serif`) e fallback extra pro Outlook via `<!--[if mso]>`. O e-mail precisa continuar com cara intencional se as web fonts falharem.
- Corpo **16px** (14px é o piso absoluto), line-height 1.5. Legal/rodapé 11-13px. Headline no mobile nunca abaixo de 26px.
- Palavra sozinha na última linha de título (viúva): prender com `&nbsp;` à palavra anterior.

### Texto vivo e imagem
- **Texto vivo sobre imagem.** Headline, corpo e CTA são texto HTML, nunca embutidos em imagem. Exceção única: o logo da marca sobre foto de hero, com o nome da marca no `alt`.
- Texto sobre imagem de fundo, **sempre com `bgcolor` sólido de fallback** que mantenha o texto legível sozinho (é o que o Outlook desktop mostra sem VML). Pra fundo com imagem no Outlook: VML (`v:rect`/`v:roundrect`), `mso-padding-alt:0px` na célula e `mso-fit-shape-to-text:true` no textbox, senão o conteúdo corta ou a tabela alarga.
- Gradiente **vira imagem** (JPG) com `bgcolor` de fallback. `linear-gradient` em CSS falha no Outlook e em parte do Gmail.
- Todo `<img>` com `width` em atributo, `display:block`, `border:0`, `alt` descritivo (ou `alt=""` se decorativa).
- Resolução **2x** (hero 600px → arquivo 1200px). JPG 70-80 pra foto, PNG só pra logo/transparência. Até ~150KB por imagem, ~800KB no e-mail.
- `border-radius` em imagem vira quadrado no Outlook desktop: aceitável, nunca estrutural.
- No repo o caminho da imagem é relativo; na exportação vira URL absoluta do ESP/CDN.

### Botão
- `<a>` real estilizado como botão, dentro de `<td>` com `bgcolor` (botão à prova de bala). Mínimo **44px** de altura, tamanho por padding, nunca por truque de line-height.
- No repo, `href` usa placeholder nomeado (`{{CTA_URL}}`, `{{HOME_URL}}`), mais fácil de ligar do que `#`. Nenhum `#` na versão final.

### Dark mode
- `<meta name="color-scheme" content="light dark">` + `supported-color-schemes`; regras em `prefers-color-scheme` (Apple Mail/iOS) e `[data-ogsc]`/`[data-ogsb]` (app do Outlook).
- O Gmail inverte por conta própria. Por isso: nada de logo transparente que some em fundo escuro (ter versão pra fundo escuro, escondida **inline** com `display:none; max-height:0; overflow:hidden; mso-hide:all` e revelada só pelo CSS de dark mode), nada de texto branco puro sobre imagem que pode ser invertida, nada de plano grande de #000/#FFF chapado.
- Texto escuro sobre foto clara pode virar claro sobre claro no app do Gmail: testar no Gmail iOS/Android antes do envio.

### Acessibilidade
- `<html lang>`, `role="presentation"`, `<h1>`/`<p>` semânticos, ordem do HTML = ordem de leitura no mobile.
- Contraste **WCAG AA 4.5:1** no texto corrido, 3:1 em texto grande. Link distinguível sem depender só de cor.

### Preheader, merge field, rodapé
- Preheader escondido logo após o `<body>` + espaçador `&zwnj;&nbsp;`.
- Merge field só onde merece, sempre com fallback, na sintaxe do ESP registrada no kit. Sem ESP definido: notação Liquid neutra `{{ first_name | default: "there" }}`.
- Rodapé legal: endereço físico, descadastro funcional, motivo do recebimento (CAN-SPAM nos EUA, LGPD no Brasil, GDPR na Europa), mais o que a régua da marca exigir.

---

## 3. O esqueleto de sete bandas

Todo e-mail é uma pilha de bandas horizontais de largura total, cada uma com fundo próprio. As bandas **são** o e-mail: nada de card boiando numa página branca sem fim. Ordem padrão:

1. **Preheader**: texto de preview escondido, 40-90 caracteres, que estende o assunto (nunca repete)
2. **Banda de logo**: wordmark centralizado, pequeno, com respiro em cima e embaixo
3. **Banda hero**: o momento mais alto. Fundo de cor ou foto, headline grande, subhead de 1-2 frases, um CTA. Quem lê só essa banda precisa entender a mensagem e conseguir agir.
4. **Banda de prova ou estrutura**: exatamente UMA destas: cards de produto, tabela comparativa, passos numerados, benefícios com ícone, lista de itens. Escolher a que mais sustenta a mensagem; nunca empilhar duas.
5. **Banda de mudança de ângulo**: a mesma mensagem, com abordagem mais suave: citação de cliente, "como as pessoas usam", "não sabe qual?", carta pessoal. Com CTA próprio.
6. **Banda de última chamada**: reafirma prazo, recompensa ou garantia numa linha, e o CTA final.
7. **Banda de rodapé**: escura ou de contraste forte. Wordmark, grade pequena de links úteis, redes sociais (só se a conta existir e estiver ativa), endereço, descadastro, copyright.

E-mail curto corta bandas (um flash sale pode ser 1-2-3-6-7). **Nunca uma oitava.** Se o conteúdo não cabe em sete, são dois e-mails. Exceção à "uma banda de estrutura só" (ex.: passos + tabela de preço, quando os dois são o conteúdo do copy-fonte) exige aprovação explícita do responsável e fica registrada no brief.

O kit de cada marca mapeia seus módulos pra essas bandas (ver README do kit).

---

## 4. Padrões por tipo de campanha (sem referência, começar daqui)

Conteúdo padrão das bandas 4-5 por tipo. **Marca regulada filtra antes:** se a régua da marca proíbe urgência, escassez ou promessa, esses elementos saem do padrão.

- **Promo / sale.** A oferta É a headline do hero ("20% off everything, ends Sunday"), código no eyebrow ou subhead. Banda 4: grade de mais vendidos ou 2-3 cards de produto. A última chamada é dona do prazo.
- **Boas-vindas.** Hero: promessa da marca + oferta de boas-vindas se houver. Banda 4: três itens numerados de "o que esperar" ou mais vendidos. Mudança de ângulo: um empurrão suave de "encontre o seu".
- **Lançamento / reposição.** Hero: headline com escassez, só se for verdade. Banda 4: cards de produto empilhados, cada um com foto, 2-3 bullets e CTA. Última chamada: disponibilidade dita de forma simples.
- **Carrinho abandonado.** Hero: o produto que ficou, foto em destaque. Banda 4: uma linha de reasseguramento (frete, troca, garantia). Sem banda de mudança de ângulo; curto.
- **Educativo / história de produto.** Hero: headline de curiosidade ou contrária ao senso comum. Banda 4: tabela comparativa ou lista numerada. Mudança de ângulo: foto de lifestyle com CTA discreto.
- **Pós-compra / fidelidade / recompra / winback.** Hero: headline de valor de volta. Banda 4: três formas numeradas de usar o produto, os pontos, ou o que há de novo. Última chamada: a recompensa, dita uma vez.
- **Newsletter / editorial.** Hero: a história ou tema, guiado por foto. Banda 4: grade 2-up de produtos com legenda. Rodapé discreto, CTAs suaves.

---

## 5. Regras visuais

- **Cor.** 2-3 cores de fundo do kit, alternadas descendo a página pra toda fronteira de banda ficar visível. Uma banda pode ter foto de fundo. Card dentro de banda contrasta com ela. **Nunca duas bandas vizinhas da mesma cor.** Trocar o fundo de um módulo entre as superfícies do kit (ex.: branco ↔ superfície alternativa) é troca de token, não módulo novo; conferir os elementos internos que assumiam o fundo antigo.
- **Tipo.** Uma face de display pra headline, uma de trabalho pro resto (podem ser a mesma família em pesos diferentes, se o kit mandar). Um destaque em itálico pode aparecer dentro de uma headline (o kit define se existe e como), e em nenhum outro lugar. Escala: hero 36-52px, headline de banda 24-32px, eyebrow 11-13px em caixa-alta com espaçamento, corpo 16px, legal 11-13px. **Eyebrow fica acima da headline, nunca abaixo.**
- **Botão.** Um formato (retângulo ou pílula, igual ao site da marca), **uma cor de preenchimento por e-mail**, repetido idêntico em toda banda com CTA. Se aparecem dois estilos de botão no mesmo e-mail, um está errado. O kit pode ter variantes de cor por e-mail de um fluxo: cada e-mail usa uma só. Botão claro sobre fundo branco tem borda fraca: preferir a variante escura ou uma banda de cor.
- **Espaçamento.** Escala de 8pt. Banda com 48-72px de padding vertical (40px no mobile). Card com 24-32px de padding interno. Botão com 14-18px vertical e 28-40px horizontal. Gutter lateral 40px desktop / 24px mobile. Na dúvida, mais espaço: e-mail apertado parece spam.
- **Imagem.** Foto real do banco aprovado da marca, seguindo a regra de fotografia do kit. Sem asset: bloco placeholder rotulado, tipo `[ HERO · product on colored background · 600×460 ]`. Sem ilustração decorativa, clip-art de ícone ou banco de imagem com cara de IA.
- **Primeira tela.** O e-mail abre com imagem ou com um visual forte; um bloco de texto grande sem imagem na abertura faz a pessoa desistir. Foto com área calma (céu, fundo liso) recebe o título por cima; recortar fechado o bastante pra pessoa ficar logo abaixo do título, sem espaço sobrando entre os dois.
- **Retrato de banco de imagem** ao lado de "fale com a equipe" ou numa assinatura sugere que aquela é a equipe real. Só usar quando o responsável aprovar esse uso; nunca em assinatura sem pessoa real.
- **Composição num fluxo.** Dois e-mails seguidos de um fluxo não abrem com o mesmo tratamento de hero. O conteúdo decide: e-mail "sobre pessoa" (boas-vindas, reengajamento) pede foto ou carta; e-mail "sobre processo" (pedido, envio, recompra) pede passos, dado, produto.
- **Só módulos do kit.** Módulo novo não nasce dentro de um e-mail: entra no kit, é aprovado, e só então é usado.

---

## 6. Regras de conversão

Inegociáveis; é por elas que o e-mail existe.

- **Uma mensagem, um destino.** O CTA pode repetir 2-3 vezes com texto variado, mas todo botão leva ao mesmo lugar ou família de produto.
- **O hero converte sozinho.** Logo, headline, subhead, oferta e botão cabem na primeira tela de um celular de 375px.
- **Oferta na frente.** O gancho mora na headline ou no eyebrow do hero e ecoa no assunto.
- **A headline carrega o e-mail.** No máximo duas frases de corpo sob qualquer headline antes de um CTA ou um visual assumir. (Exceção: banda de carta pessoal.)
- **Urgência uma vez, com honestidade.** Um prazo real, dito com clareza, perto da última chamada. Sem timer falso. Marca que proíbe urgência não usa nem essa.
- **Uma linha de reversão de risco** perto do CTA final, quando a marca tem uma de verdade.
- **Prova social = uma coisa específica.** Uma citação com nome real ou um número ("4.7 · 9,200 reviews"). Nunca carrossel de estrelas, nunca nome ou citação inventados.
- **Lista é contável.** 3-5 itens, legíveis de relance. Numeração só quando a ordem é informação (passos reais).
- **Assunto + preheader sempre entregues junto com o e-mail.** Assunto até 50 caracteres; preheader estende, nunca repete.

---

## 7. Regras de copy

- **A voz vem da marca.** Ler o Strategy Report (personalidade, we do / we don't, red flags, mensagens-chave), o documento de voz, e-mails anteriores e o site antes de escrever uma palavra. Frase-âncora "proposta" ou "não validada" não vira headline nem frase de rodapé. Mensagem condicionada ("só quando X existir") respeita a condição, inclusive no texto fixo do kit.
- **Caixa:** o padrão é headline em Title Case, corpo em sentence case, CTA em ALL CAPS, **a menos que o kit diga outra coisa** (o kit registra a regra de caixa da marca).
- Curto ganha de esperto. Fragmento vale. Palavra que não trabalha sai.
- Segunda pessoa, presente, voz ativa. Assinatura de equipe fala em "we", nunca em "I".
- Específico ganha de superlativo. Em marca regulada, específico só se estiver na fonte aprovada.
- CTA começando com verbo, 2-4 palavras.
- **Proibido:** emoji, "elevate", "unlock", "game-changing", "revolutionary", mais de um ponto de exclamação por e-mail, lorem ipsum, **travessão e meia-risca**, headline-slogan, frase antitética ("não é X, é Y").
- **Copy-fonte do cliente:** usar o texto exato. Mudar só o que a régua legal ou estas regras exigem, e registrar cada mudança (e o motivo) no brief. Texto cortado também é mudança registrada.
- **Copy faltando:** escrever texto provisório com cara de pronto e sinalizar como "copy nova, revisar". **Dado faltando** (número, preço, prazo, nome, depoimento, claim): nunca preencher, fica `[[CONFIRMAR: ...]]` visível.

---

## 8. Nunca fazer

- Mais de uma mensagem principal ou destino no mesmo e-mail
- Dois CTAs de estilo diferente disputando a mesma banda
- Corpo de texto em várias colunas, ou grade 3-up
- Texto corrido sobre gradiente forte ou foto carregada
- Card dentro de card dentro de card (um nível, no máximo)
- Terceira família tipográfica
- Texto embutido em imagem (fora o logo)
- Preço, claim, review, prazo ou nome de produto inventados
- Rodapé feito de qualquer jeito: é uma banda desenhada como as outras
- Fundo igual em toda banda (a "rolagem branca sem fim")
- Módulo improvisado fora do kit
- Link de rede social morta, `#` em arquivo final, `[[CONFIRMAR]]` em arquivo final
- Token de cor de wireframe ou de componente genérico tratado como cor de marca

---

## 9. Sem kit de marca

Pra entrega de cliente, **não existe e-mail sem kit aprovado**: primeiro se monta o kit (playbook, etapa 1). Motivo: cada marca tem ID visual própria, e um sistema genérico vira a cara de todas.

Exceção só pra teste interno descartável: declarar no topo do arquivo, em comentário, o sistema assumido (2 cores, 1-2 famílias, formato de botão) e marcar o arquivo como `draft-no-kit`. Esse arquivo nunca vai pro cliente nem pro ESP. O sistema assumido parte do que se sabe da marca (site, logo), nunca de um default fixo.

---

## 10. Entrega

- Um arquivo HTML autocontido por e-mail, nome em kebab-case em inglês com número de ordem no fluxo: `{fluxo}/{nn}-{slug}.html` (ex.: `welcome/01-welcome.html`).
- Abre no navegador e parece um e-mail numa caixa de entrada: 600px, centralizado, fundo neutro em volta.
- Comentário no topo do HTML com `Subject:`, `Preheader:`, `Modules:`, `Button:` (a ferramenta de preview lê essas linhas).
- **Assunto e preheader** também registrados no `brief.md` do fluxo.
- Relatório de entrega: módulos usados, desvios do copy-fonte com motivo, `[[CONFIRMAR]]` abertos, peso do HTML e das imagens.

---

## 11. Checklist mínimo de saída (o QA completo está no agente Email QA Reviewer)

- [ ] 600px, tabela, tudo inline, sobrevive sem o `<style>`
- [ ] Até 7 bandas, uma única banda de prova/estrutura, nenhuma banda vizinha da mesma cor
- [ ] Um destino, uma cor de botão, botão 44px+, `href` real ou placeholder nomeado
- [ ] Hero converte sozinho numa tela de 375px, abre com imagem ou visual forte
- [ ] HTML < 90KB, imagens 2x comprimidas com `alt`
- [ ] Preheader + assunto entregues, preheader estende o assunto
- [ ] Dark mode: meta tags + logo pra fundo escuro escondido inline
- [ ] Contraste AA, corpo 16px
- [ ] Rodapé legal completo
- [ ] Nenhum dado inventado, nenhum travessão, nenhum emoji
- [ ] Só módulos do kit aprovado

---

## 12. Por que algumas regras são assim

| Regra | Motivo |
|---|---|
| Régua legal da marca no topo da precedência (§0) | Marca regulada tem regra que nenhum padrão de e-commerce pode sobrepor |
| Sem kit não tem entrega (§9) | Um sistema padrão fixo vira a cara de todas as marcas |
| Placeholder nomeado em vez de `#` | Mais fácil de ligar no ESP, e o QA detecta link esquecido |
| Linha mídia + texto permitida | Padrão que empilha bem e dá ritmo a listas curtas |
| Dado provisório nunca, só `[[CONFIRMAR]]` | Em marca regulada, número ou prazo "de exemplo" pode ir ao ar por engano |
| Caixa e itálico definidos pelo kit | Cada marca tem sua regra; o padrão geral é só ponto de partida |
| Rede social só se a conta existir | Link pra conta morta é bug de confiança |
| E-mail construído em HTML, não no Figma | Montar e-mail em ferramenta de layout gerou rodadas de retrabalho (token errado, limite de auto-layout, fonte trocada, seção faltando); em HTML o que se revisa é o que se envia |
| Sem travessão nem antítese | São marcas de texto gerado por IA |
