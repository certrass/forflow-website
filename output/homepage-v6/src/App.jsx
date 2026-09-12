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
const site='https://forflow.ai';
const cases=[
 {id:'supply',name:'业务协同',Icon:FlowArrow,headline:'查清异常原因，把处理交给对的人。',description:'将订单状态、信用记录和处理条件放在一起，让负责人核对后推进交接。',link:'case-supply-chain-agentic-decision',title:'供应链异常，如何从发现走向处理？',tag:'团队过往实践',note:'基于团队成员在原组织的供应链实践。',sources:['渠道履行明细','订单状态记录','信用控制规则']},
 {id:'docs',name:'文档处理',Icon:Files,headline:'提取关键条款，逐项对照原文。',description:'把合同中的参与方、期限和付款条件整理成业务字段；点击结果，即可定位对应条款。',link:'case-financial-bda-document-automation',title:'合同信息，如何成为可复核的业务字段？',tag:'工程方法',note:'基于现有文档自动化工程方法。',sources:['供应商合同','合同字段蓝图','字段校验规则']},
 {id:'knowledge',name:'工程知识',Icon:Database,headline:'从设备出发，查清上下游关系。',description:'关联原始图纸、设备连接与检修事项，让工程师带着依据开展复核。',link:'case-manufacturing-pid-intelligence',title:'P&ID 图纸，如何变成可查询的设备关系？',tag:'团队过往实践',note:'使用团队成员加入 ForFlow 前的 P&ID 案例插图。',sources:['P&ID 工程图纸','设备主数据','维护资料']}
];
function Evidence({item,onClose}){const ref=useRef(null);useEffect(()=>{const prev=document.activeElement;ref.current?.querySelector('button')?.focus();return()=>prev?.focus({preventScroll:true})},[]);const trap=e=>{if(e.key==='Escape'){e.stopPropagation();onClose();return}if(e.key!=='Tab')return;const a=[...ref.current.querySelectorAll('button,a')];if(e.shiftKey&&document.activeElement===a[0]){e.preventDefault();a.at(-1).focus()}else if(!e.shiftKey&&document.activeElement===a.at(-1)){e.preventDefault();a[0].focus()}};return <div className="v6-modal" onClick={onClose}><section ref={ref} role="dialog" aria-modal="true" data-case-dialog="true" aria-labelledby="case-context-title" onKeyDown={trap} onClick={e=>e.stopPropagation()}><button className="modal-x" onClick={onClose} aria-label="关闭案例依据"><X size={20}/></button><span className="overline">CASE CONTEXT</span><h2 id="case-context-title">{item.title}</h2><p>{item.note}</p><div>{item.sources.map(s=><span className="modal-source" key={s}><FileText size={17}/>{s}</span>)}</div><a className="v6-button dark" href={`${site}/${item.link}`} target="_blank" rel="noreferrer">阅读完整案例<ArrowUpRight size={15}/></a></section></div>}

function EngineeringCaseArt(){return <div className="mini-engineering" aria-hidden="true">
 <header><GearSix size={23}/><div><strong>P-101 泵组</strong><small>设备关系</small></div></header>
 <div className="mini-engineering-relations"><div><span>上游储罐<strong>TK-101</strong></span><CaretRight size={12}/></div><div><span>下游阀门<strong>V-102</strong></span><CaretRight size={12}/></div></div>
 <footer><FileText size={13}/><span>图纸依据</span><LinkSimple size={12}/></footer>
 </div>}

