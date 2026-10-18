# -*- coding: utf-8 -*-

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

# Targeted homepage generation keeps unrelated generated pages intact.
from scripts.sync_homepage_theme import sync as sync_homepage_theme
if '--homepage-only' in sys.argv:
    sync_homepage_theme(ROOT)
    print('Homepage template and isolated theme generated')
    sys.exit(0)
sys.path.insert(0, str(ROOT / '.python-deps'))

from bs4 import BeautifulSoup
import html
import json
import re

SEARCH_ICON = '''<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="m16.2 16.2 4.3 4.3"></path></svg>'''
ARROW = '<span class="arrow" aria-hidden="true">→</span>'
ASSET_VERSION = '20260712-service-visual-pilot-v28'
CSS_VERSION = ASSET_VERSION
SCRIPT_VERSION = ASSET_VERSION
VISUAL_SYSTEM_VERSION = ASSET_VERSION

def mobile_title(*lines):
    return ''.join(f'<span class="mobile-title-line">{html.escape(line)}</span>' for line in lines)

def set_mobile_title(soup, selector, lines):
    target = soup.select_one(selector)
    if not target:
        return
    target.clear()
    for line in lines:
        span = soup.new_tag('span', **{'class': 'mobile-title-line'})
        span.string = line
        target.append(span)

NAV_ITEMS = [
    ('index.html', '首页', 'home'),
    ('index.html#services', '企业服务', 'services'),
    ('navigator.html', 'AI 场景诊断', 'navigator'),
    ('playbook.html', '企业 AI 手册', 'playbook'),
    ('cases.html', '案例&博客', 'cases'),
]

SERVICE_LINKS = [
    ('ai-readiness-audit.html', 'AI 准备度审核'),
    ('service-ai-enablement.html', 'AI 采用与团队赋能'),
    ('service-data-governance.html', 'AI 数据与知识治理'),
    ('service-agent-build.html', '企业 Agent 与工作流'),
    ('service-ai-training.html', 'AI 实战培训'),
]

