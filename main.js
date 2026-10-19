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

  /* ================= Case cards fly in ================= */
  const feedPosts = document.querySelectorAll('.case-card');
  if (feedPosts.length) {
    if ('IntersectionObserver' in window && !reduced) {
      const fio = new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          e.target.classList.add('is-shown');
          fio.unobserve(e.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
      feedPosts.forEach((p) => fio.observe(p));
    } else {
      feedPosts.forEach((p) => p.classList.add('is-shown'));
    }
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

  // Instagram feed: the stage is pinned and every post is scrubbed by scroll
  // position, so the swap follows the scroll instead of firing at once.
  // Per post: a = how far it has arrived (0 below → 1 in place),
  //           b = how far it has left (0 in place → 1 gone above).
  const smooth = (t) => t * t * (3 - 2 * t);
  const feeds = [...document.querySelectorAll('.feed')].map((el) => ({
    el,
    stage: el.querySelector('.feed__stage'),
    progress: el.querySelector('.feed__progress'),
    count: el.querySelector('.feed__count'),
    bars: [...el.querySelectorAll('.feed__bar')],
    sets: [...el.querySelectorAll('.feed__set')].map((set) => ({
      el: set,
      inner: set.querySelector('.feed__inner'),
      grid: set.querySelector('.feed__grid'),
      posts: [...set.querySelectorAll('.feed__post')].map((post) => ({
        el: post,
        img: post.querySelector('img'),
        main: post.classList.contains('feed__post--main'),
        d: parseFloat(post.style.getPropertyValue('--d')) || 0,
        r: parseFloat(post.style.getPropertyValue('--r')) || 0,
        last: '',
      })),
    })),
  }));

  // Within one set's slice of the pinned scroll: rows drift up first,
  // then the set hands over to the next one.
  const DRIFT = [0.06, 0.6];   // drift window
  const OUT = [0.6, 0.9];      // this set leaves
  const IN = [0.7, 1.0];       // next set arrives (overlaps the exit)
  const MAXD = 4.2;            // largest --d (diagonal wave: column + 0.6 × row)
  const STAGGER = 0.035;       // delay per wave step inside a window
  const win = (t, [a, b], d = 0) => smooth(clamp((t - a - d * STAGGER) / (b - a - MAXD * STAGGER)));

  function paintPost(p, a, b) {
    const vis = a * (1 - b);
    let tf, blur, clip = '', imgTf = '';
    if (reduced) {
      tf = 'none'; blur = 0;
    } else if (p.main) {
      // lead post: curtain reveal from the bottom, photo settles from a slight zoom
      const y = -b * 140;
      tf = `perspective(1400px) translate3d(0,${y.toFixed(1)}px,0) rotateX(${(-14 * b).toFixed(2)}deg) scale(${(1 - 0.08 * b).toFixed(3)})`;
      clip = `inset(${((1 - a) * 100).toFixed(1)}% 0 0 0 round 18px)`;
      imgTf = `scale(${(1 + 0.18 * (1 - a)).toFixed(3)})`;
      blur = 10 * b;
    } else {
      const y = (1 - a) * 140 - b * 160;
      const rx = 24 * (1 - a) - 20 * b;
      const rot = p.r * (1 - a) - p.r * b;
      const sc = 1 - 0.14 * (1 - a) - 0.1 * b;
      tf = `perspective(1200px) translate3d(0,${y.toFixed(1)}px,${(-160 * (1 - a) - 120 * b).toFixed(0)}px) rotateX(${rx.toFixed(2)}deg) rotate(${rot.toFixed(2)}deg) scale(${sc.toFixed(3)})`;
      blur = 10 * (1 - a) + 10 * b;
    }
    const op = p.main ? Math.min(1, a * 4) * (1 - b) : vis;
    const key = `${op.toFixed(3)}|${tf}|${blur.toFixed(1)}|${clip}|${imgTf}`;
    if (key === p.last) return;
    p.last = key;
    p.el.style.opacity = op.toFixed(3);
    p.el.style.transform = tf;
    p.el.style.filter = blur > 0.05 ? `blur(${blur.toFixed(1)}px)` : 'none';
    if (p.main) {
      p.el.style.clipPath = clip;
      p.img.style.transform = imgTf;
    }
  }

  // Start loading every feed photo well before the stage arrives, so posts never fly in empty.
  if ('IntersectionObserver' in window) {
    const pre = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.querySelectorAll('img[loading="lazy"]').forEach((im) => { im.loading = 'eager'; });
      pre.unobserve(e.target);
    }), { rootMargin: '200% 0px' });
    feeds.forEach((f) => pre.observe(f.el));
  }

  function updateFeeds(vh) {
    const mobile = window.innerWidth < 900;
    const header = topbar.offsetHeight;
    for (const f of feeds) {
      const r = f.el.getBoundingClientRect();
      if (r.bottom < -vh || r.top > vh * 2) continue;
      const travel = Math.max(1, f.el.offsetHeight - f.stage.offsetHeight);
      const n = f.sets.length;
      const pos = clamp((header - r.top) / travel) * n;          // 0 … n across the pinned scroll
      const enter = clamp((vh - r.top) / Math.max(1, vh - header)); // first set arrives while the stage scrolls up
      f.sets.forEach((set, i) => {
        const local = pos - i;                                   // this set's own slice
        set.posts.forEach((p) => {
          const a = i === 0 ? win(enter, [0.15, 1], p.d) : win(local + 1, IN, p.d);
          const b = i === n - 1 ? 0 : win(local, OUT, p.d);
          paintPost(p, a, b);
        });
        const active = (i === 0 ? enter > 0.5 : local + 1 > IN[1] - 0.1) && (i === n - 1 || local < OUT[0] + 0.1);
        set.el.classList.toggle('is-current', active);
        if (reduced) return;
        // drift the set so rows hidden below the stage edge scroll into view
        const target = mobile ? set.inner : set.grid;
        const overflow = Math.max(0, target.offsetTop + target.offsetHeight - f.stage.clientHeight + 24);
        const drift = i === n - 1 ? smooth(clamp((local - DRIFT[0]) / (0.9 - DRIFT[0]))) : win(local, DRIFT);
        target.style.transform = `translate3d(0,${(-overflow * drift).toFixed(1)}px,0)`;
      });
      if (f.progress) {
        const on = enter > 0.6 && pos < n - 0.05;
        f.progress.classList.toggle('is-on', on);
        f.bars.forEach((bar, i) => bar.style.setProperty('--fill', clamp(i === 0 ? Math.max(pos, enter > 0.99 ? 0.02 : 0) : pos - i).toFixed(3)));
        const shown = Math.min(n, Math.floor(pos + 1 - (IN[0] - 0.05)) + 1);
        f.count.textContent = String(clamp(shown, 1, n)).padStart(2, '0');
      }
    }
  }

  const blocks = [...document.querySelectorAll('[data-scroll]')].map((el) => ({
    el,
    pin: el.classList.contains('pin'),
    next: el.classList.contains('pin') ? el.nextElementSibling : null,
  }));

  let ticking = false;
  function update() {
    ticking = false;
    setHeader();
    const vh = window.innerHeight;
    if (reduced) { updateFeeds(vh); return; }
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
    updateFeeds(vh);
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
