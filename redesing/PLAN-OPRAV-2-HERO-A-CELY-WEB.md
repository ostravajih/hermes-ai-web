# Návrh oprav celého webu hermes-ai.cz — 2. část (hero sekce a zbytek webu)

**Datum:** 14. 10. 2026 · **Zpracoval:** Hermes
**Náhled návrhu:** `/root/.hermes/profiles/hermes-web/cache/scratch/hero-navrh.html`
**Souvisí:** `redesing/AUDIT-A-PLAN-OPRAV-2026-10-14.md` (technický audit), `redesing/PLAN.md` (původní redesign)

> **Stav (ověřeno 15. 10. 2026):** ✅ **provedeno** — hero sekce jsou „plakát" na všech stránkách (A1–A4, A6),
> přepínač jazyka vede na skutečné protějšky (B1), anglické verze tří stránek existují (B2),
> `theme-color` je na všech stránkách (B7), chybové stránky 404/500 už indexování zakazují (B3),
> 7 cest bez lomítka má skutečné 301 (část B6). ⏳ **zůstává otevřené:** 58 starých adres článků
> s meta refreshem (zbytek B6), nepoužité PNG duplikáty v produkci (B4), sada ikon a `rel="manifest"` (B5),
> sladění balíčku `redesing/` s webem (D2). Redesign je v gitu (C1 hotovo 15. 10. 2026, větev
> `feat/redesign`), dokumentace (D1) je srovnaná —
> viz `README.md`. Aktuální seznam otevřených věcí drží `OPRAVY-CELEHO-WEBU-2026-10-15.md`.
> Poznámka: body o světlém režimu (A3, A6) jsou od 15. 10. 2026 bezpředmětné — web je jen tmavý.

---

## 1. Jak má hero vypadat (můj opravený výklad zadání)

Hero sekce = **„plakát“**. Tři vrstvy přes sebe:

1. **Obrázek přes celou šířku sekce** — od levého okraje k pravému, bez rámečku a bez zaoblených rohů.
2. **Přechod (ztmavení)** — jemné ztmavení ve směru, kde leží text, aby byl text dobře čitelný.
3. **Text navrchu jako vrstva** — nadpis, popis a tlačítka položené přes obrázek. Text zůstává skutečný
   text (kvůli vyhledávačům i čtečkám), není vypálený v obrázku.

Dole se hero **přechodově „rozpije“ do další sekce** — stejný princip jako u sekce **„Rychlý start“**
na úvodu, kde obrázek terminálu přechází do pozadí přes průhlednost (dnes je to jediné místo, kde to funguje).

**Použité soubory:** na počítač `…_1920x700.webp`, na mobil `…_mobile_768x960.webp`.
Sekce „Česká komunita“ = `hermes_agent_community_hero_1600x900.webp`. Úvod má vlastní obrázek i na mobilu.

---

## 2. Jak to vypadá dnes (co je špatně)

| Stránka | Dnes | Má být |
|---|---|---|
| `/instalace/`, `/hosting/`, `/skills/`, `/faq/`, `/blog/` (+ EN) | Plakát 1920×700 je vložený jako **malá karta v pravém sloupci** — vykresluje se na ~641×234 px vedle textu | Plakát přes celou sekci, text navrchu |
| Úvod (`/`) | Obrázek 1672×941 v „kartičce“ vpravo, pozadí jen dekorativní; na mobilu zmenšený na 358×201 | Plakát přes celou sekci, text navrchu, **i na mobilu** |
| Sekce „Nejste na to sami“ (úvod) + `/komunita/` | Použit `community.webp` (1600×900) v rámečku; **ve světlém režimu se ale zobrazuje jiný obrázek** (`community-light.webp`, 960×540) | Stejný obrázek 1600×900 jako plakát, přechod jako jinde |
| `/co-je-hermes/` | Žádný plakát — používá obrázek z brand kitu 960×540 (`agent-profile-dark/light`) | Rozhodnout (viz §5) |
| `/funkce/` | Žádný plakát — používá obrázek 1200×700 (`features-tools-automation`) | Rozhodnout (viz §5) |
| 54 článků blogu | Nemají v hlavičce žádný obrázek | Rozhodnout (viz §5) |
| `/instalace/` | V balíčku jsou **dvě sady** obrázků (starší `Hermes_Agent_Instalace_Hero_Assets` a novější `Hermes_Instalace_Operatorka_v2`) | Rozhodnout (viz §5) |

**Co už je hotové:** certifikát pro www + přesměrování (14. 10.), mobilní varianty obrázků jsou
nakopírované do webu (`*-hero-mobile.webp`), ořez způsobený pevným poměrem stran je odstraněný.

