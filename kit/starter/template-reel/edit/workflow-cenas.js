export const meta = {
  name: 'reel-cenas',
  description: 'Build the stage scenes of a talking-head reel (one builder per group) then adversarially review+fix each group with dense snapshots',
  whenToUse: 'Depois do STORYBOARD.md pronto: constrói e revisa as cenas de motion (compositions/*.html) de um reel HyperFrames. Passe args {project, kit, groups}.',
  phases: [
    { title: 'Build', detail: 'one builder per group, 2-3 scenes each, adapting the proven example scenes' },
    { title: 'Review', detail: 'fresh adversarial reviewer per group: dense snapshots, fix, re-verify' },
  ],
}

// =====================================================================================================================
// workflow-cenas.js: constrói as cenas de motion do reel com vários agentes e revisa cada uma com um revisor
// adversarial (que parte do princípio de que há bugs, olha quadros reais e corrige). Ferramenta Workflow do Claude Code.
//
// QUANDO RODAR: depois de DESIGN.md + STORYBOARD.md prontos (o storyboard é o contrato dos agentes) e do index.html e
// da legenda gerados pelos scripts (edit/build_index.py, edit/build_captions.py). Os agentes escrevem SÓ as cenas em
// compositions/<id>.html. Depois: python3 edit/tools/collect_sfx.py <journal.jsonl> e python3 edit/build_index.py.
//
// COMO RODAR: no Claude Code (app Claude, aba Code), dentro da pasta do projeto. O Workflow só roda quando você pede
// explicitamente para "usar um workflow". Não use a palavra "ultracode": ela liga workflows para a sessão INTEIRA
// (toda tarefa seguinte vira workflow e o gasto dispara). Não edite este arquivo: tudo entra como args. Exemplo de pedido:
//
//   use um workflow com o script <caminho completo>/edit/workflow-cenas.js e estes args (objeto JSON):
//   {
//     "project": "/caminho/completo/do/seu-projeto",
//     "kit": "/caminho/completo/da/pasta/starter",
//     "groups": [
//       [ { "id": "s1-hook", "start": 0, "dur": 5.567, "adapt": "scenes-exemplo/s1-hook.html", "rec": "s1-hook" },
//         { "id": "s2-dinheiro", "start": 5.567, "dur": 3.166, "adapt": "scenes-exemplo/s3-calc.html", "rec": "s3-calc" } ],
//       [ { "id": "s3-cta", "start": 8.733, "dur": 6.0, "adapt": "scenes-exemplo/s8-cta.html", "rec": "s8-cta" } ]
//     ]
//   }
//
// ARGS:
//   project      (obrigatório) pasta do projeto HyperFrames (tem DESIGN.md, STORYBOARD.md, index.html, compositions/).
//   kit          (obrigatório) pasta que contém PADRAO-DE-QUALIDADE.md, RECEITAS-DE-MOTION.md e template-reel/
//                (a pasta "starter" deste kit, ou a cópia dela no seu computador).
//   groups       (obrigatório) lista de grupos; cada grupo é uma lista de cenas. Cada grupo = 1 construtor + 1 revisor.
//                Cena: { id, start (s globais), dur (s), adapt, rec }
//                  id    = nome da cena (vira compositions/<id>.html), igual ao STORYBOARD.md e ao SCENES do build_index.py
//                  adapt = cena(s)-exemplo a adaptar, relativas a template-reel/ (ex.: "scenes-exemplo/s3-calc.html" ou
//                          "scenes-exemplo/s5-ciclo.html (cards) + scenes-exemplo-2/s6-voce.html")
//                  rec   = (opcional) seção do RECEITAS-DE-MOTION.md (s1-hook … s8-cta, as cenas de scenes-exemplo/)
//                Cenas com transição entre si (o último quadro de uma = o primeiro da outra) vão no MESMO grupo.
//                2 a 3 cenas por grupo funcionou bem.
//   hyperframes  (opcional) comando do CLI. Padrão: "npx --yes hyperframes@0.8.141" (versão fixada = render reproduzível).
//   reference    (opcional) caminho do vídeo de referência/padrão-ouro com que o revisor compara o acabamento.
//
// CUSTO: é a etapa mais cara do processo. Agentes = 2 × número de grupos, rodando em paralelo. No reel que originou
// este kit (11 cenas em 5 grupos): 10 agentes, 647 chamadas de ferramenta, ~42 min e 905 snapshots conferidos.
// Consome MUITOS tokens. Para gastar menos: menos grupos/cenas, ou construa uma cena por vez sem workflow.
// =====================================================================================================================

