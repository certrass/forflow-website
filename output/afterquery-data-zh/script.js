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
window.matchMedia('(min-width: 1200px)').addEventListener('change', event => {
  if (event.matches) setMenu(false);
});

// Mark the section being read without changing the URL or moving focus.
const sectionLinks = [...document.querySelectorAll('header .section-link')];
const readingSections = [...new Set(sectionLinks.map(link => link.hash))]
  .map(hash => document.querySelector(hash));
let navigationFrame = 0;
function updateReadingPosition() {
  navigationFrame = 0;
  const threshold = document.querySelector('header').getBoundingClientRect().height + 100;
  let current = '';
  for (const section of readingSections) {
    if (section.getBoundingClientRect().top <= threshold) current = '#' + section.id;
  }
  for (const link of sectionLinks) {
    if (link.hash === current) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  }
}
function scheduleReadingPosition() {
  if (!navigationFrame) navigationFrame = requestAnimationFrame(updateReadingPosition);
}
window.addEventListener('scroll', scheduleReadingPosition, { passive: true });
window.addEventListener('resize', scheduleReadingPosition);
window.addEventListener('pageshow', scheduleReadingPosition);
new ResizeObserver(scheduleReadingPosition).observe(document.querySelector('main'));
updateReadingPosition();
