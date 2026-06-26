# ForFlow 萬維流形企业网站原型

这是在原有静态网站框架上继续完善的响应式企业官网，不依赖前端框架，也没有推倒重做既有页面。本轮重点精修 `index.html` 与 `playbook.html`，其余 11 个页面、链接和交互保持兼容。

## 本轮重点完善

### `index.html` 官网首页

- 新增桌面端三级内容型下拉导航：企业服务、场景与工具、手册与洞察
- 手机端改为可展开的分组菜单，保留搜索和诊断入口
- 重构首屏层级、字距、行距、响应式字号与留白
- 使用提供的手部主视觉、Flow Green 流线和自绘业务图标
- 补齐业务场景、四项服务、Navigator、落地方法、案例、资源、FAQ 与行动入口
- 图标全部为内联 SVG 线性图标，无第三方图标库
- 动效仅用于流线、节点、卡片揭示和导航反馈，并支持 `prefers-reduced-motion`

### `playbook.html` 企业生成式 AI 实战手册

- 直接使用用户提供的完整 `ForFlow + 萬維流形` 封面图，不重新提取或重绘
- 新增固定阅读工具栏、阅读进度、桌面粘性目录和手机目录抽屉
- 按原始 Playbook 的组织方式补齐 6 个章节与章节入口地图
- 补充 AI 演进、AI/ML/深度学习/GenAI 关系、RAG 流程、模型类型、业务价值等示意图
- 完整中文化“购买还是建设”、采用现成方案、定制建设、风险、安全、技能和实施步骤
- 加入可交互的 5 问 Buy / Build 快速判断工具
- 保留原始 PDF 在线阅读和下载入口

## 全站页面

- `index.html`：官网首页
- `navigator.html`：3 分钟 AI 场景诊断
- `navigator-results.html`：推荐结果、品牌视频控件与方案排序
- `playbook.html`：中文企业生成式 AI 实战手册
- `service-ai-enablement.html`：企业 AI 赋能计划
- `service-data-governance.html`：数据治理
- `service-agent-build.html`：企业 Agent 搭建
- `service-ai-training.html`：企业 AI 培训
- `category-hrms.html`：HR AI 场景分类页
- `cases.html`：案例&博客
- `case-wren-kitchens.html`：案例详情结构示范
- `case-manufacturing-pid-intelligence.html`：P&ID 智能化案例 Blog
- `case-healthcare-agent-roi.html`：医疗受限多智能体案例 Blog
- `case-automotive-dfmea-ontology-agent.html`：汽车 B 柱 DFMEA 本体智能体案例 Blog
- `case-supply-chain-agentic-decision.html`：供应链多智能体决策案例 Blog
- `case-financial-bda-document-automation.html`：金融文档 BDA 自动化案例 Blog
- `case-vanguard-virtual-analyst.html`：先锋集团虚拟分析师案例 Blog
- `case-agent-evaluation-first.html`：企业 Agent 评估先行案例 Blog
- `contact.html`：方案沟通与联系方式
- `search.html`：全站搜索结果页
- `document-viewer.html`：PDF 在线阅读器

## 运行

```bash
python -m http.server 8080
```

打开 `http://localhost:8080/`。

## Veee 代理应急

如果切换 Veee 节点后 GitHub、Netlify、npm 或 curl 连接异常，先用项目内包装器自动刷新当前代理端口：

```bash
tools/with-veee-proxy.sh gh auth status -h github.com
tools/with-veee-proxy.sh git ls-remote https://github.com/octocat/Hello-World.git HEAD
tools/with-veee-proxy.sh curl -I --max-time 12 https://github.com
```

也可以把当前 Veee 端口导入当前 shell：

```bash
eval "$(tools/veee-proxy-env.sh)"
```

## 复核与测试

- `python3 build_site.py`：根据 Python 清单重建一级页面、案例&博客和搜索页
- `python3 tests/static_check.py`：15 个 HTML 页面、本地资源、必需模块、案例清单联动检查
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9226 python3 tests/interaction_check.py`：搜索、手机菜单、Navigator、FAQ、筛选、案例与搜索联动等全站交互
- `BASE_URL=http://127.0.0.1:8765 CDP_PORT=9226 python3 tests/polished_pages_check.py`：首页、Playbook、案例&博客和医疗案例的视口、图片、控制台与关键交互复核
- 专项视口：桌面 `1440 × 1000`、手机 `390 × 844`
- 如果本地服务或调试浏览器端口变化，只改 `BASE_URL`、`CDP_PORT` 或 `CDP_URL`

## 维护说明

`build_site.py` 继续负责其余页面的静态生成；精修后的首页、Playbook 和 README 保存于 `templates/`，重新执行生成脚本时会自动恢复，避免复杂页面被旧模板覆盖。

案例&博客由 `build_site.py` 里的 `CASE_LIBRARY_ITEMS` 统一维护。新增案例或博客时先创建 `case-*.html` 详情页和封面图，再在清单里补一条数据；运行 `python3 build_site.py` 后，`cases.html`、`search.html`、导航 active 状态和静态检查会同步更新。

完整网站维护治理见 `docs/maintenance/site-governance.md`。每次更新页面、样式、图片、脚本、测试或部署后，都要在 `docs/maintenance/update-log.md` 追加记录，写清变更范围、主要变更、真实验证结果和后续事项。

发布前至少确认：

- 更新已写入 `docs/maintenance/update-log.md`
- `python3 build_site.py` 已重新生成站点
- `python3 tests/static_check.py` 已通过
- 涉及交互、手机端、图片或布局时，已运行 `tests/interaction_check.py` 和 `tests/polished_pages_check.py`

上线前仍需补齐表单接口、CRM/CMS、隐私条款与部署域名。
