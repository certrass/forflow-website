# ForFlow 网站更新记录

这个文件用于记录每次网站更新后的维护事实。凡是改动页面、生成脚本、样式、图片、测试、部署配置或内容口径，都应在交付前追加一条记录。

记录规则：

- 新记录放在最上方，日期使用 `YYYY-MM-DD`。
- 每条记录至少包含 `变更范围`、`主要变更`、`验证`、`后续` 四段。
- `验证` 只写真实跑过的命令、人工检查或部署结果；没有跑就写“未跑”并说明原因。
- 涉及案例、服务页、一级页面时，同时说明对应的维护入口，例如 `build_site.py`、`templates/`、`CASE_LIBRARY_ITEMS` 或具体 HTML。

## 2026-10-26 · 数据资产合作页正式发布

### 变更范围

- 当前根数据伙伴页 `output/afterquery-data-zh/`；新增 `package.py`、全站打包接入 `scripts/build_public.py`，回执与复现脚本在 `docs/maintenance/releases/data-20261026/`。

### 主要变更

- 按用户「部署上线」授权发布至 https://forflow.ai/company/data/ 。采用最新线上快照添加 35 个本页运行文件，未发布本地旧的全站或嵌套研究实验页。公开 HTML 添加 canonical 和 index/follow；本地仍为 noindex。
- 正式部署 `6adf4e420116de1e107d68df`，先经 draft `6adf4dd9f37c52372bf84c6b` 验证，再发布同一 payload。已有 193 个文件、5 个函数及配置、门禁 edge bundle/manifest 摘要全部保持。

### 验证

- 独立生成、打包、后续全站打包接入通过；35 个运行文件与部署包相同，维护回执不进入公开目录。Draft 和 production 的 35 个资源以及 16 条路由通过 HTTP 回读；自有域名 HTML 除 Cloudflare 追加的检测脚本外字节一致。
- 自有域名直连部分超时，经现有代理完成检查。远端内置浏览器导航超时，交互与视觉仅按前述本地桌面/手机实测记录。根静态检查仍有发布范围外工作台三项既有结构缺失。
- 线上未连接 Git 自动部署；源码、必要资产及发布回执同步到既有私有 GitHub 仓库，不改主工作目录中的并行内容。

### 后续

- 正式链接与本地 8899 预览保持可用。合作按钮复用现有飞书通用咨询表单，未创建专用问卷或测试提交。

## 2026-10-26 · 数据资产合作页整页文案、入口与 Logo 收敛

### 变更范围

- 当前根数据伙伴页 `output/afterquery-data-zh/`，维护入口为 `source/zh.json`、新增 `source/faq.json` / `source/site.json`、`build.py` 与 `styles.css`。Company / Data 页内容未改。

### 主要变更

- 按用户最新完整定稿统一首屏、价值主张、九个行业、六步流程及行动号召；法律段依据核心纠错去除「特权」，改为执业保密、涉密材料与未公开底稿边界。八个问答重新围绕企业授权、样本评估、访问范围、隐私和结算组织。
- 清除活动页面中的 AfterQuery、旧机翻用语、申请和条款链接；四个主按钮和页脚合作入口复用现有 ForFlow 飞书通用咨询表单。地址来自主工作目录模板，只读定位，没有修改该工作区。
- 导航 Logo 改为桌面 108px / 手机 96px；长 CTA 改为自适应高度，手机标题适配新字数。来源捕获、素材来源及早期截图保留为历史。

### 验证

- 独立生成、残留扫描、八问答/六流程/四 CTA、本地资源、锚点、重复 ID、外链安全属性、JS 语法与差异空白检查通过。
- 实际浏览器验证 1440 × 1000、390 × 844 和 320px 窄屏，无横向溢出；菜单开关、Esc、更多问答及脱敏问答开关通过，控制台无 error / warn。最终截图与版本哈希保存在 `evidence/localized-*.png` 和 `localization-verification.json`。
- 飞书入口 HTTP 200；在线浏览器读取超时，未测试提交。根目录静态检查仍为既有 `workbench_prototype.html` 的三项结构缺失。

### 后续

- 本地预览保持运行，未发布。现有通用咨询表单尚非专用数据评估/引荐问卷，日后替换入口统一修改 `source/site.json`。

## 2026-10-26 · 数据伙伴页首屏标题更新

### 变更范围

- 独立数据伙伴页的 `output/afterquery-data-zh/build.py` 与 `source/zh.json`，重新生成 `index.html`。

### 主要变更

- 按用户文案将标题改为「真实业务数据，审慎合规授权」，保持两个分句各占一行。

### 验证

- 生成、标题逐字一致与两行结构检查通过；内置浏览器回读新标题，无页面横向溢出；差异空白检查通过。

### 后续

- 本地预览已更新，未发布远端。

## 2026-10-26 · 推荐奖励改为 50 万人民币

### 变更范围

- 独立数据伙伴页 `output/afterquery-data-zh/`，维护入口为 `source/zh.json`，由 `build.py` 生成。

### 主要变更

- 按用户指定，将首屏与底部推荐入口的「最高可赚取 8.5 万美元」同步改为「最高可赚取 50 万人民币」。外部链接未改。

### 验证

- 生成通过；两处金额断言与正文旧金额扫描通过，内置浏览器刷新回读两处均为 50 万人民币，无页面横向溢出；差异空白检查通过。

### 后续

- 本地预览已更新，未发布远端。

## 2026-10-26 · 数据伙伴页首屏文案与行业原创配图

### 变更范围

- 用户明确本轮对象为 `http://127.0.0.1:8899/` 与 `#industries`。维护入口为 `output/afterquery-data-zh/source/zh.json`、`build.py`、`styles.css` 和 `source/generated-images.json`。

### 主要变更

- 首屏介绍逐字替换为用户提供的 ForFlow 历史作业留痕、脱敏审计、评测与训练资产及授权商业化流转文案。
- 内置 image_gen 生成办公室与专家核对两张虚构工作场景，保存 PNG 原图与 JPG 网页副本。行业区使用办公室图替换原站照片，手机焦点设为 `50% 35%`。
- 用户纠正页面对象后撤回专家近景在 Company / Data 的接入，恢复该页原有资料图形；专家近景保留为未使用备选。其他原计划条款、按钮与外链本轮没有重写。

### 验证

- 独立生成、首屏原文逐字一致、图片文件及引用、Company / Data 恢复与模板一致性、JS 语法及差异空白检查通过。
- 内置浏览器核对根页 1440 × 1000 / 390 × 844 首屏与行业区，图片正常加载，无页面横向溢出；桌面窄幅及手机裁切已查看。截图位于 `output/afterquery-data-zh/evidence/`，提示词与素材哈希在生成清单中。
- 根目录静态检查仍报告既有 `workbench_prototype.html` 三项结构缺失，未修改无关页面。

### 后续

- 本地服务继续运行；本轮没有发布。Company / Data 的照片截图为已撤回中间版本，当前有效证据为 `forflow-data-copy-*.png` 与 `industries-generated-*.png`。

## 2026-10-26 · Company / Data 本地页与导航标识比例

### 变更范围

- `output/afterquery-data-zh/` 独立预览。新增维护入口 `source/company-data.html`、`company-data.css`、`company-data.js`，由该目录 `build.py` 生成 `company/data/index.html`；原页只调整导航标识尺寸。

### 主要变更

- 按用户确认的 `/company/data` 路径新增数据研究与合作页，逐字保留数据质量主张，衔接专家协作、严谨整理、领域知识及合作沟通。
- 新页沿用 ForFlow 黑白与绿色设计，使用已有品牌与字体；不包含 AfterQuery 的奖金及商务承诺。原页导航标识改为桌面 144px / 手机 132px，新页同尺寸。

### 验证

- 独立生成、原文和来源一致性、本地资源、ID、锚点、JavaScript 语法及差异空白检查通过。
- 内置浏览器实测新页 1440 × 1000、390 × 844 无横向溢出，图像正常；菜单开关、Esc 焦点返回与合作章节定位通过，控制台无 error / warn。原页桌面标识实测 144px、手机断点实测 132px。
- 已打开桌面全页与手机截图复核，保存在 `output/afterquery-data-zh/evidence/company-data-*.png`；原页新标识截图为 `forflow-logo-refined.png`。
- 根目录 `tests/static_check.py` 仍报告既有 `workbench_prototype.html` 的三项结构缺失；本轮未修改该文件或正式页生成来源。

### 后续

- 本地入口 `http://127.0.0.1:8899/company/data/`，已有服务保持运行；尚未挂载或发布到正式域名。主工作目录的 `/company` 包装脚本只作来源定位，未修改或同步其他工作区。

## 2026-10-26 · 数据伙伴计划独立预览与 ForFlow 设计系统

### 变更范围

- 新增 `output/afterquery-data-zh/` 独立静态预览，生成入口为该目录的 `build.py`、`source/reference.html` 与 `source/zh.json`。正式站点及根目录生成清单未改。

### 主要变更

- 按用户给定的 AfterQuery 数据伙伴计划复刻内容结构，再按后续要求换为现有 ForFlow 黑白 / Flow Green、无衬线标题、品牌标识、圆角卡片与细边框。
- 原站照片、行业图标、字体与画布模块本地化；导航、九个行业、六步流程、问答展开和更多问题可用。手机菜单改为浮层，行业区域支持键盘横向浏览。
- 原计划的 AfterQuery 主体、8.5 万美元金额和申请/推荐地址保留，页脚保留来源；没有把它们改写为 ForFlow 商务承诺，没有收集或提交业务数据。

### 验证

- 独立页面生成、JavaScript 语法、本地资源、锚点、重复 ID、外部链接安全属性检查通过。
- 内置浏览器实测 1440 × 1000、390 × 844 和 440 像素宽布局，无页面级横向溢出；菜单展开/收起、Esc 与焦点返回、章节跳转、行业键盘横向滚动、问答和更多问题通过。减弱动效模式已运行，本页控制台无 error / warn。
- 已打开桌面全页和桌面/手机原站对照图复核。截图和版本记录位于 `output/afterquery-data-zh/evidence/`，验收记录为 `design-qa.md`。
- 根目录 `tests/static_check.py` 仍有既有 `workbench_prototype.html` 的 stylesheet、search modal 和 body 直接子级 footer 三项缺失，未修改该无关文件。没有全站重建或部署。

### 后续

- `http://127.0.0.1:8899/` 本地服务保持运行供审阅。真实触摸手势和 iOS Safari 实机未测；正式对外使用前另行确定实际主体、条款、素材许可及申请接收方。

## 2026-07-12 · 企业 Agent 服务页视觉系统试点（v28）

### 变更范围

- `service-agent-build.html` 作为唯一服务详情页试点；维护入口为 `build_site.py`、`visual-system.css` 与 `tests/service_page_pilot_check.py`，其余四项服务保持现状。

### 主要变更

- 新增独立的 `visual-system.css` 层，收敛标题尺寸、圆角、卡片密度、英文提示词和绿色行动按钮；整页只保留“验证结果”一个黑底高权重段落。
- 使用单独生成的高调编辑摄影说明真实工作场景，技术图说明任务、系统、审批、评估与生产反馈路径；不再使用旧赛博图、摆拍多屏办公室图和文字密集汇报图。
- 重写首屏、结果、范围、过程、交付与咨询文案，直接说明启动条件、两周验证要回答的问题和继续、调整或停止的判断依据。
- 静态资源版本更新为 `20260712-service-visual-pilot-v28`；生成资源位于 `assets/service-agent/`。

### 验证

- `service_page_pilot_check.py` 先在缺少试点标记时失败，再在旧文案未替换时失败；完成结构、资源、文案和高亮预算后通过。
- `python3 build_site.py`、`python3 tests/static_check.py`、`python3 tests/public_build_check.py`、`node --check script.js`、`node tests/invite_gate_check.js`、`node tests/gate_runtime_check.mjs`、`node tests/data_foundation_check.mjs`、Python 语法检查与 `git diff --check` 通过。
- 在约 `1279 × 800` 和 `390 × 844` 视口检查首屏、主视觉、黑底结果段、技术图和 FAQ；正文无横向溢出，手机端 H1 为约 47px，FAQ 展开状态实测为 `aria-expanded=true`。
- 将 Sana 官方领导力页面的高调人物摄影与试点首屏放在同一对照画面复核；保留其克制、自然光和留白原则，不复刻人物、构图或页面结构。

### 后续

- 先由用户确认该代表页，再把同一视觉预算和内容层级推广到其余企业服务页；本轮不部署生产。

## 2026-07-12 · 整站动效层级与可读性审计（v27）

### 变更范围

- 首页、五个企业服务首屏、场景诊断、案例库、HR 场景地图、联系页，以及全站通用 `data-reveal` 入场规则。

### 主要变更

- 将全站入场位移从 22px 收敛为 12px，缩短持续时间，并按同一容器内的阅读顺序设置轻微错峰，不再按整页索引循环延迟。
- 首页流程线和节点在主视觉进入后才开始运动；循环速度放慢。服务页轨道呼吸幅度和速度同步收敛。
- 场景诊断步骤改为“面板—标题—内容”三层进入，保留步骤切换后聚焦新标题的键盘和读屏路径；HR 场景切换统一使用相同缓动节奏。
- 压缩桌面首页、服务详情和案例库首屏：主要行动、关键事实和下一段内容更早出现；企业服务标题在桌面保持完整一行。
- 联系页双栏改为顶部对齐，解决表单较长时左侧标题被推到首屏之外的问题；桌面和手机标题均控制为两行，避免“了。”单独成行。
- HR 手机标签增加横向吸附和隐藏滚动条，保留最后一个标签的露出提示；场景诊断手机工作区增加底部安全空间，避免粘性行动栏遮住最后一项内容。
- 静态资源版本更新为 `20260712-motion-readability-v27`。

### 验证

- 当前状态截图覆盖首页、企业 Agent 服务、案例库、HR 场景地图、联系页，以及诊断步骤 1、选择后状态和步骤 2；每张截图保存后均重新打开检查。
- 桌面复核视口约 `1391 × 869`：首页 CTA 底部位于 655px，服务页 CTA / 事实栏 / 本页导航均在 712px 内；案例首卡顶部从约 810px 提前到 729px；企业 Agent 标题从两行异常断字改为单行。
- 手机复核视口约 `473 × 811`：案例首卡顶部从约 733px 提前到 577px；联系卡片顶部从约 673px 提前到 385px，标题由三行改为两行；首页、HR 与诊断页无正文横向溢出。
- 场景诊断实测选择业务挑战后按钮启用，进入步骤 2 后标题获得焦点；面板、标题和内容的动画延迟分别为 `0s`、`0s` 和 `0.055s`。HR 标签切换后选中态、焦点和面板标题同步更新。
- 逐页扫描 25 个 HTML 的手机标题换行和桌面横向溢出；联系页孤行已修复，其余三行案例标题均为长标题的正常分组，没有单字孤行。
- `python3 build_site.py`、`node --check script.js`、`python3 tests/static_check.py`、`python3 tests/public_build_check.py`、`node tests/invite_gate_check.js`、`node tests/gate_runtime_check.mjs` 与 `git diff --check` 通过；代表页面控制台无站点警告或错误。

### 后续

- 本轮没有宣称完整 WCAG 合规；正式发布前继续保留 `prefers-reduced-motion` 规则，并在生产门禁后的真实网络环境观察首屏图片加载与长页面滚动表现。

## 2026-07-11 · 新版页面生产部署（v26）

### 变更范围

- 将当前首页、企业服务、场景诊断、案例、博客与联系等公开页面发布到 Netlify 生产站点 `forflow.ai`，保留受邀访问门禁。

### 主要变更

- 生产公开包使用静态资源版本 `20260711-data-foundation-v26`。
- 新增构建开关 `WEBSITE_DATA_ENABLED`：未显式启用时，公开包移除联系留资和诊断报告邮箱表单，避免 Supabase / Resend 尚未配置时出现不可用入口。
- 联系页在数据功能关闭时保留 `hello@forflow.ai` 邮件入口；诊断、联系和数据 API 的完整界面留待生产数据环境接通后启用。
- deploy preview ID：`6a5268c0996b9c079c31f5e2`；production deploy ID：`6a526ad3f3353819365b175e`。

### 验证

- `python3 build_site.py`、`node --check script.js`、`python3 tests/static_check.py`、`python3 tests/public_build_check.py`、`node tests/invite_gate_check.js`、`node tests/gate_runtime_check.mjs` 与 `git diff --check` 通过。
- `netlify build` 完成 25 个页面、五个 Functions 与 `auth-gate` Edge Function 打包。
- deploy preview 未登录访问首页返回 `302` 到门禁页，门禁页返回 `200`，资源版本为 `20260711-data-foundation-v26`。
- 生产域名 `https://forflow.ai/` 未登录返回 `302` 到门禁页，门禁页和新版 CSS 返回 `200`；CSP、`noindex`、私有缓存控制等安全响应头生效。

### 后续

- 完成 Supabase、Resend 和生产环境变量配置与真实写入验证后，再设置 `WEBSITE_DATA_ENABLED=true` 并重新部署；启用前保持当前邮件兜底。

## 2026-07-11 · 官网数据基础与留资链路

### 变更范围

- 场景诊断、诊断结果、联系页、隐私说明、Netlify Functions、Supabase 迁移、Cloudflare Web Analytics 条件注入与公开构建。

### 主要变更

- 新增 `/api/events`、`/api/assessments`、`/api/leads` 三个服务端入口；事件只接受十个固定名称和有限属性，诊断答案与联系信息分表保存。
- 新增 `website_events`、`assessments`、`assessment_answers`、`leads`、`consent_records`，全表启用 RLS，浏览器角色无读写权限。
- 诊断完成后只把 `assessment_id` 放入结果 URL，不再把回答复制到查询参数；结果页增加可选邮箱报告，联系页改为真实留资表单并保留 `hello@forflow.ai` 兜底。
- 留资使用 `submission_id` 幂等写入；数据库写入与邮件通知解耦，Resend 未配置时仍可安全保存线索。
- 新增 `privacy.html`，说明数据类型、用途、服务提供方、默认保留目标和用户选择。
- 公开构建仅在设置 `CLOUDFLARE_WEB_ANALYTICS_TOKEN` 时注入 Cloudflare beacon，并同步放行所需 CSP 域名。
- 静态资源版本更新为 `20260711-data-foundation-v26`。

### 验证

- `node tests/data_foundation_check.mjs` 通过：未知事件、跨站写入、邮箱串表、查询字符串、幂等键、RLS 与 secret header 规则均符合预期。
- `python3 tests/static_check.py`、`python3 tests/public_build_check.py`、`node tests/invite_gate_check.js`、`node tests/gate_runtime_check.mjs` 通过。
- `npx --yes netlify-cli build` 完成公开构建、五个 Functions 和 Edge Function 打包。
- in-app Browser 检查诊断结果排序、桌面报告表单以及 424px 联系表单；修复手机端姓名和邮箱输入被挤在同一行的问题，复测后单列宽度 339px、无横向溢出、控制台无警告或错误。
- 旧 `tests/interaction_check.py` 未完成，因为其固定依赖的本地 CDP 端口 `9226` 当前未启动；已用 in-app Browser 覆盖本轮渲染与交互路径。

### 后续

- 当前没有 Supabase 生产项目密钥、已验证的 Resend 发件地址或 Cloudflare Web Analytics token，因此本轮不部署真实写入链路。
- 配置正式环境后，按 `docs/maintenance/data-foundation.md` 的顺序应用迁移、运行 linked lint、部署 preview，并用真实测试线索核对数据隔离和邮件送达。

## 2026-07-11 · 核心页面文案清晰度

### 变更范围

- 首页、场景诊断、诊断结果、准备度审核、四个企业服务页、HR 场景地图与案例库入口。

### 主要变更

- 拆开同时承载多个概念的长句，减少“边界、证据、复评、投入”连续堆叠，让客户先读懂问题和下一步。
- 首页首屏改为“判断值不值得做—确认数据和审批—小范围看结果”的自然表述；服务入口直接说明什么时候做准备度审核，什么时候进入具体服务。
- 场景诊断说明改为项目初筛口径；结果页把三种排序方式分别解释清楚。
- 准备度审核页将六维度、交付材料、证据说明和最终行动入口改成管理层可直接理解的句子。
- 四个服务页统一改写适用性提示、经验说明和相关路径标题；HR 与案例入口进一步解释人工接管和证据来源。
- 静态资源版本更新为 `20260711-copy-clarity-v24`。

### 验证

- `python3 build_site.py`、`python3 tests/static_check.py`、`python3 tests/public_build_check.py`、门禁静态与运行检查、JavaScript / Python 语法检查以及 `git diff --check` 全部通过。
- 1440px 复核首页与准备度审核首屏，标题、正文、按钮和事实栏没有出现挤压或异常换行。

### 后续

- 下一轮继续处理长案例详情中的术语密度和段落节奏，保留来源、样本、数字和证据边界。

## 2026-07-11 · 生产部署

### 变更范围

- 将 `20260711-final-flow-v23` 公开构建部署到 Netlify 生产站点 `forflow.ai`，同步发布 Edge 门禁、登录函数与仅含公开文件的 `dist/`。

### 主要变更

- 生成并配置新的 `SITE_GATE_PASSWORD`，仅用于 `production` 与 `deploy-preview`，并标记为 Netlify secret；旧访问码继续由登录函数明确拒绝。
- 先发布 deploy preview，通过门禁和公开包检查后，再发布同一版生产构建。
- 生产部署 ID：`6a517377f33538131b5b1843`；部署标题：`ForFlow full-site refresh v23 production`。

### 验证

- deploy preview：未登录访问首页返回 `302` 到门禁页，门禁页返回 `200`；旧码返回 `401`，新码返回 `200`；登录后首页返回 `200`，`/build_site.py` 返回 `404`。
- 生产域名：`https://forflow.ai/` 未登录返回 `302`；新码登录后首页返回 `200`，前端资源版本为 `20260711-final-flow-v23`，`/build_site.py` 返回 `404`。
- 生产门禁响应包含 CSP、`noindex`、`no-referrer`、`nosniff` 与私有内容缓存控制；Netlify API 返回生产部署状态 `ready`。

### 后续

- 新访问码只通过受控渠道发送给受邀访客；需要换码时直接更新 Netlify `SITE_GATE_PASSWORD` 并重新部署。
- 客户正式访问后，继续记录真实反馈；不要把门禁码写入源码、测试、维护文档或 Git 历史。

## 2026-07-11

### 变更范围

- 企业服务详情页、案例证据口径与公网安全收口，覆盖 `ai-readiness-audit.html`、四个 `service-*.html`、案例库及详情页、`build_site.py`、`styles.css`、Netlify 门禁、公开构建脚本与静态资源缓存版本。

### 主要变更

- 五个详情页采用同一套阅读顺序：首屏范围与周期、本页导航、适用条件、常见卡点、项目结果、服务范围、开展方式、交付材料、FAQ 和相关路径。
- 在页面前部增加“适合现在做 / 建议先别急”，直接说明内部负责人、真实材料、系统接口和风险边界等启动条件；准备度审核同步说明它不是认证、排名或部门绩效工具。
- 重写采用赋能、数据与知识治理、Agent 与工作流、实战培训四页内容。每页明确建议起步范围、企业侧参与人、五个阶段及阶段结果、四类可交付材料和不适用情况。
- 四个服务首屏保留原有绿色轨道与图标语言，分别使用编号 `02–05`、现有图标库和服务专属方法路径，替换过去四页共用的 `SE` 字样和通用“问题 → 价值 → 方案 → 运营”卡片。
- 增加可横向滚动的页内导航、服务事实栏、双栏适用性卡片和阶段结果样式；桌面首屏减少过多空白，手机端改为单列适用性卡片与满宽行动按钮。
- 静态资源版本更新为 `20260711-security-case-v20`，并同步 `templates/index.html` 与 `templates/playbook.html`，避免后续生成时回退到旧缓存版本。
- 案例统一分为公开客户案例、官方技术文章解读、合作场景材料和概念场景；Wren、Everllence P&amp;ID、Vanguard 保留客户案例身份，其余 AWS 页面按技术或方法文章标注，并补回官方母文与非 ForFlow 项目边界。
- 能效优化页保留工业协议、预测、调度、PLC / DCS 与安全技术链，但在取得书面披露授权前，不把“国家电网合作”作为列表背书或搜索关键词。
- Netlify 改为只发布 `dist/` 白名单构建；Edge 默认保护全部资源，登录函数加入同源 POST、限流、旧码停用、24 小时 `__Host-ff_gate` Cookie 与安全响应头。

### 验证

