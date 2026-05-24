#!/usr/bin/env python3
"""扫 library/visual-patterns/patterns/ 全部 pattern.yaml,生成文本 embedding 写入 text.sqlite。

用法:
    cd library/visual-patterns/_rag
    python3 embed_text.py            # 全量重建
    python3 embed_text.py --only <id>  # 只更新某 1 个 pattern(增量)

依赖:requirements.txt
首次跑会下载 BGE 中文模型 ~100MB(~/.cache/huggingface/)。

Schema:
- patterns  · id (PK) · doc · yaml_path · preview_path · category · updated_at
- pattern_embeddings · id (PK,vec0) · embedding FLOAT[512]

embed 的 document(给 BGE 看的文本)= name + category + content_intent + when_to_use + keywords
拼成一行。pattern.yaml 其他字段(visual_structure / fallback_rendering 等)不进 embed,
那些是 agent 看 yaml 时用的细节。
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

# 检测可选依赖,缺了给清晰错误
try:
    import yaml
except ImportError:
    print("ERROR: pyyaml 未装。pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("ERROR: sentence-transformers 未装。pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

try:
    import sqlite_vec
except ImportError:
    print("ERROR: sqlite-vec 未装。pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


SCRIPT_DIR = Path(__file__).parent
LIBRARY_DIR = SCRIPT_DIR.parent
PATTERNS_DIR = LIBRARY_DIR / "patterns"
DB_PATH = SCRIPT_DIR / "text.sqlite"
MODEL_NAME = "BAAI/bge-small-zh-v1.5"
EMBED_DIM = 512


def build_doc(p: dict) -> str:
    """把 pattern.yaml 关键字段拼成 embed 用的 document。

    BGE-zh 对短文本 + 中文关键词敏感,所以重复关键概念是好事(不是 noise)。
    """
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


def open_db() -> sqlite3.Connection:
    db = sqlite3.connect(DB_PATH)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.execute(
        """CREATE TABLE IF NOT EXISTS patterns (
            id TEXT PRIMARY KEY,
            doc TEXT,
            yaml_path TEXT,
            preview_path TEXT,
            category TEXT,
            updated_at TEXT
        )"""
    )
    db.execute(
        f"""CREATE VIRTUAL TABLE IF NOT EXISTS pattern_embeddings USING vec0(
            id TEXT PRIMARY KEY,
            embedding FLOAT[{EMBED_DIM}]
        )"""
    )
    return db


def load_pattern(yaml_path: Path) -> dict | None:
    try:
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ✗ 解析失败 {yaml_path}: {e}", file=sys.stderr)
        return None
    if not isinstance(data, dict):
        print(f"  ✗ {yaml_path} 不是合法 yaml dict", file=sys.stderr)
        return None
    if "id" not in data:
        print(f"  ✗ {yaml_path} 缺 id 字段", file=sys.stderr)
        return None
    return data


def main():
    parser = argparse.ArgumentParser(description="(Re)build text embeddings for pattern library")
    parser.add_argument(
        "--only",
        help="只更新某 1 个 pattern id(增量);省略 = 全量扫 patterns/",
    )
    args = parser.parse_args()

    if not PATTERNS_DIR.exists():
        print(f"ERROR: patterns 目录不存在: {PATTERNS_DIR}", file=sys.stderr)
        sys.exit(1)

    yaml_files: list[Path] = []
    if args.only:
        candidate = PATTERNS_DIR / args.only / "pattern.yaml"
        if not candidate.exists():
            print(f"ERROR: {candidate} 不存在", file=sys.stderr)
            sys.exit(1)
        yaml_files = [candidate]
    else:
        yaml_files = sorted(PATTERNS_DIR.glob("*/pattern.yaml"))

    if not yaml_files:
        print(f"没有找到 pattern.yaml(查的:{PATTERNS_DIR}/*/pattern.yaml)")
        return

    print(f"加载 BGE 中文模型 {MODEL_NAME}(首次会下载 ~100MB)...")
    model = SentenceTransformer(MODEL_NAME)

    db = open_db()
    now = datetime.now(timezone.utc).isoformat()

    count = 0
    for yp in yaml_files:
        p = load_pattern(yp)
        if not p:
            continue

        pid = p["id"]
        doc = build_doc(p)
        preview = yp.parent / "preview.png"

        embedding = model.encode(doc, normalize_embeddings=True).astype("float32")
        assert embedding.shape == (EMBED_DIM,), f"unexpected dim {embedding.shape}"

        db.execute(
            "INSERT OR REPLACE INTO patterns(id, doc, yaml_path, preview_path, category, updated_at) VALUES (?,?,?,?,?,?)",
            (pid, doc, str(yp), str(preview), p.get("category", ""), now),
        )
        db.execute(
            "INSERT OR REPLACE INTO pattern_embeddings(id, embedding) VALUES (?, ?)",
            (pid, embedding.tobytes()),
        )
        count += 1
        print(f"  ✓ {pid}  ←  {doc[:80]}{'...' if len(doc) > 80 else ''}")

    db.commit()
    db.close()
    print(f"\n完成 · embed {count} 个 pattern → {DB_PATH}")


if __name__ == "__main__":
    main()
