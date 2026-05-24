---
review_iteration: 2
reviewed_at: 2026-05-24
stage: D
brief_md: /Users/pc2026/Documents/DevTools/iLovePPT/decks/claude-code-training/brief.md
outline_md: /Users/pc2026/Documents/DevTools/iLovePPT/decks/claude-code-training/deck_v1_outline.md
content_md: /Users/pc2026/Documents/DevTools/iLovePPT/decks/claude-code-training/deck_v1_content.md
---

# Critic Report · Stage D · iteration 2(覆盖 R1)

## Verdict

verdict: **pass_with_notes**

checklist_summary:
  section_a_pyramid: pass (A1-A7 全过)
  section_b_alignment: pass (B1-B7 全过;B7 实测 5 页 mode 字数全合规 / 1 处 layout 字数边界情况降为 med rec)

judgmental_summary:
  high: 0           # 必须 0 才能进 pass / pass_with_notes ✓
  med: 1            # 4.2 matrix_2x2 axis 字数边界(speaker 8 字 vs handout 推断扩展)
  low: 5            # 4.2 metadata 表达不一致 / 1.5 论据 narrative-only / R4 BLUF schema 扩展 / 1.3 61% brief 外数字 / outline line 93 旧文字 staleness

**结论**:R1 三项 must-fix(M1 字数 / M2 字数 / M3 metadata 泄漏)全部正确应用;R2 五项 recommended 全部落地且符合预期;无 high severity 阻塞项。**ready_for_next: true** — 主线程可直接派 builder,或先按 6 条 notes polish 再 build。

---

## Section A · 金字塔结构审计

### A1 · 单一顶端论点
status: **pass**
evidence: top_recommendation 三要素齐:
- 动词:`让全员上手` / `升级` / `完成`
- 宾语:`Claude Code` + 全员
- 边界:`工程 100%` + `产品 / 设计 50%` + `高层 Deep Research` + `3 周 onboarding` + `公司 skill 库`
覆盖战略 + 范围 + 节奏,完整推荐句。

### A2 · SCQA 完整
status: **pass**
evidence:
- S(situation):2026 AI 编程进入 agentic 阶段 + $1B run-rate + 80.8% + 46% Most Loved → frontmatter line 19 全文
- C(complication):公司可能停留 "问 AI 答疑" + 缺统一 skill 库 + 非工程同事旁观 → frontmatter line 20;**R2 1.5 cards 三卡明示页**(content.md line 173-181)显式承接,narrative tension 拉满
- Q(question):怎么让全员上手 Claude Code → frontmatter line 21
- A(answer):本季度全员上手 + 3 周 + skill 库 → 与 top_recommendation 等价(压缩版)✓

C 是真冲突非 S 复述:1.4 大客户已下注(市场已动) vs 1.5 公司有三类落差(我们没动)— 反差对照,Complication signal 强。

### A3 · 答案在前(BLUF)
status: **pass**
evidence:
- cover.subtitle = "从问 AI 答疑,升级到让 AI 直接交付" 含顶端论点核心动宾 ✓
- **0. BLUF 提前页**(cover 之后、toc 之前)single_focus = "本季度全员上手 · 3 周 onboarding" + explanation "工程 100% · 产品设计 50% · 高层 Deep Research · 公司统一 skill 库" → 完整明示 ✓
- 每个 section_divider title 全是结论句(AI 编程已变天 / 7 力解构平台 / 工程 100% / 产品 50% / Hybrid 是主流 / 3 周全员上手)— 无话题型标签

### A4 · MECE 3-5 章节
status: **pass**
evidence:5 章演绎序(Why → What → How → Choose → Implement)
- Ch1 AI 编程已变天:S + C(R2 扩到含 1.5 Complication 明示)
- Ch2 7 力解构平台:What(产品能力)
- Ch3 工程 100% / 产品 50%:How(三视角使用)
- Ch4 Hybrid 是主流:Choose(工具选型)
- Ch5 3 周全员上手:Implement(落地节奏)

逐对核验 10 对(C(5,2) = 10):
- 1↔2 / 1↔3 / 1↔4 / 1↔5:Ch1 边界 = 市场 + Complication;其他章不涉及市场,无重叠 ✓
- 2↔3:能力 vs 使用方法,清楚 ✓
- 2↔4 / 2↔5:能力 vs 选型 / 节奏 ✓
- 3↔4:R1 修过 — Ch3.2 hybrid 内容已剥离推给 Ch4 ✓
- 3↔5:角色用法 vs 落地节奏 ✓
- 4↔5:工具 vs 节奏 ✓

