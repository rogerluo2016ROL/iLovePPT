---
title: 让全员上手 Claude Code
subtitle: 从问 AI 答疑,升级到让 AI 直接交付
audience: general
audience_note: |
  用户选 a+b+c 三类全要(executive + technical + general),按 general 处理。
  每章在 intent 里明示对 E / T / G 三视角各意味着什么。
duration_min: 60
presentation_mode: handout
theme: template_training
output: /Users/pc2026/Documents/DevTools/iLovePPT/decks/claude-code-training/deck_v1.pptx

top_recommendation: |
  应当本季度让全员上手 Claude Code,把日常工作从"问 AI 答疑"升级为"让 AI 直接交付":
  工程师 100% 接入做日常开发(目标 2-3× 提效)、产品 / 设计 50% 做辅助生产、
  高层用 Deep Research 模式做调研;3 周完成全员 onboarding,
  并建立公司统一的 skill 库 + prompt 模板,避免重复摸索。

scqa:
  situation: |
    2026 年 AI 编程进入 agentic 阶段 —— 95% 开发者每周用 AI,84% 已用 / 计划用 AI 编程工具;
    Claude Code GA 6 个月达 $1B run-rate(单工具最快),SWE-bench Verified 80.8% 单工具最高,
    46% 开发者评 most loved,Accenture / Salesforce / Cognizant / PwC 已大规模部署。
  complication: |
    公司内可能存在三类落差:(a) 还停留在"问 AI 答疑"(ChatGPT / Copilot 时代),没用上"让 AI 直接交付"的 agentic 能力;
    (b) 各人摸索,没有公司级 skill / prompt 库,重复造轮子;
    (c) 不同岗位缺乏分层使用方法,非工程同事觉得"这是工程师工具与我无关"。
  question: |
    怎么让全员上手 Claude Code,把 agentic 能力变成公司级生产力?
  answer: |
    本季度全员上手:工程 100% / 产品设计 50% / 高层 Deep Research;3 周 onboarding + 公司 skill 库。

footer_meta:
  classification: INTERNAL
  project: claude-code-training
  version: v2.0

asset_inventory_summary: |
  - 数据 / 案例 / 7 特性:_assets/raw/claude-code-key-facts.md
  - 30+ URL 索引(原始来源):_assets/raw/claude-code-sources.md
  - 工具对比详表:_assets/raw/claude-code-comparison.md

# === critic Stage C 应用记录(2026-05-24) ===
critic_round_1_applied:
  must_fix:
    - "A4 MECE:Ch3.2 删 hybrid 内容,改 '任务边界 / prompt 模式 / 协作约定';hybrid 推给 Ch4"
    - "Ch3 demo 占位:3.3 / 3.4 / 3.6 三页保留结构 + pending_data: true,Stage D 跳过拓写,待 1 周试点数据回填"
    - "Ch5.4 标题改 '工程 ≥95% · 产品 ≥80% · skill 库 ≥10 个'(KPI 化,跟 5.2 时间表去重叠)"
    - "BLUF 提前页:cover 后加 single_focus(3 周 + 三视角承诺),deck 34 → 35 页"
  recommended:
    - "维度 1:Ch2.3/2.4/2.5 加数字锚点(Skills 开放标准 / Agent Teams 2026-02 上线 / 24 hook 点位);Ch4.3 cards 推荐 stack 加 highlight"
    - "维度 2:Ch5.2 表格 absorb 里程碑;5 个 section_divider 全部加 sub_caption"
    - "维度 3:Ch3 divider 改 '工程 100% / 产品 50%';Ch4.1 改 '三足鼎立:agentic / 编辑器 / 插件';summary ②③ 数字化"
    - "维度 4:Ch3.1 / 3.4 / 4.2 / 4.3 临界 22 字 → 压缩"
---

# Outline

> **结构**:5 章(MECE,演绎序 Why → What → How → Choose → Implement),每章下分 1-3 内容页,共 ~35 页(含 cover / BLUF / toc / 5 dividers / summary / closing)。
>
> **三视角分层叙事(贯穿)**:每章 intent 里都标注 [E / T / G] 各意味着什么;Ch 3 整章按三视角拆分。
>
> **template_training 调性约束**:section_divider title ≤ 8 字 + sub_caption(新增字段,builder 需扩展 layout 支持;若不支持可降级为 subtitle 单行);内容页 action title ≤ 22 字(template 28pt 换行临界);cards body ≤ 80 字(handout);数据图用 accent4 青绿 `#409694`,避免与 accent1 橙红 `#EF5938` 冲突。

---

## [cover]
- title: 让全员上手 Claude Code
- subtitle: 从问 AI 答疑,升级到让 AI 直接交付  ← 顶端论点 BLUF
- 装饰建议:嵌 `_assets/template_template_training/image2.png`(商务握手深蓝调,适合"团队启动")

## [BLUF · single_focus] —— cover 后 BLUF 提前页(critic must-fix #4)
- layout: single_focus
- title: 本季度全员上手 · 3 周 onboarding
- big_number: 3 周
- explanation: 工程 100% / 产品设计 50% / 高层 Deep Research · 公司统一 skill 库
- intent: 顶端论点的"节奏 + 范围"用大字号提前抛出,后面 5 章全是论据
- source: brief 顶端论点

## [toc] — 章节导航(5 章,toc 5 行已是 template 上限)
1. AI 编程已变 · 市场验证
2. 7 大能力把它变可编程平台
3. 工程 100% / 产品 50% / 高层
4. Hybrid 是主流 · 互补不替代
5. 3 周全员上手 · 建公司 skill 库

---

## 章节 1:AI 编程已变天

