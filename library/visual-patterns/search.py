#!/usr/bin/env python3
"""Visual Patterns 检索 CLI · agent 通过 Bash 调用。

用法:
    python3 library/visual-patterns/search.py \\
        --query "3 阶段流程 + 验证循环" \\
        --category process \\
        --top-k 5 \\
        --format json

    python3 library/visual-patterns/search.py --query "PDCA" --top-k 3 --format text

返回 top-K 候选,带 score(cosine similarity)+ preview path + yaml_path,
让 agent 进一步 Read pattern.yaml 决定用哪个。

模式:
    --mode text     文本 embedding 查(默认,BGE 中文)
    --mode image    CLIP 图像 embedding 查(Phase 3 · 当前 raise NotImplementedError)
    --mode hybrid   text + image 加权(Phase 3)

依赖:_rag/requirements.txt
索引建立:python3 _rag/embed_text.py(首次或 patterns/ 改后跑)
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print(
        "ERROR: sentence-transformers 未装。\n"
        "    cd library/visual-patterns/_rag && pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    import sqlite_vec
except ImportError:
    print(
        "ERROR: sqlite-vec 未装。\n"
        "    cd library/visual-patterns/_rag && pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)


SCRIPT_DIR = Path(__file__).parent
DB_PATH = SCRIPT_DIR / "_rag" / "text.sqlite"
MODEL_NAME = "BAAI/bge-small-zh-v1.5"


def search_text(
    query: str, category: str | None = None, top_k: int = 5
) -> list[dict]:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"vec DB 不存在: {DB_PATH}\n"
            f"先跑:python3 {SCRIPT_DIR}/_rag/embed_text.py"
        )

    model = SentenceTransformer(MODEL_NAME)
    query_emb = model.encode(query, normalize_embeddings=True).astype("float32")

    db = sqlite3.connect(DB_PATH)
    db.enable_load_extension(True)
    sqlite_vec.load(db)

    if category:
        # category 过滤 + 余弦距离 ASC(BGE 是 normalize_embeddings=True,余弦距离 ≈ 1-余弦相似度)
        rows = db.execute(
            """SELECT p.id, p.doc, p.yaml_path, p.preview_path, p.category,
                      vec_distance_cosine(e.embedding, ?) AS distance
               FROM patterns p
               JOIN pattern_embeddings e ON p.id = e.id
               WHERE p.category = ?
               ORDER BY distance ASC
               LIMIT ?""",
            (query_emb.tobytes(), category, top_k),
        ).fetchall()
    else:
        rows = db.execute(
            """SELECT p.id, p.doc, p.yaml_path, p.preview_path, p.category,
                      vec_distance_cosine(e.embedding, ?) AS distance
               FROM patterns p
               JOIN pattern_embeddings e ON p.id = e.id
               ORDER BY distance ASC
               LIMIT ?""",
            (query_emb.tobytes(), top_k),
        ).fetchall()

    db.close()

    return [
        {
            "id": r[0],
            "category": r[4],
            "score": round(1 - r[5], 4),  # 余弦相似度
            "preview": r[3],
            "yaml_path": r[2],
            "doc_preview": (r[1] or "")[:120] + ("..." if r[1] and len(r[1]) > 120 else ""),
        }
        for r in rows
    ]


def search_image(query: str, top_k: int) -> list[dict]:
    raise NotImplementedError(
        "--mode image 是 Phase 3(CLIP)。当前 library 用 --mode text。\n"
        "启用:打开 _rag/embed_image.py docstring 顶部说明,装 CLIP 依赖。"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Visual Patterns 检索 · 按 content intent 找最匹配 pattern",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--query", required=True, help="自然语言查询(如 '3 阶段流程 + 验证循环')"
    )
    parser.add_argument(
        "--category",
        default=None,
        help="可选 category 过滤(process / cycle / comparison / hierarchy / data / relationship)",
    )
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--mode",
        default="text",
        choices=["text", "image", "hybrid"],
        help="查询模式(image / hybrid 是 Phase 3,当前只 text)",
    )
    parser.add_argument(
        "--format",
        default="json",
        choices=["json", "text"],
        help="输出格式(agent 用 json;人看用 text)",
    )
    args = parser.parse_args()

    if args.mode == "text":
        results = search_text(args.query, args.category, args.top_k)
    elif args.mode == "image":
        results = search_image(args.query, args.top_k)
    else:  # hybrid
        raise NotImplementedError("--mode hybrid 是 Phase 3")

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(
                f"{r['score']:.3f}  [{r['category']:>12}]  {r['id']:<30}  → {r['preview']}"
            )
            print(f"          {r['doc_preview']}")


if __name__ == "__main__":
    main()
