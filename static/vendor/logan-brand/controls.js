/* Optional vanilla controls. Framework apps should own this state themselves. */
(() => {
  const root = document.documentElement;
  const storageKey = 'logan-brand-theme';
  let saved;
  try { saved = localStorage.getItem(storageKey); } catch { /* Storage can be disabled. */ }
  if (saved === 'light' || saved === 'dark') root.dataset.theme = saved;
  if (!['light', 'dark'].includes(root.dataset.theme)) root.dataset.theme = 'light';

  function init() {
    const toggles = document.querySelectorAll('[data-lb-theme-toggle]');
    const syncLabels = () => toggles.forEach(button => {
      button.setAttribute('aria-label', `Switch to ${root.dataset.theme === 'dark' ? 'light' : 'dark'} mode`);
      button.hidden = false;
    });
    toggles.forEach(button => button.addEventListener('click', () => {
      root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(storageKey, root.dataset.theme); } catch { /* Keep the in-memory choice. */ }
      syncLabels();
    }));
    syncLabels();
    document.querySelectorAll('[data-lb-menu-toggle]').forEach(button => {
      const header = button.closest('.lb-header');
      const nav = document.getElementById(button.getAttribute('aria-controls'));
      if (!header || !nav || !header.contains(nav)) return;
      const setOpen = open => {
        header.toggleAttribute('data-menu-open', open);
        button.setAttribute('aria-expanded', String(open));
        button.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      };
      button.hidden = false;
      header.setAttribute('data-lb-enhanced', '');
      setOpen(false);
      button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
      nav.addEventListener('click', event => {
        if (event.target.closest('a[href]')) setOpen(false);
      });
      header.addEventListener('keydown', event => {
        if (event.key === 'Escape' && header.hasAttribute('data-menu-open')) {
          setOpen(false);
          button.focus();
        }
      });
      const mobile = matchMedia('(max-width: 650px)');
      mobile.addEventListener('change', () => {
        if (mobile.matches && nav.contains(document.activeElement)) button.focus();
        setOpen(false);
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
