# E-maily pro `@hermes-ai.cz` — co chybělo a jak se to doplnilo

> **Stav (15. 10. 2026): ✅ HOTOVO.** Záznamy SPF i DMARC byly vloženy do DNS u Wedosu a ověřeny
> měřením: SPF `v=spf1 mx a -all`, DMARC `v=DMARC1; p=none; rua=mailto:postmaster@multibrains.eu; fo=1`,
> DKIM (selektor `dkim`, RSA 2048) existoval už dřív. MX míří na `mail.multibrains.eu`.
> **Další krok (až budou reporty čisté):** změnit `p=none` na `p=quarantine` v DMARC záznamu.
> Kapitoly níže popisují původní stav a postup — už je netřeba dělat znovu.

Zjištěno 15. 10. 2026 měřením DNS. **Nastavení DNS u Wedosu nemám k dispozici** (v Hermesu není uložené přihlášení),
takže tenhle krok musí udělat člověk — nebo mi předat přístup (viz poslední kapitola).

## 1. Jak to teď je (změřeno)

| Co | Stav | Hodnota |
|---|---|---|
| Poštovní server (MX) | ✅ | `mail.multibrains.eu` → 144.91.99.220 (IPv6 `2a02:c207:2307:647::1`) |
| SPF (kdo smí posílat za doménu) | ✅ **doplněno 15. 10. 2026** | `v=spf1 mx a -all` |
| DKIM (podpis odesílatele) | ✅ **existuje** | selektor `dkim`, klíč RSA 2048, záznam je v pořádku |
| DMARC (pravidlo pro příjemce) | ✅ **doplněno 15. 10. 2026** | `v=DMARC1; p=none; rua=mailto:postmaster@multibrains.eu; fo=1` |

**Proč to vadí:** bez SPF neumí přijímající servery ověřit, že mail z `@hermes-ai.cz` poslal opravdu váš server.
Nejisté maily se častěji hází do spamu. DKIM už máte, takže po doplnění SPF a DMARC bude ověření kompletní.

## 2. Dva záznamy, které bylo potřeba přidat (už jsou vložené)

Oba se vkládají do DNS domény `hermes-ai.cz` (typ **TXT**).

**A) SPF** — název (jméno) záznamu nechte prázdný nebo `@`:

```
v=spf1 mx a -all
```

Význam: `mx` = smí odesílat váš poštovní server, `a` = smí odesílat i tento webový server (13.140.139.134,
například kdyby web posílal formulářové maily), `-all` = všichni ostatní ne.

**B) DMARC** — název záznamu `_dmarc`:

```
v=DMARC1; p=none; rua=mailto:postmaster@multibrains.eu; fo=1
```

Význam: `p=none` = zatím nic neblokovat, jen sledovat (bezpečný start), `rua` = kam posílat souhrnné reporty,
`fo=1` = poslat report i při částečném selhání. Až budou reporty čisté, stačí změnit `p=none` na `p=quarantine`
(maily, které neprojdou ověřením, se budou označovat jako podezřelé).

**DKIM nedoplňujte — už tam je** (selektor `dkim`). Záznam `google._domainkey` je pravděpodobně zbytek z dřívějška.

## 3. Kde to kliknout (Wedos) — postup, kterým to prošlo

1. přihlaste se na **client.wedos.com**
2. **Moje domény** → **hermes-ai.cz** → **DNS záznamy** (sekce „Zóna" / editor záznamů)
3. **Přidat záznam** → typ **TXT** → jméno nechte prázdné (nebo `@`) → hodnota `v=spf1 mx a -all` → uložit
4. znovu **Přidat záznam** → **TXT** → jméno `_dmarc` → hodnota `v=DMARC1; p=none; rua=mailto:postmaster@multibrains.eu; fo=1` → uložit
5. změna se obvykle projeví do 15 minut (někdy do hodiny)

## 4. Jak ověřím, že to funguje

Kontrolní příkazy (spustím je sám, až budou záznamy vložené):

```bash
dig +short TXT hermes-ai.cz                 # musí vrátit "v=spf1 mx a -all"
dig +short TXT _dmarc.hermes-ai.cz          # musí vrátit "v=DMARC1; p=none; ..."
```

Potom se dá ověřit i reálný provoz: poslat testovací mail na adresu, která reportuje ověření
(`check-auth@verifier.port25.com`), a v odpovědi se ukáže SPF pass, DKIM pass a DMARC pass.

## 5. Příště to zvládnu sám

Pokud si do Hermesu uložíte přihlášení do Wedosu (Hermes se zeptá na heslo v maskovaném okně — heslo se nikdy
neobjeví v chatu), můžu takové záznamy přidávat sám, bez ručního klikání. Řekněte, jestli to chcete.
