# SEO a HTML audit — hermes-ai.cz

> **Upozornění:** Tento audit je ze dne **2026-07-09** a neodráží změny od té doby. Je to **historie** —
> needitujte ho jako aktuální stav. Od 10.–12. 10. 2026 proběhl kompletní redesign (`redesing/PLAN.md`):
> nová CSS, jedno variabilní self-hosted písmo Inter, nahrazení hero obrázků WebP, SEO Test a MultiBrains
> v menu/patičce, oprava mobilního overflow. Dále 15. 10. 2026: **světlý režim zrušen** (web je jen tmavý),
> přidány živé efekty (`assets/zive.js`), měření Matomo a nastaveny e-mailové záznamy SPF/DKIM/DMARC.
> **Aktuální stav webu je v `README.md`** v kořeni.

**Datum:** 2026-07-09  
**Doména:** `https://hermes-ai.cz`  
**Laravel APP URL:** `https://app.multibrains.eu`  
**Celkem HTML souborů:** 71

---

## SOUHRN — NEJKRITIČTĚJŠÍ NÁLEZY

| # | Problém | Počet souborů | Závažnost |
|---|---|---|---|
| 1 | **Poškozené `og:description`** — náhodný text za ukončeným `content` atributem | 2 | 🔴 KRITICKÁ |
| 2 | **Canonical v HTML vs sitemap.xml — trailing slash mismatch** | 27 blog článků | 🔴 KRITICKÁ |
| 3 | **Truncated HTML / neuzavřené tagy (div mismatch)** | 33 souborů | 🔴 KRITICKÁ |
| 4 | **DOCTYPE a `<html>` na jednom řádku** W3C non-conformant | 30 souborů | 🟡 VYSOKÁ |
| 5 | **Chybějící Schema.org JSON-LD** | 61 souborů | 🟡 VYSOKÁ |
| 6 | **Chybějící `og:image:width/height`** | 63 souborů | 🟡 VYSOKÁ |
| 7 | **Chybějící `og:site_name`** | 65 souborů | 🟡 VYSOKÁ |
| 8 | **Chybějící `<main>` tag** | 6 souborů | 🟡 VYSOKÁ |
| 9 | **Chybějící hreflang na blog indexech a stránkování** | 6 souborů | 🟡 VYSOKÁ |
| 10 | **Chybějící `meta author`** | 53 souborů | 🔶 STŘEDNÍ |
| 11 | **Chybějící Twitter Card komponenty** | 53 souborů | 🔶 STŘEDNÍ |
| 12 | **`description` > 160 znaků** | 9 souborů | 🔶 STŘEDNÍ |
| 13 | **Chybějící `site.webmanifest`** | 59 souborů | 🔶 STŘEDNÍ |
| 14 | **404/500 bez SEO elementů** | 2 soubory | 🟡 VYSOKÁ |
| 15 | **Obrázky s prázdným `alt`** | 3 soubory | 🔵 NÍZKÁ |
| 16 | **Backend — chybějící OpenAI API klíč** | `.env` | 🔴 KRITICKÁ |
| 17 | **`robots.txt` — nestandardní `Host:`** | 1 řádek | 🔵 NÍZKÁ |
| 18 | **`lastmod` v sitemap v budoucnosti** | sitemap.xml | 🔶 STŘEDNÍ |

---

## 1. ZÁKLADNÍ HTML STRUKTURA A W3C VALIDITA

### 1.1 DOCTYPE `<html>` na stejném řádku — 30 souborů (VYSOKÁ)

30 souborů má `<!DOCTYPE html><html lang="cs"><head>` na **jednom řádku**. W3C standard sice nevyžaduje newline po DOCTYPE, ale minimálně 30 souborů dramaticky zhoršuje čitelnost a ladicí nástroje mohou selhat.

**Kompletní seznam postižených souborů:**

**CS blog články (12):**
- `blog/hermes-agent-aktualizace-2026.html`
- `blog/hermes-agent-google-gemini.html`
- `blog/hermes-agent-multi-platform.html`
- `blog/hermes-agent-open-source.html`
- `blog/hermes-agent-profily.html`
- `blog/hermes-agent-raspberry-pi.html`
- `blog/hermes-agent-soul-md.html`
- `blog/hermes-agent-ssh-vps.html`
- `blog/hermes-agent-system-admin.html`
- `blog/hermes-agent-voice-mode.html`
- `blog/hermes-agent-vs-codex.html`
- `blog/hermes-agent-vs-openclaw.html`

