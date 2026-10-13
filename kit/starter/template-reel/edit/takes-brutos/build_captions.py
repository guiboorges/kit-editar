"""Gera compositions/captions.html: legenda karaokê na emenda (1–3 palavras por bloco, minúsculas, destaques lima).

Pipeline : TAKES BRUTOS. Copie este arquivo para <seu projeto>/edit/build_captions.py.
Entrada  : edit/words.json (palavras na timeline, do build_edl.py) + o bloco EDITE AQUI
Saída    : compositions/captions.html. ATENÇÃO: rodar de novo APAGA qualquer ajuste feito à mão nesse arquivo.
Rodar    : python3 edit/build_captions.py
           Imprime cada bloco com início-fim, modo e as palavras em [destaque]. Leia a lista inteira junto com o
           vídeo: os blocos devem quebrar onde a voz quebra.
Modos    : "broll" (branca com sombra, sobre o B-roll do gancho), "full" (branca em y 1540, quando a câmera está em
           tela cheia), "paper" (tinta escura sobre o papel claro).

(Generate compositions/captions.html: seam karaoke captions, 1–3 words per chunk, lowercase, lime keywords.)
"""
import json, os, html

# ===== EDITE AQUI =====
# Duração do vídeo em segundos. None = lê do edit/edl.json (recomendado). EXEMPLO 1, reel PERSONAGEM: 47.9
TOTAL = None

# Blocos da legenda: quantas palavras tem cada bloco, em ordem (a soma tem que dar o total de palavras do words.json).
# Quebre onde a voz quebra; nunca termine bloco em "de / o / que / e / por".
# [] (vazio) = blocos AUTOMÁTICOS (regras STOP/MAXW/MAXC abaixo). O script imprime a lista automática pronta para colar.
CHUNKS = []
# EXEMPLO 1, reel PERSONAGEM (56 blocos, comentado por trecho):
#   CHUNKS = [3, 2, 2, 3, 3, 4,          # hook
#             4, 3, 2, 4, 4, 4,          # launchpoint
#             ...]

# Destaques lima: sequências de palavras a destacar (minúsculas/maiúsculas tanto faz). Destaca TODAS as ocorrências;
# use HL_JANELA para manter só algumas. Mire em ≈ 1 destaque a cada 3 s (gancho, número, marca, prova, CTA).
HL = [("IA",), ("CLONE",)]             # EXEMPLO; o exemplo 1 tinha 13, ex.: ("nem", "existe"), ("mil", "dólares")
# Para palavras repetidas: destacar só quando o início da palavra está entre (desde, até) segundos. None = sem limite.
HL_JANELA = {}                         # EXEMPLO 1, reel PERSONAGEM: {"personagem": (40, None), "ia": (None, 30)}

# Fim do B-roll do gancho (antes disso a legenda é branca) e o limite para ela sumir antes de o B-roll sair.
BROLL_END, BROLL_HIDE = 4.67, 4.60     # EXEMPLO 1, reel PERSONAGEM (B-roll some entre 4,40 e 4,66 s). 0, 0 = sem B-roll
# Janela de câmera em tela cheia (início, fim): tem que ser IGUAL ao FULL do build_index.py. A legenda some em FULL_HIDE,
# antes de a câmera fechar.
FULL = (21.03, 22.03)                  # EXEMPLO 1, reel PERSONAGEM ("e pensa comigo")
FULL_HIDE = 21.90                      # EXEMPLO: a câmera fecha entre 21,68 e 22,03

# Regras do chunker automático (só valem quando CHUNKS = []):
STOP = {"de", "a", "o", "e", "que", "por", "pra", "um", "uma", "no", "do", "em", "é", "eu", "ela", "isso", "se", "ao", "esse", "meu", "como"}
MAXW, MAXC = 3, 17                     # no máximo 3 palavras e 17 caracteres por bloco
# ===== FIM DO EDITE AQUI =====

# Trava contra valores de EXEMPLO esquecidos (não precisa mexer aqui): avisa e segue.
_EXEMPLOS = {"HL": [("IA",), ("CLONE",)], "BROLL_END": 4.67, "BROLL_HIDE": 4.60, "FULL": (21.03, 22.03),
             "FULL_HIDE": 21.90}
