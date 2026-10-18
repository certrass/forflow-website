# ForFlow One mechanism section — review preview

- Scope: homepage `#platform`, adapting the Qoder “How it works” composition to the accepted ForFlow dark-green homepage. This is a scoped design adaptation, not a whole-site or pixel-identical clone.
- Source visual truth: Qoder bento screenshot supplied in the conversation; https://qoder.com/zh/qoder. The historical attached file is no longer present at its supplied temporary path. The official page copy was read this turn; remote browser navigation timed out.
- Actual product sources opened: `/Users/zezhou/Documents/ChatGPT/Forflow One/outputs/ip-20260928-expanded/figures/forflow-one/FO-01_初次启动与智能体选择.png`, `FO-05_选取审阅材料.png`, `FO-07_查看判断与登记问题.png`.
- Rendered implementation: http://127.0.0.1:8903/#platform
- Implementation screenshot paths: `/private/tmp/forflow-guru-iteration/evidence/mechanisms-tablet.png`, `/private/tmp/forflow-guru-iteration/evidence/mechanisms-mobile.png`.
- Browser CSS viewports: 1440 × 1000, 1063 × 1000, 440 × 956, 390 × 844. Host devicePixelRatio is approximately 1.93. Host screenshots crop large emulated viewports; screenshots plus DOM geometry were used for implementation checks. CDP screenshot normalization returned incorrect regions and was discarded.
- State: agent selection, task-step selection, project context, file/browser/terminal panels, review image switching, native full-image dialog.

## Comparison history and fixes

1. P2: Agent menu rows inherited tall line heights and displaced the bottom link. Set explicit 18px / 13px type line heights. Post-fix menus retain the link and bottom padding.
2. P2: Upper card contents were taller than their track, and keyboard focus scrolled clipped cards internally. Increased upper row to 310px and applied overflow:clip. Post-fix 1440px / 1063px / 440px / 390px checks have no card content overflow or page horizontal overflow after animations settle.
3. P1: Actual PNG screenshots retained HTML height attributes when width changed, stretching the interface. Set height:auto. Verified rendered width/height matches source ratio and visually reread material selection.
4. P2: Phone image dialog initially showed the sidebar. It now starts at the main product pane, includes horizontal-pan guidance, and returns focus to its opener on Escape.

## Required fidelity surfaces

- Typography: inherited ForFlowInter + PingFang SC fallback; main heading 32–52px, card headings 21–27px, body 14px. Explicit menu label line heights prevent unintended card growth. Existing homepage type retained intentionally.
- Layout: asymmetric three-column desktop composition (two tall cards and a stacked middle), full-width review below; two-column intermediate layout and individually readable mobile cards. Product captures remain horizontally pannable in mobile dialogs. No internal product UI reflow into arbitrary stacked columns.
- Color: restrained off-white / grey-green cards, one green execution card, dark homepage background. Intentional deviation from Qoder's white page to preserve accepted site style.
- Image quality: three authentic, unchanged product captures, hash-verified against local source. No upstream Orca screenshot or generated fake product UI used. Browser/file/terminal card is an interactive explanatory fragment, not a claim of a recorded live session.
- Copy: concrete agent choice, task steps, materials, tools and human review. Qoder's Auto model routing, voice pet and live team chat were not imported as ForFlow capability claims.

## Implementation verification

Agent/menu selection, four step controls, pause/resume, context buttons, tool tabs, keyboard arrows, review tabs, three original image sources, dialog focus/Escape restoration, phone pan position and reduced-motion manual stepping were checked through IAB. Reduced-motion active animations in this section: 0. Console errors/warnings: none. Build and JS syntax passed. Static check reports only the three documented unrelated workbench_prototype.html errors. 72 product-page bundle files match the preceding draft byte-for-byte. Physical iOS device testing was not performed.

## Full-view comparison gate

The strict same-input, matched-density source-versus-implementation image comparison is not complete: the source attachment file has expired and large host screenshots are cropped. No pixel-level fidelity claim is made. The working preview and implementation checks are available for user review; this does not certify a 1:1 reproduction.

final result: blocked
