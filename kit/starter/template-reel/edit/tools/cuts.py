"""cuts.py: lista CANDIDATOS a corte num vídeo que já chega cortado (pipeline TAKE CORTADO).

O que faz : compara quadro a quadro só a faixa de CIMA do fundo (parede, luminária). Essa região não mexe quando você
            gesticula; ela só "pula" num corte. Candidato = quadro cuja diferença média é > max(MIN_DIFF, FACTOR ×
            mediana dos NEIGH quadros de cada lado).
Onde fica : <seu projeto>/edit/tools/cuts.py
Rodar     : (dentro da pasta do projeto, depois de criar o proxy media/take.mp4)
              ffmpeg -i media/take.mp4 -vf "scale=72:128,format=gray" -f rawvideo g.raw
              python3 edit/tools/cuts.py g.raw
Saída     : "frames N median M" e uma linha por candidato:  <segundos> f<quadro> diff=<diferença> local=<mediana local>
O que fazer com a saída:
  1. São CANDIDATOS, não cortes. Confira cada um no olho com o par "quadro antes / quadro depois":
       f=816; ffmpeg -i media/take.mp4 -vf "select='between(n,$((f-1)),$f)',scale=200:-1,tile=2x1" -fps_mode passthrough -frames:v 1 par_$f.png
     Se o fundo e a postura pulam, é corte de verdade. Movimento de mão sozinho NÃO conta.
     (No exemplo 2: 23 candidatos, 7 eram só gesto; ficaram 16 cortes, todos em fronteiras de frase.)
  2. Cole os segundos dos cortes aprovados na lista CUTS do edit/build_edl.py (take-cortado).
Se o topo do seu quadro não é um fundo parado (ex.: câmera na mão), ajuste ROWS para uma faixa de fundo parado.
"""
import sys

# ===== EDITE AQUI =====
W, H = 72, 128          # tamanho do g.raw (tem que bater com o scale=72:128 do ffmpeg; 72x128 = vídeo vertical 9:16)
FPS = 30                # quadros por segundo do proxy (para converter quadro -> segundos)
ROWS = (0, 55)          # faixa de linhas comparada (de cima para baixo, em 128): só o fundo parado do topo do quadro
MIN_DIFF = 0.9          # diferença mínima absoluta para virar candidato
FACTOR = 2.4            # ... e precisa ser FACTOR vezes maior que a mediana dos vizinhos
NEIGH = 6               # quantos quadros de cada lado entram na mediana local (6 + 6 = 12)
# ===== FIM DO EDITE AQUI =====

if len(sys.argv) < 2:
    sys.exit("uso: python3 edit/tools/cuts.py g.raw   (g.raw = ffmpeg ... -vf \"scale=72:128,format=gray\" -f rawvideo g.raw)")
b=open(sys.argv[1],'rb').read(); n=len(b)//(W*H)
fr=[b[i*W*H:(i+1)*W*H] for i in range(n)]
# compare only the upper background region (wall/lamp) to avoid hand motion
def d(a,c,r0=ROWS[0],r1=ROWS[1]):
    s=0
    for y in range(r0,r1):
        o=y*W
        for x in range(W): s+=abs(a[o+x]-c[o+x])
    return s/((r1-r0)*W)
ds=[0]+[d(fr[i-1],fr[i]) for i in range(1,n)]
srt=sorted(ds); med=srt[n//2]
print("frames",n,"median",round(med,2))
for i in range(1,n):
    nb=ds[max(1,i-NEIGH):i]+ds[i+1:i+NEIGH+1]; loc=sorted(nb)[len(nb)//2]
    if ds[i]>max(MIN_DIFF, FACTOR*loc): print(f"{i/FPS:7.3f} f{i} diff={ds[i]:.2f} local={loc:.2f}")
