# Audience Review · R2 · general(E+T+G 分层评判)视角

> 评审 deck: `decks/claude-code-training/deck_v1.pptx`(36 页)
> 评审时间: 2026-05-24
> Audience profile: **general**(主线程合并 a+b+c 三类,按 general 处理;E/T/G 分层校验)
> Top recommendation: 本季度 3 周全员上手 Claude Code · 工程 100% / 产品 50% / 高层 Deep Research · 公司统一 skill 库
> Mode: handout(60 min 内部培训,无现场讲者)
> Iteration: **2 / 5**
> Prev R1 score: 7.55 / 10

---

## TL;DR

**Overall: 8.1 / 10** —— **不达 9.0 硬阈值,verdict = needs_minor_revision**。

R1 → R2 三项重灾区全部明显修复(Top 1 → +2.5/页 · Top 2 → +1.75/页 · Top 3 → +1.75/页),整 deck 平均分从 7.55 → 8.1(+0.55)。但**仍有 3 项扣分**让总分卡在 9 以下:

1. **TBD 3 页(p20/21/23)**:body 已升级有意义,但 **title 仍含 "[待 W1/W2 回填]"** 红字,executive 一眼读到仍然会反应"这是占位页吗?"。同时 compare_pk 卡片视觉上 60% 空白(content 只填顶部 1/3)
2. **p7 SWE compare + p29 W1/W2/W3 bullet 上半页大片空白**:handout mode 60min 场景下,这两页 content 只占顶部 1/4,视觉上像"未填满"
3. **p26 ✓ badge 与 "Claude Code(推荐)" title 文字仍重叠** + **p6 chart M6 标签与 source caption 仍堆叠** ——两项 R1 已 flag 为 `needs_theme_fix`,designer R2 按 handoff 规定未动。这两项不解决,即使 author rewrite 完也压不到 9

---

## R1 → R2 Delta 评估

### ✅ Top 1 · p20/21/23 TBD 3 页(R1: 3.5 → R2: 6.0,每页 +2.5)

| 页 | R1 状态 | R2 状态 | 是否 fix |
|---|---|---|---|
| p20 Bug 修复 | 整页 [待回填] 空盒 | 传统流程 找 root cause→改代码→自测→CR · 2-4h vs /explain→CC 改→试跑→PR · **预估 4-8× 提速** + source "预估值·实测见 W1 工程试点" | **部分 fix(body ✓ · title 仍 [待 W1 回填] ✗)** |
| p21 Refactor | 同上空盒 | 传统:理解旧→设计新→改→测 · 4-8h vs /plan→CC 改→grep→验证 · **预估 8-12× 压缩** + source | 同上 |
| p23 调研 | 同上空盒 | 传统:查文档→找数据→写大纲→整理 · 3-6h vs 1 次完整 prompt→CC 调 web/docs→draft→人审 · **预估 6-10× 压缩** + source | 同上 |

**结论**:body 升级到位,3 页从"残缺品"提到"有数据估算+待验证"的可接受状态。但**title 仍是红字 [待 W1/W2 回填]**,executive 翻 deck 时一眼读到就会本能跳过。R2 仍有改进余地。

### ✅ Top 2 · 3 张嵌入 diagram(R1: 6.25-6.75 → R2: 8.25-8.5,每页 +1.5-2)

| 页 | R1 状态 | R2 状态 |
|---|---|---|
| p12 7 大能力 hub-spoke | 节点 label 6-8pt 不可读 | matplotlib 重画 · 顶部 3 层 header(基础/中层/扩展)+ 7 节点 3 色编码 + 中心 Claude Code 椭圆 · **labels 18pt 等效可读** |
| p14 Subagents + Agent Teams | 2 panel 挤一起 label 像素化 | matplotlib 重画 · 2 panel 各自标题 22pt + 主对话 vs Lead+Worker 双结构清晰 + 底部 takeaway 标签 |
| p32 Skill 库目录树 | drawio 双 panel 6pt paths | matplotlib 重画 · 左 panel monorepo 目录树 paths 12pt + 右 panel 5 步贡献流程 numbered circle |

**结论**:**完全 fix**。T 视角现在可以 dig into 这 3 张图,p12 / p32 尤其是 deck 里最技术核的两张,现在 carries weight。R1 → R2 最强一项改进。

