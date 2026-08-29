/**
 * neoOverflow — measures what does not fit on the screen at a given width.
 *
 * Injected into the running page before the measurement and called once per
 * test width. Seven things are checked:
 *
 *   1. Page overflow   — the body scrolls horizontally
 *   2. Past the edge   — an element sticks out of the visible area
 *   3. Wider than box  — an element is wider than the space it has
 *   4. Tables          — a table does not use the width of the content area
 *   5. Touch targets   — a button is too small for a finger
 *   6. Gaps            — a wrapped row leaves a hole
 *   7. Overlays        — an opened layer leaves the visible area
 *
 * The sixth is the one no standard tool checks: three cards that wrap onto
 * two columns leave half of the second row empty. The rule against it:
 * either one column, or the last element fills the row.
 *
 * The seventh only shows with the overlay OPEN. A picker near the bottom
 * edge that opens downwards covers its own options; it has to open upwards
 * instead. So the test opens every overlay and measures it — a closed page
 * proves nothing about them.
 *
 * Usage (Playwright):
 *   await page.addScriptTag({ path: 'tools/overflow.js' })
 *   for (const width of neoOverflow.WIDTHS) {
 *     await page.setViewportSize({ width: width, height: 900 })
 *     const r = await page.evaluate(() => neoOverflow.check())
 *     expect(r.findings, neoOverflow.report(r)).toHaveLength(0)
 *   }
 *
 * No dependencies, framework independent: the finished DOM is measured.
 */
