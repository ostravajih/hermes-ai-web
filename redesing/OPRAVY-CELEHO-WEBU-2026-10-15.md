# Opravy celého webu hermes-ai.cz — vysvětlení a plán
Vytvořeno 15. 10. 2026. Navazuje na `AUDIT-A-PLAN-OPRAV-2026-10-14.md` a `PLAN-OPRAV-2-HERO-A-CELY-WEB.md`.

---

## 1. Co je hotové (✅)

### 1.1 Hero sekce = „plakát" na všech hlavních stránkách

Dřív byl obrázek **vložený jako obrázek v rámečku** (vlastní sloupec, zaoblené rohy, okolo něj viditelné pozadí).
Teď je obrázek **celé pozadí sekce** (od kraje ke kraji, shora dolů) a text (nadpis, popis, tlačítka) leží **jako vrstva nad ním** — stejně jako je to v sekci „Rychlý start" na úvodu.

Přechod do další sekce: obrázek se **plynule rozplyne** do barvy pozadí (vrstva `mask-image` + ztmavovací gradient), takže mezi sekcemi **není ostrá hrana**.

**Přepsané stránky (15) a použitý obrázek:**

| Stránka | Obrázek na počítači (1920×700) | Obrázek na mobilu (768×960) |
|---|---|---|
| Úvod `/` a `/en/` | `hero/hero-ai-agent-approved.webp` | `hero/hero-ai-agent-approved_mobile_768x960.webp` |
| Instalace `/instalace/`, `/en/installation/` | `sections/installation-hero.webp` | `sections/installation-hero_mobile_768x960.webp` |
| Hosting `/hosting/`, `/en/hosting/` | `sections/hosting-hero.webp` | `sections/hosting-hero_mobile_768x960.webp` |
| Skills `/skills/`, `/en/skills/` | `sections/skills-hero.webp` | `sections/skills-hero_mobile_768x960.webp` |
| FAQ `/faq/`, `/en/faq/` | `sections/faq-hero.webp` | `sections/faq-hero_mobile_768x960.webp` |
| Blog `/blog/`, `/en/blog/` | `sections/blog-hero.webp` | `sections/blog-hero_mobile_768x960.webp` |
| Co je Hermes `/co-je-hermes/` | `sections/co-je-hermes-hero.webp` (nově vygenerováno) | `sections/co-je-hermes-hero_mobile_768x960.webp` |
| Funkce `/funkce/` | `sections/funkce-hero.webp` (nově vygenerováno) | `sections/funkce-hero_mobile_768x960.webp` |
| Komunita `/komunita/` | `sections/community.webp` (1600×900) | `sections/community_mobile_768x960.webp` |

Poznámky:
- **Mobilní obrázky se načítají automaticky** — stránka má dvě varianty obrázku (`<picture><source media="(max-width: 820px)">`), telefon si vezme svislou 768×960, počítač širokou 1920×700. Nemusí se nic přepínat ručně.
- Na úvodu a v sekci Česká komunita se nyní používá **stejný obrázek v tmavém i světlém režimu** (dřív světlý režim ukazoval jiný obrázek `community-light.webp` — to bylo nekonzistentní).
- Sekce „Česká komunita" na úvodu používá `hermes_agent_community_hero_1600x900` — beze změny, teď i jako pozadí hero na stránce `/komunita/` a na mobilu ve výřezu 768×960.

### 1.2 Staženo z plánu 1 (hotové dřív)

- ✅ Certifikát pro `www.hermes-ai.cz` doplněn (platnost do 12. 1. 2027), `www` → `hermes-ai.cz` přesměrování 301 funguje i přes IPv6.
- ✅ Obnovy certifikátů ověřeny simulací (`certbot renew --dry-run`) — všech 19 certifikátů v pořádku.
- ✅ Nasazeny chybějící mobilní obrázky pro všechny hero sekce.

---

### 1.3 Oprava hero sekcí po vaší kontrole (15. 10. 2026)

Po vaší poznámce „v hero sekcích jsou chyby a celé hero sekce zbytečně velké" jsem prošel
všechny hero sekce v prohlížeči (15 stránek × 4 šířky okna) a našel pět skutečných chyb:

