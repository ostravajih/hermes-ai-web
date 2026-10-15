/* =============================================================================
   Oživení webu hermes-ai.cz — 15. 10. 2026
   Efekty: 1) síť bodů, která se spojuje s kurzorem myši (horní sekce)
           2) napočítávání čísel      3) světlo u kurzoru a náklon karet
           4) psací terminál na instalaci a na blocích s atributem data-vystup

   Zrušeno 15. 10. 2026 večer na přání vlastníka: posun obrázku podle myši (10)
   a prolití mezi stránkami (9) — obojí působilo jako další vrstva/blikání.

   ZÁSADY (kvůli opravě blikání z 15. 10. 2026):
   - používá se jen posuv a průhlednost → nikdy se nemění rozložení stránky;
   - skript běží až po načtení stránky → nemůže zdržet první vykreslení;
   - respektuje systémové nastavení „omezit pohyb“ a pauzuje se mimo obrazovku;
   - nic nenačítá z internetu (žádná knihovna, žádný obrázek navíc).
   ============================================================================= */
(function () {
  'use strict';

  var omezenyPohyb = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  /* efekty pro myš se na dotykových zařízeních vypínají; přes ?zive=1 se dají vynutit (na vyzkoušení) */
  var presnaMys = (window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches) || /[?&]zive=1/.test(location.search);
  var jeInstalace = /^\/(en\/)?(instalace|installation)\/?$/.test(location.pathname);
  /* poznámka: dřív se hledalo jen „instalace" kdekoli v adrese, takže se efekt chytal
     i na stránce wiki /wiki/zaciname/instalace/ a psal tam vymyšlený výstup. */
  var jazykCs = (document.documentElement.lang || 'cs').slice(0, 2) !== 'en';

  /* ------------------------------------------------ pomocné ------------------ */
  function kazdy(seznam, fn) { Array.prototype.forEach.call(seznam, fn); }

  function priVideti(prvek, fn, prah) {
    if (!('IntersectionObserver' in window)) { fn(); return null; }
    var io = new IntersectionObserver(function (zaznamy) {
      kazdy(zaznamy, function (z) {
        if (z.isIntersecting) { fn(); if (z.target.__ziveJednou) io.unobserve(z.target); }
      });
    }, { threshold: prah || 0.35 });
    io.observe(prvek);
    return io;
  }

  /* =========================================================== 1) AURORA + SÍŤ */
  function pozadiHorniSekce() {
    var sekce = document.querySelector('.hero--poster, .route-hero--poster');
    if (!sekce || sekce.querySelector('.zive-pozadi')) return;

    var obal = document.createElement('div');
    obal.className = 'zive-pozadi';
    obal.setAttribute('aria-hidden', 'true');
    sekce.insertBefore(obal, sekce.firstChild);

    if (omezenyPohyb) return;

    var platno = document.createElement('canvas');
    platno.className = 'zive-sit';
    obal.appendChild(platno);
    var ctx = platno.getContext('2d');
    if (!ctx) return;

    var body = [], sirka = 0, vyska = 0, bezet = false, znam = 0;
    var mys = { x: -9999, y: -9999, aktivni: false };
    var PRITAH = 200, ODPUD = 95, SPOJ = 132;

    function velikost() {
      var r = obal.getBoundingClientRect();
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      sirka = Math.max(1, Math.round(r.width));
      vyska = Math.max(1, Math.round(r.height));
      platno.width = Math.round(sirka * dpr);
      platno.height = Math.round(vyska * dpr);
      platno.style.width = sirka + 'px';
      platno.style.height = vyska + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var pocet = Math.max(16, Math.min(72, Math.round((sirka * vyska) / 13000)));
      body = [];
      for (var i = 0; i < pocet; i++) {
        body.push({
          x: Math.random() * sirka, y: Math.random() * vyska,
          vx: (Math.random() - 0.5) * 0.26, vy: (Math.random() - 0.5) * 0.26,
          r: 1.3 + Math.random() * 1.1
        });
      }
    }

    function kresli() {
      if (!bezet) return;
      znam = requestAnimationFrame(kresli);
      ctx.clearRect(0, 0, sirka, vyska);

      for (var i = 0; i < body.length; i++) {
        var b = body[i];

        /* reakce na myš: blízké body se rozestoupí a rozzáří */
        if (mys.aktivni) {
          var dx = b.x - mys.x, dy = b.y - mys.y, d = Math.sqrt(dx * dx + dy * dy);
          if (d < ODPUD && d > 0.01) {
            var sila = (1 - d / ODPUD) * 0.32;
            b.vx += (dx / d) * sila; b.vy += (dy / d) * sila;
          }
        }

        b.x += b.vx; b.y += b.vy;
        b.vx *= 0.995; b.vy *= 0.995;
        if (Math.random() < 0.004) { b.vx += (Math.random() - 0.5) * 0.16; b.vy += (Math.random() - 0.5) * 0.16; }
        if (b.x < 0 || b.x > sirka) b.vx *= -1;
        if (b.y < 0 || b.y > vyska) b.vy *= -1;
        b.x = Math.max(0, Math.min(sirka, b.x));
        b.y = Math.max(0, Math.min(vyska, b.y));
      }

      /* spojnice mezi body */
      for (var j = 0; j < body.length; j++) {
        var a = body[j];
        for (var k = j + 1; k < body.length; k++) {
          var c = body[k], vx = a.x - c.x, vy = a.y - c.y;
          var vzd = Math.sqrt(vx * vx + vy * vy);
          if (vzd < SPOJ) {
            var o = 0.34 * (1 - vzd / SPOJ);
            ctx.strokeStyle = 'rgba(0, 220, 235, ' + o.toFixed(3) + ')';
            ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(c.x, c.y); ctx.stroke();
          }
        }
      }

      /* spojnice ke kurzoru myši — to je ta viditelná reakce */
      if (mys.aktivni) {
        for (var n = 0; n < body.length; n++) {
          var p = body[n], mx = p.x - mys.x, my = p.y - mys.y;
          var md = Math.sqrt(mx * mx + my * my);
          if (md < PRITAH) {
            var mo = 0.85 * (1 - md / PRITAH);
            ctx.strokeStyle = 'rgba(120, 240, 255, ' + mo.toFixed(3) + ')';
            ctx.lineWidth = 1.15;
            ctx.beginPath(); ctx.moveTo(mys.x, mys.y); ctx.lineTo(p.x, p.y); ctx.stroke();
          }
        }
        var zare = ctx.createRadialGradient(mys.x, mys.y, 0, mys.x, mys.y, 76);
        zare.addColorStop(0, 'rgba(0, 220, 235, .17)');
        zare.addColorStop(1, 'rgba(0, 220, 235, 0)');
        ctx.fillStyle = zare;
        ctx.beginPath(); ctx.arc(mys.x, mys.y, 76, 0, 6.2832); ctx.fill();
      }

      /* body */
      for (var q = 0; q < body.length; q++) {
        var t = body[q], blizko = 0;
        if (mys.aktivni) {
          var tdx = t.x - mys.x, tdy = t.y - mys.y, td = Math.sqrt(tdx * tdx + tdy * tdy);
          blizko = td < PRITAH ? 1 - td / PRITAH : 0;
        }
        ctx.fillStyle = 'rgba(' + Math.round(140 + 60 * blizko) + ', 230, 255, ' + (0.5 + 0.45 * blizko).toFixed(2) + ')';
        ctx.beginPath(); ctx.arc(t.x, t.y, t.r + blizko * 1.5, 0, 6.2832); ctx.fill();
      }
    }

    function startKresleni() {
      if (bezet) return;
      bezet = true; kresli();
      /* síť se zjeví plynule, aby body „nenaskočily“ naráz při přechodu na stránku */
      setTimeout(function () { platno.classList.add('zive-videt'); }, 30);
    }
    function stopKresleni() { bezet = false; if (znam) cancelAnimationFrame(znam); znam = 0; }

    velikost();
    window.addEventListener('resize', velikost);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (z) {
        if (z[0].isIntersecting) { velikost(); startKresleni(); } else stopKresleni();
      }, { threshold: 0.05 }).observe(sekce);
    } else { startKresleni(); }
    document.addEventListener('visibilitychange', function () { if (document.hidden) stopKresleni(); else startKresleni(); });

    sekce.addEventListener('pointermove', function (e) {
      var r = obal.getBoundingClientRect();
      mys.x = e.clientX - r.left; mys.y = e.clientY - r.top; mys.aktivni = true;
    }, { passive: true });
    sekce.addEventListener('pointerleave', function () { mys.aktivni = false; mys.x = -9999; mys.y = -9999; });
  }

  /* ======================================================= 2) NAPOČÍTÁNÍ ČÍSEL */
  function napocitej(el) {
    var puvodni = el.textContent.trim();
    var shoda = puvodni.match(/^([^\d]*)(\d[\d\s\u00a0]*)(.*)$/);
    if (!shoda) return;
    var zaklad = shoda[1], cislo = parseInt(shoda[2].replace(/\D/g, ''), 10), konec = shoda[3];
    if (!isFinite(cislo) || cislo === 0) return;
    if (omezenyPohyb) return;
    var od = performance.now(), trvani = 1150;
    (function krok(nynejsi) {
      var p = Math.min(1, (nynejsi - od) / trvani);
      var e = 1 - Math.pow(1 - p, 3);
      el.textContent = zaklad + Math.round(cislo * e) + konec;
      if (p < 1) requestAnimationFrame(krok);
    })(od);
  }

  function ozivCisla() {
    var prvky = document.querySelectorAll('.hero--poster .stat strong, .route-hero--poster .stat strong, .stat-num');
    kazdy(prvky, function (el) {
      if (el.__ziveHotovo) return;
      el.__ziveJednou = true; el.__ziveHotovo = true;
      priVideti(el, function () { napocitej(el); }, 0.6);
    });
  }

  /* ================================== 3) SVĚTLO U KURZORU + NÁKLON KARET -------- */
  function ozivKarty() {
    var karty = document.querySelectorAll('.blog-card, .card, .bento-panel, .stat');
    kazdy(karty, function (k) {
      if (k.__ziveKarta) return;
      k.__ziveKarta = true;
      k.classList.add('zive-svetlo');
      var naklanet = presnaMys && !omezenyPohyb && (k.classList.contains('blog-card') || k.classList.contains('card'));

      k.addEventListener('pointermove', function (e) {
        var r = k.getBoundingClientRect();
        var x = e.clientX - r.left, y = e.clientY - r.top;
        k.style.setProperty('--zive-mx', x + 'px');
        k.style.setProperty('--zive-my', y + 'px');
        if (naklanet) {
          var rx = ((y / r.height) - 0.5) * -4;
          var ry = ((x / r.width) - 0.5) * 4;
          k.classList.add('zive-naklon');
          k.style.transform = 'perspective(900px) rotateX(' + rx.toFixed(2) + 'deg) rotateY(' + ry.toFixed(2) + 'deg) translateY(-2px)';
        }
      }, { passive: true });

      k.addEventListener('pointerleave', function () {
        if (naklanet) { k.style.transform = ''; k.classList.remove('zive-naklon'); }
      });
    });
  }

  /* ============================================ 4) PSACÍ TERMINÁL (instalace) */
  function psaciTerminal() {
    /* Které bloky se mají „napsat samy":
       - na stránce instalace první blok s příkazem (chování jako dosud),
       - kdekoli jinde jen blok, u kterého je v HTML řečeno, co příkaz opravdu vypíše
         (atribut data-vystup, řádky oddělené znakem |). Bez toho by efekt na jiné
         stránce ukazoval vymyšlený výstup a mátl by. */
    var bloky = [];
    if (jeInstalace) {
      var prvni = document.querySelector('.code-block');
      if (prvni) bloky.push(prvni);
    }
    kazdy(document.querySelectorAll('.code-block[data-vystup]'), function (b) {
      if (bloky.indexOf(b) < 0) bloky.push(b);
    });

    kazdy(bloky, function (blok) {
    if (!blok || blok.__ziveTerm) return;

    var html = blok.innerHTML;
    var konecSpanu = html.lastIndexOf('</span>');
    if (konecSpanu < 0) return;
    var predpona = html.slice(0, konecSpanu + 7);
    var prikaz = html.slice(konecSpanu + 7).replace(/\s+$/, '');
    if (prikaz.length < 12 || /[<>]/.test(prikaz)) return;
    blok.__ziveTerm = true;

    /* Vlastní výstup z HTML (data-vystup) má přednost — autor stránky ví, co příkaz vypíše */
    var vlastni = blok.getAttribute('data-vystup');
    var vystup = vlastni
      ? vlastni.split('|')
      : (jazykCs
          ? ['→ kontroluji systém…', '→ stahuji Hermes Agent…', '<b>✓ hotovo</b> — napište <code>hermes</code> a začněte']
          : ['→ checking system…', '→ downloading Hermes Agent…', '<b>✓ done</b> — type <code>hermes</code> to start']);

    function prehraj() {
      blok.innerHTML = predpona + '<span class="zive-psani"></span><span class="zive-kurzor"></span>';
      var psani = blok.querySelector('.zive-psani');
      var kurzor = blok.querySelector('.zive-kurzor');
      var i = 0;
      var stare = blok.parentElement.querySelector('.zive-vystup');
      if (stare) stare.remove();

      (function dalsi() {
        if (i <= prikaz.length) {
          psani.textContent = prikaz.slice(0, i++);
          setTimeout(dalsi, 24);
          return;
        }
        setTimeout(function () { if (kurzor) kurzor.style.display = 'none'; }, 1800);
        var obal = document.createElement('span');
        obal.className = 'zive-vystup';
        blok.appendChild(obal);
        vystup.forEach(function (radek, poradi) {
          setTimeout(function () {
            var radekEl = document.createElement('span');
            radekEl.innerHTML = radek;
            obal.appendChild(radekEl);
            requestAnimationFrame(function () { radekEl.classList.add('videt'); });
          }, 420 * (poradi + 1));
        });
      })();
    }

    priVideti(blok, prehraj, 0.4);
    blok.style.cursor = 'pointer';
    blok.addEventListener('click', prehraj);
    });
  }

  /* ======================================================== spuštění --------- */
  function start() {
    try { pozadiHorniSekce(); } catch (e) {}
    try { ozivCisla(); } catch (e) {}
    try { ozivKarty(); } catch (e) {}
    try { psaciTerminal(); } catch (e) {}
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
