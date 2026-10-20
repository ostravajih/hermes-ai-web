# Plán: propojení hermes-ai.cz, multibrains.eu a Matomo (21. 10. 2026)

Cíl: tři weby se chovají jako jedna firma — obsahově, odkazy i měřením.

---

## Zjištěný stav (ověřeno)

| Co | Stav |
| --- | --- |
| `hermes-ai.cz/hosting/` | statické HTML, 100 % Contabo (affiliate odkazy `jdoqocy.com`, pixel `ftjcfx.com`), žádná zmínka o MultiBrains; verze i `/en/hosting/` |
| Patička hermes-ai.cz | sekce **Naše Projekty** už odkazuje na `multibrains.eu` a `seotestzdarma.cz` |
| Patička multibrains.eu | skupina **Firma** má jen O nás a Kontakt (`src/content/marketing.ts` → `FOOTER`) |
| Matomo na VPS2 | `matomo.sipkyliga.cz`, weby 1 SipkyLiga, 2 Hermes AI, 3 MinecraftList.cz, 4 MinecraftList.eu — **multibrains chybí** |
| Matomo na hermes-ai.cz | vlastní `/assets/matomo.js`, **bez cookies** (`disableCookies`), site 2, + serverový sběr AI botů |
| multibrains.eu | Next.js, cookie lišta s volbou analytics, GA4 se načítá až po souhlasu; Matomo nikde; CSP není, takže skript projde |
| Operátor | ani jeden web neuvádí IČO (`CONTACT.ico` je prázdné) |

---

## 1. hermes-ai.cz/hosting/ — přidat MultiBrains, Contabo zachovat

**Kde:** `/var/www/hermesagent/hosting/index.html` a `/var/www/hermesagent/en/hosting/index.html` (statické, ručně udržované, žádný generátor).

**Co přidat** — nová sekce `#managed-hosting` až za blokem „Jaký VPS pro Hermes Agent?“ a před závěrečné CTA:

1. Nadpis: **„Nechcete server spravovat? Použijte hotový Hermes Agent hosting“**
2. Tři karty tarifů (Free 7 dní zdarma / Start 99 Kč / Pro 249 Kč) — pouze orientačně, celý ceník na multibrains.eu.
3. Co je v ceně: agent do 2 minut, dashboard, SSH, zálohy a klony, crony a webhooky, API klíče, vlastní klíč k modelu (BYOK), vlastní doména (Business).
4. Srovnávací tabulka **VPS u Contabo vs. MultiBrains**:

| | Contabo VPS | MultiBrains |
| --- | --- | --- |
| Koho to je | chcete root a plnou kontrolu | chcete hotového agenta |
| Instalace | sám podle návodu (5–15 min) | 2 minuty, hotovo |
| Údržba, aktualizace, zálohy | sám | my |
| Cena | od 4,40 €/měsíc + vaše práce | od 99 Kč/měsíc |

5. CTA `https://multibrains.eu/cenik?utm_source=hermes-ai&utm_medium=hosting` s textem „Prohlédnout hosting →“.
6. Transparentnost: „MultiBrains je náš vlastní produkt — stejný provozovatel jako tento web.“ (u affiliate stránky je to nutné i kvůli důvěře.)

**Úpravy SEO:** title a description na „VPS pro AI agenty — Contabo, nebo hotový Hermes Agent hosting“; H1 zůstává. Contabo odkazy zůstávají beze změny (`rel="nofollow sponsored"`).

**Proč to neškodí Contabu:** sekce je až za vysvětlením, jaký VPS vybrat; kdo chce root, jde dál na Contabo. Kdo nechce řešit server, dostane alternativu místo odchodu na konkurenční návod.

---

## 2. multibrains.eu — patička a odkazy na sesterské weby

**Soubor:** `src/content/marketing.ts` (data) + `src/components/marketing/SiteFooter.tsx` (render).

1. Do skupiny **Firma** přidat:
   - `Hermes AI` → `https://hermes-ai.cz`
   - `Seo Test` → `https://www.seotestzdarma.cz`
2. Patička dnes používá `next/link` i pro externí adresy — doplnit pole `external: true` a vykreslit `<a target="_blank" rel="noopener">` (bez `nofollow`, aby odkaz byl opravdový backlink).
3. **Kontextové odkazy** navíc na `/o-nas`: jedna věta „Provozujeme také **Hermes AI** (návody a wiki k agentovi) a **Seo Test** (audit webu zdarma)“ s odkazy. Odkaz v textu má větší váhu než v patičce a lépe vysvětluje vztah.
4. Stejná věta (jen obráceně) už na hermes-ai.cz existuje v „Naše Projekty“ → vzniká obousměrné propojení, ne jednosměrná farma odkazů.

