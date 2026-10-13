# LEIA-ME: kit de edição de reels com o Claude Code

Se você comentou **EDITAR** no meu reel, é este o material que eu prometi.

Com este kit, você edita um reel de talking head no mesmo nível do nosso: **você em cima**, **legenda karaokê** na
emenda e **motion design** embaixo, com uma cena para cada frase, cada animação, legenda e efeito sonoro batendo na
palavra falada. Quem faz o trabalho é o **Claude Code** (aba Code do app Claude) junto com o **HyperFrames**, uma
ferramenta que monta o vídeo como uma página animada e renderiza em MP4. Você cola os prompts em ordem, confere cada
etapa e aprova.

## O que tem no kit

```text
2-kit-para-seguidores/
├─ LEIA-ME.md                 ← este arquivo
├─ PROMPTS.md                 ← o passo a passo: os prompts para colar no Claude Code, em ordem
└─ starter/                   ← copie o CONTEÚDO desta pasta para a sua pasta de trabalho
    ├─ PADRAO-DE-QUALIDADE.md ← as regras de qualidade (formato, legenda, motion, áudio, checklist final)
    ├─ RECEITAS-DE-MOTION.md  ← 59 receitas de motion com números exatos (duração, easing, escala)
    └─ template-reel/
        ├─ DESIGN.md · STORYBOARD-exemplo.md · BRIEF-exemplo.md   ← modelos do design e do "contrato" das cenas
        ├─ fonts/              ← Geist e Geist Mono (+ licença OFL.txt)
        ├─ scenes-exemplo/     ← as 8 cenas do exemplo 1 (reel PERSONAGEM), para adaptar
        ├─ scenes-exemplo-2/   ← as 11 cenas do exemplo 2 (reel CLONE), para adaptar
        └─ edit/
            ├─ takes-brutos/   ← scripts para quando você grava vários takes crus (o Claude corta a voz)
            ├─ take-cortado/   ← scripts para quando você manda um arquivo já cortado por você
            ├─ tools/          ← detector de cortes, medidor do rosto (macOS) e coletor de efeitos sonoros
            └─ workflow-cenas.js ← o workflow com vários agentes que constrói e revisa as cenas
```

**Os mesmos nomes em todo o kit:** pipeline A = `takes-brutos` = exemplo 1 (reel PERSONAGEM, 47,9 s);
pipeline B = `take-cortado` = exemplo 2 (reel CLONE, 65,4 s). "Pipeline" é só o caminho que o seu vídeo segue: um
para vários takes crus, outro para um arquivo que você já cortou.

## Começo rápido

