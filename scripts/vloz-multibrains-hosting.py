#!/usr/bin/env python3
"""Vloží do /hosting/ (CS i EN) sekci s hotovým Hermes Agent hostingem od MultiBrains.

Contabo část zůstává beze změny; nová sekce jde před závěrečné CTA.
Ceny se berou z multibrains.eu (Free 7 dní zdarma, Start 99, Pro 249, Business 690 Kč).
"""
from pathlib import Path
import re
import sys

ROOT = Path("/var/www/hermesagent")
MARK = "<!-- multibrains-managed-hosting -->"

CS = MARK + """
<section id="managed-hosting">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">Hotové řešení</div>
      <h2>Nechcete server spravovat? Použijte hotový Hermes Agent hosting</h2>
      <p>VPS u Contabo je skvělý, když chcete root a plnou kontrolu. Pokud ale chcete agenta spustit během dvou minut a neřešit instalaci, aktualizace ani zálohy, máme vlastní hosting <strong>MultiBrains</strong>.</p>
    </div>

    <div class="cards-grid">
      <div class="card">
        <div class="card-icon">🆓</div>
        <h3>Free</h3>
        <p><strong>0 Kč</strong> — prvních 7 dní</p>
        <p>1 agent, model MultiBrains Free, 2 vCPU a 4 GB paměti, 6 GB disku. Bez platební karty.</p>
      </div>
      <div class="card">
        <div class="card-icon">🚀</div>
        <h3>Start</h3>
        <p><strong>99 Kč</strong> / měsíc</p>
        <p>3 agenti, modely MultiBrains Standard, 20 GB disku, šablony n8n, Claude Code a OpenCode.</p>
      </div>
      <div class="card">
        <div class="card-icon">⚡</div>
        <h3>Pro</h3>
        <p><strong>249 Kč</strong> / měsíc</p>
        <p>10 agentů, modely MultiBrains Pro, 4 vCPU a 8 GB paměti na agenta, 100 GB disku, vlastní klíč k modelu (BYOK).</p>
      </div>
      <div class="card">
        <div class="card-icon">🏢</div>
        <h3>Business</h3>
        <p><strong>690 Kč</strong> / měsíc</p>
        <p>Bez omezení počtu agentů, vlastní doména agenta, 500 GB disku na agenta, faktury s DIČ.</p>
      </div>
    </div>

    <div style="overflow-x:auto;margin-top:32px">
      <table style="width:100%;border-collapse:collapse;font-size:0.95rem">
        <tr>
          <th style="text-align:left;padding:12px;border-bottom:1px solid var(--border)"></th>
          <th style="text-align:left;padding:12px;border-bottom:1px solid var(--border)">VPS u Contabo</th>
          <th style="text-align:left;padding:12px;border-bottom:1px solid var(--border)">MultiBrains hosting</th>
        </tr>
        <tr>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Pro koho</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Chcete root, vlastní služby a plnou kontrolu</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Chcete hotového agenta bez správy serveru</td>
        </tr>
        <tr>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Instalace</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Sami podle <a href="/instalace/" style="color:var(--accent)">návodu</a> (5–15 minut)</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">2 minuty, bez terminálu</td>
        </tr>
        <tr>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Údržba, aktualizace, zálohy</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Sami</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">My — zálohy a klony na kliknutí</td>
        </tr>
        <tr>
          <td style="padding:12px">Cena</td>
          <td style="padding:12px">Od 4,40 € měsíčně + vaše práce</td>
          <td style="padding:12px">Od 99 Kč měsíčně, první týden zdarma</td>
        </tr>
      </table>
    </div>

    <p style="text-align:center;margin-top:28px">
      <a href="https://multibrains.eu/cenik?utm_source=hermes-ai&utm_medium=hosting" target="_blank" rel="noopener" class="btn btn-primary">Prohlédnout hosting →</a>
    </p>
    <p style="text-align:center;color:var(--text-muted);font-size:0.8rem;margin-top:8px">MultiBrains je náš vlastní produkt — stejný provozovatel jako tento web.</p>
  </div>
</section>
"""

