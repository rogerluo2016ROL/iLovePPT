# PPTX Templates Ingest Workflow

用户:"把 template_X.pptx 入库"。流程 1:1(一份 .pptx → 一个模板 + N 个页 items)。

由 `iloveppt-template-extractor` agent 主导,主线程 dispatch。

## 步骤

```
1. 用户提供 .pptx 路径
2. agent 复制到 library/pptx-templates/_source/<name>.pptx
   (<name> 不允许含 __ · 跟 page id 分隔符冲突)
3. soffice --headless --convert-to pdf <pptx> + pdftoppm -png -r 120
   渲染每页 → library/pptx-templates/items/<name>/pages/<NN-slug>/preview.png
4. Claude(LLM)看 PNG:
   (a) 总览所有页 → 产 template-level meta.yaml 草稿
   (b) 逐页 → 产 page-level meta.yaml 草稿 + 决定 page slug(把 01-page 改名为 01-cover / 02-toc 等)
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
