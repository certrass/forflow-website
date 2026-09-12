# ForFlow 官网数据基础

## 当前边界

官网保持静态站点，写入只经过 Netlify Functions。浏览器不持有 Supabase 密钥，也不直接访问数据库。

| 入口 | 用途 | 数据表 |
| --- | --- | --- |
| `/api/events` | 十个白名单产品事件 | `website_events` |
| `/api/assessments` | 场景诊断及规范化答案 | `assessments`、`assessment_answers` |
| `/api/leads` | 咨询与诊断报告留资 | `leads`、`consent_records` |

联系人身份只保存在 `leads`。事件、诊断和答案表不保存姓名、邮箱、电话或表单自由文本。`assessment_id` 用于把用户主动提交的留资与诊断关联起来。

门禁邀请码仍由 Netlify Edge Function 管理，与未来的用户注册、Supabase Auth 和客户工作区分开。本阶段没有开放账号注册。

## 数据库

迁移文件：`supabase/migrations/20260711053849_website_data_foundation.sql`

正式上线前，在目标 Supabase 项目执行：

```bash
supabase link --project-ref <project-ref>
supabase db push --linked
supabase db lint --linked --level warning --fail-on error
```

迁移为所有网站表启用 RLS，撤销 `anon` 和 `authenticated` 权限，并明确授权 `service_role`。Functions 优先使用新版 `SUPABASE_SECRET_KEY`；兼容旧项目的 `SUPABASE_SERVICE_ROLE_KEY` 只作为迁移期备选。

## Netlify 环境变量

| 变量 | 必需 | 说明 |
| --- | --- | --- |
| `SUPABASE_URL` | 是 | 目标项目 URL |
| `SUPABASE_SECRET_KEY` | 是 | 仅 Functions 使用的服务端 secret key |
| `RESEND_API_KEY` | 邮件启用时 | 发送内部通知和诊断报告 |
| `LEADS_FROM_EMAIL` | 邮件启用时 | 已在 Resend 验证的发件人，例如 `ForFlow <website@forflow.ai>` |
| `CLOUDFLARE_WEB_ANALYTICS_TOKEN` | 页面统计启用时 | 公开 beacon token；只有配置后公开构建才注入脚本 |

`hello@forflow.ai` 是内部线索通知收件地址，已经固定在服务端函数里。不要把 Supabase 或 Resend 密钥写入 HTML、`script.js` 或仓库文件。

## 上线顺序

1. 新建或确认 Supabase 生产项目，应用迁移并运行 linked lint。
2. 在 Resend 验证 `forflow.ai` 发件域名和发件地址。
3. 在 Netlify 配置上述环境变量，范围至少包含 Production；Deploy Preview 使用单独的测试项目或保持写入关闭。
4. 先部署 preview，完成一次诊断、报告留资和普通咨询；核对四张业务表和 consent 记录。
5. 确认事件表没有邮箱、查询字符串和自由文本，答案表没有联系信息。
6. 发布生产并观察 Function 错误率、限流和邮件退信。

## 保留与删除

当前隐私说明给出的默认目标是：匿名事件不超过 13 个月，未留资诊断不超过 90 天，联系信息在最后一次有效沟通后不超过 12 个月。上线前还需在 Supabase 配置定时清理任务；在任务启用前，不应对外声称删除已经完全自动化。

删除留资时应先删除或匿名化 `leads` 及相应 `consent_records`。诊断记录是否同时删除，按用户请求和业务留存依据判断；匿名事件不反向保存联系人身份。

## 暂未开放

- Supabase Auth、账号注册和客户工作区
- 报告 PDF 私有存储；当前报告由服务端邮件正文生成
- 营销自动化、用户画像和任意自定义事件
- 将邮箱、电话或表单原文写入事件属性