- `node --check script.js`、`env PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py`、`python3 tests/static_check.py` 与 `git diff --check` 通过；静态检查确认 23 个 HTML 页面本地引用完整。
- `node tests/invite_gate_check.js` 与 `node tests/gate_runtime_check.mjs` 通过，邀请码登录和边缘门禁没有被本轮修改破坏。
- in-app Browser 在桌面视口复核采用赋能页：标题、事实栏、服务专属图标与方法卡、本页导航和适用性内容均正常，无横向溢出或页面控制台报错。
- in-app Browser 以手机视口逐页复核五个详情页：页面身份正确、两张适用性卡片存在、手机菜单启用、页面宽度等于滚动宽度；FAQ 页内导航与展开交互通过，Agent 页主行动按钮可进入带 `topic=agent` 的联系页。
- 手机端首张截图曾抓到入场动效的中间帧；等待稳定状态后重新截图并结合页面宽度复核，门禁页与案例详情均无横向溢出。
- `python3 tests/public_build_check.py`、`python3 tests/static_check.py`、`node tests/invite_gate_check.js`、`node tests/gate_runtime_check.mjs`、五个 JavaScript `node --check` 与 `git diff --check` 通过；公开包不含源码、测试、维护文档、模板或内部 PDF。
- in-app Browser 复核案例库、P&amp;ID 来源区、Agent 评估页、门禁页与 Navigator 结果排序；桌面和 424px 手机状态无横向溢出，P&amp;ID 页尾保持在正文外，准备度为 `idea` 时审核服务排第一。
- 线上只读探测确认 `/build_site.py`、`/tests/gate_runtime_check.mjs` 和 `/docs/maintenance/site-governance.md` 仍返回 200；本地修复尚未部署，生产 P0 仍未关闭。

### 后续

- 当前修改仍是本地预览，尚未部署到 Netlify；下一轮可根据实际客户反馈收紧服务周期、报价入口和案例佐证。
- 发布前必须轮换 `SITE_GATE_PASSWORD`；旧码按已泄露处理。部署后需核对限流日志、安全响应头、旧源码 404 和 Cloudflare 缓存。

## 2026-07-10

### 变更范围

- 企业服务信息架构 v15，覆盖首页服务区、五个服务详情页、桌面与手机菜单、站内搜索、`build_site.py`、`templates/index.html` 和全站静态资源缓存版本。

### 主要变更

- 将企业服务统一为五个问题导向的入口：`AI 准备度审核`、`AI 采用与团队赋能`、`AI 数据与知识治理`、`企业 Agent 与工作流`、`AI 实战培训`，减少“赋能、培训、治理、搭建”之间的含混重叠。
- 首页服务区改为“你现在需要解决哪一件事？”，用判断方向、推动采用、补齐数据、接通流程、训练团队五类问题帮助访客自选入口。
- 准备度审核页首屏改为“把 AI 投入顺序排清楚。”，说明具体落到场景、条件缺口和 30/90 天路线；手机菜单把该服务移到企业服务第一项，并移除重复的企业服务和联系入口。
- 五个详情页、页尾、搜索卡片和生成器统一采用新命名；搜索结果补入准备度审核，企业服务数量从四项更新为五项。
- 参考 The Software House 的服务分组、常见项目类型和明确入口周期来收紧信息层级，只借鉴表达结构，没有复制其视觉样式。
- 静态资源版本更新为 `20260710-services-clarity-v15`。

### 验证

- `node --check script.js`、`env PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py`、`python3 tests/static_check.py` 与 `git diff --check` 通过；静态检查确认 23 个 HTML 页面本地引用完整。
- `node tests/invite_gate_check.js` 与 `node tests/gate_runtime_check.mjs` 通过，邀请码门禁与受保护页面未受本轮修改影响。
- in-app Browser 复核准备度审核桌面首屏、企业服务菜单和首页服务区：五个入口均可见，无横向溢出、无控制台报错；从菜单点击“AI 数据与知识治理”可正确进入对应详情页。
- 手机端 DOM 与布局检查确认无横向溢出、菜单顺序正确且重复入口已移除；本轮浏览器截图存在缩放裁切偏差，因此没有把手机端像素级视觉复核标记为完全通过。

### 后续

- 当前修改仍是本地预览，尚未部署到 Netlify；后续可继续统一五个详情页的“适合谁、何时不适合、典型交付物”信息结构。

## 2026-07-10

### 变更范围

- 场景诊断核心流程 v14，覆盖 `navigator.html`、`navigator-results.html`、`script.js`、`styles.css`、`build_site.py`、`tests/interaction_check.py` 与全站静态资源缓存版本。

### 主要变更

- 将入口、三段问题和结果页改成更直接的业务表述；明确四个非必填下拉项，减少用户因“不知道哪些必须填”而停住。
- 下一步按钮不再静默禁用：答案不完整时仍可点击，并在固定操作栏和提示消息里说明还缺哪一项。
- 手机端固定操作栏恢复当前步骤说明，并增加页面底部安全距离，避免只看到灰色按钮却不知道原因。
- 切换步骤后把焦点移到新问题标题；侧边进度中只有已完成步骤可返回，减少键盘和读屏用户误入未完成步骤。
- 将大范围 `aria-live` 收窄到操作状态；结果页说明补充三种排序各自回答的问题。
- 静态资源版本更新为 `20260710-navigator-flow-v14`，并同步生成器与交互测试断言。

### 验证

- `node --check script.js`、`env PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py`、`python3 tests/static_check.py` 与 `git diff --check` 通过。
- `node tests/invite_gate_check.js` 与 `node tests/gate_runtime_check.mjs` 通过，门禁码与受保护页面没有被本轮修改破坏。
- 本地预览服务器已在 `127.0.0.1:8765` 启动，主机侧 `curl -I` 返回 `HTTP/1.0 200 OK`。
- in-app Browser 已复核首页诊断入口卡片；独立诊断页被当前 Browser URL policy 拦截，因此本轮没有把 Navigator 全流程的视觉或点击结果标记为已验证，也没有改用其他浏览器绕过限制。

### 后续

- 需要在允许访问 `navigator.html` 的同一浏览器中补跑桌面与手机端完整流程：空答案提示、三步填写、回退修改、结果跳转与排序。

## 2026-07-10

### 变更范围

- 首页资源区响应式修复 v13，覆盖 `styles.css`、全站静态资源缓存版本、`build_site.py`、`search-index.json` 与 23 个 HTML 页面。

### 主要变更

- 将资源卡单列断点从 600px 提升到 700px，修复 606px 附近仍套用两列布局导致右侧大片空白的问题。
- 701–900px 使用明确的网格区域：诊断器与搜索并排，Playbook 横跨下一行；避免 DOM 顺序造成空网格。
- 700px 以下三张卡统一单列、保持原顺序和完整点击区域；桌面三列布局不变。
- 静态资源版本更新为 `20260710-resources-responsive-v13`，避免浏览器继续命中旧 CSS。

### 验证

- `python3 tests/static_check.py`、`node --check script.js` 与 `git diff --check` 通过。
- in-app Browser 复核 406px 与 658px 有效视口：三张资源卡均为完整单列，无横向溢出。
- in-app Browser 复核 869px 有效视口：诊断器与搜索并排，Playbook 独占下一行，不再出现空单元格。
- 页面无坏图、无控制台错误；点击“AI 场景诊断器”可正常进入 `navigator.html`。

### 后续

- 当前修复仍为本地预览，尚未部署到 Netlify。

## 2026-07-10

### 变更范围

- 首页公开文案去模板腔 v12，覆盖 `index.html` 与 `templates/index.html` 的首屏、业务挑战、服务路径、Navigator、方法、资源、FAQ 和页尾行动文案。

### 主要变更

- 删除高频的“先……再……”二元句式，把抽象口号改成企业读者能直接理解的日常问题和具体动作。
- 业务挑战主标题改为“日常工作里，哪件事最该改？”，说明文字改为“AI 能不能帮上忙、该从哪里开始”。
- 首屏改用“把投入、数据、权限和验收算清楚”“值得做就跑小试点，效果不好及时停”等更具体的表达。
- 同步收紧方法、资源、FAQ 与页尾文案；保留原有业务含义、公开口径和内部 Q2Q 边界。

### 验证

- `python3 tests/static_check.py` 与 `git diff --check` 通过。
- in-app Browser 复核 1391px 桌面与 406px 手机视口：新标题和说明正常换行，无横向溢出、无坏图、无页面控制台错误。
- 实际点击首张业务挑战卡片，正确进入带 `challenge=customer` 参数的 Navigator 页面。

### 后续

- 当前修改仍是本地预览，尚未部署到 Netlify。

## 2026-07-10

### 变更范围

- 首页细节收口 v11，覆盖手机与桌面的段落节奏、卡片密度、关键入口、FAQ 交互，以及全站静态资源缓存版本。

### 主要变更

- 将首页主要章节的上下留白从 120px 收至 96px，并为 900px、600px 两档视口分别调整标题、章节头和卡片高度。
- 手机端关键入口从 5 行改为 2+2+1 的两列结构；压缩挑战、服务、Navigator、方法、案例和资源卡片，保留可读字号与完整触控区域。
- 手机端服务路径改为更紧凑的三列信息结构，交付项使用两列排列，并移除重复表达整行可点击状态的圆形箭头。
- FAQ 改为单项展开：打开新问题时自动收起其他答案，并同步更新每个问题的 `aria-expanded`。
- 将 23 个 HTML 页面、精修模板、搜索索引和生成器的样式脚本版本统一更新为 `20260710-home-detail-v11`。

### 验证

- `node --check script.js`、`python3 tests/static_check.py`、`node tests/invite_gate_check.js`、`node tests/gate_runtime_check.mjs` 和 `git diff --check` 全部通过。
- in-app Browser 复核 424px 手机视口：无横向溢出、无坏图、无页面控制台错误；首页总高度由本轮修正前的 17,393px 降至 14,873px。
- in-app Browser 复核 1113px 中等桌面视口：无横向溢出、无坏图；首页总高度由 10,359px 降至 9,880px。
- 实际操作确认桌面 mega-nav、全站搜索、手机菜单、首页 Navigator 第 1→2 步和 FAQ 单项展开均正常。

### 后续

- 当前仅完成本地预览与验证，尚未部署到 Netlify；下一轮可继续逐页收服务详情页和案例详情页的段落密度。

## 2026-07-10

### 变更范围

- 首页文案与全站公共介绍 v10，覆盖 `index.html`、`templates/index.html`、公共 mega-nav、页脚介绍和 `build_site.py` 维护入口。

### 主要变更

- 按“值不值得做 → 缺什么条件 → 怎么试点 → 如何验收和复评”重写首页叙事，保留“让 AI 真正流入业务”的主标题。
- 首屏说明改为场景判断、数据与权限、验收和上线后复评；四项原则同步改为“判断投入、明确验收、控住权限、持续复评”。
- 将“端到端、可拥有、能力沉淀”等抽象表达改为投入判断、可验收、可复评和责任边界等具体结果。
- 重写六类业务挑战、五条服务路径、Navigator、四阶段方法、案例说明、资源入口和 FAQ 首条回答，减少宣传语、否定式排比和技术术语。
- 公开案例明确标注“不代表 ForFlow 客户成果”，避免把外部材料误读为自有业绩。
- 全站公共导航与页脚介绍统一为“判断值得投入的场景、组织试点交付、持续复评”的当前公开口径；Q2Q 等内部机制未进入页面文案。

### 验证

- `node --check script.js` 通过。
- `python3 tests/static_check.py` 通过：23 个 HTML 页面与本地资源完整。
- `git diff --check` 通过。
- in-app Browser 复核桌面与 424px 窄屏：首页无横向页面溢出、无坏图、无站点控制台错误；首屏长句、服务说明和四项原则均可正常换行。
- DOM 文案复核确认首页九个主要段落已加载新版文字；公开案例免责声明与四阶段交付物同步生效。

### 后续

- 当前仅完成首页和全站公共介绍，服务详情页、案例详情页与 Playbook 正文仍需分批做同样的文字审校。

## 2026-07-10

### 变更范围

- 全站顶部栏 v9，覆盖 utility bar、桌面主导航与 mega-nav、滚动状态、手机品牌区、菜单抽屉和静态资源版本号；维护入口为 `styles.css`、`script.js`、`build_site.py` 与 `templates/`。

### 主要变更

- 降低顶部两层结构的视觉噪音：压缩 utility bar 和主导航高度，收紧品牌标识、导航、搜索与诊断按钮的比例关系。
- 将当前页面状态从灰色胶囊改为 Flow Green 下划线；hover、下拉展开与键盘焦点继续保留清晰反馈。
- 新增滚动后顶部栏的实体背景和轻阴影，首页打开时保持更轻，滚动进入正文后提高可读性。
- 手机端统一为 64px 顶栏、受控宽度品牌标识和 44px 菜单按钮；菜单抽屉加入安全区、内部滚动、当前项、分组加减状态和完整宽度 CTA。
- 修正手机菜单 Escape 关闭后的焦点回归，以及从手机菜单打开搜索时菜单按钮的 `aria-label` 状态。
- 将 23 个 HTML 页面的样式与脚本缓存版本统一更新为 `20260710-topbar-v9`，并同步生成器与精修模板。

### 验证

- `node --check script.js` 通过。
- `python3 tests/static_check.py` 通过：23 个 HTML 页面、本地资源和搜索索引版本一致。
- `node tests/invite_gate_check.js` 与 `node tests/gate_runtime_check.mjs` 通过，服务端访问码门禁未被本轮改动破坏。
- `git diff --check` 通过。
- in-app Browser 复核首页桌面、1113px 中等宽度、424px 手机视口和案例中心：无横向溢出；桌面 mega-nav 可展开；手机菜单可开关、分组可展开、CTA 完整落在视口内；滚动后 `is-scrolled` 状态和阴影生效；页面控制台无站点脚本错误。

### 后续

- 当前改动仅完成本地预览与验证，尚未部署到 Netlify；获得页面方向确认后再发布生产。

## 2026-07-10

### 变更范围

- 将门禁升级为 Netlify 服务端访问码校验，覆盖 `landing.html`、`gate-client.js`、`netlify/functions/gate-login.mjs`、`netlify/edge-functions/auth-gate.mjs`、`netlify.toml`、门禁专项测试和部署说明。

### 主要变更

- 不使用账号、邮箱、注册或 Netlify Identity；访客只输入共享访问码。
- 访问码仅保存在 Netlify 环境变量 `SITE_GATE_PASSWORD`，浏览器源码不包含访问码；正确验证后写入 30 天的 `HttpOnly`、`Secure`、`SameSite=Lax` Cookie。
- 未授权的根路径、HTML 页面和 Pretty URL 由 Netlify Edge Function 跳转到门禁页并保留安全回跳目标。

### 验证

- `node --check script.js`
- `node --check gate-client.js`
- `node --check netlify/functions/gate-login.mjs`
- `node --check netlify/edge-functions/auth-gate.mjs`
- `node tests/invite_gate_check.js`
- `node tests/gate_runtime_check.mjs`
- `python3 tests/static_check.py`
- `git diff --check`
- `npx netlify status` 与站点 API：已确认项目 `forflow-enterprise-suite-v3` 绑定 `https://forflow.ai`，SSL 与 Force SSL 生效。
- 生产环境 Secret `SITE_GATE_PASSWORD` 已设置；当前 Netlify 套餐不支持 granular scope，因此使用 production context 的全作用域 Secret。
- `npx netlify deploy --prod` 直连部署成功：Deploy ID `6a50d2d7f2bf0370c8d10828`，生产地址 `https://forflow.ai`。
- 线上无 Cookie 访问 `/` 与 `/contact` 均返回 `302` 到 `landing.html?next=...`；错码返回 `401`；正确访问码返回 `200` 并写入安全 Cookie；携带 Cookie 访问 `/` 与 `/contact` 均返回 `200`。

### 后续

- 后续如需更换访问码，只更新 Netlify Secret `SITE_GATE_PASSWORD` 并重新部署；不改网页源码。

## 2026-07-10

### 变更范围

- 重做官网受邀预览页并修复首页主 Hero 图片，覆盖 `landing.html`、`templates/index.html`、`index.html`、`styles.css`、`script.js`、`build_site.py`、全站静态 HTML 的资源版本、`search-index.json`、相关测试、`assets/invite/forflow-private-preview.jpg`、`assets/home/forflow-workflow-hero-v2.jpg` 与 `design-qa.md`。

### 主要变更

- 将原深色蓝绿光晕和玻璃表单改为与首页同源的白色／云灰、64px 细网格、黑色正文与 Flow Green 双栏入口；桌面左侧完成邀请码任务、右侧展示独立生成的业务场景图，手机端先展示表单再展示图片。
- 右侧场景图使用 Image Gen 单独生成，落库为 `1122 × 1402` JPEG；品牌标识不使用生成图中的重绘版本，页面直接引用现有正确资产 `assets/forflow-lockup-transparent.png`。
- 门禁文案统一为“受邀预览”；访问支持邮箱使用 `hello@forflow.ai`，并从表单校验区移入真正的页面底栏，避免被误读为错误提示的一部分。
- 移除图片底部与页底栏冲突的绿色装饰线，桌面图片改为方形裁切，使页底栏稳定落在 `1440 × 900` 首屏底部；移动端底栏随内容自然收尾。
- 输入框新增 `required`、`aria-invalid`、独立空值提示、编辑后清错、触屏设备不自动聚焦、存储失败提示和忙碌状态。
- 门禁仍保持轻量前端入口的技术边界，邀请码、30 天本地通行记录和安全回跳规则不变。
- 首页原 `hero-hand.jpg` 是一张已经烘焙 Logo、英文竖排与说明文字的整版海报，和页面原生叠层重复。改用 Image Gen 单独生成的无文字、无 Logo 业务流程底图 `assets/home/forflow-workflow-hero-v2.jpg`，保留网页里的 Flow Green 动线、浮层卡片与品牌文案。
- 进一步清理 Hero 图片叠层：移除右侧抢画面的 `DIAGNOSIS / DEPLOYMENT / GROWTH` 大号竖排字；三个绿色节点由容器百分比绝对定位改为同一条 SVG 曲线内的 `circle`，桌面和手机缩放时始终跟随曲线。
- 手机端 Hero 改为专属简化构图：隐藏两张桌面浮层卡片和底部英文角标，只保留照片、绿色路径和节点；图片槽从 `500px` 缩短为 `420px`，路径向内收，避免卡片遮挡主体和首尾节点贴边。

### 验证

- `PYTHONPATH=.python-deps PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 build_site.py`
- `PYTHONPATH=.python-deps PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 tests/static_check.py`
- `node --check script.js`
- `node --check tests/invite_gate_check.js`
- `node tests/invite_gate_check.js`
- `PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py tests/static_check.py tests/interaction_check.py tests/polished_pages_check.py`
- `git diff --check`
- 原始 Image Gen PNG 和项目内 JPEG 均已人工打开检查，主体、绿色流线、手写笔、平板和纸质材料完整。
- Chromium 桌面复核通过：`1440 × 900` 下文档高度与视口同为 `900px`，底栏位于首屏底部，无控制台错误。
- Chromium 手机复核通过：`390 × 844` 下 `scrollWidth=innerWidth=390`，图片和双行底栏完整，无横向溢出。
- Chromium 错码交互通过：提交错误邀请码后显示明确状态，输入框为 `aria-invalid=true`，控制台无错误。
- in-app Browser 首页桌面复核通过：新 Hero 资源完整加载为 `1254 × 1254`，没有内嵌品牌文字与页面叠层重复，无控制台错误。
- in-app Browser 首页手机复核通过：`scrollWidth=innerWidth`，图片主体、流程动线和浮层卡片在窄屏裁切中保持完整。
- in-app Browser Hero 叠层复核通过：桌面和手机端均无竖排大字，三个节点为 SVG `circle` 且使用同一 `viewBox` 坐标；主按钮“开始场景诊断”可正常进入 Navigator，控制台无错误。
- in-app Browser 手机 Hero 复核通过：窄屏下三块重复浮层均为 `display:none`，图片槽为 `420px`，路径首尾节点完整可见，`scrollWidth=innerWidth`；桌面端浮层仍按原设计展示。

### 后续

- 视觉与交互 QA 已完成；部署后补充生产地址上的门禁回跳和邮件链接烟测。

## 2026-07-09

### 变更范围

- 新增官网邀请码门禁页 `landing.html`，同步更新 `script.js`、`styles.css`、`templates/index.html`、`build_site.py`、`templates/README.md`、`README.md`、全站生成 HTML、`search-index.json`、`tests/static_check.py`、`tests/invite_gate_check.js`、`tests/interaction_check.py`、`tests/polished_pages_check.py` 和本维护日志。

### 主要变更

- 当时曾使用临时前端码和 30 天本地通行记录；该方案现已废弃，生产门禁改为服务端校验、HttpOnly Cookie 与短期通行。
- `landing.html` 复用 ForFlow 品牌视觉和 Flow Green 语言，页面只承担“门禁页”职责，不替代原首页。
- 根据首屏反馈精简 `landing.html`：移除右侧展示视觉、下方三条内容预告和开放范围标签，保留品牌、内测开放标题、邀请码输入和状态反馈。
- 门禁逻辑加入安全回跳处理，拒绝外部 URL、协议相对 URL 和回跳到自身；`landing.html?reset=1` 可清除本地通行状态。
- `build_site.py`、`templates/index.html` 和生成页统一恢复五条企业服务路径，把 `AI 准备度审核` 纳入服务导航、移动菜单和页脚，避免重建时回退成旧的四服务结构。
- 浏览器测试脚本在进入既有页面前注入有效门禁状态，同时新增独立 Node 逻辑检查覆盖锁定跳转、错码提示、正确码放行和回跳。

### 验证

- `python3 build_site.py`
- `node --check script.js`
- `node --check tests/invite_gate_check.js`
- `node tests/invite_gate_check.js`
- `PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py tests/static_check.py tests/interaction_check.py tests/polished_pages_check.py`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `git diff --check`
- 浏览器预览未能在当前沙盒完成：`python3 -m http.server`、动态端口和 Ruby WEBrick 均因本地 bind 权限返回 `Operation not permitted` / `Permission denied`；Playwright CLI 与 daemon 受缓存目录权限限制；CDP 连接本机调试端口被拒；Chrome headless 直接启动退出 134；Computer Use 当前浏览器 URL 不允许操作。
- 追加首屏精简后尝试用 in-app Browser 复核当前 `file://.../landing.html`，被 Browser URL 安全策略拒绝；未改用浏览器绕路。

### 后续

- 这次是静态站前端门禁，适合小范围入口控制。若要阻止技术用户直接请求静态资源，需要再升级为 Netlify Edge / Function、CDN 规则或服务端鉴权。
- 待本机端口和浏览器自动化路径恢复后，补跑 `tests/interaction_check.py`、`tests/polished_pages_check.py`，并做桌面与手机视口截图复核。

## 2026-06-29

### 变更范围

- 新增 Netlify 服务端活码能力，覆盖 `netlify.toml`、`netlify/functions/q.js`、`netlify/functions/qr-routes.json`、`tools/generate_dynamic_qr.py`、`requirements.txt`、`README.md` 和本维护日志。

### 主要变更

- 在 Netlify 配置中新增 `/q/:code` rewrite，把固定二维码入口转发到 `q` Function。
- 新增 `forflow` 默认活码，当前目标为 `/contact.html`；上线后可通过码表或 `QR_REDIRECTS_JSON` 环境变量切换目标，二维码图片不用重做。
- 新增二维码生成脚本，可根据正式域名生成 `assets/qr/:code.svg`、`:code.png` 和扫码 URL 记录文件。
- Function 响应设置 `no-store`、`noindex`，并限制跳转目标只能来自配置码表，避免开放跳转。

### 验证

- `node --check netlify/functions/q.js`
- 本地函数行为检查通过：默认 `forflow` 返回 302 到 `/contact.html`，查询参数透传，未知码返回 404，`QR_REDIRECTS_JSON` 覆盖生效，禁用码返回 410。
- `python3 tools/generate_dynamic_qr.py --base-url http://127.0.0.1:8888 --code forflow`
- 本地测试二维码生成通过：`assets/qr/forflow.svg`、`assets/qr/forflow.png`、`assets/qr/forflow.url.txt`；测试 URL 为 `http://127.0.0.1:8888/q/forflow`，不是最终印刷域名。
- `python3 -m json.tool netlify/functions/qr-routes.json >/tmp/forflow-qr-routes.json`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `git diff --check`

### 后续

- 生成正式可印刷二维码前，需要确认线上域名和 `forflow` 的最终目标链接。
- Netlify 重新部署后，应补充部署链接，并用真实域名扫码验证 `/q/forflow` 跳转。

