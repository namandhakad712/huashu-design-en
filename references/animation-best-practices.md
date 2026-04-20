# Animation Best Practices · 正向动画设计语法

> 基于 Anthropic 官方三支产品动画（Claude Design / Claude Code Desktop / Claude for Word）
> 的深度拆解，提炼出的"Anthropic 级"动画设计规则。
>
> 配套 `animation-pitfalls.md`（避坑清单）使用——本文件是「**应该这样做**」，
> pitfalls 是「**不要这样做**」，两者正交，都要读。
>
> **约束声明**：本文件只收录**运动逻辑和表达风格**，**不引入任何品牌色具体色值**。
> 色彩决策走 §1.a 核心资产协议（从品牌 spec 抽取）或「设计方向顾问」
> （20 种哲学各自的配色方案）。本 reference 讨论的是「**怎么动**」，不是「**什么色**」。

---

## 核心哲学 · 动画是物理学，不是动画曲线

大多数 AI 生成动画有廉价感的根源是——**它们表现得像「数字」不是「物体」**。
真实世界的物体有质量、有惯性、有弹性、会溢出。Anthropic 三支片子的「高级感」根源，
就在于给数字元素一套**物理世界的运动规则**。

这套规则有 3 个层次：

1. **叙事节奏层**：Slow-Fast-Boom-Stop 的时间分配
2. **运动曲线层**：Expo Out / Overshoot / Spring，拒绝 linear
3. **表达语言层**：展示过程、鼠标弧线、Logo 形变收束

---

## 1. 叙事节奏 · Slow-Fast-Boom-Stop 5 段结构

Anthropic 三支片子无一例外遵循这个结构：

| 段 | 占比 | 节奏 | 作用 |
|---|---|---|---|
| **S1 触发** | ~15% | 慢 | 给人类反应时间，建立真实感 |
| **S2 生成** | ~15% | 中 | 视觉惊艳点出现 |
| **S3 过程** | ~40% | 快 | 展示可控性/密度/细节 |
| **S4 爆发** | ~20% | Boom | 镜头拉远/3D pop-out/多面板涌现 |
| **S5 落幅** | ~10% | 静 | 品牌 Logo + 戛然而止 |

**具体时长映射**（15 秒动画为例）：
S1 触发 2s · S2 生成 2s · S3 过程 6s · S4 爆发 3s · S5 落幅 2s

**禁止做的事**：
- ❌ 均匀节奏（每秒信息密度一样）— 观众疲劳
- ❌ 持续高密度 — 无峰值无记忆点
- ❌ 渐弱收尾（fade out 到透明）— 应该**戛然而止**

**自检**：用纸笔画 5 个 thumbnail，每个代表一段的高潮画面。如果 5 张图差别不大，
说明节奏没做出来。

---

## 2. Easing 哲学 · 拒绝 linear，拥抱物理

Anthropic 三支片子的所有动效都用带「阻尼感」的贝塞尔曲线。默认的 cubic easeOut
（`1-(1-t)³`）**不够锐**——起步不够快、停顿不够稳。

### 三个核心 Easing（animations.jsx 已内置）

```js
// 1. Expo Out · 迅速启动缓慢刹车（最常用，默认主 easing）
// 对应 CSS: cubic-bezier(0.16, 1, 0.3, 1)
Easing.expoOut(t) // = t === 1 ? 1 : 1 - Math.pow(2, -10 * t)

// 2. Overshoot · 带弹性的 toggle/按钮弹出
// 对应 CSS: cubic-bezier(0.34, 1.56, 0.64, 1)
Easing.overshoot(t)

// 3. Spring 物理 · 几何体归位、自然落位
Easing.spring(t)
```

### 用法映射

| 场景 | 用哪个 Easing |
|---|---|
| 卡片 rise-in / 面板入场 / Terminal fade / focus overlay | **`expoOut`**（主 easing，最常用） |
| Toggle 切换 / 按钮弹出 / 强调交互 | `overshoot` |
| Preview 几何体归位 / 物理落位 / UI 元素抖弹 | `spring` |
| 持续运动（如鼠标轨迹插值） | `easeInOut`（保留对称性） |

