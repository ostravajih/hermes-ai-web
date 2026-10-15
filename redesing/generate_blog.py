#!/usr/bin/env python3
"""Generátor blogu pro redesign — přepisuje head + generuje index/pagination."""
import glob, re, os, json

# Mapování slug -> (CZ název, EN název) pro hreflang cross-reference
SLUG_PAIRS = {
    'ai-agent-na-vps-contabo': ('blog/ai-agent-na-vps-contabo.html', 'en/blog/ai-agent-on-vps-contabo.html'),
    'bezpecnost-hermes-agent': ('blog/bezpecnost-hermes-agent.html', 'en/blog/hermes-agent-security.html'),
    'hermes-agent-aktualizace-2026': ('blog/hermes-agent-aktualizace-2026.html', 'en/blog/hermes-agent-updates-2026.html'),
    'hermes-agent-cron-planovac': ('blog/hermes-agent-cron-planovac.html', 'en/blog/hermes-agent-cron-scheduler.html'),
    'hermes-agent-docker': ('blog/hermes-agent-docker.html', 'en/blog/hermes-agent-docker.html'),
    'hermes-agent-google-gemini': ('blog/hermes-agent-google-gemini.html', 'en/blog/hermes-agent-google-gemini.html'),
    'hermes-agent-macos': ('blog/hermes-agent-macos.html', 'en/blog/hermes-agent-macos.html'),
    'hermes-agent-mcp-integration': ('blog/hermes-agent-mcp-integration.html', 'en/blog/hermes-agent-mcp-integration.html'),
    'hermes-agent-multi-platform': ('blog/hermes-agent-multi-platform.html', 'en/blog/hermes-agent-multi-platform.html'),
    'hermes-agent-nous-portal': ('blog/hermes-agent-nous-portal.html', 'en/blog/hermes-agent-nous-portal.html'),
    'hermes-agent-ollama-lokalni-llm': ('blog/hermes-agent-ollama-lokalni-llm.html', 'en/blog/hermes-agent-ollama-local-llm.html'),
    'hermes-agent-open-source': ('blog/hermes-agent-open-source.html', 'en/blog/hermes-agent-open-source.html'),
    'hermes-agent-openrouter': ('blog/hermes-agent-openrouter.html', 'en/blog/hermes-agent-openrouter.html'),
    'hermes-agent-profily': ('blog/hermes-agent-profily.html', 'en/blog/hermes-agent-profiles.html'),
    'hermes-agent-raspberry-pi': ('blog/hermes-agent-raspberry-pi.html', 'en/blog/hermes-agent-raspberry-pi.html'),
    'hermes-agent-soul-md': ('blog/hermes-agent-soul-md.html', 'en/blog/hermes-agent-soul-md.html'),
    'hermes-agent-ssh-vps': ('blog/hermes-agent-ssh-vps.html', 'en/blog/hermes-agent-ssh-vps.html'),
    'hermes-agent-system-admin': ('blog/hermes-agent-system-admin.html', 'en/blog/hermes-agent-system-admin.html'),
    'hermes-agent-voice-mode': ('blog/hermes-agent-voice-mode.html', 'en/blog/hermes-agent-voice-mode.html'),
    'hermes-agent-vs-claude-code': ('blog/hermes-agent-vs-claude-code.html', 'en/blog/hermes-agent-vs-claude-code.html'),
    'hermes-agent-vs-codex': ('blog/hermes-agent-vs-codex.html', 'en/blog/hermes-agent-vs-codex.html'),
    'hermes-agent-vs-openclaw': ('blog/hermes-agent-vs-openclaw.html', 'en/blog/hermes-agent-vs-openclaw.html'),
    'hermes-agent-windows-wsl2': ('blog/hermes-agent-windows-wsl2.html', 'en/blog/hermes-agent-windows-wsl2.html'),
    'hermes-webui-pruvodce': ('blog/hermes-webui-pruvodce.html', 'en/blog/hermes-webui-guide.html'),
    'instalace-hermes-agent-ubuntu': ('blog/instalace-hermes-agent-ubuntu.html', 'en/blog/install-hermes-agent-ubuntu.html'),
    'jak-pouzivat-hermes-skills': ('blog/jak-pouzivat-hermes-skills.html', 'en/blog/how-to-use-hermes-skills.html'),
    'telegram-bot-hermes-agent': ('blog/telegram-bot-hermes-agent.html', 'en/blog/telegram-bot-hermes-agent.html'),
}

