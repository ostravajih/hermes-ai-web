#!/usr/bin/env python3
"""Postaví stránku wiki „Podagenti" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-delegation.md (co podagent je, předání výsledku,
vnoření, sledování, řízení běžící práce, limity), guides-delegation-patterns.md (kdy delegovat
a kdy ne, hotové vzory).

Naše zkušenosti: zpráva podagenta je tvrzení, ne důkaz — ověřovat vlastním dotazem; podagent se
neumí zeptat člověka; viditelné a kvalitativní úpravy dělá radši hlavní agent.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "16. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation"
OBRAZEK = "wiki-podagenti"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🐝</span><div><strong>Podagent je pomocník, kterého agent vyšle s jasným zadáním.</strong>
Dostane vlastní rozhovor i vlastní terminál, pracuje samostatně a zpátky se vrací <em>jen jeho
shrnutí</em> — ne všechny mezivýsledky. Proto se do vašeho rozhovoru nehrne, co cestou zkoušel.</div></div>

<h2>Kdy se rozdělení práce vyplatí</h2>
<table class="wiki-tabulka">
<tr><th>Vhodné</th><th>Proč</th></tr>
<tr><td>Úloha náročná na přemýšlení (hledání příčiny chyby, kontrola kódu, shrnutí rešerše)</td><td>Podagent má na to celý vlastní prostor a nikoho neruší</td></tr>
<tr><td>Práce, která by zaplavila hlavní rozhovor daty</td><td>Do hlavního rozhovoru se vrátí jen výsledek, ne stovky řádků mezivýsledků</td></tr>
<tr><td>Více nezávislých větví najednou</td><td>Běží souběžně — tři průzkumy místo tří po sobě</td></tr>
<tr><td>Čerstvý pohled bez zaujatosti</td><td>Podagent nevidí, co jste si už mysleli, takže mu nic nebrání říct opak</td></tr>
</table>
<table class="wiki-tabulka">
<tr><th>Nevhodné — udělejte to jinak</th><th>Jak</th></tr>
<tr><td>Jedno volání nástroje nebo drobná úprava souboru</td><td>Zadejte to přímo, ušetříte čas i peníze</td></tr>
<tr><td>Mechanická práce s logikou mezi kroky</td><td>Skript — je spustitelný znovu a přesně</td></tr>
<tr><td>Úloha, u které je potřeba se vás na něco zeptat</td><td>Podagent se ptát neumí — dělá to hlavní agent</td></tr>
<tr><td>Práce, která musí běžet dál po zavření rozhraní</td><td>Plánovaná úloha nebo proces na pozadí — viz <a href="/wiki/zaciname/pravidelne-ulohy/">Pravidelné úlohy (cron)</a></td></tr>
</table>

<h2>Jak se to projeví ve vašem rozhovoru</h2>
<table class="wiki-tabulka">
<tr><th>Co uvidíte</th><th>Co to znamená</th></tr>
<tr><td>„Poslal jsem na to tři pomocníky.“</td><td>Hlavní agent pracuje dál, výsledky dorazí jako zprávy</td></tr>
<tr><td>Pruh s počtem a stavem</td><td>V aplikaci i v terminálu vidíte, kdo běží, jak dlouho a co naposledy udělal</td></tr>
<tr><td>Možnost vstoupit do práce nebo ji zastavit</td><td>Když podagent míří špatně, dá se usměrnit nebo ukončit — nemusíte čekat do konce</td></tr>
<tr><td>Výsledek jako shrnutí</td><td>Když potřebujete i důkaz (výpis souboru, HTTP kód), vyžádejte si ho výslovně</td></tr>
</table>
<p class="note">Podagent se nemůže zeptat vás ani si najmout dalšího podagenta — hloubka je
omezená. Když úloha potřebuje rozhovor s člověkem, patří do hlavního rozhovoru.</p>
<p><strong>Jednorázový běh je zvláštní případ.</strong> Když agent odpovídá a hned končí
(<code>hermes -q „…“</code>, <code>chat --oneshot</code> nebo dotaz bez terminálu), na výsledky
pomocníků se počká a přijdou do <em>téže</em> odpovědi — po skončení už není kam je doručit.
Souběh zůstává, ale počet pomocníků v jednorázovém běhu je omezený zvlášť
(<code>delegation.oneshot_max_children</code>, výchozí <strong>2</strong>, <code>0</code> = bez omezení).
V interaktivním rozhovoru a v chatu s bránou platí dál původní chování na pozadí.</p>

<h2>Zadání pro podagenta</h2>
<p>Zadání se vyplatí psát stejně jako zakázku: co je cílem, jak poznáte, že je hotovo, a co má
přinést zpátky.</p>
<div class="code-block"><span class="p">❯</span> Zjisti, kolik u nás stojí tři varianty VPS u českých poskytovatelů.<span class="p">
❯</span> Za každou variantu uveď cenu v Kč, co je v ní a odkaz. Nevracej nic jiného.


<span class="p">❯</span> Zkontroluj tuhle změnu v kódu na chyby.<span class="p">
❯</span> Vrať seznam nálezů: co, kde a jak se to projeví. Když nic nenajdeš, řekni to.


<span class="p">❯</span> Projdi tyhle tři weby a porovnej je.<span class="p">
❯</span> Výsledek chci jako tabulku: co mají, co nemají a čím se liší.</div>
<p class="note">Když chcete odpověď ve strojovém tvaru (tabulka, seznam položek), dá se podagentovi
zadat i pevná podoba výstupu (<code>output_schema</code>) — hodí se, když výsledek zpracovává
skript.</p>

<h2>Kolik jich může běžet</h2>
<table class="wiki-tabulka">
<tr><th>Věc</th><th>Jak to je</th></tr>
<tr><td>Počet najednou</td><td>Omezený nastavením <code>delegation.max_concurrent_children</code> (u nás 10)</td></tr>
<tr><td>Souběžnost</td><td>Úlohy se spouštějí naráz, výsledky chodí, jak dokončují</td></tr>
<tr><td>Trvalost</td><td>Podagenti žijí s rozhovorem, ze kterého vznikli — přes zavření rozhraní nepřežijí</td></tr>
<tr><td>Viditelnost</td><td>V terminálu <code>/agents</code>, v aplikaci pruh nad psacím polem</td></tr>
</table>

<h2>Pasti z našeho provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co se stalo</th><th>Co s tím</th></tr>
<tr><td><strong>Podagent ohlásil „hotovo“, ale nic se nezměnilo.</strong> Jeho zpráva je jen tvrzení</td><td>Ověřujte výsledek sami — souborem, dotazem do databáze, HTTP kódem stránky. Do zadání patří, čím se má práce prokázat</td></tr>
<tr><td><strong>Podagent se zasekl na něčem, co potřebovalo naše rozhodnutí</strong></td><td>Ptát se neumí. Buď úlohu zadejte hlavnímu agentovi, nebo podagentovi dopředu řekněte, jak se rozhodnout</td></tr>
<tr><td><strong>Práce zůstala rozdělaná, když se rozhovor ukončil</strong></td><td>Podagenti nejsou trvalá služba. Co má vydržet, patří do plánované úlohy nebo mezi procesy na pozadí</td></tr>
<tr><td><strong>Viditelné úpravy dělal podagent a výsledek nebyl dobrý</strong></td><td>Na věci, na kterých záleží a které jsou vidět, se hodí hlavní agent — má celý kontext zadání. Podagenty necháváme na rešerši a práci, která zaplavuje kontext</td></tr>
<tr><td><strong>Deset podagentů a účet za ně byl vyšší, než jsme čekali</strong></td><td>Každý má vlastní kontext, takže se platí zvlášť. Vyplatí se delegovat promyšleně, ne „pro jistotu všude“</td></tr>
</table>

<h2>Hotové vzory</h2>
<table class="wiki-tabulka">
<tr><th>Vzor</th><th>Jak vypadá</th></tr>
<tr><td>Rešerše více témat najednou</td><td>„Prozkoumej tyto tři otázky paralelně a u každé vrať pět bodů.“</td></tr>
<tr><td>Kontrola kódu</td><td>Podagent hledá chyby a bezpečnostní rizika, hlavní agent mezitím pracuje dál</td></tr>
<tr><td>Porovnání variant</td><td>Každý podagent prověří jednu možnost a vrátí stejnou strukturu, aby se daly srovnat</td></tr>
<tr><td>Nejdřív posbírat, pak rozhodnout</td><td>Několik podagentů nasbírá podklady, hlavní agent z nich udělá závěr</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Zadávejte, co přesně má vrátit</td><td>Shrnutí bez formy se špatně používá; „tabulka: cena, co je v ní, odkaz“ se použije hned</td></tr>
<tr><td>Řekněte, jak se práce prokáže</td><td>Už se pak nedá jen tvrdit, že je hotovo</td></tr>
<tr><td>Dávejte podagentům úlohy, které se navzájem nepotřebují</td><td>Běží pak opravdu souběžně a nečekají na sebe</td></tr>
<tr><td>Rozdělanou práci pohlídejte v přehledu</td><td>Zastavit podagenta, který míří špatně, je levnější než dodělat špatný výsledek</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/funkce/nastroje/"><strong>Nástroje a toolsety</strong><span>Co všechno agent umí</span></a>
<a href="/wiki/zaciname/pravidelne-ulohy/"><strong>Pravidelné úlohy (cron)</strong><span>Práce, která přežije zavření rozhraní</span></a>
<a href="/wiki/funkce/sezeni/"><strong>Sezení a jejich obnova</strong><span>Kde se hledá, co se cestou ztratilo</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Podagenti do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co podagent je
Pomocník, kterého agent vyšle s jasným zadáním: vlastní rozhovor, vlastní terminál, samostatná práce.
Do hlavního rozhovoru se vrací jen shrnutí (ne mezivýsledky).

## Kdy delegovat
Vhodné: náročné na uvažování (hledání příčiny, kontrola kódu, shrnutí rešerše), práce, která by
zaplavila kontext, nezávislé větve paralelně, čerstvý pohled bez zaujatosti.
Nevhodné: jedno volání nástroje nebo drobná úprava (zadat přímo), mechanická práce (skript),
úloha vyžadující dotaz člověku (podagent se ptát neumí), práce, která musí přežít zavření
(cron nebo proces na pozadí).

## Co uvidíte
Zprávu o vyslání · pruh s počtem a stavem (aplikace i terminál) · možnost usměrnit nebo zastavit ·
výsledek jako shrnutí (důkaz si vyžádejte výslovně). Podagent si nesmí najmout dalšího (omezená hloubka).

## Zadání
Cíl + jak se pozná hotovo + co vrátit. Příklad: "Prozkoumej tři otázky paralelně, u každé vrať 5 bodů."
Strojová podoba výstupu: output_schema.

## Limity
Počet najednou: delegation.max_concurrent_children (u nás 10) · běží souběžně · trvalost: žijí
s rozhovorem, nepřežijí zavření rozhraní · přehled: /agents (terminál), pruh v aplikaci.

## Pasti z našeho provozu
1. "Hotovo" od podagenta je tvrzení -> ověřovat vlastním dotazem (soubor, DB, HTTP kód).
2. Potřeboval naše rozhodnutí -> ptát se neumí; zadat hlavnímu agentovi nebo říct předem, jak rozhodnout.
3. Rozdělaná práce po ukončení rozhovoru -> podagenti nejsou trvalá služba; použít cron/background.
4. Viditelné úpravy od podagenta nedopadly dobře -> na viditelné věci hlavní agent.
5. Cena: každý má vlastní kontext; delegovat promyšleně.

## Hotové vzory
Rešerše více témat paralelně · kontrola kódu · porovnání variant (stejná struktura) · nejdřív posbírat, pak rozhodnout.

## Tipy
Zadat, co přesně vrátit · říct, jak se práce prokáže · delegovat nezávislé úlohy · hlídat běžící
práci v přehledu.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🐝</span><div><strong>A subagent is a helper the agent sends off with a clear brief.</strong>
It gets its own conversation and its own terminal, works independently, and only <em>its summary</em>
comes back — not every intermediate step. That is why your conversation does not fill up with what
it tried along the way.</div></div>

<h2>When splitting the work pays off</h2>
<table class="wiki-tabulka">
<tr><th>Good fit</th><th>Why</th></tr>
<tr><td>A reasoning-heavy job (root-causing a bug, reviewing code, synthesising research)</td><td>The subagent gets the whole space to itself and disturbs nobody</td></tr>
<tr><td>Work that would flood the main conversation with data</td><td>Only the result returns, not hundreds of lines of intermediate output</td></tr>
<tr><td>Several independent branches at once</td><td>They run in parallel — three investigations instead of three in a row</td></tr>
<tr><td>A fresh look without bias</td><td>The subagent does not see what you already assumed, so nothing stops it from saying the opposite</td></tr>
</table>
<table class="wiki-tabulka">
<tr><th>Poor fit — do it another way</th><th>How</th></tr>
<tr><td>One tool call or a small file edit</td><td>Just ask for it directly; you save time and money</td></tr>
<tr><td>Mechanical work with logic between steps</td><td>A script — reproducible and exact</td></tr>
<tr><td>A job that needs to ask you something</td><td>Subagents cannot ask — the main agent does that</td></tr>
<tr><td>Work that must keep running after you close the interface</td><td>A scheduled job or a background process — see <a href="/en/wiki/getting-started/scheduled-tasks/">Scheduled tasks (cron)</a></td></tr>
</table>

<h2>What you see in your conversation</h2>
<table class="wiki-tabulka">
<tr><th>What appears</th><th>What it means</th></tr>
<tr><td>"I sent three helpers after that."</td><td>The main agent keeps working; results arrive as messages</td></tr>
<tr><td>A frame with a count and status</td><td>In the app and in the terminal you see who is running, for how long and what they did last</td></tr>
<tr><td>A way to steer or stop them</td><td>When a subagent heads the wrong way, guide it or end it — no need to wait it out</td></tr>
<tr><td>The result as a summary</td><td>When you need proof too (a file listing, an HTTP code), ask for it explicitly</td></tr>
</table>
<p class="note">A subagent can neither ask you anything nor hire another subagent — nesting has a
limit. When a task needs a conversation with a human, it belongs in the main conversation.</p>
<p><strong>A one-shot run is a special case.</strong> When the agent answers and exits
(<code>hermes -q "…"</code>, <code>chat --oneshot</code>, or a query with no terminal), it waits for
its helpers and returns their results in <em>the same</em> answer — after exit there is nowhere to
deliver them. Concurrency stays as before, but the number of helpers in a one-shot run is capped
separately (<code>delegation.oneshot_max_children</code>, default <strong>2</strong>, <code>0</code> =
unlimited). Interactive chats and gateway sessions keep the usual background behaviour.</p>

<h2>Briefing a subagent</h2>
<p>Write the brief like a work order: what the goal is, how you will know it is done, and what it
should bring back.</p>
<div class="code-block"><span class="p">❯</span> Find what three VPS options cost from Czech providers.<span class="p">
❯</span> For each, give the price in CZK, what it includes and a link. Return nothing else.


<span class="p">❯</span> Review this code change for bugs.<span class="p">
❯</span> Return a list of findings: what, where and how it shows up. If there is nothing, say so.


<span class="p">❯</span> Go through these three sites and compare them.<span class="p">
❯</span> Give me a table: what they have, what they lack and how they differ.</div>
<p class="note">When you want the answer in a machine-readable shape (a table, a list of items),
you can give the subagent a fixed output shape (<code>output_schema</code>) — handy when a script
processes the result.</p>

<h2>How many can run</h2>
<table class="wiki-tabulka">
<tr><th>Thing</th><th>How it works</th></tr>
<tr><td>How many at once</td><td>Bounded by <code>delegation.max_concurrent_children</code> (10 in our setup)</td></tr>
<tr><td>Concurrency</td><td>Tasks start together and results arrive as they finish</td></tr>
<tr><td>Durability</td><td>Subagents live with the conversation that spawned them — they do not survive closing the interface</td></tr>
<tr><td>Visibility</td><td><code>/agents</code> in the terminal, the frame above the composer in the app</td></tr>
</table>

<h2>Pitfalls from our systems</h2>
<table class="wiki-tabulka">
<tr><th>What happened</th><th>What to do</th></tr>
<tr><td><strong>A subagent reported "done" and nothing had changed.</strong> Its report is a claim, not evidence</td><td>Verify the outcome yourself — a file, a database query, the page's HTTP code. Put the proof into the brief</td></tr>
<tr><td><strong>A subagent got stuck on something that needed our decision</strong></td><td>It cannot ask. Either give the job to the main agent, or tell the subagent up front how to decide</td></tr>
<tr><td><strong>Work was left half-finished when the conversation ended</strong></td><td>Subagents are not a durable service. Anything that must outlive the session belongs in a scheduled job or a background process</td></tr>
<tr><td><strong>A subagent did visible edits and the result was poor</strong></td><td>For things that matter and are visible, the main agent is the better choice — it holds the whole brief. We keep subagents for research and for work that floods context</td></tr>
<tr><td><strong>Ten subagents cost more than we expected</strong></td><td>Each has its own context, so you pay for each separately. Delegate deliberately, not "just in case, everywhere"</td></tr>
</table>

<h2>Ready-made patterns</h2>
<table class="wiki-tabulka">
<tr><th>Pattern</th><th>What it looks like</th></tr>
<tr><td>Research several topics at once</td><td>"Investigate these three questions in parallel and return five points for each."</td></tr>
<tr><td>Code review</td><td>The subagent hunts bugs and security risks while the main agent keeps working</td></tr>
<tr><td>Comparing options</td><td>Each subagent examines one option and returns the same structure, so they can be compared</td></tr>
<tr><td>Gather, then decide</td><td>Several subagents collect material and the main agent draws the conclusion</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Say exactly what it should return</td><td>A shapeless summary is hard to use; "a table: price, what it includes, link" is usable immediately</td></tr>
<tr><td>Say how the work will be proven</td><td>Then nobody can just claim it is done</td></tr>
<tr><td>Give subagents jobs that do not depend on each other</td><td>They then really run in parallel instead of waiting</td></tr>
<tr><td>Watch work in progress</td><td>Stopping a subagent that went the wrong way is cheaper than finishing a bad result</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/features/tools/"><strong>Tools and toolsets</strong><span>Everything the agent can do</span></a>
<a href="/en/wiki/getting-started/scheduled-tasks/"><strong>Scheduled tasks (cron)</strong><span>Work that outlives the interface</span></a>
<a href="/en/wiki/features/sessions/"><strong>Sessions and recovery</strong><span>Where to look for what got lost</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Delegation in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What a subagent is
A helper the agent sends off with a clear brief: its own conversation, its own terminal,
independent work. Only its summary returns to the main conversation (not intermediate steps).

## When to delegate
Good: reasoning-heavy jobs (root cause, code review, research synthesis), work that would flood
context, independent parallel branches, a fresh unbiased look.
Poor: one tool call or a small edit (ask directly), mechanical work (a script), a job needing a
question to a human (subagents cannot ask), work that must outlive the interface (cron/background).

## What you see
A message that helpers were sent · a frame with count and status (app and terminal) · a way to steer
or stop them · the result as a summary (ask explicitly for proof). Subagents cannot hire further
subagents (nesting is limited).

## Briefing
Goal + how you know it is done + what to return. Example: "Investigate three questions in parallel,
return 5 points for each." Machine-readable output: output_schema.

## Limits
At once: delegation.max_concurrent_children (10 in our setup) · run in parallel · durability: they
live with the spawning conversation and do not survive closing the interface · visibility: /agents
in the terminal, the frame in the app.

## Pitfalls from our systems
1. "Done" from a subagent is a claim -> verify yourself (file, DB, HTTP code).
2. It needed our decision -> it cannot ask; give the job to the main agent or say how to decide.
3. Work left half done when the conversation ended -> subagents are not durable; use cron/background.
4. Visible edits done by a subagent came out poor -> keep visible work with the main agent.
5. Cost: each subagent has its own context; delegate deliberately.

## Ready-made patterns
Parallel research · code review · comparing options (same structure) · gather then decide.

## Tips
Say exactly what to return · say how the work will be proven · delegate independent jobs · watch
work in progress.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(18)
    stranka = najdi(18)
    assert stranka and stranka["nazev"] == "Podagenti"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Podagenti — když práci zvládne víc pomocníků",
        "Kdy se vyplatí rozdělit práci mezi víc agentů, jak se o běžící pomocníky starat, jak psát zadání a na co si dát pozor, když podagent tvrdí, že je hotovo.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Podagenti",
        "Pomocníci, kteří dostanou vlastní zadání a vrátí jen výsledek: kdy se vyplatí, kdy ne a jak je pohlídat.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Podagenti — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Subagents — when several helpers can share the work",
        "When splitting work between agents pays off, how to look after running helpers, how to write a brief and what to watch when a subagent claims it is done.",
        OBRAZEK, "Wiki · Features in depth", "Subagents",
        "Helpers that get their own brief and return only the result: when they pay off, when they do not, and how to keep an eye on them.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Subagents — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
