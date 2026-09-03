/* ============================================================
   PARALLAX — Northeast India landing page
   No dependencies. No build step.
   ============================================================ */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ── Scroll reveal ──
     opacity + translateY, unobserve after firing.
     Skipped entirely under prefers-reduced-motion. */
  function initReveal() {
    var targets = document.querySelectorAll('.reveal, .stagger');
    if (!targets.length) return;

    if (reduced.matches || !('IntersectionObserver' in window)) {
      targets.forEach(function (el) { el.classList.add('in'); });
      return;
    }

    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        obs.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });

    targets.forEach(function (el) { io.observe(el); });
  }

  function init() { initReveal(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
