# Kit EDITAR — reels com motion editados por IA

**Os prompts, em ordem, para editar um reel de talking head com motion design, legenda karaokê e efeitos sonoros, cada um batendo na palavra falada — usando o Claude Code e o HyperFrames.**

**[▶ Abrir o site do kit](https://kit-edit.vercel.app)** · **[⬇ Baixar o kit (.zip, 375 KB)](https://kit-edit.vercel.app/kit-reel-ia.zip)**

![Site do Kit EDITAR](docs/screenshots/site.png)

## O que é

Criei este kit para quem comentou **EDITAR** num reel meu no Instagram. É o mesmo processo que usei para editar os meus reels: **você em cima**, **legenda karaokê** na emenda e **motion design** embaixo, com uma cena animada para cada frase.

Quem faz o trabalho pesado é o **[Claude Code](https://claude.ai/download)** junto com o **[HyperFrames](https://hyperframes.heygen.com)**, uma ferramenta que monta o vídeo como uma página animada e renderiza em MP4. A pessoa cola os prompts em ordem, confere cada etapa e aprova.

## Como funciona

São 11 prompts, do passo 0 ao 10:

| Passo | O que acontece |
|---|---|
| 0 | Preparar a pasta e o projeto |
| 1 | Analisar o reel de referência e escrever o `DESIGN.md` (cores, tipografia, ritmo) |
| 2 | Analisar o vídeo bruto e escolher o pipeline (vários takes crus ou um arquivo já cortado) |
| 3 | Proxy, alinhamento forçado palavra a palavra, cortes e enquadramento do rosto |
| 4 | Legendas karaokê |
| 5 | Brief e storyboard: o "contrato" de cada cena |
| 6 | Câmera, `index.html` e snapshot de calibração |
| 7 | As cenas, construídas e revisadas por um workflow com vários agentes |
| 8 | Revisão própria |
| 9 | Render final e verificação (formato 9:16, áudio a −14 LUFS) |
| 10 | Ajustes finos no Studio do HyperFrames |

O exemplo do kit tem **65 segundos, 11 cenas e 108 legendas**.

## O que tem neste repositório

```text
site/                        o site publicado na Vercel (página única com botão de copiar cada prompt)
kit/
├─ LEIA-ME.md                comece por aqui
├─ PROMPTS.md                o passo a passo, prompt a prompt
└─ starter/
   ├─ PADRAO-DE-QUALIDADE.md regras de formato, legenda, motion e áudio + checklist final
   ├─ RECEITAS-DE-MOTION.md  59 receitas de motion com números exatos (duração, easing, escala)
   └─ template-reel/
      ├─ DESIGN.md · BRIEF-exemplo.md · STORYBOARD-exemplo.md
      ├─ scenes-exemplo/     8 cenas do exemplo 1, para adaptar
      ├─ scenes-exemplo-2/   11 cenas do exemplo 2, para adaptar
      ├─ fonts/              Geist e Geist Mono (licença OFL)
      └─ edit/               scripts de alinhamento, cortes, legendas, enquadramento e o workflow das cenas
```

## Como foi feito

O kit foi montado e testado por um **workflow com 7 agentes de IA** (~49 minutos):

- **3 construtores:** um para a pasta starter, um para os prompts e um para o roteiro do reel.
- **2 verificadores adversariais:** um seguiu o kit do zero como um iniciante e rodou todos os scripts; o outro conferiu fatos, tempos e o tom do texto.
- **2 corretores**, que aplicaram o que os verificadores encontraram.

Os scripts do kit, com os valores originais, reproduzem exatamente os arquivos dos reels de exemplo.

## Requisitos

- Mac com chip Apple (M1, M2, M3…)
- Plano pago do Claude, com Claude Code
- Homebrew, Node, ffmpeg, whisper.cpp, uv e as skills do HyperFrames (o `LEIA-ME.md` explica tudo, inclusive para quem nunca abriu o Terminal)

## O que não vem no kit (de propósito)

- **Efeitos sonoros:** a licença do Pixabay permite usá-los em vídeos, mas não redistribuir os arquivos. Quem instala o HyperFrames recebe os mesmos sons.
- **Vídeos, gravações e prints** dos meus reels.
- **Perfis reais de criadores:** nas cenas de exemplo eles viraram `@criador_1` e `@criador_2`.

---

### In English

A step-by-step prompt kit (in Portuguese) for editing a talking-head Instagram reel with motion design, word-synced karaoke captions and sound effects, using Claude Code and HyperFrames. 11 prompts take you from raw footage to a final 9:16 render, with a starter folder of 59 motion recipes, scene templates and alignment/captioning scripts. Built and tested by a 7-agent AI workflow. **[Open the kit site](https://kit-edit.vercel.app)**.
