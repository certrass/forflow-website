# -*- coding: utf-8 -*-

from pathlib import Path
from bs4 import BeautifulSoup
import html
import re

ROOT = Path(__file__).resolve().parent

SEARCH_ICON = '''<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="m16.2 16.2 4.3 4.3"></path></svg>'''
ARROW = '<span class="arrow" aria-hidden="true">→</span>'

NAV_ITEMS = [
    ('index.html', '首页', 'home'),
    ('index.html#services', '企业服务', 'services'),
    ('navigator.html', 'AI 场景诊断', 'navigator'),
    ('playbook.html', '企业 AI 手册', 'playbook'),
    ('cases.html', '案例', 'cases'),
]

SERVICE_LINKS = [
    ('service-ai-enablement.html', '企业 AI 赋能计划'),
    ('service-data-governance.html', '数据治理'),
    ('service-agent-build.html', '企业 Agent 搭建'),
    ('service-ai-training.html', '企业 AI 培训'),
]

SERVICE_KEYS = {href.removesuffix('.html') for href, _ in SERVICE_LINKS}
TOOLS_KEYS = {'navigator', 'navigator-results', 'category-hrms'}
INSIGHT_KEYS = {'playbook', 'document-viewer'}
CASE_KEYS = {'cases', 'case-wren-kitchens'}

def current_attr(condition):
    return ' aria-current="page"' if condition else ''

def current_class(condition):
    return ' is-current' if condition else ''

def ff_icon(name):
    return f'<svg class="ff-icon" aria-hidden="true"><use href="#{name}"></use></svg>'

def ff_symbols():
    for relative in ('templates/index.html', 'index.html'):
        path = ROOT / relative
        if not path.exists():
            continue
        match = re.search(r'<svg class="ff-symbols"[\s\S]*?</svg>', path.read_text(encoding='utf-8'))
        if match:
            return match.group(0)
    return ''

def site_chrome(active=''):
    return f'{ff_symbols()}\n{header(active)}'

def header(active=''):
    services_active = active == 'services' or active in SERVICE_KEYS
    tools_active = active in TOOLS_KEYS
    insights_active = active in INSIGHT_KEYS
    cases_active = active in CASE_KEYS
    service_mobile = ''.join(
        f'<a href="{href}"{current_attr(active == href.removesuffix(".html"))}>{label}</a>'
        for href, label in SERVICE_LINKS
    )
    return f'''
<div class="ff-utility-bar">
  <div class="container ff-utility-inner">
    <span><i aria-hidden="true"></i> AI Flows. Business Grows.</span>
    <nav aria-label="快捷链接"><a href="playbook.html">企业 AI 手册</a><a href="cases.html">案例中心</a><a href="index.html#contact">方案沟通</a></nav>
  </div>
</div>
<header class="site-header ff-header" data-header>
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="ForFlow 萬維流形首页">
      <img src="assets/forflow-lockup-transparent.png" alt="ForFlow 萬維流形">
    </a>
    <nav class="primary-nav ff-mega-nav" aria-label="主导航" data-mega-root>
      <ul>
        <li><a href="index.html"{current_attr(active == 'home')}>首页</a></li>
        <li class="mega-item">
          <button class="mega-trigger{current_class(services_active)}" type="button" data-mega-trigger aria-expanded="false">企业服务 {ff_icon('i-chevron')}</button>
          <div class="mega-panel mega-panel--services" data-mega-panel>
            <div class="mega-panel-intro"><span>ENTERPRISE SERVICES</span><h2>从一个真实问题，走到可持续运行。</h2><p>四条服务路径对应企业不同阶段；不是把所有能力打包出售，而是先解决当前最重要的一步。</p><a href="index.html#services">查看全部服务 {ff_icon('i-arrow')}</a></div>
            <div class="mega-link-grid">
              <a class="mega-link" href="service-ai-enablement.html"{current_attr(active == 'service-ai-enablement')}><span class="mega-icon">{ff_icon('i-layers')}</span><span><b>企业 AI 赋能计划</b><small>把零散试用变成团队方法与可衡量成果</small></span><em>01</em></a>
              <a class="mega-link" href="service-data-governance.html"{current_attr(active == 'service-data-governance')}><span class="mega-icon">{ff_icon('i-data')}</span><span><b>数据治理</b><small>建立可信数据、知识与 AI 应用底座</small></span><em>02</em></a>
              <a class="mega-link" href="service-agent-build.html"{current_attr(active == 'service-agent-build')}><span class="mega-icon">{ff_icon('i-agent')}</span><span><b>企业 Agent 搭建</b><small>连接知识、系统、权限与真实工作流</small></span><em>03</em></a>
              <a class="mega-link" href="service-ai-training.html"{current_attr(active == 'service-ai-training')}><span class="mega-icon">{ff_icon('i-training')}</span><span><b>企业 AI 培训</b><small>按管理层、业务与技术角色分层共创</small></span><em>04</em></a>
            </div>
          </div>
        </li>
        <li class="mega-item">
          <button class="mega-trigger{current_class(tools_active)}" type="button" data-mega-trigger aria-expanded="false">场景与工具 {ff_icon('i-chevron')}</button>
          <div class="mega-panel mega-panel--tools" data-mega-panel>
            <div class="mega-panel-intro"><span>TOOLS &amp; SCENARIOS</span><h2>先找到值得做的事，再选择技术。</h2><p>用诊断、场景地图与搜索入口，把“AI 能做什么”翻译成“企业下一步做什么”。</p><a href="navigator.html">立即开始诊断 {ff_icon('i-arrow')}</a></div>
            <div class="mega-feature-stack">
              <a class="mega-feature" href="navigator.html"{current_attr(active in {'navigator', 'navigator-results'})}><span>{ff_icon('i-compass')}</span><div><b>AI 场景诊断</b><small>3 分钟定位第一条 AI 增长流</small></div><em>开始</em></a>
              <a class="mega-feature" href="category-hrms.html"{current_attr(active == 'category-hrms')}><span>{ff_icon('i-people')}</span><div><b>HR 与组织效率场景</b><small>招聘、入职、培训、员工服务与绩效</small></div><em>浏览</em></a>
              <button class="mega-feature search-trigger" type="button"><span>{ff_icon('i-search')}</span><div><b>全站搜索</b><small>查找服务、场景、资料与案例</small></div><em>搜索</em></button>
            </div>
          </div>
        </li>
        <li class="mega-item">
          <button class="mega-trigger{current_class(insights_active)}" type="button" data-mega-trigger aria-expanded="false">手册与洞察 {ff_icon('i-chevron')}</button>
          <div class="mega-panel mega-panel--insights" data-mega-panel>
            <a class="mega-editorial" href="playbook.html"{current_attr(active == 'playbook')}><span class="mega-editorial-kicker">FEATURED GUIDE</span><strong>企业生成式 AI<br>实战手册</strong><p>从基础、商业价值和买或建，到风险、安全与实施路线。</p><span class="mega-editorial-link">在线阅读 {ff_icon('i-arrow')}</span></a>
            <div class="mega-insight-list">
              <a href="cases.html"><span>{ff_icon('i-cases')}</span><div><b>企业案例中心</b><small>按问题、过程和结果阅读公开案例</small></div></a>
              <a href="case-wren-kitchens.html"><span>{ff_icon('i-growth')}</span><div><b>案例详情示范</b><small>查看完整案例页面的信息层级</small></div></a>
              <a href="document-viewer.html?doc=playbook"{current_attr(active == 'document-viewer')}><span>{ff_icon('i-document')}</span><div><b>PDF 在线阅读</b><small>在浏览器中查看与下载参考文件</small></div></a>
            </div>
          </div>
        </li>
        <li><a href="cases.html"{current_attr(cases_active)}>案例</a></li>
      </ul>
    </nav>
    <div class="header-actions">
      <button class="icon-btn search-trigger" type="button" aria-label="打开全站搜索">{ff_icon('i-search')}</button>
      <a class="btn btn--green header-cta" href="navigator.html">开始诊断 <span aria-hidden="true">→</span></a>
    </div>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="打开菜单"><span></span></button>
  </div>
</header>
<div class="mobile-menu-panel ff-mobile-menu" id="mobile-menu" aria-hidden="true">
  <a class="mobile-menu-home" href="index.html"{current_attr(active == 'home')}>首页 <span>01</span></a>
  <details{' open' if services_active else ''}><summary>企业服务 <span>02</span></summary><div class="mobile-subnav">{service_mobile}</div></details>
  <details{' open' if tools_active else ''}><summary>场景与工具 <span>03</span></summary><div class="mobile-subnav"><a href="navigator.html"{current_attr(active in {'navigator', 'navigator-results'})}>AI 场景诊断</a><a href="category-hrms.html"{current_attr(active == 'category-hrms')}>HR 场景地图</a><button class="search-trigger" type="button">全站搜索</button></div></details>
  <details{' open' if insights_active else ''}><summary>手册与洞察 <span>04</span></summary><div class="mobile-subnav"><a href="playbook.html"{current_attr(active == 'playbook')}>企业 AI 实战手册</a><a href="cases.html">案例中心</a><a href="document-viewer.html?doc=playbook"{current_attr(active == 'document-viewer')}>PDF 阅读器</a></div></details>
  <a href="cases.html"{current_attr(cases_active)}>案例 <span>05</span></a>
  <a class="btn btn--green" href="navigator.html">开始 AI 场景诊断 <span aria-hidden="true">→</span></a>
</div>'''

def footer():
    return '''
<footer class="site-footer">
  <div class="container footer-main">
    <div class="footer-brand">
      <img src="assets/forflow-lockup-transparent.png" alt="ForFlow 萬維流形">
      <p>面向企业的 AI 原生增长运行层。<br>从高价值场景、安全落地到持续运营。</p>
    </div>
    <div class="footer-col"><h3>企业服务</h3>
      <a href="service-ai-enablement.html">企业 AI 赋能计划</a>
      <a href="service-data-governance.html">数据治理</a>
      <a href="service-agent-build.html">企业 Agent 搭建</a>
      <a href="service-ai-training.html">企业 AI 培训</a>
    </div>
    <div class="footer-col"><h3>工具与资源</h3>
      <a href="navigator.html">AI 场景诊断</a>
      <a href="playbook.html">企业 AI 实战手册</a>
      <a href="category-hrms.html">HR AI 场景地图</a>
      <a href="document-viewer.html?doc=playbook">PDF 阅读器</a>
    </div>
    <div class="footer-col"><h3>案例与行动</h3>
      <a href="cases.html">案例中心</a>
      <a href="case-wren-kitchens.html">案例详情示范</a>
      <button class="footer-search search-trigger" type="button">全站搜索</button>
      <a href="navigator.html">开始诊断</a>
    </div>
  </div>
  <div class="container footer-bottom"><span>© 2026 ForFlow.ai 萬維流形</span><span>响应式企业网站原型 · CMS / CRM / 报价接口已预留</span></div>
</footer>'''

