document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.animation-container');
  const images = document.querySelectorAll('.animation-container img');
  const title = document.querySelector('h2');

  if (!container || images.length === 0) return;

  // Store initial state for each image
  const imageStates = Array.from(images).map((img, i) => {
    return {
      element: img,
      index: i,
      initialRotation: 0,
      initialScale: 1,
      rotationSpeed: 0.5 + i * 0.3, // different rotation speeds
      scaleRange: 0.7 + (i % 2) * 0.4, // scale varies by image
      direction: i % 2 === 0 ? 1 : -1, // alternate rotation direction
    };
  });

  function clamp(v, a, b) {
    return Math.max(a, Math.min(b, v));
  }

  // Calculate progress based on element position in viewport
  function getElementProgress(el) {
    const rect = el.getBoundingClientRect();
    const viewportCenter = window.innerHeight / 2;
    const elementCenter = rect.top + rect.height / 2;
    const distance = Math.abs(elementCenter - viewportCenter);
    const maxDistance = window.innerHeight;
    return clamp(1 - distance / maxDistance, 0, 1);
  }

  function updateAnimations() {
    const scrollY = window.scrollY || window.pageYOffset;

    imageStates.forEach((state) => {
      const progress = getElementProgress(state.element);

      // Fade in based on scroll progress
      state.element.style.opacity = clamp(progress * 1.5, 0, 1).toFixed(3);

      // Rotation animation
      const rotation = (scrollY * state.rotationSpeed * state.direction) % 360;

      // Scale animation - pulsing effect combined with scroll progress
      const scaleBase = 0.5 + progress * 0.5; // grows from 0.5 to 1.0 as it enters viewport
      const scalePulse = Math.sin(scrollY * 0.005) * 0.1; // subtle pulsing
      const scale = scaleBase + scalePulse;

      // Position shift based on scroll and progress
      const offsetX = Math.sin(scrollY * 0.002 + state.index) * 15 * progress;
      const offsetY = Math.cos(scrollY * 0.002 + state.index) * 15 * progress;

      state.element.style.transform = `
        translate(${offsetX.toFixed(1)}px, ${offsetY.toFixed(1)}px)
        rotate(${rotation.toFixed(1)}deg)
        scale(${clamp(scale, 0.5, 1.5).toFixed(3)})
      `;
    });

    // Title animation
    if (title) {
      const titleProgress = getElementProgress(title);
      title.style.opacity = clamp(titleProgress, 0, 1).toFixed(3);
    }
  }

  let ticking = false;
  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(() => {
        updateAnimations();
        ticking = false;
      });
    }
  }

  // Wait for images to load
  let loadedCount = 0;
  images.forEach((img) => {
    if (img.complete) {
      loadedCount++;
      if (loadedCount === images.length) {
        updateAnimations(); // Initial render
      }
    } else {
      img.addEventListener('load', () => {
        loadedCount++;
        if (loadedCount === images.length) {
          updateAnimations();
        }
      }, { once: true });
      img.addEventListener('error', () => {
        loadedCount++;
        if (loadedCount === images.length) {
          updateAnimations();
        }
      }, { once: true });
    }
  });

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
});
