/**
 * neoUeberlauf — misst, was auf einer Breite nicht in den Bildschirm passt.
 *
 * Wird vor der Messung in die laufende Seite eingeblendet und je Prüfbreite
 * aufgerufen. Geprüft wird sechserlei:
 *
 *   1. Seitenüberlauf   — der Körper scrollt waagrecht
 *   2. Über dem Rand    — ein Element ragt aus dem sichtbaren Bereich
 *   3. Über dem Eltern  — ein Element ist breiter als sein Platz
 *   4. Tabellen         — eine Tabelle nutzt nicht die Breite des Inhaltsbereichs
 *   5. Bedienziele      — ein Knopf ist zu klein für einen Finger
 *   6. Lücken           — eine umgebrochene Reihe lässt ein Loch stehen
 *
 * Der sechste ist der, den kein Standardwerkzeug prüft: drei Karten, die auf
 * zwei Spalten umbrechen, lassen in der zweiten Reihe die Hälfte frei. Die
 * Regel dagegen lautet: entweder einspaltig, oder das letzte Element füllt.
 *
 * Einbinden (Playwright):
 *   await page.addScriptTag({ path: 'tools/ueberlauf.js' })
 *   for (const breite of neoUeberlauf.BREITEN) {
 *     await page.setViewportSize({ width: breite, height: 900 })
 *     const b = await page.evaluate(() => neoUeberlauf.pruefen())
 *     expect(b.befunde, neoUeberlauf.bericht(b)).toHaveLength(0)
 *   }
 *
 * Ohne Abhängigkeiten, framework-unabhängig: gemessen wird das fertige DOM.
 */
