# PPTX Templates Library

用户预置的 .pptx 模板知识库(按模板名分类)。被 brainstorm(列模板)、author(选页)、iloveppt-builder(Step 4 加视觉)调用。

## 目录结构

```
library/pptx-templates/
├── README.md  INDEX.md  ingest_workflow.md
├── items/<name>/
│   ├── meta.yaml                      ← 模板级 metadata(入 git)
│   ├── preview.png                    ← cover 缩略图(gitignored · `preview*.png` 规则)
│   └── pages/<NN-slug>/
│       ├── meta.yaml                  ← 页级 metadata(入 git)
│       └── preview.png                ← 该页渲染 PNG(gitignored · 单页 ~100-300KB)
└── _source/<name>.pptx                ← gitignored · build.py:load_theme() 读这里
```

> **注**:`.gitignore` line 17 `preview*.png` 当前忽略全部 preview;line 55 的注释意图是"入 git"但跟当前规则不一致。若要让 items/*/preview.png 入 git,需在 `.gitignore` 加一条 `!library/*/items/**/preview.png` 例外。

每个模板严格 1:1 对应一个 .pptx 源(放 `_source/<name>.pptx`)。

## 用法 · 4 个查询场景

```bash
# A. 语义查模板(默认 text mode · brainstorm 列模板用)
library/search.sh --kb pptx-templates --type template --query "<brief 主题>" --top-k 5
# 例:--query "财务汇报"  → finance_arrow #1
# 例:--query "团队培训"  → training_team #1

# B. 视觉风格查模板(hybrid mode · 强视觉描述时用)
library/search.sh --kb pptx-templates --type template --query "<视觉描述>" --mode hybrid --top-k 5
# 例:--query "极光渐变 黑底高级感" --mode hybrid  → creative_aurora #1
# 例:--query "深蓝金色 城市天际线" --mode hybrid  → enterprise_skyline #1

# C. 图查相似页(image mode · 用户给参考图 / builder 检查视觉一致性)
library/search.sh --kb pptx-templates --type page --query-image <PNG-path> --mode image --top-k 5
# 例:--query-image mockup.png --type page  → 视觉最像的 5 张 page,跨所有模板
# 例:--query-image mockup.png --preferred-template finance_arrow --type page  → 限 finance_arrow 内找相似页

# D. 模板内选页(author Stage C 选页)
library/search.sh --query "<本页意图>" --preferred-template <name> --type page --top-k 5
# 例:--query "5 阶段串行" --preferred-template enterprise_skyline --type page
```

**Query 静态扩展自动开**:短 query 撞库补同领域词(`财务` → `+财报 +营收 +利润 +CFO ...`)。完整触发表见 `library/search.py:EXPANSION_HINTS`。`--no-expand` 关。

**hybrid 权重**:默认 text 0.6 + image 0.4。视觉风格强时调成 `--text-weight 0.4 --image-weight 0.6`。

完整 `--help`:`library/search.sh --help`

## load_theme 集成

`.claude/skills/pptx-deck/build.py:load_theme(name)` 第 4 位查找 `library/pptx-templates/_source/<name>.pptx`。

## ingest 流程

见 [`ingest_workflow.md`](ingest_workflow.md)。
