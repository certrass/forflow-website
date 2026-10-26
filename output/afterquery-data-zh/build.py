"""Build the ForFlow data page from the captured layout and maintained copy.

Run with Python + beautifulsoup4. No network requests are made during generation.
"""
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
soup = BeautifulSoup((ROOT / 'source/reference.html').read_text(), 'html.parser')
translations = json.loads((ROOT / 'source/zh.json').read_text())
site = json.loads((ROOT / 'source/site.json').read_text())
faqs = json.loads((ROOT / 'source/faq.json').read_text())

# Translate complete semantic paragraphs before handling individual text nodes.
for node in soup.select('p'):
    text = re.sub(r'\s+', ' ', node.get_text(' ', strip=True))
    if text in translations:
        node.string = translations[text]

for node in list(soup.find_all(string=True)):
    if node.parent.name in ('script', 'style'):
        continue
    text = node.strip()
    if text in translations:
        node.replace_with(str(node).replace(text, translations[text]))

# ForFlow questions and answers are maintained independently of source claims.
assert len(soup.select('.faq-answer')) == len(faqs) == 8
for node, entry in zip(soup.select('.faq-answer'), faqs):
    node.string = entry['answer']
    node.find_parent('details').select_one('summary > span').string = entry['question']

# Keep the two Chinese clauses together when the heading wraps on a phone.
heading = soup.select_one('h1')
heading.clear()
headline = translations["Your company's data, licensed with care."]
first, second = headline.split('，', 1)
for clause in (first + '，', second):
    span = soup.new_tag('span')
    span['class'] = 'headline-clause'
    span.string = clause
    heading.append(span)

for node in soup.select('script, noscript'):
    node.decompose()
soup.html['lang'] = 'zh-CN'
soup.html.attrs.pop('data-dpl-id', None)
soup.head.clear()
head = BeautifulSoup('''
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="">
<title></title>
<link rel="icon" href="./assets/forflow-mark.png" type="image/png">
<link rel="stylesheet" href="./assets/source-fonts.css">
<link rel="stylesheet" href="./assets/source-styles.css">
<link rel="stylesheet" href="./styles.css">
''', 'html.parser')
for child in list(head.contents):
    soup.head.append(child)
soup.title.string = site['title']
soup.select_one('meta[name="description"]')['content'] = site['description']

for node in soup.select('[style]'):
    node['style'] = node['style'].replace('/brand/afterquery-logo.svg', './assets/afterquery-logo.svg')
for img in soup.select('img'):
    img['src'] = './assets/' + img['src'].split('?')[0].rsplit('/', 1)[1]
    img.attrs.pop('data-nimg', None)
    img['alt'] = '黑白办公室与团队工作场景'
    if img['src'].endswith('industries-office-hd.webp'):
        img['src'] = './assets/generated/work-records-office-v1.jpg'
        img['alt'] = '团队在办公空间整理与讨论业务资料（AI 生成情境）'
        img['width'], img['height'] = '1024', '1536'

# Apply the existing ForFlow identity to the captured layout.
for anchor in soup.select('a[aria-label="AfterQuery — home"]'):
    anchor.clear()
    anchor['aria-label'] = 'ForFlow 萬維流形首页'
    logo = soup.new_tag('img', src='./assets/forflow-lockup-transparent.png', alt='ForFlow 萬維流形')
    logo['class'] = 'forflow-logo'
    logo['width'] = '108'
    logo['height'] = '40'
    anchor.append(logo)
    anchor['class'] = ['forflow-brand']
nav = soup.select_one('header nav')
nav['aria-label'] = '主导航'
nav_links = nav.select('ul a')
for anchor, (label, href) in zip(nav_links, [
    ('数据价值', '#why'), ('合作行业', '#industries'),
    ('合作流程', '#process'), ('常见问题', '#faq')
]):
    anchor.clear()
    anchor.string = label
    anchor['href'] = href
    anchor.attrs.pop('aria-current', None)
