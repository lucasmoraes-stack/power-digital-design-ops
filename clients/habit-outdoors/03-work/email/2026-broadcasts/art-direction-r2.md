# Rodada 2 · direção de arte

Feedback do responsável (2026-09-24) sobre a rodada 1: "tímidos, sem texturas, sem imagens fullscreen de background, sem os efeitos de rasgo, ainda falta alma. Use as referências da Duck Camp."

A rodada 1 seguiu o kit ao pé da letra: bandas chapadas, fotos em card com cantos arredondados, cards de produto em grade. **A rodada 2 troca contenção por atmosfera.** A estrutura continua a mesma (copy do cliente, 7 bandas, um destino, texto vivo), mas o tratamento visual muda.

Referências para abrir e olhar antes de desenhar (560px, em `scratchpad/habit/dc/`): `dc1-*` (avental: foto emoldurada e rasgada sobre paisagem, produto cortado na borda), `dc3-*` (moletons em leque sobre paisagem que escurece, colagem "Why We Like It"), `dc4-*` (degradê granulado, grupos de produto sobrepostos sangrando, rasgo no meio da banda, colagem de 4 fotos). Os e-mails da Habit (`refs/sep*.png`) continuam mandando em cor, logo, caixa-alta e rodapé.

## Os 7 princípios

1. **Nenhuma banda chapada.** Toda banda tem matéria: papel granulado, topográfico, camo desfocado, degradê atmosférico com grão. A cor sólida continua como `bgcolor` de fallback, e a textura vai por imagem de fundo (VML no Outlook). Branco puro sai: o claro é papel `#E2DDD9` com grão.
2. **Hero em tela cheia.** Foto de ponta a ponta, 600px de largura, sem card nem canto arredondado, com o texto por cima da área calma e um degradê para a cor da banda seguinte. Logotipo HABIT® branco **sobre a foto**, sem faixa branca de cabeçalho (é o que os e-mails enviados fazem). Onde a foto não tiver área calma, a headline vai numa faixa de degradê que nasce da própria foto.
3. **Rasgo em tudo que é fronteira.** Toda troca de banda é rasgada (E18) ou um produto atravessando o rasgo (E21). Foto dentro de banda tem pelo menos uma borda rasgada ou moldura de papel. Nenhuma fronteira reta no e-mail, exceto a do rodapé, se ficar melhor.
4. **Produto com peso.** Nada de grade de cards com contorno. Produtos em leque sobrepostos (E19), cortados pela borda do e-mail (E20) ou um por banda em tamanho grande (E23). Nome, tipo e preço em texto vivo perto de cada peça. Sombra suave, produto saindo da coluna.
5. **Colagem.** Pelo menos um momento por e-mail de fotos sobrepostas em molduras tortas (E22) ou de foto rasgada sobre textura.
6. **Escala.** Headline de hero maior (46 a 56px no desktop, a serifada em até 90px na palavra-chave). Respiro generoso entre blocos.
7. **Cada e-mail com clima próprio**, ditado pelo tema:
   - **01 Memorial Day:** calor, verão, fim de tarde. Paleta clara e quente, papel com grão, céu aberto, fogueira. Patriot Blue como banda de apoio.
   - **02 Stain & Odor Reset:** cru e sujo, de trabalho. Tap Shoe e Major Brown com grão pesado, rasgos, produtos empilhados como roupa jogada.
   - **03 Art of Being Unseen:** silencioso, mata fechada. Camo desfocado de fundo, verde Ivy Green e Tap Shoe, neblina, muito espaço vazio.
   - **04 Shoreline vs Deep Water:** dois mundos. Metade barro e mata (Major Brown, textura de terra), metade água aberta (Patriot Blue com textura de água), com o rasgo no meio como a linha da margem.

## Material disponível (não inventar foto)

- Fotos: só recortes dos 5 e-mails enviados (há mais do que o kit usa hoje: caçadores no UTV, família de costas, mosaico de pesca, pescador na água, barco, celeiro, estábulo, feno) e as imagens extras da loja. Recortar o que der em `clients/habit-outdoors/01-brand/photos/lifestyle/` com prefixo `crop-sent-` (provisório, trocar pelo original). Foto da Duck Camp **nunca** entra.
- Texturas: gerar por script. Camo pode sair do próprio tecido dos packshots Realtree/Mossy Oak (recorte ampliado e desfocado). Topográfico: o do guia. Papel e grão: gerado.
- Packshots: `photos/products/<handle>--<variant>.png`, como na rodada 1.

## Limites técnicos (não negociáveis)

- Texto vivo sempre, inclusive sobre foto: imagem de fundo com VML + `bgcolor` de fallback que mantém o texto legível sozinho.
- Sobreposição, leque, sangria, rasgo e colagem = imagem composta por script, com a cor da banda nas bordas.
- Peso: até cerca de 800 KB por e-mail, cada imagem abaixo de 150 KB. Se estourar, reduzir o número de composições, não a ambição do hero.
- Botão `#FF6400` com texto `#2A2B2D`. Contraste AA do texto sobre a textura, medido na área onde o texto fica.
- Copy do cliente igual à rodada 1 (mesmos desvios registrados).
