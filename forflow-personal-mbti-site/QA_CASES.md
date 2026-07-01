# QA Cases

## Goals

- 每次打开页面都生成新的 `visit_id`、`session_id`、`assessment_id`，同一个浏览器保留稳定 `visitor_id`。
- 每次答题都记录题目、选项序号、选项文案、修订号和当前问卷编号。
- 完成后结果 payload 包含 20 条最终答案，可用于聚类、归因和漏斗统计。
- CTA、分享、重测、回退、异常补发都能作为事件查询。

## Local Capture

```bash
npm run qa:server
```

打开：

```text
http://127.0.0.1:5181/?utm_source=qa&utm_campaign=personal_cases
```

抓取前端真实提交：

```text
http://127.0.0.1:5181/__qa/payloads
```

重置抓取：

```bash
curl -X POST http://127.0.0.1:5181/__qa/reset
```

## Required Cases

1. 新打开页面：应出现 `page_view`，且带 `utm_source`、`utm_campaign`、页面 URL、客户端时区。
2. 点击开始：应出现 `start_click`、`screen_view:quiz`、第 1 题 `question_view`。
3. 第一题双击同一选项：只应进入第 2 题，且只新增 1 条 `answer_select`。
4. 答完第 2 题后点上一题：应出现 `step_back`，并记录 `from_step`、`to_step`、被移除答案。
5. 回退后改选第 2 题：第 2 题最终答案应保留新选项，`answer_revision` 应递增。
6. 完成 20 题：应出现 `quiz_complete`、`result_view`、`result` payload、`result_submit_ok`。
7. 结果 payload：`answers_indexed.length` 必须为 20；每条答案有 `answer_option_index` 和 `selected_option_indices`。
8. 点击二维码区域：应出现 `qr_click`，`cta_key` 为 `qr_follow`，页面提示长按识别。
9. 点击分享本测试：应出现 `share_click`，`cta_key` 为 `share_test`，页面出现测试链接复制成功 toast。
10. 点击测试编号：应出现 `diagnosis_id_copy`，并复制当前 `assessment_id`。
11. 点击重测：应出现 `retry_click`，页面回到封面；再次开始应使用新的 `assessment_id`。
12. 刷新或重新打开：应生成新的 `visit_id` 和 `assessment_id`，但同浏览器的 `visitor_id` 可保持一致。

## Data Gates

- `event_id` 不重复。
- 每个完成结果都有 20 条最终答案。
- `answer_select` 事件数量允许大于 20，因为回退改选会留下历史轨迹。
- `personal_mbti_results.assessment_id` 与 `personal_mbti_answers.assessment_id` 必须能一一关联。
- `received_at_bj_text` 使用 `+08:00` 北京时间文本。
