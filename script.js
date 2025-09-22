const scene = document.querySelector('.pixel-lab');

if (scene) {
  const updateFlicker = () => {
    const intensity = (Math.random() * 0.12 - 0.06).toFixed(3);
    scene.style.setProperty('--screen-flicker', intensity);
  };

  updateFlicker();
  setInterval(updateFlicker, 180);
}
