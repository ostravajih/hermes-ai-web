#!/usr/bin/env python3
"""Stáhne oficiální dokumentaci Hermes Agenta a připraví podklad pro českou wiki.

Co dělá:
  1. stáhne index (llms.txt) a celý obsah (llms-full.txt) z oficiální dokumentace
  2. rozdělí celý obsah na jednotlivé stránky (v souboru je u každé značka
     `<!-- source: website/docs/… -->`)
  3. u každé stránky spočítá otisk (SHA-256) a uloží přehled do `prehled.json`
  4. porovná s předchozím během a vypíše, které stránky jsou NOVÉ nebo ZMĚNĚNÉ
  5. uloží jednotlivé stránky do `stranky/<slug>.md`, aby se z nich dalo překládat

Použití:
  python3 wiki-zdroj/nacist-dokumentaci.py            # stáhne, porovná, zapíše
  python3 wiki-zdroj/nacist-dokumentaci.py --kontrola # jen vypíše, co se změnilo

Výstup (vše mimo veřejný web — nginx složku `wiki-zdroj/` blokuje):
  wiki-zdroj/llms.txt, wiki-zdroj/llms-full.txt
  wiki-zdroj/prehled.json
  wiki-zdroj/stranky/<slug>.md
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ZAKLAD = Path(__file__).resolve().parent
INDEX_URL = "https://hermes-agent.nousresearch.com/docs/llms.txt"
PLNY_URL = "https://hermes-agent.nousresearch.com/docs/llms-full.txt"

SEKCE_VZOR = re.compile(r"(?m)^##\s+(.+?)\s*$")
STRANKA_VZOR = re.compile(r"(?m)^-\s+\[([^\]]+)\]\((\S+?)\)(?::\s*(.*))?$")
ZDROJ_VZOR = re.compile(r"<!--\s*source:\s*(\S+?)\s*-->\s*\n#\s+(.+?)\s*\n", re.S)


def stahni(url: str) -> str:
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read().decode("utf-8")


def slug_z_cesty(cesta: str) -> str:
    """website/docs/getting-started/installation.md → zaciname/installation (sekce/stránka)."""
    c = re.sub(r"^.*?/docs/", "", cesta)
    c = re.sub(r"\.md$", "", c)
    return c.replace("/", "-") or "index"


def main() -> int:
    kontrola = "--kontrola" in sys.argv
    print("Stahuji index a celý obsah oficiální dokumentace…")
    index = stahni(INDEX_URL)
    plny = stahni(PLNY_URL)
    print(f"  index: {len(index):,} znaků | celý obsah: {len(plny):,} znaků")

    # sekce + stránky z indexu (popisky a pořadí)
    sekce, popisky, poradi = None, {}, []
    for radek in index.splitlines():
        m = SEKCE_VZOR.match(radek)
        if m:
            sekce = m.group(1).strip()
            continue
        m = STRANKA_VZOR.match(radek)
        if m and sekce:
            nazev, url, popis = m.group(1), m.group(2), (m.group(3) or "").strip()
            popisky[url] = (sekce, nazev, popis)
            poradi.append(url)

    # rozdělení celého obsahu na stránky
    stranky, otisky = {}, {}
    casti = re.split(r"(?=<!--\s*source:)", plny)
    for cast in casti:
        m = re.match(r"<!--\s*source:\s*(\S+?)\s*-->\s*\n#\s+(.+?)\s*\n", cast, re.S)
        if not m:
            continue
        cesta, nazev = m.group(1), m.group(2).strip()
        slug = slug_z_cesty(cesta)
        telo = cast.strip()
        stranky[slug] = {"cesta_zdroje": cesta, "nazev": nazev, "telo": telo}
        otisky[slug] = hashlib.sha256(telo.encode("utf-8")).hexdigest()[:16]

    # porovnání s předchozím během
    stary: dict = {}
    soubor_prehled = ZAKLAD / "prehled.json"
    if soubor_prehled.exists():
        stary = json.loads(soubor_prehled.read_text(encoding="utf-8")).get("stranky", {})

    nove, zmenene, stejne = [], [], 0
    for slug, info in stranky.items():
        if slug not in stary:
            nove.append(slug)
        elif stary[slug].get("otisk") != otisky[slug]:
            zmenene.append(slug)
        else:
            stejne += 1

    # přehled
    podle_sekce: dict = {}
    for slug, info in stranky.items():
        popis = popisky.get(f"https://hermes-agent.nousresearch.com/docs/{info['cesta_zdroje'].split('/docs/', 1)[-1][:-3]}", None)
        sek = popis[0] if popis else "Ostatní"
        preklad = stary.get(slug, {}).get("prelozeno", False)
        podle_sekce.setdefault(sek, []).append({
            "slug": slug,
            "nazev": info["nazev"],
            "cesky_nazev": stary.get(slug, {}).get("cesky_nazev", ""),
            "cesta_zdroje": info["cesta_zdroje"],
            "otisk": otisky[slug],
            "znaku": len(info["telo"]),
            "prelozeno": preklad,
            "stav": "nove" if slug in nove else ("zmenene" if slug in zmenene else "stejne"),
        })

    prehled = {
        "stazeno": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "index_url": INDEX_URL,
        "pocet_stranek": len(stranky),
        "sekce": podle_sekce,
        "stranky": {s: {"otisk": otisky[s], "nazev": stranky[s]["nazev"],
                        "prelozeno": stary.get(s, {}).get("prelozeno", False),
                        "cesky_nazev": stary.get(s, {}).get("cesky_nazev", "")}
                    for s in sorted(stranky)},
    }

    print(f"\nStránek v oficiální dokumentaci: {len(stranky)}")
    for sek in podle_sekce:
        print(f"  {sek:26s} {len(podle_sekce[sek]):3d}")
    print(f"\nZměny proti minulému běhu: {len(nove)} nových, {len(zmenene)} změněných, {stejne} beze změny")

    hotove = [s for s in stranky if stary.get(s, {}).get("prelozeno")]
    if hotove:
        ke_kontrole = [s for s in hotove if s in nove or s in zmenene]
        print(f"Přeložených stránek: {len(hotove)} | z toho k revizi: {len(ke_kontrole)}")
        for s in ke_kontrole:
            print(f"   ⚠️  {s} — {stranky[s]['nazev']}")
    if nove[:8]:
        print("Nové stránky (vzorek): " + ", ".join(nove[:8]))

    if kontrola:
        print("\n(--kontrola: nic se nezapsalo)")
        return 0

    (ZAKLAD / "llms.txt").write_text(index, encoding="utf-8")
    (ZAKLAD / "llms-full.txt").write_text(plny, encoding="utf-8")
    soubor_prehled.write_text(json.dumps(prehled, ensure_ascii=False, indent=1), encoding="utf-8")
    (ZAKLAD / "stranky").mkdir(exist_ok=True)
    for slug, info in stranky.items():
        (ZAKLAD / "stranky" / f"{slug}.md").write_text(info["telo"], encoding="utf-8")
    print(f"✅ zapsáno: prehled.json + {len(stranky)} stránek do wiki-zdroj/stranky/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
