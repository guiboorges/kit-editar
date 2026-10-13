# Padrão de qualidade: reels de talking head + motion (qualquer tema, qualquer criador)

Este é o padrão escrito que o Claude Code segue para editar um reel vertical (Instagram Reels / TikTok, 1080×1920,
30 fps) no formato **tela dividida**: você falando em cima, legenda karaokê na emenda e motion design sobre papel
claro embaixo, com uma cena para cada frase, batendo na palavra falada.

Ele nasceu da análise quadro a quadro de um reel de referência real e foi refinado em dois reels reais, citados
aqui só como **exemplos**:

- **Exemplo 1** (47,9 s): vários takes brutos, cortados pelo script na voz (pipeline A). Gerou as 8 cenas de
  `template-reel/scenes-exemplo/` e as 59 receitas de `RECEITAS-DE-MOTION.md`.
- **Exemplo 2** (65,4 s): um arquivo único já cortado pelo criador, com 16 cortes (pipeline B). Gerou as 11 cenas
  de `template-reel/scenes-exemplo-2/`.
- Referência visual que originou o formato: o reel "Comenta PERSONAGEM" (@higgsfield.ai). Para o seu vídeo, use a
  sua própria referência (§3).

> **Os mesmos nomes em todo o kit:** pipeline A = `takes-brutos` = exemplo 1 (reel PERSONAGEM, 47,9 s);
> pipeline B = `take-cortado` = exemplo 2 (reel CLONE, 65,4 s).

Onde está cada coisa neste kit (pasta `starter/`):

| Arquivo | Para quê |
|---|---|
| `PADRAO-DE-QUALIDADE.md` | este arquivo: o formato, as regras e o fluxo |
| `RECEITAS-DE-MOTION.md` | 59 receitas de motion com números exatos (easing, duração, escala) |
| `template-reel/DESIGN.md` | a "verdade do design" para copiar no projeto (zonas, paleta, tipografia, contrato da cena) |
| `template-reel/STORYBOARD-exemplo.md`, `BRIEF-exemplo.md` | modelos do storyboard (o contrato dos agentes) e do brief |
| `template-reel/edit/takes-brutos/` | scripts do pipeline A (vários takes brutos) |
| `template-reel/edit/take-cortado/` | scripts do pipeline B (um take já cortado por você) |
| `template-reel/edit/tools/` | `cuts.py` (cortes), `face.swift` (olhos), `collect_sfx.py` (SFX dos agentes) |
| `template-reel/edit/workflow-cenas.js` | o workflow multiagente que constrói e revisa as cenas |
| `template-reel/scenes-exemplo/`, `scenes-exemplo-2/` | cenas prontas para adaptar (código de referência) |
| `template-reel/fonts/` | Geist e Geist Mono (licença OFL) |
| SFX | **não vêm no kit**: ver §5 |

> **Para o Claude no próximo vídeo:** leia este arquivo inteiro antes de começar. Ele substitui a fase de
> descoberta: o formato, o design, as legendas, os SFX e o fluxo de trabalho já estão decididos. Só mude o que o
> roteiro novo ou a referência nova exigirem, e anote a mudança no BRIEF.md do projeto.

---

## 1. O formato (o que o público vê)

| Zona | Faixa (px, 1080×1920) | Conteúdo |
|---|---|---|
| Câmera | y 0–780 (≈40%) | O apresentador, close, olhos em y≈320 (≈40% do painel). Fica **acima** das cenas. |
| Emenda (legenda) | y 800–920 | Legenda karaokê 1–4 palavras. Nada da cena entra aqui. |
| Palco (motion) | y 940–1860 | Cenas de motion design sobre papel claro. Centro visual ≈ (540, 1340). |
| Área segura | x 70–1010, y 950–1680 | Texto e números importantes. Abaixo de 1700 a UI do Reels cobre. |

