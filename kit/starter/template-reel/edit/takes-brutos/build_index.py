"""Gera index.html, a composição raiz do vídeo (câmera, cenas, legenda, SFX).

Pipeline : TAKES BRUTOS. Copie este arquivo para <seu projeto>/edit/build_index.py.
Entrada  : edit/edl.json (build_edl.py) + o bloco EDITE AQUI + edit/sfx_from_review.json (opcional, ver abaixo)
Saída    : index.html. ATENÇÃO: rodar de novo APAGA qualquer ajuste feito à mão (ou no app) no index.html.
Rodar    : python3 edit/build_index.py   (rode de novo depois do workflow das cenas, para entrar com os SFX)
Confira  : npx --yes hyperframes@0.8.141 snapshot --at <tempos logo depois de cada corte e da tela cheia> --no-end -o snapshots/cam-check
           olhos na mesma altura em todos os cortes, nenhum topo de cabeça cortado no plano A.

Camadas (z): papel + brilho lima (0) · cenas/sub-composições (10) · câmera no painel de cima (20) · legenda (30)
Câmera   : cada pedaço da EDL é um <video> sobre media/t*.mp4, enquadrado A (1,0×) ou B (1,10×) em volta do rosto; a caixa
           #cam recorta o painel de cima (0–780) e abre em tela cheia na janela FULL.
Áudio    : a voz vem em cada vídeo (fade de 15 ms em cada corte, sem estalo); SFX são <audio> na raiz. Os arquivos de SFX NÃO
           vêm no kit: copie-os de ~/.claude/skills/media-use/audio/assets/sfx/ (instalados junto com as skills do
           HyperFrames) para assets/sfx/.
Novidade : em relação ao template original, este script também lê edit/sfx_from_review.json (os SFX que os revisores
           do workflow devolveram, juntados pelo tools/collect_sfx.py), se o arquivo existir.
"""
import json, os

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDL = json.load(open(f"{P}/edit/edl.json"))
TOTAL = round(EDL[-1]["start"] + EDL[-1]["duration"], 3)   # duração do vídeo (do build_edl.py); pode usar TOTAL abaixo

# ===== EDITE AQUI =====
# Formato da tela (zonas do padrão). Só mude se mudar o formato inteiro do reel.
CAM_H = 780                      # altura do painel da câmera (tela dividida)
FACE_Y = 1034                    # linha dos olhos no espaço da câmera (quadro inteiro) -> y≈320 do painel
SPLIT_Y = -714                   # deslocamento da câmera na tela dividida

# Janela de câmera em tela cheia (início, fim), numa frase de conversa direta. Igual ao FULL do build_captions.py.
FULL = (21.03, 22.03)            # EXEMPLO 1, reel PERSONAGEM ("e pensa comigo")

# Rosto de cada take: (x do centro do rosto, y da linha dos olhos), em fração do quadro, medidos em still com grade
# (ou com o tools/face.swift: média de eyeX/eyeY). Uma entrada por arquivo do CLIP_FILE do build_edl.py.
FACE = {"media/t1-hook.mp4": (0.486, 0.578), "media/t2-contexto.mp4": (0.467, 0.586),
        "media/t3-aha.mp4": (0.50, 0.586), "media/t4-prova.mp4": (0.41, 0.534)}   # EXEMPLO 1, reel PERSONAGEM
SCALE = {"A": 1.0, "B": 1.10}    # tamanho dos dois planos que alternam a cada corte

# Grade de cor. "Natural Portrait" do padrão; iPhone já é Rec.709, sem LUT.
GRADE = {"preset": "skin-soft", "intensity": 0.58,
         "adjust": {"contrast": 0.05, "highlights": -0.08, "shadows": 0.06, "vibrance": 0.03},
         "details": {"vignette": 0.03}}

# Cenas: (id, início global em s, duração em s). Vêm da tabela do STORYBOARD.md; o arquivo é compositions/<id>.html.
SCENES = [("s1-hook", 0.00, 4.67), ("s2-launchpoint", 4.67, 6.53), ("s3-calc", 11.20, 4.93)]   # EXEMPLO (exemplo 1: 8)

# Punch-ins de 1,05× na câmera: (início da palavra-chave no words.json, reset = início do próximo pedaço da EDL).
# No último punch-in, se ele vai até o fim do vídeo, use TOTAL (ou None) como reset.
PUNCH = [(2.05, 4.67), (6.89, 7.53)]                 # EXEMPLO 1, reel PERSONAGEM (lá eram 6; o último era (45.30, TOTAL))

