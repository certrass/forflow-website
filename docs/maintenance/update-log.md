# ForFlow 网站更新记录

这个文件用于记录每次网站更新后的维护事实。凡是改动页面、生成脚本、样式、图片、测试、部署配置或内容口径，都应在交付前追加一条记录。

记录规则：

- 新记录放在最上方，日期使用 `YYYY-MM-DD`。
- 每条记录至少包含 `变更范围`、`主要变更`、`验证`、`后续` 四段。
- `验证` 只写真实跑过的命令、人工检查或部署结果；没有跑就写“未跑”并说明原因。
- 涉及案例、服务页、一级页面时，同时说明对应的维护入口，例如 `build_site.py`、`templates/`、`CASE_LIBRARY_ITEMS` 或具体 HTML。

## 2026-06-25

### 变更范围

- 供应链案例详情页 `case-supply-chain-agentic-decision.html`、供应链正文架构图资源、生成脚本 `build_site.py`、样式 `styles.css`、搜索索引与维护记录。

### 主要变更

- 将用户提供的 AgentCore / Strands 多智能体供应链架构图作为正文证据图加入“架构设计：带语义层的主管-员工模式”章节，资源落到 `assets/cases/supply-chain-agentcore-architecture.png`，不替换 hero 场景图。
- 在 `build_site.py` 中为供应链案例新增 `case-figure--wide-diagram` figure，配套 alt、原图打开链接和说明文字，明确图中九个组件与左中右架构关系。
- 在 `styles.css` 新增宽 diagram 专用规则：桌面端完整收敛到正文宽度，手机端图片保持可读宽度并只在 figure 内部横向滚动，避免整页横向漂移。
- 将全站静态资源版本推进到 `v=20260625-supply-architecture-figure-v15`，刷新生成 HTML、CSS/JS 引用和 `search-index.json`。

### 验证

- `python3 build_site.py`
- `node --check script.js`
- `python3 -m json.tool search-index.json >/tmp/forflow-search-index-json-ok.json && echo json-ok`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- in-app Browser 复核：`case-supply-chain-agentic-decision.html?qa=supply-architecture-figure-v15#architecture` 加载 `styles.css?v=20260625-supply-architecture-figure-v15`，页面身份正确、正文 figure 存在、无 console error、当前窄视口下整页无横向溢出。
- 系统 Chrome 只读渲染复核：桌面 1440×1000 下架构图加载成功，图片自然尺寸 `1430×431`，页面 `docScroll=1440`；手机 390×844 下图片自然尺寸 `1430×431`，整页 `docScroll=390`，figure 内部 `clientWidth=386 / scrollWidth=653 / overflowX=auto`，符合图内横向查看预期。

### 后续

- 如果后续需要把这张英文原图中文化，应新增 `assets/cases/*-zh.png` 并替换正文 figure，保留原图作为结构参考；不要用泛化场景图替代正文 diagram。

## 2026-06-25

### 变更范围

- AI 场景诊断页 `navigator.html`、诊断结果页 `navigator-results.html`、全站页脚口径、生成脚本 `build_site.py`、交互脚本 `script.js`、样式 `styles.css`、静态/交互/视觉 QA 测试。

### 主要变更

