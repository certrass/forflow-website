import React from 'react';
import {ArrowRight,ArrowUpRight,Check,CheckCircle,Clock,FileText,PaperPlaneTilt,Sparkle,Users} from '@phosphor-icons/react';
import {recordFiles,owners} from './q2q-records.js';
import {Avatar} from './WorkspaceUI.jsx';

import {analysisFor} from './q2q-analysis.js';
export {analysisFor} from './q2q-analysis.js';

export function IntelligencePanel({record:r,stage='ready',onFile,onApply}){
 const a=analysisFor(r),ready=stage==='ready';
 const stages=['sources','align','compare','ready'];
 const progress=stages.indexOf(stage);
 const files=recordFiles(r),references=files.filter(f=>r.originalKind==='fee'?['contract','invoice'].includes(f.id):['waybill','receipt'].includes(f.id));
 return <section className="wq-ai-panel" aria-label="AI 核验结果">
  <header><span className="wq-ai-symbol"><Sparkle size={19} weight="fill"/></span><div><strong>Q2Q AI</strong><small>{ready?'核验完成 · 依据已关联':'正在核对当前运输记录'}</small></div><span className={`wq-ai-state ${ready?'':'working'}`}>{ready?<Check size={12}/>:<i/>}{ready?'已完成':'核验中'}</span></header>
  <div className="wq-ai-checks" data-tour="ai-checks">{[['关联业务材料',`${files.length} 份材料`],['对齐单号与关键字段',r.id],['检查跨单据一致性',r.rule]].map(([label,meta],i)=><div key={label} className={progress>i?'done':progress===i?'current':'waiting'}>{progress>i?<CheckCircle size={14}/>:<span className="wq-check-dot"/>}<span>{label}</span><small>{meta}</small></div>)}</div>
  {ready?<div className="wq-ai-result" data-tour="ai-result"><span className="wq-section-label">核验结论</span><h4>{a.title}</h4><p>{a.finding}</p><div className="wq-ai-references">{references.map((f,i)=><button key={f.id} data-tour={f.id==='receipt'?'ai-source':undefined} onClick={()=>onFile(f)}><span>{i+1}</span><FileText size={13}/>{f.name}<ArrowUpRight size={12}/></button>)}</div><div className="wq-ai-boundary"><span>仍需确认</span><p>{a.caution}</p></div><div className="wq-ai-next"><span><Sparkle size={13}/>处理建议</span><p>{a.action}</p></div><button className="wq-primary" data-tour="ai-draft" disabled={r.reviewed||r.originalKind==='missing'} onClick={()=>onApply(a.draft)}>{r.reviewed?'复核已确认':r.originalKind==='missing'?'待补材料后复核':'生成复核意见'}<ArrowRight size={14}/></button><small className="wq-ai-human">由业务复核人编辑并确认</small></div>:<div className="wq-ai-working"><span/><span/><span/><p>{stage==='sources'?'读取运单、签收与合同记录…':stage==='align'?'对齐运输单号、发运与实收字段…':'检查数量差异，定位对应材料…'}</p></div>}
 </section>
}

