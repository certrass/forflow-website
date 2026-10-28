# 数据合作页 · 文案调整

正式地址：https://forflow.ai/company/data/

- 最终部署 `6ae198853b135bcbd8a20766`；验证后的 draft `6ae197f55ecbb2d743238246`。
- 基线 `6ae19673db7b9d848b4672fe` 为本轮中间文案版本；最终按用户反馈，将推荐入口统一为「推荐企业合作，最高可获 50 万元奖励」，页脚为「推荐合作」。
- 仅 `/company/data/index.html` 变化，其余 227 个文件、5 个函数及门禁保持；CSS、JS、Logo、图片和版式保持。
- 维护入口为 `source/zh.json`、`faq.json`、`ui.json`、`site.json`、`data-path.html` 及 `build.py`。整页审阅稿为 `evidence/copy-review.md`，由当前 HTML 生成。

本轮将主线改为数据价值、训练评测用途与具体合作安排，融入用户关于数据质量、专家协作及领域知识的主张。删除反复的否定、排除与免责句式，授权、脱敏、权限及收益通过对应流程和问答说明。

构建、10 文件引用闭合、8 问答/9 行业/6 流程、链接/ID/金额及旧词检查通过。本地 1440 × 1000、320 × 844 无目标文本或页面溢出，新问答键盘展开通过，控制台 error/warn 为空；截图和源码摘要见 `evidence/copy-*`。根静态检查保留发布范围外工作台的三个既有错误。

Draft 与 production 均通过 10 文件、16 路由回读，正式域名的 10 文件也与包一致（HTML 仅有平台追加的 Cloudflare 检测脚本）。未提交合作表单。本地 8899 预览保留。

复现使用 `../data-20261026/snapshot.py`、`verify.py` 及本目录 `deploy.py`；原始 API 状态与认证信息只在本机临时目录。
