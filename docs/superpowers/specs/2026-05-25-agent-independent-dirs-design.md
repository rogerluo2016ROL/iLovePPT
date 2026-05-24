# Agent 独立目录布局 refactor · 设计 spec

> **任务**:每个 agent 产出物放各自独立文件夹,不混在 deck working_dir 根目录。
>
> **创建**:2026-05-25
> **分支**:`feat/optimization`
> **状态**:待执行(spec 已批准)

---

## 1. 重构目标

当前 deck working dir 把 7 个 agent 产物全堆在根目录(`brief.md` / `outline.md` / `content.md` / `critic_report_*.md` / `audience_review*.md` / `designer_report.md` / `deck_plan.json` / `.pptx` / `_assets/*` / `.iloveppt_*_state.json` / `STATUS.md` 等),问题:

- 文件多了不知道哪个是谁产的
- agent 跑多轮(audience r2/r3/r4 / deck_v2_*)后根目录爆炸
- 调试 / 复盘时要凭文件名前缀猜归属

**目标**:agent 产物按归属下沉到独立子目录,deck 根只留主线程产物(`STATUS.md`)和用户提供的共享资产(`_assets/`)。

---

## 2. 重构参数(brainstorming 已对齐)

| 维度 | 决策 |
|---|---|
| **目录命名** | 纯 agent 名(`brainstorm/` / `author/` / `critic/` / `builder/` / `designer/` / `audience/` / `extractor/`),不加编号、不带 stage 前缀 |
| **`_assets/` 拆分** | agent 生产物归各自(`author/charts/` / `designer/icons/` / `designer/hero/`),用户提供保留 deck 根 `_assets/`(`raw/` / `brand/` / `refs/`) |
| **state file** | 跟产物同目录,文件名简化为 `state.json`(`brainstorm/state.json` / `author/state.json`)|
| **现有 deck** | 删 `decks/claude-code-training/`(测试产物,不迁移) |
| **`STATUS.md`** | 保留 deck 根目录(主线程产物,非 agent) |

---

## 3. 新 schema(deck working dir)

```
<working_dir>/   # 即 ${CLAUDE_PROJECT_DIR}/decks/<slug>/
├── STATUS.md                          ← 主线程产物(交付摘要)
│
├── brainstorm/                        ← Stage A-B
│   ├── state.json                       (was .iloveppt_dialog_state.json)
│   └── brief.md
│
├── author/                            ← Stage C-D
│   ├── state.json                       (was .iloveppt_author_state.json)
│   ├── deck_v1_outline.md
│   ├── deck_v1_content.md
│   ├── deck_v2_outline.md               (大改 +1 iteration)
│   ├── deck_v2_content.md
│   └── charts/                          (matplotlib 出图,was _assets/charts/)
│
├── critic/                            ← Stage C/D 双 gate
│   ├── critic_report_C.md
│   └── critic_report_D.md
│
├── builder/                           ← Stage E
│   ├── deck_v1_content.postbuild.md     (auto 调整副本,原文不动)
│   ├── deck_plan.json                   (机械接缝)
│   ├── deck_v1.pptx                     (最终产物)
│   └── deck_v1_render/                  (QA 用 PNG)
│
├── designer/                          ← Stage E.5
│   ├── designer_report.md
│   ├── icons/                           (was _assets/icons/)
│   └── hero/                            (was _assets/hero/)
│
├── audience/                          ← Stage F
│   ├── audience_review.md               (r1,无后缀)
│   ├── audience_review_r2.md
│   ├── audience_review_r3.md
│   └── audience_review_r4.md
│
├── extractor/                         ← 旁路(用户给模板时才有)
│   └── (probe deck + 视觉分析报告)
│
└── _assets/                           ← 用户提供,跨 agent 共享
    ├── raw/                             (csv / png 等原始素材)
    ├── brand/                           (用户自带 brand assets)
    └── refs/                            (用户给的参考图)
```

---

## 4. 跨 agent 读路径(关键耦合点)

agent 写自己目录,但读其他 agent 产物 — 这是必要耦合,要在 agent 文件 + pipeline-protocol 里明确写出。

| Agent | 读什么 | 从哪 |
|---|---|---|
| `author` | brief | `brainstorm/brief.md` |
| `critic` | brief + outline + content | `brainstorm/brief.md` + `author/deck_v{N}_*.md` |
| `builder` | content + author state(pyramid_known_issues)+ critic D | `author/deck_v{N}_content.md` + `author/state.json` + `critic/critic_report_D.md` |
| `designer` | pptx + render + deck_plan + content(只读)+ brief(只读)| `builder/`(read-only)+ `author/`(read-only)+ `brainstorm/` |
| `audience` | render PNG | `builder/deck_v{N}_render/` |
| `audience`(自己) | prior reviews(多轮迭代)| `audience/audience_review_r{N-1}.md` |
| `designer`(自己) | prior reports + prior audience | `designer/designer_report.md` + `audience/audience_review_r{N-1}.md` |

**handoff 协议不变**:agent 只通过主线程 SendMessage 串联,不直接调用别的 agent;但 Read 跨目录文件是允许的(`<working_dir>/<other_agent>/<file>`)。