## 2026-06-25

### 变更范围

- 复核并补强企业 Agent 评估先行案例 `case-agent-evaluation-first.html`，同步更新维护入口 `build_site.py`、共享样式 `styles.css`、生成页面、`search-index.json` 和本维护日志。

### 主要变更

- 按用户提供的原文重新核对 Agent Evaluation 细节，补回此前遗漏的 Amazon 内部数千个生产级 Agent 经验、本系列四篇定位、Mixture-of-Experts 非确定性、`package.json` / `Changelog` 隐性依赖、Claude Sonnet / Claude Haiku 评估取舍、生产采样 78% 到 95% 的工具选择改进、外部数据 API Trace、CloudWatch / Datadog / Dynatrace / LangSmith / Langfuse、MCP Server、GitHub、工具代码示例、行级 / 列级安全、下一篇与动手实验等细节。
- 在 hero 区新增“长文阅读路线”模块，按决策层、业务负责人、技术 / 平台团队拆分阅读入口，帮助长文读者先抓判断点，再进入完整正文。
- 为 `.case-reading-map` 增加桌面四列、手机单列样式；手机端不产生整页横向滚动，保持案例详情页的上下滑动稳定性。
- 将全站静态资源版本推进到 `v=20260625-agent-eval-readability-v24`，刷新生成 HTML、CSS/JS 引用和 JSON 搜索索引。

### 验证

- `python3 build_site.py`
- 原文关键细节扫描：`missing_count=0`
- `PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py tests/static_check.py tests/interaction_check.py tests/polished_pages_check.py`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `python3 -m json.tool search-index.json >/tmp/forflow-search-v24.json`
- `node --check script.js`
- `git diff --check`
- in-app Browser 桌面 DOM QA：`case-agent-evaluation-first.html?qa=readability-v24` 加载 `styles.css?v=20260625-agent-eval-readability-v24`，`case-reading-map` 入口数为 3，关键补充术语缺失数为 0，console 无 error / warn，整页无横向溢出。
- in-app Browser 手机 QA：阅读路线在移动端为单列，`rootScrollWidth=424 / innerWidth=424`，整页无横向溢出，console 无 error / warn。
- in-app Browser 交互 QA：点击阅读路线中的 `#architecture` 入口后，URL hash 为 `#architecture`，目标段落进入视窗附近，仍无横向溢出且 console 无 error / warn。
- 说明：浏览器截图接口一度返回空白帧，最终页面证明以 DOM、布局数据、console 日志和真实点击状态为准；该截图异常未作为网站问题计入。

### 后续

- 用户后续补充本系列后续文章时，优先保持“原文细节完整 + 表格/图解辅助阅读”的模式；新增图只作为阅读证据层，不替代原有技术叙事。

## 2026-06-25

### 变更范围

- 全站“案例”入口命名口径，覆盖 `build_site.py`、`templates/index.html`、`templates/playbook.html`、`templates/README.md`、`cases.html`、`search.html`、`README.md`，以及未由生成器重写的 `case-healthcare-agent-roi.html`、`case-manufacturing-pid-intelligence.html`。

### 主要变更

- 将顶部快捷链接、主导航、移动菜单、手册与洞察下拉、页脚、案例索引页、搜索页 tab / 分组、案例详情面包屑、返回按钮和相关案例入口统一为 `案例&博客`。
- 将案例索引页 hero 文案调整为：`案例&博客不只展示技术细节，也回答为什么做、如何做、谁参与、怎样验证，以及下一步如何扩展。`
- 将搜索入口说明统一为 `查找服务、场景、资料、案例与博客`，避免旧模板仍显示“资料与案例”。
- 将全站静态资源版本推进到 `v=20260625-cases-blog-label-v23`，刷新生成 HTML、CSS/JS 引用和 `search-index.json`。

### 验证

- `python3 build_site.py`
- `PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py tests/static_check.py tests/interaction_check.py tests/polished_pages_check.py`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `python3 -m json.tool search-index.json`
- `node --check script.js`
- `git diff --check`
- 交付页面与模板旧文案扫描：`案例中心`、`企业案例中心`、`返回案例中心`、`资料与案例`、`案例 <span>`、`案例页不只展示技术` 均无残留；维护日志里的历史记录不作为页面残留计入。

### 后续

- 后续新增案例或博客时继续从 `CASE_LIBRARY_ITEMS` 维护索引与搜索联动，一级导航不再新增单独“博客”入口，先合并到 `案例&博客`。

## 2026-06-25

### 变更范围

- 新增企业 Agent 评估先行案例 `case-agent-evaluation-first.html`，同步更新 `build_site.py`、`CASE_LIBRARY_ITEMS`、`cases.html`、`search.html`、`search-index.json`、案例视觉资源、样式、README 模板与测试覆盖。
- 追加 Agent DLC / ADLC 正文图 `assets/cases/agent-evaluation-dlc-loop.png`，并在不删减原文叙事的前提下，补充多组解释型表格与原生流程图，作为正文的证据和阅读辅助层。

### 主要变更

- 将用户提供的“企业智能体之旅：为什么评估（Evaluation）是一切的起点”整理为新版案例详情页，保留从原型到生产鸿沟、传统测试失效、ADLC 飞轮、先定义成功、自动化评估、持续测试、可观测性、可评估架构、安全与个性化、评估四重角色等主线。
- 根据复核反馈补回原文关键细节：四篇系列定位、传统测试失效的三类原因展开、ADLC“先定义好”的返工逻辑、财务分析 / 人力资源政策助理 / IT 支持三类 Agent 的职责、语气、工具和基准样本、生产采样下工具选择从 78% 回升到 95% 的改进循环、组织级平台化扩展、OpenTelemetry Trace 三层可观测性、工具定义五要素、确定性代码替代 Agent 工具、多智能体交接点、安全 Gateway / Policy 外部化和用户记忆隔离。
- 在 ADLC 段落后加入用户提供的中文 Agent DLC 飞轮图，作为正文 evidence figure；图片使用 `width="1860"` / `height="958"` 保留懒加载前的比例空间，避免手机端滚动时布局跳动。
- 新增 `.case-agent-table` 和 `.case-figure--dark-diagram` 样式：桌面端完整阅读，手机端图和表格在各自容器内横向滚动，不造成整页横向溢出。
- 在 `build_site.py` 新增 `agent-evaluation-first` 案例清单项，案例中心和搜索页从 `CASE_LIBRARY_ITEMS` 自动联动；搜索关键词覆盖 `Evaluation`、`ADLC`、`Prompt 变更`、`静默漂移`、`LLM-as-a-Judge`、`Trace`、`OpenTelemetry`、`A/B测试`、`MCP`、`A2A`、`Gateway`、`Policy` 等。
- 调用 imagegen 生成无可读文字的中国企业 Agent 上线评审场景 hero 图，落到 `assets/cases/agent-evaluation-first-hero.png`，用于表达评估、Trace、质量门控和生产发布前复核。
- 新增 `case-study-hero--agent-eval` 背景样式，正文复用现有案例组件，保持新版案例详情页的桌面与手机阅读标准。
- 在传统测试失效、评估数据集、持续测试、可观测性、可评估架构、安全外部化等段落补充表格或原生图解；恢复多智能体协作模式原有卡片，新增表格仅作为补充对照，不替换正文和原有卡片。
- 新增 `.case-data-table`、`.case-native-diagram` 样式，移动端采用组件内部横向滚动，避免整页横向晃动。
- 修复 Agent Evaluation 案例新增图在手机端固定宽度显示不全的问题：ADLC 正文 PNG 通过 `.case-figure--mobile-fit` 在手机端完整按容器缩放；新增原生流程图在手机端改为纵向堆叠，避免必须横向拖动才能看全。
- 修复共享 SVG sprite 缺少 `i-chart` symbol 导致部分案例卡片 icon 只显示黑色底块的问题；`templates/index.html` 补齐 `i-chart`，并在 `tests/static_check.py` 增加全站 `<use href="#...">` 与 `<symbol id="...">` 的匹配检查，防止后续新增页面再次出现缺失 icon。
- 将全站静态资源版本推进到 `v=20260625-icon-symbol-fix-v22`，刷新生成 HTML、CSS/JS 引用和 JSON 搜索索引。

### 验证

- `python3 build_site.py`
- `PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py tests/static_check.py tests/interaction_check.py tests/polished_pages_check.py`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `python3 -m json.tool search-index.json`
- `node --check script.js`
- `git diff --check`
- SVG symbol 回归扫描：全站 HTML 的 `<use href="#...">` 引用与 `<symbol id="...">` 定义对比结果为 `missing []`，`ref_count=46 / def_count=47`。
- 现有 `tests/polished_pages_check.py` / `tests/interaction_check.py` 依赖 Chrome CDP `127.0.0.1:9226`；当前用户已关闭调试 Chrome，提升权限重跑后为 `ECONNREFUSED`，未作为页面失败计入。
- Headless Google Chrome 渲染 QA：`case-agent-evaluation-first.html?qa=v20-supplemental` 桌面 `1440×1800` 与手机 `390×1600` 均无整页横向溢出；桌面 `rootScrollWidth=1440 / innerWidth=1440`，手机 `rootScrollWidth=390 / innerWidth=390`；新增 `.case-data-table` 数量为 6，`.case-native-diagram` 数量为 2，`#architecture .case-fit-card` 数量为 4，补充表格均为组件内部横向滚动。
- Headless Google Chrome 手机图像回归 QA：`case-agent-evaluation-first.html?qa=mobile-fit-v21-final` 加载 `styles.css?v=20260625-agent-evaluation-mobile-figure-v21`；手机视口 `390×1600` 下整页无横向溢出，ADLC 图 `figureWidth=386 / imageWidth=386 / imageNaturalWidth=1860`，不再固定为 `920px`；两组 `.case-native-diagram` 均为纵向堆叠，`scrollWidth=clientWidth=386`。
- in-app Browser 回归 QA：`case-agent-evaluation-first.html?qa=icon-symbol-v22#why-fail` 手机宽度下第一张“非确定性”卡片引用 `href="#i-chart"`，`symbol#i-chart` 存在，图标尺寸 `22×22`，颜色和描边均为 `rgb(108, 246, 126)`，console 无 error / warn，整页无横向溢出。
- `CDP_PORT=9231 PYTHONPATH=.python-deps python3 tests/polished_pages_check.py > /tmp/forflow-polished-v18-expanded.log`
- Playwright 渲染 QA 复核：`case-agent-evaluation-first.html` 桌面和手机视口均 HTTP 200，整页无横向溢出，手机端 `scrollWidth=390 / innerWidth=390`，可滑到底并返回顶部，目录无横向滚动，标题行高比为 `1.2`，无缺失图片、无页面 console error；案例中心和 `search.html?search=Evaluation` 均能检索到新案例。
- Browser DOM 复核：`case-agent-evaluation-first.html?qa=agent-dlc-figure-table-v19-mobile-2` 手机视口无整页横向溢出，ADLC 图预留高度正常，`.case-agent-table` 内部横向滚动，关键术语 `getUpcomingHolidays`、`P50 低于 2 秒`、`从 92% 悄悄降到 84%`、`约 8,500`、`A2A、MCP、HTTP` 均存在，console 无 error / warn。
- Playwright 截图复核：`/tmp/forflow-agent-eval-adlc-desktop-v19.png`、`/tmp/forflow-agent-eval-adlc-mobile-v19.png`、`/tmp/forflow-agent-eval-table-desktop-v19.png`、`/tmp/forflow-agent-eval-table-mobile-v19.png`；桌面和手机均加载 `agent-evaluation-dlc-loop.png` 原图尺寸 `1860×958`，手机端图容器和表格容器均为内部横向滚动，整页无横向溢出。

### 后续

- 用户后续会补充材料；补充后优先扩展正文细节和 evidence figure，不替换当前 hero 场景图的定位。

## 2026-06-25

### 变更范围

- 新增先锋集团虚拟分析师案例 `case-vanguard-virtual-analyst.html`，同步更新 `build_site.py`、`CASE_LIBRARY_ITEMS`、`cases.html`、`search.html`、`search-index.json`、案例视觉资源、样式、README 模板与测试覆盖。

### 主要变更

- 将用户提供的“先锋集团虚拟分析师：AI 就绪数据的八项原则与实践”整理为案例详情页，保留核心认知、组织协作、AWS 技术栈、八项原则、元数据目录、语义层、示例库、数据质量、变更控制、持续评估、可衡量成果和知识图谱/RAG 下一步。
- 在 `build_site.py` 新增 `vanguard-virtual-analyst` 案例清单项，案例中心和搜索页从 `CASE_LIBRARY_ITEMS` 自动联动；搜索关键词覆盖 `先锋集团`、`Vanguard`、`虚拟分析师`、`AI-ready`、`语义层`、`元数据目录`、`示例库`、`数据质量`、`Bedrock Guardrails`、`Redshift`、`Glue` 等。
- 调用 imagegen 生成无可读文字的中国金融分析 / AI-ready data 场景 hero 图，落到 `assets/cases/vanguard-virtual-analyst-hero.png`，避免外文界面、虚构 logo 和科幻化数据大屏。
- 新增 `case-study-hero--vanguard` 背景样式，正文复用现有案例组件，保持新版案例详情页的桌面与手机阅读标准。
- 将全站静态资源版本推进到 `v=20260625-vanguard-analyst-case-v17`，刷新生成 HTML、CSS/JS 引用和 JSON 搜索索引。

### 验证

- `python3 build_site.py`
- `PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py tests/static_check.py tests/interaction_check.py tests/polished_pages_check.py`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `python3 -m json.tool search-index.json >/tmp/forflow-search-vanguard-v17.json`
- `node --check script.js`
- in-app Browser 复核：`case-vanguard-virtual-analyst.html?qa=vanguard-v17-*` 桌面与手机视口均加载 v17，标题、hero 图自然尺寸 `1672×941`、4 个 proof item、10 个目录项、8 项原则、6 个 AWS 技术栈卡、4 个质量检查卡、6 个参考链接和关键术语均存在，未发现页面 console error，未出现整页横向溢出。
- in-app Browser 复核：`search.html?search=虚拟分析师&qa=vanguard-v17-search` 使用 `json-index`，索引版本为 `20260625-vanguard-analyst-case-v17`，新案例结果可见；点击结果可进入 `case-vanguard-virtual-analyst.html`。
- in-app Browser 复核：手机视口下目录 `八项原则` 链接可滚动到 `#principles`，等待平滑滚动完成后目标标题位置正常，仍无横向溢出。
- 说明：in-app Browser 截图 API 本轮仍出现一次 `Page.captureScreenshot` 超时，浏览器外层 Statsig 遥测也出现网络超时；两者均不来自网站脚本。页面验证改用 DOM、图片自然尺寸、控制台日志、滚动位置和横向溢出数据完成。

### 后续

- 如果后续拿到 Vanguard / AWS 原始架构图或截图，应按正文 evidence figure 单独补图；hero 场景图不替代技术结构图。

## 2026-06-25

### 变更范围

- 新增金融文档 BDA 自动化案例 `case-financial-bda-document-automation.html`，同步更新 `build_site.py`、`CASE_LIBRARY_ITEMS`、`cases.html`、`search.html`、`search-index.json`、案例样式、测试覆盖、README 与案例视觉资源。

### 主要变更

- 将用户提供的 Bedrock Data Automation 金融文档提取文章整理为案例详情页，保留银行对账单、W-2、1099-B、供应商合同四类场景的 Blueprint 字段、复杂性和提取结果说明。
- 在 `build_site.py` 新增 `financial-bda-document-automation` 案例清单项，案例中心和搜索页均从同一份 Python 清单联动生成，关键词覆盖 `BDA`、`Blueprint`、`金融文档`、`W-2`、`1099-B`、`供应商合同`、`JSON/CSV` 等入口。
- 调用 imagegen 生成无可读文字的中国金融运营场景 hero 图，落到 `assets/cases/financial-bda-document-automation-hero.png`，正文保留文档自动化和 Blueprint 结构叙事，不用泛化场景图替代技术内容。
- 新增 Blueprint 流程、四类文档场景卡和 schema 代码块样式；手机端 schema 在块内横向滚动，避免整页横向溢出。
- 将全站静态资源版本推进到 `v=20260625-financial-bda-case-v16`，刷新生成 HTML、CSS/JS 引用和 JSON 搜索索引。

### 验证

- `python3 build_site.py`
- `PYTHONPATH=.python-deps python3 tests/static_check.py`
- `python3 -m json.tool search-index.json >/tmp/forflow-search-financial-v16.json`
- `node --check script.js`
- in-app Browser 复核：`case-financial-bda-document-automation.html?qa=financial-bda-v16-*` 桌面与手机视口均加载 v16，标题、4 个 schema block、4 类文档卡、AWS 官方资料链接、关键术语和 hero 图均存在，未发现页面 console error，未出现整页横向溢出。
- in-app Browser 复核：`search.html?search=金融文档&qa=financial-bda-v16-search-noscreenshot` 使用 `json-index`，索引版本为 `20260625-financial-bda-case-v16`，金融案例结果可见；点击结果可进入 `case-financial-bda-document-automation.html`。
- in-app Browser 复核：案例目录中 `Blueprint 蓝图` 链接在桌面和手机视口下均可滚动到 `#blueprint`，滚动后仍无横向溢出。
- 说明：in-app Browser 截图 API 本轮出现一次 `Page.captureScreenshot` 超时，因此视觉证明改用 DOM、图片自然尺寸、控制台日志、滚动位置和横向溢出数据完成；该超时不来自网站脚本。

### 后续

- 如后续需要加入真实金融样本文档截图，应先脱敏并转为中文业务场景说明；不要放入可读个人、账户、税务或合同敏感信息。

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


## 2026-09-06｜指令与治理范围优化

- 范围：根 AGENTS、网站维护治理与 homepage-v4/v5 原型 AGENTS；保持既有实现、设计选择和生产文件不变。
- 变更：检查按实际改动选择，部署记录放在发布后验证，保留用户审阅所需的预览服务，减少重复澄清。
- 验证：治理文档差异与引用核对；未运行站点构建和浏览器测试，未部署。本次只改变治理文字，不宣称网站功能重新通过验收。
- 后续：具体页面任务仍按受影响行为验证，正式发布使用对应检查和已有授权。

## 2026-09-06｜homepage-v6 参考站 UI 与产品展示迭代

- 范围：独立 `output/homepage-v6`；依据用户指定的 Attio sales-motions、Dataify 页面及 Databricks Governance Hub GIF 重做首页。
- 变更：企业工作总览、Chart.js 趋势和分布、运行分析下钻、能力资产检索、场景侧栏及四列任务看板；任务演示支持复核交接。保留合同原文复核、P&ID 设备关系与三类已有案例入口。CTA 使用产品演示和联系入口，界面及数据明确标为概念演示。
- 验证：构建通过；参考与实现并排实看后调整字号、淡化与锚点偏移。1440 px 桌面和 390 px 手机端无横向溢出；工作流复核交接、合同付款条件确认、工程图缩放至 120% 和上游关系、7 日分析范围、资产空搜索、手机导航及场景切换均完成交互检查，检查末尾浏览器错误/警告日志为空。Vite 有非阻塞的大包体积提示。详情见原型 `design-qa.md`。
- 远程预览：https://6a9c4fe386e46c614cc0ecaf--forflow-enterprise-suite-v3.netlify.app/ 。Netlify `deploy-preview` 已 ready，7 个静态文件 HTTP 200 且与构建产物逐字节一致，带 noindex 响应头。生产部署 ID 前后均为 `6a526ad3f3353819365b175e`。仅上传原型静态构建目录。
- 远程 UI 状态：Chrome 标签清单确认新链接和页面标题；后续浏览器桥超时，未完成部署后的视觉/交互复检，本地已检查的构建与远端文件一致。

## 2026-09-06｜小屏完整产品画面与 3D 能力展示

- 范围：`output/homepage-v6` 独立原型。新增 `ShowcaseViewport`、能力结构 3D 渲染资产及按需加载的 Three.js 模型；产品内部响应式规则改为容器查询，避免小屏把四列流程、原文/字段和图纸/关系拆散。默认完整画面，放大后横向浏览，任务详情自动进入视野，演示状态保留。
- 验证：构建通过；1536/768/390 px 页面无横向溢出，产品保持原生设计布局；手机放大任务交接、关闭后状态保留、文档与工程场景切换、三维分层、旋转、复位、返回渲染图均检查完成。浏览器末尾 error/warn 日志为空。Three.js 按需加载；仍有非阻塞的 Vite 包体积提示。详见 `output/homepage-v6/design-qa-spatial.md`。
- 视觉：生成概念与实现截图均实看对照；精细渲染图用于默认展示，实时模型用于空间结构交互，明确区分两种表现。手机保留完整模型与横向三个层次。页面图为内置 Image Gen 生成，实时模型使用 Three.js。
- 远程预览：https://6a9c56af96fffdb4300e46aa--forflow-enterprise-suite-v3.netlify.app/ 。部署为 deploy-preview，9 个资源 HTTP 200 且与构建产物逐字节一致、带 noindex；生产部署前后均为 `6a526ad3f3353819365b175e`。Chrome 原生远端手机检查确认放大详情可见，已恢复常规浏览视口。

## 2026-09-06｜首页引导与 Q2Q 产品展示

- 范围：独立 `output/homepage-v6`。参考 Attio 的产品菜单、连续场景和滚动定位，以及 Dataify 从产品到优势的首页顺序；新增有说明的导航、三个连续场景、操作提示、场景案例入口和下一步引导。优势区简述业务理解、自研评估与能力积累，保留完整小屏产品画面和 3D 能力展示。
- 来源与边界：核对当前 `/Users/zezhou/Desktop/forflow-q2q` 的 runtime、enterprise console 总览、证据视图及 transport-audit fixture；据此重做事项、证据、版本与复评、能力资产四个视图。另行编写公开展示样例，不含客户原始数据，不将本地实现或概念页面表述为客户生产能力；Q2Q 源库未改动。
- 验证：构建与样例数据关联断言通过；1440/768/390 px 无页面横向溢出，产品内部横向结构保留。产品菜单、场景定位、事项详情、证据筛选与搜索、版本复评、文档确认、手机放大后的任务交接及状态保留、工程关系、优势切换均完成本地浏览器检查，末尾 error/warn 为空。主入口 JS 约 338 KB，3D 按需加载，仍有非阻塞的包体积提示。具体记录见原型 README。
- 远程预览：https://6a9c5eafc7e4b202e0fadc98--forflow-enterprise-suite-v3.netlify.app/ 。Netlify deploy-preview 已 ready，9 个静态资源 HTTP 200、与构建产物逐字节一致且带 noindex；正式部署前后均为 `6a526ad3f3353819365b175e`。
- 远程 UI 状态：Chrome 标签清单确认新链接及标题；浏览器连接反复超时，未完成部署后的视觉与交互复检。已保留远程预览标签并恢复临时视口。本地预览服务继续保留供审阅。

## 2026-09-06｜产品展示文案清理

- 范围：独立 `output/homepage-v6`。按用户反馈，删除工作空间、场景、材料和页脚里的演示数据/样例/概念预览提示；按钮改为确认、交接、更新费率与恢复初始状态等正常产品用语，页面标题同步更新。保留预约演示入口与案例来源归属，原型数据来源留在维护文档。
- 验证：构建通过；HTML/构建脚本与浏览器正文扫描均未发现已删除提示；版本更新后显示“已生成复评任务”，控制台 error/warn 为空，检查视口无页面横向溢出。
- 远程：https://6a9c609dc0e6daff546b59f7--forflow-enterprise-suite-v3.netlify.app/ 已 ready，9 个资源 HTTP 200、逐字节一致并带 noindex。生产部署 ID 前后一致；部署后浏览器导航超时，线上交互未复检。

## 2026-09-06｜Attio 设计系统与产品动效重做

