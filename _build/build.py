"""Generates index.html and the case pages from shared templates.

Run from the repo root:  python3 _build/build.py
"""
from pathlib import Path
import hashlib
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
SITE = "https://alextritecky.github.io/submarine_portfolio/"
MAIL = "mailto:project@submarineagency.com.ua?subject=%D0%9A%D0%BE%D0%BD%D1%81%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1%86%D1%96%D1%8F"
LENIS = "https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"

SIZES_FULL = "(min-width: 1440px) 1280px, calc(100vw - 2 * var(--gutter, 20px))"
SIZES_CARD3 = "(min-width: 1100px) 410px, (min-width: 700px) 50vw, 100vw"
SIZES_CARD2 = "(min-width: 1440px) 630px, (min-width: 700px) 50vw, 100vw"


def ver(path):
    """Short content hash so browsers fetch the new file after each deploy."""
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


def dims(name):
    w, h = Image.open(IMG / f"{name}.webp").size
    return f'width="{w}" height="{h}"'


def img(name, alt="", sizes=SIZES_FULL, cls="", priority=False):
    path = IMG / f"{name}.webp"
    w, h = Image.open(path).size
    srcset = ""
    variants = []  # one file per image for now (no srcset)
    variants = [f"assets/img/{p.relative_to(IMG).as_posix()} {v}w" for v, p in variants if p.exists()]
    if variants:
        srcset = f' srcset="{", ".join(variants + [f"assets/img/{name}.webp {w}w"])}" sizes="{sizes}"'
    load = ' fetchpriority="high"' if priority else ' loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="assets/img/{name}.webp"{srcset} alt="{alt}" width="{w}" height="{h}"{load}>'


# ---------------------------------------------------------------- cases data
CASES = {
    "okko": dict(
        title="OKKO: 8 років у режимі non-stop",
        year="2018–2025",
        kpi="+199 095 підписників",
        tags="АЗК · Стратегія · SMM · Креатив · Продакшн",
        niche="auto",
        service="strategy smm creative production special",
        alt="OKKO — людина тримає шаурму у фірмовій упаковці",
    ),
    "samokus": dict(
        title="Samokus: морозимо для тих, кого любимо",
        year="2026",
        kpi="162 119 переглядів",
        tags="Pet Care · SMM · Key visual · Інфлюенс",
        niche="pet",
        service="strategy smm-strategy smm creative production kv influence branding",
        alt="Три стаканчики морозива для собак Samokus на шкіряному дивані",
    ),
    "kuriar": dict(
        title="Куріяр: від виробництва до вашої стрічки",
        year="2026 — дотепер",
        kpi="×4 аудиторія в Instagram",
        tags="FMCG · SMM · Креатив · Продакшн",
        niche="fmcg",
        service="smm-strategy smm creative production influence ads",
        alt="Мариновані курячі гомілки Куріяр на дерев’яній дошці зі спеціями",
    ),
}
ORDER = ["okko", "samokus", "kuriar"]


def card(key, sizes=SIZES_CARD3, heading="h3", i=0):
    c = CASES[key]
    return f'''<a class="case-card" href="{key}.html" style="--i:{i}" data-cursor data-niche="{c["niche"]}" data-service="{c["service"]}">
        <div class="media">{img(f"{key}-hero", c["alt"], sizes)}</div>
        <div class="case-card__body">
          <div class="case-card__row"><span>{c["year"]}</span><span class="case-card__kpi">{c["kpi"]}</span></div>
          <{heading} class="card-title">{c["title"]}</{heading}>
          <p class="tags">{c["tags"]}</p>
        </div>
      </a>'''


# ---------------------------------------------------------------- layout
def head(title, desc, og_image, path):
    url = SITE + path
    return f'''<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#1e2126">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="uk_UA">
  <meta property="og:site_name" content="Submarine Creative Agency">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}assets/og/{og_image}.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
  <link rel="icon" href="assets/icon-192.png" sizes="192x192" type="image/png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css?v={ver("styles.css")}">
  <script>(function(d){{d.classList.add('js');try{{if(sessionStorage.getItem('pt')){{d.classList.add('pt-enter');sessionStorage.removeItem('pt')}}}}catch(e){{}}}})(document.documentElement);</script>
</head>
<body>
<div class="page-transition" aria-hidden="true"></div>
<div class="cursor" aria-hidden="true"><span>Дивитись</span></div>
'''


