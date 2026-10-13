"""Gera compositions/captions.html: legenda karaokê na emenda (1–3 palavras por bloco, minúsculas, destaques lima).

Pipeline : TAKE CORTADO. Copie este arquivo para <seu projeto>/edit/build_captions.py.
Entrada  : edit/words.json (palavras na timeline, do build_edl.py) + o bloco EDITE AQUI
Saída    : compositions/captions.html. ATENÇÃO: rodar de novo APAGA qualquer ajuste feito à mão nesse arquivo.
Rodar    : python3 edit/build_captions.py
           Imprime cada bloco com início-fim, modo e as palavras em [destaque]. Leia a lista inteira em voz alta
           junto com o vídeo: os blocos devem quebrar onde a voz quebra.
Modos    : "broll" (branca com sombra, sobre o B-roll do gancho), "full" (branca em y 1540, quando a câmera está em
           tela cheia), "paper" (tinta escura sobre o papel claro).

(Generate compositions/captions.html: seam karaoke captions, 1–3 words per chunk, lowercase, lime keywords.)
"""
import json, os, html

# ===== EDITE AQUI =====
# Duração do vídeo em segundos. None = lê do edit/edl.json (recomendado: fica igual ao build_edl.py).
TOTAL = None

# Fim do B-roll do gancho: antes disso a legenda é branca (modo "broll") e some antes do B-roll sair.
# 0 = sem B-roll no gancho. EXEMPLO 2, reel CLONE: 5.50 (o B-roll da cena s1 some entre 5,28 e 5,54 s).
BROLL_END = 5.50

# Janelas de câmera em tela cheia (início, fim) em segundos. Tem que ser IGUAL ao FULLS do build_index.py.
FULLS = [(19.233, 21.10)]       # EXEMPLO: a 1ª das 2 telas cheias do exemplo 2 ("e pensa comigo…")
COLLAPSE = 0.36                 # duração da abertura/fechamento da tela cheia (igual ao TR do build_index.py)

# Blocos da legenda escritos à mão, em ordem, cobrindo TODAS as palavras do words.json (menos as de SKIP).
# Regras: 1 a 3 palavras (até 4 em expressões como "o passo a passo"), até ~18 caracteres, quebrar onde a voz quebra,
# evitar terminar em palavra fraca ("de / o / que / pra"). O script confere palavra por palavra com o áudio.
# [] (vazio) = blocos AUTOMÁTICOS (regras STOP/MAXW/MAXC abaixo): bom para começar. O script imprime a lista automática
# pronta para colar aqui e ajustar à mão (no exemplo 2 a versão automática deixou "e" e "eu" sozinhos e foi trocada).
CHUNK_TEXT = []
# EXEMPLO 2, reel CLONE (início da lista; a lista completa tinha 108 blocos):
#   CHUNK_TEXT = ["com toda", "a certeza", "você já viu", "esse tipo", "de personagem", "na internet", "e você",
#                 "se pergunta", "tá mas", "por que", "as pessoas", "estão fazendo isso", ...]

# Destaques lima: o INÍCIO (start) de cada palavra a destacar, copiado do edit/words.json (tolerância 0,03 s).
# Mire em ≈ 1 destaque a cada 3 s (gancho, número, marca, prova, CTA). [] = nenhum destaque.
HL_AT = []
# EXEMPLO 2, reel CLONE: HL_AT = [1.74, 7.68, 8.08, 10.32, 13.98, ...]  ("personagem", "muito dinheiro", "pagaria", ...)

# Regras do chunker automático (só valem quando CHUNK_TEXT = []):
STOP = {"de", "a", "o", "e", "que", "por", "pra", "pro", "um", "uma", "no", "na", "do", "da", "em", "é", "eu", "ela",
        "isso", "se", "ao", "esse", "meu", "como", "os", "seus", "as", "com", "te", "vou", "até", "mas", "são", "tá"}
MAXW, MAXC = 3, 18              # no máximo 3 palavras e 18 caracteres por bloco
# ===== FIM DO EDITE AQUI =====

