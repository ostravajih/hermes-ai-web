#!/usr/bin/env python3
"""Postaví stránku wiki „Hlasový režim" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-voice-mode.md (interaktivní hlas v terminálu,
hlasová odpověď na Telegramu a Discordu, konfigurace, požadavky),
user-guide-features-tts.md (11 poskytovatelů hlasu, doručení na platformy, přepis).

Naše zkušenosti: agent na VPS nemá mikrofon, takže interaktivní hlas patří k počítači;
hlasové odpovědi v Telegramu jsou na mobil nejpohodlnější.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode"
OBRAZEK = "wiki-hlas"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🎙️</span><div><strong>Hlas se hodí tam, kde je psaní na obtíž — v autě, na procházce, u vaření.</strong>
Nadiktujete zadání a agent odpoví nahlas. Všechno ostatní (klíče, nástroje, paměť) zůstává
stejné jako u textu — hlas je jen jiný vstup a výstup.</div></div>

<h2>Co jde a kde</h2>
<table class="wiki-tabulka">
<tr><th>Způsob</th><th>Kde funguje</th><th>Jak se používá</th></tr>
<tr><td><strong>Mluvení do agenta</strong></td><td>Terminál na vašem počítači</td><td>Zapnete <code>/voice on</code>, nahrávání spustíte klávesou (výchozně <code>Ctrl+B</code>)</td></tr>
<tr><td><strong>Hlasová odpověď</strong></td><td>Telegram a Discord</td><td>Agent pošle odpověď jako hlasovou zprávu, kterou si pustíte v mobilu</td></tr>
<tr><td><strong>Hlasové zprávy od vás</strong></td><td>Telegram, Discord a další</td><td>Pošlete botovi hlasovku — přepíše se na text a agent odpoví</td></tr>
<tr><td><strong>Hlasové kanály</strong></td><td>Discord</td><td>Agent se připojí do hlasového kanálu a mluví s vámi</td></tr>
</table>

<h2>Jak to vypadá v praxi (terminál)</h2>
<ol class="kroky">
<li><p>Zapněte hlasový režim — stav si můžete kdykoli vypsat:</p>
<div class="code-block"><span class="p">❯</span> /voice on
<span class="p">❯</span> /voice status</div></li>
<li><p>Stiskněte klávesu pro nahrávání (výchozně <code>Ctrl+B</code>). Ozve se pípnutí a začne nahrávání.</p></li>
<li><p>Mluvte. Uvidíte ukazatel hlasitosti, ať víte, že vás agent slyší.</p></li>
<li><p>Přestaňte mluvit. Po chvíli ticha (výchozně 3 vteřiny) se nahrávání <strong>samo</strong> ukončí
a ozvou se dvě pípnutí.</p></li>
<li><p>Text se přepíše a pošle agentovi. Když je zapnutý hlasový výstup, odpověď uslyšíte nahlas
a nahrávání se rovnou rozjede znovu — můžete mluvit dál bez mačkání kláves.</p></li>
</ol>
<p class="note">Řeknete-li přesně slovo <em>„stop“</em> (dá se to změnit), hlasový rozhovor se ukončí.
Nahrávání má strop (výchozně 120 vteřin), aby se nezaseklo.</p>

<h2>Co si připravit</h2>
<table class="wiki-tabulka">
<tr><th>Co</th><th>Proč</th></tr>
<tr><td>Agent fungující v textu</td><td>Nejdřív musí odpovídat na psaní — pak má smysl řešit hlas</td></tr>
<tr><td>Poskytovatel modelu (klíč)</td><td>Hlas nic nepočítá sám, jen mění řeč na text a zpět</td></tr>
<tr><td>Zvukové vybavení na tom stroji, kde Hermes běží</td><td>Mikrofon a přehrávání pro interaktivní hlas</td></tr>
<tr><td>Doplněk pro hlas</td><td>Knihovny pro zvuk a přepis se nastavují přes <code>hermes tools</code>; v Dockeru je k dispozici jen vybraná část a doinstalování je zakázané</td></tr>
</table>
<p class="note">Na Windows s čipem ARM a na Macích s procesorem Intel nejde místní přepis
(Faster-Whisper) — tam použijte přepis přes službu (Groq, OpenAI, Mistral…) nebo hlasové zprávy
v mobilu.</p>

<h2>Přepis řeči na text (co agent slyší)</h2>
<table class="wiki-tabulka">
<tr><th>Volba</th><th>Kdy se hodí</th></tr>
<tr><td><code>local</code> (výchozí, zdarma)</td><td>Běží u vás, nic se neposílá ven; náročnější na výkon</td></tr>
<tr><td>Groq, OpenAI, Mistral, xAI, ElevenLabs, DeepInfra</td><td>Rychle a přesně i na slabším stroji, platí se za použití nebo je v rámci tarifu</td></tr>
<tr><td>Vypnutý přepis (<code>stt.enabled: false</code>)</td><td>Když chcete nahrávku zpracovat po svém — agentovi se místo textu předá cesta k souboru</td></tr>
</table>
<p>Kvalitu přepisu ovlivní i zvolený model — od nejmenšího (<code>tiny</code>) po největší
(<code>large-v3</code>) nebo <code>turbo</code> jako rozumný kompromis:</p>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
stt:
  provider: "local"
  local:
    model: "turbo"
    language: "cs"        <span class="c"># když necháte prázdné, pozná jazyk sám</span></div>

<h2>Hlas, kterým agent mluví (TTS)</h2>
<table class="wiki-tabulka">
<tr><th>Volba</th><th>Cena</th><th>Poznámka</th></tr>
<tr><td><strong>Edge TTS</strong> (výchozí)</td><td>zdarma</td><td>Nepotřebuje žádný klíč; 322 hlasů ve 74 jazycích</td></tr>
<tr><td>Placené služby (ElevenLabs, OpenAI, MiniMax, Mistral, Gemini, xAI, DeepInfra)</td><td>placené / s tarifem</td><td>Nejlepší zvuk; každá má vlastní klíč</td></tr>
<tr><td>Lokální (NeuTTS, KittenTTS, Piper)</td><td>zdarma</td><td>Běží u vás, nic neodesílá; některé si při prvním použití stáhnou model</td></tr>
</table>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
tts:
  provider: "edge"
  speed: 1.0
  edge:
    voice: "en-US-AriaNeural"     <span class="c"># hlas se vybírá podle názvu, české začínají cs-CZ</span></div>
<p class="note">Hlas si vždycky <strong>poslechněte</strong>, než ho necháte nastavený natrvalo —
přepis a výslovnost se u jednotlivých hlasů dost liší.</p>

<h2>Kde hlas uslyšíte (a kde ho najdete)</h2>
<table class="wiki-tabulka">
<tr><th>Kde</th><th>Podoba</th></tr>
<tr><td>Telegram</td><td>Hlasová zpráva, kterou si pustíte přímo v chatu</td></tr>
<tr><td>Discord</td><td>Hlasová zpráva nebo příloha</td></tr>
<tr><td>WhatsApp</td><td>Zvuková příloha</td></tr>
<tr><td>Terminál</td><td>Přehrávání u vás; soubory zůstávají v <code>~/.hermes/audio_cache/</code></td></tr>
</table>

<h2>Pasti z našeho provozu</h2>
<table class="wiki-tabulka">
<tr><th>Co se stalo</th><th>Co s tím</th></tr>
<tr><td><strong>Agent běžel na serveru bez zvukové karty</strong></td><td>Interaktivní hlas (mikrofon u serveru) nemá smysl. Používejte hlasové zprávy v Telegramu — agenta to nechá na serveru a vy mluvíte z mobilu</td></tr>
<tr><td><strong>Hlasová odpověď chodila i k věcem, které se čtou lépe</strong></td><td>Hlasový výstup se dá vypnout (<code>/voice tts</code>), nebo ho zapínat jen když se hodí; výchozí stav je vypnutý</td></tr>
<tr><td><strong>Přepis česky dělal chyby ve jménech a číslech</strong></td><td>Nastavte jazyk přepisu napevno (<code>language: cs</code>) a u důležitých věcí (čísla, adresy) si je nechte potvrdit v textu</td></tr>
<tr><td><strong>Placené hlasy začaly utrácet, aniž jsme to čekali</strong></td><td>Hlasová odpověď = platba za každou odpověď. Výchozí Edge je zdarma; placený hlas zapínejte vědomě</td></tr>
<tr><td><strong>„Neslyší mě“</strong></td><td>Zkontrolujte, že běží na počítači s mikrofonem (ne v kontejneru na serveru), že je vybrané správné vstupní zařízení a že agent předtím fungoval v textu</td></tr>
</table>

<h2>Naše tipy</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Proč</th></tr>
<tr><td>Hlas používejte na diktování zadání, ne na čtení dlouhých odpovědí</td><td>Poslouchat seznam deseti bodů je otrava, nadiktovat úkol je úleva</td></tr>
<tr><td>Nechte si odpovídat krátce</td><td>Do nastavení osobnosti (SOUL.md) napište, že hlasové odpovědi mají být stručné</td></tr>
<tr><td>U hlasových zpráv v Telegramu zkontrolujte oprávnění</td><td>Agent má odpovídat jen vám — viz <a href="/wiki/zaciname/telegram-a-discord/">Telegram a Discord</a></td></tr>
<tr><td>Než hlas zapnete, zkuste agenta v textu</td><td>Ušetříte si hledání problému ve dvou věcech najednou</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/telegram-a-discord/"><strong>Telegram a Discord</strong><span>Agent, který odpovídá na mobilu</span></a>
<a href="/wiki/funkce/lokalni-modely/"><strong>Lokální modely</strong><span>Když má všechno běžet u vás doma</span></a>
<a href="/wiki/funkce/kontextove-soubory/"><strong>Kontextové soubory</strong><span>Jak agentovi určit styl a délku odpovědí</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Hlasový režim do detailu (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Co umí hlas
Mluvení do agenta (terminál na vašem počítači, /voice on + Ctrl+B) · hlasová odpověď
(Telegram, Discord) · hlasové zprávy od vás (přepis na text) · hlasové kanály (Discord).

## Průběh v terminálu
/voice on -> Ctrl+B -> pípnutí -> mluvíte (ukazatel hlasitosti) -> 3 s ticha = konec (dvě pípnutí)
-> přepis (Whisper) -> odpověď, případně nahlas -> nahrávání se rozjede znovu.
Slovo "stop" (nastavitelné) ukončí hlasový rozhovor; nahrávání má strop 120 s.

## Co si připravit
Fungující agent v textu · klíč k modelu · mikrofon a přehrávání na stroji, kde Hermes běží ·
doplněk pro hlas (hermes tools); v Dockeru jen vybraná část bez doinstalování.
Windows ARM64 a Intel macOS: místní přepis nejde, použít cloud nebo hlasovky v mobilu.

## Přepis (STT)
local (zdarma, Faster-Whisper) | groq | openai | mistral | xai | elevenlabs | deepinfra.
stt.enabled: false -> agentovi se předá cesta k nahrávce místo textu.
Modely tiny/base/small/medium/large-v3/turbo; language: cs pro pevný jazyk.

## Hlas (TTS)
Edge (výchozí, zdarma, 322 hlasů / 74 jazyků) · placené (ElevenLabs, OpenAI, MiniMax, Mistral,
Gemini, xAI, DeepInfra) · lokální zdarma (NeuTTS, KittenTTS, Piper).
Nastavení: tts.provider, tts.speed, např. tts.edge.voice.
Doručení: Telegram hlasová zpráva · Discord zpráva/příloha · WhatsApp příloha · terminál
přehrávání + soubory v ~/.hermes/audio_cache/.

## Pasti z našeho provozu
1. Agent na serveru bez zvukové karty -> interaktivní hlas nemá smysl; použít hlasovky v Telegramu.
2. Hlasový výstup u textových věcí -> vypnout /voice tts, výchozí je vypnutý.
3. Chyby v přepisu jmen a čísel -> language: cs a důležité údaje si nechat potvrdit v textu.
4. Placené hlasy platí za každou odpověď -> výchozí Edge je zdarma.
5. "Neslyší mě" -> běží na počítači s mikrofonem? správné vstupní zařízení? funguje text?

## Tipy
Hlas na diktování zadání, ne na poslech dlouhých odpovědí · v SOUL.md nastavit stručné odpovědi ·
zkontrolovat, kdo smí botovi psát · nejdřív rozchodit text.
"""

