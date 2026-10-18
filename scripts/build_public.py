from pathlib import Path
from shutil import copy2, rmtree
import json
import os
import re
from package_product_one import package
from package_company import package as package_company


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
ASSETS_ROOT = (ROOT / 'assets').resolve()

PUBLIC_ROOT_FILES = {
    'commercial.js',
    'gate-client.js',
    'robots.txt',
    'script.js',
    'search-index.json',
    'styles.css',
}
ASSET_PATTERN = re.compile(r'assets/[A-Za-z0-9_./+-]+')
PUBLIC_ASSET_ALIASES = {
    'assets/generated-review/c02-navigator-china-q2q-diagnostic-workbench.png': 'assets/site/navigator-workbench.png',
    'assets/generated-review/c04-playbook-china-q2q-leader-reading-v2.png': 'assets/site/playbook-leader-reading.png',
    'assets/generated-review/c12-case-logistics-data-china-q2q-dispatch-evidence.png': 'assets/site/logistics-dispatch-evidence.png',
    'assets/generated-review/p03-case-retail-manufacturing-workflow.png': 'assets/site/retail-manufacturing-workflow.png',
}
CF_ANALYTICS_TOKEN = os.environ.get('CLOUDFLARE_WEB_ANALYTICS_TOKEN', '').strip()
DATA_API_ENABLED = os.environ.get('WEBSITE_DATA_ENABLED', '').strip().lower() in {'1', 'true', 'yes'}
if CF_ANALYTICS_TOKEN and not re.fullmatch(r'[A-Za-z0-9_-]{20,80}', CF_ANALYTICS_TOKEN):
    raise SystemExit('CLOUDFLARE_WEB_ANALYTICS_TOKEN has an unexpected format')


if DIST.exists():
    rmtree(DIST)
DIST.mkdir(parents=True)

for source in sorted(ROOT.glob('*.html')):
    copy2(source, DIST / source.name)
for name in sorted(PUBLIC_ROOT_FILES):
    source = ROOT / name
    if not source.exists():
        raise SystemExit(f'Missing public file: {name}')
    copy2(source, DIST / name)

asset_references = set()
for source in [*sorted(ROOT.glob('*.html')), *(ROOT / name for name in sorted(PUBLIC_ROOT_FILES))]:
    if source.suffix.lower() not in {'.html', '.css', '.js', '.json'}:
        continue
    for match in ASSET_PATTERN.findall(source.read_text(encoding='utf-8')):
        asset_references.add(match.split('?', 1)[0].split('#', 1)[0])

for relative in sorted(asset_references):
    source = (ROOT / relative).resolve()
    try:
        source.relative_to(ASSETS_ROOT)
    except ValueError as exc:
        raise SystemExit(f'Asset reference escapes public assets: {relative}') from exc
    if not source.is_file():
        raise SystemExit(f'Missing referenced asset: {relative}')
    public_relative = PUBLIC_ASSET_ALIASES.get(relative, relative)
    target = (DIST / public_relative).resolve()
    try:
        target.relative_to(DIST.resolve())
    except ValueError as exc:
        raise SystemExit(f'Asset target escapes publish directory: {relative}') from exc
    target.parent.mkdir(parents=True, exist_ok=True)
    copy2(source, target)

for public_file in DIST.iterdir():
    if not public_file.is_file() or public_file.suffix.lower() not in {'.html', '.css', '.js', '.json'}:
        continue
    content = public_file.read_text(encoding='utf-8')
    rewritten = content
    for private_name, public_name in PUBLIC_ASSET_ALIASES.items():
        rewritten = rewritten.replace(private_name, public_name)
    if rewritten != content:
        public_file.write_text(rewritten, encoding='utf-8')

if not DATA_API_ENABLED:
    gated_patterns = (
        r'<section\b[^>]*\bdata-requires-data-api\b[^>]*>.*?</section>',
        r'<form\b[^>]*\bdata-requires-data-api\b[^>]*>.*?</form>',
    )
    for public_file in sorted(DIST.glob('*.html')):
        content = public_file.read_text(encoding='utf-8')
        for pattern in gated_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        if 'data-requires-data-api' in content:
            raise SystemExit(f'Unremoved data feature marker: {public_file.name}')
        public_file.write_text(content, encoding='utf-8')

if CF_ANALYTICS_TOKEN:
    beacon_data = json.dumps({'token': CF_ANALYTICS_TOKEN}, separators=(',', ':'))
    beacon = (
        '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
        f"data-cf-beacon='{beacon_data}'></script>"
    )
    for public_file in sorted(DIST.glob('*.html')):
        content = public_file.read_text(encoding='utf-8')
        if 'static.cloudflareinsights.com/beacon.min.js' in content:
            continue
        if '</body>' not in content:
            raise SystemExit(f'Missing </body> for analytics injection: {public_file.name}')
        public_file.write_text(content.replace('</body>', f'{beacon}\n</body>'), encoding='utf-8')

for forbidden in ('build_site.py', 'README.md', 'design-qa.md', 'netlify.toml', 'requirements.txt'):
    if (DIST / forbidden).exists():
        raise SystemExit(f'Private source leaked into publish directory: {forbidden}')
for forbidden in ('docs', 'templates', 'tests', 'tools', 'netlify', 'forflow-personal-mbti-site', 'vercel-demo'):
    if (DIST / forbidden).exists():
        raise SystemExit(f'Private directory leaked into publish directory: {forbidden}')
if list((DIST / 'assets').rglob('*.md')):
    raise SystemExit('Non-runtime markdown leaked into public assets')
if (DIST / 'assets' / 'explore-digital-solutions.pdf').exists():
    raise SystemExit('Internal design-reference PDF leaked into public assets')

# Preserve the independently reviewed product page on subsequent full-site builds.
# A missing or changed build fails closed; refresh its preview receipt first.
package(
    ROOT / 'output/homepage-v6/dist/client',
    ROOT / 'docs/maintenance/product-one-source.json',
    DIST,
    write_receipt=False,
)

package_company(ROOT, DIST, write_receipt=False)

print(f'public bundle ready: {DIST}')
