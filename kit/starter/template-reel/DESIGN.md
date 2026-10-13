# DESIGN: <nome-do-projeto> (a verdade do design para todas as cenas)

> **Como usar:** copie este arquivo para a raiz do seu projeto como `DESIGN.md`, troque `<nome-do-projeto>` no
> título e preencha a **tabela de assets** no fim com os arquivos do SEU vídeo. O resto (zonas, paleta, tipografia,
> superfícies, linguagem de motion e o contrato da sub-composição) já é o padrão: só mude se a sua referência pedir
> outra linguagem, e anote a mudança no `BRIEF.md`. Todo agente que constrói ou revisa uma cena lê este arquivo primeiro.
> Só as cenas leem este arquivo. As zonas da tela, a posição e as cores da legenda e o papel de fundo também estão
> escritos em `edit/build_index.py`, `edit/build_captions.py` e no bloco `COMMON` do `edit/workflow-cenas.js`: se mudar
> o formato (não só cores e fontes), adapte esses três também.

Visual de referência (no exemplo, o reel "Comenta PERSONAGEM" de @higgsfield.ai): tela dividida, com o talking head em
cima e um painel de papel claro embaixo, onde prints/cards sobem com blur, destaques lima, contagens e tipografia
cinética. Calmo, premium, *limpo*: o movimento é suave e seguro, nunca tremido. Tudo cai NA palavra falada.

## Tela e zonas (1080 × 1920, 30 fps)

| Zona | Faixa de y | Dono | Regra |
|---|---|---|---|
| CÂMERA | 0 – 780 | `index.html` | A camada da câmera fica ACIMA das cenas: o que uma cena pintar aqui fica escondido. |
| EMENDA (legenda) | 800 – 920 | `compositions/captions.html` | Sem texto das cenas. Cards só passam por aqui enquanto entram/saem. |
| PALCO | 940 – 1860 | as sub-composições das cenas | Conteúdo das cenas. Centro visual ≈ (540, 1340). |
| Área segura | x 70 – 1010, y 950 – 1680 | — | Texto e números importantes ficam dentro (a UI do Reels cobre os ~240 px de baixo e a coluna de ícones da direita). Decoração pode vazar. |

As cenas são **sub-composições transparentes de tela cheia** (1080×1920). O papel e o brilho lima de fundo são
pintados pelo `index.html` (persistentes); por isso as cenas NÃO pintam fundo inteiro (exceção: cenas de B-roll
pintam o vídeo sobre a área do palco, y 780–1920).

## Paleta (declare como variáveis CSS na raiz da cena)

```css
--paper:#F3F3F0;  /* fundo do painel (do index) */
--ink:#111113;    /* texto principal */
--ink2:#3A3A40;   /* texto secundário */
--mute:#7A7A82;   /* terciário/meta (só ≥ 24px; confira o contraste no papel) */
--line:#E2E2DC;   /* linhas finas em cards claros */
--card:#FFFFFF;   /* superfície de card claro */
--ui:#141416;     /* cards escuros de interface (prints de apps) */
--ui2:#1E1E22;    /* linhas elevadas dentro da UI escura */
--lime:#D4FF3A;   /* O acento (no exemplo, também a cor da marca do assunto) */
--limeInk:#141A00;/* texto sobre lima */
--plum:#6B2A6B;   /* cor de apoio de um momento específico (no exemplo, o personagem do criador) — só nesses momentos */
--red:#FF4A3D;    /* risco / "não", só isso */
--blue:#3D4EF2;   /* azul tirado de um print (no exemplo, a pílula da plataforma) */
```

Um único acento. Se trocar o lima, troque também no destaque da legenda (`build_captions.py`) e no brilho do papel
(`build_index.py`).

## Tipografia

Carregue as fontes com estas regras exatas (dentro do `<style>` do `<template>`; caminhos relativos à raiz do
projeto; copie `template-reel/fonts/*.woff2` para `assets/fonts/`):

```css
@font-face { font-family: "Geist"; src: url("assets/fonts/Geist-latin.woff2") format("woff2"); font-weight: 100 900; font-display: block; }
@font-face { font-family: "Geist Mono"; src: url("assets/fonts/GeistMono-latin.woff2") format("woff2"); font-weight: 100 900; font-display: block; }
```

| Papel | Fonte | Tamanho / peso / tracking |
|---|---|---|
| Número herói | Geist | 150–180px / 800 / -0.045em, `font-variant-numeric: tabular-nums` |
| Headline / cinética | Geist | 84–110px / 700 / -0.035em, line-height 1.0 |
| Título de card | Geist | 38–46px / 600 / -0.02em |
| Corpo em cards | Geist | 28–34px / 500 |
| Rótulo / tag / meta | Geist Mono | 24–30px / 500 / +0.04em, muitas vezes MAIÚSCULAS |

