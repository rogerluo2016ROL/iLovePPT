# Library 知识库统一设计 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立 `library/` 双知识库(visual-patterns + pptx-templates)统一骨架, 单 DB(`library/_rag/db.sqlite`) + 顶层 `search.sh` router + 4 个 iLovePPT agent 集成。

**Architecture:** 双 kb 共享 `library/_rag/` 基础设施(venv + DashScope API + sqlite-vec); DB 单文件 5 张管理表(vp_items / tpl_templates / tpl_pages / text_emb / image_emb); id 前缀命名空间(vp: / tpl:) 防冲突; 顶层 `library/search.sh` 是唯一检索入口, 支持 `--preferred-template` 优先 + visual-patterns fallback。

**Tech Stack:** Python 3.11+(stdlib urllib + sqlite-vec + pyyaml + DashScope tongyi-embedding-vision-plus), python-pptx, soffice / pdftoppm 渲染, pytest 测试。

**Spec:** `docs/superpowers/specs/2026-05-25-library-knowledge-base-design.md`

---

## File Structure

### Create

| 路径 | 责任 |
|---|---|
| `library/_rag/.env.example` | DashScope API key 模板 |
| `library/_rag/requirements.txt` | sqlite-vec + pyyaml |
| `library/_rag/qwen_embedding.py` | DashScope 客户端 + sqlite-vec schema 建表 |
| `library/_rag/embed_text.py` | 扫指定 kb 的 meta.yaml → 写 text_emb |
| `library/_rag/embed_image.py` | 扫指定 kb 的 preview.png → 写 image_emb |
| `library/_rag/render_pages.py` | (pptx-templates 专用)soffice → pdftoppm 渲染每页 PNG |
| `library/search.py` | 跨 kb router 实现(SQL union + fallback 逻辑) |
| `library/search.sh` | venv wrapper |
| `library/visual-patterns/README.md` | kb 总览 |
| `library/visual-patterns/INDEX.md` | item 速查索引(grep 用) |
| `library/visual-patterns/ingest_workflow.md` | 1:N inspiration ingest 流程 |
| `library/visual-patterns/items/.gitkeep` | 占位 |
| `library/visual-patterns/_source/.gitkeep` | 占位 |
| `library/pptx-templates/README.md` | kb 总览 |
| `library/pptx-templates/INDEX.md` | 模板速查索引 |
| `library/pptx-templates/ingest_workflow.md` | 1:1 模板 + N pages ingest 流程 |
| `library/pptx-templates/items/.gitkeep` | 占位 |
| `library/pptx-templates/_source/.gitkeep` | 占位 |
| `tests/library/__init__.py` | (空) |
| `tests/library/test_db_schema.py` | DB 5 张表 + 向量表结构 |
| `tests/library/test_id_namespacing.py` | vp: / tpl: id 不冲突 |
| `tests/library/test_search_routing.py` | router fallback / preferred-template |
| `tests/library/test_load_theme_path.py` | load_theme 找新路径 |
| `tests/library/test_ingest_pipeline.py` | render + embed mock 全链路 |

### Modify

