# P0 防御层 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把审计标记的 P0 三条防线从 prompt prose 落成代码执行层:静默吞错 fail-loud(组件 A)、CI(组件 B)、return-YAML gate hook + critic 结构化 severity + verdict 重算(组件 C)。

**Architecture:** 三组件解耦,可独立 commit,风险升序实现(A→B→C)。A 改 builder 让吞掉的错误可见;B 加 GitHub Actions 跑现有+RAG 测试+密钥扫;C 加 PostToolUse hook 校验 iloveppt-* subagent 的 handoff YAML,并让 critic 吐机器可读 `scores` 供 hook 重算 verdict。

**Tech Stack:** Python 3.11 / pytest / PyYAML / GitHub Actions / Claude Code hooks(PostToolUse, JSON-over-stdin, exit 2 = block)。

---

## 对已批准 spec 的偏离(已与用户确认)

1. **`build_deck` 返回类型不变**(仍 `Path`):warnings 不挂返回值(会破坏 build.py + 现有测试),改用模块级 `BUILD_WARNINGS` 列表 + 结束打印汇总,测试 import 断言。
2. **组件 C 增加「改 critic 输出契约」**:真实 critic report `.md` 不含可机器解析的整数 severity(全是散文 + high/med/low),所以无法读 report 重算。改为让 critic 在 **return YAML** 里新增机器可读 `scores: [{id, severity}]`(int 0-3),validator 直接据此重算。
3. **audience 只做 schema 校验**,不重算 verdict(其聚合公式 min/avg 文档自相矛盾,重算会误报)。
4. **J5 不计入 verdict 重算**:`critic-rubric.yaml` 内部矛盾(formula header 说全 21 项,J5 描述说「不计入 verdict 决定」)。本计划按 J5 自身描述解析 —— recompute over A1-A7 + B1-B9 + J1-J4,并在 rubric 注释里写明以消歧。

## 文件结构

| 文件 | 动作 | 职责 |
|---|---|---|
| `.claude/skills/pptx-deck/builder/base.py` | 改 | 加 `_warn`/`BUILD_WARNINGS`;token-extract + red_line except → warn |
| `.claude/skills/pptx-deck/builder/tier1.py` | 改 | slot-map / shape-removal except + print → `_warn` |
| `tests/pptx_deck/test_build_warnings.py` | 建 | 组件 A 单测 |
| `.github/workflows/ci.yml` | 建 | CI:main pytest + RAG venv subset + 密钥扫 + gitignore_lint |
| `.claude/hooks/validate_agent_return.py` | 建 | 组件 C validator(schema + critic verdict 重算) |
| `tests/hooks/test_validate_agent_return.py` | 建 | 组件 C 单测 |
| `.claude/agents/iloveppt-critic.md` | 改 | return YAML 加 `scores` 块 + 填写指令 |
| `.claude/pipeline-protocol.md` | 改 | §4.3 critic schema 加 `scores` |
| `.claude/agents/critic-rubric.yaml` | 改 | formula 注释消歧(J5 不计入重算) |
| `.claude/settings.json` | 改 | 加 PostToolUse hook(改前备份) |

---

# 组件 A(P0-3)— 消除静默吞错

### Task A1: `_warn` 基础设施 + build_deck 清空/汇总

**Files:**
- Modify: `.claude/skills/pptx-deck/builder/base.py`(加 import + 模块级常量 + helper;build_deck 头尾)
- Test: `tests/pptx_deck/test_build_warnings.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/pptx_deck/test_build_warnings.py
"""组件 A(P0-3)· builder 静默吞错 → fail-loud 可见性测试。"""
import importlib

import pytest

base = importlib.import_module("builder.base")


def test_warn_appends_and_prints(capsys):
    base.BUILD_WARNINGS.clear()
    base._warn("builder.token-extract", "示例消息")
    captured = capsys.readouterr()
    assert base.BUILD_WARNINGS == ["[builder.token-extract] WARN 示例消息"]
    assert "[builder.token-extract] WARN 示例消息" in captured.err
    assert captured.out == ""  # 必须走 stderr 不污染 stdout
```

- [ ] **Step 2: 跑测试确认 fail**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/pptx_deck/test_build_warnings.py::test_warn_appends_and_prints -v`
Expected: FAIL — `AttributeError: module 'builder.base' has no attribute '_warn'`

- [ ] **Step 3: 实现 `_warn` + `BUILD_WARNINGS`**

在 `base.py` import 区(`import sys` 已存在,line 19)后、`HERE = ...`(line 27)前插入:

```python
# === P0-3 · 静默吞错可见性(组件 A) ===
# build 过程中被"吞掉但回落"的错误统一走这里:既保留回落鲁棒性,又不再静默。
# 模块级列表方便测试断言;build_deck 入口清空,结束打印汇总。
BUILD_WARNINGS: list[str] = []


def _warn(stage: str, msg: str) -> None:
    """记一条 build warning:append 到 BUILD_WARNINGS + 打印到 stderr。

    stage 约定前缀:`builder.token-extract` / `builder.red-line` /
    `tier1.slot-map` / `tier1.shape-removal`。
    """
    line = f"[{stage}] WARN {msg}"
    BUILD_WARNINGS.append(line)
    print(line, file=sys.stderr)
