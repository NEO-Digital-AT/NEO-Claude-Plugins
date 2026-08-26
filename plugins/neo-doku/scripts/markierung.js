/*
 * NEO-Markierungsebene für Doku-Screenshots.
 *
 * Wird vor der Aufnahme in die Seite eingeblendet und mitfotografiert. Die
 * Markierungen sind damit vektorscharf, auf jedem Zoom lesbar und liegen exakt
 * an den Elementen, statt an geratenen Pixelkoordinaten.
 *
 * Einbinden (Playwright):
 *   await page.addScriptTag({ path: 'tools/markierung.js' })
 *   await page.evaluate(() => {
 *     neoMarkierung.rahmen('[data-test="monitor-anlegen"]', { nummer: 1 })
 *     neoMarkierung.pfeil('#speichern', { text: 'Speichern nicht vergessen' })
 *     neoMarkierung.infokasten({ text: 'Das Intervall gilt je Monitor.', an: '#intervall' })
 *   })
 *   await page.screenshot({ path: '...', fullPage: true })
 *
 * Die Farben sind bewusst fest und folgen nicht dem Theme: eine Markierung ist
 * eine Markierung und muss auf hellem wie dunklem Grund gleich lesbar sein.
 * Deshalb trägt jede Form eine weiße Fassung unter dem Rot.
 */
