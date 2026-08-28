/*
 * NEO annotation layer for documentation screenshots.
 *
 * Injected into the page before the shot and photographed with it. The
 * annotations are therefore crisp at any zoom and sit exactly on the
 * elements instead of on guessed pixel coordinates.
 *
 * Usage (Playwright):
 *   await page.addScriptTag({ path: 'tools/annotate.js' })
 *   await page.evaluate(() => {
 *     neoAnnotate.frame('[data-test="create-order"]', { number: 1 })
 *     neoAnnotate.arrow('#save', { text: 'Do not forget to save' })
 *     neoAnnotate.note({ text: 'The interval applies per order.', at: '#interval' })
 *   })
 *   await page.screenshot({ path: '...', fullPage: true })
 *
 * The colours are deliberately fixed and do not follow the theme: an
 * annotation is an annotation and has to read the same on a light and on a
 * dark background. That is why every shape carries a white casing under
 * the red.
 */
(function () {
  'use strict'

  var RED = '#E11D2E'
  var WHITE = '#FFFFFF'
  var INK = '#1A1A1A'
  var HIGHLIGHT = 'rgba(255, 214, 0, 0.45)'
  var FONT = '600 14px/1.4 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'
  var LAYER_ID = 'neo-annotation-layer'

  function layer () {
    var existing = document.getElementById(LAYER_ID)
    if (existing) return existing
    var el = document.createElement('div')
    el.id = LAYER_ID
    // On the root element: absolute children then live in document coordinates.
    el.style.cssText = 'position:absolute;left:0;top:0;width:0;height:0;' +
      'z-index:2147483647;pointer-events:none;'
    document.documentElement.appendChild(el)
    return el
  }

  /** Document coordinates of an element. */
  function metrics (target) {
    var el = typeof target === 'string' ? document.querySelector(target) : target
    if (!el) throw new Error('neoAnnotate: no element for "' + target + '"')
    var r = el.getBoundingClientRect()
    return {
      x: r.left + window.scrollX,
      y: r.top + window.scrollY,
      width: r.width,
      height: r.height,
      el: el
    }
  }

  function allMetrics (target, all) {
    if (typeof target !== 'string') return [metrics(target)]
    if (!all) return [metrics(target)]
    var list = Array.prototype.slice.call(document.querySelectorAll(target))
    if (!list.length) throw new Error('neoAnnotate: no element for "' + target + '"')
    return list.map(metrics)
  }

  function box (style) {
    var el = document.createElement('div')
    el.style.cssText = 'position:absolute;box-sizing:border-box;' + style
    layer().appendChild(el)
    return el
  }

  function svg (x, y, width, height) {
    var el = document.createElementNS('http://www.w3.org/2000/svg', 'svg')
    el.setAttribute('width', String(width))
    el.setAttribute('height', String(height))
    el.setAttribute('viewBox', '0 0 ' + width + ' ' + height)
    el.style.cssText = 'position:absolute;left:' + x + 'px;top:' + y + 'px;overflow:visible;'
    layer().appendChild(el)
    return el
  }

  function line (el, d, colour, thickness) {
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path')
    path.setAttribute('d', d)
    path.setAttribute('fill', 'none')
    path.setAttribute('stroke', colour)
    path.setAttribute('stroke-width', String(thickness))
    path.setAttribute('stroke-linecap', 'round')
    path.setAttribute('stroke-linejoin', 'round')
    el.appendChild(path)
    return path
  }

  /** Numbered badge as a circle, cased in white. */
  function badge (x, y, number) {
    var d = 26
    var el = box(
      'left:' + (x - d / 2) + 'px;top:' + (y - d / 2) + 'px;width:' + d + 'px;height:' + d + 'px;' +
      'border-radius:50%;background:' + RED + ';color:' + WHITE + ';' +
      'box-shadow:0 0 0 3px ' + WHITE + ', 0 1px 4px rgba(0,0,0,.35);' +
      'font:700 14px/' + d + 'px system-ui,sans-serif;text-align:center;')
    el.textContent = String(number)
    return el
  }

  var api = {
    /**
     * Red frame around an element, optionally with a badge and a caption.
     * @param {string|Element} target
     * @param {{number?:number, text?:string, padding?:number, all?:boolean}} [opt]
     */
    frame: function (target, opt) {
      opt = opt || {}
      var padding = opt.padding == null ? 6 : opt.padding
      allMetrics(target, opt.all).forEach(function (m) {
        box(
          'left:' + (m.x - padding) + 'px;top:' + (m.y - padding) + 'px;' +
          'width:' + (m.width + padding * 2) + 'px;height:' + (m.height + padding * 2) + 'px;' +
          'border:3px solid ' + RED + ';border-radius:6px;' +
          'box-shadow:0 0 0 2px rgba(255,255,255,.9), inset 0 0 0 2px rgba(255,255,255,.9);')
        if (opt.number != null) badge(m.x - padding, m.y - padding, opt.number)
        if (opt.text) api.note({ text: opt.text, at: m.el, position: 'bottom' })
      })
      return api
    },

    /**
     * Red arrow pointing at an element.
     * @param {string|Element} target
     * @param {{direction?:'left'|'right'|'top'|'bottom', length?:number, text?:string}} [opt]
     */
    arrow: function (target, opt) {
      opt = opt || {}
      var m = metrics(target)
      var direction = opt.direction || (m.x > 220 ? 'left' : 'right')
      var length = opt.length == null ? 110 : opt.length
      var tipX, tipY, startX, startY
      var distance = 10

      if (direction === 'left') {
        tipX = m.x - distance; tipY = m.y + m.height / 2
        startX = tipX - length; startY = tipY - length * 0.35
      } else if (direction === 'right') {
        tipX = m.x + m.width + distance; tipY = m.y + m.height / 2
        startX = tipX + length; startY = tipY - length * 0.35
      } else if (direction === 'top') {
        tipX = m.x + m.width / 2; tipY = m.y - distance
        startX = tipX + length * 0.35; startY = tipY - length
      } else {
        tipX = m.x + m.width / 2; tipY = m.y + m.height + distance
        startX = tipX + length * 0.35; startY = tipY + length
      }

      var surface = svg(0, 0, 1, 1)
      var midX = (startX + tipX) / 2 + (tipY - startY) * 0.12
      var midY = (startY + tipY) / 2 + (startX - tipX) * 0.12
      var d = 'M ' + startX + ' ' + startY + ' Q ' + midX + ' ' + midY +
              ' ' + tipX + ' ' + tipY
      line(surface, d, WHITE, 9)   // casing, so the arrow reads on any background
      line(surface, d, RED, 4)

      // Head from the tangent at the end point
      var angle = Math.atan2(tipY - midY, tipX - midX)
      var k = 15
      var p1 = [tipX - k * Math.cos(angle - 0.42), tipY - k * Math.sin(angle - 0.42)]
      var p2 = [tipX - k * Math.cos(angle + 0.42), tipY - k * Math.sin(angle + 0.42)]
      var head = 'M ' + p1[0] + ' ' + p1[1] + ' L ' + tipX + ' ' + tipY +
                 ' L ' + p2[0] + ' ' + p2[1] + ' Z'
      var f = document.createElementNS('http://www.w3.org/2000/svg', 'path')
      f.setAttribute('d', head)
      f.setAttribute('fill', RED)
      f.setAttribute('stroke', WHITE)
      f.setAttribute('stroke-width', '3')
      f.setAttribute('paint-order', 'stroke')
      surface.appendChild(f)

      if (opt.text) {
        var caption = box(
          'left:' + startX + 'px;top:' + startY + 'px;max-width:260px;' +
          'transform:translate(' + (direction === 'left' ? '-100%' : '0') + ', -120%);' +
          'padding:6px 10px;border-radius:6px;background:' + RED + ';color:' + WHITE + ';' +
          'box-shadow:0 0 0 2px ' + WHITE + ';font:' + FONT + ';')
        caption.textContent = opt.text
      }
      return api
    },

    /** Badge without a frame, at the top left corner of the element. */
    number: function (target, n) {
      var m = metrics(target)
      badge(m.x, m.y, n)
      return api
    },

    /**
     * Note box with text, optionally aligned to an element.
     * @param {{text:string, at?:string|Element,
     *          position?:'top'|'bottom'|'left'|'right', width?:number}} opt
     */
    note: function (opt) {
      var width = opt.width || 300
      var x = 24, y = 24
      var position = opt.position || 'bottom'
      if (opt.at) {
        var m = metrics(opt.at)
        if (position === 'top') { x = m.x; y = m.y - 16 }
        else if (position === 'left') { x = m.x - width - 16; y = m.y }
        else if (position === 'right') { x = m.x + m.width + 16; y = m.y }
        else { x = m.x; y = m.y + m.height + 12 }
      }
      var el = box(
        'left:' + Math.max(8, x) + 'px;top:' + Math.max(8, y) + 'px;width:' + width + 'px;' +
        (position === 'top' ? 'transform:translateY(-100%);' : '') +
        'padding:10px 12px;border:2px solid ' + RED + ';border-left-width:6px;border-radius:8px;' +
        'background:' + WHITE + ';color:' + INK + ';' +
        'box-shadow:0 2px 10px rgba(0,0,0,.25);font:' + FONT + ';white-space:pre-wrap;')
      el.textContent = opt.text
      return api
    },

    /**
     * Highlighter over the text lines of an element.
     *
     * Computed from a range and its line boxes, not from the element's own
     * rectangle: otherwise the highlight would run across the whole column
     * width of a heading instead of across the word.
     */
    highlight: function (target, opt) {
      opt = opt || {}
      allMetrics(target, opt.all).forEach(function (m) {
        var rects = []
        try {
          var range = document.createRange()
          range.selectNodeContents(m.el)
          rects = Array.prototype.slice.call(range.getClientRects())
          range.detach && range.detach()
        } catch (e) { rects = [] }
        if (!rects.length) {
          rects = [{ left: m.x - window.scrollX, top: m.y - window.scrollY,
                     width: m.width, height: m.height }]
        }
        rects.forEach(function (r) {
          if (r.width < 1 || r.height < 1) return
          box(
            'left:' + (r.left + window.scrollX - 2) + 'px;' +
            'top:' + (r.top + window.scrollY - 1) + 'px;' +
            'width:' + (r.width + 4) + 'px;height:' + (r.height + 2) + 'px;' +
            'background:' + HIGHLIGHT + ';mix-blend-mode:multiply;border-radius:3px;')
        })
      })
      return api
    },

    /** Dims everything except the target. */
    spotlight: function (target, opt) {
      opt = opt || {}
      var padding = opt.padding == null ? 8 : opt.padding
      var m = metrics(target)
      var width = Math.max(document.documentElement.scrollWidth, window.innerWidth)
      var height = Math.max(document.documentElement.scrollHeight, window.innerHeight)
      var dim = opt.dim == null ? 0.55 : opt.dim
      var parts = [
        [0, 0, width, m.y - padding],
        [0, m.y + m.height + padding, width, height - (m.y + m.height + padding)],
        [0, m.y - padding, m.x - padding, m.height + padding * 2],
        [m.x + m.width + padding, m.y - padding,
         width - (m.x + m.width + padding), m.height + padding * 2]
      ]
      parts.forEach(function (p) {
        if (p[2] <= 0 || p[3] <= 0) return
        box('left:' + p[0] + 'px;top:' + p[1] + 'px;width:' + p[2] + 'px;height:' + p[3] +
            'px;background:rgba(0,0,0,' + dim + ');')
      })
      return api
    },

    /** Clip for a detail screenshot: document coordinates of the element. */
    clip: function (target, padding) {
      var p = padding == null ? 12 : padding
      var m = metrics(target)
      return { x: m.x - p, y: m.y - p, width: m.width + p * 2, height: m.height + p * 2 }
    },

    /** Removes all annotations. */
    clear: function () {
      var el = document.getElementById(LAYER_ID)
      if (el) el.remove()
      return api
    }
  }

  window.neoAnnotate = api
})()
