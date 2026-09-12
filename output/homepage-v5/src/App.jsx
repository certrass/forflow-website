import React, { useEffect, useState, useRef } from 'react';
import {WorkflowHero, ProductStories} from './Showcase.jsx';
import { ArrowRight, ArrowUpRight, ArrowUp, CaretDown, CaretRight, Check, CheckCircle, Circle, Database, FileText, Files, FlowArrow, MagnifyingGlass, Play, ArrowCounterClockwise, SidebarSimple, Clock, DotsThree, List, X, ShieldCheck, LinkSimple, Quotes, Table, Buildings, Lightning, GitBranch, BookOpen, WarningCircle } from '@phosphor-icons/react';

const site = 'https://forflow.ai';
const caseBriefs = {
  supply: {
    title: '异常查清之后，谁来推动下一步？',
    problem: '渠道数据分散在订单、履行和信用控制记录里。业务人员查清原因后，还要整理材料、找人审批。',
    deliverable: '把异常、分析依据和订单放行请求放在一起，交给有权限的负责人确认。',
    measure: '用同一批业务问题，对比查数与分析耗时、结论正确性，以及行动材料是否完整。',
    attribution: '基于团队成员在原组织的供应链实践；本页使用演示数据。'
  },
  docs: {
    title: '字段提取出来之后，能不能继续用？',
    problem: '合同、对账单格式不同，提取结果缺少统一口径，关键字段仍需要逐项翻回原文检查。',
    deliverable: '先定义字段与校验规则，再生成带原文位置的结构化结果。异常项进入复核，确认后输出 JSON / CSV。',
    measure: '用企业文档样本，检查字段准确率、遗漏情况、人工复核量，以及下游系统能否接收。',
    attribution: '基于现有文档自动化工程方法；不作为已验证客户收益。'
  },
  knowledge: {
    title: '查到一张图纸，怎样找到设备关系？',
    problem: '工程知识保存在多页 PDF 里，设备上下游关系与图纸版本依赖人工查找和资深工程师的经验。',
    deliverable: '关联设备、管线和文档，回答时提供图纸出处。关键连接与版本由工程师复核。',
    measure: '选一组设备查询任务，检查定位是否准确、连接关系是否完整、图纸版本是否一致。',
    attribution: '基于团队成员加入 ForFlow 前的 P&ID 实践；新项目按自己的工程资料验证。'
  }
};
const scenarios = [
  { id:'supply', label:'供应链决策', Icon:FlowArrow, title:'渠道履行分析', question:'上个月的渠道履行情况，有哪些需要关注？', result:'找到异常，也找到下一步。', detail:'渠道 B 的履行异常集中在鞋类订单。未付款订单触发信用控制，需要业务与信用控制团队共同确认。', sources:['渠道履行明细','订单状态记录','信用控制规则'], steps:['对齐履行率口径','定位品类与时间窗口','核对信用控制记录','整理报告与审批摘要'], output:'订单放行请求', owner:'信用控制负责人', evidence:'case-supply-chain-agentic-decision', kind:'团队过往实践', conclusion:'人工确认后，再进入后续业务流程。' },
  { id:'docs', label:'文档自动化', Icon:Files, title:'合同字段复核', question:'提取这份供应商合同中的关键字段，并标出需要复核的内容。', result:'每个字段，都能回到原文。', detail:'按字段蓝图提取合同要素。付款条件进入人工复核，保留来源位置与校验结果，再输出结构化数据。', sources:['供应商合同.pdf','合同字段蓝图','字段校验规则'], steps:['匹配文档与字段蓝图','提取关键字段','标记需人工复核项','准备结构化输出'], output:'合同字段复核', owner:'合同审核负责人', evidence:'case-financial-bda-document-automation', kind:'工程方法', conclusion:'复核确认后，输出 JSON / CSV。' },
  { id:'knowledge', label:'工业知识', Icon:Database, title:'工程知识查询', question:'如何查清一个设备的上下游连接，并找到对应图纸？', result:'把图纸关系，带进工程判断。', detail:'关联设备、连接关系与图纸版本。查询结果保留图纸来源，关键连接与操作建议交给工程师确认。', sources:['P&ID 工程图纸','设备主数据','维护文档'], steps:['定位设备与图纸版本','检索上下游连接','关联原始图纸','提交工程师确认'], output:'设备关系复核', owner:'工程负责人', evidence:'case-manufacturing-pid-intelligence', kind:'团队过往实践', conclusion:'工程师确认关键连接与图纸版本。' }
];