for _nome, _ex in _EXEMPLOS.items():
    if globals()[_nome] == _ex:
        print(f"AVISO: {_nome} ainda tem o valor de EXEMPLO do kit; troque pelo seu")

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = json.load(open(f"{P}/edit/words.json"))
if TOTAL is None:
    _edl = json.load(open(f"{P}/edit/edl.json"))
    TOTAL = round(_edl[-1]["start"] + _edl[-1]["duration"], 3)

def auto_chunks(ws):
    """Greedy: ≤3 words, ≤17 chars, break on pauses/pieces; never end a chunk on a stop word."""
    out, cur = [], []
    for i, w in enumerate(ws):
        if cur:
            prev = cur[-1]
            gap = w["start"] - prev["end"]
            text = " ".join(x["text"] for x in cur + [w])
            brk = gap > 0.28 or w["piece"] != prev["piece"] or len(cur) >= MAXW or len(text) > MAXC
            if brk and prev["text"].lower() in STOP and len(cur) > 1:
                carry = cur.pop(); out.append(cur); cur = [carry]
                if len(cur) >= MAXW or len(" ".join(x["text"] for x in cur + [w])) > MAXC:
                    out.append(cur); cur = []
            elif brk:
                out.append(cur); cur = []
        cur.append(w)
    if cur: out.append(cur)
    return out

if CHUNKS:
    assert sum(CHUNKS) == len(W), f"CHUNKS soma {sum(CHUNKS)} palavras, mas o words.json tem {len(W)}"
    chunks, k = [], 0
    for n in CHUNKS:
        chunks.append(W[k:k + n]); k += n
else:
    chunks = auto_chunks(W)
    print("AVISO: CHUNKS vazio: blocos automáticos. Para ajustar à mão, cole esta lista em CHUNKS e edite:")
    print("CHUNKS = " + json.dumps([len(ch) for ch in chunks]))

# keyword highlights (lime block): word indices by matching consecutive text in a segment
hl = set()
texts = [w["text"] for w in W]
for pat in HL:
    n = len(pat)
    for i in range(len(texts) - n + 1):
        if tuple(t.lower() for t in texts[i:i + n]) == tuple(p.lower() for p in pat):
            hl.update(range(i, i + n))
# keep it sparse: a repeated word is highlighted only inside its HL_JANELA window
for i, w in enumerate(W):
    t = w["text"].lower()
    if t in HL_JANELA:
        desde, ate = HL_JANELA[t]
        if desde is not None and w["start"] < desde: hl.discard(i)
        if ate is not None and w["start"] > ate: hl.discard(i)

def mode_at(t):
    if t < BROLL_END: return "broll"
    if FULL[0] <= t < FULL[1]: return "full"
    return "paper"

rows, js = [], []
for ci, ch in enumerate(chunks):
    s = ch[0]["start"]; e_last = ch[-1]["end"]
    nxt = chunks[ci + 1][0]["start"] if ci + 1 < len(chunks) else TOTAL
    # hide at next chunk start; if a long silence follows, fade out ~0.45s after the last word
    hide = min(nxt, max(e_last + 0.45, s + 0.5))
    hide = min(hide, TOTAL - 0.04)
    m = mode_at(s)
    if m == "broll": hide = min(hide, BROLL_HIDE)   # B-roll fades out; white text must leave before the paper shows
    if m == "full": hide = min(hide, FULL_HIDE)     # camera collapses back to the split
    spans = []
    for w in ch:
        cls = "w hl" if w["i"] in hl else "w"
        inner = f'<span class="t">{html.escape(w["text"])}</span>'
        if w["i"] in hl: inner = f'<span class="bg"></span>{inner}'
        spans.append(f'<span class="{cls}" id="cap-w{w["i"]}">{inner}</span>')
    rows.append(f'<div class="ch {m}" id="cap-c{ci}">{" ".join(spans)}</div>')
    js.append({"c": ci, "s": round(s, 3), "h": round(hide, 3), "m": m,
               "w": [{"i": w["i"], "s": round(w["start"], 3), "hl": w["i"] in hl} for w in ch]})
