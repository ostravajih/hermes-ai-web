# Audit redesignu hermes-ai.cz + plán oprav

**Datum:** 14. 10. 2026 · **Větev:** `feat/redesign` (HEAD `9a4b0df` = `origin/main`)
**Metoda:** kontrola souborů na disku, HTML/CSS odkazů, git stavu a reálného vykreslení
(Chromium CDP, 12 stránek × 2 motivy × 2 viewporty = 48 měření), ověření živého webu přes HTTPS.

> **Stav (15. 10. 2026):** 📦 **historie — audit ze 14. 10. 2026.** Nálezy jsou z větší části zapracované
> (hero, přepínač jazyka, anglické mutace, `theme-color`, článkové obrázky, SPF/DKIM/DMARC, verze CSS).
> **Doplněno 17. 10. 2026:** 58 starých adres článků a `rel="manifest"` jsou vyřešené (301 v nginx, PWA
> ve všech 130 stránkách). Otevřený zůstává jen úklid nepoužitých souborů. Redesign je v gitu (15. 10. 2026). (Chybové stránky i cesty bez lomítka jsou opravené
> 15. 10. 2026.) Aktuální stav a otevřené úkoly
> viz `README.md` a `OPRAVY-CELEHO-WEBU-2026-10-15.md`; tenhle soubor needitujte jako aktuální stav.

Skripty auditu: `/root/.hermes/profiles/hermes-web/cache/scratch/audit_redesign.py`,
`audit_redesign2.py`, `audit_langswitch.py`, výstup `audit-out.txt`.

---

## 1. Certifikát a www — ✅ HOTOVO

| Co | Stav |
|---|---|
| Certifikát pro `www.hermes-ai.cz` | ✅ rozšířen — SAN: `hermes-ai.cz`, `www.hermes-ai.cz`, platnost do 12. 1. 2027 |
| HTTPS na www | ✅ `https://www.hermes-ai.cz/` → `301 https://hermes-ai.cz/` (ověřeno i přes IPv6) |
| HSTS na www | ✅ přenáší se z non-www bloku (301 na kanonickou doménu) |
| Obnova certifikátu | ✅ `certbot renew --dry-run` — všech 19 certifikátů simulovaně obnoveno |
| `renewal/hermes-ai.cz.conf` | ✅ obsahuje obě jména + webroot map pro obě |

**Poznámka k zadání:** požadavek zněl „non-www → www“, ale web má **kanonickou verzi
`hermes-ai.cz` (bez www)**: 141 HTML souborů, sitemap i `llms.txt` mají canonical/hreflang
na `https://hermes-ai.cz` (0 výskytů www). Přesměrování tedy běží opačně (www → non-www),
což je v SEO správné a hotové. Přepnutí na www by znamenalo přepsat 141 souborů + sitemap
+ `llms.txt` a znovu indexovat — bez SEO přínosu. → **rozhodnutí viz závěr.**

---

## 2. ✅ Co je hotové (ověřeno)

1. **73 URL v sitemapě = 73 reálných stránek** na disku (27 CZ + 27 EN článků, 8 CZ + 5 EN sekcí, 6 stránek blogu).
2. **0 rozbitých interních odkazů** (`<a href>` na neexistující stránku) na 142 HTML souborech.
3. **0 mrtvých SEO cílů** — všechny `canonical`, `hreflang` (cs/en/x-default), `og:url` míří na existující soubory.
4. **0 chybějících assetů** — 41 unikátních odkazů na `/assets/…` z HTML i CSS má soubor na disku.
5. **Render 48 kombinací:** 0 rozbitých obrázků, 0 horizontálního přetečení, Inter se načetl, hero art na desktopu **823×300 px** shodně na `/instalace/`, `/hosting/`, `/skills/`, `/faq/`, `/blog/`.
6. **12 stránek** s jednotným hero artworkem, **9 stránek** s dark/light párem obrázků — oba soubory existují, v prohlížeči se střídají podle `data-theme`.
7. **Fonty** self-hosted (Inter 400–800, 5× WOFF2, 1,6 MB), žádný Google Fonts import.
8. **Ikony** 11 z 32 použitých přes CSS `mask-image` (search, memory, tools, mcp, automation, community, agent, install, hosting, skills, security) — tématizovatelné, jak má být.
9. **IndexNow** běží denně 2:00 — log 14. 10.: `HTTP 200 (submitted 73 URLs)`.
10. **66 přesměrovávacích stubů** (62 blog + 4 kořenové) — všechny mají canonical na cílovou URL a cíl existuje.
11. **WebMCP** `find_hermes_guide` zachován v `index.html` i `assets/script.js`; partner odkaz ŠipkyLiga v patičce 76 stránek; MultiBrains v patičce, SEO Test v menu.