def search_modal():
    return f'''
<div class="search-modal" data-search-modal aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="search-modal-title">
  <div class="search-modal-backdrop" data-search-close></div>
  <div class="search-modal-panel">
    <h2 class="sr-only" id="search-modal-title">搜索 ForFlow</h2>
    <form class="search-modal-form" action="search.html" method="get">
      <span class="search-modal-icon">{SEARCH_ICON}</span>
      <input type="search" name="search" placeholder="输入服务、场景或资料，例如：Agent" autocomplete="off" aria-label="搜索关键词">
      <button class="btn btn--green" type="submit">搜索</button>
    </form>
    <button class="search-modal-close" type="button" data-search-close>关闭 <span aria-hidden="true">×</span></button>
    <div class="search-suggestions"><span>常用搜索</span><a href="search.html?search=Agent">企业 Agent</a><a href="search.html?search=数据治理">数据治理</a><a href="search.html?search=培训">AI 培训</a><a href="search.html?search=Playbook">企业 AI 手册</a></div>
  </div>
</div>'''

def page(title, description, active, body, body_class=''):
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#ffffff">
  <meta name="description" content="{html.escape(description)}">
  <title>{html.escape(title)}｜ForFlow 萬維流形</title>
  <link rel="icon" href="assets/forflow-mark.png">
  <link rel="stylesheet" href="styles.css">
  <script src="script.js" defer></script>
</head>
<body class="{body_class}">
<a class="skip-link" href="#main">跳至主要内容</a>
{site_chrome(active)}
<main id="main">{body}</main>
{footer()}
{search_modal()}
</body></html>'''

def patch_existing(filename, active):
    path = ROOT / filename
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    for node in [soup.find('svg', class_='ff-symbols'), soup.find('div', class_='ff-utility-bar'), soup.find('header', class_='site-header'), soup.find('div', class_='mobile-menu-panel')]:
        if node:
            node.extract()
    anchor = soup.find('main')
    if anchor:
        new_frag = BeautifulSoup(site_chrome(active), 'html.parser')
        for node in new_frag.contents:
            anchor.insert_before(node)
    # Replace all legacy logo references with correct transparent/cropped logo except deliberate cover art.
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if 'forflow-lockup' in src or 'forflow-wordmark' in src:
            img['src'] = 'assets/forflow-lockup-transparent.png'
            img['alt'] = 'ForFlow 萬維流形'
    # Footer replacement.
    old_footer = soup.find('footer')
    if old_footer:
        old_footer.replace_with(BeautifulSoup(footer(), 'html.parser').find('footer'))
    # Search modal.
    if not soup.find(attrs={'data-search-modal': True}):
        soup.body.append(BeautifulSoup(search_modal(), 'html.parser'))
    # favicon
    fav = soup.find('link', rel=lambda x: x and 'icon' in x)
    if fav: fav['href'] = 'assets/forflow-mark.png'
    else:
        tag = soup.new_tag('link', rel='icon', href='assets/forflow-mark.png')
        soup.head.append(tag)
    path.write_text(str(soup), encoding='utf-8')

# Patch existing pages instead of rebuilding them.
patch_existing('index.html', 'home')
patch_existing('navigator.html', 'navigator')

# Add the four-SKU section into the existing homepage frame.
index_path = ROOT / 'index.html'
soup = BeautifulSoup(index_path.read_text(encoding='utf-8'), 'html.parser')
content_stack = soup.find('div', class_='content-stack')
if content_stack and not soup.find(id='services'):
    service_section = BeautifulSoup('''
<section id="services" data-section>
  <div class="section-head">
    <div><p class="eyebrow">Four enterprise paths</p><h2 class="section-title">四条清晰路径，<br>从入门走向规模化。</h2></div>
    <p class="section-lead">不把“AI”当成一个模糊项目。根据企业当前问题，选择组织赋能、数据基础、Agent 搭建或分层培训。</p>
  </div>
  <div class="sku-grid">
    <a class="sku-card" href="service-ai-enablement.html" data-reveal><span class="sku-no">01</span><small>4–6 周 · 组织能力</small><h3>企业 AI 赋能计划</h3><p>把个人零散试用变成统一方法、真实任务和可衡量的团队能力。</p><span class="card-link"><span>查看服务流程与 FAQ</span><span>→</span></span></a>
    <a class="sku-card" href="service-data-governance.html" data-reveal><span class="sku-no">02</span><small>分阶段 · 数据基础</small><h3>数据治理</h3><p>让数据找得到、看得懂、用得对，为报表、RAG 与企业 AI 建立可信底座。</p><span class="card-link"><span>查看服务流程与 FAQ</span><span>→</span></span></a>
    <a class="sku-card" href="service-agent-build.html" data-reveal><span class="sku-no">03</span><small>2 周验证 · 持续实施</small><h3>企业 Agent 搭建</h3><p>让 AI 连接知识、系统和规则，不只回答问题，还能在授权范围内完成工作。</p><span class="card-link"><span>查看服务流程与 FAQ</span><span>→</span></span></a>
    <a class="sku-card" href="service-ai-training.html" data-reveal><span class="sku-no">04</span><small>分层课程 · 场景共创</small><h3>企业 AI 培训</h3><p>围绕管理层、业务团队与技术团队的真实岗位，让培训直接转化为行动。</p><span class="card-link"><span>查看服务流程与 FAQ</span><span>→</span></span></a>
  </div>
</section>''', 'html.parser').find('section')
    method = soup.find(id='method')
    if method: method.insert_before(service_section)
    else: content_stack.append(service_section)
# Add services to rail.
rail = soup.find(attrs={'data-scrollspy': True})
if rail and not rail.find('a', href='#services'):
    method_link = rail.find('a', href='#method')
    a = soup.new_tag('a', href='#services'); a.string = '四项企业服务'
    if method_link: method_link.insert_before(a)
    else: rail.append(a)
# Replace homepage placeholder resource links and case cards.
for a in soup.select('.resource-card'):
    text = a.get_text(' ', strip=True)
    if 'Playbook' in text:
        a['href'] = 'playbook.html'; a.attrs.pop('aria-label', None)
        cl = a.select_one('.card-link');
        if cl: cl.string = '在线阅读 ↗'
    elif 'Transformation' in text:
        a['href'] = 'service-ai-enablement.html'; a.attrs.pop('aria-label', None)
        cl = a.select_one('.card-link');
        if cl: cl.string = '查看企业服务 ↗'
case_cards = soup.select('.case-card')
case_hrefs = ['case-wren-kitchens.html', 'cases.html#jan-elly', 'cases.html#ihub']
for card, href in zip(case_cards, case_hrefs):
    if card.name == 'article':
        card.name = 'a'; card['href'] = href
index_path.write_text(str(soup), encoding='utf-8')

# ------------------------- New pages -------------------------

navigator_results_body = '''
<section class="results-hero">
  <div class="container results-hero-grid">
    <div class="result-video-card" data-reveal>
      <video controls muted loop playsinline autoplay preload="metadata" poster="assets/forflow-brand-motion-poster.jpg" aria-label="ForFlow 萬維流形品牌动效">
        <source src="assets/forflow-brand-motion.mp4" type="video/mp4">你的浏览器不支持视频播放。
      </video>
    </div>
    <div class="results-intro" data-reveal>
      <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="navigator.html">AI 场景诊断</a><span>/</span><strong>推荐结果</strong></nav>
      <p class="eyebrow">Recommended routes</p>
      <h1>为你的业务优先级<br>匹配的建议。</h1>
      <p>结果不是一张“工具清单”，而是按价值、准备度、数据约束和实施周期排序的行动路径。</p>
      <a class="text-link" href="navigator.html">编辑你的回答 →</a>
    </div>
  </div>
</section>
<section class="results-context">
  <div class="container results-context-card" data-reveal>
    <div><small>你的业务重点</small><strong data-result-challenge>企业知识与运营效率</strong></div>
    <div><small>优先价值</small><strong data-result-goal>缩短处理时间 · 提高质量</strong></div>
    <div><small>建议起步</small><strong data-result-start>2 周场景验证</strong></div>
    <div><small>部署边界</small><strong data-result-deployment>混合部署优先</strong></div>
  </div>
