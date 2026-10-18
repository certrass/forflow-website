/* One business record stays visible while its three handoff stages are explained. */
(() => {
  const root = document.querySelector('[data-one-flow]');
  if (!root) return;
  const play = root.querySelector('[data-flow-play]');
  const steps = [...root.querySelectorAll('[data-flow-step]')];
  const descriptions = [
    '先找齐同一笔业务的资料，保留来源与版本。',
    '按同一份规则核对条款，把需要人判断的内容留下。',
    '交接的不只是结论，还有原文、复核记录和下一位处理人。',
  ];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let step = 0, playing = false, visible = false, started = false, timer;
  const render = () => {
    root.dataset.step = String(step);
    steps.forEach((button, i) => button.setAttribute('aria-pressed', String(i === step)));
    root.querySelector('[data-flow-description]').textContent = descriptions[step];
    root.querySelector('.one-flow-foot small').textContent = `0${step + 1} / 03`;
    play.textContent = playing ? '暂停 Ⅱ' : step === 2 ? '重播 ↺' : '播放过程 ▷';
    play.setAttribute('aria-label', playing ? '暂停资料到待办的过程' : '播放资料到待办的过程');
    root.classList.toggle('is-playing', playing && visible && !document.hidden);
  };
  const schedule = () => {
    clearTimeout(timer);
    render();
    if (!playing || !visible || document.hidden) return;
    timer = setTimeout(() => {
      if (step < 2) step += 1;
      else playing = false;
      schedule();
    }, 3600);
  };
  steps.forEach((button, i) => button.addEventListener('click', () => {
    step = i; playing = false; started = true; schedule();
  }));
  play.addEventListener('click', () => {
    if (!playing && step === 2) step = 0;
    playing = !playing; started = true; schedule();
  });
  document.addEventListener('visibilitychange', schedule);
  reduced.addEventListener('change', () => {
    if (reduced.matches) { step = 2; playing = false; schedule(); }
  });
  if (reduced.matches) step = 2;
  const observer = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    if (visible && !started && !reduced.matches) { playing = true; started = true; }
    schedule();
  }, {threshold: 0.3});
  observer.observe(root);
  render();
})();
