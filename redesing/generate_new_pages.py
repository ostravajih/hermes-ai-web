#!/usr/bin/env python3
"""Generátor nových stránek redesignu: co-je-hermes, funkce, komunita (CZ+EN) + redirecty."""
import os

NAV_CZ = '''<a href="/#co-je" class="nav-link">Co je</a>
          <a href="/#funkce" class="nav-link">Funkce</a>
          <a href="/#piliry" class="nav-link">Pilíře</a>
          <a href="/instalace" class="nav-link">Instalace</a>
          <a href="/hosting" class="nav-link">Hosting</a>
          <a href="/dovednosti" class="nav-link">Dovednosti</a>
          <a href="/blog/" class="nav-link">Blog</a>
          <a href="/faq" class="nav-link">FAQ</a>'''

NAV_EN = '''<a href="/#co-je" class="nav-link">What is</a>
          <a href="/#funkce" class="nav-link">Features</a>
          <a href="/#piliry" class="nav-link">Pillars</a>
          <a href="/instalace" class="nav-link">Installation</a>
          <a href="/hosting" class="nav-link">Hosting</a>
          <a href="/dovednosti" class="nav-link">Skills</a>
          <a href="/blog/" class="nav-link">Blog</a>
          <a href="/faq" class="nav-link">FAQ</a>'''

HEAD = '''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="Hermes Agent, AI agent, open source">
  <meta name="author" content="Hermes Agent Česká komunita">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="cs" href="https://hermes-ai.cz/{cs_href}">
  <link rel="alternate" hreflang="en" href="{en_href}">
  <link rel="alternate" hreflang="x-default" href="https://hermes-ai.cz/{cs_href}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{og_locale}">
  <meta property="og:site_name" content="Hermes Agent">
  <meta property="og:image" content="https://hermes-ai.cz/assets/redesign/logos/hermes-ai-logo-dark.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/assets/redesign/logos/favicon-dark.svg" media="(prefers-color-scheme: dark)">
  <link rel="icon" type="image/svg+xml" href="/assets/redesign/logos/favicon-light.svg" media="(prefers-color-scheme: light)">
  <link rel="stylesheet" href="/assets/redesign/style.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-F3JXCFBDNF"></script>
GASCRIPT
</head>
'''

FOOTER = '''  <!-- Partner odkaz (povinný dle AGENTS.md) -->
  <p class="partner-link">
    Partner: <a href="https://www.sipkyliga.cz/" target="_blank" rel="noopener">Šipky Liga — šipkařské ligy a turnaje</a>
  </p>

  <script src="/assets/redesign/theme-toggle.js"></script>
</body>
</html>
'''

def build_page(path, lang, title, desc, canonical, cs_href, en_href, og_locale, nav, body):
    ga = "window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-F3JXCFBDNF');"
    html = HEAD.format(lang=lang, title=title, desc=desc, canonical=canonical,
                       cs_href=cs_href, en_href=en_href, og_locale=og_locale).replace('GASCRIPT', ga)
    html = html.replace('{nav}', nav)
    html += body
    html += FOOTER
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w', encoding='utf-8').write(html)
    print(f'  ✅ {path} — {title[:40]}')

