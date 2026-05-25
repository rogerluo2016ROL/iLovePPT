# Library 知识库统一设计 · pptx-templates + visual-patterns

**日期**: 2026-05-25
**作者**: pcliangx + Claude
**状态**: design (待 writing-plans 出实施计划)

## 1. 背景与动机

iLovePPT 当前已有 `library/visual-patterns/` 作为视觉模式的 RAG 知识库(被 author / iloveppt 在拓写 / 加视觉时调用)。但用户预置的 `.pptx` 模板仍以平铺方式放在仓库根 `templates/` 下,只有顶层 `<name>.yaml` 元数据,**模板内容本身不可被 agent 检索**。

本 spec 把 templates 也升级为知识库,并统一两个知识库的目录骨架 / 命名风格 / DB 设施,使其:

- 可被 agent 按"找模板" / "找模板内的某页" 检索
- 用户选定模板后,优先在该模板内匹配; 不够再降级到 visual-patterns
- 两个知识库共享 `_rag/` 基础设施(venv + 凭据 + DB),不重复

## 2. 目标 (Goals)

- `library/` 下双知识库内部目录 / 文件命名严格对称
- 单一 `library/_rag/db.sqlite` · 5 张管理表 + 2 张共享向量表
- 顶层 `library/search.sh` router 作为唯一检索入口,支持 preferred-template 优先 + fallback
- 4 个 iLovePPT agent prompt 顺势改造(brainstorm / author / iloveppt / template-extractor)
- `build.py:load_theme()` 路径切到新位置,旧 `templates/` 目录退役

## 3. Non-Goals

- 不做自动 batch ingest(单模板手动触发)
- 不做 meta.yaml 编辑器 UI(用 $EDITOR)
- 不做模板版本管理(覆盖即更新)
- 不做跨用户同步机制(沿用现有 git submodule / 共享盘建议)
- 不自动迁移已清空的 21 个旧 visual-patterns(用户重 ingest,按新 schema 重审)
- 不调优 `--fallback-threshold` 默认值(0.55 为初始,实施期按真实 deck 验证)

## 4. 目录结构

```
library/
├── _rag/                                ← 顶层 RAG 基础设施 (单一)
│   ├── .env  .venv/  requirements.txt
│   ├── qwen_embedding.py
│   ├── embed_text.py                    ← 接受 --kb 过滤
│   ├── embed_image.py
│   └── db.sqlite                        ← 单一 DB · gitignored
├── search.sh                            ← 唯一检索入口 (顶层 router)
├── search.py
│
├── visual-patterns/
│   ├── README.md  INDEX.md  ingest_workflow.md
│   ├── items/<id>/
│   │   ├── meta.yaml
│   │   └── preview.png
│   └── _source/<id>.<ext>               ← gitignored · 1:N inspiration
│
└── pptx-templates/
    ├── README.md  INDEX.md  ingest_workflow.md
    ├── items/<name>/
    │   ├── meta.yaml                    ← 模板级 metadata
    │   ├── preview.png                  ← cover 缩略图
    │   └── pages/<NN-slug>/
    │       ├── meta.yaml                ← 页级 metadata
    │       └── preview.png
    └── _source/<name>.pptx              ← gitignored · 1:1 模板源 · load_theme() 读这里
```

**对称原则**: 两个 kb 内部目录骨架 (items / _source / docs) 完全一致, 差异仅在 `pptx-templates/items/<name>/pages/` 子层(业务需要)。

## 5. Schema 设计

### 5.1 visual-patterns 的 `meta.yaml` (沿用现有 `pattern.yaml` 字段名,改文件名)

```yaml
id: timeline-band-3                       # 跟目录名一致
name: 3 段色块时间轴
category: process                         # process/cycle/comparison/hierarchy/data/relationship

content_intent:
  - 3 个时间段的阶段对比
when_to_use:
  - 季度回顾 / 阶段汇报
when_not_to_use:
  - 时段超过 5 段
keywords: [时间轴, timeline, milestone]

matches_iloveppt_layout: null             # 或某个内置 layout 名
fallback_rendering:
  method: manual
  notes: 3 个等宽矩形色块横排...
```

### 5.2 pptx-templates 模板级 `items/<name>/meta.yaml`