for anchor in nav.select('a[href="/careers"]'):
    anchor.decompose()
for anchor in nav.select('a[href="/contact"]'):
    anchor.string = '了解合作'
    anchor['href'] = '#process'
mobile_links = soup.select_one('header > div').select('ul a')
for anchor, (label, href) in zip(mobile_links[:4], [
    ('数据价值', '#why'), ('合作行业', '#industries'),
    ('合作流程', '#process'), ('常见问题', '#faq')
]):
    anchor.string = label
    anchor['href'] = href
for anchor in mobile_links[4:]:
    if anchor.get('href') == '/careers':
        anchor.parent.decompose()
    else:
        anchor.string = '了解合作'
        anchor['href'] = '#process'
soup.select_one('[data-dp-section="why"]')['id'] = 'why'
footer_credit = soup.select_one('footer p')
footer_credit.clear()
footer_credit.string = '© 2026 ForFlow 萬維流形'
footer_credit['class'] = 'footer-credit'
footer_nav = soup.select('footer nav')
for column, title, items in zip(footer_nav, ['数据合作', '流程与答疑', 'ForFlow', '联系合作'], [
    [('数据价值', '#why'), ('适用行业', '#industries')],
    [('合作流程', '#process'), ('常见问题', '#faq')],
    [('公司介绍', site['company_url']), ('ForFlow One', site['product_url'])],
    [('发起数据评估', site['contact_url']), ('生态合作引荐', site['contact_url'])]
]):
    column['aria-label'] = title
    column.select_one('h2').string = title
    links = column.select_one('ul')
    links.clear()
    for label, href in items:
        li = soup.new_tag('li')
        anchor = soup.new_tag('a', href=href)
        anchor.string = label
        li.append(anchor)
        links.append(li)
hero_layers = soup.select_one('#hero').find_all('div', recursive=False)
hero_layers[2]['class'].append('ff-hero-logos')
hero_layers[3]['class'].append('ff-hero-band')
for bar in soup.select('#process h3 > span'):
    bar['style'] = 'background-color:#06e705'

# Reuse the existing ForFlow intake form. No data is submitted by this build.
for anchor in soup.select('a[href]'):
    href = anchor['href']
    if href in ('/', '/data-partnerships'):
        anchor['href'] = '#hero'
    elif href in ('/data-partnerships/start', '/data-partnerships/refer'):
        anchor['data-cta'] = 'apply' if href.endswith('/start') else 'refer'
        anchor['href'] = site['contact_url']
        anchor['title'] = '打开 ForFlow 合作咨询表单'
    elif href.startswith('/'):
        raise ValueError('Unmapped source destination: ' + href)
    if anchor['href'].startswith('https://'):
        anchor['target'] = '_blank'
        anchor['rel'] = 'noopener noreferrer'

soup.select_one('#referral [data-cta="apply"]').string = '立即开启评估 →'

menu = soup.select_one('header button')
menu['aria-label'] = '打开菜单'
menu['aria-controls'] = 'mobile-menu'
menu.parent.parent.find_next_sibling('div')['id'] = 'mobile-menu'
for node in soup.select('[aria-label="Industries"]'):
    node['aria-label'] = '行业卡片，可左右滑动'
    node['tabindex'] = '0'
soup.select_one('#faq-more')['aria-hidden'] = 'true'

for src in ('./assets/source-hero.js', './visuals.js', './script.js'):
    script = soup.new_tag('script', src=src, defer=True)
    soup.body.append(script)
(ROOT / 'index.html').write_text(str(soup), encoding='utf-8')
print('Generated', ROOT / 'index.html')

# The ForFlow research page is authored separately from the AfterQuery clone.
company_data = ROOT / 'company/data/index.html'
company_data.parent.mkdir(parents=True, exist_ok=True)
company_data.write_text((ROOT / 'source/company-data.html').read_text(), encoding='utf-8')
print('Generated', company_data)
