import React, {useEffect, useRef, useState} from 'react';
import {ArrowUpRight} from '@phosphor-icons/react';
import {ShowcaseViewport} from './ShowcaseViewport.jsx';
import {FilmControls, FilmCursor} from './ShowcaseFilmUI.jsx';
import {useShowcaseFilm} from './useShowcaseFilm.js';

const duration=32000;
const chapters=[['提出续约问题',0],['对照条款复核',8500],['生成处理待办',20500]];
const descriptions=[
 '查看合同原文，核对终止与续约条款。',
 '对照原文复核字段，确认审批要求。',
 '先由法务复核，再交采购负责人确认。',
];

export function WorkspaceStory(){
 const root=useRef(null),frame=useRef(null);
 const [ready,setReady]=useState(false),[manual,setManual]=useState(false),[pointer,setPointer]=useState(null),[error,setError]=useState('');
 const film=useShowcaseFilm(root,duration,ready);
 const timeRef=useRef(0);timeRef.current=film.time;
 const chapter=film.time>=20500?2:film.time>=8500?1:0;
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
  <div className="story-task-brief"><div><h2>合同续约，查条款、定责任。</h2></div></div>
  <ShowcaseViewport label="ForFlow One · 企业 AI 工作台" chrome width={1440} extraControls={<button onClick={tour.toggle}>{film.playing?'暂停':'播放'}</button>} focusTarget=".source-workbench-frame" focusVersion={chapter}>
   <div className="story-stage source-workbench-stage">
    <iframe ref={frame} className="source-workbench-frame" src="/workbench/?tour=contract" title="ForFlow One 产品工作台" onLoad={()=>send({type:'hello'})}/>
    {!ready&&<div className="source-workbench-loading">正在打开 ForFlow One 工作台…</div>}
    <FilmCursor name="采购复核" x={pointer?.x||0} y={pointer?.y||0} visible={ready&&!manual&&film.playing&&!film.reduced&&!!pointer&&film.time<duration-1000} click={[3500,8500,12500,14500,18000,19000,20500,24500].some(t=>Math.abs(film.time-t)<200)}/>
   </div>
  </ShowcaseViewport>
  <div className="source-workbench-caption"><div><strong>{descriptions[chapter]}</strong></div><a href="/workbench/" target="_blank" rel="noopener">打开工作台<ArrowUpRight size={14}/></a></div>
  <div className="source-workbench-controls"><FilmControls film={tour} chapters={chapters} chapter={chapter} duration={duration} name="合同复核过程"/>{manual&&<span>已接管操作</span>}</div>
  {error&&<p className="source-workbench-error" role="status">操作过程已暂停，可重播或打开工作台继续。</p>}
 </section>;
}
