#!/usr/bin/env python3
"""Postaví stránku wiki „Desktop" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-desktop.md (co je v aplikaci, projekty a prohledávání
repozitářů, okna/taby/panely, terminál, živí podagenti, nastavení pro víc profilů, připojení ke
vzdálenému backendu, řešení potíží), user-guide-multi-connection-desktop.md.

Naše zkušenosti: aplikace po aktualizaci zmizí, dokud ji znovu nespustíte; stav se s terminálem
sdílí, takže rozhovor jde začít na serveru a dokončit v aplikaci.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "16. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/desktop"
OBRAZEK = "wiki-desktop"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🖥️</span><div><strong>Aplikace není jiný agent — je to jiné okno k tomu samému.</strong>
Stejné nastavení, stejné klíče, stejná paměť, stejné rozhovory, stejné skilly. Co uděláte
v terminálu, uvidíte v aplikaci, a naopak.</div></div>

<h2>Kdy se hodí</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Proč aplikace</th></tr>
<tr><td>Chcete vidět, co agent dělá</td><td>Průběh odpovědi i každé volání nástroje je vidět v přehledné podobě, včetně obrázků</td></tr>
<tr><td>Pracujete na víc věcech najednou</td><td>Víc oken a panelů: jeden rozhovor na jednom monitoru, druhý na jiném</td></tr>
<tr><td>Potřebujete soubory a terminál po ruce</td><td>Vedle chatu je prohlížeč souborů a skutečný terminál — bez přepínání oken</td></tr>
<tr><td>Nechcete psát příkazy</td><td>Nastavení se dělá v přehledných stránkách, ne v souboru s nastavením</td></tr>
<tr><td>Spravujete víc agentů</td><td>Volitelné okno „Applies to“ říká, kterého profilu se změna v nastavení týká</td></tr>
</table>

<h2>Instalace a spuštění</h2>
<p>Aplikace se stahuje z webu projektu, ale když už Hermes na počítači máte, stačí jeden příkaz —
použije vaše klíče, rozhovory i skilly:</p>
<div class="code-block"><span class="p">❯</span> hermes desktop
<span class="p">❯</span> hermes desktop --cwd /cesta/k/projektu    <span class="c"># otevřít rovnou v projektu</span></div>
<p>Běží na <strong>macOS</strong>, <strong>Windows</strong> i <strong>Linuxu</strong>. Na počítači
s Windows je potřeba Git a pro připojení na vzdálený stroj SSH klient.</p>

<h2>Co v aplikaci najdete</h2>
<table class="wiki-tabulka">
<tr><th>Část</th><th>K čemu slouží</th></tr>
<tr><td><strong>Chat</strong> (střed)</td><td>Rozhovor s agentem, průběh nástrojů, přílohy přetažením, obnovené neodeslané zprávy</td></tr>
<tr><td><strong>Postranní sloupec</strong></td><td>Seznam rozhovorů, projektů a nastavení; přepínání profilů</td></tr>
<tr><td><strong>Náhled vpravo</strong></td><td>Zobrazení souborů, výsledků nástrojů a webových stránek, na kterých agent pracuje</td></tr>
<tr><td><strong>Terminál vpravo</strong></td><td>Skutečný terminál: <code>Ctrl</code>+<code>`</code> ho otevře, další <code>Ctrl</code>+<code>Shift</code>+<code>`</code>. Běží dál, i když panel schováte</td></tr>
<tr><td><strong>Výstupy práce (artefakty)</strong></td><td>Hotové soubory a náhledy nad psacím polem — kliknutím se otevřou</td></tr>
<tr><td><strong>Živí podagenti</strong></td><td>Pruh s počtem a stavem pracujících pomocníků, s možností do jejich práce mluvit nebo je zastavit</td></tr>
</table>

<h2>Práce na víc věcech najednou</h2>
<table class="wiki-tabulka">
<tr><th>Klávesa</th><th>Co udělá</th></tr>
<tr><td><code>Ctrl</code>+<code>T</code></td><td>Nový rozhovor v nové kartě</td></tr>
<tr><td><code>Ctrl</code>+<code>Tab</code></td><td>Přepínání mezi rozhovory</td></tr>
<tr><td><code>Ctrl</code>+<code>1</code>…<code>9</code></td><td>Skok na rozhovor podle pořadí</td></tr>
<tr><td><code>Ctrl</code>+<code>Shift</code>+<code>N</code></td><td>Nové okno — hodí se pro dlouhou úlohu na druhý monitor</td></tr>
<tr><td><code>Ctrl</code>+<code>B</code> / <code>Ctrl</code>+<code>J</code></td><td>Skrytí levého / pravého sloupce (víc místa pro chat)</td></tr>
</table>
<p class="note">Na macOS je místo <code>Ctrl</code> klávesa <code>Cmd</code>.</p>

<h2>Projekty</h2>
<p>Aplikace umí pracovat s víc projekty vedle sebe. Složky s projekty hledá při startu — ve vaší
domovské složce do omezené hloubky. Hledání se dá vypnout nebo omezit:</p>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml — nastavení prohledávání složek</span>
repo_scan_enabled: false        <span class="c"># ať se domovská složka vůbec neprohledává</span></div>
<p>Složku, ve které má agent pracovat, můžete určit i při spuštění (<code>--cwd</code>) nebo trvale
přes <code>terminal.cwd</code> v nastavení profilu — viz
<a href="/wiki/funkce/profily/">Profily a více agentů</a>.</p>

<h2>Víc profilů v jedné aplikaci</h2>
<p>Máte-li víc profilů (třeba jeden pro práci a jeden pro osobní věci), nemusíte přepínat celou
aplikaci. Stránky nastavení mají nahoře přepínač <strong>„Applies to“</strong>, kterým určíte,
kterého profilu se změna týká.</p>
<div class="code-block"><span class="p">❯</span> <code>Cmd</code>/<code>Ctrl</code>+<code>K</code> → Export profile…   <span class="c"># celý profil do jednoho souboru</span></div>
<p class="note">Export obsahuje skilly, paměť, osobnost, plánované úlohy a nastavení —
<strong>API klíče se do exportu nedávají</strong>, ty se doplňují až na cílovém počítači. Hodí se
na přenos nastavení na jiný počítač nebo na sdílení s kolegou.</p>

<h2>Agent na serveru, aplikace u vás</h2>
<p>Aplikace umí běžet i tak, že sama nic nepočítá a jen se připojí k agentovi na serveru (VPS,
domácí server, malý počítač doma). Nastavuje se to na jedné stránce <strong>Nastavení → Gateways</strong>:</p>
<table class="wiki-tabulka">
<tr><th>Možnost</th><th>Co to znamená</th></tr>
<tr><td>Místní agent</td><td>Výchozí: aplikace si agenta spouští sama na vašem počítači</td></tr>
<tr><td>Vzdálený agent</td><td>Zadáte adresu serveru, na kterém běží <code>hermes serve</code>, a přihlásíte se</td></tr>
<tr><td>Hermes Cloud</td><td>Přihlášení a výběr agenta z vašeho účtu — bez zadávání adresy</td></tr>
</table>
<p class="note">Připojení k serveru je věc počítače, ne profilu: z jednoho počítače se dá připojit
k víc serverům a profily se načítají z toho, ke kterému jste připojení.</p>

<h2>Když něco nefunguje</h2>
<table class="wiki-tabulka">
<tr><th>Co se děje</th><th>Co s tím</th></tr>
<tr><td>Po aktualizaci (<code>hermes update</code>) aplikace zmizela</td><td>Zavřela se kvůli výměně souborů. Spusťte ji znovu: <code>hermes desktop</code></td></tr>
<tr><td>Nedostanu se na server, hlásí to přihlášení</td><td>Zkontrolujte jméno i heslo (server schválně neprozrazuje, které z nich je špatně) a jestli je přihlašování na serveru vůbec zapnuté</td></tr>
<tr><td>Okno „pod oknem“ nic nevidí</td><td>Na Windows s čipem ARM to neumí — použijte běžnou verzi pro Intel/AMD nebo to neřešte</td></tr>
<tr><td>Připojení ke vzdálenému serveru vypadlo</td><td>Dá se obnovit bez zavírání aplikace (znovu připojit na stránce Gateways)</td></tr>
<tr><td>Změnil se klíč serveru (SSH)</td><td>Aplikace se ozve, že se klíč serveru změnil — to je ochrana proti podvržení, ne chyba. Řešte to s správcem serveru</td></tr>
</table>

<h2>Naše zkušenosti</h2>
<table class="wiki-tabulka">
<tr><th>Co jsme řešili</th><th>Ponaučení</th></tr>
<tr><td>Rozhovor začal v terminálu a chtěli jsme pokračovat v aplikaci</td><td>Jde to — stav je společný. Do aplikace se dá i přepnout uprostřed úlohy</td></tr>
<tr><td>Vedle chatu jsme potřebovali vidět, co agent dělá na serveru</td><td>Terminál v pravém sloupci a náhled souborů šetří přepínání oken; terminál běží dál i skrytý</td></tr>
<tr><td>V aplikaci jsme si psali s dvěma agenty a nastavení se pletlo</td><td>Pomohl přepínač „Applies to“ — změna platí pro vybraný profil, ne pro všechny</td></tr>
<tr><td>Dvě aktualizace za sebou a aplikace se neotevřela</td><td>Není to závada: aplikaci po aktualizaci spouštějte znovu (klidně z terminálu příkazem <code>hermes desktop</code>)</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Nastavte si <code>--cwd</code> nebo <code>terminal.cwd</code></td><td>Agent začne v projektu, ne v domovské složce — míň vysvětlování na začátku</td></tr>
<tr><td>Dlouhou úlohu si vydejte do samostatného okna</td><td>Můžete pracovat jinde a nesaháte pořád na stejný rozhovor</td></tr>
<tr><td>Používejte aplikaci i terminál podle situace</td><td>Rychlý dotaz je lepší v terminálu, rozbor s obrázky a soubory v aplikaci</td></tr>
<tr><td>Před přenosem na jiný počítač si profil vyexportujte</td><td>Odnesete si nastavení a paměť; klíče doplníte — ty se schválně nepřenášejí</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/funkce/profily/"><strong>Profily a více agentů</strong><span>Víc agentů v jedné aplikaci</span></a>
<a href="/wiki/funkce/tui/"><strong>TUI — práce v terminálu</strong><span>Když je terminál pohodlnější</span></a>
<a href="/wiki/funkce/sezeni/"><strong>Sezení a jejich obnova</strong><span>Rozhovory, které zůstávají</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/desktop" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Aplikace do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co aplikace je
Jiné okno ke stejnému agentovi: stejné nastavení, klíče, paměť, rozhovory, skilly.
Běží na macOS, Windows i Linuxu. Spuštění: hermes desktop   (odkaz na projekt: --cwd /cesta)

## Co v ní je
Chat (průběh nástrojů, přílohy přetažením, obnovené neodeslané zprávy) · postranní sloupec
(rozhovory, projekty, nastavení, profily) · náhled vpravo (soubory, výsledky, weby) ·
terminál vpravo (Ctrl+`, Ctrl+Shift+` — běží i skrytý) · artefakty nad psacím polem ·
živí podagenti (počet, stav, možnost mluvit do práce nebo zastavit)

## Klávesy
Ctrl+T nová karta · Ctrl+Tab přepínání · Ctrl+1..9 skok · Ctrl+Shift+N nové okno ·
Ctrl+B / Ctrl+J levý / pravý sloupec. Na macOS místo Ctrl klávesa Cmd.

## Projekty
Složky s projekty se hledají při startu v domovské složce do omezené hloubky;
repo_scan_enabled: false v config.yaml hledání vypne.
Složka pro práci: hermes desktop --cwd <cesta> nebo terminal.cwd v nastavení profilu.

## Víc profilů
Stránky nastavení mají přepínač "Applies to" (kterého profilu se změna týká).
Cmd/Ctrl+K -> Export profile… vyexportuje skilly, paměť, osobnost, úlohy a nastavení;
API klíče se do exportu nedávají.

## Agent na serveru, aplikace u vás
Nastavení -> Gateways: místní agent / vzdálený agent (adresa serveru s hermes serve) / Hermes Cloud.
Připojení je věc počítače; profily se načítají z připojeného serveru.

## Když něco nefunguje
- po hermes update aplikace zmizí -> spustit znovu hermes desktop
- přihlášení na server selže -> zkontrolovat jméno i heslo (server neprozrazuje, co je špatně)
- okno "pod oknem" nevidí nic -> na Windows ARM to neumí
- výpadku připojení se dá obnovit bez zavření aplikace; změna SSH klíče serveru je ochrana, ne chyba

## Naše zkušenosti
Rozhovor lze začít v terminálu a pokračovat v aplikaci (společný stav) · terminál a náhled souborů
šetří přepínání oken · přepínač "Applies to" zabránil tomu, aby se nastavení pletlo mezi profily ·
po aktualizaci je normální aplikaci znovu spustit.

## Tipy
Nastavit --cwd/terminal.cwd · dlouhou úlohu do samostatného okna · kombinovat aplikaci a terminál ·
před přenosem vyexportovat profil (klíče se přenášejí zvlášť).
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🖥️</span><div><strong>The app is not a different agent — it is another window onto the same one.</strong>
Same settings, same keys, same memory, same conversations, same skills. What you do in the
terminal shows up in the app and the other way round.</div></div>

<h2>When it helps</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>Why the app</th></tr>
<tr><td>You want to see what the agent is doing</td><td>Streaming answers and every tool call are laid out clearly, images included</td></tr>
<tr><td>You work on several things at once</td><td>Multiple windows and panes: one conversation on each monitor</td></tr>
<tr><td>You need files and a terminal at hand</td><td>A file browser and a real terminal sit next to the chat — no window switching</td></tr>
<tr><td>You would rather not type commands</td><td>Settings live on plainly labelled pages instead of in a config file</td></tr>
<tr><td>You run several agents</td><td>The optional "Applies to" chip row says which profile a change belongs to</td></tr>
</table>

<h2>Install and launch</h2>
<p>The app is downloadable from the project's site, but if Hermes is already on your machine one
command is enough — it uses your keys, conversations and skills:</p>
<div class="code-block"><span class="p">❯</span> hermes desktop
<span class="p">❯</span> hermes desktop --cwd /path/to/project    <span class="c"># open straight in a project</span></div>
<p>It runs on <strong>macOS</strong>, <strong>Windows</strong> and <strong>Linux</strong>. On
Windows you need Git, and SSH client for connecting to a remote machine.</p>

<h2>What is in the app</h2>
<table class="wiki-tabulka">
<tr><th>Part</th><th>What it does</th></tr>
<tr><td><strong>Chat</strong> (centre)</td><td>The conversation, live tool activity, drag-and-drop attachments, restored unsent messages</td></tr>
<tr><td><strong>Sidebar</strong></td><td>Conversations, projects, settings, profile switching</td></tr>
<tr><td><strong>Preview rail</strong> (right)</td><td>Files, tool results and web pages the agent is working on</td></tr>
<tr><td><strong>Terminal</strong> (right)</td><td>A real terminal: <code>Ctrl</code>+<code>`</code> opens it, <code>Ctrl</code>+<code>Shift</code>+<code>`</code> starts another. Shells keep running while hidden</td></tr>
<tr><td><strong>Artifacts</strong></td><td>Finished files and previews offered above the composer — click to open</td></tr>
<tr><td><strong>Live subagents</strong></td><td>A frame with the count and state of working helpers; you can steer them or stop them</td></tr>
</table>

<h2>Working on several things at once</h2>
<table class="wiki-tabulka">
<tr><th>Key</th><th>What it does</th></tr>
<tr><td><code>Ctrl</code>+<code>T</code></td><td>New conversation in a new tab</td></tr>
<tr><td><code>Ctrl</code>+<code>Tab</code></td><td>Cycle between conversations</td></tr>
<tr><td><code>Ctrl</code>+<code>1</code>…<code>9</code></td><td>Jump to a conversation by position</td></tr>
<tr><td><code>Ctrl</code>+<code>Shift</code>+<code>N</code></td><td>New window — handy for parking a long job on a second monitor</td></tr>
<tr><td><code>Ctrl</code>+<code>B</code> / <code>Ctrl</code>+<code>J</code></td><td>Hide the left / right rail (more room for chat)</td></tr>
</table>
<p class="note">On macOS use <code>Cmd</code> instead of <code>Ctrl</code>.</p>

<h2>Projects</h2>
<p>The app handles several projects side by side. It discovers project folders at startup by
scanning your home directory to a bounded depth. You can limit or disable that scan:</p>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml — folder scanning</span>
repo_scan_enabled: false        <span class="c"># do not scan the home directory at all</span></div>
<p>You can also set the folder the agent works in at launch (<code>--cwd</code>) or permanently via
<code>terminal.cwd</code> in the profile settings — see
<a href="/en/wiki/features/profiles/">Profiles and multiple agents</a>.</p>

<h2>Several profiles in one app</h2>
<p>With more than one profile (say one for work and one for personal things) you do not have to
switch the whole app. Settings pages show an <strong>"Applies to"</strong> switcher at the top that
selects which profile your edit targets.</p>
<div class="code-block"><span class="p">❯</span> <code>Cmd</code>/<code>Ctrl</code>+<code>K</code> → Export profile…   <span class="c"># one whole profile into one file</span></div>
<p class="note">The export carries skills, memory, persona, scheduled jobs and settings —
<strong>API keys are stripped out</strong> and are added on the target machine. Great for moving a
setup between computers or sharing it with a colleague.</p>

<h2>The agent on a server, the app on your desk</h2>
<p>The app can also run without doing any work itself and simply connect to an agent on a server
(a VPS, a home server, a small machine at home). One settings page handles it —
<strong>Settings → Gateways</strong>:</p>
<table class="wiki-tabulka">
<tr><th>Option</th><th>What it means</th></tr>
<tr><td>Local backend</td><td>Default: the app starts and manages the agent on your own computer</td></tr>
<tr><td>Remote gateway</td><td>Enter the URL of a server running <code>hermes serve</code> and sign in</td></tr>
<tr><td>Hermes Cloud</td><td>Sign in once and pick an agent from your account — no URL to paste</td></tr>
</table>
<p class="note">Connections are machine-level, not per profile: one computer can connect to several
servers, and profiles are discovered from the gateway you are connected to.</p>

<h2>When something does not work</h2>
<table class="wiki-tabulka">
<tr><th>What happens</th><th>What to do</th></tr>
<tr><td>After an update (<code>hermes update</code>) the app vanished</td><td>It closed while files were being replaced. Launch it again: <code>hermes desktop</code></td></tr>
<tr><td>I cannot sign in to the server</td><td>Check both username and password (the backend deliberately does not reveal which is wrong) and whether sign-in is enabled on the server</td></tr>
<tr><td>The "window below" feature sees nothing</td><td>On Windows ARM64 it cannot — use the x64 build or ignore it</td></tr>
<tr><td>A remote connection dropped</td><td>You can reconnect without closing the app (Gateways page)</td></tr>
<tr><td>The server's SSH key changed</td><td>The app warns you that the host key changed — that is protection against impersonation, not a bug. Take it up with whoever runs the server</td></tr>
</table>

<h2>What we learned</h2>
<table class="wiki-tabulka">
<tr><th>What we dealt with</th><th>The lesson</th></tr>
<tr><td>A conversation started in the terminal and we wanted to continue in the app</td><td>It works — the state is shared. You can even switch mid-job</td></tr>
<tr><td>We needed to watch what the agent does on the server</td><td>The right-hand terminal and the file preview save window switching; a hidden terminal keeps running</td></tr>
<tr><td>We chatted with two agents and settings got mixed up</td><td>The "Applies to" switcher fixed it — an edit targets the selected profile, not all of them</td></tr>
<tr><td>Two updates in a row and the app did not open</td><td>That is expected: launch it again after an update (from a terminal with <code>hermes desktop</code> if needed)</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Set <code>--cwd</code> or <code>terminal.cwd</code></td><td>The agent starts in the project instead of your home folder — less explaining at the start</td></tr>
<tr><td>Pop a long job out into its own window</td><td>You can work elsewhere without touching the same conversation</td></tr>
<tr><td>Use the app and the terminal as the moment suits</td><td>A quick question is faster in the terminal; a review with images and files belongs in the app</td></tr>
<tr><td>Export a profile before moving machines</td><td>You take settings and memory with you; keys are added separately on purpose</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/features/profiles/"><strong>Profiles and multiple agents</strong><span>Several agents in one app</span></a>
<a href="/en/wiki/features/tui/"><strong>TUI — working in the terminal</strong><span>When the terminal is more comfortable</span></a>
<a href="/en/wiki/features/sessions/"><strong>Sessions and recovery</strong><span>Conversations that persist</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/desktop" target="_blank" rel="noopener"><strong>Official documentation</strong><span>The desktop app in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What the app is
Another window onto the same agent: same settings, keys, memory, conversations, skills.
Runs on macOS, Windows and Linux. Launch: hermes desktop   (project folder: --cwd /path)

## What is in it
Chat (live tool activity, drag-and-drop attachments, restored unsent messages) · sidebar
(conversations, projects, settings, profiles) · preview rail (files, tool results, web pages) ·
terminal (Ctrl+`, Ctrl+Shift+` — keeps running while hidden) · artifacts above the composer ·
live subagents (count, state, steer or stop)

## Keys
Ctrl+T new tab · Ctrl+Tab cycle · Ctrl+1..9 jump · Ctrl+Shift+N new window ·
Ctrl+B / Ctrl+J left / right rail. On macOS use Cmd.

## Projects
Project folders are discovered at startup by scanning the home directory to a bounded depth;
repo_scan_enabled: false in config.yaml disables the scan.
Working folder: hermes desktop --cwd <path> or terminal.cwd in the profile settings.

## Several profiles
Settings pages have an "Applies to" switcher (which profile the edit targets).
Cmd/Ctrl+K -> Export profile… writes skills, memory, persona, jobs and settings;
API keys are stripped from the export.

## Agent on a server, app on your desk
Settings -> Gateways: local backend / remote gateway (a server running hermes serve) / Hermes Cloud.
Connections are machine-level; profiles come from the connected gateway.

## When something does not work
- after hermes update the app vanished -> launch it again (hermes desktop)
- server sign-in fails -> check username and password (the backend does not say which is wrong)
- "window below" sees nothing -> cannot do it on Windows ARM64
- a dropped connection can be restored without restarting the app; a changed SSH host key is protection, not a bug

## What we learned
A conversation can start in the terminal and continue in the app (shared state) · the terminal and
file preview save window switching · the "Applies to" switcher stopped settings from getting mixed
between profiles · after an update, relaunching the app is normal.

## Tips
Set --cwd/terminal.cwd · pop long jobs into their own window · combine app and terminal · export a
profile before moving machines (keys travel separately).
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(15)
    stranka = najdi(15)
    assert stranka and stranka["nazev"] == "Desktop"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Desktop — aplikace Hermes Agent na počítač",
        "Co umí aplikace na počítač: chat s průběhem práce, projekty, terminál a náhled souborů vedle sebe, víc profilů a připojení k agentovi na serveru.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Desktop",
        "Stejný agent, ale v okně s tlačítky: projekty, soubory, terminál a rozhovory vedle sebe — a můžete se z něj připojit k agentovi na serveru.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Desktop — aplikace Hermes Agent — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Desktop — the Hermes Agent app for your computer",
        "What the desktop app does: chat with live tool activity, projects, a terminal and file preview side by side, several profiles and a connection to an agent on a server.",
        OBRAZEK, "Wiki · Features in depth", "Desktop",
        "The same agent in a window with buttons: projects, files, a terminal and conversations side by side — and you can connect it to an agent on a server.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Desktop — the Hermes Agent app — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
