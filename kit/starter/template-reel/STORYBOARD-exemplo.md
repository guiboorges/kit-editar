> **O que é este arquivo.** O storyboard real do exemplo 1 (um reel de 47,9 s com 8 cenas), usado como modelo. No
> seu projeto, o `STORYBOARD.md` é o **contrato** dos agentes que constroem as cenas: com os tempos, as posições e
> os estados de entrada e saída combinados, vários agentes trabalham em paralelo sem se falar e tudo encaixa.
>
> **Como escrever o seu** (o Claude Code escreve; você confere):
> 1. Uma frase do que o vídeo diz, e o layout global (câmera 0–780, legenda 800–920, palco 940–1860).
> 2. Uma **tabela de cenas**: id, tempo global (início–fim), batida, o que aparece no palco, por quê. Inclua as
>    janelas de câmera em tela cheia (elas não são cenas: quem faz é o `index.html`).
> 3. Um **frame block por cena**: `id`, `src` (`compositions/<id>.html`), `global_start`, `duration`, `rules`
>    (receitas citadas do `RECEITAS-DE-MOTION.md`), `cues` (cada palavra com o seu início em **tempo local** da cena:
>    tempo global − `global_start`, tirado do `edit/words.json`) e cada batida com **geometria exata** (posição,
>    tamanho, fonte, easing) e o tempo em que começa (~0,10 s antes da palavra).
> 4. As regras universais (nada na emenda, entrada/saída, pop em dois canais, um wrapper por responsabilidade,
>    nada parado, números só do print) e, onde uma cena passa para a outra, o estado combinado (HOLD, handoff).
>
> O corpo está em inglês (como os agentes leem melhor os nomes técnicos). Os assets, @perfis e números citados abaixo
> são do exemplo 1 e **não** vêm no kit (o @ do criador real foi trocado pelo marcador `@criador_1`): no seu
> storyboard, use só os seus. Os caminhos `assets/…` são relativos à
> raiz do projeto.

---

# STORYBOARD — personagem-reel (47.9s, 1080×1920, 30fps)

This video tells creators curious about AI that **companies pay in dollars for videos of people who don't exist — and making your own character takes under 5 minutes.**

Global layout: camera on top (0–780, `index.html`), seam captions (800–920, `captions.html`), scenes paint the STAGE (940–1860).
All cue times below are **scene-local seconds** = word start in the scene. Read `DESIGN.md` first — it is the design truth.

| Frame | Global | Beat | Stage | Why |
|---|---|---|---|---|
| 01 s1-hook | 0.00–4.67 | hook | AI-character B-roll + "ELE NÃO EXISTE" + "< 5 min" | Proves "gente que nem existe" while it's said; promise with a deadline |
| 02 s2-launchpoint | 4.67–11.20 | mechanism | Launchpoint campaign card → crisp pills pulled out: $1 CPM, AI Videos ONLY | Shows the platform + the two rules from the real print |
| 03 s3-calc | 11.20–16.13 | stakes | US$ 1 / 1.000 views → 1.000.000 views = US$ 1.000 | The money math, honest disclaimer |
| 04 s4-quem-banca | 16.13–21.03 | aha setup | search → "quem banca isso?" → ranking grid → Higgsfield #1 | Who pays: the tool itself |
| — fullcam | 21.03–22.03 | breath | camera goes full-screen on "e pensa comigo" (index.html) | Direct address resets attention |
| 05 s5-ciclo | 22.03–29.40 | aha | influencer ✕ vs personagem ✓ → "a ferramenta paga pela própria propaganda" | The insight in one picture |
| 06 s6-teste | 29.40–38.90 | proof | Claude window: connect Higgsfield (MCP) → prompt types → timer < 5 min → character sheet | Keeps the hook's promise |
| 07 s7-genjutsu | 38.90–43.10 | proof payoff | ORIGINAL × RESULTADO side-by-side (Genjutsu) | "esse sou eu, esse aqui é o personagem" |
| 08 s8-cta | 43.10–47.90 | CTA | Instagram comments sheet: types CLONE → DM banner | Keyword CTA |

---