| Chyba | Jak se projevovala | Oprava |
|---|---|---|
| Zůstala stará dvousloupcová mřížka | Nadpis a popis byly posunuté **doprostřed** (na počítači začínaly na 600 px místo 24 px) a přes světlou část obrázku | Mřížka zrušena, obrázek je mimo tok dokumentu, text začíná na stejném místě jako zbytek stránky (24 px na počítači, 16 px na mobilu) |
| Pevná výška 560 px bez ohledu na obsah | Podstránky měly 152–198 px prázdného místa nad i pod textem | Výška vychází z obsahu (odsazení 32–44 px) |
| Na mobilu nebyl obrázek vidět | Sekce byla vysoká jen 209 px, z obrázku zbyl tmavý pruh | Na mobilu má sekce minimálně 300 px (do 400 px na tabletu), obrázek se ukazuje nad textem |
| Úvodní obrázek měl uříznutou hlavu | Operátorce chybělo temeno hlavy (výřez byl posunutý dolů) | Výřez posunut nahoru, hlava je celá |
| CSS se drželo v keši 7 dní | Změny se nemusely načíst | Odkazy mají verzi (`style.css?v=20261015-4`) |

**Změřené výšky hero sekcí (po opravě):**

| Šířka okna | Podstránky | Úvodní stránka |
|---|---|---|
| Počítač 1280 px | 189–277 px (dřív 560 px) | 501 px |
| Notebook 1440 px | 204–290 px | 529 px |
| Tablet 800 px | 400–420 px | 454 px |
| Mobil 390 px | 300–310 px (dřív 523 px) | 482 px (dřív 600 px) |

Kontrola: 60 měření (15 stránek × 4 šířky) — obrázek kryje celou sekci, text leží nad obrázkem,
text ze sekce nepřetéká, žádné vodorovné přetečení, žádný rozbitý obrázek, správný obrázek podle šířky okna.

### 1.4 Věc k rozhodnutí u obrázku Instalace (💡)

Obrázek na stránce Instalace má **vypálené příkazy** (např. `git clone https://github.com/hermes-ai/hermes`,
`pip install -r requirements.txt`). Ty **neodpovídají skutečnému postupu** na stránce
(správně je `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`).
V hero velikosti je text drobný, ale kdo si obrázek otevře nebo má velký monitor, uvidí nesprávné příkazy.
Doporučuji obrázek vyměnit za variantu bez textu (nebo použít novější sadu `Hermes_Instalace_Operatorka_v2`).

### 1.5 Druhá oprava hero — pruh, stejná výška, text (15. 10. 2026)

Podle vašeho screenshotu (světlý režim) jsem našel a opravil další tři věci:

| Problém | Příčina (změřeno) | Oprava |
|---|---|---|
| **Světlý pruh v hero** | Vrstva, která měla ztmavovat spodní okraj, se kvůli starému pravidlu `inset: 0` kreslila **nahoře** a končila barvou pozadí → ve světlém režimu světlá páska s ostrou hranou (jas 69 → 193, hrana se skokem 177 z 255) | Svislá vrstva zrušena (rozplynutí řeší maska obrázku), pozadí hero natrvalo tmavé `#07111F` |
| **Světlý režim navíc** | Po zrušení mé vrstvy se vrátilo staré pravidlo `.route-hero::after`, které přes hero kreslilo **světlý přechod barvou pozadí** (naměřeno: celý hero jas ~150) | Pravidlo pro plakát vypnuto — světlý i tmavý režim teď mají **shodný jas** |
| **Nestejná výška** | Výška vycházela z množství textu: úvod 501 px, ostatní 189–277 px | Výška pevná pro všechny: **500 px** počítač, **460 px** tablet, **480 px** mobil |
| **Text moc vlevo a statistiky vlevo** | Text začínal na 24 px a byl úzký (620 px), statistiky byly v bloku zarovnaném vlevo | Text posunutý o 51 px od okraje a širší (760 px), statistiky **vycentrované** na střed sekce |

Ověření: 90 měření (15 stránek × 6 šířek okna) — všechny hero sekce mají přesně 500/460/480 px,
obrázek kryje celou sekci, text ze sekce nepřetéká, 0 px přetečení, 0 rozbitých obrázků.
Kontrola pixelů: v hero už není žádná umělá vodorovná hrana (dřívější skok 177 z 255 zmizel).


### 1.6 Třetí kolo oprav (15. 10. 2026, večer)

