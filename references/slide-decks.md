# Slide Decks：HTML幻灯片制作规范

做幻灯片是设计工作的高频场景。这份文档说明怎么做好HTML幻灯片——从架构选型、单页设计，到 PDF/PPTX 导出的完整路径。

**本 skill 的能力覆盖**：
- HTML 播放/PDF 导出 → 本文档 + `scripts/export_deck_pdf.mjs` / `scripts/export_deck_stage_pdf.mjs`
- 可编辑 PPTX 导出 → `references/editable-pptx.md` + `scripts/html2pptx.js` + `scripts/export_deck_pptx.mjs --mode editable`
- 图片铺底 PPTX（不可编辑但视觉保真）→ `scripts/export_deck_pptx.mjs --mode image`

---

## 🛑 开工前先确认交付格式（最硬的 checkpoint）

**这个决策比「单文件还是多文件」更先。** 2026-04-20 期权私董会项目实测：**不在动手前确认交付格式 = 2-3 小时返工。**

### 决策树

```
│ 问：最终要交付什么？
├── 只要浏览器全屏演讲 / 本地 HTML    → 视觉最自由，随便做
├── 要 PDF（打印 / 发群 / 存档）      → 视觉最自由，任何架构都能导出
└── 要可编辑 PPTX（同事会改文字）    → 🛑 从第一行 HTML 开始就按 `references/editable-pptx.md` 的 4 条硬约束写
```

### 为什么「要 PPTX 就得从头走 Path A」

PPTX 可编辑的前提是 `html2pptx.js` 能把 DOM 逐元素翻译为 PowerPoint 对象。它需要 **4 条硬约束**：

1. body 固定 720pt × 405pt（不是 1920×1080px）
2. 所有文字包在 `<p>`/`<h1>`-`<h6>` 里（禁止 div 直接放文字，禁止用 `<span>` 承载主文字）
3. `<p>`/`<h*>` 自身不能有 background/border/shadow（放外层 div）
4. `<div>` 不能用 `background-image`（用 `<img>` 标签）
5. 不用 CSS gradient、不用 web component、不用复杂 SVG 装饰

**本 skill 默认的 HTML 视觉自由度高**——大量 span、嵌套 flex、复杂 SVG、web component（如 `<deck-stage>`）、CSS 渐变——**几乎没有一条能天然过 html2pptx 的约束**（实测视觉驱动的 HTML 直接上 html2pptx，pass 率 < 30%）。

### 两条真实路径的代价对比（2026-04-20 真实踩坑）

| 路径 | 做法 | 结果 | 代价 |
|------|------|------|------|
| ❌ **先自由写 HTML，事后补救 PPTX** | 单文件 deck-stage + 大量 SVG/span 装饰 | 要可编辑 PPTX 只剩两条路：<br>A. 手写 pptxgenjs 几百行 hardcode 坐标<br>B. 重写 17 页 HTML 成 Path A 格式 | 2-3 小时返工，且手写版**维护成本永续**（HTML 改一个字，PPTX 要再人肉同步） |
| ✅ **从第一步按 Path A 约束写** | 每页独立 HTML + 4 条硬约束 + 720×405pt | 一条命令导出 100% 可编辑 PPTX，同时也能浏览器全屏演讲（Path A HTML 就是浏览器可播放的标准 HTML） | 写 HTML 时多花 5 分钟想「文字怎么包进 `<p>`」，零返工 |

### 开工话术（抄走即用）

> 动手之前先确认交付格式：
> - **浏览器演讲 / PDF** → 我按设计自由度最大的方式做（可以用动画、web component、复杂 SVG、CSS 渐变）
> - **需要可编辑 PPTX**（同事会改文字） → 我必须从一开始就按 `references/editable-pptx.md` 的 4 条硬约束写 HTML。视觉能力会少一些（无渐变、无 web component、无复杂 SVG），但导出就是一条命令的事
>
> 你选哪条？

### 混合交付怎么办

用户说「我要 HTML 演讲 **和** 可编辑 PPTX」——**这不是混合**，是 PPTX 需求覆盖 HTML 需求。按 Path A 写出来的 HTML 本身就能浏览器全屏演讲（加个 `deck_index.html` 拼接器就行）。**没有额外代价。**