# ===== Body obsah (z index.html hero + rozšířený dle brand guide) =====
CO_JE_CZ = '''<body data-theme="dark">
  <header>
    <div class="nav-container">
      <div class="left">
        <a href="/" class="brand-logo">
          <img src="/assets/redesign/logos/hermes-ai-logo-light.svg" alt="Hermes AI" width="160" class="logo-dark">
          <img src="/assets/redesign/logos/hermes-ai-logo-dark.svg" alt="Hermes AI" width="160" class="logo-light" style="display:none">
        </a>
        <nav>
          {nav}
        </nav>
      </div>
      <div class="right">
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Přepnout motiv">🌓</button>
      </div>
    </div>
  </header>

  <main class="container" style="padding: 4rem 0;">
    <div class="section-header">
      <div class="section-tag">Základy</div>
      <h1>Co je Hermes Agent?</h1>
      <p>Open-source autonomní AI agent od Nous Research, vydaný v únoru 2026. Běží na Linuxu, macOS a WSL2 — bez závislostí, všechno nainstaluje jedním příkazem.</p>
    </div>

    <div style="display:flex;gap:3rem;flex-wrap:wrap;margin-top:3rem">
      <div style="flex:1;min-width:320px">
        <img src="/assets/redesign/images/sections/co-je-hermes.svg" alt="" style="border-radius:var(--radius-xl);box-shadow:var(--shadow)">
      </div>
      <div style="flex:1;min-width:320px;display:flex;flex-direction:column;gap:1.5rem">
        <div class="card" style="padding:1.5rem">
          <div class="card-icon"><img src="/assets/redesign/icons/skills.svg" alt="" width="24"></div>
          <h3>Persistentní paměť</h3>
          <p>Pamatuje si vaše preference, projekty a prostředí napříč všemi relacemi. Čím déle běží, tím lépe vás zná — žádné opakované vysvětlování kontextu. Všechna data zůstávají na vašem serveru ve složce ~/.hermes/ jako čitelné markdown.</p>
        </div>
        <div class="card" style="padding:1.5rem">
          <div class="card-icon"><img src="/assets/redesign/icons/tools.svg" alt="" width="24"></div>
          <h3>60+ vestavěných nástrojů</h3>
          <p>Web search, extrakce stránek, automatizace prohlížeče, spouštění kódu, analýza obrázků, generování obrázků, TTS, delegování sub-agentů, MCP a další. Vše jako vestavěné nástroje agenta.</p>
        </div>
        <div class="card" style="padding:1.5rem">
          <div class="card-icon"><img src="/assets/redesign/icons/message.svg" alt="" width="24"></div>
          <h3>20+ platforem</h3>
          <p>Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Email, SMS — vše z jedné gateway. Začněte na Telegramu, pokračujte v terminálu.</p>
        </div>
      </div>
    </div>

    <div class="section" style="padding: 0;">
      <h2>Tři pilíře, které ho odlišují</h2>
      <p>Většina nástrojů je skvělá v daném okamžiku, ale slabá v průběhu času. Hermes je jiný.</p>
      <div class="pillars" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.5rem">
        <div class="card" style="padding:1.5rem;text-align:center">
          <div class="pillar-icon">🧠</div>
          <h3>Paměť, která se kumuluje</h3>
          <p>Vrstvený paměťový systém: uživatelský profil, paměť agenta, dovednosti a historie relací. Vše lokálně jako markdown. Přežije restart i výměnu modelu.</p>
        </div>
        <div class="card" style="padding:1.5rem;text-align:center">
          <div class="pillar-icon">⏰</div>
          <h3>Autonomní plánování</h3>
          <p>Vestavěný cron plánovač s doručováním na jakoukoli platformu. Ranní briefingy, PR review, monitoring — vše bez vaší přítomnosti.</p>
        </div>
        <div class="card" style="padding:1.5rem;text-align:center">
          <div class="pillar-icon">📡</div>
          <h3>Dostupný odkudkoliv</h3>
          <p>Stejný agent, stejná paměť, různé platformy. Přepínejte mezi Telegramem, Discordem, terminálem nebo Web UI — kontext zůstává.</p>
        </div>
      </div>
    </div>
  </main>
'''

