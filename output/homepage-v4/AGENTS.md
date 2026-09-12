# Prototype Instructions

The user reviews remotely. Hand off a verified remote preview URL, not localhost. Continue developing this independent prototype and preserve unrelated production-site changes.

Run the local server yourself and open the preview in the browser available to this environment. Do not give the user server-start instructions when you can run it.

Use the current brief, selected visual source, and project state first. Resolve unclear visual goals through existing context; ask only when a missing choice materially changes the result. Use Product Design for requested design exploration, not as a mandatory gate for routine implementation. Preserve durable prototype-specific feedback in this file without copying generic workflow rules.

When implementing from a selected generated mock, treat that image as the source of truth for layout, component anatomy, density, spacing, color, typography, visible content, and hierarchy.

Build app UI in `src/`. Keep `.openai/hosting.json`, `worker/index.js`, `scripts/prepare-sites-build.mjs`, and `tests/sites-worker.test.mjs` intact so the same local prototype can be handed to Sites. Before a Sites handoff, run `npm run build` and `npm run test:sites`; the build must leave `dist/client/index.html`, `dist/server/index.js`, and `dist/.openai/hosting.json`.
