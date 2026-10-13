"""Alinhamento forçado (torchaudio MMS_FA): acha o início e o fim EXATOS de cada palavra falada.

Pipeline : TAKES BRUTOS (vários arquivos de câmera, sem cortes; o script build_edl.py é quem corta na voz).
Onde fica: copie este arquivo para <seu projeto>/edit/align.py (ele procura as pastas a partir de edit/).
Entrada  : edit/segments.json, uma lista com um segmento por bloco do roteiro: {label, clip, in, out, text}
             label = nome do bloco (ex.: "hook"), usado no ORDER do build_edl.py
             clip  = nome do take (ex.: "IMG_2873"); o áudio dele fica em edit/audio/<clip>.wav
             in/out = trecho do take em segundos; text = transcrição corrigida daquele trecho
           O texto vai sem pontuação e em minúsculas, EXCETO nomes próprios e siglas, que ficam escritos exatamente
           como as chaves do dicionário NUM abaixo.
           edit/audio/<clip>.wav: áudio 16 kHz mono de cada proxy, por exemplo:
             ffmpeg -i media/t1-hook.mp4 -ac 1 -ar 16000 edit/audio/IMG_2873.wav
Saída    : edit/words_source.json: [{seg, clip, text, start, end, score}], em segundos de cada take.
Rodar    : uv run --offline --no-project -p 3.12 --with torch==2.5.1 --with torchaudio==2.5.1 --with numpy python edit/align.py
           Na 1ª vez numa máquina nova, rode SEM --offline: o uv baixa o Python 3.12, o torch e o torchaudio, e o
           torchaudio baixa o modelo MMS_FA. Depois disso funciona offline.
           Mac Intel: o torch 2.5.1 só existe para Mac com chip Apple. Troque por
             --with torch==2.2.2 --with torchaudio==2.2.2 --with "numpy<2"   (o MMS_FA existe desde o torchaudio 2.1;
           NÃO testado por nós).
Por quê  : os tempos por palavra do whisper erram por frações de segundo (às vezes segundos). O whisper só dá o TEXTO;
           o TEMPO de cada palavra vem daqui. Cortes, legendas, punch-ins, cenas e SFX são marcados com estes tempos.

(Forced-align each segment's words with torchaudio MMS_FA. Output: edit/words_source.json, source seconds.)
"""

# ===== EDITE AQUI =====
# Grafia "fonética" usada SÓ pelo alinhador (o modelo só conhece as letras a–z). Chave = como a palavra está escrita
# no edit/segments.json; valor = como ela SOA em português. Números viram palavras; nomes estrangeiros e siglas viram
# a pronúncia. A legenda continua usando a grafia original (a chave).
NUM = {
    "5": "cinco", "1": "um", "10": "dez", "1000": "mil",          # números que aparecem no roteiro, por extenso
    # EXEMPLOS (vieram do exemplo 2): troque/adicione os nomes próprios e siglas do SEU roteiro
    "IA": "ia", "MCP": "emecepe", "Claude": "cloud", "Higgsfield": "higsfild", "Launchpoint": "lantipoint",
    "Genjutsu": "guenjutsu",
}
# ===== FIM DO EDITE AQUI =====

import json, re, unicodedata, wave, struct, torch, torchaudio, os
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(w):
    w = NUM.get(w, w)
    w = unicodedata.normalize("NFKD", w.lower()); w = "".join(c for c in w if not unicodedata.combining(c))
    return re.sub(r"[^a-z']", "", w)
def load(clip, a, b):
    wf = wave.open(f"{P}/edit/audio/{clip}.wav"); sr = wf.getframerate()
    wf.setpos(int(a * sr)); n = int((b - a) * sr); raw = wf.readframes(n)
    x = torch.tensor(struct.unpack("<%dh" % (len(raw) // 2), raw), dtype=torch.float32) / 32768
    return x.unsqueeze(0), sr
bundle = torchaudio.pipelines.MMS_FA
model = bundle.get_model(with_star=False); tok = bundle.get_tokenizer(); aligner = bundle.get_aligner()
out = []
for s in json.load(open(f"{P}/edit/segments.json")):
    words = s["text"].split(); keys = [norm(w) for w in words]
    bad = [w for w, k in zip(words, keys) if not k]
    assert not bad, (f"Palavras sem grafia para o alinhador: {bad}. Ponha cada uma no NUM por extenso "
                     "(ex.: '2026': 'dois mil e vinte e seis').")
    wav, sr = load(s["clip"], s["in"], s["out"])
    with torch.inference_mode():
        em, _ = model(wav); spans = aligner(em[0], tok(keys))
    ratio = wav.shape[1] / em.shape[1] / sr
    for w, sp in zip(words, spans):
        a = s["in"] + sp[0].start * ratio; b = s["in"] + sp[-1].end * ratio
        sc = sum(x.score * len(x) for x in sp) / sum(len(x) for x in sp)
        out.append({"seg": s["label"], "clip": s["clip"], "text": w, "start": round(a, 3), "end": round(b, 3), "score": round(sc, 3)})
json.dump(out, open(f"{P}/edit/words_source.json", "w"), ensure_ascii=False, indent=0)
for o in out: print(f'{o["seg"]:6} {o["start"]:7.3f}-{o["end"]:7.3f} {o["score"]:.2f} {o["text"]}')