# ============================================================== ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🎙️</span><div><strong>Voice pays off where typing is awkward — in the car, on a walk, while cooking.</strong>
You dictate the task and the agent answers out loud. Everything else (keys, tools, memory) stays
exactly as it is for text — voice is only a different input and output.</div></div>

<h2>What works and where</h2>
<table class="wiki-tabulka">
<tr><th>Way</th><th>Where it works</th><th>How you use it</th></tr>
<tr><td><strong>Talking to the agent</strong></td><td>The terminal on your computer</td><td>Enable <code>/voice on</code>, start recording with a key (default <code>Ctrl+B</code>)</td></tr>
<tr><td><strong>Spoken replies</strong></td><td>Telegram and Discord</td><td>The agent sends its answer as a voice message you play on your phone</td></tr>
<tr><td><strong>Voice messages from you</strong></td><td>Telegram, Discord and more</td><td>Send the bot a voice note — it is transcribed and the agent answers</td></tr>
<tr><td><strong>Voice channels</strong></td><td>Discord</td><td>The agent joins a voice channel and talks with you</td></tr>
</table>

<h2>What it looks like in practice (terminal)</h2>
<ol class="kroky">
<li><p>Switch voice mode on — you can check the state any time:</p>
<div class="code-block"><span class="p">❯</span> /voice on
<span class="p">❯</span> /voice status</div></li>
<li><p>Press the recording key (default <code>Ctrl+B</code>). A beep plays and recording starts.</p></li>
<li><p>Speak. A level bar shows that the agent can hear you.</p></li>
<li><p>Stop speaking. After a moment of silence (3 seconds by default) recording ends
<strong>by itself</strong> and two beeps confirm it.</p></li>
<li><p>The audio is transcribed and sent to the agent. With spoken output enabled you hear the
answer and recording restarts immediately — keep talking without pressing anything.</p></li>
</ol>
<p class="note">Say exactly the word <em>"stop"</em> (configurable) and the voice conversation ends.
Recording also has a ceiling (120 seconds by default) so it cannot get stuck.</p>