EN = MARK + """
<section id="managed-hosting">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">Done for you</div>
      <h2>Do not want to run a server? Use managed Hermes Agent hosting</h2>
      <p>A Contabo VPS is great when you want root and full control. If you want an agent running in two minutes without installation, updates or backups, we offer our own hosting at <strong>MultiBrains</strong>.</p>
    </div>

    <div class="cards-grid">
      <div class="card">
        <div class="card-icon">🆓</div>
        <h3>Free</h3>
        <p><strong>0 CZK</strong> — first 7 days</p>
        <p>1 agent, MultiBrains Free model, 2 vCPU and 4 GB RAM, 6 GB disk. No card required.</p>
      </div>
      <div class="card">
        <div class="card-icon">🚀</div>
        <h3>Start</h3>
        <p><strong>99 CZK</strong> / month</p>
        <p>3 agents, MultiBrains Standard models, 20 GB disk, n8n, Claude Code and OpenCode templates.</p>
      </div>
      <div class="card">
        <div class="card-icon">⚡</div>
        <h3>Pro</h3>
        <p><strong>249 CZK</strong> / month</p>
        <p>10 agents, MultiBrains Pro models, 4 vCPU and 8 GB RAM per agent, 100 GB disk, bring your own model key (BYOK).</p>
      </div>
      <div class="card">
        <div class="card-icon">🏢</div>
        <h3>Business</h3>
        <p><strong>690 CZK</strong> / month</p>
        <p>Unlimited agents, custom agent domain, 500 GB disk per agent, invoices with VAT ID.</p>
      </div>
    </div>

    <div style="overflow-x:auto;margin-top:32px">
      <table style="width:100%;border-collapse:collapse;font-size:0.95rem">
        <tr>
          <th style="text-align:left;padding:12px;border-bottom:1px solid var(--border)"></th>
          <th style="text-align:left;padding:12px;border-bottom:1px solid var(--border)">Contabo VPS</th>
          <th style="text-align:left;padding:12px;border-bottom:1px solid var(--border)">MultiBrains hosting</th>
        </tr>
        <tr>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Who it is for</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">You want root, your own services and full control</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">You want a ready agent without server management</td>
        </tr>
        <tr>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Installation</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Yourself, following the <a href="/en/installation/" style="color:var(--accent)">guide</a> (5–15 min)</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">2 minutes, no terminal</td>
        </tr>
        <tr>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Maintenance, updates, backups</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">Yourself</td>
          <td style="padding:12px;border-bottom:1px solid var(--border)">We do it — backups and clones in one click</td>
        </tr>
        <tr>
          <td style="padding:12px">Price</td>
          <td style="padding:12px">From €4.40 per month plus your time</td>
          <td style="padding:12px">From 99 CZK per month, first week free</td>
        </tr>
      </table>
    </div>

    <p style="text-align:center;margin-top:28px">
      <a href="https://multibrains.eu/cenik?utm_source=hermes-ai&utm_medium=hosting" target="_blank" rel="noopener" class="btn btn-primary">See hosting →</a>
    </p>
    <p style="text-align:center;color:var(--text-muted);font-size:0.8rem;margin-top:8px">MultiBrains is our own product — the same operator as this website.</p>
  </div>
</section>
"""

ANCHOR = '<section style="background:var(--accent-light);text-align:center">'


def insert(path: Path, block: str) -> str:
    html = path.read_text(encoding="utf-8")
    if MARK in html:
        return "už obsahuje"
    if html.count(ANCHOR) != 1:
        return f"CHYBA: kotva nalezena {html.count(ANCHOR)}×"
    html = html.replace(ANCHOR, block + ANCHOR, 1)
    path.write_text(html, encoding="utf-8")
    return "vloženo"


for rel, block in (("hosting/index.html", CS), ("en/hosting/index.html", EN)):
    print(rel, "→", insert(ROOT / rel, block))
