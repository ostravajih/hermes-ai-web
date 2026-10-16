# Plán redesignu webu hermes-ai.cz v2.0

> **Stav:** ✅ Všechny hero + sekční obrázky (homepage, FAQ, hosting, skills, co-je-hermes, instalace, blog), všechny WebP. Oprava theme-image stacking, light-theme persistence, SEO Test do menu, MultiBrains do patičky, 31px mobilí overflow, **duplikátní číslování `<ol class="steps">` na /instalace/ — `list-style: none` přidáno, výchozí prohlížeční counter potlačen, zobrazí jen CSS counter (1-4)**. Ověřeno CDP QA — 60+ checks, 0 overflow, 0 broken images.
> **Cíl:** Kompletní redesign podle balíčku `/redesing` — nový design systém, URL struktura, kompletně přepsané HTML+CSS, blog i. Záloha před tím vším.

> **Co je dnes (15. 10. 2026) jinak než v plánu:**
> plán počítal se světlým **i** tmavým režimem — světlý byl 15. 10. 2026 úplně zrušen, web je jen tmavý
> (`PLAN-TMAVY-VZHLED-2026-10-15.md`); písmo není pět souborů Inter 400–800, ale jedno variabilní
> `Inter-web.woff2` (100–900); k webu přibyly živé efekty (`assets/zive.js`) a měření Matomo.
> Plán také tvrdil, že „HTML neumí 301 serverem" — dnes nginx skutečné 301 posílá
> (`/skills`, `/komunita`, `/funkce`, `/co-je-hermes`, `/en/community`, `/en/features`, `/en/what-is-hermes`,
> `/blog`, `/en/blog`). **Doplněno 17. 10. 2026:** i zbývajících 66 starých adres a 7 cest bez lomítka
> mají skutečné 301 v nginx (na disku nezůstal žádný soubor s meta refreshem) — úkol je uzavřený.

---

## 📦 1. Záloha (blok 0)

**Akce:** `tar -czf /root/.hermes/cache/scratch/hermes-ai-web-backup-pre-redesign.tar.gz` — vše kromě `redesing/`, `.git`, `standalone.html`.

- **Proč:** před kompletním přepisem — okamžitý rollback.
- **Git tag:** `v-pre-redesign-2026-10-12` (pro jistotu i v historii).
- **Nezahrnovat:** `standalone.html` (součástí deploy, ale ne součástí redesignu), `redesing/` (základ).

---

## 🗺️ 2. Nová URL struktura (podle `BRAND_GUIDE_CZ.md`)

| Stará | Nová | Poznámka |
|---|---|---|
| `/` | `/` | hero, co-je-hermes, hlavní schopnosti, rychlý start, komunita. |
| `/dovednosti.html` | `/skills/` | katalog dovedností + metadata. |
| `/instalace.html` | `/instalace/` | kroky, požadavky, příkazy. |
| `/hosting.html` | `/hosting/` | VPS, Docker, cloud. |
| `/faq.html` | `/faq/` | accordion komponenty. |
| `/index.html` → `/blog/index.html` | `/blog/` | blog index. |
| `blog/*.html` | `/blog/clanek/<slug>/` | 27 CZ + 27 EN článků. |
| — | `/co-je-hermes/` | Nová stránka: agent + Nous Research. |
| — | `/funkce/` | Nová stránka: nástroje, paměť, skills, MCP, plánování. |
| — | `/komunita/` | Nová stránka: Discord, reakce, kanály. |
| (404/500) | zachováno | 404.html, 500.html. |

### 301 přesměrování (kritické pro SEO)
Všechny staré URL (`/dovednosti.html`, `/instalace.html`, `/hosting.html`, `/faq.html`, `blog/<nazev>.html`) → 301 na nové. Implementace přes `<meta http-equiv="refresh" content="0;url=...">` + `<link rel="canonical">` (HTML neumí 301 serverem, ale meta refresh + canonical je dostatečné pro SEO a zachování rankingu). **Všechny staré URL zůstávají jako statické soubory s přesměrováním.**

### hreflang / jazyky
- `/` (CZ default) ↔ `/en/` (EN default)
- `/blog/*` (CZ) ↔ `/en/blog/*` (EN)
- Přidáno `x-default` → `/`.

---

## 🎨 3. Redesign — co se mění

