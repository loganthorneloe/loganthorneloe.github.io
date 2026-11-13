/* Optional dot-grid canvas. Bends dots around the pointer and fades them smoothly around unboxed foreground text. */
(() => {
  const root = document.documentElement;
  if (!root.classList.contains('lb-dot-grid')) return;
  if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');
  if (!context) return;
  const motionQuery = matchMedia('(prefers-reduced-motion: reduce)');
  const spacing = 20, radius = 140, push = 16;
  const baseSize = 1.25, boldSize = 2.8;
  const textInner = 7, textOuter = 28, textInnerSq = textInner * textInner, textOuterSq = textOuter * textOuter;
  const skipTags = new Set(['CANVAS', 'SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE', 'SVG', 'DIALOG']);
  const pointer = { x: 0, y: 0, active: false }, lens = { x: 0, y: 0, strength: 0 };
  let width = 0, height = 0, rgb = [0, 0, 0], baseAlpha = 0.11, boldAlpha = 0.7, frame = 0;
  let textRects = [], measureDirty = true;
  const range = document.createRange();

  const isOpaqueSurface = bg => {
    if (!bg || bg === 'transparent') return false;
    const alpha = bg.includes('/') ? parseFloat(bg.split('/')[1])
      : bg.startsWith('rgba(') ? parseFloat(bg.split(',')[3]) : 1;
    return !(alpha < 0.5);
  };
  const measureText = () => {
    const rects = [];
    if (!document.body) { textRects = rects; return; }
    const sx = scrollX, sy = scrollY;
    const walk = el => {
      if (skipTags.has(el.tagName)) return;
      const style = getComputedStyle(el);
      if (style.display === 'none' || style.visibility === 'hidden' || style.position === 'fixed' || parseFloat(style.opacity) === 0) return;
      if ((style.overflow === 'hidden' && el.offsetWidth <= 2 && el.offsetHeight <= 2)
          || style.clip === 'rect(0px, 0px, 0px, 0px)' || style.clipPath === 'inset(50%)') return;
      if (isOpaqueSurface(style.backgroundColor)) return;
      if (el.tagName === 'LI' && el.parentElement?.classList.contains('lb-list')) {
        const r = el.getBoundingClientRect();
        const fs = parseFloat(style.fontSize) || 16;
        if (r.width > 0.5 && r.height > 0.5) {
          rects.push({ l: r.left + sx, t: r.top + sy + 2, r: r.left + sx + fs * 1.6, b: r.top + sy + fs * 1.5 });
        }
      }
      for (let child = el.firstChild; child; child = child.nextSibling) {
        if (child.nodeType === 3) {
          if (!child.nodeValue.trim()) continue;
          range.selectNodeContents(child);
          for (const r of range.getClientRects()) {
            if (r.width > 0.5 && r.height > 0.5) {
              rects.push({ l: r.left + sx, t: r.top + sy, r: r.right + sx, b: r.bottom + sy });
            }
          }
        } else if (child.nodeType === 1) {
          if (child.tagName === 'IMG') {
            const s = getComputedStyle(child);
            if (s.display !== 'none' && s.visibility !== 'hidden') {
              const r = child.getBoundingClientRect();
              if (r.width > 0.5 && r.height > 0.5) {
                rects.push({ l: r.left + sx, t: r.top + sy, r: r.right + sx, b: r.bottom + sy });
              }
            }
          } else {
            walk(child);
          }
        }
      }
    };
    walk(document.body);
    range.selectNode(document.body);
    range.collapse(true);
    textRects = rects;
  };
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
    measureDirty = true;
  };
  const draw = () => {
    frame = 0;
    if (measureDirty) { measureText(); measureDirty = false; }
    const allowMotion = !motionQuery.matches;
    const targetStrength = allowMotion ? Number(pointer.active) : 0;
    if (allowMotion) {
      lens.x += (pointer.x - lens.x) * 0.2;
      lens.y += (pointer.y - lens.y) * 0.2;
      lens.strength += (targetStrength - lens.strength) * 0.12;
    } else {
      lens.strength = 0;
    }
    context.clearRect(0, 0, width, height);
    const sx = scrollX, sy = scrollY;
    const activeRects = [];
    let uMinX = Infinity, uMinY = Infinity, uMaxX = -Infinity, uMaxY = -Infinity;
    for (let i = 0; i < textRects.length; i++) {
      const tr = textRects[i];
      const l = tr.l - sx, r = tr.r - sx, vt = tr.t - sy, vb = tr.b - sy;
      if (vb + textOuter < 0 || vt - textOuter > height || r + textOuter < 0 || l - textOuter > width) continue;
      const exL = l - textOuter, exT = vt - textOuter, exR = r + textOuter, exB = vb + textOuter;
      activeRects.push(l, vt, r, vb, exL, exT, exR, exB);
      if (exL < uMinX) uMinX = exL;
      if (exT < uMinY) uMinY = exT;
      if (exR > uMaxX) uMaxX = exR;
      if (exB > uMaxY) uMaxY = exB;
    }
    const visibilityAt = (px, py) => {
      if (px <= uMinX || px >= uMaxX || py <= uMinY || py >= uMaxY) return 1;
      let minSq = textOuterSq;
      for (let i = 0; i < activeRects.length; i += 8) {
        if (px <= activeRects[i + 4] || px >= activeRects[i + 6] || py <= activeRects[i + 5] || py >= activeRects[i + 7]) continue;
        const dx = px < activeRects[i] ? activeRects[i] - px : px > activeRects[i + 2] ? px - activeRects[i + 2] : 0;
        const dy = py < activeRects[i + 1] ? activeRects[i + 1] - py : py > activeRects[i + 3] ? py - activeRects[i + 3] : 0;
        const dSq = dx * dx + dy * dy;
        if (dSq <= textInnerSq) return 0;
        if (dSq < minSq) minSq = dSq;
      }
      if (minSq >= textOuterSq) return 1;
      const u = (Math.sqrt(minSq) - textInner) / (textOuter - textInner);
      return u * u * (3 - 2 * u);
    };

    const [r, g, b] = rgb;
    const specialDots = [];
    context.fillStyle = `rgba(${r}, ${g}, ${b}, ${baseAlpha})`;
    context.beginPath();
    // Match the CSS background, which centers one dot in each 20px tile of the document.
    const offsetY = -(sy % spacing);
    for (let y = offsetY + spacing / 2; y < height + spacing; y += spacing) {
      for (let x = spacing / 2; x < width + spacing; x += spacing) {
        let px = x, py = y, lensT = 0;
        if (lens.strength > 0.001) {
          const dx = x - lens.x, dy = y - lens.y, distance = Math.hypot(dx, dy);
          if (distance < radius && distance > 0) {
            lensT = (1 - distance / radius) ** 2 * lens.strength;
            px += (dx / distance) * lensT * push;
            py += (dy / distance) * lensT * push;
          }
        }
        const vis = visibilityAt(px, py);
        if (vis <= 0.01) continue;
        if (lensT > 0.01 || vis < 0.995) {
          specialDots.push(px, py, lensT, vis);
          continue;
        }
        context.moveTo(px + baseSize, py);
        context.arc(px, py, baseSize, 0, Math.PI * 2);
      }
    }
    context.fill();
    // Feathered dots near text soften smoothly; lens dots grow and darken in open space.
    for (let i = 0; i < specialDots.length; i += 4) {
      const vis = specialDots[i + 3];
      const t = Math.sqrt(specialDots[i + 2]) * vis;
      const alpha = (baseAlpha + (boldAlpha - baseAlpha) * t) * vis;
      const size = (baseSize + (boldSize - baseSize) * t) * (0.7 + 0.3 * vis);
      context.fillStyle = `rgba(${r}, ${g}, ${b}, ${alpha})`;
      context.beginPath();
      context.arc(specialDots[i], specialDots[i + 1], size, 0, Math.PI * 2);
      context.fill();
    }
    const settling = allowMotion && (Math.abs(pointer.x - lens.x) + Math.abs(pointer.y - lens.y) > 0.5
      || Math.abs(targetStrength - lens.strength) > 0.01);
    if (settling) schedule();
  };
  const schedule = () => { if (!frame) frame = requestAnimationFrame(draw); };
  const markDirty = () => { measureDirty = true; schedule(); };

  function init() {
    canvas.className = 'lb-dot-grid-canvas';
    canvas.setAttribute('aria-hidden', 'true');
    document.body.prepend(canvas);
    root.setAttribute('data-lb-dot-grid-live', '');
    addEventListener('pointermove', event => {
      if (motionQuery.matches) return;
      if (lens.strength < 0.01) { lens.x = event.clientX; lens.y = event.clientY; }
      pointer.x = event.clientX; pointer.y = event.clientY; pointer.active = true;
      schedule();
    }, { passive: true });
    root.addEventListener('pointerleave', () => { pointer.active = false; schedule(); });
    motionQuery.addEventListener('change', () => { pointer.active = false; schedule(); });
    addEventListener('scroll', schedule, { passive: true });
    addEventListener('resize', () => { resize(); schedule(); });
    if (typeof ResizeObserver !== 'undefined') new ResizeObserver(markDirty).observe(document.body);
    new MutationObserver(mutations => {
      if (mutations.some(m => m.target !== canvas)) markDirty();
    }).observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ['hidden', 'open', 'class', 'style'] });
    new MutationObserver(() => { readColor(); schedule(); }).observe(root, { attributes: true, attributeFilter: ['data-theme'] });
    document.fonts?.ready.then(markDirty);
    readColor(); resize(); schedule();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
