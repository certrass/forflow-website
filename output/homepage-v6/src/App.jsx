import React,{useState,useEffect,useRef} from 'react';
import {ArrowRight,ArrowUpRight,CaretDown,CaretRight,Check,CheckCircle,Circle,Clock,Database,FileText,Files,FlowArrow,GearSix,SquaresFour,ShieldCheck,MagnifyingGlass,Play,Pause,ArrowCounterClockwise,X,List,DotsThree,Sparkle,ChartBar,Users,CalendarBlank,LinkSimple,Stack,CheckSquare,Bell,ListBullets} from '@phosphor-icons/react';
import {CapabilitySection} from './CapabilitySection.jsx';
import {WorkspaceStory} from './WorkspaceStory.jsx';
import {HeroHeadline} from './HeroHeadline.jsx';
import {CliShowcase} from './CliShowcase.jsx';
import {SiteNavigation} from './SiteNavigation.jsx';
import {Advantages} from './Advantages.jsx';
import {ProductDemo} from './ProductDemos.jsx';
import {usePageReveal,useChapterNavigation} from './ui-motion.js';
import {ProductSceneNav} from './ProductSceneNav.jsx';
import {CaseDialog} from './CaseDialog.jsx';
import {CaseLibrary} from './CaseLibrary.jsx';
import {ContactSection} from './ContactSection.jsx';
import {GovernanceSection} from './GovernanceSection.jsx';
import {ConnectedContext} from './ConnectedContext.jsx';
import {ConnectorSection} from './ConnectorSection.jsx';
import {CaseSpotlight} from './CaseSpotlight.jsx';
const site='https://forflow.ai';
const cases=[
 {id:'supply',name:'业务协同',Icon:FlowArrow,headline:'查清异常，推进订单交接。',description:'关联订单与信用记录，由负责人确认放行条件。',link:'case-supply-chain-agentic-decision',title:'供应链异常，如何从发现走向处理？',tag:'团队过往实践',note:'基于团队成员在原组织的供应链实践。',sources:['渠道履行明细','订单状态记录','信用控制规则']},
 {id:'docs',name:'文档处理',Icon:Files,headline:'提取关键条款，逐项对照原文。',description:'提取参与方、期限和付款条件，保留字段规则供同类合同复用。',link:'case-financial-bda-document-automation',title:'合同信息，如何成为可复核的业务字段？',tag:'工程方法',note:'基于现有文档自动化工程方法。',sources:['供应商合同','合同字段蓝图','字段校验规则']},
 {id:'knowledge',name:'工程知识',Icon:Database,headline:'查清设备关系，准备检修清单。',description:'查看图纸中的设备、管线与连接，整理待工程师确认的事项。',link:'case-manufacturing-pid-intelligence',title:'P&ID 图纸，如何变成可查询的设备关系？',tag:'团队过往实践',note:'使用团队成员加入 ForFlow 前的 P&ID 案例插图。',sources:['P&ID 工程图纸','设备主数据','维护资料']}
];
function EngineeringCaseArt(){return <div className="mini-engineering" aria-hidden="true">
 <header><GearSix size={23}/><div><strong>P-101 泵组</strong><small>设备关系</small></div></header>
 <div className="mini-engineering-relations"><div><span>上游储罐<strong>TK-101</strong></span><CaretRight size={12}/></div><div><span>下游阀门<strong>V-102</strong></span><CaretRight size={12}/></div></div>
 <footer><FileText size={13}/><span>图纸依据</span><LinkSimple size={12}/></footer>
 </div>}

const interactionHints=['点击任务，查看原因与负责人。','点击字段，核对原文。','选择设备，加入检修准备。'];

export function App(){
 const [evidence,setEvidence]=useState(null);
 const product=useRef(null);const [active,selectChapter]=useChapterNavigation(product);
 const page=useRef(null);usePageReveal(page);
 useEffect(()=>{
  if(!location.hash)return;
  let cancelled=false,frame;
  const cancel=()=>{cancelled=true};
  const reveal=()=>{if(cancelled)return;document.getElementById(location.hash.slice(1))?.scrollIntoView({block:'start',behavior:'instant'})};
  frame=requestAnimationFrame(reveal);
  document.fonts.ready.then(reveal);
  window.addEventListener('wheel',cancel,{passive:true,once:true});
  window.addEventListener('pointerdown',cancel,{once:true});
  return()=>{cancelled=true;cancelAnimationFrame(frame);window.removeEventListener('wheel',cancel);window.removeEventListener('pointerdown',cancel)};
 },[]);
 useEffect(()=>{const esc=e=>{if(e.key==='Escape')setEvidence(null)};window.addEventListener('keydown',esc);return()=>window.removeEventListener('keydown',esc)},[]);
 return <div className="v6 product-one" ref={page}><a className="skip-link" href="#main">跳到主要内容</a><SiteNavigation/>
 <main id="main">
   <section className="v6-hero"><HeroHeadline/><WorkspaceStory/></section>
   <section className="platform-intro journey-intro v6-container"><span className="overline">业务场景</span><h2>AI 可以接手哪些工作？</h2></section>
   <section className="v6-product v6-container continuous-product" id="workflows" ref={product}><aside className="product-rail"><ProductSceneNav items={cases} active={active} onSelect={selectChapter}/></aside>
   <div className="continuous-main">{cases.map((item,i)=><article className="scenario-section" id={`scenario-${i}`} data-scene={i} key={item.id}><div className="product-lead"><div className="scenario-title"><span className="scenario-kicker">{item.name}</span><h3>{item.headline.split("，")[0]}，<span>{item.headline.split("，")[1]}</span></h3></div><p className="scenario-description">{item.description}</p></div><div className={`v6-product-stage product-${item.id}`}><ProductDemo index={i} onEvidence={()=>setEvidence(item)}/><div className="interaction-hint"><Play size={12}/><span>{interactionHints[i]}</span></div></div><div className="case-strip"><div><small>{item.note}</small></div><button onClick={()=>setEvidence(item)} aria-haspopup="dialog">案例背景<ArrowUpRight size={15}/></button></div></article>)}</div></section>
   <ConnectedContext/>
   <Advantages/>
   <CapabilitySection/>
   <GovernanceSection/>
   <ConnectorSection/>
   <CliShowcase/>
   <section className="v6-cases v6-container" id="cases"><div className="v6-section-heading"><div><span className="overline"><FileText size={14}/>案例与实践</span><h2>业务中的 AI 实践。</h2></div><a href="#case-library">浏览案例库<ArrowRight size={15}/></a></div><CaseSpotlight scenes={cases} onRead={setEvidence}/><CaseLibrary onRead={setEvidence} scenes={cases}/><p className="case-context-note">案例库包含团队过往实践与工程方法，具体背景见各案例说明。</p></section>
   <ContactSection/>
 </main><footer className="v6-footer v6-container"><div><img src="/assets/forflow.png" alt="ForFlow 萬維流形"/><span>AI Flows. Business Grows.</span></div><div><a href="#platform">产品展示</a><a href="#context">业务流程</a><a href="#connectors">连接器</a><a href="/ai-governance.html">AI 评估与治理</a><a href={`${site}/service-agent-build`}>企业服务</a><a href={`${site}/playbook`}>资源</a><a href="#contact">联系我们</a></div><small>© 2026 ForFlow 萬維流形</small></footer>{evidence&&<CaseDialog item={evidence} onClose={()=>setEvidence(null)} onNext={()=>setEvidence(cases[(cases.findIndex(c=>c.id===evidence.id)+1)%cases.length])}/>}</div>;
}
