# iLovePPT Pipeline Protocol

> **Location**: `.claude/pipeline-protocol.md`(AI 运行时协议,跟 `.claude/agents/*.md` 同性质)
> **Version**: v0.5.1(2026-05-24)
> **Scope**: 主线程派发逻辑 + agent 之间的 handoff + 各 gate 规则
> **Audience**: Claude 主线程(派发时反复 reference) + 各 agent 文件(行为契约)

本文档是 iLovePPT 流水线**当前运行时协议**的权威定义。当主线程 / agent 文件有歧义时,以本文档为准。

**跟 `docs/superpowers/specs/` 的区别**:那里是设计 rationale 史档(给人看,为什么这么做);这里是活协议(给 AI 看,**现在**怎么做)。版本演进时本文档原地更新,设计史归档到 specs/。

`CLAUDE.md` 是导航文件,核心架构原则在那里;本文档是细则。

---

## 概览

```
brainstorm → author → content-review → builder → audience
   ↑                       ↑                        ↓
   └─ extractor 旁路 ─┘    └── 5 轮 cap        9 分 cap
                            (4 选 1)         (5 轮后 4 选 1)
```

5 个 agent + 1 旁路:

| agent | 角色 | 何时派 |
|---|---|---|
| `iloveppt-brainstorm` | Stage A-B 收 brief + 素材 | 用户首次说"做 PPT" |
| `iloveppt-author` | Stage C-D 出 outline + content | brainstorm 收齐后 |
| `iloveppt-content-review` | 第三方审计:brief→content 对齐 + 金字塔结构(14 项) | author 出 content.md 用户批准后,build 前强制 gate |
| `iloveppt`(builder) | Stage E 构建 .pptx + 视觉 QA 循环 | content-review pass 后 |
| `iloveppt-audience` | 模拟受众读 deck 给评分 | builder 出 .pptx 后强制跑;评分 < 9 反馈给 author |
| `iloveppt-template-extractor` | 旁路 · 提取 .pptx 模板 4 级 token | 用户给新 .pptx 模板时 |

agent 设计的源 rationale:`docs/superpowers/specs/2026-05-23-iloveppt-agent-design.md`。

---

## 1. PPT 意图触发规则(强制)

**主线程 Claude 一旦判断用户有制作 PPT 的意图,必须先建 team 再派 agent,不允许在主进程里串行调用 agent**。

1. **建 team**:用 `TeamCreate` 创建一个 agent team,team 名建议 `iloveppt-<deck-slug>`(例:`iloveppt-claude-training`)。
2. **每个 teammate 独立窗口**:5 个 agent 按需各占一格,通过 `SendMessage` 跨窗口传递交付物路径(`brief.md` / `outline.md` / `content.md` / `deck_plan.json` / `.pptx`)。
3. **主线程退居协调**:只负责派单 + 在窗口间转发消息,不直接执行任何 stage 内的逻辑(不写 brief、不写 content、不做视觉 QA)。

**触发信号**(任一命中即触发):
- 关键词:做 PPT / 帮我写 deck / 提案 / 路演 / 幻灯片 / slides / 汇报材料
- 用户给了 `.pptx` 模板路径或要求"按这个模板出"
- 工作目录里已有 `brief.md` / `outline.md` / `content.md` 且用户要求继续推进

**例外**:用户明确说"不用 team / 你自己来 / 不开窗口"时尊重决定,但仍按下方派发表行事。

**触发后的启动序列**(主线程一气呵成,不要中间等用户):

1. **derive slug** — 从 `initial_request` 取关键短语 slugify(例:"做个 Claude Code 培训" → `claude-code-training`)。这只是命名,brainstorm 后续可提议改。若 `decks/<slug>/` 已存在,追加 `-2` 后缀。
2. **derive working_dir** — `<iLovePPT-root>/decks/<slug>/`。主线程负责 `mkdir`。
3. **TeamCreate** — `team_name: "iloveppt-<slug>"`。
4. **SendMessage 给 brainstorm**(首条消息只带三字段,不扩展):

   ```yaml
   working_dir: /abs/path/to/<iLovePPT-root>/decks/<slug>/
   iloveppt_root: /abs/path/to/<iLovePPT-root>/
   initial_request: |
     <用户原话逐字粘贴,含可能附带的文件路径>
   ```

   不传 `attached_files` / `user_profile_hints` / `previous_decks` 等扩展项 —— brainstorm 自己从 initial_request 解析、自己 Glob 找已有 deck/template。

