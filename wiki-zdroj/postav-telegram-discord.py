#!/usr/bin/env python3
"""Postaví stránku wiki „Telegram a Discord" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-messaging-telegram.md a …-discord.md
(příkazy a názvy nastavení opsané z oficiální dokumentace, nic vymyšleného).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram"
OBRAZEK = "wiki-telegram"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📱</span><div><strong>Agent nemusí žít jen v terminálu.</strong>
Připojíte ho k Telegramu nebo Discordu a píšete mu z mobilu jako kamarádovi — odpovídá, spouští příkazy
a pošle vám i soubor. S botem smíte mluvit <strong>jen vy</strong> (a kdo je na seznamu) — ověření je na
číselné ID, ne na jménu.</div></div>

<h2>Co si připravit</h2>
<table class="wiki-tabulka">
<tr><th>Co</th><th>K čemu</th></tr>
<tr><td><strong>Běžící agent na serveru</strong></td><td>Brána (gateway) je součást agenta — když agent běží, stačí ji zapnout</td></tr>
<tr><td><strong>Bot</strong> v Telegramu nebo Discordu</td><td>Vytvoříte ho zdarma, je to práce na dvě minuty (postup níže)</td></tr>
<tr><td><strong>Svoje číselné ID</strong></td><td>Není to vaše jméno ani přezdívka. Podle čísla se pozná, že jste to vy — a nikdo cizí s botem nic neudělá</td></tr>
</table>
<p class="note">Vyberte si jednu platformu, nebo klidně obě. Většina lidí začne Telegramem — je to nejrychlejší cesta na mobil.</p>

<h2>Telegram — krok za krokem</h2>
<ol class="kroky">
<li><strong>Vytvořte bota v Telegramu.</strong> Napište <a href="https://t.me/BotFather" target="_blank" rel="noopener">@BotFather</a> zprávu <code>/newbot</code>,
zeptá se na jméno a na přezdívku končící na <code>bot</code>. Na konci vám pošle <strong>token</strong> (dlouhý řetězec).
Ten je jako heslo — nikomu ho nedávejte.</li>
<li><strong>Zjistěte svoje číslo.</strong> Napište <a href="https://t.me/userinfobot" target="_blank" rel="noopener">@userinfobot</a> a on vám
vaše ID hned pošle (např. <code>123456789</code>). Pozor, není to vaše přezdívka.</li>
<li><strong>Nastavte agenta.</strong> Nejsnáz průvodcem, který se zeptá na token a na vaše ID a všechno zapíše:
<div class="code-block"><span class="p">$</span> hermes gateway setup</div>
Ručně to jde taky — do souboru <code>~/.hermes/.env</code> přidejte dva řádky:
<div class="code-block"><span class="c"># ~/.hermes/.env</span>
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_ALLOWED_USERS=123456789   <span class="c"># víc lidí oddělte čárkou</span></div></li>
<li><strong>Zapněte bránu a zkontrolujte ji.</strong>
<div class="code-block"><span class="p">$</span> hermes gateway start
<span class="p">$</span> hermes gateway status</div></li>
<li><strong>Napište botovi.</strong> V Telegramu mu pošlete zprávu — do pár vteřin odpoví.</li>
</ol>
<p class="note"><strong>Do skupiny bota přidat můžete</strong>, ale Telegram mu ve výchozím nastavení nedovolí číst běžné zprávy
(ochrana soukromí) — uvidí jen příkazy a zmínky <code>@vasebot</code>. Pro skupinové použití se v @BotFather vypíná
přepínač <em>Group Privacy</em>.</p>
<p><strong>Co umí navíc:</strong> přeposílat soubory a fotky oběma směry, zpracovat hlasovou zprávu a posílat výsledky
pravidelných úloh do zvolené konverzace (nastavení <code>TELEGRAM_HOME_CHANNEL</code>).</p>

<h2>Discord — krok za krokem</h2>
<ol class="kroky">
<li><strong>Vytvořte aplikaci a bota.</strong> Na <a href="https://discord.com/developers/applications" target="_blank" rel="noopener">discord.com/developers/applications</a>
zvolte <em>New Application</em>, pak v levém menu <em>Bot</em>.</li>
<li><strong>Zapněte čtení zpráv.</strong> V nastavení bota zapněte <em>Message Content Intent</em> (privilegované oprávnění).
Bez něj bot zprávy nevidí a bude vypadat mrtvý.</li>
<li><strong>Zkopírujte token</strong> (<em>Reset Token</em>) — zobrazí se jen jednou, proto si ho hned uložte.</li>
<li><strong>Pozvěte bota na svůj server.</strong> V záložce <em>Installation</em> vygenerujte odkaz a přes něj bota přidejte
(práva: čtení a psaní zpráv, posílání souborů).</li>
<li><strong>Zjistěte svoje ID.</strong> V Discordu zapněte <em>Vývojářský režim</em> (Uživatelská nastavení → Rozšířené),
pak na sebe klikněte pravým tlačítkem a zvolte <em>Kopírovat ID uživatele</em>.</li>
<li><strong>Nastavte a spusťte agenta</strong> — stejně jako u Telegramu:
<div class="code-block"><span class="c"># průvodce (doporučeno) — vyberte Discord</span>
<span class="p">$</span> hermes gateway setup
<span class="c"># nebo ručně do ~/.hermes/.env</span>
DISCORD_BOT_TOKEN=vase-token
DISCORD_ALLOWED_USERS=284102345871466496   <span class="c"># víc lidí oddělte čárkou</span>
<span class="c"># a spuštění</span>
<span class="p">$</span> hermes gateway start</div></li>
</ol>
<p><strong>V kanálu bota oslovte</strong> <code>@vasebot</code> — v běžných kanálech reaguje na zmínky, aby se nemíchal do hovoru.
V přímé zprávě odpovídá na cokoli. Umí i lomítkové příkazy přímo v Discordu (např. stav nebo změnu modelu).</p>
<p class="note">V nastavení lze rozdělit lidi na <strong>správce</strong> (všechny příkazy) a <strong>běžné uživatele</strong>
(povolené příkazy zvlášť) pomocí <code>allow_admin_from</code> a <code>user_allowed_commands</code>. Pro rodinu nebo tým
je to praktické — ostatní se dostanou jen k tomu, co jim dovolíte.</p>

<h2>Kdo s botem může mluvit</h2>
<table class="wiki-tabulka">
<tr><th>Pravidlo</th><th>Proč</th></tr>
<tr><td><strong>Token je jako heslo</strong></td><td>Kdo ho získá, ovládá vašeho bota. Nikdy ho nevkládejte do chatu ani do repozitáře. Když ho omylem zveřejníte, ihned ho v @BotFather / Developer Portalu zneplatněte (Reset Token)</td></tr>
<tr><td><strong>Seznam povolených ID</strong></td><td>Bot odpovídá jen ID na seznamu. Cizí člověk, který bota najde, nedostane odpověď — a hlavně nic nespustí</td></tr>
<tr><td><strong>Prázdný seznam = otevřené dveře</strong></td><td>Když seznam necháte prázdný (u Discordu přepínač pro všechny), může bota použít kdokoli. Vždy doplňte svoje ID</td></tr>
<tr><td><strong>Jen jedna běžící brána na token</strong></td><td>Dva agenti se stejným tokenem si zprávy přetahují a jeden druhému je „kradou“</td></tr>
</table>

<h2>Když to nefunguje</h2>
<table class="wiki-tabulka">
<tr><th>Co se děje</th><th>Nejčastější příčina a co s tím</th></tr>
<tr><td>Bot mlčí úplně</td><td>Brána neběží — ověřte <code>hermes gateway status</code>, případně ji spusťte <code>hermes gateway start</code></td></tr>
<tr><td>Bot běží, ale neodpovídá mně</td><td>Vaše ID není na seznamu, nebo je na seznamu jiné číslo (zkontrolujte přes @userinfobot). Častá chyba: opsané jméno místo čísla</td></tr>
<tr><td>Ve skupině mlčí, v soukromé zprávě funguje</td><td>Ochrana soukromí (Group Privacy) — v @BotFather ji vypněte; nebo bota oslovte zmínkou <code>@vasebot</code></td></tr>
<tr><td>Na Discordu vypadá mrtvý</td><td>Chybí <em>Message Content Intent</em>, nebo není vygenerovaný odkaz s potřebnými právy</td></tr>
<tr><td>Odpověděl jednou a pak nic</td><td>Nejspíš běží druhá kopie agenta se stejným tokenem, nebo chybí kredit u modelu (viz <a href="/wiki/zaciname/vyber-modelu/">výběr modelu</a>)</td></tr>
<tr><td>Po restartu serveru bot zmizel</td><td>Brána musí běžet jako služba (systemd), aby se spustila sama. Postup je v oficiální dokumentaci k nasazení</td></tr>
</table>

<h2>Naše tipy z provozu</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Začněte Telegramem</td><td>Dvě minuty práce a funguje na mobilu i bez otevírání počítače</td></tr>
<tr><td>Discord se hodí pro partu</td><td>Kanály, zmínky a oddělená práva — agent v jednom kanálu neruší ostatní</td></tr>
<tr><td>Nechte si posílat delší výsledky jako soubor</td><td>Agent umí přiložit soubor (např. výpis nebo tabulku), což se v chatu čte lépe než dlouhý text</td></tr>
<tr><td>Ověřte stav po každé změně</td><td><code>hermes gateway status</code> řekne, jestli brána běží a která platforma je připojená</td></tr>
<tr><td>Zkuste hlasovku</td><td>V Telegramu můžete agentovi nadiktovat zadání hlasovou zprávou</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/prvni-chat/"><strong>První chat s agentem</strong><span>Jak zadávat úkoly, aby se daly ověřit</span></a>
<a href="/wiki/zaciname/vyber-modelu/"><strong>Výběr AI modelu</strong><span>Který model se vyplatí a kde ho pořídit</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Telegram a Discord do detailu (anglicky)</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Discord komunity</strong><span>Zeptejte se, co komu funguje</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co si připravit
- běžící agent na serveru (brána/gateway je jeho součást)
- bota v Telegramu nebo Discordu (vytvoříte zdarma během dvou minut)
- svoje číselné ID (ne jméno ani přezdívka) — podle něj se řídí přístup

## Telegram
1. @BotFather -> /newbot -> jméno + přezdívka končící na "bot" -> pošle token
2. @userinfobot -> pošle vaše číselné ID
3. hermes gateway setup   (průvodce; nebo ručně)
   do ~/.hermes/.env:
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_ALLOWED_USERS=123456789     # víc ID oddělit čárkou
4. hermes gateway start ; hermes gateway status
5. napište botovi v Telegramu

Skupiny: Telegram botovi ve výchozím stavu nedovolí číst běžné zprávy (Group Privacy) —
uvidí jen zmínky @vasebot; pro skupiny přepínač v @BotFather vypnout.
Navíc: soubory a fotky oběma směry, hlasové zprávy, TELEGRAM_HOME_CHANNEL pro výsledky pravidelných úloh.

## Discord
1. discord.com/developers/applications -> New Application -> Bot
2. zapnout Message Content Intent (bez toho bot zprávy nevidí)
3. Reset Token -> zkopírovat (zobrazí se jednou)
4. Installation -> vygenerovat odkaz a pozvat bota na server (práva: čtení/psaní zpráv, soubory)
5. Vývojářský režim -> pravé tlačítko na sebe -> Kopírovat ID uživatele
6. hermes gateway setup (vybrat Discord), nebo ručně:
   DISCORD_BOT_TOKEN=...
   DISCORD_ALLOWED_USERS=284102345871466496
   hermes gateway start
V kanálu oslovit @vasebot; v přímé zprávě odpovídá na cokoli.
Práva navíc: allow_admin_from (správci) a user_allowed_commands (běžní uživatelé).

## Bezpečnost
- token je jako heslo; při úniku zneplatnit (Reset Token)
- bot odpovídá jen ID na seznamu; prázdný seznam = otevřené dveře
- jen jedna běžící brána na jeden token (jinak si zprávy kradou)

## Když nefunguje
- mlčí úplně -> hermes gateway status / start
- neodpovídá mně -> moje ID není na seznamu (ověřit @userinfobot)
- mlčí ve skupině -> Group Privacy / chybí zmínka @vasebot
- Discord mrtvý -> chybí Message Content Intent nebo práva při pozvání
- po restartu zmizel -> brána musí běžet jako služba (systemd)
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📱</span><div><strong>The agent does not have to live in a terminal.</strong>
Connect it to Telegram or Discord and message it from your phone like a friend — it answers, runs commands and
sends you a file. Only <strong>you</strong> (and whoever is on your list) can talk to the bot: access is keyed on
a numeric ID, not on a name.</div></div>

<h2>What you need</h2>
<table class="wiki-tabulka">
<tr><th>Item</th><th>What it is for</th></tr>
<tr><td><strong>A running agent on a server</strong></td><td>The gateway is part of the agent — once it runs, you just switch the gateway on</td></tr>
<tr><td><strong>A bot</strong> on Telegram or Discord</td><td>Free to create, a two-minute job (steps below)</td></tr>
<tr><td><strong>Your numeric ID</strong></td><td>Not your name or handle. The number is how the agent knows it is you — and how nobody else can use your bot</td></tr>
</table>
<p class="note">Pick one platform, or both. Most people start with Telegram — it is the fastest route to your phone.</p>

<h2>Telegram — step by step</h2>
<ol class="kroky">
<li><strong>Create the bot.</strong> Message <a href="https://t.me/BotFather" target="_blank" rel="noopener">@BotFather</a> with <code>/newbot</code>,
answer the name questions, and it sends you a <strong>token</strong>. Treat it like a password and never share it.</li>
<li><strong>Find your numeric ID.</strong> Message <a href="https://t.me/userinfobot" target="_blank" rel="noopener">@userinfobot</a> and it replies
with your ID (e.g. <code>123456789</code>).</li>
<li><strong>Configure the agent.</strong> The easiest way is the wizard, which asks for the token and your ID
and writes everything for you:
<div class="code-block"><span class="p">$</span> hermes gateway setup</div>
Or do it by hand — add two lines to <code>~/.hermes/.env</code>:
<div class="code-block"><span class="c"># ~/.hermes/.env</span>
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_ALLOWED_USERS=123456789   <span class="c"># separate several IDs with a comma</span></div></li>
<li><strong>Start the gateway and check it.</strong>
<div class="code-block"><span class="p">$</span> hermes gateway start
<span class="p">$</span> hermes gateway status</div></li>
<li><strong>Send the bot a message.</strong> It replies within seconds.</li>
</ol>
<p class="note"><strong>You can add the bot to a group</strong>, but by default Telegram will not let it read ordinary
messages (privacy protection) — it only sees commands and <code>@yourbot</code> mentions. For group use, switch
<em>Group Privacy</em> off in @BotFather.</p>
<p><strong>What else it does:</strong> send and receive files and photos, transcribe voice messages, and deliver the
output of scheduled jobs to a chosen conversation (<code>TELEGRAM_HOME_CHANNEL</code>).</p>

<h2>Discord — step by step</h2>
<ol class="kroky">
<li><strong>Create an application and a bot.</strong> At <a href="https://discord.com/developers/applications" target="_blank" rel="noopener">discord.com/developers/applications</a>
choose <em>New Application</em>, then <em>Bot</em> in the left menu.</li>
<li><strong>Enable message reading.</strong> Turn on <em>Message Content Intent</em> (a privileged permission).
Without it the bot cannot see messages and looks dead.</li>
<li><strong>Copy the token</strong> (<em>Reset Token</em>) — it is shown once, so save it immediately.</li>
<li><strong>Invite the bot to your server.</strong> Generate an invite link in the <em>Installation</em> tab with the
read/send messages and attach files permissions.</li>
<li><strong>Find your ID.</strong> Enable <em>Developer Mode</em> (User Settings → Advanced), then right-click your
name and choose <em>Copy User ID</em>.</li>
<li><strong>Configure and start the agent</strong> — same as Telegram:
<div class="code-block"><span class="c"># wizard (recommended) — pick Discord</span>
<span class="p">$</span> hermes gateway setup
<span class="c"># or by hand in ~/.hermes/.env</span>
DISCORD_BOT_TOKEN=your-token
DISCORD_ALLOWED_USERS=284102345871466496   <span class="c"># separate several IDs with a comma</span>
<span class="c"># and start it</span>
<span class="p">$</span> hermes gateway start</div></li>
</ol>
<p><strong>Mention the bot in a channel</strong> (<code>@yourbot</code>) — in normal channels it only reacts to mentions so it
does not interrupt the conversation. In a direct message it answers anything. It also supports slash commands
directly in Discord (for example status or switching the model).</p>
<p class="note">You can split people into <strong>admins</strong> (all commands) and <strong>regular users</strong>
(only the commands you allow) using <code>allow_admin_from</code> and <code>user_allowed_commands</code>. Handy for a
family or a team — everyone else gets access only to what you grant.</p>

<h2>Who can talk to the bot</h2>
<table class="wiki-tabulka">
<tr><th>Rule</th><th>Why</th></tr>
<tr><td><strong>The token is a password</strong></td><td>Whoever gets it controls your bot. Never paste it into a chat or a repository. If you leak it, revoke it immediately (Reset Token in @BotFather / the Developer Portal)</td></tr>
<tr><td><strong>The allow list</strong></td><td>The bot only answers IDs on the list. A stranger who finds your bot gets no reply — and above all runs nothing</td></tr>
<tr><td><strong>An empty list is an open door</strong></td><td>Leave the list empty (or the "allow everyone" switch on Discord) and anyone can use your bot. Always add your own ID</td></tr>
<tr><td><strong>One running gateway per token</strong></td><td>Two agents sharing a token fight over messages and steal each other's replies</td></tr>
</table>

<h2>When it does not work</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>Usual cause and what to do</th></tr>
<tr><td>The bot is silent</td><td>The gateway is not running — check <code>hermes gateway status</code> and start it with <code>hermes gateway start</code></td></tr>
<tr><td>It runs but ignores me</td><td>Your ID is not on the list, or the wrong number is there (verify with @userinfobot). A common mistake is pasting a username instead of the number</td></tr>
<tr><td>Silent in groups, works in DMs</td><td>Group Privacy — turn it off in @BotFather, or address the bot with <code>@yourbot</code></td></tr>
<tr><td>Looks dead on Discord</td><td><em>Message Content Intent</em> is off, or the invite link was generated without the needed permissions</td></tr>
<tr><td>Answered once, then nothing</td><td>Most likely a second agent copy with the same token, or no model credit (see <a href="/en/wiki/getting-started/choosing-a-model/">choosing a model</a>)</td></tr>
<tr><td>It disappeared after a reboot</td><td>The gateway has to run as a service (systemd) to start by itself. The deployment docs cover it</td></tr>
</table>

<h2>Tips from running it</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Start with Telegram</td><td>Two minutes of work and it works from your phone, no computer needed</td></tr>
<tr><td>Discord suits a group</td><td>Channels, mentions and separate permissions — the agent does not disturb other conversations</td></tr>
<tr><td>Have long output sent as a file</td><td>The agent can attach a file (a listing or a table), which reads better in a chat than a wall of text</td></tr>
<tr><td>Check the status after every change</td><td><code>hermes gateway status</code> tells you whether the gateway runs and which platform is connected</td></tr>
<tr><td>Try a voice message</td><td>On Telegram you can dictate the task instead of typing it</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/first-chat/"><strong>Your first chat</strong><span>How to give verifiable tasks</span></a>
<a href="/en/wiki/getting-started/choosing-a-model/"><strong>Choosing an AI model</strong><span>Which model pays off and where to buy it</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Telegram and Discord in detail</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Community Discord</strong><span>Ask what works for others</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What you need
- a running agent on a server (the gateway is part of it)
- a bot on Telegram or Discord (free, takes about two minutes)
- your numeric ID (not your name or handle) - access is keyed on it

## Telegram
1. @BotFather -> /newbot -> name + handle ending in "bot" -> sends you a token
2. @userinfobot -> replies with your numeric ID
3. hermes gateway setup   (wizard; or by hand)
   in ~/.hermes/.env:
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_ALLOWED_USERS=123456789     # comma-separate several IDs
4. hermes gateway start ; hermes gateway status
5. message the bot on Telegram

Groups: by default Telegram does not let the bot read ordinary messages (Group Privacy) - it
only sees @yourbot mentions; switch it off in @BotFather for group use.
Also: files and photos both ways, voice messages, TELEGRAM_HOME_CHANNEL for scheduled output.

## Discord
1. discord.com/developers/applications -> New Application -> Bot
2. enable Message Content Intent (otherwise the bot sees nothing)
3. Reset Token -> copy it (shown once)
4. Installation -> generate the invite link and invite the bot (read/send messages, files)
5. Developer Mode -> right-click yourself -> Copy User ID
6. hermes gateway setup (pick Discord), or by hand:
   DISCORD_BOT_TOKEN=...
   DISCORD_ALLOWED_USERS=284102345871466496
   hermes gateway start
Mention @yourbot in channels; DMs answer anything.
Extra control: allow_admin_from (admins) and user_allowed_commands (regular users).

## Security
- the token is a password; if leaked, revoke it (Reset Token)
- the bot only answers IDs on the allow list; an empty list is an open door
- only one running gateway per token (otherwise they steal each other's messages)

## Troubleshooting
- completely silent -> hermes gateway status / start
- ignores me -> my ID is not on the list (verify with @userinfobot)
- silent in groups -> Group Privacy / missing @yourbot mention
- dead on Discord -> Message Content Intent off or missing invite permissions
- gone after reboot -> the gateway must run as a service (systemd)
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(4)
    stranka = najdi(4)
    assert stranka and stranka["nazev"] == "Telegram a Discord"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Telegram a Discord — jak si agenta pustit na mobil",
        "Připojte Hermes Agenta k Telegramu nebo Discordu: vytvoření bota, nastavení přístupu podle číselného ID, spuštění brány a co dělat, když bot mlčí.",
        OBRAZEK, "Wiki · Začínáme", "Telegram a Discord",
        "Aby vám agent odpovídal z mobilu — a aby s ním nikdo cizí nic nespustil.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Telegram a Discord — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Telegram and Discord — putting the agent on your phone",
        "Connect Hermes Agent to Telegram or Discord: create a bot, set access by numeric ID, start the gateway and what to do when the bot stays silent.",
        OBRAZEK, "Wiki · Start here", "Telegram and Discord",
        "So the agent answers from your phone — and nobody else can run anything with it.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Telegram and Discord — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