const A = typeof args === 'string' ? JSON.parse(args) : (args || {})
if (!A.project || !A.kit || !Array.isArray(A.groups) || A.groups.length === 0) {
  throw new Error('workflow-cenas.js: faltam args. Use {"project": "<pasta do projeto>", "kit": "<pasta starter do kit>", ' +
    '"groups": [[{"id", "start", "dur", "adapt", "rec"}, ...], ...]}')
}
const PROJ = String(A.project).replace(/\/+$/, '')
const KIT = String(A.kit).replace(/\/+$/, '')
const HF = A.hyperframes || 'npx --yes hyperframes@0.8.141'
const REF = A.reference
  ? `${A.reference}`
  : `the reference reel analysed for this project (stills/contact sheets in ${PROJ}/reference/, if present) and DESIGN.md`

const GROUPS = A.groups.map((g, i) => {
  const scenes = (Array.isArray(g) ? g : (g && g.scenes) || []).map((s) => ({
    id: String(s.id), start: Number(s.start), dur: Number(s.dur), adapt: String(s.adapt || ''), rec: s.rec ? String(s.rec) : '',
  }))
  for (const s of scenes) {
    if (!s.id || !isFinite(s.start) || !isFinite(s.dur) || s.dur <= 0 || !s.adapt) {
      throw new Error(`workflow-cenas.js: cena inválida no grupo ${i + 1}: ${JSON.stringify(s)} (precisa de id, start, dur > 0 e adapt)`)
    }
  }
  if (scenes.length === 0) throw new Error(`workflow-cenas.js: o grupo ${i + 1} está vazio`)
  return { key: `g${i + 1}`, scenes }
})
log(`${GROUPS.length} grupos, ${GROUPS.reduce((n, g) => n + g.scenes.length, 0)} cenas, ${GROUPS.length * 2} agentes`)

