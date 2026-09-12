import React from 'react';
import {PersonAvatar} from './HumanDetails.jsx';
import {Check,ClockCounterClockwise,FileText,ArrowRight} from '@phosphor-icons/react';

export function DetailTabs({value,onChange,items,label}) {
  return <div className="detail-tabs" role="group" aria-label={label}>{items.map(([id,title,count])=><button key={id} aria-pressed={value===id} onClick={()=>onChange(id)}>{title}{count!==undefined&&<span>{count}</span>}</button>)}</div>;
}

export function ReviewHistory({items,onSelect,empty='先核对一个字段，确认后会在这里留下记录。',onStart,label='本次复核'}) {
  return <div className="review-history"><div className="review-history-heading"><ClockCounterClockwise size={15}/><span>{label}</span></div>{items.length?items.map(item=><button key={item.id} disabled={!onSelect} onClick={()=>onSelect?.(item.id)} title={onSelect?'回到对应原文与字段':undefined}><>{item.person?<PersonAvatar person={item.person} size={25} checked={!item.pending}/>:<span className={`review-history-check ${item.pending?'is-pending':''}`}>{item.pending?<ClockCounterClockwise size={12}/>:<Check size={12}/>}</span>}</><span><strong>{item.title}</strong><small>{item.description}</small>{item.actor&&<small className="review-history-actor">{item.actor}</small>}</span>{onSelect&&<ArrowRight size={13}/>}</button>):<div className="review-history-empty"><FileText size={25} weight="light"/><strong>还没有复核记录</strong><p>{empty}</p>{onStart&&<button onClick={onStart}>开始核对字段<ArrowRight size={12}/></button>}</div>}</div>;
}
