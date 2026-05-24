#!/usr/bin/env python3
"""Visual Patterns 检索 CLI · agent 通过 Bash 调(或 search.sh wrapper)。

用法:
    # text-only(常用 · 用 content intent 找匹配 pattern)
    python3 search.py --query "PDCA 改进循环" --top-k 5 --format json

    # image-only(text→image 跨模态搜索 · 找视觉风格相近的 pattern)
    python3 search.py --query "现代极简 蓝白" --mode image --top-k 5

    # hybrid(融合 text + image,默认权重 text 0.6 image 0.4)
    python3 search.py --query "PDCA + 现代极简" --mode hybrid --top-k 5

    # 上传一张参考图找视觉相似 pattern(image-image 搜索,极强!)
    python3 search.py --query-image /path/to/some_inspiration.png --top-k 5

依赖:
    - sqlite-vec(底层 vec DB)
    - requests / urllib(已是 stdlib · 调 Qwen3-VL API)
    - DASHSCOPE_API_KEY env var 或 _rag/.env 文件

向量来源:
    _rag/patterns.sqlite · text_emb + image_emb 两表(模型 / dim 由 .env 决定,默认 tongyi-embedding-vision-plus · dim 1152)
索引建立:
    .venv/bin/python _rag/embed_text.py    # text 入库
    .venv/bin/python _rag/embed_image.py   # image 入库(只 embed 有 preview.png 的)
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

# 本地 lib
sys.path.insert(0, str(Path(__file__).parent / "_rag"))
from qwen_embedding import DB_PATH, embed_image, embed_text, get_api_key, open_db  # noqa: E402

DEFAULT_HYBRID_WEIGHTS = (0.6, 0.4)  # (text, image)


def _query_table(db, table: str, query_blob: bytes, category: str | None, top_k: int) -> list[tuple]:
    """从某 vec0 表查 top-K + 可选 category 过滤,返回 (id, distance, …)"""
    if category:
        sql = f"""SELECT p.id, p.text_doc, p.yaml_path, p.preview_path, p.category,
                         vec_distance_cosine(e.embedding, ?) AS distance
                  FROM patterns p JOIN {table} e ON p.id = e.id
                  WHERE p.category = ?
                  ORDER BY distance ASC
                  LIMIT ?"""
        return db.execute(sql, (query_blob, category, top_k)).fetchall()
    sql = f"""SELECT p.id, p.text_doc, p.yaml_path, p.preview_path, p.category,
                     vec_distance_cosine(e.embedding, ?) AS distance
              FROM patterns p JOIN {table} e ON p.id = e.id
              ORDER BY distance ASC
              LIMIT ?"""
    return db.execute(sql, (query_blob, top_k)).fetchall()


def _row_to_dict(r: tuple, mode_tag: str) -> dict:
    return {
        "id": r[0],
        "category": r[4] or "",
        "score": round(1 - r[5], 4),  # cosine 相似度
        "mode": mode_tag,
        "preview": r[3] or "",
        "yaml_path": r[2] or "",
        "doc_preview": (r[1] or "")[:120] + ("..." if r[1] and len(r[1]) > 120 else ""),
    }


def search(
    query: str | None,
    query_image: str | None,
    category: str | None,
    top_k: int,
    mode: str,
    text_weight: float = DEFAULT_HYBRID_WEIGHTS[0],
    image_weight: float = DEFAULT_HYBRID_WEIGHTS[1],
) -> list[dict]:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"vec DB 不存在: {DB_PATH}\n"
            f"  先跑:.venv/bin/python _rag/embed_text.py + _rag/embed_image.py"
        )

    api_key = get_api_key()
    db = open_db()

    # query embedding 来源:--query-image 优先;否则用 --query 文本
    if query_image:
        q_vec = embed_image(query_image, api_key=api_key)
    elif query:
        q_vec = embed_text(query, api_key=api_key)
    else:
        raise ValueError("必须提供 --query 或 --query-image 之一")

    q_blob = struct.pack(f"{len(q_vec)}f", *q_vec)

    if mode == "text":
        rows = _query_table(db, "text_emb", q_blob, category, top_k)
        return [_row_to_dict(r, "text") for r in rows]

    if mode == "image":
        rows = _query_table(db, "image_emb", q_blob, category, top_k)
        return [_row_to_dict(r, "image") for r in rows]

    if mode == "hybrid":
        # 各表取前 top_k * 3 候选,按 (text_weight * text_score + image_weight * image_score) 重排
        text_rows = _query_table(db, "text_emb", q_blob, category, top_k * 3)
        image_rows = _query_table(db, "image_emb", q_blob, category, top_k * 3)
        scores: dict[str, dict] = {}
        for r in text_rows:
            d = _row_to_dict(r, "text")
            scores.setdefault(d["id"], {**d, "text_score": 0.0, "image_score": 0.0})
            scores[d["id"]]["text_score"] = d["score"]
        for r in image_rows:
            d = _row_to_dict(r, "image")
            scores.setdefault(d["id"], {**d, "text_score": 0.0, "image_score": 0.0})
            scores[d["id"]]["image_score"] = d["score"]
        merged = []
        for pid, d in scores.items():
            d["score"] = round(
                text_weight * d["text_score"] + image_weight * d["image_score"], 4
            )
            d["mode"] = "hybrid"
            merged.append(d)
        merged.sort(key=lambda x: x["score"], reverse=True)
        return merged[:top_k]

    raise ValueError(f"unknown mode: {mode}")


def main():
    parser = argparse.ArgumentParser(
        description="Visual Patterns 检索 · text/image/hybrid 三模式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--query",
        help="自然语言查询(text 或 hybrid 模式 / image 模式时是 text→image 跨模态)",
    )
    parser.add_argument(
        "--query-image",
        help="参考图路径(优先用 · image-image 视觉相似度搜索)",
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
        help="text(默认)/ image(text→image 或 image-image)/ hybrid(融合)",
    )
    parser.add_argument(
        "--text-weight",
        type=float,
        default=DEFAULT_HYBRID_WEIGHTS[0],
        help="hybrid 模式下 text 权重(默认 0.6)",
    )
    parser.add_argument(
        "--image-weight",
        type=float,
        default=DEFAULT_HYBRID_WEIGHTS[1],
        help="hybrid 模式下 image 权重(默认 0.4)",
    )
    parser.add_argument(
        "--format", default="json", choices=["json", "text"], help="agent 用 json;人看用 text"
    )
    args = parser.parse_args()

    if not args.query and not args.query_image:
        parser.error("必须提供 --query 或 --query-image")

    results = search(
        query=args.query,
        query_image=args.query_image,
        category=args.category,
        top_k=args.top_k,
        mode=args.mode,
        text_weight=args.text_weight,
        image_weight=args.image_weight,
    )

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            extra = (
                f"  [t={r.get('text_score', 0):.2f} i={r.get('image_score', 0):.2f}]"
                if r.get("mode") == "hybrid"
                else ""
            )
            print(f"{r['score']:.3f}  [{r['category']:>12}]  {r['id']:<30}{extra}  → {r['preview']}")
            print(f"          {r['doc_preview']}")


if __name__ == "__main__":
    main()
