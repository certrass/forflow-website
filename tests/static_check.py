from pathlib import Path
from urllib.parse import urlparse
import ast, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.python-deps'))
from bs4 import BeautifulSoup

html_files=sorted(ROOT.glob('*.html'))
errors=[]
report={}

def load_case_items():
    tree = ast.parse((ROOT / 'build_site.py').read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(target, 'id', '') == 'CASE_LIBRARY_ITEMS' for target in node.targets):
            return ast.literal_eval(node.value)
    return []

def case_target(item):
    if item.get('href'):
        return item['href']
    if item.get('id'):
        return f'cases.html#{item["id"]}'
    return 'cases.html'

case_items = load_case_items()
for path in html_files:
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    ids=[tag.get('id') for tag in soup.find_all(attrs={'id':True}) if tag.get('id')]
    dups=sorted({x for x in ids if ids.count(x)>1})
    if dups: errors.append(f'{path.name}: duplicate ids {dups}')
    if not soup.find('meta',attrs={'name':'viewport'}): errors.append(f'{path.name}: missing viewport')
    if not soup.find('link',attrs={'rel':lambda x:x and 'stylesheet' in x}): errors.append(f'{path.name}: missing stylesheet')
    if not soup.find(attrs={'data-search-modal':True}): errors.append(f'{path.name}: missing search modal')
    broken=[]
    for tag,attr in [('a','href'),('img','src'),('script','src'),('link','href'),('source','src'),('video','poster'),('iframe','src')]:
        for node in soup.find_all(tag):
            val=node.get(attr)
            if not val or val.startswith(('#','mailto:','tel:','javascript:','http://','https://','data:')): continue
            target=val.split('#')[0].split('?')[0]
            if not target: continue
            fp=(path.parent/target).resolve()
            try: fp.relative_to(ROOT.resolve())
            except ValueError: continue
            if not fp.exists(): broken.append(val)
    if broken: errors.append(f'{path.name}: broken local refs {sorted(set(broken))}')
    report[path.name]={
        'title': soup.title.get_text(strip=True) if soup.title else '',
        'ids':len(ids),
        'links':len(soup.find_all('a')),
        'words_zh':len(re.findall(r'[\u4e00-\u9fff]',soup.get_text(' ',strip=True))),
        'faq_items':len(soup.select('.faq-item')),
        'process_steps':len(soup.select('.service-process .process-list li')),
    }

# acceptance checks
required=['index.html','navigator.html','navigator-results.html','playbook.html','service-ai-enablement.html','service-data-governance.html','service-agent-build.html','service-ai-training.html','category-hrms.html','cases.html','case-wren-kitchens.html','case-manufacturing-pid-intelligence.html','case-healthcare-agent-roi.html','case-automotive-dfmea-ontology-agent.html','search.html','document-viewer.html']
for name in required:
    if not (ROOT/name).exists(): errors.append(f'missing required page: {name}')
for name in required[4:8]:
    s=BeautifulSoup((ROOT/name).read_text(encoding='utf-8'),'html.parser')
    if len(s.select('.faq-item'))<3: errors.append(f'{name}: needs FAQ')
    if len(s.select('.service-process .process-list li'))<3: errors.append(f'{name}: needs service process')
res=BeautifulSoup((ROOT/'navigator-results.html').read_text(encoding='utf-8'),'html.parser')
video=res.find('video')
if not video or not video.has_attr('controls'): errors.append('navigator-results.html: video controls missing')
if not video or 'forflow-brand-motion.mp4' not in str(video): errors.append('navigator-results.html: brand motion video missing')
pb=BeautifulSoup((ROOT/'playbook.html').read_text(encoding='utf-8'),'html.parser')
if not pb.select_one('.playbook-cover-art img[src="assets/forflow-lockup.png"]'): errors.append('playbook.html: exact supplied cover logo missing')

cases_soup=BeautifulSoup((ROOT/'cases.html').read_text(encoding='utf-8'),'html.parser')
search_soup=BeautifulSoup((ROOT/'search.html').read_text(encoding='utf-8'),'html.parser')
for item in case_items:
    if item.get('id') and not cases_soup.select_one(f'#{item["id"]}'):
        errors.append(f'cases.html: missing case item #{item["id"]}')
    if item.get('href') and not cases_soup.select_one(f'a[href="{item["href"]}"]'):
        errors.append(f'cases.html: missing linked case {item["href"]}')
    if item.get('search') and not search_soup.select_one(f'a[href="{case_target(item)}"]'):
        errors.append(f'search.html: missing search case {case_target(item)}')
case_count_label=search_soup.select_one('[data-result-type="case"] .search-result-head h2 span')
if case_count_label and int(case_count_label.get_text(strip=True) or '0') != sum(1 for item in case_items if item.get('search')):
    errors.append('search.html: case search count does not match CASE_LIBRARY_ITEMS')

maintenance_docs={
    'docs/maintenance/update-log.md': ['# ForFlow 网站更新记录', '## 2026-06-25', '## 2026-06-24', '### 验证'],
    'docs/maintenance/site-governance.md': ['# ForFlow 网站维护治理', '更新留痕', '发布门禁', 'CASE_LIBRARY_ITEMS'],
}
for rel, needles in maintenance_docs.items():
    path=ROOT/rel
    if not path.exists():
        errors.append(f'missing maintenance doc: {rel}')
        continue
    text=path.read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            errors.append(f'{rel}: missing required text {needle}')

log_path=ROOT/'docs/maintenance/update-log.md'
if log_path.exists():
    log_text=log_path.read_text(encoding='utf-8')
    dates=re.findall(r'^## (\d{4}-\d{2}-\d{2})\s*$', log_text, flags=re.M)
    if len(dates)<2:
        errors.append('docs/maintenance/update-log.md: needs at least two dated entries')
    if dates != sorted(dates, reverse=True):
        errors.append('docs/maintenance/update-log.md: dated entries should be newest first')
    entries=re.split(r'^## \d{4}-\d{2}-\d{2}\s*$', log_text, flags=re.M)[1:]
    for date, body in zip(dates, entries):
        for heading in ['### 变更范围', '### 主要变更', '### 验证', '### 后续']:
            if heading not in body:
                errors.append(f'docs/maintenance/update-log.md: {date} missing {heading}')

print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:
    print('\nERRORS:',file=sys.stderr)
    print('\n'.join(errors),file=sys.stderr)
    sys.exit(1)
print(f'OK: {len(html_files)} HTML pages, all local references resolved.')
