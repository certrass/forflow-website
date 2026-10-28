# 数据合作页 · 恢复原画布与工具图标

正式地址：https://forflow.ai/company/data/

- 生产部署 `6ae19dfc2fb8f63096353659`；验证后的 draft `6ae19ca67a626994e22a7dcd`；基线 `6ae198853b135bcbd8a20766`。
- 用户明确反对删除原画布及工具图标。本次恢复两幅原动态画布、工具 Logo 图层、原首屏构图和 15 个工具素材，撤回三步路径图替换。视觉 JS 与删除前 `e79cb57` 字节一致。
- 最新主标题、正文、行业、流程、问答及推荐合作文案来源保持。小尺寸 Logo、手机评估入口、章节高亮和响应式修复保留。后续文案调整保留用户指定的画布与工具视觉。
- 只改变 `/company/data/index.html`、`styles.css`；其余 226 个公开文件、5 个函数及门禁保持。原画布与工具文件此前保留在生产快照，本次恢复引用；当前运行包 27 文件 / 746,169 字节。

维护入口为 `output/afterquery-data-zh/build.py`、`styles.css`、`package.py`；原视觉入口为 `visuals.js`、`assets/source-hero.js` 与 `assets/tools/`。三步路径图来源保留历史，不再挂载。

独立生成、包内引用、原视觉代码比对、主文案来源保持及 JS 语法通过。内置浏览器 1440 × 1000、320 × 844 无页面和目标文本溢出，两画布与工具图层初始化通过，控制台 error/warn 为空。最终手机截图从初始 scrollY=0 捕获，证据见 `evidence/restored-canvas-*`。根静态检查保留独立工作台三个既有错误。

Draft/production 的 27 个运行文件、16 条路由，以及正式域名全部 27 文件回读通过；HTML 仅含平台追加的 Cloudflare 检测脚本，其他字节匹配发布包。未提交合作表单，本地 8899 预览保留。

复现沿用 `../data-20261026/snapshot.py`、`verify.py` 与本目录 `deploy.py`；原始 API 状态和认证信息保留在本机临时目录。
