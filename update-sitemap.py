#!/usr/bin/env python3
"""Aktualizuje <lastmod> v sitemap.xml podle skutečného data změny souboru.

Proč: ručně psané datum v sitemapě zastará (naposledy ukazovalo 12. 10., ačkoli
se web měnil 15. 10.). Tohle bere datum z poslední změny souboru na disku, takže
je vždy pravdivé. Ostatní údaje (pořadí, changefreq, priority) zůstávají.

Použití:  python3 update-sitemap.py [--kontrola]
          --kontrola = nic nezapisuje, jen vypíše, co by se změnilo
"""
import os
import re
import sys
from datetime import date
from pathlib import Path

WEB = Path(__file__).resolve().parent
SITEMAP = WEB / "sitemap.xml"
DOMENA = "https://hermes-ai.cz"


def soubor_pro_url(url: str) -> Path | None:
    """Převede adresu na soubor na disku (adresář = index.html)."""
    if not url.startswith(DOMENA):
        return None
    cesta = url[len(DOMENA):].split("?")[0].split("#")[0]
    cil = WEB / cesta.lstrip("/")
    if cesta.endswith("/") or cesta == "":
        cil = cil / "index.html"
    if cil.is_dir():
        cil = cil / "index.html"
    return cil if cil.is_file() else None


def main() -> int:
    kontrola = "--kontrola" in sys.argv
    obsah = SITEMAP.read_text(encoding="utf-8")
    zmeny = []
    chybejici = []

    def zpracuj_zaznam(m):
        zaznam = m.group(0)
        loc = re.search(r"<loc>([^<]+)</loc>", zaznam)
        if not loc:
            return zaznam
        url = loc.group(1)
        soubor = soubor_pro_url(url)
        if soubor is None:
            chybejici.append(url)
            return zaznam
        nove = date.fromtimestamp(soubor.stat().st_mtime).isoformat()
        stare_m = re.search(r"<lastmod>([^<]+)</lastmod>", zaznam)
        stare = stare_m.group(1) if stare_m else None
        if stare == nove:
            return zaznam
        zmeny.append((url, stare, nove))
        if stare_m:
            return zaznam[: stare_m.start()] + f"<lastmod>{nove}</lastmod>" + zaznam[stare_m.end():]
        # záznam bez lastmod → vložíme ho hned za <loc>
        return zaznam[: loc.end()] + f"<lastmod>{nove}</lastmod>" + zaznam[loc.end():]

    novy = re.sub(r"<url>.*?</url>", zpracuj_zaznam, obsah, flags=re.S)

    print(f"adres v sitemapě: {len(re.findall(r'<loc>', obsah))}")
    print(f"změněných lastmod: {len(zmeny)}")
    for url, stare, nove in zmeny[:6]:
        print(f"   {url.replace(DOMENA, '') or '/':44s} {stare} → {nove}")
    if len(zmeny) > 6:
        print(f"   … a další {len(zmeny) - 6}")
    if chybejici:
        print(f"⚠️  adresy bez souboru na disku ({len(chybejici)}):")
        for u in chybejici[:8]:
            print("   ", u)

    if kontrola:
        print("(--kontrola: nic se nezapsalo)")
        return 0
    if novy != obsah:
        SITEMAP.write_text(novy, encoding="utf-8")
        print("✅ sitemap.xml zapsána")
    else:
        print("✅ sitemap.xml beze změny")
    return 0


if __name__ == "__main__":
    sys.exit(main())
