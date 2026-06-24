# ForFlow 网站更新记录

这个文件用于记录每次网站更新后的维护事实。凡是改动页面、生成脚本、样式、图片、测试、部署配置或内容口径，都应在交付前追加一条记录。

记录规则：

- 新记录放在最上方，日期使用 `YYYY-MM-DD`。
- 每条记录至少包含 `变更范围`、`主要变更`、`验证`、`后续` 四段。
- `验证` 只写真实跑过的命令、人工检查或部署结果；没有跑就写“未跑”并说明原因。
- 涉及案例、服务页、一级页面时，同时说明对应的维护入口，例如 `build_site.py`、`templates/`、`CASE_LIBRARY_ITEMS` 或具体 HTML。

## 2026-06-25

### 变更范围

- 案例中心、搜索页、医疗案例详情页、汽车 DFMEA 案例详情页、案例视觉资源、生成脚本、静态检查、交互检查、视觉/滚动检查、维护文档。

### 主要变更

- 将案例中心的内容入口收敛到 `build_site.py` 的 `CASE_LIBRARY_ITEMS`，让 `cases.html` 和 `search.html` 可以通过同一份 Python 清单联动更新。
- 将 `case-healthcare-agent-roi.html` 纳入案例中心和搜索结果；保留 P&ID 案例为同一套案例 Blog 模板的样例。
- 医疗案例 hero 使用无可读文字的 Sana 风格场景图，正文证据图保留 diagram 性质。
- 调用 imagegen，基于原英文护理点工作流和患者语音智能体流程图的结构生成中文化 diagram，并替换正文 figure；英文 diagram 原图保留在仓库作为结构参考。
- 为医疗案例正文补充两张无可读文字的 Sana 风格场景插图：`assets/cases/healthcare-model-evaluation-sana-plain.png` 与 `assets/cases/healthcare-voice-agent-service-desk-sana-plain.png`，分别放入模型训练发现和语音智能体章节。
- 为医疗案例 hero 图补充响应式 16:9 场景图规则，正文 diagram 使用 `case-figure--contain` 保持完整展示。
- 新增汽车工程案例 `case-automotive-dfmea-ontology-agent.html`，以 B 柱 DFMEA 为例讲解工程本体、RFLP、智能体 AI、跨项目知识迁移和 AgentCore / Strands SDK 下篇预告；同步加入 `CASE_LIBRARY_ITEMS`、`cases.html` 和 `search.html`。
- 为汽车 DFMEA 案例生成无文字、Sana 风格的 B 柱工程场景 hero 图：`assets/cases/automotive-dfmea-bpillar-hero.png`。
- 修复案例详情页手机端上下滑动时页面“来回晃”的问题：手机端案例目录不再使用 `overflow-x: clip`，改为 `overflow-x: hidden`、`overscroll-behavior-x: none`、`touch-action: pan-y`，避免触摸上下滑时被横向裁剪区域抢手势。
- 收窄 scrollspy 自动居中逻辑：只有目录确实横向溢出且未换行时，才调用 `scrollIntoView`；案例详情页手机端换行目录只保留高亮，不再反向拉动页面纵向位置。
- 为所有生成 HTML 的 `styles.css` 和 `script.js` 链接加入版本号 `v=20260625-case-scroll-v3`，避免本地浏览器、微信内置浏览器或 Netlify 缓存继续读取旧 CSS/JS。
- 更新 `tests/static_check.py`，增加案例清单、案例中心、搜索页联动检查。
- 更新 `tests/interaction_check.py`，增加案例筛选、医疗搜索、案例 tab 等交互检查。
- 更新 `tests/interaction_check.py`，新增 DFMEA 搜索命中汽车案例的交互检查。
- 更新 `tests/polished_pages_check.py`，覆盖首页、Playbook、案例中心、医疗案例和汽车 DFMEA 案例的桌面/手机视口、图片加载、控制台错误、导航交互、案例交互、上下滑动检查，并新增手机端案例目录不得横向滚动的断言。
- 新增本文件和 `docs/maintenance/site-governance.md`，把更新留痕和发布门禁纳入仓库维护流程。

### 验证

- `python3 build_site.py`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 python3 tests/interaction_check.py`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 python3 tests/polished_pages_check.py`

验证结果：

- 静态检查通过：16 个 HTML 页面、本地资源、案例清单与搜索联动均通过。
- 交互检查通过：桌面搜索弹层、手机菜单、Navigator、FAQ、案例筛选、医疗搜索与 DFMEA 搜索均通过。
- 视觉/滚动检查通过：首页、Playbook、案例中心、医疗案例、汽车 DFMEA 案例在桌面和手机端均无横向溢出、无坏图、无控制台错误；每页 `reachedBottom=true` 且 `returnedTop=true`。
- 医疗正文 diagram 中文化修正后复核：`healthcare-point-of-care-workflow-zh.png` 与 `healthcare-voice-agent-state-machine-zh.png` 在桌面和手机端均完整加载，手机端页面 `scrollWidth=390`、`innerWidth=390`。
- 汽车 DFMEA 案例加入后复核：`cases.html` 总案例卡 10 个；`search.html?search=DFMEA` 命中汽车案例 1 条。
- 案例详情页滑动修复后复核：医疗案例手机端 `.case-toc` 为 `position=static`、`overflowX=hidden`、`clientWidth=362`、`scrollWidth=362`；汽车 DFMEA 案例手机端同样为 `position=static`、`overflowX=hidden`、`clientWidth=362`、`scrollWidth=362`；两页均 `reachedBottom=true`、`returnedTop=true`、`scrollIntoViewCalls=[]`。

### 后续

- 每次新增案例时，先补 `case-*.html` 和图片，再更新 `CASE_LIBRARY_ITEMS`，最后记录在本文件。
- Netlify 重新部署后，应补充部署时间、部署链接和回归检查结果。
- 表单接口、CRM/CMS、隐私条款和正式域名仍属于上线前治理项。

## 2026-06-24

### 变更范围

- 首页标题排版、桌面 mega-nav、子页面导航一致性、手机端首屏展示、浏览器与代理排查、Netlify 预览部署。

### 主要变更

- 调整首页主要标题的 `line-height`，解决中文多行大标题在手机端笔画重叠、上下行过紧的问题。
- 修复桌面端 mega-nav 下拉面板在鼠标移入面板时立即消失的问题：保留 hover 预览，关闭交给外部点击、同项触发和 Escape。
- 优化不同顶部导航项切换时的下拉动画，使切换更平滑。
- 排查子页面旧式 header 与首页完整 mega-nav 不一致的问题，推动子页面统一到同一套导航结构与 active 状态。
- 对手机端首页首屏进行了视口检查，识别并修正“流入业务”大标题笔画重叠的移动端问题。
- 排查 Veee 代理、GitHub、Netlify、curl 与 Chrome 调试端口不稳定问题，并沉淀 `tools/with-veee-proxy.sh` 和 `tools/veee-proxy-env.sh` 作为代理应急入口。

### 验证

- 当日主要通过本地浏览器视口检查、截图反馈和局部交互排查验证。
- 2026-06-25 已将其中一部分高频风险固化进 `tests/interaction_check.py` 和 `tests/polished_pages_check.py`，后续应以脚本结果为准。

### 后续

- 子页面导航 active 状态、手机菜单、搜索弹层和滚动表现需要在每次大改后持续复查。
- 代理端口会随 Veee 节点切换变化，外部网络问题不要直接归因到 GitHub、Netlify 或浏览器本身。