**CS blog indexy (3):**
- `blog/index.html`
- `blog/stranka-2.html`
- `blog/stranka-3.html`

**EN blog články (12):**
- `en/blog/hermes-agent-google-gemini.html`
- `en/blog/hermes-agent-multi-platform.html`
- `en/blog/hermes-agent-open-source.html`
- `en/blog/hermes-agent-profiles.html`
- `en/blog/hermes-agent-raspberry-pi.html`
- `en/blog/hermes-agent-soul-md.html`
- `en/blog/hermes-agent-ssh-vps.html`
- `en/blog/hermes-agent-system-admin.html`
- `en/blog/hermes-agent-updates-2026.html`
- `en/blog/hermes-agent-voice-mode.html`
- `en/blog/hermes-agent-vs-codex.html`
- `en/blog/hermes-agent-vs-openclaw.html`

**EN blog indexy (3):**
- `en/blog/index.html`
- `en/blog/page-2.html`
- `en/blog/page-3.html`

### 1.2 Neuzavřené `<div>` tagy — 33 souborů (KRITICKÁ)

33 souborů (46 %) má nesoulad mezi počtem otevřených `<div` a zavřených `</div>`. Většina z nich má deficit právě **2 zavírací tagy**, což ukazuje na **systematickou chybu v šabloně** — pravděpodobně chybí `</article></div></main></body></html>` na konci.

**Soubory s přesně 2 chybějícími `</div>` (20 souborů):**
- `bezpecnost-hermes-agent.html` (otevřeno 9, zavřeno 6 — diff 3)
- `hermes-agent-aktualizace-2026.html` (4/2)
- `hermes-agent-cron-planovac.html` (11/9)
- `hermes-agent-docker.html` (7/5)
- `hermes-agent-google-gemini.html` (5/3)
- `hermes-agent-macos.html` (8/6)
- `hermes-agent-mcp-integration.html` (9/7)
- `hermes-agent-multi-platform.html` (5/3)
- `hermes-agent-nous-portal.html` (5/3)
- `hermes-agent-ollama-lokalni-llm.html` (11/9)
- `hermes-agent-open-source.html` (6/4)
- `hermes-agent-openrouter.html` (7/5)
- `hermes-agent-profily.html` (7/5)
- `hermes-agent-raspberry-pi.html` (6/4)
- `hermes-agent-soul-md.html` (6/4)
- `hermes-agent-ssh-vps.html` (6/4)
- `hermes-agent-system-admin.html` (7/5)
- `hermes-agent-voice-mode.html` (6/4)
- `hermes-agent-vs-codex.html` (4/2)
- `hermes-agent-vs-openclaw.html` (5/3)

**Soubory s 1 chybějícím `</div>` (13 souborů):**
- `hermes-agent-windows-wsl2.html` (8/7)
- `hermes-webui-pruvodce.html` (11/9)
- `blog/index.html` (14/13)
- `jak-pouzivat-hermes-skills.html` (9/8)
- `stranka-2.html` (14/13)
- `stranka-3.html` (14/13)
- `en/blog/hermes-agent-docker.html` (6/5)
- `en/blog/hermes-agent-security.html` (8/7)
- `en/blog/hermes-agent-windows-wsl2.html` (8/7)
- `en/blog/how-to-use-hermes-skills.html` (8/7)
- `en/blog/index.html` (14/13)
- `en/blog/page-2.html` (14/13)
- `en/blog/page-3.html` (14/13)

**Poznámka:** Soubor `blog/hermes-agent-aktualizace-2026.html` končí na 33. řádku znakem `>` — HTML je useknuté uprostřed článku. Pravděpodobně toto je chyba generovacího skriptu.

### 1.3 Správné DOCTYPE a lang — OK

Všechny stránky (které nejsou useknuté) mají:
- ✅ `<!DOCTYPE html>` — HTML5
- ✅ `lang="cs"` nebo `lang="en"`
- ✅ `<meta charset="UTF-8">`
- ✅ `<meta name="viewport" ...>`

---

## 2. ZÁKLADNÍ META TAGY

### 2.1 `meta description` — 2 soubory chybí, 9 má >160 znaků

**Zcela chybí:**
- `404.html`
- `500.html`

