#!/usr/bin/env python3
"""Postaví stránku wiki „Discord — server a bot" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-messaging-discord.md (vytvoření aplikace a bota, privilegované
intenty, pozvánka a oprávnění, chování v kanálech a vláknech, allowlist uživatelů/rolí/kanálů,
domovský kanál, hlas, fórová vlákna, řešení potíží).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord"
OBRAZEK = "wiki-discord"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🎮</span><div><strong>Když Discord bot zůstane offline, v 90 % případů chybí „Message Content Intent“.</strong>
Discord obsah zpráv botům ve výchozím stavu nevydává. Hermes si o něj vždy říká, a dokud není
v Developer Portalu zapnutý, Discord spojení <strong>odmítne</strong> — bot se vůbec nepřipojí.
Druhý povinný přepínač je <em>Server Members Intent</em> (jinak neumí dohledat uživatele).</div></div>

<h2>1. Aplikace a bot</h2>
<div class="code-block">1) discord.com/developers/applications → New Application (jméno = jméno bota)
2) Bot → Add Bot → zkopírovat token (DISCORD_BOT_TOKEN)
3) Privileged Gateway Intents:
     Server Members Intent   → ON   (povinné)
     Message Content Intent  → ON   (povinné!)
     Presence Intent         → volitelné
4) Installation (nebo ruční URL): scopes „bot“ + „applications.commands“</div>
<div class="code-block"><span class="c"># minimální oprávnění bota</span>
View Channels · Send Messages · Embed Links · Attach Files · Read Message History
<span class="c"># doporučená navíc</span>
Create Public Threads · Send Messages in Threads</div>
<div class="code-block"><span class="c"># ruční pozvánka (YOUR_APP_ID nahraďte)</span>
https://discord.com/oauth2/authorize?client_id=YOUR_APP_ID&scope=bot+applications.commands&permissions=309237763136</div>

<h2>2. ID uživatele a přístup</h2>
<table class="wiki-tabulka">
<tr><th>Nastavení</th><th>Význam</th></tr>
<tr><td><code>DISCORD_BOT_TOKEN</code></td><td>Token bota</td></tr>
<tr><td><code>DISCORD_ALLOWED_USERS</code></td><td>Číselná ID uživatelů (čárkou). Bez něj i bez rolí Hermes <strong>všechny odmítne</strong> — bezpečnostní výchozí stav</td></tr>
<tr><td><code>DISCORD_ALLOWED_ROLES</code></td><td>ID rolí — kdo má roli, má přístup (vhodné pro měnící se tým moderátorů)</td></tr>
<tr><td><code>DISCORD_ALLOWED_CHANNELS</code></td><td>Omezení na konkrétní kanály</td></tr>
<tr><td><code>DISCORD_REQUIRE_MENTION</code></td><td>Zda musí být bot označen (výchozí ano v kanálech)</td></tr>
<tr><td><code>DISCORD_FREE_RESPONSE_CHANNELS</code></td><td>Kanály, kde bot odpovídá i bez označení</td></tr>
</table>
<p class="note">ID se kopírují v Discordu po zapnutí <em>Developer Mode</em> (Uživatelská nastavení →
Pokročilé). Uživatelská jména fungují jen jako doplněk a nikdy se nepárují podle přezdívek na serveru
— ty si může nastavit kdokoli.</p>

<h2>3. Jak se bot chová</h2>
<table class="wiki-tabulka">
<tr><th>Kde</th><th>Chování</th></tr>
<tr><td>Soukromé zprávy</td><td>Odpovídá na vše, každá konverzace má vlastní sezení</td></tr>
<tr><td>Kanály serveru</td><td>Ve výchozím stavu jen na označení <code>@bot</code>; bez označení zprávu ignoruje</td></tr>
<tr><td>Kanály bez povinného označení</td><td>Odpovídá průběžně (hodí se pro „pracovní“ kanál); volitelně si každou zprávu vezme do vlastního vlákna</td></tr>
<tr><td>Vlákna</td><td>Odpovídá ve stejném vlákně a historie vlákna zůstává oddělená od kanálu</td></tr>
<tr><td>Víc lidí v jednom kanále</td><td>Historie se ve výchozím stavu drží <strong>zvlášť pro každého</strong> — dva lidé si nepřepisují kontext</td></tr>
<tr><td>Fórová vlákna</td><td>Bot si při každém odeslání založí nové vlákno (fórum nepřijímá přímé zprávy)</td></tr>
</table>

<h2>4. Domovský kanál a hlas</h2>
<div class="code-block"><span class="c"># příkazem v kanálu, kde bot je</span>
/sethome

<span class="c"># nebo v .env</span>
DISCORD_HOME_CHANNEL=123456789012345678
DISCORD_HOME_CHANNEL_NAME="#bot-updates"</div>
<p>Do domovského kanálu chodí to, co bot posílá sám: výsledky pravidelných úloh, připomínky, oznámení.</p>
<p>Discord umí i hlas: příchozí hlasové zprávy přepisuje, <code>/voice tts</code> zapne odpovědi
mluveným slovem a bot se umí připojit do hlasového kanálu. Podrobnosti má stránka o hlasovém režimu.</p>

<h2>5. Bezpečnost</h2>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔐</span><div>Bez <code>DISCORD_ALLOWED_USERS</code> i <code>DISCORD_ALLOWED_ROLES</code> Hermes <strong>všechny odmítne</strong>.
To je záměr: autorizovaný uživatel má plný přístup k nástrojům agenta, tedy i k serveru, kde běží.
Nikdy nedávejte přístup celému serveru jen proto, že je to pohodlnější.</div></div>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Bot je online, ale neodpovídá</td><td>Chybí allowlist (bot odmítá všechny), nebo zpráva neobsahuje označení</td></tr>
<tr><td>Bot se vůbec nepřipojí</td><td>Message Content Intent, viz začátek stránky</td></tr>
<tr><td>Nevidí uživatele</td><td>Server Members Intent je vypnutý</td></tr>
<tr><td>Odpovídá ve špatném kanále</td><td>Přidejte kanál do <code>DISCORD_FREE_RESPONSE_CHANNELS</code>, nebo naopak omezujte přes <code>DISCORD_ALLOWED_CHANNELS</code></td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/telegram-a-discord/"><strong>Telegram a Discord — začátky</strong><span>Nejrychlejší cesta k první zprávě</span></a>
<a href="/wiki/zaciname/bezpecnost/"><strong>Bezpečnost</strong><span>Kdo smí co a jak to omezit</span></a>
<a href="/wiki/zaciname/pravidelne-ulohy/"><strong>Pravidelné úlohy</strong><span>Co má chodit do domovského kanálu</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Discord do posledního detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Nastavení
1) Developer Portal -> New Application, Bot -> Add Bot -> token (DISCORD_BOT_TOKEN)
2) Privileged Gateway Intents: Server Members ON (povinné), Message Content ON (povinné), Presence volitelné
3) Pozvánka: Installation (scopes bot + applications.commands) nebo URL
   https://discord.com/oauth2/authorize?client_id=APP_ID&scope=bot+applications.commands&permissions=309237763136
   Minimální oprávnění: View Channels, Send Messages, Embed Links, Attach Files, Read Message History;
   navíc Create Public Threads, Send Messages in Threads.

## Přístup (.env)
DISCORD_BOT_TOKEN · DISCORD_ALLOWED_USERS (čárkou; bez něj i bez rolí Hermes všechny odmítne)
· DISCORD_ALLOWED_ROLES (OR s users, auto-zapne Members intent) · DISCORD_ALLOWED_CHANNELS
· DISCORD_REQUIRE_MENTION (výchozí true v kanálech) · DISCORD_FREE_RESPONSE_CHANNELS
ID kopírovat s Developer Mode; přezdívky se nepárují.

## Chování
DM: odpovídá na vše, vlastní sezení · kanály: jen na @označení (nebo free-response kanály)
· vlákna: odpovídá ve vlákně, oddělená historie · víc lidí v kanále: historie zvlášť pro každého
· fóra: každé odeslání = nové vlákno.

## Domovský kanál
/sethome nebo DISCORD_HOME_CHANNEL + DISCORD_HOME_CHANNEL_NAME. Chodí tam cron a oznámení.

## Hlas
Příchozí hlasové zprávy přepisuje, /voice tts zapne mluvené odpovědi, umí se připojit do hlasového kanálu.

## Potíže
Online, ale neodpovídá -> chybí allowlist nebo označení. Nepřipojí se -> Message Content Intent.
Nevidí uživatele -> Members intent. Špatný kanál -> FREE_RESPONSE_CHANNELS / ALLOWED_CHANNELS.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🎮</span><div><strong>When a Discord bot stays offline, 90 % of the time the “Message Content Intent” is missing.</strong>
Discord does not hand message content to bots by default. Hermes always asks for it, and while the
switch is off in the Developer Portal Discord <strong>refuses the connection</strong> — the bot never
comes online. The second required switch is <em>Server Members Intent</em> (without it usernames cannot
be resolved).</div></div>

<h2>1. Application and bot</h2>
<div class="code-block">1) discord.com/developers/applications → New Application (name = bot name)
2) Bot → Add Bot → copy the token (DISCORD_BOT_TOKEN)
3) Privileged Gateway Intents:
     Server Members Intent   → ON   (required)
     Message Content Intent  → ON   (required!)
     Presence Intent         → optional
4) Installation (or a manual URL): scopes “bot” + “applications.commands”</div>
<div class="code-block"><span class="c"># minimum bot permissions</span>
View Channels · Send Messages · Embed Links · Attach Files · Read Message History
<span class="c"># recommended extras</span>
Create Public Threads · Send Messages in Threads</div>
<div class="code-block"><span class="c"># manual invite (replace YOUR_APP_ID)</span>
https://discord.com/oauth2/authorize?client_id=YOUR_APP_ID&scope=bot+applications.commands&permissions=309237763136</div>

<h2>2. User IDs and access</h2>
<table class="wiki-tabulka">
<tr><th>Setting</th><th>Meaning</th></tr>
<tr><td><code>DISCORD_BOT_TOKEN</code></td><td>The bot token</td></tr>
<tr><td><code>DISCORD_ALLOWED_USERS</code></td><td>Numeric user IDs (comma-separated). Without this and without roles Hermes <strong>denies everyone</strong> — a safe default</td></tr>
<tr><td><code>DISCORD_ALLOWED_ROLES</code></td><td>Role IDs — anyone holding the role is authorised (handy for rotating moderator teams)</td></tr>
<tr><td><code>DISCORD_ALLOWED_CHANNELS</code></td><td>Restrict the bot to specific channels</td></tr>
<tr><td><code>DISCORD_REQUIRE_MENTION</code></td><td>Whether a mention is required (default yes in channels)</td></tr>
<tr><td><code>DISCORD_FREE_RESPONSE_CHANNELS</code></td><td>Channels where the bot answers without a mention</td></tr>
</table>
<p class="note">Copy IDs after enabling <em>Developer Mode</em> in Discord (User Settings → Advanced).
Usernames work as a convenience but server nicknames are never matched — anyone can change those.</p>

<h2>3. How the bot behaves</h2>
<table class="wiki-tabulka">
<tr><th>Where</th><th>Behaviour</th></tr>
<tr><td>Direct messages</td><td>Answers everything; each DM has its own session</td></tr>
<tr><td>Server channels</td><td>By default only when <code>@mentioned</code>; otherwise it ignores the message</td></tr>
<tr><td>Mention-free channels</td><td>Answers continuously (good for a “work” channel); optionally one thread per top-level message</td></tr>
<tr><td>Threads</td><td>Replies in the same thread; thread history stays separate from the channel</td></tr>
<tr><td>Several people in one channel</td><td>History is kept <strong>per user</strong> by default — two people do not overwrite each other's context</td></tr>
<tr><td>Forum channels</td><td>Every send creates a new thread (forums accept no direct messages)</td></tr>
</table>

<h2>4. Home channel and voice</h2>
<div class="code-block"><span class="c"># from a channel the bot is in</span>
/sethome

<span class="c"># or in .env</span>
DISCORD_HOME_CHANNEL=123456789012345678
DISCORD_HOME_CHANNEL_NAME="#bot-updates"</div>
<p>Proactive messages go to the home channel: scheduled job results, reminders, notifications.</p>
<p>Discord also supports voice: incoming voice messages are transcribed, <code>/voice tts</code> enables
spoken replies, and the bot can join a voice channel. The voice-mode page has the details.</p>

<h2>5. Security</h2>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔐</span><div>Without <code>DISCORD_ALLOWED_USERS</code> or <code>DISCORD_ALLOWED_ROLES</code> Hermes <strong>denies everyone</strong>.
That is deliberate: an authorised user gets full access to the agent's tools, and therefore to the host.
Never open the bot to a whole server just because it is convenient.</div></div>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>Online but not answering</td><td>No allowlist (bot denies everyone), or the message had no mention</td></tr>
<tr><td>Never connects at all</td><td>Message Content Intent — see the top of the page</td></tr>
<tr><td>Cannot resolve users</td><td>Server Members Intent is off</td></tr>
<tr><td>Answers in the wrong channel</td><td>Add the channel to <code>DISCORD_FREE_RESPONSE_CHANNELS</code>, or restrict with <code>DISCORD_ALLOWED_CHANNELS</code></td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/telegram-and-discord/"><strong>Telegram and Discord — the basics</strong><span>The fastest path to a first message</span></a>
<a href="/en/wiki/getting-started/security/"><strong>Security</strong><span>Who may do what and how to limit it</span></a>
<a href="/en/wiki/getting-started/scheduled-tasks/"><strong>Scheduled tasks</strong><span>What lands in the home channel</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Discord down to the last detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Setup
1) Developer Portal -> New Application, Bot -> Add Bot -> token (DISCORD_BOT_TOKEN)
2) Privileged Gateway Intents: Server Members ON (required), Message Content ON (required), Presence optional
3) Invite: Installation (scopes bot + applications.commands) or the URL
   https://discord.com/oauth2/authorize?client_id=APP_ID&scope=bot+applications.commands&permissions=309237763136
   Minimum permissions: View Channels, Send Messages, Embed Links, Attach Files, Read Message History;
   plus Create Public Threads, Send Messages in Threads.

## Access (.env)
DISCORD_BOT_TOKEN · DISCORD_ALLOWED_USERS (comma-separated; without it and roles Hermes denies everyone)
· DISCORD_ALLOWED_ROLES (OR with users, auto-enables Members intent) · DISCORD_ALLOWED_CHANNELS
· DISCORD_REQUIRE_MENTION (default true in channels) · DISCORD_FREE_RESPONSE_CHANNELS
Copy IDs with Developer Mode; nicknames are never matched.

## Behaviour
DMs: answers everything, own session · channels: only on @mention (or free-response channels)
· threads: replies in-thread, separate history · several people in a channel: history per user
· forums: every send creates a new thread.

## Home channel
/sethome or DISCORD_HOME_CHANNEL + DISCORD_HOME_CHANNEL_NAME. Cron and notifications land there.

## Voice
Transcribes incoming voice messages, /voice tts enables spoken replies, can join a voice channel.

## Troubleshooting
Online but silent -> missing allowlist or mention. Never connects -> Message Content Intent.
Cannot resolve users -> Members intent. Wrong channel -> FREE_RESPONSE_CHANNELS / ALLOWED_CHANNELS.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(32)
    stranka = najdi(32)
    assert stranka and stranka["nazev"] == "Discord — server a bot"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Discord — server, bot a oprávnění bez zmatků",
        "Jak bota pozvat na server, které přepínače musí být zapnuté, jak omezit přístup rolemi a proč bot ve výchozím stavu odpovídá jen na označení.",
        OBRAZEK, "Wiki · Integrace", "Discord — server a bot",
        "Když Discord bot zůstane offline, téměř vždy chybí Message Content Intent. Nastavení, oprávnění a chování v kanálech.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Discord — server a bot (česká wiki)", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Discord — server, bot and permissions without the confusion",
        "How to invite the bot, which switches must be on, how to gate access with roles and why the bot answers only on mention by default.",
        OBRAZEK, "Wiki · Integrations", "Discord — server and bot",
        "When a Discord bot stays offline it is almost always the Message Content Intent. Setup, permissions and channel behaviour.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Discord — server and bot (community wiki)", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
