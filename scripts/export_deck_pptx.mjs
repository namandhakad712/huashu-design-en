#!/usr/bin/env node
/**
 * export_deck_pptx.mjs — 把多文件 slide deck 导出为 PPTX
 *
 * 两种模式：
 *   --mode image     图片铺底，视觉 100% 保真，⚠️ 文字不可编辑
 *   --mode editable  文本框原生，文字可编辑，要求 HTML 符合 4 条硬约束（见 references/editable-pptx.md）
 *
 * 用法：
 *   # 图片模式（默认）
 *   node export_deck_pptx.mjs --slides <dir> --out <file.pptx>
 *   # 可编辑模式
 *   node export_deck_pptx.mjs --slides <dir> --out <file.pptx> --mode editable
 *
 * --mode image 特点：
 *   - 每张 slide 截图成 PNG，满铺一张 PPTX 页面
 *   - 视觉 100% 保真（因为就是图片）
 *   - 文字不可编辑
 *   - HTML 随便写，不挑格式
 *
 * --mode editable 特点：
 *   - 调用 scripts/html2pptx.js 把 HTML DOM 逐元素翻译成 PowerPoint 对象
 *   - 文字是真文本框，PPT 里直接双击能编辑
 *   - ⚠️ HTML 必须符合 4 条硬约束（见 references/editable-pptx.md）：
 *     1. 文字包在 <p>/<h1>-<h6> 里（div 不能直接放文字）
 *     2. 不用 CSS 渐变
 *     3. <p>/<h*> 不能有 background/border/shadow（放外层 div）
 *     4. div 不能 background-image（用 <img>）
 *   - body 尺寸默认 960pt × 540pt（LAYOUT_WIDE，13.333″ × 7.5″）
 *   - 视觉驱动的 HTML 几乎无法 pass —— 必须从写 HTML 的第一行就按约束写
 *
 * 依赖：
 *   --mode image:    npm install playwright pptxgenjs
 *   --mode editable: npm install playwright pptxgenjs sharp
 *
 * 按文件名排序（01-xxx.html → 02-xxx.html → ...）。
 */

import { chromium } from 'playwright';
import pptxgen from 'pptxgenjs';
import fs from 'fs/promises';
import path from 'path';
import os from 'os';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function parseArgs() {
  const args = { width: 1920, height: 1080, mode: 'image' };
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i += 2) {
    const k = a[i].replace(/^--/, '');
    args[k] = a[i + 1];
  }
  if (!args.slides || !args.out) {
    console.error('用法: node export_deck_pptx.mjs --slides <dir> --out <file.pptx> [--mode image|editable] [--width 1920] [--height 1080]');
    process.exit(1);
  }
  args.width = parseInt(args.width);
  args.height = parseInt(args.height);
  if (!['image', 'editable'].includes(args.mode)) {
    console.error(`未知 --mode: ${args.mode}。支持: image, editable`);
    process.exit(1);
  }
  return args;
}

async function exportImage({ slidesDir, outFile, files, width, height }) {
  console.log(`[image mode] Rendering ${files.length} slides as PNG...`);

  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width, height } });
  const page = await ctx.newPage();

  const tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), 'deck-pptx-'));
  const pngs = [];
  for (const f of files) {
    const url = 'file://' + path.join(slidesDir, f);
    await page.goto(url, { waitUntil: 'networkidle' }).catch(() => page.goto(url));
    await page.waitForTimeout(1200);
    const out = path.join(tmpDir, f.replace(/\.html$/, '.png'));
    await page.screenshot({ path: out, fullPage: false });
    pngs.push(out);
    console.log(`  [${pngs.length}/${files.length}] ${f}`);
  }
  await browser.close();

  const pres = new pptxgen();
  pres.defineLayout({ name: 'DECK', width: width / 96, height: height / 96 });
  pres.layout = 'DECK';
  for (const png of pngs) {
    const s = pres.addSlide();
    s.addImage({ path: png, x: 0, y: 0, w: pres.width, h: pres.height });
  }
  await pres.writeFile({ fileName: outFile });

  for (const p of pngs) await fs.unlink(p).catch(() => {});
  await fs.rmdir(tmpDir).catch(() => {});

  console.log(`\n✓ Wrote ${outFile}  (${files.length} slides, image mode, 文字不可编辑)`);
}

async function exportEditable({ slidesDir, outFile, files }) {
  console.log(`[editable mode] Converting ${files.length} slides via html2pptx...`);

  // 动态 require html2pptx.js（CommonJS 模块）
  const { createRequire } = await import('module');
  const require = createRequire(import.meta.url);
  let html2pptx;
  try {
    html2pptx = require(path.join(__dirname, 'html2pptx.js'));
  } catch (e) {
    console.error(`✗ 加载 html2pptx.js 失败：${e.message}`);
    console.error(`  该模块依赖 sharp —— 请跑 npm install sharp 后重试。`);
    process.exit(1);
  }

  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';  // 13.333 × 7.5 inch，对应 HTML body 960 × 540 pt

  const errors = [];
  for (let i = 0; i < files.length; i++) {
    const f = files[i];
    const fullPath = path.join(slidesDir, f);
    try {
      await html2pptx(fullPath, pres);
      console.log(`  [${i + 1}/${files.length}] ${f} ✓`);
    } catch (e) {
      console.error(`  [${i + 1}/${files.length}] ${f} ✗  ${e.message}`);
      errors.push({ file: f, error: e.message });
    }
  }

  if (errors.length) {
    console.error(`\n⚠️ ${errors.length} 张 slide 转换失败。常见原因：HTML 不符合 4 条硬约束。`);
    console.error(`  详见 references/editable-pptx.md 的「常见错误速查」。`);
    if (errors.length === files.length) {
      console.error(`✗ 全部失败，不生成 PPTX。`);
      process.exit(1);
    }
  }

  await pres.writeFile({ fileName: outFile });
  console.log(`\n✓ Wrote ${outFile}  (${files.length - errors.length}/${files.length} slides, editable mode, 文字可在 PPT 中直接编辑)`);
}

async function main() {
  const { slides, out, width, height, mode } = parseArgs();
  const slidesDir = path.resolve(slides);
  const outFile = path.resolve(out);

  const files = (await fs.readdir(slidesDir))
    .filter(f => f.endsWith('.html'))
    .sort();
  if (!files.length) {
    console.error(`No .html files found in ${slidesDir}`);
    process.exit(1);
  }

  if (mode === 'image') {
    await exportImage({ slidesDir, outFile, files, width, height });
  } else {
    await exportEditable({ slidesDir, outFile, files });
  }
}

main().catch(e => { console.error(e); process.exit(1); });
