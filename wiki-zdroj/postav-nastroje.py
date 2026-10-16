#!/usr/bin/env python3
"""Postaví stránku wiki „Nástroje a toolsety" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-tools.md (registry nástrojů, terminálové
backendy, běh na pozadí, sudo), reference-toolsets-reference.md (sady nástrojů, `disabled_toolsets`),
user-guide-features-tool-search.md (co se stane, když je nástrojů moc),
user-guide-features-tool-gateway.md (Nous Tool Gateway).

Naše zkušenosti: MCP server vracející data jiného projektu, maskování tajných údajů ve výstupu
terminálu a nástroj, který hlásí úspěch, i když se nic nestalo.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "16. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/tools"
OBRAZEK = "wiki-nastroje"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🧰</span><div><strong>Nástroj je to, čím agent skutečně něco udělá.</strong>
Mluvit umí každý model — ale zapsat soubor, spustit příkaz, otevřít web nebo se zeptat databáze
dokáže jen tehdy, když má na to nástroj. <em>Sada nástrojů</em> (toolset) je pak balík, který se
zapíná a vypíná celý najednou.</div></div>

<h2>Nástroje versus sada nástrojů</h2>
<p>Rozdíl je jako mezi nářadím a kufrem: nástroj je jedna věc, sada je kufr, který se bere na stavbu.
Vy rozhodujete, jaké kufry agent dostane — a tím i to, co může dělat.</p>
<table class="wiki-tabulka">
<tr><th>Pojem</th><th>Co to je</th><th>Příklad</th></tr>
<tr><td><strong>Nástroj</strong></td><td>Jedna konkrétní schopnost s pevným zadáním a výstupem</td><td><code>web_search</code>, <code>read_file</code>, <code>terminal</code>, <code>delegate_task</code></td></tr>
<tr><td><strong>Sada nástrojů</strong></td><td>Skupina nástrojů, která se zapíná nebo vypíná jako celek</td><td><code>web</code>, <code>file</code>, <code>terminal</code>, <code>coding</code></td></tr>
<tr><td><strong>Připojení (MCP)</strong></td><td>Cizí program, který si přinese vlastní nástroje</td><td>databáze, firemní systém, nástroj třetí strany</td></tr>
</table>

<h2>Co agent umí bez nastavování</h2>
<p>Po instalaci má agent k dispozici širokou sadu nástrojů. Rozdělení podle oblastí:</p>
<table class="wiki-tabulka">
<tr><th>Oblast</th><th>Příklady nástrojů</th><th>K čemu</th></tr>
<tr><td>Web</td><td><code>web_search</code>, <code>web_extract</code></td><td>Hledání a čtení stránek</td></tr>
<tr><td>Terminál a soubory</td><td><code>terminal</code>, <code>read_file</code>, <code>patch</code>, <code>process</code></td><td>Práce na serveru a v souborech</td></tr>
<tr><td>Prohlížeč</td><td><code>browser_navigate</code>, <code>browser_snapshot</code>, <code>browser_exec</code></td><td>Skutečný prohlížeč, kde je potřeba klikat</td></tr>
<tr><td>Média</td><td><code>vision_analyze</code>, <code>image_generate</code>, <code>text_to_speech</code></td><td>Podívat se na obrázek, vyrobit obrázek nebo hlas</td></tr>
<tr><td>Plánování a rozdělení práce</td><td><code>todo</code>, <code>clarify</code>, <code>execute_code</code>, <code>delegate_task</code></td><td>Rozdělit úkol, zeptat se, spustit skript, poslat práci podagentovi</td></tr>
<tr><td>Paměť a historie</td><td><code>memory</code>, <code>session_search</code></td><td>Trvalé poznámky a hledání ve starých rozhovorech</td></tr>
<tr><td>Plánované úlohy</td><td><code>cronjob_manage</code></td><td>Úkoly, které běží samy podle času</td></tr>
</table>
<p class="note">Přesný seznam si vypíšete kdykoli: <code>hermes tools</code>.</p>

<h2>Zapnutí a vypnutí sady nástrojů</h2>
<p>Když chcete, aby agent uměl jen to, co potřebujete, sady omezíte. Méně nástrojů = méně prostoru
pro omyl a rychlejší odpovědi.</p>
<div class="code-block"><span class="p">❯</span> hermes chat --toolsets "web,terminal"      <span class="c"># jen tyto dvě sady</span>
<span class="p">❯</span> hermes chat --toolsets all                 <span class="c"># všechno, co je k dispozici</span>
<span class="p">❯</span> hermes tools                               <span class="c"># přehled a zaškrtávání</span></div>
<p>Trvale se to nastavuje v souboru <code>config.yaml</code> profilu — buď výčtem povolených sad,
nebo naopak seznamem zakázaných:</p>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
enabled_toolsets: [web, file, terminal]
disabled_toolsets: [browser]        <span class="c"># prohlížeč nebude vůbec potřeba</span></div>
<p class="note">Pozor: <code>web_search</code> schválně <em>není</em> součástí sady <code>browser</code>,
takže vypnutím prohlížeče nepřijdete o hledání na webu.</p>

<h2>Když je nástrojů moc</h2>
<p>Se dvěma stovkami zapnutých nástrojů se model ztrácí — popisy všech nástrojů zabírají místo,
které by mohlo patřit vašemu zadání. Hermes to řeší <strong>hledáním v nástrojích</strong>:
venku nechá jen pár nejpoužívanějších a ostatní si vyžádá až ve chvíli, kdy je potřebuje.</p>
<table class="wiki-tabulka">
<tr><th>Kdy to nastane</th><th>Co se stane</th></tr>
<tr><td>Nástrojů je hodně (typicky přes 30)</td><td>Některé nástroje se schovají za hledání; agent si o ně řekne sám</td></tr>
<tr><td>Je to potřeba</td><td>Odpovědi jsou rychlejší a levnější, model se nerozptyluje</td></tr>
<tr><td>Není to vhodné</td><td>Když má agent dělat jednu úzkou věc pořád dokola — pak je lepší zapnout málo sad a hledání vypnout</td></tr>
</table>
<p class="note">Prakticky: když agent na váš dotaz sáhne po nástroji, který jste nečekali, podívejte se,
jestli nemá zapnutých sad víc, než potřebujete. Nastavení se dělá příkazem <code>hermes tools</code> —
bez ručního editování souborů.</p>

<h2>Kde nástroje běží (terminálové zázemí)</h2>
<p>Dokud agent spouští příkazy na vašem serveru, mluvíme o „místním“ zázemí. Jde to ale i jinam —
to se hodí, když mu nechcete dávat přístup do svého systému, nebo naopak když potřebujete
jiné prostředí, než máte na serveru.</p>
<table class="wiki-tabulka">
<tr><th>Zázemí</th><th>Kdy se hodí</th><th>Nastavení</th></tr>
<tr><td><code>local</code> (výchozí)</td><td>Vlastní server nebo VPS — nejjednodušší a nejrychlejší</td><td>není co nastavovat</td></tr>
<tr><td>vzdálený počítač přes SSH</td><td>Práce na jiném stroji, který už máte</td><td>přihlašovací údaje v nastavení zázemí</td></tr>
<tr><td>kontejner (Docker)</td><td>Chcete oddělit, co agent smí — vidí jen kontejner</td><td><code>terminal.backend</code> v <code>config.yaml</code></td></tr>
<tr><td>cloudové pískoviště (např. Modal, Vercel Sandbox)</td><td>Nemáte vlastní server a chcete, aby běžel jen na dobu úlohy</td><td><code>terminal.backend</code> + přístupové údaje</td></tr>
</table>
<div class="code-block"><span class="p">❯</span> hermes config set terminal.backend modal
<span class="p">❯</span> hermes config set terminal.backend singularity</div>
<p class="note">Kontejner <strong>není</strong> bezpečnostní záruka sám o sobě: chrání jen to, co do něj
agent nemá jak pustit. O oprávněních a schvalování příkazů je samostatná stránka
<a href="/wiki/zaciname/bezpecnost/">Bezpečnost</a>.</p>

<h2>Dlouhé úlohy a správcovská práva</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Jak to funguje</th></tr>
<tr><td>Úloha běží dlouho (záloha, kopírování, sledování logu)</td><td>Agent ji pustí <strong>na pozadí</strong> a může dělat jinou práci; stav si kdykoli vyžádá</td></tr>
<tr><td>Příkaz potřebuje <code>sudo</code></td><td>V interaktivním rozhovoru se objeví maskované pole pro heslo (v rámci sezení si ho pamatuje). Do kontejneru nebo na chat se heslo neposílá</td></tr>
<tr><td>Příkaz bez hesla, ale s právy</td><td>Funguje bez dotazu — není co vyplňovat</td></tr>
<tr><td>Úloha v podagentovi</td><td>Heslo vyplnit nelze — takový příkaz se musí spustit v hlavním rozhovoru</td></tr>
</table>

<h2>Tři pasti z našeho provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co se stalo</th><th>Jak se to pozná a co s tím</th></tr>
<tr><td><strong>Nástroj hlásil úspěch, ale nic se nestalo.</strong> Volání prošlo, výstup vypadal dobře, změna nikde</td><td>Neptejte se nástroje, jestli to udělal — <em>ověřte výsledek jinde</em>: v souboru, dotazem do databáze, HTTP kódem stránky. Do zadání pište, jak má být práce ověřená</td></tr>
<tr><td><strong>Připojený nástroj vracel data z jiného projektu.</strong> Server odpovídal správně, ale cizí databází (měli jsme dva projekty a jeden nástroj mezi nimi)</td><td>U cizích nástrojů si ověřte, na co jsou připojené, a ptejte se na konkrétní řádek, který znáte. Když nesedí, řešte připojení, ne agenta</td></tr>
<tr><td><strong>Tajné údaje se ve výstupu objevily jako <code>***</code></strong></td><td>Hermes tajemství ve výstupu maskuje. Nikdy je neověřujte tím, že si je necháte vypsat — výpis vyjde prázdný nebo falešně, i když je údaj správně. Používejte je přímo v příkazu</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Zapínejte jen sady, které opravdu používáte</td><td>Méně nástrojů znamená rychlejší a přesnější odpovědi</td></tr>
<tr><td>Do zadání pište, čím se má práce ověřit</td><td>„Ať stránka vrací 200“ nebo „ukaž mi řádek z databáze“ — pak se nedá nic jen tvrdit</td></tr>
<tr><td>Když agent umí všechno, ale nic pořádně, zužte rozsah</td><td>Úzké sady + jasné zadání dělají lepší výsledky než hromada nástrojů</td></tr>
<tr><td>Nové připojení testujte na tom, co znáte</td><td>Jednoduchý dotaz s očekávanou odpovědí odhalí špatné připojení dřív, než na něm postavíte práci</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/mcp-nastroje/"><strong>MCP nástroje</strong><span>Připojení cizích programů a dat</span></a>
<a href="/wiki/zaciname/bezpecnost/"><strong>Bezpečnost</strong><span>Co agentovi svěřit a co ne</span></a>
<a href="/wiki/funkce/podagenti/"><strong>Podagenti</strong><span>Když je práce na víc než jednoho agenta</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/tools" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Nástroje a zázemí do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Nástroj vs. sada nástrojů
Nástroj = jedna schopnost (web_search, read_file, terminal, delegate_task).
Sada (toolset) = balík, který se zapíná/vypíná celý (web, file, terminal, coding).
Přehled: hermes tools

## Co agent umí po instalaci (podle oblastí)
Web (web_search, web_extract) · Terminál a soubory (terminal, read_file, patch, process) ·
Prohlížeč (browser_navigate, browser_snapshot, browser_exec) · Média (vision_analyze,
image_generate, text_to_speech) · Plánování (todo, clarify, execute_code, delegate_task) ·
Paměť (memory, session_search) · Plánované úlohy (cronjob_manage)

## Zapnutí a vypnutí sad
hermes chat --toolsets "web,terminal"   |   hermes chat --toolsets all   |   hermes tools
Trvale v ~/.hermes/config.yaml: enabled_toolsets: [web, file, terminal] / disabled_toolsets: [browser]
web_search není součástí sady browser (vypnutí prohlížeče nebere hledání na webu).

## Když je nástrojů moc
Přes ~30 nástrojů se část schová za hledání v nástrojích a agent si je vyžádá sám — odpovědi jsou
rychlejší a levnější. Pro úzkou stále stejnou práci je lepší málo sad a hledání vypnout.

## Kde nástroje běží (terminálové zázemí)
local (výchozí, vlastní server) · vzdálený přes SSH · kontejner (Docker) · cloudové pískoviště
(Modal, Vercel Sandbox). Nastavení: hermes config set terminal.backend <backend>
Kontejner není bezpečnostní záruka — o oprávněních viz stránka Bezpečnost.

## Dlouhé úlohy a sudo
Dlouhý příkaz -> běh na pozadí, agent zvládne jinou práci.
sudo: v interaktivním rozhovoru maskované pole pro heslo (v rámci sezení si pamatuje);
do chatu ani podagenta se heslo neposílá; bez hesla (passwordless) proběhne bez dotazu.

## Tři pasti z našeho provozu
1. Nástroj hlásil úspěch, ale nic se nestalo -> ověřovat výsledek jinde (soubor, DB, HTTP kód).
2. Připojený nástroj vracel data z jiného projektu -> ověřit, na co je připojený, testovat známým dotazem.
3. Tajné údaje ve výstupu jako *** -> Hermes tajemství maskuje; neověřovat je výpisem, použít přímo v příkazu.

## Tipy
Zapínat jen používané sady · do zadání psát, čím se práce ověří · zužovat rozsah místo přidávání
nástrojů · nové připojení testovat na známém dotazu.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🧰</span><div><strong>A tool is how the agent actually does something.</strong>
Every model can talk — but writing a file, running a command, opening a website or querying a
database only happens when the agent has a tool for it. A <em>toolset</em> is a bundle that is
switched on and off as a whole.</div></div>

<h2>Tools versus toolsets</h2>
<p>The difference is like tools and a toolbox: a tool is one thing, a toolset is the box you take to
a job. You decide which boxes the agent gets — and that also decides what it can do.</p>
<table class="wiki-tabulka">
<tr><th>Term</th><th>What it is</th><th>Example</th></tr>
<tr><td><strong>Tool</strong></td><td>One specific ability with a fixed input and output</td><td><code>web_search</code>, <code>read_file</code>, <code>terminal</code>, <code>delegate_task</code></td></tr>
<tr><td><strong>Toolset</strong></td><td>A group of tools switched on or off together</td><td><code>web</code>, <code>file</code>, <code>terminal</code>, <code>coding</code></td></tr>
<tr><td><strong>Connection (MCP)</strong></td><td>An outside program that brings its own tools</td><td>a database, a company system, a third-party tool</td></tr>
</table>

<h2>What the agent can do out of the box</h2>
<p>A fresh install comes with a broad set of tools. Grouped by area:</p>
<table class="wiki-tabulka">
<tr><th>Area</th><th>Example tools</th><th>What for</th></tr>
<tr><td>Web</td><td><code>web_search</code>, <code>web_extract</code></td><td>Searching and reading pages</td></tr>
<tr><td>Terminal and files</td><td><code>terminal</code>, <code>read_file</code>, <code>patch</code>, <code>process</code></td><td>Working on the server and in files</td></tr>
<tr><td>Browser</td><td><code>browser_navigate</code>, <code>browser_snapshot</code>, <code>browser_exec</code></td><td>A real browser where clicking is needed</td></tr>
<tr><td>Media</td><td><code>vision_analyze</code>, <code>image_generate</code>, <code>text_to_speech</code></td><td>Looking at an image, making an image or speech</td></tr>
<tr><td>Planning and splitting work</td><td><code>todo</code>, <code>clarify</code>, <code>execute_code</code>, <code>delegate_task</code></td><td>Break down a task, ask a question, run a script, hand work to a subagent</td></tr>
<tr><td>Memory and history</td><td><code>memory</code>, <code>session_search</code></td><td>Durable notes and searching past conversations</td></tr>
<tr><td>Scheduled jobs</td><td><code>cronjob_manage</code></td><td>Jobs that run themselves on a schedule</td></tr>
</table>
<p class="note">Get the exact list any time: <code>hermes tools</code>.</p>

<h2>Switching toolsets on and off</h2>
<p>When you want the agent to do only what you need, narrow the toolsets. Fewer tools means less
room for mistakes and faster answers.</p>
<div class="code-block"><span class="p">❯</span> hermes chat --toolsets "web,terminal"      <span class="c"># only these two</span>
<span class="p">❯</span> hermes chat --toolsets all                 <span class="c"># everything available</span>
<span class="p">❯</span> hermes tools                               <span class="c"># overview and checkboxes</span></div>
<p>To make it permanent, edit the profile's <code>config.yaml</code> — either list the toolsets you
allow, or list the ones you forbid:</p>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
enabled_toolsets: [web, file, terminal]
disabled_toolsets: [browser]        <span class="c"># the browser is not needed at all</span></div>
<p class="note">Note: <code>web_search</code> is deliberately <em>not</em> part of the
<code>browser</code> toolset, so disabling the browser does not take web search away from you.</p>

<h2>When there are too many tools</h2>
<p>With two hundred tools switched on, the model gets lost — every tool description takes up space
that your request could use. Hermes solves this with <strong>tool search</strong>: only a handful of
the most used tools stay out, the rest is fetched the moment the agent needs them.</p>
<table class="wiki-tabulka">
<tr><th>When it happens</th><th>What happens</th></tr>
<tr><td>There are many tools (typically over 30)</td><td>Some tools move behind search; the agent asks for them by itself</td></tr>
<tr><td>Why it helps</td><td>Answers are faster and cheaper, the model stays focused</td></tr>
<tr><td>When it is wrong</td><td>When the agent does one narrow job over and over — then fewer toolsets with search off work better</td></tr>
</table>
<p class="note">In practice: when the agent reaches for a tool you did not expect, check whether it has
more toolsets enabled than you need. Configure it with <code>hermes tools</code> — no hand-editing files.</p>

<h2>Where tools run (terminal backends)</h2>
<p>As long as the agent runs commands on your server, we call it the "local" backend. It can also
run elsewhere — useful when you do not want to give it access to your own system, or when you need
an environment your server does not have.</p>
<table class="wiki-tabulka">
<tr><th>Backend</th><th>When it fits</th><th>How to set it</th></tr>
<tr><td><code>local</code> (default)</td><td>Your own server or VPS — simplest and fastest</td><td>nothing to configure</td></tr>
<tr><td>remote machine over SSH</td><td>Working on another machine you already have</td><td>credentials in the backend settings</td></tr>
<tr><td>container (Docker)</td><td>You want to separate what the agent may touch — it sees only the container</td><td><code>terminal.backend</code> in <code>config.yaml</code></td></tr>
<tr><td>cloud sandbox (Modal, Vercel Sandbox)</td><td>You have no server and want it to live only for the job</td><td><code>terminal.backend</code> plus credentials</td></tr>
</table>
<div class="code-block"><span class="p">❯</span> hermes config set terminal.backend modal
<span class="p">❯</span> hermes config set terminal.backend singularity</div>
<p class="note">A container is <strong>not</strong> a security guarantee by itself: it only protects
what the agent cannot reach into. Permissions and command approval are covered on the
<a href="/en/wiki/getting-started/security/">Security</a> page.</p>

<h2>Long jobs and administrator rights</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>How it works</th></tr>
<tr><td>A job runs long (backup, copying, watching a log)</td><td>The agent starts it <strong>in the background</strong> and can do other work; it can check the status any time</td></tr>
<tr><td>A command needs <code>sudo</code></td><td>An interactive session shows a masked password prompt (cached for that session). Passwords are never sent into a container or into chat</td></tr>
<tr><td>Passwordless sudo</td><td>Runs with no prompt — nothing to fill in</td></tr>
<tr><td>The job runs in a subagent</td><td>A password prompt cannot be opened there — run that command in the main conversation</td></tr>
</table>

<h2>Three pitfalls from our own running systems</h2>
<table class="wiki-tabulka">
<tr><th>What happened</th><th>How to spot it and what to do</th></tr>
<tr><td><strong>A tool reported success and nothing happened.</strong> The call went through, the output looked fine, the change was nowhere</td><td>Do not ask the tool whether it did the job — <em>verify the result somewhere else</em>: in the file, with a database query, with the page's HTTP code. Write the verification into your request</td></tr>
<tr><td><strong>A connected tool returned data from another project.</strong> The server answered correctly, but from the wrong database (we had two projects and one tool between them)</td><td>For outside tools, verify what they are connected to and ask about a specific row you know. When it does not match, fix the connection, not the agent</td></tr>
<tr><td><strong>Secrets showed up in the output as <code>***</code></strong></td><td>Hermes masks secrets in output. Never verify one by printing it — the print comes back empty or wrong even when the value is fine. Use it directly inside the command</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Enable only the toolsets you really use</td><td>Fewer tools mean faster, more accurate answers</td></tr>
<tr><td>Say how the work should be verified</td><td>"The page must return 200" or "show me the row from the database" — then nothing can just be claimed</td></tr>
<tr><td>When the agent can do everything but nothing well, narrow the scope</td><td>A narrow toolset with a clear request beats a pile of tools</td></tr>
<tr><td>Test a new connection on something you know</td><td>One simple query with an expected answer reveals a bad connection before you build on it</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/mcp-tools/"><strong>MCP tools</strong><span>Connecting outside programs and data</span></a>
<a href="/en/wiki/getting-started/security/"><strong>Security</strong><span>What to entrust to the agent and what not to</span></a>
<a href="/en/wiki/features/subagents/"><strong>Subagents</strong><span>When the work is more than one agent can hold</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/tools" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Tools and backends in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Tool vs. toolset
Tool = one ability (web_search, read_file, terminal, delegate_task).
Toolset = a bundle switched on/off as a whole (web, file, terminal, coding).
Overview: hermes tools

## What the agent can do out of the box
Web (web_search, web_extract) · Terminal and files (terminal, read_file, patch, process) ·
Browser (browser_navigate, browser_snapshot, browser_exec) · Media (vision_analyze,
image_generate, text_to_speech) · Planning (todo, clarify, execute_code, delegate_task) ·
Memory (memory, session_search) · Scheduled jobs (cronjob_manage)

## Switching toolsets on and off
hermes chat --toolsets "web,terminal"   |   hermes chat --toolsets all   |   hermes tools
Permanent in ~/.hermes/config.yaml: enabled_toolsets: [web, file, terminal] / disabled_toolsets: [browser]
web_search is NOT part of the browser toolset (disabling the browser keeps web search).

## When there are too many tools
Over roughly 30 tools, some move behind tool search and the agent fetches them on demand —
faster, cheaper answers. For one narrow repeated job, fewer toolsets with search off work better.

## Where tools run (terminal backends)
local (default, your own server) · remote over SSH · container (Docker) · cloud sandbox
(Modal, Vercel Sandbox). Setting: hermes config set terminal.backend <backend>
A container is not a security guarantee — see the Security page.

## Long jobs and sudo
Long command -> run in the background, the agent can do other work meanwhile.
sudo: an interactive session shows a masked password prompt (cached for the session);
passwords are never sent to chat or to a subagent; passwordless sudo runs without a prompt.

## Three pitfalls from our own running systems
1. A tool reported success but nothing happened -> verify elsewhere (file, DB, HTTP code).
2. A connected tool returned data from another project -> check what it is connected to, test with a known query.
3. Secrets printed as *** -> Hermes masks secrets; never verify a secret by printing it, use it inside the command.

## Tips
Enable only the toolsets you use · say how the work should be verified · narrow the scope instead of
adding tools · test a new connection with a query you know the answer to.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(13)
    stranka = najdi(13)
    assert stranka and stranka["nazev"] == "Nástroje a toolsety"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Nástroje a toolsety — co agent umí a jak mu to nastavit",
        "Jaké nástroje agent po instalaci má, jak se zapínají a vypínají sady nástrojů, kde příkazy běží, jak řešit sudo a dlouhé úlohy — a tři pasti z našeho provozu.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Nástroje a toolsety",
        "Agent umí jen to, na co má nástroj. Tady je, co dostane po instalaci, jak se sady zapínají a vypínají a na co si dát pozor.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Nástroje a toolsety — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Tools and toolsets — what the agent can do and how to configure it",
        "Which tools the agent has after installation, how toolsets are switched on and off, where commands run, how sudo and long jobs work — and three pitfalls from our systems.",
        OBRAZEK, "Wiki · Features in depth", "Tools and toolsets",
        "The agent can only do what it has a tool for. Here is what you get out of the box, how toolsets are switched on and off and what to watch out for.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Tools and toolsets — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