> **divider sub_caption**:95% 用 AI · $1B run-rate · 80.8% 性能
> **本章在回答**:为什么是现在?(SCQA 的 S + C)
> **MECE 边界**:只讲市场 / 数据,不讲产品特性(Ch 2)、不讲怎么用(Ch 3)。
> **三视角**:[E] 看市场份额 + ROI 验证 · [T] 看 SWE-bench 80.8% 技术领先 · [G] 看 46% 同行最爱.

### 1.1 95% 开发者每周用 AI,行业已变天
- intent: 用一个震撼数字打开,建立"行业普遍接受"的共识(Situation)
- layout: single_focus
- data: 95%(开发者每周用 AI 辅助)、84%(已用 / 计划用 AI 编程工具)
- diagram: 无(single_focus 自带大数字视觉冲击)
- source: SitePoint 2026 对比

### 1.2 Claude Code 6 个月达 $1B run-rate · 单工具最快
- intent: 用增长曲线证明 Claude Code 不是小众工具,是主流选择(Complication 的反面 —— 别人都上了)
- layout: pic_text
- data: 6 个月 / $1B run-rate / 单工具历史最快
- diagram: matplotlib bar(用 accent4 青绿,X = 月份 0-6,Y = run-rate)
- source: Anthropic Bun 收购公告

### 1.3 SWE 80.8% + Most Loved 46% · 性能口碑双第一
- intent: 用两个权威指标证明技术与口碑都领先,消除"是不是又一个 hype"的质疑
- layout: compare(2 列,左 = 性能 SWE-bench / 右 = 口碑 Most Loved,recommended 不设 —— 都是 Claude Code 数据)
- data: SWE-bench Verified 80.8%(单工具最高);Most Loved 46% / Cursor 19% / Copilot 9%
- diagram: 无
- source: tech-insider / SitePoint

### 1.4 Accenture 数万 / Salesforce 全组织 · 大客户已下注
- intent: 用大企业案例从抽象数字转到具体落地,给 executive 看 "别人已经在做"
- layout: cards(4 卡 · Accenture / Salesforce / Cognizant / PwC,handout 模式 body 写完整句解释规模 + 价值)
- data: Accenture 数万开发者(Anthropic 史上最大单笔)/ Salesforce 全球工程组织 / Cognizant 35 万员工可用 / PwC 技术+业务
- diagram: 无
- source: Anthropic news ×4

### 1.5 公司三类落差 · 为什么我们要现在动(critic R2 R2 新增 · SCQA C 明示页)
- intent: SCQA C(Complication)明示页 —— 把市场 S(1.1-1.4)与公司现状 gap 拉到读者面前,加强 narrative tension;呼应 BLUF 答案
- layout: **cards_flag_3**(v2 R5++ · 三类性质区分语义最契合 flag 风;旧 cards layout)
- data:
  - 看不到 ROI(高层视角):还把 AI 当 "工程团队工具",看不到 executive 自己的 Deep Research 价值 → 投入推迟
  - 自学摸索(工程视角):个人在用,无统一 skill / prompt 库,重复造轮子,新人 onboard 慢
  - 用不来(产品 / 设计 / 高层):觉得 "工程师工具与我无关",agentic 能力被局限在 1/3 公司
- diagram: 无
- source: brief.md SCQA · Complication 三类落差

---

## 章节 2:7 力解构平台

> **divider sub_caption**:agentic 系统 · 7 能力可编程
> **本章在回答**:它到底是什么 · 跟"AI 补全"差在哪?(回答 Q 的前半 —— 范围 / 能力边界)
> **MECE 边界**:只讲产品能力,不讲市场(Ch 1)、不讲使用方法(Ch 3)。
> **三视角**:[E] 看 7 能力 = 可编程性 = 抗供应商锁定 · [T] 看每个能力的扩展点 · [G] 看 CLAUDE.md / Skills 也能用(不只工程).

### 2.1 不是补全工具 · 是 agentic 编程系统
- intent: 一句话讲清 framing 差异(从"问答疑"→"让 AI 直接交付"),建立全章心智模型
- layout: compare_pk(左 = 问 AI 答疑 Copilot / ChatGPT 时代,右 = 让 AI 直接交付 agentic 时代)
- data: 端到端读 codebase / 跨文件改 / 跑测试 / 迭代 / 显式申请权限
- diagram: 无
- source: Claude Code 产品页

### 2.2 7 大能力总览:从 CLAUDE.md 到 MCP
- intent: 给一张能力地图,后续 2.3 / 2.4 / 2.5 选 3 个高价值点细展开
- layout: pic_text(左 = 7 能力 architecture 图;右 = 每个能力 1 句简介)
- data: CLAUDE.md / Skills / Subagents / Agent Teams / Hooks / Plugins / MCP
- diagram: drawio simple_relation(中央 Claude Code,7 个能力放射,3 层从内到外:基础层 CLAUDE.md / Skills,中层 Subagents / Agent Teams / Hooks,扩展层 Plugins / MCP)
- source: 7 特性来自 Towards AI / Anthropic Skills 官方

### 2.3 Skills:可重用工作流 · 团队级沉淀的关键
- intent: 重点细化 Skills(它是 Anthropic 开放标准,是公司级 skill 库的基础)
- layout: cards(3 卡:"是什么 / 为什么重要 / 怎么沉淀")
- data: 200 字 prompt → SKILL.md 一次写,后续 slash command 永远可用;**Anthropic Skills 已成开放标准(Agent Skills)**;Claude Code 在标准之上加 invocation control / subagent execution / dynamic context injection
- diagram: 无
- source: code.claude.com/skills

