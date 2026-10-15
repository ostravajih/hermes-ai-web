# Hermes AI — Česká komunita 🇨🇿

Web české komunity kolem [Hermes Agent](https://github.com/NousResearch/hermes-agent) — open-source
autonomního AI agenta od [Nous Research](https://nousresearch.com/).
**Ověřeno 15. 10. 2026:** agent má 253 821 hvězd, WebUI 18 930 hvězd (GitHub API).

> **Kontrola dokumentace:** poslední srovnání dokumentace s kódem a živým webem proběhlo
> **15. 10. 2026** (při ukládání redesignu do gitu). Když se web změní, aktualizujte prosím tuhle
> tabulku a příslušný dokument — seznam je na konci v části **📄 Dokumentace**.

## 🌐 Web

| Adresa | Co to je |
|---|---|
| [hermes-ai.cz](https://hermes-ai.cz) | hlavní stránka (CZ) |
| [hermes-ai.cz/en/](https://hermes-ai.cz/en/) | English version |
| [hermes-ai.cz/instalace/](https://hermes-ai.cz/instalace/) | kompletní návod k instalaci |
| [hermes-ai.cz/hosting/](https://hermes-ai.cz/hosting/) | VPS hosting (Contabo affiliate) |
| [hermes-ai.cz/skills/](https://hermes-ai.cz/skills/) | přehled dovedností (skills) |
| [hermes-ai.cz/faq/](https://hermes-ai.cz/faq/) | časté dotazy |
| [hermes-ai.cz/co-je-hermes/](https://hermes-ai.cz/co-je-hermes/) | co je agent a jak pracuje |
| [hermes-ai.cz/funkce/](https://hermes-ai.cz/funkce/) | nástroje, paměť a automatizace |
| [hermes-ai.cz/komunita/](https://hermes-ai.cz/komunita/) | Discord a komunitní zdroje |
| [hermes-ai.cz/blog/](https://hermes-ai.cz/blog/) | blog (27 článků, 3 strany) |
| [hermes-ai.cz/ukazka/](https://hermes-ai.cz/ukazka/) | **dočasná** živá ukázka animací — `noindex` + `Disallow: /ukazka/`, není součástí webu |

## 📁 Struktura

```
/var/www/hermesagent/            # nginx servíruje přímo tuhle složku, žádný build
├── index.html                   # hlavní stránka (CZ)
├── instalace/ hosting/ skills/ faq/ co-je-hermes/ funkce/ komunita/   # stránky s čistou URL
├── 404.html / 500.html          # chybové stránky
├── blog/
│   ├── index.html               # seznam článků (CZ)
│   ├── stranka/2/ stranka/3/    # stránkování (CZ)
│   ├── clanek/<slug>/index.html # 27 článků (CZ)
│   └── <stary-nazev>.html       # 29 starých adres — přesměrování (viz SEO)
├── en/
│   ├── index.html               # EN landing page
│   ├── installation/ hosting/ skills/ faq/ what-is-hermes/ features/ community/
│   ├── blog/index.html + page/2/ page/3/ + clanek/<slug>/index.html   # 27 článků (EN)
│   └── <old-name>.html, faq.html, hosting.html, installation.html, skills.html  # 8 starých adres
├── assets/
│   ├── redesign/style.css       # vizuální systém (jen tmavý, self-hosted písmo)
│   ├── redesign/fonts/Inter-web.woff2   # jediné písmo — variabilní Inter 100–900, ~50 KB
│   ├── redesign/images/         # hero, sekční a článkové obrázky (WebP)
│   ├── zive.js                  # živé efekty webu (síť bodů, počítadla, světlo karet, terminál)
│   ├── matomo.js                # měření (Matomo + hloubka čtení + kliky na CTA)
│   └── script.js                # přepínač jazyka, WebMCP
├── robots.txt · sitemap.xml · llms.txt     # SEO (76 adres v sitemapě)
├── submit-sitemap.sh            # odeslání sitemapy do IndexNow
├── <klíč>.txt                   # IndexNow klíče (hermes2026-1gtn3el9l463ok9n, 84907d05…)
├── standalone.html              # samostatná bundovaná stránka (nikde neodkazovaná)
├── ukazka/index.html            # dočasná ukázka animací (noindex)
├── redesing/                    # interní plány a audity (nginx blokuje, 404)
├── audit.md                     # SEO audit z 9. 7. 2026 — historie, ne aktuální stav
└── README.md
```

**Počty (15. 10. 2026):** 146 HTML souborů = **78 živých stránek** + 66 starých adres s přesměrováním
+ `standalone.html` + ukázka. Článků je 27 (CZ) a 27 (EN).

## 📈 Měření návštěvnosti

Web měří **dvěma systémy** — Matomo je hlavní, GA4 zůstává na úvodních stránkách.

### Matomo (web č. 2 na `matomo.sipkyliga.cz`)

- V každé stránce je `<script defer src="/assets/matomo.js?v=…"></script>` těsně před `</head>`
  a k tomu `noscript` obrázek pro případ vypnutého JavaScriptu (dohromady **145 z 146 stránek**;
  jediná bez měření je dočasná ukázka `/ukazka/`).
- `assets/matomo.js` nastaví Matomo, načte oficiální tracker a přidává:
  **hloubku přečtení** (25 / 50 / 75 / 100 % — událost `Scroll`), **kliky na hlavní výzvy**
  (Instalace / GitHub / Discord — událost `CTA`), **hledání v adrese** (`?q=`, `?s=`, `?search=`,
  `?hledat=`), sledování chyb JavaScriptu, tep srdce 15 s a automatické sledování odchozích odkazů.
  U odkazů v rámci webu se událost stihne odeslat (zpoždění 150 ms) — u odchozích to řeší Matomo samo.
- **AI chatboti se měří na serveru.** ChatGPT-User, Claude-User, Perplexity-User a další agenti
  JavaScript nespouštět neumí, takže je nevidí žádný skript v prohlížeči. Nginx je proto pozná
  (`/etc/nginx/conf.d/aibot.conf`, mapa `$is_ai_assistant`) a zapíše do `/var/log/nginx/aibot.log`;
  služba **`matomo-bot-collector`** z toho logu posílá záznamy do Matomy přes HTTP Tracking API
  (`recMode=1`, plugin BotTracking). V logu jsou i ostatní AI crawleři (GPTBot, ClaudeBot,
  PerplexityBot…), které Matomo záměrně nezobrazuje — zůstávají tam jako surový důkaz.
- **Nová stránka musí měření dostat taky** — zkopírujte `<script defer src="/assets/matomo.js?v=…">`
  a `noscript` obrázek z jakékoli existující stránky.

### Google Analytics 4

- `G-F3JXCFBDNF` — **jen na 5 úvodních stránkách** (`index.html`, `co-je-hermes/`, `funkce/`,
  `komunita/`, `en/index.html`). Články a podstránky GA4 neměří; ty pokrývá Matomo.

## 📝 Blog — 27 článků (× 2 jazyky)

Stránkování: CZ `/blog/stranka/2|3/`, EN `/en/blog/page/2|3/`.
Každý článek má vlastní náhledový obrázek (`assets/redesign/images/blog/`, 54 souborů) — používá se
v článku i v `og:image`.

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

- Na **první návštěvě vybírá jazyk nginx** — podle hlavičky `Accept-Language` (`map $http_accept_language`).
  JavaScript sám nikam nepřesměrovává (žádné `navigator.language`).
- Ruční přepínač `CZ` / `EN` v navigaci ukládá volbu do cookie `hermes_lang` (pro nginx) a do
  `localStorage` (pro JavaScript) a vede na skutečnou adresu protějšku (tabulka dvojic v `assets/script.js`).
- SEO: `hreflang` alternates (`cs`, `en`, `x-default`), oddělené `canonical` URL.

## 🔍 SEO

- **76 adres** v `sitemap.xml` (73 řádků — na třech řádcích jsou dvě adresy). Všechny vrací 200.
- **Skutečné 301** (ověřeno 15. 10. 2026): `/skills`, `/komunita`, `/funkce`, `/co-je-hermes`,
  `/en/community`, `/en/features`, `/en/what-is-hermes`, `/blog`, `/en/blog` a **7 cest bez lomítka**
  (`/instalace`, `/hosting`, `/faq`, `/en/skills`, `/en/installation`, `/en/hosting`, `/en/faq` —
  výslovná pravidla v nginx, zachovávají i parametry v adrese).
- **58 starých adres se pořád přesměrovává uvnitř stránky** (meta refresh, kód 200): 29 starých adres
  článků (CZ), 29 (EN) + 4 kořenové (`dovednosti.html`, `faq.html`, `hosting.html`, `instalace.html`)
  a 4 v `/en/`. Zbývající otevřený úkol je nahradit i ty skutečným 301.
- **Schema.org**: SoftwareApplication, Product, Blog, FAQPage, Article
- **IndexNow** — `submit-sitemap.sh` + ověřovací klíče v kořeni (`hermes2026-1gtn3el9l463ok9n.txt`,
  `84907d0597ff4a0f8af10a55fe6a3361.txt`). Soubor `a1b2c3d4e5f6g7h8i9j0.txt` **není platný klíč**
  (obsah neodpovídá názvu) — kandidát na smazání.
- **Meta tagy**: Open Graph, Twitter Card, description, keywords
- **Cache**: 7 dní pro `/assets/`, stránky `no-cache`; **GZIP** zapnutý
- **Bezpečnostní hlavičky**: HSTS, `Origin-Agent-Cluster: ?1` (kvůli WebMCP), X-Frame-Options,
  X-Content-Type-Options
- **Interní soubory nejsou veřejné**: nginx vrací 404 na `/redesing/` a na soubory
  `.md/.sh/.py/.csv/.bak/.log/.sql`
- Vlastní **404** a **500** chybové stránky
- Seznam.cz ověření (`uQSQdFRdQoVYGXVnuxQVlUk1CwxslRXE`), Discord invite v navigaci i patičce

### llms.txt

- **`/llms.txt`** — Markdown přehled webu pro AI vyhledávače a agenty (stránky, blog, nástroje, zdroje).
- Odkazuje na SEO platformu na **`seotestzdarma.cz`** (stará `seo.hermes-ai.cz` se přesměrovává 301).

### WebMCP

- **`find_hermes_guide`** — declarative WebMCP tool pro AI agenty; je **na `/` a `/en/`**
  (`toolname`, `tooldescription`, `toolparamdescription` na `<form>` a `<select>`).
- Event listenery `toolactivated` / `toolcancel` jsou v `assets/script.js`.

## 🎨 Design

- **Vždy tmavý režim** — světlý režim zrušen 15. 10. 2026 (blikal při přechodu mezi stránkami,
  na světlém pozadí špatně vynikaly obrázky i kontrast písma). Nikdy nepřidávat světlé varianty.
- **Živé efekty** (`assets/zive.js`, sekce „Oživení webu“ v `style.css`): síť bodů, která se spojuje
  s kurzorem myši; napočítávání čísel; světlo u kurzoru a jemný náklon karet; psací terminál na
  stránce instalace. Vypínají se při systémovém „omezit pohyb“ a respektují pravidla proti blikání
  (jen posuv a průhlednost). Popis a vypínání: `redesing/OZIVENI-WEBU-2026-10-15.md`.
- **Písmo**: jediné variabilní Inter (`assets/redesign/fonts/Inter-web.woff2`, 50 KB, váhy 100–900)
  s přednačtením a `font-display: optional` — dřív bylo pět souborů po 325 KB a způsobovalo blikání.
- **Horní sekce**: 500 px (počítač), 460 px (tablet), 480 px (telefon); obrázek přes celou sekci,
  text jako vrstva nad ním.
- **Responzivní** — mobil, tablet, desktop; 3sloupcový blog grid s přechodem na 2/1 sloupec.
- **České a anglické UI** — tlačítka, navigace, patička.

## 💬 Discord komunita

- **[discord.gg/VZpfgrCre](https://discord.gg/VZpfgrCre)**
- Hermes bot napojený přes gateway
- Automatické novinky v `#oznámení` (GitHub releases)
- Reaction role (📢 Novinky, 💬 Komunita)
- Zabezpečené kanály (pravidla, admin-log)

## 🚀 Nasazení

- **Nginx** na VPS, složka `/var/www/hermesagent` je zároveň zdroj i produkce — **žádný build**,
  změna v souboru je okamžitě živá. `git push` je záloha, ne deploy.
- **Domény**: `hermes-ai.cz` (primární, certifikát platný pro `hermes-ai.cz` **i `www.hermes-ai.cz`**).
  `www.hermes-ai.cz` se přesměrovává 301 na doménu bez www. `hermes-ai.fun` DNS nemá (odkaz je zastaralý).
- **E-maily**: MX `mail.multibrains.eu`; **SPF** `v=spf1 mx a -all` ✅, **DMARC**
  `v=DMARC1; p=none; rua=mailto:postmaster@multibrains.eu; fo=1` ✅ (další krok: `p=quarantine`),
  **DKIM** selektor `dkim` (RSA 2048) ✅ — nastaveno 15. 10. 2026
  (`redesing/EMAILY-SPF-DKIM-DMARC.md`).
- **Větev a záloha**: `feat/redesign` → `git@github.com:ostravajih/hermes-ai-web.git`.
  Redesign je **uložený a odeslaný 15. 10. 2026** (commit `7d79b93`, 424 souborů). Pracovní složka
  je zároveň produkce, takže `git push` je záloha, ne nasazení — změna souboru je živá okamžitě.
- **Cache**: 7 dní pro statické soubory (`/assets/`), HTML `no-cache`; **GZIP** zapnutý.

## 🇨🇿 Česká lokalizace

- ✅ Hermes Web UI — [čeština přidána ve v0.51.910](https://github.com/nesquena/hermes-webui/pull/5546)
- ⏳ Hermes Agent — [čeština čeká na review](https://github.com/NousResearch/hermes-agent/pull/105503)

---

Spravuje [@ostravajih](https://github.com/ostravajih) · [multibrains.eu](https://www.multibrains.eu/)

## 📊 Statistiky webu (15. 10. 2026)

| Metrika | Hodnota |
|---------|---------|
| Adres v sitemapě | 76 |
| Živých stránek | 78 |
| HTML souborů celkem | 146 (78 živých + 66 přesměrování + standalone + ukázka) |
| Blog článků | 27 (CZ) + 27 (EN) |
| Jazykové verze | 2 (CS, EN) |
| Měření | Matomo (145 stránek) + GA4 (5 stránek) |
| GitHub stars | 253 821 (agent) · 18 930 (WebUI) |
| Licence | MIT |

## 📄 Dokumentace

| Dokument | Co vlastní (je zdrojem pravdy) |
|---|---|
| `README.md` | **aktuální stav webu** — struktura, měření, SEO, design, nasazení, statistiky |
| `redesing/OZIVENI-WEBU-2026-10-15.md` | živé efekty — co je nasazené, jak je vypnout |
| `redesing/EMAILY-SPF-DKIM-DMARC.md` | nastavení e-mailových záznamů pro `@hermes-ai.cz` |
| `redesing/OPRAVY-CELEHO-WEBU-2026-10-15.md` | průběh oprav 15. 10. 2026 + **seznam otevřených chyb** |
| `redesing/PLAN.md` | původní plán redesignu (historie + co z něj platí) |
| `redesing/PLAN-*.md` | jednotlivé dílčí plány (u každého je v hlavičce stav) |
| `redesing/AUDIT-A-PLAN-OPRAV-2026-10-14.md` | audit z 14. 10. 2026 (historie) |
| `audit.md` | SEO audit z 9. 7. 2026 — **zastaralý, historie** |