```

- [ ] **Step 4: 跑测试确认 pass**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/pptx_deck/test_build_warnings.py::test_warn_appends_and_prints -v`
Expected: PASS

- [ ] **Step 5: build_deck 入口清空 + 结束汇总**

在 `build_deck`(line 531)函数体最前面(`from . import tier1, tier2, tier3` 之后)加:

```python
    BUILD_WARNINGS.clear()
```

在 `build_deck` 末尾 `prs.save(str(out))` 之后、`return out` 之前加:

```python
    if BUILD_WARNINGS:
        print(f"[build] {len(BUILD_WARNINGS)} warnings", file=sys.stderr)
```

- [ ] **Step 6: 跑全量 build 测试确认无回归**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/pptx_deck/ -q`
Expected: 全 PASS(现有 + 新增)

- [ ] **Step 7: Commit**

```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
git add .claude/skills/pptx-deck/builder/base.py tests/pptx_deck/test_build_warnings.py
git commit -m "fix(pptx-deck): 加 _warn/BUILD_WARNINGS 基础设施(P0-3 组件A)"
```

---

### Task A2: base.py token-extract + red_line except → `_warn`

**Files:**
- Modify: `.claude/skills/pptx-deck/builder/base.py:236, 258, 280, 317, 475`
- Test: `tests/pptx_deck/test_build_warnings.py`

- [ ] **Step 1: 写失败测试**

追加到 `tests/pptx_deck/test_build_warnings.py`:

```python
def test_extract_design_tokens_bad_path_warns_not_raises():
    base.BUILD_WARNINGS.clear()
    # 不存在的 .pptx → Presentation() 抛 → 必须被 catch 且回落空 dict + warn
    tokens = base._extract_design_tokens("/nonexistent/does-not-exist.pptx")
    assert tokens == {}
    assert any("token-extract" in w for w in base.BUILD_WARNINGS)


def test_parse_red_line_words_bad_yaml_block_warns(tmp_path):
    base.BUILD_WARNINGS.clear()
    brief = tmp_path / "brief.md"
    # 一个 safe_load 会抛的损坏 yaml fence + 一个合法 front-matter
    brief.write_text(
        "---\n"
        "constraints:\n"
        "  red_line_words: [禁词1]\n"
        "---\n\n"
        "```yaml\n"
        "foo: [unclosed\n"
        "```\n",
        encoding="utf-8",
    )
    words = base._parse_red_line_words(str(brief))
    # 合法 front-matter 仍解析出禁词;损坏 block 被 warn 而非静默 continue
    assert "禁词1" in words
    assert any("red-line" in w for w in base.BUILD_WARNINGS)
```

- [ ] **Step 2: 跑测试确认 fail**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/pptx_deck/test_build_warnings.py -k "bad_path or bad_yaml" -v`
Expected: FAIL — token 测试 `BUILD_WARNINGS` 为空(当前静默);red_line 测试 `BUILD_WARNINGS` 为空(当前 `except: continue` 静默)

- [ ] **Step 3: 改 5 处 except**

`base.py:236-237`(Presentation 打开失败):
```python
    try:
        prs = Presentation(pptx_path)
    except Exception as e:
        _warn("builder.token-extract", f"无法打开 .pptx 提取 token,全部回落默认: {e!r}")
        return tokens
```

`base.py:258-259`(master EA 字体/字号):
```python
    except Exception as e:
        _warn("builder.token-extract", f"master EA 字体提取失败,回落默认: {e!r}")
```

`base.py:280-281`(master 字号):
```python
    except Exception as e:
        _warn("builder.token-extract", f"master 字号提取失败,回落默认: {e!r}")
```

`base.py:317-318`(theme1.xml accent 色):
```python
    except Exception as e:
        _warn("builder.token-extract", f"theme1.xml accent 色提取失败,回落默认: {e!r}")
```

`base.py:473-476`(red_line YAML 块):
```python
        try:
            data = _yaml.safe_load(block) or {}
        except Exception as e:
            _warn("builder.red-line", f"跳过损坏的 red_line YAML 块: {e!r}")
            continue
```

- [ ] **Step 4: 跑测试确认 pass**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/pptx_deck/test_build_warnings.py -k "bad_path or bad_yaml" -v`
Expected: PASS

- [ ] **Step 5: 确认无残留静默 except**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && grep -n "except Exception:" .claude/skills/pptx-deck/builder/base.py`
Expected: 无输出(全部带 `as e` + `_warn`)

