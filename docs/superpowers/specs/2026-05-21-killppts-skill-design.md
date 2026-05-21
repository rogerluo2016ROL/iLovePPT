# KillPPTs Skill 库设计文档（v2）

**日期**：2026-05-21
**作者**：brainstorm 协作产出
**状态**：待实现
**来源**：参考 `/Users/pc2026/Documents/DevAgents/AppGenesisForge/.claude/skills/{pptx, agf-writing-pptx-reports}` 全量去 AGF 化迁入,并按"端到端 PPT 生成器"目标重构

---

## 1. 项目定位（v2 调整）

KillPPTs 的目标：**复制人类快速生成 PPT 的能力**——用户输入主题/要点（或给出参考 .pptx）,skill 自动产出完整 .pptx,包括拓写每页文案、生成架构图、套用风格,并通过 LLM 视觉能力**逐页自检与优化**。

不再是被动的"工具集",而是**端到端生成器**。

## 2. 三 Skill 架构

### 2.1 职责矩阵

| Skill | 触发场景 | 触发关键词 | 核心产物 |
|---|---|---|---|
| **`pptx-deck`** | 端到端生成；给主题/要点/brief.yaml/参考 .pptx | PPT / 演示 / deck / 汇报 / 路演 / 提案 / brief.yaml | 完整 .pptx + 视觉自检通过 |
| **`pptx`** | 只读已有 PPT、模板局部改、底层 helper 调用 | 读取 .pptx / 提取 / unpack / 修改 slide | 文本/结构/局部修改 |
| **`diagram`** | 单独要架构图 / 流程图 / 数据可视化 | 架构图 / 流程图 / mermaid / draw.io / 可视化 | PNG/SVG 图 |

### 2.2 调用关系

```
pptx-deck  ─┬─ 调 pptx skill（helpers.py / scripts/office / template ingest）
            └─ 调 diagram skill（架构图 → PNG → 嵌入）

pptx       ─── 独立可用（只读 / 局部改场景）
diagram    ─── 独立可用（单独出图场景）
```

### 2.3 顶层目录

```
KillPPTs/
├── README.md                          # 项目目标 + 三 skill 入口 + 一句话 demo
├── .gitignore
├── docs/superpowers/specs/            # spec 落地
└── skills/
    ├── pptx-deck/                     # 主入口：端到端生成
    │   ├── SKILL.md
    │   ├── workflow.md
    │   ├── content-writing.md
    │   ├── visual-qa.md
    │   ├── template-ingest.md
    │   ├── themes/
    │   │   ├── __init__.py
    │   │   └── tech_blue.py
    │   ├── brief.example.yaml
    │   └── examples/
    │       ├── demo_brief.yaml
    │       └── sample_output.pptx
    ├── pptx/                          # 底层读写
    │   ├── SKILL.md
    │   ├── creating.md
    │   ├── editing.md
    │   ├── reading.md
    │   ├── design-system.md
    │   ├── helpers.py
    │   ├── examples/minimal_deck.py
    │   └── scripts/
    │       ├── thumbnail.py
    │       ├── clean.py
    │       ├── add_slide.py
    │       ├── check_deps.sh
    │       └── office/
    │           ├── unpack.py
    │           ├── pack.py
    │           ├── soffice.py
    │           ├── validate.py
    │           ├── validators/
    │           ├── schemas/
    │           └── helpers/
    └── diagram/                       # 独立图层
        ├── SKILL.md
        ├── drawio.md
        ├── mermaid.md
        ├── matplotlib.md
        ├── pptx-native.md
        └── examples/
            ├── minimal.drawio
            └── render.sh
```

## 3. Skill: `pptx-deck`（主入口）

### 3.1 frontmatter description

> 端到端 PPT 生成器。用户给主题/要点/brief.yaml/参考 .pptx 模板,skill 自动产出完整 .pptx：拓写每页文案、生成架构图、套用风格、逐页视觉自检与优化。内置科技蓝主题,支持从用户 .pptx 学风格。触发：做一份 PPT / 帮我写 PPT / 路演 deck / 汇报 / 提案 / brief.yaml / .pptx 模板。

### 3.2 SKILL.md 章节（~250 行）

