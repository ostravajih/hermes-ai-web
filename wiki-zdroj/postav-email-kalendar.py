#!/usr/bin/env python3
"""Postaví stránku wiki „E-mail a kalendář" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-messaging-email.md (nastavení e-mailu jako platformy,
přístupová práva, ověřování odesílatele), guides-agent-email-address.md (vlastní adresa pro agenta
přes Himalaya), user-guide-skills-google-workspace.md (Gmail, Calendar, Drive, Sheets, Docs, OAuth).

Naše zkušenosti: pro vlastní doménu potřebujete SPF/DKIM/DMARC, jinak agent zprávy nezpracuje;
kalendář bez časového pásma si Google vyloží jako UTC.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/messaging/email"
OBRAZEK = "wiki-email-kalendar"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📬</span><div><strong>E-mail je pro agenta celý komunikační kanál, ne jen čtení pošty.</strong>
Můžete mu napsat z mobilu jako kolegovi, on odpoví a přitom udělá práci. Zvlášť se nastavuje
<em>vlastní adresa pro agenta</em> a zvlášť <em>přístup ke kalendáři</em> — jsou to dvě různé věci.</div></div>

<h2>Tři cesty, jak agenta k poště pustit</h2>
<table class="wiki-tabulka">
<tr><th>Cesta</th><th>Co umí</th><th>Co k tomu potřebujete</th></tr>
<tr><td><strong>E-mail jako kanál</strong> (gateway)</td><td>Píšete agentovi na adresu, on odpovídá; dá se použít pro pravidelné úlohy</td><td>Adresu, přístup přes IMAP a SMTP, heslo aplikace</td></tr>
<tr><td><strong>Vlastní adresa + Himalaya</strong></td><td>Agent sám kontroluje schránku a posílá poštu, bez trvale běžícího bota</td><td>Vlastní e-mailový účet a nástroj Himalaya</td></tr>
<tr><td><strong>Google Workspace</strong></td><td>Gmail, kalendář, Disk, Tabulky, Dokumenty a Kontakty</td><td>Projekt v Google Cloud a přihlášení přes OAuth (jednorázově)</td></tr>
</table>
<p class="note">Když chcete <strong>jen poštu</strong>, zvolte e-mail jako kanál nebo Himalayu —
nastavení je otázka minut. Google Workspace je na kalendář, Disk a Dokumenty, ale vyžaduje
projekt v Google Cloud a schvalování přístupu.</p>

<h2>E-mail jako kanál: nastavení</h2>
<ol class="kroky">
<li><p>Spusťte průvodce a vyberte E-mail (provede vás vším potřebným):</p>
<div class="code-block"><span class="p">❯</span> hermes gateway setup</div></li>
<li><p>Nebo to nastavte ručně v <code>~/.hermes/.env</code> — povinné čtyři údaje:</p>
<div class="code-block"><span class="c"># ~/.hermes/.env</span>
EMAIL_ADDRESS=agent@vasedomena.cz
EMAIL_PASSWORD=heslo aplikace        <span class="c"># pozor: ne vaše běžné heslo!</span>
EMAIL_IMAP_HOST=imap.vasedomena.cz
EMAIL_SMTP_HOST=smtp.vasedomena.cz</div></li>
<li><p>Doplňte, kdo smí psát, a identifikaci serveru (viz níž, je to bezpečnostní pojistka):</p>
<div class="code-block"><span class="c"># kdo smí agentovi psát (jinak se zprávy ignorují)</span>
EMAIL_ALLOWED_USERS=vy@vasedomena.cz,kolega@firma.cz
<span class="c"># identifikátor serveru, který přidává ověření do hlaviček zpráv</span>
EMAIL_AUTHSERV_ID=mx.google.com</div></li>
<li><p>Nechte to běžet. Buď napřímo, nebo jako službu, která se nastartuje se serverem:</p>
<div class="code-block"><span class="p">❯</span> hermes gateway                 <span class="c"># běží v popředí</span>
<span class="p">❯</span> hermes gateway install         <span class="c"># jako služba</span></div></li>
</ol>
<table class="wiki-tabulka">
<tr><th>Údaj</th><th>Výchozí</th><th>K čemu je</th></tr>
<tr><td><code>EMAIL_IMAP_PORT</code></td><td>993</td><td>Příjem pošty (zabezpečené spojení)</td></tr>
<tr><td><code>EMAIL_SMTP_PORT</code></td><td>587</td><td>Odesílání pošty</td></tr>
<tr><td><code>EMAIL_POLL_INTERVAL</code></td><td>15 vteřin</td><td>Jak často se schránka kontroluje</td></tr>
<tr><td><code>EMAIL_HOME_ADDRESS</code></td><td>—</td><td>Kam mají chodit výstupy pravidelných úloh</td></tr>
</table>
<p class="note">Při startu agent všechny zprávy ve schránce označí jako přečtené a zpracovává už jen
nové. Když tedy spouštíte e-mailový kanál poprvé, počítejte s tím, že historie se ignoruje.</p>

<h2>Kdo smí agentovi psát</h2>
<table class="wiki-tabulka">
<tr><th>Nastavení</th><th>Co se stane</th></tr>
<tr><td>Vyplněný seznam povolených</td><td>Zpracují se jen zprávy z těch adres</td></tr>
<tr><td>Prázdný seznam</td><td>Neznámí odesílatelé se <strong>tiše ignorují</strong> — nikdo nedostane ani odpověď</td></tr>
<tr><td>Režim <code>pair</code></td><td>Neznámý odesílatel dostane párovací kód (může se přidat)</td></tr>
<tr><td>Režim <code>decline</code></td><td>Neznámý odesílatel dostane jednu slušnou odpověď a pak nic (24 hodin)</td></tr>
</table>
<p><strong>Ověřování odesílatele:</strong> agent jedná, jen když server, který poštu přijal, potvrdí,
že zpráva opravdu pochází z uvedené domény (DMARC nebo SPF/DKIM). Proto je v nastavení
<code>EMAIL_AUTHSERV_ID</code> — musí přesně odpovídat tomu, co váš přijímací server píše do hlaviček.
Bez toho se dá <em>From:</em> v e-mailu podvrhnout a agent by poslouchal cizí příkazy.</p>

<h2>Kalendář a další služby Google</h2>
<p>Kalendář se neřeší přes e-mail, ale přes připravený postup pro Google Workspace. Ten vedle
kalendáře umí i Gmail, Disk, Tabulky, Dokumenty a Kontakty. Nastavení je jednorázové a vede vás jím
agent:</p>
<div class="code-block"><span class="p">❯</span> Nastav mi Google Workspace.</div>
<ol class="kroky">
<li>Vytvoří se projekt v Google Cloud a zapnou potřebná rozhraní (Gmail, Kalendář, Disk, Tabulky, Dokumenty, Kontakty).</li>
<li>Vytvoří se přihlašovací údaje typu desktopová aplikace a stáhne se soubor s tajemstvím.</li>
<li>Agent vygeneruje odkaz pro přihlášení — vy ho schválíte v prohlížeči a vložíte zpět adresu z prohlížeče.</li>
<li>Od té chvíle se přihlášení obnovuje samo.</li>
</ol>
<p>Práce s kalendářem pak vypadá takhle (příkazy zadáváte v rozhovoru, nemusíte je psát ručně):</p>
<div class="code-block"><span class="p">❯</span> Jaké mám zítra schůzky?
<span class="p">❯</span> Zapiš na čtvrtek od 10:00 na 30 minut konzultaci s Janem a pozvi ho.</div>
<p class="note"><strong>Pozor na časová pásma.</strong> Kalendář vyžaduje, aby u času bylo uvedeno
pásmo (například <code>+02:00</code> pro český letní čas) nebo aby šlo o světový čas. Když pásmo
chybí, bere se čas jako světový — a schůzka vám o dvě hodiny uteče.</p>

<h2>Pasti z našeho provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co se stalo</th><th>Co s tím</th></tr>
<tr><td><strong>Agent nezpracoval žádnou zprávu</strong></td><td>Nejčastěji nesouhlasí <code>EMAIL_AUTHSERV_ID</code> s tím, co píše váš server, nebo je adresa mimo seznam povolených. Obojí se pozná z logu služby</td></tr>
<tr><td><strong>Do schránky nechodily odpovědi</strong></td><td>U vlastní domény musí být v pořádku SPF, DKIM a DMARC. Bez nich pošta končí ve spamu nebo se zahazuje</td></tr>
<tr><td><strong>Agent poslouchal cizí adresu</strong></td><td>Nikdy nepoužívejte režim „povolit všechny“. Seznam povolených je to, co vás drží</td></tr>
<tr><td><strong>Přihlášení k e-mailu přestalo fungovat po změně hesla</strong></td><td>Heslo aplikace se musí aktualizovat i v nastavení — u některých poskytovatelů si ho vygenerujete znovu</td></tr>
<tr><td><strong>Schůzka se zapsala o dvě hodiny jinde</strong></td><td>Chybělo časové pásmo. Vždycky uveďte čas i s pásmem, nebo se před zápisem zeptejte, jak to agent pochopil</td></tr>
<tr><td><strong>V e-mailové schránce zůstaly stovky starých zpráv a agent na ně nereagoval</strong></td><td>To je správně — při startu se historie označí jako přečtená. Když potřebujete starší e-mail zpracovat, přepošlete ho znovu</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Zřiďte agentovi <strong>vlastní adresu</strong></td><td>Nepletení se s vaší pracovní poštou a jasný seznam, kdo mu smí psát</td></tr>
<tr><td>Do předmětu pište, o co jde</td><td>Agent podle předmětu lépe pozná úkol a vy si udržíte přehled ve vláknech</td></tr>
<tr><td>E-mail berte jako dopis, ne jako chat</td><td>Je veřejnější a pomalejší — na citlivé věci se hodí spíš chat nebo terminál</td></tr>
<tr><td>Pravidelné úlohy nechte posílat na jednu adresu</td><td>Nastavte <code>EMAIL_HOME_ADDRESS</code> a ranní přehledy vám budou chodit spolehlivě</td></tr>
<tr><td>Před plošným použitím si vyzkoušejte jeden e-mail</td><td>Ověříte ověřování odesílatele i odpovědi, než na tom postavíte provoz</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/telegram-a-discord/"><strong>Telegram a Discord</strong><span>Rychlejší kanál než e-mail</span></a>
<a href="/wiki/zaciname/pravidelne-ulohy/"><strong>Pravidelné úlohy (cron)</strong><span>Ranní přehled e-mailem</span></a>
<a href="/wiki/zaciname/bezpecnost/"><strong>Bezpečnost</strong><span>Kdo smí agenta ovládat</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/email" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>E-mailový kanál do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Tři cesty k poště
1) E-mail jako kanál (gateway) — píšete agentovi na adresu, on odpovídá; potřeba IMAP/SMTP + heslo aplikace.
2) Vlastní adresa + Himalaya — agent sám kontroluje schránku, bez trvale běžícího bota.
3) Google Workspace — Gmail, kalendář, Disk, Tabulky, Dokumenty, Kontakty (OAuth, projekt v Google Cloud).
Jen pošta -> cesta 1 nebo 2 (minuty). Kalendář -> cesta 3.

## Nastavení e-mailu jako kanálu
hermes gateway setup -> vybrat E-mail
~/.hermes/.env:
  EMAIL_ADDRESS, EMAIL_PASSWORD (heslo aplikace!), EMAIL_IMAP_HOST, EMAIL_SMTP_HOST
  EMAIL_ALLOWED_USERS=... (kdo smí psát) · EMAIL_AUTHSERV_ID=... (identifikátor přijímacího serveru)
Volitelné: EMAIL_IMAP_PORT 993, EMAIL_SMTP_PORT 587, EMAIL_POLL_INTERVAL 15 s, EMAIL_HOME_ADDRESS
Spuštění: hermes gateway (popředí) nebo hermes gateway install (služba)
Při startu se stávající zprávy označí jako přečtené — zpracovávají se jen nové.

## Kdo smí psát
Vyplněný seznam = jen ty adresy. Prázdný = neznámí se tiše ignorují. pair = párovací kód.
decline = jedna slušná odpověď a pak nic (24 h).
Ověřování: agent jedná jen když server potvrdí From (DMARC nebo SPF/DKIM) — proto EMAIL_AUTHSERV_ID.

## Kalendář (Google Workspace)
Nastavení vede agent: projekt v Google Cloud + rozhraní, OAuth údaje typu desktop, schválení v prohlížeči,
od té doby se přihlášení obnovuje samo.
Práce: "Jaké mám zítra schůzky?" / "Zapiš na čtvrtek od 10:00 konzultaci a pozvi Jana."
POZOR: čas musí mít pásmo (+02:00) nebo být v UTC; bez pásma se bere jako světový čas.

## Pasti z našeho provozu
1. Nic se nezpracuje -> nesouhlasí EMAIL_AUTHSERV_ID nebo adresa není v seznamu povolených (viz log služby).
2. Nedocházejí odpovědi -> u vlastní domény musí být SPF/DKIM/DMARC.
3. "Povolit všechny" = agent poslouchá kohokoli; seznam povolených je pojistka.
4. Změna hesla -> aktualizovat heslo aplikace i v nastavení.
5. Schůzka o dvě hodiny jinde -> chybějící časové pásmo.
6. Staré e-maily agent neřeší (označené jako přečtené při startu) -> přeposlat znovu.

## Tipy
Vlastní adresa pro agenta · smysluplný předmět · e-mail je dopis, ne chat (citlivé věci jinam) ·
EMAIL_HOME_ADDRESS pro ranní přehledy · nejdřív vyzkoušet jeden e-mail.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📬</span><div><strong>Email is a full communication channel for the agent, not just a way to read mail.</strong>
You can write to it from your phone like a colleague, it answers and does the work meanwhile.
<em>An address of its own</em> is set up separately from <em>access to your calendar</em> — two
different things.</div></div>

<h2>Three ways to give the agent email</h2>
<table class="wiki-tabulka">
<tr><th>Way</th><th>What it does</th><th>What you need</th></tr>
<tr><td><strong>Email as a channel</strong> (gateway)</td><td>You write to an address, the agent replies; works for scheduled jobs too</td><td>An address, IMAP and SMTP access, an app password</td></tr>
<tr><td><strong>Own address + Himalaya</strong></td><td>The agent checks the inbox and sends mail itself, with no always-on bot</td><td>A dedicated mail account and the Himalaya tool</td></tr>
<tr><td><strong>Google Workspace</strong></td><td>Gmail, Calendar, Drive, Sheets, Docs and Contacts</td><td>A Google Cloud project and a one-off OAuth sign-in</td></tr>
</table>
<p class="note">If you want <strong>email only</strong>, pick the channel or Himalaya — that is a
matter of minutes. Google Workspace is for the calendar, Drive and Docs, but it needs a Google
Cloud project and an approval step.</p>

<h2>Email as a channel: setup</h2>
<ol class="kroky">
<li><p>Run the wizard and pick Email (it walks you through everything):</p>
<div class="code-block"><span class="p">❯</span> hermes gateway setup</div></li>
<li><p>Or set it by hand in <code>~/.hermes/.env</code> — four required values:</p>
<div class="code-block"><span class="c"># ~/.hermes/.env</span>
EMAIL_ADDRESS=agent@yourdomain.com
EMAIL_PASSWORD=app-password        <span class="c"># note: not your regular password!</span>
EMAIL_IMAP_HOST=imap.yourdomain.com
EMAIL_SMTP_HOST=smtp.yourdomain.com</div></li>
<li><p>Add who may write to it, plus the receiving server's identity (see below — it is a safety
catch):</p>
<div class="code-block"><span class="c"># who may write to the agent (others are ignored)</span>
EMAIL_ALLOWED_USERS=you@yourdomain.com,colleague@company.com
<span class="c"># the authserv-id your receiving server stamps into message headers</span>
EMAIL_AUTHSERV_ID=mx.google.com</div></li>
<li><p>Keep it running — in the foreground, or as a service that starts with the machine:</p>
<div class="code-block"><span class="p">❯</span> hermes gateway                 <span class="c"># runs in the foreground</span>
<span class="p">❯</span> hermes gateway install         <span class="c"># as a service</span></div></li>
</ol>
<table class="wiki-tabulka">
<tr><th>Value</th><th>Default</th><th>What it is for</th></tr>
<tr><td><code>EMAIL_IMAP_PORT</code></td><td>993</td><td>Receiving mail (encrypted connection)</td></tr>
<tr><td><code>EMAIL_SMTP_PORT</code></td><td>587</td><td>Sending mail</td></tr>
<tr><td><code>EMAIL_POLL_INTERVAL</code></td><td>15 seconds</td><td>How often the inbox is checked</td></tr>
<tr><td><code>EMAIL_HOME_ADDRESS</code></td><td>—</td><td>Where output from scheduled jobs is delivered</td></tr>
</table>
<p class="note">On startup the agent marks every message already in the inbox as seen and processes
only new mail. Expect the history to be ignored the first time you start the email channel.</p>

<h2>Who may write to the agent</h2>
<table class="wiki-tabulka">
<tr><th>Setting</th><th>What happens</th></tr>
<tr><td>An allowlist is set</td><td>Only messages from those addresses are processed</td></tr>
<tr><td>No allowlist</td><td>Unknown senders are <strong>silently ignored</strong> — they get no reply at all</td></tr>
<tr><td>Mode <code>pair</code></td><td>An unknown sender receives a pairing code (they can be added)</td></tr>
<tr><td>Mode <code>decline</code></td><td>An unknown sender gets one polite refusal, then nothing for 24 hours</td></tr>
</table>
<p><strong>Sender authentication:</strong> the agent only acts when the server that received the
message confirms that it genuinely came from the stated domain (DMARC or aligned SPF/DKIM). That is
why <code>EMAIL_AUTHSERV_ID</code> exists — it must match exactly what your receiving server writes
into the headers. Without it, the <em>From:</em> header can be forged and the agent would take
orders from a stranger.</p>

<h2>Calendar and other Google services</h2>
<p>The calendar is not handled through email but through a ready-made Google Workspace workflow,
which also covers Gmail, Drive, Sheets, Docs and Contacts. Setup is a one-off and the agent guides
you:</p>
<div class="code-block"><span class="p">❯</span> Set up Google Workspace for me.</div>
<ol class="kroky">
<li>A Google Cloud project is created and the required APIs are enabled (Gmail, Calendar, Drive, Sheets, Docs, Contacts).</li>
<li>Desktop-app OAuth credentials are created and the client secret file is downloaded.</li>
<li>The agent generates a sign-in URL — you approve it in the browser and paste the redirect URL back.</li>
<li>From then on the token refreshes itself.</li>
</ol>
<p>Working with the calendar then looks like this (you just ask in the conversation):</p>
<div class="code-block"><span class="p">❯</span> What meetings do I have tomorrow?
<span class="p">❯</span> Book a 30-minute consultation with Jan on Thursday from 10:00 and invite him.</div>
<p class="note"><strong>Watch the timezone.</strong> The calendar requires a timezone offset
(<code>+02:00</code> for Czech summer time, for example) or a UTC time. When the offset is missing,
the time is taken as UTC — and your meeting lands two hours off.</p>

<h2>Pitfalls from our systems</h2>
<table class="wiki-tabulka">
<tr><th>What happened</th><th>What to do</th></tr>
<tr><td><strong>The agent processed no messages</strong></td><td>Usually <code>EMAIL_AUTHSERV_ID</code> does not match what your server writes, or the address is not on the allowlist. Both show up in the service log</td></tr>
<tr><td><strong>Replies never arrived</strong></td><td>With your own domain, SPF, DKIM and DMARC must be correct. Without them mail lands in spam or is dropped</td></tr>
<tr><td><strong>The agent obeyed a stranger</strong></td><td>Never use an "allow everyone" mode. The allowlist is what protects you</td></tr>
<tr><td><strong>Sign-in stopped working after a password change</strong></td><td>The app password must be updated in the settings too — some providers make you generate a new one</td></tr>
<tr><td><strong>A meeting was booked two hours off</strong></td><td>The timezone offset was missing. Always state the time with its offset, or ask how the agent understood it before writing</td></tr>
<tr><td><strong>Hundreds of old emails sat in the inbox and the agent ignored them</strong></td><td>That is correct — history is marked as seen at startup. Forward an older message again if you need it handled</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Give the agent an <strong>address of its own</strong></td><td>It stays out of your work mail and you keep a clear allowlist</td></tr>
<tr><td>Write a meaningful subject</td><td>The agent recognises the task better and you keep threads readable</td></tr>
<tr><td>Treat email like a letter, not a chat</td><td>It is more public and slower — sensitive things belong in chat or the terminal</td></tr>
<tr><td>Send scheduled jobs to one address</td><td>Set <code>EMAIL_HOME_ADDRESS</code> and your morning digests arrive reliably</td></tr>
<tr><td>Try one email before rolling it out</td><td>You verify sender authentication and replies before building on it</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/telegram-and-discord/"><strong>Telegram and Discord</strong><span>A faster channel than email</span></a>
<a href="/en/wiki/getting-started/scheduled-tasks/"><strong>Scheduled tasks (cron)</strong><span>A morning digest by email</span></a>
<a href="/en/wiki/getting-started/security/"><strong>Security</strong><span>Who may drive the agent</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/email" target="_blank" rel="noopener"><strong>Official documentation</strong><span>The email channel in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Three ways to email
1) Email as a channel (gateway) — write to an address, agent replies; needs IMAP/SMTP + app password.
2) Own address + Himalaya — the agent checks the inbox itself, no always-on bot.
3) Google Workspace — Gmail, Calendar, Drive, Sheets, Docs, Contacts (OAuth, Google Cloud project).
Email only -> way 1 or 2 (minutes). Calendar -> way 3.

## Setting up the email channel
hermes gateway setup -> pick Email
~/.hermes/.env:
  EMAIL_ADDRESS, EMAIL_PASSWORD (app password!), EMAIL_IMAP_HOST, EMAIL_SMTP_HOST
  EMAIL_ALLOWED_USERS=... (who may write) · EMAIL_AUTHSERV_ID=... (receiving server identity)
Optional: EMAIL_IMAP_PORT 993, EMAIL_SMTP_PORT 587, EMAIL_POLL_INTERVAL 15 s, EMAIL_HOME_ADDRESS
Run: hermes gateway (foreground) or hermes gateway install (service)
At startup existing messages are marked as seen — only new mail is processed.

## Who may write
Allowlist set = only those addresses. Empty = unknown senders silently ignored. pair = pairing code.
decline = one polite refusal then nothing (24 h).
Authentication: the agent acts only when the receiving server confirms From (DMARC or SPF/DKIM) —
hence EMAIL_AUTHSERV_ID.

## Calendar (Google Workspace)
The agent guides setup: Google Cloud project + APIs, desktop-type OAuth credentials, approve in the
browser, token refreshes itself afterwards.
Usage: "What meetings do I have tomorrow?" / "Book a 30-minute consultation on Thursday from 10:00."
WARNING: times need a timezone offset (+02:00) or UTC; a bare time is treated as UTC.

## Pitfalls from our systems
1. Nothing processed -> EMAIL_AUTHSERV_ID mismatch or address not allowlisted (check the service log).
2. Replies never arrived -> your domain needs SPF/DKIM/DMARC.
3. "Allow everyone" = the agent obeys anyone; the allowlist is the protection.
4. Password change -> update the app password in the settings too.
5. Meeting two hours off -> missing timezone offset.
6. Old emails are ignored (marked seen at startup) -> forward them again.

## Tips
An address of its own for the agent · meaningful subjects · email is a letter, not a chat (sensitive
things elsewhere) · EMAIL_HOME_ADDRESS for morning digests · try one email first.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(20)
    stranka = najdi(20)
    assert stranka and stranka["nazev"] == "E-mail a kalendář"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "E-mail a kalendář — vlastní adresa pro agenta a schůzky",
        "Jak dát agentovi vlastní e-mailovou adresu, kdo mu smí psát, jak ověřit odesílatele, jak nastavit přístup ke kalendáři Google a čemu se vyhnout u časových pásem.",
        OBRAZEK, "Wiki · Funkce do hloubky", "E-mail a kalendář",
        "Agent může mít vlastní adresu a přístup ke kalendáři. Tady je, jak to nastavit, kdo mu smí psát a na co si dát pozor.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "E-mail a kalendář — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Email and calendar — an address for the agent and your meetings",
        "How to give the agent its own email address, who may write to it, how sender authentication works, how to connect Google Calendar and what to watch with timezones.",
        OBRAZEK, "Wiki · Features in depth", "Email and calendar",
        "The agent can have an address of its own and access to your calendar. Here is how to set it up, who may write to it and what to watch out for.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Email and calendar — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