Voz em minúsculas, como na referência ("quem banca isso?"). Nunca use `<br>`; dimensione os contêineres com max-width.

## Superfícies

- **Card claro**: `background:#fff; border-radius:34px; box-shadow:0 34px 80px rgba(24,24,12,.16), 0 6px 18px rgba(24,24,12,.08);`
- **Card escuro de UI** (prints, janelas de app): `background:var(--ui); border-radius:30px; border:2px solid rgba(255,255,255,.07);` mesma sombra, porém mais forte (`rgba(10,10,0,.28)`).
- Imagens de print ficam dentro de um card com `overflow:hidden` e o raio do card.
- **Anel lima** (destacar uma região): caixa com posição absoluta, `border:6px solid var(--lime); border-radius:<raio do alvo + 8px>; box-shadow:0 0 0 10px rgba(212,255,58,.28), 0 10px 30px rgba(120,160,0,.25);`
- **Bloco lima** (destacar uma palavra): retângulo lima atrás da palavra, `border-radius:14px`, padding 6px 16px, cresce `scaleX 0→1` a partir da esquerda (`transform-origin:0 50%`); o texto em cima vira `--limeInk`.
- **Pílula**: `border-radius:999px; padding:14px 28px;` Geist 600 ou Geist Mono 500.
- **Chip** (atribuição do B-roll): `background:rgba(12,12,14,.62); color:#fff; border-radius:999px; padding:10px 26px 10px 10px;` avatar redondo de 40px + texto Geist 500 28px.

## Linguagem de motion (igual à referência)

- **ENTRADA = blur-rise**: de `{opacity:0, y:70, scale:.94, filter:"blur(16px)"}` → `{opacity:1, y:0, scale:1, filter:"blur(0px)"}`, 0.5s `power3.out`.
- **SAÍDA = blur-out**: para `{opacity:0, scale:1.04, filter:"blur(14px)"}`, 0.26s `power2.in`. A saída da cena tem que TERMINAR ≥ 1 frame antes do `data-duration` da cena (a janela do clip é semiaberta).
- **Foco puxado**: camadas fora de foco → `filter: blur(6px)`, `opacity:.35`, scale .97 (profundidade de campo). O elemento em foco salta para a frente (scale 1.06, sombra maior).
- **Destaque**: anéis/blocos entram com `back.out(2)` 0.3–0.4s. Contagens `power2.out` 0.6–1.0s.
- **Vivo enquanto segura**: todo card parado deriva devagar (scale +2–3% ou y −12px ao longo do hold, `ease:"none"`/`sine.inOut`). Nunca um quadro morto.
- Varie os easings dentro da cena (power3.out / back.out / expo.out / power2.inOut). Sobreponha entradas, stagger total ≤ 0.5s.
- Comece cada batida ~0.10s antes, para o movimento chegar no PICO na palavra falada (os cues do STORYBOARD.md são inícios de palavra, em tempo local da cena).
- Sem `Math.random`, sem `Date.now`, sem CSS `transition`, sem `repeat:-1`. Use `fromTo` com estado inicial explícito. Nunca anime width/height/top/left: use transforms (scale/x/y), clip-path ou máscaras.

## Contrato da sub-composição (copie exatamente)

