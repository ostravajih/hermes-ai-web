#!/usr/bin/env python3
"""Postaví stránku wiki „Zálohy a obnova" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-session-storage-recovery.md (co leží vedle state.db,
tři kroky při odmítnutém zápisu, co nikdy nedělat), developer-guide-state-db-recovery.md
(karanténa, sessions recover/repair), reference-cli-commands.md (hermes backup, hermes import,
hermes backup restore, exit kódy, co je z archivu vyloučené), reference-faq.md
(hermes backup vs hermes profile export), getting-started-updating.md (snapshot před aktualizací).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/reference/cli-commands"
OBRAZEK = "wiki-zalohy"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">💾</span><div><strong>Záloha, kterou jste nikdy nezkusili obnovit, není záloha — je to jen soubor na disku.</strong>
Hermes má naštěstí obnovu rozumně udělanou: zálohu umí vzít i za běhu a obnovu pozná, když je
archiv poškozený. Zbývá jediná věc, kterou za vás nikdo neudělá — vyzkoušet to dřív, než to budete
potřebovat.</div></div>

<h2>Co je potřeba zálohovat</h2>
<p>Všechno důležité je v jedné složce — v domovské složce Hermese (<code>~/.hermes/</code>).</p>
<table class="wiki-tabulka">
<tr><th>Co</th><th>Proč na tom záleží</th></tr>
<tr><td><code>config.yaml</code>, <code>.env</code>, <code>auth.json</code></td><td>Nastavení, klíče k modelům a přihlášení. Bez nich je obnova jen prázdný agent</td></tr>
<tr><td><code>state.db</code> (+ <code>-wal</code>, <code>-shm</code>)</td><td>Všechny konverzace, sezení a navazující data</td></tr>
<tr><td><code>skills/</code>, <code>memories/</code></td><td>Co se agent naučil a co si o vás pamatuje</td></tr>
<tr><td><code>cron/</code></td><td>Pravidelné úlohy — bez nich agent po obnově „zapomene“, co má dělat každý den</td></tr>
<tr><td><code>SOUL.md</code>, profily</td><td>Osobnost agenta a všechny další profily</td></tr>
</table>
<p class="note">Pokud používáte víc profilů, každý má vlastní <code>state.db</code> i vlastní složku.
Záloha na úrovni celého <code>~/.hermes/</code> je proto bezpečnější než kopírovat jen „ten svůj“ profil.</p>

<h2>Záloha jedním příkazem</h2>
<div class="code-block"><span class="c"># celá záloha (výchozí cíl: ~/hermes-backup-&lt;čas&gt;.zip)</span>
hermes backup

<span class="c"># na konkrétní místo, ať to máte na disku, který zálohujete jinam</span>
hermes backup -o /root/zalohy/hermes.zip

<span class="c"># rychlý snímek jen toho podstatného (config, state.db, .env, cron)</span>
hermes backup --quick --label "pred-upgradem"

<span class="c"># po plné záloze nechat jen 5 nejnovějších</span>
hermes backup -o /root/zalohy/ -k 5</div>
<table class="wiki-tabulka">
<tr><th>Vlastnost</th><th>Jak to funguje</th></tr>
<tr><td>Záloha za běhu</td><td>Kopírování jde přes SQLite <code>backup()</code>, takže je konzistentní i když agent právě pracuje (WAL režim)</td></tr>
<tr><td>Co v archivu není</td><td>Samotný kód agenta, modely a runtime (desítky GB, dají se stáhnout znovu), keše, kontrolní body a staré zálohy</td></tr>
<tr><td>Návratový kód</td><td><code>0</code> = vše v archivu; <code>1</code> = část souborů chyběla (archiv zůstane, ať se dá obnovit zbytek); <code>2</code> = jiná záloha právě běží</td></tr>
</table>
<p><strong>Kód 1 je důležitý:</strong> kdyby zálohu pouštěl cron, musí se podle kódu poznat, že archiv
není úplný. Právě proto se <code>--keep</code> v takovém případě nemaže starší (a kompletní) archivy.</p>

<h2>Obnova</h2>
<div class="code-block"><span class="c"># obnova celého archivu (nejdřív zastavte bránu)</span>
hermes gateway stop
hermes import /root/zalohy/hermes.zip

<span class="c"># vrácení snímku, který se udělá před aktualizací</span>
hermes backup restore --state pre-update</div>
<p>Archiv se před zápisem celý rozbalí a zkontroluje (CRC). Když je poškozený, příkaz skončí
s chybou a <strong>nic nezapíše</strong>. Soubory, které se nepodaří obnovit, vypíše — a vrátí kód 1,
takže se částečná obnova nikdy netváří jako úspěch.</p>

<h2>Záloha versus předání profilu</h2>
<table class="wiki-tabulka">
<tr><th></th><th><code>hermes backup</code></th><th><code>hermes profile export</code></th></tr>
<tr><td>K čemu</td><td>Přesun celého stroje, obnova po havárii</td><td>Předání nebo přenos jednoho profilu</td></tr>
<tr><td>Rozsah</td><td>Všechny profily, globální nastavení, klíče, sezení</td><td>Jeden profil: SOUL.md, paměť, sezení, skilly</td></tr>
<tr><td>Tajné údaje</td><td><strong>Jsou uvnitř</strong> (<code>.env</code>, <code>auth.json</code>)</td><td><strong>Nejsou</strong> — odstraní se, aby se dal profil bezpečně sdílet</td></tr>
<tr><td>Formát</td><td><code>.zip</code></td><td><code>.tar.gz</code></td></tr>
</table>
<p class="note">Praktický důsledek: <strong>zálohu z <code>hermes backup</code> nikdy nikomu neposílejte</strong> —
obsahuje klíče. Na sdílení je určený export profilu.</p>

<h2>Když se sezení rozbije (a co nikdy nedělat)</h2>
<p>Hermes vede každou konverzaci v jednom souboru <code>state.db</code> na profil. Když se při psaní
objeví hláška o „staré kopii write-ahead logu“, <strong>nic se neztratilo</strong> — agent právě
přestal psát, aby data nepoškodil. Řeší se to třemi kroky:</p>
<div class="code-block">1) ukončit všechny procesy profilu   hermes gateway stop   (a zavřít Desktop, dashboard, cron)
2) zjistit, kdo drží log             hermes doctor         (vypíše PID a příkaz)
3) spustit znovu (jeden proces) a poslat zprávu znovu</div>
<table class="wiki-tabulka">
<tr><th>Nikdy</th><th>Proto</th></tr>
<tr><td>Mazat <code>state.db-wal</code> nebo <code>state.db-shm</code></td><td>Log obsahuje konverzace, které ještě nejsou v hlavním souboru — smazáním je ztratíte natrvalo</td></tr>
<tr><td>Kopírovat <code>state.db</code> samo přes <code>cp</code></td><td>Ty tři soubory jsou jeden celek; správně je to <code>hermes backup</code> nebo <code>hermes sessions recover</code></td></tr>
<tr><td>Pouštět <code>hermes doctor --fix</code> za běhu</td><td>Může se stát druhým zapisovatelem — přesně tím, co problém způsobilo</td></tr>
<tr><td>Pouštět <code>sessions optimize</code> pod živou branou</td><td>Přepisuje databázi (VACUUM, přestavba indexu), takže příkaz to pozná a odmítne — i s výpisem procesů, které databázi drží. <code>--dry-run</code> je vždy povolený, <code>--force</code> jde použít, ale jen když víte, že ty procesy nic nečtou</td></tr>
<tr><td><code>sessions prune</code> pod živou branou</td><td>Tady je to naopak <em>bezpečné</em>: náhled se udělá jen pro čtení a maže sama brána (sezení s běžícím tahem přeskočí). Odmítne jen tehdy, když brána neběží a databázi drží jiný proces</td></tr>
</table>

<h2>Diagnostika a oprava poškozeného souboru</h2>
<div class="code-block">hermes gateway stop
hermes sessions recover --source ~/.hermes/state.db --inspect-only   <span class="c"># nic nemění, jen řekne, co jde</span>
hermes sessions recover --source ~/.hermes/state.db --output ~/recovered-state.db
hermes sessions repair --check-only                                  <span class="c"># co by se opravilo</span>
hermes sessions repair                                               <span class="c"># oprava (dělá si vlastní zálohu)</span></div>
<p class="note">Vedle <code>state.db</code> můžete potkat soubory jako <code>state.db.pre-update-emergency-*.bak</code>
(snímek před aktualizací) nebo <code>state.db.corrupt.*.bak</code> (kopie poškozeného souboru).
První se hodí na obnovu, druhý <strong>nikdy nevracejte</strong> přes <code>state.db</code> — je to stejná chyba.</p>

<h2>Jak to děláme u nás na serveru</h2>
<table class="wiki-tabulka">
<tr><th>Zvyk</th><th>Proč</th></tr>
<tr><td>Snímek před každou aktualizací: <code>hermes backup --quick --label "pred-upgradem"</code></td><td>Vrácení je pak jeden příkaz a nemusíte řešit, co se změnilo</td></tr>
<tr><td>Denní plná záloha mimo web (jiná složka, jiný stroj)</td><td>Záloha na stejném disku jako data není záloha</td></tr>
<tr><td>Obnova se zkouší do <strong>zkušebního profilu</strong>, ne do produkce</td><td>Ověříte, že archiv opravdu funguje, a přitom si nerozbijete běžícího agenta</td></tr>
<tr><td>Web a aplikace mají vlastní zálohu (git, dump databáze)</td><td>Hermes záloha řeší agenta, ne vaše weby — ŠipkyLiga má replikaci databáze, weby jsou v gitu</td></tr>
</table>
<div class="code-block"><span class="c"># ukázka cronu: každý den ve 3:30 rychlá záloha, v neděli plná</span>
30 3 * * *   /root/.local/bin/hermes backup --quick --label denni -o /root/zalohy/
30 4 * * 0   /root/.local/bin/hermes backup -o /root/zalohy/ -k 4</div>
<p class="note">Cesty k <code>hermes</code> si ověřte příkazem <code>which hermes</code> — v cronu nebývá
v <code>PATH</code> to, co v interaktivním shellu.</p>

<h2>Časté chyby</h2>
<table class="wiki-tabulka">
<tr><th>Příznak</th><th>Příčina a řešení</th></tr>
<tr><td>Záloha hlásí <code>Backup incomplete</code></td><td>Něco nešlo přečíst (často socket nebo síťový disk). Archiv zůstává; podívejte se, které soubory chybí</td></tr>
<tr><td>Po obnově agent „zapomněl“ pravidelná sezení</td><td>V archivu nebylo <code>cron/</code> (např. se použil export profilu) — cron se klonováním profilu nepřenáší</td></tr>
<tr><td>Obnova skončila kódem 1</td><td>Část souborů se nepřenesla (výpis <code>Warnings</code>) — zkontrolujte, co chybí, než smažete původní data</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/funkce/sezeni/"><strong>Sezení a jejich obnova</strong><span>Co je v state.db a jak se k němu dostat</span></a>
<a href="/wiki/funkce/kontrolni-body/"><strong>Kontrolní body a návrat zpět</strong><span>Vrácení změn v souborech, ne celého agenta</span></a>
<a href="/wiki/zaciname/kdyz-se-neco-pokazi/"><strong>Když se něco pokazí</strong><span>První pomoc, když agent neodpovídá</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/reference/cli-commands" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Příkazy backup, import a restore do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co zálohovat
Vše je v ~/.hermes/: config.yaml, .env, auth.json (nastavení a klíče) · state.db (+ -wal, -shm) = konverzace ·
skills/, memories/ · cron/ (pravidelné úlohy) · SOUL.md a profily.
Víc profilů = víc state.db; zálohujte celé ~/.hermes/, ne jen jeden profil.

## hermes backup
hermes backup [-o cesta] [--quick] [--label jmeno] [-k N] · výchozí cíl ~/hermes-backup-<čas>.zip.
--quick = jen kritické soubory (config.yaml, state.db, .env, auth, cron). -k = po plné záloze nechat N
nejnovějších (výchozí 3; 0 = vše). Kopírování přes SQLite backup() -> bezpečné za běhu (WAL).
Návratové kódy: 0 = kompletní, 1 = část souborů chybí (archiv zůstane, --keep se přeskočí), 2 = běží jiná záloha.
Vyloučeno: kód agenta, models/runtimes/node, keše, checkpoints/, staré zálohy a state-snapshots/, SQLite sidecary.

## Obnova
hermes gateway stop · hermes import <zip> (-f přeskočí potvrzení; archiv se před zápisem kontroluje CRC;
poškozený = nic se nezapíše; částečná obnova = kód 1).
hermes backup restore --state pre-update = vrácení snímku před aktualizací. state-snapshots/ = rychlé snímky.

## backup vs profile export
hermes backup = celý stroj, včetně .env a auth.json -> NIKDY ho neposílejte cizím lidem.
hermes profile export = jeden profil, tar.gz, bez tajemství -> na sdílení.

## Rozbitá sezení
Hláška o staré kopii WAL znamená, že agent přestal psát (data jsou v bezpečí).
1) hermes gateway stop (+ Desktop, dashboard, cron) · 2) hermes doctor vypíše držitele (PID) · 3) spustit znovu.
NIKDY: mazat state.db-wal/-shm · cp state.db samo · doctor --fix za běhu · sessions optimize pod živou branou.
Diagnostika: hermes sessions recover --inspect-only | --output · hermes sessions repair --check-only | repair.

## U nás
--quick před každou aktualizací; denní plná záloha mimo server; obnova se zkouší do zkušebního profilu;
weby mají vlastní zálohu (git, replikace DB). V cronu používejte plnou cestu k hermes (which hermes).
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">💾</span><div><strong>A backup you have never restored is not a backup — it is just a file on a disk.</strong>
Hermes makes this reasonably easy: it can take a consistent backup while running and it refuses a
damaged archive. One thing nobody can do for you: test the restore before you need it.</div></div>

<h2>What to back up</h2>
<p>Everything that matters lives in one folder — the Hermes home directory (<code>~/.hermes/</code>).</p>
<table class="wiki-tabulka">
<tr><th>Item</th><th>Why it matters</th></tr>
<tr><td><code>config.yaml</code>, <code>.env</code>, <code>auth.json</code></td><td>Settings, model keys and sign-in. Without them a restore gives you an empty agent</td></tr>
<tr><td><code>state.db</code> (+ <code>-wal</code>, <code>-shm</code>)</td><td>Every conversation, session and related data</td></tr>
<tr><td><code>skills/</code>, <code>memories/</code></td><td>What the agent learned and what it remembers about you</td></tr>
<tr><td><code>cron/</code></td><td>Scheduled jobs — without them the agent forgets what it does every day</td></tr>
<tr><td><code>SOUL.md</code>, profiles</td><td>The agent's personality and all additional profiles</td></tr>
</table>
<p class="note">With several profiles, each has its own <code>state.db</code> and folder. Backing up the
whole <code>~/.hermes/</code> is therefore safer than copying just “yours”.</p>

<h2>One-command backup</h2>
<div class="code-block"><span class="c"># full backup (default target: ~/hermes-backup-&lt;timestamp&gt;.zip)</span>
hermes backup

<span class="c"># to a specific place you back up elsewhere</span>
hermes backup -o /root/backups/hermes.zip

<span class="c"># quick snapshot of the essentials only (config, state.db, .env, cron)</span>
hermes backup --quick --label "pre-upgrade"

<span class="c"># keep only the newest five full backups</span>
hermes backup -o /root/backups/ -k 5</div>
<table class="wiki-tabulka">
<tr><th>Property</th><th>How it behaves</th></tr>
<tr><td>Safe while running</td><td>Copying goes through SQLite's <code>backup()</code> API, so it is consistent even mid-conversation (WAL mode)</td></tr>
<tr><td>Not in the archive</td><td>The agent code itself, models and runtimes (tens of GB, downloadable again), caches, checkpoints and older backups</td></tr>
<tr><td>Exit status</td><td><code>0</code> = everything included; <code>1</code> = some files were skipped (the zip is kept so the rest can be restored); <code>2</code> = another backup was already running</td></tr>
</table>
<p><strong>Exit code 1 matters:</strong> if a cron job runs the backup, it must be able to tell that the
archive is incomplete. That is also why <code>--keep</code> does not prune older (complete) archives in that case.</p>

<h2>Restore</h2>
<div class="code-block"><span class="c"># restore a whole archive (stop the gateway first)</span>
hermes gateway stop
hermes import /root/backups/hermes.zip

<span class="c"># roll back the snapshot taken before an update</span>
hermes backup restore --state pre-update</div>
<p>The archive is decompressed and CRC-checked before anything is written. A damaged archive stops
with an error and <strong>writes nothing</strong>. Files that could not be restored are listed and the
command exits 1, so a partial restore never reports success.</p>

<h2>Backup versus profile export</h2>
<table class="wiki-tabulka">
<tr><th></th><th><code>hermes backup</code></th><th><code>hermes profile export</code></th></tr>
<tr><td>Use case</td><td>Whole-machine migration, disaster recovery</td><td>Porting or sharing a single profile</td></tr>
<tr><td>Scope</td><td>All profiles, global config, keys, sessions</td><td>One profile: SOUL.md, memory, sessions, skills</td></tr>
<tr><td>Credentials</td><td><strong>Included</strong> (<code>.env</code>, <code>auth.json</code>)</td><td><strong>Excluded</strong> — stripped for safe sharing</td></tr>
<tr><td>Format</td><td><code>.zip</code></td><td><code>.tar.gz</code></td></tr>
</table>
<p class="note">Practical consequence: <strong>never send a <code>hermes backup</code> archive to anyone</strong> —
it contains your keys. Use a profile export for sharing.</p>

<h2>When sessions break (and what never to do)</h2>
<p>Hermes keeps every conversation in one <code>state.db</code> per profile. If you see a message about
“another process holding an old copy of the write-ahead log”, <strong>nothing was lost</strong> — the
agent stopped writing to protect the file. Three steps fix it:</p>
<div class="code-block">1) stop every process of that profile   hermes gateway stop   (and quit Desktop, dashboard, cron)
2) find who still holds the log         hermes doctor         (prints PID and command)
3) start again (one process) and resend the message</div>
<table class="wiki-tabulka">
<tr><th>Never</th><th>Because</th></tr>
<tr><td>Delete <code>state.db-wal</code> or <code>state.db-shm</code></td><td>The log holds conversations not yet in the main file — deleting it loses them for good</td></tr>
<tr><td>Copy <code>state.db</code> on its own with <code>cp</code></td><td>The three files are one image; use <code>hermes backup</code> or <code>hermes sessions recover</code></td></tr>
<tr><td>Run <code>hermes doctor --fix</code> while processes run</td><td>It can become the second writer that caused the problem</td></tr>
<tr><td>Run <code>sessions optimize</code> under a live gateway</td><td>It rewrites the database (VACUUM, index rebuild), so the command detects a writer and refuses — printing the processes that hold it. <code>--dry-run</code> is always allowed; <code>--force</code> works but only when you know those processes are idle</td></tr>
<tr><td><code>sessions prune</code> under a live gateway</td><td>This one is <em>safe</em>: the preview is read-only and the gateway itself does the deleting (skipping sessions with a running turn). It refuses only when no gateway runs and another process holds the database</td></tr>
</table>

<h2>Diagnosing and repairing a damaged file</h2>
<div class="code-block">hermes gateway stop
hermes sessions recover --source ~/.hermes/state.db --inspect-only   <span class="c"># read-only diagnosis</span>
hermes sessions recover --source ~/.hermes/state.db --output ~/recovered-state.db
hermes sessions repair --check-only                                  <span class="c"># what would be repaired</span>
hermes sessions repair                                               <span class="c"># repair (takes its own backup)</span></div>
<p class="note">Next to <code>state.db</code> you may find files such as <code>state.db.pre-update-emergency-*.bak</code>
(a pre-update snapshot) or <code>state.db.corrupt.*.bak</code> (a copy of a damaged file). The first is
useful for recovery; <strong>never</strong> put the second back over <code>state.db</code> — it carries the same damage.</p>

<h2>How we do it on our server</h2>
<table class="wiki-tabulka">
<tr><th>Habit</th><th>Why</th></tr>
<tr><td>Snapshot before every update: <code>hermes backup --quick --label "pre-upgrade"</code></td><td>Rollback is one command and you do not have to work out what changed</td></tr>
<tr><td>Daily full backup off the machine (another folder, another host)</td><td>A backup on the same disk as the data is not a backup</td></tr>
<tr><td>Restores are tested into a <strong>scratch profile</strong>, not production</td><td>You prove the archive works without breaking the running agent</td></tr>
<tr><td>Websites and apps have their own backup (git, database dump)</td><td>The Hermes backup covers the agent, not your sites — ŠipkyLiga replicates its database, sites live in git</td></tr>
</table>
<div class="code-block"><span class="c"># example cron: quick backup daily at 3:30, full backup on Sundays</span>
30 3 * * *   /root/.local/bin/hermes backup --quick --label daily -o /root/backups/
30 4 * * 0   /root/.local/bin/hermes backup -o /root/backups/ -k 4</div>
<p class="note">Check the <code>hermes</code> path with <code>which hermes</code> — cron does not see the
same <code>PATH</code> as your interactive shell.</p>

<h2>Common mistakes</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>Cause and fix</th></tr>
<tr><td>Backup reports <code>Backup incomplete</code></td><td>Something could not be read (often a socket or a network drive). The archive is kept; check which files are listed</td></tr>
<tr><td>The agent “forgot” its scheduled jobs after a restore</td><td><code>cron/</code> was not in the archive (e.g. a profile export was used) — cloning a profile does not move cron jobs</td></tr>
<tr><td>Restore ended with exit code 1</td><td>Some files were not restored (see <code>Warnings</code>) — check what is missing before deleting the original data</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/features/sessions/"><strong>Sessions and recovery</strong><span>What lives in state.db and how to reach it</span></a>
<a href="/en/wiki/features/checkpoints/"><strong>Checkpoints and rollback</strong><span>Undoing file changes, not the whole agent</span></a>
<a href="/en/wiki/getting-started/troubleshooting/"><strong>When something breaks</strong><span>First aid when the agent stops answering</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/reference/cli-commands" target="_blank" rel="noopener"><strong>Official documentation</strong><span>backup, import and restore in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What to back up
Everything lives in ~/.hermes/: config.yaml, .env, auth.json · state.db (+ -wal, -shm) = conversations ·
skills/, memories/ · cron/ · SOUL.md and profiles. Several profiles = several state.db files.

## hermes backup
hermes backup [-o path] [--quick] [--label name] [-k N] · default ~/hermes-backup-<timestamp>.zip.
--quick = critical state only (config.yaml, state.db, .env, auth, cron). -k keeps the newest N full backups
(default 3; 0 = all). Uses SQLite backup() -> consistent while running (WAL safe).
Exit codes: 0 complete, 1 some files skipped (zip kept, --keep skipped), 2 another backup running.
Excluded: agent code, models/runtimes/node, caches, checkpoints/, older backups and state-snapshots/, SQLite sidecars.

## Restore
hermes gateway stop · hermes import <zip> (-f skips the prompt; CRC-checked before writing; damaged archive
writes nothing; partial restore = exit 1). hermes backup restore --state pre-update rolls back the pre-update
snapshot. state-snapshots/ holds quick snapshots.

## backup vs profile export
hermes backup = whole machine incl. .env and auth.json -> never share it.
hermes profile export = single profile, tar.gz, credentials stripped -> safe to share.

## Broken sessions
"Old copy of the write-ahead log" means the agent stopped writing (data is safe).
1) hermes gateway stop (+ Desktop, dashboard, cron) · 2) hermes doctor lists holders (PID) · 3) start again.
NEVER: delete state.db-wal/-shm · cp state.db alone · doctor --fix while running · sessions optimize
under a live gateway. Diagnose: hermes sessions recover --inspect-only | --output · sessions repair --check-only | repair.

## Our practice
--quick before every update; daily full backup off the machine; restores tested into a scratch profile;
sites have their own backup (git, DB replication). In cron use the full path to hermes (which hermes).
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(25)
    stranka = najdi(25)
    assert stranka and stranka["nazev"] == "Zálohy a obnova"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Zálohy a obnova — co zálohovat a jak obnovu vyzkoušet",
        "Co je v domovské složce Hermese důležité, jak vzít konzistentní zálohu za běhu, jak obnovit archiv nebo snímek a co nikdy nedělat se souborem state.db.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Zálohy a obnova",
        "Záloha, kterou jste nikdy nezkusili obnovit, není záloha. Prakticky: co zálohovat, jak obnovit a jak se chovat, když se sezení rozbije.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Zálohy a obnova — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Backups and restore — what to back up and how to test a restore",
        "What matters in the Hermes home directory, how to take a consistent backup while running, how to restore an archive or snapshot and what never to do with state.db.",
        OBRAZEK, "Wiki · Features in depth", "Backups and restore",
        "A backup you have never restored is not a backup. Practical: what to back up, how to restore, and what to do when sessions break.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Backups and restore — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