def header(home):
    cases = "#cases" if home else "index.html#cases"
    logo = "#top" if home else "index.html"
    return f'''
<header class="topbar">
  <a href="{logo}" class="topbar__logo" aria-label="Submarine — на головну">
    <img src="assets/img/sub-logo.webp" alt="" width="44" height="44">
  </a>
  <nav class="topbar__nav" aria-label="Навігація">
    <a href="{cases}">Кейси</a>
    <a href="#contacts">Контакти</a>
  </nav>
  <a class="btn btn--pink btn--sm" href="{MAIL}" data-magnetic>Обговорити проєкт</a>
</header>
'''


FOOTER = f'''
<footer class="footer layer" id="contacts" data-scroll>
  <div class="container">
    <h2 class="footer__word" aria-label="Дякуємо"><span class="line"><span class="line__in">ДЯКУЄМО</span></span></h2>
    <div class="footer__cta">
      <p>Маєте задачу для бренду? Напишіть нам — обговоримо.</p>
      <a class="btn btn--pink btn--lg" href="{MAIL}" data-magnetic>Забронювати консультацію</a>
    </div>
    <ul class="footer__contacts" data-stagger>
      <li><span>Instagram</span><a href="https://www.instagram.com/submarine_agency/" target="_blank" rel="noopener">@submarine_agency</a></li>
      <li><span>Сайт</span><a href="https://submarineagency.com.ua" target="_blank" rel="noopener">submarineagency.com.ua</a></li>
      <li><span>Пошта</span><a href="mailto:project@submarineagency.com.ua">project@submarineagency.com.ua</a></li>
      <li><span>Адреса</span><a href="https://www.google.com/maps/search/?api=1&amp;query=%D0%B2%D1%83%D0%BB.+%D0%A8%D0%BE%D0%BF%D0%B5%D0%BD%D0%B0+10,+%D0%9B%D1%8C%D0%B2%D1%96%D0%B2" target="_blank" rel="noopener">Україна, м. Львів, вул. Шопена, 10</a></li>
    </ul>
    <div class="footer__bottom">
      <span>© 2026 SUBMARINE</span>
      <a class="to-top" href="#top">Нагору ↑</a>
    </div>
  </div>
</footer>

<script src="{LENIS}" defer></script>
<script src="main.js?v={ver("main.js")}" defer></script>
</body>
</html>
'''


def page(path, title, desc, og, body, home=False):
    out = head(title, desc, og, "" if path == "index.html" else path) + header(home)
    out += f'\n<main id="top">\n{body}\n</main>\n' + FOOTER
    (ROOT / path).write_text(out, encoding="utf-8")


# ---------------------------------------------------------------- home
FILTER_NICHES = [
    ("fmcg", "FMCG / Продукти та напої"), ("horeca", "HoReCa"), ("pet", "Pet Care"),
    ("auto", "АЗК та автомобільний сектор"), ("beauty", "Косметика та Beauty"), ("edu", "Освіта"),
    ("health", "Медицина та Health Care"), ("public", "Громадські простори"),
    ("realty", "Нерухомість та девелопмент"), ("furniture", "Меблі та інтер’єр"),
]
FILTER_SERVICES = [
    ("strategy", "Стратегія"), ("smm-strategy", "SMM-стратегія"), ("smm", "Комплексний SMM"),
    ("branding", "Брендинг"), ("kv", "Key visual"), ("merch", "Мерч"), ("creative", "Креатив"),
    ("production", "Продакшн"), ("influence", "Медіа та інфлюенс-маркетинг"),
    ("ads", "Рекламні кампанії"), ("special", "Спецпроєкти"),
]