- [ ] **Step 6: 跑全量确认无回归**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/pptx_deck/ -q`
Expected: 全 PASS

- [ ] **Step 7: Commit**

```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
git add .claude/skills/pptx-deck/builder/base.py tests/pptx_deck/test_build_warnings.py
git commit -m "fix(pptx-deck): base.py token-extract + red_line 静默 except → _warn(P0-3 组件A)"
```

---

### Task A3: tier1.py slot-map / shape-removal except + print → `_warn`

**Files:**
- Modify: `.claude/skills/pptx-deck/builder/tier1.py:302, 326-330, 334`
- Test: `tests/pptx_deck/test_build_warnings.py`

- [ ] **Step 1: 写失败测试**

追加到 `tests/pptx_deck/test_build_warnings.py`:

```python
def test_tier1_shape_removal_double_failure_warns(monkeypatch):
    """删空槽位 + 替换均失败时必须 warn-loud(模板原文可能残留),不静默。"""
    tier1 = importlib.import_module("builder.tier1")
    base.BUILD_WARNINGS.clear()

    class _BadElement:
        def getparent(self):
            raise RuntimeError("parent boom")

    class _FakeShape:
        _element = _BadElement()

    # _replace_shape_text 也抛 → 进入最内层,必须 warn 而非 pass
    monkeypatch.setattr(
        tier1, "_replace_shape_text",
        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("replace boom")),
    )
    # 直接驱动删除循环的私有 helper(若不存在则在 Step 3 提取)
    tier1._remove_blank_shapes([_FakeShape()])
    assert any("tier1.shape-removal" in w for w in base.BUILD_WARNINGS)
```

- [ ] **Step 2: 跑测试确认 fail**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/pptx_deck/test_build_warnings.py::test_tier1_shape_removal_double_failure_warns -v`
Expected: FAIL — `AttributeError: module 'builder.tier1' has no attribute '_remove_blank_shapes'`

- [ ] **Step 3: 提取 `_remove_blank_shapes` helper + 接 `_warn`**

在 `tier1.py` 顶部 import 区加(函数内局部 import 避免模块加载序问题):
> 注:`_warn` 用局部 import(`from .base import _warn`),因 tier1 只在 build_deck 运行时被 import,此时 base 已完全加载。

把 `_apply_text_map_by_slots` 里 line 319-330 的内联删除循环替换为调用新 helper,并新增 helper(放在 `_apply_text_map_by_slots` 之后):

```python
def _remove_blank_shapes(shapes) -> None:
    """删除空槽位 shape;失败回落到清空文本;两者都失败 → warn-loud(原文可能残留)。"""
    from .base import _warn
    for shape in shapes:
        try:
            sp = shape._element
            parent = sp.getparent()
            if parent is not None:
                parent.remove(sp)
        except Exception as e:
            try:
                _replace_shape_text(shape, "", text_color_hex=None, font_size_pt=None)
            except Exception as e2:
                _warn(
                    "tier1.shape-removal",
                    f"空槽位删除+替换均失败,模板原文可能残留: remove={e!r} replace={e2!r}",
                )
```

把 line 319-330 原循环改为:
```python
    # Now remove the empty-slot shapes (top-level only via parent.remove)
    _remove_blank_shapes(shapes_to_blank_remove)
```

- [ ] **Step 4: slot-map 两处 print → `_warn`**

`tier1.py:302`:
```python
        if shape is None or not shape.has_text_frame:
            from .base import _warn
            _warn("tier1.slot-map", f"slot {slot_id!r} tree_path={tree_path} 找不到 / 无 text_frame")
            continue
```

`tier1.py:334`(unmatched):
```python
    if unmatched:
        from .base import _warn
        _warn("tier1.slot-map", f"text_map keys {sorted(unmatched)} 无对应 slot, 已跳过")
```

- [ ] **Step 5: 跑测试确认 pass**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/pptx_deck/test_build_warnings.py::test_tier1_shape_removal_double_failure_warns -v`
Expected: PASS

- [ ] **Step 6: 确认无残留静默 except / 裸 print(WARN)**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && grep -nE "except Exception:\s*$|print\(f?\"  WARN" .claude/skills/pptx-deck/builder/tier1.py`
Expected: 无输出

- [ ] **Step 7: 跑全量确认无回归 + Commit**

```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
python -m pytest tests/pptx_deck/ tests/pptx/ -q
git add .claude/skills/pptx-deck/builder/tier1.py tests/pptx_deck/test_build_warnings.py
git commit -m "fix(pptx-deck): tier1 slot-map/shape-removal 静默 except+print → _warn(P0-3 组件A)"
```

---

# 组件 B(P0-2)— CI

### Task B1: GitHub Actions workflow

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: 本地预验每个 step 可绿(写 yaml 前先确认命令本身工作)**

Run:
```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
# 1. main pytest
python -m pytest -q | tail -3
# 2. RAG venv subset(确认 wheel 可装 + 测试可跑)
rm -rf /tmp/_ragvenv && python3 -m venv /tmp/_ragvenv \
  && /tmp/_ragvenv/bin/pip -q install -r library/_rag/requirements.txt \
  && /tmp/_ragvenv/bin/pip -q install -e ".[diagram,dev]" \
  && /tmp/_ragvenv/bin/python -m pytest tests/library -q | tail -5
# 3. 密钥扫(应 0 命中 → exit 1 表示「发现密钥」,这里期望无命中)
if git grep -nIE 'sk-[a-zA-Z0-9]{20,}' -- ':!docs/superpowers/' ':!.github/'; then echo "FOUND(不应该)"; else echo "clean"; fi
# 4. gitignore_lint 退出码
python scripts/gitignore_lint.py; echo "exit=$?"
```
Expected: pytest 全绿;RAG 5 测试 PASS(非 skip);密钥扫 `clean`;gitignore_lint `exit=0`。
> 若 RAG venv 装 `sqlite-vec` wheel 在本机失败,记录下来 —— Step 2 的 CI step 暂设 `continue-on-error: true` 并注释,待 ubuntu runner 验证后翻 false。