- 将诊断页从“前端原型说明/占位槽”改为客户可见的正式诊断入口：侧栏改为 `诊断口径`，步骤标签改为中文诊断语境，行业和系统字段删除“占位”字样，推荐说明改为项目初筛与场景卡表达。
- 在 `build_site.py` 新增 `polish_navigator_page()`，并把全站页脚旧文案统一改为“企业 AI 场景工程 · 诊断、案例与交付路径持续更新”；同时在 `version_asset_links()` 清理历史 HTML 旧页脚，避免模板拷贝后回退。
- 优化问卷点击体验：左侧步骤支持键盘和鼠标回退修改，未完成的后续步骤会提示先完成当前步骤；下一步按钮禁用、状态提示、选中卡片、单选/多选 hover 与 focus 状态都更新为更正式的可用表单反馈。
- 结果页说明从“正式上线时可接方案库/CRM”改为“用来确定先做哪条工作流、需要哪些数据边界、谁负责复核与验收”；脚本生成的推荐卡 CTA 从 `DETAIL / CMS SLOT` 改为“进入评估清单”。
- 更新 `tests/static_check.py`，扫描所有 HTML 的客户可见文本，禁止 `原型说明`、`内容映射占位`、`DETAIL / CMS SLOT`、`响应式企业网站原型` 等占位文案回归。
- 更新 `tests/interaction_check.py`，新增 Navigator 初始禁用态、选择解锁、步骤回退修改、结果页无占位文案断言。
- 更新 `tests/polished_pages_check.py`，把 `navigator.html` 与带查询参数的 `navigator-results.html` 加入桌面/手机截图、上下滑动、横向溢出、缺图、console error 和占位文案巡检。
- 将全站静态资源版本推进到 `v=20260625-navigator-ux-v14`，刷新 HTML、CSS、JS 和 `search-index.json`。

### 验证

- `python3 build_site.py`
- `node --check script.js`
- `python3 -m json.tool search-index.json`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 PYTHONPATH=.python-deps python3 tests/interaction_check.py`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 PYTHONPATH=.python-deps python3 tests/polished_pages_check.py`
- 浏览器 QA 使用稳定本地服务 `http://127.0.0.1:8765` 与独立 Chrome CDP `9227`；`navigator-desktop`、`navigator-mobile`、`navigator-results-desktop`、`navigator-results-mobile` 均无横向溢出、无缺图、无 console error、无客户可见占位文案，上下滑动能到顶到底。

### 后续

- 后续如果把诊断结果接入真实方案库或 CRM，应继续沿用 `build_site.py` 的 Navigator 维护入口，并给交互测试补充真实提交/收藏/导出路径。

## 2026-06-25

### 变更范围

- 案例中心、搜索页、医疗案例详情页、汽车 DFMEA 案例详情页、案例视觉资源、生成脚本、静态检查、交互检查、视觉/滚动检查、维护文档。

### 主要变更

