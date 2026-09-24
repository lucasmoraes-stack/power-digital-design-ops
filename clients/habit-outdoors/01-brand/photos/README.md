# Habit Outdoors · banco de imagens

Coloque aqui os **originais** (a maior resolução que tiver). O kit e os e-mails puxam daqui e recortam no tamanho de cada módulo em `email-kit/assets/`. Nunca coloque aqui imagem com texto embutido.

| Pasta | O que vai | Formato | Exemplos |
|---|---|---|---|
| `products/` | packshot de produto, sem fundo | PNG transparente, 1200px ou mais | `mens-cedar-branch-insulated-bib.png` |
| `lifestyle/` | foto de uso: pessoas, caça, pesca, camping, paisagem com produto | JPG, 2400px ou mais no lado maior | `fishing-river-guide-shirt-01.jpg` |
| `backgrounds/` | fundos sem pessoa: camo, papel, textura, céu, mata, água, madeira | JPG (ou PNG se tiver transparência), 2400px ou mais | `camo-realtree-apx.jpg`, `texture-paper-grain.jpg` |

- **Nome do arquivo:** minúsculas, palavras separadas por hífen, sem acento nem espaço. Em produto, use o nome da loja (o `handle` do `catalog.json`), para o preço e o nome baterem.
- **Produtos da loja:** `products/` já tem 39 packshots e o `catalog.json` com os 169 produtos, baixados por `python email-ops/tools/fetch_shopify_catalog.py https://www.habitoutdoors.com clients/habit-outdoors/01-brand/photos/products --images --match "nome"`. Packshot seu, com mais qualidade, pode substituir o da loja com o mesmo nome.
- **Git:** as imagens desta pasta ficam **fora do git**, porque pesam. Elas continuam no disco e no OneDrive. O que vai para o git é o recorte usado no kit (`email-kit/assets/`).
