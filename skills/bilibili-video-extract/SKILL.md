---
name: bilibili-video-extract
description: "Bilibili video extraction via QR login, AI subs, OCR."
---

# Bilibili 视频内容提取

获取 B 站视频的旁白与画面文字，产出带时间戳的逐字稿与结构化笔记。
核心认知：**匿名 API 拿不到字幕轨、最高只有 480p——必须先扫码登录**；登录后 B 站 AI 字幕（ai-zh）提供精确旁白，1080p 画面 OCR 提供术语拼写真值，两者交叉校对才可靠。

## 何时用
- 用户发来 b23.tv 短链或 bilibili.com/video/BV… 链接，要求"提取内容 / 讲了什么 / 做笔记 / 字幕"
- 教学视频、术语课、网课等（画面信息量大时 OCR 尤其必要）

## 环境事实（本机）
- venv python：`/Users/huangning/.hermes/hermes-agent/venv/bin/python3`（已装 requests / faster-whisper / qrcode / pyobjc-Vision）
- 网络：B 站 API 与 CDN 直连可用；huggingface.co 直连不通，模型走 `hf-mirror.com` 镜像
- macOS 自带 swiftc → 用系统 Vision 框架做 OCR，**无需 pyobjc**（pyobjc-framework-Vision 也已装好作后备）
- 扫码登录 cookie 存 `/tmp/bili_cookies.json`，有效期约一个月，同机复用免重扫

## 流程

### 1. 解析短链 + 元信息
```bash
curl -s -o /dev/null -w '%{url_effective}\n' -L --max-time 20 https://b23.tv/XXXX
# -> https://www.bilibili.com/video/BV19zt762EYr/...  取 BV 号
```
view API（UA 头必须带）取 cid / duration / pages：
`GET https://api.bilibili.com/x/web-interface/view?bvid=BV...`（免签名）

### 2. 扫码登录（首次必须，脚本见 scripts/）
```bash
python3 scripts/qr_login.py     # 生成 /tmp/bili_login_qr.png + 后台轮询
```
把 png 用 `MEDIA:` 发给用户："用 B 站 App 扫一下"。等输出 `LOGIN_SUCCESS user=…`。
- ⚠️ **轮询状态在 JSON 的 `data.code`**（顶层 `code` 恒为 0，易误判成功）：86101 未扫码 / 86090 已扫待确认 / 0 成功 / 86038 过期
- ⚠️ 用户可能扫的是**上一轮展示过的旧码**：旧码若未过期，轮询它的 key 同样能拿到 cookie。必要时把新旧两个 key 都 poll 一遍
- 成功标志：cookies 含 SESSDATA / bili_jct / DedeUserID

### 3. 拉 AI 字幕（登录态）
```bash
python3 scripts/fetch_content.py subs BV19zt762EYr 41513585403
# -> /tmp/bili_sub.json（body 数组，含 from/to/content）+ /tmp/bili_subtitle_text.txt
```
有 ai-zh/zh 轨 → 旁白真值。若没有（少数视频）→ 走第 6 节 whisper 转写。

### 4. 下载 1080p → 抽帧 → OCR（课件文字 + 术语校正）
```bash
python3 scripts/fetch_content.py video BV19zt762EYr 41513585403 80   # 80=1080p, 64=720p, 32=480p
ffmpeg -v error -i /tmp/bili_video.m4s -vf fps=1/2 /tmp/bili_fr/f_%03d.png
swiftc -O scripts/ocr.swift -o /tmp/ocr
for f in /tmp/bili_fr/f_*.png; do echo "##### $(basename "$f") #####"; /tmp/ocr "$f"; done > /tmp/bili_ocr_all.txt
python3 scripts/analyze_ocr.py    # 输出幻灯片时间线(帧N≈t=2N秒)
```
- OCR 行格式 `[y=.. x=.. h=..] 文本`；**y<0.12 是底部字幕带**（与 AI 字幕重复，跳过），y≥0.12 是课件文字
- 静态课件视频压缩率高：5 分钟 1080p 可能只有 8MB，属正常

### 5. 交叉校对、合成产出
AI 字幕典型错误：英文术语听成中文同音（Vibe Coding→"web coding"、CSS→"cs s"、DOM→"duo"、Markdown 缺失），中文同音错字（"七个词"→"吸个词"、"页面活了"→"页面火了"、组件→"组建"）。**拼写一律以画面 OCR 为准**。
产出两件（存 `~/<系列名>/` 或问用户）：
1. 结构化笔记 md：每术语 = 一句话定义（画面原文）+ 讲解展开 + 口诀/避坑 + 时间戳；收尾常有一张"串联图"逐条抄录
2. 逐字稿：AI 字幕按画面修正，`[t]` 时间戳分段，标注"术语原文以画面为准"

### 6. 备用：无 AI 字幕 → faster-whisper 本地转写
- 模型下载必须 `HF_ENDPOINT=https://hf-mirror.com`，且 ⚠️ huggingface_hub 下载器可能 0% CPU 挂死：杀掉进程，改 curl 断点续传：
```bash
curl -sL -C - -o /tmp/fw_medium/model.bin https://hf-mirror.com/Systran/faster-whisper-medium/resolve/main/model.bin
```
还需同目录 config.json、tokenizer.json（仓库无 vocabulary.json，404 正常）。
- 转写：`WhisperModel("/tmp/fw_medium", device="cpu", compute_type="int8")`；`language="zh"`、`vad_filter=True`、initial_prompt 提示术语语境。5 分钟音频 medium 全流程约 10-15 分钟。

## 陷阱汇总
1. 匿名查字幕返回空 ≠ 无字幕：**登录后再判断**（本机已验证：登录后 ai-zh 轨出现）
2. QR 轮询看 `data.code`，顶层 code 恒 0
3. wbi 签名算法（MIXIN_TABLE + wts + md5）见 scripts/bili_api.py，player/playurl 接口都要
4. 下载 m4s 必须带 UA + `Referer: https://www.bilibili.com/`，否则 403
5. 抽帧 fps=1/2 → 帧号≈2 秒/帧；OCR 文本行以 `[y=` 开头，清洗时别把文本删光
6. 给用户展示二维码图片用 `MEDIA:/tmp/bili_login_qr.png`；码约 3 分钟过期，过期重生成

## 验证
- 字幕：body 行数 × 均句长 ≈ 时长（5 分钟 ≈ 130-160 句）
- OCR 时间线能认出"网页基础术语·第 N 词"标题卡与收尾总结页
- 抽查关键术语拼写与 UP 视频标题一致
