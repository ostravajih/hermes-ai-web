# Hermes AI — Česká komunita 🇨🇿

Web české komunity kolem [Hermes Agent](https://github.com/NousResearch/hermes-agent) — open-source
autonomního AI agenta od [Nous Research](https://nousresearch.com/).
**Ověřeno 17. 10. 2026:** agent má 254 417 hvězd, WebUI 18 974 hvězd (GitHub API).

> **Kontrola dokumentace:** poslední srovnání dokumentace s kódem a živým webem proběhlo
> **17. 10. 2026** (audit dokumentace + spuštěné testy `test-web.py`). Když se web změní, aktualizujte prosím tuhle
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
├── en/
│   ├── index.html               # EN landing page
│   ├── installation/ hosting/ skills/ faq/ what-is-hermes/ features/ community/
│   ├── blog/index.html + page/2/ page/3/ + clanek/<slug>/index.html   # 27 článků (EN)
├── assets/
│   ├── redesign/style.css       # vizuální systém (jen tmavý, self-hosted písmo)
│   ├── redesign/fonts/Inter-web.woff2   # jediné písmo — variabilní Inter 100–900, ~50 KB
│   ├── redesign/images/         # hero, sekční a článkové obrázky (WebP)
│   ├── zive.js                  # živé efekty webu (síť bodů, počítadla, světlo karet, terminál)
│   ├── matomo.js                # měření (Matomo + hloubka čtení + kliky na CTA)
│   └── script.js                # přepínač jazyka, WebMCP
├── robots.txt · sitemap.xml · llms.txt     # SEO (158 adres v sitemapě)
├── submit-sitemap.sh            # odeslání sitemapy do IndexNow
├── test-web.py                  # testy webu (značky, odkazy, hreflang, sitemapa, živý web)
├── <klíč>.txt                   # IndexNow klíče (hermes2026-1gtn3el9l463ok9n, 84907d05…)
├── redesing/                    # interní plány a audity (nginx blokuje, 404)
├── audit.md                     # SEO audit z 9. 7. 2026 — historie, ne aktuální stav
└── README.md
```

**Počty (17. 10. 2026):** **160 HTML souborů = 160 živých stránek** (158 v sitemapě + `404.html` a `500.html`); wiki **39 stránek CZ + 39 EN**. (Na disku je o jeden HTML soubor víc — `redesing/index.html` z designového balíčku; nginx ho vrací 404, takže živá stránka není.)
Staré adresy jsou řešené **skutečnými 301 v nginx** — na disku po nich nezůstal žádný soubor
(`grep -rl 'http-equiv="refresh"' --include='*.html' .` vrací 0). Článků je 27 (CZ) a 27 (EN),
stránek wiki 39 (CZ i EN) — celé fáze 1, 2 i 3 hotové. Počty se dají ověřit příkazem — viz sekce **Testy** níže.

## 📈 Měření návštěvnosti

Web měří **dvěma systémy** — Matomo je hlavní, GA4 zůstává na úvodních stránkách.

### Matomo (web č. 2 na `matomo.sipkyliga.cz`)

- V každé stránce je před `</head>` `<script defer src="/assets/matomo.js?v=…"></script>` a měří se
  **vždy a bez cookies** (`paq(["disableCookies"])` v `assets/matomo.js`) — data tedy nezkresluje to,
  kdo souhlas dal a kdo ne, a cookie lišta není potřeba (16. 10. 2026 vznikla a ještě týž den byla
  na přání vlastníka zrušena). Návštěvu drží pohromadě jen denní otisk `config_id`.
  Ověřeno v prohlížeči: `document.cookie` je po načtení **prázdný**, přitom `matomo.php` odchází.
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
- **Nová stránka musí dostat měření** — zkopírujte
  `<script defer src="/assets/matomo.js?v=…"></script>` z jakékoli existující stránky.
  `noscript` obrázek se nevkládá (měří se bez cookies, JavaScript stačí).

### Google Analytics 4

- `G-F3JXCFBDNF` — **jen na 5 úvodních stránkách** (`index.html`, `co-je-hermes/`, `funkce/`,
  `komunita/`, `en/index.html`) a je **taky bez cookies**: `gtag("consent","default",{analytics_storage:"denied"})`
  + `client_storage:"none"` (jinak si GA4 zapíše `_ga` a `_ga_…`). Data o vracejících se
  uživatelích proto GA4 neuvidí — plná čísla o návštěvách má Matomo. Články a podstránky
  GA4 neměří; ty pokrývá Matomo.

## 📝 Blog — 27 článků (× 2 jazyky)

**Jazyková parita je hlídána.** Anglické články vznikly jako torza (6 z 27 mělo plný
překlad); 16. 10. 2026 byly dopřeloženy všechny. Nástroj `blog-zdroj/oprav-en-clanky.py`
vezme českou předlohu a nahradí tělo anglického článku překladem — nadpisy, seznamy,
tabulky i bloky s kódem, včetně data a doby čtení. Po úpravě českého článku ho spusťte
znovu (`python3 blog-zdroj/oprav-en-clanky.py`) a obě verze se srovnají.
Kontrola struktury: `h2`, `h3`, tabulky, řádky, odrážky, kód a boxy musí být v CZ i EN
ve stejném počtu — stav 27/27.

**Stejný hero obrázek na všech stránkách blogu:** rozcestník i stránky 2 a 3 (CZ i EN) používají
plakátovou horní sekci s `blog-hero.webp` a mobilní `blog-hero_mobile_768x960.webp`. Stránky 2 a 3
měly do 16. 10. 2026 starší tvar hero s obrázkem `blog-documentation.webp` (a bez mobilní verze) —
vlastník si toho všiml („na titulní straně je obrázek správný, na dalších ne“). Nová stránka blogu
tedy musí převzít i horní sekci, ne jen seznam karet.

Široké tabulky v článcích (4 a více sloupců) jsou v posuvném rámečku
(`<div class="table-wrapper">`), úzké se vejdou na displej samy; na mobilu se tak
nic neuřezává.

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
- SEO: `hreflang` alternates (`cs`, `en`, `x-default`) na **každé** stránce, oddělené `canonical`.
  **Přepínač jazyka v hlavičce bere adresu protějšku z `hreflang`** — ne odhadem (`/en` + cesta),
  protože blog má stránkování v každém jazyce jinak (`/blog/stranka/2/` ⇄ `/en/blog/page/2/`) a články,
  hosting i wiki mají přeložené názvy adres. Odhad vedl na 404 (nález vlastníka 16. 10. 2026: „přepnu na EN
  a je chyba 404, a to je u každých stránek“). Kontrola: 160 stránek, oba směry, 0 chyb (17. 10. 2026 znovu ověřeno).
  Nová stránka tedy musí mít správnou dvojici `hreflang` — přepínač, vyhledávače i AI agenti ji používají.

## 🔍 SEO

- **158 adres** v `sitemap.xml` (jedna adresa na řádek). Všechny vrací 200.
- **Skutečné 301** (ověřeno 15. 10. 2026): `/skills`, `/komunita`, `/funkce`, `/co-je-hermes`,
  `/en/community`, `/en/features`, `/en/what-is-hermes`, `/blog`, `/en/blog` a **7 cest bez lomítka**
  (`/instalace`, `/hosting`, `/faq`, `/en/skills`, `/en/installation`, `/en/hosting`, `/en/faq` —
  výslovná pravidla v nginx, zachovávají i parametry v adrese).
- **66 starých adres → všechny skutečné 301** (od 15. 10. 2026). Dřív 58 z nich vracelo **404**
  (staré adresy článků `/blog/<nazev>/` a staré stránkování `/blog/stranka-2/`) a zbytek se
  přesměrovával uvnitř stránky (meta refresh). Nyní to řeší **vzorová pravidla v nginx**
  (`/etc/nginx/sites-available/hermes-ai`): `/blog/<nazev>/`, `/blog/<nazev>.html` →
  `/blog/clanek/<nazev>/` (totéž pro `/en/`), `/blog/stranka-2/` → `/blog/stranka/2/`,
  `/dovednosti(.html)` → `/skills/`, `*.html` u stránek → verze s lomítkem.
  Pomocné soubory s přesměrováním jsou smazané. Ověřeno: všech 66 vrací 301 → cíl 200.
- **Schema.org**: SoftwareApplication, Product, Blog, FAQPage, Article
- **IndexNow** — běží **denně ve 04:00** (cron `0 4 * * * /var/www/hermesagent/submit-sitemap.sh`).
  Skript nejdřív aktualizuje `lastmod` v sitemapě podle skutečného data změny souborů
  (`update-sitemap.py`), ověří, že je sitemapa platné XML a že je klíč dostupný, a teprve pak odešle
  **všech 158 adres**. Výsledek píše do `/var/log/hermes-sitemap.log`, problémy zvlášť do
  `/var/log/hermes-sitemap-problem.log` (a skončí chybou). Ověřovací klíče v kořeni:
  `hermes2026-1gtn3el9l463ok9n.txt` a `84907d0597ff4a0f8af10a55fe6a3361.txt`.
  Neplatný `a1b2c3d4e5f6g7h8i9j0.txt` (obsahoval cizí klíč) byl smazán 15. 10. 2026.
  Google „ping sitemapy“ už nepodporuje — sitemapu si bere z `robots.txt`.
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
- **Přidání na plochu telefonu (aplikace)**: `assets/redesign/logos/manifest.json` — název na ploše
  „Hermes AI“, start `/?zdroj=app`, `display: standalone`, tmavý úvodní displej (`#061020`).
  Ikony: `app-icon-192.png`, `app-icon-512.png`, `app-icon-maskable-512.png` (pro masky Androidu)
  a `apple-touch-icon-180.png` (iOS) — tmavá dlaždice s písmenem **H** v gradientu webu.
  V hlavičkách všech 160 stránek je `rel="manifest"`, `apple-touch-icon` a `apple-mobile-web-app-*`
  + `mobile-web-app-capable`. Aplikace otevírá web bez adresního řádku; `?zdroj=app` v Matomu
  ukáže, kolik lidí ji tak používá.
- **České a anglické UI** — tlačítka, navigace, patička.
- **Patička** (15. 10. 2026): sloupec „Naše Projekty“ se zpětnými odkazy na naše weby
  (Šipky Liga, MultiBrains, SEO Test, Minecraft List CZ/SK i EN/DE; bez `nofollow`) a **ikony
  komunity** (Discord, Facebook, Instagram, e-mail) pod textem vlevo; odkaz na jazykovou verzi
  je ve spodní liště.
- **Hlavička**: přepínač jazyka je **před** tlačítkem „Připojit se ke komunitě“ a zůstává viditelný
  i na telefonu (dřív se na malých šířkách skrýval úplně).
- **Nadpisy článků**: o něco menší než ostatní nadpisy (68 px na počítači) a **vycentrované**;
  datum a perex zůstávají vlevo. Stejná velikost i na chybových stránkách 404/500.

## 💬 Discord komunita

- **[discord.gg/ysx9dbXpdD](https://discord.gg/ysx9dbXpdD)** (neomezená pozvánka; nahradila
  starou `discord.gg/VZpfgrCre` 15. 10. 2026)
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

## 📊 Statistiky webu (17. 10. 2026)

| Metrika | Hodnota |
|---------|---------|
| Adres v sitemapě | 158 |
| Živých stránek | 160 (158 v sitemapě + `404.html` a `500.html`) |
| HTML souborů celkem | 160 |
| Blog článků | 27 (CZ) + 27 (EN) |
| Jazykové verze | 2 (CS, EN) |
| Měření | Matomo (celý web) + GA4 (5 stránek) — obojí **bez cookies**, bez lišty |
| GitHub stars | 254 477 (agent) · 18 979 (WebUI) |
| Licence | MIT |

## ✅ Testy (`test-web.py`)

Testy se spouští jedním příkazem — hlídají to, co se u statického webu dá snadno rozbít
a čeho si v prohlížeči nevšimnete:

```bash
python3 test-web.py            # vše (disk + dotazy na živý web)
python3 test-web.py --jen-disk # bez sítě (rychlé)
```

| # | Co se kontroluje | Jak se to pozná |
|---|---|---|
| 1 | **Nevyvážené značky** | přebývající `</div>` rozbije vzhled (obsah uteče ze sloupce) — hlídá i `wiki-zdroj/aktualizuj.py` |
| 2 | **Odkazy do prázdna** | každý interní odkaz, obrázek, skript a styl musí na disku existovat |
| 3 | **hreflang** | každá stránka má `cs` + `en` + `x-default`, míří na existující stránky a **dvojice je obousměrná** |
| 4 | **Sitemapa** | každá živá stránka je v sitemapě a každá adresa v ní existuje |
| 5 | **Wiki a dlaždice** | počet dlaždic na rozcestníku odpovídá hotovým stránkám; dlaždice **nenesou odznak „✅ hotová / DONE“** (rozhodnutí vlastníka 17. 10. 2026) |
| 6 | **Verze vzhledu** | `style.css`, `wiki.css`, `script.js`, `zive.js`, `matomo.js` musí mít v adrese `?v=` (jinak je prohlížeč drží v keši) |
| 7 | **Soubory pro roboty** | `robots.txt`, `sitemap.xml`, `llms.txt` existují, `ai.txt` má značku UTF-8 (BOM) |
| 8 | **Živý web** | všech 158 adres ze sitemapy vrací 200; interní soubory (`/audit.md`, `/redesing/…`, `wiki-zdroj/…`) vrací 404; `sitemap.xml` má `charset=utf-8` |

Návratový kód **1** při jakékoli chybě, takže se dá pustit i z cronu. Testy samy nic nemění.

**Doplňkové kontroly, které se dělají v prohlížeči** (kvůli posouzení vzhledu — `test-web.py` je nedělá):
přepínač jazyka na všech stránkách oběma směry (`window.__hermesCilovaAdresa('cs'|'en')` musí odpovídat
hreflangu) a telefon v režimu aplikace na 390 i 360 px (měřit `getBoundingClientRect().right > innerWidth`
a rozlišit „posuvné“ předkem s `overflow-x: auto` od „uříznutého“ s `hidden`).

## 📄 Dokumentace

| Dokument | Co vlastní (je zdrojem pravdy) |
|---|---|
| `README.md` | **aktuální stav webu** — struktura, měření, SEO, design, nasazení, statistiky |
| `redesing/PLAN-SEO-2026-10-16.md` | stav oprav podle SEO auditu z 16. 10. + záznamy do DNS |
| `redesing/OZIVENI-WEBU-2026-10-15.md` | živé efekty — co je nasazené, jak je vypnout |
| `redesing/EMAILY-SPF-DKIM-DMARC.md` | nastavení e-mailových záznamů pro `@hermes-ai.cz` |
| `redesing/OPRAVY-CELEHO-WEBU-2026-10-15.md` | průběh oprav 15. 10. 2026 + **seznam otevřených chyb** |
| `redesing/PLAN.md` | původní plán redesignu (historie + co z něj platí) |
| `redesing/PLAN-*.md` | jednotlivé dílčí plány (u každého je v hlavičce stav) |
| `redesing/AUDIT-A-PLAN-OPRAV-2026-10-14.md` | audit z 14. 10. 2026 (historie) |
| `audit.md` | SEO audit z 9. 7. 2026 — **zastaralý, historie** |

## Wiki (česky a anglicky)

Kurátorovaná wiki podle oficiální dokumentace — méně stránek, ale s českým kontextem
(ceny v korunách, čeští poskytovatelé, platby z ČR, naše zkušenosti z provozu).

| Co | Kde |
|---|---|
| Adresy | `/wiki/` + `/wiki/<sekce>/<stranka>/`, anglicky `/en/wiki/…` |
| **Hotové stránky (39 — fáze 1, 2 i 3 dokončeny)** | **Fáze 1 „Začínáme“:** `/wiki/zaciname/instalace/` · `vyber-modelu/` · `prvni-chat/` · `telegram-a-discord/` · `skilly/` · `pamet/` · `pravidelne-ulohy/` · `mcp-nastroje/` · `bezpecnost/` · `kdyz-se-neco-pokazi/` · `caste-dotazy/` · `slovnicek/` — **Fáze 2 „Funkce do hloubky“:** `/wiki/funkce/nastroje/` · `profily/` · `desktop/` · `tui/` · `sezeni/` · `podagenti/` · **`hlas/`** · **`email-kalendar/`** · **`lokalni-modely/`** · **`kontrolni-body/`** · **`spousteni-prikazu/`** · **`kontextove-soubory/`** · **`zalohy-a-obnova/`** · **`pluginy/`** · **`kurator-skills/`** · **`import-z-jinych-agentu/`** · **`webhooky/`** · **`monitoring/`** — **Fáze 3 „Integrace a návody“:** **`/wiki/integrace/telegram/`** · **`discord/`** · **`whatsapp/`** · **`sms/`** · **`google-workspace/`** · **`github/`** · **`spravci-hesel/`** · **`hosting-a-domeny/`** · **`vlastni-aplikace-mcp/`** (+ anglické protějšky `/en/wiki/getting-started/…`, `/en/wiki/features/…` a `/en/wiki/integrations/…`) |
| Styly a skript | `assets/redesign/wiki.css` (+ `wiki.js` — tlačítko „Kopírovat" u příkazů) |
| Obrázky do hero sekcí | Fáze 1: `wiki-hero.webp`, `wiki-instalace-hero.webp`, `wiki-model-hero.webp`, `wiki-chat-hero.webp`, `wiki-telegram-hero.webp`, `wiki-skilly-hero.webp`, `wiki-pamet-hero.webp`, `wiki-cron-hero.webp`, `wiki-mcp-hero.webp`, `wiki-bezpecnost-hero.webp`, `wiki-oprava-hero.webp`, `wiki-dotazy-hero.webp`, `wiki-slovnicek-hero.webp`. Fáze 2: `wiki-nastroje-hero.webp`, `wiki-profily-hero.webp`, `wiki-desktop-hero.webp`, `wiki-tui-hero.webp`, `wiki-sezeni-hero.webp`, `wiki-podagenti-hero.webp`, `wiki-hlas-hero.webp`, `wiki-email-kalendar-hero.webp`, `wiki-lokalni-modely-hero.webp`, `wiki-kontrolni-body-hero.webp`, `wiki-spousteni-hero.webp`, `wiki-kontext-hero.webp`. Fáze 3: `wiki-telegram-hero.webp`, `wiki-discord-hero.webp`, `wiki-whatsapp-hero.webp`, `wiki-sms-hero.webp`, `wiki-google-workspace-hero.webp`, `wiki-github-hero.webp`, `wiki-spravci-hesel-hero.webp`, `wiki-hosting-hero.webp`, `wiki-vlastni-aplikace-hero.webp` (každý i mobilní 768×960) |
| Verze pro AI | `…/ai.txt` u každé stránky (`.md` na webu blokuje nginx, proto `.txt`) |
| Kódování | nginx posílá `charset=utf-8` pro HTML, text, CSS, JS i JSON (bez toho se `ai.txt` a `llms.txt` zobrazí s rozsypanou diakritikou) |
| Podklady (mimo web) | `wiki-zdroj/` — stahovač `nacist-dokumentaci.py`, `prehled.json`, `stranky/*.md`, mapa zdrojů `zdroje.json`, fronta změn `fronta-zmen.py` + `zmeny/<datum>/`, loga poskytovatelů `loga/*.svg` |

**Rozcestník wiki nemá na dlaždicích odznak „hotová“.** Dlaždice sama znamená hotovou stránku;
odznak „⏳ připravujeme“ zůstává jen u stránek, které ještě nejsou napsané (vlastník 17. 10. 2026:
„odeber z dlaždic to, že je HOTOVÁ, DONE, teď to tam nemusí být, když už to je“). Nadpis a úvod
nad dlaždicemi se počítá ze `stranky.json` (`sablona.uvod_rozcestniku`) — ručně psaný text zestaral.

**Generátor stránek:** seznam stránek je v `wiki-zdroj/stranky.json` (jediné místo pravdy),
společné části staví `wiki-zdroj/sablona.py` (hlavička, horní sekce, postranní nabídka, meta,
`ai.txt`) a `wiki-zdroj/aktualizuj.py` po každé nové stránce srovná **postranní nabídku, karty
rozcestníku, dvojice adres pro přepínač jazyka, sitemapu, verzi vzhledu `?v=` i obrázky horních
sekcí**. Obsahové skripty jednotlivých stránek: `postav-vyber-modelu.py`, `postav-prvni-chat.py`, `postav-telegram-discord.py`, `postav-skilly.py`, `postav-pamet.py`, `postav-pravidelne-ulohy.py`, `postav-mcp.py`, `postav-bezpecnost.py`, `postav-kdyz-se-pokazi.py`, `postav-caste-dotazy.py`, `postav-slovnicek.py`, `postav-nastroje.py`, `postav-profily.py`, `postav-desktop.py`, `postav-tui.py`, `postav-sezeni.py`, `postav-podagenti.py`, `postav-hlas.py`, `postav-email-kalendar.py`, `postav-lokalni-modely.py`, `postav-kontrolni-body.py`, `postav-spousteni-prikazu.py`, `postav-kontextove-soubory.py`, `postav-zalohy-a-obnova.py`, `postav-pluginy.py`, `postav-kurator-skills.py`, `postav-import-z-jinych-agentu.py`, `postav-webhooky.py`, `postav-monitoring.py`, `postav-telegram.py`, `postav-discord.py`, `postav-whatsapp.py`, `postav-sms.py`, `postav-google-workspace.py`, `postav-github.py`, `postav-spravci-hesel.py`, `postav-hosting.py`, `postav-vlastni-aplikace.py`.

**Když stavíte víc stránek v jedné dávce, spusťte obsahové skripty nakonec ještě jednou.**
Odkaz na stránku, která v okamžiku stavby ještě neexistovala, se totiž vypíše jako dlaždice
„⏳ připravujeme“ — a to je zapečené v hotovém HTML. Po dodělání celé dávky se druhým spuštěním
z dlaždic stanou skutečné odkazy (`aktualizuj.py` tuto vrstvu neřeší). Pozná se to tak, že stránka
má `document.querySelectorAll('.wiki-dalsi__ceka').length > 0`, přitom cíl na disku existuje.

**`aktualizuj.py` přepisuje i `assets/script.js`** (doplňuje dvojice adres pro přepínač jazyka).
Když se tím soubor změní, **zvyšte `?v=`** u `script.js` ve všech stránkách **i v `wiki-zdroj/sablona.py`**
(`grep -rl 'script.js?v=redesign-9'` musí sedět; aktuálně `redesign-9`, zvednuto 17. 10. 2026 po fázi 3) — jinak si prohlížeč
drží starou tabulku a stránky bez hreflangu posílá špatně.

**Fáze 4 — wiki v souladu s dokumentací (`wiki-zdroj/fronta-zmen.py`).** Nic na webu nemění,
jen říká, co je potřeba přečíst a doplnit:

```bash
python3 wiki-zdroj/fronta-zmen.py                  # stáhne dokumentaci, porovná, zapíše frontu
python3 wiki-zdroj/fronta-zmen.py --bez-site       # jen vypíše poslední frontu
python3 wiki-zdroj/fronta-zmen.py --z-diffu 2026-10-17   # obnoví frontu z uložených rozdílů
```

- Stáhne `llms-full.txt`, porovná **otisky** stránek (`prehled.json`), rozdíly uloží do
  `wiki-zdroj/zmeny/<datum>/<slug>.diff` a přepíše `wiki-zdroj/fronta-zmen.md` (+ `.json`).
- Mapování „která stránka dokumentace → která naše stránka“ je ve `wiki-zdroj/zdroje.json` (39 stránek).
  Bez něj by fronta jen vypsala 40 cizích názvů a nikdo by nevěděl, kam sáhnout.
- **Když se nic nezměnilo, fronta se nepřepisuje** — jen se poznamená datum kontroly, aby otevřené
  položky nezmizely.
- Každá stránka wiki má v hlavičce „✅ Ověřeno <datum>“ a odkaz na zdroj, takže je vidět, co zestaralo.
- Běží samo: `/etc/cron.d/hermes-wiki`, pondělí 5:20, log `/var/log/hermes-wiki.log`.

**Postup přidání stránky:** nastavit `hotovo` v `stranky.json` → napsat text česky a anglicky
(obsahový skript) → vyrobit obrázek do hero sekce (1920×700 + mobilní 768×960, název
`<stranka>-hero.webp` a `<stranka>-hero_mobile_768x960.webp`) → spustit `aktualizuj.py` →
ověřit HTTP (všechny obrázky 200, žádný odkaz do prázdna) a v prohlížeči na počítači i telefonu.

Odkaz na stránku, která ještě není hotová, zobrazí `sablona.py` sám jako dlaždici „připravujeme"
(nemůže tak vzniknout odkaz do prázdna) a po postavení stránky se z něj stane odkaz.

**Loga poskytovatelů modelů** (stránka o výběru modelu) jsou jednobarevné značky ze sady
simple-icons (`wiki-zdroj/loga/`) vložené přímo do stránky — nikdy se nevypalují do generovaného
obrázku (generátor je zkomolí a vznikne nepravé logo).

Každá stránka nese datum „Ověřeno", odkaz na oficiální předlohu a je propojená s blogem
a Discordem. Wiki je i v hlavním menu (položka „Wiki").