- 范围：独立 output/homepage-v6。以 Attio 当前页面、CSS 和动效实现为参考，统一字体、灰阶、边线、阴影、间距与进入、切换节奏；重建连续产品框架和持续存在的看板卡片，跨列时抬升并带动相邻卡片让位。完善导航键盘与退出行为、工作台引导定位。保留 Q2Q 业务结构、三个业务场景、小屏完整画布和按需三维结构。删除剩余能力示意角标，未恢复演示数据等提示。设计规则见原型 DESIGN-SYSTEM.md。
- 验证：构建与静态资源检查通过；1440/768/390 px 无页面横向溢出。实看首屏、菜单、产品区、卡片移动、文档与工程、优势和三维结构；检查菜单 Escape/键盘焦点、复核交接与状态保留、文档确认、上游关系与 120% 图纸缩放、材料搜索清空、版本复评、工作台引导定位、优势与三维层级切换、旋转、手机导航和放大详情。末尾浏览器 error/warn 为空。样式约 88 KB，Three.js 按需加载且仍有非阻塞大包提示。减少动态效果分支做代码核对，未改动系统偏好。
- 发布：https://6a9cf573843f2c8c5bdf8e3b--forflow-enterprise-suite-v3.netlify.app/ 已 ready，13 个文件 HTTP 200、逐字节一致且带 noindex，正式部署 ID 前后相同。已从公网实看首屏，并执行任务交接，回读“已完成交接”、按钮禁用、卡片进入第四列，页面无横向溢出；浏览器测试视口已恢复。详情见原型 remote-preview.json。

## 2026-09-06｜产品过程演示

- 范围：独立 `output/homepage-v6`。按用户强调的产品演示重点，把三个场景改为有过程、有业务对象变化和操作结果的连续展示：异常关联与交接、合同提取与原文复核、设备关系与检修准备。增加章节、暂停、继续和重播，Q2Q 工作台增加证据与变更的自动讲解。沿用已选定的设计系统及现有优势、案例、三维结构。
- 来源：重新查看 Attio 当前产品流程展示，并核对当前 Q2Q transport-audit 业务对象。合同与关系图为另行编写的公开内容，设备关系不宣称是对已有案例图片的自动解析结果；不导入客户原始数据，说明留在维护文档中。
- 验证：构建通过，CSS 88.99 KB、主入口 JS 347.89 KB；Three.js 独立按需加载，仍有非阻塞包体积提示。1440/768/390 px 无页面横向溢出。已检查业务确认并进入第四列、字段提取暂停与继续、重播重置、原文与字段定位、确认状态、工程关系与清单，以及手机完整结构、放大横向浏览、关闭后保留结果。Q2Q 自动生成复评任务、手动筛选接管播放通过；干净标签执行交接后 error/warn 为空。修复详情对象引用导致的重复渲染、手机放大工具栏高度，以及章节定位被固定导航遮挡；播放计时器保留暂停进度。浏览器临时视口已恢复。
- 发布：https://6a9cfff356bb089123d9b3c6--forflow-enterprise-suite-v3.netlify.app/#workflows 已 ready，13 个资源 HTTP 200、与构建逐字节一致并带 noindex；正式部署 ID 前后相同。先在公网实看并确认合同付款条件，回读确认文案与字段计数；随后仅补定位样式，最终公网回读新 CSS、九个章节、61 px 滚动偏移及零横向溢出。浏览器 AX 连接超时后通过直接浏览器 DOM 接口完成核验。记录见原型 remote-preview.json。

## 2026-09-06｜Q2Q 记录工作空间与中性色

- 范围：独立 `output/homepage-v6` 的 Q2Q 展示。参照 Attio 当前记录表格与侧边操作面板，改为 12 条运输核验记录、侧边复核、45 份材料关联及 4 个资产；按最新反馈统一黑白灰头像、状态与流程图标，仅保留克制的选择和焦点提示。既有三个产品场景、优势与三维结构继续保留。
- 来源：核对当前 Q2Q transport-audit-view-model 的逐单判断、差异、证据与复核结构，另行编写公开展示内容；未复制客户原始资料，未改动 Q2Q 工程库。
- 验证：构建通过，CSS 121.20 KB、主入口 JS 380.38 KB；3D 按需加载，仍有非阻塞包体积提示。数据数量与文件关联断言通过。Chrome 1440/390 px 实看及交互检查覆盖非空意见复核、补证、来源与历史、搜索空结果、筛选、排序、批量分配、规则比较、命令搜索和播放接管。手机无页面横向溢出，内部维持完整布局，放大详情自动进入视野且关闭后保留结果；共用查看器的旧看板详情完成回归，末尾 error/warn 为空。
- 发布：https://6a9d47d74f3ec4a2ea2c279f--forflow-enterprise-suite-v3.netlify.app/#platform 已 ready，13 个有效资源 HTTP 200、逐字节一致且带 noindex，正式部署 ID 前后相同。公网完成填写意见与复核，记录状态、意见及计数 4→3/6→7 同步，头像颜色回读为中性灰，页面无横向溢出。最终发布仅在临时上传目录剔除无引用的系统重复副本，13 个有效资源与已交互检查版本哈希一致。

## 2026-09-06｜Q2Q 彩色头像与协作界面质感

- 范围：独立 `output/homepage-v6/src/q2q-product.css`。根据用户对飞书质感的补充，恢复柔和蓝/绿/紫角色头像；保持白灰工作空间，细化文字对比、表头、边线、选中态、输入焦点与主操作按钮。状态标签维持浅灰底，小点及勾号带少量语义色。
- 验证：构建及入口资源、头像色值、密钥模式和已删除 UI 提示扫描通过。桌面 1440 × 1000 实看并填写复核意见，确认按钮进入可用状态；手机 390 × 844 保留完整原生列结构，放大详情在视野内，页面无横向溢出。无应用错误；一条 Grammarly 扩展日志警告与页面无关。CSS 123.05 KB，主入口 JS 380.38 KB；既有按需 3D 体积提示不变。
- 发布：https://6a9d5452fe2df300f1c23779--forflow-enterprise-suite-v3.netlify.app/#platform 已 ready，13 个资源 HTTP 200、逐字节一致并带 noindex，正式部署未改变。公网回读 12 条记录、蓝/绿/紫柔和头像、浅蓝选中态与最新样式文件，页面横向溢出为 0；临时视口已恢复。

## 2026-09-06｜Q2Q 自动填写与虚拟鼠标流程

- 范围：独立 `output/homepage-v6`。新增 32 秒连续操作：打开差异记录、查看签收回执、逐字填写复核意见、确认并查看活动、回到已完成列表。鼠标按实际界面元素定位，点击反馈与状态变化对应；增加当前步骤、章节、进度、暂停和重播。手动输入、键盘及指针立即接管，保留当前内容。
- 小屏：维持原生横向画布，放大工具栏可暂停，自动跟随当前操作；详情和 380 px 来源弹窗完整进入视野。原业务看板的放大详情完成回归。
- 验证：构建通过，CSS 125.31 KB、主入口 JS 387.03 KB；按需 3D 既有体积提示不变。检查自动来源 238 箱、输入中暂停/继续、手动接管与确认、自动复核 4→3 / 6→7、完成列表 7 条、重播恢复 12 条及 4/2/6。1440/390 px 临时视口容器中无页面横向溢出，手机鼠标和关键按钮在查看器内，关闭放大保留结果；干净重载无新增 Runtime.exceptionThrown。临时检查文件不发布。
- 发布：https://6a9d764405b0a4e0f4c5917c--forflow-enterprise-suite-v3.netlify.app/#platform 已 ready，13 个资源 HTTP 200、逐字节一致并带 noindex，正式部署 ID 前后相同。公网浏览器读到 12 条初始记录及新的三段章节；后续播放检查与恢复标签页均遇浏览器工具超时，未将线上完整交互记为通过。完整流程验证来自本地同构建版本，详见原型 remote-preview.json。

## 2026-09-07｜Q2Q AI 核验与团队协作展示

- 范围：独立 `output/homepage-v6`，新增 AI 核验页、记录协作页及列表入口；连续播放改为 51 秒四段流程。AI 展示材料关联、字段核对、引用结论及可编辑意见；人工确认后创建跟进任务，展示负责人接手和回复，活动记录保留全过程。已复核与协作跟进中分别呈现。
- 来源：核对当前 Q2Q transport-audit-view-model 的结论、证据与人工审核任务结构。AI 过程与角色回复为首页编写的前端场景，未接入模型服务、业务后台或发送真实协作消息；不导入客户原始资料。
- 验证：构建、入口资源、密钥模式和已删除 UI 提示扫描通过；CSS 132.23 KB、JS 401.93 KB，既有按需 3D 提示不变。完整自动流程得到 3/2/7 与协作跟进状态；AI 建议转意见、人工修改确认、创建任务、追加回复通过。1440/390 px 临时视口中无页面横向溢出；手机放大后任务、两条回复、鼠标可见，暂停保留时间，退出放大保留回复并释放滚动，构建产物 error/warn 为空。临时检查服务器与文件在仓库外。
- 发布：https://6a9d93bfb2aa99c402350e39--forflow-enterprise-suite-v3.netlify.app/#platform 已 ready；13 个资源 HTTP 200、逐字节一致且带 noindex，正式部署未改变。线上回读 12 条记录、AI 核验入口与四段章节；线上连续播放回读遇浏览器工具超时，完整流程结果采用本地同构建验证。重播恢复 12 条记录及 4/2/6，清除上一轮跟进任务。

## 2026-09-07｜统一工程知识案例封面

- 范围：独立 `output/homepage-v6/src/App.jsx` 与 `src/site-system.css`。将案例区工程知识的整张 P&ID 缩略图替换为原生设备关系卡片，呈现泵组、上下游设备及图纸依据；沿用相邻封面的白卡、边框、阴影和轻微倾斜，悬停及键盘焦点恢复平直。封面为独立界面插画，案例链接与产品区原图保留。
- 验证：构建与入口资源、密钥模式扫描通过；CSS 134.36 KB、JS 411.26 KB，既有按需 3D 体积提示不变。663 px 三列实看与 390 px 构建产物检查通过：三个封面等高，新卡片无裁切、无页面横向溢出，键盘焦点状态生效，链接仍指向工程案例，浏览器 error/warn 为空。未触发正式站点生成或全站测试。
- 发布：https://6a9d966ad0aeb9e4708eb443--forflow-enterprise-suite-v3.netlify.app/#cases 已 ready；13 个资源 HTTP 200、逐字节一致且带 noindex，正式部署未改变。公网回读新设备关系封面、旧封面图片数量为 0、三个封面高度均为 240 px，案例链接正确，页面无横向溢出。

## 2026-09-08｜GitHub 本地操作入口

- 范围：新增 `.codex/environments/environment.toml` 与 `.codex/scripts/github-workflow.py`，提供 GitHub 状态、上传预检和上传已提交版本三个项目操作。执行时读取当前系统代理；只读瞬时网络故障尝试其他路径，上传固定提交并回读远端，成功后更新本地跟踪状态。
- 验证：本库真实仓库权限、远端读取和上传预检通过；临时本地 bare 仓库验证上传、分叉拒绝、版本校验、响应丢失回读、跟踪状态和大文件阻断；连接切换与 TOML 解析通过。Codex 界面操作被 Computer Use 限制，按钮显示与点击未实测。
- 状态：仅本地工具配置，未上传历史提交、创建 PR 或部署站点；保留原有修改。

## 2026-09-08｜GitHub 操作入口复核

- 修正：非交互上传同时匹配提交 SHA、远程地址和分支；上传前再检查当前分支与远程地址。项目操作命令自动定位 Git 根目录，支持从子目录启动。相关说明明确为本地备用上传通道。
- 验证：临时本地 bare 仓库覆盖 SHA 单独授权拒绝、错分支、错仓库、检查后切换分支以及完整匹配上传与跟踪引用更新，共 5 项通过；Q2Q 和官网均从 docs 子目录执行真实上传预检通过。未向 GitHub 上传提交或修改生产环境。


## 2026-09-10｜原生产品工作空间与 CLI 展示

- 范围：独立 `output/homepage-v6/src/`。Q2Q 首屏改成一个完整窗口，包含任务导航、核验过程、原文与协作侧栏；29 秒连续输入、核验、定位、人工确认与接手。保留完整工作空间并按需加载，新增 21 秒 CLI 输入、执行、结果展示，菜单和场景尾部引导接入 CLI。正式站点生成器及 Q2Q 工程库未改动。
- 设计：遵循用户最新反馈，撤销装饰性纸张、雕塑、摄影背景与悬浮卡片方案；这些生成图片不进入代码或发布包。以 Sana / Attio 的真实界面层级、字体、留白和细边线实现单窗口，CLI 采用终端与结果并排。原文用正常文件预览，差异仅作一处浅色高亮。Inter / Inter Display 搭配 Noto Sans SC 本地变量字体子集，保留官方 OFL 许可。修正中英文字体继承、小屏工具栏换行和内部网格撑高导致顶部栏裁切。
- 来源与边界：核对当前 Q2Q Runner README 和 `run --help`，补齐必需的 `--db` 参数；沿用本站公开编写的运输记录。ForFlow CLI 为官网呈现名称，现有运行入口是 Python Runner；页面日志、文件名、结果与回复为前端编排，不安装 CLI、不执行命令、不调用真实 AI 或发送协作消息，不宣称第三方产品集成已上线。
- 验证：构建通过，CSS 158.46 KB，入口 JS 381.72 KB；完整工作空间分包 65.89 KB，既有按需 3D 分包提示不变。16 个发布资源存在，密钥模式扫描通过，中文字体为有效 WOFF2。1440 px 桌面和 390 × 844 手机实际同源 iframe 视口无页面横向溢出；原文切换与 238 箱定位、人工交接、负责人回复、CLI 结果与依据返回通过。小屏放大保持 1280 px 场景，原文整体自动进入可视范围。修复窗口内部溢出后 scrollTop 为 0，操作区与输入框不重叠。完整工作空间按需加载仍有 12 条记录；最终首屏 1440 × 1250 检查确认中文与英文继承同一无衬线组合、标题字重 500，29 秒后自动呈现接手回复。独立页面 CLI 复制显示「已复制」，error/warn 为空；系统剪贴板字节未核验。减少动态效果下鼠标隐藏；时间冻结的完整检查沿用本轮此前同一播放 hook 的验证。
- 发布：https://6aa293ec483027963e55f665--forflow-enterprise-suite-v3.netlify.app/ 已 ready；16 个资源 HTTP 200、逐字节一致并带 noindex，正式部署 ID 前后一致。公网浏览器回读最新入口资源、单窗口 UI、中文字体与 CLI，页面横向溢出为 0，自动运行后已交接并呈现团队跟进。公网手动定位的浏览器工具最终超时，不将该点击记为通过；完整手动交互采用同构建本地验证。完整回执见原型 remote-preview.json。

## 2026-09-10｜对话与工作成果画布

- 范围：独立 `output/homepage-v6`。依据用户提供的 Sana 报告与代码界面截图，将首屏改为 48 px 图标栏、324 px 对话区和较大的成果画布。新增原生核验报告、报告缩略入口、数量图和报告内复核意见；CLI 加宽结果区并提高关键文字字号。沿用品牌、字体与中性配色，不引入装饰图片。
- 数据与交互：沿用 T-260906-024，图表零基线、长度按 240 / 238 比例绘制，差异单列为 2 箱待核实。报告、原文与协作可切换，查看材料保留交接状态；核验完成前禁用确认。虚拟鼠标改为读取组件实际位置，随视图、缩放及滚动更新。官网的前端呈现边界不变。
- 验证：构建通过，入口 JS 385.03 KB、CSS 169.18 KB，既有 3D 分包提示不变；16 个资源存在、密钥模式扫描通过。1440 px 桌面与 390 × 844 手机实际 iframe 视口检查；手机页面无横向溢出，保留 1280 px 画布。原文 240 / 238 切换、确认后待回应、接手后 16:00 反馈、交接后回看原文不丢状态通过。小屏数量字段与两段协作回复均完整进入可视范围。减少动态效果时定格 29000 ms、停止播放并隐藏鼠标。CLI 的 632 / 556 px 两侧布局无裁切，结果与依据返回通过。最终独立页面 error/warn 为空；临时 iframe 重载出现 MutationObserver 工具日志，独立页面未复现。虚拟鼠标目标坐标与实际按钮中心一致。中文字体补齐新增字符，子集 213,796 字节。
- 对照：保留截图的窄对话、大成果、报告缩略入口、文档层级和引用动作；业务内容使用 ForFlow 核验场景，外部草地和浏览器装饰不移入产品界面。
- 发布：https://6aa29d87a4c494bc44b4bf01--forflow-enterprise-suite-v3.netlify.app/ 已 ready。16 个资源 HTTP 200、逐字节一致且带 noindex；正式部署 ID 保持不变。公网回读最新入口、报告缩略入口与成果画布，三栏尺寸为 48 / 324 / 810 px，自动流程到达 29000 ms 协作状态，页面横向溢出为 0。完整回执见原型 remote-preview.json。

## 2026-09-10｜首屏具体工作轮换

- 范围：独立 `output/homepage-v6/src/HeroHeadline.jsx`、`hero-headline.css` 与 `App.jsx`，同步本地字体子集。参照 Sana 的具体工作轮换与 Dataify 的固定句式，首屏轮换单据核验、合同复核、知识查询、业务跟进，固定「与 AI 一起完成。」与品牌句。4.2 秒停留、520 ms 轻移淡入，保留黑白字体和两行结构；没有加入图片或新依赖。
- 交互：四个简洁选择点、暂停与继续；手动选择接管自动播放。标题离开视野、页面隐藏或启用减少动态效果时停止，减少动态效果仍允许手动选择。标题与产品巡览独立，不重置 Q2Q 工作过程。
- 验证：构建通过，主入口 JS 387.20 KB、CSS 171.93 KB，既有按需 3D 体积提示不变。1440 × 1000、390 × 844 实看，补查 320 px：标题、按钮无裁切，无横向溢出。桌面四项切换时标题高度、固定行、按钮、产品位置逐项相同；自动轮换、手动接管、恢复、减少动态效果及离屏停止通过。「看看它如何工作」仍定位 #platform。保留原字体组合与 500 字重；字体子集 214,620 字节。
- 发布：https://6aa2a1e9be58fa2c6469ac51--forflow-enterprise-suite-v3.netlify.app/ 已 ready。16 个资源 HTTP 200、逐字节一致并带 noindex，正式部署未改变。远程回读四项标题、运行状态、最新 JS 和 #platform 引导，页面无横向溢出。远程新建标签首次超时，恢复已创建标签后 DOM 回读成功。独立本地页面 error/warn 为空；临时 iframe 历史 MutationObserver 工具日志未在独立页面复现。

## 2026-09-10｜首屏原生界面比例与可读性

- 范围：独立 `output/homepage-v6/src/artifact-workspace.css` 与 `WorkspaceReport.jsx`。根据用户对装饰图片的否定及此前 Sana 截图，去掉首屏外层灰色画框，将工作窗口扩大到 1280 × 782；三栏为 52 / 350 / 剩余宽度。报告改为单行标题、36 px 字号与 13 px 正文，加深主体文字，去掉图表与复核意见的嵌套卡片，来源使用单层平面文档，数量条改为中性色。保留既有业务内容、角色头像与巡览逻辑。
- 验证：构建通过，CSS 172.35 KB、入口 JS 387.18 KB，既有按需 3D 提示不变。1280 / 1440 px 桌面与 390 × 844 手机实际浏览器检查，首屏产品图片元素为 0，无页面横向溢出，复核区与输入区不重叠。运输运单 240 / 签收回执 238 切换、人工确认后待回应、负责人接手与 16:00 回复通过。修正来源字段宽度后，手机放大数量字段与两段回复全部进入视口，保留完整横向结构。
- 发布：https://6aa2a50748368b5b47ebe64d--forflow-enterprise-suite-v3.netlify.app/#platform 已 ready，16 个资源 HTTP 200、逐字节一致并带 noindex；正式部署未改变。远程回读最新 JS、1280 × 782 窗口、52 / 350 / 876 三栏、0 图片、0 页面横向溢出，自动流程到达 29000 ms。公网手动切回报告工具超时，未记为通过，交互验证采用同构建本地结果。独立本地页面 error/warn 为空。

## 2026-09-10｜首屏工作空间可操作化

- 范围：独立 `output/homepage-v6`。重写 `WorkspaceStory.jsx`，新增 `WorkspaceSurfaces.jsx`、`workspace-state.js`、`q2q-analysis.js` 与 `operable-workspace.css`，补齐字体子集。首屏为 1280 × 820 原生窗口，54 px 导航、304 px 对话和右侧记录详情。列表、核验、来源、协作及历史均直接可操作；旧完整工作空间源码保留，顶部标题轮换、三个场景、CLI 和其他首页内容不变。
- 交互：12 条独立记录支持搜索和组合筛选，数量字段定位原文；AI 按当前记录整理回复、来源及复核草稿。支持编辑意见、分派负责人、设置反馈时间、确认交接、更新任务进度与评论。空意见不能确认，缺少回执的记录只能安排补证；任务没有回复时不能完成。活动追溯对应本次动作，sessionStorage 保留同一标签页刷新状态。32 秒巡览复用同一状态转换，手动接管后保留自己的操作，重播不覆盖手动会话。
- 边界：官网前端交互原型，沿用公开编写记录与结构化材料，AI 使用记录规则和请求意图，无真实大模型或生产后端调用、无外部消息发送。未改 Q2Q 工程库或正式网站生成入口，未加入图片。
- 验证：7 项状态测试通过，构建通过。浏览器检查搜索、空结果、材料定位、AI 草稿、人工修改、交接、任务状态和评论、记录隔离、缺件限制、刷新恢复及减少动态效果。修复 WebKit 时间输入未触发状态更新造成回退的问题。1440 × 1100 与 390 × 844 视口无页面横向溢出；手机放大数量字段位于 16.15–373.52 px，完整落在 10–379.90 px 可视范围。干净独立页面 error/warn 为空。CSS 196.49 KB、入口 JS 412.12 KB，既有按需 3D 提示不变。
- 发布：https://6aa2abf096007425a04f0b1b--forflow-enterprise-suite-v3.netlify.app/#platform 已 ready。15 个资源 HTTP 200、逐字节一致并带 noindex，正式部署未改变。公网回读 1280 × 820 工作窗口、6 个可编辑控件及巡览完成后的复核、任务和评论；实际点击记录列表，回读 12 行，首条保留已复核及处理中。旧回执已备份，最新记录见原型 `remote-preview.json`。


## 2026-09-10 · 首页首屏改用 demo video 的 ForFlow One 源工作台

- 范围：独立原型 `output/homepage-v6`。直接复用 `demo video/product_launch_fragments/workbench` 的 15 个源文件，恢复工作流、知识与规则、AI 资产、项目及数据治理层级。Q2Q review 归于 Knowledge & rules。源工程没有修改，历史运输方案保留。
- 实现：原四步续约流程及右侧配置面板；46 秒巡览直接调用原工作台动作，支持暂停、章节与点击接管。存储隔离、字体回退和展示外框为本次适配；未增加生成图片或后台调用。独立工作台可操作并保存当前会话。
- 验证：源文件 SHA256 与资源引用校验、Vite 构建通过。浏览器检查自动与手动审核、范围确认限制、8/8 流程检查和 5/5 内容检查、资产登记与 Evidence、刷新恢复、角色与节点切换、重播。1440 × 1100 / 390 × 844 视觉检查通过；手机页面 clientWidth/scrollWidth 均为 390，源侧栏仍为 208 px，放大可横向浏览。独立工作台及干净公网首页错误日志为空；QA iframe 外壳存在此前的 MutationObserver 记录。
- 远程：draft `6aa2b1d19730ba2c12438c6a` ready；34 个文件 HTTP 200、逐字节一致且带 noindex。正式部署前后均为 `6a526ad3f3353819365b175e`。公网完成资产 Evidence 回读，并在点击 Workflow studio 后回读四个续约节点与 Business approval 配置。合并读取工具超时后，重连单项读取成功。
- 预览：https://6aa2b1d19730ba2c12438c6a--forflow-enterprise-suite-v3.netlify.app/#platform 。回执与来源见原型内 `remote-preview.json`、`workbench-source-manifest.json`。本次 8898、8899 临时服务已结束，远程预览标签保留。


## 2026-09-10 · 首页标题固定句前置

- 独立原型 `output/homepage-v6/src/HeroHeadline.jsx`：第一行“与 AI 一起完成”，第二行轮换“业务跟进 / 合同复核 / 知识查询”，同步按钮与可访问名称。
- 验证：构建通过；浏览器回读标题顺序、当前合同复核状态，DOM 几何确认固定句位于轮换词上方。Netlify draft `6aa2b4b13a81cc4881b757d5` ready，34 个文件 HTTP 200、逐字节一致且带 noindex，正式部署未变。新远程预览打开成功。
- 预览：https://6aa2b4b13a81cc4881b757d5--forflow-enterprise-suite-v3.netlify.app/ 。本机 8898 预览服务已恢复并保持运行。


## 2026-09-10 · 首页业务文案与操作引导优化

