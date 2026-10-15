const root = document.documentElement;
const button = document.querySelector('.theme');
function setTheme(theme, save = false) {
  const dark = theme === 'dark';
  root.dataset.theme = dark ? 'dark' : 'light';
  const label = dark ? 'Switch to light mode' : 'Switch to dark mode';
  button.setAttribute('aria-label', label);
  button.setAttribute('aria-pressed', String(dark));
  button.title = label;
  document.querySelector('meta[name="theme-color"]').content = getComputedStyle(root).getPropertyValue('--lb-canvas').trim();
  if (save) try { localStorage.setItem('logan-theme', root.dataset.theme); } catch {}
}
setTheme(root.dataset.theme);
button.addEventListener('click', () => setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark', true));

const header = document.querySelector('.header');
const menuButton = document.querySelector('.menu-toggle');
const primaryNav = document.querySelector('#primary-nav');
header.setAttribute('data-lb-enhanced', '');
function setMenu(open) {
  header.toggleAttribute('data-menu-open', open);
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  menuButton.querySelector('path').setAttribute('d', open ? 'M6 6l12 12M6 18 18 6' : 'M4 8h16M4 16h16');
}
menuButton.addEventListener('click', () => setMenu(menuButton.getAttribute('aria-expanded') !== 'true'));
primaryNav.addEventListener('click', (event) => {
  if (event.target.closest('a')) setMenu(false);
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    setMenu(false);
    menuButton.focus();
  }
});
document.addEventListener('click', (event) => {
  if (!header.contains(event.target)) setMenu(false);
});
window.matchMedia('(max-width:650px)').addEventListener('change', event => {
  if (event.matches && primaryNav.contains(document.activeElement)) menuButton.focus();
  setMenu(false);
});
