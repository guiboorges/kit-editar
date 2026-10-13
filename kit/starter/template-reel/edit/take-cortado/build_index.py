"""Gera index.html, a composição raiz do vídeo (câmera, cenas, legenda, SFX).

Pipeline : TAKE CORTADO. Copie este arquivo para <seu projeto>/edit/build_index.py.
Entrada  : edit/edl.json (build_edl.py) + edit/sfx_from_review.json (tools/collect_sfx.py, opcional) + o bloco EDITE AQUI
Saída    : index.html. ATENÇÃO: rodar de novo APAGA qualquer ajuste feito à mão (ou no app) no index.html.
Rodar    : python3 edit/build_index.py   (rode de novo depois do workflow das cenas, para entrar com os SFX)
Confira  : npx --yes hyperframes@0.8.141 snapshot --at <tempos logo depois de cada corte e das telas cheias> --no-end -o snapshots/cam-check
           olhos na mesma altura em todos os cortes, enquadramento B depois de cada corte, tela cheia abrindo e fechando.

Camadas (z): papel + brilho lima (0) · cenas/sub-composições (10) · câmera no painel de cima (20) · legenda (30)
Câmera   : UM <video> contínuo (media/take.mp4, o seu take já cortado: a voz nunca precisa ser recortada de novo).
           Caixas (wrappers), de fora para dentro:  #cam (clip-path: tela dividida / tela cheia) > #cam-full (y da tela
           dividida / y + escala da tela cheia) > #cam-move (punch-ins nas palavras-chave) > #cam-drift (empurrão lento
           em cada peça) > #cam-frame (enquadramento A/B de cada peça, trocado no quadro exato do corte).
Áudio    : a voz vem no próprio vídeo; os SFX são <audio> na raiz. Os arquivos de SFX NÃO vêm no kit: copie-os de
           ~/.claude/skills/media-use/audio/assets/sfx/ (instalados junto com as skills do HyperFrames) para assets/sfx/.
"""
import json, os

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDL = json.load(open(f"{P}/edit/edl.json"))
TOTAL = round(EDL[-1]["start"] + EDL[-1]["duration"], 3)   # duração do vídeo (do build_edl.py); pode usar TOTAL abaixo

# ===== EDITE AQUI =====
# Formato da tela (zonas do padrão). Só mude se mudar o formato inteiro do reel.
CAM_H = 780                      # altura do painel da câmera (tela dividida)
FACE_Y = 1034                    # linha dos olhos no espaço da câmera -> y≈320 dentro do painel (com SPLIT_Y)
SPLIT_Y = -714                   # deslocamento da câmera na tela dividida
FULL_Y = -234                    # tela cheia: olhos em y≈800 (42% da altura)
SCALE = {"A": 1.0, "B": 1.10}    # tamanho dos dois planos que alternam a cada corte

# Média de eyeY de todos os trechos (tools/face.swift). Põe a caixa base do vídeo com os olhos em FACE_Y.
EYE_MEAN_Y = 0.466               # EXEMPLO 2, reel CLONE (olhos a 46,6% da altura do quadro)

# Janelas de câmera em tela cheia (início, fim), em frases de conversa direta. Início de preferência num corte.
# A cena anterior SEGURA até a câmera cobrir o palco (wipe). Tem que ser IGUAL ao FULLS do build_captions.py.
FULLS = [(19.233, 21.10)]        # EXEMPLO: a 1ª das 2 telas cheias do exemplo 2 ("e pensa comigo…")
TR = 0.36                        # duração da abertura e do fechamento da tela cheia (power3.inOut)

# Grade de cor do take. 0.4 no exemplo 2 (o vídeo já vinha com look teal/laranja); 0.58 no exemplo 1.
GRADE = {"preset": "skin-soft", "intensity": 0.4,
         "adjust": {"contrast": 0.04, "highlights": -0.06, "shadows": 0.08, "vibrance": 0.04},
         "details": {"vignette": 0.02}}

# Cenas: (id, início global em s, duração em s). Vêm da tabela do STORYBOARD.md; o arquivo é compositions/<id>.html.
SCENES = [("s1-hook", 0.000, 5.567), ("s2-dinheiro", 5.567, 3.166), ("s3-quem-paga", 8.733, 3.167),
          ("s4-launchpoint", 11.900, 7.700)]     # EXEMPLO: as 4 primeiras das 11 cenas do exemplo 2

