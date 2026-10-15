#!/usr/bin/env python3
"""Postaví stránku wiki „Skilly — rozšíření agenta" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-skills.md, guides-work-with-skills.md,
developer-guide-creating-skills.md, reference-skills-catalog.md (58 hotových),
reference-optional-skills-catalog.md (153 volitelných).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/skills"
OBRAZEK = "wiki-skilly"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🧩</span><div><strong>Skill je zapsaný postup — recept, který agent umí použít.</strong>
Není to program ani instalace. Je to soubor s návodem, který si agent přečte, <em>až když ho potřebuje</em>.
Napíšete jednou, jak má něco dělat, a agent to příště udělá stejně — i po měsíci, i v novém rozhovoru.</div></div>

<h2>Co je skill (a co není)</h2>
<table class="wiki-tabulka">
<tr><th>Co</th><th>Co to je</th><th>Příklad</th></tr>
<tr><td><strong>Skill</strong></td><td>Napsaný postup pro agenta: kdy ho použít, jaké kroky udělat, čeho se vyvarovat, jak ověřit výsledek</td><td>„Jak u nás zálohovat databázi“</td></tr>
<tr><td><strong>Nástroj</strong> (tool)</td><td>Schopnost, kterou agent má — čte soubory, spouští příkazy, hledá na webu</td><td>Spuštění příkazu v terminálu</td></tr>
<tr><td><strong>Plugin</strong></td><td>Programové rozšíření samotného agenta (nová funkce v kódu). Píše se v Pythonu</td><td>Napojení na platební bránu</td></tr>
</table>
<p class="note">Pro většinu uživatelů stačí skilly. Plugin je něco, co programátor vyvíjí a udržuje — skill je jen prověřený postup v textu.</p>

<h2>Proč se to vyplatí</h2>
<table class="wiki-tabulka">
<tr><th>Přínos</th><th>Co to znamená v praxi</th></tr>
<tr><td>Postup se dodrží pokaždé</td><td>Agent nemusí pokaždé vymýšlet, jak na to — přečte si váš postup. Méně chyb, méně vysvětlování</td></tr>
<tr><td>Nezabírá místo, dokud není potřeba</td><td>Agent zná jen <em>názvy a popisy</em> skillů. Celý text si načte, až když se hodí — proto můžete mít desítky skillů a nic to nestojí</td></tr>
<tr><td>Vaše know-how zůstane u vás</td><td>Skilly jsou obyčejné soubory na vašem serveru ve složce <code>~/.hermes/skills/</code>. Můžete je zálohovat i přesunout</td></tr>
<tr><td>Agent se zlepšuje sám</td><td>Když se něco složitě podaří, agent si z toho umí sepsat skill a příště to má jednodušší</td></tr>
</table>

<h2>Hotové skilly — kde je brát</h2>
<p>Agent už má <strong>58 hotových skillů</strong> a dalších <strong>153 volitelných</strong>, které se doinstalovávají zvlášť.
Podívat se a vybrat si můžete příkazem:</p>
<div class="code-block"><span class="c"># prohlížení katalogu (klávesami nahoru/dolů, Enter vybere)</span>
<span class="p">$</span> hermes skills browse
<span class="c"># co už mám k dispozici</span>
<span class="p">$</span> hermes skills list
<span class="c"># hledání (funguje i v rozhovoru jako /skills search)</span>
<span class="p">$</span> hermes skills search záloha</div>
<p>Instalace jednoho skillu je jeden příkaz:</p>
<div class="code-block"><span class="c"># volitelný skill z oficiálního katalogu</span>
<span class="p">$</span> hermes skills install official/research/arxiv
<span class="c"># nebo přímo v rozhovoru</span>
<span class="p">$</span> /skills install official/creative/songwriting-and-ai-music</div>
<table class="wiki-tabulka">
<tr><th>Kategorie</th><th>Co v ní najdete (příklady z hotových skillů)</th></tr>
<tr><td>Dokumenty</td><td>Word, Excel, PDF, prezentace — tvorba i čtení</td></tr>
<tr><td>Práce s kódem</td><td>GitHub, kontrola změn, hledání chyb, spouštění testů</td></tr>
<tr><td>Výzkum a web</td><td>Ověřené citace, sběr z RSS, sledování stránek, kontrola domén</td></tr>
<tr><td>Komunikace</td><td>Procházení e-mailů a příprava odpovědí</td></tr>
<tr><td>Provoz serveru</td><td>Docker, zálohy, monitorování, bezpečnost</td></tr>
<tr><td>Tvořivé</td><td>Grafy, diagramy, obrázky, jednoduché animace</td></tr>
</table>
<p class="note"><strong>Nainstalovaný skill platí pro nové rozhovory.</strong> Když ho chcete použít hned uprostřed práce,
spusťte <code>/reset</code> (nový rozhovor), nebo si vyžádejte okamžité načtení přepínačem <code>--now</code> — to je
o něco dražší, protože se znovu načítá paměť rozhovoru.</p>

<h2>Naučte agenta vlastní postup — i bez psaní</h2>
<p>Nemusíte psát soubor ručně. Příkazem <code>/learn</code> řeknete agentovi, ať si postup sepíše sám —
z dokumentace, z webové stránky, nebo z toho, co jste právě spolu udělali:</p>
<div class="code-block"><span class="c"># z webové dokumentace</span>
<span class="p">$</span> /learn https://docs.example.com/api/quickstart
<span class="c"># z postupu, který jste právě prošli spolu</span>
<span class="p">$</span> /learn jak jsme zálohovali databázi
<span class="c"># z vlastních poznámek a souborů</span>
<span class="p">$</span> /learn naše pravidla pro zveřejňování článků</div>
<p>Agent si materiál projde, napíše z něj skill a od příště ho bude používat. Nic nemusíte umět programovat.</p>

<h2>Jak vypadá vlastní skill</h2>
<p>Skill je jediný textový soubor <code>SKILL.md</code> ve vlastní složce. Na začátku je krátké označení, podle kterého
agent pozná, kdy má skill použít, a zbytek je návod:</p>
<div class="code-block"><span class="c">---</span>
name: zaloha-databaze
description: Když se má zálohovat databáze našeho webu.
<span class="c">---</span>
<span class="c"># Záloha databáze</span>

<span class="c">## Kdy použít</span>
Když se mluví o záloze, obnově nebo úpravě zálohovacího skriptu.

<span class="c">## Postup</span>
1. Zastavit sběr dat.
2. Spustit zálohu příkazem …
3. Ověřit, že soubor vzniknul a není prázdný.

<span class="c">## Na co pozor</span>
Nezapisovat heslo do souboru se zálohou.

<span class="c">## Jak ověřit</span>
Soubor existuje, má nenulovou velikost a jde z něj obnovit testovací databáze.</div>
<p><strong>Rozhoduje první věta.</strong> Agent se dívá hlavně na <code>description</code> — musí být krátká a musí
říct, při jaké příležitosti se skill použije („Když se…“ / „Use when…“).</p>

<h2>Naše tipy z provozu</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Pište konkrétní postup, ne obecné rady</td><td>„Spusť tento příkaz a zkontroluj tento výstup“ je použitelné, „buď opatrný“ není</td></tr>
<tr><td>Jeden skill = jedna věc</td><td>Malý a přesný skill se použije správně; obří se plete s ostatními</td></tr>
<tr><td>Doplňte, co se nepovedlo</td><td>Napsat do skillu chyby, na které jste narazili, ušetří hodiny příště</td></tr>
<tr><td>Přidejte, jak výsledek ověřit</td><td>Agent si tak sám zkontroluje, jestli to udělal dobře (a vy taky)</td></tr>
<tr><td>Žádná hesla a klíče uvnitř skillu</td><td>Skill je návod, ne trezor. Tajné údaje patří do nastavení agenta</td></tr>
<tr><td>Když se realita změní, přepište skill</td><td>Zastaralý skill je horší než žádný — agent se podle něj naučí špatný postup</td></tr>
<tr><td>Než nainstalujete cizí skill, přečtěte si ho</td><td>Skill říká agentovi, co má dělat. Nainstalujte jen zdroj, kterému věříte, a text si projděte</td></tr>
</table>

<h2>Když se to nedaří</h2>
<table class="wiki-tabulka">
<tr><th>Co se děje</th><th>Příčina a co s tím</th></tr>
<tr><td>Agent skill nepoužije</td><td>Popis (první věta) nesedí na zadání — přepište ho tak, aby začínal „Když se…“ a obsahoval slova, kterými úkol zadáváte</td></tr>
<tr><td>Nainstalovaný skill nefunguje hned</td><td>V rozhovoru se načítá při jeho začátku. Spusťte <code>/reset</code>, nebo si vyžádejte načtení hned</td></tr>
<tr><td>Pletou se dva podobné skilly</td><td>Dva skilly se stejným jménem nebo stejnou oblastí. Jeden přejmenujte nebo slučte</td></tr>
<tr><td>Nevím, co agent používá</td><td><code>hermes skills list</code> (nebo <code>/skills search</code>) ukáže, co je k dispozici; <code>hermes skills audit</code> zkontroluje stav katalogu</td></tr>
<tr><td>Skill dělá něco zlého</td><td>Cizí skill může obsahovat nebezpečný postup. Smažte ho ze složky <code>~/.hermes/skills/</code> a berte skilly jen z ověřených zdrojů</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/prvni-chat/"><strong>První chat s agentem</strong><span>Jak zadávat úkoly, aby se daly ověřit</span></a>
<a href="/skills/"><strong>Přehled dovedností</strong><span>Co všechno agent umí</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/skills" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Skilly do detailu (anglicky)</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Discord komunity</strong><span>Podělte se o vlastní skill</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co je skill
Napsaný postup (recept) pro agenta: kdy ho použít, jaké kroky udělat, čeho se vyvarovat, jak ověřit výsledek.
Není to program ani plugin — je to text, který si agent přečte, až když ho potřebuje.
- Skill = návod v textu | Nástroj = schopnost agenta | Plugin = programové rozšíření (Python)

## Proč
- postup se dodrží pokaždé stejně
- nezabírá místo, dokud není potřeba (agent zná jen názvy a popisy)
- soubory ve ~/.hermes/skills/ — dají se zálohovat a přesouvat
- agent si umí sepsat skill i sám z vlastní zkušenosti

## Hotové skilly
hermes skills browse            # katalog
hermes skills list              # co mám
hermes skills search záloha     # hledání
hermes skills install official/research/arxiv
/skills install official/creative/songwriting-and-ai-music
K dispozici 58 hotových + 153 volitelných (dokumenty, kód, výzkum, e-maily, provoz serveru, tvořivé).
Nainstalovaný skill platí pro nové rozhovory; hned se dá načíst přes /reset nebo --now (dražší).

## Vlastní skill z podkladů
/learn https://docs.example.com/api/quickstart
/learn jak jsme zálohovali databázi
/learn naše pravidla pro zveřejňování článků

## Formát SKILL.md
---
name: zaloha-databaze
description: Když se má zálohovat databáze našeho webu.
---
# Záloha databáze
## Kdy použít / ## Postup / ## Na co pozor / ## Jak ověřit
Rozhoduje první věta (description) — musí říct, při jaké příležitosti se skill použije.

## Tipy
- konkrétní postup místo obecných rad
- jeden skill = jedna věc
- doplnit chyby, na které se narazilo, a způsob ověření
- žádná hesla a klíče uvnitř skillu
- zastaralý skill přepsat
- cizí skill si nejdřív přečíst (skill říká agentovi, co dělat)

## Když se nedaří
- agent skill nepoužije -> popis nesedí na zadání (začni "Když se ...")
- nefunguje hned -> /reset nebo --now
- pletou se dva -> přejmenovat/sloučit
- co agent používá -> hermes skills list, hermes skills audit
- škodlivý cizí skill -> smazat ze ~/.hermes/skills/
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🧩</span><div><strong>A skill is a written procedure — a recipe the agent can follow.</strong>
It is not a program and nothing gets installed in the usual sense. It is a document the agent reads <em>when it needs it</em>.
Write down once how something should be done, and it will be done the same way next time — even months later, even in a new chat.</div></div>

<h2>What a skill is (and is not)</h2>
<table class="wiki-tabulka">
<tr><th>Thing</th><th>What it is</th><th>Example</th></tr>
<tr><td><strong>Skill</strong></td><td>A written procedure for the agent: when to use it, which steps to take, what to avoid, how to verify the result</td><td>"How we back up the database"</td></tr>
<tr><td><strong>Tool</strong></td><td>A capability the agent already has — reading files, running commands, searching the web</td><td>Running a terminal command</td></tr>
<tr><td><strong>Plugin</strong></td><td>A code extension of the agent itself (a new feature). Written in Python</td><td>Wiring in a payment gateway</td></tr>
</table>
<p class="note">For most people skills are all they need. A plugin is something a programmer builds and maintains — a skill is just a proven procedure in plain text.</p>

<h2>Why it pays off</h2>
<table class="wiki-tabulka">
<tr><th>Benefit</th><th>What it means in practice</th></tr>
<tr><td>The procedure is followed every time</td><td>The agent does not reinvent it — it reads your procedure. Fewer mistakes, less explaining</td></tr>
<tr><td>It costs nothing until needed</td><td>The agent only knows the <em>names and descriptions</em>. The full text is loaded when relevant — so you can keep dozens of skills</td></tr>
<tr><td>Your know-how stays with you</td><td>Skills are plain files on your server in <code>~/.hermes/skills/</code>. You can back them up or move them</td></tr>
<tr><td>The agent improves on its own</td><td>When something difficult works out, the agent can write a skill from it and repeat it next time</td></tr>
</table>

<h2>Ready-made skills — where to get them</h2>
<p>The agent ships with <strong>58 bundled skills</strong> and <strong>153 optional</strong> ones you install yourself.
To browse and pick:</p>
<div class="code-block"><span class="c"># browse the catalog (arrow keys, Enter selects)</span>
<span class="p">$</span> hermes skills browse
<span class="c"># what you already have</span>
<span class="p">$</span> hermes skills list
<span class="c"># search (also works inside a chat as /skills search)</span>
<span class="p">$</span> hermes skills search backup</div>
<p>Installing one is a single command:</p>
<div class="code-block"><span class="c"># an optional skill from the official catalog</span>
<span class="p">$</span> hermes skills install official/research/arxiv
<span class="c"># or straight inside a chat</span>
<span class="p">$</span> /skills install official/creative/songwriting-and-ai-music</div>
<table class="wiki-tabulka">
<tr><th>Category</th><th>What you will find (examples of bundled skills)</th></tr>
<tr><td>Documents</td><td>Word, Excel, PDF, presentations — creating and reading</td></tr>
<tr><td>Working with code</td><td>GitHub, reviewing changes, hunting bugs, running tests</td></tr>
<tr><td>Research and web</td><td>Verifiable citations, RSS collection, watching pages, domain checks</td></tr>
<tr><td>Communication</td><td>Triaging an inbox and drafting replies</td></tr>
<tr><td>Server operations</td><td>Docker, backups, monitoring, security</td></tr>
<tr><td>Creative</td><td>Charts, diagrams, images, simple animations</td></tr>
</table>
<p class="note"><strong>An installed skill applies to new conversations.</strong> To use it right away mid-task, run
<code>/reset</code> (a fresh chat), or ask for immediate loading with <code>--now</code> — that costs a little more because
the conversation memory is reloaded.</p>

<h2>Teach the agent your own procedure — without writing code</h2>
<p>You do not have to write the file yourself. The <code>/learn</code> command tells the agent to write it for you —
from documentation, a web page, or from what you just did together:</p>
<div class="code-block"><span class="c"># from online documentation</span>
<span class="p">$</span> /learn https://docs.example.com/api/quickstart
<span class="c"># from a procedure you just walked through together</span>
<span class="p">$</span> /learn how we backed up the database
<span class="c"># from your own notes and files</span>
<span class="p">$</span> /learn our rules for publishing articles</div>
<p>The agent gathers the material, writes the skill and uses it from then on. No programming required.</p>

<h2>What your own skill looks like</h2>
<p>A skill is a single text file <code>SKILL.md</code> in its own folder. It starts with a short label the agent uses to
recognise when to apply it, followed by the procedure:</p>
<div class="code-block"><span class="c">---</span>
name: database-backup
description: Use when the website database needs backing up.
<span class="c">---</span>
<span class="c"># Database backup</span>

<span class="c">## When to use</span>
Whenever backups, restores or the backup script come up.

<span class="c">## Procedure</span>
1. Stop data collection.
2. Run the backup with this command …
3. Verify the file exists and is not empty.

<span class="c">## Pitfalls</span>
Never write the password into the backup archive.

<span class="c">## Verification</span>
The file exists, has non-zero size and a test database can be restored from it.</div>
<p><strong>The first sentence decides.</strong> The agent mainly looks at <code>description</code> — it must be short and say
at what moment the skill applies ("Use when…").</p>

<h2>Tips from experience</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Write a concrete procedure, not general advice</td><td>"Run this command and check this output" is usable; "be careful" is not</td></tr>
<tr><td>One skill, one thing</td><td>A small precise skill gets applied correctly; a huge one gets confused with others</td></tr>
<tr><td>Record what went wrong</td><td>Writing down the mistakes you hit saves hours next time</td></tr>
<tr><td>Add how to verify the result</td><td>The agent then checks its own work (and so can you)</td></tr>
<tr><td>No passwords or keys inside a skill</td><td>A skill is a procedure, not a vault. Secrets belong in the agent's settings</td></tr>
<tr><td>When reality changes, rewrite the skill</td><td>An outdated skill is worse than none — the agent learns the wrong procedure</td></tr>
<tr><td>Read a third-party skill before installing</td><td>A skill tells the agent what to do. Only install sources you trust, and read the text first</td></tr>
</table>

<h2>When it does not work</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>Cause and what to do</th></tr>
<tr><td>The agent does not use the skill</td><td>The description (first sentence) does not match the task — rewrite it to start with "Use when…" and to contain the words you actually use</td></tr>
<tr><td>A freshly installed skill does nothing</td><td>In a chat, skills load at the start of the session. Run <code>/reset</code> or request immediate loading</td></tr>
<tr><td>Two similar skills clash</td><td>Two skills share a name or an area. Rename or merge one of them</td></tr>
<tr><td>I do not know what the agent has</td><td><code>hermes skills list</code> (or <code>/skills search</code>) shows what is available; <code>hermes skills audit</code> checks the catalog state</td></tr>
<tr><td>A skill does something harmful</td><td>A third-party skill can contain a dangerous procedure. Delete it from <code>~/.hermes/skills/</code> and only take skills from trusted sources</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/first-chat/"><strong>Your first chat</strong><span>How to give verifiable tasks</span></a>
<a href="/en/skills/"><strong>Skills overview</strong><span>Everything the agent can do</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/skills" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Skills in detail</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Community Discord</strong><span>Share a skill of your own</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What a skill is
A written procedure (recipe) for the agent: when to use it, which steps to take, what to avoid, how to
verify the result. Not a program or plugin - a text the agent reads when it needs it.
- Skill = procedure in text | Tool = a capability the agent has | Plugin = code extension (Python)

## Why
- the procedure is followed the same way every time
- costs nothing until needed (the agent only knows names and descriptions)
- files live in ~/.hermes/skills/ - easy to back up or move
- the agent can write a skill from its own experience

## Ready-made skills
hermes skills browse            # catalog
hermes skills list              # what I have
hermes skills search backup     # search
hermes skills install official/research/arxiv
/skills install official/creative/songwriting-and-ai-music
58 bundled + 153 optional (documents, code, research, email, server operations, creative).
An installed skill applies to new conversations; load it at once with /reset or --now (costs more).

## Your own skill from sources
/learn https://docs.example.com/api/quickstart
/learn how we backed up the database
/learn our rules for publishing articles

## SKILL.md format
---
name: database-backup
description: Use when the website database needs backing up.
---
# Title
## When to use / ## Procedure / ## Pitfalls / ## Verification
The first sentence (description) decides - it must say when the skill applies.

## Tips
- concrete procedure, not general advice
- one skill, one thing
- record the mistakes you hit and how to verify
- no passwords or keys inside a skill
- rewrite outdated skills
- read third-party skills before installing

## Troubleshooting
- agent does not use it -> description does not match the task (start with "Use when...")
- does nothing right after install -> /reset or --now
- two skills clash -> rename or merge
- what is available -> hermes skills list, hermes skills audit
- harmful third-party skill -> delete from ~/.hermes/skills/
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(5)
    stranka = najdi(5)
    assert stranka and stranka["nazev"].startswith("Skilly")

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Skilly — jak agenta naučit nové postupy",
        "Co je skill, kde brát hotové (58 hotových a 153 volitelných), jak si nechat napsat vlastní postup příkazem /learn a jak vypadá soubor SKILL.md.",
        OBRAZEK, "Wiki · Začínáme", "Skilly — rozšíření agenta",
        "Napíšete postup jednou a agent ho použije pokaždé — bez programování a bez toho, aby to zabíralo místo.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Skilly — rozšíření agenta — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Skills — teaching the agent new procedures",
        "What a skill is, where to get ready-made ones (58 bundled, 153 optional), how to have your own procedure written with /learn, and what SKILL.md looks like.",
        OBRAZEK, "Wiki · Start here", "Skills — extending the agent",
        "Write a procedure once and the agent applies it every time — no programming, and it costs nothing until needed.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Skills — extending the agent — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
