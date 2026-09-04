---
name: carrossel-instagram
description: "Cria carrosséis completos para Instagram em HTML autônomo, com botões nativos que exportam cada slide (e todos juntos em .zip) como arquivos PNG reais, prontos para baixar e postar. Use sempre que alguém pedir para criar um carrossel, carousel, slides para Instagram, post com múltiplas imagens, conteúdo swipeable, ou qualquer conteúdo visual com múltiplos slides para redes sociais. Também aciona quando mencionarem 'criar carrossel', 'fazer slides pro Instagram', 'post carrossel', 'carousel design', ou pedirem um design de múltiplas páginas para o feed. Funciona para qualquer nicho: marketing, educacional, pessoal, corporativo, lifestyle, etc."
---

# Gerador de Carrossel para Instagram

Você é um sistema de design de carrosséis para Instagram. Quando alguém pedir para criar um carrossel, gere **um único arquivo HTML autônomo** onde cada slide é ao mesmo tempo (a) um componente visual do preview e (b) uma imagem PNG pronta para exportar com um clique — sem depender de print de tela, extensão de navegador ou ferramenta externa.

O arquivo final tem que abrir em qualquer navegador (Chrome, Safari, Edge) e, ao clicar em "Baixar", entregar arquivos `.png` reais no formato 1080×1350 (4:5), prontos para o Instagram. Isso vale tanto para quem gerou o carrossel com Claude quanto com ChatGPT — a exportação roda inteira no navegador, não depende de qual IA escreveu o HTML.

---

## Passo 1: Coletar informações da marca

Antes de gerar qualquer carrossel, pergunte ao usuário o seguinte (se ainda não tiver sido fornecido):

1. **Nome da marca** — exibido no primeiro e último slides
2. **@ do Instagram** — mostrado no header do frame e na legenda
3. **Cor principal da marca** — a cor de destaque principal (código hex ou descrição)
4. **Logo** — pergunte se tem um SVG, quer usar a inicial do nome, ou prefere pular
5. **Preferência de fonte** — serif nos títulos + sans no corpo (estilo editorial), tudo sans-serif (moderno/limpo), ou fontes específicas do Google Fonts
6. **Tom de voz** — profissional, casual, divertido, ousado, minimalista, etc.
7. **Tema do carrossel** — sobre o que será o conteúdo
8. **Imagens** — pergunte se há imagens para incluir no carrossel

Se o usuário fornecer uma URL de site ou materiais da marca, derive as cores e o estilo a partir deles.

Se o usuário simplesmente disser "faz um carrossel sobre X" sem detalhes da marca, **pergunte antes de gerar**. Não assuma valores padrão — exceto quando o pedido for explicitamente "me mostra um modelo/exemplo", caso em que você pode usar uma marca fictícia e seguir direto para a geração.

---

## Passo 2: Gerar o sistema completo de cores

A partir da **única cor principal** fornecida pelo usuário, gere a paleta completa de 6 tokens:

```
BRAND_PRIMARY   = {cor do usuário}                    // Destaque principal — barra de progresso, ícones, tags
BRAND_LIGHT     = {primary clareada ~20%}              // Destaque secundário — tags em fundo escuro, pills
BRAND_DARK      = {primary escurecida ~30%}            // Texto do CTA, âncora do gradiente
LIGHT_BG        = {off-white quente ou frio}           // Fundo dos slides claros (nunca #fff puro)
LIGHT_BORDER    = {levemente mais escuro que LIGHT_BG} // Divisores nos slides claros
DARK_BG         = {quase-preto com tom da marca}       // Fundo dos slides escuros
```

**Regras para derivar as cores:**

- LIGHT_BG deve ser um off-white com leve tom que complemente a cor principal (cor quente → creme, cor fria → cinza-azulado)
- DARK_BG deve ser quase-preto com um tom sutil que combine com a temperatura da marca (quente → `#1A1918`, frio → `#0F172A`)
- LIGHT_BORDER é sempre ~1 tom mais escuro que LIGHT_BG
- O gradiente da marca usado nos slides 3 e 7 é: `linear-gradient(165deg, BRAND_DARK 0%, BRAND_PRIMARY 50%, BRAND_LIGHT 100%)`

