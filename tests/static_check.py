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

def load_assignment(name):
    tree = ast.parse((ROOT / 'build_site.py').read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(target, 'id', '') == name for target in node.targets):
            return ast.literal_eval(node.value)
    return None

def case_target(item):
    if item.get('href'):
        return item['href']
    if item.get('id'):
        return f'cases.html#{item["id"]}'
    return 'cases.html'

case_items = load_case_items()
asset_version = load_assignment('ASSET_VERSION')
for path in html_files:
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    visible_text=soup.get_text(' ',strip=True)
    for phrase in ['原型说明','内容映射占位','内容占位说明','DETAIL / CMS SLOT','正式上线时可接','响应式企业网站原型']:
        if phrase in visible_text:
            errors.append(f'{path.name}: customer-facing prototype placeholder remains: {phrase}')
    ids=[tag.get('id') for tag in soup.find_all(attrs={'id':True}) if tag.get('id')]
    dups=sorted({x for x in ids if ids.count(x)>1})
    if dups: errors.append(f'{path.name}: duplicate ids {dups}')
    symbol_ids={tag.get('id') for tag in soup.find_all('symbol') if tag.get('id')}
    icon_refs={
        ref[1:]
        for ref in (
            (use.get('href') or use.get('xlink:href') or '')
            for use in soup.find_all('use')
        )
        if ref.startswith('#')
    }
    missing_icons=sorted(icon_refs-symbol_ids)
    if missing_icons:
        errors.append(f'{path.name}: missing svg symbols {missing_icons}')
    if not soup.find('meta',attrs={'name':'viewport'}): errors.append(f'{path.name}: missing viewport')
    if not soup.find('link',attrs={'rel':lambda x:x and 'stylesheet' in x}): errors.append(f'{path.name}: missing stylesheet')
    if path.name != 'landing.html' and not soup.find(attrs={'data-search-modal':True}): errors.append(f'{path.name}: missing search modal')
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
    external_images=[img.get('src') for img in soup.find_all('img') if (img.get('src') or '').startswith(('http://','https://'))]
    if external_images:
        errors.append(f'{path.name}: externally hosted images leak visitor metadata {external_images}')
    for link in soup.select('a[target="_blank"]'):
        rel=set(link.get('rel') or [])
        if 'noopener' not in rel:
            errors.append(f'{path.name}: target=_blank link missing noopener: {link.get("href")}')
    inline_scripts=[script for script in soup.find_all('script') if not script.get('src') and script.get_text(strip=True)]
    if inline_scripts:
        errors.append(f'{path.name}: inline script would be blocked by production CSP')
    inline_handlers=[]
    for node in soup.find_all(True):
        inline_handlers.extend(attr for attr in node.attrs if attr.lower().startswith('on'))
    if inline_handlers:
        errors.append(f'{path.name}: inline event handlers would be blocked by production CSP: {sorted(set(inline_handlers))}')
    if 'Q2Q' in visible_text:
        errors.append(f'{path.name}: internal Q2Q terminology must not be customer-facing')
    if soup.select_one('main footer.site-footer'):
        errors.append(f'{path.name}: site footer is nested inside main content')
    if path.name != 'landing.html' and not soup.select_one('body > footer.site-footer'):
        errors.append(f'{path.name}: site footer must be a direct body child')
    report[path.name]={
        'title': soup.title.get_text(strip=True) if soup.title else '',
        'ids':len(ids),
        'links':len(soup.find_all('a')),
        'words_zh':len(re.findall(r'[\u4e00-\u9fff]',soup.get_text(' ',strip=True))),
        'faq_items':len(soup.select('.faq-item')),
        'process_steps':len(soup.select('.service-process .process-list li')),
    }

