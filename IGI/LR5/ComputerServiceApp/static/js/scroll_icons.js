// static/js/scroll_parallax.js — final version: parallax + fade-in
document.addEventListener('DOMContentLoaded', () => {
  const root = document.getElementById('top');
  if (!root) return;

  const layers = {
    bg: document.getElementById('layer-bg'),
    mountainLeft: document.getElementById('layer-mountain-left'),
    mountainRight: document.getElementById('layer-mountain-right'),
    cloud1: document.getElementById('layer-cloud-1'),
    cloud2: document.getElementById('layer-cloud-2'),
    hero: document.getElementById('layer-hero'),
    title: document.getElementById('layer-title')
  };

  const config = {
    bg:           { parallaxY: 0.05,  scaleMax: 1.04, fade: false },
    mountainLeft: { parallaxX: -0.12, scaleMax: 1.02, fade:false },
    mountainRight:{ parallaxX:  0.12, scaleMax: 1.02, fade:false },
    cloud1:       { parallaxX:  0.18, rotateMax: 6,  fade: true },
    cloud2:       { parallaxX: -0.20, rotateMax: -8, fade: true },
    hero:         { parallaxY: -0.06, scaleMax: 1.12, rotateFactor: 0.15, fade: true },
    title:        { parallaxY: -0.25, fade: true }
  };

  // prepare
  Object.values(layers).forEach(el => { if (el) el.style.willChange = 'transform, opacity'; });

  function clamp(v,a,b){ return Math.max(a, Math.min(b, v)); }

  // utility: progress 0..1 depending on element center distance to viewport center
  function progressFor(el){
    const winCenter = window.innerHeight / 2;
    const limit = Math.max(window.innerHeight * 0.5, 200);
    const r = el.getBoundingClientRect();
    const center = r.top + r.height / 2;
    const d = center - winCenter;
    const norm = clamp(d / limit, -1, 1);
    return 1 - Math.abs(norm); // 1 center, 0 edges
  }

  let ticking = false;
  function rafUpdate(){
    ticking = false;
    const rect = root.getBoundingClientRect();
    if (rect.bottom <= 0 || rect.top >= window.innerHeight) return; // секция не видна

    const sc = window.scrollY || window.pageYOffset;

    // BG
    if (layers.bg){
      const p = config.bg.parallaxY;
      const prog = progressFor(layers.bg);
      const scale = 1 + (config.bg.scaleMax - 1) * prog;
      layers.bg.style.transform = `translate3d(0, ${sc * p}px, 0) scale(${scale.toFixed(3)})`;
      if (config.bg.fade) layers.bg.style.opacity = `${clamp(0.06 + prog, 0, 1).toFixed(3)}`;
      else layers.bg.style.opacity = '';
    }

    // Mountains
    ['mountainLeft','mountainRight'].forEach(key => {
      const el = layers[key];
      if (!el) return;
      const c = config[key];
      const prog = progressFor(el);
      const tx = (sc * (c.parallaxX || 0)).toFixed(1);
      const scale = (1 + (c.scaleMax - 1) * prog).toFixed(3);
      el.style.transform = `translate3d(${tx}px,0,0) scale(${scale})`;
      if (c.fade) el.style.opacity = `${clamp(0.06 + prog,0,1).toFixed(3)}`; else el.style.opacity = '';
    });

    // Clouds
    ['cloud1','cloud2'].forEach((key, i) => {
      const el = layers[key];
      if (!el) return;
      const c = config[key];
      const prog = progressFor(el);
      const tx = (sc * (c.parallaxX || 0)).toFixed(1);
      const rotate = ((1 - prog) * (c.rotateMax || 0)).toFixed(2);
      const ty = (-(1 - prog) * 12).toFixed(1);
      el.style.transform = `translate3d(${tx}px, ${ty}px, 0) rotate(${rotate}deg)`;
      if (c.fade) el.style.opacity = `${clamp(0.06 + prog,0,1).toFixed(3)}`; else el.style.opacity = '';
    });

    // Hero (monitor): rise, rotation by scroll, scale and fade
    if (layers.hero){
      const c = config.hero;
      const prog = progressFor(layers.hero);
      const ty = (-(sc * (c.parallaxY || 0))).toFixed(1);
      const scale = (1 + (c.scaleMax - 1) * prog).toFixed(3);
      const rotate = (sc * (c.rotateFactor || 0)).toFixed(2);
      layers.hero.style.transform = `translate3d(0, ${ty}px, 0) rotate(${rotate}deg) scale(${scale})`;
      if (c.fade) layers.hero.style.opacity = `${clamp(0.06 + prog,0,1).toFixed(3)}`; else layers.hero.style.opacity = '';
    }

    // Title: vertical shift and fade
    if (layers.title){
      const c = config.title;
      const prog = progressFor(layers.title);
      const ty = (sc * (c.parallaxY || 0)).toFixed(1);
      layers.title.style.transform = `translate3d(-50%, ${ty}px, 0)`;
      if (c.fade) layers.title.style.opacity = `${clamp(0.06 + prog,0,1).toFixed(3)}`; else layers.title.style.opacity = '';
    }
  }

  function onScroll(){
    if (!ticking){
      ticking = true;
      window.requestAnimationFrame(rafUpdate);
    }
  }

  // wait images loaded then init one frame
  const imgs = Array.from(root.querySelectorAll('img'));
  let loaded = 0;
  if (imgs.length === 0) onScroll();
  else {
    imgs.forEach(img => {
      if (img.complete) {
        loaded++;
        if (loaded === imgs.length) onScroll();
      } else {
        img.addEventListener('load', () => { loaded++; if (loaded === imgs.length) onScroll(); }, { once:true });
        img.addEventListener('error', () => { loaded++; if (loaded === imgs.length) onScroll(); }, { once:true });
      }
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll, { passive: true });
});
