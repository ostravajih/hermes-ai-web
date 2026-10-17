#!/usr/bin/env python3
"""Postaví stránku wiki „GitHub" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/guides-github-pr-review-agent.md (gh CLI, ověření přístupu, ruční revize,
cron místo webhooku, doručení výsledků, review skill) a user-guide-messaging-webhooks.md
(webhook pro okamžité revize) + reference-skills-catalog.md (bundled skill github).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent"
OBRAZEK = "wiki-github"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🐙</span><div><strong>Agent s přístupem k repozitáři není „jen čtenář“ — má stejná práva jako vy.</strong>
Když mu dáte token s právem zápisu, může pushovat, mazat větve i zavírat pull requesty.
Začněte právem jen pro čtení, pusťte ho do jednoho repozitáře a teprve pak přidávejte práva podle toho,
co mu opravdu chcete dovolit.</div></div>

<h2>Co k tomu patří</h2>
<table class="wiki-tabulka">
<tr><th>Věc</th><th>K čemu</th></tr>
<tr><td>GitHub CLI <code>gh</code></td><td>Přes něj agent dělá všechno — PR, issues, revize, repozitáře</td></tr>
<tr><td>Přihlášení <code>gh auth login</code></td><td>Buď interaktivně, nebo tokenem (<code>GH_TOKEN</code> v prostředí)</td></tr>
<tr><td>Běžící brána</td><td>Bez ní nefungují pravidelné úlohy ani webhooky</td></tr>
<tr><td>Skill <code>github</code></td><td>Hotový návod, jak s <code>gh</code> pracovat (je součástí Hermese)</td></tr>
</table>

<h2>Ověření, že to funguje</h2>
<div class="code-block">gh auth status                              <span class="c"># kdo jsem a co smím</span>
gh pr list --repo vlasnik/repo --state open --limit 3
gh pr diff 42 --repo vlasnik/repo           <span class="c"># co PR mění</span></div>
<p>Když tohle projde, agent má přístup a můžete mu zadávat práci. Když ne, chyba obvykle říká,
které oprávnění (scope) chybí.</p>

<h2>Revize pull requestu</h2>
<div class="code-block">Zkontroluj tento pull request: přečti diff a najdi chyby, bezpečnostní problémy
a nekvalitní kód. Buď konkrétní — čísla řádků a citace problematického kódu.</div>
<p>Agent si diff stáhne, projde ho a napíše strukturovanou revizi. Když chcete, aby to dělal
<strong>pořád stejně</strong>, udělejte z toho skill (vlastní pravidla revize) — pak se nemusí pokaždé
učit, co vás zajímá.</p>

<h2>Dvě cesty k automatickým revizím</h2>
<table class="wiki-tabulka">
<tr><th></th><th>Pravidelná úloha (cron)</th><th>Webhook</th></tr>
<tr><td>Jak to funguje</td><td>Každé 2 hodiny se agent zeptá, co je nového</td><td>GitHub zavolá hned, když PR vznikne</td></tr>
<tr><td>Potřebuje veřejnou adresu</td><td>Ne — funguje i za firewallem</td><td>Ano (přes reverzní proxy)</td></tr>
<tr><td>Zpoždění</td><td>Do intervalu</td><td>Vteřiny</td></tr>
<tr><td>Vhodné pro</td><td>Malý tým, osobní repozitáře</td><td>Firmu, kde záleží na čase</td></tr>
</table>
<p class="note">Cron je bezpečnější začátek: nic nevystavujete do internetu a přesto máte revizi
u každého PR. Webhook přidejte, až když vám zpoždění vadí (viz stránka o webhookách).</p>

<h2>Co agent umí v repozitáři</h2>
<table class="wiki-tabulka">
<tr><th>Úkol</th><th>Příklad</th></tr>
<tr><td>Projít a okomentovat PR</td><td>Revize s konkrétními nálezy, komentář přímo v PR</td></tr>
<tr><td>Založit větev a commit</td><td>Oprava, kterou pak projde CI</td></tr>
<tr><td>Issues</td><td>Založit, okomentovat, označit, zavřít</td></tr>
<tr><td>CI a kontroly</td><td>Přečíst výsledky běhů a najít, co spadlo</td></tr>
<tr><td>Release a tagy</td><td>Připravit vydání (s právem zápisu)</td></tr>
</table>

<h2>Na co si dát pozor</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Agent pushuje přímo do <code>main</code></td><td>Zapněte ochranu větve (branch protection) a nechte ho pracovat jen přes PR</td></tr>
<tr><td>Token v gitu nebo v chatu</td><td>Token patří do <code>.env</code> (nebo do správce hesel); při úniku ho zneplatněte</td></tr>
<tr><td>Revize je obecná („kód vypadá dobře“)</td><td>Napište skill s vašimi pravidly a příklady; bez nich agent hádá, co je důležité</td></tr>
<tr><td>Agent komentuje každý PR i tam, kde nemá</td><td>Omezte úlohu na konkrétní repozitáře a štítky</td></tr>
<tr><td>Chybí oprávnění</td><td><code>gh auth status</code> řekne které; u jemně zrnitých tokenů se přidává scope</td></tr>
</table>

<h2>Jak to máme u nás</h2>
<table class="wiki-tabulka">
<tr><th>Zvyk</th><th>Proč</th></tr>
<tr><td>Token jen pro čtení, dokud není potřeba zapisovat</td><td>Většina práce je čtení a komentování</td></tr>
<tr><td>Změny vždy přes větev a PR, nikdy přímo do <code>main</code></td><td>I když agent umí pushovat, člověk má poslední slovo</td></tr>
<tr><td>Vlastní skill s pravidly revize</td><td>Revize je pak stejná každý den a nemíjí to, na čem nám záleží</td></tr>
<tr><td>Výsledky do Telegramu, ne do e-mailu</td><td>Uvidíme je hned a nezapadnou</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/funkce/webhooky/"><strong>Webhooky</strong><span>Okamžitá revize, když PR vznikne</span></a>
<a href="/wiki/zaciname/skilly/"><strong>Skilly</strong><span>Vlastní pravidla revize</span></a>
<a href="/wiki/funkce/spousteni-prikazu/"><strong>Spouštění příkazů</strong><span>Co agent smí spustit sám</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Návod na revizního agenta (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co potřebujete
gh CLI (apt/brew), gh auth login nebo GH_TOKEN, běžící brána (cron/webhooky), bundled skill github.
Ověření: gh auth status · gh pr list --repo v/r --state open · gh pr diff <číslo> --repo v/r.

## Revize PR
Zadání: přečti diff, najdi chyby/bezpečnost/nekvalitní kód, buď konkrétní (čísla řádků, citace).
Pro opakovatelnou kvalitu si udělejte skill s pravidly revize.

## Automatizace
Cron každé 2 h (nepotřebuje veřejnou adresu, funguje za firewallem, zpoždění do intervalu)
vs webhook (GitHub zavolá hned, potřebuje veřejnou HTTPS adresu). Začněte cronem.

## Co umí
Komentovat PR, zakládat větve/commity, issues, číst CI, release a tagy (podle práv tokenu).

## Pozor
Branch protection + práce jen přes PR · token do .env, ne do gitu/chatu · obecná revize = chybí skill
s pravidly · omezit na konkrétní repozitáře · chybějící scope ukáže gh auth status.

## U nás
Token jen pro čtení, dokud není potřeba zápis; změny přes PR; vlastní skill s pravidly; výsledky do Telegramu.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🐙</span><div><strong>An agent with repository access is not “just a reader” — it has the same rights you do.</strong>
Give it a write token and it can push, delete branches and close pull requests.
Start read-only, in one repository, and add rights only as you actually need them.</div></div>

<h2>What it takes</h2>
<table class="wiki-tabulka">
<tr><th>Item</th><th>Purpose</th></tr>
<tr><td>GitHub CLI <code>gh</code></td><td>The agent does everything through it — PRs, issues, reviews, repos</td></tr>
<tr><td><code>gh auth login</code></td><td>Interactively, or with a token (<code>GH_TOKEN</code> in the environment)</td></tr>
<tr><td>A running gateway</td><td>Without it neither scheduled jobs nor webhooks work</td></tr>
<tr><td>The bundled <code>github</code> skill</td><td>A ready-made guide to working with <code>gh</code></td></tr>
</table>

<h2>Verify it works</h2>
<div class="code-block">gh auth status                              <span class="c"># who am I and what may I do</span>
gh pr list --repo owner/repo --state open --limit 3
gh pr diff 42 --repo owner/repo             <span class="c"># what the PR changes</span></div>
<p>If this passes, the agent has access and you can hand it work. If not, the error usually names the
missing scope.</p>

<h2>Reviewing a pull request</h2>
<div class="code-block">Review this pull request: read the diff and look for bugs, security problems
and poor code. Be specific — line numbers and quotes of the problematic code.</div>
<p>The agent fetches the diff, reads it and writes a structured review. If you want it done
<strong>the same way every time</strong>, turn that into a skill (your own review rules) — then it does
not have to guess what you care about.</p>

<h2>Two ways to automate reviews</h2>
<table class="wiki-tabulka">
<tr><th></th><th>Scheduled job (cron)</th><th>Webhook</th></tr>
<tr><td>How it works</td><td>Every 2 hours the agent asks what is new</td><td>GitHub calls in as soon as a PR appears</td></tr>
<tr><td>Needs a public address</td><td>No — works behind a firewall</td><td>Yes (through a reverse proxy)</td></tr>
<tr><td>Delay</td><td>Up to the interval</td><td>Seconds</td></tr>
<tr><td>Best for</td><td>Small teams, personal repos</td><td>A company where speed matters</td></tr>
</table>
<p class="note">Cron is the safer start: nothing is exposed to the internet and every PR still gets
reviewed. Add a webhook when the delay starts to hurt (see the webhooks page).</p>

<h2>What the agent can do in a repository</h2>
<table class="wiki-tabulka">
<tr><th>Task</th><th>Example</th></tr>
<tr><td>Review and comment on PRs</td><td>A review with concrete findings, posted as a PR comment</td></tr>
<tr><td>Create a branch and commit</td><td>A fix that then goes through CI</td></tr>
<tr><td>Issues</td><td>Open, comment on, label, close</td></tr>
<tr><td>CI and checks</td><td>Read run results and find what failed</td></tr>
<tr><td>Releases and tags</td><td>Prepare a release (with a write token)</td></tr>
</table>

<h2>Things to watch</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>The agent pushes straight to <code>main</code></td><td>Enable branch protection and make it work through PRs only</td></tr>
<tr><td>A token in git or chat</td><td>Tokens belong in <code>.env</code> (or a password manager); revoke if leaked</td></tr>
<tr><td>The review is generic (“looks good”)</td><td>Write a skill with your rules and examples; without them the agent guesses what matters</td></tr>
<tr><td>It comments on every PR, even where it should not</td><td>Limit the job to specific repositories and labels</td></tr>
<tr><td>Missing permissions</td><td><code>gh auth status</code> names the scope; fine-grained tokens need it added</td></tr>
</table>

<h2>How we do it</h2>
<table class="wiki-tabulka">
<tr><th>Habit</th><th>Why</th></tr>
<tr><td>Read-only token until writing is actually needed</td><td>Most work is reading and commenting</td></tr>
<tr><td>Always a branch and a PR, never straight to <code>main</code></td><td>Even when the agent can push, a human has the last word</td></tr>
<tr><td>A dedicated skill with review rules</td><td>The review is consistent day to day and does not miss what we care about</td></tr>
<tr><td>Results to Telegram, not e-mail</td><td>We see them immediately and they do not get buried</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/features/webhooks/"><strong>Webhooks</strong><span>Instant review when a PR opens</span></a>
<a href="/en/wiki/getting-started/skills/"><strong>Skills</strong><span>Your own review rules</span></a>
<a href="/en/wiki/features/command-execution/"><strong>Running commands</strong><span>What the agent may run on its own</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/guides/github-pr-review-agent" target="_blank" rel="noopener"><strong>Official documentation</strong><span>The PR review agent tutorial</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Requirements
gh CLI (apt/brew), gh auth login or GH_TOKEN, a running gateway (cron/webhooks), the bundled github skill.
Verify: gh auth status · gh pr list --repo o/r --state open · gh pr diff <n> --repo o/r.

## Reviewing a PR
Prompt: read the diff, find bugs/security/poor code, be specific (line numbers, quotes).
For repeatable quality, write a skill with review rules.

## Automation
Cron every 2 h (no public address, works behind a firewall, delay up to the interval) vs a webhook
(GitHub calls immediately, needs a public HTTPS address). Start with cron.

## Capabilities
Comment on PRs, create branches/commits, issues, read CI, releases and tags (per token scope).

## Watch out
Branch protection + PRs only · token in .env, never git/chat · a generic review means a missing rules skill
· limit to specific repositories · gh auth status names a missing scope.

## Our practice
Read-only token until writing is needed; changes via PRs; a dedicated review skill; results to Telegram.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(36)
    stranka = najdi(36)
    assert stranka and stranka["nazev"] == "GitHub"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "GitHub — revize pull requestů a práce v repozitáři",
        "Jak agenta připojit k GitHubu přes gh CLI, jak ověřit oprávnění, jak vypadá užitečná revize PR a jak ji automatizovat cronem nebo webhookem.",
        OBRAZEK, "Wiki · Integrace", "GitHub",
        "Agent s přístupem k repozitáři má stejná práva jako vy. Jak mu je dát rozumně a co mu pak zadávat.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "GitHub (česká wiki)", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "GitHub — pull request reviews and working in a repository",
        "Connecting the agent to GitHub through gh CLI, checking permissions, what a useful PR review looks like and how to automate it with cron or a webhook.",
        OBRAZEK, "Wiki · Integrations", "GitHub",
        "An agent with repository access has the same rights you do. How to grant them sensibly and what to give it to do.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "GitHub (community wiki)", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