# acceptance checks
required=['landing.html','index.html','navigator.html','navigator-results.html','playbook.html','service-ai-enablement.html','service-data-governance.html','service-agent-build.html','service-ai-training.html','category-hrms.html','cases.html','case-wren-kitchens.html','case-manufacturing-pid-intelligence.html','case-healthcare-agent-roi.html','case-automotive-dfmea-ontology-agent.html','case-supply-chain-agentic-decision.html','case-financial-bda-document-automation.html','case-vanguard-virtual-analyst.html','case-agent-evaluation-first.html','case-energy-optimization-agent.html','search.html','document-viewer.html','privacy.html']
for name in required:
    if not (ROOT/name).exists(): errors.append(f'missing required page: {name}')
for name in ['service-ai-enablement.html','service-data-governance.html','service-agent-build.html','service-ai-training.html']:
    s=BeautifulSoup((ROOT/name).read_text(encoding='utf-8'),'html.parser')
    if len(s.select('.faq-item'))<3: errors.append(f'{name}: needs FAQ')
    if len(s.select('.service-process .process-list li'))<3: errors.append(f'{name}: needs service process')
res=BeautifulSoup((ROOT/'navigator-results.html').read_text(encoding='utf-8'),'html.parser')
video=res.find('video')
if not video or not video.has_attr('controls'): errors.append('navigator-results.html: video controls missing')
if not video or 'forflow-brand-motion.mp4' not in str(video): errors.append('navigator-results.html: brand motion video missing')
sort_buttons=res.select('[data-sort]')
if not sort_buttons or any(button.get('aria-pressed') not in {'true','false'} for button in sort_buttons):
    errors.append('navigator-results.html: sort controls need explicit aria-pressed state')
for mode in ('match', 'speed', 'foundation'):
    mode_buttons=[button for button in sort_buttons if button.get('data-sort') == mode]
    if len(mode_buttons) != 2:
        errors.append(f'navigator-results.html: expected desktop and mobile {mode} sort controls')
    expected='true' if mode == 'match' else 'false'
    if any(button.get('aria-pressed') != expected for button in mode_buttons):
        errors.append(f'navigator-results.html: incorrect initial aria-pressed state for {mode}')
if not res.select_one('[data-mobile-sort-toggle][aria-expanded="false"]'):
    errors.append('navigator-results.html: mobile sort toggle needs initial aria-expanded=false')
if not res.select_one('[data-mobile-sort-menu][aria-hidden="true"]'):
    errors.append('navigator-results.html: mobile sort menu needs initial aria-hidden=true')
report_form=res.select_one('form[data-lead-form][data-source-type="assessment_report"]')
if not report_form or not report_form.select_one('input[name="assessment_id"][data-assessment-id]'):
    errors.append('navigator-results.html: assessment report form must carry only the internal assessment id')
if not report_form or not report_form.select_one('input[name="email"][type="email"][required]'):
    errors.append('navigator-results.html: report request needs a required email')
if not report_form or not report_form.select_one('input[name="consent"][required]'):
    errors.append('navigator-results.html: report request needs explicit consent')
contact_soup=BeautifulSoup((ROOT/'contact.html').read_text(encoding='utf-8'),'html.parser')
contact_form=contact_soup.select_one('form[data-lead-form][data-source-type="contact"]')
if not contact_form or not contact_form.select_one('input[name="email"][type="email"][required]'):
    errors.append('contact.html: contact lead form needs a required email')
if not contact_soup.select_one('a[href^="mailto:hello@forflow.ai"]'):
    errors.append('contact.html: direct email fallback missing')
privacy_soup=BeautifulSoup((ROOT/'privacy.html').read_text(encoding='utf-8'),'html.parser')
for phrase in ['诊断表和答案表不保存姓名或邮箱', 'Netlify', 'Supabase', 'hello@forflow.ai']:
    if phrase not in privacy_soup.get_text(' ', strip=True):
        errors.append(f'privacy.html: missing privacy disclosure {phrase}')
