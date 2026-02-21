from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_composite(image_paths, output_path):
    images = [Image.open(p) for p in image_paths]

    # Resize for uniform grid preview
    max_width = 600
    resized_images = []

    for img in images:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        resized_images.append(img.resize((max_width, new_height)))

    padding = 40
    cols = 2
    rows = (len(resized_images) + 1) // 2

    widths = [img.width for img in resized_images]
    heights = [img.height for img in resized_images]

    grid_width = cols * max_width + padding * (cols + 1)
    grid_height = sum(
        max(heights[i:i+2]) for i in range(0, len(heights), 2)
    ) + padding * (rows + 1)

    composite = Image.new("RGB", (grid_width, grid_height), (245, 245, 245))

    y_offset = padding
    index = 0

    for row in range(rows):
        x_offset = padding
        row_height = 0

        for col in range(cols):
            if index >= len(resized_images):
                break

            img = resized_images[index]
            composite.paste(img, (x_offset, y_offset))
            row_height = max(row_height, img.height)

            x_offset += max_width + padding
            index += 1

        y_offset += row_height + padding

    composite.save(output_path)
    return output_path