用户说「我要 PPTX **和** 动画 / web component」——**这是真矛盾**。告诉用户：要可编辑 PPTX 就得牺牲这些视觉能力。让他做取舍，不要偷偷做手写 pptxgenjs 方案（会变成永续维护债）。

### 事后才知道要 PPTX 怎么办（紧急补救）

极个别情况：HTML 已经写好了才发现要 PPTX。此时两个选项都不完美：

1. **图片铺底 PPTX**（`scripts/export_deck_pptx.mjs` image 模式）——视觉 100% 保真但文字不可编辑。适合「演讲用 PPT 播放、不改内容」场景
2. **手写 pptxgenjs 重建**（为每页手写 addText/addShape + 图形 PNG 嵌入）——文字可编辑，但位置、字体、对齐都要手调，维护成本高。**只有用户明确接受「HTML 源要改就得重新手调 PPTX」才走这条**

永远优先把选择告诉用户，让他决定。**永远不要第一反应就开始手写 pptxgenjs**——那是最后的兜底手段。

---

## 🛑 先定架构：单文件 还是 多文件？

**这个选择是做幻灯片的第一步，错了会反复踩坑。先读完这一节再动手。**

### 两种架构对比

| 维度 | 单文件 + `deck_stage.js` | **多文件 + `deck_index.html` 拼接器** |
|------|--------------------------|--------------------------------------|
| 代码结构 | 一个 HTML，所有 slide 是 `<section>` | 每页独立 HTML，`index.html` 用 iframe 拼接 |
| CSS 作用域 | ❌ 全局，一页的样式可能影响所有页 | ✅ 天然隔离，iframe 各自一片天 |
| 验证粒度 | ❌ 要 JS goTo 才能切到某页 | ✅ 单页文件双击就能在浏览器看 |
| 并行开发 | ❌ 一个文件，多 agent 改会冲突 | ✅ 多 agent 可并行做不同页，零冲突 merge |
| 调试难度 | ❌ 一处 CSS 出错，全 deck 翻车 | ✅ 一页出错只影响自己 |
| 内嵌交互 | ✅ 跨页共享状态很简单 | 🟡 iframe 间需 postMessage |
| 打印 PDF | ✅ 内置 | ✅ 拼接器 beforeprint 遍历 iframe |
| 键盘导航 | ✅ 内置 | ✅ 拼接器内置 |

### 选哪个？（决策树）

```
│ 问：deck 预计有多少页？
├── ≤10 页、需要 in-deck 动画或跨页交互、pitch deck → 单文件
└── ≥10 页、学术讲座、课件、长 deck、多 agent 并行 → 多文件（推荐）
```

**默认走多文件路径**。它不是「备选」，是**长 deck 和团队协作的主路径**。原因：单文件架构的每一个优势（键盘导航、打印、scale）多文件都有，而多文件的作用域隔离和可验证性是单文件补不回来的。

### 为什么这条规则这么硬？（真实事故记录）

单文件架构曾经在 AI心理学讲座 deck 制作中连踩四坑：

1. **CSS 特异性覆盖**：`.emotion-slide { display: grid }` (特异性 10) 干翻 `deck-stage > section { display: none }` (特异性 2)，导致所有页同时渲染叠加。
2. **Shadow DOM slot 规则被外层 CSS 压制**：`::slotted(section) { display: none }` 挡不住 outer rule 的覆盖，sections 不肯隐藏。
3. **localStorage + hash 导航竞态**：刷新后不是跳到 hash 位置，而是停在 localStorage 记录的旧位置。
4. **验证成本高**：必须 `page.evaluate(d => d.goTo(n))` 才能截某页，比直接 `goto(file://.../slides/05-X.html)` 慢一倍，还常报错。

全部根因是**单一全局命名空间**——多文件架构从物理层面把这些问题消除了。

---

## 路径 A（默认）：多文件架构

### 目录结构

