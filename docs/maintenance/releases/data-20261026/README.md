# 数据资产合作页正式发布 · 2026-10-26

- 正式地址：https://forflow.ai/company/data/
- 部署：`6adf4e420116de1e107d68df`；先验证 draft `6adf4dd9f37c52372bf84c6b` 后，以同一文件摘要创建正式部署。
- 来源：`output/afterquery-data-zh/` 的根数据伙伴页。旧的独立 `company/data/index.html` 研究实验不在发布包内。
- 35 个运行文件，约 1 MB；新增路径均在 `/company/data/`。原有 193 个文件的摘要、5 个函数及配置、edge bundle/manifest 全部保持。
- `data-package.json` 对应实际源码与发布文件摘要；`release-receipt.json` 对应平台版本；`draft-qa.json` / `production-qa.json` 记录线上文件和路由结果。

## 验证与边界

- 独立生成和打包通过，后续全站构建入口已接入数据页打包；该入口产出的 35 个文件与本次部署逐字节一致，维护回执没有进入公开目录。
- Draft 与正式部署 URL 的 35 个文件 HTTP 200 且与发布包一致；自有域名 35 个资源 HTTP 200。自有域名 HTML 只有 Cloudflare 追加的 JavaScript detection script，移除这一平台注入后页面字节完全一致，其余资源字节相同。
- 16 条路由检查覆盖数据页三种地址、公司页、产品页、AI 治理、主页/案例/API 的原门禁响应及短链 404；`nosniff` / `SAMEORIGIN` 保持。
- 桌面、手机、菜单和问答交互在本地完成。远端内置浏览器导航超时，未声称完成远端交互复验。直接访问自有域名的部分请求超时，经现有 Veee 代理重试完成全部 HTTP 回读。
- 根静态检查仍报告发布范围外 `workbench_prototype.html` 的 stylesheet、search modal、footer 三项既有缺失。本次只发布新增路径，旧全站构建没有上传。
- 表单复用现有 ForFlow 通用咨询表单，未测试提交；网站展示不等于已验证实际脱敏、审计或结算后台。

## 复现发布

依赖 Python 与仓库 `requirements.txt`；Netlify 认证读取系统已有 CLI 配置，脚本不含密钥。原始 API 快照仅留在本机临时目录，不提交或公开。

1. `python output/afterquery-data-zh/build.py`
2. `python output/afterquery-data-zh/package.py /private/tmp/forflow-data-release-YYYYMMDD/package`
3. `python docs/maintenance/releases/data-20261026/snapshot.py /private/tmp/forflow-data-release-YYYYMMDD`
4. `python docs/maintenance/releases/data-20261026/deploy.py draft /private/tmp/forflow-data-release-YYYYMMDD`
5. `python docs/maintenance/releases/data-20261026/verify.py draft /private/tmp/forflow-data-release-YYYYMMDD`
6. 在相应生产发布授权下，将命令中的 draft 换为 production，再回读自有域名。

每次使用新的临时目录。创建部署前检查生产 base 未变化；production 要求对应 payload 的 draft QA 已通过。网络需要代理时使用 `tools/with-veee-proxy.sh` 包裹命令。