<h2>What to prepare</h2>
<table class="wiki-tabulka">
<tr><th>What</th><th>Why</th></tr>
<tr><td>An agent that works in text</td><td>It must answer typed messages first — only then does voice make sense</td></tr>
<tr><td>A model provider (key)</td><td>Voice computes nothing itself, it only turns speech into text and back</td></tr>
<tr><td>Audio on the machine running Hermes</td><td>A microphone and playback for interactive voice</td></tr>
<tr><td>The voice extra</td><td>Audio and transcription libraries are configured through <code>hermes tools</code>; in Docker only a curated subset is available and on-demand installs are disabled</td></tr>
</table>
<p class="note">On Windows ARM64 and Intel Macs local transcription (Faster-Whisper) is not
available — use a cloud provider (Groq, OpenAI, Mistral…) or voice messages from your phone.</p>

<h2>Speech to text (what the agent hears)</h2>
<table class="wiki-tabulka">
<tr><th>Option</th><th>When it fits</th></tr>
<tr><td><code>local</code> (default, free)</td><td>Runs on your machine, nothing leaves it; heavier on hardware</td></tr>
<tr><td>Groq, OpenAI, Mistral, xAI, ElevenLabs, DeepInfra</td><td>Fast and accurate even on a modest machine, billed per use or included in a plan</td></tr>
<tr><td>Transcription off (<code>stt.enabled: false</code>)</td><td>When you want to process the recording yourself — the agent gets a file path instead of text</td></tr>
</table>
<p>Model size affects accuracy — from the smallest (<code>tiny</code>) to the largest
(<code>large-v3</code>), with <code>turbo</code> as a good compromise:</p>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
stt:
  provider: "local"
  local:
    model: "turbo"
    language: "en"        <span class="c"># leave blank to detect the language automatically</span></div>

