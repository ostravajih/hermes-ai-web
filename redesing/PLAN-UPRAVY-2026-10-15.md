# Plán úprav: patička, menu, nadpisy, 301 pro staré adresy, cron 04:00

**Datum:** 15. 10. 2026 · **Zpracoval:** Hermes · **Stav:** ✅ **provedeno a ověřeno 15. 10. 2026**

## Výsledek (co je nasazené)

| Bod | Stav | Ověřeno |
|---|---|---|
| 1. Patička — „Naše Projekty“ + ikony komunity | ✅ 78 stránek | 4 ikony (Discord/Facebook/Instagram/e-mail) se vykreslují, 5 zpětných odkazů bez `nofollow`, kontrola screenshotem |
| 2. Hlavička — prohození přepínače a tlačítka | ✅ 78 stránek | na 1280/1024/820/700/560/390 px je přepínač **vidět** (dřív se na ≤560 px skrýval) |
| 3. Nadpisy — menší + vycentrované | ✅ 54 článků + 404/500 | článek 76,8 → **67,8 px** (cíl 68), na střed; 404/500 80 → **68 px** na střed; datum a perex vlevo |
| 4. Smazat ukázku `/ukazka/` | ✅ | vrací **404**, řádek v `robots.txt` odstraněn |
| 5. Staré adresy → 301 | ✅ 66 adres | všech **66 vrací 301 → 200** (58 z nich dřív vracelo **404**) |
| 6. Sitemap + IndexNow + cron 04:00 | ✅ | cron `0 4 * * *`, ruční běh: 76 adres, **IndexNow HTTP 200**, `lastmod` 2026-10-15 |
| 7. Dokumentace | ✅ | `README.md`, `llms.txt`, `OPRAVY-CELEHO-WEBU-2026-10-15.md`, tento plán, skill |

**Rozhodnutí uživatele:** odkazy na Minecraft List **oba** (CZ/SK i EN/DE) · centruje se **jen nadpis**
(perex a datum vlevo) · velikost nadpisu **68 px** · pomocné soubory s přesměrováním **smazat**.

**Odchylky od plánu (nutné opravy při nasazení):**

1. **Nadpis 404/500 nebyl vycentrovaný** — měl `max-width: 11ch` a `margin: 0`, takže text stál
   vlevo od středu. Doplněno `margin: 0 auto`.
2. **Přepínač jazyka se na telefonu skrýval** (`.nav-actions .lang-switch { display: none }` v ≤560 px) —
   to je přesně to „ztrácení“, na které uživatel upozornil. Pravidlo změněno na `display: inline-flex`.
3. **Datum pod nadpisem bylo v HTML natvrdo na střed** — srovnáno vlevo (u 54 článků), aby odpovídalo
   volbě „jen nadpis na střed“.
4. **Past při vzorových 301:** pravidlo na `…/blog/<nazev>.html` chytilo i interní přesměrování
   nginx na `index.html` a rozbilo adresy `/blog/` a `/en/blog/`. Do výrazu přidána výjimka `index`.

---


**Datum:** 15. 10. 2026 · **Zpracoval:** Hermes · **Stav:** 🟡 návrh ke schválení
**Vychází z:** kontroly živého webu a kódu z 15. 10. 2026 (měřeno `curl` + prohlížečem)

---

## 0. Co se během přípravy našlo (důležité)

Původní domněnka, že staré adresy „vedou na 404“, se **potvrdila u 58 adres**.
Vzal jsem starou sitemapu z historie gitu (70 adres, commit `9a4b0df`) a otestoval každou živě:

| Stav dnes | Počet | Co to je |
|---|---|---|
| **404** | **58** | 54 starých adres článků (`/blog/<nazev>/` místo nového `/blog/clanek/<nazev>/`) + 4 stará stránkování (`/blog/stranka-2/`, `/blog/stranka-3/`, `/en/blog/page-2/`, `/en/blog/page-3/`) |
| 301 (hotovo) | 7 | cesty bez lomítka (`/instalace`, `/hosting`, …) |
| 200 s přesměrováním uvnitř | 1 | `/dovednosti` |
| v nové sitemapě | 4 | `/blog/…/2/`, `/en/blog/…/2/` (nové stránkování) |

Tyhle adresy **byly ve staré sitemapě**, takže je vyhledávače znají a dnes na nich ukazují 404.
To je přesně to, co je potřeba opravit — a je to větší problém než 7 cest, které jsem opravil ráno.

---

## 1. Patička — „Naše Projekty“ + ikony komunity

