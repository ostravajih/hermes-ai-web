/* Google Analytics 4 – hermes-ai.cz
   Nasazeno 2026-10-17. Společný soubor pro všechny stránky webu; vkládá se
   přes <script defer src="/assets/ga4.js?v=..."></script> před </head>
   (hned za matomo.js).

   Měření bez cookies: GA4 se nastavuje s client_storage:"none" a se
   souhlasem "denied", takže do prohlížeče neukládá žádnou cookie ani
   položku v localStorage → web nepotřebuje souhlasovou lištu.
   Návštěvnost se tím počítá z cookieless signálů (GA4 je v tomto režimu
   modeluje), takže čísla berte jako orientační; přesná čísla dává Matomo
   na vlastním serveru, který běží ve stejném režimu bez cookies.

   Pozor: skript se načítá s defer, takže se spustí až po HTML. gtag.js
   (googletagmanager.com) se vkládá dynamicky, aby v hlavičce stačil jeden
   řádek a nemusel se na každé stránce opakovat blok s konfigurací. */
(function () {
  "use strict";

  var ID = "G-F3JXCFBDNF";

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  // Kdyby gtag nastavil už někdo jiný (např. doplněk), nepřepisujeme ho.
  window.gtag = window.gtag || gtag;

  // Bez cookies a bez reklamního profilování — stejné nastavení jako dřív
  // na pěti úvodních stránkách.
  gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: "denied"
  });
  gtag("js", new Date());
  gtag("config", ID, { client_storage: "none" });

  // Vlastní načtení gtag.js až odsud — v HTML tak zůstává jediný řádek.
  var s = document.createElement("script");
  s.async = true;
  s.src = "https://www.googletagmanager.com/gtag/js?id=" + ID;
  (document.head || document.documentElement).appendChild(s);
})();
