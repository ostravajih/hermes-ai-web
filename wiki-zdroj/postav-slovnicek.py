#!/usr/bin/env python3
"""Postaví stránku wiki „Slovníček pojmů" (česky + anglicky) včetně verze pro AI.

Podklady: vlastní stránky wiki (aby výklad seděl s tím, co je jinde na webu),
reference-faq.md, user-guide-features-memory.md, user-guide-features-mcp.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs"
OBRAZEK = "wiki-slovnicek"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📖</span><div><strong>Slova, která se kolem agenta používají — lidsky a bez zkratek.</strong>
Když na nějaké narazíte jinde a nebudete si jistí, vraťte se sem. Co je na této stránce,
platí i na ostatních stránkách wiki.</div></div>

<h2>Základní pojmy</h2>
<table class="wiki-tabulka">
<tr><th>Pojem</th><th>Co to znamená</th></tr>
<tr><td><strong>Agent</strong></td><td>Program, kterému zadáváte úkoly lidskou řečí a který je sám vykonává — spouští příkazy, čte a mění soubory, hledá na webu. Nejen odpovídá, ale opravdu koná.</td></tr>
<tr><td><strong>Model</strong> (jazykový model)</td><td>„Mozek“, který rozumí textu a rozhoduje, co udělat. Bývá v cizí službě, za její používání se platí. Různé modely se liší schopnostmi, rychlostí a cenou.</td></tr>
<tr><td><strong>Poskytovatel modelu</strong></td><td>Firma, u které si model pronajímáte (platíte za spotřebu). Vybírá se podle ceny a schopností. Přehled v části <a href="/wiki/zaciname/vyber-modelu/">Výběr AI modelu</a>.</td></tr>
<tr><td><strong>Klíč</strong> (API klíč)</td><td>Tajný údaj, kterým se agent prokazuje u poskytovatele modelu — obdoba hesla. Patří do nastavení agenta, nikdy do textů, skillů nebo do zpráv lidem.</td></tr>
<tr><td><strong>Token</strong></td><td>Kousek textu, ze kterého se počítá spotřeba (zhruba tři čtvrtě slova). Platíte za počet tokenů, které agent pošle a přijme.</td></tr>
<tr><td><strong>Kontext</strong></td><td>Kolik textu si model naráz udrží — probíhající rozhovor včetně instrukcí a odpovědí. Když je delší než model unese, rozhovor se musí srovnat nebo začít znovu.</td></tr>
</table>

<h2>Jak se s agentem mluví</h2>
<table class="wiki-tabulka">
<tr><th>Pojem</th><th>Co to znamená</th></tr>
<tr><td><strong>Zadání</strong></td><td>Co po agentovi chcete — běžná věta, žádná zvláštní syntaxe. Konkrétní zadání („co, odkud, komu, jak dlouhé“) dopadne lépe než obecné.</td></tr>
<tr><td><strong>Lomítkový příkaz</strong></td><td>Krátký pokyn začínající lomítkem, kterým ovládáte agenta přímo — například <code>/new</code> (nový rozhovor), <code>/compress</code> (srovnat rozhovor), <code>/learn</code> (nauč se postup).</td></tr>
<tr><td><strong>Rozhovor</strong> (relace)</td><td>Jedno souvislé povídání s agentem. Má svou paměť „v hlavě“, a když je dlouhé, agent si ho srovná, aby se do něj vešlo, co je důležité.</td></tr>
<tr><td><strong>Důkaz</strong></td><td>Podklad, o který se tvrzení opírá — výpis příkazu, obsah souboru, naměřené číslo. Naše zásada: tvrzení bez důkazu se nebere.</td></tr>
</table>

<h2>Co agent umí (a z čeho to je)</h2>
<table class="wiki-tabulka">
<tr><th>Pojem</th><th>Co to znamená</th></tr>
<tr><td><strong>Nástroj</strong></td><td>Základní schopnost agenta: spustit příkaz, přečíst soubor, vyhledat na webu, poslat zprávu. Nástroje má od začátku.</td></tr>
<tr><td><strong>Skill</strong></td><td>Zapsaný postup pro určitou činnost („jak u nás zálohovat databázi“). Agent si ho přečte, až když ho potřebuje. Více v části <a href="/wiki/zaciname/skilly/">Skilly</a>.</td></tr>
<tr><td><strong>Plugin</strong></td><td>Programové rozšíření samotného agenta (nová funkce v kódu, píše se v Pythonu). Pro běžné používání ho řešit nemusíte — většinou stačí skilly.</td></tr>
<tr><td><strong>Napojení</strong> (MCP)</td><td>Připojení agenta k hotovému rozhraní cizí služby (GitHub, nástroj pro automatizaci, prohlížeč). Napojení je cizí kód — berte ho z ověřených zdrojů. Více v části <a href="/wiki/zaciname/mcp-nastroje/">MCP nástroje</a>.</td></tr>
<tr><td><strong>Brána</strong> (gateway)</td><td>Část agenta, přes kterou jde spojení s Telegramem, Discordem a dalšími platformami. Když neběží, agent neodpovídá na zprávy z mobilu — a nespouští se ani plánované úlohy.</td></tr>
<tr><td><strong>Plánovaná úloha</strong> (cron)</td><td>Úkol, který agent vykonává sám podle plánu (ráno přehled, v noci kontrola). Více v části <a href="/wiki/zaciname/pravidelne-ulohy/">Pravidelné úlohy</a>.</td></tr>
</table>

<h2>Kde to všechno žije</h2>
<table class="wiki-tabulka">
<tr><th>Pojem</th><th>Co to znamená</th></tr>
<tr><td><strong>Server</strong> (VPS)</td><td>Počítač, který běží pořád a je připojený k internetu — agent na něm bydlí. Proti domácímu počítači má výhodu, že se nevypíná.</td></tr>
<tr><td><strong>Terminál</strong></td><td>Okno, do kterého se vkládají příkazy (a potvrzují Enterem). Nic se neděje samo — každý příkaz vložíte vy.</td></tr>
<tr><td><strong>Domovská složka agenta</strong></td><td><code>~/.hermes/</code> — tam jsou rozhovory, paměť, skilly, nastavení a klíče. Když se zálohuje, zálohuje se tohle.</td></tr>
<tr><td><strong>Repozitář</strong> (git)</td><td>Složka s historií změn — každá úprava má svůj záznam a dá se vrátit. Používá se u webů a kódu, ne u nastavení agenta.</td></tr>
</table>

<h2>Bezpečnost a provoz</h2>
<table class="wiki-tabulka">
<tr><th>Pojem</th><th>Co to znamená</th></tr>
<tr><td><strong>Schválení</strong></td><td>Potvrzení, které agent vyžádá před nebezpečným příkazem (mazání, přepis). Bez vašeho souhlasu se nic takového nestane.</td></tr>
<tr><td><strong>Seznam povolených</strong></td><td>Výčet účtů, které smí agenta ovládat přes Telegram nebo Discord. Kdo v něm není, agent ho neposlechne.</td></tr>
<tr><td><strong>Párování</strong></td><td>První bezpečné spojení s novým člověkem přes soukromou zprávu — teprve pak ho agent poslouchá.</td></tr>
<tr><td><strong>Pískoviště</strong> (sandbox)</td><td>Oddělené prostředí, ve kterém může práce běžet, aby se nedostala ke zbytku serveru. Dá se omezit i to, kam smí agent zapisovat.</td></tr>
<tr><td><strong>Telemetrie</strong></td><td>Sbírání údajů o používání. Hermes Agent žádnou neposílá — vaše rozhovory, paměť a skilly zůstávají u vás.</td></tr>
<tr><td><strong>Záloha</strong></td><td>Kopie dat, ze které se dá obnovit. U agenta se zálohuje složka <code>~/.hermes/</code>, u webu zase celý web.</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/"><strong>Wiki — všechny návody</strong><span>Začínáme, od instalace po bezpečnost</span></a>
<a href="/wiki/zaciname/caste-dotazy/"><strong>Časté dotazy</strong><span>Krátké odpovědi na časté otázky</span></a>
<a href="/wiki/zaciname/kdyz-se-neco-pokazi/"><strong>Když se něco pokazí</strong><span>Co dělat, když to nechodí</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Discord komunity</strong><span>Zeptejte se na cokoli dalšího</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
# Slovníček pojmů (lidsky)

## Základní
- Agent: program, kterému zadáváte úkoly řečí a který je sám vykonává (nejen odpovídá).
- Model (jazykový model): "mozek", rozumí textu a rozhoduje; bývá v cizí službě, platí se za spotřebu.
- Poskytovatel modelu: firma, u které si model pronajímáte.
- Klíč (API klíč): tajný údaj, kterým se agent prokazuje u poskytovatele; patří do nastavení, ne do textů.
- Token: kousek textu, ze kterého se počítá spotřeba (asi 3/4 slova).
- Kontext: kolik textu si model naráz udrží; když je rozhovor delší, musí se srovnat nebo začít nový.

## Jak se mluví
- Zadání: co po agentovi chcete, běžná věta; konkrétní zadání dopadne lépe.
- Lomítkový příkaz: /new, /compress, /learn - ovládání agenta přímo.
- Rozhovor (relace): jedno souvislé povídání s agentem.
- Důkaz: podklad k tvrzení (výpis příkazu, obsah souboru) - tvrzení bez důkazu se nebere.

## Co agent umí
- Nástroj: základní schopnost (terminál, soubory, web, zprávy).
- Skill: zapsaný postup, přečte se až když je potřeba.
- Plugin: programové rozšíření agenta (Python); pro běžné používání stačí skilly.
- Napojení (MCP): připojení k hotovému rozhraní cizí služby; je to cizí kód, jen z ověřených zdrojů.
- Brána (gateway): spojení s Telegramem/Discordem a spouštění plánovaných úloh.
- Plánovaná úloha (cron): úkol, který agent vykonává sám podle plánu.

## Kde to žije
- Server (VPS): počítač, který běží pořád; agent na něm bydlí.
- Terminál: okno pro příkazy, které vkládáte vy a potvrzujete Enterem.
- ~/.hermes/: domovská složka agenta - rozhovory, paměť, skilly, nastavení, klíče; tohle se zálohuje.
- Repozitář (git): složka s historií změn.

## Bezpečnost a provoz
- Schválení: potvrzení před nebezpečným příkazem.
- Seznam povolených: účty, které smí agenta ovládat.
- Párování: první bezpečné spojení s novým člověkem přes soukromou zprávu.
- Pískoviště (sandbox): oddělené prostředí pro práci.
- Telemetrie: sbírání údajů o používání - Hermes Agent žádnou neposílá.
- Záloha: kopie dat pro obnovu (~/.hermes/ u agenta, celý web u webu).
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📖</span><div><strong>The words people use around the agent — in plain language, no jargon.</strong>
When you meet one somewhere else and are unsure, come back here. What this page says holds on the other
wiki pages too.</div></div>

<h2>The basics</h2>
<table class="wiki-tabulka">
<tr><th>Term</th><th>What it means</th></tr>
<tr><td><strong>Agent</strong></td><td>A program you brief in plain language that then carries the work out itself — runs commands, reads and changes files, searches the web. It does not just answer, it acts.</td></tr>
<tr><td><strong>Model</strong> (language model)</td><td>The "brain" that understands text and decides what to do. It usually lives in someone else's service and you pay for its usage. Models differ in ability, speed and price.</td></tr>
<tr><td><strong>Model provider</strong></td><td>The company you rent a model from (you pay per usage). You choose by price and capability. See <a href="/en/wiki/getting-started/choosing-a-model/">choosing a model</a>.</td></tr>
<tr><td><strong>Key</strong> (API key)</td><td>The secret the agent identifies itself with at the model provider — like a password. It belongs in the agent's settings, never in texts, skills or messages to people.</td></tr>
<tr><td><strong>Token</strong></td><td>A chunk of text that usage is counted in (roughly three quarters of a word). You pay for the tokens the agent sends and receives.</td></tr>
<tr><td><strong>Context</strong></td><td>How much text the model holds at once — the live conversation including instructions and replies. When it grows past what the model can hold, the conversation must be trimmed or restarted.</td></tr>
</table>

<h2>Talking to the agent</h2>
<table class="wiki-tabulka">
<tr><th>Term</th><th>What it means</th></tr>
<tr><td><strong>Prompt</strong></td><td>What you want from the agent — an ordinary sentence, no special syntax. A specific prompt ("what, from where, to whom, how long") turns out better than a vague one.</td></tr>
<tr><td><strong>Slash command</strong></td><td>A short instruction starting with a slash that controls the agent directly — for example <code>/new</code> (fresh conversation), <code>/compress</code> (trim the conversation), <code>/learn</code> (learn a procedure).</td></tr>
<tr><td><strong>Conversation</strong> (session)</td><td>One continuous exchange with the agent. It keeps its own running memory, and when it gets long the agent trims it so the important parts still fit.</td></tr>
<tr><td><strong>Evidence</strong></td><td>What a claim rests on — command output, file contents, a measured number. Our rule: a claim without evidence is not accepted.</td></tr>
</table>

<h2>What the agent can do (and what it is made of)</h2>
<table class="wiki-tabulka">
<tr><th>Term</th><th>What it means</th></tr>
<tr><td><strong>Tool</strong></td><td>A core ability of the agent: run a command, read a file, search the web, send a message. Tools are available from the start.</td></tr>
<tr><td><strong>Skill</strong></td><td>A written procedure for a particular job ("how we back up the database here"). The agent reads it when it needs it. See <a href="/en/wiki/getting-started/skills/">Skills</a>.</td></tr>
<tr><td><strong>Plugin</strong></td><td>A code extension of the agent itself (a new feature, written in Python). Day-to-day use rarely needs one — skills are usually enough.</td></tr>
<tr><td><strong>Connection</strong> (MCP)</td><td>Linking the agent to a service's ready-made interface (GitHub, an automation tool, a browser). A connection is third-party code — take it from trusted sources. See <a href="/en/wiki/getting-started/mcp-tools/">MCP tools</a>.</td></tr>
<tr><td><strong>Gateway</strong></td><td>The part of the agent that carries the link to Telegram, Discord and other platforms. With it down, the agent does not answer messages from your phone — and scheduled jobs do not fire either.</td></tr>
<tr><td><strong>Scheduled job</strong> (cron)</td><td>A task the agent performs by itself on a schedule (a morning brief, a nightly check). See <a href="/en/wiki/getting-started/scheduled-tasks/">Scheduled tasks</a>.</td></tr>
</table>

<h2>Where it all lives</h2>
<table class="wiki-tabulka">
<tr><th>Term</th><th>What it means</th></tr>
<tr><td><strong>Server</strong> (VPS)</td><td>A computer that is always on and connected to the internet — the agent's home. Its advantage over a home computer is that it never shuts down.</td></tr>
<tr><td><strong>Terminal</strong></td><td>The window where commands are pasted (and confirmed with Enter). Nothing happens on its own — you paste every command.</td></tr>
<tr><td><strong>The agent's home folder</strong></td><td><code>~/.hermes/</code> — conversations, memory, skills, settings and keys live there. Backing up means backing up this.</td></tr>
<tr><td><strong>Repository</strong> (git)</td><td>A folder with a history of changes — every edit is recorded and can be rolled back. Used for websites and code, not for the agent's settings.</td></tr>
</table>

<h2>Safety and operation</h2>
<table class="wiki-tabulka">
<tr><th>Term</th><th>What it means</th></tr>
<tr><td><strong>Approval</strong></td><td>The confirmation the agent asks for before a dangerous command (deleting, overwriting). Nothing like that happens without your consent.</td></tr>
<tr><td><strong>Allowlist</strong></td><td>The list of accounts allowed to control the agent over Telegram or Discord. Anyone outside it is not obeyed.</td></tr>
<tr><td><strong>Pairing</strong></td><td>The first safe contact with a new person over a direct message — only then does the agent listen to them.</td></tr>
<tr><td><strong>Sandbox</strong></td><td>A separated environment work can run in, so it cannot reach the rest of the server. Where the agent may write can be narrowed as well.</td></tr>
<tr><td><strong>Telemetry</strong></td><td>Collection of usage data. Hermes Agent sends none — your conversations, memory and skills stay with you.</td></tr>
<tr><td><strong>Backup</strong></td><td>A copy of data you can restore from. For the agent you back up <code>~/.hermes/</code>; for a website, the whole site.</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/"><strong>Wiki — all the guides</strong><span>From installation to security</span></a>
<a href="/en/wiki/getting-started/faq/"><strong>Frequently asked questions</strong><span>Short answers to common questions</span></a>
<a href="/en/wiki/getting-started/troubleshooting/"><strong>When something breaks</strong><span>What to do when it will not work</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Community Discord</strong><span>Ask about anything else</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
# Glossary (plain language)

## The basics
- Agent: a program you brief in plain language that carries work out itself (not just answering).
- Model (language model): the "brain" that understands text and decides; usually in a paid service.
- Model provider: the company you rent a model from.
- Key (API key): the secret identifying the agent at the provider; belongs in settings, not in texts.
- Token: a chunk of text usage is counted in (about 3/4 of a word).
- Context: how much text the model holds at once; a longer conversation must be trimmed or restarted.

## Talking to it
- Prompt: what you want, an ordinary sentence; specific prompts work better.
- Slash command: /new, /compress, /learn - direct control of the agent.
- Conversation (session): one continuous exchange with the agent.
- Evidence: what a claim rests on (command output, file contents); no evidence, no claim.

## What it can do
- Tool: a core ability (terminal, files, web, messages).
- Skill: a written procedure, read when needed.
- Plugin: a code extension of the agent (Python); skills are usually enough.
- Connection (MCP): linking to a service's ready-made interface; third-party code, trusted sources only.
- Gateway: the link to Telegram/Discord and the runner of scheduled jobs.
- Scheduled job (cron): a task the agent performs by itself on a schedule.

## Where it lives
- Server (VPS): an always-on computer; the agent's home.
- Terminal: the window for commands you paste and confirm with Enter.
- ~/.hermes/: the agent's home folder - conversations, memory, skills, settings, keys; this is what you back up.
- Repository (git): a folder with a history of changes.

## Safety and operation
- Approval: confirmation before a dangerous command.
- Allowlist: accounts allowed to control the agent.
- Pairing: the first safe contact with a new person over a direct message.
- Sandbox: a separated environment for work.
- Telemetry: usage data collection - Hermes Agent sends none.
- Backup: a copy of data for restoring (~/.hermes/ for the agent, the whole site for a website).
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(12)
    stranka = najdi(12)
    assert stranka and stranka["nazev"] == "Slovníček pojmů"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Slovníček pojmů — aby bylo jasné, co které slovo znamená",
        "Lidsky vysvětlené pojmy kolem Hermes Agenta: agent, model, klíč, token, kontext, nástroj, skill, napojení, brána, pískoviště a další.",
        OBRAZEK, "Wiki · Začínáme", "Slovníček pojmů",
        "Dvacet šest slov, která se kolem agenta používají — bez zkratek a bez programátorské hantýrky.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Slovníček pojmů — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Glossary — so every word makes sense",
        "Plain-language explanations of the terms around Hermes Agent: agent, model, key, token, context, tool, skill, connection, gateway, sandbox and more.",
        OBRAZEK, "Wiki · Start here", "Glossary",
        "Twenty-six words used around the agent — no jargon and no acronyms.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Glossary — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
