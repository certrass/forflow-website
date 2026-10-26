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

const moreButton = document.querySelector('[aria-controls="faq-more"]');
const morePanel = document.getElementById('faq-more');
moreButton.addEventListener('click', () => {
  const expanded = moreButton.getAttribute('aria-expanded') !== 'true';
  moreButton.setAttribute('aria-expanded', String(expanded));
  moreButton.querySelector('span').textContent = expanded ? '收起问题' : '查看更多';
  morePanel.classList.toggle('is-expanded', expanded);
  morePanel.inert = !expanded;
  morePanel.setAttribute('aria-hidden', String(!expanded));
});
