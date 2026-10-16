#!/usr/bin/env python3
"""Postaví stránku wiki „Sezení a jejich obnova" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-sessions.md (ukládání, navazování, pojmenování,
správní příkazy, hledání, předání mezi platformami, úložiště, udržování a stárnutí).

Naše zkušenosti: dlouhý rozhovor se zkracuje a vzniká pokračování; dávno zapomenuté detaily
se dohledávají hledáním v rozhovorech; databáze stavu umí narůst do gigabajtů.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "16. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/sessions"
OBRAZEK = "wiki-sezeni"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🗂️</span><div><strong>Každý rozhovor se ukládá sám — včetně toho, co agent dělal.</strong>
Když zavřete terminál, nic se neztratí. Rozhovory se dají dohledat, navázat v jiném okně
a klidně i na jiné platformě. Nemusíte si nic kopírovat do poznámek.</div></div>

<h2>Co je „sezení“ (session)</h2>
<p>Jeden rozhovor = jedno sezení. Ukládá se do jedné databáze, takže se v ní dá hledat a dá se
v něm pokračovat po týdnech:</p>
<table class="wiki-tabulka">
<tr><th>Kde to je</th><th>Co v tom je</th></tr>
<tr><td><code>~/.hermes/state.db</code></td><td>Všechny rozhovory a jejich stav: texty, volání nástrojů, výsledky, časy, spotřeba tokenů, název rozhovoru</td></tr>
<tr><td>Paměť (<code>memories/</code>)</td><td>Jen krátké poznámky, které platí pořád — viz <a href="/wiki/zaciname/pamet/">Paměť agenta</a></td></tr>
</table>
<p class="note">Databáze používá režim, který umožňuje čtení i zápis zároveň — proto do ní může
nahlížet víc částí Hermese (rozhraní, správce zpráv, plánované úlohy) bez zamykání.</p>

<h2>Navázání na rozhovor</h2>
<div class="code-block"><span class="p">❯</span> hermes -c                          <span class="c"># poslední rozhovor v tomto terminálu</span>
<span class="p">❯</span> hermes -c "můj projekt"            <span class="c"># podle názvu</span>
<span class="p">❯</span> hermes --resume 20260409_000000_aa11bb   <span class="c"># podle identifikátoru</span>
<span class="p">❯</span> hermes --resume latest --in ./projekt     <span class="c"># poslední rozhovor k téhle složce</span></div>
<table class="wiki-tabulka">
<tr><th>Když máte otevřených víc terminálů</th><th>Co se stane</th></tr>
<tr><td>V každém okně dáte <code>hermes -c</code></td><td>Každé okno si naváže <em>svůj</em> rozhovor, ne ten globálně poslední</td></tr>
<tr><td>Rozhovor byl smazaný nebo je záznam starší 30 dnů</td><td>Naváže se poslední rozhovor, který existuje</td></tr>
<tr><td>Toto chování chcete vypnout</td><td><code>session.terminal_continue: false</code> v nastavení</td></tr>
</table>

<h2>Pojmenujte si rozhovory</h2>
<p>Hermes po první výměně sám vymyslí krátký název (tři až sedm slov), takže se v seznamu
neztratíte. Když chcete vlastní, použijte příkaz lomítkem přímo v rozhovoru:</p>
<div class="code-block"><span class="p">❯</span> /title oprava webu
<span class="p">❯</span> hermes sessions rename 20260409_000000_aa11bb "oprava webu"</div>
<p class="note">Název musí být jedinečný a nejvýše 100 znaků; diakritika i emoji jsou v pořádku.
Automatický název se doplní jen jednou a jen když si název nenastavíte sami.</p>

<h2>Přehled a úklid</h2>
<table class="wiki-tabulka">
<tr><th>Co chcete</th><th>Příkaz</th></tr>
<tr><td>Vidět poslední rozhovory</td><td><code>hermes sessions list</code> (výchozně 20), <code>… --limit 50</code></td></tr>
<tr><td>Jen z jedné platformy nebo složky</td><td><code>hermes sessions list --source telegram</code>, <code>… --workspace ~/code/projekt</code></td></tr>
<tr><td>Souhrnná čísla</td><td><code>hermes sessions stats</code></td></tr>
<tr><td>Důležité rozhovory si připnout</td><td><code>hermes sessions pin &lt;id&gt;</code>, přehled <code>hermes sessions pinned</code></td></tr>
<tr><td>Vyexportovat rozhovor (do Markdownu, HTML, JSON…)</td><td><code>hermes sessions export --format md --session-id &lt;id&gt;</code></td></tr>
<tr><td>Uklidit staré rozhovory</td><td><code>hermes sessions prune --older-than 30 --dry-run</code> (napřed jen ukázat)</td></tr>
<tr><td>Přenést historii z jiného nástroje</td><td><code>hermes sessions import --from claude</code> / <code>--from codex</code></td></tr>
</table>
<p class="note"><code>--dry-run</code> u úklidu znamená „jen mi ukaž, co bys smazal“. Dokud ho
nepustíte bez tohoto přepínače, nic se nesmaže.</p>

<h2>Jak agent hledá ve starých rozhovorech</h2>
<p>Agent má nástroj na hledání v celé historii. Nepoužívá k tomu model — hledá přímo v databázi
plnotextově, takže je to rychlé a nic se „nedomýšlí“:</p>
<div class="code-block"><span class="p">❯</span> Jak jsme to tenkrát řešili s certifikátem?
<span class="p">❯</span> Najdi mi v naší historii, jaký byl ten příkaz na zálohu databáze.</div>
<p><strong>Praktický rozdíl:</strong> paměť si agent nosí pořád u sebe (a je proto krátká),
kdežto hledání v rozhovorech jde do hloubky — a najde i to, co se do paměti nevešlo.</p>

<h2>Dlouhé rozhovory a jejich pokračování</h2>
<p>Každý model má omezené místo na kontext. Když rozhovor přeteče, Hermes ho srovná (zhuští)
a pokračuje v <strong>novém sezení stejné řady</strong> — v seznamu se to pozná podle názvu
(<em>můj projekt</em>, <em>můj projekt #2</em>, <em>#3</em>). Navázání podle názvu vždycky vezme
nejnovější pokračování.</p>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co udělat</th></tr>
<tr><td>Chci srovnat rozhovor sám</td><td>Příkaz <code>/compress</code> v rozhovoru</td></tr>
<tr><td>Chci začít s čistou hlavou</td><td>Příkaz <code>/new</code> — paměť se znovu načte, historie zůstává dohledatelná</td></tr>
<tr><td>Chci pokračovat tam, kde jsem skončil</td><td><code>hermes -c "název projektu"</code> — vezme nejnovější pokračování</td></tr>
</table>

<h2>Rozhovory z jiných platforem</h2>
<p>Rozhovor není vázaný na jedno rozhraní. Můžete ho začít v terminálu a poslat si ho do chatu
na mobil:</p>
<div class="code-block"><span class="p">❯</span> /handoff telegram      <span class="c"># předat rozhovor do Telegramu</span></div>
<p class="note">Na mobilních platformách má každý chat své vlastní sezení (soukromý chat, skupina,
vlákno). Když se ptáte ve skupině, agent si pamatuje kontext té skupiny — ne vašich soukromých
rozhovorů.</p>

<h2>Automatické udržování</h2>
<p>Bez údržby by databáze rostla pořád dál — u běžících botů a plánovaných úloh to dělá
gigabajty za pár týdnů. Hermes proto stará sezení uklízí sám:</p>
<table class="wiki-tabulka">
<tr><th>Nastavení</th><th>Výchozí hodnota</th><th>Co dělá</th></tr>
<tr><td><code>sessions.auto_prune</code></td><td>zapnuto</td><td>Stará sezení se uklidí při startu (rozhraní, správce zpráv, plánované úlohy)</td></tr>
<tr><td><code>sessions.retention_days</code></td><td>90 dnů</td><td>Jak dlouho se nečinné rozhovory drží</td></tr>
<tr><td><code>sessions.min_interval_hours</code></td><td>24 hodin</td><td>Jak často se úklid vůbec pouští</td></tr>
</table>
<p class="note">Databáze se po úklidu zmenší jen tehdy, když je co uvolnit — je to záměr,
ne chyba. Když se do nastavení zadá nesmyslná hodnota (například záporné dny), Hermes úklid
přeskočí a napíše varování, místo aby smazal všechno.</p>

<h2>Pasti z našeho provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co se stalo</th><th>Co s tím</th></tr>
<tr><td><strong>Po dlouhé práci se z rozhovoru ztratily detaily</strong></td><td>Rozhovor se zhušťuje, když se zaplní kontext — to je normální. Podrobnosti zůstávají v historii: stačí se zeptat („najdi v naší historii…“)</td></tr>
<tr><td><strong>Domnívali jsme se, že si agent pamatuje něco, co zaznělo před měsícem</strong></td><td>V paměti to nebylo (je krátká). Dohledá se to hledáním v rozhovorech, ale přesněji: <em>„podívej se do historie, jak jsme nastavili…“</em></td></tr>
<tr><td><strong>Databáze stavu narostla na stovky megabajtů</strong></td><td>Vypnuté udržování + hodně rozhovorů z platforem a plánovaných úloh. Pomůže <code>hermes sessions stats</code>, připnutí důležitých a <code>prune</code> s <code>--dry-run</code></td></tr>
<tr><td><strong>Ve dvou panelech terminálu se pořád navazoval jeden rozhovor</strong></td><td>Chování <code>-c</code> je vázané na terminál, takže si každý panel drží svůj rozhovor — ale jen když v něm byl spuštěn aspoň jednou. Nový panel = nový rozhovor</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Důležitý rozhovor si připněte nebo pojmenujte</td><td>V seznamu plném automatických názvů se pak najde jedna dvě</td></tr>
<tr><td>Na nový úkol nový rozhovor (<code>/new</code>)</td><td>Agent má čistý kontext a znovu si načte, co o vás ví</td></tr>
<tr><td>Před úklidem si udělejte export</td><td><code>hermes sessions export</code> udělá zálohu, ke které se dá vrátit</td></tr>
<tr><td>Hledejte v historii místo vzpomínání</td><td>Agent to umí plnotextově a bez výmyslů — stačí říct, co hledáte</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/pamet/"><strong>Paměť agenta</strong><span>Co si pamatuje pořád a co se hledá v historii</span></a>
<a href="/wiki/funkce/tui/"><strong>TUI — práce v terminálu</strong><span>Přepínač rozhovorů a navazování</span></a>
<a href="/wiki/funkce/podagenti/"><strong>Podagenti</strong><span>Když práci dostane víc pomocníků</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/sessions" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Sezení do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co je sezení
Jeden rozhovor = jedno sezení, ukládá se samo (i s voláními nástrojů).
Úložiště: ~/.hermes/state.db (plnotextové hledání, režim WAL).
Paměť (memories/) je něco jiného — krátké trvalé poznámky.

## Navázání
hermes -c · hermes -c "název" · hermes --resume <id> · hermes --resume latest --in ./projekt
-c je vázané na terminál: každý panel si drží svůj rozhovor; starší než 30 dnů -> vezme poslední.
Vypnutí: session.terminal_continue: false

## Pojmenování
Automaticky 3-7 slov po první výměně; vlastní: /title oprava webu nebo
hermes sessions rename <id> "oprava webu". Unikátní, max 100 znaků, diakritika a emoji ok.

## Přehled a úklid
hermes sessions list [--limit 50] [--source telegram] [--workspace <složka>] · sessions stats ·
sessions pin <id> / pinned · sessions export --format md --session-id <id> ·
sessions prune --older-than 30 --dry-run (napřed jen ukázat) ·
sessions import --from claude|codex

## Hledání v historii
Agent má nástroj pro plnotextové hledání ve všech rozhovorech (bez volání modelu).
Paměť = krátká a vždy po ruce; hledání = do hloubky, najde i to, co se do paměti nevešlo.

## Dlouhé rozhovory
Přetečení kontextu -> zhuštění a pokračování jako nové sezení stejné řady (název, název #2, #3).
/compress = srovnat ručně · /new = čistý začátek (paměť se načte znovu, historie zůstává).
Navázání podle názvu vezme nejnovější pokračování.

## Platformy
/handoff telegram předá rozhovor do chatu na mobilu. Na platformách má každý chat (DM, skupina,
vlákno) vlastní sezení.

## Automatické udržování
sessions.auto_prune (výchozí zapnuto) · sessions.retention_days (90) · sessions.min_interval_hours (24).
Databáze se zmenší jen když je co uvolnit. Nesmyslná hodnota (záporné dny) -> úklid se přeskočí s varováním.

## Pasti z našeho provozu
1. Ztráta detailů v dlouhém rozhovoru = zhuštění kontextu; detaily zůstávají v historii (zeptat se).
2. Domněnka, že si agent pamatuje měsíc starý detail -> patřil do paměti, jinak hledat v historii.
3. state.db narostla na stovky MB (vypnuté udržování, platformy, cron) -> sessions stats + pin + prune.
4. Dva panely terminálu: -c je vázané na terminál, nový panel = nový rozhovor.

## Tipy
Připnout/pojmenovat důležité rozhovory · nový úkol = /new · před úklidem export · hledat v historii
místo vzpomínání.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🗂️</span><div><strong>Every conversation is saved by itself — including what the agent did.</strong>
Closing the terminal loses nothing. Conversations can be found again, resumed in another window and
even handed over to another platform. You do not need to copy anything into notes.</div></div>

<h2>What a session is</h2>
<p>One conversation = one session. It is stored in a single database, so it can be searched and
resumed weeks later:</p>
<table class="wiki-tabulka">
<tr><th>Where it lives</th><th>What is in it</th></tr>
<tr><td><code>~/.hermes/state.db</code></td><td>All conversations and their state: messages, tool calls, results, timestamps, token counts, the session title</td></tr>
<tr><td>Memory (<code>memories/</code>)</td><td>Only short notes that apply forever — see <a href="/en/wiki/getting-started/memory/">Agent memory</a></td></tr>
</table>
<p class="note">The database runs in a mode that allows readers and one writer at the same time —
which is why several parts of Hermes (interfaces, the messaging gateway, scheduled jobs) can look
into it without locking each other out.</p>

<h2>Resuming a conversation</h2>
<div class="code-block"><span class="p">❯</span> hermes -c                          <span class="c"># the latest conversation in this terminal</span>
<span class="p">❯</span> hermes -c "my project"             <span class="c"># by title</span>
<span class="p">❯</span> hermes --resume 20260409_000000_aa11bb   <span class="c"># by session id</span>
<span class="p">❯</span> hermes --resume latest --in ./project     <span class="c"># the latest one for this folder</span></div>
<table class="wiki-tabulka">
<tr><th>With several terminals open</th><th>What happens</th></tr>
<tr><td>You run <code>hermes -c</code> in each of them</td><td>Each window resumes <em>its own</em> conversation, not the globally most recent one</td></tr>
<tr><td>The conversation was deleted or the breadcrumb is over 30 days old</td><td>It falls back to the latest existing conversation</td></tr>
<tr><td>You want this off</td><td><code>session.terminal_continue: false</code> in the settings</td></tr>
</table>

<h2>Give your conversations names</h2>
<p>After the first exchange Hermes invents a short title (three to seven words) so you do not get
lost in the list. For your own, use the slash command right in the conversation:</p>
<div class="code-block"><span class="p">❯</span> /title website fix
<span class="p">❯</span> hermes sessions rename 20260409_000000_aa11bb "website fix"</div>
<p class="note">A title must be unique and at most 100 characters; accents and emoji are fine.
An automatic title is added once and only if you have not set one yourself.</p>

<h2>Overview and housekeeping</h2>
<table class="wiki-tabulka">
<tr><th>What you want</th><th>Command</th></tr>
<tr><td>See recent conversations</td><td><code>hermes sessions list</code> (20 by default), <code>… --limit 50</code></td></tr>
<tr><td>Only from one platform or folder</td><td><code>hermes sessions list --source telegram</code>, <code>… --workspace ~/code/project</code></td></tr>
<tr><td>Summary numbers</td><td><code>hermes sessions stats</code></td></tr>
<tr><td>Pin the important ones</td><td><code>hermes sessions pin &lt;id&gt;</code>, list them with <code>hermes sessions pinned</code></td></tr>
<tr><td>Export a conversation (Markdown, HTML, JSON…)</td><td><code>hermes sessions export --format md --session-id &lt;id&gt;</code></td></tr>
<tr><td>Clean up old conversations</td><td><code>hermes sessions prune --older-than 30 --dry-run</code> (show first)</td></tr>
<tr><td>Bring history in from another tool</td><td><code>hermes sessions import --from claude</code> / <code>--from codex</code></td></tr>
</table>
<p class="note"><code>--dry-run</code> on a cleanup means "just show me what you would delete".
Nothing is removed until you run it without that flag.</p>

<h2>How the agent searches past conversations</h2>
<p>The agent has a tool that searches the whole history. It makes no model calls — it queries the
database full-text, so it is fast and invents nothing:</p>
<div class="code-block"><span class="p">❯</span> How did we deal with the certificate back then?
<span class="p">❯</span> Find in our history the exact command we used for the database backup.</div>
<p><strong>The practical difference:</strong> memory is what the agent always carries with it (and is
therefore short), while history search goes deep — and finds what never fit into memory.</p>

<h2>Long conversations and their continuations</h2>
<p>Every model has a limited context window. When a conversation overflows, Hermes compresses it and
continues in a <strong>new session in the same lineage</strong> — visible in the list as
<em>my project</em>, <em>my project #2</em>, <em>#3</em>. Resuming by title always picks the latest
continuation.</p>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>I want to compress it myself</td><td>The <code>/compress</code> command inside the conversation</td></tr>
<tr><td>I want a clean start</td><td><code>/new</code> — memory is re-read, history stays searchable</td></tr>
<tr><td>I want to continue where I left off</td><td><code>hermes -c "project name"</code> — it picks the newest continuation</td></tr>
</table>

<h2>Conversations across platforms</h2>
<p>A conversation is not tied to one interface. You can start it in the terminal and send it to
chat on your phone:</p>
<div class="code-block"><span class="p">❯</span> /handoff telegram      <span class="c"># hand the conversation over to Telegram</span></div>
<p class="note">On messaging platforms every chat has its own session (direct message, group,
thread). When you ask in a group, the agent remembers that group's context — not your private
conversations.</p>

<h2>Automatic housekeeping</h2>
<p>Without maintenance the database would only grow — on running bots and scheduled jobs it reaches
gigabytes within weeks. Hermes therefore cleans up old sessions by itself:</p>
<table class="wiki-tabulka">
<tr><th>Setting</th><th>Default</th><th>What it does</th></tr>
<tr><td><code>sessions.auto_prune</code></td><td>on</td><td>Old sessions are pruned at startup (interface, messaging gateway, scheduled jobs)</td></tr>
<tr><td><code>sessions.retention_days</code></td><td>90 days</td><td>How long idle conversations are kept</td></tr>
<tr><td><code>sessions.min_interval_hours</code></td><td>24 hours</td><td>How often the sweep may run at all</td></tr>
</table>
<p class="note">The database file only shrinks when there is something to reclaim — that is by
design, not a bug. If the setting gets a nonsensical value (negative days, for example), Hermes
skips the sweep and logs a warning instead of deleting everything.</p>

<h2>Pitfalls from our systems</h2>
<table class="wiki-tabulka">
<tr><th>What happened</th><th>What to do</th></tr>
<tr><td><strong>After long work, details disappeared from a conversation</strong></td><td>The conversation gets compressed when context fills up — that is normal. Details stay in history: just ask ("search our history for…")</td></tr>
<tr><td><strong>We assumed the agent remembered something from a month ago</strong></td><td>It was never in memory (which is short). It can be found by searching conversations — but be explicit: <em>"look in the history for how we set up…"</em></td></tr>
<tr><td><strong>The state database grew to hundreds of megabytes</strong></td><td>Pruning off plus many platform conversations and scheduled jobs. <code>hermes sessions stats</code>, pin the important ones, then <code>prune</code> with <code>--dry-run</code></td></tr>
<tr><td><strong>Two terminal panes kept resuming the same conversation</strong></td><td><code>-c</code> is terminal-aware, so each pane keeps its own — but only once it has run at least once inside. A brand-new pane starts a new conversation</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Pin or name an important conversation</td><td>In a list full of automatic titles you then find the right one in seconds</td></tr>
<tr><td>A new task gets a new conversation (<code>/new</code>)</td><td>The agent starts with clean context and re-reads what it knows about you</td></tr>
<tr><td>Export before cleaning up</td><td><code>hermes sessions export</code> gives you a backup to come back to</td></tr>
<tr><td>Search history instead of trying to remember</td><td>The agent does it full-text and invents nothing — just say what you are looking for</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/memory/"><strong>Agent memory</strong><span>What is remembered always versus searched in history</span></a>
<a href="/en/wiki/features/tui/"><strong>TUI — working in the terminal</strong><span>Session switcher and resuming</span></a>
<a href="/en/wiki/features/subagents/"><strong>Subagents</strong><span>When the work goes to several helpers</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/sessions" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Sessions in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What a session is
One conversation = one session, saved automatically (tool calls included).
Storage: ~/.hermes/state.db (full-text search, WAL mode).
Memory (memories/) is something else — short durable notes.

## Resuming
hermes -c · hermes -c "title" · hermes --resume <id> · hermes --resume latest --in ./project
-c is terminal-aware: each pane keeps its own conversation; breadcrumbs older than 30 days fall back
to the latest. Disable with session.terminal_continue: false

## Naming
Automatic 3-7 words after the first exchange; your own: /title website fix or
hermes sessions rename <id> "website fix". Unique, max 100 characters, accents and emoji fine.

## Overview and housekeeping
hermes sessions list [--limit 50] [--source telegram] [--workspace <folder>] · sessions stats ·
sessions pin <id> / pinned · sessions export --format md --session-id <id> ·
sessions prune --older-than 30 --dry-run (show first) · sessions import --from claude|codex

## Searching history
The agent has a full-text search tool over all conversations (no model calls).
Memory = short and always at hand; history search = deep, finds what never fit into memory.

## Long conversations
Context overflow -> compression and continuation as a new session in the same lineage
(title, title #2, #3). /compress to do it manually · /new for a clean start (memory re-read,
history stays searchable). Resuming by title picks the newest continuation.

## Platforms
/handoff telegram transfers the conversation to chat on your phone. On messaging platforms every
chat (DM, group, thread) has its own session.

## Automatic housekeeping
sessions.auto_prune (on by default) · sessions.retention_days (90) · sessions.min_interval_hours (24).
The file only shrinks when there is something to reclaim. A nonsensical value (negative days) skips
the sweep with a warning instead of deleting everything.

## Pitfalls from our systems
1. Lost details in a long conversation = context compression; details stay in history (just ask).
2. Assuming the agent remembers a month-old detail -> it belonged in memory, otherwise search history.
3. state.db grew to hundreds of MB (pruning off, platforms, cron) -> sessions stats, pin, prune.
4. Two terminal panes: -c is terminal-aware, a brand-new pane starts a new conversation.

## Tips
Pin/name important conversations · a new task gets /new · export before cleanup · search history
instead of trying to remember.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(17)
    stranka = najdi(17)
    assert stranka and stranka["nazev"] == "Sezení a jejich obnova"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Sezení a jejich obnova — rozhovory, které zůstávají",
        "Jak se ukládají rozhovory, jak se na ně navazuje podle názvu i identifikátoru, jak v nich hledat, kdy se zhušťují a jak je udržovat, aby databáze nerostla.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Sezení a jejich obnova",
        "Zavřený terminál nic neztratí: rozhovory se ukládají samy, dají se dohledat, navázat a přenést jinam. A taky se o ně Hermes sám stará.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Sezení a jejich obnova — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Sessions and recovery — conversations that persist",
        "How conversations are stored, how to resume them by title or id, how to search them, when they get compressed and how they are kept from growing the database forever.",
        OBRAZEK, "Wiki · Features in depth", "Sessions and recovery",
        "Closing the terminal loses nothing: conversations are saved automatically, can be found, resumed and handed over elsewhere. Hermes also looks after them.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Sessions and recovery — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
