# Huashu Design Workbench

Browser-based GUI for huashu-design. Visual interface for users who prefer clicking over typing.

## Quick Start

```bash
cd web
npm install
npm run dev
```

Then open http://localhost:5173

## Features

- Visual prompt builder
- Output type selection (Animation/Prototype/Deck/Infographic)
- Design style picker
- Brand asset upload
- Real-time generation status
- Output preview

## File Communication

The workbench communicates with Kimi CLI via file-based protocol:
- Input: `workbench/input.json`
- Output: `workbench/output/`

## Credits

Built as an extension to [huashu-design-en](https://github.com/namandhakad712/huashu-design-en) by naman.