**Přesahuje 160 znaků (9 souborů):**
- `blog/hermes-webui-pruvodce.html` (164 znaků)
- `en/blog/hermes-agent-cron-scheduler.html` (167)
- `en/blog/hermes-agent-multi-platform.html` (163)
- `en/blog/hermes-agent-ollama-local-llm.html` (166)
- `en/blog/hermes-agent-openrouter.html` (161)
- `en/blog/hermes-agent-ssh-vps.html` (161)
- `en/blog/hermes-agent-voice-mode.html` (163)
- `en/blog/hermes-agent-vs-codex.html` (161)
- `en/blog/hermes-agent-windows-wsl2.html` (163)
- `en/blog/hermes-webui-guide.html` (161)

### 2.2 `meta robots` — chybí na 2 souborech

- `404.html` — **měl by mít `noindex`** (chybové stránky by neměly být v indexu)
- `500.html` — **měl by mít `noindex`**

### 2.3 `meta author` — chybí na 53 souborech (74 %)

Kompletní chybí na:
- `404.html`, `500.html`
- Všech CS blogových článcích (kromě `ai-agent-na-vps-contabo`, `instalace-hermes-agent-ubuntu`, `telegram-bot-hermes-agent`)
- Všech EN podstránkách a EN blogových článcích
- `faq.html`

**Mají OK:** `index.html`, `instalace.html`, `hosting.html`, `dovednosti.html`, a 3 CS blogové články.

### 2.4 Canonical URL — 2 soubory zcela chybí, 27 článků má mismatch se sitemap

**Zcela chybí canonical:**
- `404.html`
- `500.html`

**Canonical vs sitemap trailing slash neshoda (27 blogových článků):**

HTML canonical v blogových článcích používá trailing slash:
```html
<link rel="canonical" href="https://hermes-ai.cz/blog/hermes-agent-docker/">
```

Ale sitemap.xml uvádí URL bez lomítka:
```xml
<loc>https://hermes-ai.cz/blog/hermes-agent-docker</loc>
```

Toto je zásadní SEO chyba — Google dostává dva protichůdné signály. Všechny články v `sitemap.xml` je potřeba opravit přidáním trailing slashe.

---

## 3. OPEN GRAPH TAGY

### 3.1 `og:image:width` a `og:image:height` — chybí na 63 souborech (89 %)

Mají je pouze: `index.html`, `instalace.html`, `hosting.html`, `dovednosti.html`, `en/index.html`, `en/hosting.html`, `en/skills.html`, `en/installation.html`.

### 3.2 `og:site_name` — chybí na 65 souborech (92 %)

Tento tag nemá **žádná** stránka. Chybí na úplně všech HTML souborech.

### 3.3 `og:description` — poškozený obsah (KRITICKÉ)

**`instalace.html:18`:**
```html
<meta property="og:description" content="...Windows.", učí se a roste. 47+ nástrojů, 15+ platforem, MIT licence.">
```
Za uzavřeným `content="..."` následuje náhodný fragment z jiné šablony.

**`dovednosti.html:18`:**
```html
<meta property="og:description" content="...Hermes Agent.", učí se a roste. 47+ nástrojů, 15+ platforem, MIT licence.">
```
Stejná chyba.

### 3.4 `og:image` a `og:type`/`og:url` na blog indexech — chybí (VYSOKÁ)

Blog indexy a stránkování (6 souborů) postrádá:
- `og:image`, `og:description`, `og:type`, `og:url`
- `blog/index.html`, `blog/stranka-2.html`, `blog/stranka-3.html`
- `en/blog/index.html`, `en/blog/page-2.html`, `en/blog/page-3.html`

---

## 4. TWITTER CARD TAGY

### 4.1 Chybějící `twitter:title` — 48 souborů

Chybí na většině blogových článků (CS i EN), `en/faq.html`, a `404.html`/`500.html`.

### 4.2 Chybějící `twitter:image` — 55 souborů

Chybí na: většině blogových článků, `faq.html` (CS), `en/faq.html`, a `404.html`/`500.html`.

### 4.3 Chybějící `twitter:card` — 8 souborů

Chybí na: `404.html`, `500.html`, a všech 6 blog indexech/stránkování.

---

## 5. STRUKTUROVANÁ DATA (SCHEMA.ORG / JSON-LD)

### 5.1 Zcela chybí Schema.org — 61 souborů (86 %) (VYSOKÁ)

**Mají Schema.org (10 souborů):**
- `index.html` — `SoftwareApplication`
- `instalace.html` — `SoftwareApplication`
- `hosting.html` — `Product`
- `dovednosti.html` — `SoftwareApplication`
- `faq.html` — `FAQPage`
- `en/index.html` — `SoftwareApplication`
- `en/hosting.html` — pravděpodobně `Product`
- `en/installation.html` — `SoftwareApplication`
- `en/skills.html` — `SoftwareApplication`
- `en/faq.html` — `FAQPage`