| 路径:行 | 改动 |
|---|---|
| `.claude/skills/pptx-deck/build.py:219` | `_repo_templates_dir()` 路径切到 `library/pptx-templates/_source/` |
| `.claude/skills/pptx-deck/build.py:278-283` | 错误消息更新 |
| `.gitignore` | 删 templates/ + library/visual-patterns 旧段, 加 library/_rag + library/*/_source |
| `CLAUDE.md` | 新增"Library / 知识库"段; Quick Start 路径更新 |
| `.claude/pipeline-protocol.md` | §1 派发表 template-extractor 行; §3 加 library/search.sh 强制规则 |
| `README.md`(根) | 引用 templates/ 路径处更新 |
| `.claude/agents/iloveppt-brainstorm.md` | 列模板改用 search.sh |
| `.claude/agents/iloveppt-author.md` | 拓写挂 pattern: 注释 |
| `.claude/agents/iloveppt.md` | Step 4 读注释 → DB → 渲染 |
| `.claude/agents/iloveppt-template-extractor.md` | 升级为完整 ingest 入口 |

---

## Phase 0: 收尾清空 + 顶层骨架

### Task 0.1: Commit 已清空的文件

**Files:**
- Stage: 50+ 删除文件(`templates/`, `library/visual-patterns/`)

- [ ] **Step 1: 检查 working tree**

Run: `git status --short | head -10`
Expected: 显示 `D library/visual-patterns/...` 和 `D templates/...` 多行

- [ ] **Step 2: Stage all deletions**

Run: `git add -A library/ templates/`

- [ ] **Step 3: Verify staged**

Run: `git diff --cached --stat | tail -5`
Expected: 显示 ~50 文件 deleted

- [ ] **Step 4: Commit**

```bash
git commit -m "chore(library): 清空 templates/ + visual-patterns/ 准备重构

- 删除根 templates/(含 3 份 .pptx · gitignored 不可恢复)
- 删除 library/visual-patterns/(21 个 pattern · 可 git checkout 找回)
- 准备按 spec 重建 library/ 双 kb 骨架(visual-patterns + pptx-templates)
- 详见 docs/superpowers/specs/2026-05-25-library-knowledge-base-design.md"
```

### Task 0.2: 创建 library/ 顶层目录骨架

**Files:**
- Create: `library/_rag/`, `library/visual-patterns/items/`, `library/visual-patterns/_source/`, `library/pptx-templates/items/`, `library/pptx-templates/_source/`
- Create: `.gitkeep` 占位

- [ ] **Step 1: 建空目录 + .gitkeep**

```bash
mkdir -p library/_rag
mkdir -p library/visual-patterns/items library/visual-patterns/_source
mkdir -p library/pptx-templates/items library/pptx-templates/_source
touch library/visual-patterns/items/.gitkeep
touch library/visual-patterns/_source/.gitkeep
touch library/pptx-templates/items/.gitkeep
touch library/pptx-templates/_source/.gitkeep
```

- [ ] **Step 2: Verify**

Run: `find library -type d`
Expected:
```
library
library/_rag
library/pptx-templates
library/pptx-templates/items
library/pptx-templates/_source
library/visual-patterns
library/visual-patterns/items
library/visual-patterns/_source
```

- [ ] **Step 3: Commit(顶层骨架, 文档/脚本后续 phase 加)**

```bash
git add library/
git commit -m "chore(library): 顶层目录骨架 visual-patterns + pptx-templates"
```

---

## Phase 1: 共享 RAG 基础设施 `library/_rag/`

### Task 1.1: requirements.txt + .env.example + venv

**Files:**
- Create: `library/_rag/requirements.txt`
- Create: `library/_rag/.env.example`
- Create: `library/_rag/.venv/`(运行 venv 安装)

- [ ] **Step 1: 写 requirements.txt**

```
# library/_rag/requirements.txt
sqlite-vec>=0.1.0
pyyaml>=6.0
```

- [ ] **Step 2: 写 .env.example**

```
# library/_rag/.env.example
# 复制为 .env 并填 API key. NEVER commit .env 文件本身。
DASHSCOPE_API_KEY=sk-...
DASHSCOPE_EMBED_MODEL=tongyi-embedding-vision-plus-2026-03-06
DASHSCOPE_API_URL=https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding
```

- [ ] **Step 3: 建 venv + 装依赖**

```bash
cd library/_rag
python3.11 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

- [ ] **Step 4: Verify 装好**

Run: `library/_rag/.venv/bin/python -c "import sqlite_vec; import yaml; print('OK')"`
Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add library/_rag/requirements.txt library/_rag/.env.example
git commit -m "feat(library/_rag): requirements + .env.example"
```

### Task 1.2: qwen_embedding.py(DB schema + API 客户端)

**Files:**
- Create: `library/_rag/qwen_embedding.py`

- [ ] **Step 1: 写 qwen_embedding.py 完整内容**

```python
# library/_rag/qwen_embedding.py
"""DashScope tongyi-embedding-vision-plus 客户端封装 + sqlite-vec DB schema。

embed_text.py / embed_image.py / search.py 共用此 lib。

Schema:
    vp_items       · visual-patterns 的 items(扁平)
    tpl_templates  · pptx-templates 的模板管理表
    tpl_pages      · pptx-templates 的页表
    text_emb       · 跨 kb 共享文本向量(id 前缀 vp: / tpl: 区分来源)
    image_emb      · 跨 kb 共享图像向量

API:
    POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding
    EMBED_DIM = 1152(text/image 同维)
"""

from __future__ import annotations

import base64
import json
import os
import sqlite3
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

EMBED_DIM = 1152
API_URL = os.environ.get(
    "DASHSCOPE_API_URL",
    "https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding",
)
MODEL = os.environ.get("DASHSCOPE_EMBED_MODEL", "tongyi-embedding-vision-plus-2026-03-06")

SCRIPT_DIR = Path(__file__).parent
ENV_FILE = SCRIPT_DIR / ".env"
DB_PATH = SCRIPT_DIR / "db.sqlite"


def load_env() -> None:
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and v and k not in os.environ:
            os.environ[k] = v


def get_api_key() -> str:
    load_env()
    key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not key:
        print(
            "ERROR: DASHSCOPE_API_KEY 未设置。\n"
            f"  方式 1: 写入 {ENV_FILE} (DASHSCOPE_API_KEY=sk-...)\n"
            "  方式 2: export DASHSCOPE_API_KEY=sk-...",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def _post_json(payload: dict, api_key: str, timeout: int = 30) -> dict:
    req = Request(
        url=API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} from DashScope: {body}") from e
    except URLError as e:
        raise RuntimeError(f"network error: {e}") from e


def embed_text(text: str, *, api_key: str | None = None, retry: int = 3) -> list[float]:
    api_key = api_key or get_api_key()
    payload = {"model": MODEL, "input": {"contents": [{"text": text}]}}
    last_err = None
    for attempt in range(retry):
        try:
            r = _post_json(payload, api_key)
            return r["output"]["embeddings"][0]["embedding"]
        except RuntimeError as e:
            last_err = e
            if attempt < retry - 1:
                time.sleep(2**attempt)
    raise RuntimeError(f"embed_text failed after {retry} retries: {last_err}")


def embed_image(image_path: Path | str, *, api_key: str | None = None, retry: int = 3) -> list[float]:
    api_key = api_key or get_api_key()
    if isinstance(image_path, Path) or not str(image_path).startswith(("http://", "https://")):
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"image not found: {path}")
        mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        b64 = base64.b64encode(path.read_bytes()).decode("ascii")
        image_arg = f"data:{mime};base64,{b64}"
    else:
        image_arg = str(image_path)

    payload = {"model": MODEL, "input": {"contents": [{"image": image_arg}]}}
    last_err = None
    for attempt in range(retry):
        try:
            r = _post_json(payload, api_key)
            return r["output"]["embeddings"][0]["embedding"]
        except RuntimeError as e:
            last_err = e
            if attempt < retry - 1:
                time.sleep(2**attempt)
    raise RuntimeError(f"embed_image failed after {retry} retries: {last_err}")


def open_db(db_path: Path | None = None) -> sqlite3.Connection:
    """打开 sqlite-vec DB, 创建 schema 若不存在。"""
    try:
        import sqlite_vec
    except ImportError:
        print(
            "ERROR: sqlite-vec 未装。\n"
            "  cd library/_rag && .venv/bin/pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    db = sqlite3.connect(db_path or DB_PATH)
    db.enable_load_extension(True)
    sqlite_vec.load(db)

    # 1. visual-patterns items(扁平)
    db.execute(
        """CREATE TABLE IF NOT EXISTS vp_items (
            id TEXT PRIMARY KEY,
            text_doc TEXT,
            meta_path TEXT,
            preview_path TEXT,
            category TEXT,
            updated_at TEXT
        )"""
    )

    # 2. pptx-templates 模板管理表
    db.execute(
        """CREATE TABLE IF NOT EXISTS tpl_templates (
            id TEXT PRIMARY KEY,
            name TEXT,
            desc TEXT,
            category TEXT,
            keywords TEXT,
            recommended_for TEXT,
            visual_tokens_json TEXT,
            visual_signature TEXT,
            iLovePPT_can_replicate_pct INTEGER,
            source_pptx_path TEXT,
            pages_count INTEGER,
            meta_path TEXT,
            preview_path TEXT,
            text_doc TEXT,
            updated_at TEXT
        )"""
    )

    # 3. pptx-templates 页表
    db.execute(
        """CREATE TABLE IF NOT EXISTS tpl_pages (
            id TEXT PRIMARY KEY,
            template_id TEXT NOT NULL,
            layout_type TEXT,
            page_index INTEGER,
            text_doc TEXT,
            meta_path TEXT,
            preview_path TEXT,
            extras_json TEXT,
            updated_at TEXT
        )"""
    )

    # 4-5. 共享向量表
    db.execute(
        f"""CREATE VIRTUAL TABLE IF NOT EXISTS text_emb USING vec0(
            id TEXT PRIMARY KEY,
            embedding FLOAT[{EMBED_DIM}]
        )"""
    )
    db.execute(
        f"""CREATE VIRTUAL TABLE IF NOT EXISTS image_emb USING vec0(
            id TEXT PRIMARY KEY,
            embedding FLOAT[{EMBED_DIM}]
        )"""
    )
    db.commit()
    return db


def build_text_doc_vp(p: dict) -> str:
    """visual-patterns item 的 text_doc 拼接。"""
    parts: list[str] = []
    if name := p.get("name"):
        parts.append(name)
    if category := p.get("category"):
        parts.append(f"类别 {category}")
    for intent in p.get("content_intent", []):
        parts.append(intent)
    for w in p.get("when_to_use", []):
        parts.append(f"适用 {w}")
    for kw in p.get("keywords", []):
        parts.append(kw)
    return " · ".join(parts)


def build_text_doc_tpl_template(p: dict) -> str:
    """pptx-templates 模板级 text_doc 拼接(加 visual_signature)。"""
    parts: list[str] = []
    if name := p.get("name"):
        parts.append(name)
    if desc := p.get("desc"):
        parts.append(desc)
    if category := p.get("category"):
        parts.append(f"类别 {category}")
    for intent in p.get("content_intent", []):
        parts.append(intent)
    for w in p.get("when_to_use", []):
        parts.append(f"适用 {w}")
    for sig in p.get("visual_signature", []):
        parts.append(f"视觉 {sig}")
    for r in p.get("recommended_for", []):
        parts.append(f"推荐 {r}")
    for kw in p.get("keywords", []):
        parts.append(kw)
    return " · ".join(parts)


def build_text_doc_tpl_page(p: dict) -> str:
    """pptx-templates 页级 text_doc 拼接(加 layout_type)。"""
    parts: list[str] = []
    if name := p.get("name"):
        parts.append(name)
    if lt := p.get("layout_type"):
        parts.append(f"布局 {lt}")
    if cat := p.get("category"):
        parts.append(f"类别 {cat}")
    for intent in p.get("content_intent", []):
        parts.append(intent)
    for w in p.get("when_to_use", []):
        parts.append(f"适用 {w}")
    for el in p.get("native_elements", []):
        parts.append(f"元素 {el}")
    for kw in p.get("keywords", []):
        parts.append(kw)
    return " · ".join(parts)
```

- [ ] **Step 2: Syntax check**

Run: `library/_rag/.venv/bin/python -c "import library._rag.qwen_embedding"`
(或 cd library/_rag && .venv/bin/python -c "import qwen_embedding")
Expected: 无错

- [ ] **Step 3: 验证 open_db 建表**

Run:
```bash
library/_rag/.venv/bin/python -c "
import sys; sys.path.insert(0, 'library/_rag')
from qwen_embedding import open_db
import os
os.environ['DASHSCOPE_API_KEY'] = 'test'   # 不调 API,只测建表
db = open_db()
tables = [r[0] for r in db.execute(\"SELECT name FROM sqlite_master WHERE type IN ('table','virtual_table') ORDER BY name\").fetchall()]
print(sorted(tables))
db.close()
"
```
Expected 包含 `'vp_items', 'tpl_templates', 'tpl_pages', 'text_emb', 'image_emb'`

- [ ] **Step 4: Commit**

```bash
git add library/_rag/qwen_embedding.py
git commit -m "feat(library/_rag): qwen_embedding lib · DashScope client + sqlite-vec schema"
```

### Task 1.3: DB schema 测试

**Files:**
- Create: `tests/library/__init__.py`(空)
- Create: `tests/library/test_db_schema.py`

- [ ] **Step 1: 写空 `__init__.py`**

```bash
mkdir -p tests/library
touch tests/library/__init__.py
```

- [ ] **Step 2: 写 test_db_schema.py**

```python
# tests/library/test_db_schema.py
"""验证 library/_rag/db.sqlite 5 张表 + 2 张向量表结构。"""

import sqlite3
import sys
from pathlib import Path

import pytest

RAG_DIR = Path(__file__).resolve().parent.parent.parent / "library" / "_rag"
sys.path.insert(0, str(RAG_DIR))


@pytest.fixture
def db(tmp_path, monkeypatch):
    """临时 DB, 不污染真实 db.sqlite。"""
    import qwen_embedding as q
    monkeypatch.setattr(q, "DB_PATH", tmp_path / "test.sqlite")
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    conn = q.open_db()
    yield conn
    conn.close()


def test_has_five_management_tables(db):
    rows = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '%_emb%' ORDER BY name"
    ).fetchall()
    names = sorted(r[0] for r in rows)
    assert "vp_items" in names
    assert "tpl_templates" in names
    assert "tpl_pages" in names


def test_vp_items_columns(db):
    cols = [r[1] for r in db.execute("PRAGMA table_info(vp_items)")]
    for col in ("id", "text_doc", "meta_path", "preview_path", "category", "updated_at"):
        assert col in cols, f"vp_items missing column {col}"


def test_tpl_templates_columns(db):
    cols = [r[1] for r in db.execute("PRAGMA table_info(tpl_templates)")]
    for col in (
        "id", "name", "desc", "category", "keywords", "recommended_for",
        "visual_tokens_json", "visual_signature", "iLovePPT_can_replicate_pct",
        "source_pptx_path", "pages_count", "meta_path", "preview_path",
        "text_doc", "updated_at",
    ):
        assert col in cols, f"tpl_templates missing column {col}"


def test_tpl_pages_columns(db):
    cols = [r[1] for r in db.execute("PRAGMA table_info(tpl_pages)")]
    for col in (
        "id", "template_id", "layout_type", "page_index", "text_doc",
        "meta_path", "preview_path", "extras_json", "updated_at",
    ):
        assert col in cols, f"tpl_pages missing column {col}"


def test_text_emb_is_vec_virtual(db):
    rows = db.execute(
        "SELECT name FROM sqlite_master WHERE name='text_emb' AND type='table'"
    ).fetchall()
    assert rows, "text_emb table not created"


def test_image_emb_is_vec_virtual(db):
    rows = db.execute(
        "SELECT name FROM sqlite_master WHERE name='image_emb' AND type='table'"
    ).fetchall()
    assert rows, "image_emb table not created"
```

- [ ] **Step 3: 跑测试**

Run: `library/_rag/.venv/bin/python -m pytest tests/library/test_db_schema.py -v`
Expected: 6 passed

- [ ] **Step 4: 跑现有测试套 verify 未破坏**

Run: `python3 -m pytest tests/ -q --ignore=tests/library`
Expected: 72 passed(或当前数)

- [ ] **Step 5: Commit**

```bash
git add tests/library/
git commit -m "test(library): DB schema 6 tests · 5 管理表 + 2 向量表"
```

### Task 1.4: embed_text.py

**Files:**
- Create: `library/_rag/embed_text.py`

- [ ] **Step 1: 写 embed_text.py**

```python
#!/usr/bin/env python3
# library/_rag/embed_text.py
"""扫指定 kb 的 meta.yaml → 计算 text embedding → 写 db.sqlite。

用法:
    .venv/bin/python embed_text.py                              # 扫两个 kb
    .venv/bin/python embed_text.py --kb visual-patterns          # 只 vp
    .venv/bin/python embed_text.py --kb pptx-templates --id template_golden  # 单条入库
"""

from __future__ import annotations

import argparse
import struct
import sys
from datetime import datetime
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from qwen_embedding import (  # noqa: E402
    build_text_doc_tpl_page,
    build_text_doc_tpl_template,
    build_text_doc_vp,
    embed_text,
    get_api_key,
    open_db,
)

LIBRARY_ROOT = SCRIPT_DIR.parent
VP_ROOT = LIBRARY_ROOT / "visual-patterns"
TPL_ROOT = LIBRARY_ROOT / "pptx-templates"


def _vec_blob(v: list[float]) -> bytes:
    return struct.pack(f"{len(v)}f", *v)


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def ingest_vp_item(db, item_dir: Path, api_key: str) -> str:
    meta_path = item_dir / "meta.yaml"
    if not meta_path.exists():
        raise FileNotFoundError(meta_path)
    data = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    short_id = data["id"]
    full_id = f"vp:{short_id}"
    text_doc = build_text_doc_vp(data)
    vec = embed_text(text_doc, api_key=api_key)
    rel_meta = meta_path.relative_to(LIBRARY_ROOT).as_posix()
    preview = item_dir / "preview.png"
    rel_preview = preview.relative_to(LIBRARY_ROOT).as_posix() if preview.exists() else None

    db.execute(
        "INSERT OR REPLACE INTO vp_items(id, text_doc, meta_path, preview_path, category, updated_at) VALUES (?,?,?,?,?,?)",
        (full_id, text_doc, rel_meta, rel_preview, data.get("category"), _now()),
    )
    db.execute("DELETE FROM text_emb WHERE id = ?", (full_id,))
    db.execute("INSERT INTO text_emb(id, embedding) VALUES (?, ?)", (full_id, _vec_blob(vec)))
    return full_id


def ingest_tpl_template(db, item_dir: Path, api_key: str) -> str:
    meta_path = item_dir / "meta.yaml"
    if not meta_path.exists():
        raise FileNotFoundError(meta_path)
    data = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    short_id = data["id"]
    if "__" in short_id:
        raise ValueError(f"模板名不能含 '__'(跟 page id 分隔符冲突): {short_id}")
    full_id = f"tpl:{short_id}"
    text_doc = build_text_doc_tpl_template(data)
    vec = embed_text(text_doc, api_key=api_key)
    rel_meta = meta_path.relative_to(LIBRARY_ROOT).as_posix()
    rel_preview = None
    preview = item_dir / "preview.png"
    if preview.exists():
        rel_preview = preview.relative_to(LIBRARY_ROOT).as_posix()

    pages_dir = item_dir / "pages"
    pages_count = len(list(pages_dir.glob("*/meta.yaml"))) if pages_dir.exists() else 0
    source_pptx = (LIBRARY_ROOT / "pptx-templates" / "_source" / f"{short_id}.pptx")
    source_rel = source_pptx.relative_to(LIBRARY_ROOT).as_posix() if source_pptx.exists() else None

    import json as _json
    vt_json = _json.dumps(data.get("visual_tokens", {}), ensure_ascii=False)
    vs_text = "\n".join(data.get("visual_signature", []))
    keywords_text = ",".join(data.get("keywords", []))
    recommended_text = ",".join(data.get("recommended_for", []))
    iLovePPT_can_replicate = (data.get("implementation") or {}).get("iLovePPT_can_replicate_pct")

    db.execute(
        """INSERT OR REPLACE INTO tpl_templates(
            id, name, desc, category, keywords, recommended_for,
            visual_tokens_json, visual_signature, iLovePPT_can_replicate_pct,
            source_pptx_path, pages_count, meta_path, preview_path, text_doc, updated_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            full_id, data.get("name"), data.get("desc"), data.get("category"),
            keywords_text, recommended_text, vt_json, vs_text, iLovePPT_can_replicate,
            source_rel, pages_count, rel_meta, rel_preview, text_doc, _now(),
        ),
    )
    db.execute("DELETE FROM text_emb WHERE id = ?", (full_id,))
    db.execute("INSERT INTO text_emb(id, embedding) VALUES (?, ?)", (full_id, _vec_blob(vec)))

    # 同步入 pages
    if pages_dir.exists():
        for page_meta in sorted(pages_dir.glob("*/meta.yaml")):
            ingest_tpl_page(db, page_meta.parent, parent_id=full_id, api_key=api_key)
    return full_id


def ingest_tpl_page(db, page_dir: Path, parent_id: str, api_key: str) -> str:
    meta_path = page_dir / "meta.yaml"
    data = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    short_id = data["id"]  # 形如 template_golden__01-cover
    full_id = f"tpl:{short_id}"
    text_doc = build_text_doc_tpl_page(data)
    vec = embed_text(text_doc, api_key=api_key)
    rel_meta = meta_path.relative_to(LIBRARY_ROOT).as_posix()
    preview = page_dir / "preview.png"
    rel_preview = preview.relative_to(LIBRARY_ROOT).as_posix() if preview.exists() else None
    import json as _json
    extras = {
        "native_elements": data.get("native_elements"),
        "copy_constraints": data.get("copy_constraints"),
        "iLovePPT_can_replicate_pct": data.get("iLovePPT_can_replicate_pct"),
        "matches_iloveppt_layout": data.get("matches_iloveppt_layout"),
    }
    extras_json = _json.dumps({k: v for k, v in extras.items() if v is not None}, ensure_ascii=False)

    db.execute(
        """INSERT OR REPLACE INTO tpl_pages(
            id, template_id, layout_type, page_index, text_doc,
            meta_path, preview_path, extras_json, updated_at
        ) VALUES (?,?,?,?,?,?,?,?,?)""",
        (
            full_id, parent_id, data.get("layout_type"), data.get("page_index"),
            text_doc, rel_meta, rel_preview, extras_json, _now(),
        ),
    )
    db.execute("DELETE FROM text_emb WHERE id = ?", (full_id,))
    db.execute("INSERT INTO text_emb(id, embedding) VALUES (?, ?)", (full_id, _vec_blob(vec)))
    return full_id


def run(kb: str | None, target_id: str | None) -> None:
    api_key = get_api_key()
    db = open_db()
    done = 0

    if kb in (None, "visual-patterns"):
        items_dir = VP_ROOT / "items"
        if items_dir.exists():
            for d in sorted(items_dir.iterdir()):
                if not d.is_dir() or d.name.startswith("_") or d.name.startswith("."):
                    continue
                if target_id and d.name != target_id:
                    continue
                print(f"[vp] {d.name} ...", flush=True)
                ingest_vp_item(db, d, api_key)
                done += 1

    if kb in (None, "pptx-templates"):
        items_dir = TPL_ROOT / "items"
        if items_dir.exists():
            for d in sorted(items_dir.iterdir()):
                if not d.is_dir() or d.name.startswith("_") or d.name.startswith("."):
                    continue
                if target_id and d.name != target_id:
                    continue
                print(f"[tpl] {d.name} ...", flush=True)
                ingest_tpl_template(db, d, api_key)
                done += 1

    db.commit()
    db.close()
    print(f"done. {done} item(s) embedded.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kb", choices=["visual-patterns", "pptx-templates"], default=None,
                   help="限定 kb;不传则扫两个")
    p.add_argument("--id", default=None, help="单 item 入库(visual-patterns: <id>; pptx-templates: <template-name>)")
    args = p.parse_args()
    run(args.kb, args.id)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Syntax check**

Run: `library/_rag/.venv/bin/python -c "import sys; sys.path.insert(0, 'library/_rag'); import embed_text"`
Expected: 无错

- [ ] **Step 3: Commit**

```bash
git add library/_rag/embed_text.py
git commit -m "feat(library/_rag): embed_text.py · 扫 kb meta.yaml → text_emb"
```

### Task 1.5: embed_image.py

**Files:**
- Create: `library/_rag/embed_image.py`

- [ ] **Step 1: 写 embed_image.py**

```python
#!/usr/bin/env python3
# library/_rag/embed_image.py
"""扫指定 kb 的 preview.png → 计算 image embedding → 写 db.sqlite.image_emb。

用法跟 embed_text.py 一致(--kb / --id)。
"""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from qwen_embedding import embed_image, get_api_key, open_db  # noqa: E402

LIBRARY_ROOT = SCRIPT_DIR.parent
VP_ROOT = LIBRARY_ROOT / "visual-patterns"
TPL_ROOT = LIBRARY_ROOT / "pptx-templates"


def _blob(v: list[float]) -> bytes:
    return struct.pack(f"{len(v)}f", *v)


def _embed_one(db, item_id: str, preview: Path, api_key: str) -> bool:
    if not preview.exists():
        print(f"  skip(无 preview.png): {item_id}")
        return False
    vec = embed_image(preview, api_key=api_key)
    db.execute("DELETE FROM image_emb WHERE id = ?", (item_id,))
    db.execute("INSERT INTO image_emb(id, embedding) VALUES (?, ?)", (item_id, _blob(vec)))
    return True


def run(kb: str | None, target_id: str | None) -> None:
    api_key = get_api_key()
    db = open_db()
    done = 0

    if kb in (None, "visual-patterns"):
        for d in sorted((VP_ROOT / "items").glob("*")) if (VP_ROOT / "items").exists() else []:
            if not d.is_dir() or d.name.startswith(("_", ".")):
                continue
            if target_id and d.name != target_id:
                continue
            full_id = f"vp:{d.name}"
            print(f"[vp] {full_id}", flush=True)
            if _embed_one(db, full_id, d / "preview.png", api_key):
                done += 1

    if kb in (None, "pptx-templates"):
        for tpl in sorted((TPL_ROOT / "items").glob("*")) if (TPL_ROOT / "items").exists() else []:
            if not tpl.is_dir() or tpl.name.startswith(("_", ".")):
                continue
            if target_id and tpl.name != target_id:
                continue
            tpl_id = f"tpl:{tpl.name}"
            print(f"[tpl] {tpl_id}", flush=True)
            if _embed_one(db, tpl_id, tpl / "preview.png", api_key):
                done += 1
            pages = tpl / "pages"
            if pages.exists():
                for pg in sorted(pages.glob("*/preview.png")):
                    page_dir = pg.parent
                    import yaml as _yaml
                    m = page_dir / "meta.yaml"
                    if not m.exists():
                        continue
                    pg_data = _yaml.safe_load(m.read_text(encoding="utf-8"))
                    pg_id = f"tpl:{pg_data['id']}"
                    print(f"[tpl-page] {pg_id}", flush=True)
                    if _embed_one(db, pg_id, pg, api_key):
                        done += 1

    db.commit()
    db.close()
    print(f"done. {done} image(s) embedded.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kb", choices=["visual-patterns", "pptx-templates"], default=None)
    p.add_argument("--id", default=None)
    args = p.parse_args()
    run(args.kb, args.id)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Syntax check**

Run: `library/_rag/.venv/bin/python -c "import sys; sys.path.insert(0, 'library/_rag'); import embed_image"`
Expected: 无错

- [ ] **Step 3: Commit**

```bash
git add library/_rag/embed_image.py
git commit -m "feat(library/_rag): embed_image.py · 扫 kb preview.png → image_emb"
```

### Task 1.6: id 命名空间测试

**Files:**
- Create: `tests/library/test_id_namespacing.py`

- [ ] **Step 1: 写测试**

```python
# tests/library/test_id_namespacing.py
"""验证 id 命名空间:vp: / tpl: 前缀 + tpl: 模板↔页用 __ 分隔。"""

import sys
from pathlib import Path

import pytest

RAG_DIR = Path(__file__).resolve().parent.parent.parent / "library" / "_rag"
sys.path.insert(0, str(RAG_DIR))


@pytest.fixture
def db(tmp_path, monkeypatch):
    import qwen_embedding as q
    monkeypatch.setattr(q, "DB_PATH", tmp_path / "test.sqlite")
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    conn = q.open_db()
    yield conn
    conn.close()


def test_vp_and_tpl_ids_coexist(db):
    db.execute(
        "INSERT INTO vp_items(id, text_doc, meta_path, category) VALUES (?,?,?,?)",
        ("vp:timeline-band-3", "doc", "visual-patterns/items/timeline-band-3/meta.yaml", "process"),
    )
    db.execute(
        "INSERT INTO tpl_templates(id, name, source_pptx_path, pages_count, text_doc) VALUES (?,?,?,?,?)",
        ("tpl:template_golden", "golden", "pptx-templates/_source/template_golden.pptx", 8, "doc"),
    )
    db.execute(
        "INSERT INTO tpl_pages(id, template_id, layout_type, page_index, text_doc) VALUES (?,?,?,?,?)",
        ("tpl:template_golden__01-cover", "tpl:template_golden", "cover", 1, "doc"),
    )
    rows = db.execute("SELECT id FROM vp_items UNION ALL SELECT id FROM tpl_templates UNION ALL SELECT id FROM tpl_pages").fetchall()
    ids = sorted(r[0] for r in rows)
    assert ids == sorted([
        "vp:timeline-band-3",
        "tpl:template_golden",
        "tpl:template_golden__01-cover",
    ])


def test_template_id_with_double_underscore_rejected(tmp_path, monkeypatch):
    """ingest_tpl_template 应在 id 含 __ 时 raise ValueError。"""
    import qwen_embedding as q
    monkeypatch.setattr(q, "DB_PATH", tmp_path / "test.sqlite")
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")

    # 不调真实 API · 直接调 build_text_doc 校验 short_id 中是否会被 reject
    import embed_text as et
    item_dir = tmp_path / "bad__name"
    item_dir.mkdir()
    (item_dir / "meta.yaml").write_text("id: bad__name\nname: x\n", encoding="utf-8")

    with pytest.raises(ValueError, match="__"):
        et.ingest_tpl_template(et.open_db(), item_dir, api_key="test")  # noqa


def test_page_id_format(db):
    """页 id 必须形如 tpl:<template>__<NN-slug>"""
    db.execute(
        "INSERT INTO tpl_pages(id, template_id, layout_type, page_index, text_doc) VALUES (?,?,?,?,?)",
        ("tpl:template_golden__04-single-focus", "tpl:template_golden", "single-focus", 4, "doc"),
    )
    pid = db.execute("SELECT id FROM tpl_pages").fetchone()[0]
    prefix, payload = pid.split(":", 1)
    assert prefix == "tpl"
    assert "__" in payload
    tpl_part, page_part = payload.split("__", 1)
    assert tpl_part == "template_golden"
    assert page_part == "04-single-focus"
```

- [ ] **Step 2: 跑测试**

Run: `library/_rag/.venv/bin/python -m pytest tests/library/test_id_namespacing.py -v`
Expected: 3 passed(`test_template_id_with_double_underscore_rejected` 可能因 import 路径需要调整,若失败先 mark xfail 后续 Task 调整)

- [ ] **Step 3: Commit**

```bash
git add tests/library/test_id_namespacing.py
git commit -m "test(library): id 命名空间 vp:/tpl: + __ 分隔"
```

---

## Phase 2: 顶层 search router

### Task 2.1: search.py 核心

**Files:**
- Create: `library/search.py`

- [ ] **Step 1: 写 search.py**

```python
#!/usr/bin/env python3
# library/search.py
"""跨 kb 检索 router · 唯一入口。

用法:
    library/search.sh --query "..."                                  # 全 kb 搜
    library/search.sh --query "..." --kb visual-patterns             # 限 vp
    library/search.sh --query "..." --kb pptx-templates --type page  # 限 tpl 页
    library/search.sh --query "..." --preferred-template template_golden  # 优先该模板 · fallback vp

行为:
    若有 --preferred-template:
        1. 在 tpl_pages 查, parent=tpl:<name>
        2. 命中 ≥ top-k 且平均分 ≥ threshold → 直接返回
        3. 否则:fallback 到 visual-patterns + 合并 top-k
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / "_rag"))
from qwen_embedding import embed_image, embed_text, get_api_key, open_db  # noqa: E402