### 反直觉洞察

大多数产品宣传片的动画**太快太硬**。`linear` 让数字元素像机器，`easeOut` 是基础分，
`expoOut` 才是「高级感」的技术根源——它给数字元素一种**物理世界的重量感**。

---

## 3. 运动语言 · 8 条共性原则

### 3.1 底色不用纯黑纯白

Anthropic 三支片子没有一支用 `#FFFFFF` 或 `#000000` 做主底色。**带色温的中性色**
（或暖或冷）有"纸张 / 画布 / 桌面"的物质感，削弱机器感。

**具体色值决策**走 §1.a 核心资产协议（从品牌 spec 抽取）或「设计方向顾问」
（20 种哲学各自的底色方案）。本 reference 不给具体色值——那是**品牌决策**，不是运动规则。

### 3.2 Easing 绝不是 linear

见 §2。

### 3.3 Slow-Fast-Boom-Stop 叙事

见 §1。

### 3.4 展示「过程」而非「魔法结果」

- Claude Design 展示 tweak 参数、拖滑块（不是一键生成完美结果）
- Claude Code 展示代码报错 + AI 修复（不是一次成功）
- Claude for Word 展示 Redline 红删绿增的修改过程（不是直接给最终稿）

**共同潜台词**：产品是**协作者、结对工程师、资深编辑**——不是一键魔术师。
这精准打击专业用户对「可控性」和「真实性」的痛点。

**反 AI slop**：AI 默认会做「魔法一键成功」的动画（一键生成 → 完美结果），
这是通用公约数。**反过来做**——展示过程、展示 tweak、展示 bug 和修复——
是品牌识别度的来源。

### 3.5 鼠标轨迹人工绘制（弧线 + Perlin Noise）

真人鼠标运动不是直线，是「起步加速 → 弧线 → 减速修正 → 点击」。
AI 直接直线插值的鼠标轨迹**有潜意识排斥感**。

```js
// 二次贝塞尔曲线插值（起点 → 控制点 → 终点）
function bezierQuadratic(p0, p1, p2, t) {
  const x = (1-t)*(1-t)*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0];
  const y = (1-t)*(1-t)*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1];
  return [x, y];
}

// 路径：起点 → 偏离中点 → 终点（做弧线）
const path = [[100, 100], [targetX - 200, targetY + 80], [targetX, targetY]];

// 再叠加极小的 Perlin Noise（±2px）制造「手抖」
const jitterX = (simpleNoise(t * 10) - 0.5) * 4;
const jitterY = (simpleNoise(t * 10 + 100) - 0.5) * 4;
```

### 3.6 Logo「形变收束」(Morph)

Anthropic 三支片子的 Logo 出场**都不是简单 fade-in**，是**前一个视觉元素形变而来**。

**共同模式**：倒数 1-2 秒做 Morph / Rotate / Converge，让整个叙事在品牌点上「坍缩」。

**低成本实现**（不用真 morph）：
让前一个视觉元素「坍缩」成一个色块（scale → 0.1，向中心 translate），
色块再「膨胀」展开成 wordmark。过渡用 150ms 快切 + motion blur
（`filter: blur(6px)` → `0`）。

```js
<Sprite start={13} end={14}>
  {/* 坍缩：前一个元素 scale 0.1，opacity 保持，filter blur 增加 */}
  const scale = interpolate(t, [0, 0.5], [1, 0.1], Easing.expoOut);
  const blur = interpolate(t, [0, 0.5], [0, 6]);
</Sprite>
<Sprite start={13.5} end={15}>
  {/* 膨胀：Logo 从色块中心 scale 0.1 → 1，blur 6 → 0 */}
  const scale = interpolate(t, [0, 0.6], [0.1, 1], Easing.overshoot);
  const blur = interpolate(t, [0, 0.6], [6, 0]);
</Sprite>
```

### 3.7 衬线 + 无衬线双字体

- **品牌 / 旁白**：衬线（有「学术感 / 出版物感 / 品位」）
- **UI / 代码 / 数据**：无衬线 + 等宽

**单一字体都是不对的**。衬线给「品位」，无衬线给「功能」。

