import React,{useEffect,useMemo,useRef,useState} from 'react';
import {ArrowRight,ArrowLeft,ArrowUpRight,ArrowCounterClockwise,MagnifyingGlass,CalendarBlank,Check,CheckSquare,Clock,DotsThree,FileText,FlowArrow,LinkSimple,ListBullets,Pause,Play,ShieldCheck,SquaresFour,Users,X,Sparkle} from '@phosphor-icons/react';
import {DetailTabs,ReviewHistory} from './ProductDetailUI.jsx';
import {PersonAvatar,Collaborators,HandoffReceipt,personForOwner} from './HumanDetails.jsx';
import {motionTiming,reducedMotion,useCardTravel,usePresence} from './ui-motion.js';

const seed=[
 {id:'CH-024',name:'渠道 B · 鞋履订单',note:'信用控制冻结',owner:'信用控制组',date:'08 月 28 日',stage:1,color:'purple'},
 {id:'CH-031',name:'渠道 C · 配件订单',note:'收货信息待补全',owner:'渠道运营组',date:'08 月 29 日',stage:0,color:'blue'},
 {id:'CH-017',name:'渠道 A · 服饰订单',note:'确认分批出库计划',owner:'履行团队',date:'08 月 27 日',stage:1,color:'green'},
 {id:'CH-012',name:'渠道 D · 服饰订单',note:'补货时间已确认',owner:'采购团队',date:'08 月 26 日',stage:2,color:'orange'},
 {id:'CH-009',name:'渠道 A · 鞋履订单',note:'按计划完成交接',owner:'渠道运营组',date:'08 月 25 日',stage:3,color:'blue'},
];
const stages=['发现异常','分析原因','人工复核','完成交接'];
function TaskCard({record,x,y,onSelect,selected}){
 const ref=useRef(null);
 useCardTravel(ref,x,y,record.id==='CH-024');
 return <button ref={ref} className={`task-card ${record.id==='CH-024'?'main-task':''}`} style={{transform:`translate(${x}px,${y}px)`}} data-task={record.id} data-stage={record.stage} aria-pressed={selected} onClick={event=>onSelect(record,event.currentTarget)}>
  <span className="task-id">{record.id}<ArrowUpRight size={12}/></span>
  <strong><LinkSimple size={14}/>{record.name}</strong>
  <span><CalendarBlank size={14}/>{record.date}</span>
  <span className="task-person"><PersonAvatar person={personForOwner(record.owner)} size={22}/>{record.owner}</span>
  <p>{record.note}</p>
  <div><FileText size={14}/><CheckSquare size={14}/><span><Clock size={12}/>{record.stage===2?'待复核':record.stage===3?'已交接':'已关联'}</span></div>
 </button>;
}
export function BusinessBoard({onEvidence,player}){
 const [detail,setDetail]=useState(null),[view,setView]=useState('board'),[filter,setFilter]=useState(false),[done,setDone]=useState([]),[dismissed,setDismissed]=useState(false),[panel,setPanel]=useState('overview'),[query,setQuery]=useState('');
 const detailRef=useRef(null),openerRef=useRef(null),focusRequested=useRef(false);
 const phase=Math.min(player.step,2);
 useEffect(()=>{setDone([]);setDetail(null);setDismissed(false);setView('board');setFilter(false);setPanel('overview');setQuery('')},[player.run]);
 const autoHandoff=player.step===2&&player.elapsed>=3600;
 useEffect(()=>{if(autoHandoff)setDone(ids=>ids.includes('CH-024')?ids:[...ids,'CH-024'])},[autoHandoff,player.run]);
 const records=useMemo(()=>seed.map((row,i)=>({...row,stage:done.includes(row.id)?3:i===0?phase:row.stage,note:i===0?(done.includes(row.id)?'复核结果已交给履行团队':['24 笔订单等待处理','已关联信用控制记录','放行条件待负责人确认'][phase]):row.note})),[done,phase]);
 const currentDetail=(detail?records.find(row=>row.id===detail):null)||(phase===2&&!dismissed?records[0]:null);
 const shownDetail=usePresence(currentDetail);
 const search=query.trim().toLocaleLowerCase();
 const shown=records.filter(row=>(!filter||row.stage===2)&&(!search||[row.id,row.name,row.owner,row.note].some(text=>text.toLocaleLowerCase().includes(search))));
 const select=(record,opener)=>{player.pause();openerRef.current=opener;focusRequested.current=currentDetail?.id!==record.id;if(!focusRequested.current)detailRef.current?.querySelector('[aria-label="关闭任务详情"]')?.focus({preventScroll:true});setDetail(record.id);setDismissed(false);setPanel('overview')};
 const closeDetail=()=>{setDetail(null);setDismissed(true);openerRef.current?.focus({preventScroll:true})};
 useEffect(()=>{if(focusRequested.current&&shownDetail){detailRef.current?.querySelector('[aria-label="关闭任务详情"]')?.focus({preventScroll:true});focusRequested.current=false}},[detail,shownDetail]);
 const detailIndex=shownDetail?shown.findIndex(row=>row.id===shownDetail.id):-1;
 const navigate=delta=>{const next=shown[detailIndex+delta];if(next){setDetail(next.id);setPanel('overview')}};
 const clearFilters=()=>{setQuery('');setFilter(false)};
 const completed=shownDetail&&(shownDetail.stage===3||done.includes(shownDetail.id));
 const slots=[0,0,0,0];
 return <div className="motion-demo" data-playing={player.playing}>
  <div className="motion-toolbar"><div><FlowArrow size={17}/><strong>渠道履行</strong><span>/</span><span>异常处理</span></div><span className="board-run-state"><Collaborators members={['credit','operations']} label="协作分工"/><span className={player.playing?'motion-live is-running':'motion-live'}/>{done.includes('CH-024')?'交接已完成':player.playing?'流程进行中':'查看与处理'}</span></div>
  <div className="board-controls"><div><button aria-pressed={view==='board'} className={view==='board'?'selected':''} onClick={()=>{setView('board');player.pause()}}><SquaresFour size={14}/>看板</button><button aria-pressed={view==='list'} className={view==='list'?'selected':''} onClick={()=>{setView('list');player.pause()}}><ListBullets size={14}/>列表</button></div><label className="board-search"><MagnifyingGlass size={13}/><input aria-label="搜索任务" placeholder="搜索任务或负责人" value={query} onFocus={()=>player.pause()} onChange={e=>{player.pause();setQuery(e.target.value);setDetail(null);setDismissed(true)}} onKeyDown={event=>{if(event.key==='Escape'&&query){event.stopPropagation();setQuery('')}}}/>{query&&<button aria-label="清空搜索" onClick={()=>setQuery('')}><X size={12}/></button>}</label><span className="board-match-count">{shown.length} 项</span><button aria-pressed={filter} className={filter?'selected':''} onClick={()=>{setFilter(v=>!v);setDetail(null);setDismissed(true);player.pause()}}><ShieldCheck size={13}/>{filter?'清除筛选':`待复核 ${records.filter(row=>row.stage===2).length}`}</button></div>
  <div className="kanban-stage">
   {view==='board'?<div className="kanban-board">
    <div className="kanban-columns">{stages.map((stage,i)=><div className="kanban-column" key={stage}><h4><i className={`dot dot-stage-${i}`}/>{stage}<span>{shown.filter(r=>r.stage===i).length}</span></h4></div>)}</div>
    <div className="kanban-cards">{shown.map(record=><TaskCard key={record.id} record={record} selected={currentDetail?.id===record.id} x={32+record.stage*265} y={65+slots[record.stage]++*218} onSelect={select}/>)}</div>
    {!shown.length&&<div className="board-empty"><MagnifyingGlass size={23} weight="light"/><strong>{search?'没有找到匹配的任务':'当前没有待复核事项'}</strong><span>{search?'试试任务编号、名称或负责人':'可以返回全部任务，查看处理进展。'}</span><button onClick={clearFilters}>查看全部任务</button></div>}
   </div>:<div className="board-list"><div>任务名称<span>当前阶段</span><span>负责人</span></div>{shown.map(row=><button onClick={event=>select(row,event.currentTarget)} aria-pressed={currentDetail?.id===row.id} key={row.id}><strong>{row.name}<small>{row.id}</small></strong><span><i className={`dot dot-stage-${row.stage}`}/>{stages[row.stage]}</span><span><PersonAvatar person={personForOwner(row.owner)} size={23}/>{row.owner}<ArrowUpRight size={13}/></span></button>)}{!shown.length&&<div className="board-empty"><strong>{search?'没有找到匹配的任务':'当前没有待复核事项'}</strong><span>试试其他条件，或返回全部任务。</span><button onClick={clearFilters}>查看全部任务</button></div>}</div>}
   {phase===1&&!shownDetail&&view==='board'&&!filter&&!search&&<button className="board-analysis" onClick={event=>select(records[0],event.currentTarget)}><div className="board-analysis-heading"><span><Sparkle size={17}/></span><strong>已找到关联的信用记录</strong><span>CH-024</span></div><p>渠道 B 的 24 笔鞋履订单，关联到同一项信用控制冻结。</p><div className="analysis-match"><span><FileText size={14}/>履行明细<strong>24 笔待处理</strong></span><LinkSimple size={14}/><span><ShieldCheck size={14}/>信用记录<strong>信用控制冻结</strong></span></div><div className="analysis-next"><span>下一步</span>信用控制组核对放行条件<ArrowRight size={13}/></div></button>}
   {shownDetail&&<aside ref={detailRef} className="task-detail" aria-label="当前任务详情" data-open={Boolean(currentDetail)} onKeyDown={event=>{if(event.key==='Escape'){event.stopPropagation();closeDetail()}}}><div className="detail-top"><span>{shownDetail.id}</span><div className="detail-pager"><span>{detailIndex>=0?`${detailIndex+1} / ${shown.length}`:'当前任务'}</span><button aria-label="查看上一项任务" title="上一项任务" disabled={detailIndex<=0} onClick={()=>navigate(-1)}><ArrowLeft size={13}/></button><button aria-label="查看下一项任务" title="下一项任务" disabled={detailIndex<0||detailIndex>=shown.length-1} onClick={()=>navigate(1)}><ArrowRight size={13}/></button></div><button onClick={closeDetail} aria-label="关闭任务详情"><X size={18}/></button></div><h3>{shownDetail.name}</h3><DetailTabs value={panel} onChange={setPanel} items={[['overview','任务详情'],['activity','处理记录',completed?3:2]]} label="任务详情视图"/>{panel==='activity'?<ReviewHistory label="处理进展" empty="" items={[{id:'source',title:'业务依据已关联',description:shownDetail.id+' · 订单状态与处理条件'},{id:'owner',title:completed?'负责人已确认':'等待负责人复核',description:shownDetail.owner,person:personForOwner(shownDetail.owner),pending:!completed},...(completed?[{id:'handoff',title:'已确认并完成交接',description:'复核结果与关联材料一起保留',person:shownDetail.id==='CH-024'?'operations':personForOwner(shownDetail.owner)}]:[])]}/>:<><span className={`state-tag ${completed?'green':'amber'}`}>{completed?'已完成交接':'待人工复核'}</span><p>{completed?'复核结果已确认，关联材料已随任务交接。':shownDetail.id==='CH-024'?'关联记录显示，24 笔订单受到信用控制冻结。需要核对付款情况与放行条件。':shownDetail.note+'，需要负责人核对关联材料并确认下一步。'}</p><div className="task-evidence-grid"><span>履行记录<strong>{shownDetail.id==='CH-024'?(completed?'24 笔已交接':'24 笔待处理'):'当前业务任务'}</strong></span><span>信用记录<strong>{shownDetail.id==='CH-024'?'信用控制冻结':'处理条件待核对'}</strong></span></div><div className="detail-section-label">关联依据</div><button className="detail-evidence" onClick={onEvidence}><FileText size={16}/>查看案例中的关联依据<ArrowUpRight size={13}/></button><div className="detail-section-label">处理负责人</div><div className="detail-owner"><PersonAvatar person={personForOwner(shownDetail.owner)} size={28}/>{shownDetail.owner}</div>{!completed&&<div className="detail-next"><ShieldCheck size={16}/><span>确认后，复核结果与关联材料一并交接。</span></div>}{completed&&<HandoffReceipt person={shownDetail.id==='CH-024'?'operations':personForOwner(shownDetail.owner)} title={shownDetail.id==='CH-024'?'已交给履行团队':'复核结果已交接'} description="关联依据随任务一起保留"/>}<button className="detail-confirm" disabled={completed} onClick={()=>{setDone(prev=>[...new Set([...prev,shownDetail.id])]);player.pause();}}>{completed?<><Check size={15}/>已完成交接</>:<>确认并交接<ArrowRight size={15}/></>}</button></>}</aside>}
  </div>
  <div className="motion-bottom"><span><LinkSimple size={13}/>{done.includes('CH-024')?'确认结果与关联材料，已一起交给履行团队':phase===0?'从一笔具体异常开始，找出它停在哪里':phase===1?'同一渠道、品类与时间口径，关联业务记录':'负责人核对放行条件，确认后进入业务交接'}</span><button onClick={()=>player.seek(0)}><ArrowCounterClockwise size={12}/>恢复初始状态</button></div>
 </div>;
}