- 将案例详情目录间距修复推进到 `v=20260625-case-toc-gap-v13`，刷新全站生成页、搜索索引、CSS 与 JS 缓存。
- 将旧 Wren 案例的 Python 生成结构从单独 `.case-detail-shell` 改为共享 `.case-detail-shell.case-story-shell`，让旧页面和新版案例详情使用同一套移动端目录间距、滚动和回归检查。
- 将移动端 `.case-detail-shell` 的顶部间距从清零改为 `clamp(22px,7vw,34px)`，避免未来新增旧模板或未带新版 proof note 的案例详情再次出现目录标签贴边。
- 更新 `tests/static_check.py`，要求所有 `case-*.html` 案例详情页必须包含 `case-detail-page`、`.case-detail-shell.case-story-shell` 和目录 `data-scrollspy`。
- 更新 `tests/polished_pages_check.py`，新增 `caseTocSpacing` 度量；手机端案例目录距离案例壳顶部小于 20px 时直接失败。
- 将案例详情移动端目录间距修复推进到 `v=20260625-case-toc-gap-v12`，刷新全站生成页、搜索索引、CSS 与 JS 缓存。
- 确认“决策问题”等目录标签贴近上方色块不是供应链页个例，而是新版 `case-study-v2` 案例详情通用结构在手机端把 `.case-story-shell` 顶部间距清零导致；统一为新版案例详情补充移动端顶部缓冲，覆盖供应链、医疗、汽车 DFMEA 与 P&ID 案例，旧 Wren 模板不受影响。
- 将汽车 DFMEA 案例质量复核后推进到 `v=20260625-ontology-subhead-v11`，刷新全站生成页、搜索索引、CSS 与 JS 缓存。
- 将汽车案例中“本体编码的是关系”从普通小标题调整为独立关系卡片 `case-subhead--relation`，增加上下间距、绿色浅底、边框和移动端专用行高，解决该小标题与上下段落粘连的问题。
- 在汽车案例本体章节补充“企业主应该先看什么”段落，明确小范围本体化试点前应先盘点历史 DFMEA / ECO、材料与工艺窗口、试验/仿真/保修证据、供应商变更和现场质量反馈，让文章更容易被制造业老板理解和判断。
- 新增 `case-subhead--relation` 桌面与移动端样式，避免关系卡片在手机端撑宽页面。
- 将供应链案例二次质检后推进到 `v=20260625-supply-quality-v10`，补回原文中被压薄的技术细节，刷新全站生成页、搜索索引、CSS 与 JS 缓存。
- 供应链案例正文补充“从一名分析师加半天时间”到“一句话加 30 秒”的决策成本变化，并明确“从看数据到查数据、从被动展示到主动推理”的控制塔升级逻辑。
- 供应链架构章节补充分层说明：用户接入层、智能体核心层、数据访问与网关层、可观测性层；恢复 AgentCore Identity、Outbound Auth、Client Credentials、API 目标、Lambda 目标和 AgentCore Observability 等工程细节。
- 供应链语义层章节补回精确计算口径示例：`COUNT(status='delivered') / COUNT(*)`，并强调查询代理可分析 SQL 错误并自动重试。
- 新增 `.case-layer-notes` 与案例正文 `code` 样式，保证新增架构分层说明在桌面与手机端均可读、不撑宽页面。
- 将本轮内容版本推进到 `v=20260625-case-quality-v9`，刷新全站生成页、案例中心、搜索页、CSS 与 JS 缓存。
- 新增供应链多智能体案例 `case-supply-chain-agentic-decision.html`，保留用户提供的完整技术叙事骨架，并补齐企业主可读的业务问题、控制塔局限、主管-员工多智能体架构、语义层、MCP 解耦、渠道履行分析链路和落地起步方式。
- 调用 imagegen 生成供应链案例 hero 图 `assets/cases/supply-chain-agentic-decision-hero.png`，画面保持中国零售/供应链运营场景、无可读文字、无英文 UI，避免把正文技术 diagram 误替换成泛化场景图。
- 将供应链案例加入 `CASE_LIBRARY_ITEMS`、`cases.html`、`search.html` 和 `search-index.json`，新增 `供应链` 搜索入口，确保案例卡片、分类、JSON 搜索和关键词命中联动。
- 更新旧模板 `case-wren-kitchens.html`：从“案例详情示范”改成客户可见的 Wren Kitchens 案例表达，补强增长压力、交接窗口、长期合作和知识交接语境，并纳入新版案例详情页行距与手机端 QA。
- 删除汽车 DFMEA 案例中不适合客户展示的内部说明句“结合用户提供的原文结构，并补充查阅公开资料……”，改为客户可见的“公开资料适合用于理解基础概念，真正落地以企业自身数据为准”的参考资料说明。
- 继续强化汽车 DFMEA 案例的制造业老板共鸣点：首屏和正文保留“知识流失、老师傅经验断档、组织记忆、ECO 复评、供应商换线、历史项目迁移”等表达，同时不删减 B 柱、22MnB5、DFMEA、本体、RFLP、多智能体和 AgentCore / Strands 技术细节。
- 修复“本体编码的是关系”等案例小标题间距：统一 `.case-subhead` 的上下间距、中文小标题行高、技术词换行和移动端标题比例，避免小标题贴得过紧或在手机端挤成一团。
- 统一旧案例与新案例的中文阅读标准：放宽 `.case-detail-hero h1`、`.case-section h2`、段落、列表、quote、legacy 模板正文和移动端 H2 行高，解决旧页面没有随新版模板一起修复的行距问题。
- 新增供应链案例专用的对比表、架构组件栅格、指标条和响应式布局规则；手机端强制单列/横向表格安全区，保证上下滑动不会被横向溢出干扰。
- 更新 `tests/static_check.py`、`tests/interaction_check.py`、`tests/polished_pages_check.py`，把供应链案例、Wren 旧模板、搜索页 JSON 索引、案例行距、桌面/手机滚动、截图和交互检查全部纳入回归。
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

