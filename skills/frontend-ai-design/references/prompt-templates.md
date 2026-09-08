# 给 AI 的需求模板（prompt templates）

> 用法：复制模板 → 填空 → 术语照 glossary 用词 → 尾部附"验收句"。
> 原则：**一段话把 结构→布局→表单/控件→反馈→外观→交互 讲全**；中英夹杂用词 AI 最懂（switch、modal、toast 直接说）。

## 模板 A：通用骨架（先写这段，再按页面类型追加）

```
做一个【页面类型，如：活动报名页/产品落地页/数据看板】，目标用户【谁】，核心动作【如：报名/下单/看报表】。

结构：页面分【大件，如 Navbar / Hero / 主体 / Footer】几大块。
布局：【布局词，如：居中窄栏 / 栅格 / 分屏】。
【按需追加下面的表单段 / 列表段 / 反馈段 / 外观段 / 交互段】

验收：补 Title 和 Favicon；按钮有 loading/禁用态防连点；空数据有空状态；
危险操作弹确认（Modal），轻提示用 toast；表单每栏带 label 和校验；
移动端别破版。技术栈：【React? Vue? 原生? 组件库?】
```

## 模板 B：表单 / 报名页（源自 03/05 集）

```
做一个报名页，表单包含：
- 姓名（Input，label 写"姓名"，必填）
- 手机号（Input，格式校验 11 位）
- 意向课程（Radio 单选，或 select 下拉）
- 备注（Textarea，选填，placeholder 提示"还有什么想说的"）
提交按钮做成主要按钮（Button），提交中置灰防连点；
成功后 toast 提示，失败在对应字段旁显示错误。
```

## 模板 C：后台数据 / 列表页（源自 06/10/08 集）

```
做一个订单管理页：
- 顶部：搜索框（SEARCH）+ 筛选（Filter：状态/时间）+ 排序（sort）
- 主体：Table 展示订单，列含【状态用 Tag 着色、用户 Avatar+姓名】
- 空数据用 Empty，首次加载用 Skeleton
- 操作列：详情（Link）、删除（危险操作，Popconfirm 二次确认）
- 底部：Pagination 分页；页头带 Breadcrumb（首页 / 订单管理）
- 删除后 toast 提示并支持 Undo（撤销）
```

## 模板 D：营销落地页（源自 11 集网页 10 大件）

```
做一个产品落地页，按顺序：
Hero（一句主标题+副标题+主 CTA 按钮）→ 一个 CTA 就够，别贪多 →
SocialProof（数据/logo 墙）→ 3 张卡片 Feature（特性）→
UserVoice（用户评价）→ Pricing（三档，中间档标"最受欢迎"）→ FAQ → Footer。
配色与字体风格：【指定或说"参考 popular-web-designs 的 XX 风"】。
```

## 模板 E：内容社区 / 动态流（源自 06/07 集）

```
做一个活动动态页：
- 主体：Card 列表（Cover 图 + Avatar + 昵称 + 时间 + Tag）
- 内容多的卡片折叠（Collapse）；热门分类用 Tabs 切换
- 加载更多：下滑自动加载，加载中底部显示 Spinner
- 顶部轮播（Carousel）放精选内容
```

## 外观 & 交互段（追加在任意模板后，源自 13/14/15 集）

```
外观：用 Design Token 统一（主色 #__、间距 4 的倍数、圆角 8px、卡片阴影轻）；
标题用衬线/无衬线【选】，正文 14-16px；关键信息靠 Contrast 拉开层级；
支持 Dark Mode（用语义 token，别写死颜色）。
交互：按钮 hover 有过渡（transition 150ms）；打开弹窗 fade in；
禁用态用 Disabled 样式；下拉、评分这些用系统原生控件效果即可。
```

## 验收句（放需求最后，源自 02 集验收标准）

```
页面完成后自查：浏览器标签有 Title/Favicon；主要操作有 loading 与防连点；
空/错/加载三态齐全；删除有确认与 Undo；键盘可操作（SkipLink/aria）；
提交类动作用 Button 不用 Link。
```

## 避坑速记（源自各集 pitfall）

- 提交/删除 = Button；带路 = Link。别把提交做成链接。
- 反馈分轻重：Modal 管"打断确认"，Toast 管"轻提示"，别都叫弹窗。
- 值复杂程度决定控件：布尔 switch、连续值 slider、多级树 cascader/tree-select。
- label 必须配 input（可点小字聚焦）；placeholder 只是灰字提示，不能替代 label。
- 密钥/权限/价格规则别放前端；"保存成功"别写死，状态来自真实结果。
- 前端"看不见"的事（查库/校验/写入）都属于后端，提醒 AI 走接口。