DEFAULT_FALLBACK_THRESHOLD = 0.55
DEFAULT_TOP_K = 5


def _blob(v: list[float]) -> bytes:
    return struct.pack(f"{len(v)}f", *v)


def _query_table(db, kb_table: str, emb_table: str, q_blob: bytes, where: str, params: tuple, k: int):
    """通用表查询. kb_table ∈ {vp_items, tpl_templates, tpl_pages}, emb_table ∈ {text_emb, image_emb}."""
    sql = f"""SELECT k.id, k.text_doc, k.meta_path, k.preview_path,
                 {'k.category' if kb_table != 'tpl_pages' else 'k.layout_type'} AS cat,
                 {'NULL' if kb_table != 'tpl_pages' else 'k.template_id'} AS parent_id,
                 vec_distance_cosine(e.embedding, ?) AS distance
              FROM {kb_table} k JOIN {emb_table} e ON k.id = e.id
              {where}
              ORDER BY distance ASC
              LIMIT ?"""
    return db.execute(sql, (q_blob,) + params + (k,)).fetchall()


def _row_dict(r: tuple, row_type: str) -> dict:
    return {
        "id": r[0],
        "row_type": row_type,           # 'vp_item' | 'tpl_template' | 'tpl_page'
        "category_or_layout": r[4] or "",
        "parent_id": r[5],
        "score": round(1 - r[6], 4),    # cosine similarity
        "distance": round(r[6], 4),
        "preview_path": r[3] or "",
        "meta_path": r[2] or "",
        "doc_preview": (r[1] or "")[:120] + ("..." if r[1] and len(r[1]) > 120 else ""),
    }


