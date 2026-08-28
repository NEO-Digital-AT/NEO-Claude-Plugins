/*
 * neoStyleAudit: finds invented values in a running user interface.
 *
 * The picture says THAT something looks different. This check says WHY:
 * it reads the computed styles of every element and reports every colour,
 * radius, font size and shadow that does not come from the tokens. It
 * works on the finished DOM and is therefore independent of whether
 * React, Vue, Angular or anything else sits behind it.
 *
 * Usage (Playwright):
 *   await page.addScriptTag({ path: '<plugin>/scripts/style-audit.js' })
 *   const report = await page.evaluate(() => neoStyleAudit.check())
 *
 * Without explicit tokens they are read from the custom properties of the
 * root element (--neo-*, --leoflex-* or your own prefix). If you have a
 * tokens.json, pass it instead.
 */
(function () {
  'use strict'

  var CHECKED = {
    colour: ['color', 'backgroundColor', 'borderTopColor', 'borderRightColor',
             'borderBottomColor', 'borderLeftColor', 'outlineColor', 'fill', 'stroke'],
    radius: ['borderTopLeftRadius', 'borderTopRightRadius',
             'borderBottomRightRadius', 'borderBottomLeftRadius'],
    fontSize: ['fontSize'],
    shadow: ['boxShadow'],
  }

  /** Normalises a colour to "r,g,b,a" — hex, rgb() and rgba(). */
  function colour (value) {
    if (!value) return null
    var t = String(value).trim().toLowerCase()
    if (t === 'transparent' || t === 'none') return 'transparent'
    var m = t.match(/^rgba?\(([^)]+)\)$/)
    if (m) {
      var parts = m[1].replace(/\//g, ' ').split(/[\s,]+/).filter(Boolean)
      var a = parts.length > 3 ? parseFloat(parts[3]) : 1
      if (a === 0) return 'transparent'
      return [Math.round(parseFloat(parts[0])), Math.round(parseFloat(parts[1])),
              Math.round(parseFloat(parts[2])), Math.round(a * 100) / 100].join(',')
    }
    var h = t.replace('#', '')
    if (/^[0-9a-f]{3,8}$/.test(h)) {
      if (h.length === 3 || h.length === 4) h = h.split('').map(function (c) { return c + c }).join('')
      var a2 = h.length === 8 ? parseInt(h.slice(6, 8), 16) / 255 : 1
      if (a2 === 0) return 'transparent'
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16),
              parseInt(h.slice(4, 6), 16), Math.round(a2 * 100) / 100].join(',')
    }
    return t
  }

  /** Rounds lengths to two decimals so 10px and 10.0001px are the same. */
  function length (value) {
    var n = parseFloat(value)
    return isNaN(n) ? String(value).trim() : Math.round(n * 100) / 100 + 'px'
  }

  /** Reads the tokens from the custom properties of the root element. */
  function tokensFromRoot (prefixes) {
    var allowed = { colour: {}, radius: {}, fontSize: {}, shadow: {} }
    var style = getComputedStyle(document.documentElement)
    var names = []
    for (var i = 0; i < style.length; i++) {
      var n = style[i]
      if (n.indexOf('--') !== 0) continue
      if (prefixes.length && !prefixes.some(function (p) { return n.indexOf(p) === 0 })) continue
      names.push(n)
    }
    // Separate lengths by their use: a radius token must not legitimise a
    // font size. Detected from the token name; if the name says nothing, the
    // value lands in both buckets so that unfamiliar naming does not produce
    // a flood of false findings.
    var looksLikeRadius = /radius|rounded|corner/
    var looksLikeFont = /font-?size|text|heading|title|body|caption|label|lead/
    var lengths = []
    names.forEach(function (n) {
      var v = style.getPropertyValue(n).trim()
      if (!v) return
      var c = colour(v)
      if (c && c !== v.toLowerCase()) allowed.colour[c] = n
      if (/^-?\d*\.?\d+(px|rem|em)$/.test(v)) lengths.push([n, length(v)])
      if (/(inset|\d+px)\s+.*(rgba?|#)/.test(v)) allowed.shadow[v] = n
    })
    var hasNamedRadii = lengths.some(function (l) { return looksLikeRadius.test(l[0]) })
    var hasNamedFonts = lengths.some(function (l) { return looksLikeFont.test(l[0]) })
    lengths.forEach(function (l) {
      var name = l[0], value = l[1]
      var r = looksLikeRadius.test(name), f = looksLikeFont.test(name)
      if (r || (!hasNamedRadii && !f)) allowed.radius[value] = name
      if (f || (!hasNamedFonts && !r)) allowed.fontSize[value] = name
    })
    return { allowed: allowed, count: names.length }
  }

  /** Short, readable path to an element. */
  function selector (el) {
    var parts = []
    while (el && el.nodeType === 1 && parts.length < 4) {
      var s = el.tagName.toLowerCase()
      if (el.id) { parts.unshift(s + '#' + el.id); break }
      var c = (el.getAttribute('class') || '').trim().split(/\s+/).filter(Boolean)[0]
      if (c) s += '.' + c
      parts.unshift(s)
      el = el.parentElement
    }
    return parts.join(' > ')
  }

  var api = {
    /**
     * @param {{tokens?:object, prefixes?:string[], root?:Element,
     *          ignore?:string, spacing?:boolean}} [opt]
     */
    check: function (opt) {
      opt = opt || {}
      var prefixes = opt.prefixes || ['--neo-', '--leoflex-']
      var source = opt.tokens
        ? { allowed: opt.tokens, count: -1 }
        : tokensFromRoot(prefixes)
      var allowed = source.allowed
      var root = opt.root || document.body
      var ignore = opt.ignore || '[data-neo-audit="off"]'
      if (opt.spacing) {
        CHECKED.spacing = ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
                           'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
                           'rowGap', 'columnGap']
      }

      var findings = []
      var counted = 0
      var elements = [root].concat(Array.prototype.slice.call(root.querySelectorAll('*')))

      elements.forEach(function (el) {
        if (el.closest && el.closest(ignore)) return
        var tag = el.tagName.toLowerCase()
        if (tag === 'script' || tag === 'style' || tag === 'noscript') return
        var style = getComputedStyle(el)
        counted++

        var inSvg = !!(el.ownerSVGElement || tag === 'svg')
        var hasOwnText = Array.prototype.some.call(el.childNodes, function (n) {
          return n.nodeType === 3 && n.nodeValue.trim().length > 0
        })

        // A property is only checked when it actually paints something on
        // this element. Otherwise the audit reports default values nobody set.
        function paints (property) {
          if (property === 'fill' || property === 'stroke') return inSvg
          if (property === 'color') return hasOwnText || inSvg
          if (property === 'outlineColor') {
            return style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0
          }
          var border = property.match(/^border(Top|Right|Bottom|Left)Color$/)
          if (border) {
            var side = border[1]
            return style['border' + side + 'Style'] !== 'none'
                && parseFloat(style['border' + side + 'Width']) > 0
          }
          return true
        }

        Object.keys(CHECKED).forEach(function (kind) {
          CHECKED[kind].forEach(function (property) {
            if (!paints(property)) return
            var raw = style[property]
            if (!raw || raw === 'none' || raw === 'normal' || raw === 'auto') return
            var value = kind === 'colour' ? colour(raw)
                      : kind === 'shadow' ? String(raw).trim()
                      : length(raw)
            if (value === 'transparent' || value === '0px') return
            if (allowed[kind] && Object.prototype.hasOwnProperty.call(allowed[kind], value)) return
            findings.push({ kind: kind, property: property, value: String(raw).trim(),
                            normalised: value, element: selector(el) })
          })
        })
      })

      // Group by value: one wrong value in thirty places is one finding.
      var byValue = {}
      findings.forEach(function (f) {
        var k = f.kind + '|' + f.normalised
        if (!byValue[k]) byValue[k] = { kind: f.kind, value: f.value,
                                        normalised: f.normalised,
                                        properties: {}, count: 0, examples: [] }
        byValue[k].count++
        byValue[k].properties[f.property] = true
        if (byValue[k].examples.length < 3) byValue[k].examples.push(f.element)
      })
      var grouped = Object.keys(byValue).map(function (k) {
        var e = byValue[k]
        e.properties = Object.keys(e.properties)
        return e
      }).sort(function (a, b) { return b.count - a.count })

      return {
        elements: counted,
        tokenSource: opt.tokens ? 'passed in' : 'custom properties of the root element',
        tokenCount: source.count,
        allowedColours: Object.keys(allowed.colour || {}).length,
        findings: grouped,
        total: findings.length,
        passed: grouped.length === 0,
      }
    },

    /** Text report, for console output or a test run. */
    report: function (r) {
      var lines = []
      lines.push('Style audit: ' + r.elements + ' elements checked, tokens from '
                 + r.tokenSource + (r.tokenCount >= 0 ? ' (' + r.tokenCount + ')' : ''))
      if (r.passed) {
        lines.push('Passed. Every visible value comes from the tokens.')
        return lines.join('\n')
      }
      lines.push(r.findings.length + ' invented values in ' + r.total + ' places:')
      r.findings.forEach(function (f) {
        lines.push('  ' + f.kind.padEnd(15) + f.value
                   + '   ' + f.count + 'x  (' + f.properties.join(', ') + ')')
        lines.push('      e.g. ' + f.examples.join('  |  '))
      })
      return lines.join('\n')
    }
  }

  window.neoStyleAudit = api
  if (typeof module !== 'undefined' && module.exports) module.exports = api
})()