;(function (welt) {
  'use strict'

  var BREITEN = [320, 390, 768, 1024, 1280, 1920, 2560, 3840]

  var VORGABE = {
    toleranz: 1,          // px, gegen Rundung im Layout
    zielSchmal: 44,       // Bedienziel bis 768 px — Finger, nicht Zeiger
    zielBreit: 24,        // Bedienziel darüber — WCAG 2.2 (2.5.8)
    schmalBis: 768,
    lueckeAb: 0.15,       // freier Anteil einer Reihe, ab dem es ein Loch ist
    hoechstensJeArt: 12,  // je Befundart berichten, sonst wird der Bericht unlesbar
    wurzel: null,
    inhaltsbereich: '[data-inhalt], main, [role="main"]'
  }

  var BEDIENBAR = 'a[href],button,input,select,textarea,summary,[role="button"],' +
    '[role="link"],[role="checkbox"],[role="radio"],[role="switch"],[role="tab"],' +
    '[role="menuitem"],[tabindex]:not([tabindex="-1"])'

  // ---------------------------------------------------------------- Helfer

  function sichtbar (el) {
    var s = getComputedStyle(el)
    if (s.display === 'none' || s.visibility === 'hidden' || s.visibility === 'collapse') return false
    if (parseFloat(s.opacity) === 0) return false
    var r = el.getBoundingClientRect()
    return r.width > 0 && r.height > 0
  }

  function pfad (el) {
    if (!el || el === document.documentElement) return 'html'
    var teile = []
    var k = el
    while (k && k.nodeType === 1 && teile.length < 4) {
      var t = k.tagName.toLowerCase()
      if (k.id) { teile.unshift(t + '#' + k.id); break }
      var marke = k.getAttribute('data-test') || k.getAttribute('data-abgleich')
      if (marke) { teile.unshift(t + '[' + marke + ']'); break }
      var klasse = (k.getAttribute('class') || '').trim().split(/\s+/)[0]
      teile.unshift(klasse ? t + '.' + klasse : t)
      k = k.parentElement
    }
    return teile.join(' > ')
  }

  function text (el) {
    var t = (el.getAttribute('aria-label') || el.textContent || '').trim()
    return t.length > 40 ? t.slice(0, 40) + '…' : t
  }

  function scrollbar (el) {
    var s = getComputedStyle(el).overflowX
    return s === 'auto' || s === 'scroll'
  }

  function inScrollbereich (el, wurzel) {
    for (var k = el.parentElement; k && k !== wurzel; k = k.parentElement) {
      if (scrollbar(k)) return true
    }
    return false
  }

  function innenbreite (el) {
    var s = getComputedStyle(el)
    return el.clientWidth -
      parseFloat(s.paddingLeft || 0) - parseFloat(s.paddingRight || 0)
  }

  // ------------------------------------------------------------- Prüfungen

  function pruefen (opt) {
    var o = {}
    for (var k in VORGABE) o[k] = VORGABE[k]
    for (var k2 in (opt || {})) o[k2] = opt[k2]

    var wurzel = o.wurzel ? document.querySelector(o.wurzel) : document.body
    if (!wurzel) return { fehler: 'Wurzel nicht gefunden: ' + o.wurzel, befunde: [] }

    var breite = document.documentElement.clientWidth
    var ziel = breite <= o.schmalBis ? o.zielSchmal : o.zielBreit
    var befunde = []
    var alle = Array.prototype.slice.call(wurzel.querySelectorAll('*'))
    var gemeldet = []

    function melden (art, el, was, zusatz) {
      var eintrag = { art: art, was: was, stelle: pfad(el), text: text(el) }
      for (var s in (zusatz || {})) eintrag[s] = zusatz[s]
      befunde.push(eintrag)
      gemeldet.push(el)
    }

    function schonGemeldet (el) {
      for (var i = 0; i < gemeldet.length; i++) {
        if (gemeldet[i] !== el && gemeldet[i].contains(el)) return true
      }
      return false
    }

    // 1. Seitenüberlauf
    var d = document.documentElement
    var ueberstand = d.scrollWidth - d.clientWidth
    if (ueberstand > o.toleranz) {
      befunde.push({
        art: 'seitenueberlauf',
        was: 'Der Körper scrollt waagrecht um ' + Math.round(ueberstand) + ' px',
        stelle: 'html', text: ''
      })
    }
    if (getComputedStyle(document.body).overflowX === 'hidden') {
      befunde.push({
        art: 'ueberlauf_versteckt',
        was: 'overflow-x: hidden am Körper versteckt den Fehler, statt ihn zu beheben',
        stelle: 'body', text: ''
      })
    }

    // 2. Über den sichtbaren Rand hinaus
    alle.forEach(function (el) {
      if (!sichtbar(el) || schonGemeldet(el)) return
      var r = el.getBoundingClientRect()
      if (inScrollbereich(el, wurzel)) return
      if (r.right > breite + o.toleranz) {
        melden('ueber_rand', el,
          'ragt ' + Math.round(r.right - breite) + ' px über den rechten Rand',
          { breite: Math.round(r.width) })
      } else if (r.left < -o.toleranz) {
        melden('ueber_rand', el,
          'beginnt ' + Math.round(-r.left) + ' px links außerhalb',
          { breite: Math.round(r.width) })
      }
    })

    // 3. Inhalt breiter als das Element, ohne dass es scrollen darf
    alle.forEach(function (el) {
      if (!sichtbar(el) || scrollbar(el) || schonGemeldet(el)) return
      var s = getComputedStyle(el)
      if (s.overflowX === 'hidden' || s.overflowX === 'clip') return
      var zuviel = el.scrollWidth - el.clientWidth
      if (zuviel > o.toleranz && el.clientWidth > 0) {
        melden('inhalt_zu_breit', el,
          'Inhalt ist ' + Math.round(zuviel) + ' px breiter als der Platz',
          { breite: Math.round(el.clientWidth) })
      }
    })

    // 4. Tabellen nutzen die Breite des Inhaltsbereichs
    //
    // Eine Tabelle in einem ausdrücklichen Scrollbereich darf breiter sein —
    // das ist die letzte, erlaubte Stufe der Rangfolge für schmale Geräte.
    // Zu schmal ist sie nie: das lässt eine Lücke stehen.
    var inhalt = document.querySelector(o.inhaltsbereich)
    Array.prototype.forEach.call(wurzel.querySelectorAll('table'), function (t) {
      if (!sichtbar(t)) return
      var bereich = t.closest('[data-tabellenbereich]')
      var darfScrollen = (bereich && scrollbar(bereich)) || inScrollbereich(t, wurzel)
      var bezug = bereich || inhalt || wurzel
      var soll = innenbreite(bezug)
      var ist = t.getBoundingClientRect().width
      if (soll <= 0) return
      if (ist < soll - 2) {
        melden('tabelle_zu_schmal', t,
          'nutzt ' + Math.round(ist) + ' von ' + Math.round(soll) + ' px der verfügbaren Breite',
          { fehlend: Math.round(soll - ist) })
      } else if (ist > soll + o.toleranz && !darfScrollen) {
        melden('tabelle_zu_breit', t,
          'ist ' + Math.round(ist - soll) + ' px breiter als der Inhaltsbereich und ' +
          'liegt in keinem Scrollbereich', {})
      }
    })

    // 5. Bedienziele
    var zuKlein = []
    Array.prototype.forEach.call(wurzel.querySelectorAll(BEDIENBAR), function (el) {
      if (!sichtbar(el) || el.disabled) return
      var r = el.getBoundingClientRect()
      var s = getComputedStyle(el)
      if (s.display === 'inline' && el.closest('p, li, td')) return   // Textlink im Fließtext
      if (r.width + 0.5 < ziel || r.height + 0.5 < ziel) {
        zuKlein.push({
          art: 'bedienziel_zu_klein',
          was: Math.round(r.width) + '×' + Math.round(r.height) +
               ' px, verlangt sind ' + ziel + '×' + ziel,
          stelle: pfad(el), text: text(el)
        })
      }
    })
    befunde = befunde.concat(zuKlein)

    // 6. Lücken in umgebrochenen Reihen
    alle.forEach(function (el) {
      if (!sichtbar(el)) return
      var s = getComputedStyle(el)
      var art = s.display
      if (art !== 'flex' && art !== 'grid' && art !== 'inline-flex') return
      if (art !== 'grid' && s.flexWrap === 'nowrap') return

      var kinder = Array.prototype.filter.call(el.children, function (c) {
        return sichtbar(c) && getComputedStyle(c).position !== 'absolute'
      })
      if (kinder.length < 3) return

      // Nach Reihen gruppieren, über die gerundete Oberkante.
      var reihen = []
      kinder.forEach(function (c) {
        var oben = Math.round(c.getBoundingClientRect().top)
        var reihe = null
        for (var i = 0; i < reihen.length; i++) {
          if (Math.abs(reihen[i].oben - oben) <= 4) { reihe = reihen[i]; break }
        }
        if (!reihe) { reihe = { oben: oben, teile: [] }; reihen.push(reihe) }
        reihe.teile.push(c)
      })
      if (reihen.length < 2) return

      reihen.sort(function (a, b) { return a.oben - b.oben })
      var letzte = reihen[reihen.length - 1]
      var voll = 0
      for (var i = 0; i < reihen.length - 1; i++) {
        var genutzt = 0
        reihen[i].teile.forEach(function (c) { genutzt += c.getBoundingClientRect().width })
        if (genutzt > voll) voll = genutzt
      }
      var genutztLetzte = 0
      letzte.teile.forEach(function (c) { genutztLetzte += c.getBoundingClientRect().width })
      var platz = innenbreite(el)
      if (platz <= 0 || voll <= 0) return

      var frei = platz - genutztLetzte
      if (frei / platz > o.lueckeAb && genutztLetzte < voll - 2) {
        melden('luecke', el,
          'letzte Reihe lässt ' + Math.round(frei) + ' px frei (' +
          Math.round(100 * frei / platz) + ' %) — ' + letzte.teile.length +
          ' von ' + reihen[0].teile.length + ' Kacheln',
          { reihen: reihen.length, frei: Math.round(frei) })
      }
    })

    return {
      breite: breite,
      ziel: ziel,
      befunde: befunde,
      bedienbar: wurzel.querySelectorAll(BEDIENBAR).length,
      elemente: alle.length
    }
  }

  // -------------------------------------------------------------- Bericht

  var ARTNAME = {
    seitenueberlauf: 'Seite scrollt waagrecht',
    ueberlauf_versteckt: 'Überlauf versteckt statt behoben',
    ueber_rand: 'Ragt über den Rand',
    inhalt_zu_breit: 'Inhalt breiter als der Platz',
    tabelle_zu_schmal: 'Tabelle nutzt die Breite nicht',
    tabelle_zu_breit: 'Tabelle breiter als der Inhaltsbereich',
    bedienziel_zu_klein: 'Bedienziel zu klein',
    luecke: 'Loch in der umgebrochenen Reihe'
  }

  var FOLGE = ['seitenueberlauf', 'ueber_rand', 'ueberlauf_versteckt',
    'inhalt_zu_breit', 'tabelle_zu_breit', 'tabelle_zu_schmal',
    'luecke', 'bedienziel_zu_klein']

  function bericht (ergebnis, hoechstens) {
    if (ergebnis.fehler) return ergebnis.fehler
    var grenze = hoechstens || VORGABE.hoechstensJeArt
    var zeilen = ['Überlaufprüfung bei ' + ergebnis.breite + ' px, Bedienziel ' +
      ergebnis.ziel + ' px — ' + ergebnis.elemente + ' Elemente, ' +
      ergebnis.bedienbar + ' bedienbar']
    if (!ergebnis.befunde.length) {
      zeilen.push('Bestanden. Nichts ragt hinaus, keine Lücke, kein Ziel zu klein.')
      return zeilen.join('\n')
    }
    zeilen.push('')
    zeilen.push(ergebnis.befunde.length + ' Befunde:')
    FOLGE.forEach(function (art) {
      var teil = ergebnis.befunde.filter(function (b) { return b.art === art })
      if (!teil.length) return
      zeilen.push('')
      zeilen.push('  ' + ARTNAME[art] + ' (' + teil.length + '):')
      teil.slice(0, grenze).forEach(function (b) {
        zeilen.push('    ' + b.was)
        zeilen.push('        ' + b.stelle + (b.text ? '  „' + b.text + '"' : ''))
      })
      if (teil.length > grenze) {
        zeilen.push('    … und ' + (teil.length - grenze) + ' weitere')
      }
    })
    return zeilen.join('\n')
  }

  var werkzeug = { pruefen: pruefen, bericht: bericht, BREITEN: BREITEN, VORGABE: VORGABE }
  welt.neoUeberlauf = werkzeug
  if (typeof module !== 'undefined' && module.exports) module.exports = werkzeug
})(typeof window !== 'undefined' ? window : globalThis)
