# KillPPTs Skill 库实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建三层 PPT 生成 skill 库（`pptx-deck` 端到端 / `pptx` 底层读写 / `diagram` 独立图层）,在 `/Users/pc2026/Documents/DevTools/KillPPTs/skills/` 下落地,能从 brief.yaml 跑出 .pptx 成品并通过逐页视觉自检。

**Architecture:** 三 skill 静态库,`pptx-deck` 调用 `pptx`+`diagram` 作为底层,helpers.py 单源在 `pptx/`。所有文档+脚本不需要运行时,通过文件路径引用与 plugin 化分发。

**Tech Stack:** Python 3.11+（`python-pptx`、`lxml`、`pyyaml`、`pydantic`）、draw.io CLI（macOS cask）、mermaid CLI (`mmdc`)、`matplotlib`、LibreOffice (`soffice`)、`poppler` (`pdftoppm`)、`markitdown`。

**Spec source of truth:** `docs/superpowers/specs/2026-05-21-killppts-skill-design.md`。Plan 在叙述上不重复 spec 内容,只给文件路径、关键代码骨架、验证命令。

**关于字体的注意:** spec 明确默认 `Microsoft YaHei`（用户指定）。macOS 渲染验证前需装雅黑,否则 LibreOffice 会 fallback 到 PingFang SC,与 Windows PowerPoint 显示不一致。每个写字体的文档都要显式提示。

---

## File Structure（来自 spec §2.3,实施时严格对齐）

```
KillPPTs/
├── README.md
├── .gitignore
├── docs/superpowers/{specs,plans}/        # 已存在
└── skills/
    ├── pptx-deck/
    │   ├── SKILL.md
    │   ├── workflow.md
    │   ├── content-writing.md
    │   ├── visual-qa.md
    │   ├── template-ingest.md
    │   ├── themes/__init__.py
    │   ├── themes/tech_blue.py
    │   ├── brief.example.yaml
    │   └── examples/
    │       ├── demo_brief.yaml
    │       └── sample_output.pptx        # 任务 13 产物
    ├── pptx/
    │   ├── SKILL.md
    │   ├── creating.md
    │   ├── editing.md
    │   ├── reading.md
    │   ├── design-system.md
    │   ├── helpers.py
    │   ├── examples/minimal_deck.py
    │   └── scripts/
    │       ├── thumbnail.py              # 拷贝
    │       ├── clean.py                  # 拷贝
    │       ├── add_slide.py              # 拷贝
    │       ├── check_deps.sh             # 新写
    │       └── office/
    │           ├── unpack.py             # 拷贝
    │           ├── pack.py               # 拷贝
    │           ├── soffice.py            # 拷贝
    │           ├── validate.py           # 拷贝
    │           ├── validators/           # 拷贝
    │           ├── schemas/              # 拷贝
    │           └── helpers/              # 拷贝
    └── diagram/
        ├── SKILL.md
        ├── drawio.md
        ├── mermaid.md
        ├── matplotlib.md
        ├── pptx-native.md
        └── examples/
            ├── minimal.drawio
            └── render.sh
```

**文档"完成"标准**：行数在 spec §3-5 给出的估算范围内（±30%）、章节标题与 spec 一致、关键代码片段可直接粘贴跑通、所有 `[[name]]` skill 互引无死链。

---

## Task 1：仓库初始化

**Files:**
- Create: `/Users/pc2026/Documents/DevTools/KillPPTs/.gitignore`
- Create: `/Users/pc2026/Documents/DevTools/KillPPTs/README.md`
- Create: `/Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck/themes/__init__.py`（空文件）
- Create: `/Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck/examples/.gitkeep`
- Create: `/Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx/examples/.gitkeep`
- Create: `/Users/pc2026/Documents/DevTools/KillPPTs/skills/diagram/examples/.gitkeep`

- [ ] **Step 1: 写 `.gitignore`**

```
__pycache__/
*.pyc
*.pyo
.DS_Store
.venv/
venv/
.idea/
.vscode/
/tmp/
*.swp

# 渲染验证产物（生产路径会产生大量临时 .pdf .png）
/out/
*.pdf
slide-*.jpg
slide-*.png
preview*.png
thumbnails-*.jpg

# 但保留示例产物
!skills/pptx-deck/examples/sample_output.pptx
```

- [ ] **Step 2: 写最小 `README.md`**（详细版到 Task 15 再补）

```markdown
# KillPPTs

端到端 PPT 生成 skill 库。

## Skills
- `skills/pptx-deck/` — 端到端生成器：brief → 完整 .pptx
- `skills/pptx/` — 底层 .pptx 读写
- `skills/diagram/` — 架构图/流程图/可视化

详见 `docs/superpowers/specs/2026-05-21-killppts-skill-design.md`。
```

- [ ] **Step 3: 创建空目录占位**

```bash
mkdir -p /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck/themes
mkdir -p /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck/examples
mkdir -p /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx/examples
mkdir -p /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx/scripts/office
mkdir -p /Users/pc2026/Documents/DevTools/KillPPTs/skills/diagram/examples
touch /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck/themes/__init__.py
touch /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck/examples/.gitkeep
touch /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx/examples/.gitkeep
touch /Users/pc2026/Documents/DevTools/KillPPTs/skills/diagram/examples/.gitkeep
```

- [ ] **Step 4: git init + 首次 commit**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
git init
git add .gitignore README.md docs/ skills/
git commit -m "chore: bootstrap KillPPTs skill repo"
```

---

## Task 2：拷贝 pptx scripts/ + 写 check_deps.sh

**Files:**
- Copy: 源 `/Users/pc2026/Documents/DevAgents/AppGenesisForge/.claude/skills/pptx/scripts/` 全部内容到 `/Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx/scripts/`
- Create: `skills/pptx/scripts/check_deps.sh`

- [ ] **Step 1: 拷贝脚本（剔除 `__pycache__`）**

```bash
SRC=/Users/pc2026/Documents/DevAgents/AppGenesisForge/.claude/skills/pptx/scripts
DST=/Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx/scripts
cp "$SRC"/__init__.py "$DST"/
cp "$SRC"/thumbnail.py "$DST"/
cp "$SRC"/clean.py "$DST"/
cp "$SRC"/add_slide.py "$DST"/
cp -R "$SRC"/office "$DST"/
find "$DST" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
```

- [ ] **Step 2: 写 `check_deps.sh`**

```bash
#!/usr/bin/env bash
# 一键探测 pptx skill 依赖

set -e
echo "== KillPPTs pptx skill 依赖检查 =="

check_py() {
    if python3 -c "import $1" 2>/dev/null; then
        echo "  ✅ python -m $1"
    else
        echo "  ❌ python -m $1  → pip3 install $2"
    fi
}

check_bin() {
    if command -v "$1" >/dev/null 2>&1; then
        echo "  ✅ $1"
    else
        echo "  ❌ $1  → $2"
    fi
}

check_py pptx python-pptx
check_py lxml lxml
check_py markitdown "'markitdown[pptx]'"
check_py PIL Pillow

check_bin soffice "brew install --cask libreoffice"
check_bin pdftoppm "brew install poppler"

# 字体检查（macOS）
if [[ "$(uname)" == "Darwin" ]]; then
    if fc-list 2>/dev/null | grep -qi "microsoft yahei"; then
        echo "  ✅ 微软雅黑"
    else
        echo "  ⚠️  微软雅黑未装（LibreOffice 渲染中文会 fallback）"
        echo "      手动方案：放雅黑字体到 ~/Library/Fonts/，或接受 fallback"
    fi
fi

echo "完成。"
```

- [ ] **Step 3: chmod + 跑通**

```bash
chmod +x /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx/scripts/check_deps.sh
bash /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx/scripts/check_deps.sh
```

期望：输出 ✅/❌ 列表,缺啥装啥。本步若有 ❌,先 `pip3 install python-pptx lxml 'markitdown[pptx]' Pillow` + `brew install --cask libreoffice` + `brew install poppler`,再重跑。

- [ ] **Step 4: commit**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
git add skills/pptx/scripts/
git commit -m "feat(pptx): copy office scripts and add check_deps.sh"
```

---

## Task 3：写 `pptx/helpers.py`

**Files:**
- Create: `skills/pptx/helpers.py`
- Create: `tests/pptx/test_helpers.py`（仅本任务存在用于 TDD,后续可保留）

**说明**：源 `template.py`（604 行）含 GAC 红色板与 Heiti SC 字体。本任务是基于源做"去 AGF + 默认 Microsoft YaHei + 抽象品牌色"的改造,产出 ~500 行的通用 helpers.py。

- [ ] **Step 1: 写测试骨架**

```python
# tests/pptx/test_helpers.py
"""helpers.py 视觉代码 light test：验证 shape 数量、字体名、color、文字内容。
真正的"长得对不对"由 examples/minimal_deck.py 视觉 smoke test 验证。"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../skills/pptx"))

from pptx import Presentation
from pptx.util import Inches
import helpers as H


def _new_prs():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def test_set_font_writes_ea_typeface():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    tb = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(3), Inches(1))
    run = tb.text_frame.paragraphs[0].add_run()
    run.text = "中文测试"
    H.set_font(run, name="Microsoft YaHei", size=14)
    # 检查 <a:ea> 写入
    from pptx.oxml.ns import qn
    rPr = run._r.find(qn("a:rPr"))
    ea = rPr.find(qn("a:ea"))
    assert ea is not None, "set_font 必须写 <a:ea>"
    assert ea.get("typeface") == "Microsoft YaHei"


def test_card_creates_rounded_rect():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    n_before = len(slide.shapes)
    H.card(slide, Inches(1), Inches(1), Inches(4), Inches(1.5),
           fill=H.WHITE, border=H.GRAY_300)
    assert len(slide.shapes) == n_before + 1


def test_card_with_accent_creates_two_shapes():
    prs = _new_prs()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    n_before = len(slide.shapes)
    H.card(slide, Inches(1), Inches(1), Inches(4), Inches(1.5),
           fill=H.WHITE, border=H.GRAY_300, accent=H.BRAND_PRIMARY)
    assert len(slide.shapes) == n_before + 2  # 圆角矩 + 左色条


def test_default_brand_palette_defined():
    # 验证 10 色变量都存在
    for c in ["BRAND_PRIMARY", "BRAND_DARK", "BRAND_TINT", "ACCENT",
              "GRAY_900", "GRAY_700", "GRAY_500", "GRAY_300", "GRAY_50", "WHITE"]:
        assert hasattr(H, c), f"missing color: {c}"
```

- [ ] **Step 2: 跑测试验证 fail**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
python3 -m pytest tests/pptx/test_helpers.py -v
```

期望：4 个 FAIL（`ModuleNotFoundError: helpers`）。

- [ ] **Step 3: 写 `skills/pptx/helpers.py`**

完整代码（基于源 `template.py` 去 AGF 化 + 默认 Microsoft YaHei,删除 GAC 红色板与样例 deck 生成,保留 helper 全套）：

```python
"""KillPPTs pptx skill — 核心 helper 集合。

被 pptx-deck/themes/*.py 调用作为 layout 底层；也可单独 import 用于
"从零创建 PPT"或"模板局部改"场景。

设计原则：
- 单一品牌色 + 灰阶（10 色变量）
- 中文字体 lxml 写 <a:ea>（跨平台不 fallback）
- textbox margin 归零 + word_wrap 显式
- 表格关 firstRow/bandRow + 手动斑马纹
"""

from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt


# ============================================================================
# 1. 设计 token
# ============================================================================

# 字体默认 Microsoft YaHei（Windows 原生,办公标配）
# macOS 渲染验证前请装雅黑；未装则 LibreOffice 会 fallback 到 PingFang SC
FONT_CN = "Microsoft YaHei"
FONT_EN = "Helvetica Neue"
FONT_NUM = "Helvetica Neue"

