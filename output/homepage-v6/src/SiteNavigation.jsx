import React, {useEffect, useRef, useState} from 'react';
import {usePresence} from './ui-motion.js';
import {ArrowRight, ArrowUpRight, CaretDown, Database, FileText, FlowArrow, GitBranch, List, SquaresFour, Stack, TerminalWindow, X} from '@phosphor-icons/react';
const productLinks = [
  ['ForFlow One 工作台','编排工作流、审核内容、管理 AI 资产','#platform',SquaresFour],
  ['业务协同','查清异常原因，明确处理责任','#scenario-0',FlowArrow],
  ['文档处理','提取合同字段，对照原文复核','#scenario-1',FileText],
  ['工程知识','查看设备关系，整理检修事项','#scenario-2',Database],
  ['持续复评','跟进模型、规则与业务的变化','#advantages',GitBranch],
  ['能力资产','管理规则、流程与评估样本的版本','#capabilities',Stack],
  ['ForFlow CLI','从输入到核验，跟进每一步运行','#cli',TerminalWindow],
];
export function SiteNavigation(){
 const [mobile,setMobile]=useState(false),[panel,setPanel]=useState(null),root=useRef(null),productButton=useRef(null),resourceButton=useRef(null);
 const visiblePanel=usePresence(panel),hoverTimer=useRef(null),keyboardNav=useRef(false);
 const cancelHover=()=>clearTimeout(hoverTimer.current);
 const close=()=>{cancelHover();setPanel(null);setMobile(false)};
 const hover=(event,value)=>{if(event.pointerType!=='mouse'||mobile)return;keyboardNav.current=false;cancelHover();hoverTimer.current=setTimeout(()=>setPanel(value),110)};
 const leave=event=>{if(event.pointerType!=='mouse'||mobile||keyboardNav.current)return;cancelHover();hoverTimer.current=setTimeout(()=>setPanel(null),180)};
 const menuKey=(event,value)=>{if(event.key==='ArrowDown'){event.preventDefault();cancelHover();keyboardNav.current=true;setPanel(value);requestAnimationFrame(()=>root.current?.querySelector('.nav-mega a')?.focus())}};
 useEffect(()=>()=>clearTimeout(hoverTimer.current),[]);
 useEffect(()=>{const outside=e=>{if(!root.current?.contains(e.target)){cancelHover();setPanel(null)}};const key=e=>{if(e.key==='Escape'){cancelHover();if(panel)(panel==='product'?productButton:resourceButton).current?.focus();setPanel(null);setMobile(false)}};window.addEventListener('pointerdown',outside);window.addEventListener('keydown',key);return()=>{window.removeEventListener('pointerdown',outside);window.removeEventListener('keydown',key)}},[panel]);
 return <header className="v6-header guided-header" ref={root} onPointerLeave={leave} onPointerEnter={cancelHover} onBlur={event=>{if(!event.currentTarget.contains(event.relatedTarget))setPanel(null)}}><div><a href="#main" className="v6-brand" onClick={close}><img src="/assets/forflow.png" alt="ForFlow 萬維流形"/></a><nav className={mobile?'open':''} aria-label="主导航"><button ref={productButton} className="nav-trigger" onPointerEnter={event=>hover(event,'product')} onKeyDown={event=>menuKey(event,'product')} onClick={()=>{cancelHover();keyboardNav.current=false;setPanel(panel==='product'?null:'product')}} aria-expanded={panel==='product'} aria-controls="product-menu">产品<CaretDown size={12}/></button><a href="#workflows" onClick={close}>业务场景</a><a href="#advantages" onClick={close}>为什么 ForFlow</a><a href="#cases" onClick={close}>案例与实践</a><button ref={resourceButton} className="nav-trigger" onPointerEnter={event=>hover(event,'resources')} onKeyDown={event=>menuKey(event,'resources')} onClick={()=>{cancelHover();keyboardNav.current=false;setPanel(panel==='resources'?null:'resources')}} aria-expanded={panel==='resources'} aria-controls="resource-menu">资源<CaretDown size={12}/></button></nav><a className="v6-button dark nav-demo" href="https://forflow.ai/contact">预约演示<ArrowUpRight size={14}/></a><button className="v6-menu" onClick={()=>{setMobile(!mobile);setPanel(null)}} aria-label="切换导航" aria-expanded={mobile}>{mobile?<X size={23}/>:<List size={23}/>}</button></div>
 {visiblePanel&&<div data-open={Boolean(panel)} inert={!panel} className={`nav-mega ${visiblePanel==='resources'?'resource-mega':''}`} id={visiblePanel==='product'?'product-menu':'resource-menu'}><div className="mega-main"><span className="overline">{visiblePanel==='product'?'FROM CONTEXT TO CAPABILITY':'EXPLORE FORFLOW'}</span><div className="mega-links">{(visiblePanel==='product'?productLinks:[['案例库','从具体工作理解 AI 如何落地','https://forflow.ai/cases',FileText],['方法与实践','业务、工程与评估的工作方法','https://forflow.ai/playbook',Stack],['企业服务','围绕需求组织工程与持续交付','https://forflow.ai/service-agent-build',FlowArrow]]).map(([title,desc,href,Icon])=><a href={href} onClick={close} key={title}><Icon size={25} weight="light"/><span><strong>{title}</strong><small>{desc}</small></span><ArrowUpRight size={12}/></a>)}</div></div><aside className="mega-start"><span className="overline">从这里开始</span><h3>从一项任务开始，<br/>看懂完整处理过程。</h3><a href="#platform" onClick={close}>浏览工作台<ArrowRight size={13}/></a><a href="https://forflow.ai/contact" onClick={close}>和我们聊聊<ArrowUpRight size={13}/></a></aside></div>}
 </header>;
}