### 2.4 Subagents + Agent Teams:多 agent 协作的新范式
- intent: 细化最新能力(Agent Teams 2026-02-05 上线),给 technical 看技术深度,顺便埋伏笔说 "iLovePPT 自己也用这个机制"
- layout: pic_text(左 = Subagents 隔离 / Agent Teams 协作的关系图;右 = 两个能力差异 + 各自适用场景)
- data: Subagents 独立 context · summary 返回主对话;**内置 3 种 subagent(Explore / Plan / general-purpose)**;**Agent Teams 2026-02-05 上线**,多 session 互发消息 · 并行分工
- diagram: drawio simple_relation(主对话 vs Subagent 隔离窗口;Agent Team 多节点互连)
- source: Developers Digest 2026 Playbook

### 2.5 Hooks + Plugins + MCP:确定性 + 分发 + 外部连接
- intent: 把剩下 3 能力放一组(都是 "扩展层"),避免每能力一页过于碎
- layout: cards(3 卡)
- data: **Hooks 事件驱动 / 不会 hallucinate / ~24 个 hook 点位**;**Plugins 一键安装 · 打包 skills / agents / hooks / MCP / LSP / monitor**;**MCP 标准化协议 · 接 GitHub / Linear / Notion / 自定义内部系统**
- diagram: 无
- source: Nimbalyst / Towards AI

### 2.6 Anthropic 内部:消息项目从 1 周 → 2 个 30 分钟 call
- intent: 一个具体案例收口 Ch 2,把抽象能力变成可感知的提效
- layout: compare_pk(左 = 以前 1 周跨部门协调;右 = 现在 2 个 30 分钟 call)
- data: GA 上线 messaging 这种复杂跨部门项目的复盘
- diagram: 无
- source: Anthropic 团队怎么用 Claude Code PDF

---

## 章节 3:工程 100% / 产品 50%

> **divider sub_caption**:工程 100% / 产品设计 50% / 高层 Deep Research
> **本章在回答**:具体怎么用 · 我这个岗位能用吗?(回答 Q 的后半 —— 落地方法)
> **MECE 边界**:按"使用者角色"切分,三视角覆盖全员;**不涉及工具选型(Ch 4)**、不涉及落地节奏(Ch 5)。
> **三视角**:整章就是三视角骨架,每节明确一个角色 + before / after demo。
> **占位说明**:3.3 / 3.4 / 3.6 三页结构保留,内容标 `pending_data: true`,Stage D 拓写时跳过;待 1-2 工程师 + 1 产品跑 1 周 Claude Code 真实试点后回填 before / after。

### 3.1 工程 100% / 产品设计 50% / 高层调研模式
- intent: 全章地图,先给"每个角色用多少 + 用什么模式"的总览
- layout: **tri_pyramid_4sub_3**(v2 R5++ · 三视角天生金字塔 native layout;旧 pic_text + PNG · 原 PNG `_assets/charts/3_1_etg_pyramid.png` 废弃为对比备份)
- data: Engineer 100% 日常开发 / Product+Design 50% 辅助生产 / Executive Deep Research 调研
- diagram: drawio simple_relation(3 层金字塔 + 每层使用率徽章)
- source: brief 顶端论点