# Trava contra valores de EXEMPLO esquecidos (não precisa mexer aqui): avisa e segue.
_EXEMPLOS = {"BROLL_END": 5.50, "FULLS": [(19.233, 21.10)]}
for _nome, _ex in _EXEMPLOS.items():
    if globals()[_nome] == _ex:
        print(f"AVISO: {_nome} ainda tem o valor de EXEMPLO do kit; troque pelo seu")

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = [w for w in json.load(open(f"{P}/edit/words.json")) if not w["skip"]]
if TOTAL is None:
    _edl = json.load(open(f"{P}/edit/edl.json"))
    TOTAL = round(_edl[-1]["start"] + _edl[-1]["duration"], 3)


def mode_at(t):
    if t < BROLL_END: return "broll"
    for a, b in FULLS:
        if a <= t < b - COLLAPSE + 0.1: return "full"
    return "paper"


def auto_chunks(ws):
    """Greedy: ≤MAXW words, ≤MAXC chars, break on pauses/pieces; never end a chunk on a stop word."""
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


if CHUNK_TEXT:
    # Hand-cut chunks, in order (1–3 words, ≤ ~18 chars, break where the voice breaks, never end on a stop word).
    chunks, k = [], 0
    for txt in CHUNK_TEXT:
        n = len(txt.split())
        got = " ".join(w["text"] for w in W[k:k + n])
        assert got == txt, f"CHUNK_TEXT não bate com o áudio: bloco {txt!r}, mas as palavras ali são {got!r} (palavra nº {k})"
        chunks.append(W[k:k + n]); k += n
    assert k == len(W), f"CHUNK_TEXT cobre {k} palavras, mas a legenda tem {len(W)}: faltam blocos no fim"
else:
    chunks = auto_chunks(W)
    print("AVISO: CHUNK_TEXT vazio: blocos automáticos. Para ajustar à mão, cole esta lista em CHUNK_TEXT e edite:")
    print("CHUNK_TEXT = " + json.dumps([" ".join(w["text"] for w in ch) for ch in chunks], ensure_ascii=False))
BYI = {w["i"]: w for w in W}

# keyword highlights (lime block) — by the word's start time (exact occurrences)
hl = set()
for t in HL_AT:
    w = min(W, key=lambda x: abs(x["start"] - t))
    assert abs(w["start"] - t) < 0.03, f"HL_AT {t}: nenhuma palavra começa aí (a mais perto é {w['text']!r} em {w['start']})"
    hl.add(w["i"])
if not HL_AT:
    print("AVISO: HL_AT vazio: nenhum destaque lima. Copie o start das palavras-chave do edit/words.json para HL_AT.")

rows, js = [], []
for ci, ch in enumerate(chunks):
    s = ch[0]["start"]; e_last = ch[-1]["end"]
    nxt = chunks[ci + 1][0]["start"] if ci + 1 < len(chunks) else TOTAL
    # hide at next chunk start; if a long silence follows, fade out ~0.45s after the last word
    hide = min(nxt, max(e_last + 0.45, s + 0.5))
    hide = min(hide, TOTAL - 0.04)
    m = mode_at(s)
    if m == "broll": hide = min(hide, BROLL_END)
    for a, b in FULLS:
        if m == "full" and a <= s < b: hide = min(hide, b - 0.22)            # camera edge passes y≈1540
        if m == "paper" and b - COLLAPSE - 0.1 <= s < b: s = b - 0.04          # wait until the seam is uncovered
        if m == "paper" and s < a <= hide: hide = min(hide, a + 0.02)          # camera starts covering the seam
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
    print("AVISO: bloco(s) que somem antes de aparecer (nº, início, fim): ajuste FULLS/BROLL_END "
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
    ws = " ".join(("[" + BYI[w["i"]]["text"] + "]") if w["hl"] else BYI[w["i"]]["text"] for w in c["w"])
    print(f'{c["s"]:6.2f}-{c["h"]:6.2f} {c["m"]:5} | {ws}')
print(len(js), "chunks")
