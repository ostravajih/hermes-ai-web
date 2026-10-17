#!/usr/bin/env python3
"""Testy webu hermes-ai.cz — spustitelné jedním příkazem.

    python3 test-web.py            # vše (disk + živý web)
    python3 test-web.py --jen-disk # bez síťových dotazů

Co se kontroluje:
  1. nevyvážené značky (rozbitý vzhled)
  2. odkazy do prázdna (stránky i obrázky, skripty, styly)
  3. hreflang — správná dvojice CZ/EN u každé stránky, oba směry
  4. sitemapa — každá živá stránka v ní je a každá adresa v ní existuje
  5. wiki — dlaždice na rozcestníku, žádný odznak „hotová“ (rozhodnutí vlastníka)
  6. verze vzhledu a skriptů (`?v=`) na každé stránce
  7. textové soubory pro vyhledávače a AI (robots, sitemap, llms.txt, ai.txt)
  8. živý web: všechny adresy ze sitemapy vrací 200; interní soubory jsou zavřené

Návratový kód 0 = všechno v pořádku, 1 = něco selhalo (vhodné pro cron).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

WEB = Path(__file__).resolve().parent
DOMENA = "https://hermes-ai.cz"
CHYBY: list[str] = []
VAROVANI: list[str] = []
POCTY: dict[str, int] = {}


def chyba(kde: str, co: str) -> None:
    CHYBY.append(f"{kde}: {co}")


def varovani(kde: str, co: str) -> None:
    VAROVANI.append(f"{kde}: {co}")


# --------------------------------------------------------------- pomocné
def html_soubory() -> list[Path]:
    """Všechny stránky webu (bez zdrojových složek a bez bundlovaných ukázek)."""
    skip = {"redesing", "wiki-zdroj", "blog-zdroj", ".git"}
    out = []
    for p in sorted(WEB.rglob("*.html")):
        if skip & set(p.relative_to(WEB).parts):
            continue
        out.append(p)
    return out


def adresa_souboru(p: Path) -> str:
    """Adresa stránky tak, jak ji vidí prohlížeč."""
    rel = p.relative_to(WEB).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def existuje(adresa: str) -> bool:
    cesta = WEB / adresa.strip("/")
    return cesta.is_dir() or (cesta / "index.html").exists() or cesta.is_file()


# --------------------------------------------------------------- 1. značky
def test_znacky() -> None:
    problemy = 0
    for p in html_soubory():
        if p.stat().st_size > 1_000_000 or "__bundler_" in p.read_text(encoding="utf-8", errors="replace"):
            continue
        text = p.read_text(encoding="utf-8")
        for znacka in ("div", "li", "ol", "table", "tr", "td", "th", "p", "span", "a", "article", "section"):
            otevreno = len(re.findall(r"<%s[\s>]" % znacka, text))
            zavreno = len(re.findall(r"</%s>" % znacka, text))
            if otevreno != zavreno:
                chyba(str(p.relative_to(WEB)), f"<{znacka}> {otevreno}× vs </{znacka}> {zavreno}×")
                problemy += 1
    POCTY["nevyvážené značky"] = problemy


# --------------------------------------------------------------- 2. odkazy
def test_odkazy() -> None:
    vzor = re.compile(r'(?:href|src)\s*=\s*["\'](/[^"\'#?]*)["\']')
    odkazu = 0
    spatnych = 0
    for p in html_soubory():
        text = p.read_text(encoding="utf-8", errors="replace")
        for cil in set(vzor.findall(text)):
            if not cil or cil.startswith(("/assets/", "/favicon")):
                continue
            if cil.split(".")[-1] in {"txt", "xml", "json", "webp", "png", "svg", "woff2", "css", "js", "ico"}:
                continue
            odkazu += 1
            if not existuje(cil):
                chyba(str(p.relative_to(WEB)), f"odkaz do prázdna → {cil}")
                spatnych += 1
    POCTY["kontrolovaných odkazů"] = odkazu
    POCTY["odkazy do prázdna"] = spatnych

    # obrázky, skripty a styly musí na disku existovat
    vzor_soubor = re.compile(r'(?:src|href)\s*=\s*["\'](/assets/[^"\'#?]*)["\']')
    chybejici = 0
    for p in html_soubory():
        for cil in set(vzor_soubor.findall(p.read_text(encoding="utf-8", errors="replace"))):
            if not (WEB / cil.strip("/")).is_file():
                chyba(str(p.relative_to(WEB)), f"chybí soubor → {cil}")
                chybejici += 1
    POCTY["chybějící soubory"] = chybejici


# --------------------------------------------------------------- 3. hreflang
VRZOR_HREFLANG = re.compile(r'<link rel="alternate" hreflang="([a-z-]+)" href="([^"]+)">')


def test_hreflang() -> None:
    dvojice: dict[str, dict[str, str]] = {}
    for p in html_soubory():
        text = p.read_text(encoding="utf-8", errors="replace")
        stranky = {k: v for k, v in VRZOR_HREFLANG.findall(text)}
        adresa = adresa_souboru(p)
        for jazyk in ("cs", "en", "x-default"):
            if jazyk not in stranky:
                chyba(adresa, f"chybí hreflang={jazyk}")
        for jazyk, cil in stranky.items():
            if not cil.startswith(DOMENA):
                chyba(adresa, f"hreflang={jazyk} nemíří na naši doménu: {cil}")
            elif not existuje(cil[len(DOMENA):]):
                chyba(adresa, f"hreflang={jazyk} míří na neexistující stránku: {cil}")
        if "cs" in stranky and "en" in stranky:
            dvojice[adresa] = {"cs": stranky["cs"][len(DOMENA):], "en": stranky["en"][len(DOMENA):]}

    obousmerne = 0
    preskoceno = 0
    for adresa, par in dvojice.items():
        # 404 a 500 nemají vlastní protějšek — míří na úvodní stránky, proto je přeskoč
        if adresa not in (par["cs"], par["en"]):
            preskoceno += 1
            continue
        je_en = adresa.startswith("/en/")
        vlastni = par["en"] if je_en else par["cs"]
        prot = par["cs"] if je_en else par["en"]
        if prot in dvojice:
            zpet = dvojice[prot]["en"] if je_en else dvojice[prot]["cs"]
            if zpet != vlastni:
                chyba(adresa, f"hreflang není obousměrný: {prot} míří na {zpet}, ne na {vlastni}")
                obousmerne += 1
    POCTY["stránek s hreflang"] = len(dvojice)
    POCTY["neobousměrných dvojic"] = obousmerne
    POCTY["bez vlastního protějšku (404/500)"] = preskoceno


# --------------------------------------------------------------- 4. sitemapa
def sitemap_adresy() -> list[str]:
    text = (WEB / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", text)


def test_sitemapa() -> None:
    adresy = sitemap_adresy()
    POCTY["adres v sitemapě"] = len(adresy)
    for url in adresy:
        if not url.startswith(DOMENA):
            chyba("sitemap.xml", f"cizí doména: {url}")
        elif not existuje(url[len(DOMENA):]):
            chyba("sitemap.xml", f"adresa neexistuje: {url}")
    v_sitemape = set(adresy)
    chybi = 0
    for p in html_soubory():
        adresa = adresa_souboru(p)
        if adresa in ("/404.html", "/500.html"):
            continue
        if DOMENA + adresa not in v_sitemape:
            chyba(adresa, "stránka není v sitemapě")
            chybi += 1
    POCTY["stránek mimo sitemapu"] = chybi


# --------------------------------------------------------------- 5. wiki
def test_wiki() -> None:
    import json

    cesta = WEB / "wiki-zdroj/stranky.json"
    if not cesta.exists():
        return
    data = json.loads(cesta.read_text(encoding="utf-8"))
    strank = data["stranky"]
    hotovych = [s for s in strank if s["hotovo"]]
    POCTY["stránek wiki (hotových)"] = len(hotovych)
    POCTY["stránek wiki (celkem)"] = len(strank)

    for s in strank:
        for jazyk in ("cs", "en"):
            stranka = WEB / s[jazyk].strip("/") / "index.html"
            if not stranka.exists():
                chyba(f"wiki stránka {s['cislo']} ({s['nazev']})", f"chybí {s[jazyk]}index.html")
                continue
            if s["hotovo"] and not (WEB / s[jazyk].strip("/") / "ai.txt").exists():
                chyba(s[jazyk], "chybí ai.txt")

    for rozcestnik, jazyk in ((WEB / "wiki/index.html", "cs"), (WEB / "en/wiki/index.html", "en")):
        text = rozcestnik.read_text(encoding="utf-8")
        karet = len(re.findall(r'<a class="wiki-karta"', text))
        if karet != len(hotovych):
            chyba(str(rozcestnik.relative_to(WEB)), f"dlaždic {karet}, hotových stránek {len(hotovych)}")
        # vlastník 17. 10. 2026: odznak „HOTOVÁ / DONE“ na dlaždicích nemá být
        if "wiki-stav--hotovo" in text or re.search(r"✅ (hotová|done)", text):
            chyba(str(rozcestnik.relative_to(WEB)), "na dlaždicích je odznak „hotová/DONE“ (nemá tam být)")


# --------------------------------------------------------------- 6. verze
def test_verze() -> None:
    vzory = {
        "style.css": re.compile(r"style\.css\?v=[0-9-]+"),
        "wiki.css": re.compile(r"wiki\.css\?v=[0-9-]+"),
        "script.js": re.compile(r"script\.js\?v=[a-z0-9-]+"),
        "zive.js": re.compile(r"zive\.js\?v=[a-z0-9-]+"),
        "matomo.js": re.compile(r"matomo\.js\?v=[a-z0-9-]+"),
    }
    bez_verze = 0
    for p in html_soubory():
        text = p.read_text(encoding="utf-8", errors="replace")
        for nazev, vzor in vzory.items():
            if f"/assets/{nazev}" in text and not vzor.search(text):
                chyba(str(p.relative_to(WEB)), f"{nazev} bez verze ?v=")
                bez_verze += 1
    POCTY["souborů bez verze"] = bez_verze


# --------------------------------------------------------------- 7. soubory pro roboty
def test_textove_soubory() -> None:
    for nazev in ("robots.txt", "sitemap.xml", "llms.txt"):
        if not (WEB / nazev).is_file():
            chyba(nazev, "chybí")
    for ai in (WEB / "wiki/funkce/hlas/ai.txt", WEB / "en/wiki/features/voice/ai.txt"):
        if ai.is_file() and not ai.read_bytes().startswith(b"\xef\xbb\xbf"):
            chyba(str(ai.relative_to(WEB)), "chybí značka UTF-8 (BOM)")


# ------------------------------------------------------------- 8. měření
def test_mereni() -> None:
    """Matomo i GA4 musí být na každé stránce právě jednou — jinak jsou data děravá."""
    chybi, duplicitni, inline = [], [], []
    for p in html_soubory():
        h = p.read_text(encoding="utf-8")
        for nazev, vzor in (("matomo.js", "assets/matomo.js"), ("ga4.js", "assets/ga4.js")):
            kolik = h.count(vzor)
            if kolik == 0:
                chybi.append(f"{p.relative_to(WEB)}: {nazev}")
            elif kolik > 1:
                duplicitni.append(f"{p.relative_to(WEB)}: {nazev} ×{kolik}")
        if "googletagmanager.com/gtag/js" in h:
            inline.append(str(p.relative_to(WEB)))
    for c in chybi[:10]:
        chyba("měření", f"chybí {c}")
    for c in duplicitni[:10]:
        chyba("měření", f"dvakrát {c}")
    for c in inline[:10]:
        chyba("měření", f"starý vložený GA4 blok v {c} (patří do /assets/ga4.js)")
    vadne = {c.split(":")[0] for c in chybi + duplicitni} | set(inline)
    POCTY["stránek s Matomo i GA4"] = len(html_soubory()) - len(vadne)


# --------------------------------------------------------------- 8. živý web
def _kod(url: str) -> tuple[str, str]:
    r = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "20", url],
        capture_output=True, text=True)
    return url, (r.stdout or "000").strip()


def test_zivy_web() -> None:
    adresy = sitemap_adresy()
    with ThreadPoolExecutor(max_workers=8) as ex:
        vysledky = list(ex.map(_kod, adresy))
    spatne = [(u, k) for u, k in vysledky if k != "200"]
    POCTY["živě kontrolovaných adres"] = len(adresy)
    POCTY["živých adres bez 200"] = len(spatne)
    for u, k in spatne:
        chyba(u, f"HTTP {k}")

    # interní soubory nesmí být veřejné
    zavrene = ["/audit.md", "/redesing/PLAN.md", "/wiki-zdroj/aktualizuj.py", "/README.md"]
    for cesta in zavrene:
        _, kod = _kod(DOMENA + cesta)
        if kod != "404":
            chyba(cesta, f"interní soubor je veřejný (HTTP {kod})")

    # textové soubory se musí hlásit jako UTF-8
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-D", "-", DOMENA + "/sitemap.xml"],
                       capture_output=True, text=True)
    if "charset=utf-8" not in r.stdout.lower():
        chyba("/sitemap.xml", f"chybí charset v hlavičce: {r.stdout.splitlines()[:1]}")
    r = subprocess.run(["curl", "-s", DOMENA + "/wiki/funkce/hlas/ai.txt"], capture_output=True, text=True)
    if "Hlasový režim" not in r.stdout:
        chyba("/wiki/funkce/hlas/ai.txt", "obsah se nenačetl nebo je rozsypaný")


def main() -> int:
    parser = argparse.ArgumentParser(description="Testy webu hermes-ai.cz")
    parser.add_argument("--jen-disk", action="store_true", help="vynechat dotazy na živý web")
    args = parser.parse_args()

    testy = [
        ("1. nevyvážené značky", test_znacky),
        ("2. odkazy a soubory", test_odkazy),
        ("3. hreflang dvojice", test_hreflang),
        ("4. sitemapa", test_sitemapa),
        ("5. wiki a dlaždice", test_wiki),
        ("6. verze vzhledu", test_verze),
        ("7. soubory pro roboty", test_textove_soubory),
        ("8. měření na všech stránkách", test_mereni),
    ]
    if not args.jen_disk:
        testy.append(("9. živý web", test_zivy_web))

    for nazev, funkce in testy:
        pred = len(CHYBY)
        try:
            funkce()
        except Exception as e:  # test sám nesmí spadnout
            chyba(nazev, f"test selhal: {type(e).__name__}: {e}")
        stav = "✅" if len(CHYBY) == pred else f"❌ ({len(CHYBY) - pred} chyb)"
        print(f"{stav:12s} {nazev}")

    print()
    for klic, hodnota in POCTY.items():
        print(f"  {klic}: {hodnota}")
    if VAROVANI:
        print("\nVarování:")
        for v in VAROVANI:
            print("  ⚠", v)
    if CHYBY:
        print(f"\n❌ CHYBY ({len(CHYBY)}):")
        for c in CHYBY[:40]:
            print("  •", c)
        if len(CHYBY) > 40:
            print(f"  … a dalších {len(CHYBY) - 40}")
        return 1
    print("\n✅ Vše v pořádku.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
