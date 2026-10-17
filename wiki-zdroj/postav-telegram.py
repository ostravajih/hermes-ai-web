#!/usr/bin/env python3
"""Postaví stránku wiki „Telegram — provoz bota" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-messaging-telegram.md (BotFather, privacy mód a skupiny,
číselné ID uživatele, proměnné prostředí, domovský kanál a doručování z cronu, hlasové zprávy,
velké soubory přes vlastní Bot API server, webhook režim, více botů v jedné skupině, řešení potíží).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram"
OBRAZEK = "wiki-telegram"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">💬</span><div><strong>Nejčastější problém s Telegramem není v Hermesu, ale v privacy módu bota.</strong>
Telegram botům ve výchozím stavu <em>nezobrazuje</em> běžné zprávy ve skupině — jen příkazy a odpovědi
sobě. Kdo to neví, myslí si, že agent ve skupině nefunguje. Řešení je přitom jedno zaškrtnutí
(vlastně jedno vypnutí) v BotFather.</div></div>

<h2>Rychlá cesta</h2>
<p>V dashboardu (Messaging → Telegram) i v aplikaci je tlačítko <strong>Create with QR</strong>:
naskenujete kód, Hermes bota založí, sám zjistí vaše číselné ID a zapíše
<code>TELEGRAM_BOT_TOKEN</code> i <code>TELEGRAM_ALLOWED_USERS</code> do <code>.env</code>.
Ruční cesta níže je pro ty, kdo chtějí mít bota pod vlastní kontrolou — a je dobré vědět, co přesně
se při ní děje.</p>

<h2>1. Bot u BotFathera</h2>
<div class="code-block">@BotFather → /newbot
  → jméno pro lidi („Hermes Agent“)
  → uživatelské jméno, musí končit na „bot“ (např. muj_hermes_bot)
  → BotFather pošle token: 123456789:ABCdef…</div>
<p><strong>Token je klíč od bota.</strong> Kdo ho má, ovládá bota. Když unikne, zneplatníte ho
příkazem <code>/revoke</code> u BotFathera a vyměníte v <code>.env</code>.</p>
<table class="wiki-tabulka">
<tr><th>Příkaz u BotFathera</th><th>K čemu</th></tr>
<tr><td><code>/setdescription</code></td><td>Text „Co tento bot umí?“ před první zprávou</td></tr>
<tr><td><code>/setcommands</code></td><td>Nabídka příkazů na tlačítku „/“ (stačí <code>help</code>, <code>new</code>, <code>sethome</code>)</td></tr>
<tr><td><code>/setuserpic</code></td><td>Avatar bota</td></tr>
<tr><td><code>/setprivacy</code></td><td>Právě ten privacy mód — viz níže</td></tr>
</table>

<h2>2. Privacy mód: proč bot ve skupině „nevidí“</h2>
<p>Privacy mód je <strong>ve výchozím stavu zapnutý</strong>. Bot pak dostane jen:</p>
<ul>
<li>zprávy začínající <code>/</code> (příkazy),</li>
<li>odpovědi na své vlastní zprávy,</li>
<li>servisní zprávy (kdo přišel/odešel, připíchnutí),</li>
<li>vše ve skupinách, kde je <strong>správcem</strong>.</li>
</ul>
<div class="code-block">Vypnutí: @BotFather → /mybots → vybrat bota → Bot Settings → Group Privacy → Turn off
POZOR: po změně musíte bota ze skupiny odebrat a znovu přidat —
Telegram si stav pamatuje z okamžiku, kdy do skupiny přišel.</div>
<p class="note">Alternativa bez vypínání privacy módu: <strong>udělat bota správcem skupiny</strong>.
Správci dostávají všechny zprávy a nemusíte nic přenastavovat globálně.</p>

<h3>Když má bot poslouchat, ale neodpovídat</h3>
<div class="code-block">telegram:
  allowed_chats: ["-1001234567890"]
  group_allowed_chats: ["-1001234567890"]
  require_mention: true
  observe_unmentioned_group_messages: true</div>
<p>Tím se bot dívá na dění ve skupině (může shrnout, co se probíralo), ale promluví jen tehdy,
když ho někdo označí nebo zavolá příkazem.</p>

<h2>3. Číselné ID a přístup</h2>
<p>Hermes ověřuje přístup podle <strong>číselného ID</strong>, ne podle uživatelského jména (to se dá změnit).
Svoje ID zjistíte zprávou botovi <code>@userinfobot</code>.</p>
<div class="code-block"><span class="c"># ~/.hermes/.env</span>
TELEGRAM_BOT_TOKEN=123456789:ABCdef…
TELEGRAM_ALLOWED_USERS=123456789,987654321     <span class="c"># čárkou víc lidí</span></div>
<p class="note">Prázdné <code>TELEGRAM_ALLOWED_USERS</code> znamená, že bot odpovídá komukoli, kdo ho najde.
Pro vlastní agenta to nikdy nechcete — vždy doplňte aspoň svoje ID.</p>

<h2>4. Co všechno umí</h2>
<table class="wiki-tabulka">
<tr><th>Vlastnost</th><th>Jak se projeví</th></tr>
<tr><td>Hlasové zprávy</td><td>Příchozí se přepíšou na text; odpovědět lze i hlasem (když je zapnutý hlasový výstup)</td></tr>
<tr><td>Soubory a fotky</td><td>Posílá i přijímá přílohy; cesta v <code>MEDIA:/…</code> musí být čitelná na stroji, kde běží brána</td></tr>
<tr><td>Doručování z pravidelných úloh</td><td>Výsledek cronu přiletí do <strong>domovského kanálu</strong> (<code>/sethome</code> nebo <code>TELEGRAM_HOME_CHANNEL</code>)</td></tr>
<tr><td>Vlákna (témata)</td><td>V skupinách s tématy se dá určit, do kterého vlákna cron posílá (<code>TELEGRAM_CRON_THREAD_ID</code>)</td></tr>
<tr><td>Reakce</td><td>Agent může označit zprávu reakcí místo odpovědi</td></tr>
<tr><td>Velké soubory (nad 20 MB)</td><td>Jen přes vlastní Bot API server (<code>TELEGRAM_LOCAL</code>, <code>TELEGRAM_API_ID</code>, <code>TELEGRAM_API_HASH</code>)</td></tr>
<tr><td>Webhook místo dotazování</td><td>Když máte veřejnou HTTPS adresu (<code>TELEGRAM_WEBHOOK_URL</code>, <code>…_SECRET</code>, <code>…_PORT</code>)</td></tr>
</table>

<h2>5. Více botů v jedné skupině</h2>
<p>Funguje to, ale každý bot musí mít vlastní token a vlastní profil. Aby se nepřekřikovali, nastavte
jim různé spouštěcí fráze (<code>mention_patterns</code>) nebo je oddělte do témat. Bez toho budou
na stejnou zprávu reagovat oba.</p>

<h2>Časté potíže</h2>
<table class="wiki-tabulka">
<tr><th>Příznak</th><th>Příčina</th></tr>
<tr><td>V soukromé zprávě funguje, ve skupině mlčí</td><td>Privacy mód (viz výše) — vypnout, nebo bota udělat správcem</td></tr>
<tr><td>Bot po přidání do skupiny nic nedělá, i po vypnutí privacy módu</td><td>Bota je potřeba ze skupiny odebrat a znovu přidat</td></tr>
<tr><td>Bot nereaguje vůbec</td><td>Neběží brána (<code>hermes gateway status</code>), nebo je ID uživatele mimo allowlist</td></tr>
<tr><td>„Unauthorized“ v logu</td><td>Špatný nebo zneplatněný token; po <code>/revoke</code> je potřeba nový</td></tr>
<tr><td>Příloha se neodešle</td><td>Běží brána v Dockeru a cesta v <code>MEDIA:</code> existuje jen uvnitř kontejneru</td></tr>
<tr><td>Soubor nad 20 MB nejde</td><td>Limit veřejného Bot API — potřebujete vlastní Bot API server</td></tr>
</table>

<h2>Jak to máme u nás</h2>
<p>Telegram používáme jako dálkový ovladač: ráno přijde souhrn z cronu, během dne se ptáme z telefonu
a výsledky (tabulky, PDF) chodí zpět jako přílohy. Dvě věci se vyplatily:</p>
<table class="wiki-tabulka">
<tr><th>Zvyk</th><th>Proč</th></tr>
<tr><td>Domovský kanál nastavený hned na začátku</td><td>Bez něj cron neví, kam psát, a výsledky zapadnou</td></tr>
<tr><td>Allowlist jen s vlastními ID</td><td>Bot je veřejně dohledatelný; allowlist je jediná brána</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/telegram-a-discord/"><strong>Telegram a Discord — začátky</strong><span>První nastavení bez detailů</span></a>
<a href="/wiki/integrace/discord/"><strong>Discord — server a bot</strong><span>Když má agent žít v komunitě</span></a>
<a href="/wiki/zaciname/pravidelne-ulohy/"><strong>Pravidelné úlohy</strong><span>Kam až má cron doručovat</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Telegram do posledního detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Rychle
Dashboard/desktop: Messaging -> Telegram -> Create with QR (založí bota, zjistí ID, zapíše .env).

## Ručně
@BotFather /newbot -> token. Token = klíč od bota; únik -> /revoke a nový token.
Užitečné: /setdescription, /setcommands (help, new, sethome), /setuserpic, /setprivacy.

## Privacy mód (výchozí ZAPNUTÝ)
Bot vidí jen příkazy (/), odpovědi sobě, servisní zprávy a vše ve skupinách, kde je admin.
Vypnutí: /mybots -> Bot Settings -> Group Privacy -> Turn off; PO TÉ bota ze skupiny odebrat a přidat.
Alternativa: udělat bota správcem skupiny.
Poslouchat, ale neodpovídat: allowed_chats, group_allowed_chats, require_mention: true,
observe_unmentioned_group_messages: true.

## Přístup
Číselné ID (ne username) přes @userinfobot. TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USERS (čárkou).
Prázdný allowlist = bot odpovídá komukoli -> nikdy u vlastního agenta.

## Co umí
Hlas příchozí (přepis) i odchozí (TTS) · soubory a fotky (MEDIA: cesta musí být čitelná tam, kde běží brána)
· cron doručuje do domovského kanálu (/sethome, TELEGRAM_HOME_CHANNEL) · vlákna (TELEGRAM_CRON_THREAD_ID)
· reakce · soubory nad 20 MB jen přes vlastní Bot API server (TELEGRAM_LOCAL, TELEGRAM_API_ID/HASH)
· webhook režim (TELEGRAM_WEBHOOK_URL/SECRET/PORT).

## Více botů ve skupině
Každý vlastní token i profil; oddělit mention_patterns nebo témata, jinak reagují oba.

## Potíže
DM funguje, skupina ne -> privacy mód / bot není admin. Po změně privacy odebrat+přidat.
Nic -> brána neběží nebo ID mimo allowlist. Unauthorized -> token. Příloha -> Docker cesty. >20 MB -> limit API.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">💬</span><div><strong>The most common Telegram problem is not Hermes — it is the bot's privacy mode.</strong>
By default Telegram does not show bots ordinary group messages, only commands and replies to the bot.
People conclude the agent is broken in groups, while the fix is one toggle (actually one switch-off)
in BotFather.</div></div>

<h2>The quick path</h2>
<p>In the dashboard (Messaging → Telegram) and in the desktop app there is a <strong>Create with QR</strong>
button: scan the code, Hermes creates the bot, detects your numeric ID and writes
<code>TELEGRAM_BOT_TOKEN</code> and <code>TELEGRAM_ALLOWED_USERS</code> into <code>.env</code> for you.
The manual path below is for those who want the bot under their own control — and it is worth knowing
what happens along it.</p>

<h2>1. The bot at BotFather</h2>
<div class="code-block">@BotFather → /newbot
  → display name ("Hermes Agent")
  → username, must end in "bot" (e.g. my_hermes_bot)
  → BotFather returns a token: 123456789:ABCdef…</div>
<p><strong>The token is the key to the bot.</strong> Whoever holds it controls the bot. If it leaks,
revoke it with <code>/revoke</code> at BotFather and replace it in <code>.env</code>.</p>
<table class="wiki-tabulka">
<tr><th>BotFather command</th><th>Purpose</th></tr>
<tr><td><code>/setdescription</code></td><td>The “What can this bot do?” text before the first message</td></tr>
<tr><td><code>/setcommands</code></td><td>The command menu behind the “/” button (<code>help</code>, <code>new</code>, <code>sethome</code> is plenty)</td></tr>
<tr><td><code>/setuserpic</code></td><td>Bot avatar</td></tr>
<tr><td><code>/setprivacy</code></td><td>That privacy mode — see below</td></tr>
</table>

<h2>2. Privacy mode: why the bot “cannot see” in groups</h2>
<p>Privacy mode is <strong>on by default</strong>. The bot then receives only:</p>
<ul>
<li>messages starting with <code>/</code> (commands),</li>
<li>replies to its own messages,</li>
<li>service messages (joins/leaves, pins),</li>
<li>everything in groups where it is an <strong>admin</strong>.</li>
</ul>
<div class="code-block">Turn it off: @BotFather → /mybots → pick the bot → Bot Settings → Group Privacy → Turn off
WARNING: after the change you must remove the bot from the group and add it again —
Telegram caches the privacy state from the moment the bot joined.</div>
<p class="note">An alternative without touching privacy mode: <strong>make the bot a group admin</strong>.
Admins receive all messages and you do not have to change a global setting.</p>

<h3>Listen but do not answer</h3>
<div class="code-block">telegram:
  allowed_chats: ["-1001234567890"]
  group_allowed_chats: ["-1001234567890"]
  require_mention: true
  observe_unmentioned_group_messages: true</div>
<p>The bot follows the conversation (so it can summarise what was discussed) but speaks only when
mentioned or called by a command.</p>

<h2>3. Numeric ID and access</h2>
<p>Hermes gates access by <strong>numeric ID</strong>, not by username (usernames can change).
Get yours by messaging <code>@userinfobot</code>.</p>
<div class="code-block"><span class="c"># ~/.hermes/.env</span>
TELEGRAM_BOT_TOKEN=123456789:ABCdef…
TELEGRAM_ALLOWED_USERS=123456789,987654321     <span class="c"># comma-separated for several people</span></div>
<p class="note">An empty <code>TELEGRAM_ALLOWED_USERS</code> means the bot answers anyone who finds it.
Never leave that on a personal agent — always list at least your own ID.</p>

<h2>4. What it can do</h2>
<table class="wiki-tabulka">
<tr><th>Feature</th><th>How it shows up</th></tr>
<tr><td>Voice messages</td><td>Incoming ones are transcribed; the agent can reply with voice when TTS is on</td></tr>
<tr><td>Files and photos</td><td>Sends and receives attachments; a <code>MEDIA:/…</code> path must be readable where the gateway runs</td></tr>
<tr><td>Scheduled delivery</td><td>Cron results arrive in the <strong>home channel</strong> (<code>/sethome</code> or <code>TELEGRAM_HOME_CHANNEL</code>)</td></tr>
<tr><td>Topics (threads)</td><td>In topic-enabled groups you can pin which topic cron posts into (<code>TELEGRAM_CRON_THREAD_ID</code>)</td></tr>
<tr><td>Reactions</td><td>The agent can acknowledge a message with a reaction instead of a reply</td></tr>
<tr><td>Files above 20 MB</td><td>Only via your own Bot API server (<code>TELEGRAM_LOCAL</code>, <code>TELEGRAM_API_ID</code>, <code>TELEGRAM_API_HASH</code>)</td></tr>
<tr><td>Webhook instead of polling</td><td>With a public HTTPS address (<code>TELEGRAM_WEBHOOK_URL</code>, <code>…_SECRET</code>, <code>…_PORT</code>)</td></tr>
</table>

<h2>5. Several bots in one group</h2>
<p>It works, but each bot needs its own token and profile. To stop them talking over each other, give
them distinct trigger phrases (<code>mention_patterns</code>) or separate topics — otherwise both answer
the same message.</p>

<h2>Common problems</h2>
<table class="wiki-tabulka">
<tr><th>Symptom</th><th>Cause</th></tr>
<tr><td>Works in DMs, silent in groups</td><td>Privacy mode (above) — turn it off, or make the bot an admin</td></tr>
<tr><td>Still nothing after turning privacy mode off</td><td>Remove the bot from the group and add it again</td></tr>
<tr><td>The bot never answers</td><td>The gateway is not running (<code>hermes gateway status</code>) or your ID is not in the allowlist</td></tr>
<tr><td>“Unauthorized” in the log</td><td>Wrong or revoked token; after <code>/revoke</code> you need a new one</td></tr>
<tr><td>An attachment never arrives</td><td>The gateway runs in Docker and the <code>MEDIA:</code> path exists only inside the container</td></tr>
<tr><td>Files above 20 MB fail</td><td>A limit of the public Bot API — you need your own Bot API server</td></tr>
</table>

<h2>How we run it</h2>
<p>We use Telegram as a remote control: a cron summary in the morning, questions from the phone during
the day, and results (tables, PDFs) coming back as attachments. Two habits paid off:</p>
<table class="wiki-tabulka">
<tr><th>Habit</th><th>Why</th></tr>
<tr><td>Set the home channel right away</td><td>Without it cron has nowhere to post and results get lost</td></tr>
<tr><td>Keep the allowlist to our own IDs</td><td>The bot is publicly discoverable; the allowlist is the only gate</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/telegram-and-discord/"><strong>Telegram and Discord — the basics</strong><span>First setup without the details</span></a>
<a href="/en/wiki/integrations/discord/"><strong>Discord — server and bot</strong><span>When the agent lives in a community</span></a>
<a href="/en/wiki/getting-started/scheduled-tasks/"><strong>Scheduled tasks</strong><span>Where cron may deliver</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Telegram down to the last detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Quick path
Dashboard/desktop: Messaging -> Telegram -> Create with QR (creates the bot, detects your ID, writes .env).

## Manual
@BotFather /newbot -> token. The token is the key to the bot; leak -> /revoke and replace.
Useful: /setdescription, /setcommands (help, new, sethome), /setuserpic, /setprivacy.

## Privacy mode (ON by default)
The bot sees only commands (/), replies to itself, service messages, and everything in groups where it is admin.
Turn off: /mybots -> Bot Settings -> Group Privacy -> Turn off; THEN remove and re-add the bot to the group.
Alternative: make the bot a group admin.
Listen without answering: allowed_chats, group_allowed_chats, require_mention: true,
observe_unmentioned_group_messages: true.

## Access
Numeric ID (not username) via @userinfobot. TELEGRAM_BOT_TOKEN, TELEGRAM_ALLOWED_USERS (comma-separated).
An empty allowlist means the bot answers anyone -> never on a personal agent.

## Capabilities
Incoming voice (transcribed) and outgoing (TTS) · files and photos (MEDIA: path must be readable where the
gateway runs) · cron delivers to the home channel (/sethome, TELEGRAM_HOME_CHANNEL) · topics
(TELEGRAM_CRON_THREAD_ID) · reactions · files above 20 MB via your own Bot API server (TELEGRAM_LOCAL,
TELEGRAM_API_ID/HASH) · webhook mode (TELEGRAM_WEBHOOK_URL/SECRET/PORT).

## Several bots in one group
Each needs its own token and profile; separate mention_patterns or topics, otherwise both reply.

## Troubleshooting
DMs work, groups do not -> privacy mode / not an admin. After changing privacy, remove and re-add.
Nothing at all -> gateway down or ID not allowed. Unauthorized -> token. Attachment -> Docker paths. >20 MB -> API limit.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(31)
    stranka = najdi(31)
    assert stranka and stranka["nazev"] == "Telegram — provoz bota"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Telegram — provoz bota ve skupině i v soukromí",
        "Privacy mód a skupiny, číselné ID a allowlist, hlasové zprávy, domovský kanál pro cron, velké soubory a co dělat, když bot ve skupině mlčí.",
        OBRAZEK, "Wiki · Integrace", "Telegram — provoz bota",
        "Nejčastější problém s Telegramem není v Hermesu, ale v privacy módu bota. Prakticky: nastavení, skupiny a doručování.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Telegram — provoz bota (česká wiki)", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Telegram — running the bot in groups and in DMs",
        "Privacy mode and groups, numeric IDs and the allowlist, voice messages, the home channel for cron, large files and what to do when the bot goes silent in a group.",
        OBRAZEK, "Wiki · Integrations", "Telegram — running the bot",
        "The most common Telegram problem is not Hermes but the bot's privacy mode. Practical: setup, groups and delivery.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Telegram — running the bot (community wiki)", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
