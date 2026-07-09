const fs = require('fs');
const vm = require('vm');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const script = fs.readFileSync(path.join(ROOT, 'script.js'), 'utf8');

function classList() {
  const values = new Set();
  return {
    add: (...items) => items.forEach((item) => values.add(item)),
    remove: (...items) => items.forEach((item) => values.delete(item)),
    toggle: (item, force) => {
      const next = force === undefined ? !values.has(item) : Boolean(force);
      if (next) values.add(item);
      else values.delete(item);
      return next;
    },
    contains: (item) => values.has(item),
  };
}

function element(tagName = 'div') {
  const listeners = {};
  return {
    tagName: tagName.toUpperCase(),
    classList: classList(),
    dataset: {},
    style: {},
    textContent: '',
    value: '',
    disabled: false,
    addEventListener(type, handler) { listeners[type] = handler; },
    dispatchEvent(event) {
      if (listeners[event.type]) listeners[event.type](event);
    },
    setAttribute(name, value) { this[name] = String(value); },
    getAttribute(name) { return this[name] || null; },
    focus() { this.focused = true; },
    select() { this.selected = true; },
    closest() { return null; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
  };
}

function createHarness({ pathname, search = '', storage = {}, nodes = {} }) {
  const domReady = [];
  const localStore = { ...storage };
  const replaced = [];
  const document = {
    documentElement: { classList: classList() },
    body: { classList: classList(), appendChild() {} },
    readyState: 'complete',
    addEventListener(type, handler) {
      if (type === 'DOMContentLoaded') domReady.push(handler);
    },
    createElement: element,
    querySelector(selector) { return nodes[selector] || null; },
    querySelectorAll() { return []; },
  };
  const location = {
    pathname,
    search,
    hash: '',
    replace(url) {
      replaced.push(url);
      const parsed = new URL(url, 'https://forflow.local/');
      location.pathname = parsed.pathname;
      location.search = parsed.search;
      location.hash = parsed.hash;
    },
  };
  const window = {
    location,
    localStorage: {
      getItem(key) { return Object.prototype.hasOwnProperty.call(localStore, key) ? localStore[key] : null; },
      setItem(key, value) { localStore[key] = String(value); },
      removeItem(key) { delete localStore[key]; },
    },
    addEventListener() {},
    setTimeout(handler) { handler(); return 1; },
    clearTimeout() {},
    requestAnimationFrame(handler) { handler(); return 1; },
    matchMedia() { return { matches: false }; },
    innerWidth: 1440,
    URLSearchParams,
    URL,
  };
  const context = {
    window,
    document,
    localStorage: window.localStorage,
    location,
    URLSearchParams,
    URL,
    Event: function Event(type) {
      this.type = type;
      this.preventDefault = () => { this.defaultPrevented = true; };
    },
    FormData: function FormData() { return { entries: () => [] }; },
    IntersectionObserver: function IntersectionObserver() { return { observe() {}, unobserve() {} }; },
    console,
  };
  vm.createContext(context);
  vm.runInContext(script, context, { filename: 'script.js' });
  return {
    context,
    replaced,
    localStore,
    runReady() { domReady.forEach((handler) => handler()); },
  };
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const locked = createHarness({ pathname: '/index.html' });
assert(locked.replaced[0]?.startsWith('landing.html?next='), 'locked visitor should redirect to landing.html');

const now = Date.now();
const unlocked = createHarness({
  pathname: '/index.html',
  storage: {
    forflowInviteAccess: JSON.stringify({ unlockedAt: now, expiresAt: now + 100000 }),
  },
});
assert(unlocked.replaced.length === 0, 'valid invite access should not redirect');

const form = element('form');
const input = element('input');
const status = element('p');
const submit = element('button');
form.querySelector = (selector) => ({
  '[data-invite-code]': input,
  'button[type="submit"]': submit,
}[selector] || null);
const landing = createHarness({
  pathname: '/landing.html',
  search: '?next=index.html',
  nodes: {
    '[data-invite-form]': form,
    '[data-invite-code]': input,
    '[data-invite-status]': status,
    'button[type="submit"]': submit,
  },
});
landing.runReady();
assert(input.focused, 'invite input should focus on landing load');
input.value = 'wrong';
form.dispatchEvent(new landing.context.Event('submit'));
assert(status.dataset.state === 'error', 'wrong invite should show error state');
input.value = 'FLOW2026';
form.dispatchEvent(new landing.context.Event('submit'));
assert(status.dataset.state === 'success', 'valid invite should show success state');
assert(landing.replaced.at(-1) === 'index.html', 'valid invite should redirect to intended page');
assert(JSON.parse(landing.localStore.forflowInviteAccess).expiresAt > Date.now(), 'valid invite should store access expiry');

const unsafeLanding = createHarness({
  pathname: '/landing.html',
  search: '?next=javascript:alert(1)',
  storage: {
    forflowInviteAccess: JSON.stringify({ unlockedAt: now, expiresAt: now + 100000 }),
  },
  nodes: {
    '[data-invite-form]': form,
    '[data-invite-status]': status,
  },
});
unsafeLanding.runReady();
assert(unsafeLanding.replaced.at(-1) === 'index.html', 'unsafe invite destinations should fall back to index.html');

console.log('OK: invite gate redirect, unlock, and form validation paths passed.');
