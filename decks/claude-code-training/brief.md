---
deck_slug: claude-code-training
created: 2026-05-24
brainstorm_rounds: 3
---

# 顶端论点(top_recommendation)

**应当本季度让全员上手 Claude Code,把日常工作从"问 AI 答疑"升级为"让 AI 直接交付"—— 工程师 100% 接入做日常开发(目标 2-3× 提效)、产品 / 设计 50% 做辅助生产、高层用 Deep Research 模式做调研;3 周完成全员 onboarding,并建立公司统一的 skill 库 + prompt 模板,避免重复摸索。**

> 综合自用户选择的 a + b + c 三个候选(能力赋能 + 效率倍增 / 标准化 + 分层落地)。
> "3 周 onboarding"和"2-3× 提效"为**目标参考值**;若与公司实际情况差距过大,直接编辑此句。

短版(供 cover 使用,≤ 22 字):
> 让全员上手 Claude Code,从问答疑升级到让 AI 直接交付

---

# 必填字段

| 字段 | 值 |
|---|---|
| **audience** | `general`(全员混合) |
| audience_note | 用户选 a+b+c 三类全要 — author 拓写时**分层照顾三视角**:executive 看 ROI / technical 看实战 / general 看场景 |
| **duration_min** | 60 |
| **presentation_mode** | `handout`(阅读手册;信息密度 3-4×;讲者不在场也能读懂;预计 30-40 页) |
| **theme** | `template_training`(本地 `templates/template_training.pptx`,enriched yaml 已确认;主推 training / onboarding 场景;橙红 `#EF5938` + 深蓝 `#0B2A4A` + TEAM 四人扁平插画) |
| **output** | `/Users/pc2026/Documents/DevTools/iLovePPT/decks/claude-code-training/deck_v1.pptx` |

---

# 素材清单

由 brainstorm WebSearch(2026-05-24)收集,已落地 `_assets/raw/`:

| 文件 | 内容 | 给 author 的用途 |
|---|---|---|
| `_assets/raw/claude-code-sources.md` | 30+ URL 索引(官方 docs / Anthropic news / 企业案例 / 行业对比 / 教学),分类清晰 | 拓写时直接 cite + 后续可深读 |
| `_assets/raw/claude-code-key-facts.md` | 关键事实清单:positioning、市场数据($1B run-rate / SWE-bench 80.8% / 46% most loved)、企业案例(Accenture / Salesforce / Cognizant / PwC)、7 大特性(CLAUDE.md / Skills / Subagents / Agent Teams / Hooks / Plugins / MCP)、Anthropic 内部 PDF 链接 | 数据 / 案例 / 特性页直接引用 |
| `_assets/raw/claude-code-comparison.md` | Claude Code vs Cursor vs GitHub Copilot 完整对比(性能 + 采用率分层 + hybrid stack 建议) | "工具对比 + hybrid 推荐"页 |

⚠️ **重要**:用户**没有公司内部素材** —— 所有数据都来自公开来源。author 拓写时**凡引用具体数字 / 案例,在对应位置须 cite 来源链接**(可放页脚或"参考"页)。若未来用户给到公司内部试点数据,需回 brief 替换公开数据。

---

# SCQA 线索(brainstorm 推断,author 拓写 cover / 开场页用)

- **Situation**:2026 年,AI 编程进入 "agentic" 阶段;95% 开发者每周用 AI 辅助,84% 已用 / 计划用 AI 编程工具;市场上 Claude Code / Cursor / Copilot 三足鼎立但定位差异显著;Anthropic Claude Code GA 6 个月达 $1B run-rate,SWE-bench Verified 80.8%(单工具最高),开发者 46% "most loved" 排第一,Accenture 数万开发者已部署。
- **Complication**:公司内可能存在三类落差:
  - (a) 还停留在 "问 AI 答疑"(ChatGPT / Copilot 时代),没用上 "让 AI 直接交付" 的 agentic 能力;
  - (b) 各人摸索,没有公司级 skill / prompt 库,重复造轮子;
  - (c) 不同岗位(工程 / 产品 / 设计 / 高层)缺乏分层使用方法,导致非工程同事觉得 "这是工程师工具与我无关"。
- **Question**(隐含):怎么让全员上手 Claude Code,把 agentic 能力变成公司级生产力?
- **Answer**:同顶端论点。

---

# 拓写偏好提示(给 author)

1. **三视角分层叙事**:每个主要章节明确 "对 executive 意味着 X,对 technical 意味着 Y,对 general 意味着 Z"。可考虑做成 cards-3 layout 反复出现作为视觉骨架。

2. **数据点必 cite**:所有引用的数字 / 案例,在素材里都有原始来源 URL,page 注脚或末尾 "参考" 页要列。

3. **实战 demo 是培训 deck 的核心**:60min handout,不能全是 talking head。建议至少 **5-8 页**是具体场景的 before / after(prompt + 输出截图 / 终端命令)。无素材就编合理 demo + 标 "示意"。

4. **章节切分建议**(参考,author 可改):
   - Part 1 · Why now(市场 + 数据,~5 页)
   - Part 2 · What is Claude Code(7 大特性,~8 页)
   - Part 3 · 怎么用(分 E/T/G 三段实战,~12 页)
   - Part 4 · 工具对比 + hybrid 推荐(~4 页)
   - Part 5 · 落地方案 + 3 周 onboarding 计划(~5 页)
   - Part 6 · Q&A / 行动清单(~3 页)
   - **总计 ~37 页**,在 handout 模式 30-40 页区间内

5. **template_training 调性约束**(从 yaml 摘):
   - 标题字号 28pt,严守 **≤ 22 字**,长 action title 易换行
   - 数据图用 **青绿 #409694**,不要用红色(跟 accent 橙红冲突)
   - section_divider 章节号橙红色块视觉权重大,**标题 ≤ 8 字**
   - cover 后第 1 页可嵌商务握手图(`_assets/template_template_training/image2.png`,深蓝调,适合 "团队启动 / 共识达成")
   - cards body **≤ 16 字**(template_training 比 tech_blue 略严)

6. **handout 模式字数**:严格按 author SKILL 的 handout 限制(cards body ≤ 80 字、bullets 正文整句、信息密度 3-4× speaker),否则 critic 必打回。