**R2 加 1.5 不破 MECE**:1.5 内容(公司三类落差)是 Complication,Ch1 边界已扩到 S+C(outline divider sub_caption 已同步说明 "市场为什么变天 + 公司落在哪三类差距上")。读完不会问"那 X 呢"。

> ⚠️ **outline 第 93 行残留旧描述**:`> **MECE 边界**:只讲市场 / 数据,不讲产品特性`这句话文字未跟上 R2 1.5 扩展(应改为 "讲市场 + 公司落差/SCQA 的 S+C"),但**这是 outline 注释级 staleness,不破实际 MECE**。归 low note。

### A5 · 纵向疑问链(ghost deck test)
status: **pass**
evidence:全 action title 串读:
```
cover.subtitle "从问答疑到直接交付"
→ 0. BLUF "本季度全员上手 · 3 周"
→ 1.1 "95% 用 AI 行业已变天"(S₁)
→ 1.2 "$1B run-rate 单工具最快"(S₂)
→ 1.3 "SWE 80.8% + 46% 双第一"(S₃)
→ 1.4 "Accenture / Salesforce 已下注"(S₄)
→ 1.5 "公司三类落差 · 为什么我们要现在动"(C, 反差转折)
→ 2.1 "不是补全工具 · 是 agentic 系统"(范式)
→ 2.2 "7 力总览"(地图)
→ 2.3 "Skills · 团队级沉淀关键"
→ 2.4 "Subagents + Agent Teams 协作新范式"
→ 2.5 "Hooks + Plugins + MCP 扩展层"
→ 2.6 "Anthropic 内部 1 周 → 2 call"(收口)
→ 3.1 "工程 100% / 产品 50% / 高层"(总览)
→ 3.2 "工程师任务边界 / prompt / 协作"
→ 3.3 "Bug 修复 N× 提速 [W1]"
→ 3.4 "Refactor M h → H min [W1]"
→ 3.5 "产品 / 设计 50% 辅助生产"
→ 3.6 "调研 K h → Y min [W2]"
→ 3.7 "高层 Deep Research · 季度报告"
→ 4.1 "三足鼎立 agentic / 编辑器 / 插件"
→ 4.2 "规模决定工具"
→ 4.3 "Hybrid Stack 推荐"
→ 5.1 "3 周节奏"
→ 5.2 "3 周时间表 + 里程碑"
→ 5.3 "公司 Skill 库"
→ 5.4 "工程 ≥95% / 产品 ≥80% / skill 库 ≥10 个"(KPI 验收)
→ 5.5 "今天就能做的 3 件事"
→ summary + closing
```
**链通畅,1.5 加入让 S→C→A 转折更顺;Ch3 三页 [TBD] 占位 title 仍是结论形态不破链。**

### A6 · 横向逻辑同类
status: **pass**
evidence:5 章句式全部结论句(无话题标签),整体演绎序(Why → What → How → Choose → Implement)贯穿;无混合(全是 because / 全是 steps / 全是 dimensions 任一类)。

### A7 · action title ≤ 24 字
status: **pass**
evidence:author 已在 outline `# Pyramid 自检 ⑦` 块逐条复核 29 个 title,全 ≤ 22 字(template_training 实际硬限);R2 新加 / 修改的 4 个 title 已重核:
- 1.5 公司三类落差 · 为什么我们要现在动 = 15.5 字 ✓
- 3.3 工程 Demo · Bug 修复 N× 提速 [待 W1 回填] = 17.5 字 ✓
- 3.4 工程 Demo · Refactor M h → H min [待 W1 回填] = 19.5 字 ✓
- 3.6 产品 Demo · 调研 K h → Y min [待 W2 回填] = 17.5 字 ✓

5 个 section_divider title 全 ≤ 8 字 ✓(踩线 1 处:"工程 100% / 产品 50%" = 8 但未超)

---

## Section B · brief → content 对齐

### B1 · top_recommendation 字面一致(vs content.cover.subtitle)
status: **pass**
evidence:content cover.subtitle = "从问 AI 答疑,升级到让 AI 直接交付" — top_recommendation 中"升级"部分简化版;**剩余部分(本季度 / 3 周 / 工程 100% / 产品 50% / 高层 / skill 库)由 0. BLUF 提前页承接**,信息无丢失。

