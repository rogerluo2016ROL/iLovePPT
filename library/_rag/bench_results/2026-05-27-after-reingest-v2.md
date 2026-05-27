# RAG Bench: after-reingest-v2 · 2026-05-27 · mode=text

_Generated: 2026-05-27T13:22:12Z_

## Summary

| 指标 | 值 |
|---|---|
| Query 总数 | 7 |
| Top-1 命中数 | 6/7 |
| 命中率 | 85.7% |
| 平均 Top-1 score | 0.7297 |
| 平均 gap (#1 - #2) | 0.1242 |
| Low-gap 数 (<0.05) | 1/7 |

## Details

| Query | Expected | Actual #1 | Score #1 | Score #2 | Gap | Match? | Notes |
|---|---|---|---|---|---|---|---|
| 财务汇报 | finance_arrow | finance_arrow | 0.7634 | 0.5742 | 0.1892 | ✓ | 财务报告专用模板查询 |
| 团队培训 OKR kickoff | training_team | training_team | 0.6622 | 0.5792 | 0.0830 | ✓ |  |
| 极光渐变 创意 黑底高级感 | creative_aurora | creative_aurora | 0.8454 | 0.6016 | 0.2438 | ✓ |  |
| 企业年报 路演 | enterprise_skyline | enterprise_skyline | 0.6639 | 0.6622 | 0.0017 | ✓ | low-gap; 已知难点 · baseline 时被 finance_arrow 抢 |
| SWOT 工作汇报 | business_geometric | business_geometric | 0.7717 | 0.6487 | 0.1230 | ✓ | 已知难点 · baseline 时被 finance_arrow 抢 |
| 产品介绍 科技 SaaS | product_lineart | product_lineart | 0.7635 | 0.6039 | 0.1596 | ✓ |  |
| 斜切条纹 几何工业 | modern_stripes | business_geometric (expected rank=2) | 0.6377 | 0.5684 | 0.0693 | ✗ |  |

## Per-query top-5 hits

### `财务汇报`

- expected: `tpl:finance_arrow` · rank=1
- expanded: `财务汇报 财报 财务报告 净利润 营收 预算 CFO 年度财务 现金流`

| Rank | ID | Score | Type | Cat/Layout |
|---|---|---|---|---|
| 1 | `tpl:finance_arrow` | 0.7634 | tpl_template | enterprise-finance |
| 2 | `tpl:enterprise_skyline` | 0.5742 | tpl_template | enterprise-modern |
| 3 | `tpl:business_geometric` | 0.5704 | tpl_template | enterprise-strategy |
| 4 | `tpl:product_lineart` | 0.5477 | tpl_template | enterprise-product |
| 5 | `tpl:creative_aurora` | 0.5358 | tpl_template | creative-brand |

### `团队培训 OKR kickoff`

- expected: `tpl:training_team` · rank=1
- expanded: `团队培训 OKR kickoff 团建 OKR kickoff 入职 on-boarding 讲师 workshop 课件`

| Rank | ID | Score | Type | Cat/Layout |
|---|---|---|---|---|
| 1 | `tpl:training_team` | 0.6622 | tpl_template | training-workshop |
| 2 | `tpl:business_geometric` | 0.5792 | tpl_template | enterprise-strategy |
| 3 | `tpl:product_lineart` | 0.5783 | tpl_template | enterprise-product |
| 4 | `tpl:enterprise_skyline` | 0.5723 | tpl_template | enterprise-modern |
| 5 | `tpl:creative_aurora` | 0.5633 | tpl_template | creative-brand |

### `极光渐变 创意 黑底高级感`

- expected: `tpl:creative_aurora` · rank=1
- expanded: `极光渐变 创意 黑底高级感 aurora gradient creative`

| Rank | ID | Score | Type | Cat/Layout |
|---|---|---|---|---|
| 1 | `tpl:creative_aurora` | 0.8454 | tpl_template | creative-brand |
| 2 | `tpl:enterprise_skyline` | 0.6016 | tpl_template | enterprise-modern |
| 3 | `tpl:modern_stripes` | 0.5946 | tpl_template | enterprise-modern |
| 4 | `tpl:product_lineart` | 0.5843 | tpl_template | enterprise-product |
| 5 | `tpl:business_geometric` | 0.5719 | tpl_template | enterprise-strategy |

### `企业年报 路演`

- expected: `tpl:enterprise_skyline` · rank=1
- expanded: `企业年报 路演 年度报告 annual report 投资人 IPO 招股 投融资 executive briefing`

| Rank | ID | Score | Type | Cat/Layout |
|---|---|---|---|---|
| 1 | `tpl:enterprise_skyline` | 0.6639 | tpl_template | enterprise-modern |
| 2 | `tpl:finance_arrow` | 0.6622 | tpl_template | enterprise-finance |
| 3 | `tpl:product_lineart` | 0.6088 | tpl_template | enterprise-product |
| 4 | `tpl:business_geometric` | 0.6078 | tpl_template | enterprise-strategy |
| 5 | `tpl:creative_aurora` | 0.5984 | tpl_template | creative-brand |

### `SWOT 工作汇报`

- expected: `tpl:business_geometric` · rank=1
- expanded: `SWOT 工作汇报 述职 项目复盘 季度汇报 OKR review 工作总结 PPT quadrant 战略分析`

| Rank | ID | Score | Type | Cat/Layout |
|---|---|---|---|---|
| 1 | `tpl:business_geometric` | 0.7717 | tpl_template | enterprise-strategy |
| 2 | `tpl:finance_arrow` | 0.6487 | tpl_template | enterprise-finance |
| 3 | `tpl:training_team` | 0.6192 | tpl_template | training-workshop |
| 4 | `tpl:product_lineart` | 0.5992 | tpl_template | enterprise-product |
| 5 | `tpl:creative_aurora` | 0.5962 | tpl_template | creative-brand |

### `产品介绍 科技 SaaS`

- expected: `tpl:product_lineart` · rank=1
- expanded: `产品介绍 科技 SaaS feature 白皮书 whitepaper 技术架构 feature deck 互联网 工具产品`

| Rank | ID | Score | Type | Cat/Layout |
|---|---|---|---|---|
| 1 | `tpl:product_lineart` | 0.7635 | tpl_template | enterprise-product |
| 2 | `tpl:creative_aurora` | 0.6039 | tpl_template | creative-brand |
| 3 | `tpl:business_geometric` | 0.6034 | tpl_template | enterprise-strategy |
| 4 | `tpl:enterprise_skyline` | 0.5878 | tpl_template | enterprise-modern |
| 5 | `tpl:training_team` | 0.5811 | tpl_template | training-workshop |

### `斜切条纹 几何工业`

- expected: `tpl:modern_stripes` · rank=2
- expanded: `斜切条纹 几何工业 现代 硬朗 diagonal`

| Rank | ID | Score | Type | Cat/Layout |
|---|---|---|---|---|
| 1 | `tpl:business_geometric` | 0.6377 | tpl_template | enterprise-strategy |
| 2 | `tpl:modern_stripes` | 0.5684 | tpl_template | enterprise-modern |
| 3 | `tpl:creative_aurora` | 0.5179 | tpl_template | creative-brand |
| 4 | `tpl:enterprise_skyline` | 0.5124 | tpl_template | enterprise-modern |
| 5 | `tpl:product_lineart` | 0.5024 | tpl_template | enterprise-product |
