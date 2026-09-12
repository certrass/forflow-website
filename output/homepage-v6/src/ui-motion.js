import {useEffect, useLayoutEffect, useRef, useState} from 'react';

export const motionTiming = {reveal:600, entrance:800, switch:500, exit:180, travel:940};
export const motionEase = 'cubic-bezier(.33,1,.68,1)';
export const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export function usePageReveal(root) {
  useEffect(() => {
    if (!root.current) return;
    const preference=matchMedia('(prefers-reduced-motion: reduce)');
    const selector='.journey-intro>*, .scenario-kicker, .scenario-title h3, .scenario-description, .product-presentation>.showcase-viewer>.showcase-viewport, .product-benefits>div, .case-strip, .advantages-heading, .capability-copy, .v6-section-heading, .v6-case-card, .v6-cta>h2';
    const nodes=[...root.current.querySelectorAll(selector)];
    const settle=node=>{node.dataset.revealState='visible';};
    const observer=new IntersectionObserver(entries=>entries.forEach(({isIntersecting,target})=>{
      if(!isIntersecting)return;
      target.dataset.revealState=preference.matches?'visible':'entering';
      observer.unobserve(target);
    }),{threshold:.12,rootMargin:'0px 0px -24px 0px'});
    const finish=event=>{if(event.target.dataset.revealState==='entering')settle(event.target)};
    const reduce=()=>{if(preference.matches){observer.disconnect();nodes.forEach(settle)}};
    nodes.forEach(node=>{
      const canvas=node.matches('.showcase-viewport');
      node.dataset.reveal=canvas?'canvas':node.matches('h2,h3')?'heading':'copy';
      const group=node.matches('.product-benefits>div,.v6-case-card')?[...node.parentElement.children].indexOf(node):0;
      const delay=node.matches('.scenario-description')?130:node.matches('.scenario-title h3')?60:Math.min(group,2)*70;
      node.style.setProperty('--reveal-delay',delay+'ms');
      if(preference.matches||node.getBoundingClientRect().top<innerHeight){settle(node);return;}
      node.dataset.revealState='pending';observer.observe(node);
    });
    const element=root.current;
    element.addEventListener('animationend',finish);
    preference.addEventListener('change',reduce);
    return()=>{observer.disconnect();element.removeEventListener('animationend',finish);preference.removeEventListener('change',reduce);nodes.forEach(node=>{delete node.dataset.reveal;delete node.dataset.revealState;node.style.removeProperty('--reveal-delay')})};
  },[root]);
}

// Native scrolling stays in charge. Only chapter selection and the reading line
// follow it, so keyboard anchors and manual wheel/touch input remain predictable.
export function useChapterNavigation(root){
 const [active,setActive]=useState(()=>Math.max(0,['#scenario-0','#scenario-1','#scenario-2'].indexOf(location.hash)));
 const requested=useRef(null),releaseTimer=useRef(null),scheduleRef=useRef(()=>{});
 const select=index=>{
  requested.current=index;setActive(index);clearTimeout(releaseTimer.current);
  releaseTimer.current=setTimeout(()=>{requested.current=null;scheduleRef.current()},1200);
 };
 useEffect(()=>{
  const element=root.current;if(!element)return;
  const sections=[...element.querySelectorAll('[data-scene]')],rail=element.querySelector('.product-rail');
  if(!sections.length||!rail)return;
  let frame=0,disposed=false;
  const update=()=>{
   frame=0;if(disposed)return;
   const header=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--header-height'))||72;
   const probe=header+rail.offsetHeight+48;
   const boxes=sections.map(section=>section.getBoundingClientRect());
   const current=Math.max(0,boxes.findLastIndex(box=>box.top<=probe));
   if(requested.current===null)setActive(current);
   const progress=Math.max(0,Math.min(1,(probe-boxes[0].top)/(boxes.at(-1).bottom-boxes[0].top)));
   rail.style.setProperty('--journey-progress',progress.toFixed(4));
  };
  const schedule=()=>{if(!frame)frame=requestAnimationFrame(update)};
  const release=()=>{requested.current=null;clearTimeout(releaseTimer.current);schedule()};
  scheduleRef.current=schedule;
  const observer=new ResizeObserver(schedule);observer.observe(element);
  window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule);
  window.addEventListener('scrollend',release);window.addEventListener('wheel',release,{passive:true});window.addEventListener('touchstart',release,{passive:true});
  document.fonts.ready.then(()=>{if(!disposed)schedule()});schedule();
  return()=>{disposed=true;cancelAnimationFrame(frame);clearTimeout(releaseTimer.current);observer.disconnect();scheduleRef.current=()=>{};window.removeEventListener('scroll',schedule);window.removeEventListener('resize',schedule);window.removeEventListener('scrollend',release);window.removeEventListener('wheel',release);window.removeEventListener('touchstart',release)};
 },[root]);
 return [active,select];
}

// Keep the same DOM node while its visual slot changes. The primary item lifts
// across the board; surrounding items settle into the space it leaves behind.
export function useCardTravel(ref, x, y, prominent) {
  const previous=useRef(null);
  useLayoutEffect(() => {
    const prior=previous.current;
    previous.current={x,y};
    if (!prior || !ref.current || reducedMotion() || prior.x===x && prior.y===y) return;
    const el=ref.current;
    const horizontal=prior.x!==x;
    const transform=(left,top,rotation=0,scale=1)=>`translate(${left}px,${top}px) rotate(${rotation}deg) scale(${scale})`;
    const travel=horizontal&&prominent;
    const frames=travel?[
      {transform:transform(prior.x,prior.y),boxShadow:'0 1px 2px #10111205',offset:0},
      {transform:transform(prior.x+(x-prior.x)*.12,prior.y-12,-.3,1.012),boxShadow:'0 18px 40px -16px #1011122e,0 5px 14px -6px #1011121a',offset:.18},
      {transform:transform(prior.x+(x-prior.x)*.55,Math.min(y,prior.y)-20,-.6,1.015),boxShadow:'0 18px 40px -16px #1011122e,0 5px 14px -6px #1011121a',offset:.55},
      {transform:transform(x,y),boxShadow:'0 1px 2px #10111205',offset:1},
    ]:[{transform:transform(prior.x,prior.y)},{transform:transform(x,y)}];
    el.style.zIndex=travel?'8':'2';
    const animation=el.animate(frames,{duration:travel?motionTiming.travel:550,easing:motionEase});
    animation.onfinish=()=>{el.style.zIndex='';};
    return()=>{animation.cancel();el.style.zIndex='';};
  },[ref,x,y,prominent]);
}

export function usePresence(value) {
  const [present,setPresent]=useState(value);
  useEffect(()=>{
    if(value){setPresent(value);return;}
    if(reducedMotion()){setPresent(null);return;}
    const timer=setTimeout(()=>setPresent(null),motionTiming.exit);
    return()=>clearTimeout(timer);
  },[value]);
  return value||present;
}
