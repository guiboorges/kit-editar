# PROMPTS: edite um reel com o Claude Code, no mesmo nível do nosso

Estes são os prompts que você cola no **Claude Code** (aba **Code** do app Claude), **em ordem**, para editar um reel
de talking head com motion design, legenda karaokê e efeitos sonoros. É o mesmo processo que usamos no reel
"CLONE" (65 s, 11 cenas de motion, 108 blocos de legenda, 116 efeitos sonoros, −14 LUFS).

O formato de saída é este: **você em cima** (câmera), **legenda karaokê na emenda** e **motion design sobre papel claro
embaixo**, com uma cena para cada frase, batendo na palavra falada. Cores, fontes e a linguagem de motion seguem o
`DESIGN.md`, que o passo 1 adapta à sua referência. Mudar o **formato** (zonas da tela, posição da legenda, câmera
sempre em tela cheia) exige pedir ao Claude para adaptar também `build_index.py`, `build_captions.py` e o bloco
`COMMON` do `workflow-cenas.js`; o kit só foi testado no formato tela dividida.

> **Como usar este arquivo**
> - Cada passo tem um bloco **O PROMPT**. Copie o bloco inteiro e cole no Claude Code.
> - Tudo que estiver em `[COLCHETES E MAIÚSCULAS]` você troca pelo seu antes de colar.
> - Não pule a parte **Como conferir**. A qualidade vem justamente de conferir cada etapa antes de seguir.
> - O Claude vai pedir permissão para rodar comandos. Leia o que ele quer fazer e clique em permitir.

---

## Sumário

