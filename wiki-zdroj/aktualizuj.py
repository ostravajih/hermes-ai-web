#!/usr/bin/env python3
"""Srovná společné části všech stránek wiki podle seznamu `stranky.json`.

Co dělá (vše najednou, aby se nic nezapomnělo):
  1. postranní nabídku na všech stránkách wiki (podle jazyka) — včetně označení hotových
  2. karty stránek a karty fází na rozcestníku wiki
  3. dvojice adres pro přepínač jazyka v `assets/script.js` (WIKI_CS_EN)
  4. nové adresy do `sitemap.xml`

Spouštět po každé nové hotové stránce:
    python3 wiki-zdroj/aktualizuj.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import VERZE_CSS, VERZE_SK, VERZE_STYLE, WEB, STRANKY, bocni, karty_html, faze_html  # noqa: E402

ZMENY: list[str] = []


def uprav_soubor(cesta: Path, vzor: str, nahrada, popis: str) -> None:
    if not cesta.exists():
        return
    puvodni = cesta.read_text(encoding="utf-8")
    novy, pocet = re.subn(vzor, lambda m: nahrada if callable(nahrada) else nahrada, puvodni, count=1, flags=re.S)
    if pocet and novy != puvodni:
        cesta.write_text(novy, encoding="utf-8")
        ZMENY.append(f"{popis}: {cesta.relative_to(WEB)}")


def aktualizuj_bocni() -> None:
    for cesta in sorted((WEB / "wiki").rglob("index.html")) + sorted((WEB / "en" / "wiki").rglob("index.html")):
        text = cesta.read_text(encoding="utf-8")
        if 'wiki-layout' not in text:
            continue
        jazyk = "en" if "/en/wiki/" in str(cesta) else "cs"
        kanonicka = f'<link rel="canonical" href="https://hermes-ai.cz'
        m = re.search(r'<link rel="canonical" href="https://hermes-ai\.cz([^"]+)"', text)
        aktivni = "/" + m.group(1).strip("/") + "/" if m else "/"
        uprav_soubor(cesta, r'<aside class="wiki-side".*?</aside>', bocni(jazyk, aktivni), "postranní nabídka")


def aktualizuj_rozcestnik() -> None:
    for cesta, jazyk in ((WEB / "wiki/index.html", "cs"), (WEB / "en/wiki/index.html", "en")):
        if not cesta.exists():
            continue
        text = cesta.read_text(encoding="utf-8")
        if '<div class="wiki-karty">' in text:
            uprav_soubor(cesta, r'<div class="wiki-karty">.*?</div>', karty_html(jazyk), "karty stránek")
        if '<div class="wiki-faze">' in text:
            uprav_soubor(cesta, r'<div class="wiki-faze">.*?</div>', faze_html(jazyk), "karty fází")


def aktualizuj_prepinac() -> None:
    cesta = WEB / "assets/script.js"
    if not cesta.exists():
        return
    dvojice = '        "/wiki/": "/en/wiki/",\n' + "".join(
        f'        {s["cs"]!r}: {s["en"]!r},\n'.replace("'", '"')
        for s in STRANKY if s["hotovo"]
    )
    novy_blok = "    const WIKI_CS_EN = {\n" + dvojice + "    };"
    uprav_soubor(cesta, r'    const WIKI_CS_EN = \{.*?\n    \};', novy_blok, "dvojice adres pro přepínač jazyka")


def aktualizuj_sitemapu() -> None:
    cesta = WEB / "sitemap.xml"
    if not cesta.exists():
        return
    text = cesta.read_text(encoding="utf-8")
    pridano = 0
    for s in STRANKY:
        if not s["hotovo"]:
            continue
        for url in (s["cs"], s["en"]):
            plna = "https://hermes-ai.cz" + url
            if f"<loc>{plna}</loc>" not in text:
                text = text.replace(
                    "</urlset>",
                    f'<url><loc>{plna}</loc><lastmod>2026-10-15</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n</urlset>',
                    1,
                )
                pridano += 1
    if pridano:
        cesta.write_text(text, encoding="utf-8")
        ZMENY.append(f"sitemapa: přidáno {pridano} adres")


def aktualizuj_verze_vzhledu() -> None:
    """Aby se vzhled a skripty wiki nemusely přepisovat ručně na každé stránce.

    Prohlížeč si soubory vzhledu drží 7 dní, takže po každé změně `wiki.css`/`wiki.js` stačí
    zvednout verzi v `sablona.py` a spustit tento skript — přepíše ji na všech stránkách wiki.
    """
    for cesta in sorted((WEB / "wiki").rglob("index.html")) + sorted((WEB / "en" / "wiki").rglob("index.html")):
        text = cesta.read_text(encoding="utf-8")
        if "wiki.css?v=" not in text:  # rozcestník wiki vzhled taky používá
            continue
        novy = re.sub(r"wiki\.css\?v=[^\"']+", f"wiki.css?v={VERZE_CSS}", text)
        novy = re.sub(r"wiki\.js\?v=[^\"']+", f"wiki.js?v={VERZE_SK}", novy)
        novy = re.sub(r"style\.css\?v=[^\"']+", f"style.css?v={VERZE_STYLE}", novy)
        if novy != text:
            cesta.write_text(novy, encoding="utf-8")
            ZMENY.append(f"verze vzhledu: {cesta.relative_to(WEB)}")


def aktualizuj_obrazky_hero() -> None:
    """Horní sekce odkazovaly na mobilní obrázek se špatným jménem (podtržítko místo pomlčky),
    takže se na telefonu obrázek nezobrazil. Srovná se na všech stránkách wiki."""
    for cesta in sorted((WEB / "wiki").rglob("index.html")) + sorted((WEB / "en" / "wiki").rglob("index.html")):
        text = cesta.read_text(encoding="utf-8")
        novy = re.sub(r"(/assets/redesign/images/sections/[a-z0-9-]+)_hero_mobile_", r"\1-hero_mobile_", text)
        if novy != text:
            cesta.write_text(novy, encoding="utf-8")
            ZMENY.append(f"obrázek horní sekce: {cesta.relative_to(WEB)}")


VZOR_TABULKA = re.compile(r'<table class="wiki-tabulka">(.*?)</table>', re.S)


def _nazev_sloupce(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).replace("&nbsp;", " ").strip().replace('"', "&quot;")


def _uprav_tabulku(m):
    """Přidá názvy sloupců k buňkám a označí řádek s hlavičkou.

    Na telefonu se z tabulky stanou čitelné bloky (název sloupce nad hodnotou) — bez toho
    si tabulka vynutí šířku sloupce a článek přeteče mimo displej.
    Opakované spuštění nic nemění; když tabulka hlavičku ztratila, obnoví ji z názvů sloupců.
    """
    vnitrek = m.group(1)
    radky = re.findall(r"<tr[^>]*>.*?</tr>", vnitrek, re.S)
    if not radky:
        return m.group(0)

    if "<th" in radky[0]:
        nazvy = [_nazev_sloupce(h) for h in re.findall(r"<th[^>]*>(.*?)</th>", radky[0], re.S)]
        telo = radky[1:]
    elif "data-nazev" in radky[0]:  # hlavička se ztratila → obnovit z názvů sloupců
        nazvy = [_nazev_sloupce(n) for n in re.findall(r'data-nazev="([^"]*)"', radky[0])]
        telo = radky
    else:
        return m.group(0)

    hlavicka = '<tr class="wiki-tabulka__hlavicka">' + "".join(f"<th>{n}</th>" for n in nazvy) + "</tr>"
    nove = []
    for radek in telo:
        poradi = [0]

        def dopln(m2):
            j = poradi[0]
            poradi[0] += 1
            nazev = nazvy[j] if j < len(nazvy) else ""
            if not nazev or "data-nazev" in m2.group(0):
                return m2.group(0)
            return m2.group(0).replace("<td", f'<td data-nazev="{nazev}"', 1)

        nove.append(re.sub(r"<td[^>]*>", dopln, radek))
    return ('<table class="wiki-tabulka">' + hlavicka + "".join(nove) + "</table>")


def aktualizuj_tabulky() -> None:
    for cesta in sorted((WEB / "wiki").rglob("index.html")) + sorted((WEB / "en" / "wiki").rglob("index.html")):
        text = cesta.read_text(encoding="utf-8")
        if "wiki-tabulka" not in text:
            continue
        novy = VZOR_TABULKA.sub(_uprav_tabulku, text)
        if novy != text:
            cesta.write_text(novy, encoding="utf-8")
            ZMENY.append(f"tabulky pro telefon: {cesta.relative_to(WEB)}")


if __name__ == "__main__":
    aktualizuj_bocni()
    aktualizuj_rozcestnik()
    aktualizuj_prepinac()
    aktualizuj_sitemapu()
    aktualizuj_verze_vzhledu()
    aktualizuj_obrazky_hero()
    aktualizuj_tabulky()
    hotovo = [s["cislo"] for s in STRANKY if s["hotovo"]]
    print(f"Hotové stránky: {hotovo} | zbývá {len(STRANKY) - len(hotovo)}")
    if ZMENY:
        print("Změněno:")
        for z in ZMENY:
            print("  •", z)
    else:
        print("Nic k změně — všechno už je srovnané.")
