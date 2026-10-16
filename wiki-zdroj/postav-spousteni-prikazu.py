#!/usr/bin/env python3
"""Postaví stránku wiki „Spouštění příkazů a schvalování" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-security.md (režimy schvalování, YOLO, ochrana zápisu
do souborů, srovnání terminálových backendů), user-guide-features-code-execution.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/security"
OBRAZEK = "wiki-spousteni"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🛂</span><div><strong>Než agent spustí příkaz, projde kontrolou. Buď se rozhodne sám, nebo se zeptá vás — podle toho, jak si to nastavíte.</strong>
Tahle stránka je o tom, jak nastavit, aby agent v běžné práci neotravoval a přitom nemohl smazat
server. A taky o tom, že <em>zápis do souborů má vlastní pravidla</em>, na která se nikdo neptá.</div></div>

<h2>Kdy se agenta nezeptá a kdy ano</h2>
<table class="wiki-tabulka">
<tr><th>Režim</th><th>Co dělá</th><th>Pro koho</th></tr>
<tr><td><strong>smart</strong> (výchozí)</td><td>Pomocný model posoudí riziko: jasně bezpečný příkaz povolí pro ten jeden případ, opravdu nebezpečný sám zamítne a u nejasných se zeptá</td><td>Běžná práce — nejlepší kompromis</td></tr>
<tr><td><strong>manual</strong></td><td>Zeptá se pokaždé, když jde o nebezpečný příkaz</td><td>Když chcete mít přehled o každém rizikovém kroku</td></tr>
<tr><td><strong>off</strong></td><td>Vypne všechny kontroly (obdoba <code>--yolo</code>)</td><td>Jen v izolovaném prostředí, kde nic nemůže utéct</td></tr>
</table>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
approvals:
  mode: smart                <span class="c"># smart | manual | off</span>
  timeout: 300               <span class="c"># kolik vteřin čeká na vaše rozhodnutí</span>
  cron_mode: deny            <span class="c"># co mají dělat pravidelné úlohy bez dozoru</span>
  single_query_mode: deny    <span class="c"># jednorázová spuštění (hermes chat -q)</span>
  unattended_mode: deny      <span class="c"># webhooky a rozhraní bez člověka u klávesnice</span></div>

<h2>Když nemá kdo odklikat „povolit“</h2>
<p>Noční úloha nebo webhook nemá nikoho, kdo by na dotaz odpověděl. Proto mají tyhle situace vlastní
nastavení: <code>deny</code> (výchozí) příkaz <strong>zablokuje</strong> a agent musí hledat jinou
cestu; <code>approve</code> všechno dopředu povolí.</p>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Nastavení</th><th>Výchozí</th></tr>
<tr><td>Pravidelná úloha (cron)</td><td><code>cron_mode</code></td><td>zablokovat</td></tr>
<tr><td>Jednorázový příkaz <code>hermes chat -q</code></td><td><code>single_query_mode</code></td><td>zablokovat</td></tr>
<tr><td>Webhook, API bez obsluhy</td><td><code>unattended_mode</code></td><td>zablokovat</td></tr>
</table>
<p class="note">Tohle je důležité pro pochopení tichých problémů: když noční úloha narazí na
nebezpečný příkaz a nikdo neklikne, <strong>úloha se prostě nedokončí</strong> a v logu zůstane
zamítnutí. Když takovou úlohu chcete, navrhněte ji tak, aby zvládla i zablokování.</p>

<h2>YOLO režim (vše bez ptaní)</h2>
<table class="wiki-tabulka">
<tr><th>Jak</th><th>Rozsah</th></tr>
<tr><td><code>hermes --yolo</code> nebo <code>hermes chat --yolo</code></td><td>Celé spuštění</td></tr>
<tr><td><code>/yolo</code> v rozhovoru</td><td>Od té chvíle do konce sezení</td></tr>
</table>
<p class="note">Nikdy ho nezapínejte tam, kde agent pracuje na živém webu nebo kde jsou vaše klíče
a přístupy. V izolovaném kontejneru nebo v testovacím projektu je to naopak rozumná volba.</p>

<h2>Zápis do souborů: tady se neptá, tady se rovnou blokuje</h2>
<p>U zápisu do souboru není žádné okno „povolit". Hermes zkontroluje cestu proti seznamu chráněných
míst a když na nějaké narazí, zápis <strong>odmítne</strong> — bez možnosti to z chatu obejít:</p>
<table class="wiki-tabulka">
<tr><th>Chráněno vždy</th><th>Příklady</th></tr>
<tr><td>Přístupy k systému a cloudu</td><td>Klíče SSH, <code>authorized_keys</code>, přístupy k AWS a Kubernetes, nastavení <code>sudoers</code></td></tr>
<tr><td>Tajemství samotného Hermese</td><td><code>.env</code>, přihlašovací soubory, trezor, profil prohlížeče, tokeny pro nástroje, párovací soubory</td></tr>
<tr><td>Soubory s přihlašovacími údaji v projektu</td><td><code>.env.local</code>, <code>.env.production</code>, <code>.envrc</code> — agent je <em>nesmí přečíst</em>, ale může je pro vás napsat</td></tr>
</table>
<p>Hranici zápisu navíc můžete omezit na jedinou složku — pak agent nesmí zapsat nic mimo ni
(<code>HERMES_WRITE_SAFE_ROOT</code>). Chráněná místa výše zůstávají blokovaná, i kdyby byla uvnitř té
složky.</p>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⚠️</span><div><strong>Pozor na tichý omyl:</strong>
když je zápis zablokovaný, agent to dostane jako chybu — ale ve shrnutí může přesto napsat, že se to
povedlo. Věnovat pozornost patičce, kde se ověření zápisu hlásí, vyplatí se víc než věřit poslední
větě odpovědi.</div></div>

<h2>Kde agent běží a co to znamená pro kontrolu</h2>
<table class="wiki-tabulka">
<tr><th>Kde terminál běží</th><th>Kontrola nebezpečných příkazů</th><th>Pro co se hodí</th></tr>
<tr><td>Na vašem počítači</td><td>ano</td><td>Vývoj a běžná práce</td></tr>
<tr><td>Na vzdáleném serveru přes SSH</td><td>ano</td><td>Práce na serveru</td></tr>
<tr><td>V kontejneru (Docker a podobně)</td><td><strong>přeskočena</strong> — hranicí je kontejner</td><td>Nepřetržitý provoz, když je vše izolované</td></tr>
<tr><td>V cloudovém sandboxu (Modal, Daytona, Vercel)</td><td><strong>přeskočena</strong></td><td>Práce, která má zmizet se strojem</td></tr>
</table>
<p class="note">Přeskočená kontrola není chyba — jen to znamená, že ochranou je izolace kontejneru,
ne dotazy. Zkontrolujte, co všechno je do kontejneru připojené (složky, klíče, síť).</p>

<h2>Pasti z našeho provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co se stalo</th><th>Co s tím</th></tr>
<tr><td><strong>Noční úloha se tiše nedokončila</strong></td><td>Narazila na nebezpečný příkaz a nebyl kdo schválit → výchozí chování je zablokovat. Úlohu navrhněte tak, aby zvládla jinou cestu, nebo jí povolení přiznejte vědomě</td></tr>
<tr><td><strong>Agent tvrdil, že soubor uložil, ale neuložil</strong></td><td>Zápis byl zablokovaný (chráněná cesta nebo mimo povolenou složku). Kontrolujte patičku s ověřením zápisu, ne shrnutí odpovědi</td></tr>
<tr><td><strong>Agent nemohl přečíst <code>.env</code></strong></td><td>Správně — soubory s přihlašovacími údaji se nečtou. Když potřebujete hodnotu použít, zadejte ji agentovi jako nastavení, ne jako obsah souboru</td></tr>
<tr><td><strong>Zapnuté „vše povolit“ na produkčním serveru</strong></td><td>Nedělejte to. Když už to nutně potřebujete, jen na omezenou dobu a s vědomím, že agent může sáhnout na cokoli</td></tr>
<tr><td><strong>Schválení vypršelo, protože jsme byli pryč</strong></td><td>Výchozí čekání je 5 minut. Buď se k rozhodnutí vraťte, nebo zvolte režim, který se neptá (a nést jeho riziko)</td></tr>
<tr><td><strong>Přesun do kontejneru zrušil i kontrolní body</strong></td><td>V kontejneru se cesty týkají kontejneru, takže snímky nejdou. V kontejnerovém režimu se spolehněte na git a zálohy</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Nechte <code>smart</code>, dokud nemáte důvod ho měnit</td><td>Většinu rutiny povolí a u opravdu riskantních věcí se zastaví</td></tr>
<tr><td>Hranici zápisu nastavte na složku projektu</td><td>Agent pak nemůže zapsat mimo ni, i kdyby se spletl</td></tr>
<tr><td>U pravidelných úloh počítejte s možností zamítnutí</td><td>Úloha má umět pokračovat i bez povolení, jinak bude tiše selhávat</td></tr>
<tr><td>Nikdy nevypínejte kontroly „na zkoušku“ na živém systému</td><td>Riziko se projeví jednou a nevratně</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/bezpecnost/"><strong>Bezpečnost</strong><span>Kdo smí agenta ovládat a co smí</span></a>
<a href="/wiki/funkce/kontrolni-body/"><strong>Kontrolní body a návrat zpět</strong><span>Když i povolený krok byl omyl</span></a>
<a href="/wiki/zaciname/pravidelne-ulohy/"><strong>Pravidelné úlohy (cron)</strong><span>Práce bez dozoru, ale bezpečně</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/security" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Schvalování a ochrany do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Režimy schvalování (approvals.mode)
smart (výchozí) = pomocný model posoudí riziko: bezpečné povolí pro ten příkaz, nebezpečné zamítne,
nejasné se zeptá · manual = vždy se zeptá · off = bez kontrol (obdoba --yolo).

config.yaml:
approvals:
  mode: smart | manual | off
  timeout: 300               # vteřin na odpověď
  cron_mode: deny            # pravidelné úlohy bez dozoru
  single_query_mode: deny    # hermes chat -q
  unattended_mode: deny      # webhook / API bez člověka
  mcp_reload_confirm: true
  destructive_slash_confirm: true
deny = příkaz zablokován (agent hledá jinou cestu), approve = vše dopředu povoleno.
Bez obsluhy: úloha se tiše nedokončí, v logu zůstane zamítnutí.

## YOLO
hermes --yolo / hermes chat --yolo = celé spuštění; /yolo v rozhovoru = do konce sezení.
Nikdy na živém webu nebo tam, kde jsou klíče.

## Zápis do souborů
Žádný dotaz — chráněné cesty se rovnou blokují: SSH klíče a authorized_keys, AWS, Kubernetes,
sudoers, .env a přihlašovací soubory Hermese (trezor, profil prohlížeče, tokeny, párování).
.env/.env.local/.env.production/.envrc na disku = nelze přečíst, ale lze zapsat.
HERMES_WRITE_SAFE_ROOT = povolená složka; chráněné cesty uvnitř zůstávají blokované.
Pozor: model může tvrdit, že zápis proběhl, i když byl blokován — věřit ověření v patičce.

## Backendy a kontrola příkazů
local = kontrola ano, ssh = ano, docker/singularity/modal/daytona/vercel_sandbox = přeskočena
(hranicí je kontejner). V kontejneru navíc nejdou kontrolní body.

## Pasti z našeho provozu
1. Noční úloha se tiše nedokončila (nebezpečný příkaz + nikdo neklikl -> deny).
2. Agent tvrdil uložení, zápis byl přitom blokovaný.
3. Agent nemohl přečíst .env -> správně; hodnoty zadávat jako nastavení.
4. "Vše povolit" na produkci -> nedělat.
5. Schválení vypršelo (výchozí 300 s).
6. Kontejner zrušil i kontrolní body -> spoléhat na git a zálohy.

## Tipy
Zůstat u smart · hranice zápisu na složku projektu · u pravidelných úloh počítat se zamítnutím ·
nevypínat kontroly na živém systému.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🛂</span><div><strong>Before the agent runs a command it goes through a check. Either it decides on its own or it asks you — depending on your settings.</strong>
This page is about setting things up so the agent does not nag during ordinary work while still
being unable to wipe the server. And about the fact that <em>writing files has its own rules</em>,
which nobody is asked about.</div></div>

<h2>When it asks and when it does not</h2>
<table class="wiki-tabulka">
<tr><th>Mode</th><th>What it does</th><th>Who it is for</th></tr>
<tr><td><strong>smart</strong> (default)</td><td>An auxiliary model assesses the risk: a clearly safe command is approved for that one case, a genuinely dangerous one is auto-denied and uncertain ones escalate to you</td><td>Everyday work — the best compromise</td></tr>
<tr><td><strong>manual</strong></td><td>Always asks when a dangerous command comes up</td><td>When you want to see every risky step</td></tr>
<tr><td><strong>off</strong></td><td>Disables all checks (the same as <code>--yolo</code>)</td><td>Only in an isolated environment where nothing can escape</td></tr>
</table>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
approvals:
  mode: smart                <span class="c"># smart | manual | off</span>
  timeout: 300               <span class="c"># seconds to wait for your decision</span>
  cron_mode: deny            <span class="c"># what scheduled jobs do unattended</span>
  single_query_mode: deny    <span class="c"># one-shot runs (hermes chat -q)</span>
  unattended_mode: deny      <span class="c"># webhooks and interfaces with nobody present</span></div>

<h2>When nobody is around to click "approve"</h2>
<p>A nightly job or a webhook has nobody to answer the prompt. Those situations therefore have their
own setting: <code>deny</code> (the default) <strong>blocks</strong> the command and the agent must
find another path; <code>approve</code> approves everything up front.</p>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>Setting</th><th>Default</th></tr>
<tr><td>Scheduled job (cron)</td><td><code>cron_mode</code></td><td>block</td></tr>
<tr><td>One-shot command <code>hermes chat -q</code></td><td><code>single_query_mode</code></td><td>block</td></tr>
<tr><td>Webhook, unattended API</td><td><code>unattended_mode</code></td><td>block</td></tr>
</table>
<p class="note">This matters for silent problems: when a nightly job hits a dangerous command and
nobody clicks, <strong>the job simply does not finish</strong> and the refusal stays in the log. If
you want such a job, design it to cope with being blocked.</p>

<h2>YOLO mode (everything without asking)</h2>
<table class="wiki-tabulka">
<tr><th>How</th><th>Scope</th></tr>
<tr><td><code>hermes --yolo</code> or <code>hermes chat --yolo</code></td><td>The whole run</td></tr>
<tr><td><code>/yolo</code> in a conversation</td><td>From that moment until the session ends</td></tr>
</table>
<p class="note">Never enable it where the agent works on a live site or where your keys and
credentials live. In an isolated container or a scratch project it is a sensible choice.</p>

<h2>Writing files: no prompt here, it is blocked outright</h2>
<p>For file writes there is no "allow" dialog. Hermes checks the path against a list of protected
places and <strong>refuses</strong> the write — with no way to override it from the chat:</p>
<table class="wiki-tabulka">
<tr><th>Always protected</th><th>Examples</th></tr>
<tr><td>Access to the system and the cloud</td><td>SSH keys, <code>authorized_keys</code>, AWS and Kubernetes credentials, <code>sudoers</code></td></tr>
<tr><td>Hermes' own secrets</td><td><code>.env</code>, sign-in files, the vault, the browser profile, tool tokens, pairing files</td></tr>
<tr><td>Credential files inside a project</td><td><code>.env.local</code>, <code>.env.production</code>, <code>.envrc</code> — the agent <em>must not read</em> them, but it can write them for you</td></tr>
</table>
<p>You can also narrow the write boundary to a single folder — then the agent may not write outside
it (<code>HERMES_WRITE_SAFE_ROOT</code>). The protected places above stay blocked even if they sit
inside that folder.</p>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⚠️</span><div><strong>Watch out for a silent mistake:</strong>
when a write is blocked the agent gets an error — yet its summary may still claim the edit succeeded.
Trusting the write-verification footer pays off more than trusting the closing sentence.</div></div>

<h2>Where the agent runs, and what that means for checks</h2>
<table class="wiki-tabulka">
<tr><th>Where the terminal runs</th><th>Dangerous command check</th><th>What it suits</th></tr>
<tr><td>On your computer</td><td>yes</td><td>Development and everyday work</td></tr>
<tr><td>On a remote server over SSH</td><td>yes</td><td>Working on a server</td></tr>
<tr><td>In a container (Docker and similar)</td><td><strong>skipped</strong> — the container is the boundary</td><td>Always-on operation once everything is isolated</td></tr>
<tr><td>In a cloud sandbox (Modal, Daytona, Vercel)</td><td><strong>skipped</strong></td><td>Work that should vanish with the machine</td></tr>
</table>
<p class="note">A skipped check is not a bug — it just means isolation, not prompts, is the
protection. Check what is mounted into the container (folders, keys, network).</p>

<h2>Pitfalls from our systems</h2>
<table class="wiki-tabulka">
<tr><th>What happened</th><th>What to do</th></tr>
<tr><td><strong>A nightly job quietly did not finish</strong></td><td>It hit a dangerous command with nobody to approve → the default is to block. Design the job to have another path, or grant it permission deliberately</td></tr>
<tr><td><strong>The agent claimed it saved a file but did not</strong></td><td>The write was blocked (protected path or outside the safe root). Check the write-verification footer, not the summary</td></tr>
<tr><td><strong>The agent could not read <code>.env</code></strong></td><td>That is correct — credential files are not readable. When a value is needed, supply it as configuration rather than as file contents</td></tr>
<tr><td><strong>Someone enabled "allow everything" on a production server</strong></td><td>Do not. If you must, only for a limited time and knowing the agent can touch anything</td></tr>
<tr><td><strong>An approval expired because we were away</strong></td><td>The default wait is 5 minutes. Either come back to decide or pick a mode that does not ask (and own its risk)</td></tr>
<tr><td><strong>Moving into a container killed checkpoints too</strong></td><td>Inside a container paths belong to the container, so snapshots do not work. In container mode rely on git and backups</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Keep <code>smart</code> until you have a reason to change it</td><td>It approves most routine work and stops on truly risky things</td></tr>
<tr><td>Point the write boundary at your project folder</td><td>The agent then cannot write outside it, even by mistake</td></tr>
<tr><td>Assume scheduled jobs can be blocked</td><td>A job must cope without approval, or it will fail silently</td></tr>
<tr><td>Never switch checks off "just to try" on a live system</td><td>The risk shows up once and irreversibly</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/security/"><strong>Security</strong><span>Who may drive the agent and what it may do</span></a>
<a href="/en/wiki/features/checkpoints/"><strong>Checkpoints and rollback</strong><span>When even an approved step was a mistake</span></a>
<a href="/en/wiki/getting-started/scheduled-tasks/"><strong>Scheduled tasks (cron)</strong><span>Unattended work, done safely</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/security" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Approvals and safeguards in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Approval modes (approvals.mode)
smart (default) = an auxiliary model assesses risk: safe commands approved for that case, dangerous
ones auto-denied, uncertain ones escalate to you · manual = always asks · off = no checks (= --yolo).

config.yaml:
approvals:
  mode: smart | manual | off
  timeout: 300               # seconds to answer
  cron_mode: deny            # scheduled jobs unattended
  single_query_mode: deny    # hermes chat -q
  unattended_mode: deny      # webhook / API with no human
  mcp_reload_confirm: true
  destructive_slash_confirm: true
deny = command blocked (agent finds another path), approve = everything pre-approved.
Unattended: the job silently does not finish; the refusal stays in the log.

## YOLO
hermes --yolo / hermes chat --yolo = whole run; /yolo in a session = until it ends.
Never on a live site or where keys live.

## File writes
No prompt — protected paths are blocked outright: SSH keys and authorized_keys, AWS, Kubernetes,
sudoers, Hermes .env and credential stores (vault, browser profile, tokens, pairing).
.env/.env.local/.env.production/.envrc on disk = read-denied but writable.
HERMES_WRITE_SAFE_ROOT = allowed folder; protected paths inside stay blocked.
Note: the model may claim a write succeeded even when blocked — trust the verification footer.

## Backends and command checks
local = check yes, ssh = yes, docker/singularity/modal/daytona/vercel_sandbox = skipped (the
container is the boundary). Inside a container checkpoints do not work either.

## Pitfalls from our systems
1. A nightly job quietly did not finish (dangerous command + nobody to approve -> deny).
2. The agent claimed a save that was actually blocked.
3. The agent could not read .env -> correct; supply values as configuration.
4. "Allow everything" on production -> do not.
5. An approval expired (default 300 s).
6. A container killed checkpoints too -> rely on git and backups.

## Tips
Stay on smart · point the write boundary at the project folder · assume scheduled jobs can be blocked ·
never disable checks on a live system.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(23)
    stranka = najdi(23)
    assert stranka and stranka["nazev"] == "Spouštění příkazů a schvalování"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Spouštění příkazů a schvalování — kdy se agent zeptá",
        "Tři režimy schvalování, co dělat u pravidelných úloh bez dozoru, YOLO režim, chráněné cesty u zápisu do souborů a proč agent někdy tvrdí, že něco uložil, a přitom neuložil.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Spouštění příkazů a schvalování",
        "Jak nastavit, aby agent v běžné práci neotravoval, a přitom nemohl smazat server. Včetně toho, co se děje u úloh bez dozoru.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Spouštění příkazů a schvalování — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Running commands and approvals — when the agent asks",
        "The three approval modes, what to do about unattended scheduled jobs, YOLO mode, protected paths for file writes and why the agent sometimes claims a save it never made.",
        OBRAZEK, "Wiki · Features in depth", "Running commands and approvals",
        "How to keep the agent from nagging during ordinary work while it still cannot wipe the server. Including what happens with unattended jobs.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Running commands and approvals — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