```yaml
id: template_golden
name: 企业级 B2B 深蓝现代模板
category: enterprise-modern               # 模板大类
content_intent:
  - 企业级 B2B 提案
when_to_use:
  - 公司外部提案 / 销售路演
when_not_to_use:
  - 培训 / 轻量教育
keywords: [enterprise, B2B, navy, 深蓝]

visual_tokens:                            # 从 .pptx 自动提取
  primary: '#234666'
  accent: '#AD9B5D'
  font_ea: '+mj-ea'
  title_size_pt: 28
  body_size_pt: 18
visual_signature:                         # 模板辨识元素
  - 左侧 navy accent line
  - 白底 / 深蓝 cover 反差
assets:
  source_pptx: ../../_source/template_golden.pptx
  total_pages: 8
  cover_thumbnail: pages/01-cover/preview.png
pages: [01-cover, 02-toc, 03-section-divider, ...]
implementation:
  tier2_python_theme: null                # .claude/skills/pptx-deck/themes/<name>.py 若存在
  iLovePPT_can_replicate_pct: null        # 0-100
```

### 5.3 pptx-templates 页级 `items/<name>/pages/<NN-slug>/meta.yaml`

```yaml
id: template_golden__01-cover             # 全局唯一 · {template}__{page-slug}
name: Cover · 深蓝 + 白字 + navy accent line
category: cover                           # layout 大类
content_intent:
  - 企业级 B2B 严肃开场
when_to_use:
  - 正式提案 / 路演开场
when_not_to_use:
  - 轻量培训
keywords: [cover, 封面, 深蓝, navy]
fallback_rendering:
  method: native_pptx
  notes: 深蓝纯色 + 白色 ≤22 字标题 + 左侧 navy 细 accent line

# 页专有字段
template_name: template_golden
page_index: 1
layout_type: cover
native_elements:
  - 左侧 accent 线 navy 细线
iLovePPT_can_replicate_pct: 60
matches_iloveppt_layout: cover
copy_constraints:
  title_max_chars: 22
  subtitle_max_chars: 30
```

## 6. DB Schema

单一 `library/_rag/db.sqlite`:

```sql
-- 1. visual-patterns 的 items
CREATE TABLE vp_items (
    id TEXT PRIMARY KEY,                  -- 例: vp:timeline-band-3
    text_doc TEXT,
    meta_path TEXT,                       -- visual-patterns/items/<id>/meta.yaml
    preview_path TEXT,
    category TEXT,
    updated_at TEXT
);

-- 2. pptx-templates 的模板管理表
CREATE TABLE tpl_templates (
    id TEXT PRIMARY KEY,                  -- 例: tpl:template_golden
    name TEXT, desc TEXT, category TEXT,
    keywords TEXT, recommended_for TEXT,
    visual_tokens_json TEXT,
    visual_signature TEXT,
    iLovePPT_can_replicate_pct INTEGER,
    source_pptx_path TEXT,                -- pptx-templates/_source/<name>.pptx
    pages_count INTEGER,
    meta_path TEXT, preview_path TEXT,
    text_doc TEXT,
    updated_at TEXT
);

-- 3. pptx-templates 的页表
CREATE TABLE tpl_pages (
    id TEXT PRIMARY KEY,                  -- 例: tpl:template_golden__01-cover
    template_id TEXT NOT NULL,            -- FK 概念 · 指向 tpl_templates.id
    layout_type TEXT,
    page_index INTEGER,
    text_doc TEXT,
    meta_path TEXT, preview_path TEXT,
    extras_json TEXT,                     -- copy_constraints / native_elements 等
    updated_at TEXT
);

-- 4. 跨 kb 共享向量(id 前缀区分 vp: / tpl:)
CREATE VIRTUAL TABLE text_emb  USING vec0(id TEXT PRIMARY KEY, embedding FLOAT[1152]);
CREATE VIRTUAL TABLE image_emb USING vec0(id TEXT PRIMARY KEY, embedding FLOAT[1152]);
```

### 6.1 id 命名空间(必加前缀防跨表碰撞)

| 来源 | id 格式 | 例 |
|---|---|---|
| visual-patterns items | `vp:<id>` | `vp:timeline-band-3` |
| pptx-templates 模板 | `tpl:<name>` | `tpl:template_golden` |
| pptx-templates 页 | `tpl:<name>__<NN-slug>` | `tpl:template_golden__01-cover` |

模板名不允许含 `__`(双下划线),ingest 时 reject。

## 7. 检索路由(`library/search.sh`)

唯一入口,参数:

```bash
library/search.sh \
    --query "<text>"                        # 文本查询
    --query-image <path>                    # 图查询(优先于 --query)
    --mode text|image|hybrid                # 默认 text
    --kb visual-patterns|pptx-templates|all # 默认 all
    --type item|template|page|any           # 默认 any
    --category <cat>
    --preferred-template <name>             # 触发"模板优先 + vp 降级"
    --top-k 5
    --fallback-threshold 0.55               # 降级触发阈值
    --format json|text
```