def filter_menu(key, label, all_label, items):
    opts = "\n".join(f'          <li><button type="button" data-value="{v}">{t}</button></li>' for v, t in items)
    return f'''<div class="filter" data-filter="{key}">
        <button class="filter__toggle" type="button" aria-expanded="false" aria-haspopup="listbox">
          <span class="filter__name">{label}</span><span class="filter__value"></span>
        </button>
        <ul class="filter__menu" role="listbox" aria-label="{label}">
          <li><button type="button" data-value="">{all_label}</button></li>
{opts}
        </ul>
      </div>'''


MARQUEE_ITEMS = ["Стратегія", "Креатив", "SMM", "Інфлюенс", "Продакшн", "Key visual"]
marquee_run = "".join(f"<span>{t}</span><i>✿</i>" for t in MARQUEE_ITEMS)

HOME = f'''
  <section class="hero pin" data-scroll>
    <div class="container hero__inner">
      <h1 class="hero__word" aria-label="Портфоліо">
        <span class="line"><span class="line__in">ПОРТ</span></span>
        <span class="line-row"><span class="line"><span class="line__in">ФОЛІО</span></span><img class="hero__flower" src="assets/img/sub-logo.webp" alt="" width="300" height="300"></span>
      </h1>
      <div class="hero__side">
        <div class="hero__meta">
          <p>2018—2026</p>
          <p class="hero__agency">Submarine Creative Agency</p>
          <p>Стратегія · Креатив · SMM · Інфлюенс</p>
        </div>
        <a class="hero__collage" href="#cases" data-cursor aria-label="Дивитися кейси">
          {img("kuriar-hero", "", "(min-width: 900px) 30vw, 60vw", "hero__shot hero__shot--1", priority=True)}
          {img("samokus-hero", "", "(min-width: 900px) 30vw, 60vw", "hero__shot hero__shot--2", priority=True)}
          {img("okko-hero", "", "(min-width: 900px) 30vw, 60vw", "hero__shot hero__shot--3", priority=True)}
        </a>
      </div>
      <div class="hero__bottom">
        <p class="hero__lead">Систематизуємо комунікацію брендів з 2018 року. Створюємо проєкти, які хочеться бачити, читати та обговорювати. Від стратегії та креативної ідеї — до контенту, кампаній та інфлюенс-маркетингу.</p>
        <div class="hero__actions">
          <a class="btn btn--pink" href="{MAIL}" data-magnetic>Обговорити проєкт</a>
          <a class="btn btn--ghost" href="#cases">Дивитися кейси</a>
        </div>
      </div>
    </div>
  </section>

  <div class="marquee layer" aria-hidden="true">
    <div class="marquee__track">{marquee_run}{marquee_run}</div>
  </div>

  <section class="section layer" id="popular" data-scroll>
    <div class="container">
      <h2 class="display">Популярні кейси</h2>
      <div class="cards cards--2">
      {card("okko", SIZES_CARD2)}
      {card("kuriar", SIZES_CARD2, i=1)}
      </div>
    </div>
  </section>

  <section class="section layer" id="cases" data-scroll>
    <div class="container">
      <h2 class="display">Всі кейси Submarine</h2>

      <div class="filters">
        <span class="filters__label">Фільтри</span>
      {filter_menu("niche", "Ніші", "Усі ніші", FILTER_NICHES)}
      {filter_menu("service", "Послуги", "Усі послуги", FILTER_SERVICES)}
        <button class="filters__reset" type="button" hidden>Скинути ✕</button>
      </div>

      <div class="cards cards--3 cases-grid">
      {"".join(card(k, i=n) for n, k in enumerate(ORDER))}
      </div>
      <p class="cases-empty" hidden>У цій категорії кейси вже в роботі — скоро покажемо. <button type="button" class="link-btn" data-reset>Показати всі</button></p>
    </div>
  </section>
'''


# ---------------------------------------------------------------- case pages
def fig(name, alt):
    return f'''
      <figure class="figure" data-scroll><div class="container">{img(name, alt)}</div></figure>'''


