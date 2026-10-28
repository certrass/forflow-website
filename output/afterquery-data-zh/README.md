# ForFlow 数据资产合作页

正式页面为 <https://forflow.ai/company/data/>，行业区为 `#industries`。本地审阅入口 <http://127.0.0.1:8899/> 保持运行。

2026-10-26 经用户授权发布，部署 ID `6adf4e420116de1e107d68df`。发布对象是本目录根 `index.html`，不是下面保留的 Company / Data 研究实验页。完整发布回执见 `docs/maintenance/releases/data-20261026/`。

## 当前首屏：恢复画布与工具图标（2026-10-28）

已恢复上线，部署 `6ae19dfc2fb8f63096353659`。

按用户反馈恢复删除前的动态画布、工具 Logo 和首屏构图，保留最新正文、推荐合作措辞、小尺寸 Logo 及导航修复。后续文案调整保留这套视觉结构。

视觉入口为 `assets/source-hero.js`、`visuals.js` 与 `assets/tools/`。这两段运行代码与删除前 `e79cb57` 版本一致；三步路径图不再挂载，其来源文件仅留作历史。恢复截图及检查记录见 `evidence/restored-canvas-*`，发布回执在 `docs/maintenance/releases/data-canvas-restore-20261028/`。

## 最新文案（2026-10-28）

已发布至同一正式地址，部署 `6ae198853b135bcbd8a20766`。

按用户「避免防御性表述」的要求，主线调整为业务经验、训练评测用途和合作收益。首屏标题为「让真实业务经验，成为 AI 的学习基础」，六步流程与八问答以具体合作安排说明授权、处理和交付。现有布局、Logo、图片及最高 50 万元奖励保持。

整页文案可审阅 `evidence/copy-review.md`，实际浏览器检查与源码哈希见 `evidence/copy-*.json`。发布回执位于 `docs/maintenance/releases/data-copy-20261028/`。

## 首屏与导航优化（2026-10-28）

已发布至同一正式地址，部署 `6ae1922cf308c48ece9de275`。本轮回执在 `docs/maintenance/releases/data-path-20261028/`。

- 首屏改为业务说明与「业务留痕 → 授权整理 → AI 数据资产」路径图，取消原站画布、工具 Logo 和未使用字体加载。
- 手机顶部始终保留「开启评估」；导航跟随当前章节，修复重复锚点偏移。菜单关闭与原站 CSS 的 1200px 桌面断点对齐。
- 手机样式与原站 810px 行业网格断点衔接，避免 768–809px 行业内容空档；320px 长按钮均衡换行。
- 保留已确认的正文、50 万元奖励、108px / 96px 导航标识及生成配图。前一轮的分栏价值段、三列流程、手机行业展开与八问答继续保留。
- 路径图来源为 `source/data-path.html`；构建和交互入口为 `build.py`、`styles.css`、`script.js`。实测见 `evidence/path-*` 与 `design-qa.md`。

## 当前内容与维护入口

- 首屏、价值主张、九个行业、六步流程及八问答采用本轮精简文案；授权范围、数据处理、保密与收益安排在对应流程和问答中说明。
- 首屏标题为「让真实业务经验，成为 AI 的学习基础」；推荐入口为「推荐企业合作，最高可获 50 万元奖励」。导航 Logo 为桌面 108px、手机 96px。
- `source/zh.json`：页面文案；`source/faq.json`：八个本地化问答；`source/site.json`：页面元信息与 ForFlow 联系地址。
- `build.py`：从捕获的结构生成 `index.html`；命令 `python build.py`，需安装 `beautifulsoup4`。修改来源后生成，不只修改产物。
- `styles.css`、`script.js`：排版、菜单与章节高亮；`visuals.js`、`assets/source-hero.js`：原动态画布及工具图标，当前正式页恢复加载。

## 发布维护

先运行 `build.py` 生成，再运行 `python package.py /path/to/publish-root`。包只包含正式页面及所需资产，共 27 个文件（约 746 KB）；发布版增加 canonical 并将 robots 改为 `index, follow`，本地预览仍为 noindex。`scripts/build_public.py` 已加入这个打包入口，后续全站构建会保留 `/company/data/`。

发布沿用最新线上快照，只覆盖本页变更的运行文件。其他页面、5 个函数及门禁 edge bundle/manifest 保持；旧版页面可能引用的历史资产仍保留在生产快照中。

## 合作入口

四个主要行动按钮及页脚咨询链接使用现有 ForFlow 飞书通用咨询表单：
<https://zenithlink.feishu.cn/share/base/form/shrcnX80RM22yy6IxZYHCrkpwye>

地址来源为主工作目录的 `templates/index.html`，此前 HTTP 回读为 200。在线浏览器读取超时，没有测试提交，也没有创建专门的数据评估或引荐表单。将来更换专用接收入口，只需修改 `source/site.json`。页面不再含 AfterQuery 正文、品牌、申请链接、原站条款或三天回复等旧承诺。

## 图片与来源

- 行业照片使用内置 image_gen 生成的虚构中国企业办公场景：`assets/generated/work-records-office-v1.jpg`。PNG 原图、JPG 网页版、提示词与哈希记录在 `source/generated-images.json`；手机裁切焦点为 `50% 35%`。
- `expert-data-review-v1` 为未使用备选。用户澄清只修改当前数据伙伴页后，已撤回该图在 Company / Data 页的试放。
- ForFlow 标识来自本库已有资产，本地 Inter 字体来自既有首页预览。布局来源为 AfterQuery 数据合作页，原始捕获及资产来源留在 `source/reference.html`、`source/assets.json`；页面呈现已按 ForFlow 定稿替换。
- 首轮原站对照及中间截图保留历史，不代表当前文案。首轮文案本地化证据为 `evidence/localized-desktop.png`、`localized-mobile.png`、`localized-full.png` 和 `localization-verification.json`。

## 独立 Company / Data 页

此前新增的 <http://127.0.0.1:8899/company/data/> 仍保留，来源为 `source/company-data.html`、`company-data.css` 和 `company-data.js`。用户后续明确以根数据伙伴页为本轮修改对象；本轮未修改 Company / Data 的内容和布局。

## 验证

- 独立构建、八问答/六流程/四行动入口、旧文案残留、本地资源、锚点、重复 ID、外部链接安全属性及 JavaScript 语法检查通过。
- 实际浏览器检查 1440 × 1000、390 × 844 和 320px 宽布局，无页面横向溢出；320px 长标题、按钮、流程标题无文字容器溢出。手机菜单及 Esc、更多问答、脱敏问答展开/收起通过；控制台无 error / warn。
- 根目录 `tests/static_check.py` 仍报告既有 `workbench_prototype.html` 的 stylesheet、search modal 和 footer 三项缺失，本轮未修改该文件。
- 本轮没有验证实际数据处理、脱敏审计、结算服务或表单提交；已完成网站内容、链接及排版更新与本页发布。
