# 多轮迭代产物版本化 · 设计 spec

> **任务**:critic / designer / audience 多轮迭代产物全保留(_r1 / _r2 / ... / _r5),不再"只覆盖最新一份"。
>
> **创建**:2026-05-25
> **分支**:`feat/optimization`
> **状态**:待执行(spec 已批准)

---

## 1. 重构目标

当前 critic / designer 多轮迭代时,后轮产物**覆盖**前轮 —— `critic_report_D.md` 第 2 轮跑后,第 1 轮内容丢失,无法事后复盘"为什么 r1 fail r2 改成 pass"。

audience 已经有 `audience_review.md` (r1) → `_r2` → `_r3` → `_r4` 累积,但其他 agent 没有。

**目标**:critic / designer / audience 三个评审类 agent 多轮产物全保留 `_r1 / _r2 / ... / _r5`,主线程 handoff 时传具体轮次 path。可事后追溯收敛轨迹。

---

## 2. 重构参数(brainstorming 已对齐)

| 维度 | 决策 |
|---|---|
| **覆盖范围** | critic + designer + audience(builder/author 不变) |
| **后缀规则** | `_r1 / _r2 / _r3 / _r4 / _r5`(round) |
| **保留策略** | 全保留 r1-r5(已有 5 轮 cap,KB 级文件占地小) |
| **state.json** | **不动**(YAGNI · iteration 信息由文件名 + report 内 timestamp 已表达) |
| **r1 命名** | **强制 `_r1` 后缀**(改 audience 现状 `audience_review.md` → `audience_review_r1.md`,命名规则统一) |

---

## 3. 新命名规则(全部强制 `_r{N}` 后缀)

| Agent | 文件名 |
|---|---|
| critic Stage C | `critic/critic_report_C_r1.md` / `_r2.md` / `_r3.md` / `_r4.md` / `_r5.md` |
| critic Stage D | `critic/critic_report_D_r1.md` / `_r2.md` ... |
| designer | `designer/designer_report_r1.md` / `_r2.md` ... |
| audience | `audience/audience_review_r1.md` / `_r2.md` ... |

**不动**(已有版本逻辑):
- `author/deck_v{N}_outline.md` / `content.md`(N 由 author iteration 驱动,代表"内容大改",不是"评审多轮")
- `builder/deck_v{N}.pptx` / `deck_v{N}_render/`(N 同 author)
- `brainstorm/state.json` / `author/state.json`
- `_assets/raw/` / `brand/` / `refs/`(用户素材)
- `STATUS.md`(交付摘要,一份)

---

## 4. 跨 agent handoff(关键耦合点)

### 4.1 主线程"找最新轮"逻辑

主线程在 dispatch 含 `_r{N}` 路径的入参时,**必须找最新轮**:

```bash
# Python 伪代码(主线程内)
import glob, re
files = glob.glob(f"{working_dir}/critic/critic_report_D_r*.md")
files.sort(key=lambda p: int(re.search(r'_r(\d+)\.md$', p).group(1)))
latest = files[-1]    # critic_report_D_r3.md (假设当前到 r3)
```

或等价 shell:`ls critic_report_D_r*.md | sort -V | tail -1`。

### 4.2 入参传具体 path

| 接收 agent | 入参字段 | 主线程传值 |
|---|---|---|
| builder | `critic_d_report_path` | `<working_dir>/critic/critic_report_D_r{N}.md`(最新 pass 那轮)|
| designer | `prev_audience_review_path` | `<working_dir>/audience/audience_review_r{N-1}.md`(上轮)|
| designer | `prev_designer_report_path` | `<working_dir>/designer/designer_report_r{N-1}.md` |
| audience | (自己读上轮)| 自己在 Step 0 `Glob audience_review_r*.md` 找上轮 |

### 4.3 agent 写入逻辑

agent 在 Write report 时,根据"当前是第几轮"决定后缀:

