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
visible_copy_compact = "".join(visible_copy.split())
required_copy = [
    "先选一条真实流程，验证 Agent 能不能稳定完成任务。",
    "两周后，企业要拿到继续、调整或停止的依据。",
    "开始前，请准备这四项信息",
]
for phrase in required_copy:
    if "".join(phrase.split()) not in visible_copy_compact:
        fail(f"Missing approved pilot copy: {phrase}")

if len(soup.select("main .eyebrow")) > 10:
    fail("Pilot source should not add more kickers than the shared generator already owns")

if not CSS.exists():
    fail("visual-system.css is missing")
css = CSS.read_text(encoding="utf-8")
for token in ("--type-page-title", "--type-section", "--radius-card", "--surface-proof"):
    if token not in css:
        fail(f"Missing visual-system token: {token}")
for selector in (
    ".service-page--pilot",
    "@media (max-width: 640px)",
    "@media (prefers-reduced-motion: reduce)",
):
    if selector not in css:
        fail(f"Missing pilot CSS contract: {selector}")

for rule in (
    ".service-page--pilot main .eyebrow",
    ".service-page--pilot .service-hero .eyebrow",
    '.service-page--pilot [data-visual-role="proof"] .eyebrow',
):
    if rule not in css:
        fail(f"Missing kicker-budget rule: {rule}")

print("OK: service page pilot structure, assets, copy, and visual tokens")