### ✅ Top 3 · 5 个 section_divider → single_focus(R1: 5.5-6.25 → R2: 7.75-8.0,每页 +1.5-2)

5 页(p4/10/17/25/29)全部转 single_focus:橙红 /01-/05 + 深蓝 title + 灰 explanation 三段式居中。

**结论**:**完全 fix**。TEAM 卡通从 7 次→2 次(只留 cover + closing),executive 视觉疲劳源头消除,handout 翻阅顺。explanation 自动换行偶有断词(designer 已 flag cosmetic LOW),不致命。

---

## 整体印象(R2)

1. **节奏感**:5 章节弧线清晰,5 个 single_focus 章节扉页比 R1 的 section_divider 干净 ×3,翻阅时"咦这章在哪"的迷路感消失。
2. **视觉感**:橙红/深蓝/青绿三色主调统一,卡通 TEAM 只在 cover + closing 出现(2 次),executive 看的"BCG 稳重感"基本建立。
3. **数据感**:数字密度对 T 视角友好(SWE 80.8% / $1B / hub-spoke 7 力 / matrix 2×2 / 4-8×~8-12× 提效),source 全到位。
4. **致命短板**(R2 仍存):3 个 TBD 页 title 仍含 [待 W1/W2 回填] 红字 + p6/p26 两个 theme_fix 未解 = 即使本轮 author 再 rewrite 也压不下 9 分阈值。
5. **结尾收口**:p33 行动清单 · 今天 3 件事(9.25 — deck 最强页之一)+ p34 summary 4 核心结论 + p35 closing 三件事,落地强。

---

## 逐页评分