1. **触发与边界** — 何时用本 skill vs 何时直接用 `[[pptx]]` / `[[diagram]]`
2. **输入接口（双路）** — 自由对话 / brief.yaml
3. **主流程 6 步**（详见 `workflow.md`）
4. **依赖检查** — 调 `[[pptx]]` scripts/check_deps.sh
5. **共识 token** — 与 `[[pptx]]` design-system.md 同步
6. **交付前 checklist** — workflow + vision QA 合并 12 项

### 3.3 子文档

#### `workflow.md`（核心,~400 行）

主流程伪代码骨架：

```python
brief = parse_brief(user_input)                  # path A 自由对话 / path B brief.yaml
theme = load_theme(brief.theme) or ingest_template(brief.reference_pptx)
outline = generate_outline(brief, theme)
prs = init_presentation(theme)

for idx, page_spec in enumerate(outline, 1):
    slide = generate_slide(prs, page_spec, theme)
    render_one_slide(prs, idx, "/tmp/preview.png")
    issues = vision_check(image="/tmp/preview.png",
                          expected=page_spec.intent)
    attempts = 0
    while issues and attempts < 3:
        slide = fix_slide(slide, issues)
        render_one_slide(prs, idx, "/tmp/preview.png")
        issues = vision_check(...)
        attempts += 1
    if issues:
        mark_review_needed(slide, issues)        # 降级：标 TODO 继续

deck_review(prs)                                  # 跨页一致性扫描
prs.save(brief.output_path)
```

**关键决策点**：
- 页数估算：brief 未指定时,按 outline 节点数 × 1.5（含章节扉页 + 总结）
- 布局预选：要点数 → 11 种 layout 映射（见 3.4 themes）
- 图表插入：每 4-5 页至少一张图（架构/流程/对比）
- vision_check 失败兜底：单页修 ≤ 3 次后降级为「接受 + TODO 注释」,不死循环

#### `content-writing.md`（~250 行）

每页文案拓写规范：

| 块 | 规则 |
|---|---|
| 封面 | 主标题 ≤ 20 字、副标 ≤ 30 字、不堆作者头衔 |
| 目录页 | 章节列表（与 outline 同步）,数字 + 章节名,1 行 ≤ 20 字 |
| 章节扉页 | 章节号 + 标题,节奏感独立 layout |
| 单点强调 | 1 句话 ≤ 12 字 + 1 个数字（72pt+）+ 1 行解释 |
| 二栏对比 | 左右标题各 ≤ 6 字、并列对照 |
| 三栏卡片 | 卡片标题 ≤ 6 字、body ≤ 30 字、并列 3 块 |
| 五点列表 | 每点 ≤ 14 字、句式一致（动宾对齐） |
| 表格 | 列 ≤ 5、行 ≤ 7、单元格 ≤ 8 字 |
| 图文双视图 | 左图右文,右文 4 卡片每卡 ≤ 20 字 |
| 总结页 | 3-5 个核心结论,每条 ≤ 18 字,有数字佐证 |
| 封底 | "谢谢"+ 联系方式或下一步行动,极简 |

**拓写指令模板**：outline 节点 → `page_spec` JSON（title/layout_type/intent/bullets/visual_element/notes）。

#### `visual-qa.md`（~200 行）

逐页 vision 自检 prompt 模板：

```
你审视的是 PPT 第 {idx}/{total} 页,期望意图：{intent}。
渲染图：{image_path}

请找出以下问题（assume 有问题）：
1. 元素重叠（文字穿过形状、卡片相互覆盖）
2. 文字溢出框 / 被边缘截断
3. 中文字体 fallback 到丑字体
4. 标题与内容区距离失衡（>0.8" 或 <0.3"）
5. 颜色对比度不足
6. layout 与意图不符
7. 数字 / 图表位置偏右 / 偏下（margin 未归零）

输出 JSON：[{issue, severity: low|med|high, suggested_fix}]
若无问题,输出 []。
```

**单页渲染脚本**：`render_one_slide(prs, idx, out_path)` 仅导出该页 PDF → PNG,避免全 deck 渲染（41 页 ~40s vs 单页 ~3s）。

#### `template-ingest.md`（~200 行）

用户给 .pptx 时如何"学风格"：

