/* Guru's source / context / agent choreography, implemented locally with WAAPI.
   No runtime dependency, third-party tracker or product workspace changes. */
(()=>{
 const root=document.querySelector('[data-knowledge-motion]');if(!root)return;
 const svg=root.querySelector('.knowledge-paths'),scene=root.querySelector('.knowledge-scene'),viewport=root.querySelector('.knowledge-viewport');
 const play=root.querySelector('[data-knowledge-play]'),replay=root.querySelector('[data-knowledge-replay]'),expand=root.querySelector('[data-knowledge-expand]');
 const media=matchMedia('(prefers-reduced-motion: reduce)'),animations=[];
 const ns='http://www.w3.org/2000/svg',ease='cubic-bezier(.16,1,.3,1)';
 let visible=false,paused=false,expanded=false;
 const el=(tag,attrs)=>{const node=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))node.setAttribute(k,v);return node};
 const animate=(node,frames,options)=>{const a=node.animate(frames,{fill:'both',...options});a.pause();a.currentTime=0;animations.push(a);return a};
 const reveal=(node,delay,scale=.7)=>animate(node,[{opacity:0,transform:`scale(${scale})`},{opacity:1,transform:'scale(1)'}],{duration:900,delay,easing:ease});
 const draw=(path,delay,duration=1200)=>{const line=path.cloneNode();line.setAttribute('class','knowledge-draw');line.setAttribute('pathLength','1');line.style.strokeDasharray='1';path.parentNode.append(line);animate(line,[{strokeDashoffset:1},{strokeDashoffset:0}],{duration,delay,easing:'cubic-bezier(.65,0,.35,1)'});return line};
 const particles=(path,delay,count=2,duration=3800)=>{
  const length=path.getTotalLength(),points=Array.from({length:81},(_,i)=>{const p=path.getPointAtLength(length*i/80);return {offset:i/80,transform:`translate(${p.x}px,${p.y}px)`,opacity:i===0||i===80?0:i<5||i>75?.3:.85}});
  for(let i=0;i<count;i++){const dot=el('circle',{r:1.9,class:'knowledge-particle'});path.parentNode.append(dot);animate(dot,points,{duration,delay:delay+i*duration/count,iterations:Infinity,easing:'linear'});}
 };
 // Stable 1200×720 composition: resize scales the whole scene, never reflows it.
 for(const [side,nodes] of [['source',root.querySelectorAll('.knowledge-node:not(.is-target)')],['target',root.querySelectorAll('.knowledge-node.is-target')]]){
  nodes.forEach((node,i)=>{
   const y=80+i*110,isSource=side==='source';
   node.style.top=`${y-31}px`;
   const d=isSource?`M 132 ${y} C 266 ${y},250 360,330 360`:`M 870 360 C 950 360,934 ${y},1068 ${y}`;
   const branch=el('g',{class:'knowledge-branch'});svg.append(branch);
   const path=el('path',{d,class:'knowledge-track'});branch.append(path);
   const delay=(isSource?120:900)+i*55;
   animate(node,[{opacity:0,transform:`translateX(${isSource?-12:12}px)`},{opacity:1,transform:'translateX(0)'}],{duration:850,delay:(isSource?0:1050)+i*55,easing:ease});
   animate(path,[{opacity:0},{opacity:1}],{duration:1200,delay,easing:ease});
   draw(path,delay);particles(path,(isSource?850:1750)+i*170,2,4000+i*170);
   node.addEventListener('pointerenter',()=>{scene.classList.add('has-focus');branch.classList.add('is-active')});
   node.addEventListener('pointerleave',()=>{scene.classList.remove('has-focus');branch.classList.remove('is-active')});
  });
 }
 const ring=el('path',{d:'M 600 90 A 270 270 0 1 1 599.99 90',class:'knowledge-orbit'});svg.append(ring);draw(ring,550,1400);particles(ring,1700,2,16000);
 animate(root.querySelector('.knowledge-context-label'),[{opacity:0},{opacity:1}],{duration:800,delay:850,easing:ease});
 root.querySelectorAll('.knowledge-orbit-note').forEach((node,i)=>animate(node,[{opacity:0},{opacity:1}],{duration:800,delay:900+i*90,easing:ease}));
 reveal(root.querySelector('.knowledge-hub'),450,.84);reveal(root.querySelector('.knowledge-hub-label'),650,.98);
 root.querySelectorAll('.knowledge-pill-row').forEach((node,i)=>animate(node,[{opacity:0,transform:`translate(${i%2?10:-10}px,12px)`},{opacity:1,transform:'translate(0,0)'}],{duration:950,delay:700+i*85,easing:ease}));
 animate(root.querySelector('.knowledge-hub img'),[{transform:'translateY(0) rotate(-9deg)',filter:'drop-shadow(0 0 14px #78d58a10)'},{transform:'translateY(-4px) rotate(-5deg)',filter:'drop-shadow(0 0 22px #78d58a24)'}],{duration:3400,delay:1200,iterations:Infinity,direction:'alternate',easing:'ease-in-out'});
 const update=()=>{
  const running=visible&&!paused&&!document.hidden&&!media.matches;
  root.dataset.motionState=running?'running':'paused';
  animations.forEach(a=>{if(media.matches){a.pause();a.currentTime=6000}else if(running){if(a.playState!=='finished')a.play()}else if(a.playState!=='finished')a.pause()});
  play.setAttribute('aria-pressed',String(paused));play.setAttribute('aria-label',paused?'播放知识连接动效':'暂停知识连接动效');play.textContent=paused?'▷ 播放':'Ⅱ 暂停';
 };
 const reset=()=>animations.forEach(a=>{a.pause();a.currentTime=0});
 new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;if(!visible&&entry.boundingClientRect.top>=innerHeight&&!paused)reset();update()},{threshold:.08}).observe(viewport);
 play.addEventListener('click',()=>{paused=!paused;update()});replay.addEventListener('click',()=>{paused=false;reset();update()});
 document.addEventListener('visibilitychange',update);media.addEventListener('change',()=>{reset();update()});
 const resize=()=>{const width=viewport.clientWidth;const scale=expanded?Math.max(width/1200,.85):Math.min(1.2,width/1200);scene.style.setProperty('--knowledge-scale',scale);scene.parentElement.style.width=`${1200*scale}px`;viewport.style.height=`${720*scale}px`;if(width>700&&expanded){expanded=false;viewport.classList.remove('is-expanded');expand.setAttribute('aria-expanded','false');expand.textContent='放大查看';resize()}};
 new ResizeObserver(resize).observe(viewport);
 expand.addEventListener('click',()=>{expanded=!expanded;viewport.classList.toggle('is-expanded',expanded);expand.setAttribute('aria-expanded',String(expanded));expand.textContent=expanded?'恢复全貌':'放大查看';resize();viewport.scrollTo({left:expanded?(scene.getBoundingClientRect().width-viewport.clientWidth)/2:0,behavior:'instant'})});
 resize();update();root.dataset.motionReady='true';
})();
