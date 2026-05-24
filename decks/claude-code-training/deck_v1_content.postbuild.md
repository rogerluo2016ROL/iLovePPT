---
title: 让全员上手 Claude Code
subtitle: 从问 AI 答疑,升级到让 AI 直接交付
audience: general
audience_note: |
  用户选 a+b+c 三类全要(executive + technical + general),按 general 处理。
  每章 intent 在 outline 已标注对 E / T / G 各意味着什么。
duration_min: 60
presentation_mode: handout
theme: template_training
output: /Users/pc2026/Documents/DevTools/iLovePPT/decks/claude-code-training/deck_v1.pptx

top_recommendation: |
  应当本季度让全员上手 Claude Code,把日常工作从"问 AI 答疑"升级为"让 AI 直接交付":
  工程师 100% 接入做日常开发、产品 / 设计 50% 做辅助生产、高层用 Deep Research 模式做调研;
  3 周完成全员 onboarding,并建立公司统一的 skill 库 + prompt 模板。

scqa:
  situation: 2026 年 AI 编程进入 agentic 阶段;Claude Code 6 月 $1B run-rate,SWE-bench 80.8%,46% Most Loved。
  complication: 公司可能停留在 "问 AI 答疑",缺统一 skill 库,非工程同事觉得 "工具与我无关"。
  question: 怎么让全员上手 Claude Code,把 agentic 能力变成公司级生产力?
  answer: 本季度全员上手 · 3 周 onboarding · 公司统一 skill 库。

footer_meta:
  classification: INTERNAL
  project: claude-code-training
  version: v1.0

based_on: deck_v1_outline.md

# === 特殊页编号说明(给 builder)===
# `## 0.` BLUF 页是 cover 之后、toc 之前的"答案前置 single_focus"页 —— N=0 表示不属任何章节。
# Schema 上 ## N. 的 N 是 chapter sequence number,N=0 = pre-chapter intro 页。
# Builder 解析时遇 N=0 应当作正常 single_focus content page(看 HTML 注释 layout)处理。
special_page_markers:
  bluf:
    h2_id: "0"
    layout: single_focus
    position: 2   # cover=1, BLUF=2, toc=3
    not_part_of_any_chapter: true
  scqa_c_明示:
    h2_id: "1.5"
    layout: cards
    position_after: "1.4"
    intent: "SCQA C(Complication)明示页 · 三类落差"

pending_data_pages:
  - "3.3"
  - "3.4"
  - "3.6"

reference_urls:
  - title: Claude Code 产品页
    url: https://www.anthropic.com/product/claude-code
  - title: $1B run-rate milestone(Anthropic Bun 收购公告)
    url: https://www.anthropic.com/news/anthropic-acquires-bun-as-claude-code-reaches-usd1b-milestone
  - title: SWE-bench 80.8% 对比(tech-insider)
    url: https://tech-insider.org/claude-code-vs-github-copilot-2026/
  - title: 开发者对比(SitePoint 2026)
    url: https://www.sitepoint.com/claude-code-vs-cursor-vs-copilot-the-2026-developer-comparison/
  - title: Anthropic × Accenture 合作
    url: https://www.anthropic.com/news/anthropic-accenture-partnership
  - title: Anthropic × Salesforce 扩展合作
    url: https://www.anthropic.com/news/salesforce-anthropic-expanded-partnership
  - title: Anthropic × Cognizant 合作
    url: https://www.anthropic.com/news/cognizant-partnership
  - title: Anthropic × PwC 扩展合作
    url: https://www.anthropic.com/news/pwc-expanded-partnership
  - title: Anthropic 团队怎么用 Claude Code(PDF)
    url: https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf
  - title: Extend Claude with Skills(官方)
    url: https://code.claude.com/docs/en/skills
  - title: Agent Teams 2026 Playbook(Developers Digest)
    url: https://www.developersdigest.tech/blog/claude-code-agent-teams-subagents-2026
  - title: Plugins Guide(Nimbalyst)
    url: https://nimbalyst.com/blog/claude-code-plugins-guide/
---

# Content

## [cover]
- title: 让全员上手 Claude Code
- subtitle: 从问 AI 答疑,升级到让 AI 直接交付
- prepared_by: 培训组(公司平台团队)
- date: 2026-05-24
- version: v1.0
- classification: INTERNAL

> 装饰建议:嵌 `_assets/template_template_training/image2.png`(商务握手深蓝调)

---

