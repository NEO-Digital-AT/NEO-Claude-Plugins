/**
 * neoSurfaceEdge — checks whether an opaque surface reaches both window edges.
 *
 * The case it was written for: a gallery with a pinned image area that text
 * scrolls underneath. The opaque surface stopped 16px short of the window
 * edge, because its parent had padding-inline. In that strip the parent's
 * violet background showed through, and the text passing underneath was
 * visible in it. On a phone at the first station on the left, at the end of
 * the gallery on the right, 31px on a tablet, 90px in a low wide window.
 * Nobody sees that on a desktop, and a screenshot review missed it.
 *
 * Two things are checked per surface:
 *
 *   1. Edge gap     — the surface does not reach the left or right edge
 *   2. Show-through — content actually passes underneath inside that strip
 *
 * The second is what turns a gap into a defect: a surface that stops short
 * with nothing behind it is harmless and is reported as a note, not as a
 * finding — a surface that is only as wide as the content column is a
 * legitimate design. A finding names the gap in px, the element whose
 * padding or max-width causes it, and what shows through.
 *
 * A note is not an all-clear: in another scroll phase content can move into
 * that strip. That is why every phase is measured, not only the rest state.
 *
 * A surface is an element that is sticky, fixed, or marked with
 * `data-surface`, paints an opaque background, and spans at least half the
 * viewport. A surface that is meant to be inset carries `data-inset-ok`.
 *
 * Measured in the DOM, not in pixels, so the finding says WHY — and it works
 * without a screenshot. The caller drives the scroll phases: a pinned
 * surface has to be measured at the entry, at every station and at the exit,
 * not only at rest.
 *
 * Usage (Playwright):
 *   await page.addScriptTag({ path: 'tools/surface-edge.js' })
 *   for (const phase of phases) {
 *     await page.evaluate(y => window.scrollTo(0, y), phase)
 *     const r = await page.evaluate(() => neoSurfaceEdge.check())
 *     expect(r.findings, neoSurfaceEdge.report(r)).toHaveLength(0)
 *   }
 *
 * No dependencies, framework independent: the finished DOM is measured.
 */
