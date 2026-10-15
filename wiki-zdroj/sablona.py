"""Společné části stránek wiki — aby všechny vypadaly stejně a nedělaly se ručně chyby.

Používá se takto:
    from sablona import stranka_html, uloz, uloz_ai, karty_html, faze_html
"""
from __future__ import annotations

import json
import re
from pathlib import Path

WEB = Path("/var/www/hermesagent")
ZDROJ = WEB / "wiki-zdroj"
DATA = json.loads((ZDROJ / "stranky.json").read_text(encoding="utf-8"))
STRANKY: list[dict] = DATA["stranky"]
FAZE: list[dict] = DATA["faze"]
OG = "https://hermes-ai.cz/assets/redesign/images/hero/hero-ai-agent-approved.webp"
VERZE_CSS = "20261015-4"
VERZE_SK = "20261015-2"


def hotove(jazyk: str) -> list[dict]:
    return [s for s in STRANKY if s["hotovo"]]


def najdi(slug_nebo_cislo) -> dict | None:
    for s in STRANKY:
        if s["cislo"] == slug_nebo_cislo or s["cs"] == slug_nebo_cislo or s["en"] == slug_nebo_cislo:
            return s
    return None


# ------------------------------------------------------------------ části stránky
def _ze_vzoru(jazyk: str, klic: str) -> str:
    cesta = WEB / (("en/faq/index.html") if jazyk == "en" else "faq/index.html")
    t = cesta.read_text(encoding="utf-8")
    oteviraci, zaviraci = f"<{klic}", f"</{klic}>"
    return t[t.find(oteviraci):t.find(zaviraci) + len(zaviraci)]


def hlavicka(jazyk: str) -> str:
    """Horní lišta — bere se z hotové stránky webu, aby byla vždy stejná."""
    return _ze_vzoru(jazyk, "header")


def paticka(jazyk: str) -> str:
    return _ze_vzoru(jazyk, "footer")


def hlava(jazyk: str, titulek: str, popis: str, cs_url: str, en_url: str, hero: str | None) -> str:
    preload = ""
    if hero:
        preload = (
            f'<link rel="preload" as="image" href="/assets/redesign/images/sections/{hero}-hero.webp?v=20261015-1" media="(min-width: 821px)" fetchpriority="high">'
            f'<link rel="preload" as="image" href="/assets/redesign/images/sections/{hero}_hero_mobile_768x960.webp?v=20261015-1" media="(max-width: 820px)" fetchpriority="high">'
        )
    return f'''<!doctype html><html lang="{jazyk}" data-theme="dark"><head><meta charset="utf-8"><script>(function(){{try{{localStorage.removeItem("theme");localStorage.removeItem("hermes_theme");}}catch(e){{}}}})();</script><meta name="color-scheme" content="dark"><meta name="theme-color" content="#061020"><style>html{{background:#061020;color:#f8fafc;color-scheme:dark}}body{{margin:0;background:#061020;color:#f8fafc}}</style><meta name="viewport" content="width=device-width, initial-scale=1"><title>{titulek}</title><meta name="description" content="{popis}"><meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large"><link rel="canonical" href="https://hermes-ai.cz{cs_url if jazyk == "cs" else en_url}"><link rel="alternate" hreflang="cs" href="https://hermes-ai.cz{cs_url}"><link rel="alternate" hreflang="en" href="https://hermes-ai.cz{en_url}"><link rel="alternate" hreflang="x-default" href="https://hermes-ai.cz{cs_url}"><meta property="og:title" content="{titulek}"><meta property="og:description" content="{popis}"><meta property="og:url" content="https://hermes-ai.cz{cs_url if jazyk == "cs" else en_url}"><meta property="og:type" content="article"><meta property="og:site_name" content="Hermes AI"><meta property="og:image" content="{OG}"><link rel="icon" type="image/svg+xml" href="/assets/redesign/logos/hermes-ai-symbol.svg"><link rel="preload" as="font" type="font/woff2" href="/assets/redesign/fonts/Inter-web.woff2" crossorigin>{preload}<link rel="stylesheet" href="/assets/redesign/style.css?v=20261015-20"><link rel="stylesheet" href="/assets/redesign/wiki.css?v={VERZE_CSS}"><link rel="manifest" href="/assets/redesign/logos/manifest.json?v=20261015"><link rel="apple-touch-icon" sizes="180x180" href="/assets/redesign/logos/apple-touch-icon-180.png"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="Hermes AI"><meta name="application-name" content="Hermes AI"><meta name="seznam-wmt" content="uQSQdFRdQoVYGXVnuxQVlUk1CwxslRXE"><script defer src="/assets/matomo.js?v=20261015b"></script></head><body>'''


