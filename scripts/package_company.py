"""Mount the template-generated homepage at the public /company route.

Keep its assets inside /company/assets so publishing this page does not replace
shared files used by the gated site or the independently released One product.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
from shutil import copyfile
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.python-deps'))
from bs4 import BeautifulSoup


def package(root: Path, destination: Path, write_receipt: bool = True):
    source = root / 'index.html'
    soup = BeautifulSoup(source.read_text(), 'html.parser')
    for wall in soup.select('.reference-logo-wall'):
        wall.decompose()
    for node in soup.select('a[href], form[action]'):
        attr = 'href' if node.name == 'a' else 'action'
        value = node.get(attr, '')
        if value == '/':
            node[attr] = '/company'
        elif value.startswith('/#'):
            node[attr] = '/company' + value[1:]
        elif value.startswith('index.html'):
            node[attr] = '/company' + value[len('index.html'):]
        elif value and not value.startswith(('http:', 'https:', '#', 'mailto:', 'tel:', '/')) and '.html' in value:
            node[attr] = 'https://forflow.ai/' + value

    canonical = soup.new_tag('link', rel='canonical', href='https://forflow.ai/company')
    soup.head.append(canonical)
    og_url = soup.new_tag('meta', property='og:url', content='https://forflow.ai/company')
    soup.head.append(og_url)
    html = str(soup).replace('<!-- CUSTOMER_LOGO_WALL_PREVIEW_ONLY -->', '')
    references = set(re.findall(r'[\"\'](assets/[A-Za-z0-9_./+-]+)', html))
    assert not any('/reference-logos/' in path for path in references), 'Reference customer marks must not be published'
    files = []
    for relative in sorted(references):
        asset = (root / relative).resolve()
        asset.relative_to((root / 'assets').resolve())
        assert asset.is_file(), 'Missing company asset: ' + relative
        target = destination / 'company' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        copyfile(asset, target)
        files.append(target)
    html = re.sub(r'([\"\'])assets/', r'\1/company/assets/', html)
    page = destination / 'company/index.html'
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(html)
    files.append(page)
    result = {
        'mount': '/company',
        'source': str(source),
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'customer_reference_logos': False,
        'files': [{
            'path': '/' + p.relative_to(destination).as_posix(),
            'sha1': hashlib.sha1(p.read_bytes()).hexdigest(),
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
            'bytes': p.stat().st_size,
        } for p in sorted(files)],
    }
    if write_receipt:
        (destination / 'company-package.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    receipt = package(ROOT, args.destination)
    print(json.dumps({'mount': receipt['mount'], 'files': len(receipt['files']), 'destination': str(args.destination)}))
