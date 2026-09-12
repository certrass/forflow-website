import React,{useEffect,useId,useRef,useState} from 'react';
import {CaretDown,Check,LinkSimple,X} from '@phosphor-icons/react';

const people={
 credit:{image:'credit',role:'信用控制组',task:'核对付款情况与放行条件'},
 operations:{image:'operations',role:'履行团队',task:'接收复核结果，推进订单处理'},
 channel:{image:'operations',role:'渠道运营组',task:'补全收货信息，跟进履行进展'},
 procurement:{image:'procurement',role:'采购团队',task:'对照合同原文，逐项确认字段'},
 engineering:{image:'engineering',role:'工程师',task:'核对图纸版本、设备连接与隔离范围'},
};
export function personForOwner(owner){return owner==='信用控制组'?'credit':owner==='采购团队'?'procurement':owner==='履行团队'?'operations':'channel'}

export function PersonAvatar({person='procurement',size=26,checked=false}){
 const entry=people[person]||people.procurement;
 return <span className="person-avatar" style={{'--avatar-size':`${size}px`}} aria-hidden="true"><img src={`/assets/people/${entry.image}-v1.png`} alt="" width="512" height="512" loading="lazy" decoding="async"/>{checked&&<span className="person-check"><Check size={8} weight="bold"/></span>}</span>;
}

export function Collaborators({members,label='协作分工'}){
 const [open,setOpen]=useState(false),ref=useRef(null),trigger=useRef(null),id=useId();
 useEffect(()=>{
  if(!open)return;
  const outside=event=>{if(!ref.current?.contains(event.target))setOpen(false)};
  document.addEventListener('pointerdown',outside,true);
  document.addEventListener('click',outside,true);
  return()=>{document.removeEventListener('pointerdown',outside,true);document.removeEventListener('click',outside,true)};
 },[open]);
 const close=()=>{setOpen(false);trigger.current?.focus({preventScroll:true})};
 return <span className="collaborators" ref={ref} onKeyDown={event=>{if(open&&event.key==='Escape'){event.stopPropagation();close()}}}>
  <button ref={trigger} className="collaborator-trigger" aria-expanded={open} aria-controls={id} aria-label={`查看${label}`} onClick={()=>setOpen(v=>!v)}><span className="person-stack">{members.map(person=><PersonAvatar key={person} person={person}/>)}</span><span>{label}</span><CaretDown size={10}/></button>
  {open&&<span className="collaborator-popover" id={id} role="group" aria-label={label}><span className="collaborator-heading">参与这项工作<button aria-label="收起协作分工" onClick={close}><X size={12}/></button></span>{members.map(person=><span className="collaborator-row" key={person}><PersonAvatar person={person} size={34}/><span><strong>{people[person].role}</strong><small>{people[person].task}</small></span></span>)}<span className="collaborator-foot">AI 整理依据，负责人确认下一步。</span></span>}
 </span>;
}

export function ReviewMark({done=false}){
 return <span className={`human-review-mark ${done?'is-done':''}`} key={done?'done':'review'}><span className="review-anchor-icon">{done?<Check size={10}/>:<LinkSimple size={10}/>}</span><span>{done?'已核对':'原文已定位'}</span></span>;
}

export function HandoffReceipt({person='operations',title,description}){
 return <div className="human-receipt" role="status"><PersonAvatar person={person} size={28} checked/><span><strong>{title}</strong><small>{description}</small></span></div>;
}
