#!/usr/bin/env python3
"""Postaví stránku wiki „Správci hesel" (česky + anglicky) včetně verze pro AI.

Podklady: wiki-zdroj/stranky/user-guide-features-credential-vault.md (vestavěný trezor přihlášení,
2FA, karty a adresy, napojení 1Password/Bitwarden), user-guide-secrets-onepassword.md
a user-guide-secrets-bitwarden.md (načítání API klíčů při startu).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sablona import ZDROJ, najdi, stranka_html, uloz, uloz_ai  # noqa: E402

OVERENO = "17. 10. 2026"
OFICIALNI = "https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-vault"
OBRAZEK = "wiki-spravci-hesel"

# ================================================================= ČESKY
TELO_CS = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔑</span><div><strong>Hermes má dva druhy tajemství a plete se to.</strong>
<em>Přihlášení do webů</em> (jméno a heslo na cizí stránky) řeší <strong>trezor přímo v Hermesu</strong> —
nic se nenastavuje. <em>API klíče</em>, se kterými agent pracuje, se dají buď uložit do <code>.env</code>,
nebo načítat z 1Password / Bitwardenu při každém startu. První je pohodlí, druhé je hygiena.</div></div>

<h2>1. Trezor přihlášení (vestavěný)</h2>
<p>Když agent narazí na přihlašovací stránku, kterou nezná, zeptá se vás — v zakrytém poli.
Heslo se uloží <strong>zašifrované na tomto počítači</strong>, svázané s konkrétní adresou, a do stránky
se vloží přímo. <strong>Model ho nikdy nevidí</strong>; vidí jen výsledek „vyplněno 1 pole“.</p>
<table class="wiki-tabulka">
<tr><th>Kde to spravovat</th><th>Jak</th></tr>
<tr><td>Desktop</td><td>Nastavení → Passwords &amp; Logins (přidat, odebrat, odemknout správce)</td></tr>
<tr><td>Terminál</td><td><code>hermes vault list</code>, <code>hermes vault add</code></td></tr>
<tr><td>Vypnutí detekovaného správce</td><td><code>hermes vault sources --disable bitwarden</code></td></tr>
</table>

<h3>Dvoufázové ověření</h3>
<table class="wiki-tabulka">
<tr><th>Typ 2FA</th><th>Co Hermes udělá</th></tr>
<tr><td>Klíč pro autentikátor (setup key, <code>otpauth://</code>)</td><td>Kód spočítá sám a vloží — nikoho se neptá (u položky se ukáže odznak <em>2FA auto</em>)</td></tr>
<tr><td>Kód na telefon nebo e-mailem</td><td>Zobrazí malý dotaz „Ověřovací kód pro …“, vy ho napíšete, agent ho vloží. Do chatu se kód nedostane</td></tr>
<tr><td>Passkey, hardwarový klíč, schválení v aplikaci</td><td>Nic k psaní — agent počká, až to dokončíte na svém zařízení</td></tr>
</table>

<h3>Karty a adresy</h3>
<p>Ukládají se stejně jako přihlášení a vyplňují se jen na stránce, ke které patří.
<strong>Každé vyplnění karty se vás nejdřív zeptá</strong> (stejné potvrzení jako u nebezpečného příkazu);
na pozadí (cron, webhooky) se karta vyplnit nedá vůbec. Adresy potvrzení nepotřebují.</p>

<h2>2. Už používáte 1Password nebo Bitwarden?</h2>
<p>Není co zapínat. Když je nainstalovaný a přihlášený <code>op</code> nebo <code>bw</code>, Hermes si ho
najde sám a jeho webová přihlášení půjdou vyplnit stejně jako ta místní. Při prvním použití si vyžádá
odemknutí hlavním heslem (zakryté pole, jednou za sezení, po 30 minutách nečinnosti znovu).
Agent hlavní heslo ani sezení nevidí — dostane jen potvrzení, že se pole vyplnilo.</p>

<h2>3. API klíče z trezoru místo <code>.env</code></h2>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
secrets:
  onepassword:
    enabled: true
    env:
      OPENAI_API_KEY: "op://Private/OpenAI/api key"
      ANTHROPIC_API_KEY: "op://Private/Anthropic/credential"
    service_account_token_env: OP_SERVICE_ACCOUNT_TOKEN   <span class="c"># na serveru</span></div>
<p>Při každém startu (CLI, brána, cron) Hermes zavolá <code>op read</code> a hodnoty vloží do prostředí.
Otočení klíče je pak jedna změna v 1Password — všechny procesy si ji vezmou při dalším startu.
Když <code>op</code> chybí nebo je trezor zamčený, Hermes vypíše varování a jede s tím, co bylo v
<code>.env</code>; <strong>nikdy kvůli tomu nespadne</strong>.</p>
<table class="wiki-tabulka">
<tr><th>Volba</th><th>Kdy se hodí</th></tr>
<tr><td><code>override_existing: true</code> (výchozí)</td><td>Trezor je zdroj pravdy; <code>.env</code> má jen zálohu</td></tr>
<tr><td><code>override_existing: false</code></td><td>Chcete mít poslední slovo v <code>.env</code></td></tr>
<tr><td><code>cache_ttl_seconds: 0</code></td><td>Nic se neukládá na disk — nejbezpečnější, ale každý start volá <code>op</code></td></tr>
<tr><td><code>binary_path</code></td><td>Přesná cesta k <code>op</code>; <code>PATH</code> se pak neprohledává (ochrana proti podstrčenému programu)</td></tr>
</table>
<p class="note">Bitwarden funguje stejně: <code>BWS_ACCESS_TOKEN</code> v <code>.env</code> a
<code>bws secret list</code> při startu. Pro servery se používá <strong>servisní (machine) účet</strong> —
nemá 2FA dotazy a umí jen číst.</p>

<h2>4. Co si pohlídat</h2>
<table class="wiki-tabulka">
<tr><th>Situace</th><th>Co s tím</th></tr>
<tr><td>Tajemství v gitu nebo v chatu</td><td>Patří do trezoru; pokud už uniklo, zneplatnit a vyměnit</td></tr>
<tr><td>Agent se ptá na heslo pořád dokola</td><td>Přihlášení nebylo uloženo („Don't save“), nebo se stránka přesměrovává na jinou doménu</td></tr>
<tr><td>Vyplnění karty se nedaří na pozadí</td><td>Je to záměr — potvrzení vyžaduje člověka</td></tr>
<tr><td>Po změně hesla ve správci agent pořád používá staré</td><td>Odemkněte znovu správce nebo restartujte relaci</td></tr>
</table>

<h2>Kam dál</h2>
<div class="wiki-dalsi">
<a href="/wiki/zaciname/bezpecnost/"><strong>Bezpečnost</strong><span>Kdo smí co a jak omezit dopad</span></a>
<a href="/wiki/funkce/spousteni-prikazu/"><strong>Spouštění příkazů</strong><span>Schvalování a jeho hranice</span></a>
<a href="/wiki/integrace/vlastni-aplikace-mcp/"><strong>Vlastní aplikace přes MCP</strong><span>Klíče pro firemní systémy</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-vault" target="_blank" rel="noopener"><strong>Oficiální dokumentace</strong><span>Trezor přihlášení (anglicky)</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/wiki/">← Zpět na wiki</a></p>
"""

