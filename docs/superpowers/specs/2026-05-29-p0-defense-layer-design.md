# P0 防御层 — 设计 spec

- **日期**:2026-05-29
- **状态**:已批准,待出实现计划
- **背景**:全产品审计(5 路并行)发现两个结构性根因 —— (1) 整条流水线是 prompt honor-system,无代码执行层;(2) 对 LLM 宣称了它给不出的确定性。审计同时发现多处静默吞错、零 CI、核心逻辑无测试。本 spec 落地审计标记为 **P0** 的三条防线。

## 目标

把**已宣称的不变量**从 prompt prose 落成**代码执行层**。

**非目标**(明确排除,避免范围蔓延):
- 不改任何 agent prompt 的创作逻辑 / 路由语义
- 不改 build 的渲染行为(只加可见性 + 外层 gate)
- 不做语义级路由校验(hook 只能 schema 级,见组件 C)
- 不补 P1/P2 项(derive_plan 单测、model-version stamp、README 修复等)
- 不动 `pyproject.toml`(rapidfuzz/pypinyin 是合理的 RAG-only 依赖,留在 `library/_rag/requirements.txt`)

## 统一原则

1. **保守**:任何拿不准的情况一律放行 / 不抛,只在明确可判定的违规上 block。
2. **可测**:每个组件配单测,断言行为而非视觉。
3. **单一 SSOT**:阈值/公式从既有 SSOT(`critic-rubric.yaml`)读,不在新脚本里重写。
4. **解耦**:三组件互不依赖,可独立 commit。

## 实现顺序(风险升序)

P0-3(组件 A) → P0-2(组件 B) → P0-1(组件 C)。

---

## 组件 A(P0-3)— 消除静默吞错

**问题**:`builder/base.py` 与 `tier1.py` 多处 `except Exception: pass/continue` 吞掉错误后静默回落,其中部分会产出破损 deck 而无任何信号。这与「中文 EA 字体破损是 #1 产物破损源」的不变量直接冲突 —— 恰是字体提取路径在静默吞错。

**修改文件**:
- `.claude/skills/pptx-deck/builder/base.py`
- `.claude/skills/pptx-deck/builder/tier1.py`

**分类处理**:

| 位置 | 类别 | 处理 |
|---|---|---|
| `base.py:258` (master EA 字体提取) | token 提取(允许降级) | 保留回落默认;`except Exception as e:` 写 structured warn 到 stderr |
| `base.py:280` (master 字号提取) | 同上 | 同上 |
| `base.py:317` (theme1.xml accent 色提取) | 同上 | 同上 |
| `base.py:475` (red_line YAML 块解析 `except: continue`) | 正确性(静默=bug) | 保留 continue(不因一个坏块炸整 build),但改 warn-loud |
| `tier1.py:326-330` (删空槽位双层 except) | 正确性(静默=bug) | 回落 `_replace_shape_text` 保留;两层都失败时 warn-loud(`模板原文可能残留`) |
| `tier1.py:302,334` (已有 WARN print) | 统一 | 收敛到同一 `_warn` 格式,走 stderr |

**新增 helper**(放在 `builder/base.py` 或共享小模块):
```python
BUILD_WARNINGS: list[str] = []  # 模块级,build_deck 入口清空

def _warn(stage: str, msg: str) -> None:
    line = f"[{stage}] WARN {msg}"
    BUILD_WARNINGS.append(line)
    print(line, file=sys.stderr)
```
warn 格式约定:`[builder.token-extract]` / `[builder.red-line]` / `[tier1.shape-removal]` 等 stage 前缀。

**可测化**:`build_deck` 入口清空 `BUILD_WARNINGS`,return dict 附 `warnings` 列表;build 结束 print 一行 `[build] N warnings`。

**新增测试** `tests/pptx_deck/test_build_warnings.py`:
- 喂会导致 token 提取失败的畸形 master 输入 → 断言**不抛** + `warnings` 含对应 `token-extract` 条目 + 仍产出 deck(用默认 token)。
- 喂含损坏 red_line YAML 块的 plan → 断言 warn-loud 记录 + 其余 red_line 约束仍生效。

**验收**:无静默 `except: pass` 残留于上述位置;现有 192 测试仍全过;新测试通过。

---

## 组件 B(P0-2)— CI

**问题**:无 `.github/`,无 CI。`.githooks/pre-commit` 是 opt-in 且不跑 pytest。任何 push 绕过所有质量门。5 个 RAG 测试在标准 pytest 下静默 skip → 整个 RAG/DB/search 路径 0 覆盖。审计还发现 `.env` 真实 key 风险,pre-commit 不拦 `sk-` 模式。

**新增文件**:`.github/workflows/ci.yml`

**触发**:`push` + `pull_request`。**环境**:ubuntu-latest / Python 3.11。

**Job steps**:
1. checkout + setup-python 3.11
2. `pip install -e ".[diagram,dev]"`
3. **main pytest**:`python -m pytest -q`(现有非-RAG 那批,期望 192 passed)
4. **RAG subset**:
   ```bash
   python3.11 -m venv library/_rag/.venv
   library/_rag/.venv/bin/pip install -r library/_rag/requirements.txt
   library/_rag/.venv/bin/python -m pytest tests/library -q
   ```
   这 5 个测试 monkey-patch embedding 函数,**不需要真 DASHSCOPE_API_KEY**。
