# ForFlow 网站维护治理

这个网站正在从静态原型走向完整官网。维护目标不是“页面能打开”就结束，而是让内容来源、生成入口、交互验证、视觉资产和部署记录都可追踪、可复查、可持续迭代。

## 维护原则

- 单一来源优先：能进入清单、模板或脚本的数据，不在多个 HTML 里手工重复维护。
- 每次更新后留痕：所有页面、样式、图片、脚本、测试和部署改动，都要写入 `docs/maintenance/update-log.md`。
- 先改来源，再改产物：由 `build_site.py` 生成的页面，应优先改 Python 清单或模板，再重新生成 HTML。
- 验证覆盖真实使用：桌面、手机、导航、搜索、筛选、滚动、图片加载和控制台错误都需要纳入检查。
- 外部口径谨慎：客户可见页面避免未经验证的数据、夸大 ROI、含混授权或内部 BP 表述。

## 权威维护入口

| 维护对象 | 权威入口 | 生成/验证方式 |
| --- | --- | --- |
| 首页 | `templates/index.html` | `python3 build_site.py` 后复制到根目录 |
| Playbook | `templates/playbook.html` | `python3 build_site.py` 后复制到根目录 |
| README | `templates/README.md` | `python3 build_site.py` 后复制到根目录 |
| 服务页、分类页、搜索页、案例中心 | `build_site.py` | 运行 `python3 build_site.py` |
| 案例列表与搜索联动 | `build_site.py` 的 `CASE_LIBRARY_ITEMS` | `cases.html`、`search.html` 自动更新 |
| 案例详情页 | `case-*.html` + 对应图片资产 | 静态检查、交互检查、视觉检查 |
| 样式与交互 | `styles.css`、`script.js` | Playwright/CDP 检查和本地浏览器检查 |
| 更新记录 | `docs/maintenance/update-log.md` | `tests/static_check.py` 检查结构 |

## 更新流程

### 更新留痕

每次更新交付前，都要先在 `docs/maintenance/update-log.md` 追加记录。记录应能回答：改了什么、为什么改、影响哪些维护入口、跑过哪些验证、还有哪些后续事项。

1. 判断改动类型：内容、案例、视觉、交互、生成脚本、测试、部署或文档治理。
2. 找到权威入口：不要直接改一个会被生成脚本覆盖的产物。
3. 实施改动：保持页面、模板、清单和资源命名一致。
4. 运行生成：`python3 build_site.py`。
5. 运行基础检查：`python3 tests/static_check.py`。
6. 对交互或视觉相关改动，启动稳定本地服务并运行浏览器检查：

```bash
python3 -m http.server 8765 --bind 127.0.0.1
BASE_URL=http://127.0.0.1:8765 CDP_PORT=9226 python3 tests/interaction_check.py
BASE_URL=http://127.0.0.1:8765 CDP_PORT=9226 python3 tests/polished_pages_check.py
```

7. 更新 `docs/maintenance/update-log.md`，写清变更、验证结果和后续事项。
8. 部署或交付前，确认本地临时服务、调试浏览器和代理排查进程没有残留。

## 案例治理

新增案例时必须同时维护：

- `case-*.html`：详情页正文、图文结构、目录和 CTA。
- `assets/cases/`：封面图、正文图，命名使用案例主题前缀。
- `CASE_LIBRARY_ITEMS`：案例中心卡片、筛选标签、搜索词、搜索标题和描述。
- `docs/maintenance/update-log.md`：记录案例来源、更新内容和验证结果。

案例页应回答：

- 业务问题是什么。
- 为什么这个场景适合 AI 或 Agent。
- 人、模型、系统和数据的边界在哪里。
- 产出的证据是什么。
- 如何验收、复评、升级人工或停止扩展。

## 视觉治理

- 视觉优先使用中国企业或中国业务场景。
- 生成图尽量避免可读文字，防止尺寸缩放、方向和字体生成问题。
- 医疗、工业、金融、政务等高合规场景，应表现流程、证据和复核点，而不是夸张的未来感控制台。
- 图片进入页面前要确认桌面与手机端比例、裁切、加载状态和横向溢出。

## 发布门禁

发布前至少通过：

- G0 生成：`python3 build_site.py`
- G1 静态：`python3 tests/static_check.py`
- G2 交互：`tests/interaction_check.py`
- G3 视觉与滚动：`tests/polished_pages_check.py`
- G4 留痕：`docs/maintenance/update-log.md` 已记录本次更新
- G5 部署：Netlify 或其他部署结果已记录链接和时间

未通过的门禁需要写入更新记录的 `后续`，不能在最终说明里当作已完成。

## 代理与外部服务

如果 GitHub、Netlify、npm 或 curl 失败，先检查 Veee 当前代理端口：

```bash
tools/with-veee-proxy.sh gh auth status -h github.com
tools/with-veee-proxy.sh curl -I --max-time 12 https://github.com
eval "$(tools/veee-proxy-env.sh)"
```

代理端口会随节点切换变化，不要把旧端口写死到文档、脚本或部署配置里。