---

## 3. 🔧 Nalezené chyby (s důkazy)

### 3.1 Přepínač jazyka vede na 404 u 29 z 75 stránek — **vážné**
`switchLang()` v `assets/script.js` jen přepisuje cestu (`/en` + cesta), netuší skutečné protějšky:

| Stránka | Přepínač vede na | Realita |
|---|---|---|
| `/instalace/` | `/en/instalace/` | EN je `/en/installation/` |
| `/co-je-hermes/`, `/funkce/`, `/komunita/` | `/en/…` | EN verze neexistují (404) |
| `/blog/stranka/2/`, `/blog/stranka/3/` | `/en/blog/stranka/2/` | EN je `/en/blog/page/2/` |
| 10 CZ článků s jiným EN slugem (např. `ai-agent-na-vps-contabo`) | `/en/blog/clanek/<cz-slug>/` | EN slug je `ai-agent-on-vps-contabo` |
| 9 EN článků | `/blog/clanek/<en-slug>/` | CZ slug je jiný |
| `/en/installation/` | `/installation/` | CZ je `/instalace/` |
| `/404.html`, `/500.html` | `/en/404.html` | neexistuje |

Důkaz: `audit_langswitch.py` (29/75) + živé `curl /en/co-je-hermes/` → **404**.

### 3.2 Mobil: hero obrázek route stránek je ořezaný — **vážné (vizuální)**
Při 390 px je `.route-hero-art` **590×215 px** ve 358px sloupci; `overflow: hidden` kraj ořezává.
Příčina: `.route-hero-art--hero` má inline `aspect-ratio: 1920/700` a media query ≤560 px nastavuje
`min-height: 215px` → šířka se dopočítá jako 215 × 1920/700 ≈ 590 px, grid item s `min-width: auto` se nesmrkne.
Dokumentové přetečení je 0, proto to dosavadní QA („60+ checks, 0 overflow“) nezachytilo.
Důkaz: CDP měření `/instalace/`, `/hosting/`, `/blog/`, `/faq/` při 390 px.

### 3.3 Chybí EN mutace 3 CZ stránek — **parita CZ/EN**
`/co-je-hermes/`, `/funkce/`, `/komunita/` existují jen česky (živě `/en/co-je-hermes/` → 404),
a tyto CZ stránky mají `hreflang="en"` na homepage `https://hermes-ai.cz/en/` místo protějšku.

### 3.4 Chybové stránky se mohou indexovat
`404.html` i `500.html` mají `robots: index, follow` a `canonical` samy na sebe. Má být `noindex`.

### 3.5 Redesign není v gitu — **největší riziko**
`HEAD` == `origin/main` == `9a4b0df` = **stará struktura webu**. `instalace/`, `co-je-hermes/`,
`funkce/`, `komunita/`, `assets/redesign/` v commitu nejsou; redesign žije jen v pracovním stromu
(182 staged, 77 modified, 11 modified-staged, 40 untracked). Větev `feat/redesign` **nemá protějšek na GitHubu**.
Tag `v-pre-redesign-2026-10-12` je stav **před** redesignem, ne záloha redesignu.

### 3.6 Chybí tar záloha z plánu
`PLAN.md` blok 0 slibuje `/root/.hermes/cache/scratch/hermes-ai-web-backup-pre-redesign.tar.gz` — **neexistuje**.

### 3.7 Nepoužité soubory v produkci — 51 souborů / ~7,2 MB
Nejtěžší: `hero-ai-agent-approved.png` 1,9 MB, `co-je-hermes.png` 2,0 MB, `hosting-hero.png` 1,8 MB,
`skills-hero.png` 0,85 MB (vedle používaných `.webp`), 21 nepoužitých ikon, `theme-toggle.js`,
`logos/manifest.json`, `favicon-dark/light.ico`, `hero-ai-agent-dark/light.webp`.
Mimo `assets/redesign/` pak nepoužitelné staré assety: `assets/favicon.ico`, `favicon.svg`,
`apple-touch-icon.png`, `site.webmanifest`, `og-image.png`, `hermes.jpg`, `android-chrome-*.png`
a starý `assets/style.css` (nikdo na něj neodkazuje).

### 3.8 Plán sliboval `assets/style-legacy.css` — nevznikl
Starý `assets/style.css` (19 KB, 9. 7.) zůstal na původním jménu; rollback přes CSS tedy není připravený.