```html
<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8" /></head><body>
<template>
  <style>
    @font-face { ... both faces ... }
    #SID-root { position:absolute; inset:0; overflow:hidden; font-family:"Geist", sans-serif; color:var(--ink); --ink:#111113; ...palette... }
    #SID-root .something { ... }   /* every selector prefixed with #SID-root */
  </style>
  <div id="SID-root" data-composition-id="SID" data-width="1080" data-height="1920">
    ... markup (ids prefixed "SID-") ...
  </div>
  <script>
    (function () {
      const R = document.getElementById("SID-root");
      const q = (s) => R.querySelector(s), qa = (s) => Array.from(R.querySelectorAll(s));
      const tl = gsap.timeline({ paused: true });
      const IN = (el, t, o = {}) => tl.fromTo(el,
        { opacity: 0, y: o.y ?? 70, x: o.x ?? 0, scale: o.s ?? 0.94, filter: `blur(${o.b ?? 16}px)` },
        { opacity: 1, y: 0, x: 0, scale: 1, filter: "blur(0px)", duration: o.d ?? 0.5, ease: o.e ?? "power3.out" }, t);
      const OUT = (el, t, o = {}) => tl.to(el,
        { opacity: 0, scale: o.s ?? 1.04, y: o.y ?? 0, filter: `blur(${o.b ?? 14}px)`, duration: o.d ?? 0.26, ease: "power2.in" }, t);
      const POP = (el, t, o = {}) => tl.fromTo(el, { opacity: 0, scale: o.from ?? 0.6 },
        { opacity: 1, scale: 1, duration: o.d ?? 0.4, ease: o.e ?? "back.out(2)" }, t);
      const fmt = (n) => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ".");   // 1000000 -> 1.000.000
      const COUNT = (el, from, to, t, d, pre = "", suf = "") => { const o = { v: from };
        tl.fromTo(o, { v: from }, { v: to, duration: d, ease: "power2.out", immediateRender: false,
          onUpdate: () => { el.textContent = pre + fmt(o.v) + suf; } }, t); };
      // TYPE: seek-safe typewriter (writes only when the visible char count changes)
      const TYPE = (el, text, t, d) => { const o = { n: 0 }; let last = -1;
        tl.fromTo(o, { n: 0 }, { n: text.length, duration: d, ease: "none", immediateRender: false,
          onUpdate: () => { const k = Math.round(o.n); if (k !== last) { last = k; el.textContent = text.slice(0, k); } } }, t); };

      /* ... choreography, all at scene-local seconds ... */

      window.__timelines["SID"] = tl;
    })();
  </script>
</template>
</body></html>
```

(`SID` = o id da cena, ex.: `s3-calc`.)

- Ponha o valor inicial (antes da contagem) no próprio texto do HTML, para o frame 0 estar certo (ex.: `<b id="SID-num">0</b>`), e string vazia nos alvos do TYPE.
- Mídia dentro de uma cena: `<video id="SID-x" src="assets/…" muted playsinline data-start="<s local>" data-duration="…" data-media-start="…" data-hf-media-start-basis="local">` (o `data-hf-media-start-basis="local"` é obrigatório: os tempos da mídia são locais da cena); mídia não precisa de `class="clip"`; nunca ponha `data-start` num ancestral de um vídeo. Anime uma `div` wrapper, nunca o tamanho da caixa do `<video>`.
- `<img>` sem `data-start` é só markup (sem tempo): o preferido para imagens paradas.

## Assets (caminhos relativos à raiz do projeto): PREENCHA

Uma linha por arquivo que as cenas podem usar. Os agentes só usam o que estiver nesta tabela, então escreva **o que
é** cada arquivo, o tamanho em px, a duração (vídeos) e **onde estão as coisas importantes** dentro dele (coordenadas
em px da imagem), para os anéis e os "gêmeos" HTML caírem no lugar certo.

| Caminho | Tamanho / duração | O que é, e onde está o que importa | Cena(s) |
|---|---|---|---|
| `assets/img/<print-da-plataforma>.png` | `<L×A>` | `<ex.: card da campanha; pílulas na base: "X" em x335–465 y430–463 …>` | `<s2>` |
| `assets/img/<logo>.png` | `<L×A, usar ≤ N px>` | `<ex.: ícone do app>` | |
| `assets/broll/<clipe>.mp4` | `<L×A, fps, duração; melhor trecho>` | `<ex.: perfil @…, legenda queimada em y≈… (cortar fora)>` | `<s1>` |
| `assets/img/<seu-ativo>.jpg` | | | |
| `media/take.mp4` (1440×2560) | | A câmera (você). É do `index.html`: as cenas nunca usam. | — |
| `assets/fonts/*.woff2` | | Geist e Geist Mono (copiadas de `template-reel/fonts/`) | todas |
| `assets/sfx/*.mp3` | | SFX colocados pelo `index.html`: as cenas NÃO adicionam áudio | — |

Exemplos reais de linhas bem preenchidas (do reel que originou este template):

| Caminho | O que |
|---|---|
| `assets/img/lp-hero.png` (1054×487) | Card da campanha "THE AI INFLUENCER INVASION" + selo "$1 million budget" (canto superior direito, cortado no topo) + 3 pílulas na base. Caixas das pílulas em px da imagem: AI Videos ONLY x335–465 y430–463 · Up to $2,000/Video x473–631 · $1 CPM x639–718 |
| `assets/img/lp-grid.png` (1054×566) | Grade do ranking de marcas (2 colunas × 5 linhas). Linha da marca líder = coluna da esquerda, primeira linha: x7–515, y8–92 (px da imagem) |
| `assets/broll/criador2-carro.mp4` (720×1280, 16.2s) | Personagem de IA num carro (legenda queimada na origem em y≈300–340: cortar fora) |