<h2>The voice the agent speaks with (TTS)</h2>
<table class="wiki-tabulka">
<tr><th>Option</th><th>Cost</th><th>Note</th></tr>
<tr><td><strong>Edge TTS</strong> (default)</td><td>free</td><td>No key needed; 322 voices across 74 languages</td></tr>
<tr><td>Paid services (ElevenLabs, OpenAI, MiniMax, Mistral, Gemini, xAI, DeepInfra)</td><td>paid / plan</td><td>Best sound; each needs its own key</td></tr>
<tr><td>Local (NeuTTS, KittenTTS, Piper)</td><td>free</td><td>Runs on your machine, sends nothing out; some download a model on first use</td></tr>
</table>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
tts:
  provider: "edge"
  speed: 1.0
  edge:
    voice: "en-US-AriaNeural"     <span class="c"># pick by name; Czech voices start with cs-CZ</span></div>
<p class="note">Always <strong>listen</strong> to a voice before keeping it — pronunciation varies a
lot between them.</p>

<h2>Where you hear it (and find it)</h2>
<table class="wiki-tabulka">
<tr><th>Where</th><th>Shape</th></tr>
<tr><td>Telegram</td><td>A voice message you play in the chat</td></tr>
<tr><td>Discord</td><td>A voice message or an attachment</td></tr>
<tr><td>WhatsApp</td><td>An audio attachment</td></tr>
<tr><td>Terminal</td><td>Played locally; files stay in <code>~/.hermes/audio_cache/</code></td></tr>
</table>

