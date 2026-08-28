/**
 * neoTextFit — checks whether the text fits into its box.
 *
 * Complements `overflow.js`: that one checks what sticks OUT, this one
 * checks what does not fit IN. That is the more common case, because it
 * produces no scrollbar: text gets clipped, squeezed or unreadably narrow,
 * and the layout looks tidy while it happens.
 *
 * Seven things are checked:
 *
 *   1. Clipped horizontally  — text disappears behind the edge
 *   2. Clipped vertically    — text is cut off at the bottom, with no hint
 *   3. Truncated, no source  — truncated, and the full text is nowhere
 *   4. Too narrow for text   — a column holding two characters per line
 *   5. Wrong word break      — broken mid-word instead of at a syllable
 *   6. Font too small        — below the readability floor
 *   7. Overlap               — two texts sit on top of each other
 *
 * The fourth and the fifth are the ones no standard tool checks: a table
 * column that is three characters wide at 320px breaks no CSS rule. It is
 * just useless.
 *
 * Usage (Playwright):
 *   await page.addScriptTag({ path: 'tools/text-fit.js' })
 *   const r = await page.evaluate(() => neoTextFit.check())
 *   expect(r.findings, neoTextFit.report(r)).toHaveLength(0)
 *
 * No dependencies, framework independent: the finished DOM is measured.
 */
