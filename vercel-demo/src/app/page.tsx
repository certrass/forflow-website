import Image from "next/image";
import Link from "next/link";
import type { ReactNode } from "react";
import { HomeEffects } from "@/components/home-effects";

type IconName =
  | "arrow"
  | "agent"
  | "book"
  | "briefcase"
  | "chart"
  | "check"
  | "compass"
  | "data"
  | "flow"
  | "growth"
  | "layers"
  | "people"
  | "search"
  | "shield"
  | "spark"
  | "training";

type IconProps = {
  name: IconName;
  className?: string;
};

const navItems = [
  { label: "挑战", href: "#challenges" },
  { label: "服务", href: "#services" },
  { label: "Navigator", href: "/navigator" },
  { label: "案例", href: "/cases" },
];

const assuranceItems = [
  { icon: "compass", label: "投对场景" },
  { icon: "growth", label: "算清回报" },
  { icon: "shield", label: "安全部署" },
  { icon: "flow", label: "持续运营" },
] satisfies Array<{ icon: IconName; label: string }>;

const proofItems = [
  { value: "3 分钟", label: "完成第一轮场景诊断", href: "/navigator" },
  { value: "4 条", label: "清晰的企业服务路径", href: "#services" },
  { value: "2 周起", label: "验证首个 Agent 场景", href: "#method" },
  { value: "1 套", label: "中文企业 AI 实战方法", href: "#resources" },
];

const challenges = [
  {
    icon: "briefcase",
    title: "客户触达与服务",
    text: "线索响应慢、重复问答多、服务质量不稳定。",
    items: ["智能客服与坐席辅助", "线索分流与自动跟进", "个性化推荐与预约"],
  },
  {
    icon: "spark",
    title: "营销与内容增长",
    text: "产能跟不上渠道，内容难以稳定复制和复盘。",
    items: ["多渠道内容生成", "活动策划与素材变体", "客户洞察与效果总结"],
  },
  {
    icon: "book",
    title: "企业知识与决策",
    text: "资料散落、制度难查、经验依赖少数关键员工。",
    items: ["可信知识问答与引用", "SOP 与政策助手", "经营分析与决策支持"],
  },
  {
    icon: "flow",
    title: "运营流程自动化",
    text: "跨系统复制、文档处理和异常跟进消耗大量时间。",
    items: ["文档提取与校验", "订单与工单协同", "多步骤任务编排"],
  },
  {
    icon: "chart",
    title: "财务与经营分析",
    text: "对账、报表和解释工作重复，管理层看不到及时答案。",
    items: ["对账与费用审核", "管理报表与摘要", "预测和异常提示"],
  },
  {
    icon: "people",
    title: "人才与组织赋能",
    text: "招聘、入职、培训与员工服务难以规模化。",
    items: ["招聘与候选人沟通", "入职和制度问答", "岗位培训与能力陪练"],
  },
] satisfies Array<{
  icon: IconName;
  title: string;
  text: string;
  items: string[];
}>;

const services = [
  {
    icon: "layers",
    time: "4-6 周 · 组织能力",
    title: "企业 AI 赋能计划",
    text: "把个人零散试用变成统一方法、真实任务和可衡量的团队能力。",
    items: ["机会地图与优先级", "岗位共创与试点", "治理规范与采用机制"],
  },
  {
    icon: "data",
    time: "分阶段 · 数据基础",
    title: "数据治理",
    text: "让数据找得到、看得懂、用得对，为报表、RAG 与企业 AI 建立可信底座。",
    items: ["数据资产与口径", "质量、权限与管道", "面向 AI 的知识层"],
  },
  {
    icon: "agent",
    time: "2 周验证 · 持续实施",
    title: "企业 Agent 搭建",
    text: "让 AI 连接知识、系统和规则，不只回答问题，还能在授权范围内完成工作。",
    items: ["高价值流程原型", "RAG 与系统集成", "评估、权限和监控"],
  },
  {
    icon: "training",
    time: "分层课程 · 场景共创",
    title: "企业 AI 培训",
    text: "围绕管理层、业务团队与技术团队的真实岗位，让培训直接转化为行动。",
    items: ["管理层决策与治理", "业务岗位工作坊", "技术实施与评估"],
  },
] satisfies Array<{
  icon: IconName;
  time: string;
  title: string;
  text: string;
  items: string[];
}>;

const methods = [
  {
    icon: "compass",
    label: "01 / DIAGNOSE",
    title: "场景诊断",
    text: "识别高频、高价值、数据可得且风险可控的流程，形成优先级地图。",
    output: "交付：场景地图与价值假设",
  },
  {
    icon: "spark",
    label: "02 / VALIDATE",
    title: "价值验证",
    text: "用真实任务验证质量、时效、采用意愿和单位经济性，设定继续投入门槛。",
    output: "交付：可演示原型与评估报告",
  },
  {
    icon: "shield",
    label: "03 / DEPLOY",
    title: "安全部署",
    text: "连接知识和业务系统，配置权限、审计、人工兜底与运行监控。",
    output: "交付：生产流程与治理机制",
  },
  {
    icon: "growth",
    label: "04 / GROW",
    title: "持续运营",
    text: "把反馈、知识更新和模型评估变成日常机制，持续提高业务回报。",
    output: "交付：指标看板与增长循环",
  },
] satisfies Array<{
  icon: IconName;
  label: string;
  title: string;
  text: string;
  output: string;
}>;

