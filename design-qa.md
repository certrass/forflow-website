# Design QA

- Source reference: `/var/folders/l0/9_h89x255qx_3ktxr85ryxlw0000gn/T/codex-clipboard-5af83eb8-5a6d-4742-a267-b7162d3b1ddd.png`
- HR implementation: `/tmp/forflow-hr-v2-desktop-final.png`
- Full-view comparison: `/tmp/forflow-hr-reference-vs-implementation-final.png`
- Focused workbench comparison: `/tmp/forflow-hr-workbench-focus-compare-final.png`
- Homepage six-choice desktop: `/tmp/forflow-home-six-final-visible.png`
- Homepage six-choice mobile cards: `/tmp/forflow-home-six-mobile-cards.png`
- Reference viewport: 1488 x 1058
- Responsive check: in-app browser mobile override, effective CSS viewport 424 x 917
- State: employee service selected by default

## Full-view comparison

The reference and implementation were placed side by side in the same image. The implementation keeps the selected reference structure: compact breadcrumb and title, six-stage tab rail, one active scenario workbench, four responsibility columns, an evidence strip, and a three-step starting guide. The final pass reduced the title scale and vertical gap so the stage rail and workbench align more closely with the source density.

## Focused workbench comparison

The focused side-by-side crop confirms that the active employee-service state, column hierarchy, evidence area, light borders, green accent, and CTA placement remain legible without reproducing the reference's decorative arc. The implementation uses the site's existing icon sprite and button system.

## Interaction and responsive checks

- Six stage tabs and six matching workbench panels are present.
- Clicking Training Development changes `aria-selected`, the visible panel, and the title to `岗位学习与领导力陪练`.
- Eight HR system cards are present.
- Desktop document overflow is 0 px.
- Homepage challenge entry count is six; enterprise service count remains five.
- Homepage challenge cards render as two columns on desktop and one column at the mobile breakpoint.
- Mobile card text, icons, labels, and CTA fit without horizontal document overflow.

## Comparison history

1. First HR pass preserved the structure but made the title too large and pushed the workbench too low.
2. Final HR pass reduced title scale and intro spacing, then repeated the combined full-view and focused comparisons.
3. First homepage mobile pass exposed a heading that was too wide; the heading size and kicker length were reduced, then the single-column cards were recaptured.

## Findings

- No remaining P1 or P2 visual issues in the implemented scope.
- Rippling and Factorial use published remote logo assets; production deployment should keep network access available or replace them with locally licensed files later.

Final result: passed