def extract_meta(html):
    """Extrahuje title, description, og:title, og:description, og:image, date."""
    def grab(pattern):
        m = re.search(pattern, html, re.DOTALL)
        return m.group(1).strip() if m else ''

    title = grab(r'<title>(.*?)</title>') or grab(r'<title>(.*?)(?:</title>|<meta)')
    title = title.replace(' | Blog', '').strip()
    desc = grab(r'name="description" content="([^"]+)"')
    og_title = grab(r'property="og:title" content="([^"]+)"') or title
    og_desc = grab(r'property="og:description" content="([^"]+)"') or desc
    # datum: hledáme <time> nebo datum v textu
    date_m = re.search(r'(\d{4}-\d{2}-\d{2})', html)
    date = date_m.group(1) if date_m else '2026-10-01'
    return {'title': title, 'desc': desc, 'og_title': og_title, 'og_desc': og_desc, 'date': date}

def extract_body(html):
    """Extrahuje část mezi <article> a </article>, nebo celý <main>...</main>, nebo <body>...</body>."""
    article = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
    if article:
        return article.group(1)
    main = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if main:
        return main.group(1)
    body = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if body:
        # odebereme header a footer pokud jsou <body>
        inner = body.group(1)
        inner = re.sub(r'<header.*?</header>', '', inner, flags=re.DOTALL)
        inner = re.sub(r'<footer.*?</footer>', '', inner, flags=re.DOTALL)
        inner = re.sub(r'<script.*?</script>', '', inner, flags=re.DOTALL)
        return inner
    return html

def build_head(title, desc, og_title, og_desc, date, canonical, lang_href, lang_href_en, og_img='https://hermes-ai.cz/assets/redesign/logos/hermes-ai-logo-dark.png'):
    gtag_js = 'window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-F3JXCFBDNF");'
    schema = json.dumps({"@context":"https://schema.org","@type":"BlogPosting","headline":og_title,"description":og_desc,"datePublished":date,"dateModified":date,"url":canonical,"author":{"@type":"Organization","name":"Hermes Agent Česká komunita"}})
    return f'''<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="Hermes Agent, AI agent, open source">
  <meta name="author" content="Hermes Agent Česká komunita">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="cs" href="https://hermes-ai.cz/{lang_href}/">
  <link rel="alternate" hreflang="en" href="https://hermes-ai.cz/{lang_href_en}/">
  <link rel="alternate" hreflang="x-default" href="https://hermes-ai.cz/{lang_href}/">

  <!-- Open Graph -->
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="cs_CZ">
  <meta property="og:site_name" content="Hermes Agent">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og_img}">

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/assets/redesign/logos/favicon-dark.svg" media="(prefers-color-scheme: dark)">
  <link rel="icon" type="image/svg+xml" href="/assets/redesign/logos/favicon-light.svg" media="(prefers-color-scheme: light)">
  <link rel="apple-touch-icon" href="/assets/redesign/logos/hermes-ai-app-icon-dark.png">
  <link rel="manifest" href="/assets/redesign/logos/manifest.json">

  <!-- Seznam -->
  <meta name="seznam-wmt" content="uQSQdFRdQoVYGXVnuxQVlUk1CwxslRXE">

  <!-- Stylesheet -->
  <link rel="stylesheet" href="/assets/redesign/style.css">

  <!-- Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-F3JXCFBDNF"></script>
  <script>{gtag_js}</script>

  <!-- Schema.org -->
  <script type="application/ld+json">
  {schema}
  </script>
</head>'''

