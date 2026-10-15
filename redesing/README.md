# Hermes AI Brand Kit v2

> **Co je to za soubor (15. 10. 2026):** popis **brandového balíčku, jak byl dodán při redesignu** —
> je to historie balíčku, ne popis dnešního webu. Ověřeno proti živému webu:
> - web je dnes **jen tmavý** (světlý režim zrušen 15. 10. 2026) → `docs/tokens.css` s `[data-theme="light"]`
>   a světlé varianty log/obrázků se už nepoužívají,
> - písmo je **jedno variabilní** `assets/redesign/fonts/Inter-web.woff2` (váhy 100–900, ~50 KB),
>   ne pět souborů 400–800,
> - dekorativní vlny patičky (`images/footer/`) a světlé sady obrázků na webu nejsou.
> Aktuální stav drží `README.md` v kořeni a `redesing/OZIVENI-WEBU-2026-10-15.md`.

Tento balíček obsahuje samostatné asset soubory a návrhová pravidla pro světlý i tmavý vzhled webu Hermes AI.

## Obsah
- `logos/` — primární, monochromatická a app/fav ikonová loga; SVG i PNG.
- `icons/` — theme-safe SVG ikony (`currentColor`).
- `images/hero/` — hero ilustrace a dekorativní pozadí.
- `images/sections/` — samostatné vizuály pro klíčové sekce.
- `images/footer/` — SVG/PNG dekorativní vlny footeru pro oba motivy.
- `docs/BRAND_GUIDE_CZ.md` — paleta, typografie, pravidla, responsive zásady a použití assetů.
- `docs/tokens.css` — CSS custom properties pro `[data-theme="light"]` a `[data-theme="dark"]`.
- `ASSET_MANIFEST.csv` — seznam souborů.

## Font
Primární font je Inter. Fonty jsou **self-hosted** jako WOFF2 (váhy 400–800) v `assets/redesign/fonts/`. Produkční CSS (`assets/redesign/style.css`) nepoužívá žádný Google Fonts import — všechny `@font-face` reference ukazují na lokální soubory (`url('/assets/redesign/fonts/Inter-XXX.woff2')`). Původní brand kit balíček používal pro prototypování Google Fonts import, ale produkce je přešla na self-hosted.

## Poznámka k ilustracím
Hero a některé sekční obrázky jsou odvozeny z dříve vytvořených vizuálních konceptů a oříznuty do samostatných souborů. Značkové logo a ikonový systém jsou vytvořené jako samostatné SVG v tomto balíčku. Pro finální produkci doporučuji ověřit crop obrázků na reálných breakpoint screenshotech a nechat text/CTA vykreslit HTML/CSS, nikoli vkládat text do pozadí.
