#!/bin/bash
# Denní kontrola sitemapy + odeslání všech adres do IndexNow (hermes-ai.cz)
#
# Co dělá:
#   1. aktualizuje <lastmod> v sitemapě podle skutečného data změny souborů
#   2. ověří, že je sitemapa platné XML a že klíč pro IndexNow je dostupný a správný
#   3. odešle VŠECHNY adresy ze sitemapy do IndexNow (Bing, Seznam, Yandex…)
#   4. zapíše výsledek do logu; při problému skončí chybou a zapíše ji do problémového logu
#
# Google „ping sitemapy“ už nepodporuje — sitemapu si bere z robots.txt (tam je).
#
# Ruční spuštění:  /var/www/hermesagent/submit-sitemap.sh
# Cron:            0 4 * * * /var/www/hermesagent/submit-sitemap.sh

set -uo pipefail

SITE="https://hermes-ai.cz"
SITEMAP="$SITE/sitemap.xml"
SITEMAP_FILE="/var/www/hermesagent/sitemap.xml"
INDEXNOW_KEY="hermes2026-1gtn3el9l463ok9n"
INDEXNOW_KEY_URL="$SITE/$INDEXNOW_KEY.txt"
KEY_FILE="/var/www/hermesagent/$INDEXNOW_KEY.txt"
LOG="/var/log/hermes-sitemap.log"
PROBLEM="/var/log/hermes-sitemap-problem.log"
PYTHON="/usr/bin/python3"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }
problem() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] CHYBA: $*" | tee -a "$LOG" >> "$PROBLEM"; }

log "=== start ==="

# 1) lastmod podle skutečné změny souborů
if ! "$PYTHON" /var/www/hermesagent/update-sitemap.py >> "$LOG" 2>&1; then
    problem "nepodařilo se aktualizovat lastmod v sitemapě"
    exit 1
fi

# 2) kontrola sitemapy a klíče
if ! "$PYTHON" - "$SITEMAP_FILE" <<'PY' >> "$LOG" 2>&1
import sys, xml.etree.ElementTree as ET
t = ET.parse(sys.argv[1]); locs = [e.text for e in t.iter() if e.tag.endswith('loc')]
print(f"  sitemapa: OK, {len(locs)} adres")
sys.exit(0 if locs else 1)
PY
then
    problem "sitemapa není platné XML nebo neobsahuje adresy"
    exit 1
fi

if [ "$(cat "$KEY_FILE" 2>/dev/null | tr -d '\n')" != "$INDEXNOW_KEY" ]; then
    problem "klíč v $KEY_FILE nesedí s názvem souboru"
    exit 1
fi
if [ "$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$INDEXNOW_KEY_URL")" != "200" ]; then
    problem "klíč není veřejně dostupný na $INDEXNOW_KEY_URL"
    exit 1
fi

# 3) odeslání všech adres
URLS=$(curl -s --max-time 30 "$SITEMAP" | grep -oP '<loc>\K[^<]+')
POCET=$(echo "$URLS" | grep -c .)
URLS_JSON=$(echo "$URLS" | jq -R -s 'split("\n") | map(select(length > 0))')

if [ "$POCET" -lt 10 ]; then
    problem "ze sitemapy se vytáhlo jen $POCET adres — odesílání přeskočeno"
    exit 1
fi

HTTP=$(curl -s -o /tmp/indexnow-odpoved.txt -w '%{http_code}' --max-time 40 \
    -X POST "https://api.indexnow.org/indexnow" \
    -H "Content-Type: application/json" \
    -d "{
        \"host\": \"hermes-ai.cz\",
        \"key\": \"$INDEXNOW_KEY\",
        \"keyLocation\": \"$INDEXNOW_KEY_URL\",
        \"urlList\": $URLS_JSON
    }")

# IndexNow vrací 200 (přijato) nebo 202 (přijato, klíč se ověřuje)
if [ "$HTTP" = "200" ] || [ "$HTTP" = "202" ]; then
    log "  IndexNow: HTTP $HTTP — odesláno $POCET adres ✅"
else
    problem "IndexNow vrátil HTTP $HTTP — odpověď: $(head -c 300 /tmp/indexnow-odpoved.txt)"
    exit 1
fi

log "=== hotovo ==="
exit 0
