#!/usr/bin/env python3
"""Package only the homepage + public One product for a remote review.

Source service/case pages remain linked to forflow.ai. Guru customer logos are
explicit review-only assets, injected only with --reference-logos. This script
does not deploy or alter the pinned production product receipt.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / '.python-deps')]
from bs4 import BeautifulSoup
from scripts.package_product_one import package


def build_review(source, destination, reference_logos=False):
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError('Use an empty destination so old bundles are not published')
    receipt = {'deploy_id': None, 'verification': 'Local review build', 'verified_files': [
        {'path': p.relative_to(source).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in sorted(source.rglob('*')) if p.is_file()
    ]}
    receipt_path = destination.parent / (destination.name + '-product-source.json')
    receipt_path.write_text(json.dumps(receipt, indent=2))
    package(source, receipt_path, destination, write_receipt=False)
    html = (ROOT / 'index.html').read_text()
    if reference_logos:
        brands = json.loads((ROOT / 'docs/maintenance/homepage-brand-assets.json').read_text())
        logos = '<section class="reference-logo-wall" data-reference-only aria-label="客户与合作方 logo 排版参考"><p>客户与合作方</p><div>'
        logos += ''.join(f'<img src="{e["src"]}" alt="{e["alt"]}" width="{e["width"]}" height="{e["height"]}" title="Guru 参考标识 · 待替换">' for e in brands['reference_logos'])
        html = html.replace('<!-- CUSTOMER_LOGO_WALL_PREVIEW_ONLY -->', logos + '</div></section>')
    soup = BeautifulSoup(html, 'html.parser')
    for node in soup.select('a[href], form[action]'):
        attr = 'href' if node.name == 'a' else 'action'
        value = node.get(attr, '')
        if value.startswith('index.html'):
            node[attr] = '/' + value[len('index.html'):]
        elif value and not value.startswith(('http:', 'https:', '#', 'mailto:', 'tel:', '/product/one')) and '.html' in value:
            node[attr] = 'https://forflow.ai/' + value.lstrip('/')
    for tag, attr in [('img', 'src'), ('script', 'src'), ('link', 'href'), ('use', 'href')]:
        for node in soup.find_all(tag):
            path = urlparse(node.get(attr, '')).path
            if path.startswith('assets/'):
                target = destination / path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, target)
    (destination / 'index.html').write_text(str(soup))
    (destination / '_headers').write_text('/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n')
    (destination / '_redirects').write_text('/product/one/ai-governance /product/one/ai-governance.html 200\n/search.html https://forflow.ai/search.html 302\n/navigator.html https://forflow.ai/navigator.html 302\n')
    return {'files': sum(p.is_file() for p in destination.rglob('*')), 'directory': str(destination), 'reference_logos': reference_logos}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--product-build', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--reference-logos', action='store_true')
    args = parser.parse_args()
    print(json.dumps(build_review(args.product_build, args.destination, args.reference_logos)))
