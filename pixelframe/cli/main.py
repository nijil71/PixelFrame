import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

from pixelframe import __version__
from pixelframe.engine.logger import setup_logger
from pixelframe.engine.config import PixelFrameConfig, DEFAULT_BREAKPOINTS, Breakpoint
from pixelframe.engine.run_manager import create_run_directory
from pixelframe.engine.browser import BrowserManager
from pixelframe.engine.capture import capture_screenshots
from pixelframe.engine.composite import create_composite
from pixelframe.engine.report import generate_report
from pixelframe.engine.devices import get_devices, list_devices

# Root app
app = typer.Typer(
    help="PixelFrame - The Professional Visual Regression & Responsive Testing Engine.",
    add_completion=False,
    rich_markup_mode="rich"
)

def version_callback(value: bool):
    if value:
        console = Console()
        logo = """[bold cyan]
  _____ _          _ ______                         
 |  __ (_)        | |  ____|                        
 | |__) |__  _____| | |__ _ __ __ _ _ __ ___   ___  
 |  ___/ \\ \\/ / _ \\ |  __| '__/ _` | '_ ` _ \\ / _ \\ 
 | |   | |>  <  __/ | |  | | | (_| | | | | | |  __/ 
 |_|   |_/_/\\_\\___|_|_|  |_|  \\__,_|_| |_| |_|\\___| 
[/bold cyan]"""
        panel = Panel(
            Align.center(logo + f"\n[bold white]Version: {__version__}[/bold white]"), 
            border_style="cyan",
            expand=False
        )
        console.print(panel)
        raise typer.Exit()

@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True, help="Show version and exit."
    )
):
    """
    PixelFrame CLI Engine
    """
    pass

# Sub command groups
capture_app = typer.Typer(help="Capture responsive screenshots and generate reports.")
app.add_typer(capture_app, name="capture")

devices_app = typer.Typer(help="Explore and list available device presets.")
app.add_typer(devices_app, name="devices")

diff_app = typer.Typer(help="Compare screenshot runs and detect visual regressions.")
app.add_typer(diff_app, name="diff")

@diff_app.command("run")
def run_diff(
    run1: str = typer.Argument(..., help="Path to first run directory (baseline)"),
    run2: str = typer.Argument(..., help="Path to second run directory (new)"),
    output: str = typer.Option(None, help="Output directory for diff results"),
    threshold: float = typer.Option(
        95.0, 
        "--threshold", "-t", "--fail-under",
        help="Similarity percentage threshold. Exit with 1 if any image falls below this."
    ),
    open_report: bool = typer.Option(False, "--open-report", help="Open the generated HTML report in browser"),
    json_output: bool = typer.Option(False, "--json", help="Output final results as JSON for CI"),
):
    """
    Compare screenshots between two runs.
    
    Generates pixel-level diff overlays and a similarity report.
    Returns exit code 1 if any comparison falls below the threshold.
    """
    from pathlib import Path
    from pixelframe.engine.diff import generate_diff
    from pixelframe.engine.report import _image_to_base64
    from jinja2 import Environment, FileSystemLoader
    from datetime import datetime
    
    logger.info(f"Visual diffing {run1} vs {run2}")
    p1 = Path(run1) / "screenshots"
    p2 = Path(run2) / "screenshots"
    
    if not p1.exists() or not p2.exists():
        logger.error("Missing screenshots directory in one or both runs")
        raise typer.Exit(code=1)
        
    out_dir = Path(output) if output else Path(run2) / "diff"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    diff_results = []
    all_passed = True
    
    for img1_path in p1.glob("*.png"):
        img2_path = p2 / img1_path.name
        if not img2_path.exists():
            logger.warning(f"Screenshot {img1_path.name} missing in run2. Skipping.")
            continue
            
        diff_path = out_dir / f"diff_{img1_path.name}"
        
        logger.info(f"Diffing {img1_path.name}...")
        similarity = generate_diff(img1_path, img2_path, diff_path)
        
        passed = similarity >= threshold
        if not passed:
            all_passed = False
            
        diff_results.append({
            "name": img1_path.stem,
            "similarity": similarity,
            "passed": passed,
            "img1_b64": _image_to_base64(img1_path),
            "img2_b64": _image_to_base64(img2_path),
            "diff_b64": _image_to_base64(diff_path)
        })
        
    if not diff_results:
        logger.error("No comparable screenshots found.")
        raise typer.Exit(code=1)
        
    # Generate HTML report
    templates_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("diff_report.html")
    
    html_content = template.render(
        run1_name=Path(run1).name,
        run2_name=Path(run2).name,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        threshold=threshold,
        diff_results=diff_results
    )
    
    report_file = out_dir / "diff_report.html"
    report_file.write_text(html_content, encoding="utf-8")
    
    if open_report:
        import webbrowser
        webbrowser.open(f"file://{report_file.resolve()}")
        
    if json_output:
        import json
        print(json.dumps({
            "status": "PASSED" if all_passed else "FAILED",
            "threshold": threshold,
            "breakpoints": len(diff_results),
            "report_path": str(report_file.resolve())
        }))
    else:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        logger.info(f"PixelFrame Engine: Diff report generated at {report_file}")
        
        console = Console()
        table = Table(title="Visual Diff Results")
        table.add_column("Breakpoint", style="cyan")
        table.add_column("Similarity", justify="right")
        table.add_column("Status", justify="center")
        
        for r in diff_results:
            status_str = "[green]PASS[/green]" if r['passed'] else "[red]FAIL[/red]"
            table.add_row(r['name'], f"{r['similarity']}%", status_str)
            
        summary_panel = Panel(
            table, 
            title="PixelFrame Summary", 
            border_style="green" if all_passed else "red",
            expand=False
        )
        console.print(summary_panel)
    
    if not all_passed:
        if not json_output:
            logger.error("Visual diff threshold failed for one or more breakpoints.")
        raise typer.Exit(code=1)