### B2 · SCQA 4 字段在 content 有承接
status: **pass**
evidence:
- S → 1.1-1.4 四页(95% / $1B / 80.8% / Accenture 等)✓
- C → **R2 新加 1.5**(三卡 · 看不到 ROI / 自学摸索 / 用不来)✓
- Q → 隐含 1.5 → 2.1 → 0. BLUF 直接给 A,逻辑顺
- A → 0. BLUF + summary + closing 三重收口

### B3 · audience tone 匹配
status: **pass**
evidence:audience = general(混合 a+b+c)。抽 3 页验:
- 0. BLUF:`3 周 · 工程 100% / 产品设计 50% / 高层 Deep Research · 公司统一 skill 库`— 数字驱动 + 结论清晰,符合 general(类比辅助 + 结论先行)
- 2.4 pic_text:Subagents / Agent Teams 偏 technical 但配 3 点 body 解释 + 金字塔图,T 看技术深度 + G 看范式 ✓
- 5.5 cards:"今天 / 本周 / 本月" 三档 actionable — 完美 general 调性

### B4 · asset_inventory 每项有交代
status: **pass**
evidence:三份 inventory 全部有 deck 内引用:
- `claude-code-sources.md`(30+ URL):reference_urls 顶部 frontmatter 列 12 URL;每个数据页 `> 数据:Source:` cite ✓
- `claude-code-key-facts.md`:1.4 Accenture / 2.2 7 特性 / 3.2 最佳实践 各 cite ✓
- `claude-code-comparison.md`:4.1 / 4.3 各 cite ✓

### B5 · 无 brief 外新事实
status: **pass**(1 处 low note)
evidence:`Grep` 反向校验 — content 1.3 "61% 认为 CC 在复杂调试 / refactor 上更准" 是 brief.md / outline.md 字面外的新数字,**但 cite 了 SitePoint 2026 + tech-insider Q1 2026 source**,可验自 inventory 文件(brief 列出的 inventory 范围内)。strict-read 边界情况,归 low note(若后续跨用建议把 61% 反向加进 brief / key-facts 以保单一信源)。

### B6 · duration × 1.5 ≈ 总页数
status: **pass**
evidence:duration_min = 60,presentation_mode = handout。
- speaker 公式 60 × 1.5 = 90 页 ≠ 36 ❌
- **handout 信息密度 3-4× speaker** → 1 页 ≈ 1.7 min;36 × 1.7 ≈ 60 min ✓
- content-writing.md "60 min handout 30-40 页" 区间 → 36 在区间内 ✓
- brief "拓写偏好"约 37 页,实际 36 接近预估 ✓

### B7 · presentation_mode 字数(handout)
status: **pass**(1 处 layout 字数边界情况 → 见维度 3 med rec)
evidence:**实测 5 页全字段**:
- 0. BLUF single_focus explanation = 25 字 ≤ 60 ✓
- 1.5 cards body 三卡 = 38 / 39 / 34 字 ≤ 80 ✓ **R2 新加**
- 2.4 pic_text point body 三点 = 44 / 41 / 38 字 ≤ 50 ✓ **R1 M1 fix**
- 5.3 pic_text point body 三点 = 42 / 37 / 42 字 ≤ 50 ✓ **R1 M2 fix**
- 5.5 cards body 三卡 = 48 / 46 / 48 字 ≤ 80 ✓
- 5.2 table cell 全 ≤ 25 字 ✓
- summary 4 条 ≤ 60 字 ✓
- closing subtitle = 12 字 ≤ 24 ✓

**handout 模式字数全部合规**。

> ⚠️ **B7 子项边界**:4.2 matrix_2x2 y_axis low/high 标签 "工具偏好(inline 补全为主)" = 11 字、"工具偏好(agentic 多步为主)" = 11.5 字。speaker 模式 layout 规则 `x_axis/y_axis ≤ 8 字`;handout 模式未明列扩展系数,按 ~3× 推断可放到 ~24 字。**严格读 fail,宽厚读(handout 推断扩展)pass**。降为 med rec(维度 3),非 must-fix。

---

## 判断性评审(4 维度)

### 维度 1 · 论据强度