具体字体选择走品牌 spec（brand-spec.md 的 Display / Body / Mono 三栈）或设计方向
顾问的 20 种哲学。本 reference 不给具体字体——那是**品牌决策**。

### 3.8 焦点切换 = 背景减弱 + 前景锐化 + Flash 引导

焦点切换**不只是**降低 opacity。完整配方是：

```js
// 非焦点元素的滤镜组合
tile.style.filter = `
  brightness(${1 - 0.5 * focusIntensity})
  saturate(${1 - 0.3 * focusIntensity})
  blur(${focusIntensity * 4}px)        // ← 关键：加 blur 才真的"退后"
`;
tile.style.opacity = 0.4 + 0.6 * (1 - focusIntensity);

// 焦点完成后在焦点位置做 150ms Flash highlight 引导视线回流
focusOverlay.animate([
  { background: 'rgba(255,255,255,0.3)' },
  { background: 'rgba(255,255,255,0)' }
], { duration: 150, easing: 'ease-out' });
```

**为什么 blur 是必须的**：只靠 opacity + brightness，焦点外的元素还是「锐利」的，
视觉上没有「退到后景」的效果。blur(4-8px) 让非焦点真的退一层景深。

---

## 4. 具体运动技巧（可直接抄的代码片段）

### 4.1 FLIP / Shared Element Transition

按钮「膨胀」成输入框，**不是**按钮消失 + 新面板出现。核心是**同一个 DOM 元素**在
两种状态间 transition，不是两个元素 cross-fade。

```jsx
// 用 Framer Motion layoutId
<motion.div layoutId="design-button">Design</motion.div>
// ↓ 点击后同 layoutId
<motion.div layoutId="design-button">
  <input placeholder="Describe your design..." />
</motion.div>
```

原生实现参考 https://aerotwist.com/blog/flip-your-animations/

### 4.2「呼吸式」展开（width→height）

面板展开**不是同时拉 width 和 height**，而是：
- 前 40% 时间：只拉 width（保持 height 小）
- 后 60% 时间：width 保持，撑 height

这模拟物理世界「先展开，再注水」的感觉。

```js
const widthT = interpolate(t, [0, 0.4], [0, 1], Easing.expoOut);
const heightT = interpolate(t, [0.3, 1], [0, 1], Easing.expoOut);
style.width = `${widthT * targetW}px`;
style.height = `${heightT * targetH}px`;
```

### 4.3 Staggered Fade-up（30ms stagger）

表格行、卡片列、列表项入场时，**每个元素延迟 30ms**，`translateY` 从 10px 回到 0。

```js
rows.forEach((row, i) => {
  const localT = Math.max(0, t - i * 0.03);  // 30ms stagger
  row.style.opacity = interpolate(localT, [0, 0.3], [0, 1], Easing.expoOut);
  row.style.transform = `translateY(${
    interpolate(localT, [0, 0.3], [10, 0], Easing.expoOut)
  }px)`;
});
```

### 4.4 非线性呼吸 · 关键结果前悬停 0.5s

机器执行快且连贯，但**关键结果出现前悬停 0.5 秒**，让观众大脑有反应时间。

```jsx
// 典型场景：AI 生成完 → 悬停 0.5s → 结果浮现
<Sprite start={8} end={8.5}>
  {/* 0.5s 停顿——什么也不动，让观众盯着加载状态 */}
  <LoadingState />
</Sprite>
<Sprite start={8.5} end={10}>
  <ResultAppear />
</Sprite>
```

**反例**：AI 生成完立刻无缝切到结果——观众没反应时间，信息流失。

### 4.5 Chunk Reveal · 模拟 token 流式

AI 生成文字**不要用 `setInterval` 单字符蹦出**（像老电影字幕），要用 **chunk reveal**
——一次出现 2-5 个字符，间隔不规律，模拟真实 token 流式输出。

```js
// 分 chunk 而不是分字符
const chunks = text.split(/(\s+|,\s*|\.\s*|;\s*)/);  // 按词 + 标点切
let i = 0;
function reveal() {
  if (i >= chunks.length) return;
  element.textContent += chunks[i++];
  const delay = 40 + Math.random() * 80;  // 不规律 40-120ms
  setTimeout(reveal, delay);
}
reveal();
```

