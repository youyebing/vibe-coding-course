#!/usr/bin/env python3
"""B站扫码登录: 生成二维码png(/tmp/bili_login_qr.png) + 轮询 + 存cookie。
用法:
  qr_login.py               # 完整流程: 生成新码并轮询(前台跑, 把png发用户扫)
  qr_login.py <old_key>     # 只轮询已有 key(用户扫了旧码时用)
真实状态在 JSON 的 data.code(顶层 code 恒0): 86101未扫/86090已扫待确认/0成功/86038过期。
成功后 cookie 写入 /tmp/bili_cookies.json 并用 nav 校验用户名。
"""
import sys, time, json
import requests, qrcode
from PIL import Image

UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36'}
S = requests.Session(); S.headers.update(UA)

def gen_qr():
    r = S.get('https://passport.bilibili.com/x/passport-login/web/qrcode/generate', timeout=15)
    d = r.json()['data']
    img = qrcode.make(d['url']).convert('RGB')
    pad = 40
    big = Image.new('RGB', (img.width + pad*2, img.height + pad*2), 'white')
    big.paste(img, (pad, pad))
    big.save('/tmp/bili_login_qr.png')
    return d['qrcode_key']

def poll(key, timeout_s=300):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        r = S.get('https://passport.bilibili.com/x/passport-login/web/qrcode/poll',
                  params={'qrcode_key': key}, timeout=15)
        code = (r.json().get('data') or {}).get('code')
        if code == 0:
            cj = {c.name: c.value for c in S.cookies}
            need = {'SESSDATA', 'bili_jct', 'DedeUserID'}
            if not need.issubset(cj):
                print('LOGIN_OK_BUT_MISSING_COOKIES', sorted(cj.keys())); return 1
            json.dump(cj, open('/tmp/bili_cookies.json', 'w'))
            nav = S.get('https://api.bilibili.com/x/web-interface/nav').json()
            print('LOGIN_SUCCESS user=%s vip=%s' % (nav['data'].get('uname'), nav['data'].get('vipStatus')))
            return 0
        if code == 86101: print('WAITING_SCAN', flush=True)
        elif code == 86090: print('SCANNED_WAIT_CONFIRM', flush=True)
        elif code == 86038: print('QR_EXPIRED'); return 2
        else: print('UNEXPECTED', code); return 3
        time.sleep(3)
    print('TIMEOUT_WAIT_USER'); return 4

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sys.exit(poll(sys.argv[1]))
    key = gen_qr()
    print('QR_SAVED /tmp/bili_login_qr.png key=%s — 请用户用B站App扫码, 码约3分钟过期' % key, flush=True)
    sys.exit(poll(key))
