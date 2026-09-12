# Prototype Instructions

The user reviews remotely. Hand off a verified remote preview URL, not localhost. Continue developing this independent prototype and preserve unrelated production-site changes.

Run the local server yourself and open the preview in the browser available to this environment. Do not give the user server-start instructions when you can run it.

Use the current brief, selected visual source, and project state first. Resolve unclear visual goals through existing context; ask only when a missing choice materially changes the result. Use Product Design for requested design exploration, not as a mandatory gate for routine implementation. Preserve durable prototype-specific feedback in this file without copying generic workflow rules.

When implementing from a selected generated mock, treat that image as the source of truth for layout, component anatomy, density, spacing, color, typography, visible content, and hierarchy.

Build app UI in `src/`. Keep `.openai/hosting.json`, `worker/index.js`, `scripts/prepare-sites-build.mjs`, and `tests/sites-worker.test.mjs` intact so the same local prototype can be handed to Sites. Before a Sites handoff, run `npm run build` and `npm run test:sites`; the build must leave `dist/client/index.html`, `dist/server/index.js`, and `dist/.openai/hosting.json`.

Product showcase direction: use the live Attio workflow, record-list, and record-detail sections as visual references. The previous shared chat window across three scenarios was rejected. Give each business action its appropriate product interface, with readable density, real interaction states, and concise case attribution.

2026-09-06: The user explicitly selected Attio run-sales-motions, Dataify, and the supplied Databricks governance GIF as UI references. Match layout proportions, readable text, dense application components and continuous demonstration states. Keep ForFlow content and case provenance. Consulting diagnosis is not assumed to be the primary commercial entry.

2026-09-06: On small screens, product showcases must retain their spatial meaning. Preserve the complete dashboard, horizontal workflow stages, side-by-side document/field review and drawing/relationship view. Default to a fitted whole-scene composition with a working detail viewer and horizontal pan; do not collapse product interfaces into stacked mobile cards. Use selective 3D illustration/modeling to explain relationships, with presentation quality as the first priority.

2026-09-06: Keep the marketing page and product scenes free of repeated prototype labels such as 演示数据、示例数据、概念预览 and local-state disclaimers. Use normal product labels and actions. Keep source/prototype provenance in maintenance documentation; retain accurate case attribution and necessary business review states.

2026-09-10: The user rejected ornamental generated paper stacks, sculptures and studio photography in the product UI. Keep the homepage Q2Q and CLI showcases as coherent native application windows. Learn Sana/Attio through typography, spacing, restrained borders and real interaction hierarchy; do not add decorative generated elements to this product presentation.

2026-09-12: Homepage preview handoffs should use the root URL, without a scenario hash. Touch scrolling across a showcase is browsing, not manual takeover: pause on actual product-control activation. Verify mobile device mode and real touch gestures, including the 440 × 956 layout; keep mobile chapter labels out of the transport row and avoid overlapping words during hero transitions.