AI_CS = """
## Dva druhy tajemství
1) Přihlášení do webů -> vestavěný trezor (nic nenastavovat). Při prvním přihlášení se agent zeptá
   v zakrytém poli; heslo je zašifrované lokálně, svázané s adresou, model ho nikdy nevidí
   (vidí jen {filled_fields: 1, origin}).
2) API klíče -> .env, nebo secrets resolver (1Password / Bitwarden).

## Správa
Desktop: Nastavení -> Passwords & Logins (přidat/odebrat/odemknout). CLI: hermes vault list / vault add;
vypnutí detekovaného správce: hermes vault sources --disable bitwarden.

## 2FA
Klíč autentikátoru (setup key / otpauth:// / TOTP seed) -> kód spočítá sám (odznak 2FA auto).
Kód na telefon/e-mail -> malý dotaz, vy ho napíšete, agent vloží; do chatu se nedostane.
Passkey/hardwarový klíč/schválení v aplikaci -> agent počká na dokončení na vašem zařízení.

## Karty a adresy
Karta: každé vyplnění vyžaduje potvrzení; na pozadí (cron/webhooky) odmítnuto. Adresy bez potvrzení.

## 1Password / Bitwarden (detekce)
Nainstalovaný a přihlášený op/bw -> Hermes ho najde sám; při prvním použití odemknutí hlavním heslem
(1x za sezení, 30 min idle). Agent nevidí hlavní heslo ani session token.

## API klíče z trezoru (config.yaml)
secrets.onepassword.enabled: true; env: {OPENAI_API_KEY: "op://Private/OpenAI/api key"};
service_account_token_env: OP_SERVICE_ACCOUNT_TOKEN; override_existing: true;
cache_ttl_seconds: 0 (nic na disk); binary_path (nepoužívat PATH).
Bitwarden: BWS_ACCESS_TOKEN v .env, bws secret list <project_id>; machine account bez 2FA, jen čtení.
Chybějící op / zamčený trezor -> varování, start pokračuje s .env.

## Pozor
Tajemství nikdy do gitu/chatu · "Don't save" = bude se ptát znovu · karta na pozadí nejde (záměr)
· po změně hesla odemknout znovu / restartovat relaci.
"""

