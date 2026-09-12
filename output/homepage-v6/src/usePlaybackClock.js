import {useEffect,useRef,useState} from 'react';

// One clock drives product state, progress and the operation guide.
export function usePlaybackClock(root,duration,{enabled=true,reducedEnd=false}={}){
 const clock=useRef(0),intent=useRef(true),visible=useRef(false),reducedRef=useRef(false),explicit=useRef(false);
 const [time,setTime]=useState(0),[playing,setPlaying]=useState(false),[revision,setRevision]=useState(0),[reduced,setReduced]=useState(false);
 const update=useRef(()=>{});
 useEffect(()=>{
  const preference=matchMedia('(prefers-reduced-motion: reduce)');
  const sync=()=>setPlaying(enabled&&intent.current&&visible.current&&!document.hidden&&(!reducedRef.current||explicit.current)&&clock.current<duration);
  update.current=sync;
  const onMotion=()=>{
   reducedRef.current=preference.matches;setReduced(preference.matches);
   if(preference.matches){explicit.current=false;intent.current=false;if(reducedEnd){clock.current=duration;setTime(duration)}}
   sync();
  };
  onMotion();
  const observer=new IntersectionObserver(([entry])=>{visible.current=entry.isIntersecting&&entry.intersectionRatio>=.25;sync()}, {threshold:[0,.25],rootMargin:'-72px 0px -24px 0px'});
  const stage=root.current?.querySelector('.showcase-viewport')||root.current;
  if(stage)observer.observe(stage);
  preference.addEventListener('change',onMotion);document.addEventListener('visibilitychange',sync);
  return()=>{observer.disconnect();preference.removeEventListener('change',onMotion);document.removeEventListener('visibilitychange',sync);update.current=()=>{}};
 },[root,duration,enabled,reducedEnd]);
 useEffect(()=>{
  if(!playing)return;
  let previous=performance.now();
  const tick=()=>{const now=performance.now();clock.current=Math.min(duration,clock.current+now-previous);previous=now;setTime(clock.current);if(clock.current>=duration)setPlaying(false)};
  const timer=setInterval(tick,50);
  return()=>clearInterval(timer);
 },[playing,duration]);
 const seek=(at,autoplay=false)=>{clock.current=Math.max(0,Math.min(duration,at));setTime(clock.current);setRevision(v=>v+1);intent.current=autoplay;explicit.current=autoplay;update.current()};
 const pause=()=>{intent.current=false;setPlaying(false)};
 const toggle=()=>{if(playing){pause();return}if(clock.current>=duration){seek(0,true);return}intent.current=true;explicit.current=true;update.current()};
 return {time,playing,reduced,revision,seek,pause,toggle,replay:()=>seek(0,true),complete:time>=duration,duration};
}