# Punch-ins de 1,05× na câmera: (início da palavra-chave no words.json, reset = o próximo corte).
# No último punch-in, se não há corte depois dele, use TOTAL (ou None) como reset.
PUNCH = [(1.74, 5.567), (8.08, 8.733), (10.32, 11.900), (18.60, 19.233)]   # EXEMPLO (exemplo 2: 10; o último era (60.17, TOTAL))

# SFX fixos do index: (tempo, arquivo sem .mp3, volume, duração ou None). Os SFX das cenas vêm sozinhos do
# edit/sfx_from_review.json. Aqui ficam os da câmera: para cada janela de FULLS, "whoosh" no início e
# "whoosh-short" em (fim − TR).
SFX = [
    (19.233, "whoosh", 0.14, None), (20.74, "whoosh-short", 0.12, None),     # EXEMPLO: tela cheia abre / fecha
]
# SFX sugeridos pelos agentes que você quer TIRAR (ex.: mais de 2 sons na mesma batida): {(tempo, arquivo)}.
DROP = set()                     # EXEMPLO 2, reel CLONE: {(24.36, "pop"), (31.653, "pop")}

# Duração (s) de cada arquivo da biblioteca de SFX (manifest.json da skill media-use). Só acrescente se usar outro arquivo.
SFX_LEN = {"click": 0.37, "glitch-1": 2.64, "impact-bass-1": 2.12, "impact-bass-2": 2.59, "key-press": 0.4,
           "notification": 2.46, "ping": 1.32, "pop": 0.72, "sparkle": 1.8, "typing": 1.5,
           "whoosh-short": 0.57, "whoosh": 0.57,
           "chime": 2.5, "click-soft": 0.37, "error": 1.62, "glitch-2": 3.5, "glitch-3": 3.1, "riser": 10.03,
           "whoosh-cinematic": 5.54}
# ===== FIM DO EDITE AQUI =====

# Trava contra valores de EXEMPLO esquecidos (não precisa mexer aqui): avisa e segue.
_EXEMPLOS = {"EYE_MEAN_Y": 0.466, "FULLS": [(19.233, 21.10)],
             "SCENES": [("s1-hook", 0.000, 5.567), ("s2-dinheiro", 5.567, 3.166), ("s3-quem-paga", 8.733, 3.167),
                        ("s4-launchpoint", 11.900, 7.700)],
             "PUNCH": [(1.74, 5.567), (8.08, 8.733), (10.32, 11.900), (18.60, 19.233)],
             "SFX": [(19.233, "whoosh", 0.14, None), (20.74, "whoosh-short", 0.12, None)]}
for _nome, _ex in _EXEMPLOS.items():
    if globals()[_nome] == _ex:
        print(f"AVISO: {_nome} ainda tem o valor de EXEMPLO do kit; troque pelo seu")

PUNCH = [(t, TOTAL if r is None else r) for t, r in PUNCH]
VID_TOP =round(FACE_Y - EYE_MEAN_Y * 1920, 1)   # base box: mean eye line sits on FACE_Y

# SFX: scene SFX come from the builders/reviewers (edit/sfx_from_review.json, global times on each visual peak);
# DROP thins out beats that stacked more than 2 sounds.
REVIEW = f"{P}/edit/sfx_from_review.json"
if os.path.exists(REVIEW):
    for t, f, v, d, _sid in json.load(open(REVIEW)):
        if (round(t, 3), f) not in DROP:
            SFX.append((round(t, 3), f, v, d))
else:
    print("AVISO: edit/sfx_from_review.json não existe (ainda): seguindo só com a lista SFX. "
          "Ele é gerado por tools/collect_sfx.py depois do workflow das cenas.")


def framing(e):
    """(x, y, scale) of #cam-frame so this piece's eyes land on (540-ish, FACE_Y) while still covering the frame."""
    s = SCALE[e["frame"]]
    ex, ey = e["eye_x"] * 1080, VID_TOP + e["eye_y"] * 1920
    dx = -(ex - 540) * s
    dx = max(540 - 540 * s, min(540 * s - 540, dx))
    dy = -(ey - FACE_Y) * s
    top = FACE_Y + (VID_TOP - FACE_Y) * s + dy
    bot = top + 1920 * s
    return round(dx, 1), round(dy, 1), s, top, bot


