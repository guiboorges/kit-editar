"""Peças da câmera (enquadramento A/B) para um take que JÁ CHEGA CORTADO (o vídeo que você mesmo exportou com jump cuts).

Pipeline : TAKE CORTADO. Copie este arquivo para <seu projeto>/edit/build_edl.py.
Ideia    : a timeline é o seu arquivo 1:1 (nenhuma pausa é removida: a fala é contínua e os seus cortes ficam).
           Cada peça = o trecho entre dois dos seus cortes. As peças alternam o enquadramento A (1,00×) / B (1,10×),
           então cada jump cut que já existe vira também uma troca de tamanho de plano (o olho lê como edição
           intencional, não como erro). "Zoom cuts" (ZOOM) criam trocas extras dentro de trechos longos.
Entrada  : edit/words_source.json (do align.py) + as constantes do bloco EDITE AQUI
Saída    : edit/edl.json:   peças {id, start, duration, frame, eye_x, eye_y, zoomcut, text}
           edit/words.json: palavras na timeline {i, text, raw, start, end, piece, skip}
Rodar    : python3 edit/build_edl.py
           Ele imprime cada peça com o texto falado nela: confira se cada corte cai numa fronteira de frase.
Atenção  : este script NÃO roda o tools/cuts.py nem o face.swift. Os valores de CUTS, ZOOM e EYES são colados à mão
           abaixo, depois de conferir os candidatos no olho.

(Build the A-roll piece list for a take that ARRIVES ALREADY CUT. Timeline = source 1:1; pieces alternate A/B.)
"""
import json, os, subprocess

# ===== EDITE AQUI =====
FPS = 30                # quadros por segundo do vídeo final (o padrão é 30; só mude se mudar o proxy também)

# Duração do take ORIGINAL (o arquivo que você exportou), em segundos. Meça com:
#   ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "materiais/bruto/<seu vídeo>"
# None = mede sozinho no proxy (duração de media/take.mp4 − 0,27 s de cauda), com aviso.
# EXEMPLO 2, reel CLONE: 65.433
TOTAL = None

# Os SEUS cortes, em segundos (exatos no quadro: quadro ÷ 30). Vêm do tools/cuts.py, que lista CANDIDATOS:
# confira cada par "quadro antes / quadro depois" no olho e cole aqui só os cortes de verdade (gesto de mão não conta).
CUTS = [5.567, 8.733, 11.900, 16.133, 19.233]   # EXEMPLO: os 5 primeiros dos 16 cortes do exemplo 2

# "Zoom cuts": trocas extras de enquadramento DENTRO de trechos longos, num respiro da fala (mesmo take, outro plano).
ZOOM = []                                       # [] = nenhum. EXEMPLO 2, reel CLONE: [24.100, 51.400]

# Olhos de cada trecho entre cortes (eyeX, eyeY em fração do quadro: 0 = topo/esquerda, 1 = base/direita).
# Precisa ter len(CUTS) + 1 itens, na ordem. Vêm do tools/face.swift: 3 quadros por trecho (a 20%, 50% e 80% dele)
# e a média dos 3. As peças de ZOOM herdam a medida do trecho onde estão.
EYES = [(0.454, 0.460), (0.433, 0.468), (0.444, 0.470), (0.434, 0.467), (0.445, 0.467),
        (0.469, 0.468)]                         # EXEMPLO: as 6 primeiras medidas do exemplo 2

# Como algumas palavras aparecem na legenda (o resto vira minúscula). Chave = a palavra em minúsculas.
DISPLAY = {"ia": "IA", "mcp": "MCP", "clone": "CLONE"}   # EXEMPLO: siglas + a palavra do CTA em MAIÚSCULAS

# Muletas que a legenda NÃO mostra (continuam no áudio): pares (palavra, palavra seguinte).
SKIP = set()                                    # EXEMPLO 2, reel CLONE: {("a", "CLONE")}  ("comenta a CLONE")
# ===== FIM DO EDITE AQUI =====

# Trava contra valores de EXEMPLO esquecidos (não precisa mexer aqui): avisa e segue.
_EXEMPLOS = {"CUTS": [5.567, 8.733, 11.900, 16.133, 19.233],
             "EYES": [(0.454, 0.460), (0.433, 0.468), (0.444, 0.470), (0.434, 0.467), (0.445, 0.467), (0.469, 0.468)],
             "DISPLAY": {"ia": "IA", "mcp": "MCP", "clone": "CLONE"}}