#### issue 1
- severity: **low**
- page: 1.5(R2 新增 SCQA C 明示页)
- observed: "三卡 body 全部 narrative 推断('还把 AI 当工程团队工具' / '高质 prompt 没沉淀' / '觉得工具与我无关'),无具体内部数据 / 调研样本 / 访谈引用"
- impact: "SCQA C 是 framing 不强求数字,但 Complication 论据偏 narrative 时,executive 读者可能反问'怎么知道我们公司就这样?有调研吗?'"
- suggestion: "brief 已明示'用户没有公司内部素材',此情况下 narrative 论据是合理 fallback。**建议**:1.5 三卡 body 末尾加一句锚定语,如 'Q1 内部访谈样本 / 推论自行业普遍模式'。或 source 改为 '基于公开调研 + 行业普遍现象推断',让读者知道这是 hypothesis 而非 audit;**用户提供内部数据后再回填**(brief.md line 42 已为此预留 fallback path)"

**总体维度 1**:R1 数字锚点全部应用(Ch2.3/2.4/2.5 数字 / Ch4.3 highlight / Ch5.2 absorb 里程碑);1.2 chart hatched 视觉信号文案完整(caption "仅 M6 为官方公开,M0-M5 为示意 estimated path");**论据强度 R1 → R2 显著加强**。

---

### 维度 2 · 节奏感

#### 无 high / med
- 总体:**节奏感 R2 后显著改善**
  - 1.5 加入后 narrative tension:1.1-1.4(市场 4 页,S)→ 1.5(公司落差 1 页,C pivot)→ Ch2(产品能力,answer 的支撑)— S→C→A 转折顺
  - 1.4 → 1.5 反差对照:大客户已下注 ↔ 我们三类落差,效果强
  - 1.5 → Ch2 divider sub_caption "市场已变 + 公司有三类落差,但 Claude Code 凭什么领跑?" — 桥句完整
  - Ch3 篇幅(7 内容页,含 3 TBD)虽相对偏重(7/26 ≈ 27%),但三视角是 deck 核心,合理 ✓
  - 5 个 section_divider sub_caption 全部 2-3 句桥句(R1 维度 2 应用)— 跨章过渡顺畅

---

### 维度 3 · 措辞质感

#### issue 1
- severity: **med**
- page: 4.2 matrix_2x2
- observed: |
    y_axis low = "工具偏好(inline 补全为主)" = 11 字
    y_axis high = "工具偏好(agentic 多步为主)" = 11.5 字
    layout 规则(content-writing.md line 30):`x_axis/y_axis ≤ 8 字`(speaker 模式硬限)。handout 模式未明列 axis 扩展系数;反例特征"轴标签写成完整句"命中 — 当前 axis label 接近完整句式。
- impact: "若严格 8 字 axis(speaker 等同),render 时 axis 文字可能换行 / 遮挡 quadrant 边界。handout 模式按 3× 推断可放到 ~24 字,严格 fail / 宽厚 pass 边界情况。读者扫读 axis 时 11 字带括号长句比 4-5 字短词慢约 2-3 秒"
- suggestion: |
    建议压缩:
    - y low:"工具偏好(inline 补全为主)" → "inline 补全为主"(7 字)或 "偏 inline 补全"(6 字)
    - y high:"工具偏好(agentic 多步为主)" → "agentic 多步为主"(8 字)或 "偏 agentic"(5.5 字)
    x 轴同理 polish 但 "公司规模(< 50 人)" 6.5 字 / "公司规模(10000+)" 7 字 均已 ≤ 8,无需改。
    **不阻塞 builder**:若用户接受 handout 扩展放宽,可保持当前;若希望视觉更紧凑,5 分钟压两个 label。

#### issue 2
- severity: **low**
- page: 4.2 matrix_2x2(line 431 `highlight: true`)
- observed: "4.2 quadrant block 用 yaml 字段 `highlight: true` 写在 quadrant body 下(line 431);**4.1 / 4.3 用 HTML 注释**(`<!-- recommended: item_1 -->` / `<!-- highlight: card_2 -->`)— **同一 deck 内三页 metadata 表达不一致**"
- impact: "stylistic only。author 报告说 '4.2 matrix highlight 是 quadrant 字段非 body 故保留',技术上 legal(matrix_2x2 schema 明列 `highlight: bool`)。但读 content.md 的人(包括下次 author / builder maintainer)会困惑两种表达方式的区分边界"
- suggestion: |
    选其一统一:
    (A) 保持现状,在 frontmatter `special_page_markers` 添加 metadata 表达约定说明(quadrant 用 yaml 字段 / cards / compare 用 HTML 注释)
    (B) 4.2 改用 HTML 注释 `<!-- highlight: quadrant_tl -->`,跟 4.1 / 4.3 风格统一
    用户偏好哪种都可,选定即可。