**Váhy obrázků:** plakáty 86–110 KB (mobil) a 128–244 KB (počítač) — snesou být přes celou šířku.

---

## 3. Technický návrh (jednoduše vysvětleno)

**Jak se obrázek dostane „za“ text:**

```html
<section class="hero-poster">
  <picture class="hero-poster__bg">
    <source media="(max-width: 560px)" srcset="…_mobile_768x960.webp">
    <img src="…_1920x700.webp" alt="" width="1920" height="700">
  </picture>
  <div class="container hero-poster__copy">   <!-- text jako vrstva navrchu -->
    <h1>…</h1><p class="lead">…</p><a class="button">…</a>
  </div>
</section>
```

**Co k tomu přidá CSS (jen tři pravidla):**

1. obrázek je „absolutně“ položený přes celou sekci a ořezává se podle potřeby
   (`position:absolute; inset:0; width:100%; height:100%; object-fit:cover`);
2. přes obrázek jde **ztmavující přechod** — na počítači zleva doprava, na mobilu zespodu nahoru
   (text je pak čitelný na každém pozadí);
3. dolů jde **přechod do barvy pozadí** — tím zmizí okraj a hero se „rozpije“ do další sekce.

**Proč `<picture>`:** prohlížeč si sám vybere správný soubor. Na mobil se nestahuje velký plakát
(1920 px), ale úzká varianta (768 px) — web je díky tomu na mobilu rychlejší.

**Výška sekce:** na počítači cca 480–560 px (podle šířky okna), na mobilu cca 520–640 px,
aby měl portrétní obrázek prostor a text se vešel.

**Kontrola po nasazení (udělám sám, než ti řeknu „hotovo“):** prohlížeč Chromium změří každou
stránku ve dvou šířkách (počítač 1280 px, mobil 390 px) a ve dvou režimech (tmavý/světlý) a ověří:
obrázek je přes celou šířku sekce, text je čitelný (kontrast), nic nepřetéká, stránka se načte bez chyby.

---

## 4. Kompletní seznam oprav celého webu

### A) Hero a obrázky (hlavní téma — 8 stránek CZ + 5 EN + 2 sekce na úvodu)

| # | Oprava | Kde | Odhad |
|---|---|---|---|
| A1 | Předělat route hero na „plakát“ (obrázek přes celou sekci, text navrchu, přechod dolů) | instalace, hosting, skills, faq, blog + EN | 2 h |
| A2 | Stejně předělat úvodní hero (dnes karta vpravo) | `/`, `/en/` | 45 min |
| A3 | Sekce „Nejste na to sami“ + hero na `/komunita/` — použít `hermes_agent_community_hero_1600x900` jako plakát; **zrušit záměnu za jiný obrázek ve světlém režimu** | `/`, `/komunita/` | 45 min |
| A4 | Přejmenovat nasazené mobilní soubory na tvar `*_mobile_768x960.webp`, aby se daly snadno dohledat | `assets/redesign/images/sections/` | 10 min |
| A5 | Dopsat pravidla do `redesing/PLAN.md` + manifestu (aby dokumentace nelhala) | dokumentace | 20 min |
| A6 | Dopočítat rozměry a přechody i pro tmavý/světlý režim u všech plakátů | CSS | 30 min |

### B) Rozbité věci (nalezené auditem, nesouvisí s hero)

| # | Co je špatně (lidsky) | Návrh opravy | Odhad |
|---|---|---|---|
| B1 | **Přepínač jazyka posílá lidi na neexistující stránky** — u 29 z 75 stránek (např. na `/instalace/` vede tlačítko EN na `/en/instalace/`, ale anglická stránka je `/en/installation/`; u 19 článků se liší adresy CZ/EN) | Předělat přepínač tak, aby u každé stránky věděl, kam vede její dvojče | 1 h |
| B2 | **Anglické verze chybí u 3 stránek** (`/co-je-hermes/`, `/funkce/`, `/komunita/`) — anglicky mluvící návštěvník je nenajde | Doplnit anglické verze, nebo z těch stránek anglický přepínač odstranit (rozhodnutí §5) | 2 h / 15 min |
| B3 | **Chybová stránka 404 a 500 se může dostat do Googlu** (má povolené indexování) | Zakázat indexování chybových stránek | 5 min |
| B4 | **7,2 MB nepotřebných souborů** ve webu (např. `co-je-hermes.png` 2 MB, `hosting-hero.png` 1,8 MB — existují jen jako záložní kopie k WebP) | Smazat, ponechat jen používané soubory | 30 min |
| B5 | **Staré favicony a manifest** z července (web používá nové SVG logo, staré soubory zůstaly) | Doplnit kompletní sadu ikon (i pro mobil na plochu) a staré smazat | 45 min |
| B6 | **66 starých adres se přesměrovává „obalem“ (meta refresh)** místo skutečného serverového přesměrování | Nahradit skutečným přesměrováním 301 v nginx (rychlejší, čistší pro Google) | 45 min |
| B7 | Na stránkách chybí `theme-color` (barva adresního pruhu na mobilu) | Doplnit | 15 min |

