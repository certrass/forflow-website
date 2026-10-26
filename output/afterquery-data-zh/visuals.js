/* Mount the two captured source canvas modules without the source Next runtime.
 * The shader, logo sampling, positions, colours and motion are the original
 * implementation. This adapter only supplies DOM refs and lifecycle hooks.
 */
(() => {
  'use strict';
  let pendingEffects = [];
  const cleanups = [];
  const react = {
    useRef: value => ({ current: value }),
    useEffect: callback => pendingEffects.push(callback)
  };
  function createElement(type, props) {
    const node = document.createElement(type);
    for (const [key, value] of Object.entries(props || {})) {
      if (key === 'children') {
        for (const child of [value].flat(Infinity)) {
          if (child instanceof Node) node.append(child);
          else if (typeof child === 'string') node.append(document.createTextNode(child));
        }
      } else if (key === 'ref') value.current = node;
      else if (key === 'className') node.className = value;
      else if (key === 'style') Object.assign(node.style, value);
      else if (typeof value !== 'function' && value != null) node.setAttribute(key, value);
    }
    return node;
  }
  const jsx = { jsx: createElement, jsxs: createElement };
  const dependencies = {
    43476: jsx,
    71645: react,
    74080: { preload() {} }
  };
  function load(id) {
    const exports = {};
    const bridge = {
      i: dependency => {
        if (!dependencies[dependency]) throw new Error(`Unknown visual dependency ${dependency}`);
        return dependencies[dependency];
      },
      s: values => {
        for (let index = 0; index < values.length; index += 3) exports[values[index]] = values[index + 2];
      }
    };
    window.afterqueryVisualFactories[id](bridge);
    return exports;
  }
  function mount(component, props, target) {
    pendingEffects = [];
    const node = component(props);
    target.replaceWith(node);
    for (const effect of pendingEffects) {
      const cleanup = effect();
      if (typeof cleanup === 'function') cleanups.push(cleanup);
    }
  }
  const hero = document.getElementById('hero');
  const canvases = hero.querySelectorAll('canvas');
  const fieldTarget = canvases[0].parentElement;
  const logosTarget = canvases[1].parentElement;
  mount(load(13987).HalftoneField, {
    screen: 'lines',
    direction: 'vertical',
    ink: '#64866b',
    ink2: '#06e705',
    className: fieldTarget.className
  }, fieldTarget);
  mount(load(54648).HeroLogos, {}, logosTarget);
  window.addEventListener('pagehide', () => cleanups.forEach(cleanup => cleanup()), { once: true });
})();
