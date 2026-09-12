# ForFlow Enterprise Agent Service Page Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `service-agent-build.html` into the first service-detail page that keeps ForFlow's sharpness while reducing simultaneous highlights, tightening the copy, and giving photography and technical diagrams distinct jobs.

**Architecture:** Keep `build_site.py` as the source of truth. Add a small `pilot` variant to the shared `service_page()` generator, and layer scoped overrides through a new `visual-system.css` loaded after the existing stylesheet. The pilot must not change the other four generated service pages until the user approves the result.

**Tech Stack:** Static HTML, Python 3, BeautifulSoup, CSS, vanilla JavaScript, Netlify public build, existing Python and Node regression checks.

## Global Constraints

- Preserve the ForFlow black, white, and green brand system and the current logo.
- Keep exactly one Hero-level heading on the pilot page.
- Keep no more than one solid green primary CTA in the visible service-page content at a time; secondary actions use outline or text treatment.
- Keep exactly one black high-weight content section; the utility bar does not count.
- Keep no more than two English uppercase kickers on the page.
- Desktop page H1 stays within 52–68px; section H2 stays within 36–48px. Mobile H1 stays within 40–48px; H2 stays within 30–36px.
- Use restrained, high-key editorial business photography to explain the work setting and a technical diagram to explain the system path. Do not introduce a fake product UI or autoplay brand motion on this service page.
- `humanizer-zh` is a candidate-problem scanner only. Business facts, evidence boundaries, client comprehension, and human review decide the final copy.
- Do not modify the remaining service-page output until the pilot receives visual approval.

---

## File Structure

- Create `visual-system.css`: scoped tokens and pilot-only service page presentation.
- Create `tests/service_page_pilot_check.py`: static contract for structure, highlight budget, asset roles, copy, and responsive CSS.
- Create `assets/service-agent/forflow-agent-workflow-hero-v1.png`: original Sana-referenced editorial hero generated specifically for this slot.
- Create `assets/service-agent/forflow-agent-workflow-system-v1.png`: original text-free technical path generated specifically for the proof section.
- Modify `build_site.py`: add the stylesheet link, add pilot asset parameters, mark the Agent service call as the only pilot, and generate the pilot markup.
- Modify `styles.css`: only if an existing unscoped rule prevents the scoped layer from working; otherwise leave it unchanged.
- Generate `service-agent-build.html`: output only, never edit directly.
- Modify `docs/maintenance/update-log.md`: record source files, generated output, and verification.

## Task 1: Add a failing pilot contract and the scoped stylesheet layer

**Files:**
- Create: `tests/service_page_pilot_check.py`
- Create: `visual-system.css`
- Modify: `build_site.py:16-18, 631-650, 652-717`

**Interfaces:**
- Consumes: `build_site.py::page()` and `build_site.py::patch_existing()`.
- Produces: a `visual-system.css?v=<ASSET_VERSION>` link on generated pages and a test entry point run as `python3 tests/service_page_pilot_check.py`.

- [ ] **Step 1: Write the failing structural test**

Create `tests/service_page_pilot_check.py` with this exact content:

```python
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "service-agent-build.html"
CSS = ROOT / "visual-system.css"


def fail(message):
    raise AssertionError(message)


soup = BeautifulSoup(PAGE.read_text(encoding="utf-8"), "html.parser")
body = soup.body
if not body or "service-page--pilot" not in body.get("class", []):
    fail("Agent service page must be the only service-page--pilot page")

styles = [link.get("href", "").split("?")[0] for link in soup.select('link[rel="stylesheet"]')]
if "visual-system.css" not in styles:
    fail("Pilot page must load visual-system.css after styles.css")

if len(soup.select("main h1")) != 1:
    fail("Pilot page must contain exactly one main H1")
if len(soup.select('main [data-visual-role="proof"]')) != 1:
    fail("Pilot page must contain exactly one proof region")
if len(soup.select('main [data-asset-role="business-photo"]')) != 1:
    fail("Pilot page must contain one business photo")
if len(soup.select('main [data-asset-role="technical-diagram"]')) != 1:
    fail("Pilot page must contain one technical diagram")
if soup.select('main [data-asset-role="product-ui"], main [data-asset-role="brand-motion"]'):
    fail("Pilot page must not fake product UI or add brand motion")

visible_copy = soup.main.get_text(" ", strip=True)
required_copy = [
    "先选一条真实流程，验证 Agent 能不能稳定完成任务。",
    "两周后，企业要拿到继续、调整或停止的依据。",
    "开始前，请准备这四项信息",
]
for phrase in required_copy:
    if phrase not in visible_copy:
        fail(f"Missing approved pilot copy: {phrase}")

if not CSS.exists():
    fail("visual-system.css is missing")
css = CSS.read_text(encoding="utf-8")
for token in ("--type-page-title", "--type-section", "--radius-card", "--surface-proof"):
    if token not in css:
        fail(f"Missing visual-system token: {token}")
for selector in (".service-page--pilot", "@media (max-width: 640px)", "@media (prefers-reduced-motion: reduce)"):
    if selector not in css:
        fail(f"Missing pilot CSS contract: {selector}")

print("OK: service page pilot structure, assets, copy, and visual tokens")
```

- [ ] **Step 2: Run the test and verify the expected failure**

Run:

```bash
PYTHONPATH=.python-deps python3 tests/service_page_pilot_check.py
```

Expected: FAIL with `Agent service page must be the only service-page--pilot page`.

- [ ] **Step 3: Add the stylesheet link contract to the generator**

In `build_site.py`, keep `ASSET_VERSION`, then add:

```python
VISUAL_SYSTEM_VERSION = ASSET_VERSION
```

In `page()`, place this immediately after the existing `styles.css` link:

```html
<link rel="stylesheet" href="visual-system.css?v={VISUAL_SYSTEM_VERSION}">
```

In both `patch_existing()` and `version_asset_links()`, ensure exactly one `visual-system.css` link exists after `styles.css` and receives the current version:

```python
visual = soup.find("link", href=lambda value: value and value.split("?")[0] == "visual-system.css")
if not visual:
    visual = soup.new_tag("link", rel="stylesheet", href=f"visual-system.css?v={VISUAL_SYSTEM_VERSION}")
    style = soup.find("link", href=lambda value: value and value.split("?")[0] == "styles.css")
    if style:
        style.insert_after(visual)
    else:
        soup.head.append(visual)
else:
    visual["href"] = f"visual-system.css?v={VISUAL_SYSTEM_VERSION}"
```

- [ ] **Step 4: Create the scoped token file**

Create `visual-system.css` with this initial content:

```css
:root {
  --type-page-title: clamp(3.25rem, 5vw, 4.25rem);
  --type-section: clamp(2.25rem, 3.5vw, 3rem);
  --type-card: clamp(1.25rem, 2vw, 1.65rem);
  --radius-card: 12px;
  --radius-panel: 18px;
  --surface-paper: #fff;
  --surface-muted: #f2f4ef;
  --surface-proof: #050505;
}

.service-page--pilot {
  background: var(--surface-paper);
}

@media (max-width: 640px) {
  :root {
    --type-page-title: clamp(2.5rem, 12vw, 3rem);
    --type-section: clamp(1.875rem, 9vw, 2.25rem);
  }
}

@media (prefers-reduced-motion: reduce) {
  .service-page--pilot *,
  .service-page--pilot *::before,
  .service-page--pilot *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
  }
}
```

- [ ] **Step 5: Run syntax checks**

Run:

```bash
PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py tests/service_page_pilot_check.py
```

Expected: exit code 0.

- [ ] **Step 6: Commit the foundation**

```bash
git add build_site.py visual-system.css tests/service_page_pilot_check.py
git commit -m "test: define service page pilot contract"
```

## Task 2: Mark the Agent service as the pilot and assign real asset roles

**Files:**
- Modify: `build_site.py:1022-1060, 1134-1168`
- Modify: `visual-system.css`
- Generate: `service-agent-build.html`

**Interfaces:**
- Consumes: existing `service_page()` content lists and `ff_icon()`.
- Produces: optional `pilot`, `hero_asset`, and `technical_asset` parameters; data attributes used by the pilot contract.