## 0. 本季度全员上手 · 3 周 onboarding
<!-- layout: single_focus -->
<!-- bluf_page: true · 在 cover 后 · 不属任何章节 · N=0 表示 pre-chapter intro -->

- big_text: 本季度全员上手
- big_number: 3 周
- explanation: 工程 100% · 产品设计 50% · 高层 Deep Research · 公司统一 skill 库

> 数据:Source: brief 顶端论点(本 deck top_recommendation,详见 brief.md)

---

## [toc]
- AI 编程已变 · 市场验证
- 7 大能力把它变可编程平台
- 工程 100% / 产品 50% / 高层
- Hybrid 是主流 · 互补不替代
- 3 周全员上手 · 建公司 skill 库

---

## [section_divider]
- num: 1
- title: AI 编程已变天
- sub_caption: |
    AI 编程已从"辅助补全"走入"端到端 agentic 阶段"。95% 开发者每周用 AI;Claude Code 6 月 $1B run-rate + SWE-bench 80.8% 拿下单工具第一。
    先看市场为什么已经变天,以及公司可能落在哪三类差距上。

---

## 1.1 95% 开发者每周用 AI,行业已变天
<!-- layout: single_focus -->

- big_text: 行业已变天
- big_number: 95%
- explanation: 开发者每周用 AI 辅助;84% 已用或计划用 AI 编程工具(2026 SitePoint 行业调研)。

> 数据:Source: SitePoint 2026 Developer Comparison — https://www.sitepoint.com/claude-code-vs-cursor-vs-copilot-the-2026-developer-comparison/

---

## 1.2 Claude Code 6 个月达 $1B run-rate · 单工具最快
<!-- layout: pic_text -->

![Claude Code 6 月 ARR 增长曲线 · 单工具历史最快](_assets/charts/1_2_run_rate.png)

- **6 月达 $1B**: GA 后 6 个月达成 $1B run-rate;Anthropic 史上最快单工具增长,与 Bun 收购公告联合宣布。
- **图例 hatched 即示意**: 仅 M6 为官方公开数据(深色实柱);M0-M5 为示意 estimated path(浅色斜纹)。
- **企业级速度**: $1B 主要由 Accenture / Salesforce / Cognizant / PwC 等大客户支撑,非 SMB 长尾;典型 SaaS 需 18-24 月。

> 数据:Source: Anthropic, Claude Code reaches $1B milestone (2026) — https://www.anthropic.com/news/anthropic-acquires-bun-as-claude-code-reaches-usd1b-milestone

---

## 1.3 SWE 80.8% + Most Loved 46% · 性能口碑双第一
<!-- layout: compare -->

- **性能榜首 (SWE-bench Verified)**: Claude Code 80.8%,Q1 2026 单一开发工具最高记录;同 SWE-bench 评测下,Cursor / Copilot 不公开同口径数据。技术领先非 marketing 话术。
- **口碑碾压 (Most Loved)**: Claude Code 46% / Cursor 19% / Copilot 9%;同时用过 CC + Copilot 的开发者中 61% 认为 CC 在复杂调试 / refactor 上更准。

> 数据:Source: tech-insider Q1 2026 — https://tech-insider.org/claude-code-vs-github-copilot-2026/  |  SitePoint 2026 — https://www.sitepoint.com/claude-code-vs-cursor-vs-copilot-the-2026-developer-comparison/

---

## 1.4 Accenture 数万 / Salesforce 全组织 · 大客户已下注
<!-- layout: cards -->

- **Accenture**: 数万开发者接入 Claude Code,Anthropic 史上最大单笔部署;成立 "Accenture Anthropic Business Group" 帮企业客户落地。
- **Salesforce**: 全球工程组织全面部署 Claude Code 增强开发者工作流;扩展合作覆盖工程团队 + 客户侧 AI 产品集成。
- **Cognizant**: Claude 可用于 35 万员工(不只工程),加速企业 AI 采纳 + 内部转型,典型 "agentic 普及型" 部署。
- **PwC**: 部署 Claude 同时支持技术建设(开发提效)+ 业务执行(咨询交付),覆盖 PwC 全球员工 GenAI 工作流。

> 数据:Source: Anthropic news ×4 —
> Accenture: https://www.anthropic.com/news/anthropic-accenture-partnership  |
> Salesforce: https://www.anthropic.com/news/salesforce-anthropic-expanded-partnership  |
> Cognizant: https://www.anthropic.com/news/cognizant-partnership  |
> PwC: https://www.anthropic.com/news/pwc-expanded-partnership

---

