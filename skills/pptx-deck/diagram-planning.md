# 图层规划（diagram planning）

> workflow 第 3 步。读完 brief、加载主题之后、拓写 outline 之前执行。
> 目标：**主动判断哪些章节该配图**，而不是等内容写完才发现"全是文字墙"。

## 核心原则：一图胜千文

**能用图形表达的观点，就不要用文字堆。** 凡涉及结构、流程、关系、数据对比的
内容，都应主动调用 AI 绘图能力（[[diagram]] skill）生成图——一张清晰的图，
胜过三行 bullet。

判断犹豫时**倾向于画图**：文字墙是 deck 最大的失败模式。本步骤的存在就是为了
强制兑现这条原则——读完 brief 立刻想"哪里能上图"，而不是事后补救。

## 为什么要单独一步

如果不主动规划，deck 很容易变成纯文字 bullet 堆叠——读者看不懂系统结构、记不住流程。
图层规划强制在拓写文案**之前**就回答："这一章，用一张图能不能讲得更清楚？"

一个好的 deck，每 4-5 页至少有 1 张图（架构 / 流程 / 数据 / 关系）。

## 输入与输出

**输入**：`parse_brief()` 产出的标准化 brief（`outline` 章节列表 + `key_points`）。

**输出**：`diagram_plan` —— 一个 list，每项标记一个建议配图的章节：

```json
[
  {
    "section_idx": 2,
    "section": "技术架构",
    "diagram_type": "arch_diagram",
    "tool": "draw.io",
    "intent": "展示三层架构与模块依赖"
  }
]
```

## 决策规则：4 类图的触发判断

逐个扫描 `outline` 章节（结合 `key_points` 语义），判断是否命中以下信号。
每个章节最多配 1 张图。

| 内容信号（章节标题 / 要点里出现） | 图类型 `diagram_type` | 推荐工具 `tool` | 落到 [[diagram]] 的子文档 |
|---|---|---|---|
| 系统由…组成、分 N 层、模块 / 组件 / 微服务 / 技术栈 / 拓扑 | `arch_diagram` | draw.io | `drawio.md` |
| 步骤 / 阶段 / 流程 / 先后 / 时序 / 环节 / pipeline | `flow` | Mermaid | `mermaid.md` |
| 趋势 / 增长 / 占比 / 对比 / 指标 / 百分比 / 数据 | `chart` | matplotlib | `matplotlib.md` |
| 角色关系 / 依赖 / 交互 / 连接 / 映射（≤ 5 节点） | `simple_relation` | pptx-native | `pptx-native.md` |

工具选型的完整决策表（含切换阈值）见 [[diagram]] `SKILL.md`。本表是粗筛。

### 判断时的注意点

- **章节标题是主要线索，`key_points` 是补充**：标题"落地路径"含"路径"偏流程，但若要点全是数字，则应选 `chart`。
- **一个章节只配最相关的一张图**：既有架构又有流程时，挑承载信息量最大的。
- **不是每章都要图**：纯观点 / 背景陈述类章节（如"背景与意义"）通常不配图。
- **节点数决定架构图 vs 关系图**：> 5 节点或有嵌套层次走 `arch_diagram`（draw.io）；≤ 5 节点的简单关系走 `simple_relation`（slide 内直接画，可编辑）。

## 骨架实现 vs Claude 判断

`workflow.py:plan_diagrams()` 是**关键词匹配骨架**——用 `_DIAGRAM_SIGNALS` 正则扫章节标题，命中即标记。它的作用是让 `workflow.py` 能独立跑通，并给出粗筛提示。

**真实运行时，Claude 覆盖骨架输出**：Claude 读 brief 后按本文档的决策规则做**语义判断**——理解每章真正讲什么，而不只是匹配字面词。骨架命中 ≠ 最终决定；骨架漏掉的语义（如"评审机制"其实是流程）由 Claude 补上。

## 与 generate_outline / pic_text 的衔接

`diagram_plan` 传入 `generate_outline(brief, diagram_plan)`。命中的章节，其内容页 `page_spec` 会带上 `visual_element` 元数据：

```python
{
  "layout": "bullet_list",          # 骨架仍用 bullet_list（无法自己产 PNG）
  "title": "技术架构",
  "items": [...],
  "visual_element": {               # ← 图层规划标记
    "type": "arch_diagram",
    "tool": "draw.io",
    "intent": "展示三层架构与模块依赖"
  }
}
```

真实运行时，Claude 看到 `visual_element` 后：

1. 调 [[diagram]] skill，按 `tool` 生成图 → 得到 PNG 路径
2. 把该页 `layout` 从 `bullet_list` 换成 `pic_text`
3. 补上 `image_path`（PNG 路径）与 `points`（右侧 4 个说明卡片，从原 `items` 提炼）
4. `generate_slide` 调 `make_pic_text` 渲染「左图右文」版式

`visual_element` 是规划元数据，不是渲染参数——`generate_slide` 调 `make_*` 前会从 kwargs 剔除它（见 `_NON_RENDER_KEYS`）。

## 密度自检

拓完 outline 后回头看 `diagram_plan`：

- 总页数 ÷ 图数 > 5 → 偏少，重新扫一遍有没有漏判的流程 / 架构章节
- 连续 3 张图 → 偏多，挑信息量最大的保留，其余降级为 bullet
- 全 deck 0 张图 → 几乎一定是漏判，重新审视每章

## Anti-prompt

- 不要等文案写完才想图——图层规划必须在 `generate_outline` 之前
- 不要每章都硬塞图——背景 / 观点类章节不配图
- 不要混用工具——同一 deck 的图尽量同一套工具，避免视觉割裂（见 [[diagram]] 选型表）
- 不要把 `visual_element` 当渲染参数传给 `make_*`——它是规划元数据
- 不要只信骨架的关键词命中——Claude 必须做语义判断覆盖