FONT_FALLBACK_CHAIN = (
    "Microsoft YaHei",
    "PingFang SC",
    "Source Han Sans CN",
    "Heiti SC",
)

# 抽象品牌色（默认科技蓝；其他色板见 design-system.md）
BRAND_PRIMARY = RGBColor(0x1E, 0x6F, 0xE0)  # 科技蓝
BRAND_DARK    = RGBColor(0x0B, 0x2A, 0x4A)  # 深海蓝
BRAND_TINT    = RGBColor(0xE6, 0xF0, 0xFC)  # 浅蓝底
ACCENT        = RGBColor(0x00, 0xD1, 0xC1)  # 青绿点睛

GRAY_900 = RGBColor(0x1A, 0x1A, 0x1A)
GRAY_700 = RGBColor(0x4A, 0x4A, 0x4A)
GRAY_500 = RGBColor(0x8C, 0x8C, 0x8C)
GRAY_300 = RGBColor(0xD9, 0xD9, 0xD9)
GRAY_50  = RGBColor(0xFA, 0xFA, 0xFA)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
BLACK    = RGBColor(0x00, 0x00, 0x00)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
LEFT_MARGIN  = Inches(0.55)
RIGHT_MARGIN = Inches(0.55)
HEADER_BOTTOM = Inches(1.4)
FOOTER_TOP    = Inches(7.0)


# ============================================================================
# 2. 字体工具
# ============================================================================

def set_font(run, *, name=FONT_CN, size=14, bold=False, italic=False, color=GRAY_900):
    """设置 run 字体；用 lxml 写 <a:ea>+<a:cs>,中文跨平台不 fallback。

    适用：你自己 add_textbox 加的 textbox 的 run。
    placeholder（layout 自带）请用 _fix_ph_font(ph, ...)。
    """
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        elem = rPr.find(qn(tag))
        if elem is None:
            elem = etree.SubElement(rPr, qn(tag))
        elem.set("typeface", name)


def _fix_ph_font(ph, *, name=FONT_CN, size_pt=14, bold=False, color=GRAY_900):
    """修 placeholder 字体。set_font 只能改 run 级 latin,改不到 master 的 <a:ea>。"""
    for p in ph.text_frame.paragraphs:
        for run in p.runs:
            set_font(run, name=name, size=size_pt, bold=bold, color=color)


# ============================================================================
# 3. 模板生命周期
# ============================================================================

def clear_template_slides(prs):
    """清空模板自带样例 slide,保留 layout / master / theme。"""
    sldIdLst = prs.slides._sldIdLst
    for sldId in list(sldIdLst):
        sldIdLst.remove(sldId)
    # 同时清 rels 防孤儿引用
    part = prs.part
    for rel_id in list(part.rels):
        rel = part.rels[rel_id]
        if "slide" in rel.reltype and "slideLayout" not in rel.reltype and "slideMaster" not in rel.reltype:
            part.drop_rel(rel_id)


# ============================================================================
# 4. 视觉元素 helper
# ============================================================================

def fix_textbox_margins(tf):
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)


def no_fill(shape):
    shape.fill.background()


def no_line(shape):
    shape.line.fill.background()


