# Hermes AI — Česká komunita 🇨🇿

Web české komunity kolem [Hermes Agent](https://github.com/NousResearch/hermes-agent) — open-source autonomního AI agenta od [Nous Research](https://nousresearch.com/) s 210 000+ hvězdami na GitHubu.

## 🌐 Web

- **[hermes-ai.cz](https://hermes-ai.cz)** — hlavní stránka
- **[hermes-ai.cz/instalace](https://hermes-ai.cz/instalace)** — kompletní návod k instalaci
- **[hermes-ai.cz/dovednosti](https://hermes-ai.cz/dovednosti)** — přehled dostupných dovedností (skills)

## 📁 Struktura

```
/var/www/hermesagent/
├── index.html          # Hlavní stránka
├── instalace.html      # Instalační příručka
├── dovednosti.html     # Přehled dovedností
├── assets/
│   ├── style.css       # Styly (světlý/tmavý režim)
│   ├── script.js       # Skripty
│   └── ...             # Obrázky a ikony
├── robots.txt
├── sitemap.xml
└── README.md
```

## 🚀 Nasazení

Nginx na VPS, SSL přes Let's Encrypt. Domény `hermes-ai.cz` a `hermes-ai.fun` (přesměrování).

## 🇨🇿 Česká lokalizace

- ✅ Hermes Web UI — [čeština přidána ve v0.51.910](https://github.com/nesquena/hermes-webui/pull/5546)
- ⏳ Hermes Agent — [čeština čeká na review](https://github.com/NousResearch/hermes-agent/pull/56521)

---

Spravuje [@ostravajih](https://github.com/ostravajih) · [multibrains.eu](https://www.multibrains.eu/)
