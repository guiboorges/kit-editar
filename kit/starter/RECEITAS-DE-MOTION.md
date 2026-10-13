> **O que é este arquivo.** São 59 "receitas" de motion design com os números exatos (easing, duração, escala,
> blur, atrasos) que deram certo num reel real. Cada receita foi extraída do código final de uma das 8 cenas que
> estão neste kit em `template-reel/scenes-exemplo/` (s1-hook … s8-cta): há uma seção por cena, na mesma ordem.
>
> **Como usar com os prompts.** No `STORYBOARD.md` do seu vídeo, cada cena cita a cena-exemplo que vai adaptar e as
> receitas dela. Os agentes do workflow (`template-reel/edit/workflow-cenas.js`) leem a cena-exemplo e a seção
> correspondente aqui (arg `rec` do workflow). Você não precisa decorar nada: basta o storyboard apontar a
> cena-exemplo certa. Tempos são **locais da cena** (segundos desde o início dela); 'word' = início da palavra falada.
>
> O corpo está em inglês de propósito: mantém exatos os nomes de propriedades, easings e parâmetros do GSAP. Onde o
> texto abaixo diz `personagem-reel/compositions` ou `_template-reel/scenes-exemplo/`, leia
> `template-reel/scenes-exemplo/` deste kit (o personagem-reel é o exemplo 1, reel PERSONAGEM, pipeline A). As 11 cenas de `template-reel/scenes-exemplo-2/` não têm seção própria:
> cada uma adaptou estas receitas (ver a tabela no §7 do `PADRAO-DE-QUALIDADE.md`).

---

# Receitas de motion — extraídas do personagem-reel v1

Apêndice técnico do `PADRAO-DE-QUALIDADE.md`. Cada receita foi extraída do código final das cenas
(`personagem-reel/compositions/*.html`, cópias em `_template-reel/scenes-exemplo/`).
O corpo das receitas está em inglês para manter exatos os nomes de propriedades, easings e parâmetros do GSAP.

Convenções: tempos são **locais da cena** (segundos desde o início da cena); 'word' = início da palavra falada.

## Índice

- **s1-hook** — Punchy B-roll open + slow drift + impact punches (3-layer wrapper); Hard cut with 2-frame white flash + per-shot caption scrim; Glass tag spring pop + finite live-dot halo; Attribution chip rise + hard swap on the cut; Kinetic stamp slam + lime echo ring; Two-channel spring pop (opacity/blur on power2, scale on back.out); Stopwatch ring that drives a count-up readout (svg-path-draw + counter); Scene exit blur-out + B-roll fade to paper
- **s2-launchpoint** — Rack-focus card arrival (continuous from frame 0, snaps sharp on the word); One-shot lime sheen sweep across the card; Brand pill two-channel pop + drift; Focus pull (depth-of-field) — card recedes to a ghost; Pill pull-out from screenshot (print → HTML twin); Lime ring hug + label, ring jump between targets; ASR keyword glow driver (envelope-driven push); Hero promotion + flank rack focus; Lime block word highlight + clip-path lime wipe with punch; Exit
- **s3-calc** — Word-by-word build with live re-centering; Card-morph anchor: phrase reflows into the next line (FLIP by measured deltas); Counting with dynamic scale (count-up hero); Lime result slam (kinetic beat slam) + glow bloom + impact nudge; Ambient drift on a wrapper; Staggered blur-out exit, payoff holds longest
- **s4-quem-banca** — Search bar with discrete typewriter + caret + enter press; Kinetic headline with lime word-block and re-centering; Screenshot card entrance under a shrinking title; Pull-out of a crisp element from a screenshot (row lift) with focus pull; Rank tag + lime ring hug + scale punch; Exit
- **s5-ciclo** — Solo-then-split comparison (staged centre → slot); Card body that re-lays itself (group glides up when sub arrives); Strike-out the loser (path draw + X disc + desaturate); Brand badge pop + one-shot pulse ring; Lime ring hug for the winner; Cycle payoff: icon tile + self-drawing loop arrow; Kinetic 2-group sentence + lime block wipe
- **s6-teste** — Held app window with staggered row cascade; Corner sticker + header pill 'punch then cool'; Control-target sync (toggle ON + ring + status swap on one label); State crossfade with blur (A → B inside the same window); Typewriter with caret, authored line breaks and growing composer; Press-release send + text flies into bubble; Agent theater + count-up timer with spinning hand; Result card grows out of a skeleton tile (hand-off anchor)
- **s7-genjutsu** — Pixel-identical hand-off from previous scene (frame-0 replica); Card-morph (landscape sheet -> portrait card) with content zoom + locked crossfade; Live-media takeover with pull-back reveal (still -> video); Side-by-side synced video cards (ORIGINAL x RESULTADO) with book-open tilt; Label row: spring pops on spoken word, equal-gap anchors; Lime ring hug + punch + deterministic sparkle burst; Phase-opposed float while holding + clean exit
- **s8-cta** — Blur-rise sheet entrance + emoji wave; Input focus + discrete typewriter with caret (key-press synced); Send press-release spring + radial burst; FLIP word travel (typed text -> comment token) with lime block; Comment push-down (anchored-layout-expand via y); Two-channel drop-in (geometry on back.out, filter/opacity on power2.out); Lime ring + echo pulses + token punch + like, held to the end

## s1-hook

**Batida:** Hook (global 0.00-4.67, dur 4.67). Full-bleed B-roll of an AI character proves 'gente que nem existe' while it is said, then hard cut to the user's own AI character + a deadline promise ('menos de 5 minutos'). Cue grid (scene-local word starts): tem 0.03, pagando 0.65, vídeo 1.27, gente 1.67, nem 2.05, existe 2.17 | e 2.79, criar 2.89, menos 3.44, 5 3.88, minutos 4.18, speech ends ~4.6. Script constants: CUT=2.75, NEM=2.05, POP=3.76 (timer), FIVE=3.88, EXIT=4.42, XD=0.2.

**Layout:** 1080x1920, 30fps. Camera owns y 0-780 (sits ABOVE scenes, clip-path inset bottom 1140). Seam caption band y 800-920 (captions at top 812, height 96). This scene is a B-roll scene: wrapper top 780, 1080x1140, bg #0c0c0e (exception to 'scenes paint no background'). Tag top-right: right 70, top 970, h 60. Timer pill centered (540,1330), h 132. Stamp centered (540,1440). Chip row top 1554, h 72 (inside safe box x70-1010, y950-1680; Reels UI covers bottom ~240px and right icons). Camera keyword punch-in (index.html) also fires at global 2.05 (scale 1→1.05, 0.32s power2.out, from t−0.08, reset on next cut).

**SFX:** Scene global start 0.00 (global = local). Track 10 unless noted:
- 0.00 impact-bass-1.mp3 vol 0.10 → frame-0 B-roll punch-in open (1.09→1).
- 2.00 pop.mp3 vol 0.36 → stamp slam start (NEM−0.05).
- 2.75 whoosh-short.mp3 vol 0.22 → hard cut + white flash (CUT).
- 3.76 click.mp3 vol 0.35 → timer pill pop (POP).
- 4.18 ping.mp3 vol 0.22 → clock stops on 4:59 + lime sonar on 'minutos' (POP+RUN−0.08).
Next: 5.50 whoosh belongs to s2. Pattern: impact on open, pop on slam, whoosh on cut, click on UI pop, ping on the 'result/landing'. Volumes 0.1-0.36; bass hits very low (0.08-0.10).

### Punchy B-roll open + slow drift + impact punches (3-layer wrapper)

- **Quando usar:** Any scene that opens on footage: frame 0 must already be full and moving (no fade-in), and later beats need a 'hit' on the plate without fighting the drift.
- **Como:** Nest .broll (exit fade/blur, origin 50% 40%) > .punch (impact scale, origin 50% 42%) > .shot (per-shot drift) > <video>. punch: fromTo scale 1.09→1, 0.42s expo.out at 0. shot1 drift fromTo scale 1.06→1.0 over 0→CUT, ease none; shot2 drift 1.0→1.05 from CUT to 4.63, ease none. Impact punch on a beat: fromTo(punch,{scale:1},{scale:1.045,dur 0.05,power2.out,immediateRender:false}, NEM-0.06) then to(scale 1, 0.42s power3.out) at NEM-0.01. Second, smaller punch for the timer: 1.03, at POP+0.02, settle 0.4s power3.out at POP+0.07.
- **Tempo:** Punch peaks ~0.01s before the word start (NEM-0.06 + 0.05). Drifts run the full shot length.
- **Armadilhas:** Each transform channel lives on its own wrapper so the drift, the punch and the exit never overwrite each other. Punch from-state is the rest state (scale 1) with immediateRender:false, so seeking backwards stays correct. Never animate the <video> box itself.

### Hard cut with 2-frame white flash + per-shot caption scrim