---

## 2. brainstorm 内部循环协议

**续轮派发载荷** — 主线程 SendMessage 给 brainstorm 续轮时,只传最小集:

```yaml
working_dir: /abs/path
user_response: "<用户对上轮问题的答,逐字>"
```

不传 `iloveppt_root`、不传历史问题 —— brainstorm 自己从 `.iloveppt_dialog_state.json` 捞。state file 是 SSOT,主线程不复述。

**ask_user 转发协议** — brainstorm 返回 `next_action: ask_user` 时,主线程把 `message_to_user` + `questions` **原文**贴给用户(brainstorm 的口吻直通,不用 `AskUserQuestion` 包装成结构化多选)。原因:brainstorm 是有性格的对话方,主线程只做透明转发。

**软上限兜底** — `.iloveppt_dialog_state.json` 里维护 `round` 字段(brainstorm 每轮 +1)。主线程在 `round >= 10` 时,转发 brainstorm 问题前**附加一行**给用户:

> "我们已经聊到第 10 轮还没收齐字段。要继续答,还是直接让 author 用当前已知信息开工(缺的字段走默认值)?"

用户选叫停 → 主线程 SendMessage 给 brainstorm `{force_dispatch: true}`,brainstorm 用 state 里已有字段 + 默认值组装 brief,直接 `dispatch_author`。

---

## 3. brainstorm 收齐字段后的总结 + 确认 gate

brainstorm 在返回 `dispatch_author` **之前**必须**串行两步**(不允许并行、不允许跳过):

**Step 1(先)**:`Write` `<working_dir>/brief.md` —— 把结构化 brief + asset_inventory 序列化成人话(schema 见下方)。**等文件落盘成功后**再进 Step 2。

**Step 2(后)**:返回一次 `ask_user` 做最终确认 —— `message_to_user` 含 brief 节选(top_recommendation + 6 必填字段 + 素材数 + brief.md 路径),让用户"在 brief.md 直接编辑 或 回复 OK"。

收到用户 `OK` / `批准 brief` 类回复后,brainstorm 下一次派发才返回 `dispatch_author`。若用户在 brief.md 里直接改了文件,brainstorm 该轮 Read brief.md 重新加载 collected,再问"按改后版本批准?"。

**为什么需要这道 gate**:author 是流水线第一个昂贵动作(出图 + 大段拓写)。若 brief 有理解偏差,这里改的代价最低。增量复述是字段粒度;这道 gate 是组合粒度,catches "字段单独对、组合起来论点不成立"的情况。也是 v0.4.0 "主线程脑补 24 页 content"反例的预防 —— 有 brief.md,后续任何越权动作都能 diff 出来。

**brief.md schema**:

```markdown
---
deck_slug: claude-code-training
created: 2026-05-24
---

# 顶端论点
<top_recommendation 完整句>

# 必填字段
- audience: technical
- duration_min: 15
- theme: tech_blue
- output: <working_dir>/deck_v1.pptx
- presentation_mode: speaker

# 素材清单
- csv: _assets/raw/q4.csv — Q4 营收数据
- image: _assets/refs/arch.png — 现有架构图

# SCQA 线索(brainstorm 推断,author 拓写 cover 时用)
- Situation: ...
- Complication: ...
- Question: ...(隐含)
- Answer: 同顶端论点
```

---

## 4. brainstorm → author handoff

**brainstorm 窗口命运** — 收到 `dispatch_author` 后,主线程**关闭** brainstorm 窗口(不保留 idle)。`.iloveppt_dialog_state.json` 是 SSOT,需要召回时重开窗口 + Read state 即可。

**主线程不做 brief 完整性校验** — brainstorm 自己 Step 2 已检查必填字段。若 brainstorm 返回不完整 brief,那是 brainstorm bug,在 brainstorm 修而不是主线程兜底。

**handoff 消息原文转发** — 主线程拿到 brainstorm 的 `dispatch.args`(`{working_dir, stage:C, brief, asset_inventory}`)整块 SendMessage 给 author。主线程当邮局,不当海关。

**author 不读 brainstorm 的 state file** — `.iloveppt_dialog_state.json` 是 brainstorm 的内部记忆,不是 handoff 接口。author 只信入参里的 brief / asset_inventory,避免两个 agent 隐式耦合。

---