**Kde:** 78 živých stránek (40 CZ s „Komunita“, 38 EN s „Community“). Dnes má patička sloupce
`Produkt | Zdroje | Komunita` a pod logem text *„Otevřený AI agent pro každého. Komunita, návody,
nástroje a inspirace.“*

**Změny:**
1. Sloupec **„Komunita“ → „Naše Projekty“** (EN: „Our projects“) s odkazy na naše projekty
   (odkazy **bez** `nofollow`, aby se počítaly jako zpětný odkaz; `target="_blank" rel="noopener"`):
   - Šipky Liga → `https://www.sipkyliga.cz/`
   - MultiBrains → `https://www.multibrains.eu/`
   - SEO Test → `https://www.seotestzdarma.cz/`
   - Minecraft List → `https://minecraftlist.cz/`
   - MultiBrains se ze sloupce „Produkt“ odebere (byl by dvakrát)
2. **Ikony komunity pod text** *„…Komunita, návody, nástroje a inspirace.“* (EN pod anglickým textem):
   - Discord → `https://discord.gg/ysx9dbXpdD` (nový, neomezený)
   - Facebook → `https://www.facebook.com/hermesai`
   - Instagram → `https://www.instagram.com/hermesaiagent/`
   - E-mail → `mailto:kontakt@hermes-ai.cz`
   - Ikony jsou vlastní SVG v barvách webu (žádná externí knihovna), s popiskem pro čtečky.
3. Zbytek patičky: `Skills | Blog | FAQ | GitHub` zůstává, odkazy `Discord`/`Kontakt` se mění na ikony,
   `English version` se přesouvá do spodní lišty patičky (aby nebyl ztracený mezi odkazy).

**Ověření:** na 6 stránkách (úvod CZ/EN, článek CZ/EN, hosting, 404) porovnám patičku před/po,
zkontroluji 4 nové odkazy (všechny vrací 200) a že ikony sedí na svá místa (klikací plocha ≥ 44 px).

---

## 2. Hlavní menu — prohození přepínače jazyka a tlačítka komunity

**Dnes (11 položek):** `… Blog | FAQ | SEO Test | Připojit se ke komunitě | EN | ☰`
→ přepínač EN je na konci a na menších šířkách se ztrácí.

**Po změně:** `… Blog | FAQ | SEO Test | EN | Připojit se ke komunitě | ☰`
- tlačítko „Připojit se ke komunitě“ → nový Discord `https://discord.gg/ysx9dbXpdD`
- prohození na **všech 78 stránkách** (CZ i EN, včetně 404/500)
- **ověření:** prohlížeč na šířkách 390 / 768 / 1024 / 1280 px — přepínač EN musí být vidět vždy
  (a v mobilním menu taky), nesmí přetéct hlavička.

---

## 3. Nadpisy — menší a vycentrované (články + 404/500)

Naměřeno dnes (okno 1280 px):

| Kde | Teď | Po změně |
|---|---|---|
| Článek — `h1` | **76,8 px**, zarovnaný vlevo | **~68 px** (max `4.25rem`), **vycentrovaný** |
| 404 / 500 — `h1` | **80 px** (natvrdo v HTML), už vycentrovaný | **68 px** (stejná hodnota jako články) |
| Podstránky (FAQ, hosting…) | 38,4 px | beze změny — už jsou menší |

U článku se vycentruje i podtitul (perex) a údaj o datu, aby blok nezačínal uprostřed.
Změna je v `assets/redesign/style.css` (+ inline styl v `404.html`, `500.html`) → **zvýší se verze
`style.css?v=` na všech stránkách**, jinak si prohlížeč drží starý soubor 7 dní.
**Ověření:** změřená velikost a zarovnání na PC (1280) i mobilu (390) u 3 článků a obou chybových stránek.

---

## 4. Smazat ukázku `/ukazka/`

- smazat složku `ukazka/` (byla jen pro porovnání efektů, `noindex`)
- z `robots.txt` odebrat řádek `Disallow: /ukazka/`
- **ověření:** `https://hermes-ai.cz/ukazka/` → 404, v sitemapě nikdy nebyla.

---

## 5. Staré adresy → skutečné 301 (místo přesměrování uvnitř stránky)

Místo 66 ručně psaných pravidel použiju **vzorová pravidla v nginx** (pokryjí i budoucí variace):

