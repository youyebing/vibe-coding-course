import Foundation
import Vision
import AppKit

// 用法: ocr <图片路径...> 输出 "[y=.. x=.. h=..] 文本"(y为归一化坐标, 底部字幕带 y<0.12)
// 编译: swiftc -O ocr.swift -o /tmp/ocr
for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("LOAD_FAIL \(path)"); continue
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = ["zh-Hans", "en-US"]
    req.usesLanguageCorrection = true
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do {
        try handler.perform([req])
    } catch { print("OCR_FAIL \(path): \(error)"); continue }
    print("=== \(path) ===")
    for obs in req.results ?? [] {
        if let cand = obs.topCandidates(1).first {
            let b = obs.boundingBox
            print(String(format: "[y=%.2f x=%.2f h=%.2f] %@", b.origin.y, b.origin.x, b.size.height, cand.string))
        }
    }
}
