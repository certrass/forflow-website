/* Shared disclosure behavior for the static homepage and React product page. */
export function mountNavigation(root) {
  if (!root || root.dataset.navMounted) return () => {};
  root.dataset.navMounted = 'true';
  const controller = new AbortController();
  const on = (node, type, fn) => node.addEventListener(type, fn, {signal:controller.signal});
  const groups = [...root.querySelectorAll('.ff-nav-group')];
  const nav = root.querySelector('.ff-topbar-nav');
  const toggle = root.querySelector('.ff-nav-toggle');
  const compact = matchMedia('(max-width: 980px)');
  let hoverTimer, mobileOpen = false;
  const cancel = () => clearTimeout(hoverTimer);
  function show(active) {
    cancel();
    groups.forEach(group => {
      const open = group === active;
      group.classList.toggle('is-open', open);
      group.querySelector('button').setAttribute('aria-expanded', String(open));
      group.querySelector('.ff-nav-panel').inert = !open;
    });
  }
  function setMobile(open) {
    mobileOpen = open;
    root.classList.toggle('is-mobile-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? '关闭菜单' : '打开菜单');
    nav.inert = compact.matches && !open;
    document.documentElement.classList.toggle('ff-navigation-open', open);
    if (!open) show(null);
  }
  for (const group of groups) {
    const trigger = group.querySelector('button');
    on(trigger, 'click', () => show(group.classList.contains('is-open') ? null : group));
    on(trigger, 'pointerenter', e => {
      if (compact.matches || e.pointerType !== 'mouse') return;
      cancel(); hoverTimer = setTimeout(() => show(group), 100);
    });
    on(trigger, 'keydown', e => {
      if (e.key === 'ArrowDown') {
        e.preventDefault(); show(group);
        requestAnimationFrame(() => [...group.querySelectorAll('.ff-nav-panel a')].find(link => link.getClientRects().length)?.focus());
      }
    });
  }
  on(root, 'pointerenter', cancel);
  on(root, 'pointerleave', e => {
    if (compact.matches || e.pointerType !== 'mouse') return;
    cancel(); hoverTimer = setTimeout(() => show(null), 180);
  });
  on(toggle, 'click', () => setMobile(!mobileOpen));
  on(root, 'click', e => { if (e.target.closest('a')) setMobile(false); });
  on(root, 'focusout', e => { if (!root.contains(e.relatedTarget)) { if (!mobileOpen) show(null); } });
  on(document, 'pointerdown', e => { if (!root.contains(e.target)) setMobile(false); });
  on(document, 'keydown', e => {
    if (e.key !== 'Escape') return;
    const active = groups.find(g => g.classList.contains('is-open'));
    if (active) { show(null); active.querySelector('button').focus(); }
    else if (mobileOpen) { setMobile(false); toggle.focus(); }
  });
  // Keep keyboard focus inside the mobile disclosure until a link or close is chosen.
  on(root, 'keydown', e => {
    if (!mobileOpen || e.key !== 'Tab') return;
    const items = [...root.querySelectorAll('a,button')].filter(el => !el.closest('[inert]') && el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden');
    const first = items[0], last = items[items.length-1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  on(compact, 'change', () => setMobile(false));
  on(window, 'scroll', () => root.classList.toggle('is-scrolled', scrollY > 12));
  setMobile(false);
  root.classList.toggle('is-scrolled', scrollY > 12);
  return () => { cancel(); controller.abort(); document.documentElement.classList.remove('ff-navigation-open'); delete root.dataset.navMounted; };
}
if (typeof document !== 'undefined') document.querySelectorAll('[data-ff-navigation]').forEach(mountNavigation);
