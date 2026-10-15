#!/usr/bin/env python3
"""Postaví stránku wiki „Časté dotazy" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/reference-faq.md (otázky a odpovědi), ostatní stránky wiki
(křížové odkazy), user-guide-features-memory.md, user-guide-security.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/reference/faq"
OBRAZEK = "wiki-dotazy"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">❓</span><div><strong>Patnáct otázek, na které se ptá nejvíc lidí — s krátkou odpovědí a odkazem na podrobnosti.</strong>
Když odpověď nestačí, u každé je odkaz na stránku, kde je to vysvětlené celé.</div></div>

<h2>Než začnete</h2>

<h3>Co je Hermes Agent?</h3>
<p>Program, který běží na vašem serveru a pracuje jako pomocník, kterému se zadává úkol lidskou řečí.
Umí spouštět příkazy, pracovat se soubory, hledat na webu, pamatovat si souvislosti a běžet podle plánu.
Podrobněji v části <a href="/co-je-hermes/">Co je Hermes</a>.</p>

<h3>Musím umět programovat?</h3>
<p>Ne. Zadání píšete běžnou řečí a příkazy, které je potřeba vložit do serveru, dostanete hotové —
stačí je vložit a potvrdit Enterem. Agent u každého kroku ověří, co se stalo.
Průvodce najdete v <a href="/wiki/zaciname/instalace/">instalaci</a>.</p>

<h3>Na čem to poběží?</h3>
<p>Na vlastním serveru (VPS) s Linuxem. Můžete použít i svůj počítač, ale server má výhodu: běží pořád,
takže se agent ozve i v noci a hlídané úlohy se nezastaví, když zavřete notebook.
Přehled možností je v části <a href="/hosting/">Hosting</a>.</p>

<h3>Jak dlouho zabere zprovoznění?</h3>
<p>Nejvíc času zabere založení účtu u poskytovatele modelu a vložení klíče (řádově minuty).
Vlastní instalace je několik kroků, které vás návod provede jednu po druhé a každý krok si ověříte.</p>

<h2>Peníze a data</h2>

<h3>Kolik to stojí?</h3>
<p>Program samotný je zdarma a open source. Platíte jen za používání modelu — tedy za to, kolik
s agentem mluvíte. S vlastním modelem na svém stroji neplatíte nic.
Ceny a doporučení jsou v části <a href="/wiki/zaciname/vyber-modelu/">Výběr AI modelu</a>.</p>

<h3>Posílají se moje data někam?</h3>
<p>Dotazy jdou <strong>jen k poskytovateli modelu, kterého si sami zvolíte</strong>. Sbírání statistik
ani telemetrie tu není a rozhovory, paměť a skilly zůstávají na vašem serveru ve složce
<code>~/.hermes/</code>. Jediné, co odchází, je text, na který se model ptáte.</p>

<h3>Můžu to používat bez internetu?</h3>
<p>Ano — s vlastním modelem na svém počítači (například Ollama). Agent se nastaví na vaši adresu
a dál nepotřebuje nic zvenčí. Počítejte ale s tím, že vlastní model je pomalejší a slabší než
placené modely v cloudu.</p>

<h2>Ovládání</h2>

<h3>Jak to ovládám z mobilu?</h3>
<p>Přes Telegram nebo Discord — agent se tam chová stejně jako v aplikaci a můžete si psát z telefonu,
i když jste mimo domov. Návod: <a href="/wiki/zaciname/telegram-a-discord/">Telegram a Discord</a>.</p>

<h3>Může agenta používat víc lidí?</h3>
<p>Ano. Přes připojené platformy může s jedním agentem mluvit víc lidí najednou; kdo smí psát,
určuje seznam povolených účtů, u soukromých zpráv navíc párování.
Detaily v části <a href="/wiki/zaciname/bezpecnost/">Bezpečnost</a>.</p>

<h3>Umí pracovat samo, když spím?</h3>
<p>Ano — tomu se říká <a href="/wiki/zaciname/pravidelne-ulohy/">pravidelné úlohy</a>. Ráno vám může
přijít přehled, v noci proběhnout kontrola a každou hodinu se ohlídat web.</p>

<h2>Paměť a znalosti</h2>

<h3>Pamatuje si, co jsme spolu dělali?</h3>
<p>Tři věci se liší: <strong>probíhající rozhovor</strong> (všechno, co jste si napsali), <strong>paměť</strong>
(krátký seznam podstatných věcí, který má agent vždy u sebe) a <strong>starší rozhovory</strong>
(dohledatelné bez omezení). Vysvětleno v části <a href="/wiki/zaciname/pamet/">Paměť agenta</a>.</p>

<h3>Jaký je rozdíl mezi pamětí a skillem?</h3>
<p><strong>Paměť</strong> obsahuje <em>fakta</em> — kdo jste, jak to u vás chodí, co si nepřejete.
<strong>Skill</strong> obsahuje <em>postup</em> — jak něco udělat krok za krokem.
Paměť se používá pořád, skill se vytáhne, když přijde vhodný úkol:
<a href="/wiki/zaciname/skilly/">Skilly</a>.</p>

<h3>Naučí se něco nového sám?</h3>
<p>Ano. Z toho, co se povedlo, si umí sepsat postup a příště ho použít. Můžete mu taky říct
<code>/learn</code> a dát mu dokumentaci nebo webovou stránku, ze které má postup napsat.</p>

<h2>Bezpečnost a provoz</h2>

<h3>Je to bezpečné?</h3>
<p>Agent má v sobě šest pojistek — od seznamu povolených účtů po potvrzení nebezpečných příkazů.
Než spustí něco, co maže nebo přepisuje, zeptá se vás. Celý přehled je v části
<a href="/wiki/zaciname/bezpecnost/">Bezpečnost</a>.</p>

<h3>Co když se něco pokazí?</h3>
<p>Nejdřív se podívejte, co se stalo (<code>hermes logs</code>), a nechte si zkontrolovat instalaci
(<code>hermes doctor</code>). Většina potíží má jednu z pěti příčin — přehled je v části
<a href="/wiki/zaciname/kdyz-se-neco-pokazi/">Když se něco pokazí</a>.</p>

<h3>Jak to úplně zastavím?</h3>
<p>Pravidelné úlohy zastaví <code>hermes pause</code> (a <code>hermes resume</code> je zase pustí).
Když chcete, aby agent přestal úplně, vypnete službu na serveru — běžící rozhovory se tím ukončí,
uložené rozhovory, paměť a skilly zůstanou.</p>

<h3>Kde se zeptám, když si nevím rady?</h3>
<p>V <a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener">naší Discord komunitě</a> —
nejrychleji se odpovídá tam. Oficiální dokumentace je na
<a href="https://hermes-agent.nousresearch.com/docs" target="_blank" rel="noopener">hermes-agent.nousresearch.com/docs</a>.</p>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/instalace/"><strong>Instalace</strong><span>Krok za krokem od začátku</span></a>
<a href="/wiki/zaciname/vyber-modelu/"><strong>Výběr AI modelu</strong><span>Ceny a doporučení</span></a>
<a href="/wiki/zaciname/kdyz-se-neco-pokazi/"><strong>Když se něco pokazí</strong><span>Nejčastější příčiny</span></a>
<a href="/wiki/zaciname/slovnicek/"><strong>Slovníček pojmů</strong><span>Aby bylo jasné, co které slovo znamená</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Než začnete
- Co je Hermes Agent? Program na vašem serveru, kterému zadáváte úkoly lidskou řečí; umí terminál,
  soubory, web, paměť a běh podle plánu.
- Musím umět programovat? Ne. Příkazy se vkládají hotové a potvrzují Enterem.
- Na čem poběží? Vlastní server (VPS) s Linuxem; i vlastní počítač, ale server běží pořád.
- Jak dlouho zabere zprovoznění? Nejdéle založení účtu u poskytovatele modelu a vložení klíče.

## Peníze a data
- Kolik to stojí? Program zdarma (open source), platí se jen za model; vlastní model zdarma.
- Posílají se data někam? Jen k poskytovateli modelu, kterého si zvolíte; žádná telemetrie;
  rozhovory, paměť a skilly zůstávají na serveru v ~/.hermes/.
- Bez internetu? Ano, s vlastním modelem (např. Ollama) - pomalejší a slabší.

## Ovládání
- Z mobilu: Telegram nebo Discord.
- Víc lidí: ano, seznam povolených účtů + párování u soukromých zpráv.
- Běh bez vás: pravidelné úlohy (cron).

## Paměť a znalosti
- Pamatuje si: tři místa - probíhající rozhovor, paměť (fakta), starší rozhovory (dohledatelné).
- Paměť vs skill: paměť = fakta, skill = postup.
- Učí se sám: z povedené práce si sepíše skill; /learn z dokumentace nebo webu.

## Bezpečnost a provoz
- Je to bezpečné? Šest pojistek, nebezpečné příkazy se potvrzují.
- Když se něco pokazí? hermes logs, hermes doctor; pět nejčastějších příčin.
- Zastavení: hermes pause (úlohy), vypnutí služby (agent); uložená data zůstávají.
- Pomoc: Discord komunity, oficiální dokumentace.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">❓</span><div><strong>Fifteen questions people ask most — with a short answer and a link to the details.</strong>
When a short answer is not enough, each question links to the page that explains it fully.</div></div>

<h2>Before you start</h2>

<h3>What is Hermes Agent?</h3>
<p>A program that runs on your server and works as an assistant you brief in plain language. It can run
commands, work with files, search the web, remember context and run on a schedule.
More in <a href="/en/what-is-hermes/">What is Hermes</a>.</p>

<h3>Do I need to know how to program?</h3>
<p>No. You write briefs in ordinary language, and any command that has to be pasted into the server comes
ready-made — you paste it and press Enter. The agent verifies each step.
Start with <a href="/en/wiki/getting-started/installation/">installation</a>.</p>

<h3>What does it run on?</h3>
<p>A Linux server of your own (a VPS). Your own computer works too, but a server has an advantage: it is
always on, so the agent can reach you at night and scheduled jobs do not stop when you close the laptop.
See <a href="/en/hosting/">Hosting</a>.</p>

<h3>How long does it take to set up?</h3>
<p>The slowest part is creating an account with a model provider and pasting the key (minutes).
The installation itself is a handful of steps, walked through one at a time, each of them verified.</p>

<h2>Money and data</h2>

<h3>How much does it cost?</h3>
<p>The program itself is free and open source. You only pay for using a model — that is, for how much you
talk to the agent. With a model of your own on your own machine, you pay nothing.
Prices and recommendations: <a href="/en/wiki/getting-started/choosing-a-model/">choosing a model</a>.</p>

<h3>Is my data sent anywhere?</h3>
<p>Requests go <strong>only to the model provider you choose yourself</strong>. There is no telemetry or
usage collection, and conversations, memory and skills stay on your server in <code>~/.hermes/</code>.
The only thing that leaves is the text you ask about.</p>

<h3>Can I use it offline?</h3>
<p>Yes — with a model running on your own machine (Ollama, for instance). The agent is pointed at your
address and needs nothing from outside. Expect a local model to be slower and less capable than paid
cloud models, though.</p>

<h2>Using it</h2>

<h3>How do I control it from my phone?</h3>
<p>Through Telegram or Discord — the agent behaves the same as in the app, so you can write from your phone
while away from home. Guide: <a href="/en/wiki/getting-started/telegram-and-discord/">Telegram and Discord</a>.</p>

<h3>Can several people use one agent?</h3>
<p>Yes. Through connected platforms several people can talk to the same agent at once; who may write is
decided by an allowlist of accounts, plus pairing for direct messages.
Details in <a href="/en/wiki/getting-started/security/">Security</a>.</p>

<h3>Can it work on its own while I sleep?</h3>
<p>Yes — that is <a href="/en/wiki/getting-started/scheduled-tasks/">scheduled tasks</a>. A brief can arrive
in the morning, a check can run at night, a website can be watched every hour.</p>

<h2>Memory and knowledge</h2>

<h3>Does it remember what we did together?</h3>
<p>Three things differ: the <strong>live conversation</strong> (everything you have written), <strong>memory</strong>
(a short list of essentials the agent always carries) and <strong>past conversations</strong> (searchable
without limit). Explained in <a href="/en/wiki/getting-started/memory/">Agent memory</a>.</p>

<h3>What is the difference between memory and a skill?</h3>
<p><strong>Memory</strong> holds <em>facts</em> — who you are, how things work for you, what you dislike.
A <strong>skill</strong> holds a <em>procedure</em> — how to do something step by step. Memory is always in
play; a skill is pulled out when a fitting task appears: <a href="/en/wiki/getting-started/skills/">Skills</a>.</p>

<h3>Does it learn anything on its own?</h3>
<p>Yes. From work that went well it can write itself a procedure and reuse it next time. You can also say
<code>/learn</code> and hand it documentation or a web page to write the procedure from.</p>

<h2>Safety and operation</h2>

<h3>Is it safe?</h3>
<p>The agent carries six safeguards — from the account allowlist to approving dangerous commands. Before
running something that deletes or overwrites, it asks you. The full overview is in
<a href="/en/wiki/getting-started/security/">Security</a>.</p>

<h3>What if something breaks?</h3>
<p>First find out what happened (<code>hermes logs</code>) and have the installation checked
(<code>hermes doctor</code>). Most trouble has one of five causes — see
<a href="/en/wiki/getting-started/troubleshooting/">When something breaks</a>.</p>

<h3>How do I stop it completely?</h3>
<p>Scheduled jobs stop with <code>hermes pause</code> (<code>hermes resume</code> starts them again).
To stop the agent entirely, stop the service on the server — running conversations end, while saved
conversations, memory and skills remain.</p>

<h3>Where do I ask when I am stuck?</h3>
<p>In our <a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener">community Discord</a> —
that is where answers come fastest. The official documentation lives at
<a href="https://hermes-agent.nousresearch.com/docs" target="_blank" rel="noopener">hermes-agent.nousresearch.com/docs</a>.</p>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/installation/"><strong>Installation</strong><span>Step by step from the start</span></a>
<a href="/en/wiki/getting-started/choosing-a-model/"><strong>Choosing a model</strong><span>Prices and recommendations</span></a>
<a href="/en/wiki/getting-started/troubleshooting/"><strong>When something breaks</strong><span>The most common causes</span></a>
<a href="/en/wiki/getting-started/glossary/"><strong>Glossary</strong><span>So every word makes sense</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Before you start
- What is Hermes Agent? A program on your server you brief in plain language; terminal, files, web,
  memory and scheduled runs.
- Do I need to program? No. Commands come ready-made, paste and press Enter.
- What does it run on? Your own Linux server (VPS); a personal computer works but is not always on.
- Setup time? The slowest part is creating a provider account and pasting the key.

## Money and data
- Cost? The program is free and open source; you pay only for the model; a local model is free.
- Is data sent anywhere? Only to the model provider you choose; no telemetry; conversations, memory and
  skills stay in ~/.hermes/ on your server.
- Offline? Yes with a local model (e.g. Ollama) - slower and less capable.

## Using it
- From a phone: Telegram or Discord.
- Several people: yes, allowlist of accounts plus DM pairing.
- Runs while you sleep: scheduled tasks (cron).

## Memory and knowledge
- Remembers: three places - the live conversation, memory (facts), past conversations (searchable).
- Memory vs skill: memory = facts, skill = procedure.
- Learns on its own: writes a skill from work that went well; /learn from documentation or a web page.

## Safety and operation
- Is it safe? Six safeguards; dangerous commands are approved by you.
- Something broke? hermes logs, hermes doctor; five most common causes.
- Stopping it: hermes pause (jobs), stop the service (agent); saved data remains.
- Help: community Discord, official documentation.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(11)
    stranka = najdi(11)
    assert stranka and stranka["nazev"] == "Časté dotazy"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Časté dotazy — co se lidi ptají nejvíc",
        "Patnáct nejčastějších otázek o Hermes Agentovi: co to je, kolik to stojí, kam odcházejí data, jak to ovládat z mobilu, jak si pamatuje a jak to zastavit.",
        OBRAZEK, "Wiki · Začínáme", "Časté dotazy",
        "Krátké odpovědi na to, na co se ptá nejvíc lidí — s odkazem na stránku, kde je to celé.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Časté dotazy — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Frequently asked questions — what people ask most",
        "Fifteen common questions about Hermes Agent: what it is, what it costs, where data goes, how to control it from a phone, how it remembers and how to stop it.",
        OBRAZEK, "Wiki · Start here", "Frequently asked questions",
        "Short answers to what people ask most — with a link to the page that covers it fully.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Frequently asked questions — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