1. 拷贝到 `/tmp/` 防污染
2. 跑 `[[pptx]] scripts/thumbnail.py` 缩略图 → LLM 看整体风格
3. 跑 `[[pptx]] scripts/office/unpack.py` → XML
4. 从 master / theme 提 design token：
   - 主色 = `theme1.xml` 的 `<a:accent1>` 或封面 shape fill
   - 字体 = master 的 `<a:latin>` + `<a:ea>` typeface
   - layout 命名 = `slideLayout*.xml` 的 `<p:cSld name>`
5. dump slide→layout 映射 + placeholder 信息
6. 生成临时 `ingested_theme.py` 到 `/tmp/`,workflow 加载

**兜底**：模板太复杂（>10 layout 都用过）→ 降级为复用 master + theme,自定义 layout。

#### `themes/tech_blue.py`（~300 行,内置科技蓝主题）

```python
# 字体（默认微软雅黑 + fallback 链）
FONT_HEADER = "Microsoft YaHei"
FONT_BODY   = "Microsoft YaHei"
FONT_NUM    = "Helvetica Neue"
FONT_FALLBACK_CHAIN = [
    "Microsoft YaHei",   # 首选,Windows 原生,办公标配
    "PingFang SC",       # macOS 原生
    "Source Han Sans CN", # 思源黑体（开源）
    "Heiti SC",          # 最老 macOS fallback
]

# 色板（科技蓝）
PRIMARY_DEEP = RGBColor(0x0B, 0x2A, 0x4A)    # 深海蓝
PRIMARY      = RGBColor(0x1E, 0x6F, 0xE0)    # 科技蓝
PRIMARY_TINT = RGBColor(0xE6, 0xF0, 0xFC)    # 浅蓝底
ACCENT       = RGBColor(0x00, 0xD1, 0xC1)    # 青绿点睛
GRAY_900 / GRAY_700 / GRAY_500 / GRAY_300 / GRAY_50 / WHITE = ...

# 11 种 layout 函数
make_cover(prs, title, subtitle)
make_toc(prs, sections)                         # 目录页
make_section_divider(prs, num, title)
make_single_focus(prs, big_text, big_number, explanation)
make_two_col_compare(prs, left_title, left_body, right_title, right_body)
make_three_col_cards(prs, cards)                # cards: List[{title, body}]
make_bullet_list(prs, title, items)             # 5 点列表
make_table(prs, title, headers, rows)
make_pic_text(prs, title, image_path, points)   # 左图右 4 卡片
make_summary(prs, conclusions)                  # 总结页
make_closing(prs, contact_info)                 # 封底
```

每个 layout 函数内嵌：字号、字体修复、卡片样式、margin 归零、word_wrap、line_spacing,调用方零样板代码。

#### `brief.example.yaml`

```yaml
title: "AI 4A 架构评审办法 v1.0"
audience: "技术 + 业务团队,约 30 人"
duration_min: 15
outline:
  - "背景与意义"
  - "评审范围"
  - "评审流程（5 阶段）"
  - "组织保障"
  - "落地节奏"
key_points:
  - "强制嵌入研发流程"
  - "5 阶段评审,每阶段 ≤ 3 天"
  - "AI 助手提前预审"
theme: tech_blue                # 或 path/to/template.pptx
output: ./out/deck.pptx
page_count_target: 20            # 可省略,自动估
brand_color: "#0B2A4A"           # 可省略,走 theme 默认
```

#### `examples/sample_output.pptx`

跑通 `demo_brief.yaml` 的成品参考（~20 页）,作为端到端 smoke test 期望产物。

## 4. Skill: `pptx`（底层读写）

### 4.1 frontmatter description

> .pptx 文件底层读写操作。覆盖：markitdown 提取文本、unpack/pack XML、模板加载与局部修改、跨平台中文字体 EA 字段、LibreOffice 渲染验证。被 `[[pptx-deck]]` 调用作为底层引擎,也可独立用于"只读已有 PPT"或"模板小改"。触发：读取 .pptx / 提取文字 / 解包 .pptx / 改模板 / unpack。

### 4.2 SKILL.md 章节（~180 行）

