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
- 强化 `search.html` 的静态搜索体验：增加查询归一化、技术词别名扩展、相关度排序、命中高亮、结果摘要和常用搜索入口；`DFMEA`、`B柱`、`AgentCore`、`P&ID` 等混合中英文关键词均能命中对应案例。
- 将全站静态资源版本更新为 `v=20260625-search-reading-v4`，同时刷新 CSS 与 JS 缓存。
- 重写汽车 DFMEA 案例为更接近原文密度的长文结构，恢复 B 柱安全职能、DFMEA 困境、行业压力、电子表格 AI 的局限、工程本体、RFLP、事件驱动、多智能体分工和七维价值链等技术细节。
- 为汽车 DFMEA 案例新增“给非技术读者的读法”和“公开技术背景”段落，并补充 NHTSA FMVSS 214 / 216a、IIHS roof strength、AHSS/22MnB5、AIAG-VDA FMEA、Amazon Bedrock AgentCore 与 Strands SDK 等公开资料链接。
- 统一案例页排版标准：旧案例详情模板、新案例 Blog 模板、案例中心卡片、正文 figure/caption、callout、决策卡、底部 CTA 与来源区统一放宽中文标题和正文行高，并为 DFMEA、RFLP、AgentCore、22MnB5、FMVSS、P&ID、EHR 等长技术词增加安全换行。
- 将案例中心筛选标签从旧占位标签整理为业务分类：`manufacturing`、`healthcare`、`service`、`education`、`data`；医疗案例归入 `healthcare service data`，汽车 DFMEA 归入 `automotive manufacturing data`。
- 将全站静态资源版本更新为 `v=20260625-case-reading-v5`，刷新案例排版和筛选标签缓存。
- 将搜索页从纯 HTML 文本关联升级为 `search-index.json` 驱动：`build_site.py` 统一生成案例、服务、资源和业务分类索引，`search.html` 只保留首屏/fallback 卡片，运行时由 `script.js` 拉取 JSON 索引渲染结果。
- 新增 `SEARCH_CORE_ITEMS` 和 `SEARCH_TYPE_LABELS` 作为一级页面、服务页、资源页的搜索维护入口；案例搜索仍从 `CASE_LIBRARY_ITEMS` 派生，避免新增案例后还要手工同步多份 HTML。
- 强化搜索页运行态：支持 JSON 索引版本校验、实时输入搜索、URL 查询同步、分类 tab 计数、关键词别名、命中高亮、首条命中标记；JSON 加载失败时自动退回静态 HTML 结果。
- 将全站静态资源版本更新为 `v=20260625-search-index-v6`，刷新搜索索引、CSS 与 JS 缓存。
- 修复全部案例详情页手机端章节标题过大、行距被通用规则覆盖和 hash/目录定位时顶部余量不足的问题；旧模板 Wren 与新模板 P&ID、医疗、汽车案例均纳入同一套移动端标题检查。
- 为案例正文 section 增加 `scroll-margin-top`，移动端放大 `.case-toc` 与正文的间距，并将案例详情 H2 从通用移动标题组中拆出，避免后续规则再次覆盖专用行高。
- 将全站静态资源版本更新为 `v=20260625-case-heading-v7`，刷新案例标题样式、搜索索引、CSS 与 JS 缓存。
- 将汽车 DFMEA 案例重新调整为更能让制造业老板产生共鸣的表达：把“知识流失、老师傅经验断档、ECO 复评、供应商换线、历史项目教训迁移”放到首屏和证据栏，同时保留 B 柱、DFMEA、本体、RFLP、多智能体和 AgentCore / Strands SDK 技术细节。
- 将汽车案例搜索文本补充 `知识流失`、`老师傅经验`、`组织记忆`、`经验断档`、`供应商教训`、`设计变更复评` 等关键词，确保案例中心和搜索页能按制造业老板真实问题命中。
- 将 `.case-proof-rail` 改为自适应列布局，支持汽车案例 4 个证据项在桌面和手机端都稳定展示，不再依赖固定 3 列。
- 将全站静态资源版本更新为 `v=20260625-owner-resonance-v8`，刷新汽车案例、搜索索引、CSS 与 JS 缓存。
- 更新 `tests/static_check.py`，增加案例清单、案例中心、搜索页联动检查。
- 更新 `tests/interaction_check.py`，增加案例筛选、医疗搜索、案例 tab 等交互检查。
- 更新 `tests/interaction_check.py`，新增 DFMEA 搜索命中汽车案例的交互检查。
- 更新 `tests/interaction_check.py`，新增 `知识流失` 搜索命中汽车 DFMEA 案例的检查。
- 更新 `tests/static_check.py` 与 `tests/interaction_check.py`，增加 `search-index.json` 存在性、索引版本、案例目标覆盖、分类数量一致性和实时搜索交互检查。
- 更新 `tests/polished_pages_check.py`，覆盖全部 4 个案例详情页的桌面/手机视口，并新增手机端案例 H2 字号、行高比例和标题高度阈值检查。
- 更新 `tests/polished_pages_check.py`，覆盖首页、Playbook、案例中心、医疗案例和汽车 DFMEA 案例的桌面/手机视口、图片加载、控制台错误、导航交互、案例交互、上下滑动检查，并新增手机端案例目录不得横向滚动的断言。
- 新增本文件和 `docs/maintenance/site-governance.md`，把更新留痕和发布门禁纳入仓库维护流程。

