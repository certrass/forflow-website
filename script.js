(() => {
  'use strict';

  document.documentElement.classList.add('js');

  const qs = (selector, root = document) => root.querySelector(selector);
  const qsa = (selector, root = document) => [...root.querySelectorAll(selector)];

  function createToast(message) {
    let toast = qs('[data-toast]');
    if (!toast) {
      toast = document.createElement('div');
      toast.dataset.toast = '';
      toast.setAttribute('role', 'status');
      Object.assign(toast.style, {
        position: 'fixed',
        left: '50%',
        bottom: '24px',
        zIndex: '999',
        maxWidth: 'min(92vw, 460px)',
        padding: '12px 16px',
        borderRadius: '999px',
        background: '#050505',
        color: '#fff',
        boxShadow: '0 14px 40px rgba(0,0,0,.25)',
        fontSize: '.84rem',
        fontWeight: '700',
        textAlign: 'center',
        opacity: '0',
        transform: 'translate(-50%, 12px)',
        transition: 'opacity .2s, transform .2s'
      });
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translate(-50%, 0)';
    });
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translate(-50%, 12px)';
    }, 2400);
  }

  function initMenu() {
    const toggle = qs('.menu-toggle');
    const panel = qs('.mobile-menu-panel');
    if (!toggle || !panel) return;

    const setOpen = (open) => {
      document.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? '关闭菜单' : '打开菜单');
      panel.setAttribute('aria-hidden', String(!open));
    };

    toggle.addEventListener('click', () => setOpen(!document.body.classList.contains('menu-open')));
    qsa('a', panel).forEach((link) => link.addEventListener('click', () => setOpen(false)));
    window.addEventListener('resize', () => {
      if (window.innerWidth > 900) setOpen(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') setOpen(false);
    });
  }

  function initFAQ() {
    qsa('.faq-item').forEach((item) => {
      const button = qs('.faq-question', item);
      if (!button) return;
      button.addEventListener('click', () => {
        const open = item.classList.toggle('is-open');
        button.setAttribute('aria-expanded', String(open));
      });
    });
  }

  function initScrollSpy() {
    const nav = qs('[data-scrollspy]');
    const sections = qsa('[data-section]');
    if (!nav || !sections.length || !('IntersectionObserver' in window)) return;

    const links = qsa('a[href^="#"]', nav);
    const canCenterActiveLink = () => {
      const styles = window.getComputedStyle(nav);
      return window.innerWidth <= 900
        && styles.flexWrap !== 'wrap'
        && nav.scrollWidth > nav.clientWidth + 2;
    };
    const setActive = (id) => {
      links.forEach((link) => {
        const active = link.getAttribute('href') === `#${id}`;
        link.classList.toggle('is-active', active);
        if (active && canCenterActiveLink()) {
          link.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        }
      });
    };

    const observer = new IntersectionObserver((entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
      if (visible[0]) setActive(visible[0].target.id);
    }, { rootMargin: '-18% 0px -58% 0px', threshold: [0.05, 0.2, 0.5] });

    sections.forEach((section) => observer.observe(section));
  }

  function initPlaceholderActions() {
    qsa('a[aria-label*="占位"], a[href="#"]').forEach((link) => {
      link.addEventListener('click', (event) => {
        const href = link.getAttribute('href');
        if (href === '#') {
          event.preventDefault();
          createToast('该入口为内容或接口占位，可在上线阶段接入。');
        }
      });
    });

    qsa('.lang-btn').forEach((button) => {
      button.addEventListener('click', () => createToast('语言切换入口已预留；当前原型为中文版本。'));
    });
  }

  function initNavigator() {
    const root = qs('[data-navigator]');
    if (!root) return;

    const form = qs('#navigator-form', root);
    const panels = qsa('.step-panel', root);
    const progressItems = qsa('[data-progress-step]', root);
    const prevButton = qs('[data-prev]', root);
    const nextButton = qs('[data-next]', root);
    const status = qs('[data-action-status]', root);
    const mobileBar = qs('[data-mobile-progress]', root);
    const mobileLabel = qs('[data-mobile-step-label]', root);
    const choiceNote = qs('[data-choice-note]', root);
    const challengeInputs = qsa('input[name="challenge"]', root);
    const goalInputs = qsa('input[name="goal"]', root);

    if (!form || !panels.length || !prevButton || !nextButton) return;

    let currentStep = 1;
    const stepLabels = ['业务挑战', '价值与准备度', '部署偏好', '推荐结果'];

    const checkedValues = (name) => qsa(`input[name="${name}"]:checked`, root).map((input) => input.value);
    const checkedValue = (name) => qs(`input[name="${name}"]:checked`, root)?.value || '';

    function enforceMax(inputs, max, changedInput, message) {
      const checked = inputs.filter((input) => input.checked);
      if (checked.length > max) {
        changedInput.checked = false;
        createToast(message);
      }
    }

    challengeInputs.forEach((input) => {
      input.addEventListener('change', () => {
        enforceMax(challengeInputs, 2, input, '最多选择两个业务挑战。');
        updateValidation();
      });
    });

    goalInputs.forEach((input) => {
      input.addEventListener('change', () => {
        enforceMax(goalInputs, 2, input, '最多选择两个价值目标。');
        updateValidation();
      });
    });

    qsa('input, select', form).forEach((input) => {
      input.addEventListener('change', updateValidation);
    });

    const preselectedChallenge = new URLSearchParams(window.location.search).get('challenge');
    const validChallenge = challengeInputs.find((input) => input.value === preselectedChallenge);
    if (validChallenge) validChallenge.checked = true;

    function isStepValid(step) {
      if (step === 1) return checkedValues('challenge').length >= 1;
      if (step === 2) return checkedValues('goal').length >= 1 && Boolean(checkedValue('readiness'));
      if (step === 3) return Boolean(checkedValue('deployment')) && Boolean(checkedValue('timeline'));
      return true;
    }

    function getStatusText() {
      if (currentStep === 1) {
        const count = checkedValues('challenge').length;
        return count ? `已选择 ${count} 个业务挑战` : '请选择 1–2 个业务挑战';
      }
      if (currentStep === 2) {
        const goals = checkedValues('goal').length;
        const readiness = checkedValue('readiness');
        if (!goals) return '请选择至少一个价值目标';
        if (!readiness) return '请选择组织准备度';
        return '价值目标与准备度已完成';
      }
      if (currentStep === 3) {
        if (!checkedValue('deployment')) return '请选择部署偏好';
        if (!checkedValue('timeline')) return '请选择期望周期';
        return '可以生成推荐结果';
      }
      return '建议已生成，可返回修改或打印导出';
    }

    function updateValidation() {
      const challengeCount = checkedValues('challenge').length;
      if (choiceNote) choiceNote.textContent = `已选择 ${challengeCount} / 2`;
      if (status) status.textContent = getStatusText();
      nextButton.disabled = currentStep < 4 ? !isStepValid(currentStep) : false;
    }

    function updateStepUI({ scroll = false } = {}) {
      panels.forEach((panel) => {
        const active = Number(panel.dataset.step) === currentStep;
        panel.classList.toggle('is-active', active);
        panel.hidden = !active;
      });

      progressItems.forEach((item) => {
        const step = Number(item.dataset.progressStep);
        item.classList.toggle('is-active', step === currentStep);
        item.classList.toggle('is-complete', step < currentStep);
      });

      prevButton.disabled = currentStep === 1;
      if (currentStep === 3) {
        nextButton.innerHTML = '生成建议 <span class="arrow">→</span>';
      } else if (currentStep === 4) {
        nextButton.innerHTML = '打印 / 导出 <span class="arrow">↗</span>';
      } else {
        nextButton.innerHTML = '继续 <span class="arrow">→</span>';
      }

      if (mobileBar) mobileBar.style.width = `${currentStep * 25}%`;
      if (mobileLabel) mobileLabel.textContent = `步骤 ${currentStep} / 4 · ${stepLabels[currentStep - 1]}`;
      updateValidation();

      if (scroll) {
        const workspace = qs('.navigator-workspace', root);
        const top = workspace ? workspace.getBoundingClientRect().top + window.scrollY - 92 : 0;
        window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
      }
    }

    function recommendationData() {
      return [
        {
          id: 'customer-flow',
          title: '客户增长与服务流',
          description: '把客服、线索识别、跟进与推荐串成可追踪的客户旅程。',
          challenges: ['customer'],
          goals: ['revenue', 'experience', 'speed'],
          tags: ['智能客服', '线索管理', '个性化跟进']
        },
        {
          id: 'content-engine',
          title: '营销内容增长引擎',
          description: '从选题、生成、审核、分发到复盘，形成多渠道内容流水线。',
          challenges: ['marketing'],
          goals: ['revenue', 'speed', 'quality'],
          tags: ['内容生成', '渠道适配', '效果复盘']
        },
        {
          id: 'knowledge-copilot',
          title: '企业知识 Copilot',
          description: '连接制度、产品、项目与经验资料，提供可引用、可追溯的知识服务。',
          challenges: ['knowledge', 'hr'],
          goals: ['speed', 'quality', 'experience'],
          tags: ['RAG', '权限检索', '知识运营']
        },
        {
          id: 'ops-flow',
          title: '运营文档与任务流',
          description: '自动识别文档、提取关键信息、触发任务并保留人工审批节点。',
          challenges: ['operations', 'finance'],
          goals: ['speed', 'cost', 'risk'],
          tags: ['文档理解', '流程编排', '人工兜底']
        },
        {
          id: 'finance-insight',
          title: '经营分析与财务洞察流',
          description: '汇总经营数据，生成可核验的报表、异常提示和管理层摘要。',
          challenges: ['finance'],
          goals: ['quality', 'risk', 'speed'],
          tags: ['经营报表', '异常识别', '审计留痕']
        },
        {
          id: 'talent-flow',
          title: '人才发展与组织赋能流',
          description: '覆盖招聘、入职、培训与员工问答，减少重复沟通并加速上手。',
          challenges: ['hr'],
          goals: ['experience', 'speed', 'quality'],
          tags: ['员工助手', '入职培训', '能力陪练']
        },
        {
          id: 'secure-foundation',
          title: '安全 AI 运行底座',
          description: '为敏感数据、复杂集成与审计要求提供统一权限、网关和运行监控。',
          challenges: ['knowledge', 'operations', 'finance'],
          goals: ['risk', 'quality'],
          tags: ['混合部署', '权限治理', '运行监控']
        },
        {
          id: 'scenario-sprint',
          title: 'AI 场景验证冲刺',
          description: '用真实任务在短周期内验证质量、时效和单位经济性，再决定规模化路径。',
          challenges: ['customer', 'marketing', 'knowledge', 'operations', 'finance', 'hr'],
          goals: ['speed', 'cost', 'quality'],
          tags: ['快速试点', '价值评估', '路线图']
        }
      ];
    }

    function generateResults() {
      const challenges = checkedValues('challenge');
      const goals = checkedValues('goal');
      const readiness = checkedValue('readiness');
      const deployment = checkedValue('deployment');
      const timeline = checkedValue('timeline');
      const constraints = checkedValues('constraint');

      const title = qs('[data-result-title]', root);
      const description = qs('[data-result-description]', root);
      const start = qs('[data-result-start]', root);
      const deploymentText = qs('[data-result-deployment]', root);
      const metric = qs('[data-result-metric]', root);
      const list = qs('[data-recommendation-list]', root);

      let route = {
        title: '场景验证冲刺',
        description: '先用一个高价值流程完成短周期价值验证，再决定生产架构与规模化方式。',
        start: readiness === 'idea' ? '流程梳理 + 价值假设' : '真实任务样本 + 基线指标',
        deployment: '云端 / 混合可选',
        metric: '时效 · 质量 · 采用率'
      };

      if (deployment === 'private' || constraints.includes('sensitive') || constraints.includes('audit')) {
        route = {
          title: '安全部署型 AI 流',
          description: '先建立数据边界、权限、审计和人工兜底，再让 AI 进入核心业务流程。',
          start: '数据分级 + 权限与审计设计',
          deployment: deployment === 'private' ? '私有化优先' : '混合部署优先',
          metric: '合规 · 准确率 · 运行稳定性'
        };
      } else if (challenges.some((item) => ['customer', 'marketing'].includes(item)) && goals.includes('revenue')) {
        route = {
          title: '客户增长型 AI 流',
          description: '围绕客户旅程串联触达、内容、服务与跟进，用增长指标驱动迭代。',
          start: '客户旅程 + 转化漏斗基线',
          deployment: deployment === 'cloud' ? '云端快速启动' : '云端 / 混合',
          metric: '转化 · 响应速度 · 客户体验'
        };
      } else if (challenges.includes('knowledge')) {
        route = {
          title: '企业知识型 AI 流',
          description: '把高频问题、制度与经验连接成可引用、可追溯、持续更新的知识服务。',
          start: '知识源盘点 + 高频问题集',
          deployment: deployment === 'cloud' ? '云端知识服务' : '混合知识架构',
          metric: '命中率 · 引用率 · 节省时间'
        };
      } else if (challenges.some((item) => ['operations', 'finance'].includes(item))) {
        route = {
          title: '运营自动化型 AI 流',
          description: '把文档理解、规则判断、任务触发和人工审批放进同一条可监控流程。',
          start: '流程节点 + 文档样本 + 异常清单',
          deployment: deployment === 'cloud' ? '云端集成' : '混合 / 私有化',
          metric: '处理时长 · 错误率 · 自动化率'
        };
      }

      if (title) title.textContent = route.title;
      if (description) description.textContent = route.description;
      if (start) start.textContent = route.start;
      if (deploymentText) deploymentText.textContent = route.deployment;
      if (metric) metric.textContent = route.metric;

      const scored = recommendationData().map((item) => {
        let score = 48;
        score += challenges.filter((challenge) => item.challenges.includes(challenge)).length * 18;
        score += goals.filter((goal) => item.goals.includes(goal)).length * 8;
        if (item.id === 'scenario-sprint' && (readiness === 'idea' || timeline === '30d')) score += 16;
        if (item.id === 'secure-foundation' && (deployment !== 'cloud' || constraints.includes('sensitive') || constraints.includes('audit'))) score += 20;
        if (item.id === 'ops-flow' && constraints.includes('integration')) score += 8;
        if (item.id === 'knowledge-copilot' && constraints.includes('multilingual')) score += 7;
        if (item.id === 'scenario-sprint' && constraints.includes('budget')) score += 7;
        return { ...item, score: Math.min(97, score) };
      }).sort((a, b) => b.score - a.score).slice(0, 3);

      if (list) {
        list.innerHTML = scored.map((item) => `
          <article class="recommendation-card">
            <div class="recommendation-score">${item.score}%</div>
            <div class="recommendation-copy">
              <h4>${item.title}</h4>
              <p>${item.description}</p>
              <div class="micro-tags">${item.tags.map((tag) => `<span>${tag}</span>`).join('')}</div>
            </div>
            <span class="recommendation-slot">DETAIL / CMS SLOT</span>
          </article>
        `).join('');
      }
    }

    nextButton.addEventListener('click', () => {
      if (currentStep === 4) {
        window.print();
        return;
      }
      if (!isStepValid(currentStep)) {
        createToast(getStatusText());
        return;
      }
      if (currentStep === 3) {
        const payload = {};
        const formData = new FormData(form);
        for (const [key, value] of formData.entries()) {
          if (Object.prototype.hasOwnProperty.call(payload, key)) {
            payload[key] = Array.isArray(payload[key]) ? [...payload[key], value] : [payload[key], value];
          } else {
            payload[key] = value;
          }
        }
        ['challenge', 'goal', 'constraint'].forEach((key) => {
          if (!Array.isArray(payload[key])) payload[key] = payload[key] ? [payload[key]] : [];
        });
        try { localStorage.setItem('forflowNavigator', JSON.stringify(payload)); } catch (_) { /* storage can be unavailable */ }
        const params = new URLSearchParams();
        Object.entries(payload).forEach(([key, value]) => {
          if (Array.isArray(value)) value.forEach((item) => params.append(key, item));
          else if (value) params.set(key, value);
        });
        window.location.href = `navigator-results.html?${params.toString()}`;
        return;
      }
      currentStep += 1;
      if (currentStep === 4) generateResults();
      updateStepUI({ scroll: true });
    });

    prevButton.addEventListener('click', () => {
      if (currentStep > 1) {
        currentStep -= 1;
        updateStepUI({ scroll: true });
      }
    });

    updateStepUI();
  }

  function initSearchModal() {
    const modal = qs('[data-search-modal]');
    if (!modal) return;
    const input = qs('input[type="search"]', modal);
    const triggers = qsa('.search-trigger');
    const closeButtons = qsa('[data-search-close]', modal);
    let returnFocus = null;

    const setOpen = (open, trigger = null) => {
      modal.classList.toggle('is-open', open);
      modal.setAttribute('aria-hidden', String(!open));
      document.body.classList.toggle('search-open', open);
      if (open) {
        returnFocus = trigger || document.activeElement;
        document.body.classList.remove('menu-open');
        const menuToggle = qs('.menu-toggle');
        const mobileMenu = qs('.mobile-menu-panel');
        if (menuToggle) menuToggle.setAttribute('aria-expanded', 'false');
        if (mobileMenu) mobileMenu.setAttribute('aria-hidden', 'true');
        window.setTimeout(() => input?.focus(), 80);
      } else if (returnFocus && typeof returnFocus.focus === 'function') {
        returnFocus.focus();
      }
    };

    triggers.forEach((trigger) => trigger.addEventListener('click', () => setOpen(true, trigger)));
    closeButtons.forEach((button) => button.addEventListener('click', () => setOpen(false)));
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && modal.classList.contains('is-open')) setOpen(false);
    });
  }

  function initReveal() {
    const items = qsa('[data-reveal]');
    if (!items.length) return;
    if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      items.forEach((item) => item.classList.add('is-revealed'));
      return;
    }
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-revealed');
        observer.unobserve(entry.target);
      });
    }, { threshold: .12, rootMargin: '0px 0px -8% 0px' });
    items.forEach((item, index) => {
      item.style.transitionDelay = `${Math.min(index % 4, 3) * 55}ms`;
      observer.observe(item);
    });
  }

  function navigatorPayload() {
    const params = new URLSearchParams(window.location.search);
    let stored = {};
    try { stored = JSON.parse(localStorage.getItem('forflowNavigator') || '{}'); } catch (_) { stored = {}; }
    const value = (key) => params.get(key) || stored[key] || '';
    const values = (key) => {
      const fromUrl = params.getAll(key);
      if (fromUrl.length) return fromUrl;
      const fromStore = stored[key];
      return Array.isArray(fromStore) ? fromStore : (fromStore ? [fromStore] : []);
    };
    return {
      challenges: values('challenge'),
      goals: values('goal'),
      constraints: values('constraint'),
      readiness: value('readiness'),
      deployment: value('deployment'),
      timeline: value('timeline'),
      teamSize: value('teamSize'),
      industry: value('industry')
    };
  }

  function initNavigatorResults() {
    const root = qs('.results-page');
    if (!root) return;
    const payload = navigatorPayload();
    const challengeLabels = {
      customer: '客户触达与服务', marketing: '营销与内容增长', knowledge: '企业知识与决策',
      operations: '运营流程自动化', finance: '经营分析与财务', hr: '人才与组织效率'
    };
    const goalLabels = {
      speed: '缩短处理时间', cost: '降低成本', revenue: '增加收入', quality: '提高质量',
      experience: '改善体验', risk: '降低风险'
    };
    const challengeText = payload.challenges.length
      ? payload.challenges.map((item) => challengeLabels[item] || item).join(' · ')
      : '企业知识与运营效率';
    const goalText = payload.goals.length
      ? payload.goals.map((item) => goalLabels[item] || item).join(' · ')
      : '缩短处理时间 · 提高质量';
    const sensitive = payload.deployment === 'private' || payload.constraints.some((item) => ['sensitive', 'audit'].includes(item));
    const startText = payload.timeline === '30d' ? '2 周场景验证' : payload.timeline === 'quarter' ? '4–8 周分阶段试点' : '分阶段路线图';
    const deployText = sensitive ? (payload.deployment === 'private' ? '私有化优先' : '混合部署优先') : payload.deployment === 'cloud' ? '云端快速起步' : '混合部署优先';
    const set = (selector, text) => { const node = qs(selector); if (node) node.textContent = text; };
    set('[data-result-challenge]', challengeText);
    set('[data-result-goal]', goalText);
    set('[data-result-start]', startText);
    set('[data-result-deployment]', deployText);

    const cards = qsa('.solution-card', root);
    const matchScore = (card) => {
      const type = card.dataset.solution;
      let score = 50;
      if (type === 'agent' && payload.challenges.some((item) => ['customer','knowledge','operations','hr'].includes(item))) score += 30;
      if (type === 'data' && payload.challenges.some((item) => ['knowledge','operations','finance'].includes(item))) score += 28;
      if (type === 'enablement' && ['idea','process'].includes(payload.readiness)) score += 25;
      if (type === 'training' && (payload.challenges.includes('hr') || payload.readiness === 'idea')) score += 22;
      if (type === 'data' && sensitive) score += 15;
      if (type === 'agent' && payload.goals.some((item) => ['speed','quality','experience','revenue'].includes(item))) score += 12;
      if (type === 'enablement' && payload.goals.includes('quality')) score += 8;
      if (type === 'training' && payload.goals.includes('risk')) score += 8;
      return score;
    };
    [...cards].sort((a, b) => matchScore(b) - matchScore(a)).forEach((card, index) => {
      card.dataset.rankMatch = String(index + 1);
    });

    const list = qs('.solution-list', root);
    const sortButtons = qsa('[data-sort]', root);
    const mobileSort = qs('.mobile-sort', root);
    const mobileToggle = qs('[data-mobile-sort-toggle]', root);
    const mobileLabel = qs('[data-mobile-sort-toggle] span', root);
    const sortLabels = { match: '最匹配', speed: '最快见效', foundation: '基础优先' };

    const sortCards = (mode) => {
      if (!list) return;
      [...cards]
        .sort((a, b) => Number(a.dataset[`rank${mode[0].toUpperCase()}${mode.slice(1)}`]) - Number(b.dataset[`rank${mode[0].toUpperCase()}${mode.slice(1)}`]))
        .forEach((card, index) => {
          list.appendChild(card);
          const number = qs('.solution-index', card);
          if (number) number.textContent = String(index + 1).padStart(2, '0');
        });
      sortButtons.forEach((button) => button.classList.toggle('is-active', button.dataset.sort === mode));
      if (mobileLabel) mobileLabel.textContent = sortLabels[mode] || sortLabels.match;
      mobileSort?.classList.remove('is-open');
    };
    sortButtons.forEach((button) => button.addEventListener('click', () => sortCards(button.dataset.sort || 'match')));
    mobileToggle?.addEventListener('click', () => mobileSort?.classList.toggle('is-open'));
    sortCards('match');

    qsa('.favorite-btn', root).forEach((button) => {
      const card = button.closest('.solution-card');
      const key = `forflowFavorite:${card?.dataset.solution || 'unknown'}`;
      let active = false;
      try { active = localStorage.getItem(key) === '1'; } catch (_) { active = false; }
      const render = () => {
        button.classList.toggle('is-favorite', active);
        button.textContent = active ? '♥' : '♡';
        button.setAttribute('aria-label', active ? '取消收藏方案' : '收藏方案');
      };
      render();
      button.addEventListener('click', () => {
        active = !active;
        try { localStorage.setItem(key, active ? '1' : '0'); } catch (_) { /* ignore */ }
        render();
        createToast(active ? '已收藏该方案。' : '已取消收藏。');
      });
    });
  }

  function initPlaybookTools() {
    const drawer = qs('[data-toc-drawer]');
    const openButton = qs('[data-toc-open]');
    const closeButton = qs('[data-toc-close]');
    if (!drawer || !openButton) return;
    const setOpen = (open) => {
      drawer.classList.toggle('is-open', open);
      drawer.setAttribute('aria-hidden', String(!open));
      document.body.classList.toggle('search-open', open);
    };
    openButton.addEventListener('click', () => setOpen(true));
    closeButton?.addEventListener('click', () => setOpen(false));
    qsa('a', drawer).forEach((link) => link.addEventListener('click', () => setOpen(false)));
    document.addEventListener('keydown', (event) => { if (event.key === 'Escape') setOpen(false); });
  }

  function initCategoryFilters() {
    const root = qs('.category-page');
    if (!root) return;
    const panel = qs('[data-filter-panel]', root);
    const cards = qsa('.product-card', root);
    const inputs = qsa('[data-category-filter]', root);
    const count = qs('[data-category-count]', root);
    const sort = qs('[data-category-sort]', root);
    const originalOrder = new Map(cards.map((card, index) => [card, index]));

    const selectedForGroup = (group) => qsa('input:checked', group).map((input) => input.value);
    const apply = () => {
      const groups = qsa('.filter-group', root).map(selectedForGroup);
      let visible = 0;
      cards.forEach((card) => {
        const tags = (card.dataset.tags || '').split(/\s+/);
        const show = groups.every((values) => !values.length || values.some((value) => tags.includes(value)));
        card.hidden = !show;
        if (show) visible += 1;
      });
      if (count) count.textContent = String(visible);
    };
    const sortCards = () => {
      const grid = qs('.product-grid', root);
      if (!grid) return;
      const mode = sort?.value || 'recommended';
      [...cards].sort((a, b) => {
        if (mode === 'speed') return Number(a.dataset.speed) - Number(b.dataset.speed);
        if (mode === 'complexity') return Number(a.dataset.complexity) - Number(b.dataset.complexity);
        return originalOrder.get(a) - originalOrder.get(b);
      }).forEach((card) => grid.appendChild(card));
    };
    inputs.forEach((input) => input.addEventListener('change', apply));
    sort?.addEventListener('change', sortCards);
    qs('[data-filter-clear]', root)?.addEventListener('click', () => { inputs.forEach((input) => { input.checked = false; }); apply(); });
    qs('[data-filter-open]', root)?.addEventListener('click', () => panel?.classList.add('is-open'));
    qs('[data-filter-close]', root)?.addEventListener('click', () => panel?.classList.remove('is-open'));
    document.addEventListener('keydown', (event) => { if (event.key === 'Escape') panel?.classList.remove('is-open'); });
    apply();
  }

  function initCaseFilters() {
    const root = qs('.cases-page');
    if (!root) return;
    const buttons = qsa('[data-case-filter]', root);
    const cards = qsa('[data-case-tags]', root);
    buttons.forEach((button) => button.addEventListener('click', () => {
      const filter = button.dataset.caseFilter || 'all';
      buttons.forEach((item) => item.classList.toggle('is-active', item === button));
      cards.forEach((card) => {
        const tags = (card.dataset.caseTags || '').split(/\s+/);
        card.hidden = filter !== 'all' && !tags.includes(filter);
      });
    }));
  }

  function initSearchPage() {
    const root = qs('.search-page');
    if (!root) return;
    const params = new URLSearchParams(window.location.search);
    const query = (params.get('search') || '').trim();
    const input = qs('[data-search-page-input]', root);
    if (input) input.value = query;
    if (query) document.title = `${query} 的搜索结果｜ForFlow 萬維流形`;

    const normalize = (value) => (value || '')
      .normalize('NFKC')
      .toLocaleLowerCase('zh-CN')
      .replace(/&/g, ' and ')
      .replace(/[|/\\·•、，。！？；：:;,()[\]{}<>《》“”"'\-—_]+/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    const compact = (value) => normalize(value).replace(/\s+/g, '');
    const rawTokens = normalize(query).split(/\s+/).filter(Boolean);
    const compactQuery = compact(query);
    const aliasMap = {
      ai: ['人工智能', '生成式', 'genai', '大模型'],
      agent: ['智能体', '代理', 'agentic', '工作流'],
      智能体: ['agent', 'agentic', '代理'],
      dfmea: ['fmea', '失效模式', '本体', 'rflp', 'b柱', 'b 柱', '安全关键'],
      fmea: ['dfmea', '失效模式', '风险分析', 'ap', 'rpn'],
      b柱: ['b 柱', 'b-pillar', 'bpillar', '汽车', '安全关键'],
      汽车: ['b柱', 'b 柱', 'dfmea', 'fmea', '本体', '安全关键'],
      本体: ['ontology', '知识图谱', '工程推理', 'dfmea'],
      pid: ['p&id', 'p id', '管线', '图纸', '工厂'],
      'p&id': ['pid', '管线', '图纸', '工厂'],
      医疗: ['患者', 'ehr', '保险', '预约', 'healthlake', 'aws'],
      数据: ['data', '治理', '指标', '知识库', '报表'],
      培训: ['training', '课程', '角色', '工作坊'],
      playbook: ['手册', '指南', 'genai', '生成式'],
      aws: ['agentcore', 'bedrock', 'strands', 'healthlake'],
      agentcore: ['aws', 'bedrock', 'strands', '智能体运行时'],
      strands: ['agentcore', 'bedrock', 'aws', '智能体']
    };
    const expandedTerms = [...new Set(rawTokens.flatMap((token) => [token, ...(aliasMap[token] || [])]))]
      .filter((token) => token.length > 1 || /^[a-z0-9]+$/i.test(token));
    if (compactQuery && compactQuery.length > 1) expandedTerms.unshift(compactQuery);

    const scoreItem = (item) => {
      if (!query) return Number(item.dataset.searchPriority || 0);
      const title = qs('h3', item)?.textContent || '';
      const summary = qs('p', item)?.textContent || '';
      const meta = qs('small', item)?.textContent || '';
      const keywords = item.dataset.searchText || '';
      const titleNorm = normalize(title);
      const summaryNorm = normalize(summary);
      const metaNorm = normalize(meta);
      const keywordNorm = normalize(keywords);
      const haystack = `${titleNorm} ${summaryNorm} ${metaNorm} ${keywordNorm}`;
      const haystackCompact = compact(haystack);
      let score = 0;
      if (compactQuery && haystackCompact.includes(compactQuery)) score += 70;
      if (compactQuery && compact(title).includes(compactQuery)) score += 110;
      expandedTerms.forEach((term) => {
        const termNorm = normalize(term);
        const termCompact = compact(term);
        if (!termNorm) return;
        if (titleNorm.includes(termNorm) || compact(title).includes(termCompact)) score += 34;
        if (keywordNorm.includes(termNorm) || compact(keywords).includes(termCompact)) score += 22;
        if (summaryNorm.includes(termNorm) || compact(summary).includes(termCompact)) score += 12;
        if (metaNorm.includes(termNorm) || compact(meta).includes(termCompact)) score += 9;
      });
      return score;
    };

    const restoreAndHighlight = (item) => {
      ['small', 'h3', 'p'].forEach((selector) => {
        const node = qs(selector, item);
        if (!node) return;
        if (!node.dataset.originalText) node.dataset.originalText = node.textContent || '';
        node.textContent = node.dataset.originalText;
      });
      if (!query || !expandedTerms.length) return;
      const highlightTerms = [...new Set([query, ...rawTokens])]
        .map((term) => term.trim())
        .filter((term) => term.length >= 2);
      if (!highlightTerms.length) return;
      ['h3', 'p'].forEach((selector) => {
        const node = qs(selector, item);
        if (!node) return;
        const source = node.dataset.originalText || node.textContent || '';
        const fragment = document.createDocumentFragment();
        let remaining = source;
        while (remaining) {
          const match = highlightTerms
            .map((term) => ({ term, index: remaining.toLocaleLowerCase('zh-CN').indexOf(term.toLocaleLowerCase('zh-CN')) }))
            .filter((entry) => entry.index >= 0)
            .sort((a, b) => a.index - b.index || b.term.length - a.term.length)[0];
          if (!match) {
            fragment.append(document.createTextNode(remaining));
            break;
          }
          if (match.index > 0) fragment.append(document.createTextNode(remaining.slice(0, match.index)));
          const mark = document.createElement('mark');
          mark.className = 'search-mark';
          mark.textContent = remaining.slice(match.index, match.index + match.term.length);
          fragment.append(mark);
          remaining = remaining.slice(match.index + match.term.length);
        }
        node.replaceChildren(fragment);
      });
    };

    const groups = qsa('[data-result-type]', root);
    const searchable = qsa('[data-search-text]', root);
    searchable.forEach((item) => {
      const score = scoreItem(item);
      item.dataset.searchScore = String(score);
      item.hidden = Boolean(query) && score <= 0;
      item.classList.toggle('is-top-hit', Boolean(query) && score >= 85);
      restoreAndHighlight(item);
    });

    const typeCounts = {};
    groups.forEach((group) => {
      const items = qsa('[data-search-text]', group);
      items
        .slice()
        .sort((a, b) => Number(b.dataset.searchScore || 0) - Number(a.dataset.searchScore || 0))
        .forEach((item) => item.parentElement?.appendChild(item));
      const type = group.dataset.resultType;
      typeCounts[type] = qsa('[data-search-text]', group).filter((item) => !item.hidden).length;
      const headingCount = qs('.search-result-head h2 span', group);
      if (headingCount) headingCount.textContent = String(typeCounts[type]);
    });
    const total = Object.values(typeCounts).reduce((sum, value) => sum + value, 0);
    setCount('all', total);
    Object.entries(typeCounts).forEach(([type, value]) => setCount(type, value));

    const tabs = qsa('[data-search-tab]', root);
    const empty = qs('[data-search-empty]', root);
    const summary = qs('[data-search-summary]', root);
    const renderTab = (tab) => {
      let visibleGroups = 0;
      groups.forEach((group) => {
        const type = group.dataset.resultType;
        const hasVisible = (typeCounts[type] || 0) > 0;
        const show = hasVisible && (tab === 'all' || tab === type);
        group.hidden = !show;
        if (show) visibleGroups += 1;
      });
      tabs.forEach((button) => button.classList.toggle('is-active', button.dataset.searchTab === tab));
      if (empty) empty.hidden = visibleGroups > 0;
      if (summary) {
        summary.textContent = query
          ? `找到 ${total} 个与“${query}”相关的结果，已按标题、关键词和内容相关度排序。`
          : `当前展示 ${total} 个可检索入口，可输入行业、技术、场景或案例关键词。`;
      }
    };
    function setCount(type, value) {
      const node = qs(`[data-count-${type}]`, root);
      if (node) node.textContent = String(value);
    }
    tabs.forEach((button) => button.addEventListener('click', () => renderTab(button.dataset.searchTab || 'all')));
    renderTab('all');
  }

  function initDocumentViewer() {
    const root = qs('.viewer-page');
    if (!root) return;
    const docs = {
      playbook: { title: '企业生成式 AI 实战手册', file: 'assets/genai-playbook-reference.pdf' },
      solutions: { title: '方案搜索结果参考页面', file: 'assets/explore-digital-solutions.pdf' }
    };
    const key = new URLSearchParams(window.location.search).get('doc') || 'playbook';
    const doc = docs[key] || docs.playbook;
    qsa('[data-doc-title]', root).forEach((node) => { node.textContent = doc.title; });
    qsa('[data-doc-open]', root).forEach((node) => { node.href = doc.file; });
    qsa('[data-doc-download]', root).forEach((node) => { node.href = doc.file; node.setAttribute('download', ''); });
    const frame = qs('[data-doc-frame]', root);
    if (frame) frame.src = `${doc.file}#view=FitH`;
    document.title = `${doc.title}｜ForFlow 萬維流形`;
  }

  function initMegaNav() {
    const root = qs('[data-mega-root]');
    if (!root) return;

    const items = qsa('.mega-item', root);
    let switchTimer = 0;
    let clickedItem = null;

    const clearSwitchState = () => {
      window.clearTimeout(switchTimer);
      items.forEach((item) => {
        item.classList.remove('is-switching-in', 'is-switching-out');
        item.style.removeProperty('--mega-enter-x');
        item.style.removeProperty('--mega-exit-x');
      });
    };

    const closeAll = (except = null, { keepSwitchState = false } = {}) => {
      if (!keepSwitchState) clearSwitchState();
      if (!except) clickedItem = null;
      items.forEach((item) => {
        if (item === except) return;
        item.classList.remove('is-open');
        qs('[data-mega-trigger]', item)?.setAttribute('aria-expanded', 'false');
      });
    };

    const getOpenItem = () => items.find((item) => item.classList.contains('is-open'));

    const openItem = (item, { source = 'hover' } = {}) => {
      const current = getOpenItem();
      if (current === item) {
        if (source === 'click') clickedItem = item;
        return;
      }

      if (current) {
        clearSwitchState();
        const direction = Math.sign(items.indexOf(item) - items.indexOf(current)) || 1;
        current.style.setProperty('--mega-exit-x', `${direction * -14}px`);
        item.style.setProperty('--mega-enter-x', `${direction * 14}px`);
        current.classList.add('is-switching-out');
        item.classList.add('is-switching-in');
        switchTimer = window.setTimeout(clearSwitchState, 340);
      }

      closeAll(item, { keepSwitchState: true });
      item.classList.add('is-open');
      qs('[data-mega-trigger]', item)?.setAttribute('aria-expanded', 'true');
      clickedItem = source === 'click' ? item : null;
    };

    items.forEach((item) => {
      const trigger = qs('[data-mega-trigger]', item);
      const panel = qs('[data-mega-panel]', item);
      if (!trigger || !panel) return;

      trigger.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        const alreadyPinned = item.classList.contains('is-open') && clickedItem === item;
        if (alreadyPinned) {
          closeAll();
        } else {
          openItem(item, { source: 'click' });
        }
      });

      panel.addEventListener('click', (event) => event.stopPropagation());
      qsa('a', panel).forEach((link) => link.addEventListener('click', () => closeAll()));

      if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
        item.addEventListener('mouseenter', () => {
          openItem(item, { source: 'hover' });
        });
      }
    });

    document.addEventListener('click', (event) => {
      if (!root.contains(event.target)) closeAll();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        closeAll();
        qs('[data-mega-trigger]:focus')?.blur();
      }
    });
    window.addEventListener('resize', () => {
      if (window.innerWidth <= 900) closeAll();
    });
  }

  function initPlaybookProgress() {
    const bar = qs('[data-playbook-progress]');
    if (!bar) return;

    const progress = bar.closest('[role="progressbar"]');
    const article = qs('.pb-article');
    let ticking = false;

    const update = () => {
      const start = article ? article.offsetTop : 0;
      const total = article
        ? Math.max(1, article.offsetHeight - window.innerHeight)
        : Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
      const travelled = Math.max(0, window.scrollY - start);
      const percent = Math.max(0, Math.min(100, (travelled / total) * 100));
      bar.style.width = `${percent.toFixed(2)}%`;
      progress?.setAttribute('aria-valuenow', String(Math.round(percent)));
      ticking = false;
    };

    const requestUpdate = () => {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    };

    update();
    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate);
  }

  function initDecisionTool() {
    const root = qs('[data-decision-tool]');
    if (!root) return;

    const groups = qsa('[data-decision-group], fieldset', root);
    const result = qs('[data-decision-result]', root);
    const reset = qs('[data-decision-reset]', root);

    const render = () => {
      const selected = qsa('[data-decision-vote].is-selected', root);
      const buyVotes = selected.filter((button) => button.dataset.decisionVote === 'buy').length;
      const buildVotes = selected.filter((button) => button.dataset.decisionVote === 'build').length;
      const completed = selected.length;

      if (!result) return;
      if (!completed) {
        result.textContent = '完成 5 个问题后，我们会给出购买、建设或组合路线建议。';
        return;
      }

      if (completed < groups.length) {
        const leaning = buyVotes === buildVotes
          ? '两条路线暂时接近'
          : (buyVotes > buildVotes ? '目前更偏向购买成熟方案' : '目前更偏向定制建设');
        result.textContent = `已完成 ${completed} / ${groups.length}：${leaning}。`;
        return;
      }

      if (buildVotes >= 4) {
        result.textContent = '建议以建设为主：先做边界清晰的 4–8 周原型，再按业务指标逐步扩展。';
      } else if (buyVotes >= 4) {
        result.textContent = '建议以购买为主：先用成熟工具小范围试点，并明确数据、权限与退出机制。';
      } else {
        result.textContent = '建议先买后建：先快速建立使用经验，再把差异化流程与数据建设为企业资产。';
      }
    };

    groups.forEach((group) => {
      qsa('[data-decision-vote]', group).forEach((button) => {
        button.setAttribute('aria-pressed', 'false');
        button.addEventListener('click', () => {
          qsa('[data-decision-vote]', group).forEach((item) => {
            const selected = item === button;
            item.classList.toggle('is-selected', selected);
            item.setAttribute('aria-pressed', String(selected));
          });
          render();
        });
      });
    });

    reset?.addEventListener('click', () => {
      qsa('[data-decision-vote]', root).forEach((button) => {
        button.classList.remove('is-selected');
        button.setAttribute('aria-pressed', 'false');
      });
      render();
    });

    render();
  }

  function initVideoBehavior() {
    qsa('video[autoplay]').forEach((video) => {
      const promise = video.play();
      if (promise && typeof promise.catch === 'function') promise.catch(() => { /* controls remain available */ });
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initMenu();
    initMegaNav();
    initFAQ();
    initScrollSpy();
    initPlaceholderActions();
    initNavigator();
    initSearchModal();
    initReveal();
    initNavigatorResults();
    initPlaybookTools();
    initPlaybookProgress();
    initDecisionTool();
    initCategoryFilters();
    initCaseFilters();
    initSearchPage();
    initDocumentViewer();
    initVideoBehavior();
  });
})();
