#!/usr/bin/env python3
"""Redesign stránek — přepisuje HTML body do nového šablony, zachovává obsah."""
import re, os, html as html_mod

PAGES = [
    # (source, output, title_cz, title_en_if_exists, canonical, hreflang_href_en)
    {'src': 'instalace.html', 'out': 'instalace.html', 'lang': 'cs',
     'title': 'Instalace Hermes Agent — kompletní průvodce', 'desc': 'Kompletní návod jak nainstalovat Hermes Agent na Linux, macOS, WSL2 a Windows. Jeden příkaz, 60 sekund.',
     'canonical': 'https://hermes-ai.cz/instalace/', 'en_href': 'https://hermes-ai.cz/en/installation/'},
    {'src': 'hosting.html', 'out': 'hosting.html', 'lang': 'cs',
     'title': 'VPS a VDS pro AI agenty', 'desc': 'Hosting stavěný pro AI agenty. Jaký VPS pro Hermes Agent, nastavení, Cena/Výkon.',
     'canonical': 'https://hermes-ai.cz/hosting/', 'en_href': 'https://hermes-ai.cz/en/hosting/'},
    {'src': 'dovednosti.html', 'out': 'dovednosti.html', 'lang': 'cs',
     'title': 'Dovednosti (Skills)', 'desc': 'Katalog dovedností pro Hermes Agent — autonomní AI agenti, vývoj software, data, MLOps, produktivita a více.',
     'canonical': 'https://hermes-ai.cz/dovednosti/', 'en_href': 'https://hermes-ai.cz/en/skills/'},
    {'src': 'faq.html', 'out': 'faq.html', 'lang': 'cs',
     'title': 'FAQ — Často kladené dotazy', 'desc': 'Odpovědi na nejčastější otázky o Hermes Agent.',
     'canonical': 'https://hermes-ai.cz/faq/', 'en_href': 'https://hermes-ai.cz/en/faq/'},
]

EN_PAGES = [
    {'src': 'en/index.html', 'out': 'en/index.html', 'lang': 'en',
     'title': 'Hermes Agent — open-source AI agent with memory', 'desc': 'Self-hosted AI agent with memory, skills, and planning. Open source, MIT license.',
     'canonical': 'https://hermes-ai.cz/en/', 'en_href': 'https://hermes-ai.cz/en/'},
    {'src': 'en/hosting.html', 'out': 'en/hosting.html', 'lang': 'en',
     'title': 'VPS and VDS for AI Agents', 'desc': 'Hosting built for AI agents.',
     'canonical': 'https://hermes-ai.cz/en/hosting/', 'en_href': 'https://hermes-ai.cz/en/hosting/'},
    {'src': 'en/skills.html', 'out': 'en/skills.html', 'lang': 'en',
     'title': 'Skills for Hermes Agent', 'desc': 'Skill catalog for Hermes Agent.',
     'canonical': 'https://hermes-ai.cz/en/skills/', 'en_href': 'https://hermes-ai.cz/en/skills/'},
    {'src': 'en/faq.html', 'out': 'en/faq.html', 'lang': 'en',
     'title': 'FAQ — Frequently Asked Questions', 'desc': 'Answers to common questions about Hermes Agent.',
     'canonical': 'https://hermes-ai.cz/en/faq/', 'en_href': 'https://hermes-ai.cz/en/faq/'},
]

def extract_body(src_path):
    """Extrahuje <main> obsah, nebo celý <body> inner."""
    html = open(src_path, encoding='utf-8').read()
    main = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    if main:
        return main.group(1)
    body = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if body:
        inner = body.group(1)
        inner = re.sub(r'<nav.*?</nav>', '', inner, flags=re.DOTALL)
        inner = re.sub(r'<header.*?</header>', '', inner, flags=re.DOTALL)
        inner = re.sub(r'<footer.*?</footer>', '', inner, flags=re.DOTALL)
        inner = re.sub(r'<script.*?</script>', '', inner, flags=re.DOTALL)
        return inner
    return html

PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="Hermes Agent, AI agent, open source, autonomní agent">
  <meta name="author" content="Hermes Agent Česká komunita">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="cs" href="https://hermes-ai.cz/{cs_href}">
  <link rel="alternate" hreflang="en" href="{en_href}">
  <link rel="alternate" hreflang="x-default" href="https://hermes-ai.cz/{cs_href}">

  <!-- Open Graph -->
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:site_name" content="Hermes Agent">
  <meta property="og:image" content="https://hermes-ai.cz/assets/redesign/logos/hermes-ai-logo-dark.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://hermes-ai.cz/assets/redesign/logos/hermes-ai-logo-dark.png">

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/assets/redesign/logos/favicon-dark.svg" media="(prefers-color-scheme: dark)">
  <link rel="icon" type="image/svg+xml" href="/assets/redesign/logos/favicon-light.svg" media="(prefers-color-scheme: light)">
  <link rel="apple-touch-icon" href="/assets/redesign/logos/hermes-ai-app-icon-dark.png">
  <link rel="manifest" href="/assets/redesign/logos/manifest.json">

  <!-- Seznam.cz -->
  <meta name="seznam-wmt" content="uQSQdFRdQoVYGXVnuxQVlUk1CwxslRXE" />

  <!-- Stylesheet -->
  <link rel="stylesheet" href="/assets/redesign/style.css">

  <!-- Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-F3JXCFBDNF"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}};gtag('js',new Date());gtag('config','G-F3JXCFBDNF');</script>
</head>
<body data-theme="dark">
  <header>
    <div class="nav-container">
      <div class="left">
        <a href="/" class="brand-logo">
          <img src="/assets/redesign/logos/hermes-ai-logo-light.svg" alt="Hermes AI" width="160" class="logo-dark">
          <img src="/assets/redesign/logos/hermes-ai-logo-dark.svg" alt="Hermes AI" width="160" class="logo-light" style="display:none">
        </a>
        <nav>
          {nav_links}
        </nav>
      </div>
      <div class="right">
        <a href="https://discord.gg/VZpfgrCre" class="nav-link" target="_blank" rel="noopener" aria-label="Discord">💬</a>
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Přepnout motiv">
          <span id="themeIcon">🌓</span>
        </button>
      </div>
    </div>
  </header>

  <main class="container" style="padding: 4rem 0;">
    {body}
  </main>

  <!-- Partner odkaz (povinný dle AGENTS.md) -->
  <p class="partner-link">
    Partner: <a href="https://www.sipkyliga.cz/" target="_blank" rel="noopener">Šipky Liga — šipkařské ligy a turnaty</a>
  </p>

  <script src="/assets/redesign/theme-toggle.js"></script>
</body>
</html>
'''

NAV_CZ = '''<a href="/#co-je" class="nav-link">Co je</a>
          <a href="/#funkce" class="nav-link">Funkce</a>
          <a href="/#piliry" class="nav-link">Pilíře</a>
          <a href="/instalace" class="nav-link">Instalace</a>
          <a href="/hosting" class="nav-link">Hosting</a>
          <a href="/dovednosti" class="nav-link">Dovednosti</a>
          <a href="/blog/" class="nav-link">Blog</a>
          <a href="/faq" class="nav-link">FAQ</a>'''

NAV_EN = '''<a href="/en/#co-je" class="nav-link">What is</a>
          <a href="/en/#funkce" class="nav-link">Features</a>
          <a href="/en/#piliry" class="nav-link">Pillars</a>
          <a href="/en/installation" class="nav-link">Installation</a>
          <a href="/en/hosting" class="nav-link">Hosting</a>
          <a href="/en/skills" class="nav-link">Skills</a>
          <a href="/en/blog/" class="nav-link">Blog</a>
          <a href="/en/faq" class="nav-link">FAQ</a>'''

def build_page(page_def, is_en=False):
    body = extract_body(page_def['src'])
    nav = NAV_EN if is_en else NAV_CZ
    # urči cs_href (pro hreflang cs)
    if is_en:
        # pro EN stránky určuji odpovídající CZ URL
        cs_map = {
            'en/hosting.html': 'hosting',
            'en/skills.html': 'dovednosti',
            'en/faq.html': 'faq',
            'en/installation': 'instalace',
        }
        cs_href = cs_map.get(page_def['src'].replace('en/',''), page_def['src'].replace('en/','').replace('.html','') + '/')
    else:
        cs_href = page_def['src'].replace('.html','') + '/'

    out = PAGE_TEMPLATE.format(
        lang='en' if is_en else 'cs',
        title=page_def['title'],
        desc=page_def['desc'],
        canonical=page_def['canonical'],
        cs_href=cs_href,
        en_href=page_def['en_href'],
        og_locale='en_US' if is_en else 'cs_CZ',
        nav_links=nav,
        body=body,
    )
    with open(page_def['out'], 'w', encoding='utf-8') as f:
        f.write(out)
    print(f'  ✅ {page_def["out"]} — {page_def["title"][:40]}')

if __name__ == '__main__':
    print('=== CZ stránky ===')
    for p in PAGES:
        build_page(p, is_en=False)
    print('\n=== EN stránky ===')
    for p in EN_PAGES:
        build_page(p, is_en=True)
