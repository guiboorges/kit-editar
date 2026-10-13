# scenes-exemplo-2: as 11 cenas do exemplo 2 (código de referência)

São as cenas de motion de um reel real de 65,4 s (pipeline B, take já cortado), construídas pelo workflow
multiagente (`../edit/workflow-cenas.js`) adaptando as cenas de `../scenes-exemplo/` e depois corrigidas por revisores
adversariais e numa revisão final. Use como **código provado** para adaptar, do mesmo jeito que `scenes-exemplo/`.
Elas não têm seção própria no `RECEITAS-DE-MOTION.md`: a coluna "Adaptou" diz de qual cena-exemplo cada uma veio.

**Importante:**
- Elas apontam para **assets que não vêm no kit** (imagens e vídeos do projeto original). Abertas sozinhas, imagens e
  vídeos ficam vazios: o que vale aqui é o código de motion e a estrutura.
- Os textos, números e marcas dentro do código são do projeto original. Os @ e os arquivos dos dois criadores que
  apareciam nas cenas s1, s2, s3, s5 e s6 foram trocados por marcadores neutros (`@criador_1`, `@criador_2`,
  `avatar-criador-1.png`, `criador1-rua.mp4` etc.): são só nomes de exemplo. No seu vídeo, o conteúdo vem só do seu
  `STORYBOARD.md` e os assets só da tabela do seu `DESIGN.md`. Não associe pessoas reais a dinheiro ou a uma marca sem
  poder confirmar (ver o checklist do padrão).
- `s8-avatar.html` traz embutidas duas máscaras PNG pequenas (contorno do cabelo), tiradas do retrato do personagem
  do próprio criador do vídeo original: troque pelas do seu ativo, se adaptar essa cena.
- Os tempos dentro de cada cena são **locais** (segundos desde o início da cena).
- Para ver uma cena funcionando, ela precisa estar num projeto HyperFrames, hospedada pelo `index.html`, com os
  assets no lugar.

| Arquivo | Cena (tempo no vídeo original) | O que mostra | Adaptou | Assets que ela referencia (não incluídos) |
|---|---|---|---|---|
| `s1-hook.html` | 0,000–5,567 s | montagem de 3 B-rolls, tag, créditos com nº de seguidores, carimbos | s1-hook | `assets/broll/criador1-rua.mp4`, `criador1-mesa.mp4`, `criador2-carro.mp4`, `assets/img/avatar-criador-1.png`, `avatar-criador-2.png` |
| `s2-dinheiro.html` | 5,567–8,733 s | bloco "$", dois criadores, contagem até "US$ 2.000 /vídeo" | s3-calc | `assets/img/avatar-criador-1.png`, `avatar-criador-2.png` |
| `s3-quem-paga.html` | 8,733–11,900 s | título cinético "quem pagaria?" + mini-vídeo com "?" | s4-quem-banca | `assets/broll/criador1-rua.mp4` |
| `s4-launchpoint.html` | 11,900–19,600 s | página em foco, pílula puxada do print, rolagem até o ranking, linha "#1" (segura enquanto a câmera cobre) | s2-launchpoint + s4-quem-banca | `assets/img/lp-hero.png`, `lp-grid.png`, `lp-header.png`, `logo-launchpoint.png`, `logo-higgsfield.png` |
| `s5-ciclo.html` | 20,600–29,033 s | card riscado × card vencedor com moedas, depois o ciclo | s5-ciclo | `assets/broll/genjutsu.mp4`, `assets/img/avatar-gui.jpg`, `avatar-criador-1.png`, `avatar-criador-2.png`, `logo-higgsfield.png`, `personagem-retrato.jpg` |
| `s6-voce.html` | 29,033–33,833 s | 3 balões "tá", 2 cards de vídeo com "+ $", espaço tracejado "você?" | s5-ciclo + s7-genjutsu | `assets/broll/criador1-mesa.mp4`, `criador2-carro.mp4` |
| `s7-claude.html` | 33,833–40,833 s | janela do Claude: conectores, toggle, pílula MCP, prompt digitado e enviado | s6-teste | `assets/img/logo-claude.svg`, `logo-higgsfield.png` |
| `s8-avatar.html` | 40,833–46,633 s | retrato com contorno no cabelo, amostra de cor, régua, chips esqueleto, folha de corpo inteiro | s6-teste + s7-genjutsu | `assets/img/personagem-retrato.jpg`, `personagem-sheet.jpg`, `logo-claude.svg` |
| `s9-genjutsu.html` | 46,633–54,600 s | app escuro: clique na aba, sorteio entre vídeos, slots, Gerar, progresso | s6-teste | `assets/broll/original-2883.mp4`, `assets/img/personagem-corpo.jpg`, `personagem-retrato.jpg`, `thumb-*.jpg`, `logo-higgsfield.png` |
| `s10-resultado.html` | 54,600–58,533 s | ORIGINAL × RESULTADO sincronizados quadro a quadro (segura enquanto a câmera cobre) | s7-genjutsu | `assets/broll/genjutsu.mp4`, `original-2883.mp4` |
| `s11-cta.html` | 59,300–65,433 s | comentários: digita a palavra, envia, DM abre um checklist de 3 passos, carimbo final; segura até o fim | s8-cta | `assets/img/avatar-gui.jpg`, `personagem-retrato.jpg`, `thumb-genjutsu.jpg`, `logo-claude.svg`, `logo-higgsfield.png` |
| `captions.html` | 0–65,433 s | a legenda karaokê **gerada** pelo `build_captions.py` (take-cortado) daquele vídeo (108 blocos, 3 modos): exemplo de saída, não edite à mão | — | — |

Todas usam também `assets/fonts/Geist-latin.woff2` e `assets/fonts/GeistMono-latin.woff2` (estas vêm no kit, em
`../fonts/`).