- **Papel**: `#F3F3F0` + brilho radial lima (34% → 0) respirando atrás do palco + grão sutil (6%).
- **Câmera em tela cheia** em 1 ou 2 frases de conversa direta (exemplos: "e pensa comigo…", "tá, e como é que
  você pode fazer isso?"): clip-path abre 0,36 s `power3.inOut`, legenda desce para y 1540, branca. Quebra o
  ritmo da tela dividida.
- **B-roll** (o assunto do vídeo: perfis, produtos, exemplos reais) ocupa o palco inteiro (780–1920) com chip de
  atribuição `@perfil · N mil seguidores` e tag (no exemplo, `● 100% IA`). Legenda vira branca com sombra +
  degradê escuro de 260 px no topo.
- Duração-alvo 45–50 s (o exemplo 2 teve 65,4 s, com 11 cenas). Gancho nos primeiros 3 s com B-roll + carimbo.

## 2. Materiais de entrada (checklist)

- [ ] Câmera: **ou** takes do talking head sem cortes (iPhone 4K vertical HEVC 60p funciona; um take por bloco do
      roteiro, 2–3 tentativas) → pipeline A; **ou** um arquivo único que você já cortou → pipeline B (§4).
- [ ] Roteiro (texto ou PDF) com blocos, âncoras e, se tiver, uma tabela "referência de corte".
- [ ] Vídeo de referência (o formato a copiar).
- [ ] Prints de suporte (plataforma, ranking, perfis), de preferência em 2× (retina) para não amolecer no zoom.
      **Todo número que aparece na tela sai daqui ou do roteiro.**
- [ ] B-roll do assunto (MP4 do Instagram serve) + prints dos perfis com nº de seguidores.
- [ ] Seus próprios ativos (ex.: o seu personagem, telas do app que você usou, o resultado que você mostra).
- [ ] Mídia pendente? Comece mesmo assim: deixe *slots* com ids estáveis (ex.: `#s7-resultado`) e troque depois.

## 3. Análise da referência (antes de desenhar)

1. Contact sheets a 2 fps: `ffmpeg -i ref.mp4 -vf "fps=2,scale=240:-1,tile=8x2:padding=4:color=white" sheet_%02d.png`.
2. Frames em resolução cheia nos momentos-chave; medir proporção câmera/painel, posição e caixa da legenda,
   paleta, como os cards entram e saem (blur? escala?), como os números aparecem, como é o CTA.
3. Escrever o `DESIGN.md` do projeto (zonas, paleta, tipografia, superfícies, linguagem de motion, contrato da
   sub-composição). O `template-reel/DESIGN.md` é o ponto de partida. Cores, fontes e linguagem de motion seguem o
   `DESIGN.md`. Já o **formato** (zonas da tela, posição da legenda, câmera sempre em tela cheia) está fixo nos
   scripts (`build_index.py`, `build_captions.py`) e no bloco `COMMON` do `workflow-cenas.js`: mudar o formato exige
   adaptar esses três. O kit só foi testado no formato tela dividida.
4. Verificar se a referência tem trilha (`ffmpeg -af ebur128`): a do exemplo tinha.

Copie o formato de uma referência real. Uma versão com "visual genérico de IA" foi rejeitada antes de este padrão
existir.

## 4. Decupagem, palavras e câmera

### 4.1 Analisar o bruto (vale para os dois pipelines)

```bash
SRC="<seu vídeo>"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of default=nw=1 "$SRC"
ffmpeg -i "$SRC" -vf "fps=1,scale=180:-1,tile=11x6:padding=4:color=white" -frames:v 1 sheet.png   # folha de contato
ffmpeg -i "$SRC" -ac 1 -ar 16000 a16.wav
ffmpeg -i "$SRC" -af ebur128 -f null -                                   # loudness do original
ffmpeg -i a16.wav -af silencedetect=noise=-38dB:d=0.12 -f null -          # há pausas?
ffmpeg -i "$SRC" -vf "scale=270:-1,scdet=threshold=4" -an -f null -       # candidatos a corte
```

Sinais de que o arquivo **já vem cortado e tratado** (pipeline B): loudness muito alto e comprimido (no exemplo 2,
−8,2 LUFS, LRA 1,6 LU, áudio já passado num aprimorador de voz), quase nenhum silêncio e "pulos" do fundo/postura.

### 4.2 Transcrição (whisper.cpp)

`whisper-cli -m ~/.cache/hyperframes/whisper/models/ggml-large-v3-turbo-q5_0.bin -l pt -f a16.wav --prompt "<nomes próprios, marcas, siglas>"`.
O `--prompt` ensina os nomes próprios ao modelo. Mesmo assim, corrija o texto à mão (no exemplo 2 o whisper
escreveu "Claudio" e "em quem Sam Consciência"); para trechos duvidosos, recorte só aquele pedaço e transcreva de
novo. **Os timestamps por palavra do whisper NÃO servem para corte nem para sincronizar animação** (erram por
frações de segundo, às vezes segundos): o whisper só dá o texto.

### 4.3 Alinhamento forçado (`edit/align.py`, torchaudio MMS_FA, offline)

`uv run --offline --no-project -p 3.12 --with torch==2.5.1 --with torchaudio==2.5.1 --with numpy python edit/align.py`
(na 1ª vez numa máquina nova, sem `--offline`: o uv baixa Python, torch e torchaudio, e o torchaudio baixa o modelo).
O torch 2.5.1 só tem versão para Mac com chip Apple (M1, M2, M3…). Em Mac Intel, troque por
`--with torch==2.2.2 --with torchaudio==2.2.2 --with "numpy<2"` (o MMS_FA existe desde o torchaudio 2.1; não testado).

- Entrada: `edit/segments.json` (take, in, out, texto corrigido) + `edit/audio/<take>.wav` (16 kHz mono).
  Pipeline A: um segmento por bloco do roteiro. Pipeline B: um segmento só, de 0 ao fim.
- Texto sem pontuação, minúsculas, exceto nomes próprios e siglas, escritos igual às chaves do dicionário `NUM`
  do `align.py`, que troca cada um por uma grafia "fonética" (ex.: "MCP" → "emecepe"). Números viram palavras
  ("5" → "cinco").
- Saída: `edit/words_source.json`, início e fim exatos de cada palavra. **Tudo** (cortes, cenas, legendas,
  punch-ins, SFX) é marcado a partir desses tempos.

### 4.4 Qual pipeline?

| | **A: takes brutos** (`edit/takes-brutos/`) | **B: take já cortado** (`edit/take-cortado/`) |
|---|---|---|
| Você entrega | vários takes, sem cortes, com tentativas repetidas | um arquivo só, que você já decupou |
| Quem corta a voz | o `build_edl.py`, nas pausas | ninguém: a timeline fica 1:1 com o seu arquivo |
| Câmera no index | um `<video>` por pedaço da EDL | **um único `<video>` contínuo** + caixas de enquadramento |
| Esconder o jump cut | A/B a cada corte do script | A/B a cada corte seu + zoom cuts |
| Exemplo | exemplo 1 (47,9 s) | exemplo 2 (65,4 s, 16 cortes) |

### 4.5 Pipeline A: takes brutos (cortes colados na voz)

`edit/build_edl.py`:
- Pausa > **0,30 s** só é cortada se tiver **≥ 0,16 s de silêncio real** (< −45 dB). Senão é fala contínua.
- Bordas de cada pedaço andam pela energia da voz (−45 dB, olhando 60 ms à frente): o alinhamento CTC termina as
  palavras cedo; sem isso o corte come o fim da palavra.
- Pausas intencionais ficam (`KEEP`): no exemplo 1, a pausa da revelação ("esse sou eu … esse aqui é o personagem").
- Último pedaço ganha cauda (`TAIL`) de ambiente para o CTA respirar; conferir que a mão não sai do quadro.
- Escolher a melhor tentativa (`ORDER`; no exemplo 1, a 2ª tentativa do gancho). Conectores sem silêncio limpo
  antes (ex.: "por incrível que pareça") ficam: cortar no meio da fala soa picotado.
- Todos os pontos no grid de 30 fps. Conferir `edge_db` de cada corte (≤ −40 dB nas duas pontas).

`edit/build_index.py`: medir em still com grade (ou com `tools/face.swift`) a posição do rosto de cada take
(x do centro do rosto, y da linha dos olhos) → `FACE`. Cada pedaço é um `<video>` com fade de 15 ms.

### 4.6 Pipeline B: take já cortado (a timeline fica 1:1)

Quando o criador já decupou a fala, **não recortamos a voz de novo**: a timeline toca o arquivo dele do começo ao
fim. Isso evita cortes picotados, cliques de áudio e travadas do decodificador.

1. **Detectar os cortes que já existem.** `scdet` dá candidatos; o `tools/cuts.py` é mais preciso: compara quadro a
   quadro só a faixa de cima do fundo (parede, luminária), que não mexe quando você gesticula, e só "pula" num
   corte. Candidato quando a diferença média das linhas 0–54 (de 128) > max(0,9; 2,4 × mediana dos 12 quadros ao
   redor). **Candidato não é corte**: confira cada par "quadro antes / quadro depois" no olho; gesto de mão sozinho
   não conta. No exemplo 2: 23 candidatos → 16 cortes de verdade, todos em fronteiras de frase. Cole os aprovados
   em `CUTS` (`edit/build_edl.py`).
2. **Peças A/B.** Cada trecho entre cortes vira uma peça que alterna A (1,00×) / B (1,10×): o pulo do corte vira
   também troca de tamanho de plano, e o olho lê como edição intencional. **Zoom cuts** (`ZOOM`): trocas extras de
   enquadramento num respiro dentro de trechos longos (exemplo 2: 2 zoom cuts → 19 peças).
3. **Olhos medidos por trecho** (`tools/face.swift`, Apple Vision, só macOS): 3 quadros de cada trecho (a 20%, 50%
   e 80% dele), média dos 3 → `EYES`. As peças de zoom cut herdam a medida do trecho de origem. A média de todos
   (exemplo 2: olhos em 46,6% da altura) vai em `EYE_MEAN_Y` do `build_index.py`.
4. **Um único `<video>` contínuo** (`media/take.mp4`, com a voz) dentro de 5 caixas, cada uma com uma só
   responsabilidade, para nenhuma animação brigar com outra:

   ```
   #cam            → clip-path: recorta a tela dividida (0–780) ou abre em tela cheia
    └ #cam-full    → split: y −714 · tela cheia: y −234 e escala calculada (olhos a 42% da altura)
      └ #cam-move  → punch-ins de 1,05× nas palavras-chave (reset no corte seguinte)
        └ #cam-drift  → empurrão lento 1,00→1,03 em cada peça (a câmera "respira")
          └ #cam-frame → enquadramento da peça (x, y, escala A/B), trocado no quadro exato do corte
            └ <video src="media/take.mp4">
   ```

   O script calcula, para cada peça, o deslocamento que põe os olhos em y = 1034 e confere se o vídeo ainda cobre o
   painel inteiro; e calcula a menor escala que cobre a tela toda nas telas cheias.
5. **Telas cheias** (`FULLS`, igual no `build_index.py` e no `build_captions.py`): abrem e fecham em 0,36 s
   `power3.inOut`, de preferência começando num corte. **A cena anterior segura até a câmera cobrir o palco**, como
   um wipe, e a seguinte já está entrando quando a câmera recolhe. Whoosh 0,14 na abertura e whoosh-short 0,12 em
   (fim − 0,36).
6. **Proxy com cauda**: `tpad=stop_mode=clone:stop_duration=0.3` + `apad=pad_dur=0.25`. No exemplo 2, o vídeo
   original terminava 0,1 s antes do áudio; sem a cauda, o último quadro sairia preto.

### 4.7 Enquadramento e cor (os dois pipelines)

- Olhos em y = 1034 do espaço da câmera → ≈ 320 do painel. Alterna **A (1,0×) / B (1,10×)** a cada corte (esconde
  o jump cut). Punch-in **1,05×** em palavras-chave, reset no corte seguinte. Drift lento 1 → 1,03 em cada pedaço
  (câmera viva). Proxy de 1440×2560 aguenta o zoom.
- **Cor**: Natural Portrait,
  `{"preset":"skin-soft","intensity":0.58,"adjust":{"contrast":0.05,"highlights":-0.08,"shadows":0.06,"vibrance":0.03},"details":{"vignette":0.03}}`.
  iPhone já é Rec.709: sem LUT. Se o vídeo já vem com look (no exemplo 2, teal/laranja), use uma grade mais leve
  (`intensity` 0,4).

## 5. Áudio

- **Cadeia de voz nos proxies**: `highpass=f=75, acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120:makeup=2, loudnorm=I=-14:TP=-1.5:LRA=9`, AAC 192k 48 kHz.
  Os exemplos começaram com `I=-15`: o exemplo 1 mediu −14,6 LUFS no render; no exemplo 2 o rascunho mediu
  −15,0 (no limite), a voz foi renormalizada para −14 e o final mediu −14,0. Por isso o padrão agora é −14.
- **Fade de 15 ms** em cada corte (lane de volume na própria `<video>`): sem estalos. No pipeline B só há fade no
  começo e no fim, porque o vídeo é contínuo.
- **Alvo**: −14 LUFS ±1, pico ≤ −1 dBFS (o alvo usual de redes sociais; o Instagram não publica um valor
  oficial). Medido: exemplo 1, −14,6 LUFS, pico −1,1 dBFS, LRA 2,0; exemplo 2, −14,0 LUFS, pico −1,1 dBFS, LRA 1,4.
- **SFX: os arquivos não vêm no kit.** São os da biblioteca da skill `media-use` do HyperFrames (Pixabay Content
  License: uso livre dentro dos seus vídeos, mas não pode ser redistribuída como arquivos soltos). Instale as skills
  do HyperFrames (`npx --yes hyperframes@0.8.141 skills update general-video`, que instala também o conjunto básico,
  com a `media-use`) e copie para o projeto:
  `mkdir -p assets/sfx && cp ~/.claude/skills/media-use/audio/assets/sfx/*.mp3 assets/sfx/`.
  Volumes calibrados pela loudness medida de cada arquivo:

| Evento visual | Som | Volume | Regra |
|---|---|---|---|
| Card/janela entrando (blur-rise) | `whoosh` | 0,16–0,20 | no início do movimento |
| Troca rápida, morph, slide | `whoosh-short` | 0,12–0,22 | no início |
| Pílula/selo/etiqueta aparece | `pop` | 0,20–0,36 | no pico do pop (≈ +0,05 s) |
| Anel lima, destaque, "ding" | `ping` | 0,22–0,32 | no pico |
| Toggle, clique, enviar | `click` | 0,30–0,42 | no frame do clique |
| Digitação (prompt, busca) | `typing` / `key-press` | 0,34 / 0,48 | durante a digitação; 1 key-press por tecla curta |
| Revelação do personagem / vencedor | `sparkle` | 0,16–0,20 | no reveal |
| Resultado em dinheiro / slam | `impact-bass-2` + `pop` | 0,08 + 0,33 | no slam |
| Abertura do vídeo | `impact-bass-1` | 0,10 | t=0 |
| Notificação de DM | `notification` | 0,30 | quando o banner fica nítido |
| Câmera abre / fecha em tela cheia | `whoosh` / `whoosh-short` | 0,14 / 0,12 | no início de cada movimento |

  Regra geral: no máximo 1–2 SFX por batida; o som cai no **pico visual** (não no começo do fade).
  Os revisores do workflow devolvem a lista final de SFX de cada cena (tempo global); `tools/collect_sfx.py` junta
  tudo em `edit/sfx_from_review.json` e o `build_index.py` coloca no vídeo. Use `DROP` para tirar sons que empilham
  mais de 2 por batida, e a duração nunca passa do tamanho do arquivo (`SFX_LEN`).
- **Música**: o padrão ainda não tem trilha. Opções: trilha em alta no app do Instagram, ou arquivo seu mixado por
  baixo da voz com carve (`/hyperframes-audio` → `scripts/carve.mjs`).

## 6. Legendas (karaokê na emenda)

- **Tipo**: Geist 600, 66 px, tracking −0,028em, minúsculas (siglas e a palavra do CTA em maiúsculas: no exemplo,
  IA, MCP, CLONE; configure em `DISPLAY` no `build_edl.py`).
- **Blocos**: 1–4 palavras, ≤ ~22 caracteres, uma linha. **Lista manual** quebrando onde a voz quebra (nunca
  terminar bloco em "de/o/que/e/por"; poucas exceções onde a fala pede, como "por que", "e como é que"). No
  exemplo 2: em geral 1–3 palavras, até ~18 caracteres, 108 blocos. Pipeline A: `CHUNKS` (nº de palavras por
  bloco); pipeline B: `CHUNK_TEXT` (o texto de cada bloco; o script confere palavra por palavra com o áudio).
  Lista vazia = blocos automáticos, bons para começar; uma versão automática deixou "e" e "eu" sozinhos no exemplo 2
  e foi trocada pela lista manual.
- **Karaokê**: palavras ainda não ditas a 42% → 100% no início da palavra (−0,03 s).
- **Destaque lima**: bloco `#D4FF3A` raio 14 px cresce `scaleX 0→1` 0,2 s `power3.out` (−0,05 s) + texto vira
  `#141A00` + pulso 1,06 ida e volta. **≈ 1 destaque a cada 3 s** (gancho, número, marca, prova, CTA). No
  exemplo 2: 18 destaques (26 palavras em `HL_AT`, cada uma pelo tempo exato de início).
- **Entrada/saída**: entra 0,14 s (blur 8→0, y 16→0) em início −0,03; sai 0,05 s em próximo início −0,08 (sem
  sobreposição). Em pausas longas some 0,45 s após a última palavra.
- **Modos**: `paper` (tinta no papel), `broll` (branca + sombra; some antes do B-roll sair), `full` (câmera em
  tela cheia: y 1540, 74 px). Cortar o tempo de cada bloco nas fronteiras de modo: na tela cheia o bloco some quando
  a borda da câmera passa por ele (fim − 0,22 s); o primeiro bloco depois espera a emenda aparecer (fim − 0,04 s).
  Assim nunca há texto escuro sobre o vídeo nem texto branco sobre o papel.
- **Muletas** ("comenta **a** CLONE") são alinhadas no áudio mas não aparecem na legenda (`SKIP`).

## 7. Motion (linguagem e receitas)

**Princípios** (valem para toda cena):
- **Entrada blur-rise**: `{opacity 0, y 70, scale .94, blur 16px}` → limpo, 0,5 s `power3.out`.
- **Saída blur-out**: `{opacity 0, scale 1.04, blur 14px}`, 0,2–0,26 s `power2.in`, **terminando ≥ 1 frame antes do
  fim da cena** (a não ser que o storyboard diga HOLD: aí a cena segura até o último quadro, por exemplo quando a
  câmera vai cobrir o palco numa tela cheia).
- **Pico na palavra**: comece o movimento ~0,10 s antes da palavra para ele chegar no pico quando ela é dita.
- **Nada parado**: tudo que fica em tela respira (escala +2–3% ou y −10 px ao longo do hold, `ease:"none"`).
  Hold morto = mais de ~1 s sem nada se mexendo no palco.
- **Foco (rack focus)**: o que sai de foco vira *fantasma claro* (blur 5–6 px, opacity .24–.45, brightness 1,25–1,5,
  saturate .5), nunca uma mancha escura.
- **Duas camadas no pop**: NUNCA animar `filter: blur()` dentro de easing com overshoot (`back.out`): em seek o blur
  fica negativo, o navegador rejeita e o elemento fica borrado. Separar: opacity+blur em `power2.out`,
  escala em `back.out`.
- **Anel lima**: borda 6 px `#D4FF3A`, halo `0 0 0 10px rgba(212,255,58,.28)`, raio = alvo + 8 px; entra
  `back.out(2)` 0,3–0,4 s; tem que abraçar o alvo exatamente.
- Variar easings dentro da cena; stagger total ≤ 0,5 s.

**Regras de construção** (aprendidas nas 19 cenas dos dois exemplos):
- **Grade de cues no topo do script**: constantes com o início de cada palavra (`NEM=2.05`, `POP=3.76`…) e todo
  tween derivado delas (`NEM-0.05`). Retimar = mudar um número.
- **Um wrapper por responsabilidade** (saída / impacto / drift / tilt / ken burns). Nenhuma propriedade animada por
  dois tweens ao mesmo tempo; quem escreve `style.transform` num `onUpdate` é dono exclusivo daquele elemento.
- **Montar no estado final** e animar a partir de um offset; só `transform`, `opacity`, `filter`, `clip-path`.
- **Prints viram motion** reconstruindo em HTML o pedaço importante (pílula, linha do ranking) sobre a mesma posição
  do print e trocando num único frame ("gêmeo" nítido). A cor do gêmeo tem que ser a do print (no exemplo 2, o azul
  real `#0463FF`), senão a troca aparece.
- **Medir, não chutar**: larguras de texto medidas depois de `document.fonts.load`, `tabular-nums` em números.
  Número que conta ("até US$ 2.000"): caixa de largura fixa com o valor final invisível, para o layout não pular a
  cada dígito.
- **Pulsos** = `set` instantâneo + expansão (seek-safe). `repeat` sempre finito.
- **Placeholders** (bordas tracejadas, esqueletos) se dissolvem antes do conteúdo chegar; nada vaza por trás.
- **CTA final não sai de cena**: segura até o último frame com drift, pulso de eco e um micro-beat tardio (curtida).
- **Vídeo dentro de card**: caixa no aspecto nativo dentro de um wrapper com `overflow:hidden` (o render ignora
  `object-fit` em wrappers transformados).
- **Números na tela: só os do print/roteiro.** Nenhum dado inventado; ressalva escrita quando for conta ou teto
  ("cálculo ilustrativo", "teto de uma campanha real").

**Catálogo de cenas** (receitas com números exatos em `RECEITAS-DE-MOTION.md`, uma seção por cena de
`template-reel/scenes-exemplo/`):

| Arquétipo | Arquivo-exemplo | Movimentos-assinatura | Quando usar |
|---|---|---|---|
| Gancho com B-roll | `scenes-exemplo/s1-hook.html` | B-roll cheio desde o frame 0 com drift + punch de impacto; corte seco com flash branco de 2 frames; carimbo lima girado −4° que "bate" (escala 1,7→1, 0,22 s expo.out) + anel de eco; chip de atribuição; cronômetro cujo anel conduz a contagem até 4:59 | Primeiros 3–5 s, prova visual da frase-gancho |
| Print da plataforma | `scenes-exemplo/s2-launchpoint.html` | Card chega já desfocado desde o frame 0 e fica nítido na palavra; brilho lima passando; foco puxado (card vira fantasma claro); pílulas "puxadas" do print como HTML nítido; anel lima pulando de alvo; promoção a herói | Apresentar plataforma/site com regras ou números do print |
| Equação / dinheiro | `scenes-exemplo/s3-calc.html` | Frase monta palavra a palavra recentrando; a frase vira a linha de baixo (FLIP medido); contagem 0→1.000.000 crescendo de escala; resultado em bloco lima que "bate" + brilho; ressalva escrita | Qualquer conta (CPM, ganhos, %) |
| Pergunta → ranking | `scenes-exemplo/s4-quem-banca.html` | Barra de busca digitando com cursor; headline com bloco lima na palavra-chave; print do ranking sob o título que encolhe; linha do líder "levanta" do print com foco puxado; etiqueta "#1" + anel | "Quem paga / quem é o maior" |
| Comparação ✕ / ✓ | `scenes-exemplo/s5-ciclo.html` | Card sozinho no centro que abre espaço para o segundo; risco vermelho desenhado + disco ✕ + dessatura o perdedor; selo da marca; anel lima no vencedor; fecho com ícone + seta em loop e frase com bloco lima | "Em vez de X, Y" |
| Janela de app (prova) | `scenes-exemplo/s6-teste.html` | Janela fixa com estados internos (conectores → toggle ON sincronizado com anel → chat com prompt digitado → envio com mola → "gerando" com shimmer + cronômetro → resultado cresce do esqueleto) | Mostrar "eu fiz isso" num app |
| Antes × depois | `scenes-exemplo/s7-genjutsu.html` | Handoff idêntico ao último frame da cena anterior; morph do card (paisagem → retrato); still vira vídeo com zoom-out; ORIGINAL × RESULTADO sincronizados frame a frame com tilt de livro aberto; faíscas determinísticas | Revelação do resultado |
| CTA de comentários | `scenes-exemplo/s8-cta.html` | Folha de comentários sobe; campo foca e digita a palavra-chave com tecla a tecla; envio com mola e explosão radial; palavra viaja até o comentário (FLIP) e empurra a lista; banner de DM cai por cima; segura até o fim | "Comenta X que eu te mando" |

Mais 11 variações, do exemplo 2, em `template-reel/scenes-exemplo-2/` (sem seção própria nas receitas; cada uma
adaptou as cenas acima):

| Arquivo | O que mostra | Adaptou |
|---|---|---|
| `s1-hook.html` | montagem de 3 B-rolls, tag, créditos com nº de seguidores, carimbos "ELE NÃO EXISTE" e "POR QUÊ?" | s1-hook |
| `s2-dinheiro.html` | bloco "$", os dois criadores, contador até "US$ 2.000 /vídeo" que bate | s3-calc |
| `s3-quem-paga.html` | título cinético "quem pagaria?" com bloco lima + mini-vídeo com "?" | s4-quem-banca |
| `s4-launchpoint.html` | página entrando em foco, pílula puxada do print, rolagem até o ranking, linha que salta com "#1" | s2-launchpoint + s4-quem-banca |
| `s5-ciclo.html` | card riscado × card vencedor com moedas, depois o ciclo marca ⇄ vídeos | s5-ciclo |
| `s6-voce.html` | 3 balões "tá", 2 cards de vídeo com "+ $", espaço tracejado "você?" | s5-ciclo + s7-genjutsu |
| `s7-claude.html` | janela do Claude: conectores, toggle ON, pílula MCP, prompt digitado e enviado | s6-teste |
| `s8-avatar.html` | retrato com contorno de seleção no cabelo, amostra de cor, régua, chips esqueleto, folha de corpo inteiro | s6-teste + s7-genjutsu |
| `s9-genjutsu.html` | app escuro: clique na aba, sorteio entre vídeos, slots, Gerar, "manipulando… %" | s6-teste |
| `s10-resultado.html` | ORIGINAL × RESULTADO lado a lado, sincronizados quadro a quadro | s7-genjutsu |
| `s11-cta.html` | comentários: digita a palavra, envia, DM cai e abre um checklist de 3 passos, carimbo final | s8-cta |

## 8. Design tokens

```css
--paper:#F3F3F0; --ink:#111113; --ink2:#3A3A40; --mute:#7A7A82; --line:#E2E2DC; --card:#FFFFFF;
--ui:#141416; --ui2:#1E1E22; --lime:#D4FF3A; --limeInk:#141A00; --plum:#6B2A6B; --red:#FF4A3D; --blue:#3D4EF2;
```

- **Fontes**: Geist (100–900, variável) para tudo + Geist Mono para rótulos/etiquetas (UPPERCASE, +0,04–0,06em).
  Arquivos locais: copie `template-reel/fonts/*.woff2` para `assets/fonts/` do projeto e carregue com `@font-face`
  (não depender de fonte do sistema). Licença: SIL OFL 1.1 (`template-reel/fonts/OFL.txt`).
- **Escala**: número herói 150–180 px/800 · headline 84–110 px/700 · título de card 38–46 px/600 ·
  corpo de card 28–34 px/500 · rótulo 24–30 px mono. Nada abaixo de 24 px.
- **Superfícies**: card claro raio 34 + sombra `0 34px 80px rgba(24,24,12,.16), 0 6px 18px rgba(24,24,12,.08)`;
  card escuro de UI raio 30, borda `rgba(255,255,255,.07)`; pílulas raio 999.
- **Um único acento.** Nos exemplos, o lima, que casava com a marca do assunto. Se a sua referência pedir outra cor,
  troque em todo lugar: `DESIGN.md`, cenas, `build_captions.py` (destaque) e `build_index.py` (brilho do papel).
  Cores de apoio (no exemplo, roxo/vinho do personagem) só nos momentos delas.

## 9. Armadilhas técnicas já resolvidas (HyperFrames 0.8.140 / 0.8.141)

- **Proxies com GOP curto**: `-g 15 -keyint_min 15 -sc_threshold 0` (keyframe a cada 0,5 s). Com GOP longo
  (8 s) o preview trava em todo corte. B-roll do Instagram também precisa ser recodificado (`-g 12`).
- **Nunca deixar `animation-map.mjs` rodando**: abriu um Chrome invisível que comeu 8 núcleos e travou o preview.
- **Vídeo dentro de card transformado**: o render ignorou `object-fit: cover` → dar à `<video>` a caixa no aspecto
  nativo (ex.: 400×711, top −35,56) e enquadrar com um wrapper; nunca animar a caixa do `<video>`.
- `data-start` de mídia dentro de sub-composição é local; marcar `data-hf-media-start-basis="local"`.
- Ids e seletores prefixados com o id da cena; `<style>`/`<script>` dentro do `<template>`.
- Cena é sub-composição tela cheia transparente; o papel é do `index.html`; a câmera fica acima (z 20).
- Typing e count-up seek-safe (`onUpdate` só escreve quando o valor muda); `fromTo` sempre.
- Testar seek "a frio" (snapshot de um tempo isolado) em pops com blur: o bug do blur negativo só aparece assim.
- **No quadro exato de um corte, troca instantânea = `tl.set`.** Um tween de 0,001 s ali renderizou preto.
- Sincronizar vídeo derivado (ex.: o resultado de uma ferramenta de IA feito a partir de um take seu) por
  correlação do envelope de áudio com o take original (no exemplo, corr 0,98 → offset exato); depois o ORIGINAL usa
  o take com `data-media-start = início do pedaço + tempo local`, e os dois cards mostram o mesmo gesto no mesmo tempo.
- **Duração de SFX** limitada ao tamanho do arquivo (senão o runtime avisa).
- Sobreposição intencional (ex.: lista desfocada atrás de um card): marcar com `data-layout-ignore` para o `check`
  não acusar.
- **`index.html` e `compositions/captions.html` são gerados** pelos scripts: rodar de novo apaga o que foi ajustado
  à mão (ou no app) nesses dois arquivos. Ajuste os scripts, não o HTML gerado.
- Ao abrir o projeto no app desktop do HyperFrames, pare o preview em segundo plano (`npx --yes hyperframes@0.8.141 preview --stop`):
  só um editor escrevendo nos arquivos.

## 10. Fluxo de produção (ordem)

Tudo que é **medido** (tempo das palavras, cortes, posição do rosto, loudness) vem antes de qualquer motion. Assim o
storyboard marca cada animação em segundos exatos e os agentes que constroem as cenas não precisam adivinhar nada.

1. Ler BRIEF/roteiro, analisar a referência (§3) e o bruto (§4.1), inventariar materiais (§2). Começar mesmo com
   mídia pendente.
2. Projeto HyperFrames:
   `npx --yes hyperframes@0.8.141 skills update general-video` e
   `npx --yes hyperframes@0.8.141 init "<nome>" --non-interactive --example=blank --skill=general-video`. Versão fixada
   para o render ser reproduzível (no exemplo 2, todos os comandos rodaram como `npx --yes hyperframes@0.8.141 …` e os
   scripts do `package.json` foram fixados em `hyperframes@0.8.141`). As skills sempre vêm na versão mais nova (o
   `init` confere no GitHub): se o Claude sugerir um comando ou flag que a 0.8.141 não aceita, siga os comandos deste
   padrão. Criar `edit/`, `edit/audio/`, `edit/tools/`, `media/`, `reference/`, `renders/`; copiar os scripts do
   pipeline escolhido, `tools/`, `workflow-cenas.js`, `DESIGN.md`, as fontes e os SFX (§5).
3. Proxies (§4/§9) e áudio do alinhador. Pipeline B, um arquivo só:
   ```bash
   ffmpeg -i "$SRC" -vf "scale=1440:2560:flags=lanczos,format=yuv420p,tpad=stop_mode=clone:stop_duration=0.3" -r 30 \
     -c:v libx264 -preset medium -crf 17 -g 15 -keyint_min 15 -sc_threshold 0 -movflags +faststart \
     -af "highpass=f=75,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9,apad=pad_dur=0.25" \
     -c:a aac -b:a 192k -ar 48000 -t <duração + 0,27> media/take.mp4
   ffmpeg -i media/take.mp4 -ac 1 -ar 16000 edit/audio/take.wav
   ```
   (exemplo 2: original de 65,43 s → `-t 65.7`). Pipeline A: o mesmo para cada take, sem `tpad`/`apad`/`-t`.
4. Transcrever (§4.2), corrigir, montar `edit/segments.json`, alinhar (§4.3).
5. Cortes e rosto: pipeline A → `build_edl.py` (conferir `edge_db`) e `FACE`; pipeline B → `tools/cuts.py`,
   conferência visual, `CUTS`/`ZOOM`, `tools/face.swift`, `EYES`, `build_edl.py`.
6. Legendas: `build_captions.py` (blocos, destaques, modos).
7. `DESIGN.md` + `BRIEF.md` + `STORYBOARD.md` com a tabela de cenas e um bloco por cena: tempo global, duração,
   receitas citadas, cues (cada palavra com o seu tempo **local** da cena, ex.: `pagaria@1.59`) e cada batida com
   geometria exata. O storyboard é o contrato: é ele que permite vários agentes trabalharem em paralelo e tudo
   encaixar. Cenas com transição entre si são construídas pelo mesmo agente.
8. `index.html` (câmera, enquadramento, punch-ins, tela cheia, SFX) via `build_index.py`; snapshot para calibrar o
   enquadramento (olhos na mesma altura em todos os cortes, plano B depois de cada corte, tela cheia abrindo/fechando).
9. Cenas: `edit/workflow-cenas.js` (Workflow do Claude Code; você liga pedindo explicitamente para usar um
   workflow, só nesta etapa; evite "ultracode", que liga workflows para a sessão inteira). O script não é editado:
   projeto, pasta do kit e grupos de cenas entram como args (§12). Em pipeline: cada grupo de 2–3 cenas tem um
   **construtor** (lê DESIGN → storyboard → §7 e §9 deste padrão → a cena-exemplo que adapta e as receitas dela;
   verifica com lint e 12–20 snapshots por cena) e depois um
   **revisor adversarial** de contexto limpo (parte do princípio de que há bugs; snapshots a cada 0,15–0,25 s + um
   em cada palavra-chave; seeks a frio; lista de verificação: batida no tempo da palavra, nada na emenda, anéis
   abraçando o alvo, blur preso, holds mortos > 1 s, saídas antes do fim, texto estourando, vídeos certos e
   sincronizados, cara de template barato, storyboard completo e, no workflow do kit, honestidade de conteúdo;
   corrige direto no arquivo e prova com novos snapshots).
   Custa caro: no exemplo 2, 10 agentes, 647 chamadas de ferramenta, ~42 min, 905 snapshots.
   Os revisores pegam bugs reais: blur preso, anéis desalinhados, holds mortos, texto sobre a emenda, contador que
   empurra o layout, vídeo de card com o rosto saindo do quadro, placeholders vazando.
10. `python3 edit/tools/collect_sfx.py <journal.jsonl do workflow>` → `python3 edit/build_index.py` (SFX entram;
    `DROP` nos empilhados) → `npx --yes hyperframes@0.8.141 check` = 0 erros / 0 avisos / contraste AA (um aviso transitório num
    quadro de fade pode ser aceito, se você conferir).
11. Revisão própria, como espectador: `npx --yes hyperframes@0.8.141 render -q draft -o renders/<nome>-draft1.mp4` e folhas de
    contato a 2 quadros/s só do palco, 8 s por folha:
    `ffmpeg -ss 0 -t 8 -i renders/<nome>-draft1.mp4 -vf "fps=2,crop=1080:1180:0:740,scale=240:-1,tile=8x2:padding=3:color=white" -frames:v 1 folha_0.png`.
    Procure lado vazio, hold morto, conteúdo que insinua algo falso. Corrija, rode o `check` de novo.
12. Preview no Studio (`npx --yes hyperframes@0.8.141 preview --background`) → render
    `npx --yes hyperframes@0.8.141 render -q delivery -f 30 --no-best-effort -o renders/<nome>-v1.mp4` (`--no-best-effort` faz o
    render falhar se alguma mídia não estiver pronta, em vez de sair com um quadro faltando) → verificar o
    **arquivo final**: `ffprobe` (1080×1920, 30 fps, duração, áudio 48 kHz), `ffmpeg -i <mp4> -af ebur128=peak=true -f null -`
    e quadros-chave extraídos do MP4 (inclusive o último, que não pode ser preto) → enviar o MP4.

## 11. Checklist final de qualidade

- [ ] Todo corte com borda ≤ −40 dB; nenhuma palavra comida; nenhuma respiração longa (pipeline A).
- [ ] Todos os cortes do arquivo encontrados e conferidos no olho; timeline 1:1 com o original (pipeline B).
- [ ] Enquadramento alterna A/B; olhos na mesma altura em todos os cortes; nenhum topo de cabeça cortado no A.
- [ ] Legenda: 1 linha, sem sobreposição entre blocos, destaque lima ≈ 1 a cada 3 s, legível sobre B-roll; nada
      de texto escuro sobre o vídeo nem branco sobre o papel nas trocas de modo.
- [ ] Cada cena tem algo acontecendo **na palavra** que ela ilustra; nenhum hold morto > 1 s.
- [ ] Nenhum texto da cena na faixa 800–920; nada importante abaixo de 1700.
- [ ] Números só os que estão no print/roteiro; ressalva escrita onde houver conta ("cálculo ilustrativo").
- [ ] **Honestidade de conteúdo**: nada que insinue que uma pessoa ou marca real faz/recebe algo que você não pode
      confirmar (ex.: vídeos de criadores reais dentro da interface de uma marca, ou ao lado de valores em dinheiro);
      comentaristas e @ inventados num mock de comentários: confirmar ou trocar.
- [ ] Fresh-seek nos pops com blur; saídas terminam antes do fim da cena; continuidade entre cenas (handoff).
- [ ] `check` 0/0, contraste AA; −14 LUFS ±1, pico ≤ −1 dBFS.
- [ ] Mídia pendente trocada e sincronizada; handle/@ do CTA confirmado; #publi se for parceria paga.
- [ ] Arquivo final verificado (ffprobe, ebur128, quadros extraídos, último quadro não preto).

## 12. Template (`template-reel/`): o que mudar a cada vídeo

Copie para o projeto: os 4 scripts do pipeline escolhido em `<projeto>/edit/`, `tools/` em `<projeto>/edit/tools/`,
`workflow-cenas.js` em `<projeto>/edit/`, `DESIGN.md` na raiz, `fonts/*.woff2` em `<projeto>/assets/fonts/`.
Cada script tem no topo um bloco `# ===== EDITE AQUI =====` com o que muda e de onde vem cada valor.

| Arquivo | O que mudar no próximo vídeo |
|---|---|
| `edit/*/align.py` | `NUM` (grafia fonética dos nomes próprios e siglas do roteiro); lê `edit/segments.json` e `edit/audio/*.wav` |
| `edit/takes-brutos/build_edl.py` | `CLIP_FILE`, `ORDER` (ordem dos blocos, tentativa escolhida), `KEEP` (pausas intencionais), `TAIL`, `DISPLAY` |
| `edit/takes-brutos/build_captions.py` | `CHUNKS` (lista manual), `HL` + `HL_JANELA` (destaques), `BROLL_END`/`BROLL_HIDE`, `FULL`/`FULL_HIDE` |
| `edit/takes-brutos/build_index.py` | `FACE` (medir por take), `FULL`, `SCENES` (início/duração), `PUNCH`, `SFX`, `DROP` |
| `edit/take-cortado/build_edl.py` | `TOTAL`, `CUTS` (de `tools/cuts.py` + olho), `ZOOM`, `EYES` (de `tools/face.swift`), `DISPLAY`, `SKIP` |
| `edit/take-cortado/build_captions.py` | `CHUNK_TEXT` (lista manual), `HL_AT` (destaques pelo tempo), `BROLL_END`, `FULLS` |
| `edit/take-cortado/build_index.py` | `EYE_MEAN_Y`, `FULLS`, `GRADE`, `SCENES`, `PUNCH`, `SFX`, `DROP` |
| `edit/tools/cuts.py` · `face.swift` · `collect_sfx.py` | nada (cada um explica no topo como rodar e o que fazer com a saída) |
| `edit/workflow-cenas.js` | nada no arquivo: o projeto, a pasta do kit e os grupos de cenas entram como args |
| `DESIGN.md` | a tabela de assets do projeto; o resto só se a referência nova pedir outra linguagem |
| `STORYBOARD-exemplo.md`, `BRIEF-exemplo.md` | modelos: frame block (cues em tempo local, regras citadas, geometria exata) e brief |
| `scenes-exemplo/*.html`, `scenes-exemplo-2/*.html` | cenas prontas para adaptar; apontam para assets que **não** vêm no kit |
| `fonts/` | Geist e Geist Mono; SFX: ver §5 (não vêm no kit) |

Estrutura do projeto:

```
<projeto>/
├─ BRIEF.md · DESIGN.md · STORYBOARD.md       o contrato
├─ index.html                                 gerado por edit/build_index.py
├─ compositions/  captions.html (gerado) + uma cena por arquivo
├─ edit/  segments.json · align.py · build_edl.py · build_captions.py · build_index.py · workflow-cenas.js
│         tools/ · audio/ · words_source.json · edl.json · words.json · sfx_from_review.json
├─ media/  proxies da câmera
├─ assets/ fonts/ · sfx/ · img/ · broll/
├─ reference/  folhas da referência
├─ snapshots/ · renders/
```

## 13. O que mais pesa na qualidade

1. **Copiar uma referência real**: formato, paleta, caixa da legenda e entrada dos cards vêm da análise quadro a
   quadro, não de um "estilo de IA".
2. **Padrão escrito + template**: as decisões de estilo não são reabertas a cada vídeo.
3. **Tempo na palavra, medido**: alinhamento forçado (não o whisper); movimento começa 0,10 s antes da palavra.
4. **Medir em vez de chutar**: cortes pela diferença do fundo, rosto pelo Vision, loudness pelo ebur128, larguras de
   texto depois de a fonte carregar.
5. **O storyboard é um contrato**: geometria exata e estados de entrada/saída combinados.
6. **Código provado em vez de gerado do zero**: adaptar as cenas-exemplo.
7. **Revisão adversarial com quadros reais**: quem revisa não é quem construiu, olha PNGs reais (inclusive seeks a
   frio) e parte do princípio de que há bugs.
8. **Regras de segurança do render**: pop em dois canais, `fromTo` sempre, um wrapper por responsabilidade, nada
   aleatório. É o que faz o render bater com o preview.
9. **Edição invisível**: cortes viram troca de plano A/B, punch-ins nas palavras-chave, telas cheias nos momentos de
   conversa direta.
10. **Honestidade de conteúdo**: números só do print, ressalvas na tela, nada que insinue o que não é.
11. **Áudio no alvo** (−14 LUFS, pico abaixo de −1 dBFS, SFX no pico visual) e **verificar o arquivo final**, não
    só o preview.
