#!/usr/bin/env python3
"""Fronta změn oficiální dokumentace — fáze 4 (wiki v souladu s dokumentací).

Co dělá:
  1. zapamatuje si staré otisky z `prehled.json`
  2. stáhne oficiální dokumentaci (`nacist-dokumentaci.py`) — nové otisky + snímky stránek
  3. porovná otisky a vypíše, co se změnilo, přibylo nebo zmizelo
  4. přeloží to na **naše** stránky wiki pomocí `zdroje.json` (která stránka dokumentace
     se týká které stránky wiki)
  5. zapíše `wiki-zdroj/fronta-zmen.md` (lidsky čitelná fronta) a `.json` (pro skripty)

Použití:
  python3 wiki-zdroj/fronta-zmen.py              # stáhne, porovná, zapíše frontu
  python3 wiki-zdroj/fronta-zmen.py --bez-site   # jen přečte poslední frontu a vypíše ji
  python3 wiki-zdroj/fronta-zmen.py --tise       # bez výpisu, jen zápis (pro cron)

Výstupní kód: 0 = hotovo (i když se něco změnilo), 1 = nepodařilo se stáhnout dokumentaci.

Fronta se NEAKTUALIZUJE sama na webu — jen řekne, co je potřeba přečíst a doplnit.
Stránky wiki mají v hlavičce „✅ Ověřeno <datum>“ a odkaz na zdroj, takže je vidět, co zestaralo.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ZAKLAD = Path(__file__).resolve().parent
PREHLED = ZAKLAD / "prehled.json"
ZDROJE = ZAKLAD / "zdroje.json"
STRANKY = ZAKLAD / "stranky.json"
FRONTA_MD = ZAKLAD / "fronta-zmen.md"
FRONTA_JSON = ZAKLAD / "fronta-zmen.json"
NAZEV_DOKUMENTACE = "https://hermes-agent.nousresearch.com/docs"


def nacti(cesta: Path, vychozi=None):
    if cesta.exists():
        return json.loads(cesta.read_text(encoding="utf-8"))
    if vychozi is not None:
        return vychozi
    raise SystemExit(f"❌ chybí {cesta.relative_to(ZAKLAD.parent)} — nejdřív spusťte nacist-dokumentaci.py")


def stranky_podle_cisla() -> dict[str, dict]:
    data = nacti(STRANKY)
    return {str(s["cislo"]): s for s in data["stranky"]}


def opacna_mapa() -> dict[str, list[str]]:
    """slug dokumentace → seznam čísel našich wiki stránek."""
    mapa: dict[str, list[str]] = {}
    for cislo, slugy in nacti(ZDROJE)["zdroje"].items():
        for slug in slugy:
            mapa.setdefault(slug, []).append(cislo)
    return mapa


def stahni_dokumentaci() -> bool:
    skript = ZAKLAD / "nacist-dokumentaci.py"
    r = subprocess.run([sys.executable, str(skript)], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-800:])
        print(r.stderr[-800:], file=sys.stderr)
        return False
    return True


def zalohuj_snimky() -> Path:
    """Záloha snímků před stažením — bez ní by se změny daly zjistit, ale ne přečíst."""
    import shutil

    stara = ZAKLAD / ".predchozi-snimky"
    if stara.exists():
        shutil.rmtree(stara)
    stara.mkdir(parents=True)
    zdroj = ZAKLAD / "stranky"
    if zdroj.exists():
        for soubor in zdroj.glob("*.md"):
            (stara / soubor.name).write_text(soubor.read_text(encoding="utf-8"), encoding="utf-8")
    return stara


def uloz_rozdily(slugy: list[str], stara_kopiev: Path, dnesni: str) -> dict[str, str]:
    """Uloží diff staré a nové verze stránek dokumentace — aby se fronta dala opravdu přečíst."""
    import difflib

    cil = ZAKLAD / "zmeny" / dnesni
    vysledek: dict[str, str] = {}
    for slug in slugy:
        stara = stara_kopiev / f"{slug}.md"
        nova = ZAKLAD / "stranky" / f"{slug}.md"
        if not nova.exists():
            continue
        stary_text = stara.read_text(encoding="utf-8").splitlines() if stara.exists() else []
        novy_text = nova.read_text(encoding="utf-8").splitlines()
        diff = list(difflib.unified_diff(stary_text, novy_text, fromfile=f"{slug} (minule)",
                                         tofile=f"{slug} (nyní)", lineterm="", n=2))
        if not diff:
            continue
        cil.mkdir(parents=True, exist_ok=True)
        cesta = cil / f"{slug}.diff"
        cesta.write_text("\n".join(diff) + "\n", encoding="utf-8")
        vysledek[slug] = str(cesta.relative_to(ZAKLAD.parent))
    return vysledek



def obnov_z_diffu(datum: str) -> int:
    """Znovu postaví frontu z rozdílů uložených v `zmeny/<datum>/` (bez stahování)."""
    cil = ZAKLAD / "zmeny" / datum
    if not cil.exists():
        print(f"❌ wiki-zdroj/zmeny/{datum} neexistuje")
        return 1
    zmenene = sorted(p.stem for p in cil.glob("*.diff"))
    if not zmenene:
        print("❌ v té složce nejsou žádné rozdíly")
        return 1
    nove = nacti(PREHLED).get("stranky", {})
    rozdily = {s: str((cil / f"{s}.diff").relative_to(ZAKLAD.parent)) for s in zmenene}
    zpet, stranky = opacna_mapa(), stranky_podle_cisla()
    tyka_se = [s for s in zmenene if zpet.get(s)]
    radky = [f"# Fronta změn — {datum}", "",
             f"Obnoveno ze {len(zmenene)} uložených rozdílů (bez stahování dokumentace).", "",
             "## Co se týká našich stránek", "",
             "| Dokumentace | Co se stalo | Naše stránka | Rozdíl |", "|---|---|---|---|"]
    for slug in tyka_se:
        odkazy = " · ".join(f"[{stranky[c]['nazev']}]({stranky[c]['cs']})"
                            for c in sorted(zpet[slug], key=int) if c in stranky)
        radky.append(f"| `{slug}` | změněná | {odkazy} | `{rozdily[slug]}` |")
    radky += ["", "Postup u každé položky: přečíst rozdíl, doplnit text česky i anglicky, zvednout "
                  "`OVERENO` v obsahovém skriptu, spustit skript a `aktualizuj.py`.", ""]
    FRONTA_MD.write_text("\n".join(radky), encoding="utf-8")
    FRONTA_JSON.write_text(json.dumps({
        "kontrola": datetime.now().isoformat(timespec="seconds"), "den": datum,
        "obnoveno_z_rozdilu": True, "zmenene": zmenene, "rozdily": rozdily,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"✅ fronta obnovena z {len(zmenene)} rozdílů ({len(tyka_se)} se týká našich stránek)")
    return 0


def main() -> int:
    tise = "--tise" in sys.argv
    if "--z-diffu" in sys.argv:
        return obnov_z_diffu(sys.argv[sys.argv.index("--z-diffu") + 1])
    if "--bez-site" in sys.argv:
        if not FRONTA_MD.exists():
            print("Fronta zatím nevznikla — spusťte bez --bez-site.")
            return 0
        print(FRONTA_MD.read_text(encoding="utf-8"))
        return 0

    stare = nacti(PREHLED, {}).get("stranky", {})
    stara_kopiev = zalohuj_snimky()

    if not stahni_dokumentaci():
        print("❌ dokumentaci se nepodařilo stáhnout — fronta se nemění", file=sys.stderr)
        return 1

    nove = nacti(PREHLED)["stranky"]
    zmenene, nove_stranky, odebrane = [], [], []
    for slug, info in nove.items():
        if slug not in stare:
            nove_stranky.append(slug)
        elif stare[slug].get("otisk") != info.get("otisk"):
            zmenene.append(slug)
    for slug in stare:
        if slug not in nove:
            odebrane.append(slug)

    if not (zmenene or nove_stranky or odebrane):
        # Nic nového: frontu NEPŘEPISOVAT, jen poznamenat datum kontroly (otevřené položky zůstávají)
        fronta = nacti(FRONTA_JSON, {})
        fronta["posledni_kontrola"] = datetime.now().isoformat(timespec="seconds")
        fronta["stranek_dokumentace"] = len(nove)
        FRONTA_JSON.write_text(json.dumps(fronta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        if not tise:
            print(f"✅ zkontrolováno {datetime.now():%-d. %-m. %Y}: dokumentace beze změny "
                  f"({len(nove)} stránek) — fronta zůstává")
        return 0

    dnes_pro_adresar = datetime.now().strftime("%Y-%m-%d")
    rozdily = uloz_rozdily(zmenene + nove_stranky, stara_kopiev, dnes_pro_adresar)

    zpet = opacna_mapa()
    stranky = stranky_podle_cisla()
    nase: list[dict] = []
    for slug in zmenene + nove_stranky:
        cisla = sorted(zpet.get(slug, []), key=int)
        nase.append({
            "rozdil": rozdily.get(slug, ""),
            "dokumentace": slug,
            "nazev_dokumentace": nove[slug].get("nazev", slug),
            "druh": "změněná" if slug in zmenene else "nová v dokumentaci",
            "nase_stranky": [
                {"cislo": c, "nazev": stranky[c]["nazev"], "cs": stranky[c]["cs"], "en": stranky[c]["en"]}
                for c in cisla if c in stranky
            ],
        })

    tyka_se = [p for p in nase if p["nase_stranky"]]
    mimo = [p for p in nase if not p["nase_stranky"]]
    dnes = datetime.now().strftime("%-d. %-m. %Y")

    radky = [f"# Fronta změn — {dnes}", ""]
    radky.append(f"Oficiální dokumentace: {len(nove)} stránek · "
                 f"změněno **{len(zmenene)}** · nových **{len(nove_stranky)}** · odebraných **{len(odebrane)}**")
    radky.append("")
    if not tyka_se and not mimo and not odebrane:
        radky += ["**Nic se nezměnilo.** Wiki je v souladu s dokumentací.", ""]
    if tyka_se:
        radky += ["## Co se týká našich stránek", "",
                  "| Dokumentace | Co se stalo | Naše stránka | Rozdíl |", "|---|---|---|---|"]
        for p in tyka_se:
            odkazy = " · ".join(f"[{s['nazev']}]({s['cs']})" for s in p["nase_stranky"])
            rozdil = f"`{p['rozdil']}`" if p["rozdil"] else "—"
            radky.append(f"| `{p['dokumentace']}` | {p['druh']} | {odkazy} | {rozdil} |")
        radky += ["", "Postup: přečíst změnu, doplnit text česky i anglicky, zvednout „Ověřeno“ "
                      "v obsahovém skriptu (`OVERENO`), spustit skript a `aktualizuj.py`.", ""]
    if mimo:
        radky += ["## Změny mimo naši wiki", "",
                  "Těchto stránek dokumentace se naše wiki netýká — jen pro přehled:", ""]
        radky += [f"- `{p['dokumentace']}` ({p['druh']})" for p in mimo[:40]]
        if len(mimo) > 40:
            radky.append(f"- … a dalších {len(mimo) - 40}")
        radky.append("")
    if odebrane:
        radky += ["## Zaniklé stránky dokumentace", ""]
        radky += [f"- `{s}`" for s in odebrane]
        radky.append("")
        radky += ["Když některá z nich byla zdrojem naší stránky, je potřeba text přepsat podle "
                  "jiné stránky dokumentace nebo stránku zrušit.", ""]

    FRONTA_MD.write_text("\n".join(radky), encoding="utf-8")
    archiv = ZAKLAD / "zmeny" / dnes_pro_adresar
    archiv.mkdir(parents=True, exist_ok=True)
    (archiv / "fronta.md").write_text("\n".join(radky), encoding="utf-8")
    FRONTA_JSON.write_text(json.dumps({
        "kontrola": datetime.now().isoformat(timespec="seconds"),
        "stranek_dokumentace": len(nove),
        "zmenenych": zmenene,
        "novych": nove_stranky,
        "odebranych": odebrane,
        "tyka_se_nasich_stranek": tyka_se,
        "rozdily": rozdily,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    if not tise:
        print(f"✅ zkontrolováno {dnes}: {len(zmenene)} změněných + {len(nove_stranky)} nových "
              f"z {len(nove)} stránek dokumentace")
        if tyka_se:
            print(f"   ⚠️  týká se {len(tyka_se)} změn našich stránek — viz wiki-zdroj/fronta-zmen.md")
        else:
            print("   ✅ žádná změna se netýká našich stránek")
    return 0


if __name__ == "__main__":
    sys.exit(main())
