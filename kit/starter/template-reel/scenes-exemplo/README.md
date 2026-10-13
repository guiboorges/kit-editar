# scenes-exemplo: as 8 cenas do exemplo 1 (código de referência)

São as cenas de motion de um reel real de 47,9 s (pipeline A, takes brutos), já renderizadas e revisadas. Servem de
**código provado** para adaptar: em vez de gerar uma cena do zero, o agente copia a estrutura, os helpers
(`IN/OUT/POP/COUNT/TYPE`), os wrappers, os anéis, os brilhos e os números de easing destas cenas. As receitas de cada
uma, com os números exatos, estão em `../../RECEITAS-DE-MOTION.md` (uma seção por cena, mesmo nome).

**Importante:**
- Elas apontam para **assets que não vêm no kit** (imagens, vídeos e a câmera do projeto original). Abertas
  sozinhas, imagens e vídeos ficam vazios: o que vale aqui é o código de motion e a estrutura.
- Os textos, números e marcas dentro do código são do projeto original. O @ e os arquivos do criador que aparecia
  nas cenas s1 e s8 foram trocados por marcadores neutros (`@criador_1`, `avatar-criador-1.png`, `criador1-rua.mp4`).
  No seu vídeo, o conteúdo vem só do seu `STORYBOARD.md` e os assets só da tabela do seu `DESIGN.md`.
- Os tempos dentro de cada cena são **locais** (segundos desde o início da cena), nas constantes de cue no topo do
  `<script>`.
- Para ver uma cena funcionando, ela precisa estar num projeto HyperFrames, hospedada pelo `index.html`
  (`data-composition-src="compositions/<id>.html"`), com os assets no lugar.

| Arquivo | Cena (tempo no vídeo original) | Arquétipo | Assets que ela referencia (não incluídos) |
|---|---|---|---|
| `s1-hook.html` | 0,00–4,67 s | gancho com B-roll + carimbo + cronômetro | `assets/broll/criador1-rua.mp4`, `assets/broll/genjutsu.mp4`, `assets/img/avatar-criador-1.png`, `assets/img/personagem-retrato.jpg` |
| `s2-launchpoint.html` | 4,67–11,20 s | print da plataforma, foco puxado, pílulas puxadas do print | `assets/img/lp-hero.png`, `assets/img/logo-launchpoint.png` |
| `s3-calc.html` | 11,20–16,13 s | equação / dinheiro com contagem e slam lima | só as fontes |
| `s4-quem-banca.html` | 16,13–21,03 s | busca digitando → headline → ranking → linha do líder "#1" | `assets/img/lp-grid.png`, `assets/img/logo-launchpoint.png`, `assets/img/logo-higgsfield.png` |
| `s5-ciclo.html` | 22,03–29,40 s | comparação ✕ / ✓ e ciclo | `assets/img/personagem-retrato.jpg` |
| `s6-teste.html` | 29,40–38,90 s | janela de app com estados (conectores → toggle → prompt → resultado) | `assets/img/logo-claude.svg`, `assets/img/logo-higgsfield.png`, `assets/img/personagem-sheet.jpg` |
| `s7-genjutsu.html` | 38,90–43,10 s | antes × depois sincronizados (ORIGINAL × RESULTADO) | `assets/broll/genjutsu.mp4`, `media/t4-prova.mp4`, `assets/img/personagem-retrato.jpg`, `assets/img/personagem-sheet.jpg`, `assets/img/logo-higgsfield.png` |
| `s8-cta.html` | 43,10–47,90 s | CTA de comentários + DM, segura até o fim | `assets/img/avatar-gui.jpg`, `assets/img/avatar-criador-1.png` |
| `captions.html` | 0–47,9 s | a legenda karaokê **gerada** pelo `build_captions.py` (takes-brutos) daquele vídeo: exemplo de saída, não edite à mão | — |

Todas usam também `assets/fonts/Geist-latin.woff2` e `assets/fonts/GeistMono-latin.woff2` (estas vêm no kit, em
`../fonts/`).
