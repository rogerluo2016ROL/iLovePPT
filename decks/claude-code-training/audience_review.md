# Audience Review · technical 视角

> 评审 deck: `decks/claude-code-training/deck_v1_handout_render/` (25 页 jpg)
> 评审时间: 2026-05-23
> Audience profile: **technical**(工程师培训受众)
> Top recommendation: "Claude Code 不是 copilot,是 agentic coding platform,值得我们团队成为生产力主力"
> Mode: **handout**(培训材料,有讲义性质)
> v0.5.0 视觉升级背景:cover 几何 hero / section_divider 400pt 背景数字 / compare header-bar 重写 / 新增 compare_pk + matrix_2x2 / icon 系统(deck_plan 未用)

---

## 整体印象

- **节奏感**: section_divider 大数字水印 + chapter 小字升级**确实有效**,5 个章节切换有视觉重击,这是这一版最大的进步。但内容页 (page 4 / 5 / 10 / 11 / 12) 连续 cards-like 同质化**依然严重** —— 滚动看一眼分不清是哪一节。
- **视觉感**: v0.5.0 该用的新 layout 几乎都用上了 (compare_pk 出现 2 次、matrix_2x2 出现 1 次、compare header-bar 出现 1 次),但 cards 还是占主体(5 页连排白卡)。最致命的是**icon 系统完全没落地**,所有 cards 还是「标题 + 段落」无视觉锚点,跟 v0.4 时代的"长得一样"。
- **叙事感**: cover → toc → 5 chapters → summary → closing 弧线清晰,SCQA 在 page 4 (Claude Code vs ai vs API) 隐含交代,page 16 (compare_pk v2 vs v3.1) + page 17 数据表收口扎实。但 page 8 single_focus "v2.1.139+" 和 page 12 "v2.1.100+" 出现两次大版本号 single_focus,**节奏重复**,读者会觉得"又是版本号大字"。
- **结论感**: page 18 summary 三条结论用 1/2/3 蓝色色块 + 单段长文字,**视觉强但文字密度偏高**(每条都两三行),典型 handout 写法但屏幕投影会被吐槽;page 19 closing 极简 dark 蓝底回归 cover 风,首尾呼应到位。
- **致命点**: page 9 ("6 件套" bullet_list) 上半留白几乎占 50% 的版面,6 条信息挤在下半,**视觉重心严重失衡**,这是整 deck 最弱的一页。

---

## 逐页评分