| Vzor | Přesměrování | Pokryje |
|---|---|---|
| `^/blog/([a-z0-9-]+)/$` | → `/blog/clanek/$1/` | 27 CZ článků |
| `^/en/blog/([a-z0-9-]+)/$` | → `/en/blog/clanek/$1/` | 27 EN článků |
| `^/blog/([a-z0-9-]+)\.html$` | → `/blog/clanek/$1/` | 27 starých `.html` adres CZ |
| `^/en/blog/([a-z0-9-]+)\.html$` | → `/en/blog/clanek/$1/` | 27 starých `.html` adres EN |
| `/blog/stranka-2/` a `-3` | → `/blog/stranka/2/` a `/3/` | staré stránkování |
| `/en/blog/page-2/` a `-3` | → `/en/blog/page/2/` a `/3/` | staré stránkování EN |
| `/dovednosti`, `/dovednosti.html` | → `/skills/` | starý název sekce |
| `*.html` u stránek (instalace, hosting, faq, EN varianty) | → verze s lomítkem | staré názvy souborů |

Po nasazení: **66 pomocných souborů s přesměrováním se smaže** (nahradí je nginx).
**Ověření:** projdu všech 58 dnešních 404 + 7 cest + vzorek `.html` adres a všechny musí dát
**301 → 200**; zkontroluji, že se nerozbila nová stránkování `/blog/stranka/2/` a `/en/blog/page/2/`.

---

## 6. Sitemap a IndexNow — kontrola + cron ve 04:00

**Kontrola (dnes):**

| Co | Stav |
|---|---|
| Sitemap | ✅ 76 adres = přesně 76 živých stránek (nic nechybí, nic navíc), platné XML, kanonická domána bez www, bez `.html` a bez adres bez lomítka |
| `lastmod` | ⚠️ všude **12. 10. 2026**, ale web se měnil 14.–15. 10. → zastaralé |
| IndexNow klíč v cronu | ✅ `hermes2026-1gtn3el9l463ok9n` (obsah souboru sedí) |
| Odesílání | ✅ log ukazuje `HTTP 200`, 76 adres, běží denně v **02:00** |
| `a1b2c3d4e5f6g7h8i9j0.txt` | ❌ **neplatný klíč** — soubor obsahuje cizí klíč `0mfvnl2zfudodj7ukynyq0oth56qwgm6`; nikde se nepoužívá |

**Změny:**
1. `lastmod` v sitemapě se bude brát **z data změny souboru** (skript), takže už nikdy nezastará ručně.
2. Smazat neplatný klíč `a1b2c3d4e5f6g7h8i9j0.txt`.
3. **Cron přepsat na 04:00** (`0 4 * * *`) a rozšířit: ověří sitemapu, odešle **všech 76 adres**
   do IndexNow, zapíše výsledek do `/var/log/hermes-sitemap.log`; když se něco pokazí (sitemapa
   neplatná, klíč nedostupný, HTTP chyba), zapíše to jako problém, ať je vidět selhání.
   *Poznámka:* Google už „ping sitemapy“ nepodporuje — bere si ji z `robots.txt`, což tam je ✅.
   Denní odeslání všech adres do IndexNow (Bing, Seznam, Yandex) je v pořádku.
4. **Ověření:** cron spustím ručně, zkontroluji log (HTTP 200 / 202) a že se v IndexNow nic nehlásí jako chyba.

---

## 7. Dokumentace po nasazení

- `README.md` — patička, menu, nové 301, cron 04:00, datum kontroly
- `redesing/OPRAVY-CELEHO-WEBU-2026-10-15.md` — bod 12 (staré adresy) na ✅, doplnit nový nález 58× 404
- `redesing/PLAN-UPRAVY-2026-10-15.md` (zvlášť) + stavová hlavička
- skill `hermes-community-website` — nový Discord, vzorová pravidla 301, cron, ikony v patičce
- paměť — nový Discord odkaz (dnes je tam starý `VZpfgrCre`)

---

## Rozhodnutí, která potřebuji

1. **Minecraft List** — odkazovat na `minecraftlist.cz` (CZ/SK) nebo na `minecraftlist.eu` (EN/DE)? Navrhuji `.cz`.
2. **U článků vycentrovat jen nadpis, nebo celý blok** (nadpis + perex + datum)? Navrhuji celý blok.
3. **Velikost nadpisu článku** — navrhuji 68 px (z dnešních 76,8; chybové stránky stejně, z 80).
4. **Smazat těch 66 pomocných souborů** po nasazení 301? Navrhuji ano (jsou i v historii gitu).

## Pořadí prací (jeden restart nginx, jeden commit)

1. bod 6 (cron + úklid klíče) — nezávislé
2. bod 3 + 5 (CSS, nginx 301) — jeden reload nginx a zvýšení verze CSS
3. bod 1 + 2 + 4 (patička, menu, ukázka) — hromadné úpravy 78 stránek
4. ověření všeho (prohlížeč + `curl` na PC i mobilu)
5. dokumentace, commit a push
