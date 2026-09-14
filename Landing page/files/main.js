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

  /* ── Network drawer ──
     Same behaviour as the pricing drawer on parallaxorg.com, plus the bits a
     dialog needs: focus moves in on open and back to the trigger on close,
     Tab is kept inside, Escape and the scrim close it. The form posts JSON
     to /api/network and swaps itself for the sent state. */
  function initNetwork() {
    var drawer  = document.getElementById('network');
    var scrim   = document.getElementById('net-scrim');
    var opener  = document.getElementById('net-open');
    var closer  = document.getElementById('net-close');
    if (!drawer || !scrim || !opener) return;

    var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]):not([tabindex="-1"]), select:not([disabled]), textarea:not([disabled])';
    var lastFocus = null;
    var open = false;

    function focusables() {
      return Array.prototype.filter.call(drawer.querySelectorAll(FOCUSABLE), function (el) {
        return el.offsetParent !== null;
      });
    }

    function openDrawer() {
      if (open) return;
      open = true;
      lastFocus = document.activeElement;
      scrim.hidden = false;
      drawer.setAttribute('aria-hidden', 'false');
      opener.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
      /* next frame so the transition runs from the off-screen state */
      requestAnimationFrame(function () {
        scrim.classList.add('is-open');
        drawer.classList.add('is-open');
      });
      drawer.scrollTop = 0;
      var delay = reduced.matches ? 0 : 200;
      setTimeout(function () { (closer || focusables()[0]).focus({ preventScroll: true }); }, delay);
    }

    function closeDrawer() {
      if (!open) return;
      open = false;
      scrim.classList.remove('is-open');
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      opener.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
      var delay = reduced.matches ? 0 : 400;
      setTimeout(function () { scrim.hidden = true; }, delay);
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    }

    opener.addEventListener('click', function (e) { e.preventDefault(); openDrawer(); });
    if (closer) closer.addEventListener('click', closeDrawer);
    scrim.addEventListener('click', closeDrawer);
    document.addEventListener('keydown', function (e) {
      if (!open) return;
      if (e.key === 'Escape') { closeDrawer(); return; }
      if (e.key !== 'Tab') return;
      var f = focusables();
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    /* A deep link to #network opens it rather than jumping the page. */
    if (location.hash === '#network') { history.replaceState(null, '', location.pathname + location.search); openDrawer(); }

    /* ── The form ── */
    var form = document.getElementById('net-form');
    if (!form) return;
    var btn = document.getElementById('net-submit');
    var lbl = document.getElementById('net-submit-l');
    var err = document.getElementById('net-err');
    var ok  = document.getElementById('net-ok');
    var RE  = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var fields = {
      name:  { el: document.getElementById('nf-name'),  g: 'ng-name',  ok: function (v) { return !!v; } },
      city:  { el: document.getElementById('nf-city'),  g: 'ng-city',  ok: function (v) { return !!v; } },
      email: { el: document.getElementById('nf-email'), g: 'ng-email', ok: function (v) { return RE.test(v); } },
      disc:  { el: document.getElementById('nf-disc'),  g: 'ng-disc',  ok: function (v) { return !!v; } },
      port:  { el: document.getElementById('nf-port'),  g: 'ng-port',  ok: function (v) { return /^(https?:\/\/)?[^\s]+\.[^\s]{2,}/i.test(v); } }
    };
    function mark(k) {
      var f = fields[k], bad = !f.ok(f.el.value.trim());
      document.getElementById(f.g).classList.toggle('err', bad);
      return !bad;
    }
    Object.keys(fields).forEach(function (k) {
      fields[k].el.addEventListener('blur', function () { mark(k); });
      fields[k].el.addEventListener('input', function () {
        if (document.getElementById(fields[k].g).classList.contains('err')) mark(k);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      err.hidden = true;
      var valid = Object.keys(fields).map(mark).every(Boolean);
      if (!valid) {
        var firstBad = drawer.querySelector('.net-form__g.err .net-form__in');
        if (firstBad) firstBad.focus();
        return;
      }
      btn.disabled = true;
      lbl.textContent = 'Sending…';
      var payload = {};
      new FormData(form).forEach(function (v, k) { payload[k] = v; });

      fetch('/api/network', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(function (res) {
        if (res.ok) return null;
        return res.json().catch(function () { return {}; }).then(function (j) { throw new Error(j.error || ''); });
      }).then(function () {
        form.hidden = true;
        ok.hidden = false;
        ok.querySelector('h3').setAttribute('tabindex', '-1');
        ok.querySelector('h3').focus({ preventScroll: true });
      }).catch(function (ex) {
        btn.disabled = false;
        lbl.textContent = 'Apply to the network';
        err.textContent = (ex && ex.message) || 'Something went wrong. Email projects@parallaxorg.com with your portfolio link and we’ll take it from there.';
        err.hidden = false;
      });
    });
  }

  function init() { initReveal(); initHeroCursor(); initServices(); initCtaCursor(); initClocks(); initNav(); initNetwork(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
