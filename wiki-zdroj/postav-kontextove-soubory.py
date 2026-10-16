#!/usr/bin/env python3
"""Postaví stránku wiki „Kontextové soubory" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-context-files.md (podporované soubory, pořadí
a priorita, načítání při startu i za běhu, limity, kontrola proti vloženým instrukcím),
wiki-zdroj/stranky/guides-use-soul-with-hermes.md (k čemu je SOUL.md, co do něj nepatří,
rozdíl proti AGENTS.md).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files"
OBRAZEK = "wiki-kontext"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📄</span><div><strong>Soubor s pravidly je nejrychlejší způsob, jak agentovi vysvětlit, jak u vás věci chodí — a nejrychlejší způsob, jak si ho zkazit.</strong>
Agent je čte při každé práci. Krátký a konkrétní soubor funguje; dlouhý se zkrátí a na část pravidel
se nedostane. Rozdíl je i v tom, kam co patří: <em>jak mluvit</em> do jednoho souboru,
<em>jak pracovat v projektu</em> do druhého.</div></div>

<h2>Dva různé soubory, dvě různé věci</h2>
<table class="wiki-tabulka">
<tr><th>Soubor</th><th>K čemu slouží</th><th>Kde leží</th></tr>
<tr><td><strong>SOUL.md</strong></td><td>Kdo agent je a jak mluví: tón, stručnost, přímost, čemu se vyhýbat. Platí všude</td><td><code>~/.hermes/SOUL.md</code> (jen tam, hledá se pouze v domovské složce Hermese)</td></tr>
<tr><td><strong>AGENTS.md</strong></td><td>Jak se pracuje v tomhle projektu: cesty, příkazy, konvence, co se nesmí</td><td>V projektu (kořen gitu a podsložky)</td></tr>
</table>
<p class="note">Jednoduché pravidlo: co má platit <strong>všude</strong>, patří do SOUL.md; co patří
<strong>jen jednomu projektu</strong>, do AGENTS.md. Když do SOUL.md napíšete porty a cesty konkrétního
projektu, budete to za měsíc hledat a mazat.</p>

<h2>Které soubory agent zná</h2>
<table class="wiki-tabulka">
<tr><th>Soubor</th><th>Význam</th></tr>
<tr><td><code>.hermes.md</code> / <code>HERMES.md</code></td><td>Pokyny k projektu s nejvyšší prioritou</td></tr>
<tr><td><code>AGENTS.override.md</code></td><td>Vaše osobní úprava k dané složce — obvykle se nedává do gitu, takže si můžete nastavit jiná pravidla, než jaká jsou ve sdíleném souboru</td></tr>
<tr><td><code>AGENTS.md</code></td><td>Pokyny k projektu, konvence, popis architektury</td></tr>
<tr><td><code>CLAUDE.md</code></td><td>Soubor z jiného nástroje, který Hermes taky rozpozná</td></tr>
<tr><td><code>.cursorrules</code>, <code>.cursor/rules/*.mdc</code></td><td>Pravidla z editoru Cursor — vaše stávající konvence se použijí i tady</td></tr>
<tr><td><code>SOUL.md</code></td><td>Osobní nastavení agenta; načítá se vždy a nezávisle na ostatních</td></tr>
</table>
<p><strong>Načte se jen jeden</strong> z projektových souborů — první nalezený v pořadí
<code>.hermes.md</code> → <code>AGENTS.override.md</code> → <code>AGENTS.md</code> →
<code>CLAUDE.md</code> → <code>.cursorrules</code>. Když tedy vedle sebe leží <code>AGENTS.md</code>
i <code>CLAUDE.md</code>, použije se <code>AGENTS.md</code> a ten druhý se ignoruje.
<code>SOUL.md</code> se k tomu přidává vždy jako identita agenta — to je ta výjimka.</p>

<h2>Kdy se soubory načtou</h2>
<table class="wiki-tabulka">
<tr><th>Kdy</th><th>Co se stane</th></tr>
<tr><td>Při spuštění</td><td>Hledá se v pracovní složce (a směrem ke kořeni gitu). Obsah se přečte, zkontroluje proti vloženým instrukcím a případně zkrátí</td></tr>
<tr><td>Během práce</td><td>Když agent sáhne na soubor v podsložce, přidají se pravidla z té složky a až pěti složek nad ní. Pro velké projekty se to hodí: každá část si nese vlastní pravidla</td></tr>
</table>
<p class="note">Díky tomu nemusíte mít jedno obří zadání pro celý projekt. Frontend má svá pravidla,
backend svá — a agent je dostane přesně v okamžiku, kdy v té složce začne pracovat.</p>

<h2>Limity, o kterých se vyplatí vědět</h2>
<table class="wiki-tabulka">
<tr><th>Limit</th><th>Hodnota</th></tr>
<tr><td>Největší délka souboru</td><td>Nastavitelná; jinak podle velikosti modelu (nejméně 20 tisíc znaků, nejvýš 500 tisíc)</td></tr>
<tr><td>Zkrácení příliš dlouhého souboru</td><td>Zachová se začátek (70 %) a konec (20 %), doprostřed se vloží značka s upozorněním</td></tr>
<tr><td>Čas na přečtení jednoho souboru</td><td>5 vteřin. Soubor na pomalém disku (iCloud, OneDrive, síťový disk) se může přeskočit s upozorněním</td></tr>
<tr><td>Prázdný SOUL.md</td><td>Nepřidá se vůbec nic — což je také volba</td></tr>
</table>
<div class="code-block"><span class="c"># takhle vypadá značka, když byl soubor zkrácen:</span>
[...zkráceno AGENTS.md: ponecháno 14000+4000 z 25000 znaků. Pro celý soubor použij nástroje pro práci se soubory.]</div>

<h2>Jak napsat soubor, který funguje</h2>
<table class="wiki-tabulka">
<tr><th>Zásada</th><th>Příklad z praxe</th></tr>
<tr><td>Krátce a konkrétně</td><td>Deset konkrétních pravidel funguje lépe než pět stran popisu</td></tr>
<tr><td>Pište i to, co se <strong>nesmí</strong></td><td>„Nikdy nepřidávej světlý režim, web je jen tmavý“ — bez toho si agent domýšlí</td></tr>
<tr><td>Uveďte příkazy a cesty, které má použít</td><td>Agent je pak nemusí hledat a nesplete si je</td></tr>
<tr><td>Nadpisy a odrážky</td><td>Agent se v souboru líp vyzná a vy v něm taky</td></tr>
<tr><td>Aktualizujte, když se projekt změní</td><td>Zastaralá pravidla jsou horší než žádná — agent se jimi řídí</td></tr>
</table>
<p>Nejjednodušší začátek: nechte agenta projít projekt a napsat první verzi, kterou si pak
upravíte.</p>
<div class="code-block"><span class="p">❯</span> Projdi tenhle projekt a navrhni AGENTS.md — jen to podstatné,
    co se má dodržovat: jak spouštět testy, kde co leží a co se nemá dělat.</div>

<h2>Pasti z našeho provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co se stalo</th><th>Co s tím</th></tr>
<tr><td><strong>Dlouhý soubor s pravidly se zkrátil a část zmizela</strong></td><td>Přesně proto držíme soubory krátké. Když je pravidlo důležité, ať je mezi prvními</td></tr>
<tr><td><strong>Dvě pravidla si odporovala</strong> (staré v AGENTS.md, nové v SOUL.md)</td><td>Agent se přiklonil k tomu, které čte dřív. Pravidla držte na jednom místě — osobnost do SOUL.md, práci do AGENTS.md</td></tr>
<tr><td><strong>Pravidla z podsložky přebila ta hlavní</strong></td><td>Počítejte s tím, že se soubory z podsložek přidávají za běhu. Když si odporují, vyhraje konkrétnější (bližší) soubor</td></tr>
<tr><td><strong>V projektu byl i CLAUDE.md a pravidla z něj se nepoužila</strong></td><td>Načte se jen jeden projektový soubor — ten s vyšší prioritou. Ostatní nechte smazané, nebo je slučte</td></tr>
<tr><td><strong>SOUL.md v projektu se ignoroval</strong></td><td>Správně: osobnost se bere jen z domovské složky Hermese. Do projektu patří AGENTS.md</td></tr>
<tr><td><strong>Soubor z náhodné změny v síťové složce se nepřečetl</strong></td><td>Přečtení má strop 5 vteřin. Pravidla držte lokálně, ne na pomalém disku</td></tr>
<tr><td><strong>Do souboru s pravidly jsme omylem vložili cizí text</strong> (například přepsaný obsah z webu)</td><td>Obsah se kontroluje proti vloženým instrukcím, ale spoléhejte na sebe: do souboru s pravidly patří jen to, co jste napsali vy</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Začněte třemi pravidly a přidávejte, až to bolí</td><td>Prázdný soubor je lepší než pětistránkový, který se zkrátí</td></tr>
<tr><td>Do SOUL.md napište, jak dlouhé odpovědi chcete</td><td>Jedna věta ušetří tisíce slov v každé odpovědi</td></tr>
<tr><td>Do AGENTS.md patří i „co nedělat“</td><td>Zákazy fungují líp než přání</td></tr>
<tr><td>Soubory držte v gitu spolu s projektem</td><td>Uvidíte, kdy a proč se pravidlo změnilo</td></tr>
<tr><td>Osobní úpravy dejte do <code>AGENTS.override.md</code></td><td>Nepřepíšete týmový soubor a vaše změna zůstane jen u vás</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/funkce/profily/"><strong>Profily a více agentů</strong><span>Každý profil má vlastní osobnost</span></a>
<a href="/wiki/funkce/nastroje/"><strong>Nástroje a toolsety</strong><span>Co agent umí a jak to ověřit</span></a>
<a href="/wiki/zaciname/instalace/"><strong>První konfigurace</strong><span>Průvodce instalací krok za krokem</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Kontextové soubory do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co je co
SOUL.md = kdo agent je a jak mluví (tón, stručnost, čemu se vyhýbat); platí všude; jen ~/.hermes/SOUL.md
(nebo $HERMES_HOME/SOUL.md). AGENTS.md = jak se pracuje v projektu (cesty, příkazy, konvence).
Obecné -> SOUL.md; projektové -> AGENTS.md.

## Podporované soubory
.hermes.md / HERMES.md (nejvyšší priorita) · AGENTS.override.md (osobní, obvykle negitovaná) ·
AGENTS.md · CLAUDE.md · .cursorrules / .cursor/rules/*.mdc · SOUL.md (vždy zvlášť jako identita).
Načte se jen JEDEN projektový soubor (první v tomto pořadí).

## Načítání
Při spuštění z pracovní složky (ke kořeni gitu). Za běhu se při práci v podsložce přidají pravidla
z ní a až 5 složek nad ní (jeden soubor na složku).

## Limity
Max délka: context_file_max_chars, jinak podle modelu (min 20 000, max 500 000 znaků).
Zkrácení: 70 % začátek + 20 % konec + značka 10 %.
Čas na přečtení souboru: 5 s (pomalé disky se přeskočí s upozorněním).
Prázdný SOUL.md = nepřidá se nic.

## Jak psát
Krátce a konkrétně · uvést i co se NESMÍ · příkazy, cesty, porty · nadpisy · aktualizovat.
Začátek: nechat agenta projít projekt a navrhnout první verzi.

## Pasti z našeho provozu
1. Dlouhý soubor se zkrátí -> důležitá pravidla nahoru, soubor krátký.
2. Protichůdná pravidla (AGENTS.md vs SOUL.md) -> agent si vybere podle pořadí; držet je oddělené.
3. Pravidla z podsložky přebijí hlavní -> konkrétnější vyhrává.
4. CLAUDE.md se ignoruje, když je v projektu AGENTS.md -> sloučit nebo smazat.
5. SOUL.md v projektu se ignoruje -> osobnost jen z domovské složky Hermese.
6. Soubor na síťovém disku se nepřečetl (limit 5 s) -> držet lokálně.
7. Cizí text v souboru s pravidly -> kontrola proti vloženým instrukcím existuje, ale spoléhat na sebe.

## Tipy
Začít se 3 pravidly · délka odpovědí do SOUL.md · "co nedělat" do AGENTS.md · soubory v gitu ·
osobní úpravy do AGENTS.override.md.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📄</span><div><strong>A rules file is the fastest way to explain to the agent how things work at your place — and the fastest way to ruin it.</strong>
The agent reads it on every task. A short, concrete file works; a long one gets truncated and some
rules never reach it. Where things belong matters too: <em>how to speak</em> goes in one file,
<em>how to work in a project</em> in another.</div></div>

<h2>Two different files, two different jobs</h2>
<table class="wiki-tabulka">
<tr><th>File</th><th>What it is for</th><th>Where it lives</th></tr>
<tr><td><strong>SOUL.md</strong></td><td>Who the agent is and how it speaks: tone, brevity, directness, what to avoid. Applies everywhere</td><td><code>~/.hermes/SOUL.md</code> (only there — it is looked up in the Hermes home directory alone)</td></tr>
<tr><td><strong>AGENTS.md</strong></td><td>How work is done in this project: paths, commands, conventions, what is forbidden</td><td>In the project (git root and subdirectories)</td></tr>
</table>
<p class="note">A simple rule: what should apply <strong>everywhere</strong> goes into SOUL.md; what
belongs to <strong>one project</strong> goes into AGENTS.md. Put a specific project's ports and paths
into SOUL.md and you will be hunting and deleting them a month later.</p>

<h2>Which files the agent knows</h2>
<table class="wiki-tabulka">
<tr><th>File</th><th>Meaning</th></tr>
<tr><td><code>.hermes.md</code> / <code>HERMES.md</code></td><td>Project instructions with the highest priority</td></tr>
<tr><td><code>AGENTS.override.md</code></td><td>Your personal per-directory override — usually not committed, so you can run different rules than the shared file</td></tr>
<tr><td><code>AGENTS.md</code></td><td>Project instructions, conventions, architecture notes</td></tr>
<tr><td><code>CLAUDE.md</code></td><td>A file from another tool that Hermes also recognises</td></tr>
<tr><td><code>.cursorrules</code>, <code>.cursor/rules/*.mdc</code></td><td>Cursor IDE rules — your existing conventions apply here too</td></tr>
<tr><td><code>SOUL.md</code></td><td>The agent's identity; always loaded, independently of the rest</td></tr>
</table>
<p><strong>Only one</strong> project file is loaded — the first found in the order
<code>.hermes.md</code> → <code>AGENTS.override.md</code> → <code>AGENTS.md</code> →
<code>CLAUDE.md</code> → <code>.cursorrules</code>. So with both <code>AGENTS.md</code> and
<code>CLAUDE.md</code> side by side, <code>AGENTS.md</code> wins and the other is ignored.
<code>SOUL.md</code> is always added on top as the agent's identity — that is the exception.</p>

<h2>When the files are loaded</h2>
<table class="wiki-tabulka">
<tr><th>When</th><th>What happens</th></tr>
<tr><td>At startup</td><td>The working directory is scanned (upwards to the git root). Content is read, checked for injected instructions and truncated if needed</td></tr>
<tr><td>During the session</td><td>When the agent touches a file in a subdirectory, rules from that directory and up to five parents are added. Great for large projects: each part carries its own rules</td></tr>
</table>
<p class="note">That is why you do not need one giant instruction file for a whole project. The
frontend has its rules, the backend its own — and the agent gets them exactly when it starts working
in that directory.</p>

<h2>Limits worth knowing</h2>
<table class="wiki-tabulka">
<tr><th>Limit</th><th>Value</th></tr>
<tr><td>Maximum file length</td><td>Configurable; otherwise it scales with the model (floor 20,000 characters, ceiling 500,000)</td></tr>
<tr><td>Truncating an over-long file</td><td>The head (70%) and tail (20%) are kept, with a marker in the middle</td></tr>
<tr><td>Time to read one file</td><td>5 seconds. A file on a slow drive (iCloud, OneDrive, a network share) may be skipped with a warning</td></tr>
<tr><td>An empty SOUL.md</td><td>Nothing at all is added — which is also a choice</td></tr>
</table>
<div class="code-block"><span class="c"># this is the marker when a file was truncated:</span>
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars. Use file tools to read the full file.]</div>

<h2>Writing a file that works</h2>
<table class="wiki-tabulka">
<tr><th>Principle</th><th>An example from practice</th></tr>
<tr><td>Short and concrete</td><td>Ten concrete rules beat five pages of description</td></tr>
<tr><td>Write down what is <strong>forbidden</strong> too</td><td>"Never add a light theme, the site is dark only" — without it the agent improvises</td></tr>
<tr><td>State the commands and paths to use</td><td>The agent does not have to hunt for them and cannot mix them up</td></tr>
<tr><td>Headers and bullets</td><td>The agent navigates the file better, and so do you</td></tr>
<tr><td>Update it when the project changes</td><td>Stale rules are worse than none — the agent follows them</td></tr>
</table>
<p>The easiest start: have the agent walk the project and write the first version, which you then
edit.</p>
<div class="code-block"><span class="p">❯</span> Walk through this project and draft an AGENTS.md — only the essentials
    that must be followed: how to run tests, where things live and what must not be done.</div>

<h2>Pitfalls from our systems</h2>
<table class="wiki-tabulka">
<tr><th>What happened</th><th>What to do</th></tr>
<tr><td><strong>A long rules file was truncated and part of it vanished</strong></td><td>That is exactly why we keep files short. If a rule matters, put it near the top</td></tr>
<tr><td><strong>Two rules contradicted each other</strong> (old one in AGENTS.md, new one in SOUL.md)</td><td>The agent leaned towards whichever it read first. Keep rules in one place — personality in SOUL.md, work in AGENTS.md</td></tr>
<tr><td><strong>Rules from a subdirectory overrode the main ones</strong></td><td>Expect subdirectory files to be added during the session. When they conflict, the more specific (closer) file wins</td></tr>
<tr><td><strong>A CLAUDE.md existed and its rules never applied</strong></td><td>Only one project file is loaded — the highest priority one. Delete the others or merge them</td></tr>
<tr><td><strong>A SOUL.md in the project was ignored</strong></td><td>Correct: identity comes only from the Hermes home directory. Project rules belong in AGENTS.md</td></tr>
<tr><td><strong>A file on a network share was never read</strong></td><td>Reading has a 5-second cap. Keep rules on local storage</td></tr>
<tr><td><strong>We accidentally pasted foreign text into a rules file</strong> (copied web content, say)</td><td>Content is scanned for injected instructions, but rely on yourself: only put what you wrote into a rules file</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Start with three rules and add more when it hurts</td><td>An empty file beats a five-page one that gets truncated</td></tr>
<tr><td>Say in SOUL.md how long answers should be</td><td>One sentence saves thousands of words across every reply</td></tr>
<tr><td>"What not to do" belongs in AGENTS.md</td><td>Prohibitions work better than wishes</td></tr>
<tr><td>Keep the files in git with the project</td><td>You can see when and why a rule changed</td></tr>
<tr><td>Put personal tweaks in <code>AGENTS.override.md</code></td><td>You do not overwrite the team file and your change stays yours</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/features/profiles/"><strong>Profiles and multiple agents</strong><span>Each profile has its own identity</span></a>
<a href="/en/wiki/features/tools/"><strong>Tools and toolsets</strong><span>What the agent can do and how to verify it</span></a>
<a href="/en/wiki/getting-started/installation/"><strong>First configuration</strong><span>Installation step by step</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Context files in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What is what
SOUL.md = who the agent is and how it speaks (tone, brevity, what to avoid); applies everywhere; only
~/.hermes/SOUL.md (or $HERMES_HOME/SOUL.md). AGENTS.md = how work is done in a project (paths,
commands, conventions). Global -> SOUL.md; project -> AGENTS.md.

## Supported files
.hermes.md / HERMES.md (highest priority) · AGENTS.override.md (personal, usually not committed) ·
AGENTS.md · CLAUDE.md · .cursorrules / .cursor/rules/*.mdc · SOUL.md (always separately as identity).
Only ONE project file is loaded (first in that order).

## Loading
At startup from the working directory (up to the git root). During a session, rules from a
subdirectory and up to 5 parents are added when the agent works there (one file per directory).

## Limits
Max length: context_file_max_chars, otherwise model-scaled (floor 20,000, ceiling 500,000 chars).
Truncation: 70% head + 20% tail + 10% marker.
Read timeout: 5 s (slow drives may be skipped with a warning).
An empty SOUL.md adds nothing.

## How to write
Short and concrete · state what is FORBIDDEN · commands, paths, ports · headers · keep it updated.
Easiest start: have the agent walk the project and draft the first version.

## Pitfalls from our systems
1. A long file gets truncated -> keep it short, important rules first.
2. Contradicting rules (AGENTS.md vs SOUL.md) -> the agent picks by order; keep them separate.
3. Subdirectory rules override the main ones -> the more specific file wins.
4. CLAUDE.md is ignored when AGENTS.md exists -> merge or delete.
5. A project SOUL.md is ignored -> identity only from the Hermes home directory.
6. A file on a network share was never read (5 s limit) -> keep rules local.
7. Foreign text in a rules file -> injection scanning exists, but rely on yourself.

## Tips
Start with 3 rules · answer length into SOUL.md · "what not to do" into AGENTS.md · files in git ·
personal tweaks in AGENTS.override.md.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(24)
    stranka = najdi(24)
    assert stranka and stranka["nazev"] == "Kontextové soubory"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Kontextové soubory — AGENTS.md, HERMES.md a SOUL.md",
        "Jak agentovi předat pravidla projektu a vlastní osobnost: které soubory se načítají, jaké mají limity, jak se zkracují a jak nedostat protichůdná pravidla.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Kontextové soubory",
        "Soubor s pravidly je nejrychlejší cesta, jak agentovi vysvětlit, jak to u vás chodí — a nejrychlejší cesta, jak si ho zkazit. Prakticky a bez teorie.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Kontextové soubory — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Context files — AGENTS.md, HERMES.md and SOUL.md",
        "How to hand the agent project rules and your own identity: which files are loaded, their limits, how truncation works and how to avoid contradictory rules.",
        OBRAZEK, "Wiki · Features in depth", "Context files",
        "A rules file is the fastest way to explain your conventions to the agent — and the fastest way to ruin it. Practical, no theory.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Context files — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
