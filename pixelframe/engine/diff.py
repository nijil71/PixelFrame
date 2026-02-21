from PIL import Image, ImageChops, ImageEnhance, ImageDraw
from pathlib import Path
import logging

logger = logging.getLogger("pixelframe")

def generate_diff(img1_path: Path, img2_path: Path, output_path: Path) -> float:
    """
    Compare two images and save a diff image showing highlighted differences.
    Returns the similarity percentage.
    """
    if not img1_path.exists() or not img2_path.exists():
        logger.error("Missing image for diffing.")
        return 0.0

    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")

    # If dimensions mismatch, crop/pad to the maximum size of both
    max_w = max(img1.width, img2.width)
    max_h = max(img1.height, img2.height)

    if (img1.width, img1.height) != (max_w, max_h):
        new_img1 = Image.new("RGB", (max_w, max_h), (255, 255, 255))
        new_img1.paste(img1, (0, 0))
        img1 = new_img1

    if (img2.width, img2.height) != (max_w, max_h):
        new_img2 = Image.new("RGB", (max_w, max_h), (255, 255, 255))
        new_img2.paste(img2, (0, 0))
        img2 = new_img2

    # Calculate difference
    diff = ImageChops.difference(img1, img2)

    # Calculate similarity score
    # difference returns an image where pixel values represent the absolute difference.
    # We sum up the differences and calculate the percentage of changed pixels.
    bbox = diff.getbbox()
    if not bbox:
        # Images are exactly identical
        diff.save(output_path)
        return 100.0

    # To visualize diffs clearly, we convert to grayscale, then colorize differences as red
    diff_gray = diff.convert("L")
    
    # Enhance the difference so it's very visible
    diff_gray = ImageEnhance.Contrast(diff_gray).enhance(5.0)
    
    # Create a red overlay where differences exist
    red_mask = Image.new("RGB", (max_w, max_h), (255, 0, 0))
    
    # Fade the base image (img2) to 30% opacity to use as a backdrop
    base_faded = Image.blend(img2, Image.new("RGB", (max_w, max_h), (255, 255, 255)), 0.7)
    
    # Composite the red highlights over the faded base image
    diff_composite = Image.composite(red_mask, base_faded, diff_gray)
    
    diff_composite.save(output_path)
    
    # Rough similarity calculation based on non-zero pixels in grayscale diff
    histogram = diff_gray.histogram()
    # The first element is the number of fully black pixels (no difference)
    identical_pixels = histogram[0]
    total_pixels = max_w * max_h
    similarity = (identical_pixels / total_pixels) * 100.0
    
    return round(similarity, 2)

def create_side_by_side(img1_path: Path, img2_path: Path, diff_path: Path, output_path: Path, label1: str, label2: str):
    """Create a 3-panel side-by-side composite."""
    images = [Image.open(p) for p in (img1_path, img2_path, diff_path)]
    
    padding = 20
    max_h = max(img.height for img in images)
    total_w = sum(img.width for img in images) + padding * 4
    
    canvas = Image.new("RGB", (total_w, max_h + 60), (245, 245, 245))
    draw = ImageDraw.Draw(canvas)
    
    titles = [label1, label2, "Diff Overlay"]
    
    x_offset = padding
    for i, img in enumerate(images):
        # Draw title
        draw.text((x_offset, 20), titles[i], fill=(0, 0, 0))
        
        # Paste image
        canvas.paste(img, (x_offset, 50))
        x_offset += img.width + padding
        
    canvas.save(output_path)
    return output_path