## 1.5 公司三类落差 · 为什么我们要现在动
<!-- layout: cards -->
<!-- scqa_c_page: true · SCQA C(Complication)明示页 · 加强 narrative tension -->

- **看不到 ROI(高层视角)**: 还把 AI 当 "工程团队工具",看不到给 executive 自己的 Deep Research 价值;投入决策因此推迟。
- **自学摸索(工程视角)**: 个人在用 Claude Code,无统一 skill / prompt 库,重复造轮子;高质 prompt 没沉淀,新人 onboard 慢。
- **用不来(产品 / 设计 / 高层)**: 觉得 "这是工程师工具与我无关",非工程同事零接触;agentic 能力被局限在 1/3 公司。

> 数据:Source: brief.md SCQA · Complication 三类落差(详见 brief.md 第 50-55 行)

---

## [section_divider]
- num: 2
- title: 7 力解构平台
- sub_caption: |
    市场已变 + 公司有三类落差,但 Claude Code 凭什么领跑?答案在"7 大能力"——它不是又一个 IDE 插件,而是可编程的 agentic 平台。
    CLAUDE.md → MCP 七层能力解构如下。

---

## 2.1 不是补全工具 · 是 agentic 编程系统
<!-- layout: compare_pk -->

- left:
    title: 问 AI 答疑(Copilot / ChatGPT 时代)
    body: |
      单文件视野 · inline 补全 · 一问一答;
      改完之后由开发者手动跑测试 / 迭代;
      模型不持久化项目上下文,每次会话重新理解。
- right:
    title: 让 AI 直接交付(CC agentic 时代)
    body: |
      读整个 codebase · 跨文件改 · 跑测试 · 根据失败自动迭代;
      修改文件 / 执行命令前显式申请权限,人审 + 人决定 ship;
      CLAUDE.md 持久化项目规约,所有会话基于同一 context。

> 数据:Source: Claude Code 产品页 — https://www.anthropic.com/product/claude-code

---

## 2.2 7 大能力总览:从 CLAUDE.md 到 MCP
<!-- layout: pic_text -->

![7 大能力 3 层放射图 · 基础 / 中层 / 扩展](_assets/charts/2_2_seven_abilities.png)

- **基础层**: CLAUDE.md(项目级记忆,启动即读)+ Skills(可重用工作流,/slash 触发);团队级 prompt 沉淀的起点。
- **中层协作**: Subagents(隔离 context 子智能体)+ Agent Teams(2026-02 新)+ Hooks(事件驱动确定性代码);多角色 / 多线协作。
- **扩展外联**: Plugins(打包分发)+ MCP(外部服务连接协议);跨工具 / 跨团队复用与外部系统集成。

> 数据:Source: 7 特性综合自 Towards AI / Anthropic Skills 官方 / Nimbalyst Plugins Guide — 详见 _assets/raw/claude-code-key-facts.md

---

## 2.3 Skills:可重用工作流 · 团队级沉淀的关键
<!-- layout: cards -->

- **是什么**: Skills 是教 Claude 重复工作流的 markdown 文件,通过 slash command 触发;200 字 prompt 写成 SKILL.md 一次,后续 /review-component 永远可用。
- **为什么重要**: Anthropic 已把 Skills 做成开放标准(Agent Skills);Claude Code 在标准之上加 invocation control / subagent execution / dynamic context injection。
- **怎么沉淀**: 个人项目 .claude/skills/ → 团队仓库 / 公司 monorepo;PR-based 贡献 + monthly review 治理(Ch 5.3 展开)。

> 数据:Source: Extend Claude with Skills(官方)— https://code.claude.com/docs/en/skills

---

## 2.4 Subagents + Agent Teams:多 agent 协作的新范式
<!-- layout: pic_text -->

![Subagents 主对话隔离 + Agent Teams 多 session 协作](_assets/charts/2_4_subagents_teams.png)

- **Subagents**: 独立 context window · verbose 在隔离区,summary 回主对话。内置 Explore / Plan / general-purpose 3 种,可自定义。
- **Agent Teams (2026-02 新)**: 多个独立 Claude session 互相协调 + 互发消息 + 并行分工;不是孤立 worker 向 boss 汇报,而是协作小队。
- **iLovePPT 自身**: 本培训 deck 流水线(brainstorm → author → critic → builder → designer → audience)即 Agent Teams 实例。

> 数据:Source: Developers Digest 2026 Playbook — https://www.developersdigest.tech/blog/claude-code-agent-teams-subagents-2026

---

## 2.5 Hooks + Plugins + MCP:确定性 + 分发 + 外部连接
<!-- layout: cards -->