## Frame 1
status: outline
id: s1-hook
src: compositions/s1-hook.html
global_start: 0.00
duration: 4.67
rules: kinetic-beat-slam (stamp), spring-pop-entrance (timer pill), svg-path-draw (timer ring)
cues: tem@0.03 empresa@0.19 pagando@0.65 por@1.09 vídeo@1.27 de@1.55 gente@1.67 que@1.95 nem@2.05 existe@2.17 | e@2.79 criar@2.89 leva@3.19 menos@3.44 de@3.67 5@3.88 minutos@4.18 (speech ends ~4.6)

Stage = full-bleed B-roll filling y 780–1920 (a wrapper div `top:780px; height:1140px; width:1080px; overflow:hidden`).
- 0.00–2.75 `assets/broll/criador1-rua.mp4` muted, data-media-start 7.0, object-fit cover, object-position 50% 35%. Wrapper drifts scale 1.06→1.0 over the shot (`ease:"none"`).
- 2.75–4.67 HARD CUT to `assets/broll/criador2-carro.mp4` muted, data-media-start 3.0, object-fit cover, object-position 50% 80% (hides the burned-in caption). Drift scale 1.0→1.05. A 2-frame white flash (opacity .55→0, 0.12s) on the cut.
- Darken the B-roll bottom with a soft gradient (rgba(0,0,0,0) at y 1500 → rgba(0,0,0,.45) at 1920) so chips read; also a very soft top gradient under the seam (y 780–960, rgba(0,0,0,.35)→0) so the white seam caption reads.
- Top-left tag on the B-roll (x 60, y 970): dark chip with a lime dot + Geist Mono "100% IA" (pops at 0.20).
- Attribution chip, centered at y≈1590: avatar-criador-1 + "@criador_1 · 120 mil seguidores" (IN at 0.35, y:30). At 2.75 it is replaced (hard cut, then a quick 0.25s rise) by avatar-criador-2 + "@criador_2 · 95 mil seguidores".
- 2.00 ("nem"): **stamp "ELE NÃO EXISTE"** — lime block, Geist 800 72px UPPERCASE limeInk, rotation −4°, center (540, 1300). Slam: from scale 1.7, opacity 0, blur 8 → scale 1, 0.22s `expo.out`, then a tiny settle (scale 1.0→1.03 over the hold). Gone at the 2.75 hard cut.
- 3.82 ("5"): **timer pill** at center (540, 1330): white pill 520×120, left a 72px stopwatch (SVG circle ring that draws 0→100% from 3.82 to 4.30 in lime on dark track), text "menos de 5 min" Geist 700 52px ink. POP from 0.6 with back.out(1.8). Hold with slow drift.
- 4.40–4.66: everything EXIT (blur-out, B-roll wrapper fades to 0 too so the paper shows for the next scene).

## Frame 2
status: outline
id: s2-launchpoint
src: compositions/s2-launchpoint.html
global_start: 4.67
duration: 6.53
rules: depth-of-field-blur (card recedes when pills pull out), spring-pop-entrance, asr-keyword-glow (pill highlights on the words)
cues: por@0.03 incrível@0.17 que@0.51 pareça@0.63 existe@0.97 uma@1.25 plataforma@1.38 chamada@1.88 launchpoint@2.22 | que@2.88 paga@3.03 por@3.27 view@3.43 e@3.69 ela@3.79 só@3.99 aceita@4.15 vídeos@4.96 feitos@5.60 por@5.94 IA@6.12 (ends ~6.45)