### 3.9 Nedodržené detaily z `PLAN.md`
- `theme-color` meta chybí na **všech 142** stránkách.
- `rel="manifest"` na **0** stránkách (`assets/site.webmanifest` má prázdné `name`/`short_name`).
- `apple-touch-icon` jen na 5 stránkách.
- Sekční ilustrace z `PAGE_ASSET_MAP.json` (`blog.svg`, `faq.svg`, `funkce.svg`, `instalace.svg`, `skills-mcp.svg`, `co-je-hermes.svg`) se **nepoužívají vůbec**.
- Breakpointy v CSS jsou 560/820/1080 px, plán uvádí 360/768/1024/1440 px.
- Token `--transition` chybí (`--radius` je).
- Plán mluví o „21 SVG ikonách“, balíček jich má 32.

### 3.10 Balíček `redesing/` už není zdrojem pravdy
17 souborů se stejným jménem má v balíčku a v produkci **jiný obsah** (7 SVG/WebP sekcí + loga
`hermes-ai-logo-dark/light.svg`). Úpravy v produkci se do balíčku nepropsaly → při dalším
redesignu z balíčku by se vrátila stará verze grafiky.

### 3.11 Menší nálezy
- `robots.txt` má osiřelý komentář `# IndexNow` na konci.
- Certbot deploy hook `stats.crafteria.cz → Plan keystore` končí chybou
  `container rootfs is marked read-only` (nesouvisí s hermes-ai, ale hlásí se to u každé obnovy).
- Dokumentace si protiřečí ve stránkování EN blogu: `README.md`/skill uvádí `/en/blog/stranka/`,
  realita i `PLAN.md` je `/en/blog/page/`.

---

## 4. ⏳ Z plánu nehotové

| Bod plánu | Stav |
|---|---|
| F0 tar záloha před redesignem | ✗ (git tag ano) |
| F6 commit + push redesignu | ✗ (nic necommitnuto, nic na GitHubu) |
| `style-legacy.css` pro rollback | ✗ |
| `theme-color` meta | ✗ |
| Ikony jako sprite + inline `<svg>` | částečně — použito CSS `mask-image`, 11/32 |
| Sekční ilustrace dle `PAGE_ASSET_MAP.json` | ✗ |
| `rel="manifest"` + apple-touch-icon na všech stránkách | ✗ |

---

## 5. Plán oprav (pořadí dle rizika)

| # | Oprava | Odhad | Dopad |
|---|---|---|---|
| 1 | **Commit + push redesignu** na `feat/redesign` + PR proti `main`; pak tar záloha | 10 min | odstraní riziko ztráty celého redesignu |
| 2 | **Přepínač jazyka**: explicitní protějšek místo skládání cesty — doporučuji mapu slugů (`data-lang-href`) generovanou při buildu stránek | 60 min | opraví 29 rozbitých přechodů CZ↔EN |
| 3 | **Mobilní ořez hero artu**: v media ≤560 px zrušit `min-height`/`aspect-ratio` u `.route-hero-art--hero` (`min-height: 0; aspect-ratio: auto`) + `min-width: 0` na wrapperu | 30 min | hero obrázky se na mobilu vejdou celé |
| 4 | **EN mutace 3 stránek** (`/en/about-hermes/`, `/en/features/`, `/en/community/`) + oprava `hreflang="en"` na protějšky | 120 min | parita CZ/EN, čistší SEO signál |
| 5 | **`noindex` na 404.html a 500.html** (+ zrušit canonical na sebe) | 5 min | chybové stránky se nebudou indexovat |
| 6 | **Úklid assetů**: smazat 51 nepoužitých souborů (7,2 MB) + staré kořenové favicony/webmanifest; doplnit favicon set (ico/png, apple-touch-icon) a `rel="manifest"` | 60 min | rychlejší web, méně matoucí repozitář |
| 7 | **Dokumentace**: README + `redesing/PLAN.md` + skill sladit s realitou (stránkování EN, počty ikon, breakpointy, `PAGE_ASSET_MAP`), dořešit `redesing/` vs produkce (17 rozdílných souborů), `theme-color`, `robots.txt` | 60 min | dokumentace = pravda |

**Návrh na pořadí nasazení:** kroky 3, 5, 6, 7 jsou drobné opravy → najednou v jednom commitu;
kroky 2 a 4 jsou funkční změny → vlastní commit. Pak jeden restart/push.

---

## 7. Provedené opravy — hero obrázky (14. 10. 2026, večer)

