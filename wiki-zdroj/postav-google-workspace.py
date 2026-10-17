#!/usr/bin/env python3
"""Postaví stránku wiki „Google Workspace" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-skills-google-workspace.md (OAuth2 setup přes agenta,
Gmail hledání/čtení/odesílání, Calendar s časovými pásmy, Drive, Sheets, Docs, Contacts; poznámka
o himalaya skillu pro e-mail bez Google Cloud projektu).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/skills/google-workspace"
OBRAZEK = "wiki-google-workspace"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📨</span><div><strong>Nejdřív si odpovězte na jednu otázku: potřebujete e-mail, nebo celý Workspace?</strong>
Když jen posílat a číst poštu, stačí <em>himalaya</em> skill s heslem aplikace — hotové za dvě minuty
a bez Google Cloud projektu. Google Workspace skill je na Gmail <strong>plus</strong> Kalendář, Disk,
Tabulky a Dokumenty, a proto potřebuje OAuth přes cloudový projekt.</div></div>

<h2>Dvě cesty k poště</h2>
<table class="wiki-tabulka">
<tr><th></th><th>himalaya (jen e-mail)</th><th>Google Workspace skill</th></tr>
<tr><td>Nastavení</td><td>Heslo aplikace, 2 minuty</td><td>Google Cloud projekt, OAuth, 15–30 minut</td></tr>
<tr><td>Umí</td><td>Číst, hledat, posílat poštu</td><td>Gmail, Kalendář, Disk, Tabulky, Dokumenty, Kontakty</td></tr>
<tr><td>Přístup</td><td>IMAP/SMTP s heslem</td><td>OAuth2 s obnovováním tokenu</td></tr>
<tr><td>Pro běžného uživatele</td><td>Skoro vždy stačí</td><td>Když agent opravdu musí plánovat schůzky a pracovat se soubory</td></tr>
</table>

<h2>Nastavení Workspace skillu</h2>
<p>Celé nastavení vede sám agent — řeknete mu, ať Google Workspace nastaví, a on vás provede:</p>
<div class="code-block">1) založit projekt v Google Cloud a zapnout API:
   Gmail, Calendar, Drive, Sheets, Docs, People
2) vytvořit OAuth 2.0 přihlašovací údaje typu „Desktop app“
   a stáhnout JSON s client secret
3) autorizovat: agent vygeneruje odkaz, vy ho v prohlížeči schválíte
   a vložíte zpět adresu, na kterou vás to přesměrovalo
4) hotovo — token se od té chvíle obnovuje sám</div>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔐</span><div>Soubor s client secret a vzniklý token jsou
<strong>přihlašovací údaje k vaší poště</strong>. Nikdy je nedávejte do gitu ani do chatu. Když je
projekt zbytečný, zrušte autorizaci v Google účtu (Zabezpečení → Aplikace třetích stran).</div></div>

<h2>Co agent umí</h2>
<table class="wiki-tabulka">
<tr><th>Oblast</th><th>Příklady</th></tr>
<tr><td>Gmail — hledání</td><td><code>is:unread</code>, <code>from:sef@firma.cz newer_than:1d</code>, <code>has:attachment filename:pdf</code></td></tr>
<tr><td>Gmail — čtení a odesílání</td><td>Přečte tělo zprávy; pošle text, HTML i kopii (CC), umí i zobrazované jméno odesílatele</td></tr>
<tr><td>Kalendář</td><td>Vypíše události, založí schůzku s místem a účastníky, smaže událost</td></tr>
<tr><td>Disk</td><td>Hledání souborů (i podle typu přes raw dotaz)</td></tr>
<tr><td>Tabulky</td><td>Čtení rozsahu, zápis, přidávání řádků</td></tr>
<tr><td>Dokumenty a kontakty</td><td>Text dokumentu, seznam kontaktů</td></tr>
</table>
<p class="note"><strong>Kalendář vyžaduje časové pásmo.</strong> Čas jako <code>2026-03-01T10:00:00</code>
bez <code>+01:00</code> nebo <code>Z</code> se bere jako UTC — a schůzka pak vyjde o hodinu nebo dvě jinde.
Vždy pište posun: <code>2026-03-01T10:00:00+01:00</code>.</p>

<h2>Na co si dát pozor</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Autorizace skončí chybou „redirect_uri_mismatch“</td><td>Přihlašovací údaje nejsou typu Desktop app, nebo se vkládá jiná adresa, než kterou Google vrátil</td></tr>
<tr><td>Po měsíci přestane fungovat</td><td>Projekt v Google Cloud je v režimu testování — tokeny v něm vyprší; publikujte aplikaci nebo obnovte autorizaci</td></tr>
<tr><td>Agent nevidí nové zprávy</td><td>Ověřte, že skilly jsou zapnuté a že projekt má opravdu povolené Gmail API</td></tr>
<tr><td>Chcete jen poštu a nic víc</td><td>Použijte himalaya — méně práce a méně oprávnění</td></tr>
</table>

<h2>Jak to používáme</h2>
<p>Pro poštu máme himalaya (rychlé, bez cloudu), Workspace skill nasazujeme tam, kde agent opravdu
pracuje s kalendářem — třeba když z e-mailu pozná termín a má ho zapsat. Osvědčilo se:</p>
<table class="wiki-tabulka">
<tr><th>Zvyk</th><th>Proč</th></tr>
<tr><td>Agent jen <em>navrhne</em> schůzku, sám ji nezapisuje bez potvrzení</td><td>Chybně zapsaná schůzka v cizím kalendáři je horší než žádná</td></tr>
<tr><td>Posílat z vlastní adresy, ale se jménem robota</td><td>Příjemce pozná, že mu píše asistent, ne člověk</td></tr>
<tr><td>Heslo aplikace jen pro čtení, kde to jde</td><td>Menší dopad, když uteče</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/funkce/email-kalendar/"><strong>E-mail a kalendář</strong><span>Obecně: jak agentovi poštu a schůzky nastavit</span></a>
<a href="/wiki/zaciname/skilly/"><strong>Skilly</strong><span>Jak se skilly instalují a zapínají</span></a>
<a href="/wiki/integrace/github/"><strong>GitHub</strong><span>Druhá nejčastější integrace</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/skills/google-workspace" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Google Workspace skill (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Nejdřív volba
Jen e-mail -> himalaya skill (heslo aplikace, 2 min, bez Google Cloud projektu).
E-mail + Kalendář/Disk/Tabulky/Dokumenty -> Google Workspace skill (OAuth2, cloudový projekt).

## Nastavení Workspace
1) Google Cloud projekt, zapnout API: Gmail, Calendar, Drive, Sheets, Docs, People
2) OAuth 2.0 údaje typu Desktop app -> client secret JSON
3) Autorizace: agent vygeneruje URL, vy schválíte, vložíte zpět redirect URL
4) Token se dál obnovuje sám. Client secret a token = přihlašovací údaje -> nikdy do gitu/ chatu.

## Co umí
Gmail: hledání (is:unread, from:, newer_than:, has:attachment filename:pdf), čtení těla, odesílání
(text/HTML/CC, --from se jménem). Kalendář: list/create/delete, místo a účastníci.
Disk: hledání. Sheets: get/update/append. Docs: text. Contacts: list.

## Pozor
Kalendář MUSÍ mít časové pásmo (+01:00 nebo Z), jinak se bere UTC.
redirect_uri_mismatch = špatný typ údajů nebo jiná adresa.
Projekt v testovacím režimu = tokeny po čase vyprší (publikovat nebo obnovit autorizaci).
Chybí API v projektu -> agent nic nevidí.

## U nás
Pošta přes himalaya; Workspace tam, kde jde o kalendář. Agent schůzku navrhne, nezapisuje bez potvrzení;
posílá z vlastní adresy se jménem robota.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📨</span><div><strong>Answer one question first: do you need e-mail, or the whole Workspace?</strong>
If you only read and send mail, the <em>himalaya</em> skill with an app password is enough — two minutes
and no Google Cloud project. The Google Workspace skill is Gmail <strong>plus</strong> Calendar, Drive,
Sheets and Docs, which is why it needs OAuth through a cloud project.</div></div>

<h2>Two paths to mail</h2>
<table class="wiki-tabulka">
<tr><th></th><th>himalaya (e-mail only)</th><th>Google Workspace skill</th></tr>
<tr><td>Setup</td><td>App password, 2 minutes</td><td>Google Cloud project, OAuth, 15–30 minutes</td></tr>
<tr><td>Can do</td><td>Read, search, send mail</td><td>Gmail, Calendar, Drive, Sheets, Docs, Contacts</td></tr>
<tr><td>Access</td><td>IMAP/SMTP with a password</td><td>OAuth2 with token refresh</td></tr>
<tr><td>For most people</td><td>Almost always enough</td><td>When the agent must really schedule meetings and handle files</td></tr>
</table>

<h2>Setting up the Workspace skill</h2>
<p>The agent drives the whole setup — ask it to set up Google Workspace and it walks you through:</p>
<div class="code-block">1) create a Google Cloud project and enable the APIs:
   Gmail, Calendar, Drive, Sheets, Docs, People
2) create OAuth 2.0 credentials of type "Desktop app"
   and download the client secret JSON
3) authorise: the agent generates a link, you approve it in the browser
   and paste back the redirect URL
4) done — the token refreshes itself from then on</div>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔐</span><div>The client secret and the resulting token are
<strong>credentials to your mailbox</strong>. Never commit them or paste them into chat. If the project is
no longer needed, revoke access in your Google account (Security → Third-party apps).</div></div>

<h2>What the agent can do</h2>
<table class="wiki-tabulka">
<tr><th>Area</th><th>Examples</th></tr>
<tr><td>Gmail — search</td><td><code>is:unread</code>, <code>from:boss@co.com newer_than:1d</code>, <code>has:attachment filename:pdf</code></td></tr>
<tr><td>Gmail — read and send</td><td>Reads the body; sends text, HTML, CC, and can set the sender display name</td></tr>
<tr><td>Calendar</td><td>Lists events, creates a meeting with location and attendees, deletes an event</td></tr>
<tr><td>Drive</td><td>File search (including type queries via raw query)</td></tr>
<tr><td>Sheets</td><td>Read a range, write, append rows</td></tr>
<tr><td>Docs and Contacts</td><td>Document text, contact list</td></tr>
</table>
<p class="note"><strong>Calendar requires a timezone.</strong> A time like <code>2026-03-01T10:00:00</code>
without <code>+01:00</code> or <code>Z</code> is treated as UTC — and the meeting lands an hour or two off.
Always include the offset: <code>2026-03-01T10:00:00+01:00</code>.</p>

<h2>Things to watch</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>Authorisation fails with “redirect_uri_mismatch”</td><td>The credentials are not of type Desktop app, or you pasted a different URL than Google returned</td></tr>
<tr><td>It stops working after a month</td><td>The cloud project is in testing mode — tokens expire there; publish the app or re-authorise</td></tr>
<tr><td>The agent sees no new mail</td><td>Check the skills are enabled and the project really has the Gmail API switched on</td></tr>
<tr><td>You only want mail</td><td>Use himalaya — less work and fewer permissions</td></tr>
</table>

<h2>How we use it</h2>
<p>Mail runs through himalaya (fast, no cloud); the Workspace skill is deployed where the agent really
works with the calendar — for instance reading a date out of an e-mail and putting it in the calendar.
Two habits stuck:</p>
<table class="wiki-tabulka">
<tr><th>Habit</th><th>Why</th></tr>
<tr><td>The agent <em>proposes</em> a meeting instead of writing it unasked</td><td>A wrong entry in someone else's calendar is worse than none</td></tr>
<tr><td>Sending from our address but with a robot display name</td><td>Recipients can tell an assistant wrote it</td></tr>
<tr><td>Using read-only app passwords where possible</td><td>Less damage if one leaks</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/features/email-and-calendar/"><strong>E-mail and calendar</strong><span>The general setup for mail and meetings</span></a>
<a href="/en/wiki/getting-started/skills/"><strong>Skills</strong><span>How skills are installed and enabled</span></a>
<a href="/en/wiki/integrations/github/"><strong>GitHub</strong><span>The other most common integration</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/skills/google-workspace" target="_blank" rel="noopener"><strong>Official documentation</strong><span>The Google Workspace skill</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Choose first
E-mail only -> himalaya skill (app password, 2 minutes, no Google Cloud project).
E-mail + Calendar/Drive/Sheets/Docs -> Google Workspace skill (OAuth2, cloud project).

## Workspace setup
1) Google Cloud project, enable APIs: Gmail, Calendar, Drive, Sheets, Docs, People
2) OAuth 2.0 credentials of type Desktop app -> client secret JSON
3) Authorise: the agent generates a URL, you approve, paste back the redirect URL
4) The token refreshes itself. Client secret and token are credentials -> never in git or chat.

## Capabilities
Gmail: search (is:unread, from:, newer_than:, has:attachment filename:pdf), read body, send
(text/HTML/CC, --from display name). Calendar: list/create/delete with location and attendees.
Drive: search. Sheets: get/update/append. Docs: text. Contacts: list.

## Watch out
Calendar REQUIRES a timezone (+01:00 or Z), otherwise it is read as UTC.
redirect_uri_mismatch = wrong credential type or a different URL.
A project in testing mode expires tokens (publish or re-authorise).
Missing API in the project -> the agent sees nothing.

## Our practice
Mail via himalaya; Workspace where the calendar matters. The agent proposes meetings instead of writing
them unasked, and sends from our address with a robot display name.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(35)
    stranka = najdi(35)
    assert stranka and stranka["nazev"] == "Google Workspace"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Google Workspace — Gmail, Kalendář a Disk jako nástroje agenta",
        "Kdy stačí heslo aplikace a kdy je potřeba OAuth: nastavení Google Workspace skillu, co agent umí s poštou, kalendářem a tabulkami a na jaké chyby narazíte.",
        OBRAZEK, "Wiki · Integrace", "Google Workspace",
        "Nejdřív si odpovězte: potřebujete e-mail, nebo celý Workspace? Od toho se odvíjí celé nastavení.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Google Workspace (česká wiki)", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Google Workspace — Gmail, Calendar and Drive as agent tools",
        "When an app password is enough and when you need OAuth: setting up the Google Workspace skill, what the agent can do with mail, calendar and sheets, and which errors you will meet.",
        OBRAZEK, "Wiki · Integrations", "Google Workspace",
        "Answer one question first: do you need e-mail, or the whole Workspace? Everything else follows from that.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Google Workspace (community wiki)", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