const caseCards = [
  {
    icon: "spark",
    meta: "教育内容 · 公开案例摘要",
    title: "把 18 小时的内容马拉松，缩短为 30 分钟的营销冲刺。",
    metric: "18h -> 30min",
    label: "单篇内容制作时间",
  },
  {
    icon: "briefcase",
    meta: "零售客服 · 公开案例摘要",
    title: "全天候响应，让团队回到高价值服务。",
    metric: "-56%",
    label: "重复任务时间",
  },
  {
    icon: "data",
    meta: "物流数据 · 公开案例摘要",
    title: "用自然语言获得多源经营数据答案。",
    metric: "-50%",
    label: "预计报表生成时间",
  },
] satisfies Array<{
  icon: IconName;
  meta: string;
  title: string;
  metric: string;
  label: string;
}>;

const resources = [
  {
    icon: "compass",
    label: "INTERACTIVE TOOL",
    title: "AI 场景诊断器",
    text: "3 分钟把业务挑战转成场景优先级和下一步建议。",
    href: "/navigator",
    cta: "开始诊断",
  },
  {
    icon: "briefcase",
    label: "CASE LIBRARY",
    title: "企业案例中心",
    text: "按问题、过程和结果阅读公开案例，验证案例页迁移结构。",
    href: "/cases",
    cta: "查看案例",
  },
  {
    icon: "search",
    label: "PREVIEW ROUTE",
    title: "Vercel 预览首页",
    text: "先把首页迁成组件化结构，再逐步迁移搜索、手册和服务详情页。",
    href: "#main",
    cta: "回到顶部",
  },
] satisfies Array<{
  icon: IconName;
  label: string;
  title: string;
  text: string;
  href: string;
  cta: string;
}>;

const faqs = [
  {
    question: "ForFlow 与购买一个 AI 工具有何不同？",
    answer:
      "工具解决一个操作点；ForFlow 关注从场景选择、数据和系统接入，到权限、评估和持续运营的完整链路。企业最终拥有的是一套可复用的流程能力，而不是一项孤立订阅。",
  },
  {
    question: "我们应该先买成熟产品，还是定制建设？",
    answer:
      "需求通用、希望快速起步时优先买；流程独特、数据敏感、需要深度集成或能形成竞争优势时考虑定制。多数企业适合先买后建、边用边学。",
  },
  {
    question: "第一个场景通常如何控制风险？",
    answer:
      "从低风险、可人工复核的任务开始，限制数据范围和操作权限，设置引用、日志、质量评估和人工兜底；在达到明确门槛后再扩大范围。",
  },
  {
    question: "管理层、业务与技术团队分别需要参与什么？",
    answer:
      "管理层负责目标、资源和责任边界；业务团队提供真实流程、数据与验收标准；技术团队负责集成、安全、评估和运行。三方缺一，项目都容易停在演示阶段。",
  },
];

export default function Home() {
  return (
    <main id="main" className="ff-home-v4 min-h-screen bg-white text-[#050505]">
      <HomeEffects />
      <UtilityBar />
      <Header />
      <Hero />
      <Manifesto />
      <Challenges />
      <Services />
      <NavigatorSection />
      <Method />
      <Cases />
      <Resources />
      <Faq />
      <Footer />
    </main>
  );
}

function UtilityBar() {
  return (
    <div className="ff-utility-demo border-b border-[#dfe3dc] bg-[#050505] text-white">
      <div className="mx-auto flex max-w-[1380px] items-center justify-between gap-4 px-5 py-2 text-xs font-semibold sm:px-6 lg:px-8">
        <span>AI Flows. Business Grows.</span>
        <span className="hidden text-[#d8ffdf] sm:inline">Next.js pilot / Vercel preview</span>
      </div>
    </div>
  );
}