- **Quando usar:** Switching between two B-roll shots on a sentence boundary ('| e criar...').
- **Como:** tl.set(shot1,{opacity:0},CUT). Flash div (inset 0, #fff): fromTo opacity 0→0.55 in 0.001s at CUT, then to 0 over 0.12s power1.out at CUT+0.001. Scrims: .grad-top 260px rgba(0,0,0,.58→.32→0) under the seam so white captions read; .grad-top2 (300px, .32→.22→0) switched on with a 0.001s tween at CUT for the brighter second plate; .grad-bot from y 700 of the stage, 440px, 0→.22→.48 so chips read.
- **Tempo:** Cut at 2.75 = right after 'existe' and just before 'e' (2.79).
- **Armadilhas:** Second shot is a 9:16 Genjutsu clip: object-fit on the video is not trusted in render, so it is given its native box (width 1080, height 1920, top -704px, object-fit fill) positioned so the eyes (0.523h) sit ~y 300 of the stage, below the seam band. Shot1 uses 1080x1140 + object-position 50% 45% so the face stays fully under the caption band.

### Glass tag spring pop + finite live-dot halo

- **Quando usar:** Small persistent label over footage ('100% IA', 'AO VIVO', 'REAL').
- **Como:** Dark glass pill: rgba(12,12,14,.62), 1.5px border rgba(255,255,255,.14), backdrop-filter blur(14px), height 60, radius 999, Geist Mono 500 28px +0.06em white, 16px lime dot. fromTo {opacity0, scale .55, x16, blur8} → {1,1,0,blur0}, 0.45s expo.out at 0.18, transform-origin 100% 50% (grows from its right edge). Halo: fromTo scale 1→2.6, opacity .8→0, 0.8s power2.out, repeat:3 at 0.5. Hold drift y −6 from 0.63 to EXIT, ease none.
- **Tempo:** 0.18 (right after 'tem empresa' starts) — earliest context label.
- **Armadilhas:** expo.out instead of back.out because the blur is on the same tween (no overshoot = blur never goes negative). repeat must be finite (never -1).

### Attribution chip rise + hard swap on the cut

- **Quando usar:** Crediting whose footage/character is on screen; swapping the credit when the shot changes.
- **Como:** Two chips stacked in one grid cell (grid-area 1/1) at top 1554, height 72: glass pill + 52px round avatar with 2px white ring + Geist 28px (handle 600, meta 500 at 80% white). Chip1 fromTo {opacity0, y30, scale .96, blur12} → rest, 0.45s power3.out at 0.35; drift y −8 to CUT. At CUT: set chip1 opacity 0, chip2 fromTo {opacity0,y24,blur8} → rest in 0.25s power3.out; drift y −6 to EXIT.
- **Tempo:** Chip1 at 0.35; chip2 exactly on CUT (2.75), shorter 0.25s entrance so it feels like part of the cut.
- **Armadilhas:** Avatars are cropped with an absolute-positioned oversized <img> inside an overflow:hidden circle (explicit px offsets), not object-position.

### Kinetic stamp slam + lime echo ring

- **Quando usar:** The single most important claim of the hook ('ELE NÃO EXISTE'); one per video section.
- **Como:** Lime block, Geist 800 72px uppercase limeInk, padding 18/36/16, radius 18, big shadow 0 30px 70px rgba(0,0,0,.4), rotation −4°, centered at (540,1440). fromTo {opacity0, scale1.7, rot −4, blur8} → {1, 1, −4, blur0}, 0.22s expo.out at NEM−0.05. Settle: scale 1→1.03 linear until CUT, then set opacity 0 at CUT. Echo: child div inset −4, 5px lime border, radius 22: opacity 0→.95 in 0.001s at NEM+0.06, then scale 1→1.32 + opacity→0, 0.42s power2.out.
- **Tempo:** Starts 0.05s before 'nem' (2.05) so it is fully landed by 2.17 'existe'. Combined with the B-roll impact punch at NEM−0.06 and camera punch-in (index) at 2.05.
- **Armadilhas:** Positioned at y 1440 (on the character's chest), not the storyboard's 1300, so it never covers the chin even when he dips. expo.out (no overshoot) because blur rides the same tween. Removed with a hard set on the cut rather than an exit.

### Two-channel spring pop (opacity/blur on power2, scale on back.out)

- **Quando usar:** Any pill/card that should bounce in AND come out of blur.
- **Como:** Tween A: fromTo {opacity0, blur6} → {1, blur0}, 0.16s power2.out at POP. Tween B on the same element: fromTo {scale .6} → {scale 1}, 0.42s back.out(1.8), immediateRender:false, at POP. Then hold drift scale 1→1.03 linear to EXIT.
- **Tempo:** POP=3.76 so the pill is sharp by ~3.90, i.e. on the word '5' (3.88).
- **Armadilhas:** Putting filter blur in a back.out tween makes blur overshoot below 0 → stale/invalid blur on seek. Always split: filter/opacity on a non-overshooting ease, scale on the spring.

### Stopwatch ring that drives a count-up readout (svg-path-draw + counter)

- **Quando usar:** 'Takes under X minutes' promises, timers, progress claims.
- **Como:** White pill 132px tall, radius 999, gap 22: SVG stopwatch (dark circle r36, track r26 stroke 7 white 16%, lime ring r26 stroke 7 round cap rotated −90°) + digits Geist 800 88px −0.04em tabular-nums + 'min' Geist 600 40px ink2. One proxy {p:0→1}, 0.5s power3.out at POP+0.02, onUpdate paint(): dashoffset = LEN*(1 − p*STOP/300) with LEN=2π·26; s=round(p*299) → 'm:ss', only writes text when s changes. Hand line rotates 0→359 with svgOrigin '38 47', same duration/ease. Landing sonar: lime 5px ring opacity .9 at POP+RUN−0.08 then scale 1→1.75, opacity→0, 0.4s power2.out.
- **Tempo:** Counts 3.78→4.28; stops on 4:59 just as 'minutos' (4.18) lands; sonar at 4.18.
- **Armadilhas:** Decelerating ease (power3.out) makes the number 'brake' to a stop under 5:00 — reads as 'just under'. Write textContent only on change (seek-safe, no jitter). Initial '0:00' in HTML so frame 0 is correct.

### Scene exit blur-out + B-roll fade to paper

- **Quando usar:** End of every scene that does not hand off a card.
- **Como:** OUT(el,t) = to {opacity0, scale 1.04 (timer 1.08), blur14}, 0.2s power2.in. B-roll wrapper fromTo {1, scale1, blur0} → {0, scale 1.03, blur10}, 0.2s power2.in, immediateRender:false at EXIT+0.01 so the paper panel shows for s2.
- **Tempo:** EXIT 4.42 → everything ends ≤ 4.63, i.e. before 4.67 − 1 frame (4.633).
- **Armadilhas:** Clip window is half-open: an exit that ends on the last frame leaves a stale frame. Keep ≥1 frame (0.033s) margin.

**Lições da cena:** 1) Write a cue grid of word starts as constants at the top of the script and derive every tween from it (NEM−0.05, POP+0.02...) so retiming = editing one number. 2) Lead by ~0.05-0.14s so motion PEAKS on the word. 3) One transform job per wrapper (broll exit / punch impact / shot drift). 4) Never put blur in an overshooting ease; split channels. 5) All repeats finite; fromTo with explicit from-states; immediateRender:false on secondary tweens of the same prop. 6) Everything alive while holding (linear drifts y −6..−8 or scale +3%). 7) Stack 3 signals on the key beat (stamp + plate punch + camera punch-in + caption lime block + pop SFX). 8) Footage placement is solved with explicit px boxes, not object-fit, and checked against the seam band. 9) Exits end ≥1 frame before scene end.

## s2-launchpoint

**Batida:** Mechanism (global 4.67-11.20, dur 6.53). A real screenshot (Launchpoint campaign card) racks into focus, the brand pill pops, then the 3 pills printed in the screenshot are pulled out as crisp HTML twins and the two rules are highlighted on the words ($1 CPM on 'paga', AI Videos ONLY on 'só aceita', lime on 'IA'). Cues: existe 0.97, plataforma 1.38, launchpoint 2.22 | que 2.88, paga 3.03, view 3.43, só 3.99, aceita 4.15, vídeos 4.96, feitos 5.60, por 5.88/5.94, IA 6.12, ends ~6.45. Constants: SNAP 0.83, LAUNCH 2.22, PULL 2.74, PAGA 3.03, SO 3.99, HERO = VIDEOS−0.22 = 4.74, FEITOS 5.60, POR 5.88, IA 6.12, EXIT 6.28, XD 0.18, DUR 6.5.

**Layout:** Transparent full-frame sub-comp (paper + breathing lime glow painted by index.html). Brand pill centre (540,990), z3. Card left 70, top 1060, 940x434 (lp-hero.png 1054x487 at k=.892). Pills row top 1430 (pill centres y 1500), z2; labels at row-local top 160 (≈y 1590): label1 right-aligned under CPM (right 146) with a tail, label2 centred. Bloom row-local (240,−94) 600x300. Everything key inside safe box x70-1010, y950-1680. Captions on paper mode = ink 66px Geist 600 at y 812.

