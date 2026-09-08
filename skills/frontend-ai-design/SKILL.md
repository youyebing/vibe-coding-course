---
name: frontend-ai-design
description: "Frontend via AI: term lexicon, prompt phrasing, checks."
version: 1.0.0
---

# 用 AI 设计前端页面（后端工程师向）

材料来源：《Vibe Coding 术语课》17 集合集（UP: ZTough，B 站），由画面 OCR × AI 字幕交叉提取为术语卡。
目标读者：**擅长后端、缺前端词汇**的工程师。本技能让你能：
1. **听懂 AI 的前端黑话**（Modal？Drawer？Carousel？→ 查字典）
2. **用准确词汇把页面需求一次说清**，减少反复返工
3. **验收 AI 交付的页面**，有清单可逐条打勾

## 何时用
- 用户说"帮我做个页面 / 网页 / 报名页 / 管理后台 / 落地页"，要交给 AI 生成前端
- AI 回复里冒出不懂的前端术语 → 打开 `references/glossary.md` 查
- 用户描述含糊（"做个好看的页面"）→ 用分层模型引导他把需求拆成词
- 要具体视觉风格参考（Stripe / Linear 那种）→ 另加载 `popular-web-designs` 技能

## 核心方法：分层词汇模型

把"做个网页"拆成 10 层，每层用对词，AI 才听得懂。写需求前逐层过一遍：

| # | 层 | 问自己 | 代表词（全表见 glossary.md） |
|---|---|---|---|
| 1 | **页面大件** | 页面分哪几大块？ | Hero、CTA、Navbar、Footer、Feature、Pricing… |
| 2 | **布局** | 块怎么排？ | 栅格/Grid、Flex、Container、间距、对齐… |
| 3 | **表单** | 要收集什么信息？ | form、label、input、textarea、radio、checkbox、校验 |
| 4 | **控件** | 每个值怎么填/选？ | switch、slider、select、date-picker、cascader、tree-select |
| 5 | **内容展示** | 数据怎么呈现？ | table、list、card、tag、badge、avatar、tree、tabs… |
| 6 | **反馈** | 操作结果怎么告知？ | alert、toast、modal、drawer、tooltip、progress、skeleton |
| 7 | **导航** | 页面之间怎么串？ | menu、breadcrumb、pagination、steps、backtop、anchor |
| 8 | **外观** | 长什么样？ | 颜色、字体、字号、圆角、阴影、间距 |
| 9 | **交互** | 动起来是什么样？ | hover、过渡、动画、拖拽、无限滚动 |
| 10 | **网络与验收** | 对外呈现与兜底 | 域名/CDN/重定向 + Title、Favicon、Undo、Accessibility |

> 记忆锚：**值越复杂，控件越高级**（布尔→switch；连续值→slider；枚举→select；树→tree-select）。

## 工作流（四步）

1. **需求澄清**：什么页面、给谁用、核心动作是什么（报名？下单？看数据？）——一句话说清页面目的。
2. **分层填词**：按上表 10 层逐层问/填，拿不准的词去 `references/glossary.md` 查用法与给 AI 的句式。
3. **组装需求句**：用 `references/prompt-templates.md` 的模板 + glossary 每条 `usage` 句式，拼成一段可粘贴给 AI 的完整需求。**同一句话里把层讲全**：结构 + 布局 + 控件 + 反馈 + 外观。
4. **验收**：对照下方清单逐条过 AI 的产出，缺的让 AI 补。

## 验收清单（AI 交付后逐条打勾）

**存在性**
- [ ] 浏览器标签页有 `Title` + `Favicon`（页面元信息 4 件套：Title/Favicon/描述/Open Graph）
- [ ] 关键操作有 **loading/禁用态**，防连点（提交按钮提交中置灰）
- [ ] **空数据**有空状态（Empty/Result），**加载中**有 Skeleton/Spinner
- [ ] 键盘可达：导航有 SkipLink，弹窗能 Esc 关

**职责正确**
- [ ] **按钮与链接不混**：提交/删除用 Button，带路用 Link
- [ ] 反馈分轻重：破坏性操作用 **Modal 确认**，轻提示用 **Toast/Notification**，别全叫"弹窗"
- [ ] 表单每栏有 `label`，必填/格式有校验与错误提示

**兜底**
- [ ] 误操作可 **Undo**（删除/危险动作）
- [ ] 移动端不破版（若需要响应式）

## 查词与核对

- 术语全表：`references/glossary.md`（159 词，按集分章，每词 = en｜zh｜定义｜要点｜给 AI 的句式｜代码｜避坑）
- 需求模板：`references/prompt-templates.md`
- 要回到原视频核对：`bilibili-video-extract` 技能；原始逐字稿已归档在 `~/VibeCoding术语课/逐字稿/`，原始素材在 `/tmp/vibe_course/`（重启会清）