| # | layout | title(节选) | comp_5s | density | visual | flow | avg | verdict | R1→R2 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | cover | 让全员上手 Claude Code | 9 | 7 | 8 | 9 | **8.25** | good | +0.25 |
| 2 | single_focus | 3 周 · 本季度全员上手 | 10 | 8 | 9 | 9 | **9.0** | excellent | = |
| 3 | toc | 5 章目录 | 9 | 7 | 8 | 8 | **8.0** | good | = |
| 4 | single_focus | /01 AI 编程已变天 | 9 | 8 | 7 | 8 | **8.0** | good | **+2.5** ⭐ |
| 5 | single_focus | 95% 行业已变天 | 10 | 8 | 9 | 9 | **9.0** | excellent | = |
| 6 | pic_text(chart) | $1B run-rate | 8 | 8 | 6 | 8 | **7.5** | good | = |
| 7 | compare 2-col | SWE 80.8% + Most Loved 46% | 8 | 5 | 6 | 8 | **6.75** | needs_minor | -0.25 |
| 8 | cards 4-col | Accenture/Salesforce/Cog/PwC | 9 | 7 | 7 | 8 | **7.75** | good | = |
| 9 | cards 3-col | 公司三类落差 看/自/用 | 9 | 8 | 8 | 9 | **8.5** | good | = |
| 10 | single_focus | /02 7 力解构平台 | 8 | 8 | 7 | 8 | **7.75** | good | **+1.5** ⭐ |
| 11 | compare_pk | 不是补全·是 agentic 系统 | 10 | 8 | 9 | 9 | **9.0** | excellent | = |
| 12 | pic_text(diagram) | 7 大能力总览 hub-spoke | 9 | 8 | 8 | 9 | **8.5** | good | **+2.0** ⭐ |
| 13 | cards 3-col | Skills 是/为/怎 | 10 | 8 | 8 | 9 | **8.75** | good | = |
| 14 | pic_text(2-diagram) | Subagents + Agent Teams | 8 | 8 | 8 | 9 | **8.25** | good | **+2.0** ⭐ |
| 15 | cards 3-col | Hooks + Plugins + MCP | 9 | 8 | 8 | 9 | **8.5** | good | = |
| 16 | compare_pk | Anthropic 1 周→30 分钟 | 10 | 9 | 9 | 10 | **9.5** | excellent | = |
| 17 | single_focus | /03 工程 100%/产品 50% | 9 | 8 | 7 | 8 | **8.0** | good | **+1.75** ⭐ |
| 18 | pic_text(triangle) | 工程/产品/高层 分层 | 8 | 8 | 8 | 9 | **8.25** | good | = |
| 19 | cards 3-col | 工程师 任/P/协 | 9 | 8 | 8 | 9 | **8.5** | good | = |
| 20 | compare_pk **[TBD]** | 工程 Bug 修复 4-8× 提速 | 7 | 5 | 5 | 7 | **6.0** | needs_minor | **+2.5** ⭐ |
| 21 | compare_pk **[TBD]** | 工程 Refactor 8-12× 压缩 | 7 | 5 | 5 | 7 | **6.0** | needs_minor | **+2.5** ⭐ |
| 22 | cards 3-col | 产品/设计 P/原/数 | 9 | 8 | 8 | 9 | **8.5** | good | = |
| 23 | compare_pk **[TBD]** | 产品 调研 6-10× 压缩 | 7 | 5 | 5 | 7 | **6.0** | needs_minor | **+2.5** ⭐ |
| 24 | cards 3-col | 高层 行/竞/季 | 9 | 8 | 8 | 9 | **8.5** | good | = |
| 25 | single_focus | /04 Hybrid 是主流 | 9 | 8 | 7 | 8 | **8.0** | good | **+1.75** ⭐ |
| 26 | compare 3-col(recommended) | 三足鼎立 · CC 推荐 | 8 | 8 | 6 | 9 | **7.75** | good | = |
| 27 | matrix_2x2 | 规模决定工具 BCG | 9 | 8 | 9 | 10 | **9.0** | excellent | = |
| 28 | cards 3-col | Hybrid Stack 推荐 | 9 | 8 | 8 | 9 | **8.5** | good | = |
| 29 | single_focus | /05 3 周全员上手 | 9 | 8 | 7 | 8 | **8.0** | good | **+1.75** ⭐ |
| 30 | bullet_list | W1/W2/W3 节奏 | 8 | 5 | 6 | 8 | **6.75** | needs_minor | = |
| 31 | table | 3 周时间表 | 9 | 9 | 8 | 9 | **8.75** | good | = |
| 32 | pic_text(diagram) | 公司 Skill 库 目录+贡献 | 8 | 8 | 8 | 9 | **8.25** | good | **+1.5** ⭐ |
| 33 | cards 3-col | KPI 工程≥95% / 产品≥80% | 9 | 8 | 8 | 9 | **8.5** | good | = |
| 34 | cards 3-col | 行动清单 · 今天 3 件事 | 10 | 9 | 8 | 10 | **9.25** | excellent | = |
| 35 | summary | 核心结论 4 条 | 9 | 8 | 8 | 10 | **8.75** | good | = |
| 36 | closing | Thanks + W1 见 | 8 | 7 | 7 | 9 | **7.75** | good | = |

**汇总**:
- 平均分:**8.1 / 10**(R1 7.55 → R2 8.1,**+0.55**)
- excellent (≥9):6 页(p2, p5, p11, p16, p27, p34)—— 与 R1 持平
- good (7-8.99):**26 页**(R1 20 页,**+6**)
- needs_minor (5-6.99):4 页(p7, p20, p21, p23, p30 = 5 页,实为 5 页)—— R1 7 页,**-2**
- needs_major (<5):**0 页**(R1 3 页 → R2 0 页,**-3**)✓✓✓
- **overall_score: 8.1** —— 仍不达 9.0 硬阈值

---

## 三视角分层

| 视角 | R1 → R2 | 看到什么 / 没看到什么 |
|---|---|---|
| **Executive (ROI)** | 7.5 → **8.2** (+0.7) | ✓ BLUF 在前 5 页落地,KPI(p33)+ 行动清单(p34)清晰,5 节扉页 cleaner;✗ TBD 3 页 title 仍"[待 W1/W2 回填]" 红字 → "这是给我看的还是 demo 占位?";✗ p6/p26 两个视觉小瑕未解,稳重感打折 |
| **Technical (实战)** | 7.8 → **8.3** (+0.5) | ✓ 3 张 diagram 重画后真的能 dig in 了(尤其 p11 hub-spoke + p32 Skill 库目录树),T 视角的"读得到结构"基本建立;✗ TBD 3 页"预估 4-8×/8-12×/6-10×"是 hand-wavey range,T 视角仍嫌"不是实测,只是估算" |
| **General (场景)** | 7.4 → **7.8** (+0.4) | ✓ "看/自/用"(p9)+ "今天 3 件事"(p34)+ table(p30)对非工程岗友好;✗ 缩写/术语依然密集(agentic, refactor, MCP, monorepo, SKILL.md 首次出现解释不够);✗ 3 页 TBD title 让非技术读者更困惑"我应该跳过吗" |