</section>
<section class="results-listing section-pad">
  <div class="container">
    <div class="section-head"><div><p class="eyebrow">Recommended solutions</p><h2 class="section-title">先做最值得验证的，<br>再扩展到组织级能力。</h2></div><p class="section-lead">可按“最匹配、最快见效、基础优先”排序。正式上线时可接方案库、报价、CRM 与收藏功能。</p></div>
    <div class="results-panel">
      <aside class="sort-sidebar"><small>排序方式</small><button class="is-active" data-sort="match">最匹配</button><button data-sort="speed">最快见效</button><button data-sort="foundation">基础优先</button></aside>
      <div class="solution-list">
        <div class="mobile-sort"><button type="button" data-mobile-sort-toggle>排序：<span>最匹配</span> ↓</button><div data-mobile-sort-menu><button data-sort="match">最匹配</button><button data-sort="speed">最快见效</button><button data-sort="foundation">基础优先</button></div></div>
        <article class="solution-card" data-solution="agent" data-rank-match="1" data-rank-speed="1" data-rank-foundation="3">
          <div class="solution-main"><div class="solution-topline"><span class="solution-index">01</span><button class="favorite-btn" type="button" aria-label="收藏方案">♡</button></div><h3>企业 Agent 搭建</h3><p>适合把知识查询、文档处理、客户或员工服务接入真实流程，并保留权限、审批与人工复核。</p><div class="micro-tags"><span>AI Agent</span><span>RAG</span><span>系统集成</span></div><div class="feature-columns"><ul><li>流程与高价值用例拆解</li><li>2 周可工作的 PoC</li><li>权限、审计与异常回退</li></ul><ul><li>连接知识库、API 与业务系统</li><li>正式实施路线图</li><li>运行监控与持续优化</li></ul></div></div>
          <div class="solution-side"><small>建议起步</small><strong>2 周验证</strong><span>随后按里程碑实施</span><a class="btn btn--green" href="service-agent-build.html">查看详情 →</a></div>
        </article>
        <article class="solution-card" data-solution="data" data-rank-match="2" data-rank-speed="4" data-rank-foundation="1">
          <div class="solution-main"><div class="solution-topline"><span class="solution-index">02</span><button class="favorite-btn" type="button" aria-label="收藏方案">♡</button></div><h3>数据治理与 AI 就绪</h3><p>适合资料散落、指标不一致、数据权限不清，或准备建设企业知识库、分析与 RAG 的组织。</p><div class="micro-tags"><span>数据资产</span><span>质量规则</span><span>AI 数据层</span></div><div class="feature-columns"><ul><li>数据资产与风险盘点</li><li>指标、主数据和质量规则</li><li>数据管道与访问机制</li></ul><ul><li>权限、血缘与审计</li><li>向量检索和 RAG 数据层</li><li>分阶段建设路线</li></ul></div></div>
          <div class="solution-side"><small>建议起步</small><strong>2–4 周盘点</strong><span>按优先域分阶段建设</span><a class="btn btn--green" href="service-data-governance.html">查看详情 →</a></div>
        </article>
        <article class="solution-card" data-solution="enablement" data-rank-match="3" data-rank-speed="2" data-rank-foundation="2">
          <div class="solution-main"><div class="solution-topline"><span class="solution-index">03</span><button class="favorite-btn" type="button" aria-label="收藏方案">♡</button></div><h3>企业 AI 赋能计划</h3><p>适合已有零散 AI 试用，但缺少统一方法、内部负责人、使用规范和可衡量业务结果的团队。</p><div class="micro-tags"><span>组织采用</span><span>真实任务</span><span>指标体系</span></div><div class="feature-columns"><ul><li>现状盘点与工具设置</li><li>真实项目实战陪跑</li><li>内部 Champion 培养</li></ul><ul><li>采用率与绩效指标</li><li>最佳实践与使用规范</li><li>规模化推广建议</li></ul></div></div>
          <div class="solution-side"><small>典型周期</small><strong>4–6 周</strong><span>以真实业务任务为主线</span><a class="btn btn--green" href="service-ai-enablement.html">查看详情 →</a></div>
        </article>
        <article class="solution-card" data-solution="training" data-rank-match="4" data-rank-speed="3" data-rank-foundation="4">
          <div class="solution-main"><div class="solution-topline"><span class="solution-index">04</span><button class="favorite-btn" type="button" aria-label="收藏方案">♡</button></div><h3>企业 AI 分层培训</h3><p>适合需要让管理层会判断、业务团队会使用、技术团队会落地，并建立统一数据与使用边界的企业。</p><div class="micro-tags"><span>管理层</span><span>业务实战</span><span>安全规范</span></div><div class="feature-columns"><ul><li>岗位与场景定制课程</li><li>提示词与工作流实战</li><li>数据安全和责任边界</li></ul><ul><li>场景共创与行动计划</li><li>课后资料包</li><li>可选 30 天陪跑</li></ul></div></div>
          <div class="solution-side"><small>建议形式</small><strong>1–3 天</strong><span>可叠加 30 天陪跑</span><a class="btn btn--green" href="service-ai-training.html">查看详情 →</a></div>
        </article>
      </div>
    </div>
  </div>
</section>
<section class="final-cta"><div class="container final-cta-inner"><div><h2>把结果变成一张<br>可讨论的项目卡。</h2><p>带上当前流程、样本数据和希望改善的指标，进行一次 30 分钟项目梳理。</p></div><a class="btn" href="navigator.html">重新诊断 →</a></div></section>
'''
(ROOT/'navigator-results.html').write_text(page('AI 场景诊断结果','根据业务优先级生成企业 AI 行动建议。','navigator',navigator_results_body,'results-page'),encoding='utf-8')

playbook_body = '''
<section class="playbook-cover">
  <div class="container playbook-cover-grid">
    <div class="playbook-cover-copy" data-reveal><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>企业 AI 手册</strong></nav><p class="eyebrow">Generative AI Playbook for Enterprises</p><h1>企业生成式 AI<br>实战手册</h1><p>用企业能理解、能讨论、能执行的中文，讲清 GenAI 基础、业务机会、买还是建、风险治理与落地路线。</p><div class="hero-actions"><a class="btn btn--green" href="#intro">开始阅读 →</a><a class="btn btn--ghost" href="document-viewer.html?doc=playbook">查看原始 PDF</a></div></div>
    <div class="playbook-cover-art" data-reveal><img src="assets/forflow-lockup.png" alt="ForFlow 萬維流形完整品牌标识"><div class="cover-chapters"><span>01 基础</span><span>02 机会</span><span>03 买或建</span><span>04 应用</span><span>05 风险</span><span>06 建设</span></div></div>
  </div>
