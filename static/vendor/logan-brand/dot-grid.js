/* Optional dot-grid motion. Redraws the .lb-dot-grid background so dots near the pointer bend away from it and grow darker and larger. */
(() => {
  const root = document.documentElement;
  if (!root.classList.contains('lb-dot-grid')) return;
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');
  if (!context) return;
  const spacing = 20, radius = 140, push = 16;
  const baseSize = 1.25, boldSize = 2.8;
  const pointer = { x: 0, y: 0, active: false }, lens = { x: 0, y: 0, strength: 0 };
  let width = 0, height = 0, rgb = [0, 0, 0], baseAlpha = 0.11, boldAlpha = 0.7, frame = 0;

  const readColor = () => {
    const hex = getComputedStyle(root).getPropertyValue('--lb-ink').trim().replace('#', '');
    rgb = [0, 2, 4].map(i => parseInt(hex.slice(i, i + 2), 16));
    const dark = root.dataset.theme === 'dark';
    baseAlpha = dark ? 0.09 : 0.11;
    boldAlpha = dark ? 0.6 : 0.7;
  };
  const resize = () => {
    const ratio = devicePixelRatio || 1;
    width = innerWidth; height = innerHeight;
    canvas.width = width * ratio; canvas.height = height * ratio;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
  };
  const draw = () => {
    frame = 0;
    lens.x += (pointer.x - lens.x) * 0.2;
    lens.y += (pointer.y - lens.y) * 0.2;
    lens.strength += (Number(pointer.active) - lens.strength) * 0.12;
    context.clearRect(0, 0, width, height);
    const [r, g, b] = rgb;
    const lensDots = [];
    context.fillStyle = `rgba(${r}, ${g}, ${b}, ${baseAlpha})`;
    context.beginPath();
    // Match the CSS background, which centers one dot in each 20px tile of the document.
    const offsetY = -(scrollY % spacing);
    for (let y = offsetY + spacing / 2; y < height + spacing; y += spacing) {
      for (let x = spacing / 2; x < width + spacing; x += spacing) {
        let px = x, py = y;
        const dx = x - lens.x, dy = y - lens.y, distance = Math.hypot(dx, dy);
        if (distance < radius && distance > 0) {
          const t = (1 - distance / radius) ** 2 * lens.strength;
          px += (dx / distance) * t * push;
          py += (dy / distance) * t * push;
          if (t > 0.01) { lensDots.push(px, py, t); continue; }
        }
        context.moveTo(px + baseSize, py);
        context.arc(px, py, baseSize, 0, Math.PI * 2);
      }
    }
    context.fill();
    // Dots in the lens grow and darken with how far they are pushed, so the motion is easy to see.
    for (let i = 0; i < lensDots.length; i += 3) {
      const t = Math.sqrt(lensDots[i + 2]);
      context.fillStyle = `rgba(${r}, ${g}, ${b}, ${baseAlpha + (boldAlpha - baseAlpha) * t})`;
      context.beginPath();
      context.arc(lensDots[i], lensDots[i + 1], baseSize + (boldSize - baseSize) * t, 0, Math.PI * 2);
      context.fill();
    }
    const settling = Math.abs(pointer.x - lens.x) + Math.abs(pointer.y - lens.y) > 0.5
      || Math.abs(Number(pointer.active) - lens.strength) > 0.01;
    if (settling) schedule();
  };
  const schedule = () => { if (!frame) frame = requestAnimationFrame(draw); };

  function init() {
    canvas.className = 'lb-dot-grid-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    document.body.prepend(canvas);
    root.setAttribute('data-lb-dot-grid-live', '');
    addEventListener('pointermove', event => {
      if (lens.strength < 0.01) { lens.x = event.clientX; lens.y = event.clientY; }
      pointer.x = event.clientX; pointer.y = event.clientY; pointer.active = true;
      schedule();
    }, { passive: true });
    root.addEventListener('pointerleave', () => { pointer.active = false; schedule(); });
    addEventListener('scroll', schedule, { passive: true });
    addEventListener('resize', () => { resize(); schedule(); });
    new MutationObserver(() => { readColor(); schedule(); }).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
    readColor(); resize(); schedule();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