**SFX:** Scene global start 4.67 (local = global − 4.67):
- 5.50 whoosh.mp3 vol 0.20 (track 11) → local 0.83 SNAP, card snaps into focus.
- 6.77 pop.mp3 vol 0.29 → local 2.10, brand pill pop + sheen (LAUNCH−0.12).
- 7.41 whoosh-short.mp3 vol 0.18 (track 11) → local 2.74 PULL, focus pull + pills fly out.
- 7.63 ping.mp3 vol 0.29 → local 2.96, lime ring locks on $1 CPM ('paga').
- 8.57 click.mp3 vol 0.35 (track 11) → local 3.90, ring jumps to AI Videos ONLY ('só aceita').
- 9.43 whoosh-short.mp3 vol 0.14 → local 4.76, hero promotion ('vídeos').
- 10.77 pop.mp3 vol 0.29 → local 6.10, lime wipe + punch peak on 'IA'.
(11.20 whoosh vol 0.18 = s3's entrance, not s2.) Camera punch-in (index) at global 6.89 = local 2.22 'launchpoint'.

### Rack-focus card arrival (continuous from frame 0, snaps sharp on the word)

- **Quando usar:** Introducing a screenshot/app card on the paper panel when the scene starts mid-sentence: no dead plateau, the card is already moving at frame 0.
- **Como:** 3 nested layers, one channel each: .card (transform + exit, transformPerspective 1400), .lens (opacity), .dof (filter). Phase 1 (0→SNAP, ease none): card y140→20, scale .9→.975, rotationX 16→4; lens opacity 0→.85 in 0.3s power2.out; dof blur 8→5. Phase 2 at SNAP: card → y0, scale1, rotX0, 0.4s power3.out; lens →1; dof → blur0, 0.4s power3.out. Hold: card scale 1→1.03 linear until PULL. Filter uses one grammar F(b,br,sa,co) = 'blur() brightness() saturate() contrast()' everywhere so GSAP interpolates cleanly.
- **Tempo:** SNAP 0.83 → sharp at ~1.23, right on/after 'existe' (0.97) + 'plataforma' (1.38). SFX whoosh at the snap.
- **Armadilhas:** Different filter function lists between from/to break interpolation → always the same 4-function string. Dark card: radius 30, bg #141416, 2px rgba(255,255,255,.07) edge, shadow 0 40px 90px rgba(10,10,0,.30). A 20px top fade hides a glow the print cut off at its top edge.

### One-shot lime sheen sweep across the card

- **Quando usar:** Naming the brand/product the card belongs to.
- **Como:** Child .sheen 230x560 at top −60, linear-gradient lime 0→.30→(240,255,190,.42)→.30→0, mix-blend-mode screen. fromTo x −330→1060, skewX −16, 0.7s power1.inOut.
- **Tempo:** LAUNCH−0.14 (2.08), together with the brand pill.
- **Armadilhas:** One pass only (finite); sits inside the card's overflow:hidden surface.

### Brand pill two-channel pop + drift

- **Quando usar:** Brand/name callout above a card ('Launchpoint').
- **Como:** White pill h80, radius 999, 56px logo tile radius 14 + Geist 700 44px −0.03em, at center (540,990), z 3. Tween A: opacity/blur 8→0, 0.22s power2.out. Tween B: scale .5→1, y14→0, 0.45s back.out(1.6), immediateRender:false. Drift y −8 linear from LAUNCH+0.33 to EXIT.
- **Tempo:** Both at LAUNCH−0.12 (2.10) → peak on 'launchpoint' 2.22.
- **Armadilhas:** Same split rule as s1: blur never inside back.out.

### Focus pull (depth-of-field) — card recedes to a ghost

- **Quando usar:** When detail pulled from a card becomes the new focus; keeps context visible but secondary.
- **Como:** At PULL, 0.5s power2.inOut: card y −70, scale .86; lens opacity .24; dof F(6, 1.5, .5, .75) (blur 6, brighter, desaturated, lower contrast = 'light ghost' on paper). Then continue card y −96, scale .84 linear to EXIT. Brand pill stays sharp above it.
- **Tempo:** PULL 2.74 = on 'que paga por view' (que 2.88), lead ~0.14.
- **Armadilhas:** brightness 1.5 + saturate .5 makes a dark card read as a pale ghost on light paper instead of a dark blur blob.

### Pill pull-out from screenshot (print → HTML twin)

- **Quando usar:** Extracting items (pills, rows, numbers) from a real screenshot so they become crisp, animatable UI.
- **Como:** Pre-compute (never measure at tween time) each pill's in-image box (image px) → stage coords: cx = CARD.x + mid_x*k, cy = CARD.y + mid_y*k (k=.892), then apply the card's drift about card centre: s = CC + (c − CC)*DRIFT (1.03). Start transform = {x: sx − finalCx, y: sy − finalCy, scale: (y1−y0)*k*DRIFT / PILL_H}. At PULL−0.05: a 0.001s tween sets twins visible at that exact spot, and simultaneously a dark .patch (#050302, radius 20, 10px glow) covers the printed pills in the card. Then each twin → x0,y0,scale1, 0.5s power3.out with offsets {CPM: +0, AI Videos: +0.04, $2,000: +0.10} (outer pills first, centre last → no crossing). Final row: top 1430, pills h70, left/width 106.5/276, 402.5/335, 757.5/168 (row centred at x 516 so the CPM ring stays ≤ x 962). Pill face: blue #3D4EF2, 2px rgba(255,255,255,.18) border, top gloss gradient, Geist 500 29px white, bold value 700/800, shadow 0 16px 34px rgba(36,48,190,.30).
- **Tempo:** Twins appear PULL−0.05 (2.69); lifts 2.74-3.34. Row drift y −8 from 3.4 to EXIT.
- **Armadilhas:** Printed pills and twins must NEVER be visible together → instantaneous swap (patch + twin set on the same frame). Order the lifts so paths don't cross. Fixed geometry from the asset table (pill boxes in image px) — no getBoundingClientRect in the timeline.

### Lime ring hug + label, ring jump between targets

- **Quando usar:** Pointing at the item being spoken ('paga' → $1 CPM; 'só aceita' → AI Videos ONLY).
- **Como:** Ring = child of the pill, inset −14, 6px lime border, radius 999, halo box-shadow 0 0 0 10px rgba(212,255,58,.28) + 0 10px 30px rgba(120,160,0,.25). In: fromTo opacity0, scale1.3 → 1,1, 0.36s back.out(2). Label card (white, h76, radius 22, Geist 600 40px, mono '=' in #4F6B00, 20px rotated-square tail pointing at the pill) blur-rise y20→0, blur10→0, 0.4s power3.out. Jump: old ring → opacity0, scale1.12, 0.18s power2.in and old label → opacity0, y −10, blur10, 0.2s power2.in at SO−0.13; new ring pops at SO−0.09; new label at SO−0.02. Non-focal pills: step aside x ±22 + opacity .55/.35, 0.35s power2.out. Ring 'breathes' while holding: scale 1→1.025, 0.7s sine.inOut, yoyo, repeat 1.
- **Tempo:** ring1 PAGA−0.07 (2.96), label1 PAGA+0.05; ring2 SO−0.09 (3.90), label2 SO−0.02.
- **Armadilhas:** x for 'step aside' lives on the inner .punch wrappers so it never fights the still-running lift tweens on the outer .pill (nesting: .pill [lift/hero] > .punch [step-aside x, IA punch] > .boost [keyword driver] > .face).

### ASR keyword glow driver (envelope-driven push)

- **Quando usar:** Keeping the spoken item 'pushed' (lift + scale + glyph glow) for exactly as long as it is talked about, with smooth attack/release.
- **Como:** One linear proxy drv.t 0→DUR (6.5s, ease none, onUpdate paint) spanning the whole scene. env(t,s,e): 0 before s; cubic ease-out attack over 0.2s; hold 1 until e; linear release over 0.35s down to REST 0.2. paint() writes boost.style.transform = translateY(−8*e) scale(1+0.16*e) and face textShadow 0 0 18*e px rgba(255,255,255,0.6*e*(1−flash)). Windows: CPM PAGA−0.08 → SO−0.15; AI Videos SO−0.08 → 6.45. flash = progress of the lime wipe, kills the white glow once the pill turns lime.
- **Tempo:** Covers 2.95-3.84 (CPM) and 3.91-6.45 (AI Videos).
- **Armadilhas:** Pure function of t → fully seek-safe. Written to its own .boost wrapper so GSAP tweens on other wrappers never collide with the manual style writes. Hero scale is divided by (1+BOOST) so total = 1.5x.

### Hero promotion + flank rack focus

- **Quando usar:** Final emphasis: one item becomes the hero, others recede.
- **Como:** At HERO (VIDEOS−0.22 = 4.74), 0.45s power3.inOut: hero pill → x = 540 − slotCentre, y −4, scale 1.5/(1.16); other two → x to 150 / 900 minus their centre, y8, scale .72, opacity .25, blur 4.
- **Tempo:** Mid-move lands on 'vídeos' (4.96).
- **Armadilhas:** Uses pre-computed slot centres P1C/P2C/P3C, not measured positions.

### Lime block word highlight + clip-path lime wipe with punch

- **Quando usar:** Marking the key words ('100% IA') and turning the hero into the brand accent on the final word.
- **Como:** Word block: .hl-bg lime, radius 12, top −9, height +18, scaleX 0→1 from origin 0 50%, 0.32s expo.out at FEITOS−0.1. Lime face (duplicate .face.lime layered over the blue one) clip-path inset(0 100% 0 0 round 999px) → inset(0 0 0 0 round 999px), 0.22s power3.inOut at LIME_AT = POR−0.04 (5.84); blue face shadow tweened to olive rgba(110,150,0,.32) same time; ring2 out (0.18s). Punch on .punch: scale 1→1.08, 0.12s power2.out at IA−0.14, back to 1 0.26s power3.out at IA−0.02. Bloom (radial lime 600x300 behind the row) opacity 0→.5, scale .8→1, 0.3s power2.out at LIME_AT+0.02.
- **Tempo:** Wipe peaks just before 'IA' (6.12); punch peak at 6.10.
- **Armadilhas:** Colour change via a clipped duplicate layer (wipe) rather than tweening background-color — reads as a deliberate reveal. Pre-set the clip-path closed in CSS so frame 0 is right.

### Exit

- **Quando usar:** Scene end with no card handoff.
- **Como:** OUT(card) at EXIT−0.02 with scale .95 (card recedes further), brand OUT (scale 1.04, blur14, 0.18s power2.in), row fromTo explicit rest → {0, 1.04, blur14}, 0.18s power2.in, immediateRender:false at EXIT.
- **Tempo:** EXIT 6.28 → ends 6.46 < 6.53 − 1 frame.
- **Armadilhas:** Row uses fromTo with explicit from-state because its opacity/filter were never set before (seek-safe).

**Lições da cena:** 1) Real screenshots become motion by re-building the important bits as HTML twins and swapping on one frame (patch + twin). 2) Separate wrapper per channel: card/lens/dof; pill/punch/boost/face. Each GSAP tween or manual write owns exactly one wrapper. 3) Pre-computed geometry from the asset's pixel boxes; no DOM measuring. 4) Only one thing 'owns' the frame at a time: focus pull, step-aside+dim, hero promotion. 5) Highlights hop with the voice (ring jump: out 0.18 power2.in, new in back.out(2) 0.04s later). 6) SFX vocabulary: whoosh = movement/focus change, pop = something appears, ping = highlight lands, click = selection change; 0.14-0.36 vol, alternate tracks 10/11/12 when sounds overlap. 7) Captions (captions.html, reusable): 2-4 word chunks at top 812, Geist 600 66px −0.028em (74px white on full-cam at y1540; white + text-shadow over B-roll); chunk in blur8→0, y16→0, 0.14s power2.out at start−0.03, out 0.05s at next−0.08; unspoken words at opacity .42 lit to 1 at word−0.03; keywords get a lime block scaleX 0→1 0.2s power3.out at word−0.05, text→limeInk, scale 1.06 yoyo 0.12s. Highlight the same keywords the scene animates (nem/existe, 5/minutos, launchpoint, IA).

## s3-calc

**Batida:** stakes / money math. Global 11.20-16.13 (dur 4.93). Cues (scene-local word starts): dólar@0.26, cada@0.70, mil@1.04, views@1.29, ou seja@1.73, um@2.35, milhão@3.31, mil@4.23, dólares@4.43. Story: 'US$ 1 / a cada 1.000 views' -> the line morphs into the multiplier '× US$ 1 a cada 1.000' while a hero counter 0->1.000.000 views rises above -> lime result block 'US$ 1.000' slams on 'mil dólares' + honest disclaimer.

**Layout:** Full-frame transparent 1080x1920 sub-comp; paper bg + ambient glow come from index.html. All rows are full-width flex rows centered on x=540, white-space nowrap. Beat1: 'US$ 1' row top 1042 (176px Geist 800, -0.045em); subline row top 1244 (56px/600, ink2; 'views' in mute). Beat2: hero counter row top 1052 (156px/800 tabular, fixed width) + 'views' 44px/500 mute, margin-left 18; multiplier row top 1252 (54px/600 ink2, gap 16). Beat3: lime glow ellipse left -10 top 1140 1100x640; result row top 1358 height 196; disclaimer row top 1584 (Geist Mono 25px). Everything inside safe box x70-1010, y950-1680; caption band 800-920 untouched.

**SFX:** Scene global start 11.20. sfx-12 whoosh.mp3 vol 0.18 @11.20 (local 0.00) = 'US$ 1' blur-rise + scene cut. sfx-13 whoosh-short.mp3 vol 0.15 @13.30 (local 2.10) = morph M0 (line reflow). sfx-14 impact-bass-2.mp3 vol 0.08 + sfx-15 pop.mp3 vol 0.33 @15.30 (local 4.10) = lime result slam (layered: low bass very quiet + pop). Camera (index.html) punch-in scale 1->1.05 0.32s power2.out at 15.35 for 'mil dólares', reset at the next cut 16.13. No SFX on the count-up itself (no tick spam); the s4 whoosh at 16.21 covers the transition.

### Word-by-word build with live re-centering

- **Quando usar:** Any short phrase that is spoken word by word and must stay optically centered at every instant (no lopsided half-built line).
- **Como:** Hero 'US$ 1' IN (blur-rise) with y:56, scale .9, blur 18, d .4, power3.out. Subline words are separate inline-blocks: 'a cada' IN y30/s.96/b10/d.42 power3.out; '1.000' same but ease back.out(1.6); 'views' y24/d.40. The whole row is translated by x so only VISIBLE words are centered: SH1 = wFull/2 - wW1/2 (only 'a cada' visible), SH2 = wFull/2 - wAc/2; tween row x SH1->SH2 (0.26s power3.out) when word 2 lands, then SH2->0 (0.38s power3.out, immediateRender:false) when word 3 lands. Widths measured with a hidden probe span (see pitfalls).
- **Tempo:** Hero at 0.00 (sharp by 0.28, 'dólar'@0.26). 'a cada' at 0.50 (word @0.58/0.70). '1.000' at 0.94 (word 'mil'@1.04, ~0.10 lead). 'views' at 1.20 (word @1.29). Re-center tweens start on the same frame as the word's IN.
- **Armadilhas:** Second fromTo on the same property (row x) must use immediateRender:false or it overwrites the first tween's from-state on seek. Measure widths only after document.fonts.load(...) resolves; build the whole timeline inside that promise.

### Card-morph anchor: phrase reflows into the next line (FLIP by measured deltas)

- **Quando usar:** When the next beat reuses the previous statement as a component (A becomes a term of an equation). Viewer keeps track of the object instead of a cut.
- **Como:** Compute centers of source glyphs (A1 'US$ 1' 176px, AC 'a cada 1.000' 56px) and destination glyphs on the target line (MU, MC at 54px); deltas d1, d2 and scale ratios S1=54/176, S2=54/56. At M0=2.10: 'views' exits right (opacity 0, x +40, blur 10, 0.2s power1.in). 'a cada 1.000' moves x/y/scale to its slot (0.28s power3.inOut). 'US$ 1': x over 0.32s power3.inOut; scale + color ink->#3A3A40 over 0.36s power2.inOut; y over 0.32s power3.inOut but delayed +0.10s so it descends only after the slot has opened (a straight path would cut through 'a cada'). Then swap to the real target glyphs: moving copy opacity->0 in 0.08-0.10s ease none while the static target element fades 0->1 in the same window (ac/mc at M0+0.28, a1/mu at M0+0.41). The '×' sign pops in at M0+0.30 from scale .3 with back.out(2) 0.36s.
- **Tempo:** Starts 2.10 (between 'ou seja'@1.73-1.87 and 'um'@2.35), lands 2.38/2.52, i.e. the line is ready just before the next phrase begins. Single start for both groups, one ease family (power3.inOut / power2.inOut) so they land together.
- **Armadilhas:** Swap to the real glyphs only once the moving copy is fully seated, otherwise a ghosted double shows. Split x and y into separate tweens to shape the path (y trails by 0.10s). Use transforms only, never top/left/font-size.

