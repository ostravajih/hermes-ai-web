# Hermes AI — Česká komunita 🇨🇿

Web české komunity kolem [Hermes Agent](https://github.com/NousResearch/hermes-agent) — open-source autonomního AI agenta od [Nous Research](https://nousresearch.com/) s 210 000+ hvězdami na GitHubu.

## 🌐 Web

- **[hermes-ai.cz](https://hermes-ai.cz)** — hlavní stránka (CZ)
- **[hermes-ai.cz/en/](https://hermes-ai.cz/en/)** — English version
- **[hermes-ai.cz/instalace](https://hermes-ai.cz/instalace)** — kompletní návod k instalaci
- **[hermes-ai.cz/hosting](https://hermes-ai.cz/hosting)** — VPS hosting (Contabo affiliate)
- **[hermes-ai.cz/dovednosti](https://hermes-ai.cz/dovednosti)** — přehled dovedností (skills)
- **[hermes-ai.cz/faq](https://hermes-ai.cz/faq)** — časté dotazy
- **[hermes-ai.cz/blog/](https://hermes-ai.cz/blog/)** — blog (27 článků, 3 strany)

## 📁 Struktura

```
/var/www/hermesagent/
├── index.html              # Hlavní stránka (CZ)
├── instalace.html          # Instalační příručka (CZ)
├── hosting.html            # VPS hosting (CZ)
├── dovednosti.html         # Přehled dovedností (CZ)
├── faq.html                # Časté dotazy (CZ)
├── 404.html / 500.html     # Vlastní chybové stránky
├── blog/                   # 27 CZ blog článků + stránkování (3 strany)
├── en/
│   ├── index.html          # EN landing page
│   ├── installation.html   # EN install guide
│   ├── hosting.html        # EN VPS hosting
│   ├── skills.html         # EN skills overview
│   ├── faq.html            # EN FAQ
│   └── blog/               # 27 EN blog articles + pagination (3 pages)
├── assets/
│   ├── style.css           # Styly (light/dark režim, responzivní)
│   ├── script.js           # Skripty (theme toggle, jazyková detekce, přepínač)
│   └── ...                 # Favicony, ikony, obrázky
├── robots.txt
├── sitemap.xml             # 70 URL
└── README.md
```

## 📝 Blog — 27 článků

### Instalace & Provoz
- 🚀 Jak nainstalovat Hermes Agent na Ubuntu
- 🪟 Hermes Agent na Windows a WSL2
- 🍎 Hermes Agent na macOS (Apple Silicon i Intel)
- 🐳 Hermes Agent v Dockeru
- 🥧 Hermes Agent na Raspberry Pi

### LLM a API
- 🦙 Hermes Agent s Ollama a lokálním LLM
- 🔀 Hermes Agent s OpenRouter (300+ modelů)
- 🌟 Hermes Agent s Nous Portal
- 🔷 Hermes Agent s Google Gemini (1 500 req/den zdarma)

### Platformy a Integrace
- 🤖 Telegram bot s Hermes Agent
- 🌐 Hermes na všech platformách (20+)
- 🔑 Hermes Agent přes SSH (vzdálená správa)
- 🔌 MCP integrace (Model Context Protocol)
- 🖥️ Hermes WebUI — kompletní průvodce

### Automatizace & Konfigurace
- ⏰ Cron plánovač 24/7 (briefingy, PR review, monitoring)
- 🎭 Nastavení SOUL.md (osobnost agenta)
- 👥 Profily — více agentů na jednom serveru
- 🎤 Hlasový režim (STT/TTS)
- 🛡️ Bezpečnost Hermes Agent
- 🖧 Hermes pro systémové administrátory

### Srovnání & Komunita
- ⚔️ Hermes Agent vs Claude Code 2026
- ⚡ Hermes Agent vs OpenClaw
- 💻 Hermes Agent vs Codex (OpenAI)
- 💰 AI Agent na VPS: Kolik to stojí?
- 📚 Jak používat dovednosti (Skills)
- 🐙 Jak přispět do Hermes Agent (open-source)
- 📅 Hermes Agent 2026 — novinky a roadmap

## 🌍 Jazykové verze

- **CS**: výchozí pro česky/slovensky mluvící návštěvníky
- **EN**: automaticky pro ostatní (podle `navigator.language`)
- Přepínač `🇨🇿 CZ` / `🇬🇧 EN` v navigační liště
- Volba se ukládá do `localStorage`, přežije reload
- SEO: `hreflang` tagy, oddělené `canonical` URL

## 🔍 SEO

- **70 URL** v sitemap.xml
- **hreflang** alternates pro všechny stránky
- **Schema.org**: SoftwareApplication, Product, Blog, FAQPage, Article
- **IndexNow** — automatické odesílání do vyhledávačů
- **Meta tags**: Open Graph, Twitter Card, description, keywords
- **Cache headers**: 7denní cache pro statické assety
- **GZIP** komprese zapnutá
- Vlastní **404** a **500** chybové stránky
- Google Analytics (G-F3JXCFBDNF)
- Seznam.cz ověření (uQSQdFRdQoVYGXVnuxQVlUk1CwxslRXE)
- **Discord** invite v navigaci i patičce

## 🎨 Design

- **Light + Dark režim** — CSS proměnné, plynulé přepínání
- **Responzivní** — mobil, tablet, desktop
- **3-sloupcový blog grid** — 3×3 karty na stránku
- **Stránkování** — 27 článků na 3 stránkách
- **České a anglické UI** — tlačítka, navigace, patička

## 💬 Discord komunita

- **[discord.gg/VZpfgrCre](https://discord.gg/VZpfgrCre)**
- Hermes bot napojený přes gateway
- Automatické novinky v `#oznámení` (GitHub releases)
- Reaction role (📢 Novinky, 💬 Komunita)
- Zabezpečené kanály (pravidla, admin-log)

## 🚀 Nasazení

- **Nginx** na VPS (Contabo)
- **SSL** přes Let's Encrypt
- **Domény**: `hermes-ai.cz` + `hermes-ai.fun` (přesměrování)
- **Cache**: 7 dní pro statické soubory
- **GZIP** komprese
- Automatický **deploy** přes Git push

## 🇨🇿 Česká lokalizace

- ✅ Hermes Web UI — [čeština přidána ve v0.51.910](https://github.com/nesquena/hermes-webui/pull/5546)
- ⏳ Hermes Agent — [čeština čeká na review](https://github.com/NousResearch/hermes-agent/pull/56521)

---

Spravuje [@ostravajih](https://github.com/ostravajih) · [multibrains.eu](https://www.multibrains.eu/)

## 📊 Statistiky webu

| Metrika | Hodnota |
|---------|---------|
| Celkem stránek | 70 |
| Blog článků | 27 (CZ) + 27 (EN) |
| Jazykové verze | 2 (CS, EN) |
| Velikost sitemap | 70 URL |