def feed_set(main, posts, index):
    """One Instagram set: big lead post on the left, a 3×3 grid of posts on the right."""
    main_name, main_alt = main
    cols = [posts[i::3] for i in range(3)]  # column-wise, like the original slide
    col_html = "\n".join(
        '              <div class="feed__col">'
        + "".join(f'<figure class="feed__post" style="--d:{c + 1 + r * 0.6:g};--r:{(-1) ** (c + r) * 3}deg">{img(n, a, "(min-width: 900px) 18vw, 30vw")}</figure>'
                  for r, (n, a) in enumerate(col))
        + "</div>"
        for c, col in enumerate(cols))
    return f'''
          <div class="feed__set" data-set="{index}">
            <div class="feed__inner">
              <div class="feed__lead"><figure class="feed__post feed__post--main" style="--d:0;--r:-4deg">{img(main_name, main_alt, "(min-width: 900px) 34vw, 60vw")}</figure></div>
              <div class="feed__grid">
{col_html}
              </div>
            </div>
          </div>'''


def feed(label, *sets):
    """Pinned stage: while it scrolls by, each set of posts flies in, then leaves for the next one."""
    body = "".join(feed_set(m, posts, i) for i, (m, posts) in enumerate(sets))
    bars = "".join('<i class="feed__bar"></i>' for _ in sets)
    return f'''
      <section class="feed" aria-label="{label}" style="--sets:{len(sets)}">
        <div class="feed__stage container">{body}
          <div class="feed__progress" aria-hidden="true"><b class="feed__count">01</b><span>/ {len(sets):02d}</span>{bars}</div>
        </div>
      </section>'''


PLAY_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.6v12.8a1 1 0 0 0 1.52.85l10.2-6.4a1 1 0 0 0 0-1.7L9.52 4.75A1 1 0 0 0 8 5.6z" fill="currentColor"/></svg>'
PAUSE_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1.2" fill="currentColor"/><rect x="14" y="5" width="4" height="14" rx="1.2" fill="currentColor"/></svg>'
SOUND_ON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="currentColor"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
SOUND_OFF = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="currentColor"/><path d="M16 9.5l5 5m0-5l-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'


def reels(label, *items):
    """Inline 9:16 videos: poster + play button, they play right in the card."""
    cards = "\n".join(f'''          <figure class="reel">
            <video class="reel__video" src="assets/video/{src}.mp4" poster="assets/video/{src}.webp" preload="none" playsinline loop aria-label="{alt}"></video>
            <button class="reel__play" type="button" aria-label="Відтворити: {alt}"><span class="reel__icon reel__icon--play">{PLAY_ICON}</span><span class="reel__icon reel__icon--pause">{PAUSE_ICON}</span></button>
            <button class="reel__sound" type="button" aria-label="Вимкнути звук"><span class="reel__icon reel__icon--on">{SOUND_ON}</span><span class="reel__icon reel__icon--off">{SOUND_OFF}</span></button>
            <span class="reel__bar" aria-hidden="true"><i></i></span>
          </figure>''' for src, alt in items)
    return f'''
      <section class="reels" aria-label="{label}" data-scroll>
        <div class="container reels__grid" data-stagger>
{cards}
        </div>
      </section>'''


def loop_video(src, alt):
    """Muted autoplay loop, full container width (starts when on screen)."""
    return f'''
      <figure class="figure loop" data-scroll><div class="container">
        <video class="loop__video" src="assets/video/{src}.mp4" poster="assets/video/{src}.webp" muted loop playsinline preload="none" aria-label="{alt}"></video>
      </div></figure>'''


def stage(kicker, title, *paras):
    body = "\n".join(f"            <p>{p}</p>" for p in paras)
    return f'''
      <section class="story section" data-scroll>
        <div class="container story__grid">
          <div>
            <p class="kicker">{kicker}</p>
            <h2 class="story__title">{title}</h2>
          </div>
          <div class="story__text" data-stagger>
{body}
          </div>
        </div>
      </section>'''


def kpis(*items):
    cells = "\n".join(f'          <div class="kpi"><b>{n}</b><span>{t}</span></div>' for n, t in items)
    return f'''
      <div class="kpis section" data-scroll>
        <div class="container kpis__grid" data-stagger>
{cells}
        </div>
      </div>'''