</section>
<div class="container playbook-mobile-tools"><button class="btn btn--ghost" type="button" data-toc-open>目录</button><a class="btn btn--green" href="assets/genai-playbook-reference.pdf" download>下载 PDF</a></div>
<div class="container playbook-shell">
  <aside class="playbook-toc"><div class="playbook-toc-inner"><small>本页目录</small><nav data-scrollspy><a href="#intro" class="is-active">认识 GenAI</a><a href="#opportunity">业务机会</a><a href="#decision">买还是建</a><a href="#buy">采用现成方案</a><a href="#risk">风险与安全</a><a href="#build">定制与自建</a><a href="#stories">公开案例</a><a href="#start">开始行动</a></nav><a class="btn btn--ghost btn--block" href="assets/genai-playbook-reference.pdf" download>下载参考 PDF</a></div></aside>
  <article class="playbook-content">
    <section id="intro" data-section class="playbook-section"><header><span class="chapter-no">01</span><div><p class="eyebrow">Introduction</p><h2>先用业务语言认识 GenAI。</h2></div></header><p class="chapter-lead">生成式 AI 会根据学习到的模式生成文字、图片、声音、视频、代码等内容。企业真正需要理解的，不是模型名称，而是它能否在可信数据、清晰流程和责任边界内解决问题。</p>
      <h3 class="subchapter-title">AI 与 GenAI 的演进</h3><div class="timeline-grid"><div><b>1956</b><span>人工智能成为计算机科学中的独立研究方向，目标是让机器完成需要人类智能的任务。</span></div><div><b>1990s</b><span>互联网和数据规模增长推动机器学习，让系统可以从数据中改进判断。</span></div><div><b>2010s</b><span>深度学习让机器在图像、语音和复杂模式识别方面取得突破。</span></div><div><b>2021+</b><span>大规模预训练模型让普通人可以通过提示词生成文本、图像、声音和代码。</span></div></div>
      <div class="info-grid"><article><h3>大语言模型（LLM）</h3><p>LLM 专门处理和生成人类语言。参数和训练数据越丰富，模型越能识别复杂语义与上下文；但“模型更大”不等于企业答案一定正确，仍需要知识、权限、评估和人工判断。</p></article><article><h3>检索增强生成（RAG）</h3><p>RAG 在模型回答前，先从企业授权资料中检索相关内容，再把结果交给模型生成答案。它让 AI 更贴近企业制度、产品和流程，并能附上来源，便于核验。</p></article></div>
      <h3 class="subchapter-title">常见模型与企业用途</h3><div class="model-grid"><article><b>01</b><h4>文本生成</h4><p>报告、邮件、内容、客服、知识问答。</p></article><article><b>02</b><h4>图像生成</h4><p>设计概念、营销素材、视觉故事。</p></article><article><b>03</b><h4>音频与语音</h4><p>转录、语音助手、播客与无障碍。</p></article><article><b>04</b><h4>视频生成</h4><p>营销视频、培训内容和个性化素材。</p></article><article><b>05</b><h4>翻译与本地化</h4><p>实时翻译、文档翻译和跨区域沟通。</p></article><article><b>06</b><h4>代码生成</h4><p>开发、测试、调试和技术文档。</p></article><article><b>07</b><h4>3D 与多模态</h4><p>产品设计、仿真，以及文字、图像、音视频联合处理。</p></article><article><b>08</b><h4>识别与理解</h4><p>从文档、图像、录音中提取信息并分类。</p></article></div>
    </section>
    <section id="opportunity" data-section class="playbook-section"><header><span class="chapter-no">02</span><div><p class="eyebrow">Growth opportunities</p><h2>四类企业价值，先选一项作为主指标。</h2></div></header><div class="benefit-grid"><article><span>01</span><h3>提高效率</h3><p>自动完成内容初稿、资料查找、重复问答和数据整理，让员工回到需要判断和创造力的工作。</p></article><article><span>02</span><h3>个性化体验</h3><p>根据客户资料与偏好，在合适渠道提供更相关的产品、服务和沟通。</p></article><article><span>03</span><h3>降低成本</h3><p>减少人工复制、重复处理和跨系统查找，优化资源分配。</p></article><article><span>04</span><h3>增加收入</h3><p>通过更快响应、个性化推荐、精准营销和新服务形成增长机会。</p></article></div><div class="callout"><strong>企业视角</strong><p>不要同时追求所有收益。首个项目最好只设一个主指标，例如处理时长、一次解决率、转化率或错误率，再配两个保护指标，如合规和客户满意度。</p></div></section>
    <section id="decision" data-section class="playbook-section"><header><span class="chapter-no">03</span><div><p class="eyebrow">Buy or build</p><h2>现成方案，还是定制能力？</h2></div></header><p class="chapter-lead">对于常见需求、经验较少或希望快速启动的企业，先采用成熟方案通常更合适；当流程独特、数据敏感、需要深度集成或可形成竞争优势时，再考虑定制与自建。</p><div class="decision-grid"><article><h3>购买现成方案</h3><ul><li>上线快，初期投入较低</li><li>由供应商负责维护与更新</li><li>适合常见办公、内容、客服和 HR 场景</li><li>定制、模型控制和深度集成可能受限</li></ul></article><article><h3>定制或建设</h3><ul><li>贴合独特流程、数据和交互</li><li>对安全、权限和模型选择控制更强</li><li>可沉淀为企业专属能力与知识产权</li><li>需要更多技术、预算和长期运维</li></ul></article></div><div class="decision-table"><div><b>考虑因素</b><b>更偏向买</b><b>更偏向建</b></div><div><span>成本</span><span>关注前期投入与快速使用</span><span>高频长期使用，能承担建设与维护</span></div><div><span>业务要求</span><span>需求通用，市场方案已成熟</span><span>流程复杂或差异化价值明显</span></div><div><span>经验</span><span>刚接触 GenAI，希望先积累经验</span><span>已有技术团队和试点经验</span></div><div><span>风险治理</span><span>可接受供应商承担部分维护责任</span><span>需要更强数据、模型和升级控制</span></div><div><span>定制集成</span><span>标准接口和体验已足够</span><span>需深入接入系统、权限与工作流</span></div></div></section>
    <section id="buy" data-section class="playbook-section"><header><span class="chapter-no">04</span><div><p class="eyebrow">Buy</p><h2>适合直接采用的常见场景。</h2></div></header><div class="usecase-accordion"><details open><summary><span>01</span>办公效率</summary><div><h4>文档生成</h4><p>根据多源资料生成报告、邮件、方案与演示文稿初稿。</p><h4>会议管理</h4><p>安排会议、转录、总结、提取行动项并跟踪。</p><h4>数据分析与报告</h4><p>识别趋势、生成管理摘要和可视化说明。</p></div></details><details><summary><span>02</span>营销与销售</summary><div><h4>多渠道内容</h4><p>快速生成文案、图片、视频和不同渠道版本。</p><h4>个性化沟通</h4><p>根据客户画像调整消息、产品推荐与跟进。</p><h4>市场洞察</h4><p>汇总趋势、竞品和客户反馈，形成易读报告。</p></div></details><details><summary><span>03</span>客户互动</summary><div><h4>前台服务</h4><p>线索收集、销售辅助、售前售后问答、预约和预订。</p><h4>后台辅助</h4><p>对话转录、回复建议、知识检索、情绪与质量分析。</p></div></details><details><summary><span>04</span>人力资源</summary><div><h4>人才招聘</h4><p>职位描述、简历初筛、候选人沟通和面试辅助。</p><h4>入职与员工服务</h4><p>个性化入职清单、制度问答、培训与绩效辅助。</p></div></details></div>
      <h3 class="subchapter-title">购买前的四项检查</h3><div class="check-grid"><article><h4>数据与时间投入</h4><p>准备准确、最新、可授权的数据，并安排业务人员参与配置和评估。</p></article><article><h4>供应商与工具</h4><p>比较易用性、功能、支持能力、稳定性和退出机制。</p></article><article><h4>内容质量</h4><p>建立事实核验、品牌语气、版权和敏感内容规则。</p></article><article><h4>持续改进</h4><p>监测质量与采用率，收集反馈，持续调整提示词和流程。</p></article></div>
      <h3 class="subchapter-title">提示词的 7 个实用原则</h3><ol class="prompt-list"><li><b>具体清楚</b><span>说明任务、长度、要点和输出格式。</span></li><li><b>补充上下文</b><span>提供业务背景、资料范围和当前条件。</span></li><li><b>说明受众与语气</b><span>例如面向管理层、客户或新员工。</span></li><li><b>给出示例</b><span>让 AI 理解你希望的结构和质量。</span></li><li><b>设置边界</b><span>指定不能编造、必须引用、需要人工确认的内容。</span></li><li><b>要求多个选项</b><span>便于比较、组合和选择。</span></li><li><b>迭代优化</b><span>把第一次输出当作初稿，持续补充与修正。</span></li></ol>
    </section>
    <section id="risk" data-section class="playbook-section"><header><span class="chapter-no">05</span><div><p class="eyebrow">Risk & security</p><h2>让 AI 可用，也要让它可控。</h2></div></header><div class="risk-grid"><article><span>01</span><h3>“编造”与错误</h3><p>对关键事实使用可信来源、限定知识范围、显示引用并保留人工复核。</p></article><article><span>02</span><h3>偏差与不公平</h3><p>检查不同群体结果，使用多样化样本，并保留申诉和人工判断。</p></article><article><span>03</span><h3>过度依赖</h3><p>明确 AI 是助手而非责任主体，关键决定由授权人员确认。</p></article><article><span>04</span><h3>合规与伦理</h3><p>定义不可使用场景、知识产权规则、记录留存和透明告知。</p></article></div><div class="security-list"><h3>企业数据的基本安全做法</h3><ul><li>员工输入外部工具前，先确认数据分类与允许用途。</li><li>了解供应商是否保留、训练或跨境传输输入数据。</li><li>对提示注入、恶意文件、越权访问和敏感输出进行测试。</li><li>关键流程设置人工审批、审计日志与异常回退。</li><li>定期检查供应商安全、漏洞修复和治理流程。</li></ul></div></section>
    <section id="build" data-section class="playbook-section"><header><span class="chapter-no">06</span><div><p class="eyebrow">Build</p><h2>自建不等于从零训练一个大模型。</h2></div></header><p class="chapter-lead">企业“自建”通常指在现有模型基础上，接入企业数据、系统和工作流，形成可控应用或 Agent。真正从零训练模型只适合极少数具备规模、数据和研发能力的组织。</p><div class="build-modes"><article><span>01</span><h3>定制与适配</h3><p>基于现成模型与产品，增加 RAG、企业接口、专属交互和规则。适合多数企业场景，周期更短、风险更可控。</p></article><article><span>02</span><h3>专属方案</h3><p>为复杂工作流、多模态、跨业务单元或高度差异化需求设计专属架构。控制更强，但投入和运维要求更高。</p></article></div><h3 class="subchapter-title">建设所需能力</h3><div class="capability-list"><span>AI / ML 工程</span><span>软件与系统集成</span><span>数据工程</span><span>云与基础设施</span><span>前后端产品开发</span><span>安全、治理与运营</span></div><div class="partner-check"><h3>选择技术伙伴时看什么</h3><div><b>能否落地与长期支持</b><p>不仅会做 Demo，还能接系统、做监控、培训和维护。</p></div><div><b>相关经验与取舍能力</b><p>理解行业、流程和技术演进，能解释为什么这样选。</p></div><div><b>数据安全与合规</b><p>权限、日志、测试、责任边界和退出方案清楚。</p></div><div><b>信誉、稳定与伦理</b><p>团队稳定，价值观与企业长期目标一致。</p></div></div></section>
    <section id="stories" data-section class="playbook-section"><header><span class="chapter-no">07</span><div><p class="eyebrow">Public success stories</p><h2>公开案例告诉我们：从具体问题开始。</h2></div></header><div class="story-grid"><article><small>教育内容 · Jan & Elly</small><h3>18 小时 → 30 分钟</h3><p>用 GenAI 辅助选题、写作和 SEO，把内容生产变成稳定流程，并把员工培训纳入采用计划。</p></article><article><small>零售客服 · Crestar Fan</small><h3>重复任务时间 -56%</h3><p>通过全天候智能客服加快响应，让团队转向高价值服务；公开资料同时报告销售显著增长。</p></article><article><small>教育运营 · EtonHouse</small><h3>预计行政时间 -80%</h3><p>建设符合教学法和学生进度的课程与活动规划助手，并同步培训教师和开发团队。</p></article><article><small>物流数据 · iHub</small><h3>预计报表时间 -50%</h3><p>把多源数据查询转为自然语言对话，并计划增加图表和摘要，提升客户实时洞察。</p></article></div><p class="source-note">以上为用户提供的公开案例内容摘要，用于解释落地方法；正式发布前应复核来源、授权和最新结果。</p></section>
    <section id="start" data-section class="playbook-section"><header><span class="chapter-no">08</span><div><p class="eyebrow">Getting started</p><h2>用五步开始，而不是一次做大。</h2></div></header><ol class="start-steps"><li><span>1</span><div><h3>识别场景</h3><p>从内容、客服、HR、数据分析或流程中寻找高频、耗时、可衡量任务。</p></div></li><li><span>2</span><div><h3>选择工具或建设方式</h3><p>比较易用性、扩展、集成、数据安全和长期策略。</p></div></li><li><span>3</span><div><h3>建立基础</h3><p>准备负责人、数据、培训和使用规范。</p></div></li><li><span>4</span><div><h3>小步试点</h3><p>用小项目建立经验，记录质量、效率和风险。</p></div></li><li><span>5</span><div><h3>监测与扩展</h3><p>根据指标和反馈调整，再推广到更多流程。</p></div></li></ol><div class="chapter-cta"><div><h3>从企业自己的场景开始。</h3><p>AI Navigator 会把本手册的方法转成一份 3 分钟问卷和推荐结果。</p></div><a class="btn btn--green" href="navigator.html">进入 AI 场景诊断 →</a></div></section>
  </article>
</div>
<div class="playbook-toc-drawer" data-toc-drawer aria-hidden="true"><button type="button" data-toc-close>关闭目录 ×</button><a href="#intro">认识 GenAI</a><a href="#opportunity">业务机会</a><a href="#decision">买还是建</a><a href="#buy">采用现成方案</a><a href="#risk">风险与安全</a><a href="#build">定制与自建</a><a href="#stories">公开案例</a><a href="#start">开始行动</a></div>
'''
(ROOT/'playbook.html').write_text(page('企业生成式 AI 实战手册','企业生成式 AI 基础、业务机会、购买与建设、风险治理和落地路线。','playbook',playbook_body,'playbook-page'),encoding='utf-8')

# Service page generator.
def service_page(slug, title, eyebrow, subtitle, intro, pains, outcomes, scope, process, deliverables, faqs, related):
    pain_html=''.join(f'<article><span>{i:02d}</span><h3>{h}</h3><p>{p}</p></article>' for i,(h,p) in enumerate(pains,1))
    outcome_html=''.join(f'<article><span>{i:02d}</span><h3>{h}</h3><p>{p}</p></article>' for i,(h,p) in enumerate(outcomes,1))
    scope_html=''.join(f'<article><span class="service-glyph">{i:02d}</span><h3>{h}</h3><p>{p}</p></article>' for i,(h,p) in enumerate(scope,1))
    process_html=''.join(f'<li><span>{i:02d}</span><div><h3>{h}</h3><p>{p}</p></div></li>' for i,(h,p) in enumerate(process,1))
    deliver_html=''.join(f'<article><h3>{h}</h3><p>{p}</p></article>' for h,p in deliverables)
    faq_html=''.join(f'<article class="faq-item"><button class="faq-question" type="button" aria-expanded="false"><span>{q}</span><span class="plus">+</span></button><div class="faq-answer"><div><p>{a}</p></div></div></article>' for q,a in faqs)
    related_html=''.join(f'<a href="{href}"><span>{i:02d}</span><div><h3>{name}</h3><p>{desc}</p></div><b>→</b></a>' for i,(href,name,desc) in enumerate(related,1))
    body=f'''
