/*
 * NEO layout diff: compares geometry and appearance, not content.
 *
 * A pixel comparison fires as soon as a field holds a different value. But
 * content is dynamic — it comes from the database, from a picker or from a
 * third-party API. So this check measures what the design system actually
 * prescribes: how wide and how tall a field is, where it sits, what spacing
 * it keeps, what radius, what border width, what font size — and whether it
 * behaves that way in every state.
 *
 * The text inside the fields is NOT read and NOT compared.
 *
 * Measuring (Playwright, once for the design and once for the built view):
 *   await page.addScriptTag({ path: '<plugin>/scripts/layout-diff.js' })
 *   const measurement = await page.evaluate(() => neoLayoutDiff.measure())
 *
 * Comparing (in the browser or in Node, the function needs no DOM):
 *   const r = neoLayoutDiff.compare(design, built, { tolerance: 1 })
 *   console.log(neoLayoutDiff.report(r))
 */
(function (global) {
  'use strict'

  /* Matching: preferably via data-compare, otherwise via role plus order. */
  var MARKER = 'data-compare'

  var SIZE = ['width', 'height', 'x', 'y']
  var BOX = ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
             'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth',
             'marginTop', 'marginBottom', 'rowGap']
  var APPEARANCE = ['borderTopLeftRadius', 'borderTopRightRadius',
                    'borderBottomRightRadius', 'borderBottomLeftRadius',
                    'fontSize', 'lineHeight', 'fontWeight', 'letterSpacing']
  var TEXTUAL = ['borderTopColor', 'backgroundColor', 'color', 'fontFamily',
                 'boxShadow', 'textAlign', 'display', 'flexDirection']

  /**
   * The element's OWN text — only the immediate text nodes. A label and a
   * button caption are caught this way, the entries of a picker are not:
   * those sit in child elements and are content, not design.
   */
  function ownText (el) {
    var t = ''
    for (var i = 0; i < el.childNodes.length; i++) {
      var n = el.childNodes[i]
      if (n.nodeType === 3) t += n.nodeValue
    }
    return t.replace(/\s+/g, ' ').trim()
  }

  function round (n) { return Math.round(n * 2) / 2 }

  /** Rough functional role of an element — independent of the framework. */
  function role (el) {
    var tag = el.tagName.toLowerCase()
    var aria = (el.getAttribute('role') || '').toLowerCase()
    if (aria) return aria
    if (tag === 'input') {
      var type = (el.getAttribute('type') || 'text').toLowerCase()
      if (type === 'checkbox' || type === 'radio') return type
      if (type === 'button' || type === 'submit' || type === 'reset') return 'button'
      return 'textbox'
    }
    if (tag === 'textarea') return 'textarea'
    if (tag === 'select') return 'select'
    if (tag === 'button') return 'button'
    if (tag === 'a') return 'link'
    if (tag === 'label') return 'label'
    if (/^h[1-6]$/.test(tag)) return 'heading' + tag[1]
    if (tag === 'table') return 'table'
    if (tag === 'img' || tag === 'svg') return 'image'
    if (tag === 'form') return 'form'
    if (tag === 'ul' || tag === 'ol') return 'list'
    return null
  }

  function values (el, origin) {
    var r = el.getBoundingClientRect()
    var s = getComputedStyle(el)
    var f = function (n) { return round(parseFloat(s[n]) || 0) }
    return {
      width: round(r.width), height: round(r.height),
      x: round(r.left - origin.left), y: round(r.top - origin.top),
      paddingTop: f('paddingTop'), paddingRight: f('paddingRight'),
      paddingBottom: f('paddingBottom'), paddingLeft: f('paddingLeft'),
      borderTopWidth: f('borderTopWidth'), borderRightWidth: f('borderRightWidth'),
      borderBottomWidth: f('borderBottomWidth'), borderLeftWidth: f('borderLeftWidth'),
      marginTop: f('marginTop'), marginBottom: f('marginBottom'),
      rowGap: f('rowGap'),
      borderTopLeftRadius: f('borderTopLeftRadius'),
      borderTopRightRadius: f('borderTopRightRadius'),
      borderBottomRightRadius: f('borderBottomRightRadius'),
      borderBottomLeftRadius: f('borderBottomLeftRadius'),
      fontSize: f('fontSize'), lineHeight: f('lineHeight'),
      fontWeight: parseInt(s.fontWeight, 10) || 400,
      letterSpacing: round(parseFloat(s.letterSpacing) || 0),
      borderTopColor: s.borderTopWidth === '0px' ? '-' : s.borderTopColor,
      backgroundColor: s.backgroundColor, color: s.color,
      fontFamily: (s.fontFamily || '').split(',')[0].replace(/["']/g, '').trim(),
      boxShadow: s.boxShadow === 'none' ? '-' : s.boxShadow,
      textAlign: s.textAlign, display: s.display,
      flexDirection: s.display.indexOf('flex') >= 0 ? s.flexDirection : '-'
    }
  }

  var api = {
    /**
     * @param {{root?:Element, marker?:string, state?:string,
     *          markedOnly?:boolean, text?:boolean}} [opt]
     *
     * `text: true` additionally records the own text of every marked
     * element. It is meant to be switched on deliberately: static interface
     * texts belong to the design, dynamic content does not.
     */
    measure: function (opt) {
      opt = opt || {}
      var root = opt.root || document.body
      var marker = opt.marker || MARKER
      var origin = root.getBoundingClientRect()
      var all = Array.prototype.slice.call(root.querySelectorAll('*'))
      var counter = {}
      var elements = []

      all.forEach(function (el) {
        var s = getComputedStyle(el)
        if (s.display === 'none' || s.visibility === 'hidden') return
        var m = el.getAttribute(marker)
        var r = role(el)
        var key
        if (m) {
          key = m
        } else if (r && !opt.markedOnly) {
          counter[r] = (counter[r] || 0) + 1
          key = r + '#' + counter[r]
        } else {
          return
        }
        // Exclude single fields per element where the content decides the
        // size and that is intended:
        //   <button data-compare="button-primary" data-compare-except="width">
        var except = (el.getAttribute(marker + '-except') || '')
          .split(',').map(function (t) { return t.trim() }).filter(Boolean)
        var entry = {
          key: key,
          marked: !!m,
          role: r || 'unknown',
          except: except,
          values: values(el, origin)
        }
        if (opt.text) entry.text = ownText(el)
        elements.push(entry)
      })

      return {
        state: opt.state || 'rest',
        withText: !!opt.text,
        viewport: { width: window.innerWidth, height: window.innerHeight },
        rootSize: { width: round(origin.width), height: round(origin.height) },
        marked: elements.filter(function (e) { return e.marked }).length,
        elements: elements
      }
    },

    /**
     * Compares two measurements. Needs no DOM, runs in Node as well.
     * @param {{tolerance?:number, markedOnly?:boolean, text?:boolean}} [opt]
     *
     * `text: true` additionally compares the static interface texts. The
     * default is off: field values and list entries are dynamic, and a
     * deviation there is not a defect.
     */
    compare: function (design, built, opt) {
      opt = opt || {}
      var tolerance = opt.tolerance == null ? 1 : opt.tolerance
      var index = {}
      built.elements.forEach(function (e) { index[e.key] = e })

      var findings = []
      var missing = []
      var withoutText = []
      var pairs = 0
      var offsetX = {}
      var offsetY = {}

      design.elements.forEach(function (a) {
        if (opt.markedOnly && !a.marked) return
        var b = index[a.key]
        if (!b) { missing.push(a.key); return }
        pairs++
        delete index[a.key]

        var dx = b.values.x - a.values.x
        var dy = b.values.y - a.values.y
        offsetX[dx] = (offsetX[dx] || 0) + 1
        offsetY[dy] = (offsetY[dy] || 0) + 1

        var except = (a.except || []).concat(b.except || [])
        SIZE.concat(BOX, APPEARANCE).forEach(function (field) {
          if (except.indexOf(field) >= 0) return
          var expected = a.values[field], actual = b.values[field]
          var d = Math.abs(actual - expected)
          if (d > tolerance) {
            findings.push({ key: a.key, role: a.role, field: field,
                            expected: expected, actual: actual,
                            delta: round(actual - expected),
                            weight: SIZE.indexOf(field) >= 0 ? 3
                                  : BOX.indexOf(field) >= 0 ? 2 : 1 })
          }
        })
        TEXTUAL.forEach(function (field) {
          if (except.indexOf(field) >= 0) return
          if (a.values[field] !== b.values[field]) {
            findings.push({ key: a.key, role: a.role, field: field,
                            expected: a.values[field], actual: b.values[field],
                            delta: null, weight: 1 })
          }
        })

        if (opt.text && except.indexOf('text') < 0) {
          if (a.text === undefined || b.text === undefined) {
            withoutText.push(a.key)
          } else if (a.text !== b.text) {
            findings.push({ key: a.key, role: a.role, field: 'text',
                            expected: a.text || '(empty)', actual: b.text || '(empty)',
                            delta: null, weight: 2 })
          }
        }
      })

      // A uniform offset of all elements is ONE finding, not a hundred.
      function commonest (v) {
        var best = null, n = 0
        Object.keys(v).forEach(function (k) { if (v[k] > n) { n = v[k]; best = parseFloat(k) } })
        return { value: best, share: pairs ? n / pairs : 0 }
      }
      var gx = commonest(offsetX), gy = commonest(offsetY)
      var globalOffset = null
      if (pairs >= 5 && gx.share >= 0.8 && gy.share >= 0.8
          && (Math.abs(gx.value) > tolerance || Math.abs(gy.value) > tolerance)) {
        globalOffset = { x: gx.value, y: gy.value, share: gx.share }
        findings = findings.filter(function (f) {
          if (f.field === 'x') return Math.abs(f.delta - gx.value) > tolerance
          if (f.field === 'y') return Math.abs(f.delta - gy.value) > tolerance
          return true
        })
      }

      findings.sort(function (a, b) {
        if (b.weight !== a.weight) return b.weight - a.weight
        return Math.abs(b.delta || 0) - Math.abs(a.delta || 0)
      })

      return {
        state: design.state,
        tolerance: tolerance,
        textCompared: !!opt.text,
        pairs: pairs,
        missing: missing,
        withoutText: withoutText,
        extra: Object.keys(index),
        globalOffset: globalOffset,
        findings: findings,
        passed: findings.length === 0 && missing.length === 0
                && withoutText.length === 0 && !globalOffset
      }
    },

    report: function (r) {
      var lines = []
      lines.push('Layout diff, state "' + r.state + '": ' + r.pairs
                 + ' elements matched, tolerance ' + r.tolerance + 'px'
                 + (r.textCompared ? ', texts compared as well' : ''))
      if (r.withoutText && r.withoutText.length) {
        lines.push('  Texts requested but not measured: ' + r.withoutText.join(', ')
                   + ' — take both measurements with { text: true }.')
      }
      if (r.missing.length) {
        lines.push('  Not found in the built view: ' + r.missing.join(', '))
      }
      if (r.extra.length) {
        lines.push('  Not present in the design: ' + r.extra.join(', '))
      }
      if (r.globalOffset) {
        lines.push('  Uniform offset of all elements: x '
                   + r.globalOffset.x + 'px, y ' + r.globalOffset.y
                   + 'px — usually a different outer margin on the root.')
      }
      if (r.passed) {
        lines.push('Passed. Sizes, spacing and appearance match the design.')
        return lines.join('\n')
      }
      if (r.findings.length) {
        // The same deviation on many elements is ONE fault, usually a wrong
        // token. It is bundled, otherwise the report buries the cause under
        // its consequences.
        var bundle = {}
        var order = []
        r.findings.forEach(function (f) {
          var s = f.field + '|' + f.expected + '|' + f.actual
          if (!bundle[s]) {
            bundle[s] = { field: f.field, expected: f.expected, actual: f.actual,
                          delta: f.delta, weight: f.weight, keys: [] }
            order.push(s)
          }
          bundle[s].keys.push(f.key)
        })
        lines.push('  ' + order.length
                   + (order.length === 1 ? ' deviation in ' : ' deviations in ')
                   + r.findings.length
                   + (r.findings.length === 1 ? ' place:' : ' places:'))
        order.forEach(function (s) {
          var f = bundle[s]
          var value = f.delta === null
            ? f.actual + '   instead of   ' + f.expected
            : f.actual + 'px  instead of  ' + f.expected + 'px   ('
              + (f.delta > 0 ? '+' : '') + f.delta + ')'
          lines.push('    ' + String(f.field).padEnd(26) + value)
          var where = f.keys.length > 4
            ? f.keys.slice(0, 4).join(', ') + ' and '
              + (f.keys.length - 4) + ' more'
            : f.keys.join(', ')
          lines.push('        ' + where)
        })
      }
      return lines.join('\n')
    }
  }

  global.neoLayoutDiff = api
  if (typeof module !== 'undefined' && module.exports) module.exports = api
})(typeof window !== 'undefined' ? window : globalThis)
