import React,{useLayoutEffect,useRef} from 'react';

export function ProductSceneNav({items,active,onSelect}){
 const ref=useRef(null);
 useLayoutEffect(()=>{
  const nav=ref.current;let disposed=false;
  const measure=()=>{
   if(disposed)return;
   const link=nav.querySelector('[aria-current="true"]');if(!link)return;
   nav.style.setProperty('--chapter-x',`${link.offsetLeft}px`);
   nav.style.setProperty('--chapter-width',`${link.offsetWidth}px`);
   nav.style.setProperty('--chapter-y',`${link.offsetTop}px`);
   nav.style.setProperty('--chapter-height',`${link.offsetHeight}px`);
   nav.dataset.indicatorReady='true';
  };
  const observer=new ResizeObserver(measure);observer.observe(nav);
  document.fonts.ready.then(measure);measure();
  return()=>{disposed=true;observer.disconnect()};
 },[active]);
 return <nav ref={ref} className="chapter-nav" aria-label="业务场景导航">{items.map((item,index)=><a key={item.id} href={`#scenario-${index}`} aria-current={active===index?'true':undefined} onClick={()=>onSelect(index)}><item.Icon size={16}/><span>{item.name}</span></a>)}</nav>;
}
