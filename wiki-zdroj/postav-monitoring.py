#!/usr/bin/env python3
"""Postaví stránku wiki „Měření a monitoring" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/reference-slash-commands.md (/usage, /insights), user-guide-features-web-dashboard.md
(stránka Status, sezení, využití tokenů, hlášení o paměti a disku), developer-guide-gateway-monitoring.md
(OTLP export, co se exportuje, content-free, alerty, hermes monitoring status), reference-cli-commands.md
(hermes doctor jako health gate).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-monitoring"
OBRAZEK = "wiki-monitoring"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📈</span><div><strong>Monitoring není o tom mít graf. Je o tom vědět o problému dřív než uživatel.</strong>
Hermes vám dá tři úrovně: okamžitý přehled v chatu (<code>/usage</code>), přehled instalace v dashboardu
a strojový export metrik pro servery, které sledujete. Začněte první úrovní — ta je zdarma a hned.</div></div>

<h2>1. Kolik to stojí: <code>/usage</code> a <code>/insights</code></h2>
<table class="wiki-tabulka">
<tr><th>Příkaz</th><th>Co ukáže</th></tr>
<tr><td><code>/usage</code></td><td>Spotřebu tokenů, rozpad ceny (vstup/výstup), stav kontextového okna, délku sezení a — když to poskytovatel umí — zbývající kvótu nebo kredit</td></tr>
<tr><td><code>/insights</code></td><td>Přehled za posledních 30 dní: co se používalo a kolik to stálo</td></tr>
</table>
<p class="note">Pokud se vám cena zdá vysoká, podívejte se nejdřív na <strong>velikost kontextu</strong>,
ne na cenu za token. Dlouhá sezení bez úklidu jsou nejčastější důvod, proč účet roste rychleji,
než by odpovídalo množství práce.</p>

<h2>2. Přehled instalace: dashboard</h2>
<p>Stránka <strong>Status</strong> v dashboardu se obnovuje každých 5 vteřin a ukazuje:</p>
<table class="wiki-tabulka">
<tr><th>Co</th><th>Význam</th></tr>
<tr><td>Verze a datum vydání</td><td>Na jaké verzi jedete (hodí se při hlášení chyby)</td></tr>
<tr><td>Stav brány</td><td>Běží/stopped, PID, připojené platformy a jejich stav</td></tr>
<tr><td>Aktivní sezení</td><td>Kolik sezení bylo aktivních za posledních 5 minut</td></tr>
<tr><td>Posledních 20 sezení</td><td>Model, počet zpráv, spotřeba tokenů a náhled konverzace</td></tr>
</table>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⚠️</span><div><strong>Hlášení o prostředcích je to nejcennější, co tam je.</strong>
Když dojde paměť (pod 128 MiB nebo 15 %) nebo místo na disku (pod 512 MB), objeví se nahoře
pruh s varováním. U paměti Hermes pozná i to, že agent předchozí běh nepřežil kvůli nedostatku paměti.
Bez tohohle varování se restart agenta tváří jako „nějaká chyba“.</div></div>

<h2>3. Zdraví z příkazové řádky: <code>hermes doctor</code></h2>
<div class="code-block">hermes doctor            <span class="c"># kontrola, výstup 0 = bez problémů, 1 = něco zůstalo</span>
hermes doctor --fix      <span class="c"># zkusí, co jde, opravit samo</span></div>
<p>Návratový kód dělá z <code>doctor</code> použitelnou kontrolu pro cron nebo CI: dá se na něm
postavit „když se to pokazí, pošli mi zprávu“. Kontroluje i IPv6 trasu (blackholed prefix se pozná
jako varování s radou <code>network.force_ipv4: true</code>).</p>

<h2>4. Strojový export metrik (OTLP)</h2>
<p>Pro skutečný dohled — Prometheus, DataDog, OpenTelemetry Collector — umí brána posílat metriky,
události a diagnostiku přes OTLP/HTTP:</p>
<div class="code-block"><span class="c"># config.yaml</span>
monitoring:
  gateway_health_export:
    enabled: true
  export:
    otlp:
      enabled: true
      endpoint: http://collector-host:4318/v1/traces   <span class="c"># metriky a logy se odvodí</span>
      headers_env: {}   <span class="c"># název hlavičky -> NÁZEV proměnné prostředí (hodnoty se neukládají)</span></div>
<div class="code-block">hermes monitoring status    <span class="c"># jak to je nastavené a jestli to běží</span></div>
<table class="wiki-tabulka">
<tr><th>Signál</th><th>Co obsahuje</th></tr>
<tr><td>Metriky</td><td><code>hermes.gateway.up/state/busy/active_agents/background_work</code>, stav platforem, časovač cronu a počty úloh</td></tr>
<tr><td>Události (traces)</td><td>Přechody stavu brány (<code>starting → running → draining → stopped</code>), změny stavu platforem, průběh cron úloh</td></tr>
<tr><td>Diagnostika (logs)</td><td>Jen varování a chyby s kódem a třídou chyby — <strong>nikdy text promptů ani zpráv</strong></td></tr>
</table>
<p class="note"><strong>Export je záměrně „bez obsahu“:</strong> neposílá prompty, zprávy, argumenty
nástrojů, jména úloh ani historii sezení. Do cizího systému se tak nedostane nic z toho, co jste
agentovi svěřili — a přesto poznáte, že je brána dole.</p>

<h2>Na co hlídat</h2>
<table class="wiki-tabulka">
<tr><th>Pravidlo</th><th>Proč</th></tr>
<tr><td><code>hermes_gateway_up == 0</code></td><td>Brána je explicitně dole (proces běží, ale nehlásí se)</td></tr>
<tr><td>Chybějící řada delší než interval exportu</td><td>Proces, který spadl, sám nulu nepošle — bez tohohle pravidla vám výpadek nikdo neohlásí</td></tr>
<tr><td><code>hermes.platform.degraded</code></td><td>Platforma (Telegram, Discord) ztratila spojení, ale brána běží dál</td></tr>
<tr><td>Stáří posledního úspěchu cronu</td><td>Pravidelná úloha přestala běžet — častější problém než spadlá brána</td></tr>
</table>
<p class="note">Druhé pravidlo je zkušenost z našeho provozu: měření, které posílá jen „jsem OK“,
vypadá při výpadku jako klid. Vždy hlídejte i to, že data <strong>přestala chodit</strong>.</p>

<h2>Na co si dát pozor</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Chybí SDK pro OTLP</td><td>Doplňuje se při prvním použití (extra <code>otlp</code>); bez něj brána běží dál, jen se neexportuje</td></tr>
<tr><td>Endpoint je nedostupný</td><td>Export nesmí shodit agenta — selhání je omezené a nezdržuje běžný provoz</td></tr>
<tr><td>Dashboard hlásí málo paměti</td><td>Zkraťte sezení, uberte paralelní podagenty, zvyšte RAM; hlášení zmizí po restartu brány</td></tr>
<tr><td>Velká spotřeba tokenů</td><td>Kratší sezení, levnější model pro pomocné úlohy (např. kurátor), méně nástrojů v kontextu</td></tr>
<tr><td>Monitoring máte, ale nikdo se nedívá</td><td>Nastavte práh, který pošle zprávu do Telegramu — graf, na který se nechodí, není monitoring</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/pravidelne-ulohy/"><strong>Pravidelné úlohy (cron)</strong><span>Jak hlídat, že se opravdu spouští</span></a>
<a href="/wiki/funkce/kurator-skills/"><strong>Kurátor skillů</strong><span>Pomocné úlohy na levnějším modelu</span></a>
<a href="/wiki/zaciname/kdyz-se-neco-pokazi/"><strong>Když se něco pokazí</strong><span>První pomoc a diagnostika</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-monitoring" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>OTLP export a alerty do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Tři úrovně
1) /usage v chatu: tokeny, rozpad ceny (vstup/výstup), stav kontextu, délka sezení, u některých
poskytovatelů zbývající kvóta/kredit. /insights = přehled za 30 dní.
2) Dashboard, stránka Status (obnovuje se po 5 s): verze, stav brány (PID, platformy), aktivní sezení
(5 min), posledních 20 sezení s modelem, počtem zpráv a tokenů. Pruh varování: paměť pod 128 MiB/15 %
nebo 64 MiB/5 %, disk pod 512 MB/256 MB, příp. předchozí OOM restart.
3) OTLP export (config.yaml): monitoring.gateway_health_export.enabled + monitoring.export.otlp
(enabled, endpoint http://collector:4318/v1/traces, headers_env = jméno hlavičky -> NÁZEV proměnné).
Kontrola: hermes monitoring status. Export je content-free: žádné prompty, zprávy, argumenty nástrojů,
jména úloh ani historie. Metriky: hermes.gateway.up/state/busy/active_agents/background_work, platformy,
cron. Traces: přechody stavu, cron lifecycle. Logs: jen varování/chyby s kódem.

## Alerty
hermes_gateway_up == 0 · chybějící řada delší než interval exportu (spadlý proces sám nulu nepošle)
· hermes.platform.degraded · stáří posledního úspěchu cronu.

## doctor
hermes doctor (exit 0 = bez problémů, 1 = něco zůstalo) -> použitelné jako cron/CI kontrola.
--fix zkusí opravit. Kontroluje i IPv6 trasu (rada: network.force_ipv4: true).

## Pozor
Bez SDK otlp se neexportuje, ale brána běží · nedostupný endpoint nesmí shodit agenta ·
málo paměti = zkrátit sezení/uber podagenty · velká spotřeba = kratší sezení, levnější model pro aux úlohy ·
monitoring bez notifikace není monitoring.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">📈</span><div><strong>Monitoring is not about having a chart. It is about knowing before your users do.</strong>
Hermes gives you three levels: an instant view in chat (<code>/usage</code>), an installation overview
in the dashboard, and a machine-readable metrics export for the systems you already watch. Start with
the first one — it is free and immediate.</div></div>

<h2>1. What it costs: <code>/usage</code> and <code>/insights</code></h2>
<table class="wiki-tabulka">
<tr><th>Command</th><th>What it shows</th></tr>
<tr><td><code>/usage</code></td><td>Token usage, cost breakdown (input/output), context window state, session duration and — when the provider supports it — remaining quota or credit</td></tr>
<tr><td><code>/insights</code></td><td>Usage overview for the last 30 days: what was used and what it cost</td></tr>
</table>
<p class="note">If the bill looks high, look at <strong>context size</strong> first, not at the price per
token. Long sessions without cleanup are the most common reason an account grows faster than the work
justifies.</p>

<h2>2. Installation overview: the dashboard</h2>
<p>The <strong>Status</strong> page refreshes every 5 seconds and shows:</p>
<table class="wiki-tabulka">
<tr><th>Item</th><th>Meaning</th></tr>
<tr><td>Version and release date</td><td>Which version you run (handy in a bug report)</td></tr>
<tr><td>Gateway status</td><td>Running/stopped, PID, connected platforms and their state</td></tr>
<tr><td>Active sessions</td><td>How many sessions were active in the last 5 minutes</td></tr>
<tr><td>Recent 20 sessions</td><td>Model, message count, token usage and a conversation preview</td></tr>
</table>
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">⚠️</span><div><strong>The resource banner is the most valuable thing on that page.</strong>
When memory runs low (below 128 MiB or 15 %) or disk space runs out (below 512 MB), a banner appears
at the top. For memory it even recognises that the agent died on the previous boot for lack of memory.
Without that banner an agent restart just looks like “some error”.</div></div>

<h2>3. Health from the command line: <code>hermes doctor</code></h2>
<div class="code-block">hermes doctor            <span class="c"># exit 0 = no problems, 1 = something remains</span>
hermes doctor --fix      <span class="c"># tries to repair what it can</span></div>
<p>The exit code turns <code>doctor</code> into a usable check for cron or CI: “if this fails, message me”.
It also checks the IPv6 route (a blackholed prefix is reported with the remedy
<code>network.force_ipv4: true</code>).</p>

<h2>4. Machine-readable metrics (OTLP)</h2>
<p>For real supervision — Prometheus, DataDog, an OpenTelemetry Collector — the gateway exports metrics,
events and diagnostics over OTLP/HTTP:</p>
<div class="code-block"><span class="c"># config.yaml</span>
monitoring:
  gateway_health_export:
    enabled: true
  export:
    otlp:
      enabled: true
      endpoint: http://collector-host:4318/v1/traces   <span class="c"># metrics and logs derive from it</span>
      headers_env: {}   <span class="c"># header name -> ENV VAR NAME (values are never stored)</span></div>
<div class="code-block">hermes monitoring status    <span class="c"># how it is configured and whether it runs</span></div>
<table class="wiki-tabulka">
<tr><th>Signal</th><th>Contents</th></tr>
<tr><td>Metrics</td><td><code>hermes.gateway.up/state/busy/active_agents/background_work</code>, platform state, cron ticker and job counts</td></tr>
<tr><td>Events (traces)</td><td>Gateway state transitions (<code>starting → running → draining → stopped</code>), platform changes, cron lifecycle</td></tr>
<tr><td>Diagnostics (logs)</td><td>Warnings and errors with a bounded error code and class — <strong>never prompt or message text</strong></td></tr>
</table>
<p class="note"><strong>The export is content-free by design:</strong> no prompts, messages, tool
arguments, job names or session history. Nothing you entrusted to the agent reaches a third-party
system — and you still learn that the gateway is down.</p>

<h2>What to alert on</h2>
<table class="wiki-tabulka">
<tr><th>Rule</th><th>Why</th></tr>
<tr><td><code>hermes_gateway_up == 0</code></td><td>The gateway is explicitly down (the process runs but does not report)</td></tr>
<tr><td>A missing series longer than the export interval</td><td>A process that died cannot emit its own zero — without this rule an outage goes unreported</td></tr>
<tr><td><code>hermes.platform.degraded</code></td><td>A platform (Telegram, Discord) lost its connection while the gateway keeps running</td></tr>
<tr><td>Age of the last cron success</td><td>A scheduled job stopped running — more common than a dead gateway</td></tr>
</table>
<p class="note">The second rule comes from our own operations: a metric that only says “I am OK” looks
like calm during an outage. Always monitor that the data <strong>stopped arriving</strong>, too.</p>

<h2>Things to watch</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>The OTLP SDK is missing</td><td>It installs on first use (the <code>otlp</code> extra); without it the gateway runs fine, it just does not export</td></tr>
<tr><td>The endpoint is unreachable</td><td>Export must never take the agent down — failures are bounded and stay off the hot path</td></tr>
<tr><td>The dashboard warns about memory</td><td>Shorten sessions, reduce parallel subagents, add RAM; the banner clears after a gateway restart</td></tr>
<tr><td>High token usage</td><td>Shorter sessions, a cheaper model for auxiliary tasks (e.g. the curator), fewer tools in context</td></tr>
<tr><td>You have monitoring but nobody looks</td><td>Set a threshold that sends a Telegram message — a chart nobody visits is not monitoring</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/scheduled-tasks/"><strong>Scheduled tasks (cron)</strong><span>How to check they really run</span></a>
<a href="/en/wiki/features/skill-curator/"><strong>Skill curator</strong><span>Auxiliary work on a cheaper model</span></a>
<a href="/en/wiki/getting-started/troubleshooting/"><strong>When something breaks</strong><span>First aid and diagnostics</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-monitoring" target="_blank" rel="noopener"><strong>Official documentation</strong><span>OTLP export and alerts in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Three levels
1) /usage in chat: tokens, cost breakdown (input/output), context state, session duration, remaining
quota/credit where supported. /insights = 30-day overview.
2) Dashboard Status page (refreshes every 5 s): version, gateway state (PID, platforms), active sessions
(5 min), recent 20 sessions with model, message count and tokens. Resource banner: memory below
128 MiB/15 % or 64 MiB/5 %, disk below 512 MB/256 MB, plus a previous OOM restart.
3) OTLP export (config.yaml): monitoring.gateway_health_export.enabled + monitoring.export.otlp
(enabled, endpoint http://collector:4318/v1/traces, headers_env = header name -> ENV VAR NAME).
Check: hermes monitoring status. Content-free: no prompts, messages, tool arguments, job names or history.
Metrics: hermes.gateway.up/state/busy/active_agents/background_work, platforms, cron.
Traces: state transitions, cron lifecycle. Logs: warnings/errors with bounded codes.

## Alerts
hermes_gateway_up == 0 · a missing series longer than the export interval (a dead process cannot emit zero)
· hermes.platform.degraded · age of the last cron success.

## doctor
hermes doctor (exit 0 = clean, 1 = problems remain) -> usable as a cron/CI gate. --fix repairs what it can.
Also checks the IPv6 route (remedy: network.force_ipv4: true).

## Watch out
Without the otlp SDK nothing is exported but the gateway runs · an unreachable endpoint must not take the
agent down · low memory = shorter sessions/fewer subagents · high usage = shorter sessions, cheaper aux model ·
monitoring without notification is not monitoring.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(30)
    stranka = najdi(30)
    assert stranka and stranka["nazev"] == "Měření a monitoring"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Měření a monitoring — kolik agent spotřeboval a jestli běží",
        "Přehled spotřeby tokenů a ceny, stav instalace v dashboardu, zdraví z příkazové řádky a export metrik přes OTLP včetně toho, na co nastavit výstrahu.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Měření a monitoring",
        "Monitoring není o tom mít graf. Je o tom vědět o problému dřív než uživatel — od /usage po napojení na váš dohled.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Měření a monitoring — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Usage and monitoring — what the agent consumed and whether it runs",
        "Token and cost overview, installation state in the dashboard, health from the command line and an OTLP metrics export including what to alert on.",
        OBRAZEK, "Wiki · Features in depth", "Usage and monitoring",
        "Monitoring is not about having a chart. It is about knowing before your users do — from /usage to your own supervision stack.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Usage and monitoring — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
