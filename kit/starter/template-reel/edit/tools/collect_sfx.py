"""collect_sfx.py: junta os SFX que os REVISORES do workflow das cenas devolveram em edit/sfx_from_review.json.

Onde fica : <seu projeto>/edit/tools/collect_sfx.py
Quando    : depois que o workflow das cenas (edit/workflow-cenas.js) terminar, antes do build_index.py.
Rodar     : python3 edit/tools/collect_sfx.py <caminho do journal.jsonl do workflow>
            O journal.jsonl fica na pasta da transcrição do workflow (o Claude Code mostra o caminho no resultado do
            workflow). Mais fácil: peça ao Claude Code "rode o collect_sfx.py com o journal.jsonl do workflow das cenas".
Saída     : edit/sfx_from_review.json: lista [tempo global, arquivo, volume, duração ou null, id da cena], em ordem.
Depois    : python3 edit/build_index.py   (ele lê esse arquivo e coloca cada SFX no index.html; use DROP para tirar
            sons que empilham mais de 2 por batida). Os .mp3 vão em assets/sfx/, copiados de
            ~/.claude/skills/media-use/audio/assets/sfx/ (não vêm no kit).
Como      : cada revisor devolve {scenes:[{id, sfx:[{t (s globais), file, volume, duration?}]}], lint_clean}. Só entram
            as listas FINAIS dos revisores (as que têm lint_clean), não as sugestões dos construtores.

(Collect the SFX the scene reviewers returned into edit/sfx_from_review.json, read by build_index.py.)
"""
import json, os, sys

P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if len(sys.argv) < 2:
    sys.exit("uso: python3 edit/tools/collect_sfx.py <journal.jsonl do workflow>")
out = []
for line in open(sys.argv[1]):
    r = json.loads(line)
    if r.get("type") != "result":
        continue
    v = r.get("value") or r.get("result")
    if isinstance(v, str):
        try:
            v = json.loads(v)
        except ValueError:
            continue
    if not isinstance(v, dict) or "lint_clean" not in v:      # only the reviewers' (final) lists
        continue
    for s in v["scenes"]:
        for x in s["sfx"]:
            out.append((x["t"], x["file"], x["volume"], x.get("duration"), s["id"]))
json.dump(sorted(out), open(f"{P}/edit/sfx_from_review.json", "w"), indent=0)
print(len(out), "sfx ->", f"{P}/edit/sfx_from_review.json")