const COMMON = `
PROJECT: ${PROJ}  (HyperFrames project, 1080x1920, 30fps). A vertical talking-head reel (Instagram Reels / TikTok)
edited in the format of the creator's gold-standard reel. Camera (talking head) on top y 0-780 is owned by index.html;
seam captions y 800-920 by compositions/captions.html; YOU build stage scenes (sub-compositions) that paint the stage y 940-1860.

READ FIRST (in this order, fully):
1. ${PROJ}/DESIGN.md — design truth: palette, type, surfaces, motion language, assets table, and the EXACT sub-composition contract (copy it).
2. ${PROJ}/STORYBOARD.md — the header table + universal rules + YOUR frame blocks (cues are scene-local word starts). The frame block is your contract: every beat on its word, exact geometry.
3. ${KIT}/PADRAO-DE-QUALIDADE.md sections 7 and 9 (motion principles, construction rules, technical pitfalls already solved).
4. The example scene(s) you adapt in ${KIT}/template-reel/ (scenes-exemplo/ and scenes-exemplo-2/) and their recipe sections in ${KIT}/RECEITAS-DE-MOTION.md. These are proven, seek-safe, render-verified code: reuse their helpers (IN/OUT/POP/COUNT/TYPE), wrapper structure, two-channel pops, rings, sheens, typewriters. Copy and adapt, don't reinvent. Asset paths are project-root relative (assets/..., same as the examples).
   The example scenes come from OTHER projects: their assets (images, videos) are NOT in this project, and their texts, @handles, names and numbers belong to those projects. Use ONLY the assets listed in DESIGN.md and the content in STORYBOARD.md.
Optional: the /hyperframes-core skill for the composition contract details.

HARD RULES:
- Write ONLY your scene files compositions/<id>.html (if a stub exists, replace it entirely; if the file does not exist, create it). Never edit index.html, captions.html, edit/*, or other scenes. Scenes add NO audio.
- Every id/selector prefixed with the scene id; <style>/<script> inside <template>; root div id="<id>-root" data-composition-id="<id>" data-width="1080" data-height="1920"; register window.__timelines["<id>"] = paused gsap timeline. Scene is a full-frame TRANSPARENT layer (except a B-roll stage, as in the example hook).
- Deterministic and seek-safe: fromTo with explicit from-states, finite repeats, no Math.random/Date, no CSS transitions/animations, never tween width/height/top/left (transforms, opacity, filter, clip-path only). onUpdate writers (typing/counting) write only when the visible value changes.
- NEVER put filter:blur on a back.out/elastic tween (blur goes negative on cold seek -> element stuck blurred). Two channels: opacity+blur on power2.out, scale on back.out on a separate tween or wrapper.
- One wrapper per responsibility; no property animated by two overlapping tweens on the same element.
- Nothing of the scene inside y 800-920 except cards passing through while entering/exiting. Key text inside x 70-1010, y 950-1680.
- Exits end >= 1 frame before the scene duration, unless the frame block says HOLD/NO EXIT.
- Videos inside scenes: muted playsinline, data-start/data-duration/data-media-start in scene-local seconds + data-hf-media-start-basis="local", NOT inside an element that has data-start; give the <video> its native-aspect box (e.g. 400x711 with top -35.5 for a 400x640 window) inside an overflow:hidden wrapper; object-fit is not honored in render inside transformed wrappers; never animate the <video> box itself. Keep data-media-start + data-duration within the file's length.
- Measure text widths after document.fonts.load where you re-center; tabular-nums on numbers.
- Numbers on screen: only those in the storyboard. No invented data, names or @handles.

VERIFY YOUR WORK (mandatory):
- cd "${PROJ}" && ${HF} lint   -> 0 errors for your files.
- Snapshots are of the WHOLE composition at GLOBAL times (global = scene start + local):
  cd "${PROJ}" && ${HF} snapshot --at <comma-separated global times> --no-end -o snapshots/build-<id> --describe false
  Take ~12-20 frames per scene: every beat's peak (word start + 0.05..0.15), mid-holds, the exit, the first and last frame. Read the PNGs/contact sheet and fix what's wrong (alignment of rings to targets, text overflow, overlaps with the seam/camera, wrong timing, stuck blur, dead holds). Iterate until it looks like the gold standard.
- Use your own snapshot output dir only. Do not run animation-map or leave any process running.
`

const BUILD_SCHEMA = {
  type: 'object',
  properties: {
    scenes: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' },
      summary: { type: 'string', description: 'what was built, beat by beat with local times' },
      sfx: { type: 'array', items: { type: 'object', properties: {
        t: { type: 'number', description: 'GLOBAL seconds' }, file: { type: 'string', description: 'one of click, glitch-1, impact-bass-1, impact-bass-2, key-press, notification, ping, pop, sparkle, typing, whoosh-short, whoosh' },
        volume: { type: 'number' }, duration: { type: 'number' }, why: { type: 'string' } }, required: ['t', 'file', 'volume', 'why'] } },
      handoff: { type: 'string', description: 'final-frame state / frame-0 state notes relevant to neighbouring scenes' },
      concerns: { type: 'string' },
    }, required: ['id', 'summary', 'sfx'] } },
  },
  required: ['scenes'],
}

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    scenes: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' },
      found: { type: 'array', items: { type: 'string' }, description: 'problems found (with local/global time)' },
      fixed: { type: 'array', items: { type: 'string' } },
      remaining: { type: 'array', items: { type: 'string' } },
      sfx: { type: 'array', items: { type: 'object', properties: {
        t: { type: 'number' }, file: { type: 'string' }, volume: { type: 'number' }, duration: { type: 'number' }, why: { type: 'string' } }, required: ['t', 'file', 'volume', 'why'] }, description: 'FINAL SFX list for the scene (global times) after your fixes' },
    }, required: ['id', 'found', 'fixed', 'remaining', 'sfx'] } },
    lint_clean: { type: 'boolean' },
  },
  required: ['scenes', 'lint_clean'],
}

