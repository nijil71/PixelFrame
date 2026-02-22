<div align="center">
  <img src="assets/banner1.png" alt="PixelFrame Banner" width="500">

  # PixelFrame

  **Professional Visual Regression & Responsive Testing Engine**

  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
  [![Playwright](https://img.shields.io/badge/powered%20by-Playwright-green.svg?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/python/)
  [![MIT License](https://img.shields.io/badge/license-MIT-important.svg?style=for-the-badge)](LICENSE)
  [![Visual Regression](https://img.shields.io/github/actions/workflow/status/nijil71/PixelFrame/pixelframe.yml?branch=main&style=for-the-badge&label=Visual%20Regression)](https://github.com/nijil71/PixelFrame/actions/workflows/pixelframe.yml)

  <p align="center">
    <a href="#features">Features</a> •
    <a href="#installation">Installation</a> •
    <a href="#usage">Usage</a> •
    <a href="#ci-integration">CI Integration</a> •
    <a href="#contributing">Contributing</a>
  </p>
</div>

---

## Overview

PixelFrame is a high-performance CLI tool designed for frontend teams to automate responsive screenshot capture, generate detailed reports, and perform visual regression testing. It provides a structured, automation-first approach to verifying UI consistency across dozens of devices and viewports.



---

## Features

*   **Multi-Breakpoint Capture**: Capture high-fidelity screenshots across mobile, tablet, and desktop viewports in a single run.
*   **Smart Emulation**: Built-in library of 15+ device presets (iPhone 15, MacBook Pro, etc.) with support for device scale factors and touch.
*   **YAML Configuration**: Manage complex test suites using clean, version-controlled configuration files.
*   **Visual Regression**: Pixel-perfect diffing with red-highlighted heatmaps and automated similarity scoring.
*   **Portable Reports**: Self-contained HTML reports with embedded images for easy sharing and documentation.
*   **CI Ready**: Integrated exit codes, JSON output, and GitHub Action templates for automated regression gating.

---

## Installation

### 1. Prerequisites
PixelFrame requires **Python 3.10** or higher.

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/nijil71/PixelFrame.git
cd PixelFrame

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install package
pip install -e .
playwright install chromium --with-deps
```

---

## Usage

### Basic Capture
Capture a website using default responsive breakpoints.
```bash
pixelframe capture run https://example.com
```

### Device Emulation
Select specific devices from the built-in library.
```bash
pixelframe capture run https://apple.com --devices "iPhone 15, iPad Air, MacBook Pro 14"
```

### Config-Driven Capture
Run complex audits using a YAML configuration file.
```bash
pixelframe capture run --config demo-config.yml
```

### Visual Diffing
Compare two runs to identify visual regressions. The CLI returns exit code 1 if results fall below the threshold.
```bash
pixelframe diff run path/to/baseline path/to/latest --fail-under 98.0 --open-report
```

---

## CI Integration

PixelFrame is optimized for CI/CD pipelines. Use it to automatically block pull requests that introduce visual regressions.

```yaml
- name: Visual Threshold Check
  run: |
    pixelframe diff run ./baseline ./current --fail-under 99.0 --json
```

---

## Device Library
Run `pixelframe devices list` for the full directory. Popular presets include:

| Category | Devices |
| :--- | :--- |
| **Phones** | iPhone 15 Pro Max, Galaxy S23, Pixel 8, Galaxy Z Fold 5 |
| **Tablets** | iPad Air, iPad Pro (11"/12.9"), Galaxy Tab S9 |
| **Laptops** | MacBook Air, MacBook Pro (14"/16"), Surface Pro 9 |
| **Desktops**| 1080p, 1440p, 4K |

---

## Contributing

Contributions are welcome! Whether you are adding a new device preset or improving the capture engine.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

<div align="center">
  <!-- <p>Built for frontend teams by the PixelFrame contributors</p> -->
  <p>Distributed under the MIT License. See <a href="LICENSE">LICENSE</a> for more information.</p>
</div>
