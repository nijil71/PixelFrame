from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import logging

logger = logging.getLogger("pixelframe")

# Maximum height for any single image in the composite grid.
# Taller images are cropped with a fade-out indicator at the bottom.
MAX_THUMB_HEIGHT = 800
THUMB_WIDTH = 500
PADDING = 30
LABEL_HEIGHT = 40
BG_COLOR = (30, 30, 30)
CARD_BG = (45, 45, 45)
LABEL_COLOR = (220, 220, 220)
BORDER_COLOR = (70, 70, 70)
FADE_COLOR = BG_COLOR


def _get_font(size=16):
    """Try to load a clean font, fall back to default."""
    try:
        return ImageFont.truetype("arial.ttf", size)
    except (OSError, IOError):
        try:
            return ImageFont.truetype("DejaVuSans.ttf", size)
        except (OSError, IOError):
            return ImageFont.load_default()


def _crop_and_fade(img, max_height):
    """Crop a tall image and add a gradient fade at the bottom to signal continuation."""
    if img.height <= max_height:
        return img

    cropped = img.crop((0, 0, img.width, max_height))

    # Draw a gradient fade at the bottom 60px
    fade_height = 60
    overlay = Image.new("RGBA", (cropped.width, fade_height))
    draw = ImageDraw.Draw(overlay)

    for y in range(fade_height):
        alpha = int(255 * (y / fade_height))
        draw.line(
            [(0, y), (cropped.width, y)],
            fill=(*FADE_COLOR, alpha)
        )

    cropped = cropped.convert("RGBA")
    cropped.paste(overlay, (0, max_height - fade_height), overlay)
    return cropped.convert("RGB")


def create_composite(image_paths, output_path, breakpoint_names=None):
    """
    Create a well-organized composite grid image from screenshots.

    Args:
        image_paths: List of paths to screenshot images.
        output_path: Path to save the composite image.
        breakpoint_names: Optional list of label strings for each image.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not image_paths:
        logger.warning("No images to create composite from.")
        return output_path

    images = []
    for p in image_paths:
        try:
            images.append(Image.open(p))
        except Exception as e:
            logger.error(f"Failed to open image {p}: {e}")

    if not images:
        raise RuntimeError("No valid images to create composite from.")

    # Generate default labels if not provided
    if breakpoint_names is None:
        breakpoint_names = [Path(p).stem for p in image_paths]

    # Ensure we have the right number of labels
    while len(breakpoint_names) < len(images):
        breakpoint_names.append(f"View {len(breakpoint_names) + 1}")

    font = _get_font(16)
    title_font = _get_font(14)

    # Resize each image to THUMB_WIDTH, then crop if too tall
    processed = []
    for img in images:
        ratio = THUMB_WIDTH / img.width
        new_height = int(img.height * ratio)
        resized = img.resize((THUMB_WIDTH, new_height), Image.LANCZOS)
        cropped = _crop_and_fade(resized, MAX_THUMB_HEIGHT)
        processed.append(cropped)

    # Calculate grid layout — auto columns based on count
    count = len(processed)
    if count <= 2:
        cols = count
    elif count <= 4:
        cols = 2
    elif count <= 9:
        cols = 3
    else:
        cols = 4

    rows = (count + cols - 1) // cols

    # Card dimensions (image + label + border padding)
    card_inner_pad = 10
    card_width = THUMB_WIDTH + card_inner_pad * 2
    card_heights = []
    for img in processed:
        card_heights.append(img.height + LABEL_HEIGHT + card_inner_pad * 2)

    # Calculate row heights (max card height in each row)
    row_heights = []
    for r in range(rows):
        start = r * cols
        end = min(start + cols, count)
        row_max = max(card_heights[start:end])
        row_heights.append(row_max)

    # Overall canvas size
    canvas_width = cols * card_width + (cols + 1) * PADDING
    canvas_height = sum(row_heights) + (rows + 1) * PADDING

    composite = Image.new("RGB", (canvas_width, canvas_height), BG_COLOR)
    draw = ImageDraw.Draw(composite)

    # Place each image in the grid
    idx = 0
    y_offset = PADDING

    for r in range(rows):
        x_offset = PADDING

        for c in range(cols):
            if idx >= count:
                break

            img = processed[idx]
            label = breakpoint_names[idx]

            # Draw card background with rounded appearance
            card_h = card_heights[idx]
            draw.rectangle(
                [x_offset, y_offset, x_offset + card_width, y_offset + card_h],
                fill=CARD_BG,
                outline=BORDER_COLOR,
                width=1
            )

            # Paste image centered in card
            img_x = x_offset + card_inner_pad
            img_y = y_offset + card_inner_pad
            composite.paste(img, (img_x, img_y))

            # Draw label below image
            label_y = img_y + img.height + 6
            try:
                bbox = draw.textbbox((0, 0), label, font=title_font)
                text_w = bbox[2] - bbox[0]
            except AttributeError:
                text_w = len(label) * 8
            text_x = x_offset + (card_width - text_w) // 2
            draw.text((text_x, label_y), label, fill=LABEL_COLOR, font=title_font)

            x_offset += card_width + PADDING
            idx += 1

        y_offset += row_heights[r] + PADDING

    composite.save(output_path, quality=95)
    logger.info(f"Composite saved to {output_path}")
    return output_path