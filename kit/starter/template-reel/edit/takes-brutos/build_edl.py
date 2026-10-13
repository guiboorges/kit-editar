"""Monta a decupagem (EDL) da câmera a partir das palavras alinhadas: corta as pausas e cola os pedaços na voz.

Pipeline : TAKES BRUTOS (vários arquivos de câmera, sem cortes). Copie este arquivo para <seu projeto>/edit/build_edl.py.
Entrada  : edit/words_source.json (align.py) + edit/audio/<clip>.wav (para medir a energia da voz nas bordas)
Saída    : edit/edl.json:   pedaços em ordem {id, seg, clip, src, media_start, start, duration, frame, edge_db, text}
           edit/words.json: cada palavra mantida, em segundos da TIMELINE {i, text, raw, start, end, seg, piece}
Regras   : corta toda pausa maior que MAX_GAP que tenha ≥ 0,16 s de silêncio real (abaixo de THRESH), a não ser que
           KEEP permita uma pausa maior; deixa PRE antes da 1ª palavra e POST depois da última de cada pedaço; as bordas
           andam pela energia da voz (o alinhamento termina as palavras cedo); tudo cai no grid de 30 fps.
Rodar    : python3 edit/build_edl.py
Confira  : no que ele imprime, edges=[entrada, saída] de cada pedaço deve ficar ≤ −40 dB (sem palavra comida, sem estalo).

(Build the A-roll EDL from aligned words: cut pauses, pad each piece, snap to the 30 fps grid.)
"""
import json, os, wave, struct, math

# ===== EDITE AQUI =====
FPS = 30                    # quadros por segundo do vídeo final
PRE, POST = 0.07, 0.11      # respiro (s) antes da 1ª palavra e depois da última de cada pedaço
TAIL = 0.47                 # ambiente extra (s) no último pedaço, para o CTA respirar (EXEMPLO 1, reel PERSONAGEM: 0.47)
MAX_GAP = 0.30              # pausas maiores que isso são cortadas (se tiverem silêncio real)
THRESH = -45.0              # dB: abaixo disso conta como silêncio; acima, a palavra ainda está soando

# Nome de cada take (o "clip" do segments.json) -> o proxy dele em media/.
CLIP_FILE = {"IMG_2873": "media/t1-hook.mp4", "IMG_2874": "media/t2-contexto.mp4",
             "IMG_2875": "media/t3-aha.mp4", "IMG_2883": "media/t4-prova.mp4"}   # EXEMPLO 1, reel PERSONAGEM (4 takes)

# Ordem da história e o que descartar: (label do segmento, índice da 1ª palavra mantida, índice da última; inclusive).
# None = até o fim do segmento. Use para escolher a melhor tentativa (ex.: começar na palavra 3 = 2ª tentativa).
# [] (vazio) = todos os segmentos inteiros, na ordem do segments.json.
ORDER = []
# EXEMPLO 1, reel PERSONAGEM:
#   ORDER = [("hook", 3, None),     # 2ª tentativa: "tem empresa pagando por vídeo…"
#            ("ctx-a", 0, None), ("ctx-b", 0, None), ("ctx-c", 0, None), ("aha", 0, None), ("prova", 0, None)]

# Pausas que ficam DE PROPÓSITO: (label do segmento, palavra ANTES da pausa) -> pausa máxima mantida (s).
# Palavra repetida no mesmo segmento: "eu#2" = a 2ª vez que "eu" aparece.
KEEP = {}
# EXEMPLO 1, reel PERSONAGEM:
#   KEEP = {("prova", "eu#2"): 0.30,          # "esse sou eu … e esse aqui é o personagem" (batida da revelação)
#           ("prova", "personagem#2"): 1.10,  # segura a revelação em tela dividida antes do CTA
#           ("prova", "aqui#2"): 0.26, ("prova", "CLONE"): 0.24}

# Como algumas palavras aparecem na legenda (o resto vira minúscula). Chave = a palavra em minúsculas.
DISPLAY = {"ia": "IA", "mcp": "MCP", "clone": "CLONE"}   # EXEMPLO: siglas + a palavra do CTA em MAIÚSCULAS
# ===== FIM DO EDITE AQUI =====

# Trava contra valores de EXEMPLO esquecidos (não precisa mexer aqui): avisa e segue.
_EXEMPLOS = {"CLIP_FILE": {"IMG_2873": "media/t1-hook.mp4", "IMG_2874": "media/t2-contexto.mp4",
                           "IMG_2875": "media/t3-aha.mp4", "IMG_2883": "media/t4-prova.mp4"},
             "DISPLAY": {"ia": "IA", "mcp": "MCP", "clone": "CLONE"}}
for _nome, _ex in _EXEMPLOS.items():
    if globals()[_nome] == _ex:
        print(f"AVISO: {_nome} ainda tem o valor de EXEMPLO do kit; troque pelo seu")

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def snap(t):
    return round(round(t * FPS) / FPS, 4)