FUNCKCE_CZ = '''<body data-theme="dark">
  <header>
    <div class="nav-container">
      <div class="left">
        <a href="/" class="brand-logo">
          <img src="/assets/redesign/logos/hermes-ai-logo-light.svg" alt="Hermes AI" width="160" class="logo-dark">
          <img src="/assets/redesign/logos/hermes-ai-logo-dark.svg" alt="Hermes AI" width="160" class="logo-light" style="display:none">
        </a>
        <nav>
          {nav}
        </nav>
      </div>
      <div class="right">
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Přepnout motiv">🌓</button>
      </div>
    </div>
  </header>

  <main class="container" style="padding: 4rem 0;">
    <div class="section-header">
      <div class="section-tag">Kompletní výbava</div>
      <h1>Funkce Hermes Agenta</h1>
      <p>Všechny vestavěné nástroje, dovednosti, MCP integrace a platformní podpora.</p>
    </div>
    <img src="/assets/redesign/images/sections/funkce.svg" alt="" style="max-width:100%;border-radius:var(--radius-xl);margin:2rem 0;box-shadow:var(--shadow)">

    <div class="cards-grid" style="margin-top:3rem">
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/tools.svg" alt="" width="24"></div><h3>60+ vestavěných nástrojů</h3><p>Web search, extrakce stránek, prohlížeč, spouštění kódu, analýza obrázků, generování obrázků, TTS, delegování sub-agentů.</p></div>
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/memory.svg" alt="" width="24"></div><h3>Vrstvení paměť</h3><p>Profil uživatele, paměť agenta, dovednosti a historie relací. Vše jako čitelné markdown.</p></div>
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/skills.svg" alt="" width="24"></div><h3>Auto-skládání dovedností</h3><p>Agent si sám píše dovednosti ze zkušeností. Kompatibilní s agentskills.io.</p></div>
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/mcp.svg" alt="" width="24"></div><h3>MCP integrace</h3><p>Připojení k libovolnému MCP serveru. Hermes může také fungovat jako MCP server pro Claude Code, Cursor nebo Codex.</p></div>
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/terminal.svg" alt="" width="24"></div><h3>6 terminálních backendů</h3><p>Local, Docker, SSH, Daytona, Singularity, Modal. Od $5 VPS po serverless cloud.</p></div>
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/personality.svg" alt="" width="24"></div><h3>Osobnost a SOUL.md</h3><p>Definujte výchozí hlas agenta pomocí SOUL.md. 14 vestavěných osobností + vlastní.</p></div>
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/mic.svg" alt="" width="24"></div><h3>Hlasový režim</h3><p>Hlas v reálném čase v CLI, hlasové zprávy na Telegramu i Discordu. Podpora faster-whisper, Groq, OpenAI Whisper.</p></div>
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/mobile.svg" alt="" width="24"></div><h3>Responzivní Web UI</h3><p>Třípanelové rozhraní od nesquena. Light + dark režim. Česká lokalizace.</p></div>
    </div>
  </main>
'''

KOMUNITA_CZ = '''<body data-theme="dark">
  <header>
    <div class="nav-container">
      <div class="left">
        <a href="/" class="brand-logo">
          <img src="/assets/redesign/logos/hermes-ai-logo-light.svg" alt="Hermes AI" width="160" class="logo-dark">
          <img src="/assets/redesign/logos/hermes-ai-logo-dark.svg" alt="Hermes AI" width="160" class="logo-light" style="display:none">
        </a>
        <nav>
          {nav}
        </nav>
      </div>
      <div class="right">
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Přepnout motiv">🳚</button>
      </div>
    </div>
  </header>

  <main class="container" style="padding: 4rem 0;">
    <div class="section-header">
      <div class="section-tag">Česká komunita</div>
      <h1>Přidejte se k nám</h1>
      <p>Hermes Agent v češtině — lokalizace, podpora a komunita pro české a slovenské uživatele.</p>
    </div>
    <img src="/assets/redesign/images/sections/community.svg" alt="" style="max-width:100%;border-radius:var(--radius-xl);margin:2rem 0;box-shadow:var(--shadow)">

    <div class="cards-grid" style="margin-top:3rem">
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/czech.svg" alt="" width="24"></div><h3>Česká lokalizace</h3><p>Plný překlad Web UI do češtiny. Všechny klíče, menu, nastavení a dialogy.</p></div>
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/discord.svg" alt="" width="24"></div><h3>Discord komunita</h3><p>Pomoc s instalací, konfigurací, sdílení dovedností a nejnovější news. Připoj se na <a href="https://discord.gg/VZpfgrCre" target="_blank" rel="noopener">discord.gg/VZpfgrCre</a>.</p></div>
      <div class="card"><div class="card-icon"><img src="/assets/redesign/icons/blog.svg" alt="" width="24"></div><h3>Dokumentace a blog</h3><p>překlady oficiální dokumentace, tutoriály a návody pro začátečníky v češtině.</p></div>
    </div>

    <div class="section" style="padding:0;margin-top:3rem;text-align:center">
      <a href="https://discord.gg/VZpfgrCre" class="btn-primary" target="_blank" rel="noopener">💬 Připojit se na Discord</a>
    </div>
  </main>
'''