function Button({children, href, secondary=false, className='', ...props}) {
  const cls=`button ${secondary?'secondary':'primary'} ${className}`;
  return href ? <a href={href} className={cls} {...props}>{children}</a> : <button className={cls} {...props}>{children}</button>;
}
function WindowBar({title, children}) { return <div className="window-bar"><span className="window-title"><FlowArrow size={14}/>{title}</span><span className="window-tools">{children || <><Clock size={13}/><DotsThree size={18}/></>}</span></div>; }

function ScenarioContext({scenario}) {
  const brief=caseBriefs[scenario.id];
  return <section className="scenario-context" aria-label={`${scenario.label}场景说明`}>
    <div className="scenario-context-heading"><div><span className="eyebrow">{scenario.label} · 从问题到交付</span><h3>{brief.title}</h3></div><a className="inline-link" href={`${site}/${scenario.evidence}`} target="_blank" rel="noreferrer">完整案例 <ArrowUpRight size={15}/></a></div>
    <dl className="scenario-context-grid">{[['工作卡在哪里',brief.problem],['流程交付什么',brief.deliverable],['怎样判断有效',brief.measure]].map(([title,copy])=><div key={title}><dt>{title}</dt><dd>{copy}</dd></div>)}</dl>
    <p className="scenario-attribution">{brief.attribution}</p>
  </section>
}

function Evidence({scenario, onClose}) {
  const dialog = useRef(null);
  useEffect(()=>{const previous=document.activeElement;dialog.current?.querySelector('button')?.focus();return()=>previous?.focus()},[]);
  const trap=e=>{if(e.key!=='Tab')return;const list=[...dialog.current.querySelectorAll('button,a[href]')];const first=list[0],last=list[list.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}};
  return <div className="modal-backdrop" onClick={onClose}><section ref={dialog} onKeyDown={trap} role="dialog" aria-modal="true" aria-labelledby="evidence-title" className="evidence-dialog" onClick={e=>e.stopPropagation()}>
    <button onClick={onClose} aria-label="关闭依据" className="icon-button dialog-close"><X size={21}/></button>
    <span className="eyebrow">CASE CONTEXT</span><h2 id="evidence-title">这段演示，从哪里来？</h2>
    <p>{scenario.detail}</p><div className="source-list">{scenario.sources.map((s,i)=><div key={s}><FileText size={19}/><span>{s}</span><small>依据 {i+1}</small></div>)}</div>
    <p className="small muted">本页使用演示数据说明工作方式。完整案例保留项目背景、方法与验证边界。</p>
    <Button href={`${site}/${scenario.evidence}`} target="_blank" rel="noreferrer">阅读完整案例 <ArrowUpRight size={16}/></Button>
  </section></div>;
}

