# 数据合作页 · 首屏路径与导航优化

正式地址：https://forflow.ai/company/data/

- 生产部署：`6ae1922cf308c48ece9de275`；验证后的 draft：`6ae190a421f24ad84fcaccbb`。
- 基线生产：`6adf5849ad615a73004034d9`。只改变 `/company/data/index.html`、`styles.css`、`script.js`，其余 225 个文件、5 个函数及门禁 bundle/config 保持。
- 来源为 `output/afterquery-data-zh/build.py`、`source/data-path.html`、`styles.css`、`script.js` 与 `package.py`；实验研究页没有发布。
- 首屏将原站动画与工具 Logo 改为可访问的三步业务路径。手机保留直接评估入口；导航高亮当前章节并修正锚点偏移。菜单与 1200px 桌面断点对齐，手机行业与 810px 网格断点衔接，窄屏长按钮均衡换行。
- 本页运行包共 10 文件 / 678,633 字节。旧版使用的历史资源仍保留在生产快照中，避免破坏缓存页面；没有将包大小当成实测加载耗时。

浏览器实际验证 320/390/768/811/1024/1025/1440 CSS 像素宽度，无横向溢出。四章节导航、桌面与手机定位、原生行业/FAQ 键盘开合、Escape 焦点返回及 768→1201px 菜单关闭通过，控制台 error/warn 为空。截图和详细结果在 `output/afterquery-data-zh/evidence/path-*`；本地 8899 预览保持可用。未宣称生产浏览器或物理 iOS 检查，也未提交合作表单。

独立构建可复现、运行引用闭合、8 问答/9 行业/6 流程/3 路径、锚点/外链、JS 语法和差异检查通过。根静态检查保留发布范围外工作台的三个既有缺失。

Draft 与 production 均完成 10 个运行文件、16 条路由验证；自有域名全部 10 文件回读通过，HTML 仅有 Cloudflare 平台追加的检测脚本，其余字节一致。详见 `draft-qa.json`、`production-qa.json`、`data-package.json` 和 `release-receipt.json`。

复现沿用 `../data-20261026/snapshot.py`、`verify.py` 及本目录 `deploy.py`。首次 draft 创建回执因网络截断，先回读定位同一候选，再补传三个变更文件，未重复创建或发布旧版。原始 API 快照和认证状态仅保存在本机临时目录。