# ================================================================= ANGLICKY
TELO_EN = """
<div class="wiki-upozorneni"><span class="wiki-upozorneni__ikona">🔑</span><div><strong>Hermes deals with two kinds of secrets and people mix them up.</strong>
<em>Website logins</em> (username and password on someone else's site) are handled by the
<strong>vault built into Hermes</strong> — nothing to configure. <em>API keys</em> the agent works with
either live in <code>.env</code> or are read from 1Password / Bitwarden at every start. The first is
convenience, the second is hygiene.</div></div>

<h2>1. The login vault (built in)</h2>
<p>When the agent hits a sign-in page it has no login for, it asks you — in a masked field. The password is
stored <strong>encrypted on this machine</strong>, bound to one origin, and filled straight into the page.
<strong>The model never sees it</strong>; it sees “filled 1 field”.</p>
<table class="wiki-tabulka">
<tr><th>Where to manage it</th><th>How</th></tr>
<tr><td>Desktop</td><td>Settings → Passwords &amp; Logins (add, remove, unlock a manager)</td></tr>
<tr><td>Terminal</td><td><code>hermes vault list</code>, <code>hermes vault add</code></td></tr>
<tr><td>Turning a detected manager off</td><td><code>hermes vault sources --disable bitwarden</code></td></tr>
</table>

<h3>Two-factor codes</h3>
<table class="wiki-tabulka">
<tr><th>2FA type</th><th>What Hermes does</th></tr>
<tr><td>Authenticator key (setup key, <code>otpauth://</code>)</td><td>Generates the code and enters it — nobody is asked (the item shows a <em>2FA auto</em> badge)</td></tr>
<tr><td>Code sent to phone or e-mail</td><td>Shows a small “Verification code for …” prompt, you type it, the agent enters it. The code never enters the chat</td></tr>
<tr><td>Passkey, hardware key, app approval</td><td>Nothing to type — the agent waits for you to finish on your device</td></tr>
</table>

<h3>Cards and addresses</h3>
<p>Stored the same way as logins and filled only on the site they belong to.
<strong>Every card fill asks you first</strong> (the same approval as a dangerous command); headless
sessions (cron, webhooks) cannot fill a card at all. Address fills need no confirmation.</p>

<h2>2. Already using 1Password or Bitwarden?</h2>
<p>Nothing to enable. With <code>op</code> or <code>bw</code> installed and signed in, Hermes finds it and
its website logins become fillable alongside local ones. The first time it needs one, it asks you to
unlock the manager with your master password (masked, once per session, re-locked after 30 idle minutes).
The agent never sees the master password or the session token — only that the field was filled.</p>

<h2>3. API keys from a vault instead of <code>.env</code></h2>
<div class="code-block"><span class="c"># ~/.hermes/config.yaml</span>
secrets:
  onepassword:
    enabled: true
    env:
      OPENAI_API_KEY: "op://Private/OpenAI/api key"
      ANTHROPIC_API_KEY: "op://Private/Anthropic/credential"
    service_account_token_env: OP_SERVICE_ACCOUNT_TOKEN   <span class="c"># on a server</span></div>
<p>On every start (CLI, gateway, cron) Hermes runs <code>op read</code> and puts the values into the
environment. Rotating a key is then one change in 1Password — every process picks it up on next start.
If <code>op</code> is missing or the vault is locked, Hermes logs a warning and carries on with whatever
<code>.env</code> had; <strong>it never blocks startup</strong>.</p>
<table class="wiki-tabulka">
<tr><th>Option</th><th>When it helps</th></tr>
<tr><td><code>override_existing: true</code> (default)</td><td>The vault is the source of truth; <code>.env</code> is only a fallback</td></tr>
<tr><td><code>override_existing: false</code></td><td>You want <code>.env</code> to win</td></tr>
<tr><td><code>cache_ttl_seconds: 0</code></td><td>Nothing is written to disk — safest, but every start calls <code>op</code></td></tr>
<tr><td><code>binary_path</code></td><td>Exact path to <code>op</code>; <code>PATH</code> is then not searched (protects against a planted binary)</td></tr>
</table>
<p class="note">Bitwarden works the same way: <code>BWS_ACCESS_TOKEN</code> in <code>.env</code> and
<code>bws secret list</code> at startup. Servers use a <strong>machine account</strong> — no 2FA prompts
and read-only by design.</p>

<h2>4. What to watch</h2>
<table class="wiki-tabulka">
<tr><th>Situation</th><th>What to do</th></tr>
<tr><td>A secret in git or chat</td><td>It belongs in a vault; if it leaked, revoke and replace it</td></tr>
<tr><td>The agent keeps asking for the password</td><td>The login was not saved (“Don't save”), or the page redirects to a different origin</td></tr>
<tr><td>A card fill fails in the background</td><td>By design — a human must confirm</td></tr>
<tr><td>After changing a password the agent still uses the old one</td><td>Unlock the manager again or restart the session</td></tr>
</table>

<h2>Where next</h2>
<div class="wiki-dalsi">
<a href="/en/wiki/getting-started/security/"><strong>Security</strong><span>Who may do what and how to limit the blast radius</span></a>
<a href="/en/wiki/features/command-execution/"><strong>Running commands</strong><span>Approvals and where they stop</span></a>
<a href="/en/wiki/integrations/your-app-via-mcp/"><strong>Your app via MCP</strong><span>Keys for internal systems</span></a>
<a href="https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-vault" target="_blank" rel="noopener"><strong>Official documentation</strong><span>The login vault</span></a>
</div>
<p style="margin-top:2rem"><a class="back-link" href="/en/wiki/">← Back to the wiki</a></p>
"""