frames = []
for e in EDL:
    dx, dy, s, top, bot = framing(e)
    assert top <= 714 - 40 and bot >= 1494 + 40, \
        f"peça {e['id']}: o vídeo não cobre o painel da câmera (top={top:.0f}, bot={bot:.0f}); confira EYES e EYE_MEAN_Y"  # split panel always covered
    frames.append({"t": e["start"], "x": dx, "y": dy, "s": s, "top": top, "bot": bot})


def full_scale(a, b):
    """Smallest scale (around FACE_Y) that covers 0..1920 at FULL_Y for every piece shown in [a, b)."""
    need = 1.0
    for f, e in zip(frames, EDL):
        if e["start"] < b and e["start"] + e["duration"] > a:
            need = max(need, (1920 - FULL_Y - FACE_Y) / (f["bot"] - FACE_Y), (FACE_Y + FULL_Y) / (FACE_Y - f["top"]))
    return round(need + 0.02, 3)


FS = [full_scale(a, b) for a, b in FULLS]

auto = {"version": 1, "lanes": [{"target": "volume", "points": [
    {"t": 0, "v": 0}, {"t": 0.015, "v": 1}, {"t": round(TOTAL - 0.03, 3), "v": 1}, {"t": TOTAL, "v": 0}]}]}
video = (f'<video id="take" class="aroll" src="media/take.mp4" playsinline data-has-audio="true" '
         f'data-start="0" data-duration="{TOTAL}" data-media-start="0" data-track-index="0" '
         f'style="left:0px;top:{VID_TOP}px;width:1080px;height:1920px" '
         f"data-color-grading='{json.dumps(GRADE)}' data-automation='{json.dumps(auto)}'></video>")

hosts = []
for sid, st, du in SCENES:
    hosts.append(f'<div id="{sid}" class="scene" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                 f'data-start="{st}" data-duration="{du}" data-track-index="2" data-width="1080" data-height="1920"></div>')

_unknown = sorted({x[1] for x in SFX} - set(SFX_LEN))
assert not _unknown, f"SFX sem duração em SFX_LEN: {_unknown} (veja o manifest.json da skill media-use)"
audios, lane_end = [], {}
for n, (t, f, v, d) in enumerate(sorted(SFX)):
    dd = min(d, SFX_LEN[f]) if d else SFX_LEN[f]
    dd = min(dd, round(TOTAL - t, 3))
    lane = next(k for k in range(10, 40) if lane_end.get(k, -1) <= t - 0.01)
    lane_end[lane] = t + dd
    audios.append(f'<audio id="sfx-{n:02d}" src="assets/sfx/{f}.mp3" data-start="{t}" data-duration="{dd}" '
                  f'data-track-index="{lane}" data-volume="{v}"></audio>')

js_pieces = json.dumps([{"s": e["start"], "d": e["duration"]} for e in EDL])
js_frames = json.dumps([{k: f[k] for k in ("t", "x", "y", "s")} for f in frames])
GRAIN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' seed='7' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0'/></filter>"
         "<rect width='100%' height='100%' filter='url(%23n)'/></svg>")
CLIP_SPLIT = f"inset(0px 0px {1920 - CAM_H}px 0px)"
CLIP_FULL = "inset(0px 0px 0px 0px)"

full_js = []
for (a, b), fs in zip(FULLS, FS):
    full_js.append(f'''        tl.fromTo("#cam", {{ clipPath: "{CLIP_SPLIT}" }}, {{ clipPath: "{CLIP_FULL}", duration: {TR}, ease: "power3.inOut", immediateRender: false }}, {a});
        tl.fromTo("#cam-full", {{ y: {SPLIT_Y}, scale: 1 }}, {{ y: {FULL_Y}, scale: {fs}, duration: {TR}, ease: "power3.inOut", immediateRender: false }}, {a});
        tl.fromTo("#cam", {{ clipPath: "{CLIP_FULL}" }}, {{ clipPath: "{CLIP_SPLIT}", duration: {TR}, ease: "power3.inOut", immediateRender: false }}, {round(b - TR, 3)});
        tl.fromTo("#cam-full", {{ y: {FULL_Y}, scale: {fs} }}, {{ y: {SPLIT_Y}, scale: 1, duration: {TR}, ease: "power3.inOut", immediateRender: false }}, {round(b - TR, 3)});''')