- **Hooks(确定性)**: 事件驱动 shell 脚本,在 Claude Code 内某事发生时跑;不像 prompt 靠模型解释,hooks 跑确定性代码不 hallucinate;约 24 个 hook 点位可用。
- **Plugins(分发)**: 把 skills / agents / hooks / MCP / LSP / monitor 打包成可一键安装的单元;适合跨项目分享或团队内部分发,降低复制粘贴成本。
- **MCP(外部连接)**: Model Context Protocol 标准化连接协议,让 Claude 接 GitHub / Linear / Notion / 自定义内部系统;企业级 system of record 全面接入。

> 数据:Source: Nimbalyst Plugins Guide — https://nimbalyst.com/blog/claude-code-plugins-guide/  |  Towards AI Extensions Explained — _assets/raw/claude-code-sources.md

---

## 2.6 Anthropic 内部:消息项目从 1 周 → 2 个 30 分钟 call
<!-- layout: compare_pk -->

- left:
    title: 以前 — 1 周跨部门协调
    body: |
      GA 上线 messaging 这种复杂跨部门项目:
      产品写 PRD → 工程评估 → 设计 review → 法务审 → 多个 Slack / 会议来回拉齐;
      整个对齐周期约 1 周。
- right:
    title: 现在 — 2 个 30 分钟 call
    body: |
      Claude Code 读完所有上下文(PRD / 历史 ticket / 仓库结构)→ 生成同步草稿;
      团队只需 2 个 30 分钟 call 校对方向 + 决议关键问题;
      "ship production software in weeks, not quarters."

> 数据:Source: Anthropic 团队怎么用 Claude Code(PDF)— https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf

---

## [section_divider]
- num: 3
- title: 工程 100% / 产品 50%
- sub_caption: |
    能力清楚了,关键问题:我这个岗位能用吗?
    答:工程 100% 接入做日常开发 / 产品设计 50% 做辅助生产 / 高层用 Deep Research 做调研。三视角分层,无人旁观。

---

## 3.1 工程 100% / 产品设计 50% / 高层调研模式
<!-- layout: pic_text -->

![E/T/G 3 层金字塔 · 工程 100% / 产品 50% / 高层 Deep Research](_assets/charts/3_1_etg_pyramid.png)

- **工程层(底)**: 100% 接入做日常开发,目标 2-3× 提效;复杂调试 / 跨文件 refactor / 端到端 agentic 任务全部交给 CC。
- **产品 / 设计层(中)**: 50% 接入做辅助生产;PRD 起草 / 原型 mockup / 数据分析 / 用研梳理。
- **高层(顶)**: 用 Deep Research 模式做调研;行业调研 / 竞品分析 / 季度报告草稿,不必依赖下面层层汇报。

> 数据:Source: brief 顶端论点(本 deck top_recommendation,详见 brief.md)

---

## 3.2 工程师:任务边界 + prompt 模式 + 协作约定
<!-- layout: cards -->

- **任务边界**: 复杂调试 / 跨文件 refactor / 端到端 agentic 任务交给 Claude Code;单文件补全留给 IDE 插件(Copilot / Cursor 哪个更合适见 Ch 4)。
- **Prompt 模式**: Plan 模式先规划再执行 / 显式申请权限不全自动放权 / CLAUDE.md 写项目规约 / Skills 沉淀重复 3 次以上的 prompt。
- **协作约定**: PR 标 "claude-code-assisted" 标签 / 关键改动人审不省 / 敏感模块(支付 / 鉴权)禁全自动 / 复盘失败 prompt 进 skill 库。

> 数据:Source: brief 顶端论点 + _assets/raw/claude-code-key-facts.md "最佳实践 / 培训建议"

---

## 3.3 工程 Demo · Bug 修复 N× 提速 [待 W1 回填]
<!-- layout: compare_pk -->
<!-- pending_data: true -->

> ⚠ **pending_data: true**(此页 Stage D 跳过拓写,builder 将渲染为 TBD 占位 banner)
>
> **Placeholder body**:此处将填入 1-2 工程师跑 1 周 Claude Code 的真实 Bug 修复任务 before / after,含 prompt 原文 + 输出片段截图 + 耗时对比 + lesson learned 一句话。回填路径:Stage D 重派或主线程在 Stage E build 前 checkpoint 补 content.md。
> 回填后 action title 中 "N×" 替换为实测倍率(例:"3× 提速" 或 "5× 提速")。

- left:
    title: 试点前 · 手动 [TBD]
    body: "[待回填]"
