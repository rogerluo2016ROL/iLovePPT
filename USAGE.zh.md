# iLovePPT 使用说明

> 端到端 PPT 生成工具:给主题/要点 → 自动产出完整 .pptx,含视觉自检。

---

## 一、这是什么

iLovePPT 是一个 Claude Code skill 库,目标是**复制人类快速生成 PPT 的能力**。你输入主题与要点,工具自动:

- 拓写每页文案(标题/要点/对比/数据)
- 选择合适的版式(11 种 layout)
- 嵌入架构图、流程图、可视化
- 套用统一风格(默认科技蓝主题)
- 逐页渲染 + LLM 视觉自检 + 自动优化

最终产物是一份可以直接打开的 `.pptx` 文件。

---

## 二、快速开始(3 步)

### 1. 装依赖

```bash
git clone git@github.com:pcliangx/iLovePPT.git
cd iLovePPT
bash skills/pptx/scripts/check_deps.sh
```

脚本会输出 ✅/❌/⚠️ 清单。缺啥按提示装:

```bash
pip3 install python-pptx lxml 'markitdown[pptx]' Pillow pyyaml
brew install --cask libreoffice
brew install poppler
# 可选(画架构图)
brew install --cask drawio
brew install mermaid-cli
pip3 install matplotlib
```

**⚠️ macOS 用户注意**:LibreOffice 默认没装微软雅黑,渲染中文会 fallback 到 PingFang SC。如要与 Windows PowerPoint 显示一致,把微软雅黑字体文件放入 `~/Library/Fonts/`。

### 2. 跑示例

```bash
cd skills/pptx-deck
python3 workflow.py examples/demo_brief.yaml
```

产物:`examples/sample_output.pptx`(12 页参考成品,深海蓝 + 科技蓝主题)。

### 3. 自定义你的 PPT

复制 `brief.example.yaml` 改字段:

```yaml
title: "你的 PPT 标题"
subtitle: "副标题"
outline:
  - "章节 1"
  - "章节 2"
  - "..."
key_points:
  - "关键论点 1"
  - "关键论点 2"
theme: tech_blue
output: ./my_deck.pptx
```

然后跑:

```bash
python3 skills/pptx-deck/workflow.py my_brief.yaml
```

---

## 三、三个 skill 的关系

| Skill | 干嘛的 | 何时单独用 |
|---|---|---|
| `pptx-deck` | 端到端生成(主入口) | 给主题让它写整份 PPT |
| `pptx` | 底层 .pptx 读写 | 只想读已有 PPT,或局部改文字 |
| `diagram` | 架构图/流程图/数据可视化 | 只想出一张图 |

`pptx-deck` 内部会调用 `pptx` 与 `diagram`,你通常只跟 `pptx-deck` 打交道。

---

## 四、在 Claude Code 里用

把 skills/ 链接到目标项目:

```bash
ln -s /path/to/iLovePPT/skills/pptx       /path/to/your-project/.claude/skills/pptx
ln -s /path/to/iLovePPT/skills/pptx-deck  /path/to/your-project/.claude/skills/pptx-deck
ln -s /path/to/iLovePPT/skills/diagram    /path/to/your-project/.claude/skills/diagram
```

之后跟 Claude 说"帮我做一份 XX 的 PPT","我要做路演 deck"等,Claude 会自动触发对应 skill。

---

## 五、内置主题与自定义

### 内置:科技蓝
- 主色 `#1E6FE0` + 深海蓝 `#0B2A4A` + 浅蓝底 `#E6F0FC` + 青绿点睛 `#00D1C1`
- 字体:微软雅黑(中文)+ Helvetica Neue(英文/数字)

### 其他 10 套预设色板
见 `skills/pptx/design-system.md`:商务深蓝 / 党政红 / 极简白 / 咨询黑 / 莫兰迪灰 / 薄荷绿 / 暖橙 / 灰盐 / 酒红。

切换方法:改 `skills/pptx/helpers.py` 顶部的 `BRAND_*` 常量。

### 用你自己的 .pptx 模板学风格

在 brief.yaml 里把 theme 改为 .pptx 路径:

```yaml
theme: /path/to/your_template.pptx
```

工具会自动提取模板的主色与字体,生成临时主题模块跑生成。

---

## 六、11 种版式

| 版式 | 适用场景 |
|---|---|
| `cover` | 封面 |
| `toc` | 目录页 |
| `section_divider` | 章节扉页 |
| `single_focus` | 单点强调(大数字+大字) |
| `two_col_compare` | 二栏对比 |
| `three_col_cards` | 三栏卡片 |
| `bullet_list` | 5 点列表 |
| `table` | 数据表格 |
| `pic_text` | 左图右文(图+4 卡) |
| `summary` | 总结页 |
| `closing` | 封底 |

详细文案规范见 `skills/pptx-deck/content-writing.md`。

---

## 七、视觉自检流程

每生成一页,工具会:
1. 渲染该页为 PNG(`soffice` + `pdftoppm`)
2. LLM Read 该 PNG,按 12 项 checklist 找问题
3. 若有问题,自动修(字号过大 → 缩 20% / margin 未归零 → 重置)
4. 修 ≤ 3 次仍失败 → 标记 `review_needed`,人工最后审

12 项 checklist 与 prompt 模板见 `skills/pptx-deck/visual-qa.md`。

---

## 八、测试与验证

```bash
python3 -m pytest tests/ -v     # 35 个单元/集成测试
python3 skills/pptx/examples/minimal_deck.py     # pptx skill smoke test
bash skills/diagram/examples/render.sh           # diagram smoke test
```

---

## 九、目录结构

```
iLovePPT/
├── README.md
├── pyproject.toml
├── USAGE.zh.md                       # 本文件
├── docs/superpowers/{specs,plans}/   # 设计文档 & 实施计划
└── skills/
    ├── pptx-deck/                    # 端到端生成(主)
    ├── pptx/                         # 底层读写
    └── diagram/                      # 架构图/可视化
```

---

## 十、常见问题

**Q: 生成的 PPT 字体不对/中文是花体?**
A: macOS 没装微软雅黑,LibreOffice 渲染时 fallback。装雅黑,或接受 fallback(Windows PowerPoint 打开会正常)。

**Q: soffice / pdftoppm 命令找不到?**
A: 跑 `bash skills/pptx/scripts/check_deps.sh`,按提示装。

**Q: 生成的 PPT 卡片重叠/文字溢出?**
A: 视觉自检循环会自动修。若 3 次仍不行,看终端的 `review_needed` 清单,手动调 brief.yaml 的 key_points 或 outline。

**Q: 想加自己的主题?**
A: 复制 `skills/pptx-deck/themes/tech_blue.py` 为 `your_theme.py`,改 PRIMARY/PRIMARY_DEEP 等常量,在 `workflow.py:THEMES` 字典里注册。

**Q: 想读已有 PPT 提取内容?**
A: `python3 -m markitdown your_deck.pptx` 一行搞定。

---

## 十一、设计文档

- 完整设计:`docs/superpowers/specs/2026-05-21-killppts-skill-design.md`
- 实施计划:`docs/superpowers/plans/2026-05-21-killppts-skill.md`

---

GitHub: `https://github.com/pcliangx/iLovePPT`
