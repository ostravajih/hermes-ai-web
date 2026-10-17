#!/usr/bin/env python3
"""Postaví stránku wiki „Import z jiných agentů" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-import-from-other-agents.md (import-agent: co se převezme
z Claude Code a Codex CLI, co nikdy, chování), guides-migrate-from-openclaw.md (claw migrate,
presety, --migrate-secrets, záloha před migrací, konflikty skillů).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents"
OBRAZEK = "wiki-import"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔁</span><div><strong>Přechod není kopírování složky — je to rozhodnutí, co si nechat.</strong>
Hermes převezme z Claude Code, Codex CLI i OpenClaw to, co dává smysl (pravidla, paměť, skilly,
MCP servery), a tajné klíče <strong>záměrně nechá doma</strong>. Vždycky vám ale nejdřív ukáže plán
a teprve pak se ptá, jestli ho má provést.</div></div>

<h2>Ze Claude Code a Codex CLI</h2>
<div class="code-block">hermes import-agent                     <span class="c"># samo najde ~/.claude nebo ~/.codex</span>
hermes import-agent claude-code        <span class="c"># jen Claude Code</span>
hermes import-agent codex              <span class="c"># jen Codex CLI</span>
hermes import-agent claude-code --dry-run              <span class="c"># jen náhled, nic nezapíše</span>
hermes import-agent codex --source /cesta/.codex       <span class="c"># jiné umístění</span>
hermes import-agent claude-code --overwrite --yes      <span class="c"># přepsat konflikty bez dotazů</span></div>

<h2>Co se převezme</h2>
<table class="wiki-tabulka">
<tr><th>V Claude Code</th><th>V Hermesu</th></tr>
<tr><td><code>CLAUDE.md</code> (globální pokyny)</td><td>Záznamy v <code>~/.hermes/memories/MEMORY.md</code></td></tr>
<tr><td><code>permissions.allow</code> (<code>Bash(...)</code>)</td><td><code>command_allowlist</code> v <code>config.yaml</code></td></tr>
<tr><td><code>permissions.deny</code></td><td><code>approvals.deny</code> v <code>config.yaml</code></td></tr>
<tr><td><code>mcpServers</code></td><td><code>mcp_servers</code> v <code>config.yaml</code></td></tr>
<tr><td><code>skills/&lt;název&gt;/</code> (se souborem <code>SKILL.md</code>)</td><td><code>~/.hermes/skills/claude-code-imports/&lt;název&gt;/</code></td></tr>
<tr><td><code>commands/*.md</code> (lomítkové příkazy)</td><td><strong>Nepřevezme</strong> — vypíše je k ručnímu převedení na skilly</td></tr>
</table>
<table class="wiki-tabulka">
<tr><th>V Codex CLI</th><th>V Hermesu</th></tr>
<tr><td><code>AGENTS.md</code> (globální pokyny)</td><td>Záznamy v <code>MEMORY.md</code></td></tr>
<tr><td><code>config.toml</code> → <code>[mcp_servers.*]</code></td><td><code>mcp_servers</code></td></tr>
<tr><td><code>memories/*.md</code></td><td>Záznamy v <code>MEMORY.md</code></td></tr>
<tr><td><code>skills/&lt;název&gt;/</code></td><td><code>~/.hermes/skills/codex-imports/&lt;název&gt;/</code></td></tr>
</table>
<p class="note">Pravidla typu <code>Bash(npm run test:*)</code> se převádějí na vzory (<code>npm run test*</code>).
Pravidla, která se týkají nástrojů specifických pro Claude (např. <code>Read(...)</code>), import
vypíše jako nepřevedená — nemá je na co namapovat.</p>

<h2>Co se nikdy nepřevezme</h2>
<table class="wiki-tabulka">
<tr><th>Co</th><th>Proč</th></tr>
<tr><td>Soubory s přihlášením (<code>~/.claude/.credentials.json</code>, <code>~/.codex/auth.json</code>)</td><td>Import je vůbec nečte</td></tr>
<tr><td>Hodnoty vypadající jako tajemství v MCP serverech</td><td>Proměnné jako <code>*_TOKEN</code>, <code>*_API_KEY</code> a hlavičky <code>Authorization</code> se odstraní a vypíšou, abyste je doplnili vědomě</td></tr>
</table>
<p>Přihlášení k modelům pak nastavíte přes <code>hermes setup</code>, klíče doplníte do
<code>~/.hermes/.env</code>. Je to otrava, ale je to jediný způsob, jak import nemůže omylem vysypat
klíče tam, kde nemají být.</p>

<h2>Jak se to chová</h2>
<table class="wiki-tabulka">
<tr><th>Vlastnost</th><th>Význam</th></tr>
<tr><td>Nejdřív náhled</td><td>Příkaz vždy vypíše plán po položkách; v neinteraktivním režimu skončí u náhledu, dokud nepřidáte <code>--yes</code></td></tr>
<tr><td>Slučuje, nepřepisuje</td><td>Záznamy paměti se odduplikují proti tomu, co už máte; allowlist a denylist se slévají s existujícím nastavením</td></tr>
<tr><td>Konflikty přeskočí</td><td>MCP server nebo skill, který už v Hermesu je, se ohlásí jako konflikt a nechá být (přepíše jen <code>--overwrite</code>)</td></tr>
</table>

<h2>Z OpenClaw</h2>
<div class="code-block">hermes claw migrate                            <span class="c"># náhled, pak potvrzení</span>
hermes claw migrate --dry-run                  <span class="c"># jen náhled</span>
hermes claw migrate --preset full --migrate-secrets --yes   <span class="c"># včetně klíčů, bez dotazů</span></div>
<table class="wiki-tabulka">
<tr><th>Co</th><th>Kam</th></tr>
<tr><td>Osobnost (<code>workspace/SOUL.md</code>)</td><td><code>~/.hermes/SOUL.md</code></td></tr>
<tr><td>Pokyny k pracovní složce (<code>AGENTS.md</code>)</td><td><code>AGENTS.md</code> v cíli (<code>--workspace-target</code>)</td></tr>
<tr><td>Dlouhodobá paměť a profil</td><td><code>memories/MEMORY.md</code> a <code>USER.md</code> (sloučené, odduplikované)</td></tr>
<tr><td>Denní poznámky</td><td>Sloučí se do hlavní paměti</td></tr>
<tr><td>Skilly, MCP servery, nastavení modelů</td><td>Odpovídající části <code>config.yaml</code> a <code>skills/</code></td></tr>
</table>
<table class="wiki-tabulka">
<tr><th>Přepínač</th><th>K čemu</th></tr>
<tr><td><code>--preset full</code> / <code>user-data</code></td><td>Vše nebo jen uživatelská data bez infrastruktury</td></tr>
<tr><td><code>--migrate-secrets</code></td><td>Převzít i API klíče. <strong>Ani <code>full</code> je nebere samo</strong> — musí se říct výslovně</td></tr>
<tr><td><code>--skill-conflict skip|overwrite|rename</code></td><td>Co se stejným jménem skillu (výchozí je přeskočit)</td></tr>
<tr><td><code>--no-backup</code></td><td>Přeskočit zálohu <code>~/.hermes/</code>, která se jinak dělá před zápisem (<code>~/.hermes/backups/pre-migration-*.zip</code>)</td></tr>
</table>
<p class="note">Ta záloha před migrací je vaše záchranná síť a obnovuje se přes <code>hermes import</code>.
Nevypínejte ji, dokud nemáte jistotu, že migrace sedla.</p>

<h2>Na co si dát pozor</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Agent po importu „nezná“ vaše pravidla</td><td>Pokyny z jiného nástroje skončily v paměti, ne v <code>AGENTS.md</code> projektu — pravidla k projektu patří do souboru projektu</td></tr>
<tr><td>Agent toho umí víc, než chcete</td><td>Allowlist z Claude Code může být široký; projděte <code>command_allowlist</code> a uberte</td></tr>
<tr><td>MCP server se nepřipojil</td><td>Byl to konflikt, nebo mu chybí tajemství, které import záměrně odstranil</td></tr>
<tr><td>Chybí pravidelné úlohy</td><td>Cron se migrací nepřenáší — pravidelné úlohy založte znovu v Hermesu</td></tr>
<tr><td>Po měsíci se zdroje rozešly</td><td>Import je jednorázový. Buď ho spusťte znovu, nebo (lépe) přestaňte používat dva agenty na totéž</td></tr>
</table>

<h2>Doporučený postup</h2>
<div class="code-block">1) hermes import-agent --dry-run        <span class="c"># co by se převzalo</span>
2) projít plán a vypnout, co nechci
3) hermes import-agent                 <span class="c"># provést</span>
4) hermes setup                        <span class="c"># přihlášení k modelům</span>
5) doplnit klíče do ~/.hermes/.env
6) zkusit reálný úkol a porovnat se starým agentem</div>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/instalace/"><strong>Instalace na VPS</strong><span>Čistý start, když migrovat nechcete</span></a>
<a href="/wiki/funkce/kontextove-soubory/"><strong>Kontextové soubory</strong><span>Kam patří pravidla, aby je agent četl</span></a>
<a href="/wiki/zaciname/pamet/"><strong>Paměť agenta</strong><span>Co si agent nese mezi sezeními</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Import a migrace do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Import z Claude Code / Codex CLI
hermes import-agent [claude-code|codex] [--dry-run] [--source cesta] [--overwrite --yes]
Bez argumentu samo najde ~/.claude nebo ~/.codex.

Claude Code -> Hermes: CLAUDE.md -> MEMORY.md · permissions.allow (Bash(...)) -> command_allowlist ·
permissions.deny -> approvals.deny · mcpServers -> mcp_servers · skills/<n> -> skills/claude-code-imports/<n> ·
commands/*.md se nepřevezmou (převést na skilly). Bash(npm run test:*) -> npm run test*.
Codex CLI: AGENTS.md a memories/*.md -> MEMORY.md · config.toml [mcp_servers.*] -> mcp_servers · skills -> codex-imports.

## Co se nikdy nepřevezme
Přihlašovací soubory (~/.claude/.credentials.json, ~/.codex/auth.json) se vůbec nečtou; tajemství v MCP
(*_TOKEN, *_API_KEY, Authorization) se odstraní a vypíšou. Přihlášení pak hermes setup, klíče do .env.

## Chování
Vždy náhled první (v neinteraktivním režimu se čeká na --yes) · slučuje, nepřepisuje (dedup paměti) ·
konflikty přeskočí, přepíše jen --overwrite.

## OpenClaw
hermes claw migrate [--dry-run] [--preset full|user-data] [--migrate-secrets] [--overwrite]
[--no-backup] [--source] [--workspace-target] [--skill-conflict skip|overwrite|rename] [--yes]
SOUL.md -> ~/.hermes/SOUL.md · AGENTS.md -> cíl (--workspace-target) · MEMORY.md/USER.md sloučené ·
denní poznámky do hlavní paměti · skilly, MCP a modely do config.yaml a skills/.
--migrate-secrets je nutné i s --preset full. Před zápisem záloha ~/.hermes/backups/pre-migration-*.zip (obnova hermes import).

## Pozor
Pravidla z jiného nástroje skončí v paměti, ne v AGENTS.md projektu · allowlist může být moc široký ·
MCP bez tajemství se nepřipojí · cron se nepřenáší · import je jednorázový.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔁</span><div><strong>Moving over is not copying a folder — it is deciding what to keep.</strong>
Hermes takes what makes sense from Claude Code, Codex CLI and OpenClaw (rules, memory, skills, MCP
servers) and deliberately <strong>leaves credentials behind</strong>. It always shows you the plan
first and only then asks whether to apply it.</div></div>

<h2>From Claude Code and Codex CLI</h2>
<div class="code-block">hermes import-agent                     <span class="c"># auto-detects ~/.claude or ~/.codex</span>
hermes import-agent claude-code        <span class="c"># Claude Code only</span>
hermes import-agent codex              <span class="c"># Codex CLI only</span>
hermes import-agent claude-code --dry-run              <span class="c"># preview only, writes nothing</span>
hermes import-agent codex --source /path/.codex        <span class="c"># custom location</span>
hermes import-agent claude-code --overwrite --yes      <span class="c"># replace conflicts, no prompts</span></div>

<h2>What gets imported</h2>
<table class="wiki-tabulka">
<tr><th>In Claude Code</th><th>In Hermes</th></tr>
<tr><td><code>CLAUDE.md</code> (global instructions)</td><td>Entries in <code>~/.hermes/memories/MEMORY.md</code></td></tr>
<tr><td><code>permissions.allow</code> (<code>Bash(...)</code>)</td><td><code>command_allowlist</code> in <code>config.yaml</code></td></tr>
<tr><td><code>permissions.deny</code></td><td><code>approvals.deny</code> in <code>config.yaml</code></td></tr>
<tr><td><code>mcpServers</code></td><td><code>mcp_servers</code> in <code>config.yaml</code></td></tr>
<tr><td><code>skills/&lt;name&gt;/</code> (with <code>SKILL.md</code>)</td><td><code>~/.hermes/skills/claude-code-imports/&lt;name&gt;/</code></td></tr>
<tr><td><code>commands/*.md</code> (slash commands)</td><td><strong>Not imported</strong> — listed for manual conversion into skills</td></tr>
</table>
<table class="wiki-tabulka">
<tr><th>In Codex CLI</th><th>In Hermes</th></tr>
<tr><td><code>AGENTS.md</code> (global instructions)</td><td>Entries in <code>MEMORY.md</code></td></tr>
<tr><td><code>config.toml</code> → <code>[mcp_servers.*]</code></td><td><code>mcp_servers</code></td></tr>
<tr><td><code>memories/*.md</code></td><td>Entries in <code>MEMORY.md</code></td></tr>
<tr><td><code>skills/&lt;name&gt;/</code></td><td><code>~/.hermes/skills/codex-imports/&lt;name&gt;/</code></td></tr>
</table>
<p class="note">Rules such as <code>Bash(npm run test:*)</code> become globs (<code>npm run test*</code>).
Rules for Claude-specific tools (e.g. <code>Read(...)</code>) are reported as unmapped — there is
nothing to map them onto.</p>

<h2>What is never imported</h2>
<table class="wiki-tabulka">
<tr><th>Item</th><th>Why</th></tr>
<tr><td>Credential files (<code>~/.claude/.credentials.json</code>, <code>~/.codex/auth.json</code>)</td><td>The import never reads them</td></tr>
<tr><td>Secret-looking values in MCP servers</td><td>Variables such as <code>*_TOKEN</code>, <code>*_API_KEY</code> and <code>Authorization</code> headers are stripped and listed so you can re-add them deliberately</td></tr>
</table>
<p>Sign in to providers with <code>hermes setup</code> and add keys to <code>~/.hermes/.env</code>.
It is a chore, but it is the only way an import cannot dump your keys somewhere they do not belong.</p>

<h2>How it behaves</h2>
<table class="wiki-tabulka">
<tr><th>Property</th><th>Meaning</th></tr>
<tr><td>Preview first</td><td>The command always prints a per-item plan; in non-interactive sessions it stops at the preview unless you pass <code>--yes</code></td></tr>
<tr><td>Merges, not replaces</td><td>Memory entries are deduplicated against yours; allow/deny patterns merge with the existing config</td></tr>
<tr><td>Conflicts are skipped</td><td>An MCP server or skill that already exists is reported as a conflict and left alone (only <code>--overwrite</code> replaces)</td></tr>
</table>

<h2>From OpenClaw</h2>
<div class="code-block">hermes claw migrate                            <span class="c"># preview, then confirm</span>
hermes claw migrate --dry-run                  <span class="c"># preview only</span>
hermes claw migrate --preset full --migrate-secrets --yes   <span class="c"># with keys, no prompts</span></div>
<table class="wiki-tabulka">
<tr><th>Item</th><th>Destination</th></tr>
<tr><td>Persona (<code>workspace/SOUL.md</code>)</td><td><code>~/.hermes/SOUL.md</code></td></tr>
<tr><td>Workspace instructions (<code>AGENTS.md</code>)</td><td><code>AGENTS.md</code> at <code>--workspace-target</code></td></tr>
<tr><td>Long-term memory and profile</td><td><code>memories/MEMORY.md</code> and <code>USER.md</code> (merged, deduplicated)</td></tr>
<tr><td>Daily notes</td><td>Merged into main memory</td></tr>
<tr><td>Skills, MCP servers, model settings</td><td>Matching parts of <code>config.yaml</code> and <code>skills/</code></td></tr>
</table>
<table class="wiki-tabulka">
<tr><th>Option</th><th>Purpose</th></tr>
<tr><td><code>--preset full</code> / <code>user-data</code></td><td>Everything, or user data without infrastructure config</td></tr>
<tr><td><code>--migrate-secrets</code></td><td>Include API keys. <strong>Even <code>full</code> does not take them by default</strong> — it must be explicit</td></tr>
<tr><td><code>--skill-conflict skip|overwrite|rename</code></td><td>What to do with a skill of the same name (skip by default)</td></tr>
<tr><td><code>--no-backup</code></td><td>Skip the <code>~/.hermes/</code> snapshot that is otherwise taken before writing (<code>~/.hermes/backups/pre-migration-*.zip</code>)</td></tr>
</table>
<p class="note">That pre-migration backup is your safety net and restores with <code>hermes import</code>.
Do not disable it until you are sure the migration worked.</p>

<h2>Things to watch</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>The agent does not “know” your rules after the import</td><td>Instructions from another tool landed in memory, not in the project's <code>AGENTS.md</code> — project rules belong in the project file</td></tr>
<tr><td>The agent can do more than you want</td><td>A Claude Code allowlist can be broad; review <code>command_allowlist</code> and trim it</td></tr>
<tr><td>An MCP server did not connect</td><td>It was a conflict, or it is missing the secret the import deliberately stripped</td></tr>
<tr><td>Scheduled jobs are missing</td><td>Cron does not migrate — recreate scheduled jobs in Hermes</td></tr>
<tr><td>The two setups drifted apart a month later</td><td>The import is one-shot. Either run it again, or (better) stop using two agents for the same thing</td></tr>
</table>

<h2>Recommended procedure</h2>
<div class="code-block">1) hermes import-agent --dry-run        <span class="c"># what would be taken</span>
2) review the plan and disable what you do not want
3) hermes import-agent                 <span class="c"># apply</span>
4) hermes setup                        <span class="c"># sign in to providers</span>
5) add keys to ~/.hermes/.env
6) run a real task and compare with the old agent</div>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/installation/"><strong>Installation on a VPS</strong><span>A clean start if you prefer not to migrate</span></a>
<a href="/en/wiki/features/context-files/"><strong>Context files</strong><span>Where rules belong so the agent reads them</span></a>
<a href="/en/wiki/getting-started/memory/"><strong>Agent memory</strong><span>What the agent carries between sessions</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Import and migration in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Import from Claude Code / Codex CLI
hermes import-agent [claude-code|codex] [--dry-run] [--source path] [--overwrite --yes]
With no argument it auto-detects ~/.claude or ~/.codex.

Claude Code -> Hermes: CLAUDE.md -> MEMORY.md · permissions.allow (Bash(...)) -> command_allowlist ·
permissions.deny -> approvals.deny · mcpServers -> mcp_servers · skills/<n> -> skills/claude-code-imports/<n> ·
commands/*.md are not imported (convert to skills). Bash(npm run test:*) -> npm run test*.
Codex CLI: AGENTS.md and memories/*.md -> MEMORY.md · config.toml [mcp_servers.*] -> mcp_servers · skills -> codex-imports.

## Never imported
Credential files (~/.claude/.credentials.json, ~/.codex/auth.json) are not read; secrets in MCP
(*_TOKEN, *_API_KEY, Authorization) are stripped and listed. Then hermes setup, keys into .env.

## Behaviour
Preview first (non-interactive stops unless --yes) · merges, not replaces (memory dedup) ·
conflicts skipped, only --overwrite replaces.

## OpenClaw
hermes claw migrate [--dry-run] [--preset full|user-data] [--migrate-secrets] [--overwrite]
[--no-backup] [--source] [--workspace-target] [--skill-conflict skip|overwrite|rename] [--yes]
SOUL.md -> ~/.hermes/SOUL.md · AGENTS.md -> target (--workspace-target) · MEMORY.md/USER.md merged ·
daily notes into main memory · skills, MCP and models into config.yaml and skills/.
--migrate-secrets is required even with --preset full. Pre-write backup ~/.hermes/backups/pre-migration-*.zip (restore with hermes import).

## Watch out
Instructions from another tool land in memory, not the project AGENTS.md · allowlists can be too broad ·
MCP without its secret will not connect · cron does not migrate · the import is one-shot.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(28)
    stranka = najdi(28)
    assert stranka and stranka["nazev"] == "Import z jiných agentů"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Import z jiných agentů — Claude Code, Codex CLI, OpenClaw",
        "Co Hermes převezme z jiného agenta, co záměrně nechá doma, jak si nejdřív prohlédnout plán a na co si dát pozor, aby vám po přechodu nezmizela pravidla.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Import z jiných agentů",
        "Přechod není kopírování složky — je to rozhodnutí, co si nechat. Co se převezme, co ne a jak si to zkontrolovat.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Import z jiných agentů — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Import from other agents — Claude Code, Codex CLI, OpenClaw",
        "What Hermes takes over from another agent, what it deliberately leaves behind, how to preview the plan first and what to watch so your rules do not disappear.",
        OBRAZEK, "Wiki · Features in depth", "Import from other agents",
        "Moving over is not copying a folder — it is deciding what to keep. What comes over, what does not and how to check it.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Import from other agents — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