export function App() {
 const [idx,setIdx]=useState(0),[evidence,setEvidence]=useState(false),[menu,setMenu]=useState(false);
 const scenario=scenarios[idx];
 useEffect(()=>{const esc=e=>{if(e.key==='Escape'){setEvidence(false);setMenu(false)}};window.addEventListener('keydown',esc);return()=>window.removeEventListener('keydown',esc)},[]);
 useEffect(()=>{document.body.style.overflow=evidence?'hidden':'';return()=>{document.body.style.overflow=''}},[evidence]);
 return <><a className="skip-link" href="#main">跳到主要内容</a><div className="announcement"><a href="#cases">从案例里，看见 AI 如何进入业务 <ArrowRight size={13}/></a></div>
  <header><div className="nav-inner"><a className="brand" href="#" aria-label="ForFlow 首页"><img src="/assets/forflow.png" alt="ForFlow 萬維流形"/></a><nav className={menu?'is-open':''} aria-label="主导航"><a href="#workflows" onClick={()=>setMenu(false)}>产品与能力 <CaretDown size={12}/></a><a href="#cases" onClick={()=>setMenu(false)}>案例与实践</a><a href="#approach" onClick={()=>setMenu(false)}>企业服务</a><a href={`${site}/playbook`}>资源</a></nav><Button className="nav-contact" href={`${site}/contact`}>联系团队 <ArrowUpRight size={14}/></Button><button className="menu-button" onClick={()=>setMenu(!menu)} aria-label={menu?'关闭导航':'打开导航'} aria-expanded={menu}>{menu?<X size={23}/>:<List size={23}/>}</button></div></header>
  <main id="main"><section className="hero" aria-labelledby="hero-title"><div className="hero-copy"><a href="#workflows" className="hero-kicker"><span/>企业 AI，从一条流程开始 <CaretRight size={13}/></a><h1 id="hero-title">让 AI 真正<br/>流入业务。</h1><p>连接知识、系统与人的判断。<br/>把反复耗时的工作，变成可运行、可追溯的流程。</p><div className="hero-buttons"><Button secondary href={`${site}/navigator`}>开始场景诊断</Button><Button href="#workflows">探索工作流 <ArrowRight size={15}/></Button></div></div>
  <WorkflowHero onEvidence={()=>{setIdx(0);setEvidence(true)}}/></section>
  <ProductStories scenario={scenario} scenarios={scenarios} idx={idx} setIdx={setIdx} onEvidence={()=>setEvidence(true)} context={<ScenarioContext scenario={scenario}/>}/>
  <section className="cases-section" id="cases"><div className="section-shell"><div className="section-heading"><div><span className="eyebrow">THE WORK, IN PRACTICE</span><h2>具体的问题，<br/><span>具体的工作方式。</span></h2></div><a className="inline-link" href={`${site}/cases`}>浏览全部案例 <ArrowUpRight size={15}/></a></div><div className="case-grid"><a className="case-feature" href={`${site}/case-manufacturing-pid-intelligence`}><div className="case-visual industrial"><div className="case-preview-bar"><FileText size={14}/>P&ID / 工业知识</div><img src="/assets/pid.png" alt="现有 P&ID 案例中的工程图纸"/><div className="diagram-caption"><MagnifyingGlass size={15}/>从设备定位到连接关系<ArrowUpRight size={14}/></div></div><div className="case-meta">工业知识<span>团队过往实践</span></div><h3>让工厂图纸，<br/>成为可查询的运营知识。</h3><p>从静态图纸到设备关系，保留工程师的校验与判断。</p><span className="inline-link">阅读案例 <ArrowUpRight size={15}/></span></a><a className="case-feature" href={`${site}/case-financial-bda-document-automation`}><div className="case-visual document-visual"><div className="paper-preview"><FileText size={22}/><h4>供应商合同</h4><small>字段蓝图示例</small><div><span>合同参与方</span><Check size={13}/></div><div><span>合同期限</span><Check size={13}/></div><div className="paper-review"><span>付款条件</span><small>待复核</small></div><div className="paper-source"><LinkSimple size={12}/>结果关联原文依据</div></div></div><div className="case-meta">文档自动化<span>工程方法</span></div><h3>让文档里的字段，<br/>进入可复核的业务流程。</h3><p>提取、校验与人工复核，让结构化结果继续被使用。</p><span className="inline-link">阅读案例 <ArrowUpRight size={15}/></span></a></div><a className="evaluation-link" href={`${site}/case-agent-evaluation-first`}><span><ShieldCheck size={19}/>企业 Agent 上线前，先建立评估基线。</span><span>查看评估方法 <ArrowUpRight size={15}/></span></a></div></section>
  <section className="approach section-shell" id="approach"><div><span className="eyebrow">START SMALL. BUILD WITH EVIDENCE.</span><h2>从一条流程开始。<br/><span>把结果验证清楚。</span></h2><p>每个阶段都有可以检查的交付物。<br/>业务、技术和一线使用者，共同判断下一步。</p><Button secondary href={`${site}/service-agent-build`}>查看服务与交付 <ArrowRight size={15}/></Button></div><ol>{[['诊断','明确现有流程、负责人和判断口径。交付场景清单、业务基线与试点范围。'],['验证','用企业样本跑通最小流程。交付可操作原型、评估记录与待解决问题。'],['部署','接入系统与权限，设置人工交接。交付运行流程、异常处理和团队使用说明。'],['复评','跟踪真实运行与失败样本。交付复评结果，明确继续改进或扩大范围的依据。']].map(([a,b],i)=><li key={a}><small>0{i+1}</small><div><h3>{a}</h3><p>{b}</p></div><ArrowUpRight size={17}/></li>)}</ol></section>
  <section className="faq-section section-shell" aria-labelledby="faq-heading"><div><span className="eyebrow">BEFORE WE START</span><h2 id="faq-heading">开始之前，<br/><span>先说清楚。</span></h2><p>把业务范围与交付预期对齐，<br/>才能选出值得先做的那条流程。</p></div><div className="faq-list">{[
    ['ForFlow 具体交付什么？','围绕选定的业务流程，交付知识与数据接入、Agent 与工具编排、人工确认节点，以及评估和运行记录。范围以场景诊断为起点，再确定需要集成的系统和验收方式。'],
    ['先从哪种场景开始？','优先选择频繁发生、输入资料可取得、输出能检查、有业务负责人接手的任务。例如合同字段复核、设备资料查询，或一类供应链异常分析。'],
    ['已有系统和数据要怎么接？','先梳理现有数据源、业务定义和访问权限，再按实际系统条件选择接口、文件或知识检索。试点阶段明确哪些步骤由 AI 处理，哪些步骤需要人工确认。'],
    ['怎样知道这次投入是否有效？','开始前保存当前做法的样本和耗时，约定正确性、处理时间、复核量等指标。使用同一组任务评估新流程，并检查失败样本，再决定是否扩展。']
  ].map(([question,answer])=><details key={question}><summary>{question}<CaretDown size={17}/></summary><p>{answer}</p></details>)}</div></section>
  <section className="final-cta"><span className="eyebrow">YOUR NEXT WORKFLOW</span><h2>下一段工作，<br/>从这里开始改变。</h2><p>带上一条高频流程，找到最小可验证的起点。</p><div className="hero-buttons"><Button href={`${site}/navigator`}>开始场景诊断 <ArrowRight size={15}/></Button><Button secondary href={`${site}/contact`}>与团队聊聊</Button></div></section>
  </main><footer><div className="footer-inner"><div><img src="/assets/forflow.png" alt="ForFlow 萬維流形"/><p>AI Flows. Business Grows.</p></div><div className="footer-links"><a href={`${site}/service-agent-build`}>企业服务</a><a href={`${site}/cases`}>案例与实践</a><a href={`${site}/playbook`}>企业 AI 手册</a><a href={`${site}/contact`}>联系我们</a></div></div><div className="footer-bottom"><span>© 2026 ForFlow 萬維流形</span><span>首页设计预览 · 演示数据</span></div></footer>
  {evidence&&<Evidence scenario={scenario} onClose={()=>setEvidence(false)}/>}</>;
}
