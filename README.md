# PixelFrame

PixelFrame is an automated responsive screenshot and reporting engine
for developers.

It captures websites at multiple breakpoints, generates structured
outputs, and prepares responsive previews for documentation, clients, or
regression workflows from a single CLI command.

------------------------------------------------------------------------

## Features

-   Multi breakpoint screenshot capture
-   Full page support
-   Structured timestamped run directories
-   Clean CLI interface
-   Composite grid generation (in progress)
-   Visual diff mode (planned)
-   CI friendly architecture

------------------------------------------------------------------------

## Why PixelFrame

Frontend teams and freelancers often need:

-   Responsive previews for clients
-   Documentation screenshots
-   Visual regression baselines
-   Repeatable screenshot automation
-   CI pipeline compatibility

Most workflows are manual or fragmented.

PixelFrame provides a clean, structured, automation first approach.

------------------------------------------------------------------------

## Installation

### 1. Clone the repository

``` bash
git clone https://github.com/yourusername/pixelframe.git
cd pixelframe
```

### 2. Create a virtual environment

``` bash
python -m venv env
```

### 3. Activate it

**Windows**

``` bash
env\Scripts\activate
```

**macOS or Linux**

``` bash
source env/bin/activate
```

### 4. Install locally

``` bash
pip install -e .
playwright install
```

------------------------------------------------------------------------

## Usage

### Basic capture

``` bash
pixelframe capture run https://example.com
```

This creates a structured run folder:

    pixelframe-output/
      run-YYYY-MM-DD-HHMMSS/
        screenshots/
        composite/
        report/

Each run is isolated and timestamped for stability and future diff
comparisons.

------------------------------------------------------------------------

## Default Breakpoints

-   Mobile --- 375x812
-   Tablet --- 768x1024
-   Laptop --- 1366x768
-   Desktop --- 1920x1080

------------------------------------------------------------------------

## CLI Options

``` bash
pixelframe capture run URL [OPTIONS]
```

### Options

-   `--output` Custom output directory
-   `--full-page` or `--no-full-page` Toggle full page screenshot
    capture

------------------------------------------------------------------------

## Project Structure

    pixelframe/
      cli/
      engine/

Designed for extensibility and future automation workflows.

------------------------------------------------------------------------

## Roadmap

-   Composite grid generator
-   Professional PDF reports
-   Visual diff mode
-   Threshold based CI failure
-   YAML config support
-   GitHub Action integration
-   VS Code extension

------------------------------------------------------------------------

## Vision

PixelFrame aims to become a developer grade responsive testing engine
with:

-   Automated reporting
-   Visual regression comparison
-   CI integration
-   Clean version controlled layout baselines

------------------------------------------------------------------------

## Contributing

Pull requests are welcome.

If you plan significant changes, open an issue first to discuss
direction.

------------------------------------------------------------------------

## License

MIT License
