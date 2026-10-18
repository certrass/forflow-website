/* Viewport / page visibility aware ribbon motion with explicit user pause. */
(()=>{
  const mounted=new WeakSet(), media=matchMedia('(prefers-reduced-motion: reduce)');
  const mount=()=>document.querySelectorAll('[data-guru-motion]').forEach(root=>{
    if(mounted.has(root))return;mounted.add(root);
    let visible=false,paused=false;
    const button=root.querySelector('[data-motion-toggle]');
    const update=()=>{
      root.dataset.motionState=visible&&!paused&&!document.hidden&&!media.matches?'running':'paused';
      button.setAttribute('aria-pressed',String(paused));
      button.setAttribute('aria-label',paused?'播放工作动态':'暂停工作动态');
      button.textContent=paused?'▷ 播放动态':'Ⅱ 暂停动态';
    };
    button.addEventListener('click',()=>{paused=!paused;update()});
    const observer=new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;update()},{threshold:.04});
    observer.observe(root);document.addEventListener('visibilitychange',update);media.addEventListener('change',update);update();
  });
  mount();new MutationObserver(records=>{
    if(records.some(r=>[...r.addedNodes].some(n=>n.nodeType===1&&(n.matches('[data-guru-motion]')||n.querySelector('[data-guru-motion]')))))mount();
  }).observe(document.body,{childList:true,subtree:true});
})();