### Counting with dynamic scale (count-up hero)

- **Quando usar:** Big number that grows on the spoken value ('um milhão').
- **Como:** Proxy object {v:0} -> 1000000, 0.93s power2.out, immediateRender:false, onUpdate writes fmt(v) (pt-BR thousands dots). Same start/duration/ease tween on the number's scale .86 -> 1 (transform-origin 100% 60% so it grows from its right edge next to 'views'). Number box has a FIXED width = probeW('1.000.000') + 4 px, text-align right, font-variant-numeric: tabular-nums -> zero layout shift. The hero row enters 2.48: opacity 0, y -30, blur 14 -> clear, 0.4s power3.out (drops in from above). Small 'views' unit pops at 3.24: opacity 0, x -16 -> 0, 0.36s back.out(1.6).
- **Tempo:** Count 2.45-3.38; ends right around 'milhão'@3.31 (value lands on the word). Unit label 3.24.
- **Armadilhas:** Put the initial value ('0') in the HTML so frame 0 is right. Value and scale must share start/duration/ease or the number 'breathes' out of sync.

### Lime result slam (kinetic beat slam) + glow bloom + impact nudge

- **Quando usar:** The payoff number of a scene (the result, the price, the punchline).
- **Como:** Lime block (radius 28, padding 0 46px, height 196, limeInk text 156px/800/-0.05em) fixed width = probeW('US$ 1.000') + 92, text LEFT-anchored so 'US$' never moves while digits grow and the final value is exactly centered. Slam: opacity 0, scale 1.35, blur 8 -> 1/1/0, 0.32s expo.out. Inner count 0->1000 in 0.28s power2.out (text set to 'US$ 0' before build). Glow (radial lime ellipse 1100x640 behind) opacity 0->.42, scale .72->1, 0.5s power2.out, starting 0.04s BEFORE the slam. The equation above reacts once: y 0->-10 in 0.09s power2.out at +0.03, back to 0 in 0.34s power2.out at +0.12.
- **Tempo:** S3=4.10, word 'mil'@4.23 (~0.13s lead so it peaks on the word). Disclaimer pill (Geist Mono 25px, white 72% pill, 1.5px line ring) IN at 4.16 with tiny params y12/s.98/b6/d.24, so it lands WITH the slam (storyboard had 4.45; moved earlier so it is readable before exit).
- **Armadilhas:** Filter blur is used only with non-overshooting eases (expo.out/power); never put filter inside a back.out tween (overshoot leaves stale blur on seek). One percussive nudge only; repeated shakes read as jitter.

### Ambient drift on a wrapper

- **Quando usar:** Every scene, so held frames are never dead.
- **Como:** Wrap all content in a full-frame layer with transform-origin 540px 1340px (stage visual center); scale 1 -> 1.025, 4.6s ease none, starting 0.06.
- **Tempo:** Whole scene.
- **Armadilhas:** Drift on a wrapper, not on elements that already have their own scale tweens (avoids conflicting tweens on one property).

### Staggered blur-out exit, payoff holds longest

- **Quando usar:** End of every scene.
- **Como:** OUT = to opacity 0, scale 1.04, blur 14, power2.in. Equation 4.66 (d .20), disclaimer 4.68 (d .18, s 1.02), result 4.70 (d .18), glow-wrap opacity 0 at 4.70 (0.18s).
- **Tempo:** Ends 4.88 < 4.93 - 1 frame (0.033).
- **Armadilhas:** Clip window is half-open: exits must END at least 1 frame before data-duration or the last frame pops.

**Lições da cena:** 1) Measure, don't guess: hidden probe span appended to <body> (scene may be display:none while building), same font/weight/size/letter-spacing in px + tabular-nums; build after document.fonts.load for every face/size used. 2) Fixed-width numeric boxes + tabular-nums + left/right anchoring kill layout shift in counters. 3) Morphs: split x/y/scale/color into separate tweens with small offsets to shape the path; swap to real glyphs only after seating. 4) Lead beats by ~0.10-0.13s so motion peaks on the word; storyboard cues were nudged during build (morph 2.25->2.10, count 2.35->2.45, slam 4.15->4.10, disclaimer 4.45->4.16). 5) Vary eases per beat: power3.out entrances, power3.inOut morphs, power2.out counts, expo.out slam, back.out only for small pops without filter. 6) All later fromTo on already-tweened props: immediateRender:false.

## s4-quem-banca

**Batida:** aha setup / who pays. Global 16.13-21.03 (dur 4.90). Cues: obviamente@0.14, verificar@0.74, quem@1.51, banca@1.87, isso@2.11, empresa@2.66, paga@3.42, isso@3.78, higgsfield@4.30. Story: platform pill + search bar types 'quem paga esses criadores?' -> enter -> kinetic headline 'quem banca isso?' (lime block on banca) -> shrinks to a title, ranking screenshot rises -> on 'paga' focus pull, crisp Higgsfield row lifts out of its slot -> '#1' tag, then lime ring + punch on 'higgsfield'.

**Layout:** Platform pill row top 1122 height 76 (centered). Search bar left 70 top 1236 940x136 (center y 1304). Headline box left 40 top 1244 width 1000 height 112 (line-height 112), later moved to y~944-1000 at scale .5-.54. Grid card 70,1090 940x505 (ends 1595). Hero row lands centered at (540,1330), 860x157, scale 1.08-1.12 (~930-963 wide incl. ring). Tag sits 40px above the row's top-right. All key content in safe box x70-1010 / y950-1680.

**SFX:** Scene global start 16.13. sfx-16 whoosh.mp3 vol 0.16 @16.21 (local 0.08) = search bar IN. sfx-17 typing.mp3 vol 0.34 dur 1.0 @16.43 (local 0.30) = first keystroke, covers typing to ~1.30. sfx-18 pop.mp3 vol 0.33 @18.00 (local 1.87) = lime block wipe on 'banca'. sfx-19 whoosh.mp3 vol 0.18 @18.63 (local 2.50) = headline shrink + grid blur-rise (2.40/2.56). sfx-20 whoosh-short.mp3 vol 0.16 @19.48 (local 3.35) = row lift / focus pull. sfx-21 pop.mp3 vol 0.26 @19.86 (local 3.73) = '#1' tag pop (3.74). sfx-22 ping.mp3 vol 0.32 @20.33 (local 4.20) = lime ring + punch on 'higgsfield'. Camera punch-in at 20.35 (scale 1.05) reset 21.03; sfx-23 whoosh vol 0.14 @21.03 = camera goes full-screen after the scene. No click on the enter press (typing bed covers it).

### Search bar with discrete typewriter + caret + enter press

- **Quando usar:** 'I went to check / I searched' moments; any UI typing.
- **Como:** Search pill 940x136 radius 999, white, big light-card shadow, magnifier SVG left, lime round 'go' button 92px right. Platform pill (logo + 'Launchpoint' 36px/700 + mono tab 'EXPLORAR') sits above at top 1122, enters 0.12 from y26/scale .7/blur 8, 0.45s power3.out (origin 50% 100%). Search IN at 0.08 (y60, d.5). Typing is a hand-timed key schedule (26 keystroke times 0.30..1.20, irregular gaps 0.02-0.07 with small pauses between words) driven by a proxy {t} tween 0->1.5 ease none; onUpdate looks up text for the time and writes textContent only when it changed. Caret = inline 4x54px ink bar right after the typed span (moves with text, no blinking). Hold life: search scale 1->1.02 and pill y 0->-8 over 0.7s ease none from 0.6. Enter press: go scale ->.84 in 0.07 power2.in at 1.18, back to 1 in 0.24 back.out(3) at 1.25. Then pill and bar lift away: y -100/-90, scale .92/.96, blur 14/16, opacity 0, 0.22s power2.in at 1.27/1.30.
- **Tempo:** Typing 0.30-1.20 spans 'eu fui verificar'(0.56-0.74); press at 1.18; UI gone by 1.52, just as 'quem'@1.51 is spoken.
- **Armadilhas:** Seek-safe typing: never append chars incrementally; compute the full string from time and write only on change. Initial typed span empty in HTML. Irregular key timings read as human; even spacing reads robotic.

### Kinetic headline with lime word-block and re-centering

- **Quando usar:** The question/hook line of a scene, 2-4 words, one highlighted keyword.
- **Como:** Single line 104px Geist 700 -0.035em, words are inline-blocks. Row pre-set x so only visible words are centered (measured offsets X_QUEM=307.5, X_BANCA=134.1, X_ALL=0; gsap.set at build). 'quem' 1.43: y40/blur14 -> 0, 0.3s power3.out. 'banca' 1.78: y40/scale 1.18/blur14 -> 1, 0.3s expo.out (lands bigger-to-normal for emphasis) + row x -> X_BANCA 0.3s power3.out. Lime block behind 'banca' (absolute span, inset -16px sides, top 10 bottom 4, radius 18, z 0, origin 0 50%) scaleX 0->1 0.28s power3.out at 1.87; the word is in limeInk from the start via class. 'isso?' 2.04: y40/rotation 4/blur14 -> 0, 0.32s power3.out + row x -> 0. Small breath scale 1->1.03 (0.32s none) at 2.08. Then the headline becomes a title: scale .54, y -300 (to y~1000), 0.4s power3.inOut at 2.40; breathes .545 (0.55s none); steps back on focus pull to scale .5 opacity .55 (0.45s power2.inOut) at 3.35; keeps breathing .505.
- **Tempo:** Each word IN starts ~0.07-0.09s before its spoken word (quem 1.43 vs 1.51, banca 1.78 vs 1.87, isso 2.04 vs 2.11); block wipe exactly on 'banca'@1.87.
- **Armadilhas:** Never use <br>; one-line nowrap with measured offsets. The headline is reused as the scene title rather than exiting, so the viewer keeps the question in view during the answer.

### Screenshot card entrance under a shrinking title

- **Quando usar:** Bringing in proof (a real print) right after the question.
- **Como:** Dark UI card 940x505 at (70,1090), radius 30, overflow hidden, strong shadow; img scaled 1054->940 (x0.89184). IN at 2.56 with a longer travel (y130, d .55). A 'world' wrapper (origin 540 1342) drifts scale 1->1.02 over 2.04s ease none. Screenshot rim cleanup: a 40px overlay of linear-gradients paints out the warm edge/glow bleed of the PNG; ::after inset 2px white-7% hairline.
- **Tempo:** 2.56, between 'isso tudo' and 'a empresa'@2.58, overlapping the headline shrink (2.40-2.80).
- **Armadilhas:** Fix screenshot artifacts with overlays inside the card instead of editing the asset; keep the img at exact computed size (504.8px tall) so later pixel-mapped geometry matches.

### Pull-out of a crisp element from a screenshot (row lift) with focus pull