AI_EN = """
## Two kinds of secrets
1) Website logins -> built-in vault (no setup). First sign-in prompts in a masked field; the password is
   encrypted locally, bound to the origin, never seen by the model (it sees {filled_fields: 1, origin}).
2) API keys -> .env, or a secrets resolver (1Password / Bitwarden).

## Managing
Desktop: Settings -> Passwords & Logins (add/remove/unlock). CLI: hermes vault list / vault add;
disable a detected manager: hermes vault sources --disable bitwarden.

## 2FA
Authenticator key (setup key / otpauth:// / TOTP seed) -> the code is generated and entered (2FA auto badge).
Code sent to phone/e-mail -> small prompt, you type it, the agent enters it; it never enters the chat.
Passkey/hardware key/app approval -> the agent waits for you to finish on your device.

## Cards and addresses
Card: every fill needs confirmation; headless (cron/webhooks) is refused. Addresses need none.

## 1Password / Bitwarden (detection)
Installed and signed-in op/bw is detected automatically; first use asks for the master password
(once per session, 30 min idle). The agent never sees the master password or session token.

## API keys from a vault (config.yaml)
secrets.onepassword.enabled: true; env: {OPENAI_API_KEY: "op://Private/OpenAI/api key"};
service_account_token_env: OP_SERVICE_ACCOUNT_TOKEN; override_existing: true;
cache_ttl_seconds: 0 (nothing on disk); binary_path (avoid PATH lookup).
Bitwarden: BWS_ACCESS_TOKEN in .env, bws secret list <project_id>; machine account, no 2FA, read-only.
Missing op / locked vault -> warning, startup continues with .env.

## Watch out
Secrets never in git/chat · choosing "Don't save" means being asked again · card fills fail headless by design
· after a password change, unlock again or restart the session.
"""


def oznac_hotovo(cislo: int) -> None:
    cesta = ZDROJ / "stranky.json"
    data = json.loads(cesta.read_text(encoding="utf-8"))
    for s in data["stranky"]:
        if s["cislo"] == cislo:
            s["hotovo"] = True
    cesta.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    oznac_hotovo(37)
    stranka = najdi(37)
    assert stranka and stranka["nazev"] == "Správci hesel"

    uloz("cs", stranka, stranka_html(
        "cs", stranka,
        "Správci hesel — přihlášení i API klíče pod kontrolou",
        "Vestavěný trezor přihlášení bez nastavování, dvoufázové ověření, karty s potvrzením a jak načítat API klíče z 1Password nebo Bitwardenu.",
        OBRAZEK, "Wiki · Integrace", "Správci hesel",
        "Hermes má dva druhy tajemství a plete se to. Přihlášení do webů řeší trezor, API klíče trezor nebo .env.",
        TELO_CS, OVERENO, OFICIALNI))
    uloz_ai("cs", stranka, "Správci hesel (česká wiki)", OVERENO, OFICIALNI, AI_CS)
    print("✅ česká stránka + ai.txt")

    uloz("en", stranka, stranka_html(
        "en", stranka,
        "Password managers — logins and API keys under control",
        "The built-in login vault with nothing to configure, two-factor codes, cards behind a confirmation, and how to read API keys from 1Password or Bitwarden.",
        OBRAZEK, "Wiki · Integrations", "Password managers",
        "Hermes handles two kinds of secrets and people mix them up. Website logins go to the vault; API keys to a vault or .env.",
        TELO_EN, OVERENO, OFICIALNI))
    uloz_ai("en", stranka, "Password managers (community wiki)", OVERENO, OFICIALNI, AI_EN)
    print("✅ anglická stránka + ai.txt")
    print("   adresy:", stranka["cs"], "↔", stranka["en"])