## 5. author Stage C → D 内部协议

**Stage 间硬隔离** — author 收到"批准 outline"后,不在同一次派发里继续拓 content。标 `approvals.outline=true` → 返回主线程 → **主线程再派一次** author(stage=D)才开始 Stage D。原因:Stage D 出图 + 拓 content 是分钟级动作,每个昂贵动作独立派发,主线程可见性 + 用户可中途叫停。

**md 文件是 SSOT,state 只记 approval** — author 不维护 md 的 hash/mtime。每次派发都 Read `deck_v{N}_outline.md` / `deck_v{N}_content.md` 当唯一真相源。`.iloveppt_author_state.json` 只记 `{stage, outline_md_path, content_md_path, approvals: {outline: bool, content: bool}, iteration: N, pyramid_known_issues: [...]}`。用户在 md 里直接改了 → 下次派发 Read md 自然加载新内容,询问"批准当前版本?"。

**版本号迭代:author 判断 + 询问** — author 收到改动指令时:
- 改动小(改 page X / 改某段措辞)→ 就地 Edit,版本号不动
- 改动大(章节重组 / 论点重写 / 节奏推翻)→ author 主动问"这是大改,要在 v{N} 上 Edit 还是开 v{N+1} 平行版本?"
- 用户明确说"开 v2 / 重做" → 直接 +1,Write 新文件

判断"大改"的启发式:涉及顶端论点变更 / 章节增删 / 超过 3 个 page 的连锁改动。

**Stage C outline.md frontmatter 默认填 footer_meta** — author 出 outline 时默认写入(classification=`INTERNAL` / project=`<deck_slug>` / version=`v1.0`),用户可在审 outline 时改。这避免 brainstorm 多问 3 个低优先级字段;若 author 漏填,builder 透传无值不画 footer(双保险)。

**Pyramid 自检软阻塞 + audit** — 7 项有任一不过时:
- `Write outline.md` 时末尾 checkbox 标 unchecked
- 返回 `ask_user`,message 列明哪几项不过 + 原因,**强制用户二选一**:
  - "豁免第 X 项,理由:..." → 主线程把理由 SendMessage 回 author,author 写入 `state.pyramid_known_issues: [{item: 3, reason: "数据下周才有", approved_at: ...}]`,允许进 Stage D
  - "改第 X 项" → author 收用户指令 Edit outline 重新自检
- **不允许**用户回"先放着" / "不管它"含糊过关 —— 必须显式豁免 + 理由,留 audit 痕迹

---

## 6. author → builder handoff

**author 窗口保留到 builder Step 0 通过才能关** — author 的工作真正完成的标志,不是"用户批准 content",而是 **builder 跑过 Step 0 Pyramid 自检拿到内容层绿灯**。Step 0 若失败,author 窗口立即被召回,直接 Read state file + content.md 续接修改。Step 0 通过后主线程关闭 author 窗口。

**content.md 不被 builder 改 —— builder 写副本** — builder Step 3.4 的 `auto_md_edits` 不允许写回原文 `deck_v{N}_content.md`,而是写副本 `deck_v{N}_content.postbuild.md`:
- 原文 = 用户批准的最后版本(SSOT,不可变)
- 副本 = builder 自动调整后的实际构建版本(`deck_plan.json` 从副本生成)
- builder 返回主线程时附 `auto_md_edits[]` diff,主线程把"builder 自动调整了这些"展示给用户
- 用户决定:接受副本 → 后续 author 改动以副本为基础;拒绝 → 保留原文,author 后续按用户指令重改
- author 被召回时只 Read 原文 `deck_v{N}_content.md`,不读副本(避免污染)

**builder 入参 `footer_meta` 哪来** — author 在 Stage C `outline.md` frontmatter 里默认填(见上节)→ Stage D 拓写时透传到 `content.md` frontmatter → builder 从 content.md frontmatter 读取。author dispatch_builder 时不重复传 footer_meta,builder 自己 Read content.md 拿。

**builder hard stop 回主线程的处理** — builder Step 0 Pyramid fail 或反向 diff fail 返回 `error: ...` 时,主线程**不自动重派 author**,而是把错误展示给用户,**三选一**:
- "按 builder 的 suggestion 自动改" → 主线程 SendMessage 给 author,把 `failed_items + evidence + suggestion` 当 user_response 传入,author 按 suggestion Edit
- "我来指定怎么改" → 主线程接用户的指令,转发给 author
- "终止" → 主线程关 team,保留 working_dir 现状供后续手动处理