def rect(slide, x, y, w, h, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    no_line(shape)
    return shape


def card(slide, x, y, w, h, *, fill=WHITE, border=GRAY_300, accent=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = border
    shape.line.width = Pt(0.75)
    shape.adjustments[0] = 0.05
    if accent:
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Emu(36000), h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        no_line(bar)
    return shape


def bullets(slide, x, y, w, h, items, *, size=14,
            accent_color=BRAND_PRIMARY, body_color=GRAY_900):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    fix_textbox_margins(tf)
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.45
        r1 = p.add_run(); r1.text = "▎ "
        set_font(r1, size=size, color=accent_color, bold=True)
        r2 = p.add_run(); r2.text = item
        set_font(r2, size=size, color=body_color)
    return box


def table_modern(slide, x, y, w, h, headers, rows, *,
                 header_fill=BRAND_DARK, header_color=WHITE,
                 body_color=GRAY_900, zebra=GRAY_50, font_size=11,
                 row_height=Inches(0.5)):
    tbl_shape = slide.shapes.add_table(len(rows) + 1, len(headers), x, y, w, h)
    tbl = tbl_shape.table
    for row in tbl.rows:
        row.height = row_height
    tblPr = tbl._tbl.find(qn("a:tblPr"))
    if tblPr is not None:
        tblPr.set("firstRow", "0")
        tblPr.set("bandRow", "0")
    # 表头
    for j, h_text in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid(); cell.fill.fore_color.rgb = header_fill
        tf = cell.text_frame
        tf.text = h_text
        for run in tf.paragraphs[0].runs:
            set_font(run, size=font_size, bold=True, color=header_color)
    # body
    for i, row in enumerate(rows):
        for j, txt in enumerate(row):
            cell = tbl.cell(i + 1, j)
            if i % 2 == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = zebra
            tf = cell.text_frame
            tf.text = str(txt)
            for run in tf.paragraphs[0].runs:
                set_font(run, size=font_size, color=body_color)
    return tbl_shape


def page_decoration(slide, num, tint_color, *, x=Inches(8.8), y=Inches(0.25),
                    w=Inches(4.4), h=Inches(2.0), size=140):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    fix_textbox_margins(tf)
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    p.line_spacing = 1.0
    r = p.add_run()
    r.text = str(num)
    set_font(r, name=FONT_NUM, size=size, bold=True, color=tint_color)
    return box


def section_header(slide, title, num, color):
    """章节扉页：左大色块 + 大数字 + 标题。"""
    rect(slide, Inches(0.55), Inches(1.9), Inches(1.7), Inches(2.0), color)
    box = slide.shapes.add_textbox(Inches(0.55), Inches(1.9), Inches(1.7), Inches(2.0))
    tf = box.text_frame
    fix_textbox_margins(tf)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(num)
    set_font(r, name=FONT_NUM, size=80, bold=True, color=WHITE)

    box2 = slide.shapes.add_textbox(Inches(2.55), Inches(2.3), Inches(10), Inches(1.2))
    tf2 = box2.text_frame
    fix_textbox_margins(tf2)
    r2 = tf2.paragraphs[0].add_run(); r2.text = title
    set_font(r2, size=36, bold=True, color=color)
    return box, box2


def embed_picture(slide, path, x, y, *, height=None, width=None):
    if height is not None:
        return slide.shapes.add_picture(str(path), x, y, height=height)
    if width is not None:
        return slide.shapes.add_picture(str(path), x, y, width=width)
    return slide.shapes.add_picture(str(path), x, y)
```

- [ ] **Step 4: 跑测试验证 pass**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
python3 -m pytest tests/pptx/test_helpers.py -v
```

期望：4 PASS。

- [ ] **Step 5: commit**

```bash
git add skills/pptx/helpers.py tests/pptx/test_helpers.py
git commit -m "feat(pptx): add helpers.py with Microsoft YaHei default"
```

---

## Task 4：`pptx/examples/minimal_deck.py` smoke test

**Files:**
- Create: `skills/pptx/examples/minimal_deck.py`

- [ ] **Step 1: 写脚本**

```python
"""pptx skill smoke test — 8 行核心代码生成 3 页 .pptx。

跑通=helper + 字体 EA + 渲染管线 OK。

依赖：python-pptx, lxml,（可选验证）soffice + pdftoppm
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pptx import Presentation
from pptx.util import Inches
import helpers as H


def main(out="/tmp/killppts_minimal.pptx"):
    prs = Presentation()
    prs.slide_width = H.SLIDE_W
    prs.slide_height = H.SLIDE_H

    # 页 1：封面
    s = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    H.rect(s, 0, 0, H.SLIDE_W, H.SLIDE_H, H.BRAND_DARK)
    box = s.shapes.add_textbox(Inches(0.55), Inches(2.8), Inches(12), Inches(2))
    H.fix_textbox_margins(box.text_frame)
    r = box.text_frame.paragraphs[0].add_run()
    r.text = "KillPPTs minimal smoke test"
    H.set_font(r, size=44, bold=True, color=H.WHITE)

    # 页 2：内容（card + bullets）
    s = prs.slides.add_slide(prs.slide_layouts[6])
    H.card(s, Inches(0.55), Inches(1.4), Inches(12.2), Inches(5.6),
           fill=H.BRAND_TINT, border=H.GRAY_300, accent=H.BRAND_PRIMARY)
    H.bullets(s, Inches(1.0), Inches(1.7), Inches(11), Inches(5),
              items=["验证 EA 字段中文不 fallback",
                     "验证 textbox margin 归零",
                     "验证 card 圆角 + 左色条",
                     "验证 bullet ▎ 现代风"])

    # 页 3：表格
    s = prs.slides.add_slide(prs.slide_layouts[6])
    H.table_modern(s, Inches(0.55), Inches(1.4), Inches(12.2), Inches(3),
                   headers=["指标", "Q1", "Q2", "Q3"],
                   rows=[["收入", "100", "120", "150"],
                         ["利润", "20", "25", "32"],
                         ["客户数", "8", "12", "18"]])

    prs.save(out)
    print(f"✅ saved: {out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 跑生成**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
python3 skills/pptx/examples/minimal_deck.py
```

期望：输出 `✅ saved: /tmp/killppts_minimal.pptx`。

- [ ] **Step 3: 渲染验证（视觉 smoke test）**

```bash
cd /tmp && rm -rf killppts_preview && mkdir killppts_preview && cd killppts_preview
soffice --headless --convert-to pdf /tmp/killppts_minimal.pptx
pdftoppm -jpeg -r 120 killppts_minimal.pdf slide
ls slide-*.jpg
```

期望：3 张 jpg。用 Read tool 看 slide-01.jpg / slide-02.jpg / slide-03.jpg,确认：

- slide-01：深蓝底 + 白色英文标题不糊
- slide-02：浅蓝卡片 + 4 行 bullets + 中文字体不 fallback（如果 macOS 没装雅黑,会 fallback 但可识别）
- slide-03：表格无 banding 横纹 + 斑马纹仅奇数行 + 表头深底白字

如视觉异常,定位到 helpers.py 对应函数修复并回 Task 3 重跑测试。

- [ ] **Step 4: commit**

```bash
git add skills/pptx/examples/minimal_deck.py
git commit -m "test(pptx): add minimal_deck.py smoke test"
```

---

## Task 5：`pptx/` 全部文档（SKILL.md + 4 子文档）

**Files:**
- Create: `skills/pptx/SKILL.md`（~180 行）
- Create: `skills/pptx/creating.md`（~400 行）
- Create: `skills/pptx/editing.md`（~250 行）
- Create: `skills/pptx/reading.md`（~180 行）
- Create: `skills/pptx/design-system.md`（~300 行）

**说明**：本任务把 spec §4 全部铺开成文档。每文档遵循 spec 章节结构与行数预算。所有代码片段必须可直接粘贴跑通,所有 `[[name]]` 互引保持一致。

- [ ] **Step 1: 写 `creating.md`**

骨架（按 spec §4.3 与源 `agf-writing-pptx-reports/SKILL.md` 的「7 致丑反模式」+「12 关键技巧」节铺开,去除 GAC 红/AI 4A 业务叙述）：

```markdown
# 从零创建 .pptx（python-pptx 全定制路径）

## 何时走本路径
- 没有现成 .pptx 模板
- 视觉风格自定义,要程序化重生成
- 跨平台中文输出（Windows + macOS）
- 23+ 页量级

## 工具链（macOS 实测）
| 用途 | 工具 | 装法 |
|---|---|---|
| PPT 生成 | python-pptx ≥ 1.0 | `pip3 install python-pptx lxml` |
| PPT → PDF | soffice | `brew install --cask libreoffice` |
| PDF → PNG | pdftoppm (poppler) | `brew install poppler` |

## ⚠️ 中文字体（最致命的坑）

默认 `font.name` 只写 `<a:latin>`,中文跨平台 fallback。必须用 lxml 写 `<a:ea>`+`<a:cs>`。
本 skill 默认 `Microsoft YaHei`（见 `helpers.py` `set_font`）。

**macOS 渲染验证前请装雅黑**：将 .ttf 放入 `~/Library/Fonts/`,否则 LibreOffice fallback 到 PingFang SC,与 Windows PowerPoint 显示不一致。

[完整 EA 字段代码引用 helpers.py:set_font / _fix_ph_font]

## Placeholder vs Shape
[参考源 agf-writing-pptx-reports/SKILL.md Step 2 表格]

## 7 致丑反模式
[完整拷贝源 §「7 个致丑反模式」表格,删除任何业务叙述]

## 12 关键技巧
[完整拷贝源 §「12 个关键技巧」,代码引用 helpers.py 已有函数,不重复实现]
1. 中文字体跨平台生效 — 引用 helpers.py:set_font
2. textbox margin 归零 — 引用 helpers.py:fix_textbox_margins
3. 大字号装饰数字防换行 — 引用 helpers.py:page_decoration
4. 表格行高 + 关闭 banding — 引用 helpers.py:table_modern
5. shape 真无填充/无边框 — 引用 helpers.py:no_fill/no_line
6. 卡片化 — 引用 helpers.py:card
7. 现代 bullet ▎ — 引用 helpers.py:bullets
8. 字号层级（封面 44-54 / 标题 28 / 正文 14）
9. 留白边界（左右 0.55"、标题区 1.4"、页脚 7.0"）
10. 双视图嵌入图 + 卡片
11. 阶段流程 layout
12. 单一品牌色覆盖

## 迭代验证 5 步循环
[soffice → pdftoppm → Read → 修 → 回 step 1]
```

acceptance: 文件存在,跑 `wc -l skills/pptx/creating.md` 在 [280, 520] 范围；grep 关键词 `set_font` `_fix_ph_font` `Microsoft YaHei` 都命中。

- [ ] **Step 2: 写 `editing.md`**

骨架（按 spec §4.3,源 agf-writing-pptx-reports/SKILL.md 的「基于已有 .pptx 模板生成」节铺开）：

```markdown
# 基于模板编辑 .pptx

## Step 1 — 模板分析三件套
- python scripts/thumbnail.py path/to/template.pptx --cols 4
- python scripts/office/unpack.py path/to/template.pptx /tmp/unpacked/
- 写 dump 脚本：[骨架代码]

## Step 2 — Placeholder vs Shape 概念区分
[参考源表格]

## Step 3 — 加载模板 + clear_template_slides
[helpers.py:clear_template_slides 用法]

## Step 4 — 选 layout + 填 placeholder + 修字体
[helpers.py:_fix_ph_font 用法]

## Step 5 — 内容页 layout[5] 空白画布 + add_shape
[helpers.py:card / bullets / table_modern 联动]

## Step 6 — LibreOffice 不渲染部分 slide 兜底
[iSlide 工具页问题]

## Step 7 — 渲染验证 5 步循环
[同 creating.md 引用]
```

acceptance: 跑 `wc -l skills/pptx/editing.md` 在 [175, 325]；grep `clear_template_slides` `_fix_ph_font` 命中。

- [ ] **Step 3: 写 `reading.md`**

```markdown
# 读取 .pptx 提取内容

## 文字提取
python -m markitdown deck.pptx

## 视觉概览
python scripts/thumbnail.py deck.pptx

## 原始 XML 结构
python scripts/office/unpack.py deck.pptx /tmp/unpacked/

## 提取语义结构（slide → layout 映射 + placeholder 信息）
[dump 脚本骨架]

## 何时配合其他 skill
- 模板局部改：→ editing.md
- 用作 pptx-deck 学风格：→ [[pptx-deck]] template-ingest.md
```

acceptance: 跑 `wc -l skills/pptx/reading.md` 在 [125, 235]；grep `markitdown` `thumbnail` `unpack` 都命中。

- [ ] **Step 4: 写 `design-system.md`**（最重要的设计文档）

```markdown
# 设计系统：色板 / 字体 / 字号 / 12 helper 详解

## 10 现成色板（按主题列出）

| 主题 | BRAND_PRIMARY | BRAND_DARK | BRAND_TINT | ACCENT |
|---|---|---|---|---|
| **科技蓝**（默认） | #1E6FE0 | #0B2A4A | #E6F0FC | #00D1C1 |
| **商务深蓝**（Midnight Executive） | #1E2761 | #0A1234 | #CADCFC | #FFFFFF |
| **党政红**（严肃中式） | #8B1F24 | #5E0E14 | #FBE5E7 | #EC0A1E |
| **极简白**（高端 pitch） | #212121 | #000000 | #F5F5F5 | #FF6B35 |
| **咨询黑**（McKinsey 风） | #1A1A1A | #000000 | #E0E0E0 | #C99A4D |
| **莫兰迪灰** | #6D6D6D | #3D3D3D | #E8E4E0 | #B85042 |
| **薄荷绿**（消费品） | #028090 | #00A896 | #D6F0EE | #F0C808 |
| **暖橙**（活力创业） | #F96167 | #C73E1D | #FFEDDB | #2F3C7E |
| **灰盐**（学术） | #50808E | #2C3E50 | #ECEFF1 | #E8A87C |
| **酒红**（品质零售） | #6D2E46 | #4A1F30 | #ECE2D0 | #C99A4D |

切换色板：在 helpers.py 顶部 4 个 BRAND_* 常量改 RGBColor 值,全 deck 联动。

## 字体配对（默认 Microsoft YaHei）

| 角色 | 字体 |
|---|---|
| 中文标题/正文 | Microsoft YaHei |
| 英文/数字装饰 | Helvetica Neue |
| Fallback 链 | Microsoft YaHei → PingFang SC → Source Han Sans CN → Heiti SC |

⚠️ macOS 渲染前装雅黑（详见 creating.md）。

## 字号体系（16:9 = 13.333 × 7.5 in）
[完整表格：封面 44-54 / 章节扉页 36-40 / H2 20-28 / H3 14-18 / 正文 11.5-14 / 表格 10.5-12 / 页脚 8.5-10 / 装饰 120-150]

## 留白 layout
[完整左右 0.55、HEADER_BOTTOM 1.4、FOOTER_TOP 7.0、CONTENT_W/H 计算]

## 12 helper 详解（每个：签名 + 用例 + 何时不该用）
[逐个：set_font / _fix_ph_font / clear_template_slides / fix_textbox_margins
 / no_fill / no_line / rect / card / bullets / table_modern / page_decoration
 / section_header / embed_picture]
```

acceptance: 10 色板 × 4 列 hex 与本步表格一致；helper 列表覆盖 helpers.py 全部 public 函数（grep `def [a-z]` skills/pptx/helpers.py 与文档对照）。

- [ ] **Step 5: 写 `SKILL.md`**

```markdown
---
name: pptx
description: .pptx 文件底层读写操作。覆盖 markitdown 提取文本、unpack/pack XML、模板加载与局部修改、跨平台中文字体 EA 字段、LibreOffice 渲染验证。被 [[pptx-deck]] 调用,也可独立用于"只读已有 PPT"或"模板小改"。触发：读取 .pptx / 提取文字 / 解包 .pptx / 改模板 / unpack / 演示文稿 / 幻灯片。
---

# pptx skill — .pptx 读写底层

## 场景路由
| 场景 | 子文档 |
|---|---|
| 从零创建 | [creating.md](creating.md) |
| 模板编辑 | [editing.md](editing.md) |
| 提取内容 | [reading.md](reading.md) |
| 设计参考 | [design-system.md](design-system.md) |

## 依赖检查
`bash scripts/check_deps.sh`

## 路径决策
| 路径 | 何时选 |
|---|---|
| 模板局部改 | 已有 .pptx,改 ≤ 5 张文字 |
| 模板 + 代码混合 | 有模板,需版本化重生成 |
| python-pptx 全定制 | 无模板,跨平台中文,23+ 页 |

## 跨场景共识
- 中文字体默认 Microsoft YaHei,EA 字段必写（helpers.py:set_font / _fix_ph_font）
- LibreOffice 渲染 PDF + pdftoppm PNG 验证闭环
- 12 helper 入口见 [design-system.md](design-system.md)

## 交付前 checklist
[13 项通用 + 4 项模板专项,从源拷贝去 AGF 化]
```

acceptance: frontmatter `name: pptx` 与 description 完整；4 子文档链接 + scripts/check_deps.sh 都能命中。

- [ ] **Step 6: commit**

```bash
git add skills/pptx/*.md
git commit -m "docs(pptx): write SKILL.md + 4 child docs"
```

---

## Task 6：diagram skill smoke test（先跑通工具链）

**Files:**
- Create: `skills/diagram/examples/minimal.drawio`
- Create: `skills/diagram/examples/render.sh`

- [ ] **Step 1: 写 `minimal.drawio`**

```xml
<mxfile host="app.diagrams.net" version="30.0.1">
  <diagram name="killppts-minimal" id="D1">
    <mxGraphModel dx="1600" dy="900" page="1" pageWidth="1600" pageHeight="900">
      <root>
        <mxCell id="0" /><mxCell id="1" parent="0" />
        <mxCell id="n1" value="输入" vertex="1" parent="1"
                style="rounded=1;fillColor=#1E6FE0;strokeColor=#1E6FE0;fontColor=#FFFFFF;fontSize=20;fontFamily=Microsoft YaHei;fontStyle=1;strokeWidth=2;arcSize=10;">
          <mxGeometry x="200" y="400" width="240" height="80" as="geometry" />
        </mxCell>
        <mxCell id="n2" value="处理" vertex="1" parent="1"
                style="rounded=1;fillColor=#00D1C1;strokeColor=#00D1C1;fontColor=#0B2A4A;fontSize=20;fontFamily=Microsoft YaHei;fontStyle=1;strokeWidth=2;arcSize=10;">
          <mxGeometry x="680" y="400" width="240" height="80" as="geometry" />
        </mxCell>
        <mxCell id="n3" value="输出" vertex="1" parent="1"
                style="rounded=1;fillColor=#0B2A4A;strokeColor=#0B2A4A;fontColor=#FFFFFF;fontSize=20;fontFamily=Microsoft YaHei;fontStyle=1;strokeWidth=2;arcSize=10;">
          <mxGeometry x="1160" y="400" width="240" height="80" as="geometry" />
        </mxCell>
        <mxCell id="e1" edge="1" parent="1" source="n1" target="n2"
                style="endArrow=classic;endFill=1;endSize=14;strokeColor=#0B2A4A;strokeWidth=2.5;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" edge="1" parent="1" source="n2" target="n3"
                style="endArrow=classic;endFill=1;endSize=14;strokeColor=#0B2A4A;strokeWidth=2.5;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

- [ ] **Step 2: 写 `render.sh`**

```bash
#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRAWIO="/Applications/draw.io.app/Contents/MacOS/drawio"

if [ ! -x "$DRAWIO" ]; then
    echo "❌ draw.io 未装。运行: brew install --cask drawio"
    exit 1
fi

cd "$SCRIPT_DIR"
"$DRAWIO" --export --format png --width 3200 \
    --output minimal.png minimal.drawio

echo "✅ 渲染产物：$SCRIPT_DIR/minimal.png"
```

- [ ] **Step 3: chmod + 跑通**

```bash
chmod +x /Users/pc2026/Documents/DevTools/KillPPTs/skills/diagram/examples/render.sh
bash /Users/pc2026/Documents/DevTools/KillPPTs/skills/diagram/examples/render.sh
```

期望：输出 `✅ 渲染产物：.../minimal.png`,且 minimal.png 文件存在、≥ 50KB（避免 800px 默认糊图）。

```bash
ls -lh /Users/pc2026/Documents/DevTools/KillPPTs/skills/diagram/examples/minimal.png
```

用 Read tool 看 minimal.png：3 个圆角节点 + 2 个箭头,中文字体不糊（如未装雅黑,字体会 fallback 但仍清晰）。

- [ ] **Step 4: commit**

```bash
git add skills/diagram/examples/
git commit -m "test(diagram): add minimal.drawio smoke test"
```

---

## Task 7：diagram 全部文档（SKILL.md + 4 子文档）

**Files:**
- Create: `skills/diagram/SKILL.md`（~250 行）
- Create: `skills/diagram/drawio.md`（~450 行）
- Create: `skills/diagram/mermaid.md`（~200 行）
- Create: `skills/diagram/matplotlib.md`（~200 行）
- Create: `skills/diagram/pptx-native.md`（~120 行）

**说明**：本任务把 spec §5 全部铺开。`drawio.md` 大部分内容直接取自源 `agf-writing-pptx-reports/diagram-generation-guide.md`,去除 AGF / GAC / 41 张图叙述,**字体默认改为 Microsoft YaHei**。

- [ ] **Step 1: 写 `drawio.md`**

骨架按源 `diagram-generation-guide.md` 节构,核心改动：
- 全文 `PingFang SC` 替换为 `Microsoft YaHei`
- 删除「沉淀自 AGF 内部培训 deck v2.2 实战」叙述
- 保留 mxGraph XML 最小模板、10 Cell 类型、`--width 3200`、8 大致丑坑、批量 sed
- 加一节"嵌入 PPT 链路"引用 `[[pptx]]` 的 `embed_picture`

acceptance: 跑 `wc -l skills/diagram/drawio.md` 在 [315, 585]；grep `Microsoft YaHei` `--width 3200` `mxGraphModel` 都命中；grep `PingFang SC` 仅出现在 fallback 链上下文（≤ 3 次）。

- [ ] **Step 2: 写 `mermaid.md`**

骨架：
```markdown
# Mermaid 出图

## 安装
brew install mermaid-cli

## 工具选型决策
当节点 ≤ 6 + 单层流程 → mermaid（drawio overkill）

## 4 种图模板
- flowchart: [完整示例]
- sequence: [完整示例]
- class: [完整示例]
- state: [完整示例]

## 默认主题改字体
%%{init: {'theme':'base', 'themeVariables': {'fontFamily': 'Microsoft YaHei'}}}%%

## subgraph 配色翻车修复
[themeVariables.primaryColor / lineColor 设置]

## 出图命令
mmdc -i diag.mmd -o diag.png -w 2400 -H 1800 -b transparent

## 嵌入 PPT
[引用 [[pptx]] helpers.py:embed_picture]
```

acceptance: 跑 `wc -l skills/diagram/mermaid.md` 在 [140, 260]；grep `mmdc` `themeVariables` `Microsoft YaHei` 都命中。

- [ ] **Step 3: 写 `matplotlib.md`**

骨架：
```markdown
# matplotlib 数据可视化

## 中文字体配置
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'PingFang SC', 'Source Han Sans CN']
matplotlib.rcParams['axes.unicode_minus'] = False

## 色板与 pptx 同步
[引用 [[pptx]]/design-system.md 的 BRAND_* hex]

## 3 类常用图模板
- 柱状图: [完整代码]
- 雷达图: [完整代码]
- 仪表盘: [完整代码]

## 输出 DPI ≥ 200
plt.savefig("out.png", dpi=200, bbox_inches='tight')

## 嵌入 PPT
[引用 [[pptx]] helpers.py:embed_picture]
```

acceptance: `wc -l` 在 [140, 260]；grep `rcParams` `font.sans-serif` `Microsoft YaHei` 都命中。

- [ ] **Step 4: 写 `pptx-native.md`**

骨架：
```markdown
# slide 内直接 add_shape 画简单关系图

## 何时用
- 节点 ≤ 5
- 已经在 pptx skill 流程内,不想跳出去出 PNG
- 需要 PowerPoint 打开后可编辑（draw.io 出 PNG 不可编辑）

## 限制
- 节点 > 5 → 切 draw.io（精确坐标管理累）
- 嵌套层次 → 切 draw.io（subgraph）

## 与 helpers.py 联动
[引用 card / rect / textbox / 箭头线 add_connector]

## 示例：3 节点流程
[完整代码 60-80 行]
```

acceptance: `wc -l` 在 [85, 155]；grep `add_shape` `add_connector` `[[pptx]]` 都命中。

- [ ] **Step 5: 写 `SKILL.md`**

```markdown
---
name: diagram
description: 生成架构图、流程图、矩阵、决策树、数据可视化。覆盖 draw.io（多层架构/矩阵）、Mermaid（线性流程）、matplotlib（数据驱动）、python-pptx add_shape（slide 内画）四套工具。提供选型决策表、跨平台中文字体（默认 Microsoft YaHei）、PNG 嵌入 PPT 链路、8 大致丑坑规避。被 [[pptx-deck]] 调用,也可独立产出图。触发：架构图 / 流程图 / 矩阵 / 决策树 / draw.io / mermaid / sequence / 可视化。
---

# diagram skill — 架构图与可视化

## 工具选型决策
[8 种图 × 首选/替代/切换阈值表,来源 spec §5.2]

## 跨工具共识
- 字体默认 Microsoft YaHei,与 [[pptx]] 同步
- 渲染基准 1600 × 900；字号：标题 28 / 节点 20-22 / 注解 16-18
- 色板与 [[pptx]] design-system.md BRAND_* 同步

## 子文档
- [drawio.md](drawio.md)
- [mermaid.md](mermaid.md)
- [matplotlib.md](matplotlib.md)
- [pptx-native.md](pptx-native.md)

## 8 大致丑坑速查
[1) Heiti SC 老派 → 用 Microsoft YaHei
 2) sketch hatch
 3) 长英文换行
 4) 默认 800px 糊
 5) &#xa; 换行
 6) XML 转义
 7) edge 坐标失稳
 8) emoji LibreOffice fallback]