- in-app Browser 复核：`case-automotive-dfmea-ontology-agent.html?qa=toc-gap-v13#overview` 加载 `styles.css?v=20260625-case-toc-gap-v13`，手机视口下目录壳为 `container case-detail-shell case-story-shell`，目录间距约 29.67px，无横向溢出，无 console 错误。
- in-app Browser 复核：`case-wren-kitchens.html`、`case-supply-chain-agentic-decision.html`、`case-healthcare-agent-roi.html`、`case-manufacturing-pid-intelligence.html` 均加载 v13，手机视口下目录间距约 29.67px，旧 Wren 也已使用共享壳。
- `python3 build_site.py`
- `node --check script.js`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `python3 -m json.tool search-index.json`
- `python3 -c "import json; idx=json.load(open('search-index.json')); print(idx.get('version'), len(idx.get('items', [])))"`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 PYTHONPATH=.python-deps python3 tests/polished_pages_check.py`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `node --check script.js`
- `python3 -m json.tool search-index.json`
- `python3 -c "import json; idx=json.load(open('search-index.json')); print(idx.get('version'), len(idx.get('items', [])))"`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 PYTHONPATH=.python-deps python3 tests/polished_pages_check.py`
- 浏览器截图复核：`tests/polished/supply-chain-case-mobile-toc-gap-v12.png` 显示供应链案例手机端目录标签与上方说明块之间已有清楚白场缓冲；临时 Chrome CDP 端口 `9227` 已关闭。
- `python3 build_site.py`
- `node --check script.js`
- `python3 -m json.tool search-index.json >/dev/null`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 python3 tests/interaction_check.py`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 python3 tests/polished_pages_check.py`
- `python3 -c "import ast, pathlib; [ast.parse(p.read_text()) for p in pathlib.Path('tests').glob('*.py')]"`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 PYTHONPATH=.python-deps python3 tests/interaction_check.py`
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9227 PYTHONPATH=.python-deps python3 tests/polished_pages_check.py`
- `rg -n "COUNT\\(status='delivered'\\)|Client Credentials|Outbound Auth|AgentCore Identity|自我纠错|自动重试|一名分析师加半天|从“看数据”到“查数据”|实际运营数据做匿名化" case-supply-chain-agentic-decision.html search-index.json`
- `rg -n "case-subhead--relation|企业主应该先看什么|20260625-ontology-subhead-v11|本体试点不必一开始覆盖整车" build_site.py case-automotive-dfmea-ontology-agent.html styles.css search-index.json`
- in-app Browser 复核：`case-automotive-dfmea-ontology-agent.html?qa=ontology-subhead-v11#ontology` 加载 `styles.css?v=20260625-ontology-subhead-v11` 与 `script.js?v=20260625-ontology-subhead-v11`，关系卡片存在、企业主段落存在、无页面控制台错误。
- in-app Browser 复核：汽车案例手机宽度下关系卡片和企业主段落均未撑宽页面，`scrollWidth` 与 `innerWidth` 一致。
- in-app Browser 复核：`case-supply-chain-agentic-decision.html?qa=supply-quality-v10` 加载 `styles.css?v=20260625-supply-quality-v10` 与 `script.js?v=20260625-supply-quality-v10`，正文命中 `COUNT(status='delivered') / COUNT(*)`、Client Credentials、Outbound Auth、自动重试和 3 个架构分层说明。
- in-app Browser 复核：`search.html?search=供应链&qa=supply-quality-v10` 使用 JSON 索引 `20260625-supply-quality-v10`，供应链案例可见且点击可进入详情页。
- in-app Browser 复核：`case-supply-chain-agentic-decision.html?qa=v9-browser` 页面身份、首屏、hero 图、9 个架构组件、4 个指标项、控制台和横向溢出。
- in-app Browser 复核：`case-wren-kitchens.html?qa=v9-browser` 旧模板已加载 `case-study-legacy`，H1/H2 行距正常，桌面端无横向溢出。
- in-app Browser 复核：`case-automotive-dfmea-ontology-agent.html?qa=v9-browser` 不再包含内部说明句，参考资料段落为客户可见版本，“本体编码的是关系”等小标题行距正常。
- in-app Browser 复核：`search.html?search=供应链&qa=v9-browser` 使用 JSON 索引 `20260625-case-quality-v9` 命中供应链案例。
- in-app browser 复核：`case-automotive-dfmea-ontology-agent.html?qa=case-heading-v7-iab` 加载 `styles.css?v=20260625-case-heading-v7`，`#industry-pressure` H2 字号约 30.5px、行高约 36.6px、标题高度约 110px、`scroll-margin-top=110px`。
- in-app browser 复核：`case-automotive-dfmea-ontology-agent.html?qa=search-reading-v4` 与 `search.html?search=B柱` 均加载 `styles.css?v=20260625-search-reading-v4`、`script.js?v=20260625-search-reading-v4`。
- in-app browser 复核：`case-healthcare-agent-roi.html?qa=case-reading-v5-iab` 加载 `styles.css?v=20260625-case-reading-v5`，无横向溢出；`cases.html?qa=case-reading-v5-iab` 点选“医疗与高合规”后只展示 `healthcare-agent-roi`。
- in-app browser 复核：`index.html?qa=build-web-qa-v8` 加载 `styles.css?v=20260625-owner-resonance-v8` 与 `script.js?v=20260625-owner-resonance-v8`，首页无控制台错误、无横向溢出，桌面搜索弹层可打开且焦点进入输入框。
- in-app browser 复核：`case-automotive-dfmea-ontology-agent.html?qa=owner-resonance-v8` 首屏文案包含制造业老板、老师傅经验、供应商换线、ECO 和组织记忆断层，4 个证据项完整展示。
- in-app browser 复核：`search.html?search=知识流失&qa=owner-resonance-v8` 使用 JSON 索引 `20260625-owner-resonance-v8`，命中汽车 DFMEA 案例 1 条。