;(function (global) {
  'use strict'

  var DEFAULTS = {
    tolerance: 1,             // px, against rounding in the layout
    minCharsPerLine: 8,       // below this a column is unusable
    fromLines: 3,             // only meaningful from this many lines
    minFontSize: 12,          // px, hard floor
    minFontSizeNarrow: 14,    // px, on narrow devices
    narrowUpTo: 768,
    overlapFrom: 4,           // px, from which an overlap is a finding
    truncationAllowed: true,  // truncation with a full text counts as intent
    maxPerKind: 12,
    root: null
  }

  // --------------------------------------------------------------- Helpers

  function visible (el) {
    var s = getComputedStyle(el)
    if (s.display === 'none' || s.visibility === 'hidden') return false
    if (parseFloat(s.opacity) === 0) return false
    var r = el.getBoundingClientRect()
    return r.width > 0 && r.height > 0
  }

  /** Own text only, not that of children. Otherwise every ancestor reports too. */
  function ownText (el) {
    var t = ''
    for (var i = 0; i < el.childNodes.length; i++) {
      var n = el.childNodes[i]
      if (n.nodeType === 3) t += n.nodeValue
    }
    return t.replace(/\s+/g, ' ').trim()
  }

  function lineCount (el) {
    var range = document.createRange()
    range.selectNodeContents(el)
    var boxes = range.getClientRects()
    var tops = []
    for (var i = 0; i < boxes.length; i++) {
      if (boxes[i].width < 0.5) continue
      var y = Math.round(boxes[i].top)
      var isNew = true
      for (var j = 0; j < tops.length; j++) if (Math.abs(tops[j] - y) <= 2) isNew = false
      if (isNew) tops.push(y)
    }
    return tops.length
  }

  function selector (el) {
    if (!el || el === document.documentElement) return 'html'
    var parts = []
    for (var n = el; n && n.nodeType === 1 && parts.length < 4; n = n.parentElement) {
      var t = n.tagName.toLowerCase()
      if (n.id) { parts.unshift(t + '#' + n.id); break }
      var marker = n.getAttribute('data-test') || n.getAttribute('data-compare')
      if (marker) { parts.unshift(t + '[' + marker + ']'); break }
      var cls = (n.getAttribute('class') || '').trim().split(/\s+/)[0]
      parts.unshift(cls ? t + '.' + cls : t)
    }
    return parts.join(' > ')
  }

  function shorten (t) { return t.length > 48 ? t.slice(0, 48) + '…' : t }

  function clips (value) {
    return value === 'hidden' || value === 'clip'
  }

  /** Is the full text available anywhere it can be retrieved from? */
  function fullTextAvailable (el, shown) {
    var sources = [el.getAttribute('title'), el.getAttribute('aria-label'),
      el.getAttribute('data-fulltext')]
    for (var i = 0; i < sources.length; i++) {
      var s = sources[i]
      if (s && s.replace(/\s+/g, ' ').trim().length >= shown.length) return true
    }
    var describedBy = el.getAttribute('aria-describedby')
    if (describedBy) {
      var d = document.getElementById(describedBy.split(/\s+/)[0])
      if (d && d.textContent.trim().length >= shown.length) return true
    }
    return false
  }

  // ---------------------------------------------------------------- Checks

  function check (opt) {
    var o = {}
    for (var k in DEFAULTS) o[k] = DEFAULTS[k]
    for (var k2 in (opt || {})) o[k2] = opt[k2]

    var root = o.root ? document.querySelector(o.root) : document.body
    if (!root) return { error: 'Root not found: ' + o.root, findings: [] }

    var width = document.documentElement.clientWidth
    var fontFloor = width <= o.narrowUpTo ? o.minFontSizeNarrow : o.minFontSize
    var findings = []
    var withText = []

    function add (kind, el, what, shown) {
      findings.push({ kind: kind, what: what, where: selector(el), text: shorten(shown || '') })
    }

    Array.prototype.forEach.call(root.querySelectorAll('*'), function (el) {
      if (!visible(el)) return
      var content = ownText(el)
      if (!content) return
      withText.push(el)

      var s = getComputedStyle(el)
      var r = el.getBoundingClientRect()
      var fontSize = parseFloat(s.fontSize) || 0

      // 1./3. Clipped horizontally
      var over = el.scrollWidth - el.clientWidth
      if (clips(s.overflowX) && over > o.tolerance) {
        var truncated = s.textOverflow === 'ellipsis'
        if (!truncated) {
          add('clipped-x', el,
            'text disappears ' + Math.round(over) +
            'px behind the edge, with no ellipsis', content)
        } else if (!fullTextAvailable(el, content)) {
          add('truncated-no-source', el,
            'truncated by ' + Math.round(over) +
            'px, and the full text is nowhere (no title, no aria-label)', content)
        } else if (!o.truncationAllowed) {
          add('truncated', el, 'truncated by ' + Math.round(over) + 'px', content)
        }
      }

      // 2. Clipped vertically
      var overY = el.scrollHeight - el.clientHeight
      if (clips(s.overflowY) && overY > o.tolerance) {
        var clamped = s.webkitLineClamp && s.webkitLineClamp !== 'none'
        if (!clamped || !fullTextAvailable(el, content)) {
          add('clipped-y', el,
            'text is cut off at the bottom by ' + Math.round(overY) + 'px' +
            (clamped ? ' (line clamp without a full text)' : ' and cannot be reached'), content)
        }
      }

      // 4. Too narrow for text
      var lines = lineCount(el)
      if (lines >= o.fromLines) {
        var perLine = content.length / lines
        if (perLine < o.minCharsPerLine) {
          add('too-narrow', el,
            Math.round(r.width) + 'px wide — ' + content.length + ' characters on ' +
            lines + ' lines, ' + perLine.toFixed(1) + ' per line on average', content)
        }
      }

      // 5. Wrong word break: hard break mid-word although this is prose
      var multiWord = /\S\s+\S/.test(content)
      if (multiWord && content.length > 24) {
        if (s.wordBreak === 'break-all') {
          add('break-in-word', el,
            'word-break: break-all breaks mid-word — wrong for prose', content)
        } else if (s.overflowWrap === 'anywhere' && lines > 1) {
          add('break-in-word', el,
            'overflow-wrap: anywhere breaks at any position — prose needs ' +
            'hyphens: auto with the language set', content)
        }
        if (s.hyphens === 'auto' && !el.closest('[lang]')) {
          add('hyphens-no-lang', el,
            'hyphens: auto without a lang attribute on an ancestor — nothing is hyphenated',
            content)
        }
      }

      // 6. Font too small
      if (fontSize > 0 && fontSize + 0.5 < fontFloor) {
        add('font-too-small', el,
          Math.round(fontSize * 10) / 10 + 'px, required is ' + fontFloor + 'px', content)
      }
    })

    // 7. Overlap of two texts in normal flow
    for (var i = 0; i < withText.length; i++) {
      for (var j = i + 1; j < withText.length; j++) {
        var a = withText[i], b = withText[j]
        if (a.contains(b) || b.contains(a)) continue
        var sa = getComputedStyle(a), sb = getComputedStyle(b)
        if (sa.position !== 'static' && sa.position !== 'relative') continue
        if (sb.position !== 'static' && sb.position !== 'relative') continue
        var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect()
        var acrossX = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left)
        var acrossY = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top)
        if (acrossX > o.overlapFrom && acrossY > o.overlapFrom) {
          findings.push({
            kind: 'overlap',
            what: 'covers ' + Math.round(acrossX) + 'x' + Math.round(acrossY) +
                  'px of ' + selector(b),
            where: selector(a),
            text: shorten(ownText(a))
          })
        }
      }
    }

    return {
      width: width,
      fontFloor: fontFloor,
      textElements: withText.length,
      findings: findings
    }
  }

  // ---------------------------------------------------------------- Report

  var KIND_NAMES = {
    'clipped-x': 'Text disappears behind the edge',
    'clipped-y': 'Text cut off at the bottom',
    'truncated-no-source': 'Truncated without offering the full text',
    'truncated': 'Truncated',
    'too-narrow': 'Area too narrow for its text',
    'break-in-word': 'Break in the middle of a word',
    'hyphens-no-lang': 'Hyphenation without a language',
    'font-too-small': 'Font too small',
    'overlap': 'Texts overlap'
  }

  var ORDER = ['clipped-x', 'clipped-y', 'truncated-no-source',
    'overlap', 'too-narrow', 'break-in-word',
    'hyphens-no-lang', 'font-too-small', 'truncated']

  function report (result, maxPerKind) {
    if (result.error) return result.error
    var limit = maxPerKind || DEFAULTS.maxPerKind
    var lines = ['Text fit at ' + result.width + 'px, font floor ' +
      result.fontFloor + 'px — ' + result.textElements + ' elements with text']
    if (!result.findings.length) {
      lines.push('Passed. No text clipped, no area too narrow, no break inside a word.')
      return lines.join('\n')
    }
    lines.push('')
    var n = result.findings.length
    lines.push(n + (n === 1 ? ' finding:' : ' findings:'))
    ORDER.forEach(function (kind) {
      var part = result.findings.filter(function (f) { return f.kind === kind })
      if (!part.length) return
      lines.push('')
      lines.push('  ' + KIND_NAMES[kind] + ' (' + part.length + '):')
      part.slice(0, limit).forEach(function (f) {
        lines.push('    ' + f.what)
        lines.push('        ' + f.where + (f.text ? '  "' + f.text + '"' : ''))
      })
      if (part.length > limit) lines.push('    … and ' + (part.length - limit) + ' more')
    })
    return lines.join('\n')
  }

  var tool = { check: check, report: report, DEFAULTS: DEFAULTS }
  global.neoTextFit = tool
  if (typeof module !== 'undefined' && module.exports) module.exports = tool
})(typeof window !== 'undefined' ? window : globalThis)
