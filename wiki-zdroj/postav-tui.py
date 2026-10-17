#!/usr/bin/env python3
"""Postaví stránku wiki „TUI — práce v terminálu" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-tui.md (spuštění, příznaky, klávesy, příkazy lomítkem
s bohatším výstupem, automatické navázání, stavový řádek, myš, konfigurace).

Naše zkušenosti: TUI na VPS přes SSH (když spojení vypadne, pomůže automatické navázání),
v tmux zlobí sledování myši, na malý terminál je lepší sbalit živý dok.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "16. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/tui"
OBRAZEK = "wiki-tui"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⌨️</span><div><strong>TUI je terminálové rozhraní pro toho samého agenta.</strong>
Stejné rozhovory, stejné příkazy lomítkem jako dřív — jen s lepším rozvržením, stavovým
řádkem a přehledem o běžících pomocnících. Pro práci na serveru je to nejpohodlnější cesta.</div></div>

<h2>Spuštění</h2>
<div class="code-block"><span class="p">❯</span> hermes --tui                    <span class="c"># otevřít TUI</span>
<span class="p">❯</span> hermes --tui -c                 <span class="c"># navázat na poslední rozhovor</span>
<span class="p">❯</span> hermes --tui --resume latest    <span class="c"># totéž delším zápisem</span>
<span class="p">❯</span> hermes --tui -r 20260409_000000_aa11bb   <span class="c"># podle identifikátoru</span>
<span class="p">❯</span> hermes --tui --resume "můj projekt"      <span class="c"># podle názvu rozhovoru</span></div>
<p>Můžete si ho zapnout i natrvalo — buď proměnnou prostředí, nebo v nastavení. Explicitní
příznak vždycky vyhraje (jednorázově se do klasického režimu vrátíte přes <code>hermes --cli</code>):</p>
<div class="code-block"><span class="c"># dočasně pro toto okno</span>
<span class="p">❯</span> export HERMES_TUI=1
<span class="c"># nebo natrvalo v ~/.hermes/config.yaml</span>
display:
  interface: tui</div>

<h2>Proč ho používat</h2>
<table class="wiki-tabulka">
<tr><th>Výhoda</th><th>Co to znamená v praxi</th></tr>
<tr><td>Okamžité první vykreslení</td><td>Úvodní obrazovka je na místě dřív, než se všechno načte — terminál nepůsobí zaseknutě</td></tr>
<tr><td>Živý přehled o práci</td><td>Dole vidíte, kolik běží pomocníků a jaké procesy agent spustil na pozadí</td></tr>
<tr><td>Stavový řádek</td><td>Píše, co agent právě dělá (<code>ready</code>, <code>thinking…</code>, <code>running…</code>) a jak se jmenuje rozhovor</td></tr>
<tr><td>Bohatší příkazy lomítkem</td><td>Některé příkazy umí v TUI přehledovou tabulku nebo výběr z nabídky místo výpisu do textu</td></tr>
</table>

<h2>Příkazy lomítkem, které v TUI vypadají líp</h2>
<table class="wiki-tabulka">
<tr><th>Příkaz</th><th>Co udělá</th></tr>
<tr><td><code>/help</code></td><td>Přehled příkazů po skupinách, ovládaný šipkami</td></tr>
<tr><td><code>/sessions</code> (nebo <code>/switch</code>)</td><td>Přepínač otevřených rozhovorů — přepnutí, zavření, nový</td></tr>
<tr><td><code>/model</code></td><td>Výběr modelu podle poskytovatele, včetně orientační ceny</td></tr>
<tr><td><code>/usage</code></td><td>Přehled o spotřebě: tokeny, náklady, zaplnění kontextu</td></tr>
<tr><td><code>/agents</code> (nebo <code>/tasks</code>)</td><td>Strom běžících pomocníků s možností zastavit je a s přehledem nákladů</td></tr>
<tr><td><code>/details</code></td><td>Zapnutí podrobných výpisů volání nástrojů (pro celý běh nebo jen pro jednu část)</td></tr>
<tr><td><code>/skin</code></td><td>Změna vzhledu s živým náhledem</td></tr>
<tr><td><code>/reload</code></td><td>Znovu načte <code>~/.hermes/.env</code> — nové klíče platí bez restartu</td></tr>
<tr><td><code>/mouse</code></td><td>Nastavení sledování myši (viz past s tmux níž)</td></tr>
</table>

<h2>Klávesy</h2>
<table class="wiki-tabulka">
<tr><th>Klávesa</th><th>Co udělá</th></tr>
<tr><td><code>Ctrl+T</code></td><td>Rozbalí přehled běžící práce na celou obrazovku (pomocníci a procesy)</td></tr>
<tr><td><code>Ctrl+R</code></td><td>Přepne přehled mezi podrobným a jednou shrnující řádkou</td></tr>
<tr><td><code>Enter</code> nebo <code>t</code></td><td>V přehledu otevře živý přepis zvoleného pomocníka</td></tr>
<tr><td><code>d</code> / <code>e</code> / <code>x</code></td><td>Podrobnosti / vstoupit do práce / zastavit zvoleného pomocníka</td></tr>
</table>
<p class="note">Na macOS se funkční klávesa <code>F7</code> (v některých terminálech záložní
zkratka k <code>Ctrl+R</code>) nemusí předávat — MacBooky ji mají nastavenou na ovládání
systému. Držte <code>Fn</code> (klávesa se zeměkoulí) nebo použijte <code>Ctrl+R</code>.</p>

<h3>Psaní, když agent právě pracuje</h3>
<p>Text se neodkládá na později — vloží se do <strong>fronty na bráně</strong> a tam počká, až na něj
přijde řada. Když brána spadne nebo se restartuje, zpráva ve frontě zůstane; uvidíte ji jako
<code>[queued] …</code> i v jiném okně se stejným rozhovorem. Do přepisu se dostane, až když její
tah opravdu začne.</p>
<table class="wiki-tabulka">
<tr><th>Co uděláte</th><th>Co se stane</th></tr>
<tr><td>Napíšete a odešlete během práce agenta</td><td>Zpráva se zařadí do fronty a odejde po dokončení běžícího tahu</td></tr>
<tr><td><code>Ctrl+X</code> na zařazenou zprávu</td><td>Zruší ji na bráně — zmizí všem, kdo ten rozhovor vidí</td></tr>
<tr><td><code>Esc</code></td><td>Jen ukončí úpravu; zprávu nemaže</td></tr>
</table>

<h2>Když vypadne spojení</h2>
<p>Na serveru přes SSH se spojení občas utrhne. Dá se nastavit, aby se TUI po spuštění sám
vrátil k poslednímu rozhovoru:</p>
<div class="code-block"><span class="p">❯</span> export HERMES_TUI_RESUME=1        <span class="c"># vždy navázat na poslední rozhovor TUI</span>
<span class="p">❯</span> export HERMES_TUI_RESUME=&lt;id&gt;     <span class="c"># nebo na konkrétní rozhovor</span></div>

<h2>Pasti z našeho provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co se stalo</th><th>Co s tím</th></tr>
<tr><td><strong>V tmuxu se nad psacím polem pořád objevovalo „No image in clipboard“</strong></td><td>Sledování myši posílalo terminálu události, kterým tmux nerozuměl. Pomohl režim <code>/mouse wheel</code> (kolečko funguje, ale bez najíždění kurzoru)</td></tr>
<tr><td><strong>Na malém terminálu zbylo na psaní málo místa</strong></td><td>Přehled běžící práce se přizpůsobuje výšce okna; pomáhá <code>Ctrl+R</code> (jedna shrnující řádka) nebo práce v novém okně terminálu</td></tr>
<tr><td><strong>Příkaz spadl na chybě v Pythonu, přitom systém je v pořádku</strong></td><td>Když se pouští systémové nástroje z prostředí, které si nese vlastní Python, dědí se cesty ke knihovnám. Pomáhá spouštět je s čistým prostředím (<code>env -u PYTHONPATH</code>)</td></tr>
<tr><td><strong>Po úpravě nastavení se nic nezměnilo</strong></td><td>Nový klíč v <code>.env</code> platí po <code>/reload</code>; co je v <code>config.yaml</code>, se načítá při startu rozhovoru</td></tr>
<tr><td><strong>Přepnul jsem na TUI a nešlo se vrátit</strong></td><td>Jednorázově <code>hermes --cli</code>, natrvalo změnit <code>display.interface</code> v nastavení</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Rozhovory si pojmenujte (<code>/title</code>)</td><td>V přepínači i v navazování se pak hledá mnohem líp</td></tr>
<tr><td>Dlouhé úlohy pouštějte na pozadí</td><td>V TUI vidíte, co běží, a můžete mezitím zadávat další práci</td></tr>
<tr><td>Na serveru používejte tmux nebo screen</td><td>Když spojení vypadne, práce i agent zůstanou běžet</td></tr>
<tr><td>Sledujte stavový řádek</td><td><code>thinking…</code> znamená, že agent pracuje — nemusíte psát další dotaz „tak co?“</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/funkce/desktop/"><strong>Desktop</strong><span>Když chcete okno s tlačítky</span></a>
<a href="/wiki/funkce/sezeni/"><strong>Sezení a jejich obnova</strong><span>Jak se v rozhovorech neztratit</span></a>
<a href="/wiki/funkce/podagenti/"><strong>Podagenti</strong><span>Práce, kterou zvládne víc pomocníků</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/tui" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>TUI do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co TUI je
Terminálové rozhraní pro stejného agenta: stejné rozhovory, stejné příkazy lomítkem,
lepší rozvržení, stavový řádek a přehled o běžící práci. Doporučený způsob interaktivní práce.

## Spuštění
hermes --tui · hermes --tui -c (navázat na poslední) · --resume latest · -r <id> · --resume "název"
Dočasně: export HERMES_TUI=1 · natrvalo: display.interface: tui v config.yaml
Jednorázově zpět do klasického režimu: hermes --cli

## Příkazy lomítkem s bohatším výstupem
/help (přehled po skupinách) · /sessions neboli /switch (přepínač rozhovorů) · /model (výběr a cena) ·
/usage (tokeny, náklady, kontext) · /agents neboli /tasks (strom pomocníků, zastavení) ·
/details (podrobná volání nástrojů) · /skin (vzhled) · /reload (znovu načte .env) · /mouse

## Klávesy
Ctrl+T přehled běžící práce na celou obrazovku · Ctrl+R podrobný/shrnutý přehled ·
Enter nebo t živý přepis pomocníka · d podrobnosti · e vstoupit do práce · x zastavit
macOS: F7 se nemusí předávat, držet Fn nebo použít Ctrl+R.

## Výpadek spojení
export HERMES_TUI_RESUME=1 (vždy navázat na poslední rozhovor TUI) nebo =<id>

## Pasti z našeho provozu
1. tmux + sledování myši -> "No image in clipboard" nad psacím polem; pomohl /mouse wheel.
2. Malý terminál -> méně místa na psaní; Ctrl+R sbalí přehled, případně nové okno.
3. Systémové nástroje spuštěné z prostředí s vlastním Pythonem dědí cesty ke knihovnám;
   pomáhá env -u PYTHONPATH.
4. Nový klíč v .env platí po /reload; config.yaml se načítá při startu rozhovoru.
5. Návrat do klasického režimu: hermes --cli (jednorázově) nebo display.interface v nastavení.

## Tipy
Pojmenovat rozhovory (/title) · dlouhé úlohy na pozadí · na serveru tmux/screen · sledovat stavový
řádek (thinking… = agent pracuje).
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⌨️</span><div><strong>The TUI is a terminal interface for the same agent.</strong>
Same conversations, same slash commands as before — with a cleaner layout, a status line and a
live view of work in progress. On a server it is the most comfortable way to work.</div></div>

<h2>Launch</h2>
<div class="code-block"><span class="p">❯</span> hermes --tui                    <span class="c"># open the TUI</span>
<span class="p">❯</span> hermes --tui -c                 <span class="c"># resume the latest conversation</span>
<span class="p">❯</span> hermes --tui --resume latest    <span class="c"># the same, spelled out</span>
<span class="p">❯</span> hermes --tui -r 20260409_000000_aa11bb   <span class="c"># by session id</span>
<span class="p">❯</span> hermes --tui --resume "my project"       <span class="c"># by session title</span></div>
<p>You can make it permanent — with an environment variable or in the settings. An explicit flag
always wins (to drop back to the classic REPL for one run: <code>hermes --cli</code>):</p>
<div class="code-block"><span class="c"># for this shell only</span>
<span class="p">❯</span> export HERMES_TUI=1
<span class="c"># or permanently in ~/.hermes/config.yaml</span>
display:
  interface: tui</div>

<h2>Why use it</h2>
<table class="wiki-tabulka">
<tr><th>Benefit</th><th>What it means in practice</th></tr>
<tr><td>Instant first frame</td><td>The banner paints before everything finishes loading — the terminal never feels stuck</td></tr>
<tr><td>A live view of work</td><td>You see how many helpers are running and which background processes the agent started</td></tr>
<tr><td>A status line</td><td>Says what the agent is doing (<code>ready</code>, <code>thinking…</code>, <code>running…</code>) and the session title</td></tr>
<tr><td>Richer slash commands</td><td>Some commands render a navigable panel or picker in the TUI instead of plain text</td></tr>
</table>

<h2>Slash commands that look better in the TUI</h2>
<table class="wiki-tabulka">
<tr><th>Command</th><th>What it does</th></tr>
<tr><td><code>/help</code></td><td>Commands grouped by category, navigable with arrow keys</td></tr>
<tr><td><code>/sessions</code> (or <code>/switch</code>)</td><td>Live session switcher — switch, close or open one</td></tr>
<tr><td><code>/model</code></td><td>Model picker grouped by provider, with cost hints</td></tr>
<tr><td><code>/usage</code></td><td>Tokens, cost and context usage panel</td></tr>
<tr><td><code>/agents</code> (or <code>/tasks</code>)</td><td>Tree of running helpers with per-branch cost and stop controls</td></tr>
<tr><td><code>/details</code></td><td>Verbose tool-call details (globally or per section)</td></tr>
<tr><td><code>/skin</code></td><td>Theme change with a live preview</td></tr>
<tr><td><code>/reload</code></td><td>Re-reads <code>~/.hermes/.env</code> so new keys work without a restart</td></tr>
<tr><td><code>/mouse</code></td><td>Mouse tracking preset (see the tmux pitfall below)</td></tr>
</table>

<h2>Keys</h2>
<table class="wiki-tabulka">
<tr><th>Key</th><th>What it does</th></tr>
<tr><td><code>Ctrl+T</code></td><td>Expands the live work dock to full height (helpers and processes)</td></tr>
<tr><td><code>Ctrl+R</code></td><td>Toggles the dock between detailed and a single summary line</td></tr>
<tr><td><code>Enter</code> or <code>t</code></td><td>Opens the live transcript of the selected helper</td></tr>
<tr><td><code>d</code> / <code>e</code> / <code>x</code></td><td>Details / steer it / stop it</td></tr>
</table>
<p class="note">On macOS the function key <code>F7</code> (a fallback binding for <code>Ctrl+R</code>
in some terminals) may not be forwarded — MacBooks use that row for system controls. Hold
<code>Fn</code> (the globe key) or just use <code>Ctrl+R</code>.</p>

<h3>Typing while the agent is working</h3>
<p>Your text is not held back — it goes into the <strong>gateway queue</strong> and waits its turn.
If the gateway crashes or restarts, the queued message survives; you see it as <code>[queued] …</code>
in any other window attached to the same conversation. It appears in the transcript only when its
own turn actually starts.</p>
<table class="wiki-tabulka">
<tr><th>What you do</th><th>What happens</th></tr>
<tr><td>Type and send while the agent is busy</td><td>The message is queued and goes out after the running turn finishes</td></tr>
<tr><td><code>Ctrl+X</code> on a queued message</td><td>Cancels it on the gateway — it disappears for everyone viewing the conversation</td></tr>
<tr><td><code>Esc</code></td><td>Only ends editing; it does not delete the message</td></tr>
</table>

<h2>When the connection drops</h2>
<p>Over SSH the link sometimes breaks. You can make the TUI re-attach to your last conversation on
launch:</p>
<div class="code-block"><span class="p">❯</span> export HERMES_TUI_RESUME=1        <span class="c"># always resume the most recent TUI session</span>
<span class="p">❯</span> export HERMES_TUI_RESUME=&lt;id&gt;     <span class="c"># or a specific one</span></div>

<h2>Pitfalls from our systems</h2>
<table class="wiki-tabulka">
<tr><th>What happened</th><th>What to do</th></tr>
<tr><td><strong>Inside tmux the prompt row kept showing "No image in clipboard"</strong></td><td>Mouse tracking sent events tmux did not understand. The <code>/mouse wheel</code> preset fixed it (scrolling works, hover events are off)</td></tr>
<tr><td><strong>On a small terminal there was little room to type</strong></td><td>The dock fits the terminal height; <code>Ctrl+R</code> collapses it to one line, or use a separate terminal window</td></tr>
<tr><td><strong>A command died with a Python error although the system was fine</strong></td><td>System tools launched from an environment carrying its own Python inherit library paths. Running them with a clean environment (<code>env -u PYTHONPATH</code>) fixes it</td></tr>
<tr><td><strong>After editing settings nothing changed</strong></td><td>A new key in <code>.env</code> applies after <code>/reload</code>; what is in <code>config.yaml</code> is read when a session starts</td></tr>
<tr><td><strong>I switched to the TUI and could not get back</strong></td><td><code>hermes --cli</code> for one run, or change <code>display.interface</code> in the settings</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Name your sessions (<code>/title</code>)</td><td>The switcher and resume become far easier to use</td></tr>
<tr><td>Run long jobs in the background</td><td>The TUI shows what is running while you give it the next task</td></tr>
<tr><td>On a server, use tmux or screen</td><td>If the connection drops, your work and the agent keep running</td></tr>
<tr><td>Watch the status line</td><td><code>thinking…</code> means the agent is working — no need to ask "so, how is it going?"</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/features/desktop/"><strong>Desktop</strong><span>When you want a window with buttons</span></a>
<a href="/en/wiki/features/sessions/"><strong>Sessions and recovery</strong><span>How not to lose track of conversations</span></a>
<a href="/en/wiki/features/subagents/"><strong>Subagents</strong><span>Work several helpers can share</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/tui" target="_blank" rel="noopener"><strong>Official documentation</strong><span>The TUI in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What the TUI is
A terminal interface for the same agent: same conversations, same slash commands, a cleaner layout,
a status line and a live view of work in progress. The recommended interactive way to run Hermes.

## Launch
hermes --tui · hermes --tui -c (resume latest) · --resume latest · -r <id> · --resume "title"
Temporarily: export HERMES_TUI=1 · permanently: display.interface: tui in config.yaml
Back to the classic REPL for one run: hermes --cli

## Slash commands with richer output
/help (grouped) · /sessions or /switch (session switcher) · /model (picker with cost) ·
/usage (tokens, cost, context) · /agents or /tasks (helper tree, stop controls) ·
/details (verbose tool calls) · /skin · /reload (re-reads .env) · /mouse

## Keys
Ctrl+T full-height work dock · Ctrl+R detailed/summary dock · Enter or t live transcript ·
d details · e steer · x stop. macOS: F7 may not be forwarded — hold Fn or use Ctrl+R.

## Dropped connection
export HERMES_TUI_RESUME=1 (always resume the most recent TUI session) or =<id>

## Pitfalls from our systems
1. tmux + mouse tracking -> "No image in clipboard" above the prompt; /mouse wheel fixed it.
2. Small terminal -> little room to type; Ctrl+R collapses the dock, or use another window.
3. System tools launched from an environment with its own Python inherit library paths;
   env -u PYTHONPATH fixes it.
4. A new key in .env applies after /reload; config.yaml is read when a session starts.
5. To go back to the classic REPL: hermes --cli, or change display.interface.

## Tips
Name sessions (/title) · long jobs in the background · tmux/screen on a server · watch the status
line (thinking… means the agent is working).
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(16)
    stranka = najdi(16)
    assert stranka and stranka["nazev"].startswith("TUI")

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "TUI — práce s agentem v terminálu",
        "Terminálové rozhraní pro Hermes Agenta: spuštění, navázání na rozhovor, bohatší příkazy lomítkem, klávesy, stavový řádek a pasti z našeho provozu na serveru.",
        OBRAZEK, "Wiki · Funkce do hloubky", "TUI — práce v terminálu",
        "Nejpohodlnější cesta k agentovi na serveru: přehled o běžící práci, stavový řádek a rozhovory, ke kterým se dá vrátit i po výpadku spojení.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "TUI — práce v terminálu — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "TUI — working with the agent in the terminal",
        "The terminal interface for Hermes Agent: launching, resuming a conversation, richer slash commands, keys, the status line and pitfalls from our servers.",
        OBRAZEK, "Wiki · Features in depth", "TUI — working in the terminal",
        "The most comfortable way to reach an agent on a server: a live view of running work, a status line and conversations you can resume after a dropped connection.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "TUI — working in the terminal — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
