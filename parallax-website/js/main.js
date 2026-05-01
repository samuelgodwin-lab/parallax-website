// Parallax — Main JS
'use strict';

document.addEventListener('DOMContentLoaded', () => {
  const bgGeometry = document.getElementById('parallax-bg');
  const headline = document.getElementById('parallax-headline');
  const geoCenter = document.getElementById('geo-center');

  // Position SVG geometry group at viewport center
  function positionGeometry() {
    if (!geoCenter) return;
    const cx = window.innerWidth / 2;
    const cy = window.innerHeight / 2;
    geoCenter.setAttribute('transform', `translate(${cx}, ${cy})`);
  }

  positionGeometry();
  window.addEventListener('resize', positionGeometry);

  // Parallax scroll effect
  let ticking = false;

  window.addEventListener('scroll', () => {
    if (ticking) return;

    window.requestAnimationFrame(() => {
      const scrolled = window.scrollY;

      // Background moves at half speed
      if (bgGeometry) {
        bgGeometry.style.transform = `translate3d(0, ${scrolled * 0.5}px, 0)`;
      }

      // Headline fades and drifts up
      if (headline) {
        const opacity = Math.max(0, Math.min(1, 1 - scrolled * 0.003));
        headline.style.opacity = opacity;
        headline.style.transform = `translate3d(0, ${scrolled * -0.15}px, 0)`;
      }

      ticking = false;
    });

    ticking = true;
  });

  // "OR MANY?" mouse-tracking parallax
  const layerMid = document.querySelector('.many-text--mid');
  const layerBack = document.querySelector('.many-text--back');

  if (layerMid && layerBack) {
    document.addEventListener('mousemove', (e) => {
      const xAxis = (window.innerWidth / 2 - e.pageX) / 50;
      const yAxis = (window.innerHeight / 2 - e.pageY) / 50;

      layerMid.style.transform =
        `translate(${10 + xAxis * 0.5}px, ${10 + yAxis * 0.5}px) translateZ(-30px)`;
      layerBack.style.transform =
        `translate(${20 + xAxis}px, ${20 + yAxis}px) translateZ(-60px)`;
    });
  }
});