function Header() {
  return (
    <header className="ff-header-demo sticky top-0 z-50 border-b border-[#dfe3dc] bg-white/95 backdrop-blur-xl">
      <div className="mx-auto flex h-[76px] max-w-[1380px] items-center justify-between gap-5 px-5 sm:px-6 lg:px-8">
        <Link href="/" aria-label="ForFlow 首页" className="inline-flex shrink-0 items-center">
          <Image
            src="/forflow/forflow-lockup-transparent.png"
            alt="ForFlow 萬維流形"
            width={214}
            height={80}
            priority
            className="h-auto w-[172px] sm:w-[204px]"
          />
        </Link>
        <nav aria-label="主导航" className="hidden items-center gap-1 lg:flex">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-[8px] px-3 py-2 text-sm font-semibold text-[#343934] transition hover:bg-[#f2f4ef]"
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <Link
            href="/navigator"
            className="inline-flex h-11 items-center justify-center gap-2 rounded-[8px] bg-[#63f578] px-4 text-sm font-bold text-[#050505] transition hover:bg-[#43e75d]"
          >
            开始诊断
            <Icon name="arrow" className="h-4 w-4" />
          </Link>
        </div>
      </div>
    </header>
  );
}

function Hero() {
  return (
    <section className="ff-hero relative overflow-hidden border-b border-[#dfe3dc] bg-[#fbfcfa]">
      <div
        className="ff-hero-gridline pointer-events-none absolute inset-0 opacity-45"
        style={{
          backgroundImage:
            "linear-gradient(rgba(5,5,5,.05) 1px, transparent 1px), linear-gradient(90deg, rgba(5,5,5,.05) 1px, transparent 1px)",
          backgroundSize: "56px 56px",
        }}
      />
      <div className="ff-hero-grid relative mx-auto grid min-h-[760px] max-w-[1380px] items-center gap-12 px-5 py-14 sm:px-6 lg:grid-cols-[0.92fr_1.08fr] lg:px-8 lg:py-20">
        <div className="ff-hero-copy max-w-3xl" data-reveal>
          <p className="ff-kicker mb-5 flex items-center gap-3 text-xs font-black uppercase text-[#123d19]">
            <span className="h-1 w-9 rounded-full bg-[#63f578]" />
            AI-NATIVE BUSINESS FLOW RUNTIME
          </p>
          <h1 className="ff-hero-title text-6xl font-black leading-[0.95] text-[#050505] sm:text-7xl lg:text-8xl">
            让 AI 真正
            <br />
            <span className="ff-hero-outline">流入业务。</span>
          </h1>
          <p className="ff-hero-lead mt-7 max-w-2xl text-lg leading-8 text-[#4f584f] sm:text-xl">
            从高价值场景切入，把模型、企业知识、业务系统与治理规则连成一条能运行、能衡量、能持续优化的
            AI 工作流。
          </p>
          <div className="ff-hero-actions mt-9 flex flex-col gap-3 sm:flex-row">
            <Link
              href="/navigator"
              className="inline-flex h-12 items-center justify-center gap-2 rounded-[8px] bg-[#63f578] px-5 text-sm font-black text-[#050505] transition hover:bg-[#43e75d]"
            >
              开始场景诊断
              <Icon name="arrow" className="h-4 w-4" />
            </Link>
            <Link
              href="#services"
              className="inline-flex h-12 items-center justify-center gap-2 rounded-[8px] border border-[#cbd2c9] bg-white px-5 text-sm font-black text-[#050505] transition hover:border-[#9aa597]"
            >
              查看企业服务
              <Icon name="arrow" className="h-4 w-4 rotate-90" />
            </Link>
          </div>
          <ul className="ff-hero-assurance mt-8 grid max-w-xl grid-cols-2 gap-3 text-sm font-bold text-[#262b26] sm:flex sm:flex-wrap">
            {assuranceItems.map((item) => (
              <li key={item.label} className="flex items-center gap-2">
                <Icon name={item.icon} className="h-4 w-4 text-[#0b641c]" />
                {item.label}
              </li>
            ))}
          </ul>
        </div>

        <div className="ff-hero-visual relative min-h-[520px] lg:min-h-[650px]" data-reveal>
          <div className="ff-hero-photo absolute inset-0 overflow-hidden rounded-[8px] border border-[#d8ddd5] bg-white shadow-[0_28px_70px_rgba(0,0,0,0.16)]">
            <Image
              src="/forflow/hero-hand.jpg"
              alt="手持透明 ForFlow 标识卡片的品牌视觉"
              fill
              priority
              sizes="(max-width: 1024px) 100vw, 52vw"
              className="ff-hero-img object-cover"
            />
            <div className="ff-hero-fade absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-white via-white/75 to-transparent" />
            <div aria-hidden="true" className="ff-vertical-type">
              DIAGNOSIS
              <br />
              DEPLOYMENT
              <br />
              GROWTH
            </div>
            <svg
              aria-hidden="true"
              className="ff-flow-line absolute left-[-6%] top-[26%] h-[44%] w-[112%] text-[#63f578]"
              viewBox="0 0 760 360"
            >
              <path
                d="M-40 230C105 85 207 290 344 154S545 281 805 111"
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeWidth="4"
              />
            </svg>
            <span className="ff-flow-node node-a" />
            <span className="ff-flow-node node-b" />
            <span className="ff-flow-node node-c" />
          </div>
          <HeroFloat
            icon="flow"
            className="ff-float-card-top left-3 top-5 sm:left-7 sm:top-10"
            label="业务流程覆盖"
            value="端到端"
            text="从问题定位到持续运行"
          />
          <HeroFloat
            icon="layers"
            className="ff-float-card-bottom bottom-6 right-3 sm:bottom-10 sm:right-7"
            label="企业专属资产"
            value="可拥有 · 可迭代"
            text="流程、知识和评估一起沉淀"
          />
          <div className="ff-hero-caption absolute bottom-5 left-5 rounded-[8px] border border-[#dfe3dc] bg-white/95 p-4 text-xs font-bold shadow-[0_18px_50px_rgba(0,0,0,0.13)] backdrop-blur">
            <span className="text-[#0b641c]">FORFLOW / 01</span>
            <p className="mt-1 leading-5">AI Flows. Business Grows.</p>
          </div>
        </div>
      </div>

      <div className="ff-proof-band relative mx-auto grid max-w-[1380px] gap-3 px-5 pb-10 sm:px-6 md:grid-cols-2 lg:grid-cols-4 lg:px-8">
        {proofItems.map((item) => (
          <Link
            key={item.value}
            href={item.href}
            className="group flex items-center justify-between rounded-[8px] border border-[#d8ddd5] bg-white p-5 transition hover:border-[#63f578] hover:shadow-[0_14px_34px_rgba(0,0,0,0.08)]"
          >
            <span>
              <strong className="block text-2xl font-black">{item.value}</strong>
              <span className="mt-1 block text-sm font-semibold text-[#5d655e]">{item.label}</span>
            </span>
            <Icon name="arrow" className="h-5 w-5 text-[#0b641c] transition group-hover:translate-x-1" />
          </Link>
        ))}
      </div>
    </section>
  );
}

function HeroFloat({
  icon,
  label,
  value,
  text,
  className,
}: {
  icon: IconName;
  label: string;
  value: string;
  text: string;
  className: string;
}) {
  return (
    <div
      className={`ff-float-card absolute flex max-w-[250px] items-center gap-3 rounded-[8px] border border-[#d8ddd5] bg-white/95 p-4 shadow-[0_18px_50px_rgba(0,0,0,0.14)] backdrop-blur ${className}`}
    >
      <span className="grid h-11 w-11 shrink-0 place-items-center rounded-[8px] bg-[#e5ffe9] text-[#0b641c]">
        <Icon name={icon} className="h-5 w-5" />
      </span>
      <span>
        <small className="block text-[11px] font-black text-[#6b746b]">{label}</small>
        <strong className="mt-1 block text-sm font-black text-[#050505]">{value}</strong>
        <span className="mt-1 block text-xs leading-5 text-[#5d655e]">{text}</span>
      </span>
    </div>
  );
}

function Manifesto() {
  return (
    <section id="platform" className="ff-section ff-manifesto bg-white py-20 sm:py-24 lg:py-28" data-section>
      <div className="ff-manifesto-grid mx-auto grid max-w-[1380px] gap-10 px-5 sm:px-6 lg:grid-cols-[0.86fr_0.84fr_1.3fr] lg:items-center lg:px-8">
        <div data-reveal>
          <SectionKicker>FROM TOOLS TO ORGANIZATIONAL AI</SectionKicker>
          <h2 className="mt-5 text-4xl font-black leading-tight sm:text-5xl lg:text-6xl">
            工具会更换。
            <br />
            流程、数据和能力
            <br />
            <span className="text-[#0b641c]">应该留在企业。</span>
          </h2>
        </div>
        <div className="ff-manifesto-copy space-y-5 text-base leading-8 text-[#4f584f]" data-reveal>
          <p>多数 AI 项目卡住，并不是模型不够强，而是业务目标不清、知识没有治理、系统没有连接、责任边界没有定义。</p>
          <p>ForFlow 把这些工作放进同一套运行方法：从企业问题出发，用小步验证建立信心，再把有效能力接进真实流程。</p>
        </div>
        <div className="ff-system-map relative min-h-[360px] overflow-hidden rounded-[8px] border border-[#d8ddd5] bg-[#f4f5f3] p-6" data-reveal>
          <div className="ff-system-ring ff-system-ring--outer absolute inset-6 rounded-full border border-[#cbd2c9]"><span>GROWTH LOOP</span></div>
          <div className="ff-system-ring ff-system-ring--middle absolute inset-14 rounded-full border border-[#b5c0b2]"><span>FLOW RUNTIME</span></div>
          <div className="ff-system-ring ff-system-ring--inner absolute inset-24 rounded-full border border-[#8fdc99]"><span>SCENE MAP</span></div>
          <div className="relative z-10 flex h-full min-h-[308px] items-end">
            <div className="w-full rounded-[8px] border border-[#d8ddd5] bg-white p-5 shadow-[0_18px_50px_rgba(0,0,0,0.08)]">
              <small className="text-xs font-black text-[#0b641c]">企业 AI 增长运行层</small>
              <strong className="mt-2 block text-xl font-black">场景 - 数据 - 流程 - 治理 - 指标</strong>
              <p className="mt-3 text-sm leading-6 text-[#5d655e]">每一次使用都产生可复用的组织资产。</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Challenges() {
  return (
    <section id="challenges" className="ff-section ff-challenges bg-[#f4f5f3] py-20 sm:py-24 lg:py-28" data-section>
      <div className="mx-auto max-w-[1380px] px-5 sm:px-6 lg:px-8">
        <SectionHead
          kicker="START WITH A BUSINESS CHALLENGE"
          title={
            <>
              先说清楚哪里最痛，
              <br />
              再讨论 AI 怎么做。
            </>
          }
          text="选择与你当前问题最接近的一项。每个入口都会带着预设场景进入 Navigator，减少从空白开始的成本。"
        />
        <div className="ff-challenge-grid mt-12 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {challenges.map((challenge, index) => (
            <Link
              key={challenge.title}
              href="/navigator"
              className="ff-challenge-card group rounded-[8px] border border-[#d8ddd5] bg-white p-6 transition hover:border-[#63f578] hover:shadow-[0_18px_44px_rgba(0,0,0,0.08)]"
              data-reveal
            >
              <div className="flex items-start justify-between gap-4">
                <span className="text-sm font-black text-[#7b857b]">0{index + 1}</span>
                <span className="grid h-12 w-12 place-items-center rounded-[8px] bg-[#e5ffe9] text-[#0b641c]">
                  <Icon name={challenge.icon} className="h-6 w-6" />
                </span>
              </div>
              <h3 className="mt-8 text-2xl font-black">{challenge.title}</h3>
              <p className="mt-3 min-h-[56px] text-sm leading-7 text-[#5d655e]">{challenge.text}</p>
              <ul className="mt-6 space-y-2 text-sm font-semibold text-[#2c332c]">
                {challenge.items.map((item) => (
                  <li key={item} className="flex items-center gap-2">
                    <Icon name="check" className="h-4 w-4 text-[#0b641c]" />
                    {item}
                  </li>
                ))}
              </ul>
              <span className="mt-8 inline-flex items-center gap-2 text-sm font-black text-[#0b641c]">
                进入诊断
                <Icon name="arrow" className="h-4 w-4 transition group-hover:translate-x-1" />
              </span>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

function Services() {
  return (
    <section id="services" className="ff-section ff-services bg-[#050505] py-20 text-white sm:py-24 lg:py-28" data-section>
      <div className="mx-auto max-w-[1380px] px-5 sm:px-6 lg:px-8">
        <div className="ff-services-head grid gap-8 lg:grid-cols-[0.92fr_1.08fr] lg:items-end">
          <div>
            <SectionKicker tone="dark">THE RIGHT PATH, RIGHT NOW</SectionKicker>
            <h2 className="mt-5 text-4xl font-black leading-tight sm:text-5xl lg:text-6xl">
              四条路径，
              <br />
              对应四种企业处境。
            </h2>
          </div>
          <p className="max-w-2xl text-base leading-8 text-[#b6bdb6]">
            像选择业务方案一样选择 AI 服务：看当前瓶颈、现有基础、希望多快见效，以及企业需要保留多少控制权。
          </p>
        </div>

        <div className="ff-service-list mt-12 overflow-hidden rounded-[8px] border border-white/15">
          {services.map((service, index) => (
            <Link
              key={service.title}
              href="/navigator"
              className="ff-service-row group grid gap-5 border-b border-white/15 p-5 transition last:border-b-0 hover:bg-white/[0.06] sm:p-6 lg:grid-cols-[70px_76px_1fr_0.92fr_48px] lg:items-center"
              data-reveal
            >
              <span className="text-sm font-black text-[#63f578]">0{index + 1}</span>
              <span className="grid h-14 w-14 place-items-center rounded-[8px] border border-white/15 bg-white/[0.08] text-[#63f578]">
                <Icon name={service.icon} className="h-7 w-7" />
              </span>
              <span>
                <small className="text-xs font-black text-[#aeb7ae]">{service.time}</small>
                <strong className="mt-2 block text-2xl font-black">{service.title}</strong>
                <span className="mt-2 block max-w-2xl text-sm leading-7 text-[#c7cec7]">{service.text}</span>
              </span>
              <span className="grid gap-2 text-sm font-semibold text-[#d9dfd9] sm:grid-cols-3 lg:grid-cols-1">
                {service.items.map((item) => (
                  <span key={item}>{item}</span>
                ))}
              </span>
              <Icon name="arrow" className="h-5 w-5 text-[#63f578] transition group-hover:translate-x-1" />
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

function NavigatorSection() {
  return (
    <section id="navigator" className="ff-section ff-navigator bg-[#eef2ea] py-20 sm:py-24 lg:py-28" data-section>
      <div className="ff-navigator-grid mx-auto grid max-w-[1380px] gap-10 px-5 sm:px-6 lg:grid-cols-[0.84fr_1.16fr] lg:items-center lg:px-8">
        <div className="ff-navigator-copy" data-reveal>
          <SectionKicker>FORFLOW AI NAVIGATOR</SectionKicker>
          <h2 className="mt-5 text-4xl font-black leading-tight sm:text-5xl lg:text-6xl">
            3 分钟，定位
            <br />
            第一条 AI 增长流。
          </h2>
          <p className="mt-6 max-w-xl text-base leading-8 text-[#4f584f]">
            从业务挑战、价值目标、数据条件和部署偏好出发，生成一份可以拿去内部讨论的场景优先级与行动建议。
          </p>
          <ol className="mt-8 border-y border-[#d8ddd5]">
            {["选择当前最重要的业务挑战", "明确效率、收入、体验或风险目标", "说明数据、系统和部署条件", "获得匹配方案与下一步路线"].map(
              (item, index) => (
                <li
                  key={item}
                  className="grid grid-cols-[42px_1fr] gap-3 border-b border-[#d8ddd5] py-3 text-sm font-bold last:border-b-0"
                >
                  <span className="text-xs font-black text-[#0b641c]">0{index + 1}</span>
                  {item}
                </li>
              ),
            )}
          </ol>
          <Link
            href="/navigator"
            className="mt-8 inline-flex h-12 items-center justify-center gap-2 rounded-[8px] bg-[#63f578] px-5 text-sm font-black text-[#050505] transition hover:bg-[#43e75d]"
          >
            启动 Navigator
            <Icon name="arrow" className="h-4 w-4" />
          </Link>
        </div>

        <div className="ff-navigator-visual relative min-h-[520px] overflow-hidden rounded-[8px] border border-[#d8ddd5] bg-[#0b1511] lg:min-h-[650px]" data-reveal>
          <Image
            src="/forflow/flow-runtime.png"
            alt="蓝绿色流线构成的 AI 运行视觉"
            fill
            sizes="(max-width: 1024px) 100vw, 55vw"
            className="object-cover opacity-75"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[#0b1511]/70 via-transparent to-transparent" />
          <div className="ff-navigator-ui absolute inset-x-4 bottom-4 rounded-[8px] border border-white/18 bg-white/90 p-4 text-[#050505] shadow-[0_24px_60px_rgba(0,0,0,0.24)] backdrop-blur sm:inset-x-8 sm:bottom-8 sm:p-6">
            <div className="ff-navigator-ui-head flex items-center gap-2 border-b border-[#d8ddd5] pb-4">
              <span className="h-2.5 w-2.5 rounded-full bg-[#ff5f57]" />
              <span className="h-2.5 w-2.5 rounded-full bg-[#ffbd2e]" />
              <span className="h-2.5 w-2.5 rounded-full bg-[#28c840]" />
              <small className="ml-auto text-xs font-black text-[#5d655e]">AI SCENE NAVIGATOR</small>
            </div>
            <p className="mt-5 text-xs font-black text-[#0b641c]">STEP 01 / BUSINESS CHALLENGE</p>
            <h3 className="mt-2 text-2xl font-black">你现在最想改善哪一段业务？</h3>
            <div className="ff-navigator-options mt-5 grid grid-cols-2 gap-2 sm:grid-cols-4">
              {["客户服务", "营销增长", "知识管理", "运营效率"].map((item, index) => (
                <span
                  key={item}
                  className={`rounded-[8px] border px-3 py-3 text-center text-xs font-black ${
                    index === 0
                      ? "border-[#63f578] bg-[#e5ffe9] text-[#0b641c]"
                      : "border-[#d8ddd5] bg-white text-[#343934]"
                  }`}
                >
                  {item}
                </span>
              ))}
            </div>
            <div className="ff-navigator-foot mt-5 flex items-center gap-4">
              <small className="text-xs font-black text-[#5d655e]">已完成 1 / 4</small>
              <span className="h-2 flex-1 rounded-full bg-[#e0e6dd]">
                <span className="block h-2 w-1/4 rounded-full bg-[#63f578]" />
              </span>
              <strong className="text-sm font-black text-[#0b641c]">继续</strong>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Method() {
  return (
    <section id="method" className="ff-section ff-method bg-white py-20 sm:py-24 lg:py-28" data-section>
      <div className="mx-auto max-w-[1380px] px-5 sm:px-6 lg:px-8">
        <SectionHead
          kicker="A CONTROLLED PATH TO VALUE"
          title={
            <>
              从一条流开始，
              <br />
              走向组织级 AI。
            </>
          }
          text="每一步都留下可审查的业务依据、技术资产和下一阶段决策条件，避免一次性大项目。"
        />
        <div className="ff-method-track mt-12 grid overflow-hidden rounded-[8px] border border-[#d8ddd5] md:grid-cols-2 xl:grid-cols-4">
          {methods.map((method) => (
            <article key={method.label} className="border-b border-[#d8ddd5] p-6 last:border-b-0 md:border-r md:even:border-r-0 xl:border-b-0 xl:even:border-r xl:last:border-r-0" data-reveal>
              <span className="grid h-12 w-12 place-items-center rounded-[8px] bg-[#e5ffe9] text-[#0b641c]">
                <Icon name={method.icon} className="h-6 w-6" />
              </span>
              <small className="mt-10 block text-xs font-black text-[#788078]">{method.label}</small>
              <h3 className="mt-3 text-2xl font-black">{method.title}</h3>
              <p className="mt-3 text-sm leading-7 text-[#565d56]">{method.text}</p>
              <b className="mt-7 block border-t border-[#d8ddd5] pt-4 text-sm">{method.output}</b>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function Cases() {
  return (
    <section id="cases" className="ff-section ff-cases bg-[#050505] py-20 text-white sm:py-24 lg:py-28" data-section>
      <div className="mx-auto max-w-[1380px] px-5 sm:px-6 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-[1fr_auto] lg:items-end">
          <div>
            <SectionKicker tone="dark">REAL PROBLEMS, MEASURABLE OUTCOMES</SectionKicker>
            <h2 className="mt-5 text-4xl font-black leading-tight sm:text-5xl lg:text-6xl">
              案例不只讲技术，
              <br />
              要讲业务前后发生了什么。
            </h2>
          </div>
          <Link href="/cases" className="inline-flex items-center gap-2 text-sm font-black text-[#63f578]">
            查看案例中心
            <Icon name="arrow" className="h-4 w-4" />
          </Link>
        </div>

        <div className="ff-case-grid mt-12 grid gap-4 lg:grid-cols-[1.2fr_0.9fr_0.9fr]">
          {caseCards.map((item, index) => (
            <Link
              key={item.title}
              href="/cases"
              className={`ff-case-card group rounded-[8px] border border-white/15 bg-white/[0.06] p-5 transition hover:border-[#63f578] sm:p-6 ${index === 0 ? "ff-case-card-feature" : ""}`}
              data-reveal
            >
              <div className={`ff-case-art ff-case-art-${index} grid place-items-center rounded-[8px] ${index === 0 ? "h-48" : "h-36"} bg-white/[0.08] text-[#63f578]`}>
                <Icon name={item.icon} className={index === 0 ? "h-16 w-16" : "h-12 w-12"} />
              </div>
              <small className="mt-6 block text-xs font-black text-[#b8beb8]">{item.meta}</small>
              <h3 className="mt-3 text-2xl font-black leading-tight">{item.title}</h3>
              <div className="mt-6">
                <strong className="block text-3xl font-black text-[#63f578]">{item.metric}</strong>
                <span className="mt-1 block text-sm text-[#c7cec7]">{item.label}</span>
              </div>
              <span className="mt-7 inline-flex items-center gap-2 text-sm font-black text-[#63f578]">
                阅读案例
                <Icon name="arrow" className="h-4 w-4 transition group-hover:translate-x-1" />
              </span>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

function Resources() {
  return (
    <section id="resources" className="ff-section ff-resources bg-[#f4f5f3] py-20 sm:py-24 lg:py-28" data-section>
      <div className="mx-auto max-w-[1380px] px-5 sm:px-6 lg:px-8">
        <SectionHead
          kicker="TOOLS & GUIDES"
          title={
            <>
              按你所在的阶段，
              <br />
              选择下一步。
            </>
          }
          text="还在判断机会、正在比较方案，或准备组织实施，都有一个更低门槛的入口。"
        />
        <div className="ff-resource-grid mt-12 grid gap-4 md:grid-cols-3">
          {resources.map((item, index) => (
            <Link
              key={item.title}
              href={item.href}
              className={`ff-resource-card group rounded-[8px] border border-[#d8ddd5] bg-white p-6 transition hover:border-[#63f578] hover:shadow-[0_18px_44px_rgba(0,0,0,0.08)] ${index === 0 ? "ff-resource-card-green" : ""} ${index === 1 ? "ff-resource-card-dark" : ""}`}
              data-reveal
            >
              <span className="grid h-12 w-12 place-items-center rounded-[8px] bg-[#e5ffe9] text-[#0b641c]">
                <Icon name={item.icon} className="h-6 w-6" />
              </span>
              <small className="mt-8 block text-xs font-black text-[#6b746b]">{item.label}</small>
              <h3 className="mt-3 text-2xl font-black">{item.title}</h3>
              <p className="mt-3 min-h-[72px] text-sm leading-7 text-[#5d655e]">{item.text}</p>
              <span className="mt-7 inline-flex items-center gap-2 text-sm font-black text-[#0b641c]">
                {item.cta}
                <Icon name="arrow" className="h-4 w-4 transition group-hover:translate-x-1" />
              </span>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

function Faq() {
  return (
    <section id="faq" className="ff-section ff-faq bg-white py-20 sm:py-24 lg:py-28" data-section>
      <div className="ff-faq-grid mx-auto grid max-w-[1380px] gap-10 px-5 sm:px-6 lg:grid-cols-[0.7fr_1.3fr] lg:px-8">
        <div data-reveal>
          <SectionKicker>FREQUENTLY ASKED</SectionKicker>
          <h2 className="mt-5 text-4xl font-black leading-tight sm:text-5xl lg:text-6xl">
            企业主最常问的
            <br />
            四个问题。
          </h2>
          <p className="mt-6 max-w-md text-base leading-8 text-[#5d655e]">答案先讲清决策逻辑，再进入技术细节。</p>
        </div>
        <div className="ff-faq-list divide-y divide-[#d8ddd5] border-y border-[#d8ddd5]" data-reveal>
          {faqs.map((faq, index) => (
            <details key={faq.question} className="group" open={index === 0}>
              <summary className="flex cursor-pointer list-none items-center justify-between gap-6 py-6 text-lg font-black">
                {faq.question}
                <span className="grid h-8 w-8 shrink-0 place-items-center rounded-[8px] border border-[#d8ddd5] text-[#0b641c] transition group-open:rotate-45">
                  +
                </span>
              </summary>
              <p className="max-w-3xl pb-6 text-base leading-8 text-[#596059]">{faq.answer}</p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer id="contact" className="ff-footer-demo border-t border-[#d8ddd5] bg-[#050505] text-white">
      <div className="mx-auto max-w-[1380px] px-5 py-16 sm:px-6 lg:px-8">
        <p className="text-base font-black text-[#63f578]">下一步，不需要先买工具。</p>
        <div className="mt-4 grid gap-8 lg:grid-cols-[1fr_auto] lg:items-end">
          <h2 className="max-w-3xl text-4xl font-black leading-tight sm:text-5xl lg:text-6xl">
            先把最值得改变的
            <br />
            那一段业务说清楚。
          </h2>
          <Link
            href="/navigator"
            className="inline-flex h-12 items-center justify-center gap-2 rounded-[8px] bg-[#63f578] px-5 text-sm font-black text-[#050505] transition hover:bg-[#43e75d]"
          >
            开始 3 分钟诊断
            <Icon name="arrow" className="h-4 w-4" />
          </Link>
        </div>
        <div className="mt-14 grid gap-8 border-t border-white/14 pt-8 md:grid-cols-[1.2fr_0.8fr_0.8fr]">
          <div>
            <Image
              src="/forflow/forflow-lockup-transparent.png"
              alt="ForFlow 萬維流形"
              width={214}
              height={80}
              className="h-auto w-[190px] invert"
            />
            <p className="mt-5 max-w-md text-sm leading-7 text-[#c7cec7]">
              面向企业的 AI 原生增长运行层。从高价值场景、安全落地到持续运营。
            </p>
          </div>
          <div className="grid gap-3 text-sm text-[#d9dfd9]">
            <strong className="text-white">企业服务</strong>
            <Link href="#services">企业 AI 赋能计划</Link>
            <Link href="#services">数据治理</Link>
            <Link href="#services">企业 Agent 搭建</Link>
            <Link href="#services">企业 AI 培训</Link>
          </div>
          <div className="grid gap-3 text-sm text-[#d9dfd9]">
            <strong className="text-white">工具与资源</strong>
            <Link href="/navigator">AI 场景诊断</Link>
            <Link href="/cases">案例中心</Link>
            <Link href="#resources">预览资源</Link>
          </div>
        </div>
        <div className="mt-10 flex flex-col gap-2 border-t border-white/14 pt-5 text-xs font-semibold text-[#9aa39a] sm:flex-row sm:justify-between">
          <span>© 2026 ForFlow.ai 萬維流形</span>
          <span>Next.js Vercel demo · production domain stays on Netlify</span>
        </div>
      </div>
    </footer>
  );
}

function SectionHead({
  kicker,
  title,
  text,
}: {
  kicker: string;
  title: ReactNode;
  text: string;
}) {
  return (
    <div className="ff-section-head grid gap-7 lg:grid-cols-[1fr_0.72fr] lg:items-end" data-reveal>
      <div>
        <SectionKicker>{kicker}</SectionKicker>
        <h2 className="mt-5 text-4xl font-black leading-tight sm:text-5xl lg:text-6xl">{title}</h2>
      </div>
      <p className="max-w-2xl text-base leading-8 text-[#5d655e]">{text}</p>
    </div>
  );
}

function SectionKicker({
  children,
  tone = "light",
}: {
  children: ReactNode;
  tone?: "light" | "dark";
}) {
  return (
    <p
      className={`ff-kicker flex items-center gap-3 text-xs font-black uppercase ${
        tone === "dark" ? "text-[#d8ffdf]" : "text-[#123d19]"
      }`}
    >
      <span className="h-1 w-9 rounded-full bg-[#63f578]" />
      {children}
    </p>
  );
}

function Icon({ name, className = "h-5 w-5" }: IconProps) {
  const common = "fill-none stroke-current stroke-[2] stroke-linecap-round stroke-linejoin-round";

  return (
    <svg aria-hidden="true" className={className} viewBox="0 0 24 24">
      {name === "arrow" && <path className={common} d="M5 19 19 5M9 5h10v10" />}
      {name === "agent" && (
        <>
          <rect className={common} height="11" rx="3" width="14" x="5" y="7" />
          <path className={common} d="M9 11h.01M15 11h.01M9 15h6M12 7V4m-2 0h4M3 12H1m22 0h-2" />
        </>
      )}
      {name === "book" && (
        <path
          className={common}
          d="M4 5.5A3.5 3.5 0 0 1 7.5 2H11v17H7.5A3.5 3.5 0 0 0 4 22V5.5ZM20 5.5A3.5 3.5 0 0 0 16.5 2H13v17h3.5A3.5 3.5 0 0 1 20 22V5.5Z"
        />
      )}
      {name === "briefcase" && (
        <>
          <rect className={common} height="15" rx="2" width="18" x="3" y="5" />
          <path className={common} d="M8 5V3h8v2M3 10h18M9 14h6" />
        </>
      )}
      {name === "chart" && (
        <>
          <path className={common} d="M4 19V5m0 14h16" />
          <path className={common} d="m7 15 4-4 3 2 5-6M15 7h4v4" />
        </>
      )}
      {name === "check" && <path className={common} d="m5 12 4 4L19 6" />}
      {name === "compass" && (
        <>
          <circle className={common} cx="12" cy="12" r="9" />
          <path className={common} d="m15.5 8.5-2.1 4.9-4.9 2.1 2.1-4.9 4.9-2.1Z" />
        </>
      )}
      {name === "data" && (
        <>
          <ellipse className={common} cx="12" cy="5" rx="8" ry="3" />
          <path className={common} d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6" />
        </>
      )}
      {name === "flow" && (
        <>
          <path className={common} d="M3 7h6a3 3 0 0 1 3 3v4a3 3 0 0 0 3 3h6" />
          <circle className={common} cx="3" cy="7" r="1.5" />
          <circle className={common} cx="21" cy="17" r="1.5" />
        </>
      )}
      {name === "growth" && (
        <>
          <path className={common} d="M4 19V5m0 14h16" />
          <path className={common} d="m7 15 4-4 3 2 5-6M15 7h4v4" />
        </>
      )}
      {name === "layers" && (
        <>
          <path className={common} d="m12 3 9 5-9 5-9-5 9-5Z" />
          <path className={common} d="m3 12 9 5 9-5M3 16l9 5 9-5" />
        </>
      )}
      {name === "people" && (
        <>
          <circle className={common} cx="9" cy="8" r="3" />
          <circle className={common} cx="17" cy="9" r="2" />
          <path className={common} d="M3 20c0-4 2.5-7 6-7s6 3 6 7M14 14c3.5 0 6 2.2 6 6" />
        </>
      )}
      {name === "search" && (
        <>
          <circle className={common} cx="10.5" cy="10.5" r="6.5" />
          <path className={common} d="m15.3 15.3 5.2 5.2" />
        </>
      )}
      {name === "shield" && (
        <>
          <path className={common} d="M12 3 4 6v6c0 5 3.3 8 8 9 4.7-1 8-4 8-9V6l-8-3Z" />
          <path className={common} d="m8.5 12 2.2 2.2 4.8-5" />
        </>
      )}
      {name === "spark" && (
        <path
          className={common}
          d="m12 2 1.6 5.4L19 9l-5.4 1.6L12 16l-1.6-5.4L5 9l5.4-1.6L12 2ZM19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8L19 15ZM5 14l.7 1.8L7.5 16l-1.8.7L5 18.5l-.7-1.8L2.5 16l1.8-.7L5 14Z"
        />
      )}
      {name === "training" && (
        <>
          <path className={common} d="m3 9 9-5 9 5-9 5-9-5Z" />
          <path className={common} d="M7 12v4c2.8 2.2 7.2 2.2 10 0v-4M21 9v6" />
        </>
      )}
    </svg>
  );
}