- [ ] **Step 2: 写 workflow**

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install main deps
        run: pip install -e ".[diagram,dev]"

      - name: Main pytest (non-RAG)
        run: python -m pytest -q

      - name: RAG venv + subset tests
        run: |
          python3 -m venv library/_rag/.venv
          library/_rag/.venv/bin/pip install -r library/_rag/requirements.txt
          library/_rag/.venv/bin/pip install -e ".[diagram,dev]"
          library/_rag/.venv/bin/python -m pytest tests/library -q

      - name: Secret scan (block sk- keys)
        run: |
          if git grep -nIE 'sk-[a-zA-Z0-9]{20,}' -- ':!docs/superpowers/' ':!.github/'; then
            echo "::error::发现疑似 API key(sk-...)入库"
            exit 1
          fi
          echo "no secrets found"

      - name: gitignore lint
        run: python scripts/gitignore_lint.py
```

- [ ] **Step 3: 校验 yaml 语法**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml')); print('yaml ok')"`
Expected: `yaml ok`

- [ ] **Step 4: 模拟密钥扫能拦下真 key(临时验证后删)**

Run:
```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
printf 'key=sk-abcdefghij0123456789abcdef\n' > /tmp/_leak.txt
git add -f /tmp/_leak.txt 2>/dev/null || true
# 直接对工作区文件验证正则(不真 add 到仓库)
echo 'key=sk-abcdefghij0123456789abcdef' | grep -nIE 'sk-[a-zA-Z0-9]{20,}' && echo "BLOCK works"
rm -f /tmp/_leak.txt
```
Expected: 命中 + `BLOCK works`

- [ ] **Step 5: Commit**

```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
git add .github/workflows/ci.yml
git commit -m "ci: 加 GitHub Actions — main pytest + RAG venv subset + 密钥扫 + gitignore_lint(P0-2 组件B)"
```

---

# 组件 C(P0-1)— return-YAML gate hook + critic 结构化 severity

### Task C1: validator 纯函数 — 文本提取 + yaml block 抽取 + 阈值加载

**Files:**
- Create: `.claude/hooks/validate_agent_return.py`
- Test: `tests/hooks/test_validate_agent_return.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/hooks/test_validate_agent_return.py
"""组件 C(P0-1)· PostToolUse validator 单测。"""
import importlib.util
from pathlib import Path

_HOOK = Path(__file__).resolve().parents[2] / ".claude/hooks/validate_agent_return.py"
_spec = importlib.util.spec_from_file_location("validate_agent_return", _HOOK)
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)


def test_extract_text_handles_str_and_blocks():
    assert v._extract_text("hello") == "hello"
    assert v._extract_text({"content": "abc"}) == "abc"
    assert v._extract_text([{"type": "text", "text": "x"}, {"type": "text", "text": "y"}]) == "x\ny"
    assert v._extract_text(None) == ""


def test_extract_last_yaml_block():
    text = "preamble\n```yaml\na: 1\n```\nmid\n```yaml\nnext_action: pass\n```\n"
    block = v._extract_last_yaml_block(text)
    assert "next_action: pass" in block
    assert "a: 1" not in block  # 取最后一个 block
    assert v._extract_last_yaml_block("no fence here") is None


def test_load_critic_thresholds():
    t = v._load_critic_thresholds()
    assert t["block_severity"] == 3
    assert t["warn_accumulation"] == 5
    assert t["notes_min_severity"] == 1
```