### C) Provoz a bezpečí (nejdůležitější riziko)

| # | Co je špatně | Návrh | Odhad |
|---|---|---|---|
| C1 | **Celý redesign není v Gitu ani na GitHubu** — `HEAD` i `origin/main` obsahují starou verzi webu; kdyby se server pokazil, redesign je nevratně pryč (194 změn čeká na uložení, 262 souborů navíc) | Odeslat (`commit` + `push`) na větev `feat/redesign` a otevřít PR | 15 min |
| C2 | Chybí záložní archiv (tar) z původního plánu; existuje jen značka v Gitu před redesignem | Vytvořit záložní archiv | 5 min |
| C3 | Při obnově certifikátu se nenačte znovu nginx (muselo se ručně) | Přidat automatické načtení po obnově | 10 min |
| C4 | Při obnově certifikátů hlásí chybu pomocný skript pro Minecraft server (nesouvisí s tímto webem, ale mate) | Opravit nebo vypnout hlášení | 20 min |

### D) Dokumentace

| # | Co je špatně | Návrh | Odhad |
|---|---|---|---|
| D1 | `README.md` uvádí anglické stránkování blogu `/en/blog/stranka/`, realita je `/en/blog/page/`; mluví o 21 ikonách, balíček má 32; popisuje breakpointy, které v CSS nejsou | Srovnat dokumentaci s realitou | 30 min |
| D2 | Balíček `redesing/` se u 17 souborů rozešel s webem (novější verze grafiky jen na webu) | Doplnit balíček, aby byl znovu zdrojem pravdy | 20 min |
| D3 | `audit.md` je ze 9. 7. a popisuje stav před redesignem | Označit jako zastaralý / doplnit odkaz na aktuální audit | 10 min |

---

## 5. Co potřebuji od tebe (5 rozhodnutí)

1. **Instalace:** v balíčku jsou dvě sady plakátů. Na webu běží novější `Hermes_Instalace_Operatorka_v2`
   (sedí ke stylu ostatních stránek). **Doporučuji ji ponechat** a starou sadu použít jen jako zálohu — souhlasíš?
2. **`/co-je-hermes/` a `/funkce/` nemají plakát 1920×700** — v balíčku k nim plakát v plné velikosti není.
   Možnosti: (a) nechat jim dnešní obrázky a roztáhnout je přes celou sekci, (b) vygenerovat nové plakáty
   1920×700 + mobilní 768×960 (umím vygenerovat ve stejném stylu), (c) nechat je bez plakátu.
   **Doporučuji (b)** — bude to stejné jako ostatní stránky.
3. **Články blogu (54) nemají obrázek v hlavičce.** Přidávat plakát do každého článku znamená 54 nových
   obrázků (váha + práce). **Doporučuji** dát plakát jen článkům, které si ho zaslouží (např. 6 nejčtenějších),
   nebo žádný.
4. **Úvod na mobilu:** pro úvodní obrázek 1672×941 neexistuje mobilní varianta.
   **Doporučuji** z něj vyrobit mobilní výřez 768×960 (jako u ostatních stránek), aby na mobilu sedl na výšku.
5. **můžu po odsouhlasení odeslat redesign do Gitu (C1)?** Dnes není nikde zálohovaný — to je největší riziko.

---

## 6. Pořadí prací, jakmile odsouhlasíš

1. C1 + C2 — záloha a odeslání do Gitu (5 minut, hned klid na práci)
2. A1–A3 — hero jako plakát na 13 stránkách + 2 sekce na úvodu, včetně mobilních variant
3. A4–A6 — názvy souborů, dokumentace, režimy
4. B1–B3, B7 — přepínač jazyka, anglické stránky, chybové stránky, barva pruhu
5. B4–B6 — úklid souborů, ikony, skutečná přesměrování
6. D1–D3 — dokumentace

Po každém kroku ti napíšu, co je hotové a co jsem ověřil v prohlížeči — nic nehlásím „hotovo“ jen podle zápisu do souboru.
