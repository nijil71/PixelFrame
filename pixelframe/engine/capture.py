from pathlib import Path
import logging

logger = logging.getLogger("pixelframe")

def capture_screenshots(config, run_path, browser_manager):
    screenshots_path = run_path / "screenshots"
    screenshots_path.mkdir(parents=True, exist_ok=True)
    image_paths = []

    for bp in config.breakpoints:
        logger.info(f"Capturing {bp.name} ({bp.width}x{bp.height})")

        page = browser_manager.new_page(
            width=bp.width, 
            height=bp.height,
            device_scale_factor=bp.device_scale_factor,
            is_mobile=bp.is_mobile,
            has_touch=bp.has_touch,
            user_agent=bp.user_agent
        )
        try:
            page.goto(config.url, wait_until="networkidle", timeout=30000)

            file_path = screenshots_path / f"{bp.name}.png"
            page.screenshot(
                path=str(file_path),
                full_page=config.full_page
            )
            image_paths.append(file_path)
        except Exception as e:
            logger.error(f"Failed to capture {bp.name}: {e}")
        finally:
            page.close()

    if not image_paths:
        raise RuntimeError("No screenshots were captured successfully.")

    return image_paths