;(function (global) {
  'use strict'

  var DEFAULTS = {
    tolerance: 1,          // px, against rounding in the layout
    minSpan: 0.5,          // a surface spans at least this share of the width
    minAlpha: 0.9,         // from this alpha a background counts as opaque
    behindMin: 4,          // px, from which content counts as showing through
    maxPerKind: 12,
    root: null
  }

  function visible (el) {
    var s = getComputedStyle(el)
    if (s.display === 'none' || s.visibility === 'hidden') return false
    if (parseFloat(s.opacity) === 0) return false
    var r = el.getBoundingClientRect()
    return r.width > 0 && r.height > 0
  }

  function alphaOf (color) {
    var m = (color || '').match(/rgba?\(([^)]+)\)/)
    if (!m) return 0
    var parts = m[1].split(',')
    return parts.length > 3 ? parseFloat(parts[3]) : 1
  }

  /** Opaque means: a background that hides what is behind it. */
  function opaque (el, minAlpha) {
    var s = getComputedStyle(el)
    if (s.backgroundImage && s.backgroundImage !== 'none') return true
    return alphaOf(s.backgroundColor) >= minAlpha
  }

  /** How far the element paints BEYOND its border box. The sanctioned way to
   * take a surface full width is border-image with outset: it paints outside
   * the box without adding layout, so it produces no overflow finding — and
   * getBoundingClientRect does not see it. A box shadow with spread and an
   * outline do the same. Anything else has to be measured on the pixels, so
   * such a surface carries `data-inset-ok` with a reason. */
  function paintedBeyond (el) {
    var s = getComputedStyle(el)
    var left = 0
    var right = 0

    if (s.borderImageSource && s.borderImageSource !== 'none') {
      var widths = (s.borderWidth || '0px').split(' ')
      var borderLeft = parseFloat(s.borderLeftWidth) || 0
      var borderRight = parseFloat(s.borderRightWidth) || 0
      var outset = (s.borderImageOutset || '0').trim().split(/\s+/)
      var top = outset[0]
      var rightSide = outset.length > 1 ? outset[1] : top
      var leftSide = outset.length > 3 ? outset[3] : rightSide
      // A unitless outset is a multiple of the border width.
      function resolve (value, border) {
        if (value === undefined) return 0
        return value.indexOf('px') >= 0 ? parseFloat(value)
          : (parseFloat(value) || 0) * border
      }
      left = resolve(leftSide, borderLeft)
      right = resolve(rightSide, borderRight)
      // With a zero-width border and `fill`, the image paints the whole box
      // and the outset alone carries it outward.
      if (!left && !right && widths.length) {
        left = right = 0
      }
    }

    var shadow = s.boxShadow || 'none'
    if (shadow !== 'none' && shadow.indexOf('inset') < 0) {
      var numbers = shadow.match(/-?\d+(\.\d+)?px/g) || []
      if (numbers.length >= 4) {
        var offsetX = Math.abs(parseFloat(numbers[0]))
        var spread = Math.abs(parseFloat(numbers[3]))
        left = Math.max(left, spread + offsetX)
        right = Math.max(right, spread + offsetX)
      }
    }

    var outline = parseFloat(s.outlineWidth) || 0
    if (outline > 0 && s.outlineStyle !== 'none') {
      left = Math.max(left, outline)
      right = Math.max(right, outline)
    }

    return { left: left, right: right }
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

  function shorten (t) {
    t = (t || '').replace(/\s+/g, ' ').trim()
    return t.length > 40 ? t.slice(0, 40) + '…' : t
  }

  /** The ancestor that keeps the surface off the edge: its padding or its
   * max-width. Naming it saves the search. */
  function whyInset (el, side) {
    var prop = side === 'left' ? 'paddingLeft' : 'paddingRight'
    for (var n = el.parentElement; n && n !== document.documentElement; n = n.parentElement) {
      var s = getComputedStyle(n)
      var pad = parseFloat(s[prop]) || 0
      if (pad > 0) return selector(n) + ' has ' + Math.round(pad) + 'px ' +
        (side === 'left' ? 'padding-left' : 'padding-right')
      if (s.maxWidth && s.maxWidth !== 'none') {
        var max = parseFloat(s.maxWidth)
        if (max && max < document.documentElement.clientWidth) {
          return selector(n) + ' is limited to ' + Math.round(max) + 'px'
        }
      }
    }
    return 'no padding or max-width found on an ancestor'
  }

  function check (opt) {
    var o = {}
    for (var k in DEFAULTS) o[k] = DEFAULTS[k]
    for (var k2 in (opt || {})) o[k2] = opt[k2]

    var root = o.root ? document.querySelector(o.root) : document.body
    if (!root) return { error: 'Root not found: ' + o.root, findings: [] }

    var width = document.documentElement.clientWidth
    var findings = []
    var notes = []
    var surfaces = []

    Array.prototype.forEach.call(root.querySelectorAll('*'), function (el) {
      if (!visible(el)) return
      var s = getComputedStyle(el)
      var marked = el.hasAttribute('data-surface')
      if (!marked && s.position !== 'sticky' && s.position !== 'fixed') return
      var r = el.getBoundingClientRect()
      if (r.width < width * o.minSpan) return
      if (!marked && !opaque(el, o.minAlpha)) return
      if (el.hasAttribute('data-inset-ok')) return
      surfaces.push({ el: el, rect: r })
    })

    surfaces.forEach(function (surface) {
      var el = surface.el
      var r = surface.rect
      var beyond = paintedBeyond(el)
      var paintedLeft = r.left - beyond.left
      var paintedRight = r.right + beyond.right
      var gaps = []
      if (paintedLeft > o.tolerance) {
        gaps.push({ side: 'left', from: 0, to: paintedLeft })
      }
      if (width - paintedRight > o.tolerance) {
        gaps.push({ side: 'right', from: paintedRight, to: width })
      }
      if (!gaps.length) return

      // Content running UNDERNEATH the surface is what makes the gap a
      // defect: that content stays visible in the strip. Looking only
      // inside the strip finds nothing, because the same padding that
      // insets the surface insets the text as well.
      var behind = []
      Array.prototype.forEach.call(document.body.querySelectorAll('*'),
        function (other) {
          if (other === el || el.contains(other) || other.contains(el)) return
          if (!visible(other)) return
          var ro = other.getBoundingClientRect()
          var acrossX = Math.min(ro.right, r.right) - Math.max(ro.left, r.left)
          var acrossY = Math.min(ro.bottom, r.bottom) - Math.max(ro.top, r.top)
          if (acrossX < o.behindMin || acrossY < o.behindMin) return
          var own = ''
          for (var i = 0; i < other.childNodes.length; i++) {
            if (other.childNodes[i].nodeType === 3) own += other.childNodes[i].nodeValue
          }
          if (!own.trim()) return
          behind.push({ where: selector(other), text: shorten(own) })
        })

      gaps.forEach(function (gap) {
        var size = Math.round(gap.to - gap.from)

        var entry = {
          kind: behind.length ? 'edge-gap' : 'edge-gap-empty',
          what: size + 'px ' + gap.side + ' of the surface are uncovered' +
                (behind.length
                  ? ', while ' + behind.length +
                    (behind.length === 1 ? ' element runs' : ' elements run') +
                    ' underneath it: ' + behind[0].where
                  : ', and nothing runs underneath it in this phase'),
          why: whyInset(el, gap.side),
          where: selector(el),
          text: behind.length ? behind[0].text : ''
        }
        if (behind.length) findings.push(entry)
        else notes.push(entry)
      })
    })

    return {
      width: width,
      scrollY: Math.round(window.scrollY),
      surfaces: surfaces.length,
      findings: findings,
      notes: notes
    }
  }

  var KIND_NAMES = {
    'edge-gap': 'Surface does not reach the edge while content runs underneath',
    'edge-gap-empty': 'Surface does not reach the edge'
  }

  function report (result, maxPerKind) {
    if (result.error) return result.error
    var limit = maxPerKind || DEFAULTS.maxPerKind
    var lines = ['Surface edges at ' + result.width + 'px, scrolled to ' +
      result.scrollY + 'px — ' + result.surfaces +
      (result.surfaces === 1 ? ' surface' : ' surfaces')]
    if (!result.surfaces) {
      lines.push('No sticky, fixed or marked surface found. Is this the phase ' +
        'where the surface is pinned?')
      return lines.join('\n')
    }
    if (!result.findings.length) {
      lines.push('Passed. No surface with content underneath stops short of ' +
        'an edge.')
      if (result.notes && result.notes.length) {
        lines.push('')
        lines.push('Notes — a gap with nothing behind it, harmless in this ' +
          'phase (' + result.notes.length + '). Another phase can put ' +
          'content there, so measure every phase:')
        result.notes.slice(0, limit).forEach(function (f) {
          lines.push('    ' + f.what)
          lines.push('        surface: ' + f.where)
        })
      }
      return lines.join('\n')
    }
    lines.push('')
    var n = result.findings.length
    lines.push(n + (n === 1 ? ' finding:' : ' findings:'))
    Object.keys(KIND_NAMES).forEach(function (kind) {
      var part = result.findings.filter(function (f) { return f.kind === kind })
      if (!part.length) return
      lines.push('')
      lines.push('  ' + KIND_NAMES[kind] + ' (' + part.length + '):')
      part.slice(0, limit).forEach(function (f) {
        lines.push('    ' + f.what)
        lines.push('        surface: ' + f.where)
        lines.push('        cause:   ' + f.why)
        if (f.text) lines.push('        behind:  "' + f.text + '"')
      })
      if (part.length > limit) lines.push('    … and ' + (part.length - limit) + ' more')
    })
    lines.push('')
    lines.push('Full width belongs on the surface itself — border-image with ' +
      'outset. A pseudo element with 100vw or a negative margin produces an ' +
      'overflow finding instead.')
    return lines.join('\n')
  }

  var tool = { check: check, report: report, DEFAULTS: DEFAULTS }
  global.neoSurfaceEdge = tool
  if (typeof module !== 'undefined' && module.exports) module.exports = tool
})(typeof window !== 'undefined' ? window : globalThis)
