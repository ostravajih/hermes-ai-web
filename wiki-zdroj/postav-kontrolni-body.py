#!/usr/bin/env python3
"""Postaví stránku wiki „Kontrolní body a návrat zpět" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-checkpoints-and-rollback.md (co spouští kontrolní bod,
seznam příkazů, nastavení, obnova jednoho souboru, ochranné meze, kde body bydlí).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback"
OBRAZEK = "wiki-kontrolni-body"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📸</span><div><strong>Než agent sáhne na soubor, může si udělat snímek. Když se něco pokazí, vrátíte se o krok zpět — a o vaše vlastní úpravy nepřijdete.</strong>
Pozor na dvě věci: kontrolní body jsou <strong>ve výchozím stavu vypnuté</strong> a <strong>nejsou to
zálohy</strong>. Jsou to vrátné kroky pro práci agenta.</div></div>

<h2>Nejdřív je zapněte</h2>
<p>Bez zapnutí se žádné snímky nedělají — ať se stane cokoli, není se kam vrátit. Máte dvě možnosti:</p>
<div class="code-block"><span class="c"># jednorázově pro jedno spuštění</span>
<span class="p">❯</span> hermes chat --checkpoints

<span class="c"># natrvalo v ~/.hermes/config.yaml</span>
checkpoints:
  enabled: true              <span class="c"># hlavní vypínač (výchozí: false)</span>
  max_snapshots: 20          <span class="c"># kolik snímků na projekt</span>
  max_total_size_mb: 500     <span class="c"># strop velikosti celého úložiště</span>
  max_file_size_mb: 10       <span class="c"># větší jednotlivé soubory se přeskakují</span></div>

<h2>Kdy si agent snímek udělá</h2>
<table class="wiki-tabulka">
<tr><th>Před čím</th><th>Příklady</th></tr>
<tr><td>Nástroje pro soubory</td><td>Zápis souboru, úprava souboru</td></tr>
<tr><td>Ničivé příkazy v terminálu</td><td>Smazání (<code>rm</code>, <code>rmdir</code>), přesun a kopírování (<code>mv</code>, <code>cp</code>), úprava na místě (<code>sed -i</code>), zkrácení (<code>truncate</code>, <code>dd</code>, <code>shred</code>), přesměrování výstupu do souboru (<code>&gt;</code>), změny v gitu (reset, clean, checkout)</td></tr>
</table>
<p class="note">Na jednu složku vznikne nejvýš <strong>jeden snímek za jedno kolo</strong> — aby se
úložiště nezaplnilo desítkami kopií během dlouhé práce.</p>

<h2>Jak se vracíte zpět</h2>
<table class="wiki-tabulka">
<tr><th>Co napíšete</th><th>Co to udělá</th></tr>
<tr><td><code>/rollback</code></td><td>Vypíše seznam snímků i s přehledem změn</td></tr>
<tr><td><code>/rollback 3</code></td><td>Vrátí stav k třetímu snímku; <strong>vaše ruční úpravy zůstanou</strong> a zároveň se zruší poslední kolo rozhovoru</td></tr>
<tr><td><code>/rollback 3 --all</code></td><td>Vrátí úplně všechno — i vaše ruční úpravy</td></tr>
<tr><td><code>/rollback diff 3</code></td><td>Ukáže, co se od třetího snímku změnilo (ještě nic nemění)</td></tr>
<tr><td><code>/rollback 3 poznamky.md</code></td><td>Vrátí jen jeden soubor ze snímku</td></tr>
</table>
<p>Seznam vypadá nějak takhle — u každé položky poznáte, co ji vyvolalo:</p>
<div class="code-block">📸 Kontrolní body pro /var/www/muj-web:

  1. 4270a8c  17. 10. 2026 04:36  před úpravou  (1 soubor, +1/−0)
  2. eaf4c1f  17. 10. 2026 04:35  před zápisem souboru
  3. b3f9d2e  17. 10. 2026 04:34  před příkazem: sed -i s/old/new/ config.py</div>
<p>Když je potřeba se do úložiště podívat mimo rozhovor:</p>
<table class="wiki-tabulka">
<tr><th>Příkaz</th><th>K čemu</th></tr>
<tr><td><code>hermes checkpoints status</code></td><td>Kolik místa snímky zabírají a u kterých projektů</td></tr>
<tr><td><code>hermes checkpoints prune</code></td><td>Ruční úklid — smaže stará a osiřelá data a vynutí strop velikosti</td></tr>
<tr><td><code>hermes checkpoints clear</code></td><td>Smaže celé úložiště (zeptá se předem)</td></tr>
</table>

<h2>Vaše vlastní úpravy se nechají</h2>
<p>Když po agentovi sáhnete do souboru sami a pak se vrátíte k nějakému snímku, Hermes soubor, který
jste mezitím upravili, <strong>nepřepíše</strong> — vypíše ho zvlášť:</p>
<div class="code-block">✅ Návrat ke snímku a1b2c3d4: před zápisem souboru
↷ Nechal jsem vaše úpravy: src/config.py, poznamky.md
   Chcete vrátit i ty? Použijte /rollback 1 --all</div>
<p>Přepíše se jen to, co mezitím zapsal agent. Když vrátit opravdu všechno, přidejte <code>--all</code>.</p>

<h2>Co snímky nezachrání</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co se stane</th></tr>
<tr><td>Agent běží v kontejneru (Docker a podobně)</td><td>Cesty patří kontejneru, ne vašemu počítači — snímky se nedělají a obnova se odmítne. Ověřeno i na terminálu, v chatu, v TUI i v aplikaci</td></tr>
<tr><td>Vnořený git repozitář uvnitř složky</td><td>Uloží se jen odkaz, ne jeho soubory. Úplná obnova se odmítne (neslíbí něco, co nemá). Záchrana: snímek pořídit přímo ve složce toho vnořeného repozitáře</td></tr>
<tr><td>Složka s více než 50 tisíci soubory</td><td>Přeskočí se</td></tr>
<tr><td>Kořen systému nebo domovská složka</td><td>Přeskočí se (moc široké)</td></tr>
<tr><td>Na počítači není <code>git</code></td><td>Kontrolní body se tiše vypnou</td></tr>
<tr><td>Soubor větší než 10 MB</td><td>Přeskočí se</td></tr>
</table>

<h2>Kde snímky bydlí</h2>
<div class="code-block">~/.hermes/checkpoints/
  ├── store/          <span class="c"># jedno společné úložiště pro všechny projekty</span>
  ├── .last_prune     <span class="c"># značka posledního úklidu</span>
  └── legacy-…        <span class="c"># archiv staršího uspořádání</span></div>
<p>Úklid běží sám na pozadí (snímky projektů, kterých jste se dlouho nedotkli, se mažou; údržba se
spouští nejvýš jednou za několik hodin a nikdy neblokuje start). Ručně se dá vyvolat příkazem
<code>hermes checkpoints prune</code>.</p>

<h2>Pasti z našeho provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co se stalo</th><th>Co s tím</th></tr>
<tr><td><strong>Kontrolní body byly vypnuté a nebylo se kam vrátit</strong></td><td>Nejčastější past — výchozí stav je vypnuto. Zapněte je dřív, než začnete pracovat, ne až když je zle</td></tr>
<tr><td><strong>Považovali jsme snímky za zálohu</strong></td><td>Nejsou. Snímky se týkají jen souborů, které měnil agent, a mají stropy (20 na projekt, 500 MB). Skutečná záloha je jinde</td></tr>
<tr><td><strong><code>--all</code> přepsal naši ruční úpravu</strong></td><td>Vrácení zpět bez <code>--all</code> vaše úpravy chrání — používejte ho jen vědomě</td></tr>
<tr><td><strong>V kontejneru obnova nešla</strong></td><td>Očekávané chování: cesty patří kontejneru. V kontejnerovém režimu se spolehněte na git nebo na zálohu mimo kontejner</td></tr>
<tr><td><strong>Snímek vznikl, ale obnova se odmítla</strong></td><td>Nejspíš obsahoval vnořený repozitář. Obnovte zvlášť ostatní soubory (<code>/rollback 1 poznamky.md</code>) nebo mějte snímky z vnořeného repozitáře</td></tr>
<tr><td><strong>Úložiště snímků rostlo do stovek megabajtů</strong></td><td>Stropy se dají snížit (<code>max_snapshots</code>, <code>max_total_size_mb</code>) a stav zjistíte přes <code>hermes checkpoints status</code></td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Před obnovou si dejte <code>/rollback diff</code></td><td>Uvidíte, co přesně zmizí, a vyberete správný snímek</td></tr>
<tr><td>Na projekty, které mají vlastní historii, používejte git</td><td>Kontrolní body jsou pojistka pro práci agenta, ne náhrada gitu</td></tr>
<tr><td>Zapněte si je hlavně tam, kde agent sahá na soubory</td><td>V projektech, kde jen čte, jsou zbytečné</td></tr>
<tr><td>Když pracujete na důležité věci, dělejte i kopii mimo projekt</td><td>Snímky chrání před omylem agenta, ne před smazaným diskem</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/funkce/spousteni-prikazu/"><strong>Spouštění příkazů a schvalování</strong><span>Kdy se agent zeptá, než něco udělá</span></a>
<a href="/wiki/funkce/sezeni/"><strong>Sezení a jejich obnova</strong><span>Vrátit se k rozdělané práci</span></a>
<a href="/wiki/zaciname/bezpecnost/"><strong>Bezpečnost</strong><span>Co agent smí a co ne</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Kontrolní body do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Zapnutí (výchozí je VYPNUTO)
hermes chat --checkpoints   (jednorázově)
config.yaml: checkpoints.enabled: true; max_snapshots 20; max_total_size_mb 500; max_file_size_mb 10

## Kdy vzniká snímek
Před zápisem a úpravou souboru; před ničivými příkazy v terminálu (rm, rmdir, cp, install, mv, sed -i,
truncate, dd, shred, přesměrování >, git reset/clean/checkout).
Na jednu složku nejvýš jeden snímek za kolo.

## Příkazy
/rollback              seznam snímků s přehledem změn
/rollback 3            návrat ke snímku 3, ruční úpravy zůstanou, zruší poslední kolo rozhovoru
/rollback 3 --all      úplný návrat (přepíše i ruční úpravy)
/rollback diff 3       náhled změn od snímku 3
/rollback 3 soubor.md  návrat jednoho souboru
hermes checkpoints status | prune | clear | clear-legacy

## Ochrana ručních úprav
Návrat bez --all vrátí jen soubory, které měnil agent; soubory upravené člověkem přeskočí a vypíše je.

## Meze (nejsou to zálohy)
Kontejner (docker…) -> snímky se nedělají a obnova se odmítne (i v chat/TUI/aplikaci).
Vnořený git repozitář -> uloží se jen odkaz; úplná obnova se odmítne.
Více než 50 000 souborů, kořen / a domovská složka -> přeskočeno. Bez gitu na PATH -> vypnuto.
Soubor nad 10 MB -> přeskočen.

## Kde bydlí
~/.hermes/checkpoints/store/ (jedno společné úložiště, na projekt větev podle otisku cesty);
.last_prune = značka úklidu; legacy-* = archiv staršího uspořádání. Úklid běží na pozadí,
ručně hermes checkpoints prune.

## Pasti z našeho provozu
1. Vypnuté kontrolní body -> není se kam vrátit (zapnout předem).
2. Považovat snímky za zálohu -> nejsou (stropy, jen soubory měněné agentem).
3. --all přepsal ruční úpravu -> používat vědomě.
4. V kontejneru obnova nejde -> spolehnout se na git/zálohu mimo kontejner.
5. Obnova odmítnuta -> snímek obsahoval vnořený repozitář; obnovit po souborech.
6. Úložiště roste -> snížit stropy, zkontrolovat hermes checkpoints status.

## Tipy
Před obnovou /rollback diff · na projekty s vlastní historií git · zapínat tam, kde agent sahá na
soubory · u důležitých věcí ještě kopii mimo projekt.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📸</span><div><strong>Before the agent touches a file it can take a snapshot. When something breaks you step back one move — without losing your own edits.</strong>
Two things to remember: checkpoints are <strong>off by default</strong> and they are
<strong>not backups</strong>. They are undo steps for the agent's work.</div></div>

<h2>Enable them first</h2>
<p>With checkpoints off no snapshots are taken at all — whatever happens, there is nothing to return
to. Two options:</p>
<div class="code-block"><span class="c"># once, for a single run</span>
<span class="p">❯</span> hermes chat --checkpoints

<span class="c"># permanently in ~/.hermes/config.yaml</span>
checkpoints:
  enabled: true              <span class="c"># master switch (default: false)</span>
  max_snapshots: 20          <span class="c"># snapshots per project</span>
  max_total_size_mb: 500     <span class="c"># cap on the whole store</span>
  max_file_size_mb: 10       <span class="c"># larger single files are skipped</span></div>

<h2>When a snapshot is taken</h2>
<table class="wiki-tabulka">
<tr><th>Before</th><th>Examples</th></tr>
<tr><td>File tools</td><td>Writing a file, editing a file</td></tr>
<tr><td>Destructive terminal commands</td><td>Deleting (<code>rm</code>, <code>rmdir</code>), moving and copying (<code>mv</code>, <code>cp</code>), in-place edits (<code>sed -i</code>), truncating (<code>truncate</code>, <code>dd</code>, <code>shred</code>), output redirection (<code>&gt;</code>), git changes (reset, clean, checkout)</td></tr>
</table>
<p class="note">At most <strong>one snapshot per directory per turn</strong>, so a long session does not
fill the store with dozens of copies.</p>

<h2>How you go back</h2>
<table class="wiki-tabulka">
<tr><th>What you type</th><th>What it does</th></tr>
<tr><td><code>/rollback</code></td><td>Lists the snapshots with change stats</td></tr>
<tr><td><code>/rollback 3</code></td><td>Restores checkpoint 3; <strong>your hand-edits stay</strong>, and the last chat turn is undone too</td></tr>
<tr><td><code>/rollback 3 --all</code></td><td>Full restore — your hand-edits are overwritten as well</td></tr>
<tr><td><code>/rollback diff 3</code></td><td>Shows what changed since checkpoint 3 (changes nothing yet)</td></tr>
<tr><td><code>/rollback 3 notes.md</code></td><td>Restores a single file from checkpoint 3</td></tr>
</table>
<p>The listing looks roughly like this — each entry says what triggered it:</p>
<div class="code-block">📸 Checkpoints for /var/www/my-site:

  1. 4270a8c  2026-10-17 04:36  before patch  (1 file, +1/−0)
  2. eaf4c1f  2026-10-17 04:35  before write_file
  3. b3f9d2e  2026-10-17 04:34  before terminal: sed -i s/old/new/ config.py</div>
<p>To inspect the store outside a session:</p>
<table class="wiki-tabulka">
<tr><th>Command</th><th>What for</th></tr>
<tr><td><code>hermes checkpoints status</code></td><td>How much space snapshots take and for which projects</td></tr>
<tr><td><code>hermes checkpoints prune</code></td><td>Manual sweep — deletes stale and orphaned data, enforces the size cap</td></tr>
<tr><td><code>hermes checkpoints clear</code></td><td>Removes the whole store (asks first)</td></tr>
</table>

<h2>Your own edits are kept</h2>
<p>If you edit a file by hand after the agent touched it and then roll back, Hermes
<strong>skips</strong> that file instead of overwriting it, and lists it separately:</p>
<div class="code-block">✅ Restored to checkpoint a1b2c3d4: before write_file
↷ Kept your hand-edits: src/config.py, notes.md
   To restore those too, use /rollback 1 --all</div>
<p>Only files the agent last wrote get reverted. Add <code>--all</code> when you really want everything
back.</p>

<h2>What snapshots will not save you from</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What happens</th></tr>
<tr><td>The agent runs in a container (Docker and similar)</td><td>Paths belong to the container, not your machine — no checkpoints are taken and restore is refused. The same on the CLI, in chat, in the TUI and in the desktop app</td></tr>
<tr><td>A nested git repository inside the directory</td><td>Only a reference is stored, not its files. A full restore is refused (it will not claim success for files it never captured). Workaround: take the checkpoint inside the nested repository's own directory</td></tr>
<tr><td>A directory with more than 50,000 files</td><td>Skipped</td></tr>
<tr><td>The filesystem root or your home directory</td><td>Skipped (too broad)</td></tr>
<tr><td>No <code>git</code> on the machine</td><td>Checkpoints are silently disabled</td></tr>
<tr><td>A file larger than 10 MB</td><td>Skipped</td></tr>
</table>

<h2>Where the snapshots live</h2>
<div class="code-block">~/.hermes/checkpoints/
  ├── store/          <span class="c"># one shared store for all projects</span>
  ├── .last_prune     <span class="c"># marker of the last sweep</span>
  └── legacy-…        <span class="c"># archive of the older layout</span></div>
<p>Housekeeping runs by itself in the background (snapshots of projects you have not touched for a
while are removed; maintenance runs at most once every few hours and never blocks startup). You can
trigger it by hand with <code>hermes checkpoints prune</code>.</p>

<h2>Pitfalls from our systems</h2>
<table class="wiki-tabulka">
<tr><th>What happened</th><th>What to do</th></tr>
<tr><td><strong>Checkpoints were off and there was nothing to return to</strong></td><td>The most common trap — off is the default. Enable them before you start working, not once it hurts</td></tr>
<tr><td><strong>We treated snapshots as a backup</strong></td><td>They are not. They cover only files the agent changed and have caps (20 per project, 500 MB). Real backup lives elsewhere</td></tr>
<tr><td><strong><code>--all</code> overwrote our hand-edit</strong></td><td>A restore without <code>--all</code> protects your edits — use it deliberately</td></tr>
<tr><td><strong>Restore did not work in a container</strong></td><td>Expected: paths belong to the container. In container mode rely on git or a backup outside the container</td></tr>
<tr><td><strong>A snapshot existed but restore was refused</strong></td><td>It probably contained a nested repository. Restore the other files individually (<code>/rollback 1 notes.md</code>) or keep snapshots from the nested repository</td></tr>
<tr><td><strong>The checkpoint store grew into hundreds of megabytes</strong></td><td>Lower the caps (<code>max_snapshots</code>, <code>max_total_size_mb</code>) and check <code>hermes checkpoints status</code></td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Run <code>/rollback diff</code> before restoring</td><td>You see exactly what is about to disappear and pick the right snapshot</td></tr>
<tr><td>Use git for projects that already have history</td><td>Checkpoints are a safety net for the agent's work, not a replacement for git</td></tr>
<tr><td>Enable them where the agent actually writes files</td><td>In read-only projects they are pointless</td></tr>
<tr><td>Keep a copy outside the project for important work</td><td>Snapshots protect against an agent mistake, not a dead disk</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/features/command-execution/"><strong>Running commands and approvals</strong><span>When the agent asks before acting</span></a>
<a href="/en/wiki/features/sessions/"><strong>Sessions and resuming</strong><span>Coming back to unfinished work</span></a>
<a href="/en/wiki/getting-started/security/"><strong>Security</strong><span>What the agent may and may not do</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Checkpoints in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Enabling (OFF by default)
hermes chat --checkpoints   (one run)
config.yaml: checkpoints.enabled: true; max_snapshots 20; max_total_size_mb 500; max_file_size_mb 10

## When a snapshot is taken
Before write_file and patch; before destructive terminal commands (rm, rmdir, cp, install, mv, sed -i,
truncate, dd, shred, output redirect >, git reset/clean/checkout).
At most one snapshot per directory per turn.

## Commands
/rollback              list snapshots with change stats
/rollback 3            restore checkpoint 3, hand-edits kept, last chat turn undone
/rollback 3 --all      full restore (overwrites hand-edits too)
/rollback diff 3       preview changes since checkpoint 3
/rollback 3 notes.md   restore a single file
hermes checkpoints status | prune | clear | clear-legacy

## Hand-edit protection
A restore without --all reverts only files the agent wrote; human-edited files are skipped and listed.

## Limits (not backups)
Container (docker…) -> no checkpoints, restore refused (CLI, chat, TUI, desktop alike).
Nested git repo -> only a gitlink stored; full restore refused.
More than 50,000 files, root / and $HOME -> skipped. No git on PATH -> disabled.
Single file over 10 MB -> skipped.

## Where they live
~/.hermes/checkpoints/store/ (one shared store, per-project branch keyed by path hash);
.last_prune = last sweep marker; legacy-* = archive of the older layout. Housekeeping runs in the
background; manually hermes checkpoints prune.

## Pitfalls from our systems
1. Checkpoints off -> nothing to return to (enable beforehand).
2. Treating snapshots as a backup -> they are not (caps, only agent-changed files).
3. --all overwrote a hand-edit -> use deliberately.
4. Restore refused in a container -> rely on git/backup outside the container.
5. Restore refused for a snapshot -> it contained a nested repo; restore files individually.
6. Store growing -> lower the caps, check hermes checkpoints status.

## Tips
/rollback diff before restoring · git for projects with history · enable where the agent writes files ·
keep a copy outside the project for important work.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(22)
    stranka = najdi(22)
    assert stranka and stranka["nazev"] == "Kontrolní body a návrat zpět"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Kontrolní body a návrat zpět — když se něco pokazí",
        "Jak zapnout kontrolní body (ve výchozím stavu jsou vypnuté), jak vrátit agentovu práci zpět, jak ochránit vlastní úpravy a co snímky nezachrání.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Kontrolní body a návrat zpět",
        "Než agent sáhne na soubor, může si udělat snímek. Ukážeme, jak se vracet zpět, jak nepřijít o vlastní úpravy a proč to není záloha.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Kontrolní body a návrat zpět — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Checkpoints and rollback — when something breaks",
        "How to enable checkpoints (off by default), how to undo the agent's work, how your own edits are protected, and what snapshots will not save you from.",
        OBRAZEK, "Wiki · Features in depth", "Checkpoints and rollback",
        "Before the agent touches a file it can take a snapshot. Here is how to roll back, how your own edits stay safe and why it is not a backup.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Checkpoints and rollback — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
