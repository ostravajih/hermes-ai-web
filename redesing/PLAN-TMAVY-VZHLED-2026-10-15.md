# Plán: úplné zrušení světlého režimu (web bude vždy tmavý)

Vytvořeno 15. 10. 2026 · podklad: přesné zmapování kódu (viz tabulky níže)
Stav: **PROVEDENO 15. 10. 2026** — všechny fáze hotové a ověřené měřením (viz `OPRAVY-CELEHO-WEBU-2026-10-15.md`, sekce 1.9).
Počty stránek v tabulkách („78 stránek“) jsou stav **v době provedení**; dnes má web 130 stránek (ověřeno 17. 10. 2026).
Zvolená varianta: **A** (atribut `data-theme="dark"` na `<html>` zůstal, zmizelo všechno světlé).

---

## 0. Co jsem zjistil (proč to jde a co je potřeba vzít s sebou)

Světlý režim není jen „jedno tlačítko". Je provázaný na **9 místech**:

| Kde | Co tam je | Počet |
|---|---|---|
| `assets/redesign/style.css` | 13 pravidel pro světlý režim (řádky 39–51, 82–83, 122, 139–140, 183, 306, 336–341, 348–350) | 1 soubor |
| HTML – tlačítko | `<button class="theme-toggle">☼ Světlý</button>` | **81 stránek** |
| HTML – logo | druhé (světlé) logo v hlavičce i patičce `<img class="logo-light">` | **78 stránek** × 2 |
| HTML – obrázky | páry `class="theme-dark"` / `class="theme-light"` u ilustrací | 6 stránek |
| HTML – hlavička | `data-theme="dark"`, inline skript načítající uložený režim, `color-scheme: dark light`, světlé barvy v inline stylech | **144 stránek** |
| JS | `toggleTheme()`, načtení uloženého režimu z prohlížeče, klonování tlačítka do mobilního menu | `assets/script.js` |
| Obrázky | 17 světlých souborů (světlé logo, světlé ilustrace, světlá vlna v patičce, světlé pozadí hero) | 17 souborů / ~590 KB |
| Nepoužívaný soubor | `assets/redesign/theme-toggle.js` (nikde se nenačítá) | 1 soubor |
| Dokumentace | zmínky o přepínání režimu | README + redesing/*.md |

**Klíčové zjištění pro bezpečnost opravy:** v CSS jsou 4 pravidla se selektorem `html[data-theme] …`
(řádky 504–505, 593–594), která drží tmavou vrstvu v horní sekci. Kdybych z HTML odstranil atribut
`data-theme` a tato pravidla nechal, horní sekce by se rozbila (vrátil by se světlý pruh, který jsme
opravovali). Proto se ošetří zvlášť.

---

## 1. Rozhodnutí, které potřebuju potvrdit

**Varianta A (doporučená, bez rizika):** atribut `data-theme="dark"` na `<html>` **zůstane**
(není to „světlý prvek", jen jasné označení, že web je tmavý), ale **všechno světlé zmizí** —
pravidla, tlačítko, světlé obrázky, loga i skript.

**Varianta B (důkladnější):** zmizí i atribut `data-theme` → v HTML bude jen `<html lang="cs">`.
Vyžaduje přepsat ta 4 pravidla `html[data-theme] …` na `.hero.hero--poster::before` (jinak by se
rozbila horní sekce). O pár řádků čistší, ale dotýká se to znovu horní sekce, kterou jsme pracně
srovnali.

Doporučuju **A** — výsledek je pro návštěvníka naprosto stejný (tmavý web bez přepínače) a nehrozí
regrese. Bod 4 níže pak popisuju jako volitelný.

---

## 2. Fáze 1 — úklid CSS (`assets/redesign/style.css`)

1. **Smazat** blok `[data-theme="light"] { … }` (řádky 39–51) — světlé barvy pozadí, textů, rámů, stínů.
2. **Sloučit** `:root, [data-theme="dark"] { … }` do jediného `:root { … }` (řádky 8–38) — barvy přestanou
   záviset na atributu a platí vždy. `color-scheme: dark` zůstane.
3. **Smazat** světlé varianty:
   - ř. 82–83 — přepínání světlého loga v hlavičce,
   - ř. 122 — světlé pozadí horní sekce (`hero-background-light.webp`),
   - ř. 139–140 — `.theme-light` / `.theme-dark` u ilustrací,
   - ř. 183 — světlá vlna v patičce (`footer-wave-light.svg`),
   - ř. 306 — barva ozdoby v horní sekci pro světlý režim,
   - ř. 336–341 — světlá varianta obrázku v horní sekci,
   - ř. 348–350 — `img.theme-dark` / `img.theme-light`.
4. **Ponechat a zkontrolovat** ř. 504–505 a 593–594 (`html[data-theme] … ::before`) — u varianty A
   fungují dál, u varianty B je přepsat.
5. Zkontrolovat, že v CSS nezůstane ani slovo `light` (kromě názvů souborů, které se smažou) —
   ověřím strojově: `grep -i light style.css` musí vrátit 0 řádků (u varianty B i 0 výskytů `data-theme`).

## 3. Fáze 2 — úklid HTML (78 živých stránek + 404 a 500)

Provedu skriptem přes všechny stránky, aby byl výsledek všude stejný:

1. **Smazat tlačítko přepínání režimu** (`<button class="theme-toggle">…</button>`) — 81 stránek
   (hlavička na počítači i klon v mobilním menu, ten se přestane vytvářet v JS).
2. **Smazat světlé logo** `<img class="logo-light" …>` v hlavičce i patičce (78 × 2) — zůstane jen tmavé.
3. **Odstranit párové obrázky**: tam, kde je dvojice `theme-dark` / `theme-light`, zůstane jen ta tmavá
   varianta a její pomocná třída se odstraní (6 stránek: úvod CZ + EN, stránky blogu 2 a 3 v obou jazycích).
4. **Hlavička stránky**:
   - inline skript načítající uložený režim → **nahradit jedním řádkem, který uloženou volbu z prohlížeče
     smaže** (`localStorage.removeItem('theme')`) — aby lidem, kteří si světlý režim kdysi zapnuli,
     nezůstala v prohlížeči hodnota, která už nic neznamená,
   - inline styly: místo dvou režimů zůstane **jen tmavá barva** + `color-scheme: dark`,
   - `<meta name="color-scheme" content="dark light">` → `content="dark"`,
   - **přidat** `<meta name="theme-color" content="#061020">` (na mobilu se podle něj barví horní lišta
     prohlížeče — dřív chybělo, mohlo to přispívat k „blikání" na mobilu),
   - `<html lang="cs" data-theme="dark">` → u varianty B jen `<html lang="cs">`.

## 4. Fáze 3 — úklid JS (`assets/script.js`)

1. Smazat funkci `toggleTheme()` (ř. 108–127) a blok „Load saved theme" (ř. 128+).
2. Smazat klonování tlačítka režimu do mobilního menu (ř. 85, 97–101) — tlačítko už neexistuje.
3. Zkontrolovat, že skript po úpravě projde kontrolou syntaxe (`node --check`) a přepínač jazyka funguje.

## 5. Fáze 4 — smazání nepotřebných souborů (až po ověření, že na ně nic neodkazuje)

| Soubor | Velikost |
|---|---|
| `images/hero/hero-ai-agent-light.webp` | 78 KB |
| `images/sections/blog-documentation-light.webp` | 75 KB |
| `images/sections/features-tools-automation-light.webp` | 74 KB |
| `images/hero/hero-background-light.webp` | 69 KB |
| `images/sections/installation-terminal-light.webp` | 54 KB |
| `images/sections/agent-profile-light.webp` | 51 KB |
| `images/sections/security-community-light.webp` | 39 KB |
| `images/sections/agent-profile-dark-light.webp` | 25 KB |
| `images/sections/skills-mcp-light.webp` | 22 KB |
| `images/sections/hosting-light.webp`, `installation-light.webp`, `community-light.webp` | 50 KB |
| `logos/hermes-ai-logo-light.svg`, `hermes-ai-logo-mono-light.svg`, `hermes-ai-app-icon-light.svg`, `favicon-light.ico` | 5 KB |
| `images/footer/footer-wave-light.svg` | 0,6 KB |
| `assets/redesign/theme-toggle.js` (nikde se nenačítá) | 1,5 KB |
| **celkem** | **~590 KB** |

Postup: nejdřív ověřím, že na každý soubor vede **0 odkazů** v živých stránkách i v CSS, a teprve pak mažu.
(Soubory zůstávají v záloze ve `redesing/`, takže je lze kdykoli vrátit.)

## 6. Fáze 5 — ověření, že web opravdu nikde nesvítí bíle (měřením, ne dojmem)

Tohle je nejdůležitější část, protože dosud se blikání nedařilo spolehlivě reprodukovat.

1. **Test prvního vykreslení bez stylů** (simulace pomalé sítě): prohlížeči zablokuju `style.css`
   a změním 10 různých stránek (úvod, článek CZ, článek EN, seznam blogu, instalace, hosting, komunita,
   EN úvod, 404, stránka s obrázkem v článku). Snímám první snímky a měřím podíl bílých ploch.
   **Kritérium: 0 % bílých ploch na všech 10 stránkách.**
2. **Test přechodu z menu** na stejných 10 stránkách se **vypnutou keší a zpomalenou sítí**:
   snímám celý přechod a hledám jakoukoli náhlou změnu jasu. **Kritérium: žádný snímek, který by
   se od sousedního lišil o víc než malou toleranci.**
3. **Test načítání obrázků horní sekce** (nejpravděpodobnější zbývající příčina „probliknutí"):
   změřím průměrnou barvu horní sekce **před** načtením obrázku a **po** něm. Pokud je rozdíl velký
   (obrázek „skočí" jinou barvou), doladím: barvu podkladu sekce nastavím na převažující barvu obrázku
   a obrázek dám načítat přednostně (`preload`), aby se vykreslil společně se stránkou.
4. **Kontrola zbytků**: `grep -i 'light'` v CSS = 0, `grep 'data-theme="light"'` v celém webu = 0,
   `grep 'theme-toggle'` = 0, žádná stránka neodkazuje smazaný soubor.
5. **Kontrola webu jako celku**: všech 76 adres ze sitemapy vrací 200, žádný rozbitý obrázek,
   žádná chyba v konzoli, horní sekce mají dál stejnou výšku (500/460/480 px).
6. **Kontrola kontrastu textů** v tmavém režimu na 10 stránkách (světlý režim dřív mohl maskovat
   nečitelné místo — teď bude jediný režim, tak ať je v pořádku).

## 7. Fáze 6 — dokumentace

- `README.md` a `redesing/OPRAVY-CELEHO-WEBU-2026-10-15.md`: doplnit, že web je odteď jen tmavý
  a proč (světlé pozadí + obrázky = špatný kontrast, navíc zdroj problikávání).
- Poučení do skillu (aby se světlý režim nevrátil při další práci): tmavý režim je jediný,
  nové prvky nedělat s druhou barvou.

## 8. Co dělat, kdyby blikání po zrušení světlého režimu zůstalo

Světlý režim je hlavní podezřelý, ale ne jediný — v plánu proto měřím i **načítání obrázků** (bod 6.3).
Kdyby bliklo i potom, zbývají tyto možnosti (v tomto pořadí):
1. dorovnat podklad horní sekce s barvou obrázku + přednostní načtení obrázku (bod 6.3),
2. přidat jemné prolínání při přechodu mezi stránkami (prohlížeč sám spojí obě stránky plynulým
   prolnutím místo ostrého přepnutí) — podporují ho moderní Chrome/Edge/Safari, ostatní to ignorují,
3. dohledat konkrétní stránky, kde to dělá, a změřit je samostatně (potřeboval bych od vás vědět,
   na kterých stránkách to vidíte nejčastěji).

## 9. Rizika a jak je ošetřím

| Riziko | Ošetření |
|---|---|
| Rozbití tmavé vrstvy v horní sekci (4 pravidla `html[data-theme]`) | varianta A atribut ponechává; u varianty B se pravidla přepíšou a hned změří |
| Lidé s uloženou volbou „světlý" v prohlížeči | skript uloženou volbu smaže; světlé barvy v CSS po úpravě neexistují |
| Stránka zapomene odkaz na smazaný obrázek | před smazáním ověřím 0 odkazů, po smazání projdu všech 76 adres + kontrolu rozbitých obrázků |
| Keš prohlížeče (CSS/JS 7 dní) | u obou souborů zvýším verzi v odkazu (`?v=…`), aby si každý stáhl novou |
| Ztráta světlé varianty, kdyby ji někdo chtěl zpět | soubory i pravidla zůstanou v záloze ve `redesing/` a v git historii |

## 10. Odhad práce

Fáze 1–3 (kód) dohromady cca 30–45 minut, fáze 4 (soubory) 10 minut, fáze 5 (měření a doladění)
30–60 minut podle toho, co se najde, fáze 6 (dokumentace) 15 minut. **Celkem cca 1,5–2 hodiny**,
vše najednou, bez nutnosti dalšího zásahu z vaší strany.
