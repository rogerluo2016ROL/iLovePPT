# pptx-deck 主流程(v3:主线程对话 + agent build)

端到端:用户一句话 → 主线程多轮对话 → 用户审 markdown → agent build .pptx。
v3 把 "智能" 分到 **主线程 Claude(Stage A-D)** + **agent(Stage E)** 两侧,接缝是 markdown 文档。

详细设计见 [v3 spec](../../docs/superpowers/specs/2026-05-23-iloveppt-v3-markdown-first.md)。

## 5 阶段全景

```
[主线程 Claude]                                         [agent]
─────────────────                                       ─────────
Stage A · 需求挖掘对话(brainstorming)
  ↓ 收齐 audience/duration/核心命题
Stage B · 素材摄入(对话推进时)
  ↓ 数据表 / 图 / 模板 落到 _assets/
Stage C · 内容规划
  ↓ 出 deck_v1_outline.md
  ↓ 用户审 outline · 改 / 批
Stage D · 全文拓写
  ↓ 出 deck_v1_content.md
  ↓ 用户审 content · 改 / 批
                                                        Stage E · 终稿构建
                                                          0. Read content.md + Pyramid 自检 7 项
                                                          1. md → deck_plan.json(严约束)
                                                          2. build.py → .pptx + PNG
                                                          3. 视觉 QA 循环 ≤ 3 轮(自动改 md 重 build)
                                                          4. 返回 pptx + auto_md_edits + review_needed
```

## Stage A:需求挖掘(主线程,brainstorming)

用户扔一句话 → 主线程 Claude 调 brainstorming skill,多轮问:

| 必收齐字段 | prompt 模板 |
|---|---|
| `audience` | "给谁看?老板 / 客户 / 团队 / 投资人 / 大众?" |
| `duration_min` | "多长?10/15/20/30 分钟?" |
| `top_recommendation` | "一句话总结你想让听众接受的核心判断" |
| `theme` | "用默认 tech_blue,还是你公司有模板 .pptx?" |
| `output` | "成品 .pptx 放哪?(默认 ./deck_v1.pptx)" |

未收齐前**不进 Stage B**。

## Stage B:素材摄入

对话中如识别用户提到数据 / 图 / 模板 / 参考文档,**主动 prompt** 让其提供。规则与 prompt 模板见 [content-writing.md 素材摄入小节](content-writing.md#素材摄入主线程-stage-b)。

素材落到 `<工作目录>/_assets/{raw,charts,refs}/`,后续 Stage D 拓写时引用。

## Stage C:内容规划 + outline.md

按金字塔原理 5 件套设计 outline:

- ① 单一顶端论点(`top_recommendation`)
- ② SCQA 开场
- ③ 答案在前(BLUF,顶端论点出现在 cover.subtitle 或第 1 内容页)
- ④ 横向 MECE(3-5 章节)
- ⑤ 纵向疑问/回答链(章节标题串起来讲完整故事)

加 ⑥ 字段完整性 + ⑦ action title ≤ 24 字,共 **Pyramid 自检 7 项**。

产出 `deck_v1_outline.md`(schema 见 [content-writing.md](content-writing.md#deck_vnoutlinemd-schema))。给用户:

```
Outline 在 deck_v1_outline.md。审一下,改完告诉我"批准"或"改 X 处"。
```

## Stage D:全文拓写 + content.md

基于已批准 outline,逐节展开:

- 每节按 layout 选型规则(content-writing.md)
- 数据图先调 matplotlib_rc 生成 PNG 落到 `_assets/charts/`,再在 md 用 `![](_assets/charts/X.png)` 嵌入
- 文案严守 11 layout 字数规则
- 关键 stat 加 `> 数据:Source: ...` 引文

产出 `deck_v1_content.md`(schema 见 [content-writing.md](content-writing.md#deck_vncontentmd-schema-agent-的输入))。给用户:

```
全文在 deck_v1_content.md。逐页审,有问题改 md 文件再告诉我"批准"。
```

## Stage E:agent 派发 + build

content 批准后,主线程派发 agent:

```
@agent-iloveppt
content_md_path: /abs/path/to/deck_v1_content.md
output_pptx: /abs/path/to/deck_v1.pptx
theme: tech_blue
footer_meta: {classification: INTERNAL, project: ..., version: v1.0}
```

agent 5 步详见 [iloveppt agent 文件](../../.claude/agents/iloveppt.md):

0. Read content.md + Pyramid 自检 7 项 → 失败 hard stop
1. md → deck_plan.json(严约束:不引入新论点,反向 diff 校验)
2. python3 build.py → .pptx + 渲染 PNG
3. 视觉 QA 循环 ≤ 3 轮:
   - 找到视觉问题(溢出/字号/字体 fallback 等)
   - 自动改 content.md(仅限格式类,见 agent 文件的允许/禁止表)
   - rerun build.py
4. 返回 yaml:`pptx_path + auto_md_edits + review_needed + pyramid_check`

主线程收到返回后:

- 展示 `auto_md_edits` 给用户(可批量批准或回退某条)
- 展示 `review_needed` 让用户人工处理

## 接缝:为什么是 markdown 而不是 yaml(v2 旧设计)

| 接缝介质 | v2 yaml | v3 markdown |
|---|---|---|
| 用户可读性 | 差(技术语言) | 强(自然文档) |
| 编辑工具 | 必须用文本编辑器谨慎改 | 任何 markdown editor / Obsidian / VS Code |
| 版本对比 | git diff 难读(嵌套字段) | git diff 易读(逐段) |
| 多人协作 | 容易冲突 | markdown merge 相对友好 |
| 用户能直接审什么 | 框架(120 字) | 完整文案(2000-5000 字) |
| 改 1 个字成本 | 整个 deck rebuild | 改 md → rebuild 仍要 3-5 min,但**用户已知道改什么** |

## build.py 的能力边界(不变)

build.py 仍是纯机械:`deck_plan.json → .pptx + PNG`。v3 没改 build.py 接口;只是输入的 `deck_plan.json` 由 agent 从 md 生成(v2 是 agent 从 brief 拓写)。

CLI:`python3 build.py deck_plan.json [--no-render]`

## 11 种 layout(不变)

cover / toc / section_divider / single_focus / compare / cards / bullet_list / table / pic_text / summary / closing。字段约束与 markdown 表达形式见 [content-writing.md](content-writing.md)。

## v2 → v3 主要差异速查

| 维度 | v2 | v3 |
|---|---|---|
| 用户入口 | `@agent-iloveppt 帮我做 X` | "帮我做 X"(直接对话主线程) |
| 谁做 brief 解析 | agent Phase 1 | 主线程 Stage A |
| 谁做大纲设计 | agent Phase 1 | 主线程 Stage C |
| 谁做文案拓写 | agent Phase 2 | 主线程 Stage D |
| 用户审什么 | Phase 1 输出的 YAML outline | outline.md + content.md(2 个 checkpoint) |
| 接缝 | brief → agent → pptx | content.md → agent → pptx |
| 视觉修复 | agent 改 deck_plan.json | agent 改 content.md(用户最终源是 md) |

## Anti-prompt

- 主线程不要跳过 Stage A 对话,直接派 agent —— agent 会 reject
- 主线程不要在 Stage C/D 中生成 yaml schema —— markdown 才是接缝
- agent 不要做 brief 解析 / 大纲设计 —— 那是 Stage A-D 的事
- agent 不要超出 auto_md_edits 边界(只允许格式修正,不允许动观点 / 数据 / 引文)
- 配图必须在 Stage D 写 content.md 之前生成好(主线程负责)