# ===== GENEROVÁNÍ ČLÁNKŮ =====
def process_blog(lang='cs'):
    for slug, (cz_name, en_name) in SLUG_PAIRS.items():
        if lang == 'cs':
            fpath = cz_name                     # už obsahuje blog/
            slug_cz = cz_name.replace('.html','')
            canonical = f'https://hermes-ai.cz/{slug_cz}/'
            out_path = slug_cz + '.html'        # blog/<slug>.html
            lang_href = slug_cz
            lang_href_en = en_name.replace('.html','')
        else:
            fpath = en_name                  # už obsahuje en/blog/
            slug_en = en_name.replace('.html','')   # en/blog/<slug>
            canonical = f'https://hermes-ai.cz/{slug_en}/'
            out_path = slug_en + '.html'     # en/blog/<slug>.html
            lang_href_en = slug_en
            lang_href = cz_name.replace('.html','')

        if not os.path.exists(fpath):
            print(f'  ⚠️  SKIP (neexistuje): {fpath}')
            continue

        with open(fpath, encoding='utf-8') as f:
            html = f.read()

        meta = extract_meta(html)
        body = extract_body(html)

        # pro EN musíme fixnout og:title/description
        og_title = meta['og_title']
        if not og_title or og_title.startswith('Hermes') == False:
            og_title = meta['title']
        og_desc = meta['og_desc'] if meta['og_desc'] else meta['desc']
        title_for_head = meta['title']
        desc_for_head = meta['desc']

        head = build_head(
            title=title_for_head,
            desc=desc_for_head,
            og_title=og_title,
            og_desc=og_desc,
            date=meta['date'],
            canonical=canonical,
            lang_href=lang_href,
            lang_href_en=lang_href_en
        )

        full_html = f'''<!DOCTYPE html>
<html lang="{'cs' if lang=='cs' else 'en'}">
{head}
<body data-theme="dark">
  <!-- Header -->
  <header>
    <div class="nav-container">
      <div class="left">
        <a href="/" class="brand-logo">
          <img src="/assets/redesign/logos/hermes-ai-logo-light.svg" alt="Hermes AI" width="160" class="logo-dark">
          <img src="/assets/redesign/logos/hermes-ai-logo-dark.svg" alt="Hermes AI" width="160" class="logo-light" style="display:none">
        </a>
        <nav>
          <a href="/#co-je" class="nav-link">Co je</a>
          <a href="/#funkce" class="nav-link">Funkce</a>
          <a href="/#piliry" class="nav-link">Pilíře</a>
          <a href="/instalace" class="nav-link">Instalace</a>
          <a href="/hosting" class="nav-link">Hosting</a>
          <a href="/skills" class="nav-link">Dovednosti</a>
          <a href="/blog/" class="nav-link">Blog</a>
          <a href="/faq" class="nav-link">FAQ</a>
        </nav>
      </div>
      <div class="right">
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Přepnout motiv">
          <span id="themeIcon">🌓</span>
        </button>
      </div>
    </div>
  </header>

  <main class="container" style="padding: 4rem 0;">
    <article class="blog-post">
      <header class="blog-post-header" style="margin-bottom: 3rem; padding-bottom: 2rem; border-bottom: 1px solid var(--border);">
        <div style="display: flex; gap: .75rem; align-items: center; margin-bottom: 1rem;">
          <span class="blog-category" style="background: var(--surface-2); color: var(--primary); font-size: .8rem; font-weight: 600; padding: .25rem .7rem; border-radius: var(--radius-sm);">Blog</span>
          <time datetime="{meta['date']}" style="color: var(--text-muted); font-size: .875rem;">{meta['date']}</time>
        </div>
        {('<h1>' + og_title + '</h1>') if lang == 'en' else ('<h1>' + meta['title'] + '</h1>')}
        <p style="color: var(--text-muted); font-size: 1.0625rem; line-height: 1.7; margin-top: 1rem;">{desc_for_head}</p>
      </header>
      <div class="blog-post-content">
        {body}
      </div>
    </article>
  </main>

  <!-- Footer -->
  <footer>
    <div class="footer-content container">
      <p style="font-size: .8125rem; color: var(--text-muted);">
        © 2026 Hermes Agent Česká komunita · <a href="https://github.com/NousResearch/hermes-agent">GitHub</a> · <a href="https://hermes-agent.nousresearch.com/docs">Dokumentace</a>
      </p>
      <p class="partner-link">
        Partner: <a href="https://www.sipkyliga.cz/" target="_blank" rel="noopener">Šipky Liga — šipkařské ligy a turnaje</a>
      </p>
    </div>
  </footer>
  <script src="/assets/redesign/theme-toggle.js"></script>
</body>
</html>'''

        # Zápis
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f'  ✅ {out_path} — {meta["title"][:45]}')

