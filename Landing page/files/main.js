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

  /* ── Hero cursor colour-reveal ──
     Copied from parallaxorg.com. Writes the pointer position as a percentage
     into --hx/--hy; the radial gradient in .hero__cursor-fx::after reads them.
     Desktop pointers only — the CSS hides the layer under 768px anyway. */
  function initHeroCursor() {
    var hero = document.querySelector('.hero');
    if (!hero) return;
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    hero.addEventListener('mousemove', function (e) {
      var r = hero.getBoundingClientRect();
      var x = ((e.clientX - r.left) / r.width * 100).toFixed(1);
      var y = ((e.clientY - r.top) / r.height * 100).toFixed(1);
      hero.style.setProperty('--hx', x + '%');
      hero.style.setProperty('--hy', y + '%');
    });
    hero.addEventListener('mouseleave', function () {
      hero.style.setProperty('--hx', '85%');
      hero.style.setProperty('--hy', '50%');
    });
  }

  /* ── Services accordion ──
     Copied from parallaxorg.com: one item open at a time, height animated by
     grid-template-rows. The live rows are click-only divs; these also answer
     Enter/Space and keep aria-expanded in sync. */
  function initServices() {
    var items = document.querySelectorAll('[data-svc]');
    if (!items.length) return;

    function toggle(item) {
      var isOpen = item.classList.contains('open');
      items.forEach(function (s) {
        s.classList.remove('open');
        s.setAttribute('aria-expanded', 'false');
      });
      if (!isOpen) {
        item.classList.add('open');
        item.setAttribute('aria-expanded', 'true');
      }
    }

    items.forEach(function (item) {
      item.addEventListener('click', function () { toggle(item); });
      item.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
          e.preventDefault();
          toggle(item);
        }
      });
    });
  }

  /* ── CTA cursor FX ──
     Copied from parallaxorg.com's "Work With Us" section. Same contract as the
     hero: pointer position as a percentage, read by the mask and the radial. */
  function initCtaCursor() {
    var contact = document.querySelector('.contact');
    if (!contact) return;
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    contact.addEventListener('mousemove', function (e) {
      var r = contact.getBoundingClientRect();
      var x = ((e.clientX - r.left) / r.width * 100).toFixed(1);
      var y = ((e.clientY - r.top) / r.height * 100).toFixed(1);
      contact.style.setProperty('--cx', x + '%');
      contact.style.setProperty('--cy', y + '%');
    });
    contact.addEventListener('mouseleave', function () {
      contact.style.setProperty('--cx', '50%');
      contact.style.setProperty('--cy', '50%');
    });
  }

  /* ── Market clocks ──
     Every element carrying data-tz gets its local time, so the map pins and
     the list stay in sync and a new market needs no JS change at all. Times
     come from the visitor's own clock via toLocaleTimeString + timeZone. */
  function initClocks() {
    var els = document.querySelectorAll('[data-tz]');
    if (!els.length) return;

    function fmt(tz) {
      return new Date().toLocaleTimeString('en-GB', {
        timeZone: tz,
        hour: '2-digit', minute: '2-digit',
        hour12: false
      });
    }

    function tick() {
      els.forEach(function (el) {
        var out = el.matches('.mk__time') ? el : el.querySelector('.mk__time');
        if (!out) return;
        var t = fmt(el.getAttribute('data-tz'));
        if (out.textContent !== t) {
          out.textContent = t;
          out.classList.add('tick');
          setTimeout(function () { out.classList.remove('tick'); }, 700);
        }
      });
    }

    tick();
    setInterval(tick, 1000);
  }

  /* ── Nav frosting ──
     Copied from parallaxorg.com: the nav is transparent over the hero and
     frosts once you are past 40px, so it stays readable over whatever is
     scrolling under it. Passive listener — this never blocks scrolling. */
  function initNav() {
    var nav = document.querySelector('.nav');
    if (!nav) return;

    function sync() { nav.classList.toggle('scrolled', window.scrollY > 40); }
    sync();
    window.addEventListener('scroll', sync, { passive: true });
    /* A deep link to #cta jumps the page before this can run, and an in-page
       anchor jump does not always fire scroll — resync on both so the nav is
       never left transparent halfway down the page. */
    window.addEventListener('load', sync);
    window.addEventListener('hashchange', sync);
  }

  function init() { initReveal(); initHeroCursor(); initServices(); initCtaCursor(); initClocks(); initNav(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