| # | layout | title | 综评 | 短评 |
|---|---|---|---|---|
| 1 | cover | Claude Code · 不只是 copilot | **8.5** | 同心圆 + 网格 hero 视觉升级到位,标题抓人,deep navy + 绿 accent line 有品味;subtitle "它是 agentic coding platform" 略平,但够清 |
| 2 | toc | 目录 | 7.5 | 5 章节蓝色编号清爽,行距舒展;但右侧 50% 留白浪费,可加章节缩略图或时间轴装饰 |
| 3 | section_divider 01 | 什么是 Claude Code | **8** | 400pt 背景 "01" 水印 + CHAPTER 01 小字 + 蓝竖条,层次感比 v0.4 强很多,这是升级最成功的 layout |
| 4 | cards (3) | 五端可用的 agentic coding tool | 6 | 3 张同质白卡 "定义/能力/场景",card title 加粗够大,但 body 都是中文密文字,**5 秒抓不到差异**;无 icon |
| 5 | cards (5) | 一套 Claude · 五个 surface 跑 | 5.5 | 5 张窄白卡视觉同质度最高的一页,工程师扫一眼只觉"5 个产品",**记不住差异**;最该加 icon 但没加 |
| 6 | compare (3 列, recommended) | 跟 Claude.ai 和 API 是三回事 | **8** | 新 compare 蓝 header bar + Claude Code 列蓝主推 + 绿 ✓ 徽章,主张明确,视觉拉开;3 列字数对齐 OK |
| 7 | section_divider 02 | ≠ Copilot · 3 个根本差别 | 8 | 同 page 3,大数字水印有效 |
| 8 | matrix_2x2 | AI 编码工具全景 · Claude Code 占哪格 | **8.5** | BCG 风 2×2 矩阵,Claude Code 象限浅蓝高亮,**轴标签"主动干任务/被动给建议"清晰**,这是新 layout 最成功的应用,工程师会立刻看懂 |
| 9 | compare_pk | Copilot vs Claude Code · 同 AI 但本质不同 | **8** | 巨型 VS 圆 + 两侧白卡,视觉冲击强;但左侧 body 文字偏短(3 行)、右侧 4 行,**字数不对称**,VS 圆下方两边留白也不均匀 |
| 10 | section_divider 03 | 心智 1 · Agentic loop | 7.5 | 标题"心智 1"略抽象,3 个 section_divider 标题"心智 1/2/3"的命名重复,**首次读者搞不清"心智"是啥** |
| 11 | pic_text | Plan → Act → Verify · 闭环跑到目标 | 7.5 | 左侧 drawio 流程图清晰、4 个点说明卡分类得当;但流程图风格简朴(蓝白方块 + 黑箭头),**跟 deck 整体精致度略不匹配**,流程图字号略小 |
| 12 | single_focus | v2.1.139+ /goal "全测试过再停" | 7 | 蓝色 "v2.1.139+" 大字够冲击,但**版本号作为大数字的语义不强**(版本号本身不是"惊艳数字");/goal 副标在下方略小,可放大 |
| 13 | section_divider 04 | 心智 2 · 6 件套扩展能力 | 7.5 | 同 page 10 |
| 14 | bullet_list | 它是 platform · 不是 chat · 6 件套 | **4** | **整 deck 最致命的一页**:6 条 bullet 挤在下半部分,**上半空白接近 50%**;6 条 bullet 平铺无层级、无视觉锚点,工程师扫一眼会想"为什么不画个图分组"。这页内容是 deck 的核心 platform 论点,被弱呈现拖垮 |
| 15 | cards (4) | Commands + Skills · 触发与复用 | 6 | 4 张同质白卡,跟 page 4/5 视觉雷同;Commands/Skills 是核心卖点之一,应该有图标或 code snippet 锚点 |
| 16 | cards (4) | Sub-agents + Hooks · 隔离与自动化 | 6 | 同 page 15,4 列同质白卡;Hooks 是技术受众最关心的钩子机制,**配个事件流图或时序图会强很多** |
| 17 | cards (4) | MCP + Plugins · 连外部与生态 | 6 | 同 15/16,**第三页连排 4 列白卡**,严重触发 v0.4 的"≥ 2 张 cards-like 连续警告"硬规则,典型同质化 |
| 18 | table | 6 件套何时用 · 一表速查 | **8** | 3 列 6 行表格,header 深蓝 + 行交替浅灰,典型"速查表"风,handout 场景非常合适;字号舒服 |
| 19 | section_divider 05 | 心智 3 · 真实 case · iLovePPT | 7.5 | 同 page 10/13 |
| 20 | bullet_list | 起点 · v2 单 agent 痛点真实存在 | 6 | 4 条 bullet 在下半部,上半 50% 空白,**跟 page 14 的失衡问题如出一辙**;痛点列表如果配 v2 旧架构 diagram 会强 10 倍 |
| 21 | pic_text | 演进 · 1 session 6 milestone | **8.5** | 双轴折线 + 柱状 matplotlib 图清晰、右侧 4 个里程碑说明卡;这是 deck 最有"工程师味"的一页,**Plan/Tests/Agents 三条数据线** + commits 67/tests 26/agents 4/release 2 数字硬实,可信度高 |
| 22 | compare_pk | v2 vs v3.1 · 架构演进对决 | **8** | 跟 page 9 同 compare_pk 风格,VS 圆 + 两侧白卡;左右字数也不太均匀,但叙事强(单 agent → 三 agent) |
| 23 | table | 真实成绩 · 1 个 session 跑出 | **8** | 3 列 5 行数据对比表,数字硬,v2 起点 vs v0.2.0 终点,典型咨询风 before/after |
| 24 | summary | 核心结论 | 7 | 1/2/3 蓝色大色块 + 单段长文字,**视觉强但每条文字太密**(2-3 行),不像 takeaway 像段落;每条都含 6 件套全名,有"再复述一遍"嫌疑 |
| 25 | closing | Next Steps | **8** | 回归 cover dark navy + 绿色编号,3 条 next step + 时间标记 [本周/本月/下月] 落地感强;首尾呼应到位 |