- [ ] **Step 1: Extend the shared generator without changing default output**

Add these keyword-only parameters to `service_page()`:

```python
pilot=False,
hero_asset=None,
technical_asset=None,
```

Before `body=f'''`, compute the pilot-only fragments:

```python
pilot_class = " service-page--pilot" if pilot else ""
hero_visual = (
    f'<figure class="service-pilot-photo" data-asset-role="business-photo">'
    f'<img src="{hero_asset}" alt="业务团队在桌面上核对 Agent 工作流、审批点和异常处理" decoding="async">'
    f'<figcaption>先把任务、系统和人工责任画清楚，再进入验证。</figcaption></figure>'
    if pilot and hero_asset else
    f'<div class="service-hero-art" data-code="{number}" data-reveal><span class="service-hero-icon">{ff_icon(icon)}</span><div class="service-orbit"></div><div class="service-hero-card"><small>FORFLOW / {number}</small><strong>{method}</strong><span>{method_note}</span></div></div>'
)
technical_visual = (
    f'<figure class="service-pilot-diagram" data-asset-role="technical-diagram">'
    f'<a href="{technical_asset}" target="_blank" rel="noopener">'
    f'<img src="{technical_asset}" alt="企业 Agent 从定义、构建、评估、发布、生产观测到失败样本回流的生命周期"></a>'
    f'<figcaption><strong>一条生产路径：</strong>评估不是上线前的一次检查，而是持续接收生产失败样本。</figcaption></figure>'
    if pilot and technical_asset else ""
)
```

Replace the hero-art element in the existing body with `{hero_visual}`. Add `data-visual-role="proof"` to the `#outcomes` section, and insert `{technical_visual}` immediately before the outcome grid.

Change the final write call to:

```python
body_class = f"service-page {slug}{pilot_class}"
(ROOT / f"{slug}.html").write_text(
    page(title, subtitle, slug, body, body_class),
    encoding="utf-8",
)
```

- [ ] **Step 2: Enable the pilot for only the Agent service call**

At the end of the `service-agent-build` call add:

```python
pilot=True,
hero_asset="assets/service-agent/forflow-agent-workflow-hero-v1.png",
technical_asset="assets/service-agent/forflow-agent-workflow-system-v1.png",
```

Do not add these parameters to the other four service calls.

- [ ] **Step 3: Generate the site and verify the asset-role test now reaches copy checks**

Run:

```bash
PYTHONPATH=.python-deps PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 build_site.py
PYTHONPATH=.python-deps python3 tests/service_page_pilot_check.py
```

Expected: the build succeeds; the pilot test fails first on `Missing approved pilot copy`.

- [ ] **Step 4: Add the pilot-only asset and hierarchy styles**

Append the following to `visual-system.css`:

```css
.service-page--pilot .service-hero-grid {
  min-height: 590px;
  grid-template-columns: minmax(0, 1fr) minmax(420px, .95fr);
}

.service-page--pilot .service-hero-copy h1 {
  font-size: var(--type-page-title);
  line-height: 1;
}

.service-page--pilot .section-title,
.service-page--pilot .section-title--small {
  max-width: 18ch;
  font-size: var(--type-section);
  line-height: 1.08;
}

.service-pilot-photo,
.service-pilot-diagram {
  margin: 0;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: var(--radius-panel);
  background: var(--surface-muted);
}

.service-pilot-photo img {
  display: block;
  width: 100%;
  min-height: 440px;
  object-fit: cover;
}

.service-pilot-photo figcaption,
.service-pilot-diagram figcaption {
  padding: 14px 16px;
  color: var(--muted);
  font-size: .78rem;
  line-height: 1.55;
}

.service-page--pilot .service-transformation {
  background: var(--surface-proof);
}

.service-page--pilot .related-services {
  background: var(--surface-paper);
  color: var(--ink);
}

.service-page--pilot .problem-grid,
.service-page--pilot .scope-grid,
.service-page--pilot .deliverable-grid {
  gap: 0;
  border-top: 1px solid var(--line);
}

.service-page--pilot .problem-grid article,
.service-page--pilot .scope-grid article,
.service-page--pilot .deliverable-grid article {
  min-height: 0;
  padding: 24px 18px;
  border: 0;
  border-bottom: 1px solid var(--line);
  border-radius: 0;
  box-shadow: none;
}

.service-page--pilot .problem-grid h3,
.service-page--pilot .scope-grid h3,
.service-page--pilot .deliverable-grid h3 {
  margin: 24px 0 8px;
  font-size: var(--type-card);
}

.service-page--pilot .service-pilot-diagram {
  margin-top: 38px;
  background: #08120b;
}

.service-page--pilot .service-pilot-diagram img {
  display: block;
  width: 100%;
}

.service-page--pilot .service-pilot-diagram figcaption {
  color: #c3cbc4;
}

.service-page--pilot .service-pilot-diagram figcaption strong {
  color: var(--flow);
}

@media (max-width: 900px) {
  .service-page--pilot .service-hero-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .service-pilot-photo img {
    min-height: 280px;
  }
  .service-page--pilot .problem-grid,
  .service-page--pilot .scope-grid,
  .service-page--pilot .deliverable-grid {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 5: Commit asset roles and pilot presentation**

```bash
git add build_site.py visual-system.css service-agent-build.html
git commit -m "feat: add service page visual pilot"
```

## Task 3: Tighten the Agent service copy and highlighter budget

**Files:**
- Modify: `build_site.py:1134-1168`
- Modify: `visual-system.css`
- Modify: `tests/service_page_pilot_check.py`
- Generate: `service-agent-build.html`

**Interfaces:**
- Consumes: the pilot generator and asset-role markup from Task 2.
- Produces: approved enterprise-facing copy and a page with one proof section and no decorative highlighter competition.

- [ ] **Step 1: Replace the pilot's key copy with the approved direct wording**

Use these exact values in the `service-agent-build` call:

```python
subtitle='先选一条真实流程，验证 Agent 能不能稳定完成任务。我们会把知识、系统操作和人工审批接起来，用真实样本检查结果。',
intro='Agent 能回答问题，不代表它能进入真实流程。',
insight_lead='真正影响上线的是任务边界、系统权限、异常处理和人工责任。',
outcome_title='两周后，企业要拿到继续、调整或停止的依据。',
outcome_lead='验证结果会说明这条流程能否稳定运行，还缺哪些接口、数据和运营条件。',
scope_title='只接通完成这条流程需要的能力。',
scope_lead='不默认上多 Agent 或大平台。先把知识、工具、审批和回退接稳。',
process_title='用五步完成一次受控验证。',
process_lead='正常样本要跑，资料缺失、权限不足和系统失败也要专门测试。',
deliverable_title='工作版本和评估证据一起交付。',
deliverable_lead='企业可以看到 Agent 做了什么、哪里失败，以及为什么值得继续或应该停。',
faq_lead='这里说明验证周期、生产边界和失败处理。',
cta_title=mobile_title('开始前，', '请准备这四项信息。'),
cta_lead='一条高频流程、当前步骤、需要连接的系统，以及不可接受的结果。',
```

Do not run automatic rewriting over pains, outcomes, FAQs, or evidence boundaries. Review those fields manually against the same four questions in the approved spec.

- [ ] **Step 2: Reduce visible kickers and solid green actions through scoped CSS**

Append:

```css
.service-page--pilot main .eyebrow {
  display: none;
}

.service-page--pilot .service-hero .eyebrow,
.service-page--pilot [data-visual-role="proof"] .eyebrow {
  display: flex;
}

.service-page--pilot .ff-header .header-cta,
.service-page--pilot .service-consult-actions .btn--green {
  border-color: var(--ink);
  background: transparent;
  color: inherit;
}

.service-page--pilot .service-consult-actions .btn--green {
  border-color: rgba(255, 255, 255, .45);
  color: #fff;
}
```

Keep the Hero booking action as the only solid green service-content CTA.

- [ ] **Step 3: Extend the static contract for highlighter budget**

Add to `tests/service_page_pilot_check.py`:

```python
if len(soup.select("main .eyebrow")) > 9:
    fail("Pilot source should not add more kickers than the shared generator already owns")