**Chybí na:** `404.html`, `500.html`, všech 30 CS blogových stránkách, všech 30 EN blogových stránkách.

Doporučení: každý blogový článek by měl mít `@type: Article` nebo `BlogPosting` Schema.org.

---

## 6. FAVICON A IKONY

### 6.1 `site.webmanifest` — chybí na 59 souborech (83 %)

Mají manifest pouze: `index.html`, `instalace.html`, `hosting.html`, `dovednosti.html`, `en/index.html`, `en/hosting.html`, `en/installation.html`, `en/skills.html`.

### 6.2 Favicon — 2 soubory zcela bez ikon

`404.html` a `500.html` nemají **žádné** favicon elementy.

### 6.3 Nekonzistentní favicon sada

Různé stránky odkazují na různé kombinace faviconů. Žádná stránka neodkazuje na všechny dostupné varianty v `assets/`:
- `favicon.ico` — existuje, ale NENÍ linkován v žádné stránce
- `favicon-48.png` — existuje, NENÍ linkován
- `favicon-16x32.png` — existuje, NENÍ linkován (pravděpodobně překlep — měl být `favicon-32x32.png`?)

---

## 7. CHYBĚJÍCÍ `<main>` TAG — 6 souborů (VYSOKÁ)

Bez `<main>` sémantického tagu:
- `index.html`
- `hosting.html`
- `en/index.html`
- `en/hosting.html`
- `404.html`
- `500.html`

Hero sekce na těchto stránkách používá `<section>` bez obalení do `<main>`. Na menších stránkách (`instalace.html` atd.) je `<main class="page">` přítomen.

---

## 8. HREFLANG — PROBLÉMY

### 8.1 Zcela chybějící hreflang (6 souborů) (VYSOKÁ)

- `blog/index.html`
- `blog/stranka-2.html`
- `blog/stranka-3.html`
- `en/blog/index.html`
- `en/blog/page-2.html`
- `en/blog/page-3.html`

### 8.2 Chybějící `hreflang="x-default"` — 44 souborů

Většina blogových článků (CS i EN) má hreflang alternativu na druhý jazyk, ale **nemá** `x-default`. Pouze hlavní stránky (index, instalace, hosting, dovednosti, faq) a EN hlavní stránky ho mají správně.

### 8.3 Chybějící `hreflang="cs"` na CS blogových článcích

CS blogové články odkazují pouze:
```html
<link rel="canonical" href="...CS..."><link rel="alternate" hreflang="en" href="...EN...">
```
Chybí `hreflang="cs"` ukazující na sebe sama. Každá jazyková mutace by měla mít hreflang na všechny jazyky včetně sebe.

---

## 9. OBRÁZKY A ALT ATRIBUTY

### 9.1 Prázdné `alt` atributy — 3 soubory

- `hosting.html` — 2 obrázky s `alt=""` (tracking pixely Contabo)
- `en/hosting.html` — 2 obrázky s `alt=""` (tracking pixely Contabo)
- `instalace.html` — 1 obrázek s `alt=""` (tracking pixel Contabo)
- `en/installation.html` — 1 obrázek s `alt=""` (tracking pixel Contabo)

U tracking pixelů je `alt=""` akceptovatelné, ale měly by být skryté přes `aria-hidden="true"`.

---

## 10. NADPISOVÁ HIERARCHIE

Většina stránek má správnou strukturu: 1× `<h1>` na stránku, `<h2>`/`<h3>` pro podnadpisy. Žádná stránka nemá vícenásobný `<h1>`. ✅

---

## 11. ROBOTS.TXT

### 11.1 Nestandardní direktiva `Host:`

```
Host: hermes-ai.cz
```

Toto je historická direktiva pro ruský Yandex. Google ani Seznam ji nerespektují. Doporučeno odstranit.

---

## 12. SITEMAP.XML

### 12.1 `lastmod` v budoucnosti

Všechny URL mají `<lastmod>2026-07-10</lastmod>` — zítřejší datum.

### 12.2 Trailing slash mismatch

Blogové články v sitemap nemají trailing slash, ale HTML canonical ho má. Viz kapitola 2.4.

---

## 13. BACKEND CHYBY (LARAVEL)

### 13.1 Embedding: chybí API klíč (KRITICKÁ)