def hero(obrazek: str | None, eyebrow: str, nadpis: str, lead: str) -> str:
    if not obrazek:
        return (f'<section class="route-hero" aria-labelledby="route-title"><div class="route-hero__copy">'
                f'<p class="eyebrow">{eyebrow}</p><h1 id="route-title">{nadpis}</h1><p class="lead">{lead}</p></div></section>')
    return (f'<section class="route-hero route-hero--poster" aria-labelledby="route-title">'
            f'<picture aria-hidden="true"><source media="(max-width: 820px)" '
            f'srcset="/assets/redesign/images/sections/{obrazek}_hero_mobile_768x960.webp?v=20261015-1" width="768" height="960">'
            f'<img class="route-hero--poster__bg" src="/assets/redesign/images/sections/{obrazek}-hero.webp?v=20261015-1" '
            f'alt="" width="1920" height="700" fetchpriority="high"></picture>'
            f'<div class="route-hero__copy"><p class="eyebrow">{eyebrow}</p><h1 id="route-title">{nadpis}</h1>'
            f'<p class="lead">{lead}</p></div></section>')


def bocni(jazyk: str, aktivni_url: str) -> str:
    """Postranní nabídka — staví se z jednoho seznamu, takže je všude stejná."""
    titulek = "Wiki — start here" if jazyk == "en" else "Wiki — začínáme"
    r = [f'<aside class="wiki-side" aria-label="{"Wiki contents" if jazyk == "en" else "Obsah wiki"}">'
         f'<details class="wiki-obsah" open><summary>{titulek}</summary><nav>']
    for s in STRANKY:
        nazev = s["nazev_en"] if jazyk == "en" else s["nazev"]
        url = s["en"] if jazyk == "en" else s["cs"]
        if not s["hotovo"]:
            r.append(f'<span class="pripravujeme">{nazev}</span>')
        elif url == aktivni_url:
            r.append(f'<a href="{url}" aria-current="page">{nazev}</a>')
        else:
            r.append(f'<a href="{url}">{nazev}</a>')
    odkaz = "/en/wiki/" if jazyk == "en" else "/wiki/"
    text = ("Written in Czech and English from the official docs — with Czech pricing, providers and our own experience added."
            if jazyk == "en" else
            "Wiki píšeme podle oficiální dokumentace, ale s českými reálniemi a našimi zkušenostmi.")
    text = text.replace("reálniemi", "reáliemi")
    r.append(f'</nav></details><p>{text} <a href="{odkaz}">{"How the wiki works →" if jazyk == "en" else "Jak je wiki uspořádaná →"}</a></p></aside>')
    return "".join(r)


def meta(jazyk: str, overeno: str, oficialni: str, ai_soubor: str = "ai.txt") -> str:
    if jazyk == "cs":
        return (f'<div class="wiki-meta"><span>✅ Ověřeno {overeno}</span>'
                f'<span>Zdroj: <a href="{oficialni}" target="_blank" rel="noopener">oficiální dokumentace →</a></span>'
                f'<a class="wiki-ai" href="{ai_soubor}">📋 Zkopírovat pro AI</a></div>')
    return (f'<div class="wiki-meta"><span>✅ Verified {overeno}</span>'
            f'<span>Source: <a href="{oficialni}" target="_blank" rel="noopener">official documentation →</a></span>'
            f'<a class="wiki-ai" href="{ai_soubor}">📋 Copy for your AI</a></div>')