- right:
    title: 试点后 · Claude Code [TBD]
    body: "[待回填]"

> 数据:Source: 待 W1 试点回填(1-2 工程师 · 真实 Bug 修复任务)

---

## 3.4 工程 Demo · Refactor M h → H min [待 W1 回填]
<!-- layout: compare_pk -->
<!-- pending_data: true -->

> ⚠ **pending_data: true**(此页 Stage D 跳过拓写,builder 将渲染为 TBD 占位 banner)
>
> **Placeholder body**:此处将填入 1 工程师跑 1 次跨 ≥5 文件 refactor 的真实 before / after,含 prompt 原文 + 输出片段 + 耗时对比 + 强调 "跨文件" 是 agentic 关键差异点(单文件 IDE 也能做,跨文件才显 CC 价值)。
> 回填后 action title 中 "M h → H min" 替换为实测数值(例:"8h → 45min" 或 "4h → 30min")。

- left:
    title: 试点前 · 手动跨文件 [TBD]
    body: "[待回填]"
- right:
    title: 试点后 · CC agentic [TBD]
    body: "[待回填]"

> 数据:Source: 待 W1 试点回填(1 工程师 · 跨 ≥5 文件 refactor)

---

## 3.5 产品 / 设计:50% 做辅助生产 · 文档 / 原型 / 数据
<!-- layout: cards -->

- **PRD 起草**: 给 CC 喂用户访谈纪要 + 历史 PRD 模板,生成结构化 v1 草稿;产品手改 30 分钟而非从零起 4 小时(示意,W2 试点验证)。
- **原型快速 mockup**: 描述交互流程 → CC 生成 HTML/Tailwind 静态原型;设计师在 v1 基础上调视觉,而非画 Figma 从空白页。
- **数据分析**: 给 CSV 直接让 CC 跑 pandas 分析 + 出 matplotlib 图;不必先建 Jupyter 环境,Deep Research 模式直接出趋势 + 异常 + 结论草稿。

> 数据:Source: 示意 [基于 Anthropic 团队 PDF 中跨岗位使用经验]— https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf

---

## 3.6 产品 Demo · 调研 K h → Y min [待 W2 回填]
<!-- layout: compare_pk -->
<!-- pending_data: true -->

> ⚠ **pending_data: true**(此页 Stage D 跳过拓写,builder 将渲染为 TBD 占位 banner)
>
> **Placeholder body**:此处将填入 1 产品跑 1 次竞品 / 行业调研报告的真实 before / after,含 Deep Research prompt 原文 + 输出结构 + 耗时对比 + 人工校证修正幅度(避免幻觉风险)。
> 回填后 action title 中 "K h → Y min" 替换为实测数值(例:"4h → 40min")。

- left:
    title: 试点前 · 手动整理 [TBD]
    body: "[待回填]"
- right:
    title: 试点后 · Deep Research [TBD]
    body: "[待回填]"

> 数据:Source: 待 W2 试点回填(1 产品 · 竞品 / 行业调研报告)

---

## 3.7 高层:Deep Research 做调研 · 季度报告草稿
<!-- layout: cards -->

- **行业调研**: 输入 "Q2 X 行业头部公司战略变化 + 最近 3 个月并购动态" → Deep Research 跑 10-30 分钟 → 出带 source 的结构化报告草稿。
- **竞争对手分析**: 输入竞品官网 + 财报 + media coverage → 输出 SWOT + 关键举措时间线 + 我方应对建议草稿;人工 30 分钟内 polish 即可发。
- **季度报告草稿**: 输入财务 / 业务关键数字 + 上季度对比 + 已知重大事件 → 输出叙述性季度报告 v1,高管手改而非起草。

> 数据:Source: Anthropic Deep Research 文档 + brief 顶端论点;实际 ROI 待高层 W3 试点回填

---

## [section_divider]
- num: 4
- title: Hybrid 是主流
- sub_caption: |
    分层用过之后,自然冒出疑问:那 Cursor / Copilot 怎么办?
    答案不是取代而是 hybrid 共存——平均开发者同时用 2.3 个工具(2026 survey)。本章给出推荐 stack。

---

## 4.1 三足鼎立:agentic / 编辑器 / 插件
<!-- layout: compare -->
<!-- recommended: item_1 -->