- [ ] **Step 2: 跑测试确认 fail**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/hooks/test_validate_agent_return.py -k "extract or thresholds" -v`
Expected: FAIL — 文件不存在 / 函数未定义

- [ ] **Step 3: 实现纯函数**

```python
#!/usr/bin/env python3
# .claude/hooks/validate_agent_return.py
"""PostToolUse hook · 校验 iloveppt-* subagent 的 return handoff YAML(组件 C / P0-1)。

设计原则:block(exit 2)极保守 —— 拿不准 / 无结构 / 非主流水线 agent 一律 exit 0 放行。
只在「明确可判定的违规」上 block:
  - return YAML 解析失败(主流水线 agent 末尾 yaml fence 不合法)
  - next_action / verdict 不在该 agent 枚举内,或 verdict != next_action(critic)
  - 分数越界(audience overall_score / 各维度)
  - critic scores[].severity 非 int 0-3,或据公式重算的 verdict 与声明不符
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent  # <repo>/.claude/hooks → <repo>
RUBRIC = REPO / ".claude/agents/critic-rubric.yaml"

ILOVEPPT_AGENTS = {
    "iloveppt-critic", "iloveppt-audience", "iloveppt-builder",
    "iloveppt-author", "iloveppt-brainstorm",
}

# next_action 枚举(来源:pipeline-protocol.md §4.2 / 各 agent return 契约)
NEXT_ACTION_ENUM = {
    "iloveppt-critic": {"pass", "pass_with_notes", "needs_revision"},
    "iloveppt-audience": {"delivered", "needs_author_rewrite", "needs_visual_redo", "needs_theme_fix"},
    "iloveppt-builder": {"dispatch_audience", "hard_stop"},
    "iloveppt-author": {
        "ask_user_for_outline_approval", "ask_user_for_content_approval",
        "dispatch_self_stage_d", "dispatch_critic",
    },
    "iloveppt-brainstorm": {"dispatch_author", "needs_self_revision", "ask_user"},
}


def _extract_text(resp) -> str:
    """从 tool_response(str / dict / content-block list)里抽出文本。"""
    if resp is None:
        return ""
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        for k in ("content", "text", "output", "result"):
            val = resp.get(k)
            if isinstance(val, str):
                return val
            if isinstance(val, list):
                return _extract_text(val)
        return ""
    if isinstance(resp, list):
        parts = []
        for item in resp:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts)
    return ""


def _extract_last_yaml_block(text: str) -> str | None:
    """抽末尾 ```yaml ... ``` fence;无则 None。"""
    blocks = re.findall(r"```ya?ml\s*\n(.*?)```", text, re.S | re.I)
    return blocks[-1] if blocks else None


def _load_critic_thresholds() -> dict:
    """从 critic-rubric.yaml 读 verdict 阈值(SSOT);读不到回落硬编码默认。"""
    try:
        data = yaml.safe_load(RUBRIC.read_text(encoding="utf-8")) or {}
        t = data.get("verdict_thresholds") or {}
        return {
            "block_severity": int(t.get("block_severity", 3)),
            "warn_accumulation": int(t.get("warn_accumulation", 5)),
            "notes_min_severity": int(t.get("notes_min_severity", 1)),
        }
    except Exception:
        return {"block_severity": 3, "warn_accumulation": 5, "notes_min_severity": 1}
```

- [ ] **Step 4: 跑测试确认 pass**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/hooks/test_validate_agent_return.py -k "extract or thresholds" -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
git add .claude/hooks/validate_agent_return.py tests/hooks/test_validate_agent_return.py
git commit -m "feat(hooks): validator 纯函数(文本/yaml/阈值)(P0-1 组件C)"
```

---

### Task C2: verdict 重算函数 + per-agent schema 校验

**Files:**
- Modify: `.claude/hooks/validate_agent_return.py`(加 `_recompute_verdict` + `validate_block`)
- Test: `tests/hooks/test_validate_agent_return.py`

- [ ] **Step 1: 写失败测试**

追加到 `tests/hooks/test_validate_agent_return.py`:

```python
def test_recompute_verdict():
    t = v._load_critic_thresholds()
    assert v._recompute_verdict([0, 0, 1], t) == "pass_with_notes"
    assert v._recompute_verdict([0, 0, 0], t) == "pass"
    assert v._recompute_verdict([0, 3, 1], t) == "needs_revision"
    assert v._recompute_verdict([2, 2, 2, 2, 2, 2], t) == "needs_revision"  # >5 个 2
    assert v._recompute_verdict([2, 2], t) == "pass_with_notes"


def test_validate_block_critic_ok():
    block = (
        "next_action: pass_with_notes\n"
        "verdict: pass_with_notes\n"
        "scores:\n"
        "  - {id: A1, severity: 0}\n"
        "  - {id: B9, severity: 1}\n"
        "  - {id: J5, severity: 2}\n"  # J5 不计入 → 不影响 verdict
    )
    code, msg = v.validate_block("iloveppt-critic", block)
    assert code == 0, msg


def test_validate_block_critic_verdict_mismatch_blocks():
    block = (
        "next_action: pass\n"
        "verdict: pass\n"
        "scores:\n"
        "  - {id: A6, severity: 3}\n"  # 有 block → 应 needs_revision,声明 pass → 拦
    )
    code, msg = v.validate_block("iloveppt-critic", block)
    assert code == 2
    assert "needs_revision" in msg


def test_validate_block_critic_severity_out_of_range_blocks():
    block = "next_action: pass\nverdict: pass\nscores:\n  - {id: A1, severity: 4}\n"
    code, msg = v.validate_block("iloveppt-critic", block)
    assert code == 2


def test_validate_block_critic_verdict_ne_next_action_blocks():
    block = "next_action: pass\nverdict: needs_revision\n"
    code, msg = v.validate_block("iloveppt-critic", block)
    assert code == 2


def test_validate_block_critic_no_scores_schema_only():
    # 无 scores → 只 schema 校验,不重算 → 合法枚举即放行
    block = "next_action: pass_with_notes\nverdict: pass_with_notes\n"
    code, msg = v.validate_block("iloveppt-critic", block)
    assert code == 0


def test_validate_block_audience_score_out_of_range_blocks():
    block = "next_action: delivered\noverall_score: 11\nverdict: excellent\n"
    code, msg = v.validate_block("iloveppt-audience", block)
    assert code == 2


def test_validate_block_audience_ok():
    block = (
        "next_action: delivered\noverall_score: 9\nverdict: excellent\n"
        "per_page_scores:\n  - {page: 1, comprehension_5s: 9, info_density: 8, visual_appeal: 9, flow_coherence: 8}\n"
    )
    code, msg = v.validate_block("iloveppt-audience", block)
    assert code == 0, msg


def test_validate_block_bad_yaml_blocks():
    code, msg = v.validate_block("iloveppt-critic", "next_action: [unclosed\n")
    assert code == 2


def test_validate_block_unknown_next_action_blocks():
    code, msg = v.validate_block("iloveppt-builder", "next_action: teleport\n")
    assert code == 2
```

- [ ] **Step 2: 跑测试确认 fail**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/hooks/test_validate_agent_return.py -k "recompute or validate_block" -v`
Expected: FAIL — `_recompute_verdict` / `validate_block` 未定义

- [ ] **Step 3: 实现 `_recompute_verdict` + `validate_block`**

追加到 `validate_agent_return.py`:

```python
# J5 是 advisory,不计入 verdict 重算(见 critic-rubric.yaml formula 注释 + 本计划偏离 #4)
_VERDICT_EXCLUDE_IDS = {"J5"}


def _recompute_verdict(severities: list[int], thresholds: dict) -> str:
    """按 critic-rubric.yaml 公式从整数 severity 列表算 verdict。"""
    block = thresholds["block_severity"]
    warn_cap = thresholds["warn_accumulation"]
    notes_min = thresholds["notes_min_severity"]
    if any(s == block for s in severities):
        return "needs_revision"
    if sum(1 for s in severities if s == 2) > warn_cap:
        return "needs_revision"
    if any(s >= notes_min for s in severities):
        return "pass_with_notes"
    return "pass"


def validate_block(agent: str, block: str) -> tuple[int, str]:
    """校验单个 handoff YAML block。返回 (exit_code, message)。0=放行 2=block。"""
    try:
        data = yaml.safe_load(block)
    except Exception as e:
        return 2, f"{agent} return YAML 解析失败: {e!r}"
    if not isinstance(data, dict):
        return 0, ""  # 非 dict 结构,保守放行

    na = data.get("next_action")
    enum = NEXT_ACTION_ENUM.get(agent, set())
    if na is not None and enum and na not in enum:
        return 2, f"{agent} next_action={na!r} 不在枚举 {sorted(enum)}"

    if agent == "iloveppt-critic":
        verdict = data.get("verdict")
        if verdict is not None and na is not None and verdict != na:
            return 2, f"critic verdict={verdict!r} 与 next_action={na!r} 不一致(应相等)"
        scores = data.get("scores")
        if isinstance(scores, list) and scores:
            sev: list[int] = []
            for item in scores:
                if not isinstance(item, dict):
                    continue
                s = item.get("severity")
                if not isinstance(s, int) or isinstance(s, bool) or not (0 <= s <= 3):
                    return 2, f"critic scores 项 {item.get('id')!r} severity={s!r} 必须是 int 0-3"
                if str(item.get("id")) not in _VERDICT_EXCLUDE_IDS:
                    sev.append(s)
            if sev:
                thresholds = _load_critic_thresholds()
                expected = _recompute_verdict(sev, thresholds)
                declared = verdict or na
                if declared and declared != expected:
                    return 2, (
                        f"critic verdict 公式重算={expected!r} 但声明={declared!r} "
                        f"(severity={sev}) — 改 verdict 或 复查 severity"
                    )
        return 0, ""

    if agent == "iloveppt-audience":
        sc = data.get("overall_score")
        if isinstance(sc, int) and not (0 <= sc <= 10):
            return 2, f"audience overall_score={sc} 越界(应 0-10)"
        pps = data.get("per_page_scores")
        if isinstance(pps, list):
            for pg in pps:
                if not isinstance(pg, dict):
                    continue
                for dim in ("comprehension_5s", "info_density", "visual_appeal", "flow_coherence"):
                    dv = pg.get(dim)
                    if isinstance(dv, int) and not (1 <= dv <= 10):
                        return 2, f"audience page {pg.get('page')} {dim}={dv} 越界(应 1-10)"
        return 0, ""

    return 0, ""  # builder/author/brainstorm:本版只校 next_action 枚举
```

- [ ] **Step 4: 跑测试确认 pass**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/hooks/test_validate_agent_return.py -k "recompute or validate_block" -v`
Expected: 全 PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
git add .claude/hooks/validate_agent_return.py tests/hooks/test_validate_agent_return.py
git commit -m "feat(hooks): verdict 重算 + per-agent schema 校验(P0-1 组件C)"
```

---

### Task C3: main() stdin 入口 + 顶层 gate 逻辑

**Files:**
- Modify: `.claude/hooks/validate_agent_return.py`(加 `main()` + `__main__`)
- Test: `tests/hooks/test_validate_agent_return.py`

- [ ] **Step 1: 写失败测试(子进程喂 stdin,断言 exit code)**

追加:

```python
import json as _json
import subprocess
import sys as _sys


def _run_hook(payload: dict):
    return subprocess.run(
        [_sys.executable, str(_HOOK)],
        input=_json.dumps(payload), text=True, capture_output=True,
    )


def test_main_non_iloveppt_agent_passes():
    r = _run_hook({"tool_input": {"subagent_type": "Explore"},
                   "tool_response": "```yaml\nnext_action: teleport\n```"})
    assert r.returncode == 0


def test_main_no_yaml_block_passes():
    r = _run_hook({"tool_input": {"subagent_type": "iloveppt-critic"},
                   "tool_response": "just prose, no fence"})
    assert r.returncode == 0


def test_main_critic_mismatch_blocks():
    resp = ("summary text\n```yaml\nnext_action: pass\nverdict: pass\n"
            "scores:\n  - {id: A6, severity: 3}\n```")
    r = _run_hook({"tool_input": {"subagent_type": "iloveppt-critic"}, "tool_response": resp})
    assert r.returncode == 2
    assert "needs_revision" in r.stderr


def test_main_malformed_stdin_passes():
    r = subprocess.run([_sys.executable, str(_HOOK)], input="not json",
                       text=True, capture_output=True)
    assert r.returncode == 0  # 防御性:解析不了的 stdin 不崩不拦
```

- [ ] **Step 2: 跑测试确认 fail**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/hooks/test_validate_agent_return.py -k main -v`
Expected: FAIL(main 未实现,no-yaml 等可能已偶然 0 但 mismatch 不会 block)

- [ ] **Step 3: 实现 main()**

追加到文件末尾:

```python
def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except Exception:
        return 0  # stdin 非 JSON:防御性放行,绝不因 hook 自身崩溃卡流水线
    if not isinstance(payload, dict):
        return 0

    tool_input = payload.get("tool_input") or {}
    agent = tool_input.get("subagent_type") if isinstance(tool_input, dict) else None
    if agent not in ILOVEPPT_AGENTS:
        return 0

    text = _extract_text(payload.get("tool_response"))
    block = _extract_last_yaml_block(text)
    if not block:
        return 0  # 无 yaml fence:保守放行

    try:
        code, msg = validate_block(agent, block)
    except Exception:
        return 0  # validator 自身异常:放行(绝不误杀)
    if code == 2:
        print(f"[gate] BLOCK · {msg}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 跑测试确认 pass**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest tests/hooks/test_validate_agent_return.py -v`
Expected: 全 PASS

- [ ] **Step 5: Commit**

```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
git add .claude/hooks/validate_agent_return.py tests/hooks/test_validate_agent_return.py
git commit -m "feat(hooks): main() stdin 入口 + 防御性放行(P0-1 组件C)"
```

---

### Task C4: critic 输出契约加 `scores` 块(critic.md + protocol + rubric 消歧)

**Files:**
- Modify: `.claude/agents/iloveppt-critic.md`(return schema 区,line 61-65 附近 + Step 3 verdict 区)
- Modify: `.claude/pipeline-protocol.md:614-635`(§4.3 critic 必加字段)
- Modify: `.claude/agents/critic-rubric.yaml`(formula 注释消歧 J5)

- [ ] **Step 1: pipeline-protocol §4.3 critic schema 加 `scores`**

在 `.claude/pipeline-protocol.md` critic 必加字段块(line 618 `next_action` 之后、`issues` 之前)插入:

```yaml
scores:                              # P0-1 · 机器可读 · validate_agent_return.py 据此重算 verdict
  - {id: A1, severity: 0}            # 21 项全列(A1-A7 + B1-B9 + J1-J5)· severity int 0-3
  # ...(其余 20 项)
  - {id: J5, severity: 0}            # J5 advisory · 不计入 verdict 重算
```

并在该块后加一行说明:
```
> `scores` 是 report .md 里 21 项量化 severity 的机器可读镜像;`issues`(high/med/low)是人读摘要。verdict 由 `scores` 按 critic-rubric.yaml 公式算(J5 除外)。
```

- [ ] **Step 2: critic.md 加填写指令**

在 `.claude/agents/iloveppt-critic.md` line 65(`next_action 取值即 verdict ...`)之后插入:

```markdown
**P0-1 · 必填 `scores` 块**:return YAML 除 `issues`(人读 high/med/low)外,**必须**再附一个机器可读 `scores: [{id, severity}]` 块,逐项列出 21 项(A1-A7 + B1-B9 + J1-J5)的整数 severity(0-3),与 report .md 里的量化结果一致。主线程 PostToolUse hook 据此按公式重算 verdict;声明的 verdict 与重算不符会被 **block**。J5 为 advisory,severity 照填但不计入 verdict 重算。
```

- [ ] **Step 3: critic-rubric.yaml formula 消歧**

把 `.claude/agents/critic-rubric.yaml` line 30-35 的 formula 注释改为:

```yaml
# verdict 自动算公式(critic.md Step 3 + validate_agent_return.py 引用):
#   适用范围:A1-A7 + B1-B9 + J1-J4(J5 是 advisory,severity 照填但**不计入** verdict 重算)
#   if any(s.severity == 3): verdict = "needs_revision"
#   elif count(s.severity == 2) > 5: verdict = "needs_revision"  # warn 累积亦 block
#   elif count(s.severity >= 1) >= 1: verdict = "pass_with_notes"
#   else: verdict = "pass"
```

- [ ] **Step 4: 校验改动不破坏 yaml + 现有 critic 测试(若有)**

Run:
```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
python -c "import yaml; yaml.safe_load(open('.claude/agents/critic-rubric.yaml')); print('rubric ok')"
python -m pytest tests/hooks/test_validate_agent_return.py -q
```
Expected: `rubric ok` + hook 测试全 PASS(`_load_critic_thresholds` 仍读到 3/5/1)

- [ ] **Step 5: Commit**

```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
git add .claude/agents/iloveppt-critic.md .claude/pipeline-protocol.md .claude/agents/critic-rubric.yaml
git commit -m "feat(critic): return YAML 加机器可读 scores 块 + J5 重算消歧(P0-1 组件C)"
```

---

### Task C5: 接入 settings.json + 历史返回零误杀验证

**Files:**
- Modify: `.claude/settings.json`(改前备份)

- [ ] **Step 1: dump 一次真实 PostToolUse stdin 确认字段名**

> Claude Code 不同版本 PostToolUse payload 字段可能不同。先临时加一个 dump-only hook 跑一次 Task,确认 `tool_input.subagent_type` 与 `tool_response` 的真实形态,再决定是否要调整 `_extract_text`。

Run(临时):在 `.claude/settings.json` 临时加一个 `PostToolUse` matcher=`Task` 的 hook,command 写 `cat > /tmp/posttooluse_sample.json`,触发一次任意 Task(如派个 Explore),然后:
```bash
cat /tmp/posttooluse_sample.json | python -m json.tool | head -40
```
Expected: 确认有 `tool_input.subagent_type` 与 `tool_response`。若字段名不同 → 回 Task C1 调 `_extract_text` / main() 取字段路径 + 补测试。

- [ ] **Step 2: 历史 critic 返回零误杀抽查**

> 真实历史报告是旧格式(无 scores),validator 对无 scores 只做 schema 校验。构造几个「合法旧返回」确认放行:

Run:
```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
python - <<'PY'
import importlib.util, json, subprocess, sys
HOOK = ".claude/hooks/validate_agent_return.py"
cases = [
  {"tool_input":{"subagent_type":"iloveppt-critic"},
   "tool_response":"ok\n```yaml\nnext_action: pass_with_notes\nverdict: pass_with_notes\nissues:\n  - severity: low\n```"},
  {"tool_input":{"subagent_type":"iloveppt-audience"},
   "tool_response":"```yaml\nnext_action: delivered\noverall_score: 9\nverdict: excellent\n```"},
]
for c in cases:
    r = subprocess.run([sys.executable, HOOK], input=json.dumps(c), text=True, capture_output=True)
    print(c["tool_input"]["subagent_type"], "->", r.returncode, r.stderr.strip())
    assert r.returncode == 0, "FALSE POSITIVE!"
print("no false positives")
PY
```
Expected: 两 case 都 `-> 0` + `no false positives`

- [ ] **Step 3: 备份 settings.json**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && cp .claude/settings.json .claude/settings.json.pre-p0-bak`

- [ ] **Step 4: 加 PostToolUse hook**

把 `.claude/settings.json` 的 `"hooks"` 对象从只含 `Stop` 改为同时含 `PostToolUse`(保留原 Stop 块不动):

```json
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "python \"${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/validate_agent_return.py\""
          }
        ]
      }
    ],
    "Stop": [
      ... (原内容不动) ...
    ]
  }
```

- [ ] **Step 5: 校验 settings.json 合法 JSON**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -c "import json; json.load(open('.claude/settings.json')); print('settings ok')"`
Expected: `settings ok`

- [ ] **Step 6: 删临时 dump hook + 备份文件,Commit**

```bash
cd /Users/pc2026/Documents/DevTools/iLovePPT
rm -f .claude/settings.json.pre-p0-bak /tmp/posttooluse_sample.json
git add .claude/settings.json
git commit -m "feat(hooks): 接入 PostToolUse return-YAML gate(P0-1 组件C)"
```

- [ ] **Step 7: 全量回归**

Run: `cd /Users/pc2026/Documents/DevTools/iLovePPT && python -m pytest -q | tail -3`
Expected: 全 PASS(含新增 hooks 测试)

---

## 整体验收

- [ ] `python -m pytest -q` 全绿(现有 192 + 新增 build_warnings + hooks 测试)
- [ ] `grep -rn "except Exception:$" .claude/skills/pptx-deck/builder/` 无裸静默 except
- [ ] CI yaml 合法 + 本地预验四 step 绿
- [ ] validator 历史返回零误杀;构造 verdict 算错能 block
- [ ] settings.json 合法 JSON,Stop telemetry 未被破坏
- [ ] 三组件各自独立 commit,conventional commits
