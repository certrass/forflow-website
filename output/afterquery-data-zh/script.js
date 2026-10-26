'use strict';

const menuButton = document.querySelector('header button');
const menuPanel = document.getElementById('mobile-menu');
function setMenu(open) {
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? '关闭菜单' : '打开菜单');
  menuPanel.classList.toggle('menu-open', open);
  menuPanel.inert = !open;
  const bars = menuButton.querySelectorAll('span > span');
  bars[0].style.transform = open ? 'translateY(7px) rotate(45deg)' : '';
  bars[1].style.opacity = open ? '0' : '';
  bars[2].style.transform = open ? 'translateY(-7px) rotate(-45deg)' : '';
}
setMenu(false);
menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
menuPanel.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    setMenu(false);
    menuButton.focus();
  }
});

document.addEventListener('click', event => {
  if (!menuPanel.contains(event.target) && !menuButton.contains(event.target)) {
    setMenu(false);
  }
});
window.matchMedia('(min-width: 768px)').addEventListener('change', event => {
  if (event.matches) setMenu(false);
});
