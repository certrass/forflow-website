import React, {useEffect, useRef, useState} from 'react';
import {ArrowUpRight} from '@phosphor-icons/react';
import {ShowcaseViewport} from './ShowcaseViewport.jsx';
import {FilmControls, FilmCursor} from './ShowcaseFilmUI.jsx';
import {useShowcaseFilm} from './useShowcaseFilm.js';

const duration=46000;
const chapters=[['编排业务工作流',0],['审核内容与依据',8500],['评测并登记资产',26000]];
const descriptions=[
 ['把业务流程，编排成可执行的工作。','接收续约请求，关联供应商与合同，再按规则交由负责人审批。'],
 ['关键内容，先核对，再进入评测。','对照合同原文确认提取结果与审核结论，让后续评测有明确依据。'],
 ['通过评测后，登记为可复用的资产。','将工作流、规则与审核依据固定到一个版本，供后续项目使用。'],
];

export function WorkspaceStory(){
 const root=useRef(null),frame=useRef(null);
 const [ready,setReady]=useState(false),[manual,setManual]=useState(false),[pointer,setPointer]=useState(null),[error,setError]=useState('');
 const film=useShowcaseFilm(root,duration,ready);
 const timeRef=useRef(0);timeRef.current=film.time;
 const chapter=film.time>=26000?2:film.time>=8500?1:0;
 const send=data=>frame.current?.contentWindow?.postMessage({scope:'forflow-source-workbench',...data},location.origin);
 useEffect(()=>{
  const receive=e=>{if(e.origin!==location.origin||e.source!==frame.current?.contentWindow||e.data?.scope!=='forflow-source-workbench')return;
   if(e.data.type==='ready'){setReady(true);send({type:'seek',time:timeRef.current});}
   if(e.data.type==='takeover'){film.pause();setManual(true);setPointer(null);}
   if(e.data.type==='frame')setPointer(e.data.pointer);
   if(e.data.type==='error'){film.pause();setManual(true);setError(e.data.message);}
   if(e.data.type==='escape')root.current?.querySelector('[aria-label="关闭放大展示"]')?.click();
  };
  window.addEventListener('message',receive);return()=>window.removeEventListener('message',receive);
 },[]);
 useEffect(()=>{if(ready&&!manual)send({type:'seek',time:film.time});},[film.time,ready,manual]);
 const seek=(time,play=!film.reduced)=>{setManual(false);setError('');film.seek(time,play);send({type:'seek',time});};
 const tour={...film,seek,replay:()=>seek(0),toggle:()=>manual?seek(0):film.toggle()};
 return <section id="platform" className="workspace-story source-workbench" ref={root} aria-label="ForFlow One 产品工作台" data-mode={manual?'manual':'tour'} data-time={Math.floor(film.time)}>
  <ShowcaseViewport label="ForFlow One · 企业 AI 工作台" width={1440} extraControls={<button onClick={tour.toggle}>{film.playing?'暂停':'播放'}</button>} focusTarget=".source-workbench-frame" focusVersion={chapter}>
   <div className="story-stage source-workbench-stage">
    <iframe ref={frame} className="source-workbench-frame" src="/workbench/?tour=1" title="ForFlow One 产品工作台" onLoad={()=>send({type:'hello'})}/>
    {!ready&&<div className="source-workbench-loading">正在打开 ForFlow One 工作台…</div>}
    <FilmCursor name="平台管理员" x={pointer?.x||0} y={pointer?.y||0} visible={ready&&!manual&&film.playing&&!film.reduced&&!!pointer&&film.time<duration-1000} click={[2000,5700,8500,11000,15500,19500,21500,26000,32500,37000,41500].some(t=>Math.abs(film.time-t)<200)}/>
   </div>
  </ShowcaseViewport>
  <div className="source-workbench-caption"><div><strong>{descriptions[chapter][0]}</strong><p>{descriptions[chapter][1]}</p></div><a href="/workbench/" target="_blank" rel="noopener">打开工作台<ArrowUpRight size={14}/></a></div>
  <div className="source-workbench-controls"><FilmControls film={tour} chapters={chapters} chapter={chapter} duration={duration} name="工作台操作"/><span>{manual?'已接管，可继续操作工作台':'点击界面即可接管操作'}</span></div>
  {error&&<p className="source-workbench-error" role="status">操作过程已暂停，可重播或打开工作台继续。</p>}
 </section>;
}
