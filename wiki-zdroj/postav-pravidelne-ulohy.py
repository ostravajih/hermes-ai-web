#!/usr/bin/env python3
"""Postaví stránku wiki „Pravidelné úlohy (cron)" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-cron.md, guides-automate-with-cron.md,
guides-cron-troubleshooting.md, reference-automation-blueprints-catalog.mdx.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/cron"
OBRAZEK = "wiki-cron"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⏰</span><div><strong>Co se dělá pořád dokola, ať se dělá samo.</strong>
Ráno vám přijde přehled, v noci proběhne kontrola, každou hodinu se ohlídá web. Výsledek chodí tam,
kde si s agentem píšete — nejčastěji do Telegramu nebo Discordu. <strong>Nic se nespustí potichu:</strong>
než úloha vznikne, vždycky ji potvrdíte.</div></div>

<h2>Co se dá naplánovat</h2>
<table class="wiki-tabulka">
<tr><th>Úloha</th><th>Jak často</th><th>Co vám přinese</th></tr>
<tr><td>Ranní přehled</td><td>každý den v 7:30</td><td>Krátká zpráva: co se stalo v oboru, co hoří, co dnes čeká</td></tr>
<tr><td>Kontrola webu</td><td>každou hodinu</td><td>Ozve se jen když stránka neodpovídá — jinak mlčí</td></tr>
<tr><td>Sběr novinek</td><td>každé 2 hodiny</td><td>Nové články z odběrů, o které se zajímáte</td></tr>
<tr><td>Kontrola po nasazení</td><td>jednou</td><td>Ověří, že se změna opravdu projevila naživo</td></tr>
<tr><td>Měsíční souhrn</td><td>1. den v měsíci</td><td>Co se za měsíc udělalo, kolik to stálo, co dál</td></tr>
<tr><td>Noční úklid</td><td>každou noc ve 3:00</td><td>Protřídit frontu úkolů nebo připravit podklady na ráno</td></tr>
</table>

<h2>Jak úlohu zadat — tři způsoby</h2>
<ol class="kroky">
<li><strong>Řekněte to v rozhovoru.</strong> Nejjednodušší cesta, zvládne to i člověk, který nikdy neslyšel
o plánování úloh:
<div class="code-block"><span class="p">❯</span> Každý všední den v osm ráno mi pošli přehled novinek o umělé inteligenci.
<span class="p">❯</span> Každou hodinu zkontroluj, že náš web odpovídá, a napiš mi jen když bude problém.</div>
Agent se doptá na detaily a úlohu založí.</li>
<li><strong>Zápisem s časem.</strong> Když víte, co chcete, je to jeden řádek:
<div class="code-block"><span class="c"># v rozhovoru</span>
<span class="p">$</span> /cron add "every 2h" "Zkontroluj stav serveru a napiš mi, jen když je něco špatně."
<span class="c"># z příkazové řádky</span>
<span class="p">$</span> hermes cron create "every 1d at 09:00" "Pošli mi dnešní plán a tři priority."</div></li>
<li><strong>Hotovým vzorem.</strong> Pro časté úlohy existují připravené vzory — jen doplníte pár údajů
a nemusíte znát žádný zápis času:
<div class="code-block"><span class="p">$</span> /blueprint morning-brief</div>
Na výběr jsou vzory jako ranní přehled, hlídání dostupnosti, sběr novinek, kontrola nasazení,
bezpečnostní kontrola závislostí nebo noční třídění úkolů.</li>
</ol>

<h2>Jak se píše čas</h2>
<table class="wiki-tabulka">
<tr><th>Zápis</th><th>Znamená</th></tr>
<tr><td><code>every 5m</code> / <code>every 2h</code></td><td>každých 5 minut / každé 2 hodiny</td></tr>
<tr><td><code>every 1d at 09:00</code></td><td>jednou denně v 9:00</td></tr>
<tr><td><code>every 1d at 07:30</code></td><td>jednou denně v půl osmé ráno</td></tr>
<tr><td>slovy: „každý všední den v osm“</td><td>funguje taky — agent to převede sám</td></tr>
</table>
<p class="note">Časy se počítají v časovém pásmu serveru. Když je server nastavený na český čas (což je u nás obvyklé),
sedí i to, co si představujete pod pojmem „ráno“.</p>

<h2>Kam přijde výsledek</h2>
<p>Tam, kde si s agentem píšete — Telegram, Discord, nebo jiná připojená platforma. Když úloha nemá kam
doručit, běh sice proběhne, ale výsledek se ztratí; stav se to hlásí jako <em>nepodařilo se doručit</em>,
takže na to přijdete v přehledu úloh.</p>
<p><strong>Úloha umí i mlčet.</strong> Když se agent rozhodne, že nemá co říct (vše v pořádku), odpoví místo zprávy
značkou <code>[SILENT]</code> a nic se neodešle. Proto se hodí zadání typu „napiš mi jen když je problém“.</p>

<h2>Co musí platit, aby to fungovalo</h2>
<table class="wiki-tabulka">
<tr><th>Podmínka</th><th>Proč a co s tím</th></tr>
<tr><td><strong>Musí běžet brána</strong> (gateway)</td><td>Plánovač je její součástí a každou minutu se ptá, co je na řadě. Když brána neběží, úlohy se nespustí — zkontrolujte <code>hermes cron status</code></td></tr>
<tr><td><strong>Zadání musí být úplné samo o sobě</strong></td><td>Každý běh začíná s čistou hlavou: úloha nevidí vaše rozhovory ani předchozí běhy. Nemůže se tedy odvolávat na „to, co jsme včera probírali“ — napište do zadání všechno potřebné</td></tr>
<tr><td>Musí být kredit u modelu</td><td>Úloha spotřebovává model stejně jako běžný rozhovor (viz <a href="/wiki/zaciname/vyber-modelu/">výběr modelu</a>)</td></tr>
<tr><td>Server musí být vzhůru</td><td>Když je stroj vypnutý, běh se neodehraje. Agent zmeškané běhy pozná a umí je dohnat, ale zmeškaný čas nikdo nevrátí</td></tr>
</table>

<h2>Užitečné příkazy</h2>
<table class="wiki-tabulka">
<tr><th>Příkaz</th><th>Co udělá</th></tr>
<tr><td><code>hermes cron list</code></td><td>Vypíše všechny úlohy i s tím, jak naposledy dopadly</td></tr>
<tr><td><code>hermes cron status</code></td><td>Řekne, jestli plánovač běží a kdy je nejbližší úloha</td></tr>
<tr><td><code>hermes cron doctor</code></td><td>Projde úlohy a najde problémy (nedoručené výsledky, chyby za sebou)</td></tr>
<tr><td><code>hermes pause</code> a <code>hermes resume</code></td><td>Nouzové zastavení <em>všech</em> úloh a opětovné spuštění</td></tr>
    <tr><td><code>hermes cron pause „Název úlohy“</code></td><td>Úlohy jdou adresovat i <strong>jménem</strong>, ne jen ID — jméno se porovnává bez ohledu na velikost písmen. Když ho má víc úloh, Hermes to odmítne a vypíše kandidáty s ID, aby se omylem nezměnila jiná</td></tr>
<tr><td><code>hermes cron tick</code></td><td>Projede plánovačem jeden cyklus a skončí — pro ladění. <strong>Brána ale musí běžet</strong>: tick ji sám nespustí, a když neběží, úlohy s agentem se jen přeskočí (a doženou se při dalším cyklu)</td></tr>
<tr><td><code>/cron</code> v rozhovoru</td><td>Přehled a správa úloh bez opouštění chatu</td></tr>
</table>

<h2>Naše tipy z provozu</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Dejte úlohám levný model</td><td>Běží často a bez dozoru, takže se spotřeba nasčítá. Nastavením <code>cron.model</code> jim určíte levnější model, než používáte vy v rozhovoru</td></tr>
<tr><td>Pište zadání konkrétně</td><td>Co zjistit, odkud, komu poslat a jak dlouhé to má být. „Udělej přehled“ dopadne pokaždé jinak</td></tr>
<tr><td>Krátká zpráva, dlouhé věci jako soubor</td><td>Do mobilu se hodí pár vět; tabulku si nechte přiložit jako soubor</td></tr>
<tr><td>Nechte úlohu mlčet, když je vše dobré</td><td>Upozornění, které chodí pořád, přestanete číst — a to je horší než žádné</td></tr>
<tr><td>Občas se podívejte, jak si vede</td><td><code>hermes cron list</code> ukáže, jestli úloha opravdu běží a co posílá</td></tr>
<tr><td>Nic nevratného bez dozoru</td><td>Úloha běží, když u toho nejste. Mazání, platby nebo odesílání zpráv lidem patří do ručního potvrzení</td></tr>
</table>

<h2>Když to nefunguje</h2>
<table class="wiki-tabulka">
<tr><th>Co se děje</th><th>Příčina a co s tím</th></tr>
<tr><td>Nic nepřišlo</td><td>Nejdřív <code>hermes cron status</code> — běží plánovač? Pak <code>hermes cron list</code>, jestli úloha není pozastavená a jak dopadl poslední běh</td></tr>
<tr><td>Běh proběhl, ale zpráva nedošla</td><td>Úloha nemá kam doručit (nepřipojená platforma) nebo se zprávu nepodařilo odeslat. Přehled to hlásí jako nedoručeno</td></tr>
<tr><td>Chodí to mockrát nebo ve špatnou dobu</td><td>Zkontrolujte zápis času a časové pásmo serveru</td></tr>
<tr><td>Úloha si plete souvislosti</td><td>Zadání se odvolává na rozhovor nebo na předchozí běh, které úloha nevidí. Doplňte do zadání všechny údaje</td></tr>
<tr><td>Chci, aby přestaly chodit</td><td>Jednu úlohu pozastavíte nebo smažete v <code>/cron</code>; všechny naráz zastaví <code>hermes pause</code></td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/telegram-a-discord/"><strong>Telegram a Discord</strong><span>Bez toho nemá úloha kam doručit</span></a>
<a href="/wiki/zaciname/pamet/"><strong>Paměť agenta</strong><span>Co si agent odnese do dalšího běhu</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/cron" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Plánování úloh do detailu (anglicky)</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Discord komunity</strong><span>Co si kdo naplánoval</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co se dá naplánovat
ranní přehled · kontrola webu každou hodinu · sběr novinek · kontrola po nasazení · měsíční souhrn · noční úklid

## Jak úlohu zadat
1. v rozhovoru: "Každý všední den v osm mi pošli přehled novinek o AI."
2. zápisem: /cron add "every 2h" "Zkontroluj stav serveru a napiš mi, jen když je něco špatně."
   hermes cron create "every 1d at 09:00" "Pošli mi dnešní plán a tři priority."
3. hotovým vzorem: /blueprint morning-brief  (ranní přehled, hlídání dostupnosti, sběr novinek,
   kontrola nasazení, bezpečnostní kontrola závislostí, noční třídění úkolů)
Nic se nespustí potichu - úlohu vždy potvrdíte.

## Zápis času
every 5m / every 2h / every 1d at 09:00 / slovy "každý všední den v osm"
Časy platí v časovém pásmu serveru.

## Doručení výsledku
Tam, kde si s agentem píšete (Telegram, Discord...). Když není kam doručit, běh proběhne,
ale výsledek se ztratí (stav "nedoručeno").
Agent umí odpovědět [SILENT] = zpráva se neodešle (hodí se pro "napiš mi jen když je problém").

## Podmínky
- musí běžet brána (gateway) - plánovač je její součást, kontroluje každou minutu; hermes cron status
- zadání musí být úplné samo o sobě: každý běh začíná s čistou hlavou (nevidí rozhovory ani předchozí běhy)
- musí být kredit u modelu
- server musí být vzhůru (zmeškané běhy agent pozná, čas se ale nevrátí)

## Příkazy
hermes cron list      # úlohy a jak naposledy dopadly
hermes cron status    # běží plánovač? kdy je nejbližší úloha
hermes cron doctor    # kontrola problémů (nedoručené výsledky, chyby)
hermes pause / resume # nouzové zastavení a obnovení všech úloh
/cron                 # správa úloh v rozhovoru

## Tipy
- úlohám dejte levný model (cron.model) - běží často a bez dozoru
- zadání konkrétně: co zjistit, odkud, komu, jak dlouhé
- krátká zpráva do mobilu, dlouhé výstupy jako soubor
- nechte úlohu mlčet, když je vše dobré (jinak upozornění přestanete číst)
- občas zkontrolujte hermes cron list
- nic nevratného bez dozoru (mazání, platby, zprávy lidem)

## Když nefunguje
- nic nepřišlo -> hermes cron status (běží plánovač?), hermes cron list (není pozastavená?)
- běh proběhl, zpráva nedošla -> není kam doručit / nepodařilo se odeslat
- chodí mockrát nebo ve špatnou dobu -> zápis času a časové pásmo serveru
- plete si souvislosti -> zadání se odvolává na rozhovor, který úloha nevidí
- chci zastavit -> /cron (jedna úloha) nebo hermes pause (všechny)
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⏰</span><div><strong>Anything done over and over should do itself.</strong>
A summary arrives in the morning, a check runs at night, a website is watched every hour. The result lands where
you chat with the agent — usually Telegram or Discord. <strong>Nothing is scheduled silently:</strong>
you always confirm a job before it is created.</div></div>

<h2>What you can schedule</h2>
<table class="wiki-tabulka">
<tr><th>Job</th><th>How often</th><th>What it gives you</th></tr>
<tr><td>Morning brief</td><td>daily at 7:30</td><td>A short message: what happened in your field, what is urgent, what today holds</td></tr>
<tr><td>Website check</td><td>every hour</td><td>Speaks up only when the site stops answering — silent otherwise</td></tr>
<tr><td>News collection</td><td>every 2 hours</td><td>New articles from the feeds you care about</td></tr>
<tr><td>Post-deploy check</td><td>once</td><td>Verifies the change really went live</td></tr>
<tr><td>Monthly summary</td><td>1st of the month</td><td>What was done, what it cost, what is next</td></tr>
<tr><td>Nightly tidy-up</td><td>every night at 3:00</td><td>Triage the task queue or prepare material for the morning</td></tr>
</table>

<h2>Three ways to create a job</h2>
<ol class="kroky">
<li><strong>Say it in the conversation.</strong> The easiest route — it works even if you have never heard
of scheduled jobs:
<div class="code-block"><span class="p">❯</span> Every weekday at eight in the morning send me a summary of AI news.
<span class="p">❯</span> Every hour check that our website responds, and only write to me if there is a problem.</div>
The agent asks for the details and creates the job.</li>
<li><strong>With an explicit schedule.</strong> One line when you know what you want:
<div class="code-block"><span class="c"># inside a chat</span>
<span class="p">$</span> /cron add "every 2h" "Check the server and write to me only if something is wrong."
<span class="c"># from the command line</span>
<span class="p">$</span> hermes cron create "every 1d at 09:00" "Send me today's plan and three priorities."</div></li>
<li><strong>From a ready-made blueprint.</strong> Common tasks have templates — fill in a few fields and
you never touch a schedule format:
<div class="code-block"><span class="p">$</span> /blueprint morning-brief</div>
Available blueprints include a morning brief, uptime monitoring, news collection, deploy verification,
dependency security audits and nightly backlog triage.</li>
</ol>

<h2>How schedules are written</h2>
<table class="wiki-tabulka">
<tr><th>Notation</th><th>Meaning</th></tr>
<tr><td><code>every 5m</code> / <code>every 2h</code></td><td>every 5 minutes / every 2 hours</td></tr>
<tr><td><code>every 1d at 09:00</code></td><td>once a day at 9:00</td></tr>
<tr><td><code>every 1d at 07:30</code></td><td>once a day at half past seven</td></tr>
<tr><td>in words: "every weekday at eight"</td><td>works too — the agent translates it</td></tr>
</table>
<p class="note">Times are evaluated in the server's time zone. If the server runs on your local time (the usual
setup), "morning" means exactly what you expect.</p>

<h2>Where the result goes</h2>
<p>To wherever you chat with the agent — Telegram, Discord or another connected platform. If a job has nowhere
to deliver, it still runs but the output is lost; the job reports that as a <em>delivery failure</em>,
so you can spot it in the job list.</p>
<p><strong>A job can also stay silent.</strong> When the agent decides there is nothing to report (all is well),
it answers with <code>[SILENT]</code> instead of a message and nothing is sent. That is why prompts like
"write to me only if there is a problem" work so well.</p>

<h2>What must hold for it to work</h2>
<table class="wiki-tabulka">
<tr><th>Condition</th><th>Why, and what to do</th></tr>
<tr><td><strong>The gateway must be running</strong></td><td>The scheduler is part of it and checks every minute what is due. With the gateway down, jobs do not fire — check <code>hermes cron status</code></td></tr>
<tr><td><strong>The prompt must be self-contained</strong></td><td>Every run starts with a clean head: the job sees neither your conversations nor previous runs. It cannot refer to "what we discussed yesterday" — put everything it needs into the prompt</td></tr>
<tr><td>There must be model credit</td><td>A job consumes the model just like a normal conversation (see <a href="/en/wiki/getting-started/choosing-a-model/">choosing a model</a>)</td></tr>
<tr><td>The server must be awake</td><td>With the machine off, nothing runs. The agent notices missed runs and can catch up, but the missed time is gone</td></tr>
</table>

<h2>Useful commands</h2>
<table class="wiki-tabulka">
<tr><th>Command</th><th>What it does</th></tr>
<tr><td><code>hermes cron list</code></td><td>Lists every job with how its last run went</td></tr>
<tr><td><code>hermes cron status</code></td><td>Tells you whether the scheduler is alive and when the next run is</td></tr>
<tr><td><code>hermes cron doctor</code></td><td>Checks the jobs and reports problems (undelivered output, repeated failures)</td></tr>
<tr><td><code>hermes pause</code> and <code>hermes resume</code></td><td>Emergency stop for <em>all</em> jobs, and starting them again</td></tr>
    <tr><td><code>hermes cron pause "Job name"</code></td><td>Jobs can be addressed by <strong>name</strong>, not just by ID — matching is case-insensitive. When several jobs share a name Hermes refuses and lists the candidates with their IDs, so the wrong job is never mutated by accident</td></tr>
<tr><td><code>hermes cron tick</code></td><td>Runs one scheduler pass and exits — for debugging. <strong>The gateway must be running</strong>: a tick never starts one, and with no gateway agent jobs are skipped (they fire on the next tick after <code>hermes gateway start</code>)</td></tr>
<tr><td><code>/cron</code> inside a chat</td><td>Review and manage jobs without leaving the conversation</td></tr>
</table>

<h2>Tips from experience</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Give jobs a cheap model</td><td>They run often and unattended, so the cost adds up. Set <code>cron.model</code> to send them to a cheaper model than the one you chat with</td></tr>
<tr><td>Write specific prompts</td><td>What to check, from where, who it goes to, how long it should be. "Make a summary" turns out differently every time</td></tr>
<tr><td>Short message, long output as a file</td><td>A few sentences suit a phone; have a table attached as a file instead</td></tr>
<tr><td>Let the job stay silent when all is well</td><td>Alerts that always arrive stop being read — which is worse than none</td></tr>
<tr><td>Check on it occasionally</td><td><code>hermes cron list</code> shows whether the job really runs and what it sends</td></tr>
<tr><td>Nothing irreversible unattended</td><td>A job runs while you are away. Deletions, payments or messaging people belong behind manual approval</td></tr>
</table>

<h2>When it does not work</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>Cause and what to do</th></tr>
<tr><td>Nothing arrived</td><td>Start with <code>hermes cron status</code> — is the scheduler alive? Then <code>hermes cron list</code> to see whether the job is paused and how the last run went</td></tr>
<tr><td>The run happened but no message came</td><td>The job has nowhere to deliver (platform not connected) or the send failed. The list reports it as a delivery failure</td></tr>
<tr><td>It fires too often or at the wrong time</td><td>Check the schedule notation and the server's time zone</td></tr>
<tr><td>The job mixes up context</td><td>The prompt refers to a conversation or a previous run that the job cannot see. Add every needed detail to the prompt</td></tr>
<tr><td>I want it to stop</td><td>Pause or delete one job in <code>/cron</code>; <code>hermes pause</code> stops all of them at once</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/telegram-and-discord/"><strong>Telegram and Discord</strong><span>Without them a job has nowhere to deliver</span></a>
<a href="/en/wiki/getting-started/memory/"><strong>Agent memory</strong><span>What the agent carries into the next run</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/cron" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Scheduled tasks in detail</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Community Discord</strong><span>See what others schedule</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What you can schedule
morning brief · hourly website check · news collection · post-deploy check · monthly summary · nightly tidy-up

## Three ways to create a job
1. in conversation: "Every weekday at eight send me a summary of AI news."
2. explicit schedule: /cron add "every 2h" "Check the server and write only if something is wrong."
   hermes cron create "every 1d at 09:00" "Send me today's plan and three priorities."
3. ready-made blueprint: /blueprint morning-brief  (morning brief, uptime monitor, news collection,
   deploy verification, dependency security audit, nightly backlog triage)
Nothing is scheduled silently - you always confirm the job.

## Schedule notation
every 5m / every 2h / every 1d at 09:00 / in words "every weekday at eight"
Times use the server's time zone.

## Where the result goes
Wherever you chat with the agent (Telegram, Discord...). With nowhere to deliver, the job runs but the
output is lost (reported as a delivery failure).
The agent can answer [SILENT] = nothing is sent (great for "only tell me if there is a problem").

## Conditions
- the gateway must be running (the scheduler is part of it, ticking every minute); hermes cron status
- the prompt must be self-contained: each run starts with a clean head (no access to conversations or
  previous runs)
- model credit is required
- the server must be awake (missed runs are noticed, but the time is gone)

## Commands
hermes cron list      # jobs and how the last run went
hermes cron status    # is the scheduler alive, when is the next run
hermes cron doctor    # checks for problems (undelivered output, repeated failures)
hermes pause / resume # emergency stop and restart of all jobs
/cron                 # manage jobs inside a chat

## Tips
- give jobs a cheap model (cron.model) - they run often and unattended
- specific prompts: what, from where, to whom, how long
- short message to a phone, long output as a file
- let a job stay silent when all is well (otherwise you stop reading alerts)
- check hermes cron list occasionally
- nothing irreversible unattended (deletions, payments, messaging people)

## Troubleshooting
- nothing arrived -> hermes cron status (scheduler alive?), hermes cron list (job paused?)
- run happened, message did not -> nowhere to deliver / send failed
- fires too often or at the wrong time -> schedule notation and server time zone
- mixes up context -> the prompt refers to a conversation the job cannot see
- stop it -> /cron (one job) or hermes pause (all jobs)
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(7)
    stranka = najdi(7)
    assert stranka and stranka["nazev"].startswith("Pravidelné úlohy")

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Pravidelné úlohy (cron) — úkoly, které běží samy",
        "Jak naplánovat úlohy, které běží bez vás: tři způsoby zadání, zápis času, kam chodí výsledek, co musí platit (běžící brána, úplné zadání) a jak to zastavit.",
        OBRAZEK, "Wiki · Začínáme", "Pravidelné úlohy (cron)",
        "Ráno přehled, v noci kontrola, každou hodinu dohled — a výsledek vám přijde tam, kde si s agentem píšete.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Pravidelné úlohy (cron) — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Scheduled tasks (cron) — jobs that run themselves",
        "How to schedule jobs that run without you: three ways to create them, where the result goes and what must hold.",
        OBRAZEK, "Wiki · Start here", "Scheduled tasks (cron)",
        "A morning brief, a nightly check, hourly monitoring — delivered where you chat with the agent.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Scheduled tasks (cron) — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
