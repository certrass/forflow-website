import React, {useRef, useState} from 'react';
import {ArrowLeft, ArrowRight, BookOpen, Check, Database, FileText, FolderSimple, Graph, LinkSimple, Pause, Play, Users} from '@phosphor-icons/react';
import {usePlaybackClock} from './usePlaybackClock.js';
import {ShowcaseViewport} from './ShowcaseViewport.jsx';

const chapterLength = 9000;
const moments = [
 {name:'找齐相关资料', body:'从 ERP、合同库和知识库关联本次续约资料。'},
 {name:'列出待核对事项', body:'核对合作安排与续约条款，标出待确认事项。'},
 {name:'交给负责人确认', body:'将材料和复核清单交给采购负责人。'},
];
const sources = [
 {Icon:Database, name:'供应商档案', origin:'ERP 系统', id:'supplier', title:'供应商档案', subtitle:'供应商主数据', fields:[['负责团队','采购团队'],['业务状态','待复核']], note:'通过供应商编号，关联合同与续约任务。'},
 {Icon:FileText, name:'供应商合同', origin:'合同库', id:'contract', title:'供应商合作合同', subtitle:'合同原文', note:'当前续约沿用这一版合同，条款调整由负责人复核。'},
 {Icon:BookOpen, name:'续约规则', origin:'知识库', id:'第 4.2 条', title:'供应商续约规则', subtitle:'采购制度 / 第 4.2 条', quote:'合同到期前 30 天，发起续约复核。', note:'核对履约记录，关联合同原文。由业务负责人确认下一步。'},
];
const detailSections = [{label:'关联资料',target:'.renewal-source-list'}, {label:'当前内容',target:'.renewal-detail'}];

