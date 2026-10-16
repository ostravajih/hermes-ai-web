#!/usr/bin/env python3
"""Postaví stránku wiki „MCP nástroje" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-mcp.md, guides-use-mcp-with-hermes.md,
reference-mcp-config-reference.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp"
OBRAZEK = "wiki-mcp"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔌</span><div><strong>Řada služeb už má hotové rozhraní pro agenty — agent se k němu jen připojí.</strong>
Říká se tomu MCP a je to způsob, jak agentovi přidat schopnosti, které sám nemá: přístup k vašim
souborům, k projektu na GitHubu, ke svému nástroji pro automatizaci nebo k prohlížeči.
Nepíše se k tomu žádný kód.</div></div>

<h2>Co to je, lidsky</h2>
<p>Agent sám umí pracovat s terminálem, soubory a webem. Kdyby měl umět i všechno ostatní, musel by
mít pro každou službu vlastní řešení — což je pomalé a křehké. MCP je společná dohoda, kterou už
řada služeb nabízí. Agent se tedy připojí k hotovému rozhraní a hned umí to, co nabízí.</p>
<table class="wiki-tabulka">
<tr><th>Přinese vám</th><th>Příklad</th></tr>
<tr><td>Agent vidí do vašich systémů</td><td>Projde soubory v projektu, přečte si dokumentaci, podívá se do databáze</td></tr>
<tr><td>Ovládá nástroje, které už používáte</td><td>Založí kartu v nástroji pro automatizaci, přidá komentář k úkolu, nahraje soubor</td></tr>
<tr><td>Umí se podívat na web jako člověk</td><td>Otevře stránku v prohlížeči a ověří, že opravdu vypadá správně</td></tr>
<tr><td>Dosáhne na chyby a dokumentaci</td><td>Přečte hlášené chyby z vašeho sledování, dohledá aktuální dokumentaci knihovny</td></tr>
</table>

<h2>Dva druhy napojení</h2>
<table class="wiki-tabulka">
<tr><th>Druh</th><th>Jak funguje</th><th>Typicky pro</th></tr>
<tr><td><strong>Místní</strong></td><td>Program se spouští přímo na vašem serveru, agent s ním mluví uvnitř počítače</td><td>Přístup ke složkám, k databázi, k místnímu nástroji</td></tr>
<tr><td><strong>Vzdálené</strong></td><td>Agent se připojuje přes internet k cizí službě; některé chtějí přihlášení</td><td>GitHub, project management, sledování chyb</td></tr>
</table>

<h2>Jak napojení přidat</h2>
<ol class="kroky">
<li><strong>Z katalogu — nejjednodušší cesta.</strong> Pro vybraná napojení existuje katalog,
ze kterého se instalují jedním příkazem:
<div class="code-block"><span class="p">$</span> hermes mcp catalog
<span class="p">$</span> hermes mcp install</div>
U některých napojení se při instalaci vybírá, které nástroje má agent vidět.</li>
<li><strong>Přidáním z adresy nebo příkazu.</strong> Když napojení v katalogu není:
<div class="code-block"><span class="p">$</span> hermes mcp add</div></li>
<li><strong>Zápisem do nastavení.</strong> Ruční cesta pro toho, kdo ví, co dělá — do souboru
<code>~/.hermes/config.yaml</code>:
<div class="code-block">mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projekty"]</div></li>
</ol>
<p>U napojení, která chtějí přihlášení, se použije <code>hermes mcp login</code> — otevře se přihlášení
v prohlížeči, stejně jako u kteréhokoli jiného účtu. Klíče se do nastavení nepíšou natvrdo:
napojení si je bere z prostředí.</p>
<p><strong>Ověření:</strong> <code>hermes mcp test</code> řekne, jestli se napojení podařilo připojit
a jaké nástroje přineslo. Změny se projeví po novém spuštění agenta.</p>

<h2>Bezpečnost: napojení je cizí kód</h2>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⚠️</span><div>Napojení dává agentovi nové schopnosti — a může v podstatě cokoli, co sám umí.
<strong>Berte jen zdroje, kterým věříte</strong> (oficiální katalog, ověření výrobci) a u napojení,
která to nabízejí, <strong>omezte, které nástroje agent uvidí</strong>. Napojení od neznámého zdroje je
jako spustit cizí program s přístupem k vašemu serveru.</div></div>
<table class="wiki-tabulka">
<tr><th>Pojistka</th><th>Co dělá</th></tr>
<tr><td>Oficiální katalog</td><td>Napojení v katalogu prošla kontrolou, takže je bezpečné začít tam</td></tr>
<tr><td>Výběr nástrojů</td><td>U napojení se dá zaškrtnout jen to, co opravdu chcete používat — zbytek agent ani nevidí</td></tr>
<tr><td>Klíče mimo soubor</td><td>Tajné údaje se berou z prostředí, ne z konfigurace, takže se nekopírují do záloh ani do gitu</td></tr>
</table>

<h2>Když to nefunguje</h2>
<table class="wiki-tabulka">
<tr><th>Co se děje</th><th>Příčina a co s tím</th></tr>
<tr><td>Agent nové nástroje nevidí</td><td>Změna se projeví až po novém spuštění agenta. Pak ověřte <code>hermes mcp test</code></td></tr>
<tr><td>Napojení hlásí chybu přihlášení</td><td>Spusťte <code>hermes mcp login</code> a přihlaste se v prohlížeči; pozor, přihlášení má svou platnost</td></tr>
<tr><td>Některý nástroj chybí</td><td>Při instalaci byl vynechán z výběru — <code>hermes mcp configure</code> výběr upraví</td></tr>
<tr><td>Agent se plete mezi nástroji</td><td>Napojení přineslo příliš mnoho nástrojů. Zúžte výběr na ty, které používáte</td></tr>
<tr><td>Nevím, co je připojené</td><td>V rozhovoru se zeptejte; v nastavení je to v sekci <code>mcp_servers</code></td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Začněte katalogem</td><td>Nemusíte nic vymýšlet a víte, že napojení prošlo kontrolou</td></tr>
<tr><td>Přidávejte po jednom</td><td>Když jich zapnete deset naráz, nepoznáte, které zlobí, a agent se v nástrojích ztratí</td></tr>
<tr><td>Zúžte výběr nástrojů</td><td>Méně nástrojů znamená méně zmatků a menší riziko, že agent sáhne po něčem, co jste nechtěli</td></tr>
<tr><td>Co nepoužíváte, odpojte</td><td>Každé napojení je další cizí kód na vašem serveru</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/bezpecnost/"><strong>Bezpečnost</strong><span>Co agent smí a co musí odsouhlasit</span></a>
<a href="/wiki/zaciname/pravidelne-ulohy/"><strong>Pravidelné úlohy</strong><span>Napojení se hodí i úlohám</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>MCP do detailu (anglicky)</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Discord komunity</strong><span>Co si kdo připojil</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co to je
MCP = společná dohoda, přes kterou se agent připojí k hotovému rozhraní služby a získá její schopnosti.
Bez psaní kódu. Např. přístup k souborům, GitHub, n8n, prohlížeč, sledování chyb, dokumentace.

## Dva druhy
- místní: program běží na vašem serveru (složky, databáze, místní nástroje)
- vzdálené: připojení přes internet, některá chtějí přihlášení (GitHub, project management)

## Jak přidat
hermes mcp catalog            # katalog napojení
hermes mcp install            # instalace z katalogu (u některých se vybírá, které nástroje agent uvidí)
hermes mcp add                # přidání z adresy/příkazu
hermes mcp login              # přihlášení u napojení, která ho chtějí
hermes mcp test               # ověření, že se napojení připojilo a jaké nástroje přineslo
hermes mcp configure          # úprava výběru nástrojů
Ručně: ~/.hermes/config.yaml -> mcp_servers: (command/args, nebo HTTP adresa).
Klíče se berou z prostředí, ne z konfigurace. Změny se projeví po novém spuštění agenta.

## Bezpečnost
Napojení je cizí kód a může dělat, co umí -> brát jen důvěryhodné zdroje (oficiální katalog),
u napojení omezit výběr nástrojů. Co nepoužíváte, odpojte.

## Když nefunguje
- agent nástroje nevidí -> projeví se po restartu; hermes mcp test
- chyba přihlášení -> hermes mcp login (přihlášení má platnost)
- chybí nástroj -> byl vynechán z výběru; hermes mcp configure
- agent se plete -> příliš mnoho nástrojů, zúžit výběr
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔌</span><div><strong>Many services already speak a language agents understand — your agent just connects.</strong>
It is called MCP, and it is how you give the agent abilities it does not have on its own: access to your
files, to a GitHub project, to your automation tool or to a browser. No code is written for it.</div></div>

<h2>What it is, in plain words</h2>
<p>On its own the agent works with a terminal, files and the web. Making it handle everything else would
mean a custom solution per service — slow and fragile. MCP is a shared agreement that many services
already offer. The agent connects to that ready-made interface and can immediately do what it offers.</p>
<table class="wiki-tabulka">
<tr><th>What it gives you</th><th>Example</th></tr>
<tr><td>The agent can see into your systems</td><td>Walks through project files, reads documentation, looks into a database</td></tr>
<tr><td>It drives tools you already use</td><td>Creates a card in your automation tool, comments on a task, uploads a file</td></tr>
<tr><td>It can look at the web like a person</td><td>Opens a page in a browser and verifies it really looks right</td></tr>
<tr><td>It reaches errors and documentation</td><td>Reads reported errors from your monitoring, looks up current library docs</td></tr>
</table>

<h2>Two kinds of connections</h2>
<table class="wiki-tabulka">
<tr><th>Kind</th><th>How it works</th><th>Typically for</th></tr>
<tr><td><strong>Local</strong></td><td>A program runs on your own server; the agent talks to it inside the machine</td><td>Access to folders, a database, a local tool</td></tr>
<tr><td><strong>Remote</strong></td><td>The agent connects over the internet to a service; some ask you to sign in</td><td>GitHub, project management, error tracking</td></tr>
</table>

<h2>How to add a connection</h2>
<ol class="kroky">
<li><strong>From the catalog — the easy route.</strong> Selected connections have a catalog and install
with one command:
<div class="code-block"><span class="p">$</span> hermes mcp catalog
<span class="p">$</span> hermes mcp install</div>
For some connections you pick which tools the agent should see.</li>
<li><strong>By adding an address or command.</strong> When a connection is not in the catalog:
<div class="code-block"><span class="p">$</span> hermes mcp add</div></li>
<li><strong>By editing the settings.</strong> The manual route, for when you know what you are doing — in
<code>~/.hermes/config.yaml</code>:
<div class="code-block">mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]</div></li>
</ol>
<p>Connections that require a sign-in use <code>hermes mcp login</code> — you log in through the browser,
just like any other account. Keys are not written into the settings; a connection reads them from the
environment.</p>
<p><strong>Verification:</strong> <code>hermes mcp test</code> tells you whether the connection came up and
which tools it brought. Changes take effect after the agent restarts.</p>

<h2>Safety: a connection is third-party code</h2>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⚠️</span><div>A connection gives the agent new abilities — and it can do essentially anything it is capable of.
<strong>Only use sources you trust</strong> (the official catalog, verified vendors), and for connections that
offer it, <strong>limit which tools the agent can see</strong>. A connection from an unknown source is like
running a stranger's program with access to your server.</div></div>
<table class="wiki-tabulka">
<tr><th>Safeguard</th><th>What it does</th></tr>
<tr><td>The official catalog</td><td>Catalog connections have been reviewed, so it is the safe place to start</td></tr>
<tr><td>Tool selection</td><td>You can tick only what you actually want — the agent never even sees the rest</td></tr>
<tr><td>Keys kept out of the file</td><td>Secrets come from the environment, not from configuration, so they are not copied into backups or git</td></tr>
</table>

<h2>When it does not work</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>Cause and what to do</th></tr>
<tr><td>The agent does not see the new tools</td><td>The change applies after the agent restarts. Then verify with <code>hermes mcp test</code></td></tr>
<tr><td>The connection reports a sign-in error</td><td>Run <code>hermes mcp login</code> and sign in through the browser; note that a sign-in does expire</td></tr>
<tr><td>A particular tool is missing</td><td>It was left out of the tool selection — <code>hermes mcp configure</code> adjusts it</td></tr>
<tr><td>The agent confuses the tools</td><td>The connection brought too many tools. Narrow the selection to the ones you use</td></tr>
<tr><td>I do not know what is connected</td><td>Ask in the conversation; in the settings it is the <code>mcp_servers</code> section</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Start with the catalog</td><td>Nothing to invent, and you know the connection was reviewed</td></tr>
<tr><td>Add them one at a time</td><td>Enabling ten at once hides which one misbehaves and drowns the agent in tools</td></tr>
<tr><td>Narrow the tool selection</td><td>Fewer tools means less confusion and less risk of the agent reaching for something you did not intend</td></tr>
<tr><td>Disconnect what you do not use</td><td>Every connection is more third-party code on your server</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/security/"><strong>Security</strong><span>What the agent may do and what it must ask for</span></a>
<a href="/en/wiki/getting-started/scheduled-tasks/"><strong>Scheduled tasks</strong><span>Connections are useful to jobs too</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp" target="_blank" rel="noopener"><strong>Official documentation</strong><span>MCP in detail</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Community Discord</strong><span>See what others connected</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What it is
MCP = a shared agreement through which the agent connects to a service's ready-made interface and gains
its abilities. No code involved: files, GitHub, n8n, a browser, error tracking, documentation.

## Two kinds
- local: the program runs on your server (folders, database, local tools)
- remote: connected over the internet, some require signing in (GitHub, project management)

## How to add
hermes mcp catalog            # catalog of connections
hermes mcp install            # install from the catalog (tool selection where offered)
hermes mcp add                # add by address or command
hermes mcp login              # sign-in for connections that need it
hermes mcp test               # verify the connection and list the tools it brought
hermes mcp configure          # adjust the tool selection
Manually: ~/.hermes/config.yaml -> mcp_servers: (command/args or an HTTP URL).
Keys come from the environment, never from the config file. Restart to apply.

## Safety
A connection is third-party code and can do anything it is capable of -> trusted sources only (official
catalog), narrow the tool selection, disconnect what you do not use.

## Troubleshooting
- agent does not see the tools -> applies after restart; hermes mcp test
- sign-in error -> hermes mcp login (sign-ins expire)
- a tool is missing -> left out of the selection; hermes mcp configure
- agent confuses tools -> too many tools, narrow the selection
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(8)
    stranka = najdi(8)
    assert stranka and stranka["nazev"] == "MCP nástroje"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "MCP nástroje — jak agentovi přidat další schopnosti",
        "Co je MCP, jak agentovi připojit služby jako GitHub, n8n nebo prohlížeč, jak napojení přidat z katalogu a na co si dát pozor (napojení je cizí kód).",
        OBRAZEK, "Wiki · Začínáme", "MCP nástroje",
        "Hotová rozhraní, ke kterým se agent připojí — a najednou umí pracovat s vašimi systémy, bez psaní kódu.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "MCP nástroje — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "MCP tools — giving the agent more abilities",
        "What MCP is, how to connect services like GitHub, n8n or a browser from the catalog, and what to watch out for.",
        OBRAZEK, "Wiki · Start here", "MCP tools",
        "Ready-made interfaces the agent plugs into — suddenly it works with your systems, with no code written.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "MCP tools — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