doc = f'''<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #F3F3F0; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #F3F3F0; }}
      #paper {{ position: absolute; inset: 0; z-index: 0; background: #F3F3F0; overflow: hidden; }}
      #glow {{ position: absolute; left: -160px; top: 640px; width: 1400px; height: 1400px; border-radius: 50%;
        background: radial-gradient(closest-side, rgba(212, 255, 58, 0.34), rgba(212, 255, 58, 0.12) 52%, rgba(243, 243, 240, 0)); }}
      #grain {{ position: absolute; inset: 0; opacity: 0.06; background-image: url("{GRAIN}"); background-size: 220px 220px; }}
      .scene {{ z-index: 10; }}
      #cam {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; z-index: 20; overflow: hidden;
        clip-path: {CLIP_SPLIT}; background: #0d1114; }}
      #cam-full, #cam-move, #cam-drift, #cam-frame {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px {FACE_Y}px; }}
      .aroll {{ position: absolute; object-fit: cover; }}
      #captions {{ z-index: 30; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-fps="30" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="paper"><div id="glow"></div><div id="grain"></div></div>

      <!-- Stage scenes (bottom panel). Each is a full-frame transparent sub-composition. -->
      {chr(10).join("      " + h for h in hosts).strip()}

      <!-- Camera: the user's jump-cut take, one continuous clip; framing alternates A/B on every cut (edit/edl.json). -->
      <div id="cam"><div id="cam-full"><div id="cam-move"><div id="cam-drift"><div id="cam-frame">
        {video}
      </div></div></div></div></div>

      <div id="captions" data-track-kind="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-width="1080" data-height="1920"></div>

      <!-- SFX -->
      {chr(10).join("      " + a for a in audios).strip()}
    </div>
    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        const PIECES = {js_pieces};
        const FRAMES = {js_frames};
        const TOTAL = {TOTAL};
        tl.set("#cam-full", {{ y: {SPLIT_Y}, scale: 1 }}, 0);
        // per-piece framing, switched exactly on each cut (A 1.00x / B 1.10x, eyes on the same line)
        for (const f of FRAMES) tl.set("#cam-frame", {{ x: f.x, y: f.y, scale: f.s }}, f.t);
        // slow push inside every piece (a locked-off camera that still feels alive)
        for (const p of PIECES) {{
          tl.fromTo("#cam-drift", {{ scale: 1 }}, {{ scale: 1.03, duration: p.d, ease: "none", immediateRender: false }}, p.s);
        }}
        // keyword punch-ins (reset on the next cut)
        for (const [t, r] of {json.dumps(PUNCH)}) {{
          tl.fromTo("#cam-move", {{ scale: 1 }}, {{ scale: 1.05, duration: 0.32, ease: "power2.out", immediateRender: false }}, t - 0.08);
          tl.set("#cam-move", {{ scale: 1 }}, Math.min(r, TOTAL - 0.001));
        }}
        // full-screen camera windows ("e pensa comigo" / "tá, e como é que você pode fazer isso?")
{chr(10).join(full_js)}
        // ambient lime glow breathing behind the stage
        tl.fromTo("#glow", {{ scale: 0.9, x: 0 }}, {{ scale: 1.1, x: 40, duration: 6, ease: "sine.inOut", yoyo: true, repeat: Math.max(0, Math.floor(TOTAL / 6) - 1) }}, 0);
        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
'''
open(f"{P}/index.html", "w").write(doc)
print("index.html written; duration", TOTAL, "pieces", len(EDL), "sfx", len(audios), "full scales", FS)
for f, e in zip(frames, EDL):
    print(f'{e["id"]} {e["frame"]} t={f["t"]:6.2f} x={f["x"]:6.1f} y={f["y"]:6.1f} s={f["s"]} top={f["top"]:.0f} bot={f["bot"]:.0f}')
