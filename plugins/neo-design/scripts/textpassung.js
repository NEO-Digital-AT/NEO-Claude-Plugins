/**
 * neoTextpassung — prüft, ob der Text in seinen Bereich passt.
 *
 * Ergänzt `ueberlauf.js`: der prüft, was **hinausragt**, dieser prüft, was
 * **innen nicht passt**. Das ist der häufigere Fall, weil er keinen Balken
 * erzeugt: Text wird abgeschnitten, gestaucht oder unleserlich schmal, und
 * das Layout sieht dabei ordentlich aus.
 *
 * Geprüft wird siebenerlei:
 *
 *   1. Waagrecht abgeschnitten — Text verschwindet hinter der Kante
 *   2. Senkrecht abgeschnitten — Text ist unten weg, ohne Hinweis
 *   3. Kürzung ohne Volltext   — gekürzt, und nirgends steht das Ganze
 *   4. Zu schmal für Text      — eine Spalte, in der zwei Buchstaben stehen
 *   5. Falsch umgebrochen      — mitten im Wort statt an der Trennstelle
 *   6. Schrift zu klein        — unter der Lesbarkeitsgrenze
 *   7. Überlappung             — zwei Texte liegen übereinander
 *
 * Der vierte und der fünfte sind die, die kein Standardwerkzeug prüft:
 * eine Tabellenspalte, die auf 320 px drei Zeichen breit ist, verletzt
 * keine CSS-Regel. Sie ist nur unbrauchbar.
 *
 * Einbinden (Playwright):
 *   await page.addScriptTag({ path: 'tools/textpassung.js' })
 *   const b = await page.evaluate(() => neoTextpassung.pruefen())
 *   expect(b.befunde, neoTextpassung.bericht(b)).toHaveLength(0)
 *
 * Ohne Abhängigkeiten, framework-unabhängig: gemessen wird das fertige DOM.
 */