pilot_css = CSS.read_text(encoding="utf-8")
for rule in (
    '.service-page--pilot main .eyebrow',
    '.service-page--pilot .service-hero .eyebrow',
    '.service-page--pilot [data-visual-role="proof"] .eyebrow',
):
    if rule not in pilot_css:
        fail(f"Missing kicker-budget rule: {rule}")
```

- [ ] **Step 4: Rebuild and run the focused tests**

Run:

```bash
PYTHONPATH=.python-deps PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 build_site.py
PYTHONPATH=.python-deps python3 tests/service_page_pilot_check.py
PYTHONPATH=.python-deps python3 tests/static_check.py
```

Expected: all three commands exit 0; pilot check prints its `OK` line; static check reports all local references resolved.

- [ ] **Step 5: Commit the copy and highlight budget**

```bash
git add build_site.py visual-system.css tests/service_page_pilot_check.py service-agent-build.html search-index.json
git commit -m "refine: tighten Agent service page copy"
```

## Task 4: Verify the pilot without disturbing the gate or production build

**Files:**
- Modify: `docs/maintenance/update-log.md`
- Verify: `service-agent-build.html`, `visual-system.css`, `dist/`

**Interfaces:**
- Consumes: all pilot output from Tasks 1–3.
- Produces: a reviewed local service-page URL and a regression record; no production deployment.

- [ ] **Step 1: Run syntax and public-build checks**

Run:

```bash
node --check script.js
PYTHONPYCACHEPREFIX=/tmp/forflow-pycache python3 -m py_compile build_site.py tests/static_check.py tests/service_page_pilot_check.py tests/public_build_check.py
PYTHONPATH=.python-deps python3 tests/public_build_check.py
node tests/invite_gate_check.js
node tests/gate_runtime_check.mjs
git diff --check
```

Expected: every command exits 0. The public build contains `service-agent-build.html` and `visual-system.css`, but not `build_site.py`, `tests/`, `docs/`, or `.superpowers/`.

- [ ] **Step 2: Start the local preview**

Run:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:8765/service-agent-build.html?qa=service-visual-pilot-v28
```

- [ ] **Step 3: Perform desktop and mobile visual QA**

At 1280×800 and 390×844, capture and compare these states:

1. Hero: one H1, business photo, one solid green service CTA.
2. Fit and problem sections: smaller H2, quiet white surface, no repeated card glow.
3. Proof section: the only black high-weight region and the technical diagram.
4. Evidence and consultation: evidence labels remain explicit; consultation CTA remains usable without competing with the Hero.
5. Mobile: no horizontal overflow; photo and diagram crop cleanly; local navigation remains scrollable.
6. Reduced motion: all text is immediately readable and no orbit animation remains on the pilot.

Expected: the page keeps ForFlow's black/green sharpness but no two adjacent sections have the same visual weight.

- [ ] **Step 4: Record the pilot**

Add a dated entry to `docs/maintenance/update-log.md` containing:

```markdown
## 2026-07-12 · 企业 Agent 服务页视觉系统试点 v28

- `service-agent-build.html` 作为唯一服务页试点；其余四项服务保持原样，等待视觉确认后再同步。
- 新增 `visual-system.css`，把标题、圆角、表面和减少动效规则与历史样式分层。
- 业务摄影说明工作现场，技术图说明评估与生产反馈路径；本页不伪造产品界面，也不加入自动播放品牌动效。
- 文案按业务问题、启动条件、验证结果和下一步重写；`humanizer-zh` 只用于问题扫描。
- 验证：`service_page_pilot_check.py`、`static_check.py`、`public_build_check.py`、门禁静态与运行检查、Python / JavaScript 语法检查和 `git diff --check` 通过。
```

- [ ] **Step 5: Commit the verified pilot**

```bash
git add docs/maintenance/update-log.md
git commit -m "docs: record service page visual pilot"
```

## Review Gate

Stop after Task 4 and show the user the desktop and mobile pilot. Do not apply the variant to `ai-readiness-audit.html`, `service-ai-enablement.html`, `service-data-governance.html`, or `service-ai-training.html` until the user approves the pilot.
