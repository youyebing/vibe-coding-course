# Vibe Coding 术语课 · 学习整理（课程笔记 + Hermes Skills）

把 B 站《Vibe Coding 术语课》17 集系统整理成可检索的学习资料，并沉淀为一组可供 AI 助手（Hermes）直接调用的技能，帮助**后端工程师用 AI 设计前端页面**。

## 📚 内容结构

```
├── skills/                        # Hermes Skills（可直接安装复用）
│   ├── frontend-ai-design/        #   用 AI 设计前端页面：10 层词汇模型 + 159 词术语字典 + 需求模板
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── glossary.md        #     159 词术语字典（定义/句式/代码/避坑）
│   │       └── prompt-templates.md #    5 类页面需求模板 + 验收句
│   ├── api-contract-vocabulary/    #   前后端对接契约：6 层模型 + 63 词对接词表 + 契约模板与验收清单
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── contract-glossary.md   #     63 词六层词表（请求/响应/鉴权/跨域/界面态/联调治理）
│   │       └── contract-templates.md  #     接口契约表 / 响应包装 / 错误码分段 / AI 提词 / 联调清单
│   ├── bilibili-video-extract/    #   B 站视频提取工具链（扫码登录/字幕/OCR 交叉校对）
│   │   ├── SKILL.md
│   │   └── scripts/               #     wbi 签名 / 二维码登录 / 字幕拉取 / Vision OCR 等
│   ├── socratic-inquiry/          #   通用苏格拉底问诊：重建问题本身（一次一问 ≤6 问，六要素收敛）
│   │   └── SKILL.md
│   └── socratic-requirement-clarification/  #   工程需求澄清：锁定交付物（决定编号记账、全量复述确认）
│       └── SKILL.md
└── 课程笔记/
    ├── 分集笔记/                  # 17 集 × md，每概念配视频截图（标题卡 + 讲解屏）
    │   ├── README.md              #   目录索引
    │   └── ep01~ep17/
    └── 逐字稿/                    # 17 集带时间戳字幕文本（便于回看定位）
```

## 🚀 安装与使用

**Skills**（Hermes 用户）：把 `skills/` 下四个目录复制到 `~/.hermes/skills/<分类>/`（如 `creative/frontend-ai-design`、`software-development/api-contract-vocabulary`、`media/bilibili-video-extract`、`software-development/socratic-inquiry`、`software-development/socratic-requirement-clarification`），之后对 AI 说"帮我做个页面"或发 B 站链接即可自动调用。`frontend-ai-design` 的需求澄清环节会联动两个 socratic skill：先问诊重建问题（`socratic-inquiry`），再澄清锁定交付物（`socratic-requirement-clarification`）。`api-contract-vocabulary` 补的是 `frontend-ai-design` 第 1–10 层之外的第 11 层——**页面怎么接上自己的后端**：六层对接模型（请求/响应/鉴权/跨域与环境/界面态/联调治理）、63 词对接词表、接口契约表与联调验收清单。

**课程笔记**：用 Obsidian / Typora 打开 `课程笔记/分集笔记/README.md`，图片随文档渲染（相对路径，整个文件夹搬家不断链）。

## 🙏 出处与致谢

- **课程**：《Vibe Coding 术语课》——UP 主 **ZTough**（Bilibili），合集 17 集，共 159 个前端/网页术语。
  - 合集链接：https://www.bilibili.com/video/BV19zt762EYr （season_id=8995110）
  - 每集逐字稿、视频画面截图均整理自该系列。
- **整理**：@huangning（youyebing）——画面 OCR × AI 字幕交叉校对提取，英文术语拼写以画面为准。
- **感谢 ZTough** 制作了这套对后端工程师极友好的前端术语课。

## ⚖️ 版权声明

- `skills/` 下代码与文档、笔记的文字整理结构为本仓库作者原创（见 LICENSE）。
- **课程视频画面、字幕文本版权归原作者 ZTough 及 Bilibili 平台所有**，本仓库以学习整理目的收录，已获原作者授权分享；如需商业使用或再次转载，请联系原作者。
- 仓库中不包含任何视频文件本体。
