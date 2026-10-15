# Plán: oprava hero sekcí (pruh, stejná výška, umístění textu)
Vytvořeno 15. 10. 2026 · podklad: měření v prohlížeči + screenshot od zadavatele (světlý režim)

> **STAV: NASAZENO A OVĚŘENO 15. 10. 2026 (večer).**
> Pruh odstraněn, výška sjednocena na 500 px (počítač) / 460 px (tablet) / 480 px (mobil),
> text posunutý o 51 px od okraje a širší (760 px), statistiky vycentrované.
> Ověřeno 90 měřeními (15 stránek × 6 šířek okna) — všechny výšky přesné na ±0 px,
> obrázek kryje sekci, text nepřetéká, žádné přetečení, žádný rozbitý obrázek.
> V světlém režimu už hero nevykresluje světlý překryv (světlý a tmavý režim mají stejný jas).

---

## Co je špatně (změřeno, ne odhad)

### 1. V hero je vodorovný pruh (nejvýraznější ve světlém režimu)
Příčina: vrstva, která měla **ztmavovat spodní okraj**, se kvůli zděděnému pravidlu
`inset: 0` kreslila **nahoře** — a protože končila barvou pozadí (ve světlém režimu světlou),
vznikla světlá páska s **ostrou spodní hranou**.

Naměřeno na screenshotu (okno 1279 × 508, světlý režim):

| místo | jas (0–255) |
|---|---|
| 10 % výšky | 235 (světlé – páska) |
| 20 % | 69 → 124 → 193 (páska sílí) |
| **35 % výšky** | **ostrá hrana, skok 177** |
| 50–100 % | 40–99 (tmavé) |

Po zkušebním odstranění této vrstvy (test v prohlížeči, nic se neměnilo na serveru):
ostrá hrana zmizela, po celé sekci je stejnoměrně tmavý obraz, zbyla jen přirozená hranice pod hlavičkou.

Navíc se vrstvy ztmavení potkávají dvakrát (jedna přes druhou) — odtud dojem „jako by tam byla dvakrát".

### 2. Hero sekce nemají stejnou výšku
| Stránka | Výška hero (okno 1280) |
|---|---|
| Úvod | **501 px** ← referenční, „správná" |
| Instalace / Funkce / FAQ / Blog | 189–227 px |
| Komunita / Skills | 258–277 px |
| Mobil: úvod vs. ostatní | 482 px vs. 300 px |

Výška dnes vychází z množství textu, proto je každá stránka jiná.

### 3. Text je moc vlevo a statistiky nejsou vycentrované
- Textový blok začíná na 24 px od okraje a je úzký (620 px) → působí „přilepený" k levému okraji.
- Statistiky (60+ Nástrojů, 20+ Integrací, Aktivní Komunita, MIT Licence) jsou v bloku 660 px
  zarovnaném vlevo, proto jsou **posunuté doleva** místo na střed.

---

## Navržené opravy

### A. Pruh — jedna vrstva místo dvou
1. **Odstranit** samostatnou vrstvu ztmavení dolů (`::after`) úplně — obrázek se už sám
   rozplývá do pozadí svou maskou, takže druhá vrstva je navíc.
2. Pozadí hero nastavit **natrvalo na tmavou barvu** (`#07111F`) v obou režimech, aby se obrázek
   rozplýval do tmava a ne do světlého pozadí (ve světlém režimu by jinak vznikl světlý pruh dole).
3. Ponechat vodorovné ztmavení vlevo (kvůli čitelnosti textu) — to pruh nedělá.

Výsledek: sekce je v obou režimech stejnoměrně tmavá, žádná ostrá vnitřní hrana, text i statistiky zůstávají čitelné.

### B. Stejná výška na všech stránkách
Výška bude **pevná pro všechny hero sekce** (ne podle množství textu):

| Šířka okna | Výška hero (všechny stránky) |
|---|---|
| Počítač ≥ 1080 px | **500 px** (jako má dnes úvod) |
| 820–1080 px | 440 px |
| Mobil a tablet ≤ 820 px | 440 px |

Obsah se v sekci svisle vycentruje. Před nasazením ověřím, že se obsah úvodu na mobilu do 440 px
vejde (dnes má 412 px) — pokud bude těsno, zmenším rozestupy u statistik (ne výšku).

### C. Text a statistiky
- Textový blok **posunout od levého okraje dovnitř** (začátek na 6 % šířky, nejméně 40 px)
  a **roztáhnout doprava** (šířka bloku 620 → 760 px) — nadpis, popis i tlačítka tak mají víc místa.
- **Statistiky vycentrovat** na střed hero sekce: řada čtyř položek přes celou šířku obsahu,
  každá položka na střed svého sloupce (dnes jsou všechny vlevo).

Poznámka: chápu to tak, že text nemá být nalepený vlevo, ale posunutý kousek doprava a širší;
statistiky mají být na střed. Pokud to myslíte jinak, řeknete a upravím.

### D. Ověření po změně (až budu hotový)
1. **Pruh**: kontrola pixelů po řádcích — v hero nesmí být žádná umělá vodorovná hrana
   (skok jasu > 60 z 255), a to v tmavém i světlém režimu, na počítači i na mobilu.
2. **Stejná výška**: 15 stránek × 4 šířky okna — odchylka výšky nejvýš ±2 px od zadané hodnoty.
3. **Umístění textu**: změřená poloha textového bloku a statistik (mají být na středu).
4. **Screenshoty** tmavý/světlý režim, počítač/mobil — k nahlédnutí.

---

## Postup
1. Ukázkový náhled (jedna stránka, světlý + tmavý režim, počítač + mobil) ke schválení proporcí.
2. Nasazení do `style.css` (jedna úprava, pak kontrola podle bodu D).
3. Zvýšení verze CSS, aby se změna načetla i vám (keš je 7 dní).

## Co nechat být (mimo tento plán)
- Velikost písma nadpisů a délky textů (měnit jen pokud bude nutné kvůli vejité výšce).
- Obrázky samotné (mění se jen jejich ořez a rozplynutí).
