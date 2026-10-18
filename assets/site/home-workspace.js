(() => {
  const root = document.querySelector('[data-workspace-film]');
  if (!root) return;
  const $ = selector => root.querySelector(selector);
  const all = selector => [...root.querySelectorAll(selector)];
  const scene = $('.fw-scene');
  const viewport = $('.fw-viewport');
  const frameBox = $('.fw-scale-frame');
  const drawer = $('.fw-source-drawer');
  const cursor = $('.fw-cursor');
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  const duration = 28000;
  const boundaries = [0, 7200, 17500, duration];
  const question = '核对这份续约合同，告诉我下一步由谁复核。';
  const sourceData = {
    contract: {
      name: '供应商服务合同', meta: '合同原文', section: '4.2 终止与续约变更',
      quote: '终止与续约变更须先由采购负责人复核，获批后方可更新供应商状态。',
      next: 'rule', nextText: '核对续约审批规则'
    },
    rule: {
      name: '续约审批规则', meta: '终止条款复核', section: '处理顺序 / 终止条款异常',
      quote: '终止条款需先由法务复核，再交负责人审批。',
      next: 'contract', nextText: '查看合同第 4.2 条'
    }
  };
  let elapsed = media.matches ? 18000 : 0;
  let requested = !media.matches;
  let visible = false;
  let raf = 0;
  let lastTime = 0;
  let lastPaint = 0;
  let lastPhase = '';
  let lastChapter = -1;
  let sourceKey = '';
  let sourceOpener = null;
  let cursorKey = '';
  let lastAutoSource = '';
  let completed = false;
  let creationTimer = 0;
  const effects = new Map();
  const ease = 'cubic-bezier(.22,1,.36,1)';

  // Transitions are local to the changed element. Replay and rapid clicks cancel stale work.
  function motion(element, keyframes, duration = 220, timeline = requested) {
    effects.get(element)?.animation.cancel();
    effects.delete(element);
    if (media.matches) return null;
    const animation = element.animate(keyframes, {duration, easing:ease});
    effects.set(element, {animation, timeline});
    const cleanup = () => { if (effects.get(element)?.animation === animation) effects.delete(element); };
    animation.finished.then(cleanup, cleanup);
    if (timeline && !playing()) animation.pause();
    return animation;
  }
  function enter(element, x = 0, duration = 220) {
    return motion(element, [{opacity:0,transform:`translate(${x}px,${x ? 0 : 4}px)`},{opacity:1,transform:'translate(0,0)'}], duration);
  }
  function moveIndicator() {
    const group = $('.fw-chapters');
    const active = $('[data-fw-chapter][aria-pressed="true"]');
    const indicator = $('.fw-chapter-indicator');
    if (!active) return;
    indicator.style.width = `${active.offsetWidth}px`;
    indicator.style.transform = `translateX(${active.offsetLeft - group.clientLeft}px)`;
  }

  const playing = () => requested && visible && !document.hidden && !completed;
  const announce = message => { $('.fw-live').textContent = message; };
  const narrow = () => matchMedia('(max-width:700px)').matches;
  function fit() {
    const compact = narrow();
    root.classList.toggle('is-mobile-film', compact);
    root.style.setProperty('--fw-pane-width', `${viewport.clientWidth}px`);
    const expanded = root.classList.contains('is-expanded');
    const scale = compact || expanded ? 1 : Math.min(viewport.clientWidth / 1000, 1.2);
    const width = compact ? viewport.clientWidth * 2 : 1000;
    scene.style.width = `${width}px`;
    scene.style.transform = `scale(${scale})`;
    frameBox.style.width = `${width * scale}px`;
    frameBox.style.height = `${644 * scale}px`;
    viewport.style.height = expanded ? '' : `${644 * scale}px`;
    $('.fw-pan-controls').hidden = !compact && !expanded;
    if (compact) panTo(Number(root.dataset.chapter) === 0 ? 'task' : 'result', false);
    else if (!expanded) viewport.scrollLeft = 0;
    cursorKey = '';
    renderCursor();
    moveIndicator();
  }
  function updatePlayback() {
    const active = playing();
    root.classList.toggle('is-playing', active);
    root.classList.toggle('is-complete', completed);
    $('[data-fw-play-label]').textContent = completed ? '重播' : active ? '暂停' : '播放';
    $('[data-fw-play-icon]').textContent = completed ? '↻' : active ? 'Ⅱ' : '▷';
    $('[data-fw-play]').setAttribute('aria-label', completed ? '重播合同复核过程' : active ? '暂停合同复核过程' : '播放合同复核过程');
    if (active && !raf) { lastTime = performance.now(); raf = requestAnimationFrame(tick); }
    if (!active && raf) { cancelAnimationFrame(raf); raf = 0; }
    effects.forEach(({animation, timeline}) => {
      if (!timeline || animation.playState === 'finished') return;
      if (active) animation.play(); else animation.pause();
    });
  }
  function pause() { requested = false; updatePlayback(); }
  function panTo(area, animate = true) {
    if (!narrow() && !root.classList.contains('is-expanded')) return;
    const left = area === 'task' ? 0 : narrow() ? viewport.clientWidth : 331;
    viewport.scrollTo({left, top: 0, behavior: !animate || media.matches ? 'instant' : 'smooth'});
    all('[data-fw-pan]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.fwPan === area)));
  }
  function setSource(key, opener = null, animate = true) {
    if (!key) {
      sourceKey = '';
      $('.fw-artifact').inert = false;
      $('.fw-intake').inert = false;
      drawer.inert = true;
      if (animate && !drawer.hidden && !media.matches) {
        const exit = motion(drawer, [{opacity:1,transform:'translateX(0)'},{opacity:0,transform:'translateX(8px)'}], 160);
        exit?.finished.then(() => { if (!sourceKey) drawer.hidden = true; }, () => {});
      } else {
        effects.get(drawer)?.animation.cancel();
        drawer.hidden = true;
      }
      all('[data-fw-source]').forEach(button => button.setAttribute('aria-pressed', 'false'));
      cursorKey = '';
      return;
    }
    const source = sourceData[key];
    if (!source) return;
    if (sourceKey === key && !drawer.hidden) return;
    const opening = drawer.hidden || !sourceKey;
    if (opener && !drawer.contains(opener)) sourceOpener = opener;
    sourceKey = key;
    const name = $('[data-fw-source-name]');
    name.replaceChildren(document.createTextNode(source.name));
    const small = document.createElement('small'); small.textContent = source.meta; name.append(small);
    $('[data-fw-source-section]').textContent = source.section;
    $('[data-fw-source-quote]').textContent = source.quote;
    const next = $('.fw-switch-source');
    next.dataset.fwSource = source.next;
    next.replaceChildren(document.createTextNode(source.nextText));
    const arrow = document.createElement('span'); arrow.textContent = '→'; next.append(arrow);
    drawer.hidden = false;
    drawer.inert = false;
    const backLabel = elapsed < 7200 ? '返回续约资料' : '返回核对结果';
    $('[data-fw-close]').textContent = `← ${backLabel}`;
    $('[data-fw-close]').setAttribute('aria-label', backLabel);
    $('.fw-artifact').inert = true;
    $('.fw-intake').inert = true;
    all('[data-fw-source]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.fwSource === key)));
    cursorKey = '';
    if (animate) {
      if (opening) enter(drawer, 12);
      else enter($('.fw-source-document'), 8);
      motion($('[data-fw-source-quote]'), [{backgroundColor:'#fff'},{backgroundColor:'#edf4e2'}], 420);
    }
    if (opener) {
      panTo('result');
      $('[data-fw-close]').focus({preventScroll:true});
    }
  }
  function closeSource(returnFocus = false, animate = true) {
    const opener = sourceOpener;
    setSource('', null, animate);
    if (returnFocus && opener?.isConnected && opener.getClientRects().length) opener.focus({preventScroll:true});
  }
  function renderCursor() {
    const targetKey = elapsed < 1700 ? 'composer' : elapsed < 7200 ? 'send' : elapsed < 10000 ? 'clause' : elapsed < 13800 ? 'switch' : elapsed < 17900 ? 'back' : 'create';
    if (targetKey === cursorKey) return;
    cursorKey = targetKey;
    const target = targetKey === 'composer' ? $('.fw-composer-text') : targetKey === 'send' ? $('[data-fw-send]') : targetKey === 'switch' ? $('.fw-switch-source') : targetKey === 'back' ? $('[data-fw-close]') : $(`[data-fw-cursor-target="${targetKey}"]`);
    if (!target?.getClientRects().length) return;
    const rect = target.getBoundingClientRect(); const box = scene.getBoundingClientRect();
    const scale = box.width / scene.offsetWidth;
    const from = getComputedStyle(cursor).transform;
    const to = `translate(${(rect.left - box.left + rect.width * .62) / scale}px,${(rect.top - box.top + rect.height * .58) / scale}px)`;
    cursor.style.transform = to;
    if (requested) motion(cursor, [{transform:from},{transform:to}], 480);
    else effects.get(cursor)?.animation.cancel();
  }
  function render(force = false) {
    const chapter = elapsed < 7200 ? 0 : elapsed < 17500 ? 1 : 2;
    const phase = elapsed < 2500 ? 'typing' : elapsed < 7200 ? 'reading' : elapsed < 17500 ? 'checking' : elapsed < 22500 ? 'handoff' : 'created';
    root.dataset.chapter = String(chapter);
    all('[data-fw-chapter]').forEach((button, index) => {
      button.setAttribute('aria-pressed', String(index === chapter));
      button.style.setProperty('--chapter-progress', Math.max(0, Math.min(1, (elapsed - boundaries[index]) / (boundaries[index + 1] - boundaries[index]))));
    });
    if (chapter !== lastChapter) {
      lastChapter = chapter;
      if (narrow()) panTo(chapter === 0 ? 'task' : 'result');
      moveIndicator();
    }
    if (phase !== lastPhase || force) {
      root.dataset.phase = phase;
      const created = phase === 'created';
      const intake = chapter === 0;
      $('.fw-intake').hidden = !intake;
      $('.fw-artifact').hidden = intake;
      if (!intake && (lastPhase === 'typing' || lastPhase === 'reading' || !lastPhase)) {
        enter($('.fw-artifact'), 0);
        [$('.fw-verdict'), $('.fw-records'), $('.fw-handoff')].forEach((element, index) => {
          motion(element, [{opacity:0,transform:'translateY(5px)',offset:0},{opacity:0,transform:'translateY(5px)',offset:index*.18},{opacity:1,transform:'translateY(0)',offset:1}], 260 + index * 70);
        });
      }
      $('[data-fw-intake-status]').textContent = phase === 'typing' ? '等待提交复核任务' : '正在核对第 4.2 条与续约审批规则…';
      $('[data-fw-status]').textContent = chapter === 0 ? '核对 2 份材料' : chapter === 1 ? '已找到 2 处依据' : created ? '已创建复核待办' : '复核顺序已确认';
      $('[data-fw-response]').textContent = chapter === 0 ? '先查续约条款，再核对审批规则。' : chapter === 1 ? '先请法务复核终止条款，再交采购负责人审批。' : created ? '法务复核待办已生成，完成后转采购负责人审批。' : '法务确认终止条款后，交采购负责人审批续约。';
      if (lastPhase) enter($('[data-fw-response]'), 0, 180);
      $('[data-fw-badge]').textContent = created ? '待复核' : '核对完成';
      $('[data-fw-route-state]').textContent = created ? '待处理' : '待创建';
      $('[data-fw-window-state]').textContent = created ? '1 项待办' : '2 份材料';
      const create = $('[data-fw-create]');
      create.removeAttribute('aria-busy');
      create.disabled = created || intake;
      create.innerHTML = created ? '待办已生成 <span>✓</span>' : '生成复核待办 <span>↗</span>';
      $('[data-fw-send]').disabled = phase !== 'typing';
      lastPhase = phase;
    }
    all('[data-fw-file-state]').forEach(label => {
      const contract = label.dataset.fwFileState === 'contract';
      const state = elapsed < 2500 ? 'ready' : elapsed < (contract ? 4300 : 6500) ? (contract || elapsed >= 4300 ? 'reading' : 'ready') : 'done';
      if (label.dataset.state !== state) {
        label.dataset.state = state;
        label.textContent = state === 'ready' ? '已上传' : state === 'reading' ? '读取中' : '✓ 已读取';
        label.closest('button').dataset.state = state;
      }
    });
    if (phase === 'reading') $('[data-fw-intake-status]').textContent = elapsed < 4300 ? '正在定位合同的续约条款…' : elapsed < 6500 ? '正在核对法务与采购的审批顺序…' : '2 份材料已核对，正在整理结论…';
    $('[data-fw-typing]').textContent = elapsed < 2500 ? question.slice(0, Math.floor(elapsed / 63)) : '核对这份续约合同';
    if (requested) {
      const autoSource = elapsed >= 9600 && elapsed < 13400 ? 'contract' : elapsed >= 13400 && elapsed < 17500 ? 'rule' : '';
      if (autoSource !== lastAutoSource) { setSource(autoSource); lastAutoSource = autoSource; }
      cursor.classList.toggle('is-clicking', [2450, 9550, 13350, 17450, 22450].some(time => elapsed >= time && elapsed < time + 550));
      const cues = [[2380,2500,'[data-fw-send]'],[9480,9600,'[data-fw-cursor-target="clause"]'],[13280,13400,'.fw-switch-source'],[17380,17500,'[data-fw-close]'],[22380,22500,'[data-fw-create]']];
      const pressed = cues.find(([start,end]) => elapsed >= start && elapsed < end);
      all('.is-film-pressed').forEach(button => { if (!pressed || !button.matches(pressed[2])) button.classList.remove('is-film-pressed'); });
      if (pressed) $(pressed[2]).classList.add('is-film-pressed');
    }
    renderCursor();
  }
  function tick(time) {
    raf = 0;
    if (!playing()) return;
    elapsed = Math.min(duration, elapsed + Math.min(time - lastTime, 150));
    lastTime = time;
    if (time - lastPaint >= 50 || elapsed === duration) { render(); lastPaint = time; }
    if (elapsed >= duration) { completed = true; requested = false; closeSource(); updatePlayback(); }
    else raf = requestAnimationFrame(tick);
  }
  function seek(time, play = false) {
    clearTimeout(creationTimer);
    effects.forEach(({animation}) => animation.cancel());
    effects.clear();
    all('.is-film-pressed').forEach(button => button.classList.remove('is-film-pressed'));
    pause(); elapsed = time; completed = time >= duration; requested = play;
    lastAutoSource = ''; closeSource(false, false); render(true); updatePlayback();
  }
  function expandView(expanded) {
    root.classList.toggle('is-expanded', expanded);
    const button = $('.fw-expand');
    button.setAttribute('aria-expanded', String(expanded));
    button.innerHTML = expanded ? '收起视图 <span aria-hidden="true">↙</span>' : '放大查看 <span aria-hidden="true">↗</span>';
    $('.fw-pan-controls').hidden = !expanded && !narrow();
    fit();
    if (!expanded && !narrow()) viewport.scrollTo(0, 0);
  }
  function selectChapter(chapter) {
    seek([1700, 7700, 18000][chapter]);
    if (chapter > 0) panTo('result');
    else panTo('task');
    announce(['发起复核：点击箭头提交合同和审批规则。', '查看依据：点击条款或审批规则打开原文。', '交给负责人：确认顺序后生成复核待办。'][chapter]);
  }
  root.addEventListener('click', event => {
    const button = event.target.closest('button'); if (!button || button.disabled) return;
    if (button.matches('[data-fw-play]')) {
      if (completed) seek(0, true);
      else { requested = !requested; if (requested) { lastAutoSource = null; render(); } updatePlayback(); }
    } else if (button.matches('[data-fw-replay]')) seek(0, true);
    else if (button.matches('[data-fw-send]')) { seek(2500, true); announce('已提交合同复核任务。'); }
    else if (button.matches('[data-fw-chapter]')) selectChapter(Number(button.dataset.fwChapter));
    else if (button.matches('[data-fw-source]')) {
      const key = button.dataset.fwSource;
      pause(); setSource(key, button); announce(`已打开${sourceData[key].name}。`);
    } else if (button.matches('[data-fw-close]')) { pause(); closeSource(true); }
    else if (button.matches('[data-fw-create]')) {
      pause(); button.disabled = true; button.setAttribute('aria-busy', 'true');
      button.textContent = '正在生成待办…';
      creationTimer = setTimeout(() => { seek(duration); announce('待办已生成，待法务复核，完成后转采购负责人审批。'); }, media.matches ? 0 : 320);
    }
    else if (button.matches('.fw-expand')) { pause(); expandView(!root.classList.contains('is-expanded')); }
    else if (button.matches('[data-fw-pan]')) { pause(); panTo(button.dataset.fwPan); }
  });
  root.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      if (!drawer.hidden) { event.preventDefault(); pause(); closeSource(true); }
      else if (root.classList.contains('is-expanded')) { event.preventDefault(); expandView(false); $('.fw-expand').focus({preventScroll:true}); }
    }
    if (event.key === 'Tab') pause();
    const chapter = event.target.closest('[data-fw-chapter]');
    if (chapter && ['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) {
      event.preventDefault();
      const index = Number(chapter.dataset.fwChapter);
      const next = event.key === 'Home' ? 0 : event.key === 'End' ? 2 : (index + (event.key === 'ArrowRight' ? 1 : 2)) % 3;
      selectChapter(next); all('[data-fw-chapter]')[next].focus({preventScroll:true});
    }
  });
  viewport.addEventListener('scroll', () => {
    all('[data-fw-pan]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.fwPan === (viewport.scrollLeft > (narrow() ? viewport.clientWidth / 2 : 165) ? 'result' : 'task'))));
  }, {passive:true});
  document.addEventListener('visibilitychange', updatePlayback);
  media.addEventListener('change', () => { if (media.matches) seek(18000); });
  new ResizeObserver(fit).observe(viewport);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting && entries[0].intersectionRatio >= .35; updatePlayback(); }, {threshold:[0,.35]}).observe(viewport);
  fit(); render(true); updatePlayback();
})();
