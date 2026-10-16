#!/usr/bin/env python3
"""Postaví stránku wiki „Když se něco pokazí" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/reference-faq.md (sekce Troubleshooting),
guides-troubleshooting-agent-quality.md, user-guide-session-storage-recovery.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/reference/faq"
OBRAZEK = "wiki-oprava"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔧</span><div><strong>Nic se nerozbije navždy — a většina potíží má jednu z pěti příčin.</strong>
Agent si sám vede záznam o tom, co dělal, takže se dá nejdřív zjistit, co se stalo, a teprve pak
něco měnit. Vyřešeno bylo i to, co vypadalo beznadějně.</div></div>

<h2>První tři kroky (v tomto pořadí)</h2>
<ol class="kroky">
<li><strong>Zeptejte se agenta, co se stalo.</strong> V rozhovoru můžete napsat přímo:
<div class="code-block"><span class="p">❯</span> Podívej se do záznamu a zjisti, co se pokazilo při posledním kroku.
<span class="p">❯</span> Proč ten příkaz neproběhl? Co mu bránilo?</div>
Agent má přístup ke své historii a k výpisu běhů, takže často odpoví sám a hned to i opraví.</li>
<li><strong>Nechte si zkontrolovat instalaci.</strong> Příkaz <code>hermes doctor</code> projde nastavení
a řekne, co chybí nebo co je špatně:
<div class="code-block"><span class="p">$</span> hermes doctor</div></li>
<li><strong>Podívejte se do záznamu a do historie rozhovorů.</strong>
<div class="code-block"><span class="p">$</span> hermes logs              <span class="c"># co se naposledy dělo</span>
<span class="p">$</span> hermes sessions browse   <span class="c"># projít starší rozhovory</span></div></li>
</ol>

<h2>Pět nejčastějších příčin</h2>
<table class="wiki-tabulka">
<tr><th>Co se děje</th><th>Příčina</th><th>Řešení</th></tr>
<tr><td>Odpovědi přestaly chodit, hlásí chybu 429</td><td>Došel kredit nebo jste narazili na hodinový limit u poskytovatele modelu</td><td>Dobít kredit, chvíli počkat, nebo přepnout na levnější model (viz <a href="/wiki/zaciname/vyber-modelu/">výběr modelu</a>)</td></tr>
<tr><td>Agent hlásí, že je kontext příliš dlouhý</td><td>Rozhovor je delší, než model unese</td><td>Srovnat rozhovor příkazem <code>/compress</code>, nebo začít nový (<code>/new</code>)</td></tr>
<tr><td>Agent neodpovídá v Telegramu ani Discordu, ale v aplikaci ano</td><td>Neběží brána, která zprávy přeposílá</td><td>Zkontrolovat stav a bránu spustit znovu (viz <a href="/wiki/zaciname/telegram-a-discord/">Telegram a Discord</a>)</td></tr>
<tr><td>Model hlásí neplatný klíč</td><td>Klíč vypršel, byl smazán, nebo je u něj vyčerpaný kredit</td><td>Ověřit klíč u poskytovatele a vložit nový do nastavení agenta</td></tr>
<tr><td>Agent odmítá spustit příkaz</td><td>Příkaz je nebezpečný (nebo na seznamu zakázaných) a čeká na vaše potvrzení</td><td>Potvrdit, povolit natrvalo, nebo zvolit jiný postup (viz <a href="/wiki/zaciname/bezpecnost/">bezpečnost</a>)</td></tr>
</table>

<h2>Když agent odpovídá divně</h2>
<table class="wiki-tabulka">
<tr><th>Projev</th><th>Co s tím</th></tr>
<tr><td>Odpověď se uprostřed přerušila</td><td>Napište „pokračuj“ — agent naváže tam, kde skončil. Když se to opakuje, je to nejčastěji slabé spojení nebo malý model</td></tr>
<tr><td>Plete si souvislosti a vrací se k něčemu dávnému</td><td>Začněte nový rozhovor (<code>/new</code>). Dlouhý rozhovor se plní nepotřebnými detaily a agent se v nich ztrácí</td></tr>
<tr><td>Tvrdí něco, co si nemůže ověřit</td><td>Vyžádejte důkaz: „Ukaž mi soubor / výstup příkazu, ze kterého to víš.“ Když důkaz nedá, tvrzení neberte</td></tr>
<tr><td>Odpovídá zbytečně dlouze</td><td>Řekněte, jak to chcete: „odpovídej stručně, bez tabulek“ nebo „nejdřív mi to shrň do pěti vět“. Agent si to může uložit do <a href="/wiki/zaciname/pamet/">paměti</a></td></tr>
<tr><td>Odpovídá pomalu</td><td>Je to velký model nebo dlouhý rozhovor. Pomůže menší/rychlejší model nebo nový rozhovor</td></tr>
</table>

<h2>Co si můžete spravit sami</h2>
<table class="wiki-tabulka">
<tr><th>Příkaz</th><th>K čemu je</th></tr>
<tr><td><code>hermes doctor</code></td><td>Kontrola: instalace, nastavení, klíče, co chybí</td></tr>
<tr><td><code>hermes logs</code></td><td>Záznam o tom, co se dělo (vhodné přiložit, když se ptáte na pomoc)</td></tr>
<tr><td><code>hermes sessions browse</code></td><td>Projít starší rozhovory a dohledat, co se kdy dělalo</td></tr>
<tr><td><code>hermes pause</code> / <code>hermes resume</code></td><td>Zastavit a znovu pustit všechny pravidelné úlohy</td></tr>
<tr><td><code>hermes cron status</code></td><td>Zda plánovač běží — když ne, úlohy se nespustí</td></tr>
</table>

<h2>Kde hledat pomoc</h2>
<table class="wiki-tabulka">
<tr><th>Kde</th><th>Kdy se tam obrátit</th></tr>
<tr><td><a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener">Discord komunity</a></td><td>Nejrychlejší cesta — zeptejte se ostatních, kteří si tím prošli</td></tr>
<tr><td><a href="https://hermes-agent.nousresearch.com/docs" target="_blank" rel="noopener">Oficiální dokumentace</a></td><td>Potřebujete přesný popis nastavení nebo chybového hlášení (anglicky)</td></tr>
<tr><td>Oficiální repozitář (GitHub)</td><td>Skutečná chyba v programu — tam patří hlášení s popisem postupu</td></tr>
</table>
<p><strong>Než napíšete o pomoc, přiložte:</strong> co jste dělali, co jste čekali, co se stalo a kolik bylo
hodin. A když je to možné, i výpis z <code>hermes logs</code>. Bez toho se problém hledá naslepo a odpověď
bude znít „zkuste to znovu“.</p>

<h2>Prevence, která se vyplácí</h2>
<table class="wiki-tabulka">
<tr><th>Co</th><th>Proč</th></tr>
<tr><td>Zálohovat složku <code>~/.hermes/</code></td><td>Jsou tam rozhovory, paměť i skilly — tedy všechno, co se nedá dohledat znovu</td></tr>
<tr><td>Tajnosti držet v nastavení</td><td>Aby se nedostaly do textů, záloh ani do gitu (viz <a href="/wiki/zaciname/bezpecnost/">bezpečnost</a>)</td></tr>
<tr><td>Měnit věci po jednom</td><td>Když uděláte tři změny naráz a něco přestane fungovat, nepoznáte viníka</td></tr>
<tr><td>Sledovat spotřebu</td><td>Nejčastější důvod náhlého nefunkčního stavu je vyčerpaný kredit, ne chyba</td></tr>
<tr><td>Vědět, co je připojené</td><td>Napojení, skilly a plánované úlohy jsou tři místa, odkud přicházejí překvapení</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/caste-dotazy/"><strong>Časté dotazy</strong><span>Odpovědi na to, na co se ptá nejvíc lidí</span></a>
<a href="/wiki/zaciname/bezpecnost/"><strong>Bezpečnost</strong><span>Co agent smí a co musí odsouhlasit</span></a>
<a href="/wiki/zaciname/pravidelne-ulohy/"><strong>Pravidelné úlohy</strong><span>Když úloha nechodí, jak ji prověřit</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/reference/faq" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Řešení potíží do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## První tři kroky
1. zeptat se agenta, co se stalo ("podívej se do záznamu a zjisti, co se pokazilo")
2. hermes doctor   # kontrola instalace a nastavení
3. hermes logs / hermes sessions browse   # záznam a historie

## Pět nejčastějších příčin
- chyba 429 / odpovědi přestaly chodit -> došel kredit nebo hodinový limit u poskytovatele
- kontext příliš dlouhý -> /compress nebo /new
- neodpovídá v Telegramu/Discordu, v aplikaci ano -> neběží brána
- neplatný klíč k modelu -> vypršel / smazán / vyčerpaný kredit
- agent odmítá příkaz -> čeká na potvrzení (nebezpečný příkaz), viz bezpečnost

## Když odpovídá divně
- přerušená odpověď -> napsat "pokračuj"
- plete si souvislosti -> nový rozhovor (/new)
- nemůže ověřit tvrzení -> vyžádat důkaz (soubor/výstup)
- příliš dlouhé odpovědi -> říct, jak je chci (uloží se do paměti)
- pomalé -> menší model nebo nový rozhovor

## Příkazy
hermes doctor · hermes logs · hermes sessions browse · hermes pause|resume · hermes cron status

## Pomoc
Discord komunity · oficiální dokumentace · GitHub (skutečná chyba v programu)
Přiložit: co jsem dělal, co jsem čekal, co se stalo, kolik bylo hodin, výpis z hermes logs.

## Prevence
zálohovat ~/.hermes/ (rozhovory, paměť, skilly) · tajnosti v nastavení · měnit věci po jednom ·
sledovat spotřebu · vědět, co je připojené (MCP, skilly, úlohy)
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔧</span><div><strong>Nothing breaks forever — and most trouble has one of five causes.</strong>
The agent keeps a record of what it did, so the first move is finding out what actually happened, and only
then changing something. Even things that looked hopeless got solved.</div></div>

<h2>First three steps (in this order)</h2>
<ol class="kroky">
<li><strong>Ask the agent what happened.</strong> You can write it straight into the conversation:
<div class="code-block"><span class="p">❯</span> Look through the log and find out what went wrong in the last step.
<span class="p">❯</span> Why did that command not run? What stopped it?</div>
The agent can read its own history and run output, so it often answers by itself and fixes it on the spot.</li>
<li><strong>Have the installation checked.</strong> <code>hermes doctor</code> walks the setup and reports
what is missing or wrong:
<div class="code-block"><span class="p">$</span> hermes doctor</div></li>
<li><strong>Read the log and the conversation history.</strong>
<div class="code-block"><span class="p">$</span> hermes logs              <span class="c"># what happened last</span>
<span class="p">$</span> hermes sessions browse   <span class="c"># walk through past conversations</span></div></li>
</ol>

<h2>The five most common causes</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>Cause</th><th>Fix</th></tr>
<tr><td>Replies stop arriving, error 429</td><td>Credit ran out, or you hit the provider's hourly limit</td><td>Top up, wait a while, or switch to a cheaper model (see <a href="/en/wiki/getting-started/choosing-a-model/">choosing a model</a>)</td></tr>
<tr><td>The agent says the context is too long</td><td>The conversation is longer than the model can hold</td><td>Trim it with <code>/compress</code>, or start a new one (<code>/new</code>)</td></tr>
<tr><td>No reply on Telegram or Discord, but the app works</td><td>The gateway that relays messages is not running</td><td>Check its status and start it again (see <a href="/en/wiki/getting-started/telegram-and-discord/">Telegram and Discord</a>)</td></tr>
<tr><td>The model reports an invalid key</td><td>The key expired, was deleted, or its account is out of credit</td><td>Verify the key with the provider and enter a fresh one in the agent settings</td></tr>
<tr><td>The agent refuses to run a command</td><td>The command is dangerous (or on a deny list) and is waiting for your approval</td><td>Approve it, allow it permanently, or pick another approach (see <a href="/en/wiki/getting-started/security/">security</a>)</td></tr>
</table>

<h2>When the agent answers oddly</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>What to do</th></tr>
<tr><td>An answer was cut off mid-way</td><td>Write "continue" — the agent picks up where it stopped. If it keeps happening, it is usually a weak connection or a small model</td></tr>
<tr><td>It mixes up context and drags up something old</td><td>Start a new conversation (<code>/new</code>). A long chat fills with irrelevant detail and the agent loses the thread</td></tr>
<tr><td>It claims something it cannot verify</td><td>Demand evidence: "Show me the file or command output you got that from." If there is no evidence, do not trust the claim</td></tr>
<tr><td>Answers are needlessly long</td><td>Say how you want them: "be concise, no tables" or "sum it up in five sentences first". The agent can save that to <a href="/en/wiki/getting-started/memory/">memory</a></td></tr>
<tr><td>Answers are slow</td><td>It is a large model or a long conversation. A smaller/faster model or a fresh chat helps</td></tr>
</table>

<h2>What you can fix yourself</h2>
<table class="wiki-tabulka">
<tr><th>Command</th><th>What it is for</th></tr>
<tr><td><code>hermes doctor</code></td><td>Checks installation, settings, keys, what is missing</td></tr>
<tr><td><code>hermes logs</code></td><td>The record of what happened (good to attach when asking for help)</td></tr>
<tr><td><code>hermes sessions browse</code></td><td>Walk through past conversations and find what was done when</td></tr>
<tr><td><code>hermes pause</code> / <code>hermes resume</code></td><td>Stop and restart all scheduled jobs</td></tr>
<tr><td><code>hermes cron status</code></td><td>Whether the scheduler is alive — if not, jobs will not fire</td></tr>
</table>

<h2>Where to get help</h2>
<table class="wiki-tabulka">
<tr><th>Where</th><th>When to go there</th></tr>
<tr><td><a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener">Community Discord</a></td><td>The fastest route — ask others who have been through it</td></tr>
<tr><td><a href="https://hermes-agent.nousresearch.com/docs" target="_blank" rel="noopener">Official documentation</a></td><td>You need the exact wording of a setting or an error message</td></tr>
<tr><td>The official repository (GitHub)</td><td>A genuine bug in the software — that is where a report with steps belongs</td></tr>
</table>
<p><strong>Before you ask for help, include:</strong> what you were doing, what you expected, what happened, and
the time. Where possible also the output of <code>hermes logs</code>. Without that the problem is hunted
blindly and the answer will be "try again".</p>

<h2>Prevention that pays off</h2>
<table class="wiki-tabulka">
<tr><th>What</th><th>Why</th></tr>
<tr><td>Back up the <code>~/.hermes/</code> folder</td><td>Conversations, memory and skills live there — everything that cannot be found again</td></tr>
<tr><td>Keep secrets in the settings</td><td>So they never reach texts, backups or git (see <a href="/en/wiki/getting-started/security/">security</a>)</td></tr>
<tr><td>Change one thing at a time</td><td>Make three changes at once and something breaks, you cannot tell which one did it</td></tr>
<tr><td>Watch your usage</td><td>The most common reason for a sudden dead end is exhausted credit, not a bug</td></tr>
<tr><td>Know what is connected</td><td>Connections, skills and scheduled jobs are the three places surprises come from</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/faq/"><strong>Frequently asked questions</strong><span>Answers to what people ask most</span></a>
<a href="/en/wiki/getting-started/security/"><strong>Security</strong><span>What the agent may do and what it must ask for</span></a>
<a href="/en/wiki/getting-started/scheduled-tasks/"><strong>Scheduled tasks</strong><span>When a job does not fire, how to check it</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/reference/faq" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Troubleshooting in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## First three steps
1. ask the agent what happened ("look through the log and find out what went wrong")
2. hermes doctor   # checks installation and settings
3. hermes logs / hermes sessions browse   # log and history

## Five most common causes
- error 429 / replies stopped -> credit exhausted or provider hourly limit
- context too long -> /compress or /new
- no reply on Telegram/Discord but the app works -> the gateway is not running
- invalid model key -> expired / deleted / out of credit
- agent refuses a command -> waiting for approval (dangerous command), see security

## When answers are odd
- answer cut off -> write "continue"
- mixes up context -> new conversation (/new)
- claims it cannot verify -> demand evidence (file or command output)
- needlessly long answers -> say how you want them (saved to memory)
- slow -> smaller model or a fresh chat

## Commands
hermes doctor · hermes logs · hermes sessions browse · hermes pause|resume · hermes cron status

## Help
Community Discord · official documentation · GitHub (a real bug in the software)
Include: what you were doing, what you expected, what happened, the time, the hermes logs output.

## Prevention
back up ~/.hermes/ (conversations, memory, skills) · secrets in the settings · one change at a time ·
watch usage · know what is connected (MCP, skills, jobs)
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(10)
    stranka = najdi(10)
    assert stranka and stranka["nazev"] == "Když se něco pokazí"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Když se něco pokazí — jak to najít a spravit",
        "První tři kroky při potížích, pět nejčastějších příčin a co přiložit, když píšete o pomoc. Většina problémů se tím vyřeší.",
        OBRAZEK, "Wiki · Začínáme", "Když se něco pokazí",
        "Většina potíží má jednu z pěti příčin — a agent si sám vede záznam, takže se dá zjistit, co se stalo.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Když se něco pokazí — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "When something breaks — how to find and fix it",
        "The first three steps when things go wrong, the five most common causes and what to include when asking for help.",
        OBRAZEK, "Wiki · Start here", "When something breaks",
        "Most trouble has one of five causes — and the agent keeps its own record, so you can find out what happened.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "When something breaks — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