---

## 5. 改动清单

| 类型 | 文件 | 改动 |
|---|---|---|
| **agent 文件** | `.claude/agents/iloveppt-brainstorm.md` | brief.md 路径 → `brainstorm/brief.md`;state file → `brainstorm/state.json` |
| | `.claude/agents/iloveppt-author.md` | outline / content / charts 路径 → `author/`;state → `author/state.json` |
| | `.claude/agents/iloveppt-critic.md` | report 路径 → `critic/`;入参 brief/outline/content path 调整(跨目录读) |
| | `.claude/agents/iloveppt.md`(builder) | content / postbuild / deck_plan / pptx / render 路径 → `builder/`;Read critic_d / author state 路径调整 |
| | `.claude/agents/iloveppt-designer.md` | report / icons / hero 路径 → `designer/`;Read pptx / render / deck_plan / content / brief 跨目录调整 |
| | `.claude/agents/iloveppt-audience.md` | review 路径 → `audience/`;Read render 跨目录 → `builder/deck_v{N}_render/` |
| | `.claude/agents/iloveppt-template-extractor.md` | extractor 产物 → `extractor/` |
| **协议文档** | `.claude/pipeline-protocol.md` | §11 工作目录布局重写;各 agent 入参契约 path 字段更新 |
| **架构文档** | `docs/agent-internals.zh.md` | §5.3 工作目录布局图重写;agent 内部流程图里涉及路径的 caption 更新 |
| | `docs/MANUAL.zh.md` | "你的 deck 会用一个目录管所有产物"章节布局图更新 |
| **代码** | `skills/pptx-deck/build.py` | content_md_path 默认值 / output_pptx 默认值 / 渲染 PNG 输出目录调整 |
| | `tests/` | 检查有无引用旧路径的测试 fixture / mock(实施时验证)|
| **清理** | `decks/claude-code-training/` | 整目录删除(17 文件,测试产物)|
| **新增** | 本 spec | `docs/superpowers/specs/2026-05-25-agent-independent-dirs-design.md` |

---

## 6. 执行步骤

按依赖顺序:

1. **删 `decks/claude-code-training/`**(避免迁移负担,clean slate)
2. **改 7 agent 文件**(每个里面 path / state file / Read 跨目录 都改对)
3. **改 `pipeline-protocol.md`**(§11 + 各 agent 入参契约 path 字段)
4. **改 `build.py`**(默认路径)
5. **跑测试**(`python3 -m pytest tests/ -q`)确认 72 个测试不被路径变化破坏
6. **改文档**(`agent-internals.zh.md` + `MANUAL.zh.md` 工作目录布局图)
7. **测试新 deck**(可选 · 实施完成后跑一个新 deck 验证 end-to-end work)

---

## 7. 验收标准

- [ ] 7 个 agent 文件里所有 path 字段都按新 schema(grep 旧路径残留为 0)
- [ ] `pipeline-protocol.md` §11 工作目录布局跟 spec §3 一致
- [ ] `agent-internals.zh.md` §5.3 工作目录布局跟 spec §3 一致
- [ ] `MANUAL.zh.md` 工作目录章节跟 spec §3 一致
- [ ] `build.py` 默认路径 + render 输出目录跟新 schema 对齐
- [ ] `decks/claude-code-training/` 删除完成
- [ ] 72 个 pytest 测试全过
- [ ] grep `.iloveppt_dialog_state` / `.iloveppt_author_state` 不再出现在 agent / 协议 / 文档(state file 改名为 `state.json` + 进 agent 目录)
- [ ] grep `_assets/charts/` / `_assets/icons/` / `_assets/hero/` 不再出现(改到 agent 目录下)

---

## 8. 风险与缓解

| 风险 | 缓解 |
|---|---|
| 改完 agent 文件路径但漏掉 build.py 默认参数 → 跑新 deck 时 builder 写错位置 | step 4 + step 5(跑 pytest)防住;实施时 grep 全仓 `working_dir` 引用 |
| 跨 agent Read 路径写错导致 agent 找不到文件 → 跑 deck 时静默 fail | 在每个 agent 文件里**显式列出"跨目录读"的所有 path**,审 PR 时对照 spec §4 表格 |
| 文档没改 / 改不全 → 新人按文档跑 deck 跑错 | 实施时把 spec §3 schema 整段贴进 agent-internals + pipeline-protocol + MANUAL |
| 旧 .gitignore 还在 ignore `.iloveppt_*_state.json` → 新 state.json 不被 ignore | 看 .gitignore 是否引用旧 state 名,需要时改成 `state.json`(若 state 不进 git;若进 git 就不动)|
| pytest fixture 引用旧路径破坏测试 | step 5 跑测试拦截,失败时 grep 修复 |

---

## 9. 不在本次范围

- 不动 `templates/`(整模板库,不属于 deck working_dir)
- 不动 `library/visual-patterns/`(全局 RAG 库,跟 deck 解耦)
- 不动 git history(用 `rm -rf` 删测试 deck,不用 git mv)
- 不实现新 deck 测试自动化(留作下一步可选)
