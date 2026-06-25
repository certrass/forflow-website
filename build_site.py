# -*- coding: utf-8 -*-

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.python-deps'))

from bs4 import BeautifulSoup
import html
import json
import re

SEARCH_ICON = '''<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="m16.2 16.2 4.3 4.3"></path></svg>'''
ARROW = '<span class="arrow" aria-hidden="true">→</span>'
ASSET_VERSION = '20260625-case-quality-v9'
CSS_VERSION = ASSET_VERSION
SCRIPT_VERSION = ASSET_VERSION

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

CASE_LIBRARY_ITEMS = [
    {
        'id': 'wren',
        'featured': True,
        'href': 'case-wren-kitchens.html',
        'tags': ['retail', 'manufacturing', 'data'],
        'kicker': '制造与零售 · 公开技术合作参考',
        'title': 'Wren Kitchens：从紧急团队扩容，到长期技术合作',
        'description': '公开案例摘要：先稳住关键系统，再把安装、物流、产品、QA 和移动应用纳入长期协作。',
        'visual': {'type': 'art', 'class': 'case-art--wren', 'html': '<span>WREN / PUBLIC REFERENCE</span>'},
        'link_label': '查看案例详情 →',
        'search': True,
        'search_text': 'Wren 厨房 零售 制造 物流 技术合作 跨模块 软件交付 知识交接 长期合作',
        'search_kicker': '案例结构参考',
        'search_title': 'Wren Kitchens：从紧急扩容到长期技术合作',
        'search_description': '挑战、接管、模块、公开影响与可复用经验。',
    },
    {
        'id': 'jan-elly',
        'tags': ['education'],
        'kicker': '教育内容 · 公开 GenAI 案例',
        'title': '把 18 小时博客工作压缩为 30 分钟',
        'description': '从选题、写作到 SEO，建立可重复内容流程，并培训团队共同使用。',
        'visual': {'type': 'art', 'class': 'case-art--green', 'html': '<b>18h</b><span>→ 30min</span>'},
    },
    {
        'tags': ['retail', 'service'],
        'kicker': '零售客服 · 公开 GenAI 案例',
        'title': '用 7×24 智能客服提升响应和转化',
        'description': '减少高频问答，让团队把时间转向复杂服务和销售机会。',
        'visual': {'type': 'art', 'class': 'case-art--dark', 'html': '<b>-56%</b><span>重复任务时间</span>'},
    },
    {
        'tags': ['education'],
        'kicker': '教育运营 · 公开 GenAI 案例',
        'title': '让教师把时间从行政工作还给学生',
        'description': '建设符合教学法与学生进度的课程和活动规划助手。',
        'visual': {'type': 'art', 'class': 'case-art--blue', 'html': '<b>-80%</b><span>预计行政时间</span>'},
    },
    {
        'id': 'ihub',
        'tags': ['data'],
        'kicker': '物流数据 · 公开 GenAI 案例',
        'title': '用自然语言查询多源供应链数据',
        'description': '减少手工提取和整理，计划加入图表、摘要和多轮查询。',
        'visual': {'type': 'art', 'class': 'case-art--lines', 'html': '<b>-50%</b><span>预计报表时间</span>'},
        'search': True,
        'search_text': '物流 数据 Agent 自然语言 报表 iHub 供应链 多源数据',
        'search_kicker': '公开 GenAI 案例',
        'search_title': '物流：自然语言数据 Agent',
        'search_description': '用对话查询多源数据，减少人工报表处理。',
    },
    {
        'id': 'pid',
        'href': 'case-manufacturing-pid-intelligence.html',
        'tags': ['manufacturing', 'data'],
        'kicker': '工业知识资产化 · 案例 Blog 模板',
        'title': 'P&ID 智能化扩展工厂运营',
        'description': '把静态管线图纸变成可查询、可关联、可由工程师复核的运营知识网络。',
        'visual': {'type': 'media', 'src': 'assets/cases/thumb-manufacturing-pid.webp', 'label': '制造业'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '制造业 P&ID 工厂运营 工业知识资产化 工程师复核 图纸 查询 关联',
        'search_kicker': '案例 Blog 模板',
        'search_title': '制造业：P&ID 智能化扩展工厂运营',
    },
    {
        'id': 'healthcare-agent-roi',
        'href': 'case-healthcare-agent-roi.html',
        'tags': ['healthcare', 'service', 'data'],
        'kicker': '高合规医疗 · 受限多智能体',
        'title': '复杂医疗工作流中的智能体落地与 ROI 验证',
        'description': '把就诊前中后和患者语音入口拆成可验收、可追踪、可升级人工的生产级流程。',
        'visual': {'type': 'media', 'src': 'assets/cases/healthcare-care-chain-sana-plain.png', 'label': '医疗工作流'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '医疗 医院 诊所 AWS Amazon Connect Health 受限多智能体 ROI 患者语音 EHR EMR 保险验证 预约管理 HealthLake SFT GRPO 临床记录 医疗编码 CPT ICD 就诊前 就诊中 就诊后 状态机 人工升级',
        'search_kicker': '高合规医疗 · 受限多智能体',
        'search_title': '医疗：受限多智能体架构与 ROI 验证',
    },
    {
        'id': 'automotive-dfmea-ontology-agent',
        'href': 'case-automotive-dfmea-ontology-agent.html',
        'tags': ['automotive', 'manufacturing', 'data'],
        'kicker': '汽车工程 · 本体智能体 DFMEA',
        'title': '本体智能体如何重塑安全关键零部件 DFMEA',
        'description': '以 B 柱为例，把材料、工艺、失效机理和法规要求连成可推理、可追溯、可复评的风险情报系统。',
        'visual': {'type': 'media', 'src': 'assets/cases/automotive-dfmea-bpillar-hero.png', 'label': '汽车 DFMEA'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '汽车 汽车工程 B柱 B 柱 B-pillar 安全关键零部件 侧面碰撞 车顶抗压 安全带锚固 DFMEA FMEA 本体 Ontology 知识图谱 智能体 Agent AI RFLP AgentCore Strands SDK AWS Bedrock 22MnB5 硼钢 热冲压 氢脆 疲劳 腐蚀 电偶腐蚀 粘接失效 失效模式 RPN AP ECO 工程变更 工程推理 知识流失 老师傅经验 组织记忆 经验断档 机构记忆 跨项目迁移 供应商教训 设计变更复评 FMVSS 214 FMVSS 216 Euro NCAP IIHS AIAG VDA',
        'search_kicker': '汽车工程 · 本体智能体 DFMEA',
        'search_title': '汽车：本体智能体重塑 B 柱 DFMEA',
        'search_description': '从电子表格 DFMEA 到工程本体推理，解释 AI 如何发现组合失效并沉淀组织知识。',
    },
    {
        'id': 'supply-chain-agentic-decision',
        'href': 'case-supply-chain-agentic-decision.html',
        'tags': ['retail', 'data', 'service'],
        'kicker': '零售供应链 · 多智能体决策',
        'title': '多智能体 AI 如何将供应链数据转化为决策与行动',
        'description': '从控制塔的数据可见性，走向自然语言查询、异常钻取、根因归因和行动协同的完整决策链。',
        'visual': {'type': 'media', 'src': 'assets/cases/supply-chain-agentic-decision-hero.png', 'label': '供应链决策'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '供应链 零售 鞋服 库存 SKU 控制塔 control tower 多智能体 Agent AgentCore Strands MCP Gateway 语义层 自然语言 SQL 履行率 渠道履行 订单 冻结 信用控制 DynamoDB Cognito API Gateway Lambda Bedrock Observability 决策 行动',
        'search_kicker': '零售供应链 · 多智能体决策',
        'search_title': '供应链：多智能体 AI 把数据转化为行动',
        'search_description': '从数据可见性到自动查询、分析、根因归因和行动通知，解释供应链控制塔之后的 Agent 架构。',
    },
    {
        'tags': ['data', 'service'],
        'kicker': '文档流程 · TSH 公开案例引用',
        'title': '文档审阅与投标 Agent',
        'description': '通过 AI 应用减少大量人工文档处理，并保留质量控制。',
        'visual': {'type': 'art', 'class': 'case-art--paper', 'html': '<b>-95%</b><span>流程时间公开案例</span>'},
    },
    {
        'tags': ['service'],
        'kicker': '概念案例 · 可替换',
        'title': '员工制度与入职知识助手',
        'description': '把分散制度转为按权限检索、带引用的员工服务入口。',
        'visual': {'type': 'art', 'class': 'case-art--grid', 'html': '<b>HR</b><span>知识与服务</span>'},
    },
]

SEARCH_TYPE_LABELS = {
    'category': '方案分类',
    'service': '企业服务',
    'resource': '资料',
    'case': '案例',
}

SEARCH_CORE_ITEMS = [
    {
        'id': 'category-hrms',
        'type': 'category',
        'href': 'category-hrms.html',
        'kicker': '方案分类',
        'title': '人力资源与组织效率',
        'description': '招聘、入职、员工服务、培训、绩效与 HR 数据分析场景。',
        'action': '查看分类 →',
        'priority': 8,
        'keywords': ['人力资源', 'HR', '招聘', '入职', '员工', 'Agent', '培训', '绩效', '员工服务'],
    },
    {
        'id': 'service-agent-build',
        'type': 'service',
        'href': 'service-agent-build.html',
        'kicker': '企业服务',
        'title': '企业 Agent 搭建',
        'description': '连接知识、系统和规则，完成多步业务任务。',
        'action': '2 周验证起步 →',
        'priority': 8,
        'keywords': ['企业 Agent', '智能体', '搭建', 'RAG', '系统集成', '自动化', '工作流', '工具调用', '审批', '人工复核'],
    },
    {
        'id': 'service-data-governance',
        'type': 'service',
        'href': 'service-data-governance.html',
        'kicker': '企业服务',
        'title': '数据治理',
        'description': '资产、口径、质量、管道、权限与 AI 数据层。',
        'action': '查看详情 →',
        'priority': 7,
        'keywords': ['数据治理', '数据工程', 'RAG', '知识库', '指标', '质量', '权限', '口径', '数据资产'],
    },
    {
        'id': 'service-ai-enablement',
        'type': 'service',
        'href': 'service-ai-enablement.html',
        'kicker': '企业服务',
        'title': '企业 AI 赋能计划',
        'description': '把零散试用变成可衡量的团队能力。',
        'action': '查看详情 →',
        'priority': 6,
        'keywords': ['AI 赋能', '采用', '组织', '团队', '绩效', '场景诊断', 'Q2Q', '试点', '扩展'],
    },
    {
        'id': 'service-ai-training',
        'type': 'service',
        'href': 'service-ai-training.html',
        'kicker': '企业服务',
        'title': '企业 AI 培训',
        'description': '按角色和岗位定制，学完即用。',
        'action': '查看详情 →',
        'priority': 6,
        'keywords': ['AI 培训', '课程', '管理层', '业务', '技术', '提示词', '工作坊', '角色训练'],
    },
    {
        'id': 'resource-playbook',
        'type': 'resource',
        'href': 'document-viewer.html?doc=playbook',
        'kicker': 'PDF',
        'title': '企业生成式 AI 实战手册',
        'description': 'GenAI、RAG、买还是建、风险治理和落地步骤。',
        'action': '在线查看 →',
        'priority': 6,
        'keywords': ['GenAI', '生成式 AI', 'playbook', '手册', 'RAG', '风险', '买还是建'],
    },
    {
        'id': 'resource-solutions',
        'type': 'resource',
        'href': 'document-viewer.html?doc=solutions',
        'kicker': 'PDF',
        'title': '方案搜索结果参考页面',
        'description': '用户提供的 SMEs Go Digital 搜索结果 PDF，用于布局与交互参考。',
        'action': '在线查看 →',
        'priority': 4,
        'keywords': ['方案', '搜索', '解决方案', 'SMEs', 'digital'],
    },
]

SERVICE_KEYS = {href.removesuffix('.html') for href, _ in SERVICE_LINKS}
TOOLS_KEYS = {'navigator', 'navigator-results', 'category-hrms'}
INSIGHT_KEYS = {'playbook', 'document-viewer'}
CASE_KEYS = {'cases'} | {
    item['href'].split('#')[0].removesuffix('.html')
    for item in CASE_LIBRARY_ITEMS
    if item.get('href', '').startswith('case-')
}

def current_attr(condition):
    return ' aria-current="page"' if condition else ''

def current_class(condition):
    return ' is-current' if condition else ''

def ff_icon(name):
    return f'<svg class="ff-icon" aria-hidden="true"><use href="#{name}"></use></svg>'

def esc(value):
    return html.escape(str(value), quote=True)

def render_case_visual(item):
    visual = item['visual']
    if visual['type'] == 'media':
        return (
            '<div class="case-card-media">'
            f'<img src="{esc(visual["src"])}" alt="" decoding="async" loading="lazy">'
            f'<span>{esc(visual["label"])}</span>'
            '</div>'
        )
    return f'<div class="case-art {esc(visual["class"])}">{visual["html"]}</div>'

def render_case_library_card(item):
    id_attr = f' id="{esc(item["id"])}"' if item.get('id') else ''
    tags_attr = esc(' '.join(item['tags']))
    visual_html = render_case_visual(item)
    title_tag = 'h2' if item.get('featured') else 'h3'
    link_html = f'<span class="{"text-link" if item.get("featured") else "case-card-link"}">{item.get("link_label", "查看案例 →")}</span>' if item.get('href') else ''
    body_html = (
        f'<div><small>{esc(item["kicker"])}</small>'
        f'<{title_tag}>{esc(item["title"])}</{title_tag}>'
        f'<p>{esc(item["description"])}</p>'
        f'{link_html}</div>'
    )
    if item.get('href'):
        modifier = 'case-library-card--feature' if item.get('featured') else 'case-library-card--linked'
        return (
            f'<a{id_attr} class="case-library-card {modifier}" data-case-tags="{tags_attr}" '
            f'href="{esc(item["href"])}">{visual_html}{body_html}</a>'
        )
    return f'<article{id_attr} class="case-library-card" data-case-tags="{tags_attr}">{visual_html}{body_html}</article>'

def render_case_library(featured=False):
    return '\n'.join(
        render_case_library_card(item)
        for item in CASE_LIBRARY_ITEMS
        if bool(item.get('featured')) is featured
    )

def case_target(item):
    if item.get('href'):
        return item['href']
    if item.get('id'):
        return f'cases.html#{item["id"]}'
    return 'cases.html'

def search_case_entries():
    entries = []
    for item in CASE_LIBRARY_ITEMS:
        if not item.get('search'):
            continue
        entries.append({
            'id': item.get('id') or re.sub(r'[^a-z0-9]+', '-', case_target(item).lower()).strip('-'),
            'type': 'case',
            'href': case_target(item),
            'kicker': item.get('search_kicker', item['kicker']),
            'title': item.get('search_title', item['title']),
            'description': item.get('search_description', item['description']),
            'action': '查看案例 →',
            'priority': 10,
            'keywords': [
                item.get('search_text', item['title']),
                item['title'],
                item['description'],
                ' '.join(item.get('tags', [])),
            ],
        })
    return entries

def search_index_items():
    return SEARCH_CORE_ITEMS + search_case_entries()

def render_search_card(entry):
    keywords = entry.get('keywords', [])
    if isinstance(keywords, str):
        keywords_text = keywords
    else:
        keywords_text = ' '.join(str(item) for item in keywords)
    return (
        f'<a class="search-result-card" href="{esc(entry["href"])}" '
        f'data-search-id="{esc(entry.get("id", ""))}" '
        f'data-search-text="{esc(keywords_text)}" '
        f'data-search-priority="{esc(str(entry.get("priority", 0)))}">'
        f'<small>{esc(entry.get("kicker", SEARCH_TYPE_LABELS.get(entry["type"], entry["type"])))}</small>'
        f'<h3>{esc(entry["title"])}</h3>'
        f'<p>{esc(entry["description"])}</p>'
        f'<span>{esc(entry.get("action", "查看 →"))}</span></a>'
    )

def render_search_cards(result_type):
    return '\n'.join(
        render_search_card(entry)
        for entry in search_index_items()
        if entry.get('type') == result_type
    )

def search_type_count(result_type):
    return sum(1 for entry in search_index_items() if entry.get('type') == result_type)

def write_search_index():
    payload = {
        'version': ASSET_VERSION,
        'types': [
            {'type': key, 'label': label}
            for key, label in SEARCH_TYPE_LABELS.items()
        ],
        'items': search_index_items(),
    }
    (ROOT / 'search-index.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

def render_search_case_cards():
    return render_search_cards('case')

def search_case_count():
    return search_type_count('case')

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
              <a href="case-wren-kitchens.html"><span>{ff_icon('i-growth')}</span><div><b>Wren Kitchens 案例</b><small>从紧急扩容到长期技术合作</small></div></a>
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
      <a href="case-wren-kitchens.html">Wren Kitchens 案例</a>
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
    <div class="search-suggestions"><span>常用搜索</span><a href="search.html?search=Agent">企业 Agent</a><a href="search.html?search=供应链">供应链</a><a href="search.html?search=DFMEA">DFMEA</a><a href="search.html?search=医疗">医疗智能体</a><a href="search.html?search=数据治理">数据治理</a><a href="search.html?search=Playbook">企业 AI 手册</a></div>
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
  <link rel="stylesheet" href="styles.css?v={CSS_VERSION}">
  <script src="script.js?v={SCRIPT_VERSION}" defer></script>
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
    for sheet in soup.find_all('link', rel=lambda x: x and 'stylesheet' in x):
        href = sheet.get('href', '')
        if href.split('?')[0] == 'styles.css':
            sheet['href'] = f'styles.css?v={CSS_VERSION}'
    for script in soup.find_all('script', src=True):
        src = script.get('src', '')
        if src.split('?')[0] == 'script.js':
            script['src'] = f'script.js?v={SCRIPT_VERSION}'
    path.write_text(str(soup), encoding='utf-8')

def version_asset_links():
    for path in ROOT.glob('*.html'):
        soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
        changed = False
        for sheet in soup.find_all('link', rel=lambda x: x and 'stylesheet' in x):
            href = sheet.get('href', '')
            if href.split('?')[0] == 'styles.css':
                sheet['href'] = f'styles.css?v={CSS_VERSION}'
                changed = True
        for script in soup.find_all('script', src=True):
            src = script.get('src', '')
            if src.split('?')[0] == 'script.js':
                script['src'] = f'script.js?v={SCRIPT_VERSION}'
                changed = True
        if changed:
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

cases_body=f'''
<section class="cases-hero"><div class="container"><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>案例</strong></nav><p class="eyebrow">Case studies</p><h1>从业务问题到<br>可验证结果。</h1><p>案例页不只展示技术，而是回答为什么做、如何做、谁参与、怎样验证，以及下一步怎么扩展。</p><div class="case-filter-bar"><button class="is-active" data-case-filter="all">全部</button><button data-case-filter="manufacturing">工业与制造</button><button data-case-filter="healthcare">医疗与高合规</button><button data-case-filter="service">客户服务</button><button data-case-filter="education">教育</button><button data-case-filter="data">数据与运营</button></div></div></section>
<section class="section-pad"><div class="container case-library">
{render_case_library(featured=True)}
<div class="case-library-grid">
{render_case_library(featured=False)}
</div><p class="source-note">案例中心持续收录可拆解、可复用、可验证的企业 AI 落地样板，帮助团队把标杆实践转化为自己的场景诊断与交付路径。</p></div></section>
<section class="case-method section-pad section-ink"><div class="container"><div class="section-head"><div><p class="eyebrow eyebrow--light">A useful case study</p><h2 class="section-title">一个可信案例，<br>至少回答五个问题。</h2></div></div><ol class="case-method-list"><li><span>01</span><p>原来的业务问题和基线是什么？</p></li><li><span>02</span><p>为什么选择这个场景和方法？</p></li><li><span>03</span><p>数据、系统、团队和风险如何处理？</p></li><li><span>04</span><p>用哪些指标证明效果？</p></li><li><span>05</span><p>下一步如何运营和扩展？</p></li></ol></div></section>
'''
(ROOT/'cases.html').write_text(page('企业 AI 案例中心','企业 AI、数据、Agent 和组织赋能案例结构与公开案例摘要。','cases',cases_body,'cases-page'),encoding='utf-8')

case_detail_body='''
<section class="case-detail-hero"><div class="container"><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="cases.html">案例</a><span>/</span><strong>Wren Kitchens</strong></nav><p class="eyebrow">Public case reference</p><h1>Wren Kitchens：<br>从紧急团队扩容到长期技术合作。</h1><p>这是一篇公开案例的结构化解读，用来说明企业在高速增长、系统复杂和内部团队承压时，如何先稳住关键流程，再把外部技术能力沉淀为长期协作能力。</p><div class="case-detail-metrics"><div><strong>31</strong><span>公开资料中的合作团队规模</span></div><div><strong>1 分钟 → 约 5 秒</strong><span>关键产品浏览服务加载优化</span></div><div><strong>多业务模块</strong><span>安装、物流、产品、QA、移动应用</span></div></div><div class="case-detail-visual case-art--wren"><span>MANUFACTURING × RETAIL × SOFTWARE DELIVERY</span></div></div></section>
<div class="container case-detail-shell"><aside class="case-toc"><div class="case-toc-inner"><small>本页目录</small><nav data-scrollspy><a class="is-active" href="#challenge">业务挑战</a><a href="#takeover">快速接管</a><a href="#modules">合作模块</a><a href="#impact">公开影响</a><a href="#lessons">可复用经验</a></nav></div></aside><article>
<section id="challenge" data-section class="case-section"><p class="eyebrow">Challenge</p><h2>增长很快的企业，最怕系统能力追不上业务节奏。</h2><p>公开案例显示，Wren Kitchens 在结束上一家供应商合作后，需要快速补充开发能力，同时保持质量、可靠性和按期交付。当地专业人才有限，路线图又会随业务变化，因此企业不仅需要“人手”，还需要能接管知识、处理高风险工作并灵活扩缩的伙伴。</p><ul><li>需要立即补充大量 PHP 开发能力</li><li>短期与长期项目并存，团队规模需要灵活变化</li><li>未来几个季度的技术工作难以完全提前规划</li><li>关键业务要求稳定、准时且可持续交付</li></ul></section>
<section id="takeover" data-section class="case-section"><p class="eyebrow">Project takeover</p><h2>没有完整交接窗口，也要先稳住业务，再谈优化。</h2><p>新团队直接进入已有内部 IT 组织。由于客户拥有清晰文档和技术责任，新伙伴可以从第一天建立可靠知识基础。重点不是立即大改系统，而是确认责任、运行风险、关键流程和可快速改善的事项。</p><div class="case-quote"><blockquote>先建立稳定交付与信任，再逐步承担更复杂、更关键的业务模块。</blockquote><footer>案例页面结构总结</footer></div></section>
<section id="modules" data-section class="case-section"><p class="eyebrow">Workstreams</p><h2>合作扩展到安装、物流、产品、质量和移动应用。</h2><div class="case-modules"><article class="case-module"><h3>安装流程</h3><p>支持安装人员网络、测量、预约、日期和客户验收等完整生命周期。</p></article><article class="case-module"><h3>物流与交付</h3><p>优化影响夜间运行和标签准确性的关键流程，减少异常与处罚。</p></article><article class="case-module"><h3>产品与知识交接</h3><p>协助新内部开发人员理解领域知识、系统和责任边界。</p></article><article class="case-module"><h3>质量与移动应用</h3><p>完善上线前验证、QA 标准和 iPad 内部应用的稳定与持续交付。</p></article></div></section>
<section id="impact" data-section class="case-section"><p class="eyebrow">Impact</p><h2>公开案例报告了成本、稳定性和交付速度的共同改善。</h2><p>公开页面提到，团队先处理“容易见效”的数据库与服务问题，其中一个关键产品浏览服务从约 1 分钟缩短到约 5 秒；物流与标签流程也提高了准确性，减少了处罚并稳定关键夜间运行。</p><p>更重要的结果是合作模式从紧急扩容逐步转为长期、跨模块协作：外部团队不只是完成任务，还承担知识传递、风险工作和持续改进。</p></section>
<section id="lessons" data-section class="case-section"><p class="eyebrow">Lessons for enterprise AI</p><h2>这类案例对 AI 项目同样有三点启发。</h2><ol class="start-steps"><li><span>1</span><div><h3>先稳住关键流程</h3><p>AI 项目也应先理解现有责任、数据和失败成本，不要一开始大规模重构。</p></div></li><li><span>2</span><div><h3>从可验证改善建立信任</h3><p>选择能快速量化的时效、错误和质量问题，形成共同工作方式。</p></div></li><li><span>3</span><div><h3>把知识留在企业</h3><p>文档、评估、培训和内部负责人必须与技术交付同步。</p></div></li></ol></section>
</article></div>
<section class="final-cta"><div class="container final-cta-inner"><div><h2>把同样的案例结构，<br>用于你的项目。</h2><p>先写清问题、基线、流程、数据、风险与成功指标。</p></div><a class="btn" href="navigator.html">开始场景诊断 →</a></div></section>
'''
(ROOT/'case-wren-kitchens.html').write_text(page('Wren Kitchens：从紧急团队扩容到长期技术合作','Wren Kitchens 公开合作案例的中文结构化摘要。','case-wren-kitchens',case_detail_body,'case-detail-page case-study-v2 case-study-legacy'),encoding='utf-8')

automotive_dfmea_body='''
<section class="case-study-hero">
  <div class="container">
    <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="cases.html">案例中心</a><span>/</span><strong>汽车工程与安全关键零部件</strong></nav>
    <div class="case-study-hero__grid">
      <div class="case-study-hero__copy">
        <div class="case-study-meta"><span>案例 Blog · 上篇</span><span>汽车安全关键件</span><span>B 柱 DFMEA</span><span>知识流失治理</span></div>
        <h1>基于本体的智能体 AI 如何重塑安全关键型汽车零部件的 DFMEA</h1>
        <p class="case-study-lead">对制造业老板来说，真正可怕的不是开不出 DFMEA 会，而是几位资深工程师一退休、一次供应商换线、一张 ECO 改完设计，为什么某个焊点不能改、某个批次曾经出过什么问题、哪些风险必须重新验证，没人能完整说清。B 柱只是一个放大镜：它把安全责任、工程知识流失和组织记忆断层同时摆到台面上。</p>
        <div class="case-study-actions"><a class="btn btn--green" href="#overview">先看核心问题 <span aria-hidden="true">↓</span></a><a class="btn btn--ghost" href="#ontology">查看本体逻辑 <span aria-hidden="true">↘</span></a></div>
      </div>
      <figure class="case-study-hero__media case-study-hero__media--scene">
        <img alt="汽车 B 柱结构件与工程风险网络场景图" decoding="async" fetchpriority="high" loading="eager" src="assets/cases/automotive-dfmea-bpillar-hero.png">
        <figcaption>B 柱 DFMEA 的难点不在“列一张表”，而在材料、工艺、界面、载荷和法规要求同时交汇。</figcaption>
      </figure>
    </div>
    <div aria-label="本案例的风险与交付证据结构" class="case-proof-rail"><div><strong>老师傅经验</strong><span>失效案例、工艺窗口和供应商批次不能只留在个人记忆里</span></div><div><strong>ECO 复评</strong><span>设计变更后，哪些 DFMEA 条目失效、哪些仍有效，需要自动回到台面</span></div><div><strong>跨项目迁移</strong><span>旧车型、C 柱、焊接接头和保修索赔教训要能进入新平台</span></div><div><strong>RFLP</strong><span>需求、功能、逻辑、物理四层追溯，让风险能被解释和审计</span></div></div>
    <p class="case-proof-note">本文是上篇，先回答制造业老板最该追问的三个问题：经验怎样不随人流失，设计变更怎样触发复评，AI 怎样从“填表工具”变成能保留组织工程判断的风险系统。下篇再展开 AgentCore、Strands SDK、多智能体编排、本体读写和 B 柱逐步演练。</p>
  </div>
</section>
<div class="container case-detail-shell case-story-shell">
  <aside class="case-toc"><div class="case-toc-inner"><small>本页目录 · 上篇</small><nav data-scrollspy><a class="is-active" href="#overview">引言</a><a href="#bpillar">B 柱关键性</a><a href="#dfmea-gap">DFMEA 困境</a><a href="#industry-pressure">行业压力</a><a href="#ontology">本体突破</a><a href="#rflp">RFLP 与事件</a><a href="#agent-system">七维重塑</a><a href="#manager-actions">管理者布局</a><a href="#references">公开依据</a><a href="#next">下篇预告</a></nav><a class="case-toc-source" href="#case-source">案例价值 ↘</a></div></aside>
  <article>
    <section class="case-section case-overview" data-section id="overview">
      <p class="eyebrow">Introduction</p>
      <h2>DFMEA 的价值，不是把风险写进表格，而是把工程经验留在企业里。</h2>
      <p>设计失效模式及影响分析 DFMEA，是工程领域防止设计缺陷演变为灾难性现场故障的最后一道防线。对于安全关键部件而言，一个被忽略的失效模式，其代价不只是保修索赔；它可能直接决定车内乘员在事故中能否生还。对制造企业来说，它也决定了组织能不能把一次次试验、事故、返工和供应商问题沉淀成下一代产品能继承的判断力。</p>
      <p>本篇文章讨论的不是“让大模型帮工程师填表”。那条路最多得到一个更快的电子表格助手。真正值得关注的是：企业能否把多年积累的材料知识、工艺窗口、试验记录、保修索赔和工程师判断，转化为机器可读、可推理、可审计、可随设计变化持续更新的工程本体。</p>
      <div class="case-reading-note"><strong>给制造业老板的读法</strong><p>你不需要先懂所有材料学细节，只需要抓住一条主线：B 柱失效不是单点问题，而是“需求、功能、结构、材料、工艺、环境、历史经验”之间的因果链问题。AI 的价值，不是替代工程师拍板，而是让这条因果链不再散落在会议、表格、微信群、供应商邮件和个人记忆里。</p></div>
      <div class="case-question-panel">
        <div><small>本篇核心问题</small><h3>AI 如何从“自动补全 DFMEA 表格”，升级为可追踪的工程推理系统？</h3></div>
        <div class="case-goal"><small>企业主视角</small><p>真正的投资对象不是某个模型，而是一套能把资深工程师经验、供应商教训、质量索赔和设计变更长期沉淀下来，并能触发复评、支撑试验证据的工程风险系统。</p></div>
      </div>
      <div class="case-fact-grid">
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-shield"></use></svg></span><div><small>安全对象</small><strong>B 柱：侧碰防护、车顶抗压、安全带锚固</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-data"></use></svg></span><div><small>知识问题</small><strong>老师傅经验、电子表格和历史项目孤岛</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-brain"></use></svg></span><div><small>AI 关键</small><strong>本体上下文 + 专项智能体 + 可审计推理</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-reference"></use></svg></span><div><small>业务结果</small><strong>更少遗漏、更快复评、更稳地保留工程经验</strong></div></div>
      </div>
    </section>

    <section class="case-section" data-section id="bpillar">
      <p class="eyebrow">B-pillar in 60 seconds</p>
      <h2>B 柱：乘客几乎看不见，却承担三项生命安全功能。</h2>
      <p>B 柱，是车辆前后车门之间的垂直结构立柱。它不像发动机、电池包或智能座舱那样醒目，但在车身安全结构里，它承担着极高的风险密度。</p>
      <div class="case-value-cards"><article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-shield"></use></svg></span><small>侧面碰撞防护</small><h3>乘员舱第一道屏障</h3><p>在侧面碰撞中，B 柱必须吸收并耗散动能，同时控制乘员舱侵入。FMVSS 214 的动态侧碰测试和相关 NCAP 体系，都把车身侧部结构能力推到工程验证前台。</p></article><article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-risk"></use></svg></span><small>车顶抗压强度</small><h3>翻滚事故中的生存空间</h3><p>车辆翻滚时，B 柱与车顶纵梁、门槛梁共同决定车顶结构是否能维持生存空间。IIHS 屋顶强度测试会以峰值强度重量比等指标评估结构能力。</p></article><article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-security"></use></svg></span><small>安全带锚固点</small><h3>急剧减速下的载荷锚点</h3><p>B 柱上部常集成肩部安全带锚固点。车辆急剧减速时，它要承受高瞬时载荷，任何局部开裂、连接失效或锚固板变形都可能放大乘员伤害。</p></article><article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-layers"></use></svg></span><small>多材料结构</small><h3>强度与轻量化并存</h3><p>现代 B 柱常使用热冲压硼钢 22MnB5、先进高强钢、软区设计、激光拼焊板和局部加强结构。材料越先进，界面和工艺带来的组合失效越不能靠记忆补漏。</p></article></div>
      <p>以 22MnB5 为例，热冲压后形成的超高强马氏体组织，可以支持车身减重与碰撞性能提升。但它也带来新的工程问题：热影响区性能变化、涂层缺陷、氢脆敏感性、焊接残余应力、局部冷却速率差异、腐蚀和疲劳交互。</p>
      <aside class="case-callout"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-bulb"></use></svg></span><div><small>读者要抓住的重点</small><h3>B 柱不是一个零件清单，而是一个高耦合工程系统。</h3><p>传统会议可能把问题写成“焊缝失效”四个字。本体系统必须继续追问：哪种材料？哪道工艺？哪个热影响区？什么载荷谱？什么环境暴露？违反哪项安全需求？下一步用什么证据验证？</p></div></aside>
    </section>

    <section class="case-section" data-section id="dfmea-gap">
      <p class="eyebrow">Why classic DFMEA breaks</p>
      <h2>传统 DFMEA 的困境，不是工程师不专业，而是流程已经扛不住复杂度。</h2>
      <p>DFMEA 对设计中的每个要素提出三个看似简单的问题：哪些地方可能出问题？出问题会带来什么后果？如何发现这些问题？最终输出的 RPN 或行动优先级，会影响后续工程决策、试验计划和供应商控制。</p>
      <p>对 B 柱而言，这些问题会迅速膨胀为数百种失效模式，横跨多材料界面、多种载荷工况，以及材料、工艺和环境之间的交互关系。全面分析是唯一负责任的选择，但用传统方法做到真正全面，已经越来越接近不可能。</p>
      <div class="case-decision-grid"><article class="case-decision-card"><small>问题一</small><h3>耗时惊人</h3><p>完整 B 柱 DFMEA 往往需要数周跨部门研讨。工程师需要把设计、仿真、制造、质量、试验、售后经验同时拉到桌面上。</p></article><article class="case-decision-card"><small>问题二</small><h3>知识正在流失</h3><p>资深工程师退休或转岗，电动化又要求团队快速掌握新材料、新平台和新工艺。某个焊接接头为什么当年不能这么改，如果只存在于人的记忆里，它会随人离开。</p></article><article class="case-decision-card"><small>问题三</small><h3>评分不一致</h3><p>不同团队对严重度、发生率、探测度或行动优先级的理解不一致，RPN/AP 就失去横向可比性，优先级排序也会被稀释。</p></article><article class="case-decision-card"><small>问题四</small><h3>文档随时过期</h3><p>ECO 一旦修改设计，静态表格很可能滞后于真实设计状态，在“记录中的风险”和“实际产品状态”之间留下危险鸿沟。</p></article></div>
      <div class="case-reading-note"><strong>换成企业语言</strong><p>DFMEA 的慢，不只是会议慢；它慢在每次都要重新召回知识。DFMEA 的不准，也不只是评分不准；它不准在组织没有一套持续更新的风险知识底座。老板真正要防的是：换人后经验断档，换供应商后风险重来，换平台后过去交过的学费又交一遍。</p></div>
    </section>

    <section class="case-section" data-section id="industry-pressure">
      <p class="eyebrow">Why now</p>
      <h2>行业压力让这个问题更紧迫：复杂性上升，周期压缩，人才断层，监管演进。</h2>
      <div class="case-fit-grid"><article class="case-fit-card case-fit-card--yes"><small>复杂性激增</small><h3>多材料 B 柱引入十年前少见的失效机制</h3><ul><li>定制坯料、热冲压分区、软区和激光拼焊板</li><li>钢/复合材料或不同钢种之间的界面风险</li><li>分层开裂、电偶腐蚀、粘接失效、涂层缺陷</li><li>材料、工艺、环境和载荷同时作用的组合失效</li></ul></article><article class="case-fit-card case-fit-card--yes"><small>开发周期压缩</small><h3>安全关键件不能无限依赖 3 到 4 周研讨会</h3><ul><li>EV 平台开发节奏普遍压缩</li><li>每个关键部件都用传统深度会议难以扩展</li><li>法规和评级测试规程持续变化</li><li>设计变更要求风险分析能快速复评</li></ul></article><article class="case-fit-card case-fit-card--yes"><small>知识断层</small><h3>老师傅的判断必须变成企业资产</h3><ul><li>资深工程师的隐性判断需要沉淀</li><li>新工程师需要可追溯案例，不只是历史表格</li><li>跨平台、跨项目经验需要自动迁移</li><li>供应商和内部团队需要统一语义与责任边界</li></ul></article><article class="case-fit-card case-fit-card--yes"><small>失效代价</small><h3>越晚发现，成本越指数级上升</h3><ul><li>设计阶段修复是工程代价</li><li>生产阶段修复是供应链和质量代价</li><li>上市后修复可能变成召回和品牌代价</li><li>安全关键件还叠加法律和声誉风险</li></ul></article></div>
    </section>

    <section class="case-section" data-section id="ontology">
      <p class="eyebrow">Ontology as reasoning context</p>
      <h2>“电子表格 AI”为什么必然失败？因为它继承的是历史记录，不是工程因果。</h2>
      <p>很多 AI 辅助 DFMEA 的直觉方案，是把历史 DFMEA 电子表格喂给大语言模型，期待它生成新的失效模式。这条路最多得到一个自动补全引擎。它能复述历史上常见的词，但无法真正判断新的材料、工艺、界面和载荷组合会带来什么风险。</p>
      <div class="case-decision-grid"><article class="case-decision-card"><small>失败原因一</small><h3>继承知识盲区</h3><p>如果历史 DFMEA 本来就遗漏了某类失效模式，模型会把这个遗漏当作正常分布继承下来。未被记录的失效，无法从表格里学到。</p></article><article class="case-decision-card"><small>失败原因二</small><h3>缺乏因果理解</h3><p>模型可能写出“焊接失效”，却分不清是阴极浸涂后的氢脆、焊趾疲劳裂纹，还是激光焊接参数漂移导致熔合不足。</p></article><article class="case-decision-card"><small>失败原因三</small><h3>无法推断组合失效</h3><p>最危险的失效模式往往来自多个因素交互，而这些因素可能从未在历史项目中同时出现过。</p></article></div>
      <div class="case-subhead"><small>本体编码的是关系</small><h3>材料 → 工艺 → 失效机理 → 影响效应。</h3></div>
      <p>工程本体的作用，是把知识从“事实列表”变成“关系网络”。当本体知道 22MnB5 硼钢经过约 900°C 奥氏体化热冲压，随后进入涂装、焊接和服役环境，它就能把热影响区、涂层状态、氢敏感性、残余应力、腐蚀暴露和疲劳载荷连到同一条推理路径上。</p>
      <div class="case-board-questions"><div><small>AI 推理上下文</small><h3>本体给智能体的不是答案，而是工程背景。</h3><p>当专项 AI 代理被要求识别 B 柱车顶纵梁焊缝的失效模式时，本体提供五类上下文，让 AI 可以沿因果链判断，而不是在历史表格里做关键词联想。</p></div><ol><li><span>01</span><p>材料上下文：22MnB5、奥氏体化、淬火、热影响区、强度梯度、氢敏感性曲线。</p></li><li><span>02</span><p>工艺上下文：激光焊接、焊点几何、热输入、残余应力、涂层连续性和熔合质量。</p></li><li><span>03</span><p>环境上下文：道路盐分、水分循环、底盘暴露、涂层缺陷处的腐蚀机制。</p></li><li><span>04</span><p>载荷上下文：侧面冲击的瞬态载荷、路面振动的循环载荷、热胀冷缩的日变化载荷。</p></li><li><span>05</span><p>历史上下文：过去 B 柱或相邻结构项目中的焊缝失效、失效里程、试验条件、保修索赔和供应商批次。</p></li></ol></div>
      <aside class="case-callout"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-risk"></use></svg></span><div><small>B 柱焊缝示例</small><h3>“焊缝失效”不该是分析终点，而应该是推理起点。</h3><p>车顶纵梁焊缝把热冲压 B 柱与不同钢种连接在一起；焊接改变局部微观结构；接头同时承受道路振动和碰撞冲击；焊渣飞溅可能降低涂层附着；腐蚀萌生后又可能在持续载荷下发展为应力腐蚀开裂。只有这些条件同时出现时，真正危险的组合失效才会显形。</p></div></aside>
    </section>

    <section class="case-section" data-section id="rflp">
      <p class="eyebrow">RFLP + event-driven knowledge</p>
      <h2>RFLP 让 AI 不只列失效模式，还能追溯它违反了哪条安全要求。</h2>
      <p>用于 DFMEA 的工程本体，可以基于 RFLP 构建：需求 Requirements、功能 Functions、逻辑架构 Logical、物理架构 Physical。这个框架不是随意分类，它反映了系统工程分解的方式，也让失效模式具备纵向追溯能力。</p>
      <ol class="case-process"><li><span>R</span><div><h3>需求层：定义 B 柱必须达到什么指标</h3><p>例如侧碰能量吸收、车顶抗压、安全带锚固载荷、侵入量约束和法规/评级要求。</p></div></li><li><span>F</span><div><h3>功能层：定义它如何实现这些目标</h3><p>包括可控塑性变形、载荷路径分配、侵入量限制、乘员舱保持和约束系统锚固。</p></div></li><li><span>L</span><div><h3>逻辑架构层：把功能映射到抽象解决方案</h3><p>例如能量吸收区、结构连接件、锚固点、软硬区过渡、材料界面和载荷传递路径。</p></div></li><li><span>P</span><div><h3>物理架构层：对应实际硬件</h3><p>例如 22MnB5 帽形截面、激光焊接接头、四螺栓锚固板、涂层区域和钢/复合材料界面。</p></div></li></ol>
      <p>失效模式不再孤立存在。它可以向上追溯到物理部件，经由逻辑要素抵达某项功能，最终影响某条需求。于是 AI 可以回答更有工程价值的问题：如果这条焊缝失效，会违反哪项安全要求？会影响哪个功能？会产生什么乘员后果？需要什么试验或仿真来验证？</p>
      <aside class="case-callout"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><div><small>事件驱动</small><h3>本体不是一次性分类表，而是持续演进的风险情报系统。</h3><p>新材料进入供应链，失效机制会传播到相关部件；现场故障出现，发生率评级沿因果链更新；法规标准变化，受影响功能和需求被标记复评；ECO 修改设计，系统判断哪些 DFMEA 条目已经失效、哪些仍然有效。</p></div></aside>
    </section>

    <section class="case-section" data-section id="agent-system">
      <p class="eyebrow">Seven dimensions</p>
      <h2>以本体为基础，智能体 AI 从七个维度重塑 DFMEA。</h2>
      <p>这七个维度不是并列功能清单，而是一条递进价值链：数据消除记忆问题，推理应用结构化智能，发现找到未知风险，预测预判未来失效，证据让决策植根于物理规律，行动确保每项风险都有验证路径，演进让 DFMEA 随设计变化保持实时更新。</p>
      <div class="case-adoption-grid"><article><span>01</span><small>规模化知识</small><h3>终结记忆局限</h3><p>AI 增强型 DFMEA 同时调用过去项目、材料库、试验报告、保修索赔、供应商记录和未量产原型缺陷。质量不再取决于当天谁在会议室。</p></article><article><span>02</span><small>本体推理</small><h3>应用结构化智能</h3><p>失效模式、结构分解、法规认证和耐久性分析代理共享同一本体，每项断言都能沿材料、工艺、功能和需求链路审计。</p></article><article><span>03</span><small>跨项目迁移</small><h3>发现意想不到的发现</h3><p>卡车 C 柱项目中的焊接疲劳，可以通过材料、工艺、环境和载荷相似性迁移到轿车 B 柱，而不是困在旧项目表格里。</p></article><article><span>04</span><small>组合失效识别</small><h3>找到你不知道自己在找什么</h3><p>系统不只检索“焊缝失效”，还会追踪氢脆、疲劳循环、腐蚀、涂层附着力和残余应力的交互。</p></article><article><span>05</span><small>物理证据</small><h3>让结论回到工程规律</h3><p>每条高风险断言都绑定材料曲线、焊接窗口、载荷谱、腐蚀环境、仿真或试验依据，而不是只给一个文本答案。</p></article><article><span>06</span><small>验证行动</small><h3>每项风险都有下一步</h3><p>风险被转化为试验、仿真、供应商控制、工艺窗口、设计复核或人工专家审批任务。</p></article><article><span>07</span><small>持续演进</small><h3>DFMEA 成为动态风险情报系统</h3><p>每次 DFMEA、保修索赔、现场故障、法规变化和 ECO 都反过来丰富本体，让下一次分析更完整。</p></article></div>
      <div class="case-board-questions"><div><small>多智能体分工</small><h3>每个代理贡献一类工程深度，但共享同一条证据链。</h3><p>这不是让一个通用聊天模型“懂汽车”，而是把不同专业任务拆给不同代理，再用本体统一上下文、权限和审计。</p></div><ol><li><span>01</span><p>失效模式分析代理：材料科学、氢脆、疲劳、腐蚀和断裂机制。</p></li><li><span>02</span><p>结构分解代理：界面节点、载荷路径、软硬区过渡和组合效应。</p></li><li><span>03</span><p>法规/认证代理：FMVSS、Euro NCAP、IIHS、ISO 26262 等要求映射。</p></li><li><span>04</span><p>通用分析代理：制造工艺风险、长期耐久性、供应商变更和现场反馈。</p></li></ol></div>
    </section>

    <section class="case-section case-application" data-section id="manager-actions">
      <p class="eyebrow">What leaders should build</p>
      <h2>对制造企业来说，本体是把老师傅经验留在公司里的 AI 资产。</h2>
      <p>提示词和模型选择可以被竞争对手复制，但本体很难复制。它以结构化、机器可读的形式编码组织多年积累的工程专有知识：真实代价换来的失效模式、适配自身制造能力的材料工艺组合、目标市场监管条款解读，以及与自身车辆架构相关的界面风险。它解决的不是“有没有 AI”，而是“企业交过的学费能不能被下一代项目继续使用”。</p>
      <div class="case-fit-grid"><article class="case-fit-card case-fit-card--yes"><small>现在就该做</small><h3>把机构记忆转成可计算资产</h3><ul><li>梳理历史 DFMEA、试验报告、保修索赔和现场故障</li><li>把材料、工艺、界面、载荷、法规和功能要求编码为关系</li><li>建立严重度、发生率、探测度或行动优先级的统一口径</li><li>让 ECO、法规变化和供应链变化触发复评</li></ul></article><article class="case-fit-card case-fit-card--yes"><small>不要先做</small><h3>不要把 LLM 当成电子表格填充器</h3><ul><li>不要只让模型复述历史表格</li><li>不要把未验证生成结果直接作为工程结论</li><li>不要跳过人类专家复核和试验证据</li><li>不要忽视本体读写、审计和权限边界</li></ul></article></div>
      <div class="case-reading-note"><strong>Q2Q 视角</strong><p>DFMEA 智能体不是替代工程责任，而是把工程师、材料知识、历史证据和验证路径组织成一个可追踪的 Human + Agent 工作单元。制造企业先判断这条工作单元能否减少知识流失、缩短复评时间、降低遗漏风险，再谈多智能体架构。</p></div>
    </section>

    <section class="case-section" data-section id="references">
      <p class="eyebrow">Public technical context</p>
      <h2>公开资料用于校准技术背景，项目实施仍要回到企业自己的设计、试验和质量数据。</h2>
      <p>下面这些公开资料适合用于理解法规测试、材料工艺、FMEA 方法和智能体平台的基础概念。真正落地时，风险判断仍应以企业自己的设计数据、试验记录、工艺窗口、供应商信息和质量反馈为准。</p>
      <div class="case-reference-list"><a href="https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/809004" target="_blank" rel="noopener">NHTSA FMVSS 214 侧碰保护评估</a><a href="https://www.iihs.org/media/46940e89-46cb-4e6e-81ee-8230bb3b5dd9/0dx8eA/Ratings/Protocols/current/test_protocol_roof.pdf" target="_blank" rel="noopener">IIHS Roof Strength Test Protocol</a><a href="https://crashstats.nhtsa.dot.gov/Api/Public/Publication/813027" target="_blank" rel="noopener">NHTSA FMVSS 216a Roof Crush Resistance 评估</a><a href="https://ahssinsights.org/tag/hot-stamped-boron/" target="_blank" rel="noopener">AHSS Guidelines：热冲压硼钢与 B 柱案例</a><a href="https://www.open-access.bcu.ac.uk/6942/" target="_blank" rel="noopener">22MnB5 热冲压超高强钢论文摘要</a><a href="https://www.aiag.org/training-and-resources/manuals/details/FMEAAV-1" target="_blank" rel="noopener">AIAG &amp; VDA FMEA Handbook 训练资料</a><a href="https://docs.aws.amazon.com/bedrock-agentcore/" target="_blank" rel="noopener">Amazon Bedrock AgentCore 文档</a><a href="https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/" target="_blank" rel="noopener">AWS：Strands Agents SDK 介绍</a></div>
    </section>

    <section class="case-section" data-section id="next">
      <p class="eyebrow">Part two preview</p>
      <h2>下篇进入技术实现：AgentCore、Strands SDK、七层 AWS 架构和 B 柱逐步演练。</h2>
      <p>第二部分将深入技术架构细节：基于 Amazon Bedrock AgentCore 与 Strands SDK 的实现逻辑，多智能体编排 Pipeline，本体读写机制，以及 B 柱 DFMEA 的逐步实现演练。</p>
      <div class="case-related-grid"><article class="case-related-card"><div><small>架构层</small><h3>7 层 AWS 架构</h3><p>从数据接入、本体存储、AgentCore 运行时，到审计、权限和工程系统集成。</p></div></article><article class="case-related-card"><div><small>编排层</small><h3>多智能体管道</h3><p>失效模式、结构分解、法规认证、通用耐久性分析代理如何协同。</p></div></article><article class="case-related-card"><div><small>演练层</small><h3>B 柱 DFMEA 步进实现</h3><p>从输入设计、调用本体、生成候选失效模式，到证据复核和 ECO 更新。</p></div></article></div>
    </section>
  </article>
</div>
<section class="case-related">
  <div class="container">
    <div class="case-related-head"><div><p class="eyebrow">Related cases</p><h2>继续看相邻问题，建立完整判断。</h2></div><a class="text-link" href="cases.html">查看全部案例 →</a></div>
    <div class="case-related-grid">
      <a class="case-related-card" href="case-manufacturing-pid-intelligence.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/thumb-manufacturing-pid.webp"><div><small>制造业知识资产化</small><h3>P&amp;ID 图纸如何变成可查询运营知识</h3><p>静态图纸、知识图谱、工程师复核和可追溯问答</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-healthcare-agent-roi.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/healthcare-care-chain-sana-plain.png"><div><small>高合规智能体</small><h3>医疗工作流中的受限多智能体架构</h3><p>状态机、人工升级、模型专项化和 ROI 验证</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="navigator.html"><img alt="" decoding="async" loading="lazy" src="assets/generated-review/c02-navigator-china-q2q-diagnostic-workbench.png"><div><small>Q2Q 场景诊断</small><h3>先判断场景是否值得 AI 化</h3><p>从问题、数据、责任和证据门判断第一条 AI 增长流</p><span>继续阅读 <b>↗</b></span></div></a>
    </div>
  </div>
</section>
<section class="case-next-cta"><div class="container case-next-cta__inner"><div><small>把案例映射到你的企业</small><h2>不要先问用哪个模型，先问知识能否被推理和复评。</h2><p>把真实流程、材料工艺、历史失效和验证责任带进一次场景诊断，判断这个 AI 工作单元是否具备上线资格。</p></div><div><a class="btn btn--light" href="navigator.html">开始 AI 场景诊断 →</a><a class="btn btn--ghost" href="cases.html">返回案例中心</a></div></div></section>
<section class="case-source-foot" id="case-source" aria-labelledby="case-source-title"><div class="container"><div class="case-source-card"><span class="case-source-card__icon"><svg aria-hidden="true" class="ff-icon"><use href="#i-reference"></use></svg></span><div><small>案例价值</small><h2 id="case-source-title">这不是“AI 写 DFMEA”，而是把安全关键工程知识变成可复用资产。</h2><p>对企业来说，真正的收益来自三件事：减少遗漏，统一判断口径，保留工程经验。本体智能体让 DFMEA 从一次性会议和静态表格，变成随设计、法规、现场反馈和工程变更持续演进的风险情报系统。</p><a href="navigator.html">开始 AI 场景诊断 <span aria-hidden="true">↗</span></a></div></div></div></section>
'''
(ROOT/'case-automotive-dfmea-ontology-agent.html').write_text(page('基于本体的智能体 AI 如何重塑安全关键型汽车零部件的 DFMEA（上篇）','以 B 柱 DFMEA 为例，解释工程本体、RFLP、智能体 AI 和多项目知识迁移如何重塑安全关键汽车零部件风险分析。','case-automotive-dfmea-ontology-agent',automotive_dfmea_body,'case-detail-page case-theme--automotive case-study-v2'),encoding='utf-8')

supply_chain_agentic_body='''
<section class="case-study-hero case-study-hero--supply">
  <div class="container">
    <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="cases.html">案例中心</a><span>/</span><strong>零售供应链与多智能体决策</strong></nav>
    <div class="case-study-hero__grid">
      <div class="case-study-hero__copy">
        <div class="case-study-meta"><span>案例 Blog</span><span>零售供应链</span><span>多智能体 AI</span><span>从洞察到行动</span></div>
        <h1>多智能体 AI 如何将供应链数据转化为决策与行动</h1>
        <p class="case-study-lead">供应链老板最关心的不是又多一个仪表盘，而是异常能不能更早被发现，根因能不能更快说清，行动能不能直接进入负责人手里。库存周转缩短一天、缺货率降低一个百分点、物流异常提前一小时发现，单看都不惊人；放到数百万个 SKU 和数十亿美元营收规模里，就会持续改变成本结构、客户体验和新品上市速度。</p>
        <div class="case-study-actions"><a class="btn btn--green" href="#architecture">看架构设计 <span aria-hidden="true">↓</span></a><a class="btn btn--ghost" href="#workflow">看 30 秒履行分析 <span aria-hidden="true">↘</span></a></div>
      </div>
      <figure class="case-study-hero__media case-study-hero__media--scene">
        <img alt="零售供应链运营负责人查看数据并准备行动" decoding="async" loading="eager" src="assets/cases/supply-chain-agentic-decision-hero.png">
        <figcaption>供应链决策不止是“看见数据”，而是把查询、分析、归因和行动连成一条可复盘的工作链。</figcaption>
      </figure>
    </div>
    <div aria-label="本案例的决策证据结构" class="case-proof-rail"><div><strong>数据可见</strong><span>ERP、WMS、TMS、数据湖和仪表盘只是起点</span></div><div><strong>主动推理</strong><span>自然语言发问，自动查询、钻取和归因</span></div><div><strong>行动闭环</strong><span>通知、审批摘要和工单直接进入团队流程</span></div><div><strong>可维护架构</strong><span>语义层和 MCP 让数据源变化不拖垮智能体</span></div></div>
    <p class="case-proof-note">这篇案例的重点不是替代供应链团队，而是把分析师、运营经理、渠道负责人和信用控制团队之间的人工衔接，改造成可追踪、可复用、可审计的 Human + Agent 决策工作单元。</p>
  </div>
</section>
<div class="container case-detail-shell case-story-shell">
  <aside class="case-toc"><div class="case-toc-inner"><small>本页目录</small><nav data-scrollspy><a class="is-active" href="#challenge">决策问题</a><a href="#bottleneck">控制塔瓶颈</a><a href="#architecture">架构设计</a><a href="#design-decisions">关键设计</a><a href="#workflow">履行分析</a><a href="#operating-model">企业落地</a><a href="#references">技术背景</a></nav><a class="case-toc-source" href="cases.html">返回案例中心</a></div></aside>
  <article>
    <section class="case-section" data-section id="challenge">
      <p class="eyebrow">Decision quality</p>
      <h2>供应链竞争力，最后会落到每一天的决策质量上。</h2>
      <p>供应链既是零售企业最重要的竞争优势之一，也是运营上最复杂的环节之一。每一个决策都有可量化的成本代价：库存周转时间缩短一天、缺货率降低一个百分点、提前一小时发现物流异常，这些收益都会在规模里叠加。</p>
      <p>真正的问题不是企业有没有数据，而是在正确的时间，基于正确的信息，做出正确判断。大型语言模型已经能够可靠调用工具，编排框架也日趋成熟，多智能体架构开始有能力以生产级质量完成复杂的查询、分析、根因归因和行动协同。</p>
      <div class="case-question-panel"><div><small>老板视角</small><h3>如果一个问题要半天才查清，很多异常根本不会被调查。</h3><p>当提问成本很高，团队只会追几个固定 KPI；当提问成本降到一句话和几十秒，供应链团队才会追踪更多边角异常，决策覆盖范围才会扩大。</p></div><div class="case-goal"><small>目标工作单元</small><h3>收集 → 查询 → 洞察 → 行动</h3><p>数据收集已经基本解决，Agent 要补的是后面三步：自动查询、自动分析、把结论变成可执行动作。</p></div></div>
    </section>

    <section class="case-section" data-section id="bottleneck">
      <p class="eyebrow">Visibility is not decision</p>
      <h2>数据可见性，不等于数据驱动决策。</h2>
      <p>经过多年数字化投资，大多数零售商已经建立了相当完整的数据基础设施：ERP、WMS、TMS、数据湖和各类仪表盘一应俱全。控制塔把多源数据聚合起来，提供可视化和告警，解决了“看见数据”的问题。</p>
      <p>但控制塔本质上仍然偏被动：分析逻辑在构建时就已固化，只能展示预定义指标，无法主动推理；迭代周期常常以周或月计。业务人员仍然要通过数据工程团队提需求、等结果，在电子表格里做分析，再靠邮件和会议推动行动。</p>
      <div class="case-value-cards case-value-cards--triple"><article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-data"></use></svg></span><small>查询障碍</small><h3>业务人员难以自助获取数据</h3><p>SQL 技能门槛、不一致的业务定义和复杂多表关联，让很多问题停在“能不能帮我拉一下数”。</p></article><article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-brain"></use></svg></span><small>洞察差距</small><h3>原始数据不能自动变成结论</h3><p>异常检测、多维钻取和根因归因仍然依赖人工经验，分析质量和速度跟人强相关。</p></article><article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><small>行动脱节</small><h3>洞察留在报告里，行动靠人协调</h3><p>即使结论清楚，后续仍要发邮件、拉群、开会和追审批，响应时间以天计。</p></article></div>
      <div class="case-comparison-table"><div><span>决策瓶颈</span><span>控制塔的局限</span><span>智能体 AI 的解法</span><strong>查询障碍</strong><p>需要 SQL 技能和数据工程支持</p><p>自动将自然语言翻译成 SQL 查询</p><strong>洞察差距</strong><p>只展示预定义指标</p><p>执行异常检测、多维钻取和根因归因</p><strong>行动脱节</strong><p>分析留在报告里，行动依赖人工协调</p><p>生成可执行材料并通知相关团队</p></div></div>
    </section>

    <section class="case-section" data-section id="architecture">
      <p class="eyebrow">Supervisor-worker architecture</p>
      <h2>架构的关键，是让主管代理理解意图，让专项代理各自做好一件事。</h2>
      <p>基于一家全球鞋服零售商的匿名化场景，可以把系统拆成九个核心组件：用户接入层、智能体核心层、数据访问与网关层、可观测性层。它不是在现有数据平台旁边再做一个“更漂亮的仪表盘”，而是在数据基础设施之上自动化整条推理链。</p>
      <div class="case-architecture-map" aria-label="供应链多智能体架构九组件">
        <article><span>01</span><h3>Web UI</h3><p>业务用户用自然语言发起供应链问题。</p></article>
        <article><span>02</span><h3>Chatbot App</h3><p>承接对话、上下文和前端状态。</p></article>
        <article><span>03</span><h3>API Gateway + Lambda</h3><p>把前后端请求接入后端服务。</p></article>
        <article><span>04</span><h3>Cognito</h3><p>统一用户认证与访问入口。</p></article>
        <article><span>05</span><h3>DynamoDB</h3><p>保存对话历史和应用配置。</p></article>
        <article><span>06</span><h3>Strands + AgentCore Runtime</h3><p>运行主管代理和专项代理。</p></article>
        <article><span>07</span><h3>Amazon Bedrock</h3><p>提供模型能力和工具调用推理。</p></article>
        <article><span>08</span><h3>AgentCore Gateway + MCP</h3><p>通过 API 目标和 Lambda 目标访问外部数据源。</p></article>
        <article><span>09</span><h3>AgentCore Observability</h3><p>追踪智能体状态、工具调用和执行链路。</p></article>
      </div>
      <div class="case-board-questions"><div><small>代理分工</small><h3>职责拆开，准确性才有空间提升。</h3><p>实践中的一个重要经验是：把所有能力塞进单一智能体提示词，提示词越长，SQL 生成准确性越容易下降。拆成主管-员工模式后，每个代理可以有自己的语义、工具、错误重试和质量检查。</p></div><ol><li><span>01</span><p>主管代理：解读用户意图，判断简单查询还是复杂分析，并协调流程。</p></li><li><span>02</span><p>查询代理：自然语言转 SQL，执行基准查询和周期比较。</p></li><li><span>03</span><p>详细代理：发现异常后，按类别、时间段和区域执行多维钻取。</p></li><li><span>04</span><p>研究代理：从多个角度调查根因。</p></li><li><span>05</span><p>汇总代理：将结果整理为结构化业务报告。</p></li><li><span>06</span><p>行动代理：生成通知、审批摘要和工单。</p></li></ol></div>
    </section>

    <section class="case-section" data-section id="design-decisions">
      <p class="eyebrow">Semantic layer + MCP</p>
      <h2>两个设计决策，决定系统能不能长期可靠运行。</h2>
      <div class="case-fit-grid"><article class="case-fit-card case-fit-card--yes"><small>业务术语语义层</small><h3>最常见错误不是 SQL 语法，而是业务定义误解。</h3><ul><li>“滞销库存”“履行率”“未付款订单”在不同企业有不同口径</li><li>把业务术语到 SQL 表达式的映射注入查询代理</li><li>例如将“履行率”定义为已交付订单数 / 全部订单数</li><li>强制所有查询包含日期筛选器，避免无边界扫描</li></ul></article><article class="case-fit-card case-fit-card--yes"><small>MCP 数据源解耦</small><h3>智能体不直接绑死某个数据库或查询引擎。</h3><ul><li>AgentCore Gateway 将 API、Lambda 和现有服务转换为 MCP 工具</li><li>底层查询引擎迁移时，优先替换 MCP 服务器实现</li><li>渠道伙伴和数据源变化时，智能体代码不必反复改</li><li>认证、凭据交换和工具发现由网关层统一处理</li></ul></article></div>
      <aside class="case-callout"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-shield"></use></svg></span><div><small>企业级边界</small><h3>Agent 能行动，不代表可以无限行动。</h3><p>供应链场景里的工具调用要绑定身份、权限、日期范围、业务口径和审批边界。可以让 Agent 生成订单放行请求摘要，但是否放行、放行多少、由谁审批，仍要回到企业的责任体系。</p></div></aside>
    </section>

    <section class="case-section" data-section id="workflow">
      <p class="eyebrow">Channel fulfillment analysis</p>
      <h2>一次“渠道履行情况如何”的提问，可以形成从查询到行动的完整链路。</h2>
      <p>月度运营回顾中，运营经理提出问题：“我们渠道合作伙伴上个月的订单履行情况如何？有哪些需要关注？”过去这类问题往往需要半天时间、电子表格分析和多轮邮件协调。多智能体流程把它拆成可复盘的步骤。</p>
      <ol class="case-process"><li><span>01</span><div><h3>主管代理识别复杂分析请求</h3><p>它不直接给一句笼统回答，而是将任务路由给查询代理，先建立可计算基线。</p></div></li><li><span>02</span><div><h3>查询代理映射业务定义并执行 SQL</h3><p>“履行绩效”被映射到语义层定义，按渠道执行查询，并与上月数据进行比较。</p></div></li><li><span>03</span><div><h3>渠道 B 履行率异常，环比下降 6.8%</h3><p>系统识别这不是普通波动，需要进入详细代理的多维钻取。</p></div></li><li><span>04</span><div><h3>详细代理定位到品类与时间窗口</h3><p>异常集中在鞋类，并且主要发生在当月第二周和第三周。</p></div></li><li><span>05</span><div><h3>研究代理发现信用控制触发</h3><p>渠道 B 的未付款订单率从 8% 上升到 22%，约 340 个订单因此被冻结。</p></div></li><li><span>06</span><div><h3>汇总与行动代理推动后续处理</h3><p>系统生成根因报告、行动建议、渠道客户经理通知、信用控制团队通知和订单放行请求摘要，进入审批流程。</p></div></li></ol>
      <div class="case-metric-strip"><div><strong>30 秒</strong><span>从提问到结构化分析和行动材料</span></div><div><strong>-6.8%</strong><span>渠道 B 履行率环比异常</span></div><div><strong>8% → 22%</strong><span>未付款订单率上升触发信用控制</span></div><div><strong>约 340</strong><span>被冻结订单进入后续放行判断</span></div></div>
    </section>

    <section class="case-section" data-section id="operating-model">
      <p class="eyebrow">How leaders should read it</p>
      <h2>企业主不需要先买一整套大平台，可以从一个高频决策问题开始。</h2>
      <p>起点不必很大。先选一个能明确算成本、能明确追责、能明确行动人的问题，例如渠道履行异常、库存冻结、缺货风险、物流延迟或高退货 SKU。把数据源、业务术语、审批边界和人工复核路径定义清楚，再让多智能体系统接管查询、分析、材料生成和通知。</p>
      <div class="case-adoption-grid"><article><span>01</span><small>选择问题</small><h3>从一个真问题开始</h3><p>不要先问“我们能不能做 Agent”，而是问“哪个供应链问题每天都在消耗人力和响应时间”。</p></article><article><span>02</span><small>定义口径</small><h3>先建语义层</h3><p>履行率、滞销、缺货、冻结、异常订单等术语要有统一计算口径，否则自然语言查询只会更快地产生错误。</p></article><article><span>03</span><small>接入工具</small><h3>用 MCP 包住数据源</h3><p>ERP、WMS、TMS、数据湖、审批系统和消息系统不必一次性重构，但要以可治理工具形式暴露给 Agent。</p></article><article><span>04</span><small>保留责任</small><h3>行动必须有审批边界</h3><p>Agent 可以建议和生成材料，关键库存、信用和客户动作仍应由授权人员确认。</p></article><article><span>05</span><small>复盘质量</small><h3>让每次分析可审查</h3><p>同样的问题和数据应产生一致路径，SQL、工具调用、根因判断和通知记录都要能回看。</p></article><article><span>06</span><small>逐步扩展</small><h3>从局部闭环到控制面升级</h3><p>先跑通一个问题的收集、查询、洞察和行动，再扩展到更多渠道、品类和供应链任务。</p></article></div>
      <div class="case-reading-note"><strong>Q2Q 视角</strong><p>这类项目的评估重点，不是模型回答得多漂亮，而是一个 Human + Agent 工作单元能否减少等待、减少误判、缩短行动链路，并让业务负责人愿意在真实运营会上使用它。</p></div>
    </section>

    <section class="case-section" data-section id="references">
      <p class="eyebrow">Technical context</p>
      <h2>技术选型要服务于业务闭环，而不是把供应链变成另一个演示场。</h2>
      <p>AgentCore、Strands 和 MCP 的价值，在于让企业把模型、工具、身份、数据源和可观测性组织到可运行的体系里。正式项目仍要回到企业自身的数据结构、业务口径、权限模型、审批流程和运营节奏。</p>
      <div class="case-reference-list"><a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html" target="_blank" rel="noopener">Amazon Bedrock AgentCore 官方概览</a><a href="https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html" target="_blank" rel="noopener">AgentCore Gateway 与 MCP 工具接入</a><a href="https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/" target="_blank" rel="noopener">AWS：Strands Agents SDK 介绍</a><a href="https://modelcontextprotocol.io/docs/getting-started/intro" target="_blank" rel="noopener">Model Context Protocol 官方介绍</a></div>
    </section>
  </article>
</div>
<section class="case-related">
  <div class="container">
    <div class="case-related-head"><div><p class="eyebrow">Related cases</p><h2>继续看相邻问题，建立完整判断。</h2></div><a class="text-link" href="cases.html">查看全部案例 →</a></div>
    <div class="case-related-grid">
      <a class="case-related-card" href="case-healthcare-agent-roi.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/healthcare-care-chain-sana-plain.png"><div><small>高合规智能体</small><h3>医疗工作流中的受限多智能体架构</h3><p>状态机、人工升级、模型专项化和 ROI 验证</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-automotive-dfmea-ontology-agent.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/automotive-dfmea-bpillar-hero.png"><div><small>汽车工程知识资产</small><h3>B 柱 DFMEA 如何沉淀组织记忆</h3><p>工程本体、RFLP、多智能体和知识流失治理</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-manufacturing-pid-intelligence.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/thumb-manufacturing-pid.webp"><div><small>制造业知识资产化</small><h3>P&amp;ID 图纸如何变成可查询运营知识</h3><p>静态图纸、知识图谱、工程师复核和可追溯问答</p><span>继续阅读 <b>↗</b></span></div></a>
    </div>
  </div>
</section>
<section class="case-next-cta"><div class="container case-next-cta__inner"><div><small>把案例映射到你的企业</small><h2>先找一个供应链问题，把“看见数据”推进到“采取行动”。</h2><p>用一次 Q2Q 场景诊断，把数据源、业务口径、行动边界和验收指标摆清楚，判断这个 Agent 工作单元是否值得进入试点。</p></div><div><a class="btn btn--light" href="navigator.html">开始 AI 场景诊断 →</a><a class="btn btn--ghost" href="cases.html">返回案例中心</a></div></div></section>
<section class="case-source-foot" id="case-source" aria-labelledby="supply-case-source-title"><div class="container"><div class="case-source-card"><span class="case-source-card__icon"><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><div><small>案例价值</small><h2 id="supply-case-source-title">这不是“AI 问数”，而是把供应链决策变成可复盘的行动系统。</h2><p>对企业来说，真正的收益来自三件事：降低提问成本、缩短根因定位时间、让行动材料直接进入责任人流程。多智能体 AI 的价值，只有在业务口径、权限和人工审批都被设计清楚后，才会稳定释放。</p><a href="navigator.html">开始 AI 场景诊断 <span aria-hidden="true">↗</span></a></div></div></div></section>
'''
(ROOT/'case-supply-chain-agentic-decision.html').write_text(page('多智能体 AI 如何将供应链数据转化为决策与行动','以零售供应链为例，解释多智能体 AI、语义层和 MCP 如何把数据可见性推进到查询、洞察和行动闭环。','case-supply-chain-agentic-decision',supply_chain_agentic_body,'case-detail-page case-theme--supply case-study-v2'),encoding='utf-8')

write_search_index()

search_body=f'''
<section class="search-page-hero"><div class="container"><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>搜索</strong></nav><form class="search-page-form" action="search.html" method="get"><span>{SEARCH_ICON}</span><input data-search-page-input type="search" name="search" value="" placeholder="输入行业、技术、场景或案例，例如：供应链 / DFMEA / 医疗" aria-label="搜索关键词"><button class="btn btn--green" type="submit">搜索</button></form><p class="search-live-summary" data-search-summary aria-live="polite">输入关键词后会按相关度排序。</p><div class="search-quick-links" aria-label="常用搜索"><span>试试：</span><a href="search.html?search=供应链">供应链</a><a href="search.html?search=DFMEA">DFMEA</a><a href="search.html?search=B柱">B 柱</a><a href="search.html?search=医疗">医疗智能体</a><a href="search.html?search=AgentCore">AgentCore</a><a href="search.html?search=P%26ID">P&amp;ID</a><a href="search.html?search=数据治理">数据治理</a></div><div class="search-tabs"><button class="is-active" data-search-tab="all">全部 <span data-count-all>0</span></button><button data-search-tab="category">方案分类 <span data-count-category>0</span></button><button data-search-tab="service">企业服务 <span data-count-service>0</span></button><button data-search-tab="resource">资料 <span data-count-resource>0</span></button><button data-search-tab="case">案例 <span data-count-case>0</span></button></div></div></section>
<section class="search-results-page section-pad" data-search-index="search-index.json?v={ASSET_VERSION}"><div class="container"><div class="search-result-group" data-result-type="category"><div class="search-result-head"><h2>方案分类 <span>{search_type_count('category')}</span></h2><a href="category-hrms.html">查看全部 →</a></div><div class="search-result-grid" data-search-grid="category">{render_search_cards('category')}</div></div>
<div class="search-result-group" data-result-type="service"><div class="search-result-head"><h2>企业服务 <span>{search_type_count('service')}</span></h2><a href="index.html#services">查看全部 →</a></div><div class="search-result-grid" data-search-grid="service">{render_search_cards('service')}</div></div>
<div class="search-result-group" data-result-type="resource"><div class="search-result-head"><h2>资料 <span>{search_type_count('resource')}</span></h2><span>PDF / 在线手册</span></div><div class="search-result-grid" data-search-grid="resource">{render_search_cards('resource')}</div></div>
<div class="search-result-group" data-result-type="case"><div class="search-result-head"><h2>案例 <span>{search_case_count()}</span></h2><a href="cases.html">查看全部 →</a></div><div class="search-result-grid" data-search-grid="case">{render_search_case_cards()}</div></div>
<div class="search-empty" data-search-empty hidden><h2>没有找到完全匹配的内容。</h2><p>可以尝试“Agent”“数据治理”“培训”“HR”或“Playbook”。</p><a class="btn btn--green" href="navigator.html">改用场景诊断 →</a></div></div></section>
'''
(ROOT/'search.html').write_text(page('搜索','搜索 ForFlow 企业服务、场景、资料与案例。','',search_body,'search-page'),encoding='utf-8')

viewer_body='''
<section class="viewer-toolbar"><div class="container viewer-toolbar-inner"><div><a class="viewer-back" href="search.html">← 返回搜索</a><h1 data-doc-title>企业生成式 AI 实战手册</h1></div><div class="viewer-actions"><a class="btn btn--ghost" data-doc-open target="_blank" rel="noopener"><span>新窗口打开</span> ↗</a><a class="btn btn--green" data-doc-download download><span>下载 PDF</span> ↓</a></div></div></section>
<section class="viewer-main"><div class="container viewer-shell"><aside class="viewer-meta"><img src="assets/forflow-lockup.png" alt="ForFlow 萬維流形"><div><small>文档类型</small><strong>PDF 参考资料</strong></div><div><small>阅读说明</small><p>桌面端使用浏览器内置阅读器。手机浏览器若无法内嵌，可使用“新窗口打开”或“下载 PDF”。</p></div></aside><div class="pdf-frame"><iframe data-doc-frame title="PDF 阅读器" src="assets/genai-playbook-reference.pdf#view=FitH"></iframe><div class="pdf-fallback"><p>当前浏览器无法内嵌 PDF？</p><a class="btn btn--green" data-doc-open target="_blank" rel="noopener">打开文档 →</a></div></div></div></section>
'''
(ROOT/'document-viewer.html').write_text(page('PDF 阅读器','在线查看和下载企业 AI 参考 PDF。','document-viewer',viewer_body,'viewer-page'),encoding='utf-8')

# README
readme='''# ForFlow 萬維流形企业网站原型\n\n这是在已有 `index.html` 与 `navigator.html` 基础上继续扩展的静态响应式网站，不依赖前端框架。\n\n## 页面\n\n- `index.html`：主页（保留原有框架并加入四项企业服务）\n- `navigator.html`：3 分钟 AI 场景诊断\n- `navigator-results.html`：推荐结果、品牌视频控件与方案排序\n- `playbook.html`：中文企业生成式 AI 实战手册\n- `service-ai-enablement.html`：企业 AI 赋能计划\n- `service-data-governance.html`：数据治理\n- `service-agent-build.html`：企业 Agent 搭建\n- `service-ai-training.html`：企业 AI 培训\n- `category-hrms.html`：HR AI 场景分类页\n- `cases.html`：案例中心\n- `case-wren-kitchens.html`：Wren Kitchens 公开案例结构参考\n- `case-manufacturing-pid-intelligence.html`：制造业 P&ID 智能化案例\n- `case-healthcare-agent-roi.html`：医疗智能体 ROI 案例\n- `case-automotive-dfmea-ontology-agent.html`：汽车 DFMEA 本体智能体案例\n- `case-supply-chain-agentic-decision.html`：供应链多智能体决策案例\n- `search.html`：全站搜索结果页\n- `document-viewer.html`：PDF 在线阅读器\n\n## 运行\n\n```bash\npython -m http.server 8080\n```\n\n打开 `http://localhost:8080/`。\n\n## 说明\n\n- 使用用户提供的 ForFlow + 萬維流形完整标识，不使用黑色方形图标。\n- Navigator 结果页的动效视频由完整品牌标识制作，带原生视频控件。\n- 所有服务页包含服务流程、交付物、FAQ 与相关路径。\n- 搜索弹层、搜索结果、PDF 展示、筛选、排序、FAQ、移动菜单和目录均为前端可交互原型。\n- 案例中的公开企业资料仅作为结构参考，正式发布前需复核授权和最新数据。\n'''
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
version_asset_links()
