# Audience Review · R3 · general(E+T+G 分层评判)视角

> 评审 deck: `decks/claude-code-training/deck_v1.pptx`(36 页)
> 评审时间: 2026-05-24
> Audience profile: **general**(主线程合并 a+b+c 三类,按 general 处理;E/T/G 分层校验)
> Top recommendation: 本季度 3 周全员上手 Claude Code · 工程 100% / 产品 50% / 高层 Deep Research · 公司统一 skill 库
> Mode: handout(60 min 内部培训,无现场讲者)
> Iteration: **3 / 5**(还剩 2 轮预算)
> Prev: R1 = 7.55 → R2 = 8.10 → R3 = ?

---

## TL;DR

**Overall: 8.30 / 10** —— **不达 9.0 硬阈值,verdict = needs_minor_revision**

R2 → R3 delta = **+0.20**(R2 的 6 项 fix 中,5 项完全成功,1 项部分成功)。

### R2 → R3 改动 verification(三路并行)

| R2 Top | 内容 | R3 验证结果 |
|---|---|---|
| **#1 author** · p20/21/23 title 升级 magnitude 数字 + 移 [待回填] 到 source caption | 三页 title 全部干净改写:"工程 Bug 修复 · 预估 4-8× 提速 · W1 实测验证" / "工程 Refactor · 预估 8-12× 压缩 · W1 实测验证" / "产品 调研 · 预估 6-10× 压缩 · W2 实测验证";红字 [TBD] 完全消失。**source caption 内嵌"预估值·W1/W2 工程试点"** | ✅ **完全 fix** |
| **#2a author** · p7 SWE compare body 扩到 77/78 字 | p7 左/右 col body 从 R2 ~50 字扩到 ~75 字(3 行 vs R2 2 行) | ✅ **完全 fix** |
| **#2b author** · p30 W1/W2/W3 加 sub-bullet 一层 | p30 现 3 主 bullet + 3 sub-bullet(每 sub 1 行),纵向密度上升 ~50% | ✅ **完全 fix** |
| **#3a 主线程** · p26 ✓ badge 改 stamp 形态不覆盖 title | p26 推荐列 ✓ badge 是右上角白底独立小圆,**完全脱离 title 文字尾**,title "Claude Code(推荐)" 完整可读 | ✅ **完全 fix** |
| **#3b 主线程** · p6 chart M6 label 与 source caption 不重叠 | p6 chart M6 顶端 "$1000M" 黑字标签清晰;chart 下方 source caption italic GRAY 独立行,**已无堆叠** | ✅ **完全 fix** |
| **(派生)** p20/21/23 compare_pk 卡内 body 填卡(R2 #1 "补充 body" 路径) | body 仍是 **2-3 行/col**,大卡 box 下方 **60% 仍空白**。author 这轮只动了 title,没动 body 填充 | ⚠️ **未处理 / 部分**(本轮 author 选了 title 路径,body emptiness 残留) |

### 为什么仍 < 9

R3 把 R2 列出的"必坏"问题清理光,但 **p20/21/23 三页 compare_pk 卡片下方 60% 空白** 仍是单一最大扣分源 —— 三页都被这个视觉残缺压在 7.25,拖整 deck ~0.3 分。其它页都在 8+,无别的明显短板可优化。

要破 9.0 现在不只是 "再修 bug",而是 **要做 lift**(p20/21/23 body 加 50-60 字/col + 几张 8.5 页推到 9+),综合成本高于收益。

**realistic R4-5 路径**:R4 集中填 p20/21/23 body → 预估 R4 ≈ **8.40-8.50**;R5 polish p7/p30/p36 → R5 ≈ **8.55-8.70**。**两轮预算内 ≥ 9 概率 < 30%**,建议主线程问用户是否接受 quality_grade B(详见末尾"5 轮 cap 提醒")。

---

## 整体印象(R3)

1. **节奏感**:5 章 + 5 个 single_focus 章节扉页节奏稳;开场 SCQA(p1-p9)、章节 1-5 各自的内容(p10-p32)、收口(p33-p36)三段式清晰。整 deck 翻阅时不再有 R1 的"section_divider 翻到第几节了?"迷路感
2. **视觉感**:R3 后橙红/深蓝/青绿三色统一,TEAM 卡通**仅在 cover + closing 出现 2 次**,executive 视觉疲劳源消除。但 p20/21/23 三大白 compare_pk 卡片下方空白成为新的"视觉冷场"
3. **数据感**:对 T 视角友好(95% / 80.8% / $1B / 46% Most Loved / 4-8× / 8-12× / 6-10× / ≥95% / ≥80% / ≥10 skill),source 全到位且 R3 后字号 / 位置 cleaner
4. **致命残留**:p20/21/23 三页 compare_pk title 已 magnitude 开门,但 body 仍是骨架(2-3 行短句),60% 卡内空白让 handout 读者本能感觉"页面未填满"
5. **结尾收口**:p33 KPI + p34 行动清单 + p35 4 条核心结论 + p36 Thanks,落地强;但 p36 closing 的橙色 left band + TEAM 卡通右侧的组合视觉略凌乱

---

## R2 → R3 Delta 详情

### Top 1 · p20 / p21 / p23 TBD 三页(R2: 6.0 → R3: 7.25,**每页 +1.25**)

| 页 | R2 title | R3 title(已 fix) | R3 body 状态 |
|---|---|---|---|
| p20 | "工程 Bug 修复 [待 W1 回填]" 红字 | **"工程 Bug 修复 · 预估 4-8× 提速 · W1 实测验证"** ✓ | 传统 4 步 → CC 4 步,2 行 vs 2 行,卡内 60% 空白 ⚠️ |
| p21 | "Refactor [待 W1 回填]" 红字 | **"工程 Refactor · 预估 8-12× 压缩 · W1 实测验证"** ✓ | 同上 ⚠️ |
| p23 | "调研 [待 W2 回填]" 红字 | **"产品 调研 · 预估 6-10× 压缩 · W2 实测验证"** ✓ | 1 行 vs 2 行,卡内 65% 空白 ⚠️(p23 最瘦) |

**结论**:executive 翻 deck 时不再被 [TBD] 红字震慑("这是给我看的?");但 handout 读者眼睛沿 box 边线扫下去仍会感觉"为什么这么空"。

### Top 2 · p7 SWE 扩 body(R2: 6.75 → R3: 7.5,**+0.75**)+ p30 加 sub-bullet(R2: 6.75 → R3: 7.75,**+1.0**)

| 页 | R2 状态 | R3 状态 |
|---|---|---|
| p7 SWE compare | 左右 col 各 ~50 字,2 行 | 左 col 3 行 ~75 字("SWE-bench 是行业基准...同口径下 Cursor/Copilot 未公开成绩;CC 是首个破 80% 门槛的工具");右 col 3 行 ~75 字("同时用过 CC + Copilot 的开发者中,61% 认为 CC 复杂调试/refactor 更准 —— 反映用户实际倾向远高于装机量") |
| p30 W1/W2/W3 bullet | 3 主 bullet 居中,上下 50% 空白 | 3 主 bullet + 3 sub-bullet(└ 缩进格式),纵向密度提升 ~50% |

**结论**:两页都从 R2 needs_minor 提到 R3 good 区间;空白感不再致命。

### Top 3 · 两项 theme fix(R2: 6.5/7.75 → R3: 8.25/8.25)

| 页 | R2 issue | R3 状态 |
|---|---|---|
| p6 $1B chart | M6 "$1000M" label 与 source caption 重叠 | M6 label 顶端独立 + source italic GRAY 单独行,**已 cleanly 分离** ✓ |
| p26 三足鼎立 compare 3-col | ✓ 绿勾 badge 覆盖 "Claude Code(推荐)" title 文字尾 | ✓ badge 已改 stamp 形态(右上角小白圆 + 深色 ✓),**完全脱离 title 文字** ✓ |

**结论**:两项 theme_fix 均已干净落地,executive "稳重感" + technical "数据呈现" 双双补完。

---

## 逐页评分(36 页)

| # | layout | title(节选) | comp_5s | density | visual | flow | avg | verdict | R2→R3 delta |
|---|---|---|---|---|---|---|---|---|---|
| 1 | cover | 让全员上手 Claude Code | 8 | 7 | 8 | 9 | **8.00** | good | -0.25(TEAM 卡通仍占左半 - executive 看的"BCG 稳重感"小折扣) |
| 2 | single_focus | 3 周 · 本季度全员上手 | 10 | 8 | 9 | 9 | **9.00** | excellent | = |
| 3 | toc | 5 章目录 + 03 高亮 | 9 | 7 | 8 | 8 | **8.00** | good | = |
| 4 | single_focus | /01 AI 编程已变天 | 9 | 8 | 7 | 8 | **8.00** | good | = |
| 5 | single_focus | 95% 行业已变天 | 10 | 8 | 9 | 9 | **9.00** | excellent | = |
| 6 | pic_text(chart) | $1B run-rate | 9 | 8 | 8 | 8 | **8.25** | good | **+0.75 ⭐**(theme_fix) |
| 7 | compare 2-col | SWE 80.8% + Most Loved 46% | 8 | 7 | 7 | 8 | **7.50** | needs_minor | **+0.75 ⭐**(body 扩) |
| 8 | cards 4-col | Accenture/Salesforce/Cog/PwC | 9 | 7 | 7 | 8 | **7.75** | good | = |
| 9 | cards 3-col | 公司三类落差 看/自/用 | 9 | 8 | 8 | 9 | **8.50** | good | = |
| 10 | single_focus | /02 7 力解构平台 | 8 | 8 | 7 | 8 | **7.75** | good | = |
| 11 | compare_pk | 不是补全·是 agentic 系统 | 10 | 8 | 9 | 9 | **9.00** | excellent | = |
| 12 | pic_text(diagram) | 7 大能力总览 hub-spoke | 9 | 8 | 8 | 9 | **8.50** | good | = |
| 13 | cards 3-col | Skills 是/为/怎 | 10 | 8 | 8 | 9 | **8.75** | good | = |
| 14 | pic_text(2-diagram) | Subagents + Agent Teams | 8 | 8 | 8 | 9 | **8.25** | good | = |
| 15 | cards 3-col | Hooks + Plugins + MCP | 9 | 8 | 8 | 9 | **8.50** | good | = |
| 16 | compare_pk | Anthropic 1 周→30 分钟 | 10 | 9 | 9 | 10 | **9.50** | excellent | = |
| 17 | single_focus | /03 工程 100%/产品 50% | 9 | 8 | 7 | 8 | **8.00** | good | = |
| 18 | pic_text(triangle) | 工程/产品/高层 分层 | 8 | 8 | 8 | 9 | **8.25** | good | = |
| 19 | cards 3-col | 工程师 任/P/协 | 9 | 8 | 8 | 9 | **8.50** | good | = |
| 20 | compare_pk | 工程 Bug 修复 4-8× 提速 ✓ | 9 | 6 | 6 | 8 | **7.25** | needs_minor | **+1.25 ⭐**(title fix,body 仍空) |
| 21 | compare_pk | 工程 Refactor 8-12× 压缩 ✓ | 9 | 6 | 6 | 8 | **7.25** | needs_minor | **+1.25 ⭐**(同上) |
| 22 | cards 3-col | 产品/设计 P/原/数 | 9 | 8 | 8 | 9 | **8.50** | good | = |
| 23 | compare_pk | 产品 调研 6-10× 压缩 ✓ | 9 | 6 | 6 | 8 | **7.25** | needs_minor | **+1.25 ⭐**(同上) |
| 24 | cards 3-col | 高层 行/竞/季 | 9 | 8 | 8 | 9 | **8.50** | good | = |
| 25 | single_focus | /04 Hybrid 是主流 | 9 | 8 | 7 | 8 | **8.00** | good | = |
| 26 | compare 3-col(recommended) | 三足鼎立 · CC 推荐 ✓ | 9 | 8 | 7 | 9 | **8.25** | good | **+0.50 ⭐**(✓ badge fix) |
| 27 | matrix_2x2 | 规模决定工具 BCG | 9 | 8 | 9 | 10 | **9.00** | excellent | = |
| 28 | cards 3-col | Hybrid Stack 推荐 | 9 | 8 | 8 | 9 | **8.50** | good | = |
| 29 | single_focus | /05 3 周全员上手 | 9 | 8 | 7 | 8 | **8.00** | good | = |
| 30 | bullet_list | W1/W2/W3 节奏 + sub-bullets | 8 | 8 | 7 | 8 | **7.75** | good | **+1.00 ⭐**(sub-bullet) |
| 31 | table | 3 周时间表 | 9 | 9 | 8 | 9 | **8.75** | good | = |
| 32 | pic_text(diagram) | 公司 Skill 库 目录+贡献 | 8 | 8 | 8 | 9 | **8.25** | good | = |
| 33 | cards 3-col | KPI 工程≥95% / 产品≥80% / skill≥10 | 9 | 8 | 8 | 9 | **8.50** | good | = |
| 34 | cards 3-col | 行动清单 · 今天 3 件事 | 10 | 9 | 8 | 10 | **9.25** | excellent | = |
| 35 | summary | 核心结论 4 条 | 9 | 8 | 8 | 10 | **8.75** | good | = |
| 36 | closing | Thanks + W1 见 | 8 | 7 | 7 | 9 | **7.75** | good | = |

**汇总**:
- 平均分:**8.30 / 10**(R2 8.10 → R3 8.30,**+0.20**)
- excellent (≥9):**6 页**(p2, p5, p11, p16, p27, p34)+ 边缘 p35(8.75)/ p13(8.75)/ p31(8.75) —— 与 R2 持平
- good (7.5-8.99):**27 页**(R2 26 页,+1 是 p7 从 needs_minor 升入)
- needs_minor (5-7.49):**3 页**(p20 / p21 / p23,均 7.25)—— R2 5 页(p7/p20/p21/p23/p30)→ R3 3 页,**-2**
- needs_major (<5):**0 页**(R2 0 → R3 0)✓
- **overall_score: 8.30** —— 仍不达 9.0 硬阈值

---

## 三视角分层

| 视角 | R2 → R3 | 看到什么 / 没看到什么 |
|---|---|---|
| **Executive (ROI)** | 8.2 → **8.5** (+0.3) | ✓ p20/21/23 红字 [TBD] 消失,title 直接磁力开门"预估 4-8×"等;✓ p6/p26 视觉小瑕全修;BLUF (p2)+ KPI (p33)+ 行动清单 (p34) 落地强。✗ 三页 compare_pk 卡内 60% 空白仍让"稳重感"差最后一口气;✗ p1 封面 TEAM 卡通仍偏插画风,执行者看的"BCG 报告"印象差 0.5 分 |
| **Technical (实战)** | 8.3 → **8.4** (+0.1) | ✓ p12/p14/p32 三 diagram 标签清晰可 dig in;p11 agentic vs Copilot 对决干净;p16 Anthropic 内部案例 deck 最强页;p27 BCG matrix 严谨。✗ p20/21/23 "预估 4-8× / 8-12× / 6-10×" 仍是 hand-wavey range —— T 视角嫌"这只是估算,不是实测"(source 已写 W1/W2 待回填,合规但 evidence 弱) |
| **General (场景)** | 7.8 → **7.9** (+0.1) | ✓ p30 sub-bullet 帮非技术读者跟节奏;✓ p33 KPI / p34 今天 3 件事 / p31 table 对全员友好;✓ TBD title 消失帮非技术读者不再困惑"我该跳过吗"。✗ agentic / refactor / MCP / monorepo / SKILL.md 首次出现仍密集,第一次读会出戏;✗ p20/21/23 仍偏工程语境(/explain · /plan · grep),产品 / 高层读者翻这三页只能空看 |

**任一视角 < 9 → 总分被拉低**。最低 G = 7.9(handoff 约束已守住,但仍 < 9)。

---

## Top 3 必改(R3 残留)

### #1 · p20 / p21 / p23 · compare_pk 卡内 body 仍 60% 空白(severity: **high**)

- **issue**:三页 title 已 magnitude 开门 ✓,但卡内 body 仍是 2-3 行短句("找 root cause → 改代码 → 自测 → CR · 单 bug 通常 2-4 h" / "/explain → 让 CC 改 → 试跑 → 出 PR · 预估 4-8× 提速")。compare_pk 两个大白卡 box 顶部填了 1/3,**底部 60-65% 仍空白**,handout mode 60min 场景下读者眼睛沿 box 边线扫下去,本能感觉"未填满"
- **suggestion**(R4 时让 author 做 body 扩充):
  - **p20 Bug 修复 · 传统流程 col 扩到 70-80 字**:加上"为什么传统流程慢"的具体痛点 ——"调试断点要本地复现/单元测试通常 grep 不到/线上日志看到现象但根因要顺藤摸瓜跨 2-3 个文件";**CC col 扩到 70-80 字**:加上"为什么 CC 快"——"/explain 一次性读完所有相关文件 + 报上下文 / 跑测试看失败原因自动迭代 / 让 user 决定 patch 大小再 PR"
  - **p21 Refactor · 传统流程**:"逐个文件 trace 旧逻辑 / 整理重构计划文档 / 改完跑测试看 break 哪些 / 一次大 PR review 慢";**CC**:"/plan 模式先输出重构计划文档 / CC 跨文件 grep 关联点 / 自动跑 tests 看回归 / 分批 PR 易 review"
  - **p23 调研** 同理
- **归类**:`needs_author_rewrite`(改 markdown body 即可,不动 layout)
- **estimated_impact**:三页 7.25 → 8.50,**整 deck +0.10**(7.25×3=21.75 → 8.50×3=25.50,delta +3.75/36)

### #2 · p7 SWE compare · 已扩 body 但仍属 needs_minor(severity: **med**)

- **issue**:R3 body 已从 R2 50 字扩到 75 字(进展明显),但 2 大卡仍是上半页有内容、下半页空白。compare 2-col 在 handout 用比 compare 3-col 更易"显空"(每 col 宽度大)。**不致命**,但占 needs_minor 一个名额
- **suggestion**(可选,R5 polish):
  - 改 layout 为 `pic_text` 加 sparkline / 小柱状图说明 80.8% 在历史 SWE-bench 排名 vs Cursor 19% / Copilot 9% 的可视化
  - 或在每 col 加 1 个"开发者 quote"(取自 SitePoint / Most Loved 调研原文)
- **归类**:`needs_author_rewrite`(content + 可能 image_path)/ `needs_designer_revision`(若加 sparkline,designer 补素材)
- **estimated_impact**:p7 7.5 → 8.0,**整 deck +0.014**(微)

### #3 · p36 closing 视觉布局凌乱(severity: **low**)

- **issue**:Thanks 大字 + 3 numbered action + 橙色 left band + TEAM 卡通右侧 —— 4 个视觉元素分散,橙色 left band 占左 1/3 但高度只 1/6,下方留白多;TEAM 卡通从 cover 又出现一次,closing 应更克制
- **suggestion**:
  - 砍掉橙色 left band(纯装饰,无信息载体),让 3 个 action numbered 下方有"W1 见 · 工程团队 lead · contact: ..."一行收口
  - 或保留 left band 但加 1 行卖点("3 周后再聚:看 W1 工程试点数据" / "提问:#claude-code-help Slack 频道")
- **归类**:`needs_designer_revision`(视觉布局调整,builder 自动 rebuild)/ 可选 `needs_theme_fix`(closing layout helper 砍 left band)
- **estimated_impact**:p36 7.75 → 8.25,**整 deck +0.014**(微)

---

## 综合建议

整 deck 平均分:**8.30 / 10** —— 不达 ready_for_delivery 阈值(9.0),但**已无 needs_major 页**。

**R3 vs R2 改进幅度**:
- needs_major:0 → 0(持平,均无)
- needs_minor:5 → 3(p7/p30 升入 good;只剩 p20/21/23)
- excellent:6 → 6(无变化)
- good:25 → 27(p7/p30 升入)

**关键改进方向(R4 建议路径)**:
1. **优先**:author 扩 p20/21/23 三页 compare_pk body 到 70-80 字/col(handout-mode 标准密度)—— 预估 +0.10
2. **次优**:author / designer 微 polish p7 SWE compare(加 sparkline 或 quote)—— +0.014
3. **可选**:designer 整 p36 closing 布局(砍 left band 或加卖点)—— +0.014

**R4 → R5 预估路径**:
- R4 完成 #1 → 预估 **8.40-8.50**(不到 9.0,仍 quality_grade B)
- R5 完成 #2 + #3 → 预估 **8.55-8.70**(仍不到 9.0)
- 要达 9.0 需 push 多个 8.5 baseline 页到 9+ —— 需要新 hero data anchor / 新 layout,**不是 polish 能解决的,是 restructure**

---

## 5 轮 cap 提醒(给主线程)

当前 iter **3 / 5**,还剩 **2 轮**。基于现状预估:

| 路径 | R4 预估 | R5 预估 | 综合判断 |
|---|---|---|---|
| **A · 继续修** | 8.40-8.50 | 8.55-8.70 | 2 轮预算内 ≥ 9 概率 **< 30%** |
| **B · 当前接受(quality_grade B)** | — | — | overall 8.30 已是 deck 历史最高,且无 needs_major,handout 完成度足够 |
| **C · R4 只修 Top 1,R5 留 buffer** | 8.40-8.50 | 8.40-8.50(不动) | 折中,quality_grade B+ |

**我的建议**(audience 视角):**走 C 或 B 路径**。R3 已把所有"必坏"问题清理光,p20/21/23 body 残缺是这份 deck 在 W1 实测前的**结构性限制**(没数据就只能"预估 X×"),不是 polish 能根治的。**等 W1 实测真的跑完(用户的下一轮节奏),再回来填三页 body,deck 自然就到 9.0**。

主线程问用户四选一时,请把这层 context 给用户:**"这 deck 现状 8.30 已是 W1 实测前的天花板,继续 polish 收益递减;建议接受 B 级,W1 跑完后回来填 p20/21/23 实测数据,届时 deck 自然 ≥ 9"**。

---

## 反馈三类分流

```yaml
needs_author_rewrite: [20, 21, 23, 7]
  # 20/21/23: compare_pk body 扩到 70-80 字/col(handout 密度,填卡内 60% 空白)
  #   - p20: 传统流程加 "为什么慢" 痛点(调试 / 测试 / 跨文件);CC 加 "为什么快"(/explain / 跑测试自动迭代 / patch 决策)
  #   - p21: 传统 Refactor 痛点(逐文件 trace / 大 PR review 慢);CC 优势(/plan 计划 / 跨文件 grep / 分批 PR)
  #   - p23: 传统调研痛点(查文档 / 拼数据);CC + Deep Research 优势(1 prompt 调 web/docs / 人审 polish)
  # 7: SWE compare 可选 polish - 加开发者 quote 或 sparkline(R5 buffer 时再做)

needs_designer_revision: [36]
  # 36: closing layout 调整 - 砍左侧橙色 band(纯装饰无信息),
  #     或保留 band 加一行卖点 "W1 见 · contact / Slack 频道"
  # 注: 优先级 LOW, R5 buffer 时再做

needs_theme_fix: []
  # R2 两项 theme_fix 已 verified working(p6 chart label + p26 ✓ badge),
  # R3 无新增 theme 层问题

ready_for_delivery: false   # avg 8.30 < 9.0 + 3 页 needs_minor(均 7.25)
audience_iteration: 3 / 5    # 还剩 2 轮预算
predicted_R4_score_if_top1_fixed: 8.40-8.50
predicted_R5_score: 8.55-8.70
realistic_path_to_9: "需 W1 实测数据回填 p20/21/23,polish 单独无法达 9"
suggested_user_decision_frame:
  - "A · 继续(R4 修 Top 1)→ 预估 8.45,quality_grade B+"
  - "B · 接受当前 8.30,quality_grade B,W1 跑完回来填实测"
  - "C · R4 修 Top 1 后接受 8.45,quality_grade B+,W1 跑完再回填"
  - "D · 回 brainstorm 重排(不推荐,deck 结构已稳)"
```

---

## R3 最强 / 最弱

- **最强 5 页**:p16 Anthropic 1 周→30 分钟(9.5)/ p34 行动清单(9.25)/ p2 BLUF 3 周(9.0)/ p5 95% 行业(9.0)/ p11 不是补全是 agentic(9.0)+ p27 BCG matrix(9.0)
- **最弱 3 页**:p20 / p21 / p23(3 个 compare_pk · 全员 7.25,卡 body 残缺)
- **本轮最大改进**:p20/21/23 三页 title 升级(+1.25/页)+ p7 body 扩(+0.75)+ p30 sub-bullet(+1.0)+ p6/p26 两 theme_fix(+0.75/+0.5)
- **R3 → R4 杠杆点**:p20/21/23 三页 body 填卡 = 唯一显著回报(+0.10);R4 后再无大空间,9.0 需 W1 实测数据回填

---

## audience iter 历史曲线

```
R1 (iter 1/5): 7.55  [基线 · 3 个 needs_major + 7 个 needs_minor]
R2 (iter 2/5): 8.10  [+0.55 · 0 needs_major + 5 needs_minor · 6 项 fix 全成功]
R3 (iter 3/5): 8.30  [+0.20 · 0 needs_major + 3 needs_minor · 6 项 fix 中 5 完整 + 1 部分]
R4 预估:        8.40-8.50  [若 author 填 p20/21/23 body]
R5 预估:        8.55-8.70  [若加微 polish p7/p36]
9.0 真实路径:    需 W1 实测数据回填(超出 audience iteration 能力)
```