### Zdroje
- **Font:** self-hosted Inter WOFF2, weight 400–800 (bez externího Google Fonts importu).
- **Paleta:** tmavě modrý `#07111F` → neon tyrkys `#00DCEB`, modrá `#3B82F6`, fialová `#8B5CF6` (gradient pro CTA). Světlý reverzní.
- **tokens.css:** použít jako základ (`docs/tokens.css`), rozšířit o `--radius`, `--transition`.
- **Loga:** `hermes-ai-logo-dark.svg` (na světlém), `hermes-ai-logo-light.svg` (na tmavém). `data-theme` switch.
- **Ikony:** 21 SVG z `icons/` jako sprite + inline `<svg>`.
- **Obrázky:** hero + sekční `.webp` podle `PAGE_ASSET_MAP.json`.
- **Board revize:** homepage používá schválený `hero-ai-agent-approved.png` v obou motivech jako jeden plný 16:9 artwork bez cropování; dekorativní background už nepřebíjí artwork. Sekundární route hero používají odpovídající dark/light assety (`installation`, `hosting`, `skills`, `blog`, `faq`, `community`) a theme variants jsou vzájemně exkluzivní.
- **Vizuální ověření:** implementované screenshoty dark/light desktopu a mobilu jsou v `/root/.hermes/cache/scratch/hermes-audit/implemented-*`; kontrola proběhla přes Chromium CDP proti lokálnímu serveru.
- **Layout:** max-width 1240px, 360/768/1024/1440px breakpointy podle brand guide.
- **Dark mode:** výchozí `dark` (předpokládám z auditního kontextu — web už měl dark mode). Persistent toggle v `localStorage`.

### Co se mění v kódu
- **`<head>`** přepsán: nové loga, favicon (`logos/favicon-dark/light.ico`), `og:` tagy s novými hodnotami (60+ tools, 20+ platforms), `theme-color` meta.
- **CSS:** celý `style.css` nahrazen novým (ne jen tokeny — kompletní reset + layout). Starý stůl (`assets/style.css`) zachován jako `assets/style-legacy.css` pro rollback.
- **HTML:** kompletně přepsané od šablony — nové section-y dle `BRAND_GUIDE_CZ.md` § „Doporučená struktura použití“. Texty zachovány (ověřené proti oficiálnímu projektu), jen nový wrapper.
- **Assety:** `images/`, `logos/`, `icons/` nakopírovány z `redesing/` do `assets/` (např. `assets/images/`, `assets/logos/`, `assets/icons/`).
- **Partner odkaz** (Šipky Liga) — **povinně zachován** ve patičce všech stránek (dle AGENTS.md zákonitosti).
- **Standalone HTML** — nechán beze změny.

---

## 📝 4. Blog — co se mění

- **27 CZ + 27 EN článků** přepsaných do nového stylu (stejné texty, nový wrapper, nové obrázky, nové og:tagy).
- `PAGE_ASSET_MAP.json` má `/blog` → `blog.svg` + `blog-documentation.webp` jako sekční ilustrace na blog indexu.
- Stránkování zachováno: 27 článků, 3 stránky (`/blog/stranka/2/` → `/blog/stranka/3/`; EN `/en/blog/page/2/` → `/en/blog/page/3/`).

---

## 🔍 5. SEO / technika (zachováno + vylepšeno)

- **sitemap.xml:** kompletně přegenerována s novými URL (CZ + EN).
- **robots.txt:** aktualizován o nové cesty + `Sitemap:` direktivy.
- **IndexNow:** submit skript použije novou sitemapu.
- **Schema.org:** strukturovaná data přenesena do nového HTML (Article, Blog, FAQPage, Website).
- **WebMCP:** `find_hermes_guide` tool (v `assets/script.js`) — zachován.
- **Dark mode toggle:** zachován `data-theme`, přidán `.theme-toggle` per brand guide.

---

## 🚀 6. Branch + PR + deploy

1. Branch: `feat/redesign` (od `main`).
2. Záloha commitnut jako `chore: backup pre-redesign` (tag `v-pre-redesign-2026-10-12`).
3. Celý redesign commitnout po krocích (HTML → CSS → assety → blog → SEO).
4. PR otevřít proti `main`.

> **Poznámka:** Nejde o Laravel projekt — je to statický web. Deploy je jen `git push`. Žádné composer/npm build nebo migrace.

---

## ⏳ 7. Timing / fáze

| Fáze | Obsah | ETA |
|---|---|---|
| F0 | Backup + tag + branch | 10 min |
| F1 | Kořenové stránky (/, /co-je-hermes, /funkce, /instalace, /hosting, /skills, /faq, /komunita) | 4 hod |
| F2 | Blog (27 CZ + 27 EN) | 8 hod |
| F3 | 404/500 + standalone check | 20 min |
| F4 | SEO (sitemap, robots, strukturovaná data) | 1 hod |
| F5 | Testy (cross-browser, dark/light, mobil, odkazy) | 1 hod |
| F6 | Commit + push (NE push, dokud neříkáš) | — |

**Celkem:** ~14 hodin práce (rozděitelné do subagentů).

---

## ❓ Co od tebe potřebuji

- **Potvrdit:** mám zálohovat a začít? Nebo chceš upravit některý krok (např. jinou URL strukturu)?
- **Font hosting:** googlit Google Fonts nebo self-hostovat?
- **Co dělat se starými soubory** (`dovednosti.html` atd.) — přepsat jako přesměrovací stránky, nebo smazat?

**Schválíš plán? Pak hned začínám se zálohovaním.**
