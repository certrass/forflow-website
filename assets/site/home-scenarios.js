(() => {
  const root = document.querySelector('[data-scenario-stories]');
  if (!root) return;
  const tabs = [...root.querySelectorAll('[data-story-tab]')];
  const panels = [...root.querySelectorAll('.scenario-panel')];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  let active = 0;
  let effects = [];

  function select(index, focus = false) {
    if (index === active) return;
    effects.forEach(animation => animation.cancel());
    effects = [];
    active = index;
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
    });
    if (focus) tabs[index].focus({preventScroll:true});
    const list = tabs[index].parentElement;
    const tab = tabs[index];
    list.scrollTo({left:tab.offsetLeft - list.offsetLeft - (list.clientWidth - tab.offsetWidth)/2, behavior:reduce.matches?'instant':'smooth'});
    if (!reduce.matches) {
      panels[index].querySelectorAll('.scenario-copy,.story-question,.story-context,.story-result,.story-source').forEach((el,i) => {
        effects.push(el.animate([{opacity:0,transform:`translateY(${i?7:4}px)`},{opacity:1,transform:'translateY(0)'}], {duration:300,delay:i*35,easing:'cubic-bezier(.22,1,.36,1)',fill:'backwards'}));
      });
    }
    root.querySelector('[data-story-live]').textContent = `当前场景：${tab.textContent.trim()}。${panels[index].querySelector('h3').textContent}`;
  }
  tabs.forEach((tab,i) => {
    tab.addEventListener('click',()=>select(i));
    tab.addEventListener('keydown',event=>{
      if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
      event.preventDefault();
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length-1 : (i + (event.key === 'ArrowRight' ? 1 : tabs.length-1)) % tabs.length;
      select(next,true);
    });
  });
  reduce.addEventListener('change',()=>{if(reduce.matches){effects.forEach(a=>a.cancel());effects=[];}});
})();