CASE_LIBRARY_ITEMS = [
    {
        'id': 'wren',
        'featured': True,
        'href': 'case-wren-kitchens.html',
        'tags': ['retail', 'manufacturing', 'data'],
        'kicker': '制造与零售 · 公开技术合作参考',
        'title': 'Wren Kitchens：从紧急团队扩容，到长期技术合作',
        'description': '公开案例摘要：团队接手关键系统后，把安装、物流、产品、QA 和移动应用逐步纳入长期协作。',
        'visual': {'type': 'art', 'class': 'case-art--wren', 'html': '<span>WREN / PUBLIC REFERENCE</span>'},
        'link_label': '查看案例详情 →',
        'search': True,
        'search_text': 'Wren 厨房 零售 制造 物流 技术合作 跨模块 软件交付 知识交接 长期合作',
        'search_kicker': '公开案例解读',
        'search_title': 'Wren Kitchens：从紧急扩容到长期技术合作',
        'search_description': '挑战、接管、模块、公开影响与可复用经验。',
    },
    {
        'id': 'jan-elly',
        'tags': ['education'],
        'kicker': 'IMDA 公开案例摘要',
        'title': '把单篇内容制作从 18 小时缩短到 30 分钟',
        'description': 'IMDA Playbook 报告的案例结果；页面仅做摘要，具体流程与口径以原文为准。',
        'visual': {'type': 'art', 'class': 'case-art--green', 'html': '<b>18h</b><span>→ 30min</span>'},
        'source_href': 'https://file.go.gov.sg/genai-playbook-pdf.pdf',
        'source_label': '查看 IMDA 原文 ↗',
    },
    {
        'id': 'crestar',
        'tags': ['retail', 'service'],
        'kicker': 'IMDA 公开案例摘要',
        'title': '智能客服把每周常规询问工时从 18 小时降到 8 小时',
        'description': 'Crestar Fan 的公开材料结果；强调高频问答分流，不把数字延伸为 ForFlow 成效。',
        'visual': {'type': 'art', 'class': 'case-art--dark', 'html': '<b>18h</b><span>→ 8h / 周</span>'},
        'source_href': 'https://www.imda.gov.sg/-/media/imda/files/news-and-events/media-room/media-releases/2024/10/singapore-digital-economy-remains-robust/annex-3-how-crestar-fan-supercharged-sales-and-efficiency-with-genai-powered-chatbot-solutions.pdf',
        'source_label': '查看 IMDA 原文 ↗',
    },
    {
        'id': 'etonhouse',
        'tags': ['education'],
        'kicker': 'IMDA 公开材料 · 预期目标',
        'title': '让教师把时间从行政工作还给学生',
        'description': 'IMDA 材料中的预期行政时间目标，不是已验证结果；实际变化仍需项目测量。',
        'visual': {'type': 'art', 'class': 'case-art--blue', 'html': '<b>-80%</b><span>预期行政时间</span>'},
        'source_href': 'https://file.go.gov.sg/genai-playbook-pdf.pdf',
        'source_label': '查看 IMDA 原文 ↗',
    },
    {
        'id': 'ihub',
        'tags': ['data'],
        'kicker': 'IMDA 公开材料 · 预期目标',
        'title': '用自然语言查询多源供应链数据',
        'description': 'IMDA 材料中的预期报表时长目标，不是已验证结果；实际变化仍需项目测量。',
        'visual': {'type': 'art', 'class': 'case-art--lines', 'html': '<b>-50%</b><span>预期报表时间</span>'},
        'source_href': 'https://file.go.gov.sg/genai-playbook-pdf.pdf',
        'source_label': '查看 IMDA 原文 ↗',
        'search': True,
        'search_text': '物流 数据 Agent 自然语言 报表 iHub 供应链 多源数据',
        'search_kicker': 'IMDA 公开材料 · 预期目标',
        'search_title': '物流：自然语言数据 Agent',
        'search_description': '用对话查询多源数据并生成报表；50% 是公开材料中的预期目标，不是已验证结果。',
    },
    {
        'id': 'pid',
        'href': 'case-manufacturing-pid-intelligence.html',
        'tags': ['manufacturing', 'data'],
        'kicker': 'ForFlow 团队实践 · 工业知识',
        'title': 'P&ID 智能化扩展工厂运营',
        'description': '把静态管线图纸变成可查询、可关联、可由工程师复核的运营知识网络。',
        'visual': {'type': 'media', 'src': 'assets/cases/thumb-manufacturing-pid.webp', 'label': '制造业'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '制造业 P&ID 工厂运营 工业知识资产化 工程师复核 图纸 查询 关联',
        'search_kicker': 'ForFlow 团队实践 · 工业知识',
        'search_title': '制造业：P&ID 智能化扩展工厂运营',
    },
    {
        'id': 'energy-optimization-agent',
        'href': 'case-energy-optimization-agent.html',
        'tags': ['manufacturing', 'data'],
        'kicker': '工业能效 · 合作场景材料',
        'title': '实时电价驱动的工厂能效优化 Agent',
        'description': '从电价、负荷和设备状态出发，拆解感知、预测、调度、执行与反馈闭环，以及自动控制必须守住的安全边界。',
        'visual': {'type': 'media', 'src': 'assets/cases/energy-optimization-agent-hero.png', 'label': '工厂智慧用能'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '工业能效 工厂 能源管理 能效优化 Agent 智能体 实时电价 电力现货 需求响应 源网荷储 EMS MES WMS APS OT IT Modbus OPC UA PROFINET PLC DCS LSTM Transformer SAC DQN PPO 负荷预测 光伏预测 电价预测 储能 SOC 冷冻站 空压站 COP 多目标优化 人工接管 安全约束',
        'search_kicker': '工业能效 · 合作场景材料',
        'search_title': '制造业：实时电价驱动的能效优化 Agent',
        'search_description': '保留工业协议、预测模型、多目标调度、设备约束和分阶段上线方法；合作名称与成效披露仍待项目方确认。',
    },
    {
        'id': 'healthcare-agent-roi',
        'href': 'case-healthcare-agent-roi.html',
        'tags': ['healthcare', 'service', 'data'],
        'kicker': 'ForFlow 团队实践 · 医疗 AI',
        'title': '医疗智能体的受限架构与验证方法',
        'description': '把就诊前中后和患者语音入口拆成可验收、可追踪、可升级人工的生产级流程。',
        'visual': {'type': 'media', 'src': 'assets/cases/healthcare-care-chain-sana-plain.png', 'label': '医疗工作流'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '医疗 医院 诊所 受限多智能体 ROI 患者语音 EHR EMR 保险验证 预约管理 SFT GRPO 临床记录 医疗编码 CPT ICD 就诊前 就诊中 就诊后 状态机 人工升级',
        'search_kicker': 'ForFlow 团队实践 · 医疗 AI',
        'search_title': '医疗：受限智能体架构与验证方法',
    },
    {
        'id': 'automotive-dfmea-ontology-agent',
        'href': 'case-automotive-dfmea-ontology-agent.html',
        'tags': ['automotive', 'manufacturing', 'data'],
        'kicker': 'ForFlow 工程方法 · 汽车知识',
        'title': '本体智能体如何重塑安全关键零部件 DFMEA',
        'description': '以 B 柱为例，把材料、工艺、失效机理和法规要求连成可推理、可追溯、可复评的风险情报系统。',
        'visual': {'type': 'media', 'src': 'assets/cases/automotive-dfmea-bpillar-hero.png', 'label': '汽车 DFMEA'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '汽车 汽车工程 B柱 B 柱 B-pillar 安全关键零部件 侧面碰撞 车顶抗压 安全带锚固 DFMEA FMEA 本体 Ontology 知识图谱 智能体 Agent AI RFLP 22MnB5 硼钢 热冲压 氢脆 疲劳 腐蚀 电偶腐蚀 粘接失效 失效模式 RPN AP ECO 工程变更 工程推理 知识流失 老师傅经验 组织记忆 经验断档 机构记忆 跨项目迁移 供应商教训 设计变更复评 FMVSS 214 FMVSS 216 Euro NCAP IIHS AIAG VDA',
        'search_kicker': 'ForFlow 工程方法 · 汽车知识',
        'search_title': '汽车：本体智能体重塑 B 柱 DFMEA',
        'search_description': '从电子表格 DFMEA 到工程本体推理，解释 AI 如何发现组合失效并沉淀组织知识。',
    },
    {
        'id': 'supply-chain-agentic-decision',
        'href': 'case-supply-chain-agentic-decision.html',
        'tags': ['retail', 'data', 'service'],
        'kicker': 'ForFlow 团队实践 · 供应链',
        'title': '多智能体 AI 如何将供应链数据转化为决策与行动',
        'description': '基于团队成员在原组织中积累的项目经验，讲清自然语言查询、异常钻取、根因归因和行动协同；匿名客户与测量边界按公开资料保留。',
        'visual': {'type': 'media', 'src': 'assets/cases/supply-chain-agentic-decision-hero.png', 'label': '供应链决策'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '供应链 零售 鞋服 库存 SKU 控制塔 control tower 多智能体 Agent 语义层 自然语言 SQL 履行率 渠道履行 订单 冻结 信用控制 工具网关 可观测性 决策 行动',
        'search_kicker': 'ForFlow 团队实践 · 供应链',
        'search_title': '供应链：多智能体 AI 把数据转化为行动',
        'search_description': '用团队过往项目经验解释自动查询、分析、根因归因和行动通知的 Agent 架构。',
    },
    {
        'id': 'financial-bda-document-automation',
        'href': 'case-financial-bda-document-automation.html',
        'tags': ['finance', 'data', 'service'],
        'kicker': 'ForFlow 工程方法 · 文档自动化',
        'title': '把金融文档提取接入可复核工作流',
        'description': '围绕银行对账单、税务文件和供应商合同，讲清字段蓝图如何把文档提取变成可复用、可复核的工作流。',
        'visual': {'type': 'media', 'src': 'assets/cases/financial-bda-document-automation-hero.png', 'label': '金融文档自动化'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '金融 文档 金融文档 字段蓝图 OCR IDP 智能文档处理 银行对账单 bank statement W-2 W2 1099-B 1099B 税务表格 供应商合同 vendor contract 结构化提取 JSON CSV 置信度 视觉定位 visual grounding 幻觉缓解 字段验证 会计 对账 税务 合同管理',
        'search_kicker': 'ForFlow 工程方法 · 文档自动化',
        'search_title': '金融：把文档提取接入可复核工作流',
        'search_description': '从四类金融文档到字段蓝图，说明如何提取、验证并接入会计、税务和合同工作流。',
    },
    {
        'id': 'vanguard-virtual-analyst',
        'href': 'case-vanguard-virtual-analyst.html',
        'tags': ['finance', 'data', 'service'],
        'kicker': 'ForFlow 团队实践 · 金融数据',
        'title': '先锋集团虚拟分析师：AI 就绪数据的八项原则',
        'description': '从 SQL 等待、指标口径和数据治理出发，说明金融企业如何把对话式 AI 建在可靠数据基础上。',
        'visual': {'type': 'media', 'src': 'assets/cases/vanguard-virtual-analyst-hero.png', 'label': '虚拟分析师'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '先锋集团 Vanguard 虚拟分析师 AI-ready data AI 就绪数据 金融分析师 SQL 自助分析 数据架构 数据产品 运营模式 元数据目录 语义层 业务元数据 技术元数据 示例库 回归测试 数据质量 变更控制 持续评估 知识图谱 RAG 合规 安全',
        'search_kicker': 'ForFlow 团队实践 · 金融数据',
        'search_title': '金融：先锋集团虚拟分析师与 AI 就绪数据',
        'search_description': '八项原则解释为什么企业对话式分析的关键不是换模型，而是数据产品、语义层、质量和持续评估。',
    },
    {
        'id': 'agent-evaluation-first',
        'href': 'case-agent-evaluation-first.html',
        'tags': ['service', 'data'],
        'kicker': 'ForFlow 工程方法 · Agent 评估',
        'title': '企业 Agent 上线前，先建立评估基线',
        'description': '从原型到生产的鸿沟、ADLC 飞轮、持续评估、可观测性和可评估架构。',
        'visual': {'type': 'media', 'src': 'assets/cases/agent-evaluation-first-hero.png', 'label': 'Agent 评估'},
        'link_label': '阅读案例 <b>↗</b>',
        'search': True,
        'search_text': '企业智能体 Agent AI Agent Evaluation 评估 评测 ADLC Agent Development Lifecycle 原型 生产可信赖 单元测试 非确定性 Prompt 变更 静默漂移 CI CD LLM-as-a-Judge 基准数据集 工具选择 参数提取 拒绝准确率 延迟 Token 可观测性 Trace OpenTelemetry 漂移检测 A/B测试 多智能体 解耦 Supervisor MCP A2A Gateway Policy 安全 个性化',
        'search_kicker': 'ForFlow 工程方法 · Agent 评估',
        'search_title': '企业 Agent：上线前先建立评估基线',
        'search_description': '解释企业智能体从 Demo 走向生产时，为什么要先建立评估基线、ADLC 飞轮、Trace 和可评估架构。',
    },
    {
        'tags': ['data', 'service'],
        'kicker': 'TSH 公开客户案例摘要',
        'title': 'Pension Lab：把单份文档处理从 15 分钟缩短到 40 秒',
        'description': 'TSH 原文报告使用 AI OCR 与敏感数据匿名化，将文档流程时间减少约 95%；本页不把它混写成投标 Agent。',
        'visual': {'type': 'art', 'class': 'case-art--paper', 'html': '<b>15min</b><span>→ 40s</span>'},
        'source_href': 'https://tsh.io/portfolio/pension-lab-ai-case-study',
        'source_label': '查看 TSH 原文 ↗',
    },
    {
        'tags': ['service'],
        'kicker': 'HR 服务 · 场景示例',
        'title': '员工制度与入职知识助手',
        'description': '把分散制度转为按权限检索、带引用的员工服务入口。',
        'visual': {'type': 'art', 'class': 'case-art--grid', 'html': '<b>HR</b><span>知识与服务</span>'},
        'status_label': '概念场景 · 非客户案例',
    },
]

SEARCH_TYPE_LABELS = {
    'category': '方案分类',
    'service': '企业服务',
    'resource': '资料',
    'case': '案例&博客',
}

SEARCH_CORE_ITEMS = [
    {
        'id': 'category-hrms',
        'type': 'category',
        'href': 'category-hrms.html',
        'kicker': '方案分类',
        'title': '人力资源与组织效率',
        'description': '招聘、入职、员工服务、培训、绩效与 HR 数据分析场景，包含优先级、证据链、人工复核和上线边界。',
        'action': '查看分类 →',
        'priority': 8,
        'keywords': ['人力资源', 'HR', '招聘', '入职', '员工', 'Agent', '培训', '绩效', '员工服务'],
    },
    {
        'id': 'ai-readiness-audit',
        'type': 'service',
        'href': 'ai-readiness-audit.html',
        'kicker': '企业服务',
        'title': 'AI 准备度审核',
        'description': '用 1–2 个工作日排清场景优先级、基础缺口和 30/90 天路线。',
        'action': '查看审核方式 →',
        'priority': 9,
        'keywords': ['AI 准备度', '审核', '场景优先级', '路线图', '30/90 天', '风险', '治理', '投资判断'],
    },
    {
        'id': 'service-agent-build',
        'type': 'service',
        'href': 'service-agent-build.html',
        'kicker': '企业服务',
        'title': '企业 Agent 与工作流',
        'description': '连接知识、系统、工具和人工审批，完成多步业务任务。',
        'action': '2 周验证起步 →',
        'priority': 8,
        'keywords': ['企业 Agent', '智能体', '搭建', 'RAG', '系统集成', '自动化', '工作流', '工具调用', '审批', '人工复核'],
    },
    {
        'id': 'service-data-governance',
        'type': 'service',
        'href': 'service-data-governance.html',
        'kicker': '企业服务',
        'title': 'AI 数据与知识治理',
        'description': '统一数据口径、知识来源、质量、管道与权限。',
        'action': '查看详情 →',
        'priority': 7,
        'keywords': ['数据治理', '数据工程', 'RAG', '知识库', '指标', '质量', '权限', '口径', '数据资产'],
    },
    {
        'id': 'service-ai-enablement',
        'type': 'service',
        'href': 'service-ai-enablement.html',
        'kicker': '企业服务',
        'title': 'AI 采用与团队赋能',
        'description': '把零散试用变成可衡量的团队能力。',
        'action': '查看详情 →',
        'priority': 6,
        'keywords': ['AI 赋能', '采用', '组织', '团队', '绩效', '场景诊断', '试点', '扩展'],
    },
    {
        'id': 'service-ai-training',
        'type': 'service',
        'href': 'service-ai-training.html',
        'kicker': '企业服务',
        'title': 'AI 实战培训',
        'description': '按角色和岗位定制，学完即用。',
        'action': '查看详情 →',
        'priority': 6,
        'keywords': ['AI 培训', '课程', '管理层', '业务', '技术', '提示词', '工作坊', '角色训练'],
    },
    {
        'id': 'resource-playbook',
        'type': 'resource',
        'href': 'playbook.html',
        'kicker': '在线手册',
        'title': '企业生成式 AI 实战手册',
        'description': 'GenAI、RAG、买还是建、风险治理和落地步骤。',
        'action': '阅读手册 →',
        'priority': 6,
        'keywords': ['GenAI', '生成式 AI', 'playbook', '手册', 'RAG', '风险', '买还是建'],
    },
    {
        'id': 'contact',
        'type': 'resource',
        'href': 'contact.html',
        'kicker': '联系方式',
        'title': '联系 ForFlow 萬維流形',
        'description': 'ForFlow 萬維流形联系方式：邮件联系 hello@forflow.ai，北京、上海、深圳可沟通。',
        'action': '查看联系方式 →',
        'priority': 7,
        'keywords': ['联系', '联系方式', '邮箱', '咨询', '合作', '万维流形', 'ForFlow', '北京', '上海', '深圳'],
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
    if item.get('href'):
        link_html = f'<span class="{"text-link" if item.get("featured") else "case-card-link"}">{item.get("link_label", "查看案例 →")}</span>'
    elif item.get('source_href'):
        link_html = f'<a class="case-card-source" href="{esc(item["source_href"])}" target="_blank" rel="noopener noreferrer">{esc(item.get("source_label", "查看公开来源 ↗"))}</a>'
    else:
        link_html = f'<span class="case-card-status">{esc(item.get("status_label", "摘要案例 · 详情整理中"))}</span>'
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
    <nav aria-label="快捷链接"><a href="playbook.html">企业 AI 手册</a><a href="cases.html">案例&博客</a><a href="contact.html">联系</a></nav>
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
            <div class="mega-panel-intro"><span>ENTERPRISE SERVICES</span><h2>先看现在缺哪一步。</h2><p>问题还没排清，先做准备度审核；缺口明确，就直接进入团队采用、数据、工作流或培训。</p><a href="index.html#services">查看全部服务 {ff_icon('i-arrow')}</a></div>
            <div class="mega-link-grid">
              <a class="mega-link" href="ai-readiness-audit.html"{current_attr(active == 'ai-readiness-audit')}><span class="mega-icon">{ff_icon('i-compass')}</span><span><b>AI 准备度审核</b><small>先判断价值、基础、风险和 30/90 天路线</small></span><em>01</em></a>
              <a class="mega-link" href="service-ai-enablement.html"{current_attr(active == 'service-ai-enablement')}><span class="mega-icon">{ff_icon('i-layers')}</span><span><b>AI 采用与团队赋能</b><small>把零散试用变成岗位方法与采用指标</small></span><em>02</em></a>
              <a class="mega-link" href="service-data-governance.html"{current_attr(active == 'service-data-governance')}><span class="mega-icon">{ff_icon('i-data')}</span><span><b>AI 数据与知识治理</b><small>统一口径、质量、权限与知识来源</small></span><em>03</em></a>
              <a class="mega-link" href="service-agent-build.html"{current_attr(active == 'service-agent-build')}><span class="mega-icon">{ff_icon('i-agent')}</span><span><b>企业 Agent 与工作流</b><small>连接知识、系统、工具和人工审批</small></span><em>04</em></a>
              <a class="mega-link" href="service-ai-training.html"{current_attr(active == 'service-ai-training')}><span class="mega-icon">{ff_icon('i-training')}</span><span><b>AI 实战培训</b><small>管理层、业务与技术团队分角色训练</small></span><em>05</em></a>
            </div>
          </div>
        </li>
        <li class="mega-item">
          <button class="mega-trigger{current_class(tools_active)}" type="button" data-mega-trigger aria-expanded="false">场景与工具 {ff_icon('i-chevron')}</button>
          <div class="mega-panel mega-panel--tools" data-mega-panel>
            <div class="mega-panel-intro"><span>TOOLS &amp; SCENARIOS</span><h2>从业务问题进入，工具放在后面。</h2><p>方向还不清楚，可以做诊断；已有问题，直接看场景或搜索资料。</p><a href="navigator.html">立即开始诊断 {ff_icon('i-arrow')}</a></div>
            <div class="mega-feature-stack">
              <a class="mega-feature" href="navigator.html"{current_attr(active in {'navigator', 'navigator-results'})}><span>{ff_icon('i-compass')}</span><div><b>AI 场景诊断</b><small>3 分钟排出一个建议起点</small></div><em>开始</em></a>
              <a class="mega-feature" href="category-hrms.html"{current_attr(active == 'category-hrms')}><span>{ff_icon('i-people')}</span><div><b>HR 场景地图</b><small>招聘、入职、培训、员工服务与绩效</small></div><em>浏览</em></a>
              <button class="mega-feature search-trigger" type="button"><span>{ff_icon('i-search')}</span><div><b>全站搜索</b><small>查找服务、场景、资料、案例与博客</small></div><em>搜索</em></button>
            </div>
          </div>
        </li>
        <li class="mega-item">
          <button class="mega-trigger{current_class(insights_active)}" type="button" data-mega-trigger aria-expanded="false">手册与洞察 {ff_icon('i-chevron')}</button>
          <div class="mega-panel mega-panel--insights" data-mega-panel>
            <a class="mega-editorial" href="playbook.html"{current_attr(active == 'playbook')}><span class="mega-editorial-kicker">FEATURED GUIDE</span><strong>企业生成式 AI<br>实战手册</strong><p>从基础、商业价值和买或建，到风险、安全与实施路线。</p><span class="mega-editorial-link">在线阅读 {ff_icon('i-arrow')}</span></a>
            <div class="mega-insight-list">
              <a href="cases.html"><span>{ff_icon('i-cases')}</span><div><b>案例&博客</b><small>按问题、过程和结果阅读案例与文章</small></div></a>
              <a href="case-wren-kitchens.html"><span>{ff_icon('i-growth')}</span><div><b>Wren Kitchens 案例</b><small>从紧急扩容到长期技术合作</small></div></a>
              <a href="document-viewer.html?doc=playbook"{current_attr(active == 'document-viewer')}><span>{ff_icon('i-document')}</span><div><b>PDF 在线阅读</b><small>在浏览器中查看与下载参考文件</small></div></a>
            </div>
          </div>
        </li>
        <li><a href="cases.html"{current_attr(cases_active)}>案例&博客</a></li>
        <li><a href="contact.html"{current_attr(active == 'contact')}>联系</a></li>
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
  <details{' open' if insights_active else ''}><summary>手册与洞察 <span>04</span></summary><div class="mobile-subnav"><a href="playbook.html"{current_attr(active == 'playbook')}>企业 AI 实战手册</a><a href="cases.html">案例&博客</a><a href="document-viewer.html?doc=playbook"{current_attr(active == 'document-viewer')}>PDF 阅读器</a></div></details>
  <a href="cases.html"{current_attr(cases_active)}>案例&博客 <span>05</span></a>
  <a href="contact.html"{current_attr(active == 'contact')}>联系 <span>06</span></a>
  <a class="btn btn--green" href="navigator.html">开始 AI 场景诊断 <span aria-hidden="true">→</span></a>
</div>'''

def footer():
    return '''
<footer class="site-footer">
  <div class="container footer-main">
    <div class="footer-brand">
      <img src="assets/forflow-lockup-transparent.png" alt="ForFlow 萬維流形">
      <p>判断投入，验证结果；<br>跑通后再扩大。</p>
    </div>
  <div class="footer-col"><h3>企业服务</h3>
      <a href="ai-readiness-audit.html">AI 准备度审核</a>
      <a href="service-ai-enablement.html">AI 采用与团队赋能</a>
      <a href="service-data-governance.html">AI 数据与知识治理</a>
      <a href="service-agent-build.html">企业 Agent 与工作流</a>
      <a href="service-ai-training.html">AI 实战培训</a>
    </div>
    <div class="footer-col"><h3>工具与资源</h3>
      <a href="navigator.html">AI 场景诊断</a>
      <a href="playbook.html">企业 AI 实战手册</a>
      <a href="category-hrms.html">HR AI 场景地图</a>
      <a href="document-viewer.html?doc=playbook">PDF 阅读器</a>
    </div>
    <div class="footer-col"><h3>案例&博客与行动</h3>
      <a href="cases.html">案例&博客</a>
      <a href="case-wren-kitchens.html">Wren Kitchens 案例</a>
      <button class="footer-search search-trigger" type="button">全站搜索</button>
      <a href="navigator.html">开始诊断</a>
      <a href="contact.html">联系</a>
    </div>
  </div>
  <div class="container footer-bottom"><span>© 2026 ForFlow.ai 萬維流形</span><span>企业 AI 场景工程 · 诊断、案例与交付路径持续更新</span><a href="privacy.html">隐私说明</a></div>
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
  <link rel="stylesheet" href="visual-system.css?v={VISUAL_SYSTEM_VERSION}">
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
    old_footer = soup.find('footer', class_='site-footer')
    if old_footer:
        old_footer.extract()
    new_footer = BeautifulSoup(footer(), 'html.parser').find('footer')
    main = soup.find('main')
    if main:
        main.insert_after(new_footer)
    else:
        soup.body.append(new_footer)
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
    visual = soup.find('link', href=lambda value: value and value.split('?')[0] == 'visual-system.css')
    if not visual:
        visual = soup.new_tag('link', rel='stylesheet', href=f'visual-system.css?v={VISUAL_SYSTEM_VERSION}')
        style = soup.find('link', href=lambda value: value and value.split('?')[0] == 'styles.css')
        if style:
            style.insert_after(visual)
        else:
            soup.head.append(visual)
    else:
        visual['href'] = f'visual-system.css?v={VISUAL_SYSTEM_VERSION}'
    for script in soup.find_all('script', src=True):
        src = script.get('src', '')
        if src.split('?')[0] == 'script.js':
            script['src'] = f'script.js?v={SCRIPT_VERSION}'
    path.write_text(str(soup), encoding='utf-8')

def version_asset_links():
    for path in ROOT.glob('*.html'):
        soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
        changed = False
        footer_note = soup.select_one('.footer-bottom span:last-child')
        if footer_note and footer_note.get_text(strip=True) == '响应式企业网站原型 · CMS / CRM / 报价接口已预留':
            footer_note.string = '企业 AI 场景工程 · 诊断、案例与交付路径持续更新'
            changed = True
        for sheet in soup.find_all('link', rel=lambda x: x and 'stylesheet' in x):
            href = sheet.get('href', '')
            if href.split('?')[0] == 'styles.css':
                sheet['href'] = f'styles.css?v={CSS_VERSION}'
                changed = True
        visual = soup.find('link', href=lambda value: value and value.split('?')[0] == 'visual-system.css')
        if not visual:
            visual = soup.new_tag('link', rel='stylesheet', href=f'visual-system.css?v={VISUAL_SYSTEM_VERSION}')
            style = soup.find('link', href=lambda value: value and value.split('?')[0] == 'styles.css')
            if style:
                style.insert_after(visual)
            else:
                soup.head.append(visual)
            changed = True
        elif visual.get('href') != f'visual-system.css?v={VISUAL_SYSTEM_VERSION}':
            visual['href'] = f'visual-system.css?v={VISUAL_SYSTEM_VERSION}'
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
patch_existing('ai-readiness-audit.html', 'ai-readiness-audit')

def polish_readiness_page():
    path = ROOT / 'ai-readiness-audit.html'
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    def set_two_line(selector, first, second):
        node = soup.select_one(selector)
        if not node:
            return
        node.clear()
        node.append(first)
        node.append(soup.new_tag('br'))
        node.append(second)

    hero_lead = soup.select_one('.commercial-hero .commercial-lead')
    if hero_lead:
        hero_lead.string = '我们会检查真实流程、可用数据、现有系统和责任边界，排出可以启动的场景，也说明哪些条件要先补。最后给管理层一份 30/90 天行动路线。'
    set_two_line('#dimensions .section-title', '“准备好了吗”，', '要看六类证据。')
    set_two_line('#deliverables .section-title', '审核结束后，', '管理层会拿到这些材料。')
    set_two_line('.service-evidence .section-title', '准备度不能靠感觉，', '要看得见证据。')
    set_two_line('.commercial-final-cta h2', '把候选项目、条件缺口', '和投入顺序一次排清。')
    self_check_title = soup.select_one('.audit-self-intro h2')
    if self_check_title:
        self_check_title.clear()
        self_check_title.append('做一轮自测，')
        self_check_title.append(soup.new_tag('br'))
        self_check_title.append('先看卡在哪一层。')
    faq_lead = soup.select_one('.service-faq .section-lead')
    if faq_lead:
        faq_lead.string = '这里说明审核范围、参与人和结果，避免被误解成技术演示。'
    score = soup.select_one('.rf-score')
    if score:
        label = score.find('small')
        value = score.select_one('.rf-score-head strong')
        state = score.select_one('.rf-score-head span')
        if label:
            label.string = 'SAMPLE READINESS OUTPUT'
        if value:
            value.string = 'A2'
        if state:
            state.string = '示例状态 · 可启动受控试点'
        score['aria-label'] = 'AI 准备度审核示例输出，不代表当前企业评级'
    path.write_text(str(soup), encoding='utf-8')

polish_readiness_page()

def polish_navigator_page():
    path = ROOT / 'navigator.html'
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    set_mobile_title(soup, '.navigator-hero-inner h1', ['哪件事适合', '交给 AI？'])
    set_mobile_title(soup, '#step-1-title', ['日常工作里，', '哪件事最该改？'])

    hero_intro = soup.select_one('.navigator-hero-inner > p')
    if hero_intro:
        hero_intro.string = '回答几道题，大约 3 分钟。我们会给出一条建议起点，也会列出开始前还缺的条件，方便带回团队讨论。'

    description = soup.select_one('meta[name="description"]')
    if description:
        description['content'] = '用 3 分钟判断哪件事适合交给 AI，并得到一条建议起点。'

    navigator_copy = {
        '#step-1-title': '日常工作里，哪件事最该改？',
        '#step-2-title': '这次最想看到什么变化？',
        '#step-3-title': '你对数据和部署有哪些要求？',
        '#step-4-title': '你的第一版场景建议。',
    }
    for selector, text in navigator_copy.items():
        heading = soup.select_one(selector)
        if heading and selector not in {'#step-1-title'}:
            heading.string = text

    panel_copy = [
        '选 1–2 个最影响效率、质量或客户体验的环节。',
        '选 1–2 个最重要的结果，再告诉我们团队现在准备到哪一步。',
        '这些条件会影响能否快速试点，以及哪些方案一开始就不合适。',
        '我们会把你的回答整理成可讨论的起点，并列出试点前还需要确认的条件。',
    ]
    for panel, text in zip(soup.select('.step-panel'), panel_copy):
        intro = panel.select_one('.step-panel-head > p')
        if intro:
            intro.string = text

    sidebar_rows = [
        ('业务挑战', '选择最需要改善的环节'),
        ('价值与准备度', '明确目标和现状'),
        ('部署边界', '约束、周期和数据条件'),
        ('生成场景建议', '确认起点与下一步动作'),
    ]
    for item, (title, text) in zip(soup.select('.step-item'), sidebar_rows):
        strong = item.select_one('.step-copy strong')
        span = item.select_one('.step-copy span')
        if strong:
            strong.string = title
        if span:
            span.string = text

    trust = soup.select_one('.sidebar-trust')
    if trust:
        icon = trust.select_one('.trust-icon')
        title = trust.find('h3')
        body = trust.find('p')
        if icon:
            icon.string = '依据'
        if title:
            title.string = '诊断口径'
        if body:
            body.string = '这份结果用于项目前的初步判断，会列出业务问题、数据边界、负责人和验收指标。正式试点仍需结合真实流程和样本确认。'

    tag_texts = [
        '诊断 01 · 业务挑战',
        '诊断 02 · 价值与准备度',
        '诊断 03 · 部署边界',
        '诊断 04 · 生成建议',
    ]
    for tag, text in zip(soup.select('.step-panel-head .step-tag'), tag_texts):
        tag.string = text

    for label in soup.find_all('label'):
        label_text = label.get_text(strip=True)
        if label_text in {'预计首批使用团队', '预计首批使用团队（选填）'}:
            label.string = '预计首批使用团队（选填）'
        elif label_text in {'所属行业', '所属行业（内容映射占位）', '所属行业（选填）'}:
            label.string = '所属行业（选填）'
        elif label_text in {'需要连接的系统数量', '需要连接的系统数量（占位）', '需要连接的系统数量（选填）'}:
            label.string = '需要连接的系统数量（选填）'
        elif label_text in {'是否已有业务负责人', '是否已有业务负责人（选填）'}:
            label.string = '是否已有业务负责人（选填）'

    result_intro = soup.select_one('.step-panel[data-step="4"] .step-panel-head p')
    if result_intro:
        result_intro.string = '我们会把你的回答整理成可讨论的起点，并列出试点前还需要确认的条件。'
    disclaimer = soup.select_one('.result-disclaimer')
    if disclaimer:
        disclaimer.string = '建议用于项目沟通前的初筛：正式进入试点前，还需要补充真实流程、样本数据、权限边界、负责人和验收指标。'

    path.write_text(str(soup), encoding='utf-8')

polish_navigator_page()

# Add the four-SKU section into the existing homepage frame.
index_path = ROOT / 'index.html'
soup = BeautifulSoup(index_path.read_text(encoding='utf-8'), 'html.parser')
content_stack = soup.find('div', class_='content-stack')
if content_stack and not soup.find(id='services'):
    service_section = BeautifulSoup('''
<section id="services" data-section>
  <div class="section-head">
    <div><p class="eyebrow">Enterprise services</p><h2 class="section-title">五项服务，<br>对应五类问题。</h2></div>
    <p class="section-lead">方向不清，从准备度审核开始；缺口明确，直接进入采用、数据、工作流或培训。</p>
  </div>
  <div class="sku-grid">
    <a class="sku-card" href="ai-readiness-audit.html" data-reveal><span class="sku-no">01</span><small>1–2 天 · 投入判断</small><h3>AI 准备度审核</h3><p>排清场景优先级、基础缺口和 30/90 天路线。</p><span class="card-link"><span>查看审核方式</span><span>→</span></span></a>
    <a class="sku-card" href="service-ai-enablement.html" data-reveal><span class="sku-no">02</span><small>4–6 周 · 采用与改变</small><h3>AI 采用与团队赋能</h3><p>把个人零散试用变成岗位方法、团队规范和采用指标。</p><span class="card-link"><span>查看服务流程与 FAQ</span><span>→</span></span></a>
    <a class="sku-card" href="service-data-governance.html" data-reveal><span class="sku-no">03</span><small>分阶段 · 数据与知识</small><h3>AI 数据与知识治理</h3><p>统一数据口径、知识来源、质量和权限。</p><span class="card-link"><span>查看服务流程与 FAQ</span><span>→</span></span></a>
    <a class="sku-card" href="service-agent-build.html" data-reveal><span class="sku-no">04</span><small>2 周验证 · 工作流实施</small><h3>企业 Agent 与工作流</h3><p>连接知识、系统、工具和人工审批，完成真实任务。</p><span class="card-link"><span>查看服务流程与 FAQ</span><span>→</span></span></a>
    <a class="sku-card" href="service-ai-training.html" data-reveal><span class="sku-no">05</span><small>分角色 · 真实任务训练</small><h3>AI 实战培训</h3><p>让管理层、业务和技术团队分别练自己的决策与任务。</p><span class="card-link"><span>查看服务流程与 FAQ</span><span>→</span></span></a>
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
    <div class="result-video-card">
      <video controls muted loop playsinline autoplay preload="metadata" poster="assets/forflow-brand-motion-poster.jpg" aria-label="ForFlow 萬維流形品牌动效">
        <source src="assets/forflow-brand-motion.mp4" type="video/mp4">你的浏览器不支持视频播放。
      </video>
    </div>
    <div class="results-intro">
      <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="navigator.html">AI 场景诊断</a><span>/</span><strong>推荐结果</strong></nav>
      <p class="eyebrow">Recommended routes</p>
      <h1>你的第一版<br>场景建议。</h1>
      <p>我们按业务目标、现有条件和部署要求排了顺序。你可以带着这份结果继续讨论，不必现在就决定买什么工具。</p>
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
    <div class="section-head"><div><p class="eyebrow">Recommended solutions</p><h2 class="section-title">从第一条值得试的<br>流程开始。</h2></div><p class="section-lead">你可以按三种方式看结果：“最匹配”看问题是否对路，“最快见效”看能否马上启动，“基础优先”先补最影响落地的条件。选定一条后，再确认数据边界、负责人和验收方式。</p></div>
    <div class="results-panel">
      <aside class="sort-sidebar" role="group" aria-label="方案排序"><small>排序方式</small><button class="is-active" data-sort="match" aria-pressed="true">最匹配</button><button data-sort="speed" aria-pressed="false">最快见效</button><button data-sort="foundation" aria-pressed="false">基础优先</button></aside>
      <div class="solution-list">
        <div class="mobile-sort"><button type="button" data-mobile-sort-toggle aria-expanded="false">排序：<span>最匹配</span> ↓</button><div data-mobile-sort-menu aria-hidden="true"><button data-sort="match" aria-pressed="true">最匹配</button><button data-sort="speed" aria-pressed="false">最快见效</button><button data-sort="foundation" aria-pressed="false">基础优先</button></div></div>
        <article class="solution-card" data-solution="audit" data-rank-match="5" data-rank-speed="1" data-rank-foundation="1">
          <div class="solution-main"><div class="solution-topline"><span class="solution-index">01</span><button class="favorite-btn" type="button" aria-label="收藏方案">♡</button></div><h3>AI 准备度审核</h3><p>适合问题和想法已经出现，但场景顺序、数据条件、风险和投入范围还没有排清的团队。</p><div class="micro-tags"><span>场景顺序</span><span>基础缺口</span><span>投入判断</span></div><div class="feature-columns"><ul><li>候选流程与业务目标梳理</li><li>数据、系统和治理条件检查</li><li>主要风险与停止条件</li></ul><ul><li>30 / 90 天行动路线</li><li>负责人和下一步材料清单</li><li>适合进入哪项服务的建议</li></ul></div></div>
          <div class="solution-side"><small>建议起步</small><strong>1–2 个工作日</strong><span>先完成投入与条件判断</span><a class="btn btn--green" href="ai-readiness-audit.html">查看详情 →</a></div>
        </article>
        <article class="solution-card" data-solution="agent" data-rank-match="1" data-rank-speed="1" data-rank-foundation="3">
          <div class="solution-main"><div class="solution-topline"><span class="solution-index">01</span><button class="favorite-btn" type="button" aria-label="收藏方案">♡</button></div><h3>企业 Agent 与工作流</h3><p>适合把知识查询、文档处理、客户或员工服务接入真实流程，并保留权限、审批与人工复核。</p><div class="micro-tags"><span>智能工作流</span><span>带来源的知识检索</span><span>系统集成</span></div><div class="feature-columns"><ul><li>流程与高价值用例拆解</li><li>2 周可工作的验证版本</li><li>权限、审计与异常回退</li></ul><ul><li>连接知识库、API 与业务系统</li><li>正式实施路线图</li><li>运行监控与持续优化</li></ul></div></div>
          <div class="solution-side"><small>建议起步</small><strong>2 周验证</strong><span>随后按里程碑实施</span><a class="btn btn--green" href="service-agent-build.html">查看详情 →</a></div>
        </article>
        <article class="solution-card" data-solution="data" data-rank-match="2" data-rank-speed="4" data-rank-foundation="1">
          <div class="solution-main"><div class="solution-topline"><span class="solution-index">02</span><button class="favorite-btn" type="button" aria-label="收藏方案">♡</button></div><h3>AI 数据与知识治理</h3><p>适合资料散落、指标不一致、数据权限不清，或准备建设企业知识库、分析与带来源知识检索的组织。</p><div class="micro-tags"><span>数据资产</span><span>质量规则</span><span>AI 数据层</span></div><div class="feature-columns"><ul><li>数据资产与风险盘点</li><li>指标、主数据和质量规则</li><li>数据管道与访问机制</li></ul><ul><li>权限、血缘与审计</li><li>知识检索与智能体访问层</li><li>分阶段建设路线</li></ul></div></div>
          <div class="solution-side"><small>建议起步</small><strong>2–4 周盘点</strong><span>按优先域分阶段建设</span><a class="btn btn--green" href="service-data-governance.html">查看详情 →</a></div>
        </article>
        <article class="solution-card" data-solution="enablement" data-rank-match="3" data-rank-speed="2" data-rank-foundation="2">
          <div class="solution-main"><div class="solution-topline"><span class="solution-index">03</span><button class="favorite-btn" type="button" aria-label="收藏方案">♡</button></div><h3>AI 采用与团队赋能</h3><p>适合已有零散 AI 试用，但缺少统一方法、内部负责人、使用规范和可衡量业务结果的团队。</p><div class="micro-tags"><span>组织采用</span><span>真实任务</span><span>指标体系</span></div><div class="feature-columns"><ul><li>现状盘点与工具设置</li><li>真实项目实战陪跑</li><li>内部负责人培养</li></ul><ul><li>采用率与绩效指标</li><li>最佳实践与使用规范</li><li>规模化推广建议</li></ul></div></div>
          <div class="solution-side"><small>典型周期</small><strong>4–6 周</strong><span>以真实业务任务为主线</span><a class="btn btn--green" href="service-ai-enablement.html">查看详情 →</a></div>
        </article>
        <article class="solution-card" data-solution="training" data-rank-match="4" data-rank-speed="3" data-rank-foundation="4">
          <div class="solution-main"><div class="solution-topline"><span class="solution-index">04</span><button class="favorite-btn" type="button" aria-label="收藏方案">♡</button></div><h3>AI 实战培训</h3><p>适合需要让管理层会判断、业务团队会使用、技术团队会落地，并建立统一数据与使用边界的企业。</p><div class="micro-tags"><span>管理层</span><span>业务实战</span><span>安全规范</span></div><div class="feature-columns"><ul><li>岗位与场景定制课程</li><li>提示词与工作流实战</li><li>数据安全和责任边界</li></ul><ul><li>场景共创与行动计划</li><li>课后资料包</li><li>可选 30 天陪跑</li></ul></div></div>
          <div class="solution-side"><small>建议形式</small><strong>1–3 天</strong><span>可叠加 30 天陪跑</span><a class="btn btn--green" href="service-ai-training.html">查看详情 →</a></div>
        </article>
      </div>
    </div>
  </div>
</section>
<section class="result-report" id="email-report" data-requires-data-api>
  <div class="container result-report__inner">
    <div class="result-report__copy">
      <p class="eyebrow">Email this result</p>
      <h2>把这份结果<br>发到邮箱。</h2>
      <p>留下工作邮箱，我们会发送当前诊断摘要。邮箱只用于发送报告和后续联系，不会写入诊断答案或匿名事件。</p>
    </div>
    <form class="lead-form lead-form--report" data-lead-form data-source-type="assessment_report">
      <input type="hidden" name="assessment_id" data-assessment-id>
      <input type="hidden" name="service_interest" value="AI 场景诊断">
      <label class="form-honeypot" aria-hidden="true">公司网址<input type="text" name="website" tabindex="-1" autocomplete="off"></label>
      <label><span>工作邮箱 *</span><input type="email" name="email" autocomplete="email" placeholder="name@company.com" required></label>
      <label><span>公司或团队</span><input type="text" name="company" autocomplete="organization" maxlength="160" placeholder="选填"></label>
      <label class="lead-consent"><input type="checkbox" name="consent" required><span>我同意 ForFlow 按<a href="privacy.html">《隐私说明》</a>保存信息并发送本次诊断结果。</span></label>
      <button class="btn btn--green" type="submit">发送诊断结果 <span aria-hidden="true">→</span></button>
      <p class="lead-status" data-lead-status role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
<section class="final-cta"><div class="container final-cta-inner"><div><h2>把结果变成一张<br>可讨论的项目卡。</h2><p>带上当前流程、样本数据和希望改善的指标，进行一次 30 分钟项目梳理。</p></div><div class="final-cta-actions"><a class="btn" href="contact.html?topic=audit">带着结果预约沟通 →</a><a class="btn btn--ghost" href="navigator.html">重新诊断</a></div></div></section>
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
    <section id="opportunity" data-section class="playbook-section"><header><span class="chapter-no">02</span><div><p class="eyebrow">Growth opportunities</p><h2>{mobile_title('四类企业价值，', '先选一项', '作为主指标。')}</h2></div></header><div class="benefit-grid"><article><span>01</span><h3>提高效率</h3><p>自动完成内容初稿、资料查找、重复问答和数据整理，让员工回到需要判断和创造力的工作。</p></article><article><span>02</span><h3>个性化体验</h3><p>根据客户资料与偏好，在合适渠道提供更相关的产品、服务和沟通。</p></article><article><span>03</span><h3>降低成本</h3><p>减少人工复制、重复处理和跨系统查找，优化资源分配。</p></article><article><span>04</span><h3>增加收入</h3><p>通过更快响应、个性化推荐、精准营销和新服务形成增长机会。</p></article></div><div class="callout"><strong>企业视角</strong><p>不要同时追求所有收益。首个项目最好只设一个主指标，例如处理时长、一次解决率、转化率或错误率，再配两个保护指标，如合规和客户满意度。</p></div></section>
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
def service_page(
    slug, title, eyebrow, subtitle, intro, pains, outcomes, scope, process,
    deliverables, faqs, related, *, number, icon, method, method_note, facts,
    best_fit, not_fit, insight_lead, outcome_title, outcome_lead, scope_title,
    scope_lead, process_title, process_lead, deliverable_title,
    deliverable_lead, faq_lead, cta_title, cta_lead, case_evidence,
    consult_materials, contact_topic, pilot=False, hero_asset=None,
    technical_asset=None,
):
    pain_html=''.join(f'<article><span>{i:02d}</span><h3>{h}</h3><p>{p}</p></article>' for i,(h,p) in enumerate(pains,1))
    outcome_html=''.join(f'<article><span>{i:02d}</span><h3>{h}</h3><p>{p}</p></article>' for i,(h,p) in enumerate(outcomes,1))
    scope_html=''.join(f'<article><span class="service-glyph">{i:02d}</span><h3>{h}</h3><p>{p}</p></article>' for i,(h,p) in enumerate(scope,1))
    process_html=''.join(f'<li><span>{i:02d}</span><div><h3>{h}</h3><p>{p}</p><small>阶段结果：{result}</small></div></li>' for i,(h,p,result) in enumerate(process,1))
    deliver_html=''.join(f'<article><small>{kind}</small><h3>{h}</h3><p>{p}</p></article>' for kind,h,p in deliverables)
    faq_html=''.join(f'<article class="faq-item"><button class="faq-question" type="button" aria-expanded="false"><span>{q}</span><span class="plus">+</span></button><div class="faq-answer"><div><p>{a}</p></div></div></article>' for q,a in faqs)
    related_html=''.join(f'<a href="{href}"><span>{i:02d}</span><div><h3>{name}</h3><p>{desc}</p></div><b>→</b></a>' for i,(href,name,desc) in enumerate(related,1))
    fact_html=''.join(f'<div><dt>{value}</dt><dd>{label}</dd></div>' for value,label in facts)
    best_fit_html=''.join(f'<li><strong>{h}</strong><span>{p}</span></li>' for h,p in best_fit)
    not_fit_html=''.join(f'<li><strong>{h}</strong><span>{p}</span></li>' for h,p in not_fit)
    def evidence_card(item):
        href,kind,case_title,proof,lesson,boundary=item
        external=' target="_blank" rel="noopener"' if href.startswith('http') else ''
        badge='公开资料' if href.startswith('http') else 'ForFlow 团队实践'
        return f'<a class="service-evidence-card" href="{href}"{external}><div class="service-evidence-meta"><span>{kind}</span><small>{badge}</small></div><h3>{case_title}</h3><p>{proof}</p><dl><div><dt>这项服务可借鉴</dt><dd>{lesson}</dd></div><div><dt>经验边界</dt><dd>{boundary}</dd></div></dl><span class="service-evidence-link">查看完整案例与依据 →</span></a>'
    evidence_html=''.join(evidence_card(item) for item in case_evidence)
    consult_material_html=''.join(f'<li>{item}</li>' for item in consult_materials)
    pilot_class = ' service-page--pilot' if pilot else ''
    hero_visual = (
        f'<figure class="service-pilot-photo" data-asset-role="business-photo" data-reveal>'
        f'<img src="{hero_asset}" alt="业务负责人正在核对 Agent 工作流、审批点和异常处理" '
        f'fetchpriority="high" decoding="async">'
        f'<figcaption>先把任务、系统和人工责任画清楚，再进入验证。</figcaption></figure>'
        if pilot and hero_asset else
        f'<div class="service-hero-art" data-code="{number}" data-reveal><span class="service-hero-icon">{ff_icon(icon)}</span><div class="service-orbit"></div><div class="service-hero-card"><small>FORFLOW / {number}</small><strong>{method}</strong><span>{method_note}</span></div></div>'
    )
    technical_visual = (
        f'<figure class="service-pilot-diagram" data-asset-role="technical-diagram">'
        f'<img src="{technical_asset}" alt="企业 Agent 从任务定义、系统连接、人工审批、评估到生产反馈的受控路径" '
        f'loading="lazy" decoding="async">'
        f'<figcaption><strong>一条生产路径：</strong>生产中的异常和失败样本，会回到评估环节继续修正。</figcaption></figure>'
        if pilot and technical_asset else ''
    )
    body=f'''
<section class="service-hero"><div class="container service-hero-grid"><div class="service-hero-copy" data-reveal><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="index.html#services">企业服务</a><span>/</span><strong>{title}</strong></nav><p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="service-hero-lead">{subtitle}</p><div class="hero-actions"><a class="btn btn--green" href="contact.html?topic={contact_topic}">预约 30 分钟初步沟通 →</a><a class="btn btn--ghost" href="#fit">查看适用条件</a></div><dl class="service-facts">{fact_html}</dl></div>{hero_visual}</div></section>
<div class="service-local-nav-wrap"><nav class="container service-local-nav" aria-label="本页内容"><a href="#fit">适用条件</a><a href="#why-now">常见卡点</a><a href="#outcomes">项目结果</a><a href="#scope">服务范围</a><a href="#process">开展方式</a><a href="#deliverables">交付材料</a><a href="#evidence">团队经验</a><a href="#consult">开始咨询</a><a href="#faq">常见问题</a></nav></div>
<section class="service-fit-check section-pad" id="fit"><div class="container"><div class="section-head"><div><p class="eyebrow">A quick check</p><h2 class="section-title">这项服务现在<br>适不适合？</h2></div><p class="section-lead">如果下面的启动条件还不具备，先补条件会更省时间。</p></div><div class="service-fit-columns"><article class="service-fit-card service-fit-card--yes" data-reveal><span>适合现在做</span><ul>{best_fit_html}</ul></article><article class="service-fit-card service-fit-card--wait" data-reveal><span>暂时不建议</span><ul>{not_fit_html}</ul></article></div></div></section>
<section class="service-insight section-pad surface" id="why-now"><div class="container"><div class="section-head"><div><p class="eyebrow">Where it gets stuck</p><h2 class="section-title">{intro}</h2></div><p class="section-lead">{insight_lead}</p></div><div class="problem-grid">{pain_html}</div></div></section>
<section class="service-transformation section-pad section-ink" id="outcomes" data-visual-role="proof"><div class="container"><div class="section-head"><div><p class="eyebrow eyebrow--light">What changes</p><h2 class="section-title">{outcome_title}</h2></div><p class="section-lead">{outcome_lead}</p></div>{technical_visual}<div class="outcome-grid">{outcome_html}</div></div></section>
<section class="service-scope section-pad" id="scope"><div class="container"><div class="section-head"><div><p class="eyebrow">Scope</p><h2 class="section-title">{scope_title}</h2></div><p class="section-lead">{scope_lead}</p></div><div class="scope-grid">{scope_html}</div></div></section>
<section class="service-process-section section-pad surface" id="process"><div class="container service-process"><div class="process-intro"><p class="eyebrow">How it works</p><h2 class="section-title section-title--small">{process_title}</h2><p>{process_lead}</p></div><ol class="process-list">{process_html}</ol></div></section>
<section class="service-deliverables section-pad" id="deliverables"><div class="container"><div class="section-head"><div><p class="eyebrow">Deliverables</p><h2 class="section-title">{deliverable_title}</h2></div><p class="section-lead">{deliverable_lead}</p></div><div class="deliverable-grid">{deliver_html}</div></div></section>
<section class="service-evidence section-pad surface" id="evidence"><div class="container"><div class="section-head"><div><p class="eyebrow">Team experience</p><h2 class="section-title">这些经验，<br>如何用于你的项目。</h2></div><p class="section-lead">这里收录了团队成员参与过的项目、公开案例和产品资料，用来说明我们如何工作。新项目仍要用你的目标、数据和验收标准重新判断。</p></div><div class="service-evidence-layout"><div class="service-evidence-list">{evidence_html}</div><aside class="service-consult-card" id="consult" aria-label="咨询 {title}"><small>FIRST CONVERSATION · 30 MIN</small><h3>用 30 分钟确认范围。</h3><p>带上下面几项基本信息，我们会判断问题是否适合这项服务，以及下一步需要什么材料。</p><ul>{consult_material_html}</ul><div class="service-consult-actions"><a class="btn btn--green" href="contact.html?topic={contact_topic}">预约这项服务 →</a><a href="mailto:hello@forflow.ai">hello@forflow.ai</a></div><span>沟通只做范围判断，不现场承诺方案或报价。</span></aside></div></div></section>
<section class="service-faq section-pad surface" id="faq"><div class="container faq-layout"><div><p class="eyebrow">FAQ</p><h2 class="section-title section-title--small">合作前，通常会问这些。</h2><p class="section-lead">{faq_lead}</p></div><div class="faq-list">{faq_html}</div></div></section>
<section class="related-services section-pad section-ink"><div class="container"><div class="section-head"><div><p class="eyebrow eyebrow--light">Related paths</p><h2 class="section-title">当前条件还不够，<br>可以先走这些路径。</h2></div></div><div class="related-service-list">{related_html}</div></div></section>
<section class="final-cta"><div class="container final-cta-inner"><div><h2>{cta_title}</h2><p>{cta_lead}</p></div><a class="btn" href="contact.html?topic={contact_topic}">预约服务沟通 →</a></div></section>'''
    body_class = f'service-page {slug}{pilot_class}'
    (ROOT/f'{slug}.html').write_text(page(title,subtitle,slug,body,body_class),encoding='utf-8')

service_page(
 'service-ai-enablement','AI 采用与团队赋能','AI Adoption & Enablement',
 '选一个团队和几项高频任务，把零散试用变成可复用的岗位方法；再用实际数据判断要不要扩大。',
 '工具已经进了公司，用法却还没有变成团队的工作方法。',
 [('经验留在个人手里','少数人用得顺，但方法说不清、教不会，也无法交给新人。'),('任务没有起点数据','只知道“感觉更快”，没有时间、返工或质量基线，复盘时说不清效果。'),('规则和工作脱节','安全政策写在文档里，员工面对真实资料时仍不知道哪些能放、哪些要复核。')],
 [('跑通一组岗位任务','试点团队有一套能直接照着做、也能由主管检查的方法。'),('边界进入日常工作','数据使用、事实核验、人工审批和异常升级写进任务步骤。'),('效果有记录','使用频次、完成时长、返工和质量变化可以回看。'),('扩不扩大有依据','管理层能选择推广、调整或暂停，不靠热情做决定。')],
 [('试点团队与任务选择','确定一个团队、3–5 个代表性岗位和几项高频任务。'),('工具、账号与资料边界','复用已批准工具，配置账号、权限、模板和可用资料。'),('岗位方法共创','把提示、输入要求、输出格式、核验和审批写成操作步骤。'),('真实任务试行','在日常工作中使用并记录时间、返工、质量和异常。'),('主管与 Champion 机制','让内部负责人能答疑、抽查结果并组织复盘。'),('推广与治理建议','说明哪些做法可复制，哪些仍需数据、系统或管理动作。')],
 [('选定试点与基线','访谈负责人和代表用户，选择任务并记录当前用时、质量和返工。','试点任务表、参与人和基线'),('配置环境与边界','确认工具、账号、资料范围、核验要求和不能使用的内容。','可用环境与使用边界'),('共创岗位方法','用企业自己的材料跑任务，逐步收紧输入、输出、检查和审批。','首批岗位任务模板'),('两周真实试行','让团队在日常工作中使用，记录成功、放弃和返工原因。','使用记录与问题清单'),('复盘并决定下一步','比较基线和试行结果，确认推广、调整或暂停。','采用复盘与扩展决定')],
 [('盘点','AI 采用基线表','谁在用、用在哪、当前效果和主要阻力。'),('方法','岗位任务手册','任务步骤、提示模板、资料要求、核验与审批。'),('资料包','可复用模板包','首批任务模板、检查清单、示例和常见错误。'),('决策','采用复盘报告','指标变化、问题清单、推广条件和下一阶段建议。')],
 [('没有技术团队也能做吗？','可以。业务负责人提供真实任务并判断结果；只有涉及系统接入或账号权限时，才需要 IT 或现有技术伙伴参加。'),('为什么不直接做一次培训？','一次课能建立概念，但很难改变日常工作。这里会把方法放进真实任务，并连续观察使用、质量和阻力。'),('需要统一更换所有 AI 工具吗？','不需要。先用企业已经批准的工具；现有工具明显做不到时，再讨论替换。'),('效果怎么量？','启动前记录任务用时、返工、质量和使用情况。试行结束后看变化，也记录员工放弃使用的原因。'),('员工不愿意用怎么办？','先选真正困扰团队的任务，让员工参与设计方法。试行中如果收益不明显或步骤更麻烦，会直接记录并调整。'),('能不能直接推广到全公司？','不建议从全公司起步。先在一个团队跑通，再判断相近岗位能否复用；不同部门可能需要不同资料、规则和指标。')],
 [('service-ai-training.html','AI 实战培训','需要先建立共同语言时，从分角色训练开始。'),('service-agent-build.html','企业 Agent 与工作流','任务方法已经稳定，再考虑接入系统。'),('service-data-governance.html','AI 数据与知识治理','资料、口径和权限不稳时，先补数据与知识基础。')],
 number='02', icon='i-layers', method='选岗位 → 做样板 → 真实试行 → 决定推广',
 method_note='从一个团队开始，把“有人会用”变成“团队有方法”。',
 facts=[('4–6 周','典型首轮周期'),('1 个团队','建议起步范围'),('负责人 + 3–5 人','企业侧核心参与')],
 best_fit=[('已经有工具，使用差异很大','有人每天使用，有人完全不用，团队没有共同方法。'),('个人试用有效，准备推广','希望把少数人的经验整理成岗位模板和主管可检查的步骤。'),('管理层需要真实采用数据','要用时间、质量、返工和使用情况决定是否继续投入。')],
 not_fit=[('只需要一次全员宣讲','这种需求更适合 AI 实战培训，不需要做四到六周陪跑。'),('没有团队负责人投入时间','没人选任务、看结果、处理阻力，外部顾问无法替代内部责任。'),('工具和数据边界尚未批准','先确认能用什么工具、能处理哪些资料，再开始真实任务试行。')],
 insight_lead='问题通常不在员工会不会写提示词，而在任务、资料、检查和负责人没有连起来。',
 outcome_title='一个团队跑通，<br>再决定要不要推广。',
 outcome_lead='项目会留下一组被真实使用过的方法，以及继续推广、调整或暂停的依据。',
 scope_title='围绕一个团队，<br>把方法做实。',
 scope_lead='首轮不追求覆盖所有岗位。任务越具体，越容易看清收益和阻力。',
 process_title='五步跑完一轮<br>真实采用。',
 process_lead='典型周期 4–6 周。每一步都留下可交接材料，方便团队自己继续。',
 deliverable_title='团队可以继续使用的<br>四份材料。',
 deliverable_lead='不交一摞通用讲义。交付物直接对应试点团队的任务、规则和复盘。',
 faq_lead='团队投入、衡量方式和推广边界都在这里说明。',
 cta_title=mobile_title('让一个团队', '先跑出方法。'),
 cta_lead='告诉我们团队、工具和最常见的三项任务，我们会先判断适不适合做采用陪跑。',
 case_evidence=[
   ('cases.html#jan-elly','教育内容 · 团队采用','把单篇内容制作从 18 小时缩短到 30 分钟','公开材料显示，团队把选题、写作、SEO 和培训放进同一条工作流程，而不是只给员工一个生成工具。','选择真实任务，记录时间变化，再把个人用法整理成团队可复用的方法。','这是公开案例摘要，页面不把该结果归因于 ForFlow；正式发布前仍需复核原始来源与授权。'),
   ('https://sanalabs.com/customers/learning/spotify','Spotify · 学习与采用','把数字学习和线下实践接起来','Spotify 的 L&D 负责人介绍了 AI Learning Festival：员工展示日常工作中的真实用法，平台承载知识学习，线下环节用于练习；其公开说法是全公司大部分人已经使用 Sana 内容。','组织采用不靠一次宣讲，要让真实岗位案例被看见、被练习，并形成内部同伴带教。','这是 Sana 发布的客户访谈，采用表述来自 Spotify 受访者，没有披露统一的效率或业务基线。'),
 ],
 consult_materials=['一个明确的试点团队和负责人','团队最常见的 3–5 项任务','已批准的工具、资料和数据边界','希望改善的用时、质量或返工指标'],
 contact_topic='enablement',
)

service_page(
 'service-data-governance','AI 数据与知识治理','AI-ready Data & Knowledge',
 '围绕一个业务域，把来源、口径、质量、权限和更新责任说清楚，让报表、知识检索和 Agent 使用同一套可信输入。',
 mobile_title('数据很多，', '可信的输入却不够。'),
 [('同一问题有多个答案','销售额、客户、库存或项目状态在不同报表里口径不一，会议先花时间争数字。'),('知识库看似齐全，实际不敢用','制度、产品和项目资料版本混在一起，没人能确认哪份有效、谁负责更新。'),('AI 接入后才发现权限不清','系统能连上，但哪些字段能用、能留多久、谁能看到没有明确规则。')],
 [('核心资产有地图','知道数据和文档在哪里、谁负责、什么用途可以调用。'),('口径与来源有顺序','关键指标和知识问题都有权威来源，冲突时知道以谁为准。'),('质量问题能被处理','缺失、延迟、重复和过期有检查方式、阈值和负责人。'),('AI 访问有边界','RAG、分析和 Agent 按权限取数，调用与变更可以追踪。')],
 [('业务域与资产盘点','围绕客户、产品、供应链或 HR 等一个业务域，梳理系统、报表、文件和知识库。'),('指标与概念口径','统一关键指标、主数据对象、计算逻辑和业务解释。'),('知识来源与版本','明确权威文档、有效期、引用方式、更新流程和归档规则。'),('质量检查与异常处理','为缺失、重复、延迟和冲突设置检查、阈值与处理责任。'),('权限、血缘与审计','记录数据从哪里来、经过什么处理、谁能访问和如何留痕。'),('RAG 与 Agent 访问层','为检索、自然语言问数和工具调用设计可控接口与返回规则。')],
 [('确定业务问题与范围','从一个报表争议、知识问答或 Agent 计划倒推要治理的数据与文档。','业务域、使用场景和范围'),('盘点来源、口径与责任','访谈业务和 IT，核对系统、报表、文件、权限和现有问题。','资产清单与问题台账'),('定权威来源和规则','确认指标定义、文档版本、质量阈值、更新人和访问条件。','口径表、来源层级与责任表'),('做一条可用链路','选一个高价值问题，打通采集、清洗、检索或接口调用。','可验证的数据或知识链路'),('评审并排建设顺序','根据价值、风险和改造成本确定下一批数据域和系统工作。','分期路线与治理节奏')],
 [('地图','数据与知识责任地图','数据源、文档、负责人、用途、敏感等级和当前问题。'),('规则','指标与知识口径表','计算方式、权威来源、版本、有效期和冲突处理。'),('控制','质量与访问规则','检查阈值、异常处理、权限、调用日志和审计要求。'),('路线','分期建设清单','先处理哪些问题、依赖哪些系统、何时能支持目标场景。')],
 [('是不是要先建一个很大的数据平台？','不需要。先围绕最影响当前业务或 AI 场景的一个业务域，把来源、口径、质量和访问跑通，再决定要不要扩展平台。'),('现有 ERP、CRM 和 BI 还能继续用吗？','可以。先利用现有系统和接口，只有在能力或维护成本明显不合适时才讨论替换。'),('文档和知识库也算治理范围吗？','算。AI 经常依赖制度、产品和项目资料，这些内容同样需要版本、权限、有效期和更新责任。'),('多久能看到结果？','2–4 周通常能完成一个业务域的盘点、规则和优先级。真正打通多少链路，取决于数据质量和系统接口。'),('怎么判断数据是否能给 AI 用？','至少要知道来源、负责人、权限、更新频率、质量和敏感等级，并且能通过稳定、可记录的方式访问。'),('治理会不会变成填表项目？','如果规则没有进入报表、知识更新或系统调用，就没有意义。我们只保留会影响使用、质量和责任的字段。')],
 [('service-agent-build.html','企业 Agent 与工作流','数据和权限清楚后，把它们接进真实任务。'),('service-ai-enablement.html','AI 采用与团队赋能','让业务团队会使用并持续反馈数据问题。'),('ai-readiness-audit.html','AI 准备度审核','范围还不清楚时，先排场景和基础缺口。')],
 number='03', icon='i-data', method='定来源 → 统一口径 → 设质量线 → 控制访问',
 method_note='不从大平台开始，从一个业务问题和一条可用链路开始。',
 facts=[('2–4 周','首轮盘点与设计'),('1 个业务域','建议起步范围'),('业务负责人 + IT','企业侧核心参与')],
 best_fit=[('同一指标总在会议里争论','报表、系统和部门各有口径，需要明确权威来源。'),('知识检索或 Agent 被资料拖住','文档过期、版本混乱、权限不清，回答无法被信任。'),('准备连接 ERP、CRM 或 BI','需要先确认字段、接口、质量和访问责任。')],
 not_fit=[('希望几周内重建整个数据平台','首轮只解决一个业务域和目标场景，不能替代大型平台重构。'),('业务侧没有数据负责人','IT 可以管理系统，但无法替业务决定指标含义和权威来源。'),('只想先买向量库或知识库工具','工具不能替代来源、版本、质量和权限判断。')],
 insight_lead='AI 会放大现有数据问题。先把权威来源和责任说清楚，技术选型才有意义。',
 outcome_title='让数据和知识<br>可以被放心调用。',
 outcome_lead='一个业务问题需要稳定、可追踪的输入，治理工作围绕这条链路展开。',
 scope_title='数据、文档和权限，<br>放在同一张图里。',
 scope_lead='结构化数据和非结构化知识一起看，避免报表能用、知识库却失控。',
 process_title='从一个业务问题<br>打通一条链路。',
 process_lead='责任和规则确定后，再做必要的管道、检索或接口工作。',
 deliverable_title='把“数据有问题”<br>变成可执行清单。',
 deliverable_lead='每份材料都对应一个负责人、使用场景或系统动作，不做空泛的数据蓝图。',
 faq_lead='治理范围、现有系统和业务责任都在这里说明。',
 cta_title=mobile_title('先把一个业务域', '说清楚。'),
 cta_lead='告诉我们最常争议的指标、最常用的知识资料或准备接入的 AI 场景。',
 case_evidence=[
   ('case-vanguard-virtual-analyst.html','金融分析 · AI-ready data','先锋集团虚拟分析师','ForFlow 团队成员做过这类虚拟分析师与数据基础工作：把数天的查询等待缩短到分钟级，同时补齐数据责任、语义层、权限和持续评估。','先治理业务口径、元数据和访问规则，再让自然语言查询进入关键分析流程。','这是团队成员加入 ForFlow 前积累的项目经验。原项目数字按公开资料保留，进入新项目后仍需重新建立基线。'),
   ('case-automotive-dfmea-ontology-agent.html','汽车工程 · 知识资产','把 DFMEA 从静态表格变成可追溯知识链','ForFlow 团队把材料、工艺、失效机理、法规和工程变更连成知识链，保留关系、来源和复评责任。','为高价值知识定义对象、关系、版本、证据来源和专家复核，让检索结果可以追溯。','这是 ForFlow 团队成员的过往工程经验；企业结论仍要回到自己的设计、试验和质量数据。'),
 ],
 consult_materials=['一个最想先治理的业务域','争议最多的指标或高频知识问题','当前系统、文档与数据来源','权限、更新和业务解释的负责人'],
 contact_topic='data',
)

service_page(
 'service-agent-build','企业 Agent 与工作流','Enterprise Agents & Workflows',
 '先选一条真实流程，验证 Agent 能不能稳定完成任务。我们会把知识、系统操作和人工审批接起来，用真实样本检查结果。',
 'Agent 能回答问题，不代表它能进入真实流程。',
 [('任务被切成很多人工接力','员工在邮件、表格和多个系统之间复制信息，任何一步漏掉都要返工。'),('Demo 能跑，异常没人接','正常样本看起来顺利，遇到资料缺失、权限不足或系统失败就停住。'),('责任边界没有进入设计','Agent 能调用哪些工具、哪些动作必须审批、出错后谁处理没有写清。')],
 [('一条真实流程可以运行','Agent 使用真实知识和系统完成任务，结果会写回流程。'),('权限和人工接管明确','每个工具、动作和审批点都有范围，异常能回到人手里。'),('质量有评估基线','常见任务、边界样本和失败情况可以重复测试。'),('生产投入有决定','企业知道继续实施需要哪些接口、数据、预算和运营责任。')],
 [('知识检索与引用','从制度、产品、项目和文档中找答案，并显示可核验来源。'),('工具与系统调用','连接 ERP、CRM、工单、邮件、数据库或内部 API。'),('多步任务编排','按顺序收集信息、调用工具、等待审批、更新状态和通知相关人。'),('人工审批与接管','为高风险动作、低置信度结果和异常设置人工处理。'),('评估、日志与成本','记录任务成功、工具调用、失败原因、延迟和模型成本。'),('部署与运行设计','确定云端、混合或私有环境，以及监控、回退和版本管理。')],
 [('界定任务和成功标准','选定一个流程，写清输入、输出、不能做的事和当前基线。','任务定义与验收标准'),('拆流程、系统和异常','逐步核对工具、接口、权限、人工节点和失败处理。','流程图与系统依赖表'),('搭建受控验证版本','接入必要知识和工具，让 Agent 跑通真实样本。','可工作的验证版本'),('用基准样本测试','覆盖常见任务、边界输入、应拒绝和应转人工的情况。','评估结果与失败清单'),('做上线或停止决定','说明生产化所需改造、运营责任、预算和剩余风险。','实施路线与进入决定')],
 [('定义','Agent 任务与边界说明','处理什么、不处理什么、成功标准、工具和人工责任。'),('验证','可工作的流程版本','使用真实知识、样本、系统调用和审批节点完成任务。'),('证据','评估集与测试报告','常见样本、边界样本、失败原因、质量、延迟和成本。'),('路线','生产实施与运营方案','接口、权限、部署、监控、回退、团队和分期计划。')],
 [('Agent 和普通聊天机器人有什么区别？','聊天机器人主要生成回答；Agent 还会在授权范围内查知识、调用工具、更新系统和等待审批，因此需要更严格的权限、评估和回退。'),('两周一定能上线生产吗？','两周通常用于做受控验证，目标是跑通一条真实流程并暴露问题。生产上线取决于接口、权限、数据敏感度和异常复杂度。'),('一定要私有化部署吗？','不一定。根据数据分类、监管、延迟和成本选择云端、混合或私有环境。敏感数据可以留在企业内部。'),('怎么避免 Agent 做错事？','先缩小职责和工具权限，再加输入输出校验、人工审批、日志、预算限制和异常回退。没有任何设计能保证零错误。'),('可以连接现有 ERP、CRM 或工单系统吗？','可以，前提是系统有可用 API 或其他可控集成方式。项目开始时会先确认权限、频率、失败处理和测试环境。'),('验证后一定要继续实施吗？','不一定。验证的价值就是支持继续、调整或停止的决定；效果不足或风险过高时，停止也是有效结果。')],
 [('service-data-governance.html','AI 数据与知识治理','资料、口径或权限不稳时，先补输入基础。'),('ai-readiness-audit.html','AI 准备度审核','还没选定流程时，先排场景和投入顺序。'),('service-ai-enablement.html','AI 采用与团队赋能','流程上线后，让团队会用、会复盘、会反馈。')],
 number='04', icon='i-agent', method='拆任务 → 接工具 → 设审批 → 用失败样本测试',
 method_note='把一条流程做到可运行、可接管、可评估，再讨论规模化。',
 facts=[('约 2 周','首轮受控验证'),('1 条流程','建议起步范围'),('负责人 + 接口 + 样本','企业侧关键准备')],
 best_fit=[('任务高频，步骤基本清楚','员工每天重复查资料、录系统、发通知或追状态。'),('系统有接口或可控集成方式','至少能在测试环境连接必要知识和工具。'),('失败后可以由人接住','有明确审批、转人工或回退方式，不让 Agent 单独承担高风险决定。')],
 not_fit=[('流程本身还在争议中','如果团队连现有步骤和责任都没有共识，先做流程梳理。'),('希望 Agent 自主做高风险最终决定','授信、录用、诊断等决定需要人负责，不能把责任交给模型。'),('拿不到系统、样本或权限','没有真实输入和可控工具，只能做演示，无法判断是否值得实施。')],
 insight_lead='真正影响上线的是任务边界、系统权限、异常处理和人工责任。',
 outcome_title='两周后，企业要拿到继续、调整或停止的依据。',
 outcome_lead='验证结果会说明这条流程能否稳定运行，还缺哪些接口、数据和运营条件。',
 scope_title='只接通完成这条流程需要的能力。',
 scope_lead='不默认上多 Agent 或大平台。先把知识、工具、审批和回退接稳。',
 process_title='用五步完成一次受控验证。',
 process_lead='正常样本要跑，资料缺失、权限不足和系统失败也要专门测试。',
 deliverable_title='工作版本和评估证据一起交付。',
 deliverable_lead='企业可以看到 Agent 做了什么、哪里失败，以及为什么值得继续或应该停。',
 faq_lead='这里说明验证周期、生产边界和失败处理。',
 cta_title=mobile_title('开始前，', '请准备这四项信息。'),
 cta_lead='一条高频流程、当前步骤、需要连接的系统，以及不可接受的结果。',
 case_evidence=[
   ('case-financial-bda-document-automation.html','金融文档 · 受控自动化','把文档提取接入复核与下游流程','ForFlow 团队用字段蓝图、质量检查和人工复核把文档提取接进会计、税务和合同流程，重点是让结构化结果能继续使用。','从一种高频文档和一条下游流程起步，明确字段、失败样本、人工复核和写回边界。','这是团队成员的过往工程方法。准确率和效率要用企业自己的文档样本重新测试。'),
   ('case-agent-evaluation-first.html','企业 Agent · 评估先行','定义成功，才让 Agent 进入生产','ForFlow 的评估方法把基准样本、工具调用、拒绝边界、生产 Trace 和失败样本回流接成一套可重复测试的流程。','试点阶段准备常见样本、边界样本和应转人工样本，避免把演示效果当成上线结论。','页面中的阈值和数字来自团队过往工程实践，用于说明方法；新项目需要按自己的风险和容错标准重新设定。'),
 ],
 consult_materials=['一条高频且步骤基本清楚的流程','当前步骤、异常和人工审批点','需要连接的系统、接口或测试环境','真实样本、成功标准和不可接受结果'],
 contact_topic='agent',
 pilot=True,
 hero_asset='assets/service-agent/forflow-agent-workflow-hero-v1.png',
 technical_asset='assets/service-agent/forflow-agent-workflow-system-v1.png',
)

service_page(
 'service-ai-training','AI 实战培训','Role-based AI Training',
 '管理层练投入判断，业务团队练岗位任务，技术团队练接入与评估。课程使用企业自己的材料，不做一套课讲给所有人。',
 mobile_title('听懂 AI 不难，', '难的是回到岗位后', '知道怎么做。'),
 [('所有人听同一套内容','管理层想知道怎么投，员工想知道怎么做，技术团队关心怎么接；一堂通用课很难同时回答。'),('演示很精彩，课后用不上','案例和工具离真实工作太远，员工回到岗位仍不知道从哪项任务开始。'),('边界只停在口号','员工知道“注意数据安全”，却不会判断一份客户表、合同或会议纪要能不能放进工具。')],
 [('管理层能讨论投入','会用业务价值、准备度和风险判断项目，不再只比较模型和工具。'),('业务团队完成真实练习','每个角色都用自己的材料跑任务，现场看输入、输出和核验。'),('技术团队知道配合什么','理解数据、接口、权限、评估和部署中需要提前准备的条件。'),('课后有下一步','形成可以继续使用的任务模板、规则和 30 天行动清单。')],
 [('管理层决策工作坊','场景价值、买或建、投入顺序、治理责任和停止条件。'),('业务岗位实战','用文档、分析、客服、营销、HR 等真实任务练习。'),('技术与数据专题','RAG、Agent、权限、评估、接口和运行要求。'),('工具与资料使用边界','数据分类、外部工具、版权、事实核验和敏感内容处理。'),('场景共创练习','把一个业务问题拆成任务、输入、输出、人工判断和验收方式。'),('课后 30 天跟进','答疑、任务复盘、模板修订和内部带教支持。')],
 [('课前确认角色和任务','访谈负责人，了解参与人、工具环境、数据政策和希望解决的问题。','分组方案与练习任务'),('准备企业化练习材料','选择可用资料，必要时脱敏，按角色设计案例和模板。','课程、案例与练习环境'),('分角色训练与现场实作','概念只讲够用的部分，把主要时间留给真实任务和复盘。','完成的岗位练习与问题记录'),('共同讨论边界和行动','把数据、核验、审批和升级规则落到具体任务。','使用边界与 30 天行动'),('可选课后跟进','观察实际使用，答疑并修订模板，避免课程停在当天。','复盘记录与模板更新')],
 [('课程','分角色课程与练习','管理层、业务和技术团队各自对应的问题、案例和任务。'),('模板','岗位任务练习包','输入要求、提示模板、输出格式、核验和审批清单。'),('规则','AI 使用边界初稿','数据、版权、事实核验、敏感内容和责任处理。'),('行动','30 天行动清单','下一批任务、负责人、使用频次和复盘安排。')],
 [('完全没用过 AI 的团队也适合吗？','适合。会先说明够用的基础概念和安全边界，再通过岗位任务逐步上手。'),('可以用企业自己的资料练吗？','可以，但要先确认资料分类。敏感内容只能在批准环境中使用，或者先脱敏、改成练习样本。'),('管理层和员工上同一门课吗？','不会完全相同。管理层关注投入和风险，业务团队关注任务与质量，技术团队关注架构、评估和运行。'),('怎么避免“学完就忘”？','现场完成真实练习，课后留下任务模板、负责人和 30 天行动；需要时可以加跟进复盘。'),('只做半天工作坊可以吗？','可以，适合管理层对齐或项目启动。若目标是改变日常工作，建议加入岗位实作和课后跟进。'),('培训会直接做出 PoC 吗？','培训可以完成场景拆解或小型技术练习，但生产 PoC 需要另行确认系统、数据、权限和评估范围。')],
 [('service-ai-enablement.html','AI 采用与团队赋能','培训后把方法放进真实工作，并连续观察采用。'),('service-agent-build.html','企业 Agent 与工作流','场景和任务清楚后，验证系统接入。'),('playbook.html','企业 AI 实战手册','用于课前阅读和内部讨论。')],
 number='05', icon='i-training', method='按角色分组 → 用真实材料练 → 当场复盘 → 课后行动',
 method_note='少讲通用概念，多练企业自己的任务和判断。',
 facts=[('0.5–3 天','常见课程与工作坊'),('分角色小组','建议组织方式'),('可用材料 + 工具环境','企业侧关键准备')],
 best_fit=[('管理层和团队缺少共同语言','对 AI 能做什么、该投多少、哪里有风险理解不一致。'),('已经批准工具，但员工不会落到岗位','需要用真实文档、分析或服务任务练出第一套方法。'),('准备启动试点','希望项目开始前对齐目标、数据边界、人工责任和验收方式。')],
 not_fit=[('想让所有人听同一场两小时讲座','可以做通识分享，但无法同时解决不同角色的真实问题。'),('希望培训替代流程、数据或系统改造','课程能发现问题，不能单独修好接口、数据质量或生产流程。'),('没有批准环境，也不能提供练习样本','没有可操作材料时只能讲概念，实战价值会很低。')],
 insight_lead='培训有没有用，取决于参与人是否能用自己的材料完成一项任务，而不是听了多少概念。',
 outcome_title='下课时，手里要有<br>能继续用的东西。',
 outcome_lead='每个角色带走自己的任务模板、边界和下一步，不靠课后重新摸索。',
 scope_title='同一家公司，<br>按角色教不同内容。',
 scope_lead='可组合半天工作坊、岗位实作和 30 天跟进，不默认全套购买。',
 process_title='课前看任务，<br>课堂做任务。',
 process_lead='参与人的真实任务和可用资料决定课程内容。',
 deliverable_title='课程结束，<br>留下四类可用材料。',
 deliverable_lead='讲义只是其中一部分，更重要的是岗位模板、使用边界和行动安排。',
 faq_lead='参与人、练习材料、工具环境和课后目标都在这里说明。',
 cta_title=mobile_title('先说清楚谁来学，', '回去要做什么。'),
 cta_lead='告诉我们参与角色、可用工具和最想练的任务，我们会建议课程拆分和准备材料。',
 case_evidence=[
   ('https://sanalabs.com/products/sana-learn/solutions/leadership-development','领导力发展 · 产品能力参考','管理者在真实谈话前练一次','Sana Learn 把 AI 辅导、困难对话角色扮演、岗位变化触发学习、企业领导原则和技能看板放在同一条发展路径中。','管理者培训应围绕反馈、绩效沟通、团队调整等真实时刻设计练习，并把企业自己的领导原则放进反馈标准。','这是供应商产品页面，不是独立效果研究；功能和成效主张应与客户案例、实际试用和采购验证分开看。'),
   ('https://sanalabs.com/customers/learning/brex','Brex · 内容生产与学习','31 分钟完成一门课程','Brex 运营学习负责人在 Sana 客户访谈中称，他用 31 分钟创建课程，并表示团队生产力提升到原来的两到三倍。','培训项目既要看学习体验，也要记录课程制作时间、参与人能否自主创建内容和课后工作变化。','数字来自供应商发布的客户证言，未提供独立测量方法，不能直接作为 ForFlow 项目目标或收益承诺。'),
 ],
 consult_materials=['参与角色、人数和希望解决的问题','企业已经批准使用的 AI 工具','最想在课堂完成的真实任务','可用、可脱敏或需要替换的练习材料'],
 contact_topic='training',
)

category_body='''
<section class="category-hero hr-map-hero"><div class="container category-hero-grid"><div data-reveal><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>HR 场景地图</strong></nav><p class="eyebrow">HR scenario map</p><h1>HR AI<br>场景地图</h1><p>不从“哪个工具最热”开始，而是沿着招聘、入职、服务、发展、绩效和组织分析这条员工旅程，判断哪些任务适合买、哪些值得定制、哪些必须保留人工判断。</p><div class="category-stats"><span><b>6</b> 个优先场景</span><span><b>2–6 周</b> 起步周期</span><span><b>人工复核</b> 默认保留</span></div><div class="hr-hero-actions"><a class="btn btn--green" href="#scenarios">查看场景单元 →</a><a class="btn btn--ghost" href="navigator.html?challenge=hr">做 3 分钟诊断</a></div></div><div class="category-hero-card hr-map-preview" data-reveal><span class="category-icon">HR</span><h2><span class="mobile-title-line">把员工旅程</span><span class="mobile-title-line">拆成六段。</span></h2><ol><li><b>招</b><span>需求、JD、候选人沟通</span></li><li><b>入</b><span>制度、IT、岗位知识</span></li><li><b>服</b><span>问答、工单、转人工</span></li><li><b>育</b><span>培训、陪练、能力证据</span></li><li><b>评</b><span>材料、反馈、复核边界</span></li><li><b>析</b><span>指标、趋势、组织风险</span></li></ol></div></div></section>
<section class="hr-journey section-pad"><div class="container"><div class="section-head"><div><p class="eyebrow">Journey first</p><h2 class="section-title">先看 HR 工作流，再决定 AI 进入哪里。</h2></div><p>HR 场景不是一个“聊天机器人入口”。每个任务都要先明确业务对象、系统数据、人工责任和可验收证据，再决定用现成工具、知识助手、流程 Agent 还是分析 Agent。</p></div><div class="hr-stage-strip" aria-label="按员工旅程筛选 HR 场景"><button class="is-active" type="button" data-hr-stage-filter="all">全部旅程</button><button type="button" data-hr-stage-filter="recruit">招聘</button><button type="button" data-hr-stage-filter="onboard">入职</button><button type="button" data-hr-stage-filter="service">员工服务</button><button type="button" data-hr-stage-filter="develop">发展绩效</button><button type="button" data-hr-stage-filter="analytics">组织分析</button></div><div class="hr-journey-map" aria-label="HR AI 场景旅程地图">
<article data-hr-stage-card="recruit"><span>01</span><h3>招聘前置</h3><p>岗位需求、JD、招聘渠道和面试标准先统一。</p><dl><div><dt>AI 适合</dt><dd>生成初稿、对齐口径、整理候选材料。</dd></div><div><dt>人要判断</dt><dd>岗位必要性、录用标准、公平性风险。</dd></div></dl><button class="hr-stage-link" type="button" data-hr-stage-filter="recruit">查看招聘场景</button></article>
<article data-hr-stage-card="recruit"><span>02</span><h3>候选人沟通</h3><p>把邮件、短信、日程和反馈放入可追踪流程。</p><dl><div><dt>AI 适合</dt><dd>改写话术、补齐信息、生成面试问题。</dd></div><div><dt>人要判断</dt><dd>候选人体验、敏感拒信、最终筛选。</dd></div></dl><button class="hr-stage-link" type="button" data-hr-stage-filter="recruit">查看招聘场景</button></article>
<article data-hr-stage-card="onboard"><span>03</span><h3>入职与知识</h3><p>新员工反复问制度、福利、IT、岗位资料。</p><dl><div><dt>AI 适合</dt><dd>权限检索、引用来源、按岗位给答案。</dd></div><div><dt>人要判断</dt><dd>制度解释、例外审批、资料有效期。</dd></div></dl><button class="hr-stage-link" type="button" data-hr-stage-filter="onboard">查看入职场景</button></article>
<article data-hr-stage-card="service"><span>04</span><h3>员工服务</h3><p>高频问答、表单、工单和跨部门协同不断打断 HR。</p><dl><div><dt>AI 适合</dt><dd>收集信息、创建工单、提醒 SLA。</dd></div><div><dt>人要判断</dt><dd>员工关系、争议事项、异常升级。</dd></div></dl><button class="hr-stage-link" type="button" data-hr-stage-filter="service">查看服务场景</button></article>
<article data-hr-stage-card="develop"><span>05</span><h3>发展与绩效</h3><p>培训、反馈和绩效材料分散在多个系统和会议里。</p><dl><div><dt>AI 适合</dt><dd>整理证据、生成学习路径、提示缺口。</dd></div><div><dt>人要判断</dt><dd>评价、晋升、薪酬和个人发展决定。</dd></div></dl><button class="hr-stage-link" type="button" data-hr-stage-filter="develop">查看发展绩效</button></article>
<article data-hr-stage-card="analytics"><span>06</span><h3>组织分析</h3><p>人力指标口径不一，管理层很难快速看到趋势。</p><dl><div><dt>AI 适合</dt><dd>自然语言问数、异常解释、管理摘要。</dd></div><div><dt>人要判断</dt><dd>业务解释、敏感人群分析、行动方案。</dd></div></dl><button class="hr-stage-link" type="button" data-hr-stage-filter="analytics">查看分析场景</button></article>
</div></div></section>
<section class="hr-priority section-pad surface" id="priority"><div class="container"><div class="section-head"><div><p class="eyebrow">Where to start</p><h2 class="section-title">先选哪一个 HR 场景？</h2></div><p>企业主和 HR 负责人不需要一次把整个人力系统都 AI 化。先看四个判断维度：频次够不够高、答案是否有权威来源、动作是否可控、失败后是否能由人工接住。</p></div><div class="hr-priority-grid">
<article><span>01</span><small>最快起步</small><h3>制度问答与入职知识</h3><p>适合先做知识助手：制度、福利、IT 指引和岗位资料已有来源，输出可引用、可复核、可持续更新。</p><ul><li>起点：Top 50 高频问题</li><li>证据：引用命中率、人工纠错、未回答原因</li><li>边界：正式制度系统仍是权威来源</li></ul></article>
<article><span>02</span><small>最容易见效</small><h3>员工服务 Agent</h3><p>适合做流程型 Agent：收集信息、创建工单、查询状态、提醒 SLA，把 HR 从重复追问中释放出来。</p><ul><li>起点：请假、证明、设备、权限等高频请求</li><li>证据：工单流转、升级原因、处理时长</li><li>边界：员工关系和争议事项转人工</li></ul></article>
<article><span>03</span><small>最要谨慎</small><h3>招聘与绩效辅助</h3><p>只做材料整理、口径对齐和缺口提示，不让 AI 单独决定候选人、晋升、薪酬或淘汰。</p><ul><li>起点：JD、面试题、绩效材料初稿</li><li>证据：引用来源、经理复核、拒绝边界</li><li>边界：重大人才决定必须由人负责</li></ul></article>
<article><span>04</span><small>基础优先</small><h3>HR 数据分析助手</h3><p>适合有数据基础的团队；如果指标口径、权限和数据质量不清，先做数据治理，再做自然语言问数。</p><ul><li>起点：人力指标口径和权限表</li><li>证据：查询日志、指标定义、异常解释</li><li>边界：敏感人群分析最小权限</li></ul></article>
</div></div></section>
<section class="hr-chain section-pad"><div class="container"><div class="section-head"><div><p class="eyebrow">Evidence chain</p><h2 class="section-title"><span class="mobile-title-line">员工服务 Agent，</span><span class="mobile-title-line">要做成一条工作链。</span></h2></div><p>一条可上线的 HR 工作链需要记录员工问题、系统查询、AI 动作、人工接管和最终处理结果。</p></div><div class="hr-chain-layout"><div class="hr-chain-steps">
<article><span>01</span><h3>员工提出请求</h3><p>例如“我想申请陪产假”“VPN 权限开不了”“需要收入证明”。</p></article>
<article><span>02</span><h3>身份与权限确认</h3><p>根据员工身份、地区、岗位和请求类型决定能看哪些资料、能触发哪些动作。</p></article>
<article><span>03</span><h3>查询知识与系统</h3><p>从制度库、工单系统、假勤系统或 ITSM 读取授权信息，并保留来源。</p></article>
<article><span>04</span><h3>生成答复或工单</h3><p>能直接答复的给出引用；需要动作的创建工单、补齐字段、提示缺失材料。</p></article>
<article><span>05</span><h3>人工接管与复盘</h3><p>敏感、争议、低置信度或多次失败的请求转人工，并把失败样本回流评估集。</p></article>
</div><aside class="hr-chain-proof"><small>交付物应留下什么</small><h3>一套能复盘的运行记录</h3><dl><div><dt>Trace</dt><dd>每次问答、检索、工具调用和转人工原因。</dd></div><div><dt>Policy</dt><dd>哪些数据能用、哪些动作需要审批、哪些必须拒绝。</dd></div><div><dt>Scorecard</dt><dd>命中率、升级率、SLA、满意度、敏感事件和纠错闭环。</dd></div></dl></aside></div></div></section>
<section class="category-main section-pad" id="scenarios"><div class="container category-shell"><aside class="filter-panel" data-filter-panel><button class="filter-close" type="button" data-filter-close>关闭筛选 ×</button><h2>筛选场景</h2><div class="filter-group"><h3>任务阶段</h3><label><input type="checkbox" value="recruit" data-category-filter> 招聘</label><label><input type="checkbox" value="onboard" data-category-filter> 入职</label><label><input type="checkbox" value="service" data-category-filter> 员工服务</label><label><input type="checkbox" value="develop" data-category-filter> 培训绩效</label><label><input type="checkbox" value="analytics" data-category-filter> 组织分析</label></div><div class="filter-group"><h3>实施方式</h3><label><input type="checkbox" value="buy" data-category-filter> 现成方案</label><label><input type="checkbox" value="build" data-category-filter> 定制建设</label><label><input type="checkbox" value="both" data-category-filter> 两者均可</label></div><div class="filter-group"><h3>主要价值</h3><label><input type="checkbox" value="speed" data-category-filter> 提高效率</label><label><input type="checkbox" value="experience" data-category-filter> 员工体验</label><label><input type="checkbox" value="quality" data-category-filter> 质量一致性</label><label><input type="checkbox" value="risk" data-category-filter> 降低风险</label></div><button class="btn btn--ghost btn--block" type="button" data-filter-clear>清除筛选</button></aside><div class="category-results"><div class="category-toolbar"><div><button class="btn btn--ghost filter-mobile-toggle" type="button" data-filter-open>筛选</button><span><b data-category-count>6</b> 个场景单元</span></div><select data-category-sort aria-label="排序"><option value="recommended">推荐排序</option><option value="speed">最快起步</option><option value="complexity">复杂度从低到高</option></select></div><div class="product-grid">
<article class="product-card" data-tags="recruit buy both speed quality" data-speed="1" data-complexity="1"><div class="product-head"><span>招聘</span><b>01</b></div><h3>招聘筛选与沟通助手</h3><p>生成职位描述、整理简历、形成面试问题，并在人工确认后发送候选人沟通。</p><div class="micro-tags"><span>现成方案可起步</span><span>人工复核</span></div><ul><li>减少简历整理时间</li><li>统一候选人沟通口径</li><li>保留公平性检查</li></ul><div class="product-meta"><span>起点：JD 与候选人样本</span><span>证据：面试题、沟通记录、拒绝边界</span></div><a class="btn btn--green" href="service-ai-training.html">查看落地路径 →</a></article>
<article class="product-card" data-tags="onboard build both speed experience" data-speed="2" data-complexity="2"><div class="product-head"><span>入职</span><b>02</b></div><h3>员工入职知识助手</h3><p>连接制度、福利、IT 指引和岗位资料，为新员工提供可引用、按权限展示的答案。</p><div class="micro-tags"><span>RAG</span><span>权限检索</span></div><ul><li>减少 HR 重复问答</li><li>提高新员工上手速度</li><li>资料更新可追踪</li></ul><div class="product-meta"><span>起点：制度、福利、IT 文档</span><span>证据：引用来源、答案命中率、人工纠错</span></div><a class="btn btn--green" href="service-agent-build.html">查看落地路径 →</a></article>
<article class="product-card" data-tags="service build speed experience quality" data-speed="2" data-complexity="3"><div class="product-head"><span>员工服务</span><b>03</b></div><h3>员工服务 Agent</h3><p>处理高频问题、收集表单信息、创建工单并在必要时转交 HR 或 IT。</p><div class="micro-tags"><span>AI Agent</span><span>系统连接</span></div><ul><li>7×24 一致服务</li><li>自动分流与工单</li><li>可设置人工接管</li></ul><div class="product-meta"><span>起点：Top 50 高频请求</span><span>证据：工单流转、升级原因、SLA 记录</span></div><a class="btn btn--green" href="service-agent-build.html">查看落地路径 →</a></article>
<article class="product-card" data-tags="develop buy both experience quality" data-speed="1" data-complexity="1"><div class="product-head"><span>培训</span><b>04</b></div><h3>岗位培训与能力助手</h3><p>根据岗位、能力差距和企业资料生成学习路径、练习与反馈。</p><div class="micro-tags"><span>个性化学习</span><span>知识库</span></div><ul><li>缩短课程制作时间</li><li>按岗位提供练习</li><li>保留导师审核</li></ul><div class="product-meta"><span>起点：岗位能力模型</span><span>证据：课程初稿、练习反馈、导师确认</span></div><a class="btn btn--green" href="service-ai-training.html">查看落地路径 →</a></article>
<article class="product-card" data-tags="develop both quality risk" data-speed="3" data-complexity="2"><div class="product-head"><span>绩效</span><b>05</b></div><h3>绩效材料整理助手</h3><p>汇总目标、项目、反馈和证据，帮助经理形成结构化初稿，不替代最终判断。</p><div class="micro-tags"><span>辅助决策</span><span>证据引用</span></div><ul><li>减少材料整理</li><li>提醒信息缺口</li><li>避免自动做人才决定</li></ul><div class="product-meta"><span>起点：OKR、项目和反馈材料</span><span>证据：引用证据、缺口提示、经理复核</span></div><a class="btn btn--green" href="playbook.html#risk">查看风险说明 →</a></article>
<article class="product-card" data-tags="analytics build quality risk speed" data-speed="4" data-complexity="4"><div class="product-head"><span>分析</span><b>06</b></div><h3>HR 数据分析助手</h3><p>连接人员、招聘、培训和离职数据，用自然语言生成趋势、图表和需关注问题。</p><div class="micro-tags"><span>数据治理</span><span>分析 Agent</span></div><ul><li>统一人力指标口径</li><li>快速形成管理摘要</li><li>敏感数据最小权限</li></ul><div class="product-meta"><span>起点：指标口径和权限表</span><span>证据：SQL / 查询日志、异常解释、管理摘要</span></div><a class="btn btn--green" href="service-data-governance.html">查看落地路径 →</a></article>
</div></div></div></section>
<section class="hr-evidence section-pad surface" id="evidence"><div class="container"><div class="section-head"><div><p class="eyebrow">上线前检查</p><h2 class="section-title"><span class="mobile-title-line">HR 场景上线前，</span><span class="mobile-title-line">要过四项检查。</span></h2></div><p>HR 数据涉及个人信息、公平性和组织信任。试点开始前，需要写清数据范围、人工责任、系统动作和验收指标。</p></div><div class="hr-evidence-grid"><article><span>01</span><h3>数据边界</h3><p>哪些资料可用、哪些要脱敏、哪些只能由 HR 系统返回。</p></article><article><span>02</span><h3>人工判断</h3><p>候选人筛选、绩效、员工关系等重大影响事项必须有人负责。</p></article><article><span>03</span><h3>系统动作</h3><p>区分“生成建议”“创建工单”“写回系统”和“触发审批”。</p></article><article><span>04</span><h3>验收指标</h3><p>用时、命中率、升级率、员工满意度和合规记录要能持续追踪。</p></article></div></div></section>
<section class="hr-operating section-pad"><div class="container"><div class="section-head"><div><p class="eyebrow">Operating model</p><h2 class="section-title">上线前，把责任和证据摆在一张表里。</h2></div><p>HR 场景的风险不是“模型会不会说错一句话”这么简单，而是谁定义制度、谁批准动作、谁看敏感数据、谁负责员工申诉。上线前先把这些写清楚，后面才不会靠临时沟通救火。</p></div><div class="hr-operating-table" role="table" aria-label="HR AI 上线责任和证据表"><div role="row"><b role="columnheader">角色</b><b role="columnheader">上线前要确认</b><b role="columnheader">持续留下的证据</b></div><div role="row"><span>业务负责人</span><span>场景目标、成功指标、停止条件和预算边界。</span><span>月度采用率、处理时长、升级率和业务复盘。</span></div><div role="row"><span>HR 专家</span><span>制度口径、例外处理、敏感事项和转人工规则。</span><span>答案纠错、制度版本、例外审批和人工复核记录。</span></div><div role="row"><span>IT / 数据团队</span><span>身份权限、系统接口、日志、数据保留和故障回退。</span><span>工具调用日志、权限审计、可用性和错误类型。</span></div><div role="row"><span>法务 / 合规</span><span>个人信息、跨境、供应商政策、公平性和告知方式。</span><span>风险评审、数据处理记录、申诉与事件处理。</span></div><div role="row"><span>一线经理 / 员工代表</span><span>体验是否顺手、表达是否清楚、升级路径是否可信。</span><span>满意度、未解决问题、投诉样本和改进建议。</span></div></div></div></section>
<section class="category-guidance section-pad"><div class="container"><div class="section-head"><div><p class="eyebrow">Buy or build</p><h2 class="section-title">HR 场景买还是建？</h2></div></div><div class="guidance-grid"><article><h3>适合买</h3><p>职位描述、会议总结、通用课程制作等标准场景，可先用成熟工具，并明确数据政策。</p></article><article><h3>适合定制</h3><p>企业制度问答、员工服务 Agent、跨系统工单和敏感分析，需要接入企业数据、权限和流程。</p></article><article><h3>无论买还是建</h3><p>招聘、绩效和员工关系涉及公平、隐私和重大影响，必须保留人工判断、记录与申诉机制。</p></article></div></div></section>
<section class="section-pad"><div class="container faq-layout"><div><p class="eyebrow">FAQ</p><h2 class="section-title section-title--small">HR AI 常见问题</h2></div><div class="faq-list"><article class="faq-item"><button class="faq-question"><span>可以让 AI 自动淘汰候选人吗？</span><span class="plus">+</span></button><div class="faq-answer"><div><p>不建议让 AI 单独作出重大人才决定。AI 可辅助整理和提示，但筛选标准、公平性检查和最终决定应由授权人员负责。</p></div></div></article><article class="faq-item"><button class="faq-question"><span>员工资料能放进公共模型吗？</span><span class="plus">+</span></button><div class="faq-answer"><div><p>先按企业数据分类和供应商政策判断。敏感人员数据通常应在批准环境中使用，并遵循最小权限、脱敏和审计要求。</p></div></div></article><article class="faq-item"><button class="faq-question"><span>知识助手如何保持答案最新？</span><span class="plus">+</span></button><div class="faq-answer"><div><p>需要资料负责人、有效期、版本、更新流程和引用。模型不是制度来源，正式制度系统仍是权威来源。</p></div></div></article></div></div></section>
'''
category_body = f'''
<section class="hr-v2-hero" id="workbench"><div class="container">
  <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="navigator.html">场景与工具</a><span>/</span><strong>HR 场景地图</strong></nav>
  <div class="hr-v2-intro"><div><p class="eyebrow">HR AI SCENARIO MAP</p><h1>HR AI<br class="hr-v2-title-break">场景地图</h1><p>你现在最想改善哪一段 HR 工作？</p></div><div class="hr-v2-intro-note"><span>{ff_icon('i-layers')}</span><p>选一段工作，看看 AI 能接哪一步、谁来判断、上线前要准备什么。</p></div></div>
  <div class="hr-v2-tabs" role="tablist" aria-label="选择 HR 工作阶段">
    <button type="button" role="tab" aria-selected="false" data-hr-stage-tab="recruit">{ff_icon('i-people')}<span>招聘</span></button>
    <button type="button" role="tab" aria-selected="false" data-hr-stage-tab="onboard">{ff_icon('i-document')}<span>入职</span></button>
    <button class="is-active" type="button" role="tab" aria-selected="true" data-hr-stage-tab="service">{ff_icon('i-customer')}<span>员工服务</span></button>
    <button type="button" role="tab" aria-selected="false" data-hr-stage-tab="learn">{ff_icon('i-training')}<span>培训发展</span></button>
    <button type="button" role="tab" aria-selected="false" data-hr-stage-tab="performance">{ff_icon('i-chart')}<span>绩效</span></button>
    <button type="button" role="tab" aria-selected="false" data-hr-stage-tab="analytics">{ff_icon('i-data')}<span>组织分析</span></button>
  </div>
  <div class="hr-v2-workbench">
    <article class="hr-v2-panel" data-hr-workbench-panel="recruit" hidden>
      <div class="hr-v2-panel-lead"><span class="hr-v2-panel-icon">{ff_icon('i-people')}</span><small>01 · RECRUITING</small><h2>招聘筛选与沟通助手</h2><p>岗位标准统一后，AI 可以整理候选材料、准备面试问题和沟通草稿。</p><div><a class="btn btn--green" href="navigator.html?challenge=hr&amp;hrStage=recruit">用招聘场景继续诊断 →</a><a class="btn btn--ghost" href="#scenarios">查看全部场景</a></div></div>
      <div class="hr-v2-panel-grid"><section><span>{ff_icon('i-bulb')}</span><h3>当前问题</h3><ul><li>岗位标准和 JD 口径不一</li><li>简历量大，筛选记录分散</li><li>候选人跟进容易遗漏</li></ul></section><section><span>{ff_icon('i-spark')}</span><h3>AI 可以做</h3><ul><li>形成 JD 和面试问题初稿</li><li>按批准标准整理候选材料</li><li>起草进度与结果通知</li></ul></section><section><span>{ff_icon('i-people')}</span><h3>人要判断</h3><ul><li>岗位是否真的需要招聘</li><li>筛选标准是否公平合理</li><li>录用、拒绝和 offer 决定</li></ul></section><section><span>{ff_icon('i-requirements')}</span><h3>启动前准备</h3><ul><li>岗位画像与批准标准</li><li>脱敏候选样本</li><li>拒绝与升级边界</li></ul></section></div>
      <div class="hr-v2-proof"><span><b>来源版本</b>用了哪版 JD 与标准</span><span><b>建议记录</b>AI 给过哪些建议</span><span><b>人工修改</b>谁改了什么</span><span><b>处理用时</b>从收件到反馈</span></div>
    </article>
    <article class="hr-v2-panel" data-hr-workbench-panel="onboard" hidden>
      <div class="hr-v2-panel-lead"><span class="hr-v2-panel-icon">{ff_icon('i-document')}</span><small>02 · ONBOARDING</small><h2>员工入职知识助手</h2><p>让新员工按岗位和权限找到制度、福利、IT 与岗位资料，并看到答案出处。</p><div><a class="btn btn--green" href="navigator.html?challenge=hr&amp;hrStage=onboard">用入职场景继续诊断 →</a><a class="btn btn--ghost" href="#scenarios">查看全部场景</a></div></div>
      <div class="hr-v2-panel-grid"><section><span>{ff_icon('i-bulb')}</span><h3>当前问题</h3><ul><li>资料散落在多个入口</li><li>相同问题反复打断 HR</li><li>新员工不知道哪版有效</li></ul></section><section><span>{ff_icon('i-spark')}</span><h3>AI 可以做</h3><ul><li>按身份检索已批准资料</li><li>给答案并附原文引用</li><li>提醒缺资料和待办事项</li></ul></section><section><span>{ff_icon('i-people')}</span><h3>人要判断</h3><ul><li>制度解释与例外申请</li><li>资料责任人与有效期</li><li>敏感权限是否开放</li></ul></section><section><span>{ff_icon('i-requirements')}</span><h3>启动前准备</h3><ul><li>入职清单与岗位分组</li><li>权威资料目录</li><li>身份与权限规则</li></ul></section></div>
      <div class="hr-v2-proof"><span><b>引用来源</b>答案对应原文位置</span><span><b>资料版本</b>更新人与有效期</span><span><b>未答问题</b>为什么没回答</span><span><b>人工纠错</b>修正如何回流</span></div>
    </article>
    <article class="hr-v2-panel is-active" data-hr-workbench-panel="service">
      <div class="hr-v2-panel-lead"><span class="hr-v2-panel-icon">{ff_icon('i-customer')}</span><small>03 · EMPLOYEE SERVICE</small><h2>员工服务 Agent</h2><p>用自然语言理解请求、查知识、建工单，复杂和敏感事项及时交给人。</p><div><a class="btn btn--green" href="navigator.html?challenge=hr&amp;hrStage=service">用员工服务场景继续诊断 →</a><a class="btn btn--ghost" href="#scenarios">查看全部场景</a></div></div>
      <div class="hr-v2-panel-grid"><section><span>{ff_icon('i-bulb')}</span><h3>当前问题</h3><ul><li>FAQ 重复，HR 被动响应</li><li>工单分流慢、体验不一</li><li>知识分散，难追踪改进</li></ul></section><section><span>{ff_icon('i-spark')}</span><h3>AI 可以做</h3><ul><li>理解问题并检索知识库</li><li>回答高频问题、创建工单</li><li>识别意图并发起流程</li></ul></section><section><span>{ff_icon('i-people')}</span><h3>人要判断</h3><ul><li>复杂或例外情况的处理方案</li><li>政策解释的关键口径</li><li>跨部门协作与特殊审批</li></ul></section><section><span>{ff_icon('i-requirements')}</span><h3>启动前准备</h3><ul><li>梳理并清洗现有知识库</li><li>明确服务范围与边界</li><li>配置流程与权限规则</li></ul></section></div>
      <div class="hr-v2-proof"><span><b>引用来源</b>每次回答的知识出处</span><span><b>工单流转</b>工单状态与处理记录</span><span><b>转人工原因</b>触发人工的原因分类</span><span><b>处理时长</b>从受理到解决的时间</span></div>
    </article>
    <article class="hr-v2-panel" data-hr-workbench-panel="learn" hidden>
      <div class="hr-v2-panel-lead"><span class="hr-v2-panel-icon">{ff_icon('i-training')}</span><small>04 · LEARNING</small><h2>岗位学习与领导力陪练</h2><p>在反馈、绩效沟通和角色变化等真实时刻练一次，再进入真实工作。</p><div><a class="btn btn--green" href="navigator.html?challenge=hr&amp;hrStage=learn">用培训发展场景继续诊断 →</a><a class="btn btn--ghost" href="#scenarios">查看全部场景</a></div></div>
      <div class="hr-v2-panel-grid"><section><span>{ff_icon('i-bulb')}</span><h3>当前问题</h3><ul><li>课程与岗位任务脱节</li><li>管理者缺少练习机会</li><li>学完后难看到行为变化</li></ul></section><section><span>{ff_icon('i-spark')}</span><h3>AI 可以做</h3><ul><li>按角色分配学习和练习</li><li>模拟困难对话并即时反馈</li><li>引用企业原则给建议</li></ul></section><section><span>{ff_icon('i-people')}</span><h3>人要判断</h3><ul><li>能力标准和练习难度</li><li>反馈是否符合企业文化</li><li>真实岗位表现与发展决定</li></ul></section><section><span>{ff_icon('i-requirements')}</span><h3>启动前准备</h3><ul><li>岗位与能力模型</li><li>领导原则和优秀样例</li><li>角色变化触发规则</li></ul></section></div>
      <div class="hr-v2-proof"><span><b>学习触发</b>为什么此时分配</span><span><b>练习记录</b>完成了哪些场景</span><span><b>导师复核</b>哪些反馈被确认</span><span><b>能力变化</b>前后表现差异</span></div>
    </article>
    <article class="hr-v2-panel" data-hr-workbench-panel="performance" hidden>
      <div class="hr-v2-panel-lead"><span class="hr-v2-panel-icon">{ff_icon('i-chart')}</span><small>05 · PERFORMANCE</small><h2>绩效材料整理助手</h2><p>把目标、项目和反馈整理成有来源的初稿，最终评价仍由经理负责。</p><div><a class="btn btn--green" href="navigator.html?challenge=hr&amp;hrStage=performance">用绩效场景继续诊断 →</a><a class="btn btn--ghost" href="#scenarios">查看全部场景</a></div></div>
      <div class="hr-v2-panel-grid"><section><span>{ff_icon('i-bulb')}</span><h3>当前问题</h3><ul><li>证据散落在多个系统</li><li>评价写作耗时、口径不一</li><li>近期事件容易被过度放大</li></ul></section><section><span>{ff_icon('i-spark')}</span><h3>AI 可以做</h3><ul><li>汇总目标、项目和反馈</li><li>标注来源并提示信息缺口</li><li>生成结构化材料初稿</li></ul></section><section><span>{ff_icon('i-people')}</span><h3>人要判断</h3><ul><li>事实是否完整与准确</li><li>绩效等级、晋升和薪酬</li><li>员工申诉与校准结论</li></ul></section><section><span>{ff_icon('i-requirements')}</span><h3>启动前准备</h3><ul><li>评价周期和统一标准</li><li>授权数据来源</li><li>经理复核与申诉流程</li></ul></section></div>
      <div class="hr-v2-proof"><span><b>证据引用</b>每句话来自哪里</span><span><b>缺口提示</b>哪些事实仍缺失</span><span><b>经理修改</b>人工调整了什么</span><span><b>校准记录</b>最终如何确认</span></div>
    </article>
    <article class="hr-v2-panel" data-hr-workbench-panel="analytics" hidden>
      <div class="hr-v2-panel-lead"><span class="hr-v2-panel-icon">{ff_icon('i-data')}</span><small>06 · PEOPLE ANALYTICS</small><h2>HR 数据分析助手</h2><p>让管理者用自然语言查询经过定义的人力指标，同时保留查询与解释路径。</p><div><a class="btn btn--green" href="navigator.html?challenge=hr&amp;hrStage=analytics">用组织分析场景继续诊断 →</a><a class="btn btn--ghost" href="#scenarios">查看全部场景</a></div></div>
      <div class="hr-v2-panel-grid"><section><span>{ff_icon('i-bulb')}</span><h3>当前问题</h3><ul><li>指标定义和数据口径不一</li><li>临时分析依赖数据团队</li><li>敏感人群分析风险高</li></ul></section><section><span>{ff_icon('i-spark')}</span><h3>AI 可以做</h3><ul><li>把问题转成批准的查询</li><li>生成趋势与异常说明</li><li>形成管理层摘要初稿</li></ul></section><section><span>{ff_icon('i-people')}</span><h3>人要判断</h3><ul><li>业务原因与行动含义</li><li>小样本与敏感切片风险</li><li>管理动作是否合适</li></ul></section><section><span>{ff_icon('i-requirements')}</span><h3>启动前准备</h3><ul><li>人力指标口径表</li><li>数据质量与访问权限</li><li>敏感分析最小样本规则</li></ul></section></div>
      <div class="hr-v2-proof"><span><b>查询记录</b>问了什么、查了什么</span><span><b>指标版本</b>口径由谁维护</span><span><b>异常解释</b>结论依据是什么</span><span><b>行动复盘</b>后续是否有效</span></div>
    </article>
  </div>
  <div class="hr-v2-start"><div><span class="hr-v2-panel-icon">{ff_icon('i-layers')}</span><div><h2>如何选择第一个场景？</h2><p>优先看业务价值、数据条件和失败成本。</p></div></div><ol><li><b>01</b><span><strong>明确目标</strong>说清要改善的痛点与结果</span></li><li><b>02</b><span><strong>评估条件</strong>确认数据、流程和知识是否就绪</span></li><li><b>03</b><span><strong>快速试点</strong>小范围验证，留下证据再扩展</span></li></ol></div>
</div></section>

<section class="hr-v2-integrations section-pad" id="integrations"><div class="container"><div class="hr-v2-section-head"><div><p class="eyebrow">HR SYSTEMS</p><h2>需要联动用户、岗位和权限时，<br>再接入 HR 系统。</h2></div><p>下列为常见对接对象。实际接入仍需确认 API、字段、身份、数据驻留和写回能力，不代表已经具备开箱即用集成。</p></div><div class="hr-v2-logo-grid">
  <article><img src="assets/integrations/sap.svg" alt="SAP logo"><span>SAP SuccessFactors</span></article>
  <article><img src="assets/integrations/oracle.svg" alt="Oracle logo"><span>Oracle Cloud HCM</span></article>
  <article><img src="assets/integrations/rippling.png" alt="Rippling logo"><span>Rippling</span></article>
  <article><img src="assets/integrations/workday.svg" alt="Workday logo"><span>Workday HCM</span></article>
  <article><img src="assets/integrations/bamboohr.svg" alt="BambooHR logo"><span>BambooHR</span></article>
  <article><img src="assets/integrations/hibob.svg" alt="HiBob logo"><span>HiBob</span></article>
  <article><img src="assets/integrations/personio.svg" alt="Personio logo"><span>Personio</span></article>
  <article><img src="assets/integrations/factorial.png" alt="Factorial logo"><span>Factorial</span></article>
  </div><div class="hr-v2-integration-note"><b>实际接入前要验证</b><span>API 与版本</span><span>字段与身份映射</span><span>数据驻留与权限</span><span>写回、日志与失败回退</span></div></div></section>

<section class="hr-v2-catalog section-pad surface" id="scenarios"><div class="container"><div class="hr-v2-section-head"><div><p class="eyebrow">SIX STARTING POINTS</p><h2>六个场景，先选一个起点。</h2></div><p>第一轮优先选择问题明确、资料齐全、出错时能由人工接管的场景。每张卡都说明从哪里开始、要留下什么记录，以及哪些决定仍由人负责。</p></div><div class="hr-v2-card-grid">
  <article><span>01 · 招聘</span><h3>招聘筛选与沟通助手</h3><p>从 JD、候选材料和沟通草稿开始。</p><dl><div><dt>留下证据</dt><dd>标准版本、建议记录、人工修改</dd></div><div><dt>人来决定</dt><dd>筛选、公平性、录用与拒绝</dd></div></dl><button type="button" data-hr-stage-jump="recruit">在工作台查看 →</button></article>
  <article><span>02 · 入职</span><h3>员工入职知识助手</h3><p>从制度、福利、IT 和岗位资料开始。</p><dl><div><dt>留下证据</dt><dd>引用来源、资料版本、未答问题</dd></div><div><dt>人来决定</dt><dd>制度解释、例外与敏感权限</dd></div></dl><button type="button" data-hr-stage-jump="onboard">在工作台查看 →</button></article>
  <article><span>03 · 员工服务</span><h3>员工服务 Agent</h3><p>从 Top 50 高频请求和工单流程开始。</p><dl><div><dt>留下证据</dt><dd>工单流转、升级原因、处理时长</dd></div><div><dt>人来决定</dt><dd>员工关系、争议与异常审批</dd></div></dl><button type="button" data-hr-stage-jump="service">在工作台查看 →</button></article>
  <article><span>04 · 培训发展</span><h3>岗位学习与领导力陪练</h3><p>从真实岗位任务和困难对话练习开始。</p><dl><div><dt>留下证据</dt><dd>学习触发、练习记录、导师复核</dd></div><div><dt>人来决定</dt><dd>能力标准、反馈与发展决定</dd></div></dl><button type="button" data-hr-stage-jump="learn">在工作台查看 →</button></article>
  <article><span>05 · 绩效</span><h3>绩效材料整理助手</h3><p>从目标、项目与多方反馈材料开始。</p><dl><div><dt>留下证据</dt><dd>引用证据、缺口提示、经理修改</dd></div><div><dt>人来决定</dt><dd>等级、晋升、薪酬与申诉</dd></div></dl><button type="button" data-hr-stage-jump="performance">在工作台查看 →</button></article>
  <article><span>06 · 组织分析</span><h3>HR 数据分析助手</h3><p>从指标口径、权限表和常见问题开始。</p><dl><div><dt>留下证据</dt><dd>查询日志、指标版本、异常解释</dd></div><div><dt>人来决定</dt><dd>业务含义、敏感分析与行动</dd></div></dl><button type="button" data-hr-stage-jump="analytics">在工作台查看 →</button></article>
</div></div></section>

<section class="hr-v2-gates section-pad" id="evidence"><div class="container"><div class="hr-v2-section-head"><div><p class="eyebrow">BEFORE GO-LIVE</p><h2>上线前，四件事写清楚。</h2></div><p>HR 场景涉及个人信息、公平性和组织信任。无论购买现成产品还是定制 Agent，都要先确认下面四件事。</p></div><div class="hr-v2-gate-grid"><article><b>01</b><h3>数据边界</h3><p>哪些资料可用、如何脱敏、谁能访问。</p></article><article><b>02</b><h3>人工判断</h3><p>哪些建议必须复核，哪些决定不能交给 AI。</p></article><article><b>03</b><h3>系统动作</h3><p>区分建议、建单、写回系统和触发审批。</p></article><article><b>04</b><h3>验收证据</h3><p>用时、命中率、升级率、满意度和审计记录。</p></article></div><div class="hr-v2-buybuild"><div><small>适合买</small><h3>标准、低敏、边界清楚的任务</h3><p>通用内容制作、会议整理和基础学习工具，可先试成熟产品。</p></div><div><small>适合定制</small><h3>需要企业知识、权限和流程的任务</h3><p>制度问答、员工服务、跨系统工单和敏感分析，更适合按企业环境建设。</p></div><div><small>共同底线</small><h3>重大人才决定必须由人负责</h3><p>招聘、绩效、薪酬和员工关系保留复核、记录与申诉机制。</p></div></div></div></section>

<section class="hr-v2-cta section-pad"><div class="container"><div><p class="eyebrow">START SMALL</p><h2>挑一个场景，<br>把第一轮验证做扎实。</h2><p>告诉我们业务痛点、现有 HR 系统和可用资料，我们会给出起步范围、准备清单和验证指标。</p></div><a class="btn btn--green" href="contact.html?topic=hr">聊聊 HR 场景 →</a></div></section>
'''

(ROOT/'category-hrms.html').write_text(page('HR AI 场景地图','招聘、入职、员工服务、培训、绩效与 HR 分析的 AI 场景地图。','category-hrms',category_body,'category-page'),encoding='utf-8')

cases_body=f'''
<section class="cases-hero"><div class="container"><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>案例&博客</strong></nav><p class="eyebrow">Case studies &amp; blog</p><h1>案例里，把问题、<br>做法和结果讲清楚。</h1><p>这里收录了团队过往项目、公开案例、合作材料和概念场景。每个页面都会注明：哪些是团队经验，哪些来自公开资料，哪些数字仍需验证。</p><div class="case-filter-bar" role="group" aria-label="按行业筛选案例"><button class="is-active" data-case-filter="all" aria-pressed="true">全部</button><button data-case-filter="manufacturing" aria-pressed="false">工业与制造</button><button data-case-filter="healthcare" aria-pressed="false">医疗与健康</button><button data-case-filter="service" aria-pressed="false">客户服务</button><button data-case-filter="education" aria-pressed="false">教育</button><button data-case-filter="data" aria-pressed="false">数据与运营</button></div></div></section>
<section class="section-pad"><div class="container case-library">
{render_case_library(featured=True)}
<div class="case-library-grid">
{render_case_library(featured=False)}
</div><p class="source-note">页内会保留原项目数字及其公开口径，并把预计、示例、目标和已发生结果分开标注。</p></div></section>
<section class="case-method section-pad section-ink"><div class="container"><div class="section-head"><div><p class="eyebrow eyebrow--light">A useful case study</p><h2 class="section-title">判断案例值不值得参考，<br>看这五件事。</h2></div></div><ol class="case-method-list"><li><span>01</span><p>原来的业务问题和基线是什么？</p></li><li><span>02</span><p>为什么选择这个场景和方法？</p></li><li><span>03</span><p>数据、系统、团队和风险如何处理？</p></li><li><span>04</span><p>用哪些指标证明效果？</p></li><li><span>05</span><p>下一步如何运营和扩展？</p></li></ol></div></section>
'''
(ROOT/'cases.html').write_text(page('企业 AI 案例&博客','企业 AI、数据、Agent 和组织赋能案例与博客索引。','cases',cases_body,'cases-page'),encoding='utf-8')

case_detail_body='''
<section class="case-detail-hero"><div class="container"><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="cases.html">案例&博客</a><span>/</span><strong>Wren Kitchens</strong></nav><p class="eyebrow">TSH public customer case</p><h1>Wren Kitchens：<br>从紧急团队扩容到长期技术合作。</h1><p>这是一篇公开客户案例的结构化解读，用来说明企业在高速增长、系统复杂和内部团队承压时，如何先稳住关键流程，再把外部技术能力沉淀为长期协作能力。</p><div class="case-detail-metrics"><div><strong>31</strong><span>TSH 原文中的合作团队规模</span></div><div><strong>1 分钟 → 约 5 秒</strong><span>TSH 原文中的关键服务加载优化</span></div><div><strong>多业务模块</strong><span>安装、物流、产品、QA、移动应用</span></div></div><p class="case-proof-note">本文依据 The Software House（TSH）公开客户案例整理，不代表 ForFlow 参与该项目。团队规模、加载时间与物流改善均保留原文口径，引用时请以原文为准。</p><div class="case-detail-visual case-art--wren"><span>MANUFACTURING × RETAIL × SOFTWARE DELIVERY</span></div></div></section>
<div class="container case-detail-shell case-story-shell"><aside class="case-toc"><div class="case-toc-inner"><small>本页目录</small><nav data-scrollspy><a class="is-active" href="#challenge">业务挑战</a><a href="#takeover">快速接管</a><a href="#modules">合作模块</a><a href="#impact">公开影响</a><a href="#lessons">可复用经验</a></nav></div></aside><article>
<section id="challenge" data-section class="case-section"><p class="eyebrow">Challenge</p><h2>增长很快的企业，最怕系统能力追不上业务节奏。</h2><p>公开案例显示，Wren Kitchens 在结束上一家供应商合作后，需要快速补充开发能力，同时保持质量、可靠性和按期交付。当地专业人才有限，路线图又会随业务变化，因此企业不仅需要“人手”，还需要能接管知识、处理高风险工作并灵活扩缩的伙伴。</p><ul><li>需要立即补充大量 PHP 开发能力</li><li>短期与长期项目并存，团队规模需要灵活变化</li><li>未来几个季度的技术工作难以完全提前规划</li><li>关键业务要求稳定、准时且可持续交付</li></ul></section>
<section id="takeover" data-section class="case-section"><p class="eyebrow">Project takeover</p><h2>没有完整交接窗口，也要先稳住业务，再谈优化。</h2><p>新团队直接进入已有内部 IT 组织。由于客户拥有清晰文档和技术责任，新伙伴可以从第一天建立可靠知识基础。重点不是立即大改系统，而是确认责任、运行风险、关键流程和可快速改善的事项。</p><div class="case-quote"><blockquote>先建立稳定交付与信任，再逐步承担更复杂、更关键的业务模块。</blockquote><cite>ForFlow 对 TSH 公开材料的归纳</cite></div></section>
<section id="modules" data-section class="case-section"><p class="eyebrow">Workstreams</p><h2>合作扩展到安装、物流、产品、质量和移动应用。</h2><div class="case-modules"><article class="case-module"><h3>安装流程</h3><p>支持安装人员网络、测量、预约、日期和客户验收等完整生命周期。</p></article><article class="case-module"><h3>物流与交付</h3><p>优化影响夜间运行和标签准确性的关键流程，减少异常与处罚。</p></article><article class="case-module"><h3>产品与知识交接</h3><p>协助新内部开发人员理解领域知识、系统和责任边界。</p></article><article class="case-module"><h3>质量与移动应用</h3><p>完善上线前验证、QA 标准和 iPad 内部应用的稳定与持续交付。</p></article></div></section>
<section id="impact" data-section class="case-section"><p class="eyebrow">Impact</p><h2>公开案例报告了成本、稳定性和交付速度的共同改善。</h2><p>公开页面提到，团队先处理“容易见效”的数据库与服务问题，其中一个关键产品浏览服务从约 1 分钟缩短到约 5 秒；物流与标签流程也提高了准确性，减少了处罚并稳定关键夜间运行。</p><p>更重要的结果是合作模式从紧急扩容逐步转为长期、跨模块协作：外部团队不只是完成任务，还承担知识传递、风险工作和持续改进。</p></section>
<section id="lessons" data-section class="case-section"><p class="eyebrow">Lessons for enterprise AI</p><h2>这类案例对 AI 项目同样有三点启发。</h2><ol class="start-steps"><li><span>1</span><div><h3>先稳住关键流程</h3><p>AI 项目也应先理解现有责任、数据和失败成本，不要一开始大规模重构。</p></div></li><li><span>2</span><div><h3>从可验证改善建立信任</h3><p>选择能快速量化的时效、错误和质量问题，形成共同工作方式。</p></div></li><li><span>3</span><div><h3>把知识留在企业</h3><p>文档、评估、培训和内部负责人必须与技术交付同步。</p></div></li></ol></section>
</article></div>
<section class="case-source-foot" id="case-source" aria-labelledby="wren-case-source-title"><div class="container"><div class="case-source-card"><span class="case-source-card__icon"><svg aria-hidden="true" class="ff-icon"><use href="#i-reference"></use></svg></span><div><small>公开客户案例原文</small><h2 id="wren-case-source-title">数字有出处，但不是 ForFlow 项目结果。</h2><p>本页只对 TSH 发布的 Wren Kitchens 客户案例做中文结构化整理；具体合作范围、结果与表述以原文为准。</p><a href="https://tsh.io/portfolio/wren-kitchens-partnership" target="_blank" rel="noopener noreferrer">查看 TSH 官方案例 <span aria-hidden="true">↗</span></a></div></div></div></section>
<section class="final-cta"><div class="container final-cta-inner"><div><h2><span class="mobile-title-line">把同样的案例结构，</span><span class="mobile-title-line">用于你的项目。</span></h2><p>先写清问题、基线、流程、数据、风险与成功指标。</p></div><a class="btn" href="navigator.html">开始场景诊断 →</a></div></section>
'''
(ROOT/'case-wren-kitchens.html').write_text(page('Wren Kitchens：从紧急团队扩容到长期技术合作','Wren Kitchens 公开合作案例的中文结构化摘要。','case-wren-kitchens',case_detail_body,'case-detail-page case-study-v2 case-study-legacy'),encoding='utf-8')

automotive_dfmea_body='''
<section class="case-study-hero">
  <div class="container">
    <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="cases.html">案例&博客</a><span>/</span><strong>汽车工程与安全关键零部件</strong></nav>
    <div class="case-study-hero__grid">
      <div class="case-study-hero__copy">
        <div class="case-study-meta"><span>ForFlow 工程方法 · 上篇</span><span>汽车安全关键件</span><span>B 柱 DFMEA</span><span>知识流失治理</span></div>
        <h1><span class="mobile-title-line">用工程本体补齐</span><span class="mobile-title-line">B 柱 DFMEA 的</span><span class="mobile-title-line">知识与追溯</span></h1>
        <p class="case-study-lead">对制造业老板来说，真正可怕的不是开不出 DFMEA 会，而是几位资深工程师一退休、一次供应商换线、一张 ECO 改完设计，为什么某个焊点不能改、某个批次曾经出过什么问题、哪些风险必须重新验证，没人能完整说清。B 柱只是一个放大镜：它把安全责任、工程知识流失和组织记忆断层同时摆到台面上。</p>
        <div class="case-study-actions"><a class="btn btn--green" href="#overview">先看核心问题 <span aria-hidden="true">↓</span></a><a class="btn btn--ghost" href="#ontology">查看本体逻辑 <span aria-hidden="true">↘</span></a></div>
      </div>
      <figure class="case-study-hero__media case-study-hero__media--scene">
        <img alt="汽车 B 柱结构件与工程风险网络场景图" decoding="async" fetchpriority="high" loading="eager" src="assets/cases/automotive-dfmea-bpillar-hero.png">
        <figcaption>B 柱 DFMEA 的难点不在“列一张表”，而在材料、工艺、界面、载荷和法规要求同时交汇。</figcaption>
      </figure>
    </div>
    <div aria-label="本案例的风险与交付证据结构" class="case-proof-rail"><div><strong>老师傅经验</strong><span>失效案例、工艺窗口和供应商批次不能只留在个人记忆里</span></div><div><strong>ECO 复评</strong><span>设计变更后，哪些 DFMEA 条目失效、哪些仍有效，需要自动回到台面</span></div><div><strong>跨项目迁移</strong><span>旧车型、C 柱、焊接接头和保修索赔教训要能进入新平台</span></div><div><strong>RFLP</strong><span>需求、功能、逻辑、物理四层追溯，让风险能被解释和审计</span></div></div>
    <p class="case-proof-note">这套方法来自 ForFlow 团队成员在原组织中积累的汽车工程与智能体经验，并用公开法规和原项目资料校准可披露细节。上篇讲知识与追溯，下篇再展开实现架构；具体效果仍要用企业自己的设计、试验和质量数据验证。</p>
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
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-reference"></use></svg></span><div><small>试点要验证</small><strong>是否减少遗漏、加快复评并保留工程经验</strong></div></div>
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
      <div class="case-fit-grid"><article class="case-fit-card case-fit-card--yes"><small>复杂性激增</small><h3>多材料 B 柱引入十年前少见的失效机制</h3><ul><li>定制坯料、热冲压分区、软区和激光拼焊板</li><li>钢/复合材料或不同钢种之间的界面风险</li><li>分层开裂、电偶腐蚀、粘接失效、涂层缺陷</li><li>材料、工艺、环境和载荷同时作用的组合失效</li></ul></article><article class="case-fit-card case-fit-card--yes"><small>开发周期压缩</small><h3>完整手工研讨通常需要约 3 到 4 周</h3><ul><li>具体周期取决于部件、资料和组织流程</li><li>每个关键部件都用传统深度会议难以扩展</li><li>法规和评级测试规程持续变化</li><li>设计变更要求风险分析能快速复评</li></ul></article><article class="case-fit-card case-fit-card--yes"><small>知识断层</small><h3>老师傅的判断必须变成企业资产</h3><ul><li>资深工程师的隐性判断需要沉淀</li><li>新工程师需要可追溯案例，不只是历史表格</li><li>跨平台、跨项目经验需要自动迁移</li><li>供应商和内部团队需要统一语义与责任边界</li></ul></article><article class="case-fit-card case-fit-card--yes"><small>失效代价</small><h3>越晚发现，成本越指数级上升</h3><ul><li>设计阶段修复是工程代价</li><li>生产阶段修复是供应链和质量代价</li><li>上市后修复可能变成召回和品牌代价</li><li>安全关键件还叠加法律和声誉风险</li></ul></article></div>
    </section>

    <section class="case-section" data-section id="ontology">
      <p class="eyebrow">Ontology as reasoning context</p>
      <h2>“电子表格 AI”为什么必然失败？因为它继承的是历史记录，不是工程因果。</h2>
      <p>很多 AI 辅助 DFMEA 的直觉方案，是把历史 DFMEA 电子表格喂给大语言模型，期待它生成新的失效模式。这条路最多得到一个自动补全引擎。它能复述历史上常见的词，但无法真正判断新的材料、工艺、界面和载荷组合会带来什么风险。</p>
      <div class="case-decision-grid"><article class="case-decision-card"><small>失败原因一</small><h3>继承知识盲区</h3><p>如果历史 DFMEA 本来就遗漏了某类失效模式，模型会把这个遗漏当作正常分布继承下来。未被记录的失效，无法从表格里学到。</p></article><article class="case-decision-card"><small>失败原因二</small><h3>缺乏因果理解</h3><p>模型可能写出“焊接失效”，却分不清是阴极浸涂后的氢脆、焊趾疲劳裂纹，还是激光焊接参数漂移导致熔合不足。</p></article><article class="case-decision-card"><small>失败原因三</small><h3>无法推断组合失效</h3><p>最危险的失效模式往往来自多个因素交互，而这些因素可能从未在历史项目中同时出现过。</p></article></div>
      <div class="case-subhead case-subhead--relation"><small>本体编码的是关系</small><h3>材料 → 工艺 → 失效机理 → 影响效应。</h3></div>
      <p>工程本体的作用，是把知识从“事实列表”变成“关系网络”。当本体知道 22MnB5 硼钢经过约 900°C 奥氏体化热冲压，随后进入涂装、焊接和服役环境，它就能把热影响区、涂层状态、氢敏感性、残余应力、腐蚀暴露和疲劳载荷连到同一条推理路径上。</p>
      <div class="case-reading-note"><strong>企业主应该先看什么</strong><p>本体试点不必一开始覆盖整车。先看四类资料是否能拿出来：历史 DFMEA 和设计变更记录、关键材料与工艺窗口、试验/仿真/保修证据、供应商变更与现场质量反馈。如果这些资料散在不同系统和个人经验里，B 柱这样的安全关键件就值得先做一个小范围本体化试点。</p></div>
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
      <div class="case-reading-note"><strong>项目判断</strong><p>DFMEA 智能体不是替代工程责任，而是把工程师、材料知识、历史证据和验证路径组织成可追踪流程。先判断它能否减少知识流失、缩短复评时间和降低遗漏风险，再谈多智能体架构。</p></div>
    </section>

    <section class="case-section" data-section id="references">
      <p class="eyebrow">Public technical context</p>
      <h2>公开资料用于校准技术背景，项目实施仍要回到企业自己的设计、试验和质量数据。</h2>
      <p>下面这些公开资料适合用于理解法规测试、材料工艺、FMEA 方法和智能体平台的基础概念。真正落地时，风险判断仍应以企业自己的设计数据、试验记录、工艺窗口、供应商信息和质量反馈为准。</p>
      <div class="case-reference-list"><a href="https://aws.amazon.com/blogs/industries/reimagining-b-pillar-dfmea/" target="_blank" rel="noopener noreferrer">原项目公开资料：B-Pillar DFMEA</a><a href="https://crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/809004" target="_blank" rel="noopener">NHTSA FMVSS 214 侧碰保护评估</a><a href="https://www.iihs.org/media/46940e89-46cb-4e6e-81ee-8230bb3b5dd9/0dx8eA/Ratings/Protocols/current/test_protocol_roof.pdf" target="_blank" rel="noopener">IIHS Roof Strength Test Protocol</a><a href="https://crashstats.nhtsa.dot.gov/Api/Public/Publication/813027" target="_blank" rel="noopener">NHTSA FMVSS 216a Roof Crush Resistance 评估</a><a href="https://ahssinsights.org/tag/hot-stamped-boron/" target="_blank" rel="noopener">AHSS Guidelines：热冲压硼钢与 B 柱案例</a><a href="https://www.open-access.bcu.ac.uk/6942/" target="_blank" rel="noopener">22MnB5 热冲压超高强钢论文摘要</a><a href="https://www.aiag.org/training-and-resources/manuals/details/FMEAAV-1" target="_blank" rel="noopener">AIAG &amp; VDA FMEA Handbook 训练资料</a></div>
    </section>

    <section class="case-section" data-section id="next">
      <p class="eyebrow">Part two preview</p>
      <h2>下篇进入技术实现：运行平台、工具编排、七层架构和 B 柱逐步演练。</h2>
      <p>第二部分将展开多智能体编排、本体读写、权限审计和工程系统集成，并用 B 柱 DFMEA 做逐步演练。</p>
      <div class="case-related-grid"><article class="case-related-card"><div><small>架构层</small><h3>7 层生产架构</h3><p>从数据接入、本体存储、智能体运行，到审计、权限和工程系统集成。</p></div></article><article class="case-related-card"><div><small>编排层</small><h3>多智能体管道</h3><p>失效模式、结构分解、法规认证、通用耐久性分析代理如何协同。</p></div></article><article class="case-related-card"><div><small>演练层</small><h3>B 柱 DFMEA 步进实现</h3><p>从输入设计、调用本体、生成候选失效模式，到证据复核和 ECO 更新。</p></div></article></div>
    </section>
  </article>
</div>
<section class="case-related">
  <div class="container">
    <div class="case-related-head"><div><p class="eyebrow">Related cases</p><h2>继续看相邻问题，建立完整判断。</h2></div><a class="text-link" href="cases.html">查看全部案例&博客 →</a></div>
    <div class="case-related-grid">
      <a class="case-related-card" href="case-manufacturing-pid-intelligence.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/thumb-manufacturing-pid.webp"><div><small>制造业知识资产化</small><h3>P&amp;ID 图纸如何变成可查询运营知识</h3><p>静态图纸、知识图谱、工程师复核和可追溯问答</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-healthcare-agent-roi.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/healthcare-care-chain-sana-plain.png"><div><small>高合规智能体</small><h3>医疗工作流中的受限多智能体架构</h3><p>状态机、人工升级、模型专项化和 ROI 验证</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="navigator.html"><img alt="" decoding="async" loading="lazy" src="assets/generated-review/c02-navigator-china-q2q-diagnostic-workbench.png"><div><small>AI 场景诊断</small><h3>先判断场景是否值得 AI 化</h3><p>从问题、数据、责任和验收方式判断第一条工作流</p><span>继续阅读 <b>↗</b></span></div></a>
    </div>
  </div>
</section>
<section class="case-next-cta"><div class="container case-next-cta__inner"><div><small>把案例映射到你的企业</small><h2>不要先问用哪个模型，先问知识能否被推理和复评。</h2><p>把真实流程、材料工艺、历史失效和验证责任带进一次场景诊断，判断这个 AI 工作单元是否具备上线资格。</p></div><div><a class="btn btn--light" href="navigator.html">开始 AI 场景诊断 →</a><a class="btn btn--ghost" href="cases.html">返回案例&博客</a></div></div></section>
<section class="case-source-foot" id="case-source" aria-labelledby="case-source-title"><div class="container"><div class="case-source-card"><span class="case-source-card__icon"><svg aria-hidden="true" class="ff-icon"><use href="#i-reference"></use></svg></span><div><small>ForFlow 团队经验与公开依据</small><h2 id="case-source-title">团队做过这类工程工作，公开资料负责说明可披露部分。</h2><p>这套方法来自团队成员加入 ForFlow 前的工程经验。新的车企项目仍要用自己的设计、试验、工艺和质量数据验证。</p><a href="https://aws.amazon.com/blogs/industries/reimagining-b-pillar-dfmea/" target="_blank" rel="noopener noreferrer">查看原项目公开资料 <span aria-hidden="true">↗</span></a></div></div></div></section>
'''
(ROOT/'case-automotive-dfmea-ontology-agent.html').write_text(page('用工程本体补齐 B 柱 DFMEA 的知识与追溯','ForFlow 团队工程方法：用本体、RFLP、智能体和多项目知识迁移改进安全关键汽车零部件风险分析。','case-automotive-dfmea-ontology-agent',automotive_dfmea_body,'case-detail-page case-theme--automotive case-study-v2'),encoding='utf-8')

supply_chain_agentic_body='''
<section class="case-study-hero case-study-hero--supply">
  <div class="container">
    <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="cases.html">案例&博客</a><span>/</span><strong>零售供应链与多智能体决策</strong></nav>
    <div class="case-study-hero__grid">
      <div class="case-study-hero__copy">
        <div class="case-study-meta"><span>ForFlow 团队实践</span><span>匿名鞋服零售商</span><span>多智能体 AI</span><span>从洞察到行动</span></div>
        <h1><span class="mobile-title-line">多智能体 AI 如何</span><span class="mobile-title-line">将供应链数据</span><span class="mobile-title-line">转化为决策与行动</span></h1>
        <p class="case-study-lead">供应链老板最关心的不是又多一个仪表盘，而是异常能不能更早被发现，根因能不能更快说清，行动能不能直接进入负责人手里。库存周转缩短一天、缺货率降低一个百分点、物流异常提前一小时发现，单看都不惊人；放到数百万个 SKU 和数十亿美元营收规模里，就会持续改变成本结构、客户体验和新品上市速度。</p>
        <div class="case-study-actions"><a class="btn btn--green" href="#architecture">看架构设计 <span aria-hidden="true">↓</span></a><a class="btn btn--ghost" href="#workflow">看匿名化履行分析 <span aria-hidden="true">↘</span></a></div>
      </div>
      <figure class="case-study-hero__media case-study-hero__media--scene">
        <img alt="零售供应链运营负责人查看数据并准备行动" decoding="async" loading="eager" src="assets/cases/supply-chain-agentic-decision-hero.png">
        <figcaption>供应链决策不止是“看见数据”，而是把查询、分析、归因和行动连成一条可复盘的工作链。</figcaption>
      </figure>
    </div>
    <div aria-label="本案例的决策证据结构" class="case-proof-rail"><div><strong>数据可见</strong><span>ERP、WMS、TMS、数据湖和仪表盘只是起点</span></div><div><strong>主动推理</strong><span>自然语言发问，自动查询、钻取和归因</span></div><div><strong>行动闭环</strong><span>通知、审批摘要和工单直接进入团队流程</span></div><div><strong>可维护架构</strong><span>语义层和 MCP 让数据源变化不拖垮智能体</span></div></div>
    <p class="case-proof-note">这是 ForFlow 团队成员在原组织中积累的供应链智能体经验。原项目来自一家匿名全球鞋服零售商；客户身份、完整测量口径和观察期未公开，页面只使用可披露的架构与匿名数据。</p>
  </div>
</section>
<div class="container case-detail-shell case-story-shell">
  <aside class="case-toc"><div class="case-toc-inner"><small>本页目录</small><nav data-scrollspy><a class="is-active" href="#challenge">决策问题</a><a href="#bottleneck">控制塔瓶颈</a><a href="#architecture">架构设计</a><a href="#design-decisions">关键设计</a><a href="#workflow">履行分析</a><a href="#operating-model">企业落地</a><a href="#references">技术背景</a></nav><a class="case-toc-source" href="cases.html">返回案例&博客</a></div></aside>
  <article>
    <section class="case-section" data-section id="challenge">
      <p class="eyebrow">Decision quality</p>
      <h2>供应链竞争力，最后会落到每一天的决策质量上。</h2>
      <p>供应链既是零售企业最重要的竞争优势之一，也是运营上最复杂的环节之一。每一个决策都有可量化的成本代价：库存周转时间缩短一天、缺货率降低一个百分点、提前一小时发现物流异常，这些收益都会在规模里叠加。</p>
      <p>真正的问题不是企业有没有数据，而是在正确的时间，基于正确的信息，做出正确判断。如今，这种能力已经触手可及：大型语言模型已经能够可靠调用各类工具，编排框架也日趋成熟，足以协调多个专项智能体以生产级质量完成复杂流程。</p>
      <div class="case-question-panel"><div><small>老板视角</small><h3>如果一个问题要半天才查清，很多异常根本不会被调查。</h3><p>当提问成本很高，团队只会追几个固定 KPI；当回答一个供应链问题的最小单位从“一名分析师加半天时间”降到“一句话加 30 秒”，团队才会追踪更多边角异常，决策覆盖范围才会扩大。</p></div><div class="case-goal"><small>目标工作单元</small><h3>收集 → 查询 → 洞察 → 行动</h3><p>数据收集已经基本解决，Agent 要补的是后面三步：自动查询、自动分析、把结论变成可执行动作。</p></div></div>
    </section>

    <section class="case-section" data-section id="bottleneck">
      <p class="eyebrow">Visibility is not decision</p>
      <h2>数据可见性，不等于数据驱动决策。</h2>
      <p>经过多年数字化投资，大多数零售商已经建立了相当完整的数据基础设施：ERP、WMS、TMS、数据湖和各类仪表盘一应俱全。控制塔把多源数据聚合起来，提供可视化和告警，解决了“看见数据”的问题。</p>
      <p>但控制塔本质上仍然偏被动：分析逻辑在构建时就已固化，只能展示预定义指标，无法主动推理；迭代周期常常以周或月计。业务人员仍然要通过数据工程团队提需求、等结果，在电子表格里做分析，再靠邮件和会议推动行动。</p>
      <p>智能体 AI 代表的是控制塔之后的下一步：从“看数据”到“查数据”，从“被动展示”到“主动推理”。供应链团队无需等待分析师重新做仪表盘或临时写查询，直接用自然语言提出问题，获得结构化分析、根因归因和可立即执行的行动方案。</p>
      <div class="case-value-cards case-value-cards--triple"><article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-data"></use></svg></span><small>查询障碍</small><h3>业务人员难以自助获取数据</h3><p>SQL 技能门槛、不一致的业务定义和复杂多表关联，让很多问题停在“能不能帮我拉一下数”。</p></article><article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-brain"></use></svg></span><small>洞察差距</small><h3>原始数据不能自动变成结论</h3><p>异常检测、多维钻取和根因归因仍然依赖人工经验，分析质量和速度跟人强相关。</p></article><article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><small>行动脱节</small><h3>洞察留在报告里，行动靠人协调</h3><p>即使结论清楚，后续仍要发邮件、拉群、开会和追审批，响应时间以天计。</p></article></div>
      <div class="case-comparison-table"><div><span>决策瓶颈</span><span>控制塔的局限</span><span>智能体 AI 的解法</span><strong>查询障碍</strong><p>需要 SQL 技能和数据工程支持</p><p>自动将自然语言翻译成 SQL 查询</p><strong>洞察差距</strong><p>只展示预定义指标</p><p>执行异常检测、多维钻取和根因归因</p><strong>行动脱节</strong><p>分析留在报告里，行动依赖人工协调</p><p>生成可执行材料并通知相关团队</p></div></div>
    </section>

    <section class="case-section" data-section id="architecture">
      <p class="eyebrow">Supervisor-worker architecture</p>
      <h2>架构的关键，是让主管代理理解意图，让专项代理各自做好一件事。</h2>
      <p>ForFlow 把系统拆成九个核心组件，覆盖用户接入、身份、会话、智能体运行、工具网关和可观测性。原项目说明了一条可运行的路径，但不代表同样的收益可以直接复制到其他企业。</p>
      <div class="case-layer-notes"><article><small>用户接入层 · 组件 01-05</small><p>业务用户通过 Web 应用访问系统。前后端经由 API 网关和无服务器函数集成；企业身份平台负责认证；低延迟数据存储保存对话历史和应用配置。</p></article><article><small>智能体核心层 · 组件 06-07</small><p>主管智能体和专项智能体运行在受管平台上，由模型服务提供推理能力。身份层统一管理用户权限、服务凭据和外部 API 授权。</p></article><article><small>数据与可观测性层 · 组件 08-09</small><p>工具网关通过 MCP 或 API 访问外部数据源；可观测性层记录运行状态、工具调用和执行链路，方便审计和质量复盘。</p></article></div>
      <div class="case-architecture-map" aria-label="供应链多智能体架构九组件">
        <article><span>01</span><h3>Web UI</h3><p>业务用户用自然语言发起供应链问题。</p></article>
        <article><span>02</span><h3>Chatbot App</h3><p>承接对话、上下文和前端状态。</p></article>
        <article><span>03</span><h3>API 网关与函数</h3><p>把前端请求接入后端服务。</p></article>
        <article><span>04</span><h3>企业身份平台</h3><p>统一用户认证与访问入口。</p></article>
        <article><span>05</span><h3>会话数据存储</h3><p>保存对话历史和应用配置。</p></article>
        <article><span>06</span><h3>智能体运行平台</h3><p>运行主管智能体和专项智能体。</p></article>
        <article><span>07</span><h3>模型服务</h3><p>提供推理和工具调用能力。</p></article>
        <article><span>08</span><h3>工具网关 + MCP</h3><p>通过 API 和企业服务访问外部数据源。</p></article>
        <article><span>09</span><h3>可观测性</h3><p>追踪智能体状态、工具调用和执行链路。</p></article>
      </div>
      <div class="case-board-questions"><div><small>代理分工</small><h3>职责拆开，准确性才有空间提升。</h3><p>实践中的一个重要经验是：把所有能力塞进单一智能体提示词，提示词越长，SQL 生成准确性越容易下降。拆成主管-员工模式后，每个代理可以有自己的语义、工具、错误重试和质量检查；查询代理还能分析 SQL 报错并自动重试，而不是把错误直接甩给业务人员。</p></div><ol><li><span>01</span><p>主管代理：解读用户意图，判断简单查询还是复杂分析，并协调流程。</p></li><li><span>02</span><p>查询代理：自然语言转 SQL，执行基准查询和周期比较。</p></li><li><span>03</span><p>详细代理：发现异常后，按类别、时间段和区域执行多维钻取。</p></li><li><span>04</span><p>研究代理：从多个角度调查根因。</p></li><li><span>05</span><p>汇总代理：将结果整理为结构化业务报告。</p></li><li><span>06</span><p>行动代理：生成通知、审批摘要和工单。</p></li></ol></div>
    </section>

    <section class="case-section" data-section id="design-decisions">
      <p class="eyebrow">Semantic layer + MCP</p>
      <h2>两个设计决策，决定系统能不能长期可靠运行。</h2>
      <div class="case-fit-grid"><article class="case-fit-card case-fit-card--yes"><small>业务术语语义层</small><h3>最常见错误不是 SQL 语法，而是业务定义误解。</h3><ul><li>“滞销库存”“履行率”“未付款订单”在不同企业有不同口径</li><li>把业务术语到 SQL 表达式的映射直接注入查询代理的提示词</li><li>例如将“履行率”定义为 <code>COUNT(status='delivered') / COUNT(*)</code></li><li>强制所有查询包含日期筛选器，避免无边界扫描</li></ul></article><article class="case-fit-card case-fit-card--yes"><small>MCP 数据源解耦</small><h3>智能体不直接绑死某个数据库或查询引擎。</h3><ul><li>工具网关把 API 和现有服务转换为 MCP 工具</li><li>底层查询引擎迁移时，优先替换 MCP 服务实现</li><li>渠道伙伴和数据源变化时，智能体代码不必反复改</li><li>认证、凭据交换、工具发现和外发调用由网关与身份层统一处理</li></ul></article></div>
      <aside class="case-callout"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-shield"></use></svg></span><div><small>企业级边界</small><h3>Agent 能行动，不代表可以无限行动。</h3><p>供应链场景里的工具调用要绑定身份、权限、日期范围、业务口径和审批边界。可以让 Agent 生成订单放行请求摘要，但是否放行、放行多少、由谁审批，仍要回到企业的责任体系。</p></div></aside>
    </section>

    <section class="case-section" data-section id="workflow">
      <p class="eyebrow">Channel fulfillment analysis</p>
      <h2>一次“渠道履行情况如何”的提问，可以形成从查询到行动的完整链路。</h2>
      <p>以下数字来自团队过往项目的匿名化履行分析，用来说明查询、钻取、归因和行动链路。客户身份、完整样本和测量口径未公开，不能把这些数字延伸为所有企业都可复制的收益。月度运营回顾中，运营经理提出问题：“我们渠道合作伙伴上个月的订单履行情况如何？有哪些需要关注？”</p>
      <ol class="case-process"><li><span>01</span><div><h3>主管代理识别复杂分析请求</h3><p>它不直接给一句笼统回答，而是将任务路由给查询代理，先建立可计算基线。</p></div></li><li><span>02</span><div><h3>查询代理映射业务定义并执行 SQL</h3><p>“履行绩效”被映射到语义层定义，按渠道执行查询，并与上月数据进行比较。</p></div></li><li><span>03</span><div><h3>渠道 B 履行率异常，环比下降 6.8%</h3><p>系统识别这不是普通波动，需要进入详细代理的多维钻取。</p></div></li><li><span>04</span><div><h3>详细代理定位到品类与时间窗口</h3><p>异常集中在鞋类，并且主要发生在当月第二周和第三周。</p></div></li><li><span>05</span><div><h3>研究代理发现信用控制触发</h3><p>渠道 B 的未付款订单率从 8% 上升到 22%，约 340 个订单因此被冻结。</p></div></li><li><span>06</span><div><h3>汇总与行动代理推动后续处理</h3><p>系统生成根因报告、行动建议、渠道客户经理通知、信用控制团队通知和订单放行请求摘要，进入审批流程。</p></div></li></ol>
      <div class="case-metric-strip"><div><strong>30 秒</strong><span>从提问到结构化分析和行动材料</span></div><div><strong>-6.8%</strong><span>渠道 B 履行率环比异常</span></div><div><strong>8% → 22%</strong><span>未付款订单率上升触发信用控制</span></div><div><strong>约 340</strong><span>被冻结订单进入后续放行判断</span></div></div>
    </section>

    <section class="case-section" data-section id="operating-model">
      <p class="eyebrow">How leaders should read it</p>
      <h2>企业主不需要先买一整套大平台，可以从一个高频决策问题开始。</h2>
      <p>起点不必很大。先选一个能明确算成本、能明确追责、能明确行动人的问题，例如渠道履行异常、库存冻结、缺货风险、物流延迟或高退货 SKU。把数据源、业务术语、审批边界和人工复核路径定义清楚，再让多智能体系统接管查询、分析、材料生成和通知。</p>
      <div class="case-adoption-grid"><article><span>01</span><small>选择问题</small><h3>从一个真问题开始</h3><p>不要先问“我们能不能做 Agent”，而是问“哪个供应链问题每天都在消耗人力和响应时间”。</p></article><article><span>02</span><small>定义口径</small><h3>先建语义层</h3><p>履行率、滞销、缺货、冻结、异常订单等术语要有统一计算口径，否则自然语言查询只会更快地产生错误。</p></article><article><span>03</span><small>接入工具</small><h3>用 MCP 包住数据源</h3><p>ERP、WMS、TMS、数据湖、审批系统和消息系统不必一次性重构，但要以可治理工具形式暴露给 Agent。</p></article><article><span>04</span><small>保留责任</small><h3>行动必须有审批边界</h3><p>Agent 可以建议和生成材料，关键库存、信用和客户动作仍应由授权人员确认。</p></article><article><span>05</span><small>复盘质量</small><h3>让每次分析可审查</h3><p>同样的问题和数据应产生一致路径，SQL、工具调用、根因判断和通知记录都要能回看。</p></article><article><span>06</span><small>逐步扩展</small><h3>从局部闭环到控制面升级</h3><p>先跑通一个问题的收集、查询、洞察和行动，再扩展到更多渠道、品类和供应链任务。</p></article></div>
      <div class="case-reading-note"><strong>项目判断</strong><p>这类项目的评估重点，不是模型回答得多漂亮，而是业务团队与智能体共同完成的决策流程能否减少等待、减少误判、缩短行动链路，并让负责人愿意在真实运营会上使用它。</p></div>
    </section>

    <section class="case-section" data-section id="references">
      <p class="eyebrow">Technical context</p>
      <h2>技术选型要服务于业务闭环，而不是把供应链变成另一个演示场。</h2>
      <p>ForFlow 的重点是把模型、工具、身份、数据源和可观测性组织成一套可运行的系统。正式项目仍要回到企业自身的数据结构、业务口径、权限模型、审批流程和运营节奏。</p>
      <div class="case-reference-list"><a href="https://aws.amazon.com/blogs/industries/how-multi-agent-ai-turns-supply-chain-data-into-decisions-and-actions/" target="_blank" rel="noopener noreferrer">团队过往项目的公开资料</a><a href="https://modelcontextprotocol.io/docs/getting-started/intro" target="_blank" rel="noopener">Model Context Protocol 公开资料</a></div>
    </section>
  </article>
</div>
<section class="case-related">
  <div class="container">
    <div class="case-related-head"><div><p class="eyebrow">Related cases</p><h2>继续看相邻问题，建立完整判断。</h2></div><a class="text-link" href="cases.html">查看全部案例&博客 →</a></div>
    <div class="case-related-grid">
      <a class="case-related-card" href="case-healthcare-agent-roi.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/healthcare-care-chain-sana-plain.png"><div><small>高合规智能体</small><h3>医疗工作流中的受限多智能体架构</h3><p>状态机、人工升级、模型专项化和 ROI 验证</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-automotive-dfmea-ontology-agent.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/automotive-dfmea-bpillar-hero.png"><div><small>汽车工程知识资产</small><h3>B 柱 DFMEA 如何沉淀组织记忆</h3><p>工程本体、RFLP、多智能体和知识流失治理</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-manufacturing-pid-intelligence.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/thumb-manufacturing-pid.webp"><div><small>制造业知识资产化</small><h3>P&amp;ID 图纸如何变成可查询运营知识</h3><p>静态图纸、知识图谱、工程师复核和可追溯问答</p><span>继续阅读 <b>↗</b></span></div></a>
    </div>
  </div>
</section>
<section class="case-next-cta"><div class="container case-next-cta__inner"><div><small>把案例映射到你的企业</small><h2>先找一个供应链问题，把“看见数据”推进到“采取行动”。</h2><p>把数据源、业务口径、行动边界和验收指标摆清楚，再判断这条决策流程是否值得进入试点。</p></div><div><a class="btn btn--light" href="navigator.html">开始 AI 场景诊断 →</a><a class="btn btn--ghost" href="cases.html">返回案例&博客</a></div></div></section>
<section class="case-source-foot" id="case-source" aria-labelledby="supply-case-source-title"><div class="container"><div class="case-source-card"><span class="case-source-card__icon"><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><div><small>ForFlow 团队经验与公开依据</small><h2 id="supply-case-source-title">团队做过这类供应链智能体，匿名数据用于说明工作链路。</h2><p>客户名称、完整样本和观察期没有公开。页面保留可披露的架构与分析结果；新项目必须按自己的业务口径重新测量。</p><a href="https://aws.amazon.com/blogs/industries/how-multi-agent-ai-turns-supply-chain-data-into-decisions-and-actions/" target="_blank" rel="noopener noreferrer">查看团队过往项目的公开资料 <span aria-hidden="true">↗</span></a></div></div></div></section>
'''
(ROOT/'case-supply-chain-agentic-decision.html').write_text(page('多智能体 AI 如何将供应链数据转化为决策与行动','ForFlow 团队供应链实践：用多智能体、语义层和 MCP 把数据可见性推进到查询、洞察和行动闭环。','case-supply-chain-agentic-decision',supply_chain_agentic_body,'case-detail-page case-theme--supply case-study-v2'),encoding='utf-8')

financial_bda_body='''
<section class="case-study-hero case-study-hero--financial">
  <div class="container">
    <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="cases.html">案例&博客</a><span>/</span><strong>金融文档自动化</strong></nav>
    <div class="case-study-hero__grid">
      <div>
        <div class="case-study-meta"><span>ForFlow 文档自动化方法</span><span>字段蓝图</span><span>人工复核</span><span>JSON / CSV 输出</span></div>
        <h1><span class="mobile-title-line">把金融文档提取</span><span class="mobile-title-line">接入可复核的</span><span class="mobile-title-line">业务流程。</span></h1>
        <p class="case-study-lead">金融团队经常处理税表、对账单和合同。格式、结构与字段命名各不相同，传统 OCR 很难稳定接入下游流程。ForFlow 的做法是先定义字段蓝图，再把提取、校验、人工复核和系统写回接成一条链。</p>
        <div class="case-study-actions"><a class="btn btn--green" href="#blueprint">先看蓝图设计 ↓</a><a class="btn btn--ghost" href="#documents">查看四类文档 ↘</a></div>
      </div>
      <figure class="case-study-hero__media case-study-hero__media--scene">
        <img alt="中国金融运营团队审核文档自动化提取结果的办公场景" decoding="async" fetchpriority="high" loading="eager" src="assets/cases/financial-bda-document-automation-hero.png">
        <figcaption>文档自动化不是把纸面内容搬进系统，而是让业务字段、验证规则和下游动作可以被稳定复用。</figcaption>
      </figure>
    </div>
    <div aria-label="本案例的交付证据结构" class="case-proof-rail"><div><strong>4 类文档</strong><span>银行对账单、W-2、1099-B、供应商合同</span></div><div><strong>Blueprint</strong><span>用字段、类型、说明和验证规则定义提取地图</span></div><div><strong>JSON / CSV</strong><span>输出直接进入会计、税务、合同和审查流程</span></div><div><strong>可解释性</strong><span>用置信度与视觉定位帮助人工复核关键字段</span></div></div>
    <p class="case-proof-note">这套方法来自 ForFlow 团队成员的过往文档自动化经验。页面中的四类文档用于说明字段蓝图与复核流程，不代表某家金融机构的项目结果；效率和准确率要用企业自己的样本重新测量。</p>
  </div>
</section>
<div class="container case-detail-shell case-story-shell">
  <aside class="case-toc"><div class="case-toc-inner"><small>本页目录</small><nav data-scrollspy><a class="is-active" href="#overview">业务问题</a><a href="#blueprint">Blueprint 蓝图</a><a href="#documents">四类文档</a><a href="#bank">银行对账单</a><a href="#w2">W-2 表格</a><a href="#b1099">1099-B</a><a href="#contract">供应商合同</a><a href="#design">蓝图策略</a><a href="#production">生产落地</a><a href="#references">官方资料</a></nav><a class="case-toc-source" href="#case-source">案例价值 ↘</a></div></aside>
  <article>
    <section class="case-section case-overview" data-section id="overview">
      <p class="eyebrow">Document operations</p>
      <h2>金融文档自动化的难点，不是 OCR 识别率，而是字段能否进入真实业务流程。</h2>
      <p>金融团队经常处理税务表格、贷款报表、采购订单、银行对账单和供应商合同。文档看起来都是“表格和文字”，但真正进入业务系统时，每一种文档都有不同字段、不同版式、不同章节结构、不同命名方式，以及不同的校验要求。</p>
      <p>传统 OCR 通常解决的是“把图片里的字识别出来”。但业务团队真正需要的是：每笔交易的日期、金额和描述是否完整；W-2 的联邦税、州税、Box 12 代码和 Box 14 自由填写项是否被正确分组；1099-B 里同一证券在不同页面、不同描述下能否保持一致；供应商合同里的参与方、义务、期限和终止条件能否被结构化输出。</p>
      <p>文档理解引擎不是简单的 OCR 升级。它要理解上下文、章节逻辑和字段关系，把原始文档转换为结构化数据；同时提供自定义提取配置、置信度评分和视觉定位，让低置信度结果进入人工复核。</p>
      <div class="case-question-panel">
        <div><small>本篇核心问题</small><h3>如何把“金融文档被读懂”，变成“字段被验证、结果可接入、异常可复核”？</h3></div>
        <div class="case-goal"><small>企业主视角</small><p>真正要买的不是一次 PDF 解析能力，而是一套能持续处理不同文档、稳定输出字段、让人工只复核低置信度或高风险项的运营能力。</p></div>
      </div>
      <div class="case-fact-grid">
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-data"></use></svg></span><div><small>文档类型</small><strong>对账单、税表、交易报表、合同</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-layers"></use></svg></span><div><small>核心资产</small><strong>按业务流程设计的自定义 Blueprint</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-shield"></use></svg></span><div><small>风险控制</small><strong>字段验证、置信度、视觉定位与人工复核</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><div><small>下游动作</small><strong>会计入账、税务处理、合同审查、风控校验</strong></div></div>
      </div>
    </section>

    <section class="case-section" data-section id="blueprint">
      <p class="eyebrow">Blueprint</p>
      <h2>Blueprint 蓝图，是把金融文档提取变成稳定工作流的配置地图。</h2>
      <p>核心配置单元是字段蓝图。它不是普通提示词，而是一份定义数据提取方式的配置：说明正在处理哪类文档，需要提取哪些字段，字段属于什么类型，如何组织数组或自定义对象，以及输出应该如何进入下游系统。</p>
      <div class="case-blueprint-flow" aria-label="ForFlow 文档自动化字段蓝图工作流">
        <article><small>01</small><h3>文档类型</h3><p>银行对账单、W-2、1099-B、合同等。</p></article>
        <span aria-hidden="true">→</span>
        <article><small>02</small><h3>Blueprint</h3><p>字段、类型、说明、验证规则和输出结构。</p></article>
        <span aria-hidden="true">→</span>
        <article><small>03</small><h3>文档理解与提取</h3><p>理解版式、章节、上下文和表格关系。</p></article>
        <span aria-hidden="true">→</span>
        <article><small>04</small><h3>验证复核</h3><p>置信度、视觉定位、规则校验和人工处理。</p></article>
        <span aria-hidden="true">→</span>
        <article><small>05</small><h3>JSON / CSV</h3><p>进入会计、税务、合同或风控系统。</p></article>
      </div>
      <p>可以把字段蓝图理解为一张提取地图：它告诉系统从哪里找什么信息，以什么类型表达，如何把多行表格、多组税务字段和自由文本条款变成结构化结果。金融场景通常需要自定义蓝图，因为字段口径和下游流程会因企业而异。</p>
      <aside class="case-callout"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-bulb"></use></svg></span><div><small>判断标准</small><h3>蓝图设计质量，决定提取结果的准确性上限。</h3><p>字段是否拆得足够细、数组和对象是否符合业务系统、自由文本是否单独归类、金额字段是否定义为数字、同类文档是否需要多份蓝图，这些决定了输出能不能直接进入下游，而不是停留在“AI 看起来读出来了”。</p></div></aside>
    </section>

    <section class="case-section" data-section id="documents">
      <p class="eyebrow">Four document families</p>
      <h2>四类文档，分别验证交易明细、税务字段、上下文一致性和合同条款提取。</h2>
      <div class="case-document-grid">
        <article><span>01</span><small>Bank statement</small><h3>银行对账单</h3><p>跨页交易明细、借贷金额、描述和参考编号。</p></article>
        <article><span>02</span><small>W-2</small><h3>薪资税务表格</h3><p>联邦税、州税、Box 12 代码金额对和 Box 14 自由项。</p></article>
        <article><span>03</span><small>1099-B</small><h3>证券交易税表</h3><p>同一证券跨页面、跨描述的一致识别和交易字段提取。</p></article>
        <article><span>04</span><small>Vendor contract</small><h3>供应商合同</h3><p>非标准版式下的参与方、义务、期限、保密和终止条款。</p></article>
      </div>
    </section>

    <section class="case-section" data-section id="bank">
      <p class="eyebrow">Scenario 01</p>
      <h2>银行对账单：核心任务是把跨页交易明细稳定送入会计工作流。</h2>
      <p>银行对账单记录账户在特定周期内的全部金融活动，包括存款、取款和手续费。它的挑战在于交易记录数量大、经常跨越多页、格式和描述方式因银行而异。对财务团队而言，核心不是“读完整份 PDF”，而是精确捕获每笔交易的日期、金额、描述和参考编号，再输入自动化会计分类或对账流程。</p>
      <div class="case-schema-block"><div><small>蓝图设计</small><h3>主字段与自定义类型</h3></div><pre><code>主字段：
- transactions: [TRANSACTION_DETAILS]

TRANSACTION_DETAILS：
  - date（日期）
  - description（描述）
  - debit（借方）: number
  - credit（贷方）: number</code></pre></div>
      <p>提取结果能够以 CSV、JSON 和原始数据格式输出，便于对接下游会计系统。试点应重点测量人工录入错误、对账时长和异常复核量；实际变化必须用企业自己的文档样本验证。</p>
    </section>

    <section class="case-section" data-section id="w2">
      <p class="eyebrow">Scenario 02</p>
      <h2>W-2 表格：标准表格不等于简单表格，关键在字段分组和代码配对。</h2>
      <p>W-2 表格用于报告收入和已预扣税款。它的结构看似标准，但信息维度复杂：联邦税和州税信息在表格上不一定以业务系统需要的方式分组；Box 12 可能包含多个代码，每个代码都对应不同薪酬或福利类型；Box 14 是自由填写项，雇主可以写入不属于其他专属格的信息，必须单独归类，不能污染结构化字段。</p>
      <div class="case-schema-block"><div><small>蓝图设计</small><h3>字段组与自定义类型</h3></div><pre><code>主字段：
- employer_info: EmployerInfo
- employee_general_info: EmployeeInfo
- federal_tax_info: FederalTaxInfo
- federal_wage_info: FederalWageInfo
- filing_info: FilingInfo
- state_taxes_table: [StateTaxInfo]
- codes: [CodeAmount]
- nonqualified_plans_income: number
- other

自定义类型：
1. EmployerInfo：ein、雇主名称、地址、邮编、控制编号
2. EmployeeInfo：社安号、姓名、地址、邮编
3. FederalWageInfo：应税工资、社保工资、医保工资、社保小费
4. FederalTaxInfo：联邦所得税、社保税、医保税、分配小费
5. StateTaxInfo：州名、雇主州税 ID、州应税工资、州所得税、地方工资、地方所得税、地方名称
6. CodeAmount：code、amount: number
7. FilingInfo：OMB 编号、验证码</code></pre></div>
      <p>提取结果重点解决三类复杂场景：联邦税和州税信息被正确关联分组；Box 12 的多个代码-金额对被准确配对；Box 14 的自由填写内容被单独归类。这样输出才能进入税务处理，而不是让人工重新拆字段。</p>
    </section>

    <section class="case-section" data-section id="b1099">
      <p class="eyebrow">Scenario 03</p>
      <h2>1099-B：真正考验的是跨交易记录的上下文一致性。</h2>
      <p>IRS 1099-B 用于追踪证券交易活动、经纪商促成的交易以及易货交易。它的复杂性在于，同一证券的多笔交易记录可能使用不同描述方式出现，系统需要在整个文档处理过程中保持上下文一致性，正确识别并关联同一证券的不同交易。</p>
      <div class="case-schema-block"><div><small>蓝图设计</small><h3>交易字段结构</h3></div><pre><code>TRANSACTION_DETAILS：
  - security_description（证券描述）
  - quantity_sold（卖出数量）: number
  - date_acquired（取得日期）
  - date_sold_or_disposed（卖出或处置日期）
  - proceeds（所得金额）: number
  - cost_or_other_basis（成本或其他基础）: number
  - gainloss_amount（盈亏金额）: number
  - additional_information（附加信息）</code></pre></div>
      <p>在该场景中，系统需要统一识别同一证券描述符，即使它以不同方式出现在不同交易记录中。这验证的是文档级上下文理解能力，而不是逐行孤立解析。对税务和投资运营团队来说，这类一致性直接影响成本基础、盈亏计算和后续申报质量。</p>
    </section>

    <section class="case-section" data-section id="contract">
      <p class="eyebrow">Scenario 04</p>
      <h2>供应商合同：没有标准模板时，自定义蓝图就是业务规则的载体。</h2>
      <p>供应商合同没有统一行业模板，每家企业都需要根据自身运营工作流和法务审查需求定义字段。这是典型的“无内置蓝图”场景，完全依赖自定义蓝图把非标准文本转换为结构化条款。</p>
      <div class="case-schema-block"><div><small>蓝图设计</small><h3>合同要素提取</h3></div><pre><code>主字段：
- PARTICIPANT_DETAILS: PARTICIPANT_DETAILS
- effective_date（生效日期）
- time_period（时间周期）
- participant_requirements: PARTICIPANT_REQUIREMENTS
- confidentiality_obligations（保密义务）
- TERM_AND_TERMINATION: TERM_AND_TERMINATION

自定义类型：
1. PARTICIPANT_DETAILS：参与方名称、授权代表
2. PARTICIPANT_REQUIREMENTS：分配资源、参与方义务、参与方限制
3. TERM_AND_TERMINATION：合同期限、终止条件</code></pre></div>
      <p>提取结果输出为结构化 JSON，可对接合同管理系统或法务审查工作流。对合同场景来说，不能只看字段是否提取出来，还要看低置信度条款、缺失条款、异常终止条件和高风险义务是否能进入人工复核队列。</p>
    </section>

    <section class="case-section" data-section id="design">
      <p class="eyebrow">Blueprint strategy</p>
      <h2>一份蓝图还是多份蓝图，取决于工作流差异和文档版式差异。</h2>
      <p>通常情况下，针对特定文档类型创建一份自定义蓝图即可满足提取需求。但如果同类文档服务于不同工作流，或者不同来源文档版式差异显著，就应考虑创建多份蓝图。</p>
      <div class="case-fit-grid"><article class="case-fit-card case-fit-card--yes"><small>适合一份蓝图</small><h3>字段目标稳定，格式差异可控。</h3><ul><li>同类银行对账单只需要交易明细</li><li>W-2 输出字段稳定，差异集中在缺失项</li><li>下游系统能容忍可选字段为空</li><li>人工复核主要关注低置信度字段</li></ul></article><article class="case-fit-card case-fit-card--yes"><small>适合多份蓝图</small><h3>工作流或版式差异会改变输出结构。</h3><ul><li>同样是对账单，一个流程只要交易明细，另一个还要账户汇总</li><li>不同银行对账单版式差异过大</li><li>合同按采购、外包、渠道合作需要不同条款集合</li><li>高风险字段需要不同验证规则和人工升级路径</li></ul></article></div>
      <p>字段蓝图创建完成后，可以作为工作流标准组件复用。输入文档字段不同时，系统可能返回略有差异的结构化输出。由于输出是 JSON，下游规则可以处理可选字段、缺失字段和低置信度字段；关键是提前定义哪些字段可以为空，哪些字段必须触发人工复核。</p>
    </section>

    <section class="case-section" data-section id="production">
      <p class="eyebrow">Production workflow</p>
      <h2>生产环境里的文档 AI，必须同时考虑准确性、可解释性、成本和合规。</h2>
      <p>金融文档处理的终点不是“模型回答正确”，而是“字段进入系统后不会制造新的运营风险”。因此，生产化需要把确定性规则与 AI 提取结合起来：标准格式字段可以用规则和类型约束处理；需要上下文理解的内容，例如合同义务、1099-B 证券描述、自由填写项归类，则交给模型理解，再通过置信度、视觉定位和人工复核闭环控制风险。</p>
      <ol class="case-process"><li><span>01</span><div><h3>文档分类与蓝图匹配</h3><p>先判断文档类型，再使用对应自定义 Blueprint，避免用一个泛化提示词处理所有格式。</p></div></li><li><span>02</span><div><h3>字段提取与类型约束</h3><p>金额、日期、代码、数组和对象都要按业务系统需要输出，而不是只返回自然语言摘要。</p></div></li><li><span>03</span><div><h3>置信度与视觉定位复核</h3><p>低置信度字段、高金额字段、关键合同条款和税务代码进入人工复核队列。</p></div></li><li><span>04</span><div><h3>下游系统集成</h3><p>JSON / CSV 输出进入会计、税务、合同管理和风控系统，异常项保留可追溯记录。</p></div></li></ol>
      <div class="case-reading-note"><strong>三个核心收获</strong><p>第一，自定义蓝图的设计质量决定输出可用性；第二，混合确定性规则与 AI 上下文提取，通常比单一路径更可靠；第三，输出即集成，只有 JSON / CSV 结构能直接对接业务系统，文档 AI 才能从演示走向运营。</p></div>
      <aside class="case-callout"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-shield"></use></svg></span><div><small>敏感数据提醒</small><h3>金融文档含有高度敏感信息，生产环境必须按机构安全和合规要求设计。</h3><p>处理税务、银行、合同和个人身份信息时，应遵循所在机构的网络安全、隐私、数据留存、访问控制和适用地区监管要求，例如 GDPR 或行业特定规则。系统设计要把权限、审计、加密、人工复核和异常升级作为默认能力，而不是上线后补丁。</p></div></aside>
    </section>

    <section class="case-section" data-section id="references">
      <p class="eyebrow">Technical context</p>
      <h2>ForFlow 的文档自动化方法，把提取能力做成可配置、可复用、可审计的工作流组件。</h2>
      <p>在企业项目中，文档理解引擎负责把非结构化或半结构化文档转成字段；数据治理、权限、人工复核和系统集成再把它接成完整流程。</p>
      <div class="case-reference-list"><a href="https://aws.amazon.com/blogs/machine-learning/process-financial-documents-using-amazon-bedrock-data-automation/" target="_blank" rel="noopener noreferrer">团队过往方法的公开资料</a></div>
    </section>
  </article>
</div>
<section class="case-related">
  <div class="container">
    <div class="case-related-head"><div><p class="eyebrow">Related cases</p><h2>继续看相邻问题，建立完整判断。</h2></div><a class="text-link" href="cases.html">查看全部案例&博客 →</a></div>
    <div class="case-related-grid">
      <a class="case-related-card" href="case-supply-chain-agentic-decision.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/supply-chain-agentic-decision-hero.png"><div><small>供应链决策系统</small><h3>多智能体 AI 如何把数据转化为行动</h3><p>语义层、MCP、根因归因和行动通知</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-healthcare-agent-roi.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/healthcare-care-chain-sana-plain.png"><div><small>高合规智能体</small><h3>医疗工作流中的受限多智能体架构</h3><p>状态机、人工升级、模型专项化和 ROI 验证</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-manufacturing-pid-intelligence.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/thumb-manufacturing-pid.webp"><div><small>制造业知识资产化</small><h3>P&amp;ID 图纸如何变成可查询运营知识</h3><p>静态图纸、知识图谱、工程师复核和可追溯问答</p><span>继续阅读 <b>↗</b></span></div></a>
    </div>
  </div>
</section>
<section class="case-next-cta"><div class="container case-next-cta__inner"><div><small>把方法映射到你的企业</small><h2>先选一类高频金融文档，把字段、复核和下游系统串起来。</h2><p>判断文档类型、蓝图粒度、人工复核边界和系统集成路径，再决定是否进入验证。</p></div><div><a class="btn btn--light" href="navigator.html">开始 AI 场景诊断 →</a><a class="btn btn--ghost" href="cases.html">返回案例&博客</a></div></div></section>
<section class="case-source-foot" id="case-source" aria-labelledby="financial-case-source-title"><div class="container"><div class="case-source-card"><span class="case-source-card__icon"><svg aria-hidden="true" class="ff-icon"><use href="#i-data"></use></svg></span><div><small>ForFlow 团队经验与公开依据</small><h2 id="financial-case-source-title">团队做过文档自动化，页面把方法和复核边界讲清楚。</h2><p>原项目资料用于说明字段蓝图和四类文档的处理方式。是否减少错误、缩短对账或降低复核量，仍需用企业样本实测。</p><a href="https://aws.amazon.com/blogs/machine-learning/process-financial-documents-using-amazon-bedrock-data-automation/" target="_blank" rel="noopener noreferrer">查看团队过往方法的公开资料 <span aria-hidden="true">↗</span></a></div></div></div></section>
'''
(ROOT/'case-financial-bda-document-automation.html').write_text(page('把金融文档提取接入可复核工作流','ForFlow 文档自动化方法：围绕银行对账单、税务文件和供应商合同，把字段提取变成可复用、可验证、可接入下游系统的工作流。','case-financial-bda-document-automation',financial_bda_body,'case-detail-page case-theme--financial case-study-v2'),encoding='utf-8')

vanguard_virtual_analyst_body='''
<section class="case-study-hero case-study-hero--vanguard">
  <div class="container">
    <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="cases.html">案例&博客</a><span>/</span><strong>先锋集团虚拟分析师</strong></nav>
    <div class="case-study-hero__grid">
      <div>
        <div class="case-study-meta"><span>ForFlow 团队实践</span><span>AI-ready data</span><span>语义层</span><span>治理与评估</span></div>
        <h1><span class="mobile-title-line">先锋集团虚拟分析师：</span><span class="mobile-title-line">AI 就绪数据的</span><span class="mobile-title-line">八项原则与实践。</span></h1>
        <p class="case-study-lead">当金融分析师需要查询复杂数据集时，即使是基本问题也可能变成复杂 SQL、排队需求和数天等待。对话式 AI 看似可以提供即时响应，但真正的瓶颈往往不是底层模型，而是企业有没有一套能被 AI 可靠理解、查询、治理和持续评估的数据基础设施。</p>
        <div class="case-study-actions"><a class="btn btn--green" href="#principles">查看八项原则 ↓</a><a class="btn btn--ghost" href="#stack">查看技术栈 ↘</a></div>
      </div>
      <figure class="case-study-hero__media case-study-hero__media--scene">
        <img alt="中国金融分析团队围绕 AI 就绪数据和虚拟分析师工作台协作" decoding="async" fetchpriority="high" loading="eager" src="assets/cases/vanguard-virtual-analyst-hero.png">
        <figcaption>虚拟分析师的可靠性，取决于数据产品、语义定义、质量检查和持续评估能否先被组织化。</figcaption>
      </figure>
    </div>
    <div aria-label="本案例的交付证据结构" class="case-proof-rail"><div><strong>SQL 等待</strong><span>分析师基本问题也要依赖复杂查询和数据团队排期</span></div><div><strong>数据架构</strong><span>项目重点从模型选择转向 AI 就绪型数据基础</span></div><div><strong>八项原则</strong><span>数据产品、治理、元数据、语义层、示例库和评估</span></div><div><strong>可复制框架</strong><span>从单个虚拟分析师扩展到多个业务部门</span></div></div>
    <p class="case-proof-note">ForFlow 团队成员在原组织中参与过这类虚拟分析师与 AI-ready data 工作。数天到数分钟、高精度 SQL、减少数据团队工作量和跨业务单元采用均按原项目公开口径保留；公开资料没有给出样本量、百分比和观察期，因此不补写更精确的 KPI。</p>
  </div>
</section>
<div class="container case-detail-shell case-story-shell">
  <aside class="case-toc"><div class="case-toc-inner"><small>本页目录</small><nav data-scrollspy><a class="is-active" href="#overview">核心认知</a><a href="#collaboration">组织协作</a><a href="#stack">技术架构</a><a href="#principles">八项原则</a><a href="#metadata">元数据目录</a><a href="#semantic-layer">语义层与示例库</a><a href="#quality">质量与评估</a><a href="#outcomes">可衡量成果</a><a href="#next-step">下一步</a><a href="#references">参考资料</a></nav><a class="case-toc-source" href="#case-source">团队经验 ↘</a></div></aside>
  <article>
    <section class="case-section case-overview" data-section id="overview">
      <p class="eyebrow">Core insight</p>
      <h2>这是数据架构挑战，不是机器学习挑战。</h2>
      <p>先锋集团是一家全球投资管理公司，采用独特的投资者所有制结构，为个人投资者、机构投资者和金融专业人士提供投资选择、咨询服务和退休服务。其使命围绕维护投资者利益、公平对待每一位投资者，并帮助投资者实现长期投资成功展开。</p>
      <p>当金融分析师需要查询复杂数据集时，他们面对的是一个令人沮丧的现实：即使是基础问题，也要写复杂 SQL，或者把需求交给数据团队排期，响应时间有时长达数天。对话式 AI 可以把“提问到答案”的时间压缩到分钟级，但前提是模型背后有足够清晰、可信、可治理的数据基础。</p>
      <p>随着虚拟分析师项目推进，团队形成了一个根本判断：构建高效的对话式 AI，最复杂的部分不是模型选择，而是数据架构。即使是能力最强的基础模型，如果没有合适的数据产品、元数据、业务定义、权限边界和评估机制，也无法稳定产出企业可依赖的答案。</p>
      <div class="case-question-panel">
        <div><small>本篇核心问题</small><h3>如何让虚拟分析师回答金融问题时，既快、又准、还可审计？</h3></div>
        <div class="case-goal"><small>企业主视角</small><p>真正要建设的不是一个“会聊天的数据助手”，而是一套能把指标口径、权限规则、质量状态和业务语义同时交给 AI 的数据基础设施。</p></div>
      </div>
      <div class="case-fact-grid">
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-data"></use></svg></span><div><small>业务压力</small><strong>复杂 SQL、数据团队排队、洞察获取慢</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-layers"></use></svg></span><div><small>方法转变</small><strong>从模型功能转向 AI-ready data</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-shield"></use></svg></span><div><small>金融约束</small><strong>身份、权限、合规、安全与审计缺一不可</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><div><small>可复制资产</small><strong>数据产品、语义层、示例库和评估套件</strong></div></div>
      </div>
    </section>

    <section class="case-section" data-section id="collaboration">
      <p class="eyebrow">Operating model</p>
      <h2>协作是前提：虚拟分析师先要求组织打破数据、业务和合规之间的墙。</h2>
      <p>构建虚拟分析师团队，需要解决许多企业都面临的组织难题：让传统上各自为政的团队真正协同运作。先锋集团将数据工程师、业务分析师、合规官、安全团队和业务利益相关者汇聚在一起，让每个团队把不可替代的专业知识放进同一套数据工作流。</p>
      <div class="case-value-cards case-value-cards--triple">
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-data"></use></svg></span><small>数据工程师</small><h3>维护技术基础设施。</h3><p>负责数据管道、仓库、目录、低延迟会话和可扩展计算，让虚拟分析师有稳定数据入口。</p></article>
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-bulb"></use></svg></span><small>业务分析师</small><h3>定义财务指标语义。</h3><p>解释指标含义、常见查询模式、业务规则和上下文，让模型知道问题真正指向什么。</p></article>
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-shield"></use></svg></span><small>合规与安全</small><h3>把边界前置。</h3><p>建立身份、角色、查询级授权、数据保留和审计机制，让 AI 能进入金融场景而不越界。</p></article>
      </div>
      <p>这种跨职能协作奠定了 AI 的组织基础。它建立了清晰的所有权模型、语义定义和质量标准。团队意识到：如果没有所有人都能理解和参与的共识，AI 解决方案就缺乏可靠地基。虚拟分析师项目催生的新流程和框架，其价值也超出了最初的 AI 应用本身。</p>
    </section>

    <section class="case-section" data-section id="stack">
      <p class="eyebrow">ForFlow architecture</p>
      <h2>ForFlow 把金融级安全、对话、会话、实验和数据整合放进同一条链。</h2>
      <p>虚拟分析师不能只靠一个模型。生产架构要同时处理自然语言理解、输入输出防护、会话持久化、实验环境、数据仓库和 ETL 编目。</p>
      <div class="case-document-grid">
        <article><span>01</span><small>模型服务</small><h3>自然语言理解</h3><p>理解问题、生成查询路径并组织回答。</p></article>
        <article><span>02</span><small>安全策略</small><h3>输入输出防护</h3><p>控制敏感内容、拒答边界和数据访问范围。</p></article>
        <article><span>03</span><small>运行与会话</small><h3>保存上下文</h3><p>可扩展运行环境负责请求处理，低延迟存储保存会话上下文。</p></article>
        <article><span>04</span><small>存储与实验</small><h3>管理资产和评估</h3><p>保存相关资产，并支持模型、提示词和查询策略评估。</p></article>
        <article><span>05</span><small>数据仓库</small><h3>承载可查询数据</h3><p>让自然语言问题能够转化为结构化查询。</p></article>
        <article><span>06</span><small>数据目录与 ETL</small><h3>统一编目和加工</h3><p>把准确数据整合到可查询环境，并记录来源与更新状态。</p></article>
      </div>
    </section>

    <section class="case-section" data-section id="principles">
      <p class="eyebrow">Eight principles</p>
      <h2>AI 就绪数据的八项原则，来自让 AI 可靠处理企业数据时遇到的真实挑战。</h2>
      <p>这些原则建立在现有数据能力之上，并面向 AI 场景进行扩展。它们解决的不是“如何让模型更聪明”，而是“如何让模型面对企业数据时，有清晰责任、准确语义、可控权限、可测质量和可回归评估”。</p>
      <ol class="case-process">
        <li><span>01</span><div><h3>建立清晰的数据产品和运营模式</h3><p>更高质量的数据需要明确责任归属。数据产品负责人确保数据与业务目标一致，工程管理人员维护技术质量。为关键数据资产指定业务负责人和技术负责人，并书面记录职责范围。</p></div></li>
        <li><span>02</span><div><h3>尽早制定治理和安全措施</h3><p>在项目早期与合规、安全团队协作，建立企业身份管理、基于角色的数据访问控制、查询级授权和数据保留策略；必要时实施行级和列级安全。</p></div></li>
        <li><span>03</span><div><h3>构建统一技术与业务上下文的元数据目录</h3><p>技术元数据描述表、列、类型、血缘、同义词和数据集关系；业务元数据记录指标定义、领域术语、所有权和使用上下文。两者融合，AI 才能同时理解结构与含义。</p></div></li>
        <li><span>04</span><div><h3>实现语义层，让业务元数据真正落地</h3><p>语义层把业务定义、规则和本体转化为可运行逻辑，规范关键指标的定义和数据元素关系，让自然语言问题可以被解释成结构化 SQL 查询。</p></div></li>
        <li><span>05</span><div><h3>开发真实示例库</h3><p>示例库包含问答对和正确数据库映射，可用于少样本提示、评估基准和回归测试。先覆盖最常见查询模式，再根据用户反馈和边缘情况扩充。</p></div></li>
        <li><span>06</span><div><h3>实施自动化数据质量检查</h3><p>通过分布检查、参照检查、对账检查和新鲜度检查持续监控数据可靠性，避免虚拟分析师基于过期、异常或关系失效的数据作答。</p></div></li>
        <li><span>07</span><div><h3>建立变更控制流程</h3><p>把语义定义、示例库和配置文件视为代码，纳入版本控制和 CI/CD。影响 KPI 或 SLA 的变更需要利益相关者审批，同时让改进可以安全上线。</p></div></li>
        <li><span>08</span><div><h3>建立持续评估机制</h3><p>用节省的分析师工时、洞察获取时间、用户满意度和业务影响作为评估基准；维护回归测试套件和用户反馈闭环，并对性能下降自动告警。</p></div></li>
      </ol>
    </section>

    <section class="case-section" data-section id="metadata">
      <p class="eyebrow">Metadata catalog</p>
      <h2>统一元数据目录，解决的是“技术表结构”和“业务问题”之间长期错位。</h2>
      <p>大多数组织维护了完整的技术元数据，却缺乏集成的业务上下文，导致技术实现与业务需求长期错位。虚拟分析师需要一个统一的元数据和目录系统，集中管理技术元数据和业务元数据，并通过 API 对外开放。</p>
      <div class="case-fit-grid">
        <article class="case-fit-card case-fit-card--yes"><small>技术元数据</small><h3>让 AI 知道数据在哪里、如何连接。</h3><ul><li>表和列描述、数据类型</li><li>跨转换的数据血缘</li><li>同义词和分类标识</li><li>数据集之间的关系映射</li></ul></article>
        <article class="case-fit-card case-fit-card--yes"><small>业务元数据</small><h3>让 AI 知道指标到底是什么意思。</h3><ul><li>业务定义和计算规则</li><li>领域专用术语和本体</li><li>业务所有权信息</li><li>使用场景和上下文</li></ul></article>
      </div>
      <p>单一目录将两类元数据融合，使 AI 系统能够生成同时符合技术结构和业务含义的准确查询。实操上，可以先从最常用的数据集入手，系统记录技术元数据，再扩展到其他数据源；对元数据进行版本控制，并持续衡量映射准确性。</p>
    </section>

    <section class="case-section" data-section id="semantic-layer">
      <p class="eyebrow">Semantic layer & examples</p>
      <h2>语义层和示例库，让业务知识从文档变成可执行逻辑。</h2>
      <p>语义层是让元数据目录中定义的业务知识真正可执行的实现层。它将业务定义、规则和本体转化为可运行逻辑，规范关键指标的定义方式和数据元素之间的关系表达。有了这一层，业务分析师用自然语言表达的数据关系，才能被解释并转换为结构化 SQL 查询。</p>
      <div class="case-reading-note"><strong>指标口径示例</strong><p>先锋集团的语义层通过执行业务用户定义的规则，在各部门和系统之间统一维护“客户生命周期价值”的定义。这个指标在不同团队之间历来容易产生争议，但对虚拟分析师来说，争议指标必须先被语义层标准化，才能稳定回答。</p></div>
      <p>真实示例库是另一个关键组成部分。先锋集团构建了包含 50 多个示例的集合，用于三件事：作为少样本提示，引导模型生成正确响应；作为评估基准，衡量模型相对于已知正确答案的准确率；作为回归测试，验证新变更不会破坏现有功能。</p>
      <aside class="case-callout"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-bulb"></use></svg></span><div><small>落地建议</small><h3>先记录最常用 20 个指标，再建立 20 至 30 个高频查询示例。</h3><p>虚拟分析师初期不需要覆盖所有问题。更稳的方式是先覆盖最常问、最影响决策、最容易出错的指标和查询模式，再用用户反馈持续扩充示例库。</p></div></aside>
    </section>

    <section class="case-section" data-section id="quality">
      <p class="eyebrow">Quality & change control</p>
      <h2>数据质量、变更控制和持续评估，是让虚拟分析师长期可信的运营系统。</h2>
      <p>先锋集团建立了可观测性工具，通过四类自动化检查持续监控数据可靠性：分布检查用于检测数值突然飙升或骤降；参照检查验证表之间关系是否持续有效；对账检查确认各系统间数据一致；新鲜度检查确认数据按计划更新。</p>
      <div class="case-document-grid">
        <article><span>01</span><small>分布检查</small><h3>发现异常模式</h3><p>检测数值突然飙升、骤降或分布漂移，避免异常数据进入回答。</p></article>
        <article><span>02</span><small>参照检查</small><h3>验证关系有效</h3><p>确保表之间关系持续成立，例如订单必须指向有效客户。</p></article>
        <article><span>03</span><small>对账检查</small><h3>确认系统一致</h3><p>比较源数据和仓库数据总量或关键金额，避免口径偏移。</p></article>
        <article><span>04</span><small>新鲜度检查</small><h3>保证按时更新</h3><p>确认数据在计划窗口内完成更新，避免回答基于过期数据。</p></article>
      </div>
      <p>同时，语义定义、示例库和配置文件需要像代码一样进入版本控制。影响 KPI 或 SLA 的变更要经过阶梯式审批；上线前做同行评审和回归测试。持续评估则需要把业务指标提前设为基准，例如节省的分析师工时、洞察获取时间、用户满意度和可衡量业务影响。</p>
    </section>

    <section class="case-section" data-section id="outcomes">
      <p class="eyebrow">Measured outcomes</p>
      <h2>专注 AI 就绪数据后，虚拟分析师开始产生可衡量的业务结果。</h2>
      <div class="case-value-cards case-value-cards--triple">
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-chart"></use></svg></span><small>洞察速度</small><h3>从数天缩短至数分钟。</h3><p>复杂财务查询不再总是进入数据团队排队，分析师可以更快获得初步洞察。</p></article>
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><small>自助分析</small><h3>业务用户无需掌握 SQL。</h3><p>自然语言入口降低查询门槛，让分析覆盖面从少数会写查询的人扩展到更多业务用户。</p></article>
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-layers"></use></svg></span><small>复用框架</small><h3>多业务部门采纳推广。</h3><p>元数据、语义层、示例库、质量检查和评估套件成为可复制的数据能力框架。</p></article>
      </div>
      <p>项目还显著减少了数据团队处理日常分析请求的工作量。通过元数据和语义层实现，AI 生成 SQL 查询达到高精度；更重要的是，企业形成了一套可复用框架，让虚拟分析师从单点应用变成数据基础能力的外显界面。</p>
    </section>

    <section class="case-section" data-section id="next-step">
      <p class="eyebrow">Next</p>
      <h2>下一步是知识图谱和 RAG：增强实体关系、跨领域上下文和可解释性。</h2>
      <p>先锋集团正在评估如何利用知识图谱和 RAG 技术进一步增强虚拟分析师能力。知识图谱可以提供明确实体关系、规范化解析和跨领域上下文，从而提升模糊匹配能力、连接推理能力，并增强生成查询的可解释性。</p>
      <p>RAG 系统可以利用示例库提高准确性，并把真实反馈送回评估集。随着使用积累，团队能持续修正模型、语义层和查询策略。这个项目最终解决的不是聊天界面，而是组织的数据基础。</p>
      <div class="case-reading-note"><strong>结论</strong><p>成功的企业级 AI，不仅在于更优算法，更在于更强的数据基础。当数据工程、业务语义、治理合规和持续评估真正协同运作时，AI 模型能力才会转化为高管可以在关键决策中信赖的业务成果。</p></div>
    </section>

    <section class="case-section" data-section id="references">
      <p class="eyebrow">Technical context</p>
      <h2>虚拟分析师不是一个单点工具，而是数据产品化、语义治理和安全运行的组合工程。</h2>
      <p>企业复用这类案例时，应先审视数据产品责任、核心指标口径、数据访问边界、示例库和回归评估，而不是先比较模型排行榜。</p>
      <div class="case-reference-list"><a href="https://aws.amazon.com/blogs/machine-learning/building-ai-ready-data-vanguards-virtual-analyst-journey/" target="_blank" rel="noopener noreferrer">团队过往项目的公开资料</a><a href="https://corporate.vanguard.com/content/corporatesite/us/en/corp/who-we-are.html" target="_blank" rel="noopener noreferrer">Vanguard 官方介绍</a></div>
    </section>
  </article>
</div>
<section class="case-related">
  <div class="container">
    <div class="case-related-head"><div><p class="eyebrow">Related cases</p><h2>继续看相邻问题，建立完整判断。</h2></div><a class="text-link" href="cases.html">查看全部案例&博客 →</a></div>
    <div class="case-related-grid">
      <a class="case-related-card" href="case-financial-bda-document-automation.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/financial-bda-document-automation-hero.png"><div><small>金融文档自动化</small><h3>把文档提取接入可复核工作流</h3><p>字段蓝图、置信度、视觉定位和结构化输出</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-supply-chain-agentic-decision.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/supply-chain-agentic-decision-hero.png"><div><small>供应链决策系统</small><h3>多智能体 AI 如何把数据转化为行动</h3><p>语义层、MCP、根因归因和行动通知</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-healthcare-agent-roi.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/healthcare-care-chain-sana-plain.png"><div><small>高合规智能体</small><h3>医疗工作流中的受限多智能体架构</h3><p>状态机、人工升级、模型专项化和 ROI 验证</p><span>继续阅读 <b>↗</b></span></div></a>
    </div>
  </div>
</section>
<section class="case-next-cta"><div class="container case-next-cta__inner"><div><small>把案例映射到你的企业</small><h2>先选一个高频分析问题，检查它背后的数据是否已经 AI-ready。</h2><p>先把指标定义、数据权限、质量检查、示例库和评估基线摆清楚，再决定虚拟分析师是否值得进入试点。</p></div><div><a class="btn btn--light" href="navigator.html">开始 AI 场景诊断 →</a><a class="btn btn--ghost" href="cases.html">返回案例&博客</a></div></div></section>
<section class="case-source-foot" id="case-source" aria-labelledby="vanguard-case-source-title"><div class="container"><div class="case-source-card"><span class="case-source-card__icon"><svg aria-hidden="true" class="ff-icon"><use href="#i-data"></use></svg></span><div><small>ForFlow 团队经验与公开依据</small><h2 id="vanguard-case-source-title">团队做过这类虚拟分析师和 AI-ready data 工作。</h2><p>页面保留原项目的方向性结果，并明确公开资料没有披露的样本量、百分比和观察期；进入新项目后要重新建立基线。</p><a href="https://aws.amazon.com/blogs/machine-learning/building-ai-ready-data-vanguards-virtual-analyst-journey/" target="_blank" rel="noopener noreferrer">查看团队过往项目的公开资料 <span aria-hidden="true">↗</span></a></div></div></div></section>
'''
(ROOT/'case-vanguard-virtual-analyst.html').write_text(page('先锋集团虚拟分析师：AI 就绪数据的八项原则与实践','以先锋集团虚拟分析师为例，说明金融企业如何通过数据产品、元数据目录、语义层、示例库、质量检查和持续评估构建 AI-ready data。','case-vanguard-virtual-analyst',vanguard_virtual_analyst_body,'case-detail-page case-theme--financial case-study-v2'),encoding='utf-8')

agent_evaluation_first_body='''
<section class="case-study-hero case-study-hero--agent-eval">
  <div class="container">
    <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><a href="cases.html">案例&博客</a><span>/</span><strong>企业 Agent 评估</strong></nav>
    <div class="case-study-hero__grid">
      <div>
        <div class="case-study-meta"><span>ForFlow Agent 评估方法</span><span>Evaluation-first</span><span>ADLC</span><span>生产门控</span></div>
        <h1><span class="mobile-title-line">企业 Agent 上线前，</span><span class="mobile-title-line">先建立</span><span class="mobile-title-line">评估基线。</span></h1>
        <p class="case-study-lead">当企业把 AI Agent 从演示推向生产，最先需要补上的不是更多功能，而是一套能持续判断质量的评估方法。ForFlow 团队把过往生产经验整理成一条 Evaluation-first 路径，从原型验证一直走到上线门控和持续观测。</p>
        <div class="case-study-actions"><a class="btn btn--green" href="#adlc">查看 ADLC 飞轮 ↓</a><a class="btn btn--ghost" href="#metrics">查看评估指标 ↘</a></div>
      </div>
      <figure class="case-study-hero__media case-study-hero__media--scene">
        <img alt="中国企业团队在上线前评审 AI Agent 评估结果和生产 Trace" decoding="async" fetchpriority="high" loading="eager" src="assets/cases/agent-evaluation-first-hero.png">
        <figcaption>Agent 从 Demo 进入生产，真正需要补上的不是一个新模型，而是一套评估、Trace、门控和持续改进机制。</figcaption>
      </figure>
    </div>
    <div aria-label="本案例的交付证据结构" class="case-proof-rail"><div><strong>原型鸿沟</strong><span>Demo 反馈积极，但没人能回答是否生产就绪</span></div><div><strong>评估基线</strong><span>先定义成功、边界、工具和基准数据集</span></div><div><strong>ADLC 飞轮</strong><span>生产 Trace 回流评估集，持续挖掘失败案例</span></div><div><strong>可评估架构</strong><span>工具、代码、安全和多智能体都要能独立归因</span></div></div>
    <p class="case-proof-note">这是 ForFlow 团队成员在原组织中积累并带入现团队的工程方法。文中的阈值、模型切换和工具调用数字来自过往项目示例；用于新项目时，必须按任务、风险、数据和业务容错标准重新设定。</p>
    <div class="case-reading-map" aria-label="长文阅读路线">
      <div><small>长文阅读路线</small><strong>不用一口气读完，按角色先抓住自己的判断点。</strong></div>
      <a href="#overview"><span>决策层</span><b>先看原型鸿沟、ADLC 和结语，判断为什么评估是上线前置条件。</b></a>
      <a href="#start-small"><span>业务负责人</span><b>重点看成功定义、三类 Agent 交付物和 PoC 如何避免范围蔓延。</b></a>
      <a href="#architecture"><span>技术 / 平台团队</span><b>重点看工具策略、可观测性、安全外部化和多智能体解耦。</b></a>
    </div>
  </div>
</section>
<div class="container case-detail-shell case-story-shell">
  <aside class="case-toc"><div class="case-toc-inner"><small>本页目录</small><nav data-scrollspy><a class="is-active" href="#overview">核心问题</a><a href="#why-fail">传统测试为何失效</a><a href="#adlc">ADLC 飞轮</a><a href="#start-small">先定义成功</a><a href="#metrics">自动化评估</a><a href="#continuous">持续测试</a><a href="#observability">可观测性</a><a href="#architecture">可评估架构</a><a href="#security">安全与个性化</a><a href="#conclusion">结语</a></nav><a class="case-toc-source" href="#case-source">案例价值 ↘</a></div></aside>
  <article>
    <section class="case-section case-overview" data-section id="overview">
      <p class="eyebrow">Production gap</p>
      <h2>从原型到生产，企业真正缺的是一套持续判断质量的工程纪律。</h2>
      <p>过去一年，AI 智能体已经从技术探索进入工程落地阶段。越来越多企业开始构建能够调用工具的 LLM 系统、串联多个 API 的编排流程，以及基于内部知识库的对话助手。原型阶段往往进展顺利，Demo 效果不错，业务方反馈积极。</p>
      <p>但当团队尝试把系统推向生产时，关键问题浮现：它真的准备好上线了吗？大多数团队正是在这里遭遇瓶颈。制约因素并非模型能力本身，而是缺少一套工程化质量评判体系，一套能持续回答“它到底好不好”的方法。</p>
      <p>传统软件有单元测试、CI/CD 流水线和明确的 pass/fail 标准。AI 智能体没有。同样的用户输入，今天跑出一个结果，明天换了模型版本，行为可能悄悄变了。开发者甚至无法用一行 assert 语句验证一个多步推理过程是否正确。这本质上是工程纪律问题，而不是模型能力问题。</p>
      <p>本系列共四篇，主线是给企业一套完整的智能体工程纪律路线图。第一篇从评估开始，因为它是一切其他工程实践的地基：没有评估，团队既不知道自己在哪里，也不知道改了之后有没有变好；没有基线，任何 Prompt、工具、模型和检索策略的调整都只是凭感觉试错。</p>
      <div class="case-question-panel">
        <div><small>本篇核心问题</small><h3>如何在企业里判断一个 Agent 是否已经可上线、可回归、可监控、可持续改进？</h3></div>
        <div class="case-goal"><small>企业主视角</small><p>评估不是上线前的形式检查，而是规格说明、质量门控、生产监控和改进驱动力。没有评估，团队既不知道自己在哪里，也不知道改动后有没有变好。</p></div>
      </div>
      <div class="case-fact-grid">
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-bulb"></use></svg></span><div><small>Demo 风险</small><strong>演示惊艳不等于生产可信赖</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-chart"></use></svg></span><div><small>质量信号</small><strong>从断言输出转向评估行为分布</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><div><small>开发生命周期</small><strong>ADLC 把生产数据变成飞轮输入</strong></div></div>
        <div class="case-fact"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-shield"></use></svg></span><div><small>上线边界</small><strong>不达阈值不上线，漂移前置告警</strong></div></div>
      </div>
    </section>

    <section class="case-section" data-section id="why-fail">
      <p class="eyebrow">Why SDLC fails</p>
      <h2>传统软件工程方法对智能体会系统性失效，原因主要有三类。</h2>
      <div class="case-value-cards case-value-cards--triple">
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-chart"></use></svg></span><small>非确定性</small><h3>测试用例今天通过，明天可能失败。</h3><p>LLM 是概率模型。即使 temperature 设为 0，GPU 浮点运算、Mixture-of-Experts 路由和批处理顺序也可能引入差异；目前也没有任何主流模型提供商承诺完全确定性输出。</p></article>
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-data"></use></svg></span><small>Prompt 即代码</small><h3>自然语言改动会改变系统行为。</h3><p>系统 Prompt 末尾加一句话，就可能改变拒答边界、工具调用顺序或输出格式。没有评估，Prompt 工程就是在黑箱里射击。</p></article>
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><small>隐式依赖漂移</small><h3>代码没动，模型行为也会变。</h3><p>模型提供商可能更新安全策略、能力或系统提示。没有持续基线，某天早上 Agent 变得更保守、格式改变或工具倾向变化，团队很难及时发现。</p></article>
      </div>
      <p>软件工程师天然会把 AI 智能体当成“另一种软件”：写逻辑、做测试、上 CI/CD。这个直觉合理，但在 Agent 身上会系统性失效。传统测试假设“给定输入 A，断言输出 B”；智能体更像一个行为分布，应该衡量在一组真实输入和边界输入上的整体表现。</p>
      <p>Prompt 也不再只是配置文本，而是会改变系统行为的源代码。传统代码有 Git diff、代码评审、版本历史和回滚路径；Prompt 改动往往缺少同等纪律。模型本身又是隐式依赖，和 <code>package.json</code> 里可锁定版本的依赖不同：安全微调、能力升级和系统提示调整可能没有详细 Changelog，却足以让业务行为发生变化，而代码库没有任何变更。</p>
      <div class="case-data-table" role="region" aria-label="传统软件测试假设与智能体评估解法对照" tabindex="0">
        <table>
          <thead><tr><th>传统软件测试假设</th><th>Agent 现实</th><th>Evaluation-first 解法</th></tr></thead>
          <tbody>
            <tr><th scope="row">输出可以被 assert 精确断言</th><td>同一输入可能产生多个合理回答，多步推理过程也可能有不同路径。</td><td>在基准数据集上衡量行为分布，评估工具选择、参数提取、边界拒绝和回答质量。</td></tr>
            <tr><th scope="row">代码 diff 能解释行为变化</th><td>Prompt 是自然语言源代码，一句话可能改变拒答边界、工具顺序和输出格式。</td><td>每次 Prompt、工具、模型和检索策略变更都触发回归评估，指标未达阈值不上线。</td></tr>
            <tr><th scope="row">依赖版本可以锁定</th><td>模型、安全策略和外部 API 是会漂移的隐式依赖，代码不动行为也可能改变。</td><td>用生产采样、Trace、漂移检测和告警持续监控质量曲线。</td></tr>
          </tbody>
        </table>
      </div>
      <aside class="case-callout"><span><svg aria-hidden="true" class="ff-icon"><use href="#i-shield"></use></svg></span><div><small>关键判断</small><h3>企业 Agent 的 QA 不是“多写几个单元测试”，而是重建质量测量方式。</h3><p>传统 CI/CD 和 QA 框架不是为概率性、可变性、隐式依赖而设计的。评估体系要覆盖工具选择、参数提取、拒绝边界、延迟、成本、业务可用性和生产漂移。</p></div></aside>
    </section>

    <section class="case-section" data-section id="adlc">
      <p class="eyebrow">ADLC</p>
      <h2>ADLC 不是线性流水线，而是让生产 Trace 反哺评估集的持续飞轮。</h2>
      <p>传统 SDLC 是线性的：需求、设计、开发、测试、上线。上线通常被视为阶段终点。智能体不同，它在生产环境里的每一次对话，都是关于真实行为的宝贵数据。因此，ADLC 更像一个持续运转的飞轮。</p>
      <ol class="case-process">
        <li><span>01</span><div><h3>定义“好”</h3><p>在动手构建之前，先明确什么叫成功：具体评估标准、阈值、边界和基准数据集，而不是一句抽象愿景。</p></div></li>
        <li><span>02</span><div><h3>构建</h3><p>基于清晰定义搭建智能体系统，包括 Prompt、工具、知识源、权限和会话流程。</p></div></li>
        <li><span>03</span><div><h3>评估</h3><p>用定义好的标准系统衡量行为，覆盖常见查询、边界查询、应拒绝或升级人工的查询。</p></div></li>
        <li><span>04</span><div><h3>门控上线</h3><p>评估不只是报告，而是上线通行证。关键指标未达阈值，不部署。</p></div></li>
        <li><span>05</span><div><h3>生产观测</h3><p>上线后持续追踪真实流量下的延迟、成功率、工具调用模式、用户反馈和成本。</p></div></li>
        <li><span>06</span><div><h3>挖掘失败案例</h3><p>从生产 Trace 中找到失败或异常样本，加入评估集，让下一轮迭代更接近真实场景。</p></div></li>
      </ol>
      <figure class="case-figure case-figure--contain case-figure--wide-diagram case-figure--dark-diagram case-figure--mobile-fit">
        <a href="assets/cases/agent-evaluation-dlc-loop.png" target="_blank" rel="noopener" aria-label="打开企业级智能体开发生命周期图原图">
          <img src="assets/cases/agent-evaluation-dlc-loop.png" width="1860" height="958" alt="企业级智能体开发生命周期图：定义好、构建、评估、质量门禁与发布、生产环境观测、挖掘失败案例形成生产反馈飞轮。" loading="lazy" decoding="async">
          <span class="case-figure-zoom" aria-hidden="true">↗</span>
        </a>
        <figcaption>企业级智能体开发生命周期：评估不是上线前的一次检查，而是从定义规范、质量门禁、生产观测到失败案例回流的持续飞轮。手机端可在图内左右滑动查看完整细节。</figcaption>
      </figure>
      <p>与传统 CI/CD 最关键的区别在于：生产不是终点，而是飞轮最有价值的输入。评估集也不是项目初期一次性定义的静态资产，而是随生产数据持续生长的动态系统。生产 Trace 可以变成评估数据，评估数据积累到一定规模后，还可能成为微调或蒸馏的训练数据。</p>
      <div class="case-reading-note"><strong>定义“好”是第一步，不是上线后的复盘</strong><p>很多团队的真实顺序是先把 Demo 做出来，上线后等用户反馈，再回头想怎么衡量好坏。这通常带来显著返工成本：上线时没有评估基线，就无法判断下一次改动是变好了还是变坏了。ADLC 强制把“定义好”放在最前面，本质上是要求团队开工前先画图纸，而不是楼盖完之后再补验收标准。</p></div>
    </section>

    <section class="case-section" data-section id="start-small">
      <p class="eyebrow">Start small</p>
      <h2>启动智能体项目，第一问不是“它能做什么”，而是“我们要解决什么问题”。</h2>
      <p>很多团队一开始就想覆盖所有场景，结果 Prompt 越写越复杂，Tool 选择越来越混乱，性能越来越难归因。更稳的方式是从问题出发，倒推 Agent 的职责边界：它应该处理什么，不应该处理什么。财务分析助手可以先只做查季度收入、计算增长率、生成摘要三件事，把这三件事做可靠，再扩展。</p>
      <div class="case-document-grid">
        <article><span>01</span><small>职责定义</small><h3>做什么，不做什么</h3><p>把智能体的职责边界写下来，与利益相关者分享，用它来拒绝功能蔓延。</p></article>
        <article><span>02</span><small>语气与个性</small><h3>如何与用户交互</h3><p>明确正式或对话风格、如何问候用户、遇到范围外问题如何处理。</p></article>
        <article><span>03</span><small>工具与知识源</small><h3>每个工具都要可理解</h3><p>工具、参数和知识源必须有明确定义，模糊描述会导致错误选择。</p></article>
        <article><span>04</span><small>基准数据集</small><h3>评估体系的燃料</h3><p>覆盖常见查询、边缘情况、应拒绝回答和应升级人工的问题。</p></article>
      </div>
      <div class="case-reading-note"><strong>基准数据集不是上线后再补的东西</strong><p>它是整个评估体系的燃料。没有它，评估系统无从运转，团队也无法回答“智能体有没有进步”。在 PoC 阶段用真实用户测试，团队会立即发现没有预料到的问题：日期解析出错、缩写理解不好、问题换一种表达方式就调用错误工具。在 PoC 阶段学到这些，代价是几周时间；在生产阶段学到，代价是信誉和用户信任。</p></div>
      <div class="case-agent-table" role="region" aria-label="三类智能体启动交付物对照表" tabindex="0">
        <table>
          <thead>
            <tr><th>智能体类型</th><th>智能体定义</th><th>语气与个性</th><th>工具定义</th><th>基准数据集</th></tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">财务分析智能体</th>
              <td>帮助分析师查询 EMEA、APAC、AMER 各区域季度营收数据，计算增长指标，生成高管摘要。不提供投资建议，不执行交易，不访问员工薪酬数据。</td>
              <td>专业但不失亲切，以名字称呼用户；主动承认数据局限；数据质量存疑时明确说明置信度；不用没有解释的金融行话。</td>
              <td><p><code>getQuarterlyRevenue(Region, quarter)</code>：返回指定区域和季度的营收数据，单位为百万美元。</p><p><code>calculateGrowth(currentValue, previousValue)</code>：返回百分比变化。</p><p><code>getMarketData(Region, dataType)</code>：获取最新行业指标数据。</p></td>
              <td>50 条，包括：“EMEA 第三季度的营收是多少？”“和上个季度相比增长了多少？”“亚太区表现怎么样？”“CEO 的奖金是多少？”（应拒绝回答）“对比 2024 年所有区域的表现”。</td>
            </tr>
            <tr>
              <th scope="row">HR 政策助手</th>
              <td>回答员工关于休假政策、请假申请、福利注册和公司政策的问题。不访问保密人事档案，不提供法律建议，不讨论个人薪酬或绩效评估。</td>
              <td>友好且支持性；使用员工偏好的称呼；保持专业同时平易近人；遇到复杂政策时逐步分解说明；对敏感事项主动提出转接 HR 专员。</td>
              <td><p><code>checkVacationBalance(employeeId)</code>：返回各类型可用天数。</p><p><code>getPolicy(policyName)</code>：从知识库获取政策文件。</p><p><code>createHRTicket(employeeId, category, description)</code>：升级复杂问题。</p><p><code>getUpcomingHolidays(year, region)</code>：返回公司假期日历。</p></td>
              <td>45 条，包括：“我还有几天假？”“育儿假政策是什么？”“我下周能请假吗？”“为什么我的奖金比预期低？”（应升级处理）“怎么参加健康保险？”。</td>
            </tr>
            <tr>
              <th scope="row">IT 支持智能体</th>
              <td>协助员工处理密码重置、软件访问申请、VPN 故障排查和常见技术问题。不访问生产系统，不直接修改安全权限，不处理基础设施变更。</td>
              <td>耐心清晰；避免技术行话；提供分步骤操作说明；移到下一步前确认理解；庆祝小进展；需要系统权限时升级给 IT 团队。</td>
              <td><p><code>resetPassword(userId, system)</code>：触发密码重置流程。</p><p><code>checkVPNStatus(userId)</code>：验证 VPN 配置与连通性。</p><p><code>requestSoftwareAccess(userId, software, justification)</code>：创建访问申请工单。</p><p><code>searchKnowledgeBase(query)</code>：检索排障文档。</p></td>
              <td>40 条，包括：“我登不上邮箱”“VPN 一直断线”“我需要访问 Salesforce”“能给我管理员权限吗？”（应拒绝）“笔记本连不上 Wi-Fi”“怎么安装 Slack？”。</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="case-section" data-section id="metrics">
      <p class="eyebrow">Evaluation metrics</p>
      <h2>自动化评估要同时追踪技术指标和业务指标。</h2>
      <p>有了基准数据集，下一步是建立自动化评估机制，让它成为开发流程的一部分，而不是上线前临时跑一遍的检查清单。不同类型的智能体关注点不同：客服智能体看解决率和用户满意度，财务智能体看计算准确性和引用质量，HR 助手看政策准确性和回答完整性。</p>
      <p>评估数据集至少要覆盖三类情况。第一，同一问题的多种表达：用户不会像 API 文档那样说话，“上季度欧洲收入”和“EMEA Q3 数字”应该触发相同工具调用。第二，应该拒绝或升级人工的查询：边界案例同样必须进入评估。第三，有歧义的查询：当一个问题有多个合理解读时，智能体应该追问、澄清，还是选择默认口径，也要被评估。</p>
      <div class="case-data-table" role="region" aria-label="评估数据集覆盖类型" tabindex="0">
        <table>
          <thead><tr><th>覆盖类型</th><th>样例</th><th>评估要回答的问题</th></tr></thead>
          <tbody>
            <tr><th scope="row">同义表达</th><td>“上季度欧洲收入”“EMEA Q3 数字”“欧洲今年整体表现怎么样”</td><td>是否稳定选择正确工具，是否把业务口语映射为标准参数。</td></tr>
            <tr><th scope="row">拒绝或升级</th><td>“CEO 奖金是多少？”“给我管理员权限”“为什么我的奖金比预期低？”</td><td>是否识别权限边界、敏感数据和人工升级路径。</td></tr>
            <tr><th scope="row">歧义查询</th><td>“亚太区表现怎么样？”“这个渠道上月是不是有问题？”</td><td>是否主动澄清指标口径、时间窗口和比较基线。</td></tr>
          </tbody>
        </table>
      </div>
      <div class="case-fit-grid">
        <article class="case-fit-card case-fit-card--yes"><small>技术指标</small><h3>判断系统是否稳定、可扩展、可控成本。</h3><ul><li>工具选择准确率，例如目标 ≥ 95%</li><li>参数提取准确率，例如目标 ≥ 98%</li><li>延迟 P50 / P95，例如 2 秒和 5 秒</li><li>每次查询 Token 用量和调用次数</li></ul></article>
        <article class="case-fit-card case-fit-card--yes"><small>业务指标</small><h3>判断回答是否真的有用、可信、符合边界。</h3><ul><li>拒绝准确率，敏感问题应 100% 拒绝</li><li>回答质量和解释清晰度</li><li>引用质量和计算准确性</li><li>用户满意度和任务完成率</li></ul></article>
      </div>
      <div class="case-comparison-table"><div><span>评估维度</span><span>财务分析智能体例子</span><span>为什么重要</span><strong>工具选择准确率</strong><p>面对“上季度收入”类问题，是否选择 <code>getQuarterlyRevenue</code> 而不是 <code>getMarketData</code>；目标 ≥ 95%</p><p>工具选错，后面的计算和回答都会建立在错误入口上。</p><strong>参数提取准确率</strong><p>是否正确将 “EMEA” 和 “Q3 2024” 映射到区域与季度参数；目标 ≥ 98%</p><p>自然语言里的时间、区域、指标口径经常是业务错误来源。</p><strong>拒绝准确率</strong><p>面对“CEO 奖金是多少”，是否正确拒绝；目标 100%</p><p>边界失败比普通回答错误更危险，尤其涉及权限和敏感数据。</p><strong>回答质量</strong><p>解释是否清晰、有没有歧义，可用 LLM-as-a-Judge 评估</p><p>业务用户需要的是可执行判断，不只是原始数据。</p><strong>延迟和成本</strong><p>P50 低于 2 秒、P95 低于 5 秒；平均每次查询低于 5,000 tokens</p><p>答案正确但成本过高或太慢，也无法生产化。</p></div></div>
      <p>评估必须嵌入开发流程：改了 Prompt，跑评估；加了新工具，跑评估；换了模型，跑评估。比如把模型从 Claude Sonnet 换成 Claude Haiku 后，工具选择准确率从 92% 降到 87%，但 P50 延迟从 3.2 秒降到 1.8 秒，团队就能基于数字判断速度提升是否值得那 5% 的准确率代价。</p>
    </section>

    <section class="case-section" data-section id="continuous">
      <p class="eyebrow">Continuous testing</p>
      <h2>上线不是测试结束，而是测试场景从预设样本变成真实世界。</h2>
      <p>开发阶段只能测试团队预想到的场景。进入生产后，真实用户会用完全没预料到的方式提问，会触发新的边界，也会在特定时间和上下文下暴露问题。同时，模型后台更新、外部 API 行为变化都会在不知情的情况下影响表现。这就是静默漂移，它不会报错，只会让质量指标悄悄变差。</p>
      <ol class="case-process">
        <li><span>01</span><div><h3>每次变更触发回归测试</h3><p>改 Prompt、加工具、换模型，都要跑完整评估套件，确认没有引入回归。</p></div></li>
        <li><span>02</span><div><h3>生产流量持续采样</h3><p>从真实用户交互中随机抽样，用离线评估相同指标体系打分，监控质量曲线。</p></div></li>
        <li><span>03</span><div><h3>漂移检测与自动告警</h3><p>如果工具选择准确率从 92% 悄悄降到 84%，系统必须捕捉并告警。</p></div></li>
        <li><span>04</span><div><h3>重大更新做 A/B 测试</h3><p>新版本先用部分流量验证，确认指标不差于旧版本，再逐步切换。</p></div></li>
      </ol>
      <div class="case-data-table case-data-table--wide" role="region" aria-label="持续测试机制表" tabindex="0">
        <table>
          <thead><tr><th>触发器</th><th>评估动作</th><th>核心信号</th><th>未通过时怎么处理</th></tr></thead>
          <tbody>
            <tr><th scope="row">Prompt / 工具 / 模型变更</th><td>跑完整回归评估集，并与上一个稳定版本比较。</td><td>工具选择准确率、参数提取、拒绝准确率、回答质量、延迟和成本。</td><td>阻断发布，回滚变更，定位是 Prompt、工具描述还是检索策略问题。</td></tr>
            <tr><th scope="row">生产流量采样</th><td>抽取真实交互，用同一指标体系离线打分。</td><td>真实用户问题覆盖率、边界案例、任务完成率和投诉样本。</td><td>把失败样本加入评估集，补充反例和澄清规则。</td></tr>
            <tr><th scope="row">质量曲线异常</th><td>触发漂移检测和告警，拉取相关 Trace。</td><td>两周内工具选择准确率从 92% 降到 84%，或外部 API 错误率异常上升。</td><td>先排查外部依赖和工具返回格式，再决定是否调 Prompt 或检索策略。</td></tr>
            <tr><th scope="row">重大版本更新</th><td>做 A/B 测试或灰度流量验证。</td><td>新旧版本的准确率、延迟、成本和业务满意度差异。</td><td>新版本不优于旧版本时暂停切换，保留旧版作为生产基线。</td></tr>
          </tbody>
        </table>
      </div>
      <p>改进循环的正确姿势是：评估、定位问题、修改 Prompt 或工具定义或 Retrieval 策略、重新评估。对绝大多数企业智能体来说，大部分性能提升来自 Prompt、工具和 Retrieval 层面的优化，而不是立刻换模型或微调。</p>
      <div class="case-reading-note"><strong>ForFlow 团队的工具优化示例</strong><p>财务智能体上线后，通过生产采样发现一类查询的工具选择准确率从 78% 起步：用户问“欧洲今年整体表现怎么样”，智能体频繁调用 <code>getMarketData</code>，而不是 <code>getQuarterlyRevenue</code>。根因不是模型不够聪明，而是工具描述不够精确，<code>getMarketData</code> 描述里有 “market performance” 字样，和用户表达高度重合。细化两个工具的适用场景并加入反例后，准确率回升到 95%。这组数字来自团队成员的过往项目，用于说明优化方法。</p></div>
      <p>第一个智能体上线只是里程碑。企业真正的价值，来自把这套能力在组织内规模化复制，而不是每次构建新智能体都从零开始。规模化有一个前提：单个智能体的质量基线必须先建立好。多个智能体协作时，问题可能来自任何一个环节，也可能来自交接过程本身；如果没有评估基线，出了问题几乎无从归因。</p>
      <p>扩展到组织级时，团队需要从项目思维转向平台思维。单个项目关心“这个智能体能不能用”；平台团队还要关心“整个组织的智能体能不能统一治理”。这意味着要维护经过安全审查的工具目录，建立统一的可观测性和评估标准，并运行跨智能体集中监控，让成本、质量和风险曲线可以被及时发现。</p>
      <p>生产数据是持续改进的原料。第一版上线时的 50 个基准样本，会随着真实用户交互不断扩充。生产中出现的新边界案例、新失败模式，都应该回流到评估集。规模化不是建更多智能体，而是建立一套让每个智能体都能持续变好的机制。</p>
      <div class="case-document-grid">
        <article><span>爬</span><small>爬行阶段</small><h3>内部小范围试点。</h3><p>核心目标是学习和迭代。失败成本低，错了可以快速改，重点建立第一套基准数据集、指标体系和 CI 门控。</p></article>
        <article><span>走</span><small>行走阶段</small><h3>受控外部用户验证。</h3><p>更多用户带来更多反馈和边界案例，此前在可观测性和评估上的投入开始产生回报。</p></article>
        <article><span>跑</span><small>奔跑阶段</small><h3>规模化上线。</h3><p>平台能力让其他团队更快构建自己的智能体，统一工具目录、可观测性和评估标准开始形成组织复利。</p></article>
      </div>
    </section>

    <section class="case-section" data-section id="observability">
      <p class="eyebrow">Observability</p>
      <h2>可观测性是评估的数据管道，必须从第一天就埋好。</h2>
      <p>可观测性经常被推迟：先把功能做出来，上线再说。但等到意识到需要它时，往往已经有一个行为不透明的智能体跑在生产上，团队完全不知道它在做什么。可以有最好的评估框架，但没有 Trace 数据，在线评估无从采样，生产失败案例也无从挖掘。</p>
      <div class="case-document-grid">
        <article><span>01</span><small>开发者层</small><h3>用于调试</h3><p>从第一次测试查询开始，就能看到模型调用、工具选择、参数、推理步骤和错误。</p></article>
        <article><span>02</span><small>平台层</small><h3>用于治理</h3><p>谁在用智能体、用了多少 Token、哪个团队成本增长、事故完整时序是什么。</p></article>
        <article><span>03</span><small>运营层</small><h3>用于 SLA</h3><p>延迟百分位、错误率、工具调用成功率、用户会话完成率和告警触发。</p></article>
        <article><span>04</span><small>标准协议</small><h3>OpenTelemetry</h3><p>把模型调用、工具调用和推理步骤结构化为 Trace，接入 CloudWatch、Datadog、Dynatrace、LangSmith 或 Langfuse 等观测基础设施。</p></article>
      </div>
      <div class="case-native-diagram" role="img" aria-label="从生产 Trace 到评估集回流的图解">
        <div class="case-native-diagram__nodes">
          <article><small>01</small><strong>用户请求</strong><span>真实业务问题、上下文、权限身份</span></article>
          <article><small>02</small><strong>Agent 运行</strong><span>Prompt、模型调用、工具选择和参数</span></article>
          <article><small>03</small><strong>Trace 采集</strong><span>延迟、错误、Token、工具返回和中间步骤</span></article>
          <article><small>04</small><strong>自动评估</strong><span>离线指标、LLM-as-a-Judge、规则校验</span></article>
          <article><small>05</small><strong>回流改进</strong><span>失败样本进入评估集，推动下一轮迭代</span></article>
        </div>
        <p>这条链路让生产不再只是上线终点，而是评估数据和训练数据的来源。</p>
      </div>
      <div class="case-data-table" role="region" aria-label="可观测性三层职责表" tabindex="0">
        <table>
          <thead><tr><th>层级</th><th>主要看什么</th><th>服务对象</th><th>产出</th></tr></thead>
          <tbody>
            <tr><th scope="row">开发者层</th><td>模型调用、工具参数、推理步骤、错误堆栈</td><td>开发与调试团队</td><td>快速复现问题，判断是模型、工具还是业务规则错误。</td></tr>
            <tr><th scope="row">平台层</th><td>Token 成本、调用量、团队归属、事故时序</td><td>平台团队与管理层</td><td>成本治理、容量规划、跨团队质量对比。</td></tr>
            <tr><th scope="row">运营层</th><td>P50 / P95 延迟、错误率、会话完成率、用户反馈</td><td>业务负责人和运维团队</td><td>SLA、告警、自动回滚和生产健康度。</td></tr>
          </tbody>
        </table>
      </div>
      <div class="case-reading-note"><strong>为什么顺序重要</strong><p>如果财务智能体上线三周后用户投诉“查询很慢、有时答错”，没有 Trace 时团队可能花四天排查是模型慢、数据库慢还是外部数据 API 变了。如果第一天就接入 Trace，就能直接看到那条查询耗时 12 秒，其中 10 秒来自外部 API，同时工具返回值解析错误率从 0 变成了 100%。</p></div>
    </section>

    <section class="case-section" data-section id="architecture">
      <p class="eyebrow">Evaluable architecture</p>
      <h2>系统架构要让每个错误能被归因，每个环节能被独立评估。</h2>
      <p>评估不是只跑在模型输出上，它要求整个系统架构本身可被评估。工具定义要清晰，确定性操作要交给代码，多智能体协作要解耦，协议和协作模式要分清。否则，出问题时团队无法判断是模型失败、工具描述歧义、业务规则错误，还是交接上下文丢失。</p>
      <div class="case-value-cards case-value-cards--triple">
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-layers"></use></svg></span><small>工具策略</small><h3>工具定义比工具数量更重要。</h3><p>完整工具定义应包含名称、参数、返回格式、错误条件和使用指引。模糊的“获取收入数据”会让 Agent 猜错工具；精确描述能显著降低误用。</p></article>
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-data"></use></svg></span><small>确定性代码</small><h3>Agent 负责编排，代码负责计算。</h3><p>日期获取、增长率计算、格式验证和业务规则判断都应交给确定性代码。这样更快、更便宜，也更容易测试。</p></article>
        <article><span><svg aria-hidden="true" class="ff-icon"><use href="#i-flow"></use></svg></span><small>多智能体解耦</small><h3>职责清晰，才能独立评估。</h3><p>顺序、层级、对等协作各有适用场景。交接点要监控上下文是否完整，协议如 A2A、MCP、HTTP 不等于协作模式。</p></article>
      </div>
      <div class="case-comparison-table"><div><span>工具定义要素</span><span>作用</span><span>示例</span><strong>清晰名称</strong><p>直接传达工具用途</p><p><code>getQuarterlyRevenue</code>，而不是 <code>getData</code></p><strong>明确参数</strong><p>消除输入歧义</p><p><code>region: EMEA|APAC|AMER</code>，<code>quarter: YYYY-QN</code></p><strong>返回格式</strong><p>明确输出结构和单位</p><p><code>{revenue: number, currency: "USD", period: string}</code></p><strong>错误条件</strong><p>记录失败场景</p><p>季度不存在返回 404，服务不可用返回 503</p><strong>使用指引</strong><p>说明何时用、何时不用</p><p>询问营收、销售或财务表现时使用；不适用于预测或趋势分析</p></div></div>
      <p>当工具数量增长到二三十个时，工具目录管理就变得关键。不同团队不应该重复造同一个数据库连接器，建议维护一个经过安全审查、在生产中验证过的工具目录，新团队从目录取用。同时推荐用 MCP Server 暴露工具：Slack、GitHub、Salesforce 等服务已有现成 Server 可以接入，不必每次从零封装。工具还需要健壮错误处理：瞬时故障自动重试，可能时回退到缓存数据，服务完全不可用时主动告知用户。这样评估时也能区分“智能体做错决策”和“工具本身故障”。</p>
      <div class="case-reading-note"><strong>工具定义要配代码示例</strong><p>每个工具都应该附调用示例和返回示例。开发者不应该靠猜来理解参数、输出结构或错误格式；完整示例能减少误用，也让评估失败时更容易判断是模型选错工具，还是工具描述本身有歧义。</p></div>
      <div class="case-comparison-table"><div><span>实现方式</span><span>把当前日期做成 Agent 工具</span><span>用代码获取日期后传入</span><strong>智能体行为</strong><p>制定计划 → 调用 <code>get_current_date()</code> → 计算下个月 → 调用 <code>create_report()</code></p><p>代码获取今天日期 → 传入智能体 → 推断下个月 → 调用 <code>create_report()</code></p><strong>延迟</strong><p>约 12 秒</p><p>约 9 秒</p><strong>LLM 调用次数</strong><p>4 次</p><p>3 次</p><strong>总 Token 用量</strong><p>约 8,500</p><p>约 6,200</p></div></div>
      <p>“获取当前日期”一行代码就能解决，用不着 LLM。如果把它设计成智能体工具，每次查询就多 1 次 LLM 调用、约 2,300 个 Token 和 3 秒延迟。乘以每天数千次查询，成本和延迟差距会非常可观。更重要的是，确定性操作的结果是二元对错，可以用程序直接验证，不需要 LLM-as-a-Judge。</p>
      <p>正确的架构是智能体负责编排，代码负责计算。用户问“我们 EMEA 这季度增长了多少”，智能体用推理能力理解意图、决定调哪些数据，然后调用确定性函数执行计算，最后再用自然语言解释结果。LLM 只在需要模糊理解和表达的地方介入。</p>
      <p>多智能体系统的拆分逻辑也类似组织分工：不会让一个人同时负责销售、工程、客服和财务，也不应该让一个 Agent 处理三十种任务。职责单一的智能体有更短的指令、更聚焦的工具集和更清晰的指标。最容易出问题的是交接点：上下文是否完整传递、哪个智能体处理了哪部分请求、延迟发生在哪个环节、用户已经提供的信息有没有被重复询问，都要进入 Trace 和评估。</p>
      <div class="case-fit-grid">
        <article class="case-fit-card case-fit-card--yes"><small>顺序模式</small><h3>任务有天然先后顺序。</h3><ul><li>第一个智能体取数据</li><li>第二个智能体分析</li><li>第三个智能体生成报告</li><li>适合稳定流程和明确交接</li></ul></article>
        <article class="case-fit-card case-fit-card--yes"><small>层级模式</small><h3>需要智能路由和分发。</h3><ul><li>Supervisor 判断用户意图</li><li>分发给专门智能体</li><li>适合多业务入口</li><li>要重点评估路由准确率</li></ul></article>
        <article class="case-fit-card case-fit-card--yes"><small>对等协作模式</small><h3>需要动态协同。</h3><ul><li>没有中央协调者</li><li>适合探索性任务</li><li>交接和上下文完整性更难评估</li><li>需要更强 Trace 和边界约束</li></ul></article>
        <article class="case-fit-card case-fit-card--yes"><small>协议 vs 模式</small><h3>通信协议不等于协作模式。</h3><ul><li>A2A、MCP、HTTP 是协议</li><li>顺序、层级、对等是模式</li><li>同一协议可支持不同模式</li><li>分清两者才能避免基础设施和业务逻辑耦合</li></ul></article>
      </div>
      <div class="case-data-table case-data-table--wide" role="region" aria-label="多智能体协作模式与评估重点表" tabindex="0">
        <table>
          <thead><tr><th>模式</th><th>适用场景</th><th>主要风险</th><th>评估重点</th></tr></thead>
          <tbody>
            <tr><th scope="row">顺序模式</th><td>任务有天然先后顺序：取数据、分析、生成报告。</td><td>上游结果错误会被下游放大，交接上下文可能丢失。</td><td>每一步的输入输出契约、失败重试、最终报告与原始数据的一致性。</td></tr>
            <tr><th scope="row">层级模式</th><td>一个 Supervisor 判断用户意图，分发给专门智能体。</td><td>路由错误会让后续代理全部跑偏，Supervisor 容易变成复杂 Prompt 黑箱。</td><td>意图分类准确率、路由置信度、人工升级边界和错误归因。</td></tr>
            <tr><th scope="row">对等协作</th><td>智能体之间动态协同，没有固定中央协调者。</td><td>协同路径更难预测，循环调用和责任不清风险更高。</td><td>Trace 完整性、协作终止条件、每个代理的责任边界和成本上限。</td></tr>
            <tr><th scope="row">协议与模式分离</th><td>A2A、MCP、HTTP 是通信协议；顺序、层级、对等是协作模式。</td><td>把协议当业务模式，会让基础设施选型绑死业务编排。</td><td>通信契约、工具发现、权限边界和业务编排是否可独立替换。</td></tr>
          </tbody>
        </table>
      </div>
      <p>一个实用原则是：如果确定性代码能可靠解决问题，就用代码；如果需要推理或自然语言理解，才用智能体。最常见的错误是默认一切都应该 Agentic，结果成本高、延迟长、评估也更困难。</p>
    </section>

    <section class="case-section" data-section id="security">
      <p class="eyebrow">Security & personalization</p>
      <h2>安全控制不能写在 Prompt 里，必须外部化到 Gateway 和 Policy 层。</h2>
      <p>从单用户原型扩展到数千用户的生产系统时，需要同时解决安全边界和个性化体验。前者确保用户只能访问自己有权限的数据；后者让智能体记住用户偏好和历史，提供更连贯响应。两者共用同一套基础设施：用户身份和权限隔离。</p>
      <div class="case-fit-grid">
        <article class="case-fit-card case-fit-card--no"><small>错误方式</small><h3>把规则写进 System Prompt。</h3><ul><li>依赖 LLM 自己判断是否遵守安全规则</li><li>Prompt 注入可能绕过限制</li><li>内部决策不可观测、不可审计</li><li>安全问题难以复现和系统测试</li></ul></article>
        <article class="case-fit-card case-fit-card--yes"><small>正确方式</small><h3>把控制放到 Gateway 和 Policy 层。</h3><ul><li>认证层携带用户身份和权限 token</li><li>授权层在工具调用前拦截请求</li><li>会话隔离防止上下文跨用户泄露</li><li>个性化记忆按用户命名空间存储</li></ul></article>
      </div>
      <div class="case-document-grid">
        <article><span>01</span><small>认证层</small><h3>身份先进入会话。</h3><p>用户通过企业现有身份平台完成验证，拿到携带权限信息的 token。这个 token 在整个会话中传递。</p></article>
        <article><span>02</span><small>授权层</small><h3>工具调用前先拦截。</h3><p>Gateway 验证当前用户是否有权限以当前参数调用这个工具，也可以注入第三方 OAuth 凭证、执行限流和审计。</p></article>
        <article><span>03</span><small>会话隔离</small><h3>上下文不能串用户。</h3><p>多用户并发时，每个用户会话必须完全独立。用户 A 的上下文和个性化记忆，不能泄露给用户 B。</p></article>
        <article><span>04</span><small>用户记忆</small><h3>个性化也要受控。</h3><p>报告格式偏好、常用筛选条件和历史交互可以按用户命名空间存储，但检索同样必须经过授权层管控。</p></article>
      </div>
      <div class="case-native-diagram" role="img" aria-label="安全控制外部化到 Gateway 和 Policy 层的图解">
        <div class="case-native-diagram__nodes case-native-diagram__nodes--security">
          <article><small>身份</small><strong>Identity Provider</strong><span>用户身份、角色、权限 token</span></article>
          <article><small>拦截</small><strong>Gateway</strong><span>工具调用前检查权限和参数</span></article>
          <article><small>策略</small><strong>Policy Layer</strong><span>行级 / 列级访问、限流、审计和 OAuth 凭据</span></article>
          <article><small>执行</small><strong>Tool / Database</strong><span>只有通过授权的请求才进入系统</span></article>
          <article><small>留痕</small><strong>Trace / Audit</strong><span>记录谁在何时调用了什么</span></article>
        </div>
        <p>安全规则不交给模型“自觉遵守”，而是在工具调用之前由可审计的网关和策略层确定性执行。</p>
      </div>
      <div class="case-data-table" role="region" aria-label="安全控制方式对照表" tabindex="0">
        <table>
          <thead><tr><th>控制方式</th><th>优点</th><th>风险</th><th>适用判断</th></tr></thead>
          <tbody>
            <tr><th scope="row">System Prompt 约束</th><td>实现快，适合原型阶段说明行为边界。</td><td>不可保证、不可审计、难复现，可能被 Prompt 注入绕过。</td><td>只能作为行为提示，不能作为生产权限控制。</td></tr>
            <tr><th scope="row">Gateway / Policy 外部化</th><td>工具调用前确定性鉴权，能审计、能测试、能和企业 IAM 集成。</td><td>需要提前设计工具权限、参数规则和日志结构。</td><td>生产环境访问企业数据、财务、人事、客户或权限系统时必须采用。</td></tr>
          </tbody>
        </table>
      </div>
      <p>如果初级分析师试图查询高管薪酬数据，靠 System Prompt 多数情况下会拒绝，但无法保证每次都正确。把访问控制放在 Gateway 层，请求在到达数据库前就被策略拦截，结果是确定的，与模型当次推理无关。</p>
    </section>

    <section class="case-section" data-section id="conclusion">
      <p class="eyebrow">Conclusion</p>
      <h2>评估同时是规格说明、质量门控、生产监控和改进驱动力。</h2>
      <p>企业智能体和传统软件有本质不同，传统 QA 框架在这里失效。ADLC 提供了一套新的方法论，把生产数据变成飞轮的驱动力；而三类工程实践，无论是把评估跑起来、让数据持续流入评估，还是让系统架构可被评估，最终都指向同一件事。</p>
      <div class="case-document-grid">
        <article><span>01</span><small>规格说明</small><h3>定义什么叫好</h3><p>基准数据集和指标体系是开发工作的起点，不是上线后的复盘。</p></article>
        <article><span>02</span><small>质量门控</small><h3>不达阈值不上线</h3><p>每次变更触发评估，阻止回归悄悄进入生产。</p></article>
        <article><span>03</span><small>生产监控</small><h3>捕捉静默漂移</h3><p>持续采样和漂移检测，让质量衰退在影响用户前被发现。</p></article>
        <article><span>04</span><small>改进驱动力</small><h3>失败案例回流</h3><p>生产失败样本进入评估集，为下一轮优化提供有据可查的方向。</p></article>
      </div>
      <p>越早建立这套能力，它的复利效应越显著：每一次迭代都会让评估集更完整、指标体系更精准、整个飞轮转得更快。下一篇可以继续细化智能体评估到底有哪些维度、方法和从零构建路径；配套动手实验则可以把这里的基准数据集、工具定义和 Trace 回流做成可运行样例。</p>
      <div class="case-reference-list"><a href="https://aws.amazon.com/cn/blogs/china/part-1-enterprise-intelligent-why-evaluation/" target="_blank" rel="noopener noreferrer">团队过往方法的公开资料</a><a href="https://opentelemetry.io/docs/" target="_blank" rel="noopener noreferrer">OpenTelemetry 可观测性资料</a></div>
    </section>
  </article>
</div>
<section class="case-related">
  <div class="container">
    <div class="case-related-head"><div><p class="eyebrow">Related cases</p><h2>继续看相邻问题，建立完整判断。</h2></div><a class="text-link" href="cases.html">查看全部案例&博客 →</a></div>
    <div class="case-related-grid">
      <a class="case-related-card" href="case-supply-chain-agentic-decision.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/supply-chain-agentic-decision-hero.png"><div><small>多智能体生产架构</small><h3>供应链数据如何进入决策与行动</h3><p>语义层、主管代理、MCP 和行动闭环</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-vanguard-virtual-analyst.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/vanguard-virtual-analyst-hero.png"><div><small>AI-ready data</small><h3>先锋集团虚拟分析师</h3><p>数据产品、语义层、质量检查和持续评估</p><span>继续阅读 <b>↗</b></span></div></a>
      <a class="case-related-card" href="case-healthcare-agent-roi.html"><img alt="" decoding="async" loading="lazy" src="assets/cases/healthcare-care-chain-sana-plain.png"><div><small>高合规智能体</small><h3>医疗工作流中的受限多智能体架构</h3><p>状态机、人工升级、模型专项化和 ROI 验证</p><span>继续阅读 <b>↗</b></span></div></a>
    </div>
  </div>
</section>
<section class="case-next-cta"><div class="container case-next-cta__inner"><div><small>把方法映射到你的企业</small><h2>先选一个 Agent 原型，补齐评估基线，再讨论扩展。</h2><p>把职责边界、工具定义、基准数据集、上线阈值和 Trace 采样机制摆清楚，再决定是否进入生产验证。</p></div><div><a class="btn btn--light" href="navigator.html">开始 AI 场景诊断 →</a><a class="btn btn--ghost" href="cases.html">返回案例&博客</a></div></div></section>
<section class="case-source-foot" id="case-source" aria-labelledby="agent-eval-case-source-title"><div class="container"><div class="case-source-card"><span class="case-source-card__icon"><svg aria-hidden="true" class="ff-icon"><use href="#i-chart"></use></svg></span><div><small>ForFlow 团队经验与公开依据</small><h2 id="agent-eval-case-source-title">这套评估方法来自团队做过的生产项目。</h2><p>公开资料用于说明可披露的方法和示例。企业落地时，评估集、阈值和上线门槛仍要按自己的业务风险重新定义。</p><a href="https://aws.amazon.com/cn/blogs/china/part-1-enterprise-intelligent-why-evaluation/" target="_blank" rel="noopener noreferrer">查看团队过往方法的公开资料 <span aria-hidden="true">↗</span></a></div></div></div></section>
'''
(ROOT/'case-agent-evaluation-first.html').write_text(page('企业 Agent 上线前，先建立评估基线','ForFlow Agent 评估方法：用 Evaluation-first、ADLC、自动化评估、可观测性、工具策略与安全边界把原型推向生产。','case-agent-evaluation-first',agent_evaluation_first_body,'case-detail-page case-theme--agent case-study-v2'),encoding='utf-8')

energy_optimization_body = (ROOT / 'templates/case-energy-optimization-agent-body.html').read_text(encoding='utf-8')
(ROOT/'case-energy-optimization-agent.html').write_text(page('实时电价驱动的工厂能效优化 Agent','工业能效合作场景材料整理：保留工业协议、预测模型、多目标调度、PLC / DCS 执行、安全边界与分阶段上线方法。','case-energy-optimization-agent',energy_optimization_body,'case-detail-page case-study-v2 case-theme--energy'),encoding='utf-8')

contact_body = '''
<section class="contact-hero">
  <div class="container contact-hero__inner">
    <nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>联系</strong></nav>
    <div class="contact-hero__grid">
      <div class="contact-hero__copy">
        <h1 data-contact-title>告诉我们，<br>哪段业务卡住了。</h1>
        <p data-contact-lead>写清公司、业务问题和现有系统即可，不用先准备完整需求书。</p>
      </div>
      <aside class="contact-card" aria-label="联系 ForFlow">
        <span data-contact-service>ForFlow 萬維流形</span>
        <h2 data-contact-heading>发一段简短说明</h2>
        <p data-contact-note>建议带上公司与联系人、最想解决的问题、已有数据或系统，以及希望沟通的时间。</p>
        <form class="lead-form" data-lead-form data-source-type="contact" data-requires-data-api>
          <input type="hidden" name="service_interest" data-contact-service-input value="企业 AI 项目咨询">
          <label class="form-honeypot" aria-hidden="true">公司网址<input type="text" name="website" tabindex="-1" autocomplete="off"></label>
          <div class="lead-form__row"><label><span>姓名</span><input type="text" name="name" autocomplete="name" maxlength="100" placeholder="怎么称呼你"></label><label><span>工作邮箱 *</span><input type="email" name="email" autocomplete="email" placeholder="name@company.com" required></label></div>
          <label><span>公司或团队</span><input type="text" name="company" autocomplete="organization" maxlength="160" placeholder="选填"></label>
          <label><span>最想解决的问题</span><textarea name="problem" maxlength="2000" rows="4" placeholder="例如：客服知识分散，回复慢且口径不一致"></textarea></label>
          <label><span>方便沟通的时间</span><input type="text" name="preferred_time" maxlength="160" placeholder="例如：工作日下午"></label>
          <label class="lead-consent"><input type="checkbox" name="consent" required><span>我同意 ForFlow 按<a href="privacy.html">《隐私说明》</a>保存信息并与我联系。</span></label>
          <button class="btn btn--green" type="submit">提交项目说明 <span aria-hidden="true">→</span></button>
          <p class="lead-status" data-lead-status role="status" aria-live="polite"></p>
        </form>
        <a class="btn btn--ghost contact-mail-fallback" data-contact-email href="mailto:hello@forflow.ai?subject=ForFlow%20%E8%81%94%E7%B3%BB">暂用邮件联系 <span aria-hidden="true">→</span></a>
        <p class="contact-fallback">也可以直接邮件至 <a class="contact-email" data-contact-email href="mailto:hello@forflow.ai?subject=ForFlow%20%E8%81%94%E7%B3%BB">hello@forflow.ai</a></p>
      </aside>
    </div>
  </div>
</section>
<section class="contact-cities">
  <div class="container contact-cities__inner">
    <div class="contact-cities__head">
      <p class="eyebrow">City presence</p>
      <h2>北京、上海、深圳<br>均可安排沟通。</h2>
      <p>需要线下见面，请在邮件里写明城市和时间。</p>
    </div>
    <div class="contact-city-grid" aria-label="城市沟通入口">
      <article class="contact-city-card contact-city-card--beijing">
        <figure class="contact-city-media">
          <img src="assets/contact/contact-city-card-beijing.png" alt="北京商务沟通场景视觉" decoding="async" loading="eager">
          <span>北京</span>
        </figure>
        <div class="contact-city-copy">
          <small>Beijing</small>
          <h3>北京</h3>
          <p>如需在北京沟通，请在邮件中备注城市、时间和联系人。</p>
        </div>
      </article>
      <article class="contact-city-card contact-city-card--shanghai">
        <figure class="contact-city-media">
          <img src="assets/contact/contact-city-card-shanghai.png" alt="上海业务运营场景视觉" decoding="async" loading="eager">
          <span>上海</span>
        </figure>
        <div class="contact-city-copy">
          <small>Shanghai</small>
          <h3>上海</h3>
          <p>如需在上海沟通，请在邮件中备注城市、时间和联系人。</p>
        </div>
      </article>
      <article class="contact-city-card contact-city-card--shenzhen">
        <figure class="contact-city-media">
          <img src="assets/contact/contact-city-card-shenzhen.png" alt="深圳制造工程场景视觉" decoding="async" loading="eager">
          <span>深圳</span>
        </figure>
        <div class="contact-city-copy">
          <small>Shenzhen</small>
          <h3>深圳</h3>
          <p>如需在深圳沟通，请在邮件中备注城市、时间和联系人。</p>
        </div>
      </article>
    </div>
  </div>
</section>
'''
(ROOT/'contact.html').write_text(page('联系','联系 ForFlow 萬維流形：hello@forflow.ai。','contact',contact_body,'contact-page'),encoding='utf-8')

privacy_body = '''
<section class="privacy-hero"><div class="container privacy-hero__inner"><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>隐私说明</strong></nav><p class="eyebrow">Privacy notice</p><h1>我们收集什么，<br>就说清什么。</h1><p>本说明适用于 forflow.ai 官网、AI 场景诊断、报告发送和咨询表单。版本：2026-07-11-v1。</p></div></section>
<section class="privacy-content section-pad"><div class="container privacy-layout"><aside><strong>快速说明</strong><p>匿名事件不含姓名和邮箱；诊断答案与联系信息分表保存；只有你主动提交后，我们才会保存邮箱。</p><a href="mailto:hello@forflow.ai">hello@forflow.ai</a></aside><article>
  <section><h2>1. 我们收集的信息</h2><p><strong>页面与产品事件：</strong>页面路径、会话编号、事件名称以及有限的页面或操作属性，用于理解页面访问、诊断完成和咨询转化。事件名称只允许本站公布的固定清单。</p><p><strong>诊断信息：</strong>你在 AI 场景诊断中选择的业务挑战、目标、限制条件和部署偏好。诊断表和答案表不保存姓名或邮箱。</p><p><strong>联系信息：</strong>只有在你提交咨询或要求发送诊断结果时，我们才会保存邮箱，以及你自愿填写的姓名、公司、问题和方便沟通的时间。</p></section>
  <section><h2>2. 我们如何使用</h2><p>这些信息用于生成诊断建议、发送你要求的报告、回复咨询、改进页面和诊断流程，以及维护服务安全。我们不会把联系信息复制到匿名事件表或诊断答案表。</p></section>
  <section><h2>3. 服务提供方</h2><p>网站由 Netlify 托管并运行服务端函数；结构化数据计划保存在 Supabase；邮件通知启用后由 Resend 发送；Cloudflare Web Analytics 启用后用于汇总页面访问与性能。我们只向完成上述目的所需的服务提供方传输必要信息。</p></section>
  <section><h2>4. 保存期限与安全</h2><p>正式上线时，默认目标是：匿名产品事件不超过 13 个月；未留资的诊断记录不超过 90 天；联系信息在最后一次有效沟通后不超过 12 个月，法律或争议处理另有要求的除外。正式环境会通过服务端校验、限流、字段白名单、行级安全和私有访问密钥降低风险。</p></section>
  <section><h2>5. 你的选择</h2><p>你可以不填写联系信息，直接查看浏览器中的诊断结果。需要查询、更正或删除你提交的信息，请用提交时的邮箱联系 <a href="mailto:hello@forflow.ai">hello@forflow.ai</a>。我们会先核验请求人与信息的关联。</p></section>
  <section><h2>6. 更新</h2><p>如收集范围、用途或服务提供方发生实质变化，我们会更新本页版本和日期；需要重新征得同意时，会在提交前再次说明。</p></section>
</article></div></section>
'''
(ROOT/'privacy.html').write_text(page('隐私说明','ForFlow 官网、AI 场景诊断与咨询表单的隐私说明。','',privacy_body,'privacy-page'),encoding='utf-8')

write_search_index()

search_body=f'''
<section class="search-page-hero"><div class="container"><nav class="breadcrumbs"><a href="index.html">首页</a><span>/</span><strong>搜索</strong></nav><h1>搜索 ForFlow</h1><p class="search-page-intro">按业务问题、行业或服务查找案例、方法和下一步入口。</p><form class="search-page-form" action="search.html" method="get"><span>{SEARCH_ICON}</span><input data-search-page-input type="search" name="search" value="" placeholder="例如：客服重复问答 / 合同审阅 / 工厂能效" aria-label="搜索关键词"><button class="btn btn--green" type="submit">搜索</button></form><p class="search-live-summary" data-search-summary aria-live="polite">输入关键词后会按相关度排序。</p><div class="search-quick-links" aria-label="常用搜索"><span>试试：</span><a href="search.html?search=客服">客服重复问答</a><a href="search.html?search=合同">合同审阅</a><a href="search.html?search=报表">经营报表</a><a href="search.html?search=员工服务">员工服务</a><a href="search.html?search=能效">工厂能效</a><a href="search.html?search=供应链">供应链</a><a href="search.html?search=数据治理">数据治理</a></div><div class="search-tabs"><button class="is-active" data-search-tab="all">全部 <span data-count-all>0</span></button><button data-search-tab="category">方案分类 <span data-count-category>0</span></button><button data-search-tab="service">企业服务 <span data-count-service>0</span></button><button data-search-tab="resource">资料 <span data-count-resource>0</span></button><button data-search-tab="case">案例&博客 <span data-count-case>0</span></button></div></div></section>
<section class="search-results-page section-pad" data-search-index="search-index.json?v={ASSET_VERSION}"><div class="container"><div class="search-result-group" data-result-type="category"><div class="search-result-head"><h2>方案分类 <span>{search_type_count('category')}</span></h2><a href="category-hrms.html">查看全部 →</a></div><div class="search-result-grid" data-search-grid="category">{render_search_cards('category')}</div></div>
<div class="search-result-group" data-result-type="service"><div class="search-result-head"><h2>企业服务 <span>{search_type_count('service')}</span></h2><a href="index.html#services">查看全部 →</a></div><div class="search-result-grid" data-search-grid="service">{render_search_cards('service')}</div></div>
<div class="search-result-group" data-result-type="resource"><div class="search-result-head"><h2>资料 <span>{search_type_count('resource')}</span></h2><span>PDF / 在线手册</span></div><div class="search-result-grid" data-search-grid="resource">{render_search_cards('resource')}</div></div>
<div class="search-result-group" data-result-type="case"><div class="search-result-head"><h2>案例&博客 <span>{search_case_count()}</span></h2><a href="cases.html">查看全部 →</a></div><div class="search-result-grid" data-search-grid="case">{render_search_case_cards()}</div></div>
<div class="search-empty" data-search-empty hidden><h2>没有找到完全匹配的内容。</h2><p>可以尝试“Agent”“数据治理”“培训”“HR”或“Playbook”。</p><a class="btn btn--green" href="navigator.html">改用场景诊断 →</a></div></div></section>
'''
(ROOT/'search.html').write_text(page('搜索','搜索 ForFlow 企业服务、场景、资料、案例与博客。','',search_body,'search-page'),encoding='utf-8')

viewer_body='''
<section class="viewer-toolbar"><div class="container viewer-toolbar-inner"><div><a class="viewer-back" href="search.html">← 返回搜索</a><h1 data-doc-title>企业生成式 AI 实战手册</h1></div><div class="viewer-actions"><a class="btn btn--ghost" data-doc-open href="assets/genai-playbook-reference.pdf" target="_blank" rel="noopener"><span>新窗口打开</span> ↗</a><a class="btn btn--green" data-doc-download href="assets/genai-playbook-reference.pdf" download><span>下载 PDF</span> ↓</a></div></div></section>
<section class="viewer-main"><div class="container viewer-shell"><aside class="viewer-meta"><img src="assets/forflow-lockup.png" alt="ForFlow 萬維流形"><div><small>文档类型</small><strong>PDF 参考资料</strong></div><div><small>阅读说明</small><p>桌面端使用浏览器内置阅读器。手机浏览器若无法内嵌，可使用“新窗口打开”或“下载 PDF”。</p></div></aside><div class="pdf-frame"><iframe data-doc-frame title="PDF 阅读器" src="assets/genai-playbook-reference.pdf#view=FitH"></iframe><div class="pdf-fallback"><p>当前浏览器无法内嵌 PDF？</p><a class="btn btn--green" data-doc-open href="assets/genai-playbook-reference.pdf" target="_blank" rel="noopener">打开文档 →</a></div></div></div></section>
'''
(ROOT/'document-viewer.html').write_text(page('PDF 阅读器','在线查看和下载企业 AI 参考 PDF。','document-viewer',viewer_body,'viewer-page'),encoding='utf-8')

# README
readme='''# ForFlow 萬維流形企业网站原型\n\n这是在已有 `index.html` 与 `navigator.html` 基础上继续扩展的静态响应式网站，不依赖前端框架。\n\n## 页面\n\n- `index.html`：主页（保留原有框架并加入五项企业服务）\n- `navigator.html`：3 分钟 AI 场景诊断\n- `navigator-results.html`：推荐结果、品牌视频控件与方案排序\n- `playbook.html`：中文企业生成式 AI 实战手册\n- `service-ai-enablement.html`：AI 采用与团队赋能\n- `service-data-governance.html`：AI 数据与知识治理\n- `service-agent-build.html`：企业 Agent 与工作流\n- `service-ai-training.html`：AI 实战培训\n- `category-hrms.html`：HR AI 场景分类页\n- `cases.html`：案例&博客\n- `case-wren-kitchens.html`：Wren Kitchens 公开案例结构参考\n- `case-manufacturing-pid-intelligence.html`：制造业 P&ID 智能化案例\n- `case-healthcare-agent-roi.html`：医疗智能体 ROI 案例\n- `case-automotive-dfmea-ontology-agent.html`：汽车 DFMEA 本体智能体案例\n- `case-supply-chain-agentic-decision.html`：供应链多智能体决策案例\n- `case-financial-bda-document-automation.html`：金融文档 BDA 自动化案例\n- `search.html`：全站搜索结果页\n- `document-viewer.html`：PDF 在线阅读器\n\n## 运行\n\n```bash\npython -m http.server 8080\n```\n\n打开 `http://localhost:8080/`。\n\n## 说明\n\n- 使用用户提供的 ForFlow + 萬維流形完整标识，不使用黑色方形图标。\n- Navigator 结果页的动效视频由完整品牌标识制作，带原生视频控件。\n- 所有服务页包含服务流程、交付物、FAQ 与相关路径。\n- 搜索弹层、搜索结果、PDF 展示、筛选、排序、FAQ、移动菜单和目录均为前端可交互原型。\n- 案例中的公开企业资料仅作为结构参考，正式发布前需复核授权和最新数据。\n'''
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
for _filename, _active in (
    ('case-manufacturing-pid-intelligence.html', 'case-manufacturing-pid-intelligence'),
    ('case-healthcare-agent-roi.html', 'case-healthcare-agent-roi'),
):
    if (ROOT / _filename).exists():
        patch_existing(_filename, _active)
version_asset_links()

# Refresh the isolated homepage base after normal full-site generation.
sync_homepage_theme(ROOT)
