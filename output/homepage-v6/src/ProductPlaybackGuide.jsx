import React,{useLayoutEffect,useState} from 'react';

const tracks=[
 [
  [[400,'.main-task'],[3250,'.main-task',true]],
  [[900,'.board-analysis'],[4950,'.board-analysis',true]],
  [[500,'.detail-owner'],[2400,'.detail-confirm'],[3400,'.detail-confirm',true],[4000,'.task-evidence-grid']],
 ],
 [
  [[700,'.film-fields .demo-primary'],[2700,'.film-fields .demo-primary',true]],
  [[3900,'.extracted-fields>button:nth-child(3)'],[4950,'.extracted-fields>button:nth-child(3)',true]],
  [[400,'.paper-clauses>button:nth-child(3)'],[2200,'.film-fields .demo-primary'],[3400,'.film-fields .demo-primary',true],[4100,'.field-confirmed-actions']],
 ],
 [
  [[600,'.drawing-open-card button'],[2850,'.drawing-open-card button',true]],
  [[900,'.equipment-node.central'],[3100,'.equipment-node:nth-of-type(5)'],[4250,'.equipment-node:nth-of-type(5)',true]],
  [[500,'.relation-results .selected'],[2100,'.maintenance-prepare .demo-primary'],[3100,'.maintenance-prepare .demo-primary',true],[3800,'.prepared-work']],
 ],
];
export function ProductPlaybackGuide({root,index,player}){
 const [point,setPoint]=useState(null);
 const cue=tracks[index][player.step].findLast(([at])=>player.elapsed>=at);
 const targetSelector=cue?.[1];
 useLayoutEffect(()=>{
  if(!player.playing||player.reduced||!targetSelector){setPoint(null);return;}
  const native=root.current?.querySelector('.showcase-native');
  const target=native?.querySelector(targetSelector);
  if(!native||!target){setPoint(null);return;}
  const frame=native.getBoundingClientRect(),box=target.getBoundingClientRect(),scale=frame.width/native.offsetWidth;
  if(!box.width||!scale){setPoint(null);return;}
  const next={x:(box.left+box.width*.72-frame.left)/scale,y:(box.top+Math.min(24,box.height*.5)-frame.top)/scale};
  setPoint(old=>old&&Math.abs(old.x-next.x)<.5&&Math.abs(old.y-next.y)<.5?old:next);
 },[root,targetSelector,player.playing,player.reduced,player.time]);
 const click=cue?.[2]&&player.elapsed-cue[0]<320;
 return <div className={`product-guide-cursor ${point?'visible':''} ${click?'clicking':''}`} style={{transform:`translate3d(${point?.x||0}px,${point?.y||0}px,0)`}} aria-hidden="true"><i key={click?`${player.run}-${player.step}-${cue[0]}`:'rest'}/><svg width="23" height="29" viewBox="0 0 23 29"><path d="M3 2L20 17H12L8 25L3 2Z" fill="#252d29" stroke="white" strokeWidth="1.7" strokeLinejoin="round"/></svg></div>;
}