pb=BeautifulSoup((ROOT/'playbook.html').read_text(encoding='utf-8'),'html.parser')
if not pb.select_one('.playbook-cover-art img[src="assets/forflow-lockup.png"]'): errors.append('playbook.html: exact supplied cover logo missing')
landing_soup=BeautifulSoup((ROOT/'landing.html').read_text(encoding='utf-8'),'html.parser')
if not landing_soup.select_one('.invite-gate-brand img[src="assets/forflow-lockup-transparent.png"]'):
    errors.append('landing.html: exact ForFlow lockup missing')
if not landing_soup.select_one('.invite-gate-visual img[src="assets/invite/forflow-private-preview.jpg"]'):
    errors.append('landing.html: generated invitation visual missing')
gate_code=landing_soup.select_one('[data-gate-code]')
if not gate_code or gate_code.get('type') != 'password' or not gate_code.has_attr('required'):
    errors.append('landing.html: access-code input accessibility contract missing')
if not landing_soup.select_one('script[src^="gate-client.js"]'):
    errors.append('landing.html: access-code client missing')
gate_form=landing_soup.select_one('form[data-gate-form]')
if not gate_form or gate_form.get('method', '').lower() != 'post' or gate_form.get('action') != '/api/gate-login':
    errors.append('landing.html: gate form must fail closed to POST /api/gate-login')
home_soup=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
hero_preview = home_soup.select_one('.one-product-preview[data-workspace-film]')
if not hero_preview or not all(hero_preview.select_one(selector) for selector in ['.one-source', '.one-result', 'a.one-preview-action[href="/product/one#platform"]', 'button[data-fw-play]', 'button[data-fw-source="contract"]', 'button[data-fw-create]']):
    errors.append('index.html: product entry must connect contract source, result and full walkthrough')
if home_soup.select_one('.home-hero-photo img[src="assets/hero-hand.jpg"]'):
    errors.append('index.html: poster-style legacy hero visual still in use')
if home_soup.select_one('.home-vertical-type'):
    errors.append('index.html: oversized vertical hero text should be removed')
# The full business sequence lives in the contract workbench. The former
# duplicate three-column flow is now the interactive product-mechanism section.
if [button.get('data-fw-chapter') for button in home_soup.select('.fw-film-controls [data-fw-chapter]')] != ['0', '1', '2']:
    errors.append('index.html: business flow must retain source, verification and handoff controls')
if not home_soup.select_one('.fw-film-controls button[data-fw-play]'):
    errors.append('index.html: business flow must expose a playback control')
# The duplicate numeric entry band was removed during the accepted copy trim.
# Validate the destinations are still reachable through their primary controls.
for selector, label in [
    ('.fw-film-controls a[href^="/product/one"]', 'full product'),
    ('#navigator button[data-diagnosis-toggle]', 'scenario diagnosis'),
    ('#services a[href="ai-readiness-audit.html"]', 'readiness service'),
    ('#services a[href="service-agent-build.html"]', 'workflow service'),
]:
    if not home_soup.select_one(selector):
        errors.append(f'index.html: missing primary entry for {label}')

cases_soup=BeautifulSoup((ROOT/'cases.html').read_text(encoding='utf-8'),'html.parser')
search_soup=BeautifulSoup((ROOT/'search.html').read_text(encoding='utf-8'),'html.parser')
viewer_soup=BeautifulSoup((ROOT/'document-viewer.html').read_text(encoding='utf-8'),'html.parser')
case_filter_buttons=cases_soup.select('[data-case-filter]')
if not case_filter_buttons or any(button.get('aria-pressed') not in {'true','false'} for button in case_filter_buttons):
    errors.append('cases.html: case filters need explicit aria-pressed state')
if sum(button.get('aria-pressed') == 'true' for button in case_filter_buttons) != 1:
    errors.append('cases.html: exactly one case filter should be pressed initially')
search_index_path=ROOT/'search-index.json'
if not search_index_path.exists():
    errors.append('missing search-index.json')
    search_index={'items':[]}
else:
    search_index=json.loads(search_index_path.read_text(encoding='utf-8'))
    if search_index.get('version') != asset_version:
        errors.append('search-index.json: version does not match ASSET_VERSION')
    if not isinstance(search_index.get('items'), list) or not search_index['items']:
        errors.append('search-index.json: missing searchable items')
