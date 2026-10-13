// face.swift: mede a posição dos olhos (pupilas) em quadros do vídeo com o Apple Vision.
//
// Requisitos: macOS + ferramentas de linha de comando do Xcode (xcode-select --install, para ter o swiftc).
//             Não funciona no Windows/Linux: lá, meça os olhos em stills com grade, à mão.
// Onde fica : <seu projeto>/edit/tools/face.swift
// Para quê  : pôr os olhos sempre na mesma altura em todos os cortes (enquadramento A/B). Medir, não chutar.
//
// Como usar (pipeline TAKE CORTADO, dentro da pasta do projeto):
//   1. Extraia 3 quadros de cada trecho entre cortes (a 20%, 50% e 80% dele). Troque a lista c pelos SEUS valores:
//      0, os seus CUTS e a duração TOTAL.
//        mkdir -p ff
//        for t in $(python3 -c "
//        c=[0,5.567,8.733,11.9,65.433]
//        for a,b in zip(c,c[1:]):
//          for k in (0.2,0.5,0.8): print(round(a+(b-a)*k,2))"); do
//          ffmpeg -v error -y -ss $t -i media/take.mp4 -frames:v 1 -vf scale=1080:1920 ff/f_$t.png
//        done
//   2. Compile e rode:
//        swiftc -O edit/tools/face.swift -o face && ./face $(ls ff/*.png | sort -t_ -k2 -n)
//
// Saída: uma linha por quadro em que achou um rosto:
//   <arquivo> face_cx=<centro x do rosto> top=<topo> bottom=<base> eyeX=<x dos olhos> eyeY=<y dos olhos>
//   Tudo em fração do quadro (0 = esquerda/topo, 1 = direita/base). eyeX/eyeY = -1 se não achou as pupilas.
//   Quadro sem rosto não imprime nada: tire outro quadro daquele trecho.
//   Uma linha de log do sistema como "FBBA: creating VNFaceBBoxAligner…" pode aparecer antes: é do macOS, ignore.
//
// O que fazer com a saída:
//   - take-cortado: tire a MÉDIA de eyeX e de eyeY dos 3 quadros de cada trecho e cole como (eyeX, eyeY) na lista
//     EYES do edit/build_edl.py (um par por trecho, em ordem). A média de todos os eyeY vai em EYE_MEAN_Y do
//     edit/build_index.py. (No exemplo 2: 17 trechos × 3 = 51 quadros; olhos em 46,6% da altura e 45,6% da largura.)
//   - takes-brutos: a média de cada take vai em FACE do edit/build_index.py, como (x do rosto, y dos olhos).
//   - Confira num snapshot com grade: olhos na mesma altura em todos os cortes.
import Vision
import AppKit
for path in CommandLine.arguments.dropFirst() {
  guard let img = NSImage(contentsOfFile: path), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
  let req = VNDetectFaceLandmarksRequest()
  let h = VNImageRequestHandler(cgImage: cg, options: [:])
  try? h.perform([req])
  let W = Double(cg.width), H = Double(cg.height)
  if let f = req.results?.first {
    let bb = f.boundingBox
    var eyeY = -1.0, eyeX = -1.0
    if let le = f.landmarks?.leftPupil, let re = f.landmarks?.rightPupil {
      let p1 = le.pointsInImage(imageSize: CGSize(width: W, height: H))[0]
      let p2 = re.pointsInImage(imageSize: CGSize(width: W, height: H))[0]
      eyeY = (H - (p1.y + p2.y)/2) / H; eyeX = ((p1.x + p2.x)/2) / W
    }
    let name = (path as NSString).lastPathComponent
    print(String(format: "%@ face_cx=%.3f top=%.3f bottom=%.3f eyeX=%.3f eyeY=%.3f", name, bb.midX, 1-bb.maxY, 1-bb.minY, eyeX, eyeY))
  }
}