def case_page(key, num, logo, logo_alt, partner, period, tagline, facts, content):
    c = CASES[key]
    i = ORDER.index(key)
    nxt = ORDER[(i + 1) % len(ORDER)]
    niche, services, tools = facts
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    return f'''
  <article class="case">
    <div class="layer">
      <section class="case-hero section" data-scroll>
        <div class="container">
          <div class="case-hero__top"><span>{partner} × SUBMARINE</span><span>Період співпраці: {period}</span></div>
          <div class="case-hero__body">
            <div class="media">{img(f"{key}-hero", c["alt"], "(min-width: 900px) 62vw, 100vw", priority=True)}</div>
            <div class="case-hero__brand">
              <h1 class="case-hero__logo"><img src="assets/img/{logo}.webp" alt="{logo_alt}" {dims(logo)} fetchpriority="high"></h1>
              <p class="case-hero__tagline">{tagline}</p>
              <p class="case-hero__kpi">{c["kpi"]}</p>
            </div>
          </div>
          <dl class="case-facts" data-stagger>
            <div><dt>Ніша</dt><dd>{niche}</dd></div>
            <div><dt>Послуги</dt><dd><ul>{li(services)}</ul></dd></div>
            <div><dt>Інструменти</dt><dd><ul>{li(tools)}</ul></dd></div>
          </dl>
        </div>
      </section>
{content}
    </div>
  </article>

  <nav class="next-case layer section" aria-label="Інші кейси" data-scroll>
    <div class="container next-case__inner">
      <a class="next-case__back" href="index.html#cases">← Всі кейси</a>
      <p class="kicker">Наступний кейс</p>
      <div class="next-case__card">{card(nxt, SIZES_CARD2, "h2")}</div>
    </div>
  </nav>
'''


OKKO = case_page(
    "okko", 1, "okko-logo", "OKKO", "OKKO", "2018–2025", "8 років у режимі non-stop",
    ("АЗК та автомобільний сектор", ["Стратегія", "SMM", "Креатив", "Продакшн", "Спецпроєкти"],
     ["Instagram", "Facebook", "Digital Media"]),
    stage("Задача", "8 років комунікації, яка не зупиняється",
          "SUBMARINE стала частиною щоденної комунікації OKKO: від SMM-стратегії до продакшну, кампаній і спецпроєктів. Ми працювали з продуктами, сервісами, ситуативами та соціальними ініціативами — разом із брендом постійно рухали комунікацію АЗК, зважаючи на настрій аудиторії та світу навколо.")
    + fig("okko-stats", "+130 зйомок, +16 000 кадрів, +3800 відео")
    + stage("Ідея", "Ми винайшли тисячі способів не повторюватись та залишатись в контексті",
            "Їжа, сервіси, меми, ситуативи, великі кампанії та соціальні ініціативи — за 8 років співпраці OKKO розповідало про своє життя, ритм та вподобання гостей, завжди залишаючись впізнаваним.")
    + fig("okko-collage", "Колаж кадрів зі зйомок OKKO: їжа, кава, гості на АЗК")
    + stage("Виконання", "Продукти, сервіси, ситуативи та соціальні ініціативи")
    + feed("Публікації OKKO в Instagram", (("okko/main-1", "Публікація OKKO «Айс меню»: чотири холодні кавові напої"), [
        ("okko/opt-1", "Кіт на заправці OKKO: «Сварити OKKO, щоб зробили окремі каси для заправки»"),
        ("okko/opt-2", "Пальне PULLS Diesel «Арктика −32°»: каністра в кризі"),
        ("okko/opt-3", "Дівчина з брелоками та в’язаною сумкою біля OKKO"),
        ("okko/opt-4", "«На АЗК знайдено той самий шоколад»"),
        ("okko/opt-5", "Вихідні знижених цін на пальне OKKO"),
        ("okko/opt-6", "Морозиво «Твого настрою» від OKKO летить у небі"),
        ("okko/opt-7", "«Освіжи ідеї»: ріжок морозива з мініатюрними фігурками"),
        ("okko/opt-8", "Новинка на OKKO — міні-хотдоги"),
        ("okko/opt-9", "«Маленьке винце»: вина на АЗК OKKO"),
    ]), (("okko/main-2", "«Восьмий пульстрон готується підсилити військо»: OKKO × Повернись живим"), [
        ("okko/opt-10", "OKKO × Ukrarmor: шолом із шевроном «OKKO нСТАХА»"),
        ("okko/opt-11", "131 млн грн заощаджено військовими завдяки Армія+ та «Зігріваємо захисників»"),
        ("okko/opt-12", "«Одразу два пульстрони підсилили військо»"),
        ("okko/opt-13", "Результати ліги «Дронопад»"),
        ("okko/opt-14", "OKKO пригощає енергетиків ДТЕК на своїх АЗК"),
        ("okko/opt-15", "Близько 53 тонни речей для рідних незнайомців у зелених контейнерах"),
        ("okko/opt-16", "«Дев’ятий пульстрон готується підсилити військо»"),
        ("okko/opt-17", "«Зігріваємо захисників»: 4 247 427 хотдогів і 7 303 102 чашки кави та чаю"),
        ("okko/opt-18", "Відновлення будинку: до і після"),
    ]))
    + stage("Результати", "Результати співпраці",
            "Ми фокусувалися не лише на зростанні фанбази, а на побудові активного ком’юніті. Постійно шукали нові теми, формати та приводи для взаємодії, щоб комунікація розвивалася разом із брендом та його аудиторією.",
            "Результат: +199 095 нових підписників на двох платформах і ком’юніті, яке продовжує зростати.")
    + fig("okko-results", "Профіль OKKO в Instagram до та після співпраці"),
)