const SFX_RULES = `SFX map (from the standard; volumes calibrated): card/window entering whoosh 0.16-0.20 at motion start; quick swap/morph/slide whoosh-short 0.12-0.22; pill/badge/tag pop 0.20-0.36 at the pop peak (~+0.05s); lime ring/highlight ping 0.22-0.32; toggle/click/send click 0.30-0.42 on the click frame; typing 'typing' 0.34 (duration = typing span) or key-press 0.48 per key; reveal sparkle 0.16-0.20; money slam impact-bass-2 0.08 + pop 0.33; DM notification 0.30. Max 1-2 SFX per beat; sound lands on the visual PEAK.`

function sceneBlock(s) {
  const rec = s.rec ? `recipes RECEITAS-DE-MOTION.md § ${s.rec}` : 'no dedicated recipe section: use the closest archetype in RECEITAS-DE-MOTION.md'
  return `- ${s.id}: global ${s.start.toFixed(3)} → ${(s.start + s.dur).toFixed(3)} (duration ${s.dur}); file compositions/${s.id}.html; adapt from (relative to ${KIT}/template-reel/): ${s.adapt}; ${rec}.`
}

const results = await pipeline(
  GROUPS,
  (g) => agent(
    `You are a senior motion designer building HyperFrames scenes for a vertical talking-head reel (Instagram Reels / TikTok).\n${COMMON}\nYOUR SCENES (build all of them, in order; they may hand off to each other — match final/first frames exactly where the storyboard says so):\n${g.scenes.map(sceneBlock).join('\n')}\n\n${SFX_RULES}\nReturn per scene: summary, the SFX you suggest (GLOBAL times), hand-off notes and any concerns.`,
    { label: `build:${g.scenes.map(s => s.id).join('+')}`, phase: 'Build', schema: BUILD_SCHEMA }),
  (built, g) => agent(
    `You are an ADVERSARIAL reviewer + fixer for HyperFrames scenes another agent just built for a vertical talking-head reel (Instagram Reels / TikTok). Assume there ARE bugs; your job is to find them by looking at real frames, then fix them in place.\n${COMMON}\nSCENES TO REVIEW:\n${g.scenes.map(sceneBlock).join('\n')}\n\nBuilder's report (claims to verify, not to trust):\n${JSON.stringify(built, null, 1)}\n\nPROCESS:\n1. Read DESIGN.md, your STORYBOARD frame blocks, then the scene HTML.\n2. Dense snapshots per scene: every 0.15-0.25s across the whole scene PLUS each beat's word start +0.08 (global times), into snapshots/review-<id>. Also COLD SEEKS: a separate snapshot run with only 3-4 isolated mid-pop times (that is where stuck/negative blur shows).\n3. Check against this list and write down every failure: (a) each beat peaks ON its word (storyboard cue) — not early, not late; (b) nothing of the scene in the seam band y 800-920 at rest, key text inside x 70-1010 / y 950-1680; (c) rings/outlines hug their targets exactly; pulled-out HTML twins line up with the print; (d) no stuck blur, no element left semi-transparent by mistake, no flicker/pop at scene start or end; (e) no dead hold > 1s (things drift/breathe); (f) exits end before the scene end unless HOLD; HOLD scenes truly hold to the last frame; (g) text never overflows its pill/card, no clipped descenders, legible sizes (>= 24px), contrast; (h) videos show the right content, framed (no black bars, no burned-in captions where avoided, synced where required), never frozen when they should play; (i) visual quality vs the gold standard (${REF} — look: premium, clean, the DESIGN.md accent, cards with real shadows) — anything that looks cheap/template-like or cluttered; (j) the storyboard content is fully present (every listed element/beat); (k) content honesty: no text, @handle, name, number or asset left over from the example scenes; nothing on screen that is not in the storyboard or DESIGN.md.\n4. FIX everything you can directly in compositions/<id>.html (keep the contract, keep it seek-safe). Re-snapshot the fixed moments to prove it. Run ${HF} lint at the end.\n5. Return found/fixed/remaining per scene and the FINAL SFX list (global times) adjusted to the real visual peaks.\n\n${SFX_RULES}`,
    { label: `review:${g.scenes.map(s => s.id).join('+')}`, phase: 'Review', schema: REVIEW_SCHEMA }),
)

return results.filter(Boolean)