不允许"主线程自动按 suggestion 改"—— builder 的 suggestion 是机械建议(例如"合并章节 2 和 3"),用户可能不同意。

---

## 7. content-review 强制 gate(v0.5.1 新增)

`iloveppt-content-review` 是第三方独立审计员,填的是"**author 自检之外、第三方裁判**"的空位。

**位置**:author Stage D content 用户批准后 → **强制 gate** → dispatch_builder

```
author 出 content.md 用户批准
  ↓
主线程派 iloveppt-content-review
  ↓
content-review 跑 14 项检查 → 写 content_review_report.md + verdict
  ├── verdict: pass → 主线程派 builder
  └── verdict: needs_revision → 主线程展示 report → 用户 cherry-pick
        → 派 author(stage=C 或 D,取决于改动深度)
        → 改完重派 content-review(第 2 轮)
        → 5 轮上限 → 主线程问用户四选一(见下)
```

**入参**:
```yaml
working_dir: /abs/path
brief_md_path: <working_dir>/brief.md
outline_md_path: <working_dir>/deck_v{N}_outline.md
content_md_path: <working_dir>/deck_v{N}_content.md
asset_inventory: [...]   # 主线程从 brainstorm dispatch 时透传
```

**14 项检查分两个 section,每项必须收集 evidence**(verification-before-completion):

**Section A · 金字塔结构审计(7 项)**:
- A1 单一顶端论点(动+宾+边界)
- A2 SCQA 完整(answer == top_recommendation)
- A3 答案在前(BLUF,顶端论点 cover/第1内容页出现)
- A4 MECE 3-5 章节(两两不重叠)
- A5 纵向疑问链(action title 串读)
- A6 横向逻辑同类(章节并列同型论据)
- A7 action title ≤ 24 字

**Section B · brief → content 对齐(7 项)**:
- B1 top_recommendation 字面一致(允许压缩缩短)
- B2 SCQA 4 字段在 content 都有承接(定位页号)
- B3 audience tone 匹配 brief(抽 3 页验语气)
- B4 asset_inventory 每项有交代(`used_in_page: 5` / `intentionally_unused: 理由`)
- B5 无 brief 外新事实(反向 grep)
- B6 duration × 1.5 ≈ 总页数(±3)
- B7 presentation_mode 字数遵守(抽 5 页实测)

**3 层 Pyramid 防线(质量优先,接受冗余)**:

| 层 | 何时 | 阻塞性 | 角色 |
|---|---|---|---|
| author Stage C 自检 | Stage C 出 outline 时 | **软阻塞**(可豁免附理由) | 起草时早 catch |
| **content-review(新)** | Stage D 批准后,build 前 | **强阻塞**(5 轮 cap) | **第三方独立审计 + brief 对齐** |
| builder Step 0 | 构建前 | **硬阻塞**(hard stop) | 进 mechanical build 前最后保险 |

3 层各跑 Pyramid 看似冗余,但角色清晰:author 自检不够独立、builder Step 0 不查 brief 对齐 —— 缺哪一层都有盲区。Pyramid 单次跑 ≈ 30s,3 层 ≈ 90s,买质量底线值得。

**用户 cherry-pick 失败处理(跟 audience 一致)** — content-review fail 时主线程不直接派 author。流程:
1. 主线程展示 `content_review_report.md` 路径 + verdict + 失败项摘要
2. 用户 cherry-pick:"接受 A3 / B5 的指出,A6 我觉得不是问题"
3. 用户筛过的部分作为 `user_response` 自然语言指令派给 author

不允许"content-review 直接命令 author"的强耦合。

**5 轮上限 + 反复改不收敛时给用户四选一**:

```
第 5 轮 content-review 仍 fail → 主线程问用户:
  1) 继续改(计数器重置,新 5 轮)
  2) 接受当前版本(标 quality_grade: B,绕过 gate 进 builder)
  3) 终止保留中间态
  4) 回 brainstorm 改 brief(很可能 brief 本身有歧义,例如 audience 标 sales 但 top_recommendation 是技术语言)
```

选 4) 时主线程把当前 content_review_report.md 路径作为 `[system] content_review_blocked` 标记 SendMessage 给 brainstorm,brainstorm 重开窗口、Read state + report 后跟用户对话调 brief。