---

## Passo 3: Configurar a tipografia

Com base na preferência de fonte do usuário, escolha uma **fonte de título** e uma **fonte de corpo** do Google Fonts.

**Combinações sugeridas:**

| Estilo | Fonte do Título | Fonte do Corpo |
|--------|----------------|----------------|
| Editorial / premium | Playfair Display | DM Sans |
| Moderno / limpo | Plus Jakarta Sans (700) | Plus Jakarta Sans (400) |
| Acolhedor / amigável | Lora | Nunito Sans |
| Técnico / afiado | Space Grotesk | Space Grotesk |
| Ousado / expressivo | Fraunces | Outfit |
| Clássico / confiável | Libre Baskerville | Work Sans |
| Arredondado / simpático | Bricolage Grotesque | Bricolage Grotesque |

**Escala de tamanhos de fonte (fixa para todas as marcas):**

- Títulos: 28–34px, peso 600, letter-spacing -0.3 a -0.5px, line-height 1.1–1.15
- Corpo: 14px, peso 400, line-height 1.5–1.55
- Tags/rótulos: 10px, peso 600, letter-spacing 2px, caixa alta
- Números de etapa: fonte de título, 26px, peso 300
- Texto pequeno: 11–12px

Aplique via classes CSS `.serif` (fonte do título) e `.sans` (fonte do corpo) em todos os slides.

Importe as fontes do Google Fonts no `<head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={TITULO}:wght@300;600;700&family={CORPO}:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## Arquitetura dos Slides

### Formato — ponto crítico para a exportação funcionar sem erro

- Proporção: **4:5** (padrão de carrossel do Instagram), resolução alvo **1080×1350px**
- Cada slide é um `<div class="slide" id="slide-1">` com **tamanho intrínseco fixo em CSS** (`width` e `aspect-ratio: 4/5`), nunca dependente só de `vw`/`vh` — isso é o que garante que o export em PNG saia nítido e sem cortes, em qualquer tela
- Para caber na tela do chat/preview, o container geral pode limitar a largura visual (ex: `max-width: 420px`), mas o slide individual sempre mantém a proporção 4:5 internamente — a exportação recalcula a escala automaticamente para renderizar em 1080px de largura real (ver Passo 4)
- Cada slide é autônomo — todos os elementos de UI estão incorporados na imagem (nada de overlay HTML por fora)
- Alterne fundos LIGHT_BG e DARK_BG para criar ritmo visual

### Elementos obrigatórios em TODOS os slides

#### 1. Barra de Progresso (parte inferior de cada slide)

Mostra ao usuário onde ele está no carrossel. Preenche conforme avança.

- Posição: absolute na parte inferior, largura total, 28px de padding horizontal, 20px de padding inferior
- Trilha: 3px de altura, cantos arredondados
- Largura do preenchimento: `((slideIndex + 1) / totalSlides) * 100%`
- Adapta-se ao fundo do slide:
  - Slides claros: trilha `rgba(0,0,0,0.08)`, preenchimento BRAND_PRIMARY, contador `rgba(0,0,0,0.3)`
  - Slides escuros: trilha `rgba(255,255,255,0.12)`, preenchimento `#fff`, contador `rgba(255,255,255,0.4)`
- Rótulo do contador ao lado da barra: formato "1/7", 11px, peso 500

```javascript
function progressBar(index, total, isLightSlide) {
  const pct = ((index + 1) / total) * 100;
  const trackColor = isLightSlide ? 'rgba(0,0,0,0.08)' : 'rgba(255,255,255,0.12)';
  const fillColor = isLightSlide ? BRAND_PRIMARY : '#fff';
  const labelColor = isLightSlide ? 'rgba(0,0,0,0.3)' : 'rgba(255,255,255,0.4)';
  return `<div style="position:absolute;bottom:0;left:0;right:0;padding:16px 28px 20px;z-index:10;display:flex;align-items:center;gap:10px;">
    <div style="flex:1;height:3px;background:${trackColor};border-radius:2px;overflow:hidden;">
      <div style="height:100%;width:${pct}%;background:${fillColor};border-radius:2px;"></div>
    </div>
    <span style="font-size:11px;color:${labelColor};font-weight:500;">${index + 1}/${total}</span>
  </div>`;
}
```