function SourceDetail({source, canReturn, onReturn}) {
 const item = sources[source];
 return <div className="renewal-source-detail">
  <div className="renewal-detail-eyebrow">{canReturn?<button onClick={onReturn}><ArrowLeft size={12}/>返回当前步骤</button>:<span>已关联的业务资料</span>}</div>
  <div className="renewal-document"><span className="renewal-document-icon"><item.Icon size={22} weight="light"/></span><small>{item.subtitle}</small><h4>{item.title}</h4>
   {item.fields?<dl>{item.fields.map(([label,value])=><div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl>:item.quote&&<blockquote>{item.quote}</blockquote>}
   <p>{item.note}</p><footer><item.Icon size={12}/>{item.origin}</footer>
  </div>
 </div>;
}

function RenewalWorkspace({active, film, select}) {
 const detail = useRef(null);
 const [source, setSource] = useState(1);
 const [drilldownRevision, setDrilldownRevision] = useState(null);
 const sourceOpen = drilldownRevision === film.revision;
 const [selection, setSelection] = useState(0);
 const viewingSource = active === 0 || sourceOpen;
 const focusDetail = () => requestAnimationFrame(()=>detail.current?.focus({preventScroll:true}));
 const openSource = index => {film.pause();setSource(index);setDrilldownRevision(film.revision);setSelection(v=>v+1);focusDetail();};
 const changeStep = index => {setDrilldownRevision(null);select(index);};
 const returnToStep = () => {film.pause();setDrilldownRevision(null);setSelection(v=>v+1);focusDetail();};
 return <ShowcaseViewport label="ForFlow One · 供应商续约" width={640} onExpand={film.pause} focusTarget=".renewal-detail" focusVersion={`${active}-${source}-${selection}`} detailSections={detailSections}>
  <div className="context-field renewal-workspace" data-playing={film.playing} data-step={active}>
   <header className="renewal-appbar"><span><Graph size={16}/><strong>ForFlow One</strong><i/>采购工作台</span></header>
   <div className="renewal-record-heading"><div><small>采购 / 续约任务</small><h3>供应商续约</h3></div><span className={`renewal-status status-${active}`}><i/>{['资料已关联','待确认续约条件','待负责人复核'][active]}</span></div>
   <div className="renewal-body">
    <aside className="renewal-source-list" aria-label="续约关联资料"><div><span>关联资料</span><small>03</small></div>{sources.map((item,i)=><button key={item.id} onClick={()=>openSource(i)} aria-pressed={viewingSource && source===i}><item.Icon size={17}/><span><strong>{item.name}</strong><small>{item.origin}</small></span><ArrowRight size={11}/></button>)}</aside>
    <section className="renewal-detail" ref={detail} tabIndex={-1} aria-label={viewingSource?sources[source].title:active===1?'续约复核清单':'采购审批待办'}>
     {viewingSource?<SourceDetail source={source} canReturn={active!==0} onReturn={returnToStep}/>:active===1?<div className="renewal-review">
      <div className="renewal-detail-eyebrow"><span>资料与待核对事项</span><span>2 项资料已关联 · 决策待确认</span></div><h4>资料已找齐，续约安排待确认。</h4>
      <div className="renewal-check"><Check size={15}/><div><strong>供应商与合同已关联</strong></div><button onClick={()=>openSource(1)}>查看合同<ArrowRight size={11}/></button></div>
      <div className="renewal-check"><Check size={15}/><div><strong>已找到续约规则</strong><p>合同到期前 30 天，发起续约复核。</p></div><button onClick={()=>openSource(2)}>查看规则<ArrowRight size={11}/></button></div>
      <div className="renewal-open-question"><span>待人工确认</span><strong>是否继续合作，续约条款是否需要调整？</strong><p>整理为审批待办，由采购负责人确认。</p></div>
     </div>:<div className="renewal-handoff">
      <div className="renewal-detail-eyebrow"><span>审批待办</span><span>待处理</span></div><h4>确认供应商续约安排</h4><div className="renewal-assignee"><span>采</span><div><strong>采购负责人</strong><small>负责确认合作安排与续约条款</small></div><span>待复核</span></div>
      <div className="renewal-task-items"><span>本次需要确认</span><p><i/>是否继续与该供应商合作</p><p><i/>合同条款是否需要调整</p></div>
      <div className="renewal-attachments"><span><FolderSimple size={15}/>复核清单与 3 份材料已随附</span><button onClick={()=>openSource(1)}>查看材料<ArrowRight size={12}/></button></div><p className="renewal-handoff-note">接手后可直接查看合同和规则，无需重新收集。</p>
     </div>}
    </section>
   </div>
   <footer className="renewal-footer"><span><i/>{['已关联 3 份资料，保留来源与版本','资料已关联，合作安排与条款仍待确认','由采购负责人确认是否续约'][active]}</span><button onClick={()=>viewingSource&&active!==0?returnToStep():changeStep(active===2?0:active+1)}>{viewingSource&&active!==0?'返回当前步骤':['列出待核对事项','整理审批材料','重新查看流程'][active]}<ArrowRight size={13}/></button></footer>
  </div>
 </ShowcaseViewport>;
}

export function ConnectedContext(){
 const stage=useRef(null),film=usePlaybackClock(stage,chapterLength*3,{reducedEnd:false});
 const active=Math.min(2,Math.floor(film.time/chapterLength));
 const select=index=>film.seek(index*chapterLength,false);
 function keySelect(e,i){let next;if(e.key==='ArrowDown'||e.key==='ArrowRight')next=(i+1)%3;if(e.key==='ArrowUp'||e.key==='ArrowLeft')next=(i+2)%3;if(e.key==='Home')next=0;if(e.key==='End')next=2;if(next===undefined)return;e.preventDefault();select(next);e.currentTarget.parentElement.querySelectorAll('[role=tab]')[next].focus();}
 return <section className="connected-context v6-container" id="context">
  <header className="context-heading"><span className="overline"><Graph size={15}/>业务流程</span><h2>资料与待办，<br/><span>一起交接。</span></h2><div><p>关联合同、业务记录和规则，交给负责人复核。</p><a href="#connectors">查看连接器<ArrowRight size={15}/></a></div></header>
  <div className="context-story" ref={stage} data-context-phase={active} data-playing={film.playing}>
   <div className="context-story-copy"><h3>供应商续约</h3><div className="context-moments" role="tablist" aria-label="供应商续约的工作过程" aria-orientation="vertical">{moments.map((m,i)=><button role="tab" key={m.name} aria-selected={active===i} aria-controls="context-stage" id={`context-tab-${i}`} tabIndex={active===i?0:-1} onKeyDown={e=>keySelect(e,i)} onClick={()=>select(i)}><strong><small>0{i+1}</small>{m.name}</strong>{active===i&&<p>{m.body}</p>}<span className="context-moment-track"><i style={{width:`${i===active?Math.min(100,(film.time-i*chapterLength)/(chapterLength/100)):0}%`}}/></span></button>)}</div><div className="context-story-controls"><span>0{active+1} / 03</span><button aria-label={`${film.playing?'暂停':'播放'}续约流程`} onClick={film.toggle}>{film.playing?<Pause size={12} weight="fill"/>:<Play size={12} weight="fill"/>}{film.playing?'暂停':'播放'}</button></div></div>
   <div id="context-stage" role="tabpanel" aria-labelledby={`context-tab-${active}`}><RenewalWorkspace active={active} film={film} select={select}/></div>
  </div>

 </section>;
}