| Co | Příčina (změřeno) | Oprava | Ověření |
|---|---|---|---|
| **Web při přepínání stránek z menu „problikne"** | Téma (světlý/tmavý režim) se nastavovalo až po načtení stránky — v HTML je natvrdo tmavé, takže se světlý režim přepnul, až když se stránka vykreslila (viditelné bliknutí tmavě → světle) | Do hlavičky všech **141 stránek** přidán drobný skript, který se spustí **před** vykreslením | I s vypnutým `script.js` je hned po načtení HTML správné téma (světlý režim světlý, tmavý tmavý) — bliknutí nemůže nastat |
| **Přepínač jazyka vedl na 404** | Adresy článků se v obou jazycích jmenují jinak; skript jen přidal `/en` před českou adresu | Do skriptu doplněna tabulka **27 párů článků** i stránek (`/instalace/` ↔ `/en/installation/` atd.); neznámá adresa teď vede na přehled blogu, ne na chybu | 13/13 testovaných přepnutí v prohlížeči vede na existující stránku |
| **Na úvodní stránce přepínač „nic nedělal"** | Úvodní adresa `/` slouží oběma jazykům podle cookie, takže adresa před i po přepnutí byla stejná → stránka se znovu nenačetla | Volba jazyka má na serveru **přednost před jazykem prohlížeče** + skript při stejné adrese stránku znovu načte | Přepnutí CZ ↔ EN na úvodu funguje oběma směry |
| **Chybějící anglické stránky** | `/co-je-hermes/`, `/funkce/`, `/komunita/` neměly EN verzi | Vytvořeny `/en/what-is-hermes/`, `/en/features/`, `/en/community/` (překlad českých předloh) | 3× HTTP 200, doplněny do sitemapy (76 adres) a odeslány IndexNow |
| **Všechny články měly stejný náhledový obrázek** | 54 článků odkazovalo na jeden obrázek | Vygenerováno **27 obrázků** (jeden pro CZ+EN verzi téhož článku, 1920×700 + mobil 768×960) a vloženy do textu + do náhledu pro sítě | 54 stránek: obrázek se načítá (1920×700), 0 přetečení; všech 27 obrázků zkontrolováno očima — sedí k tématu a neobsahují text |
| **Obrázek na Instalaci měl chybné příkazy** | Do obrázku byly vypálené příkazy, které neodpovídají návodu | Nahrazen novým obrázkem bez textu (šipka stahování do notebooku), u odkazů zvýšena verze, aby se neukazovala stará verze z cache | Ověřeno v prohlížeči (1920×700, žádný text v obrázku) |
| **E-maily z `@hermes-ai.cz`** | Chybí SPF a DMARC (DKIM existuje) | Návod s přesnými záznamy: `redesing/EMAILY-SPF-DKIM-DMARC.md` | Čeká na vložení do DNS (Wedos) — nemám k němu přístup |


### 1.7 Čtvrté kolo — blikání stránek: skutečná příčina (15. 10. 2026, noc)

Moje předchozí oprava (skript s tématem v hlavičce) problém **nevyřešila**, protože příčina byla jiná.
Změřil jsem to tak, že jsem prohlížeči **zablokoval načtení `style.css`** a snímal, co vykresluje:

| Měření | Před opravou | Po opravě |
|---|---|---|
| První vykreslení v tmavém režimu | **99 % plochy bílé**, jas 254 | **0 % bílých ploch**, jas 24 |
| První vykreslení ve světlém režimu | bílá stránka bez stylů | světlé pozadí jako má web |

**Příčina:** Než dorazí CSS (je to velký soubor a drží se v keši), prohlížeč na okamžik vykreslí stránku
**bez stylů** — a ta má výchozí bílé pozadí. Proto to bliká i v tmavém režimu: bílý záblesk je vidět
nejvíc právě na tmavém webu. Moje první oprava řešila jen barvu režimu, ne tuhle bílou plochu.

**Oprava:** Do hlavičky **144 stránek** vložen malý kousek stylů přímo do HTML (před odkazem na hlavní CSS):
barva pozadí a textu pro oba režimy + `color-scheme`. Prohlížeč tak hned od prvního vykreslení ví,
že má kreslit tmavě (nebo světle) a bílá plocha nemůže vzniknout.

**Důkaz:** se zablokovaným CSS je první vykreslení tmavé (0 % bílých ploch) místo bílého (99 %).

### 1.8 Menu odkazuje na stránky (15. 10. 2026)