### 4.6 Anticipation → Action → Follow-through

Disney 12 原则中的 3 条。Anthropic 用得很显式：

- **Anticipation**（预备）：动作开始前有小反向动作（按钮轻微缩小再弹出）
- **Action**（动作）：主要动作本身
- **Follow-through**（跟随）：动作结束后有余韵（卡片落位后轻微 bounce）

```js
// 卡片入场的完整三段
const anticip = interpolate(t, [0, 0.2], [1, 0.95], Easing.easeIn);     // 预备
const action  = interpolate(t, [0.2, 0.7], [0.95, 1.05], Easing.expoOut); // 主动
const settle  = interpolate(t, [0.7, 1], [1.05, 1], Easing.spring);       // 回弹
// 最终 scale = 三段乘积或分段应用
```

**反例**：只有 Action 没有 Anticipation + Follow-through 的动画，像「PowerPoint 动画」。

### 4.7 3D Perspective + translateZ 分层

想要「倾斜 3D + 悬浮卡片」的气质，给容器加 perspective，给单个元素不同的 translateZ：

```css
.stage-wrap {
  perspective: 2400px;
  perspective-origin: 50% 30%;  /* 视线略俯视 */
}
.card-grid {
  transform-style: preserve-3d;
  transform: rotateX(8deg) rotateY(-4deg);  /* 黄金比例 */
}
.card:nth-child(3n) { transform: translateZ(30px); }
.card:nth-child(5n) { transform: translateZ(-20px); }
.card:nth-child(7n) { transform: translateZ(60px); }
```

**为什么 rotateX 8° / rotateY -4° 是黄金比例**：
- 大于 10° → 元素扭曲感过强，看起来像「倒下」
- 小于 5° → 像「错切」而不是「透视」
- 8° × -4° 的非对称比例模拟「镜头在桌面左上角俯视」的 natural angle

### 4.8 斜向 Pan · 同时动 XY

镜头运动不是纯上下或纯左右，而是**同时动 XY** 模拟斜向移动：

```js
const panX = Math.sin(flowT * 0.22) * 40;
const panY = Math.sin(flowT * 0.35) * 30;
stage.style.transform = `
  translate(-50%, -50%)
  rotateX(8deg) rotateY(-4deg)
  translate3d(${panX}px, ${panY}px, 0)
`;
```

**关键**：X 和 Y 的频率不同（0.22 vs 0.35），避免 Lissajous 循环规则化。

---

## 5. 场景配方（三种叙事模板）

参考材料里三支视频对应三种产品性格。**选一种最贴合你的产品**，不要混搭。

### 配方 A · Apple Keynote 戏剧式（Claude Design 类）

**适合**：大版本发布、hero 动画、视觉惊艳优先
**节奏**：Slow-Fast-Boom-Stop 强弧线
**Easing**：全程 `expoOut` + 少量 `overshoot`
**SFX 密度**：高（~0.4/s），SFX 音高调到 BGM 音阶
**BGM**：IDM / 极简科技电子，冷静+精密
**收束**：镜头急拉远 → drop → Logo 形变 → 空灵单音 → 戛然而止

### 配方 B · 一镜到底工具式（Claude Code 类）

**适合**：开发者工具、生产力 App、心流场景
**节奏**：持续稳定 flow，没有明显峰值
**Easing**：`spring` 物理 + `expoOut`
**SFX 密度**：**0**（纯靠 BGM 驱动剪辑节奏）
**BGM**：Lo-fi Hip-hop / Boom-bap，85-90 BPM
**核心技巧**：关键 UI 动作踩在 BGM kick/snare 瞬态上——「**音乐律动即交互音效**」

### 配方 C · 办公效率叙事式（Claude for Word 类）

**适合**：企业软件、文档/表格/日历类、专业感优先
**节奏**：多 scene 硬切 + Dolly In/Out
**Easing**：`overshoot`（toggle）+ `expoOut`（面板）
**SFX 密度**：中（~0.3/s），UI click 为主
**BGM**：Jazzy Instrumental，小调，BPM 90-95
**核心亮点**：某一幕必有「全片高光」—— 3D pop-out / 脱离平面浮起