<h2>Pitfalls from our systems</h2>
<table class="wiki-tabulka">
<tr><th>What happened</th><th>What to do</th></tr>
<tr><td><strong>The agent ran on a server with no sound card</strong></td><td>Interactive voice (a microphone at the server) makes no sense. Use voice messages in Telegram — the agent stays on the server and you speak from your phone</td></tr>
<tr><td><strong>Spoken replies arrived for things better read</strong></td><td>Spoken output can be switched off (<code>/voice tts</code>) or enabled only when it helps; it is off by default</td></tr>
<tr><td><strong>Transcription got names and numbers wrong</strong></td><td>Pin the transcription language (<code>language: cs</code>) and have important details (numbers, addresses) confirmed in writing</td></tr>
<tr><td><strong>Paid voices started spending without us noticing</strong></td><td>Spoken answers are billed per reply. The default Edge voice is free; enable a paid one deliberately</td></tr>
<tr><td><strong>"It cannot hear me"</strong></td><td>Check that it runs on a computer with a microphone (not in a container on a server), that the right input device is selected and that the agent worked in text first</td></tr>
</table>

<h2>Our tips</h2>
<table class="wiki-tabulka">
<tr><th>Tip</th><th>Why</th></tr>
<tr><td>Use voice to dictate tasks, not to listen to long answers</td><td>Listening to a ten-point list is a chore; dictating a task is a relief</td></tr>
<tr><td>Ask for short spoken answers</td><td>Put it into the personality file (SOUL.md) that spoken replies must be brief</td></tr>
<tr><td>Check permissions for voice messages on Telegram</td><td>Only you should be able to talk to the bot — see <a href="/en/wiki/getting-started/telegram-and-discord/">Telegram and Discord</a></td></tr>
<tr><td>Get the agent working in text before enabling voice</td><td>You avoid chasing a problem in two things at once</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/telegram-and-discord/"><strong>Telegram and Discord</strong><span>An agent that answers on your phone</span></a>
<a href="/en/wiki/features/local-models/"><strong>Local models</strong><span>When everything should run at home</span></a>
<a href="/en/wiki/features/context-files/"><strong>Context files</strong><span>Telling the agent your style and answer length</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode" target="_blank" rel="noopener"><strong>Official documentation</strong><span>Voice mode in detail</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## What voice can do
Talking to the agent (terminal on your computer, /voice on + Ctrl+B) · spoken replies
(Telegram, Discord) · voice messages from you (transcribed) · voice channels (Discord).

