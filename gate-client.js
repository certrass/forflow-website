(() => {
  'use strict';

  const root = document.querySelector('[data-gate]');
  if (!root) return;

  const form = root.querySelector('[data-gate-form]');
  const input = root.querySelector('[data-gate-code]');
  const submit = root.querySelector('[data-gate-submit]');
  const status = root.querySelector('[data-gate-status]');
  const params = new URLSearchParams(window.location.search);

  const destination = () => {
    const raw = (params.get('next') || '/').trim();
    if (!raw || /^[a-zA-Z][a-zA-Z\d+.-]*:/.test(raw) || raw.startsWith('//') || raw.startsWith('\\')) return '/';
    try {
      const parsed = new URL(raw, window.location.origin);
      if (parsed.origin !== window.location.origin || /\/landing(?:\.html)?$/.test(parsed.pathname)) return '/';
      return `${parsed.pathname}${parsed.search}${parsed.hash}`;
    } catch (_) {
      return '/';
    }
  };

  const setStatus = (message, state = '') => {
    status.textContent = message;
    status.dataset.state = state;
    input.setAttribute('aria-invalid', String(state === 'error'));
  };

  const setBusy = (busy) => {
    form.setAttribute('aria-busy', String(busy));
    input.disabled = busy;
    submit.disabled = busy;
  };

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const code = input.value.trim();
    if (!code) {
      setStatus('请输入访问码。', 'error');
      input.focus();
      return;
    }

    setBusy(true);
    setStatus('正在验证访问码。');
    try {
      const response = await fetch('/.netlify/functions/gate-login', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.message || '访问码验证失败。');
      setStatus('验证通过，正在进入官网。', 'success');
      window.setTimeout(() => window.location.replace(destination()), 180);
    } catch (error) {
      setStatus(error.message || '暂时无法验证，请稍后重试。', 'error');
      input.select();
    } finally {
      setBusy(false);
    }
  });

  input.addEventListener('input', () => {
    if (status.dataset.state === 'error') setStatus('访问码由 ForFlow 团队提供。');
  });

  if (window.matchMedia?.('(hover: hover) and (pointer: fine)').matches) input.focus();
})();
