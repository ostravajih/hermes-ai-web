#!/usr/bin/env python3
"""Postaví stránku wiki „Pluginy" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-plugins.md (struktura pluginu, co vše umí,
opt-in přes plugins.enabled, časové limity, projektové pluginy), user-guide-features-plugin-catalog.md
(katalog, pinovaný SHA, tiery, instalace jménem), user-guide-features-built-in-plugins.md
(vestavěné pluginy a jejich opt-in).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins"
OBRAZEK = "wiki-pluginy"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🧩</span><div><strong>Plugin je cizí kód, který běží uvnitř agenta — proto se sám od sebe nespustí.</strong>
Hermes pluginy najde a ukáže, ale nic, co přidává nástroje nebo se věší na události, se nenačte,
dokud ho výslovně nepovolíte. To je celý bezpečnostní model a stojí za to ho znát dřív, než něco
nainstalujete.</div></div>

<h2>Co plugin je</h2>
<p>Obyčejná složka v <code>~/.hermes/plugins/</code> s manifestem a kusem Pythonu:</p>
<div class="code-block">~/.hermes/plugins/muj-plugin/
├── plugin.yaml      <span class="c"># název, verze, popis</span>
├── __init__.py      <span class="c"># register(ctx) — co plugin přidá</span>
├── schemas.py       <span class="c"># co vidí model (schémata nástrojů)</span>
└── tools.py         <span class="c"># co se opravdu spustí</span></div>
<p>Po startu se nástroje z pluginu objeví vedle vestavěných a model je může hned volat. Nejmenší
funkční plugin má dva soubory — <code>plugin.yaml</code> a <code>__init__.py</code> s funkcí
<code>register(ctx)</code>.</p>

<h2>Co všechno plugin umí</h2>
<table class="wiki-tabulka">
<tr><th>Schopnost</th><th>Příklad použití</th></tr>
<tr><td>Přidat nástroje</td><td>Vlastní API vaší firmy jako nástroj, který model volá</td></tr>
<tr><td>Věšet se na události (hooky)</td><td>Logovat každé volání nástroje, upozornit před spuštěním příkazu</td></tr>
<tr><td>Přidat lomítkové příkazy</td><td><code>/muj-prikaz</code> v chatu i v bráně</td></tr>
<tr><td>Přidat příkazy do terminálu</td><td><code>hermes muj-plugin neco</code></td></tr>
<tr><td>Přibalené skilly</td><td>Plugin si nese vlastní skilly jako <code>plugin:skill</code></td></tr>
<tr><td>Platforma pro zprávy</td><td>Nová chatovací síť vedle Telegramu a Discordu</td></tr>
<tr><td>Backend pro obrázky, video, terminál, paměť</td><td>Jiný model obrázků nebo úložiště paměti</td></tr>
<tr><td>Způsob schvalování</td><td>Potvrzení nebezpečných kroků jinam než do chatu (např. do jiné aplikace)</td></tr>
</table>

<h2>Povolení: nic se nespustí samo</h2>
<p>Plugin se po vložení do složky objeví v přehledu, ale jeho nástroje a hooky se nenačtou, dokud
jeho název nepřidáte do <code>plugins.enabled</code> v <code>config.yaml</code>:</p>
<div class="code-block">plugins:
  enabled:
    - muj-plugin
  disabled:          <span class="c"># volitelný seznam zakázaných — při konfliktu vždy vyhraje</span>
    - hlučný-plugin</div>
<div class="code-block">hermes plugins                    <span class="c"># přehled a přepínání (mezerou zaškrtnete)</span>
hermes plugins enable muj-plugin
hermes plugins disable muj-plugin</div>
<p class="note"><strong>Pozor na výjimku:</strong> hooky brány ve <code>~/.hermes/hooks/&lt;název&gt;/</code>
nejsou pluginy a allow-list je neřídí — spouští se pouhým položením souborů na to místo. Kdo tam
něco dá, tomu to poběží při každém startu.</p>

<h2>Katalog: instalace jménem</h2>
<p>Pro ručně prohlédnuté pluginy existuje katalog. Instalace jménem stáhne <strong>přesně ten commit,
který někdo zkontroloval</strong> (pinovaný SHA), ne špičku větve:</p>
<div class="code-block">hermes plugins install <span class="c">&lt;název-z-katalogu&gt;</span>
hermes plugins enable <span class="c">&lt;název&gt;</span>      <span class="c"># instalace sama plugin nezapne</span></div>
<table class="wiki-tabulka">
<tr><th>Údaj v katalogu</th><th>Co znamená</th></tr>
<tr><td><code>tier</code></td><td><code>official</code> (spravuje NousResearch) nebo <code>community</code></td></tr>
<tr><td><code>sha</code></td><td>Přesný 40znakový commit, který prošel revizí</td></tr>
<tr><td><code>capabilities</code></td><td>Jaké nástroje, hooky a proměnné prostředí plugin deklaruje</td></tr>
<tr><td><code>requires_hermes</code></td><td>Minimální verze Hermese, kterou plugin potřebuje</td></tr>
</table>
<p>Vestavěné pluginy, které Hermes vozí s sebou (například <em>disk-cleanup</em>, <em>security-guidance</em>,
<em>google_meet</em>, <em>hermes-achievements</em>), jsou <strong>také opt-in</strong> — zapínají se stejně
jako ostatní. Důvod je jednoduchý: aby po aktualizaci někdo nepřišel o nástroje, které nikdy nechtěl.</p>

<h2>Časové limity, které se hodí vědět</h2>
<table class="wiki-tabulka">
<tr><th>Nastavení</th><th>Výchozí</th><th>K čemu</th></tr>
<tr><td><code>clone_timeout_seconds</code></td><td>300 s</td><td>Kolik může trvat stažení pluginu z gitu</td></tr>
<tr><td><code>load_timeout_seconds</code></td><td>10 s</td><td>Kolik může trvat načtení jednoho pluginu; pomalejší se přeskočí s důvodem</td></tr>
<tr><td><code>hook_callback_timeout</code></td><td>30 s</td><td>Limit pro Python hooky; hook před voláním nástroje při vypršení nástroj <strong>zablokuje</strong></td></tr>
</table>

<h2>Plugin, nebo MCP server?</h2>
<table class="wiki-tabulka">
<tr><th></th><th>Plugin</th><th>MCP server</th></tr>
<tr><td>Kde běží</td><td>Uvnitř procesu agenta</td><td>Samostatný proces, agent se k němu připojuje</td></tr>
<tr><td>Umí zasahovat do agenta</td><td>Ano — hooky, schvalování, paměť, platformy</td><td>Ne — jen nabízí nástroje</td></tr>
<tr><td>Vhodné pro</td><td>Změnu chování agenta, napojení interních částí</td><td>Cizí služby a API, která mají vlastní život</td></tr>
<tr><td>Riziko</td><td>Větší — kód běží ve stejném procesu</td><td>Menší — izolovaný proces s vlastními právy</td></tr>
</table>
<p class="note">V našem provozu platí: <strong>na cizí služby MCP, na zásahy do agenta plugin.</strong>
Externí nástroje (vyhledávání, prohlížeč, dokumentace) máme jako MCP servery, protože se dají
restartovat a omezit zvlášť.</p>

<h2>Na co si dát pozor</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Plugin po <code>hermes update</code> mlčí</td><td>Zkontrolujte <code>/plugins</code> a log startu — plugin mohl narazit na <code>load_timeout_seconds</code> nebo na novou verzi</td></tr>
<tr><td>Projekt má vlastní <code>./.hermes/plugins/</code></td><td>Projektové pluginy jsou vypnuté; zapínají se jen pro důvěryhodné repozitáře přes <code>HERMES_ENABLE_PROJECT_PLUGINS=true</code></td></tr>
<tr><td>Plugin něco blokuje</td><td>Hook <code>pre_tool_call</code> může nástroj zakázat — hledejte ho v pluginu, ne v oprávněních</td></tr>
<tr><td>Chcete plugin vyzkoušet bez rizika</td><td>Založte nový profil a zapněte ho tam; produkce zůstane nedotčená (viz stránka o profilech)</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/funkce/nastroje/"><strong>Nástroje a toolsety</strong><span>Co agent umí a jak to ověřit</span></a>
<a href="/wiki/zaciname/mcp-nastroje/"><strong>MCP nástroje</strong><span>Cizí služby jako nástroje agenta</span></a>
<a href="/wiki/zaciname/skilly/"><strong>Skilly</strong><span>Návody, které agent načte, když je potřebuje</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Pluginy, hooky a katalog do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co plugin je
Složka v ~/.hermes/plugins/ s plugin.yaml + __init__.py, kde register(ctx) registruje nástroje/hooky.
Typicky: plugin.yaml, __init__.py, schemas.py (co vidí model), tools.py (co se spustí).
Po startu jsou nástroje vedle vestavěných.

## Co umí
Nástroje · hooky (např. post_tool_call) · lomítkové příkazy · CLI příkazy (hermes <plugin> <cmd>) ·
přibalené skilly (plugin:skill) · platformu pro zprávy · backend pro obrázky/video/terminál/paměť ·
způsob schvalování · dispatch nástrojů z příkazů.

## Opt-in
Discovery plugin najde, ale nástroje a hooky se nenačtou, dokud název není v plugins.enabled (config.yaml).
disabled vyhrává při konfliktu. hermes plugins / enable / disable.
POZOR: hooky brány ~/.hermes/hooks/<název>/ nejsou pluginy a allow-list je neřídí (spustí se položením souborů).

## Katalog
hermes plugins install <název> stáhne pinovaný SHA (40 znaků, revidovaný commit), pak zvlášť enable.
Položky: tier (official/community), sha, capabilities, requires_hermes, subdir. Vestavěné pluginy jsou také opt-in.

## Limity (config.yaml)
clone_timeout_seconds 300 · load_timeout_seconds 10 (pomalejší plugin se přeskočí) ·
hook_callback_timeout 30 (pre_tool_call při vypršení nástroj zablokuje).

## Plugin vs MCP
Plugin běží v procesu agenta, umí hooky/schvalování/platformy -> větší riziko; MCP je samostatný proces s nástroji.
U nás: cizí služby přes MCP, zásahy do agenta pluginem.

## Pozor
Po update zkontrolovat /plugins a log (load timeout). Projektové pluginy vypnuté (HERMES_ENABLE_PROJECT_PLUGINS=true).
Blokovaný nástroj = hook pre_tool_call, ne oprávnění. Nový plugin zkoušet v novém profilu.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🧩</span><div><strong>A plugin is third-party code running inside the agent — which is why it never starts by itself.</strong>
Hermes discovers and lists plugins, but nothing that adds tools or hooks loads until you explicitly
allow it. That is the whole security model, and it is worth knowing before you install anything.</div></div>

<h2>What a plugin is</h2>
<p>An ordinary folder in <code>~/.hermes/plugins/</code> with a manifest and some Python:</p>
<div class="code-block">~/.hermes/plugins/my-plugin/
├── plugin.yaml      <span class="c"># name, version, description</span>
├── __init__.py      <span class="c"># register(ctx) — what the plugin adds</span>
├── schemas.py       <span class="c"># what the model sees (tool schemas)</span>
└── tools.py         <span class="c"># what actually runs</span></div>
<p>After startup the plugin's tools appear next to the built-in ones and the model can call them right
away. The smallest working plugin is two files — <code>plugin.yaml</code> and <code>__init__.py</code>
with a <code>register(ctx)</code> function.</p>

<h2>What a plugin can do</h2>
<table class="wiki-tabulka">
<tr><th>Capability</th><th>Example use</th></tr>
<tr><td>Add tools</td><td>Your company's API as a tool the model can call</td></tr>
<tr><td>Hook into events</td><td>Log every tool call, warn before a command runs</td></tr>
<tr><td>Add slash commands</td><td><code>/my-command</code> in chat and in the gateway</td></tr>
<tr><td>Add CLI commands</td><td><code>hermes my-plugin something</code></td></tr>
<tr><td>Bundle skills</td><td>The plugin ships its own skills as <code>plugin:skill</code></td></tr>
<tr><td>Add a messaging platform</td><td>A new chat network beside Telegram and Discord</td></tr>
<tr><td>Image, video, terminal or memory backend</td><td>A different image model or memory store</td></tr>
<tr><td>Approval transport</td><td>Dangerous-step confirmations delivered somewhere other than chat</td></tr>
</table>

<h2>Permission: nothing runs on its own</h2>
<p>A plugin shows up in the listing once it is on disk, but its tools and hooks do not load until you
add its name to <code>plugins.enabled</code> in <code>config.yaml</code>:</p>
<div class="code-block">plugins:
  enabled:
    - my-plugin
  disabled:          <span class="c"># optional deny-list — always wins on conflict</span>
    - noisy-plugin</div>
<div class="code-block">hermes plugins                    <span class="c"># overview and toggles (space to check)</span>
hermes plugins enable my-plugin
hermes plugins disable my-plugin</div>
<p class="note"><strong>Watch the exception:</strong> gateway hooks in <code>~/.hermes/hooks/&lt;name&gt;/</code>
are not plugins and are not gated by the allow-list — they run simply by being placed there. Whoever
puts files there gets them executed on every start.</p>

<h2>Catalog: install by name</h2>
<p>Human-reviewed plugins live in a catalog. Installing by name checks out <strong>exactly the commit
someone reviewed</strong> (a pinned SHA), not a branch tip:</p>
<div class="code-block">hermes plugins install <span class="c">&lt;catalog-name&gt;</span>
hermes plugins enable <span class="c">&lt;name&gt;</span>      <span class="c"># installing does not enable it</span></div>
<table class="wiki-tabulka">
<tr><th>Catalog field</th><th>What it means</th></tr>
<tr><td><code>tier</code></td><td><code>official</code> (maintained by NousResearch) or <code>community</code></td></tr>
<tr><td><code>sha</code></td><td>The exact 40-hex commit that was reviewed</td></tr>
<tr><td><code>capabilities</code></td><td>Which tools, hooks and environment variables it declares</td></tr>
<tr><td><code>requires_hermes</code></td><td>Minimum Hermes version the plugin needs</td></tr>
</table>
<p>Bundled plugins that ship with Hermes (for example <em>disk-cleanup</em>, <em>security-guidance</em>,
<em>google_meet</em>, <em>hermes-achievements</em>) are <strong>opt-in as well</strong> — enabled the same
way as any other. The reason is simple: an update must not silently hand you tools you never asked for.</p>

<h2>Timeouts worth knowing</h2>
<table class="wiki-tabulka">
<tr><th>Setting</th><th>Default</th><th>Purpose</th></tr>
<tr><td><code>clone_timeout_seconds</code></td><td>300 s</td><td>How long a git fetch of a plugin may take</td></tr>
<tr><td><code>load_timeout_seconds</code></td><td>10 s</td><td>Load limit per plugin; slower ones are skipped with a reason</td></tr>
<tr><td><code>hook_callback_timeout</code></td><td>30 s</td><td>Limit for Python hooks; a timed-out pre-tool hook <strong>blocks</strong> the tool</td></tr>
</table>

<h2>Plugin or MCP server?</h2>
<table class="wiki-tabulka">
<tr><th></th><th>Plugin</th><th>MCP server</th></tr>
<tr><td>Runs</td><td>Inside the agent process</td><td>A separate process the agent connects to</td></tr>
<tr><td>Can touch the agent</td><td>Yes — hooks, approvals, memory, platforms</td><td>No — it offers tools only</td></tr>
<tr><td>Best for</td><td>Changing agent behaviour, wiring internal parts</td><td>Third-party services and APIs with their own lifecycle</td></tr>
<tr><td>Risk</td><td>Higher — code shares the process</td><td>Lower — isolated process with its own rights</td></tr>
</table>
<p class="note">Our rule of thumb: <strong>MCP for external services, a plugin for changing the agent.</strong>
External tools (search, browser, docs) run as MCP servers because they can be restarted and limited separately.</p>

<h2>Things to watch</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>A plugin goes quiet after <code>hermes update</code></td><td>Check <code>/plugins</code> and the startup log — it may have hit <code>load_timeout_seconds</code> or a version change</td></tr>
<tr><td>A project ships its own <code>./.hermes/plugins/</code></td><td>Project plugins are off; enable them only for trusted repos with <code>HERMES_ENABLE_PROJECT_PLUGINS=true</code></td></tr>
<tr><td>A plugin blocks something</td><td>A <code>pre_tool_call</code> hook can deny a tool — look in the plugin, not in permissions</td></tr>
<tr><td>You want to try a plugin safely</td><td>Create a new profile and enable it there; production stays untouched (see the profiles page)</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/features/tools/"><strong>Tools and toolsets</strong><span>What the agent can do and how to check it</span></a>
<a href="/en/wiki/getting-started/mcp-tools/"><strong>MCP tools</strong><span>Third-party services as agent tools</span></a>
<a href="/en/wiki/getting-started/skills/"><strong>Skills</strong><span>Instructions the agent loads when needed</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Plugins, hooks and the catalog in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What a plugin is
A folder in ~/.hermes/plugins/ with plugin.yaml + __init__.py whose register(ctx) registers tools/hooks.
Typical layout: plugin.yaml, __init__.py, schemas.py (model-facing), tools.py (what runs).
After startup its tools sit beside the built-in ones.

## Capabilities
Tools · hooks (e.g. post_tool_call) · slash commands · CLI commands (hermes <plugin> <cmd>) ·
bundled skills (plugin:skill) · messaging platforms · image/video/terminal/memory backends ·
approval transports · dispatching tools from commands.

## Opt-in
Discovery lists a plugin, but tools and hooks load only when the name is in plugins.enabled (config.yaml).
disabled wins on conflict. hermes plugins / enable / disable.
NOTE: gateway hooks in ~/.hermes/hooks/<name>/ are not plugins and are not gated — placing files there runs them.

## Catalog
hermes plugins install <name> checks out the pinned SHA (40-hex reviewed commit); enable separately.
Fields: tier (official/community), sha, capabilities, requires_hermes, subdir. Bundled plugins are opt-in too.

## Timeouts (config.yaml)
clone_timeout_seconds 300 · load_timeout_seconds 10 (slower plugins skipped) ·
hook_callback_timeout 30 (a timed-out pre_tool_call hook blocks the tool).

## Plugin vs MCP
A plugin runs in the agent process and can hook/approve/platform -> higher risk; MCP is a separate process
offering tools. Our rule: external services via MCP, agent behaviour via plugins.

## Watch out
After an update check /plugins and the log (load timeouts). Project plugins are off
(HERMES_ENABLE_PROJECT_PLUGINS=true). A blocked tool means a pre_tool_call hook, not permissions.
Try new plugins in a fresh profile.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(26)
    stranka = najdi(26)
    assert stranka and stranka["nazev"] == "Pluginy"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Pluginy — vlastní nástroje a hooky pro Hermes Agenta",
        "Jak vypadá plugin, co všechno umí, proč se nespustí bez povolení, jak ho nainstalovat z katalogu a kdy je lepší sáhnout po MCP serveru.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Pluginy",
        "Plugin je cizí kód uvnitř agenta — proto se sám nespustí. Co umí, jak ho povolit a jak se liší od MCP serveru.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Pluginy — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Plugins — custom tools and hooks for Hermes Agent",
        "What a plugin looks like, what it can do, why it never runs without permission, how to install one from the catalog and when an MCP server is the better choice.",
        OBRAZEK, "Wiki · Features in depth", "Plugins",
        "A plugin is third-party code inside the agent — which is why it never starts by itself. What it can do, how to allow it and how it differs from an MCP server.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Plugins — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