```python
# Python 伪代码(agent 内,以 critic 为例)
existing = glob(f"{working_dir}/critic/critic_report_{stage}_r*.md")
next_r = max([int(re.search(r'_r(\d+)\.md$', p).group(1)) for p in existing], default=0) + 1
output_path = f"{working_dir}/critic/critic_report_{stage}_r{next_r}.md"
Write(output_path, report_content)
```

agent 自己计算下一轮号(避免依赖入参)。

---

## 5. 改动清单

| 类型 | 文件 | 改动 |
|---|---|---|
| **agent 文件** | `.claude/agents/iloveppt-critic.md` | 产物路径加 `_r{N}` + 写入逻辑(找最新轮 +1)|
| | `.claude/agents/iloveppt-designer.md` | 产物 + prev_audience/prev_designer 入参描述 |
| | `.claude/agents/iloveppt-audience.md` | 产物 + 找上轮 review 逻辑 |
| | `.claude/agents/iloveppt.md`(builder) | Read critic_report_D 路径变(入参带 `_r{N}`)|
| **协议** | `.claude/pipeline-protocol.md` | 各 agent 入参契约 path / 主线程"找最新轮"伪代码新增章节 / handoff 描述含 _r{N} |
| **文档** | `docs/agent-internals.zh.md` §5.3 | 工作目录布局同步新命名 |
| | `docs/MANUAL.zh.md` | 工作目录章节同步 |
| **不动** | `build.py` / `extract_template.py` / `tests/` | 机械工具不感知 agent 命名 |
| **新增** | 本 spec | `docs/superpowers/specs/2026-05-25-version-mgmt-design.md` |

---

## 6. 执行步骤

按依赖顺序:

1. **改 4 agent 文件**(critic / designer / audience / builder)
2. **改 pipeline-protocol.md**(新增 §X "找最新轮"伪代码 + 各处 path 更新)
3. **改 docs**(agent-internals + MANUAL 工作目录布局)
4. **跑 pytest** 确认 72 测试不破
5. **commit + push**(本分支 feat/optimization)

---

## 7. 验收标准

- [ ] critic 产物全部 `_r{N}` 后缀(grep `critic_report_[CD]\.md` 无裸名)
- [ ] designer 产物 `designer_report_r{N}.md`(grep `designer_report\.md` 无裸名)
- [ ] audience 产物 `audience_review_r{N}.md`(grep `audience_review\.md` 无裸名)
- [ ] pipeline-protocol.md 含"找最新轮"伪代码(主线程参考)
- [ ] agent 文件含"写入找下一轮 +1"逻辑
- [ ] agent-internals.zh.md §5.3 工作目录布局图同步
- [ ] MANUAL.zh.md 工作目录章节同步
- [ ] 72 pytest 全过
- [ ] builder 不感知 `_r{N}`(只 Read 入参传的具体路径)

---

## 8. 风险与缓解

| 风险 | 缓解 |
|---|---|
| 主线程"找最新轮"逻辑漏写或写错 → agent 收到错 path | spec §4.1 给伪代码;pipeline-protocol 新增独立章节强调 |
| agent 多轮跑时算 next_r 算错(并发场景)→ 多轮同一文件名冲突 | iLovePPT agent 是串行派发(主线程 SendMessage 后才进入下一轮),无并发问题 |
| 文档同步漏改 → 用户按文档跑 path 跑错 | step 3 + 7 验收 check |
| 现有 audience 用户已习惯 `audience_review.md` 命名 | spec 明确改名 → audience_review_r1.md;agent 文件 + 用户文档都同步 |

---

## 9. 不在本次范围

- 不动 `author/deck_v{N}_*.md`(N 已经被 author iteration 用)
- 不动 `builder/deck_v{N}.pptx`(N 同 author)
- 不动 state.json(YAGNI · 文件名已表达 iteration)
- 不实现"按时间戳排序 vs 按 r 号排序"歧义处理(本 spec 只用 r 号)
- 不实现自动清理旧轮(全保留 5 轮内,5 轮 cap 已是上限)
