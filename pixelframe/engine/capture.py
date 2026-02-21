from pathlib import Path
import logging

logger = logging.getLogger("pixelframe")

def capture_screenshots(config, run_path, browser_manager):
    screenshots_path = run_path / "screenshots"
    image_paths = []

    for bp in config.breakpoints:
        logger.info(f"Capturing {bp.name} ({bp.width}x{bp.height})")

        page = browser_manager.new_page(bp.width, bp.height)
        page.goto(config.url, wait_until="networkidle")

        file_path = screenshots_path / f"{bp.name}.png"
        page.screenshot(
            path=str(file_path),
            full_page=config.full_page
        )

        page.close()
        image_paths.append(file_path)

    return image_paths