SAMOKUS = case_page(
    "samokus", 2, "samokus-logo", "Samokus", "SAMOKUS", "травень–червень 2026",
    "Морозимо для тих, кого любимо",
    ("Pet Care", ["SMM-стратегія", "Комплексний SMM", "Креатив", "Продакшн", "Key visual", "Медіа та інфлюенс-маркетинг"],
     ["Instagram", "UGC / UGC Creators", "Creative Production", "Consulting"]),
    stage("Задача", "Запуск бренду",
          "Виклик: познайомити аудиторію з абсолютно новим брендом та пояснити продукт, про який більшість собачників навіть не чула.",
          "Ми почали з дослідження ринку та аудиторії, розробили стратегію просування, унікальний Tone of Voice та Key Visual. І свідомо відмовившись від звичних для pet-категорії візуальних і вербальних кліше, створили власний характер SAMOKUS.")
    + fig("samokus-strategy", "Фрагменти стратегії Samokus: цілі, аналіз Tone of Voice, слова та фрази-фішки")
    + fig("samokus-brand", "Айдентика Samokus: кольорова палітра, аватарки, highlights, шрифти та сторіс")
    + stage("Виконання", "Контент і продакшн",
            "Основою комунікації зробили справжніх собак та їх емоції. AI використовували точково — для легкого розважального контенту, який доповнював живі фото- та відеозйомки.",
            "А коли SAMOKUS почав активно з’являтися на офлайн-подіях — інтегрували їх у контент, знайомлячи з брендом не лише власників собак, а й потенційних B2B-партнерів.")
    + fig("samokus-photos", "Фотозйомка собак різних порід із морозивом Samokus")
    + fig("samokus-feed", "Публікації Samokus в Instagram: смаки, інструкції, розіграш")
    + reels("Reels Samokus",
            ("samokus/reel-1", "Чорний пес куштує морозиво Samokus на вулиці"),
            ("samokus/reel-2", "Собаки співають на сцені Samokus"),
            ("samokus/reel-3", "Доберман обирає між трьома смаками Samokus"))
    + stage("Інфлюенс", "Слово дегустаторам",
            "Щоб новий продукт швидше знаходив свою аудиторію, ми залучили pet-блогерів та UGC-креаторів: сформували базу релевантних dog-акаунтів і супроводжували бартерні співпраці — від перших домовленостей до виходу контенту.")
    + reels("UGC-відео pet-блогерів",
            ("samokus/reel-4", "Пес у жовтій панамі куштує морозиво Samokus"),
            ("samokus/reel-5", "«Стоп… собакам морозиво!»: стаканчики Samokus на пляжі"),
            ("samokus/reel-6", "Французький бульдог чекає на морозиво Samokus зі смаком вишні"))
    + stage("Результати", "Результати співпраці",
            "За перший місяць ми сформували впізнаваний характер бренду, познайомили людей із новою продуктовою категорією та заклали основу для подальшого розвитку комунікації.")
    + fig("samokus-results", "Доберман тримає лапу на стаканчику морозива Samokus"),
)

