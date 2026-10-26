# 数据合作页 · 阅读与手机交互优化

正式地址：https://forflow.ai/company/data/

- 生产部署：`6adf5849ad615a73004034d9`；验证后的 draft：`6adf57e7afbd3cc5a5a0bf3a`。
- 基于上一生产 `6adf4e420116de1e107d68df`，仅改变 `/company/data/index.html`、`styles.css`、`script.js`；其余 225 个文件、5 个函数及 edge 门禁 bundle/config 保持。
- 源码维护：`output/afterquery-data-zh/build.py`、`styles.css`、`script.js` 和 `source/ui.json`。原始业务正文保留，新增说明来自原 FAQ，未引入新业务承诺。
- 价值标题与解释分层；六步流程增加阅读宽度；手机九行业使用原生展开列表，保留生成图片；八个问答直接列出；菜单完善外部点击与跨断点关闭。

本地实际验证 1440 × 1000、1024 × 900、390 × 844、320 × 844 的布局、窄屏文字边界、行业键盘展开、隐私问答开合、菜单 Escape/焦点返回/外部点击/断点关闭。控制台 error/warn 为空。证据及源码哈希见 `output/afterquery-data-zh/evidence/reading-verification.json`，截图为 `reading-*.png`。

独立生成、35 文件打包、JS 语法、文案与锚点/外链校验通过。根静态检查仍为不在本次发布范围内的 `workbench_prototype.html` 三项既有结构缺失。远端浏览器读取超时，不将本地交互宣称为远端交互复验；HTTP 文件与路由结果单独记录。没有提交飞书咨询表单或测试实际数据处理服务。

复现使用上一发布目录的 `snapshot.py`、`verify.py` 与本目录的 `deploy.py`。本次 deploy 脚本按 Netlify 已存储的路径大小写复用键名，避免重复添加大小写不同的字体路径；保留原始文件与函数摘要、生产 base 检查以及 draft QA 门禁。原始 API 快照和认证信息只留在本机，不进入仓库或公开目录。

Draft 与 production 均完成 35 个资源、16 条路由回读。自有域名 HTML 仅包含 Cloudflare 追加的检测脚本，原页面字节一致；其他资源与包内文件完全一致，既有访问状态及响应头保持。详见 `draft-qa.json`、`production-qa.json`、`data-package.json` 与 `release-receipt.json`。
