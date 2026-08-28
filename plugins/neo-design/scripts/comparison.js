/*
 * neoComparison: design system versus proposal, in a single image.
 *
 * Every deviation from the design system is a question to the project
 * owner, not a decision by the agent — and a question without a picture
 * is not one. This tool puts both versions side by side, labelled, with a
 * note on what differs.
 *
 * CAREFUL with the image sources: a page on about:blank may not load
 * file:// images — the browser blocks it. Either load the page itself from
 * a file:// address, or pass the images as data: URIs:
 *
 *   const asDataUri = (path) =>
 *     'data:image/png;base64,' + fs.readFileSync(path).toString('base64')
 *
 * If an image fails to load, the tool reports it inside the picture AND in
 * the return value (`errors`). A question with a missing picture is not a
 * question.
 *
 * Usage (Playwright):
 *   await page.addScriptTag({ path: '<plugin>/scripts/comparison.js' })
 *   const size = await page.evaluate(() => neoComparison.render({
 *     heading: 'Create order - form card',
 *     left:  { image: 'file:///.../design.png',   title: 'Design system' },
 *     right: { image: 'file:///.../proposal.png', title: 'Proposal' },
 *     note: 'Two extra fields on the right. Card, spacing and field height unchanged.'
 *   }))
 *   await page.setViewportSize(size)
 *   await page.screenshot({ path: 'question.png' })
 *
 * The colours are fixed: green for the specification, magenta for the
 * proposal. Whoever looks for the legend finds it in the image, not in the
 * text beside it.
 */
(function (global) {
  'use strict'

  var GREEN = '#16A34A'
  var MAGENTA = '#E11D2E'
  var CANVAS = '#F4F4F6'
  var SURFACE = '#FFFFFF'
  var INK = '#17171A'
  var BORDER = '#D9D9DE'
  var FONT = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'

  function el (tag, style, text) {
    var e = document.createElement(tag)
    if (style) e.style.cssText = style
    if (text != null) e.textContent = text
    return e
  }

  var api = {
    /**
     * @param {{heading?:string, note?:string, width?:number,
     *          left:{image:string,title?:string,subtitle?:string},
     *          right:{image:string,title?:string,subtitle?:string}}} opt
     * @returns {Promise<{width:number,height:number,errors:string[],usable:boolean}>}
     */
    render: function (opt) {
      document.documentElement.style.cssText = 'margin:0;padding:0;'
      document.body.style.cssText =
        'margin:0;padding:24px;background:' + CANVAS + ';color:' + INK +
        ';font:15px/1.5 ' + FONT + ';display:inline-block;'

      if (opt.heading) {
        document.body.appendChild(
          el('div', 'font:700 20px/1.3 ' + FONT + ';margin:0 0 4px;', opt.heading))
      }
      document.body.appendChild(
        el('div', 'font:13px/1.4 ' + FONT + ';color:#5C5C66;margin:0 0 16px;',
           'Left the specification from the design system, right the proposal. '
           + 'The project owner decides.'))

      var row = el('div', 'display:flex;gap:20px;align-items:flex-start;')
      document.body.appendChild(row)

      var images = []
      var columns = [
        { side: opt.left, colour: GREEN, fallbackTitle: 'Design system' },
        { side: opt.right, colour: MAGENTA, fallbackTitle: 'Proposal' }
      ]

      columns.forEach(function (c) {
        var column = el('div',
          'background:' + SURFACE + ';border:1px solid ' + BORDER + ';border-radius:10px;' +
          'overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.08);')
        var head = el('div',
          'background:' + c.colour + ';color:#fff;padding:8px 14px;' +
          'font:700 14px/1.3 ' + FONT + ';')
        head.textContent = c.side.title || c.fallbackTitle
        column.appendChild(head)
        if (c.side.subtitle) {
          column.appendChild(el('div',
            'padding:6px 14px;border-bottom:1px solid ' + BORDER + ';' +
            'font:12px/1.4 ' + FONT + ';color:#5C5C66;', c.side.subtitle))
        }
        var image = document.createElement('img')
        image.src = c.side.image
        image.style.cssText = 'display:block;max-width:' + (opt.width || 720) + 'px;height:auto;'
        column.appendChild(image)
        row.appendChild(column)
        images.push({ el: image, column: column, source: c.side.image })
      })

      if (opt.note) {
        var box = el('div',
          'margin:18px 0 0;padding:12px 14px;background:' + SURFACE + ';' +
          'border:1px solid ' + BORDER + ';border-left:5px solid ' + MAGENTA + ';' +
          'border-radius:8px;font:14px/1.5 ' + FONT + ';max-width:960px;white-space:pre-wrap;')
        box.textContent = opt.note
        document.body.appendChild(box)
      }

      return Promise.all(images.map(function (i) {
        return i.el.complete
          ? Promise.resolve()
          : new Promise(function (done) {
              i.el.addEventListener('load', done)
              i.el.addEventListener('error', done)
            })
      })).then(function () {
        return document.fonts && document.fonts.ready ? document.fonts.ready : null
      }).then(function () {
        // An image that did not load is made visible, not kept quiet.
        var errors = []
        images.forEach(function (i) {
          if (i.el.naturalWidth > 0) return
          errors.push(i.source)
          i.el.remove()
          var warning = el('div',
            'padding:24px;background:#FFF1F2;color:' + MAGENTA + ';max-width:420px;' +
            'font:700 14px/1.5 ' + FONT + ';border-top:1px solid ' + BORDER + ';',
            'Image did not load.\n' + i.source +
            '\n\nfile:// images need a file:// page or a data: URI.')
          warning.style.whiteSpace = 'pre-wrap'
          i.column.appendChild(warning)
        })
        var r = document.body.getBoundingClientRect()
        return {
          width: Math.ceil(r.width), height: Math.ceil(r.height),
          errors: errors, usable: errors.length === 0
        }
      })
    }
  }

  global.neoComparison = api
  if (typeof module !== 'undefined' && module.exports) module.exports = api
})(typeof window !== 'undefined' ? window : globalThis)
