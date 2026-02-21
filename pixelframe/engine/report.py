from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import base64
import logging

logger = logging.getLogger("pixelframe")


def _image_to_base64(image_path):
    """Convert an image file to a base64 data URI for self-contained HTML."""
    path = Path(image_path)
    if not path.exists():
        logger.warning(f"Image not found: {image_path}")
        return ""

    suffix = path.suffix.lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    mime = mime_map.get(suffix, "image/png")

    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime};base64,{encoded}"


def generate_report(config, run_path, composite_path, image_paths, browser_manager):
    """Generate an HTML report and convert it to PDF."""
    templates_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("report.html")

    # Build screenshot data with base64-encoded images
    screenshots_data = []
    for bp, img_path in zip(config.breakpoints, image_paths):
        img_path = Path(img_path)
        file_size_kb = round(img_path.stat().st_size / 1024, 1) if img_path.exists() else 0

        screenshots_data.append({
            "name": bp.name,
            "width": bp.width,
            "height": bp.height,
            "path": _image_to_base64(img_path),
            "file_size_kb": file_size_kb,
        })

    composite_b64 = _image_to_base64(composite_path)

    html_content = template.render(
        url=config.url,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        composite_path=composite_b64,
        screenshots=screenshots_data,
    )

    report_dir = run_path / "report"
    report_dir.mkdir(exist_ok=True)

    html_file = report_dir / "report.html"
    html_file.write_text(html_content, encoding="utf-8")

    pdf_file = report_dir / "pixelframe-report.pdf"

    # Use existing browser to generate PDF
    page = browser_manager.browser.new_page()
    try:
        page.goto(html_file.resolve().as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(pdf_file),
            format="A4",
            print_background=True,
            margin={"top": "15mm", "bottom": "15mm", "left": "10mm", "right": "10mm"},
        )
        logger.info(f"PDF report saved to {pdf_file}")
    except Exception as e:
        logger.error(f"Failed to generate PDF: {e}")
    finally:
        page.close()

    return pdf_file