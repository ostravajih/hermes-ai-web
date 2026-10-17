# Fronta změn — 2026-10-17

Zkontrolováno 17. 10. 2026 · 17 změn se týkalo našich stránek · **všechny vyřízené**

## ✅ Doplněno do wiki

| Dokumentace | Co se udělalo |
|---|---|
| `user-guide-tui` | Doplněno na stránku TUI (fronta zpráv na bráně, [queued], Ctrl+X vs. Esc). |
| `user-guide-desktop` | Doplněno na stránku Desktop (historie zadání šipkami, fronta, „Turn lost during restart“). |
| `user-guide-features-delegation` | Doplněno na stránku Podagenti (jednorázový běh počká na výsledky, limit 2 pomocníků). |
| `user-guide-features-curator` | Upřesněno na stránce Kurátor skillů (údržba brány pokrývá i místní Desktop, hodinový časovač hermes serve). |
| `user-guide-features-cron` | Doplněno na stránku Pravidelné úlohy (adresování jménem vedle ID). |
| `guides-cron-troubleshooting` | Doplněno na stránku Pravidelné úlohy (cron tick potřebuje běžící bránu). |
| `user-guide-session-storage-recovery` | Opraveno na stránce Zálohy a obnova (sessions prune je pod živou branou bezpečné). |
| `getting-started-installation` | Doplněno na stránku Instalace (poslední stabilní verze, --channel main). |

## ➖ Bez dopadu na naše stránky

Změny se týkají vnitřností brány, CLI nebo oblastí, které na wiki nepokrýváme:

| Dokumentace | Proč se nic nemění |
|---|---|
| `reference-cli-commands` | nové --base-url/--api-key a --model u --safe-mode; na žádné naší stránce se --safe-mode nepoužívá |
| `getting-started-updating` | pravidla přesunu mezi kanály; stránku o aktualizacích nemáme, řeší ji instalace |
| `user-guide-configuring-models` | přepis řádku Model: v systémové výzvě; naše stránka mluví jen o ceně za nové načtení kontextu |
| `user-guide-docker` | supervised gateway pod --tui a logy v kontejneru; naše stránky Docker nerozebírají |
| `user-guide-features-plugins` | plugin běží pod autoritou sezení brány — vnitřní věc |
| `user-guide-features-web-dashboard` | identita požadavků při mazání sezení — vnitřní věc |
| `user-guide-multi-connection-desktop` | socket pro každou dvojici připojení+profil — vnitřní věc |
| `user-guide-multi-profile-gateways` | rezervace profilu v multiplexeru — vnitřní věc |
| `user-guide-sessions` | přístup více operátorů k sezení a evidence autorství — vnitřní věc |

## Jak to znovu projít

Rozdíly jsou uložené v `wiki-zdroj/zmeny/2026-10-17/` (jeden `.diff` na stránku dokumentace).
Když se dokumentace změní znovu, `fronta-zmen.py` zapíše novou frontu a tuhle nahradí.