**Návrh textu patičky (Firma):** O nás · Kontakt · Hermes AI · Seo Test.
Do hlavičky nic nepřidávat, aby se nerozbila navigace na mobilu.

---

## 3. Matomo pro multibrains.eu

### 3.1 Založení webu

Přes API na VPS2 (`/root/.matomo-api-token`, stejný postup jako `matomo-add-site.sh`):

- název: `MultiBrains`
- adresy: `https://multibrains.eu`, `https://www.multibrains.eu`
- timezone `Europe/Prague`, měna `CZK`, skupina `MultiBrains`
- siteSearch: vypnuto (fulltext na webu není), ecommerce: vypnuto

Výsledek: `idsite` (očekávám 5) — uloží se do konfigurace webu.

### 3.2 Měřící kód

Vzor vezmu z hermes-ai.cz, protože je ověřený v provozu:

- `public/matomo.js` — vlastní soubor, `setSiteId(<nové>)`, `setTrackerUrl https://matomo.sipkyliga.cz/matomo.php`
- **`disableCookies`** → žádná cookie, žádná změna cookie lišty, žádný souhlas navíc; Matomo počítá návštěvu přes denní otisk
- `enableHeartBeatTimer(15)`, `enableJSErrorTracking`, `enableLinkTracking`
- vložení v `src/app/(marketing)/layout.tsx` přes `next/script` (`strategy="afterInteractive"`), aby se nenačítal v dashboardu ani administraci

**Rozhodnutí k potvrzení:** měřit jen veřejný web (marketing, dokumentace, blog), nebo i dashboard? Doporučuji **jen veřejný web** — dashboard je přihlášený a do Matomy by tekla jména stránek agentů.

### 3.3 Ověření

- `curl` na `matomo.php` → 204/200, `matomo.js` → 200
- návštěva v prohlížeči → v Matomě `VisitsSummary.get` do 1 minuty vidí 1 návštěvu a pageview
- `document.cookie` po načtení prázdné (důkaz bez cookies)
- kontrola, že se skript nenačítá na `/dashboard` a `/admin`

### 3.4 Volitelně (později)

Serverový sběr AI botů (ChatGPT-User, Claude-User, Perplexity-User) jako na hermes-ai.cz — nginx + malá služba. Není součástí tohoto plánu, ale je to stejná infrastruktura.

---

## 4. Pořadí a odhad

| # | Krok | Čas |
| --- | --- | --- |
| 1 | Matomo: založit web, měřicí kód, ověřit návštěvu | 30 min |
| 2 | Patička multibrains + kontextové odkazy na /o-nas | 30 min |
| 3 | Sekce na /hosting/ (CS + EN), title/description | 60 min |
| 4 | Ověření: odkazy obousměrně, mobil 390 px, sitemap, IndexNow | 20 min |

Nasazení: multibrains vyžaduje build + restart (jeden restart), hermes-ai.cz je statické (bez restartu).

---

## 5. Rizika a jak je hlídat

- **Kanibalizace klíčových slov** — hermes-ai.cz cílí „VPS pro AI agenty / Contabo“, multibrains „Hermes Agent hosting“. V H1 a popiscích se nesmí objevit stejná fráze; odkazy mají různý anchor text.
- **Affiliate etika** — na stránce s affiliate odkazy musí být vidět, že MultiBrains je náš produkt. Doplněno v sekci.
- **Matomo bez cookies** — nesmí se změnit na cookie variantu, jinak je potřeba nový souhlas v liště.
- **Výkon** — skript `defer`/`afterInteractive`, žádný blokující request.

---

## 6. Co potřebuji od vás (rozhodnout před spuštěním)

1. **Operátor:** ani jeden web neuvádí IČO. Aby to vypadalo jako jedna firma i právně, doplnit do patiček stejný údaj (jméno / firma, IČO, adresa)? Pokud IČO nechcete zveřejnit, necháme jen text „stejný provozovatel“.
2. **Ceny na /hosting/:** ukázat konkrétní tarify (99/249/690 Kč), nebo jen „od 99 Kč“ s odkazem na ceník?
3. **Matomo:** měřit jen veřejný web (doporučuji), nebo i dashboard?
4. **Název odkazu v patičce:** `Hermes AI` a `Seo Test` (jak píšete), nebo `Hermes AI — návody` a `SEO test zdarma`?