### 7.1 跨 kb 单 SQL 检索(简化)

```sql
WITH ranked AS (
    SELECT 'vp_item' AS row_type, id, category, NULL AS parent_id,
           vec_distance_cosine(e.embedding, ?) AS distance
      FROM vp_items v JOIN text_emb e ON v.id = e.id
    UNION ALL
    SELECT 'tpl_template', id, category, NULL,
           vec_distance_cosine(e.embedding, ?) AS distance
      FROM tpl_templates t JOIN text_emb e ON t.id = e.id
    UNION ALL
    SELECT 'tpl_page', id, layout_type, template_id,
           vec_distance_cosine(e.embedding, ?) AS distance
      FROM tpl_pages p JOIN text_emb e ON p.id = e.id
)
SELECT * FROM ranked
 WHERE (? IS NULL OR row_type = ?)
   AND (? IS NULL OR parent_id = ?)
 ORDER BY distance ASC LIMIT ?;
```

### 7.2 Fallback 行为

```
有 --preferred-template?
├─ 是 → 在 tpl_pages 查, 限定 template_id = tpl:<name>
│   ├─ top-k 命中, 平均分 ≥ threshold → 返回
│   └─ 命中数不够 / 分数低 → fallback ──┐
└─ 否 → 直接查 visual-patterns ←─────────┘
                                         ↓
返回结果 marking source:
  'preferred-template' / 'visual-patterns'
按 distance 合并 top-k
```

## 8. Ingest Workflow

### 8.1 visual-patterns(用户上传灵感 .pptx,拆 N 个 pattern)

```
1. 用户:"把这份 .pptx 入库,拆视觉 pattern"
2. agent 复制 .pptx 到 library/visual-patterns/_source/<basename>.pptx
3. soffice → pdftoppm → 每页 PNG 候选
4. Claude 看 PNG → 推断 N 份 candidate meta.yaml (草稿)
5. 用户审 / 改名 / 弃用 (用户选哪些纳入)
6. 通过的写入 library/visual-patterns/items/<id>/meta.yaml + preview.png
7. 跑 library/_rag/.venv/bin/python library/_rag/embed_text.py --kb visual-patterns --id <id>
8. 跑 embed_image.py 同
```

### 8.2 pptx-templates(用户上传 .pptx 模板,拆 1 template + N pages)

```
1. 用户:"把 template_X.pptx 入库"
2. agent 复制到 library/pptx-templates/_source/<name>.pptx
3. soffice 渲染每页 → library/pptx-templates/items/<name>/pages/<NN-slug>/preview.png
4. Claude 推断 template-level meta.yaml(整体风格) + per-page meta.yaml
5. 用户审改
6. 通过的写入 items/<name>/meta.yaml + pages/<NN-slug>/meta.yaml + preview.png
7. embed_text.py + embed_image.py(--kb pptx-templates --id <name>)
   会同时入 tpl_templates 表 1 行 + tpl_pages 表 N 行 + 向量 N+1 行
```

## 9. Agent 集成点

### 9.1 `iloveppt-brainstorm` (Stage A · 列模板)

从硬扫 `templates/*.yaml` 改为查 DB:

```bash
library/search.sh --kb pptx-templates --type template --query "<用户主题>" --top-k 5 --format text
```

展示 top-5 给用户(按主题相关性排序),用户选定后 brainstorm 在 brief.md 写 `theme: template_golden`。

### 9.2 `iloveppt-author` (Stage D · 拓写每页时)

```bash
library/search.sh \
    --query "<本页核心意图>" \
    --preferred-template <brief 的 theme> \
    --type page --top-k 5 --fallback-threshold 0.55
```

author 在 content.md 嵌入注释:

```markdown
## 4. 用户增长破亿
<!-- pattern: tpl:template_golden__04-single-focus -->

或 fallback:
## 3. PDCA 持续改进
<!-- pattern: vp:pdca-iterations -->
```

注释 id 完整带 `vp:` / `tpl:` 前缀,下游能定位。

### 9.3 `iloveppt` (Stage E · Step 4 加视觉)

1. 读 content.md 提取 `pattern:` 注释
2. 用 id 查 DB → 拿 meta.yaml 路径 → Read 看 `fallback_rendering`
3. 按 method 渲染(native_pptx / diagram / manual)

无 `pattern:` 注释时,自己跑 `library/search.sh --type=any` 现查。

### 9.4 `iloveppt-template-extractor` (升级为 ingest 入口)

不再仅抽 token,改为走 §8.2 完整 ingest 流程:复制 .pptx → render → LLM 起草 meta.yaml → 用户审 → embed 入库。