### 3.2 工程师:任务边界 + prompt 模式 + 协作约定
- intent: T 视角第 1 节 —— **只讲工程师怎么用 CC**(critic must-fix #1:hybrid 推给 Ch4,本节不再讲 "什么任务用 Copilot")
- layout: cards(3 卡:"任务边界 / prompt 模式 / 协作约定")
- data:
  - 卡 1 任务边界:复杂调试 / 跨文件 refactor / 端到端 agentic 任务交给 CC;单文件补全留给 IDE(具体哪个工具见 Ch 4)
  - 卡 2 prompt 模式:Plan 模式先规划再执行 / 显式申请权限 / CLAUDE.md 写项目规约 / Skills 沉淀重复流程
  - 卡 3 协作约定:PR 标 "claude-code-assisted" / 关键改动人审 / 不在敏感模块全自动放权 / 复盘失败 prompt
- diagram: 无
- source: brief 顶端论点 + claude-code-key-facts.md "最佳实践"

### 3.3 工程 Demo · Bug 修复 before / after [TBD]
- intent: T 视角 demo 1 —— **占位**,待 1 周试点数据回填
- layout: compare_pk(左 = 试点前 / 右 = 试点后)
- pending_data: true
- placeholder_body: "[TBD · 待 1 周试点数据回填 · 占位说明:此处将填入 1-2 工程师跑 1 周 Claude Code 的真实 Bug 修复任务 before / after,含 prompt + 输出片段 + 耗时对比]"
- diagram: 无(后续 builder 跳过拓写,留空白页带占位 banner)
- source: 待试点回填

### 3.4 工程 Demo · 跨文件 refactor [TBD]
- intent: T 视角 demo 2 —— **占位**,待 1 周试点数据回填(强调 "跨文件" 是 agentic 关键差异)
- layout: compare_pk(左 = 试点前 / 右 = 试点后)
- pending_data: true
- placeholder_body: "[TBD · 待 1 周试点数据回填 · 占位说明:此处将填入 1 工程师跑 1 次跨 ≥5 文件 refactor 的 before / after,含 prompt + 输出片段 + 耗时对比]"
- diagram: 无
- source: 待试点回填

### 3.5 产品 / 设计:50% 做辅助生产 · 文档 / 原型 / 数据
- intent: P 视角(归为 G 大类) —— 给产品 / 设计同事看适用场景
- layout: cards(3 卡:"PRD 起草 / 原型快速 mockup / 数据分析")
- data: 任务类型 + 推荐 prompt 模式 + 注意事项([示意])
- diagram: 无
- source: 示意,基于 Anthropic 团队 PDF 中跨岗位使用经验

### 3.6 产品 Demo · 调研报告 before / after [TBD]
- intent: P 视角 demo —— **占位**,待 1 周试点数据回填
- layout: compare_pk(左 = 试点前 / 右 = 试点后)
- pending_data: true
- placeholder_body: "[TBD · 待 1 周试点数据回填 · 占位说明:此处将填入 1 产品跑 1 次竞品 / 行业调研报告 before / after,含 Deep Research prompt + 输出结构 + 耗时对比]"
- diagram: 无
- source: 待试点回填

### 3.7 高层:Deep Research 做调研 · 季度报告草稿
- intent: E 视角 —— 给高层看 "你也能直接用,不只是签字"
- layout: cards(3 卡:"行业调研 / 竞争对手分析 / 季度报告草稿")
- data: Deep Research 典型 prompt 模式 + 适合的输入数据类型 + ROI 估算
- diagram: 无
- source: Anthropic Deep Research 文档,brief 顶端论点

---

## 章节 4:Hybrid 是主流

> **divider sub_caption**:三足鼎立 · 互补共存 · 平均 2.3 工具
> **本章在回答**:跟 Cursor / Copilot 怎么选?会不会冲突?(消除"那已有的怎么办"的疑虑)
> **MECE 边界**:只讲工具选型 + 互补关系;**Ch 3 已剥离 hybrid 内容,本章独家承接**;不重复 Ch 2 的能力介绍。
> **三视角**:[E] 看 hybrid 减锁定风险 · [T] 看 stack 推荐 · [G] 看不必弃用 Copilot.

### 4.1 三足鼎立:agentic / 编辑器 / 插件
- intent: 用一句话把三个工具的定位讲清,破除"取代"的错误叙事
- layout: compare(3 列 · Claude Code / Cursor / Copilot,每列 = 定位 + 强项 + 适用场景;recommended = Claude Code 列)
- data: CC = agentic 系统 / Cursor = AI-first 编辑器 / Copilot = IDE 插件
- diagram: 无
- source: claude-code-comparison.md

### 4.2 规模决定工具:小型 CC 75% · 大企 Copilot 56%
- intent: 用市场份额分层数据,告诉读者本公司应该选哪个组合
- layout: matrix_2x2(x = 公司规模 小 / 大,y = 工具偏好 agentic / inline;quadrant = 4 类典型 stack;highlight = 本公司预估位置)
- data: 小型创业 CC 75% / Cursor 42%;大企业 Copilot 56%;中型混合
- diagram: 无(matrix_2x2 自带视觉)
- source: SitePoint 采用率分层

### 4.3 Hybrid Stack 推荐:Copilot 补全 + CC agentic
- intent: 给出具体推荐组合,落到岗位级建议
- layout: **cards_flag_3**(v2 R5++ · 三种 stack 性质区分 + highlight: card_2 配合;旧 cards · 旗帜风强化决策页)
- data: 经验丰富开发者平均同时用 2.3 个工具(2026 survey)
- card_extension_note: |
  cards 默认 schema 无 highlight 字段,本页是 layout 扩展请求 —— builder 阶段若 cards 未支持 highlight,可降级为 compare 3 列(第 2 列 recommended: true)
- diagram: 无
- source: claude-code-comparison.md "Hybrid 是主流" 章节

---

## 章节 5:3 周全员上手

> **divider sub_caption**:W1 工程 / W2 产品 / W3 高层 · 公司 skill 库
> **本章在回答**:怎么落地 · 谁什么时候做什么?(顶端论点的 "3 周 onboarding + skill 库" 的具体节奏)
> **MECE 边界**:只讲落地节奏 + KPI + skill 库;**Ch5.2 时间表 absorb 关键里程碑**(原 5.4 里程碑并入,5.4 转 KPI 验收专页);不再讲产品 / 工具选型。
> **三视角**:[E] 看 3 周时间表 + KPI 验收 · [T] 看 skill 库治理 + ownership · [G] 看每个人 W1 / W2 / W3 做什么.

### 5.1 3 周节奏:W1 工程 → W2 产品 → W3 高层
- intent: **执行层节奏概览**(critic R2 med_1 微调:跟 Page 2 BLUF "战略层 3 周 + 全员上手" 拉开 —— Ch5.1 落到三周的分阶段执行节奏,3 行 bullet 一目了然,5.2 表格再展开 day-by-day)
- layout: **timeline_band_3**(v2 R5++ · 三段时序天生 timeline 结构,W1/W2/W3 色块 + 上下交错破 audience R4 "bullet 上 1/3 空白";旧 bullet_list)
- data:
  - W1(工程):5 半天 · CLAUDE.md + Skills + 1 真实任务 · 接入率 ≥95%
  - W2(产品 / 设计):4 半天 · Deep Research + PRD demo · 覆盖率 ≥80%
  - W3(高层):2 半天 · 调研模式 + 季度报告 demo · ≥3 人完成 1 次 Deep Research
- diagram: 无
- source: brief 顶端论点,3 周节奏自定

### 5.2 3 周时间表:W1 工程 → W2 产品设计 → W3 高层
- intent: 把 3 周展开成 day-by-day 时间表 + **关键里程碑列**(critic recommended 维度 2:absorb 原 5.4 里程碑)
- layout: table(列 = Week / Day / 对象 / 内容 / 负责人 / **关键里程碑**;handout 模式可多行)
- data:
  - W1 工程 5 个半天:CLAUDE.md + Skills + 1 个真实任务;里程碑 = 工程师 ≥95% 接入
  - W2 产品设计 4 半天:Deep Research + PRD demo;里程碑 = 产品设计 ≥80% 接入
  - W3 高层 2 半天:调研模式 + 季度报告 demo;里程碑 = 高层 ≥3 人完成 1 次 Deep Research
  - 每周末 1 次 retro 复盘,沉淀 ≥3 个 skill 进库
- diagram: 无(table 已足够)
- source: brief 顶端论点,3 周节奏自定

### 5.3 公司 Skill 库:统一 prompt + 复用 · 避免重复摸索
- intent: 落地的关键基础设施 —— skill 库治理
- layout: pic_text(左 = skill 库目录结构图 / 治理流程;右 = ownership / 贡献流程 / review 节奏)
- data: SKILL.md 模板 + slash command 命名约定 + monthly review;首批沉淀 10 个高频 skill
- diagram: drawio simple_relation(skill 库结构:repo / .claude/skills/ / 各 skill folder)
- source: brief 顶端论点,Anthropic Skills 标准

### 5.4 工程 ≥95% · 产品 ≥80% · skill 库 ≥10 个
- intent: KPI 验收专页(critic must-fix #3 + 维度 2 合并:原 5.4 里程碑已归并到 5.2 表格,本页只讲 KPI 数值 + 验收口径)
- layout: cards(3 卡 · 每卡 1 个 KPI:接入率 / 覆盖率 / skill 库存量;每卡含数值 + 验收方式 + Owner)
- data:
  - 卡 1:工程师接入率 ≥ 95% · 验收 = Q2 月底 PR commit 含 CC 标签的工程师占比 · Owner = 工程团队 lead
  - 卡 2:产品 / 设计覆盖率 ≥ 80% · 验收 = 跑通 ≥1 次 Deep Research 或 PRD demo · Owner = 产品 / 设计团队 lead
  - 卡 3:公司 skill 库存量 ≥ 10 个 · 验收 = Q2 月底入库 ≥10 个 + 至少 3 人贡献 · Owner = 平台团队
- diagram: 无
- source: brief 顶端论点,KPI 自拟

### 5.5 行动清单:今天就能做的 3 件事
- intent: 培训 deck 收尾必须给 actionable 清单,把 "听完没动作" 这个最大失败模式堵住
- layout: cards(3 卡 · 工程师 / 产品设计 / 高层 各 1 张,每张写 "今天 / 本周 / 本月" 三个行动)
- data: 今天:装 Claude Code;本周:跑通一个真实任务;本月:贡献 1 个 skill
- diagram: 无
- source: brief 顶端论点

---

## [summary]
- 顶端论点回顾:本季度全员上手 Claude Code · 3 周 onboarding · 公司 skill 库
- 三视角承诺:**工程 100% · 产品设计 50% · 高层 Deep Research · 3 周完成**(critic 维度 3 数字化)
- 落地节奏:**W1 工程 → W2 产品 → W3 高层 · skill 库首批 ≥10 个**(critic 维度 3 数字化)
- 核心 ROI 锚点:80.8% SWE-bench · 46% Most Loved · Accenture 万人部署 · 几周 vs 几季度

## [closing]
- subtitle: 今天就装上 Claude Code,W1 见
- next_steps:
  - action: 工程师装 Claude Code · 跑通一个真实任务
    owner: 工程团队
    due: 本周
  - action: 产品 / 设计跑通 Deep Research demo
    owner: 产品设计团队
    due: W2
  - action: 高层完成 1 次季度调研草稿生成
    owner: 高管团队
    due: W3
  - action: 公司 skill 库首批 10 个 skill 沉淀
    owner: 平台团队
    due: Q2 月底
- 装饰建议:嵌 `_assets/template_template_training/image4.png`(QR 课程评价 / 反馈入口)

---

# 图层规划(diagram_plan)

| section | layout | diagram_type | tool | intent |
|---|---|---|---|---|
| 1.2 | pic_text | chart | matplotlib | $1B run-rate 6 月增长曲线(青绿 #409694) |
| 2.2 | pic_text | arch_diagram | drawio | 7 能力 3 层放射图(基础 / 中层 / 扩展) |
| 2.4 | pic_text | simple_relation | drawio | Subagents 隔离 + Agent Teams 互连 |
| 3.1 | pic_text | arch_diagram | drawio | E/T/G 3 层金字塔 + 使用率徽章 |
| 5.3 | pic_text | simple_relation | drawio | 公司 skill 库结构 + 贡献流程 |

> 全 deck ~35 页,5 张图 → 约 7 页 / 图,密度合适。
> 数据图(1.2)颜色用 accent4 青绿 `#409694`,避免与 accent1 橙红 `#EF5938` 冲突(template_training 调性约束)。
> Ch 3 的 3 个 [TBD] demo 页占位中无图,builder 会留空白带 "TBD · 待试点数据回填" banner。

---

# Pyramid 自检(critic Round 1 修改后重跑)

- [x] ① **单一顶端论点存在** —— top_recommendation 完整推荐句:"本季度全员上手 + 工程 100% / 产品 50% / 高层 Deep Research + 3 周 onboarding + 公司 skill 库",动宾 + 具体边界 + 节奏 全齐。
- [x] ② **SCQA 完整** —— S(95% 用 AI / Claude Code $1B / 80.8%)、C(三类落差 a/b/c)、Q(怎么让全员上手)、A(同顶端论点);C 是冲突而非 S 复述。**A 在 cover.subtitle + BLUF 页(新增)双重明示。**
- [x] ③ **答案在前** —— cover.subtitle = 顶端论点简化版;**cover 后 single_focus BLUF 页(critic must-fix #4)再次明示 "3 周" + 三视角承诺**;每个 section_divider title 是结论简称(AI 编程已变天 / 7 力解构平台 / 工程 100% / 产品 50% / Hybrid 是主流 / 3 周全员上手),全是结论非话题标签。
- [x] ④ **MECE(3-5 节,两两不重叠)** —— 5 节:Why / What / How / Choose / Implement。
      - Ch 1 只讲市场,Ch 2 只讲产品能力,Ch 4 只讲工具选型,Ch 5 只讲落地节奏。
      - **Ch 3 已剥离 hybrid 内容**(critic must-fix #1):3.2 改为 "工程师怎么用 CC"(任务边界 / prompt 模式 / 协作约定),hybrid 完全归 Ch 4。
      - **Ch 5.4 / 5.5 边界已分**(critic 维度 2):5.4 = 纯 KPI 验收(数值 + 验收口径 + Owner);5.5 = 纯行动清单(今天 / 本周 / 本月);里程碑归 5.2 表格。
      - 听众听完不会问 "那 X 呢"。
- [x] ⑤ **章节排列方式一致** —— 演绎序(Why now → What is it → How to use → Choose stack → Implement),5 章一以贯之。
- [x] ⑥ **纵向疑问链通过(ghost deck test)** —— 重新串读:
      "cover BLUF '3 周 + 三视角承诺' → AI 编程已变天 → 95% 用 AI / $1B / 80.8% + 46% / 大客户已下注 → 7 力解构平台 → agentic vs 补全 / 7 力总览 / Skills 重要 / Subagents + Teams / Hooks + Plugins + MCP / 1 周 → 2call → 工程 100% / 产品 50% → 三视角总览 / 工程师任务边界 + 模式 + 协作 / 工程 demo×2 [TBD] / 产品设计 50% / 产品 demo [TBD] / 高层 Deep Research → Hybrid 是主流 → 三足鼎立 / 规模决定工具 / hybrid stack 推荐 → 3 周全员上手 → 节奏 / 时间表+里程碑 / skill 库 / KPI 验收 / 行动清单 → summary + closing。"
      读完串通顶端论点 "本季度全员上手 + 3 周 + skill 库",无断裂。
      **Ch 3 三个 [TBD] 占位页虽内容未拓写,但 action title 仍是结论形态,串读链不破。**
- [x] ⑦ **全部 action title ≤ 24 字(template 实际 ≤ 22 字)** —— **本轮逐条复核**(中文计 1,英文 / 数字 计 0.5):
      - cover.subtitle "从问 AI 答疑,升级到让 AI 直接交付" = 14.5
      - BLUF "本季度全员上手 · 3 周 onboarding" = 14
      - 1.1 "95% 开发者每周用 AI,行业已变天" = 14
      - 1.2 "Claude Code 6 个月达 $1B run-rate · 单工具最快" = 19.5
      - 1.3 "SWE 80.8% + Most Loved 46% · 性能口碑双第一" = 19.5(已压缩自原 22.5)
      - 1.4 "Accenture 数万 / Salesforce 全组织 · 大客户已下注" = 21.5
      - 2.1 "不是补全工具 · 是 agentic 编程系统" = 15
      - 2.2 "7 大能力总览:从 CLAUDE.md 到 MCP" = 13.5
      - 2.3 "Skills:可重用工作流 · 团队级沉淀的关键" = 18
      - 2.4 "Subagents + Agent Teams:多 agent 协作的新范式" = 20.5
      - 2.5 "Hooks + Plugins + MCP:确定性 + 分发 + 外部连接" = 19
      - 2.6 "Anthropic 内部:消息项目从 1 周 → 2 个 30 分钟 call" = 21
      - 3.1 "工程 100% / 产品设计 50% / 高层调研模式" = 16.5(已压缩自原 24)
      - 3.2 "工程师:任务边界 + prompt 模式 + 协作约定" = 17.5
      - 3.3 "工程 Demo · Bug 修复 N× 提速 [待 W1 回填]" = 17.5(R2 升级数字占位结论模板)
      - 3.4 "工程 Demo · Refactor M h → H min [待 W1 回填]" = 19.5(R2 升级)
      - 3.5 "产品 / 设计:50% 做辅助生产 · 文档 / 原型 / 数据" = 19
      - 3.6 "产品 Demo · 调研 K h → Y min [待 W2 回填]" = 17.5(R2 升级)
      - **1.5 "公司三类落差 · 为什么我们要现在动" = 15.5(R2 新增 SCQA C 明示页)**
      - 3.7 "高层:Deep Research 做调研 · 季度报告草稿" = 18.5
      - 4.1 "三足鼎立:agentic / 编辑器 / 插件" = 14(critic 维度 3 改自 "定位差异显著")
      - 4.2 "规模决定工具:小型 CC 75% · 大企 Copilot 56%" = 18.5(已压缩自原 22.5)
      - 4.3 "Hybrid Stack 推荐:Copilot 补全 + CC agentic" = 19(已压缩自原 23)
      - 5.1 "3 周节奏:W1 工程 → W2 产品 → W3 高层" = 16(critic R2 med_1 微调)
      - 5.2 "3 周时间表:W1 工程 → W2 产品设计 → W3 高层" = 19.5
      - 5.3 "公司 Skill 库:统一 prompt + 复用 · 避免重复摸索" = 19.5
      - 5.4 "工程 ≥95% · 产品 ≥80% · skill 库 ≥10 个" = 15.5(critic must-fix #3)
      - 5.5 "行动清单:今天就能做的 3 件事" = 12.5
      **全部 ≤ 22 字 ✓,最长 21.5(1.4)和 21(2.6)有一定余量但未超 template 上限。**
      section_divider title 也复核:
      - "AI 编程已变天" = 6
      - "7 力解构平台" = 5.5
      - "工程 100% / 产品 50%" = 8(踩线但未超)
      - "Hybrid 是主流" = 6
      - "3 周全员上手" = 5.5
      **全 ≤ 8 字 ✓**

**自检结论**:7 项全过 ✓,可送 critic 复核。

---

# 页数预估

| 类型 | 页数 |
|---|---|
| cover | 1 |
| **BLUF single_focus(critic must-fix #4 新增)** | **1** |
| toc | 1 |
| section_divider × 5 | 5 |
| Ch 1 内容页 | 5(R2 新增 1.5 SCQA C 明示页) |
| Ch 2 内容页 | 6 |
| Ch 3 内容页(含 3 个 [TBD] 占位) | 7 |
| Ch 4 内容页 | 3 |
| Ch 5 内容页 | 5 |
| summary | 1 |
| closing | 1 |
| **合计** | **36** |

预期 1.5×60 = 90 页(speaker 公式);**handout 模式信息密度 3-4×,1 页 ≈ 1.7 min**,36 页 × ~1.7 min ≈ 60 min,匹配 duration。**仍在 brief 30-40 页 handout 区间**(critic R2 R2 加 SCQA C 后,从 35 → 36)。

---

# critic Round 1 + R2 修改记录(audit trail)

| critic 项 | 修改内容 | 实际改动位置 |
|---|---|---|
| Must-fix #1 A4 MECE | Ch3.2 cards 改 "任务边界 / prompt 模式 / 协作约定";hybrid 推 Ch4 | 3.2 cards data 重写 + Ch 3 / Ch 4 MECE 边界声明 |
| Must-fix #2 Ch3 demo 占位(用户选 A) | 3.3 / 3.4 / 3.6 三页保留结构,内容标 `pending_data: true` + 占位说明 | 3.3 / 3.4 / 3.6 加 pending_data + placeholder_body 字段 |
| Must-fix #3 Ch5.4 标题 | "责任分工 + 关键里程碑" → "工程 ≥95% · 产品 ≥80% · skill 库 ≥10 个" + 内容转 KPI 验收 | 5.4 title + layout + data 重写 |
| Must-fix #4 BLUF 提前页 | cover 后加 single_focus,3 周 + 三视角承诺 | 新增 [BLUF · single_focus] section,deck 34 → 35 页 |
| 维度 1 数字锚点 | Ch2.3 加 Anthropic Skills 开放标准;Ch2.4 加 Agent Teams 2026-02-05 上线 + 内置 3 种 subagent;Ch2.5 加 ~24 hook 点位 | 2.3 / 2.4 / 2.5 data 字段加粗 |
| 维度 1 Ch4.3 highlight | cards 第 2 卡 "不换编辑器" 加 highlight: true + builder 降级备注 | 4.3 layout + card_extension_note |
| 维度 2 Ch5.2 absorb 里程碑 | table 列加 "关键里程碑" + 各 W 写入里程碑 | 5.2 data 字段重写 |
| 维度 2 section_divider sub_caption | 5 个 divider 全部加 sub_caption | 各章 heading 下加 "> **divider sub_caption**: ..." |
| 维度 3 Ch3 divider 改名 | "E/T/G 三分用" → "工程 100% / 产品 50%" + toc 同步 | Ch 3 heading + toc 第 3 项 |
| 维度 3 Ch4.1 改名 | "三足鼎立 · 定位差异显著" → "三足鼎立:agentic / 编辑器 / 插件" | 4.1 标题 |
| 维度 3 summary 数字化 | summary ② ③ 加 "3 周完成" + "首批 ≥10 个" | summary 二三条 |
| 维度 4 临界压缩 | 1.3 / 3.1 / 3.4 / 4.2 / 4.3 action title 压缩 | 各页标题 + #7 复核字数明示 |
| **R2 med_1 Ch5.1 去重** | Ch5.1 从 single_focus(与 Page 2 BLUF 90% 重叠) → bullet_list 3 条;title 改 "3 周节奏:W1 工程 → W2 产品 → W3 高层";落到执行层节奏(战略层留给 BLUF) | 5.1 layout / title / data 重写 + ⑦ 字数同步 |
| R2 low(action title placeholder / 数字重复 / divider 桥句) | outline 不动,Stage D 拓写时一并处理 | Stage D content.md |

# critic Stage D R1 修订记录(2026-05-24 · 本轮新增)

| critic Stage D R1 项 | 修改内容 | 实际改动位置 |
|---|---|---|
| Must-fix M1 · 2.4 Subagents body 字数 | 3 个 point 全部压到 ≤ 50 字(Subagents 47 / Agent Teams 43 / iLovePPT 45) | content.md 2.4 |
| Must-fix M2 · 5.3 双 point ≤ 50 | 目录结构 47 / 贡献流程 43;治理 Owner 45.5 保留 | content.md 5.3 |
| Must-fix M3 · 4.3 card 2 builder metadata 泄漏(build-blocker) | 删 body 内 "highlight: true(...)" 整段;以 HTML 注释替代;扫描发现 4.1 同类问题一并修 | content.md 4.3 + 4.1 + HTML 注释 |
| Recommended R1 · 1.2 chart M0-M5 estimated 视觉 | 重画 matplotlib:M0-M5 alpha 0.55 + hatch "///";M6 solid 深蓝;新加 Legend 明示 | _assets/charts/1_2_run_rate.png 重渲染 |
| **Recommended R2 · SCQA C 加明示页** | **新增 1.5 cards 3 卡 · 公司三类落差(看不到 ROI / 自学摸索 / 用不来);deck 35 → 36 页;Ch1 divider sub_caption 同步更新提及"三类落差"** | outline + content 都加 1.5 |
| Recommended R3 · 3.3/3.4/3.6 TBD title 升级数字占位 | 3.3 "Bug 修复 N× 提速 [待 W1 回填]" / 3.4 "Refactor M h → H min [待 W1 回填]" / 3.6 "调研 K h → Y min [待 W2 回填]" | content.md + outline ⑦ 字数同步 |
| Recommended R4 · BLUF "## 0." h2 marker | 加 HTML 注释 + frontmatter `special_page_markers.bluf` 字段告 builder | content.md `## 0.` heading + frontmatter |
| Recommended R5 · Ch3 篇幅 pending_data 联动 | 无改动(critic 明示不强动) | — |

# v2 R5++ 全方位改造记录(audience R4 = 8.42 → 目标 8.7-8.8 · 2026-05-24)

> v1 baseline 已保留为 `deck_v1_baseline.pptx`(8.42/10)。v2 = R5++ 全方位改造(本任务);v3 = W1 实测数据回填(将来另一轮)。
> 5 杠杆并行:① 3 个新 visual-pattern layout 切换 · ② WebSearch evidence anchor · ③ G 视角翻译层 · ④ 4 扉页 sub_caption 削字 · ⑤ p7 evidence 强化。
> **outline 仅 5 处 layout 字段变更**(p9 / p18 / p28 / p30 切新 pattern · 标 R5++)+ ⑦ 字数复核表新增;**action title 0 变更**,Pyramid 7 项不重跑(无影响)。

| 杠杆 | 页 | 改动 | 实际位置 |
|---|---|---|---|
| **杠杆 1 · 新 layout** | p9 (1.5) | cards → **cards_flag_3** · "三类性质区分" | outline + content layout 字段 |
| **杠杆 1 · 新 layout** | p18 (3.1) | pic_text → **tri_pyramid_4sub_3** · E/T/G 金字塔 native;原 PNG 废弃备份 | outline + content layout + 移除 ![]() |
| **杠杆 1 · 新 layout** | p28 (4.3) | cards → **cards_flag_3** · Hybrid Stack 三类 + highlight: card_2 配合 | outline + content layout 字段 |
| **杠杆 1 · 新 layout** | p30 (5.1) | bullet_list → **timeline_band_3** · W1/W2/W3 色块时间轴 | outline + content layout + segments 字段 |
| **杠杆 2 · evidence** | p20 source | 旧 "预估值" → 新 "预估 4-8× · 同序级锚:Anthropic 安全团队 15min → 5min(3×,Anthropic PDF)" | content.md 3.3 source caption |
| **杠杆 2 · evidence** | p21 source | 旧 "预估值" → 新 "预估 8-12× · 同序级锚:Anthropic 消息项目 1 周 → 2×30min(~14×)" | content.md 3.4 source caption |
| **杠杆 2 · evidence** | p23 source | 旧 "预估值" → 新 "预估 6-10× · 同序级锚:Claude.ai 任务 3.1h → 15min(~12×,Sacra)" | content.md 3.6 source caption |
| **杠杆 2 · evidence** | p7 body | right col body 加 1 句市场印证锚 "Anthropic Q1 2026 总营收 $30B / Claude Code $2.5B" | content.md 1.3 right col body(轻越限 ⚠ 80→120,审计留痕) |
| **杠杆 3 · G 翻译** | p20 right.body | 末尾追加 "通俗讲:让 CC 直接读 codebase + 改代码 + 跑测试,不再逐行教写法。" | content.md 3.3 right.body |
| **杠杆 3 · G 翻译** | p21 right.body | 末尾追加 "通俗讲:跨多个文件的大改动,CC 一次列清全部影响点,人脑不再漏看依赖。" | content.md 3.4 right.body |
| **杠杆 3 · G 翻译** | p23 right.body | 末尾追加 "通俗讲:一次问完直接出带引用的初稿,人只做事实校对,不用逐篇搜整理。" | content.md 3.6 right.body |
| **杠杆 4 · 扉页削字** | p10 (Ch2 divider) | sub_caption 67 → 24 字:"Claude Code 不是 IDE 插件,是可编程 agentic 平台。" | content.md ch2 section_divider |
| **杠杆 4 · 扉页削字** | p17 (Ch3 divider) | sub_caption 54 → 22 字:"三视角分层,无人旁观 · 每人按自己角色装 CC。" | content.md ch3 section_divider |
| **杠杆 4 · 扉页削字** | p25 (Ch4 divider) | sub_caption 50 → 24 字:"答案不是取代而是 hybrid 共存 · 推荐 stack 见本章。" | content.md ch4 section_divider |
| **杠杆 4 · 扉页削字** | p29 (Ch5 divider) | sub_caption 53 → 21 字:"本季度 3 周节奏 + 公司 skill 库基础设施。" | content.md ch5 section_divider |
| **杠杆 5 · p7 evidence** | p7 right.body | 同杠杆 2(已合并) | content.md 1.3 |
| **kept_unchanged** | — | 3 TBD 页 pending_data flag 保留(v3 待 W1 数据回填) · action title 0 改 · outline MECE / SCQA / Pyramid 全部未动 · cover / BLUF / toc / closing 未动 | — |

## v2 R5++ Pyramid 自检 ⑦ 字数复核(本轮无 action title 改动)

| 页 id | action title | 字数 | 备注 |
|---|---|---|---|
| (无新增 / 无修改) | — | — | v2 R5++ 全部是 layout / body / sub_caption 改动,outline action title 一字不动;Pyramid 7 项全部不重跑(无影响) |

## v2 R5++ 预估 audience R5 评分

| 改动类型 | 预估 delta | 累加 |
|---|---|---|
| 3 个新 layout 视觉破节奏 + native pattern | +0.15-0.20 | 8.42 → 8.57-8.62 |
| WebSearch evidence anchor(T 视角 fix) | +0.10-0.15 | 8.57-8.62 → 8.67-8.77 |
| G 视角翻译层(p20/21/23) | +0.05-0.08 | 8.67-8.77 → 8.72-8.85 |
| 4 扉页 sub_caption 削字 | +0.03-0.05 | 8.72-8.85 → 8.75-8.90 |
| p7 evidence anchor 强化(轻) | +0.02-0.03 | 8.75-8.90 → 8.77-8.93 |

**v2 R5++ 综合预估**:**8.77-8.93**(下限 8.77 已超用户目标 8.7-8.8 中位,上限破 9 概率 < 25%)。
**3 TBD 页 pending_data flag 仍保留** —— v2 是 R5++ polish 极限,v3 才是 W1 实测数据回填(自然破 9 路径)。
