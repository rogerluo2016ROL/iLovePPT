# iLovePPT Eval Baseline Scorecard

> 记录于 v2 layout 修复后（cards/compare/section_divider 居中修复，commit f1eb345）。
> 对比基准——后续改 layout/build 代码后重跑 eval，fail 项变多即回归。

## 01_short （6 页）

- page 2, #13 — TOC 页三条目之间仍有大片空白（条目顶部堆叠，中段留白过宽），内容未均布
- page 4, #13 — bullet_list 三条集中在页面中偏下区域，标题与内容之间大片空白
- page 5, #13 — numbered_list 三个蓝色方块各自内容只有一行文字，方块内部下半段为大片空白

其余页（cover、section_divider page 3、closing）全部通过。
**注：page 3（section_divider）数字方块与标题已垂直居中，旧基准 #13 fail 已修复。**

## 02_long （28 页，抽检 cover/TOC/divider/content×4/closing）

抽检页：page-01、02、03、04、07、14、26、28

- page-04, #13 — bullet_list（3 条）集中在页面中偏下，标题与内容之间大片空白
- page-07, #13 — bullet_list（3 条）同上，大片空白
- page-14, #13 — cards 页（3 卡片）每张卡片内容（标题+一行正文）在卡片顶部，下半段大片空白
- page-26, #13 — cards 页（3 卡片）同上

其余抽检页（cover、TOC、section_divider page-03、closing）全部通过。
**注：page-03（section_divider）数字方块与标题已垂直居中，旧基准 #13 fail 已修复。**

## 03_cards （5 页）

- page 2, #13 — 双卡片内容（标题+一行文字）在卡片顶部，卡片下半部约 60% 为空白
- page 3, #13 — 三卡片同上，每张卡仅一行正文，下半部空白明显
- page 4, #13 — 四卡片同上，每张卡仅一行正文，下半部空白明显

其余页（cover、closing）全部通过。
**注：卡片内容仍顶部对齐（非居中），cards 的 airy 修复在此 deck 尚未完全生效。**

## 04_compare （4 页）

- page 2, #13 — 双对比卡片内容（多行正文）在卡片顶部，卡片下半约 50% 为空白
- page 3, #13 — 三对比卡片同上，内容在卡片顶部，下段大片空白

其余页（cover、closing）全部通过。
**注：旧基准 04_compare 全部通过，此次重新评分发现卡片下方有明显空白，判定为 #13 fail。**

## 05_pictext （3 页）

全部通过。

page-2 pic_text 布局：左侧图片占位块（纯蓝）+ 右侧三张特性卡，布局与意图一致，无溢出/重叠。

## 06_table （4 页）

全部通过。

page-2、3 表格行 banding 为交替浅蓝/白，属于设计内预期样式，非意外 banding（rubric #10 通过）。

## 07_chinese （6 页）

- page 1, #12 — 封面标题"人工智能驱动的新一代企业数字化转型解决方案全景评估报告"字号较大、文字较长，换行形成 2 行（末字组"全景评估报告"换行），大字号文本换行

其余页（TOC、bullet×3、closing）全部通过。中文字体正常渲染（无 Arial/花体 fallback），文字无溢出/截断。

已知限制：07_chinese page 1 标题超长（24 个汉字）属压力测试，换行为预期边缘情况。

## 08_template_extract （3 页）

全部通过。

模板主色提取（4F81BD）正确应用，页面布局与 tech_blue 主题一致，文字/布局无异常。

---

## 汇总

- 总检查页数: 37（01_short 6页 + 02_long 抽检 8页 + 03_cards 5页 + 04_compare 4页 + 05_pictext 3页 + 06_table 4页 + 07_chinese 6页 + 08_template_extract 3页；注：02_long 实际 28 页，仅抽检）
- 总 fail 项: 12
- 已修复（对比旧基准 bb0f87b）:
  1. **#13 section_divider 居中** — 01_short page 3 和 02_long page-03 的数字方块+标题已垂直居中，旧基准 2 处 #13 fail 消除。
- 已知问题清单:
  1. **#13 空白过多（bullet_list 系统性）**：bullet_list 页面标题与内容之间有大片空白，内容未居中/均布。影响 01_short（page 4）、02_long（page-04、07）。
  2. **#13 空白过多（cards/compare 卡片）**：卡片内容（短内容时）顶部对齐，卡片下方大片空白。影响 03_cards（3处）、04_compare（2处）、02_long 抽检（2处）。
  3. **#13 TOC 间距**：01_short page 2 TOC 三条目间距过大（仅 3 条时均匀拉伸，显空旷）。
  4. **#13 numbered_list 方块过高**：01_short page 5 蓝色方块高度过大，短内容仅占方块上部。
  5. **#12 大字号换行（07_chinese page 1）**：封面超长标题（24 汉字）换行，已知压力测试边缘情况。
