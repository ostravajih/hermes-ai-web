/* Wiki — drobné vylepšení stránek wiki (15. 10. 2026)
   1) ke každému bloku s příkazem přidá tlačítko „Kopírovat"
   2) na telefonu sbalí obsah wiki (na počítači zůstává otevřený)  */
(function () {
  'use strict';

  function pripravKopirovani() {
    var bloky = document.querySelectorAll('.wiki-layout .code-block');
    Array.prototype.forEach.call(bloky, function (blok) {
      if (blok.parentNode && blok.parentNode.classList.contains('kod')) return;
      var obal = document.createElement('div');
      obal.className = 'kod';
      blok.parentNode.insertBefore(obal, blok);
      obal.appendChild(blok);

      var tlacitko = document.createElement('button');
      tlacitko.type = 'button';
      tlacitko.className = 'kod-kopiruj';
      tlacitko.textContent = 'Kopírovat';
      tlacitko.setAttribute('aria-label', 'Zkopírovat příkaz');
      tlacitko.addEventListener('click', function () {
        // text bez znaku „$" na začátku řádku, aby se dal rovnou vložit do terminálu
        var text = (blok.innerText || blok.textContent || '')
          .split('\n')
          .map(function (radek) { return radek.replace(/^\s*\$\s?/, '').trim(); })
          .filter(function (radek) { return radek.length > 0; })
          .join('\n');
        var hotovo = function () {
          tlacitko.textContent = 'Zkopírováno ✓';
          tlacitko.classList.add('kod-kopiruj--hotovo');
          setTimeout(function () {
            tlacitko.textContent = 'Kopírovat';
            tlacitko.classList.remove('kod-kopiruj--hotovo');
          }, 1800);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(hotovo, function () { vyber(text); hotovo(); });
        } else {
          vyber(text);
          hotovo();
        }
      });
      obal.appendChild(tlacitko);
    });
  }

  // záložní cesta pro starší prohlížeče a HTTP
  function vyber(text) {
    var pole = document.createElement('textarea');
    pole.value = text;
    pole.setAttribute('readonly', '');
    pole.style.position = 'absolute';
    pole.style.left = '-9999px';
    document.body.appendChild(pole);
    pole.select();
    try { document.execCommand('copy'); } catch (e) { /* nic se neděje */ }
    document.body.removeChild(pole);
  }

  function sbalObsahNaTelefonu() {
    var obsah = document.querySelector('.wiki-obsah');
    if (obsah && window.innerWidth <= 900) obsah.removeAttribute('open');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { pripravKopirovani(); sbalObsahNaTelefonu(); });
  } else {
    pripravKopirovani();
    sbalObsahNaTelefonu();
  }
})();