- [Antes de começar](#antes-de-começar)
- [Passo 0. Preparar a pasta e o projeto](#passo-0-preparar-a-pasta-e-o-projeto)
- [Passo 1. Analisar a referência e escrever o DESIGN.md](#passo-1-analisar-a-referência-e-escrever-o-designmd)
- [Passo 2. Analisar o vídeo bruto e escolher o pipeline](#passo-2-analisar-o-vídeo-bruto-e-escolher-o-pipeline)
- [Passo 3. Proxy, alinhamento forçado, cortes e enquadramento](#passo-3-proxy-alinhamento-forçado-cortes-e-enquadramento)
- [Passo 4. Legendas karaokê](#passo-4-legendas-karaokê)
- [Passo 5. BRIEF e STORYBOARD (o contrato)](#passo-5-brief-e-storyboard-o-contrato)
- [Passo 6. Câmera, index.html e snapshot de calibração](#passo-6-câmera-indexhtml-e-snapshot-de-calibração)
- [Passo 7. As cenas, com workflow multiagente](#passo-7-as-cenas-com-workflow-multiagente)
- [Passo 8. Revisão própria](#passo-8-revisão-própria)
- [Passo 9. Render final e verificação](#passo-9-render-final-e-verificação)
- [Passo 10. Ajustes finos no Studio ou no app HyperFrames](#passo-10-ajustes-finos-no-studio-ou-no-app-hyperframes)
- [Prompt único (atalho)](#prompt-único-atalho)
- [Checklist de qualidade](#checklist-de-qualidade)
- [Perguntas frequentes](#perguntas-frequentes)
- [De onde vem cada coisa](#de-onde-vem-cada-coisa)

---

## Antes de começar

### O que você precisa ter

| O quê | Para quê | Como instalar |
|---|---|---|
| **Um Mac com chip Apple** (M1, M2, M3…) | O kit foi feito e testado no macOS. **Em Mac Intel não funciona sem ajuste**: o alinhamento do passo 3 usa uma versão do PyTorch que só existe para chip Apple (veja "Meu Mac é Intel" nas [Perguntas frequentes](#perguntas-frequentes)). O passo que mede o seu rosto usa o Apple Vision, que só existe no Mac (veja as Perguntas frequentes se você usa Windows ou Linux). | Para saber: menu Apple → Sobre Este Mac → "Chip Apple M…" (ou "Processador Intel"). |
| **App Claude** com o **Claude Code** (aba Code), num **plano pago** que inclua o Claude Code | É quem faz todo o trabalho: lê os arquivos, roda os comandos, cria as cenas e revisa. Nós usamos o Claude Opus 5.5. | [claude.ai/download](https://claude.ai/download) |
| **Homebrew** | Instalador de programas pelo Terminal. | Siga [brew.sh](https://brew.sh). Ele pede a senha do Mac, então rode você mesmo, no app Terminal. Primeira vez no Terminal? Veja o quadro "Primeira vez no Terminal" no `LEIA-ME.md` (a senha não aparece enquanto você digita, e no fim é preciso rodar as linhas de "Next steps"). |
| **Node.js** | Para o comando `npx`, que roda o HyperFrames. | `brew install node` |
| **ffmpeg, whisper.cpp e uv** | Vídeo e áudio (ffmpeg/ffprobe), transcrição (whisper), Python isolado para o alinhamento (uv). | `brew install ffmpeg whisper-cpp uv` |
| **Ferramentas de linha de comando do Xcode** | Para compilar o script que mede o rosto (`swiftc`). Também trazem o `python3`. | `xcode-select --install` |
| **Skills do HyperFrames** | Ensinam o Claude a montar vídeo em HTML + GSAP e trazem a biblioteca de efeitos sonoros. | `npx --yes hyperframes@0.8.141 skills update general-video` (instala também o conjunto básico, com a `media-use`) |

Depois de instalar as skills, **feche e abra uma sessão nova** do Claude Code. Skills só são carregadas quando a sessão
começa.

Na primeira vez, alguns downloads grandes acontecem sozinhos (com a sua permissão): o modelo de transcrição do whisper
(`ggml-large-v3-turbo-q5_0.bin`, de huggingface.co/ggerganov/whisper.cpp), o Python 3.12, o PyTorch e o modelo de
alinhamento (via `uv`) e, no primeiro snapshot (passo 6), o navegador Chrome que o HyperFrames usa para tirar snapshots
e renderizar.

> **Quer que o Claude confira tudo isso para você?** Cole isto numa sessão nova:
> ```text
> Confira se tenho tudo para editar vídeo com HyperFrames: node e npx, ffmpeg, ffprobe, whisper-cli, uv, swiftc, python3,
> as skills do HyperFrames em ~/.claude/skills (hyperframes, general-video e media-use) e o modelo do whisper em
> ~/.cache/hyperframes/whisper/models/ggml-large-v3-turbo-q5_0.bin. Veja também se o Mac é chip Apple (uname -m deve
> dar arm64). Rode npx --yes hyperframes@0.8.141 doctor. No doctor, IGNORE: Version (usamos a 0.8.141 de propósito;
> não atualize), Docker, TTS (Kokoro) e BGM (MusicGen). Para este kit só importam Node.js, FFmpeg, FFprobe,
> whisper-cpp e Chrome. Me diga o que falta e como instalar. Não instale nem baixe nada sem me perguntar.
> ```

### Monte a pasta de trabalho

1. Crie uma pasta para os seus reels, por exemplo `Documentos/Reels`.
2. Copie para dentro dela **o conteúdo** da pasta `starter/` deste kit (não a pasta `starter` em si).
3. Crie uma pasta `materiais/` e coloque nela o seu material (lista abaixo).

Vai ficar assim:

```text
Reels/                          ← a pasta de trabalho: abra ESTA pasta no Claude Code
├─ PADRAO-DE-QUALIDADE.md       ← (do starter) as regras de qualidade
├─ RECEITAS-DE-MOTION.md        ← (do starter) 59 receitas de motion com números exatos
├─ template-reel/               ← (do starter) design, storyboard de exemplo, scripts, cenas prontas, fontes
├─ materiais/
│   ├─ bruto/                   ← seu(s) vídeo(s) gravado(s), em pé (9:16)
│   ├─ referencia/              ← o reel que você quer copiar (MP4)
│   ├─ prints/                  ← prints de sites, perfis, rankings, apps
│   ├─ broll/                   ← vídeos de apoio
│   └─ roteiro.txt              ← o texto do que você fala (ou .pdf)
└─ meu-reel/                    ← o projeto do vídeo, criado no passo 0
```

No app Claude, abra a aba **Code** e escolha a pasta `Reels` como pasta do projeto. Todos os prompts partem dela.

### O material que você precisa juntar

- [ ] **O vídeo bruto**, gravado em pé (9:16). Funciona de dois jeitos:
  - **vários takes crus** (um por bloco do roteiro, com 2 ou 3 tentativas cada, com pausas): o Claude corta a voz para você;
  - **um arquivo só, já cortado por você** (com os cortes que você mesmo fez): o Claude mantém a sua fala e só disfarça os cortes.
  Mesma luz, mesmo fundo e mesma roupa do começo ao fim ajudam muito.
- [ ] **Um reel de referência** para copiar o formato. Isto é o que mais pesa na qualidade: um visual copiado de um
  reel real fica muito melhor do que um "estilo de IA" genérico. Se você quer exatamente o nosso visual, o
  `template-reel/DESIGN.md` já é ele.
- [ ] **Prints** de tudo que você cita (site, ranking, perfil, app), de preferência em resolução 2× (tela retina),
  para não amolecer no zoom. **Todo número que aparecer na tela vai sair desses prints ou do roteiro.**
- [ ] **B-roll** (vídeos de apoio) que você tem direito de usar, e prints dos perfis se for dar crédito
  (`@perfil · N mil seguidores`).
- [ ] **O roteiro**, com os nomes próprios escritos certo (marcas, ferramentas, siglas). Ajuda muito na transcrição.
- [ ] **A palavra do CTA** ("comenta [PALAVRA] que eu te mando...") e o seu @.

Material faltando? Comece mesmo assim. O Claude deixa um espaço reservado e troca depois.

### Quanto tempo e quanto custa

- **No nosso caso**, com o padrão já escrito e o material pronto, foram **cerca de 1h15** da primeira análise até o v1.
  Na primeira vez, conte com bem mais: instalação, downloads e você conferindo cada etapa com calma.
- **A etapa pesada é o passo 7** (as cenas). No nosso reel ela usou **10 agentes** (5 construtores e 5 revisores), fez
  **647 chamadas de ferramenta**, tirou **905 snapshots** e levou **cerca de 42 minutos**. Isso consome **muito mais uso
  do seu plano** do que uma conversa normal. Se o seu plano tiver limite, ele pode acabar no meio da etapa. O passo 7
  mostra como reduzir esse custo.
- Renders no nosso Mac, para 65 s de vídeo: rascunho em 1 min 32 s, final em 2 min 29 s.

### Glossário rápido (as palavras que vão aparecer)

- **Talking head**: você falando para a câmera. **B-roll**: vídeos de apoio que aparecem enquanto você fala.
- **CTA**: a chamada final do vídeo ("comenta X que eu te mando...").
- **Pipeline**: o caminho que o seu vídeo segue. Pipeline A = `takes-brutos` = exemplo 1 (reel PERSONAGEM, 47,9 s):
  vários takes crus. Pipeline B = `take-cortado` = exemplo 2 (reel CLONE, 65,4 s): um arquivo que você já cortou.
- **HyperFrames**: ferramenta que monta o vídeo como uma página HTML animada (com GSAP) e a renderiza quadro a quadro para MP4.
- **Proxy**: uma cópia mais leve e fácil de editar do seu vídeo bruto. É ela que o vídeo final usa.
- **H.264 / HEVC**: formatos de vídeo. O iPhone grava em HEVC, que não toca bem no navegador; o proxy é H.264.
- **GOP / keyframe**: de quantos em quantos quadros o vídeo guarda uma imagem completa (o keyframe). GOP curto =
  pular na timeline sem travar.
- **EDL**: a lista de pedaços da câmera (de onde até onde cada um vai, e com qual enquadramento), no `edit/edl.json`.
- **Alinhamento forçado**: dado o texto certo e o áudio, achar o instante exato em que cada palavra começa e termina.
  É o que faz cada animação, legenda e efeito sonoro cair **na palavra**.
- **Jump cut / zoom cut**: corte dentro do mesmo plano. Mudar o tamanho do plano no corte (A 1,00× e B 1,10×) disfarça o pulo.
- **Punch-in**: zoom rápido na câmera para dar ênfase a uma palavra.
- **Snapshot**: um quadro do vídeo salvo como imagem (PNG) para conferir. **Folha de contato**: vários quadros numa grade.
- **Storyboard**: o roteiro visual. Aqui ele é um **contrato**: diz o que aparece, onde, de que tamanho e em que palavra.
- **Cue**: uma palavra com o seu tempo, escrita `palavra@segundo` (ex.: `pagaria@1.59`).
- **Tempo global × local**: global = segundos no vídeo inteiro; local = segundos desde o início da cena (o
  storyboard usa o local).
- **HOLD / handoff**: HOLD = a cena segura parada até o fim (por exemplo, enquanto a câmera cobre o palco). Handoff =
  o último quadro de uma cena é igual ao primeiro da seguinte, para a passagem não piscar.
- **Tween / easing**: uma animação de A para B, e a curva do movimento (`power3.out` = começa rápido e freia).
- **Wrapper**: uma caixa em volta de um elemento, só para carregar um tipo de movimento (a regra é um wrapper por
  responsabilidade).
- **Workflow**: um script que coordena vários agentes do Claude ao mesmo tempo (uns constroem, outros revisam). Ele só
  roda quando você pede explicitamente ("use um workflow"), e este kit só pede isso no passo 7. Existe também a
  palavra **"ultracode"**, que liga o modo de workflows para a sessão inteira (toda tarefa seguinte vira workflow e o
  gasto dispara): o kit **não** usa.
- **Seek**: pular direto para um instante do vídeo. O render faz isso a cada quadro, por isso as animações precisam
  estar certas em qualquer ponto ("seek-safe").
- **Hold morto**: mais de ~1 s sem nada se mexendo no palco.
- **LUFS**: volume percebido. O alvo usual das redes é −14 LUFS. **dBFS**: pico do sinal (0 é o máximo).
- **lint / check**: verificações automáticas do HyperFrames (estrutura, erros, layout, contraste).

---

## Passo 0. Preparar a pasta e o projeto

**Objetivo:** criar o projeto HyperFrames e fazer o Claude ler as regras antes de qualquer coisa.

**O PROMPT**

```text
Estou na minha pasta de trabalho de reels. Aqui tem PADRAO-DE-QUALIDADE.md, RECEITAS-DE-MOTION.md, a pasta
template-reel/ e a pasta materiais/ com o meu material. Vamos editar um reel no formato do template: câmera em cima,
legenda karaokê na emenda e motion design sobre papel claro embaixo, tudo batendo na palavra falada.
O processo é o do PADRAO-DE-QUALIDADE.md: não rode a entrevista de intenção da skill /hyperframes e não troque para
outro fluxo (como o /talking-head-recut).

1. Leia o PADRAO-DE-QUALIDADE.md inteiro. Ele é a regra de tudo o que vamos fazer neste vídeo e substitui a fase de
   "descobrir o visual". Leia também template-reel/DESIGN.md, template-reel/STORYBOARD-exemplo.md,
   template-reel/BRIEF-exemplo.md e o índice do RECEITAS-DE-MOTION.md.
2. Crie o projeto HyperFrames nesta pasta:
   npx --yes hyperframes@0.8.141 init "meu-reel" --non-interactive --example=blank --skill=general-video
   Use sempre essa mesma versão (npx --yes hyperframes@0.8.141 ...) em todos os comandos do HyperFrames daqui pra frente.
   Logo depois do init, crie meu-reel/BRIEF.md só com o cabeçalho (o trecho entre as linhas ---) do modelo em branco
   de template-reel/BRIEF-exemplo.md: workflow: general-video, flow: companion, destination, aspect "9:16" e
   language pt-BR (message e length ficam como no modelo). O resto do BRIEF é preenchido no passo 5.
3. Dentro de meu-reel/, crie as pastas media/, edit/audio/, edit/tools/, assets/fonts/, assets/img/, assets/broll/,
   assets/sfx/, reference/, analise/, ff/ e renders/.
   - Copie template-reel/fonts/*.woff2 para meu-reel/assets/fonts/.
   - Copie os efeitos sonoros (.mp3) de ~/.claude/skills/media-use/audio/assets/sfx/ para meu-reel/assets/sfx/.
     Se essa pasta não existir, pare e me avise (as skills do HyperFrames não estão instaladas).
   - Copie template-reel/edit/tools/* para meu-reel/edit/tools/.
   - Copie template-reel/DESIGN.md para meu-reel/DESIGN.md.
4. Faça um inventário de materiais/: para cada arquivo, tipo, duração, resolução e fps (ffprobe). Compare com o
   checklist de materiais do PADRAO-DE-QUALIDADE.md e me diga o que está faltando.

Regras: não edite nada fora de meu-reel/ (os arquivos do starter são o modelo e ficam intactos). Termine com um resumo
curto do que foi feito e do que falta.
```

**O que o Claude vai fazer**

```bash
npx --yes hyperframes@0.8.141 init "meu-reel" --non-interactive --example=blank --skill=general-video
mkdir -p meu-reel/{media,edit/audio,edit/tools,assets/fonts,assets/img,assets/broll,assets/sfx,reference,analise,ff,renders}
cp template-reel/fonts/*.woff2 meu-reel/assets/fonts/
cp ~/.claude/skills/media-use/audio/assets/sfx/*.mp3 meu-reel/assets/sfx/
cp template-reel/edit/tools/* meu-reel/edit/tools/
cp template-reel/DESIGN.md meu-reel/
# meu-reel/BRIEF.md: só o cabeçalho (workflow: general-video · flow: companion · aspect "9:16" · language: pt-BR)
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of default=nw=1 "<arquivo>"
```

**Como conferir**
- Existe a pasta `meu-reel/` com `index.html`, `package.json` e `hyperframes.json`, e um `meu-reel/BRIEF.md` só com o
  cabeçalho.
- `meu-reel/assets/sfx/` tem os `.mp3` (click, pop, ping, whoosh...) e `meu-reel/assets/fonts/` tem os dois `.woff2`.
- O inventário lista todos os seus arquivos e diz o que falta.

**Armadilhas**
- Se o Claude começar a fazer perguntas sobre o vídeo (público, estilo, "pitch", itens obrigatórios) ou sugerir outro
  fluxo, responda: *"Siga o PADRAO-DE-QUALIDADE.md; o BRIEF.md já tem o cabeçalho e o resto vem no passo 5."*
- Skills instaladas com a sessão aberta não aparecem: abra uma sessão nova do Claude Code.
- O `init` busca as skills no GitHub, então precisa de internet.
- Os caminhos das fontes no DESIGN.md e nos scripts são `assets/fonts/...`. Se as fontes não estiverem lá, o texto
  sai numa fonte genérica.

---

## Passo 1. Analisar a referência e escrever o DESIGN.md

**Objetivo:** transformar o reel de referência num documento de design (`DESIGN.md`) que todos os agentes vão seguir.

**O PROMPT**

```text
Agora analise o vídeo de referência: materiais/referencia/[ARQUIVO-DA-REFERENCIA].mp4. É o formato que eu quero copiar.
Não quero um "visual genérico de IA": quero o jeito dessa referência.

1. Faça folhas de contato a 2 quadros por segundo e salve em meu-reel/reference/:
   ffmpeg -i <referência> -vf "fps=2,scale=240:-1,tile=8x2:padding=4:color=white" meu-reel/reference/sheet_%02d.png
   Olhe todas as folhas.
2. Extraia quadros em resolução cheia dos momentos-chave e MEÇA (em pixels, num quadro 1080×1920): a altura da
   câmera e do palco, onde fica a legenda (caixa, tamanho, cor, quantas palavras por vez, minúsculas ou não), a paleta,
   a tipografia, como os cards entram e saem (blur? escala? de onde vêm?), como os números aparecem, como é o CTA e o
   ritmo (de quantos em quantos segundos algo muda no palco).
3. Veja se a referência tem trilha musical: rode ffmpeg -i <referência> -af ebur128 -f null -, meça um trecho sem
   fala (ebur128 ou astats) e me diga se parece haver trilha por baixo; eu confirmo ouvindo.
4. Compare com meu-reel/DESIGN.md (que veio do template) e reescreva-o para esta referência: zonas da tela, paleta,
   tipografia, superfícies, linguagem de motion e o contrato da sub-composição (o esqueleto HTML/GSAP que toda cena
   copia). Se a referência tiver o mesmo formato do template (câmera em cima, legenda na emenda, motion embaixo), mude
   só o que for diferente. Se o FORMATO da referência for diferente do template (outras zonas da tela, legenda em
   outro lugar, câmera sempre em tela cheia), PARE e me liste o que teria de mudar nos scripts (build_index.py,
   build_captions.py) e no bloco COMMON do workflow-cenas.js antes de reescrever o DESIGN.md. As regras técnicas do
   PADRAO-DE-QUALIDADE.md (seek-safe, pop em dois canais, um wrapper por responsabilidade, fromTo sempre, nada
   aleatório) continuam valendo seja qual for o visual.
5. Me mostre 3 ou 4 quadros da referência e, para cada um, a decisão correspondente no DESIGN.md. Depois, uma lista
   "o que mudou em relação ao template e por quê".
```

> Sem referência própria? Troque o prompt por: *"Não tenho referência. Use o meu-reel/DESIGN.md como está (é o visual
> do template) e só me mostre um resumo dele."*

**O que o Claude vai fazer**

```bash
ffmpeg -i ref.mp4 -vf "fps=2,scale=240:-1,tile=8x2:padding=4:color=white" reference/sheet_%02d.png
ffmpeg -ss 12.5 -i ref.mp4 -frames:v 1 reference/quadro_12.5.png      # quadros cheios nos momentos-chave
ffmpeg -i ref.mp4 -af ebur128 -f null -                                # volume e se há trilha (você confirma ouvindo)
```

**Como conferir**
- Abra as folhas em `meu-reel/reference/` e o `meu-reel/DESIGN.md`. As cores, a posição da legenda e o jeito como os
  cards entram descritos no DESIGN.md batem com o que você vê na referência?
- O DESIGN.md tem a seção do contrato da sub-composição (um esqueleto de código). Sem ela, as cenas saem inconsistentes.

**Armadilhas**
- "Inspirado em" vira genérico. Peça medidas (px, segundos, easing), não adjetivos.
- Se a referência tem música, anote. A música não vem no kit (veja as [Perguntas frequentes](#perguntas-frequentes)).

---

## Passo 2. Analisar o vídeo bruto e escolher o pipeline

**Objetivo:** medir o seu vídeo antes de editar (texto, volume, cortes) e decidir qual dos dois pipelines usar.

**O PROMPT**

```text
Agora analise o meu vídeo bruto em materiais/bruto/ (pode ser um arquivo só ou vários takes). O roteiro está em
materiais/roteiro.* (se existir). Trabalhe em meu-reel/analise/.

Para cada arquivo:
1. Ficha técnica com ffprobe (codec, resolução, fps, duração, áudio) e uma folha de contato a 1 quadro por segundo.
2. Transcrição: extraia o áudio em 16 kHz mono e rode
   whisper-cli -m ~/.cache/hyperframes/whisper/models/ggml-large-v3-turbo-q5_0.bin -l pt -f <audio.wav> --prompt "[NOMES PRÓPRIOS E SIGLAS DO SEU VÍDEO, SEPARADOS POR VÍRGULA]"
   (se o modelo não estiver nessa pasta, peça minha permissão e baixe ggml-large-v3-turbo-q5_0.bin de
   huggingface.co/ggerganov/whisper.cpp para lá). Corrija a transcrição comparando com o roteiro. Trechos duvidosos:
   recorte só aquele pedaço e transcreva de novo. Lembre: os tempos por palavra do whisper NÃO servem para corte nem
   para sincronia; do whisper só usamos o TEXTO.
3. Áudio: loudness com ebur128 e pausas com silencedetect=noise=-38dB:d=0.12. Diga se o áudio parece já processado
   (muito alto e comprimido, quase sem pausas).
4. Cortes: rode o scdet do ffmpeg (scale=270:-1,scdet=threshold=4) e olhe a folha de contato. Diga se o vídeo já vem
   cortado por mim (um arquivo com jump cuts e fala contínua) ou se são takes brutos (pausas, tentativas repetidas).
5. Escolha o pipeline e me explique por quê:
   - takes-brutos (template-reel/edit/takes-brutos/): vários takes crus; o script corta as pausas na voz e usa a
     melhor tentativa de cada bloco.
   - take-cortado (template-reel/edit/take-cortado/): um arquivo já cortado por mim; a voz NÃO é recortada de novo, a
     timeline fica 1:1 com o arquivo e cada corte meu vira uma troca de enquadramento.
   Copie os 4 scripts do pipeline escolhido (align.py, build_edl.py, build_captions.py, build_index.py) para
   meu-reel/edit/.
6. Me entregue: a ficha, a transcrição corrigida (marque as palavras que você mudou), as medidas de áudio e a decisão
   do pipeline. PARE e espere eu confirmar a transcrição antes de seguir.
```

**O que o Claude vai fazer**

```bash
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate,sample_rate,channels -of default=nw=1 "$SRC"
ffmpeg -i "$SRC" -vf "fps=1,scale=180:-1,tile=11x6:padding=4:color=white" -frames:v 1 analise/sheet.png
ffmpeg -i "$SRC" -ac 1 -ar 16000 analise/a16.wav
whisper-cli -m ~/.cache/hyperframes/whisper/models/ggml-large-v3-turbo-q5_0.bin -l pt -f analise/a16.wav --prompt "Nome1, Nome2, SIGLA"
ffmpeg -i "$SRC" -af ebur128 -f null -
ffmpeg -i analise/a16.wav -af silencedetect=noise=-38dB:d=0.12 -f null -
ffmpeg -i "$SRC" -vf "scale=270:-1,scdet=threshold=4" -an -f null -
```

**Como conferir**
- **Leia a transcrição inteira.** Nomes próprios são onde o whisper mais erra. No nosso vídeo ele escreveu "Claudio"
  no lugar de "Claude" e "em quem Sam Consciência" no lugar de "quem em sã consciência", mesmo com o `--prompt`.
- A decisão do pipeline faz sentido? Você sabe se exportou o vídeo já cortado ou não.

**Armadilhas**
- A transcrição errada contamina tudo depois (alinhamento, legendas, storyboard). Corrija agora.
- No nosso caso o áudio veio a −8,2 LUFS (alto e comprimido por um aprimorador de voz) e quase sem pausas: sinal de
  que o vídeo já vinha cortado. Isso mudou o plano inteiro.
- Vídeo de iPhone em HEVC não toca bem no navegador. Não tem problema: o proxy do próximo passo resolve.

---

## Passo 3. Proxy, alinhamento forçado, cortes e enquadramento

**Objetivo:** criar o arquivo de câmera leve (proxy), achar o tempo exato de cada palavra, fechar a lista de cortes e
medir onde está o seu rosto.

**O PROMPT**

```text
Transcrição confirmada. Agora proxy, alinhamento forçado, cortes e enquadramento, seguindo o pipeline escolhido
(os scripts estão em meu-reel/edit/; o que precisa mudar fica no bloco "EDITE AQUI" no topo de cada script, que vem
com valores de EXEMPLO do reel do kit: troque todos pelos meus). Trabalhe dentro de meu-reel/.

1. PROXY da câmera (o arquivo que o vídeo realmente usa): 1440×2560, 30 fps, H.264, GOP de 15 quadros (um keyframe a
   cada 0,5 s, senão o preview trava a cada salto), cadeia de voz do padrão com loudnorm em −14 LUFS e uma cauda de
   0,3 s para o último quadro não sair preto. Referência:
   ffmpeg -i "$SRC" -vf "scale=1440:2560:flags=lanczos,format=yuv420p,tpad=stop_mode=clone:stop_duration=0.3" -r 30 \
     -c:v libx264 -preset medium -crf 17 -g 15 -keyint_min 15 -sc_threshold 0 -movflags +faststart \
     -af "highpass=f=75,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120:makeup=2,loudnorm=I=-14:TP=-1.5:LRA=9,apad=pad_dur=0.25" \
     -c:a aac -b:a 192k -ar 48000 -t <duração do áudio + 0,27 s> media/take.mp4
   Take cortado: um proxy (media/take.mp4). Takes brutos: o mesmo comando para cada take (media/t1-....mp4 etc.), mas
   SEM tpad, apad e -t (a cauda só é necessária no take cortado). Depois, o WAV 16 kHz mono de cada proxy em
   edit/audio/ (o nome do arquivo é o "clip" do segments.json).
2. MÍDIA DE APOIO: B-roll recodificado em assets/broll/ (H.264, 30 fps, GOP curto -g 12 -keyint_min 12
   -sc_threshold 0, sem áudio; vertical em 720×1280) e prints em assets/img/. Atualize a tabela de assets do
   meu-reel/DESIGN.md: arquivo, tamanho em px, o que mostra e, nos prints, as regiões importantes em px
   (ex.: "linha do ranking: x 7–515, y 8–92").
3. ALINHAMENTO FORÇADO: escreva edit/segments.json com o texto corrigido, sem pontuação, em minúsculas, exceto nomes
   próprios e siglas. No dicionário NUM do edit/align.py, coloque números por extenso e uma grafia "fonética" para cada
   nome próprio ou sigla (ex.: "MCP": "emecepe", "Claude": "cloud"); no segments.json esses nomes ficam escritos
   exatamente como as chaves do NUM. Rode (na primeira vez SEM --offline, para baixar o que falta):
   uv run --offline --no-project -p 3.12 --with torch==2.5.1 --with torchaudio==2.5.1 --with numpy python edit/align.py
   Se este Mac for Intel (uname -m dá x86_64), troque por --with torch==2.2.2 --with torchaudio==2.2.2
   --with "numpy<2" e me avise que essa combinação não foi testada pelo kit. Me mostre as palavras com score baixo.
4. CORTES:
   - take cortado: ache os cortes que já existem comparando quadro a quadro só a parte de cima do fundo (parede,
     luminária), que não mexe quando eu gesticulo:
     ffmpeg -i media/take.mp4 -vf "scale=72:128,format=gray" -f rawvideo analise/g.raw && python3 edit/tools/cuts.py analise/g.raw
     Isso dá CANDIDATOS. Para cada um, monte um par "quadro antes / quadro depois" e olhe: só é corte se o fundo e a
     postura pulam; gesto de mão não conta. Cole os aprovados em CUTS no edit/build_edl.py e sugira 1 ou 2 "zoom cuts"
     (ZOOM) em respiros dentro de trechos longos.
   - takes brutos: configure CLIP_FILE, ORDER (a melhor tentativa de cada bloco), KEEP (pausas que são de propósito) e
     TAIL no edit/build_edl.py. Regra: pausa maior que 0,30 s só é cortada se tiver pelo menos 0,16 s de silêncio real;
     toda borda de corte precisa ficar em −40 dB ou menos (edge_db).
5. ROSTO MEDIDO, NÃO CHUTADO: extraia 3 quadros (a 20%, 50% e 80%) de cada trecho entre cortes (take cortado) ou de
   cada take (takes brutos) para ff/, em 1080×1920. Compile e rode o detector de rosto do macOS:
   swiftc -O edit/tools/face.swift -o face && ./face ff/*.png
   Cole a média dos olhos de cada trecho em EYES no edit/build_edl.py (take cortado) ou em FACE no
   edit/build_index.py (takes brutos, um valor por take). Os trechos de zoom cut herdam a medida do trecho de origem.
6. Antes, no take cortado, ponha em TOTAL (edit/build_edl.py) a duração do vídeo ORIGINAL:
   ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "materiais/bruto/<arquivo>"
   Rode python3 edit/build_edl.py e me mostre: a lista de peças (A/B alternando, início, duração e texto de cada uma)
   e os pares antes/depois que você usou para aprovar ou descartar cada corte. Se ele imprimir "AVISO: ... ainda tem
   o valor de EXEMPLO do kit", troque esse valor pelo meu e rode de novo.
```

**O que o Claude vai fazer**

```bash
ffmpeg -i "$SRC" -vf "scale=1440:2560:...,tpad=..." -r 30 -c:v libx264 -crf 17 -g 15 ... -af "highpass...,loudnorm=I=-14..." media/take.mp4
ffmpeg -i media/take.mp4 -ac 1 -ar 16000 edit/audio/take.wav
uv run --no-project -p 3.12 --with torch==2.5.1 --with torchaudio==2.5.1 --with numpy python edit/align.py   # → edit/words_source.json
ffmpeg -i media/take.mp4 -vf "scale=72:128,format=gray" -f rawvideo analise/g.raw && python3 edit/tools/cuts.py analise/g.raw
f=816; ffmpeg -i media/take.mp4 -vf "select='between(n,$((f-1)),$f)',scale=200:-1,tile=2x1" -fps_mode passthrough -frames:v 1 analise/par_$f.png
ffmpeg -v error -y -ss 12.3 -i media/take.mp4 -frames:v 1 -vf scale=1080:1920 ff/f_12.3.png     # 3 por trecho
swiftc -O edit/tools/face.swift -o face && ./face ff/*.png
python3 edit/build_edl.py    # → edit/edl.json (peças A/B) + edit/words.json (palavras na timeline)
```

**Como conferir**
- Olhe os pares antes/depois dos cortes. No nosso vídeo o script achou 23 candidatos; olhando os pares, 7 eram só
  gesto e foram descartados. Ficaram 16 cortes reais, todos em fronteira de frase.
- Na lista de peças, A e B se alternam e o texto de cada peça termina em fim de frase.
- Palavras com score muito baixo no alinhamento costumam ser nomes sem grafia fonética no NUM. Ajuste e rode de novo.

**Armadilhas**
- Os scripts **não leem sozinhos** a saída do `cuts.py` nem do `face`. Os valores são colados à mão no topo dos
  scripts: TOTAL, CUTS, ZOOM e EYES no `build_edl.py` (take cortado), FACE no `build_index.py` (takes brutos). Os
  scripts vêm com os valores do nosso reel como exemplo e avisam quando um deles continua lá
  (`AVISO: CUTS ainda tem o valor de EXEMPLO do kit; troque pelo seu`). Não siga em frente com esse aviso.
- Mac Intel: o comando do alinhador muda (veja "Meu Mac é Intel" nas [Perguntas frequentes](#perguntas-frequentes)).
- A primeira execução do alinhador baixa Python, PyTorch e o modelo: demora e precisa de internet.
- No take cortado, não deixe o Claude "limpar" pausas: a sua fala já está decupada, recortar de novo dá áudio picotado.

---

## Passo 4. Legendas karaokê

**Objetivo:** gerar a legenda da emenda: blocos curtos escritos à mão, palavra acendendo no tempo exato e destaques
em lima.

**O PROMPT**

```text
Agora as legendas karaokê: compositions/captions.html, gerado por edit/build_captions.py a partir de edit/words.json.
O words.json é escrito pelo edit/build_edl.py, então o que muda o TEXTO da legenda fica nele.

1. No edit/build_edl.py: configure DISPLAY com as siglas e a palavra do CTA em MAIÚSCULAS ([SIGLAS],
   [PALAVRA-DO-CTA]; tire os exemplos "ia", "mcp" e "clone" que não forem meus; o resto fica em minúsculas) e, no take
   cortado, SKIP com as muletas que eu falei mas não devem aparecer na legenda: [EX.: O "A" EM "COMENTA A PALAVRA"].
   Nos takes brutos não existe SKIP: adapte o build_edl.py e o build_captions.py para ter o mesmo efeito. Rode
   python3 edit/build_edl.py de novo antes de escrever os blocos (eles usam as palavras como ficaram no words.json).
2. Escreva os blocos À MÃO (CHUNK_TEXT no take cortado, CHUNKS no takes brutos). Não use divisão automática:
   1 a 3 palavras por bloco (até 4 em expressões como "o passo a passo"), até uns 18–22 caracteres, sempre uma linha,
   quebrando onde a minha voz quebra. Nunca termine um bloco em palavra fraca ("de", "o", "que", "e", "pra", "por"),
   a não ser onde a fala pedir.
3. Destaques em lima: mais ou menos 1 a cada 3 segundos, nas palavras que importam (o gancho, números, marcas, a
   prova, a palavra do CTA). No take cortado, HL_AT com o tempo exato de início de cada palavra. Nos takes brutos, HL
   pelas palavras (ele destaca TODAS as vezes em que a sequência aparece) + HL_JANELA para limitar as repetições a um
   intervalo de tempo.
4. Modos: "broll" (branca com sombra, sobre o B-roll do gancho), "paper" (tinta escura sobre o papel) e "full" (branca,
   mais embaixo, quando a câmera está em tela cheia). Proponha agora: até que segundo vai o B-roll do gancho
   (BROLL_END; nos takes brutos também BROLL_HIDE; 0 se não houver B-roll) e 1 ou 2 momentos de câmera em tela cheia,
   em frases de conversa direta comigo (tipo "e pensa comigo"): FULLS no take cortado; nos takes brutos, FULL +
   FULL_HIDE, e ali o script aceita exatamente UMA tela cheia (para nenhuma ou duas, adapte build_index.py e
   build_captions.py). Esses tempos valem também para a câmera no passo 6.
5. Rode python3 edit/build_edl.py && python3 edit/build_captions.py e me mostre a lista de blocos com tempo, modo e
   [destaques]. Se aparecer "AVISO: ... ainda tem o valor de EXEMPLO do kit", troque esse valor pelo meu e rode de novo.
```

**O que o Claude vai fazer**

```bash
python3 edit/build_edl.py && python3 edit/build_captions.py    # words.json (DISPLAY/SKIP) → compositions/captions.html;
                                                              # imprime cada bloco com tempos, modo e [destaques]
```

**Como conferir**
- Leia a lista de blocos em voz alta junto com o vídeo. Cada bloco tem que soar como uma unidade da sua fala.
- Os destaques estão espaçados (não 3 seguidos, não 10 segundos sem nenhum)?

**Armadilhas**
- No nosso primeiro teste, a divisão automática gerou blocos ruins ("e" sozinho, "eu" sozinho). Por isso a lista é manual.
- Mudou DISPLAY ou SKIP? Rode o `build_edl.py` antes do `build_captions.py`; senão a legenda não muda.
- O script confere palavra por palavra se os blocos batem com o áudio. Se der erro, é porque a lista pulou ou repetiu
  uma palavra.
- Nas trocas de modo, a legenda tem que sair antes da borda da câmera passar por ela; senão aparece texto escuro sobre
  o vídeo ou texto branco sobre o papel. Confira isso nos snapshots do passo 6.

---

## Passo 5. BRIEF e STORYBOARD (o contrato)

**Objetivo:** escrever o que cada cena mostra, em que palavra, onde e de que tamanho, para que os agentes do passo 7
trabalhem em paralelo sem precisar adivinhar nada.

**O PROMPT**

```text
Agora o contrato do vídeo: complete meu-reel/BRIEF.md (o cabeçalho já existe desde o passo 0: mantenha) e escreva
meu-reel/STORYBOARD.md. Use template-reel/BRIEF-exemplo.md e
template-reel/STORYBOARD-exemplo.md como modelo de formato. As cenas prontas para adaptar estão em
template-reel/scenes-exemplo/ e template-reel/scenes-exemplo-2/, e as receitas delas no RECEITAS-DE-MOTION.md.

BRIEF.md: a mensagem do vídeo numa frase, o destino (Reels/TikTok, 9:16), a duração, os materiais e de onde veio cada
um, as decisões (telas cheias, números permitidos) e tudo o que você inferiu sem eu confirmar.

STORYBOARD.md:
- Uma tabela no topo: cada cena com id (s1-..., s2-...), tempo global, duração, o que é falado, o que aparece no palco
  e de qual cena-exemplo ela é adaptada. As cenas começam e terminam nos cortes ou nas fronteiras de frase.
- TODA frase tem uma referência visual no palco, batendo na palavra.
- Um bloco por cena (status, id, src, global_start, duration, rules, cues) e, depois, cada batida com geometria exata:
  posição, tamanho, fonte, easing, estado de entrada e de saída. "cues" = cada palavra com o seu tempo LOCAL na cena
  (palavra@segundos desde o início da cena), tirado de edit/words.json. O movimento começa ~0,10 s antes da palavra
  para chegar no pico exatamente nela.
- Cenas que passam uma para a outra: descreva o último quadro de uma e o primeiro da outra (handoff). Cenas que ficam
  embaixo da câmera em tela cheia: HOLD (seguram até a câmera cobrir o palco).
- Uma seção de regras universais (do PADRAO-DE-QUALIDADE.md): nada da cena na faixa da legenda (y 800–920), texto
  importante dentro de x 70–1010 e y 950–1680, pop em dois canais (nunca blur num easing que passa do ponto), um
  wrapper por responsabilidade, fromTo sempre, repetições finitas, nada aleatório, vídeo dentro de card com a caixa no
  aspecto nativo.
- NÚMEROS NA TELA: SÓ os que estão nos prints ou no roteiro. Nenhum dado inventado. Se houver conta, escreva a ressalva
  na tela (ex.: "cálculo ilustrativo").
- HONESTIDADE: não coloque criadores ou perfis reais ao lado de dinheiro, de uma marca ou de uma interface de um jeito
  que sugira algo que não é verdade. Marque com CONFIRMAR tudo o que for inventado ou não confirmado (comentaristas de
  um mock, o @ do CTA, parcerias).
- O CTA é "comenta [PALAVRA-DO-CTA]" e o meu @ é [SEU-@].

Me mostre a tabela e a lista do que está marcado como CONFIRMAR. Espere a minha aprovação antes de construir qualquer cena.
```

**O que o Claude vai fazer:** lê `edit/words.json`, `edit/edl.json`, o `DESIGN.md`, os prints e as cenas-exemplo, e
escreve os dois arquivos. Não roda comandos pesados.

**Como conferir**
- Leia a tabela do storyboard como se fosse o vídeo: cada frase tem um visual? O visual ajuda a entender a frase?
- Confira cada número que vai aparecer na tela contra o seu print.
- Resolva a lista CONFIRMAR agora (troque o que for inventado, confirme o seu @).

Exemplo de batidas reais do nosso storyboard (cena s4, resumida):

```text
cues: aí@0.06 ... existe@0.86 ... launchpoint@2.08 | que@2.70 só@2.80 aceita@2.90 vídeos@3.34 ... IA@4.08 | ... higgsfield@6.70
- 0.00  card da página já em cena, desfocado (blur 18px, opac .55) → fica nítido em "existe" (0.76–1.10)
- 1.98  pílula "Launchpoint" (logo 56px + Geist 700 44px) estoura sobre a borda do card + brilho lima
- 3.24  anel lima em "AI Videos ONLY"; 3.98 a pílula pisca lima em "IA"
- 6.60  anel lima + etiqueta "#1 · quem mais paga"; 6.90–7.70 SEGURA (a câmera cobre o palco)
```

**Armadilhas**
- Storyboard vago = cenas genéricas. Se uma batida diz "aparece um card bonito", peça posição, tamanho e palavra.
- Tempo global × local: o storyboard usa o tempo **local** da cena (segundos desde o início dela). Exemplo: uma palavra
  dita aos 18,60 s do vídeo, numa cena que começa em 11,90 s, tem cue local 6,70.
- No nosso vídeo, um revisor chegou a pôr vídeos de criadores reais dentro de uma interface de uma empresa, o que
  insinuava que o conteúdo deles era de lá. A regra de honestidade existe por isso.

---

## Passo 6. Câmera, index.html e snapshot de calibração

**Objetivo:** montar a composição principal (câmera, cenas provisórias, legendas) e conferir o enquadramento em
quadros reais antes de criar o motion.

**O PROMPT**

```text
Storyboard aprovado. Agora a câmera e a montagem principal: meu-reel/index.html, gerado por edit/build_index.py.

1. Configure no build_index.py: SCENES (id, início e duração de cada cena, iguais ao STORYBOARD.md), as janelas de
   tela cheia (FULLS no take cortado, FULL no takes brutos; abrir e fechar em 0,36 s power3.inOut), PUNCH (punch-ins de
   1,05× em palavras-chave, voltando ao normal no corte seguinte) e a cor (grade leve "skin-soft"). Os efeitos sonoros
   das cenas ainda não existem (o edit/sfx_from_review.json chega no passo 7); por enquanto o script segue só com os
   sons da câmera e avisa.
2. Crie um arquivo provisório compositions/<id>.html para cada cena do storyboard, seguindo o contrato de
   sub-composição do DESIGN.md (pode ser vazio), só para o index carregar.
3. Rode python3 edit/build_index.py e depois npx --yes hyperframes@0.8.141 lint.
4. Snapshot de calibração. Escolha tempos: 1 s; logo depois de 2 cortes (um enquadramento A e um B); a abertura e o meio
   de cada tela cheia; e um bloco de legenda de cada modo (broll, paper, full). Rode:
   npx --yes hyperframes@0.8.141 snapshot --at <tempos separados por vírgula> --no-end -o snapshots/cam-check --describe false
   Olhe os PNGs e confira: olhos na mesma altura em todos os cortes (≈ y 320 do painel da câmera), topo da cabeça não
   cortado no A, o vídeo cobrindo o painel inteiro, a tela cheia sem bordas, a legenda legível em cada modo.
5. Me mostre os snapshots e o que você ajustou.
```

**O que o Claude vai fazer**

```bash
python3 edit/build_index.py       # index.html: papel + brilho, cenas, câmera em camadas, legendas, SFX
npx --yes hyperframes@0.8.141 lint
npx --yes hyperframes@0.8.141 snapshot --at 1.0,6.0,19.45,19.9,24.5,58.6 --no-end -o snapshots/cam-check --describe false
```

**Como conferir**
- Abra os PNGs em `meu-reel/snapshots/cam-check/`. Os seus olhos estão na mesma altura em todos? O corte de A para B
  parece uma troca de câmera intencional?
- Na tela cheia, a legenda está branca e embaixo; na tela dividida, escura sobre o papel.

**Armadilhas**
- No take cortado, a câmera é montada em 5 camadas (recorte, tela cheia, punch-in, "respiração" lenta, enquadramento
  por peça), cada uma com uma só função. Se o Claude quiser animar tudo numa camada só, as animações brigam entre si.
- No take cortado, o `build_index.py` confere se o vídeo cobre o painel inteiro em todas as peças e para com erro se
  não cobrir. Quase sempre é a medida do rosto daquele trecho: refaça o item 5 do passo 3 para ele.

---

## Passo 7. As cenas, com workflow multiagente

**Objetivo:** construir todas as cenas de motion em paralelo e revisá-las com um segundo agente que procura erros em
quadros reais.

> **Atenção ao custo.** Esta é a etapa que mais consome uso do plano. No nosso reel: 10 agentes, 647 chamadas de
> ferramenta, 905 snapshots, ~42 minutos. Para controlar o gasto: rode só alguns grupos de cada vez ("rode só os grupos
> 1 e 2 agora"), ou use o plano B no fim desta seção, em que você acompanha e pode parar a cada cena.
>
> O workflow só roda quando **você pede explicitamente**: por isso o prompt diz "use um workflow". **Não escreva
> "ultracode"**: essa palavra liga o modo de workflows para a sessão inteira, e aí até os passos 8 a 10 virariam
> workflows (e o gasto dispara).
>
> O prompt usa o script do kit: `starter/template-reel/edit/workflow-cenas.js`, que na sua pasta de trabalho está em
> `template-reel/edit/workflow-cenas.js`. Ele traz os prompts dos construtores e dos revisores que usamos e **não é
> editado**: o Claude só monta os "args" (os caminhos e os grupos de cenas do seu storyboard) e roda.

**O PROMPT**

```text
Use um workflow para construir e revisar as cenas deste reel (só nesta etapa).

1. Copie template-reel/edit/workflow-cenas.js para meu-reel/edit/workflow-cenas.js SEM editar: tudo o que muda entra
   como args.
2. Monte os grupos a partir do meu STORYBOARD.md: 2 ou 3 cenas por grupo, e cenas que passam uma para a outra
   (handoff) ficam no mesmo grupo. Cada cena é {"id", "start", "dur", "adapt", "rec"}: id igual ao storyboard e ao
   SCENES do build_index.py; start = início global em s; dur = duração em s; adapt = a cena-exemplo que ela adapta,
   relativa a template-reel/ (ex.: "scenes-exemplo/s3-calc.html"); rec = a seção do RECEITAS-DE-MOTION.md (ex.:
   "s3-calc"), opcional.
3. Rode o Workflow com scriptPath = <caminho absoluto>/meu-reel/edit/workflow-cenas.js e args (objeto JSON, não
   texto) =
   {"project": "<caminho absoluto de meu-reel>",
    "kit": "<caminho absoluto desta pasta de trabalho>",
    "reference": "<caminho absoluto de materiais/referencia/[ARQUIVO-DA-REFERENCIA].mp4>",
    "groups": [[{"id": "...", "start": 0, "dur": 0, "adapt": "...", "rec": "..."}, ...], ...]}
   O script já usa npx --yes hyperframes@0.8.141 (arg "hyperframes", opcional).

O script já faz isto (não reescreva; só confira no resultado):
- Pipeline "construir → revisar" por grupo, sem barreira (o grupo que termina de construir já começa a ser revisado).
- CONSTRUTORES: leem, nesta ordem, DESIGN.md → o seu bloco do STORYBOARD.md → as seções de motion e de armadilhas
  técnicas do PADRAO-DE-QUALIDADE.md → a cena-exemplo que adaptam e as receitas dela. Adaptam código provado (os
  helpers, a estrutura de wrappers, os anéis e brilhos), não inventam do zero. Escrevem SÓ compositions/<id>.html, sem
  áudio. Verificam com lint e 12 a 20 snapshots por cena (no pico de cada batida, nos holds, na saída, no primeiro e no
  último quadro). Devolvem: resumo da cena, efeitos sonoros sugeridos (tempo GLOBAL, arquivo de assets/sfx/, volume) e
  notas de transição.
- REVISORES ADVERSARIAIS (outro agente, contexto limpo, um por grupo): partem do princípio de que HÁ bugs. Snapshots a
  cada 0,15–0,25 s da cena inteira, mais um em cada palavra-chave, mais seeks "a frio" (snapshots isolados no meio dos
  pops, onde o blur travado aparece). Conferem: (a) cada batida no tempo da palavra; (b) nada da cena na emenda
  800–920 e texto importante na área segura; (c) anéis e contornos abraçando o alvo; (d) blur preso, elemento
  meio-transparente por engano, piscada no início ou no fim; (e) hold morto > 1 s; (f) saídas antes do fim da cena
  (e HOLD segurando de verdade); (g) texto estourando a caixa, tamanho mínimo 24 px, contraste; (h) vídeos certos,
  enquadrados e sincronizados; (i) cara de template barato perto da referência; (j) storyboard completo; (k) honestidade
  de conteúdo: nenhum texto, @, nome, número ou asset sobrando das cenas-exemplo. Corrigem direto no arquivo, provam a
  correção com novos snapshots, rodam lint e devolvem: encontrado / corrigido / pendente e a lista FINAL de efeitos
  sonoros (tempo global).
- Regras para todos: cada um usa a sua própria pasta de snapshots; ninguém roda animation-map nem deixa processo rodando.

Antes de rodar, me mostre os args, quantos agentes vão rodar (2 por grupo) e quais grupos, e espere o meu OK.

Depois do workflow:
1. Junte os efeitos sonoros dos revisores: python3 edit/tools/collect_sfx.py <journal.jsonl do workflow>
   → edit/sfx_from_review.json (o build_index.py dos dois pipelines lê esse arquivo). Se algum som empilhar com outro
   na mesma batida, tire-o com DROP no build_index.py.
2. Rode python3 edit/build_index.py e npx --yes hyperframes@0.8.141 check.
3. Me mostre o relatório de cada revisor (encontrado / corrigido / pendente) e o resultado do check.
```

**O que o Claude vai fazer**

Os args que o Claude monta (exemplo com 2 grupos; no nosso reel foram 5 grupos, 11 cenas e 10 agentes). O script
`meu-reel/edit/workflow-cenas.js` fica como veio do kit:

```json
{
  "project": "/Users/SEU-USUARIO/Documents/Reels/meu-reel",
  "kit": "/Users/SEU-USUARIO/Documents/Reels",
  "reference": "/Users/SEU-USUARIO/Documents/Reels/materiais/referencia/referencia.mp4",
  "groups": [
    [ { "id": "s1-hook", "start": 0, "dur": 5.567, "adapt": "scenes-exemplo/s1-hook.html", "rec": "s1-hook" },
      { "id": "s2-dinheiro", "start": 5.567, "dur": 3.166, "adapt": "scenes-exemplo/s3-calc.html", "rec": "s3-calc" } ],
    [ { "id": "s3-cta", "start": 8.733, "dur": 6.0, "adapt": "scenes-exemplo/s8-cta.html", "rec": "s8-cta" } ]
  ]
}
```

```bash
npx --yes hyperframes@0.8.141 lint
npx --yes hyperframes@0.8.141 snapshot --at 12.0,12.9,13.95,14.5 --no-end -o snapshots/build-s4 --describe false
python3 edit/tools/collect_sfx.py <journal.jsonl>    # → edit/sfx_from_review.json
python3 edit/build_index.py
npx --yes hyperframes@0.8.141 check
```

**Como conferir**
- Leia o relatório dos revisores. No nosso reel eles pegaram, por exemplo: um contador que empurrava o texto a cada
  dígito, um "?" que aparecia por só 2 ou 3 quadros, uma pílula num azul diferente do print, um card parado (hold
  morto), um card translúcido deixando a lista de trás aparecer.
- Abra alguns snapshots dos revisores em `meu-reel/snapshots/review-*`.
- Os itens "pendente" viram tarefa do passo 8.

**Armadilhas**
- **Blur com easing que passa do ponto** (`back.out`): num seek o blur fica negativo e o elemento trava borrado. A
  regra é pop em dois canais: opacidade e blur num tween, escala em outro.
- **Vídeo dentro de card**: o render ignora `object-fit` dentro de caixas transformadas. A `<video>` precisa da caixa
  no aspecto nativo, dentro de um wrapper com `overflow:hidden`.
- Se o limite de uso do seu plano acabar no meio, espere renovar e peça "continue o workflow só com os grupos que
  faltam".
- Se a sua versão do Claude Code não tiver a ferramenta de workflow, o Claude vai avisar. Use o plano B abaixo.
- Depois do workflow, se o Claude continuar abrindo workflows sozinho, escreva *"sem workflow daqui pra frente"* ou
  abra uma sessão nova (veja a pergunta "Fechei o app no meio" nas [Perguntas frequentes](#perguntas-frequentes))
  antes do passo 8.

**Plano B (sem workflow: mais lento, mas você acompanha e pode parar a cada cena)**

```text
Não use workflow. Construa as cenas uma por vez, na ordem do storyboard, seguindo as mesmas regras de
template-reel/edit/workflow-cenas.js: para cada cena, primeiro construa (lendo DESIGN.md, o bloco do STORYBOARD.md, as
seções de motion e armadilhas do PADRAO-DE-QUALIDADE.md, a cena-exemplo e as receitas dela, verificando com lint e
snapshots); depois revise como se outra pessoa tivesse feito, com snapshots densos e seeks a frio, usando a lista de 11
itens do revisor, de (a) a (k). Me mostre os snapshots de cada cena antes de passar para a próxima.
```

---

## Passo 8. Revisão própria

**Objetivo:** assistir ao vídeo inteiro como espectador, achar o que os agentes deixaram passar e corrigir.

**O PROMPT**

```text
Agora revise o vídeo inteiro como espectador, não como programador.
1. Rode npx --yes hyperframes@0.8.141 check (lint + runtime + layout + motion + contraste) e corrija os erros.
2. Render rascunho: npx --yes hyperframes@0.8.141 render -q draft -o renders/meu-reel-draft1.mp4
3. Folhas de contato a 2 quadros por segundo só do palco, em blocos de 8 s, cobrindo o vídeo inteiro:
   ffmpeg -ss <início> -t 8 -i renders/meu-reel-draft1.mp4 -vf "fps=2,crop=1080:1180:0:740,scale=240:-1,tile=8x2:padding=3:color=white" -frames:v 1 analise/folha_<n>.png
   Olhe todas. Procure: hold morto (mais de ~1 s sem nada mexendo), metade do palco vazia, coisa fora de tempo, texto
   na emenda da legenda, cena que não ilustra a frase falada.
4. Conteúdo: algum número que não está nos prints ou no roteiro? Algum criador real ou marca associado a algo que não é
   verdade? Algo inventado ainda sem confirmação?
5. Áudio: meça o rascunho com ffmpeg -i renders/meu-reel-draft1.mp4 -af ebur128=peak=true -f null -
   Alvo: −14 LUFS (±1) e pico em −1 dBFS ou menos. Efeitos sonoros: no máximo 2 por batida, no pico visual; a duração
   de cada um não pode passar do tamanho do arquivo.
6. Corrija e me mostre, para cada correção, a folha de contato do trecho antes e depois. No fim, rode o check de novo.
```

**O que o Claude vai fazer**

```bash
npx --yes hyperframes@0.8.141 check
npx --yes hyperframes@0.8.141 render -q draft -o renders/meu-reel-draft1.mp4
ffmpeg -ss 0 -t 8 -i renders/meu-reel-draft1.mp4 -vf "fps=2,crop=1080:1180:0:740,scale=240:-1,tile=8x2:padding=3:color=white" -frames:v 1 analise/folha_0.png
ffmpeg -i renders/meu-reel-draft1.mp4 -af ebur128=peak=true -f null -
```

**Como conferir**
- **Assista ao rascunho no celular**, em tela cheia, com som. É assim que o seu público vai ver.
- Olhe as folhas antes/depois. No nosso reel, numa cena, o lado direito ficava vazio por ~1,5 s; a correção foram
  "chips" esperando e acendendo cada um na sua palavra.

**Armadilhas**
- Nosso rascunho mediu −15,0 LUFS (no limite). A correção foi renormalizar a voz no proxy para −14 e renderizar de novo.
- Avisos de contraste num único quadro de transição (algo entrando em fade) podem ser aceitos. Avisos que se repetem, não.
- Quatro efeitos sonoros empilhados na mesma batida viram barulho. Remova os excedentes.

---

## Passo 9. Render final e verificação

**Objetivo:** gerar o MP4 de entrega e conferir o arquivo final, não só o preview.

**O PROMPT**

```text
Render final e verificação do arquivo:
1. npx --yes hyperframes@0.8.141 render -q delivery -f 30 --no-best-effort -o renders/meu-reel-v1.mp4
2. Ficha do arquivo: ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,nb_frames,sample_rate -of default=nw=1 renders/meu-reel-v1.mp4
   Me diga codec, resolução, fps, número de quadros, duração, áudio e tamanho.
3. Volume: ffmpeg -i renders/meu-reel-v1.mp4 -af ebur128=peak=true -f null -
   Alvo: integrado −14 LUFS (±1), pico em −1 dBFS ou menos. Se estiver fora, renormalize a voz no proxy e renderize de novo.
4. Extraia uns 20 quadros-chave do MP4 final (incluindo o último, que não pode ser preto) e confira.
5. Passe pelo checklist final do PADRAO-DE-QUALIDADE.md item por item e me diga o que passou e o que não passou.
```

**O que o Claude vai fazer**

```bash
npx --yes hyperframes@0.8.141 render -q delivery -f 30 --no-best-effort -o renders/meu-reel-v1.mp4
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,nb_frames,sample_rate -of default=nw=1 renders/meu-reel-v1.mp4
ffmpeg -i renders/meu-reel-v1.mp4 -af ebur128=peak=true -f null -
```

**Como conferir:** o nosso v1 deu `h264 1080x1920 30/1`, `aac 48000 Hz`, −14,0 LUFS integrado e pico de −1,1 dBFS. O
seu deve dar 1080×1920, 30 fps, −14 LUFS (±1) e pico abaixo de −1 dBFS. Assista ao MP4 final inteiro, no celular.

**Armadilhas**
- `--no-best-effort` faz o render **falhar** se alguma mídia não estiver pronta, em vez de sair com um quadro faltando.
  Se falhar, leia o erro: geralmente é um arquivo com caminho errado.
- O Instagram não publica um valor oficial de loudness; −14 LUFS é o alvo usual das redes sociais.

---

## Passo 10. Ajustes finos no Studio ou no app HyperFrames

**Objetivo:** mexer você mesmo, visualmente, em detalhes (tempo de um elemento, um texto, uma posição) e renderizar o v2.

**O PROMPT**

```text
Quero fazer ajustes finos visualmente.
1. Abra o Studio do HyperFrames em segundo plano: npx --yes hyperframes@0.8.141 preview --background
   e me passe o endereço (normalmente http://localhost:3002).
2. Se eu quiser usar o app desktop do HyperFrames (com o chat do Framey): primeiro pare o preview
   (npx --yes hyperframes@0.8.141 preview --stop) e depois rode npx --yes hyperframes@0.8.141 open . — só um editor
   escrevendo nos arquivos por vez.
3. Quando eu voltar do app para cá, rode npx --yes hyperframes@0.8.141 catch-up . antes de mudar qualquer coisa e me
   diga o que mudou.
4. Lembre: index.html e compositions/captions.html são GERADOS por edit/build_index.py e edit/build_captions.py. Se eu
   mudar algo nesses dois arquivos no Studio ou no app, não rode esses scripts de novo sem antes levar a mudança para
   dentro do script.
5. Quando eu disser "pode renderizar", gere renders/meu-reel-v2.mp4 com os mesmos parâmetros e verificações do passo final.
```

**O que o Claude vai fazer**

```bash
npx --yes hyperframes@0.8.141 preview --background    # Studio em http://localhost:3002
npx --yes hyperframes@0.8.141 preview --stop
npx --yes hyperframes@0.8.141 open .                  # abre no app desktop (chat com o Framey)
npx --yes hyperframes@0.8.141 catch-up .              # ao voltar: o que mudou no app
npx --yes hyperframes@0.8.141 render -q delivery -f 30 --no-best-effort -o renders/meu-reel-v2.mp4
```

**Como conferir:** no Studio, arraste a agulha da timeline pelos pontos que você ajustou. Depois do v2, refaça as
verificações do passo 9.

**Armadilhas**
- O app desktop é baixado em hyperframes.dev/studio/download.
- Ajustar à mão o `index.html` ou o `captions.html` e depois rodar `build_index.py` ou `build_captions.py` **apaga** o
  ajuste. Peça ao Claude para colocar a mudança no script.

---

## Prompt único (atalho)

Para quem já fez o processo uma vez e quer rodar tudo de uma vez. O Claude para nos pontos de conferência. Ainda vale
fazer o "Antes de começar" e montar a pasta de trabalho primeiro. O atalho **não** usa workflow: na etapa das cenas
ele para, e você cola o [Passo 7](#passo-7-as-cenas-com-workflow-multiagente).

```text
Vamos editar um reel do começo ao fim, seguindo o PADRAO-DE-QUALIDADE.md desta pasta. Estou na minha pasta de trabalho:
aqui tem PADRAO-DE-QUALIDADE.md, RECEITAS-DE-MOTION.md, template-reel/ (DESIGN.md, STORYBOARD-exemplo.md,
BRIEF-exemplo.md, fontes, cenas-exemplo em scenes-exemplo/ e scenes-exemplo-2/, scripts em edit/takes-brutos/,
edit/take-cortado/ e edit/tools/, e o modelo de workflow edit/workflow-cenas.js) e materiais/ (bruto/, referencia/,
prints/, broll/, roteiro). Use sempre npx --yes hyperframes@0.8.141. Não edite nada fora de meu-reel/.

Dados do vídeo: nomes próprios e siglas = [NOMES]; palavra do CTA = [PALAVRA-DO-CTA]; meu @ = [SEU-@].

Etapas, nesta ordem (e PARE onde está escrito PARE):
0. Leia o PADRAO-DE-QUALIDADE.md inteiro, o template-reel/DESIGN.md e o STORYBOARD-exemplo.md (sem a entrevista de
   intenção da skill /hyperframes e sem trocar de fluxo: o processo é o do padrão). Crie o projeto com
   init "meu-reel" --non-interactive --example=blank --skill=general-video e, logo depois, meu-reel/BRIEF.md só com o
   cabeçalho do modelo em branco de template-reel/BRIEF-exemplo.md (workflow: general-video, flow: companion,
   destination, aspect "9:16", language pt-BR). Crie as pastas (media, edit/audio, edit/tools, assets/fonts,
   assets/img, assets/broll, assets/sfx, reference, analise, ff, renders), copie as fontes de template-reel/fonts/, os
   .mp3 de ~/.claude/skills/media-use/audio/assets/sfx/, template-reel/edit/tools/, e template-reel/DESIGN.md para
   meu-reel/DESIGN.md.
1. Referência: folhas de contato a 2 fps, quadros-chave medidos, trilha (ebur128 num trecho sem fala; eu confirmo
   ouvindo). Reescreva meu-reel/DESIGN.md para ela, mantendo as regras técnicas do padrão. Se o FORMATO for diferente
   do template, PARE e me liste o que teria de mudar nos scripts e no workflow.
2. Bruto: ficha (ffprobe), folha de contato, transcrição com whisper-cli (ggml-large-v3-turbo-q5_0, -l pt, --prompt com
   os nomes), loudness, silencedetect, scdet. Escolha o pipeline (takes-brutos ou take-cortado) e copie os 4 scripts
   dele para meu-reel/edit/. PARE: me mostre a transcrição corrigida e a escolha do pipeline.
3. Proxy 1440×2560, 30 fps, GOP 15, voz em −14 LUFS, cauda de 0,3 s; B-roll com GOP 12; prints em assets/img e tabela
   de assets no DESIGN.md (takes brutos: um proxy por take, sem tpad/apad/-t). Alinhamento forçado (segments.json +
   NUM fonético + align.py via uv; Mac Intel: torch 2.2.2). Cortes (cuts.py + pares antes/depois no take cortado;
   ORDER/KEEP/TAIL e bordas ≤ −40 dB nos takes brutos). Olhos medidos com face.swift. No take cortado, TOTAL = duração
   do vídeo original (ffprobe). build_edl.py, sem nenhum "AVISO: ... EXEMPLO do kit". PARE: me mostre os cortes
   aprovados e a lista de peças A/B.
4. Legendas: primeiro DISPLAY (siglas e a palavra do CTA em maiúsculas) e SKIP (muletas) no build_edl.py, rodado de
   novo; depois blocos à mão (1–3 palavras, ~18–22 caracteres, nunca terminar em palavra fraca), destaques lima ≈ 1 a
   cada 3 s (HL_AT no take cortado; HL + HL_JANELA nos takes brutos), modos broll/paper/full, 1 ou 2 telas cheias em
   frases de conversa direta (nos takes brutos o script aceita só uma). build_edl.py && build_captions.py.
5. BRIEF.md (complete; o cabeçalho já existe) e STORYBOARD.md no formato dos exemplos: toda frase com visual, cues por palavra em tempo local, geometria
   exata, handoffs, HOLD sob as telas cheias, números SÓ dos prints/roteiro, honestidade com criadores e marcas reais,
   CONFIRMAR em tudo o que for inventado. PARE: me mostre a tabela e a lista CONFIRMAR e espere a minha aprovação.
6. build_index.py (cenas provisórias, telas cheias, punch-ins, cor) + lint + snapshot de calibração (olhos na mesma
   altura, A/B, tela cheia, legenda em cada modo). Me mostre os snapshots.
7. Cenas: PARE antes desta etapa e me peça a mensagem do workflow (o Passo 7 do PROMPTS.md). Não abra nenhum
   workflow por conta própria. O Passo 7 já inclui o que vem depois (collect_sfx.py, build_index.py, check); quando
   ele terminar, siga do item 8.
8. Revisão própria: check, render draft, folhas de contato a 2 fps só do palco, conteúdo honesto, −14 LUFS, no máximo 2
   efeitos sonoros por batida. Corrija e me mostre antes/depois.
9. Render delivery -f 30 --no-best-effort, ffprobe, ebur128=peak=true, ~20 quadros do MP4 final (inclusive o último),
   checklist final do padrão item por item. PARE: me entregue o caminho do MP4 e o resultado do checklist.
```

---

## Checklist de qualidade

Use antes de publicar. Peça ao Claude: *"passe pelo checklist final do PADRAO-DE-QUALIDADE.md item por item"*.

**Câmera e cortes**
- [ ] Nenhuma palavra comida nos cortes; nenhuma respiração longa; bordas de corte em −40 dB ou menos (takes brutos).
- [ ] Enquadramento alterna A/B a cada corte; olhos na mesma altura em todos; topo da cabeça inteiro no A.

**Legenda**
- [ ] Sempre uma linha, sem dois blocos ao mesmo tempo; nunca termina em palavra fraca.
- [ ] Destaque lima mais ou menos a cada 3 s; legível sobre o B-roll e na tela cheia.

**Cenas**
- [ ] Cada cena tem algo acontecendo **na palavra** que ela ilustra; nenhum hold morto maior que 1 s.
- [ ] Nada da cena na faixa da legenda (y 800–920); nada importante abaixo de y 1700 (a interface do Reels cobre).
- [ ] Nenhum elemento travado borrado (seek a frio nos pops); saídas terminam antes do fim da cena; passagens entre
      cenas sem piscar.

**Conteúdo**
- [ ] Números só os dos prints ou do roteiro; ressalva escrita onde houver conta.
- [ ] Criadores e marcas reais sem associação que não é verdade; nada inventado sem você saber.
- [ ] O @ do CTA e a palavra do CTA conferidos; #publi se for parceria paga.

**Técnico**
- [ ] `check` sem erros (avisos só os transitórios que você aceitou conscientemente).
- [ ] −14 LUFS (±1), pico em −1 dBFS ou menos; no máximo 2 efeitos sonoros por batida, no pico visual.
- [ ] MP4 final conferido (ffprobe, ebur128, quadros extraídos, último quadro não preto) e assistido no celular.

---

## Perguntas frequentes

**Funciona no Windows ou no Linux?**
O kit foi feito e testado só no Mac. ffmpeg, whisper.cpp, uv, Node e o HyperFrames existem em outros sistemas, mas o
`face.swift` usa o Apple Vision, que é exclusivo do macOS. A alternativa: medir o rosto à mão. Peça ao Claude: *"extraia
um quadro de cada trecho com uma grade desenhada por cima (linhas a cada 5% da altura e da largura) e meça a linha dos
olhos e o centro do rosto em fração do quadro; use esses valores em EYES/FACE"*. Era assim que o template fazia antes do Vision.

**Meu Mac é Intel. E agora?**
O passo 3 (alinhamento das palavras) usa o PyTorch 2.5.1, que só tem versão para Mac com chip Apple. Num Mac Intel, peça
ao Claude: *"rode o align.py com --with torch==2.2.2 --with torchaudio==2.2.2 --with "numpy<2" no lugar das versões do
comando"*. O modelo de alinhamento (MMS_FA) existe desde o torchaudio 2.1, então deve funcionar, mas **não testamos
essa combinação**. Confira as palavras com score baixo com mais cuidado.

**E a música?**
O nosso reel saiu sem trilha (a referência tinha). Duas opções: adicionar uma trilha em alta direto no app do Instagram
na hora de publicar, ou mixar um arquivo seu por baixo da voz. Para a segunda, peça ao Claude para usar a skill
`/hyperframes-audio` e abrir espaço para a voz na música (o recurso que ela chama de "carve").

**Quanto custa?**
O kit é gratuito e as ferramentas que ele usa são gratuitas, exceto o Claude Code, que precisa de um plano pago do Claude. O que
mais pesa no uso do plano é o passo 7 (workflow com vários agentes). Para economizar: rode o workflow por partes ou use
o plano B do passo 7. Não temos uma medida de tokens para te passar; o que medimos foi o tamanho do trabalho
(10 agentes, 647 chamadas de ferramenta, ~42 min).

**E se o meu vídeo já vier cortado?**
É o pipeline **take-cortado** (foi o nosso caso). A voz não é recortada de novo: a timeline fica igual ao seu arquivo, e
cada corte seu vira uma troca de enquadramento A/B, que disfarça o pulo. O passo 2 detecta isso para você.

**Como mudo o estilo?**
Troque a referência e refaça o passo 1. Cores, fontes e a linguagem de motion seguem o `DESIGN.md`. Mudar o
**formato** (zonas da tela, posição da legenda, câmera sempre em tela cheia) exige pedir ao Claude para adaptar também
`build_index.py`, `build_captions.py` e o bloco `COMMON` do `workflow-cenas.js`: o kit só foi testado no formato tela
dividida. Se mudar a cor de destaque, ela também precisa mudar no `build_captions.py` (destaque da legenda) e no
`build_index.py` (brilho do papel). O que **não** deve mudar são as regras técnicas do padrão (seek-safe, pop em dois
canais, um wrapper por responsabilidade, números só dos prints). Elas são o que faz o render sair igual ao preview.

**Preciso saber programar?**
Não. Você precisa saber o que quer ver, conferir as etapas e dizer ao Claude o que está errado ("o anel está
desalinhado do botão aos 12 s", "esse card fica parado tempo demais"). Quanto mais específico, melhor o resultado.

**Fechei o app no meio. E agora?**
Abra uma sessão nova na mesma pasta de trabalho e cole: *"Estamos editando o reel em meu-reel/. Leia o
PADRAO-DE-QUALIDADE.md, o meu-reel/BRIEF.md, o meu-reel/DESIGN.md e o meu-reel/STORYBOARD.md (os que existirem), veja
quais arquivos já foram gerados e me diga em que passo paramos."*

**Algo deu errado e eu não entendi.**
Cole: *"Pare. Me explique em português simples o que deu errado, o que você já tentou e quais são as opções. Não apague
nada."*

**Posso usar uma versão mais nova do HyperFrames?**
Pode, mas este kit foi testado com a **0.8.141**. Para ver o que mudou: `npx hyperframes@latest upgrade --project . --check`
dentro de `meu-reel/`. Se algo quebrar, volte para a 0.8.141. Atenção: as **skills** do HyperFrames sempre vêm na
versão mais nova (o `init` confere no GitHub), mesmo com o comando fixado na 0.8.141. Se o Claude sugerir um comando
ou uma flag que a 0.8.141 não aceita, peça para ele seguir os comandos do PROMPTS.md.

**As cenas-exemplo aparecem com buracos quando eu abro.**
É normal. Elas apontam para arquivos (B-roll, prints) do nosso reel, que não vêm no kit. Elas servem como código para
o Claude adaptar, não como cenas prontas para usar.

---

## De onde vem cada coisa

| O quê | Origem |
|---|---|
| **HyperFrames** (CLI 0.8.141, Studio, app desktop com o Framey) | HeyGen, código aberto (Apache-2.0) · [hyperframes.heygen.com](https://hyperframes.heygen.com) · app: hyperframes.dev/studio/download |
| **Claude Code** | Anthropic · [code.claude.com/docs](https://code.claude.com/docs) |
| **GSAP 3.14** (todas as animações) | [gsap.com](https://gsap.com/docs/v3), carregado pelas composições via CDN |
| **Geist e Geist Mono** (fontes) | Vercel · SIL Open Font License (texto da licença em `template-reel/fonts/OFL.txt`) · [vercel.com/font](https://vercel.com/font) |
| **Efeitos sonoros** | Biblioteca da skill `media-use` do HyperFrames (`~/.claude/skills/media-use/audio/assets/sfx/`), sons do Pixabay sob a Pixabay Content License. **Não vêm no kit**: você os recebe ao instalar as skills. |
| **whisper.cpp** (transcrição) e o modelo `ggml-large-v3-turbo-q5_0.bin` | [github.com/ggml-org/whisper.cpp](https://github.com/ggml-org/whisper.cpp) · modelo em huggingface.co/ggerganov/whisper.cpp |
| **Alinhamento forçado** (MMS_FA) | torchaudio (PyTorch), rodando via [uv](https://docs.astral.sh/uv) |
| **FFmpeg / ffprobe** | [ffmpeg.org](https://ffmpeg.org) (filtros usados: scdet, silencedetect, ebur128, loudnorm, tpad) |
| **Detecção do rosto** | Apple Vision (`VNDetectFaceLandmarksRequest`), no `face.swift` |
| **Padrão, receitas, scripts e cenas-exemplo** | Extraídos dos nossos reels (exemplo 1, reel PERSONAGEM, e exemplo 2, reel CLONE), cujo formato veio da análise quadro a quadro do reel "Comenta PERSONAGEM" (@higgsfield.ai) |