const sceneBenefits = [
  [['找出订单卡在哪里','将履行明细与信用控制记录对应起来，找到影响订单处理的具体条件。',MagnifyingGlass],['交接时，把依据一起带上','负责人确认处理条件后，将复核结果和关联材料一并交给后续团队。',Users]],
  [['每个字段，都能找到出处','提取值与原文条款并排呈现，哪些已经确认、哪些还需复核，一眼可见。',FileText],['同类合同，沿用同一套标准','保留字段定义与校验规则，后续处理同类文档时继续使用。',Stack]],
  [['把设备关系看清楚','围绕泵组查看上下游连接，把相关管线、阀门和设备组织在一张关系图里。',Database],['让检修准备有据可查','将设备与待核对事项加入准备清单，由工程师确认图纸版本和现场情况。',ShieldCheck]],
];
const interactionHints=['打开一笔异常，查看原因、关联依据和处理负责人。','选择「付款条件」，对照合同原文完成复核。','展开设备关系，选择关联对象，再加入检修准备。'];

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
 useEffect(()=>{if(!evidence)return;const previous=document.body.style.overflow;document.body.style.overflow='hidden';return()=>{document.body.style.overflow=previous}},[evidence]);
 return <div className="v6" ref={page}><a className="skip-link" href="#main">跳到主要内容</a><SiteNavigation/>
 <main id="main">
   <section className="v6-hero"><HeroHeadline/><WorkspaceStory/></section>
   <section className="platform-intro journey-intro v6-container"><span className="overline">THE PRODUCT, AT WORK</span><h2>从信息到行动，<br/><span>看见工作的完整过程。</span></h2><p>查清一笔异常、复核一份合同、梳理一组设备关系。<br/>看 AI 如何处理信息，团队如何据此推进工作。</p></section>
   <section className="v6-product v6-container continuous-product" id="workflows" ref={product}><aside className="product-rail"><span className="overline">PRODUCT IN ACTION</span><ProductSceneNav items={cases} active={active} onSelect={selectChapter}/><p className="rail-note">选择一个场景，<br/>查看具体操作过程。</p><a href="#advantages">为什么 ForFlow<ArrowRight size={13}/></a></aside>
   <div className="continuous-main">{cases.map((item,i)=><article className="scenario-section" id={`scenario-${i}`} data-scene={i} key={item.id}><div className="product-lead"><div className="scenario-title"><span className="scenario-kicker"><span>0{i+1}</span>{item.name}</span><h3>{item.headline.split("，")[0]}，<br/>{item.headline.split("，")[1]}</h3></div><p className="scenario-description">{item.description}</p></div><div className={`v6-product-stage product-${item.id}`}><ProductDemo index={i} onEvidence={()=>setEvidence(item)}/><div className="interaction-hint"><Play size={12}/><span>{interactionHints[i]}</span><small>点击界面体验</small></div></div><div className="product-benefits">{sceneBenefits[i].map(([title,body,Icon])=><div key={title}><Icon size={20}/><h4>{title}</h4><p>{body}</p></div>)}</div><div className="case-strip"><div><span className="overline">{item.tag}</span><h4>{item.title}</h4><small>{item.note}</small></div><a href={`${site}/${item.link}`} target="_blank" rel="noreferrer">阅读案例<ArrowUpRight size={15}/></a></div><div className="scenario-next"><span>0{i+1} / 03</span><a href={i<2?`#scenario-${i+1}`:'#cli'}>{i<2?`接着看${cases[i+1].name}`:'查看 CLI 核验流程'}<ArrowRight size={13}/></a></div></article>)}</div></section>
   <CliShowcase/>
   <Advantages/>
   <CapabilitySection/>
   <section className="v6-cases v6-container" id="cases"><div className="v6-section-heading"><div><span className="overline">THE WORK, IN PRACTICE</span><h2>从具体案例，<br/><span>看懂落地方法。</span></h2></div><a href={`${site}/cases`}>探索案例库<ArrowUpRight size={15}/></a></div><div className="v6-case-grid">{cases.map((c,i)=><a className="v6-case-card" key={c.id} href={`${site}/${c.link}`}><div className={`case-art case-art-${i}`}>{i===2?<EngineeringCaseArt/>:i===1?<div className="mini-document"><FileText size={23}/><strong>供应商合同</strong><span>合同主体<Check size={12}/></span><span>付款条件<span className="state-tag amber">待复核</span></span><span>原文依据<LinkSimple size={12}/></span></div>:<div className="mini-work"><div><i className="dot dot-0"/>发现异常<Check size={12}/></div><div><i className="dot dot-1"/>关联依据<Check size={12}/></div><div><i className="dot dot-stage-2"/>业务负责人复核<CaretRight size={12}/></div></div>}</div><div className="v6-case-meta">{c.name}<span>{c.tag}</span></div><h3>{c.title}</h3><span className="case-read">阅读案例<ArrowUpRight size={15}/></span></a>)}</div><p className="case-context-note">案例库包含团队过往实践与工程方法，具体背景见各案例说明。</p></section>
   <section className="v6-cta"><span className="overline">YOUR BUSINESS. WITH AI.</span><h2>下一项业务改进，<br/>从这里开始。</h2><p>告诉我们你的业务目标、现有流程和遇到的问题。<br/>一起明确 AI 的切入点，以及如何验证结果。</p><div className="v6-actions"><a className="v6-button dark" href={`${site}/contact`}>讨论业务场景<ArrowRight size={15}/></a><a className="v6-button light" href={`${site}/cases`}>先看看案例</a></div></section>
 </main><footer className="v6-footer v6-container"><div><img src="/assets/forflow.png" alt="ForFlow 萬維流形"/><span>AI Flows. Business Grows.</span></div><div><a href="#platform">产品展示</a><a href="#advantages">为什么 ForFlow</a><a href={`${site}/service-agent-build`}>企业服务</a><a href={`${site}/playbook`}>资源</a><a href={`${site}/contact`}>联系我们</a></div><small>© 2026 ForFlow 萬維流形</small></footer>{evidence&&<Evidence item={evidence} onClose={()=>setEvidence(null)}/>}</div>;
}
