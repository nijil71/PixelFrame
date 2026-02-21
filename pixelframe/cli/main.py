import typer
from pixelframe.engine.logger import setup_logger
from pixelframe.engine.config import PixelFrameConfig, DEFAULT_BREAKPOINTS
from pixelframe.engine.run_manager import create_run_directory
from pixelframe.engine.browser import BrowserManager
from pixelframe.engine.capture import capture_screenshots

# Root app
app = typer.Typer(help="PixelFrame - Responsive Screenshot Automation Engine")

# Sub command group
capture_app = typer.Typer()
app.add_typer(capture_app, name="capture")

logger = setup_logger()


@capture_app.command("run")
def run_capture(
    url: str = typer.Argument(..., help="Website URL to capture"),
    output: str = typer.Option("pixelframe-output", help="Output directory"),
    full_page: bool = typer.Option(True, help="Capture full page"),
):
    logger.info(f"Starting PixelFrame for {url}")

    config = PixelFrameConfig(
        url=url,
        output_dir=output,
        full_page=full_page,
        breakpoints=DEFAULT_BREAKPOINTS,
    )

    run_path = create_run_directory(output)

    browser = BrowserManager()
    browser.start()

    try:
        capture_screenshots(config, run_path, browser)
        logger.info("Screenshots captured successfully.")
    finally:
        browser.stop()

    logger.info(f"Run completed at {run_path}")


def main():
    app()


if __name__ == "__main__":
    main()