## 嵌入 PPT 链路
[引用 [[pptx]] helpers.py:embed_picture]

## 依赖检查
| 工具 | 检测 | 装法 |
|---|---|---|
| drawio CLI | `which drawio` | brew install --cask drawio |
| mmdc | `which mmdc` | brew install mermaid-cli |
| matplotlib | `python -c 'import matplotlib'` | pip3 install matplotlib |

## 交付前 checklist
[渲染分辨率 / 字体 / 配色 / 转义 / 边对齐]
```

acceptance: frontmatter 完整；4 子文档链接命中。

- [ ] **Step 6: commit**

```bash
git add skills/diagram/*.md
git commit -m "docs(diagram): write SKILL.md + 4 child docs"
```

---

## Task 8：`pptx-deck/themes/tech_blue.py`（11 layout）

**Files:**
- Create: `skills/pptx-deck/themes/tech_blue.py`
- Create: `tests/pptx_deck/test_tech_blue.py`

- [ ] **Step 1: 写测试**

```python
# tests/pptx_deck/test_tech_blue.py
"""tech_blue 主题 11 layout light test：验证每个 layout 创建后 prs.slides 增加 1。"""
import os, sys
ROOT = os.path.join(os.path.dirname(__file__), "../../skills")
sys.path.insert(0, os.path.join(ROOT, "pptx"))
sys.path.insert(0, os.path.join(ROOT, "pptx-deck"))

from pptx import Presentation
from pptx.util import Inches
from themes import tech_blue as T


def _new():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def test_make_cover():
    prs = _new()
    T.make_cover(prs, "主标题", "副标题")
    assert len(prs.slides) == 1

def test_make_toc():
    prs = _new()
    T.make_toc(prs, sections=["背景", "范围", "流程", "保障", "节奏"])
    assert len(prs.slides) == 1

def test_make_section_divider():
    prs = _new()
    T.make_section_divider(prs, 1, "第一章")
    assert len(prs.slides) == 1

def test_make_single_focus():
    prs = _new()
    T.make_single_focus(prs, big_text="一句话", big_number="80%", explanation="解释")
    assert len(prs.slides) == 1

def test_make_two_col_compare():
    prs = _new()
    T.make_two_col_compare(prs, "现状", "现状描述", "目标", "目标描述")
    assert len(prs.slides) == 1

def test_make_three_col_cards():
    prs = _new()
    T.make_three_col_cards(prs, cards=[
        {"title": "卡1", "body": "正文1"},
        {"title": "卡2", "body": "正文2"},
        {"title": "卡3", "body": "正文3"},
    ])
    assert len(prs.slides) == 1

def test_make_bullet_list():
    prs = _new()
    T.make_bullet_list(prs, "标题", items=["要点1", "要点2", "要点3", "要点4", "要点5"])
    assert len(prs.slides) == 1

def test_make_table():
    prs = _new()
    T.make_table(prs, "表格标题",
                 headers=["A", "B", "C"],
                 rows=[["1", "2", "3"], ["4", "5", "6"]])
    assert len(prs.slides) == 1

def test_make_pic_text(tmp_path):
    import shutil
    # 用 minimal_deck.py 的副产物或一个空白 1x1 png
    import struct, zlib
    def make_blank_png(path):
        # 极小白色 PNG（10x10）
        from PIL import Image
        img = Image.new("RGB", (10, 10), "white")
        img.save(str(path))
    img_path = tmp_path / "blank.png"
    make_blank_png(img_path)
    prs = _new()
    T.make_pic_text(prs, "标题", str(img_path),
                    points=[{"title": "点1", "body": "正文1"},
                            {"title": "点2", "body": "正文2"}])
    assert len(prs.slides) == 1

def test_make_summary():
    prs = _new()
    T.make_summary(prs, conclusions=["结论 1", "结论 2", "结论 3"])
    assert len(prs.slides) == 1

def test_make_closing():
    prs = _new()
    T.make_closing(prs, contact_info="联系邮箱：x@y.com")
    assert len(prs.slides) == 1

def test_font_default_is_microsoft_yahei():
    assert T.FONT_HEADER == "Microsoft YaHei"
    assert T.FONT_BODY == "Microsoft YaHei"
```

- [ ] **Step 2: 跑测试验证 fail**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
python3 -m pytest tests/pptx_deck/test_tech_blue.py -v
```

期望：12 FAIL（`ModuleNotFoundError: themes` 或函数未定义）。

- [ ] **Step 3: 写 `tech_blue.py`**

文件骨架（11 layout 函数依赖 `pptx/helpers.py`）：

```python
"""KillPPTs pptx-deck — 内置科技蓝主题。

调用 [[pptx]]/helpers.py 作为底层。11 个 layout 函数对应 spec §3.4。
默认字体 Microsoft YaHei（用户决策）。
"""
import os, sys
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "../../pptx"))

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

import helpers as H


# ===== 字体（默认微软雅黑）=====
FONT_HEADER = "Microsoft YaHei"
FONT_BODY   = "Microsoft YaHei"
FONT_NUM    = "Helvetica Neue"

# ===== 色板（科技蓝）=====
PRIMARY_DEEP = RGBColor(0x0B, 0x2A, 0x4A)
PRIMARY      = RGBColor(0x1E, 0x6F, 0xE0)
PRIMARY_TINT = RGBColor(0xE6, 0xF0, 0xFC)
ACCENT       = RGBColor(0x00, 0xD1, 0xC1)
# Gray 沿用 helpers.py


def _blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def _add_title(slide, text, *, y=Inches(0.6), size=28, color=PRIMARY_DEEP):
    box = slide.shapes.add_textbox(Inches(0.55), y, Inches(12.2), Inches(0.8))
    tf = box.text_frame
    H.fix_textbox_margins(tf)
    r = tf.paragraphs[0].add_run()
    r.text = text
    H.set_font(r, name=FONT_HEADER, size=size, bold=True, color=color)
    return box


def make_cover(prs, title, subtitle):
    s = _blank_slide(prs)
    H.rect(s, 0, 0, H.SLIDE_W, H.SLIDE_H, PRIMARY_DEEP)
    # 大主标题
    box = s.shapes.add_textbox(Inches(0.55), Inches(2.8), Inches(12), Inches(1.8))
    H.fix_textbox_margins(box.text_frame)
    r = box.text_frame.paragraphs[0].add_run()
    r.text = title
    H.set_font(r, name=FONT_HEADER, size=48, bold=True, color=H.WHITE)
    # 副标
    box2 = s.shapes.add_textbox(Inches(0.55), Inches(4.6), Inches(12), Inches(0.8))
    H.fix_textbox_margins(box2.text_frame)
    r2 = box2.text_frame.paragraphs[0].add_run()
    r2.text = subtitle
    H.set_font(r2, name=FONT_HEADER, size=20, color=PRIMARY_TINT)
    return s


def make_toc(prs, sections):
    """目录页：左侧大字"目录" + 右侧 N 行章节,每行编号 + 标题。"""
    s = _blank_slide(prs)
    _add_title(s, "目录", size=40, y=Inches(0.6), color=PRIMARY_DEEP)
    for i, sec in enumerate(sections):
        y = Inches(1.8 + i * 0.7)
        # 编号
        n_box = s.shapes.add_textbox(Inches(1.5), y, Inches(0.7), Inches(0.6))
        H.fix_textbox_margins(n_box.text_frame)
        r = n_box.text_frame.paragraphs[0].add_run()
        r.text = f"{i+1:02d}"
        H.set_font(r, name=FONT_NUM, size=26, bold=True, color=PRIMARY)
        # 标题
        t_box = s.shapes.add_textbox(Inches(2.4), y, Inches(10), Inches(0.6))
        H.fix_textbox_margins(t_box.text_frame)
        r2 = t_box.text_frame.paragraphs[0].add_run()
        r2.text = sec
        H.set_font(r2, name=FONT_HEADER, size=20, color=H.GRAY_900)
    return s


def make_section_divider(prs, num, title):
    s = _blank_slide(prs)
    H.section_header(s, title, num, PRIMARY_DEEP)
    return s


def make_single_focus(prs, *, big_text="", big_number="", explanation=""):
    s = _blank_slide(prs)
    # 大数字
    box = s.shapes.add_textbox(Inches(0.55), Inches(2.0), Inches(12), Inches(2.5))
    H.fix_textbox_margins(box.text_frame)
    p = box.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = big_number
    H.set_font(r, name=FONT_NUM, size=120, bold=True, color=PRIMARY)
    # 大文字
    box2 = s.shapes.add_textbox(Inches(0.55), Inches(4.5), Inches(12), Inches(1.0))
    H.fix_textbox_margins(box2.text_frame)
    p2 = box2.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = big_text
    H.set_font(r2, name=FONT_HEADER, size=32, bold=True, color=PRIMARY_DEEP)
    # 解释
    box3 = s.shapes.add_textbox(Inches(0.55), Inches(5.6), Inches(12), Inches(0.6))
    H.fix_textbox_margins(box3.text_frame)
    p3 = box3.text_frame.paragraphs[0]
    p3.alignment = PP_ALIGN.CENTER
    r3 = p3.add_run(); r3.text = explanation
    H.set_font(r3, name=FONT_HEADER, size=14, color=H.GRAY_500)
    return s


def make_two_col_compare(prs, left_title, left_body, right_title, right_body):
    s = _blank_slide(prs)
    _add_title(s, "对比", size=28)
    # 左
    H.card(s, Inches(0.55), Inches(1.8), Inches(6.0), Inches(5.2),
           fill=PRIMARY_TINT, border=H.GRAY_300, accent=PRIMARY)
    lt = s.shapes.add_textbox(Inches(0.85), Inches(2.0), Inches(5.4), Inches(0.6))
    H.fix_textbox_margins(lt.text_frame)
    r = lt.text_frame.paragraphs[0].add_run()
    r.text = left_title
    H.set_font(r, name=FONT_HEADER, size=20, bold=True, color=PRIMARY_DEEP)
    lb = s.shapes.add_textbox(Inches(0.85), Inches(2.8), Inches(5.4), Inches(4.0))
    H.fix_textbox_margins(lb.text_frame)
    r2 = lb.text_frame.paragraphs[0].add_run()
    r2.text = left_body
    H.set_font(r2, name=FONT_BODY, size=14, color=H.GRAY_900)
    # 右
    H.card(s, Inches(6.78), Inches(1.8), Inches(6.0), Inches(5.2),
           fill=H.WHITE, border=H.GRAY_300, accent=ACCENT)
    rt = s.shapes.add_textbox(Inches(7.08), Inches(2.0), Inches(5.4), Inches(0.6))
    H.fix_textbox_margins(rt.text_frame)
    r3 = rt.text_frame.paragraphs[0].add_run()
    r3.text = right_title
    H.set_font(r3, name=FONT_HEADER, size=20, bold=True, color=PRIMARY_DEEP)
    rb = s.shapes.add_textbox(Inches(7.08), Inches(2.8), Inches(5.4), Inches(4.0))
    H.fix_textbox_margins(rb.text_frame)
    r4 = rb.text_frame.paragraphs[0].add_run()
    r4.text = right_body
    H.set_font(r4, name=FONT_BODY, size=14, color=H.GRAY_900)
    return s


def make_three_col_cards(prs, cards, title="三栏"):
    s = _blank_slide(prs)
    _add_title(s, title, size=28)
    for i, c in enumerate(cards[:3]):
        x = Inches(0.55 + i * 4.15)
        H.card(s, x, Inches(1.8), Inches(3.85), Inches(5.0),
               fill=H.WHITE, border=H.GRAY_300, accent=PRIMARY if i % 2 == 0 else ACCENT)
        t = s.shapes.add_textbox(x + Inches(0.3), Inches(2.0), Inches(3.4), Inches(0.6))
        H.fix_textbox_margins(t.text_frame)
        r = t.text_frame.paragraphs[0].add_run()
        r.text = c["title"]
        H.set_font(r, name=FONT_HEADER, size=18, bold=True, color=PRIMARY_DEEP)
        b = s.shapes.add_textbox(x + Inches(0.3), Inches(2.8), Inches(3.4), Inches(3.8))
        H.fix_textbox_margins(b.text_frame)
        r2 = b.text_frame.paragraphs[0].add_run()
        r2.text = c["body"]
        H.set_font(r2, name=FONT_BODY, size=13, color=H.GRAY_900)
    return s


def make_bullet_list(prs, title, items):
    s = _blank_slide(prs)
    _add_title(s, title, size=28)
    H.bullets(s, Inches(0.55), Inches(1.8), Inches(12.2), Inches(5.2),
              items=items, size=16, accent_color=PRIMARY, body_color=H.GRAY_900)
    return s


def make_table(prs, title, headers, rows):
    s = _blank_slide(prs)
    _add_title(s, title, size=28)
    H.table_modern(s, Inches(0.55), Inches(1.8), Inches(12.2), Inches(4.0),
                   headers=headers, rows=rows,
                   header_fill=PRIMARY_DEEP, header_color=H.WHITE,
                   zebra=PRIMARY_TINT, font_size=12)
    return s


def make_pic_text(prs, title, image_path, points):
    s = _blank_slide(prs)
    _add_title(s, title, size=28)
    H.embed_picture(s, image_path, Inches(0.55), Inches(1.9), height=Inches(5.0))
    # 右 4 卡片
    for i, p in enumerate(points[:4]):
        y = Inches(2.0 + i * 1.15)
        H.card(s, Inches(7.0), y, Inches(5.78), Inches(0.95),
               fill=H.WHITE, border=H.GRAY_300, accent=PRIMARY)
        t = s.shapes.add_textbox(Inches(7.3), y + Inches(0.1), Inches(5.4), Inches(0.4))
        H.fix_textbox_margins(t.text_frame)
        r = t.text_frame.paragraphs[0].add_run()
        r.text = p["title"]
        H.set_font(r, name=FONT_HEADER, size=14, bold=True, color=PRIMARY_DEEP)
        b = s.shapes.add_textbox(Inches(7.3), y + Inches(0.45), Inches(5.4), Inches(0.45))
        H.fix_textbox_margins(b.text_frame)
        r2 = b.text_frame.paragraphs[0].add_run()
        r2.text = p["body"]
        H.set_font(r2, name=FONT_BODY, size=11, color=H.GRAY_700)
    return s


def make_summary(prs, conclusions, title="核心结论"):
    s = _blank_slide(prs)
    _add_title(s, title, size=32, color=PRIMARY_DEEP)
    for i, c in enumerate(conclusions[:5]):
        y = Inches(1.9 + i * 1.0)
        # 序号大色块
        H.rect(s, Inches(0.55), y, Inches(0.9), Inches(0.85), PRIMARY)
        n_box = s.shapes.add_textbox(Inches(0.55), y, Inches(0.9), Inches(0.85))
        H.fix_textbox_margins(n_box.text_frame)
        p = n_box.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = str(i + 1)
        H.set_font(r, name=FONT_NUM, size=32, bold=True, color=H.WHITE)
        # 结论文字
        t = s.shapes.add_textbox(Inches(1.7), y + Inches(0.18), Inches(11), Inches(0.6))
        H.fix_textbox_margins(t.text_frame)
        r2 = t.text_frame.paragraphs[0].add_run()
        r2.text = c
        H.set_font(r2, name=FONT_HEADER, size=18, color=H.GRAY_900)
    return s


def make_closing(prs, contact_info="谢谢"):
    s = _blank_slide(prs)
    H.rect(s, 0, 0, H.SLIDE_W, H.SLIDE_H, PRIMARY_DEEP)
    box = s.shapes.add_textbox(Inches(0.55), Inches(3.0), Inches(12), Inches(1.5))
    H.fix_textbox_margins(box.text_frame)
    p = box.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = "谢谢"
    H.set_font(r, name=FONT_HEADER, size=64, bold=True, color=H.WHITE)
    box2 = s.shapes.add_textbox(Inches(0.55), Inches(4.6), Inches(12), Inches(0.6))
    H.fix_textbox_margins(box2.text_frame)
    p2 = box2.text_frame.paragraphs[0]
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run(); r2.text = contact_info
    H.set_font(r2, name=FONT_BODY, size=16, color=PRIMARY_TINT)
    return s
```

- [ ] **Step 4: 跑测试验证 pass**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
python3 -m pytest tests/pptx_deck/test_tech_blue.py -v
```

期望：12 PASS。

- [ ] **Step 5: 视觉 smoke test（生成 11 页 demo）**

写 `/tmp/test_tech_blue_demo.py`,调用每个 layout 函数生成 11 页 .pptx,然后 soffice 渲染。

```python
# /tmp/test_tech_blue_demo.py
import sys
sys.path.insert(0, "/Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx")
sys.path.insert(0, "/Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck")
from pptx import Presentation
from pptx.util import Inches
from themes import tech_blue as T

prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
T.make_cover(prs, "KillPPTs 主题演示", "tech_blue 11 layout")
T.make_toc(prs, ["背景", "目标", "方法", "数据", "结论"])
T.make_section_divider(prs, 1, "背景")
T.make_single_focus(prs, big_number="80%", big_text="效率提升", explanation="基于实测")
T.make_two_col_compare(prs, "现状", "手工生成,3 天一份", "目标", "自动化,15 分钟一份")
T.make_three_col_cards(prs, [
    {"title": "快", "body": "5 分钟出 deck"},
    {"title": "准", "body": "视觉自检"},
    {"title": "稳", "body": "代码可重生成"}])
T.make_bullet_list(prs, "5 大原则", ["简洁", "数据驱动", "对比清晰", "视觉一致", "可迭代"])
T.make_table(prs, "Q1-Q3 指标", ["指标", "Q1", "Q2", "Q3"],
             [["收入", "100", "120", "150"], ["利润", "20", "25", "32"]])
# pic_text 用 minimal_deck 副产物的某张 png
import subprocess
subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                "/tmp/killppts_minimal.pptx", "--outdir", "/tmp/"], check=True)
subprocess.run(["pdftoppm", "-jpeg", "-r", "100",
                "/tmp/killppts_minimal.pdf", "/tmp/p"], check=True)
T.make_pic_text(prs, "图文双视图", "/tmp/p-2.jpg",
                [{"title": "点 1", "body": "正文"},
                 {"title": "点 2", "body": "正文"},
                 {"title": "点 3", "body": "正文"},
                 {"title": "点 4", "body": "正文"}])
T.make_summary(prs, ["结论 1：自动化 PPT 可行", "结论 2：视觉自检有效",
                     "结论 3：成本下降 80%"])
T.make_closing(prs, "Contact: hello@killppts.dev")
prs.save("/tmp/tech_blue_demo.pptx")
print("✅ /tmp/tech_blue_demo.pptx")
```

跑：
```bash
python3 /tmp/test_tech_blue_demo.py
soffice --headless --convert-to pdf /tmp/tech_blue_demo.pptx --outdir /tmp/
pdftoppm -jpeg -r 100 /tmp/tech_blue_demo.pdf /tmp/tb
ls /tmp/tb-*.jpg | wc -l
```

期望：11 张 jpg。逐张 Read 看：
- 01 封面：深蓝底大白字
- 02 目录：5 行编号 + 章节名
- 03 章节扉页：左大色块大数字 1 + 右标题
- 04 单点强调：超大 80% + 解释
- 05 二栏对比：左右两个卡片对称
- 06 三栏卡片：3 个等宽卡片
- 07 五点列表：5 行 ▎ bullet
- 08 表格：表头深蓝白字、无 banding 横纹
- 09 图文双视图：左图右 4 卡
- 10 总结：5 行序号 + 结论
- 11 封底：深蓝底大字"谢谢"

逐张视觉检查 OK 才能算通过。如有问题修对应 layout 函数后回 Step 4。

- [ ] **Step 6: commit**

```bash
git add skills/pptx-deck/themes/ tests/pptx_deck/test_tech_blue.py
git commit -m "feat(pptx-deck): add tech_blue theme with 11 layouts"
```

---

## Task 9：brief schema + demo_brief.yaml

**Files:**
- Create: `skills/pptx-deck/brief.example.yaml`
- Create: `skills/pptx-deck/examples/demo_brief.yaml`

- [ ] **Step 1: 写 `brief.example.yaml`**（带注释的完整 schema 样例）

```yaml
# KillPPTs pptx-deck brief schema 完整样例
# 必填：title / outline / theme / output
# 可选：subtitle / audience / duration_min / key_points / page_count_target / brand_color / reference_pptx

title: "AI 4A 架构评审办法 v1.0"           # 主标题,≤ 20 字
subtitle: "技术 + 业务 协同评审机制"        # 可选,≤ 30 字
audience: "技术 + 业务团队,约 30 人"        # 可选,影响文案风格
duration_min: 15                            # 可选,影响页数估算
outline:                                    # 必填,章节列表
  - "背景与意义"
  - "评审范围"
  - "评审流程（5 阶段）"
  - "组织保障"
  - "落地节奏"
key_points:                                 # 可选,跨章节关键信息
  - "强制嵌入研发流程"
  - "5 阶段评审,每阶段 ≤ 3 天"
  - "AI 助手提前预审"
theme: tech_blue                            # 必填: 内置主题名 或 .pptx 模板路径
output: ./out/deck.pptx                     # 必填,产物路径
page_count_target: 20                       # 可选,自动估算时省略
brand_color: "#0B2A4A"                      # 可选,覆盖 theme 默认色
reference_pptx: null                        # 可选,用户给参考 .pptx 学风格,走 template-ingest 流程
```

- [ ] **Step 2: 写 `examples/demo_brief.yaml`**（最小可跑 brief,用于 Task 13 端到端 smoke test）

```yaml
title: "KillPPTs 自动化 PPT 生成"
subtitle: "demo brief 跑通整条 pipeline"
outline:
  - "动机"
  - "技术方案"
  - "效果数据"
  - "落地路径"
key_points:
  - "5 分钟生成一份完整 deck"
  - "视觉自检 + 自动修复"
  - "支持模板学风格"
theme: tech_blue
output: /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck/examples/sample_output.pptx
page_count_target: 12
```

- [ ] **Step 3: 验证 yaml 语法**

```bash
python3 -c "import yaml; yaml.safe_load(open('/Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck/brief.example.yaml'))"
python3 -c "import yaml; yaml.safe_load(open('/Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck/examples/demo_brief.yaml'))"
```

期望：无报错。

- [ ] **Step 4: commit**

```bash
git add skills/pptx-deck/brief.example.yaml skills/pptx-deck/examples/demo_brief.yaml
git commit -m "feat(pptx-deck): add brief.yaml schema and demo brief"
```

---

## Task 10：`workflow.md` + 配套可跑 Python 骨架

**Files:**
- Create: `skills/pptx-deck/workflow.md`（~400 行）
- Create: `skills/pptx-deck/workflow.py`（端到端可跑骨架,被 SKILL.md 引用）

**说明**：workflow.md 是 pptx-deck 的核心文档,描述 6 步主流程。workflow.py 是给实施者跑通的端到端骨架（vision_check 占位实现：导出 PNG 后由人工 / LLM 看,不内嵌 LLM 调用）。

- [ ] **Step 1: 写 `workflow.py` 骨架**

```python
"""KillPPTs pptx-deck — 端到端 workflow 骨架。

用法：
    python3 workflow.py path/to/brief.yaml

流程：parse_brief → load_theme → outline → per-slide(generate + render + vision_check) → save
vision_check 当前实现为：导出 PNG,打印路径,等用户/LLM 决定是否过；
真实使用时由 Claude 调本脚本后逐张看图,出 issue JSON 再 fix。
"""
import os, sys, subprocess, json
from pathlib import Path

import yaml
from pptx import Presentation
from pptx.util import Inches

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "../pptx"))
sys.path.insert(0, str(HERE))

import helpers as H
from themes import tech_blue as T


# ----- 1. parse_brief -----

REQUIRED = {"title", "outline", "theme", "output"}


def parse_brief(path):
    with open(path) as f:
        data = yaml.safe_load(f)
    missing = REQUIRED - set(data.keys())
    if missing:
        raise ValueError(f"brief 缺字段: {missing}")
    data.setdefault("subtitle", "")
    data.setdefault("page_count_target", None)
    data.setdefault("key_points", [])
    data.setdefault("reference_pptx", None)
    return data


# ----- 2. load_theme -----

THEMES = {"tech_blue": T}


def load_theme(theme_id):
    if theme_id in THEMES:
        return THEMES[theme_id]
    # 用户给 .pptx 模板 → 走 template-ingest（占位,真实实现见 template-ingest.md）
    if str(theme_id).endswith(".pptx"):
        raise NotImplementedError(
            "template-ingest 走 LLM 流程,见 template-ingest.md;"
            "本骨架先实现 tech_blue 路径"
        )
    raise ValueError(f"未知 theme: {theme_id}")


# ----- 3. outline → page_specs -----

def estimate_page_count(brief):
    if brief["page_count_target"]:
        return brief["page_count_target"]
    return int(len(brief["outline"]) * 1.5) + 4  # +封面 +目录 +总结 +封底


def generate_outline(brief, theme):
    """根据 brief 生成 page_spec list。LLM 在真实运行时会替换此函数。
    本骨架返回固定的简版 outline 跑通 pipeline。"""
    specs = []
    specs.append({"layout": "cover", "title": brief["title"],
                  "subtitle": brief.get("subtitle", "")})
    specs.append({"layout": "toc", "sections": brief["outline"]})
    for i, sec in enumerate(brief["outline"], 1):
        specs.append({"layout": "section_divider", "num": i, "title": sec})
        # 每章 1 页内容（demo 简化）
        specs.append({"layout": "bullet_list", "title": sec,
                      "items": brief.get("key_points", [f"{sec} 要点 1", f"{sec} 要点 2"])[:5]})
    specs.append({"layout": "summary",
                  "conclusions": brief.get("key_points", ["结论 1", "结论 2", "结论 3"])})
    specs.append({"layout": "closing", "contact_info": "谢谢"})
    return specs


# ----- 4. generate_slide -----

def generate_slide(prs, spec, theme):
    fn = getattr(theme, f"make_{spec['layout']}")
    # 去掉 layout key,剩余作为 kwargs
    kwargs = {k: v for k, v in spec.items() if k != "layout"}
    return fn(prs, **kwargs)


# ----- 5. render_one_slide -----

def render_one_slide(prs, idx, out_png):
    """导出全 deck PDF,然后 pdftoppm 仅截第 idx 页。

    优化：可以拆出"单 slide → 单页 .pptx"再 soffice,但 soffice 启动开销 ~1.5s,
    全 deck 渲染 12 页 ~6s,逐页方案首次仍要 ~1.5s+pdftoppm 0.3s。本骨架走简单全渲染。"""
    tmpdir = Path("/tmp/killppts_render")
    tmpdir.mkdir(exist_ok=True)
    pptx_tmp = tmpdir / "current.pptx"
    prs.save(str(pptx_tmp))
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf",
         str(pptx_tmp), "--outdir", str(tmpdir)],
        check=True, capture_output=True,
    )
    pdf = tmpdir / "current.pdf"
    subprocess.run(
        ["pdftoppm", "-jpeg", "-r", "120",
         "-f", str(idx), "-l", str(idx),
         str(pdf), str(tmpdir / "slide_only")],
        check=True, capture_output=True,
    )
    # pdftoppm 输出名 slide_only-{idx}.jpg 或 slide_only-{idx:02d}.jpg
    candidates = list(tmpdir.glob(f"slide_only-{idx}*.jpg"))
    if not candidates:
        raise RuntimeError(f"渲染失败,未找到第 {idx} 页 jpg")
    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    candidates[0].rename(out_png)


def vision_check(image_path, intent):
    """占位实现：打印图像路径让上层 LLM 看图。真实运行时 Claude 用 Read tool
    看图后输出 issue JSON。返回空 list 表示通过。"""
    print(f"  [vision_check] {image_path} (intent: {intent})")
    print(f"  请 Read 此图,如有问题返回 issue list；空 list = 通过")
    return []  # 骨架：默认接受


def fix_slide(slide, issues):
    """根据 issues 修 slide。骨架占位：不修。"""
    print(f"  [fix_slide] 应用 {len(issues)} 个修复")
    return slide


# ----- 6. main loop -----

def run(brief_path):
    brief = parse_brief(brief_path)
    theme = load_theme(brief["theme"])
    outline = generate_outline(brief, theme)

    prs = Presentation()
    prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

    review_needed = []

    for idx, spec in enumerate(outline, 1):
        print(f"slide {idx}/{len(outline)}: {spec['layout']}")
        slide = generate_slide(prs, spec, theme)
        png_path = f"/tmp/killppts_render/page_{idx:02d}.png"
        try:
            render_one_slide(prs, idx, png_path)
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  渲染失败: {e}; 标 review-needed")
            review_needed.append({"idx": idx, "reason": "render_failed"})
            continue

        attempts = 0
        issues = vision_check(png_path, intent=spec["layout"])
        while issues and attempts < 3:
            slide = fix_slide(slide, issues)
            render_one_slide(prs, idx, png_path)
            issues = vision_check(png_path, intent=spec["layout"])
            attempts += 1
        if issues:
            review_needed.append({"idx": idx, "reason": "vision_unresolved",
                                  "issues": issues})

    out = Path(brief["output"]).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    print(f"\n✅ 已生成 {out}")
    if review_needed:
        print(f"⚠️  {len(review_needed)} 页需 review:")
        for r in review_needed:
            print(f"  - page {r['idx']}: {r['reason']}")
    return out, review_needed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python3 workflow.py path/to/brief.yaml")
    run(sys.argv[1])
```

- [ ] **Step 2: 验证 workflow.py 能解析 demo_brief.yaml**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
python3 -c "
import sys
sys.path.insert(0, 'skills/pptx-deck')
from workflow import parse_brief
b = parse_brief('skills/pptx-deck/examples/demo_brief.yaml')
print('outline:', b['outline'])
print('theme:', b['theme'])
print('output:', b['output'])
"
```

期望：打印 outline list + theme=tech_blue + output 路径。

- [ ] **Step 3: 写 `workflow.md`**

骨架（按 spec §3.3 workflow.md 节铺开,~400 行）：

```markdown
# pptx-deck 主流程

## 6 步流程

### Step 1：parse_brief
- 路 A 自由对话：LLM 与用户对话补齐字段（必填 title/outline/theme/output）
- 路 B brief.yaml：直接读
- 字段补齐 prompt 模板：[完整提示词,见 content-writing.md]

### Step 2：load_theme
- 内置 tech_blue → themes/tech_blue.py
- 用户给 .pptx → template-ingest.md 流程
- 兜底：模板太复杂 → 降级为自定义 layout

### Step 3：generate_outline
- 页数估算: outline 节点数 × 1.5 + 4（封面/目录/总结/封底）
- 每节内容拓写：用 content-writing.md 模板 → page_spec list
- 布局预选：要点数 → 11 种 layout 映射表[完整表]
- 图表插入：每 4-5 页至少一张

### Step 4：per-slide generate + vision QA 循环
[伪代码引用 workflow.py:run]

每页：
1. generate_slide(theme.make_<layout>, **spec)
2. render_one_slide → PNG
3. vision_check → issue JSON（参见 visual-qa.md）
4. while issues and attempts < 3: fix_slide → render → vision_check
5. 仍失败 → 标 review-needed,不停 pipeline

### Step 5：deck_review
- 跨页字体一致性扫描
- 页脚 / 页码完整性
- 章节扉页与内容页 layout 配对正确性

### Step 6：交付
- prs.save(output)
- 打印 review-needed 清单（如有）
- 给用户最后人工核审建议

## 可跑骨架：workflow.py

完整代码引用 [workflow.py](workflow.py)。运行：

\`\`\`bash
cd skills/pptx-deck
python3 workflow.py examples/demo_brief.yaml
\`\`\`

## 用法（在 Claude 会话内）

Claude 调用本 workflow 时,vision_check 由 Claude 自己用 Read 看 PNG 实现：
1. 调 workflow.py 跑到生成 + render
2. 用 Read 看 /tmp/killppts_render/page_NN.png
3. 比照 visual-qa.md 的检查清单输出 issue JSON
4. 修 page_spec / theme 函数后重跑该页

[完整 prompt 流程]
```

acceptance: `wc -l skills/pptx-deck/workflow.md` 在 [280, 520]；grep `parse_brief` `vision_check` `render_one_slide` 都命中。

- [ ] **Step 4: commit**

```bash
git add skills/pptx-deck/workflow.py skills/pptx-deck/workflow.md
git commit -m "feat(pptx-deck): add workflow.py runnable + workflow.md doc"
```

---

## Task 11：content-writing.md + visual-qa.md + template-ingest.md

**Files:**
- Create: `skills/pptx-deck/content-writing.md`（~250 行）
- Create: `skills/pptx-deck/visual-qa.md`（~200 行）
- Create: `skills/pptx-deck/template-ingest.md`（~200 行）

- [ ] **Step 1: 写 `content-writing.md`**

骨架（spec §3.3 content-writing.md 节铺开）：

```markdown
# 每页文案拓写规范

## 11 种 layout 文案规则

| layout | 字数 / 句式约束 | 反例 |
|---|---|---|
| cover | 主标题 ≤ 20 字、副标 ≤ 30 字、不堆头衔 | "关于 XX 公司 2026 年战略发展规划暨数字化转型实施路径研讨" |
| toc | 章节 ≤ 5、每章 ≤ 12 字、动宾对齐 | "公司发展的历史背景与现状分析" |
| section_divider | 章节号 + 标题（≤ 10 字）,layout 独立于内容页 | 与内容页同 header |
| single_focus | 1 句话 ≤ 12 字 + 1 数字（72pt+）+ 1 行解释 | 5 个要点平铺 |
| two_col_compare | 左右标题各 ≤ 6 字、句式对称 | 标题长度差 2× |
| three_col_cards | 每卡标题 ≤ 6 字、body ≤ 30 字 | body 一长一短 |
| bullet_list | 每点 ≤ 14 字、句式一致（动宾或名词性结构） | 一点一句话一点一段 |
| table | 列 ≤ 5、行 ≤ 7、单元格 ≤ 8 字 | 把段落塞进单元格 |
| pic_text | 左图右文,4 卡片每卡 ≤ 20 字 | 图占满 + 文字塞角落 |
| summary | 3-5 条结论,每条 ≤ 18 字,有数字佐证 | 重复 outline 章节 |
| closing | 极简："谢谢"+ 联系方式或下一步 | 又一页要点总结 |

## 拓写指令模板

给 LLM 用的 prompt:

\`\`\`
你正在生成 PPT 第 {idx}/{total} 页。
本章节是：{section_title}
关键信息（从 brief.key_points）：{key_points}
本页 layout：{layout_type}
本页意图：{intent}

请输出 page_spec JSON：
{
  "layout": "{layout_type}",
  "title": "...",
  ...该 layout 所需的所有字段
}

遵循约束（见 content-writing.md 第 X 节）：
- 字数限制
- 句式一致
- 数字 > 文字（能用数字就别用形容词）
- 不使用 emoji,除 ⚠ ⛔ 🔒 警示性
\`\`\`

## 跨页内容设计

[节奏感：cover → toc → section divider 1 → 1-3 内容页 → section 2 → ... → summary → closing]
[变化感：相邻页 layout 不重复]
[强调感：关键论点单独 single_focus 一页]

## 一致性 checklist
- [ ] 标题大小写、标点风格一致
- [ ] 数字单位统一（"%" vs "百分点"）
- [ ] 缩写首次出现给全称
- [ ] 不用通用形容词（"高效"、"创新"、"优秀"）
```

acceptance: `wc -l` 在 [175, 325]；11 种 layout 表行数 = 11；grep "字数 / 句式约束" "拓写指令模板" 命中。

- [ ] **Step 2: 写 `visual-qa.md`**

骨架：

```markdown
# 逐页视觉自检 prompt 与流程

## 单页 vision 自检 prompt 模板

\`\`\`
你审视的是 PPT 第 {idx}/{total} 页,期望意图：{intent}。
渲染图：{image_path}

请找出以下问题（assume 有问题,不要试图确认）：
1. 元素重叠（文字穿过形状、卡片相互覆盖、线条压住文字）
2. 文字溢出框 / 被边缘截断 / 标题换行成两行但装饰按一行布局
3. 中文字体 fallback 到丑字体（Arial 字形显示汉字 / cursive 花体）
4. 标题与内容区距离失衡（> 0.8" 或 < 0.3"）
5. 颜色对比度不足（深底深字 / 浅底浅字）
6. layout 与意图不符（要点 5 个却用了二栏对比）
7. 数字 / 图表位置偏右 / 偏下（textbox margin 未归零）
8. 装饰线、配色或字体与全 deck 不一致
9. 留白边界不达标（< 0.5" 离页边）
10. 表格 banding 横纹意外出现

输出 JSON：
[
  {"issue": "描述", "severity": "low|med|high", "suggested_fix": "改 X 函数 / 调 Y 参数"}
]

若全无问题,输出 []。
\`\`\`

## 单页渲染脚本

[引用 workflow.py:render_one_slide]

## fix → 重渲染 → 再 check 循环

[流程图描述]

## 降级策略

单页修 ≥ 3 次仍有 high severity issue → 接受当前版本 + 在 review_needed list 加该页 + 继续下一页。
不允许死循环（≥ 3 次 fix 还没好,大概率是 layout 选错,不是文字调整能修的）。

## 全 deck 复核（deck_review）

- 字体一致性：随机抽 5 页 run,grep `<a:ea>` typeface,期望全是 Microsoft YaHei
- 页码 / 页脚完整性：每页除 cover / section_divider / closing 外应有页脚
- 章节扉页配对：每个 section_divider 后应有 ≥ 1 内容页

## 视觉 QA checklist（12 项）

- [ ] 无重叠
- [ ] 无截断
- [ ] 字体统一
- [ ] 配色一致
- [ ] 字号层级清晰
- [ ] 留白达标
- [ ] 对齐网格
- [ ] 表格无意外 banding
- [ ] 卡片圆角小（≤ 0.05 调整值）
- [ ] 装饰大字号不换行（word_wrap=False）
- [ ] textbox margin 归零
- [ ] 引用图分辨率清晰（≥ 1600px 宽）
```

acceptance: `wc -l` 在 [140, 260]；grep `vision_check` `[]` `severity` 都命中；checklist 12 项全列。

- [ ] **Step 3: 写 `template-ingest.md`**

骨架：

```markdown
# 从用户 .pptx 模板"学风格"

## 流程 6 步

### Step 1：拷贝到 /tmp/ 防污染
cp user_template.pptx /tmp/template-ingest/

### Step 2：缩略图整体看一眼
python [[pptx]]/scripts/thumbnail.py /tmp/template-ingest/user_template.pptx --cols 4

LLM Read 缩略图,识别整体风格（深色 / 浅色 / 极简 / 装饰繁复）。

### Step 3：unpack XML
python [[pptx]]/scripts/office/unpack.py /tmp/template-ingest/user_template.pptx /tmp/template-ingest/unpacked/

### Step 4：提 design token
- 主色 = theme1.xml 的 <a:accent1> 或封面 shape fill
- 字体 = master 的 <a:latin> + <a:ea> typeface
- layout 命名 = slideLayout*.xml 的 <p:cSld name>

dump 脚本骨架：
\`\`\`python
[完整 dump 脚本：读 theme1.xml + slideMaster1.xml,输出 token JSON]
\`\`\`

### Step 5：dump slide → layout 映射
[骨架代码,参考 [[pptx]]/editing.md Step 1]

### Step 6：生成 /tmp/ingested_theme.py
基于 tech_blue.py 结构,把 BRAND_* / FONT_* 替换为提取出的 token,layout 函数沿用相同签名。

\`\`\`python
[ingested_theme.py 模板：与 tech_blue.py 相同结构,占位 token]
\`\`\`

## 降级方案

模板太复杂（>10 layout 都用过）→ 不再尝试映射所有 layout,改为：
- 复用 master + theme（保留视觉资产）
- 11 个 layout 函数自定义实现（同 tech_blue 结构）
- 输出仍保持 .pptx 原 master,但 slide 全由代码生成

## 何时不走 template-ingest

- 用户 .pptx 风格诡异（含艺术字、动画、3D）→ 警告并退回 tech_blue
- 用户只想看现有 .pptx 内容 → 直接用 [[pptx]]/reading.md
```

acceptance: `wc -l` 在 [140, 260]；grep `template-ingest` `theme1.xml` `slideLayout` 都命中；流程 6 步标题在文档内。

- [ ] **Step 4: commit**

```bash
git add skills/pptx-deck/content-writing.md skills/pptx-deck/visual-qa.md skills/pptx-deck/template-ingest.md
git commit -m "docs(pptx-deck): write content-writing/visual-qa/template-ingest"
```

---

## Task 12：`pptx-deck/SKILL.md`

**Files:**
- Create: `skills/pptx-deck/SKILL.md`

- [ ] **Step 1: 写 SKILL.md**

```markdown
---
name: pptx-deck
description: 端到端 PPT 生成器。用户给主题/要点/brief.yaml/参考 .pptx 模板,skill 自动产出完整 .pptx：拓写每页文案、生成架构图、套用风格、逐页视觉自检与优化。内置科技蓝主题,支持从用户 .pptx 学风格。触发：做一份 PPT / 帮我写 PPT / 路演 deck / 汇报 / 提案 / brief.yaml / .pptx 模板。
---

# pptx-deck — 端到端 PPT 生成器

## 何时用本 skill

| 场景 | 用 |
|---|:--:|
| 用户给主题 + 要点,要完整 deck | ✅ |
| 用户给 brief.yaml | ✅ |
| 用户给参考 .pptx 模板让仿照风格 | ✅ |
| 只读已有 .pptx → 用 [[pptx]] reading.md |
| 只生成单张架构图 → 用 [[diagram]] |
| 模板局部改文字 → 用 [[pptx]] editing.md |

## 输入接口（双路）

### 路 A：自由对话
LLM 与用户对话补齐字段。必填：title / outline / theme / output。
缺哪问哪,问完即开始生成。

### 路 B：brief.yaml
用户直接给 yaml。schema 见 [brief.example.yaml](brief.example.yaml),demo 见 [examples/demo_brief.yaml](examples/demo_brief.yaml)。

## 主流程 6 步

详见 [workflow.md](workflow.md)。可跑脚本见 [workflow.py](workflow.py)。

\`\`\`bash
python3 workflow.py examples/demo_brief.yaml
\`\`\`

## 依赖检查

bash [[pptx]]/scripts/check_deps.sh
+ 确认 [[diagram]] 工具链（drawio / mmdc）按 [[diagram]] SKILL.md 装好

## 共识 token

- 字体：Microsoft YaHei（与 [[pptx]] / [[diagram]] 同源）
- 色板：[tech_blue 默认] / 其他色板见 [[pptx]]/design-system.md
- 字号体系：[[pptx]]/design-system.md

## 子文档

| 文档 | 用途 |
|---|---|
| [workflow.md](workflow.md) | 主流程 6 步 + workflow.py 引用 |
| [content-writing.md](content-writing.md) | 11 layout 文案规则 + 拓写 prompt |
| [visual-qa.md](visual-qa.md) | 单页 vision 自检 prompt + 12 项 checklist |
| [template-ingest.md](template-ingest.md) | 用户 .pptx 学风格 6 步流程 |

## 内置主题

[themes/tech_blue.py](themes/tech_blue.py) — 11 layout 函数 + 科技蓝色板 + Microsoft YaHei。

切换其他色板：改 themes/tech_blue.py 顶部 PRIMARY_* 常量,或从 [[pptx]]/design-system.md 的 10 色板挑一套覆盖。

## 交付前 checklist

- [ ] brief 必填字段全到位
- [ ] theme 加载成功（tech_blue / 用户 .pptx）
- [ ] outline → page_spec 全部生成
- [ ] 逐页 vision QA 通过（或加入 review_needed）
- [ ] deck_review 通过：字体一致 + 页脚完整 + 章节配对
- [ ] 最终 .pptx 用 PowerPoint 打开验证（可选,Windows 端）
- [ ] review_needed 清单给用户人工核审
```

acceptance: frontmatter 完整;4 子文档 + workflow.py + brief.example.yaml + themes/tech_blue.py 都有链接;`[[pptx]]` `[[diagram]]` 互引出现。

- [ ] **Step 2: commit**

```bash
git add skills/pptx-deck/SKILL.md
git commit -m "docs(pptx-deck): write SKILL.md entry"
```

---

## Task 13：端到端 smoke test（跑 demo_brief.yaml 产 sample_output.pptx）

**Files:**
- Generate: `skills/pptx-deck/examples/sample_output.pptx`

- [ ] **Step 1: 跑 workflow**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck
python3 workflow.py examples/demo_brief.yaml
```

期望输出（骨架版 vision_check 默认接受）：

```
slide 1/12: cover
  [vision_check] /tmp/killppts_render/page_01.png (intent: cover)
  ...
✅ 已生成 .../examples/sample_output.pptx
```

- [ ] **Step 2: 视觉抽检 sample_output.pptx**

```bash
soffice --headless --convert-to pdf /Users/pc2026/Documents/DevTools/KillPPTs/skills/pptx-deck/examples/sample_output.pptx --outdir /tmp/
pdftoppm -jpeg -r 100 /tmp/sample_output.pdf /tmp/so
ls /tmp/so-*.jpg
```

期望：~12 张 jpg。逐张 Read 抽 4 张关键页：
- so-01.jpg 封面：深蓝 + "KillPPTs 自动化 PPT 生成"
- so-02.jpg 目录：4 个章节
- so-04.jpg 章节扉页 1：大色块 1 + "动机"
- so-12.jpg 封底：深蓝 + "谢谢"

如有任一致命问题（字体 fallback / 重叠 / 截断）,定位到 themes/tech_blue.py 修复并回 Task 8 重跑测试。

- [ ] **Step 3: commit sample_output.pptx**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
git add -f skills/pptx-deck/examples/sample_output.pptx
git commit -m "test(pptx-deck): add end-to-end sample_output.pptx"
```

注意 `-f`：`.gitignore` 默认排除 `.pptx`,但 `!skills/pptx-deck/examples/sample_output.pptx` 已加白名单（任务 1 step 1）；若未加,本步用 `-f`。

---

## Task 14：跨 skill 互引核对

- [ ] **Step 1: 扫描所有 `[[name]]` 引用**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
grep -rn "\[\[" skills/ | sort
```

期望发现的引用（核对每条目标存在）：
- `[[pptx]]` 出现在 pptx-deck/* 与 diagram/*
- `[[diagram]]` 出现在 pptx-deck/*
- `[[pptx-deck]]` 出现在 pptx/SKILL.md（"被 pptx-deck 调用"上下文）与 diagram/SKILL.md

每个 `[[name]]` 对应的 skill 名要在 `skills/<name>/SKILL.md` 的 frontmatter 出现：

```bash
for name in pptx pptx-deck diagram; do
    head -3 skills/$name/SKILL.md | grep "name: $name" || echo "❌ missing name: $name in $name/SKILL.md"
done
```

期望：三行都命中,无 ❌。

- [ ] **Step 2: 扫描相对路径引用**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
grep -rn "\](.*\.md)" skills/ | grep -v "http"
```

每个本地链接（如 `[creating.md](creating.md)`）都要对应实际文件。手动核对 ≥ 90% 命中。

- [ ] **Step 3: 字体一致性扫描**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
# 默认字体应是 Microsoft YaHei
grep -rn "PingFang SC" skills/ | grep -v "fallback\|FALLBACK"
```

期望：除 fallback 链上下文外,无 `PingFang SC` 出现（用户决策）。如有,改为 Microsoft YaHei 或加 fallback 注释。

- [ ] **Step 4: commit 修正（如有）**

```bash
git add skills/
git diff --cached --stat
git commit -m "docs: cross-skill ref consistency pass"
```

如无修改本步跳过。

---

## Task 15：写正式 README.md

**Files:**
- Modify: `/Users/pc2026/Documents/DevTools/KillPPTs/README.md`

- [ ] **Step 1: 覆盖写正式 README**

```markdown
# KillPPTs

端到端 PPT 生成 skill 库。复制人类快速生成 PPT 的能力——给主题/要点,自动产出完整 .pptx,含视觉自检。

## 三个 Skill

| Skill | 一句话职责 |
|---|---|
| [`skills/pptx-deck/`](skills/pptx-deck/) | 端到端生成器：brief → 完整 .pptx,含逐页视觉自检 |
| [`skills/pptx/`](skills/pptx/) | .pptx 底层读写：从零创建 / 模板编辑 / 提取内容 |
| [`skills/diagram/`](skills/diagram/) | 架构图 / 流程图 / 可视化（draw.io / mermaid / matplotlib / pptx-native） |

## 快速开始

### 1. 装依赖

\`\`\`bash
bash skills/pptx/scripts/check_deps.sh
\`\`\`

### 2. 跑 demo

\`\`\`bash
cd skills/pptx-deck
python3 workflow.py examples/demo_brief.yaml
\`\`\`

产物：`skills/pptx-deck/examples/sample_output.pptx`。

### 3. 自定义 brief

复制 `skills/pptx-deck/brief.example.yaml` 改字段,跑：

\`\`\`bash
python3 workflow.py my_brief.yaml
\`\`\`

## 在 Claude Code 中使用

把本仓库的 `skills/` 拷贝到你的项目 `.claude/skills/` 下,或符号链接：

\`\`\`bash
ln -s /path/to/KillPPTs/skills/* /path/to/your-project/.claude/skills/
\`\`\`

Claude 会自动触发对应 skill。触发关键词见各 `SKILL.md` 的 frontmatter。

## 设计文档

完整设计见 [docs/superpowers/specs/2026-05-21-killppts-skill-design.md](docs/superpowers/specs/2026-05-21-killppts-skill-design.md)。

## 默认风格说明

- 主题：`tech_blue`（深海蓝 + 科技蓝 + 青绿点睛）
- 字体：Microsoft YaHei（macOS 渲染前请装雅黑,否则 LibreOffice fallback）
- 其他色板：见 [skills/pptx/design-system.md](skills/pptx/design-system.md) 10 色板

## 鸣谢

迁移自 [AppGenesisForge](../DevAgents/AppGenesisForge) 的 pptx skill 沉淀,经过去业务化重构。
```

- [ ] **Step 2: commit**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
git add README.md
git commit -m "docs: write KillPPTs README"
```

- [ ] **Step 3: 全仓状态检查**

```bash
cd /Users/pc2026/Documents/DevTools/KillPPTs
git log --oneline
git status
find skills -type f | sort
```

期望：
- 15+ commit
- working tree clean
- 文件清单完整（对照本计划顶部的 File Structure）

---

## 完成标准

- [ ] 全部 15 任务的 commit 在主分支
- [ ] `bash skills/pptx/scripts/check_deps.sh` 全 ✅
- [ ] `python3 -m pytest tests/` 全 PASS
- [ ] `python3 skills/pptx/examples/minimal_deck.py` 跑通,3 页视觉抽检无异常
- [ ] `bash skills/diagram/examples/render.sh` 跑通,minimal.png 视觉清晰
- [ ] `python3 skills/pptx-deck/workflow.py skills/pptx-deck/examples/demo_brief.yaml` 跑通,12 页 sample_output.pptx 视觉抽检无异常
- [ ] 互引扫描通过（Task 14）
- [ ] README 中"快速开始"3 步在干净环境照做能跑通