- 范围：独立原型 `output/homepage-v6` 的 8 个 React 组件，统一首屏说明、工作台字幕、三个业务场景、CLI、优势、能力资产、案例与联系入口。以订单卡点、合同条款、设备连接和检修准备替换泛化表达，保留用户确定的首屏标题顺序。重建本地中文字体子集，未更改 CSS 和源工作台。
- 验证：Vite 构建通过；桌面 1440 × 1100 检查工程知识标题和段落，通读全部六个营销主标题；手机 390 × 844 页面宽度与 scrollWidth 均为 390，工程知识加入检修准备后显示清单。合同字段复核、确认、点击撤销均通过。主 JS 364.70 KB，CSS 174.23 KB，既有 3D 包提示不变。
- 发布：Netlify draft `6aa2bf3fe767a8de512b7376` ready；34 个资源 HTTP 200、逐字节一致且带 noindex。部署状态读取曾遇到 429，继续核验同一部署，没有重复发布；最终确认正式部署 ID 仍为 `6a526ad3f3353819365b175e`。公网已回读工程知识标题与说明。回执见 `output/homepage-v6/remote-preview.json`。
- 预览：https://6aa2bf3fe767a8de512b7376--forflow-enterprise-suite-v3.netlify.app/#scenario-2 。8898 原有预览服务保持运行。


## 2026-09-10 · 首屏补充一句话公司说明

- 在独立原型 `output/homepage-v6/src/HeroHeadline.jsx` 的主标题下，改用“ForFlow 帮助企业把 AI 用进业务流程，解决具体问题，并把有效方法沉淀为可复用的能力。”说明公司在做什么；保留现有标题与轮换顺序。表述参考当前公司背景中的业务价值与能力积累方向。
- 验证：构建通过；手机 390 × 844 浏览器回读完整说明，页面 clientWidth 与 scrollWidth 均为 390。字体子集同步生成，未修改样式或工作台逻辑。
- Netlify draft `6aa2c7bd228fdff785fe255f` ready，34 个文件 HTTP 200、逐字节一致且带 noindex，正式部署保持 `6a526ad3f3353819365b175e`。新预览已打开：https://6aa2c7bd228fdff785fe255f--forflow-enterprise-suite-v3.netlify.app/ 。回执见原型 `remote-preview.json`。


## 2026-09-11 — 独立首页预览：Sana 产品界面细节

- 范围：仅 `output/homepage-v6`。细化业务协同、合同、工程知识和 CLI 的工具栏、内容画布、来源/状态、切换控件与操作反馈；新增合同复核记录、任务处理记录、工程图纸回看和撤销加入检修。首屏文案及真实 ForFlow One 层级保留。
- 维护入口：`src/ProductDemos.jsx`、`BusinessBoard.jsx`、`CliShowcase.jsx`、新 `ProductDetailUI.jsx` 和 `product-detail-refinements.css`；刷新中文字体子集并构建。仅展示层状态，不接入外部服务。
- 验证：构建通过；1440 × 1100 / 390 × 844 无页面横向溢出，手机放大后合同侧栏 29.50–379.10 px、CLI 结果 20.05–369.65 px。合同定位/确认/撤销/记录回看、协同列表筛选/交接/记录、工程选中/回图/缩放/撤销准备、CLI 标签和复制通过。15 个源工作台文件校验一致。独立页面 error/warn 为空；QA 视口壳出现的 MutationObserver 错误未在干净页面复现。
- 远程：https://6aa2d722e052c7a15223f1bf--forflow-enterprise-suite-v3.netlify.app/#scenario-1 ，Netlify draft ready；34 个文件 HTTP 200、逐字节一致且带 noindex。公网回读新字段与来源界面；最后确认/记录序列工具超时，仅记本地流程通过。正式部署保持 `6a526ad3f3353819365b175e`。回执为 `output/homepage-v6/remote-preview.json`；上一版回执已归档。


## 2026-09-11 — 独立首页预览：操作衔接与微文案

- 维护入口：`output/homepage-v6/src/ProductDemos.jsx`、`BusinessBoard.jsx`、`ProductDetailUI.jsx`、`CliShowcase.jsx`、`ScenePlayback.jsx` 与 `product-detail-refinements.css`。补合同下一待复核项/独立撤销/完成与空状态/方向键；补协同筛选清除、等待图标及交接文案同步；工程准备按设备保留、缩放重置；CLI 完整命令复制反馈、播放状态与图标提示。
- 验证：构建、字体子集、15 个源工作台清单校验通过；1440 × 1100 / 390 × 844 无页面横向溢出，手机确认操作 46.77–362.54 px。5 项合同复核完成、下一项、撤销、键盘切换、协同筛选空状态、两个设备准备跨视图保留/单独撤销、缩放边界/重置、CLI 完整命令复制通过；干净独立页面 error/warn 为空。复制失败回退已实现，未人为触发验证。
- 远程：https://6aa2da15e052c7c24823f215--forflow-enterprise-suite-v3.netlify.app/#scenario-1 。Draft ready；34 个文件 HTTP 200、逐字节一致、noindex；正式部署保持 `6a526ad3f3353819365b175e`。公网新提示已回读，确认工具调用超时，因此仅记本地交互通过。上一版回执已归档，新回执与 README 已更新。


## 2026-09-11 — 独立首页预览：搜索与连续查看

- 维护入口：`output/homepage-v6/src/BusinessBoard.jsx`、`ProductDemos.jsx`、`ShowcaseViewport.jsx`、`App.jsx` 与 `product-detail-refinements.css`。增加搜索/计数/筛选组合、任务前后导航与焦点返回、分层 Esc、设备连接高亮和图例、移动端平移边界提示。手动搜索暂停自动播放，避免观看内容被推进。
- 验证：构建通过，字体子集 716 字符，15 个源工作台文件一致。1440 × 1100 / 390 × 844 检查搜索、空状态、切换保留条件、侧栏导航、案例→侧栏→放大界面分层关闭、焦点与滚动锁、工程连接高亮、平移终点禁用及全貌隐藏控件；手机页面无横向溢出，干净独立页面 error/warn 为空。
- 远程：https://6aa413deabd8ddec7da50a6d--forflow-enterprise-suite-v3.netlify.app/#scenario-0 。Draft ready；34 个文件 HTTP 200、逐字节一致且带 noindex，正式部署仍为 `6a526ad3f3353819365b175e`。公网回读任务数和详情位置通过；搜索占位符的后续工具读取超时，未声称公网交互通过。回执与 README 已更新，上一版回执归档。8898 本地预览已恢复并保持运行。


## 2026-09-11 — 独立首页预览：生图人物素材与协作细节

- 范围仅 `output/homepage-v6`。内置 image_gen 生成四张自然光角色头像，原图和提示词存于 `design-assets/people-v1/`，网页使用 128 px PNG，合计 104,115 字节。新增 `HumanDetails.jsx` / `human-details.css`，接入负责人、协作分工弹层、原文复核标记、处理记录与交接回执。确认/撤销驱动对应标记，动效支持 reduced-motion；不改源工作台层级，不触发真实后台操作。
- 验证：构建通过，15 个源工作台文件校验一致；1440 × 1100 / 390 × 844 的头像加载、弹层关闭、Esc 分层、合同确认/撤销/记录、业务交接、工程准备通过。修复弹层层级和重复交接提示；手机合同操作 46.77–362.54 px、页面 client/scroll width 均 390。干净独立页面 error/warn 为空。系统 reduced-motion 未主动切换，仅核验样式。
- 远程：https://6aa41723f4b5f503515f2337--forflow-enterprise-suite-v3.netlify.app/#scenario-1 。Draft ready；38 个文件 HTTP 200、逐字节一致且带 noindex，正式部署仍为 `6a526ad3f3353819365b175e`。公网导航完成，后续头像 DOM 读取超时，仅将交互记为本地验证。新回执、素材清单和 README 已更新，上一版回执归档；8898 预览服务保持运行。


## 2026-09-11 — 独立首页预览：产品展示版式与设计完成度

- 用户澄清“活人感”为专业 UI 审美。仅调整 `output/homepage-v6`：将占 25% 宽度的侧栏改为横向粘性章节，将标题与说明拆为清晰层级，给完整工作台统一展示底框；收紧合同画布与字段行高，统一选中状态、播放条、按钮与案例引导，原文人物浮标改为来源标记。入口为 `src/App.jsx`、`HumanDetails.jsx`、`main.jsx`、新 `product-editorial.css`。
- 验证：构建、字体子集与 15 个源工作台清单通过。Chrome 实际 1440 × 1000 / 390 × 844 的布局、章节选中、合同确认/撤销、任务搜索/交接、工程关系图通过，console error/warn 为空。桌面字段侧栏 client / scroll height 均 657，手机确认区 53.18–355.86 px、侧栏宽 349.6 px；两尺寸无页面横向溢出。测试视口已恢复。首屏真实工作台文件与业务操作保持不变。
- 远程：https://6aa41973bd3e6d164162923c--forflow-enterprise-suite-v3.netlify.app/#scenario-1 。Draft ready；38 个文件逐字节一致、HTTP 200、noindex，正式部署仍为 `6a526ad3f3353819365b175e`。公网导航返回，后续 DOM 读取超时，仅记本地交互验证通过。回执及 README 已更新，上一版回执归档，8898 服务保持运行。


## 2026-09-12 — 独立首页预览：滚动交互与字号细化

- 范围仅 `output/homepage-v6`。新增 `ProductSceneNav.jsx` / `motion-type.css`，调整 `ui-motion.js`、`App.jsx` 与 CSS 引入：分层、一次性入场，原生滚动驱动章节滑动指示与阅读进度，统一按钮/确认/交接反馈；放大说明与摘要，保持现有工作台层级和横向展示。
- 验证：构建通过；Chrome 实际 1440 × 1000 / 390 × 844 页面无横向溢出，桌面标题/说明/正文为 42 / 16 / 14 px，手机为 30 / 14 / 12 px。上下翻页选中与已读内容稳定、全屏尺寸、合同确认/撤销、业务交接通过；页面级 reduced-motion 仿真通过并恢复，测试视口已恢复，控制台 error/warn 为空，15 个源工作台文件哈希一致。
- 远端：https://6aa4290cb2742a2e5b890df0--forflow-enterprise-suite-v3.netlify.app/#scenario-1 。Draft `6aa4290cb2742a2e5b890df0` ready，38 个文件 HTTP 200、逐字节一致且 noindex；正式部署仍为 `6a526ad3f3353819365b175e`。本轮未重复公网浏览器交互，以本地交互与公网资源回读分别记录。README 与回执已更新，上一版回执已归档，8898 服务保持可用。


## 2026-09-12 — 独立首页预览：专业产品播放与操作引导

- 范围仅 `output/homepage-v6`。参考 Databricks 官方页面结构及用户提供的 17.23 秒治理动图；官网实时浏览器回读超时，没有声称复现其确切播放逻辑。新增统一 `usePlaybackClock.js`、`ProductPlaybackGuide.jsx` 与 `playback-refinements.css`，接入首屏/业务场景/CLI，统一时间、进度、提取扫描、离屏暂停续播及手动接管；三段业务流程增加指针、点击和最终结果停留。
- 验证：构建、15 个源工作台文件哈希一致；Chrome 1440 × 1000 / 390 × 844 截图与交互通过。合同暂停 5500 ms 时字段数与进度保持，离屏 3602 ms 保持并续播，手动章节切换在往返后仍暂停。合同 14900 ms 完成一项复核，业务 15500 ms 完成交接，工程 14000 ms 加入准备。手机页面无溢出、放大/撤销，首屏就绪后播放/暂停，CLI 命令与结果通过；reduced-motion 仿真与视口已恢复，console error/warn 为空。
- 远端：https://6aa42f1e50d7dc5f778fdf17--forflow-enterprise-suite-v3.netlify.app/#scenario-1 。Draft ready；38 个文件 HTTP 200、逐字节一致且 noindex，正式部署保持 `6a526ad3f3353819365b175e`。实际交互在本地验证，公网资源单独回读；README 与回执更新、上一版归档，8898 服务保持可用。


## 2026-09-12 — 独立首页预览：手机滑动播放与文字排版修复

- 用户在上一版发现打开即跳文档章节、滚动未播放和 iPhone 16 Pro Max 叠字。纠正交付链接带 `#scenario-1` 的做法，首页预览使用无锚点根链接。保留网站内部章节锚点。范围仅 `output/homepage-v6`。
- 实际复现首屏桥接和业务展示在 pointerdown 时误暂停；改为点击具体控件或键盘操作才接管。触摸滑动不暂停，原来的离屏暂停/返回续播和手动暂停仍保留。手机工作台与 CLI 播放条采用三个独立章节列和下排控制，标题切换先退后入；父页面与嵌入框架设置 100% text-size-adjust，避免移动端自动放大固定 UI 文字。
- 入口：`src/ProductDemos.jsx`、`ScenePlayback.jsx`、`ShowcaseFilmUI.jsx`、`design-tokens.css`、`hero-headline.css`、`playback-refinements.css`，以及展示适配层 `public/workbench/showcase-bridge.js` / `showcase.css`。
- 验证：构建通过；15 个源工作台文件哈希一致。Chrome 1440 × 1000、440 × 956、390 × 844 检查；手机模式完整触摸手势从工作台滚入业务/合同/工程自动播放，合同画面上滑后时间从 551 ms 继续到 1301 ms；手动章节暂停在上下滚动后仍为 3000 ms。手机标题/章节/字段没有横向文字溢出，440 px 放大合同确认按钮在 103.18–405.86 px 内，确认成功。源工作台点击接管与重播恢复、reduced-motion 通过，控制台无 error/warn，测试设置已恢复。iOS Safari 实机未测。
- 远端：https://6aa4cf937b730691532ec80a--forflow-enterprise-suite-v3.netlify.app/ 。Draft ready，38 个文件 HTTP 200、逐字节一致且 noindex；正式部署仍为 `6a526ad3f3353819365b175e`。远端浏览器回读超时，实际交互仅记本地验证；README 和回执已更新，旧回执归档，8898 预览保持运行。


## 2026-09-12 — Dataify 对照与大陆客户表达校准

- 用户明确首页面向大陆客户，要求继续参考 Dataify。已把目标受众与参考范围记入独立原型 AGENTS.md，本轮为内容与路径检查，未改页面或发布。
- 读取 Dataify 当前官方首页的产品分类、解决方案、接入、安全说明及电话/微信咨询入口；浏览器捕获超时，没有声称观察了其实时动效。对照当前首页代码，后续优先项为真实工作台中文化、区分产品与应用场景、补齐实际接入/交付说明和咨询路径。
- 实测 https://forflow.ai/contact 返回 HTTP 200，但最终地址为 /landing.html?next=%2Fcontact，标题为受邀访问；目前预览中的预约按钮统一指向该路径。此为当前可复现的访客障碍，未更改正式站门禁。
- 当前两张展示 PNG 合计 2,545,729 字节，其中工程图纸未设置延迟加载；大陆网络和微信浏览器体验仍需专项实测。对照依据：https://www.dataify.com/ 。仅文档校准，无全站构建或部署。


## 2026-09-12 — 独立首页预览：预约恢复、中文工作台与完整案例索引

- 范围为 `output/homepage-v6`；正式站生成入口与业务模型保持不变。导航、首屏和案例预约统一接回历史 Git 提交 `65c839f` 中的飞书需求表，增加明确的填写需求→联系确认安排说明、邮件入口与复制状态。公开 HTTP 元数据可用；未提交线索，飞书浏览器捕获超时。
- 沿真实 demo video 工作台增加 `showcase-zh.js` 显示层，覆盖主流程标签、状态、角色、表单说明与日期；保留原字段值、业务模型、引用原文与 action ID。自动演示期间抑制主动聚焦，修复首屏/案例浏览被拉回工作台；手动操作仍保留焦点行为。
- 三个原有案例改为页内详解，并补回用户指出的汽车 B 柱 DFMEA。`scripts/sync-case-catalog.py` 从 `build_site.py` 的 `CASE_LIBRARY_ITEMS` 生成15条预览目录及 `docs/maintenance/case-catalog.md`，支持搜索、分类、空状态；原文入口沿用既有地址和访问权限。用户确认事项已写入本地 `forflow-website` 工作上下文、原型 AGENTS 及 Codex 记忆更新笔记；本轮未执行 GitHub commit/push。
- 验证：桌面及440×956/390×844设备模拟；新页 scrollY=0，手机无横向溢出，触摸滑动后自动播放继续，案例筛选/空状态/切换/Esc焦点返回和独立触摸滚动、联系邮箱复制通过。中文工作台提取、复核、5/5内容检查、8/8工作流检查、1.0.0登记与依据页通过；中文筛选保留 `All checks`/`Failed` 原值。构建、4项Sites打包检查、JS语法、差异空白检查和15条来源/副本哈希校验通过。只观察到无关Grammarly扩展消息；iOS Safari实机未测。
- 远端：https://6aa4e4e37c82178a5644dee6--forflow-enterprise-suite-v3.netlify.app/ 。Draft ready；39个文件和根入口HTTP200、逐字节一致且noindex；正式部署仍为 `6a526ad3f3353819365b175e`。本地交互与远端资源核验分别记录于 `mainland-preview-qa.json`、`remote-preview.json`；旧回执归档，8898服务保留。


## 2026-09-12 — 独立首页预览：Attio / Sana 局部视觉微调

- 按用户指定只做局部优化；通过 Chrome 原生截图观察 Attio 首屏与场景结构、Sana 轮换标题与产品窗口。网页自动捕获接口超时，原生截图成功。保留真实工作台、产品交互和已有业务内容；未新增生图资产。
- 入口为 `output/homepage-v6/src/HeroHeadline.jsx`、`hero-headline.css`、`source-workbench.css`、`product-editorial.css`、`motion-type.css` 与 `site-system.css`。调整中文标题字重/字距、简化辅助说明、统一主次按钮，首屏工作台改为1280px外框与轻中性背景，场景灰阶和圆角收紧。
- 验证：构建与4项Sites检查通过；15条真实工作台来源/副本哈希不变。1440×1000、440×956、390×844无页面溢出，手机标题无横向溢出；工作台46秒巡览到资产登记、合同自动完成1/5复核，手机放大保持1440px原生宽度，关闭、重播及触摸滑动保留tour通过。字体可变范围100–900，首屏与工作台文案无缺字；应用控制台无error/warn。iOS Safari实机未测。详见 `visual-refinement-qa.json`。
- Drive 已回查私人 ForFlow Memory Hub 和00入口，作为可复查资料索引；留档邮箱已向用户询问，尚未发送邮件。远端：https://6aa4e921983dd2411a1fe8f9--forflow-enterprise-suite-v3.netlify.app/ 。Draft ready，39个文件HTTP200、逐字节一致且noindex，正式部署保持 `6a526ad3f3353819365b175e`。回执已更新，上一版归档，8898服务保留。


## 2026-09-12 — 独立首页按 Attio 实测细化

- 依据用户“还是有点简陋，像素级学习attio”的纠正，截图并读取 Attio 公开样式；独立原型采用 24 列贯通栅格、1/4 固定目录、36px 主按钮和淡色竖纹。中文场景标题由 42px 调整为 26px，产品展示改为共享边线，保留 demo video 工作台层级。入口为 `output/homepage-v6/src/attio-fidelity.css` 及对应 React 组件。
- 修正横竖目录指示测量、章节锚点重复页头偏移，放大组件增加占位和阅读位置/焦点恢复。实测手机关闭前后 scrollY 均 2191.71，目录仍为文档处理。
- 本地构建、4/4 Sites 打包检查、git diff --check、15/15 工作台源和适配副本哈希通过。1440×1000、1316×635、440×956、390×844 检查无页面横向溢出；进入视区自动播放、下一合同字段与原文联动、放大、平移、返回已测试。iOS Safari 实机与触摸未测。
- 预览 https://6aa520f0f0b7211b123168d8--forflow-enterprise-suite-v3.netlify.app/ ，draft ready，39 文件 HTTP200、逐字节一致、noindex；正式部署仍为 `6a526ad3f3353819365b175e`。远端控制台 error/warn 空，远端截图超时；视觉与交互结论来自同构本地构建。上一回执归档，当前回执/README/设计 QA/项目反馈均已保存。本轮没有 Git commit/push、邮件发送或 Drive 写入。


## 2026-09-12 — 独立首页下半部分与交互细化

- 用户指定优化下半部分。范围仅 `output/homepage-v6` 的 CLI、优势、能力资产、案例与联系页脚；新增 `src/lower-editorial.css`，统一贯通边线、字号、控件与案例封面。CLI 改为左命令/右结果窗口并使18.9s虚拟点击实际展开核验依据；能力层级支持键盘切换；预约保留飞书需求表并说明后续联系步骤。
- 手机章节与播放控制分行，完整横向工作台仍可放大/平移；440px放大结果宽386.4px、视窗418px。1440×1000、440×956和390×844无页面溢出，章节锚点偏移修正；触摸上滑80px保持播放。CLI复制/自动依据、优势切换、模型加载/键盘、15案例/B柱搜索/弹窗/Esc、联系邮箱复制通过。构建、4/4打包检查、15/15工作台源与副本哈希、git diff --check与凭据模式扫描通过；本地console error/warn为空。
- 预览 https://6aa52ce8d8321b545c1145e1--forflow-enterprise-suite-v3.netlify.app/ ，draft ready，39文件HTTP200、逐字节一致且noindex；正式部署保持 `6a526ad3f3353819365b175e`。远端浏览器更新URL/标题但截图/DOM超时，实际视觉与交互仅记本地通过，iOS Safari实机未测。QA/README/项目反馈已保存，旧回执归档；临时浏览器视口已恢复、测试页关闭，8898服务保留。


## 2026-09-12 — AI 治理产品研究、独立展示与交流模板

- 用户请求研究 Holistic AI 和 a16z 投资的 Neo，结合 Q2Q 形成偏差、幻觉、噪音三类能力，在 AI 资产之后新增独立板块；随后明确按既有关系配合展示、做可替换模板。第一层改为检查对象、配合方式与交付，采购口径留在内部研究。核对客户侧 Caseware、公示采购与当前 Q2Q 代码，确认 Neo 为 neo.ai；保留原完整竞品研究，不把他人客户或尚未接入的引擎能力写成已有交付。
- 范围仅 `output/homepage-v6`：新增治理工作台、`/ai-governance.html` 独立方案及 `/ai-governance-brief.html` 编辑模板。三类能力包含四个视图，支持选行、筛选、依据、整改复测、键盘和自动播放；工作台维持1280×646原生构图，手机可放大查看。模板可改单位、场景、问题和正文、保存独立HTML或浏览器打印；修复下载包含扩展注入DOM问题。研究与交流稿、项目有范围反馈已保存。
- 验证：构建、4/4打包检查、15/15源工作台/副本哈希、中文缺字与凭据扫描通过；Chrome 1440×1050/440×956/390×844无横向溢出，349.6px手机侧栏、交互和减少动态效果通过。实际下载回读保留修改且无Grammarly注入；打印CSS已检查，未生成PDF。没有实际引擎调用、iOS真机或本轮触摸手势验收；应用无error/warn，编辑页有无关扩展消息。
- 远端 https://6aa537bee275bb8affc7c7d4--forflow-enterprise-suite-v3.netlify.app/ ，draft ready，41资源HTTP200/noindex，40字节一致，1个仅为已验证的Netlify Pretty URLs链接改写；干净方案路径已核验。正式部署保持 `6a526ad3f3353819365b175e`。本地视觉交互和远程资源回读分别记录；QA/README/回执更新，旧回执归档，浏览器测试设置恢复、本次测试页关闭，8898服务保留。未执行Git push、邮件或Drive写入。


## 2026-09-12 — 补齐业务上下文、连接器与重点案例展示

- 用户指出后半段与连接器展示不足，附 Attio 四张参考。核对原有资产、治理与案例仍在；在独立 `output/homepage-v6` 新增深色上下文章节和六类来源连接器，案例改为 B柱/供应链/合同/工程知识四个可切换大幅图文。保留3个产品场景、CLI、资产、治理、15条案例及飞书预约。
- 连接器参照真实 demo 的来源/数据表/对象/流程层级，字段、业务关联与权限可切换；完整1280×590窗口支持手机放大和横向浏览。没有新增真实系统接入或品牌连接器承诺。复用原网站案例配图转WebP，共287600字节；补齐字体字符，提高文字对比度。缺失图标导入导致的初次渲染错误已修复并重建。
- 构建、4项打包检查、15/15工作台源与副本哈希、凭据模式扫描和diff检查通过。1440×1050、440×956、390×844无页面溢出；放大侧栏329.36px，横向控制、触摸能力条滚动306px、字段/权限/关联、案例检索与详情、自动推进及减少动态效果已测；首次根入口scrollY=0，最终本地error/warn空。iOS实机和本轮键盘自动化未完成。
- 预览 https://6aa53fe6e0de31148f1ee7ef--forflow-enterprise-suite-v3.netlify.app/ ，45资源HTTP200/noindex；44个逐字节一致，1个仅为已验证的Pretty URLs链接改写，生产部署`6a526ad3f3353819365b175e`保持。远端浏览器导航和恢复超时，不记为远端视觉通过。详见`connectors-context-qa.json`与`remote-preview.json`；旧回执归档，项目反馈回读通过，8898保留。未执行Git commit/push、正式站发布或外部消息发送。