(function () {
  'use strict'

  var ROT = '#E11D2E'
  var WEISS = '#FFFFFF'
  var TINTE = '#1A1A1A'
  var MARKER = 'rgba(255, 214, 0, 0.45)'
  var SCHRIFT = '600 14px/1.4 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'
  var EBENE_ID = 'neo-markierungsebene'

  function ebene () {
    var vorhanden = document.getElementById(EBENE_ID)
    if (vorhanden) return vorhanden
    var el = document.createElement('div')
    el.id = EBENE_ID
    // Am Wurzelelement: absolute Kinder liegen dann im Dokumentkoordinatensystem.
    el.style.cssText = 'position:absolute;left:0;top:0;width:0;height:0;' +
      'z-index:2147483647;pointer-events:none;'
    document.documentElement.appendChild(el)
    return el
  }

  /** Dokumentkoordinaten eines Elements. */
  function masse (ziel) {
    var el = typeof ziel === 'string' ? document.querySelector(ziel) : ziel
    if (!el) throw new Error('neoMarkierung: kein Element für "' + ziel + '"')
    var r = el.getBoundingClientRect()
    return {
      x: r.left + window.scrollX,
      y: r.top + window.scrollY,
      breite: r.width,
      hoehe: r.height,
      el: el
    }
  }

  function alleMasse (ziel, alle) {
    if (typeof ziel !== 'string') return [masse(ziel)]
    if (!alle) return [masse(ziel)]
    var liste = Array.prototype.slice.call(document.querySelectorAll(ziel))
    if (!liste.length) throw new Error('neoMarkierung: kein Element für "' + ziel + '"')
    return liste.map(masse)
  }

  function kasten (stil) {
    var el = document.createElement('div')
    el.style.cssText = 'position:absolute;box-sizing:border-box;' + stil
    ebene().appendChild(el)
    return el
  }

  function svg (x, y, breite, hoehe) {
    var el = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
    el.setAttribute('width', String(breite))
    el.setAttribute('height', String(hoehe))
    el.setAttribute('viewBox', '0 0 ' + breite + ' ' + hoehe)
    el.style.cssText = 'position:absolute;left:' + x + 'px;top:' + y + 'px;overflow:visible;'
    ebene().appendChild(el)
    return el
  }

  function linie(el, d, farbe, staerke) {
    var pfad = document.createElementNS('http://www.w3.org/2000/svg', 'path')
    pfad.setAttribute('d', d)
    pfad.setAttribute('fill', 'none')
    pfad.setAttribute('stroke', farbe)
    pfad.setAttribute('stroke-width', String(staerke))
    pfad.setAttribute('stroke-linecap', 'round')
    pfad.setAttribute('stroke-linejoin', 'round')
    el.appendChild(pfad)
    return pfad
  }

  /** Nummernmarke als Kreis, weiß gefasst. */
  function marke (x, y, nummer) {
    var d = 26
    var el = kasten(
      'left:' + (x - d / 2) + 'px;top:' + (y - d / 2) + 'px;width:' + d + 'px;height:' + d + 'px;' +
      'border-radius:50%;background:' + ROT + ';color:' + WEISS + ';' +
      'box-shadow:0 0 0 3px ' + WEISS + ', 0 1px 4px rgba(0,0,0,.35);' +
      'font:700 14px/' + d + 'px system-ui,sans-serif;text-align:center;')
    el.textContent = String(nummer)
    return el
  }

  var api = {
    /**
     * Roter Rahmen um ein Element, wahlweise mit Nummernmarke und Beschriftung.
     * @param {string|Element} ziel
     * @param {{nummer?:number, text?:string, luft?:number, alle?:boolean}} [opt]
     */
    rahmen: function (ziel, opt) {
      opt = opt || {}
      var luft = opt.luft == null ? 6 : opt.luft
      alleMasse(ziel, opt.alle).forEach(function (m) {
        kasten(
          'left:' + (m.x - luft) + 'px;top:' + (m.y - luft) + 'px;' +
          'width:' + (m.breite + luft * 2) + 'px;height:' + (m.hoehe + luft * 2) + 'px;' +
          'border:3px solid ' + ROT + ';border-radius:6px;' +
          'box-shadow:0 0 0 2px rgba(255,255,255,.9), inset 0 0 0 2px rgba(255,255,255,.9);')
        if (opt.nummer != null) marke(m.x - luft, m.y - luft, opt.nummer)
        if (opt.text) api.infokasten({ text: opt.text, an: m.el, position: 'unten' })
      })
      return api
    },

    /**
     * Roter Pfeil, der auf ein Element zeigt.
     * @param {string|Element} ziel
     * @param {{richtung?:'links'|'rechts'|'oben'|'unten', laenge?:number, text?:string}} [opt]
     */
    pfeil: function (ziel, opt) {
      opt = opt || {}
      var m = masse(ziel)
      var richtung = opt.richtung || (m.x > 220 ? 'links' : 'rechts')
      var laenge = opt.laenge == null ? 110 : opt.laenge
      var spitzeX, spitzeY, startX, startY
      var abstand = 10

      if (richtung === 'links') {
        spitzeX = m.x - abstand; spitzeY = m.y + m.hoehe / 2
        startX = spitzeX - laenge; startY = spitzeY - laenge * 0.35
      } else if (richtung === 'rechts') {
        spitzeX = m.x + m.breite + abstand; spitzeY = m.y + m.hoehe / 2
        startX = spitzeX + laenge; startY = spitzeY - laenge * 0.35
      } else if (richtung === 'oben') {
        spitzeX = m.x + m.breite / 2; spitzeY = m.y - abstand
        startX = spitzeX + laenge * 0.35; startY = spitzeY - laenge
      } else {
        spitzeX = m.x + m.breite / 2; spitzeY = m.y + m.hoehe + abstand
        startX = spitzeX + laenge * 0.35; startY = spitzeY + laenge
      }

      var flaeche = svg(0, 0, 1, 1)
      var mittelX = (startX + spitzeX) / 2 + (spitzeY - startY) * 0.12
      var mittelY = (startY + spitzeY) / 2 + (startX - spitzeX) * 0.12
      var d = 'M ' + startX + ' ' + startY + ' Q ' + mittelX + ' ' + mittelY +
              ' ' + spitzeX + ' ' + spitzeY
      linie(flaeche, d, WEISS, 9)   // Fassung, damit der Pfeil auf jedem Grund trägt
      linie(flaeche, d, ROT, 4)

      // Spitze aus der Tangente am Endpunkt
      var winkel = Math.atan2(spitzeY - mittelY, spitzeX - mittelX)
      var k = 15
      var p1 = [spitzeX - k * Math.cos(winkel - 0.42), spitzeY - k * Math.sin(winkel - 0.42)]
      var p2 = [spitzeX - k * Math.cos(winkel + 0.42), spitzeY - k * Math.sin(winkel + 0.42)]
      var spitze = 'M ' + p1[0] + ' ' + p1[1] + ' L ' + spitzeX + ' ' + spitzeY +
                   ' L ' + p2[0] + ' ' + p2[1] + ' Z'
      var f = document.createElementNS('http://www.w3.org/2000/svg', 'path')
      f.setAttribute('d', spitze)
      f.setAttribute('fill', ROT)
      f.setAttribute('stroke', WEISS)
      f.setAttribute('stroke-width', '3')
      f.setAttribute('paint-order', 'stroke')
      flaeche.appendChild(f)

      if (opt.text) {
        var k2 = kasten(
          'left:' + startX + 'px;top:' + startY + 'px;max-width:260px;' +
          'transform:translate(' + (richtung === 'links' ? '-100%' : '0') + ', -120%);' +
          'padding:6px 10px;border-radius:6px;background:' + ROT + ';color:' + WEISS + ';' +
          'box-shadow:0 0 0 2px ' + WEISS + ';font:' + SCHRIFT + ';')
        k2.textContent = opt.text
      }
      return api
    },

    /** Nummernmarke ohne Rahmen, an der oberen linken Ecke des Elements. */
    nummer: function (ziel, n) {
      var m = masse(ziel)
      marke(m.x, m.y, n)
      return api
    },

    /**
     * Infokasten mit Text, wahlweise an einem Element ausgerichtet.
     * @param {{text:string, an?:string|Element, position?:'oben'|'unten'|'links'|'rechts', breite?:number}} opt
     */
    infokasten: function (opt) {
      var breite = opt.breite || 300
      var x = 24, y = 24
      var position = opt.position || 'unten'
      if (opt.an) {
        var m = masse(opt.an)
        if (position === 'oben') { x = m.x; y = m.y - 16 }
        else if (position === 'links') { x = m.x - breite - 16; y = m.y }
        else if (position === 'rechts') { x = m.x + m.breite + 16; y = m.y }
        else { x = m.x; y = m.y + m.hoehe + 12 }
      }
      var el = kasten(
        'left:' + Math.max(8, x) + 'px;top:' + Math.max(8, y) + 'px;width:' + breite + 'px;' +
        (position === 'oben' ? 'transform:translateY(-100%);' : '') +
        'padding:10px 12px;border:2px solid ' + ROT + ';border-left-width:6px;border-radius:8px;' +
        'background:' + WEISS + ';color:' + TINTE + ';' +
        'box-shadow:0 2px 10px rgba(0,0,0,.25);font:' + SCHRIFT + ';white-space:pre-wrap;')
      el.textContent = opt.text
      return api
    },

    /**
     * Textmarker über den Textzeilen eines Elements.
     *
     * Gerechnet wird über einen Bereich (Range) und dessen Zeilenkästen, nicht
     * über den Rahmen des Elements: sonst zöge sich der Marker bei einer
     * Überschrift über die ganze Spaltenbreite statt über das Wort.
     */
    marker: function (ziel, opt) {
      opt = opt || {}
      alleMasse(ziel, opt.alle).forEach(function (m) {
        var kaesten = []
        try {
          var bereich = document.createRange()
          bereich.selectNodeContents(m.el)
          kaesten = Array.prototype.slice.call(bereich.getClientRects())
          bereich.detach && bereich.detach()
        } catch (e) { kaesten = [] }
        if (!kaesten.length) {
          kaesten = [{ left: m.x - window.scrollX, top: m.y - window.scrollY,
                       width: m.breite, height: m.hoehe }]
        }
        kaesten.forEach(function (r) {
          if (r.width < 1 || r.height < 1) return
          kasten(
            'left:' + (r.left + window.scrollX - 2) + 'px;' +
            'top:' + (r.top + window.scrollY - 1) + 'px;' +
            'width:' + (r.width + 4) + 'px;height:' + (r.height + 2) + 'px;' +
            'background:' + MARKER + ';mix-blend-mode:multiply;border-radius:3px;')
        })
      })
      return api
    },

    /** Alles außer dem Ziel abdunkeln. */
    scheinwerfer: function (ziel, opt) {
      opt = opt || {}
      var luft = opt.luft == null ? 8 : opt.luft
      var m = masse(ziel)
      var breite = Math.max(document.documentElement.scrollWidth, window.innerWidth)
      var hoehe = Math.max(document.documentElement.scrollHeight, window.innerHeight)
      var dunkel = opt.staerke == null ? 0.55 : opt.staerke
      var teile = [
        [0, 0, breite, m.y - luft],
        [0, m.y + m.hoehe + luft, breite, hoehe - (m.y + m.hoehe + luft)],
        [0, m.y - luft, m.x - luft, m.hoehe + luft * 2],
        [m.x + m.breite + luft, m.y - luft, breite - (m.x + m.breite + luft), m.hoehe + luft * 2]
      ]
      teile.forEach(function (t) {
        if (t[2] <= 0 || t[3] <= 0) return
        kasten('left:' + t[0] + 'px;top:' + t[1] + 'px;width:' + t[2] + 'px;height:' + t[3] +
               'px;background:rgba(0,0,0,' + dunkel + ');')
      })
      return api
    },

    /** Ausschnitt für einen Detailscreenshot: Dokumentkoordinaten des Elements. */
    ausschnitt: function (ziel, luft) {
      var l = luft == null ? 12 : luft
      var m = masse(ziel)
      return { x: m.x - l, y: m.y - l, width: m.breite + l * 2, height: m.hoehe + l * 2 }
    },

    /** Entfernt alle Markierungen. */
    aufraeumen: function () {
      var el = document.getElementById(EBENE_ID)
      if (el) el.remove()
      return api
    }
  }

  window.neoMarkierung = api
})()
