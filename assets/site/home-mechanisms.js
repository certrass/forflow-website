(() => {
 'use strict';
 const root = document.querySelector('[data-mechanisms]');
 if (!root) return;
 const reduced = matchMedia('(prefers-reduced-motion: reduce)');
 const animations = new Map();
 const enter = element => {
   animations.get(element)?.cancel();
   if (reduced.matches) return;
   const animation = element.animate([{opacity:0, transform:'translateY(6px)'},{opacity:1,transform:'translateY(0)'}], {duration:280,easing:'cubic-bezier(.22,1,.36,1)'});
   animations.set(element,animation);
 };
 const announce = text => { root.querySelector('[data-mechanism-live]').textContent = text; };
 const picker = root.querySelector('[data-agent-menu]');
 const pickerToggle = root.querySelector('[data-agent-toggle]');
 pickerToggle.addEventListener('click', () => {
   picker.hidden = !picker.hidden;
   pickerToggle.setAttribute('aria-expanded', String(!picker.hidden));
   if (!picker.hidden) enter(picker);
 });
 root.querySelectorAll('[data-agent-choice]').forEach(button => button.addEventListener('click', () => {
   root.querySelectorAll('[data-agent-choice]').forEach(b => b.setAttribute('aria-pressed',String(b===button)));
   pickerToggle.querySelector('img').src = button.querySelector('img').getAttribute('src');
   pickerToggle.querySelector('b').textContent = button.dataset.agentChoice;
   enter(pickerToggle.querySelector('img'));
   announce('已选择 '+button.dataset.agentChoice);
 }));
 root.querySelectorAll('[data-context-file]').forEach(button => button.addEventListener('click', () => {
   root.querySelectorAll('[data-context-file]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
   const caption=root.querySelector('[data-context-caption]');
   caption.textContent=button.dataset.contextFile;
   enter(caption);
 }));
 function tabs(group, tabAttribute, panelAttribute, after) {
   const buttons=[...group.querySelectorAll('['+tabAttribute+']')];
   const activate=(button, focus=false)=>{
     buttons.forEach(b=>{b.setAttribute('aria-selected',String(b===button));b.tabIndex=b===button?0:-1;});
     group.querySelectorAll('['+panelAttribute+']').forEach(panel=>{
       const selected=panel.getAttribute(panelAttribute)===button.getAttribute(tabAttribute);
       panel.hidden=!selected;if(selected)enter(panel);
     });
     if(focus)button.focus({preventScroll:true});
     after?.(button);
   };
   buttons.forEach((b,i)=>{
     b.addEventListener('click',()=>activate(b));
     b.addEventListener('keydown',e=>{
       if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;
       e.preventDefault();const index=e.key==='Home'?0:e.key==='End'?buttons.length-1:(i+(e.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length;
       activate(buttons[index],true);
     });
   });
 }
 tabs(root.querySelector('[data-mechanism-tools]'),'data-tool-tab','data-tool-panel');
 tabs(root.querySelector('[data-mechanism-review]'),'data-review-tab','data-review-panel');
 const statuses=['正在拆解任务…','正在读取项目材料…','正在生成工作结果…','正在核对改动…'];
 const icons=['i-flow','i-document','i-code','i-check'];
 const run=root.querySelector('[data-mechanism-run]');
 const status=run.querySelector('[data-run-status]');
 const play=run.querySelector('[data-run-play]');
 const steps=[...run.querySelectorAll('[data-run-step]')];
 let current=0, elapsed=0,previous=0,frame=0,visible=false,paused=false;
 const paint=()=>{
   status.textContent=statuses[current];
   run.querySelector('[data-run-icon]').setAttribute('href','#'+icons[current]);
   steps.forEach((b,i)=>b.setAttribute('aria-pressed',String(i===current)));
   run.dataset.step=String(current);enter(status);
 };
 const tick=now=>{
   if(previous)elapsed+=Math.min(now-previous,100);
   previous=now;
   if(elapsed>=2800){elapsed=0;current=(current+1)%statuses.length;paint();}
   frame=requestAnimationFrame(tick);
 };
 const update=()=>{
   cancelAnimationFrame(frame);previous=0;
   const running=visible&&!paused&&!document.hidden&&!reduced.matches;
   run.dataset.motionState=running?'running':'paused';
   play.textContent=reduced.matches?'下一步 →':paused?'▷ 播放':'Ⅱ 暂停';
   play.setAttribute('aria-label',reduced.matches?'查看下一任务步骤':paused?'播放任务步骤':'暂停任务步骤');
   play.setAttribute('aria-pressed',String(paused||reduced.matches));
   if(running)frame=requestAnimationFrame(tick);
 };
 steps.forEach((button,i)=>button.addEventListener('click',()=>{current=i;elapsed=0;paused=true;paint();update();announce(statuses[i].replace('…',''));}));
 play.addEventListener('click',()=>{if(reduced.matches){current=(current+1)%statuses.length;paint();announce(statuses[current]);}else{paused=!paused;update();}});
 new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;update();},{threshold:.25}).observe(run);
 document.addEventListener('visibilitychange',update);
 reduced.addEventListener('change',()=>{animations.forEach(a=>a.cancel());update();});
 const dialog=document.querySelector('[data-mechanism-dialog]');
 const captureImage=dialog.querySelector('img');
 const captureBody=dialog.querySelector('.mechanism-dialog-body');
 const zoom=dialog.querySelector('[data-capture-zoom]');
 let opener=null,bodyBefore=null,scrollBefore=0;
 const setCaptureView=(detail)=>{
   dialog.dataset.view=detail?'detail':'overview';
   zoom.setAttribute('aria-pressed',String(detail));
   zoom.textContent=detail?'查看全貌':'放大细看';
   dialog.querySelector('[data-capture-hint]').textContent=detail?'左右滑动，查看界面细节':'完整工作台';
   const reveal=()=>{
     if(!dialog.open)return;
     const mainPane=Number(opener?.dataset.captureX ?? .095);
     const top=Number(opener?.dataset.captureY ?? 0);
     const imageRect=captureImage.getBoundingClientRect();
     captureBody.scrollTo({left:detail?imageRect.width*mainPane:0,top:detail?imageRect.height*top:0,behavior:'instant'});
   };
   captureImage.onload=reveal;
   if(captureImage.complete)reveal();
 };
 root.querySelectorAll('[data-product-capture]').forEach(button=>button.addEventListener('click',()=>{
   opener=button;captureImage.src=button.dataset.productCapture;
   captureImage.alt=button.dataset.captureTitle;
   dialog.querySelector('[data-capture-title]').textContent=button.dataset.captureTitle;
   scrollBefore=window.scrollY;
   bodyBefore=Object.fromEntries(['overflow','position','top','width'].map(key=>[key,document.body.style[key]]));
   document.body.style.overflow='hidden';
   // Fixed positioning also prevents the underlying page moving in iOS Safari.
   if(innerWidth<=700)Object.assign(document.body.style,{position:'fixed',top:-scrollBefore+'px',width:'100%'});
   dialog.showModal();
   setCaptureView(innerWidth<=700);
 }));
 zoom.addEventListener('click',()=>setCaptureView(dialog.dataset.view!=='detail'));
 dialog.querySelector('[data-capture-close]').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 dialog.addEventListener('close',()=>{
   captureImage.onload=null;
   Object.assign(document.body.style,bodyBefore);
   window.scrollTo({top:scrollBefore,behavior:'instant'});
   opener?.focus({preventScroll:true});
 });
 update();
})();
