#!/usr/bin/env python3
"""解析全量OCR输出(/tmp/bili_ocr_all.txt) -> 幻灯片时间线。
OCR行格式: [y=.. x=.. h=..] 文本; 帧N ≈ t=N*step 秒(默认抽帧fps=1/2 -> step=2)。
y<0.12 视为底部字幕带(与AI字幕重复)跳过; y>=0.12 为课件文字。
用法: python3 analyze_ocr.py [ocr文件] [step秒]
"""
import re, sys, json

path = sys.argv[1] if len(sys.argv) > 1 else '/tmp/bili_ocr_all.txt'
step = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0

frames = {}
cur = None
for line in open(path):
    line = line.rstrip('\n')
    m = re.match(r'^##### (f_\d+)\.png #####$', line)
    if m:
        cur = int(m.group(1).split('_')[1]); frames[cur] = []; continue
    m2 = re.match(r'^\[y=([\d.]+) x=[\d.]+ h=[\d.]+\] (.*)$', line)
    if m2 and cur is not None:
        y = float(m2.group(1)); text = m2.group(2).strip()
        if text:
            frames[cur].append((y, text))

def slide_lines(i):
    return tuple(sorted(t for y, t in frames.get(i, []) if y >= 0.12))

prev, timeline = None, []
for i in sorted(frames):
    key = slide_lines(i)
    if key != prev and key:
        t = i * step
        timeline.append((t, i, [txt for (y2, txt) in sorted(frames[i], key=lambda p: -p[0]) if y2 >= 0.12]))
        prev = key

for t, i, lines in timeline:
    print(f"===== t={int(t//60)}:{int(t%60):02d} (帧{i:03d}) =====")
    for ln in lines:
        print("   ", ln)
