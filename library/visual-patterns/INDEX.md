# Visual Patterns 索引

> **给 author / designer 用** —— Read 全文 + 按 content intent 选 pattern → Read 对应 pattern.yaml 看细节。
> **库小时(< 30 pattern)**直接读这份 INDEX 选;**库大时**用 `python3 search.py --query "..."` RAG 检索。
>
> 维护:加新 pattern 后,本文件 + `_rag/embed_text.py` 一起更新。

---

## 索引规则

每个 entry 一行:`id` · 类别 · `n_items` · 一句话 intent · **关键词** · **何时用** · **何时不用**

按 category 分组 → 6 类:**process / cycle / comparison / hierarchy / data / relationship**

---

## category: process(顺序 / 步骤 / 流程)

### timeline-3-events
- intent:3 里程碑按**时间顺序**展示,有明确日期
- n_items:3-5
- 关键词:时间轴 / 路线图 / roadmap / 里程碑 / Q1Q2Q3 / 季度
- 用于:项目分 X 阶段有日期 / 公司发展史关键节点
- **不用于**:无日期(改 `wavy-3-steps`)/ 节点 > 5(改 `bullet_list`)
- 匹配现有 layout:**无**(draw.io 现画)

### funnel-3-stage
- intent:3 阶段递减漏斗(转化 / 筛选)
- n_items:3
- 关键词:漏斗 / funnel / 转化 / 销售漏斗 / 招聘漏斗
- 用于:用户转化 / 销售漏斗 / 招聘漏斗
- **不用于**:等权重(改 `cards`)/ > 4 层(漏斗过窄)
- 匹配现有 layout:**无**(draw.io 现画)

### numbered-cards-3
- intent:3 步骤带编号 badge,无时间锚点
- n_items:3
- 关键词:编号 / 步骤 / 1-2-3 / 三步走 / numbered
- 用于:简单 3-step 流程,无 timeline 复杂度
- **不用于**:有日期(`timeline-3-events`)/ 等权重(`cards`)/ journey 感(`wavy-3-steps`)
- 匹配现有 layout:**cards**(加编号前缀 OK,完整 badge 需扩展 make_cards)

### wavy-3-steps
- intent:3 步骤 + **有机进程感**(非严格时序),journey 风
- n_items:3
- 关键词:波浪 / journey / 演进 / 流动 / organic
- 用于:用户 onboarding journey / 产品演进路径
- **不用于**:有日期(`timeline`)/ 强制步骤(`numbered-cards`)
- 匹配现有 layout:**无**(draw.io 现画)

---

## category: cycle(循环 / 闭环)

### cycle-donut-3
- intent:3 阶段循环,等权重环形布局
- n_items:3
- 关键词:循环 / 闭环 / 环形 / donut / cycle
- 用于:敏捷 sprint(plan/do/retro)/ 营销闭环(吸引/转化/留存)
- **不用于**:多轮迭代(`pdca-loop`)/ 段数 ≠ 3(`cards` 或 `compare_pk`)
- 匹配现有 layout:**无**(draw.io 现画)

### triangle-cycle-3
- intent:3 段循环 + 中心三角形(强调互锁 / 稳定)
- n_items:3
- 关键词:三角 / 三要素 / 互锁 / trade-off / 平衡 / 金三角
- 用于:trade-off 三角(成本/质量/速度)/ 战略三要素
- **不用于**:并列点(`cards`)/ 时序(`timeline`)
- 匹配现有 layout:**无**(draw.io 现画)

### pdca-loop
- intent:PDCA **N 轮迭代**展示(持续改进)
- n_items:variable(typical 3-5 轮)
- 关键词:PDCA / 戴明环 / 持续改进 / 迭代 / sprint / 复盘
- 用于:PDCA 方法论 / 多轮迭代复盘
- **不用于**:单次循环(`cycle-donut-3` 更简洁)
- 匹配现有 layout:**无**(draw.io 现画)

---

## category: comparison(对比 / 对决)
*暂无入库 pattern · 用现有 layout `compare` / `compare_pk` / `matrix_2x2`*

---

## category: hierarchy(层级 / 结构)

### triangle-3-elements
- intent:3 独立同型组件(支柱 / 鼎立)
- n_items:3
- 关键词:三角 / 三支柱 / pillars / 三大 / 同型对等
- 用于:战略 3 大支柱 / 产品 3 大模块
- **不用于**:有顺序(`timeline` / `wavy-3-steps`)/ 互锁(`triangle-cycle-3`)
- 匹配现有 layout:**无**(draw.io 现画;但跟 `cards` 接近)

---

## category: data(数据 / 图表)
*用 `skills/diagram/matplotlib_rc.py` 现画 · 不在本 library 范围*

---

## category: relationship(关系 / 互动)

### photo-with-3-points
- intent:左照片 + 右 3 编号点(上下文化 3 要点)
- n_items:3
- 关键词:图文 / 照片 / hero image / pic+text / 案例 / 场景
- 用于:章节扉页 / 客户案例 / 团队介绍
- **不用于**:无合适照片(改 `cards`)/ 数据为主(改 `pic_text` 带 chart)
- 匹配现有 layout:**pic_text**(直接套用,加编号前缀)

### two-loop-flow
- intent:2 实体 A↔B 双向往返 + 4 角描述
- n_items:2 main + 4 supporting
- 关键词:双向 / 互锁 / 反馈循环 / feedback loop / 供需 / 双圆 / bidirectional
- 用于:供需 / DevOps 开发↔运维 / 持续协作关系
- **不用于**:单向流(改 `cards`)/ 3 方(改 `triangle-cycle-3`)/ 对立(改 `compare_pk`)
- 匹配现有 layout:**无**(draw.io 现画;**别套 `compare_pk`**,语义不同)

---

## author / designer 怎么用

### 拓写 / 加视觉时(简版,< 30 pattern):

1. 想清楚 page 的 content intent(2-3 个关键词)
2. Read 本 INDEX.md 全文
3. 按 category + content_intent 匹配最相似 pattern
4. Read 对应 `patterns/<id>/pattern.yaml` 看完整细节
5. 在 content.md 嵌入 `<!-- pattern: <id> -->` 注释
6. 按 fallback_rendering.method 决定怎么画:
   - `python_make_func` + `matches_iloveppt_layout`:套现成 layout
   - `drawio_template`:调 `[[diagram]]` skill 现画 draw.io
   - `manual`:author 自己决定怎么实现(可现画 / 可用近似 layout)

### 库大时(50+ pattern):用 RAG

```bash
python3 library/visual-patterns/search.py \
    --query "<page content intent>" \
    --category <optional> \
    --top-k 5 \
    --format json
# 拿 top-5 → Read 各 pattern.yaml → 选 → 嵌入注释
```

---

## 入库新 pattern 流程

见 `ingest_workflow.md`。简版:
- 用户给 .pptx 或 PNG → 我推断 pattern.yaml 草稿 → 用户审 → 入 `patterns/<id>/` → 跑 `_rag/embed_text.py` 重生 vec DB → **更新本 INDEX.md**

**每加一个 pattern,本 INDEX.md 必须同步加 entry**(否则 LLM 选不到)。