- **Quando usar:** Highlighting one item inside a real screenshot (a row, pill, badge) so it becomes legible and hero.
- **Como:** Rebuild the item as crisp HTML (860x157 dark raised row #1E1E22, radius 22: logo 88px, name 40px/600 white, sub 26px #9A9AA2, price 30px tabular, 'per video' 24px). Map its slot from image px to screen px (img x6..516,y6..99 x0.89184 + card offset -> center (302.77,1136.82), width 454.84). Start state: x=302.77-540, y=1136.82-1330, scale S0=454.84/860 so it sits pixel-on-top of the print; each text child also starts with per-element x/y/scale corrections (e.g. name scale .653, sub .823, amt .85, per .89) so its proportions match the print, then all go to 0/1 in 0.45s power3.out while the row goes to center (540,1330) scale 1.08 in 0.45s power3.out. Background color tweens rgb(20,20,23)->rgb(30,30,34) (looks like the print, then 'raises'). Separate shadow layer opacity 0->1 0.4s from +0.03. Hard cut: row opacity and an empty 'hole' slot (inset shadow) inside the grid both switch 0->1 with duration 0.001 at 3.345 (no crossfade). Focus pull on the grid: blur 5px, opacity .4, scale .97, 0.5s power2.inOut. Hold: row scale 1.08->1.095 0.4s none.
- **Tempo:** 3.35, word 'paga'@3.42 (~0.07 lead).
- **Armadilhas:** Cross-fading print and crisp copy produces a double image; cut on the frame the lift starts. Leave a 'hole' behind so the grid reads as physically missing the row. Animate the shadow on its own layer (opacity) rather than tweening box-shadow.

### Rank tag + lime ring hug + scale punch

- **Quando usar:** Final emphasis on the hero item when its name is spoken.
- **Como:** Tag pill (lime, limeInk Geist Mono 26px, 2.5px dark outline ring, origin 100% 100%) at row's top-right (right 26, top -40): opacity 0, scale .5, rotation -8 -> 1, 1, rotation 3, 0.38s back.out(2). Ring = absolute box inset -12px, radius 34 (row radius 22 + 12), border 6px lime, outer halo box-shadow 0 0 0 10px rgba(212,255,58,.28): POP from scale .9, opacity 0, 0.36s back.out(2). Row punch: scale ->1.12 in 0.12s power2.out at 4.22, settle 1.10 in 0.2s power2.inOut at 4.34.
- **Tempo:** Tag at 3.74 on 'isso'@3.78 (storyboard had it on 'higgsfield'; split into two beats for rhythm). Ring 4.20 + punch 4.22 on 'higgsfield'@4.30.
- **Armadilhas:** back.out is fine here because there is no filter in these tweens. Ring radius = target radius + gap so it hugs evenly.

### Exit

- **Quando usar:** End of scene.
- **Como:** OUT(headline, 4.59, scale .52, y -312) keeps its title position while blurring out; OUT(world, 4.59) default (opacity 0, scale 1.04, blur 14, 0.26s power2.in).
- **Tempo:** Ends 4.85 < 4.90 - 1 frame.
- **Armadilhas:** When an element was scaled/moved earlier, pass its current scale/y in the exit so it does not jump back to 1/0 while fading.

**Lições da cena:** 1) SFX vocabulary: whoosh (0.14-0.20) for big moves/entrances, whoosh-short (0.12-0.16) for secondary moves/morphs, pop (0.20-0.36) for highlights/blocks/tags, ping (0.22-0.32) for the hero reveal, click (0.31-0.42) for UI presses, typing (0.34) for text entry, impact-bass (0.08-0.10, layered under a pop) only for the payoff slam, sparkle (0.16-0.20) for magic/result moments. Spread across tracks 10-14 so overlaps never cut each other. 2) SFX start = visual tween start (not the word), since visuals already lead the word by ~0.1s. 3) Reuse the question as a persistent title instead of exiting it. 4) Pixel-map screenshot regions (image px * scale + card offset) to make crisp HTML replicas that start exactly on the print; hard-cut swap (0.001s) + hole. 5) Depth-of-field focus pull (blur 5-6, opacity .35-.4, scale .97) on everything non-focal. 6) Every hold has a tiny ease:none drift (scale +0.5-3%). 7) Camera punch-ins in index.html on keywords (scale 1.05, 0.32s power2.out, starting 0.08s before the word) double the emphasis of stage beats. 8) Captions live in their own band (800-920, z 30) from captions.html; scenes never put text there.

## s5-ciclo

**Batida:** AHA / comparison → payoff. Global 22.03–29.40 (7.37s). 'ao invés de pagar influencer pra falar dela | ela paga | por um serviço que é feito dentro dela | isso faz muito mais sentido'. Shape: loser card alone & centred → split with winner → strike loser → winner hug → cards part → icon tile + looping arrow + kinetic 2-group sentence with lime block. Spoken cues are scene-local word starts; every move starts ~0.08–0.12s BEFORE the word so it peaks ON it.

**Layout:** Canvas 1080x1920 @30fps. CAM 0–780 (camera layer sits above scenes — anything painted there is hidden); caption seam band 800–920 (keep text out); STAGE 940–1860, visual centre ≈ (540,1340); safe text box x 70–1010, y 950–1680 (Reels UI eats bottom ~240px and right icon column). s5: two 430x600 cards, tops 1030, lefts 85/565 (centres 300/780, y 1330), 50px gutter; media area top 320px of card, body 280px; X disc at card-local (356,18). Payoff: tile 150px at (465,1075), arc wrapper 320px at (380,990) concentric with tile, sentence top 1330 width 900. Scene is a transparent full-frame sub-composition; paper bg + lime glow belong to index.html.

**SFX:** Scene global start 22.03 (local = global − 22.03). whoosh.mp3 vol .16 @22.13 (L 0.10 card entrance) · pop.mp3 .20 @22.53 (0.50 coin drop) · whoosh-short .16 @24.65 (2.62 right card flies in) · click .35 @25.03 (3.00 strike line draw) · pop .23 @25.15 (3.12 red X disc, track 12 to overlap the click) · pop .22 @25.93 (3.90 Higgsfield badge) · sparkle .16 @26.83 (4.80 winner ring/pulse) · whoosh .14 @27.63 (5.60 cards part) · pop .26 @28.11 (6.08 'própria propaganda' punch). Overlapping SFX go on different data-track-index (10/11/12). Levels: whoosh .12–.22, pop .20–.36, click .31–.42, ping .22–.32, sparkle .16–.20, impact-bass .08–.10, typing .34, key-press .48. SFX live only in index.html, never in scenes.

### Solo-then-split comparison (staged centre → slot)

- **Quando usar:** Any A-vs-B argument where A is introduced first by voice. Avoids an empty half-frame while only A is being talked about.
- **Como:** Cards 430x600, slots left 85 / 565, top 1030 (centres x 300/780, y 1330). Three nested wrappers per card: .pos (x/y/rotationY/opacity/filter) > .scl (scale only) > .flt (float y only) — so moves, scaling and idle float never fight over one transform. A enters at x:+240 (i.e. centred) from {x:160,y:60,scale:.94,rotationY:10,transformPerspective:1200,blur 16} → {x:240,y:0,rotationY:0,blur 0} 0.55s power3.out @0.10; its .scl staged at 1.12→1.145 linear over the solo hold (1.83s). On the split word: A .pos x→0 rotationY 4 (0.5s power3.out) + .scl →1 (0.4s) @2.48; B enters mirrored {x:80,rotationY:-10,blur16}→{x:0,rotationY:-4} 0.53s @2.62. Mirrored ±4° rest tilt (book-open) with shared perspective 1200.
- **Tempo:** A @0.10 (cue 'ao' 0.05); split @2.48–2.62 for 'ela' 2.77.
- **Armadilhas:** Never animate left/width — use x on .pos. Keep perspective identical on both cards or the tilts look mismatched.

### Card body that re-lays itself (group glides up when sub arrives)

- **Quando usar:** Card text that grows in steps (title first, sub later) without empty space before the sub appears.
- **Como:** Body group (label+title[+chip]) is absolutely positioned at its FINAL top; starts offset y:+41 (L) / +69 (R) so it looks vertically centred; when the sub line arrives: group y→0 0.45s power3.inOut, sub IN {opacity0,y20,blur10}→ 0.36s power3.out starting 0.08s later. Sub separated by 2px hairline border-top.
- **Tempo:** Group glide 0.07–0.1s before the word ('pra' 1.73 → glide 1.66, sub 1.74; 'feito' 4.83 → 4.74 / 4.80).
- **Armadilhas:** Offsets are hand-computed constants (LGRP_Y/RGRP_Y) from layout heights — recompute if font sizes change.

### Strike-out the loser (path draw + X disc + desaturate)

- **Quando usar:** 'não', 'em vez de', rejecting option A.
- **Como:** SVG line across card (x1 36,y1 566 → x2 394,y2 34), stroke #FF4A3D 10px round cap, dasharray=dashoffset=641.24 (exact length) → 0, 0.28s power2.out. Same time: card filter grayscale(1)+opacity .55 0.4s power2.out, .scl 0.94 0.45s power2.inOut. Red X disc 56px at top-right POP {opacity0,scale .3,rotation -45}→ back.out(2) 0.4s, +0.12s after the line starts.
- **Tempo:** Line @3.00 for 'paga' 3.09; X @3.12.
- **Armadilhas:** FIXED: a round linecap at full dashoffset still paints a dot at the path start — keep the SVG at opacity 0 and flip it to 1 (0.02s) exactly when the draw starts. Same fix used on the loop arrow.

### Brand badge pop + one-shot pulse ring

- **Quando usar:** Naming the product/service ('serviço', 'higgsfield') on top of an image.
- **Como:** 70px rounded (18px) logo badge on the photo corner, box-shadow 0 0 0 3px #fff ring; POP {opacity0,scale .4,rotation -12}→ back.out(2.2) 0.42s. Pulse = 4px lime border box, two-step: fromTo opacity 0→0.9 at scale .9 in 0.01s, then to {opacity0, scale1.6} 0.6s power2.out.
- **Tempo:** Badge @3.90 for 'serviço' 4.01; pulse 3.98–4.59.
- **Armadilhas:** FIXED: the two-step (instant set + expand) keeps the pulse invisible before its beat under any seek order; a single fromTo from opacity .9 would render early on backward seeks.

### Lime ring hug for the winner

- **Quando usar:** Declaring the winner / highlighting one card among several.
- **Como:** Ring box inset -10px, radius card+10 (44px), border 6px lime, box-shadow 0 0 0 10px rgba(212,255,58,.28), 0 10px 30px rgba(120,160,0,.25). On the beat: inner 4px lime inset border fades 1→0 in 0.2s (ring REPLACES it, no double border); POP ring from .92 0.38s back.out(2); winner .pos x→-40 rotationY→0, .scl 1.06 0.5s power3.out; loser drifts x -24 rotationY 7; pulse ring (opacity .9→0, scale 1→1.12, 0.7s) +0.1s; then .scl 1.06→1.075 linear hold with immediateRender:false.
- **Tempo:** @4.74–4.87 for 'feito' 4.83.
- **Armadilhas:** Chained fromTo on the same property later in the timeline needs immediateRender:false or it overwrites the earlier state on load.

### Cycle payoff: icon tile + self-drawing loop arrow

