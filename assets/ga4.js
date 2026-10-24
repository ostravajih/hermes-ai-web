/* Google Analytics 4 – hermes-ai.cz
   Nasazeno 2026-10-17. Společný soubor pro všech 160 stránek webu; vkládá se
   přes <script defer src="/assets/ga4.js?v=..."></script> před </head>
   (hned za matomo.js).

   Nastavení (rozhodnutí vlastníka 17. 10. 2026: „žádnou lištu nechci“):
   GA4 měří standardně, tj. analytics_storage = granted, aby se data
   v přehledech opravdu objevila. Reklamní soubory zůstávají vypnuté
   (ad_storage / ad_user_data / ad_personalization = denied), takže
   nevzniká _gcl_* ani nic pro reklamu — jen měřicí cookies _ga a _ga_<ID>.

   Pozor na dvě věci, které se u GA4 pletou:
   1) analytics_storage "denied" NEznamená „měřím bez cookies“ — GA4 pak
      pošle jen cookieless ping (gcs=G100) a ten se v přehledech neukáže.
      Proto je tu granted.
   2) client_storage:"none" ani cookie_domain:"none" zápis _ga nezabrání
      (ověřeno v prohlížeči 17. 10. 2026) — s granted se cookies zapíšou
      vždy. Držíme je proto krátce (395 dní) a bez reklamních příznaků.

   Matomo na vlastním serveru běží dál bez cookies (assets/matomo.js) a je
   zdrojem čísel o unikátních návštěvnících napříč dny. */
(function () {
  "use strict";

  var ID = "G-F3JXCFBDNF";
  var TRINACT_MESICU = 395 * 24 * 60 * 60; // 395 dní ≈ 13 měsíců

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  // Kdyby gtag nastavil už někdo jiný (např. doplněk), nepřepisujeme ho.
  window.gtag = window.gtag || gtag;

  gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: "granted"
  });
  gtag("js", new Date());
  gtag("config", ID, {
    cookie_expires: TRINACT_MESICU,
    cookie_flags: "SameSite=Lax;Secure"
  });

  // Vlastní načtení gtag.js až odsud — v HTML tak zůstává jediný řádek.
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + ID;
  (document.head || document.documentElement).appendChild(s);
})();
