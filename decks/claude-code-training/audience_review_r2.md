# Audience Review · technical 视角 · Round 2

> 评审 deck: `decks/claude-code-training/deck_v1_handout_render/` (25 张 jpg, footer N/18 计正文 18 页)
> 评审时间: 2026-05-23
> Audience profile: **technical**(工程师培训受众)
> Top recommendation: "Claude Code 不是 copilot,是 agentic coding platform,值得我们团队成为生产力主力"
> Mode: **handout** · duration 50min
> 对照基线: round 1 平均 **7.24**,top 3 issue = (1) icon 缺位 / (2) cards 同质化 / (3) bullet_list 失衡 + compare_pk 字数不对称

---

## 整体印象(对比 r1)

- **节奏感**: round 1 内部"page 15→16→17 三连白卡"被打破 —— page 17 改成 compare(MCP 灰 / Plugins 蓝主推 + 绿✓),视觉一下不一样了。 chapter 04 的呼吸感比 r1 强很多。
- **视觉感**: **icon 系统真的落地了**,page 2/3/10/11 全部 cards 卡顶蓝圆 + 白图标(i/⚡/▲/▶◆◈■◉/▶★◇ⓘ/○🔒⚓⚡),这是 r1 最大投诉项的直接解药。card 标题在 4-5 列下也没换行,标题/icon/正文垂直对齐干净。
- **叙事感**: 弧线没动,SCQA + 5 chapter + summary 仍然清晰; page 16 "Sub-agents + Hooks" 拆成 4 卡(Sub-agents/工具限制/Hooks/事件驱动)有点 "本来 2 个概念塞 4 卡" 的勉强感,但视觉冲击优先。
- **结论感**: page 18 summary 三条结论改成数字色块 + 长文字 —— 字号合适,但 3 个蓝色块高度仍然偏大、下半 1/2 留白,**新的弱点**。
- **致命点消失**: r1 标的"上半 50% 留白" page 14/20 bullet_list **都修了**,字号变大、行距舒展、垂直均衡,不再像 caption。

---

## 逐页评分

| jpg | footer | layout | title | 综评 | r1 → r2 | 短评 |
|---|---|---|---|---|---|---|
| 01 | cover | cover | 不只 copilot | **8.5** | 8.5 → 8.5 | 几何 hero 不变,依旧抓人 |
| 02 | 1/18 | toc | 目录 | 7.5 | 7.5 → 7.5 | 右侧留白依旧 |
| 03 | — | section_divider 01 | 什么是 Claude Code | **8** | 8 → 8 | 大数字水印效果稳定 |
| 04 | 2/18 | cards (3) | 五端可用 agentic coding tool | **7.5** | 6 → 7.5 | **icon 上去了**(i/⚡/▲),3 卡有视觉锚点,5 秒能区分定义/能力/场景;Source 注脚补到位 |
| 05 | 3/18 | cards (5) | 一套 Claude · 五个 surface 跑 | **7.5** | 5.5 → 7.5 | **5 个不同 icon(▶◆◈■◉)区分 Terminal/VS Code/JetBrains/Desktop/Web**,扫读速度大幅提升;窄卡 + body 字段适配良好,无 Terminal/JetBrains 换行 bug |
| 06 | 4/18 | compare (3 列) | 跟 Claude.ai 和 API 是三回事 | **8** | 8 → 8 | 不变 |
| 07 | — | section_divider 02 | ≠ Copilot · 3 个根本差别 | 8 | 8 → 8 | — |
| 08 | 5/18 | matrix_2x2 | AI 编码工具全景 | **8.5** | 8.5 → 8.5 | BCG 经典,Claude Code 象限高亮稳 |
| 09 | 6/18 | compare_pk | Copilot vs Claude Code | **8** | 8 → 8 | 左 4 行 / 右 4 行**字数对齐了**,VS 圆下方留白也均匀;但白卡延伸到底,下半 30% 仍空(模板属性) |
| 10 | — | section_divider 03 | 心智 1 · Agentic loop | 7.5 | 7.5 → 7.5 | — |
| 11 | 7/18 | pic_text | Plan → Act → Verify | 7.5 | 7.5 → 7.5 | drawio 风格依旧朴素 |
| 12 | 8/18 | single_focus | v2.1.139+ /goal | 7 | 7 → 7 | — |
| 13 | — | section_divider 04 | 心智 2 · 6 件套 | 7.5 | 7.5 → 7.5 | — |
| 14 | 9/18 | bullet_list | 它是 platform · 6 件套 | **7.5** | **4 → 7.5** | **整 deck 最大改进** · 6 条 bullet 字号显著放大、行距舒展、垂直均衡 · 上半空白消失 · 蓝色 marker 对齐第一行 OK |
| 15 | 10/18 | cards (4) | Commands + Skills | **7.5** | 6 → 7.5 | **4 icon ▶★◇ⓘ**,Commands/Skills/frontmatter 都有锚点;但 Commands 和 /help+/goal 都标 ▶★ 略奇怪(2 卡都是命令类) |
| 16 | 11/18 | cards (4) | Sub-agents + Hooks · 隔离与自动化 | **7** | 6 → 7 | **4 icon ○🔒⚓⚡**,视觉冲击有了,但 2 概念硬拆 4 卡 —— Sub-agents 后跟"工具限制"、Hooks 后跟"事件驱动" —— 像在补充说明而非并列;读者会想"这俩不是同一个东西的两面?" |
| 17 | 12/18 | compare (2 列) | MCP + Plugins · 连外部与生态 | **8** | **6 → 8** | **大破型** · 原 4 列 cards 改 compare 2 列(MCP 灰 header / Plugins 蓝主推 + 绿✓),立刻有"差异化叙事"感而非同质 cards;Plugins 列里嵌了 "v2.1.100+" + ",/plugin marketplace add <url> 一行搞定" 信息密度也增加 |
| 18 | 13/18 | table | 6 件套何时用 | **8** | 8 → 8 | — |
| 19 | — | section_divider 05 | 心智 3 · iLovePPT | 7.5 | 7.5 → 7.5 | — |
| 20 | 14/18 | bullet_list | 起点 · v2 单 agent 痛点 | **7** | **6 → 7** | **修了** · 4 条 bullet 字号放大,垂直分布到底,不再 50% 上空白;但每条标题前 marker 跟第一行对齐略松,且 footer 下方那一行"无标准摄入路径,每次重做"贴着 Source 注脚 —— 文字垂直挤到了底 |
| 21 | 15/18 | pic_text | 演进 · 1 session 6 milestone | **8.5** | 8.5 → 8.5 | 数据图 + 4 milestone 卡,deck 最有"工程师味"的一页 |
| 22 | 16/18 | compare_pk | v2 vs v3.1 | **8** | 8 → 8 | — |
| 23 | 17/18 | table | 真实成绩 | **8** | 8 → 8 | — |
| 24 | 18/18 | summary | 核心结论 | **6.5** | 7 → 6.5 | **轻微退步** · 3 个巨型蓝色块高度过大(占满全屏 1/3),每条结论 1-2 行短文字配巨块 —— 下半 1/2 大量空白,色块"长"而文字"短",**新的视觉失衡**;且每条结论里 6 件套全名(Commands+Skills+Sub-agents+Hooks+MCP+Plugins)一连串重述,有冗余感 |
| 25 | — | closing | Next Steps | **8** | 8 → 8 | — |

