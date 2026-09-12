import React from 'react';
import {ArrowCounterClockwise,Pause,Play,Check} from '@phosphor-icons/react';
import {usePlaybackClock} from './usePlaybackClock.js';

export function useScenePlayback(root,durations){
 const total=durations.reduce((sum,value)=>sum+value,0);
 const clock=usePlaybackClock(root,total);
 const starts=durations.map((_,i)=>durations.slice(0,i).reduce((sum,value)=>sum+value,0));
 const step=Math.max(0,starts.findLastIndex(at=>clock.time>=at));
 const seek=index=>clock.seek(starts[index]);
 const startAt=index=>clock.seek(starts[index],true);
 const takeOver=event=>{
  // A swipe is page navigation. Only activating a product control takes over.
  if(!event.target.closest('.showcase-native')||!event.target.closest('button,a,input,textarea,select,[role="button"]'))return;
  if(event.type==='keydown'&&['Tab','Escape','PageUp','PageDown'].includes(event.key))return;
  clock.pause();
 };
 return {...clock,step,run:clock.revision,seek,startAt,takeOver,elapsed:clock.time-starts[step],progress:Math.min(1,(clock.time-starts[step])/durations[step]),duration:durations[step],total};
}
export const formatPlaybackTime=ms=>`${Math.floor(ms/60000)}:${String(Math.floor(ms/1000)%60).padStart(2,'0')}`;

export function ScenePlayback({player,steps,label,onNavigate=()=>{}}){
 return <div className="scene-playback" aria-label={label}>
  <div className="scene-chapters">{steps.map((step,index)=><button key={step} onClick={()=>{player.seek(index);onNavigate()}} aria-label={`${String(index+1).padStart(2,'0')} ${step}`} aria-pressed={player.step===index} className={player.step===index?'current':player.step>index?'past':''}><span>{player.step>index?<Check size={11}/>:String(index+1).padStart(2,'0')}</span><strong>{step}</strong><i className="chapter-progress" style={{transform:`scaleX(${index<player.step?1:index>player.step?0:player.progress})`}}/></button>)}</div>
  <div className="scene-transport">
   <span className="playback-time" aria-label={`${formatPlaybackTime(player.time)} / ${formatPlaybackTime(player.total)}`}>{formatPlaybackTime(player.time)}<span> / {formatPlaybackTime(player.total)}</span></span>
   <button className="scene-toggle" title={player.playing?'暂停，停下来查看细节':player.complete?'从头播放流程':'继续播放流程'} onClick={()=>{player.toggle();if(!player.playing)onNavigate()}} aria-label={player.playing?'暂停产品演示':player.complete?'重播产品演示':'播放产品演示'}>{player.playing?<Pause size={13} weight="fill"/>:player.complete?<ArrowCounterClockwise size={14}/>:<Play size={13} weight="fill"/>}</button>
   <button className="scene-replay" title="重播并恢复初始状态" onClick={()=>{player.replay();onNavigate()}} aria-label="重新播放产品演示"><ArrowCounterClockwise size={14}/></button>
  </div>
 </div>;
}
