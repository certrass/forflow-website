# ForFlow homepage v6 — design QA

## 2026-09-12 — 本轮 Attio 实测细化

Preview: https://6aa520f0f0b7211b123168d8--forflow-enterprise-suite-v3.netlify.app/

参考由当日 Attio 官网原生截图、公开 HTML/CSS共同构成。图库位于 `design-review/20260912-attio/`，仅保留作项目内设计依据，不在公开站点发布参考图。原站截图为 1316×768（含浏览器栏）；实现对照按约 1316×636 内容视口规范化，构图状态不同，不将对照描述为逐像素差分通过。

| 检查项 | 参考和改动 | 验证结论 |
| --- | --- | --- |
| 章节栅格 | Attio 24 列、左栏 6 列；改为贯穿的 25/75 布局 | 截图核对，边线和目录连续 |
| 标题与正文 | 原站章节 24px；中文 26px / 13px，主次句用深浅两级 | 桌面与手机实看，窄屏不重叠 |
| 首屏窗口 | 36px 按钮、10px 圆角、6px 外框内衬、竖纹淡色底景 | 真实工作台保留，未新增装饰图片 |
| 目录定位 | 垂直指示改用 offsetTop/height；手机仍横排 | 文档锚点约 111px，含 60px 页头与 51px 目录 |
| 产品操作 | 自动推进、核对下一项、来源同步、手动接管 | 本地交互通过 |
| 手机细节 | 完整横向画布、放大和平移、占位与返回 | 关闭前后 scrollY 均 2191.71，当前仍为文档处理 |
| 资源与构建 | 真实工作台源和适配副本 15 对 | 哈希一致；构建和 4 项打包测试通过 |
| 发布 | 39 个文件回读，console error/warn 空 | 字节一致、HTTP200、noindex；生产未变 |

已修复：重复页头偏移、展开时缺少占位和关闭后的阅读位置恢复。保留的差异：中文标题原文与轮换顺序、真实 workbench 的业务层级和绿色状态、三个业务场景和现有案例。没有引入 Attio 客户标识或其业务数据。

边界：远端导航和截图调用超时，浏览器清单已显示新 URL/标题，实际视觉和交互检查在同构本地构建完成。iOS Safari 实机未测；本轮工具不支持 touch dispatch。用户浏览器的临时 viewport 已恢复默认；截图缩放不用于推断用户的默认浏览器字号。本轮只记录通过的实际检查，不沿用下方历史版本的结果。

## 历史设计 QA（此前版本，保留原记录）

final result: passed

Scope: the independent homepage prototype, its reference-led composition, responsive layout and core demonstration interactions. This result does not imply user aesthetic approval, production readiness or pixel-identical replication of the source sites.

## Reference comparison

- Captured and opened the live Attio sales-motions section and Dataify hero/product sections. Inspected six frames of the user-provided Databricks Governance Hub GIF.
- Opened combined reference/implementation comparisons in `compare-attio.png` and `compare-governance.png`. Source browser chrome was excluded from the product crops; panels were normalized to comparable widths. The source and ForFlow data/content differ intentionally.
- Attio informs the left scenario rail, concise lead, broad product canvas, task columns and supporting benefit panels. The ForFlow rail is narrower to preserve a larger Chinese work surface.
- Dataify informs the Chinese serif emphasis and grouped product explanation. No Dataify artwork, logo or business claims are reused.
- Databricks informs the dashboard anatomy: metrics, blue charts, recommendations and drill-down. ForFlow adds a persistent workspace sidebar and a capability-asset table.
- After the first comparison, increased desktop task, table, chart and detail typography, reduced fading of background tasks, and fixed the platform anchor offset. Reopened the final desktop/mobile captures and combined comparisons.
- Final captures: `desktop-final.png` at 1440 px and `mobile-final.png` at 390 px. The mobile capture was repeated from a fresh top-of-page URL to eliminate a preserved-scroll/sticky-header capture artifact. No clipping or horizontal overflow found in inspected states.

## Interaction checks executed in Chrome

- Fresh workflow demonstration reached human review. Confirming CH-024 moved it to completed handoff; completed count became 2. Controls support board/list, review filter, reset and task detail.
- Document scene: original clause/field selection, payment-condition confirmation and undo control.
- Engineering scene: image zoom to 120% and upstream equipment relationship selection.
- Dashboard: running-analysis drill-down, 7-day range showing 6,220 demonstration calls, usage switch, asset view, search empty state and reset.
- Mobile: menu opens, business-scene navigation closes it, and document scene selection updates correctly. Both overall and document-scene page widths equal the 390 px viewport.
- Desktop page width equals the 1440 px viewport. Browser error/warning log returned an empty list at the end of local checks.
- Existing case, service and contact URLs remain the destinations; no new backend business actions are submitted.

## Build, assets and limits

- `npm run build`: passed. Vite reports a nonblocking JavaScript chunk-size advisory (about 525 kB before gzip); no runtime failure was observed. The prototype retains the prior scene dependency stack.
- Existing ForFlow logo, local fonts and P&ID drawing are retained. Product interfaces are HTML controls; quantitative charts use Chart.js. Reference screenshots and the supplied GIF are not deployed as ForFlow product assets.
- Demonstration values are explicitly labelled. No customer ROI or actual product-launch claim was added.
- An initial dependency install targeted the workspace root accidentally; the newly created root package files were removed and the four pre-existing dependency packages restored from their cached exact releases. Chart.js is installed within v6.
- Deployment state and byte-for-byte remote asset verification are recorded in `remote-preview.json`.

Remote preview: https://6a9c4fe386e46c614cc0ecaf--forflow-enterprise-suite-v3.netlify.app/

Remote verification: all 7 deployed HTML, JavaScript, CSS, font and image files returned HTTP 200, matched the staged build byte for byte, and included the noindex header. The production deployment ID remained unchanged. The Chrome tab inventory confirmed navigation to the new remote URL and the ForFlow page title; the subsequent browser bridge timed out, so post-deployment visual and interaction checks were not completed. Local rendering/interactions above were verified against the identical deployed build.

2026-09-06 后续空间展示与 3D 迭代的当前验证、视觉依据和远程链接见 `design-qa-spatial.md`。本文件前文为初版 v6 检查记录。