- **Claude Code(推荐)**: Agentic 编程系统;读整个 codebase + 跨文件多步执行 + 跑测试自动迭代;终端 + IDE + SDK;复杂任务首选。
- **Cursor**: AI-first 编辑器,把 IDE 重做;深度对话 + Composer 多文件改 + Tab 补全极快;适合愿意换编辑器的 power user。
- **GitHub Copilot**: IDE 插件,专注 inline 补全 + 对话;VSCode / JetBrains / Visual Studio 全覆盖;大企业生态 + 合规成熟。

> 数据:Source: _assets/raw/claude-code-comparison.md(综合 7 篇 2026 对比文章)

---

## 4.2 规模决定工具:小型 CC 75% · 大企 Copilot 56%
<!-- layout: matrix_2x2 -->

- x_axis:
    low: 公司规模(< 50 人)
    high: 公司规模(10000+)
- y_axis:
    low: 工具偏好(inline 补全为主)
    high: 工具偏好(agentic 多步为主)
- quadrants:
  - pos: tl
    title: 小型 + agentic 偏好
    body: Claude Code 75% / Cursor 42%;创业团队 power user 心头好。
    highlight: true
  - pos: tr
    title: 大企 + agentic 偏好
    body: 中型 50-1000 人混合;CC 在 power user 中渗透快,but 大企 procurement 慢。
  - pos: bl
    title: 小型 + inline 偏好
    body: 个人开发 / 独立 contributor 仍大量用 Copilot;Cursor 也在抢份额。
  - pos: br
    title: 大企 + inline 偏好
    body: GitHub Copilot 56%(微软采购关系 / SOC2 / volume discount)。

> 数据:Source: SitePoint 2026 采用率分层数据 — https://www.sitepoint.com/claude-code-vs-cursor-vs-copilot-the-2026-developer-comparison/

---

## 4.3 Hybrid Stack 推荐:Copilot 补全 + CC agentic
<!-- layout: cards -->
<!-- highlight: card_2 -->

- **Power user(Cursor + Claude Code)**: Cursor 做日常编辑(inline 补全快)+ Claude Code 做复杂 / 跨文件 agentic 任务;适合愿意换编辑器的工程师。
- **不换编辑器(Copilot + Claude Code · 本公司推荐 ★)**: VSCode + Copilot inline 补全 + 终端跑 Claude Code 处理 agentic 任务;多数同事场景适配最佳,迁移成本最低。
- **完全 agentic(Claude Code only)**: 终端 + CC 的 VSCode 扩展;适合习惯命令行 / 偏 agent 模式的人;首批工程师 power user 可试。

> 数据:Source: claude-code-comparison.md "Hybrid 是主流" 章节;2026 survey "经验丰富开发者平均同时用 2.3 个工具"

---

## [section_divider]
- num: 5
- title: 3 周全员上手
- sub_caption: |
    愿景到位 + 工具选好,最后落到节奏:本季度 3 周 onboarding(W1 工程 / W2 产品设计 / W3 高层)+ 公司 skill 库。
    5 节展开节奏 / 时间表 / 基础设施 / KPI / 行动清单。

---

## 5.1 3 周节奏:W1 工程 → W2 产品 → W3 高层
<!-- layout: bullet_list -->

- W1(工程):5 半天 · CLAUDE.md + Skills + 1 真实任务 · 接入率 ≥95%
- W2(产品 / 设计):4 半天 · Deep Research + PRD demo · 覆盖率 ≥80%
- W3(高层):2 半天 · 调研模式 + 季度报告 demo · ≥3 人完成 1 次 Deep Research

> 数据:Source: brief 顶端论点 + 3 周节奏自定(详见 brief.md "拓写偏好提示")

---

## 5.2 3 周时间表:W1 工程 → W2 产品设计 → W3 高层
<!-- layout: table -->

- title: 3 周时间表 + 关键里程碑
- headers:
  - Week
  - 半天
  - 对象
  - 主题
  - 负责人
  - 关键里程碑
- rows:
  - ["W1", "5", "工程", "CLAUDE.md + Skills + 真实任务", "工程 lead", "工程 ≥95% 接入"]
  - ["W2", "4", "产品 / 设计", "Deep Research + PRD demo", "产品 lead", "产品设计 ≥80% 接入"]
  - ["W3", "2", "高层", "调研模式 + 季度报告 demo", "高管 lead", "≥3 人 1 次 Deep Research"]
  - ["每周末", "1", "全员", "Retro + skill 沉淀", "平台团队", "沉淀 ≥3 个 skill / 周"]

> 数据:Source: brief 顶端论点;3 周节奏 + 里程碑自拟(critic R1 维度 2 已 absorb 自原 5.4)

---

