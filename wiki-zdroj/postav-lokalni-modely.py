#!/usr/bin/env python3
"""Postaví stránku wiki „Lokální modely" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-local-models.md (katalog modelů pro váš stroj, stažení,
správa paměti, vlastní llama-server, požadavky a meze),
wiki-zdroj/stranky/guides-local-ollama-setup.md (Ollama, srovnání ceny, co se lokálně vyplatí).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/local-models"
OBRAZEK = "wiki-lokalni-modely"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🏠</span><div><strong>Lokální model je jako domácí pekárna: máte ji, nic neplatíte za každý bochník a nikdo se nedozví, co pečete.</strong>
Ale trvá to déle a na složitý dort si radši zajdete do cukrárny. Přesně tak se k tomu stavíme —
lokální model na soukromé a jednoduché věci, velký model v cloudu na to ostatní.</div></div>

<h2>Kdy se to vyplatí a kdy ne</h2>
<table class="wiki-tabulka">
<tr><th>Vyplatí se</th><th>Nevyplatí se</th></tr>
<tr><td>Data nesmí opustit váš počítač (smlouvy, zdravotní zprávy, interní kód)</td><td>Složitá mnohakroková práce, kde musí agent spolehlivě používat nástroje</td></tr>
<tr><td>Práce bez internetu nebo na cestě</td><td>Dlouhé rozhovory a dlouhé dokumenty</td></tr>
<tr><td>Opakované jednoduché úlohy: shrnutí, překlad, vytěžení údajů z textu, psaní konceptů</td><td>Rychlost — když potřebujete odpověď hned</td></tr>
<tr><td>Chcete si to vyzkoušet, než začnete platit</td><td>Nejvyšší kvalita u složitých úvah</td></tr>
</table>

<h2>Nejjednodušší cesta: v aplikaci</h2>
<ol class="kroky">
<li><p>Otevřete <strong>Nastavení → Poskytovatelé → Lokální modely</strong> (nabídne se to i při prvním
spuštění jako „Spouštět modely lokálně").</p></li>
<li><p>Klikněte na <strong>Nainstalovat běhové prostředí</strong>. Stáhne se oficiální běhové prostředí
pro váš hardware (pár set megabajtů), ověří se a bude se udržovat aktuální.</p></li>
<li><p>Vyberte model z katalogu a klikněte na <strong>Stáhnout</strong>. U každého modelu předem vidíte,
zda se vejde do paměti vaší karty (zelená), poběží přes operační paměť (oranžová), nebo je na váš
stroj velký (červená).</p></li>
<li><p>Klikněte na <strong>Použít</strong>. Nové rozhovory běží na lokálním modelu. Návrat k modelu
v cloudu je jedno kliknutí ve výběru modelu.</p></li>
</ol>
<p class="note">Stahování se dá pozastavit a zase pustit — i po zavření aplikace zůstane
rozdělané. Velké modely mají desítky gigabajtů, takže to na pomalém připojení chvíli trvá.</p>

<h2>Když používáte Ollamu nebo vlastní server</h2>
<p>Když už na počítači běží server (Ollama, vlastní llama-server, MLX), Hermes si ho najde a použije
místo vlastního. Dá se to i nastavit ručně — stačí uvést adresu serveru:</p>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
providers:
  ollama:
    base_url: http://127.0.0.1:11434/v1
    model: gemma3:12b        <span class="c"># název modelu, který má Ollama stažený</span></div>
<p>Volitelně se dá zapnout i spravované běhové prostředí a určit, na kterých portech se má hledat:</p>
<div class="code-block">local_runtime:
  enabled: true          <span class="c"># spustit spravovaný server spolu s Hermesem</span>
  backend: auto          <span class="c"># auto | cuda | metal | vulkan | hip | cpu</span>
  detect_ports: [8081]   <span class="c"># další porty, kde hledat vlastní llama-server</span></div>
<p class="note">Když server neběží, chyba to řekne přímo („lokální server modelu neběží") — nemusíte
luštit hlášky o chybějícím klíči.</p>

<h2>Co to potřebuje</h2>
<table class="wiki-tabulka">
<tr><th>Stroj</th><th>Co se použije</th></tr>
<tr><td>NVIDIA (Windows i Linux)</td><td>CUDA (na Linuxu s čipem ARM potřeba ovladač CUDA 13)</td></tr>
<tr><td>AMD a Intel</td><td>Vulkan; na vybraných strojích i HIP/ROCm</td></tr>
<tr><td>Mac</td><td>Metal</td></tr>
<tr><td>Bez karty</td><td>Procesor — funguje, ale pomalu</td></tr>
</table>
<table class="wiki-tabulka">
<tr><th>Paměť karty</th><th>Co se na ni vejde</th></tr>
<tr><td>8 GB a více</td><td>Menší modely z katalogu pohodlně</td></tr>
<tr><td>16 GB a více</td><td>Modely velikosti 27–35 miliard parametrů v dobré kvalitě</td></tr>
</table>

<h2>Jak se Hermes stará o paměť</h2>
<table class="wiki-tabulka">
<tr><th>Co dělá</th><th>Co to znamená pro vás</th></tr>
<tr><td>Začne s oknem, které se vejde do karty, a postupně ho zvětšuje</td><td>V přehledu se objeví „okno kontextu narostlo" — to je správně, není to chyba</td></tr>
<tr><td>Doporučený model má vždy aspoň 64 tisíc znaků kontextu</td><td>Udrží se rozumně dlouhý rozhovor</td></tr>
<tr><td>Co se nevejde do karty, umístí do operační paměti tak, aby to bolelo co nejméně</td><td>Pomalejší odpovědi, ale rozhovor nespadne</td></tr>
<tr><td>Počítá i s režijní pamětí (kontext, buffery, obrázkový adaptér)</td><td>Do karty se vejde méně, než kolik má soubor modelu — s tím Hermes počítá za vás</td></tr>
<tr><td>Když se okno zvětšit nedá, rozhovor se zkrátí</td><td>Místo tichého spadnutí se starší část rozhovoru shrne</td></tr>
</table>

<h2>Další modely a vlastní soubory</h2>
<table class="wiki-tabulka">
<tr><th>Kde</th><th>Co tam je</th></tr>
<tr><td>Katalog v aplikaci</td><td>Vybrané modely s ověřením, že fungují</td></tr>
<tr><td>Vyhledávání na Hugging Face</td><td>Mnohem širší nabídka; u každého výsledku je vidět, zda se vejde do vaší karty. Ověření od nás ale nemá</td></tr>
<tr><td>Vlastní soubor <code>.gguf</code></td><td>Dá se přidat do knihovny <strong>bez kopírování</strong> — soubor zůstane, kde je</td></tr>
</table>

<h2>Cena: doma versus v cloudu</h2>
<table class="wiki-tabulka">
<tr><th></th><th>Lokálně</th><th>Cloud (poskytovatel modelu)</th></tr>
<tr><td>Platba za dotazy</td><td>žádná</td><td>podle počtu znaků</td></tr>
<tr><td>Vstupní náklad</td><td>grafická karta a elektřina</td><td>žádný</td></tr>
<tr><td>Odesílání dat</td><td>nic neodchází</td><td>text jde k poskytovateli</td></tr>
<tr><td>Rychlost a kvalita</td><td>nižší</td><td>vyšší</td></tr>
<tr><td>Limity použití</td><td>žádné</td><td>podle tarifu, občas zpomalení ve špičce</td></tr>
</table>

<h2>Pasti z našeho provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co se stalo</th><th>Co s tím</th></tr>
<tr><td><strong>Agent běžel na serveru bez grafické karty</strong></td><td>Model poběží na procesoru, ale tak pomalu, že se to nedá používat. Lokální model patří na počítač s kartou, ne na server</td></tr>
<tr><td><strong>Malý model nezvládl nástroje</strong></td><td>Nepoužil je, nebo si vymyslel výsledek. Na práci s nástroji (soubory, příkazy, weby) berte větší model nebo cloud</td></tr>
<tr><td><strong>Model se do karty nevešel, i když soubor byl menší</strong></td><td>Do paměti patří i kontext a režijní buffery. Řiďte se barvou v katalogu, ne velikostí souboru</td></tr>
<tr><td><strong>Stahování velkého modelu zablokovalo připojení na celý den</strong></td><td>Použijte pozastavení a stahujte mimo pracovní dobu; stahuje se i obrázkový adaptér a další soubory</td></tr>
<tr><td><strong>Do paměti se nevešel delší rozhovor</strong></td><td>To je normální — Hermes rozhovor radši zkrátí, než aby spadl. Když to vadí, zvolte menší model, nebo si nechte dlouhé rozhovory v cloudu</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Začněte v aplikaci, ne v příkazové řádce</td><td>Uvidíte předem, co se do vašeho stroje vejde</td></tr>
<tr><td>Nechte si lokální model jako záložní cestu</td><td>Když nejde internet nebo dojdou peníze za cloud, agent pořád funguje</td></tr>
<tr><td>Na citlivé věci lokální model, na složité cloudový</td><td>Kombinace je nejlepší z obojího; mezi modely přepínáte jedním kliknutím</td></tr>
<tr><td>Než model stáhnete, všimněte si barvy u katalogu</td><td>Ušetříte desítky gigabajtů stažených zbytečně</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/vyber-modelu/"><strong>Výběr AI modelu</strong><span>Který model na co a kolik stojí</span></a>
<a href="/wiki/zaciname/prvni-chat/"><strong>Nastavení agenta</strong><span>První rozhovor s agentem</span></a>
<a href="/wiki/funkce/nastroje/"><strong>Nástroje a toolsety</strong><span>Co agent umí a jak to ověřit</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/local-models" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Lokální modely do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Kdy se vyplatí
Soukromá data (nic neodchází) · práce bez internetu · opakované jednoduché úlohy (shrnutí, překlad,
vytěžení údajů, koncepty) · vyzkoušení bez placení.
Nevyplatí se: složitá mnohakroková práce s nástroji, dlouhé rozhovory a dokumenty, rychlost, špičková kvalita.

## V aplikaci
Nastavení -> Poskytovatelé -> Lokální modely -> Nainstalovat běhové prostředí -> vybrat model
z katalogu (barvy: vejde se do karty / poběží přes RAM / je moc velký) -> Stáhnout -> Použít.
Návrat do cloudu jedním kliknutím. Stahování lze pozastavit a obnovit.
Z terminálu totéž: hermes model -> Local models.

## Ollama / vlastní server
Hermes najde běžící server sám a použije ho. Ručně:
providers:
  ollama:
    base_url: http://127.0.0.1:11434/v1
    model: gemma3:12b
local_runtime:
  enabled: true          # spravovaný server
  backend: auto          # auto|cuda|metal|vulkan|hip|cpu
  detect_ports: [8081]
Když server neběží, chyba to řekne přímo.

## Požadavky
NVIDIA -> CUDA (Linux ARM: ovladač CUDA 13), AMD/Intel -> Vulkan (i HIP/ROCm), Mac -> Metal, bez
karty -> procesor (pomalu). 8 GB+ paměti karty = menší modely; 16 GB+ = modely 27-35B.

## Správa paměti (za vás)
Okno začíná tak, aby se vešlo do karty, a roste ("okno kontextu narostlo" = správně). Doporučený model
má vždy aspoň 64K kontextu. Přetečení jde do operační paměti (pomalejší). Do výpočtu patří kontext,
buffery i obrázkový adaptér, ne jen soubor modelu. Když se okno zvětšit nedá, rozhovor se zkrátí.

## Další modely
Katalog (ověřené) · hledání na Hugging Face (u výsledku vidět, zda se vejde) · vlastní .gguf soubor
lze přidat bez kopírování.

## Cena
Lokálně: bez platby za dotazy, náklad = karta a elektřina, nic neodchází, nižší rychlost, žádné limity.
Cloud: platba za znaky, žádný vstupní náklad, text odchází, vyšší kvalita, limity tarifu.

## Pasti z našeho provozu
1. Server bez karty -> na procesoru nepoužitelně pomalé; lokální model patří na počítač s kartou.
2. Malý model nezvládl nástroje (nebo si vymyslel výsledek) -> větší model nebo cloud.
3. Model se nevešel, i když byl soubor menší -> rozhoduje barva v katalogu (kontext + buffery).
4. Velké stahování zablokovalo připojení -> pozastavit, stahovat mimo pracovní dobu.
5. Dlouhý rozhovor se nevešel -> Hermes ho zkrátí; menší model nebo dlouhé věci do cloudu.

## Tipy
Začít v aplikaci · lokální model jako záložní cesta · citlivé lokálně, složité v cloudu · všímat si
barvy u katalogu před stažením.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🏠</span><div><strong>A local model is like a bread maker at home: you own it, you pay nothing per loaf and nobody learns what you bake.</strong>
But it takes longer, and for a complicated cake you still go to the bakery. That is exactly how we
treat it — a local model for private and simple things, a large cloud model for everything else.</div></div>

<h2>When it pays off and when it does not</h2>
<table class="wiki-tabulka">
<tr><th>Pays off</th><th>Does not pay off</th></tr>
<tr><td>Data must not leave your computer (contracts, medical notes, internal code)</td><td>Complex multi-step work where the agent must use tools reliably</td></tr>
<tr><td>Working without internet, or on the move</td><td>Long conversations and long documents</td></tr>
<tr><td>Repeated simple jobs: summaries, translation, extracting facts, drafts</td><td>Speed — when you need the answer right now</td></tr>
<tr><td>Trying things out before you start paying</td><td>The highest quality on hard reasoning</td></tr>
</table>

<h2>The easiest way: inside the app</h2>
<ol class="kroky">
<li><p>Open <strong>Settings → Providers → Local Models</strong> (offered during onboarding as
"Run models locally" too).</p></li>
<li><p>Click <strong>Install runtime</strong>. The official runtime for your hardware is downloaded
(a few hundred MB), verified and kept up to date.</p></li>
<li><p>Pick a model from the catalog and click <strong>Download</strong>. Before you download
anything you can see whether it fits your GPU (green), runs via system memory (amber) or is too big
for this machine (red).</p></li>
<li><p>Click <strong>Use</strong>. New chats now run on the local model. Switching back to a cloud
provider is one click in the model picker.</p></li>
</ol>
<p class="note">Downloads can be paused and resumed — even after closing the app. Large models are
tens of gigabytes, so on a slow connection it takes a while.</p>

<h2>If you already run Ollama or your own server</h2>
<p>When a server is already running (Ollama, your own llama-server, MLX), Hermes finds it and uses it
instead of starting its own. You can also point it there by hand:</p>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
providers:
  ollama:
    base_url: http://127.0.0.1:11434/v1
    model: gemma3:12b        <span class="c"># the name of a model Ollama already has</span></div>
<p>The managed runtime can be enabled too, with extra ports to probe:</p>
<div class="code-block">local_runtime:
  enabled: true          <span class="c"># start the managed server together with Hermes</span>
  backend: auto          <span class="c"># auto | cuda | metal | vulkan | hip | cpu</span>
  detect_ports: [8081]   <span class="c"># further ports to probe for your own llama-server</span></div>
<p class="note">With no server reachable the error names the local runtime ("the local model server
isn't running") — no puzzling over a missing API key.</p>

<h2>What it needs</h2>
<table class="wiki-tabulka">
<tr><th>Machine</th><th>What gets used</th></tr>
<tr><td>NVIDIA (Windows and Linux)</td><td>CUDA (on Linux ARM a CUDA 13 driver is required)</td></tr>
<tr><td>AMD and Intel</td><td>Vulkan; HIP/ROCm on supported targets</td></tr>
<tr><td>Mac</td><td>Metal</td></tr>
<tr><td>No GPU</td><td>The CPU — it works, but slowly</td></tr>
</table>
<table class="wiki-tabulka">
<tr><th>GPU memory</th><th>What fits</th></tr>
<tr><td>8 GB and up</td><td>The smaller catalog models comfortably</td></tr>
<tr><td>16 GB and up</td><td>27–35B models at high quality</td></tr>
</table>

<h2>How Hermes manages memory</h2>
<table class="wiki-tabulka">
<tr><th>What it does</th><th>What it means for you</th></tr>
<tr><td>Starts with a window that fits the GPU and grows it as needed</td><td>You may see "context window grown" — that is correct, not an error</td></tr>
<tr><td>Every recommended model gets at least a 64K context window</td><td>A reasonably long conversation fits</td></tr>
<tr><td>Overflow goes to system memory in the least harmful order</td><td>Slower answers, but the conversation survives</td></tr>
<tr><td>It counts overhead (context, buffers, vision projector)</td><td>Less fits in the GPU than the model file's size — Hermes accounts for that</td></tr>
<tr><td>When the window cannot grow, the conversation is compressed</td><td>Instead of failing silently, older parts get summarised</td></tr>
</table>

<h2>More models and your own files</h2>
<table class="wiki-tabulka">
<tr><th>Where</th><th>What is there</th></tr>
<tr><td>The app catalog</td><td>Curated models with our validation badge</td></tr>
<tr><td>Hugging Face search</td><td>Far more choice; each result shows whether it fits your GPU, but carries no validation badge</td></tr>
<tr><td>Your own <code>.gguf</code> file</td><td>Can be added to the library <strong>without copying</strong> — the file stays where it is</td></tr>
</table>

<h2>Cost: at home versus in the cloud</h2>
<table class="wiki-tabulka">
<tr><th></th><th>Local</th><th>Cloud (model provider)</th></tr>
<tr><td>Payment per query</td><td>none</td><td>by the number of characters</td></tr>
<tr><td>Up-front cost</td><td>a graphics card and electricity</td><td>none</td></tr>
<tr><td>Data leaving your machine</td><td>none</td><td>the text goes to the provider</td></tr>
<tr><td>Speed and quality</td><td>lower</td><td>higher</td></tr>
<tr><td>Usage limits</td><td>none</td><td>set by your plan, occasional slowdowns at peak</td></tr>
</table>

<h2>Pitfalls from our systems</h2>
<table class="wiki-tabulka">
<tr><th>What happened</th><th>What to do</th></tr>
<tr><td><strong>The agent ran on a server with no graphics card</strong></td><td>It runs on the CPU, but so slowly it is unusable. A local model belongs on a machine with a GPU, not on a server</td></tr>
<tr><td><strong>A small model could not handle tools</strong></td><td>It ignored them or invented the result. For tool work (files, commands, websites) use a larger model or the cloud</td></tr>
<tr><td><strong>The model did not fit even though the file was smaller</strong></td><td>Context and overhead count too. Go by the colour in the catalog, not the file size</td></tr>
<tr><td><strong>Downloading a large model saturated the connection for a day</strong></td><td>Use pause and download outside working hours; vision adapters and other files are downloaded as well</td></tr>
<tr><td><strong>A longer conversation no longer fit</strong></td><td>That is normal — Hermes shortens the conversation rather than crashing. If it bothers you, pick a smaller model or keep long sessions in the cloud</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Start inside the app, not on the command line</td><td>You see up front what fits your machine</td></tr>
<tr><td>Keep a local model as a fallback</td><td>With no internet or no cloud budget the agent still works</td></tr>
<tr><td>Local for sensitive things, cloud for hard ones</td><td>The combination gets the best of both; switching is one click</td></tr>
<tr><td>Check the colour next to a model before downloading</td><td>Saves tens of gigabytes downloaded for nothing</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/choosing-a-model/"><strong>Choosing an AI model</strong><span>Which model for what, and what it costs</span></a>
<a href="/en/wiki/getting-started/first-chat/"><strong>Setting up the agent</strong><span>The first conversation with the agent</span></a>
<a href="/en/wiki/features/tools/"><strong>Tools and toolsets</strong><span>What the agent can do and how to verify it</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/local-models" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Local models in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## When it pays off
Private data (nothing leaves) · working offline · repeated simple jobs (summaries, translation,
extracting facts, drafts) · trying things out for free.
It does not pay off for: complex multi-step tool work, long conversations and documents, speed,
top-quality reasoning.

## In the app
Settings -> Providers -> Local Models -> Install runtime -> pick a model from the catalog
(colours: fits GPU / runs via RAM / too big) -> Download -> Use.
Back to cloud in one click. Downloads can be paused and resumed.
From the terminal: hermes model -> Local models.

## Ollama / your own server
Hermes detects a running server and uses it. By hand:
providers:
  ollama:
    base_url: http://127.0.0.1:11434/v1
    model: gemma3:12b
local_runtime:
  enabled: true          # managed server
  backend: auto          # auto|cuda|metal|vulkan|hip|cpu
  detect_ports: [8081]
With no server reachable the error names the local runtime.

## Requirements
NVIDIA -> CUDA (Linux ARM: CUDA 13 driver), AMD/Intel -> Vulkan (and HIP/ROCm), Mac -> Metal, no GPU
-> CPU (slow). 8 GB+ GPU memory = smaller models; 16 GB+ = 27-35B models.

## Memory management (handled for you)
The window starts fitting the GPU and grows ("context window grown" is correct). Recommended models
always get at least 64K context. Overflow goes to system memory (slower). Overhead counts: context,
buffers, vision projector — not just the model file. When the window cannot grow, the conversation is
compressed.

## More models
Catalog (validated) · Hugging Face search (fit check per result) · your own .gguf can be linked
without copying.

## Cost
Local: no per-query payment, cost = GPU and electricity, nothing leaves, lower speed, no limits.
Cloud: payment per character, no up-front cost, text leaves, higher quality, plan limits.

## Pitfalls from our systems
1. Server with no GPU -> unusably slow on the CPU; a local model belongs on a GPU machine.
2. A small model mishandled tools (or invented results) -> larger model or the cloud.
3. Model did not fit though the file was smaller -> the catalog colour decides (context + buffers).
4. A large download saturated the connection -> pause it, download off-hours.
5. A long conversation no longer fit -> Hermes compresses it; smaller model or keep long sessions in the cloud.

## Tips
Start in the app · keep a local model as a fallback · sensitive locally, hard tasks in the cloud ·
mind the catalog colour before downloading.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(21)
    stranka = najdi(21)
    assert stranka and stranka["nazev"] == "Lokální modely"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Lokální modely — model, který běží u vás doma",
        "Kdy se lokální model vyplatí, jak ho nainstalovat v aplikaci, kolik potřebuje paměti, jak Hermes hlásí, co se do karty vejde, a proč malý model nezvládne nástroje.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Lokální modely",
        "Model, který běží na vašem počítači: zdarma, bez odesílání dat a pomalejší. Kdy se vyplatí, co potřebuje a na co si dát pozor.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Lokální modely — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Local models — a model that runs at home",
        "When a local model pays off, how to install it in the app, how much memory it needs, how Hermes reports what fits your GPU, and why a small model mishandles tools.",
        OBRAZEK, "Wiki · Features in depth", "Local models",
        "A model running on your own computer: free, nothing leaves the machine, and slower. When it pays off, what it needs and what to watch out for.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Local models — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
