# PixelFrame

**PixelFrame** is an automated responsive screenshot and reporting engine for developers.

Capture websites at multiple breakpoints, generate structured outputs, and prepare responsive previews for documentation, clients, or regression workflows — all from a single CLI command.

---

## ✨ Features

- Multi-breakpoint screenshot capture
- Full-page support
- Structured timestamped run directories
- Clean CLI interface
- Composite grid generation (in progress)
- Visual diff mode (planned)
- CI-friendly architecture

---

## 🚀 Why PixelFrame?

Frontend teams and freelancers often need:

- Responsive previews for clients
- Documentation screenshots
- Visual regression baselines
- Repeatable screenshot automation
- CI pipeline compatibility

Most workflows are manual or fragmented.

PixelFrame provides a clean, structured, automation-first approach.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/pixelframe.git
cd pixelframe

Create a virtual environment:

python -m venv env

Activate it:

Windows

env\Scripts\activate

macOS / Linux

source env/bin/activate

Install locally:

pip install -e .
playwright install
🖥 Usage

Basic capture:

pixelframe capture run https://example.com

This creates a structured run folder:

pixelframe-output/
  run-YYYY-MM-DD-HHMMSS/
    screenshots/
    composite/
    report/

Each run is isolated and timestamped for stability and future diff comparisons.

📱 Default Breakpoints

Mobile — 375x812

Tablet — 768x1024

Laptop — 1366x768

Desktop — 1920x1080

🏗 Project Structure
pixelframe/
  cli/
  engine/

Designed for extensibility and future automation workflows.

🛣 Roadmap

Composite grid generator

Professional PDF reports

Visual diff mode

Threshold-based CI failure

YAML config support

GitHub Action integration

VS Code extension

🎯 Future Vision

PixelFrame aims to become a developer-grade responsive testing engine with:

Automated reporting

Visual regression comparison

CI integration

Clean, version-controlled layout baselines

🤝 Contributing

Pull requests are welcome.

If you plan significant changes, open an issue first to discuss direction.

📄 License

MIT License