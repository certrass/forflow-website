/* On-demand detail without autoplay or loss of in-progress answers. */
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const toggle = document.querySelector('[data-diagnosis-toggle]');
  const drawer = document.querySelector('#home-diagnosis-drawer');
  if (toggle && drawer) {
    const setOpen = open => {
      drawer.inert = !open;
      drawer.setAttribute('aria-hidden', String(!open));
      drawer.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.querySelector('[data-diagnosis-label]').textContent = open ? '收起场景诊断' : '开始场景诊断';
    };
    toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
    document.querySelector('[data-diagnosis-close]').addEventListener('click', () => {
      setOpen(false);
      toggle.focus({preventScroll:true});
      toggle.closest('section').scrollIntoView({block:'start', behavior:reduced.matches ? 'instant' : 'smooth'});
    });
    // A deliberate navigation to the diagnostic section opens it; initial page
    // loads stay compact and continue to follow the site's hero-first policy.
    document.addEventListener('click', event => {
      const anchor = event.target.closest('a[href="#navigator"]');
      if (anchor) setOpen(true);
    });
  }

  const methods = [...document.querySelectorAll('.lower-method-item')];
  methods.forEach(item => item.addEventListener('toggle', () => {
    if (item.open) methods.filter(other => other !== item).forEach(other => { other.open = false; });
  }));

  const tabs = [...document.querySelectorAll('.lower-case-tabs [role="tab"]')];
  const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
  let active = 0, transition;
  const select = index => {
    if (index === active) return;
    active = index;
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
    });
    transition?.cancel();
    if (!reduced.matches) transition = panels[index].animate(
      [{opacity:0,transform:'translateY(7px)'},{opacity:1,transform:'translateY(0)'}],
      {duration:280,easing:'cubic-bezier(.22,1,.36,1)'}
    );
  };
  tabs.forEach((tab,index) => {
    tab.addEventListener('click', () => select(index));
    tab.addEventListener('keydown', event => {
      const next = event.key === 'ArrowRight' ? (index+1)%tabs.length :
        event.key === 'ArrowLeft' ? (index-1+tabs.length)%tabs.length :
        event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length-1 : null;
      if (next === null) return;
      event.preventDefault(); select(next); tabs[next].focus({preventScroll:true});
    });
  });
  reduced.addEventListener('change', () => { if (reduced.matches) transition?.cancel(); });
})();
