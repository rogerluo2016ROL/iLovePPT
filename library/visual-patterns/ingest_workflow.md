# Ingest Workflow · 给我喂模板素材的标准流程

用户有新的 .pptx 模板 / 截图素材 → 通过这个流程入库,变成可被 agent 检索的 pattern。

---

## 场景 A · 用户给一份 .pptx(标准场景)

### Step 1 · 用户:把 .pptx 拷到归档目录

```bash
cp my_company_template.pptx library/visual-patterns/_source_inspiration/
```

### Step 2 · 用户:跟主线程说"入库"

```
我有一份新模板 library/visual-patterns/_source_inspiration/my_company_template.pptx
请入库
```

### Step 3 · 主线程(我):渲染每页 PNG

```bash
mkdir -p /tmp/ingest_<timestamp>/
soffice --headless --convert-to pdf my_company_template.pptx --outdir /tmp/ingest_<timestamp>/
pdftoppm -jpeg -r 120 /tmp/ingest_<timestamp>/my_company_template.pdf /tmp/ingest_<timestamp>/page
```

### Step 4 · 主线程:逐页 Read PNG + 推断 pattern.yaml 草稿

对每页:
- `Read` PNG
- 推断:
  - `id`(短中划线名,如 `cycle-donut-3` / `pdca-loop`)
  - `name`(中文短名)
  - `category`(process / cycle / comparison / hierarchy / data / relationship 选一)
  - `content_intent`(2-3 条用户视角描述)
  - `visual_structure`(n_items / has_X / axis 等)
  - `when_to_use` / `when_not_to_use`
  - `keywords`(中文 + 英文同义词)
- 抠 preview.png(crop 或直接用整页 PNG)
- 写到 `patterns/<id>/`

### Step 5 · 主线程:把所有 draft 列给用户审

```
我从你这份 .pptx 推断了 10 个 pattern 草稿:

[01] cycle-donut-3       · 3 段环形循环      · category=cycle    · 看起来匹配你的 page 2
[02] funnel-3-stage      · 3 阶漏斗          · category=process  · 看起来匹配你的 page 4
[03] pdca-loop           · PDCA 迭代循环     · category=cycle    · 看起来匹配你的 page 10
...

请逐个审:
- ✓ 通过 → 留下
- 改名 → "把 cycle-donut-3 改成 donut-3stages"
- 弃用 → "丢掉 #07"
- 改 content_intent → "在 cycle-donut-3 加'PDCA 单次循环'到 intent"
```

### Step 6 · 用户审完 → 主线程:重建 vec DB

```bash
python3 library/visual-patterns/_rag/embed_text.py
```

### Step 7 · 主线程:更新 INDEX.md(自动生成)

每个 pattern.yaml 的 1 行摘要进 INDEX.md。

### Step 8 · 验证

```bash
python3 library/visual-patterns/search.py --query "PDCA 改进循环" --top-k 3
# 期望 pdca-loop 排第 1
```

---

## 场景 B · 用户只给截图(图片素材)

跟场景 A 类似,差异:
- Step 1:`cp screenshot.png library/visual-patterns/_source_inspiration/`
- Step 3:跳过(已是 PNG)
- Step 4:Read 这张 PNG → 推断里面包含的 patterns(可能多个,需分割)
  - 若用户单张图含多个 layout 缩略图(像幻灯片缩略图视图)→ 我按缩略图位置切割推断
  - 若是单页深度截图 → 当 1 个 pattern

---

## 场景 C · 增量(只加 1 个 pattern)

用户:"page 3 这种我没见过,加进库"

- 用户提供单页 PNG
- 主线程推断 → 写 pattern.yaml → `python3 _rag/embed_text.py --only <id>` 增量更新

---

## 我推断 pattern.yaml 的判断标准

| 字段 | 怎么推 |
|---|---|
| `id` | 短中划线名,优先模式描述(`cycle-donut-3` 而非 `slide_2`) |
| `name` | 中文,5-10 字 |
| `category` | 看视觉主体决定:循环图 → cycle / 漏斗 → process / 对比 → comparison / 层级 → hierarchy / 数据 → data / 关系 → relationship |
| `content_intent` | 至少 2 条:1 条用专业术语(读者懂)+ 1 条用大白话(用户搜) |
| `visual_structure` | 数字优先(n_items=3),布尔标识(has_dates=true) |
| `when_to_use` / `when_not_to_use` | **关键!**让 agent 知道何时选这个 vs 替代方案 |
| `keywords` | 同义词列表(中文 + 英文 + 行业行话) |
| `matches_iloveppt_layout` | 若现有 layout 能映射就标(`cards` / `pic_text` 等),否则 `null` |
| `fallback_rendering` | 首版多为 `method: manual`(agent 看到后自己用 diagram skill 现画);常用 pattern 后续升级 `method: drawio_template` 或 `python_make_func` |

---

## 维护

- 改 pattern.yaml 后必须重跑 `_rag/embed_text.py --only <id>`(否则 vec DB 不同步)
- 删 pattern 后跑 `_rag/embed_text.py`(全量重建会清掉孤儿)
- 新 pattern 加进 patterns/ 后跑 `_rag/embed_text.py --only <id>`(增量)
