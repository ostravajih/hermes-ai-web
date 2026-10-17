#!/usr/bin/env python3
"""Postaví stránku wiki „SMS přes Twilio" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-messaging-sms.md (Twilio účet a číslo, proměnné, webhook
a ověřování podpisu, allowlist čísel, domovský kanál pro cron).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/messaging/sms"
OBRAZEK = "wiki-sms"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">✉️</span><div><strong>SMS je nejdražší a nejhloupější kanál — a přesto se hodí.</strong>
Nemá historii, neumí formátování a každá zpráva něco stojí. Na druhou stranu dojde tam, kde WhatsApp
ani Telegram nemá kdo otevřít: na obyčejný telefon. Používejte ji na <em>upozornění a krátké dotazy</em>,
ne na práci s přílohami.</div></div>

<h2>Co k tomu potřebujete</h2>
<table class="wiki-tabulka">
<tr><th>Věc</th><th>Poznámka</th></tr>
<tr><td>Účet Twilio</td><td>Má zkušební režim; zkušební číslo ale odpovídá jen ověřeným číslům</td></tr>
<tr><td>Číslo s podporou SMS</td><td>U Twilia koupené číslo (v ČR obvykle české nebo mezinárodní)</td></tr>
<tr><td>Veřejně dostupný server</td><td>Twilio posílá příchozí SMS na webhook — potřebujete HTTPS adresu</td></tr>
<tr><td><code>aiohttp</code> v prostředí</td><td>Doplní instalace závislostí pro režim <code>sms</code></td></tr>
</table>

<h2>Nastavení</h2>
<div class="code-block"><span class="c"># ~/.hermes/.env</span>
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=vas_auth_token
TWILIO_PHONE_NUMBER=+420777123456

<span class="c"># komu smí agent odepisovat (doporučeno vždy)</span>
SMS_ALLOWED_USERS=+420777654321,+420777222333

<span class="c"># kam chodí výsledky pravidelných úloh</span>
SMS_HOME_CHANNEL=+420777654321

<span class="c"># musí přesně odpovídat adrese nastavené u Twilia</span>
SMS_WEBHOOK_URL=https://vas-server:8080/webhooks/twilio</div>
<div class="code-block">hermes gateway setup      <span class="c"># nebo průvodcem: vybrat SMS (Twilio)</span></div>

<h2>Webhook u Twilia</h2>
<div class="code-block">Twilio Console → Phone Numbers → Manage → Active Numbers → vaše číslo
  Messaging → A MESSAGE COMES IN
  Webhook:  https://vas-server:8080/webhooks/twilio
  Method:   POST</div>
<p class="note">Když běží Hermes na domácím počítači, vystavte port dočasně tunelem
(<code>cloudflared tunnel --url http://localhost:8080</code> nebo <code>ngrok http 8080</code>) a jeho
adresu vložte jak do Twilia, tak do <code>SMS_WEBHOOK_URL</code>. Bez shody adres adaptér
<strong>odmítne nastartovat</strong> — je to ochrana proti podvrženým požadavkům.</p>

<h2>Bezpečnost</h2>
<table class="wiki-tabulka">
<tr><th>Opatření</th><th>Proč</th></tr>
<tr><td><code>SMS_ALLOWED_USERS</code></td><td>Bez něj odpovídá agent komukoli, kdo zná vaše číslo — a SMS posílá na cizí účet</td></tr>
<tr><td>Ověřování podpisu</td><td>Twilio podepisuje požadavky; <code>SMS_INSECURE_NO_SIGNATURE</code> patří jen na testování</td></tr>
<tr><td>Veřejná adresa jen přes HTTPS</td><td>HTTP tunelem je pozvánka pro cizí požadavky</td></tr>
<tr><td>Rozpočet</td><td>SMS se platí za kus; nastavte si limit u Twilia a hlídejte spotřebu</td></tr>
</table>

<h2>Kolik to stojí</h2>
<p>Cena má dvě části: <strong>měsíční poplatek za číslo</strong> a <strong>cena za odeslanou/přijatou SMS</strong>
(u nás se pohybuje v řádu korun za zprávu, přesná částka závisí na zemi a operátorovi). Ceník Twilia se
mění — před nasazením si ho ověřte v konzoli. Pro srovnání: Telegram i WhatsApp jsou zdarma, takže SMS
dává smysl jen tam, kde jiná cesta není.</p>

<h2>Na co si dát pozor</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Na zkušebním účtu zprávy nedorazí</td><td>Zkušební číslo odpovídá jen ověřeným číslům; ověřte je v konzoli</td></tr>
<tr><td>Agent mlčí</td><td>Chybí <code>SMS_WEBHOOK_URL</code>, nebo nesouhlasí s adresou u Twilia</td></tr>
<tr><td>Odpovídá i cizím lidem</td><td>Chybí allowlist — doplňte ho hned</td></tr>
<tr><td>Dlouhá odpověď se rozpadne</td><td>SMS má limit znaků a diakritika ho zkracuje; pište krátce</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/integrace/telegram/"><strong>Telegram — provoz bota</strong><span>Zdarma a s přílohami</span></a>
<a href="/wiki/integrace/whatsapp/"><strong>WhatsApp</strong><span>Když adresát používá WhatsApp</span></a>
<a href="/wiki/zaciname/pravidelne-ulohy/"><strong>Pravidelné úlohy</strong><span>Co má chodit jako SMS</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/sms" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>SMS a Twilio do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## K čemu
SMS dojde i tam, kde nikdo neotevře WhatsApp/Telegram. Hodí se na upozornění a krátké dotazy;
ne na přílohy a dlouhé texty. Platí se za číslo i za každou zprávu.

## Potřeby
Twilio účet + číslo s SMS · veřejný HTTPS webhook · aiohttp (extra "sms").

## Nastavení (.env)
TWILIO_ACCOUNT_SID · TWILIO_AUTH_TOKEN · TWILIO_PHONE_NUMBER (E.164) · SMS_ALLOWED_USERS (doporučeno vždy)
· SMS_HOME_CHANNEL (cron) · SMS_WEBHOOK_URL (musí přesně odpovídat adrese u Twilia, jinak adaptér nenastartuje).
Průvodce: hermes gateway setup -> SMS (Twilio).

## Webhook u Twilia
Phone Numbers -> Active Numbers -> číslo -> Messaging -> A MESSAGE COMES IN -> URL https://server:8080/webhooks/twilio, POST.
Lokálně: cloudflared tunnel --url http://localhost:8080 nebo ngrok http 8080; stejnou adresu do SMS_WEBHOOK_URL.

## Bezpečnost
SMS_ALLOWED_USERS (jinak agent odpovídá komukoli) · ověřování podpisu (SMS_INSECURE_NO_SIGNATURE jen na test)
· HTTPS · limit útraty u Twilia.

## Pozor
Zkušební číslo jen ověřená čísla · chybějící/nestejná webhook adresa · allowlist · diakritika zkracuje SMS.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">✉️</span><div><strong>SMS is the dumbest and most expensive channel — and still useful.</strong>
It has no history, no formatting, and every message costs money. On the other hand it arrives where
neither WhatsApp nor Telegram will be opened: on a plain phone. Use it for <em>notifications and short
questions</em>, not for attachments.</div></div>

<h2>What you need</h2>
<table class="wiki-tabulka">
<tr><th>Item</th><th>Note</th></tr>
<tr><td>A Twilio account</td><td>It has a trial mode; a trial number only messages verified numbers</td></tr>
<tr><td>An SMS-capable number</td><td>A number bought at Twilio</td></tr>
<tr><td>A publicly reachable server</td><td>Twilio delivers incoming SMS to a webhook — you need an HTTPS address</td></tr>
<tr><td><code>aiohttp</code> in the environment</td><td>Installed by the dependency step for the <code>sms</code> extra</td></tr>
</table>

<h2>Configuration</h2>
<div class="code-block"><span class="c"># ~/.hermes/.env</span>
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+420777123456

<span class="c"># who the agent may answer (always recommended)</span>
SMS_ALLOWED_USERS=+420777654321,+420777222333

<span class="c"># where scheduled job results go</span>
SMS_HOME_CHANNEL=+420777654321

<span class="c"># must match the URL configured at Twilio exactly</span>
SMS_WEBHOOK_URL=https://your-server:8080/webhooks/twilio</div>
<div class="code-block">hermes gateway setup      <span class="c"># or via the wizard: pick SMS (Twilio)</span></div>

<h2>The Twilio webhook</h2>
<div class="code-block">Twilio Console → Phone Numbers → Manage → Active Numbers → your number
  Messaging → A MESSAGE COMES IN
  Webhook:  https://your-server:8080/webhooks/twilio
  Method:   POST</div>
<p class="note">Running Hermes on a home machine? Expose the port temporarily with a tunnel
(<code>cloudflared tunnel --url http://localhost:8080</code> or <code>ngrok http 8080</code>) and put the
same URL in both Twilio and <code>SMS_WEBHOOK_URL</code>. Without the match the adapter
<strong>refuses to start</strong> — protection against forged requests.</p>

<h2>Security</h2>
<table class="wiki-tabulka">
<tr><th>Measure</th><th>Why</th></tr>
<tr><td><code>SMS_ALLOWED_USERS</code></td><td>Without it the agent answers anyone who knows your number — and sends SMS on your bill</td></tr>
<tr><td>Signature validation</td><td>Twilio signs requests; <code>SMS_INSECURE_NO_SIGNATURE</code> is for testing only</td></tr>
<tr><td>HTTPS only</td><td>An HTTP tunnel is an invitation for foreign requests</td></tr>
<tr><td>A budget</td><td>SMS is billed per message; set a cap at Twilio and watch the spend</td></tr>
</table>

<h2>What it costs</h2>
<p>Two parts: a <strong>monthly number fee</strong> and a <strong>per-message price</strong>. Twilio's price
list changes — check it in the console before deploying. For comparison: Telegram and WhatsApp are free,
so SMS only makes sense where nothing else works.</p>

<h2>Things to watch</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>Messages vanish on a trial account</td><td>A trial number only messages verified numbers; verify them in the console</td></tr>
<tr><td>The agent stays silent</td><td><code>SMS_WEBHOOK_URL</code> is missing or does not match the Twilio URL</td></tr>
<tr><td>It answers strangers</td><td>No allowlist — add one immediately</td></tr>
<tr><td>A long answer falls apart</td><td>SMS has a character limit and diacritics shorten it; keep it short</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/integrations/telegram/"><strong>Telegram — running the bot</strong><span>Free, with attachments</span></a>
<a href="/en/wiki/integrations/whatsapp/"><strong>WhatsApp</strong><span>When the recipient uses WhatsApp</span></a>
<a href="/en/wiki/getting-started/scheduled-tasks/"><strong>Scheduled tasks</strong><span>What should arrive as an SMS</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/sms" target="_blank" rel="noopener"><strong>Official documentation</strong><span>SMS and Twilio in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What for
SMS arrives where nobody opens WhatsApp/Telegram. Good for alerts and short questions, not attachments
or long text. You pay for the number and per message.

## Requirements
Twilio account + SMS-capable number · public HTTPS webhook · aiohttp (the "sms" extra).

## Configuration (.env)
TWILIO_ACCOUNT_SID · TWILIO_AUTH_TOKEN · TWILIO_PHONE_NUMBER (E.164) · SMS_ALLOWED_USERS (always)
· SMS_HOME_CHANNEL (cron) · SMS_WEBHOOK_URL (must match Twilio exactly or the adapter will not start).
Wizard: hermes gateway setup -> SMS (Twilio).

## Twilio webhook
Phone Numbers -> Active Numbers -> number -> Messaging -> A MESSAGE COMES IN -> https://server:8080/webhooks/twilio, POST.
Locally: cloudflared tunnel --url http://localhost:8080 or ngrok http 8080; same URL into SMS_WEBHOOK_URL.

## Security
SMS_ALLOWED_USERS (otherwise it answers anyone) · signature validation (SMS_INSECURE_NO_SIGNATURE is test-only)
· HTTPS · a spend cap at Twilio.

## Watch out
Trial number only messages verified numbers · missing/mismatched webhook URL · allowlist · diacritics shorten SMS.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(34)
    stranka = najdi(34)
    assert stranka and stranka["nazev"] == "SMS přes Twilio"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "SMS přes Twilio — kdy se hodí a kolik to stojí",
        "Nastavení SMS bota: Twilio účet a číslo, veřejný webhook s ověřením podpisu, allowlist čísel, domovský kanál pro cron a na co si dát pozor.",
        OBRAZEK, "Wiki · Integrace", "SMS přes Twilio",
        "SMS je nejdražší a nejhloupější kanál — a přesto se hodí. Kdy, jak a za kolik.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "SMS přes Twilio (česká wiki)", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "SMS via Twilio — when it makes sense and what it costs",
        "Setting up an SMS bot: a Twilio account and number, a public webhook with signature validation, a number allowlist, a home channel for cron and the pitfalls.",
        OBRAZEK, "Wiki · Integrations", "SMS via Twilio",
        "SMS is the dumbest and most expensive channel — and still useful. When, how and for how much.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "SMS via Twilio (community wiki)", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
