# Habit Outdoors · banco de fotos de uso (lifestyle)

Criado em 2026-09-24 para o kit v0.4 (rodada 2 do lote 2026-broadcasts).

**Todos os arquivos `crop-sent-*` são provisórios:** recortes dos 5 e-mails enviados em `email-kit/references/` (prints de 1200px de largura, JPG q85). Nenhum texto, logo ou botão sobreposto (a marca impressa na roupa ou no boné é do produto e fica). Trocar pelo original do banco assim que o cliente mandar: mesmo enquadramento, mais resolução. **Foto da Duck Camp nunca entra aqui.**

Recortes em que a linha de pesca desenhada foi removida por script estão marcados; o retoque é bom em escala de e-mail, mas conferir no original.

Imagens extras da loja (`photos/products/*-N.png`): revisadas as 51. Todas são de estúdio (fundo cinza, modelo, detalhe com rótulo, tabela de medidas). **Nenhuma em locação**, nenhuma entra aqui. O close do bolso (`mens-heavyweight-soft-flannel-6`) continua servindo só como detalhe de colagem (E22).

"Área calma" = onde cabe texto vivo por cima, medida pelo desvio de luminância no terço de cima e de baixo (desvio abaixo de ~35 = calmo).

| Arquivo | O que mostra | Tamanho | Área calma | Melhor uso |
|---|---|---|---|---|
| `crop-sent-sep15-family-forest-walk.jpg` | pai, filho e mulher de costas em Realtree, caminhando para a mata, bokeh escuro | 1200x610 | topo (escuro, calmo; as cabeças encostam na borda de cima: a área de texto é gerada acima, `extend_top="fog"`) · base calma | **hero full-bleed** (E24, texto em cima); amostra `e24-hero-forest.jpg` · linha desenhada removida |
| `crop-sent-sep24-barn-door-feed-bag.jpg` | homem de flanela verde carregando saco de ração na porta do celeiro vermelho | 1200x1010 | nenhuma no topo (a cabeça está na borda: fachada estendida por script, `extend_top="stretch"`) · base: jeans, calmo depois do degradê | **hero full-bleed** (E24B, texto embaixo); amostra `e24-hero-barn.jpg` |
| `crop-sent-sep22-angler-tackle-box.jpg` | pescador de camisa azul e boné Habit olhando a caixa de iscas, fundo escuro de rio | 1200x440 | topo (escuro, o mais calmo do banco) | hero full-bleed curto ou topo de E24 com `extend_top="fog"`; feature · linha desenhada removida (é o mesmo frame do `hero-fishing.jpg` do kit) |
| `crop-sent-sep15-camp-chairs-family.jpg` | família em cadeiras de camping no campo, fim de tarde | 1200x514 | nenhuma (cheia de ponta a ponta) | feature, foto rasgada (E26: `e26-torn-camp.jpg`) |
| `crop-sent-sep10-utv-hunters.jpg` | dois caçadores de boné laranja no UTV, céu azul e mata de outono | 1200x565 | topo parcial (faixa de céu, depois copas) | hero full-bleed com degradê escuro no topo (`top_shade`), feature |
| `crop-sent-sep10-truck-hunter.jpg` | caçador com rifle na traseira da caminhonete, luz de fim de tarde | 1200x670 | base (caçamba escura) | hero full-bleed com texto embaixo, feature |
| `crop-sent-sep24-stable-horse.jpg` | homem de flanela marrom no estábulo, cavalo com máscara ao lado | 1200x748 | nenhuma | foto rasgada (E26: `e26-torn-stable.jpg`), colagem (E22) |
| `crop-sent-sep2-hunter-blind.jpg` | caçador de boné laranja Habit saindo do blind com rifle, primeiro plano desfocado | 1081x1276 | base (desfoque claro, pede texto escuro ou degradê) | feature vertical, colagem, E26 |
| `crop-sent-sep10-utv-hunter-standing.jpg` | caçador em Realtree de pé ao lado do UTV (vertical) | 465x1115 | nenhuma | colagem (peça alta) |
| `crop-sent-sep10-family-walking-card.jpg` | a mesma família de costas, plano mais aberto e baixa resolução | 900x374 | topo (mata escura) | colagem pequena; para hero usar `sep15-family-forest-walk` |
| `crop-sent-sep24-hay-bale-seated.jpg` | homem de flanela sentado no fardo de feno com luvas amarelas (desrotacionado de 6,4°) | 405x698 | nenhuma | colagem (E22), E26 pequena |
| `crop-sent-sep22-sunset-boat-pocket.jpg` | detalhe da calça Habit (bolso, logo bordado) no barco, contraluz de pôr do sol | 592x662 | nenhuma | colagem, detalhe de produto em uso |
| `crop-sent-sep22-fly-tying.jpg` | mãos amarrando mosca, camisa xadrez de pesca | 594x450 | nenhuma | colagem, detalhe |
| `crop-sent-sep22-boat-anglers.jpg` | três pescadores de azul no barco, pesca de mosca | 594x254 | topo (margem escura) | colagem (faixa larga) |
| `crop-sent-sep22-canoe-river.jpg` | proa de canoa num rio verde fechado de mata | 326x434 | topo (céu claro) | colagem |
| `crop-sent-sep22-trout-in-hand.jpg` | truta na mão, água ao fundo | 316x484 | nenhuma | colagem |
| `crop-sent-sep22-wading-river.jpg` | pescador andando no rio raso, céu azul limpo | 304x434 | topo (céu, o mais limpo) | colagem |

**Resumo:** 17 recortes. Bons para hero full-bleed: `sep15-family-forest-walk` e `sep24-barn-door-feed-bag` (os dois já compostos no E24/E24B), mais `sep22-angler-tackle-box`, `sep10-utv-hunters` e `sep10-truck-hunter` com área de texto gerada ou com degradê. O resto serve para colagem, E26 e feature. Só dois recortes passam de 1000px de altura. A limitação é a resolução: todo hero full-bleed precisa de área calma gerada, porque os e-mails enviados já tinham texto em cima da parte calma da foto.

Não aproveitados: o hero de Sep 2 (paisagem coberta por packshots e texto), a mata atrás do card de Sep 15 (só sobram bordas de 50px) e o hero de Sep 24 acima da porta (texto em cima de toda a parede).

Script dos recortes: `email-kit/tools/crop_sent.py` (roda de novo e refaz os 17). Caixas em pixels do print de 1200px, remoção da linha desenhada por componente conexo mais retoque por mediana em áreas limitadas.