1. 场景路由表 — 3 种场景（创建/编辑/读取）
2. 依赖检查 — `scripts/check_deps.sh`
3. 路径决策 — 3 选 1（模板局部 / 模板+代码混合 / 全代码）
4. 跨场景共识 — 中文字体 EA、LibreOffice 验证、12 helper 入口
5. 交付前 checklist — 13 通用 + 4 模板专项

### 4.3 子文档

| 文件 | 内容 | 估行数 |
|---|---|---|
| `creating.md` | python-pptx 全定制；7 致丑反模式；12 关键技巧；**中文字体默认微软雅黑 + EA 字段写法 + 跨平台 fallback 链** | ~400 |
| `editing.md` | 模板加载 → clear → 选 layout → 填 placeholder → `_fix_ph_font` → 渲染；Placeholder vs Shape | ~250 |
| `reading.md` | markitdown / unpack / thumbnail / 提取语义结构 | ~180 |
| `design-system.md` | **10 现成色板**（含科技蓝、商务深蓝、党政红、极简白、咨询黑、莫兰迪、薄荷绿、暖橙、灰盐、酒红）+ 字体配对推荐（默认 `Microsoft YaHei + Helvetica Neue`）+ 字号体系 + 12 helper 详解 | ~300 |

### 4.4 helpers.py（核心 helper,被 pptx-deck themes 调用）

```python
# 字体（默认微软雅黑）
set_font(run, *, name="Microsoft YaHei", size=14, bold=False, color)
_fix_ph_font(ph, *, name="Microsoft YaHei", size_pt=14, bold=False, color)

# 模板生命周期
clear_template_slides(prs)

# 视觉元素
card(slide, x, y, w, h, *, fill, border, accent)
bullets(slide, x, y, w, h, items, ...)
table_modern(slide, x, y, w, h, headers, rows, ...)
rect(slide, x, y, w, h, color)
page_decoration(slide, num, tint_color)
section_header(slide, title, num, color)

# 工具
fix_textbox_margins(tf)
no_fill(shape) / no_line(shape)
embed_picture(slide, path, x, y, *, height)
```

### 4.5 scripts/

全量从源 `pptx` skill 拷贝 + 新增 `check_deps.sh`：

| 文件 | 用途 |
|---|---|
| `thumbnail.py` | slide 网格预览 |
| `clean.py` | .pptx 冗余清理 |
| `add_slide.py` | slide 复制工具 |
| `office/unpack.py` / `pack.py` | .pptx ↔ 目录 |
| `office/soffice.py` | LibreOffice headless 封装（自动 sandbox 配置） |
| `office/validate.py` + `validators/` + `schemas/` + `helpers/` | XML schema 校验依赖 |
| **新** `check_deps.sh` | 一键探测 python-pptx / markitdown / soffice / pdftoppm,给安装命令 |

### 4.6 examples/

`minimal_deck.py` — 8 行用 helpers 生成 3 页 .pptx 的 smoke test。

## 5. Skill: `diagram`（独立图层）

### 5.1 frontmatter description

> 生成架构图、流程图、矩阵、决策树、数据可视化。覆盖 draw.io（多层架构/矩阵）、Mermaid（线性流程）、matplotlib（数据驱动）、python-pptx add_shape（slide 内画）四套工具。提供选型决策表、跨平台中文字体（默认微软雅黑）、PNG 嵌入 PPT 链路、8 大致丑坑规避。被 `[[pptx-deck]]` 调用,也可独立产出图。触发：架构图 / 流程图 / 矩阵 / 决策树 / draw.io / mermaid / sequence / 可视化。

### 5.2 SKILL.md 章节（~250 行）

1. 何时用本 skill — 触发信号
2. 工具选型决策表 — 8 种图 → 首选/替代
3. 跨工具共识 — **字体 Microsoft YaHei**、设计 token 与 `[[pptx]]` design-system.md 同步、字号体系（基准 1600×900：标题 28pt / 节点 20-22pt / 注解 16-18pt）、8 大致丑坑速查
4. 嵌入 PPT 链路 — 调 `[[pptx]]` `embed_picture`
5. 批量工作流 — sed 字体替换 + for loop
6. 交付前 checklist — 渲染分辨率 / 字体 / 配色 / 转义 / 边对齐

### 5.3 子文档