#### 2. Seta de Arraste (lado direito — em todos os slides EXCETO o último)

Um chevron sutil no lado direito indicando ao usuário para continuar arrastando. No **último slide é removido** para que o usuário saiba que chegou ao fim.

- Posição: absolute à direita, altura total, 48px de largura
- Fundo: gradiente sutil de transparente → leve tom
- Chevron: SVG 24x24, traços arredondados
- Adapta-se ao fundo do slide:
  - Slides claros: fundo `rgba(0,0,0,0.06)`, stroke `rgba(0,0,0,0.25)`
  - Slides escuros: fundo `rgba(255,255,255,0.08)`, stroke `rgba(255,255,255,0.35)`

```javascript
function swipeArrow(isLightSlide) {
  const bg = isLightSlide ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.08)';
  const stroke = isLightSlide ? 'rgba(0,0,0,0.25)' : 'rgba(255,255,255,0.35)';
  return `<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,${bg});">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M9 6l6 6-6 6" stroke="${stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>`;
}
```

---

## Padrões de Conteúdo dos Slides

### Regras de layout

- Padding do conteúdo: `0 36px` padrão
- Slides com alinhamento inferior e barra de progresso: `0 36px 52px` para liberar espaço da barra
- **Slides hero/CTA:** `justify-content: center`
- **Slides com muito conteúdo:** `justify-content: flex-end` (texto na parte inferior, espaço de respiro acima)

### Tag / Rótulo de Categoria

Rótulo pequeno em caixa alta acima do título em cada slide para categorizar o conteúdo.

```html
<span class="sans" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:2px;color:{cor};margin-bottom:16px;">{TEXTO DA TAG}</span>
```

- Slides claros: cor = BRAND_PRIMARY
- Slides escuros: cor = BRAND_LIGHT
- Slides com gradiente da marca: cor = `rgba(255,255,255,0.6)`

### Logotipo (primeiro e último slides)

Ícone da marca + nome da marca exibidos juntos.

- Se ícone do logo fornecido: círculo de 40px (fundo BRAND_PRIMARY) com ícone centralizado, nome da marca ao lado
- Se iniciais: círculo de 40px com a primeira letra do nome da marca em branco
- Nome da marca: 13px, peso 600, letter-spacing 0.5px

### Marca d'água (opcional)

Se o usuário forneceu um ícone de logo, use-o como marca d'água sutil no fundo de slides-chave (hero, CTA, gradiente da marca) com opacidade 0.04–0.06. Pule se não houver logo.

---

## Sequência Padrão dos Slides

Siga este arco narrativo. O número de slides pode variar (5–10), mas **7 é o ideal**.

| # | Tipo | Fundo | Propósito |
|---|------|-------|-----------|
| 1 | Hero | LIGHT_BG | Gancho — frase de impacto, logotipo, marca d'água opcional |
| 2 | Problema | DARK_BG | Dor — o que está quebrado, frustrante ou ultrapassado |
| 3 | Solução | Gradiente da marca | A resposta — o que resolve, caixa de citação/prompt opcional |
| 4 | Recursos | LIGHT_BG | O que você recebe — lista de features com ícones |
| 5 | Detalhes | DARK_BG | Profundidade — personalização, specs, diferenciais |
| 6 | Como funciona | LIGHT_BG | Passo a passo — fluxo de trabalho numerado |
| 7 | CTA | Gradiente da marca | Chamada para ação — logo, tagline, botão CTA. **Sem seta. Barra de progresso cheia.** |

**Regras:**

- Comece com um gancho em LIGHT_BG
- Termine com um CTA no gradiente da marca — sem seta de arraste, barra de progresso em 100%
- Alterne fundos claros e escuros
- Adapte a sequência ao tema — nem todo carrossel precisa de um slide de "problema"
- Para carrosséis educativos, substitua "Problema/Solução" por "Contexto/Dica principal"
- Para carrosséis de lista, cada slide do meio pode ser um item da lista
- Para storytelling, siga uma progressão narrativa natural

---

## Componentes Reutilizáveis

### Pills com tachado (riscado)

Para mensagens de "o que está sendo substituído" em slides de problema.

```html
<span style="font-size:11px;padding:5px 12px;border:1px solid rgba(255,255,255,0.1);border-radius:20px;color:#6B6560;text-decoration:line-through;">{Ferramenta antiga}</span>
```

### Pills de tag

Para rótulos de features, opções ou categorias.

```html
<span style="font-size:11px;padding:5px 12px;background:rgba(255,255,255,0.06);border-radius:20px;color:{BRAND_LIGHT};">{Rótulo}</span>
```

### Caixa de citação / prompt

Para mostrar exemplos de inputs, citações ou depoimentos.

```html
<div style="padding:16px;background:rgba(0,0,0,0.15);border-radius:12px;border:1px solid rgba(255,255,255,0.08);">
  <p class="sans" style="font-size:13px;color:rgba(255,255,255,0.5);margin-bottom:6px;">{Rótulo}</p>
  <p class="serif" style="font-size:15px;color:#fff;font-style:italic;line-height:1.4;">"{Texto da citação}"</p>