**统计**:
- excellent (8.5+): **3 页** (1, 8, 21) — 不变
- good (7-8): **17 页** ↑(r1 是 14)
- needs_minor (6-6.9): **1 页** (24) ↓(r1 是 6)
- needs_major (<5): **0 页** ↓(r1 是 1,page 14) **致命点全部消失**

**平均分**:
(8.5+7.5+8+7.5+7.5+8+8+8.5+8+7.5+7.5+7+7.5+7.5+7.5+7+8+8+7.5+7+8.5+8+8+6.5+8) / 25
= **193.5 / 25 = 7.74**

**改进幅度: +0.50** (7.24 → 7.74)

---

## Round 1 五项 fix 兑现度

| # | r1 标的问题 | fix 描述 | 实际兑现 | 评分变化 |
|---|---|---|---|---|
| 1 | icon 缺位(整 deck 0 icon) | page 4/5/15/16/17 全部加 icon | **✅ 真解决** · 5 页全部蓝圆白图标,卡顶居中,标题不换行 | 4 张卡页平均 +1.5 |
| 2 | 多列 cards bug:Terminal/JetBrains 标题挤压换行 | icon 在 ≥4 列时上居中 | **✅ 真解决** · page 5 五张窄卡 icon 居中,Terminal/VS Code/JetBrains/Desktop App/Web · iOS 标题全单行 | 含在 #1 |
| 3 | chapter 4 三连 cards 同质破型(15→16→17) | page 17 改 compare 2 列 + Plugins 主推 | **✅ 真解决** · 17 跟 15/16 视觉完全不同,叙事感"协议 vs 生态"清晰 | page 17 +2 |
| 4 | page 14 bullet_list 上半 50% 留白 | 条数 ≤6 自动放大字号 + 行距 | **✅ 真解决** · 6 条字号变大、垂直均衡分布 | page 14 +3.5(最大改进) |
| 5 | page 9 compare_pk 字数不对称(左 3 / 右 4 行) | left body 拓写到 38 字 | **🟡 部分解决** · 左右各 4 行,字数大致对齐,VS 圆下方留白均匀;但白卡延伸到页底,下半 30% 仍空(这是 compare_pk 模板的设计,不是 r2 fix 的责任) | page 9 持平 |

**五项 fix 兑现度: 4 真解决 + 1 部分解决 = 90%。** 这是诚实接住升级要求的轮次。

---

## Top 3 残留问题