_bad = [(c["c"], c["s"], c["h"]) for c in js if c["h"] <= c["s"]]
if _bad:
    print("AVISO: bloco(s) que somem antes de aparecer (nº, início, fim): ajuste FULL/FULL_HIDE/BROLL_END/BROLL_HIDE "
          "ou os blocos perto das trocas de modo:", _bad)

doc = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8" /></head><body>
<template>
  <style>
    @font-face {{ font-family: "Geist"; src: url("assets/fonts/Geist-latin.woff2") format("woff2"); font-weight: 100 900; font-display: block; }}
    #captions-root {{ position: absolute; inset: 0; overflow: hidden; font-family: "Geist", sans-serif;
      --ink: #111113; --lime: #D4FF3A; --limeInk: #141A00; }}
    #captions-root .ch {{ position: absolute; left: 60px; right: 60px; top: 812px; height: 96px; display: flex; align-items: center;
      justify-content: center; gap: 0 18px; flex-wrap: nowrap; opacity: 0; will-change: transform, opacity, filter; }}
    #captions-root .ch.full {{ top: 1540px; }}
    #captions-root .w {{ position: relative; display: inline-block; font-size: 66px; font-weight: 600; letter-spacing: -0.028em;
      line-height: 1; white-space: nowrap; color: var(--ink); }}
    #captions-root .ch.broll .w, #captions-root .ch.full .w {{ color: #FFFFFF; text-shadow: 0 2px 18px rgba(0,0,0,.55), 0 1px 3px rgba(0,0,0,.4); }}
    #captions-root .ch.full .w {{ font-size: 74px; }}
    #captions-root .w .t {{ position: relative; display: inline-block; }}
    #captions-root .w.hl .bg {{ position: absolute; left: -12px; right: -12px; top: -6px; bottom: -10px; border-radius: 14px;
      background: var(--lime); transform-origin: 0 50%; transform: scaleX(0); }}
  </style>
  <div id="captions-root" data-composition-id="captions" data-width="1080" data-height="1920">
    {"".join(rows)}
  </div>
  <script>
    (function () {{
      const R = document.getElementById("captions-root");
      const C = {json.dumps(js, ensure_ascii=False)};
      const tl = gsap.timeline({{ paused: true }});
      for (const c of C) {{
        const el = R.querySelector("#cap-c" + c.c);
        tl.fromTo(el, {{ opacity: 0, y: 16, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.14, ease: "power2.out" }}, Math.max(0, c.s - 0.03));
        tl.to(el, {{ opacity: 0, duration: 0.05, ease: "none" }}, c.h - 0.08);
        for (const w of c.w) {{
          const we = R.querySelector("#cap-w" + w.i);
          const t = we.querySelector(".t");
          if (w.s > c.s + 0.02) tl.fromTo(t, {{ opacity: 0.42 }}, {{ opacity: 1, duration: 0.08, ease: "none" }}, w.s - 0.03);
          if (w.hl) {{
            tl.fromTo(we.querySelector(".bg"), {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.2, ease: "power3.out" }}, w.s - 0.05);
            tl.fromTo(we, {{ color: c.m === "paper" ? "#111113" : "#FFFFFF", textShadow: c.m === "paper" ? "none" : "0 2px 18px rgba(0,0,0,.55)" }},
              {{ color: "#141A00", textShadow: "0 0 0 rgba(0,0,0,0)", duration: 0.12, ease: "none" }}, w.s - 0.02);
            tl.fromTo(we, {{ scale: 1 }}, {{ scale: 1.06, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }}, w.s - 0.03);
          }}
        }}
      }}
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
</body></html>
'''
os.makedirs(f"{P}/compositions", exist_ok=True)
open(f"{P}/compositions/captions.html", "w").write(doc)
for c in js:
    ws = " ".join(("[" + W[w["i"]]["text"] + "]") if w["hl"] else W[w["i"]]["text"] for w in c["w"])
    print(f'{c["s"]:6.2f}-{c["h"]:6.2f} {c["m"]:5} | {ws}')
print(len(js), "chunks")