KURIAR = case_page(
    "kuriar", 3, "kuriar-logo", "Куріяр", "КУРІЯР", "лютий 2026 — дотепер",
    "Від виробництва до вашої стрічки",
    ("FMCG / Продукти та напої", ["SMM-стратегія", "Комплексний SMM", "Креатив", "Продакшн", "Медіа та інфлюенс-маркетинг"],
     ["Instagram", "Facebook", "AI Generation", "Meta Ads", "Фото- та відеопродакшн"]),
    stage("Задача", "Скільки можна говорити про курку? Виявилося, багато",
          "Куріяр прийшов до нас із завданням побудувати системну присутність бренду в Instagram та Facebook. Але просто регулярно показувати курятину — не наш метод.",
          "Ми адаптували бренд-стратегію до соцмереж: розробили SMM-стратегію, визначили принципи комунікації, візуальний напрям і контентні рубрики.",
            "Так з’явилася система, у якій курятина — лише початок розмови. Далі — рецепти, виробництво, люди, партнери та креативні експерименти.")
    + fig("kuriar-strategy", "Фрагменти стратегії Куріяр: цілі в соцмережах, мудборд, спосіб споживання")
    + fig("kuriar-brand", "«Спочатку була курка»: обкладинки Facebook, highlights та публікації Куріяр")
    + stage("Виконання", "Контент і продакшн",
            "Знімаємо Куріяр там, де вирує його справжнє життя: на виробництві, у фірмових магазинах, офісі та на виїзних подіях. Показуємо не лише продукт, а й людей, процеси та історії, які стоять за брендом.",
            "А коли реальності стає замало — підключаємо AI. Створюємо контент, експериментуємо із сюжетами та втілюємо ідеї, для яких звичайного знімального майданчика було б недостатньо.",
            "Так у стрічці Куріяру поєднуються справжнє життя бренду та креатив, який виходить за його межі.")
    + loop_video("kuriar/content", "Зйомки та діджитал Куріяр: пости, виробництво, магазини та AI-візуали")
    + stage("Результати", "Результати співпраці",
            "Системна робота зі стратегією, контентом, продакшном та креативами дає вимірювані результати. За час співпраці ми збільшили аудиторію в Instagram більш ніж у 4 рази, а у Facebook — у 3,5 раза.",
            "І це не фінальні результати. Ми продовжуємо експериментувати з форматами, знаходити нові точки контакту з аудиторією та розвивати присутність бренду в соцмережах.")
    + fig("kuriar-growth", "Профілі Куріяр до та після: Instagram 471 → 2 007 підписників (+326%), Facebook 1 400 → 4 900 (+250%)"),
)

page("index.html", "Портфоліо — Submarine Creative Agency",
     "Портфоліо Submarine Creative Agency: стратегія, креатив, SMM та інфлюенс-маркетинг з 2018 року.",
     "home", HOME, home=True)
page("okko.html", "OKKO — кейс Submarine", "OKKO × Submarine: 8 років комунікації АЗК у режимі non-stop.", "okko", OKKO)
page("samokus.html", "Samokus — кейс Submarine", "Samokus × Submarine: запуск бренду морозива для собак.", "samokus", SAMOKUS)
page("kuriar.html", "Куріяр — кейс Submarine", "Куріяр × Submarine: системна присутність бренду в Instagram та Facebook.", "kuriar", KURIAR)
print("built 4 pages")