## 5.3 公司 Skill 库:统一 prompt + 复用 · 避免重复摸索
<!-- layout: pic_text -->

![公司 Skill 库 · 目录结构 + 贡献流程](_assets/charts/5_3_skill_lib.png)

- **目录结构**: monorepo company-skills/.claude/skills/ 放 skill folder;每个 = SKILL.md + helpers(可选);slash 即 skill 名。
- **贡献流程**: 工程师写 SKILL.md → PR → Owner 评审 → 合并自动同步到全员 .claude/skills/ → Monthly review 治理。
- **治理 Owner**: 平台团队负责目录治理 + monthly review;贡献全员 PR-based;失败 prompt 也归档(作为 anti-pattern 参考)。

> 数据:Source: Anthropic Skills 开放标准 + brief 顶端论点 — https://code.claude.com/docs/en/skills

---

## 5.4 工程 ≥95% · 产品 ≥80% · skill 库 ≥10 个
<!-- layout: cards -->

- **工程接入率 ≥ 95%**: Q2 月底验收;计算口径 = 工程团队中至少 1 次提交标 "claude-code-assisted" 的 PR 的人占比;Owner = 工程团队 lead。
- **产品 / 设计覆盖率 ≥ 80%**: Q2 月底验收;计算口径 = 产品 / 设计团队中至少跑通 1 次 Deep Research 或 PRD demo 的人占比;Owner = 产品 / 设计团队 lead。
- **公司 skill 库 ≥ 10 个**: Q2 月底验收;计算口径 = company-skills 仓主分支入库 skill 数 ≥ 10 且至少 3 个不同贡献者;Owner = 平台团队。