## 2026-09-12｜homepage-v6 连续版式与 UI 一致性修正

- 反馈对象：6aa53fe6 预览；用户指出页面断层，以及新增 UI 与上半段不一致。
- 修正：上下文从独立黑色大首屏改为相同的白底标题与交互图；上下文、连接器、治理与原页面共用外框断点；下半段文字和控件统一灰阶。入场动画不再隐藏整块内容，连接器详情避免裁切。
- 实际验证：构建、4 项打包检查通过；390–1600px 共 12 档外框 / 接缝 / 横向溢出检查通过；16 屏连续滚动内容可见；6 类连接器、权限视图、手机详情、键盘切换通过。远程 45 资源均 200 / noindex 并核对正文。远程浏览器自动回读超时，视觉为同一构建本地 Chrome；未验证 iOS 实机。
- 预览：https://6aa571cdfa3641ac3084ecc1--forflow-enterprise-suite-v3.netlify.app/ 。生产版本未变。证据：output/homepage-v6/continuity-qa.json、remote-preview.json。

## 2026-10-07 — Qoder 参考的局部能力动效

- 用户选定 Qoder 的模型/Harness/电脑操控卡片组。通过实际页面截图与样式读取，参考480ms胶囊过渡和有停留的光标/选区节奏；只调整独立 `output/homepage-v6` 的优势区，增加资料关联、Q2Q步骤展开、条款划选与保存反馈。入口为 `Advantages.jsx`、`method-motion.css`、`useAmbientSequence.js`。原工作台、连接器、资产、治理、案例和联系均保留。
- 支持视区自动播放、离屏/隐藏页面暂停、点击接管与全组继续；减少动态效果显示完成状态。手机横向卡片保留原生小界面及放大返回。无新增生成图或第三方图像，展示状态不代表在线系统接入。
- 实测：构建和4/4打包检查通过；IAB桌面1440×1000及手机440×956/390×844无页面横向溢出、标题与界面无重叠；步骤切换、保存、自动推进、离屏暂停、放大返回、减少动态效果通过，error/warn为空。20个原工作台发布文件哈希保持；5个本机云端占位素材按上版SHA256恢复。本轮未测iOS真机和触摸手势。正式站静态检查另有旧 `workbench_prototype.html` 结构失败，与本次独立原型无关，未修改该页。
- 远程预览 https://6ac53cbc1f7b6dd9fd07650e--forflow-enterprise-suite-v3.netlify.app/ ：draft ready；45资源200/noindex，44逐字节一致，1个仅为Netlify已核实的链接/引号改写。远端首次打开在hero，3卡片/10章节/保存反馈已回读；生产版本未变。回执和上版归档已保存，局部反馈沉淀于原型AGENTS.md；本地8898静态预览保持。未推送Git、未发送邮件或写入Drive。

## 2026-10-08 — Q2Q 交互概览与修订对比

- 用户指定 OpenAI GPT-6 / Intelligent UI 页面，并要求部分1:1复刻。仅在独立 homepage-v6 治理部分新增场景胶囊、问答到图表的展示、版本切换和原文依据联动；原评估工作台、连接器、资产、15案例与预约入口全部保留。入口为 EvaluationCanvas.jsx / evaluation-canvas.css / GovernanceSection.jsx。
- 图表来自现有 authored walkthrough 记录，未新增客户成绩。修订后点击柱条仍保留比较值；手动操作同步播放章节；展示模式变化后重新观察画布，避免换回工作台后无法播放。
- 相同package-lock的项目外暂存构建通过，Sites 4/4；原目录iCloud占位导致初次构建阻塞，公开占位素材在暂存目录按上一回执SHA256恢复，输出同步回dist。20个原工作台发布文件哈希保持，案例15条。1440×1000、440×956、390×844无横向溢出；82/74到80/80、证据高亮与数值保留、P-041/S-071记录定位、三次补证复测、播放/离屏暂停、减少动态效果和手机放大平移/返回通过，console error/warn空；iOS实机及本轮触摸未测。
- Draft https://6ac76b7c397123c707404c46--forflow-enterprise-suite-v3.netlify.app/ ready，45资源HTTP200/noindex，44字节一致，1个仅有已验证Netlify链接改写；B柱图首次网络回读不完整，重试哈希一致。生产部署保持6a526ad3f3353819365b175e。远端浏览器导航超时，远端渲染不计通过；原页精确样式/动画与逐像素比对未完成，不声称1:1。截图在 /private/tmp/forflow-intelligent-ui-qa/，回执与上版归档已更新。本次未commit/push、未发送邮件或写入Drive。

## 2026-10-08 — homepage-v6 阅读衔接与案例检索

- 用户认可当前方向并允许继续改善UX。保持既有视觉与全部章节；治理概览/工作台往返保留比较版本和阅读视图、统一 S-071 路由并交接键盘焦点；放大阅读暂停播放，窄屏增加图表/依据快速定位；案例空结果恢复全部15条，清空搜索恢复焦点，收起回到案例标题。
- 修改入口：GovernanceSection / EvaluationCanvas / ShowcaseViewport / CaseLibrary，以及两处既有样式。相同锁文件的暂存构建、Sites 4/4、源码diff空白检查通过。IAB实测1440×1000、440×956、390×844：80/80与核验视图往返保留、P-041/S-071定位、放大暂停、双柱与依据定位、关闭/Esc焦点恢复、15条恢复与4条收起通过；原文档展示放大回归通过，无页面横向溢出及console error/warn。20工作台发布文件哈希保持。原生截图被IAB视口裁切，本轮不记为整屏视觉验收；iOS实机/触摸未测。
- Draft https://6ac779fa4a72f1217e797e36--forflow-enterprise-suite-v3.netlify.app/ ready；45资源200/noindex，44逐字节一致，交流模板只有既有Netlify链接改写；生产版本6a526ad3f3353819365b175e未变。远端浏览器导航超时，远端渲染未记通过。上一版回执归档，详见ux-refinement-qa.json与remote-preview.json。8898继续服务当前构建；未commit/push、未发送邮件或写入Drive。

## 2026-10-09 — 上下文板块改为可理解的续约流程

- 用户标注 context-stage，指出关系图与文案不明所以。仅调整独立 homepage-v6 的 ConnectedContext.jsx / connected-context.css：同一笔 SUP-018 续约按「找齐资料、核对条件、负责人确认」展示；合同与规则可打开，返回保留原步骤和暂停状态。负责人待办写明待确认问题与三份材料，底部从五项泛化说明改为三项具体用途。
- 复用既有工作台的供应商/合同标识与规则，未增加真实查询、审批或客户效果宣称。640×544原生工作台在中等屏宽独占一行，手机可放大并定位资料/内容；操作接管播放、键盘方向键/Home/End和减少动态效果沿用现有机制。所有后续章节、连接器、15条案例和预约入口保留。
- 验证：相同package-lock暂存构建、4/4 Sites检查、源文件diff空白检查通过；IAB实测1440×1000、806×750、440×956、390×844无页面横向溢出或详情正文裁切。资料/规则原文与返回、负责人待办、手机定位/放大/Esc、Home/ArrowDown切换、减少动态效果通过，console error/warn空。20个工作台发布文件哈希不变。IAB原生截图裁切，不记整屏视觉验收；iOS实机未测。
- 预览 https://6ac7cc80195297efb38c0be7--forflow-enterprise-suite-v3.netlify.app/ ready；45资源200/noindex，44逐字节一致，交流模板仅有已确认的Netlify链接改写；正式部署6a526ad3f3353819365b175e保持。远端浏览器导航45秒超时，本地检查使用同一部署构建。旧回执已归档，当前回执/README/项目反馈已保存，8898服务保留。未执行Git commit/push、生产发布、邮件或Drive写入。

## 2026-10-10 — ForFlow One 挂载到正式产品路径

- 用户授权将当前预览 `6ac7cc80195297efb38c0be7` 发布到 `https://forflow.ai/product/one`，并明确产品页公开，其他页面继续保留访问码。本次不改产品视觉或内容。
- 新增 `scripts/package_product_one.py`：以预览回执验证45个构建文件，重定位资源、工作台和治理页链接，设置子路径 base 与 canonical。`scripts/build_public.py` 加入相同打包入口，缺文件或构建与回执不符时停止，避免后续全站构建遗漏产品页。Netlify 门禁只排除 `/product/one` 及其子路径；产品页允许同源工作台嵌入。
- 发布以正式版本 `6a526ad3f3353819365b175e` 的文件摘要为底，保留73个原文件，仅调整边缘路由清单，并保留5个函数的代码摘要、路由和限流配置；新增45个产品文件及重定向/响应头文件。不部署本地正式站的其他未发布修改。
- 发布前校验版 `6ac91a63fc7dc0dcc8d511bc` ready：121文件摘要核对，45个产品文件HTTP200并逐字节回读（交流模板仅有已确认的Netlify链接改写），10项路由检查通过。原官网仍跳转访问码页，产品近似前缀 `/product/one-other` 仍受保护。门禁静态/运行测试、子路径边界检查、JS语法检查、Python语法检查和源码diff空白检查通过。产品打包从原型dist再次生成通过；本地IAB首页/工作台嵌入/治理页导航通过，无损坏图片和console error。远端IAB导航超时，未记远端视觉通过。
- 根目录静态检查仍为既有 `workbench_prototype.html` 的样式/搜索/页脚结构三项失败，该本地原型不在本次生产发布包内。此次不重新生成旧正式页面；以原生产摘要保留代替全站重建。iOS实机未测。正式发布与回读结果见随后记录及 `docs/maintenance/product-one-deployment.json`。
- 正式最终发布 `6ac91f00a3371bf5a7fa42d3`，2026-10-10 01:06:38 +08:00。初次生产上传遗漏流式调用模式导致 gate-login GET 502，已向前修复；4个函数ZIP只改归档注释（所有可执行成员逐字节一致），显式上传 invocation_mode=stream，5个函数路由/限流/模式核对通过。最终正式域名10项路由回读通过，登录GET恢复405；首页、治理页、工作台及主要JS/CSS共6项内容校验通过，HTML差异仅为既有Cloudflare检测脚本。固定正式源回执为 product-one-source.json，未来预览不会自动替换正式源。完整记录见 product-one-deployment.json。未Git push、未发送邮件或写入Drive。


## 2026-10-10 — Guru 设计体系、ForFlow 内容与动效联合预览

- 用户最终指定按 Guru design system 重做并补动效。主站首页由 templates/index.html 生成，采用深色／绿色、大字、两类独立 logo 墙、三排可暂停工作动态；保留五项服务、诊断与资源，案例使用原有 B 柱、供应链、P&ID。产品开场同步主题并增加并行／审阅／接续说明，首屏改32秒合同原文→复核→处理待办；所有下半章节、连接器与15案例保留。Guru 客户标识仅按用户要求作临时版式参考，正常构建不显示；固定正式产品源未覆盖。
- 入口与来源清单：guru-homepage-20261010.md、homepage-brand-assets.json；共享 guru-system.css / guru-motion.css / guru-motion.js、BrandWall.jsx / WorkActivity.jsx，联合打包脚本 package_homepage_review.py。首页基样式与脚本隔离，避免影响其他正式详情页。
- 验证：Vite 与 Sites4/4、JS/Python语法检查通过；首页静态检查通过，既有 workbench_prototype.html 仍有3项结构错误。桌面1440px、440×956、390×844无页面横向溢出；两类标识加载、按钮位置、播放／暂停／离屏／减少动态、合同第三章与重播、手机放大返回通过，console error/warn为空。IAB截图裁切，不记整页1:1视觉通过；iOS真机未测。
- 联合预览 https://6ac9389bb0b5a08718433763--forflow-enterprise-suite-v3.netlify.app/ ready，104个资源HTTP200/noindex并校验内容；主站与产品路径均在该版本，正式部署 6ac91f00a3371bf5a7fa42d3 保持。远程浏览器导航超时，不计远端视觉通过。回执为 homepage-guru-preview.json，旧独立产品预览与正式源回执保留。未Git push、未发送邮件或写入Drive。


## 2026-10-10 — 主站与 ForFlow One 顶栏统一

- 按用户补充同步顶栏，归为产品、企业服务、资源、案例与实践四组；保留连接器、治理、能力资产和 CLI。右侧为场景诊断与既有飞书预约，统一 logo 比例、桌面 78px / 手机 68px 高度、字号、间距、绿色按钮与深色下拉面板。
- 样式与行为在 assets/site/guru-navigation.css / guru-navigation.js，首页内容在 templates/index.html，产品入口在 navigation-content.json 与 SiteNavigation.jsx；修改文案时同步两处。悬停进入 100ms、离开容错 180ms；支持方向键进入、Esc 返回焦点、手机分组滚动、点击章节后收起与减少动态。修复横向 overflow 导致吸顶失效，以及产品挂载误改 logo 返回地址。
- 验证：主站和产品 1440px、440px、390px 无横向溢出，滚动顶栏 top=0；菜单切换、键盘、手机关闭、连接器跳转、减少动态通过，控制台 error/warn 空。Vite 与 Sites 4/4 通过，静态检查仅有无关 workbench_prototype.html 三项既有错误。IAB 桌面截图裁切，iOS 实机未测。检查明细与源码摘要见 guru-navigation-qa-20261010.json。
- 预览 https://6ac93ef4dc72e5af311332da--forflow-enterprise-suite-v3.netlify.app/ ready，109 个资源 HTTP200/noindex 并完成内容回读；正式部署 6ac91f00a3371bf5a7fa42d3 未变。远端 IAB 导航 20 秒超时，本地交互检查使用同一构建。旧回执已归档，当前为 homepage-guru-preview.json。未 Git push、未正式发布。


## 2026-10-10 — 首页合同展示框与连续操作动效

- 按用户对 Qoder / OpenAI 框内展示与动效的要求，先改首页合同产品框。将整块跳转链接替换为保持位置稳定的任务对话、结果工作区和原文侧栏；围绕 SUP-018、CTR-1042 第3版和第4.2条，演示提问、对照依据、生成复核待办。合同条款与业务审批规则分开展示，法务顺序不冒充合同原文。所有交互为官网本地展示状态，未接后端提交。
- 新入口 assets/site/home-workspace.css / home-workspace.js，模板为 templates/index.html；生成根 index.html。25秒连续过程包括逐字输入、虚拟鼠标定位与点击、原文高亮、依据切换、状态反馈；可手动选择章节、开关原文、生成待办、暂停及重播。离屏和页面隐藏时停止计时，操作接管播放，减少动态时停在完成状态。手机保留左右构图，可放大并横向查看。静态检查保留合同来源、结果和完整工作台入口要求，并改查实际按钮结构。
- 来源：Qoder 当前官网 HTML/CSS 与模块资产仅存临时参考页并在本地浏览器查看，未复制其图像资产进入发布包；OpenAI 页面正文经 web 读取，直接 HTML 403、原页交互未完成视觉核对，不记为已实现像素级或时序1:1。参考拆解用于稳定框架、局部状态和操作结果的对应关系。
- 验证：首页生成、JS语法通过；1440px 桌面结果内容在工作区边界内，440×956 / 390×844无整页横向溢出、标题与控制不重叠。章节/来源切换、Esc焦点恢复、待办状态、播放到结束、离屏暂停并恢复、减少动态、放大后方向键横移通过；console error/warn空。IAB截图受到宿主裁切，不记完整桌面截图验收；iOS实机未测。静态检查仅余 workbench_prototype.html 的3个既有问题。明细见 home-workspace-qa-20261010.json。
- 远程预览 https://6ac947da5ab3e8272b6b9239--forflow-enterprise-suite-v3.netlify.app/#one ready，111个资源HTTP200/noindex并逐字节核对；72个产品子树文件与上一预览完全相同，顶栏及产品下半内容未重写。正式部署6ac91f00a3371bf5a7fa42d3未变。远端IAB导航25秒超时，本地已按同一发布包验证；当前回执 homepage-guru-preview.json，旧回执已归档。8903预览继续保留，本轮临时8905参考服务已停止。未Git push或正式发布。


## 2026-10-10 — 首页三张案例配图按正文重做

- 用户指出三张配图生搬硬套。核对后确认原版混用两张泛行业场景照与一张带标题的旧文章封面，首页 cover 裁切不能说明各案例工作内容。替换为三张统一660×440的原创SVG视觉：B柱材料/工艺/失效机理与变更复评；渠道B履行异常→信用控制冻结→待审批放行请求；P&ID阀门定位与设备连接查询。正文来源及图形表达边界记录在 home-case-visuals-20261010.json，不将说明性视觉称为真实客户工作台截图。
- 图片位于 assets/site/case-studies/，布局为 home-case-studies.css；生成来源 templates/index.html 已同步。三卡等宽、完整contain显示、移除灰度滤镜及旧图片强制裁切；标题和摘要改成与对应案例一致的具体问题。案例详情页和固定产品构建不变；未引入新的量化效果或客户背书。
- 验证：首页生成、三张SVG XML解析通过；静态检查仅有无关workbench_prototype.html三个既有错误。浏览器目视检查三张图，1440px三卡等高514.63px、等宽369.33px；440px与390px图片加载、文字间距、完整边界检查通过，无整页横向溢出，console error/warn为空。iOS实机未测。
- 预览 https://6ac94c4ca545c33274d20db5--forflow-enterprise-suite-v3.netlify.app/#cases ready，112资源HTTP200/noindex及内容回读通过。包仅改首页HTML、案例CSS和三张SVG，并移除首页不再使用的旧三张位图；产品子树、顶栏、上一轮工作台动效文件保持。正式部署6ac91f00a3371bf5a7fa42d3未变。当前回执homepage-guru-preview.json，前版回执按ID归档。未重复此前持续超时的远程IAB导航，本地按相同包核验，8903本地预览保留。未Git push、未正式发布。

## 2026-10-10 — 产品页保留原版，仅轻微对齐主站

- 用户明确 /product/one 保持原有页面，风格略微靠近主站。产品恢复浅色居中首屏，标题后直接进入真实工作台；移除本轮额外叠入的客户墙、滚动状态条与首屏功能／生态栏。原有三个场景、处理过程、优势、AI 资产、治理、连接器、CLI、15 条案例与联系部分全部保留，合同讲解流程也保留。主站首页继续使用已经接受的 Guru 方案。
- App.jsx 与 main.jsx 分开主站／产品样式；新增 product-brand-alignment.css，仅调整浅色导航、灰绿色强调与浅绿圆角预约按钮。共享导航只增加产品选择器别名，不改变首页样式声明；产品导航降至 z-index 60，修复放大工作台时关闭按钮被导航层截获的问题。工作台 20 个文件逐字节未变；主站 HTML、案例配图和工作台文件未变。最新范围同步至产品 AGENTS.md 与 guru-homepage-20261010.md。
- 验证：最终 Vite 构建与 Sites 4/4 通过。IAB 检查 1440px、440×956、390×844 无页面横向溢出，首屏标题／说明／CTA 边界不重叠；桌面导航方向键和 Esc、手机菜单展开关闭、合同章节／重播／暂停通过。发现并修复导航与放大层层级冲突，390px 下复测关闭成功、恢复 body 滚动。控制台 error/warn 为空；九个下半区块及 15 条案例入口保留。桌面截图受宿主裁切，配合 DOM 几何检查；iOS 真机未测。根静态检查仍为无关 workbench_prototype.html 三项既有错误。
- 预览 https://6ac95170650074502b34ff9f--forflow-enterprise-suite-v3.netlify.app/product/one/ ready，112 个资源 HTTP200/noindex 并校验内容。正式部署 6ac91f00a3371bf5a7fa42d3 未变，固定正式产品源未覆盖；当前回执 homepage-guru-preview.json，上一版已按 ID 归档。本地 8903 继续可用。远程 IAB 不重复此前的导航超时，本地验证相同包并逐文件回读远程内容。未 Git push、未正式发布。

## 2026-10-10 — 补齐首页知识连接与聚合动效

- 用户指出 Guru 首页关键动效遗漏。核对发现首页只有倾斜卡片滚动，缺少来源连线、中心知识聚合与 AI 工具联动。重新读取官网源码并在临时本地参考页观察 SVG、CSS 与原时间线；远程 IAB 超时，不记为原站交互实测或逐像素复刻。
- 仅在主站首屏状态条与产品工作台之间新增知识连接板块。入口为 templates/index.html、assets/site/home-knowledge-motion.css / .js；原生 SVG 与 Web Animations API 实现分批出场、路径绘制、环形标签、知识卡片和持续光点，采用参考的出场顺序与约 2 秒展开节奏，无新增运行依赖或外部请求。原动态卡片、工作台、案例与其他内容保留。
- 加入暂停、重播、滚入播放、离屏及页面隐藏暂停、减少动态模式。修复完成动画恢复时重复闪现、Codex 标识对比不足、手机放大缩放布局留下空白；手机可完整查看或放大横移。产品页 72 个包文件与上一版逐字节一致。
- 验证：首页生成与 JS 语法通过；首页静态检查通过，仅无关 workbench_prototype.html 三项既有错误。IAB 的 1440px、440×956、390×844 无整页横向溢出，图标加载、暂停计时保持、重播起点、离屏恢复、减少动态、手机放大恢复与键盘横移通过，console error/warn 空。局部构图已目视检查，大尺寸截图受宿主裁切并结合 DOM 边界检查，iOS 真机未测。详见 home-knowledge-motion-qa-20261010.json。
- Draft https://6ac95943b0b5a0778a4337de--forflow-enterprise-suite-v3.netlify.app/#knowledge-flow ready，114 个资源 HTTP200/noindex 且内容回读通过；只改变首页 HTML 和两份新动效资产。正式部署 6ac91f00a3371bf5a7fa42d3 未变。当前回执已更新，上版已归档；8903 预览保留，临时 8906 参考服务已结束。未 Git push 或正式发布。

## 2026-10-10 — 修正知识连接图的中文排布和标签样式

- 用户指出「来源可追溯」等十五字显示异常、合同条款等标签样式突兀。移除 SVG textPath 弧形中文，顶部改为水平上下文标题；三句说明移至图下方，手机保持正常 12px 字号，不跟随整个图缩小旋转。
- 十二个原知识标签全部保留，改为低饱和深底、细边框、圆角胶囊与对应小图标，自然排列为四行；取消亮绿色实底和渐隐遮罩。修改模板及 home-knowledge-motion.css / .js，连线和光点动效保持。产品页 72 个包文件与上版逐字节相同。
- 验证：首页生成、JS 语法通过；首页静态检查通过，仍只有无关 workbench_prototype.html 三项既有错误。IAB 检查 1440px、440px、390px 无整页横向溢出，十二标签无裁字、图标引用全部有效，弧形文字数量为零。暂停、重播、手机 840px 放大和恢复通过，console error/warn 空；局部截图已目视核对。大尺寸使用 DOM 边界辅助检查，iOS 实机未测。
- 远程预览 https://6ac966962f49dee977839197--forflow-enterprise-suite-v3.netlify.app/#knowledge-flow ready，114 个资源 HTTP200/noindex 与内容回读通过。只改变首页及两份动效资产；正式部署未变。当前回执已更新，上版已归档，8903 本地预览保留。未 Git push 或正式发布。

## 2026-10-10 — 聚合中心直接使用 ForFlow One 产品图标

- 按用户要求，将首页知识连接图中央临时绘制的 SVG 符号替换为 ForFlow One 原版应用图标。来源为已安装 Forflow One.app 的 app.asar.unpacked/resources/forflow/forflow-app-icon.png，原文件直接复制至 assets/site/forflow-one-app-icon.png；无重绘或生成改造。保留 ForFlow One 名称、知识标签、连线和播放过程，去掉旧绿色图标框，柔光改为沿原图透明边缘显示。
- 修改 templates/index.html 和 home-knowledge-motion.css / .js；生成与 JS 语法通过，静态检查仍仅有无关 workbench_prototype.html 三项既有错误。IAB 确认原图加载 1024px、旧 SVG 数量为零、动效运行；目视检查及 1440px/390px 边界检查通过，图标／名称／标签无重叠、无页面横向溢出，console error/warn 空。iOS 真机未测。
- 预览 https://6ac9cbcefb5a9c000f51ff7f--forflow-enterprise-suite-v3.netlify.app/#knowledge-flow ready，115 资源 HTTP200/noindex 和内容回读通过。产品页 72 个文件保持不变，正式部署未变。回执更新并归档上一版，8903 本地预览保留；未 Git push 或正式发布。