**Zadání:** správné obrázky do všech hero sekcí + mobilní varianty ze složky
`redesing/images/obrázky`.

**Kontrola balíčku proti produkci (podle SHA-256):** desktopové hero obrázky už v produkci
byly soubor po souboru stejné jako zdroje v balíčku:

| Stránka | Zdroj v balíčku | Soubor v produkci |
|---|---|---|
| `/blog/` | `Hermes_Agent_Blog_Operatorka_v1/…1920x700.webp` | `blog-hero.webp` ✅ |
| `/faq/` | `Hermes_Agent_FAQ_Operatorka_v1/…1920x700.webp` | `faq-hero.webp` ✅ |
| `/hosting/` | `Hermes_Agent_Hosting_Operatorka_v1/…1920x700.webp` | `hosting-hero.webp` ✅ |
| `/skills/` | `Hermes_Agent_Skills_Operatorka_v1/…1920x700.webp` | `skills-hero.webp` ✅ |
| `/instalace/` | `Hermes_Instalace_Operatorka_v2/…1920x700.webp` | `installation-hero.webp` ✅ |
| homepage hero | `hero-ai-agent-filled-left.webp` | `hero-ai-agent-approved.webp` ✅ |
| `/komunita/` | `Hermes_Agent_Community_Hero_Assets/…1600x900.webp` | `community.webp` ✅ |

**Co chybělo a bylo doplněno** — 5 mobilních variant 768×960 (v produkci nebyly vůbec):

```
assets/redesign/images/sections/blog-hero-mobile.webp          99 KB
assets/redesign/images/sections/faq-hero-mobile.webp          102 KB
assets/redesign/images/sections/hosting-hero-mobile.webp      108 KB
assets/redesign/images/sections/skills-hero-mobile.webp       108 KB
assets/redesign/images/sections/installation-hero-mobile.webp  86 KB
```

**Změny v kódu:**
- 10 stránek (`/instalace/`, `/hosting/`, `/skills/`, `/faq/`, `/blog/` + EN protějšky):
  hero obrázek obalen do `<picture>` s `<source media="(max-width: 560px)">` na mobilní
  variantu; zrušen inline `style="aspect-ratio: 1920 / 700"` na wrapperu.
- `assets/redesign/style.css`:
  - `.route-hero-art--hero` — zrušeno `aspect-ratio: 1672/941`, přidáno `min-width: 0`
    (pevný poměr + `min-height` nutil wrapper šířku 590 px na mobilu a 823 px na desktopu,
    což `overflow: hidden` ořezával);
  - `.route-hero-art picture { display: block; width: 100% }`;
  - v media ≤560 px: `.route-hero-art--hero { min-height: 0 }` a `img.hero-artwork { height: auto !important }`.

**Ověření v prohlížeči (Chromium CDP, 10 stránek × 2 motivy × 2 viewporty = 40 měření):**
- mobil 390 px: `currentSrc` = `*-hero-mobile.webp`, vykresleno **358×448 px**, bez ořezu, bez přetečení;
- desktop 1280 px: `currentSrc` = `*-hero.webp`, vykresleno **641×234 px**, celý obrázek v kontejneru;
- před opravou: wrapper 823×300 px při šířce sloupce 641 px → **182 px (22 %) obrázku bylo na desktopu ukrojeno**;
  na mobilu 590×215 px ve 358px sloupci → ukrojeno 232 px;
- 0 rozbitých obrázků, 0 horizontálního přetečení.

**Zbývající (záměrný) ořez:** `/co-je-hermes/`, `/funkce/`, `/komunita/`, `/blog/stranka/2–3/`
používají párové obrázky s `object-fit: cover` (design záměrně vyplňuje box) — v balíčku k nim
mobilní varianty nejsou, proto se nemění.

**Nevyužitý zdroj v balíčku:** `Hermes_Agent_Instalace_Hero_Assets/…illustration_1020x768.webp`
(ilustrace do obsahové sekce `/instalace/`) — nikde nasazená; případný další krok.


- Nahradit 66 meta-refresh stubů skutečnými **301 v nginx** (`map`/`rewrite`) a stuby smazat.
- Doplnit **deploy hook pro `nginx -s reload`** po obnově certifikátu (dnes se spoléhá na ruční reload).
- Přidat do `.gitignore` archiv `redesing/images/obrázky/` (zdrojové koncepty, nezveřejňovat).
- Zvážit `loading="lazy"` + `srcset` u sekčních WebP (dnes jednotný 1920×700).