### 验证

- `python3 build_site.py`
- `node --check script.js`
- `python3 -m json.tool search-index.json >/dev/null`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 python3 tests/interaction_check.py`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 python3 tests/polished_pages_check.py`
- in-app browser 复核：`case-automotive-dfmea-ontology-agent.html?qa=case-heading-v7-iab` 加载 `styles.css?v=20260625-case-heading-v7`，`#industry-pressure` H2 字号约 30.5px、行高约 36.6px、标题高度约 110px、`scroll-margin-top=110px`。
- in-app browser 复核：`case-automotive-dfmea-ontology-agent.html?qa=search-reading-v4` 与 `search.html?search=B柱` 均加载 `styles.css?v=20260625-search-reading-v4`、`script.js?v=20260625-search-reading-v4`。
- in-app browser 复核：`case-healthcare-agent-roi.html?qa=case-reading-v5-iab` 加载 `styles.css?v=20260625-case-reading-v5`，无横向溢出；`cases.html?qa=case-reading-v5-iab` 点选“医疗与高合规”后只展示 `healthcare-agent-roi`。
- in-app browser 复核：`index.html?qa=build-web-qa-v8` 加载 `styles.css?v=20260625-owner-resonance-v8` 与 `script.js?v=20260625-owner-resonance-v8`，首页无控制台错误、无横向溢出，桌面搜索弹层可打开且焦点进入输入框。
- in-app browser 复核：`case-automotive-dfmea-ontology-agent.html?qa=owner-resonance-v8` 首屏文案包含制造业老板、老师傅经验、供应商换线、ECO 和组织记忆断层，4 个证据项完整展示。
- in-app browser 复核：`search.html?search=知识流失&qa=owner-resonance-v8` 使用 JSON 索引 `20260625-owner-resonance-v8`，命中汽车 DFMEA 案例 1 条。

验证结果：

- 静态检查通过：16 个 HTML 页面、本地资源、案例清单与搜索联动均通过。
- 交互检查通过：桌面搜索弹层、手机菜单、Navigator、FAQ、案例筛选、医疗搜索与 DFMEA 搜索均通过。
- 强化搜索复核：`DFMEA`、`B柱`、`AgentCore` 命中汽车 DFMEA 案例，`P&ID` 命中制造业 P&ID 案例；`B柱` 查询显示 1 条案例结果和 2 处命中高亮。
- 视觉/滚动检查通过：首页、Playbook、案例中心、医疗案例、汽车 DFMEA 案例在桌面和手机端均无横向溢出、无坏图、无控制台错误；每页 `reachedBottom=true` 且 `returnedTop=true`。
- 医疗正文 diagram 中文化修正后复核：`healthcare-point-of-care-workflow-zh.png` 与 `healthcare-voice-agent-state-machine-zh.png` 在桌面和手机端均完整加载，手机端页面 `scrollWidth=390`、`innerWidth=390`。
- 汽车 DFMEA 案例加入后复核：`cases.html` 总案例卡 10 个；`search.html?search=DFMEA` 命中汽车案例 1 条。
- 案例详情页滑动修复后复核：医疗案例手机端 `.case-toc` 为 `position=static`、`overflowX=hidden`、`clientWidth=362`、`scrollWidth=362`；汽车 DFMEA 案例手机端同样为 `position=static`、`overflowX=hidden`、`clientWidth=362`、`scrollWidth=362`；两页均 `reachedBottom=true`、`returnedTop=true`、`scrollIntoViewCalls=[]`。
- v5 排版复核：医疗案例 in-app browser 首屏标题行距正常，`heroLineHeight=66.913px`、正文首个 H2 `lineHeight=56.25px`；案例中心 `healthcare` 筛选后可见案例为 1 个，标签为 `healthcare service data`。
- v6 搜索索引复核：`search-index.json` 生成 12 条索引，覆盖 `category` 1 条、`service` 4 条、`resource` 2 条、`case` 5 条；`search.html?search=RFLP` 通过 in-app browser 确认为 `searchSource=json-index`、`searchVersion=20260625-search-index-v6`，只显示汽车 DFMEA 案例且无横向溢出。
- v7 案例标题复核：四个案例详情页手机端均无横向溢出、无坏图、无控制台错误、可上下滑动到底并返回顶部；Wren 旧模板手机端 H2 为 32px / 1.18，新模板 P&ID、医疗、汽车案例手机端 H2 为 29.12px / 1.2，全部通过标题阈值检查。
- v8 Build Web Apps QA 复核：首页、搜索页、案例中心和 4 个案例详情页在桌面/手机端均通过自动化视觉与交互检查；汽车 DFMEA 手机端 4 个证据项堆叠高度正常，`scrollWidth=390`、`innerWidth=390`，上下滑动到底并返回顶部。
- v8 搜索复核：`search.html?search=知识流失` 通过 JSON 索引命中汽车 DFMEA 案例；`interaction_check.py` 输出 `DFMEA/B柱/AgentCore/知识流失/P&ID/RFLP 均命中`。

### 后续

- 每次新增案例时，先补 `case-*.html` 和图片，再更新 `CASE_LIBRARY_ITEMS`，最后记录在本文件。
- 每次新增一级页面、服务页或资源页时，优先更新 `SEARCH_CORE_ITEMS`，再运行 `python3 build_site.py` 生成 `search-index.json`。
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
