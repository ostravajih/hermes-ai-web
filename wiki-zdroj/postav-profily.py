#!/usr/bin/env python3
"""Postaví stránku wiki „Profily a více agentů" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-profiles.md (co je profil, clone, profily vs. pracovní
složka vs. pískoviště, HERMES_HOME vs. HOME), user-guide-multi-profile-gateways.md (jeden
gateway na profil, multiplex, konflikt tokenů), reference-profile-commands.md (příkazy).

Naše zkušenosti: na jednom VPS běží víc profilů vedle sebe (web, agent, bot pro komunitu) a
potkali jsme se s restartovací smyčkou gatewaye i s prázdným nastavením paměti po klonování.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "16. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/profiles"
OBRAZEK = "wiki-profily"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">👥</span><div><strong>Profil je vlastní domov jednoho agenta.</strong>
Vlastní nastavení, vlastní klíče, vlastní paměť, vlastní rozhovory i vlastní skilly. Když chcete
druhého agenta — na jinou práci, pro jiný projekt nebo pro jiného člověka — založíte mu vlastní
profil. <em>Nikdy nespouštějte dva agenty nad jedním profilem.</em></div></div>

<h2>Co profil obsahuje</h2>
<p>Profil je jedna složka v <code>~/.hermes/profiles/<em>název</em>/</code>. Všechno, co agent má,
je v ní pohromadě — proto se dají profily zálohovat, přesouvat i klonovat:</p>
<table class="wiki-tabulka">
<tr><th>Co v profilu je</th><th>K čemu</th></tr>
<tr><td><code>config.yaml</code></td><td>Nastavení: model, nástroje, zázemí terminálu, plánované úlohy</td></tr>
<tr><td><code>.env</code></td><td>Klíče a tajné údaje (API klíče, tokeny)</td></tr>
<tr><td><code>SOUL.md</code></td><td>Jak agent mluví a chová se</td></tr>
<tr><td><code>memories/</code></td><td>Paměť — co si o vás a o práci píše</td></tr>
<tr><td><code>sessions</code> + <code>state.db</code></td><td>Všechny rozhovory a stav agenta</td></tr>
<tr><td><code>skills/</code>, <code>cron/</code>, <code>plugins/</code></td><td>Naučené postupy, pravidelné úlohy, rozšíření</td></tr>
</table>
<p class="note">Složka se počítá za profil jen když v ní leží některý z těchto souborů
(<code>config.yaml</code>, <code>.env</code>, <code>SOUL.md</code>, <code>profile.yaml</code>,
<code>auth.json</code>, <code>state.db</code>). Prázdná složka po logu se ignoruje.</p>

<h2>Založení profilu ve třech krocích</h2>
<ol class="kroky">
<li><p>Vytvořte profil — vznikne i stejnojmenný příkaz:</p>
<div class="code-block"><span class="p">❯</span> hermes profile create coder</div></li>
<li><p>Nastavte mu klíče a model (probíhá v novém profilu, ne v tom stávajícím):</p>
<div class="code-block"><span class="p">❯</span> coder setup</div></li>
<li><p>Pište si s ním. Od téhle chvíle má <code>coder</code> vlastní paměť i historii:</p>
<div class="code-block"><span class="p">❯</span> coder chat</div></li>
</ol>
<p class="note">Když chcete nový profil rovnou s nastavením toho současného, přidejte
<code>--clone</code> (vezme nastavení, klíče, SOUL.md, skilly a paměť).
<code>hermes profile create work --clone</code></p>

<h2>Jak s profilem pracovat</h2>
<table class="wiki-tabulka">
<tr><th>Co chcete</th><th>Příkaz</th></tr>
<tr><td>Spustit cokoli v jiném profilu</td><td><code>hermes -p coder chat</code>, <code>hermes -p coder doctor</code></td></tr>
<tr><td>Krátký dotaz bez otevírání rozhraní</td><td><code>hermes -p work chat -q "Zkontroluj stav serveru"</code></td></tr>
<tr><td>Vypsat profily</td><td><code>hermes profile list</code></td></tr>
<tr><td>Vysvětlit, co je v profilu</td><td><code>hermes profile show coder</code></td></tr>
<tr><td>Kopírovat profil</td><td><code>hermes profile create work-backup --clone-from coder --clone-all</code></td></tr>
<tr><td>Vyexportovat / přenést na jiný stroj</td><td><code>hermes profile export</code> · <code>hermes profile import</code></td></tr>
</table>

<h2>Profil není pískoviště</h2>
<p>Tohle je nejčastější nedorozumění. Profil odděluje <em>stav agenta</em>, ale ne <em>práva</em>:</p>
<table class="wiki-tabulka">
<tr><th>Co</th><th>Čím se řídí</th><th>Co to znamená</th></tr>
<tr><td>Stav (konfigurace, paměť, rozhovory)</td><td>Profil (proměnná <code>HERMES_HOME</code>)</td><td>Dva profily si do sebe nevidí</td></tr>
<tr><td>Kde příkazy startují</td><td><code>terminal.cwd</code> v <code>config.yaml</code></td><td>Agent může klidně pracovat ve vašem projektu; nastavte mu to napevno</td></tr>
<tr><td>Co smí na disku</td><td>Systémová práva uživatele (+ pískoviště, pokud ho zapnete)</td><td>Profil sám přístup neomezí — o tom je stránka Bezpečnost</td></tr>
</table>
<div class="code-block"><span class="c"># ~/.hermes/profiles/coder/config.yaml</span>
terminal:
  backend: local
  cwd: /var/www/muj-projekt</div>
<p class="note"><code>cwd: "."</code> znamená „složka, ze které jsem Hermes spustil“, ne složka profilu.
Ptejte se agenta, ve které složce je — není to spolehlivá zkouška oddělení. Nastavte ji.</p>

<h2>Víc agentů na jednom serveru</h2>
<p>Na jednom VPS takhle běžně vedle sebe žije několik profilů: jeden pro web, jeden pro hlavního
asistenta, jeden pro komunitního bota. Každý má vlastní databázi stavu a vlastní rozhovory.</p>
<table class="wiki-tabulka">
<tr><th>Co hlídat</th><th>Proč a jak</th></tr>
<tr><td><strong>Jeden profil = jeden běžící agent.</strong> Nikdy ne dva procesy nad stejným profilem</td><td>Oba si píšou paměť a každý si při startu načte, co napsal ten druhý — stav se množí, až není jasné, co jste vůbec nastavili</td></tr>
<tr><td>Pro každou platformu správný profil</td><td>Když mají dva profily stejný token bota (např. Discord), perou se o připojení a služba se restartuje pořád dokola</td></tr>
<tr><td>Jeden gateway na profil (nebo multiplex)</td><td>Pro každý profil se dá spustit vlastní gateway; nebo jeden společný s <code>gateway.multiplex_profiles: true</code></td></tr>
<tr><td>Po klonování zkontrolujte paměť</td><td>Když profil používá vnější paměť, ověřte, že její nastavení cestovalo — jinak je paměť <em>tiše vypnutá</em>, agent se jen tváří, že si pamatuje</td></tr>
</table>
<div class="code-block"><span class="p">❯</span> hermes gateway list                    <span class="c"># co na stroji běží</span>
<span class="p">❯</span> hermes -p coder gateway restart        <span class="c"># restart jednoho profilu</span>
<span class="p">❯</span> hermes -p coder logs -f                <span class="c"># živý log profilu</span>
<span class="p">❯</span> hermes gateway migrate --multiplex     <span class="c"># přechod na jeden společný gateway</span></div>

<h2>Když se profil a váš počítač rozcházejí</h2>
<p>Profil je oddělený jen pro Hermese. Nástroje, které používá (git, ssh, gh, npm…), berou
přihlašovací údaje <em>vašeho</em> systémového účtu, takže dva profily na jednom počítači mají
společný GitHub i společný SSH klíč.</p>
<table class="wiki-tabulka">
<tr><th>Chcete</th><th>Nastavení</th></tr>
<tr><td>Aby profily sdílely údaje vašeho účtu (obvyklé a pohodlné)</td><td>Výchozí stav — nic nedělat</td></tr>
<tr><td>Aby měl profil vlastní přihlášení do CLI nástrojů</td><td><code>terminal.home_mode: profile</code> v <code>config.yaml</code> profilu</td></tr>
</table>

<h2>Naše zkušenosti z provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co jsme řešili</th><th>Ponaučení</th></tr>
<tr><td>Na jednom VPS se sešly tři profily a jeden bot. Služba gatewaye se pořád restartovala</td><td>Příčinou byl konflikt tokenu a nedostavěná součást v profilu, ne chyba botu. Pomohlo rozdělit role do profilů a restartovat služby najednou, ne po jedné</td></tr>
<tr><td>Po upgradu se agent tvářil, že si nic nepamatuje</td><td>V profilu bylo prázdné nastavení paměti (<code>memory.provider</code>). U vnější paměti vždycky ověřte nastavení, ne jen že soubor existuje</td></tr>
<tr><td>Web, hlavní asistent a bot pro komunitu běží jako tři profily</td><td>Když jeden upravujete, ostatních se to netýká — a když se něco pokazí, víte, který profil to byl</td></tr>
<tr><td>Dva agenti potřebovali různé projekty ve stejné složce</td><td>Pomohl <code>terminal.cwd</code> v každém profilu. „Ve které složce jsi?“ jako kontrola nestačí</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Profil na projekt, ne na náladu</td><td>Paměť i klíče patří projektu — jinak si agent plete souvislosti</td></tr>
<tr><td>Pojmenujte profily krátce a bez diakritiky</td><td>Název je zároveň příkaz: <code>coder chat</code> se píše snadno, <code>můj-web chat</code> ne</td></tr>
<tr><td>Nové pokusy dělejte v klonu</td><td><code>--clone</code> vám dá kopii, kterou můžete klidně rozbít</td></tr>
<tr><td>Pamatujte, že profil není zeď</td><td>Práva řešte zvlášť — systémovými účty, kontejnerem nebo schvalováním příkazů</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/funkce/nastroje/"><strong>Nástroje a toolsety</strong><span>Co agent umí a kde to běží</span></a>
<a href="/wiki/zaciname/bezpecnost/"><strong>Bezpečnost</strong><span>Klíče, práva a schvalování</span></a>
<a href="/wiki/zaciname/telegram-a-discord/"><strong>Telegram a Discord</strong><span>Připojení agenta k chatu</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/profiles" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Profily do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co je profil
Vlastní domov jednoho agenta: ~/.hermes/profiles/<název>/
Obsahuje config.yaml, .env, SOUL.md, memories/, sessions + state.db, skills/, cron/, plugins/.
Za profil se počítá jen složka s jedním z těchto souborů: config.yaml, .env, SOUL.md, profile.yaml, auth.json, state.db.

## Založení
hermes profile create coder     -> vznikne i příkaz "coder"
coder setup                     -> klíče a model
coder chat                      -> rozhovor s vlastní pamětí a historií
Kopie stávajícího nastavení: hermes profile create work --clone

## Příkazy
hermes -p coder chat · hermes -p work chat -q "..." · hermes profile list · hermes profile show coder ·
hermes profile create work-backup --clone-from coder --clone-all · hermes profile export / import

## Profil není pískoviště
- stav agenta -> profil (HERMES_HOME), profily si do sebe nevidí
- kde příkazy startují -> terminal.cwd v config.yaml (cwd: "." = složka spuštění Hermese)
- co smí na disku -> systémová práva uživatele (+ pískoviště, pokud zapnuté); profil sám neomezuje

## Víc agentů na jednom serveru
Jeden profil = jeden běžící agent (dva procesy nad stejným profilem si množí paměť).
Dva profily se stejným tokenem bota (Discord) se perou o připojení -> služba se restartuje pořád dokola.
Gateway: hermes gateway list · hermes -p coder gateway restart · hermes -p coder logs -f ·
hermes gateway migrate --multiplex (nebo gateway.multiplex_profiles: true)
Po klonování ověřit nastavení vnější paměti (memory.provider) — jinak je paměť tiše vypnutá.

## Sdílení údajů s účtem
Nástroje (git, ssh, gh, npm) berou údaje systémového účtu -> profily je sdílejí.
Vlastní přihlášení pro profil: terminal.home_mode: profile

## Naše zkušenosti
1. Gateway se restartovala pořád dokola kvůli konfliktu tokenu + nedostavěné součásti v profilu;
   pomohlo rozdělení rolí do profilů a restart služeb najednou.
2. Po upgradu se zdálo, že si agent nic nepamatuje -> prázdné memory.provider v profilu.
3. Web, hlavní asistent a komunitní bot = tři profily; úprava jednoho se ostatních netýká.
4. Dvě role se stejným projektem: pomohl terminal.cwd v každém profilu.

## Tipy
Profil na projekt · krátké názvy bez diakritiky (je to i příkaz) · pokusy v klonu · práva řešit
zvlášť (účty, kontejner, schvalování), ne spoléhat na profil.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">👥</span><div><strong>A profile is one agent's own home.</strong>
Its own settings, its own keys, its own memory, conversations and skills. When you want a second
agent — for different work, a different project or a different person — give it its own profile.
<em>Never run two agents against one profile.</em></div></div>

<h2>What a profile contains</h2>
<p>A profile is a single folder in <code>~/.hermes/profiles/<em>name</em>/</code>. Everything the
agent has lives there — which is why profiles can be backed up, moved and cloned:</p>
<table class="wiki-tabulka">
<tr><th>Inside the profile</th><th>What for</th></tr>
<tr><td><code>config.yaml</code></td><td>Settings: model, tools, terminal backend, scheduled jobs</td></tr>
<tr><td><code>.env</code></td><td>Keys and secrets (API keys, tokens)</td></tr>
<tr><td><code>SOUL.md</code></td><td>How the agent talks and behaves</td></tr>
<tr><td><code>memories/</code></td><td>Memory — what it writes down about you and the work</td></tr>
<tr><td><code>sessions</code> + <code>state.db</code></td><td>All conversations and the agent's state</td></tr>
<tr><td><code>skills/</code>, <code>cron/</code>, <code>plugins/</code></td><td>Learned procedures, scheduled jobs, extensions</td></tr>
</table>
<p class="note">A folder counts as a profile only when it holds one of these files
(<code>config.yaml</code>, <code>.env</code>, <code>SOUL.md</code>, <code>profile.yaml</code>,
<code>auth.json</code>, <code>state.db</code>). An empty folder left behind by a log is ignored.</p>

<h2>Creating a profile in three steps</h2>
<ol class="kroky">
<li><p>Create it — a matching command appears as well:</p>
<div class="code-block"><span class="p">❯</span> hermes profile create coder</div></li>
<li><p>Configure its keys and model (this runs inside the new profile, not the current one):</p>
<div class="code-block"><span class="p">❯</span> coder setup</div></li>
<li><p>Start talking to it. From now on <code>coder</code> has its own memory and history:</p>
<div class="code-block"><span class="p">❯</span> coder chat</div></li>
</ol>
<p class="note">To start from your current settings, add <code>--clone</code> (it copies config,
keys, SOUL.md, skills and memory). <code>hermes profile create work --clone</code></p>

<h2>Working with profiles</h2>
<table class="wiki-tabulka">
<tr><th>What you want</th><th>Command</th></tr>
<tr><td>Run anything in another profile</td><td><code>hermes -p coder chat</code>, <code>hermes -p coder doctor</code></td></tr>
<tr><td>A quick question without opening the UI</td><td><code>hermes -p work chat -q "Check the server status"</code></td></tr>
<tr><td>List profiles</td><td><code>hermes profile list</code></td></tr>
<tr><td>Explain what is in a profile</td><td><code>hermes profile show coder</code></td></tr>
<tr><td>Copy a profile</td><td><code>hermes profile create work-backup --clone-from coder --clone-all</code></td></tr>
<tr><td>Export / move to another machine</td><td><code>hermes profile export</code> · <code>hermes profile import</code></td></tr>
</table>

<h2>A profile is not a sandbox</h2>
<p>This is the most common misunderstanding. A profile separates the <em>agent's state</em>, not
its <em>permissions</em>:</p>
<table class="wiki-tabulka">
<tr><th>What</th><th>Controlled by</th><th>What it means</th></tr>
<tr><td>State (config, memory, conversations)</td><td>The profile (<code>HERMES_HOME</code>)</td><td>Two profiles cannot see into each other</td></tr>
<tr><td>Where commands start</td><td><code>terminal.cwd</code> in <code>config.yaml</code></td><td>The agent may well work inside your project; set that folder explicitly</td></tr>
<tr><td>What it may touch on disk</td><td>Your OS user's rights (plus a sandbox if you enable one)</td><td>A profile alone does not restrict anything — that is the Security page</td></tr>
</table>
<div class="code-block"><span class="c"># ~/.hermes/profiles/coder/config.yaml</span>
terminal:
  backend: local
  cwd: /var/www/my-project</div>
<p class="note"><code>cwd: "."</code> means "the folder I launched Hermes from", not the profile
folder. Asking the agent which directory it is in is not a reliable isolation test. Set it.</p>

<h2>Several agents on one server</h2>
<p>On a single VPS it is normal to run several profiles side by side: one for a website, one main
assistant, one community bot. Each has its own state database and its own conversations.</p>
<table class="wiki-tabulka">
<tr><th>What to watch</th><th>Why and how</th></tr>
<tr><td><strong>One profile = one running agent.</strong> Never two processes on the same profile</td><td>Both write memory, and each loads the other's writes at session start — the state compounds until nobody knows what you configured</td></tr>
<tr><td>The right profile per platform</td><td>When two profiles share one bot token (Discord, for example) they fight over the connection and the service restarts in a loop</td></tr>
<tr><td>One gateway per profile (or multiplexing)</td><td>Each profile can run its own gateway; or use one shared gateway with <code>gateway.multiplex_profiles: true</code></td></tr>
<tr><td>Check memory after cloning</td><td>If the profile uses an external memory provider, verify its settings travelled — otherwise memory is <em>silently off</em> and the agent only looks like it remembers</td></tr>
</table>
<div class="code-block"><span class="p">❯</span> hermes gateway list                    <span class="c"># what runs on this machine</span>
<span class="p">❯</span> hermes -p coder gateway restart        <span class="c"># restart one profile</span>
<span class="p">❯</span> hermes -p coder logs -f                <span class="c"># live log for a profile</span>
<span class="p">❯</span> hermes gateway migrate --multiplex     <span class="c"># move to one shared gateway</span></div>

<h2>Where a profile and your machine mix</h2>
<p>A profile is separated only for Hermes itself. The tools it uses (git, ssh, gh, npm…) take the
credentials of <em>your</em> system account, so two profiles on one machine share your GitHub and
your SSH key.</p>
<table class="wiki-tabulka">
<tr><th>You want</th><th>Setting</th></tr>
<tr><td>Profiles to share your account's credentials (usual and convenient)</td><td>The default — do nothing</td></tr>
<tr><td>A profile with its own CLI logins</td><td><code>terminal.home_mode: profile</code> in that profile's <code>config.yaml</code></td></tr>
</table>

<h2>What we learned running this</h2>
<table class="wiki-tabulka">
<tr><th>What we dealt with</th><th>The lesson</th></tr>
<tr><td>Three profiles and one bot on a single VPS. The gateway service kept restarting</td><td>The cause was a token conflict plus an unfinished component in the profile, not the bot. Splitting roles into profiles and restarting services together fixed it</td></tr>
<tr><td>After an upgrade the agent acted as if it remembered nothing</td><td>The profile had an empty memory setting (<code>memory.provider</code>). With external memory, always verify the setting, not just that the file exists</td></tr>
<tr><td>The website, the main assistant and the community bot run as three profiles</td><td>Editing one does not touch the others — and when something breaks, you know which profile it was</td></tr>
<tr><td>Two agents needed different projects in the same folder</td><td><code>terminal.cwd</code> per profile did it. "Which folder are you in?" is not a sufficient check</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>A profile per project, not per mood</td><td>Memory and keys belong to a project — otherwise the agent mixes contexts up</td></tr>
<tr><td>Name profiles short and plain ASCII</td><td>The name is also a command: <code>coder chat</code> is easy, a name with accents is not</td></tr>
<tr><td>Try things in a clone</td><td><code>--clone</code> gives you a copy you can safely break</td></tr>
<tr><td>Remember a profile is not a wall</td><td>Handle permissions separately — OS accounts, a container or command approval</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/features/tools/"><strong>Tools and toolsets</strong><span>What the agent can do and where it runs</span></a>
<a href="/en/wiki/getting-started/security/"><strong>Security</strong><span>Keys, permissions and approvals</span></a>
<a href="/en/wiki/getting-started/telegram-and-discord/"><strong>Telegram and Discord</strong><span>Connecting the agent to chat</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/profiles" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Profiles in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What a profile is
One agent's own home: ~/.hermes/profiles/<name>/
Contains config.yaml, .env, SOUL.md, memories/, sessions + state.db, skills/, cron/, plugins/.
A folder counts as a profile only with one of: config.yaml, .env, SOUL.md, profile.yaml, auth.json, state.db.

## Creating one
hermes profile create coder     -> also creates the "coder" command
coder setup                     -> keys and model
coder chat                      -> a conversation with its own memory and history
Copy of current settings: hermes profile create work --clone

## Commands
hermes -p coder chat · hermes -p work chat -q "..." · hermes profile list · hermes profile show coder ·
hermes profile create work-backup --clone-from coder --clone-all · hermes profile export / import

## A profile is not a sandbox
- agent state -> the profile (HERMES_HOME); profiles cannot see into each other
- where commands start -> terminal.cwd in config.yaml ("." = the launch folder)
- what it may touch -> your OS user's rights (+ sandbox if enabled); a profile alone restricts nothing

## Several agents on one server
One profile = one running agent (two processes on one profile compound memory).
Two profiles sharing one bot token (Discord) fight over the connection -> the service restarts in a loop.
Gateway: hermes gateway list · hermes -p coder gateway restart · hermes -p coder logs -f ·
hermes gateway migrate --multiplex (or gateway.multiplex_profiles: true)
After cloning, verify external memory settings (memory.provider) — otherwise memory is silently off.

## Credentials shared with your account
Tools (git, ssh, gh, npm) use your system account's credentials -> profiles share them.
Separate CLI logins per profile: terminal.home_mode: profile

## What we learned
1. A restarting gateway was caused by a token conflict plus an unfinished component in the profile;
   splitting roles into profiles and restarting services together fixed it.
2. After an upgrade the agent seemed to remember nothing -> empty memory.provider in the profile.
3. Website, main assistant and community bot are three profiles; editing one leaves the others alone.
4. Two roles needing the same project folder: terminal.cwd per profile.

## Tips
A profile per project · short ASCII names (the name is a command) · experiment in a clone · handle
permissions separately (accounts, container, approval), do not rely on the profile.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(14)
    stranka = najdi(14)
    assert stranka and stranka["nazev"] == "Profily a více agentů"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Profily a více agentů — víc agentů na jednom počítači",
        "Jak založit druhého agenta s vlastní pamětí, klíči a nastavením, jak se profily liší od pískoviště a na co si dát pozor při více agentech na jednom serveru.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Profily a více agentů",
        "Druhý agent pro jinou práci není druhý server — stačí mu vlastní profil. Tady je jak na to a kde se profily pletou s právy.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Profily a více agentů — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Profiles and multiple agents — several agents on one machine",
        "How to create a second agent with its own memory, keys and settings, how profiles differ from sandboxes, and what to watch with several agents on one server.",
        OBRAZEK, "Wiki · Features in depth", "Profiles and multiple agents",
        "A second agent for different work is not a second server — it just needs its own profile. Here is how, and where profiles get confused with permissions.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Profiles and multiple agents — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