# SFX fixos: (tempo, arquivo sem .mp3, volume, duração ou None). Os SFX das cenas podem vir do
# edit/sfx_from_review.json (abaixo); aqui ficam os seus ajustes e os da câmera (tela cheia: whoosh / whoosh-short).
SFX = [
    (0.00, "impact-bass-1", 0.1, 1.2),               # abertura do vídeo (regra do padrão)
    (21.03, "whoosh", 0.14, None), (21.68, "whoosh-short", 0.12, None),   # EXEMPLO: tela cheia abre / fecha
]
# SFX sugeridos pelos agentes que você quer TIRAR (ex.: mais de 2 sons na mesma batida): {(tempo, arquivo)}.
DROP = set()

# Duração (s) de cada arquivo da biblioteca de SFX (manifest.json da skill media-use). Só acrescente se usar outro arquivo.
SFX_LEN = {"click": 0.37, "glitch-1": 2.64, "impact-bass-1": 2.12, "impact-bass-2": 2.59, "key-press": 0.4,
           "notification": 2.46, "ping": 1.32, "pop": 0.72, "sparkle": 1.8, "typing": 1.5,
           "whoosh-short": 0.57, "whoosh": 0.57,
           "chime": 2.5, "click-soft": 0.37, "error": 1.62, "glitch-2": 3.5, "glitch-3": 3.1, "riser": 10.03,
           "whoosh-cinematic": 5.54}
# ===== FIM DO EDITE AQUI =====

# Trava contra valores de EXEMPLO esquecidos (não precisa mexer aqui): avisa e segue.
_EXEMPLOS = {"FULL": (21.03, 22.03),
             "FACE": {"media/t1-hook.mp4": (0.486, 0.578), "media/t2-contexto.mp4": (0.467, 0.586),
                      "media/t3-aha.mp4": (0.50, 0.586), "media/t4-prova.mp4": (0.41, 0.534)},
             "SCENES": [("s1-hook", 0.00, 4.67), ("s2-launchpoint", 4.67, 6.53), ("s3-calc", 11.20, 4.93)],
             "PUNCH": [(2.05, 4.67), (6.89, 7.53)],
             "SFX": [(0.00, "impact-bass-1", 0.1, 1.2), (21.03, "whoosh", 0.14, None), (21.68, "whoosh-short", 0.12, None)]}
for _nome, _ex in _EXEMPLOS.items():
    if globals()[_nome] == _ex:
        print(f"AVISO: {_nome} ainda tem o valor de EXEMPLO do kit; troque pelo seu")

PUNCH = [(t, TOTAL if r is None else r) for t, r in PUNCH]

REVIEW =f"{P}/edit/sfx_from_review.json"
if os.path.exists(REVIEW):
    for t, f, v, d, _sid in json.load(open(REVIEW)):
        if (round(t, 3), f) not in DROP:
            SFX.append((round(t, 3), f, v, d))
    SFX = sorted(SFX)
else:
    print("AVISO: edit/sfx_from_review.json não existe (ainda): seguindo só com a lista SFX. "
          "Ele é gerado por tools/collect_sfx.py depois do workflow das cenas.")
_unknown = sorted({x[1] for x in SFX} - set(SFX_LEN))
assert not _unknown, f"SFX sem duração em SFX_LEN: {_unknown} (veja o manifest.json da skill media-use)"
_noface = sorted({e["src"] for e in EDL} - set(FACE))
assert not _noface, f"take(s) sem medida de rosto em FACE: {_noface}"


def frame_rect(src, frame):
    fx, fy = FACE[src]; s = SCALE[frame]
    w, h = 1080 * s, 1920 * s
    left = min(0.0, max(1080 - w, 540 - fx * w))
    top = FACE_Y - fy * h
    top = min(714.0, max(1494 - h, top))
    return round(left, 1), round(top, 1), round(w, 1), round(h, 1)


