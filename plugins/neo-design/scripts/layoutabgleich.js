/*
 * NEO-Layoutabgleich: vergleicht Geometrie und Aussehen, nicht den Inhalt.
 *
 * Ein Pixelvergleich schlaegt an, sobald in einem Feld ein anderer Wert steht.
 * Inhalte sind aber dynamisch — sie kommen aus der Datenbank, aus einer
 * Auswahlliste oder aus einer Fremd-API. Diese Pruefung misst deshalb das,
 * was das Designsystem tatsaechlich vorgibt: wie breit und hoch ein Feld ist,
 * wo es steht, welchen Abstand es haelt, welchen Radius, welche Randstaerke,
 * welche Schriftgroesse — und ob es sich in jedem Zustand so verhaelt.
 *
 * Der Text in den Feldern wird NICHT gelesen und NICHT verglichen.
 *
 * Messen (Playwright, je einmal fuer Entwurf und gebaute Ansicht):
 *   await seite.addScriptTag({ path: '<plugin>/scripts/layoutabgleich.js' })
 *   const messung = await seite.evaluate(() => neoLayoutabgleich.messen())
 *
 * Vergleichen (im Browser oder in Node, die Funktion braucht kein DOM):
 *   const e = neoLayoutabgleich.vergleichen(entwurf, gebaut, { toleranz: 1 })
 *   console.log(neoLayoutabgleich.bericht(e))
 */