#### issue 3
- severity: **low**
- page: 0. BLUF(content.md line 93 "## 0.")
- observed: "h2 命名约定上 `## N. <action title>` 要求 N ≥ 1(章节序号);N=0 是 schema 扩展。R4 已加 HTML 注释 `<!-- bluf_page: true · N=0 表示 pre-chapter intro -->` + frontmatter `special_page_markers.bluf` 双保险"
- impact: "若 builder 严格按 schema 校验,N=0 可能报错;若 fallback 兼容(读 frontmatter marker 或 layout 注释)则 pass。author 已尽力提示,builder 端兼容性未验"
- suggestion: "send to builder 时若解析报错,主线程指引 builder 读 `special_page_markers.bluf.h2_id: '0'` + `position: 2` 字段直接当 single_focus 处理。**这是 framework 兼容性 note,非 content 质量问题**"

#### issue 4 · R3 TBD title 数字占位模板
- 评价:**3.3 / 3.4 / 3.6 title 形态升级合规 ✓**
- 形态:"Bug 修复 N× 提速" / "Refactor M h → H min" / "调研 K h → Y min" — 介于话题标签和确切结论之间,暗示"会有提速 / 缩短"结论方向,比之前"Bug 修复 before / after"(纯话题)明显升级
- 风险点:"N×" / "M h" 是占位符变量,handout 读者初次看会 confused — 但 author 已在 placeholder body 加 "回填后替换为实测数值(例:'3× 提速' 或 '5× 提速')" 指引,可控
- 评价:**结论:R3 应用正确,无需追加 action**

---

### 维度 4 · 整体平衡

#### 无 issue
- 总页数 36,在 brief 30-40 区间 ✓
- 章节篇幅分布:Ch1=5 / Ch2=6 / Ch3=7(含 3 TBD)/ Ch4=3 / Ch5=5,合计 26 内容页 + 10 (cover+BLUF+toc+5dividers+summary+closing) = 36
- summary 4 条结论全带数字(80.8% / 46% / 100% / 50% / 3 周 / ≥10 个)— 非 toc 重列 ✓
- closing 极简 subtitle + next_steps 4 项 actionable ✓
- 0. BLUF + cover.subtitle 双 BLUF 不冗余 — cover 是 product framing,BLUF 是节奏 + 范围,信息互补

---

## R1 三项 must-fix · R2 应用验收

| R1 must-fix | author 改动 | R2 critic 验收 |
|---|---|---|
| **M1** 2.4 pic_text point body ≤ 50 | 三 point 压缩到 Subagents 44 / Agent Teams 41.5 / iLovePPT 38.5 | ✅ 全过 |
| **M2** 5.3 pic_text point body ≤ 50 | 目录结构 42.5 / 贡献流程 37.5 / 治理 42.5 | ✅ 全过 |
| **M3** 4.3 card 2 metadata 泄漏 + 扫描 | 4.3 card 2 改 HTML 注释 + 用户可见 title "本公司推荐 ★";4.1 card 1 同类 metadata 也改 HTML 注释 + title "(推荐)";4.2 matrix highlight 是 schema 字段保留;全 cards 扫无其他泄漏 | ✅ 全过 |

## R2 五项 recommended · 应用验收

| R2 rec | author 改动 | R2 critic 验收 |
|---|---|---|
| **R1** 1.2 chart hatched M0-M5 | matplotlib 重渲染 + caption 明示 "仅 M6 为官方公开,M0-M5 为示意 estimated path" | ✅ 视觉信号文案完整(PNG 未直接读 — caption 已充分) |
| **R2** SCQA C 加 1.5 明示页 | 新增 cards 3 卡(高层 / 工程 / 产品+设计+高层 各 1 落差);Ch1 divider sub_caption 同步更新;deck 35 → 36 页 | ✅ 不破 MECE,加强 narrative tension |
| **R3** 3.3/3.4/3.6 TBD title 数字占位模板 | "N× 提速" / "M h → H min" / "K h → Y min";placeholder body 加 "回填后替换实测数值"指引 | ✅ 形态升级合规;handout 读者风险低(placeholder body 已指引) |
| **R4** BLUF "## 0." h2 marker | HTML 注释 `<!-- bluf_page: true · N=0 -->` + frontmatter `special_page_markers.bluf` 双保险 | ⚠️ 自身正确,builder 端兼容性 low note(等 Stage E 看) |
| **R5** Ch3 篇幅 pending_data 联动不强动 | 无改动 | ✅ 按 R1 明示 |