任一视角 < 9 → 总分被拉低。最低 G = 7.8(handoff 约束符合)。

---

## Top 3 必改(从所有 needs_minor 中挑影响最大)

### #1 · pages 20 / 21 / 23 · TBD compare_pk title 仍含红字 [待 W1/W2 回填] + 卡片视觉 60% 空白(severity: **high**)

- **issue**:
  - **title 层**:三页 action title 仍写 "工程 Demo · Bug 修复 N× 提速 [待 W1 回填]" / "Refactor M h → H min [待 W1 回填]" / "调研 K h → Y min [待 W2 回填]"。即使 body 有 4-8× / 8-12× / 6-10× 数据,executive 一眼读到 title 红字 [TBD] 还是会心理打折。
  - **视觉层**:compare_pk 两个白卡 box 占满全屏垂直空间,但 content 只填顶部 1/3-1/4(传统 4-5 行 · CC 3-4 行)。下方 60-70% 空白,handout mode 60min 场景下视觉等同"未完成"。
- **suggestion**(三选一,优先级 from cheap to invasive):
  1. **(cheapest) author rewrite title** —— title 把 "[待 W1 回填]" 从 title 移到 source caption(已经有了)。新 title 可改:
     - "工程 Bug 修复 · **预估 4-8× 提速** · W1 实测验证" 
     - "工程 Refactor · **预估 8-12× 压缩** · W1 实测验证"
     - "产品 调研 · **预估 6-10× 压缩** · W2 实测验证"
     这样 title 卖点鲜明(数字 magnitude 进 title),"待回填"信号留在 source 里
  2. **(medium) 补充 body** —— 每个卡再 +2-3 行 handout 解释("CC 怎么找 root cause"/"为什么 plan mode 能压缩 refactor")让卡片填满 60%+
  3. **(invasive) 改 layout** —— 3 页改 `single_focus` 横幅 big_number="4-8×" / "8-12×" / "6-10×" + big_text + caption,彻底跳出"占位 compare_pk"印象
- **归类**:`needs_author_rewrite`(改 title + body 即可)
- **estimated_impact**:三页 6.0 → 7.5-8.0,**整 deck +0.2-0.3**

### #2 · pages 7 + 30 · 卡片/bullet 上半页大片空白(severity: **med**)

- **issue**:
  - p7(compare 2-col SWE 80.8% + Most Loved 46%):两个大卡 content 只填顶部 1/4,下方 75% 空白,handout 60min 场景视觉冷清
  - p30(bullet_list W1/W2/W3 节奏):3 个 bullet 居中纵向,上方 1/3 屏空白,下方半屏空白
- **suggestion**:
  - p7:author 加 2-3 行 handout body 解释("80.8% 意味着什么 · Cursor/Copilot 不公开同口径数据的原因 · 61% 复杂调试更准的开发者反馈来源")
  - p30:加 3 个章节 sub-bullet(每周做啥)或者 designer 在 bullet 前加 W1/W2/W3 数字徽章打破纵向单一节奏
- **归类**:p7 → `needs_author_rewrite`;p30 → `needs_author_rewrite`(加 sub-bullet)或 `needs_designer_revision`(加 W 数字徽章)
- **estimated_impact**:两页 6.75 → 8.0,**整 deck +0.07**

### #3 · pages 6 + 26 · theme_fix 未解(severity: **med**)

- **issue**:
  - p6($1B chart):M6 "1000M (公开)" label 与 chart 下方 source caption 重叠,视觉混乱(R1 known issue, handoff 明示本轮不动)
  - p26(compare 3-col CC 推荐):✓ 绿勾徽章覆盖 "Claude Code(推荐)" title 文字尾部,推荐列视觉打折(R1 known issue, handoff 明示本轮不动)