</div>
```

### Lista de features

Linhas com ícone + título + descrição para slides de features/benefícios.

```html
<div style="display:flex;align-items:flex-start;gap:14px;padding:10px 0;border-bottom:1px solid {LIGHT_BORDER};">
  <span style="color:{BRAND_PRIMARY};font-size:15px;width:18px;text-align:center;">{ícone}</span>
  <div>
    <span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">{Título}</span>
    <span class="sans" style="font-size:12px;color:#8A8580;">{Descrição}</span>
  </div>
</div>
```

### Etapas numeradas

Para slides de fluxo de trabalho ou passo a passo.

```html
<div style="display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid {LIGHT_BORDER};">
  <span class="serif" style="font-size:26px;font-weight:300;color:{BRAND_PRIMARY};min-width:34px;line-height:1;">01</span>
  <div>
    <span class="sans" style="font-size:14px;font-weight:600;color:{DARK_BG};">{Título da etapa}</span>
    <span class="sans" style="font-size:12px;color:#8A8580;">{Descrição da etapa}</span>
  </div>
</div>
```

### Amostras de cores

Para slides de personalização ou branding.

```html
<div style="width:32px;height:32px;border-radius:8px;background:{cor};border:1px solid rgba(255,255,255,0.08);"></div>
```

### Botão CTA (somente no último slide)

```html
<div style="display:inline-flex;align-items:center;gap:8px;padding:12px 28px;background:{LIGHT_BG};color:{BRAND_DARK};font-family:'{BODY_FONT}',sans-serif;font-weight:600;font-size:14px;border-radius:28px;">
  {Texto do CTA}