20 po sobě jdoucích chyb v logu (2026-07-06):
```
production.ERROR: Embedding failed — "You didn't provide an API key..."
```
Nastavte `OPENAI_API_KEY` v `.env`.

### 13.2 APP_URL nesoulad

Laravel: `APP_URL=https://app.multibrains.eu`  
Statický web: `https://hermes-ai.cz`

---

## 14. PAGE-SPECIFIC REPORT (stránky s 3+ chybami)

| Stránka | DOCTYPE | div mismatch | chybí Schema | chybí og:w/h | chybí author | chybí twitter:title | chybí manifest |
|---|---|---|---|---|---|---|---|
| `404.html` | ✅ | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| `500.html` | ✅ | ✅ | ✗ | ✗ | ✗ | ✗ | ✗ |
| `blog/index.html` | ❌ 1ř. | ✗ (14/13) | ✗ | ✗ | ✗ | ✗ | ✗ |
| `blog/stranka-2.html` | ❌ 1ř. | ✗ (14/13) | ✗ | ✗ | ✗ | ✗ | ✗ |
| `blog/stranka-3.html` | ❌ 1ř. | ✗ (14/13) | ✗ | ✗ | ✗ | ✗ | ✗ |
| `en/blog/index.html` | ❌ 1ř. | ✗ (14/13) | ✗ | ✗ | ✗ | ✗ | ✗ |
| `en/blog/page-2.html` | ❌ 1ř. | ✗ (14/13) | ✗ | ✗ | ✗ | ✗ | ✗ |
| `en/blog/page-3.html` | ❌ 1ř. | ✗ (14/13) | ✗ | ✗ | ✗ | ✗ | ✗ |
| `faq.html` | ✅ | ✅ | ✅ | ✗ | ✗ | ✅ | ✗ |
| `instalace.html` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `dovednosti.html` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 15. KOMPLETNÍ CHECKLIST DLE KONTROLNÍHO SEZNAMU

| Pravidlo | Stav | Poznámka |
|---|---|---|
| DOCTYPE na 1. řádku | ⚠️ 58% | 30/71 na stejném řádku s `<html>` |
| `lang` atribut na `<html>` | ✅ 100% | Vše OK |
| `charset="UTF-8"` jako první v `<head>` | ✅ 100% | Vše OK |
| Validní zanořování tagů | ❌ 46% | 33 souborů má `div` mismatch |
| Sémantické značky (`<main>`, `<nav>`...) | ⚠️ 8% chybí `<main>` | 6 souborů |
| `meta description` | ⚠️ 3% chybí, 13% >160 zn. | 2 chybí, 9 přes limit |
| `meta robots` | ⚠️ 3% chybí | 404/500 |
| `meta author` | ❌ 74% chybí | 53 souborů |
| Canonical URL (absolutní) | ⚠️ 3% chybí, 38% mismatch | 2 chybí, 27 mismatch |
| `og:title` | ✅ 100% | Vše OK |
| `og:description` | ❌ 2 poškozené | instalace, dovednosti |
| `og:type` | ⚠️ 8% chybí | Blog indexy |
| `og:url` | ⚠️ 8% chybí | Blog indexy |
| `og:image` | ⚠️ 11% chybí | Blog indexy + 404/500 |
| `og:image:width` | ❌ 89% chybí | 63 souborů |
| `og:image:height` | ❌ 89% chybí | 63 souborů |
| `og:locale` | ✅ 100% | Vše OK |
| `og:site_name` | ❌ 100% chybí | Není nikde |
| `twitter:card` | ⚠️ 11% chybí | Blog indexy + 404/500 |
| `twitter:title` | ⚠️ 68% chybí | 48 souborů |
| `twitter:image` | ⚠️ 77% chybí | 55 souborů |
| Schema.org JSON-LD | ❌ 86% chybí | 61 souborů |
| `favicon` (alespoň 1 ikona) | ⚠️ 3% chybí | 404/500 |
| `apple-touch-icon` | ⚠️ 70% chybí | ~50 souborů |
| `site.webmanifest` | ❌ 83% chybí | 59 souborů |
| `<h1>` právě jeden | ✅ 100% | Vše OK |
| `alt` na obrázcích | ⚠️ 4 tracking pixely | Prázdný alt |
| hreflang alternativy | ❌ 8% zcela chybí, 62% bez x-default | 6 + 44 souborů |
| `robots.txt` | ⚠️ nestandardní `Host:` | |
| `sitemap.xml` | ⚠️ `lastmod` v budoucnosti + trailing slash mismatch | |
