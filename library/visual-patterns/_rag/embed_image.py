#!/usr/bin/env python3
"""扫 library/visual-patterns/patterns/<id>/preview.png,调 Qwen3-VL embedding API
生成图像 embedding 写入 patterns.sqlite 的 image_emb 表。

Qwen3-VL 是多模态 embedding,跟 text 用同一 API,但 input 传 image 而非 text。
本地 PNG 会自动 base64 后塞进 data URI。

用法:
    cd library/visual-patterns/_rag
    .venv/bin/python embed_image.py            # 全量重建(image_emb)
    .venv/bin/python embed_image.py --only <id>  # 增量

要求每个 pattern dir 有 preview.png(无的 skip + warn)。
"""

from __future__ import annotations

import argparse
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

# 本地 lib
sys.path.insert(0, str(Path(__file__).parent))
from qwen_embedding import embed_image, get_api_key, open_db  # noqa: E402


PATTERNS_DIR = Path(__file__).parent.parent / "patterns"


def main():
    parser = argparse.ArgumentParser(description="(Re)build IMAGE embeddings via Qwen3-VL API")
    parser.add_argument("--only", help="只更新某 1 个 pattern id(增量)")
    args = parser.parse_args()

    api_key = get_api_key()

    if not PATTERNS_DIR.exists():
        print(f"ERROR: patterns 目录不存在: {PATTERNS_DIR}", file=sys.stderr)
        sys.exit(1)

    pattern_dirs: list[Path] = []
    if args.only:
        candidate = PATTERNS_DIR / args.only
        if not candidate.exists():
            print(f"ERROR: {candidate} 不存在", file=sys.stderr)
            sys.exit(1)
        pattern_dirs = [candidate]
    else:
        pattern_dirs = sorted(d for d in PATTERNS_DIR.iterdir() if d.is_dir())

    if not pattern_dirs:
        print(f"没有找到 pattern dir({PATTERNS_DIR}/*)")
        return

    db = open_db()
    now = datetime.now(timezone.utc).isoformat()

    count = 0
    skipped = 0
    for pd in pattern_dirs:
        pid = pd.name
        preview = pd / "preview.png"
        if not preview.exists():
            print(f"  - {pid}: 无 preview.png,skip")
            skipped += 1
            continue

        try:
            vec = embed_image(preview, api_key=api_key)
        except (RuntimeError, FileNotFoundError) as e:
            print(f"  ✗ {pid}: {e}", file=sys.stderr)
            continue

        emb_blob = struct.pack(f"{len(vec)}f", *vec)

        # 确保 patterns 表里有 row(允许 image_emb 在 text_emb 之前跑)
        db.execute(
            "INSERT OR IGNORE INTO patterns(id, preview_path, updated_at) VALUES (?, ?, ?)",
            (pid, str(preview), now),
        )
        db.execute(
            "INSERT OR REPLACE INTO image_emb(id, embedding) VALUES (?, ?)",
            (pid, emb_blob),
        )
        count += 1
        print(f"  ✓ {pid}  ←  {preview.relative_to(PATTERNS_DIR.parent)}")

    db.commit()
    db.close()
    print(f"\n完成 · embed {count} 个 pattern (image) · skip {skipped} → patterns.sqlite")


if __name__ == "__main__":
    main()