for _nome, _ex in _EXEMPLOS.items():
    if globals()[_nome] == _ex:
        print(f"AVISO: {_nome} ainda tem o valor de EXEMPLO do kit; troque pelo seu")

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROXY = f"{P}/media/take.mp4"
CAUDA_PROXY = 0.27      # o proxy é cortado com -t <duração do original + 0,27 s> (passo 3, item 1)


def snap(t):
    return round(round(t * FPS) / FPS, 4)


def proxy_duration():
    """Duração do proxy media/take.mp4 (ffprobe), ou None se ele ainda não existe."""
    if not os.path.exists(PROXY):
        return None
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "default=nw=1:nk=1", PROXY])
    return float(out.decode().strip())


words = json.load(open(f"{P}/edit/words_source.json"))
_proxy = proxy_duration()
if TOTAL is None:
    assert _proxy is not None, ("TOTAL não foi definido e o proxy media/take.mp4 ainda não existe. Crie o proxy "
                                "(passo 3, item 1) ou ponha em TOTAL a duração do vídeo ORIGINAL (ffprobe, veja o "
                                "comentário de TOTAL).")
    TOTAL = snap(_proxy - CAUDA_PROXY)
    print(f"AVISO: TOTAL não foi definido; usando {TOTAL}s (duração do proxy media/take.mp4 − {CAUDA_PROXY} s de "
          "cauda). Confira com o ffprobe do vídeo ORIGINAL e cole o valor em TOTAL.")
elif _proxy is not None and TOTAL > _proxy:
    print(f"AVISO: TOTAL ({TOTAL}s) passa do fim do proxy media/take.mp4 ({_proxy:.3f}s): confira TOTAL com o "
          "ffprobe do vídeo ORIGINAL.")
_ultima = max(w["end"] for w in words)
if _ultima > TOTAL:
    print(f"AVISO: a última palavra termina em {_ultima}s, depois de TOTAL ({TOTAL}s): confira TOTAL.")
assert CUTS == sorted(CUTS) and all(0 < c < TOTAL for c in CUTS + ZOOM), \
    "CUTS/ZOOM precisam estar em ordem e dentro do vídeo: troque os EXEMPLOS pelos seus cortes"
cut_bounds = [0.0] + CUTS + [TOTAL]
assert len(EYES) == len(cut_bounds) - 1, f"EYES precisa de {len(cut_bounds) - 1} itens (len(CUTS) + 1); tem {len(EYES)}"
bounds = sorted(cut_bounds[:-1] + ZOOM) + [TOTAL]
edl = []
for n, (a, b) in enumerate(zip(bounds, bounds[1:])):
    k = max(j for j, c in enumerate(cut_bounds[:-1]) if c <= a)          # parent (real) piece for the eye data
    ws = [w["text"] for w in words if a <= w["start"] < b]
    edl.append({"id": f"a{n:02d}", "start": snap(a), "duration": snap(b - a), "frame": "A" if n % 2 == 0 else "B",
                "eye_x": EYES[k][0], "eye_y": EYES[k][1], "zoomcut": a in ZOOM, "text": " ".join(ws)})

kept = []
for i, w in enumerate(words):
    nxt = words[i + 1]["text"] if i + 1 < len(words) else ""
    piece = next(e["id"] for e in edl if e["start"] <= w["start"] < e["start"] + e["duration"] + 1e-6)
    kept.append({"i": i, "text": DISPLAY.get(w["text"].lower(), w["text"].lower()), "raw": w["text"],
                 "start": w["start"], "end": w["end"], "piece": piece, "skip": (w["text"], nxt) in SKIP})

json.dump(edl, open(f"{P}/edit/edl.json", "w"), ensure_ascii=False, indent=1)
json.dump(kept, open(f"{P}/edit/words.json", "w"), ensure_ascii=False, indent=0)
print(f"{len(edl)} pieces, total {TOTAL}s, {len(kept)} words ({sum(w['skip'] for w in kept)} skipped in captions)")
for e in edl:
    print(f'{e["id"]} {e["frame"]} {e["start"]:6.2f} +{e["duration"]:5.2f} | {e["text"]}')
