# ForFlow homepage v4 — design QA

Date: 2026-09-05

## Scope and target

A local interactive homepage prototype, using the live Attio homepage as the main composition reference and existing ForFlow branding, case content, and P&ID imagery. This is an intentional adaptation for ForFlow, not a pixel-identical clone. Scenario outputs are demonstration data. Confirmation controls change local UI state only; they do not submit business actions. Existing ForFlow pages supply the case and contact destinations.

## Visual evidence

- Reference: `attio-reference-top.png`, captured from the live Attio homepage in Chrome at the same 822 × 768 native screenshot dimensions as the final prototype capture.
- Latest implementation: `implementation-top-final.png` and `implementation-product-final.png`.
- Side-by-side comparison: `reference-comparison-final.png`. Both screenshots crop the same 134 px of browser chrome. This comparison was opened and inspected together.
- Desktop full page: `forflow-v4-desktop-final.png`, 1440 CSS px viewport width, DPR 2 (2880 × 9084 image). The latest native captures additionally verify the subsequent reduction in hero spacing; this full-page capture precedes that spacing adjustment.
- Mobile full page: `forflow-v4-mobile-final.png`, 390 × 844 CSS px viewport, DPR 2 (780 × 9916 image). Mobile layout was inspected at readable scale using `forflow-v4-mobile-final-top.png`.
- Additional state captures: `implementation-docs.png`, `implementation-evidence.png`, `implementation-capabilities.png`, `implementation-evaluation.png`, and `implementation-cases.png`.

## Comparison and fixes

| Surface | Observation and disposition |
| --- | --- |
| Typography | Inter used for Latin text with a native Chinese fallback. Centered headline, short gray supporting copy, and compact CTA hierarchy follow the reference. Chinese character metrics and line breaks are intentionally adapted. Product text was enlarged and secondary text darkened after the first screenshot exposed weak readability. |
| Spacing and layout | Hero-to-product whitespace was reduced after the combined comparison. Product frames use one consistent workspace, with supporting process and approval windows. Desktop main window height increased to separate the evidence link from the composer. |
| Color and borders | Neutral black/white shell, light gray borders, and restrained green states use ForFlow branding. The reference's lavender background is an intentional difference. |
| Images and icons | Existing ForFlow wordmark and actual P&ID asset are used with preserved proportions. Phosphor supplies icons. No generated whole-page mock is used as a substitute for working UI. |
| Copy and hierarchy | Business task → product output → evidence → human confirmation → full case. No invented ROI, customer quote, or performance claim. |

Resolved findings:

- P2: small, low-contrast product labels — enlarged and darkened.
- P2: mobile approval panel covered the main output and composer — moved below the main product window at narrow widths; checked again.
- P2: desktop composer competed with the evidence area — main window height increased; verified in the final product capture.
- P2: excessive gap above the product relative to the reference — reduced hero/demo spacing and compared again.

No unresolved P0–P2 layout or core interaction defects were observed in the checked states. Further brand and visual preference refinement remains a design decision; this report does not claim the user has approved the aesthetic direction.

## Functional checks

Verified in native Chrome:

- Scenario selection updates the query, answer, output, sources, process steps, and relevant case destination.
- Replay advances through the local process and restores the completed state; conflicting controls are disabled while running.
- Human confirmation switches to the confirmed state and can be undone locally.
- Evidence modal opens with source details and a case link; Escape closes it. Focus containment and restoration are implemented.
- Capability tabs change the displayed knowledge, workflow, and evaluation content.
- Narrow-screen navigation opens and closes; Escape dismisses it.
- Console after reload showed no JavaScript errors. Initial missing favicon request was fixed with an explicit favicon asset.
- Local preview returned HTTP success at `http://127.0.0.1:8894/`.
- Final `npm run build` passed (Vite build and starter hosting preparation).

## Boundaries

No backend integration or production deployment is included. An independent Netlify deploy preview is available for remote review. Case/contact links continue to the existing ForFlow website and can require its access gate. Full-page screenshots document the captured states rather than every possible browser/device combination. Final aesthetic acceptance remains with the user.

## Remote review content update

Added scenario-specific explanations for the business problem, deliverable, and validation method. The three descriptions use the existing supply-chain, document-automation, and P&ID case pages as content sources, with their different attribution retained. Service stages now specify reviewable deliverables. Four expandable questions cover delivery scope, scenario choice, system integration, and value measurement.

The current content build passed. New content was checked in the native Chrome desktop viewport; evidence: `remote-content-context.png`, `remote-content-delivery.png`, and `remote-content-faq.png`. The first FAQ was expanded and its answer verified. Existing mobile QA above applies to the prior layout; the content additions have responsive rules but this update has not yet received a fresh mobile visual check.

## Remote deployment verification

- URL: https://6a9ba5a7a3128710a3261c29--forflow-enterprise-suite-v3.netlify.app
- Netlify state: `ready`; context: `deploy-preview`.
- Homepage and checked JS, CSS, P&ID, and wordmark resources returned HTTP 200. Downloaded resources matched the validated local build by SHA-256.
- The production published deploy remained unchanged.
- Preview response includes `X-Robots-Tag: noindex, nofollow`.
- The remote bundle is identical to the locally inspected content build; a fresh remote browser render was unavailable after the native browser surface stopped returning UI state.

final result: passed