@devices_app.command("list")
def list_available_devices():
    """List all available device presets."""
    devices = list_devices()
    print("Available devices:")
    for d in devices:
        print(f"  - {d}")

logger = setup_logger()


@capture_app.command("run")
def run_capture(
    url: str = typer.Argument(None, help="Website URL to capture (optional if using config)"),
    config_file: str = typer.Option(None, "--config", "-c", help="Path to YAML config file"),
    output: str = typer.Option("pixelframe-output", help="Output directory"),
    full_page: bool = typer.Option(True, help="Capture full page"),
    devices: str = typer.Option(None, help="Comma-separated list of devices to emulate"),
    open_report: bool = typer.Option(False, "--open-report", help="Open the generated HTML report in browser"),
    json_output: bool = typer.Option(False, "--json", help="Output final results as JSON for CI"),
):
    if config_file:
        from pixelframe.engine.config import load_config
        logger.info(f"Loading config from {config_file}")
        try:
            config = load_config(config_file)
        except Exception as e:
            logger.error(str(e))
            raise typer.Exit(code=1)
            
        # CLI overrides
        if url: config.url = url
        if output != "pixelframe-output": config.output_dir = output
        
        if devices:
            device_names = [d.strip() for d in devices.split(",")]
            found_devices = get_devices(device_names)
            if not found_devices:
                logger.error(f"Could not find any valid devices from: {devices}")
                raise typer.Exit(code=1)
            config.breakpoints = [
                Breakpoint(
                    name=d.name, width=d.width, height=d.height,
                    device_scale_factor=d.device_scale_factor,
                    is_mobile=d.is_mobile, has_touch=d.has_touch,
                    user_agent=d.user_agent
                ) for d in found_devices
            ]
    else:
        if not url:
            logger.error("Missing argument 'URL'. Either provide a URL or use --config.")
            raise typer.Exit(code=1)
            
        logger.info(f"Starting PixelFrame for {url}")
        
        if devices:
            device_names = [d.strip() for d in devices.split(",")]
            found_devices = get_devices(device_names)
            if not found_devices:
                logger.error(f"Could not find any valid devices from: {devices}")
                raise typer.Exit(code=1)
            
            breakpoints = [
                Breakpoint(
                    name=d.name, width=d.width, height=d.height,
                    device_scale_factor=d.device_scale_factor,
                    is_mobile=d.is_mobile, has_touch=d.has_touch,
                    user_agent=d.user_agent
                ) for d in found_devices
            ]
        else:
            breakpoints = DEFAULT_BREAKPOINTS

        config = PixelFrameConfig(
            url=url,
            output_dir=output,
            full_page=full_page,
            breakpoints=breakpoints,
        )

    run_path = create_run_directory(config.output_dir)
    browser = BrowserManager()
    browser.start()

    try:
        image_paths = capture_screenshots(config, run_path, browser)
        if not json_output: logger.info("PixelFrame Engine: Screenshots captured successfully.")

        composite_path = run_path / "composite" / "grid.png"
        breakpoint_labels = [
            f"{bp.name.capitalize()} ({bp.width}×{bp.height})"
            for bp in config.breakpoints
        ]
        create_composite(image_paths, composite_path, breakpoint_names=breakpoint_labels)
        if not json_output: logger.info("PixelFrame Engine: Composite grid generated.")

        generate_report(
            config=config,
            run_path=run_path,
            composite_path=composite_path,
            image_paths=image_paths,
            browser_manager=browser,
        )
        if not json_output: logger.info("PixelFrame Engine: Interactive report generated successfully.")
        
        if open_report:
            import webbrowser
            report_file = run_path / "report" / "report.html"
            if report_file.exists():
                webbrowser.open(f"file://{report_file.resolve()}")
                
        if json_output:
            import json
            print(json.dumps({
                "status": "PASSED",
                "run_directory": str(run_path.resolve()),
                "breakpoints": len(config.breakpoints),
                "url": config.url
            }))
        else:
            from rich.console import Console
            from rich.panel import Panel
            
            console = Console()
            summary = (
                f"[bold cyan]URL:[/bold cyan] {config.url}\n"
                f"[bold cyan]Breakpoints:[/bold cyan] {len(config.breakpoints)}\n"
                f"[bold cyan]Output:[/bold cyan] [green]{run_path}[/green]\n"
                f"[bold cyan]Status:[/bold cyan] [bold green]PASSED[/bold green]"
            )
            console.print(Panel(summary, title="PixelFrame Capture Summary", expand=False, border_style="blue"))

    except Exception as e:
        if json_output:
            import json
            print(json.dumps({"status": "FAILED", "error": str(e)}))
        else:
            from rich.console import Console
            Console().print(f"[bold red]❌ Pipeline failed:[/bold red] {e}")
        raise typer.Exit(code=1)
    finally:
        browser.stop()


def main():
    app()


if __name__ == "__main__":
    main()