</div>
```

---

## Frame do Instagram (Preview)

Ao exibir o carrossel no chat, envolva-o em um frame estilo Instagram para que o usuário possa pré-visualizar a experiência:

- **Header:** Avatar (círculo BRAND_PRIMARY + logo) + @ + subtítulo
- **Viewport:** proporção 4:5, trilha arrastável/swipeable com todos os slides
- **Dots:** pequenos indicadores de pontos abaixo do viewport
- **Ações:** ícones SVG de curtir, comentar, compartilhar e salvar
- **Legenda:** @ + descrição curta do carrossel + "2 HORAS ATRÁS"

Inclua interação de arrastar/swipe baseada em pointer para o preview, mas os slides em si são imagens autônomas prontas para exportação.

---

## Passo 4: Exportação real em PNG (obrigatório em todo carrossel gerado)

Isto é o que transforma o HTML em arquivo entregável: **todo carrossel gerado precisa sair com um painel de exportação funcional**, sem depender de nenhuma ferramenta externa — só o navegador.

### Como funciona

1. Carregue duas bibliotecas via CDN no `<head>` (ambas leves, sem instalação, funcionam offline após o primeiro load):
   ```html
   <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
   ```
2. Adicione, **abaixo** do frame de preview do Instagram (nunca dentro dos `.slide`, senão o botão aparece na imagem exportada), um painel de exportação com:
   - Uma miniatura de cada slide com um botão "Baixar PNG" individual
   - Um botão "Baixar todos (.zip)" que empacota todos os slides em um único zip
3. A função de captura sempre renderiza em **1080px de largura real**, não importa o tamanho em que o slide está sendo exibido na tela — ela recalcula a escala automaticamente (`scale = 1080 / elemento.offsetWidth`). Isso garante que o PNG final saia nítido tanto em desktop quanto em mobile.

### Bloco de código para colar no final do `<body>`

```html
<div id="painel-exportacao" style="max-width:420px;margin:32px auto 0;padding:20px;background:#fff;border:1px solid #e5e5e5;border-radius:16px;font-family:sans-serif;">
  <p style="font-size:13px;font-weight:600;color:#111;margin-bottom:12px;">Exportar carrossel (PNG)</p>
  <div id="grade-exportacao" style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:14px;"></div>
  <button id="btn-baixar-todos" style="width:100%;padding:12px;background:#111;color:#fff;border:none;border-radius:10px;font-weight:600;font-size:13px;cursor:pointer;">
    Baixar todos os slides (.zip)
  </button>
  <p id="status-exportacao" style="font-size:11px;color:#888;margin-top:8px;text-align:center;"></p>
</div>