5. **secret scan**:对 tracked 文件 grep `sk-[a-zA-Z0-9]{20,}`,命中 → 非零退出 fail(堵 key 入库)。排除本 spec / 文档里的占位示例(用 `\bsk-` 加白名单路径或限定可疑扩展名)。
6. **gitignore lint**:`python scripts/gitignore_lint.py`

**明确不做**:CI 不装 LibreOffice / 字体 / 真 API key —— 渲染与 online-RAG 不在测试层。

**验收**:CI 在 PR 上跑通;故意 push 一个含 `sk-xxxx...` 的文件能被 step 5 拦下(本地模拟验证)。

---

## 组件 C(P0-1)— return-YAML gate hook

**问题**:所有「硬门」靠主线程 parse YAML 后自觉路由,无代码兜底。审计根因 1。本组件把「YAML malformed / 缺字段 / severity 越界 / verdict 算错」这类**可机判**的违规变成代码强制(exit 2 顶回主线程)。**做不到**「YAML 合法但 next_action 选错」的语义级校验(超出 hook 能力,主线程逻辑负责)。

**新增文件**:
- `.claude/hooks/validate_agent_return.py`
- `tests/hooks/test_validate_agent_return.py`

**修改文件**:`.claude/settings.json`(加 PostToolUse hook;改前 cp 备份)

**hook 配置**(settings.json):
```json
"PostToolUse": [
  { "matcher": "Task",
    "hooks": [{ "type": "command",
      "command": "python \"${CLAUDE_PROJECT_DIR}/.claude/hooks/validate_agent_return.py\"" }] }
]
```

**validator 逻辑**(block = exit 2,极保守,拿不准一律 exit 0 放行):
1. 读 stdin JSON,取 `tool_input.subagent_type` + `tool_response` 文本。**实现期先 dump 一份真实 stdin 样本确认字段名**(不同 Claude Code 版本 payload 形态可能不同),validator 对缺字段防御性降级到 exit 0。
2. `subagent_type` 不在 `{iloveppt-critic, iloveppt-audience, iloveppt-builder, iloveppt-author, iloveppt-brainstorm}` → **exit 0**。
3. 从 response 末尾提取 ```yaml fenced block;**抓不到 → exit 0**。
4. 抓到才校验(只拦明确违规):
   - **通用**:`yaml.safe_load` 可解析;存在 `next_action` 且值在该 agent 的允许 enum 内(enum 表内置于 validator,来源 = 各 agent .md 的 return 契约)。
   - **critic**:若存在 `verdict` → 遍历各项 `severity` 必须 int ∈ {0,1,2,3};用 `critic-rubric.yaml` 读到的公式**重算 verdict**,与声明的 `verdict` 不符 → block。
   - **audience**:若存在 per-page scores → 每项 int ∈ [0,3];`deck_score`(或 `overall_score`)∈ [0,10]。
5. 合法 → exit 0;违规 → **exit 2** + stderr 输出:命中的 agent / 哪条规则 / 实际值 vs 期望 / 修法提示。

**SSOT**:critic 公式与阈值从 `.claude/agents/critic-rubric.yaml` 解析读取,validator 不硬编码阈值。

**新增测试** `tests/hooks/test_validate_agent_return.py`(以子进程 / 直接调函数喂构造的 stdin JSON,断言 exit code):
- 合法 critic 返回 → exit 0
- critic severity = 4 → exit 2
- critic verdict 与公式重算不符 → exit 2
- audience deck_score = 11 → exit 2
- 缺 yaml block → exit 0
- 非 iloveppt subagent_type(如 Explore) → exit 0
- 畸形 / 缺字段 stdin → exit 0(防御性放行,不崩)

**上线顺序**(降误杀风险):先把 validator + 单测写完跑绿,**确认对历史真实返回零误杀**,再改 settings.json 接入。

**验收**:单测全绿;接入后正常跑一次完整 / 半截流水线无误杀;构造一个 verdict 算错的返回能被 block。

---

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| 组件 C validator 误杀正常返回卡死流水线 | 极保守设计(拿不准放行) + 上线前用历史返回验零误杀 + 单测覆盖放行 case |
| PostToolUse payload 字段名跟假设不符 | 实现期先 dump 真实 stdin 样本;validator 对缺字段防御降级 exit 0 |
| CI RAG venv 安装在 ubuntu 失败(sqlite-vec wheel) | step 4 设为 `continue-on-error` 观察期 or pin 版本;先验证 wheel 可用 |
| 改 settings.json 破坏现有 telemetry hook | 改前 cp 备份;只新增 PostToolUse,不动 Stop |

## 验收(整体)

- 三组件各自单测/CI 绿。
- 现有 192 测试不回归。
- 三组件独立 commit,commit message 用 conventional commits(`fix(pptx-deck):` / `ci:` / `feat(hooks):`)。
