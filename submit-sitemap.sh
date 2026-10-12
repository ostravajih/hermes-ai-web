#!/bin/bash
# Daily sitemap + IndexNow submission for hermes-ai.cz
# Google & Bing auto-discover sitemap from robots.txt
# IndexNow pings both engines instantly

SITE="https://hermes-ai.cz"
SITEMAP="$SITE/sitemap.xml"
INDEXNOW_KEY="hermes2026-1gtn3el9l463ok9n"
INDEXNOW_KEY_URL="$SITE/$INDEXNOW_KEY.txt"
LOG="/var/log/hermes-sitemap.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Submitting to IndexNow..." >> "$LOG"

URLS=$(curl -s --max-time 30 "$SITEMAP" | grep -oP '<loc>\K[^<]+')
URLS_JSON=$(echo "$URLS" | jq -R -s 'split("\n") | map(select(length > 0))')

if [ -n "$URLS_JSON" ] && [ "$URLS_JSON" != "[]" ]; then
    RESP=$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 \
        -X POST "https://api.indexnow.org/indexnow" \
        -H "Content-Type: application/json" \
        -d "{
            \"host\": \"hermes-ai.cz\",
            \"key\": \"$INDEXNOW_KEY\",
            \"keyLocation\": \"$INDEXNOW_KEY_URL\",
            \"urlList\": $URLS_JSON
        }")
    echo "  IndexNow: HTTP $RESP (submitted $(echo "$URLS" | wc -l) URLs)" >> "$LOG"
else
    echo "  IndexNow: FAILED (no URLs extracted from sitemap)" >> "$LOG"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Done." >> "$LOG"
