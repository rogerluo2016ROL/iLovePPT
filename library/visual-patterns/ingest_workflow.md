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
