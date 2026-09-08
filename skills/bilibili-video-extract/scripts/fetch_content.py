#!/usr/bin/env python3
"""拉取B站视频内容(需 /tmp/bili_cookies.json 登录态, 见 qr_login.py)。
用法:
  fetch_content.py info <bvid>
  fetch_content.py subs  <bvid> <cid>          # 字幕body -> /tmp/bili_sub.json + 纯文本
  fetch_content.py video <bvid> <cid> [质量id] # 下载画面流 -> /tmp/bili_video.m4s (默认80=1080p)
  fetch_content.py audio <bvid> <cid>          # 下载音频流 -> /tmp/bili_audio.m4s (whisper备用)
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bili_api

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    cmd, bvid = sys.argv[1], sys.argv[2]
    s = bili_api.session()
    if cmd == 'info':
        print(json.dumps(bili_api.view_info(s, bvid), ensure_ascii=False, indent=1)); return
    cid = int(sys.argv[3])
    if cmd == 'subs':
        subs = bili_api.list_subtitles(s, bvid, cid)
        if not subs:
            print('无字幕轨(登录态下仍无 → 走 whisper 路线)'); sys.exit(2)
        print('字幕轨:', [(x['lan'], x['lan_doc']) for x in subs])
        target = next((x for x in subs if x['lan'].startswith('zh')), subs[0])
        body = bili_api.get_subtitle_body(s, target)
        json.dump(body, open('/tmp/bili_sub.json', 'w'), ensure_ascii=False)
        txt = '\n'.join('[%d:%02d] %s' % (int(x['from'] // 60), int(x['from'] % 60), x['content']) for x in body)
        open('/tmp/bili_subtitle_text.txt', 'w').write(txt)
        print('SUB_LINES %d -> /tmp/bili_sub.json + /tmp/bili_subtitle_text.txt' % len(body))
    elif cmd == 'video':
        qid = int(sys.argv[4]) if len(sys.argv) > 4 else 80
        url = bili_api.dash_url(s, bvid, cid, quality=qid, kind='video')
        _dl(url, '/tmp/bili_video.m4s')
    elif cmd == 'audio':
        url = bili_api.dash_url(s, bvid, cid, kind='audio')
        _dl(url, '/tmp/bili_audio.m4s')

def _dl(url, out):
    r = bili_api.session().get(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(out, 'wb') as f:
        for chunk in r.iter_content(1 << 16):
            f.write(chunk)
    print('SAVED', out, os.path.getsize(out), 'bytes')

if __name__ == '__main__':
    main()
