from pathlib import Path
from subprocess import run
import os
import re


ROOT = Path(__file__).resolve().parents[1]
run(['python3', 'scripts/build_public.py'], cwd=ROOT, check=True)

config_text = (ROOT / 'netlify.toml').read_text(encoding='utf-8')
build_match = re.search(r'(?ms)^\[build\]\s*(.*?)(?=^\[|\Z)', config_text)
assert build_match, 'missing [build] config'
build_config = build_match.group(1)
assert re.search(r'^\s*publish\s*=\s*"dist"\s*$', build_config, re.M)
assert re.search(r'^\s*command\s*=\s*"python3 scripts/build_public\.py"\s*$', build_config, re.M)

dist = ROOT / 'dist'
for required in ('index.html', 'landing.html', 'styles.css', 'script.js', 'gate-client.js', 'search-index.json', 'robots.txt'):
    assert (dist / required).exists(), required
for forbidden in ('build_site.py', 'README.md', 'design-qa.md', 'docs', 'templates', 'tests', 'netlify', 'forflow-personal-mbti-site', 'vercel-demo'):
    assert not (dist / forbidden).exists(), forbidden
assert not (dist / 'assets' / 'explore-digital-solutions.pdf').exists()
assert not list((dist / 'assets').rglob('*.md'))
assert not (dist / 'assets' / 'generated-review').exists()
assert not any('q2q' in path.name.lower() for path in dist.rglob('*'))
assert not any('static.cloudflareinsights.com/beacon.min.js' in path.read_text(encoding='utf-8') for path in dist.glob('*.html')), 'Cloudflare beacon must stay off without a token'
assert 'data-lead-form' not in (dist / 'contact.html').read_text(encoding='utf-8'), 'contact form must stay off until the data API is enabled'
assert 'data-lead-form' not in (dist / 'navigator-results.html').read_text(encoding='utf-8'), 'report form must stay off until the data API is enabled'
assert 'mailto:hello@forflow.ai' in (dist / 'contact.html').read_text(encoding='utf-8'), 'contact email fallback must remain available'

asset_pattern = re.compile(r'assets/[A-Za-z0-9_./+-]+')
for public_file in dist.rglob('*'):
    if not public_file.is_file() or public_file.suffix.lower() not in {'.html', '.css', '.js', '.json'}:
        continue
    public_text = public_file.read_text(encoding='utf-8')
    assert 'q2q' not in public_text.lower(), f'{public_file.name}: internal Q2Q terminology leaked into public bundle'
    assert 'generated-review' not in public_text, f'{public_file.name}: internal review path leaked into public bundle'
    for reference in asset_pattern.findall(public_text):
        clean_reference = reference.split('?', 1)[0].split('#', 1)[0]
        assert (dist / clean_reference).is_file(), f'{public_file.name}: missing bundled asset {clean_reference}'

analytics_env = {**os.environ, 'CLOUDFLARE_WEB_ANALYTICS_TOKEN': 'a' * 32}
run(['python3', 'scripts/build_public.py'], cwd=ROOT, check=True, env=analytics_env)
for public_file in dist.glob('*.html'):
    public_text = public_file.read_text(encoding='utf-8')
    assert public_text.count('https://static.cloudflareinsights.com/beacon.min.js') == 1, f'{public_file.name}: Cloudflare beacon missing or duplicated'
    assert '"token":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"' in public_text, f'{public_file.name}: Cloudflare token missing'

data_env = {**os.environ, 'WEBSITE_DATA_ENABLED': 'true'}
run(['python3', 'scripts/build_public.py'], cwd=ROOT, check=True, env=data_env)
assert 'data-lead-form' in (dist / 'contact.html').read_text(encoding='utf-8'), 'contact form missing when data API is enabled'
assert 'data-lead-form' in (dist / 'navigator-results.html').read_text(encoding='utf-8'), 'report form missing when data API is enabled'

run(['python3', 'scripts/build_public.py'], cwd=ROOT, check=True)

print('OK: Netlify publish bundle contains public site files only.')