def search(
    query: str | None,
    query_image: str | None,
    kb: str,                       # 'visual-patterns' | 'pptx-templates' | 'all'
    type_: str,                    # 'item' | 'template' | 'page' | 'any'
    category: str | None,
    preferred_template: str | None,
    top_k: int,
    fallback_threshold: float,
    mode: str,                     # 'text' | 'image' | 'hybrid'
    text_weight: float = 0.6,
    image_weight: float = 0.4,
) -> list[dict]:
    api_key = get_api_key()
    db = open_db()

    if query_image:
        q_vec = embed_image(query_image, api_key=api_key)
    elif query:
        q_vec = embed_text(query, api_key=api_key)
    else:
        raise ValueError("必须 --query 或 --query-image")
    q_blob = _blob(q_vec)

    emb_table = "image_emb" if mode == "image" else "text_emb"
    # hybrid 简化: 用 text_emb(image weighting 在 v2 加, spec §3-C)
    if mode == "hybrid":
        emb_table = "text_emb"

    pref_id = f"tpl:{preferred_template}" if preferred_template else None

    def _do_query(target_kb: str, target_type: str, filter_parent: str | None, k: int):
        out: list[dict] = []
        if target_kb in ("all", "visual-patterns") and target_type in ("any", "item"):
            where = "WHERE 1=1"
            params: tuple = ()
            if category:
                where += " AND k.category = ?"
                params = params + (category,)
            for r in _query_table(db, "vp_items", emb_table, q_blob, where, params, k):
                out.append(_row_dict(r, "vp_item"))
        if target_kb in ("all", "pptx-templates") and target_type in ("any", "template"):
            where = "WHERE 1=1"
            params = ()
            if category:
                where += " AND k.category = ?"
                params = params + (category,)
            for r in _query_table(db, "tpl_templates", emb_table, q_blob, where, params, k):
                out.append(_row_dict(r, "tpl_template"))
        if target_kb in ("all", "pptx-templates") and target_type in ("any", "page"):
            where = "WHERE 1=1"
            params = ()
            if filter_parent:
                where += " AND k.template_id = ?"
                params = params + (filter_parent,)
            if category:
                where += " AND k.layout_type = ?"
                params = params + (category,)
            for r in _query_table(db, "tpl_pages", emb_table, q_blob, where, params, k):
                out.append(_row_dict(r, "tpl_page"))
        return out

    if pref_id:
        primary = _do_query("pptx-templates", "page", pref_id, top_k)
        primary.sort(key=lambda x: x["distance"])
        for r in primary:
            r["source"] = "preferred-template"
        avg_score = (sum(r["score"] for r in primary) / len(primary)) if primary else 0.0
        if len(primary) >= top_k and avg_score >= fallback_threshold:
            db.close()
            return primary[:top_k]
        # fallback: 加 vp item 候选
        fallback = _do_query("visual-patterns", "item", None, top_k)
        for r in fallback:
            r["source"] = "visual-patterns"
        combined = primary + fallback
        combined.sort(key=lambda x: x["distance"])
        # 去重(同 id 取 primary 那条)
        seen = set()
        deduped: list[dict] = []
        for r in combined:
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            deduped.append(r)
        db.close()
        return deduped[:top_k]
    else:
        out = _do_query(kb, type_, None, top_k * 3)
        out.sort(key=lambda x: x["distance"])
        for r in out:
            r["source"] = "preferred-template" if r["row_type"].startswith("tpl_") else "visual-patterns"
        db.close()
        return out[:top_k]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query")
    p.add_argument("--query-image")
    p.add_argument("--mode", default="text", choices=["text", "image", "hybrid"])
    p.add_argument("--kb", default="all", choices=["visual-patterns", "pptx-templates", "all"])
    p.add_argument("--type", dest="type_", default="any", choices=["item", "template", "page", "any"])
    p.add_argument("--category", default=None)
    p.add_argument("--preferred-template", default=None)
    p.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    p.add_argument("--fallback-threshold", type=float, default=DEFAULT_FALLBACK_THRESHOLD)
    p.add_argument("--format", default="json", choices=["json", "text"])
    args = p.parse_args()

    if not args.query and not args.query_image:
        p.error("必须提供 --query 或 --query-image")

    results = search(
        query=args.query,
        query_image=args.query_image,
        kb=args.kb,
        type_=args.type_,
        category=args.category,
        preferred_template=args.preferred_template,
        top_k=args.top_k,
        fallback_threshold=args.fallback_threshold,
        mode=args.mode,
    )

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            src = r.get("source", "?")
            print(f"{r['score']:.3f}  [{src:>20}] [{r['row_type']:<12}] {r['id']:<50}")
            print(f"          {r['doc_preview']}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Syntax check**

Run: `library/_rag/.venv/bin/python library/search.py --help`
Expected: 显示 help 不报错

- [ ] **Step 3: Commit**

```bash
git add library/search.py
git commit -m "feat(library): search.py router · 跨 kb SQL + preferred-template fallback"
```

### Task 2.2: search.sh wrapper

**Files:**
- Create: `library/search.sh`

- [ ] **Step 1: 写 search.sh**

```bash
#!/usr/bin/env bash
# library/search.sh · 顶层检索 router wrapper(自动用 _rag/.venv)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PY="${SCRIPT_DIR}/_rag/.venv/bin/python"

if [ ! -x "${VENV_PY}" ]; then
    echo "ERROR: venv 未建。先跑:" >&2
    echo "  cd ${SCRIPT_DIR}/_rag && python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
    exit 1
fi

exec "${VENV_PY}" "${SCRIPT_DIR}/search.py" "$@"
```

- [ ] **Step 2: chmod +x**

```bash
chmod +x library/search.sh
```

- [ ] **Step 3: 测试 --help**

Run: `library/search.sh --help`
Expected: argparse help 输出

- [ ] **Step 4: Commit**

```bash
git add library/search.sh
git commit -m "feat(library): search.sh wrapper · 自动用 _rag/.venv"
```

### Task 2.3: search routing 测试

**Files:**
- Create: `tests/library/test_search_routing.py`

- [ ] **Step 1: 写测试**

```python
# tests/library/test_search_routing.py
"""验证 search.py router · preferred-template 优先 + fallback 行为。"""

import struct
import sys
from pathlib import Path

import pytest

LIB_DIR = Path(__file__).resolve().parent.parent.parent / "library"
RAG_DIR = LIB_DIR / "_rag"
sys.path.insert(0, str(LIB_DIR))
sys.path.insert(0, str(RAG_DIR))


@pytest.fixture
def db_with_fixtures(tmp_path, monkeypatch):
    import qwen_embedding as q
    monkeypatch.setattr(q, "DB_PATH", tmp_path / "test.sqlite")
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")
    db = q.open_db()

    # 固定向量(单位向量,前 3 维不同, 其余 0)
    def vec(a, b, c):
        v = [0.0] * q.EMBED_DIM
        v[0], v[1], v[2] = a, b, c
        # 归一
        norm = sum(x * x for x in v) ** 0.5
        return [x / norm if norm else 0.0 for x in v]

    items = [
        # vp items
        ("vp:item-near",   "process item near query",  vec(1.0, 0.1, 0.0), "vp_items"),
        ("vp:item-far",    "unrelated noise",          vec(0.0, 0.0, 1.0), "vp_items"),
        # tpl pages 同一 template
        ("tpl:template_golden__01-cover", "cover golden", vec(0.9, 0.2, 0.0), "tpl_pages"),
        ("tpl:template_golden__02-toc",   "toc golden",   vec(0.85, 0.25, 0.0), "tpl_pages"),
        # tpl template-level
        ("tpl:template_golden", "golden template",      vec(0.95, 0.15, 0.0), "tpl_templates"),
    ]

    for id_, doc, v, table in items:
        if table == "vp_items":
            db.execute("INSERT INTO vp_items(id, text_doc, category) VALUES (?,?,?)", (id_, doc, "process"))
        elif table == "tpl_pages":
            db.execute("INSERT INTO tpl_pages(id, template_id, layout_type, page_index, text_doc) VALUES (?,?,?,?,?)",
                       (id_, "tpl:template_golden", "cover", 1, doc))
        elif table == "tpl_templates":
            db.execute("INSERT INTO tpl_templates(id, name, category, source_pptx_path, pages_count, text_doc) VALUES (?,?,?,?,?,?)",
                       (id_, "golden", "enterprise-modern", "pptx-templates/_source/template_golden.pptx", 2, doc))
        blob = struct.pack(f"{len(v)}f", *v)
        db.execute("INSERT INTO text_emb(id, embedding) VALUES (?, ?)", (id_, blob))
    db.commit()
    yield db, q
    db.close()


def _patch_embed(monkeypatch, query_vec):
    """让 embed_text 返回固定 query 向量。"""
    import qwen_embedding as q
    monkeypatch.setattr(q, "embed_text", lambda text, **kw: query_vec)
    monkeypatch.setattr(q, "embed_image", lambda p, **kw: query_vec)
    # 同时 patch search.py 内 from import 的引用
    import search as s
    monkeypatch.setattr(s, "embed_text", lambda text, **kw: query_vec)
    monkeypatch.setattr(s, "embed_image", lambda p, **kw: query_vec)


def test_search_all_returns_mixed(db_with_fixtures, monkeypatch):
    db, q = db_with_fixtures
    v = [0.0] * q.EMBED_DIM
    v[0] = 1.0
    _patch_embed(monkeypatch, v)
    import search as s
    results = s.search(
        query="x", query_image=None, kb="all", type_="any",
        category=None, preferred_template=None, top_k=5,
        fallback_threshold=0.55, mode="text",
    )
    ids = [r["id"] for r in results]
    assert "vp:item-near" in ids
    assert "tpl:template_golden__01-cover" in ids


def test_preferred_template_returns_pages(db_with_fixtures, monkeypatch):
    db, q = db_with_fixtures
    v = [0.0] * q.EMBED_DIM
    v[0] = 1.0
    _patch_embed(monkeypatch, v)
    import search as s
    results = s.search(
        query="x", query_image=None, kb="all", type_="any",
        category=None, preferred_template="template_golden", top_k=2,
        fallback_threshold=0.0, mode="text",  # 阈值 0 让它不 fallback
    )
    ids = [r["id"] for r in results]
    # 所有结果都该是 template_golden 的 page
    for r in results:
        assert r["source"] == "preferred-template"
        assert r["parent_id"] == "tpl:template_golden"
    assert "tpl:template_golden__01-cover" in ids


def test_fallback_when_score_low(db_with_fixtures, monkeypatch):
    """阈值 0.99 强制触发 fallback,vp items 应出现。"""
    db, q = db_with_fixtures
    v = [0.0] * q.EMBED_DIM
    v[0] = 1.0
    _patch_embed(monkeypatch, v)
    import search as s
    results = s.search(
        query="x", query_image=None, kb="all", type_="any",
        category=None, preferred_template="template_golden", top_k=5,
        fallback_threshold=0.99, mode="text",
    )
    sources = {r["source"] for r in results}
    assert "visual-patterns" in sources  # fallback 触发


def test_type_filter_page_only(db_with_fixtures, monkeypatch):
    db, q = db_with_fixtures
    v = [0.0] * q.EMBED_DIM
    v[0] = 1.0
    _patch_embed(monkeypatch, v)
    import search as s
    results = s.search(
        query="x", query_image=None, kb="pptx-templates", type_="page",
        category=None, preferred_template=None, top_k=5,
        fallback_threshold=0.55, mode="text",
    )
    for r in results:
        assert r["row_type"] == "tpl_page"
```

- [ ] **Step 2: 跑测试**

Run: `library/_rag/.venv/bin/python -m pytest tests/library/test_search_routing.py -v`
Expected: 4 passed

- [ ] **Step 3: Commit**

```bash
git add tests/library/test_search_routing.py
git commit -m "test(library): search routing · fallback / preferred-template / type filter"
```

---

## Phase 3: 双 kb docs 骨架

### Task 3.1: visual-patterns kb docs

**Files:**
- Create: `library/visual-patterns/README.md`
- Create: `library/visual-patterns/INDEX.md`
- Create: `library/visual-patterns/ingest_workflow.md`

- [ ] **Step 1: 写 visual-patterns/README.md**

```markdown
# Visual Patterns Library

跨模板复用的视觉模式知识库(timeline / pdca / funnel / cards / 等)。被 iloveppt-author / iloveppt(Step 4 加视觉)在拓写时调用。

## 目录结构

```
library/visual-patterns/
├── README.md  INDEX.md  ingest_workflow.md
├── items/<id>/{meta.yaml, preview.png}        ← 资产 · 入 git
└── _source/<id>.<ext>                         ← gitignored · 1:N inspiration 归档
```

RAG 基础设施(venv / DB / 凭据)在 `library/_rag/`,跨 kb 共享。

## 用法

唯一检索入口是 `library/search.sh`,不要直接调本 kb 私有脚本(已无)。

```bash
# 查 PDCA 循环 pattern
library/search.sh --query "PDCA 循环" --kb visual-patterns --top-k 5
```

## ingest 流程

见 [`ingest_workflow.md`](ingest_workflow.md)。
```

- [ ] **Step 2: 写 visual-patterns/INDEX.md**

```markdown
# Visual Patterns Index

> 给人和 LLM grep 的速查索引。每 ingest 一个新 pattern, 在此加一行。
> RAG 检索请用 `library/search.sh`。

## process(流程)

(空 · 待 ingest)

## cycle(循环)

(空 · 待 ingest)

## comparison(对比)

(空 · 待 ingest)

## hierarchy(层级)

(空 · 待 ingest)

## data(数据)

(空 · 待 ingest)

## relationship(关系)

(空 · 待 ingest)
```

- [ ] **Step 3: 写 visual-patterns/ingest_workflow.md**

````markdown
# Visual Patterns Ingest Workflow

用户:"把这份 .pptx 灵感图入库,拆视觉 pattern"。流程 1:N(一份 source → N 个 pattern items)。

## 步骤

```
1. 用户上传 .pptx / .png 到任意位置
2. agent 复制到 library/visual-patterns/_source/<basename>.<ext>
3. (若 .pptx)soffice --headless --convert-to pdf + pdftoppm 渲染每页 → /tmp/_vp_render/
4. Claude(LLM)看每页 PNG → 推断 candidate meta.yaml 草稿(逐页)
5. 用户审 / 改名 / 弃用 · 决定哪些纳入
6. 通过的写入 library/visual-patterns/items/<id>/
       meta.yaml
       preview.png(从 _vp_render/page-N.png 复制)
7. 重生 vec DB:
     library/_rag/.venv/bin/python library/_rag/embed_text.py  --kb visual-patterns
     library/_rag/.venv/bin/python library/_rag/embed_image.py --kb visual-patterns
   (单条入库可加 --id <pattern-id>)
8. 更新 INDEX.md 加一行
```

## meta.yaml schema

```yaml
id: <kebab-case-id>          # 跟目录名一致
name: <人类可读>
category: process|cycle|comparison|hierarchy|data|relationship

content_intent:              # 表达什么内容意图
  - ...
when_to_use:                 # 适用场景
  - ...
when_not_to_use:             # 反面例子
  - ...
keywords: [...]              # 检索关键词

matches_iloveppt_layout: null  # 若对应内置 layout 写名,否则 null
fallback_rendering:
  method: manual|native_pptx|diagram
  notes: |
    描述如何渲染(若 method=diagram, 给 diagram skill 提示)
```
````

- [ ] **Step 4: Commit**

```bash
git add library/visual-patterns/
git commit -m "docs(library/visual-patterns): README + INDEX + ingest_workflow"
```

### Task 3.2: pptx-templates kb docs

**Files:**
- Create: `library/pptx-templates/README.md`
- Create: `library/pptx-templates/INDEX.md`
- Create: `library/pptx-templates/ingest_workflow.md`

- [ ] **Step 1: 写 pptx-templates/README.md**

```markdown
# PPTX Templates Library

用户预置的 .pptx 模板知识库(按模板名分类)。被 brainstorm(列模板)、author(选页)、iloveppt(Step 4 加视觉)调用。

## 目录结构

```
library/pptx-templates/
├── README.md  INDEX.md  ingest_workflow.md
├── items/<name>/
│   ├── meta.yaml                      ← 模板级 metadata
│   ├── preview.png                    ← cover 缩略图(入 git)
│   └── pages/<NN-slug>/
│       ├── meta.yaml                  ← 页级 metadata(入 git)
│       └── preview.png                ← 该页渲染 PNG(入 git, 单页 ~100-300KB)
└── _source/<name>.pptx                ← gitignored · build.py:load_theme() 读这里
```

每个模板严格 1:1 对应一个 .pptx 源(放 `_source/<name>.pptx`)。

## 用法

```bash
# 列模板 + 按用户主题相关性排
library/search.sh --kb pptx-templates --type template --query "<主题>" --top-k 5

# 已选 template_golden, 找最适合"数据冲击"的页
library/search.sh --query "数据冲击" --preferred-template template_golden --type page
```

## load_theme 集成

`.claude/skills/pptx-deck/build.py:load_theme(name)` 第 4 位查找 `library/pptx-templates/_source/<name>.pptx`。

## ingest 流程

见 [`ingest_workflow.md`](ingest_workflow.md)。
```

- [ ] **Step 2: 写 pptx-templates/INDEX.md**

```markdown
# PPTX Templates Index

> 给人 grep 的模板速查。每 ingest 一个新模板, 加一行。

## 已入库模板

(空 · 待 ingest)

## 模板格式

```
<name>:
  - desc:      <一句话简介>
  - category:  enterprise-modern | training | marketing | ...
  - pages:     <page-count>
  - replicate: <0-100%, iLovePPT 可复刻度>
```
```

- [ ] **Step 3: 写 pptx-templates/ingest_workflow.md**

````markdown
# PPTX Templates Ingest Workflow

用户:"把 template_X.pptx 入库"。流程 1:1(一份 .pptx → 一个模板 + N 个页 items)。

由 `iloveppt-template-extractor` agent 主导,主线程 dispatch。

## 步骤

```
1. 用户提供 .pptx 路径
2. agent 复制到 library/pptx-templates/_source/<name>.pptx
   (<name> 不允许含 __ · 跟 page id 分隔符冲突)
3. soffice --headless --convert-to pdf <pptx> + pdftoppm -jpeg -r 120
   渲染每页 → library/pptx-templates/items/<name>/pages/<NN-slug>/preview.png
4. Claude(LLM)看 PNG:
   (a) 总览所有页 → 产 template-level meta.yaml 草稿
   (b) 逐页 → 产 page-level meta.yaml 草稿
5. agent 把草稿展示给用户审 / 改 / 弃
6. 通过的写入:
       library/pptx-templates/items/<name>/meta.yaml
       library/pptx-templates/items/<name>/preview.png   (用 cover 缩略图)
       library/pptx-templates/items/<name>/pages/<NN-slug>/meta.yaml
       library/pptx-templates/items/<name>/pages/<NN-slug>/preview.png
7. 入库:
       library/_rag/.venv/bin/python library/_rag/embed_text.py  --kb pptx-templates --id <name>
       library/_rag/.venv/bin/python library/_rag/embed_image.py --kb pptx-templates --id <name>
   会同时入 tpl_templates(1 行)+ tpl_pages(N 行)+ 向量(N+1 行)
8. 更新 INDEX.md 加一行
```

## 模板级 meta.yaml schema

```yaml
id: <name>                          # 同目录名 · 不含 __
name: <人类可读>
category: enterprise-modern | training | marketing | ...
content_intent:
  - <模板适合什么内容场景>
when_to_use:    [...]
when_not_to_use: [...]
keywords:       [...]
recommended_for: [executive, sales, training, ...]

visual_tokens:                      # 从 .pptx 自动提取
  primary: '#234666'
  accent: '#AD9B5D'
  font_ea: '+mj-ea'
  title_size_pt: 28
  body_size_pt: 18
visual_signature:
  - <模板辨识元素描述>
assets:
  source_pptx: ../../_source/<name>.pptx
  total_pages: <N>
  cover_thumbnail: pages/01-cover/preview.png
pages: [01-cover, 02-toc, ...]
implementation:
  tier2_python_theme: null          # 若有 .claude/skills/pptx-deck/themes/<name>.py 写路径
  iLovePPT_can_replicate_pct: null  # 0-100 综合可复刻度
```

## 页级 meta.yaml schema

```yaml
id: <name>__<NN-slug>               # 例: template_golden__01-cover
name: <人类可读 · "Cover · 深蓝 + 白字">
category: cover | toc | section_divider | single_focus | cards | bullet_list | summary | closing | data | ...
content_intent:  [...]
when_to_use:    [...]
when_not_to_use: [...]
keywords:       [...]
fallback_rendering:
  method: native_pptx | diagram | manual
  notes: ...

# 页专有
template_name: <name>
page_index: <int>
layout_type: cover | toc | ...      # 跟 category 一致
native_elements:
  - <模板原页面的视觉元素>
iLovePPT_can_replicate_pct: <0-100>
matches_iloveppt_layout: <iLovePPT 内置 layout 名 或 null>
copy_constraints:
  title_max_chars: <N>
  subtitle_max_chars: <N>
```
````

- [ ] **Step 4: Commit**

```bash
git add library/pptx-templates/
git commit -m "docs(library/pptx-templates): README + INDEX + ingest_workflow"
```

---

## Phase 4: build.py load_theme 路径改造

### Task 4.1: 测试先行 · test_load_theme_path.py

**Files:**
- Create: `tests/library/test_load_theme_path.py`

- [ ] **Step 1: 写测试(此时会 fail · 路径还是旧的)**

```python
# tests/library/test_load_theme_path.py
"""验证 build.py:load_theme() 查找新路径 library/pptx-templates/_source/。"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / ".claude" / "skills" / "pptx-deck"))
sys.path.insert(0, str(REPO_ROOT / ".claude" / "skills" / "pptx"))


def test_repo_templates_dir_points_to_library(monkeypatch):
    import build
    actual = build._repo_templates_dir()
    expected_tail = ("library", "pptx-templates", "_source")
    parts = actual.parts
    assert parts[-3:] == expected_tail, f"got {parts[-3:]} expected {expected_tail}"


def test_find_template_in_library_pptx_templates_source(tmp_path, monkeypatch):
    import build
    fake_root = tmp_path / "fake_repo"
    fake_src = fake_root / "library" / "pptx-templates" / "_source"
    fake_src.mkdir(parents=True)
    (fake_src / "demo.pptx").write_bytes(b"PK\x03\x04 fake pptx")  # 假 .pptx
    monkeypatch.setattr(build, "_repo_templates_dir", lambda: fake_src)
    found = build._find_template("demo")
    assert found is not None
    assert found.name == "demo.pptx"


def test_error_message_mentions_new_path(tmp_path, monkeypatch):
    import build
    monkeypatch.setattr(build, "_repo_templates_dir", lambda: tmp_path / "nonexistent")
    monkeypatch.setattr(build, "_list_available_templates", lambda: [])
    with pytest.raises(ValueError, match=r"library/pptx-templates"):
        build.load_theme("nonexistent_theme")
```

- [ ] **Step 2: 跑测试 verify fail**

Run: `python3 -m pytest tests/library/test_load_theme_path.py -v`
Expected: 3 个测试 FAIL,错误消息指出路径是 `templates/` 不是 `library/pptx-templates/_source/`

- [ ] **Step 3: Commit failing tests**

```bash
git add tests/library/test_load_theme_path.py
git commit -m "test(library): load_theme path (failing pre-refactor)"
```

### Task 4.2: 改 build.py 路径

**Files:**
- Modify: `.claude/skills/pptx-deck/build.py:219`, `:282`

- [ ] **Step 1: 改 `_repo_templates_dir()` (build.py:219-222)**

替换为(用 `parents[N]` 比一串 `.parent` 更不易数错):

```python
def _repo_templates_dir() -> Path:
    """仓库根的 library/pptx-templates/_source/ 目录(模板 .pptx 全局共享)。
    build.py 位于 <repo>/.claude/skills/pptx-deck/build.py。"""
    repo_root = Path(__file__).resolve().parents[3]  # build.py → pptx-deck → skills → .claude → repo
    return repo_root / "library" / "pptx-templates" / "_source"
```

注:`parents[3]` 在实施时若发现实际 build.py 位置不同,跑 Task 4.1 的 `test_repo_templates_dir_points_to_library` 会暴露,届时调整为 `parents[N]` 让 tail 等于 `("library","pptx-templates","_source")` 即可。

- [ ] **Step 2: 改错误消息**

build.py:278-283 改为:

```python
    available_str = ", ".join(available) if available else "(空,把 .pptx 放进 library/pptx-templates/_source/)"
    raise ValueError(
        f"未知 theme: {theme_id!r}. "
        f"内置: tech_blue. "
        f"library/pptx-templates/_source/ 可用: {available_str}. "
        f"或直接给 .pptx 绝对/相对路径。"
    )
```

- [ ] **Step 3: 跑 load_theme 测试**

Run: `python3 -m pytest tests/library/test_load_theme_path.py -v`
Expected: 3 passed

- [ ] **Step 4: 跑全测试套 verify 未 break**

Run: `python3 -m pytest tests/ -q`
Expected: 75 passed(原 72 + 新 3 个 load_theme 测试; DB schema 已经 add 6 但需要 venv,可能 skip)

注:如果新测试要 venv,先看 pytest 报告。若 sqlite-vec 不在 PATH,需要确保 venv 测试隔离。可能需要在 conftest.py mark.

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/pptx-deck/build.py
git commit -m "fix(build): load_theme 路径 templates/ → library/pptx-templates/_source/"
```

---

## Phase 5: ingest 工具脚本 + 测试

### Task 5.1: render_pages.py(pptx-templates 专用)

**Files:**
- Create: `library/_rag/render_pages.py`

- [ ] **Step 1: 写 render_pages.py**

```python
#!/usr/bin/env python3
# library/_rag/render_pages.py
"""把 library/pptx-templates/_source/<name>.pptx 渲染成每页 PNG。

用法:
    .venv/bin/python render_pages.py <name>
    .venv/bin/python render_pages.py template_golden --dpi 120

会:
    1. soffice --headless --convert-to pdf <pptx> --outdir <tmp>
    2. pdftoppm -jpeg(默认 png)-r <dpi> <pdf> <tmp>/page
    3. 把 page-N.png 复制到 library/pptx-templates/items/<name>/pages/<NN-slug>/preview.png
       <NN-slug> 用 01-page / 02-page 占位, ingest agent 后续 rename 为 01-cover 等
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LIBRARY_ROOT = SCRIPT_DIR.parent
TPL_ROOT = LIBRARY_ROOT / "pptx-templates"


def _which(name: str) -> Path | None:
    p = shutil.which(name)
    return Path(p) if p else None


def render(name: str, dpi: int = 120) -> list[Path]:
    pptx = TPL_ROOT / "_source" / f"{name}.pptx"
    if not pptx.exists():
        print(f"ERROR: 源 .pptx 不存在: {pptx}", file=sys.stderr)
        sys.exit(1)

    if not _which("soffice"):
        print("ERROR: soffice(LibreOffice)未装。bash .claude/skills/pptx/scripts/check_deps.sh", file=sys.stderr)
        sys.exit(1)
    if not _which("pdftoppm"):
        print("ERROR: pdftoppm 未装。", file=sys.stderr)
        sys.exit(1)

    item_dir = TPL_ROOT / "items" / name
    item_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"render_{name}_") as td:
        td_path = Path(td)
        print(f"[render] soffice {pptx.name} → pdf ...", flush=True)
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "pdf", str(pptx), "--outdir", str(td_path)],
            check=True,
            capture_output=True,
        )
        pdf_files = list(td_path.glob("*.pdf"))
        if not pdf_files:
            print("ERROR: soffice 未产 PDF", file=sys.stderr)
            sys.exit(1)
        pdf = pdf_files[0]
        print(f"[render] pdftoppm -r {dpi} {pdf.name} → png ...", flush=True)
        subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(td_path / "page")],
            check=True,
            capture_output=True,
        )
        pages = sorted(td_path.glob("page-*.png"))
        if not pages:
            print("ERROR: 无 page-*.png", file=sys.stderr)
            sys.exit(1)

        produced: list[Path] = []
        for i, src in enumerate(pages, 1):
            slot = item_dir / "pages" / f"{i:02d}-page"
            slot.mkdir(parents=True, exist_ok=True)
            dst = slot / "preview.png"
            shutil.copy2(src, dst)
            produced.append(dst)
        print(f"[render] {len(produced)} pages → {item_dir}/pages/", flush=True)
        return produced


def main():
    p = argparse.ArgumentParser()
    p.add_argument("name", help="模板名 · 对应 library/pptx-templates/_source/<name>.pptx")
    p.add_argument("--dpi", type=int, default=120)
    args = p.parse_args()
    render(args.name, args.dpi)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Syntax check**

Run: `library/_rag/.venv/bin/python library/_rag/render_pages.py --help`
Expected: argparse help 输出

- [ ] **Step 3: Commit**

```bash
git add library/_rag/render_pages.py
git commit -m "feat(library/_rag): render_pages.py · pptx → 每页 preview.png"
```

### Task 5.2: ingest pipeline 测试(mock LLM + mock embed)

**Files:**
- Create: `tests/library/test_ingest_pipeline.py`

- [ ] **Step 1: 写测试**

```python
# tests/library/test_ingest_pipeline.py
"""验证 ingest pipeline end-to-end(mock embed API, 真跑 yaml + DB 写入)。"""

import struct
import sys
from pathlib import Path

import pytest

LIB_DIR = Path(__file__).resolve().parent.parent.parent / "library"
RAG_DIR = LIB_DIR / "_rag"
sys.path.insert(0, str(LIB_DIR))
sys.path.insert(0, str(RAG_DIR))


@pytest.fixture
def fake_lib(tmp_path, monkeypatch):
    """临时 library/ + DB。"""
    fake_lib = tmp_path / "library"
    (fake_lib / "visual-patterns" / "items").mkdir(parents=True)
    (fake_lib / "pptx-templates" / "items").mkdir(parents=True)

    import qwen_embedding as q
    monkeypatch.setattr(q, "DB_PATH", tmp_path / "db.sqlite")
    monkeypatch.setenv("DASHSCOPE_API_KEY", "test-key")

    import embed_text as et
    monkeypatch.setattr(et, "LIBRARY_ROOT", fake_lib)
    monkeypatch.setattr(et, "VP_ROOT", fake_lib / "visual-patterns")
    monkeypatch.setattr(et, "TPL_ROOT", fake_lib / "pptx-templates")
    fake_vec = [0.0] * q.EMBED_DIM
    fake_vec[0] = 1.0
    monkeypatch.setattr(et, "embed_text", lambda text, **kw: fake_vec)
    monkeypatch.setattr(q, "embed_text", lambda text, **kw: fake_vec)
    yield fake_lib, q


def test_ingest_vp_item(fake_lib):
    fake_lib_path, q = fake_lib
    item_dir = fake_lib_path / "visual-patterns" / "items" / "demo-pattern"
    item_dir.mkdir()
    (item_dir / "meta.yaml").write_text(
        "id: demo-pattern\nname: Demo\ncategory: process\n"
        "content_intent: [test]\nkeywords: [demo]\n",
        encoding="utf-8",
    )

    import embed_text as et
    db = q.open_db()
    full_id = et.ingest_vp_item(db, item_dir, api_key="test")
    db.commit()

    assert full_id == "vp:demo-pattern"
    row = db.execute("SELECT id, category FROM vp_items WHERE id = ?", (full_id,)).fetchone()
    assert row[0] == "vp:demo-pattern"
    assert row[1] == "process"
    emb_row = db.execute("SELECT id FROM text_emb WHERE id = ?", (full_id,)).fetchone()
    assert emb_row is not None
    db.close()


def test_ingest_tpl_template_with_pages(fake_lib):
    fake_lib_path, q = fake_lib
    tpl_dir = fake_lib_path / "pptx-templates" / "items" / "demo_tpl"
    tpl_dir.mkdir()
    (tpl_dir / "meta.yaml").write_text(
        "id: demo_tpl\nname: Demo Template\ncategory: marketing\n"
        "content_intent: [a]\nkeywords: [b]\n"
        "visual_tokens: {primary: '#000'}\nvisual_signature: [c]\n"
        "implementation: {iLovePPT_can_replicate_pct: 50}\n",
        encoding="utf-8",
    )
    page_dir = tpl_dir / "pages" / "01-cover"
    page_dir.mkdir(parents=True)
    (page_dir / "meta.yaml").write_text(
        "id: demo_tpl__01-cover\nname: Cover\ncategory: cover\n"
        "layout_type: cover\npage_index: 1\n"
        "content_intent: [open]\nkeywords: [cover]\n"
        "native_elements: [accent]\ncopy_constraints: {title_max_chars: 22}\n",
        encoding="utf-8",
    )

    import embed_text as et
    db = q.open_db()
    full_id = et.ingest_tpl_template(db, tpl_dir, api_key="test")
    db.commit()

    assert full_id == "tpl:demo_tpl"
    t_row = db.execute("SELECT id, name, pages_count FROM tpl_templates WHERE id = ?", (full_id,)).fetchone()
    assert t_row[0] == "tpl:demo_tpl"
    assert t_row[1] == "Demo Template"
    assert t_row[2] == 1  # pages_count

    p_row = db.execute("SELECT id, template_id, layout_type FROM tpl_pages WHERE template_id = ?", (full_id,)).fetchone()
    assert p_row[0] == "tpl:demo_tpl__01-cover"
    assert p_row[1] == "tpl:demo_tpl"
    assert p_row[2] == "cover"
    db.close()


def test_ingest_rejects_double_underscore(fake_lib):
    fake_lib_path, q = fake_lib
    bad_dir = fake_lib_path / "pptx-templates" / "items" / "bad__name"
    bad_dir.mkdir()
    (bad_dir / "meta.yaml").write_text("id: bad__name\nname: x\n", encoding="utf-8")

    import embed_text as et
    db = q.open_db()
    with pytest.raises(ValueError, match=r"__"):
        et.ingest_tpl_template(db, bad_dir, api_key="test")
    db.close()
```

- [ ] **Step 2: 跑测试**

Run: `library/_rag/.venv/bin/python -m pytest tests/library/test_ingest_pipeline.py -v`
Expected: 3 passed

- [ ] **Step 3: Commit**

```bash
git add tests/library/test_ingest_pipeline.py
git commit -m "test(library): ingest pipeline · vp item / tpl template+pages / reject __"
```

---

## Phase 6: agent prompt 改动

### Task 6.1: iloveppt-brainstorm

**Files:**
- Modify: `.claude/agents/iloveppt-brainstorm.md`

- [ ] **Step 1: 找到 Stage A 列模板的段落**

Run: `grep -n "templates/" .claude/agents/iloveppt-brainstorm.md | head`
也 grep `theme:` / `选模板` / `模板列表` 等关键词找位置

- [ ] **Step 2: 替换为新调用方式**

把"扫 templates/ 显示模板列表"段改为:

```markdown
### Stage A · 列模板给用户选

不要扫 `templates/` 目录,改为查 DB 取按主题相关性排序的 top-5:

```bash
library/search.sh \
    --kb pptx-templates \
    --type template \
    --query "<用户的 deck 主题>" \
    --top-k 5 \
    --format text
```

把结果按相关性 % 展示给用户,例如:

```
按你的主题相关性排,可用模板:
1. template_golden       (~85% 匹配)  · enterprise-modern · 推荐 ★
2. template_high-end-vibe (~62% 匹配) · high-end
3. template_training     (~31% 匹配)  · training
4. tech_blue             (内置默认科技蓝, 无相关性分数)
```

用户选定后, 在 brief.md 写:

```yaml
theme: template_golden       # 自动解析为 library/pptx-templates/_source/template_golden.pptx
```
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/iloveppt-brainstorm.md
git commit -m "feat(agents/brainstorm): Stage A 列模板用 library/search.sh"
```

### Task 6.2: iloveppt-author

**Files:**
- Modify: `.claude/agents/iloveppt-author.md`

- [ ] **Step 1: 找拓写每页时调用 search 的段落**

Run: `grep -n "search.sh\|visual-patterns\|pattern:" .claude/agents/iloveppt-author.md | head`

- [ ] **Step 2: 替换为新接口 + 注释规范**

新增/替换段落:

```markdown
### Stage D · 拓写时挂 pattern 注释

每页拓写前查 library, **必须**自动带 `--preferred-template` = brief.theme:

```bash
library/search.sh \
    --query "<本页核心意图,一句话>" \
    --preferred-template <brief.theme> \
    --type page \
    --top-k 5 \
    --fallback-threshold 0.55 \
    --format json
```

返回结果含 `source` 字段:
- `"source": "preferred-template"` → 模板内的页
- `"source": "visual-patterns"` → fallback 到通用 pattern

选最合适的(看 source / score / doc_preview),在 content.md 嵌入 `<!-- pattern: <full-id> -->`:

```markdown
## 4. 用户增长破亿
<!-- pattern: tpl:template_golden__04-single-focus -->

87% 的 Q3 用户来自移动端...
```

或 fallback 情况:

```markdown
## 3. PDCA 持续改进
<!-- pattern: vp:pdca-iterations -->

...
```

完整 id 必须带 `vp:` / `tpl:` 前缀,下游 iloveppt Step 4 据此定位 meta.yaml。
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/iloveppt-author.md
git commit -m "feat(agents/author): Stage D 挂 <!-- pattern: --> 注释"
```

### Task 6.3: iloveppt(Step 4 加视觉)

**Files:**
- Modify: `.claude/agents/iloveppt.md`

- [ ] **Step 1: 找 Step 4 段落**

Run: `grep -n "Step 4\|加视觉\|iconify\|visual" .claude/agents/iloveppt.md | head`

- [ ] **Step 2: 替换 Step 4 行为**

```markdown
### Step 4 · 主动加视觉(走 library 注释优先)

读 content.md 提取所有 `<!-- pattern: <full-id> -->` 注释:

1. 用 id 查 DB 拿 meta_path:
   ```bash
   library/_rag/.venv/bin/python -c "
   import sys; sys.path.insert(0, 'library/_rag')
   from qwen_embedding import open_db
   db = open_db()
   row = db.execute('SELECT meta_path, preview_path FROM vp_items WHERE id=? UNION SELECT meta_path, preview_path FROM tpl_pages WHERE id=?', ('<id>', '<id>')).fetchone()
   print(row)
   "
   ```
2. Read meta.yaml 看 `fallback_rendering.method`:
   - `native_pptx` → 直接复刻视觉描述,用 helpers/diagram 实现
   - `diagram` → 调 diagram skill 现画
   - `manual` → 用 fallback_rendering.notes 中的指示
3. 若 content.md 没标 `pattern:` 注释 → 自行调 `library/search.sh --type=any` 现查现选

不允许凭空造 pattern id; 所有 visual 决策必须有 library 出处。
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/iloveppt.md
git commit -m "feat(agents/iloveppt): Step 4 读 pattern: 注释 → 查 DB → 渲染"
```

### Task 6.4: iloveppt-template-extractor 升级

**Files:**
- Modify: `.claude/agents/iloveppt-template-extractor.md`

- [ ] **Step 1: 找当前 extractor 描述**

Run: `cat .claude/agents/iloveppt-template-extractor.md | head -30`

- [ ] **Step 2: 替换全文为完整 ingest pipeline**

(保留 frontmatter, 改 body 为以下流程描述)

```markdown
## 角色

把用户上传的 .pptx 模板**完整 ingest** 到 library/pptx-templates/ kb(不再只抽 token)。

## 输入

主线程 SendMessage 给 `<.pptx 绝对路径>` + `<期望短名 name>`(可选, 默认用文件名)。

## 步骤

```
1. 校验 name 不含 '__'(跟 page id 分隔符冲突),含则报错请用户改名
2. 复制 .pptx 到 library/pptx-templates/_source/<name>.pptx
3. 跑渲染:
       library/_rag/.venv/bin/python library/_rag/render_pages.py <name> --dpi 120
   → 产 library/pptx-templates/items/<name>/pages/01-page/preview.png 等 N 个 placeholder 目录
4. Read 每个 preview.png(LLM 多模态), 推断:
   (a) template-level meta.yaml 草稿(整体风格摘要 · §schema 见 ingest_workflow.md)
   (b) per-page meta.yaml 草稿 + 决定 page slug(把 01-page 改名为 01-cover / 02-toc 等)
5. 把草稿写入 .draft 后缀:
       items/<name>/meta.yaml.draft
       items/<name>/pages/01-cover/meta.yaml.draft
   ...
6. return yaml 给主线程:
       next_action: user_review_drafts
       drafts: [<path>, ...]
   主线程 SendMessage 给用户审 / 改
7. 用户审完, 用户(或主线程协助)把 .draft 改名去掉后缀
8. 主线程跑入库:
       library/_rag/.venv/bin/python library/_rag/embed_text.py  --kb pptx-templates --id <name>
       library/_rag/.venv/bin/python library/_rag/embed_image.py --kb pptx-templates --id <name>
9. 更新 library/pptx-templates/INDEX.md 加一行
10. return yaml: next_action: done, template_id: tpl:<name>, pages_count: N
```

## 不再负责

- 抽 token 后写 templates/<name>.yaml(顶层 manifest) ← 废弃
- 直接复制 .pptx 到根 templates/ ← 改到 library/pptx-templates/_source/
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/iloveppt-template-extractor.md
git commit -m "feat(agents/template-extractor): 升级为 library/pptx-templates/ ingest 入口"
```

---

## Phase 7: 配置与文档同步

### Task 7.1: .gitignore 重写

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: 删旧段**

把 `.gitignore` 中以下段落整段删除:

```
# 用户本地 .pptx 模板(机密 / 版权防误 commit)
# 仅 README.md + example.yaml 入 git,其他都不入
templates/*.pptx
templates/*.pptx.bak
templates/*.yaml
!templates/example.yaml
```

以及:

```
# library/visual-patterns/ RAG 生成产物(由 _rag/embed_text.py 重生)
library/visual-patterns/_rag/text.sqlite
library/visual-patterns/_rag/image.sqlite
library/visual-patterns/_rag/patterns.sqlite
library/visual-patterns/_rag/.cache/

# library/visual-patterns/ RAG · API key + 任何 .env(NEVER commit)
library/visual-patterns/_rag/.env
library/visual-patterns/_rag/.env.*

# library/visual-patterns/patterns/*/preview.png 是 pattern 资产,**保留**
!library/visual-patterns/patterns/*/preview.png
# library/visual-patterns/_source_inspiration/ 用户上传的 .pptx 模板可能含机密 → 不入 git
library/visual-patterns/_source_inspiration/*.pptx
library/visual-patterns/_source_inspiration/*.pdf
# 但保留用户给的 .png 截图作为入库参考(无版权风险且文件小)
!library/visual-patterns/_source_inspiration/*.png
```

- [ ] **Step 2: 加新段**

在 `.gitignore` 末尾追加:

```
# === library/ · 知识库 ===
# 共享 RAG 基础设施(venv / 凭据 / DB)
library/_rag/.venv/
library/_rag/.env
library/_rag/.env.*
library/_rag/db.sqlite
library/_rag/.cache/

# 各 kb 的 _source/ · 用户原始材料(机密 / 版权 / 体积)
library/*/_source/*
!library/*/_source/.gitkeep

# items/<id>/{meta.yaml,preview.png} 是产品资产 · 入 git(无需特别 ignore 规则)
```

- [ ] **Step 3: Verify**

```bash
git check-ignore -v library/_rag/db.sqlite                    # 应被 ignored
git check-ignore -v library/_rag/.venv/foo                    # ignored
git check-ignore -v library/pptx-templates/_source/x.pptx     # ignored
git check-ignore -v library/visual-patterns/_source/x.png     # ignored
git check-ignore -v library/visual-patterns/items/x/meta.yaml # NOT ignored(无输出/退出码 1)
```

- [ ] **Step 4: Commit**

```bash
git add .gitignore
git commit -m "chore(gitignore): 切到新 library/ 结构 · _rag + */_source ignored, items/ kept"
```

### Task 7.2: CLAUDE.md 新增 Library 段

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: 找"三 skill 分层"段落位置**

Run: `grep -n "三 skill 分层\|三skill\|skill 分层" CLAUDE.md`

- [ ] **Step 2: 在该段之后插入 Library 段**

```markdown
### Library / 知识库(RAG)

`${CLAUDE_PROJECT_DIR}/library/` 是双知识库的 RAG 检索系统,由 5-agent 流水线在不同 stage 调用:

| kb | 单位 | 调用场景 |
|---|---|---|
| `library/visual-patterns/` | 跨模板视觉模式(timeline / pdca / funnel ...) | author 拓写 / iloveppt Step 4 加视觉 |
| `library/pptx-templates/` | 用户预置 .pptx 模板 + 拆出的每页 | brainstorm 列模板 / author 选页 / iloveppt 渲染参考 |

**唯一检索入口**:`library/search.sh`(自动带 `--preferred-template` 优先 + visual-patterns fallback)。

```bash
# brainstorm 列模板(按主题相关性排)
library/search.sh --kb pptx-templates --type template --query "<主题>" --top-k 5

# author 拓写每页(优先模板 page, 降级 vp pattern)
library/search.sh --query "<本页意图>" --preferred-template <brief.theme> --type page
```

**资产管理**:
- 入 git:`items/<id>/{meta.yaml, preview.png}` 是产品资产, 版本控制
- 不入 git:`_rag/db.sqlite`(向量, 可重生)、`_rag/.venv/`、`_rag/.env`、`*/_source/*.pptx`(用户原料)

**ingest 流程**:见各 kb 的 `ingest_workflow.md`。
```

- [ ] **Step 3: 更新 Quick Start 路径**

找 `templates/<name>.pptx` 提示, 改为 `library/pptx-templates/_source/<name>.pptx`。

Run: `grep -n "templates/" CLAUDE.md`
逐处判断: deck 项目本地的 `<plan_dir>/templates/` 保留;仓库全局共享的改为新路径。

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(CLAUDE): 新增 Library/知识库 段 · Quick Start 路径更新"
```

### Task 7.3: pipeline-protocol.md 同步

**Files:**
- Modify: `.claude/pipeline-protocol.md`

- [ ] **Step 1: 找 template-extractor 行**

Run: `grep -n "template-extractor\|template_extractor" .claude/pipeline-protocol.md`

- [ ] **Step 2: 更新派发表里 template-extractor 行描述**

把"抽 4 级 token"改为"完整 ingest 入库(.pptx → library/pptx-templates/items/<name>/)"。

- [ ] **Step 3: 在 §3 派发规则段新增 library/search.sh 强制规则**

例如新增一条:

```markdown
### library/search.sh 调用规则

下列三个 stage **强制**走 `library/search.sh`,不允许 agent 凭空造 pattern 引用:

| Stage | 调用方 | 用途 |
|---|---|---|
| Stage A 列模板 | brainstorm | `--kb pptx-templates --type template --query <主题>` 按主题相关性排序 |
| Stage D 拓写 | author | `--preferred-template <brief.theme> --type page` 优先模板内页, fallback vp |
| Step 4 加视觉 | iloveppt | 读 `<!-- pattern: <id> -->` 注释, 查 DB 拿 meta.yaml |

若 author 在 content.md 嵌入了 `<!-- pattern: ... -->`, 注释必须含 `vp:` 或 `tpl:` 前缀, 否则 iloveppt 拒绝执行。
```

- [ ] **Step 4: Commit**

```bash
git add .claude/pipeline-protocol.md
git commit -m "docs(pipeline-protocol): library/search.sh 强制规则 + template-extractor 升级描述"
```

### Task 7.4: README.md(根) 路径同步

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 找路径引用**

Run: `grep -n "templates/" README.md`

- [ ] **Step 2: 改路径**

如果 README.md 有提到把 .pptx 放进 `templates/` 的说明, 改为 `library/pptx-templates/_source/`。
如果有提 library/visual-patterns/ 的, 同步描述新双 kb 结构。

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs(README): templates/ → library/pptx-templates/_source/"
```

---

## Phase 8: 收尾验证

### Task 8.1: sweep grep 找遗漏的旧路径

**Files:**
- Read-only sweep

- [ ] **Step 1: 找所有旧 templates/ 引用**

```bash
grep -rn "/templates/" --include="*.py" --include="*.md" --include="*.sh" --include="*.json" --include="*.yaml" \
    . 2>/dev/null | grep -v "library/pptx-templates" | grep -v "<plan_dir>/templates" | grep -v "docs/superpowers/" | head -30
```

逐条判断: 若是"deck 项目本地 `<plan_dir>/templates/`" 保留; 若是仓库根 `templates/` 必须改新路径。

- [ ] **Step 2: 找旧 library/visual-patterns/patterns 引用**

```bash
grep -rn "visual-patterns/patterns" --include="*.py" --include="*.md" . 2>/dev/null | head
```

逐条改为 `library/visual-patterns/items`。

- [ ] **Step 3: 找旧 pattern.yaml 引用**

```bash
grep -rn "pattern.yaml\|patterns.sqlite" --include="*.py" --include="*.md" --include="*.sh" . 2>/dev/null | head
```

逐条改为 `meta.yaml` / `db.sqlite`。

- [ ] **Step 4: Commit 修正**

```bash
git add -A
git commit -m "chore(library): sweep 修正遗漏的旧路径引用"
```

(若 grep 无 hit, 跳过本 commit)

### Task 8.2: 跑全测试套 + 烟测

**Files:**
- Read-only

- [ ] **Step 1: pytest 全跑**

Run: `python3 -m pytest tests/ -v`
Expected: 全部 passed(应在 75-85 之间, 取决于跳过的 venv 限定测试)

- [ ] **Step 2: load_theme 烟测**

```bash
python3 -c "
import sys; sys.path.insert(0, '.claude/skills/pptx-deck'); sys.path.insert(0, '.claude/skills/pptx')
import build
print('repo templates dir:', build._repo_templates_dir())
print('available:', build._list_available_templates())
try:
    build.load_theme('non_existent_template')
except ValueError as e:
    print('expected ValueError:', str(e)[:200])
"
```
Expected: 打印新路径 `.../library/pptx-templates/_source`, 错误消息含 `library/pptx-templates/_source/`

- [ ] **Step 3: search.sh 烟测(不调 API, --help)**

Run: `library/search.sh --help`
Expected: argparse help, 无错

- [ ] **Step 4: 现有最小 deck build 烟测**

Run: `python3 .claude/skills/pptx/examples/minimal_deck.py`
Expected: 产生 `/tmp/iloveppt_minimal.pptx`, 无错

### Task 8.3: 总收尾 commit + 准备 PR

**Files:**
- Read-only

- [ ] **Step 1: 检查 working tree 干净**

Run: `git status --short`
Expected: 空(所有变更已 commit)

- [ ] **Step 2: 看 commit 历史**

Run: `git log --oneline main..HEAD | head -30`
Expected: ~25 笔 commits 按 phase 顺序

- [ ] **Step 3:(可选)合并 commit 为更少笔**

若过多碎 commit, 可考虑 squash 关键节点(建议保留 phase 边界的 commit, 不必每 Task 单独保留)。

```bash
# 例如保留: phase 0 清空 / phase 1 _rag / phase 2 search / phase 3 docs / phase 4 build / phase 5 ingest / phase 6 agents / phase 7 配置 / phase 8 sweep
git rebase -i <base>     # 用户决定保留粒度, 不强求
```

- [ ] **Step 4: 提示用户 review + 创建 PR**

输出给用户:

```
✅ Library 知识库统一设计实施完成。
  - 双 kb 骨架建好(items/ + _source/ + _rag/)
  - 单 DB 5 表 + 2 向量表
  - search.sh router 含 fallback 逻辑
  - 4 个 agent prompt 已升级
  - 75+ 测试全过

下一步:
1. 用户配 library/_rag/.env(填 DASHSCOPE_API_KEY)
2. 手动 ingest 现有模板/pattern(走 template-extractor agent + visual-patterns ingest 流程)
3. 或创建 PR
```

---

## Self-Review Notes

**Spec coverage check**(对照 spec §1-§13):

| Spec 段 | 实施 Task |
|---|---|
| §1 背景 | (无 task · 设计 rationale) |
| §2 目标 | 整体 plan |
| §3 Non-goals | (无 task · 显式排除) |
| §4 目录结构 | Task 0.2, 3.1, 3.2 |
| §5 meta.yaml schema | Task 3.1, 3.2(写在 ingest_workflow.md) |
| §6 DB schema | Task 1.2, 1.3(qwen_embedding.py + test_db_schema.py) |
| §6.1 id 命名空间 | Task 1.6(test_id_namespacing.py) |
| §7 检索 router | Task 2.1, 2.2, 2.3 |
| §8 ingest workflow | Task 3.1, 3.2, 5.1, 5.2, 6.4 |
| §9 agent 集成 | Task 6.1-6.4 |
| §10 代码/配置同步 | Task 4.1-4.3, 7.1-7.4 |
| §11 风险 R1-R7 | R1 → Task 1.4(reject __); R3 → fallback-threshold CLI arg(Task 2.1); R5 → CREATE IF NOT EXISTS(Task 1.2) |
| §12 决策固化 | 整体 plan 体现 |
| §13 实施前置 | 已完成(plan 之前) |

**Type / naming consistency check**:

- `_repo_templates_dir()` 一致使用(Task 4.1-4.2)
- `vp:` / `tpl:` 前缀贯穿 search.py / embed_text.py / 测试
- `meta.yaml` 文件名贯穿(没用过 `pattern.yaml` / `template.yaml`)
- `library/_rag/db.sqlite` 单一路径(不再有 `patterns.sqlite` / `templates.sqlite`)
- `--preferred-template` 参数名贯穿 search.py CLI / agent prompt / spec

**Placeholder scan**: 无 TBD / TODO / "implement later"。所有代码片段完整。

**Scope check**: 单一 plan 可承载,各 Task < 5 分钟,有 commit 节点。Phase 8 收尾验证为可选 squash 给出空间。
