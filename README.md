# PixelFrame

**The Professional Visual Regression & Responsive Testing Engine.**

PixelFrame is a high-performance CLI tool designed for frontend teams to automate responsive screenshot capture, generate beautiful reports, and perform visual regression testing with ease.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/powered%20by-Playwright-green.svg)](https://playwright.dev/python/)

---

## 🚀 Key Features

- 📸 **Multi-Breakpoint Capture**: High-quality screenshots across mobile, tablet, and desktop viewports in one command.
- 📱 **Device Library**: 15+ curated real-world device presets (iPhone 15, MacBook Pro 14, Galaxy S23, etc.).
- 📂 **YAML Configuration**: Scale your testing with `pixelframe.yml` configuration files.
- 🌓 **Visual Diffing**: Pixel-perfect comparison between runs with red-highlighted difference heatmaps.
- 📑 **Self-Contained Reports**: Portable HTML/PDF reports with embedded base64 images—no external assets required.
- 🤖 **CI/CD Ready**: Integrated exit codes and GitHub Action support for automated regression gating.

---

## 📦 Installation

### 1. Setup Environment
```bash
git clone https://github.com/nijil71/PixelFrame.git
cd PixelFrame
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

### 2. Install PixelFrame
```bash
pip install -e .
playwright install chromium --with-deps
```

---

## 🛠 Usage

### 1. Basic Capture
Capture a single URL using default breakpoints.
```bash
pixelframe capture run https://example.com
```

### 2. Emulating Real Devices
Use fuzzy-matching to select specific device profiles.
```bash
pixelframe capture run https://apple.com --devices "iPhone 15, iPad Air, MacBook Pro 14"
```

### 3. Using YAML Configuration
Manage complex runs via a `pixelframe.yml` file.
```yaml
url: "https://your-site.com"
output_dir: "visual-audit"
full_page: true
devices:
  - "iPhone 15 Pro Max"
  - "Desktop 1440p"
```
```bash
pixelframe capture run --config pixelframe.yml
```

### 4. Visual Regression (Diffing)
Compare a baseline run against a new run.
```bash
pixelframe diff run path/to/baseline path/to/current --fail-under 98.0
```

---

## 🤖 GitHub Action Integration

Automate your visual tests on every PR using our GitHub Action template.

```yaml
- name: Visual Diff
  run: |
    python -m pixelframe diff run "$BASELINE" "$CURRENT" --fail-under 95.0
```

---

## 📋 Available Device Presets
Run `pixelframe devices list` to see all 15+ built-in presets including:
- **Phones**: iPhone 15, Galaxy S23, Pixel 8...
- **Tablets**: iPad Air, iPad Pro 12.9, Galaxy Tab S9...
- **Laptops**: MacBook Air, Surface Pro 9...
- **Desktops**: 1080p, 1440p, 4K...

---

## 🤝 Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
