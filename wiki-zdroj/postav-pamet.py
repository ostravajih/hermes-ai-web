#!/usr/bin/env python3
"""Postaví stránku wiki „Paměť agenta" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-memory.md (limity 2 200 / 1 375 znaků,
co si agent ukládá sám, session_search, /journey, write_approval),
user-guide-features-context-files.md (pravidlové soubory).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/memory"
OBRAZEK = "wiki-pamet"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🧠</span><div><strong>Paměť je to, co si agent odnese do příštího rozhovoru.</strong>
Drží se v ní jen to podstatné o vás a o vašem projektu — je totiž <em>součástí každého zadání</em>,
takže musí zůstat krátká. Všechno ostatní si agent najde ve starých rozhovorech, až když to potřebuje.</div></div>

<h2>Dvě paměti odděleně</h2>
<p>Agent si vede dva krátké seznamy — jeden o vás, druhý o práci. Oba leží ve složce
<code>~/.hermes/memories/</code> jako obyčejné textové soubory, takže je můžete zálohovat i přesunout.</p>
<table class="wiki-tabulka">
<tr><th>Soubor</th><th>Co v něm je</th><th>Jak je velký</th></tr>
<tr><td><code>USER.md</code></td><td>Kdo jste a jak s vámi mluvit: jméno, čím se živíte, co vám vadí, jestli chcete stručně nebo podrobně</td><td>asi <strong>1 375 znaků</strong> (půl strany textu)</td></tr>
<tr><td><code>MEMORY.md</code></td><td>Poznámky k práci: jak je nastavený server, jaké máte zvyky, co se osvědčilo, na co si dát pozor</td><td>asi <strong>2 200 znaků</strong> (necelá stránka)</td></tr>
</table>
<p class="note">Jednotlivé poznámky jsou oddělené znakem <code>§</code>, aby se daly samostatně měnit a mazat.</p>

<h2>Proč je paměť tak krátká</h2>
<table class="wiki-tabulka">
<tr><th>Důvod</th><th>Co z toho plyne pro vás</th></tr>
<tr><td>Je součástí každého zadání</td><td>Za každý řádek v paměti platíte při každém dotazu — proto se do ní nevejde všechno</td></tr>
<tr><td>Nezkrátí se sama</td><td>Když je plná, agent musí nejdřív něco vyhodit nebo zkrátit, teprve pak přidá nové</td></tr>
<tr><td>Patří tam jen podstatné věci</td><td>Ne úryvky z rozhovoru a ne to, co se dá kdykoli dohledat</td></tr>
</table>

<h2>Co si agent zapamatuje sám</h2>
<p>Nemusíte o to žádat. Agent si uloží, když se dozví něco, co bude platit i příště:</p>
<table class="wiki-tabulka">
<tr><th>Co se dozví</th><th>Příklad</th></tr>
<tr><td>Vaše zvyky a přání</td><td>„Chci stručné odpovědi a bez tabulek.“</td></tr>
<tr><td>Jak je nastavené vaše prostředí</td><td>„Web běží na nginxu, databáze je MariaDB, doména je hermes-ai.cz.“</td></tr>
<tr><td>Opravy a upozornění</td><td>„Nepoužívej sudo, uživatel je ve skupině docker.“</td></tr>
<tr><td>Zavedené postupy v projektu</td><td>„Adresy píšeme s lomítkem na konci, obrázky mají název s pomlčkou.“</td></tr>
<tr><td>Dokončené věci</td><td>„Migrace databáze proběhla 12. 10. 2026.“</td></tr>
</table>
<p><strong>Co si naopak neuloží:</strong> co jste řekli jen mimochodem a k ničemu to nebylo, údaje z nastavení
(hesla a klíče patří jinam, ne do paměti) a nic, co si dokáže dohledat v historii rozhovorů.</p>

<h2>Když chcete, aby si něco zapamatoval</h2>
<p>Řekněte to přímo — funguje to spolehlivě:</p>
<div class="code-block"><span class="p">❯</span> Zapamatuj si, že naše faktury posíláme vždycky k pátému dni v měsíci.
<span class="p">❯</span> Poznamenej si, že tenhle server nesmí být nikdy vypnutý bez upozornění.</div>
<p>A kdykoli se můžete zeptat, co si o vás vede, nebo ho nechat poznámku opravit:</p>
<div class="code-block"><span class="p">❯</span> Co si o mně pamatuješ?
<span class="p">❯</span> Smaž z paměti tu poznámku o fakturách, změnilo se to.</div>
<p class="note">Klidně si soubor otevřete a přečtěte (je to obyčejný text):
<code>cat ~/.hermes/memories/USER.md</code>. Ruční zásah ale dělejte jen když víte, co děláte —
přes agenta je to bezpečnější, sám si po sobě uklidí duplicity.</p>

<h2>Tři místa, kde si agent pamatuje</h2>
<table class="wiki-tabulka">
<tr><th>Kde</th><th>Co tam je</th><th>Jak to použít</th></tr>
<tr><td><strong>Živý rozhovor</strong></td><td>Všechno, co jste si právě napsali</td><td>Stačí mluvit; když je rozhovor dlouhý, agent ho srovná (<code>/compress</code>)</td></tr>
<tr><td><strong>Paměť</strong> (USER.md, MEMORY.md)</td><td>Jen to podstatné, vždy po ruce</td><td>Platí v každém novém rozhovoru od prvního dotazu</td></tr>
<tr><td><strong>Staré rozhovory</strong></td><td>Všechno, co jste kdy řešili — bez omezení</td><td>„Jak jsme to tenkrát dělali?“ Agent si vzpomene i po měsících</td></tr>
</table>
<p class="note"><strong>Praktický důsledek:</strong> paměť se projeví při <strong>novém rozhovoru</strong>.
Když začnete nový úkol nebo nový den, spusťte <code>/new</code> — agent si znovu přečte, co o vás ví,
a začne s čistou hlavou (staré rozhovory zůstávají dohledatelné).</p>

<h2>Pravidla, která platí pořád</h2>
<p>Vedle paměti si agent na začátku práce přečte i <strong>pravidlové soubory</strong> ve vaší složce. Ty píšete
vy, mají neomezenou délku a platí pro celý projekt:</p>
<table class="wiki-tabulka">
<tr><th>Soubor</th><th>K čemu je</th></tr>
<tr><td><code>AGENTS.md</code></td><td>Pravidla a zvyklosti projektu — co se kde udržuje, co se nesmí, jak se co nasazuje</td></tr>
<tr><td><code>HERMES.md</code> (nebo <code>.hermes.md</code>)</td><td>Totéž, ale s nejvyšší předností</td></tr>
<tr><td><code>SOUL.md</code></td><td>Jak má agent mluvit a chovat se (tón, jazyk)</td></tr>
</table>
<p><strong>Rozdíl je jednoduchý:</strong> co platí pořád a je delší, patří do souboru s pravidly.
Co je krátké a musí to mít agent vždy u sebe, patří do paměti.</p>

<h2>Když to nefunguje</h2>
<table class="wiki-tabulka">
<tr><th>Co se děje</th><th>Příčina a co s tím</th></tr>
<tr><td>„Řekl jsem mu to a on to zapomněl.“</td><td>Nejspíš to zůstalo jen v rozhovoru a neuložilo se. Řekněte to znovu a výslovně: <em>„zapamatuj si, že…“</em></td></tr>
<tr><td>Zapamatoval si to, ale v novém rozhovoru jako by ne</td><td>Zkontrolujte, jestli vznikl nový rozhovor (<code>/new</code>) — paměť se čte na jeho začátku</td></tr>
<tr><td>Pamatuje si něco špatně</td><td>Řekněte mu přesně, co je špatně: <em>„smaž z paměti…“</em> nebo <em>„uprav si to na…“</em></td></tr>
<tr><td>Paměť je plná a nové si neuloží</td><td>Agent musí nejdřív uklidit. Řekněte mu: <em>„srovnej paměť a ulož tohle.“</em> Ručně se nezkracuje</td></tr>
<tr><td>Chci o všem rozhodovat</td><td>Dá se zapnout potvrzování každého zápisu do paměti nastavením <code>memory.write_approval: true</code></td></tr>
</table>

<h2>Naše tipy z provozu</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Začínejte nový den novým rozhovorem</td><td>Paměť se právě tehdy uplatní — agent si přečte, co o vás ví, a nezůstane mu v hlavě včerejší nepořádek</td></tr>
<tr><td>Co platí pořád, dejte do souboru s pravidly</td><td>Nemusíte to opakovat a nezabírá to místo v krátké paměti</td></tr>
<tr><td>Dobré poznámky jsou konkrétní</td><td>„Adresy s lomítkem na konci“ se dá dodržet; „dělej to pěkně“ ne</td></tr>
<tr><td>Hesla a klíče do paměti nepatří</td><td>Paměť je součástí každého zadání — tajné údaje patří do nastavení</td></tr>
<tr><td>Zeptejte se, co si vede</td><td>Překvapení se lépe řeší hned než po měsíci. Stačí: <em>„co si o mně pamatuješ?“</em></td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/skilly/"><strong>Skilly</strong><span>Postupy, které si agent odnese do příště</span></a>
<a href="/wiki/zaciname/prvni-chat/"><strong>První chat s agentem</strong><span>Jak zadávat úkoly, aby se daly ověřit</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/memory" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Paměť do detailu (anglicky)</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Discord komunity</strong><span>Zeptejte se, co komu funguje</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Dvě paměti (složka ~/.hermes/memories/)
- USER.md (~1 375 znaků) — kdo jste, jak s vámi mluvit, co vám vadí
- MEMORY.md (~2 200 znaků) — poznámky k práci: nastavení serveru, zvyky, co se osvědčilo, na co pozor
Poznámky oddělené znakem §.

## Proč je krátká
- je součástí každého zadání (platíte za ni při každém dotazu)
- nezkracuje se sama: když je plná, agent musí nejdřív něco vyhodit nebo zkrátit
- patří tam jen podstatné věci

## Co si agent uloží sám
zvyky a přání uživatele · nastavení prostředí · opravy a upozornění · zavedené postupy · dokončené věci
Neuloží: co zaznělo jen mimochodem, údaje z nastavení (hesla a klíče), co se dá dohledat v historii.

## Jak říct, co si má zapamatovat
"Zapamatuj si, že ..." / "Poznamenej si, že ..."
Zeptat se: "Co si o mně pamatuješ?"; opravit: "Smaž z paměti ..." / "Uprav si to na ..."
Soubor je obyčejný text: cat ~/.hermes/memories/USER.md

## Tři místa, kde si agent pamatuje
1. živý rozhovor (vše, co jste si napsali; /compress když je dlouhý)
2. paměť (jen to podstatné, vždy po ruce)
3. staré rozhovory (všechno, dohledatelné: "jak jsme to tenkrát dělali?")
Paměť se uplatní při novém rozhovoru -> začínat nový den/úkol přes /new.

## Pravidlové soubory (neomezené, píše je uživatel)
AGENTS.md · HERMES.md/.hermes.md (nejvyšší přednost) · SOUL.md (tón a jazyk)
Co platí pořád a je delší -> do souboru; co musí mít agent vždy u sebe -> do paměti.

## Když to nefunguje
- zapomněl -> řeklo se to jen v rozhovoru; říct výslovně "zapamatuj si, že ..."
- v novém rozhovoru jako by ne -> paměť se čte na začátku rozhovoru (/new)
- pamatuje si něco špatně -> "smaž z paměti ..." / "uprav si to na ..."
- plná paměť -> "srovnej paměť a ulož tohle"
- chtít potvrzovat každý zápis -> memory.write_approval: true
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🧠</span><div><strong>Memory is what the agent carries into the next conversation.</strong>
It holds only the essentials about you and your project — because it is <em>part of every request</em>,
so it has to stay short. Everything else the agent finds in past conversations when it needs it.</div></div>

<h2>Two memories, kept apart</h2>
<p>The agent keeps two short lists — one about you, one about the work. Both live in
<code>~/.hermes/memories/</code> as plain text files, so you can back them up or move them.</p>
<table class="wiki-tabulka">
<tr><th>File</th><th>What is in it</th><th>How big it is</th></tr>
<tr><td><code>USER.md</code></td><td>Who you are and how to talk to you: name, what you do, what annoys you, concise or detailed answers</td><td>about <strong>1,375 characters</strong> (half a page)</td></tr>
<tr><td><code>MEMORY.md</code></td><td>Notes about the work: how the server is set up, your habits, what worked, what to watch out for</td><td>about <strong>2,200 characters</strong> (under a page)</td></tr>
</table>
<p class="note">Individual notes are separated by the <code>§</code> character so they can be edited or removed one by one.</p>

<h2>Why memory is so short</h2>
<table class="wiki-tabulka">
<tr><th>Reason</th><th>What it means for you</th></tr>
<tr><td>It is part of every request</td><td>Every line in memory costs you on every question — so it cannot hold everything</td></tr>
<tr><td>It does not shrink by itself</td><td>When it is full, the agent must first drop or shorten something before adding a new note</td></tr>
<tr><td>Only essentials belong there</td><td>Not fragments of a conversation, and not anything that can be looked up later</td></tr>
</table>

<h2>What the agent saves by itself</h2>
<p>You do not have to ask. It saves anything it learns that will still be true next time:</p>
<table class="wiki-tabulka">
<tr><th>What it learns</th><th>Example</th></tr>
<tr><td>Your preferences</td><td>"I want short answers, no tables."</td></tr>
<tr><td>How your environment is set up</td><td>"The site runs on nginx, the database is MariaDB, the domain is example.com."</td></tr>
<tr><td>Corrections and warnings</td><td>"Don't use sudo, the user is in the docker group."</td></tr>
<tr><td>Project conventions</td><td>"URLs end with a slash, image filenames use hyphens."</td></tr>
<tr><td>Completed work</td><td>"The database migration happened on 12 Oct 2026."</td></tr>
</table>
<p><strong>What it will not save:</strong> something you mentioned in passing with no consequence, values from
settings (passwords and keys belong elsewhere, not in memory), and anything it can find in past conversations.</p>

<h2>When you want it to remember something</h2>
<p>Just say so — that always works:</p>
<div class="code-block"><span class="p">❯</span> Remember that we always send invoices by the fifth of the month.
<span class="p">❯</span> Note that this server must never be shut down without a warning.</div>
<p>You can also ask what it keeps, or have a note corrected:</p>
<div class="code-block"><span class="p">❯</span> What do you remember about me?
<span class="p">❯</span> Delete the note about invoices from memory, that changed.</div>
<p class="note">You are welcome to open the file and read it (it is plain text):
<code>cat ~/.hermes/memories/USER.md</code>. Editing it by hand is best left alone — going through the
agent is safer, as it cleans up duplicates itself.</p>

<h2>Three places where the agent remembers</h2>
<table class="wiki-tabulka">
<tr><th>Where</th><th>What is there</th><th>How to use it</th></tr>
<tr><td><strong>The live conversation</strong></td><td>Everything you have just written to each other</td><td>Just talk; when a chat gets long the agent trims it (<code>/compress</code>)</td></tr>
<tr><td><strong>Memory</strong> (USER.md, MEMORY.md)</td><td>Only the essentials, always at hand</td><td>Applies to every new conversation from the first question</td></tr>
<tr><td><strong>Past conversations</strong></td><td>Everything you have ever discussed — unlimited</td><td>"How did we do that back then?" It remembers months later</td></tr>
</table>
<p class="note"><strong>A practical consequence:</strong> memory takes effect in a <strong>new conversation</strong>.
When you start a new task or a new day, run <code>/new</code> — the agent re-reads what it knows about you and
starts with a clear head (past conversations remain searchable).</p>

<h2>Rules that always apply</h2>
<p>Alongside memory, the agent reads <strong>context files</strong> from your folder at the start of work. You write
those yourself; they have no length limit and apply to the whole project:</p>
<table class="wiki-tabulka">
<tr><th>File</th><th>What it is for</th></tr>
<tr><td><code>AGENTS.md</code></td><td>Project rules and conventions — what is kept where, what is forbidden, how things are deployed</td></tr>
<tr><td><code>HERMES.md</code> (or <code>.hermes.md</code>)</td><td>The same, but with the highest priority</td></tr>
<tr><td><code>SOUL.md</code></td><td>How the agent should speak and behave (tone, language)</td></tr>
</table>
<p><strong>The distinction is simple:</strong> anything long and always true belongs in a context file.
Anything short that the agent must always have at hand belongs in memory.</p>

<h2>When it does not work</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>Cause and what to do</th></tr>
<tr><td>"I told it and it forgot."</td><td>Most likely it stayed in the conversation and was never saved. Say it again explicitly: <em>"remember that…"</em></td></tr>
<tr><td>It saved it, but a new chat acts as if it did not</td><td>Check that a new conversation actually started (<code>/new</code>) — memory is read at its beginning</td></tr>
<tr><td>It remembers something wrong</td><td>Tell it exactly what is wrong: <em>"delete … from memory"</em> or <em>"change that note to…"</em></td></tr>
<tr><td>Memory is full and it saves nothing new</td><td>The agent must tidy up first. Say: <em>"tidy up memory and save this."</em> It never compacts on its own</td></tr>
<tr><td>I want to approve every save</td><td>Set <code>memory.write_approval: true</code> to be asked before anything is written</td></tr>
</table>

<h2>Tips from experience</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Start a new day with a new conversation</td><td>That is when memory pays off — the agent re-reads what it knows and does not carry yesterday's clutter</td></tr>
<tr><td>Put lasting rules in a context file</td><td>You do not have to repeat them and they do not take up the short memory</td></tr>
<tr><td>Good notes are specific</td><td>"URLs end with a slash" can be followed; "do it nicely" cannot</td></tr>
<tr><td>Passwords and keys do not belong in memory</td><td>Memory is part of every request — secrets belong in settings</td></tr>
<tr><td>Ask what it keeps</td><td>Surprises are easier to fix now than in a month. Just ask: <em>"what do you remember about me?"</em></td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/skills/"><strong>Skills</strong><span>Procedures the agent carries forward</span></a>
<a href="/en/wiki/getting-started/first-chat/"><strong>Your first chat</strong><span>How to give verifiable tasks</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/memory" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Memory in detail</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Community Discord</strong><span>Ask what works for others</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Two memories (~/.hermes/memories/)
- USER.md (~1,375 chars) - who you are, how to talk to you, what annoys you
- MEMORY.md (~2,200 chars) - notes about the work: server setup, habits, what worked, what to watch
Notes are separated by the section sign.

## Why it is short
- it is part of every request (you pay for it on every question)
- it does not shrink by itself: when full the agent must drop or shorten first
- only essentials belong there

## What the agent saves by itself
preferences, environment facts, corrections, project conventions, completed work
It will not save: passing remarks with no consequence, values from settings (passwords, keys),
anything it can find in past conversations.

## Telling it to remember
"Remember that ..." / "Note that ..."
Ask: "What do you remember about me?"; correct: "Delete ... from memory" / "Change that to ..."
The file is plain text: cat ~/.hermes/memories/USER.md

## Three places it remembers
1. the live conversation (everything; /compress when long)
2. memory (essentials, always at hand)
3. past conversations (all of them, searchable: "how did we do that back then?")
Memory takes effect in a new conversation -> start a new day/task with /new.

## Context files (unlimited, written by the user)
AGENTS.md · HERMES.md/.hermes.md (highest priority) · SOUL.md (tone and language)
Long rules that always apply -> context file; short facts always at hand -> memory.

## Troubleshooting
- forgot -> it only stayed in the conversation; say "remember that ..." explicitly
- a new chat acts as if it did not -> memory is read at the start of a conversation (/new)
- remembers something wrong -> "delete ... from memory" / "change that to ..."
- memory full -> "tidy up memory and save this"
- want to approve saves -> memory.write_approval: true
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(6)
    stranka = najdi(6)
    assert stranka and stranka["nazev"] == "Paměť agenta"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Paměť agenta — aby si pamatoval souvislosti",
        "Co si agent pamatuje mezi rozhovory, kde to leží, jak mu říct, aby si něco uložil, a jak se liší paměť od historie rozhovorů a od pravidel v souborech.",
        OBRAZEK, "Wiki · Začínáme", "Paměť agenta",
        "Dvě krátké poznámky, které si agent odnese do každého dalšího rozhovoru — a tři místa, kde si vůbec pamatuje.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Paměť agenta — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Agent memory — remembering context across conversations",
        "What the agent remembers between conversations, where it lives, how to have something saved, and how memory differs from conversation history and from context files.",
        OBRAZEK, "Wiki · Start here", "Agent memory",
        "Two short notes the agent carries into every new conversation — and the three places where it remembers anything at all.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Agent memory — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
