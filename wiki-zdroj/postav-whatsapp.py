#!/usr/bin/env python3
"""Postaví stránku wiki „WhatsApp" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-messaging-whatsapp.md (most přes Baileys — bez Meta účtu,
riziko omezení účtu, párování, proměnné, skupiny, více profilů) a user-guide-messaging-whatsapp-cloud.md
(oficiální Business Cloud API: Meta aplikace, WABA, trvalý token, veřejný webhook, ověřovací token).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp"
OBRAZEK = "wiki-whatsapp"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📱</span><div><strong>WhatsApp má dvě úplně různé cesty a plete se to u nich pořád.</strong>
Rychlý most (Baileys) se chová jako WhatsApp Web na vlastním čísle — nastavíte ho za pár minut,
nepotřebujete firemní účet, ale WhatsApp ho oficiálně netrpí. Business Cloud API je oficiální cesta
pro firmu: bez rizika zablokování, ale s firemním účtem, veřejnou HTTPS adresou a placením za konverzace.</div></div>

<h2>Kterou cestu zvolit</h2>
<table class="wiki-tabulka">
<tr><th></th><th>Most (Baileys)</th><th>Business Cloud API</th></tr>
<tr><td>Nastavení</td><td>Minuty — naskenujete QR kód</td><td>Hodiny — Meta aplikace, firemní portfolio, webhook</td></tr>
<tr><td>Účet</td><td>Stačí vaše číslo (ideálně samostatné)</td><td>Meta Business + WhatsApp Business Account</td></tr>
<tr><td>Veřejná adresa</td><td>Nepotřebujete</td><td>Potřebujete HTTPS webhook (např. Cloudflare Tunnel)</td></tr>
<tr><td>Riziko</td><td>Menší riziko omezení účtu (není oficiální)</td><td>Žádné — oficiální cesta</td></tr>
<tr><td>Platby</td><td>Zdarma</td><td>Platí se za konverzace podle ceníku Meta</td></tr>
<tr><td>Vhodné pro</td><td>Vlastní agent, rodinu, malý tým</td><td>Zákaznickou podporu, firmu</td></tr>
</table>

<h2>Cesta 1: rychlý most</h2>
<div class="code-block">hermes gateway setup      <span class="c"># vybrat WhatsApp a projít průvodcem</span></div>
<p>Průvodce vás nechá naskenovat QR kód (jako při přihlášení WhatsApp Web). Od té chvíle agent
odpovídá na zprávy na tom čísle.</p>
<table class="wiki-tabulka">
<tr><th>Nastavení</th><th>Význam</th></tr>
<tr><td><code>WHATSAPP_ENABLED</code></td><td>Zapnutí adaptéru</td></tr>
<tr><td><code>WHATSAPP_ALLOWED_USERS</code></td><td>Komu smí agent odpovídat (číslo v mezinárodním tvaru)</td></tr>
<tr><td><code>WHATSAPP_GROUP_POLICY</code></td><td>Jak se chovat ve skupinách</td></tr>
<tr><td><code>WHATSAPP_REQUIRE_MENTION</code></td><td>Zda musí být ve skupině označen</td></tr>
<tr><td><code>WHATSAPP_MODE</code></td><td>Režim bridge (viz dokumentace podle verze)</td></tr>
</table>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⚠️</span><div><strong>Tři pravidla, která snižují riziko omezení účtu:</strong>
používejte <em>samostatné číslo</em> (ne svoje osobní), neposílejte hromadné zprávy a nepište lidem,
kteří vám první nenapsali. Agent má konverzovat, ne rozesílat.</div></div>
<p class="note">WhatsApp občas změní protokol a most se na chvíli rozbije. Řešení je obvykle
aktualizovat Hermes a číslo znovu spárovat — ne hledat chybu v konfiguraci.</p>

<h2>Cesta 2: Business Cloud API</h2>
<div class="code-block">hermes whatsapp-cloud      <span class="c"># průvodce, který ověří každý údaj hned při vložení</span></div>
<table class="wiki-tabulka">
<tr><th>Co potřebujete</th><th>Kde to vznikne</th></tr>
<tr><td>Firemní portfolio a aplikace s WhatsApp</td><td>business.facebook.com, developers.facebook.com</td></tr>
<tr><td>Phone Number ID a WABA ID</td><td>API Setup ve vaší aplikaci</td></tr>
<tr><td>Trvalý přístupový token (produkce)</td><td>Systémový uživatel v Meta Business</td></tr>
<tr><td>Veřejná HTTPS adresa pro webhook</td><td>Cloudflare Tunnel (zdarma), ngrok, nebo reverzní proxy na VPS</td></tr>
<tr><td>Ověřovací token webhooku</td><td>Vymyslíte si ho a vložíte na obou stranách</td></tr>
</table>
<table class="wiki-tabulka">
<tr><th>Proměnná</th><th>K čemu</th></tr>
<tr><td><code>WHATSAPP_CLOUD_ACCESS_TOKEN</code></td><td>Trvalý token</td></tr>
<tr><td><code>WHATSAPP_CLOUD_PHONE_NUMBER_ID</code></td><td>ID čísla (ne samotné číslo — častá záměna)</td></tr>
<tr><td><code>WHATSAPP_CLOUD_WABA_ID</code></td><td>ID účtu WhatsApp Business</td></tr>
<tr><td><code>WHATSAPP_CLOUD_VERIFY_TOKEN</code></td><td>Ověření webhooku při registraci</td></tr>
<tr><td><code>WHATSAPP_CLOUD_ALLOWED_USERS</code></td><td>Komu smí agent odpovídat</td></tr>
</table>
<p class="note">Nejčastější past průvodce odchytí sám: do kolonky <em>Phone Number ID</em> se vkládá
dlouhé číselné ID, ne telefonní číslo. Když to prohodíte, API vrátí chybu, která vypadá jako špatný token.</p>

<h2>Co umí obě cesty</h2>
<table class="wiki-tabulka">
<tr><th>Vlastnost</th><th>Poznámka</th></tr>
<tr><td>Text, obrázky, soubory</td><td>Ano, v obou režimech</td></tr>
<tr><td>Hlasové zprávy</td><td>V Cloud API se odchozí hlasovka zobrazí jako „voice note“, když je na serveru <code>ffmpeg</code></td></tr>
<tr><td>Skupiny</td><td>Most je zvládá; Cloud API skupiny nepodporuje (jen individuální konverzace)</td></tr>
<tr><td>Doručování z cronu</td><td>Ano — do domovského chatu (<code>WHATSAPP_CLOUD_HOME_CHANNEL</code>)</td></tr>
</table>

<h2>Na co si dát pozor</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Agent neodpovídá na nové číslo</td><td>Chybí v allowlistu; zkontrolujte tvar čísla (mezinárodní, bez mezer)</td></tr>
<tr><td>Most po aktualizaci WhatsApp přestal fungovat</td><td>Aktualizovat Hermes a znovu spárovat</td></tr>
<tr><td>Cloud API hlásí chybu tokenu</td><td>Používáte testovací token, který vyprší — nasaďte trvalý</td></tr>
<tr><td>Webhook se neověří</td><td>Ověřovací token nesedí, nebo adresa není dostupná z internetu přes HTTPS</td></tr>
<tr><td>Podezření na omezení účtu</td><td>Přestaňte posílat hromadné zprávy; pro firmu přejděte na Cloud API</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/integrace/telegram/"><strong>Telegram — provoz bota</strong><span>Nejrychlejší chat pro vlastní agenta</span></a>
<a href="/wiki/integrace/sms/"><strong>SMS přes Twilio</strong><span>Když adresát nemá WhatsApp ani Telegram</span></a>
<a href="/wiki/funkce/webhooky/"><strong>Webhooky</strong><span>Veřejná adresa, kterou Cloud API potřebuje</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>WhatsApp most i Cloud API (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Dvě cesty
1) Most (Baileys): obdoba WhatsApp Web, hermes gateway setup -> QR. Bez Meta účtu, bez veřejné adresy,
   zdarma; není oficiální -> riziko omezení účtu. Pro osobní číslo nebo malý tým.
2) Business Cloud API: oficiální, bez rizika; Meta Business + WABA, trvalý token, veřejný HTTPS webhook
   (Cloudflare Tunnel), platba za konverzace. Průvodce: hermes whatsapp-cloud.

## Most — proměnné
WHATSAPP_ENABLED · WHATSAPP_ALLOWED_USERS · WHATSAPP_GROUP_POLICY · WHATSAPP_REQUIRE_MENTION · WHATSAPP_MODE.
Pravidla proti omezení účtu: samostatné číslo, žádné hromadné zprávy, nepsat lidem, kteří nenapsali první.
Po změně protokolu WhatsApp: aktualizovat Hermes a znovu spárovat.

## Cloud API — proměnné
WHATSAPP_CLOUD_ACCESS_TOKEN (trvalý!) · WHATSAPP_CLOUD_PHONE_NUMBER_ID (ID čísla, ne číslo)
· WHATSAPP_CLOUD_WABA_ID · WHATSAPP_CLOUD_VERIFY_TOKEN · WHATSAPP_CLOUD_ALLOWED_USERS
· WHATSAPP_CLOUD_HOME_CHANNEL. Testovací token vyprší -> používat trvalý.

## Co umí
Text/obrázky/soubory v obou · hlasovky (voice note s ffmpeg) · cron do domovského chatu
· skupiny jen v mostu (Cloud API ne).

## Pozor
Nové číslo není v allowlistu · mezinárodní tvar čísla · token expirace · ověřovací token webhooku
· hromadné zprávy = riziko blokace.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📱</span><div><strong>WhatsApp has two completely different paths and people mix them up constantly.</strong>
The quick bridge (Baileys) behaves like WhatsApp Web on your own number — set up in minutes, no business
account needed, but WhatsApp does not officially support it. The Business Cloud API is the official
route for a company: no ban risk, but a Meta business account, a public HTTPS address and per-conversation
billing.</div></div>

<h2>Which path to choose</h2>
<table class="wiki-tabulka">
<tr><th></th><th>Bridge (Baileys)</th><th>Business Cloud API</th></tr>
<tr><td>Setup</td><td>Minutes — scan a QR code</td><td>Hours — Meta app, business portfolio, webhook</td></tr>
<tr><td>Account</td><td>Your number (ideally a dedicated one)</td><td>Meta Business + WhatsApp Business Account</td></tr>
<tr><td>Public address</td><td>Not needed</td><td>HTTPS webhook needed (e.g. Cloudflare Tunnel)</td></tr>
<tr><td>Risk</td><td>Some risk of account restrictions (unofficial)</td><td>None — the official route</td></tr>
<tr><td>Cost</td><td>Free</td><td>Per conversation, per Meta's price list</td></tr>
<tr><td>Best for</td><td>Your own agent, family, a small team</td><td>Customer support, a business</td></tr>
</table>

<h2>Path 1: the quick bridge</h2>
<div class="code-block">hermes gateway setup      <span class="c"># pick WhatsApp and follow the wizard</span></div>
<p>The wizard has you scan a QR code (like signing in to WhatsApp Web). From then on the agent answers
messages on that number.</p>
<table class="wiki-tabulka">
<tr><th>Setting</th><th>Meaning</th></tr>
<tr><td><code>WHATSAPP_ENABLED</code></td><td>Turns the adapter on</td></tr>
<tr><td><code>WHATSAPP_ALLOWED_USERS</code></td><td>Who the agent may answer (international format)</td></tr>
<tr><td><code>WHATSAPP_GROUP_POLICY</code></td><td>How to behave in groups</td></tr>
<tr><td><code>WHATSAPP_REQUIRE_MENTION</code></td><td>Whether a mention is required in groups</td></tr>
<tr><td><code>WHATSAPP_MODE</code></td><td>Bridge mode (see the docs for your version)</td></tr>
</table>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⚠️</span><div><strong>Three rules that lower the risk of account restrictions:</strong>
use a <em>dedicated number</em> (not your personal one), do not send bulk messages, and do not message
people who have not written first. An agent should converse, not broadcast.</div></div>
<p class="note">WhatsApp occasionally changes its protocol and the bridge breaks for a while. The fix is
usually to update Hermes and re-pair the number — not to hunt for a configuration error.</p>

<h2>Path 2: Business Cloud API</h2>
<div class="code-block">hermes whatsapp-cloud      <span class="c"># a wizard that validates each value as you paste it</span></div>
<table class="wiki-tabulka">
<tr><th>What you need</th><th>Where it comes from</th></tr>
<tr><td>Business portfolio and an app with WhatsApp</td><td>business.facebook.com, developers.facebook.com</td></tr>
<tr><td>Phone Number ID and WABA ID</td><td>API Setup in your app</td></tr>
<tr><td>Permanent access token (production)</td><td>A system user in Meta Business</td></tr>
<tr><td>Public HTTPS address for the webhook</td><td>Cloudflare Tunnel (free), ngrok, or a reverse proxy on a VPS</td></tr>
<tr><td>Webhook verify token</td><td>You invent it and paste it on both sides</td></tr>
</table>
<table class="wiki-tabulka">
<tr><th>Variable</th><th>Purpose</th></tr>
<tr><td><code>WHATSAPP_CLOUD_ACCESS_TOKEN</code></td><td>The permanent token</td></tr>
<tr><td><code>WHATSAPP_CLOUD_PHONE_NUMBER_ID</code></td><td>The number ID (not the number itself — a common mix-up)</td></tr>
<tr><td><code>WHATSAPP_CLOUD_WABA_ID</code></td><td>WhatsApp Business account ID</td></tr>
<tr><td><code>WHATSAPP_CLOUD_VERIFY_TOKEN</code></td><td>Webhook verification during registration</td></tr>
<tr><td><code>WHATSAPP_CLOUD_ALLOWED_USERS</code></td><td>Who the agent may answer</td></tr>
</table>
<p class="note">The wizard catches the most common trap for you: the <em>Phone Number ID</em> field takes a
long numeric ID, not a phone number. Swap them and the API returns an error that looks like a bad token.</p>

<h2>What both paths can do</h2>
<table class="wiki-tabulka">
<tr><th>Feature</th><th>Note</th></tr>
<tr><td>Text, images, files</td><td>Yes, in both modes</td></tr>
<tr><td>Voice messages</td><td>In the Cloud API an outgoing voice message appears as a proper voice note when <code>ffmpeg</code> is present</td></tr>
<tr><td>Groups</td><td>The bridge handles them; the Cloud API does not (one-to-one only)</td></tr>
<tr><td>Scheduled delivery</td><td>Yes — to the home chat (<code>WHATSAPP_CLOUD_HOME_CHANNEL</code>)</td></tr>
</table>

<h2>Things to watch</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>A new number gets no answers</td><td>It is not in the allowlist; check the number format (international, no spaces)</td></tr>
<tr><td>The bridge stopped after a WhatsApp update</td><td>Update Hermes and re-pair</td></tr>
<tr><td>The Cloud API reports a token error</td><td>You are using a test token that expires — deploy the permanent one</td></tr>
<tr><td>The webhook will not verify</td><td>The verify token does not match, or the address is not reachable over HTTPS</td></tr>
<tr><td>Signs of an account restriction</td><td>Stop bulk messaging; for a business move to the Cloud API</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/integrations/telegram/"><strong>Telegram — running the bot</strong><span>The fastest chat for your own agent</span></a>
<a href="/en/wiki/integrations/sms/"><strong>SMS via Twilio</strong><span>When the recipient has neither WhatsApp nor Telegram</span></a>
<a href="/en/wiki/features/webhooks/"><strong>Webhooks</strong><span>The public address the Cloud API needs</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp" target="_blank" rel="noopener"><strong>Official documentation</strong><span>WhatsApp bridge and Cloud API</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Two paths
1) Bridge (Baileys): WhatsApp Web emulation, hermes gateway setup -> QR. No Meta account, no public URL,
   free; unofficial -> account restriction risk. For a personal number or small team.
2) Business Cloud API: official, no ban risk; Meta Business + WABA, permanent token, public HTTPS webhook
   (Cloudflare Tunnel), per-conversation billing. Wizard: hermes whatsapp-cloud.

## Bridge variables
WHATSAPP_ENABLED · WHATSAPP_ALLOWED_USERS · WHATSAPP_GROUP_POLICY · WHATSAPP_REQUIRE_MENTION · WHATSAPP_MODE.
Anti-restriction rules: dedicated number, no bulk messages, never message people who did not write first.
After a WhatsApp protocol change: update Hermes and re-pair.

## Cloud API variables
WHATSAPP_CLOUD_ACCESS_TOKEN (permanent!) · WHATSAPP_CLOUD_PHONE_NUMBER_ID (an ID, not a number)
· WHATSAPP_CLOUD_WABA_ID · WHATSAPP_CLOUD_VERIFY_TOKEN · WHATSAPP_CLOUD_ALLOWED_USERS
· WHATSAPP_CLOUD_HOME_CHANNEL. Test tokens expire -> use the permanent one.

## Capabilities
Text/images/files in both · voice notes (with ffmpeg) · cron to the home chat · groups only in the bridge
(Cloud API does not support them).

## Watch out
New number not in the allowlist · international number format · token expiry · webhook verify token
· bulk messaging = restriction risk.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(33)
    stranka = najdi(33)
    assert stranka and stranka["nazev"] == "WhatsApp"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "WhatsApp — most pro vlastní číslo nebo firemní Cloud API",
        "Dvě cesty k WhatsApp botovi: rychlý most bez firemního účtu (a s rizikem omezení) versus oficiální Business Cloud API s veřejným webhookem. Kdy kterou zvolit.",
        OBRAZEK, "Wiki · Integrace", "WhatsApp",
        "WhatsApp má dvě úplně různé cesty a plete se to u nich pořád. Kterou zvolit a na co si dát pozor.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "WhatsApp (česká wiki)", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "WhatsApp — a bridge for your own number or the business Cloud API",
        "Two paths to a WhatsApp bot: a quick bridge with no business account (and restriction risk) versus the official Business Cloud API with a public webhook. Which one to pick and when.",
        OBRAZEK, "Wiki · Integrations", "WhatsApp",
        "WhatsApp has two completely different paths and people mix them up constantly. Which one to choose and what to watch.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "WhatsApp (community wiki)", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
