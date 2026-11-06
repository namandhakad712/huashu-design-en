# 小红书分区样张的共用件

- `xhs.css`：页面盒子（1242×1660）、两种打开方式（1200×750 视口时缩成样张；其余宽度按真实尺寸排，给 `scripts/xhs_render.py` 切图）、纸面点阵、贴纸投影、字号底线变量。
- `xhs.js`：页码、`straddle()` 跨缝摆放、`wire()`/`perch()` 连续长卷的电线与站鸟。
- `stickers/`：样张用的鸟类贴纸缩略图，来自 [huashu-bird-sticker](https://github.com/alchaincyf/huashu-bird-sticker)，许可是 **PolyForm Shield 1.0.0**（条款：https://polyformproject.org/licenses/shield/1.0.0 ），和本仓库的 MIT 不同，见 `stickers/LICENSE.md`。只为演示版式；你的作品请换成自己的素材。
- `birds.js`：这些贴纸的名字、学名和几项数据。

样张题材都是同一个鸟类贴纸项目，借的是版式，不是题材。