def stranka_html(jazyk: str, stranka: dict, titulek: str, popis: str, obrazek: str | None,
                 eyebrow: str, nadpis: str, lead: str, telo: str, overeno: str, oficialni: str) -> str:
    url = stranka["en"] if jazyk == "en" else stranka["cs"]
    obsah = (hero(obrazek, eyebrow, nadpis, lead) +
             f'<div class="container wiki-layout">{bocni(jazyk, url)}<article>'
             + meta(jazyk, overeno, oficialni) + telo + "</article></div>")
    skripty = (f'<script src="/assets/redesign/wiki.js?v={VERZE_SK}" defer></script>'
               f'<script src="/assets/script.js?v=redesign-5"></script>'
               f'<script src="/assets/zive.js?v=5" defer></script>')
    return (hlava(jazyk, titulek, popis, stranka["cs"], stranka["en"], obrazek) + hlavicka(jazyk)
            + '<main class="page-shell"><div class="container page-content">' + obsah + "</div></main>"
            + paticka(jazyk) + skripty + "</body></html>")


def uloz(jazyk: str, stranka: dict, html: str) -> Path:
    cesta = WEB / (stranka["en"] if jazyk == "en" else stranka["cs"]).strip("/")
    cesta = WEB / cesta
    cesta.mkdir(parents=True, exist_ok=True)
    (cesta / "index.html").write_text(html, encoding="utf-8")
    return cesta


def uloz_ai(jazyk: str, stranka: dict, osnova: str, overeno: str, oficialni: str, telo_md: str) -> Path:
    cesta = WEB / (stranka["en"] if jazyk == "en" else stranka["cs"]).strip("/")
    web_url = f"https://hermes-ai.cz{stranka['en'] if jazyk == 'en' else stranka['cs']}"
    hlavicka_md = (
        f"# {osnova}\n\n"
        f"Zdroj: {web_url}\n"
        f"Ověřeno proti oficiální dokumentaci: {overeno}\n"
        f"Oficiální stránka: {oficialni}\n"
        + ("Jazyk: čeština. Verze pro AI — zkopírujte celý text svému agentovi.\n\n"
           if jazyk == "cs" else
           "Language: English. AI version — paste the whole text into your agent.\n\n"))
    (cesta / "ai.txt").write_text(hlavicka_md + telo_md.strip() + "\n", encoding="utf-8")
    return cesta


# ------------------------------------------------------------------ rozcestník
def karty_html(jazyk: str) -> str:
    r = ['<div class="wiki-karty">']
    for s in STRANKY:
        nazev = s["nazev_en"] if jazyk == "en" else s["nazev"]
        popis = s["popis_en"] if jazyk == "en" else s["popis"]
        url = s["en"] if jazyk == "en" else s["cs"]
        if s["hotovo"]:
            stav = "✅ done" if jazyk == "en" else "✅ hotová"
            r.append(f'<a class="wiki-karta" href="{url}"><span class="wiki-karta__cislo">{s["cislo"]}</span>'
                     f'<span><h3>{nazev}</h3><p>{popis}</p><span class="wiki-stav wiki-stav--hotovo">{stav}</span></span></a>')
        else:
            stav = "⏳ in progress" if jazyk == "en" else "⏳ připravujeme"
            r.append(f'<span class="wiki-karta wiki-karta--ceka"><span class="wiki-karta__cislo">{s["cislo"]}</span>'
                     f'<span><h3>{nazev}</h3><p>{popis}</p><span class="wiki-stav wiki-stav--ceka">{stav}</span></span></span>')
    r.append("</div>")
    return "".join(r)


def faze_html(jazyk: str) -> str:
    r = ['<div class="wiki-faze">']
    for f in FAZE:
        nazev = f["nazev_en"] if jazyk == "en" else f["nazev"]
        popis = f["popis_en"] if jazyk == "en" else f["popis"]
        odkaz = f["odkaz_en"] if jazyk == "en" else f["odkaz"]
        cil = f' href="{odkaz}"' if odkaz else ' href="#pripravujeme"'
        r.append(f'<a{cil}><strong>{nazev}</strong><span>{popis}</span></a>')
    r.append("</div>")
    return "".join(r)
