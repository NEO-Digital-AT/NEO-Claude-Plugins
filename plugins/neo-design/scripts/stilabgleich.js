/*
 * NEO-Stilabgleich: findet erfundene Werte in einer laufenden Oberflaeche.
 *
 * Das Bild sagt, DASS etwas anders aussieht. Diese Pruefung sagt, WARUM:
 * sie liest die berechneten Stile jedes Elements und meldet jede Farbe, jeden
 * Radius, jede Schriftgroesse und jeden Schatten, der nicht aus den Tokens
 * stammt. Sie arbeitet am fertigen DOM und ist damit unabhaengig davon, ob
 * React, Vue, Angular oder etwas anderes dahintersteht.
 *
 * Einbinden (Playwright):
 *   await page.addScriptTag({ path: '<plugin>/scripts/stilabgleich.js' })
 *   const bericht = await page.evaluate(() => neoStilabgleich.pruefen())
 *
 * Ohne Angabe von Tokens werden sie aus den CSS-Eigenschaften der Wurzel
 * gelesen (--neo-*, --leoflex-* oder ein eigenes Praefix). Wer eine
 * tokens.json hat, uebergibt sie stattdessen.
 */
(function () {
  'use strict'

  var GEPRUEFT = {
    farbe: ['color', 'backgroundColor', 'borderTopColor', 'borderRightColor',
            'borderBottomColor', 'borderLeftColor', 'outlineColor', 'fill', 'stroke'],
    radius: ['borderTopLeftRadius', 'borderTopRightRadius',
             'borderBottomRightRadius', 'borderBottomLeftRadius'],
    schriftgroesse: ['fontSize'],
    schatten: ['boxShadow'],
  }

  /** Normalisiert eine Farbangabe auf "r,g,b,a" — Hex, rgb() und rgba(). */
  function farbe (wert) {
    if (!wert) return null
    var t = String(wert).trim().toLowerCase()
    if (t === 'transparent' || t === 'none') return 'durchsichtig'
    var m = t.match(/^rgba?\(([^)]+)\)$/)
    if (m) {
      var teile = m[1].replace(/\//g, ' ').split(/[\s,]+/).filter(Boolean)
      var a = teile.length > 3 ? parseFloat(teile[3]) : 1
      if (a === 0) return 'durchsichtig'
      return [Math.round(parseFloat(teile[0])), Math.round(parseFloat(teile[1])),
              Math.round(parseFloat(teile[2])), Math.round(a * 100) / 100].join(',')
    }
    var h = t.replace('#', '')
    if (/^[0-9a-f]{3,8}$/.test(h)) {
      if (h.length === 3 || h.length === 4) h = h.split('').map(function (z) { return z + z }).join('')
      var a2 = h.length === 8 ? parseInt(h.slice(6, 8), 16) / 255 : 1
      if (a2 === 0) return 'durchsichtig'
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16),
              parseInt(h.slice(4, 6), 16), Math.round(a2 * 100) / 100].join(',')
    }
    return t
  }

  /** Rundet Laengen auf zwei Nachkommastellen, damit 10px und 10.0001px gleich sind. */
  function laenge (wert) {
    var z = parseFloat(wert)
    return isNaN(z) ? String(wert).trim() : Math.round(z * 100) / 100 + 'px'
  }

  /** Liest die Tokens aus den CSS-Eigenschaften der Wurzel. */
  function tokensAusWurzel (praefixe) {
    var erlaubt = { farbe: {}, radius: {}, schriftgroesse: {}, schatten: {} }
    var stil = getComputedStyle(document.documentElement)
    var namen = []
    for (var i = 0; i < stil.length; i++) {
      var n = stil[i]
      if (n.indexOf('--') !== 0) continue
      if (praefixe.length && !praefixe.some(function (p) { return n.indexOf(p) === 0 })) continue
      namen.push(n)
    }
    // Laengen nach ihrer Verwendung trennen: ein Radius-Token darf keine
    // Schriftgroesse legitimieren. Erkannt wird am Tokennamen; sagt der Name
    // nichts, landet der Wert in beiden Toepfen, damit fremde Benennungen
    // nicht zu einer Flut von Fehlfunden fuehren.
    var istRadius = /radius|rounded|corner|ecke/
    var istSchrift = /font-?size|text|schrift|heading|title|body|caption|label|lead/
    var laengen = []
    namen.forEach(function (n) {
      var w = stil.getPropertyValue(n).trim()
      if (!w) return
      var f = farbe(w)
      if (f && f !== w.toLowerCase()) erlaubt.farbe[f] = n
      if (/^-?\d*\.?\d+(px|rem|em)$/.test(w)) laengen.push([n, laenge(w)])
      if (/(inset|\d+px)\s+.*(rgba?|#)/.test(w)) erlaubt.schatten[w] = n
    })
    var benannteRadien = laengen.some(function (l) { return istRadius.test(l[0]) })
    var benannteSchriften = laengen.some(function (l) { return istSchrift.test(l[0]) })
    laengen.forEach(function (l) {
      var name = l[0], wert = l[1]
      var r = istRadius.test(name), s = istSchrift.test(name)
      if (r || (!benannteRadien && !s)) erlaubt.radius[wert] = name
      if (s || (!benannteSchriften && !r)) erlaubt.schriftgroesse[wert] = name
    })
    return { erlaubt: erlaubt, anzahl: namen.length }
  }

  /** Kurzer, lesbarer Pfad zu einem Element. */
  function pfad (el) {
    var teile = []
    while (el && el.nodeType === 1 && teile.length < 4) {
      var s = el.tagName.toLowerCase()
      if (el.id) { teile.unshift(s + '#' + el.id); break }
      var k = (el.getAttribute('class') || '').trim().split(/\s+/).filter(Boolean)[0]
      if (k) s += '.' + k
      teile.unshift(s)
      el = el.parentElement
    }
    return teile.join(' > ')
  }

  var api = {
    /**
     * @param {{tokens?:object, praefixe?:string[], wurzel?:Element,
     *          ignorieren?:string, abstaende?:boolean}} [opt]
     */
    pruefen: function (opt) {
      opt = opt || {}
      var praefixe = opt.praefixe || ['--neo-', '--leoflex-']
      var quelle = opt.tokens
        ? { erlaubt: opt.tokens, anzahl: -1 }
        : tokensAusWurzel(praefixe)
      var erlaubt = quelle.erlaubt
      var wurzel = opt.wurzel || document.body
      var ignorieren = opt.ignorieren || '[data-neo-abgleich="aus"]'
      if (opt.abstaende) {
        GEPRUEFT.abstand = ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
                            'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
                            'rowGap', 'columnGap']
      }

      var funde = []
      var gezaehlt = 0
      var elemente = [wurzel].concat(Array.prototype.slice.call(wurzel.querySelectorAll('*')))

      elemente.forEach(function (el) {
        if (el.closest && el.closest(ignorieren)) return
        var tag = el.tagName.toLowerCase()
        if (tag === 'script' || tag === 'style' || tag === 'noscript') return
        var stil = getComputedStyle(el)
        gezaehlt++

        var imSvg = !!(el.ownerSVGElement || tag === 'svg')
        var hatEigenenText = Array.prototype.some.call(el.childNodes, function (k) {
          return k.nodeType === 3 && k.nodeValue.trim().length > 0
        })

        // Eine Eigenschaft wird nur geprueft, wenn sie an diesem Element
        // ueberhaupt etwas zeichnet. Sonst meldet der Prueferstandardwerte,
        // die niemand gesetzt hat.
        function zeichnet (eig) {
          if (eig === 'fill' || eig === 'stroke') return imSvg
          if (eig === 'color') return hatEigenenText || imSvg
          if (eig === 'outlineColor') {
            return stil.outlineStyle !== 'none' && parseFloat(stil.outlineWidth) > 0
          }
          var rand = eig.match(/^border(Top|Right|Bottom|Left)Color$/)
          if (rand) {
            var seite = rand[1]
            return stil['border' + seite + 'Style'] !== 'none'
                && parseFloat(stil['border' + seite + 'Width']) > 0
          }
          return true
        }

        Object.keys(GEPRUEFT).forEach(function (art) {
          GEPRUEFT[art].forEach(function (eig) {
            if (!zeichnet(eig)) return
            var roh = stil[eig]
            if (!roh || roh === 'none' || roh === 'normal' || roh === 'auto') return
            var wert = art === 'farbe' ? farbe(roh)
                     : art === 'schatten' ? String(roh).trim()
                     : laenge(roh)
            if (wert === 'durchsichtig' || wert === '0px') return
            if (erlaubt[art] && Object.prototype.hasOwnProperty.call(erlaubt[art], wert)) return
            funde.push({ art: art, eigenschaft: eig, wert: String(roh).trim(),
                         normalisiert: wert, element: pfad(el) })
          })
        })
      })

      // Nach Wert buendeln: ein falscher Wert an dreissig Stellen ist ein Fund.
      var nachWert = {}
      funde.forEach(function (f) {
        var s = f.art + '|' + f.normalisiert
        if (!nachWert[s]) nachWert[s] = { art: f.art, wert: f.wert,
                                          normalisiert: f.normalisiert,
                                          eigenschaften: {}, anzahl: 0, beispiele: [] }
        nachWert[s].anzahl++
        nachWert[s].eigenschaften[f.eigenschaft] = true
        if (nachWert[s].beispiele.length < 3) nachWert[s].beispiele.push(f.element)
      })
      var gebuendelt = Object.keys(nachWert).map(function (s) {
        var e = nachWert[s]
        e.eigenschaften = Object.keys(e.eigenschaften)
        return e
      }).sort(function (a, b) { return b.anzahl - a.anzahl })

      return {
        elemente: gezaehlt,
        tokenquelle: opt.tokens ? 'uebergeben' : 'CSS-Eigenschaften der Wurzel',
        tokenanzahl: quelle.anzahl,
        erlaubteFarben: Object.keys(erlaubt.farbe || {}).length,
        funde: gebuendelt,
        gesamt: funde.length,
        bestanden: gebuendelt.length === 0,
      }
    },

    /** Bericht als Text, fuer die Ausgabe in der Konsole oder im Testlauf. */
    bericht: function (e) {
      var zeilen = []
      zeilen.push('Stilabgleich: ' + e.elemente + ' Elemente geprueft, Tokens aus '
                  + e.tokenquelle + (e.tokenanzahl >= 0 ? ' (' + e.tokenanzahl + ')' : ''))
      if (e.bestanden) {
        zeilen.push('Bestanden. Jeder sichtbare Wert stammt aus den Tokens.')
        return zeilen.join('\n')
      }
      zeilen.push(e.funde.length + ' erfundene Werte an ' + e.gesamt + ' Stellen:')
      e.funde.forEach(function (f) {
        zeilen.push('  ' + f.art.padEnd(15) + f.wert
                    + '   ' + f.anzahl + 'x  (' + f.eigenschaften.join(', ') + ')')
        zeilen.push('      z. B. ' + f.beispiele.join('  |  '))
      })
      return zeilen.join('\n')
    }
  }

  window.neoStilabgleich = api
})()
