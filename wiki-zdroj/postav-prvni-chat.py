#!/usr/bin/env python3
"""Postaví stránku wiki „První chat s agentem" (česky + anglicky) včetně verze pro AI."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/reference/slash-commands"
OBRAZEK = "wiki-chat"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">💬</span><div><strong>Agent není vyhledávač ani klávesa na odpovědi.</strong>
Dávejte mu úkoly, které se dají ověřit — a on je sám provede: spustí příkazy, přečte soubory, něco zapíše.
Než začnete, mějte hotový <a href="/wiki/zaciname/vyber-modelu/">vybraný model</a>.</div></div>

<h2>Jak to vypadá</h2>
<p>Napište <code>hermes</code> a otevře se rozhovor v terminálu. Vy píšete běžnou češtinou, agent pracuje:</p>
<div class="code-block"><span class="c"># spuštění</span>
<span class="p">$</span> hermes
<span class="c"># a první úkol — ověřitelný, s jasným výsledkem</span>
<span class="p">❯</span> Zjisti, kolik místa zabírá disk, a vypiš to jako tabulku.</div>
<p>V rozhovoru pak uvidíte, co agent dělá: každý spuštěný nástroj má na začátku řádku <code>●</code> a na konci
<code>✓</code> (nebo <code>✗</code>, když selhal). Během psaní bliká ukazatel — agent právě přemýšlí.</p>

<h2>Jak zadávat úkoly, aby se daly ověřit</h2>
<table class="wiki-tabulka">
<tr><th>Místo</th><th>Napište</th><th>Proč</th></tr>
<tr><td>„Nastav server.“</td><td>„Zjisti verzi systému a napiš ji do souboru <code>verze.txt</code>.“</td><td>Výsledek si přečtete a hned víte, jestli to udělal správně</td></tr>
<tr><td>„Udělej pořádek v datech.“</td><td>„Vypiš deset největších souborů ve složce /var/log a nic nemaž.“</td><td>Malý krok, který se dá zkontrolovat, a jasně řečeno, co nesmí</td></tr>
<tr><td>„Oprav to.“</td><td>„Najdi příčinu chyby v logu, napiš mi ji a navrhni dvě možnosti opravy — zatím nic neopravuj.“</td><td>Nejdřív zjištění, pak akce. Agent se tak nerozjede špatným směrem</td></tr>
<tr><td>„Zkontroluj web.“</td><td>„Ověř, že stránka vrací 200 a že se v hlavičce posílá kódování utf-8; ukaž mi přesný příkaz, kterým jsi to zjistil.“</td><td>Chcete důkaz, ne dojem</td></tr>
</table>
<p class="note"><strong>Zlaté pravidlo:</strong> čím lépe si dokážete výsledek ověřit vy, tím lépe se s agentem pracuje.
Když nepoznáte, že je úkol hotový, nepozná to ani on.</p>

<h2>Užitečné lomítkové příkazy</h2>
<p>Do rozhovoru se píšou příkazy začínající lomítkem — ovládají agenta, ne jeho práci:</p>
<table class="wiki-tabulka">
<tr><th>Příkaz</th><th>Co udělá</th></tr>
<tr><td><code>/help</code></td><td>Vypíše, co všechno v rozhovoru jde</td></tr>
<tr><td><code>/new</code></td><td>Začne novou konverzaci (stará zůstává uložená)</td></tr>
<tr><td><code>/model</code></td><td>Změní model uprostřed práce (drahý jen na těžký úkol)</td></tr>
<tr><td><code>/context</code></td><td>Ukáže, jak je zaplněná paměť rozhovoru</td></tr>
<tr><td><code>/compress</code></td><td>Srovná paměť rozhovoru, když je plná</td></tr>
<tr><td><code>/undo</code> a <code>/retry</code></td><td>Vezme zpět poslední výměnu / zopakuje poslední dotaz</td></tr>
<tr><td><code>/stop</code></td><td>Zastaví všechny běžící úlohy na pozadí</td></tr>
<tr><td><code>/queue</code> (nebo <code>/q</code>)</td><td>Zařadí další úkol, až agent dokončí ten současný</td></tr>
<tr><td><code>/bg</code></td><td>Pustí úkol na pozadí, ať můžete pracovat dál</td></tr>
<tr><td><code>/status</code></td><td>Ukáže model, profil, složku a identifikátor konverzace</td></tr>
</table>
<p>Kompletní seznam má oficiální dokumentace (přes 160 příkazů) — odkaz je dole.</p>

<h2>Schvalování: agent se vás na důležité věci zeptá</h2>
<p>Než agent spustí něco, co může něco změnit nebo smazat, zobrazí se mu <strong>panel s žádostí o schválení</strong>
(<code>⚠ approval required</code>) a uvidíte přesný příkaz. Můžete potvrdit, nebo odmítnout a napsat, co místo toho.
Režim, kdy se agent neptá (<em>YOLO</em>), existuje, ale na serveru s daty ho nedoporučujeme — nikdo pak nedrží
ruku nad tím, co se spouští.</p>

<h2>Pokračování v práci</h2>
<div class="code-block"><span class="c"># pokračovat v posledním rozhovoru</span>
<span class="p">$</span> hermes --continue
<span class="c"># vypsat uložené konverzace a vybrat si</span>
<span class="p">$</span> hermes sessions
<span class="c"># jeden dotaz bez otevírání rozhovoru (hodí se do skriptů)</span>
<span class="p">$</span> hermes chat -q "kolik je volného místa na disku?"</div>

<h2>Naše tipy z praxe</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Pište česky, jak jste zvyklí</td><td>Agent češtině rozumí. Když má odpovídat česky i v delších výstupech, řekněte mu to na začátku</td></tr>
<tr><td>Nechte ho nejdřív zjistit stav</td><td>„Podívej se…“ místo „Udělej…“. Ušetříte opravy po unáhleném zásahu</td></tr>
<tr><td>Žádejte důkaz</td><td>„Ukaž mi příkaz, kterým jsi to zjistil.“ Ověříte výsledek i to, že si ho nevymyslel</td></tr>
<tr><td>Když se to zvrtne, použijte <code>/stop</code></td><td>Zastaví běžící úlohy. Změny v souborech jde vrátit přes <code>/rollback</code></td></tr>
<tr><td>Nedávejte jeden obří úkol</td><td>Rozdělte ho na kroky, které po sobě zkontrolujete. Menší kroky = méně slepých cest</td></tr>
<tr><td>Co má platit i zítra, napište do souboru</td><td>Rozhovor se zapomene, soubor (návod, poznámka, skill) ne</td></tr>
</table>

<h2>Když to nevyjde napoprvé</h2>
<table class="wiki-tabulka">
<tr><th>Co se stane</th><th>Co s tím</th></tr>
<tr><td>Agent pochopil úkol jinak</td><td>Napište <code>/undo</code> a zkuste to přesněji. Řekněte mu, co jste čekali</td></tr>
<tr><td>Odpovídá pořád dokola nebo se zasekl</td><td><code>/stop</code>, případně začněte nový rozhovor <code>/new</code> a shrňte, co už víte</td></tr>
<tr><td>Došla paměť rozhovoru</td><td><code>/context</code> ukáže stav, <code>/compress</code> ho srovná</td></tr>
<tr><td>Něco rozbil</td><td><code>/rollback</code> vrátí soubory z uloženého bodu; u systémových změn se ptejte, než je udělá</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/vyber-modelu/"><strong>Výběr AI modelu</strong><span>Který model se vyplatí a kde ho pořídit</span></a>
<a href="/wiki/zaciname/telegram-a-discord/"><strong>Telegram a Discord</strong><span>Aby vám agent odpovídal i na mobilu</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/reference/slash-commands" target="_blank" rel="noopener"><strong>Všechny lomítkové příkazy</strong><span>Oficiální seznam (přes 160 příkazů, anglicky)</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Discord komunity</strong><span>Když si nevíte rady, napište nám</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Spuštění
hermes                 # rozhovor v terminálu
hermes chat -q "dotaz" # jeden dotaz bez rozhovoru (do skriptů)
hermes --continue      # pokračovat v posledním rozhovoru
hermes sessions        # seznam uložených konverzací

## Jak zadávat úkoly
- dávejte úkoly, které se dají ověřit (výsledek si přečtete)
- nejdřív zjištění („podívej se“), pak akce
- žádejte důkaz: „ukaž příkaz, kterým jsi to zjistil“
- jasně řekněte, co se nesmí (např. nic nemazat)
- velký úkol rozdělte na kroky

## Užitečné lomítkové příkazy
/help /new /model /context /compress /undo /retry /stop /queue /bg /status /rollback
Kompletní seznam: https://hermes-agent.nousresearch.com/docs/reference/slash-commands

## Schvalování
Před nebezpečnými příkazy se zobrazí panel „approval required“ s přesným příkazem.
Režim bez potvrzování (YOLO) se na serveru s daty nedoporučuje.

## V rozhovoru uvidíte
● nástroj  ✓/✗ výsledek  | blikající ukazatel = agent přemýšlí

## Když to nevyjde
- nepochopený úkol → /undo a upřesnit
- zaseknutí → /stop, případně /new a shrnout stav
- plná paměť → /context, /compress
- rozbité soubory → /rollback
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">💬</span><div><strong>An agent is not a search box.</strong>
Give it tasks whose result you can verify — and it does them: runs commands, reads files, writes things down.
Before you start, make sure you have <a href="/en/wiki/getting-started/choosing-a-model/">picked a model</a>.</div></div>

<h2>What it looks like</h2>
<p>Type <code>hermes</code> and a terminal conversation opens. You write plain English, the agent works:</p>
<div class="code-block"><span class="c"># start it</span>
<span class="p">$</span> hermes
<span class="c"># and a first task — verifiable, with a clear result</span>
<span class="p">❯</span> Check how much disk space is used and print it as a table.</div>
<p>In the conversation you see what the agent does: every tool it runs starts with <code>●</code> and ends with
<code>✓</code> (or <code>✗</code> when it failed). A blinking cursor means it is still thinking.</p>

<h2>How to give tasks that can be verified</h2>
<table class="wiki-tabulka">
<tr><th>Instead of</th><th>Write</th><th>Why</th></tr>
<tr><td>"Set up the server."</td><td>"Find the OS version and write it to <code>version.txt</code>."</td><td>You read the result and immediately know whether it was done right</td></tr>
<tr><td>"Tidy up the data."</td><td>"List the ten largest files in /var/log and delete nothing."</td><td>A small step you can check, with clear limits</td></tr>
<tr><td>"Fix it."</td><td>"Find the cause of the error in the log, tell me what it is and suggest two fixes — do not change anything yet."</td><td>Diagnosis before action keeps the agent from charging off in the wrong direction</td></tr>
<tr><td>"Check the website."</td><td>"Verify the page returns 200 and that the header declares utf-8; show me the exact command you used."</td><td>You want evidence, not an impression</td></tr>
</table>
<p class="note"><strong>Golden rule:</strong> the better you can verify the result yourself, the better the agent works.
If you cannot tell that a task is finished, neither can it.</p>

<h2>Useful slash commands</h2>
<p>Inside a chat you drive the agent with commands starting with a slash:</p>
<table class="wiki-tabulka">
<tr><th>Command</th><th>What it does</th></tr>
<tr><td><code>/help</code></td><td>Lists everything you can do in the chat</td></tr>
<tr><td><code>/new</code></td><td>Starts a fresh conversation (the old one stays saved)</td></tr>
<tr><td><code>/model</code></td><td>Switches model mid-task (expensive one only for hard work)</td></tr>
<tr><td><code>/context</code></td><td>Shows how full the conversation memory is</td></tr>
<tr><td><code>/compress</code></td><td>Trims the conversation memory when it fills up</td></tr>
<tr><td><code>/undo</code> and <code>/retry</code></td><td>Removes the last exchange / resends the last message</td></tr>
<tr><td><code>/stop</code></td><td>Kills all running background tasks</td></tr>
<tr><td><code>/queue</code> (or <code>/q</code>)</td><td>Queues the next task for when the current one finishes</td></tr>
<tr><td><code>/bg</code></td><td>Runs a task in the background while you carry on</td></tr>
<tr><td><code>/status</code></td><td>Shows model, profile, working directory and session ID</td></tr>
</table>
<p>The full list lives in the official documentation (160+ commands) — link below.</p>

<h2>Approvals: the agent asks before anything risky</h2>
<p>Before running something that can change or delete things, an <strong>approval panel</strong> appears
(<code>⚠ approval required</code>) showing the exact command. You confirm, or refuse and say what to do instead.
A mode where the agent never asks (<em>YOLO</em>) exists, but we do not recommend it on a server that holds data —
nobody is watching what gets run.</p>

<h2>Coming back later</h2>
<div class="code-block"><span class="c"># continue the most recent conversation</span>
<span class="p">$</span> hermes --continue
<span class="c"># list stored conversations and pick one</span>
<span class="p">$</span> hermes sessions
<span class="c"># a single question without opening a chat (handy in scripts)</span>
<span class="p">$</span> hermes chat -q "how much free disk space is there?"</div>

<h2>Tips from experience</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Ask it to inspect before acting</td><td>"Take a look…" instead of "Do…" saves you from cleaning up after a rushed change</td></tr>
<tr><td>Ask for evidence</td><td>"Show me the command you used." You verify both the result and that it was not invented</td></tr>
<tr><td>When it goes wrong, use <code>/stop</code></td><td>It halts running tasks. File changes can be reverted with <code>/rollback</code></td></tr>
<tr><td>Do not hand over one giant task</td><td>Split it into steps you can check. Smaller steps mean fewer dead ends</td></tr>
<tr><td>Anything that must last belongs in a file</td><td>A conversation is forgotten; a file (a guide, a note, a skill) is not</td></tr>
</table>

<h2>When it does not work first time</h2>
<table class="wiki-tabulka">
<tr><th>What happens</th><th>What to do</th></tr>
<tr><td>The agent understood it differently</td><td>Type <code>/undo</code> and be more specific. Tell it what you expected</td></tr>
<tr><td>It loops or gets stuck</td><td><code>/stop</code>, or start a new chat with <code>/new</code> and summarise what you know</td></tr>
<tr><td>The conversation memory is full</td><td><code>/context</code> shows the state, <code>/compress</code> trims it</td></tr>
<tr><td>It broke something</td><td><code>/rollback</code> restores files from a checkpoint; ask before system-wide changes</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/choosing-a-model/"><strong>Choosing an AI model</strong><span>Which model pays off and where to buy it</span></a>
<a href="/en/wiki/getting-started/telegram-and-discord/"><strong>Telegram and Discord</strong><span>So the agent answers on your phone too</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/reference/slash-commands" target="_blank" rel="noopener"><strong>All slash commands</strong><span>The official list (160+ commands)</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Community Discord</strong><span>Stuck? Ask us</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Starting
hermes                 # terminal conversation
hermes chat -q "question"  # one-shot question (handy in scripts)
hermes --continue      # continue the most recent conversation
hermes sessions        # list stored conversations

## Giving tasks
- give tasks whose result you can verify
- inspect first ("take a look"), act second
- ask for evidence: "show the command you used"
- state clearly what must not happen (e.g. delete nothing)
- split big tasks into steps

## Useful slash commands
/help /new /model /context /compress /undo /retry /stop /queue /bg /status /rollback
Full list: https://hermes-agent.nousresearch.com/docs/reference/slash-commands

## Approvals
Before dangerous commands an "approval required" panel shows the exact command.
The auto-approve mode (YOLO) is not recommended on a server holding data.

## In the transcript
● tool call  ✓/✗ result  | blinking cursor = the agent is thinking

## When it goes wrong
- misunderstood task -> /undo and clarify
- stuck -> /stop, or /new and summarise
- full memory -> /context, /compress
- broken files -> /rollback
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(3)
    stranka = najdi(3)
    assert stranka and "chat" in stranka["nazev"].lower()

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "První chat s Hermes Agentem — jak zadávat úkoly a co od agenta čekat",
        "Jak s agentem mluvit, aby jeho práce dávala smysl: ověřitelné úkoly, nejužitečnější lomítkové příkazy, schvalování a co dělat, když se něco zvrtne.",
        OBRAZEK, "Wiki · Začínáme", "První chat s agentem",
        "Agent není vyhledávač. Tady je, jak mu zadávat úkoly, aby se daly ověřit — a co dělat, když se něco zvrtne.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "První chat s agentem — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Your first chat with Hermes Agent — how to give tasks and what to expect",
        "How to talk to the agent so its work makes sense: verifiable tasks, the most useful slash commands, approvals and what to do when things go wrong.",
        OBRAZEK, "Wiki · Start here", "Your first chat",
        "An agent is not a search box. Here is how to give it tasks you can verify — and what to do when something goes wrong.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Your first chat — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
