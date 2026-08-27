/*
 * NEO-Gegenueberstellung: Designsystem gegen Vorschlag, in einem Bild.
 *
 * Jede Abweichung vom Designsystem ist eine Rueckfrage an den
 * Projektinhaber, keine Entscheidung des Agenten — und eine Rueckfrage
 * ohne Bild ist keine. Dieses Werkzeug stellt beide Fassungen
 * nebeneinander, beschriftet, mit einem Hinweis, was sich unterscheidet.
 *
 * ACHTUNG bei den Bildquellen: eine Seite auf about:blank darf keine
 * file://-Bilder laden — der Browser blockt das. Entweder die Seite selbst
 * von einer file://-Adresse laden, oder die Bilder als data:-URI uebergeben:
 *
 *   const alsDatenUri = (pfad) =>
 *     'data:image/png;base64,' + fs.readFileSync(pfad).toString('base64')
 *
 * Laedt ein Bild nicht, meldet das Werkzeug es im Bild UND im Rueckgabewert
 * (`fehler`). Eine Rueckfrage mit fehlendem Bild ist keine Rueckfrage.
 *
 * Verwendung (Playwright):
 *   await seite.addScriptTag({ path: '<plugin>/scripts/gegenueberstellung.js' })
 *   const masse = await seite.evaluate(() => neoGegenueberstellung.zeigen({
 *     ueberschrift: 'Auftrag anlegen — Formularkarte',
 *     links:  { bild: 'file:///.../design.png',    titel: 'Designsystem' },
 *     rechts: { bild: 'file:///.../vorschlag.png', titel: 'Vorschlag' },
 *     hinweis: 'Rechts zwei Felder mehr. Karte, Abstaende und Feldhoehe unveraendert.'
 *   }))
 *   await seite.setViewportSize(masse)
 *   await seite.screenshot({ path: 'rueckfrage.png' })
 *
 * Die Farben sind fest: gruen fuer die Vorgabe, magenta fuer den
 * Vorschlag. Wer die Legende sucht, findet sie im Bild, nicht im Text
 * daneben.
 */
(function (global) {
  'use strict'

  var GRUEN = '#16A34A'
  var MAGENTA = '#E11D2E'
  var GRUND = '#F4F4F6'
  var FLAECHE = '#FFFFFF'
  var TINTE = '#17171A'
  var RAND = '#D9D9DE'
  var SCHRIFT = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'

  function el (tag, stil, text) {
    var e = document.createElement(tag)
    if (stil) e.style.cssText = stil
    if (text != null) e.textContent = text
    return e
  }

  var api = {
    /**
     * @param {{ueberschrift?:string, hinweis?:string, breite?:number,
     *          links:{bild:string,titel?:string,unterzeile?:string},
     *          rechts:{bild:string,titel?:string,unterzeile?:string}}} opt
     * @returns {Promise<{width:number,height:number}>}
     */
    zeigen: function (opt) {
      document.documentElement.style.cssText = 'margin:0;padding:0;'
      document.body.style.cssText =
        'margin:0;padding:24px;background:' + GRUND + ';color:' + TINTE +
        ';font:15px/1.5 ' + SCHRIFT + ';display:inline-block;'

      if (opt.ueberschrift) {
        document.body.appendChild(
          el('div', 'font:700 20px/1.3 ' + SCHRIFT + ';margin:0 0 4px;', opt.ueberschrift))
      }
      document.body.appendChild(
        el('div', 'font:13px/1.4 ' + SCHRIFT + ';color:#5C5C66;margin:0 0 16px;',
           'Links die Vorgabe aus dem Designsystem, rechts der Vorschlag. '
           + 'Die Entscheidung trifft der Projektinhaber.'))

      var reihe = el('div', 'display:flex;gap:20px;align-items:flex-start;')
      document.body.appendChild(reihe)

      var bilder = []
      var spalten = [
        { d: opt.links, farbe: GRUEN, standard: 'Designsystem' },
        { d: opt.rechts, farbe: MAGENTA, standard: 'Vorschlag' }
      ]

      spalten.forEach(function (s) {
        var spalte = el('div',
          'background:' + FLAECHE + ';border:1px solid ' + RAND + ';border-radius:10px;' +
          'overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.08);')
        var kopf = el('div',
          'background:' + s.farbe + ';color:#fff;padding:8px 14px;' +
          'font:700 14px/1.3 ' + SCHRIFT + ';')
        kopf.textContent = s.d.titel || s.standard
        spalte.appendChild(kopf)
        if (s.d.unterzeile) {
          spalte.appendChild(el('div',
            'padding:6px 14px;border-bottom:1px solid ' + RAND + ';' +
            'font:12px/1.4 ' + SCHRIFT + ';color:#5C5C66;', s.d.unterzeile))
        }
        var bild = document.createElement('img')
        bild.src = s.d.bild
        bild.style.cssText = 'display:block;max-width:' + (opt.breite || 720) + 'px;height:auto;'
        spalte.appendChild(bild)
        reihe.appendChild(spalte)
        bilder.push({ el: bild, spalte: spalte, quelle: s.d.bild })
      })

      if (opt.hinweis) {
        var kasten = el('div',
          'margin:18px 0 0;padding:12px 14px;background:' + FLAECHE + ';' +
          'border:1px solid ' + RAND + ';border-left:5px solid ' + MAGENTA + ';' +
          'border-radius:8px;font:14px/1.5 ' + SCHRIFT + ';max-width:960px;white-space:pre-wrap;')
        kasten.textContent = opt.hinweis
        document.body.appendChild(kasten)
      }

      return Promise.all(bilder.map(function (b) {
        return b.el.complete
          ? Promise.resolve()
          : new Promise(function (fertig) {
              b.el.addEventListener('load', fertig)
              b.el.addEventListener('error', fertig)
            })
      })).then(function () {
        return document.fonts && document.fonts.ready ? document.fonts.ready : null
      }).then(function () {
        // Ein nicht geladenes Bild wird sichtbar gemacht, nicht verschwiegen.
        var fehler = []
        bilder.forEach(function (b) {
          if (b.el.naturalWidth > 0) return
          fehler.push(b.quelle)
          b.el.remove()
          var warnung = el('div',
            'padding:24px;background:#FFF1F2;color:' + MAGENTA + ';max-width:420px;' +
            'font:700 14px/1.5 ' + SCHRIFT + ';border-top:1px solid ' + RAND + ';',
            'Bild nicht geladen.\n' + b.quelle +
            '\n\nfile://-Bilder brauchen eine file://-Seite oder eine data:-URI.')
          warnung.style.whiteSpace = 'pre-wrap'
          b.spalte.appendChild(warnung)
        })
        var r = document.body.getBoundingClientRect()
        return {
          width: Math.ceil(r.width), height: Math.ceil(r.height),
          fehler: fehler, brauchbar: fehler.length === 0
        }
      })
    }
  }

  global.neoGegenueberstellung = api
  if (typeof module !== 'undefined' && module.exports) module.exports = api
})(typeof window !== 'undefined' ? window : globalThis)
