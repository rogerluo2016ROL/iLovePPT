# Fixture 05 · Brief

## user_initial_request

```
做一份本周技术部门周报,10 分钟看完(读,不讲),给 VP 看。
有本周指标(_assets/raw/weekly_metrics.csv)。
```

## user_responses

| brainstorm 提问 | 标准回答 |
|---|---|
| audience | executive(VP 是高管) |
| duration_min | 10 |
| **presentation_mode** | **handout**(关键:读手册不演讲) |
| top_recommendation | 本周技术部交付 3 大里程碑(订单 v2 上线 / 灰度 P99 降 6× / Sec 0 高危),Q3 OKR 完成 73% |
| theme | tech_blue |
| structure_mode? | data_report(周报是数据驱动,bypass_pyramid: true) |
| 数据 | _assets/raw/weekly_metrics.csv |
| 其他 checkpoint | 标准流程 |

## 准备素材

```bash
WORKDIR=/tmp/eval_<timestamp>/decks/05-handout-weekly
mkdir -p $WORKDIR/_assets/raw

cat > $WORKDIR/_assets/raw/weekly_metrics.csv <<EOF
metric,this_week,last_week,delta_pct
orders_completed,28400,26100,8.8
api_p99_ms,130,820,-84.1
incidents_p0,0,1,-100
sec_high_vuln,3,7,-57.1
okr_progress_pct,73,68,7.4
EOF
```
