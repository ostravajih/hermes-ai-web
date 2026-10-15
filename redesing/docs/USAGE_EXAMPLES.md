# Použití assetů ve webu

## Přepínání loga
SVG loga jsou transparentní; použij odpovídající variantu podle motivu. Při přepínání přes `data-theme` lze vložit dvě image a jednu skrýt:

```html
<img class="brand-logo logo-light" src="/assets/logos/hermes-ai-logo-light.svg" alt="Hermes AI">
<img class="brand-logo logo-dark" src="/assets/logos/hermes-ai-logo-dark.svg" alt="Hermes AI">
```

```css
.logo-dark { display: none; }
[data-theme="dark"] .logo-light { display: none; }
[data-theme="dark"] .logo-dark { display: inline-block; }
.brand-logo { width: 220px; max-width: 100%; height: auto; }
```

## Ikony
Ikony v `icons/*.svg` používají `stroke="currentColor"`; nastav barvu přes komponentu nebo CSS:

```css
.site-icon { color: var(--primary); width: 24px; height: 24px; }
```

## Hero obrázek bez textu

```css
.hero {
  background-color: var(--bg);
  background-image: url('/assets/images/hero/hero-background-dark.webp');
  background-position: center right;
  background-size: cover;
}
[data-theme="light"] .hero {
  background-image: url('/assets/images/hero/hero-background-light.webp');
}
```

Hlavní nadpisy a CTA vždy renderuj jako HTML. Text nevypaluj do rastrového pozadí, aby zůstal čitelný v responsivním zobrazení a přístupný čtečkám.

## Stránková mapa
Viz `PAGE_ASSET_MAP.json`, který přiřazuje každé hlavní URL příslušné ilustrace a varianty obrázků.
