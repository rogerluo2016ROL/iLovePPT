# Fixture 02 · Brief 输入

## user_initial_request

```
给团队讲一下新一代订单系统的三层架构,30 分钟,工程师听。
有 perf benchmark 数据(_assets/raw/bench.csv),需要架构图。
```

## user_responses

| brainstorm 提问 | 标准回答 |
|---|---|
| audience | technical |
| duration_min | 30 |
| presentation_mode | speaker |
| top_recommendation | 新一代订单系统三层架构把 P99 延迟从 820ms 降到 130ms,Q3 灰度 |
| theme | tech_blue |
| 数据? | _assets/raw/bench.csv |
| 架构图?现画还是有? | 现画(让 author 调 draw.io 出) |
| brief.md OK? | OK |
| outline / content / critic / audience 各 checkpoint | 一律照 fixture 01 风格(批准 / 接受 notes / cherry-pick 视觉建议) |

## 准备素材

```bash
WORKDIR=/tmp/eval_<timestamp>/decks/02-tech-architecture
mkdir -p $WORKDIR/_assets/raw

cat > $WORKDIR/_assets/raw/bench.csv <<EOF
endpoint,p50_ms,p99_ms,qps,error_rate
order_create_v1,180,820,1200,0.024
order_create_v2,42,130,3800,0.003
order_query_v1,95,420,5400,0.012
order_query_v2,28,68,12000,0.0008
EOF
```
