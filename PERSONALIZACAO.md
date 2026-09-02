# Personalização do tema — Loja Bling/Tray

Camada de personalização aplicada sobre o tema **Perfumaria 8.8.16** fornecido
pela Tray/Bling. O objetivo foi modernizar a aparência e a organização da home
seguindo a estrutura de uma loja profissional (busca em destaque, menu de
categorias, faixa de vantagens, vitrines, passo a passo, rodapé completo),
aplicando a paleta da cliente — **sem** copiar textos, imagens ou identidade
visual de nenhum site de referência.

O histórico do repositório tem dois commits de propósito: o primeiro traz o
tema original intacto, o segundo traz a personalização. Assim dá para ver
exatamente o que mudou com `git diff`.

---

## 1. Paleta

Os quatro tons enviados pela cliente:

| Cor | Hex | Uso principal |
|---|---|---|
| Azul-petróleo escuro | `#0F2A36` | Barra superior, rodapé, títulos, textos e preços |
| Azul médio | `#3E6696` | Menu de categorias, links, ícones e apoios |
| Amarelo/ouro | `#EBBC19` | Botões de ação, selos de desconto, destaques |
| Areia | `#D3C3A2` | Fundos suaves e apoios secundários |

> **Observação sobre a paleta enviada:** no material da cliente o amarelo está
> rotulado como `1E1E1C`, mas esse código corresponde a um cinza quase preto e
> não bate com o RGB indicado ao lado (R:235 G:188 B:25). Prevaleceu o RGB, que
> equivale a `#EBBC19` — e é também o valor que já estava salvo nas
> configurações do tema. Os outros três rótulos conferem com o RGB.

---

## 2. Como as cores continuam editáveis

A personalização **não tem cor fixa no CSS**. O arquivo `css/custom.css.html`
(processado pela Tray a cada carregamento) publica as cores do painel como
variáveis CSS, e `css/redesign.css` consome essas variáveis:

```
--bl-deep  ← Configurações › Cores › Cor primária      (color_bg_pimaria)
--bl-blue  ← Configurações › Cores › Cor secundária    (color_bg_secundaria)
--bl-gold  ← Configurações › Cores › Vitrine › botão   (color_cta)
--bl-sand  ← Configurações › Cores › botão limpar      (color_button_clear)
```

Trocar qualquer uma dessas cores no painel do Bling repagina a loja inteira,
sem editar código.

---

## 3. Arquivos criados

| Arquivo | O que faz |
|---|---|
| `css/redesign.css` | Camada visual completa. Carregada por último, depois de `theme.min.css` e `custom.css`, e organizada em 14 seções comentadas. |
| `elements/benefits-bar.html` | Faixa de 4 vantagens abaixo do banner principal. |
| `elements/category-grid.html` | Grade de atalhos por categoria, montada a partir das categorias reais da loja. |
| `elements/how-it-works.html` | Seção "Como funciona" em 4 passos. |

## 4. Arquivos alterados

| Arquivo | Alteração |
|---|---|
| `layouts/default.html` | Carrega `redesign.css` e a fonte Inter; insere a faixa de vantagens na home. |
| `pages/home.html` | Nova ordem das seções; insere a grade de categorias e o "Como funciona"; envolve os banners promocionais em grade. |
| `elements/header.html` | Bloco de atendimento (WhatsApp ou telefone) ao lado do carrinho. |
| `elements/horizontal-nav.html` | O item "+ Categorias" virou "Todas as categorias", com ícone. |
| `elements/showcase.html`, `elements/showcase-best-sellers.html` | Título decorativo em fonte cursiva substituído por um cabeçalho de seção com chapéu e link "Ver todos". |
| `elements/snippets/newsletter.html` | Textos configuráveis e formulário em linha. |
| `elements/snippets/search.html` | Placeholder mais claro e rótulos de acessibilidade. |
| `css/custom.css.html` | Publica os tokens de marca no `:root`. |
| `configs/settings.json` | 29 novas chaves (com valores padrão preenchidos). |
| `configs/settings.html` | Nova aba **Seções da Home** no painel. |

Nenhum arquivo foi removido e nenhuma funcionalidade do tema foi desligada:
carrinho, busca com sugestão, filtros, comparador, avaliações, selos,
newsletter, menu mobile, header flutuante e os scripts da Tray seguem intactos.

---

## 5. O que passou a ser editável no painel

Painel do tema → **Seções da Home**, com quatro abas:

- **Vantagens** — liga/desliga a faixa e edita os 4 títulos e descrições.
- **Categorias** — liga/desliga a grade, edita chapéu, título e quantas
  categorias exibir.
- **Como funciona** — liga/desliga a seção e edita os 4 passos.
- **Textos e links** — título e texto da newsletter, e a URL do link
  "Ver todos" de cada vitrine (em branco, o link não aparece).

---

## 6. Correções de layout incluídas

Ajustes feitos porque afetavam o uso real da loja:

- **Botão de comprar acessível no celular.** No tema original o botão do
  cartão de produto só aparecia no `hover`, ficando inalcançável em telas de
  toque. Agora fica sempre visível.
- **Vitrine "mais vendidos" sem buraco.** O `clear:left` inline do tema
  empurrava dois produtos para baixo e deixava metade da faixa vazia. A área
  virou grid: o banner ocupa duas linhas e os quatro produtos formam um 2×2 ao
  lado.
- **Cabeçalho em tablet (768–991px).** A busca era esmagada até sumir. Agora o
  logo e o carrinho ficam na primeira linha e a busca ocupa a segunda.
- **Botão de busca à direita.** O `pull-right` do tema deixava de valer com o
  formulário em flex; reposicionado com `order`.
- **Sem rolagem horizontal** em 360, 414, 768, 992, 1280 e 1440px.
- **Duas colunas de produto no celular**, em vez de uma.

---

## 7. Publicando na loja

1. Compacte o conteúdo desta pasta (os arquivos na raiz, não a pasta em si).
2. No Bling: **Loja virtual → Layout → Meus temas → Enviar tema**.
3. Publique o tema e depois abra **Personalizar** para revisar a nova aba
   *Seções da Home*.

Se preferir aplicar aos poucos, o mínimo necessário é: enviar
`css/redesign.css`, `css/custom.css.html` e `layouts/default.html`. As demais
alterações são incrementais e podem ir depois.

---

## 8. Tamanhos de imagem recomendados

| Slot | Onde aparece | Proporção sugerida |
|---|---|---|
| Banner principal | Topo da home | 1920 × 520 |
| Banner régua (`extra3` / `extra8`) | Abaixo do banner principal | 1920 × 160 |
| Banners promocionais (`extra4` / `extra9`) | Entre as vitrines | 2 peças de 760 × 260 |
| Banner lateral (`extra5`) | Ao lado de "Mais vendidos" | 600 × 700 (a arte nunca é cortada; sobra vira fundo neutro) |
| Imagem de categoria | Grade de categorias | 200 × 200, quadrada |

---

## 9. Um ponto para acompanhar

Em `pages/home.html`, nas consultas de produto que já vinham no tema original,
o filtro é escrito como `'filter': available` (variável indefinida) em vez de
`'filter': 'available'`. Isso vem do tema da Tray e **não foi alterado**, para
não mudar quais produtos aparecem nas vitrines. Se um dia uma vitrine trouxer
produtos indisponíveis, é aí que se ajusta.
