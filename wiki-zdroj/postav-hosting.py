#!/usr/bin/env python3
"""Postaví stránku wiki „Hosting a domény" (česky + anglicky) včetně verze pro AI.

Vlastní zkušenosti z provozu (označeno „u nás"): kde agenta provozovat, jak velký server,
co udělat s doménou a DNS, HTTPS, firewall, zálohy a monitoring. Ceny se neuvádějí —
odkazuje se na stránku /hosting/ s aktuální nabídkou.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/getting-started/installation"
OBRAZEK = "wiki-hosting"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🏠</span><div><strong>Agent potřebuje místo, kde běží nepřetržitě — ale nemusí to být server za tisíce.</strong>
Na chat stačí váš počítač. Jakmile ale chcete, aby agent odpovídal na Telegram, spouštěl pravidelné
úlohy a přijímal webhooky, musí běžet pořád. Nejčastější volba je malý VPS za pár desítek korun měsíčně.</div></div>

<h2>Tři možnosti</h2>
<table class="wiki-tabulka">
<tr><th></th><th>Váš počítač</th><th>VPS (pronajatý server)</th><th>Domácí server</th></tr>
<tr><td>Běží pořád</td><td>Ne — usne s počítačem</td><td>Ano</td><td>Ano, dokud jde elektřina a internet</td></tr>
<tr><td>Veřejná adresa</td><td>Ne</td><td>Ano, ihned</td><td>Jen přes tunel nebo veřejnou IP</td></tr>
<tr><td>Cena</td><td>0</td><td>Několik desítek až stovek Kč měsíčně</td><td>Elektřina + hardware</td></tr>
<tr><td>Vhodné pro</td><td>Zkoušení, práci s vlastními soubory</td><td>Běžný provoz, webhooky, cron</td><td>Kdo nechce data u poskytovatele</td></tr>
</table>

<h2>Jak velký server</h2>
<table class="wiki-tabulka">
<tr><th>Zátěž</th><th>Rozumné minimum</th></tr>
<tr><td>Jeden agent, Telegram, cron, pár skillů</td><td>2 jádra, 4 GB RAM, 40 GB disku</td></tr>
<tr><td>Víc profilů, lokální model na malé úkoly</td><td>4 jádra, 8–16 GB RAM</td></tr>
<tr><td>Lokální model pro hlavní práci</td><td>Výkonná GPU nebo pronájem GPU — jinak zůstaňte u cloudového modelu</td></tr>
</table>
<p class="note">Disk se plní rychleji, než se čeká — sezení, logy, zálohy a obrázky. Hlídejte
<code>df -h</code> a nastavte úklid starých souborů dřív, než dojde místo.</p>

<h2>Doména a DNS</h2>
<p>Doménu potřebujete ze dvou důvodů: kvůli <strong>webhookům</strong> (GitHub, Twilio, WhatsApp Cloud
chtějí veřejnou HTTPS adresu) a kvůli <strong>příjemnému přístupu</strong> k webovému rozhraní agenta.
Stačí jediná doména a subdomény.</p>
<div class="code-block"><span class="c"># příklad DNS záznamů</span>
A      agent.vasedomena.cz     →  IP serveru
AAAA   agent.vasedomena.cz     →  IPv6 (pokud ji máte)
CNAME  www.vasedomena.cz       →  vasedomena.cz</div>
<table class="wiki-tabulka">
<tr><th>Krok</th><th>Proč</th></tr>
<tr><td>Subdoména pro agenta, ne celá doména</td><td>Hlavní doménu si necháte pro web; kdyby agent spadl, web běží dál</td></tr>
<tr><td>Nízké TTL (300 s) při prvním nastavení</td><td>Změna se projeví za minuty, ne za hodinu</td></tr>
<tr><td>Po ověření TTL zvýšit</td><td>Méně dotazů do DNS</td></tr>
</table>

<h2>HTTPS</h2>
<div class="code-block"><span class="c"># nginx + certbot na Ubuntu/Debian</span>
apt install nginx certbot python3-certbot-nginx
certbot --nginx -d agent.vasedomena.cz
systemctl enable --now certbot.timer     <span class="c"># obnova řeší sama</span></div>
<p>Alternativa pro toho, kdo nechce řešit nginx: <strong>Caddy</strong> si certifikát vyřídí sám.
Pro webhooky z internetu je <strong>HTTPS povinné</strong> — bez něj vám GitHub ani Twilio nic nepošle.</p>
<p class="note">Na serveru bez veřejné adresy (domácí počítač) stačí dočasný tunel:
<code>cloudflared tunnel --url http://localhost:8080</code>. Adresa se mění, takže se hodí jen na testování;
pro stálý provoz je lepší pojmenovaný tunel nebo VPS.</p>

<h2>Bezpečnost serveru</h2>
<table class="wiki-tabulka">
<tr><th>Opatření</th><th>Jak</th></tr>
<tr><td>Přihlášení jen klíčem</td><td><code>PasswordAuthentication no</code> v <code>/etc/ssh/sshd_config</code></td></tr>
<tr><td>Firewall</td><td><code>ufw allow 22,80,443/tcp</code> a <code>ufw enable</code>; ostatní porty zavřené</td></tr>
<tr><td>Aktualizace</td><td><code>unattended-upgrades</code> — bezpečnostní záplaty samy</td></tr>
<tr><td>Agent nesmí být root nad vším</td><td>Vlastní uživatel, allowlist v kanálech, potvrzování nebezpečných příkazů</td></tr>
<tr><td>Brána jako služba</td><td><code>hermes gateway install</code> — přežije odhlášení i restart</td></tr>
</table>

<h2>Zálohy a monitoring</h2>
<div class="code-block"><span class="c"># záloha konfigurace, skillů a paměti</span>
hermes backup
<span class="c"># obnova</span>
hermes backup restore</div>
<p>Zálohujte <code>~/.hermes</code> mimo server (jinam než na stejný disk) a ověřte, že se z ní dá
obnovit. Na monitoring stačí agent hlídat sám sebe — viz stránka o měření a monitoringu.</p>

<h2>Jak to máme u nás</h2>
<table class="wiki-tabulka">
<tr><th>Zvyk</th><th>Proč se vyplatil</th></tr>
<tr><td>Jeden malý VPS na agenta, zvlášť weby</td><td>Když agent experimentuje, weby běží dál</td></tr>
<tr><td>Subdoména <code>agent.</code> s HTTPS</td><td>Webhooky fungují a adresa je zapamatovatelná</td></tr>
<tr><td>Záloha každou noc mimo server</td><td>Obnova po pokažené aktualizaci je otázka minut</td></tr>
<tr><td>Sledování místa na disku</td><td>Nejčastější důvod, proč něco přestane fungovat</td></tr>
</table>
<p>Konkrétní nabídky pronájmu najdete na stránce <a href="/hosting/">Hosting</a>; ceny se mění,
proto je tam neopisujeme.</p>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/instalace/"><strong>Instalace na VPS</strong><span>Krok za krokem od nuly</span></a>
<a href="/wiki/funkce/zalohy-a-obnova/"><strong>Zálohy a obnova</strong><span>Co zálohovat a jak obnovit</span></a>
<a href="/wiki/funkce/monitoring/"><strong>Měření a monitoring</strong><span>Aby se o výpadku dozvěděl agent</span></a>
<a href="/wiki/funkce/webhooky/"><strong>Webhooky</strong><span>Proč potřebujete HTTPS adresu</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Kde provozovat
Vlastní počítač (jen na zkoušení, neběží pořád) · VPS (běžný provoz: Telegram, cron, webhooky) ·
domácí server (data u sebe, ale elektřina/internet jsou slabé místo).

## Velikost
1 agent + Telegram + cron: 2 jádra / 4 GB / 40 GB. Víc profilů: 4 jádra / 8–16 GB.
Lokální model na hlavní práci: GPU. Disk se plní (sezení, logy, zálohy) -> hlídat df -h a úklid.

## Doména a DNS
Doména kvůli webhookům (GitHub, Twilio, WhatsApp Cloud chtějí veřejné HTTPS) a přístupu k webovému UI.
A agent.domena -> IP; AAAA -> IPv6; CNAME www -> doména. Subdoména pro agenta; TTL 300 s při změnách.

## HTTPS
apt install nginx certbot python3-certbot-nginx; certbot --nginx -d agent.domena; certbot.timer.
Alternativa Caddy (certifikát sám). Bez veřejné adresy: cloudflared tunnel --url http://localhost:8080
(dočasné, adresa se mění).

## Bezpečnost
SSH jen klíčem (PasswordAuthentication no) · ufw allow 22,80,443 · unattended-upgrades ·
agent ne jako root, allowlist v kanálech, potvrzování příkazů · hermes gateway install.

## Zálohy
hermes backup / hermes backup restore; ~/.hermes mimo server, obnovu vyzkoušet. Monitoring agentem.

## U nás
Malý VPS zvlášť od webů, subdoména agent. s HTTPS, noční záloha mimo server, sledování místa na disku.
Ceny na /hosting/.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🏠</span><div><strong>The agent needs somewhere to run around the clock — but it does not have to be an expensive server.</strong>
Your own computer is enough for a chat. The moment the agent must answer Telegram, run scheduled jobs
and receive webhooks, it has to stay up. The usual answer is a small VPS for the price of a couple of
coffees a month.</div></div>

<h2>Three options</h2>
<table class="wiki-tabulka">
<tr><th></th><th>Your computer</th><th>VPS (rented server)</th><th>Home server</th></tr>
<tr><td>Always on</td><td>No — it sleeps with the machine</td><td>Yes</td><td>Yes, while power and internet last</td></tr>
<tr><td>Public address</td><td>No</td><td>Yes, immediately</td><td>Only via a tunnel or a public IP</td></tr>
<tr><td>Cost</td><td>0</td><td>A few euros a month</td><td>Electricity + hardware</td></tr>
<tr><td>Best for</td><td>Trying it out, working with local files</td><td>Normal operation, webhooks, cron</td><td>Those who do not want their data at a provider</td></tr>
</table>

<h2>How big a server</h2>
<table class="wiki-tabulka">
<tr><th>Load</th><th>Sensible minimum</th></tr>
<tr><td>One agent, Telegram, cron, a few skills</td><td>2 cores, 4 GB RAM, 40 GB disk</td></tr>
<tr><td>Multiple profiles, a small local model</td><td>4 cores, 8–16 GB RAM</td></tr>
<tr><td>A local model for the main work</td><td>A strong GPU or rented GPU time — otherwise stay with a cloud model</td></tr>
</table>
<p class="note">Disks fill up faster than expected — sessions, logs, backups, images. Watch
<code>df -h</code> and set up cleanup of old files before you run out of space.</p>

<h2>Domain and DNS</h2>
<p>You need a domain for two reasons: <strong>webhooks</strong> (GitHub, Twilio and WhatsApp Cloud all
want a public HTTPS address) and a <strong>pleasant way in</strong> to the agent's web UI. One domain and
a subdomain is enough.</p>
<div class="code-block"><span class="c"># example DNS records</span>
A      agent.yourdomain.com     →  server IP
AAAA   agent.yourdomain.com     →  IPv6 (if you have one)
CNAME  www.yourdomain.com       →  yourdomain.com</div>
<table class="wiki-tabulka">
<tr><th>Step</th><th>Why</th></tr>
<tr><td>A subdomain for the agent, not the whole domain</td><td>Keep the main domain for your site; if the agent breaks, the site stays up</td></tr>
<tr><td>Low TTL (300 s) during setup</td><td>Changes take minutes, not an hour</td></tr>
<tr><td>Raise the TTL once it works</td><td>Fewer DNS queries</td></tr>
</table>

<h2>HTTPS</h2>
<div class="code-block"><span class="c"># nginx + certbot on Ubuntu/Debian</span>
apt install nginx certbot python3-certbot-nginx
certbot --nginx -d agent.yourdomain.com
systemctl enable --now certbot.timer     <span class="c"># renewal handled for you</span></div>
<p>If you would rather not manage nginx, <strong>Caddy</strong> obtains certificates by itself.
For webhooks from the internet <strong>HTTPS is mandatory</strong> — without it GitHub and Twilio will
not deliver anything.</p>
<p class="note">On a machine with no public address (home computer) a temporary tunnel is enough:
<code>cloudflared tunnel --url http://localhost:8080</code>. The address changes, so it is for testing;
for permanent operation use a named tunnel or a VPS.</p>

<h2>Server security</h2>
<table class="wiki-tabulka">
<tr><th>Measure</th><th>How</th></tr>
<tr><td>Key-only SSH</td><td><code>PasswordAuthentication no</code> in <code>/etc/ssh/sshd_config</code></td></tr>
<tr><td>Firewall</td><td><code>ufw allow 22,80,443/tcp</code> then <code>ufw enable</code>; everything else closed</td></tr>
<tr><td>Updates</td><td><code>unattended-upgrades</code> — security patches apply themselves</td></tr>
<tr><td>The agent is not root over everything</td><td>Its own user, channel allowlists, confirmations for dangerous commands</td></tr>
<tr><td>Gateway as a service</td><td><code>hermes gateway install</code> — survives logout and reboot</td></tr>
</table>

<h2>Backups and monitoring</h2>
<div class="code-block"><span class="c"># back up config, skills and memory</span>
hermes backup
<span class="c"># restore</span>
hermes backup restore</div>
<p>Keep a copy of <code>~/.hermes</code> off the server (not on the same disk) and verify a restore
actually works. For monitoring, let the agent watch itself — see the measurement and monitoring page.</p>

<h2>How we do it</h2>
<table class="wiki-tabulka">
<tr><th>Habit</th><th>Why it paid off</th></tr>
<tr><td>One small VPS for the agent, websites elsewhere</td><td>When the agent experiments, sites keep serving</td></tr>
<tr><td>An <code>agent.</code> subdomain with HTTPS</td><td>Webhooks work and the address is memorable</td></tr>
<tr><td>A nightly backup off the server</td><td>Recovering from a bad update takes minutes</td></tr>
<tr><td>Watching disk space</td><td>The most common reason something stops working</td></tr>
</table>
<p>For concrete hosting offers see the <a href="/en/hosting/">Hosting</a> page; prices move, which is why
we do not copy them here.</p>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/installation/"><strong>Installing on a VPS</strong><span>Step by step from zero</span></a>
<a href="/en/wiki/features/backups-and-restore/"><strong>Backups and restore</strong><span>What to back up and how to restore</span></a>
<a href="/en/wiki/features/monitoring/"><strong>Measurement and monitoring</strong><span>So the agent learns about an outage</span></a>
<a href="/en/wiki/features/webhooks/"><strong>Webhooks</strong><span>Why you need an HTTPS address</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Where to run it
Your computer (trial only, not always on) · VPS (normal operation: Telegram, cron, webhooks) ·
home server (data stays with you, but power/internet are the weak point).

## Sizing
One agent + Telegram + cron: 2 cores / 4 GB / 40 GB. More profiles: 4 cores / 8-16 GB.
A local model for real work: a GPU. Disks fill (sessions, logs, backups) -> watch df -h and clean up.

## Domain and DNS
A domain for webhooks (GitHub, Twilio, WhatsApp Cloud need public HTTPS) and for reaching the web UI.
A agent.domain -> IP; AAAA -> IPv6; CNAME www -> domain. Use a subdomain for the agent; TTL 300 s while changing.

## HTTPS
apt install nginx certbot python3-certbot-nginx; certbot --nginx -d agent.domain; certbot.timer.
Or Caddy (certificates automatic). No public address: cloudflared tunnel --url http://localhost:8080
(temporary, address changes).

## Security
SSH keys only (PasswordAuthentication no) · ufw allow 22,80,443 · unattended-upgrades ·
agent not as root, channel allowlists, command confirmations · hermes gateway install.

## Backups
hermes backup / hermes backup restore; keep ~/.hermes off the server and test a restore. Monitor with the agent.

## Our practice
A small VPS separate from the websites, an agent. subdomain with HTTPS, a nightly off-server backup,
disk-space watch. Prices live on /hosting/.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(38)
    stranka = najdi(38)
    assert stranka and stranka["nazev"] == "Hosting a domény"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Hosting a domény — kde agenta provozovat a jak ho zabezpečit",
        "Vlastní počítač, VPS nebo domácí server: jak vybrat, jak velký stroj stačí, co udělat s doménou a DNS, HTTPS pro webhooky, firewall, zálohy a monitoring.",
        OBRAZEK, "Wiki · Integrace", "Hosting a domény",
        "Agent potřebuje místo, kde běží nepřetržitě — ale nemusí to být server za tisíce. Praktický průvodce provozem.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Hosting a domény (česká wiki)", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Hosting and domains — where to run the agent and how to secure it",
        "Your own computer, a VPS or a home server: how to choose, how big a machine you need, what to do with a domain and DNS, HTTPS for webhooks, firewall, backups and monitoring.",
        OBRAZEK, "Wiki · Integrations", "Hosting and domains",
        "The agent needs somewhere to run around the clock — but not an expensive server. A practical operations guide.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Hosting and domains (community wiki)", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