PAGES = [
    ('co-je-hermes.html', 'cs', 'Co je Hermes Agent?',
     'Open-source autonomní AI agent od Nous Research. 60+ nástrojů, 20+ platforem, MIT licence.',
     'https://hermes-ai.cz/co-je-hermes/', 'co-je-hermes/', 'https://hermes-ai.cz/en/co-je-hermes/', 'cs_CZ',
     NAV_CZ, CO_JE_CZ),
    ('funkce.html', 'cs', 'Funkce Hermes Agenta',
     'Kompletní seznam funkcí Hermes Agenta: 60+ nástrojů, paměť, skills, MCP, plánování, platformy.',
     'https://hermes-ai.cz/funkce/', 'funkce/', 'https://hermes-ai.cz/en/funkce/', 'cs_CZ',
     NAV_CZ, FUNCKCE_CZ),
    ('komunita.html', 'cs', 'Komunita — Hermes Agent Česká komunita',
     'Podpora, lokalizace a komunita pro české a slovenské uživatele Hermes Agent.',
     'https://hermes-ai.cz/komunita/', 'komunita/', 'https://hermes-ai.cz/en/komunita/', 'cs_CZ',
     NAV_CZ, KOMUNITA_CZ),
    ('en/co-je-hermes.html', 'en', 'What is Hermes Agent?',
     'Open-source autonomous AI agent by Nous Research. 60+ tools, 20+ platforms, MIT license.',
     'https://hermes-ai.cz/en/co-je-hermes/', 'co-je-hermes/', 'https://hermes-ai.cz/en/co-je-hermes/', 'en_US',
     NAV_EN, CO_JE_CZ.replace('cs_CZ','').replace('{nav}', NAV_EN).replace('Česk','English').replace(' češtině',' in English').replace('všechny klíče, menu, nastavení','all keys, menu, settings').replace('předplatné reálného','').replace('překlady oficiální dokumentace, tutoriály a návody pro začátečníky v češtině.','Official docs, tutorials, and beginner guides.')),
    ('en/funkce.html', 'en', 'Hermes Agent Features',
     'Complete feature list: 60+ tools, memory layers, auto-skills, MCP, planning, 20+ platforms.',
     'https://hermes-ai.cz/en/funkce/', 'funkce/', 'https://hermes-ai.cz/en/funkce/', 'en_US',
     NAV_EN, FUNCKCE_CZ.replace('{nav}', NAV_EN)),
    ('en/komunita.html', 'en', 'Community — Hermes Agent',
     'Support, localization, and community for English-speaking Hermes Agent users.',
     'https://hermes-ai.cz/en/komunita/', 'komunita/', 'https://hermes-ai.cz/en/komunita/', 'en_US',
     NAV_EN, KOMUNITA_CZ.replace('{nav}', NAV_EN).replace('Česká komunita','Community').replace('české a slovenské','English-speaking').replace('češtině','in English').replace('Českou','English').replace('překlady oficiální dokumentace','Documentation and tutorials').replace('překlady oficiální dokumentace, tutoriály a návody pro začátečníky v češtině.','Official documentation, tutorials, and beginner guides.')),
]

if __name__ == '__main__':
    for p in PAGES:
        build_page(*p)
