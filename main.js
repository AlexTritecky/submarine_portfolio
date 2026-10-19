(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));

  /* ================= Filters (home page only) ================= */
  if (document.querySelector('.filters')) initFilters();
  function initFilters() {
    const cards = [...document.querySelectorAll('.cases-grid .case-card')];
    const filters = [...document.querySelectorAll('.filter')];
    const resetBtn = document.querySelector('.filters__reset');
    const emptyMsg = document.querySelector('.cases-empty');
    const state = { niche: '', service: '' };

    const matches = (card, key, value) =>
      !value || (card.dataset[key] || '').split(/\s+/).includes(value);

    // Show how many cases each option has.
    filters.forEach((f) => {
      const key = f.dataset.filter;
      f.querySelectorAll('.filter__menu button').forEach((btn) => {
        const v = btn.dataset.value;
        if (!v) return;
        const n = cards.filter((c) => matches(c, key, v)).length;
        const count = document.createElement('span');
        count.className = 'count';
        count.textContent = n;
        btn.append(count);
        if (!n) btn.classList.add('is-empty');
      });
    });

    const closeAll = (except) =>
      filters.forEach((f) => {
        if (f === except) return;
        f.classList.remove('is-open');
        f.querySelector('.filter__toggle').setAttribute('aria-expanded', 'false');
      });

    function apply() {
      const filtering = Boolean(state.niche || state.service);
      let shown = 0;
      cards.forEach((card) => {
        const ok = matches(card, 'niche', state.niche) && matches(card, 'service', state.service);
        const wasHidden = card.classList.contains('is-hidden');
        card.classList.toggle('is-hidden', !ok);
        if (!ok) return;
        shown += 1;
        if (wasHidden) {
          card.classList.remove('is-in');
          void card.offsetWidth;
          card.classList.add('is-in');
        }
      });
      emptyMsg.hidden = shown > 0;
      resetBtn.hidden = !filtering;

      filters.forEach((f) => {
        const value = state[f.dataset.filter];
        f.classList.toggle('is-active', Boolean(value));
        let label = '';
        f.querySelectorAll('.filter__menu button').forEach((b) => {
          const sel = b.dataset.value === value;
          b.setAttribute('aria-selected', String(sel));
          if (sel && value) label = b.firstChild.textContent.trim();
        });
        f.querySelector('.filter__value').textContent = label;
      });
    }

    filters.forEach((f) => {
      const toggle = f.querySelector('.filter__toggle');
      toggle.addEventListener('click', (e) => {
        e.stopPropagation();
        const open = !f.classList.contains('is-open');
        closeAll(f);
        f.classList.toggle('is-open', open);
        toggle.setAttribute('aria-expanded', String(open));
      });
      f.querySelector('.filter__menu').addEventListener('click', (e) => {
        const btn = e.target.closest('button');
        if (!btn) return;
        state[f.dataset.filter] = btn.dataset.value;
        closeAll();
        apply();
      });
    });

    const reset = () => { state.niche = ''; state.service = ''; apply(); };
    resetBtn.addEventListener('click', reset);
    document.querySelector('[data-reset]').addEventListener('click', reset);
    document.addEventListener('click', (e) => { if (!e.target.closest('.filter')) closeAll(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeAll(); });
    apply();
  }

  /* ================= Header state ================= */
  const topbar = document.querySelector('.topbar');
  const setHeader = () => topbar.classList.toggle('is-scrolled', window.scrollY > 24);
  setHeader();

  /* ================= Line reveals (hero, footer) ================= */
  const hero = document.querySelector('.hero');
  if (hero) setTimeout(() => hero.classList.add('is-revealed'), 60);

  /* ================= Staggered reveal ================= */
  const staggerGroups = document.querySelectorAll('[data-stagger]');
  staggerGroups.forEach((g) => [...g.children].forEach((el, i) => el.style.setProperty('--i', i)));
  const footer = document.querySelector('.footer');
  if ('IntersectionObserver' in window && !reduced) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        e.target.classList.add(e.target === footer ? 'is-revealed' : 'is-visible');
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -12% 0px' });
    staggerGroups.forEach((g) => io.observe(g));
    if (footer) io.observe(footer);
  } else {
    staggerGroups.forEach((g) => g.classList.add('is-visible'));
    footer && footer.classList.add('is-revealed');
  }

  /* ================= Page transitions ================= */
  const veil = document.querySelector('.page-transition');
  const root = document.documentElement;
  if (root.classList.contains('pt-enter')) {
    setTimeout(() => root.classList.add('pt-go'), 30);
    setTimeout(() => root.classList.remove('pt-enter', 'pt-go'), 700);
  }
  if (!reduced) {
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href]');
      if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if (a.target === '_blank' || a.hasAttribute('download')) return;
      const url = new URL(a.href, location.href);
      if (url.origin !== location.origin || url.protocol.startsWith('mailto')) return;
      if (url.pathname === location.pathname) return; // same-page anchors scroll instead
      e.preventDefault();
      try { sessionStorage.setItem('pt', '1'); } catch (_) {}
      veil.classList.add('is-leaving');
      setTimeout(() => { location.href = url.href; }, 450);
    });
    window.addEventListener('pageshow', (e) => { if (e.persisted) veil.classList.remove('is-leaving'); });
  }

  /* ================= Smooth scroll (Lenis) ================= */
  let lenis = null;
  if (!reduced && window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.1, smoothWheel: true });
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href');
    const target = id === '#top' ? 0 : document.querySelector(id);
    if (target === null) return;
    e.preventDefault();
    if (lenis) lenis.scrollTo(target, { offset: id === '#top' ? 0 : -64 });
    else if (target === 0) window.scrollTo({ top: 0 });
    else target.scrollIntoView();
    history.replaceState(null, '', id === '#top' ? location.pathname : id);
  });

  /* ================= Custom cursor & magnetic buttons ================= */
  if (finePointer && !reduced) {
    const cursor = document.querySelector('.cursor');
    let x = -200, y = -200, pending = false;
    window.addEventListener('mousemove', (e) => {
      x = e.clientX; y = e.clientY;
      if (pending) return;
      pending = true;
      requestAnimationFrame(() => {
        pending = false;
        cursor.style.setProperty('--x', `${x}px`);
        cursor.style.setProperty('--y', `${y}px`);
      });
    }, { passive: true });
    document.querySelectorAll('[data-cursor]').forEach((el) => {
      el.classList.add('cursor-on');
      el.addEventListener('mouseenter', () => cursor.classList.add('is-active'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('is-active'));
    });

    document.querySelectorAll('[data-magnetic]').forEach((btn) => {
      btn.addEventListener('mousemove', (e) => {
        const r = btn.getBoundingClientRect();
        const dx = e.clientX - (r.left + r.width / 2);
        const dy = e.clientY - (r.top + r.height / 2);
        btn.style.transform = `translate(${dx * 0.25}px, ${dy * 0.35}px)`;
      });
      btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
    });
  }

  /* ================= Scroll-triggered fade ================= */
  // Every [data-scroll] block fades out as it leaves the top of the viewport
  // while the next block rises into its place. Pinned (.pin) slides stay put
  // and dissolve as the following layer slides over them.
  const heroLines = hero ? [...hero.querySelectorAll('.hero__word > span')] : [];
  const footerWord = document.querySelector('.footer__word');

  const blocks = [...document.querySelectorAll('[data-scroll]')].map((el) => ({
    el,
    pin: el.classList.contains('pin'),
    next: el.classList.contains('pin') ? el.nextElementSibling : null,
  }));

  let ticking = false;
  function update() {
    ticking = false;
    setHeader();
    if (reduced) return;
    const vh = window.innerHeight;
    for (const b of blocks) {
      let o, t;
      if (b.pin && getComputedStyle(b.el).position === 'sticky') {
        const p = b.next ? clamp(1 - b.next.getBoundingClientRect().top / vh) : 0;
        o = clamp(1 - p * 1.25);
        t = `translateY(${(-p * 8).toFixed(2)}vh) scale(${(1 - p * 0.08).toFixed(4)})`;
        if (b.el === hero) {
          heroLines.forEach((l, i) => { l.style.transform = `translateX(${(i ? 1 : -1) * p * 12}vw)`; });
        }
      } else {
        const r = b.el.getBoundingClientRect();
        if (r.bottom < -50 || r.top > vh + 50) continue;
        const enter = clamp((vh - r.top) / (vh * 0.3));
        const exit = clamp(r.bottom / (vh * 0.5));
        o = Math.min(enter, exit);
        const dy = (1 - enter) * 60 - (1 - exit) * 40;
        t = `translateY(${dy.toFixed(1)}px) scale(${(1 - (1 - exit) * 0.04).toFixed(4)})`;
      }
      b.el.style.opacity = o.toFixed(3);
      b.el.style.transform = t;
      b.el.style.visibility = o <= 0.001 ? 'hidden' : '';
    }
    if (footerWord) {
      const r = footerWord.getBoundingClientRect();
      if (r.top < vh && r.bottom > 0) {
        const p = clamp((vh - r.top) / (vh + r.height));
        footerWord.style.transform = `translateX(${((0.5 - p) * 16).toFixed(2)}vw)`;
      }
    }
  }
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();
