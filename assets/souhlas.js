/* Souhlas s měřením — hermes-ai.cz
   Nasazeno 2026-10-16. Vkládá se na každou stránku místo měřicích skriptů:

     <script defer src="/assets/souhlas.js?v=20261016"></script>

   Měření (Matomo na vlastním serveru a Google Analytics na několika stránkách)
   se načte až ve chvíli, kdy návštěvník klikne na „Povolit měření“.
   Do té doby neodejde z prohlížeče ani jeden požadavek na měřicí server.

   Volba se pamatuje v prohlížeči pod klíčem hermes_souhlas:
     "ano" = měření povoleno, "ne" = jen nezbytné (žádné měření).
   Změnit ji lze tlačítkem na stránce /soukromí/ (odkaz v patičce). */
(function () {
  "use strict";

  var KLIC = "hermes_souhlas";
  var jeEn = /^\/en(\/|$)/.test(window.location.pathname);
  var verze = "20261016";

  var texty = jeEn ? {
    popis: "We anonymously measure how many people visit the site and which pages interest them, so we know what to improve. Nothing we collect identifies you and we never sell your data.",
    ano: "Allow measurement",
    ne: "Essential only",
    odkaz: "How we measure",
    odkazUrl: "/en/privacy/",
    nastaveni: "Measurement settings"
  } : {
    popis: "Anonymně měříme, kolik lidí si web prohlédne a které stránky je zajímají — díky tomu víme, co zlepšovat. Nic z toho vás neidentifikuje a data nikomu neprodáváme.",
    ano: "Povolit měření",
    ne: "Jen nezbytné",
    odkaz: "Jak měříme",
    odkazUrl: "/soukromi/",
    nastaveni: "Nastavení měření"
  };

  function uloz(hodnota) {
    try { window.localStorage.setItem(KLIC, hodnota); } catch (e) { /* prohlížeč paměť blokuje */ }
  }
  function precti() {
    try { return window.localStorage.getItem(KLIC); } catch (e) { return null; }
  }
  function smaz() {
    try { window.localStorage.removeItem(KLIC); } catch (e) { /* nic */ }
  }

  /* ---------- načtení měření (až po souhlasu) ---------- */
  function nactiMereni() {
    var hlava = document.head || document.getElementsByTagName("head")[0];

    // Matomo na vlastním serveru (matomo.js si sám načte tracker)
    if (!document.getElementById("hermes-matomo")) {
      var m = document.createElement("script");
      m.id = "hermes-matomo";
      m.async = true;
      m.src = "/assets/matomo.js?v=" + verze;
      hlava.appendChild(m);
    }

    // Google Analytics – jen na stránkách, které ho používají
    if (window.__hermesGA4 && !document.getElementById("hermes-ga4")) {
      var id = window.__hermesGA4;
      var g = document.createElement("script");
      g.id = "hermes-ga4";
      g.async = true;
      g.src = "https://www.googletagmanager.com/gtag/js?id=" + id;
      hlava.appendChild(g);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      window.gtag("config", id);
    }
  }

  /* ---------- lišta ---------- */
  function skryjListu() {
    var el = document.getElementById("hermes-souhlas");
    if (!el) { return; }
    if (el.parentNode) { el.parentNode.removeChild(el); }
  }

  function zobrazListu() {
    if (document.getElementById("hermes-souhlas")) { return; }

    var list = document.createElement("div");
    list.id = "hermes-souhlas";
    list.setAttribute("role", "region");
    list.setAttribute("aria-label", texty.nastaveni);
    list.style.cssText = "position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#0b1727;border-top:1px solid #1e3a5f;" +
      "box-shadow:0 -10px 30px rgba(0,0,0,.5);color:#f8fafc;opacity:0;transition:opacity .25s ease";

    var vnitrek = document.createElement("div");
    vnitrek.style.cssText = "max-width:1100px;margin:0 auto;padding:.9rem 1rem;display:flex;flex-wrap:wrap;gap:.75rem;" +
      "align-items:center;font-size:.88rem;line-height:1.5;box-sizing:border-box";

    var popis = document.createElement("p");
    popis.style.cssText = "margin:0;flex:1 1 320px;min-width:0";
    popis.appendChild(document.createTextNode(texty.popis + " "));
    var odkaz = document.createElement("a");
    odkaz.href = texty.odkazUrl;
    odkaz.style.cssText = "color:#00dceb;white-space:nowrap";
    odkaz.textContent = texty.odkaz + " →";
    popis.appendChild(odkaz);

    var tlacitka = document.createElement("div");
    tlacitka.style.cssText = "display:flex;gap:.5rem;flex-wrap:wrap";

    var ano = document.createElement("button");
    ano.type = "button";
    ano.textContent = texty.ano;
    ano.style.cssText = "cursor:pointer;border:0;border-radius:.5rem;padding:.55rem .95rem;font:inherit;font-weight:600;" +
      "background:#00dceb;color:#061020";
    var ne = document.createElement("button");
    ne.type = "button";
    ne.textContent = texty.ne;
    ne.style.cssText = "cursor:pointer;border:1px solid #1e3a5f;border-radius:.5rem;padding:.55rem .95rem;font:inherit;" +
      "background:transparent;color:#f8fafc";

    function rozhodni(hodnota) {
      uloz(hodnota);
      skryjListu();
      if (hodnota === "ano") { nactiMereni(); }
    }
    ano.addEventListener("click", function () { rozhodni("ano"); });
    ne.addEventListener("click", function () { rozhodni("ne"); });

    tlacitka.appendChild(ano);
    tlacitka.appendChild(ne);
    vnitrek.appendChild(popis);
    vnitrek.appendChild(tlacitka);
    list.appendChild(vnitrek);
    document.body.appendChild(list);

    var klid = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (klid) { list.style.opacity = "1"; }
    else { window.requestAnimationFrame(function () { list.style.opacity = "1"; }); }
  }

  /* ---------- spuštění ---------- */
  function start() {
    var volba = precti();
    if (volba === "ano") { nactiMereni(); }
    else if (volba === "ne") { /* nic – jen nezbytné */ }
    else { zobrazListu(); }
  }

  // Tlačítko „Nastavení měření“ na stránce o soukromí
  window.hermesSouhlas = {
    zmenit: function () {
      smaz();
      window.location.reload();
    },
    stav: precti
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