def loud(clip, t):
    """True while the voice is audible at t or in the next 60 ms (ignores brief inter-syllable dips)."""
    return max(energy_db(clip, t + k * 0.02, 0.02) for k in range(4)) > THRESH

def silent_span(clip, a, b):
    """Seconds of genuinely quiet audio between a and b (10 ms frames under THRESH)."""
    n = 0; t = a
    while t < b:
        if energy_db(clip, t, 0.02) <= THRESH: n += 1
        t += 0.01
    return n * 0.01

def energy_db(clip, t, win=0.03):
    wf = wave.open(f"{P}/edit/audio/{clip}.wav"); sr = wf.getframerate()
    a = max(0, int((t - win / 2) * sr)); wf.setpos(a); raw = wf.readframes(int(win * sr))
    x = struct.unpack("<%dh" % (len(raw) // 2), raw)
    return 20 * math.log10(math.sqrt(sum(v * v for v in x) / max(1, len(x))) / 32768 + 1e-9)

words = json.load(open(f"{P}/edit/words_source.json"))
by_seg = {}
for w in words:
    by_seg.setdefault(w["seg"], []).append(w)
if not ORDER:
    ORDER = [(seg, 0, None) for seg in by_seg]
    print("AVISO: ORDER vazio: usando todos os segmentos inteiros, na ordem do segments.json:", list(by_seg))
_missing = [seg for seg, _, _ in ORDER if seg not in by_seg]
assert not _missing, f"ORDER cita segmentos que não existem no words_source.json: {_missing}; existem: {list(by_seg)}"
_noclip = sorted({w["clip"] for seg, _, _ in ORDER for w in by_seg[seg]} - set(CLIP_FILE))
assert not _noclip, f"take(s) sem arquivo em CLIP_FILE: {_noclip}"

pieces, kept = [], []
for seg, a, b in ORDER:
    ws = by_seg[seg][a:(b + 1 if b is not None else None)]
    # occurrence-tagged keys so KEEP can name a specific repeated word
    seen = {}
    for w in ws:
        k = w["text"]; seen[k] = seen.get(k, 0) + 1
        w["key"] = k if seen[k] == 1 else f"{k}#{seen[k]}"
    cur = [ws[0]]
    for prev, w in zip(ws, ws[1:]):
        gap = w["start"] - prev["end"]
        allow = KEEP.get((seg, prev["key"]), MAX_GAP)
        if gap > allow and silent_span(prev["clip"], prev["end"], w["start"]) >= 0.16:
            pieces.append((seg, cur)); cur = [w]
        else:
            cur.append(w)
    pieces.append((seg, cur))

edl, t = [], 0.0
for n, (seg, ws) in enumerate(pieces):
    clip = ws[0]["clip"]
    allw = by_seg[seg]; i0 = allw.index(ws[0]); i1 = allw.index(ws[-1])
    lo = allw[i0 - 1]["end"] + 0.03 if i0 > 0 else ws[0]["start"] - 0.30
    hi = allw[i1 + 1]["start"] - 0.03 if i1 < len(allw) - 1 else ws[-1]["end"] + 0.45
    # walk out from the aligned word edges while the voice is still audible (CTC edges run early)
    a = ws[0]["start"]
    while a - 0.01 > lo and loud(clip, a - 0.07): a -= 0.01
    b = ws[-1]["end"]
    while b + 0.01 < hi and loud(clip, b + 0.01): b += 0.01
    src_in = max(lo, a - PRE * 0.5)
    src_out = min(hi, b + POST * 0.5)
    if n == len(pieces) - 1: src_out += TAIL
    src_in, src_out = snap(src_in), snap(src_out)
    dur = snap(src_out - src_in)
    edl.append({"id": f"a{n:02d}", "seg": seg, "clip": clip, "src": CLIP_FILE[clip],
                "media_start": src_in, "start": snap(t), "duration": dur,
                "frame": "A" if n % 2 == 0 else "B",
                "edge_db": [round(energy_db(clip, src_in), 1), round(energy_db(clip, src_out), 1)],
                "text": " ".join(w["text"] for w in ws)})
    for w in ws:
        kept.append({"text": DISPLAY.get(w["text"].lower(), w["text"].lower()), "raw": w["text"],
                     "start": round(t + (w["start"] - src_in), 3), "end": round(t + (w["end"] - src_in), 3),
                     "seg": seg, "piece": f"a{n:02d}"})
    t += dur

for i, w in enumerate(kept):
    w["i"] = i
json.dump(edl, open(f"{P}/edit/edl.json", "w"), ensure_ascii=False, indent=1)
json.dump(kept, open(f"{P}/edit/words.json", "w"), ensure_ascii=False, indent=0)
print(f"{len(edl)} pieces, total {t:.2f}s")
for e in edl:
    print(f'{e["id"]} {e["seg"]:6} {e["frame"]} start={e["start"]:6.2f} dur={e["duration"]:5.2f} src={e["media_start"]:6.2f} edges={e["edge_db"]} | {e["text"]}')