Stránky `/co-je-hermes/`, `/funkce/`, `/komunita/` (a jejich anglické verze) byly z menu nedostupné —
menu na ně posílalo jen na úseky úvodní stránky. Teď na ně odkazuje menu na **všech** stránkách:

| Česky | Anglicky |
|---|---|
| Co je Hermes → `/co-je-hermes/` | What is Hermes → `/en/what-is-hermes/` |
| Funkce → `/funkce/` | Features → `/en/features/` |
| **Komunita** → `/komunita/` (nová položka) | **Community** → `/en/community/` (nová položka) |

Ověřeno: všech 9 položek se vejde do menu na šířkách 1440–900 px (622 px z 1240 px v nejužším místě),
pod 900 px se menu schová do mobilního tlačítka; na mobilu i v angličtině mají položky správné názvy
a odkazy vracejí 200.


### 1.9 Světlý režim úplně zrušen — web je vždy tmavý (15. 10. 2026)

**Proč:** blikání se nedařilo spolehlivě odstranit a na světlém pozadí navíc špatně vynikaly
obrázky (jsou kreslené pro tmavý web) i kontrast písma. Rozhodnutí: světlý režim zrušit **úplně**,
aby nikde nezůstal žádný jeho prvek — v HTML, v CSS ani mezi soubory.

**Co bylo potřeba odstranit (světlý režim nebyl jen tlačítko):**

| Kde | Co tam bylo | Kolik |
|---|---|---|
| `assets/redesign/style.css` | 13 pravidel pro světlý režim | 1 soubor |
| HTML | tlačítko „Světlý/Tmavý" | 81 stránek |
| HTML | druhé (světlé) logo v hlavičce i patičce | 78 stránek (156×) |
| HTML | páry obrázků světlá/tmavá varianta | 6 stránek |
| HTML | skript načítající uložený režim + světlé barvy v hlavičce | 144 stránek |
| `assets/script.js` | funkce přepnutí režimu + načtení uložené volby | 1 soubor |
| soubory | 17 světlých obrázků/log + nepoužívaný `theme-toggle.js` (556 KB) | 18 souborů |

**Co se změnilo:**

- V CSS zmizela **všechna** světlá pravidla (kontrola: `grep -i light` = 0 výskytů) a tmavé barvy se
  sloučily do jediného místa (`:root`), takže platí vždy a nezávisle na čemkoli.
- Z hlavičky **144 stránek** zmizel skript, který načítal uložený režim; místo něj se uložená volba
  z prohlížeče **smaže** — kdo si kdysi světlý režim zapnul, nemá v prohlížeči mrtvou hodnotu.
