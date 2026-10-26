'use strict';

const toggle = document.querySelector('.menu-toggle');
const menu = document.getElementById('data-menu');
function setDataMenu(open) {
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? '关闭菜单' : '打开菜单');
  menu.hidden = !open;
}
toggle.addEventListener('click', () => setDataMenu(toggle.getAttribute('aria-expanded') !== 'true'));
menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setDataMenu(false)));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !menu.hidden) {
    setDataMenu(false);
    toggle.focus();
  }
});
