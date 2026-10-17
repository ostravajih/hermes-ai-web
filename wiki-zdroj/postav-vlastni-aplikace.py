#!/usr/bin/env python3
"""Postaví stránku wiki „Vlastní aplikace přes MCP" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/guides-use-mcp-with-hermes.md (kdy MCP ano/ne, myšlenkový model),
reference-mcp-config-reference.md (tvary konfigurace: command/url, tools.include/exclude, timeouty,
lazy, ssl_verify, headers) a user-guide-features-mcp.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes"
OBRAZEK = "wiki-vlastni-aplikace"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔌</span><div><strong>MCP se nejčastěji pokazí dvěma způsoby: agent dostane celý nástrojový povrch firmy najednou,
nebo se server přidá tam, kde by stačil obyčejný HTTP požadavek.</strong>
Dobré napojení není „připojit všechno“, ale „připojit to pravé s co nejmenší plochou“ —
proto se v konfiguraci filtrují nástroje a nastavují časové limity.</div></div>

<h2>Kdy MCP dává smysl</h2>
<table class="wiki-tabulka">
<tr><th>Použijte MCP</th><th>Nepoužívejte MCP</th></tr>
<tr><td>Nástroj už existuje v MCP podobě a nechcete psát vlastní</td><td>Stačí zabudovaný nástroj Hermese (čtení souborů, terminál, web)</td></tr>
<tr><td>Potřebujete čistou vrstvu k firemnímu systému, databázi nebo internímu API</td><td>Server vystavuje obrovskou plochu nebezpečných nástrojů a nemáte čas ji filtrovat</td></tr>
<tr><td>Chcete jemně řídit, které nástroje jsou vidět</td><td>Jde o jednu úzkou věc a prostý skript by byl jednodušší i bezpečnější</td></tr>
</table>

<h2>Dvě podoby serveru</h2>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml — lokální program (stdio)</span>
mcp_servers:
  moje-aplikace:
    command: "python3"
    args: ["/opt/mcp/moje-aplikace.py"]
    env:
      DATABAZE_URL: "${DATABASE_URL}"        <span class="c"># hodnota z prostředí, ne natvrdo</span>
    enabled: true
    timeout: 120
    tools:
      exclude: ["smazat_vse"]                <span class="c"># tohle agentovi nedávejte</span></div>
<div class="code-block"><span class="c"># vzdálený server přes HTTP</span>
mcp_servers:
  firemni-api:
    url: "https://api.firma.cz/mcp"
    headers:
      Authorization: "Bearer ${FIRMA_TOKEN}"   <span class="c"># z .env, nikdy do gitu</span>
    ssl_verify: true
    connect_timeout: 60
    tools:
      include: ["hledej_zakaznika", "vytvor_fakturu"]</div>
<table class="wiki-tabulka">
<tr><th>Klíč</th><th>K čemu</th></tr>
<tr><td><code>tools.include</code> / <code>tools.exclude</code></td><td>Které nástroje agent uvidí. Začněte úzkým výběrem a rozšiřujte</td></tr>
<tr><td><code>timeout</code>, <code>connect_timeout</code></td><td>Kolik sekund čekat na odpověď a na spojení</td></tr>
<tr><td><code>lazy: true</code></td><td>Server se spustí až při prvním volání — start Hermese je rychlejší</td></tr>
<tr><td><code>ssl_verify</code></td><td>Ověřování TLS; cesta k vlastnímu CA, když máte interní certifikát</td></tr>
<tr><td><code>transport: sse</code></td><td>Když server mluví starším SSE protokolem místo Streamable HTTP</td></tr>
</table>

<h2>Postup krok za krokem</h2>
<div class="code-block">1) server spustit samostatně a ověřit, že odpovídá (bez Hermese)
2) vložit konfiguraci do ~/.hermes/config.yaml
3) hermes mcp list                  # co Hermes vidí
4) zkusit jeden nástroj na neškodném dotazu („najdi zákazníka 123“)
5) teprve potom pustit do pravidelné úlohy nebo do komunity</div>
<p>Bod 1 je důležitý: když server nefunguje sám, v Hermesu to vypadá jako chyba agenta a hledá se
na špatném místě.</p>

<h2>Na co si dát pozor</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Agent je najednou „hloupější“ nebo dražší</td><td>Server přidal desítky nástrojů a zaplavil kontext — filtrujte přes <code>tools.include</code></td></tr>
<tr><td>Tajemství v konfiguraci</td><td>Pište <code>${PROMENNA}</code> a hodnotu držte v <code>.env</code> nebo v trezoru</td></tr>
<tr><td>Server občas „zmizí“</td><td>Zvyšte <code>timeout</code> nebo <code>keepalive_interval</code>; u vzdáleného zkontrolujte <code>ssl_verify</code></td></tr>
<tr><td>Nebezpečný nástroj omylem dostupný</td><td>Přidejte ho do <code>tools.exclude</code> dřív, než se něco stane</td></tr>
<tr><td>Server se načítá pomalu</td><td><code>lazy: true</code> — nástroje se registrují z uloženého schématu</td></tr>
</table>

<h2>Jak to máme u nás</h2>
<table class="wiki-tabulka">
<tr><th>Napojení</th><th>Zkušenost</th></tr>
<tr><td>Databáze aplikace</td><td>Skvělé na čtení a rychlé dotazy; zápisy pouštíme jen po potvrzení</td></tr>
<tr><td>Monitoring chyb</td><td>Pomáhá hlavně správná oblast serveru (<code>de.sentry.io</code>) — se špatnou adresou to vypadá jako výpadek</td></tr>
<tr><td>Dokumentace knihoven</td><td>Užitečné, ale jen pro konkrétní knihovnu; globální „vše o všem“ agenta zpomaluje</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/mcp-nastroje/"><strong>MCP nástroje</strong><span>Základy a první server</span></a>
<a href="/wiki/funkce/nastroje/"><strong>Nástroje a toolsety</strong><span>Co agent umí bez MCP</span></a>
<a href="/wiki/integrace/spravci-hesel/"><strong>Správci hesel</strong><span>Kam s tokeny pro server</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>MCP v praxi (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Kdy MCP
Ano: hotový MCP nástroj, čistá vrstva k firemnímu systému/DB, jemné řízení viditelných nástrojů.
Ne: stačí zabudovaný nástroj; server vystavuje obrovskou nebezpečnou plochu; jedna úzká věc = prostý skript.

## Konfigurace (~/.hermes/config.yaml)
mcp_servers:
  nazev:
    command/args/env        # stdio
    url/headers             # HTTP (Authorization: "Bearer ${TOKEN}")
    ssl_verify: true|false|cesta k CA
    enabled, timeout, connect_timeout, keepalive_interval, lazy, transport: sse
    tools: {include: [...], exclude: [...], resources: true, prompts: true}

## Postup
1) server spustit samostatně · 2) config.yaml · 3) hermes mcp list · 4) vyzkoušet jeden nástroj
· 5) teprve pak cron/komunita. Když server nefunguje sám, v Hermesu to vypadá jako chyba agenta.

## Pozor
Mnoho nástrojů = dražší a hloupější agent -> tools.include/exclude · tajemství přes ${PROMENNA}, hodnota
v .env/trezoru · timeout/keepalive při výpadcích · nebezpečné nástroje do exclude · lazy: true pro rychlý start.

## U nás
DB aplikace: čtení ano, zápisy po potvrzení. Sentry: správná regionUrl (de.sentry.io). Dokumentace
knihoven jen konkrétní, ne „vše o všem“.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔌</span><div><strong>MCP fails in two typical ways: the agent is handed a company's entire tool surface at once,
or a server is added where a plain HTTP request would do.</strong>
Good integration is not “connect everything” but “connect the right thing with the smallest useful
surface” — which is why tools get filtered and timeouts set in the configuration.</div></div>

<h2>When MCP makes sense</h2>
<table class="wiki-tabulka">
<tr><th>Use MCP</th><th>Do not use MCP</th></tr>
<tr><td>A tool already exists in MCP form and you do not want to build one</td><td>A built-in Hermes tool already does the job (files, terminal, web)</td></tr>
<tr><td>You need a clean layer onto a company system, database or internal API</td><td>The server exposes a huge surface of dangerous tools you have no time to filter</td></tr>
<tr><td>You want fine-grained control over which tools are visible</td><td>It is one narrow thing and a small script would be simpler and safer</td></tr>
</table>

<h2>Two shapes of a server</h2>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml — local program (stdio)</span>
mcp_servers:
  my-app:
    command: "python3"
    args: ["/opt/mcp/my-app.py"]
    env:
      DATABASE_URL: "${DATABASE_URL}"        <span class="c"># value from the environment, not hardcoded</span>
    enabled: true
    timeout: 120
    tools:
      exclude: ["delete_everything"]         <span class="c"># do not hand this to the agent</span></div>
<div class="code-block"><span class="c"># a remote server over HTTP</span>
mcp_servers:
  company-api:
    url: "https://api.company.com/mcp"
    headers:
      Authorization: "Bearer ${COMPANY_TOKEN}"   <span class="c"># from .env, never in git</span>
    ssl_verify: true
    connect_timeout: 60
    tools:
      include: ["find_customer", "create_invoice"]</div>
<table class="wiki-tabulka">
<tr><th>Key</th><th>Purpose</th></tr>
<tr><td><code>tools.include</code> / <code>tools.exclude</code></td><td>Which tools the agent can see. Start narrow and widen</td></tr>
<tr><td><code>timeout</code>, <code>connect_timeout</code></td><td>How long to wait for an answer and for a connection</td></tr>
<tr><td><code>lazy: true</code></td><td>The server starts on the first tool call — Hermes boots faster</td></tr>
<tr><td><code>ssl_verify</code></td><td>TLS verification; a path to your own CA for internal certificates</td></tr>
<tr><td><code>transport: sse</code></td><td>When the server speaks the older SSE protocol instead of Streamable HTTP</td></tr>
</table>

<h2>Step by step</h2>
<div class="code-block">1) run the server on its own and confirm it answers (without Hermes)
2) add the configuration to ~/.hermes/config.yaml
3) hermes mcp list                  # what Hermes sees
4) try one tool on a harmless query ("find customer 123")
5) only then wire it into a scheduled job or a community</div>
<p>Step 1 matters: if the server does not work alone, inside Hermes it looks like an agent bug and you
hunt in the wrong place.</p>

<h2>Things to watch</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>The agent suddenly got “dumber” or more expensive</td><td>The server added dozens of tools and flooded the context — filter with <code>tools.include</code></td></tr>
<tr><td>Secrets in the configuration</td><td>Write <code>${VARIABLE}</code> and keep the value in <code>.env</code> or a vault</td></tr>
<tr><td>The server sometimes “disappears”</td><td>Raise <code>timeout</code> or <code>keepalive_interval</code>; for remote servers check <code>ssl_verify</code></td></tr>
<tr><td>A dangerous tool is accidentally available</td><td>Put it in <code>tools.exclude</code> before something happens</td></tr>
<tr><td>The server slows startup</td><td><code>lazy: true</code> — tools are registered from the cached schema</td></tr>
</table>

<h2>How we do it</h2>
<table class="wiki-tabulka">
<tr><th>Integration</th><th>Experience</th></tr>
<tr><td>The application database</td><td>Great for reading and quick queries; writes only with confirmation</td></tr>
<tr><td>Error monitoring</td><td>Mostly about the right region (<code>de.sentry.io</code>) — the wrong address looks like an outage</td></tr>
<tr><td>Library documentation</td><td>Useful per library; a global “everything about everything” slows the agent down</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/mcp-tools/"><strong>MCP tools</strong><span>The basics and your first server</span></a>
<a href="/en/wiki/features/tools/"><strong>Tools and toolsets</strong><span>What the agent can do without MCP</span></a>
<a href="/en/wiki/integrations/password-managers/"><strong>Password managers</strong><span>Where server tokens belong</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes" target="_blank" rel="noopener"><strong>Official documentation</strong><span>MCP in practice</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## When MCP
Yes: an existing MCP tool, a clean layer onto a company system/DB, fine control over visible tools.
No: a built-in tool already does it; the server exposes a huge dangerous surface; one narrow thing where
a small script is simpler.

## Configuration (~/.hermes/config.yaml)
mcp_servers:
  name:
    command/args/env        # stdio
    url/headers             # HTTP (Authorization: "Bearer ${TOKEN}")
    ssl_verify: true|false|CA path
    enabled, timeout, connect_timeout, keepalive_interval, lazy, transport: sse
    tools: {include: [...], exclude: [...], resources: true, prompts: true}

## Procedure
1) run the server standalone · 2) config.yaml · 3) hermes mcp list · 4) try one tool
· 5) only then cron/community. If the server fails alone, inside Hermes it looks like an agent bug.

## Watch out
Many tools = a slower, pricier agent -> tools.include/exclude · secrets via ${VAR}, value in .env/vault
· timeout/keepalive when calls drop · dangerous tools in exclude · lazy: true for a fast start.

## Our practice
App database: reads yes, writes with confirmation. Sentry: the correct regionUrl (de.sentry.io).
Library docs: per library only, never "everything about everything".
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(39)
    stranka = najdi(39)
    assert stranka and stranka["nazev"] == "Vlastní aplikace přes MCP"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Vlastní aplikace přes MCP — napojení bez velkého povrchu",
        "Kdy má MCP smysl a kdy ne, jak vypadá konfigurace pro lokální i vzdálený server, filtrování nástrojů, časové limity a jak napojení otestovat.",
        OBRAZEK, "Wiki · Integrace", "Vlastní aplikace přes MCP",
        "MCP se nejčastěji pokazí dvěma způsoby: agent dostane celý nástrojový povrch najednou, nebo se server přidá tam, kde stačil HTTP požadavek.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Vlastní aplikace přes MCP (česká wiki)", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Your app via MCP — integration without a huge surface",
        "When MCP makes sense and when it does not, what the configuration looks like for a local and a remote server, tool filtering, timeouts and how to test the integration.",
        OBRAZEK, "Wiki · Integrations", "Your app via MCP",
        "MCP fails in two typical ways: the agent is handed an entire tool surface at once, or a server is added where an HTTP request would do.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Your app via MCP (community wiki)", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
