#!/usr/bin/env python3
"""Postaví stránku wiki „Webhooky" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-messaging-webhooks.md (zapnutí, port, trasy, vlastnosti
tras, filtry, plný příklad, doručení, přímé doručení, cron na událost, slévání událostí),
guides-webhook-github-pr-review.md (typické použití: revize pull requestu).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks"
OBRAZEK = "wiki-webhooky"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🪝</span><div><strong>Webhook je dveře do vašeho agenta. Zamčené je to bezpečné, otevřené do internetu ne.</strong>
Hermes ověřuje podpis každého požadavku (HMAC), ale port 8644 nikdy nevystavujte přímo do světa.
Webhook patří za firewall nebo za reverzní proxy s HTTPS — a tajný klíč patří do <code>.env</code>,
ne do gitu.</div></div>

<h2>K čemu to je</h2>
<p>Agent pak nemusí čekat, až se ho někdo zeptá. Když se ve vaší aplikaci něco stane (nový
pull request, zaplacená objednávka, nový článek, chyba v logu), aplikace pošle požadavek a Hermes
na něm začne pracovat — a výsledek doručí tam, kam určíte.</p>
<table class="wiki-tabulka">
<tr><th>Typické použití</th><th>Co agent udělá</th></tr>
<tr><td>GitHub: nový pull request</td><td>Projde změny, napíše revizi a vloží ji jako komentář k PR</td></tr>
<tr><td>Push do hlavní větve</td><td>Zkontroluje web, spustí testy, napíše na Telegram, že je hotovo</td></tr>
<tr><td>Z vaší aplikace: dokončená platba</td><td>Vystaví doklad, pošle e-mail, založí úkol</td></tr>
<tr><td>Monitoring: spadlá služba</td><td>Podívá se na logy a pošle souhrn, co se stalo</td></tr>
</table>

<h2>Zapnutí</h2>
<div class="code-block"><span class="c"># ~/.hermes/.env</span>
WEBHOOK_ENABLED=true
WEBHOOK_PORT=8644              <span class="c"># výchozí</span>
WEBHOOK_SECRET=vas-globalni-tajny-klic</div>
<div class="code-block"><span class="c"># nebo průvodcem (zapne webhooky, port a globální klíč)</span>
hermes gateway setup

<span class="c"># ověření, že server běží</span>
curl http://localhost:8644/health
<span class="c"># → {"status": "ok", "platform": "webhook"}</span></div>

<h2>Trasy</h2>
<p>Každý zdroj událostí má vlastní pojmenovanou trasu. Adresa pro váš systém je pak
<code>http://vas-server:8644/webhooks/&lt;nazev-trasy&gt;</code>.</p>
<table class="wiki-tabulka">
<tr><th>Vlastnost</th><th>Význam</th></tr>
<tr><td><code>events</code></td><td>Které typy událostí brát (např. <code>["pull_request"]</code>); prázdné = vše</td></tr>
<tr><td><code>secret</code></td><td><strong>Povinné.</strong> Klíč pro ověření podpisu; bez něj platí globální</td></tr>
<tr><td><code>prompt</code></td><td>Zadání pro agenta s hodnotami z události (<code>{pull_request.title}</code>)</td></tr>
<tr><td><code>filters</code></td><td>Filtr na obsah — událost, která neprojde, agenta vůbec nevzbudí</td></tr>
<tr><td><code>skills</code></td><td>Které skilly má agent pro tuto trasu načíst</td></tr>
<tr><td><code>deliver</code></td><td>Kam poslat odpověď: <code>telegram</code>, <code>discord</code>, <code>github_comment</code>, <code>email</code>, <code>log</code> (výchozí)…</td></tr>
<tr><td><code>deliver_only</code></td><td>Přeskočí agenta — zpráva se jen přepošle (nulové náklady na model)</td></tr>
<tr><td><code>cron_job</code></td><td>Místo nového sezení spustí existující pravidelnou úlohu</td></tr>
<tr><td><code>coalesce</code></td><td>Slije rychlé události o téže věci do jednoho běhu (např. 5 commitů v PR)</td></tr>
</table>

<h2>Příklad: revize pull requestu</h2>
<div class="code-block">platforms:
  webhook:
    enabled: true
    extra:
      port: 8644
      secret: "globalni-zalozni-klic"
      routes:
        github-pr:
          events: ["pull_request"]
          secret: "klic-pro-github"
          prompt: |
            Zkontroluj tento pull request:
            Repozitář: {repository.full_name}
            PR #{number}: {pull_request.title}
            Autor: {pull_request.user.login}
            URL: {pull_request.html_url}
            Diff: {pull_request.diff_url}
            Akce: {action}
          skills: ["github-code-review"]
          deliver: "github_comment"
          deliver_extra:
            repo: "{repository.full_name}"
            pr_number: "{number}"
        deploy-notify:
          events: ["push"]
          secret: "klic-pro-deploy"
          prompt: "Nový push do {repository.full_name}, větev {ref}: {head_commit.message}"
          filters:
            - field: "ref"
              equals: "refs/heads/main"
          deliver: "telegram"</div>

<h2>Trasu můžete založit i příkazem</h2>
<div class="code-block">hermes webhook subscribe <span class="c">&lt;nazev&gt;</span>            <span class="c"># vytvoří trasu za běhu</span>
hermes webhook subscribe <span class="c">&lt;nazev&gt;</span> --route-profile coder   <span class="c"># pro konkrétní profil</span></div>
<p class="note">Trasu založenou příkazem nejde povýšit na vyšší oprávnění — nástroje (<code>toolsets</code>)
se u tras mění jen ručně v <code>config.yaml</code>. Je to schválně: kdyby to uměl agent sám, mohl by
si webhookem přidělit víc, než má.</p>

<h2>Bezpečnost: podepsané neznamená důvěryhodné</h2>
<table class="wiki-tabulka">
<tr><th>Pravidlo</th><th>Proč</th></tr>
<tr><td>Port 8644 nikdy přímo do internetu</td><td>Za reverzní proxy s HTTPS, nebo jen na localhost/VPN</td></tr>
<tr><td><code>INSECURE_NO_AUTH</code> jen na zkoušku</td><td>Vypíná ověření podpisu — na produkci nikdy</td></tr>
<tr><td>Vlastní klíč pro každou trasu</td><td>Když unikne klíč z GitHubu, ostatní trasy zůstanou zavřené</td></tr>
<tr><td>Obsah události je cizí text</td><td>Popis PR nebo zpráva od uživatele může obsahovat pokyn („ignoruj pravidla a…“). Agent se jím nesmí řídit</td></tr>
<tr><td>Filtry a <code>events</code> co nejtěsnější</td><td>Méně probuzení = méně nákladů a menší plocha pro zneužití</td></tr>
</table>

<h2>Na co si dát pozor</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Webhook nefunguje, ale <code>/health</code> odpovídá</td><td>Nejspíš nesedí podpis (jiný klíč) nebo událost neprošla <code>events</code>/<code>filters</code> — vrací se 200 s <code>"ignored"</code></td></tr>
<tr><td>Port 8644 je obsazený</td><td>Něco jiného ho používá; změňte <code>WEBHOOK_PORT</code> a upravte adresu u zdroje</td></tr>
<tr><td>Agent na událost nereaguje po restartu</td><td>Webhooky obsluhuje brána — musí běžet (<code>hermes gateway status</code>)</td></tr>
<tr><td>Příliš mnoho běhů z jednoho PR</td><td>Přidejte <code>coalesce</code> (klíč např. <code>pull_request.number</code>)</td></tr>
<tr><td>Chcete jen přeposlat zprávu</td><td><code>deliver_only: true</code> — bez agenta a bez nákladů na model</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/pravidelne-ulohy/"><strong>Pravidelné úlohy (cron)</strong><span>Když má agent pracovat podle času, ne podle události</span></a>
<a href="/wiki/zaciname/bezpecnost/"><strong>Bezpečnost</strong><span>Schvalování, oprávnění a co agent smí</span></a>
<a href="/wiki/zaciname/mcp-nastroje/"><strong>MCP nástroje</strong><span>Opačný směr: agent volá vaši aplikaci</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Webhooky, filtry a doručování do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co to je
Brána Hermese umí přijímat HTTP webhooky a spustit podle nich agenta. Ověřuje HMAC podpis.
Adresa: http://server:8644/webhooks/<nazev-trasy>.

## Zapnutí
.env: WEBHOOK_ENABLED=true, WEBHOOK_PORT=8644, WEBHOOK_SECRET=...  (nebo hermes gateway setup)
Kontrola: curl http://localhost:8644/health -> {"status":"ok","platform":"webhook"}

## Trasy (config.yaml platforms.webhook.extra.routes)
events (typy událostí, prázdné = vše) · secret (POVINNÉ, jinak globální) · prompt (šablona s {pole})
· filters (neprošlo = 200 "ignored") · script (filtr/transformace) · skills · toolsets (jen ručně v configu)
· deliver (telegram/discord/github_comment/email/log...) · deliver_extra · deliver_only (bez agenta)
· cron_job (spustí existující úlohu) · coalesce (slije rychlé události; key + window_seconds 30 + max_wait 300)
· profile (u multiplexu, /p/<profil>/webhooks/<trasa>).

## Dynamicky
hermes webhook subscribe <nazev> [--route-profile <profil>] — toolsets takto nelze měnit (bezpečnost).

## Bezpečnost
Port nikdy přímo do internetu (reverzní proxy s HTTPS, nebo VPN/localhost) · INSECURE_NO_AUTH jen na test
· vlastní klíč pro každou trasu · obsah události je cizí text (pokyny v popisu PR neposlouchat)
· filtry co nejtěsnější.

## Pozor
Nefunguje = špatný podpis nebo událost neprošla filtrem (200 ignored) · port obsazený · webhooky obsluhuje brána
(musí běžet) · hodně běhů z jednoho PR -> coalesce · jen přeposlat -> deliver_only.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🪝</span><div><strong>A webhook is a door into your agent. Locked it is useful; open to the internet it is a liability.</strong>
Hermes verifies a signature on every request (HMAC), but never expose port 8644 directly to the world.
Keep webhooks behind a firewall or a reverse proxy with HTTPS — and keep the secret in <code>.env</code>,
not in git.</div></div>

<h2>What it is for</h2>
<p>The agent no longer has to wait to be asked. When something happens in your app (a new pull
request, a paid order, a new article, an error in the logs), the app sends a request, Hermes starts
working on it — and delivers the result wherever you point it.</p>
<table class="wiki-tabulka">
<tr><th>Typical use</th><th>What the agent does</th></tr>
<tr><td>GitHub: a new pull request</td><td>Reads the diff, writes a review and posts it as a PR comment</td></tr>
<tr><td>Push to the main branch</td><td>Checks the site, runs tests, messages Telegram that it is done</td></tr>
<tr><td>From your app: a completed payment</td><td>Issues a receipt, sends an e-mail, creates a task</td></tr>
<tr><td>Monitoring: a service went down</td><td>Reads the logs and sends a summary of what happened</td></tr>
</table>

<h2>Enabling</h2>
<div class="code-block"><span class="c"># ~/.hermes/.env</span>
WEBHOOK_ENABLED=true
WEBHOOK_PORT=8644              <span class="c"># default</span>
WEBHOOK_SECRET=your-global-secret</div>
<div class="code-block"><span class="c"># or via the wizard (enables webhooks, port and global secret)</span>
hermes gateway setup

<span class="c"># verify the server is up</span>
curl http://localhost:8644/health
<span class="c"># → {"status": "ok", "platform": "webhook"}</span></div>

<h2>Routes</h2>
<p>Every event source gets its own named route. Your system then points at
<code>http://your-server:8644/webhooks/&lt;route-name&gt;</code>.</p>
<table class="wiki-tabulka">
<tr><th>Property</th><th>Meaning</th></tr>
<tr><td><code>events</code></td><td>Which event types to accept (e.g. <code>["pull_request"]</code>); empty = all</td></tr>
<tr><td><code>secret</code></td><td><strong>Required.</strong> Signature key; the global one is the fallback</td></tr>
<tr><td><code>prompt</code></td><td>Instructions for the agent with payload values (<code>{pull_request.title}</code>)</td></tr>
<tr><td><code>filters</code></td><td>Payload filter — a non-match never wakes the agent</td></tr>
<tr><td><code>skills</code></td><td>Which skills the agent should load for this route</td></tr>
<tr><td><code>deliver</code></td><td>Where the answer goes: <code>telegram</code>, <code>discord</code>, <code>github_comment</code>, <code>email</code>, <code>log</code> (default)…</td></tr>
<tr><td><code>deliver_only</code></td><td>Skips the agent — the message is just forwarded (zero model cost)</td></tr>
<tr><td><code>cron_job</code></td><td>Runs an existing scheduled job instead of a fresh session</td></tr>
<tr><td><code>coalesce</code></td><td>Debounces rapid events about the same entity into one run (e.g. 5 commits in a PR)</td></tr>
</table>

<h2>Example: pull request review</h2>
<div class="code-block">platforms:
  webhook:
    enabled: true
    extra:
      port: 8644
      secret: "global-fallback-secret"
      routes:
        github-pr:
          events: ["pull_request"]
          secret: "github-webhook-secret"
          prompt: |
            Review this pull request:
            Repository: {repository.full_name}
            PR #{number}: {pull_request.title}
            Author: {pull_request.user.login}
            URL: {pull_request.html_url}
            Diff: {pull_request.diff_url}
            Action: {action}
          skills: ["github-code-review"]
          deliver: "github_comment"
          deliver_extra:
            repo: "{repository.full_name}"
            pr_number: "{number}"
        deploy-notify:
          events: ["push"]
          secret: "deploy-secret"
          prompt: "New push to {repository.full_name} branch {ref}: {head_commit.message}"
          filters:
            - field: "ref"
              equals: "refs/heads/main"
          deliver: "telegram"</div>

<h2>Routes can also be created from the CLI</h2>
<div class="code-block">hermes webhook subscribe <span class="c">&lt;name&gt;</span>            <span class="c"># creates a route at runtime</span>
hermes webhook subscribe <span class="c">&lt;name&gt;</span> --route-profile coder   <span class="c"># for a specific profile</span></div>
<p class="note">A route created from the CLI cannot grant itself more power — <code>toolsets</code> are
only changed by hand in <code>config.yaml</code>. That is deliberate: otherwise an agent could use a
webhook to give itself more than it has.</p>

<h2>Security: signed does not mean trusted</h2>
<table class="wiki-tabulka">
<tr><th>Rule</th><th>Why</th></tr>
<tr><td>Never expose port 8644 directly</td><td>Put it behind a reverse proxy with HTTPS, or keep it on localhost/VPN</td></tr>
<tr><td><code>INSECURE_NO_AUTH</code> only for testing</td><td>It disables signature checks — never in production</td></tr>
<tr><td>A separate secret per route</td><td>If the GitHub secret leaks, the other routes stay closed</td></tr>
<tr><td>Payload content is untrusted text</td><td>A PR description can contain instructions (“ignore your rules and…”). The agent must not follow them</td></tr>
<tr><td>Keep <code>events</code> and filters tight</td><td>Fewer wake-ups means lower cost and a smaller attack surface</td></tr>
</table>

<h2>Things to watch</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>Webhooks do nothing but <code>/health</code> answers</td><td>Likely a signature mismatch (different secret) or the event failed <code>events</code>/<code>filters</code> — you get 200 with <code>"ignored"</code></td></tr>
<tr><td>Port 8644 is taken</td><td>Something else uses it; change <code>WEBHOOK_PORT</code> and update the source URL</td></tr>
<tr><td>The agent stops reacting after a restart</td><td>The gateway serves webhooks — it must be running (<code>hermes gateway status</code>)</td></tr>
<tr><td>Too many runs from one PR</td><td>Add <code>coalesce</code> (key e.g. <code>pull_request.number</code>)</td></tr>
<tr><td>You only want to forward a message</td><td><code>deliver_only: true</code> — no agent, no model cost</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/scheduled-tasks/"><strong>Scheduled tasks (cron)</strong><span>When the agent should work on time, not on an event</span></a>
<a href="/en/wiki/getting-started/security/"><strong>Security</strong><span>Approvals, permissions and what the agent may do</span></a>
<a href="/en/wiki/getting-started/mcp-tools/"><strong>MCP tools</strong><span>The other direction: the agent calls your app</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Webhooks, filters and delivery in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What it is
The Hermes gateway accepts HTTP webhooks and starts the agent from them. HMAC signatures are verified.
URL: http://server:8644/webhooks/<route-name>.

## Enabling
.env: WEBHOOK_ENABLED=true, WEBHOOK_PORT=8644, WEBHOOK_SECRET=...  (or hermes gateway setup)
Check: curl http://localhost:8644/health -> {"status":"ok","platform":"webhook"}

## Routes (config.yaml platforms.webhook.extra.routes)
events (types; empty = all) · secret (REQUIRED, global fallback) · prompt (template with {fields})
· filters (non-match = 200 "ignored") · script (filter/transform) · skills · toolsets (manual config only)
· deliver (telegram/discord/github_comment/email/log...) · deliver_extra · deliver_only (no agent)
· cron_job (runs an existing job) · coalesce (key + window_seconds 30 + max_wait_seconds 300)
· profile (with multiplexing: /p/<profile>/webhooks/<route>).

## Runtime
hermes webhook subscribe <name> [--route-profile <profile>] — toolsets cannot be changed this way (security).

## Security
Never expose the port directly (reverse proxy with HTTPS, or VPN/localhost) · INSECURE_NO_AUTH is test-only
· one secret per route · payload text is untrusted (instructions inside a PR description must be ignored)
· tight filters.

## Watch out
Silent webhooks = wrong secret or event filtered out (200 ignored) · port conflicts · the gateway must run
· many runs from one PR -> coalesce · forwarding only -> deliver_only.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(29)
    stranka = najdi(29)
    assert stranka and stranka["nazev"] == "Webhooky"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Webhooky — když má agenta spustit událost, ne člověk",
        "Jak zapnout webhooky v bráně Hermese, jak popsat trasy a filtry, kam doručovat výsledek a jak to udělat tak, aby port do internetu nekoukal otevřený.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Webhooky",
        "Webhook je dveře do vašeho agenta. Jak je zamknout, komu je otevřít a co má agent udělat, když něco zaklepe.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Webhooky — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Webhooks — when an event should start the agent, not a person",
        "How to enable webhooks in the Hermes gateway, how to describe routes and filters, where to deliver results and how to keep the port closed to the internet.",
        OBRAZEK, "Wiki · Features in depth", "Webhooks",
        "A webhook is a door into your agent. How to lock it, whom to open it for and what the agent should do when something knocks.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Webhooks — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