- **suggestion**:
  - p6:重生成 `1_2_run_rate.png`(matplotlib),把 M6 label 抬高 30px 或换 inside-bar 模式
  - p26:改 `themes/template_training.py` make_compare,recommended 列的 ✓ badge 位置往右上角偏移(避开 title 文字)或缩小到 12pt 等效
- **归类**:`needs_theme_fix` × 2
- **estimated_impact**:两页 +1.0,**整 deck +0.06**

---

## 综合建议

整 deck 平均分:**8.1 / 10** —— 不达 ready_for_delivery 阈值(9.0),但已**全部消除 R1 的 needs_major 类(0 页)**。

**R2 vs R1 改进幅度**:
- needs_major 类:**3 → 0**(三个 TBD 整页空盒全部消除)
- needs_minor 类:**7 → 5**(section_divider 5 页全部脱离 needs_minor;新增 0;p7/p30 仍 needs_minor)
- excellent 类:**6 → 6**(无变化,因为最强页本就是 9+ 级,无空间再上提)
- good 类:**20 → 25**(大量原 needs_minor 升 good 区间)

**关键改进方向(R3 建议路径)**:
1. **立刻处理 3 页 TBD title**(author rewrite)—— 把 "[待 W1/W2 回填]" 从 title 移到 source/caption,新 title 用 magnitude 数字开门;预估 +0.25
2. **补充 p7 + p30 body / 视觉变化**(author rewrite 或 designer)—— 填充上半页空白;预估 +0.1
3. **theme_fix 2 处(p6 chart label / p26 ✓ badge)**(主线程改 themes/*.py 或 chart 重生成)—— 预估 +0.1

完成 R3 后预估 **overall_score ≈ 8.5-8.7**,接近但仍可能不到 9.0 硬阈值。再迭代一轮(R4 / iter 4/5)可达 9.0+。

**5 轮 cap 提醒**:当前 iter 2/5,还有 3 轮空间。预算应留 1 轮(R5)做最后微调,因此**建议 R3 一次性处理上述 3 类**,不要拆轮做。

---

## 反馈三类分流

```yaml
needs_author_rewrite: [20, 21, 23, 7, 30]
  # 20/21/23: TBD title 改写(把"[待 W1/W2 回填]"从 title 移到 source · 
  #          新 title 用 4-8× / 8-12× / 6-10× magnitude 数字开门)+ body 补充填卡
  # 7: SWE compare 2 卡补充 handout body(80.8% 含义 / Cursor 不公开 / 61% 来源)
  # 30: W1/W2/W3 bullet 加 sub-bullet 填上半页空白 (或转交 designer 加数字徽章)

needs_designer_revision: [30]
  # 30: 备选方案 - bullet 前加 W1/W2/W3 圆形数字徽章 (取代 sub-bullet 路径)
  # 注: 30 在 author/designer 两路二选一处理即可,不要双重处理

needs_theme_fix: [6, 26]
  # 6: chart M6 "$1000M (公开)" label 与 source caption 重叠 → 
  #    重生成 _assets/charts/1_2_run_rate.png · M6 label 抬高 30px 或 inside-bar
  # 26: compare 3-col ✓ badge 覆盖 "Claude Code(推荐)" title 文字 →
  #    themes/template_training.py make_compare · recommended 列 ✓ badge 位置右上角偏移

ready_for_delivery: false   # avg 8.1 < 9.0 且 5 页 needs_minor(无 needs_major)
audience_iteration: 2 / 5    # 还有 3 轮预算
predicted_R3_score_if_all_fixed: 8.5-8.7
predicted_R4_score: 9.0+
```

---

## R2 最强 / 最弱

- **最强 3 页**:p16 Anthropic 1 周→30 分钟(9.5)/ p33 行动清单 · 今天 3 件事(9.25)/ p2 BLUF 3 周(9.0)
- **最弱 3 页**:p20 / p21 / p23(3 个 TBD,均 6.0,但已从 R1 的 3.5 翻倍)
- **本轮最大改进**:p12 7 大能力 hub-spoke(R1 6.5 → R2 8.5)+ p14 Subagents+Teams(R1 6.25 → R2 8.25)+ p4/10/17/25/29 五个章节扉页(均 +1.75 左右)
