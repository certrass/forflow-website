# 官网案例检索入口

来源：`build_site.py` 中的 `CASE_LIBRARY_ITEMS`。
更新：运行 `python3 output/homepage-v6/scripts/sync-case-catalog.py`，同时生成预览索引与本文件。

新增或调整案例时先查此清单，再读对应原页与来源。首页三场景不等于完整案例库。
团队过往实践、工程方法、合作场景、外部公开参考与概念场景各有自己的适用范围；索引不证明客户交付或效果。

| 案例 | 来源类型 | 原页 / 原始来源 | 检索词 |
| --- | --- | --- | --- |
| Wren Kitchens：从紧急团队扩容，到长期技术合作 | 制造与零售 · 公开技术合作参考 | [case-wren-kitchens.html](../../case-wren-kitchens.html) | Wren 厨房 零售 制造 物流 技术合作 跨模块 软件交付 知识交接 长期合作 |
| 把单篇内容制作从 18 小时缩短到 30 分钟 | IMDA 公开案例摘要 | [https://file.go.gov.sg/genai-playbook-pdf.pdf](https://file.go.gov.sg/genai-playbook-pdf.pdf) |  |
| 智能客服把每周常规询问工时从 18 小时降到 8 小时 | IMDA 公开案例摘要 | [https://www.imda.gov.sg/-/media/imda/files/news-and-events/media-room/media-releases/2024/10/singapore-digital-economy-remains-robust/annex-3-how-crestar-fan-supercharged-sales-and-efficiency-with-genai-powered-chatbot-solutions.pdf](https://www.imda.gov.sg/-/media/imda/files/news-and-events/media-room/media-releases/2024/10/singapore-digital-economy-remains-robust/annex-3-how-crestar-fan-supercharged-sales-and-efficiency-with-genai-powered-chatbot-solutions.pdf) |  |
| 让教师把时间从行政工作还给学生 | IMDA 公开材料 · 预期目标 | [https://file.go.gov.sg/genai-playbook-pdf.pdf](https://file.go.gov.sg/genai-playbook-pdf.pdf) |  |
| 用自然语言查询多源供应链数据 | IMDA 公开材料 · 预期目标 | [https://file.go.gov.sg/genai-playbook-pdf.pdf](https://file.go.gov.sg/genai-playbook-pdf.pdf) | 物流 数据 Agent 自然语言 报表 iHub 供应链 多源数据 |
| P&ID 智能化扩展工厂运营 | ForFlow 团队实践 · 工业知识 | [case-manufacturing-pid-intelligence.html](../../case-manufacturing-pid-intelligence.html) | 制造业 P&ID 工厂运营 工业知识资产化 工程师复核 图纸 查询 关联 |
| 实时电价驱动的工厂能效优化 Agent | 工业能效 · 合作场景材料 | [case-energy-optimization-agent.html](../../case-energy-optimization-agent.html) | 工业能效 工厂 能源管理 能效优化 Agent 智能体 实时电价 电力现货 需求响应 源网荷储 EMS MES WMS APS OT IT Modbus OPC UA PROFINET PLC DCS LSTM Transformer SAC DQN PPO 负荷预测 光伏预测 电价预测 储能 SOC 冷冻站 空压站 COP 多目标优化 人工接管 安全约束 |
| 医疗智能体的受限架构与验证方法 | ForFlow 团队实践 · 医疗 AI | [case-healthcare-agent-roi.html](../../case-healthcare-agent-roi.html) | 医疗 医院 诊所 受限多智能体 ROI 患者语音 EHR EMR 保险验证 预约管理 SFT GRPO 临床记录 医疗编码 CPT ICD 就诊前 就诊中 就诊后 状态机 人工升级 |
| 本体智能体如何重塑安全关键零部件 DFMEA | ForFlow 工程方法 · 汽车知识 | [case-automotive-dfmea-ontology-agent.html](../../case-automotive-dfmea-ontology-agent.html) | 汽车 汽车工程 B柱 B 柱 B-pillar 安全关键零部件 侧面碰撞 车顶抗压 安全带锚固 DFMEA FMEA 本体 Ontology 知识图谱 智能体 Agent AI RFLP 22MnB5 硼钢 热冲压 氢脆 疲劳 腐蚀 电偶腐蚀 粘接失效 失效模式 RPN AP ECO 工程变更 工程推理 知识流失 老师傅经验 组织记忆 经验断档 机构记忆 跨项目迁移 供应商教训 设计变更复评 FMVSS 214 FMVSS 216 Euro NCAP IIHS AIAG VDA |
| 多智能体 AI 如何将供应链数据转化为决策与行动 | ForFlow 团队实践 · 供应链 | [case-supply-chain-agentic-decision.html](../../case-supply-chain-agentic-decision.html) | 供应链 零售 鞋服 库存 SKU 控制塔 control tower 多智能体 Agent 语义层 自然语言 SQL 履行率 渠道履行 订单 冻结 信用控制 工具网关 可观测性 决策 行动 |
| 把金融文档提取接入可复核工作流 | ForFlow 工程方法 · 文档自动化 | [case-financial-bda-document-automation.html](../../case-financial-bda-document-automation.html) | 金融 文档 金融文档 字段蓝图 OCR IDP 智能文档处理 银行对账单 bank statement W-2 W2 1099-B 1099B 税务表格 供应商合同 vendor contract 结构化提取 JSON CSV 置信度 视觉定位 visual grounding 幻觉缓解 字段验证 会计 对账 税务 合同管理 |
| 先锋集团虚拟分析师：AI 就绪数据的八项原则 | ForFlow 团队实践 · 金融数据 | [case-vanguard-virtual-analyst.html](../../case-vanguard-virtual-analyst.html) | 先锋集团 Vanguard 虚拟分析师 AI-ready data AI 就绪数据 金融分析师 SQL 自助分析 数据架构 数据产品 运营模式 元数据目录 语义层 业务元数据 技术元数据 示例库 回归测试 数据质量 变更控制 持续评估 知识图谱 RAG 合规 安全 |
| 企业 Agent 上线前，先建立评估基线 | ForFlow 工程方法 · Agent 评估 | [case-agent-evaluation-first.html](../../case-agent-evaluation-first.html) | 企业智能体 Agent AI Agent Evaluation 评估 评测 ADLC Agent Development Lifecycle 原型 生产可信赖 单元测试 非确定性 Prompt 变更 静默漂移 CI CD LLM-as-a-Judge 基准数据集 工具选择 参数提取 拒绝准确率 延迟 Token 可观测性 Trace OpenTelemetry 漂移检测 A/B测试 多智能体 解耦 Supervisor MCP A2A Gateway Policy 安全 个性化 |
| Pension Lab：把单份文档处理从 15 分钟缩短到 40 秒 | TSH 公开客户案例摘要 | [https://tsh.io/portfolio/pension-lab-ai-case-study](https://tsh.io/portfolio/pension-lab-ai-case-study) |  |
| 员工制度与入职知识助手 | HR 服务 · 场景示例 | 仅概念场景 |  |

重点回查：汽车 B 柱 / B-pillar / DFMEA / ECO 对应 `case-automotive-dfmea-ontology-agent.html`。

预约入口配置：`output/homepage-v6/src/contact-config.js`。历史来源：Git 提交 `65c839f`。
已确认预约方式：填写需求表，团队联系确认交流时间。
飞书表单：万维流形 AI 转型会后对接；2026-09-12 公开表单元数据和访问权限回读可用，未提交测试线索。

当前预览与实际验证：`output/homepage-v6/remote-preview.json`；维护记录：`docs/maintenance/update-log.md`。

清单条目：15；清单源 SHA-256：`61df76ba2d44adab4b1cdb6b881fc80de68e1a28bfc42ff73e8e23317867ee00`。