**content-review 窗口每轮新建**(跟 audience 一致) — 无状态,所有 state 在 content_review_report.md。

**builder Step 0 必须 Read content-review 报告确认 pass** — builder 启动时第一动作不是跑自己的 Pyramid,而是 Read `<working_dir>/content_review_report.md`:
- 文件不存在 → 拒绝构建,return error `content_review_missing`
- 存在但 verdict ≠ pass → 拒绝构建,return error `content_review_not_passed`
- verdict == pass → 继续 builder Step 0 自跑 Pyramid(3 层防线的第 3 层)

---

## 8. builder 内部 + 视觉 QA 定位

**两套视觉 QA 定位严格分离 —— 不允许功能重叠**:

| 维度 | builder Step 3 | audience(独立 agent) |
|---|---|---|
| 视角 | 作者视角(自检) | 读者视角(他检) |
| 关注 | **机械缺陷**:字号失衡 / 对齐错位 / 文字溢出 / 颜色违规 / layout 异常 | **认知接收**:论点清晰度 / 节奏感 / 记忆点 / 哪页让我走神 / 看完能记住几个论点 |
| 自动修 | 是(决策 8a 边界内) | 否(回 author 大改) |
| 输出 | issues + auto_md_edits + review_needed | rubric 评分 + 走神点列表 + author 反馈清单 |
| Checklist | visual-qa.md 17 项(机械)+ rubric.md D1-D14(机械维) | audience 自定义 4 维评分(comprehension_5s / info_density / visual_appeal / flow_coherence) |

builder Step 3 不允许评"这页论点不清"(那是 audience 的),audience 不允许标"字号 14 偏小"(那是 builder 的)。

**Pyramid 自检 builder 独立跑,但读 author 豁免状态** — builder Step 0 独立跑 7 项自检(基于当前 md 文件状态,含用户手改后版本),不信任 author 的自检结果(author 可能漏标 / 用户后续手改了 md)。但 builder Read author state(`.iloveppt_author_state.json`)拿 `pyramid_known_issues`,若 builder 检出 fail 的项恰好是 author 已豁免的,错误信息加注:

```yaml
error: pyramid_check_failed
failed_items: [4]
evidence:
  item_4: "章节 2 与章节 3 评审范围重叠"
note: "author 已豁免此项(理由:数据下周才有)。builder 仍判定 fail,需用户最终决定:接受 author 豁免 跳过 / 改 md / 终止"
```

这是 **builder 唯一允许 Read author state 的场景**(handoff 隔离的例外)。

**`deck_plan.json` 持久化 + commit-worthy** — builder 生成 `<working_dir>/deck_plan.json` 到工作目录,**不视为 ephemeral**。用户可绕过 author 直接手改 deck_plan.json 跑 `build.py` 重新出 .pptx(适用 mechanical tweak 场景,如调字号 / 微调位置)。这跟"the seam is deck_plan.json"的设计一致。

**`*_render/` 同目录 build 时覆盖** — `<working_dir>/<deck_name>_render/page-*.jpg` 每次 build 覆盖。不做版本化、不做自动清理。audience 后续 Read 这些 PNG,清理早会断流;清理交由用户手动处理。

---

## 9. builder → audience handoff + 反馈环

**串行 + 9 分硬阈值** — builder 完成后不直接把 .pptx 给用户,**必须先派 audience 评审**。audience `overall_score < 9` 一律不交付,自动进入修复环,**直到拿到 ≥ 9 才允许交付**。理由:audience < 9 的 deck 给用户也用不出去,白送有缺陷版本损害体验。9 分门槛比"7 合格"更进取 —— audience 在 anti-prompt 里被要求"敢打低分",9 分代表"真正打磨过"。

**author rewrite 先,theme fix 后** — audience 同时返回 `needs_author_rewrite` + `needs_theme_fix` 时:
- 主线程**先**派 author 改 content → author 完 → 主线程再改 themes(若有 `needs_theme_fix`)→ 重派 builder
- 不允许 theme fix 先(author 改完 content 又得 rebuild 一次,白跑一轮)
- 不允许 theme + content 并行(同一份 content.md 上 theme/content 改动可能耦合,例如 audience 说 page 8 "section_divider 数字背景缺",这既是 theme 也是 content 的事,要 author 先判定哪一层的事)

