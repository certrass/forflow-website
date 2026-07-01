(() => {
  'use strict';
  const qs = (selector, root = document) => root.querySelector(selector);
  const qsa = (selector, root = document) => [...root.querySelectorAll(selector)];

  const PLAN_COPY = {
    explore: ['探索版', '适合一个团队建立共同认知，验证 1–2 个低风险场景。'],
    team: ['协同版', '适合多角色共同试点，把知识、流程、审核和效果指标放在一起。'],
    enterprise: ['企业版', '适合多部门、敏感数据和关键流程，需要更强控制、集成与运营支持。'],
    audit: ['人工智能准备度审核', '从六个维度形成当前状态、机会地图、快速收益与 30/90 天路线图。'],
    enablement: ['企业 AI 赋能计划', '把个人零散试用变成统一方法、真实任务和可衡量采用。'],
    data: ['数据治理', '建立可信数据、知识、权限、质量和面向 AI 的访问基础。'],
    agent: ['企业 Agent 搭建', '验证并建设连接知识、系统、规则与人工审批的受控工作流。'],
    training: ['企业 AI 培训', '为管理层、业务和技术团队建立共同语言与岗位实战能力。']
  };

  function initAuditCheck() {
    const root = qs('[data-audit-check]');
    if (!root) return;
    const questions = qsa('[data-audit-question]', root);
    const progress = qs('[data-audit-progress]', root);
    const progressBox = progress?.closest('[role="progressbar"]');
    const count = qs('[data-audit-count]', root);
    const result = qs('[data-audit-result]', root);

    const render = () => {
      const selected = questions
        .map((question) => qs('input:checked', question))
        .filter(Boolean);
      const completed = selected.length;
      const score = selected.reduce((sum, input) => sum + Number(input.value || 0), 0);
      const percent = questions.length ? (completed / questions.length) * 100 : 0;
      if (progress) progress.style.width = `${percent}%`;
      progressBox?.setAttribute('aria-valuenow', String(completed));
      if (count) count.textContent = `已完成 ${completed} / ${questions.length}`;
      if (!result) return;

      const heading = qs('h3', result);
      const paragraph = qs('p', result);
      if (completed < questions.length) {
        if (heading) heading.textContent = completed ? `还差 ${questions.length - completed} 个问题。` : '完成 6 个问题后显示建议。';
        if (paragraph) paragraph.textContent = '正式审核会结合访谈、材料、流程和样本进一步验证。';
        result.dataset.stage = 'pending';
        return;
      }
      if (score <= 4) {
        result.dataset.stage = 'explore';
        if (heading) heading.textContent = '探索期：先把业务问题与责任边界说清楚。';
        if (paragraph) paragraph.textContent = '优先确认 1 个高价值流程、当前基线、可用数据和不可接受的风险，再考虑工具或平台。';
      } else if (score <= 8) {
        result.dataset.stage = 'pilot';
        if (heading) heading.textContent = '试点期：具备启动受控验证的基础。';
        if (paragraph) paragraph.textContent = '建议选择 1 个可人工复核的场景，在 2–6 周内验证质量、时效、采用与运行边界。';
      } else {
        result.dataset.stage = 'scale';
        if (heading) heading.textContent = '规模化准备期：重点转向治理、集成与运营。';
        if (paragraph) paragraph.textContent = '建议统一权限、审计、指标、知识更新和跨部门责任，再扩大场景与组织范围。';
      }
    };

    qsa('input[type="radio"]', root).forEach((input) => input.addEventListener('change', render));
    render();
  }

  function planFromUrl() {
    const source = window.location.search || document.body?.dataset.testQuery || '';
    return new URLSearchParams(source).get('plan') || '';
  }

  function initPurchasePage() {
    const select = qs('[data-purchase-select]');
    const title = qs('[data-purchase-plan]');
    const description = qs('[data-purchase-description]');
    if (!select && !title) return;

    const update = (value) => {
      const copy = PLAN_COPY[value] || ['方案咨询', '先描述业务目标与边界，我们会建议合适的版本或专项服务。'];
      if (title) title.textContent = copy[0];
      if (description) description.textContent = copy[1];
      if (select && [...select.options].some((option) => option.value === value)) select.value = value;
    };
    update(planFromUrl());
    select?.addEventListener('change', () => update(select.value));
  }

  function initFileInputs() {
    qsa('[data-file-input]').forEach((input) => {
      const label = input.closest('label');
      const target = qs('[data-file-label]', label || document);
      input.addEventListener('change', () => {
        if (!target) return;
        const file = input.files?.[0];
        target.textContent = file ? file.name : '可选：上传现状说明、流程图或需求文档';
      });
    });
  }

  function validateIntent(form) {
    const choices = qsa('input[name="interest"]', form);
    if (!choices.length) return true;
    const valid = choices.some((input) => input.checked);
    const fieldset = choices[0].closest('fieldset');
    fieldset?.classList.toggle('has-error', !valid);
    return valid;
  }

  function initInquiryForms() {
    qsa('[data-inquiry-form]').forEach((form) => {
      const status = qs('[data-form-status]', form);
      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const intentValid = validateIntent(form);
        if (!form.checkValidity() || !intentValid) {
          form.reportValidity();
          if (status) status.textContent = intentValid ? '请完成必填字段。' : '请至少选择一个希望讨论的方向。';
          return;
        }

        const submit = qs('button[type="submit"]', form);
        submit?.setAttribute('disabled', '');
        if (status) status.textContent = '正在处理…';
        const endpoint = form.dataset.endpoint || '';
        const data = new FormData(form);
        data.set('source_page', window.location.pathname.split('/').pop() || 'index.html');
        data.set('submitted_at', new Date().toISOString());

        try {
          if (endpoint) {
            const response = await fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            if (status) status.textContent = '已提交。项目顾问会通过你填写的工作邮箱联系。';
            form.reset();
          } else {
            const draft = {};
            for (const [key, value] of data.entries()) {
              if (value instanceof File) {
                if (value.name) draft[key] = { name: value.name, size: value.size, type: value.type };
              } else if (Object.prototype.hasOwnProperty.call(draft, key)) {
                draft[key] = Array.isArray(draft[key]) ? [...draft[key], value] : [draft[key], value];
              } else {
                draft[key] = value;
              }
            }
            try { localStorage.setItem(`forflow:${form.dataset.formKind || 'inquiry'}:draft`, JSON.stringify(draft)); } catch (_) { /* storage can be blocked */ }
            if (status) status.textContent = '原型已保存本次填写内容；上线时接入 CRM / Webhook 后即可真实发送。';
          }
        } catch (error) {
          if (status) status.textContent = '暂时无法提交，请稍后重试或使用“联系我们”入口。';
        } finally {
          submit?.removeAttribute('disabled');
        }
      });
      qsa('input[name="interest"]', form).forEach((input) => input.addEventListener('change', () => validateIntent(form)));
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initAuditCheck();
    initPurchasePage();
    initFileInputs();
    initInquiryForms();
  });
})();
