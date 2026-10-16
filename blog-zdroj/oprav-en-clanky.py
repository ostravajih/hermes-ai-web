#!/usr/bin/env python3
"""Doplní anglické články na blogu — přeloží českou předlohu do angličtiny.

Anglické články vznikly jako torza (jen nadpis a pár řádků), některé měly
i český nadpis nebo perex. Tento nástroj vezme český originál a nahradí tělo
anglického článku skutečným překladem — stejné nadpisy, odstavce, seznamy
i bloky s příkazy. Datum a doba čtení se přebírají z české předlohy.

Spuštění:  python3 blog-zdroj/oprav-en-clanky.py
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

WEB = Path("/var/www/hermesagent")
MESICE = {"ledna": "January", "února": "February", "března": "March", "dubna": "April",
          "května": "May", "června": "June", "července": "July", "srpna": "August",
          "září": "September", "října": "October", "listopadu": "November", "prosince": "December"}


def datum_en(cz_cesta: Path) -> str:
    """Z české předlohy udělá anglické datum a dobu čtení (10 July 2026 · 2 min read)."""
    t = cz_cesta.read_text(encoding="utf-8")
    m = re.search(r'margin-bottom:32px">\s*(\d+)\.\s*([a-zá-ž]+)\s*(\d{4})\s*·\s*([^<]*)<', t)
    if not m:
        return ""
    den, mesic, rok, cas = m.group(1), m.group(2), m.group(3), m.group(4)
    # doba čtení bývá „2 min“, „4 minuty“ i „Doba čtení: 5 minut“
    minuty = re.search(r'(\d+)\s*(?:min|minut|minuty)', cas)
    mesic_en = MESICE.get(mesic, mesic)
    return f"{den} {mesic_en} {rok} · {minuty.group(1) if minuty else '3'} min read"


def oprav(slug_cz: str, slug_en: str, h1_en: str, telo_en: str,
          titulek: str | None = None, popis: str | None = None,
          alt: str | None = None) -> None:
    """Nahradí tělo anglického článku překladem (obrázek zůstává)."""
    en = WEB / "en" / "blog" / "clanek" / slug_en / "index.html"
    cz = WEB / "blog" / "clanek" / slug_cz / "index.html"
    if not en.exists():
        print(f"  ⚠ chybí {en.relative_to(WEB)}"); return
    t = en.read_text(encoding="utf-8")

    # 1) nadpis
    t = re.sub(r'<h1>.*?</h1>', f'<h1>{h1_en}</h1>', t, count=1, flags=re.S)
    # 2) datum a doba čtení podle české předlohy
    d = datum_en(cz)
    if d:
        t = re.sub(r'(margin-bottom:32px">)[^<]*(</p>)', rf'\g<1>{d}\g<2>', t, count=1)
    # 3) tělo — obrázek zůstává, zbytek se nahradí
    fig = re.search(r'<figure class="article-illustration">.*?</figure>', t, re.S)
    figura = fig.group(0) if fig else ""
    novy = f'<div class="article">{figura}\n{telo_en.strip()}\n\\g<1>'
    t, n = re.subn(r'<div class="article">.*?(</div>\s*<p style="text-align:center;margin-top:40px">)',
                   novy, t, count=1, flags=re.S)
    # 4) titulek a popisek pro vyhledávače
    if titulek:
        stary_t = re.search(r'<title>([^<]*)</title>', t)
        if stary_t:
            t = t.replace(f'<title>{stary_t.group(1)}</title>', f'<title>{titulek}</title>')
        t = re.sub(r'(property="og:title" content=")[^"]*(")', rf'\g<1>{titulek}\g<2>', t)
    if popis:
        t = re.sub(r'(name="description" content=")[^"]*(")', rf'\g<1>{popis}\g<2>', t)
        t = re.sub(r'(property="og:description" content=")[^"]*(")', rf'\g<1>{popis}\g<2>', t)
    if alt:
        t = re.sub(r'(<img[^>]*\balt=")[^"]*(")', rf'\g<1>{alt}\g<2>', t)
        t = re.sub(r'(property="og:image:alt" content=")[^"]*(")', rf'\g<1>{alt}\g<2>', t)
    en.write_text(t, encoding="utf-8")
    print(f"  ✅ {slug_en}: tělo přeloženo ({len(telo_en)} znaků, {n} náhrada)")


# ============================================================ DÁVKA 1
MACOS = """
<p>Hermes Agent runs natively on macOS — on <strong>Apple Silicon (M1/M2/M3/M4)</strong> and Intel alike. Installation takes a minute, and the desktop app gives you a full graphical interface.</p>
<h2>Quick install (shell script)</h2>
<div class="code-block"><span class="prompt">$</span> curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash</div>
<p>The installer sets up Python 3.11, Node.js, ripgrep, ffmpeg and every dependency for you.</p>
<h2>Alternative install through Homebrew</h2>
<div class="code-block">
<span class="c"># If you don't have Homebrew yet:</span>
<span class="prompt">$</span> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
<span class="c"># Install Hermes Agent</span>
<span class="prompt">$</span> brew install hermes-agent
</div>
<h2>Configuration after install</h2>
<div class="code-block">
<span class="prompt">$</span> source ~/.zshrc   <span class="c"># or: source ~/.bashrc</span>
<span class="prompt">$</span> hermes setup      <span class="c"># setup wizard (model, provider, API key)</span>
<span class="prompt">$</span> hermes            <span class="c"># start it in the terminal</span>
</div>
<h2>The desktop app</h2>
<p>Hermes has a native Electron desktop app for macOS:</p>
<div class="code-block"><span class="prompt">$</span> hermes desktop</div>
<p>What the desktop app brings:</p>
<ul>
<li><strong>Streaming chat</strong> — answers show up in real time</li>
<li><strong>Drag &amp; drop files</strong> — drop in images, PDFs or code</li>
<li><strong>Cmd+K palette</strong> — quick commands, like in VS Code</li>
<li><strong>Session list</strong> — every conversation in one place</li>
<li><strong>Native notifications</strong> — a ping when the agent finishes a task</li>
<li><strong>Live subagent watch-windows</strong> — follow agents running in parallel</li>
<li><strong>Model switching</strong> — pick a provider straight from the UI</li>
</ul>
<h2>Apple Silicon: the advantage for AI</h2>
<p>Macs with M1–M4 chips share one pool of memory (unified memory) between the CPU and the GPU. That means:</p>
<ul>
<li>A 16 GB MacBook Air can run local LLMs up to roughly 13B parameters</li>
<li>Ollama uses Metal (GPU acceleration) automatically on a Mac — models run far faster than on an Intel Mac</li>
<li>No external GPU is needed</li>
</ul>
<h2>Running a local LLM on macOS</h2>
<div class="code-block">
<span class="c"># Install Ollama</span>
<span class="prompt">$</span> brew install ollama
<span class="c"># Start the Ollama service in the background</span>
<span class="prompt">$</span> brew services start ollama
<span class="c"># Download a model</span>
<span class="prompt">$</span> ollama pull llama3.1
<span class="c"># In Hermes: Custom provider → http://localhost:11434/v1</span>
</div>
<h2>Living with macOS</h2>
<ul>
<li>Terminal.app / iTerm2 / Warp: Hermes works in any terminal</li>
<li>Spotlight: set up an alias for a quick start</li>
<li>Menu bar: the desktop app minimises into the menu bar</li>
<li>Touch ID: you can approve sudo commands with Touch ID</li>
</ul>
<h2>Troubleshooting on macOS</h2>
<h3>"hermes: command not found"</h3>
<p>The installer adds Hermes to your PATH. If it still does not work, add it by hand: <code>export PATH="$HOME/.local/bin:$PATH" &gt;&gt; ~/.zshrc</code></p>
<h3>Gatekeeper blocks the app</h3>
<p>macOS can block unsigned apps. On the first run of <code>hermes desktop</code>, go to System Settings → Privacy &amp; Security → Allow Anyway.</p>
<h3>Ollama does not see the GPU</h3>
<p>On Apple Silicon GPU acceleration is automatic. Check it with <code>ollama run llama3.1 --verbose</code> and make sure the output names "Metal" as the backend.</p>
"""

CRON = """
<p>Hermes Agent has a built-in cron scheduler — your agent can run tasks automatically around the clock, deliver the results to Telegram, Discord or email, and do it all without you being there.</p>
<h2>How the scheduler works</h2>
<p>The cron scheduler runs inside the Hermes gateway as a separate component. Every job has its own:</p>
<ul>
<li><strong>Schedule</strong> — a cron expression, an interval, or a one-off run</li>
<li><strong>Prompt</strong> — instructions for the agent (or <code>no_agent=true</code> for script-only jobs)</li>
<li><strong>Delivery</strong> — where the result goes (Telegram, Discord, email, …)</li>
<li><strong>Skill</strong> — optionally skills to load up front</li>
<li><strong>Script</strong> — optionally a script that runs before the agent (collecting data)</li>
</ul>
<h2>Creating a job</h2>
<div class="code-block">
<span class="c"># Every morning at 8:00 — a morning briefing</span>
<span class="prompt">$</span> /cron create "0 8 * * *" "Give me a morning briefing: weather, GitHub notifications, today's tasks"
<span class="c"># Every 2 hours — check pull requests</span>
<span class="prompt">$</span> /cron create "every 2h" "Check for new pull requests and issues on GitHub"
<span class="c"># Every Friday at 17:00 — a weekly report</span>
<span class="prompt">$</span> /cron create "0 17 * * 5" "Write a weekly activity report and send it by email"
<span class="c"># One-off — 1 August 2026 at 09:00</span>
<span class="prompt">$</span> /cron create "2026-08-01T09:00:00" "Send me a reminder: pay the invoice"
</div>
<h2>The cron expression format</h2>
<table><tr><th>Position</th><th>Meaning</th><th>Values</th></tr>
<tr><td>1</td><td>Minute</td><td>0–59</td></tr>
<tr><td>2</td><td>Hour</td><td>0–23</td></tr>
<tr><td>3</td><td>Day of month</td><td>1–31</td></tr>
<tr><td>4</td><td>Month</td><td>1–12</td></tr>
<tr><td>5</td><td>Day of week</td><td>0–7 (0 = Sunday)</td></tr></table>
<h2>Real examples worth copying</h2>
<h3>1. A morning briefing on Telegram</h3>
<div class="code-block">
<span class="c"># Every weekday at 7:30</span>
<span class="prompt">$</span> /cron create "30 7 * * 1-5" "Give me a morning overview:
- today's weather in Prague
- unread GitHub notifications
- new emails in the last 24 hours
- today's tasks from Todoist"
</div>
<h3>2. A server watchdog</h3>
<div class="code-block">
<span class="c"># Every 30 minutes</span>
<span class="prompt">$</span> /cron create "*/30 * * * *" "Check:
- CPU and RAM usage (alert if above 80%)
- free disk space (alert if below 10%)
- whether the website responds"
</div>
<h3>3. Automatic pull request review</h3>
<div class="code-block">
<span class="c"># Every hour during working hours</span>
<span class="prompt">$</span> /cron create "0 9-17 * * 1-5" "Check open pull requests in the repository. For each one:
- look at the diff for problems
- run the tests where possible
- write a review comment"
</div>
<h2>Managing jobs</h2>
<div class="code-block">
<span class="prompt">$</span> hermes cron list            <span class="c"># list every job</span>
<span class="prompt">$</span> hermes cron pause ID        <span class="c"># pause one</span>
<span class="prompt">$</span> hermes cron resume ID       <span class="c"># resume it</span>
<span class="prompt">$</span> hermes cron run ID          <span class="c"># run it right now</span>
<span class="prompt">$</span> hermes cron remove ID       <span class="c"># delete it</span>
<span class="prompt">$</span> hermes cron status          <span class="c"># is the scheduler alive</span>
</div>
<h2>Script-only jobs (no_agent)</h2>
<p>For jobs that need no AI (monitoring, heartbeats), use <code>no_agent=true</code>: the script runs directly and its output is delivered as the message. If the output is empty, nothing is sent — ideal for a watchdog, which only speaks up when something is wrong.</p>
<div class="code-block">
<span class="c"># CLI:</span>
<span class="prompt">$</span> hermes cron add --name "Watchdog" --schedule "*/5 * * * *" --script scripts/check_server.sh --no-agent
<span class="c"># /cron inside a chat:</span>
<span class="prompt">$</span> /cron create "*/5 * * * *" script=scripts/check_server.sh no_agent=true
</div>
<h2>Where results are delivered</h2>
<p>Job results can go to several platforms:</p>
<ul>
<li>Telegram: <code>deliver: telegram</code></li>
<li>Discord: <code>deliver: discord:CHANNEL_ID</code></li>
<li>Email: <code>deliver: email</code></li>
<li>The original chat: <code>deliver: origin</code> (the default)</li>
</ul>
<div class="tip"><strong>⏰</strong> Jobs run even while Hermes is closed to you — the scheduler is part of the gateway, which runs as a systemd service around the clock. Set up a morning briefing and never lose track of an important task again.</div>
"""

OLLAMA = """
<p>Hermes Agent supports local LLMs through Ollama — free to run, offline, and completely private. Unlike cloud APIs you pay nothing per token, and your data never leaves your computer.</p>
<h2>What is Ollama?</h2>
<p>Ollama runs open-source LLMs locally (Llama, Mistral, Gemma, Qwen and others). It works on Linux, macOS and Windows (through WSL2). It handles model downloads, GPU acceleration and a REST API for you.</p>
<h2>Installing Ollama</h2>
<div class="code-block">
<span class="c"># Linux</span>
<span class="prompt">$</span> curl -fsSL https://ollama.com/install.sh | sh
<span class="c"># macOS</span>
<span class="prompt">$</span> brew install ollama
<span class="c"># Windows — through WSL2 (see our WSL2 article)</span>
<span class="prompt">$</span> wsl --install   <span class="c"># if you don't have it yet</span>
<span class="prompt">$</span> curl -fsSL https://ollama.com/install.sh | sh
</div>
<h2>Downloading a model</h2>
<p>Once installed, pull a model. We recommend Llama 3.1 8B for general use:</p>
<div class="code-block">
<span class="prompt">$</span> ollama pull llama3.1
<span class="c"># Other models worth trying:</span>
<span class="prompt">$</span> ollama pull mistral      <span class="c"># 7B, fast, good at code</span>
<span class="prompt">$</span> ollama pull gemma2       <span class="c"># 9B, excellent at Czech</span>
<span class="prompt">$</span> ollama pull qwen2.5:7b   <span class="c"># 7B, best at technical tasks</span>
</div>
<h2>Hardware requirements</h2>
<table><tr><th>Model</th><th>Min. RAM</th><th>Recommended</th><th>GPU</th></tr>
<tr><td>Llama 3.1 8B</td><td>8 GB</td><td>16 GB</td><td>6+ GB VRAM</td></tr>
<tr><td>Mistral 7B</td><td>6 GB</td><td>12 GB</td><td>4+ GB VRAM</td></tr>
<tr><td>Gemma 2 9B</td><td>10 GB</td><td>16 GB</td><td>8+ GB VRAM</td></tr>
<tr><td>Qwen 2.5 7B</td><td>6 GB</td><td>12 GB</td><td>4+ GB VRAM</td></tr></table>
<h2>Configuring Hermes Agent</h2>
<div class="code-block">
<span class="prompt">$</span> hermes model
<span class="c"># → Select: "Custom OpenAI-compatible endpoint"</span>
<span class="c"># → Base URL: http://localhost:11434/v1</span>
<span class="c"># → API Key: ollama (Ollama needs no real key)</span>
<span class="c"># → Model: llama3.1</span>
</div>
<p>Or by hand in <code>~/.hermes/config.yaml</code>:</p>
<div class="code-block">
<span class="c"># model:</span>
<span class="c">#   default: llama3.1</span>
<span class="c">#   provider: custom</span>
<span class="c">#   base_url: http://localhost:11434/v1</span>
<span class="c">#   api_key: ollama</span>
</div>
<h2>Ollama as a service (autostart)</h2>
<div class="code-block">
<span class="c"># Start automatically after boot</span>
<span class="prompt">$</span> sudo systemctl enable ollama
<span class="prompt">$</span> sudo systemctl start ollama
<span class="c"># Verify that Ollama is running</span>
<span class="prompt">$</span> curl http://localhost:11434/api/tags
</div>
<h2>Performance tips</h2>
<ul>
<li><strong>GPU acceleration:</strong> Ollama uses the GPU automatically (NVIDIA CUDA, AMD ROCm, Apple Metal)</li>
<li><strong>Context window:</strong> 2048 tokens by default — for longer conversations raise it with <code>/set parameter num_ctx 4096</code> inside <code>ollama run llama3.1</code></li>
<li><strong>Several models at once:</strong> Ollama can serve more than one, each taking its own RAM</li>
<li><strong>Apple Silicon:</strong> on M1/M2/M3 it uses shared memory — a 16 GB MacBook Air handles even 13B models</li>
</ul>
<div class="tip"><strong>⚡</strong> The upside of a local LLM: no API fees, full privacy (data never leaves your computer), offline operation, unlimited use. The downside: you need stronger hardware, models are generally weaker than GPT-4o or Claude, and responses are slower.</div>
<h2>Local LLM vs cloud API</h2>
<table><tr><th></th><th>Local (Ollama)</th><th>Cloud (API)</th></tr>
<tr><td>Cost</td><td>Free</td><td>$5–200 a month</td></tr>
<tr><td>Privacy</td><td>100% local</td><td>Data on someone else's server</td></tr>
<tr><td>Quality</td><td>Good (8B–70B)</td><td>Excellent (GPT-4o, Claude)</td></tr>
<tr><td>Speed</td><td>Depends on your hardware</td><td>Consistent</td></tr>
<tr><td>Offline</td><td>Yes</td><td>No</td></tr></table>
<h2>Troubleshooting</h2>
<h3>Ollama will not start</h3>
<p>Check whether the service is running: <code>systemctl status ollama</code>. If not, start it with <code>ollama serve</code>.</p>
<h3>Hermes cannot reach Ollama</h3>
<p>Verify the base URL: <code>curl http://localhost:11434/v1/models</code>. If Ollama runs in Docker, use <code>http://host.docker.internal:11434/v1</code>.</p>
<h3>The model is slow</h3>
<p>Try a smaller model (mistral instead of llama3.1) or a quantised build: <code>ollama pull llama3.1:8b-instruct-q4_K_M</code>.</p>
<h2>Useful links</h2>
<ul>
<li><a href="https://ollama.com/library" target="_blank" rel="noopener">Ollama model library</a> — every available model</li>
<li><a href="https://github.com/ollama/ollama" target="_blank" rel="noopener">Ollama on GitHub</a> — source code and documentation</li>
<li><a href="https://ollama.com/search" target="_blank" rel="noopener">Model search</a> — find one that fits your needs</li>
</ul>
"""

WEBUI = """
<p>Hermes WebUI is a community web interface by nesquena (18.8k ⭐ on GitHub). It gives Hermes Agent a professional three-panel layout — a bit like VS Code, but for your AI agent.</p>
<h2>What the WebUI offers</h2>
<table><tr><th>Feature</th><th>What it does</th></tr>
<tr><td>🖥️ Three-panel layout</td><td>Session sidebar, chat panel, file browser</td></tr>
<tr><td>🌙 Light + dark</td><td>Smooth switching that follows your system setting</td></tr>
<tr><td>🇨🇿 Czech localisation</td><td>Complete translation — every string, menu and dialog</td></tr>
<tr><td>🔐 Password protection</td><td>Safe access by password or environment variable</td></tr>
<tr><td>📱 Responsive design</td><td>Fully usable on phone, tablet and desktop</td></tr>
<tr><td>🐳 Docker image</td><td>An official image for easy deployment</td></tr>
<tr><td>📂 File browser</td><td>Browse and edit files straight from the UI</td></tr>
<tr><td>💬 Multi-session</td><td>Several conversations open in tabs at once</td></tr></table>
<h2>Installing with Docker (recommended)</h2>
<div class="code-block">
<span class="c"># Download and run</span>
<span class="prompt">$</span> docker run -d -p 3000:3000 --name hermes-webui nesquena/hermes-webui
<span class="c"># With a password</span>
<span class="prompt">$</span> docker run -d -p 3000:3000 -e PASSWORD=mypassword --name hermes-webui nesquena/hermes-webui
<span class="c"># With persistent data</span>
<span class="prompt">$</span> docker run -d -p 3000:3000 -v ~/hermes-webui-data:/app/data --name hermes-webui nesquena/hermes-webui
</div>
<p>Then open <code>http://localhost:3000</code>.</p>
<h2>Installing with Docker Compose</h2>
<div class="code-block">
<span class="c"># docker-compose.yml</span>
<span class="c"># version: '3.8'</span>
<span class="c"># services:</span>
<span class="c">#   webui:</span>
<span class="c">#     image: nesquena/hermes-webui:latest</span>
<span class="c">#     ports:</span>
<span class="c">#       - "3000:3000"</span>
<span class="c">#     environment:</span>
<span class="c">#       - PASSWORD=mypassword</span>
<span class="c">#     volumes:</span>
<span class="c">#       - ./data:/app/data</span>
<span class="c">#     restart: unless-stopped</span>
</div>
<div class="code-block"><span class="prompt">$</span> docker-compose up -d</div>
<h2>Manual install (Node.js)</h2>
<div class="code-block">
<span class="prompt">$</span> git clone https://github.com/nesquena/hermes-webui.git
<span class="prompt">$</span> cd hermes-webui
<span class="prompt">$</span> npm install
<span class="prompt">$</span> npm run build
<span class="prompt">$</span> npm start
</div>
<h2>Connecting it to Hermes Agent</h2>
<p>The WebUI talks to a running Hermes Agent instance. Make sure Hermes is up:</p>
<div class="code-block"><span class="prompt">$</span> hermes</div>
<p>In the WebUI settings, enter the URL of your Hermes API endpoint (the default is <code>http://localhost:8080</code>).</p>
<h2>Deploying to a VPS behind Nginx</h2>
<div class="code-block">
<span class="c"># server {</span>
<span class="c">#   listen 443 ssl;</span>
<span class="c">#   server_name webui.your-domain.com;</span>
<span class="c">#   location / {</span>
<span class="c">#     proxy_pass http://localhost:3000;</span>
<span class="c">#     proxy_http_version 1.1;</span>
<span class="c">#     proxy_set_header Upgrade $http_upgrade;</span>
<span class="c">#     proxy_set_header Connection "upgrade";</span>
<span class="c">#   }</span>
<span class="c"># }</span>
</div>
<h2>Czech localisation</h2>
<p>The WebUI is fully localised into Czech — every screen, menu, setting and dialog. Turn it on under Settings → Language → Čeština.</p>
<div class="tip"><strong>🔗</strong> WebUI on GitHub: <a href="https://github.com/nesquena/hermes-webui" target="_blank" rel="noopener">github.com/nesquena/hermes-webui</a> — 18.8k ⭐. Docker image: <a href="https://hub.docker.com/r/nesquena/hermes-webui" target="_blank" rel="noopener">hub.docker.com/r/nesquena/hermes-webui</a></div>
"""

NOUS = """
<p>Nous Portal is the official subscription from the makers of Hermes Agent (Nous Research). One payment covers everything — both the LLM models and the tools.</p>
<h2>What you get</h2>
<ul>
<li>🤖 <strong>300+ models</strong> — Claude, GPT, Gemini, Llama and more</li>
<li>🔍 <strong>Web search</strong> — through Firecrawl</li>
<li>🎨 <strong>Image generation</strong> — FLUX</li>
<li>🔊 <strong>Text-to-Speech</strong> — OpenAI TTS</li>
<li>🎤 <strong>Speech-to-Text</strong> — Whisper</li>
<li>🌐 <strong>Cloud browser</strong> — a browser in the cloud</li>
</ul>
<h2>How to start</h2>
<ol>
<li>Go to <a href="https://nousresearch.com/portal" target="_blank" rel="noopener">nousresearch.com/portal</a></li>
<li>Create an account and pick a plan</li>
<li>In your terminal run: <code>hermes setup --portal</code></li>
<li>Sign in through OAuth — no API keys to handle</li>
</ol>
<div class="code-block"><span class="prompt">$</span> hermes setup --portal</div>
<div class="tip"><strong>💰</strong> If you use several tools (web search, images, TTS), Nous Portal works out cheaper than paying for each separately — and you get access to premium models on top.</div>
"""

# ============================================================ DÁVKA 2
OPENROUTER = """
<p>OpenRouter is an aggregator for LLM APIs — one account, one API key, access to 300+ models from every major provider. For Hermes Agent it is an ideal choice, because you can switch models without touching the configuration.</p>
<h2>Why OpenRouter with Hermes?</h2>
<ul>
<li>✅ One API key for Claude, GPT, Gemini, Llama and others</li>
<li>✅ Automatic fallback — when a model fails, it moves to another</li>
<li>✅ Transparent pricing — you pay only for the tokens you use</li>
<li>✅ No minimum balance, no monthly fee</li>
<li>✅ Price comparison across providers in one place</li>
</ul>
<h2>Step 1: Create an account</h2>
<p>Go to <a href="https://openrouter.ai" target="_blank" rel="noopener">openrouter.ai</a> → click Sign Up → sign in with Google, GitHub or email.</p>
<h2>Step 2: Get an API key</h2>
<ul>
<li>Once signed in, go to Settings → API Keys (<a href="https://openrouter.ai/settings/keys" target="_blank" rel="noopener">direct link</a>)</li>
<li>Click <strong>Create Key</strong></li>
<li>Name the key (for example "Hermes Agent")</li>
<li>Optionally set a spending limit (we suggest $10–20 a month to start)</li>
<li>Copy the key — it starts with <code>sk-or-v1-</code></li>
</ul>
<h2>Step 3: Top up credit</h2>
<p>Go to Settings → Credits (<a href="https://openrouter.ai/settings/credits" target="_blank" rel="noopener">direct link</a>) → add credit (at least $5). OpenRouter draws from that balance as tokens are used.</p>
<h2>Step 4: Configure Hermes</h2>
<div class="code-block">
<span class="prompt">$</span> hermes model
<span class="c"># → Provider: OpenRouter</span>
<span class="c"># → API Key: sk-or-v1-... (your key)</span>
<span class="c"># → Model: anthropic/claude-sonnet-4 (or any other)</span>
</div>
<h2>The best models on OpenRouter (July 2026)</h2>
<table><tr><th>Model</th><th>Input (1M tokens)</th><th>Output (1M)</th><th>Best at</th></tr>
<tr><td>Claude Sonnet 4</td><td>$3.00</td><td>$15.00</td><td>Coding, logical tasks</td></tr>
<tr><td>GPT-4o</td><td>$2.50</td><td>$10.00</td><td>General use, creative work</td></tr>
<tr><td>Gemini 2.5 Pro</td><td>$1.25</td><td>$5.00</td><td>Long context (2M)</td></tr>
<tr><td>Gemini 2.5 Flash</td><td>$0.15</td><td>$0.60</td><td>Best price/performance</td></tr>
<tr><td>DeepSeek v3</td><td>$0.27</td><td>$1.10</td><td>Cheapest good model</td></tr>
<tr><td>Llama 4 Maverick</td><td>$0.20</td><td>$0.60</td><td>Open-source alternative</td></tr></table>
<h2>Setting a fallback model</h2>
<p>When the primary model fails (rate limit, outage), Hermes switches to a backup automatically:</p>
<div class="code-block">
<span class="c"># ~/.hermes/config.yaml</span>
<span class="c"># fallback_model:</span>
<span class="c">#   provider: openrouter</span>
<span class="c">#   model: google/gemini-2.5-flash</span>
</div>
<h2>Tips for keeping costs down</h2>
<ul>
<li><strong>Cheap routine, expensive logic:</strong> use Gemini Flash ($0.15/M) for ordinary questions and switch to Claude or GPT for hard tasks</li>
<li><strong>Watch your usage:</strong> openrouter.ai/activity shows a detailed breakdown</li>
<li><strong>Set a limit:</strong> under Settings → API Keys → Edit set a monthly cap so you never spend more than you meant to</li>
</ul>
<div class="tip"><strong>💡</strong> Suggestion: top up $10, point Hermes at Gemini Flash (the cheapest good model), and switch to Claude Sonnet by hand for difficult jobs. At ordinary usage $10 lasts one to three months.</div>
"""

MCPCLAN = """
<p>MCP (Model Context Protocol) is an open standard from Anthropic for connecting AI agents to external tools, data and services. Hermes Agent supports it fully — as a client and as a server.</p>
<h2>What MCP makes possible</h2>
<ul>
<li>🔌 Connect Hermes to any MCP server (databases, APIs, file systems)</li>
<li>🛠️ Automatic discovery of the tools a server offers</li>
<li>🔄 Hermes as an MCP server for other agents (Claude Code, Cursor, Codex)</li>
<li>📦 Installing MCP servers from a catalog</li>
</ul>
<h2>Adding an MCP server to Hermes</h2>
<div class="code-block">
<span class="c"># From a URL (HTTP/SSE transport)</span>
<span class="prompt">$</span> hermes mcp add my-server --url https://example.com/mcp
<span class="c"># From a command (stdio transport)</span>
<span class="prompt">$</span> hermes mcp add local-tools --command "python3 my_mcp_server.py"
<span class="c"># Installing from the catalog</span>
<span class="prompt">$</span> hermes mcp install @anthropic/fetch
<span class="prompt">$</span> hermes mcp install @modelcontextprotocol/server-filesystem
</div>
<h2>Hermes as an MCP server</h2>
<p>Run Hermes in MCP server mode — other agents (Claude Code, Cursor) can then reach it:</p>
<div class="code-block"><span class="prompt">$</span> hermes mcp serve</div>
<p>Then add Hermes as an MCP server in Claude Code or Cursor:</p>
<div class="code-block">
<span class="c"># In .cursor/mcp.json or claude_desktop_config.json:</span>
<span class="c"># { "mcpServers": { "hermes": { "command": "hermes", "args": ["mcp", "serve"] } } }</span>
</div>
<p>That way you can use Claude Code for coding while Hermes runs in the background handling memory, scheduling, cron jobs and notifications.</p>
<h2>Managing MCP servers</h2>
<div class="code-block">
<span class="prompt">$</span> hermes mcp list             <span class="c"># connected servers</span>
<span class="prompt">$</span> hermes mcp test NAME        <span class="c"># test the connection</span>
<span class="prompt">$</span> hermes mcp configure NAME   <span class="c"># turn individual tools on or off</span>
<span class="prompt">$</span> hermes mcp remove NAME      <span class="c"># remove a server</span>
</div>
<h2>A practical example: a filesystem MCP server</h2>
<div class="code-block">
<span class="c"># Install the filesystem MCP server</span>
<span class="prompt">$</span> npx @anthropic/mcp-server-filesystem /path/to/project
<span class="c"># Add it to Hermes</span>
<span class="prompt">$</span> hermes mcp add filesystem --command "npx @anthropic/mcp-server-filesystem /path/to/project"
<span class="c"># Hermes can now read and write files in that directory</span>
</div>
<div class="tip"><strong>🔌</strong> MCP catalog: <a href="https://github.com/modelcontextprotocol/servers" target="_blank" rel="noopener">github.com/modelcontextprotocol/servers</a> — official and community MCP servers for many services (Google Drive, Slack, PostgreSQL, Puppeteer and dozens more).</div>
"""

DOCKER = """
<p>Docker is an ideal way to run Hermes Agent in isolation, without affecting the rest of the system. It suits testing, production deployment and development alike.</p>
<h2>The benefits of Docker</h2>
<ul>
<li>✅ Isolation — the agent cannot interfere with the host system</li>
<li>✅ Reproducibility — the same environment on every machine</li>
<li>✅ Easy management — <code>docker-compose up/down</code></li>
<li>✅ Persistent data — skills, memory and configuration through volumes</li>
</ul>
<h2>Installing Docker</h2>
<div class="code-block">
<span class="c"># Ubuntu/Debian</span>
<span class="prompt">$</span> sudo apt install docker.io docker-compose -y
<span class="prompt">$</span> sudo systemctl enable --now docker
<span class="c"># Add your user to the docker group (so no sudo is needed)</span>
<span class="prompt">$</span> sudo usermod -aG docker $USER
</div>
<h2>docker-compose.yml</h2>
<div class="code-block">
<span class="c"># version: '3.8'</span>
<span class="c"># services:</span>
<span class="c">#   hermes:</span>
<span class="c">#     image: hermes-agent:latest</span>
<span class="c">#     volumes:</span>
<span class="c">#       - ./hermes-data:/root/.hermes</span>
<span class="c">#     environment:</span>
<span class="c">#       - OPENAI_API_KEY=sk-...</span>
<span class="c">#     restart: unless-stopped</span>
</div>
<div class="tip"><strong>🔒</strong> Never put API keys straight into docker-compose.yml. Use a .env file instead: <code>env_file: .env</code></div>
"""

WSL2 = """
<p>Hermes Agent runs natively on Linux and macOS. On Windows you get it going through WSL2 (Windows Subsystem for Linux) — Microsoft's official virtualisation layer, free and built right into Windows 10 and 11.</p>
<h2>Step 1: Install WSL2</h2>
<p>Open PowerShell as administrator:</p>
<div class="code-block"><span class="prompt">PS&gt;</span> wsl --install</div>
<p>That installs WSL2 and the default Ubuntu distribution. Restart the computer when it finishes.</p>
<h2>Step 2: Set up Ubuntu</h2>
<p>After the restart an Ubuntu terminal opens. Create a username and password. Then update the system:</p>
<div class="code-block"><span class="prompt">$</span> sudo apt update &amp;&amp; sudo apt upgrade -y</div>
<h2>Step 3: Install Hermes Agent</h2>
<div class="code-block">
<span class="prompt">$</span> curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
<span class="prompt">$</span> source ~/.bashrc
<span class="prompt">$</span> hermes setup
</div>
<div class="tip"><strong>⚡</strong> The beauty of WSL2: Hermes runs in a Linux environment while you still have your Windows files at <code>/mnt/c/</code>. So you can work on projects stored in Windows.</div>
<h2>Troubleshooting</h2>
<h3>WSL2 will not install</h3>
<p>Make sure virtualisation is enabled in the BIOS (Intel VT-x / AMD-V).</p>
<h3>Hermes does not see the GPU</h3>
<p>For a local LLM through Ollama you need WSL2 with GPU support: run <code>wsl --update</code> and then <code>ollama serve</code> inside Ubuntu.</p>
<p>Done — your AI agent now runs on Windows through WSL2.</p>
"""

SKILLS = """
<p>Skills are one of the strongest features of Hermes Agent. They are reusable knowledge documents the agent loads when it needs them. When Hermes works out a difficult problem, it can write a skill from it and use it next time — without repeating the same mistakes.</p>
<h2>How skills work</h2>
<p>Skills use progressive disclosure to save tokens:</p>
<ul>
<li><strong>Level 0:</strong> the agent sees only the name and description (~3k tokens for dozens of skills)</li>
<li><strong>Level 1:</strong> the full text of a skill loads only when the agent needs it</li>
<li><strong>Level 2:</strong> the specific reference files (scripts, templates)</li>
</ul>
<h2>Slash commands for skills</h2>
<div class="code-block">
<span class="c"># Run a particular skill</span>
<span class="prompt">$</span> /github-pr-workflow create a PR for the auth refactor
<span class="c"># Chain several skills (up to five at once)</span>
<span class="prompt">$</span> /plan /github-pr-workflow design and implement issue #42
<span class="c"># Search for a skill</span>
<span class="prompt">$</span> /skills search docker
</div>
<h2>Creating a new skill with /learn</h2>
<p>The fastest route — the agent gathers the material and writes a structured skill itself:</p>
<div class="code-block">
<span class="c"># From a local directory</span>
<span class="prompt">$</span> /learn REST API v ~/projects/api-docs
<span class="c"># From online documentation</span>
<span class="prompt">$</span> /learn https://docs.example.com/api
<span class="c"># From a conversation</span>
<span class="prompt">$</span> /learn how I just set up the CI/CD pipeline
</div>
<h2>The SKILL.md format</h2>
<p>Every skill is a folder with one required file, <code>SKILL.md</code>:</p>
<div class="code-block">
<span class="c"># ---</span>
<span class="c"># name: my-skill</span>
<span class="c"># description: What it does</span>
<span class="c"># version: 1.0.0</span>
<span class="c"># ---</span>
<span class="c">#</span>
<span class="c"># Procedure</span>
<span class="c"># 1. Step one</span>
<span class="c"># 2. Step two</span>
</div>
<h2>Skills Hub — community skills</h2>
<p>Hermes installs skills from several sources:</p>
<ul>
<li><strong>agentskills.io</strong> — the official open standard (also used by Claude Code, Codex, Cursor and others)</li>
<li><strong>ClawHub</strong> — a community repository</li>
<li><strong>GitHub repositories</strong> — collections of your own</li>
</ul>
<div class="code-block">
<span class="prompt">$</span> hermes skills install docker-deploy
<span class="prompt">$</span> hermes skills list
</div>
<div class="tip"><strong>💡</strong> Skills follow the agentskills.io standard — you can share them between Hermes, Claude Code, Codex and other agents.</div>
<p>Skills are the key to your agent improving itself over time. The longer it runs, the more skills it collects — and the smarter it gets.</p>
"""

# ============================================================ DÁVKA 3
SSH = """
<p>Hermes supports SSH as a terminal backend — it can manage remote servers without the agent being installed on them.</p>
<h2>Configuration</h2>
<div class="code-block">
<span class="c"># config.yaml</span>
<span class="c"># terminal:</span>
<span class="c">#   backend: ssh</span>
<span class="c">#   ssh:</span>
<span class="c">#     host: 192.168.1.100</span>
<span class="c">#     user: admin</span>
<span class="c">#     key_path: ~/.ssh/id_ed25519</span>
</div>
<h2>The SSH key</h2>
<div class="code-block">
<span class="prompt">$</span> ssh-keygen -t ed25519 -C "hermes-agent"
<span class="prompt">$</span> ssh-copy-id -i ~/.ssh/id_ed25519 admin@remote-server
</div>
<div class="tip"><strong>🔒</strong> Use SSH keys, never passwords. On production servers restrict access to specific commands. Consider creating a dedicated user.</div>
"""

ADMIN = """
<p>Hermes Agent is an ideal helper for running servers — from monitoring to automating routine work.</p>
<h2>Monitoring</h2>
<div class="code-block"><span class="prompt">$</span> /cron create "0 * * * *" "Check CPU, RAM and disk. If anything is above 80%, send me an alert."</div>
<h2>Working with logs</h2>
<div class="code-block"><span class="prompt">$</span> hermes chat -q "Go through /var/log/syslog for the last hour and find ERROR and CRITICAL entries"</div>
<h2>Security audit</h2>
<div class="code-block"><span class="prompt">$</span> hermes chat -q "Run a security audit: check open ports and failed SSH attempts, and suggest what to do"</div>
<h2>Automation</h2>
<ul>
<li>🔒 A weekly security audit</li>
<li>📦 Automatic package updates (with a review)</li>
<li>💾 Backups with verification</li>
<li>📊 A monthly report on resource usage</li>
</ul>
<div class="tip"><strong>⚠️</strong> Always keep approval mode on. Never run as root. For production servers create a dedicated user with limited rights.</div>
"""

VSCODEX = """
<p>Codex is excellent at interactive coding in the terminal. Hermes is a full autonomous agent with memory, a scheduler and multi-platform access. You can use both at once — Codex for coding, Hermes for everything else.</p>
"""

VSOPENCLAW = """
<p>Both are open-source AI agents (MIT licence) and both run on your own server. Where do they differ, and which one should you pick?</p>
<h2>Side by side</h2>
<table><tr><th>Feature</th><th>Hermes</th><th>OpenClaw</th></tr>
<tr><td>Licence</td><td>✓ MIT</td><td>✓ MIT</td></tr>
<tr><td>Platforms</td><td>✓ 20+</td><td>✓ 24+</td></tr>
<tr><td>Memory</td><td>✓ Layered and persistent</td><td>✓</td></tr>
<tr><td>Skills</td><td>✓ Automatic, agentskills.io</td><td>Partly</td></tr>
<tr><td>Cron scheduler</td><td>✓ Built in</td><td>✓</td></tr>
<tr><td>LLM providers</td><td>✓ 20+ (local ones too)</td><td>✓</td></tr>
<tr><td>MCP</td><td>✓ Client and server</td><td>Partly</td></tr>
<tr><td>WebUI</td><td>✓ Community (18.8k ⭐)</td><td>✗</td></tr>
<tr><td>Desktop app</td><td>✓ Native (Electron)</td><td>✗</td></tr></table>
<div class="tip"><strong>🤝</strong> Both are fine projects. Hermes stands out in skills, memory and the desktop and WebUI side; OpenClaw supports more platforms. The choice depends on what you value most.</div>
"""

GEMINI = """
<p>Google Gemini offers 1,500 requests a day for free — ideal for getting started with Hermes Agent. It also handles Czech unusually well.</p>
<h2>Getting an API key</h2>
<ul>
<li>Go to <a href="https://aistudio.google.com" target="_blank" rel="noopener">aistudio.google.com</a></li>
<li>Sign in with your Google account</li>
<li>On the left: Get API Key → Create API Key</li>
<li>Copy the key</li>
</ul>
<h2>Configuration</h2>
<div class="code-block">
<span class="c"># ~/.hermes/.env</span>
<span class="c"># GEMINI_API_KEY=AIza...</span>
<span class="c"># or:</span>
<span class="prompt">$</span> hermes model   <span class="c"># → Provider: Google → Model: gemini-2.5-flash</span>
</div>
<h2>Free tier limits</h2>
<ul>
<li>1,500 requests per day</li>
<li>1,000,000 tokens per minute</li>
<li>Enough for ordinary use</li>
</ul>
<div class="tip"><strong>🇨🇿</strong> Gemini is one of the strongest models at Czech — its answers are grammatically correct and read naturally. For Czech users it is a great choice.</div>
"""

VOICE = """
<p>Hermes supports two-way voice: speech-to-text (STT) for what you say, and text-to-speech (TTS) for the answers.</p>
<h2>Voice in the CLI (Ctrl+B)</h2>
<p>While chatting, press Ctrl+B → speak → Hermes transcribes it and answers.</p>
<h2>Voice on messaging platforms</h2>
<p>On Telegram and Discord just send a voice message — Hermes transcribes it automatically.</p>
<h2>STT providers</h2>
<table><tr><th>Provider</th><th>Cost</th><th>Note</th></tr>
<tr><td>faster-whisper</td><td>Free</td><td>Local, needs CPU/GPU</td></tr>
<tr><td>Groq Whisper</td><td>Free (free tier)</td><td>Very fast</td></tr>
<tr><td>OpenAI Whisper</td><td>$0.006/min</td><td>Most accurate</td></tr></table>
<h2>Configuration</h2>
<div class="code-block">
<span class="c"># ~/.hermes/config.yaml</span>
<span class="c"># stt:</span>
<span class="c">#   enabled: true</span>
<span class="c">#   provider: local</span>
<span class="c"># tts:</span>
<span class="c">#   provider: edge   # free, or: openai, elevenlabs</span>
</div>
<div class="tip"><strong>🎤</strong> For free local STT: <code>pip install faster-whisper</code>. For free TTS: Edge TTS is the default and needs no API key.</div>
"""

# ============================================================ DÁVKA 4
MULTI = """
<p>Hermes Agent supports 20+ platforms from a single gateway — the same agent, the same memory, different platforms.</p>
<h2>Supported platforms</h2>
<table><tr><th>Platform</th><th>Type</th><th>Note</th></tr>
<tr><td>📱 Telegram</td><td>Messaging</td><td>The most popular, voice messages</td></tr>
<tr><td>🎮 Discord</td><td>Messaging</td><td>Slash commands, reactions</td></tr>
<tr><td>💼 Slack</td><td>Messaging</td><td>Company integrations</td></tr>
<tr><td>💬 WhatsApp</td><td>Messaging</td><td>Baileys bridge + Business API</td></tr>
<tr><td>🔐 Signal</td><td>Messaging</td><td>Encrypted communication</td></tr>
<tr><td>🔗 Matrix</td><td>Messaging</td><td>Federated, open-source</td></tr>
<tr><td>📧 Email</td><td>Messaging</td><td>SMTP/IMAP</td></tr>
<tr><td>📨 SMS</td><td>Messaging</td><td>Through a gateway</td></tr>
<tr><td>🖥️ CLI</td><td>Direct</td><td>Terminal, TUI</td></tr>
<tr><td>🖥️ Desktop</td><td>Direct</td><td>Electron app</td></tr>
<tr><td>🌐 WebUI</td><td>Direct</td><td>Web interface</td></tr>
<tr><td>🏠 Home Assistant</td><td>IoT</td><td>Smart home</td></tr></table>
<h2>Setting it up</h2>
<div class="code-block">
<span class="prompt">$</span> hermes gateway setup
<span class="c"># → Choose a platform → paste the token or key → done</span>
</div>
<p>The gateway runs as a systemd service and serves every platform at once.</p>
"""

PROFILY = """
<p>Profiles let you run several independent Hermes instances — each with its own configuration, memory, skills and session history. Ideal for keeping projects apart.</p>
<h2>Creating one</h2>
<div class="code-block">
<span class="prompt">$</span> hermes profile create project-a
<span class="prompt">$</span> hermes profile create client-b --clone   <span class="c"># copies the current settings</span>
</div>
<h2>Using a profile</h2>
<div class="code-block">
<span class="prompt">$</span> hermes --profile project-a
<span class="prompt">$</span> hermes profile use project-a   <span class="c"># make it the default</span>
</div>
<h2>Managing profiles</h2>
<div class="code-block">
<span class="prompt">$</span> hermes profile list
<span class="prompt">$</span> hermes profile show project-a
<span class="prompt">$</span> hermes profile delete old-profile
<span class="prompt">$</span> hermes profile export project-a   <span class="c"># back it up to a tar.gz</span>
</div>
<h2>Typical uses</h2>
<ul>
<li>💼 Work versus personal projects</li>
<li>👥 Different clients with different API keys</li>
<li>🧪 Testing a new Hermes version without risk</li>
<li>🌍 Different languages or regions with different models</li>
</ul>
<div class="tip"><strong>💼</strong> Every profile has its own <code>~/.hermes/profiles/NAME/</code> with a complete configuration, skills and memory.</div>
"""

RPI = """
<p>A Raspberry Pi 4/5 with 4–8 GB of RAM is enough for Hermes Agent. It draws about 5 W and costs around 1,000 CZK — ideal for a home AI agent that never sleeps.</p>
<h2>Hardware</h2>
<ul>
<li>Raspberry Pi 4 (4 GB) — the minimum, ~800 CZK</li>
<li>Raspberry Pi 5 (8 GB) — recommended, ~1,500 CZK</li>
<li>An external SSD — essential (an SD card wears out quickly)</li>
</ul>
<h2>Installation</h2>
<div class="code-block">
<span class="c"># Raspberry Pi OS (64-bit) on the SSD</span>
<span class="prompt">$</span> sudo apt update &amp;&amp; sudo apt upgrade -y
<span class="prompt">$</span> curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
</div>
<h2>Optimisation</h2>
<div class="code-block">
<span class="c"># Turn swap off (saves the SSD)</span>
<span class="prompt">$</span> sudo dphys-swapfile swapoff &amp;&amp; sudo dphys-swapfile uninstall
<span class="c"># Move logs into RAM (saves the SSD)</span>
<span class="prompt">$</span> sudo nano /etc/fstab
<span class="c"># add: tmpfs /var/log tmpfs defaults,noatime 0 0</span>
</div>
<h2>Recommended setup</h2>
<p>Use a cloud API (DeepSeek, Gemini Flash) — a Raspberry Pi has nowhere near the power for a local LLM.</p>
<div class="tip"><strong>💡</strong> Ideal for: a Telegram bot, home automation, server monitoring. Not suitable for: local LLMs, heavy computation.</div>
"""

SOUL = """
<p>SOUL.md defines how your Hermes Agent behaves and speaks: its personality, tone and rules. It is the "personality" file of your agent — a markdown file at <code>~/.hermes/SOUL.md</code>, loaded into the system prompt on every start.</p>
<h2>Built-in personas</h2>
<div class="code-block">
<span class="prompt">$</span> hermes config set agent.personality technical
<span class="c"># available: technical, friendly, concise, humorous, professional, surfer, hype, pirate, poet, ...</span>
</div>
<h2>Your own SOUL.md</h2>
<div class="code-block">
<span class="c"># ~/.hermes/SOUL.md</span>
<span class="c"># You are an AI agent specialising in DevOps and Linux server management.</span>
<span class="c"># - Answer briefly and use proper terminology</span>
<span class="c"># - Prefer Bash over Python for scripts</span>
<span class="c"># - Ask for confirmation before every destructive command</span>
<span class="c"># - Never reveal API keys in answers</span>
</div>
<h2>What SOUL.md can define</h2>
<ul>
<li>🎯 <strong>Specialisation</strong> — "You are a database expert"</li>
<li>🗣️ <strong>Communication style</strong> — brief or verbose, formal or informal</li>
<li>⚠️ <strong>Safety rules</strong> — what never to do</li>
<li>🔧 <strong>Tool preferences</strong> — which toolsets to use</li>
</ul>
<div class="tip"><strong>💡</strong> SOUL.md is loaded on every start. Changes take effect after <code>/reset</code> in a chat or after a restart.</div>
"""

TELEGRAM = """
<p>Telegram is the most popular platform for Hermes Agent. Within five minutes you can have your own AI agent that answers messages, runs tasks and remembers context across conversations.</p>
<h2>Step 1: Create a bot with BotFather</h2>
<p>Open Telegram and write to @BotFather:</p>
<div class="code-block">
<span class="c">/newbot → Name: My Hermes → Username: MyHermesBot → Save the HTTP API token!</span>
</div>
<h2>Step 2: Configure the Hermes gateway</h2>
<p>On your VPS run:</p>
<div class="code-block">
<span class="prompt">$</span> hermes gateway setup → Choose Telegram → paste the token from BotFather
</div>
<h2>Step 3: Start it</h2>
<div class="code-block"><span class="prompt">$</span> hermes gateway</div>
<p>The bot is online. Send it a message on Telegram.</p>
<h2>What the Telegram bot can do</h2>
<ul>
<li>💬 <strong>Chat</strong> — a full conversation with the AI agent</li>
<li>🔧 <strong>Every tool</strong> — web search, running code, generating images</li>
<li>🧠 <strong>Persistent memory</strong> — it remembers you across days and weeks</li>
<li>🎤 <strong>Voice messages</strong> — transcribed and answered automatically</li>
<li>⏰ <strong>The cron scheduler</strong> — morning briefings straight into Telegram</li>
<li><strong>/slash commands</strong> — /new, /model, /skills and more</li>
</ul>
<div class="tip"><strong>🔒</strong> Security: in <code>~/.hermes/.env</code> you can set <code>TELEGRAM_ALLOWED_USERS</code> — a comma-separated list of the IDs allowed to talk to the bot. That keeps everyone else out.</div>
<h2>Setting up a morning briefing</h2>
<p>The most useful feature — every morning Hermes sends you a summary:</p>
<div class="code-block"><span class="prompt">$</span> /cron create "0 8 * * *" "Give me a morning briefing: weather, GitHub notifications, today's tasks"</div>
<p>That's it. Your personal AI agent is with you around the clock on Telegram.</p>
"""

CONTABO = """
<p>Running an AI agent around the clock needs a server. The good news: Hermes Agent needs no GPU — an ordinary CPU VPS is enough. This article works out the costs and shows the best options.</p>
<h2>Why a VPS and not your own computer?</h2>
<ul>
<li>✅ It runs 24/7 — the agent answers while you sleep</li>
<li>✅ A static IP — needed for webhooks and APIs</li>
<li>✅ 99.9% uptime — professional data centres</li>
<li>✅ Unmetered traffic — you do not pay per gigabyte</li>
<li>✅ From €4.40 a month — cheaper than Netflix</li>
</ul>
<h2>Comparing VPS providers</h2>
<table><tr><th>Provider</th><th>RAM</th><th>vCPU</th><th>SSD</th><th>Traffic</th><th>Price</th></tr>
<tr><td>Contabo VPS 10 ⭐</td><td>8 GB</td><td>4</td><td>75 GB NVMe</td><td>unmetered</td><td>€5.50</td></tr>
<tr><td>Contabo VPS 20</td><td>12 GB</td><td>6</td><td>100 GB NVMe</td><td>unmetered</td><td>€7.50</td></tr>
<tr><td>Hetzner CX22</td><td>4 GB</td><td>2</td><td>40 GB</td><td>20 TB</td><td>€3.99</td></tr>
<tr><td>Hetzner CX32</td><td>8 GB</td><td>4</td><td>80 GB</td><td>20 TB</td><td>€7.99</td></tr>
<tr><td>DigitalOcean</td><td>4 GB</td><td>2</td><td>80 GB</td><td>4 TB</td><td>€28</td></tr></table>
<div class="tip"><strong>⭐</strong> Our pick: Contabo VPS 10. 8 GB RAM, unmetered traffic, an NVMe disk. Everything Hermes Agent needs for €5.50 a month. <a href="/en/hosting/">Get a VPS at Contabo →</a></div>
<h2>What it all costs</h2>
<table style="width:100%;border-collapse:collapse">
<tr><td style="padding:8px">🖥️ <strong>VPS</strong></td><td>€5.50 a month (Contabo VPS 10)</td></tr>
<tr><td style="padding:8px">🤖 <strong>LLM API</strong></td><td>€5–30 a month (depending on use and provider)</td></tr>
<tr><td style="padding:8px">🌐 <strong>Domain</strong></td><td>~€10 a year</td></tr>
<tr><td style="padding:8px;font-weight:700">💰 Total</td><td style="font-weight:700">~€10–35 a month</td></tr>
</table>
<p>* With cheap models such as DeepSeek or Gemini Flash the API cost can come to only a few euros a month.</p>
<h2>How to save on the API</h2>
<ul>
<li><strong>DeepSeek v3</strong> — $0.27 / 1M input tokens (the cheapest good model)</li>
<li><strong>Google Gemini Flash</strong> — free up to 1,500 requests a day</li>
<li><strong>OpenRouter</strong> — an aggregator with the lowest prices across providers</li>
<li><strong>Nous Portal</strong> — one subscription for 300+ models</li>
</ul>
<h2>The whole setup in 10 minutes</h2>
<div class="code-block">
<span class="c"># 1. Buy a VPS at Contabo (Ubuntu 22.04)</span>
<span class="c"># 2. Connect over SSH</span>
<span class="prompt">$</span> ssh root@your-ip
<span class="c"># 3. Install Hermes Agent</span>
<span class="prompt">$</span> curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
<span class="c"># 4. Configure it</span>
<span class="prompt">$</span> hermes setup
<span class="c"># 5. Start the gateway</span>
<span class="prompt">$</span> hermes gateway install
</div>
<p>Done — your AI agent runs 24/7 and is reachable over Telegram, Discord or the terminal.</p>
"""

VSCLAUDE = """
<p>The AI agent market is moving fast. Two major players — Hermes Agent (Nous Research) and Claude Code (Anthropic) — take different approaches to autonomous coding. Let us look at the key differences.</p>
<h2>Philosophy</h2>
<p>Claude Code is an Anthropic product — it runs in the terminal, is tightly integrated with Claude models and is proprietary. You pay for API calls and you do not get the source code.</p>
<p>Hermes Agent is fully open source (MIT licence). It runs on your own server, supports any LLM provider (not only Claude), and you keep full control of your data.</p>
<h2>Side by side</h2>
<table><tr><th>Feature</th><th>Hermes Agent</th><th>Claude Code</th></tr>
<tr><td>Licence</td><td>✓ MIT (open source)</td><td>✗ Proprietary</td></tr>
<tr><td>Memory</td><td>✓ Persistent, layered</td><td>Partly (per session)</td></tr>
<tr><td>Autonomous scheduling</td><td>✓ 24/7 cron scheduler</td><td>Cloud/desktop</td></tr>
<tr><td>Platforms</td><td>✓ 20+ (Telegram, Discord…)</td><td>✗ Terminal only</td></tr>
<tr><td>Self-hosted</td><td>✓ Fully</td><td>✗</td></tr>
<tr><td>Skills</td><td>✓ Automatic, agentskills.io</td><td>✗</td></tr>
<tr><td>LLM providers</td><td>Any (20+)</td><td>Claude only</td></tr>
<tr><td>Cost</td><td>An API key plus a VPS</td><td>API charges</td></tr></table>
<h2>When to choose Hermes</h2>
<ul>
<li>You want to own your data and keep full control</li>
<li>You need an agent 24/7 — morning briefings, monitoring, automatic pull request reviews</li>
<li>You want to reach it over Telegram, Discord or WhatsApp, not only a terminal</li>
<li>You want one agent for development, research, server admin and your home</li>
<li>You do not want to be tied to one provider — Hermes supports 20+ LLMs</li>
</ul>
<h2>When to choose Claude Code</h2>
<ul>
<li>You need maximum coding performance and do not mind a proprietary tool</li>
<li>You work mainly in the terminal and do not need messaging platforms</li>
<li>You are used to the Claude ecosystem and do not want to change</li>
</ul>
<div class="tip"><strong>🤝</strong> The best of both worlds: Hermes Agent can act as an MCP server for Claude Code — you code in Claude Code while Hermes runs in the background handling memory, scheduling and notifications.</div>
<h2>In closing</h2>
<p>Hermes Agent is not a "better Claude Code" — it is a different category. Claude Code is an excellent interactive coding tool. Hermes is an autonomous agent that lives on your server, remembers context across days and weeks, and is reachable from anywhere.</p>
<p>For individuals and small teams that want to get the most out of AI, Hermes is often the better choice — mainly because of memory, the scheduler and multi-platform access.</p>
"""

# ============================================================ DÁVKA 5 (dorovnání parit)
OPENSOURCE = """
<p>Hermes Agent is open-source (MIT licence) and welcomes contributions from the community. Here is how to get started.</p>
<h2>Development environment</h2>
<div class="code-block">
<span class="prompt">$</span> git clone https://github.com/NousResearch/hermes-agent.git
<span class="prompt">$</span> cd hermes-agent
<span class="prompt">$</span> python3 -m venv venv &amp;&amp; source venv/bin/activate
<span class="prompt">$</span> uv pip install -e .
</div>
<h2>Commit conventions</h2>
<div class="code-block">
<span class="c">fix: bug fix in ...</span>
<span class="c">feat: added support for ...</span>
<span class="c">docs: documentation update</span>
<span class="c">refactor: simplification of ...</span>
</div>
<h2>Tests</h2>
<div class="code-block">
<span class="prompt">$</span> scripts/run_tests.sh
<span class="prompt">$</span> scripts/run_tests.sh tests/tools/test_web.py
</div>
<h2>Pull requests</h2>
<ol>
<li>Create a fork on GitHub</li>
<li>Create a feature branch</li>
<li>Write the code plus tests</li>
<li>Open a PR describing the changes</li>
</ol>
<p>More at <a href="https://github.com/NousResearch/hermes-agent" target="_blank" rel="noopener">github.com/NousResearch/hermes-agent</a></p>
"""

SECURITY = """
<p>Hermes Agent has access to the terminal, your files and APIs. Getting security right matters — especially if you put the agent on public platforms.</p>
<h2>1. Restrict the users</h2>
<div class="code-block">
<span class="c"># ~/.hermes/.env</span>
TELEGRAM_ALLOWED_USERS=123456789
DISCORD_ALLOWED_USERS=987654321
</div>
<h2>2. Limit the tools</h2>
<p>CLI: every tool. A public bot: only web, memory and skills. Never give terminal access on a public platform.</p>
<h2>3. YOLO mode</h2>
<div class="code-block">
<span class="c"># config.yaml — for a public bot ALWAYS manual</span>
approvals:
  mode: manual
</div>
<h2>4. API keys</h2>
<p>✅ <code>~/.hermes/.env</code> — the only place keys belong. ✅ Add it to <code>.gitignore</code>. ❌ Never commit them to a repository.</p>
<h2>5. Firewall</h2>
<div class="code-block">
<span class="prompt">$</span> sudo ufw allow 22/tcp
<span class="prompt">$</span> sudo ufw allow 443/tcp
<span class="prompt">$</span> sudo ufw enable
</div>
<h2>6. Never run as root</h2>
<div class="code-block">
<span class="prompt">$</span> sudo useradd -m hermes
<span class="prompt">$</span> sudo -u hermes hermes
</div>
<div class="tip"><strong>🛡️ The golden rule:</strong> Hermes is only as safe as the server it runs on. Isolate it, limit its privileges, and never run it as root with YOLO mode on a production server.</div>
"""

UPDATES = """
<p>2026 has been a landmark year for Hermes Agent. Let us look at the key milestones and what is coming next.</p>
<h2>What 2026 brought</h2>
<ul>
<li>🌟 <strong>Desktop application</strong> — a native Electron app for macOS, Linux and Windows (streaming chat, drag &amp; drop, Cmd+K, notifications)</li>
<li>🔌 <strong>MCP integration</strong> — Model Context Protocol, Hermes as both server and client</li>
<li>🖥️ <strong>WebUI 1.0</strong> — the community interface from nesquena, localised into Czech</li>
<li>🌍 <strong>20+ platforms</strong> — Discord, WhatsApp, Teams, Google Chat and more</li>
<li>🇨🇿 <strong>Czech localisation</strong> — a community translation of the agent and the WebUI</li>
<li>🧠 <strong>Hindsight memory</strong> — a new memory provider with a vector database</li>
</ul>
<h2>What's coming</h2>
<ul>
<li>📱 A mobile application for iOS and Android</li>
<li>🧠 Improved memory with long-term context</li>
<li>🔗 More integrations (Google Workspace, Notion)</li>
<li>🎯 Better multi-agent orchestration</li>
</ul>
<div class="tip"><strong>🚀</strong> Follow the news on <a href="https://github.com/NousResearch/hermes-agent" target="_blank" rel="noopener">GitHub</a> (253k+ ⭐) and on our <a href="/en/community/">Discord</a>.</div>
"""

VSCODEX2 = """
<table><tr><th>Feature</th><th>Hermes</th><th>Codex</th></tr>
<tr><td>Licence</td><td>✓ MIT</td><td>✓ Apache 2.0</td></tr>
<tr><td>Self-hosted</td><td>✓ Fully, on your own server</td><td>✓ A CLI tool</td></tr>
<tr><td>Platforms</td><td>✓ 20+ (Telegram, Discord…)</td><td>✗ Terminal only</td></tr>
<tr><td>Memory</td><td>✓ Persistent, layered</td><td>Partly (per session)</td></tr>
<tr><td>Skills</td><td>✓ Automatic, agentskills.io</td><td>✗</td></tr>
<tr><td>Scheduler</td><td>✓ Cron 24/7</td><td>✗</td></tr>
<tr><td>LLM providers</td><td>Any (20+)</td><td>OpenAI only</td></tr>
<tr><td>Cost</td><td>An API key plus a VPS</td><td>An API key</td></tr></table>
<p>Codex is excellent at interactive coding in the terminal. Hermes is a full autonomous agent with memory, a scheduler and multi-platform access. You can use both at once — Codex for coding, Hermes for everything else.</p>
"""

INSTALACE = """
<p>Hermes Agent is an open-source AI agent by Nous Research that runs on your own server. Unlike cloud solutions, you have full control over your data, memory and configuration. This guide shows how to get it running on an Ubuntu VPS in under a minute.</p>
<h2>What you'll need</h2>
<ul>
<li><strong>A VPS with Ubuntu 22.04+</strong> — even the cheapest 1 GB RAM one works (we recommend <a href="/en/hosting/">Contabo from €4.40</a>)</li>
<li><strong>An LLM API key</strong> — OpenAI, Anthropic, DeepSeek, OpenRouter or any compatible provider</li>
<li><strong>SSH access</strong> to your server</li>
</ul>
<h2>Step 1: Connect to the server</h2>
<p>Connect to your VPS over SSH:</p>
<div class="code-block"><span class="prompt">$</span> ssh root@your-server-ip</div>
<h2>Step 2: Run the installer</h2>
<p>A single command installs everything you need — Python 3.11, Node.js, ripgrep, ffmpeg and Hermes itself:</p>
<div class="code-block">
<span class="c"># Install Hermes Agent</span>
<span class="prompt">$</span> curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
</div>
<div class="tip"><strong>💡</strong> The installer works out what is missing and installs it. The only prerequisites are <code>git</code>, <code>curl</code> and <code>xz-utils</code> — usually already present on Ubuntu.</div>
<h2>Step 3: Reload the shell and start</h2>
<div class="code-block">
<span class="c"># Reload the shell</span>
<span class="prompt">$</span> source ~/.bashrc
<span class="c"># Start interactive chat</span>
<span class="prompt">$</span> hermes
</div>
<h2>Step 4: Configure the LLM provider</h2>
<p>On the first run Hermes walks you through the configuration. Choose a provider and enter your API key:</p>
<div class="code-block">
<span class="c"># Pick a model interactively</span>
<span class="prompt">$</span> hermes model
<span class="c"># Or go through the whole wizard</span>
<span class="prompt">$</span> hermes setup
</div>
<p><strong>Supported providers:</strong> Nous Portal, OpenRouter, OpenAI, Anthropic, Google Gemini, DeepSeek, xAI Grok and dozens more.</p>
<h2>Step 5: Set up a Telegram bot (optional)</h2>
<p>Hermes can talk over 20+ platforms. The most popular is Telegram:</p>
<div class="code-block">
<span class="c"># Configure the messaging gateway</span>
<span class="prompt">$</span> hermes gateway setup
<span class="c"># Start the gateway</span>
<span class="prompt">$</span> hermes gateway
</div>
<p>The gateway runs in the background as a systemd service and survives a server restart.</p>
<h2>Running 24/7 as a service</h2>
<p>To keep Hermes running without interruption, install the gateway as a systemd service:</p>
<div class="code-block">
<span class="prompt">$</span> hermes gateway install
<span class="prompt">$</span> systemctl --user enable hermes-gateway
<span class="prompt">$</span> sudo loginctl enable-linger $USER
</div>
<h2>Minimum requirements</h2>
<table>
<tr><td>💾 <strong>RAM</strong></td><td>1 GB min, 2 GB recommended</td></tr>
<tr><td>⚙️ <strong>CPU</strong></td><td>1 vCPU minimum</td></tr>
<tr><td>💿 <strong>Storage</strong></td><td>10–20 GB SSD</td></tr>
<tr><td>🐧 <strong>OS</strong></td><td>Ubuntu 22.04+, Debian 12+, or a modern Linux</td></tr>
<tr><td>🤖 <strong>GPU</strong></td><td><strong>Not required</strong> — Hermes calls external LLM APIs</td></tr>
</table>
<div class="tip"><strong>🚀</strong> Want to save money? Our <a href="/en/hosting/">VPS hosting page</a> lists the cheapest Contabo VPS — from €4.40 a month with 8 GB RAM and unmetered traffic.</div>
<h2>Troubleshooting</h2>
<h3>"hermes: command not found"</h3>
<p>Reload the shell: <code>source ~/.bashrc</code> or <code>exec bash</code></p>
<h3>Missing API key</h3>
<p>Run <code>hermes model</code> and choose a provider. The API key is stored in <code>~/.hermes/.env</code>.</p>
<h3>The gateway will not start</h3>
<p>Check the log: <code>tail -f ~/.hermes/logs/gateway.log</code></p>
<p>That's it! Your own AI agent is running on your server, with full control over your data and privacy.</p>
"""

if __name__ == "__main__":
    print("=== dávka 1: macOS, cron, Ollama, WebUI, Nous Portal ===")
    oprav("hermes-agent-macos", "hermes-agent-macos", "Hermes Agent on <span>macOS</span>", MACOS)
    oprav("hermes-agent-cron-planovac", "hermes-agent-cron-scheduler",
          "Hermes Agent <span>Cron Scheduler</span>", CRON,
          titulek="Hermes Agent Cron Scheduler — 24/7 Automation | Blog",
          popis="How scheduled jobs work in Hermes Agent: creating tasks, cron expressions, real examples, script-only watchdogs and where results are delivered.")
    oprav("hermes-agent-ollama-lokalni-llm", "hermes-agent-ollama-local-llm",
          "Hermes Agent with a <span>local LLM</span>", OLLAMA,
          titulek="Local LLM in Hermes Agent (Ollama) — Free &amp; Private | Blog",
          popis="Run Hermes Agent on a local model through Ollama: installation, model choice, hardware needs, configuration and troubleshooting.",
          alt="Hermes Agent with a local LLM")
    print("=== dávka 2: OpenRouter, MCP, Docker, WSL2, Skills ===")
    oprav("hermes-agent-openrouter", "hermes-agent-openrouter",
          "Hermes Agent with <span>OpenRouter</span>", OPENROUTER,
          titulek="Hermes Agent with OpenRouter — 300+ Models, One Key | Blog",
          popis="OpenRouter with Hermes Agent: getting an API key, topping up credit, the best models of July 2026 and how to keep costs down.")
    oprav("hermes-agent-mcp-integration", "hermes-agent-mcp-integration",
          "Hermes Agent and <span>MCP</span>", MCPCLAN,
          titulek="Hermes Agent MCP Integration — Connect External Tools | Blog",
          popis="Connect Hermes Agent to MCP servers: adding them by URL or command, running Hermes as an MCP server, and managing what it may use.")
    oprav("hermes-agent-docker", "hermes-agent-docker",
          "Hermes Agent in <span>Docker</span>", DOCKER,
          titulek="Hermes Agent in Docker — Isolated Deployment Guide | Blog",
          popis="Run Hermes Agent in Docker: why isolation pays off, installing Docker, a docker-compose setup and the one mistake to avoid with keys.")
    oprav("hermes-agent-windows-wsl2", "hermes-agent-windows-wsl2",
          "Hermes Agent on <span>Windows and WSL2</span>", WSL2,
          titulek="Hermes Agent on Windows via WSL2 — Step by Step | Blog",
          popis="Run Hermes Agent on Windows through WSL2: installing WSL2, setting up Ubuntu, installing Hermes and fixing the usual snags.")
    oprav("jak-pouzivat-hermes-skills", "how-to-use-hermes-skills",
          "How to use <span>skills</span>", SKILLS,
          titulek="How to Use Hermes Agent Skills — Progressive Disclosure | Blog",
          popis="How skills work in Hermes Agent: three levels of loading, slash commands, creating a skill with /learn and the SKILL.md format.")
    print("=== dávka 3: SSH, admin, vs Codex, vs OpenClaw, Gemini, hlas ===")
    oprav("hermes-agent-ssh-vps", "hermes-agent-ssh-vps",
          "Hermes Agent over <span>SSH</span>", SSH,
          titulek="Hermes Agent over SSH — Managing Remote Servers | Blog",
          popis="How Hermes Agent manages remote servers over SSH: the terminal backend, key configuration and what to watch on production.",
          alt="Hermes Agent over SSH")
    oprav("hermes-agent-system-admin", "hermes-agent-system-admin",
          "Hermes Agent for <span>system administrators</span>", ADMIN,
          titulek="Hermes Agent for System Administrators | Blog",
          popis="Hermes Agent for sysadmins: monitoring, sifting logs, security audits and automating routine server work.",
          alt="Hermes Agent for system administrators")
    oprav("hermes-agent-vs-codex", "hermes-agent-vs-codex",
          "Hermes Agent vs <span>Codex</span>", VSCODEX,
          titulek="Hermes Agent vs Codex — Two Different Tools | Blog",
          popis="Codex for interactive coding in the terminal, Hermes as a full autonomous agent with memory and a scheduler. Why use both.")
    oprav("hermes-agent-vs-openclaw", "hermes-agent-vs-openclaw",
          "Hermes Agent vs <span>OpenClaw</span>", VSOPENCLAW,
          titulek="Hermes Agent vs OpenClaw — Comparison | Blog",
          popis="Hermes Agent and OpenClaw side by side: licence, platforms, memory, skills, MCP, WebUI and desktop app. Which one to pick.")
    oprav("hermes-agent-google-gemini", "hermes-agent-google-gemini",
          "Hermes Agent with <span>Google Gemini</span>", GEMINI,
          titulek="Hermes Agent with Google Gemini — Free API Tier | Blog",
          popis="Google Gemini with Hermes Agent: a free tier of 1,500 requests a day, getting a key, configuration and what the limits are.")
    oprav("hermes-agent-voice-mode", "hermes-agent-voice-mode",
          "Hermes Agent <span>voice mode</span>", VOICE,
          titulek="Hermes Agent Voice Mode — STT and TTS for Free | Blog",
          popis="Voice in Hermes Agent: dictating in the CLI, voice messages on Telegram and Discord, STT providers and configuration.")
    print("=== dávka 4: platformy, profily, Raspberry Pi, SOUL.md, Telegram, VPS, vs Claude Code ===")
    oprav("hermes-agent-multi-platform", "hermes-agent-multi-platform",
          "Hermes Agent on <span>20+ platforms</span>", MULTI,
          titulek="Hermes Agent on All Platforms — 20+ Integrations | Blog",
          popis="Every platform Hermes Agent speaks to from one gateway: Telegram, Discord, Slack, WhatsApp, Signal, Matrix, email and more.",
          alt="Hermes Agent on all platforms")
    oprav("hermes-agent-profily", "hermes-agent-profiles",
          "Hermes Agent <span>profiles</span>", PROFILY,
          titulek="Hermes Agent Profiles — Separate Instances | Blog",
          popis="Hermes Agent profiles: running separate instances with their own configuration, memory and skills. Creating, using and backing up.")
    oprav("hermes-agent-raspberry-pi", "hermes-agent-raspberry-pi",
          "Hermes Agent on a <span>Raspberry Pi</span>", RPI,
          titulek="Hermes Agent on a Raspberry Pi — a 24/7 Agent | Blog",
          popis="Running Hermes Agent on a Raspberry Pi 4 or 5: hardware, installing on an SSD, tuning the system and which models make sense.")
    oprav("hermes-agent-soul-md", "hermes-agent-soul-md",
          "<span>SOUL.md</span> — the agent's personality", SOUL,
          titulek="SOUL.md — Setting the Agent's Personality | Blog",
          popis="SOUL.md decides how your Hermes Agent behaves and speaks: built-in personas, your own file, and what it can define.")
    oprav("telegram-bot-hermes-agent", "telegram-bot-hermes-agent",
          "A <span>Telegram bot</span> with Hermes Agent", TELEGRAM,
          titulek="Telegram Bot with Hermes Agent — Setup in 5 Minutes | Blog",
          popis="A Telegram bot with Hermes Agent in five minutes: BotFather, the gateway, voice messages, memory and a morning briefing.")
    oprav("ai-agent-na-vps-contabo", "ai-agent-on-vps-contabo",
          "An AI agent on a <span>VPS</span> — what it costs", CONTABO,
          titulek="AI Agent on VPS — Costs and Setup | Blog",
          popis="What an always-on AI agent costs: comparing VPS providers, the API bill, saving tips and a complete setup in ten minutes.")
    oprav("hermes-agent-vs-claude-code", "hermes-agent-vs-claude-code",
          "Hermes Agent vs <span>Claude Code</span>", VSCLAUDE,
          titulek="Hermes Agent vs Claude Code — Which to Pick | Blog",
          popis="Hermes Agent and Claude Code compared: licence, memory, scheduling, platforms, skills and cost, plus when each one is the right tool.")
    print("=== dávka 5: dorovnání parit (open-source, bezpečnost, novinky, Codex, instalace, VPS) ===")
    oprav("hermes-agent-open-source", "hermes-agent-open-source",
          "Hermes Agent — <span>open source</span>", OPENSOURCE,
          alt="Hermes Agent is open source")
    oprav("bezpecnost-hermes-agent", "hermes-agent-security",
          "Hermes Agent <span>security</span>", SECURITY,
          popis="Hermes Agent has access to the terminal, files and APIs. How to secure it: restricting users and tools, approvals, API keys, firewall.")
    oprav("hermes-agent-aktualizace-2026", "hermes-agent-updates-2026",
          "Hermes Agent 2026 — <span>what is new</span>", UPDATES,
          titulek="Hermes Agent 2026 — News and Roadmap | Blog",
          popis="What 2026 brought to Hermes Agent and what comes next: the desktop app, MCP, WebUI 1.0, 20+ platforms, Czech localisation and memory.")
    oprav("hermes-agent-vs-codex", "hermes-agent-vs-codex",
          "Hermes Agent vs <span>Codex</span> (OpenAI)", VSCODEX2,
          titulek="Hermes Agent vs Codex (OpenAI) — Comparison | Blog",
          popis="Hermes Agent and OpenAI Codex compared: licence, self-hosting, platforms, memory, scheduling and cost — and why to run both.")
    oprav("instalace-hermes-agent-ubuntu", "install-hermes-agent-ubuntu",
          "Install <span>Hermes Agent</span> on Ubuntu", INSTALACE,
          titulek="Install Hermes Agent on Ubuntu VPS in 60 Seconds | Blog",
          popis="Install Hermes Agent on an Ubuntu VPS in under a minute: connecting, the installer, the model provider, Telegram and running 24/7.")
    oprav("ai-agent-na-vps-contabo", "ai-agent-on-vps-contabo",
          "An AI agent on a <span>VPS</span> — what it costs", CONTABO,
          titulek="AI Agent on VPS — Costs and Setup | Blog",
          popis="What an always-on AI agent costs: comparing VPS providers, the API bill, saving tips and a complete setup in ten minutes.")
    oprav("hermes-webui-pruvodce", "hermes-webui-guide", "Hermes <span>WebUI</span> — the complete guide", WEBUI,
          titulek="Hermes WebUI — Complete Guide to the Web Interface | Blog",
          popis="A guide to Hermes WebUI: three-panel layout, Docker, theming, Czech localisation, password protection and Nginx setup.")
    oprav("hermes-agent-nous-portal", "hermes-agent-nous-portal", "Hermes Agent with <span>Nous Portal</span>", NOUS,
          titulek="Hermes Agent with Nous Portal — Official Subscription | Blog",
          popis="Nous Portal in one page: what the official subscription covers, how much work the setup is, and when it beats paying per service.")
