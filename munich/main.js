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
  /* Accordion: one open at a time within a group. Used by What We Build
     ([data-svc]) and the perks list in the network drawer ([data-perk]). */
  function initAccordion(selector) {
    var items = document.querySelectorAll(selector);
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

  /* ── Pricing cards + plan drawer ──
     Same behaviour as the pricing cards on parallaxorg.com: the whole card
     opens a drawer with the full inclusions, and a radial glow tracks the
     pointer inside the card (--gx / --gy). The drawer is the network
     drawer's shell with one static pane per plan; opening a card shows its
     pane. Focus is trapped while open, Escape and the scrim close it. */
  function initPricing() {
    var drawer = document.getElementById('plans');
    var scrim  = document.getElementById('prc-scrim');
    var closer = document.getElementById('prc-close');
    var cards  = document.querySelectorAll('.plan[data-plan]');
    if (!drawer || !scrim || !cards.length) return;

    var panes = drawer.querySelectorAll('.prc-pane');
    var FOCUSABLE = 'a[href], button:not([disabled])';
    var lastFocus = null, open = false;

    function focusables() {
      return Array.prototype.filter.call(drawer.querySelectorAll(FOCUSABLE), function (el) { return el.offsetParent !== null; });
    }
    function show(plan) {
      panes.forEach(function (p) { p.hidden = p.getAttribute('data-plan-pane') !== plan; });
    }
    function openDrawer(plan, card) {
      show(plan);
      if (open) return;
      open = true;
      lastFocus = card || document.activeElement;
      scrim.hidden = false;
      drawer.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      requestAnimationFrame(function () { scrim.classList.add('is-open'); drawer.classList.add('is-open'); });
      drawer.scrollTop = 0;
      setTimeout(function () { (closer || focusables()[0]).focus({ preventScroll: true }); }, reduced.matches ? 0 : 200);
    }
    function closeDrawer() {
      if (!open) return;
      open = false;
      scrim.classList.remove('is-open');
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      setTimeout(function () { scrim.hidden = true; }, reduced.matches ? 0 : 400);
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    }

    var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    cards.forEach(function (card) {
      var plan = card.getAttribute('data-plan');
      card.addEventListener('click', function () { openDrawer(plan, card); });
      card.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') { e.preventDefault(); openDrawer(plan, card); }
      });
      if (fine) {
        card.addEventListener('mousemove', function (e) {
          var r = card.getBoundingClientRect();
          card.style.setProperty('--gx', ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%');
          card.style.setProperty('--gy', ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%');
        });
      }
    });
    /* The pane's CTA points at #cta on the page: close first so the scroll lands. */
    drawer.querySelectorAll('.prc-pane a[href="#cta"]').forEach(function (a) { a.addEventListener('click', closeDrawer); });
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
  }

  /* ── Hero video loop guard ──
     The hero is a Vimeo background embed with loop=1. Free-plan players can
     still run an end screen ("related videos") when a loop stalls, which on
     a page with two of our own videos means the other market's hero plays
     next. So the page enforces the loop itself over the player.js message
     API: on `ended` it seeks to 0 and plays; if the player ever reports a
     different video id, the iframe is reloaded with its original src. */
  function initHeroLoop() {
    var frame = document.querySelector('.hero__video iframe');
    if (!frame) return;
    var src = frame.getAttribute('src');
    var m = src && src.match(/\/video\/(\d+)/);
    if (!m) return;
    var id = Number(m[1]);
    var origin = 'https://player.vimeo.com';

    function post(o) {
      try { frame.contentWindow.postMessage(JSON.stringify(o), origin); } catch (e) {}
    }
    function subscribe() {
      post({ method: 'setLoop', value: true });
      /* Auto quality opens on a 240p/360p rendition and steps up over the first
         seconds; on a 15–20 s loop that soft start is most of what a visitor
         sees, and the `quality` URL parameter is ignored by the background
         player. Pinning via the API holds. 1080p, not 4K: the frame covers a
         ~1500 css px hero and the loop restarts often. */
      post({ method: 'setQuality', value: '1080p' });
      post({ method: 'addEventListener', value: 'ended' });
      post({ method: 'addEventListener', value: 'loaded' });
    }

    window.addEventListener('message', function (e) {
      if (e.origin !== origin || e.source !== frame.contentWindow) return;
      var d;
      try { d = typeof e.data === 'string' ? JSON.parse(e.data) : e.data; } catch (x) { return; }
      if (!d || !d.event) return;
      if (d.event === 'ready') subscribe();
      if (d.event === 'loaded' && d.data && d.data.id && Number(d.data.id) !== id) {
        /* the player moved on to another video: put ours back */
        frame.setAttribute('src', src);
      }
      if (d.event === 'ended') {
        post({ method: 'setCurrentTime', value: 0 });
        post({ method: 'play' });
      }
    });
    /* `ready` may have fired before this script ran; subscribing twice is harmless. */
    subscribe();
    frame.addEventListener('load', subscribe);
  }

  /* ── FAQ accordion ──
     Like initAccordion, but the question is a real <button> inside an <h3>
     (so the heading survives for screen readers and crawlers) and the
     expanded state lives on that button. Clicking anywhere on the row
     toggles it; one open at a time, like the services list. */
  function initFaq() {
    var items = document.querySelectorAll('.faq__item');
    if (!items.length) return;
    function set(item, open) {
      item.classList.toggle('open', open);
      var btn = item.querySelector('.faq__btn');
      if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    items.forEach(function (item) {
      var btn = item.querySelector('.faq__btn');
      function toggle() {
        var isOpen = item.classList.contains('open');
        items.forEach(function (i) { set(i, false); });
        if (!isOpen) set(item, true);
      }
      item.addEventListener('click', function (e) {
        if (e.target === btn) return;   /* the button handles its own click */
        toggle();
      });
      if (btn) btn.addEventListener('click', function (e) { e.stopPropagation(); toggle(); });
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

  /* ── Map ↔ list ──
     The map was decoration: nothing tied a pin to the row underneath it. Now
     lighting either half of a market lights the other, so hovering "Munich" in
     the list names Munich on the map, and the map reads as a control rather
     than an illustration. Pairing is by href, so a new market needs no JS
     change — same contract as the clocks above. The pointer half is gated to
     real hover devices: on a phone the map is hidden and a tap should just
     follow the link. Focus is bound either way, so the map answers the
     keyboard too. */
  function initMarketLink() {
    var section = document.querySelector('.markets');
    if (!section) return;

    var groups = {};
    section.querySelectorAll('a.mk__pin[href], a.mk__cell[href]').forEach(function (el) {
      var href = el.getAttribute('href');
      (groups[href] = groups[href] || []).push(el);
    });

    var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    Object.keys(groups).forEach(function (href) {
      var pair = groups[href];
      /* Defensive: a market that somehow has only one half has nothing to
         light. (Below 760px the map is display:none, but its pins are still in
         the DOM — the pointer gate above is what spares touch devices.) */
      if (pair.length < 2) return;

      function set(on) {
        pair.forEach(function (el) { el.classList.toggle('is-linked', on); });
      }

      pair.forEach(function (el) {
        if (fine) {
          el.addEventListener('pointerenter', function () { set(true); });
          el.addEventListener('pointerleave', function () { set(false); });
        }
        el.addEventListener('focus', function () { set(true); });
        el.addEventListener('blur', function () { set(false); });
      });
    });
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

  /* ── Marquee fill ──
     The track is authored as two copies of the items and animated to -50%,
     which is only seamless while one copy is wider than the viewport. On a
     wide screen it isn't, and the band runs empty until the loop restarts.
     Double the copies until the track is at least twice the viewport, and
     scale the duration so the speed stays what it was at two copies. */
  function initMarquee() {
    var tracks = document.querySelectorAll('.marquee__t');
    if (!tracks.length) return;
    tracks.forEach(function (t) {
      var base = parseFloat(getComputedStyle(t).animationDuration) || 28;
      t.dataset.copies = t.dataset.copies || '2';
      function fill() {
        var guard = 0;
        while (t.scrollWidth < window.innerWidth * 2 && guard++ < 6) {
          Array.prototype.slice.call(t.children).forEach(function (c) { t.appendChild(c.cloneNode(true)); });
          t.dataset.copies = String(Number(t.dataset.copies) * 2);
        }
        t.style.animationDuration = (base * Number(t.dataset.copies) / 2) + 's';
      }
      fill();
      window.addEventListener('resize', fill, { passive: true });
    });
  }

  function init() { initReveal(); initHeroCursor(); initAccordion('[data-svc]'); initAccordion('[data-perk]'); initPricing(); initCtaCursor(); initClocks(); initMarketLink(); initNav(); initNetwork(); initMarquee(); initHeroLoop(); initFaq(); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
