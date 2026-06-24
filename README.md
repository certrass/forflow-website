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
- `cases.html`：案例中心
- `case-wren-kitchens.html`：案例详情结构示范
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

- `tests/static-check-report.txt`：13 个 HTML 页面、本地资源、必需模块检查
- `tests/interaction-check-report.json`：搜索、手机菜单、Navigator、FAQ、筛选等全站交互
- `tests/polished/polished-check-report.json`：首页与 Playbook 专项复核
- 专项视口：桌面 `1440 × 1000`、手机 `390 × 844`
- 专项检查通过：下拉导航、Escape 关闭、搜索弹层、手机菜单、手机目录、Buy / Build 判断、阅读进度
- 两个精修页面均无横向溢出、图片丢失或控制台错误

## 维护说明

`build_site.py` 继续负责其余页面的静态生成；精修后的首页、Playbook 和 README 保存于 `templates/`，重新执行生成脚本时会自动恢复，避免复杂页面被旧模板覆盖。

公开案例与外部参考资料用于页面结构和内容组织示范。正式发布前仍需复核内容授权、最新数据、表单接口、CRM/CMS、隐私条款与部署域名。