- **Quando usar:** 'paga a si mesma', loops, flywheels, self-funding ideas.
- **Como:** Cards exit sideways (L x -240, R x +180, blur 14, 0.24s power2.in). Tile 150px radius 35 POP {scale .5, blur 8}→ back.out(1.6) 0.5s, then 1→1.05 linear hold. Arc: SVG path r128 ~300°, stroke #C6F02A 16px, dasharray 670.21 draw 0.6s power2.out, wrapper rotates -50→20 linear 1.32s (draw + spin = momentum), drop-shadow on svg. Arrowhead polygon scales 0→1 back.out(2.4) 0.24s with svgOrigin at the path end, starting exactly when the draw finishes (+0.5s).
- **Tempo:** Exit 5.60; tile 5.74; arc 5.76 (opacity flip 5.79); head 6.26 — under 'isso faz' 6.13–6.29.
- **Armadilhas:** Arc opacity flips 0.03s after draw start (cap-dot fix). Use svgOrigin (not transformOrigin) for SVG children.

### Kinetic 2-group sentence + lime block wipe

- **Quando usar:** The one-line takeaway of the reel.
- **Como:** Geist 700 76px/86px, -0.035em, centred, width 900 at top 1330; each line a fixed-height block, words inline-block. Group 1 words: {opacity0,y50,blur12}→ 0.38s power3.out, stagger 0.04. Group 2 (highlight phrase) punches DOWN from scale 1.3, blur 12 → 1, 0.32s expo.out. Lime bg span inset -16px sides, radius 16, scaleX 0→1 from origin 0 50%, 0.3s power3.out, text in --limeInk. Whole block scale 1→1.025 linear to the exit.
- **Tempo:** G1 5.80, G2 6.08, block 6.30, exit 7.08 (0.24s, ends 7.32 < 7.37 − 1 frame).
- **Armadilhas:** No <br>: lines are separate block divs with white-space:nowrap. Exits must END ≥1 frame before data-duration (half-open clip window) or the last frame shows a half-blurred ghost.

**Lições da cena:** Nest wrappers per responsibility (position / scale / float) so tweens never collide. Lead every beat ~0.1s before the word. Cap-dot bug on stroke draws: hide until draw starts. Pulses = instant set then expand (seek-safe). Later fromTo on an already-tweened prop → immediateRender:false. Vary eases inside a scene (power3.out entries, back.out pops, expo.out punch, power2.in exits, none for holds). Every hold has a linear scale drift or sine float — never a dead frame. Exit 0.24–0.26s power2.in and finish ≥1 frame before scene end.

## s6-teste

**Batida:** PROOF / product demo. Global 29.40–38.90 (9.50s). 'então obviamente que eu fui testar | liguei pro MCP | do claude no higgsfield | e detalhei exatamente como eu queria esse meu personagem de IA | em menos de 5 minutos eu tinha ele pronto'. One held app window cycling states (connectors → chat typing → generating) then the result card grows out of a skeleton tile and is HELD (no exit) for a card-morph handoff to s7.

**Layout:** Window 940x700 at (70,1010) — inside safe box x70–1010; header 96px; connector rows 884x116 radius 24 at window-local tops 172/304/436, 'add' dashed row at 568; ring 900x132 at (20,296). Composer 884x228 at (28,452). Skeleton tiles top 352 local. Timer pill row top 933, height 64 (centre y 965) — just under the caption seam. Sheet card 900x509 centre (540,1390); 'pronto' pill 172x60 at (70,1080). Sticker overhangs the window edge (decor may bleed).

**SFX:** Scene global start 29.40. whoosh .18 @29.42 (0.02 window enters) · pop .26 @30.80 (1.40 'teste real' sticker) · click .31 @31.78 (2.38 MCP pill) · click .42 @33.30 (3.90 toggle knob) + ping .25 @33.35 (3.95 ring/connected, track 11) · whoosh-short .12 @34.20 (4.80 A→B crossfade) · typing .34 @34.32 dur 1.5 (4.92 typing start, track 12) + typing .34 @35.82 dur 0.9 (6.42 continuation — two clips cover the 2.38s type) · click .42 @36.76 (7.36 send press) · pop .26 @37.05 (7.65 timer pop) · whoosh .20 @37.98 (8.58 window out / card grows) · sparkle .18 @38.10 (8.70 card flash + sparkles) · pop .29 @38.45 (9.05 'pronto' pill). Next scene whoosh-short @39.00 (s7 morph).

### Held app window with staggered row cascade

- **Quando usar:** Showing a tool/app UI that will change state several times.
- **Como:** Window 940x700 white radius 34 at (70,1010); traffic-light dots, logo 46px + title 36px/600, hairline at y95. Wrapper stack: #drift (idle y/scale) > #winbox (IN/OUT) > #push (camera push-in, origin at the composer 470px 500px) > #win. Window IN y:120 0.5s @0.04; label IN {y16,s1,blur6} 0.4s @0.22; rows IN {y26,s.98,blur8} 0.45s staggered 0.08 (0.26/0.34/0.42/0.50). Drift: y 0→6 linear 6.75s; scale 1→1.035 sine.inOut over the connectors hold, reset to 1 (0.4s) hidden under the A→B crossfade.
- **Tempo:** Settled by 'então' 0.31.
- **Armadilhas:** Separate wrappers for drift vs push vs IN/OUT, otherwise the camera push and blur exit overwrite each other's transform.

### Corner sticker + header pill 'punch then cool'

- **Quando usar:** Small meta tags on a word ('teste real', 'MCP', 'beta').
- **Como:** Sticker: lime pill 54px tall, Geist Mono 26/600, sits half off the window top-right (top -27, left 708), POP from scale .4 rotation -10 → rotation 4, 0.45s back.out(2). Header pill: opacity 0→1 0.12s + scale .5→1.18 0.16s power2.out, then →1 0.32s back.out(2.2); background starts LIME and cools to #EFEFEA (0.3s) after landing — draws the eye then gets out of the way.
- **Tempo:** Sticker @1.30 for 'testar' 1.37; MCP @2.30 for 'MCP' 2.41, cool @2.62.
- **Armadilhas:** POP helper here carries immediateRender:false (r0/r1 rotation params) so stickers stay hidden at frame 0 regardless of other tweens.

### Control-target sync (toggle ON + ring + status swap on one label)

- **Quando usar:** Connecting/enabling something in UI on the spoken name.
- **Como:** addLabel('hf', 3.86). At 'hf': knob x 0→38 0.28s power2.inOut; track bg #E2E2DC→#D4FF3A same; lime ring (900x132, radius 32) opacity 0 scale 1.08→1.02 back.out(2) 0.36s; row scale 1→1.02 back.out(2); siblings dim to opacity .42 + blur 1.5px (focus pull). Status swap without overlap: old label out y-10 0.12s power2.in at hf, new 'conectado' (green #4B7A00 + dot) in y12→0 0.3s at hf+0.14. Pre-cue on the previous word ('claude' 3.38): logo rotates 120° 0.7s + scale yoyo 1.18, and a radial lime glow behind the target icon fades in (lead the eye).
- **Tempo:** Label 3.86 for 'higgsfield' 3.97; pre-glow 3.30.
- **Armadilhas:** Keep all four channels on one label so they cannot drift apart when retimed.

### State crossfade with blur (A → B inside the same window)

- **Quando usar:** Switching screens without cutting the container.
- **Como:** State A to {opacity0, y-24, blur10} 0.26s power2.in @4.70; state B from {opacity0,y30,blur12} 0.4s power3.out @4.88 (slight gap, no double exposure). Greeting in B steps back (opacity .5, blur 2px) as depth-of-field when typing starts.
- **Tempo:** For 'e detalhei' 4.86–4.92.
- **Armadilhas:** Use the crossfade to hide resets (drift scale back to 1) so the next push-in starts clean.

### Typewriter with caret, authored line breaks and growing composer

- **Quando usar:** Prompt/search typing in a chat or input.
- **Como:** Seek-safe proxy: fromTo {n:0}→{n:len} ease none, onUpdate writes textContent only when Math.round(n) changes. Lines authored with '\n' + white-space:pre-wrap so wrap position is a fact, not layout luck. Composer drawn at final 3-line size (884x228); growth = cap + text translateY 80→40→0 and body clip-path inset(top) synced (0.18s power3.out) at the exact char time of each break: wrapAt(m)=T0+((m−0.5)/len)*TD. Caret 3x34px opacity flip on at start, off at end. Camera push-in on the composer: scale 1→1.065, y -16 sine.inOut over the typing (2.2s), eases back 0.3s on send. Composer sits 72px higher while typing, docks y→0 on send.
- **Tempo:** T0 4.92, TD 2.38 (ends 7.30) — duration chosen to fill the sentence 'detalhei … personagem de IA'.
- **Armadilhas:** Never tween height — use clip-path + translate. Keep wrap times derived from the same LINES array as the text.

### Press-release send + text flies into bubble

- **Quando usar:** Submitting a prompt/message.
- **Como:** Send button scale →.86 0.08s power1.in @7.30, →1 0.45s back.out(2.2) @7.38; lime ring burst opacity .9→0 scale 1→2.4 0.5s. Prompt text block moves x92 y-336 0.32s power3.inOut into the right-aligned bubble (same width + same breaks = identical wrapping); bubble fades/scales .94→1 0.26s at +0.14; composer collapses (cap y 0→80, clip 26→106px) and placeholder fades back.
- **Tempo:** Press 7.30–7.38 (cue none: lands just before 'em' 7.63).
- **Armadilhas:** Caret off at 7.34 before the text moves.

### Agent theater + count-up timer with spinning hand

- **Quando usar:** 'em X minutos', generation/progress moments.
- **Como:** 'gerando personagem…' mono text with background-clip:text lime sheen (background-position 100%→0% 0.5s, repeat 1 — finite); 3 skeleton tiles 284x150 IN stagger 0.06 with lime sheen sweep x -180→300 0.42s repeat 1. Timer pill (lime, Geist Mono 30/600 tabular-nums, stopwatch svg) POP from .55 back.out(1.8) 0.42s above window (centred y 965); seconds proxy 0→287 0.9s power2.out formatted mm:ss (writes only on change); hand rotation 0→1800 svgOrigin '17 19.5' same ease; final bump scale 1.07 yoyo 0.12s at landing. Window nudged down y 6→24 (0.42s) as the pill lands above it.
- **Tempo:** Timer 7.58–8.55 across 'em menos de 5 minutos' 7.63–8.37; bump 8.53.
- **Armadilhas:** No repeat:-1 (non-deterministic length); all loops finite.

### Result card grows out of a skeleton tile (hand-off anchor)

- **Quando usar:** Revealing the generated result; preparing a card-morph handoff to the next scene.
- **Como:** Window OUT (blur 14, scale 1.03, 0.25s) @8.56 starting before the card so it never prints over sharp UI. Card final: 900x509 at left 90, top 1135.5 (centre 540,1390). Start scale CS = 284*1.012/900, start y = tile centre − final centre (computed from drift y 28 and drift scale 1.012 at 8.62), borderRadius 20/CS → 34 so the corner radius looks constant while scaling; 0.48s power3.out. Image blur 12→0 0.5s; inset 8px lime flash in 0.14s then out 0.36s. 5 sparkles (34–46px) pop 0.14s, fly 30–60px out with rotation -30→30, fade by 9.37. 'pronto ✓' pill POP rotation -14→-4 at the card's top-left @9.02.
- **Tempo:** Card 8.62 for 'eu tinha' 8.69; pronto 9.02 for 'pronto' 9.11.
- **Armadilhas:** NO exit: held to 9.50; s7 begins with an IDENTICAL card + pills (same px) and morphs. Compute start geometry from the parent's drift at that exact time or the grow 'jumps'. Sparkles fully gone before the cut so the handoff frame is clean.

