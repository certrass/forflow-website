# ForFlow homepage v6 — design QA

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