;(function (global) {
  'use strict'

  var WIDTHS = [320, 390, 768, 1024, 1280, 1920, 2560, 3840]

  var DEFAULTS = {
    tolerance: 1,        // px, against rounding in the layout
    targetNarrow: 44,    // touch target up to 768px — finger, not pointer
    targetWide: 24,      // touch target above that — WCAG 2.2 (2.5.8)
    narrowUpTo: 768,
    gapFrom: 0.15,       // free share of a row from which it counts as a hole
    maxPerKind: 12,      // reported per kind, otherwise the report is unreadable
    root: null,
    contentArea: '[data-content], main, [role="main"]'
  }

  var INTERACTIVE = 'a[href],button,input,select,textarea,summary,[role="button"],' +
    '[role="link"],[role="checkbox"],[role="radio"],[role="switch"],[role="tab"],' +
    '[role="menuitem"],[tabindex]:not([tabindex="-1"])'

  // Layers that open on top of the page: pickers, menus, dialogs, tooltips.
  // Whatever a framework names differently a project marks with data-overlay.
  var OVERLAY = '[role="listbox"],[role="menu"],[role="menubar"],[role="dialog"],' +
    '[role="alertdialog"],[role="tooltip"],[popover],[data-overlay]'

  // --------------------------------------------------------------- Helpers

  function visible (el) {
    var s = getComputedStyle(el)
    if (s.display === 'none' || s.visibility === 'hidden' || s.visibility === 'collapse') return false
    if (parseFloat(s.opacity) === 0) return false
    var r = el.getBoundingClientRect()
    return r.width > 0 && r.height > 0
  }

  function selector (el) {
    if (!el || el === document.documentElement) return 'html'
    var parts = []
    var node = el
    while (node && node.nodeType === 1 && parts.length < 4) {
      var t = node.tagName.toLowerCase()
      if (node.id) { parts.unshift(t + '#' + node.id); break }
      var marker = node.getAttribute('data-test') || node.getAttribute('data-compare')
      if (marker) { parts.unshift(t + '[' + marker + ']'); break }
      var cls = (node.getAttribute('class') || '').trim().split(/\s+/)[0]
      parts.unshift(cls ? t + '.' + cls : t)
      node = node.parentElement
    }
    return parts.join(' > ')
  }

  function label (el) {
    var t = (el.getAttribute('aria-label') || el.textContent || '')
      .replace(/\s+/g, ' ').trim()
    return t.length > 40 ? t.slice(0, 40) + '…' : t
  }

  function scrollable (el) {
    var s = getComputedStyle(el).overflowX
    return s === 'auto' || s === 'scroll'
  }

  function insideScroller (el, root) {
    for (var n = el.parentElement; n && n !== root; n = n.parentElement) {
      if (scrollable(n)) return true
    }
    return false
  }

  /** The nearest ancestor that cuts off whatever sticks out of it. */
  function clippingParent (el, root) {
    var cuts = /^(hidden|clip|auto|scroll)$/
    for (var n = el.parentElement; n && n !== root.parentElement; n = n.parentElement) {
      var s = getComputedStyle(n)
      if (s.position === 'fixed') return null
      if (cuts.test(s.overflowX) || cuts.test(s.overflowY)) return n
    }
    return null
  }

  function innerWidth (el) {
    var s = getComputedStyle(el)
    return el.clientWidth -
      parseFloat(s.paddingLeft || 0) - parseFloat(s.paddingRight || 0)
  }

  // ---------------------------------------------------------------- Checks

  function check (opt) {
    var o = {}
    for (var k in DEFAULTS) o[k] = DEFAULTS[k]
    for (var k2 in (opt || {})) o[k2] = opt[k2]

    var root = o.root ? document.querySelector(o.root) : document.body
    if (!root) return { error: 'Root not found: ' + o.root, findings: [] }

    var width = document.documentElement.clientWidth
    var target = width <= o.narrowUpTo ? o.targetNarrow : o.targetWide
    var findings = []
    var all = Array.prototype.slice.call(root.querySelectorAll('*'))
    var reported = []

    function add (kind, el, what, extra) {
      var entry = { kind: kind, what: what, where: selector(el), text: label(el) }
      for (var e in (extra || {})) entry[e] = extra[e]
      findings.push(entry)
      reported.push(el)
    }

    function alreadyReported (el) {
      for (var i = 0; i < reported.length; i++) {
        if (reported[i] !== el && reported[i].contains(el)) return true
      }
      return false
    }

    // 1. Page overflow
    var d = document.documentElement
    var excess = d.scrollWidth - d.clientWidth
    if (excess > o.tolerance) {
      findings.push({
        kind: 'page-overflow',
        what: 'The body scrolls horizontally by ' + Math.round(excess) + 'px',
        where: 'html', text: ''
      })
    }
    if (getComputedStyle(document.body).overflowX === 'hidden') {
      findings.push({
        kind: 'overflow-hidden',
        what: 'overflow-x: hidden on the body hides the fault instead of fixing it',
        where: 'body', text: ''
      })
    }

    // 2. Past the visible edge
    all.forEach(function (el) {
      if (!visible(el) || alreadyReported(el)) return
      var r = el.getBoundingClientRect()
      if (insideScroller(el, root)) return
      if (r.right > width + o.tolerance) {
        add('past-edge', el,
          'sticks out ' + Math.round(r.right - width) + 'px past the right edge',
          { width: Math.round(r.width) })
      } else if (r.left < -o.tolerance) {
        add('past-edge', el,
          'starts ' + Math.round(-r.left) + 'px outside on the left',
          { width: Math.round(r.width) })
      }
    })

    // 3. Content wider than the element, without permission to scroll
    all.forEach(function (el) {
      if (!visible(el) || scrollable(el) || alreadyReported(el)) return
      var s = getComputedStyle(el)
      if (s.overflowX === 'hidden' || s.overflowX === 'clip') return
      var over = el.scrollWidth - el.clientWidth
      if (over > o.tolerance && el.clientWidth > 0) {
        add('content-too-wide', el,
          'content is ' + Math.round(over) + 'px wider than the available space',
          { width: Math.round(el.clientWidth) })
      }
    })

    // 4. Tables use the width of the content area
    //
    // A table inside an explicit scroll area may be wider — that is the last,
    // permitted step of the ranking for narrow devices. Narrower it is never:
    // that leaves a gap.
    var content = document.querySelector(o.contentArea)
    Array.prototype.forEach.call(root.querySelectorAll('table'), function (t) {
      if (!visible(t)) return
      var area = t.closest('[data-table-area]')
      var mayScroll = (area && scrollable(area)) || insideScroller(t, root)
      var reference = area || content || root
      var expected = innerWidth(reference)
      var actual = t.getBoundingClientRect().width
      if (expected <= 0) return
      if (actual < expected - 2) {
        add('table-too-narrow', t,
          'uses ' + Math.round(actual) + ' of ' + Math.round(expected) + 'px of the available width',
          { missing: Math.round(expected - actual) })
      } else if (actual > expected + o.tolerance && !mayScroll) {
        add('table-too-wide', t,
          'is ' + Math.round(actual - expected) + 'px wider than the content area and ' +
          'sits in no scroll area', {})
      }
    })

    // 5. Touch targets
    var tooSmall = []
    Array.prototype.forEach.call(root.querySelectorAll(INTERACTIVE), function (el) {
      if (!visible(el) || el.disabled) return
      var r = el.getBoundingClientRect()
      var s = getComputedStyle(el)
      if (s.display === 'inline' && el.closest('p, li, td')) return   // text link in prose
      if (r.width + 0.5 < target || r.height + 0.5 < target) {
        tooSmall.push({
          kind: 'target-too-small',
          what: Math.round(r.width) + 'x' + Math.round(r.height) +
                'px, required is ' + target + 'x' + target,
          where: selector(el), text: label(el)
        })
      }
    })
    findings = findings.concat(tooSmall)

    // 6. Gaps in wrapped rows
    all.forEach(function (el) {
      if (!visible(el)) return
      var s = getComputedStyle(el)
      var display = s.display
      if (display !== 'flex' && display !== 'grid' && display !== 'inline-flex') return
      if (display !== 'grid' && s.flexWrap === 'nowrap') return

      var children = Array.prototype.filter.call(el.children, function (c) {
        return visible(c) && getComputedStyle(c).position !== 'absolute'
      })
      if (children.length < 3) return

      // Group into rows via the rounded top edge.
      var rows = []
      children.forEach(function (c) {
        var top = Math.round(c.getBoundingClientRect().top)
        var row = null
        for (var i = 0; i < rows.length; i++) {
          if (Math.abs(rows[i].top - top) <= 4) { row = rows[i]; break }
        }
        if (!row) { row = { top: top, items: [] }; rows.push(row) }
        row.items.push(c)
      })
      if (rows.length < 2) return

      rows.sort(function (a, b) { return a.top - b.top })
      var last = rows[rows.length - 1]
      var fullest = 0
      for (var i = 0; i < rows.length - 1; i++) {
        var used = 0
        rows[i].items.forEach(function (c) { used += c.getBoundingClientRect().width })
        if (used > fullest) fullest = used
      }
      var usedLast = 0
      last.items.forEach(function (c) { usedLast += c.getBoundingClientRect().width })
      var space = innerWidth(el)
      if (space <= 0 || fullest <= 0) return

      var free = space - usedLast
      if (free / space > o.gapFrom && usedLast < fullest - 2) {
        add('row-gap', el,
          'last row leaves ' + Math.round(free) + 'px free (' +
          Math.round(100 * free / space) + '%) — ' + last.items.length +
          ' of ' + rows[0].items.length + ' tiles',
          { rows: rows.length, free: Math.round(free) })
      }
    })

    // 7. Overlays stay inside the visible area
    //
    // Only measurable with the overlay OPEN. A picker near the bottom edge
    // that opens downwards covers its own options — it has to flip. The
    // finding names the free space on the opposite side, because that is
    // the space the flip would use.
    var height = document.documentElement.clientHeight
    Array.prototype.forEach.call(root.querySelectorAll(OVERLAY), function (el) {
      if (!visible(el)) return
      var r = el.getBoundingClientRect()

      // The free space is only what is really on the screen, never the
      // part of the page that lies outside it.
      function free (space) { return Math.round(Math.max(0, Math.min(space, height))) }
      var sides = [
        ['bottom', r.bottom - height, 'upwards', free(r.top)],
        ['top', -r.top, 'downwards', free(height - r.bottom)],
        ['right', r.right - width, 'to the left', free(r.left)],
        ['left', -r.left, 'to the right', free(width - r.right)]
      ]
      sides.forEach(function (side) {
        var name = side[0], over = side[1], flip = side[2], free = side[3]
        if (over <= o.tolerance) return
        findings.push({
          kind: 'overlay-outside',
          what: 'reaches ' + Math.round(over) + 'px past the ' + name +
                ' edge — ' + free + 'px free on the other side, so it has ' +
                'to open ' + flip,
          where: selector(el), text: label(el)
        })
      })

      // Higher than the screen without a scroll area of its own: the lower
      // part cannot be reached at all, and flipping does not help.
      var s = getComputedStyle(el)
      if (r.height > height + o.tolerance &&
          !/^(auto|scroll)$/.test(s.overflowY)) {
        findings.push({
          kind: 'overlay-unreachable',
          what: Math.round(r.height) + 'px high on a screen of ' + height +
                'px, without overflow-y — the lower part cannot be reached',
          where: selector(el), text: label(el)
        })
      }

      // Cut off by an ancestor: the classic picker inside a card with
      // overflow: hidden. Flipping does not help there either.
      var parent = clippingParent(el, root)
      if (parent) {
        var p = parent.getBoundingClientRect()
        var out = Math.max(r.bottom - p.bottom, p.top - r.top,
                           r.right - p.right, p.left - r.left)
        if (out > o.tolerance) {
          findings.push({
            kind: 'overlay-clipped',
            what: 'is cut off ' + Math.round(out) + 'px by ' + selector(parent) +
                  ' — that ancestor clips its overflow',
            where: selector(el), text: label(el)
          })
        }
      }
    })

    return {
      width: width,
      target: target,
      findings: findings,
      interactive: root.querySelectorAll(INTERACTIVE).length,
      overlays: root.querySelectorAll(OVERLAY).length,
      elements: all.length
    }
  }

  // ---------------------------------------------------------------- Report

  var KIND_NAMES = {
    'page-overflow': 'Page scrolls horizontally',
    'overflow-hidden': 'Overflow hidden instead of fixed',
    'past-edge': 'Sticks out past the edge',
    'content-too-wide': 'Content wider than the space',
    'table-too-narrow': 'Table does not use the width',
    'table-too-wide': 'Table wider than the content area',
    'target-too-small': 'Touch target too small',
    'row-gap': 'Hole in the wrapped row',
    'overlay-outside': 'Opened layer leaves the visible area',
    'overlay-unreachable': 'Opened layer higher than the screen',
    'overlay-clipped': 'Opened layer cut off by an ancestor'
  }

  var ORDER = ['page-overflow', 'overlay-outside', 'overlay-clipped',
    'overlay-unreachable', 'past-edge', 'overflow-hidden',
    'content-too-wide', 'table-too-wide', 'table-too-narrow',
    'row-gap', 'target-too-small']

  function report (result, maxPerKind) {
    if (result.error) return result.error
    var limit = maxPerKind || DEFAULTS.maxPerKind
    var lines = ['Overflow check at ' + result.width + 'px, touch target ' +
      result.target + 'px — ' + result.elements + ' elements, ' +
      result.interactive + ' interactive, ' + result.overlays + ' open layers']
    if (!result.findings.length) {
      lines.push('Passed. Nothing sticks out, no gap, no target too small, ' +
        'every open layer inside the visible area.')
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
      if (part.length > limit) {
        lines.push('    … and ' + (part.length - limit) + ' more')
      }
    })
    return lines.join('\n')
  }

  var tool = { check: check, report: report, WIDTHS: WIDTHS, DEFAULTS: DEFAULTS }
  global.neoOverflow = tool
  if (typeof module !== 'undefined' && module.exports) module.exports = tool
})(typeof window !== 'undefined' ? window : globalThis)
