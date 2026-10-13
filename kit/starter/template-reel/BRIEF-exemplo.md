# BRIEF: modelo comentado

O `BRIEF.md` fica na raiz do projeto e diz **o que** o vídeo precisa entregar: a mensagem, o destino, os
materiais, as decisões tomadas e o que foi **inferido sem confirmação**. O HyperFrames lê o cabeçalho (entre as linhas
`---`) para saber qual fluxo seguir; o Claude e os agentes leem o resto. O `DESIGN.md` diz *como* o vídeo parece, e
o `STORYBOARD.md` diz *o que acontece em cada segundo*.

Abaixo: (1) o modelo em branco para copiar e (2) o BRIEF real do exemplo 2 (um reel de 65,4 s editado a partir de
um take já cortado), com comentários `← assim` explicando cada parte.

---

## 1. Modelo em branco (copie para `<projeto>/BRIEF.md`)

```markdown
---
workflow: general-video
flow: companion
storyboard: no
message: "<a ideia do vídeo em uma frase>"
destination: Instagram Reels / TikTok
aspect: "9:16"
language: pt-BR
length: "~<duração>s"
---

## Intent
Pedido (<data>): "<o que você pediu, com as suas palavras>"
Formato: tela dividida (câmera 0–780, legenda karaokê na emenda, motion em papel claro embaixo), seguindo
PADRAO-DE-QUALIDADE.md e a referência <nome/@ do reel de referência>.

## Assets
- Câmera: <takes brutos (pipeline A) OU um take já cortado por você (pipeline B)>: <caminho, resolução, fps, duração,
  loudness medida>. Proxy: <media/…>.
- Cortes: <pipeline A: quem corta é o build_edl.py | pipeline B: N cortes seus, detectados por diferença de fundo>.
- Prints: <caminho → assets/img/…: o que é; é daqui que saem os números da tela>.
- B-roll: <caminho → assets/broll/…: o que é; @perfil e nº de seguidores, se aparecer>.
- Seus ativos: <ex.: o seu personagem, telas do app que você usou, o resultado>.

## Customizations
- <decisões que fogem do padrão ou que precisam ficar escritas: telas cheias (em que frases), nº de cenas, de onde
  vêm os números, cores, o que NÃO mostrar>

## Notes
- Inferido (não confirmado): <tudo que o Claude assumiu sem você dizer: @ do CTA, nomes, valores…>
- <trilha ou sem trilha; minúsculas na legenda; muletas que não aparecem na legenda>
```

---

## 2. Exemplo real comentado (exemplo 2)

```markdown
---
workflow: general-video        ← campos lidos pelo HyperFrames: o fluxo usado é o "general-video"
flow: companion                ← com "companion", o HyperFrames sempre executa pelo general-video (peças longas, várias cenas)
storyboard: no                 ← sem pausa de revisão do plano nem folha de esboço; o STORYBOARD.md é escrito assim mesmo
message: "Tem gente ganhando dinheiro com personagem de IA — a Higgsfield paga quem usa a ferramenta, e eu mostro como criei o meu (Claude + MCP + Genjutsu)."
                               ← UMA frase: é com ela que se decide o que cada cena precisa provar
destination: Instagram Reels / TikTok
aspect: "9:16"
language: pt-BR
length: "~65s"
---

## Intent
Pedido (2026-10-08): "Edita esse vídeo. A ideia é ter motion, cortes e tudo o que for dito com referência visual."
                               ← o pedido literal, com data: evita reinterpretar depois
Mesmo formato do padrão-ouro e da referência "Comenta PERSONAGEM" (@higgsfield.ai):
tela dividida — câmera em cima (0–780), legenda karaokê na emenda, motion em papel claro embaixo.
Toda frase tem uma referência visual no palco, batendo na palavra.
                               ← a regra de ouro do vídeo, escrita: o storyboard vai ter uma cena por frase

## Assets
- Take único já decupado pelo usuário: 1008.mov (2160×3840 30p, H.264 Rec.709, 65,43 s, áudio já processado
  a −8 LUFS). Proxy media/take.mp4 (1440×2560, GOP 15, voz → −15 LUFS, cauda +0,3 s).
                               ← medido com ffprobe/ebur128, não chutado. (Depois a voz foi para −14 LUFS: ver PADRAO §5.)
- O vídeo chega com 16 jump cuts do próprio usuário (detectados por diferença de fundo; quadros f167, f262, …).
  Não removemos pausas: a fala é contínua. Cada corte vira troca de enquadramento A (1,0×) / B (1,10×);
  2 "zoom cuts" extras em respiros (24,10 s e 51,40 s) nos trechos longos.
                               ← a decisão que define o pipeline B (take já cortado), escrita para ninguém "recortar a voz"
- Reaproveitados do exemplo 1: B-roll de 2 perfis de personagens de IA, prints da plataforma (página + ranking),
  logos, folha do personagem, o vídeo do Genjutsu + o trecho ORIGINAL sincronizado com ele.
                               ← cada asset vira uma linha na tabela de assets do DESIGN.md, com tamanho e coordenadas

## Customizations
- Duas janelas de câmera em tela cheia: "e pensa comigo, ao invés da Higgsfield" (19,23–20,95) e
  "tá, e como é que você pode fazer isso?" (58,17–59,67). A cena anterior segura até a câmera cobrir o palco (wipe).
                               ← as frases de conversa direta. Os tempos finais (FULLS) foram ajustados depois no build_index.py
- Números na tela só os do print: "até US$ 2.000 por vídeo" (pílula "Up to $2,000/Video"), ranking da plataforma.
                               ← honestidade de conteúdo: diz de ONDE sai cada número que aparece
- 11 cenas (s1–s11), ver STORYBOARD.md.

## Notes
- Inferido (não confirmado): handle do DM no CTA = "<@ herdado do exemplo 1>".
                               ← tudo que foi assumido fica marcado, para você confirmar antes de publicar
- Sem trilha (a referência tem). Legendas minúsculas como na referência.
- Fala "comenta a CLONE": o "a" (muleta) não aparece na legenda.
                               ← vira o SKIP do build_edl.py
```