1. **Instale o básico no Mac** (veja "Primeira vez no Terminal" logo abaixo se nunca usou o Terminal): app Claude com
   Claude Code, [Homebrew](https://brew.sh), `brew install node ffmpeg whisper-cpp uv`, `xcode-select --install` e
   `npx --yes hyperframes@0.8.141 skills update general-video`.
2. **Monte a pasta de trabalho:** crie uma pasta (ex.: `Documentos/Reels`), copie para ela o conteúdo de `starter/`,
   crie `materiais/` e, dentro dela, `bruto/` (o seu vídeo), `referencia/` (o reel que você quer copiar), `prints/`,
   `broll/` e o `roteiro.txt`.
3. **Abra essa pasta na aba Code do app Claude.** Leia "Antes de começar" no `PROMPTS.md` e depois cole os passos
   0 a 10, conferindo cada etapa.

> **Primeira vez no Terminal**
> 1. Aperte **Cmd + Espaço**, digite **Terminal** e aperte **Enter**.
> 2. Copie um comando por vez, cole com **Cmd + V** e aperte **Enter**. Espere terminar antes do próximo.
> 3. Quando ele pedir a senha do Mac, digite e aperte Enter. **A senha não aparece enquanto você digita**: é normal.
> 4. No fim da instalação do Homebrew aparece **"Next steps"**: copie e rode as linhas que ele mostra. Num Mac com
>    chip Apple, são estas:
>    ```bash
>    echo >> ~/.zprofile
>    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
>    eval "$(/opt/homebrew/bin/brew shellenv)"
>    ```
>    Depois feche e abra o Terminal. Sem esse passo, o Mac responde `brew: command not found`.
> 5. Se preferir, depois que o Homebrew estiver instalado, peça ao Claude Code para rodar os `brew install` por você
>    (ele pede permissão antes de cada comando).

## Requisitos

- **Mac com chip Apple (M1, M2, M3…).** O kit foi feito e testado no macOS. Em **Mac Intel não funciona sem um
  ajuste**: o alinhamento das palavras (passo 3) usa uma versão do PyTorch que só existe para chip Apple (no
  `PROMPTS.md`, pergunta "Meu Mac é Intel" nas Perguntas frequentes). O medidor de rosto usa o Apple Vision, que só
  existe no Mac (no `PROMPTS.md` tem a alternativa manual para Windows/Linux).
- **App Claude com Claude Code**, num plano pago que inclua o Claude Code.
- **Node.js, Homebrew, ffmpeg, whisper.cpp, uv** e as **ferramentas de linha de comando do Xcode**.
- **Skills do HyperFrames** instaladas (`npx --yes hyperframes@0.8.141 skills update general-video`). Depois de
  instalar, abra uma sessão nova do Claude Code.
- **O "doctor" do HyperFrames vai mostrar alguns ✗ mesmo com tudo certo.** Ignore: Version (usamos a 0.8.141 de
  propósito; não atualize), Docker, TTS (Kokoro) e BGM (MusicGen). Para este kit só importam Node.js, FFmpeg,
  FFprobe, whisper-cpp e Chrome.
- **Internet na primeira vez:** o modelo de transcrição, o Python 3.12, o PyTorch e o modelo de alinhamento são
  baixados no primeiro uso (o Claude pede permissão), e também o navegador Chrome que o HyperFrames usa para tirar
  snapshots e renderizar (baixado no passo 6).
- **O seu material:** vídeo em pé (9:16), um reel de referência para copiar o formato, prints de tudo o que você cita,
  B-roll e o roteiro.

**Tempo e custo, com honestidade:** no nosso caso, com tudo pronto, foram cerca de 1h15 da primeira análise até a
primeira versão do vídeo. Na sua primeira vez, conte com mais. A etapa das cenas (workflow com 10 agentes, ~42 min) é
a que mais consome uso do seu plano; o `PROMPTS.md` explica como controlar esse gasto.

## O que NÃO vem no kit, e por quê

| Não vem | Por quê | Como conseguir |
|---|---|---|
| **Os efeitos sonoros (.mp3)** | São do Pixabay, sob a Pixabay Content License: dá para usar dentro dos seus vídeos, mas não para redistribuir os arquivos soltos. | Eles já vêm com as skills do HyperFrames. Depois de instalar, ficam em `~/.claude/skills/media-use/audio/assets/sfx/`, e o passo 0 copia de lá para o seu projeto. |
| **As minhas gravações** | São o meu rosto e a minha voz; o seu vídeo vai ser você. | — |
| **B-roll, prints e o reel de referência que eu usei** | São conteúdo de outras pessoas e empresas (perfis do Instagram, sites, o reel da Higgsfield); não tenho direito de redistribuir. Nas cenas-exemplo, os @ dos criadores viraram marcadores (`@criador_1`, `@criador_2`). | Junte os seus. Use só o que você tem direito de usar e dê o crédito na tela. |
| **O modelo de transcrição, o PyTorch e o modelo de alinhamento** | Arquivos grandes, com fontes oficiais. | São baixados no primeiro uso (passos 0 a 3). |
| **App desktop do HyperFrames** (opcional, passo 10) | É um programa à parte, só para ajustes visuais no fim. | hyperframes.dev/studio/download |

Como o B-roll e os prints não vêm, as **cenas-exemplo** aparecem com buracos (sem os vídeos e as imagens) se você
abrir direto. Elas são código para o Claude adaptar ao seu vídeo, não cenas prontas.

## Uma regra antes de começar

Números na tela só os que estão nos seus prints ou no seu roteiro, e nada de associar criadores ou marcas reais a algo
que não é verdade. O `PROMPTS.md` já pede isso ao Claude em todos os passos que importam. Confira mesmo assim.

Bom vídeo! Se usar o kit, me marca. Quero ver o resultado.
