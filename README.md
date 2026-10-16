# submarine_portfolio

Сайт-портфоліо Submarine Creative Agency, зібраний на основі PDF-портфоліо.

Статичний сайт: `index.html`, `okko.html`, `samokus.html`, `kuriar.html`, `styles.css`, `main.js`, зображення в `assets/img/`.

HTML-сторінки генеруються зі спільних шаблонів (хедер, футер, мета-теги, картки кейсів).
Тексти й дані кейсів правляться в `_build/build.py`, після чого:

```bash
python3 _build/build.py
```

- Фільтри кейсів за нішами та послугами
- Scroll-triggered анімація: верхній блок плавно зникає, наступний займає його місце (вимикається при `prefers-reduced-motion`)

Локальний запуск:

```bash
python3 -m http.server 5173
```