videos = []
for e in EDL:
    frame = e["frame"]
    if FULL[0] <= e["start"] < FULL[1]:
        frame = "A"                                   # full-screen piece must cover the whole frame
    l, t, w, h = frame_rect(e["src"], frame)
    if FULL[0] <= e["start"] < FULL[1]:
        t = 0.0
    d = e["duration"]
    auto = {"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0, "v": 0}, {"t": 0.015, "v": 1}, {"t": round(d - 0.015, 3), "v": 1}, {"t": d, "v": 0}]}]}
    videos.append(
        f'<video id="{e["id"]}" class="aroll" src="{e["src"]}" playsinline data-has-audio="true" '
        f'data-start="{e["start"]}" data-duration="{d}" data-media-start="{e["media_start"]}" data-track-index="{0 if int(e["id"][1:]) % 2 == 0 else 1}" '
        f'style="left:{l}px;top:{t}px;width:{w}px;height:{h}px" '
        f"data-color-grading='{json.dumps(GRADE)}' data-automation='{json.dumps(auto)}'></video>")

hosts = []
for i, (sid, st, du) in enumerate(SCENES):
    hosts.append(f'<div id="{sid}" class="scene" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                 f'data-start="{st}" data-duration="{du}" data-track-index="2" data-width="1080" data-height="1920"></div>')

audios, lane_end = [], {}
for n, (t, f, v, d) in enumerate(SFX):
    dd = d if d else SFX_LEN[f]
    dd = min(dd, round(TOTAL - t, 3))
    lane = next(k for k in range(10, 40) if lane_end.get(k, -1) <= t - 0.01)
    lane_end[lane] = t + dd
    audios.append(f'<audio id="sfx-{n:02d}" src="assets/sfx/{f}.mp3" data-start="{t}" data-duration="{dd}" '
                  f'data-track-index="{lane}" data-volume="{v}"></audio>')

js_pieces = json.dumps([{"s": e["start"], "d": e["duration"]} for e in EDL])
GRAIN = ("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' seed='7' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0'/></filter>"
         "<rect width='100%' height='100%' filter='url(%23n)'/></svg>")

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
        clip-path: inset(0px 0px {1920 - CAM_H}px 0px); background: #1b1a18; }}
      #cam-move, #cam-drift {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 540px {FACE_Y}px; }}
      .aroll {{ position: absolute; object-fit: cover; }}
      #captions {{ z-index: 30; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-fps="30" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="paper"><div id="glow"></div><div id="grain"></div></div>

      <!-- Stage scenes (bottom panel). Each is a full-frame transparent sub-composition. -->
      {chr(10).join("      " + h for h in hosts).strip()}

      <!-- Camera: best takes cut on the voice (edit/edl.json), framed A/B, clipped to the top panel. -->
      <div id="cam"><div id="cam-move"><div id="cam-drift">
        {chr(10).join("        " + v for v in videos).strip()}
      </div></div></div>

      <div id="captions" data-track-kind="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-width="1080" data-height="1920"></div>

      <!-- SFX -->
      {chr(10).join("      " + a for a in audios).strip()}
    </div>
    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        const PIECES = {js_pieces};
        const TOTAL = {TOTAL};
        // split framing + per-piece slow push (life on a locked-off camera)
        tl.set("#cam-move", {{ y: {SPLIT_Y}, scale: 1 }}, 0);
        for (const p of PIECES) {{
          tl.fromTo("#cam-drift", {{ scale: 1 }}, {{ scale: 1.03, duration: p.d, ease: "none", immediateRender: false }}, p.s);
        }}
        // keyword punch-ins (reset on the next cut)
        for (const [t, r] of {json.dumps(PUNCH)}) {{
          tl.fromTo("#cam-move", {{ scale: 1 }}, {{ scale: 1.05, duration: 0.32, ease: "power2.out", immediateRender: false }}, t - 0.08);
          tl.set("#cam-move", {{ scale: 1 }}, Math.min(r, TOTAL - 0.001));
        }}
        // full-screen camera on "e pensa comigo"
        tl.fromTo("#cam", {{ clipPath: "inset(0px 0px {1920 - CAM_H}px 0px)" }}, {{ clipPath: "inset(0px 0px 0px 0px)", duration: 0.36, ease: "power3.inOut", immediateRender: false }}, {FULL[0]});
        tl.fromTo("#cam-move", {{ y: {SPLIT_Y} }}, {{ y: 0, duration: 0.36, ease: "power3.inOut", immediateRender: false }}, {FULL[0]});
        tl.fromTo("#cam", {{ clipPath: "inset(0px 0px 0px 0px)" }}, {{ clipPath: "inset(0px 0px {1920 - CAM_H}px 0px)", duration: 0.34, ease: "power3.inOut", immediateRender: false }}, {FULL[1]} - 0.36);
        tl.fromTo("#cam-move", {{ y: 0 }}, {{ y: {SPLIT_Y}, duration: 0.34, ease: "power3.inOut", immediateRender: false }}, {FULL[1]} - 0.36);
        // ambient lime glow breathing behind the stage
        tl.fromTo("#glow", {{ scale: 0.9, x: 0 }}, {{ scale: 1.1, x: 40, duration: 6, ease: "sine.inOut", yoyo: true, repeat: Math.max(0, Math.floor(TOTAL / 6) - 1) }}, 0);
        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
'''
open(f"{P}/index.html", "w").write(doc)
print("index.html written; duration", TOTAL, "videos", len(videos), "sfx", len(audios))
