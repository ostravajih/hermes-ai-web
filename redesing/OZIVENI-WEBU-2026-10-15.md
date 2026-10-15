# Oživení webu — živé efekty (15. 10. 2026)

Web byl do 15. 10. 2026 čistě statický. Na základě živé ukázky si majitel vybral **6 efektů**.
Téhož dne večer po připomínkách **tři z nich ubral** (byly to další vrstvy a blikání navíc) — níže
je stav po této opravě.

## Co je nasazené (stav po večerní opravě)

| # | Efekt | Kde na webu | Jak je udělaný |
|---|---|---|---|
| 1 | **Síť bodů, která se spojuje s kurzorem myši** | horní sekce všech stránek | plátno s body; mezi blízkými body se táhnou spojnice, ke kurzoru myši vede výraznější spojnice a jemná záře |
| 2 | **Napočítávání čísel** | statistiky v horní sekci | číslo se napočítá z 0 na cílovou hodnotu, když se dostane na obrazovku |
| 3 | **Světlo u kurzoru + náklon karty** | karty článků, dlaždice, statistiky | pod myší se rozsvítí světlo, malé karty se jemně nakloní (max 4°) |
| 4 | **Psací terminál** | `/instalace/` a `/en/installation/` | příkaz se napíše sám, pak se objeví výsledek; kliknutím se přehraje znovu |

Efekty, které majitel **nechtěl**: nekonečný pás nástrojů, postup čtení u článků,
rychlé hledání Ctrl+K, magnetická tlačítka. Do webu se nedostaly.

### Co bylo zrušeno a proč (15. 10. 2026 večer)

| Zrušeno | Důvod |
|---|---|
| **Tři barevné rozostřené plochy** (aurora) nad obrázkem | obrázek v horní sekci byl „jako v mlze“ — šlo o další vrstvu navíc |
| **Ztmavení přes obrázek** (gradient kvůli čitelnosti) | totéž — obrázek ztrácel ostrost; web měl vlastní ztmavení už předtím a stačí |
| **Prolití mezi stránkami** (efekt 9) | při kliknutí na jinou stránku to **blikalo** |
| **Posun obrázku podle myši** (efekt 10) | majitel zrušil |

Přes obrázek tak jde **jediná vrstva** — tenká síť bodů. Ověřeno měřením: horní sekce se s efekty
liší jen v **0,8 % pixelů** (dřív s mlžnými plochami a ztmavením to byly desítky procent).

## Kde to je v kódu

| Soubor | Co obsahuje |
|---|---|
| `assets/zive.js` | všechny efekty (~13 KB, bez jediné externí knihovny) |
| `assets/redesign/style.css` | sekce „Oživení webu“ na konci souboru (vrstvy, světlo karet, kurzor terminálu, vypnutí při „omezit pohyb“) |
| hlavička 78 stránek | `<script src="/assets/zive.js?v=4" defer></script>` hned za hlavním skriptem, `style.css?v=20261015-18` |

## Pravidla, která efekty dodržují (a proč)

1. **Jen posuv a průhlednost** (`transform`, `opacity`). Nikdy se nemění rozměry ani vzdálenosti,
   takže obsah nemůže „poskočit“ — to je přesně to, co způsobovalo blikání.
2. **Nepřidávat vrstvy přes obrázek.** Jedna tenká síť bodů stačí; jakákoli další plocha nebo
   ztmavení nad obrázkem ho okamžitě „zamlží“ (majitel to pozná a vadí mu to).
3. **Skript má `defer`** a je na konci stránky → nemůže zdržet první vykreslení.
   Naměřeno: skript se stahuje **současně s CSS** (63 ms), stránka je hotová za ~350 ms.
4. **Nic se nenačítá z internetu** — žádná knihovna, žádný obrázek navíc.
5. **Síť se zjeví plynule** (0,55 s), aby body „nenaskočily“ naráz při přechodu na stránku.
6. **Pauza mimo obrazovku** — plátno se přestane kreslit, když horní sekce není vidět,
   a když je záložka prohlížeče na pozadí.
7. **Respektuje systémové „omezit pohyb“** — plátno se vůbec nevytvoří, kurzor terminálu nebliká,
   čísla se rovnou zobrazí hotová.
