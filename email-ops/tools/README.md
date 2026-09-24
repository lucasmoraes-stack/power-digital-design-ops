# Ferramentas da operação de e-mail

Python 3, só biblioteca padrão. Pillow é opcional (acelera o recorte do render). Chrome ou Edge instalado; se estiver num caminho fora do padrão, apontar com `--browser` ou a variável `EMAIL_OPS_BROWSER`. Rodar de qualquer pasta; os caminhos abaixo partem da pasta do pacote (`email-ops/`).

## build_kit.py: criar e gerar o kit de uma marca

```
python tools/build_kit.py --init <pasta da marca>/email-kit     # copia o molde (não sobrescreve)
python tools/build_kit.py <pasta da marca>/email-kit            # tokens.json + molde → components.html
```

- `--init` copia `templates/email-kit/` (README, tokens.json, assets de amostra, references/).
- O build troca cada `%%grupo.chave%%` do molde pelo valor do `tokens.json` e **falha** se sobrar token sem valor.
- Depois do primeiro build, o `components.html` da marca passa a ser lapidado à mão (Email Designer, Modo A). Rodar o build de novo **sobrescreve** o `components.html`: só fazer isso antes de lapidar, ou depois de levar as mudanças pro molde da marca.

## make_sample_assets.py: amostras neutras do molde

`python tools/make_sample_assets.py` refaz as imagens de amostra de `templates/email-kit/assets/` (precisa de Pillow). São placeholders rotulados, nunca vão pra e-mail real: cada marca troca pelos assets dela, conforme `assets/README.md`.

## render.py: ver o e-mail como ele aparece

```
python tools/render.py <email.html ou pasta> --out <pasta>             # 680px e 375px, modo claro
python tools/render.py <email.html ou pasta> --out <pasta> --dark      # os mesmos, em dark mode
```

- Gera `{nome}-680.png`, `{nome}-375.png` (e `-dark`).
- Resolve sozinho três armadilhas: a largura mínima do Chrome headless (o mobile é renderizado num iframe de 375px), a janela de 600px que ativaria a regra de mobile (o desktop sai em 680px) e o tema do sistema vazando pro render (o modo claro é forçado).
- E-mail com mais de 6000px de altura: `--height 9000`.
- Serve também pra estudar referências salvas em `email-kit/references/` sem colar o HTML no chat.

## build_preview.py: página de revisão do fluxo

```
python tools/build_preview.py <pasta do fluxo> --out preview.html --title "Nome do fluxo" --notes notas.md
```

- Uma aba por e-mail. Mostra assunto (com contagem de caracteres), preheader, botão e módulos, lidos das linhas `Subject:` / `Preheader:` / `Button:` / `Modules:` do comentário no topo de cada e-mail. Desktop e mobile ficam lado a lado.
- As imagens vão embutidas: a página é um arquivo só, pronto pra publicar e mandar o link pro responsável revisar.
- `--notes`: arquivo com linhas `- item` (o que mudou nesta rodada, decisões em aberto), mostrado em destaque no topo.
- A página precisa de JavaScript pra montar os e-mails.

## fetch_shopify_catalog.py: packshots e preços da loja da marca

```
python tools/fetch_shopify_catalog.py https://www.loja.com <pasta da marca>/01-brand/photos/products                      # só catalog.json
python tools/fetch_shopify_catalog.py https://www.loja.com <pasta da marca>/01-brand/photos/products --images --match "linha x"
```

- Lê o catálogo público do Shopify (`/products.json`): título, tipo, preço, URL e imagens de cada produto, em `catalog.json`.
- `--images` baixa a 1ª imagem de cada produto (packshot, normalmente PNG com fundo transparente), `--all-images` todas, `--match` filtra por título. Não baixa de novo o que existe.
- Preço e nome valem na data da coleta: reconfirmar na data de envio. Loja que não é Shopify: pedir os packshots ao cliente.
- As imagens baixadas ficam fora do git (pesam); o recorte usado no kit vai pra `email-kit/assets/`.

## export.py: levar a operação pra outro projeto

```
python tools/export.py <pasta do projeto> --dry-run     # só lista o que faria
python tools/export.py <pasta do projeto>               # copia
python tools/export.py <pasta do projeto> --force       # sobrescreve o que já existir
```

- Copia o pacote pra `<projeto>/email-ops/` e os três agentes (`design-email-designer.md`, `design-email-qa-reviewer.md`, `marketing-email-strategist.md`) pra `<projeto>/.claude/agents/`.
- Sem `--force`, não sobrescreve nada e lista os conflitos.
- Depois de copiar: colar `email-ops/install/CLAUDE-snippet.md` no `CLAUDE.md` do projeto e abrir `email-ops/README.md`.
- A cópia exportada também exporta (dá pra passar adiante em cadeia).