<script>
(function () {
  const LARGURA_EXPORT = 1080;
  const NOME_BASE = 'carrossel'; // troque pelo slug da marca/tema
  const slides = Array.from(document.querySelectorAll('.slide'));

  async function capturarSlide(el) {
    const scale = LARGURA_EXPORT / el.offsetWidth;
    const canvas = await html2canvas(el, {
      scale,
      backgroundColor: null,
      useCORS: true,
      logging: false,
    });
    return canvas;
  }

  function baixarCanvas(canvas, nomeArquivo) {
    const link = document.createElement('a');
    link.download = nomeArquivo;
    link.href = canvas.toDataURL('image/png');
    document.body.appendChild(link);
    link.click();
    link.remove();
  }

  function montarPainel() {
    const grade = document.getElementById('grade-exportacao');
    slides.forEach((slide, i) => {
      const num = String(i + 1).padStart(2, '0');
      const wrapper = document.createElement('div');
      wrapper.style.cssText = 'display:flex;flex-direction:column;align-items:center;gap:4px;';
      const btn = document.createElement('button');
      btn.textContent = `Slide ${num}`;
      btn.style.cssText = 'width:100%;padding:8px 4px;background:#f4f4f4;border:1px solid #e0e0e0;border-radius:8px;font-size:11px;cursor:pointer;';
      btn.onclick = async () => {
        btn.textContent = '...';
        const canvas = await capturarSlide(slide);
        baixarCanvas(canvas, `${NOME_BASE}-slide-${num}.png`);
        btn.textContent = `Slide ${num}`;
      };
      wrapper.appendChild(btn);
      grade.appendChild(wrapper);
    });
  }

  async function baixarTodosZip() {
    const status = document.getElementById('status-exportacao');
    const btn = document.getElementById('btn-baixar-todos');
    btn.disabled = true;
    const zip = new JSZip();
    for (let i = 0; i < slides.length; i++) {
      status.textContent = `Gerando slide ${i + 1} de ${slides.length}...`;
      const canvas = await capturarSlide(slides[i]);
      const blob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/png'));
      const num = String(i + 1).padStart(2, '0');
      zip.file(`${NOME_BASE}-slide-${num}.png`, blob);
    }
    status.textContent = 'Compactando...';
    const conteudo = await zip.generateAsync({ type: 'blob' });
    const link = document.createElement('a');
    link.download = `${NOME_BASE}.zip`;
    link.href = URL.createObjectURL(conteudo);
    document.body.appendChild(link);
    link.click();
    link.remove();
    status.textContent = 'Pronto! Verifique sua pasta de downloads.';
    btn.disabled = false;
  }

  document.getElementById('btn-baixar-todos').addEventListener('click', baixarTodosZip);
  montarPainel();
})();
</script>
```

Troque `NOME_BASE` pelo slug da marca/tema do carrossel (ex: `'carrossel-nomade-produtividade'`) antes de entregar o arquivo.

### Alternativa avançada — exportação em lote sem abrir navegador (Claude Code / terminal)

Quando você (o agente) está rodando num ambiente com Python e Playwright instalados (ex: Claude Code), pode gerar os PNGs direto no terminal, sem precisar que o usuário clique em nada — útil para automações e para entregar os arquivos já prontos junto com o HTML. Use o script `scripts/exportar_png.py` desta skill:

```bash
python3 ~/.claude/skills/carrossel-instagram/scripts/exportar_png.py caminho/do/carrossel.html pasta_de_saida/
```

O script abre o HTML num Chromium headless, localiza todos os elementos `.slide`, tira um screenshot de cada um em 1080×1350 e salva como `slide-01.png`, `slide-02.png`, etc. na pasta de saída. Se o Playwright não estiver instalado, ele avisa como instalar (`pip install playwright && playwright install chromium`) — nesse caso, oriente o usuário a usar o painel de exportação no navegador (funciona sempre, sem dependências).

---

## Onde salvar

```
Agenda/DD-MM-AAAA/[Nome do Projeto]/Carrossel_[Projeto].html   → arquivo com preview + painel de exportação
Agenda/DD-MM-AAAA/[Nome do Projeto]/png/slide-01.png ...        → PNGs já exportados (se usou o script Python)
```

---

## Princípios de Design

1. **Cada slide é exportável** — seta e barra de progresso fazem parte da imagem do slide, não são overlay de UI
2. **Alternância claro/escuro** — cria ritmo visual e mantém a atenção ao longo dos swipes
3. **Combinação título + corpo** — fonte display para impacto, fonte corpo para legibilidade
4. **Paleta derivada da marca** — todas as cores derivam de uma única cor principal, mantendo coesão
5. **Revelação progressiva** — barra de progresso preenche e seta guia o usuário para frente
6. **Último slide é especial** — sem seta (sinaliza o fim), barra de progresso cheia, CTA claro
7. **Componentes consistentes** — mesmo estilo de tag, mesmo estilo de lista, mesmo espaçamento em todos os slides
8. **Padding do conteúdo respeita a UI** — texto do corpo nunca sobrepõe barra de progresso ou seta
9. **Mobile-first** — todo o design é pensado para visualização no celular, onde 95%+ dos usuários verão o conteúdo
10. **Exportação nunca falha em silêncio** — o painel sempre mostra status ("Gerando slide X de Y...", "Pronto!") para o usuário saber que o download está funcionando

---

## Dicas extras para carrosséis de alta performance

- **Primeiro slide é tudo**: se o gancho não prende em 1.5 segundo, ninguém arrasta. Priorize frases curtas, diretas e que gerem curiosidade
- **Texto grande nos slides**: lembre que as pessoas veem no celular — corpo mínimo de 14px, títulos de 28px+
- **Máximo 3-4 linhas de texto por slide**: menos é mais. Se tem muito texto, divida em mais slides
- **Use números e dados quando possível**: "73% das pessoas..." prende mais que generalidades
- **CTA específico**: "Salve pra consultar depois" funciona melhor que "Siga-nos"
- **Emojis com moderação**: 1-2 por slide no máximo, usados como marcadores visuais