**Lições da cena:** One held container + internal state changes reads more premium than cutting between screens. Use addLabel for multi-channel beats. Typing: proxy object + write-on-change + authored breaks + clip/translate growth; size the SFX typing clips to the exact typing window. Never tween width/height/top/left; use transforms, clip-path. Count-ups write only on integer change. Compute hand-off geometry numerically (include parent drift/scale). A scene that hands off to a card-morph must NOT exit; next scene starts with pixel-identical elements. Filters inside overshooting (back.out) eases can leave residual blur on seek — keep blur on a power ease channel and put scale on back.out (two-channel pop), as done for the timer/sticker POP (no filter) and card (blur on child img with power2.out).

## s7-genjutsu

**Batida:** Proof payoff, global 38.90-43.10 (4.20s). Line: "como vocês podem ver | esse sou eu | e esse aqui é o personagem". Cues (local): ver@0.66, esse sou eu@0.98-1.46, esse aqui@2.02, personagem@2.72 (speech ends ~3.3, hold to 4.2). The s6 sheet card morphs into the RESULTADO portrait. ORIGINAL (the creator's own take, muted video) enters on the left. Labels ORIGINAL · Genjutsu · RESULTADO run along the top, and a lime ring plus a sparkle burst lands on "personagem".

**Layout:** Canvas 1080x1920 at 30fps. Camera 0-780 sits above the scenes. Caption band 800-920 belongs to captions.html. Stage 940-1860, safe box x70-1010 / y950-1680. s7: label row centers at y 988 (x 310 / 536 / 770). Two cards 400x640 at y 1040-1680, left 110-510, right 570-970, 60px gutter. The ring is inset 8px outward. The burst origin is (952,1058), with stars kept inside x<=1056 and y>=926. The scene paints no background (index.html owns the paper and glow).

**SFX:** Scene global start 38.90 (local = global - 38.90). Note: sparkle 38.10 (.18) and pop 38.45 (.29) belong to the end of s6. whoosh-short.mp3 39.00 vol .16 -> local 0.10, morph start. pop.mp3 39.45 vol .23 -> 0.55, Genjutsu pill pop. whoosh-short.mp3 39.62 vol .12 -> 0.72, R stack slides right. whoosh.mp3 39.82 vol .16 -> 0.92, ORIGINAL card enters. pop.mp3 40.90 vol .26 -> 2.00, RESULTADO label. sparkle.mp3 41.60 vol .20 -> 2.70, ring + burst on 'personagem'. No SFX on the exit (3.92). Volumes stay low (.12-.26) under the voice. Overlapping hits alternate track-index 10/11/12.

### Pixel-identical hand-off from previous scene (frame-0 replica)

- **Quando usar:** Any scene whose first frame must be the previous scene's last frame, so the cut is invisible and one object reads as continuing.
- **Como:** Rebuild s6's held state in s7 markup with the same boxes and CSS: sheet0 at left 90 / top 1135.5, 900x509, r34, plus the same timer pill (lime, 64px, top 933) and 'pronto' pill (left 70, top 1080, rotate -4deg). The previous scene has NO exit (s6 holds to its end). At M0=0.10, tl.set swaps sheet0 opacity 0 and the morph card opacity 1. The morph card's p=0 pose is mathematically identical to sheet0, so the swap can't be seen. Carry-over pills leave with OUT: timer at 0.05 (d .24, scale .92, blur 12) and pronto at 0.07 (d .22, scale .9, blur 12).
- **Tempo:** Replica holds 0-0.10. Swap on the first moving frame. Carry-overs clear by ~0.30, before the first spoken cue that matters.
- **Armadilhas:** The replica must match the previous scene's final pose exactly: same CSS, same shadow, filter blur(0px). Otherwise the cut pops. Put the previous scene's exit only in the new scene, never in both.

### Card-morph (landscape sheet -> portrait card) with content zoom + locked crossfade

- **Quando usar:** When a card in the previous beat needs to turn into the subject of the next beat with a different aspect ratio and position, e.g. a screenshot becoming a result card.
- **Como:** Lay the morph box out at its FINAL slot: left 570, top 1040, 400x640. Then tween FROM a transformed start in one tween: x 540-770+230, y 30, scale S0=900/400=2.25, clipPath inset(206.89px 0 206.89px 0 round 34/S0 px) -> x0 y0 scale1 clipPath inset(0 round 30px). Use power3.inOut, 0.56s, force3D:false. The aspect change is a paint-only clip-path and never touches width/height. Inner sheet image tweens x -95, y -206.89, scale 2.8288 (zooms into its own face). The portrait layer rides the inverse path (origin 0 0, same ease): from x -SH_X/SH_S, y CLIP_V, scale 1/SH_S to identity, so the faces stay registered. Crossfade portrait opacity 0->1 at 0.58 (0.26s, power1.inOut) once the shapes have converged (p>~0.93), and hide the sheet image at 0.86. The drop-shadow goes on a PARENT wrapper via filter: drop-shadow(...) so it follows the clipped shape. Afterwards the whole R stack slides x -230->0 (0.5s power3.inOut at 0.72), so the morph lands centered and then makes room as ORIGINAL enters.
- **Tempo:** 0.10-0.66 morph, 0.58 crossfade, 0.72-1.22 slide right. The slide overlaps ORIGINAL's 0.92 entrance, so the two cards read as one push.
- **Armadilhas:** Put the slide on the outer exit wrapper (Rexit), not on Rfloat. Rfloat's transform is written by the float onUpdate and would clobber it. Box-shadow on a clipped element gets clipped, so use drop-shadow on a parent. Crossfading too early shows the portrait's rectangle edges inside the card.

### Live-media takeover with pull-back reveal (still -> video)

- **Quando usar:** When a still placeholder should 'come alive' as video, e.g. an AI result clip replacing a portrait.
- **Como:** <video id=s7-resultado data-start=0.8 data-duration=3.4 data-media-start=0.94> sits inside a wrapper (gjin) that fades in 0->1 over 0.24s at 0.80. The inner gjkb gets a face-anchored pose helper: gpose(s,tx,ty) = {x: tx-GF.x*s, y: ty-GF.y*s, scale:s}, where the source face is at GF=(183,355) card px. It goes from gpose(3.0,200,250), matched to the still's face size, to gpose(1.58,200,225) (head-and-shoulders) over 0.95s power3.inOut. Then a slow linear push to 1.64 until 3.95. The still underneath gets a Ken Burns scale 1->1.08, linear, from 0.66 to 3.95.
- **Tempo:** Starts at 0.80, just after 'ver' (0.66), and resolves before 'esse sou eu' (0.98) lands on the left card.
- **Armadilhas:** object-fit/object-position on <video> was ignored in render. Fix: give the video its native-aspect box (400x711.11, top -35.56, object-fit: fill) and frame it with transforms on a wrapper. Never animate the video element's own box. Never put data-start on an ancestor of a video.

### Side-by-side synced video cards (ORIGINAL x RESULTADO) with book-open tilt

- **Quando usar:** Before/after or original/AI comparisons.
- **Como:** Two 400x640 slots: left 110..510 (center 310,1360) and right 570..970 (center 770,1360), 60px gutter, stage center x 540. ORIGINAL enters at 0.92 from x -150, rotationY 24, scale .9, blur 16, opacity 0 to x0, rotationY 5, scale 1, blur 0. That's 0.55s power3.out with transformPerspective 1400. RESULTADO settles to rotationY -5 (0.7s sine.inOut at 0.61), so the pair opens like a book facing the viewer. Both videos are framed face-anchored: ORIGINAL face LF=(180,355) placed at (200,225), scale 1.32->1.38 linear over the hold. The face sizes match (~140px) so the gestures read side by side. The ORIGINAL card is dark (--ui) with r30.
- **Tempo:** The ORIGINAL entrance starts ON 'esse' (0.92 vs cue 0.98, ~0.06 lead) and peaks on 'sou eu'.
- **Armadilhas:** Use force3D:false on the 3D/scale tweens to avoid blurry raster layers. Choose a source take/time where the face is framed similarly (switched to t4-prova.mp4 @13.02s).

### Label row: spring pops on spoken word, equal-gap anchors

- **Quando usar:** Tagging the elements of a comparison (ORIGINAL / tool / RESULTADO).
- **Como:** Static .anc boxes (position absolute, translate(-50%,-50%)) at y 988, x 310 / 536 / 770. GSAP animates only the child. The tool pill sits at the midpoint of the two labels so both gaps are ~44px. Labels: Geist Mono 26px, .06em, 50px tall pills. ORIGINAL is white with a 2px line ring, ink2 text. RESULTADO is lime with limeInk 600 text. The Genjutsu pill is dark #141416, 52px tall, with a 34px lime tile clipped to the logo squiggle plus Geist 600 26px white text. POP = opacity 0, scale .6, y 10-12 -> 1. Durations: Genjutsu 0.42s at 0.52, ORIGINAL label 0.38s at 1.04, RESULTADO 0.40s back.out(1.8) at 1.95, all back.out(1.7-1.8). The whole row drifts y 0->-6 (sine.inOut, 0.6-3.92).
- **Tempo:** Each pop lands ~0.06-0.10s before its word: Genjutsu on 'ver' 0.66, ORIGINAL label just after the card enters, RESULTADO on 'esse aqui' 2.02.
- **Armadilhas:** Keep the labels below the caption band (800-920). Clip the app icon to its mark so the tiny wordmark doesn't show at 34px.

### Lime ring hug + punch + deterministic sparkle burst

- **Quando usar:** The single payoff word of a scene (here 'personagem').
- **Como:** The ring is 8px outside the card (left 562, top 1032, 416x656, r 38 = 30+8): 6px lime border, 0 0 0 10px rgba(212,255,58,.28) halo. It goes from opacity 0, scale 1.06 to 1/1 in 0.36s back.out(1.8) at 2.64. The card punches with Rtilt scale 1->1.035 (0.3s power2.out) then settles to 1.02 (0.6s power2.inOut). Burst: 8 four-point lime stars with a white core (sizes 26-46px, drop-shadow glow), fanned -118 to -18deg from the card's top-right corner. Speeds are pre-solved (260-380 px/s) so every star stays on screen and out of the label/caption zone. Seeded prand(n)=frac(sin(n*127.1+311.7)*43758.5453). One proxy tween (T 0->1, 0.6s, linear at 2.68) drives all stars in onUpdate: drag 1-0.45T, gravity 80, scale-in over the first 18% then shrink, fade over the second half.
- **Tempo:** Ring at 2.64, burst at 2.68, both peaking on 'personagem' at 2.72.
- **Armadilhas:** No Math.random and no per-particle tweens with repeat. Opacity must be 0 when T===0 so seeking backwards hides the stars. Keep the burst behind/away from the labels.

### Phase-opposed float while holding + clean exit

- **Quando usar:** Any hold of 2+ seconds with two cards. Never leave a dead frame.
- **Como:** One proxy tween p: 0 -> (F1-F0)/2.6*2π from 0.66 to 4.17 (linear). onUpdate writes translateY(±sin(p)*6*env) to Lfloat and Rfloat in opposite phase. env=min(1,p/1.2) eases the amplitude in. Exit: OUT labels at 3.92, L at 3.94, R at 3.95, each 0.2s, to opacity 0, scale 1.04, blur 14, power2.in. Everything ends by 4.15 < 4.166 (the last frame).
- **Tempo:** Float from morph end to the scene end. The exit is staggered 0.01-0.02s, starts after the speech ends (~3.3) and finishes 1+ frame before 4.2.
- **Armadilhas:** Wrapper nesting gives each concern its own element: Lexit > Lfloat > Lin > card > Lkb (and Rexit > Rfloat > Rtilt > Rshadow > morph). Tweens never fight over one transform. Exits must END before data-duration, because the clip window is half-open and a cut-off exit flashes.

**Lições da cena:** (1) Lay out at the FINAL position and tween FROM an offset. Only transforms and clip-path, never width/height/top/left. (2) Use one wrapper per concern (exit / float / enter / tilt / ken-burns). Code that writes style.transform in onUpdate must own its element exclusively. (3) Frame video with transforms on a wrapper, with the video at its native aspect and object-fit fill. object-fit/object-position on <video> was ignored at render. (4) Face-anchored framing math (x = target - face*s) keeps faces pinned and matched in size across cards. (5) The previous scene holds without an exit, and the next scene's frame-0 replica takes over, for invisible continuity. (6) The storyboard was a plan. The final build swapped the source take (t4-prova @13.02) and replaced the placeholder with a real Genjutsu video, so keep media boxes swappable by id. (7) Use force3D:false on scale and 3D tweens for crisp text and images.

## s8-cta

**Batida:** Final CTA, global 43.10-47.90 (4.80s, last frame of the video, NO exit). Line: "se vocês quiserem criar o seu | comente aqui | CLONE | que eu envio o passo a passo". Cues: comente@1.48, aqui@1.86, CLONE@2.20, envio@2.94, passo a passo@3.60-3.94. An Instagram comment sheet rises in. The input focuses, CLONE types in letter by letter, send gets pressed, and the word flies into a new comment that pushes the list down. A DM banner drops in on 'envio', and a lime ring with echoes plus a heart like carry the hold.

**Layout:** Sheet 940x590 at (70,1090), with a 64x8 grabber, 'Comentários' 34px/600 at the top (y 32), and hairlines at 96 and 386. Rows are 940x140: avatar 64 at (32,22), name at x116 (28/600 + 24px meta time), text at y54 (30/500), reply at y100, heart on the right (40). The new row is at top 104 and the old row at 244. Emoji row y 406 (852 wide, space-between). Input pill 726x72 at (106,488), send 64px at (844,492). DM banner 900x120 at (90,946), just under the caption band. Meta color #66666E (darker than --mute for contrast). Instagram blue #3D8BFF is only for send.

**SFX:** Scene global start 43.10. whoosh.mp3 43.12 vol .18 -> local 0.02, sheet blur-rise. key-press.mp3 x5 at 45.12 / 45.18 / 45.24 / 45.30 / 45.36, vol .48, each on its own track (10-14) -> local 2.02-2.26, one per letter of CLONE, exactly matching the SEQ table. click.mp3 45.58 vol .42 -> 2.48, send release. whoosh-short.mp3 45.60 vol .12 -> 2.50, FLIP travel. pop.mp3 45.65 vol .26 -> 2.55, new comment push. notification.mp3 45.98 vol .30 -> 2.88, DM banner. No SFX on the ring, like or echoes (the hold stays quiet so the voice CTA carries).

### Blur-rise sheet entrance + emoji wave

- **Quando usar:** Opening a UI mock (sheet or app card) at the scene start, with secondary elements filling the gap before the first key word.
- **Como:** IN(sheetE, 0.0, {y:140, d:0.5, b:14}) means opacity 0, y 140, scale .94, blur 14 -> 1/0/1/0, power3.out. The sheet is 940x590 at left 70, top 1090, with radius 40 on the top and bottom surfaces. The shadow is drop-shadow on a wrapper (sheetW) so the two-part surface casts a single shadow. The 8 emoji (44px, row y 406) POP left to right at 0.26 + i*0.08: from scale .4, 0.36s, back.out(1.7), landing by ~1.2.
- **Tempo:** Starts at local 0.00 so there's no bare stage at the s7->s8 cut. The emoji wave keeps things moving through 'criar o seu' (0.84-1.24).
- **Armadilhas:** Load emoji through a local() @font-face (Apple Color Emoji / Noto / Segoe) so they render consistently. Pre-cue states live in CSS (opacity:0) so frame 0 is correct.

### Input focus + discrete typewriter with caret (key-press synced)

- **Quando usar:** Typing a keyword CTA (CLONE, LINK, etc.) into a field.
- **Como:** Focus at 1.40: a 2px ink outline over the 726x72 pill goes from opacity 0, scale 1.015 to 1/1 in 0.2s power2.out. The placeholder fades out in 0.12s. Typing uses a SEQ table of discrete states: '' @0, C @2.02, CL @2.08, CLO @2.14, CLON @2.20, CLONE @2.26, '' @2.50 (cleared on send). One linear proxy tween drv.t 0->4.8 drives it. onUpdate looks up the text for time t and writes textContent ONLY when it changes. Caret is 3x38px ink, margin-left 3. It's visible 1.44-2.50, solid while typing (1.96-2.42) and blinks otherwise as a 0.8s square wave (sin > -0.2). Typed text is Geist 700 32px.
- **Tempo:** The first letter lands at 2.02, 0.18s before the spoken 'CLONE' (2.20), so the word completes (2.26) right on it. Letters are 0.06s apart, equal to the key-press SFX spacing.
- **Armadilhas:** Never append characters across frames. Derive the state from absolute t so seeking in either direction is correct. Write to the DOM only on change.

### Send press-release spring + radial burst

- **Quando usar:** Any 'submit/send' moment.
- **Como:** Send is a 64px #3D8BFF circle with a white arrow at opacity .4 (disabled). At 2.28 it goes to opacity 1 (0.1s). Press at 2.40: scale 1->.85 over 0.08s power1.in. Release at 2.48: scale ->1 over 0.5s back.out(2.2). Burst: a radial-gradient blue disc behind it goes opacity 0->.9 and scale 1->2.4 (0.22s power2.out), then ->0 and 3.0 (0.4s power2.in at 2.70). Back to idle at 2.62-2.70: send opacity .4, focus outline out, placeholder back.
- **Tempo:** The release (2.48) sits on the click SFX at local 2.48.
- **Armadilhas:** Restore the idle state afterwards so the UI reads as 'posted'. Leaving the field focused looks unfinished.

### FLIP word travel (typed text -> comment token) with lime block

- **Quando usar:** When the typed word should visibly BECOME the posted comment, so the viewer's eye is carried along.
- **Como:** A 'fly' traveller has the same box model as the destination token (left 116, padding 14, 36px, line 48). From x 134-(116+14*SC0), y 384-172, scale SC0=32/36, weight 700 to identity and weight 800 over 0.45s power3.inOut at 2.50. A lime block inside grows scaleX 0->1 (origin left, 0.24s power2.out at 2.53). A lift shadow fades in at 2.55 and out at 2.81. On the landing frame (2.95), tl.set swaps: the real token's block scaleX 1, its text opacity 1, the fly opacity 0. Same box, so the swap can't be seen. The token is Geist 800 36px limeInk on lime, r12.
- **Tempo:** 2.50-2.95. Starts as the input clears and lands just before 'envio' (2.94).
- **Armadilhas:** The traveller must share font, padding and line-height exactly with the target, or the hand-off frame jumps. It renders above the sheet surface but inside the sheet's coordinate space, so it follows the drift.

### Comment push-down (anchored-layout-expand via y)

- **Quando usar:** Inserting a new row at the top of a list without animating height.
- **Como:** Everything below the new slot (old comment, bottom surface, emoji, input) is in one 'below' group, pre-parked with gsap.set y -ROW_H (-140). At 2.53 it goes y -140->0 over 0.5s power3.out. The new row is already laid out at top 104. Its tint (#F6FFD4, r26) fades in over 0.35s at 2.58. Avatar, name, reply and heart rise from y 18 with blur 4 and opacity 0 (0.4s power3.out, stagger 0.03, at 2.56).
- **Tempo:** 2.53-3.03, overlapping the FLIP so one motion reads as 'posted'.
- **Armadilhas:** One tween drives the seam. Never tween height/top. Split the sheet surface into top and bottom parts so the gap opens cleanly while the shadow stays one shape.

### Two-channel drop-in (geometry on back.out, filter/opacity on power2.out)

- **Quando usar:** Any entrance that overshoots AND blurs, e.g. a notification or DM banner.
- **Como:** DM banner: 900x120 at left 90, top 946, r28, white. The avatar has a white + lime double ring. Name 'guiborges' plus a 'DM' mono chip, the message at 28px nowrap. Tween A: y -60, scale .96 -> 0/1 over 0.55s back.out(1.4). Tween B (separate): opacity 0, blur 10 -> 1/0 over 0.3s power2.out. Both start at 2.86, origin 50% 0%.
- **Tempo:** 2.86, peaking on 'envio' at 2.94.
- **Armadilhas:** BUG FIXED: putting filter inside an overshooting ease drives blur negative, which is invalid CSS and leaves stale blurred frames when seeking. Only geometry may overshoot. Keep the banner top >= ~923 so it never enters the caption band, including during the drift.

### Lime ring + echo pulses + token punch + like, held to the end

- **Quando usar:** Final emphasis that must stay alive through the last frame without an exit.
- **Como:** The ring hugs the tint with an 8px gap (left 16, top 104, 908x140, r34 = 26+8, 6px lime, 8px halo). It goes opacity 0, scale 1.05 -> 1 in 0.36s back.out(1.8) at 3.52. Echo ring (4px): opacity .9, scale 1 -> 0, 1.07 over 0.7s power2.out at 3.66. The token punches scale 1.12 (0.14s power2.out at 3.54), then settles to 1.06 (0.42s back.out(2)). The heart fills red #FF3B5C: opacity 0, scale .3 -> 1 in 0.42s back.out(2.4) at 4.02. Second echo: opacity .6 -> 0, scale 1.05, 0.6s at 4.16, ending 4.76 < 4.767. Whole-stage drift: y 0->-14 and scale 1->1.02, linear, 0.65-4.78, origin (540,1380).
- **Tempo:** Ring at 3.52 on 'passo' (3.60), heart at 4.02 after the speech, final echo 4.16-4.76.
- **Armadilhas:** The ring lives outside the drop-shadow group and above the pushed list. Every tween must end inside the last frame (4.767). Use linear drift so both the early hold and the final 0.7s visibly move. An eased drift looks frozen at the end.

**Lições da cena:** (1) For CTA endings, skip the exit and hold to the last frame. Keep it alive with linear drift, echo pulses and a late micro-beat (heart like). End every tween inside the last frame. (2) Typing and other discrete UI state is a time-indexed lookup table driven by one proxy tween, written only on change. Seek-safe, and SFX timestamps are copied from the same table. (3) Split overshoot: geometry on back.out, filter/opacity on power2/power1. Never let blur overshoot. (4) FLIP hand-offs need identical box models at the landing frame, then a tl.set swap. (5) Grow lists by translating a pre-parked 'below' group, never by height. (6) Pre-cue states go in CSS or gsap.set so frame 0 renders correctly. Use immediateRender:false on later fromTo's targeting the same element. (7) Cross-scene: index.html places all SFX on tracks 10-14 at low volumes (.12-.48, key presses loudest, whooshes softest), aligned to the motion start (whoosh) or the peak frame (pop/click/ping), ~0-0.1s before the spoken word. Captions own y 800-920, and no scene content may sit there while held.