- Do hlavičky přidáno `<meta name="theme-color" content="#061020">` — na mobilu se podle něj barví
  horní lišta prohlížeče (dřív chybělo, mohlo přispívat k „bliknutí" na mobilu).
- Atribut `data-theme="dark"` na `<html>` zůstal (drží tmavou vrstvu horní sekce) — jen říká „tmavý",
  žádný světlý prvek v sobě nemá.
- Smazané soubory jsou v záloze: `scratch/svetly-rezim-zaloha.tgz` (556 KB).
- Verze v odkazech zvýšeny na `style.css?v=20261015-11` a `script.js?v=redesign-4`, aby si prohlížeče
  nestahovaly staré soubory ze své keše.

**Ověřeno měřením (ne dojmem):**

| Test | Výsledek |
|---|---|
| První vykreslení se zablokovaným CSS (11 různých stránek) | **0 % bílých ploch na 11 z 11** |
| Přechod z menu se vypnutou keší a zpomalenou sítí (4 dvojice stránek) | největší změna jasu **3–8** z 255, **0 % bílých ploch** |
| Obrázek horní sekce, než dorazí (3 stránky) | jen nepatrná změna odstínu (řádově 14 z 255), žádný záblesk |
| Zbytky světlého režimu v HTML/CSS/JS | **0** (tlačítko, světlé logo, světlé obrázky, světlé barvy) |
| Adresy ze sitemapy | **76 z 76** vrací 200, žádný rozbitý obrázek |
| Výška horní sekce na podstránkách | **500 px** (beze změny) |
| Mobil (390 px) | menu má 9 položek + přepínač jazyka, přepínač režimu 0× |

**Vedlejší nález při úklidu:** při mazání pravidel pro tlačítko režimu jsem omylem smazal i části
pravidel, které platily společně pro přepínač jazyka (`.lang-switch`) — odhaleno hned kontrolou
v prohlížeči a vráceno zpět (přepínač jazyka má znovu rámeček, odsazení i správné chování na mobilu).



### 1.10 Problikávání — skutečná příčina: fonty (15. 10. 2026)

Po zrušení světlého režimu uživatel upřesnil: **„když stránku obnovím CTRL+F5, tak blikají všechny"**.
To byla stopa — tvrdé obnovení znovu stahuje i soubory, které si prohlížeč normálně drží v keši.

**Změřeno (tvrdé obnovení, vypnutá keš, zpomalená síť):**

| Soubor | Kdy začal | Kdy dorazil |
|---|---|---|
| `style.css` | 281 ms | 609 ms |
| obrázek horní sekce | 282 ms | 817 ms |
| **`Inter-400` … `Inter-800` (5 souborů)** | **641–690 ms** (až PO CSS) | **2 021–2 968 ms** |

Každý soubor písma měl **325 KB**, všech pět dohromady **1,6 MB**. Písmo se navíc nemohlo začít stahovat
dřív než s CSS (odkaz na něj je uvnitř CSS). Text se tedy nejdřív vykreslil náhradním písmem a teprve
po **2–3 sekundách** se přeskládal na Inter — což je přesně to „probliknutí": měřeno **6–14 % pixelů
stránky se změní**, když písmo dorazí. Při každém tvrdém obnovení se písma stahují znovu, proto to
dělalo na všech stránkách.

**Oprava:**

| Co | Před | Po |
|---|---|---|
| Písmo | 5 souborů × 325 KB = **1,6 MB** | 1 variabilní soubor se všemi tloušťkami = **50 KB** |
| Znaky v písmu | celý svět (cyrilice, řečtina, vietnamština…) | jen znaky, které web opravdu používá (346) |
| Načítání | až po CSS, 2–3 s | **přednostní (`preload`), hned s CSS** |
| Výměna písma | `swap` = písmo se vymění v zobrazené stránce | `optional` = **výměna uvnitř zobrazené stránky nemůže nastat** |
| Obrázek horní sekce | vykresloval se o snímek později (`decoding="async"`) | vykresluje se spolu se stránkou |

**Ověřeno:**

| Test | Výsledek |
|---|---|
| Písmo Inter aktivní (i s vypnutou keší) | ✅ na všech testovaných stránkách |
| Míry nadpisu v čase po vykreslení | **od 192 ms do 1 179 ms úplně stejné** (691 × 44 px, Inter) = text se nikdy nepřeskládá |
| Změna stránky po jejím vykreslení (9 stránek, tvrdé obnovení) | **✅ žádná** (dřív 6–14 % pixelů) |
| Adresy ze sitemapy | 76 z 76 vrací 200 |
| Česká diakritika (ě, š, č, ř, ž, í, á) | zobrazená správně, potvrzeno i pohledem na snímek |
| Velikost stránky | CSS 35 KB + písmo 50 KB + skript 6 KB (dřív **+1,6 MB** písma) |

**Proč to dřív nešlo najít:** první měření sledovalo jen **jas** stránky — výměna písma jas skoro nemění
(text zůstane světlý na tmavém), ale **změní tvar písmen**, takže se přeskládá celá stránka. Pomohlo až
měření **rozdílu pixelů mezi snímky** a přímé porovnání dvou snímků (s písmem / bez písma = 6–14 %).

**Past, na kterou jsem při tom narazil (a hned opravil):** horní sekce má obrázek ve dvou velikostech
(`<picture>` + `<source media="(max-width: 820px)">`). Když jsem přidal přednačtení obrázku s jedinou
adresou, **telefon stahoval oba obrázky** — velký i malý (u článku na blogu 239 KB úplně zbytečně).
Přednačtení proto musí být taky rozdělené podle šířky obrazovky:

```html
<link rel="preload" as="image" href="…-hero.webp" media="(min-width: 821px)" fetchpriority="high">
<link rel="preload" as="image" href="…_mobile_768x960.webp" media="(max-width: 820px)" fetchpriority="high">
```

Po opravě: telefon stahuje **jen malý obrázek** (39 KB místo 103 KB), počítač jen velký.
Stránka `/instalace/` tak váží 92 KB na telefonu a 117 KB na počítači.

**Poslední stav po všech opravách (měřeno):**

| Test | Výsledek |
|---|---|
| CSS i písmo dorazí | společně, 65–180 ms po HTML (dřív písmo 2–3 s) |
| Přeskládání obsahu po vykreslení (16 stránek, vymazaná keš) | žádné; největší rozdíl 4 px na šířce nadpisu v prvních ~100 ms (dřív celá stránka) |
| Telefon vs. počítač | každý stahuje správnou velikost obrázku |
| Váha stránky | 92 KB (telefon) / 117 KB (počítač) |


### 1.11 Oživení webu — šest živých efektů (15. 10. 2026, noc)

Web byl do té doby čistě statický. Majitel si v živé ukázce vybral **6 z 10 efektů**; nasazeny jsou
všechny najednou a ověřené v prohlížeči:

| # | Efekt | Kde |
|---|---|---|
| 1 | síť bodů, která se spojuje s kurzorem myši | horní sekce všech stránek |
| 2 | čísla ve statistikách se napočítají | horní sekce |
| 3 | světlo u kurzoru + jemné naklonění karet | karty článků, dlaždice, statistiky |
| 4 | terminál, který se sám napíše a pak ukáže výsledek (kliknutím znovu) | `/instalace/`, `/en/installation/` |

Soubor `assets/zive.js` (~13 KB, bez jakékoli knihovny) + sekce „Oživení webu“ na konci `style.css`.
Drží stejná pravidla jako oprava blikání (jen posuv a průhlednost, `defer`, pauza mimo obrazovku,
respektuje systémové „omezit pohyb“).

**Tentýž večer jsem na připomínky majitele tři efekty ubral** — byly to další vrstvy a blikání navíc:

| Ubrané | Důvod |
|---|---|
| tři barevné rozostřené plochy nad obrázkem v horní sekci | obrázek byl „jako v mlze“ |
| ztmavení přes obrázek (gradient kvůli čitelnosti) | totéž — web má vlastní ztmavení už předtím |
| prolití mezi stránkami (efekt 9) | při kliknutí na jinou stránku to blikalo |
| posun obrázku podle myši (efekt 10) | majitel zrušil |

Přes obrázek tak jde jediná vrstva — tenká síť bodů (horní sekce se s efekty liší jen v **0,8 %
pixelů**, dřív to byly desítky procent). Dvě chyby, které se přitom našly a opravily: na podstránkách
drželo konkrétnější CSS pravidlo nápisy **pod** efektovou vrstvou (nápisy vypadaly schované), a síť
se zjevovala naráz (teď se plynule prolne za 0,55 s).

**Ověřeno po opravě:** blikání se nevrátilo (6 stránek s vypnutou keší), v CSS nejsou žádná pravidla
pro prolití stránek, výšky horních sekcí beze změny (500 px / 480 px na telefonu), 0 px vodorovného
přetečení, žádné chyby v prohlížeči, 76/76 adres ze sitemapy vrací 200.

Podrobný popis, jak efekty vypnout nebo upravit: `redesing/OZIVENI-WEBU-2026-10-15.md`.

---

> **Co je to za dokument:** průběžný záznam oprav webu ze **15. 10. 2026** (kapitoly 1.1–1.11)
> a **seznam otevřených chyb se stavem** (kapitoly 3–7). Je to historie jednotlivých kroků, ne popis
> dnešního stavu — ten drží `README.md` v kořeni. Poslední kontrola proti kódu: 15. 10. 2026.

## 2. Jak hero teď funguje (vysvětlení „jak to vypadá")

Sekce má **tři vrstvy** nad sebou (stav 15. 10. 2026, po oživení webu):
1. **Spodní vrstva — obrázek** (`z-index: 1`). Je „přilepený" na celou sekci (`position: absolute; inset: 0`),
   roztahuje se přes celou šířku i výšku (`object-fit: cover`) a ve spodní části se rozplývá do pozadí (maska).
   Na ≤ 820 px se načítá svislá varianta `*_mobile_768x960`, nad tím široká `*_hero.webp`.
2. **Prostřední vrstva — ztmavení** (uvnitř obrázku, `::before`). Zleva doprava tmavý přechod
   (vlevo 93 % krytí, vpravo 0 %), aby byl text vlevo vždy čitelný. Zespodu další tmavý přechod
   pro plynulé napojení na další sekci.
3. **Svrchní vrstva — text** (`z-index: 3`). Nadpis, popis, tlačítka a statistiky. Text je **skutečný text**,
   ne vypálený v obrázku — je tedy čitelný pro vyhledávače i pro čtečky pro nevidomé.

Navíc je mezi obrázkem a textem **tenká síť bodů** (`assets/zive.js`, `z-index: 2`), která se spojuje
s kurzorem myši. Přes obrázek nesmí jít nic dalšího — 15. 10. 2026 se ukázalo, že barevné rozostřené
plochy a ztmavení navíc dělají z obrázku „mlhu" (viz 1.11).

Světlý režim už neexistuje (zrušen 15. 10. 2026) — web je vždy tmavý, text leží na tmavém obrázku.

**Výšky sekce (měřeno):** počítač 500 px, tablet 460 px, telefon 480 px.

---

## 3. Ověření (měřeno v prohlížeči, ne odhad)

| Co se měřilo | Výsledek |
|---|---|
| Obrázek přes celou sekci | 45/45 měření (15 stránek × 3 šířky) obrázek přesně kryje sekci |
| Správný obrázek podle šířky | na ≤ 820 px se načítá `*_mobile_768x960`, nad 820 px `*_hero.webp` |
| Text nad obrázkem | ano, ve všech 15 případech vrací prohlížeč pod kurzorem text, ne obrázek |
| Ostrá hrana dole | ne — 3 px nad hranou má barva hodnotu pozadí (skok 0–1/255) |
| Vodorovné přetečení | 0 px na všech stránkách a šířkách |
| Rozbité obrázky | 0 |
| Nevyvážené `<div>` v hero sekci | 0 (15/15 stránek vyváženo, starý „rámeček" odstraněn) |

---

## 4. Nalezené chyby (🔧) — se stavem k 15. 10. 2026

| # | Chyba | Stav |
|---|---|---|
| 1 | Přepínač jazyka EN/CS vedl na neexistující adresu | ✅ **opraveno** — přepínač má tabulku dvojic adres (13/13 kontrol prošlo) |
| 2 | 3 české stránky neměly anglickou verzi (`/co-je-hermes/`, `/funkce/`, `/komunita/`) | ✅ **hotovo** — `/en/what-is-hermes/`, `/en/features/`, `/en/community/` existují a jsou v menu i sitemapě |
| 3 | `404.html` a `500.html` měly `robots: index, follow` | ✅ **OPRAVENO 15. 10. 2026** — obě mají `noindex, follow`; ověřeno živě (chybová stránka vrací 404 a zakazuje indexování) |
| 4 | Redesign nebyl zálohovaný v gitu | ✅ **HOTOVO 15. 10. 2026** — commit `7d79b93` (424 souborů) odeslán na větev `feat/redesign` v `ostravajih/hermes-ai-web` |
| 5 | Nevyvážený `<div>` v článku o Dockeru | ⚠️ **částečně** — starý soubor je dnes jen přesměrování; v novém článku `blog/clanek/hermes-agent-docker/` je o jednu uzavírací značku víc (15× `<div>` / 16× `</div>`) než otevírací. Prohlížeč přebytečnou značku ignoruje, vykreslení je ověřené v pořádku — jde jen o neplatné HTML |
| 6 | Stránkování blogu nemělo EN protějšek | ✅ **vyřešeno** — CZ `/blog/stranka/2\|3/`, EN `/en/blog/page/2\|3/`, přepínač je tabulkou |
| 7 | Staré soubory mimo provoz | ⏳ **otevřené** — `redesing/` má 62 MB, v produkci zůstávají PNG duplikáty k WebP (`co-je-hermes.png`, `hosting-hero.png`, `skills-hero.png`, `hero-ai-agent-approved.png`) |
| 8 | Chybí `theme-color` a `rel="manifest"` | ⚠️ **částečně** — `theme-color #061020` je na všech stránkách ✅; `rel="manifest"` chybí na všech (0 stránek) |
| 9 | E-maily z `@hermes-ai.cz` bez SPF/DKIM/DMARC | ✅ **hotovo** — SPF `v=spf1 mx a -all`, DMARC `p=none` + reporty, DKIM (selektor `dkim`); ověřeno živě v DNS |
| 10 | Články měly jen jeden společný náhledový obrázek a žádný obrázek v textu | ✅ **hotovo** — 54 obrázků (`assets/redesign/images/blog/`), každý článek svůj, používá se i v `og:image` |
| 11 | CSS se drželo v keši 7 dní | ✅ **hotovo** — odkazy mají verzi (`style.css?v=20261015-18`, `zive.js?v=4`, `matomo.js?v=20261015b`) |
| 12 | 66 starých adres se přesměrovává „měkkým“ způsobem (meta refresh, kód 200) | 🟡 **částečně opraveno** — 8 z nich už posílá skutečné 301 (`/skills`, `/komunita`, 7 cest bez lomítka); zbývá 58 starých adres článků a kořenových souborů |
| 13 | 5 chyb v hero sekcích | ✅ **opraveno** a ověřeno 90 měřeními (viz 1.3–1.5) |
| 14 | **(nové)** 7 cest bez lomítka obsloužil starý soubor s meta refreshem místo 301 | ✅ **OPRAVENO 15. 10. 2026** — v nginx je 7 výslovných pravidel `return 301`; ověřeno: všechny vrací 301 na adresu s lomítkem (200) a zachovají parametry |

Největší zbývající SEO dluh je teď **58 starých adres článků** s „přesměrováním uvnitř" (meta refresh
místo 301) — cesty bez lomítka a chybové stránky jsou vyřešené.

---

## 5. Navržené opravy (⏳) — se stavem

### Krok A — oprava přepínače jazyka ✅ HOTOVO
Tabulka dvojic česká ↔ anglická adresa v `assets/script.js`; kliknutí na EN vždy otevře existující stránku.

### Krok B — anglické verze 3 stránek ✅ HOTOVO
`/en/what-is-hermes/`, `/en/features/`, `/en/community/` — založené, v menu, v sitemapě i v přepínači.

### Krok C — drobné technické opravy (částečně)
- ✅ `theme-color` (barva lišty na telefonu) na všech stránkách.
- ✅ SPF/DKIM/DMARC pro `@hermes-ai.cz` — hotové a ověřené (`EMAILY-SPF-DKIM-DMARC.md`).
- ✅ `404.html` a `500.html` → `noindex, follow` — hotovo a ověřeno.
- ✅ 7 cest bez lomítka → skutečné 301 v nginx — hotovo a ověřeno.
- ⚠️ přebytečná uzavírací značka `</div>` v `blog/clanek/hermes-agent-docker/` — **zbývá** (kosmetika).

### Krok D — záloha redesignu (probíhá)
- ✅ tar zálohy jednotlivých kroků jsou ve scratch (`svetly-rezim-zaloha.tgz`, `fonty-zaloha/`).
- ✅ **commit + push na `feat/redesign`** — hotovo 15. 10. 2026 (commit `7d79b93`, 424 souborů).

### Krok E — úklid (zbývá)
- Nejdřív ověřit, že na soubor nevede žádný odkaz, pak smazat PNG duplikáty (asi 7 MB).
- Zdrojové obrázky mimo web přesunout do archivu (`redesing/` má 62 MB).

---

## 6. Nápady (💡) — se stavem

1. **Vlastní obrázek pro každý článek (27 kusů).** ✅ **hotovo** — 54 obrázků (CZ + EN), v článku i v `og:image`.
2. **Doplnit ilustrace do sekcí** podle `PAGE_ASSET_MAP.json` — ⏳ neprovedeno (sekce na podstránkách mají text a hero obrázek).
3. **Tlačítka v hero** (např. „Začít instalovat ↓") na podstránkách — ⏳ neprovedeno (mají je jen úvodní stránky).
4. **(nové)** Doplnit `rel="manifest"` a sadu ikon, aby se web dal přidat na plochu telefonu.

---

## 7. Co potřebuji od vás rozhodnout (stav)

1. ~~Vygenerovat 27 obrázků pro články?~~ ✅ hotovo.
2. ~~Přeložit a založit 3 chybějící anglické stránky?~~ ✅ hotovo.
3. ~~Poslat redesign do GitHubu~~ ✅ **hotovo 15. 10. 2026** (větev `feat/redesign`).
4. ~~Doplnit SPF/DKIM/DMARC?~~ ✅ hotovo (záznamy jsou v DNS a ověřené).

**Otevřené a připravené k rozhodnutí:** nahradit zbývajících 58 „měkkých" přesměrování skutečným 301,
doplnit `rel="manifest"` a uklidit nepoužité soubory (krok E výše).
Indexování chybových stránek i cesty bez lomítka jsou **hotové 15. 10. 2026**.
