// Copyright (c) 2026 alchaincyf (花叔, Peanut). MIT License.
//
// Independent implementation: written from scratch against a spec that only describes
// inputs, outputs, and observable behavior; no other html2pptx source was consulted.
// Depends on the two public libraries Playwright and pptxgenjs.
//
// Responsibility: take a single 960pt×540pt HTML page (by convention; the body's actual
// size is the source of truth), open it in a real Chromium via Playwright, measure each
// element's rendered result (position/size/computed style), and translate it into native
// editable pptxgenjs objects (text frames / shapes / lines / pictures).

'use strict';

const path = require('path');
const { chromium } = require('playwright');

// ---- Unit conversion constants ----
const PT_PER_PX = 0.75; // CSS px -> pt
const IN_PER_PX = 1 / 96; // CSS px -> inch
const EMU_PER_INCH = 914400;

function toPt(px) {
  return px * PT_PER_PX;
}
function toIn(px) {
  return px * IN_PER_PX;
}

// ============================================================================
// In-browser extraction logic: handed to page.evaluate as one whole string function and
// run in the page context; it must not rely on outer closure variables (Playwright
// serializes Function.toString() and re-evaluates it in the browser).
// ============================================================================
function extractPageDataInBrowser() {
  const PT_PER_PX = 0.75;
  function toPt(px) {
    return px * PT_PER_PX;
  }
  function toIn(px) {
    return px / 96;
  }
  const SINGLE_WEIGHT_FONTS = ['impact'];
  const INLINE_TAGS = new Set(['SPAN', 'B', 'STRONG', 'I', 'EM', 'U']);
  const TEXT_TAG_BG_CHECK = new Set(['P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'UL', 'OL', 'LI']);
  const TEXT_ELEMENT_TAGS = new Set(['P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'LI']);
  const MANUAL_BULLET_CHARS_VALIDATE = ['•', '-', '*', '▪', '▸', '○', '●', '◆', '◇', '■', '□'];
  const MANUAL_BULLET_CHARS_STRIP = ['•', '-', '*', '▪', '▸'];

  const errors = [];
  const elements = [];
  const placeholders = [];
  const consumed = new Set();

  // ---- Basic helpers ----
  function parsePx(v) {
    const n = parseFloat(v);
    return isNaN(n) ? 0 : n;
  }

  function rectOf(el) {
    const r = el.getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height };
  }

  function truncate(str, max) {
    if (str.length <= max) return str;
    return str.slice(0, max) + '...';
  }

  function collapseWs(s) {
    return s.replace(/[\t\n\r ]+/g, ' ');
  }

  function parseColorString(str) {
    if (!str) return null;
    const m = /rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)/i.exec(str);
    if (!m) return null;
    const r = Math.max(0, Math.min(255, Math.round(parseFloat(m[1]))));
    const g = Math.max(0, Math.min(255, Math.round(parseFloat(m[2]))));
    const b = Math.max(0, Math.min(255, Math.round(parseFloat(m[3]))));
    const hasAlpha = m[4] !== undefined;
    const alpha = hasAlpha ? parseFloat(m[4]) : 1;
    const hex = [r, g, b].map((v) => v.toString(16).padStart(2, '0')).join('');
    return { hex, alpha, hasAlpha };
  }

  function isVisibleColor(c) {
    return !!c && c.alpha > 0;
  }

  // {color, transparency?} — transparency is included only when an explicit alpha channel was parsed
  function fillFieldOf(c) {
    const out = { color: c.hex };
    if (c.hasAlpha) out.transparency = Math.round((1 - c.alpha) * 100);
    return out;
  }

  function firstFontFamily(v) {
    if (!v) return '';
    const first = v.split(',')[0].trim();
    return first.replace(/^["']|["']$/g, '');
  }

  function isSingleWeightFont(fontFace) {
    return SINGLE_WEIGHT_FONTS.indexOf((fontFace || '').toLowerCase()) !== -1;
  }

  function normalizeAlign(v) {
    return v === 'start' ? 'left' : v;
  }

  function parseLineHeightPt(lineHeightStr, fontSizePt) {
    const v = parseFloat(lineHeightStr);
    if (!isNaN(v) && /px\s*$/.test(String(lineHeightStr).trim())) {
      return v * PT_PER_PX;
    }
    // Defensive fallback: real Chromium's computed line-height is almost always an
    // already-resolved px value, so the fontSize*1.2 branch here should never be hit.
    return fontSizePt * 1.2;
  }

  function applyTextTransform(str, tt) {
    if (tt === 'uppercase') return str.toUpperCase();
    if (tt === 'lowercase') return str.toLowerCase();
    if (tt === 'capitalize') return str.replace(/\b\w/g, (c) => c.toUpperCase());
    return str;
  }

  function getBordersInfo(cs) {
    return {
      top: { w: parsePx(cs.borderTopWidth), c: cs.borderTopColor },
      right: { w: parsePx(cs.borderRightWidth), c: cs.borderRightColor },
      bottom: { w: parsePx(cs.borderBottomWidth), c: cs.borderBottomColor },
      left: { w: parsePx(cs.borderLeftWidth), c: cs.borderLeftColor },
    };
  }

  function computeRectRadius(cs, widthPx, heightPx) {
    const raw = (cs.borderTopLeftRadius || '0px').trim();
    const m = /^(-?[\d.]+)(px|pt|%)?$/.exec(raw);
    if (!m) return 0;
    const val = parseFloat(m[1]);
    const unit = m[2] || 'px';
    if (!val) return 0;
    if (unit === '%') {
      if (val >= 50) return 1;
      return ((val / 100) * Math.min(widthPx, heightPx)) / 96;
    }
    if (unit === 'pt') return val / 72;
    return val / 96;
  }

  function parseBoxShadow(str) {
    if (!str || str === 'none') return null;
    if (/inset/i.test(str)) return null;
    const colorMatch = str.match(/rgba?\([^)]+\)/i);
    const colorParsed = colorMatch ? parseColorString(colorMatch[0]) : null;
    const withoutColor = colorMatch ? str.replace(colorMatch[0], '') : str;
    const nums = withoutColor.match(/-?[\d.]+px/g) || [];
    if (nums.length < 2) return null;
    const vals = nums.map((s) => parseFloat(s));
    const offsetX = vals[0];
    const offsetY = vals[1];
    const blur = vals[2] || 0;
    const offsetPt = Math.hypot(offsetX, offsetY) * PT_PER_PX;
    let angleDeg = (Math.atan2(offsetY, offsetX) * 180) / Math.PI;
    angleDeg = ((angleDeg % 360) + 360) % 360;
    const blurPt = blur * PT_PER_PX;
    const color = colorParsed ? colorParsed.hex : '000000';
    const opacity = colorParsed && colorParsed.hasAlpha ? colorParsed.alpha : 0.5;
    return { type: 'outer', angle: angleDeg, blur: blurPt, color, offset: offsetPt, opacity };
  }

  function violationOf(el) {
    const cs = getComputedStyle(el);
    const bg = parseColorString(cs.backgroundColor);
    if (isVisibleColor(bg)) return 'background';
    const b = getBordersInfo(cs);
    if (b.top.w > 0 || b.right.w > 0 || b.bottom.w > 0 || b.left.w > 0) return 'border';
    if (cs.boxShadow && cs.boxShadow !== 'none') return 'shadow';
    return null;
  }

  // ---- Rotation angle + position/size (section 4.5) ----
  function computeRotationDeg(cs) {
    let angle = 0;
    if (cs.writingMode === 'vertical-rl') angle += 90;
    else if (cs.writingMode === 'vertical-lr') angle += 270;
    const t = cs.transform;
    if (t && t !== 'none') {
      const rm = /rotate\(([-\d.]+)deg\)/.exec(t);
      if (rm) {
        angle += parseFloat(rm[1]);
      } else {
        const mm = /matrix\(([^)]+)\)/.exec(t);
        if (mm) {
          const parts = mm[1].split(',').map((s) => parseFloat(s.trim()));
          angle += (Math.atan2(parts[1], parts[0]) * 180) / Math.PI;
        }
      }
    }
    return ((angle % 360) + 360) % 360;
  }

  function computeGeometryPx(el, rotationDeg) {
    const r = el.getBoundingClientRect();
    if (rotationDeg === 90 || rotationDeg === 270) {
      const cx = r.left + r.width / 2;
      const cy = r.top + r.height / 2;
      const w = r.height;
      const h = r.width;
      return { x: cx - w / 2, y: cy - h / 2, w, h };
    }
    if (rotationDeg !== 0) {
      const cx = r.left + r.width / 2;
      const cy = r.top + r.height / 2;
      const w = el.offsetWidth;
      const h = el.offsetHeight;
      return { x: cx - w / 2, y: cy - h / 2, w, h };
    }
    return { x: r.left, y: r.top, w: r.width, h: r.height };
  }

  // ---- 4.5.3 Generic inline rich-text parsing ----
  function hasInlineFormatting(el) {
    return !!el.querySelector('span,b,strong,i,em,u,br');
  }

  function buildRuns(containerEl, marginErrsOut) {
    const rawRuns = [];

    function styleOf(el) {
      const cs = getComputedStyle(el);
      const fontSizePt = parseFloat(cs.fontSize) * PT_PER_PX;
      const fontFace = firstFontFamily(cs.fontFamily);
      let bold = cs.fontWeight === 'bold' || parseInt(cs.fontWeight, 10) >= 600;
      if (isSingleWeightFont(fontFace)) bold = false;
      const italic = cs.fontStyle === 'italic';
      const deco = cs.textDecorationLine || cs.textDecoration || '';
      const underline = deco.indexOf('underline') !== -1;
      const colorParsed = parseColorString(cs.color);
      const textTransform = cs.textTransform;
      return { fontSizePt, bold, italic, underline, colorParsed, textTransform };
    }

    function sameStyle(a, b) {
      if (!a || !b) return false;
      return (
        a.fontSizePt === b.fontSizePt &&
        a.bold === b.bold &&
        a.italic === b.italic &&
        a.underline === b.underline &&
        a.textTransform === b.textTransform &&
        JSON.stringify(a.colorParsed) === JSON.stringify(b.colorParsed)
      );
    }

    function append(text, style) {
      if (text === '') return;
      const last = rawRuns[rawRuns.length - 1];
      if (last && sameStyle(last.style, style)) {
        last.text += text;
      } else {
        rawRuns.push({ text, style });
      }
    }

    function checkInlineMargins(el, tag) {
      const cs = getComputedStyle(el);
      ['Left', 'Right', 'Top', 'Bottom'].forEach((dir) => {
        const v = parsePx(cs['margin' + dir]);
        if (v !== 0) {
          marginErrsOut.push(
            `Inline element <${tag.toLowerCase()}> has a non-zero margin-${dir.toLowerCase()} (inline elements do not support margin — remove it).`
          );
        }
      });
    }

    function walk(node) {
      if (node.nodeType === 3) {
        const collapsed = collapseWs(node.textContent);
        if (collapsed === '') return;
        const style = styleOf(node.parentElement);
        append(applyTextTransform(collapsed, style.textTransform), style);
        return;
      }
      if (node.nodeType !== 1) return;
      const tag = node.tagName;
      if (tag === 'BR') {
        const style = styleOf(node.parentElement);
        append('\n', style);
        return;
      }
      if (INLINE_TAGS.has(tag)) {
        const text = node.textContent;
        if (!text || !text.trim()) return;
        checkInlineMargins(node, tag);
        Array.from(node.childNodes).forEach(walk);
        return;
      }
      // Unrecognized tags (e.g. <code>): skipped entirely, the text disappears from the
      // output (existing behavior; do not extend).
    }

    Array.from(containerEl.childNodes).forEach(walk);

    if (rawRuns.length > 0) {
      rawRuns[0].text = rawRuns[0].text.replace(/^ +/, '');
      rawRuns[rawRuns.length - 1].text = rawRuns[rawRuns.length - 1].text.replace(/ +$/, '');
    }

    // pptxgenjs TextProps expects { text, options }: options carries only the overrides
    // that differ from the inherited style; missing fields are left for pptxgenjs itself
    // to resolve from the top-level / previous run's defaults.
    return rawRuns
      .filter((r) => r.text !== '')
      .map((r) => {
        const options = { fontSize: r.style.fontSizePt };
        if (r.style.bold) options.bold = true;
        if (r.style.italic) options.italic = true;
        if (r.style.underline) options.underline = true;
        const c = r.style.colorParsed;
        const isPureBlack = c && c.hex === '000000' && !c.hasAlpha;
        if (c && !isPureBlack) {
          options.color = c.hex;
          if (c.hasAlpha) options.transparency = Math.round((1 - c.alpha) * 100);
        }
        return { text: r.text, options };
      });
  }

  function stripLeadingManualBullet(run) {
    for (const ch of MANUAL_BULLET_CHARS_STRIP) {
      if (run.text.indexOf(ch) === 0) {
        run.text = run.text.slice(1).replace(/^\s+/, '');
        return;
      }
    }
  }

  // ---- 4.2 Placeholders ----
  function processPlaceholder(el) {
    consumed.add(el);
    Array.from(el.querySelectorAll('*')).forEach((d) => consumed.add(d));
    const rect = rectOf(el);
    if (rect.w === 0 || rect.h === 0) {
      const dim = rect.w === 0 ? 'width' : 'height';
      const id = el.id || 'unnamed';
      errors.push(`Placeholder #${id} renders with a ${dim} of 0 — check its CSS layout`);
      return;
    }
    const id = el.id || 'placeholder-' + placeholders.length;
    placeholders.push({ id, x: toIn(rect.x), y: toIn(rect.y), w: toIn(rect.w), h: toIn(rect.h) });
  }

  // ---- 4.3 Images ----
  function processImage(el) {
    const rect = rectOf(el);
    if (rect.w === 0 || rect.h === 0) return;
    elements.push({ type: 'image', src: el.src, x: toIn(rect.x), y: toIn(rect.y), w: toIn(rect.w), h: toIn(rect.h) });
  }

  // ---- 4.4 div ----
  function buildBorderLines(rect, b) {
    const out = [];
    const sides = [
      { info: b.top, geo: () => ({ x: rect.x, y: rect.y + b.top.w / 2, w: rect.w, h: 0 }) },
      { info: b.right, geo: () => ({ x: rect.x + rect.w - b.right.w / 2, y: rect.y, w: 0, h: rect.h }) },
      { info: b.bottom, geo: () => ({ x: rect.x, y: rect.y + rect.h - b.bottom.w / 2, w: rect.w, h: 0 }) },
      { info: b.left, geo: () => ({ x: rect.x + b.left.w / 2, y: rect.y, w: 0, h: rect.h }) },
    ];
    sides.forEach((s) => {
      if (s.info.w > 0) {
        const g = s.geo();
        const c = parseColorString(s.info.c);
        out.push({
          type: 'line',
          x: toIn(g.x),
          y: toIn(g.y),
          w: toIn(g.w),
          h: toIn(g.h),
          color: c ? c.hex : '000000',
          widthPt: toPt(s.info.w),
        });
      }
    });
    return out;
  }

  function processDiv(div) {
    // 1: bare-text validation (always runs; never skipped because of the background-image violation below)
    const rawDirectText = Array.from(div.childNodes)
      .filter((n) => n.nodeType === 3)
      .map((n) => n.textContent)
      .join('')
      .trim();
    if (rawDirectText) {
      errors.push(
        `<div> has text written directly inside it ("${truncate(rawDirectText, 50)}") — it will not appear in the PPT; wrap it in <p>, <h1>-<h6>, or <ul>/<ol> instead`
      );
    }

    // 2: background-image validation (a hit emits no shape/line but does not consume the node; descendants are still traversed)
    const cs = getComputedStyle(div);
    if (cs.backgroundImage && cs.backgroundImage !== 'none') {
      if (/gradient/i.test(cs.backgroundImage)) {
        errors.push(
          '<div> backgrounds cannot use CSS gradients: switch to a solid background-color, or export the gradient to PNG first and place it via <img> / slide.addImage()'
        );
      } else {
        errors.push(
          '<div> cannot use background-image: turn the picture into an <img> tag, or layer it on separately with slide.addImage()'
        );
      }
      return;
    }

    const rect = rectOf(div);
    if (rect.w === 0 || rect.h === 0) return;

    const bgColor = parseColorString(cs.backgroundColor);
    const hasBg = isVisibleColor(bgColor);
    const b = getBordersInfo(cs);
    const hasBorder = b.top.w > 0 || b.right.w > 0 || b.bottom.w > 0 || b.left.w > 0;
    const hasUniformBorder = hasBorder && b.top.w === b.right.w && b.right.w === b.bottom.w && b.bottom.w === b.left.w;

    let shapeEl = null;
    let lineEls = [];

    if (hasBorder && !hasUniformBorder) {
      lineEls = buildBorderLines(rect, b);
    }

    if (hasBg || hasBorder) {
      if (hasBg || hasUniformBorder) {
        const shadow = parseBoxShadow(cs.boxShadow);
        shapeEl = {
          type: 'shape',
          x: toIn(rect.x),
          y: toIn(rect.y),
          w: toIn(rect.w),
          h: toIn(rect.h),
          fill: hasBg ? fillFieldOf(bgColor) : null,
          line: hasUniformBorder ? { color: parseColorString(b.top.c).hex, width: toPt(b.top.w) } : null,
          rectRadius: computeRectRadius(cs, rect.w, rect.h),
          shadow,
        };
      }
      consumed.add(div);
    }

    if (shapeEl) elements.push(shapeEl);
    lineEls.forEach((l) => elements.push(l));
  }

  // ---- 4.1 data-pptx-merge containers ----
  function processMergeContainer(container) {
    const rect = rectOf(container);
    if (rect.w === 0 || rect.h === 0) {
      consumed.add(container);
      return;
    }

    const nested = container.querySelectorAll('[data-pptx-merge="true"]');
    if (nested.length > 0) {
      errors.push('data-pptx-merge containers cannot be nested. Remove the inner data-pptx-merge="true" attribute.');
      consumed.add(container);
      return;
    }

    const cs = getComputedStyle(container);
    if (cs.backgroundImage && cs.backgroundImage !== 'none') {
      if (/gradient/i.test(cs.backgroundImage)) {
        errors.push(
          'CSS gradients are not supported on data-pptx-merge containers. Use a solid background-color, or overlay the gradient with slide.addImage().'
        );
      } else {
        errors.push(
          'data-pptx-merge containers do not support background-image. Use a solid background-color/border, or overlay the picture with slide.addImage().'
        );
      }
      consumed.add(container);
      return;
    }

    const paragraphs = Array.from(container.querySelectorAll('p,h1,h2,h3,h4,h5,h6'));
    if (paragraphs.length === 0) {
      errors.push(
        'data-pptx-merge container has no mergeable text elements. Remove data-pptx-merge or add <p>/<h1>-<h6> text inside it.'
      );
      consumed.add(container);
      return;
    }

    const bgColor = parseColorString(cs.backgroundColor);
    const hasBg = isVisibleColor(bgColor);
    const b = getBordersInfo(cs);
    const hasUniformBorder = b.top.w > 0 && b.top.w === b.right.w && b.right.w === b.bottom.w && b.bottom.w === b.left.w;

    let shapeEl = null;
    if (hasBg || hasUniformBorder) {
      const shadow = parseBoxShadow(cs.boxShadow);
      shapeEl = {
        type: 'shape',
        x: toIn(rect.x),
        y: toIn(rect.y),
        w: toIn(rect.w),
        h: toIn(rect.h),
        fill: hasBg ? fillFieldOf(bgColor) : null,
        line: hasUniformBorder ? { color: parseColorString(b.top.c).hex, width: toPt(b.top.w) } : null,
        rectRadius: computeRectRadius(cs, rect.w, rect.h),
        shadow,
      };
    }

    // Frame-level base style is taken from the first text descendant
    const baseEl = paragraphs[0];
    const baseCs = getComputedStyle(baseEl);
    const baseFontSizePt = parseFloat(baseCs.fontSize) * PT_PER_PX;
    const baseFontFace = firstFontFamily(baseCs.fontFamily);
    const baseColorParsed = parseColorString(baseCs.color);
    const baseAlign = normalizeAlign(baseCs.textAlign);
    const baseLineSpacingPt = parseLineHeightPt(baseCs.lineHeight, baseFontSizePt);

    const marginArr = [
      toPt(parsePx(cs.paddingLeft)),
      toPt(parsePx(cs.paddingRight)),
      toPt(parsePx(cs.paddingBottom)),
      toPt(parsePx(cs.paddingTop)),
    ];

    paragraphs.forEach((p) => consumed.add(p));
    consumed.add(container);

    const allRuns = [];
    paragraphs.forEach((p, idx) => {
      const marginErrs = [];
      const runs = buildRuns(p, marginErrs);
      errors.push(...marginErrs);
      if (runs.length === 0) return;
      if (idx < paragraphs.length - 1) {
        runs[runs.length - 1].options.breakLine = true;
      }
      allRuns.push(...runs);
    });

    if (allRuns.length === 0) return;

    if (shapeEl) elements.push(shapeEl);
    elements.push({
      type: 'merged-text',
      x: toIn(rect.x),
      y: toIn(rect.y),
      w: toIn(rect.w),
      h: toIn(rect.h),
      fontSize: baseFontSizePt,
      fontFace: baseFontFace,
      color: baseColorParsed ? baseColorParsed.hex : null,
      transparency: baseColorParsed && baseColorParsed.hasAlpha ? Math.round((1 - baseColorParsed.alpha) * 100) : null,
      align: baseAlign,
      lineSpacing: baseLineSpacingPt,
      marginArr,
      items: allRuns,
    });
  }

  // ---- 4.6 Lists ----
  function processList(listEl) {
    const rect = rectOf(listEl);
    if (rect.w === 0 || rect.h === 0) return;

    const cs = getComputedStyle(listEl);
    const paddingLeftPt = toPt(parsePx(cs.paddingLeft));
    const half = paddingLeftPt / 2;

    const liEls = Array.from(listEl.querySelectorAll('li'));
    liEls.forEach((li) => consumed.add(li));
    consumed.add(listEl);
    if (liEls.length === 0) return;

    const baseCs = getComputedStyle(liEls[0]);
    const baseFontSizePt = parseFloat(baseCs.fontSize) * PT_PER_PX;
    const baseFontFace = firstFontFamily(baseCs.fontFamily);
    const baseColorParsed = parseColorString(baseCs.color);
    const baseAlign = normalizeAlign(baseCs.textAlign);
    const baseLineSpacingPt = parseLineHeightPt(baseCs.lineHeight, baseFontSizePt);
    const paraSpaceAfterPt = toPt(parsePx(baseCs.marginBottom));

    const allRuns = [];
    liEls.forEach((li, idx) => {
      const marginErrs = [];
      const runs = buildRuns(li, marginErrs);
      errors.push(...marginErrs);
      if (runs.length === 0) return;
      stripLeadingManualBullet(runs[0]);
      runs[0].options.bullet = { indent: half };
      if (idx < liEls.length - 1) {
        runs[runs.length - 1].options.breakLine = true;
      }
      allRuns.push(...runs);
    });

    if (allRuns.length === 0) return;

    elements.push({
      type: 'list',
      x: toIn(rect.x),
      y: toIn(rect.y),
      w: toIn(rect.w),
      h: toIn(rect.h),
      fontSize: baseFontSizePt,
      fontFace: baseFontFace,
      color: baseColorParsed ? baseColorParsed.hex : null,
      transparency: baseColorParsed && baseColorParsed.hasAlpha ? Math.round((1 - baseColorParsed.alpha) * 100) : null,
      align: baseAlign,
      lineSpacing: baseLineSpacingPt,
      paraSpaceAfter: paraSpaceAfterPt,
      marginArr: [half, 0, 0, 0],
      items: allRuns,
    });
  }

  // ---- 4.5 Single text tags (including the li fallback branch mentioned in the 4.5 preamble) ----
  function processTextElement(el) {
    const tag = el.tagName;
    const rect = rectOf(el);
    const collapsedFull = collapseWs(el.textContent).trim();

    if (rect.w === 0 || rect.h === 0 || collapsedFull === '') return;

    if (tag !== 'LI') {
      const m = /^([•\-*▪▸○●◆◇■□])\s/.exec(collapsedFull);
      if (m) {
        errors.push(
          `<${tag.toLowerCase()}> starts with a hand-typed bullet ("${truncate(collapsedFull, 20)}") — use <ul>/<ol> for lists; do not type the bullet yourself`
        );
        return;
      }
    }

    const cs = getComputedStyle(el);
    const rotation = computeRotationDeg(cs);
    const geomPx = computeGeometryPx(el, rotation);

    const fontSizePt = parseFloat(cs.fontSize) * PT_PER_PX;
    const fontFace = firstFontFamily(cs.fontFamily);
    const colorParsed = parseColorString(cs.color);
    const align = normalizeAlign(cs.textAlign);
    const lineSpacingPt = parseLineHeightPt(cs.lineHeight, fontSizePt);
    const marginTopPt = toPt(parsePx(cs.marginTop));
    const marginBottomPt = toPt(parsePx(cs.marginBottom));
    const paddingArr = [
      toPt(parsePx(cs.paddingLeft)),
      toPt(parsePx(cs.paddingRight)),
      toPt(parsePx(cs.paddingBottom)),
      toPt(parsePx(cs.paddingTop)),
    ];
    const hasPadding = paddingArr.some((v) => v !== 0);

    let boldBase = cs.fontWeight === 'bold' || parseInt(cs.fontWeight, 10) >= 600;
    if (isSingleWeightFont(fontFace)) boldBase = false;
    const italicBase = cs.fontStyle === 'italic';
    const decoBase = cs.textDecorationLine || cs.textDecoration || '';
    const underlineBase = decoBase.indexOf('underline') !== -1;

    let textOut;
    let effectiveLineSpacing = lineSpacingPt;

    if (hasInlineFormatting(el)) {
      const marginErrs = [];
      const runs = buildRuns(el, marginErrs);
      errors.push(...marginErrs);
      if (runs.length === 0) return;
      textOut = runs;
      const maxRunFontSize = Math.max.apply(
        null,
        runs.map((r) => r.options.fontSize)
      );
      if (maxRunFontSize > fontSizePt) {
        effectiveLineSpacing = maxRunFontSize * (lineSpacingPt / fontSizePt);
      }
    } else {
      textOut = applyTextTransform(collapsedFull, cs.textTransform);
    }

    // Geometry compensation (6.6): widen single p/h1-h6 text frames by 2% to compensate
    // for the known error that pptxgenjs/PowerPoint measures text width narrower than
    // the browser does.
    const heightIn = geomPx.h / 96;
    let xIn = geomPx.x / 96;
    let yIn = geomPx.y / 96;
    let wIn = geomPx.w / 96;
    let hIn = heightIn;
    {
      const widen = wIn * 0.02;
      if (align === 'right') {
        xIn -= widen;
        wIn += widen;
      } else if (align === 'center') {
        xIn -= widen / 2;
        wIn += widen;
      } else {
        wIn += widen;
      }
    }

    const outEl = {
      type: tag.toLowerCase(),
      x: xIn,
      y: yIn,
      w: wIn,
      h: hIn,
      fontSize: fontSizePt,
      fontFace,
      color: colorParsed ? colorParsed.hex : null,
      transparency: colorParsed && colorParsed.hasAlpha ? Math.round((1 - colorParsed.alpha) * 100) : null,
      align,
      lineSpacing: effectiveLineSpacing,
      paraSpaceBefore: marginTopPt,
      paraSpaceAfter: marginBottomPt,
      marginArr: hasPadding ? paddingArr : null,
      rotate: rotation !== 0 ? rotation : null,
      text: textOut,
    };
    if (typeof textOut === 'string') {
      outEl.bold = boldBase;
      outEl.italic = italicBase;
      outEl.underline = underlineBase;
    }
    elements.push(outEl);
  }

  // ---- Background ----
  function extractBackground() {
    const cs = getComputedStyle(document.body);
    if (cs.backgroundImage && cs.backgroundImage !== 'none') {
      const m = /url\((['"]?)(.*?)\1\)/.exec(cs.backgroundImage);
      if (m) return { type: 'image', value: m[2] };
    }
    const c = parseColorString(cs.backgroundColor);
    if (isVisibleColor(c)) return { type: 'color', value: c.hex };
    return null;
  }

  // ---- Main traversal ----
  const allNodes = Array.from(document.body.querySelectorAll('*'));

  for (const el of allNodes) {
    const tag = el.tagName;

    if (TEXT_TAG_BG_CHECK.has(tag)) {
      const v = violationOf(el);
      if (v) {
        errors.push(
          `Text tag <${tag.toLowerCase()}> has ${v} set on it: backgrounds, borders, and shadows may only be applied to a <div> — wrap it in an outer <div> instead`
        );
        continue;
      }
    }

    if (consumed.has(el)) continue;

    const classAttr = el.getAttribute('class') || '';

    if (el.getAttribute('data-pptx-merge') === 'true') {
      processMergeContainer(el);
      continue;
    }
    if (classAttr.indexOf('placeholder') !== -1) {
      processPlaceholder(el);
      continue;
    }
    if (tag === 'IMG') {
      processImage(el);
      continue;
    }
    if (tag === 'DIV') {
      processDiv(el);
      continue;
    }
    if (tag === 'UL' || tag === 'OL') {
      processList(el);
      continue;
    }
    if (TEXT_ELEMENT_TAGS.has(tag)) {
      processTextElement(el);
      continue;
    }
    // Any other element: ignore — emit nothing, raise no error
  }

  const bodyCs = getComputedStyle(document.body);
  return {
    background: extractBackground(),
    elements,
    placeholders,
    errors,
    body: {
      width: parseFloat(bodyCs.width),
      height: parseFloat(bodyCs.height),
      scrollWidth: document.body.scrollWidth,
      scrollHeight: document.body.scrollHeight,
    },
  };
}

// ============================================================================
// Node side: writing into pptxgenjs
// ============================================================================

function stripFileProtocol(p) {
  return p.replace(/^file:\/\//, '');
}

function previewTextOf(el) {
  if (typeof el.text === 'string') return el.text;
  const arr = Array.isArray(el.text) ? el.text : Array.isArray(el.items) ? el.items : [];
  for (const r of arr) {
    if (r && typeof r.text === 'string' && r.text.trim() !== '') return r.text;
  }
  return '';
}

function writeElement(slide, pres, el) {
  switch (el.type) {
    case 'image': {
      slide.addImage({ path: stripFileProtocol(el.src), x: el.x, y: el.y, w: el.w, h: el.h });
      break;
    }
    case 'line': {
      slide.addShape(pres.ShapeType.line, {
        x: el.x,
        y: el.y,
        w: el.w,
        h: el.h,
        line: { color: el.color, width: el.widthPt },
      });
      break;
    }
    case 'shape': {
      const shapeName = el.rectRadius > 0 ? pres.ShapeType.roundRect : pres.ShapeType.rect;
      const opts = { x: el.x, y: el.y, w: el.w, h: el.h, shape: shapeName };
      if (el.fill) opts.fill = el.fill;
      if (el.line) opts.line = el.line;
      if (el.rectRadius > 0) opts.rectRadius = el.rectRadius;
      if (el.shadow) opts.shadow = el.shadow;
      slide.addText('', opts);
      break;
    }
    case 'list': {
      const opts = {
        x: el.x,
        y: el.y,
        w: el.w,
        h: el.h,
        fontSize: el.fontSize,
        fontFace: el.fontFace,
        color: el.color,
        align: el.align,
        valign: 'top',
        lineSpacing: el.lineSpacing,
        paraSpaceBefore: 0,
        paraSpaceAfter: el.paraSpaceAfter,
        margin: el.marginArr,
      };
      if (el.transparency != null) opts.transparency = el.transparency;
      slide.addText(el.items, opts);
      break;
    }
    case 'merged-text': {
      const opts = {
        x: el.x,
        y: el.y,
        w: el.w,
        h: el.h,
        fontSize: el.fontSize,
        fontFace: el.fontFace,
        color: el.color,
        align: el.align,
        valign: 'top',
        lineSpacing: el.lineSpacing,
        paraSpaceBefore: 0,
        paraSpaceAfter: 0,
        margin: el.marginArr,
      };
      if (el.transparency != null) opts.transparency = el.transparency;
      slide.addText(el.items, opts);
      break;
    }
    default: {
      // p / h1-h6 / (fallback li): a single text frame
      const opts = {
        x: el.x,
        y: el.y,
        w: el.w,
        h: el.h,
        fontSize: el.fontSize,
        fontFace: el.fontFace,
        color: el.color,
        align: el.align,
        valign: 'top',
        lineSpacing: el.lineSpacing,
        paraSpaceBefore: el.paraSpaceBefore,
        paraSpaceAfter: el.paraSpaceAfter,
        inset: 0,
      };
      if (typeof el.text === 'string') {
        opts.bold = el.bold;
        opts.italic = el.italic;
        opts.underline = el.underline;
      }
      if (el.marginArr) opts.margin = el.marginArr;
      if (el.rotate) opts.rotate = el.rotate;
      if (el.transparency != null) opts.transparency = el.transparency;
      slide.addText(el.text, opts);
      break;
    }
  }
}

module.exports = async function html2pptx(htmlFile, pres, options) {
  options = options || {};
  const absHtmlPath = path.isAbsolute(htmlFile) ? htmlFile : path.resolve(process.cwd(), htmlFile);
  const tmpDir = options.tmpDir || process.env.TMPDIR || '/tmp';

  function finalizeError(rawMessage) {
    let message = rawMessage;
    if (!message.startsWith(htmlFile)) {
      message = `${htmlFile}: ${message}`;
    }
    return new Error(message);
  }

  let browser;
  let extraction;
  try {
    const launchOptions = { env: Object.assign({}, process.env, { TMPDIR: tmpDir }) };
    if (process.platform === 'darwin') launchOptions.channel = 'chrome';
    browser = await chromium.launch(launchOptions)
      .catch(() => chromium.launch({ ...launchOptions, channel: undefined }))
      .catch(() => chromium.launch({ ...launchOptions, channel: 'msedge' }));  // fallback for Macs without Chrome installed and Windows without a downloaded browser
    const page = await browser.newPage();
    await page.goto('file://' + absHtmlPath);

    const initialBodySize = await page.evaluate(() => {
      const cs = getComputedStyle(document.body);
      return { width: parseFloat(cs.width), height: parseFloat(cs.height) };
    });
    await page.setViewportSize({
      width: Math.max(1, Math.round(initialBodySize.width)),
      height: Math.max(1, Math.round(initialBodySize.height)),
    });

    extraction = await page.evaluate(extractPageDataInBrowser);
  } finally {
    if (browser) await browser.close();
  }

  // ---- Whole-page validation (section 5), merged with the errors collected during extraction ----
  const errors = extraction.errors.slice();

  const widthOverflowPx = Math.max(0, extraction.body.scrollWidth - extraction.body.width - 1);
  const heightOverflowPx = Math.max(0, extraction.body.scrollHeight - extraction.body.height - 1);
  if (widthOverflowPx > 0) {
    errors.push(`Content overflows the page horizontally by ${(widthOverflowPx * PT_PER_PX).toFixed(1)}pt`);
  }
  if (heightOverflowPx > 0) {
    errors.push(
      `Content overflows the page vertically by ${(heightOverflowPx * PT_PER_PX).toFixed(1)}pt (keep 0.5 inch of blank space at the bottom of the page)`
    );
  }

  let slideHeightIn = null;
  if (pres.presLayout) {
    const layoutWIn = pres.presLayout.width / EMU_PER_INCH;
    const layoutHIn = pres.presLayout.height / EMU_PER_INCH;
    const bodyWIn = extraction.body.width * IN_PER_PX;
    const bodyHIn = extraction.body.height * IN_PER_PX;
    if (Math.abs(bodyWIn - layoutWIn) > 0.1 || Math.abs(bodyHIn - layoutHIn) > 0.1) {
      errors.push(
        `Page size mismatch: the HTML body is ${bodyWIn.toFixed(1)}×${bodyHIn.toFixed(1)} inches but the PPT layout is ${layoutWIn.toFixed(1)}×${layoutHIn.toFixed(1)} inches`
      );
    }
    slideHeightIn = layoutHIn;
  }

  if (slideHeightIn != null) {
    const CHECK_TYPES = new Set(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'list', 'merged-text']);
    for (const el of extraction.elements) {
      if (!CHECK_TYPES.has(el.type)) continue;
      if (!(el.fontSize > 12)) continue;
      const distance = slideHeightIn - (el.y + el.h);
      if (distance < 0.5) {
        const preview = previewTextOf(el).slice(0, 50);
        errors.push(`Text frame "${preview}" is only ${distance.toFixed(2)} inches from the bottom edge of the page; leave at least 0.5 inches`);
      }
    }
  }

  if (errors.length > 0) {
    let message;
    if (errors.length === 1) {
      message = errors[0];
    } else {
      message = `Found ${errors.length} problem(s):\n` + errors.map((e, i) => `  ${i + 1}. ${e}`).join('\n');
    }
    throw finalizeError(message);
  }

  // ---- Write into the slide ----
  const slide = options.slide || pres.addSlide();

  if (extraction.background) {
    if (extraction.background.type === 'image') {
      slide.background = { path: stripFileProtocol(extraction.background.value) };
    } else {
      slide.background = { color: extraction.background.value };
    }
  }

  for (const el of extraction.elements) {
    writeElement(slide, pres, el);
  }

  return { slide, placeholders: extraction.placeholders };
};
