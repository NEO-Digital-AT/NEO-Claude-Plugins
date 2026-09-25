/**
 * neoTextFit — checks whether the text fits into its box.
 *
 * Complements `overflow.js`: that one checks what sticks OUT, this one
 * checks what does not fit IN. That is the more common case, because it
 * produces no scrollbar: text gets clipped, squeezed or unreadably narrow,
 * and the layout looks tidy while it happens.
 *
 * Eight things are checked:
 *
 *   1. Clipped horizontally  — text disappears behind the edge
 *   2. Clipped vertically    — text is cut off at the bottom, with no hint
 *   3. Truncated, no source  — truncated, and the full text is nowhere
 *   4. Too narrow for text   — a column holding two characters per line
 *   5. Wrong word break      — broken mid-word instead of at a syllable
 *   6. Font too small        — below the readability floor
 *   7. Overlap               — two texts sit on top of each other
 *   8. Covered text          — something else is painted on top of a line
 *
 * The fourth and the fifth are the ones no standard tool checks: a table
 * column that is three characters wide at 320px breaks no CSS rule. It is
 * just useless.
 *
 * The eighth catches what a glance misses: a progress bar, a badge or a
 * gradient sitting on top of running text. Check 7 only sees two TEXTS in
 * normal flow; this one sees any painting element above any text line,
 * including absolutely positioned and sticky ones, found per point with
 * document.elementsFromPoint.
 *
 * Because elementsFromPoint ignores elements with `pointer-events: none`,
 * and decoration usually sets exactly that, the check switches pointer
 * events on for the duration of the measurement and restores them after.
 *
 * A pinned or fixed surface that spans most of the width is page chrome:
 * content scrolls underneath it by design, so it is not reported here —
 * whether it reaches both window edges is `surface-edge.js`'s question.
 * Any other cover that is intended carries `data-covers-ok` or is named in
 * the `coverAllowed` option. An unmarked cover is a finding.
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
    coverSamples: 3,          // sample points per axis and text line
    coverMinArea: 12,         // px², below this a cover is a rounding artefact
    coverMaxLines: 12,        // lines sampled per element
    coverAllowed: [],         // selectors that are allowed to cover text
    coverChromeSpan: 0.5,     // from this share of the width a sticky surface
                              // counts as page chrome, not as decoration
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

  /** Does the element paint anything of its own? A transparent wrapper that
   * happens to span the area covers nothing. */
  function paints (el) {
    var tag = el.tagName
    if (tag === 'IMG' || tag === 'SVG' || tag === 'CANVAS' || tag === 'VIDEO' ||
        tag === 'PICTURE') return true
    var s = getComputedStyle(el)
    if (s.visibility === 'hidden' || parseFloat(s.opacity) === 0) return false
    if (s.backgroundImage && s.backgroundImage !== 'none') return true
    if (s.boxShadow && s.boxShadow !== 'none') return true
    var bg = s.backgroundColor || ''
    var rgba = bg.match(/rgba?\(([^)]+)\)/)
    if (rgba) {
      var parts = rgba[1].split(',')
      var alpha = parts.length > 3 ? parseFloat(parts[3]) : 1
      if (alpha > 0.02) return true
    }
    var sides = ['borderTopWidth', 'borderRightWidth', 'borderBottomWidth',
      'borderLeftWidth']
    for (var i = 0; i < sides.length; i++) {
      if (parseFloat(s[sides[i]]) > 0) return true
    }
    return false
  }

  /** The line boxes of the element's own text, one rect per line. */
  function lineBoxes (el) {
    var range = document.createRange()
    range.selectNodeContents(el)
    var boxes = range.getClientRects()
    var out = []
    for (var i = 0; i < boxes.length; i++) {
      if (boxes[i].width < 1 || boxes[i].height < 1) continue
      out.push(boxes[i])
    }
    return out
  }

  /** Which relationship means "not a cover":
   *  - the element itself
   *  - an ancestor: it paints BEHIND its own text, never over it
   *  - a descendant in normal flow: an inline span is part of the line
   * A positioned descendant is NOT exempt: decoration absolutely positioned
   * inside the very paragraph it covers is the most common form of this
   * defect, because it looks correct in the markup. */
  function partOfLine (over, el) {
    if (over === el) return true
    if (over.contains(el)) return true
    if (el.contains(over)) {
      // Not the element itself decides, but the chain up to the text: the
      // strips are static flex items, their CONTAINER is the absolute one.
      for (var n = over; n && n !== el; n = n.parentElement) {
        var position = getComputedStyle(n).position
        if (position === 'absolute' || position === 'fixed' ||
            position === 'sticky') return false
      }
      return true
    }
    return false
  }

  /** A pinned or fixed surface spanning most of the width is page chrome:
   * content scrolls underneath it, and that is the design. Whether such a
   * surface reaches both window edges is `surface-edge.js`'s question. This
   * check is about DECORATION over text — strips, badges, glows. */
  function pageChrome (el, minSpan) {
    var s = getComputedStyle(el)
    if (s.position !== 'sticky' && s.position !== 'fixed') return false
    var r = el.getBoundingClientRect()
    return r.width >= document.documentElement.clientWidth * minSpan
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

    // 8. Something is painted on top of a text line
    var patch = document.createElement('style')
    patch.textContent = '*{pointer-events:auto !important}'
    document.head.appendChild(patch)
    try {
      var allowed = o.coverAllowed || []
      var seen = {}
      withText.forEach(function (el) {
        var boxes = lineBoxes(el).slice(0, o.coverMaxLines)
        boxes.forEach(function (box) {
          var points = []
          for (var k = 1; k <= o.coverSamples; k++) {
            for (var v = 1; v <= o.coverSamples; v++) {
              // Sampling only the middle of the line misses decoration that
              // covers its upper or lower half — a 6px strip on a 20px line.
              points.push([box.left + box.width * (k / (o.coverSamples + 1)),
                box.top + box.height * (v / (o.coverSamples + 1))])
            }
          }
          for (var pi = 0; pi < points.length; pi++) {
            var x = points[pi][0]
            var y = points[pi][1]
            if (x < 0 || y < 0 || x > width || y > window.innerHeight) continue
            var stack = document.elementsFromPoint(x, y)
            for (var i = 0; i < stack.length; i++) {
              var over = stack[i]
              if (partOfLine(over, el)) break
              if (over === document.body ||
                  over === document.documentElement) break
              if (over.hasAttribute('data-covers-ok')) break
              var isAllowed = false
              for (var a = 0; a < allowed.length; a++) {
                if (over.closest(allowed[a])) isAllowed = true
              }
              if (isAllowed) break
              if (pageChrome(over, o.coverChromeSpan)) break
              if (!paints(over)) continue
              var r = over.getBoundingClientRect()
              var acrossX = Math.min(r.right, box.right) - Math.max(r.left, box.left)
              var acrossY = Math.min(r.bottom, box.bottom) - Math.max(r.top, box.top)
              if (acrossX * acrossY < o.coverMinArea) continue
              var key = selector(over) + '|' + selector(el)
              if (seen[key]) break
              seen[key] = true
              findings.push({
                kind: 'covered-text',
                what: selector(over) + ' is painted over ' +
                      Math.round(acrossX) + 'x' + Math.round(acrossY) +
                      'px of this line',
                where: selector(el),
                text: shorten(ownText(el))
              })
              break
            }
          }
        })
      })
    } finally {
      patch.parentNode.removeChild(patch)
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
    'overlap': 'Texts overlap',
    'covered-text': 'Something is painted over the text'
  }

  var ORDER = ['clipped-x', 'clipped-y', 'covered-text', 'truncated-no-source',
    'overlap', 'too-narrow', 'break-in-word',
    'hyphens-no-lang', 'font-too-small', 'truncated']

  function report (result, maxPerKind) {
    if (result.error) return result.error
    var limit = maxPerKind || DEFAULTS.maxPerKind
    var lines = ['Text fit at ' + result.width + 'px, font floor ' +
      result.fontFloor + 'px — ' + result.textElements + ' elements with text']
    if (!result.findings.length) {
      lines.push('Passed. No text clipped, nothing painted over it, no area ' +
        'too narrow, no break inside a word.')
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
