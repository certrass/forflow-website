# ForFlow 数据资产合作页

正式页面为 <https://forflow.ai/company/data/>，行业区为 `#industries`。本地审阅入口 <http://127.0.0.1:8899/> 保持运行。

2026-10-26 经用户授权发布，部署 ID `6adf4e420116de1e107d68df`。发布对象是本目录根 `index.html`，不是下面保留的 Company / Data 研究实验页。完整发布回执见 `docs/maintenance/releases/data-20261026/`。

## 最新优化

已发布至同一正式地址，部署 `6adf5849ad615a73004034d9`。本轮回执在 `docs/maintenance/releases/data-reading-20261026/`。

- 价值段分清标题和解释；流程改为桌面三列、手机纵向阅读。
- 手机九个行业直接展开，全部八个问答无需额外点击「查看更多」。
- 首屏说明无需上传原始数据，导航「开启评估」直达现有表单；菜单外部点击与跨断点关闭完善。
- 新文案入口为 `source/ui.json`，结构与交互入口仍为 `build.py`、`styles.css`、`script.js`。本轮实测见 `evidence/reading-verification.json` 与 `design-qa.md`。

## 当前内容与维护入口

- 以用户提供的完整定稿统一首屏、价值主张、九个行业、六步流程、行动按钮及页脚。法律段按用户的核心纠错去掉「特权」，采用执业保密、涉密材料与未公开底稿边界。
- 首屏标题为「企业真实业务数据，审慎合规授权」；推荐入口为「成为生态引荐人，享最高 50 万元居间奖励」。导航 Logo 为桌面 108px、手机 96px。
- `source/zh.json`：页面文案；`source/faq.json`：八个本地化问答；`source/site.json`：页面元信息与 ForFlow 联系地址。
- `build.py`：从捕获的结构生成 `index.html`；命令 `python build.py`，需安装 `beautifulsoup4`。修改来源后生成，不只修改产物。
- `styles.css`、`script.js`：排版与菜单、问答交互；`visuals.js` 与 `assets/source-hero.js`：既有首屏画布。

## 发布维护

先运行 `build.py` 生成，再运行 `python package.py /path/to/publish-root`。包只包含正式页面及 35 个运行文件；发布版增加 canonical 并将 robots 改为 `index, follow`，本地预览仍为 noindex。`scripts/build_public.py` 已加入这个打包入口，后续全站构建会保留 `/company/data/`。

本次采用线上快照增量发布，193 个已有文件、5 个函数及门禁 edge bundle/manifest 的摘要均保持。没有从旧工作区发布全站。

## 合作入口

四个主要行动按钮及页脚咨询链接使用现有 ForFlow 飞书通用咨询表单：
<https://zenithlink.feishu.cn/share/base/form/shrcnX80RM22yy6IxZYHCrkpwye>

地址来源为主工作目录的 `templates/index.html`，本轮 HTTP 回读为 200。在线浏览器读取超时，没有测试提交，也没有创建专门的数据评估或引荐表单。将来更换专用接收入口，只需修改 `source/site.json`。页面不再含 AfterQuery 正文、品牌、申请链接、原站条款或三天回复等旧承诺。

## 图片与来源

- 行业照片使用内置 image_gen 生成的虚构中国企业办公场景：`assets/generated/work-records-office-v1.jpg`。PNG 原图、JPG 网页版、提示词与哈希记录在 `source/generated-images.json`；手机裁切焦点为 `50% 35%`。
- `expert-data-review-v1` 为未使用备选。用户澄清只修改当前数据伙伴页后，已撤回该图在 Company / Data 页的试放。
- ForFlow 标识来自本库已有资产，本地 Inter 字体来自既有首页预览。布局来源为 AfterQuery 数据合作页，原始捕获及资产来源留在 `source/reference.html`、`source/assets.json`；页面呈现已按 ForFlow 定稿替换。
- 首轮原站对照及中间截图保留历史，不代表当前文案。当前证据为 `evidence/localized-desktop.png`、`localized-mobile.png`、`localized-full.png` 和 `localization-verification.json`。

## 独立 Company / Data 页

此前新增的 <http://127.0.0.1:8899/company/data/> 仍保留，来源为 `source/company-data.html`、`company-data.css` 和 `company-data.js`。用户后续明确以根数据伙伴页为本轮修改对象；本轮未修改 Company / Data 的内容和布局。

## 验证

- 独立构建、八问答/六流程/四行动入口、旧文案残留、本地资源、锚点、重复 ID、外部链接安全属性及 JavaScript 语法检查通过。
- 实际浏览器检查 1440 × 1000、390 × 844 和 320px 宽布局，无页面横向溢出；320px 长标题、按钮、流程标题无文字容器溢出。手机菜单及 Esc、更多问答、脱敏问答展开/收起通过；控制台无 error / warn。
- 根目录 `tests/static_check.py` 仍报告既有 `workbench_prototype.html` 的 stylesheet、search modal 和 footer 三项缺失，本轮未修改该文件。
- 本轮没有验证实际数据处理、脱敏审计、结算服务或表单提交；已完成网站内容、链接及排版更新与本页发布。