```
我的Deck/
├── index.html              # 从 assets/deck_index.html 复制来，改 MANIFEST
├── shared/
│   ├── tokens.css          # 共享设计 token（色板/字号/常用 chrome）
│   └── fonts.html          # <link> 引入 Google Fonts（每页 include）
└── slides/
    ├── 01-cover.html       # 每个文件都是完整 1920×1080 HTML
    ├── 02-agenda.html
    ├── 03-problem.html
    └── ...
```

### 每张 slide 的模板骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>P05 · Chapter Title</title>
<link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
<link rel="stylesheet" href="../shared/tokens.css">
<style>
  /* 这一页独有的样式。用任何 class 名都不会污染别的页。*/
  body { padding: 120px; }
  .my-thing { ... }
</style>
</head>
<body>
  <!-- 1920×1080 的内容（由 body 的 width/height 在 tokens.css 里锁定）-->
  <div class="page-header">...</div>
  <div>...</div>
  <div class="page-footer">...</div>
</body>
</html>
```

**关键约束**：
- `<body>` 就是画布，直接在上面布局。不要包 `<section>` 或其他 wrapper。
- `width: 1920px; height: 1080px` 由 `shared/tokens.css` 里的 `body` 规则锁定。
- 引 `shared/tokens.css` 共享设计 token（色板、字号、page-header/footer 等）。
- 字体 `<link>` 每页自己写（fonts 单独 import 不贵，且保证每页独立可打开）。

### 拼接器：`deck_index.html`

**直接从 `assets/deck_index.html` 复制**。你只需要改一处——`window.DECK_MANIFEST` 数组，按顺序列出所有 slide 文件名和人类可读标签：

```js
window.DECK_MANIFEST = [
  { file: "slides/01-cover.html",    label: "封面" },
  { file: "slides/02-agenda.html",   label: "目录" },
  { file: "slides/03-problem.html",  label: "问题陈述" },
  // ...
];
```

拼接器已内置：键盘导航（←/→/Home/End/数字键/P 打印）、scale + letterbox、右下计数器、localStorage 记忆、hash 跳页、打印模式（遍历 iframe 按页输出 PDF）。

### 单页验证（这是多文件架构的杀手级优势）

每张 slide 都是独立 HTML。**做完一张就在浏览器双击打开看**：

```bash
open slides/05-personas.html
```

Playwright 截图也是直接 `goto(file://.../slides/05-personas.html)`，不需要 JS 跳页，也不会被别的页的 CSS 干扰。这让「改一点验一点」的工作流成本接近零。

### 并行开发

把每张 slide 的任务拆给不同 agent，同时跑——HTML 文件彼此独立，merge 时没有冲突。长 deck 用这种并行方式能把制作时间压到 1/N。

### `shared/tokens.css` 该放什么

只放**真正跨页共用**的东西：

- CSS 变量（色板、字号阶、间距阶）
- `body { width: 1920px; height: 1080px; }` 这样的 canvas 锁定
- `.page-header` / `.page-footer` 这种每页都用一模一样的 chrome

**不要**把单页的布局 class 塞进来——那会退化回单文件架构的全局污染问题。

---

## 路径 B（小 deck）：单文件 + `deck_stage.js`

适用于 ≤10 页、需要跨页共享状态（比如一个 React tweaks 面板要操控所有页）、或者做 pitch deck demo 这种要求极度紧凑的场景。

### 基本用法

1. 从 `assets/deck_stage.js` 读取内容，嵌入 HTML 的 `<script>`（或 `<script src="deck_stage.js">`）
2. 在 body 里用 `<deck-stage>` 包 slide
3. 🛑 **script 标签必须放在 `</deck-stage>` 之后**（见下方硬约束）

```html
<body>

  <deck-stage>
    <section>
      <h1>Slide 1</h1>
    </section>
    <section>
      <h1>Slide 2</h1>
    </section>
  </deck-stage>

  <!-- ✅ 正确：script 在 deck-stage 之后 -->
  <script src="deck_stage.js"></script>

</body>
```

### 🛑 Script 位置硬约束（2026-04-20 真实踩坑）

**不能把 `<script src="deck_stage.js">` 放在 `<head>` 里。** 即使它在 `<head>` 里能定义 `customElements`，parser 在解析到 `<deck-stage>` 开始标签时就会触发 `connectedCallback`——此时子 `<section>` 还没被 parse，`_collectSlides()` 拿到空数组，counter 显示 `1 / 0`，所有页同时叠加渲染。

**三条合规写法**（任选其一）：

```html
<!-- ✅ 最推荐：script 在 </deck-stage> 之后 -->
</deck-stage>
<script src="deck_stage.js"></script>

<!-- ✅ 也可：script 在 head 但加 defer -->
<head><script src="deck_stage.js" defer></script></head>

<!-- ✅ 也可：module 脚本天然 defer -->
<head><script src="deck_stage.js" type="module"></script></head>
```

`deck_stage.js` 本身已内置 `DOMContentLoaded` 延迟收集防御，即使 script 放 head 也不会彻底炸掉——但 `defer` 或放 body 底部仍然是更干净的做法，避免依赖防御分支。

### ⚠️ 单文件架构的 CSS 陷阱（务必阅读）

单文件架构最常见的坑——**`display` 属性被单页样式偷走**。

常见错误姿势 1（直接写 display: flex 到 section）：

```css
/* ❌ 外部 CSS 特异性 2，覆盖了 shadow DOM 的 ::slotted(section){display:none}（也是 2）*/
deck-stage > section {
  display: flex;            /* 所有页会同时叠加渲染！ */
  flex-direction: column;
  padding: 80px;
  ...
}
```

常见错误姿势 2（section 有特异性更高的 class）：

```css
.emotion-slide { display: grid; }   /* 特异性: 10，更糟 */
```

两种都会让 **所有 slide 同时叠加渲染**——counter 可能显示 `1 / 10` 假装正常，但视觉上第一页盖着第二页盖着第三页。

### ✅ Starter CSS（开工直接 copy，不踩坑）

**section 自身**只管「可见/不可见」；**layout（flex/grid 等）写到 `.active` 上**：

```css
/* section 只定义非 display 的通用样式 */
deck-stage > section {
  background: var(--paper);
  padding: 80px 120px;
  overflow: hidden;
  position: relative;
  /* ⚠️ 不要在这里写 display! */
}

/* 锁死「非激活即隐藏」——特异性+权重双保险 */
deck-stage > section:not(.active) {
  display: none !important;
}

/* 激活页才写需要的 display + layout */
deck-stage > section.active {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* 打印模式：所有页都要显示，覆盖 :not(.active) */
@media print {
  deck-stage > section { display: flex !important; }
  deck-stage > section:not(.active) { display: flex !important; }
}
```

替代方案：**把单页的 flex/grid 写到内部 wrapper `<div>` 上**，section 本身永远只是 `display: block/none` 的切换器。这是最干净的做法：

```html
<deck-stage>
  <section>
    <div class="slide-content flex-layout">...</div>
  </section>
</deck-stage>
```

### 自定义尺寸

```html
<deck-stage width="1080" height="1920">
  <!-- 9:16 竖版 -->
</deck-stage>
```

---

## Slide Labels

Deck_stage 和 deck_index 都会给每页打标签（计数器显示）。给它们**更有意义**的 label：

**多文件**：在 `MANIFEST` 里写 `{ file, label: "04 问题陈述" }`
**单文件**：在 section 上加 `<section data-screen-label="04 Problem Statement">`

**关键：Slide 编号从 1 开始，不要从 0**。

用户说"slide 5"时，他指的是第 5 张，永远不是数组位置 `[4]`。人类不说 0-indexed。

---

## Speaker Notes

**默认不加**，只在用户明确要求时才加。

加了 speaker notes 你就可以把 slide 上的文字减少到最小，focus on impactful visuals——notes 承载完整 script。

### 格式

**多文件**：在 `index.html` 的 `<head>` 里写：

```html
<script type="application/json" id="speaker-notes">
[
  "第1张的 script...",
  "第2张的 script...",
  "..."
]
</script>
```

**单文件**：同上位置。

### Notes 写作要点

- **完整**：不是提纲，是真要讲的话
- **对话式**：像平时说话，不是书面语
- **对应**：数组第 N 个对应第 N 张 slide
- **长度**：200-400 字最佳
- **情绪线**：标注重音、停顿、强调点

---

## Slide 设计模式

### 1. 建立一个系统（必做）

探索完 design context 后，**先口头说你要用的系统**：

```markdown
Deck系统：
- 背景色：最多2种（90% 白 + 10% 深色 section divider）
- 字型：display 用 Instrument Serif，body 用 Geist Sans
- 节奏：section divider 用 full-bleed 彩色 + 白字，普通 slide 白底
- 图像：hero slide 用 full-bleed 照片，data slide 用 chart

我按这个系统做，有问题告诉我。
```

用户确认后再往下做。

### 2. 常用 slide layouts

- **Title slide**：纯色背景 + 巨大标题 + 副标题 + 作者/日期
- **Section divider**：彩色背景 + 章节号 + 章节标题
- **Content slide**：白底 + 标题 + 1-3 bullet points
- **Data slide**：标题 + 大图表/数字 + 简短说明
- **Image slide**：full-bleed 照片 + 底部小 caption
- **Quote slide**：留白 + 巨大 quote + attribution
- **Two-column**：左右对比（vs / before-after / problem-solution）

一个 deck 里最多用 4-5 种 layout。

### 3. Scale（再次强调）

- 正文最小 **24px**，理想 28-36px
- 标题 **60-120px**
- Hero 字 **180-240px**
- 幻灯片是给 10 米外看的，字要够大

### 4. 视觉节奏

Deck 需要 **intentional variety**：

- 颜色节奏：大部分白底 + 偶尔彩色 section divider + 偶尔 dark 片段
- 密度节奏：几张 text-heavy 的 + 几张 image-heavy 的 + 几张 quote 留白
- 字号节奏：正常标题 + 偶尔巨型 hero 文字

**不要每张 slide 长一样**——那是 PPT 模板，不是设计。

### 5. 空间呼吸（数据密集页必读）

**新手最容易踩的坑**：把所有能放的信息都塞进一页。

信息密度 ≠ 有效信息传达。学术/演讲类 deck 尤其要克制：

- 列表/矩阵页：不要把 N 个元素都画成同一大小。用 **主次分层**——今天要聊的 5 个放大做主角，剩下 16 个缩小做背景 hint。
- 大数字页：数字本身是视觉主角。周围的 caption 不要超过 3 行，否则观众眼球来回跳。
- 引用页：引语和 attribution 之间要有留白隔开，不要贴在一起。

对照「数据是不是主角」「文字有没有挤在一起」两条自我审查，改到留白让你有点不安为止。

---

## 打印为 PDF

**多文件**：`deck_index.html` 已处理 `beforeprint` 事件，按页输出 PDF。

**单文件**：`deck_stage.js` 同样处理。

打印样式已写好，不需要额外写 `@media print` CSS。

---

## 导出为 PPTX / PDF（自助脚本）

HTML 优先是第一公民。但用户经常需要 PPTX/PDF 交付。提供两个通用脚本，**任何多文件 deck 都能用**，位于 `scripts/` 下：

### `export_deck_pdf.mjs` — 导出矢量 PDF（多文件架构）

```bash
node scripts/export_deck_pdf.mjs --slides <slides-dir> --out deck.pdf
```

**特点**：
- 文字**保留矢量**（可复制、可搜索）
- 视觉 100% 保真（Playwright 内嵌 Chromium 渲染后打印）
- **不需要改 HTML 任何一个字**
- 每个 slide 独立 `page.pdf()`，再用 `pdf-lib` 合并

**依赖**：`npm install playwright pdf-lib`

**限制**：PDF 不能再编辑文字——要改回到 HTML 改。

### `export_deck_stage_pdf.mjs` — 单文件 deck-stage 架构专用 ⚠️

**什么时候用**：deck 是单 HTML 文件 + `<deck-stage>` web component 包裹 N 个 `<section>`（即路径 B 架构）。此时 `export_deck_pdf.mjs` 那套「每个 HTML 一次 `page.pdf()`」走不通，需要走这个专用脚本。

```bash
node scripts/export_deck_stage_pdf.mjs --html deck.html --out deck.pdf
```

**为什么不能复用 export_deck_pdf.mjs**（2026-04-20 真实踩坑记录）：

1. **Shadow DOM 赢过 `!important`**：deck-stage 的 shadow CSS 里有 `::slotted(section) { display: none }`（只 active 的那张 `display: block`）。即使在 light DOM 用 `@media print { deck-stage > section { display: block !important } }` 也压不住——`page.pdf()` 触发 print 媒体后 Chromium 最终渲染只有 active 那一张，结果**整个 PDF 只有 1 页**（当前 active slide 的重复）。

2. **循环 goto 每页还是只出 1 页**：直觉解法「对每个 `#slide-N` navigate 一次再 `page.pdf({pageRanges:'1'})`」也失败——因为 print CSS 在 shadow DOM 之外也有 `deck-stage > section { display: block }` 规则被 override 后，最终渲染永远是 section 列表的第一个（不是你 navigate 到的那一页）。结果 17 次循环得到 17 张 P01 封面。

3. **absolute 子元素跑到下一页**：即使成功让所有 section 渲染出来，section 本身若 `position: static`，其 absolute 定位的 `cover-footer`/`slide-footer` 会相对 initial containing block 定位——当 section 被 print 强制为 1080px 高度，absolute footer 可能被推到下一页（表现为 PDF 比 section 数量多 1 页，多出来的那页只含 footer 孤儿）。

**修复策略**（脚本已实现）：

```js
// 打开 HTML 后，用 page.evaluate 把 section 从 deck-stage slot 中提出来，
// 直接挂到 body 下一个普通 div 里，并内联 style 确保 position:relative + 固定尺寸
await page.evaluate(() => {
  const stage = document.querySelector('deck-stage');
  const sections = Array.from(stage.querySelectorAll(':scope > section'));
  document.head.appendChild(Object.assign(document.createElement('style'), {
    textContent: `
      @page { size: 1920px 1080px; margin: 0; }
      html, body { margin: 0 !important; padding: 0 !important; }
      deck-stage { display: none !important; }
    `,
  }));
  const container = document.createElement('div');
  sections.forEach(s => {
    s.style.cssText = 'width:1920px!important;height:1080px!important;display:block!important;position:relative!important;overflow:hidden!important;page-break-after:always!important;break-after:page!important;background:#F7F4EF;margin:0!important;padding:0!important;';
    container.appendChild(s);
  });
  // 最后一页禁分页，避免尾部空白页
  sections[sections.length - 1].style.pageBreakAfter = 'auto';
  sections[sections.length - 1].style.breakAfter = 'auto';
  document.body.appendChild(container);
});

await page.pdf({ width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true });
```

**为什么这能 work**：
- 把 section 从 shadow DOM slot 拔到 light DOM 的普通 div——彻底绕过 `::slotted(section) { display: none }` 规则
- 内联 `position: relative` 让 absolute 子元素相对 section 定位，不会溢出
- `page-break-after: always` 让浏览器 print 时每 section 独立一页
- `:last-child` 不分页避免尾部空白页

**用 `mdls -name kMDItemNumberOfPages` 验证时注意**：macOS 的 Spotlight metadata 有缓存，PDF 重写后要跑 `mdimport file.pdf` 强制刷新，否则显示旧的页数。用 `pdfinfo` 或 `pdftoppm` 数文件数才是真数。

---

### `export_deck_pptx.mjs` — 导出 PPTX（两种模式）

```bash
# 图片铺底（视觉 100% 保真，不可编辑文字）
node scripts/export_deck_pptx.mjs --slides <dir> --out deck.pptx --mode image

# 每个文本独立文本框（可编辑，但字体会回落）
node scripts/export_deck_pptx.mjs --slides <dir> --out deck.pptx --mode editable
```

| 模式 | 视觉保真 | 文字可编辑 | 工作原理 | 限制 |
|------|---------|----------|---------|------|
| `image` | ✅ 100% | ❌ | Playwright 截图 → pptxgenjs addImage | 文字变图片 |
| `editable` | 🟡 ~70% | ✅ | html2pptx 提取每个文本框 | 见下方约束 |

**editable 模式的硬性约束**（用户 HTML 必须满足，否则该页 skip）：
- 所有文字必须在 `<p>`/`<h1>`-`<h6>`/`<ul>`/`<ol>` 里（禁止裸文本 div）
- `<p>`/`<h*>` 标签自身不能有 background/border/shadow（放外层 div）
- 不用 `::before`/`::after` 插入装饰文字（伪元素提不出来）
- inline 元素（span/em/strong）不能有 margin
- 不用 CSS gradient（不可渲染）
- div 不用 `background-image`（用 `<img>`）

脚本已内置**自动预处理器**——把 "叶子 div 里的裸文本" 自动包成 `<p>`（保留 class）。这解决了最常见的违规（裸文本）。但其他违规（p 上有 border、span 上有 margin 等）仍需 HTML 源头合规。

**editable 模式的另一个 caveat——字体回落**：
- Playwright 用 webfont 测量 text-box 尺寸；PowerPoint/Keynote 用本机字体渲染
- 两者不同时会有**溢出或错位**——每页都要肉眼过
- 建议目标机器装好 HTML 里用的字体，或 fallback 到 `system-ui`

### 从一开始就让 HTML 对导出友好

对性能最稳的 deck：**从写 HTML 时就按 editable 模式的约束写**。这样 `--mode editable` 可以直接全部 pass。额外成本不大：

```html
<!-- ❌ 不好 -->
<div class="title">关键发现</div>

<!-- ✅ 好（p 包裹，class 继承） -->
<p class="title">关键发现</p>

<!-- ❌ 不好（border 在 p 上） -->
<p class="stat" style="border-left: 3px solid red;">41%</p>

<!-- ✅ 好（border 在外层 div） -->
<div class="stat-wrap" style="border-left: 3px solid red;">
  <p class="stat">41%</p>
</div>
```

### 何时选哪个

| 场景 | 推荐 |
|------|------|
| 给主办方/档案存档 | **PDF**（通用、高保真、文字可搜） |
| 发给协作者让他们微调文字 | **PPTX editable**（接受字体回落） |
| 要现场演讲、不改内容 | **PDF** 或 **PPTX image** |
| HTML 是首选呈现媒介 | 直接浏览器播放，导出只是备份 |

## 导出为可编辑 PPTX 的深度路径（仅长期项目）

如果你的 deck 会长期维护、反复修改、团队协作——建议**一开始就按 html2pptx 约束写 HTML**，让 `--mode editable` 稳定通过。详见 `references/editable-pptx.md`（4 条硬约束 + HTML 模板 + 常见错误速查）。

---

## 常见问题

**多文件：iframe 里的页打不开 / 白屏**
→ 检查 `MANIFEST` 的 `file` 路径是否相对 `index.html` 正确。用浏览器 DevTools 看 iframe 的 src 能否直接访问。

**多文件：某页样式和别页冲突**
→ 不可能（iframe 隔离）。如果感觉冲突，那是缓存——Cmd+Shift+R 强刷。

**单文件：多 slide 同时渲染叠加**
→ CSS 特异性问题。看上面「单文件架构的 CSS 陷阱」一节。

**单文件：缩放看起来不对**
→ 检查是否所有 slide 直接挂在 `<deck-stage>` 下作为 `<section>`。中间不能包 `<div>`。

**单文件：想跳到特定 slide**
→ URL 加 hash：`index.html#slide-5` 跳到第 5 张。

**两种架构都适用：字在不同屏幕下位置不一致**
→ 用固定尺寸（1920×1080）和 `px` 单位，不要用 `vw`/`vh` 或 `%`。缩放统一处理。

---

## 验证检查清单（做完 deck 必过）

1. [ ] 浏览器直接打开 `index.html`（或主 HTML），检查首页无破图、字体已加载
2. [ ] 按 → 键翻到每一页，没有空白页、没有布局错位
3. [ ] 按 P 键打印预览，每页恰好一张 A4（或 1920×1080）且无裁切
4. [ ] 随机选 3 页 Cmd+Shift+R 强刷，localStorage 记忆正常工作
5. [ ] Playwright 批量截图（单页架构：遍历 `slides/*.html`；单文件架构：用 goTo 切换），人工肉眼过一遍
6. [ ] 搜一下 `TODO` / `placeholder` 残留，确认都清理了
