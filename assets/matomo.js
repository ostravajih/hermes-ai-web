/* Matomo – hermes-ai.cz (site 2) + měření AI agentů.
   Nasazeno 2026-10-15. Společný soubor pro všechny stránky webu; vkládá se
   přes <script defer src="/assets/matomo.js?v=..."></script> před </head>.
   AI chatboti (ChatGPT-User, Claude-User, Perplexity-User…) neumí JavaScript,
   proto je sbírá server (nginx + služba matomo-bot-collector) přes HTTP Tracking API.

   Pozor: po načtení matomo.js Matomo window._paq NAHRADÍ vlastním objektem,
   proto se do fronty smí pushovat jen přes aktuální window._paq (ne přes
   referenci na pole zjištěnou na začátku). */
(function () {
  "use strict";

  // ---------------------------------------------------------------- vypínač
  // false = Matomo se vůbec nespustí: nenačte se tracker ani se neodešle
  // žádný požadavek. Používá se, když je server s Matomem (VPS2) mimo provoz.
  // Zapnutí zpět: přepiš na true a zvyš ?v= u matomo.js ve všech stránkách
  // i v wiki-zdroj/sablona.py, aby si prohlížeče nevzaly starou verzi z keše.
  var MERENI_ZAPNUTO = false;
  if (!MERENI_ZAPNUTO) { return; }

  var u = "https://matomo.sipkyliga.cz/";

  function paq(args) {
    window._paq = window._paq || [];
    window._paq.push(args);
  }

  paq(["setTrackerUrl", u + "matomo.php"]);
  paq(["setSiteId", "2"]);

  // Měření bez cookies: žádné ukládání v prohlížeči, žádná cookie lišta.
  // Matomo drží návštěvu pohromadě přes denní otisk (config_id), ne přes cookie.
  paq(["disableCookies"]);
  paq(["enableHeartBeatTimer", 15]);
  paq(["enableJSErrorTracking"]);
  paq(["trackAllContentImpressions"]);
  paq(["enableLinkTracking"]);

  // Vyhledávání na webu (kdyby web dostal vyhledávání s ?q=/?s=/?search=/?hledat=)
  var keyword = null;
  try {
    var params = new URLSearchParams(window.location.search);
    ["q", "s", "search", "hledat"].some(function (key) {
      var value = params.get(key);
      if (value) { keyword = value; return true; }
      return false;
    });
  } catch (err) { /* starší prohlížeč – ignorovat */ }

  if (keyword) {
    paq(["trackSiteSearch", keyword, false, false]);
  } else {
    paq(["trackPageView"]);
  }

  // Načtení oficiálního Matomo trackeru
  var script = document.createElement("script");
  script.async = true;
  script.src = u + "matomo.js";
  (document.head || document.getElementsByTagName("head")[0]).appendChild(script);

  // ---- Hloubka přečtení stránky (25/50/75/100 %) ----
  var marks = [25, 50, 75, 100], sent = {}, deepest = 0;
  function percentOf(el) {
    if (!el || typeof el.scrollHeight !== "number") { return 0; }
    var max = el.scrollHeight - el.clientHeight;
    return max <= 0 ? 100 : Math.round((el.scrollTop / max) * 100);
  }
  function measureScroll(event) {
    var best = 0;
    [document.scrollingElement, document.documentElement, document.body].forEach(function (el) {
      best = Math.max(best, percentOf(el));
    });
    var target = event && event.target;
    if (target && target.nodeType === 1 && target !== document && target.scrollHeight > target.clientHeight) {
      best = Math.max(best, percentOf(target));
    }
    if (best > deepest) { deepest = best; }
    marks.forEach(function (mark) {
      if (!sent[mark] && deepest >= mark) {
        sent[mark] = true;
        paq(["trackEvent", "Scroll", mark + " %", document.title]);
      }
    });
  }
  document.addEventListener("scroll", measureScroll, { passive: true, capture: true });
  window.addEventListener("scroll", measureScroll, { passive: true });
  window.addEventListener("resize", measureScroll);
  window.addEventListener("load", function () { setTimeout(measureScroll, 600); });

  // ---- Kliky na hlavní výzvy (CTA) ----
  function ctaName(href) {
    if (/(^|\/)en\/installation|instalace/i.test(href)) { return "Instalace"; }
    if (/github\.com/i.test(href)) { return "GitHub"; }
    if (/discord/i.test(href)) { return "Discord"; }
    return null;
  }
  document.addEventListener("click", function (event) {
    var link = event.target && event.target.closest ? event.target.closest("a") : null;
    if (!link) { return; }
    var href = link.getAttribute("href") || "";
    var name = ctaName(href);
    if (!name) { return; }
    paq(["trackEvent", "CTA", name, (link.textContent || "").trim().replace(/\s+/g, " ").slice(0, 60)]);

    // U odkazů v rámci webu dát události čas odeslat (odchozí odkazy a soubory
    // řeší Matomo sám přes sendBeacon při opuštění stránky).
    var sameSite = link.hostname === window.location.hostname;
    if (sameSite && link.target !== "_blank" && !event.metaKey && !event.ctrlKey && !event.shiftKey) {
      event.preventDefault();
      setTimeout(function () { window.location.href = link.href; }, 150);
    }
  }, true);
})();