验证结果：

- v13 静态检查通过：17 个 HTML 页面、本地资源、案例详情共享壳、目录 scrollspy 和案例搜索联动均通过；`search-index.json` 版本为 `20260625-case-toc-gap-v13`，索引 13 条。
- v13 in-app Browser 检查通过：汽车、Wren、供应链、医疗、P&ID 五个案例详情页手机视口均加载 v13，目录间距约 29.67px，`scrollWidth` 与 `innerWidth` 一致，无相关 console 错误。
- v13 视觉/滚动回归通过：首页、Playbook、案例中心、Wren、P&ID、医疗、汽车、供应链案例在桌面与手机端均无横向溢出、无坏图、无控制台错误；五个案例详情手机端 `caseTocSpacing.topGap=27.3px`，上下滑动可到底并回顶，`scrollIntoViewCalls=[]`。
- v12 静态检查通过：17 个 HTML 页面、本地资源和案例搜索联动均通过；`search-index.json` 版本为 `20260625-case-toc-gap-v12`，索引 13 条。
- v12 视觉/滚动回归通过：首页、Playbook、案例中心、Wren、P&ID、医疗、汽车、供应链案例在桌面与手机端均无横向溢出、无坏图、无控制台错误；新版案例手机端目录 `scrollWidth=362`、`clientWidth=362`，上下滑动可到底并回顶，`scrollIntoViewCalls=[]`。
- v12 供应链手机目录截图通过：`决策问题 / 控制塔瓶颈 / 架构设计 / 关键设计 / 履行分析 / 企业落地 / 技术背景` 标签行与上方色块之间不再贴边。
- v11 静态检查通过：17 个 HTML 页面、本地资源和案例搜索联动均通过；汽车 DFMEA 案例中文正文约 6026 字。
- v11 搜索索引通过：`search-index.json` 版本为 `20260625-ontology-subhead-v11`，索引 13 条。
- v11 in-app Browser 检查通过：汽车 DFMEA 本体章节的关系卡片上方约 34px、下方约 26px，独立卡片样式生效；新增“企业主应该先看什么”段落命中；无页面控制台错误。
- v11 视觉/滚动回归通过：首页、Playbook、案例中心、Wren、P&ID、医疗、汽车、供应链案例在桌面与手机端均无横向溢出、无坏图、无控制台错误；汽车手机端 `scrollWidth=390`、`innerWidth=390`，`reachedBottom=true` 且 `returnedTop=true`。
- v10 静态检查通过：17 个 HTML 页面、本地资源和案例搜索联动均通过；供应链案例中文正文约 4147 字。
- v10 搜索索引通过：`search-index.json` 版本为 `20260625-supply-quality-v10`，索引 13 条，包含 `supply-chain-agentic-decision`。
- v10 in-app Browser 检查通过：供应链详情页首屏非空、hero 图加载、无页面控制台错误、无横向溢出；补回的 SQL 公式、Client Credentials、Outbound Auth、自动重试等细节均在页面中命中。
- v10 搜索交互通过：`search.html?search=供应链` 使用 JSON 索引，供应链案例可见，点击结果进入 `case-supply-chain-agentic-decision.html`，详情页仍保留 SQL 公式。
- v10 交互回归通过：搜索、手机菜单、Navigator、FAQ、案例筛选、医疗搜索、供应链搜索、DFMEA/B柱/AgentCore/知识流失/P&ID/RFLP 均命中。
- v10 视觉/滚动回归通过：首页、Playbook、案例中心、Wren、P&ID、医疗、汽车、供应链案例在桌面与手机端均无横向溢出、无坏图、无控制台错误；供应链手机端 `scrollWidth=390`、`innerWidth=390`，`reachedBottom=true` 且 `returnedTop=true`。
- v9 静态检查通过：17 个 HTML 页面、本地资源、案例清单、供应链新案例、Wren 旧模板和搜索联动均通过。
- v9 语法检查通过：`script.js` 通过 `node --check`，测试脚本通过 AST 语法检查；`py_compile` 因沙盒无法写入默认缓存目录，改用无副作用 AST 检查。
- v9 in-app Browser 检查通过：供应链案例首屏非空、hero 图加载、9 个架构组件和 4 个指标项完整；Wren 旧模板行距正常；汽车案例内部说明句已移除；搜索页通过 JSON 索引命中供应链案例。
- v9 交互检查通过：桌面搜索弹层、手机菜单、Navigator、FAQ、案例筛选、医疗搜索、供应链搜索、DFMEA/B柱/AgentCore/知识流失/P&ID/RFLP 均命中。
- v9 视觉/滚动检查通过：首页、Playbook、案例中心、Wren、P&ID、医疗、汽车、供应链案例在桌面和手机端均无横向溢出、无坏图、无控制台错误；每页 `reachedBottom=true` 且 `returnedTop=true`。
- v9 Wren 手机端复核：`.case-detail-shell` 在手机端不再保持桌面两列宽度，`scrollWidth=390`、`innerWidth=390`，H2 行高比例约 1.24。
- v9 供应链案例复核：手机端 `scrollWidth=390`、`innerWidth=390`，架构组件、指标条和表格响应式正常，页面可上下滑动到底并返回顶部。
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