**统计**:
- excellent (8.5+): 3 页 (1, 8, 21)
- good (7-8): 14 页
- needs_minor (5.5-6.5): 6 页 (4, 5, 15, 16, 17, 20)
- needs_major (<5): 2 页 (9 = page 14, 19 = page 20 bullet 失衡;严格说 page 14 = 4 分 = 唯一 needs_major)

平均分: **(8.5+7.5+8+6+5.5+8+8+8.5+8+7.5+7.5+7+7.5+4+6+6+6+8+7.5+6+8.5+8+8+7+8) / 25 = 181 / 25 ≈ 7.24**

---

## Top 3 必改

### #1 page 14 (bullet_list "它是 platform · 6 件套") — severity: **HIGH**

**问题**:
- 整 deck 最弱的一页,**上半 50% 版面纯白浪费**,6 条 bullet 全堆在下半
- 6 件套是 deck Chapter 04 的开场页 + 核心 platform 论点的承载页,**被弱呈现拖垮**
- 6 条 bullet 平铺无层级,跟 page 18 "6 件套何时用" 表格信息重复

**建议**:
- 改成 `pic_text`,左侧画一张 6 件套生态图(中心 Claude → 6 卫星 Commands/Skills/Sub-agents/Hooks/MCP/Plugins),右侧 6 条简短说明;draw.io 半小时可画
- 或者:用 `cards` 6 张,每张配一个 H.icon (deck_plan 还没用上 v0.5.0 新增的 icon 系统,正是用武之地)
- 或者:整页改成 single_focus "Platform = 6 件套",大数字 6 + 6 件套名字小字横列,page 15-17 cards 再展开细节

**预期影响**: +3 visual_appeal, +2 comprehension_5s, +1 flow_coherence(承上启下到 15-17 cards 更自然)

---

### #2 page 5 + 15 + 16 + 17 (4-5 张连排 cards) — severity: **HIGH**

**问题**:
- page 5 (5 列 cards "五个 surface")
- page 15 (4 列 cards "Commands + Skills")
- page 16 (4 列 cards "Sub-agents + Hooks")
- page 17 (4 列 cards "MCP + Plugins")

**4 页连续多列白卡**,虽然中间隔了 section_divider,但 chapter 04 内部 page 15→16→17 **是 3 张连排 cards** —— 直接触发 content-writing.md 的"≥ 2 张 cards-like 连续 → 警告"硬规则;扫一眼眼睛找不到差异落点。

**建议**:
- v0.5.0 新增的 H.icon 系统就是为这场景设计的,**立即给每张 card 配 24-32pt 的 icon**:
  - Commands → ▶ (Terminal/run)
  - Skills → ◇ (modular block)
  - Sub-agents → ◯ (isolation/circle)
  - Hooks → ⚓ (anchor) 或 → (arrow)
  - MCP → ◈ (diamond/protocol)
  - Plugins → ⊕ (plus/extend)
- page 16 (Sub-agents + Hooks) 最适合换 `pic_text` —— 画一个 sub-agent 隔离上下文 + hooks 事件时序的小图,工程师秒懂
- page 17 (MCP + Plugins) 如果改 `compare` (左 MCP / 右 Plugins, header bar 风) 比 4 列 cards 视觉冲击强

