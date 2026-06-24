from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json, re, sys

ROOT=Path(__file__).resolve().parents[1]
html_files=sorted(ROOT.glob('*.html'))
errors=[]
report={}
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
required=['index.html','navigator.html','navigator-results.html','playbook.html','service-ai-enablement.html','service-data-governance.html','service-agent-build.html','service-ai-training.html','category-hrms.html','cases.html','case-wren-kitchens.html','search.html','document-viewer.html']
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

print(json.dumps(report,ensure_ascii=False,indent=2))
if errors:
    print('\nERRORS:',file=sys.stderr)
    print('\n'.join(errors),file=sys.stderr)
    sys.exit(1)
print(f'OK: {len(html_files)} HTML pages, all local references resolved.')
