export const previewGates = [
  { label: "Local", status: "next build" },
  { label: "Preview", status: "Vercel URL" },
  { label: "China", status: "manual check" },
];

export const routeCards = [
  {
    code: "01",
    title: "首页试点",
    href: "/",
    description: "保留 ForFlow 视觉基调，验证 App Router、图片资产和首屏响应式。",
  },
  {
    code: "02",
    title: "案例中心骨架",
    href: "/cases",
    description: "把静态 CASE_LIBRARY_ITEMS 的维护思路迁成 TypeScript 数据源。",
  },
  {
    code: "03",
    title: "Navigator 雏形",
    href: "/navigator",
    description: "用客户端组件验证表单状态、结果切换和移动端交互。",
  },
];

export const caseItems = [
  {
    slug: "healthcare-agent-roi",
    domain: "医疗受限多智能体",
    title: "复杂医疗工作流中的智能体落地与 ROI 验证",
    summary: "把就诊前中后和患者语音入口拆成可验收、可追踪、可升级人工的生产级流程。",
  },
  {
    slug: "automotive-dfmea-ontology-agent",
    domain: "汽车工程 DFMEA",
    title: "本体智能体如何重塑安全关键零部件 DFMEA",
    summary: "以 B 柱为例，把材料、工艺、失效机理和法规要求连成可复评的风险情报系统。",
  },
  {
    slug: "manufacturing-pid-intelligence",
    domain: "工业知识资产化",
    title: "P&ID 智能化扩展工厂运营",
    summary: "把静态管线图纸变成可查询、可关联、可由工程师复核的运营知识网络。",
  },
  {
    slug: "wren-kitchens",
    domain: "制造与零售",
    title: "从紧急团队扩容到长期技术合作",
    summary: "公开案例结构样本，用于验证案例详情页、案例中心和搜索联动迁移。",
  },
];

export const navigatorOptions = [
  {
    id: "service",
    label: "客户服务",
    result: "优先验证高频问答、坐席辅助和人工接管证据。",
  },
  {
    id: "knowledge",
    label: "企业知识",
    result: "优先验证引用可信度、权限边界和复评证据。",
  },
  {
    id: "operations",
    label: "运营流程",
    result: "优先验证跨系统任务拆解、异常路径和验收指标。",
  },
];
