# Hermes AI — design systém v2.0

## Směr značky
Tmavě modrý základ, neonově tyrkysová, modrá a fialová; stejné komponenty v dark/light režimu. Značka zůstává **Hermes AI** a web zůstává zaměřený na Hermes Agent, otevřený projekt, instalaci, funkce, komunitu a návody.

## Doporučená typografie
- **Primární písmo:** Inter (Google Fonts nebo self-hosted webfont; soubory fontů nejsou součástí balíčku).
- Nadpisy: Inter 700–800, běžný text 400–500, UI štítky 500–600.
- H1: `clamp(2.5rem, 5vw, 4.25rem)`, line-height 1.02–1.1, tracking `-0.04em`.
- H2: `clamp(1.8rem, 3vw, 2.75rem)`, line-height 1.12.
- H3: 1.2–1.5rem, weight 650–700.
- Body: 1rem / 1.65; drobný UI text ne menší než 0.8125rem.
- Fallback: `ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.

## Barevná paleta

### Značkové barvy (sdílené mezi motivy)
| Token | HEX | Použití |
|---|---|---|
| Brand Cyan | `#00DCEB` | Akce, focus, ikony |
| Brand Blue | `#3B82F6` | Odkazy, druhá část gradientu |
| Brand Violet | `#8B5CF6` | Akcent, ilustrace |
| Gradient | `linear-gradient(110deg, #00DCEB 0%, #3B82F6 52%, #8B5CF6 100%)` | Primární CTA, zvýraznění H1 |
| Success | `#10B981` | Stav úspěchu |
| Warning | `#F59E0B` | Upozornění |
| Danger | `#EF4444` | Chyby |

### Tmavý vzhled
| Token | HEX |
|---|---|
| Background | `#07111F` |
| Surface | `#0B1727` |
| Surface elevated | `#111F32` |
| Surface hover | `#192A40` |
| Text primary | `#F8FAFC` |
| Text muted | `#A7B7CC` |
| Border | `#263A53` |
| Border strong | `#3A5473` |

### Světlý vzhled
| Token | HEX |
|---|---|
| Background | `#F7FAFE` |
| Surface | `#FFFFFF` |
| Surface elevated | `#EEF4FB` |
| Surface hover | `#E5EDF7` |
| Text primary | `#0F172A` |
| Text muted | `#52657C` |
| Border | `#D6E1EE` |
| Border strong | `#AFC1D5` |

## Loga
- `hermes-ai-logo-dark.svg` používat na tmavé plochy (světlý wordmark).
- `hermes-ai-logo-light.svg` používat na světlé plochy (tmavý wordmark).
- `hermes-ai-logo-mono-*` pro monochromatické nebo omezené výstupy.
- `hermes-ai-symbol.svg` pro avatar, favicon a malé UI; zachovat bezpečnou zónu alespoň 20 % výšky symbolu.
- SVG loga jsou transparentní; PNG verze jsou exporty pro nástroje bez SVG podpory.

## Ikonografie
- Ikony v `icons/*.svg` mají `stroke="currentColor"`, rozměr 24×24, zaoblené zakončení a tloušťku 1.8. Barvu určovat přes CSS podle tématu; nebarvit každý symbol jinak.
- Základní velikosti: 16 px (inline), 20 px (UI), 24 px (karty), 32 px (hero feature).
- Nepoužívat ikony jako jediné označení akce bez textu nebo přístupného `aria-label`.

## Obrázky / sekce
- `images/hero/hero-ai-agent-dark.webp` a `hero-ai-agent-light.webp`: hlavní hero ilustrace pro odpovídající téma.
- `hero-background-*`: široké dekorativní pozadí; text a CTA nevkládat do obrázku, ale vykreslit v HTML.
- `images/sections/*`: samostatné vizuály pro Co je Hermes Agent, Funkce, Instalace, Hosting, Skills/MCP, Blog/FAQ, bezpečnost a komunitu; SVG ilustrace jsou vektorové a lze je použít na obou pozadích. Kde existuje `*-light.webp`, jde o odlehčenou variantu rastru.
- `images/footer/footer-wave-*`: škálovatelný dekorativní footer wave, vhodný pro background.
- Na mobilu použít objektovou pozici tak, aby ilustrace neomezila čitelnost textu; hero copy umístit nad obrázek nebo obrázek zkrátit.
- Obrázky původně pocházejí z vizuálních konceptů a část sekčních variant je oříznuta z návrhových tabulí; jde o samostatné asset soubory, nikoli finálně retušovanou fotobankovou produkci. Pro klíčové marketingové plochy je doporučené před nasazením schválit finální crop.

## Komponenty
- Karty: radius 16–20 px, 1 px border; dark režim bez přehnané záře, light režim jemný stín.
- CTA: primární gradient, kontrastní text, výška 44–48 px, radius 10–12 px.
- Navigace: při scrollu lze změnit na solid surface s border; na mobilu menu v draweru.
- Gradient nepoužívat jako pozadí každé karty; vyhradit pro CTA, malé ikony a důležitá zvýraznění.
- Přístupnost: kontrast textu ověřit pro každý stav; focus ring 3 px; respektovat `prefers-reduced-motion`.

## Doporučená struktura použití
- `/` — hlavní hero, co je Hermes Agent, hlavní schopnosti, rychlý start, komunita.
- `/co-je-hermes` — vysvětlení agenta a jeho vztahu k projektu Nous Research.
- `/funkce` — nástroje, paměť, skills, MCP a plánování.
- `/instalace` — instalační kroky, systémové požadavky a ověřené příkazy.
- `/hosting` — lokální běh, Docker, VPS a cloud; uvádět jen skutečně podporované možnosti.
- `/skills` — katalog dovedností a bezpečnostní metadata.
- `/blog` — návody, aktuality a praktické příklady.
- `/faq` — přístupné accordion komponenty.

## Responzivní body (výchozí návrh)
- 360–767 px: mobil, jedna kolona, hamburger menu, hero ilustrace pod hlavním CTA.
- 768–1023 px: tablet, karty 2 sloupce, omezená šířka textu.
- 1024 px a více: desktop, hero 2 sloupce, obsah max-width přibližně 1240 px.
- 1440 px a více: hero obrázek může využít větší plochu, ale textový sloupec ponechat do 650 px.

## Důležitá poznámka
Tento balíček je vizuální návrhový základ. Texty, počty nástrojů, licence, kompatibilitu, GitHub odkazy a technické příkazy na stávajícím webu ověřit proti aktuálnímu projektu Hermes Agent před publikací.
