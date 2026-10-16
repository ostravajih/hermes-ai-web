#!/usr/bin/env python3
"""Postaví stránku wiki „Výběr AI modelu" (česky + anglicky) včetně verze pro AI.

Ceny jsou z oficiálních ceníků (api-docs.deepseek.com, OpenRouter) a v textu je vždy datum
ověření, protože se mění. Loga poskytovatelů jsou z jednobarevné sady simple-icons (licence CC0)
a vkládají se přímo do stránky — jsou ostrá, obarví se podle vzhledu a nejsou vymyšlená.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import STRANKY, ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "15. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models"
OBRAZEK = "wiki-model"

ZNACKY = [
    ("openai", "OpenAI", "Modely GPT — nejvyšší kvalita, vyšší cena", "GPT models — top quality, higher price", "https://platform.openai.com/"),
    ("anthropic", "Anthropic", "Claude — výborný na kód a dlouhé texty", "Claude — excellent for code and long texts", "https://console.anthropic.com/"),
    ("googlegemini", "Google Gemini", "Gemini — obrovský kontext, levné rychlé verze", "Gemini — huge context, cheap fast tiers", "https://ai.google.dev/"),
    ("deepseek", "DeepSeek", "Nejnižší ceny u kvalitních modelů, 1M kontext", "Among the lowest prices, 1M context", "https://platform.deepseek.com/"),
    ("qwen", "Qwen (Alibaba)", "Levné a rychlé modely na běžné úkoly", "Cheap, fast models for everyday tasks", "https://chat.qwen.ai/"),
    ("mistralai", "Mistral", "Evropský poskytovatel, otevřené modely", "European provider, open models", "https://console.mistral.ai/"),
    ("meta", "Meta (Llama)", "Otevřené modely — dají se spustit i doma", "Open models — can run locally too", "https://www.llama.com/"),
    ("x", "xAI", "Grok — alternativa k velkým modelům", "Grok — an alternative to the big models", "https://console.x.ai/"),
    ("openrouter", "OpenRouter", "Jeden účet na 300+ modelů, část i zdarma", "One account for 300+ models, some free", "https://openrouter.ai/"),
]


def logo(soubor: str) -> str:
    t = (ZDROJ / "loga" / f"{soubor}.svg").read_text(encoding="utf-8")
    view = re.search(r'viewBox="([^"]+)"', t).group(1)
    vnitrek = re.sub(r"<title>.*?</title>", "", t[t.find(">") + 1:t.rfind("</svg>")], flags=re.S).strip()
    return f'<svg viewBox="{view}" aria-hidden="true">{vnitrek}</svg>'


def znacky(jazyk: str) -> str:
    i = 2 if jazyk == "cs" else 3
    r = ['<div class="wiki-znacky">']
    for z in ZNACKY:
        r.append(f'<a class="wiki-znacka" href="{z[4]}" target="_blank" rel="noopener">'
                 f'<span class="wiki-znacka__logo">{logo(z[0])}</span>'
                 f'<strong>{z[1]}</strong><span>{z[i]}</span></a>')
    r.append("</div>")
    return "".join(r)


# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🧠</span><div><strong>Model je mozek agenta.</strong>
Jeho výběr je nejdůležitější rozhodnutí — stejný agent je s jedním modelem rychlý a spolehlivý a s jiným pomalý a zbytečně drahý.
Dobrá zpráva: vybírá se jedním příkazem (<code>hermes model</code>) a změnit se dá kdykoli později.</div></div>

<h2>Co model musí umět</h2>
<p>Ne každý model se pro agenta hodí. Ať vyberete cokoli, musí splnit tři věci:</p>
<table class="wiki-tabulka">
<tr><th>Požadavek</th><th>Proč</th></tr>
<tr><td><strong>Kontext aspoň 64 tisíc tokenů</strong></td><td>Agent si do konverzace skládá nástroje, návody a paměť. Menší kontext Hermes odmítne — na nástroje by nestačil</td></tr>
<tr><td><strong>Umí volat nástroje</strong> (tool calling)</td><td>Bez toho agent nemůže spouštět příkazy ani číst soubory — jen by povídal</td></tr>
<tr><td><strong>Rozumná cena za milion tokenů</strong></td><td>Agent posílá modelu hodně textu (nástroje, výsledky, historii). U drahých modelů se to rychle nasčítá</td></tr>
</table>
<p class="note">Čtení obrázků (vision) se hodí, ale není povinné — bez něj agent zvládne všechno kromě fotografií a screenshotů.</p>

<h2>Tři cesty k modelu</h2>
<table class="wiki-tabulka">
<tr><th>Cesta</th><th>Jak to funguje</th><th>Hodí se pro</th></tr>
<tr><td><strong>Nous Portal</strong></td><td>Jedno předplatné a přes 300 modelů pod jedním účtem. V Hermesu se přihlásíte příkazem <code>hermes setup --portal</code></td><td>Nejjednodušší začátek — jedno přihlášení, žádné klíče</td></tr>
<tr><td><strong>API klíč u poskytovatele</strong></td><td>Založíte účet (OpenAI, Anthropic, Google, DeepSeek…) a platíte za spotřebu, obvykle po dobití kreditu</td><td>Když chcete konkrétní model nebo nejnižší cenu</td></tr>
<tr><td><strong>OpenRouter</strong></td><td>Jeden účet a jedna platba za 300+ modelů od různých firem — přepínáte mezi nimi bez nových registrací</td><td>Když chcete vyzkoušet víc modelů a porovnávat</td></tr>
<tr><td><strong>Lokální model (Ollama)</strong></td><td>Model běží přímo na vašem stroji, nic neposílá ven</td><td>Jen na výkonném počítači s grafickou kartou — <strong>na malém VPS nereálné</strong></td></tr>
</table>

<h2>Kde modely pořídíte</h2>
<p>Klikněte na dlaždici a dostanete se rovnou na registraci:</p>
""" + znacky("cs") + """
<p class="note">Loga jsou jednobarevné značky poskytovatelů (sada simple-icons) — slouží k rozpoznání, neznamenají partnerství ani doporučení z jejich strany.</p>

<h2>Co doporučujeme (podzim 2026)</h2>
<table class="wiki-tabulka">
<tr><th>Na co</th><th>Doporučení</th><th>Proč</th></tr>
<tr><td>Úplný začátek a běžné úkoly</td><td><strong>DeepSeek</strong> (<code>deepseek-flash</code>)</td><td>Jedny z nejnižších cen, kontext 1 milion tokenů, umí nástroje i obrázky. Na učení ideální</td></tr>
<tr><td>Nejlepší poměr cena/výkon</td><td><strong>GLM (Z.ai), Kimi (Moonshot), Qwen</strong></td><td>V Hermesu jsou označené jako <em>doporučené</em> nebo <em>výchozí</em> — s nástroji si rozumí</td></tr>
<tr><td>Složité úkoly a programování</td><td><strong>Claude (Anthropic)</strong> nebo <strong>GPT (OpenAI)</strong></td><td>Nejspolehlivější na dlouhé postupy, ale několikanásobně dražší</td></tr>
<tr><td>Vyzkoušení zdarma</td><td>modely s označením <code>:free</code> na OpenRouteru</td><td>Nestojí nic, ale jsou pomalejší a mají limity — na hraní dobré, na provoz ne</td></tr>
<tr><td>Citlivá data nesmí ven</td><td>lokální model (Ollama) na vlastním stroji</td><td>Data zůstanou u vás; potřebujete ale pořádný počítač s grafickou kartou</td></tr>
</table>

<h2>Kolik to stojí</h2>
<p>Ceny se účtují za <strong>milion tokenů</strong> (token je kousek slova). Údaje jsou z oficiálních ceníků k 15. 10. 2026 — mění se, proto si je před platbou ověřte:</p>
<table class="wiki-tabulka">
<tr><th>Model</th><th>Vstup (za milion tokenů)</th><th>Výstup</th><th>Poznámka</th></tr>
<tr><td><code>deepseek-flash</code></td><td>0,15 $ mimo špičku / 0,30 $ ve špičce</td><td>0,60 $ / 1,20 $</td><td>kontext 1M, špička je dvakrát dražší</td></tr>
<tr><td><code>deepseek-v4-pro</code></td><td>0,66 $ / 1,32 $</td><td>1,98 $ / 3,96 $</td><td>silnější varianta stejné rodiny</td></tr>
<tr><td>modely na OpenRouteru</td><td>od ~0,14 $</td><td>od ~0,28 $</td><td>u 300+ modelů se ceny výrazně liší</td></tr>
<tr><td>Claude, GPT (špičkové)</td><td>jednotky dolarů</td><td>jednotky až desítky dolarů</td><td>řádově dražší než DeepSeek</td></tr>
</table>
<p><strong>Co je „špička“ u DeepSeeku:</strong> v pracovní dny 01:00–04:00 a 06:00–10:00 světového času (UTC). U nás to vychází na <strong>3:00–6:00 a 8:00–12:00</strong> (v zimě o hodinu dřív). Mimo špičku a o víkendu platíte polovinu — kdo nechá agenta pracovat v noci, ušetří.</p>
<p class="note"><strong>Kolik to vyjde měsíčně?</strong> Orientačně: při běžném osobním používání (desítky dotazů denně) se u DeepSeeku vejdete do desítek korun měsíčně. U špičkových modelů (Claude, GPT) počítejte s desetinásobkem i víc. Čím víc agent pracuje sám (pravidelné úlohy, sběr dat), tím víc spotřebuje.</p>

<h2>Pozor na dvě časté mýlky</h2>
<table class="wiki-tabulka">
<tr><th>Mýlka</th><th>Jak to je</th></tr>
<tr><td>„Mám předplatné ChatGPT Plus / Claude Pro, takže to mám zdarma.“</td><td>Ne. Předplatné platí pro jejich chat v prohlížeči. Agent potřebuje <strong>API přístup</strong>, kde se platí za spotřebu — jiný účet i jiná platba. Výjimkou je Nous Portal, kde předplatné zahrnuje model i nástroje</td></tr>
<tr><td>„Stačí nejlevnější model, je to jedno.“</td><td>Model s malým kontextem agent vůbec nespustí a model, který neumí nástroje, vám nic nespustí. Ušetřené koruny se vrátí jako hodiny ztracené práce</td></tr>
</table>

<h2>Jak model nastavit</h2>
<div class="code-block"><span class="c"># varianta A: jedno přihlášení přes Nous Portal (nejjednodušší začátek)</span>
<span class="p">$</span> hermes setup --portal</div>
<div class="code-block"><span class="c"># varianta B: ruční výběr poskytovatele a vložení klíče</span>
<span class="p">$</span> hermes model</div>
<div class="code-block"><span class="c"># co je právě nastavené</span>
<span class="p">$</span> hermes portal info</div>
<p>V běžícím rozhovoru model změníte lomítkovým příkazem <code>/model</code> — použije se hned. Nastavení z příkazové řádky platí pro <strong>nové</strong> konverzace.</p>

<h2>Naše tipy z provozu</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Začněte levným modelem (DeepSeek)</td><td>Naučíte se, co agent umí, a zaplatíte pár korun. Drahý model má smysl až na úkoly, na které levný nestačí</td></tr>
<tr><td>Špičkový model zapínejte jen na těžké úkoly</td><td>Příkazem <code>/model</code> uprostřed práce — drahý model tak platíte jen za to, co má opravdu udělat</td></tr>
<tr><td>Nastavte si i pomocný model</td><td>Vedlejší úlohy (čtení obrázků, shrnutí) umí Hermes posílat levnému modelu a hlavní nechat na kvalitním</td></tr>
<tr><td>Pravidelné úlohy plánujte mimo špičku</td><td>U DeepSeeku je mimo špičku poloviční cena a v noci agent nikoho neobtěžuje</td></tr>
<tr><td>Sledujte zaplnění kontextu</td><td>Příkaz <code>/context</code> v rozhovoru ukáže, jak je kontext plný; <code>/compress</code> ho srovná</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/prvni-chat/"><strong>První chat s agentem</strong><span>Jak zadávat úkoly, aby se daly ověřit</span></a>
<a href="/instalace/"><strong>Instalace</strong><span>Když ještě agenta nemáte spuštěného</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Nastavení modelů do detailu (anglicky)</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Discord komunity</strong><span>Zeptejte se, co komu funguje</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co model musí umět
- kontext aspoň 64 000 tokenů (jinak Hermes model odmítne)
- umět volat nástroje (tool calling) — bez toho agent nespustí příkazy
- rozumná cena za milion tokenů (agent posílá hodně textu)
- čtení obrázků (vision) výhodou, ne podmínkou

## Tři cesty k modelu
1. Nous Portal — jedno předplatné, 300+ modelů: hermes setup --portal
2. API klíč u poskytovatele (OpenAI, Anthropic, Google, DeepSeek…) — platba za spotřebu
3. OpenRouter — jeden účet na 300+ modelů různých firem
4. Lokální model (Ollama) — jen na stroji s grafickou kartou, na malém VPS nereálné

## Doporučení (podzim 2026)
- začátek a běžné úkoly: DeepSeek (deepseek-flash) — jedny z nejnižších cen, 1M kontext
- poměr cena/výkon: GLM (Z.ai), Kimi (Moonshot), Qwen — v Hermesu doporučené/výchozí
- složité úkoly a kód: Claude (Anthropic), GPT (OpenAI) — několikanásobně dražší
- zdarma na vyzkoušení: modely s :free na OpenRouteru

## Ceny (oficiální ceníky k 15. 10. 2026 — mění se)
- deepseek-flash: 0,15 $ / 0,60 $ za milion tokenů (vstup/výstup) mimo špičku, ve špičce dvojnásobek
- deepseek-v4-pro: 0,66 $ / 1,98 $ mimo špičku
- OpenRouter: od ~0,14 $ vstup / ~0,28 $ výstup
- Claude, GPT: jednotky až desítky dolarů za milion tokenů
Špička DeepSeeku = pracovní dny 01:00–04:00 a 06:00–10:00 UTC (u nás 3:00–6:00 a 8:00–12:00, v zimě o hodinu dřív).
Měsíčně: osobní používání u DeepSeeku desítky korun, u špičkových modelů desetinásobek i víc.

## Časté mýlky
- Předplatné ChatGPT Plus / Claude Pro NENÍ přístup pro agenta — potřebujete API (platba za spotřebu).
  Výjimka: Nous Portal, kde předplatné zahrnuje model i nástroje.
- Nejlevnější model nestačí: malý kontext agent odmítne, model bez nástrojů nic nespustí.

## Nastavení
hermes setup --portal   # Nous Portal, jedno přihlášení
hermes model            # ruční výběr poskytovatele a klíč
hermes portal info      # co je nastavené
/model                  # změna v běžícím rozhovoru
Nastavení z příkazové řádky platí pro nové konverzace.

## Tipy
- začněte levným modelem, drahý používejte na těžké úkoly přes /model
- vedlejší úlohy (obrázky, shrnutí) lze posílat levnému pomocnému modelu
- pravidelné úlohy plánujte mimo špičku (poloviční cena)
- /context ukáže zaplnění kontextu, /compress ho srovná
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🧠</span><div><strong>The model is the agent's brain.</strong>
Choosing it is the most important decision you make — the same agent is fast and reliable with one model and slow and needlessly
expensive with another. The good news: you pick it with one command (<code>hermes model</code>) and can change it any time later.</div></div>

<h2>What a model must be able to do</h2>
<p>Not every model suits an agent. Whatever you pick, it must meet three conditions:</p>
<table class="wiki-tabulka">
<tr><th>Requirement</th><th>Why</th></tr>
<tr><td><strong>At least 64k tokens of context</strong></td><td>The agent packs tools, guides and memory into the conversation. Smaller context is rejected by Hermes — it would not fit the tools</td></tr>
<tr><td><strong>Tool calling support</strong></td><td>Without it the agent cannot run commands or read files — it would only talk</td></tr>
<tr><td><strong>Sensible price per million tokens</strong></td><td>The agent sends a lot of text (tools, results, history). With expensive models this adds up fast</td></tr>
</table>
<p class="note">Reading images (vision) is useful but optional — without it the agent handles everything except photos and screenshots.</p>

<h2>Three routes to a model</h2>
<table class="wiki-tabulka">
<tr><th>Route</th><th>How it works</th><th>Best for</th></tr>
<tr><td><strong>Nous Portal</strong></td><td>One subscription and 300+ models under a single account. In Hermes you sign in with <code>hermes setup --portal</code></td><td>The easiest start — one login, no API keys</td></tr>
<tr><td><strong>API key at a provider</strong></td><td>You create an account (OpenAI, Anthropic, Google, DeepSeek…) and pay for usage, usually by topping up credit</td><td>A specific model or the lowest price</td></tr>
<tr><td><strong>OpenRouter</strong></td><td>One account and one payment for 300+ models from different companies — switch between them with no new signups</td><td>Trying several models and comparing</td></tr>
<tr><td><strong>Local model (Ollama)</strong></td><td>The model runs on your own machine and sends nothing out</td><td>Only on a powerful computer with a GPU — <strong>unrealistic on a small VPS</strong></td></tr>
</table>

<h2>Where to get the models</h2>
<p>Click a tile to go straight to the signup page:</p>
""" + znacky("en") + """
<p class="note">The logos are monochrome provider marks (the simple-icons set) — they are here for recognition only and imply no partnership or endorsement.</p>

<h2>What we recommend (autumn 2026)</h2>
<table class="wiki-tabulka">
<tr><th>For</th><th>Recommendation</th><th>Why</th></tr>
<tr><td>Getting started and everyday tasks</td><td><strong>DeepSeek</strong> (<code>deepseek-flash</code>)</td><td>Among the lowest prices, 1M token context, supports tools and images. Ideal for learning</td></tr>
<tr><td>Best value for money</td><td><strong>GLM (Z.ai), Kimi (Moonshot), Qwen</strong></td><td>Marked as <em>recommended</em> or <em>default</em> in Hermes — they handle tools well</td></tr>
<tr><td>Complex tasks and coding</td><td><strong>Claude (Anthropic)</strong> or <strong>GPT (OpenAI)</strong></td><td>Most reliable on long procedures, but several times more expensive</td></tr>
<tr><td>Trying it for free</td><td>models tagged <code>:free</code> on OpenRouter</td><td>Cost nothing, but are slower and rate limited — fine for playing, not for production</td></tr>
<tr><td>Sensitive data must stay in-house</td><td>a local model (Ollama) on your own machine</td><td>Data never leaves you; you do need a proper GPU machine</td></tr>
</table>

<h2>What it costs</h2>
<p>Prices are charged per <strong>million tokens</strong> (a token is a piece of a word). The figures below come from the official price lists as of 15 Oct 2026 — they change, so check before you pay:</p>
<table class="wiki-tabulka">
<tr><th>Model</th><th>Input (per million tokens)</th><th>Output</th><th>Note</th></tr>
<tr><td><code>deepseek-flash</code></td><td>$0.15 off-peak / $0.30 peak</td><td>$0.60 / $1.20</td><td>1M context, peak hours cost double</td></tr>
<tr><td><code>deepseek-v4-pro</code></td><td>$0.66 / $1.32</td><td>$1.98 / $3.96</td><td>stronger variant of the same family</td></tr>
<tr><td>models on OpenRouter</td><td>from ~$0.14</td><td>from ~$0.28</td><td>prices vary widely across 300+ models</td></tr>
<tr><td>Claude, GPT (flagships)</td><td>single-digit dollars</td><td>single to double-digit dollars</td><td>an order of magnitude above DeepSeek</td></tr>
</table>
<p><strong>What "peak" means at DeepSeek:</strong> weekdays 01:00–04:00 and 06:00–10:00 UTC. In Czechia that is <strong>3:00–6:00 and 8:00–12:00</strong> (an hour earlier in winter). Off-peak and at weekends you pay half — scheduling the agent to work at night saves money.</p>
<p class="note"><strong>What about a monthly bill?</strong> As a rough guide: ordinary personal use (dozens of questions a day) stays within tens of Czech crowns a month on DeepSeek. With flagship models (Claude, GPT) expect ten times that or more. The more the agent works on its own (scheduled tasks, data collection), the more it spends.</p>

<h2>Two common misconceptions</h2>
<table class="wiki-tabulka">
<tr><th>Misconception</th><th>Reality</th></tr>
<tr><td>"I have a ChatGPT Plus / Claude Pro subscription, so this is free."</td><td>No. Those subscriptions cover their chat in a browser. An agent needs <strong>API access</strong>, billed per usage — a different account and a different payment. The exception is Nous Portal, where the subscription includes both the model and the tools</td></tr>
<tr><td>"The cheapest model is enough, it does not matter."</td><td>A model with a small context will not even start, and a model without tool support will run nothing for you. The money you saved returns as hours of lost work</td></tr>
</table>

<h2>How to set the model</h2>
<div class="code-block"><span class="c"># option A: one sign-in via Nous Portal (the easiest start)</span>
<span class="p">$</span> hermes setup --portal</div>
<div class="code-block"><span class="c"># option B: pick a provider manually and paste a key</span>
<span class="p">$</span> hermes model</div>
<div class="code-block"><span class="c"># what is configured right now</span>
<span class="p">$</span> hermes portal info</div>
<p>Inside a running chat you switch models with the <code>/model</code> slash command — it applies immediately. Settings made from the command line apply to <strong>new</strong> conversations.</p>

<h2>Tips from running it</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Start with a cheap model (DeepSeek)</td><td>You learn what the agent can do for a few crowns. An expensive model only pays off on tasks the cheap one cannot handle</td></tr>
<tr><td>Reach for a flagship only on hard tasks</td><td>Switch with <code>/model</code> mid-task — you then pay the expensive model only for what it really has to do</td></tr>
<tr><td>Set an auxiliary model too</td><td>Side tasks (reading images, summaries) can go to a cheap model while the main one stays high quality</td></tr>
<tr><td>Schedule recurring jobs off-peak</td><td>DeepSeek is half price off-peak, and a night job bothers nobody</td></tr>
<tr><td>Watch how full the context gets</td><td>The <code>/context</code> command in a chat shows how full it is; <code>/compress</code> trims it</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/first-chat/"><strong>Your first chat</strong><span>How to give verifiable tasks</span></a>
<a href="/en/installation/"><strong>Installation</strong><span>If the agent is not running yet</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Model configuration in detail</span></a>
<a href="https://discord.gg/ysx9dbXpdD" target="_blank" rel="noopener"><strong>Community Discord</strong><span>Ask what works for others</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What a model must do
- at least 64,000 tokens of context (otherwise Hermes rejects it)
- tool calling support - without it the agent cannot run commands
- sensible price per million tokens (the agent sends a lot of text)
- vision is a bonus, not a requirement

## Three routes
1. Nous Portal - one subscription, 300+ models: hermes setup --portal
2. API key at a provider (OpenAI, Anthropic, Google, DeepSeek...) - pay per usage
3. OpenRouter - one account for 300+ models from different companies
4. Local model (Ollama) - only on a machine with a GPU, unrealistic on a small VPS

## Recommendations (autumn 2026)
- start and everyday tasks: DeepSeek (deepseek-flash) - among the lowest prices, 1M context
- value for money: GLM (Z.ai), Kimi (Moonshot), Qwen - marked recommended/default in Hermes
- complex tasks and code: Claude (Anthropic), GPT (OpenAI) - several times more expensive
- free for testing: models tagged :free on OpenRouter

## Prices (official price lists as of 15 Oct 2026 - they change)
- deepseek-flash: $0.15 / $0.60 per million tokens (input/output) off-peak, double at peak
- deepseek-v4-pro: $0.66 / $1.98 off-peak
- OpenRouter: from ~$0.14 input / ~$0.28 output
- Claude, GPT: single to double-digit dollars per million tokens
DeepSeek peak = weekdays 01:00-04:00 and 06:00-10:00 UTC (03:00-06:00 and 08:00-12:00 in Czechia).
Monthly: personal use on DeepSeek costs tens of CZK, flagship models ten times that or more.

## Misconceptions
- A ChatGPT Plus / Claude Pro subscription is NOT agent access - you need the API (usage based).
  Exception: Nous Portal, where the subscription includes model and tools.
- The cheapest model is not enough: small context is rejected and a model without tools runs nothing.

## Setting it up
hermes setup --portal   # Nous Portal, one sign-in
hermes model            # pick a provider manually and paste a key
hermes portal info      # what is configured
/model                  # switch inside a running chat
Command-line settings apply to new conversations.

## Tips
- start cheap, use an expensive model only for hard tasks via /model
- side tasks (images, summaries) can go to a cheap auxiliary model
- schedule recurring jobs off-peak (half price)
- /context shows how full the context is, /compress trims it
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(2)
    stranka = najdi(2)
    assert stranka and stranka["nazev"] == "Výběr AI modelu", "stránka 2 musí být Výběr AI modelu"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Výběr AI modelu pro Hermes Agenta — doporučení a ceny",
        "Které AI modely se pro agenta hodí, co musí umět, kolik stojí a kde je pořídit — včetně plateb z Česka a doporučení pro začátek.",
        OBRAZEK, "Wiki · Začínáme", "Výběr AI modelu",
        "Agent je jen tak dobrý, jaký model mu dáte. Tady je výběr bez zbytečné teorie — co musí model umět, co doporučujeme a kolik to vyjde.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Výběr AI modelu — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Choosing an AI model for Hermes Agent — picks and prices",
        "Which AI models suit an agent, what they must support, what they cost and where to buy them — including paying from Czechia.",
        OBRAZEK, "Wiki · Start here", "Choosing an AI model",
        "An agent is only as good as the model you give it. Here is how to choose without the theory — what a model must support, what we recommend and what it costs.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Choosing an AI model — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