export function CollaborationPanel({record:r,draft,onDraft,onCreate,onSend}){
 const a=analysisFor(r),task=r.followUp,owner=owners.find(o=>o.id===(task?.owner||a.owner));
 return <section className="wq-team-panel" aria-label="记录协作">
  <header><Users size={17}/><strong>围绕这条记录协作</strong><span>3 位成员</span></header>
  <div className="wq-team-people"><Avatar id="review" small/><Avatar id="transport" small/><Avatar id="finance" small/><span>业务 · 运输 · 结算</span></div>
  <div className="wq-handoff-card" data-tour="team-task"><div><span><CheckCircle size={14}/>{r.reviewed?'人工复核已确认':'关联当前核验记录'}</span><small>{task?(task.acknowledged?'处理中':'待接手'):'待分派'}</small></div><h4>{a.task}</h4><p>{a.action}</p><dl><dt>负责人</dt><dd><Avatar id={owner.id} small/>{owner.name}</dd><dt>关联依据</dt><dd><FileText size={12}/>{r.files} 份材料 · {r.id}</dd></dl>{!task?<button data-tour="team-assign" className="wq-primary" onClick={onCreate}>创建跟进任务<ArrowRight size={13}/></button>:<footer><Check size={12}/>任务与复核意见已关联<Clock size={12}/>{task.acknowledged?'今天 16:00 前反馈':'等待负责人接手'}</footer>}</div>
  <div className="wq-thread-heading">讨论<span>{task?.comments?.length||0} 条回复</span></div>
  {task?.comments?.length?<div className="wq-team-thread" data-tour="team-reply">{task.comments.map(c=><article key={c.id}><Avatar id={c.owner} small/><div><header><strong>{owners.find(o=>o.id===c.owner).name}</strong><time>刚刚</time></header><p>{c.owner==='review'&&<span className="wq-mention">@{owner.name} </span>}{c.text}</p></div></article>)}</div>:<p className="wq-thread-empty">补充处理要求，相关材料随记录一起保留。</p>}
  <form className="wq-team-compose" onSubmit={e=>{e.preventDefault();if(draft.trim())onSend(draft.trim())}}><label htmlFor={`team-note-${r.id}`}>回复并提醒负责人</label><textarea data-tour="team-note" id={`team-note-${r.id}`} value={draft} onChange={e=>onDraft(e.target.value)} placeholder={task?`@${owner.name} 补充处理要求…`:'先创建跟进任务…'} disabled={!task} maxLength={240}/><footer><span><Avatar id="review" small/>业务复核人</span><button data-tour="team-send" disabled={!task||!draft.trim()} type="submit" aria-label="发送协作回复"><PaperPlaneTilt size={14}/>发送</button></footer></form>
 </section>
}

export function RecordActivity({record:r,title,count}){return <div className="wq-activity">
 <div><span className="wq-activity-dot"><FileText size={12}/></span><strong>材料已关联</strong><time>今天 09:12</time><p>运单、合同与当前可用的业务凭证已归集。</p><small>{count} 份材料 · 来源版本已保留</small></div>
 <div><span className="wq-activity-dot"><CheckCircle size={12}/></span><strong>跨单据核验完成</strong><time>今天 09:14</time><p>{title}。</p><small>跨单据一致性 · {r.rule}</small></div>
 {r.aiDraft&&<div><span className="wq-activity-dot"><Sparkle size={12}/></span><strong>AI 生成复核建议</strong><time>本次核验</time><p>{analysisFor(r).finding}</p><small>材料引用与处理建议已保留</small></div>}
 {r.requested&&<div><span className="wq-activity-dot"><Users size={12}/></span><strong>补证任务已建立</strong><time>刚刚</time><p>补充有效签收回执，并关联当前运单。</p><small>负责人 · 运输负责人</small></div>}
 {r.reviewed&&<div className="review-complete"><span className="wq-activity-dot"><Check size={12}/></span><strong>复核已记录</strong><time>{r.note?'刚刚':'今天 09:30'}</time><p>{r.note||'字段与关联材料已完成核对。'}</p><small>复核人 · {owners.find(o=>o.id===(r.reviewedBy||r.owner)).name}</small></div>}
 {r.followUp&&<div data-tour="activity-handoff"><span className="wq-activity-dot"><Users size={12}/></span><strong>{r.followUp.acknowledged?'负责人已接手跟进':'跟进任务已分派'}</strong><time>刚刚</time><p>{analysisFor(r).task} · {owners.find(o=>o.id===r.followUp.owner).name}</p><small>{r.followUp.acknowledged?'处理中 · 今天 16:00 前反馈':'等待负责人接手'} · {r.followUp.comments.length} 条回复</small></div>}
 </div>}
