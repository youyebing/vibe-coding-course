#!/usr/bin/env python3
"""无AI字幕时的备用转写: faster-whisper(本地模型)。
用法:
  1) 模型就位(首次): HF_ENDPOINT=https://hf-mirror.com \
       curl -sL -C - -o /tmp/fw_medium/model.bin \
         https://hf-mirror.com/Systran/faster-whisper-medium/resolve/main/model.bin
     并放 config.json / tokenizer.json 到同目录(仓库无 vocabulary.json, 404正常)。
     ⚠️ huggingface_hub 下载器可能 0% CPU 挂死 -> 杀掉改用上面 curl 断点续传。
  2) python3 transcribe_local.py [音频] [模型目录]
输出带时间戳分段, 并存 <音频>.transcript.txt
"""
import sys
from faster_whisper import WhisperModel

audio = sys.argv[1] if len(sys.argv) > 1 else '/tmp/bili_audio.m4s'
model_dir = sys.argv[2] if len(sys.argv) > 2 else '/tmp/fw_medium'

model = WhisperModel(model_dir, device='cpu', compute_type='int8')
segments, _ = model.transcribe(audio, language='zh', vad_filter=True,
                               initial_prompt='这是一段中文教学/讲解视频。')
out = []
for seg in segments:
    line = f"[{seg.start:7.2f} -> {seg.end:7.2f}] {seg.text.strip()}"
    print(line, flush=True)
    out.append(line)
open(audio + '.transcript.txt', 'w').write('\n'.join(out))
print(f'DONE segments={len(out)}', flush=True)