## 2026-10-10 — 首页工作台细节、任务状态与 Cursor 标识

- 按用户反馈删除“所有材料在同一工作区”“资料保持关联”等泛化解释，改为材料数量、合同条款、复核顺序与待办状态；同步细化工作台下方三项能力文案。保留既有主站视觉与知识聚合动画，不修改产品页。
- 实际浏览 Qoder 中文产品页，点击竞争分析任务及 HTML 产物，参考其稳定的对话／产物分区、紧凑状态行和原文阅读层级。首页复核过程改为提交前只显示材料、提交后读取、核对完成再显示结论；手动第三步停在待创建，点击才生成 TK-1042，完成后禁止重复创建。发送按钮提交当前问题，不再重播整个过程。
- 原文改为完整右侧阅读面板，增加返回入口、Esc 返回及焦点恢复；修复切换依据后读屏播报错误来源。放大模式保留横向工作台，补任务／结果视野切换与 Esc 收起；字体、对比度、表格间距和内容高度统一调整。暂停、重播、滚入播放、离屏暂停及减少动态模式保留。
- Cursor 原位图被统一反白滤镜抹成白块，替换为官方品牌包 General Logos/Cube/SVG/CUBE_2D_LIGHT.svg（https://cursor.com/brand），原 SVG 直接复制；知识聚合和工具栏都使用此资产。工具栏撤销整图反白，为各标识设置相同尺寸，Codex 保留深色底以承载白色标识。
- 验证：主页生成、JS 语法通过；静态检查仅 workbench_prototype.html 三项既有错误。IAB 实测提交至自动完成、手动章节、依据切换与播报、Esc／焦点恢复、创建前后状态与禁用重复创建。桌面 1440px 布局及局部截图检查，440px 手机放大切换实际点击后 scrollLeft=331px、整页无溢出；390px 标题和控件无重叠。减少动态停在待创建并隐藏虚拟鼠标；控制台 error/warn 空。宿主缩放影响大尺寸截图，辅以 DOM 测量；iOS 真机未测。
- 最终包 workspace-refinement-final 与上一版相比，仅首页、工作台 CSS/JS、工具栏样式与 Cursor 资产变更；产品子树 72 文件逐字节一致。旧预览回执已按 ID 归档；本地 8903 保留。

- Draft https://6ac9dec27bc79588a72a0c48--forflow-enterprise-suite-v3.netlify.app/#one ready，115 个资源 HTTP200/noindex 与内容回读通过；正式部署 6ac91f00a3371bf5a7fa42d3 未变。远程 IAB 导航 30 秒超时，使用同包本地交互与逐文件 HTTPS 回读验证。当前回执更新，未 Git push 或正式发布。

## 2026-10-10 — 工作台切换节奏与动作说明细化

- 按用户对 Qoder 点击、切换、小动效和文案的反馈，核对当前官网正文及官网 CSS 的 220ms 面板、480ms 选中项与 140–160ms 显隐节奏。当前远程参考页 IAB 超时，参考结论来自官网内容与样式，不记作本轮原站交互实测或逐像素复刻。
- 仅细化主站合同工作台：章节改为“发起复核 / 查看依据 / 交给负责人”，增加各步说明；材料依次显示读取状态，结果分层出现，引用局部展开，按钮按压反馈，待办生成先显示处理状态。保持工作台边界和整体视觉，去掉整块重复入场；快速切换取消旧动画与延迟创建。
- 验证：主页生成及 JS 语法通过；静态检查仍仅 workbench_prototype.html 三项既有错误。IAB 实测完整自动播放、手动章节、原文切换与关闭、生成中到 TK-1042、快速跳转取消创建；暂停后时间线动画保持相同时间戳，恢复播放；减少动态时停在待创建、隐藏鼠标、活动动画为零。控制台 error/warn 空。1063px、1440px 桌面及 440×956、390×844 手机边界检查，无整页横向溢出、说明与控件无重叠。宿主缩放裁切截图，辅以 DOM 几何；iOS 真机未测。
- 发布包 workspace-qoder-motion 相对 workspace-refinement-final 仅 index.html、home-workspace.css、home-workspace.js 改变，产品子树 72 文件逐字节一致。8903 本地预览保留。部署脚本准备首次失败后误建了上一包的重复草稿 6ac9f178c15e4a453265571b，无内容变化，正式部署未变；该回执已归档，后续交付使用本轮包。
- 交付预览 https://6ac9f355c15d91d7303c0957--forflow-enterprise-suite-v3.netlify.app/#one ready，115 个资源 HTTP200/noindex 并逐文件回读通过，正式部署 6ac91f00a3371bf5a7fa42d3 未变。当前回执 homepage-guru-preview.json 已更新；未重复远程浏览器导航超时，以同包本地交互和远端文件核对验证。未 Git push、未正式发布。

## 2026-10-10 — 知识连接区改为开放构图

- 用户提供 Guru 截图，指出当前表达过于规整。本次按截图调整知识连接区的重心、疏密与层次：去掉两侧统一方框，保留原产品标识；拉开两侧弧线，中心扩大为五行错位知识卡片，由浅绿逐层过渡到深绿。ForFlow One 原图标略倾斜，只有图标轻微浮动；光点沿资料汇入和工具接出的路径移动。保留十二个知识主题，不改合同工作台和产品页。
- 标题简化为“把企业的知识，交到 AI 手中”，说明直接使用合同、业务记录、团队经验。三个原则放在圆环附近，中文保持完整横排，不再使用容易挤字的中文 textPath。移除底部横线与清单式说明，连接入口居中、播放控件退至次要位置。
- 维护入口：templates/index.html、home-knowledge-motion.css / .js；生成根 index.html。包 knowledge-open-composition 与 workspace-qoder-motion 相比仅三份首页文件变更，72 个产品文件逐字节一致。生成和 JS 语法通过，静态检查仍仅无关 workbench_prototype.html 三项既有问题。
- IAB 验证：1440px 桌面构图与局部截图，440px 和 390px 页面无横向溢出、控件不重叠；7 个图标加载，12 条连接线、12 个知识标签完整；手机放大为1020px画布并可横移、恢复全貌。暂停时光点时间戳保持不变，重播回到起点；减少动态模式活动动画为零、全部卡片可见；控制台 error/warn 空。桌面截图受宿主缩放裁切，CDP 大图捕获出现拼接异常，不作为完整桌面截图验收；已用 DOM 边界辅助检查，iOS 真机未测。8903 预览保留。
- 预览 https://6ac9ff7ae3ef053a94fa6890--forflow-enterprise-suite-v3.netlify.app/#knowledge-flow ready；115 个资源 HTTP200/noindex 及内容回读通过，正式部署 6ac91f00a3371bf5a7fa42d3 未变。当前回执 homepage-guru-preview.json 已更新，上一版按 ID 归档；未 Git push 或正式发布。

## 2026-10-10 — 业务场景从困难描述改为问题、结果与依据

- 用户要求参考 Guru 讲清“从业务问题开始”下方内容。读取 Guru 首页、solutions 与 how-it-works：团队场景先讲能完成的工作，机制段用问题、处理过程与具体输出衔接。参考地址：https://www.getguru.com/、https://www.getguru.com/solutions、https://www.getguru.com/product/how-it-works。远程 IAB 导航超时，未将网页源码阅读记为原站交互实测。
- 主站六张挑战卡改为六个可切换场景，保留客户服务、营销内容、企业知识、运营流程、财务经营、人才组织范围。标题改为“把 AI 用在每天都要做的工作里”，各场景展示具体提问、回复／邮件／差异清单／待办／办理清单，以及可展开的依据；供应链入口关联已有案例，其余保留带场景参数的诊断入口。图内文字是说明性工作场景，不增加客户、上线、效果数字或实际产品截图的断言。
- 沿用已接受的深绿主站和浅色工作界面。手动切换、局部错峰过渡、来源展开；支持方向键、Home/End、焦点和读屏状态，减少动态模式停止过渡。手机保留可读的结果内容，横滑选择场景。补齐固定展示高度和展开图标余量，避免切换跳动与文字裁切。
- 入口为 templates/index.html 与新增 home-scenarios.css / .js，执行 homepage-only 生成和独立预览打包。119 个包文件，相对 knowledge-open-composition 仅首页 HTML 与两份场景资产变化，产品子树 72 文件逐字节相同。未改工作台、知识连接动效、案例详情或 /product/one。
- 验证：JS 语法、首页生成通过；静态检查仍只余无关 workbench_prototype.html 三个既有错误。IAB 六场景切换、原文展开/关闭、方向键与 Home、焦点和状态播报通过；1440px 六面板均高 591.87px，390px 均高 798.43px，无整页溢出或内容裁切。440px 初检后统一修正展示高度与图标余量；减少动态时本区活动动画为零，键盘切换 scrollY 差为零，图标全部加载，console error/warn 空。手机局部截图已目视检查，桌面截图受宿主缩放裁切，辅以 DOM 几何；iOS 真机未测。
- 预览 https://6aca0c7cabc97a970d516824--forflow-enterprise-suite-v3.netlify.app/#challenges ready；117 个资源 HTTP200/noindex 并逐文件回读通过，正式部署 6ac91f00a3371bf5a7fa42d3 未变。回执更新并归档上一版。8903 本地预览保留；未 Git push 或正式发布。

## 2026-10-10 — 知识标签细化与圆环中文可读性

- 用户截图标注弧形中文拉散、标签过厚且缺乏 Guru 式细节。基于最新版本继续细化：标签从 17px/42px 改为 15px/34px，减小内边距、边框与圆角，保留五行错位和由浅到深的层次。新增九种本地 SVG 小图标，用于十二个知识标签，按文档、规则、工程图、历史、流程、复核、关系、材料和权限分别表达。
- 圆环标题取消字距，三项原则改为完整水平文字。手机全览将三项说明放在图下，以正常 12px 字号显示；放大后回到图内。真实 ForFlow One 图标、连接线与光点、十二项主题保持。旧截图中的大方框与中文 textPath 不带回当前版本。
- 维护入口 templates/index.html、home-knowledge-motion.css、knowledge-tag-icons.svg。预览打包脚本补充 SVG use href 资源收集，避免外部 sprite 遗漏。主页生成、SVG XML 和九个 symbol 校验通过；静态检查仍只余无关 workbench_prototype.html 三个既有错误。
- IAB 验证：1063px 桌面局部构图；十二个 SVG use 均有非零绘制尺寸，标签不裁字、三个说明 transform=none、textPath 数量零。440px 放大为 1020px 可横移画布，图标与横排说明目视通过，暂停后活动动画为零、重播恢复运行。390px 全览无整页溢出，三项说明均为 12px，减少动态时活动动画零且五行标签可见，console error/warn 空。宿主裁切大尺寸截图，结合 DOM 几何核对；iOS 真机未测。
- 包 knowledge-tag-detail-final 共 120 文件，相对 scenario-stories-final 仅首页 HTML、知识样式与新图标 sprite 改变；72 个产品文件逐字节相同，上一轮六场景完整保留。8903 本地预览保留。
- 预览 https://6aca12669f486c47c77dfce6--forflow-enterprise-suite-v3.netlify.app/#knowledge-flow ready，118 个资源 HTTP200/noindex 且逐文件内容核对通过。正式部署 6ac91f00a3371bf5a7fa42d3 未变；当前回执更新并归档上一版。未 Git push 或正式发布。

## 2026-10-10 — ForFlow One 工作机制与真实产品界面

- 按用户的 Qoder「如何工作」参考，替换重复的三列续约流程，保留 #platform。新增智能体选择、步骤进度、项目背景、工作台工具、人工审阅五张错落卡片，沿用深绿主站与浅色界面。完整业务工作台、案例、场景及产品页保留。
- 支持菜单选择、步骤播放／暂停、资料与工具切换、审阅截图切换、完整图片弹层；含键盘方向键、离屏暂停、减少动态手动步进与弹层焦点恢复。手机图片从主操作区开始，可左右查看。
- 使用 ForFlow One 2026-09-28 产品截图集的三张原图，文件与来源哈希相同，仅 CSS 裁切。来源与适用范围见 home-mechanisms-assets.json。Mac 当前锁定，未取得新的实时截图；使用已有真实产品素材。没有套用 Qoder 的智能路由、语音伙伴或多人实时对话承诺。
- 验证修复菜单行高、内部焦点滚动、截图拉伸及手机弹层位置。主页生成和 JS 语法通过；静态检查改为检查保留的完整工作台三阶段和播放入口，仍仅有 workbench_prototype.html 三个既有错误。IAB 在 1440／1063／440／390px 验证无整页溢出，卡片内容不裁切；主要选择、切换、键盘、暂停与弹层通过。减少动态时本区活动动画零，控制台 error/warn 空。
- 大尺寸截图受宿主裁切，结合局部目视与 DOM 几何检查；Qoder 同屏等密度严格视觉对照未完成，design-qa.md 记为 blocked，不声称像素级复刻。iOS 真机未测。预览包 mechanisms-final 共 124 文件，72 个产品文件逐字节不变；本地 8903 预览保留。

- Draft https://6aca24ee208c9cfa7530f90c--forflow-enterprise-suite-v3.netlify.app/#platform ready; all 122 served assets passed HTTP 200, noindex and byte readback. Production 6ac91f00a3371bf5a7fa42d3 unchanged. Receipt archived and updated; no production release or Git push.

## 2026-10-10 — 首页手机阅读、点按与产品放大

- 按用户补充的手机版要求，保留当前首页内容和视觉，调整首屏字号随屏宽变化，修复 320px 下标题四行且“一步步”断开的情况。机制卡片、播放、工具切换、场景切换、导航及来源展开的主要控件扩大到至少 44px；小字和说明适度调大，窄屏不强行重排工作台内部层级。
- 真实产品截图补充“查看全貌／放大细看”。手机从 1200px 图片的主操作区开始，可双向滑动；弹层采用动态视口高度、安全区余量与背景定位锁定，关闭及 Esc 恢复原滚动位置和触发焦点。修正手机材料截图裁切后底部留白。合同工作台保留 1000px 横向画布，并增大任务／结果视野切换与播放按钮。
- 维护入口为 templates/index.html 和对应首页样式／机制脚本，执行 homepage-only 生成，独立打包 mobile-refinement-reviewed。相对 mechanisms-final，72 个 product 文件逐字节一致。生成、JS 语法、差异空白检查通过；静态检查仍只有无关 workbench_prototype.html 三个既有错误。
- IAB 在 320／375／390／440／1440px 检查：整页横向溢出为零；主要点按控件达到 44px；320px 步骤控件保持一行，机制卡片没有内容裁切；320／440px 首屏为两行标题。智能体／工具／审阅切换、场景横滑与依据展开、工作台放大和平移、截图全貌／细节与关闭位置恢复通过；减少动态时机制区活动动画为零，手动步进可用。console error/warn 空。实际 iOS Safari 真机尚未测试，不把浏览器窄屏检查记为真机验收。详情见 home-mobile-qa-20261010.json。
- 远程预览 https://6aca311bb69e965b30629c54--forflow-enterprise-suite-v3.netlify.app/ ready，122 个资源 HTTP200/noindex 及逐文件内容回读通过。正式部署保持 6ac91f00a3371bf5a7fa42d3；回执归档并更新，未 Git push 或正式发布。8903 本地预览继续可用。

## 2026-10-10 — 审阅截图去掉教学浮层并统一取景

- 用户指出审阅展示的教程浮层与图片尺寸不合适。替换两张旧截图为已有的真实产品 QA 原图：1.4.220-forflow.1 的审阅活动、1.4.222-forflow.1 的材料选择；原始像素与来源哈希保持一致。图片没有教学提示浮层，素材版本、路径与用途写入 home-mechanisms-assets.json。使用的是合成 QA 工作区与记录，不作为客户成果或模型效果证据。
- 首页默认页签改为“看审阅记录”，说明与实际图片内容对齐。用固定比例的取景窗口替代各断点的大幅百分比偏移，两张图切换高度相同；全图按钮移到图片下方，避免遮住内容。窄屏保留 520px 画布，可横向查看并打开原图；全图弹层依据每张图片的主体位置定位。
- IAB 验证 320／440／1063／1440px 整页无横向溢出；440px 两页签卡片高度同为 674.61px，材料原图宽高比 1.42223 与原始 1.42222 一致。320px 实际横移到 107.77px，主要按钮约 44px；放大全图／恢复全貌、键盘页签切换、关闭后恢复滚动 5423.06px 和触发焦点通过，控制台 error/warn 空。原图及手机局部截图已目视核对；桌面宿主截图裁切，辅以 DOM 几何检查，未做 iOS 真机验收。
- homepage-only 生成、JS 语法通过；静态检查仅剩无关 workbench_prototype.html 三项既有问题。review-captures-clean 包相对上一预览只改变首页 HTML、机制 CSS／JS 和两张截图；72 个产品文件逐字节相同。8903 本地预览保留。
- 新预览 https://6aca52f80dec4ccbfa69384f--forflow-enterprise-suite-v3.netlify.app/#platform ready；122 个资源 HTTP200/noindex 与内容回读通过，正式部署 6ac91f00a3371bf5a7fa42d3 未变。当前回执归档并更新，未 Git push 或正式发布。

## 2026-10-10 — 首页诊断入口统一视觉与四步交互

- 用户指出诊断卡不符合整页审美。原浅色卡片仍继承深色方案的浅字色；去掉厚绿背景与仿浏览器圆点，采用单层浅色卡片、深灰文字、细边框和低饱和选中状态。英文步骤标签换为四段中文进度，左侧说明改为具体输出。
- 选项增加图标与一行工作说明，使用原生 radio 支持方向键、焦点与读屏；取消预选，未选择时下一步不可用。新增上一步并保留答案，切题采用 220ms 局部过渡，减少动态时停止过渡。手机切题将问题带回可见区域。末步传递四项选择至现有完整诊断。
- 维护入口 templates/index.html、script.js、新增 home-navigator.css；homepage-only 生成 home-interactions.js 和 index.html。独立预览包 navigator-refined-final 保留上轮审阅截图修正。
- IAB 在 320／440／1063／1440px 检查无整页横向溢出；320px 选项未溢出、下一步高约 44px；1063px 两题切换卡片高度均为 675.95px。四步推进、返回保留 knowledge/risk、键盘选择 operations、减少动态时活动动画零、console error/warn 空。手机局部与桌面局部截图目视通过；桌面宿主截图裁切，辅以 DOM 边界检查，未做 iOS 真机验收。
- 完整诊断跳转带齐四项参数，线上仍进入既有访问码页 landing.html?next=/navigator.html?...；首轮浏览器等待超时，随后标签清单确认目标和参数。未改已有门禁，未将该跳转记为诊断结果页验收。
- 生成和 JS 语法通过；静态检查仍只有无关 workbench_prototype.html 三项既有错误。一次发布准备脚本编码错误，使旧审阅包产生了重复 draft 6aca5d45a3371b3771fa42aa；不作为本轮交付，正式站点未变。
- 本轮交付 https://6aca5dbc2212dc4e03be0b6d--forflow-enterprise-suite-v3.netlify.app/#navigator ready；125 个包文件中的 123 个资源 HTTP200/noindex 与逐文件回读通过。相对上轮仅首页 HTML、首页交互脚本、新诊断样式三份文件变化，72 个产品文件逐字节不变。正式部署 6ac91f00a3371bf5a7fa42d3 未变；回执更新，未 Git push。8903 本地预览保留。

## 2026-10-11 — 首页资料、问答与页尾收尾打磨

- 用户要求继续打磨底部。工具与资料改成三张紧凑、等高的入口卡，统一线性图标、中文标签和箭头反馈；诊断入口回到本页四步卡。常见问题改为产品用途、已有系统接入、试点材料、效果判断，使用一问一答的单项展开；补齐问题与答案的 aria 关联、收起状态和键盘操作。
- 页尾删除重复诊断号召和大尺寸装饰，改为左右分区的预约产品演示入口，沿用既有飞书需求表，并说明填写后联系确认内容与时间。重排产品、企业服务、探索与资料三个导航组，补齐 ForFlow One、连接器、隐私说明与返回顶部，去掉“案例详情示范”。保留上部所有已接受内容、诊断改造和真实审阅截图。
- 维护入口 templates/index.html、script.js、新增 assets/site/home-closing.css；homepage-only 生成 index.html/home-interactions.js。搜索弹窗中文化、缩短输入提示、修复关闭按钮对比度，手机底栏目标至少 44px。
- IAB 检查 320／440／1063／1440px 无整页横向溢出；桌面三卡等宽等高，窄屏标题与链接不裁切。FAQ 单项展开、Enter 展开与 Space 收起、搜索打开／Esc／关闭及触发焦点恢复、返回顶部 scrollY=0 均通过；减少动态下卡片与答案过渡为 0s；console error/warn 空。手机与桌面局部目视检查通过，桌面截图受宿主裁切，辅以 DOM 几何检查；未做 iOS 真机验收。
- 生成与 JS 语法检查通过，静态检查仍仅有 workbench_prototype.html 三项既有问题。closing-refined-final 共 125 文件，72 个产品文件与上一预览逐字节一致。8903 本地预览保留；只更新独立预览，不改正式站点或 Git 远端。
- 新预览 https://6aca68412f49deea9f83923c--forflow-enterprise-suite-v3.netlify.app/ ready；123 个资源 HTTP200/noindex 与逐文件内容回读通过。正式部署 6ac91f00a3371bf5a7fa42d3 未变，回执更新并归档上一版。本包仅 index.html、home-interactions.js、新增 home-closing.css 改变，移除不再使用的 logo 副本；浏览器远程导航两次超时（第二次为状态检查），不计为远程视觉验收，本地视觉与交互结果不受影响。

## 2026-10-11 — 首页诊断以下按需展开与案例切换

- 用户要求诊断区域及后续内容重新调整，允许折叠。沿用当前首页视觉，诊断压缩为一条入口，点击展开原有四步表单；收起保留答案与当前步骤，资料区和页尾诊断入口会直接展开。手机只保留必要提示，主要点按目标至少 44px。
- 实施方法改为四项单项展开，每项给出具体工作和交付；案例改为汽车工程、供应链、工程知识三个可点击／键盘切换的面板，沿用各自机制图和案例来源。资源区压缩为三个简洁入口，减少问答和预约区间距与字号。借鉴 OpenAI／Qoder 的按需查看节奏，无自动切换。
- 维护 templates/index.html，新增 assets/site/home-lower-story.css/js，执行 homepage-only 构建。lower-story 预览包相对 closing-refined-final 只改 index.html 和两项新增资产，诊断之前的首页内容逐字节一致，72 个 product/one 文件逐字节一致。
- IAB 检查 320／440／1063／1440px 无整页横向溢出；窄屏标题不裁切。诊断展开／收起、选择后下一步、返回保留答案、页内入口展开通过；方法单项展开与 Enter 切换、案例点击与方向键切换、搜索打开／Esc 关闭通过。440px 三案例面板高度均为 596.43px，320px 检查汽车与工程知识均为 530px。减少动态时新案例动画为零、抽屉过渡 0s；console error/warn 空。桌面宿主截图存在裁切，辅以 DOM 几何；未进行 iOS 真机测试。
- 构建及 JS 语法通过；静态检查仍仅 workbench_prototype.html 三项既有问题。QA 保存在 home-lower-story-qa-20261011.json。本地 8903 预览保留，发布仅独立 draft。
- 新预览 https://6aca71b5b321ea466677801f--forflow-enterprise-suite-v3.netlify.app/ ready；125 个资源 HTTP200/noindex 与逐文件内容回读通过。正式部署 6ac91f00a3371bf5a7fa42d3 未变；回执更新并归档上一版，未 Git push。

## 2026-10-11 — 场景对话联系人头像与异常跟进文案

