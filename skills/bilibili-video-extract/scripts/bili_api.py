"""B站 API 公共助手: wbi签名 / 登录态会话 / 元信息 / 字幕 / 播放流"""
import hashlib, json, time, urllib.parse
import requests

UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
      'Referer': 'https://www.bilibili.com/'}
MIXIN_TABLE = [46,47,18,2,53,8,23,32,15,50,10,31,58,3,45,35,27,43,5,49,33,9,42,19,29,28,14,39,12,38,41,13,37,48,7,16,24,55,40,61,26,17,0,1,60,51,30,4,22,25,54,21,56,59,6,63,57,62,11,36,20,34,44,52]

def session(cookie_path='/tmp/bili_cookies.json'):
    """带 UA/Referer 的会话; cookie 存在则自动附加登录态"""
    s = requests.Session(); s.headers.update(UA)
    try:
        s.cookies.update(json.load(open(cookie_path)))
    except Exception:
        pass
    return s

def _mixin(orig):
    return ''.join(orig[i] for i in MIXIN_TABLE if i < len(orig))[:32]

def wbi_sign(s, params):
    """wbi 签名(需要先 GET nav 拿 keys; 匿名也能签, 但结果无登录权益)"""
    nav = s.get('https://api.bilibili.com/x/web-interface/nav', timeout=15).json()
    img = nav['data']['wbi_img']
    ik = img['img_url'].rsplit('/', 1)[-1].split('.')[0]
    sk = img['sub_url'].rsplit('/', 1)[-1].split('.')[0]
    key = _mixin(ik + sk)
    params['wts'] = int(time.time())
    params = dict(sorted(params.items()))
    q = urllib.parse.urlencode(params)
    params['w_rid'] = hashlib.md5((q + key).encode()).hexdigest()
    return params

def view_info(s, bvid):
    j = s.get('https://api.bilibili.com/x/web-interface/view',
              params={'bvid': bvid}, timeout=15).json()
    d = j['data']
    return {'title': d['title'], 'owner': d['owner']['name'], 'duration': d['duration'],
            'aid': d['aid'],
            'pages': [{'part': p['part'], 'cid': p['cid']} for p in d['pages']]}

def list_subtitles(s, bvid, cid):
    """登录态返回 ai-zh/zh 轨; 匿名几乎恒为空 —— 别据此判'无字幕'"""
    info = view_info(s, bvid)
    j = s.get('https://api.bilibili.com/x/player/wbi/v2',
              params=wbi_sign(s, {'aid': info['aid'], 'cid': cid, 'bvid': bvid}), timeout=15).json()
    return ((j.get('data') or {}).get('subtitle') or {}).get('subtitles') or []

def get_subtitle_body(s, sub):
    url = sub['subtitle_url']
    if url.startswith('//'):
        url = 'https:' + url
    return s.get(url, timeout=15).json().get('body', [])

def dash_url(s, bvid, cid, quality=80, kind='video'):
    """kind=video: 指定清晰度 80=1080p/64=720p/32=480p, 取不到则降级<=1080p最高;
       kind=audio: 取码率最高的纯音频流"""
    info = view_info(s, bvid)
    j = s.get('https://api.bilibili.com/x/player/playurl',
              params=wbi_sign(s, {'aid': info['aid'], 'bvid': bvid, 'cid': cid,
                                  'fnval': '16', 'fourk': '1'}), timeout=15).json()
    streams = (j['data'].get('dash') or {}).get(kind, [])
    if not streams:
        raise SystemExit(f'no dash {kind} stream (code={j.get("code")})')
    if kind == 'video':
        cand = [v for v in streams if v.get('id') == quality] or \
               [v for v in streams if v.get('height', 9999) <= 1080]
    else:
        cand = streams
    return sorted(cand, key=lambda x: x.get('bandwidth', 0))[-1]['baseUrl']
