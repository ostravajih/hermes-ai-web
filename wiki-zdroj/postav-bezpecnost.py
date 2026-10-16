#!/usr/bin/env python3
"""Postaví stránku wiki „Bezpečnost" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-security.md, guides-secure-hermes-on-a-work-machine.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/security"
OBRAZEK = "wiki-bezpecnost"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🛡️</span><div><strong>Agent umí spouštět příkazy a měnit soubory — proto má v sobě několik pojistek, které se navzájem jistí.</strong>
Většinu z nich nemusíte nastavovat, jsou zapnuté od začátku. Tato stránka shrnuje, co vás chrání
a kdy je potřeba přidat pozornost ručně.</div></div>

<h2>Šest pojistek, které drží pohromadě</h2>
<table class="wiki-tabulka">
<tr><th>Pojistka</th><th>Před čím chrání</th></tr>
<tr><td><strong>1. Kdo smí mluvit s agentem</strong></td><td>Před cizími lidmi. U Telegramu a Discordu rozhoduje seznam povolených účtů; kdo v něm není, agent ho neposlechne</td></tr>
<tr><td><strong>2. Potvrzení nebezpečných příkazů</strong></td><td>Před nevratnou škodou. Než agent spustí něco, co maže nebo přepisuje, musí si vyžádat vaše potvrzení</td></tr>
<tr><td><strong>3. Ochrana souborů</strong></td><td>Před přepsáním důležitých souborů. Klíče, nastavení agenta a další citlivé cesty jsou zakázané vždy</td></tr>
<tr><td><strong>4. Oddělené běhy</strong></td><td>Před útěkem mimo pískoviště. Práci je možné pustit v odděleném prostředí (kontejneru), odkud se nedostane ke zbytku serveru</td></tr>
<tr><td><strong>5. Kontrola projektových souborů</strong></td><td>Před podstrčenými příkazy. V textech a souborech projektu se hledá snaha ovlivnit agenta („podvrh“)</td></tr>
<tr><td><strong>6. Filtrování tajných hodnot</strong></td><td>Před únikem klíčů. Do příkazů a do pískoviště se předává jen to, co má smysl — ne celé prostředí serveru</td></tr>
</table>

<h2>Potvrzování příkazů — jak to vypadá v praxi</h2>
<p>Když se agent chystá na něco nebezpečného, místo vykonání se zeptá. Vy vidíte <strong>konkrétní příkaz</strong>
a rozhodnete: povolit jednou, povolit natrvalo (přidá se do trvalého seznamu) nebo odmítnout.</p>
<table class="wiki-tabulka">
<tr><th>Režim</th><th>Chování</th><th>Kdy se hodí</th></tr>
<tr><td><code>smart</code> (výchozí)</td><td>Ptá se u nebezpečných příkazů, u běžných ne</td><td>Vždy — je to rozumný kompromis</td></tr>
<tr><td>YOLO (bez dotazování)</td><td>Nepotřebuje potvrzení vůbec</td><td>Jen na vlastním serveru bez cizích dat a když víte, co děláte</td></tr>
</table>
<p>Některé příkazy agent odmítne vždy, i v režimu bez dotazování — to je pevná podlaha, která se
vypnout nedá. Když se vám zdá, že se ptá příliš často, můžete po schválení příkaz přidat do
<strong>trvalého seznamu</strong> (pak se už neptá) nebo se inspirovat vlastní historií schvalování
příkazem <code>hermes approvals suggest</code> — ten navrhne, co má smysl povolit natrvalo.</p>

<h2>Když u toho nikdo není</h2>
<p>Některé běhy probíhají bez dohledu: pravidelné úlohy v noci, dotazy z jiných systémů. Tam nestačí,
že se nemá kdo zeptat — <strong>nebezpečný příkaz se prostě odmítne</strong>. Stejně se agent chová
v režimu jednoho dotazu a u běhů spouštěných zvenčí. To je to, co drží automatizaci bezpečnou:
úloha, kterou jste napsali včera, nemůže v noci smazat server.</p>

<h2>Soubory a tajné údaje</h2>
<table class="wiki-tabulka">
<tr><th>Pravidlo</th><th>Vysvětlení</th></tr>
<tr><td>Klíče a hesla patří do nastavení agenta</td><td>Ne do textů, skillů ani do paměti. Nastavení je jedno místo, které se dá ohlídat a nezapisuje se do záloh kódu</td></tr>
<tr><td>Chráněné cesty jsou zakázané vždy</td><td>Agent nemůže přepsat vlastní nastavení ani soubory s přihlašovacími údaji</td></tr>
<tr><td>Dá se zapnout pískoviště pro zápisy</td><td>Volbou <code>HERMES_WRITE_SAFE_ROOT</code> omezíte, kam všude smí agent zapisovat</td></tr>
<tr><td>Tajnosti neopouštějí server</td><td>Do příkazů se předává jen omezený výběr hodnot z prostředí, ne všechno</td></tr>
</table>

<h2>Kdo s agentem smí mluvit</h2>
<p>Když je agent připojený k Telegramu nebo Discordu, je veřejně dostupný na kontakt — proto je
přístup omezený <strong>seznamem povolených účtů</strong> a u soukromých zpráv <strong>párováním</strong>
(neznámý člověk se musí nejdřív spárovat, teprve pak ho agent poslouchá). Víc v části
<a href="/wiki/zaciname/telegram-a-discord/">Telegram a Discord</a>.</p>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Nezapínejte režim bez dotazování na stroji s cizími daty</td><td>Jedna přehlédnutá chyba pak může vzít data ostatním. Výchozí nastavení nechte být, dokud nemáte důvod</td></tr>
<tr><td>Tajné údaje držte v nastavení</td><td>Nikdy je nepište do zadání, do skillů ani do poznámek pro agenta</td></tr>
<tr><td>Napojení (MCP) jen z ověřených zdrojů</td><td>Napojení je cizí kód s přístupem k vašemu serveru</td></tr>
<tr><td>Občas se zeptejte, co je povolené</td><td>V rozhovoru je k dispozici přehled <code>/security</code> — co je povolené natrvalo a které cesty jsou chráněné</td></tr>
<tr><td>Zálohy řešte dřív než oprávnění</td><td>Pojistky snižují riziko, ale zálohu nenahradí</td></tr>
</table>

<h2>Když to nefunguje</h2>
<table class="wiki-tabulka">
<tr><th>Co se děje</th><th>Příčina a co s tím</th></tr>
<tr><td>Agent se pořád ptá na to samé</td><td>Povolení platí jednou. Povolte příkaz natrvalo, nebo si nechte poradit přes <code>hermes approvals suggest</code></td></tr>
<tr><td>Agent odmítá i bezpečný příkaz</td><td>Příkaz spadá pod pevnou podlahu nebo pod vaše vlastní pravidlo zákazu. Zkuste jiný postup — lépe než vypínat pojistky</td></tr>
<tr><td>Agent neposlouchá v Telegramu</td><td>Nejste v seznamu povolených účtů, nebo chybí párování</td></tr>
<tr><td>Přestal fungovat zápis do souboru</td><td>Cesta je chráněná, nebo je zapnuté pískoviště pro zápisy. Ověřte, kam se smí zapisovat</td></tr>
<tr><td>Chci mít jistotu, že se nic nestalo samo</td><td>Podívejte se do historie běhů a do přehledu schválených příkazů</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/telegram-a-discord/"><strong>Telegram a Discord</strong><span>Kdo smí agenta ovládat</span></a>
<a href="/wiki/zaciname/mcp-nastroje/"><strong>MCP nástroje</strong><span>Napojení je cizí kód</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/security" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Bezpečnost do detailu (anglicky)</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Discord komunity</strong><span>Zeptejte se na zkušenosti</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Šest pojistek
1. kdo smí mluvit s agentem (seznam povolených účtů, párování u soukromých zpráv)
2. potvrzení nebezpečných příkazů (agent si vyžádá schválení)
3. ochrana souborů (chráněné cesty zakázané vždy)
4. oddělené běhy v kontejneru (pískoviště pro práci)
5. kontrola projektových souborů proti podstrčeným příkazům
6. filtrování tajných hodnot, které se předávají příkazům

## Potvrzování příkazů
- smart (výchozí): ptá se u nebezpečných, u běžných ne
- YOLO (bez dotazování): jen na vlastním serveru bez cizích dat
- pevná podlaha: některé příkazy se odmítnou vždy, i bez dotazování
- po schválení lze přidat do trvalého seznamu (už se neptá); hermes approvals suggest navrhne,
  co má smysl povolit natrvalo; /security ukáže přehled

## Bez dohledu (pravidelné úlohy, dotazy zvenčí, jeden dotaz)
Nebezpečný příkaz se prostě odmítne - nestačí, že se nemá kdo zeptat.

## Soubory a tajné údaje
- klíče a hesla do nastavení agenta, ne do textů/skillů/paměti
- chráněné cesty zakázané vždy (nastavení agenta, přihlašovací údaje)
- HERMES_WRITE_SAFE_ROOT omezuje, kam smí agent zapisovat
- do příkazů se předává jen omezený výběr hodnot z prostředí

## Tipy
- nezapínat režim bez dotazování na stroji s cizími daty
- MCP napojení jen z ověřených zdrojů (cizí kód s přístupem k serveru)
- zálohy řešit dřív než oprávnění
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🛡️</span><div><strong>The agent can run commands and change files — so it carries several safeguards that back each other up.</strong>
You do not have to configure most of them; they are on from the start. This page sums up what protects you
and when to add your own attention.</div></div>

<h2>Six safeguards working together</h2>
<table class="wiki-tabulka">
<tr><th>Safeguard</th><th>What it protects against</th></tr>
<tr><td><strong>1. Who may talk to the agent</strong></td><td>Strangers. On Telegram and Discord an allowlist of accounts decides; anyone outside it is not obeyed</td></tr>
<tr><td><strong>2. Approval of dangerous commands</strong></td><td>Irreversible damage. Before running something that deletes or overwrites, the agent asks for your approval</td></tr>
<tr><td><strong>3. File protection</strong></td><td>Overwriting important files. Keys, agent settings and other sensitive paths are always blocked</td></tr>
<tr><td><strong>4. Isolated runs</strong></td><td>Escaping the sandbox. Work can run in a separated environment (a container) with no way out to the rest of the server</td></tr>
<tr><td><strong>5. Project file scanning</strong></td><td>Injected instructions. Texts and project files are scanned for attempts to manipulate the agent</td></tr>
<tr><td><strong>6. Secret filtering</strong></td><td>Leaking keys. Commands and the sandbox receive only what makes sense — not the whole server environment</td></tr>
</table>

<h2>Command approval in practice</h2>
<p>When the agent is about to do something dangerous, it asks instead of acting. You see the
<strong>exact command</strong> and decide: allow once, allow permanently (it joins a permanent list), or deny.</p>
<table class="wiki-tabulka">
<tr><th>Mode</th><th>Behaviour</th><th>When to use it</th></tr>
<tr><td><code>smart</code> (default)</td><td>Asks for dangerous commands, not for ordinary ones</td><td>Always — a sensible balance</td></tr>
<tr><td>YOLO (no asking)</td><td>Needs no approval at all</td><td>Only on your own server with no one else's data, and when you know what you are doing</td></tr>
</table>
<p>Some commands are refused no matter what, even in the no-asking mode — a hard floor that cannot be
switched off. If it asks too often, you can allow a command permanently after approving it (then it stops
asking), or let the recorded approval history suggest it for you with <code>hermes approvals suggest</code>.</p>

<h2>When nobody is watching</h2>
<p>Some runs happen unattended: nightly scheduled jobs, requests from other systems. There it does not help
that nobody can answer — <strong>a dangerous command is simply denied</strong>. The same applies to
single-query sessions and runs triggered from outside. That is what keeps automation safe: a job you wrote
yesterday cannot delete the server at night.</p>

<h2>Files and secrets</h2>
<table class="wiki-tabulka">
<tr><th>Rule</th><th>Reason</th></tr>
<tr><td>Keys and passwords belong in the agent's settings</td><td>Not in texts, skills or memory. Settings are one place you can watch, and they are not written into code backups</td></tr>
<tr><td>Protected paths are always blocked</td><td>The agent cannot overwrite its own settings or files holding credentials</td></tr>
<tr><td>A write sandbox can be enabled</td><td><code>HERMES_WRITE_SAFE_ROOT</code> narrows where the agent may write</td></tr>
<tr><td>Secrets do not leave the server</td><td>Commands receive only a limited selection of environment values, not everything</td></tr>
</table>

<h2>Who may talk to the agent</h2>
<p>Once connected to Telegram or Discord, the agent is publicly reachable — so access is limited by an
<strong>allowlist of accounts</strong> and, for direct messages, by <strong>pairing</strong> (a stranger must
pair first, only then is the agent listening). More in
<a href="/en/wiki/getting-started/telegram-and-discord/">Telegram and Discord</a>.</p>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Do not enable the no-asking mode on a machine with other people's data</td><td>One oversight can then take everyone's data. Leave the default until you have a reason</td></tr>
<tr><td>Keep secrets in the settings</td><td>Never write them into prompts, skills or notes for the agent</td></tr>
<tr><td>Only connect MCP servers from trusted sources</td><td>A connection is third-party code with access to your server</td></tr>
<tr><td>Ask what is allowed now and then</td><td>Inside a chat, <code>/security</code> shows what is permanently allowed and which paths are protected</td></tr>
<tr><td>Sort backups before permissions</td><td>Safeguards lower the risk; they do not replace a backup</td></tr>
</table>

<h2>When it does not work</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>Cause and what to do</th></tr>
<tr><td>The agent keeps asking about the same thing</td><td>An approval is valid once. Allow the command permanently, or take the suggestion from <code>hermes approvals suggest</code></td></tr>
<tr><td>The agent refuses even a safe command</td><td>The command falls under the hard floor or under your own deny rule. Find another approach — better than disabling safeguards</td></tr>
<tr><td>The agent ignores me on Telegram</td><td>You are not on the allowlist, or pairing is missing</td></tr>
<tr><td>Writing to a file stopped working</td><td>The path is protected, or the write sandbox is on. Check where writing is permitted</td></tr>
<tr><td>I want certainty that nothing happened on its own</td><td>Look at the run history and the list of approved commands</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/telegram-and-discord/"><strong>Telegram and Discord</strong><span>Who may control the agent</span></a>
<a href="/en/wiki/getting-started/mcp-tools/"><strong>MCP tools</strong><span>A connection is third-party code</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/security" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Security in detail</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Community Discord</strong><span>Ask how others handle it</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Six safeguards
1. who may talk to the agent (account allowlist, DM pairing)
2. approval of dangerous commands
3. file protection (protected paths always blocked)
4. isolated runs in a container (sandbox)
5. project file scanning against injected instructions
6. secret filtering for what commands receive

## Command approval
- smart (default): asks for dangerous commands only
- YOLO (no asking): own server, no one else's data only
- hard floor: some commands are always refused, even without asking
- an approval is valid once; a command can be allowed permanently afterwards
  (hermes approvals suggest proposes what is worth allowlisting); /security shows the overview

## Unattended runs (scheduled jobs, external requests, single queries)
A dangerous command is simply denied - nobody being there to answer does not help.

## Files and secrets
- keys and passwords in the agent's settings, never in texts, skills or memory
- protected paths always blocked (agent settings, credentials)
- HERMES_WRITE_SAFE_ROOT narrows where the agent may write
- commands receive only a limited selection of environment values

## Tips
- no-asking mode is a bad idea on a machine with other people's data
- MCP connections from trusted sources only (they are third-party code)
- backups come before permissions
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(9)
    stranka = najdi(9)
    assert stranka and stranka["nazev"] == "Bezpečnost"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Bezpečnost — co agent smí a co musí odsouhlasit",
        "Šest pojistek, které agenta drží na uzdě: kdo s ním smí mluvit, potvrzení nebezpečných příkazů, ochrana souborů a filtrování tajných údajů.",
        OBRAZEK, "Wiki · Začínáme", "Bezpečnost",
        "Pojistky jsou zapnuté od začátku — a nebezpečný příkaz se u nehlídaných běhů prostě odmítne.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Bezpečnost — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Security — what the agent may do and what it must ask for",
        "Six safeguards keeping the agent in check: who may talk to it, approval of dangerous commands, file protection and secret filtering.",
        OBRAZEK, "Wiki · Start here", "Security",
        "The safeguards are on from the start — and in unattended runs a dangerous command is simply denied.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Security — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
