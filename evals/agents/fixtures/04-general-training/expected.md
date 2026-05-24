# Fixture 04 · Expected

## brief.md 应有

```yaml
audience: general
duration_min: 45
presentation_mode: speaker
structure_mode: tutorial    # 启 bypass_pyramid: true
top_recommendation: RAG 是给 LLM 加"开卷考试"能力 ...
```

## outline.md 应有

- **bypass_pyramid: true** 在 frontmatter 标
- 章节按知识点结构序(✓ "RAG 是什么 → RAG 怎么工作 → 实际例子 → 何时用 / 不用 RAG → Q&A")
- 不强求 MECE 严格(培训 deck 允许递进结构)
- action title 可以是话题标签(培训场景 ✗ 推荐结论句不适用,✓ 知识点名)

## content.md 应有

- 总页数 45 × 1.5 = **67 页 ± 5**(长 deck)
- **类比丰富**(✓ "RAG 像考试时翻参考书,不是凭记忆")
- 行话首次出现给全称(✓ "LLM(Large Language Model 大语言模型)")
- 至少 1 张 RAG 流程图(draw.io 现画)
- 节奏感:每节 ≤ 3 内容页(防 general 受众疲劳)

## critic 应有

- 注意:bypass_pyramid 模式下 Section A 部分项可豁免
- 维度 1 论据强度:培训稿不强求"sharp 论据"(知识点清晰即可)
- 维度 3 措辞质感:重"行话翻译"是否到位

## audience 应有

- **按 general profile**:`comprehension_5s` 阈值严(行话过多就扣分)
- `info_density` 重(每页 5+ bullet 即过载)
- **overall_score ≥ 8.0**

## 评分锚点

| 维 | 期望 |
|---|---|
| 1 | ≥ 8(brainstorm 识别培训场景 + bypass_pyramid)|
| 2 | ≥ 7(培训 outline 结构跟金字塔不同,标准放宽) |
| 3 | ≥ 8(长 deck 字数严守 + 行话翻译) |
| 4 | ≥ 7 |
| 5 | ≥ 8.0 |
| **总分** | ≥ **38** |