8. **Na telefonu se vypíná to, co nemá smysl** — náklon karet (dotyk žádnou myš nemá).
9. **Žádné prolití mezi stránkami** — vlastník ho vnímal jako blikání; přechody mezi stránkami
   musí zůstat okamžité, jako byly před efekty.

## Jak efekty vypnout nebo upravit

- **Všechny najednou:** ze stránek odebrat `<script src="/assets/zive.js?v=4" defer></script>`.
- **Jen některý:** v `zive.js` zakomentovat příslušné volání v `start()`:
  `pozadiHorniSekce()` (1), `ozivCisla()` (2), `ozivKarty()` (3), `psaciTerminal()` (4).
- **Vyzkoušet efekty pro myš i na dotykovém zařízení:** přidat do adresy `?zive=1`
  (např. `hermes-ai.cz/?zive=1`).

**Pozor při každé úpravě:** po změně `assets/zive.js` nebo `style.css` je **nutné zvýšit číslo
verze** v odkazech (`?v=`) ve všech stránkách. Prohlížeče si soubory drží 7 dní v keši a bez
zvýšení verze uvidí lidé (i já při testech) starou verzi — 15. 10. 2026 se to stalo a málem to
vedlo k mylnému závěru, že efekt nefunguje.

## Jak se to ověřovalo (a co se nesmí stát)

| Test | Výsledek |
|---|---|
| **Ostrost obrázku v horní sekci** (srovnání se stavem bez efektů) | ✅ liší se jen 0,8 % pixelů |
| **Blikání po tvrdém obnovení** (6 stránek, vypnutá keš) | ✅ obsah se po vykreslení nikdy nemění |
| **Text nad efekty** (nápisy na podstránkách) | ✅ vrstva textu 3, efekt 2; `elementFromPoint` vrací nadpis |
| Žádné prolití mezi stránkami | ✅ v CSS nejsou žádná pravidla `view-transition` |
| Reakce sítě na myš | ✅ u kurzoru 9 659 pixelů spojnic a záře (nejsilnější 223/255) |
| Výška horních sekcí | ✅ 500 px na počítači, 480 px na telefonu (beze změny) |
| Vodorovné přetečení | ✅ 0 px (počítač i telefon 390 px) |
| Chyby v prohlížeči | ✅ žádné |
| Systémové „omezit pohyb“ | ✅ plátno se nevytvoří |
| Rychlost | ✅ HTML hotové 293 ms, vše 354 ms |
| Adresy ze sitemapy | ✅ 76 z 76 vrací 200 |

### Past, na kterou se narazilo (aby se neopakovala)

Na podstránkách má pravidlo `.page-content .route-hero--poster .route-hero__copy` (3 třídy) vyšší
váhu než `.route-hero--poster .route-hero__copy` (2 třídy) — text proto zůstal **pod** efektovou
vrstvou a nápisy vypadaly „jako schované pod vrstvou“. Stačilo do pravidla pro vrstvy napsat i delší
selektor. Ověřuje se to `document.elementFromPoint()` v místě nadpisu — musí vrátit textový prvek,
ne plátno.

## Oprava efektu 4 (15. 10. 2026, večer)

- **Chyba:** efekt „psací terminál" se spouštěl podle toho, zda adresa *obsahuje* „instalace"
  (`/(instalace|installation)/`). Nová stránka wiki `/wiki/zaciname/instalace/` tím efekt chytla
  a do okna s příkazem `ssh` psala vymyšlený výstup („kontroluji systém… stahuji… hotovo") —
  působilo to, jako by server po přihlášení pracoval sám od sebe.
- **Oprava:** adresa se porovnává přesně (`^/(en/)?(instalace|installation)/?$`), takže efekt
  zůstává jen na stránce instalace.
- **Novinka:** blok s příkazem si může sám říct, co má vypsat — atribut `data-vystup`
  na `.code-block` (řádky oddělené `|`, může obsahovat HTML). Bez atributu se použije
  výchozí text pro instalaci. Na wiki se tak v okně `ssh` objeví skutečná odpověď serveru
  (uvítání Ubuntu, poslední přihlášení, čekající kurzor).
- **Souvislost:** tlačítko „Kopírovat" (wiki.js) si text ukládá při načtení stránky, takže
  po přehrání efektu nezkopíruje výstup příkazu, ale jen samotný příkaz bez `$` a komentářů.