---

## Failed Items + High-Severity Summary

**Must-fix(verdict 决定权)**:
- 无

**Recommended (notes,主线程展示给用户决定接受 / polish):**
- **维度 3 med** · 4.2 matrix_2x2 y_axis 字数:"工具偏好(inline 补全为主)" 11 字超 speaker 8 字硬限,handout 模式无明列扩展 → 边界情况。建议 5 分钟压缩两个 y_axis label 到 ≤ 8 字。或保持现状由 builder render 后视觉验证(可能换行 / 遮挡)。
- **维度 1 low** · 1.5 三卡 body narrative-only,无内部数据 → brief 已说明 fallback 是合理,后续用户回填内部访谈数据时再 strengthen。
- **维度 3 low** · 4.2 highlight: true 用 yaml 字段 vs 4.1 / 4.3 用 HTML 注释 → 同 deck 三页 metadata 表达不一致,stylistic 统一即可。
- **维度 3 low** · 0. BLUF "## 0." schema 扩展 → author 已尽力(HTML 注释 + frontmatter 双保险),builder 端兼容性 ship 前若解析报错,主线程指引读 special_page_markers。
- **B5 low** · 1.3 "61% 同时用过 CC + Copilot 的开发者更倾向 CC" 数字在 brief.md 字面外但 cite 了 inventory source → 后续可反向把 61% 加进 brief / key-facts 保单一信源。
- **A4 low** · outline line 93 旧文字 "只讲市场 / 数据" 未跟上 R2 1.5 扩展(应改为 "讲市场 + 公司落差/SCQA 的 S+C")— outline 注释级 staleness,不破实际 MECE,下版 outline 修正即可。

---

## Pass Items Highlights

- **A1**:top_recommendation 三要素齐 + 5 维度边界全(本季度 / 工程 100% / 产品 50% / 高层 Deep Research / 3 周 / skill 库)
- **A4 MECE**:5 章演绎序贯穿;R2 加 1.5 在 Ch1 (S+C) 范围内不破 MECE,反而强化 Complication signal
- **A5 纵向链**:1.4 大客户已下注 → 1.5 公司有三类落差 → 0. BLUF 给答案 — narrative tension 完整
- **B7 字数**:handout 字数表全过(实测 5 页全字段);R1 M1/M2 字数 fix 全部正确应用
- **R1 M3 metadata cleanup**:4.3 + 4.1 双修干净,全 cards 扫描无遗漏;build-blocker 解除
- **R2 1.5 narrative pivot**:cards 三卡按 E/T/G+P 视角分层,呼应 brief SCQA C(brief.md line 49-53)字面表达
- **summary 数字驱动**:80.8% / 46% / 100% / 50% / 3 周 / ≥10 个 — 非 toc 重列,真给结论
- **closing actionable**:next_steps 4 项明确 owner + due

---

## 验收建议(给主线程 / 用户)

**Option A · 直接派 builder**(推荐):
- 接受 5 条 low + 1 条 med 作为 notes,不做 polish
- 进 Stage E builder build .pptx;若 4.2 axis 渲染换行 / 遮挡 → 用户审视觉后回头压缩 axis label
- 0. BLUF schema 扩展若 builder Step 0 报错 → 主线程指引读 frontmatter `special_page_markers.bluf`

**Option B · 先 polish 再 build**:
- 维度 3 med · 4.2 axis 5 分钟改 2 处(y_axis low/high → ≤ 8 字)
- 维度 3 low · 4.2 metadata 改 HTML 注释统一(2 分钟)
- 总耗时 < 10 分钟,deck 进 builder 更净

无论 A / B,**R1 must-fix 已闭环、R2 recommended 已落地;deck 已具备进 Stage E 资格**。
