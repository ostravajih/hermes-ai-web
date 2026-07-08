# Hermes AI — Česká komunita 🇨🇿

Web české komunity kolem [Hermes Agent](https://github.com/NousResearch/hermes-agent) — open-source autonomního AI agenta od [Nous Research](https://nousresearch.com/) s 210 000+ hvězdami na GitHubu.

## 🌐 Web

- **[hermes-ai.cz](https://hermes-ai.cz)** — hlavní stránka (CZ)
- **[hermes-ai.cz/en/](https://hermes-ai.cz/en/)** — English version
- **[hermes-ai.cz/instalace](https://hermes-ai.cz/instalace)** — kompletní návod k instalaci
- **[hermes-ai.cz/dovednosti](https://hermes-ai.cz/dovednosti)** — přehled dostupných dovedností (skills)
- **[hermes-ai.cz/hosting](https://hermes-ai.cz/hosting)** — VPS hosting

## 📁 Struktura

```
/var/www/hermesagent/
├── index.html              # Hlavní stránka (CZ)
├── instalace.html          # Instalační příručka (CZ)
├── hosting.html            # VPS hosting (CZ)
├── dovednosti.html         # Přehled dovedností (CZ)
├── en/
│   ├── index.html          # Landing page (EN)
│   ├── installation.html   # Installation guide (EN)
│   ├── hosting.html        # VPS hosting (EN)
│   └── skills.html         # Skills overview (EN)
├── assets/
│   ├── style.css           # Styly (světlý/tmavý režim)
│   ├── script.js           # Skripty (theme toggle, jazyková detekce)
│   └── ...                 # Obrázky a ikony
├── robots.txt
├── sitemap.xml
└── README.md
```

## 🌍 Jazykové verze

- **CS**: výchozí pro česky/slovensky mluvící návštěvníky
- **EN**: automaticky pro ostatní (podle `navigator.language`)
- Přepínač `🇨🇿 CZ` / `🇬🇧 EN` v navigační liště
- Volba se ukládá do `localStorage`, přežije reload
- SEO: `hreflang` tagy, oddělené `canonical` URL

## 🚀 Nasazení

Nginx na VPS, SSL přes Let's Encrypt. Domény `hermes-ai.cz` a `hermes-ai.fun` (přesměrování).

## 🇨🇿 Česká lokalizace

- ✅ Hermes Web UI — [čeština přidána ve v0.51.910](https://github.com/nesquena/hermes-webui/pull/5546)
- ⏳ Hermes Agent — [čeština čeká na review](https://github.com/NousResearch/hermes-agent/pull/56521)

---

Spravuje [@ostravajih](https://github.com/ostravajih) · [multibrains.eu](https://www.multibrains.eu/)
