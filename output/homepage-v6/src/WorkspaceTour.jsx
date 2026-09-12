import React,{useEffect,useLayoutEffect,useRef,useState} from 'react';

export const reviewOpinion='已对照运单和签收回执，确认实收 238 箱。2 箱差异由运输负责人继续核实。';
export const teamRequest='请核实这笔运单的 2 箱差异，核验依据已关联。';
export const teamReply='收到，我来核对仓库出入库记录，今天 16:00 前补充结果。';
export const tourLength=51000;
export const tourChapters=[{label:'AI 核验',at:0},{label:'核对依据',at:9500},{label:'人工确认',at:15200},{label:'团队协作',at:26000}];
const pointerStops=[[0,'start'],[650,'record'],[2400,'ai-checks'],[6500,'ai-result'],[9500,'ai-source'],[10300,'source-quantity'],[13000,'source-close'],[14500,'ai-draft'],[15800,'note'],[22200,'confirm'],[25200,'collaboration'],[27800,'team-assign'],[30400,'team-note'],[35500,'team-send'],[39000,'team-reply'],[42800,'activity'],[44200,'activity-handoff'],[45600,'close-record'],[47300,'complete'],[48700,'result']];
const clicks=[2100,10200,13900,15700,23700,26400,29700,31700,36400,43900,46900,48200];
export function tourFrame(time){
 const selected=time>=2200&&time<47000;
 const tab=time>=44000?'activity':time>=26500?'collaboration':time>=15800?'overview':'ai';
 const source=time>=10300&&time<14000;
 const reviewed=time>=23800,assigned=time>=29800,sent=time>=36500,acknowledged=time>=39000,aiDraft=time>=15800;
 const filter=time>=48300?'complete':'all';
 const partial=(text,start,duration)=>text.slice(0,Math.floor(Math.max(0,Math.min(1,(time-start)/duration))*text.length));
 const note=partial(reviewOpinion,15900,5700),teamNote=sent?'':partial(teamRequest,32000,3300);
 const aiStage=time<3600?'sources':time<4800?'align':time<6400?'compare':'ready';
 const chapter=time>=26000?3:time>=15200?2:time>=9500?1:0;
 const label=time<2200?'打开当前记录，让 AI 核对关联材料':time<6400?'AI 关联材料、对齐字段，检查跨单据一致性':time<9500?'AI 指出 2 箱差异，给出依据和仍需确认的问题':time<14000?'打开 AI 引用的签收回执，核对实收 238 箱':time<15800?'采用 AI 建议，生成可编辑的复核意见':time<23800?'AI 草拟意见，由业务复核人核对并确认':time<26500?'人工确认实收数量，后续差异继续跟进':time<29800?'将 2 箱差异交给运输负责人，材料和意见一起交接':time<36500?'在同一条记录里补充要求，并提醒负责人':time<44000?'运输负责人接手任务，回复处理计划和反馈时间':time<47000?'AI 判断、人工确认和团队交接保留在同一条记录':'复核已确认，2 箱差异由运输负责人继续跟进';
 return {selected,tab,source,reviewed,filter,note,teamNote,aiStage,aiDraft,assigned,sent,acknowledged,chapter,label,target:pointerStops.findLast(([at])=>time>=at)[1],click:clicks.findIndex(at=>time>=at&&time<at+380),typing:time>=15800&&time<22200,stateKey:[selected,tab,source,reviewed,filter,assigned,sent,acknowledged,aiDraft].join(':')};
}