(function (global) {
  'use strict'

  /* Zuordnung: bevorzugt ueber data-abgleich, sonst ueber Rolle plus Reihenfolge. */
  var MARKER = 'data-abgleich'

  var MASSE = ['breite', 'hoehe', 'x', 'y']
  var KASTEN = ['polsterOben', 'polsterRechts', 'polsterUnten', 'polsterLinks',
                'randOben', 'randRechts', 'randUnten', 'randLinks',
                'aussenOben', 'aussenUnten', 'luecke']
  var AUSSEHEN = ['radiusOL', 'radiusOR', 'radiusUR', 'radiusUL',
                  'schriftgroesse', 'zeilenhoehe', 'schriftstaerke', 'laufweite']
  var TEXTE = ['randfarbe', 'flaechenfarbe', 'schriftfarbe', 'schriftart',
               'schatten', 'ausrichtung', 'anzeige', 'richtung']

  /**
   * Der EIGENE Text eines Elements — nur die unmittelbaren Textknoten.
   * Eine Beschriftung und ein Knopftext werden damit erfasst, die Eintraege
   * einer Auswahlliste nicht: die stehen in Kindelementen und sind Inhalt,
   * nicht Gestaltung.
   */
  function eigenerText (el) {
    var t = ''
    for (var i = 0; i < el.childNodes.length; i++) {
      var k = el.childNodes[i]
      if (k.nodeType === 3) t += k.nodeValue
    }
    return t.replace(/\s+/g, ' ').trim()
  }

  function rund (z) { return Math.round(z * 2) / 2 }

  /** Grobe fachliche Rolle eines Elements — unabhaengig vom Framework. */
  function rolle (el) {
    var tag = el.tagName.toLowerCase()
    var aria = (el.getAttribute('role') || '').toLowerCase()
    if (aria) return aria
    if (tag === 'input') {
      var art = (el.getAttribute('type') || 'text').toLowerCase()
      if (art === 'checkbox' || art === 'radio') return art
      if (art === 'button' || art === 'submit' || art === 'reset') return 'knopf'
      return 'textfeld'
    }
    if (tag === 'textarea') return 'textbereich'
    if (tag === 'select') return 'auswahl'
    if (tag === 'button') return 'knopf'
    if (tag === 'a') return 'verweis'
    if (tag === 'label') return 'beschriftung'
    if (/^h[1-6]$/.test(tag)) return 'ueberschrift' + tag[1]
    if (tag === 'table') return 'tabelle'
    if (tag === 'img' || tag === 'svg') return 'bild'
    if (tag === 'form') return 'formular'
    if (tag === 'ul' || tag === 'ol') return 'liste'
    return null
  }

  function messwerte (el, ursprung) {
    var r = el.getBoundingClientRect()
    var s = getComputedStyle(el)
    var f = function (n) { return rund(parseFloat(s[n]) || 0) }
    return {
      breite: rund(r.width), hoehe: rund(r.height),
      x: rund(r.left - ursprung.left), y: rund(r.top - ursprung.top),
      polsterOben: f('paddingTop'), polsterRechts: f('paddingRight'),
      polsterUnten: f('paddingBottom'), polsterLinks: f('paddingLeft'),
      randOben: f('borderTopWidth'), randRechts: f('borderRightWidth'),
      randUnten: f('borderBottomWidth'), randLinks: f('borderLeftWidth'),
      aussenOben: f('marginTop'), aussenUnten: f('marginBottom'),
      luecke: f('rowGap'),
      radiusOL: f('borderTopLeftRadius'), radiusOR: f('borderTopRightRadius'),
      radiusUR: f('borderBottomRightRadius'), radiusUL: f('borderBottomLeftRadius'),
      schriftgroesse: f('fontSize'), zeilenhoehe: f('lineHeight'),
      schriftstaerke: parseInt(s.fontWeight, 10) || 400,
      laufweite: rund(parseFloat(s.letterSpacing) || 0),
      randfarbe: s.borderTopWidth === '0px' ? '-' : s.borderTopColor,
      flaechenfarbe: s.backgroundColor, schriftfarbe: s.color,
      schriftart: (s.fontFamily || '').split(',')[0].replace(/["']/g, '').trim(),
      schatten: s.boxShadow === 'none' ? '-' : s.boxShadow,
      ausrichtung: s.textAlign, anzeige: s.display,
      richtung: s.display.indexOf('flex') >= 0 ? s.flexDirection : '-'
    }
  }

  var api = {
    /**
     * @param {{wurzel?:Element, marker?:string, zustand?:string,
     *          nurMarkierte?:boolean, texte?:boolean}} [opt]
     *
     * `texte: true` erfasst zusaetzlich den eigenen Text jedes markierten
     * Elements. Das ist ausdruecklich abzuschalten gedacht: statische
     * Oberflaechentexte gehoeren zum Entwurf, dynamische Inhalte nicht.
     */
    messen: function (opt) {
      opt = opt || {}
      var wurzel = opt.wurzel || document.body
      var marker = opt.marker || MARKER
      var ursprung = wurzel.getBoundingClientRect()
      var alle = Array.prototype.slice.call(wurzel.querySelectorAll('*'))
      var zaehler = {}
      var elemente = []

      alle.forEach(function (el) {
        var s = getComputedStyle(el)
        if (s.display === 'none' || s.visibility === 'hidden') return
        var m = el.getAttribute(marker)
        var r = rolle(el)
        var schluessel
        if (m) {
          schluessel = m
        } else if (r && !opt.nurMarkierte) {
          zaehler[r] = (zaehler[r] || 0) + 1
          schluessel = r + '#' + zaehler[r]
        } else {
          return
        }
        // Einzelne Felder je Element ausnehmen, wo der Inhalt die Groesse
        // bestimmt und das so gewollt ist:
        //   <button data-abgleich="knopf-primaer" data-abgleich-ohne="breite">
        var ohne = (el.getAttribute(marker + '-ohne') || '')
          .split(',').map(function (t) { return t.trim() }).filter(Boolean)
        var eintrag = {
          schluessel: schluessel,
          markiert: !!m,
          rolle: r || 'unbekannt',
          ausnahmen: ohne,
          werte: messwerte(el, ursprung)
        }
        if (opt.texte) eintrag.text = eigenerText(el)
        elemente.push(eintrag)
      })

      return {
        zustand: opt.zustand || 'ruhe',
        mitTexten: !!opt.texte,
        sichtfeld: { breite: window.innerWidth, hoehe: window.innerHeight },
        wurzelmasse: { breite: rund(ursprung.width), hoehe: rund(ursprung.height) },
        markiert: elemente.filter(function (e) { return e.markiert }).length,
        elemente: elemente
      }
    },

    /**
     * Vergleicht zwei Messungen. Braucht kein DOM, laeuft auch in Node.
     * @param {{toleranz?:number, nurMarkierte?:boolean, texte?:boolean}} [opt]
     *
     * `texte: true` vergleicht zusaetzlich die statischen Oberflaechentexte.
     * Standard ist aus: Feldwerte und Listeneintraege sind dynamisch, und
     * eine Abweichung dort ist kein Mangel.
     */
    vergleichen: function (entwurf, gebaut, opt) {
      opt = opt || {}
      var toleranz = opt.toleranz == null ? 1 : opt.toleranz
      var index = {}
      gebaut.elemente.forEach(function (e) { index[e.schluessel] = e })

      var funde = []
      var fehlend = []
      var ohneText = []
      var paare = 0
      var versatzX = {}
      var versatzY = {}

      entwurf.elemente.forEach(function (a) {
        if (opt.nurMarkierte && !a.markiert) return
        var b = index[a.schluessel]
        if (!b) { fehlend.push(a.schluessel); return }
        paare++
        delete index[a.schluessel]

        var dx = b.werte.x - a.werte.x
        var dy = b.werte.y - a.werte.y
        versatzX[dx] = (versatzX[dx] || 0) + 1
        versatzY[dy] = (versatzY[dy] || 0) + 1

        var ausnahmen = (a.ausnahmen || []).concat(b.ausnahmen || [])
        MASSE.concat(KASTEN, AUSSEHEN).forEach(function (feld) {
          if (ausnahmen.indexOf(feld) >= 0) return
          var soll = a.werte[feld], ist = b.werte[feld]
          var d = Math.abs(ist - soll)
          if (d > toleranz) {
            funde.push({ schluessel: a.schluessel, rolle: a.rolle, feld: feld,
                         soll: soll, ist: ist, abweichung: rund(ist - soll),
                         gewicht: MASSE.indexOf(feld) >= 0 ? 3
                                : KASTEN.indexOf(feld) >= 0 ? 2 : 1 })
          }
        })
        TEXTE.forEach(function (feld) {
          if (ausnahmen.indexOf(feld) >= 0) return
          if (a.werte[feld] !== b.werte[feld]) {
            funde.push({ schluessel: a.schluessel, rolle: a.rolle, feld: feld,
                         soll: a.werte[feld], ist: b.werte[feld],
                         abweichung: null, gewicht: 1 })
          }
        })

        if (opt.texte && ausnahmen.indexOf('text') < 0) {
          if (a.text === undefined || b.text === undefined) {
            ohneText.push(a.schluessel)
          } else if (a.text !== b.text) {
            funde.push({ schluessel: a.schluessel, rolle: a.rolle, feld: 'text',
                         soll: a.text || '(leer)', ist: b.text || '(leer)',
                         abweichung: null, gewicht: 2 })
          }
        }
      })

      // Ein gleichmaessiger Versatz aller Elemente ist EIN Fund, nicht hundert.
      function haeufigster (v) {
        var best = null, n = 0
        Object.keys(v).forEach(function (k) { if (v[k] > n) { n = v[k]; best = parseFloat(k) } })
        return { wert: best, anteil: paare ? n / paare : 0 }
      }
      var gx = haeufigster(versatzX), gy = haeufigster(versatzY)
      var globalerVersatz = null
      if (paare >= 5 && gx.anteil >= 0.8 && gy.anteil >= 0.8
          && (Math.abs(gx.wert) > toleranz || Math.abs(gy.wert) > toleranz)) {
        globalerVersatz = { x: gx.wert, y: gy.wert, anteil: gx.anteil }
        funde = funde.filter(function (f) {
          if (f.feld === 'x') return Math.abs(f.abweichung - gx.wert) > toleranz
          if (f.feld === 'y') return Math.abs(f.abweichung - gy.wert) > toleranz
          return true
        })
      }

      funde.sort(function (a, b) {
        if (b.gewicht !== a.gewicht) return b.gewicht - a.gewicht
        return Math.abs(b.abweichung || 0) - Math.abs(a.abweichung || 0)
      })

      return {
        zustand: entwurf.zustand,
        toleranz: toleranz,
        texteVerglichen: !!opt.texte,
        paare: paare,
        fehlend: fehlend,
        ohneText: ohneText,
        zusaetzlich: Object.keys(index),
        globalerVersatz: globalerVersatz,
        funde: funde,
        bestanden: funde.length === 0 && fehlend.length === 0
                   && ohneText.length === 0 && !globalerVersatz
      }
    },

    bericht: function (e) {
      var z = []
      z.push('Layoutabgleich, Zustand "' + e.zustand + '": ' + e.paare
             + ' Elemente zugeordnet, Toleranz ' + e.toleranz + ' px'
             + (e.texteVerglichen ? ', Texte mitverglichen' : ''))
      if (e.ohneText && e.ohneText.length) {
        z.push('  Texte verlangt, aber nicht gemessen: ' + e.ohneText.join(', ')
               + ' — beide Messungen mit { texte: true } erzeugen.')
      }
      if (e.fehlend.length) {
        z.push('  Im Gebauten nicht gefunden: ' + e.fehlend.join(', '))
      }
      if (e.zusaetzlich.length) {
        z.push('  Im Entwurf nicht vorhanden: ' + e.zusaetzlich.join(', '))
      }
      if (e.globalerVersatz) {
        z.push('  Gleichmaessiger Versatz aller Elemente: x '
               + e.globalerVersatz.x + ' px, y ' + e.globalerVersatz.y
               + ' px — meist ein abweichender Aussenabstand der Wurzel.')
      }
      if (e.bestanden) {
        z.push('Bestanden. Masse, Abstaende und Aussehen decken sich mit dem Entwurf.')
        return z.join('\n')
      }
      if (e.funde.length) {
        // Dieselbe Abweichung an vielen Elementen ist EIN Fehler, meist ein
        // falscher Token. Sie wird gebuendelt, sonst erschlaegt der Bericht
        // die Ursache mit ihren Folgen.
        var buendel = {}
        var reihenfolge = []
        e.funde.forEach(function (f) {
          var s = f.feld + '|' + f.soll + '|' + f.ist
          if (!buendel[s]) {
            buendel[s] = { feld: f.feld, soll: f.soll, ist: f.ist,
                           abweichung: f.abweichung, gewicht: f.gewicht,
                           schluessel: [] }
            reihenfolge.push(s)
          }
          buendel[s].schluessel.push(f.schluessel)
        })
        z.push('  ' + reihenfolge.length + ' Abweichungen an '
               + e.funde.length + ' Stellen:')
        reihenfolge.forEach(function (s) {
          var f = buendel[s]
          var wert = f.abweichung === null
            ? f.ist + '   statt   ' + f.soll
            : f.ist + ' px  statt  ' + f.soll + ' px   ('
              + (f.abweichung > 0 ? '+' : '') + f.abweichung + ')'
          z.push('    ' + String(f.feld).padEnd(16) + wert)
          var wo = f.schluessel.length > 4
            ? f.schluessel.slice(0, 4).join(', ') + ' und '
              + (f.schluessel.length - 4) + ' weitere'
            : f.schluessel.join(', ')
          z.push('        ' + wo)
        })
      }
      return z.join('\n')
    }
  }

  global.neoLayoutabgleich = api
  if (typeof module !== 'undefined' && module.exports) module.exports = api
})(typeof window !== 'undefined' ? window : globalThis)