- 用户指出紫色“我”与绿色“业”字块缺少真实产品感，订单放行文案含混。六个业务场景提问头像统一复用已有合成联系人肖像，售后与信用控制联系人同步替换；素材复制到 assets/site/people，来源与哈希记录在 home-scenario-contact-assets.json，未使用真人员工身份或客户资料。
- 沿用整体深色官网，局部对话借鉴 Sana 已提供参考的浅灰提问气泡、白色回答区和独立结果卡层级。去掉重复的内嵌边框与过小的字标，状态、标题、正文与跟进人分级。只统一场景组件，首屏及其他部分保持不变。
- 运营文案依据现有供应链案例：未付款订单增加触发信用控制冻结。改为“待核对回款”，明确渠道客户经理补充回款凭证、信用控制组核对后提出放行意见并提交审批；未写成已经批准或解除冻结。跟进事项和两项分析依据支持点击与键盘展开，同组一次展开一项。
- IAB 检查 320／440／1063／1440px 无整页横向溢出，320px 六个场景标题与气泡未裁切；头像加载成功，手机头像 32px／窄屏 28px，跟进目标高 76px。跟进与依据展开、Enter 切换、六页签切换通过；减少动态模式下当前场景活动动画为零，展开过渡 0s；console error/warn 空。手机局部截图目视检查，桌面截图受宿主裁切并辅以 DOM 几何；未测试 iOS 真机。
- homepage-only 生成通过；静态检查仍仅 workbench_prototype.html 三项既有错误。contact-story-final 共 129 文件，相对 lower-story 仅 index.html、home-scenarios.css、两张联系人头像变化，72 个产品文件与首页其他部分逐字节一致。8903 预览继续可用；只更新独立 draft，未改正式站或 Git 远端。
- 新预览 https://6acae7440dec4c6d8669384e--forflow-enterprise-suite-v3.netlify.app/ ready，127 个资源 HTTP200/noindex 与逐文件内容回读通过，正式部署 6ac91f00a3371bf5a7fa42d3 保持不变。回执更新并归档上一版。

## 2026-10-13 — 首页删减重复文案

- 用户明确本轮重点为多余文案。删除六场景重复分类与同义结果总结、无操作的省略号、产品演示下重复三步说明与数字入口带、能力区重复介绍、案例图下同义说明及页尾重复口号；缩短审阅说明、上下文提示与 FAQ。保留具体业务判断、依据、负责人、状态和预约说明。
- 已改 templates/index.html，并同步现有生成 HTML。iCloud 将构建依赖与部分资产卸载，homepage-only 与标准打包读取被阻塞，已中止本次等待；以已有完整 contact-story-final 包同步同一文案修改，未改 CSS 或 JS。后续文件恢复后运行标准生成与打包。QA 记录 home-copy-trim-qa-20261013.json。
- IAB 440／1280px 无横向溢出，删减目标在 DOM 中为零，场景切换正常，console error/warn 空。保存手机及桌面截图；桌面截图临时缩放用于克服宿主截图比例异常，随后恢复并关闭本地检查标签。未做 iOS 真机测试。结构标签平衡、所引用资产存在、72 个 product/one 文件逐字节不变。
- 新 draft https://6acdbcd7bee14c5be42a099f--forflow-enterprise-suite-v3.netlify.app/ ready；127 个资源 HTTP200/noindex 与逐文件内容回读通过，正式部署未变。回执保存 homepage-guru-preview-copy-trim-20261013.json（旧回执受 iCloud 卸载阻塞，未覆盖）。远程浏览器打开超时，不记为远程视觉验收。本地 8903 预览保留。

## 2026-10-13 — 手机产品窗口信息与对齐

- 用户要求调整手机屏幕信息、参考 Qoder 的视觉对齐。原工作台把 1000px 桌面画面整体缩小，手机正文难以辨认；改为同一工作台的任务／结果两个视野，手机原字号展示、横向平移，章节切换自动定位结果。保留材料、原文、核对字段、复核待办与来源交互。手机收掉重复放大控件，统一标题、结果表格、来源页和按钮边距。
- 六场景统一问题气泡、状态、结果与依据的字号和边距，收起重复结果标签与固定 450px 留白；能力卡片及真实审阅截图调整内边距与裁切宽度。仅作用于 <=700px；桌面工作台构图保留。
- 维护 templates/index.html、home-workspace.js、新 home-mobile-product.css；homepage-only 生成完成。标准打包因 iCloud 卸载资产卡住，使用同一打包函数与按字节复制，未变的卸载资产复用上一已验证包。新包只改首页 HTML、工作台脚本与新手机样式，72 个产品文件逐字节相同。
- 浏览器宽度 320／390／440／1280px 无整页横向溢出，手机结果区与窗口等宽、scale=1，判断正文 14px；原文打开、章节与视野切换、六场景文字未横向裁切、跟进展开通过。减少动态模式下活动动画零；console error/warn 空。截图保存 /private/tmp/forflow-mobile-result-20261013.png、forflow-mobile-story-20261013.png。未做 iOS 真机验收。当前 Qoder 浏览器检查超时，参考用户已给视觉与本轮官方页面结构，未声称当前手机像素复刻。
- JS 语法通过。静态检查发现上轮删掉重复数字入口带后仍保留“四链接”结构断言，已改为验证产品、诊断、准备度、工作流四个实际入口仍可到达；重跑仅 workbench_prototype.html 三项既有问题。QA 保存 home-mobile-product-qa-20261013.json。
- 额外播放验证：可见窗口重播后 is-playing=true；随后自动进入第三章 created，视野移至结果，scrollLeft=397.67、窗口宽398。手机截图验证完成后恢复浏览器宽度并关闭检查页。
- 新 draft https://6acdc3a82ba08b5700ec769c--forflow-enterprise-suite-v3.netlify.app/ ready；128 个资源 HTTP200/noindex 与逐文件内容回读通过，正式部署未变。回执保存 homepage-guru-preview-mobile-product-20261013.json。8903 本地预览保留。

## 2026-10-13 — 浅色产品页案例区视觉与交互

- 用户指定 6aa571cdfa3641ac3084ecc1 预览的 #cases，明确先优化网页视觉交互。沿用当前浅色产品原型，调整 CaseSpotlight、CaseLibrary、connected-context.css 和 lower-editorial.css；保留四个重点案例与完整 15 条目录及归属。重点案例统一留白、字级和实色“查看案例”按钮；案例库增加分类数量、精选/全部/匹配数量，整卡可点击并保留原文链接的原生快捷打开行为。
- 补齐重点案例 Home/End/方向键切换、空结果恢复全部、搜索 Escape 清空和关闭详情后的焦点返回。手机正文 14px、搜索 16px，主要案例按钮、分类及清除按钮至少 44px。
- 本地浏览器验证 1280/440/320px 无整页横向溢出；制造类 4 条、B 柱检索 1 条、空结果恢复 15 条、收起恢复精选 4 条及标题焦点通过；B 柱详情打开、Escape 关闭并返回按钮通过。桌面/手机截图已目视检查；console error/warn 空，未做 iOS 真机测试。
- iCloud 卸载文件阻塞原依赖和部分源码读取。使用同一锁文件 npm ci，在 /tmp/forflow-cases-build-20261013 独立构建；未修改的卸载文件从 HEAD 还原到临时目录，其余复制当前工作区。15 条目录同步成功，最终 Vite 构建、4 项 Sites 打包测试及 diff 空白检查通过。全站静态检查仍为 workbench_prototype.html 的 3 项既有问题。
- 四个改动文件与临时构建源逐字节相同，前后哈希及截图记录在 output/homepage-v6/design-review/20261013-cases/qa.json。保留 http://127.0.0.1:8899/ 本地预览；本轮未发布远端、未 Git push，未改其他任务的 8903 服务。
- 最终本地服务已切至构建目录，HTTP 200、产物脚本 main-CC2zz9VN.js 与 4 条精选 DOM 可读。切换后 IAB 截图返回与当前 DOM 不一致的旧弹窗画面，未记为构建版视觉验收；视觉交付使用已核对的开发态截图，四个源文件哈希与最终构建一致。

## 2026-10-13 — 企业服务手机对齐与文案简化

- 用户指出五项服务手机未适配，并要求调整同一部分文案。手机元信息置于标题上方，标题、说明、交付项统一左边界，交付项自然换行，收掉占宽图标；桌面排版保留。五项名称保留，说明改为具体工作，交付项明确为清单、规则、记录等；移除重复总介绍及抽象周期标签。
- 维护 templates/index.html 与 assets/site/home-mobile-product.css，homepage-only 生成完成。320/390/440/700/768/1280px 无整页与服务文字横向溢出，手机五项对齐；390px 目视检查并保存截图，console error/warn 空。未做 iOS 真机测试。静态检查仍仅 workbench_prototype.html 三项既有问题。
- 独立预览包相对上一版仅 index.html 与手机样式变化，服务目标链接相同，服务区外首页内容相同，72 个 product/one 文件逐字节相同。QA 保存 home-services-mobile-qa-20261013.json，8903 预览保留。
- 新 draft https://6acdede9c7904eca1f68c174--forflow-enterprise-suite-v3.netlify.app/#services ready；128 个资源 HTTP200/noindex 与逐文件内容回读通过，正式部署未变。回执保存 homepage-guru-preview-mobile-services-20261013.json，未 Git push。

## 2026-10-13 — 产品展示删除无信息量的编号标签

- 用户明确要求删掉“供应商 SUP-018／合同 CTR-1042 · 第 3 版”这类废话。删除工作台标题旁整组标签、续约界面重复编号与公司占位行、资料卡和连接器展示的装饰性编号/版本；展示内容直接指向合同条款、负责团队与待处理事项。内嵌 Q2Q 复核界面同步删除重复合同编号、版本标记，保留条款位置和复核操作；底层记录标识和数据关联未变。
- 修改 WorkspaceStory、Advantages、ConnectedContext、ConnectorSection、public/workbench/q2q-ui.js。复用已建立的独立构建目录；Vite 构建、内嵌 JS 语法、diff 空白检查通过。浏览器回读外层展示及初始内嵌复核页面的目标编号为零；634px 宽度无横向溢出，切换复核章节打开对话框、重播及暂停正常，无流程错误。
- 已更新本地 8899 预览；未发布远端。截图、源文件哈希和验证结果保存在 output/homepage-v6/design-review/20261013-copy-trim/。

## 2026-10-13 — 产品展示继续精简重复说明

- 按用户“还有别的吗”继续通读并落实上一轮文案方向。删除任务卡、列表、详情与处理记录里展示的 CH 编号，以及核验依据中的 Q 编号；保留底层记录标识和交互。删除三场景重复结果总结、显然的操作提示、重复来源标记、连接器英文装饰与通用说明、核验和连接器底部套话、CLI 重复文件名；相应收紧两个窗口高度。
- Vite 构建与 diff 空白检查通过，9 个源文件与临时构建目录逐字节一致。1280px 浏览器无页面横向溢出，目标文案无残留；看板/列表打开正确任务、关闭详情、合同连接器续约字段切换、权限面板、核验依据高亮通过；两个收紧窗口的内容均位于边界内，console error/warn 空。
- 本地 8899 预览已更新；未发布远端。仅本轮差异、前版备份、哈希、截图和验证记录位于 output/homepage-v6/design-review/20261013-copy-trim-followup/。

## 2026-10-14 - Homepage copy cleanup

- Continued the service copy refinement. Removed the visible layout-reference label from the review logo wall, keeping the internal reference-asset markers. Removed repeated SUP/CTR/TK identifiers and version subtitles from the homepage contract walkthrough; source links and review handoff remain functional.
- Shortened diagnosis and implementation copy: select work, verify real tasks, integrate into the team flow, review results. Simplified the resource heading and contact explanation. Sources: templates/index.html, home-workspace.js, package_homepage_review.py. Homepage-only generation completed.
- Browser checks at 320/440/1280px: no horizontal overflow or clipped changed copy. Chapter switch, original-source open/close, task creation, diagnosis expand/choose/next/back with answer retention/collapse, and single-item method expansion passed. Two high-level browser clicks did not execute due to mapping/timeouts; after checking the unchanged state, ordinary same-page DOM clicks completed the interactions and were read back. Console warning/error list empty; desktop/mobile screenshots saved. No iOS device test. JS syntax passed; static check retained only the three pre-existing workbench_prototype.html issues.
- Review bundle changes only index.html and home-workspace.js; 72 pinned product files remain byte-identical. Concurrent product-prototype work was preserved. QA: home-copy-refined-qa-20261014.json. Local preview 8903 remains available.
- Draft https://6ace659b8c55f8a77a789db9--forflow-enterprise-suite-v3.netlify.app ready; 128 served resources verified HTTP200/noindex and byte-equal. Production unchanged; receipt homepage-guru-preview-copy-refined-20261014.json. No Git push.

## 2026-10-14 — 产品原型整页精简与留白调整

- 用户要求整页去重、精简无意义文案，并学习 Qoder / ChatGPT 官网。范围为 output/homepage-v6 独立浅色产品原型；依据官方页面的信息层级，将首屏、场景、流程、能力、资产、治理、连接器、CLI、案例和联系区收为明确标题、必要说明与操作展示。
- 删除三场景六张重复说明卡、流程后的重复总结、章节间重复引导、装饰性序号和预约介绍。连接器合并重复视图入口，保留字段、关联与权限三个页签；工作依据卡片与联系区收紧高度、正文和间距。保留三场景、六类连接器、三类治理、完整 15 条案例及归属。
- Vite 构建与改动文件 diff 空白检查通过，14 个改动文件与临时构建源逐字节一致。IAB 320/440/634/1280px 无整页横向溢出；案例搜索/15 条展开/4 条收起、详情返回、连接器权限切换、治理依据与复测、资产方向键、合同字段定位确认、窄屏详情开关和菜单通过，console error/warn 空。桌面及移动截图目视通过；未测试物理手机。参考官网只核对内容与层级，远程截图获取未成功，不记为像素对齐。
- 本地 8899 预览已更新，构建脚本 main-CUDhrWVI.js；未发布远端、未 Git push，未改 8903 服务。记录位于 output/homepage-v6/design-review/20261014-whole-page/，含前版备份、仅本轮差异、哈希、构建日志、截图和 qa.json。

## 2026-10-14 — ForFlow One 精简版正式上线

- 用户明确要求上线当前产品页。正式发布到 https://forflow.ai/product/one/，生产部署 6acf5716ab87222a3fb75bf0；先在候选 6acf56abb2434905a10f89b3 验证同一 payload，再创建正式部署。仅更新产品目录，原正式站其他 76 个文件、5 个函数的代码/路由/流式模式及边缘访问控制保持一致。未发布并行任务的官网首页草稿。
- 候选和生产的 72 个产品资源 HTTP 200 与内容核对通过；正式域名产品、治理和工作台入口 200，原门禁路径与 gate-login GET 405、无效短链 404 均保持预期，共 11 路径通过。正式域名新 JS/CSS/q2q-ui 逐字节一致，HTML 带现有 Cloudflare 检测脚本。Python 请求被 Cloudflare 1010 拒绝后，普通 curl 请求正常；未修改访问控制。IAB 页面/截图超时，不计远端视觉验收；本轮发布沿用已验本地构建。
- 同步已发布构建到 output/homepage-v6/dist/client，并更新 product-one-source.json 与 product-one-deployment.json；重新打包的 72 个挂载文件逐字节一致。旧回执和本次验证归档在 docs/maintenance/releases/product-one-20261014/。正式站无 Git 自动部署连接，本轮未 Git push。

## 2026-10-14 - Homepage role and status hierarchy

- User flagged the unexplained legal label at the upper right. The walkthrough window bar now shows material/task counts, and the result badge uses a short review state. Role names and duties stay with the review task. Replaced role initial letters with consistent people icons; removed the current-task label, process-stage count, and redundant flow footer.
- Sources: templates/index.html, home-workspace.js/css. Homepage-only generation and JS syntax passed. Removing the footer exposed an old cached JS reference during local reload; changed both asset query versions and verified a fresh page completing the task with an empty warning/error list.
- Measured CSS widths 320/440/927/1279: no page overflow or clipped role text. Task creation, approval-source open/close, and replay resetting the material count passed. Screenshots saved; no iOS device test. Browser bindings/remote reads timed out initially and the local server had stopped; restored 8903 and used a fresh local tab. Static check retained only three pre-existing workbench_prototype.html issues.
- Draft package differs only in homepage HTML and workspace JS/CSS; 72 product files are byte-identical to the previous review package. No production or unrelated product-prototype changes. QA: home-role-labels-qa-20261014.json. The restored local preview remains available.
- Draft https://6acf5cbbfdddea8d01b0eba1--forflow-enterprise-suite-v3.netlify.app/#one ready; 128 resources verified HTTP200/noindex and byte-equal. Current production deployment remained unchanged. Receipt: homepage-guru-preview-role-labels-20261014.json. No Git push.

## 2026-10-14 - Homepage redundant copy cleanup

- User asked for further copy reduction. Removed chapter tutorials outside the workspace, assistant task subtitle, repeated creation receipt, conversation status/attachment footer, original-clause paraphrase and operations next-step footer. Six scenario descriptions now each have one sentence; removed duplicate scenario/mechanism introductions, simplified FAQ heading, and replaced the unverified diagnosis duration with a direct action label. Context tabs now describe the actual contract task.
- Sources: templates/index.html and home-workspace.js. Homepage-only generation and JS syntax passed. CSS viewport widths 320/440/1280: no page horizontal overflow or clipped changed copy. Source open/close, task creation and replay, six scene switches, operations evidence, material-caption update and single-item FAQ expansion passed. Mobile task creation also completed; console warning/error list empty. Screenshots saved; no physical iOS test. Static check retained only the three pre-existing workbench_prototype.html errors.
- Review bundle changes only homepage HTML and workspace JS. All 72 product files remain byte-identical to the previous review bundle; parallel product source and production were not incorporated. QA: home-lean-copy-qa-20261014.json. Local preview 8903 remains available.
- Draft https://6acf622c49d76d543265e009--forflow-enterprise-suite-v3.netlify.app/#one ready; 128 served resources verified HTTP200/noindex and byte-equal. Final source whitespace cleanup produces byte-identical packaged HTML; diff whitespace check passed. Current production remained unchanged. Receipt: homepage-guru-preview-lean-copy-20261014.json. No Git push.

## 2026-10-14 - Public company page release

- User explicitly approved publishing the accepted homepage at forflow.ai/company. Added scripts/package_company.py using the template-generated index as source, with assets isolated under /company/assets, company-local section/brand navigation and a canonical URL. Reference-only Guru customer marks are excluded; actual tool ecosystem marks remain. Added company packaging to build_public.py and scoped Netlify gate exclusions/headers to the new page.
- Current production snapshot 6acf5716ab87222a3fb75bf0 is the base. Candidate preserves 147 existing file digests, all 74 product files and 5 function archives with their routes and invocation modes; only edge exclusions and company headers change. The gated root and unrelated routes stay protected.
- Company package generation, syntax and whitespace checks passed. All 79 asset references resolve; edge exclusion checks distinguish /company from /company-other. Gate static/runtime checks passed. Static site check has only the three existing workbench_prototype.html errors. Browser CSS widths 320/440/1280 have no page overflow; navigation, mobile menu, source open/close, task creation, material caption, scenario switch and review image dialog passed. No failed loaded images or console warnings/errors. Local screenshots saved; no physical iOS check.
- Candidate 6acf73eff889e4d8013bbd54 passed 43 served-file and 13 route checks. Netlify Pretty URLs changed only same-domain .html hrefs and opening anchor quotes; all other HTML parts and 42 assets matched byte-for-byte. Published the identical payload as production 6acf755c573ae60400561b0a. forflow.ai/company and /company/ return 200 without a gate cookie; five custom-domain resources and original gated/functional routes passed. Actual product digests and five functions remain unchanged.
- Formal-domain browser navigation completed, but DOM/screenshot reads and a recovery attempt timed out; not counted as remote visual acceptance. Local screenshots remain the visual record. Release receipt: company-deployment.json; archived sources, payload and QA: releases/company-20261014/. No Git push.

## 2026-10-14 · Q2Q 与企业 AI 资产的说明及交互

- 依据用户提供的资产工程稿，将产品页 Q2Q 的默认概览改为“核对依据 → 记录纠正 → 形成资产 → 再次验证”。借鉴 OpenAI Intelligent UI 的问题与交互表达、TypeSafe Jev 的输入与结构化判断表达，保留现有浅色体系、原三类评估模块及详细工作台。独立治理页仍默认显示评估概览。
- 新增 `output/homepage-v6/src/Q2QAssetCanvas.jsx`、`src/q2q-asset-canvas.css`，调整 `src/GovernanceSection.jsx`；设计与口径来源在 `output/homepage-v6/q2q-assets-design.md`。采购阈值、边界样本和制度变化为编写的本地交互，不是模型、客户效果或资产持久化接入结果。
- 验证：Vite 构建通过；四个步骤、阈值边界、制度变更使结果待复核、产品默认入口及独立治理页共 8 项 React 服务端渲染/状态检查通过；本地两个 HTML 入口及引用资源共 10 项字节回读通过。证据在 `output/homepage-v6/design-review/20261014-q2q-assets/`。
- 根站 `tests/static_check.py` 报告未改动的 `workbench_prototype.html` 缺 stylesheet、search modal、直接 body footer，未扩大修改该独立页面。该检查不扫描本次原型源码。浏览器工具读取当前内部错误页被 URL 安全策略拒绝，已请求用户刷新，未绕过，视觉及浏览器交互验收待补。
- 本地预览 `http://127.0.0.1:8899/#governance` 已更新；本轮未发布，正式站仍保留此前已发布版本。

## 2026-10-15 · Q2Q 资产交互浏览器验证

- 用户确认 Jev 产品官网为参考，并刷新本地预览。继续检查既有四步资产链，保留原有评估与工作台。修复意外显示的表格说明，改用表格无障碍标签；制度变更时保留原候选处理，仅将核验状态置为待复核，便于追查旧判断。
- Vite 构建及 8 项 React 渲染/状态检查重新通过。浏览器验证阈值 100/50 对应 2/3 与 3/3、制度变化、原文工作台往返保留步骤与条件；440 × 956 CSS 视口的章节、放大面板与阈值/制度控件通过，整页无横向溢出；1279 × 1000 桌面截图目视通过。浏览器 warning/error 列表为空。
- 手机截图接口未取得可靠完整画面，未记为完整手机视觉或物理设备验收；Jev 远程页打开超时，未记为像素对齐。截图、当前源文件哈希与详细检查范围保存在 Codex visualizations 的 `q2q-assets-20261015/`。临时视口已恢复，8899 预览可用。只更新本地构建，未发布、未改生产快照。

## 2026-10-18 - Website source sync to GitHub

- User explicitly requested pushing website content to the existing private certrass/forflow-website repository. Prepared an immutable snapshot of the current static homepage/company source, interactive assets, independent ForFlow One source, case catalog, packaging scripts and curated maintenance receipts. Credentials, dependency directories, compiled builds, old screenshot folders and raw release API dumps are outside the new selection.
- The original workspace contains slow-reading historical screenshots; used an isolated Git checkout to preserve its files and index. Remote main was 6ace69e4258cfa36d2c0b7613c2263e03645e30d. Netlify has no Git continuous deployment connection; production deployment remained 6acf755c573ae60400561b0a before the push. This task synchronizes source, not a new website release.
- Homepage generation, 9 homepage JS syntax checks, the current product Vite build, 4 hosting checks and 7 workbench state checks passed. Generation did not change the frozen source bytes. Known credential-pattern scan covered 263 text files with no findings. Existing dependency audit has 1 moderate and 5 high findings on the Vite dependency chain; versions and lockfile were retained rather than upgraded during the source sync. Additional check results are recorded in github-sync-20261018.json.
- Company package rebuilt from the commit source matches all 43 published files. Both gate checks passed. Static check retains only the three pre-existing workbench_prototype.html errors; no new static errors. Whitespace check passed. Production is not redeployed by this source push.
- Push completed: main commit 2aa7dac5c721ff9760697584c220f24ec6d5ec3c. GitHub main and all 222 selected file hashes were read back successfully. Production remains 6acf755c573ae60400561b0a. Local original index/branch were preserved; source push was made from an isolated checkout, so a dirty original checkout alone does not mean the source is absent from GitHub. Receipt: github-push-20261018.json.

## 2026-10-19 · 官网改动默认同步 GitHub

- 用户要求以后每次官网改完都同步到 GitHub，并沉淀重要改动和发布记录。已将日常提交、推送、远端回读及记录范围写入 `AGENTS.md` 和 `site-governance.md`，同时保存项目范围的工作记忆。此约定覆盖日常源码同步，正式发布继续按已授权目标和版本执行。
- 同时补入上次已完成源码推送的回执 `github-push-20261018.json`，使已推送版本与验证记录可从仓库直接查到。
- 本轮只改维护约定、日志及推送回执；文档内容、相对链接、回执 JSON 与提交差异检查通过，不重建、不部署站点。使用隔离检出提交四个项目文件，保留原工作区及其索引；推送完成与远端回读结果以本条对应的 GitHub 提交为准。