if not search_soup.select_one('[data-search-index]'):
    errors.append('search.html: missing data-search-index')
if not search_soup.find('h1'):
    errors.append('search.html: missing page h1')
for selector in ['a[data-doc-open][href]', 'a[data-doc-download][href]']:
    if not viewer_soup.select_one(selector):
        errors.append(f'document-viewer.html: missing static fallback link {selector}')
index_hrefs={item.get('href') for item in search_index.get('items', [])}
index_type_counts={}
for entry in search_index.get('items', []):
    index_type_counts[entry.get('type')] = index_type_counts.get(entry.get('type'), 0) + 1
for item in case_items:
    if item.get('id') and not cases_soup.select_one(f'#{item["id"]}'):
        errors.append(f'cases.html: missing case item #{item["id"]}')
    if item.get('href') and not cases_soup.select_one(f'a[href="{item["href"]}"]'):
        errors.append(f'cases.html: missing linked case {item["href"]}')
    if item.get('search') and not search_soup.select_one(f'a[href="{case_target(item)}"]'):
        errors.append(f'search.html: missing search case {case_target(item)}')
    if item.get('search') and case_target(item) not in index_hrefs:
        errors.append(f'search-index.json: missing search case {case_target(item)}')
energy_item=next((item for item in case_items if item.get('id') == 'energy-optimization-agent'), None)
if not energy_item:
    errors.append('build_site.py: missing energy optimization case item')
else:
    if not cases_soup.select_one('a[href="case-energy-optimization-agent.html"]'):
        errors.append('cases.html: energy optimization case link missing')
    energy_entry=next((entry for entry in search_index.get('items', []) if entry.get('href') == 'case-energy-optimization-agent.html'), None)
    if not energy_entry:
        errors.append('search-index.json: energy optimization case missing')
    if not {'manufacturing', 'data'}.issubset(set(energy_item.get('tags', []))):
        errors.append('build_site.py: energy optimization case needs manufacturing and data tags')
    if not energy_item.get('visual'):
        errors.append('build_site.py: energy optimization case visual missing')

energy_soup=BeautifulSoup((ROOT/'case-energy-optimization-agent.html').read_text(encoding='utf-8'),'html.parser')
if 'case-theme--energy' not in (energy_soup.body.get('class', []) if energy_soup.body else []):
    errors.append('case-energy-optimization-agent.html: energy theme missing')
for section_id in ['architecture', 'prediction', 'decision', 'safety', 'evidence']:
    if not energy_soup.select_one(f'#{section_id}'):
        errors.append(f'case-energy-optimization-agent.html: missing #{section_id}')
if not energy_soup.select_one('a[href="contact.html?topic=energy-agent"]'):
    errors.append('case-energy-optimization-agent.html: consultation topic link missing')

script_text=(ROOT/'script.js').read_text(encoding='utf-8')
if 'navigator-results.html?assessment_id=' not in script_text:
    errors.append('script.js: navigator result URL must use only assessment_id')
if 'navigator-results.html?challenge=' in script_text:
    errors.append('script.js: navigator answers must not be copied into the result URL')
for endpoint in ['/api/events', '/api/assessments', '/api/leads']:
    if endpoint not in script_text:
        errors.append(f'script.js: missing first-party endpoint {endpoint}')
for topic in ["hr", "energy-agent"]:
    if re.search(rf"(?:^|\n)\s*['\"]?{re.escape(topic)}['\"]?\s*:\s*\{{", script_text) is None:
        errors.append(f'script.js: contact topic {topic} missing')
if "hrStage: value('hrStage')" not in script_text:
    errors.append('script.js: HR stage is not carried into navigator results')
case_count_label=search_soup.select_one('[data-result-type="case"] .search-result-head h2 span')
if case_count_label and int(case_count_label.get_text(strip=True) or '0') != sum(1 for item in case_items if item.get('search')):
    errors.append('search.html: case search count does not match CASE_LIBRARY_ITEMS')