**预期影响**: +3 visual_appeal, +2 comprehension_5s (有锚点后扫读速度翻倍)

---

### #3 page 9 (compare_pk) + page 20 (bullet_list 失衡) — severity: **MED**

**page 9 问题**:
- compare_pk 视觉骨架很好(巨型 VS + 两侧白卡)
- 但**左右 body 字数严重不对称**(左 3 行/右 4 行),VS 圆下方两边的留白也不均匀
- 视觉是 compare_pk 但骨子里破了对称感

**page 20 问题**:
- 跟 page 14 一样,上半 50% 留白,bullet 挤下半
- "v2 痛点"是 chapter 05 (iLovePPT case) 的关键铺垫,被弱呈现稀释了说服力

**建议**:
- page 9 左侧 body 拓写 1 句话 (28 字 → 38 字) 跟右侧对齐;或反之裁右侧
- page 20 改成 `pic_text`,左侧贴一张 v2 单 agent 上下文膨胀图 (matplotlib 一根上升曲线即可),右侧 4 痛点
- 或 page 20 改 `compare` 2 列:左"v2 痛点"4 条 + 右"v3.1 解法"4 条,主推右列,直接顺到 page 22 v2 vs v3.1 PK

**预期影响**: +1.5 visual_appeal, +1 flow_coherence

---

## 综合建议

整 deck 平均分: **7.24 / 10**

### 最强 3 页
1. **page 1 cover** (8.5) — v0.5.0 几何 hero 升级最成功
2. **page 8 matrix_2x2** (8.5) — 新 layout BCG 矩阵,工程师秒懂
3. **page 21 pic_text 数据图** (8.5) — 数据硬、双轴折线说服力强

### 最弱 3 页
1. **page 14 bullet_list "6 件套"** (4) — 上半空白 + 核心论点被弱呈现
2. **page 5 cards (5)** (5.5) — 5 张窄白卡同质化严重
3. **page 20 bullet_list "v2 痛点"** (6) — 跟 page 14 同失衡问题

### 关键改进方向

1. **icon 系统是用户上一轮投诉"视觉低端"的核心解药,但本版完全没落地** —— v0.5.0 helper 加了 icon 但 deck_plan 没用上。立即在 page 4/5/15/16/17 5 张 cards 加 icon,可以一举消除"4 张白卡连排"的同质化体感,这是最高 ROI 的改动。
2. **page 14 + page 20 bullet_list 的上半空白失衡** 是当前 build.py 的 layout bug(还是 author 的 content 太短?),需要查 themes/make_bullet_list 是否有"top-align"vs"vertical center"的选项;**或者主线程应该在 author 阶段强制 bullet_list ≥ 5 条且每条 ≥ 12 字以填满版面**,否则降级用 cards 4 列。
3. **chapter 04 (page 13-18) 内部 page 15/16/17 三张连排 cards 是节奏重灾区** —— 建议至少 1 页换 layout(pic_text 或 compare),即使加 icon 也只能缓解,根治是 layout 多样化。
4. **page 10/13/19 三个 section_divider 标题 "心智 1/2/3"** 命名抽象,首次读者(尤其外部工程师)分不清"心智"是啥;建议改成动宾结论句,如 "心智 1 · loop 跑到目标" / "心智 2 · 6 件套自定义" / "心智 3 · 用 iLovePPT 看疗效"。

### 用户上一轮"视觉低端"投诉的回应度

- **section_divider 大数字水印 + cover 几何 hero**: 明显解决了"PPT 看起来像 Word"的低端感,**这部分升级成功**
- **compare_pk + matrix_2x2 新 layout**: 单点冲击强,但只在 page 8/9/22 出现 3 次,**频次不够**
- **cards 同质化 + icon 缺位**: **没解决**,这是用户最容易再投诉的点,**v0.5.0 的 icon 系统必须立即在 deck_plan 里启用**

如果不解决 cards 同质化,即使 cover/section_divider 升级了,用户大概率还会有"中间内容页看上去都一样"的二次投诉。
