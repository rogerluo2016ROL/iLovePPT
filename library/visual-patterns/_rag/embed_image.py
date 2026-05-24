#!/usr/bin/env python3
"""CLIP 图像 embedding · Phase 3 stub。

当 library 视觉风格多样化(用户加入手绘 / 卡通 / 黑白极简等),启用此脚本:
扫 patterns/*/preview.png 跑 CLIP image embedding → image.sqlite

启用步骤:
1. 解开 requirements.txt 里 CLIP 相关注释
   open-clip-torch>=2.20.0
   torch>=2.0.0
   pillow>=10.0.0
2. pip install -r requirements.txt
3. 实现下方 main()(参考注释里的 pseudo code)
4. search.py --mode image 才能用

当前 stub:跑会抛 NotImplementedError。这是有意的 —— 让用户明确决定何时启用。

设计参考:
    import open_clip
    import torch
    from PIL import Image

    model, _, preprocess = open_clip.create_model_and_transforms(
        'ViT-B-32', pretrained='openai'
    )
    tokenizer = open_clip.get_tokenizer('ViT-B-32')

    # 对每个 pattern 的 preview.png:
    image = preprocess(Image.open(png_path)).unsqueeze(0)
    with torch.no_grad():
        image_features = model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
    # → embed 512 维 float32,存 image.sqlite

    # query 时(在 search.py --mode image):
    # text → tokenizer + model.encode_text(...) → 跟 image.sqlite 找最近邻
    # 或 image → preprocess + model.encode_image(...) → 找最近邻

启用时:跟 embed_text.py 复用同一 schema 结构(独立 sqlite 文件)。
"""

import sys


def main():
    raise NotImplementedError(
        "CLIP 图像 embedding 是 Phase 3。当前 library 还以文本 RAG 为主(embed_text.py)。\n"
        "启用步骤见本文件顶部 docstring。"
    )


if __name__ == "__main__":
    main()