for result_type in ['category','service','resource','case']:
    label=search_soup.select_one(f'[data-result-type="{result_type}"] .search-result-head h2 span')
    if label and int(label.get_text(strip=True) or '0') != index_type_counts.get(result_type, 0):
        errors.append(f'search.html: {result_type} count does not match search-index.json')

for case_path in sorted(ROOT.glob('case-*.html')):
    case_soup=BeautifulSoup(case_path.read_text(encoding='utf-8'),'html.parser')
    body=case_soup.body
    if not body or 'case-detail-page' not in body.get('class', []):
        errors.append(f'{case_path.name}: missing case-detail-page body class')
        continue
    shell=case_soup.select_one('.case-detail-shell')
    if not shell:
        errors.append(f'{case_path.name}: missing case-detail-shell')
    elif 'case-story-shell' not in shell.get('class', []):
        errors.append(f'{case_path.name}: case detail shell should include case-story-shell for shared mobile spacing')
    if not case_soup.select_one('.case-toc nav[data-scrollspy]'):
        errors.append(f'{case_path.name}: missing case toc scrollspy nav')

source_contracts={
    'case-manufacturing-pid-intelligence.html': 'aws.amazon.com/cn/blogs/industries/how-everllence-scaled-pid-intelligence-to-improve-plant-operations/',
    'case-healthcare-agent-roi.html': 'aws.amazon.com/blogs/industries/how-we-built-healthcare-ai-you-can-trust-the-engineering-behind-amazon-connect-health/',
    'case-automotive-dfmea-ontology-agent.html': 'aws.amazon.com/blogs/industries/reimagining-b-pillar-dfmea/',
    'case-supply-chain-agentic-decision.html': 'aws.amazon.com/blogs/industries/how-multi-agent-ai-turns-supply-chain-data-into-decisions-and-actions/',
    'case-financial-bda-document-automation.html': 'aws.amazon.com/blogs/machine-learning/process-financial-documents-using-amazon-bedrock-data-automation/',
    'case-vanguard-virtual-analyst.html': 'aws.amazon.com/blogs/machine-learning/building-ai-ready-data-vanguards-virtual-analyst-journey/',
    'case-agent-evaluation-first.html': 'aws.amazon.com/cn/blogs/china/part-1-enterprise-intelligent-why-evaluation/',
}
for name, source_fragment in source_contracts.items():
    source_soup=BeautifulSoup((ROOT/name).read_text(encoding='utf-8'),'html.parser')
    if not source_soup.select_one('.case-source-foot'):
        errors.append(f'{name}: missing explicit source and evidence boundary')
    if not any(source_fragment in (a.get('href') or '') for a in source_soup.select('a[href]')):
        errors.append(f'{name}: missing primary source link {source_fragment}')
    visible_text=source_soup.get_text(' ',strip=True)
    for vendor_name in ['AWS', 'Amazon', 'Bedrock', 'AgentCore', 'BDA', 'SageMaker', 'DynamoDB', 'Cognito', 'Strands']:
        if vendor_name in visible_text:
            errors.append(f'{name}: vendor brand remains in customer-facing copy: {vendor_name}')
    if 'ForFlow' not in visible_text:
        errors.append(f'{name}: ForFlow team framing missing from customer-facing copy')

for name in ['cases.html', 'search.html', 'ai-readiness-audit.html', 'service-data-governance.html', 'service-agent-build.html']:
    visible_text=BeautifulSoup((ROOT/name).read_text(encoding='utf-8'),'html.parser').get_text(' ',strip=True)
    for vendor_name in ['AWS', 'Amazon', 'Bedrock', 'AgentCore', 'BDA', 'SageMaker', 'DynamoDB', 'Cognito', 'Strands']:
        if vendor_name in visible_text:
            errors.append(f'{name}: vendor brand remains in customer-facing copy: {vendor_name}')

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