### 9.5 `iloveppt-audience` (无改动)

audience 评分跟 library 无关。

## 10. 代码 / 配置同步变更

### 10.1 `build.py:219` `load_theme()` 路径

```python
def _repo_templates_dir() -> Path:
-    return Path(__file__).resolve().parent.parent.parent / "templates"
+    return Path(__file__).resolve().parent.parent.parent / "library" / "pptx-templates" / "_source"
```

错误消息 / 短名查找逻辑也同步,deck 项目本地 `<plan_dir>/templates/` 保留(向后兼容)。

### 10.2 `.gitignore` 重写

删除 `templates/*.pptx` / `templates/*.yaml` / 旧 `library/visual-patterns/` 相关段。新增:

```
# === library/ · 知识库 ===
library/_rag/.venv/
library/_rag/.env
library/_rag/.env.*
library/_rag/db.sqlite
library/_rag/.cache/

# 各 kb 的 _source/ · 用户原始材料
library/*/_source/

# items/<id>/{meta.yaml,preview.png} 入 git(不 ignore)
```

### 10.3 `CLAUDE.md` 同步

- "三 skill 分层"段后新增 "Library / 知识库" 一段
- Quick Start 里 `templates/<name>.pptx` 提示 → `library/pptx-templates/_source/<name>.pptx`
- "约定 · 路径表示"段加一条 `library/` 是 RAG 根

### 10.4 `.claude/pipeline-protocol.md` 同步

- §1 派发表 `iloveppt-template-extractor` 行: 从"抽 4 级 token" → "完整 ingest 入库"
- §3 派发规则新增: brainstorm Stage A 列模板 / author Stage D 拓写 / iloveppt Step 4 加视觉,三处都强制走 `library/search.sh`

### 10.5 测试策略

新增 `tests/library/`:

| 测试 | 验证 |
|---|---|
| `test_search_routing.py` | router 的 fallback 逻辑 |
| `test_id_namespacing.py` | vp: / tpl: 不冲突,跨表 join 正确 |
| `test_load_theme_path.py` | load_theme 找新路径 |
| `test_db_schema.py` | 5 张表结构 + 索引 |
| `test_ingest_pipeline.py` | render → meta.yaml → embed 全链路(mock LLM) |

现有受影响测试 sweep:

```bash
grep -rn "templates/" tests/ .claude/skills/
grep -rn "library/visual-patterns/patterns" tests/
grep -rn "pattern.yaml" tests/
```

## 11. 风险与缓解

| # | 风险 | 缓解 |
|---|---|---|
| R1 | 模板名含 `__` 与 page id 分隔符冲突 | ingest 时 reject |
| R2 | 21 个旧 visual-patterns 已清,需重 ingest | git checkout 旧版本参考,人工对齐新 schema |
| R3 | fallback-threshold 0.55 是猜测 | 实施时做成 .env 配置 |
| R4 | embed API 撞 DashScope 限速 | 已有 retry=3 exponential backoff |
| R5 | DB schema v1 字段不全后续要 migration | sqlite-vec 表用 IF NOT EXISTS;主表 ALTER ADD COLUMN |
| R6 | `_source/<name>.pptx` gitignored,团队同步靠用户 | 不变,沿用旧 README 建议 |
| R7 | tpl_templates 的 text_doc 区分度可能不够 | build_text_doc 把 visual_signature + recommended_for + keywords 都拼进去 |

## 12. 关键决策记录

| 决策 | 结论 |
|---|---|
| kb 命名 | `library/visual-patterns/` + `library/pptx-templates/` (双词 hyphen) |
| 内部骨架 | items/ + meta.yaml + preview.png + _source/(对称) |
| 源文件位置 | 都进 `_source/<id>.<ext>` (gitignored) |
| DB | 单文件 `library/_rag/db.sqlite` |
| Schema | 接受业务差异;pptx-templates 双层 templates+pages |
| id 规范 | `vp:<id>` / `tpl:<name>` / `tpl:<name>__<NN-slug>` |
| 唯一入口 | `library/search.sh` router |
| Fallback | preferred-template 优先,< 0.55 或不足 top-k 降级到 vp |

## 13. 实施前置(已完成)

- [x] 清空旧 `templates/` (含 3 份 .pptx · 不可恢复)
- [x] 清空旧 `library/visual-patterns/` (含 21 个 pattern · 可 git checkout 找回)
- [x] 建空骨架目录 `library/visual-patterns/` + `library/pptx-templates/`

下一步交给 `writing-plans` skill 出实施计划。
