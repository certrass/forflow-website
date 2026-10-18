#!/usr/bin/env python3
"""Mount an already verified homepage build without changing the main website.

This is packaging, not a second source for the product UI. Build homepage-v6 first,
then supply that build and its verification receipt. Original files are untouched.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


MOUNT = '/product/one'
ROOT_URL = re.compile(r'''(["'`])(/(?:assets/|workbench/|ai-governance(?:-brief)?(?:\.html)?(?=["'`/#?]))[^"'`]*)(\1)''')


def relocate(content, relative):
    content = ROOT_URL.sub(lambda m: m[1] + MOUNT + m[2] + m[3], content)
    # CSS supports both quoted and unquoted URLs.
    content = re.sub(r'url\(/assets/', 'url(' + MOUNT + '/assets/', content)
    content = content.replace('"/#capabilities"', '"' + MOUNT + '/#capabilities"')
    content = re.sub(r'''(href\s*[:=]\s*)(["'])/\2''', lambda m: m[1] + m[2] + MOUNT + '/' + m[2], content)
    if relative.suffix == '.html':
        base = MOUNT + '/' + (relative.parent.as_posix() + '/' if relative.parent.as_posix() != '.' else '')
        content = re.sub(r'(<head\b[^>]*>)', lambda m: m[1] + '<base href="' + base + '">', content, count=1)
        if relative.name == 'index.html' and relative.parent.as_posix() == '.':
            content = content.replace('</head>', '<link rel="canonical" href="https://forflow.ai/product/one">\n</head>', 1)
    return content


def package(source, receipt, destination, write_receipt=True):
    original = json.loads(receipt.read_text())
    records = []
    for entry in original['verified_files']:
        relative = Path(entry['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe source path: ' + str(relative))
        raw = (source / relative).read_bytes()
        expected = raw
        if entry.get('transformation'):
            expected = expected.replace(b'href="/ai-governance.html"', b"href='/ai-governance'")
        if hashlib.sha256(expected).hexdigest() != entry['sha256']:
            raise ValueError('Build differs from verified preview: ' + str(relative))
        rendered = relocate(raw.decode('utf-8'), relative).encode('utf-8') if relative.suffix in {'.html', '.js', '.css'} else raw
        target = destination / MOUNT.lstrip('/') / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(rendered)
        records.append({'path': MOUNT + '/' + relative.as_posix(), 'sha1': hashlib.sha1(rendered).hexdigest(), 'sha256': hashlib.sha256(rendered).hexdigest(), 'bytes': len(rendered), 'relocated': raw != rendered})
    result = {'source_deploy': original['deploy_id'], 'mount': MOUNT, 'files': records}
    if write_receipt:
        (destination / 'product-one-package.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    result = package(args.source, args.receipt, args.destination)
    print(json.dumps({'source_deploy': result['source_deploy'], 'mount': MOUNT, 'files': len(result['files'])}))