**用户 cherry-pick audience 建议** — audience 返回 review.md 后,主线程**不**直接把 top_3_must_fix 转发给 author。流程:
1. 主线程把 `audience_review.md` 路径 + `overall_score` + `top_3_must_fix` 摘要展示给用户
2. 用户 cherry-pick:"接受 page 5/13 的建议,page 8 我不改" / "全接受" / "全否决,直接交付当前版本"
3. 主线程把**用户筛过**的部分作为 `user_response` 字符串(自然语言指令)派给 author

不允许"audience 命令 author"的强耦合 —— audience 的反馈是给"作者 + 用户"两方看的建议,**用户是最终决策者**。

**5 轮上限 + 用户决定续命** — `audience → author → builder → audience` 这个循环上限 5 轮(主线程在 team 元数据里维护 `audience_round` 计数器)。第 5 轮 audience 仍 < 9 时,主线程**不自动继续**,问用户:

> "已迭代 5 轮,audience 评分 8.4,top remaining issues: ...。继续改 / 接受当前版本 / 终止保留中间态?"

用户选"继续改" → 计数器重置,新一轮 5 轮开始。

**audience 窗口每轮新建** — audience 评一次出一份 `audience_review.md`,无状态(state 全在 review.md 里)。主线程每轮新派 audience 窗口、评完关、下轮新建。不保留 idle、不复用窗口。

---

## 10. template-extractor 旁路衔接

extractor 是嵌套 handoff:`brainstorm → extractor → brainstorm`。

**主线程当邮局,中转两跳** — agent 不允许嵌套派 agent。链路:

```
brainstorm 检测到新模板 → return { next_action: dispatch_template_extractor, dispatch.args: { working_dir, template_path } }
  ↓
主线程派 extractor(SendMessage 给 extractor 窗口,载荷 = dispatch.args 原文)
  ↓
extractor 一次性跑完,return { next_action: dispatch_brainstorm, dispatch.args: { working_dir, user_response: "模板已摄入..." }, template_ready: bool }
  ↓
主线程 SendMessage 回 brainstorm(载荷 = dispatch.args)
```

跟其他 handoff 一致(主线程不当海关,只当邮局)。

**brainstorm 窗口在 extractor 跑期间保留 idle**(handoff 通则的例外) — extractor 耗时 1-3 分钟(probe 渲染 + 8 张 PNG 视觉分析),且 extractor 完后立刻要回 brainstorm 续接,关闭再重开 brainstorm 是无谓开销。所以这是**唯一允许 brainstorm 保留 idle 的场景**。其他 handoff(dispatch_author)brainstorm 仍然关闭。

**extractor 窗口** — 一次性任务,跑完关闭,不保留。

**extractor 失败由 brainstorm 跟用户对话** — extractor 返回 `template_ready: false`(soffice 没装 / probe 失败 / 模板格式异常)时,主线程**不**自动降级、**不**自己问用户。而是 SendMessage 给 brainstorm:

```yaml
working_dir: <working_dir>
user_response: |
  [system] template_extractor_failed
  reason: <extractor 返回的 reason>
  yaml_partial_path: <若已写部分 yaml,给路径>
```

brainstorm 收到这种带 `[system]` 前缀的特殊 user_response,自动转换成跟用户的对话:

> "刚才模板摄入失败了,原因是 X(例:soffice 没装)。三选一:1)装好依赖重试 2)降级用 tech_blue 默认模板 3)终止本次任务"

理由:brainstorm 是跟用户对话的 agent,问最自然;主线程直接问会断层。

---

## 11. 整体退出 + 交付物

**正常退出 = 质量底线 + 用户最终确认(双闸门)**:

```
audience ≥ 9 + Pyramid pass + 无 architectural blocker
  ↓
主线程展示给用户:.pptx + audience_review.md 摘要 + 改动 audit
  ↓
用户答 "OK 交付" / "我还想再改 page X"
  ↓ (OK 才结束)
交付完成,主线程关 team
```

第一道闸门(质量)是硬规则,audience < 9 强制进修复环;第二道闸门(用户确认)是软规则,用户始终是 ship 的最终决策者。即使 audience 给 9.5,用户也可以说"再调调",回 author。

**交付物 = 标准集**(主线程展示给用户的清单):