---

## 6. 反例 · 这样做就是 AI slop

| 反 pattern | 为什么错 | 正确做法 |
|---|---|---|
| `transition: all 0.3s ease` | `ease` 是 linear 的亲戚，所有元素同速 | 用 `expoOut` + 分元素 stagger |
| 所有入场都 `opacity 0→1` | 没有运动方向感 | 配合 `translateY 10→0` + Anticipation |
| Logo 淡入 | 没有叙事收束感 | Morph / Converge / 坍缩-展开 |
| 鼠标直线移动 | 潜意识机器感 | 贝塞尔弧线 + Perlin Noise |
| 打字单字蹦出（setInterval） | 像老电影字幕 | Chunk Reveal，随机间隔 |
| 关键结果无悬停 | 观众没反应时间 | 结果前 0.5s 悬停 |
| 焦点切换只改 opacity | 非焦点元素还锐利 | opacity + brightness + **blur** |
| 纯黑底 / 纯白底 | 赛博感 / 反光疲劳 | 带色温的中性色（走品牌 spec） |
| 所有动画同样快 | 无节奏 | Slow-Fast-Boom-Stop |
| Fade out 收尾 | 无决定感 | 戛然而止（hold 最后一帧） |

---

## 7. 自检清单（动画交付前 60 秒）

- [ ] 叙事结构是 Slow-Fast-Boom-Stop，不是均匀节奏？
- [ ] 默认 easing 是 `expoOut`，不是 `easeOut` 或 `linear`？
- [ ] Toggle / 按钮弹出用了 `overshoot`？
- [ ] 卡片 / 列表入场有 30ms stagger？
- [ ] 关键结果前有 0.5s 悬停？
- [ ] 打字用 Chunk Reveal，不是 setInterval 单字？
- [ ] 焦点切换加了 blur（不只是 opacity）？
- [ ] Logo 是形变收束（Morph），不是淡入？
- [ ] 底色不是纯黑 / 纯白（带色温）？
- [ ] 文字有衬线 + 无衬线层次？
- [ ] 收尾是戛然而止，不是渐弱？
- [ ] （有鼠标的话）鼠标轨迹是弧线，不是直线？
- [ ] SFX 密度符合产品性格（见配方 A/B/C）？
- [ ] BGM 和 SFX 有 6-8dB 响度差？（见 `audio-design-rules.md`）

---

## 8. 与其他 reference 的关系

| reference | 定位 | 关系 |
|---|---|---|
| `animation-pitfalls.md` | 技术避坑（16 条） | 「**不要这样做**」· 本文件的反面 |
| `animations.md` | Stage/Sprite 引擎用法 | 动画**怎么写**的基础 |
| `audio-design-rules.md` | 双轨制音频规则 | 动画**配音频**的规则 |
| `sfx-library.md` | 37 个 SFX 清单 | 音效**素材库** |
| `apple-gallery-showcase.md` | Apple 画廊展示风格 | 一种特定运动风格的专题 |
| **本文件** | 正向运动设计语法 | 「**应该这样做**」 |

**调用顺序**：
1. 先看 SKILL.md 工作流程 Step 3 的位置四问（决定叙事角色和视觉温度）
2. 选定方向后读本文件确定**运动语言**（配方 A/B/C）
3. 写代码时参考 `animations.md` 和 `animation-pitfalls.md`
4. 导出视频时走 `audio-design-rules.md` + `sfx-library.md`

---

## 附录 · 本文件素材来源

- Anthropic 官方动画拆解：花叔项目目录的 `参考动画/BEST-PRACTICES.md`
- Anthropic 音频拆解：同目录 `AUDIO-BEST-PRACTICES.md`
- 3 支参考视频：`ref-{1,2,3}.mp4` + 对应 `gemini-ref-*.md` / `audio-ref-*.md`
- **严格过滤**：本 reference 不收录任何具体品牌色值、字体名、产品名。
  色彩/字体决策走 §1.a 核心资产协议或 20 种设计哲学。