> 数据:Source: brief 顶端论点 + KPI 自拟(critic R1 must-fix #3 + R2 low note "10 个 skill" 此页独占)

---

## 5.5 行动清单:今天就能做的 3 件事
<!-- layout: cards -->

- **工程师(全员)**: 今天 — 装 Claude Code(claude.com/code 下载);本周 — 跑通 1 个真实任务(用 Plan 模式先规划);本月 — 贡献 1 个 skill 到 company-skills 仓。
- **产品 / 设计**: 今天 — 装 Claude Code + 试 Deep Research 一次;本周 — 跑通 1 个 PRD 或原型 demo;本月 — 与工程合作沉淀 1 个跨岗位 skill(如 PRD 模板)。
- **高层**: 今天 — 让助理装 Claude Code 帮你跑一次行业摘要;本周 — 完成 1 次 Deep Research 调研;本月 — 在 1 次决策中引用 CC 产出的草稿数据。

> 数据:Source: brief 顶端论点 + 行动清单自拟

---

## [summary]
- 顶端论点回顾:本季度全员上手 Claude Code · 3 周 onboarding · 公司统一 skill 库
- 三视角承诺:工程 100% · 产品设计 50% · 高层 Deep Research · 3 周完成
- 落地节奏:W1 工程 → W2 产品 → W3 高层 · skill 库首批 ≥10 个
- 核心 ROI 锚点:80.8% SWE-bench · 46% Most Loved · Accenture 万人部署

---

## [closing]
- subtitle: 今天就装上 Claude Code,W1 见
- next_steps:
  - action: 工程师装 Claude Code · 跑通一个真实任务
    owner: 工程团队
    due: 本周
  - action: 产品 / 设计跑通 Deep Research demo
    owner: 产品 / 设计团队
    due: W2
  - action: 高层完成 1 次季度调研草稿生成
    owner: 高管团队
    due: W3
  - action: 公司 skill 库首批 ≥10 个 skill 沉淀
    owner: 平台团队
    due: Q2 月底

> 装饰建议:嵌 `_assets/template_template_training/image4.png`(QR 课程评价 / 反馈入口)

---

# 拓写记录 / Stage D audit

| 类型 | 计数 | 备注 |
|---|---|---|
| 总页数 | **36** | cover 1 + BLUF 1 + toc 1 + 5 dividers + 23 内容页(含新 1.5)+ 3 占位 + summary 1 + closing 1 |
| 正常拓写页 | 33 | 含 cover / BLUF / toc / 5 dividers / 23 内容(R2 新加 1.5)/ summary / closing |
| Pending data 页 | 3 | 3.3 / 3.4 / 3.6(builder 将渲染为 TBD 占位 banner) |
| 含图页 | 5 | 1.2 matplotlib(青绿 + R2 polish: hatched M0-M5 / solid M6)/ 2.2 / 2.4 / 3.1 / 5.3 drawio |
| 含 source 引文页 | 25 | 所有数据页 cite 完整 URL;占位页 cite "待试点回填" |
| handout 字数严守 | ✓ | cards body ≤ 80 / bullet ≤ 40 / summary ≤ 60 / table cell ≤ 25 / pic_text point ≤ 50 |
| template_training 调性 | ✓ | action title 全 ≤ 22 字 / divider title ≤ 8 / 数据图色 #409694 青绿 |

## R1(initial Stage D)low notes 处理记录

| critic R1 low | 处理 |
|---|---|
| Ch3 TBD action title 改 placeholder 结论形态 | 3.3 / 3.4 改 "[待 W1 试点数据回填]";3.6 改 "[待 W2 试点数据回填]" |
| Ch5.3/5.4 "10 个 skill" 数字让 Ch5.4 独占 | 5.3 内容 + 5.3 chart 双重去重;"≥10 个" 唯一保留在 5.4 |
| 5 divider sub_caption 升级为 2-3 句过渡桥句 | 5 个 section_divider 全部 sub_caption 写成 2-3 句桥句 |

## R2(critic Stage D R1)修订记录(本轮新增)

| critic R2 项 | 修改内容 | 实际改动位置 |
|---|---|---|
| **Must-fix M1**:2.4 Subagents body 字数 ~64 → ≤ 50 | 3 个 point 全部压缩:Subagents 47 字 / Agent Teams 43 字 / iLovePPT 45 字 | content.md 2.4 三个 point body |
| **Must-fix M2**:5.3 双 point ≤ 50 | 目录结构 47 字(去掉重复 path)/ 贡献流程 43 字(箭头链精简) | content.md 5.3 point 1+2 body |
| **Must-fix M3**:4.3 card 2 builder metadata 泄漏 | 删 body 内 "highlight: true(builder 若...)" 整段;以 HTML 注释 `<!-- highlight: card_2 -->` 替代;title 保留 "本公司推荐 ★" 用户可见标记 | content.md 4.3 + HTML 注释 |
| **Must-fix M3 扫描**:4.1 同类 metadata 泄漏 | 4.1 card 1 body 删 "— recommended: true";以 HTML 注释 `<!-- recommended: item_1 -->` 替代 | content.md 4.1 + HTML 注释 |
| **Recommended R1**:1.2 chart M0-M5 estimated 视觉 | 重画 matplotlib chart:M0-M5 用 alpha 0.55 + hatch "///";M6 用 solid 深蓝;新加 Legend 明示 estimated vs 公开;caption "仅 M6 为官方公开" | _assets/charts/1_2_run_rate.png 重渲染 |
| **Recommended R2**:SCQA C 加明示页 | 加 1.5 cards 3 卡 · 公司三类落差(看不到 ROI / 自学摸索 / 用不来);deck 35 → 36 页;Ch1 divider sub_caption 同步更新提及"三类落差" | content.md 新增 1.5 + Ch1 divider |
| **Recommended R3**:3.3/3.4/3.6 TBD title 升级数字占位 | 3.3 "Bug 修复 N× 提速"/ 3.4 "Refactor M h → H min" / 3.6 "调研 K h → Y min";placeholder body 加 "回填后替换为实测数值" 指引 | content.md 3.3 / 3.4 / 3.6 title + placeholder note |
| **Recommended R4**:BLUF "## 0." h2 marker | 加 HTML 注释 `<!-- bluf_page: true · 在 cover 后 · 不属任何章节 · N=0 表示 pre-chapter intro -->` + frontmatter `special_page_markers.bluf` 字段告 builder | content.md `## 0.` heading + frontmatter |
| **Recommended R5**:Ch3 篇幅 pending_data 联动不强动 | 无改动(按 critic 明示) | — |

## Pyramid 自检 ⑦ 字数补充(R2 新增 / 修改的 action title)

| 页 id | action title | 字数 |
|---|---|---|
| **1.5** | 公司三类落差 · 为什么我们要现在动 | 15.5(新增) |
| **3.3** | 工程 Demo · Bug 修复 N× 提速 [待 W1 回填] | 17.5(R3 升级) |
| **3.4** | 工程 Demo · Refactor M h → H min [待 W1 回填] | 19.5(R3 升级) |
| **3.6** | 产品 Demo · 调研 K h → Y min [待 W2 回填] | 17.5(R3 升级) |

全部 ≤ 22(template_training)/ ≤ 24(硬约束)。其他页 action title 未动,字数同 R2 outline ⑦ 自检表(详见 deck_v1_outline.md "# Pyramid 自检" 块)。