## The terminal loop
/voice on -> Ctrl+B -> beep -> speak (level bar) -> 3 s of silence ends it (two beeps)
-> transcription (Whisper) -> answer, spoken if enabled -> recording restarts.
The word "stop" (configurable) ends the voice conversation; recording caps at 120 s.

## What to prepare
An agent that works in text · a model key · microphone and playback on the machine running Hermes ·
the voice extra (hermes tools); Docker ships a subset with installs disabled.
Windows ARM64 and Intel macOS: no local transcription — use cloud STT or phone voice notes.

## Transcription (STT)
local (free, Faster-Whisper) | groq | openai | mistral | xai | elevenlabs | deepinfra.
stt.enabled: false -> the agent receives a file path instead of text.
Models tiny/base/small/medium/large-v3/turbo; language: cs to pin the language.

## Spoken output (TTS)
Edge (default, free, 322 voices / 74 languages) · paid (ElevenLabs, OpenAI, MiniMax, Mistral,
Gemini, xAI, DeepInfra) · free local (NeuTTS, KittenTTS, Piper).
Settings: tts.provider, tts.speed, e.g. tts.edge.voice.
Delivery: Telegram voice message · Discord message/attachment · WhatsApp attachment · terminal
playback plus files in ~/.hermes/audio_cache/.

## Pitfalls from our systems
1. Agent on a server with no sound card -> interactive voice is pointless; use Telegram voice notes.
2. Spoken output for things better read -> switch off with /voice tts; off by default.
3. Transcription errors on names and numbers -> pin language and confirm important details in text.
4. Paid voices bill every reply -> Edge is free by default.
5. "It cannot hear me" -> a machine with a microphone? right input device? does text work first?

## Tips
Dictate tasks rather than listen to long answers · set brief spoken replies in SOUL.md · check who
may message the bot · get text working first.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(19)
    stranka = najdi(19)
    assert stranka and stranka["nazev"] == "Hlasový režim"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Hlasový režim — mluvit s agentem a poslouchat odpovědi",
        "Jak zapnout hlas v terminálu, nechat si odpovídat nahlas v Telegramu, vybrat přepis a hlas, kolik to stojí a na co si dát pozor na serveru bez mikrofonu.",
        OBRAZEK, "Wiki · Funkce do hloubky", "Hlasový režim",
        "Nadiktujete zadání a agent odpoví nahlas. Kde hlas funguje, co si připravit, jak vybrat hlas a jak se vyhnout zbytečným platbám.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Hlasový režim — česká wiki", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Voice mode — talking to the agent and hearing answers",
        "How to enable voice in the terminal, get spoken replies in Telegram, choose transcription and a voice, what it costs and what to watch on a server with no microphone.",
        OBRAZEK, "Wiki · Features in depth", "Voice mode",
        "Dictate the task and the agent answers out loud. Where voice works, what to prepare, how to choose a voice and how to avoid needless spending.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Voice mode — community wiki", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