# ===== GENEROVÁNÍ BLOG INDEXU =====
def generate_blog_index(lang='cs', page=1, per_page=8):
    posts = sorted([(slug, cz, en) for slug, (cz, en) in SLUG_PAIRS.items() if os.path.exists(cz if lang=='cs' else en)])
    total = len(posts)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    page_posts = posts[start:start+per_page]

    cards_html = ''
    for slug, cz, en in page_posts:
        if lang == 'cs':
            fname = cz                           # blog/<name>.html
            url = '/' + cz.replace('.html','') + '/'
            title_path = fname
        else:
            fname = en                           # en/blog/<name>.html
            slug_en = en.replace('.html','')     # en/blog/<slug>
            url = '/' + slug_en + '/'
            title_path = fname
        txt = open(title_path, encoding='utf-8').read()
        meta = extract_meta(txt)
        img_name = slug.replace('-', '-')
        cards_html += f'''<a href="{url}" class="blog-card">
          <img src="/assets/redesign/images/sections/blog-documentation.webp" alt="" class="blog-card-img">
          <div class="blog-card-body">
            <span class="blog-card-category">Blog</span>
            <h3 class="blog-card-title">{meta['title']}</h3>
            <p class="blog-card-excerpt">{meta['desc'][:120]}…</p>
            <span class="blog-card-date">{meta['date']}</span>
          </div>
        </a>'''

    # pagination links
    def pg_link(p, label):
        if lang == 'cs':
            return f'/blog/stranka-{p}.html' if p > 1 else '/blog/'
        else:
            return f'/en/blog/page-{p}.html' if p > 1 else '/en/blog/'

    prev = pg_link(page-1, '←') if page > 1 else '#'
    next_l = pg_link(page+1, '→') if page < total_pages else '#'

    prev_disabled = " class='disabled'" if page == 1 else ""
    next_disabled = " class='disabled'" if page == total_pages else ""

    index_html = f'''<!DOCTYPE html>
<html lang="{'cs' if lang=='cs' else 'en'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Blog — Hermes Agent | Čeština</title>
  <meta name="description" content="Blog o Hermes Agent — open-source AI agent od Nous Research. Návody, tutoriály, srovnání a novinky.">
  <meta name="author" content="Hermes Agent Česká komunita">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{'https://hermes-ai.cz/blog/' if page==1 else f'https://hermes-ai.cz/blog/stranka-{page}/'}">
  <link rel="alternate" hreflang="cs" href="https://hermes-ai.cz/blog/">
  <link rel="alternate" hreflang="en" href="https://hermes-ai.cz/en/blog/">
  <meta property="og:title" content="Blog — Hermes Agent">
  <meta property="og:description" content="Blog o Hermes Agent — návody, tutoriály, novinky.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://hermes-ai.cz/blog/">
  <meta property="og:image" content="https://hermes-ai.cz/assets/redesign/logos/hermes-ai-logo-dark.png">
  <link rel="icon" type="image/svg+xml" href="/assets/redesign/logos/favicon-dark.svg" media="(prefers-color-scheme: dark)">
  <link rel="icon" type="image/svg+xml" href="/assets/redesign/logos/favicon-light.svg" media="(prefers-color-scheme: light)">
  <link rel="stylesheet" href="/assets/redesign/style.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-F3JXCFBDNF"></script>
GASCRIPT
</head>
<body data-theme="dark">
  <!-- reuse header from index -->
  <header><div class="nav-container"><div class="left"><a href="/" class="brand-logo">
    <img src="/assets/redesign/logos/hermes-ai-logo-light.svg" alt="Hermes AI" width="160" class="logo-dark">
    <img src="/assets/redesign/logos/hermes-ai-logo-dark.svg" alt="Hermes AI" width="160" class="logo-light" style="display:none">
  </a><nav>
    <a href="/#co-je" class="nav-link">Co je</a>
    <a href="/#funkce" class="nav-link">Funkce</a>
    <a href="/#piliry" class="nav-link">Pilíře</a>
    <a href="/instalace" class="nav-link">Instalace</a>
    <a href="/hosting" class="nav-link">Hosting</a>
    <a href="/skills" class="nav-link">Dovednosti</a>
    <a href="/blog/" class="nav-link">Blog</a>
    <a href="/faq" class="nav-link">FAQ</a>
  </nav></div>
  <div class="right">
    <button class="theme-toggle" onclick="toggleTheme()" aria-label="Přepnout motiv">
      <span id="themeIcon">🌓</span>
    </button>
  </div></div></header>

  <main class="container" style="padding: 4rem 0;">
    <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">Blog</h1>
    <p style="color: var(--text-muted); margin-bottom: 3rem;">Návody, tutoriály, srovnání a novinky o Hermes Agent.</p>

    <div class="blog-grid">
      {cards_html}
    </div>

    <nav class="blog-pagination" style="margin-top: 3rem; display: flex; justify-content: center; gap: 1rem;">
      <a href="{prev}"{prev_disabled} class="btn-outline">← Předchozí</a>
      <span style="align-self: center; color: var(--text-muted); font-size: .875rem;">Stránka {page} z {total_pages}</span>
      <a href="{next_l}"{next_disabled} class="btn-outline">Další →</a>
    </nav>
  </main>

  <footer>
    <div class="footer-content container">
      <p style="font-size: .8125rem; color: var(--text-muted);">© 2026 Hermes Agent Česká komunita · <a href="https://github.com/NousResearch/hermes-agent">GitHub</a></p>
      <p class="partner-link">Partner: <a href="https://www.sipkyliga.cz/" target="_blank" rel="noopener">Šipky Liga — šipkařské ligy a turnaje</a></p>
    </div>
  </footer>
  <script src="/assets/redesign/theme-toggle.js"></script>
</body>
</html>'''

    # urči výstupní cestu
    if lang == 'cs':
        out = f'blog/index.html' if page == 1 else f'blog/stranka-{page}.html'
    else:
        out = f'en/blog/index.html' if page == 1 else f'en/blog/page-{page}.html'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(index_html.replace('GASCRIPT', 'window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-F3JXCFBDNF\');'))
    print(f'  ✅ {out} (stránka {page}/{total_pages})')

if __name__ == '__main__':
    print('=== Generování blog článků CZ ===')
    process_blog('cs')
    print('\n=== Generování blog článků EN ===')
    process_blog('en')
    print('\n=== Generování CZ index/pagination ===')
    generate_blog_index('cs', 1)
    generate_blog_index('cs', 2)
    generate_blog_index('cs', 3)
    print('\n=== Generování EN index/pagination ===')
    generate_blog_index('en', 1)
    generate_blog_index('en', 2)
    generate_blog_index('en', 3)
