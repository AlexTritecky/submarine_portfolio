(() => {
  /* ================= Filters (home page only) ================= */
  if (document.querySelector('.filters')) initFilters();
  function initFilters() {
  const cards = [...document.querySelectorAll('.case-card')];
  const realCards = cards.filter((c) => !c.hasAttribute('data-soon'));
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
      const n = realCards.filter((c) => matches(c, key, v)).length;
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
      const soon = card.hasAttribute('data-soon');
      const ok = soon ? !filtering : matches(card, 'niche', state.niche) && matches(card, 'service', state.service);
      const wasHidden = card.classList.contains('is-hidden');
      card.classList.toggle('is-hidden', !ok);
      if (ok) {
        shown += soon ? 0 : 1;
        if (wasHidden) {
          card.classList.remove('is-in');
          void card.offsetWidth;
          card.classList.add('is-in');
        }
      }
    });
    emptyMsg.hidden = !filtering || shown > 0;
    resetBtn.hidden = !filtering;

    filters.forEach((f) => {
      const key = f.dataset.filter;
      const value = state[key];
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

  /* ================= Scroll-triggered fade ================= */
  // Every [data-scroll] block fades out as it leaves the top of the viewport
  // while the next block rises into its place. Pinned (.pin) slides stay put
  // and dissolve as the following layer slides over them.
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const clamp = (v) => Math.min(1, Math.max(0, v));
  const blocks = [...document.querySelectorAll('[data-scroll]')].map((el) => ({
    el,
    pin: el.classList.contains('pin'),
    next: el.classList.contains('pin') ? el.nextElementSibling : null,
  }));

  let ticking = false;
  function update() {
    ticking = false;
    const vh = window.innerHeight;
    for (const b of blocks) {
      let o, t;
      if (b.pin) {
        const p = b.next ? clamp(1 - b.next.getBoundingClientRect().top / vh) : 0;
        o = clamp(1 - p * 1.25);
        t = `translateY(${(-p * 8).toFixed(2)}vh) scale(${(1 - p * 0.08).toFixed(4)})`;
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
  }
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();
