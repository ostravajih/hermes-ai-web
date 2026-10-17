#!/usr/bin/env python3
"""Postaví stránku wiki „Kurátor skillů" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-curator.md (co kurátor je, jak se spouští,
výchozí nastavení, CLI, zálohy a rollback, auditní ledger, pinning, archivace, telemetrie).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/curator"
OBRAZEK = "wiki-kurator"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🗂️</span><div><strong>Kurátor nikdy nemaže. Nejdrsnější, co umí, je archivace — a ta se dá vrátit jedním příkazem.</strong>
Řeší jen jednu nepříjemnou věc: když agent při každém novém problému uloží další skill, za půl roku
máte knihovnu plnou úzkých skoro-duplikátů. Kurátor to udržuje v rozumné míře, ale rozhodnutí
nechává na vás — a do knihovny nesáhne dřív, než si ji stihnete projít.</div></div>

<h2>Co kurátor dělá</h2>
<p>Sleduje u každého skillu, kolikrát byl zobrazený, použitý a upravený, a posouvá ho ve třech
stavech: <strong>aktivní → zastaralý → archivovaný</strong>. Když je zapnutá i slučovací fáze,
jednou za čas pustí krátkou kontrolu na levnějším modelu, která navrhne sloučení nebo opravu.</p>
<table class="wiki-tabulka">
<tr><th>Fáze</th><th>Co dělá</th><th>Stojí peníze?</th></tr>
<tr><td>Automatické přechody</td><td>Skill nepoužitý 14 dní = zastaralý; 30 dní = do archivu</td><td>Ne (běží vždy, když je kurátor zapnutý)</td></tr>
<tr><td>Slučování (LLM)</td><td>Projde skilly, navrhne sloučení přibližných duplikátů a opraví zastaralé texty</td><td>Ano, ale jde poslat na levný model</td></tr>
</table>
<p class="note">Automaticky se spravují jen skilly, které si <strong>vytvořil agent sám</strong>. Skilly
nainstalované z hubu (agentskills.io) jsou mimo hru vždy.</p>

<h2>Kdy se spustí</h2>
<p>Ne podle cronu, ale podle nečinnosti. Hermes se ptá při startu CLI, při údržbě brány a na
časovači Desktopu, jestli platí obojí:</p>
<table class="wiki-tabulka">
<tr><th>Podmínka</th><th>Výchozí hodnota</th></tr>
<tr><td>Od posledního běhu uplynulo</td><td><code>interval_hours</code> = 168 (7 dní)</td></tr>
<tr><td>Agent je dost dlouho nečinný</td><td><code>min_idle_hours</code> = 2 hodiny</td></tr>
</table>
<p><strong>První běh je odložený</strong> o celý interval: na nové instalaci se jen zapíše „teď“ a teprve
za týden proběhne první skutečný průchod. To je schválně — máte čas si knihovnu projít a důležité
skilly připnout.</p>

<h2>Nastavení</h2>
<div class="code-block">curator:
  enabled: true
  interval_hours: 168          <span class="c"># 7 dní</span>
  min_idle_hours: 2
  stale_after_days: 14
  archive_after_days: 30
  consolidate: false           <span class="c"># slučování pomocí LLM — vypnuto</span>
  prune_builtins: false        <span class="c"># archivovat i nepoužité vestavěné skilly</span></div>
<table class="wiki-tabulka">
<tr><th>Klíč</th><th>K čemu</th></tr>
<tr><td><code>consolidate</code></td><td>Zapíná slučovací průchod. Ten jediný přepisuje obsah skillů — a proto si před ním Hermes dělá zálohu</td></tr>
<tr><td><code>prune_builtins</code></td><td>I nepoužité vestavěné skilly se mají archivovat. Volitelné, protože mizející vestavěné skilly vypadají jako rozbitá instalace</td></tr>
<tr><td><code>auxiliary.curator</code></td><td>Který model dělá kontrolu. Nechte <code>auto</code> (hlavní model), nebo sem dejte levný model</td></tr>
</table>
<div class="code-block"><span class="c"># levnější model pro kontrolu (v config.yaml)</span>
auxiliary:
  curator:
    provider: openrouter
    model: google/gemini-3-flash-preview
    timeout: 600</div>

<h2>Příkazy, které se hodí</h2>
<table class="wiki-tabulka">
<tr><th>Příkaz</th><th>Co udělá</th></tr>
<tr><td><code>hermes curator status</code></td><td>Poslední běh, počty, připnuté skilly, nejméně používané</td></tr>
<tr><td><code>hermes curator run --dry-run</code></td><td><strong>Zkuste jako první</strong> — vypíše, co by kurátor udělal, a nic nezmění</td></tr>
<tr><td><code>hermes curator run</code></td><td>Spustí průchod hned (jen archivace, pokud nezapnete slučování)</td></tr>
<tr><td><code>hermes curator pin &lt;skill&gt;</code></td><td>Skill se nikdy automaticky nepřesune ani nezarchivuje</td></tr>
<tr><td><code>hermes curator backup</code> / <code>rollback</code></td><td>Ruční snímek knihovny a návrat k němu</td></tr>
<tr><td><code>hermes curator restore &lt;skill&gt;</code></td><td>Vrátí skill z archivu zpět mezi aktivní</td></tr>
<tr><td><code>hermes curator ledger</code></td><td>Kdo co kdy změnil; <code>rollback &lt;id&gt;</code> vrátí jednu konkrétní změnu</td></tr>
</table>

<h2>Co se nikdy nestane</h2>
<table class="wiki-tabulka">
<tr><th>Obava</th><th>Realita</th></tr>
<tr><td>„Smaže mi moje skilly“</td><td>Nemaže. Archivace přesune skill do <code>~/.hermes/skills/.archive/</code></td></tr>
<tr><td>„Sáhne na skilly z hubu“</td><td>Ne, ty jsou vždy vynechané</td></tr>
<tr><td>„Zarchivuje skill, který používá cron“</td><td>Ne. Skill použitý v jakékoli pravidelné úloze (i pozastavené) se přesouvá jako připnutý</td></tr>
<tr><td>„Zahodí skill, který ještě nikdo nepoužil“</td><td>Ne. Skill s nulovým použitím má lhůtu — nearchivuje se dřív, než je starý jako <code>stale_after_days</code></td></tr>
</table>

<h2>Jak to děláme u nás</h2>
<table class="wiki-tabulka">
<tr><th>Zvyk</th><th>Proč</th></tr>
<tr><td>Nejdřív <code>run --dry-run</code>, pak ruční úklid</td><td>U knihovny, která vznikala půl roku, je lepší vidět návrh a rozhodnout sám</td></tr>
<tr><td>Zapnuté slučování až po prvním průchodu</td><td>Aby se nejdřív uklidilo a teprve pak slučovalo — jinak se slučují i skilly, které jen mají podobný název</td></tr>
<tr><td>Skilly v gitu</td><td>Verze, rozdíly a návrat zpět bez spoléhání na zálohu kurátora</td></tr>
<tr><td>Archiv, ne smazání</td><td>I po měsících se najde skill, který byl „zbytečný“, ale měl v sobě jeden recept</td></tr>
</table>

<h2>Časté chyby</h2>
<table class="wiki-tabulka">
<tr><th>Příznak</th><th>Příčina a řešení</th></tr>
<tr><td>Kurátor se vůbec nespouští</td><td>Musí platit obojí: uplynul interval <em>a</em> agent je nečinný. Na nové instalaci navíc první běh čeká celý interval</td></tr>
<tr><td>Po sloučení něco chybí</td><td><code>hermes curator rollback --list</code> a návrat konkrétního snímku; obsah před sloučením je i v ledgeru</td></tr>
<tr><td>Vestavěné skilly mizí</td><td>Máte <code>prune_builtins: true</code> — vypněte ho a archivované skilly vraťte přes <code>restore</code></td></tr>
<tr><td>Kontrola je drahá</td><td>Nasměrujte <code>auxiliary.curator</code> na levný model; samotná archivace nic nestojí</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/skilly/"><strong>Skilly</strong><span>Co to je a jak je psát</span></a>
<a href="/wiki/funkce/zalohy-a-obnova/"><strong>Zálohy a obnova</strong><span>Snímek celého agenta, ne jen knihovny</span></a>
<a href="/wiki/zaciname/pamet/"><strong>Paměť agenta</strong><span>Druhá polovina toho, co si agent nese</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/curator" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Kurátor, ledger a telemetrie do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co kurátor je
Údržba skillů, které si vytvořil agent: sleduje zobrazení/použití/úpravy a posouvá stavy
aktivní -> zastaralý (14 dní bez použití) -> archiv (30 dní). Volitelně pustí LLM sloučení.
Nemaže: maximum je archiv do ~/.hermes/skills/.archive/. Hub skilly (agentskills.io) jsou vždy vynechané.

## Kdy běží
Ne cron, ale nečinnost: interval_hours 168 (7 dní) + min_idle_hours 2. První běh na nové instalaci
je odložen o celý interval (last_run_at = teď). Desktop/serve mají hodinový údržbový časovač.

## Nastavení (config.yaml)
curator.enabled true · interval_hours 168 · min_idle_hours 2 · stale_after_days 14 · archive_after_days 30 ·
consolidate false (LLM, jediná fáze, která přepisuje obsah -> před ní záloha) · prune_builtins false.
Model pro kontrolu: auxiliary.curator (provider auto = hlavní model).

## CLI
status · run [--consolidate|--background|--dry-run] · backup · rollback [--list|--id <ts>|-y] ·
pause/resume · pin/unpin · adopt [--all-unmanaged] · list-unmanaged · restore · list-archived ·
archive · prune [--days N] · ledger [--skill X] · rollback <entry-id> · purge [--days N --dry-run].

## Jistoty
Připnuté skilly a skilly použité v cronu (i pozastaveném) se nepřesouvají. Skill s use_count 0 má lhůtu
(stale_after_days), než může být archivován.

## U nás
Nejdřív run --dry-run, pak ruční úklid; consolidate až po prvním průchodu; skilly v gitu; archiv, ne mazání.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🗂️</span><div><strong>The curator never deletes. The harshest thing it does is archive — and that is one command away from coming back.</strong>
It solves one annoying fact: when the agent saves a new skill for every novel problem, half a year
later the library is full of narrow near-duplicates. The curator keeps that in check, but leaves the
decisions to you — and it does not touch the library before you have had a chance to look.</div></div>

<h2>What the curator does</h2>
<p>It tracks how often each skill was viewed, used and patched, and moves it through three states:
<strong>active → stale → archived</strong>. With the consolidation phase enabled it occasionally runs
a short review on a cheaper model that proposes merges or patches drift.</p>
<table class="wiki-tabulka">
<tr><th>Phase</th><th>What it does</th><th>Does it cost money?</th></tr>
<tr><td>Automatic transitions</td><td>Unused for 14 days = stale; 30 days = archived</td><td>No (always on while the curator is enabled)</td></tr>
<tr><td>LLM consolidation</td><td>Surveys the skills, proposes merging near-duplicates and fixes drifted text</td><td>Yes, but it can run on a cheap model</td></tr>
</table>
<p class="note">Only <strong>agent-created</strong> skills are managed automatically. Skills installed
from the hub (agentskills.io) are always off-limits.</p>

<h2>When it runs</h2>
<p>Not on a cron schedule, but on inactivity. Hermes checks at CLI start, during gateway housekeeping
and on the Desktop maintenance timer whether both are true:</p>
<table class="wiki-tabulka">
<tr><th>Condition</th><th>Default</th></tr>
<tr><td>Time since the last run</td><td><code>interval_hours</code> = 168 (7 days)</td></tr>
<tr><td>The agent has been idle long enough</td><td><code>min_idle_hours</code> = 2 hours</td></tr>
</table>
<p><strong>The first run is deferred</strong> by a full interval: on a fresh install it just records
“now” and the first real pass happens a week later. That is deliberate — you get time to review the
library and pin anything important.</p>

<h2>Configuration</h2>
<div class="code-block">curator:
  enabled: true
  interval_hours: 168          <span class="c"># 7 days</span>
  min_idle_hours: 2
  stale_after_days: 14
  archive_after_days: 30
  consolidate: false           <span class="c"># LLM consolidation — off</span>
  prune_builtins: false        <span class="c"># also archive unused bundled skills</span></div>
<table class="wiki-tabulka">
<tr><th>Key</th><th>Purpose</th></tr>
<tr><td><code>consolidate</code></td><td>Enables the consolidation pass. It is the only phase that rewrites skill content — which is why Hermes snapshots the library before it</td></tr>
<tr><td><code>prune_builtins</code></td><td>Archive unused bundled skills too. Optional, because bundled skills disappearing looks like a broken install</td></tr>
<tr><td><code>auxiliary.curator</code></td><td>Which model runs the review. Leave <code>auto</code> (main model) or pin a cheap one</td></tr>
</table>
<div class="code-block"><span class="c"># cheaper model for the review (config.yaml)</span>
auxiliary:
  curator:
    provider: openrouter
    model: google/gemini-3-flash-preview
    timeout: 600</div>

<h2>Commands worth knowing</h2>
<table class="wiki-tabulka">
<tr><th>Command</th><th>What it does</th></tr>
<tr><td><code>hermes curator status</code></td><td>Last run, counts, pinned skills, least-used skills</td></tr>
<tr><td><code>hermes curator run --dry-run</code></td><td><strong>Start here</strong> — prints what the curator would do and changes nothing</td></tr>
<tr><td><code>hermes curator run</code></td><td>Runs a pass now (prune-only unless consolidation is on)</td></tr>
<tr><td><code>hermes curator pin &lt;skill&gt;</code></td><td>Never auto-transition or archive this skill</td></tr>
<tr><td><code>hermes curator backup</code> / <code>rollback</code></td><td>Manual snapshot of the library and returning to it</td></tr>
<tr><td><code>hermes curator restore &lt;skill&gt;</code></td><td>Moves an archived skill back to active</td></tr>
<tr><td><code>hermes curator ledger</code></td><td>Who changed what and when; <code>rollback &lt;id&gt;</code> undoes one change</td></tr>
</table>

<h2>What never happens</h2>
<table class="wiki-tabulka">
<tr><th>Worry</th><th>Reality</th></tr>
<tr><td>“It will delete my skills”</td><td>It does not delete. Archiving moves a skill to <code>~/.hermes/skills/.archive/</code></td></tr>
<tr><td>“It will touch hub skills”</td><td>No, those are always excluded</td></tr>
<tr><td>“It will archive a skill a cron job uses”</td><td>No. A skill referenced by any scheduled job (even a paused one) is treated as pinned</td></tr>
<tr><td>“It will drop a skill nobody used yet”</td><td>No. A skill with zero uses gets a grace period — it is not archived before it is as old as <code>stale_after_days</code></td></tr>
</table>

<h2>How we do it</h2>
<table class="wiki-tabulka">
<tr><th>Habit</th><th>Why</th></tr>
<tr><td><code>run --dry-run</code> first, then clean up by hand</td><td>With a library that grew over months it is better to see the proposal and decide yourself</td></tr>
<tr><td>Turn consolidation on only after the first pass</td><td>Clean up first, merge afterwards — otherwise you merge skills that merely share a name</td></tr>
<tr><td>Keep skills in git</td><td>Versions, diffs and rollback without relying on the curator's snapshot</td></tr>
<tr><td>Archive, never delete</td><td>Months later a “useless” skill turns out to hold one recipe you need</td></tr>
</table>

<h2>Common mistakes</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>Cause and fix</th></tr>
<tr><td>The curator never runs</td><td>Both conditions must hold: the interval has passed <em>and</em> the agent is idle. On a fresh install the first run waits a full interval</td></tr>
<tr><td>Something is missing after consolidation</td><td><code>hermes curator rollback --list</code> and restore a specific snapshot; the ledger also records the pre-merge content</td></tr>
<tr><td>Bundled skills are disappearing</td><td>You have <code>prune_builtins: true</code> — turn it off and bring archived skills back with <code>restore</code></td></tr>
<tr><td>The review is expensive</td><td>Point <code>auxiliary.curator</code> at a cheap model; the archival pass itself costs nothing</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/skills/"><strong>Skills</strong><span>What they are and how to write them</span></a>
<a href="/en/wiki/features/backups-and-restore/"><strong>Backups and restore</strong><span>A snapshot of the whole agent, not just the library</span></a>
<a href="/en/wiki/getting-started/memory/"><strong>Agent memory</strong><span>The other half of what the agent carries</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/curator" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Curator, ledger and telemetry in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What it is
Maintenance for agent-created skills: tracks views/uses/patches and moves states
active -> stale (14 days unused) -> archive (30 days). Optional LLM consolidation.
It never deletes: the maximum is archiving to ~/.hermes/skills/.archive/. Hub skills (agentskills.io) always excluded.

## When it runs
Not cron, but inactivity: interval_hours 168 (7 days) + min_idle_hours 2. The first run on a fresh install
is deferred one full interval (last_run_at = now). Desktop/serve share an hourly maintenance timer.

## Config (config.yaml)
curator.enabled true · interval_hours 168 · min_idle_hours 2 · stale_after_days 14 · archive_after_days 30 ·
consolidate false (the only phase that rewrites content -> snapshot taken first) · prune_builtins false.
Review model: auxiliary.curator (provider auto = main model).

## CLI
status · run [--consolidate|--background|--dry-run] · backup · rollback [--list|--id <ts>|-y] ·
pause/resume · pin/unpin · adopt [--all-unmanaged] · list-unmanaged · restore · list-archived ·
archive · prune [--days N] · ledger [--skill X] · rollback <entry-id> · purge [--days N --dry-run].

## Guarantees
Pinned skills and skills referenced by cron (even paused) are not transitioned. A skill with use_count 0
gets a grace period (stale_after_days) before it can be archived.

## Our practice
run --dry-run first, then manual cleanup; consolidation only after the first pass; skills in git; archive, never delete.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(27)
    stranka = najdi(27)
    assert stranka and stranka["nazev"] == "Kurátor skillů"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Kurátor skillů — údržba knihovny bez mazání",
        "Jak kurátor pozná nepoužívané skilly, kdy se spouští, jaké má limity a jak knihovnu projít a uklidit, aniž byste o něco přišli.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Kurátor skillů",
        "Kurátor nemaže — jen archivuje, a archiv se dá vrátit. Co dělá, kdy se spustí a jak si knihovnu projít.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Kurátor skillů — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Skill curator — keeping the library tidy without deleting",
        "How the curator spots unused skills, when it runs, what its limits are and how to review and tidy the library without losing anything.",
        OBRAZEK, "Wiki · Features in depth", "Skill curator",
        "The curator never deletes — it archives, and an archive can be restored. What it does, when it runs and how to review your library.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Skill curator — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