```
主交付:
  deck_v{N}.pptx                            ← 给客户/听众用的就是这一份

辅料(供用户复盘 / 后续手改):
  audience_review.md                         ← 最后一轮 audience 报告
  brief.md                                   ← 起始 brief
  deck_v{N}_outline.md                       ← 章节骨架
  deck_v{N}_content.md                       ← 用户批准版(SSOT)
  deck_v{N}_content.postbuild.md             ← builder 自动调整版
  deck_plan.json                             ← mechanical seam,可手改重 build
  _assets/charts/                            ← 出图 PNG
  <deck_name>_render/                        ← 视觉 QA 用的逐页 PNG
  STATUS.md                                  ← 主线程写的交付摘要(见下)
  .iloveppt_*_state.json                    ← 各 agent state(回看用)
```

working_dir 不打包、不删 —— 留在 `<iLovePPT-root>/decks/<slug>/` 原地。主线程在最终给用户的消息里**列路径清单 + 一句话用途**,不要把所有文件内容贴出来。

**`STATUS.md` 主线程在每次退出(正常 / 叫停 / 失败)时写**:

```markdown
# Deck status · <slug>
status: delivered | paused | terminated
stopped_at: 2026-05-24T15:30:00
quality_grade: A | B | C
  A = audience ≥ 9, Pyramid pass, 无 known_issues
  B = audience 7-8.9 用户接受,或有豁免的 Pyramid 项
  C = audience < 7 用户强制接受,或 Step 0 fail 用户终止
audience_final_score: 9.2
pyramid_known_issues: []
review_needed_architectural: []

last_artifacts:
  - brief.md ✓
  - outline.md ✓ (approved)
  - content.md ✓ (approved)
  - deck_v1.pptx ✓

how_to_resume: 跟主线程说"继续 deck <slug>",会从 stage X 续接
```

**非正常退出**(任何阶段叫停 / 失败):
- **不清理 working_dir**(所有半成品留下,STATUS.md 当书签)
- 主线程关 team(包括所有 idle 窗口)
- 主线程给用户最后一条消息含 STATUS.md 路径 + how_to_resume 摘要

**audience 5 轮后用户选"接受当前版本"**:
- 不在文件名加 `_known_issues` 后缀(避免用户拿出去用时尴尬)
- 在 `STATUS.md` 里标 `quality_grade: B` + 列具体 known_issues(audience 最后一轮的 top issues)
- 仍然走"用户最终确认"闸门,确认后才算 delivered

---

## 12. 主线程派发表(v0.5.0 引入,v0.5.1 扩展)

主线程在做 PPT 相关工作时,必须按下表派发,不允许自己干 agent 该干的事:

| 任务类型 | 谁干 | 原因 |
|---|---|---|
| 改 helpers.py / themes / build.py / pyproject / 加 tests | **主线程** | 系统改造需要 cross-file 一致性 + 完整 context |
| 用户首次说"做 PPT" / 没有 brief | 派 **iloveppt-brainstorm** | 多轮对话收 brief,主线程不该自己脑补字段 |
| 已有 brief,要出 outline / content | 派 **iloveppt-author** | content 拓写是独立 context 任务;主线程脑补容易跑偏 |
| 已有 content.md,审核保真度 + 金字塔结构 | 派 **iloveppt-content-review** | 第三方独立审计;author 自检 + builder Pyramid 不足以替代 |
| content-review pass,要构建 .pptx | 派 **iloveppt** (builder) | Pyramid 自检 + 视觉 QA 循环是 agent 内逻辑 |
| .pptx 构建完,要评视觉 | 派 **iloveppt-audience** | 读者视角是新视角;主线程的自检是作者视角,有盲区 |
| 用户给新 .pptx 模板 | 派 **iloveppt-template-extractor** | 模板提取是独立 4 级 token 流程 |

**反例(v0.4.0 失误)**:主线程自己重写了 claude-code-training 24 页 content + 自己跑 visual check。**应该派 author 写 content + 派 audience 评视觉**。

**例外**:如果用户明确说"你自己改"/"不用派 agent",尊重决定。

---

## 附录:跟旧版本的关系

- v0.5.0 引入"主线程派发规则"(本文第 12 节)
- v0.5.1 引入 content-review gate(第 7 节)+ 各 handoff 细则(第 1-11 节)
- 旧 v3 markdown-first 设计(brief.md → outline.md → content.md → deck_plan.json)继续沿用,见 `2026-05-23-iloveppt-v3-markdown-first.md`
- agent 设计的整体 rationale 见 `2026-05-23-iloveppt-agent-design.md`