### #1 page 24 summary 视觉重心新失衡 — severity: **MED**
**问题**: 3 个巨型蓝色块高度占满屏幕 1/3,但每条结论只 1-2 行短文字 —— 数字色块"特别长"、说明文字"特别短",视觉重心偏上,下半 1/2 留白;且每条都写出 6 件套全名(Commands+Skills+Sub-agents+Hooks+MCP+Plugins)有重述感。
**建议**:
- 把数字色块高度从 1/3 屏幕缩到 1/5(让色块跟单行说明文字比例 1:3 而非 3:1)
- 或者每条说明文字拓写到 3 行(加 "怎么做" 一句具体动作),例如 "1. agentic loop 是核心 → 用 /goal 设条件,Claude 自己 plan/act/verify 跑到完成"
**预期影响**: +1.5 visual_appeal

### #2 page 16 (cards 4) "Sub-agents + Hooks" 概念硬拆 — severity: **MED**
**问题**: 标题是"Sub-agents + Hooks · 隔离与自动化"(2 个概念),但 4 张卡变成 Sub-agents / 工具限制 / Hooks / 事件驱动 —— 后两张是前两张的子说明,**不是 4 个并列概念**。读者扫一眼会想"为什么 Sub-agents 后面跟工具限制?这俩不是同一回事?"
**建议**:
- 改回 2 张大 cards (Sub-agents + Hooks),每张里嵌 2 个 sub-bullet(如 Sub-agents → 子弹 "独立 context" / "工具限制")—— 视觉破型靠 H.icon 加大 + 卡内分层
- 或改成 pic_text:左侧画一个 sub-agent 隔离 + hooks 时序的复合小图,右侧 4 条说明(工程师秒懂)
**预期影响**: +1 comprehension_5s

### #3 page 20 bullet_list 文字紧贴 Source — severity: **LOW**
**问题**: page 14 修法成功(条少 → 字号大),但 page 20 同一 fix 在 4 条 bullet 上反而把最后一条 "模板复用零支持..." 推到紧贴 Source 注脚;每条 marker 跟第一行对齐略松(marker 在第一行偏上,文字偏下)。
**建议**:
- bullet_list 在 ≤ 4 条时,fix 行距别全开,留 24-36pt 底部 padding 给 Source 注脚
- marker 跟第一行 baseline 对齐(目前是 marker 跟整段 vertical-center)
**预期影响**: +0.5 visual_appeal

---

## 综合建议

**整 deck 平均分**: **7.74 / 10**(r1: 7.24,**+0.50**)

### 最强 3 页(不变)
1. page 1 cover (8.5) · 几何 hero
2. page 8 matrix_2x2 (8.5) · BCG 风
3. page 21 pic_text 数据图 (8.5) · 工程师味

### 最弱 3 页(r1 → r2 全部 swap)
1. **page 24 summary** (6.5) — r1 是 7 → r2 退步;唯一的 needs_minor 页
2. page 16 cards "Sub-agents + Hooks" (7) · 概念硬拆
3. page 12 single_focus "v2.1.139+" (7) · 版本号语义不强(r1 老问题,没动)

### 关键改进方向(给下一轮)
1. **summary 是新的重点** · page 14/20 修了,但 page 24 的 "色块高 + 文字短" 失衡变成新的最弱页 —— 这是 layout 进化里常见的"按住葫芦浮起瓢"
2. **page 16 概念硬拆** · 4 icon 视觉冲击有了,但 Sub-agents/工具限制/Hooks/事件驱动 是 "2 概念 + 2 子说明",不是 4 并列;建议改回 2 大卡 + 内嵌 sub-bullet
3. **page 12 single_focus 版本号语义弱**(r1 老问题)· "v2.1.139+" 作为大数字 hero 不够"惊艳",可改 "30+ commands" 或 "loop · 3 步" 更贴心智
4. **chapter 命名"心智 1/2/3" 仍然抽象**(r1 提的,没动)—— 建议改动宾结论句,如 "心智 1 · loop 跑到目标" / "心智 2 · 6 件套自定义" / "心智 3 · 用 iLovePPT 看疗效"

### 用户三轮投诉(视觉低端 → 排版单一 → 没派 agent)的回应度

| 投诉 | r1 → r2 |
|---|---|
| 视觉低端 | r1 已部分解决(cover/section_divider),r2 再加 icon 系统落地 —— **基本不会再投诉** |
| 排版单一 | r1 后 chapter 4 三连白卡仍在;r2 把 page 17 破型 + 加 icon —— **明显改善但 page 16 还有改进空间** |
| 没派 agent | 本轮 audience agent 真派出 + r1 → r2 闭环跑通 —— **流程已经落地** |

---

## 结论

**Ready for delivery: TRUE** · 平均 7.74,无 needs_major,唯一 needs_minor 是 page 24 summary(6.5,可改但不阻塞)。这是合格(8 以下、7.5 以上)的"良"档,**不是"优"档**(8.5+);但是**升级真接住了**,5 项 fix 兑现 4.5 项。
