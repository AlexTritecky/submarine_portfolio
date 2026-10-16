"""Generates index.html and the case pages from shared templates.

Run from the repo root:  python3 _build/build.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
SITE = "https://alextritecky.github.io/submarine_portfolio/"
MAIL = "mailto:project@submarineagency.com.ua?subject=%D0%9A%D0%BE%D0%BD%D1%81%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1%86%D1%96%D1%8F"
LENIS = "https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"

SIZES_FULL = "(min-width: 1440px) 1280px, calc(100vw - 2 * var(--gutter, 20px))"
SIZES_CARD3 = "(min-width: 1100px) 410px, (min-width: 700px) 50vw, 100vw"
SIZES_CARD2 = "(min-width: 1440px) 630px, (min-width: 700px) 50vw, 100vw"


def dims(name):
    w, h = Image.open(IMG / f"{name}.webp").size
    return f'width="{w}" height="{h}"'


def img(name, alt="", sizes=SIZES_FULL, cls="", priority=False):
    path = IMG / f"{name}.webp"
    w, h = Image.open(path).size
    srcset = ""
    variants = [(v, IMG / f"{name}-w{v}.webp") for v in (800, 1200)]
    variants = [f"assets/img/{p.name} {v}w" for v, p in variants if p.exists()]
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


def card(key, sizes=SIZES_CARD3, heading="h3"):
    c = CASES[key]
    return f'''<a class="case-card" href="{key}.html" data-cursor data-niche="{c["niche"]}" data-service="{c["service"]}">
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
  <link rel="stylesheet" href="styles.css">
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


INSTAGRAM_ICON = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1.1.4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 2c-3.1 0-3.5 0-4.7.1-1 0-1.6.2-1.9.3-.5.2-.8.4-1.1.7-.3.3-.6.7-.7 1.1-.1.4-.3.9-.3 1.9-.1 1.2-.1 1.6-.1 4.7s0 3.5.1 4.7c0 1 .2 1.6.3 1.9.2.5.4.8.7 1.1.3.3.7.6 1.1.7.4.1.9.3 1.9.3 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1 0 1.6-.2 1.9-.3.5-.2.8-.4 1.1-.7.3-.3.6-.7.7-1.1.1-.4.3-.9.3-1.9.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c0-1-.2-1.6-.3-1.9-.2-.5-.4-.8-.7-1.1-.3-.3-.7-.6-1.1-.7-.4-.1-.9-.3-1.9-.3-1.2-.1-1.6-.1-4.7-.1zm0 3.3a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9zm0 2a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zm4.7-3.3a1.1 1.1 0 1 1 0 2.1 1.1 1.1 0 0 1 0-2.1z"/></svg>'

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
      <a class="footer__social" href="https://www.instagram.com/submarine_agency/" target="_blank" rel="noopener" aria-label="Instagram">{INSTAGRAM_ICON}</a>
      <a class="to-top" href="#top">Нагору ↑</a>
    </div>
  </div>
</footer>

<script src="{LENIS}" defer></script>
<script src="main.js" defer></script>
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
        <span class="line"><span class="line__in">ФОЛІО</span><img class="hero__flower" src="assets/img/sub-logo.webp" alt="" width="258" height="258"></span>
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
      <p class="kicker">01 —</p>
      <h2 class="display">Популярні кейси</h2>
      <div class="cards cards--2" data-stagger>
      {card("okko", SIZES_CARD2)}
      {card("kuriar", SIZES_CARD2)}
      </div>
    </div>
  </section>

  <section class="section layer" id="cases" data-scroll>
    <div class="container">
      <p class="kicker">02 —</p>
      <h2 class="display">Всі кейси Submarine</h2>

      <div class="filters">
        <span class="filters__label">Фільтри</span>
      {filter_menu("niche", "Ніші", "Усі ніші", FILTER_NICHES)}
      {filter_menu("service", "Послуги", "Усі послуги", FILTER_SERVICES)}
        <button class="filters__reset" type="button" hidden>Скинути ✕</button>
      </div>

      <div class="cards cards--3 cases-grid" data-stagger>
      {"".join(card(k) for k in ORDER)}
      </div>
      <p class="cases-empty" hidden>У цій категорії кейси вже в роботі — скоро покажемо. <button type="button" class="link-btn" data-reset>Показати всі</button></p>
    </div>
  </section>
'''


# ---------------------------------------------------------------- case pages
def fig(name, alt):
    return f'''
      <figure class="figure" data-scroll><div class="container">{img(name, alt)}</div></figure>'''


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


def case_page(key, num, logo, logo_alt, logo_cls, partner, period, tagline, facts, content):
    c = CASES[key]
    i = ORDER.index(key)
    nxt = ORDER[(i + 1) % len(ORDER)]
    niche, services, tools = facts
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    return f'''
  <article class="case">
    <section class="case-intro pin" data-scroll>
      <img class="case-intro__badge" src="assets/img/case-badge-{num}.webp" alt="Кейс {num}" width="264" height="264">
      <img class="case-intro__logo {logo_cls}" src="assets/img/{logo}.webp" alt="{logo_alt}" {dims(logo)} fetchpriority="high">
    </section>

    <div class="layer">
      <section class="case-hero section" data-scroll>
        <div class="container">
          <div class="case-hero__top"><span>{partner} × SUBMARINE</span><span>Період співпраці: {period}</span></div>
          <div class="case-hero__body">
            <div class="media">{img(f"{key}-hero", c["alt"], "(min-width: 900px) 62vw, 100vw")}</div>
            <div class="case-hero__brand">
              <img src="assets/img/{logo}.webp" alt="" {dims(logo)} loading="lazy">
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
    "okko", 1, "okko-logo", "OKKO", "", "OKKO", "2018–2025", "8 років у режимі non-stop",
    ("АЗК та автомобільний сектор", ["Стратегія", "SMM", "Креатив", "Продакшн", "Спецпроєкти"],
     ["Instagram", "Facebook", "Digital Media"]),
    stage("01 — Задача", "8 років комунікації, яка не зупиняється",
          "SUBMARINE стала частиною щоденної комунікації OKKO: від SMM-стратегії до продакшну, кампаній і спецпроєктів. Ми працювали з продуктами, сервісами, ситуативами та соціальними ініціативами — разом із брендом постійно рухали комунікацію АЗК, зважаючи на настрій аудиторії та світу навколо.")
    + fig("okko-stats", "+130 зйомок, +16 000 кадрів, +3800 відео")
    + stage("02 — Ідея", "Ми винайшли тисячі способів не повторюватись та залишатись в контексті",
            "Їжа, сервіси, меми, ситуативи, великі кампанії та соціальні ініціативи — за 8 років співпраці OKKO розповідало про своє життя, ритм та вподобання гостей, завжди залишаючись впізнаваним.")
    + fig("okko-collage", "Колаж кадрів зі зйомок OKKO: їжа, кава, гості на АЗК")
    + stage("03 — Виконання", "Продукти, сервіси, ситуативи та соціальні ініціативи")
    + fig("okko-feed-1", "Публікації OKKO в Instagram: айс-меню, ціни на пальне, новинки")
    + fig("okko-feed-2", "Соціальні ініціативи OKKO в Instagram: пульстрони, дронопад, допомога військовим")
    + stage("04 — Результати", "Результати співпраці",
            "Ми фокусувалися не лише на зростанні фанбази, а на побудові активного ком’юніті. Постійно шукали нові теми, формати та приводи для взаємодії, щоб комунікація розвивалася разом із брендом та його аудиторією.",
            "Результат: +199 095 нових підписників на двох платформах і ком’юніті, яке продовжує зростати.")
    + fig("okko-results", "Профіль OKKO в Instagram до та після співпраці"),
)

SAMOKUS = case_page(
    "samokus", 2, "samokus-logo", "Samokus", "case-intro__logo--tall", "SAMOKUS", "травень–червень 2026",
    "Морозимо для тих, кого любимо",
    ("Pet Care", ["SMM-стратегія", "Комплексний SMM", "Креатив", "Продакшн", "Key visual", "Медіа та інфлюенс-маркетинг"],
     ["Instagram", "UGC / UGC Creators", "Creative Production", "Consulting"]),
    stage("01 — Задача", "Запуск бренду",
          "Виклик: познайомити аудиторію з абсолютно новим брендом та пояснити продукт, про який більшість собачників навіть не чула.")
    + stage("02 — Ідея", "Власний характер SAMOKUS",
            "Ми почали з дослідження ринку та аудиторії, розробили стратегію просування, унікальний Tone of Voice та Key Visual. І свідомо відмовившись від звичних для pet-категорії візуальних і вербальних кліше, створили власний характер SAMOKUS.")
    + fig("samokus-strategy", "Фрагменти стратегії Samokus: цілі, аналіз Tone of Voice, слова та фрази-фішки")
    + fig("samokus-brand", "Айдентика Samokus: кольорова палітра, аватарки, highlights, шрифти та сторіс")
    + stage("03 — Виконання", "Контент і продакшн",
            "Основою комунікації зробили справжніх собак та їх емоції. AI використовували точково — для легкого розважального контенту, який доповнював живі фото- та відеозйомки.",
            "А коли SAMOKUS почав активно з’являтися на офлайн-подіях — інтегрували їх у контент, знайомлячи з брендом не лише власників собак, а й потенційних B2B-партнерів.")
    + fig("samokus-photos", "Фотозйомка собак різних порід із морозивом Samokus")
    + fig("samokus-feed", "Публікації Samokus в Instagram: смаки, інструкції, розіграш")
    + fig("samokus-reels", "Кадри з Reels Samokus")
    + stage("03 — Інфлюенс", "Слово дегустаторам",
            "Щоб новий продукт швидше знаходив свою аудиторію, ми залучили pet-блогерів та UGC-креаторів: сформували базу релевантних dog-акаунтів і супроводжували бартерні співпраці — від перших домовленостей до виходу контенту.")
    + fig("samokus-ugc", "UGC-контент pet-блогерів із морозивом Samokus")
    + stage("04 — Результати", "Результати співпраці",
            "За перший місяць ми сформували впізнаваний характер бренду, познайомили людей із новою продуктовою категорією та заклали основу для подальшого розвитку комунікації.")
    + fig("samokus-results", "Доберман тримає лапу на стаканчику морозива Samokus"),
)

KURIAR = case_page(
    "kuriar", 3, "kuriar-logo", "Куріяр", "case-intro__logo--tall", "КУРІЯР", "лютий 2026 — дотепер",
    "Від виробництва до вашої стрічки",
    ("FMCG / Продукти та напої", ["SMM-стратегія", "Комплексний SMM", "Креатив", "Продакшн", "Медіа та інфлюенс-маркетинг"],
     ["Instagram", "Facebook", "AI Generation", "Meta Ads", "Фото- та відеопродакшн"]),
    stage("01 — Задача", "Скільки можна говорити про курку? Виявилося, багато",
          "Куріяр прийшов до нас із завданням побудувати системну присутність бренду в Instagram та Facebook. Але просто регулярно показувати курятину — не наш метод.")
    + stage("02 — Ідея", "Курятина — лише початок розмови",
            "Ми адаптували бренд-стратегію до соцмереж: розробили SMM-стратегію, визначили принципи комунікації, візуальний напрям і контентні рубрики.",
            "Так з’явилася система, у якій курятина — лише початок розмови. Далі — рецепти, виробництво, люди, партнери та креативні експерименти.")
    + fig("kuriar-strategy", "Фрагменти стратегії Куріяр: цілі в соцмережах, мудборд, спосіб споживання")
    + fig("kuriar-brand", "«Спочатку була курка»: обкладинки Facebook, highlights та публікації Куріяр")
    + stage("03 — Виконання", "Контент і продакшн",
            "Знімаємо Куріяр там, де вирує його справжнє життя: на виробництві, у фірмових магазинах, офісі та на виїзних подіях. Показуємо не лише продукт, а й людей, процеси та історії, які стоять за брендом.",
            "А коли реальності стає замало — підключаємо AI. Створюємо контент, експериментуємо із сюжетами та втілюємо ідеї, для яких звичайного знімального майданчика було б недостатньо.",
            "Так у стрічці Куріяру поєднуються справжнє життя бренду та креатив, який виходить за його межі.")
    + stage("04 — Результати", "Результати співпраці",
            "Системна робота зі стратегією, контентом, продакшном та креативами дає вимірювані результати. За час співпраці ми збільшили аудиторію в Instagram більш ніж у 4 рази, а у Facebook — у 3,5 раза.",
            "І це не фінальні результати. Ми продовжуємо експериментувати з форматами, знаходити нові точки контакту з аудиторією та розвивати присутність бренду в соцмережах.")
    + kpis(("×4+", "аудиторія в Instagram"), ("×3,5", "аудиторія у Facebook"))
    + fig("kuriar-results", "Куряче стегно зі спеціями та імбиром на жовтому тлі"),
)

page("index.html", "Портфоліо — Submarine Creative Agency",
     "Портфоліо Submarine Creative Agency: стратегія, креатив, SMM та інфлюенс-маркетинг з 2018 року.",
     "home", HOME, home=True)
page("okko.html", "OKKO — кейс Submarine", "OKKO × Submarine: 8 років комунікації АЗК у режимі non-stop.", "okko", OKKO)
page("samokus.html", "Samokus — кейс Submarine", "Samokus × Submarine: запуск бренду морозива для собак.", "samokus", SAMOKUS)
page("kuriar.html", "Куріяр — кейс Submarine", "Куріяр × Submarine: системна присутність бренду в Instagram та Facebook.", "kuriar", KURIAR)
print("built 4 pages")