- 0.85 ("existe uma plataforma"): **campaign card** = `assets/img/lp-hero.png` inside a dark UI card, displayed 940 wide (scale .892 → 940×434), centered x, top at y 1060. ENTER blur-rise (y:120). Slow drift scale 1→1.03 until 2.8.
- 2.10 ("launchpoint"): **brand pill** above the card at y≈990: logo-launchpoint (56px, radius 14) + "Launchpoint" Geist 700 44px ink on a white pill. POP. A one-shot lime sheen passes over the card (ambient-glow-bloom sheen, 0.6s).
- 2.80 ("que paga por view"): FOCUS PULL — card moves up (y −40), scale .9, blur(5px), opacity .45; the brand pill stays sharp. The three pills are re-created in HTML (crisp) and "pulled out" of the card: they start at their in-card positions/size and travel to a row centered at y≈1450, each scaled to ~1.9× the in-card size (≈ font 30px, height 64px), stagger 0.06s, `power3.out` 0.5s. Pill look: fill var(--blue), 2px border rgba(255,255,255,.18), white Geist 600; text "AI Videos ONLY" (ONLY in 800), "Up to $2,000/Video", "$1 CPM".
- 3.03 ("paga"): lime ring pops around **$1 CPM**; mono label under the row at y≈1560: "= US$ 1 a cada 1.000 views" (IN y:20).
- 3.95 ("só aceita"): ring jumps to **AI Videos ONLY** (old ring blur-out 0.18s, new ring POP), label swaps (blur crossfade) to "= só aceita vídeo feito com IA". "Up to $2,000/Video" dims to opacity .3 (it's no longer the focus — campaign cap varies).
- 6.05 ("IA"): "AI Videos ONLY" pill flashes lime fill (background to lime, text limeInk) with a small scale punch 1→1.08→1.
- 6.22–6.50: EXIT everything.

## Frame 3
status: outline
id: s3-calc
src: compositions/s3-calc.html
global_start: 11.20
duration: 4.93
rules: counting-dynamic-scale, kinetic-beat-slam (lime result slam), card-morph-anchor (first line becomes the multiplier line)
cues: é@0.04 um@0.14 dólar@0.26 a@0.58 cada@0.70 mil@1.04 views@1.29 | ou@1.73 seja@1.87 | um@2.35 vídeo@2.47 desse@2.67 que@2.89 bate@3.01 um@3.25 milhão@3.31 você@3.59 consegue@3.79 mil@4.23 dólares@4.43 (ends ~4.8)

Layout = the reference's equation (centered, x center 540):
- 0.08: "US$ 1" Geist 800 170px ink at y≈1180 (IN, y:50). 0.62: "a cada 1.000 views" Geist 600 56px ink2 under it (IN).
- 2.25: MORPH — the "US$ 1 / a cada 1.000 views" group shrinks and slides to become the multiplier line "× US$ 1 a cada 1.000" (Geist 600 52px ink2) at y≈1330 (single-line, 0.45s power2.inOut). Simultaneously the hero line "1.000.000" + small "views" (Geist 500 40px mute, baseline-aligned) rises at y≈1180 and COUNTS 0 → 1.000.000 from 2.35 to 3.35 (counting-dynamic-scale: scale .9 → 1.0 as it counts).
- 4.15 ("mil dólares"): **result block** lime (radius 26, padding 18px 44px) with "US$ 1.000" Geist 800 150px limeInk at y≈1500; slams from scale 1.35 → 1 `expo.out` 0.3s, number counts 0→1.000 over 0.35s. A soft lime glow bloom behind it.
- 4.45: disclaimer Geist Mono 24px ink2 at y≈1640: "cálculo ilustrativo · só conta view elegível" (IN y:12, 0.3s).
- Hold: whole group drifts scale 1→1.02. 4.64–4.90 EXIT.

## Frame 4
status: outline
id: s4-quem-banca
src: compositions/s4-quem-banca.html
global_start: 16.13
duration: 4.90
rules: discrete-text-sequence (search typing), css-marker-patterns highlight (lime block on "banca"), depth-of-field-blur + spring-pop (Higgsfield row pops out of the grid)
cues: e@0.04 obviamente@0.14 eu@0.56 fui@0.60 verificar@0.74 | quem@1.51 é@1.69 que@1.75 banca@1.87 isso@2.11 tudo@2.23 | a@2.58 empresa@2.66 que@3.06 mais@3.20 paga@3.42 isso@3.78 é@4.18 higgsfield@4.30 (ends ~4.8)

- 0.08: **search bar** (white pill card 860×120 at y≈1250, magnifier icon left in ink2) IN. 0.30–1.30 TYPE "quem paga esses criadores?" in Geist 500 40px ink with a blinking-free solid caret (caret = 3px ink bar right after the text; move it with the text — or place it as an inline element after the typed span).
- 1.42: search bar blurs out up; **kinetic headline** builds centered at y≈1300, Geist 700 104px ink, 2 lines max-width 900: "quem" (1.45) "banca" (1.82) "isso?" (2.08), each word blur-rise y:40 0.3s. At 1.87 the lime block wipes behind "banca" (scaleX 0→1, 0.28s power3.out) and "banca" turns limeInk.
- 2.50: headline shrinks to 56px and moves to y≈1000 (keeps the lime block), 0.4s power2.inOut. **Ranking card** = `assets/img/lp-grid.png` in a dark UI card, 940 wide (×.892 → 940×505), top y≈1090, ENTER blur-rise.
- 3.35 ("paga"): focus pull on the grid (blur 5px, opacity .4, scale .97). A crisp HTML **Higgsfield row** (dark raised card #1E1E22, radius 22): logo-higgsfield 84px, "Higgsfield AI" Geist 600 40px white, "Best pay · Publicações ilimitadas" Geist 500 26px #9a9aa2, right "US$ 78–US$ 10.075" Geist 600 30px white + "per video" 22px #9a9aa2. It starts exactly over the row's place in the grid (left col, row 1) and lifts to center x, y≈1330, scale 1.12, with a big shadow (0.45s power3.out).
- 4.25 ("higgsfield"): lime ring around the row + lime pill tag "#1 · quem mais paga" (Geist Mono 26px limeInk) popping at the row's top-right corner, rotation 3°.
- 4.62–4.88 EXIT.

## Frame 5
status: outline
id: s5-ciclo
src: compositions/s5-ciclo.html
global_start: 22.03
duration: 7.37
rules: comparison-split (blueprint shape, adapted), svg-path-draw (strike line + loop arrow), kinetic-type-beats payoff with lime block
cues: ao@0.05 invés@0.11 dela@0.39 pagar@0.63 influencer@0.95 pra@1.73 falar@1.91 dela@2.25 | ela@2.77 paga@3.09 | por@3.69 um@3.89 serviço@4.01 que@4.61 é@4.71 feito@4.83 dentro@5.27 dela@5.71 | isso@6.13 faz@6.29 muito@6.54 mais@6.76 sentido@6.90 (ends ~7.3)

Two equal cards side by side (each 430×600, centers x 300 and 780, y center 1330), mirrored tilt (rotationY ±10° settling to ±4°, transformPerspective 1200):
- 0.10: LEFT card "influencer" enters from the left (x −80 → 0, blur-rise). Light card: top area 300px with a neutral gray avatar silhouette (SVG person in a #E7E7E2 circle 200px), mono label "INFLUENCER" (Geist Mono 24px mute), title "pagar influencer" Geist 600 40px, sub "pra falar dela" Geist 500 30px ink2 (sub IN at 1.80).
- 2.70 ("ela paga"): RIGHT card "personagem" enters from the right (mirrored). Top area = `personagem-retrato.jpg` (cover, object-position 50% 25%), 4px lime border on the card, small Higgsfield logo badge (64px, radius 16) on the photo's corner, mono label "PERSONAGEM DE IA" (limeInk on a lime pill), title "paga o personagem" Geist 600 40px.
- 2.85: the LEFT card gets a red strike line drawn diagonally across it (SVG line, stroke var(--red) 10px round, dashoffset draw 0.3s) + a red "✕" disc (56px) POPs at its top-right; the card dims (opacity .55, saturate .2 via `filter:grayscale(1)`), scale .94.
- 4.80 ("feito dentro dela"): right card sub "feito dentro dela" Geist 500 30px ink2 IN + a lime ring pulse on the right card; it scales 1.06 and moves toward center (x −40) — the winner.
- 6.05 ("isso faz muito mais sentido"): both cards EXIT (blur-out). **Payoff**: centered at y≈1150 a 150px Higgsfield logo tile with a lime circular arrow (SVG arc, ~300°, arrowhead) drawing around it (6.10–6.70, `power2.inOut`); below at y≈1420 kinetic text Geist 700 76px ink, max-width 900, centered: "a ferramenta paga pela própria propaganda" — words arrive in 2 quick groups ("a ferramenta paga pela" 6.15, "própria propaganda" 6.45), lime block wipes behind "própria propaganda" at 6.75.
- 7.10–7.35 EXIT.

## Frame 6
status: outline
id: s6-teste
src: compositions/s6-teste.html
global_start: 29.40
duration: 9.50
rules: device-surface-showcase (held app window, states cycle), control-target-sync (connector toggle ON on "higgsfield"), prompt-type-submit-generate, agent-progress-theater (generating shimmer), counting (timer)
cues: então@0.31 obviamente@0.67 que@1.11 eu@1.19 fui@1.23 testar@1.37 | liguei@1.83 pro@2.11 MCP@2.41 | do@3.23 claude@3.38 no@3.83 higgsfield@3.97 | e@4.86 detalhei@4.92 exatamente@5.32 como@5.78 eu@5.90 queria@6.00 esse@6.40 meu@6.54 personagem@6.66 de@7.16 IA@7.24 | em@7.63 menos@7.75 de@7.97 5@8.13 minutos@8.37 eu@8.69 tinha@8.79 ele@8.93 pronto@9.11

**App window** (light, Claude-like): white card 940×700, top y≈1010, radius 34. Header row 96px: logo-claude.svg 48px + "Claude" Geist 600 36px ink; right side a mono pill that appears later. Body area below a hairline.
- 0.25: window ENTER blur-rise (y:140). Body state A = **"Conectores"** list (Geist Mono 24px mute title "CONECTORES"), 3 rows 96px tall: "Google Drive" (simple gray drive glyph), "Higgsfield" (logo-higgsfield 56px), "Notion" (gray N tile). Each row has an iOS-style toggle on the right (OFF = #E2E2DC track, white knob).
- 1.40 ("testar"): small lime pill "teste real" pops at the window's top-right corner (rotation 4°).
- 2.38 ("MCP"): header mono pill "MCP" (ink on #EFEFEA, Geist Mono 26px) POP next to the title.
- 3.90 ("higgsfield"): Higgsfield row: lime ring around the row + toggle ON (knob x slides right 0.25s, track color → var(--lime)), status text "conectado" (Geist 500 26px, #4b7a00) fades in under "Higgsfield". (control-target-sync: knob + track + ring share one beat.)
- 4.80 ("e detalhei"): body crossfades (blur) to state B = **chat**: composer box at the bottom of the window (rounded 26px, #F6F6F2, 2px line) where the prompt TYPES from 4.92 to 7.30: "cria meu personagem: cabelo lilás na altura do ombro, bigode preto grosso, óculos redondos de metal, polo de tricô vinho e calça listrada" (Geist 500 30px ink, wraps within the composer; composer may grow by animating a mask — never height). Send button (ink circle with white ↑) presses at 7.36 (scale .88→1). The text then moves up into a user bubble (right-aligned, #EFEFEA) 7.40–7.60.
- 7.60 ("em menos de 5 minutos"): a response area below the bubble shows "gerando personagem…" (Geist Mono 24px) + 3 skeleton tiles shimmering (lime sheen sweep, finite). A **timer pill** pops above the window at y≈965 (lime, limeInk Geist Mono 30px, stopwatch glyph): counts "00:00" → "04:47" between 7.65 and 8.55 (format mm:ss from a seconds proxy 0→287).
- 8.65 ("eu tinha ele pronto"): window EXITS (blur-out, 0.25s) while the **character sheet card** (`personagem-sheet.jpg` in a white card, radius 34, no padding) grows out of the response area to its final hold: **x center 540, y center 1390, width 900 (height 509)**, 0.45s `power3.out`, with a brief lime flash border. 9.05 ("pronto"): lime pill "pronto ✓" POP at the card's top-left corner (x≈150, y≈1110). Timer pill stays.
- NO exit at the end: the sheet card + "pronto" pill + timer are held to 9.50 (scene s7 takes over from an identical card).

## Frame 7
status: outline
id: s7-genjutsu
src: compositions/s7-genjutsu.html
global_start: 38.90
duration: 4.20
rules: card-morph-anchor (sheet card → RESULTADO card), comparison-split, spring-pop-entrance (labels)
cues: como@0.08 vocês@0.22 podem@0.46 ver@0.66 | esse@0.98 sou@1.26 eu@1.46 | e@1.88 esse@2.02 aqui@2.30 é@2.58 o@2.66 personagem@2.72 (ends ~3.3; hold to 4.2)

- 0.00: starts with an IDENTICAL sheet card to s6's final state (x center 540, y center 1390, 900×509, `personagem-sheet.jpg`) + identical "pronto ✓" pill (x≈150,y≈1110) and timer pill (lime, "04:47", centered at y≈965). 0.05–0.30: pills blur out.
- 0.10–0.60: MORPH: sheet card shrinks/moves to the RIGHT slot (center x 770, y 1360, 400×640 portrait) and crossfades into the **RESULTADO** card (img `personagem-retrato.jpg` → id `s7-resultado`, object-fit cover; slow Ken Burns 1.0→1.08). (Placeholder until the Genjutsu result video arrives — keep the media box a simple element with id `s7-resultado` so it can be swapped for a `<video>`.)
- 0.55: **Genjutsu pill** POP at top center y≈990: dark pill (#141416) with logo-higgsfield 36px + "Genjutsu" Geist 600 30px white.
- 0.92 ("esse sou eu"): **ORIGINAL** card enters from the left into the LEFT slot (center x 310, y 1360, 400×640): `<video id="s7-original" src="media/t1-hook.mp4" muted playsinline data-start="0.92" data-duration="3.28" data-media-start="5.2">` object-fit cover, object-position 50% 45%, inside a radius-30 card wrapper. Label "ORIGINAL" Geist Mono 26px ink2 above the card (y≈1015) at 1.05.
- 2.00 ("esse aqui é o personagem"): label "RESULTADO" Geist Mono 26px limeInk on lime pill above the right card. 2.70: lime ring around the right card + a small sparkle burst (particle-burst, ≤ 12 lime dots, deterministic).
- Both cards hold with opposing gentle float (±8px, sine). 3.95–4.18 EXIT.

## Frame 8
status: outline
id: s8-cta
src: compositions/s8-cta.html
global_start: 43.10
duration: 4.80
rules: anchored-layout-expand (new comment pushes the list), discrete-text-sequence (typing CLONE), press-release-spring (send), spring-pop-entrance (DM banner)
cues: se@0.08 vocês@0.20 quiserem@0.48 criar@0.84 o@1.12 seu@1.24 | comente@1.48 aqui@1.86 | CLONE@2.20 | que@2.76 eu@2.84 envio@2.94 o@3.50 passo@3.60 a@3.82 passo@3.94 (ends ~4.3; hold to 4.8 = end of video)

**Instagram comments sheet** (white, radius 40 top corners and 40 bottom, width 940, centered, top y≈1080, height ≈560), like the reference:
- grabber bar (64×8, #DADAD4) + title "Comentários" Geist 600 34px centered; hairline.
- existing comment: avatar-criador-1 64px · "lucas.ia" Geist 600 28px + "2 min" mute 24px · text "esse cara não existe?? 😳" Geist 500 30px · "Responder" mute 22px · heart + "24" on the right.
- emoji row (❤️ 🙌 🔥 👏 😢 😍 😮 😂) 44px, spread.
- input row: avatar-gui 56px + input pill (#F3F3F0, radius 999) "Adicione um comentário…" mute; send button (blue #3D8BFF circle with white ↑) at the right, disabled look (opacity .4).
- 0.10: sheet ENTER blur-rise (y:160, 0.55s).
- 1.50 ("comente aqui"): input pill gets 2px ink outline (focus); placeholder hides.
- 2.02–2.32 TYPE "CLONE" (Geist 600 32px ink) into the input; send button becomes active (opacity 1) at 2.34 and presses at 2.48 (scale .85 → 1.0 back.out).
- 2.55: new comment row slides in at the TOP of the list (anchored-layout-expand: list content shifts down by the row height via y, never height): avatar-gui · "você" · "agora" · text "CLONE" in Geist 700 30px with a lime block behind it. Input clears.
- 2.95 ("envio"): **DM banner** drops in ABOVE the sheet at y≈960 (white card radius 28, 900×120, shadow): avatar-gui 64px · "guiborges" Geist 600 28px + "agora" mute · text "te mandei o link + o passo a passo pra criar o seu ✨" Geist 500 28px (max-width so it wraps to ≤2 lines). Enter: from y −60, opacity 0, blur 10 → settle, back.out(1.4).
- 3.60: lime pulse ring on the "CLONE" comment (one pulse). Hold everything to the end (no exit — last frame of the video), with a slow drift (sheet y −10 over the hold).