| 文件 | 内容 | 估行数 |
|---|---|---|
| `drawio.md` | 安装 + headless CLI（`--width 3200` 必设）；mxGraph XML 最小模板；10 类 Cell；mxGeometry 坐标系；**8 大致丑坑详解**；批量 sed；**默认 fontFamily="Microsoft YaHei"** | ~450 |
| `mermaid.md` | mmdc CLI；flowchart/sequence/class/state；subgraph 配色翻车修复（`%%{init: {themeVariables: {fontFamily: "Microsoft YaHei"}}}%%`） | ~200 |
| `matplotlib.md` | 中文 `rcParams['font.sans-serif'] = ['Microsoft YaHei', 'PingFang SC', ...]`；柱/雷达/仪表盘 3 类模板；输出 DPI 200+；色板与 pptx 同步 | ~200 |
| `pptx-native.md` | slide 内 `add_shape`（≤ 5 节点）；与 `pptx/helpers.py` 联动；何时切到 draw.io | ~120 |

### 5.4 examples/

- `minimal.drawio` — 3 节点 mxGraph XML 样例（fontFamily="Microsoft YaHei"）
- `render.sh` — 调 drawio headless 渲染

### 5.5 与 pptx-deck 的接口

`pptx-deck` 根据 `page_spec.visual_element.type` 决定：

| visual type | 调用方式 |
|---|---|
| `arch_diagram` | drawio.md 流程 → PNG → 嵌入 |
| `flow` | mermaid.md → PNG → 嵌入 |
| `chart` | matplotlib.md → PNG → 嵌入 |
| `simple_relation`（≤ 5 节点） | pptx-native.md slide 内 add_shape（不出 PNG） |

## 6. 跨 Skill 设计 Token 同步

避免"图用 A 字体、PPT 用 B 字体"造成跨页面字体跳变：

**默认 token**（写到三个 skill 的 SKILL.md / design-system.md）：

```
字体首选：Microsoft YaHei（Windows 原生,办公标配）
fallback 链：Microsoft YaHei → PingFang SC → Source Han Sans CN → Heiti SC
图基准尺寸：1600 × 900
字号：标题 28pt / 节点 20-22pt / 注解 16-18pt
配色：使用 pptx skill BRAND_* + GRAY_* 变量,hex 在 design-system.md
```

⚠️ **macOS 渲染验证前**需装微软雅黑（不装则 LibreOffice fallback 到 PingFang SC,与 Windows PowerPoint 显示不一致）。`pptx/creating.md` + `pptx-deck/SKILL.md` + `diagram/SKILL.md` 都要显式提示。

## 7. 错误处理 / 兜底

| 故障 | 兜底位置 | 检测方法 |
|---|---|---|
| brief 字段缺失（path A） | `workflow.md` 字段补齐对话模板 | 必填字段为空 |
| brief.yaml schema 不符 | `workflow.md` yaml 校验 | pydantic validate |
| 用户 .pptx 太复杂（>10 layout 都被用过） | `template-ingest.md` 降级方案 | layout 使用率扫描 |
| 单页 vision_check 修 ≥ 3 次仍失败 | `visual-qa.md` 接受 + TODO 注释 | attempts 计数 |
| LibreOffice 单页渲染失败（iSlide 不识别） | `workflow.md` 跳过 vision,标 review-needed | PNG 不存在 |
| 中文字体 fallback | `pptx/creating.md` EA 字段写法 + 装雅黑提示 | 渲染后看字形 |
| `mmdc`/`drawio` 未装 | 各 SKILL.md 依赖检查 + `check_deps.sh` | `which` 检测 |
| diagram 工具产图失败 | `workflow.md` 降级为 pptx-native add_shape | 退出码 |
| 跨页字体不一致 | `deck_review()` 扫 run-level font 抽样 | 抽样对比 theme |
| .pptx 不可被 PowerPoint 打开 | `pptx/scripts/office/validate.py` schema 校验 | unpack → validate |

**核心容错原则**：单点失败不停 pipeline,降级 + 标 review-needed,让用户最后看清单决定。

## 8. 测试策略

skill 是文档+脚本集,三层验证：

### Layer 1 — 依赖检查
- `pptx/scripts/check_deps.sh` 探测 python-pptx / markitdown / soffice / pdftoppm
- `diagram/SKILL.md` 给 mmdc / drawio brew 安装命令

