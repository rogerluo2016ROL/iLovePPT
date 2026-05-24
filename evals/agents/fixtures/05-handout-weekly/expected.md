# Fixture 05 · Expected

## brief.md 应有

```yaml
audience: executive
duration_min: 10
presentation_mode: handout       # 关键
structure_mode: data_report      # 启 bypass_pyramid
top_recommendation: 本周技术部交付 3 大里程碑 ...
```

## outline.md 应有

- **bypass_pyramid: true** 在 frontmatter 标
- 章节按数据维度(订单 / 性能 / 安全 / OKR)非论证
- footer_meta + classification: INTERNAL

## content.md 应有(关键测试!)

- 总页数 10 × 1.5 = **15 页 ± 2**(短 deck)
- **handout 字数遵守**:
  - cards body **≤ 80 字**(speaker 是 18)
  - bullet items **≤ 40 字**(speaker 是 12)
  - summary **≤ 60 字**(speaker 是 15)
- **每 bullet 是完整可读句子**(handout 不写关键词)
  - ✗ "订单 v2 上线 → 完成"(关键词风,speaker 写法)
  - ✓ "订单系统 v2 已于周三完成全量上线,首日处理 28400 单同比 +8.8%,无 P0 故障"(完整句,handout 写法)
- Source 引文齐全(VP 读时要能 verify)
- 句末加句号(handout 严守)

## critic 应有

- **B7 字数检查关键** —— 必须按 handout 模式查 cards body ≤ 80 / bullet ≤ 40
- **维度 3 措辞质感**:句子是否完整可读(不是关键词)

## audience 应有

- **按 executive + handout profile**:VP 读时希望"每页一眼能 grasp + 数字 verify"
- info_density 应该高(handout 模式信息密度 3-4× speaker)
- `comprehension_5s` 不是"5 秒抓要点"(读手册可以慢慢看),改测"每条 bullet 自洽可读"
- **overall_score ≥ 8.0**

## 评分锚点

| 维 | 期望 |
|---|---|
| 1 | ≥ 8(brainstorm 识别 handout 模式 + structure_mode: data_report) |
| 2 | ≥ 7(bypass_pyramid 模式,outline 是数据维度) |
| 3 | ≥ 8.5(**关键!handout 字数遵守是这个 fixture 的核心测试点**) |
| 4 | ≥ 7(critic 必须按 handout 字数表查) |
| 5 | ≥ 8.0 |
| **总分** | ≥ **38.5** |
