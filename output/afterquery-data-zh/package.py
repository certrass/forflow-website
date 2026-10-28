"""Package the reviewed root landing page at /company/data/ for production.

The separate experimental company/data/index.html is deliberately not included.
Run build.py first, then: python package.py /path/to/publish-root
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from shutil import copy2

ROOT = Path(__file__).resolve().parent
PUBLIC_PATH = Path('company/data')


def package(destination, write_receipt=True):
    destination = Path(destination).resolve()
    target = destination / PUBLIC_PATH
    target.mkdir(parents=True, exist_ok=True)
    assets = [
        ROOT / name for name in (
            'index.html', 'styles.css', 'script.js',
            'assets/source-styles.css', 'assets/forflow-mark.png',
            'assets/forflow-lockup-transparent.png',
            'assets/generated/work-records-office-v1.jpg',
            'assets/inter-regular.woff2', 'assets/inter-medium.woff2',
            'assets/inter-semibold.woff2',
        )
    ]
    entries = []
    for source in assets:
        relative = source.relative_to(ROOT)
        output = target / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        if relative.as_posix() == 'index.html':
            content = source.read_text()
            assert '<meta content="noindex, nofollow" name="robots"/>' in content
            content = content.replace('content="noindex, nofollow"', 'content="index, follow"')
            content = content.replace('</head>', '<link rel="canonical" href="https://forflow.ai/company/data/"/></head>')
            assert 'afterquery' not in content.lower()
            output.write_text(content)
        else:
            copy2(source, output)
        data = output.read_bytes()
        entries.append({
            'path': '/' + (PUBLIC_PATH / relative).as_posix(),
            'bytes': len(data), 'sha1': hashlib.sha1(data).hexdigest(),
            'sha256': hashlib.sha256(data).hexdigest(),
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        })
    # Fail for any missing relative HTML/CSS resource, including nested font URLs.
    for source in target.rglob('*'):
        if source.suffix not in ('.html', '.css'):
            continue
        for reference in re.findall(r'(?:src|href)=["\']([^"\']+)["\']|url\(["\']?([^\)"\']+)', source.read_text()):
            url = next(value for value in reference if value).split('?', 1)[0].split('#', 1)[0]
            if not url or url.startswith(('https:', 'http:', 'data:', '/')):
                continue
            resolved = (source.parent / url).resolve()
            assert resolved.is_relative_to(target) and resolved.is_file(), (source, url)
    manifest = {
        'public_url': 'https://forflow.ai/company/data/',
        'source': 'output/afterquery-data-zh/index.html',
        'production_only_changes': ['index, follow robots meta', 'canonical URL'],
        'files': entries,
    }
    if write_receipt:
        (destination / 'data-package.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'files': len(entries), 'bytes': sum(x['bytes'] for x in entries), 'destination': str(target)}))
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('--no-receipt', action='store_true', help='Exclude release metadata from a full-site public bundle')
    args = parser.parse_args()
    package(args.destination, write_receipt=not args.no_receipt)