export function useWorkspaceTour(root){
 const [time,setTime]=useState(0),[playing,setPlaying]=useState(false),[run,setRun]=useState(0),[manual,setManual]=useState(false),[started,setStarted]=useState(false);
 const elapsed=useRef(0),inView=useRef(false),entered=useRef(false),userPaused=useRef(false),isManual=useRef(false),reduced=useRef(false);
 useEffect(()=>{
  const element=root.current;if(!element)return;
  const preference=matchMedia('(prefers-reduced-motion: reduce)');reduced.current=preference.matches;
  const visible=()=>{if(document.hidden)setPlaying(false);else if(inView.current&&entered.current&&!userPaused.current&&!isManual.current&&!reduced.current&&elapsed.current<tourLength)setPlaying(true)};
  const observer=new IntersectionObserver(entries=>{
   inView.current=entries.at(-1).intersectionRatio>=.4;
   if(!inView.current){setPlaying(false);return;}
   if(!entered.current&&!isManual.current&&!reduced.current){entered.current=true;setStarted(true);setPlaying(true)}
   else visible();
  },{threshold:[0,.4]});
  const change=()=>{reduced.current=preference.matches;if(preference.matches){userPaused.current=true;setPlaying(false)}};
  observer.observe(element);document.addEventListener('visibilitychange',visible);preference.addEventListener('change',change);
  return()=>{observer.disconnect();document.removeEventListener('visibilitychange',visible);preference.removeEventListener('change',change)};
 },[root]);
 useEffect(()=>{
  if(!playing)return;
  let previous=performance.now();
  const tick=()=>{const now=performance.now();elapsed.current=Math.min(tourLength,elapsed.current+now-previous);previous=now;setTime(elapsed.current);if(elapsed.current===tourLength)setPlaying(false)};
  const timer=setInterval(tick,40);
  return()=>clearInterval(timer);
 },[playing,run]);
 const reveal=()=>{if(!root.current?.querySelector('.is-expanded'))root.current?.scrollIntoView({block:'start',behavior:reduced.current?'instant':'smooth'})};
 const startAt=at=>{entered.current=true;userPaused.current=false;isManual.current=false;elapsed.current=at;setTime(at);setManual(false);setStarted(true);setRun(v=>v+1);setPlaying(true);reveal()};
 const toggle=()=>{if(playing){userPaused.current=true;setPlaying(false)}else if(isManual.current||elapsed.current>=tourLength||!entered.current){startAt(0)}else{userPaused.current=false;setPlaying(true);reveal()}};
 const takeOver=event=>{if(event?.target.closest('.scene-playback-control,.showcase-controls'))return;entered.current=true;isManual.current=true;userPaused.current=true;setManual(true);setPlaying(false)};
 return {time,playing,run,manual,started,controlled:started&&!manual,frame:tourFrame(time),toggle,startAt,replay:()=>startAt(0),takeOver,pause:()=>takeOver()};
}

export function WorkspaceCursor({canvas,tour}){
 const pointer=useRef(null);
 const visible=tour.controlled&&tour.time>300&&tour.time<tourLength;
 useLayoutEffect(()=>{
  if(!visible||!pointer.current||!canvas.current)return;
  const app=canvas.current;const target=app.querySelector(`[data-tour="${tour.frame.target}"]`);
  const box=app.getBoundingClientRect();const scale=box.width/1280;
  let x=560,y=115;
  if(target){const rect=target.getBoundingClientRect();x=(rect.left-box.left+Math.min(rect.width*.48,110))/scale;y=(rect.top-box.top+rect.height*.52)/scale;
   if(tour.frame.target==='note'){x=(rect.left-box.left)/scale+34;y=(rect.top-box.top)/scale+22}
  }
  pointer.current.style.transform=`translate3d(${x}px,${y}px,0)`;
 },[canvas,visible,tour.time,tour.frame.target]);
 if(!visible)return null;
 return <div ref={pointer} className={`wq-virtual-cursor ${tour.playing?'':'is-paused'}`} aria-hidden="true" data-target={tour.frame.target}>
  {tour.frame.click>=0&&<i key={`${tour.run}-${tour.frame.click}`} className="wq-cursor-click"/>}
  <svg width="25" height="31" viewBox="0 0 25 31"><path d="M3 2.5L21.5 19H12.8L8.5 26.5L3 2.5Z" fill="#252b37" stroke="white" strokeWidth="1.7" strokeLinejoin="round"/></svg>
 </div>
}