<section class="service-hero"><div class="container service-hero-grid"><div class="service-hero-copy" data-reveal><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="index.html#services">企业服务</a><span>/</span><strong>{title}</strong></nav><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="service-hero-lead">{subtitle}</p><div class="hero-actions"><a class="btn btn--green" href="navigator.html">从业务问题开始 →</a><a class="btn btn--ghost" href="#process">查看服务流程</a></div></div><div class="service-hero-art" data-code="{slug[:2].upper()}" data-reveal><div class="service-orbit"></div><div class="service-hero-card"><small>ForFlow Method</small><strong>问题 → 价值 → 方案 → 运营</strong><span>每一步都有业务负责人和可衡量结果</span></div></div></div></section>
<section class="service-insight section-pad"><div class="container"><div class="section-head"><div><p class="eyebrow">Why now</p><h2 class="section-title">{intro}</h2></div><p class="section-lead">先把经营问题说清楚，再讨论工具、模型和技术架构。</p></div><div class="problem-grid">{pain_html}</div></div></section>
<section class="service-transformation section-pad section-ink"><div class="container"><div class="section-head"><div><p class="eyebrow eyebrow--light">From now to next</p><h2 class="section-title">从“尝试”走向<br>可持续的业务能力。</h2></div><p class="section-lead">目标不是短期炫技，而是让方法、数据和团队在项目结束后继续工作。</p></div><div class="outcome-grid">{outcome_html}</div></div></section>
<section class="service-scope section-pad"><div class="container"><div class="section-head"><div><p class="eyebrow">Scope</p><h2 class="section-title">服务范围</h2></div><p class="section-lead">根据企业成熟度组合模块，不强迫一次性购买完整范围。</p></div><div class="scope-grid">{scope_html}</div></div></section>
<section class="service-process-section section-pad" id="process"><div class="container service-process"><div class="process-intro"><p class="eyebrow">How it works</p><h2 class="section-title section-title--small">服务流程</h2><p>每个阶段都有明确输入、决策点和交付物，便于企业内部推进。</p></div><ol class="process-list">{process_html}</ol></div></section>
<section class="service-deliverables section-pad surface"><div class="container"><div class="section-head"><div><p class="eyebrow">Deliverables</p><h2 class="section-title">项目结束时，<br>你会拿到什么。</h2></div></div><div class="deliverable-grid">{deliver_html}</div></div></section>
<section class="service-faq section-pad"><div class="container faq-layout"><div><p class="eyebrow">FAQ</p><h2 class="section-title section-title--small">常见问题</h2><p class="section-lead">围绕投入、周期、数据和团队配合，把关键疑问提前说清楚。</p></div><div class="faq-list">{faq_html}</div></div></section>
<section class="related-services section-pad section-ink"><div class="container"><div class="section-head"><div><p class="eyebrow eyebrow--light">Related paths</p><h2 class="section-title">与这项服务配套的路径。</h2></div></div><div class="related-service-list">{related_html}</div></div></section>
<section class="final-cta"><div class="container final-cta-inner"><div><h2>先用一个业务问题，<br>确认是否值得投入。</h2><p>3 分钟场景诊断会给出第一版优先级、部署边界和下一步。</p></div><a class="btn" href="navigator.html">开始诊断 →</a></div></section>'''
    (ROOT/f'{slug}.html').write_text(page(title,subtitle,slug,body,f'service-page {slug}'),encoding='utf-8')

service_page(
 'service-ai-enablement','企业 AI 赋能计划','AI Enablement Program','把零散试用变成团队真正会用、持续会用、能够衡量的组织能力。','几乎每个人都在试 AI，企业却不一定更快。',
 [('碎片化采用','员工各自试工具，经验无法复用，输出质量和数据边界不一致。'),('停留在表面','AI 只用于简单问答或改写，没有进入真实流程、知识和协作。'),('无法证明价值','缺少采用率、质量和交付指标，管理层不知道该不该继续投入。')],
 [('更快见效','团队在真实任务中建立适合自己的用法，而不是从头摸索。'),('统一最佳实践','形成工具配置、提示词、审核和数据使用的共同标准。'),('可持续内部能力','培养负责人和内部 Champion，项目结束后继续迭代。'),('可衡量规模化','用采用率、交付时长、质量与业务结果决定扩展节奏。')],
 [('实战陪跑','顾问与业务/技术团队在真实任务中并肩工作，示范可复用方法。'),('环境与工具设置','配置账号、权限、知识、模板和必要的集成环境。'),('采用与绩效指标','建立使用率、时效、质量、返工和满意度等指标。'),('内部 Champion 培养','培训能够答疑、复盘和推广的内部负责人。'),('最佳实践与规范','沉淀提示词、审核、数据边界、异常处理和使用指引。'),('即时咨询','在实际使用遇到问题时提供答疑、评审和优化建议。')],
 [('现状盘点与设置（约 1 周）','了解团队结构、现有工具、使用态度、流程和主要阻碍，完成基础环境设置。'),('目标与行动计划（约 1 周）','明确成功标准、负责人、成熟度基线和本月赋能路线。'),('真实任务实战（约 2 周）','围绕真实项目进行共创、复盘、模板优化和 Champion 培养。'),('复盘与规模化（约 1 周）','汇总指标、最佳实践、剩余风险和更大范围推广建议。')],
 [('AI 采用现状与成熟度基线','说明目前谁在用、用在哪、效果怎样、风险在哪里。'),('真实任务模板与工作流','可直接复用的提示词、审核清单、工具配置和操作步骤。'),('团队指标与复盘报告','采用率、节省时间、质量变化和问题清单。'),('内部推广路线图','负责人、培训节奏、场景扩展顺序和治理建议。')],
 [('没有技术团队也能做吗？','可以。业务团队负责真实任务和结果判断，ForFlow 负责方法、工具配置与必要技术支持；涉及系统集成时再加入 IT 或技术伙伴。'),('为什么不是只做一次培训？','单次培训容易停留在概念。赋能计划把学习放进真实任务，并持续观察采用、质量和阻碍。'),('需要统一更换所有 AI 工具吗？','不需要。会先盘点现有工具与安全政策，优先复用；只有明显不满足需求时才建议调整。'),('如何衡量效果？','在启动前确定基线，例如完成任务所需时间、返工率、质量评分、采用率和业务指标。'),('员工会不会抗拒？','会通过真实痛点、清晰边界、小范围示范和内部 Champion 降低不确定感，而不是强制“一刀切”。'),('能否扩展到其他部门？','可以。先在一个团队验证方法，再把模板、指标和治理机制复制到相近流程。')],
 [('service-ai-training.html','企业 AI 培训','为管理层、业务与技术团队建立共同语言。'),('service-agent-build.html','企业 Agent 搭建','把已验证用法接进知识与业务流程。'),('service-data-governance.html','数据治理','解决知识、指标、质量和权限基础问题。')]
)

service_page(
 'service-data-governance','数据治理','Data Governance & AI Readiness','让数据找得到、看得懂、用得对，才能让报表、RAG 与企业 AI 给出可信答案。','数据一直在产生，却没有真正变成可复用的资产。',
 [('数据散落','交易、客户、文档和流程数据分布在数据库、文件、SaaS 与个人电脑。'),('答案不一致','不同部门对指标、客户和产品有不同口径，管理层无法快速确认真相。'),('AI 无法安全使用','数据质量、权限、来源和保留规则不清，AI 接入后风险被放大。')],
 [('一张数据资产地图','知道有哪些数据、在哪里、谁负责、能否用于分析与 AI。'),('统一指标与质量规则','关键业务概念、指标口径和质量标准有明确负责人。'),('可复用的数据管道','从系统、API、文件和 SaaS 自动汇集、清洗和更新。'),('AI 就绪的数据访问','让分析、知识检索和 Agent 在授权范围内取得可信数据。')],
 [('数据资产盘点','梳理数据库、文件、SaaS、报表、文档和非结构化知识。'),('ETL / ELT 与数据管道','建立自动采集、清洗、转换和更新流程。'),('数据仓库与湖仓','为报表、分析、模型和历史追溯提供统一存储。'),('指标、主数据与质量','统一客户、产品、组织等核心对象和关键指标。'),('权限、血缘与审计','记录数据从哪里来、谁能用、如何变更、如何追责。'),('AI / RAG 数据层','为向量检索、知识库、实时数据和 Agent 设计安全访问。')],
 [('数据与业务访谈','从管理问题、报表、AI 计划和现有系统了解真实需求。'),('资产与风险盘点','建立数据目录、质量问题、权限风险和优先级。'),('目标架构与治理设计','明确数据域、指标、管道、存储、责任和访问方式。'),('分阶段建设','从一个高价值数据域开始实施、验证与迁移。'),('运营与持续改进','建立质量监测、变更流程、使用反馈和治理例会。')],
 [('数据资产与责任地图','数据源、负责人、用途、敏感等级和当前质量一目了然。'),('目标架构与分期路线','说明先做什么、依赖什么、如何逐步减少风险。'),('指标与质量规则','关键口径、校验方式、异常处理和责任人。'),('AI 数据访问规范','RAG、Agent、分析和外部模型可使用的数据边界与审计要求。')],
 [('是不是要先建设一个很大的数据平台？','不一定。通常从最影响业务或 AI 场景的一个数据域开始，先解决口径、质量和访问，再决定是否扩展平台。'),('现有 ERP、CRM 和 BI 还能继续用吗？','可以。治理目标是连接和统一，不是为了替换而替换。会优先利用现有接口和投资。'),('文档和知识库也属于数据治理吗？','属于。企业 AI 大量依赖非结构化资料，需要版本、权限、有效期、来源和更新责任。'),('多久能看到效果？','盘点和优先级通常可在 2–4 周形成；建设周期取决于数据源数量、质量和系统接口。'),('如何判断数据是否 AI 就绪？','至少要能确认来源、权限、更新频率、质量、敏感等级和责任人，并有可重复的访问方式。'),('治理会不会增加业务负担？','好的治理会把责任嵌入现有流程，并用自动监测减少人工核对，而不是增加大量表格。')],
 [('service-agent-build.html','企业 Agent 搭建','在可信数据和权限基础上连接真实工作流。'),('service-ai-enablement.html','企业 AI 赋能计划','让团队采用和治理机制同步建立。'),('playbook.html','企业 AI 实战手册','了解 RAG、风险与买还是建。')]
)

service_page(
 'service-agent-build','企业 Agent 搭建','AI Agents Development','让 AI 不只回答问题，还能连接系统、遵守规则并在授权范围内完成工作。','真正拖慢团队的，往往是大量“必须做、但不值得人一直做”的工作。',
 [('重复任务过多','员工反复查资料、复制内容、整理文档、更新系统和跟进状态。'),('系统彼此割裂','数据和流程分布在多个系统，必须靠人工拼接上下文。'),('高峰期服务下降','客户或内部需求增加时，响应时间和质量快速波动。')],
 [('找到最佳切入点','从高频、可衡量、风险可控的流程中选择首个 Agent 场景。'),('两周可工作的 PoC','用真实知识、样本和流程验证，不只展示对话界面。'),('明确正式实施路线','确认系统连接、权限、安全、成本和团队要求。'),('可运营的 Agent','建立监控、人工接管、反馈和持续优化机制。')],
 [('知识型 Agent','从制度、产品、项目和文档中检索并提供可引用答案。'),('流程型 Agent','理解输入、调用工具、触发任务、等待审批并更新状态。'),('客户 / 员工服务 Agent','处理高频问题、收集信息、分流和生成回复建议。'),('分析型 Agent','连接数据源，用自然语言生成报告、图表和异常提示。'),('多 Agent 编排','让多个专职 Agent 在明确边界内协同完成复杂任务。'),('运行与治理','权限、审计、提示注入防护、成本、质量和人工回退。')],
 [('认识 Agent 与业务边界','建立共同理解：Agent 能做什么、不能做什么、责任在哪里。'),('场景发现与流程拆解','梳理关键流程、系统依赖、异常和高价值用例。'),('方案与安全设计','验证模型、数据、工具、权限、审计和部署可行性。'),('工作 PoC','在 2 周左右让 Agent 完成一个真实流程，验证价值与风险。'),('正式实施与运营','按路线图接入生产系统，建立监控、回退和持续优化。')],
 [('Agent 场景优先级与业务案例','价值、可行性、风险、预计周期和成功指标。'),('可工作的 PoC','可演示真实任务、知识、系统调用和人工审批。'),('目标架构与安全设计','模型、RAG、工具、权限、日志、部署和回退方式。'),('实施与运营路线图','里程碑、团队、成本、质量评估和扩展顺序。')],
 [('Agent 和普通聊天机器人有什么区别？','聊天机器人主要对话；Agent 会在权限范围内调用知识、系统和工具，执行多步任务，并需要更严格的监控与回退。'),('两周一定能上线生产吗？','两周目标通常是完成可工作的验证 PoC。生产上线取决于系统接口、数据敏感度、权限和异常复杂度。'),('是否必须私有化？','不一定。根据数据分类、监管、延迟和成本选择云端、混合或私有化，并可让敏感数据留在内部。'),('如何避免 Agent 做错事？','限制可用工具和权限，设置输入输出校验、人工审批、审计日志、预算和异常回退，并持续测试。'),('可以连接现有 ERP、CRM 或工单系统吗？','可以，前提是系统有可用接口或可控的集成方式。会先评估 API、权限、频率和失败处理。'),('PoC 之后是否必须继续完整实施？','不必须。PoC 的目的就是帮助企业做继续、调整或停止的理性决定。')],
 [('service-data-governance.html','数据治理','为知识、指标和系统访问建立可信基础。'),('service-ai-enablement.html','企业 AI 赋能计划','让团队会使用、会评估、会持续改进。'),('service-ai-training.html','企业 AI 培训','在项目开始前建立共同语言和安全边界。')]
)

service_page(
 'service-ai-training','企业 AI 培训','Role-based AI Training','不讲一堆概念，围绕岗位、任务和数据边界，学完就能用、知道哪里不能用。','买了工具，不等于团队知道何时用、怎么用、哪里不能用。',
 [('管理层难判断','无法区分真实机会、短期热点和潜在风险，难以做投资优先级。'),('员工不敢或乱用','有人担心犯错完全不用，有人把敏感数据直接放进外部工具。'),('培训无法转化','通用课程与实际岗位脱节，课后没有任务、模板和跟进。')],
 [('管理层会判断','能用业务价值、成本、风险和准备度判断 AI 项目。'),('业务团队会实战','围绕文档、营销、客服、HR、分析等真实任务建立方法。'),('技术团队会落地','理解 RAG、Agent、评估、安全和集成的关键取舍。'),('企业形成共同规范','统一术语、数据边界、人工复核和问题升级机制。')],
 [('管理层工作坊','能力边界、商业价值、买或建、风险与投资组合。'),('业务实战课','按岗位设计提示词、工作流、审核和质量标准。'),('技术与数据课','RAG、Agent、评估、权限、集成与运行治理。'),('场景共创 Sprint','识别用例、验证技术与组织条件，形成可讨论 PoC。'),('企业使用规范','数据分类、外部工具、版权、事实核验和责任边界。'),('30 天陪跑','课后答疑、任务复盘、模板优化和 Champion 支持。')],
 [('课前访谈与问卷','了解角色、真实任务、工具、数据政策和学习目标。'),('课程与案例定制','把通用概念翻译成企业自己的流程、资料和案例。'),('分层培训与共创','管理层、业务和技术团队分别学习，再在共同场景上协作。'),('行动计划与资料包','输出模板、清单、规范和每个团队的 30 天行动。'),('可选实战陪跑','观察使用、答疑、复盘和优化，推动培训转化为结果。')],
 [('分层课程与讲义','面向管理层、业务团队和技术团队的不同版本。'),('岗位任务模板','提示词、输入要求、输出格式、核验和审批清单。'),('企业 AI 使用规范初稿','数据、版权、事实核验、敏感内容和责任边界。'),('场景优先级与行动计划','明确下一步试点、负责人、指标和需要补齐的条件。')],
 [('培训适合完全没用过 AI 的团队吗？','适合。会从基础概念和安全边界开始，并通过岗位任务逐步上手。'),('可以使用企业自己的资料做练习吗？','可以，但会先做数据分类。敏感资料应在批准环境中使用，或先脱敏、改写为练习样本。'),('管理层和员工要上同一门课吗？','不建议完全相同。管理层关注决策和风险，业务团队关注任务与质量，技术团队关注架构和运营。'),('培训结束如何避免“学完就忘”？','每个团队会形成真实任务模板、行动计划和负责人；可配 30 天陪跑与复盘。'),('能否只做半天工作坊？','可以，适合管理层共识或启动前对齐；但若希望改变日常工作，建议增加实战与跟进。'),('培训能直接产生 PoC 吗？','场景共创 Sprint 可形成小型 PoC 或技术验证；复杂生产项目需单独进入 Agent 搭建或数据治理路径。')],
 [('service-ai-enablement.html','企业 AI 赋能计划','在培训后把方法带入真实工作并衡量采用。'),('service-agent-build.html','企业 Agent 搭建','把共创场景做成可工作的流程。'),('playbook.html','企业 AI 实战手册','作为课前阅读和内部讨论材料。')]
)

category_body='''
<section class="category-hero"><div class="container category-hero-grid"><div data-reveal><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>解决方案分类</strong></nav><p class="eyebrow">Solution category</p><h1>人力资源与<br>组织效率</h1><p>把招聘、入职、员工服务、培训和绩效中的重复工作交给可治理的 AI 助手，让 HR 把时间放回人才和组织。</p><div class="category-stats"><span><b>6</b> 个优先场景</span><span><b>2–6 周</b> 起步周期</span><span><b>人工复核</b> 默认保留</span></div></div><div class="category-hero-card" data-reveal><span class="category-icon">HR</span><h2>HR AI 场景地图</h2><ul><li>招聘与候选人沟通</li><li>入职与制度问答</li><li>培训与能力发展</li><li>绩效与员工体验</li></ul></div></div></section>
<section class="category-main section-pad"><div class="container category-shell"><aside class="filter-panel" data-filter-panel><button class="filter-close" type="button" data-filter-close>关闭筛选 ×</button><h2>筛选场景</h2><div class="filter-group"><h3>实施方式</h3><label><input type="checkbox" value="buy" data-category-filter> 现成方案</label><label><input type="checkbox" value="build" data-category-filter> 定制建设</label><label><input type="checkbox" value="both" data-category-filter> 两者均可</label></div><div class="filter-group"><h3>主要价值</h3><label><input type="checkbox" value="speed" data-category-filter> 提高效率</label><label><input type="checkbox" value="experience" data-category-filter> 员工体验</label><label><input type="checkbox" value="quality" data-category-filter> 质量一致性</label><label><input type="checkbox" value="risk" data-category-filter> 降低风险</label></div><button class="btn btn--ghost btn--block" type="button" data-filter-clear>清除筛选</button></aside><div class="category-results"><div class="category-toolbar"><div><button class="btn btn--ghost filter-mobile-toggle" type="button" data-filter-open>筛选</button><span><b data-category-count>6</b> 个场景</span></div><select data-category-sort aria-label="排序"><option value="recommended">推荐排序</option><option value="speed">最快起步</option><option value="complexity">复杂度从低到高</option></select></div><div class="product-grid">
<article class="product-card" data-tags="buy both speed quality" data-speed="1" data-complexity="1"><div class="product-head"><span>招聘</span><b>01</b></div><h3>招聘筛选与沟通助手</h3><p>生成职位描述、整理简历、形成面试问题，并在人工确认后发送候选人沟通。</p><div class="micro-tags"><span>现成方案可起步</span><span>人工复核</span></div><ul><li>减少简历整理时间</li><li>统一候选人沟通口径</li><li>保留公平性检查</li></ul><a class="btn btn--green" href="service-ai-training.html">查看落地路径 →</a></article>
<article class="product-card" data-tags="build both speed experience" data-speed="2" data-complexity="2"><div class="product-head"><span>入职</span><b>02</b></div><h3>员工入职知识助手</h3><p>连接制度、福利、IT 指引和岗位资料，为新员工提供可引用、按权限展示的答案。</p><div class="micro-tags"><span>RAG</span><span>权限检索</span></div><ul><li>减少 HR 重复问答</li><li>提高新员工上手速度</li><li>资料更新可追踪</li></ul><a class="btn btn--green" href="service-agent-build.html">查看落地路径 →</a></article>
<article class="product-card" data-tags="build speed experience quality" data-speed="2" data-complexity="3"><div class="product-head"><span>员工服务</span><b>03</b></div><h3>员工服务 Agent</h3><p>处理高频问题、收集表单信息、创建工单并在必要时转交 HR 或 IT。</p><div class="micro-tags"><span>AI Agent</span><span>系统连接</span></div><ul><li>7×24 一致服务</li><li>自动分流与工单</li><li>可设置人工接管</li></ul><a class="btn btn--green" href="service-agent-build.html">查看落地路径 →</a></article>
<article class="product-card" data-tags="buy both experience quality" data-speed="1" data-complexity="1"><div class="product-head"><span>培训</span><b>04</b></div><h3>岗位培训与能力助手</h3><p>根据岗位、能力差距和企业资料生成学习路径、练习与反馈。</p><div class="micro-tags"><span>个性化学习</span><span>知识库</span></div><ul><li>缩短课程制作时间</li><li>按岗位提供练习</li><li>保留导师审核</li></ul><a class="btn btn--green" href="service-ai-training.html">查看落地路径 →</a></article>
<article class="product-card" data-tags="both quality risk" data-speed="3" data-complexity="2"><div class="product-head"><span>绩效</span><b>05</b></div><h3>绩效材料整理助手</h3><p>汇总目标、项目、反馈和证据，帮助经理形成结构化初稿，不替代最终判断。</p><div class="micro-tags"><span>辅助决策</span><span>证据引用</span></div><ul><li>减少材料整理</li><li>提醒信息缺口</li><li>避免自动做人才决定</li></ul><a class="btn btn--green" href="playbook.html#risk">查看风险说明 →</a></article>
<article class="product-card" data-tags="build quality risk speed" data-speed="4" data-complexity="4"><div class="product-head"><span>分析</span><b>06</b></div><h3>HR 数据分析助手</h3><p>连接人员、招聘、培训和离职数据，用自然语言生成趋势、图表和需关注问题。</p><div class="micro-tags"><span>数据治理</span><span>分析 Agent</span></div><ul><li>统一人力指标口径</li><li>快速形成管理摘要</li><li>敏感数据最小权限</li></ul><a class="btn btn--green" href="service-data-governance.html">查看落地路径 →</a></article>
</div></div></div></section>
<section class="category-guidance section-pad surface"><div class="container"><div class="section-head"><div><p class="eyebrow">Buy or build</p><h2 class="section-title">HR 场景买还是建？</h2></div></div><div class="guidance-grid"><article><h3>适合买</h3><p>职位描述、会议总结、通用课程制作等标准场景，可先用成熟工具，并明确数据政策。</p></article><article><h3>适合定制</h3><p>企业制度问答、员工服务 Agent、跨系统工单和敏感分析，需要接入企业数据、权限和流程。</p></article><article><h3>无论买还是建</h3><p>招聘、绩效和员工关系涉及公平、隐私和重大影响，必须保留人工判断、记录与申诉机制。</p></article></div></div></section>
<section class="section-pad"><div class="container faq-layout"><div><p class="eyebrow">FAQ</p><h2 class="section-title section-title--small">HR AI 常见问题</h2></div><div class="faq-list"><article class="faq-item"><button class="faq-question"><span>可以让 AI 自动淘汰候选人吗？</span><span class="plus">+</span></button><div class="faq-answer"><div><p>不建议让 AI 单独作出重大人才决定。AI 可辅助整理和提示，但筛选标准、公平性检查和最终决定应由授权人员负责。</p></div></div></article><article class="faq-item"><button class="faq-question"><span>员工资料能放进公共模型吗？</span><span class="plus">+</span></button><div class="faq-answer"><div><p>先按企业数据分类和供应商政策判断。敏感人员数据通常应在批准环境中使用，并遵循最小权限、脱敏和审计要求。</p></div></div></article><article class="faq-item"><button class="faq-question"><span>知识助手如何保持答案最新？</span><span class="plus">+</span></button><div class="faq-answer"><div><p>需要资料负责人、有效期、版本、更新流程和引用。模型不是制度来源，正式制度系统仍是权威来源。</p></div></div></article></div></div></section>
'''
(ROOT/'category-hrms.html').write_text(page('人力资源与组织效率场景','招聘、入职、员工服务、培训、绩效与 HR 分析的 AI 场景地图。','category-hrms',category_body,'category-page'),encoding='utf-8')

cases_body='''
<section class="cases-hero"><div class="container"><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>案例</strong></nav><p class="eyebrow">Case studies</p><h1>从业务问题到<br>可验证结果。</h1><p>案例页不只展示技术，而是回答为什么做、如何做、谁参与、怎样验证，以及下一步怎么扩展。</p><div class="case-filter-bar"><button class="is-active" data-case-filter="all">全部</button><button data-case-filter="retail">零售与制造</button><button data-case-filter="education">教育</button><button data-case-filter="service">客户服务</button><button data-case-filter="data">数据与运营</button></div></div></section>
<section class="section-pad"><div class="container case-library">
<a id="wren" class="case-library-card case-library-card--feature" data-case-tags="retail data" href="case-wren-kitchens.html"><div class="case-art case-art--wren"><span>WREN / PUBLIC REFERENCE</span></div><div><small>制造与零售 · 长期技术合作结构参考</small><h2>从紧急团队扩容，到跨物流、安装与内部系统的战略合作</h2><p>公开案例摘要：快速接管、嵌入内部团队、优化关键流程，并逐步扩展到多个业务模块。</p><span class="text-link">查看案例详情 →</span></div></a>
<div class="case-library-grid">
<article id="jan-elly" class="case-library-card" data-case-tags="education"><div class="case-art case-art--green"><b>18h</b><span>→ 30min</span></div><div><small>教育内容 · 公开 GenAI 案例</small><h3>把 18 小时博客工作压缩为 30 分钟</h3><p>从选题、写作到 SEO，建立可重复内容流程，并培训团队共同使用。</p></div></article>
<article class="case-library-card" data-case-tags="retail service"><div class="case-art case-art--dark"><b>-56%</b><span>重复任务时间</span></div><div><small>零售客服 · 公开 GenAI 案例</small><h3>用 7×24 智能客服提升响应和转化</h3><p>减少高频问答，让团队把时间转向复杂服务和销售机会。</p></div></article>
<article class="case-library-card" data-case-tags="education"><div class="case-art case-art--blue"><b>-80%</b><span>预计行政时间</span></div><div><small>教育运营 · 公开 GenAI 案例</small><h3>让教师把时间从行政工作还给学生</h3><p>建设符合教学法与学生进度的课程和活动规划助手。</p></div></article>
<article id="ihub" class="case-library-card" data-case-tags="data"><div class="case-art case-art--lines"><b>-50%</b><span>预计报表时间</span></div><div><small>物流数据 · 公开 GenAI 案例</small><h3>用自然语言查询多源供应链数据</h3><p>减少手工提取和整理，计划加入图表、摘要和多轮查询。</p></div></article>
<article class="case-library-card" data-case-tags="data service"><div class="case-art case-art--paper"><b>-95%</b><span>流程时间公开案例</span></div><div><small>文档流程 · TSH 公开案例引用</small><h3>文档审阅与投标 Agent</h3><p>通过 AI 应用减少大量人工文档处理，并保留质量控制。</p></div></article>
<article class="case-library-card" data-case-tags="service"><div class="case-art case-art--grid"><b>HR</b><span>知识与服务</span></div><div><small>概念案例 · 可替换</small><h3>员工制度与入职知识助手</h3><p>把分散制度转为按权限检索、带引用的员工服务入口。</p></div></article>
</div><p class="source-note">部分案例为用户提供的公开资料摘要或页面结构参考，不代表 ForFlow 已为相关企业提供服务。正式发布时请补充授权、来源与真实项目数据。</p></div></section>
<section class="case-method section-pad section-ink"><div class="container"><div class="section-head"><div><p class="eyebrow eyebrow--light">A useful case study</p><h2 class="section-title">一个可信案例，<br>至少回答五个问题。</h2></div></div><ol class="case-method-list"><li><span>01</span><p>原来的业务问题和基线是什么？</p></li><li><span>02</span><p>为什么选择这个场景和方法？</p></li><li><span>03</span><p>数据、系统、团队和风险如何处理？</p></li><li><span>04</span><p>用哪些指标证明效果？</p></li><li><span>05</span><p>下一步如何运营和扩展？</p></li></ol></div></section>
'''
(ROOT/'cases.html').write_text(page('企业 AI 案例中心','企业 AI、数据、Agent 和组织赋能案例结构与公开案例摘要。','cases',cases_body,'cases-page'),encoding='utf-8')

case_detail_body='''
<section class="case-detail-hero"><div class="container"><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="cases.html">案例</a><span>/</span><strong>Wren Kitchens</strong></nav><p class="eyebrow">Public case reference</p><h1>从紧急团队扩容，<br>走向长期技术合作。</h1><p>以下内容根据 TSH 公开案例重新组织为中文示范页面，用来展示 ForFlow 案例页应有的信息结构；不代表 ForFlow 参与该项目。</p><div class="case-detail-metrics"><div><strong>31</strong><span>公开资料中的合作团队规模</span></div><div><strong>1 分钟 → 约 5 秒</strong><span>关键产品浏览服务加载优化</span></div><div><strong>多业务模块</strong><span>安装、物流、产品、QA、移动应用</span></div></div><div class="case-detail-visual case-art--wren"><span>MANUFACTURING × RETAIL × SOFTWARE DELIVERY</span></div></div></section>
<div class="container case-detail-shell"><aside class="case-toc"><div class="case-toc-inner"><small>本页目录</small><nav data-scrollspy><a class="is-active" href="#challenge">业务挑战</a><a href="#takeover">快速接管</a><a href="#modules">合作模块</a><a href="#impact">公开影响</a><a href="#lessons">可复用经验</a></nav></div></aside><article>
<section id="challenge" data-section class="case-section"><p class="eyebrow">Challenge</p><h2>业务增长很快，但技术能力无法同速扩展。</h2><p>公开案例显示，Wren Kitchens 在结束上一家供应商合作后，需要快速补充开发能力，同时保持质量、可靠性和按期交付。当地专业人才有限，路线图又会随业务变化，因此企业不仅需要“人手”，还需要能接管知识、处理高风险工作并灵活扩缩的伙伴。</p><ul><li>需要立即补充大量 PHP 开发能力</li><li>短期与长期项目并存，团队规模需要灵活变化</li><li>未来几个季度的技术工作难以完全提前规划</li><li>关键业务要求稳定、准时且可持续交付</li></ul></section>
<section id="takeover" data-section class="case-section"><p class="eyebrow">Project takeover</p><h2>没有完整交接窗口，也要先稳住业务。</h2><p>新团队直接进入已有内部 IT 组织。由于客户拥有清晰文档和技术责任，新伙伴可以从第一天建立可靠知识基础。重点不是立即大改系统，而是确认责任、运行风险、关键流程和可快速改善的事项。</p><div class="case-quote"><blockquote>先建立稳定交付与信任，再逐步承担更复杂、更关键的业务模块。</blockquote><footer>案例页面结构总结</footer></div></section>
<section id="modules" data-section class="case-section"><p class="eyebrow">Workstreams</p><h2>合作扩展到安装、物流、产品、质量和移动应用。</h2><div class="case-modules"><article class="case-module"><h3>安装流程</h3><p>支持安装人员网络、测量、预约、日期和客户验收等完整生命周期。</p></article><article class="case-module"><h3>物流与交付</h3><p>优化影响夜间运行和标签准确性的关键流程，减少异常与处罚。</p></article><article class="case-module"><h3>产品与知识交接</h3><p>协助新内部开发人员理解领域知识、系统和责任边界。</p></article><article class="case-module"><h3>质量与移动应用</h3><p>完善上线前验证、QA 标准和 iPad 内部应用的稳定与持续交付。</p></article></div></section>
<section id="impact" data-section class="case-section"><p class="eyebrow">Impact</p><h2>公开案例报告了成本、稳定性和交付速度的共同改善。</h2><p>公开页面提到，团队先处理“容易见效”的数据库与服务问题，其中一个关键产品浏览服务从约 1 分钟缩短到约 5 秒；物流与标签流程也提高了准确性，减少了处罚并稳定关键夜间运行。</p><p>更重要的结果是合作模式从紧急扩容逐步转为长期、跨模块协作：外部团队不只是完成任务，还承担知识传递、风险工作和持续改进。</p></section>
<section id="lessons" data-section class="case-section"><p class="eyebrow">Lessons for enterprise AI</p><h2>这类案例对 AI 项目同样有三点启发。</h2><ol class="start-steps"><li><span>1</span><div><h3>先稳住关键流程</h3><p>AI 项目也应先理解现有责任、数据和失败成本，不要一开始大规模重构。</p></div></li><li><span>2</span><div><h3>从可验证改善建立信任</h3><p>选择能快速量化的时效、错误和质量问题，形成共同工作方式。</p></div></li><li><span>3</span><div><h3>把知识留在企业</h3><p>文档、评估、培训和内部负责人必须与技术交付同步。</p></div></li></ol></section>
</article></div>
<section class="final-cta"><div class="container final-cta-inner"><div><h2>把同样的案例结构，<br>用于你的项目。</h2><p>先写清问题、基线、流程、数据、风险与成功指标。</p></div><a class="btn" href="navigator.html">开始场景诊断 →</a></div></section>
'''
(ROOT/'case-wren-kitchens.html').write_text(page('案例详情：Wren Kitchens 公开案例结构参考','Wren Kitchens 与 TSH 公开合作案例的中文结构化摘要。','case-wren-kitchens',case_detail_body,'case-detail-page'),encoding='utf-8')

search_body=f'''
<section class="search-page-hero"><div class="container"><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>搜索</strong></nav><form class="search-page-form" action="search.html" method="get"><span>{SEARCH_ICON}</span><input data-search-page-input type="search" name="search" value="" placeholder="输入服务、场景或资料" aria-label="搜索关键词"><button class="btn btn--green" type="submit">搜索</button></form><div class="search-tabs"><button class="is-active" data-search-tab="all">全部 <span data-count-all>0</span></button><button data-search-tab="category">方案分类 <span data-count-category>0</span></button><button data-search-tab="service">企业服务 <span data-count-service>0</span></button><button data-search-tab="resource">资料 <span data-count-resource>0</span></button><button data-search-tab="case">案例 <span data-count-case>0</span></button></div></div></section>
<section class="search-results-page section-pad"><div class="container"><div class="search-result-group" data-result-type="category"><div class="search-result-head"><h2>方案分类 <span>1</span></h2><a href="category-hrms.html">查看全部 →</a></div><div class="search-category-card" data-search-text="人力资源 HR 招聘 入职 员工 Agent 培训"><span class="category-icon">HR</span><div><h3>人力资源与组织效率</h3><p>招聘、入职、员工服务、培训、绩效与 HR 数据分析场景。</p></div><a href="category-hrms.html">→</a></div></div>
<div class="search-result-group" data-result-type="service"><div class="search-result-head"><h2>企业服务 <span>4</span></h2><a href="index.html#services">查看全部 →</a></div><div class="search-result-grid"><a class="search-result-card" href="service-agent-build.html" data-search-text="企业 Agent 智能体 搭建 RAG 系统集成 自动化"><small>企业服务</small><h3>企业 Agent 搭建</h3><p>连接知识、系统和规则，完成多步业务任务。</p><span>2 周验证起步 →</span></a><a class="search-result-card" href="service-data-governance.html" data-search-text="数据治理 数据工程 RAG 知识库 指标 质量"><small>企业服务</small><h3>数据治理</h3><p>资产、口径、质量、管道、权限与 AI 数据层。</p><span>查看详情 →</span></a><a class="search-result-card" href="service-ai-enablement.html" data-search-text="AI 赋能 采用 组织 团队 绩效"><small>企业服务</small><h3>企业 AI 赋能计划</h3><p>把零散试用变成可衡量的团队能力。</p><span>查看详情 →</span></a><a class="search-result-card" href="service-ai-training.html" data-search-text="AI 培训 课程 管理层 业务 技术 提示词"><small>企业服务</small><h3>企业 AI 培训</h3><p>按角色和岗位定制，学完即用。</p><span>查看详情 →</span></a></div></div>
<div class="search-result-group" data-result-type="resource"><div class="search-result-head"><h2>资料 <span>2</span></h2><span>PDF / 在线手册</span></div><div class="document-result-grid"><a href="document-viewer.html?doc=playbook" data-search-text="GenAI 生成式 AI playbook 手册 RAG 风险 买还是建"><div class="doc-thumb doc-thumb--playbook"><img src="assets/forflow-lockup.png" alt="ForFlow 萬維流形"></div><div><span class="doc-type">PDF</span><h3>企业生成式 AI 实战手册</h3><p>GenAI、RAG、买还是建、风险治理和落地步骤。</p><small>参考 PDF · 支持在线查看与下载</small></div></a><a href="document-viewer.html?doc=solutions" data-search-text="方案 搜索 解决方案 SMEs digital"><div class="doc-thumb doc-thumb--solutions">{SEARCH_ICON}<b>Explore</b><span>digital solutions</span></div><div><span class="doc-type">PDF</span><h3>方案搜索结果参考页面</h3><p>用户提供的 SMEs Go Digital 搜索结果 PDF，用于布局与交互参考。</p><small>2 页 · 在线查看</small></div></a></div></div>
<div class="search-result-group" data-result-type="case"><div class="search-result-head"><h2>案例 <span>2</span></h2><a href="cases.html">查看全部 →</a></div><div class="search-result-grid"><a class="search-result-card" href="case-wren-kitchens.html" data-search-text="Wren 厨房 零售 制造 物流 技术合作"><small>案例结构参考</small><h3>大型零售：从紧急扩容到长期技术合作</h3><p>挑战、接管、模块、公开影响与可复用经验。</p><span>查看案例 →</span></a><a class="search-result-card" href="cases.html#ihub" data-search-text="物流 数据 Agent 自然语言 报表 iHub"><small>公开 GenAI 案例</small><h3>物流：自然语言数据 Agent</h3><p>用对话查询多源数据，减少人工报表处理。</p><span>查看案例 →</span></a></div></div>
<div class="search-empty" data-search-empty hidden><h2>没有找到完全匹配的内容。</h2><p>可以尝试“Agent”“数据治理”“培训”“HR”或“Playbook”。</p><a class="btn btn--green" href="navigator.html">改用场景诊断 →</a></div></div></section>
'''
(ROOT/'search.html').write_text(page('搜索','搜索 ForFlow 企业服务、场景、资料与案例。','',search_body,'search-page'),encoding='utf-8')

viewer_body='''
<section class="viewer-toolbar"><div class="container viewer-toolbar-inner"><div><a class="viewer-back" href="search.html">← 返回搜索</a><h1 data-doc-title>企业生成式 AI 实战手册</h1></div><div class="viewer-actions"><a class="btn btn--ghost" data-doc-open target="_blank" rel="noopener"><span>新窗口打开</span> ↗</a><a class="btn btn--green" data-doc-download download><span>下载 PDF</span> ↓</a></div></div></section>
<section class="viewer-main"><div class="container viewer-shell"><aside class="viewer-meta"><img src="assets/forflow-lockup.png" alt="ForFlow 萬維流形"><div><small>文档类型</small><strong>PDF 参考资料</strong></div><div><small>阅读说明</small><p>桌面端使用浏览器内置阅读器。手机浏览器若无法内嵌，可使用“新窗口打开”或“下载 PDF”。</p></div></aside><div class="pdf-frame"><iframe data-doc-frame title="PDF 阅读器" src="assets/genai-playbook-reference.pdf#view=FitH"></iframe><div class="pdf-fallback"><p>当前浏览器无法内嵌 PDF？</p><a class="btn btn--green" data-doc-open target="_blank" rel="noopener">打开文档 →</a></div></div></div></section>
'''
(ROOT/'document-viewer.html').write_text(page('PDF 阅读器','在线查看和下载企业 AI 参考 PDF。','document-viewer',viewer_body,'viewer-page'),encoding='utf-8')

# README
readme='''# ForFlow 萬維流形企业网站原型\n\n这是在已有 `index.html` 与 `navigator.html` 基础上继续扩展的静态响应式网站，不依赖前端框架。\n\n## 页面\n\n- `index.html`：主页（保留原有框架并加入四项企业服务）\n- `navigator.html`：3 分钟 AI 场景诊断\n- `navigator-results.html`：推荐结果、品牌视频控件与方案排序\n- `playbook.html`：中文企业生成式 AI 实战手册\n- `service-ai-enablement.html`：企业 AI 赋能计划\n- `service-data-governance.html`：数据治理\n- `service-agent-build.html`：企业 Agent 搭建\n- `service-ai-training.html`：企业 AI 培训\n- `category-hrms.html`：HR AI 场景分类页\n- `cases.html`：案例中心\n- `case-wren-kitchens.html`：案例详情结构示范\n- `search.html`：全站搜索结果页\n- `document-viewer.html`：PDF 在线阅读器\n\n## 运行\n\n```bash\npython -m http.server 8080\n```\n\n打开 `http://localhost:8080/`。\n\n## 说明\n\n- 使用用户提供的 ForFlow + 萬維流形完整标识，不使用黑色方形图标。\n- Navigator 结果页的动效视频由完整品牌标识制作，带原生视频控件。\n- 所有服务页包含服务流程、交付物、FAQ 与相关路径。\n- 搜索弹层、搜索结果、PDF 展示、筛选、排序、FAQ、移动菜单和目录均为前端可交互原型。\n- 案例中的公开企业资料仅作为结构参考，正式发布前需复核授权和最新数据。\n'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
print('site pages generated')

# Keep the hand-polished homepage and Playbook when the generator is rerun.
# Other pages continue to be generated by this script; these two are maintained
# as explicit templates so their richer editorial layout is not flattened.
from shutil import copyfile
for _name in ('index.html', 'playbook.html', 'README.md'):
    _template = ROOT / 'templates' / _name
    if _template.exists():
        copyfile(_template, ROOT / _name)