### Layer 2 — 单 skill smoke test
- `pptx/examples/minimal_deck.py` — 3 页样例,跑通=helper + 字体 + 渲染 OK
- `diagram/examples/render.sh` — 渲染 minimal.drawio,跑通=drawio CLI OK

### Layer 3 — 端到端 smoke test
- `pptx-deck/examples/demo_brief.yaml` + `sample_output.pptx`
- 运行：`python -m pptx_deck.workflow demo_brief.yaml`
- 期望：跑出 .pptx 与仓库内 `sample_output.pptx` 视觉相似
- **不做** byte-level diff（LLM 拓写不可重现）；**不引入** image similarity 度量；**靠人工抽检**

### Layer 4 — 文档级 QA
- workflow 内强制走过 vision QA loop,生产路径自带

## 9. 显式不做（YAGNI）

- ❌ pytest / unittest 单测（skill 不是 Python 库）
- ❌ schema 自动验证整套文档（人审）
- ❌ CI（静态库）
- ❌ npm / pypi 打包
- ❌ 携带 .pptx 模板文件（除 pptx-deck 的 1 个 sample_output 成品）
- ❌ 携带业务样例叙述（GAC 红 / AI 4A 等）
- ❌ web UI / CLI 包装（workflow.md 给 Python 脚本即可）
- ❌ 内置 LLM 调用（拓写 / vision_check 是 LLM 本身做的,skill 只给 prompt 模板）

## 10. 从源 AGF skill 的迁移变化清单

| 维度 | 源 AGF | KillPPTs v2 |
|---|---|---|
| skill 命名 | `pptx` + `agf-writing-pptx-reports` | `pptx-deck` + `pptx` + `diagram` |
| 项目定位 | 工具方法论沉淀 | 端到端 PPT 生成器 |
| 路径 | `.claude/skills/` | `skills/` |
| 业务上下文 | GAC 红 / AI 4A / TopConsultant | 全部删除 |
| 色变量 | `PRIMARY_DEEP = #8B1F24` 业务色 | 抽象 `BRAND_*` / `GRAY_*` + 10 色板供挑 |
| 默认字体 | PingFang SC | **Microsoft YaHei**（含 fallback 链） |
| 模板 | 依赖 5 个 `.pptx` 模板 | 1 个内置 theme（`tech_blue.py`）+ 1 个 sample 成品；支持用户给 .pptx 走 template-ingest |
| diagram 内容 | 嵌在 `agf-writing-pptx-reports` 子文档 | 独立 `skills/diagram/` |
| vision 闭环 | 文档化的"5 步调试 cycle"末尾跑 | **逐页生成 + 逐页 vision 自检**主循环（核心架构） |
| 内容拓写能力 | 无（用户自己给文字） | `pptx-deck/content-writing.md` 完整规范 |
| 风格学习 | 无 | `template-ingest.md` 从用户 .pptx 提 token |
| 输入接口 | 无 | brief.yaml schema + 自由对话双路 |
| 实战章节 | "沉淀自《AI 4A 架构评审办法》" | 删除业务叙述 |

## 11. 实现顺序建议

1. 仓库初始化（README、.gitignore）
2. 拷 `pptx/scripts/` 全量 + `check_deps.sh`
3. 改写 `pptx/helpers.py`（去 AGF + 默认 Microsoft YaHei）
4. 写 `pptx/SKILL.md` → 4 子文档（含 design-system.md 的 10 色板与字体配对）
5. 写 `pptx/examples/minimal_deck.py` smoke test
6. 写 `diagram/SKILL.md` → 4 子文档（含 8 致丑坑 / 默认字体设置）
7. 写 `diagram/examples/{minimal.drawio, render.sh}`
8. 写 `pptx-deck/themes/tech_blue.py`（11 layout + 色板 + 字体）
9. 写 `pptx-deck/SKILL.md` → 4 子文档（workflow / content-writing / visual-qa / template-ingest）
10. 写 `pptx-deck/brief.example.yaml` + `examples/demo_brief.yaml`
11. 跑端到端：`demo_brief.yaml` → `sample_output.pptx`,人工抽检
12. 互引核对（pptx-deck → pptx / diagram；diagram → pptx）
13. README 写三 skill 入口 + 一行 demo 命令