;(function (welt) {
  'use strict'

  var VORGABE = {
    toleranz: 1,            // px, gegen Rundung im Layout
    mindestZeichenJeZeile: 8,   // darunter ist eine Spalte unbrauchbar
    abZeilen: 3,            // erst ab so vielen Zeilen aussagekräftig
    mindestSchrift: 12,     // px, harte Untergrenze
    mindestSchriftSchmal: 14,   // px, auf schmalen Geräten
    schmalBis: 768,
    ueberlappungAb: 4,      // px, ab der eine Überdeckung ein Befund ist
    kuerzenErlaubt: true,   // Kürzung mit Volltext gilt als Absicht
    hoechstensJeArt: 12,
    wurzel: null
  }

  // --------------------------------------------------------------- Helfer

  function sichtbar (el) {
    var s = getComputedStyle(el)
    if (s.display === 'none' || s.visibility === 'hidden') return false
    if (parseFloat(s.opacity) === 0) return false
    var r = el.getBoundingClientRect()
    return r.width > 0 && r.height > 0
  }

  /** Nur eigener Text, nicht der von Kindern. Sonst meldet jeder Vorfahr mit. */
  function eigenerText (el) {
    var t = ''
    for (var i = 0; i < el.childNodes.length; i++) {
      var k = el.childNodes[i]
      if (k.nodeType === 3) t += k.nodeValue
    }
    return t.replace(/\s+/g, ' ').trim()
  }

  function zeilen (el) {
    var bereich = document.createRange()
    bereich.selectNodeContents(el)
    var kisten = bereich.getClientRects()
    var oben = []
    for (var i = 0; i < kisten.length; i++) {
      if (kisten[i].width < 0.5) continue
      var y = Math.round(kisten[i].top)
      var neu = true
      for (var j = 0; j < oben.length; j++) if (Math.abs(oben[j] - y) <= 2) neu = false
      if (neu) oben.push(y)
    }
    return oben.length
  }

  function pfad (el) {
    if (!el || el === document.documentElement) return 'html'
    var teile = []
    for (var k = el; k && k.nodeType === 1 && teile.length < 4; k = k.parentElement) {
      var t = k.tagName.toLowerCase()
      if (k.id) { teile.unshift(t + '#' + k.id); break }
      var marke = k.getAttribute('data-test') || k.getAttribute('data-abgleich')
      if (marke) { teile.unshift(t + '[' + marke + ']'); break }
      var klasse = (k.getAttribute('class') || '').trim().split(/\s+/)[0]
      teile.unshift(klasse ? t + '.' + klasse : t)
    }
    return teile.join(' > ')
  }

  function kurz (t) { return t.length > 48 ? t.slice(0, 48) + '…' : t }

  function abgeschnitten (s) {
    return s === 'hidden' || s === 'clip'
  }

  /** Steht der volle Text irgendwo, wo er zu holen ist? */
  function volltextDa (el, gezeigt) {
    var quellen = [el.getAttribute('title'), el.getAttribute('aria-label'),
      el.getAttribute('data-volltext')]
    for (var i = 0; i < quellen.length; i++) {
      var q = quellen[i]
      if (q && q.replace(/\s+/g, ' ').trim().length >= gezeigt.length) return true
    }
    var beschrieben = el.getAttribute('aria-describedby')
    if (beschrieben) {
      var b = document.getElementById(beschrieben.split(/\s+/)[0])
      if (b && b.textContent.trim().length >= gezeigt.length) return true
    }
    return false
  }

  // ------------------------------------------------------------ Prüfungen

  function pruefen (opt) {
    var o = {}
    for (var k in VORGABE) o[k] = VORGABE[k]
    for (var k2 in (opt || {})) o[k2] = opt[k2]

    var wurzel = o.wurzel ? document.querySelector(o.wurzel) : document.body
    if (!wurzel) return { fehler: 'Wurzel nicht gefunden: ' + o.wurzel, befunde: [] }

    var breite = document.documentElement.clientWidth
    var schriftGrenze = breite <= o.schmalBis ? o.mindestSchriftSchmal : o.mindestSchrift
    var befunde = []
    var mitText = []

    function melden (art, el, was, gezeigt) {
      befunde.push({ art: art, was: was, stelle: pfad(el), text: kurz(gezeigt || '') })
    }

    Array.prototype.forEach.call(wurzel.querySelectorAll('*'), function (el) {
      if (!sichtbar(el)) return
      var inhalt = eigenerText(el)
      if (!inhalt) return
      mitText.push(el)

      var s = getComputedStyle(el)
      var r = el.getBoundingClientRect()
      var schrift = parseFloat(s.fontSize) || 0

      // 1./3. Waagrecht abgeschnitten
      var zuviel = el.scrollWidth - el.clientWidth
      if (abgeschnitten(s.overflowX) && zuviel > o.toleranz) {
        var gekuerzt = s.textOverflow === 'ellipsis'
        if (!gekuerzt) {
          melden('abgeschnitten_quer', el,
            'Text verschwindet um ' + Math.round(zuviel) +
            ' px hinter der Kante, ohne Kürzungszeichen', inhalt)
        } else if (!volltextDa(el, inhalt)) {
          melden('kuerzung_ohne_volltext', el,
            'gekürzt um ' + Math.round(zuviel) +
            ' px, und der volle Text steht nirgends (kein title, kein aria-label)', inhalt)
        } else if (!o.kuerzenErlaubt) {
          melden('kuerzung', el, 'gekürzt um ' + Math.round(zuviel) + ' px', inhalt)
        }
      }

      // 2. Senkrecht abgeschnitten
      var hoch = el.scrollHeight - el.clientHeight
      if (abgeschnitten(s.overflowY) && hoch > o.toleranz) {
        var zeilenklemme = s.webkitLineClamp && s.webkitLineClamp !== 'none'
        if (!zeilenklemme || !volltextDa(el, inhalt)) {
          melden('abgeschnitten_hoch', el,
            'Text ist unten um ' + Math.round(hoch) + ' px abgeschnitten' +
            (zeilenklemme ? ' (Zeilenklemme ohne Volltext)' : ' und nicht erreichbar'), inhalt)
        }
      }

      // 4. Zu schmal für Text
      var n = zeilen(el)
      if (n >= o.abZeilen) {
        var jeZeile = inhalt.length / n
        if (jeZeile < o.mindestZeichenJeZeile) {
          melden('zu_schmal_fuer_text', el,
            Math.round(r.width) + ' px breit — ' + inhalt.length + ' Zeichen auf ' +
            n + ' Zeilen, im Mittel ' + jeZeile.toFixed(1) + ' je Zeile', inhalt)
        }
      }

      // 5. Falsch umgebrochen: harter Bruch mitten im Wort, obwohl es Fließtext ist
      var mehrwortig = /\S\s+\S/.test(inhalt)
      if (mehrwortig && inhalt.length > 24) {
        if (s.wordBreak === 'break-all') {
          melden('bruch_im_wort', el,
            'word-break: break-all bricht mitten im Wort — für Fließtext falsch', inhalt)
        } else if (s.overflowWrap === 'anywhere' && n > 1) {
          melden('bruch_im_wort', el,
            'overflow-wrap: anywhere bricht an beliebiger Stelle — für Fließtext ' +
            'gehört hyphens: auto mit gesetzter Sprache', inhalt)
        }
        if (s.hyphens === 'auto' && !el.closest('[lang]')) {
          melden('trennung_ohne_sprache', el,
            'hyphens: auto ohne lang-Attribut im Vorfahren — es wird nicht getrennt', inhalt)
        }
      }

      // 6. Schrift zu klein
      if (schrift > 0 && schrift + 0.5 < schriftGrenze) {
        melden('schrift_zu_klein', el,
          Math.round(schrift * 10) / 10 + ' px, verlangt sind ' + schriftGrenze + ' px', inhalt)
      }
    })

    // 7. Überlappung zweier Texte im normalen Fluss
    for (var i = 0; i < mitText.length; i++) {
      for (var j = i + 1; j < mitText.length; j++) {
        var a = mitText[i], b = mitText[j]
        if (a.contains(b) || b.contains(a)) continue
        var sa = getComputedStyle(a), sb = getComputedStyle(b)
        if (sa.position !== 'static' && sa.position !== 'relative') continue
        if (sb.position !== 'static' && sb.position !== 'relative') continue
        var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect()
        var quer = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left)
        var hoch2 = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top)
        if (quer > o.ueberlappungAb && hoch2 > o.ueberlappungAb) {
          befunde.push({
            art: 'ueberlappung',
            was: 'überdeckt ' + Math.round(quer) + '×' + Math.round(hoch2) + ' px von ' + pfad(b),
            stelle: pfad(a),
            text: kurz(eigenerText(a))
          })
        }
      }
    }

    return {
      breite: breite,
      schriftGrenze: schriftGrenze,
      textelemente: mitText.length,
      befunde: befunde
    }
  }

  // -------------------------------------------------------------- Bericht

  var ARTNAME = {
    abgeschnitten_quer: 'Text verschwindet hinter der Kante',
    abgeschnitten_hoch: 'Text unten abgeschnitten',
    kuerzung_ohne_volltext: 'Gekürzt, ohne den vollen Text anzubieten',
    kuerzung: 'Gekürzt',
    zu_schmal_fuer_text: 'Bereich zu schmal für seinen Text',
    bruch_im_wort: 'Umbruch mitten im Wort',
    trennung_ohne_sprache: 'Silbentrennung ohne Sprachangabe',
    schrift_zu_klein: 'Schrift zu klein',
    ueberlappung: 'Texte überlappen'
  }

  var FOLGE = ['abgeschnitten_quer', 'abgeschnitten_hoch', 'kuerzung_ohne_volltext',
    'ueberlappung', 'zu_schmal_fuer_text', 'bruch_im_wort',
    'trennung_ohne_sprache', 'schrift_zu_klein', 'kuerzung']

  function bericht (ergebnis, hoechstens) {
    if (ergebnis.fehler) return ergebnis.fehler
    var grenze = hoechstens || VORGABE.hoechstensJeArt
    var zeilen = ['Textpassung bei ' + ergebnis.breite + ' px, Schriftgrenze ' +
      ergebnis.schriftGrenze + ' px — ' + ergebnis.textelemente + ' Elemente mit Text']
    if (!ergebnis.befunde.length) {
      zeilen.push('Bestanden. Kein Text abgeschnitten, kein Bereich zu schmal, ' +
        'kein Umbruch im Wort.')
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
      if (teil.length > grenze) zeilen.push('    … und ' + (teil.length - grenze) + ' weitere')
    })
    return zeilen.join('\n')
  }

  var werkzeug = { pruefen: pruefen, bericht: bericht, VORGABE: VORGABE }
  welt.neoTextpassung = werkzeug
  if (typeof module !== 'undefined' && module.exports) module.exports = werkzeug
})(typeof window !== 'undefined' ? window : globalThis)
