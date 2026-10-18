import React, {useRef, useState} from 'react';
import {ArrowRight, ArrowUpRight, Buildings, FileText, FlowArrow, GearSix} from '@phosphor-icons/react';
import {bPillarCase} from './CaseLibrary.jsx';
const presentations=[
 {id:'bpillar',label:'汽车 B 柱',Icon:Buildings,kicker:'汽车工程 · 知识与风险追溯',title:'追查 B 柱变更的风险依据。',body:'关联材料、工艺、失效机理与变更记录，支持工程风险复核。',image:'automotive-dfmea-bpillar-hero.webp',alt:'汽车 B 柱结构件与工程知识的案例配图',note:'团队过往实践与工程方法'},
 {id:'supply',label:'供应链协同',Icon:FlowArrow,kicker:'供应链 · 异常分析与交接',title:'从订单异常到业务交接。',body:'关联履行明细、订单状态与信用控制条件，形成带依据、处理条件和责任人的异常分析。',image:'supply-chain-agentic-decision-hero.webp',alt:'供应链运营人员分析业务信息的案例配图',note:'团队成员在原组织的实践'},
 {id:'docs',label:'合同处理',Icon:FileText,kicker:'文档自动化 · 字段提取与复核',title:'将合同条款转为业务字段。',body:'将参与方、付款条件和关键义务逐项提取，与原文保持对应，交给采购与法务人员复核。',image:'financial-bda-document-automation-hero.webp',alt:'文档审核与结构化信息的案例配图',note:'ForFlow 工程方法'},
 {id:'knowledge',label:'工程知识',Icon:GearSix,kicker:'工业工程 · 图纸与设备关系',title:'从图纸查询设备关系。',body:'把图纸中的设备、阀门和管线组织为可查询的关系，支持工程团队追溯来源与准备检修。',image:'cover-manufacturing-pid.webp',alt:'P&ID 图纸与工厂设备的案例配图',note:'团队成员加入 ForFlow 前的实践'},
];
export function CaseSpotlight({scenes,onRead}){
 const [active,setActive]=useState(0),item=presentations[active];
 const tabs=useRef([]);
 const open=()=>onRead(item.id==='bpillar'?bPillarCase:scenes.find(s=>s.id===item.id));
 const selectKey=(event,index)=>{
  const count=presentations.length;
  const next={ArrowRight:(index+1)%count,ArrowLeft:(index+count-1)%count,Home:0,End:count-1}[event.key];
  if(next===undefined)return;
  event.preventDefault();
  setActive(next);
  tabs.current[next]?.focus({preventScroll:true});
 };
 return <div className="case-spotlight">
  <div className="case-spotlight-tabs" role="tablist" aria-label="重点案例">
   {presentations.map((entry,index)=><button
    ref={node=>{tabs.current[index]=node;}}
    id={`spotlight-tab-${entry.id}`} key={entry.id} role="tab"
    aria-selected={active===index} aria-controls="spotlight-panel"
    tabIndex={active===index?0:-1} onClick={()=>setActive(index)} onKeyDown={event=>selectKey(event,index)}
   ><entry.Icon size={21} weight="light"/><span>{entry.label}</span></button>)}
  </div>
  <div className="case-spotlight-panel" id="spotlight-panel" role="tabpanel" aria-labelledby={`spotlight-tab-${item.id}`}>
   <div className="case-spotlight-copy" key={item.id}>
    <span>{item.kicker}</span><h3>{item.title}</h3><p>{item.body}</p>
    <button className="v6-button dark" onClick={open} aria-haspopup="dialog">查看案例<ArrowUpRight size={16}/></button>
    <small>{item.note}</small>
   </div>
   <button className="case-spotlight-image" onClick={open} aria-label={`查看${item.label}案例`} tabIndex={-1}>
    <img src={`/assets/cases/${item.image}`} width="1672" height="941" loading="lazy" alt={item.alt}/>
    <span><ArrowUpRight size={18}/></span>
   </button>
  </div>

 </div>;
}
