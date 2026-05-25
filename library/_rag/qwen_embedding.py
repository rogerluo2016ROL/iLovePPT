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
