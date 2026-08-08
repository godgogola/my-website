import sys
import os
from PIL import Image

def crop_to_16_9(input_path, output_png_path, output_webp_path):
    img = Image.open(input_path)
    width, height = img.size

    # Target ratio 16:9
    target_ratio = 16.0 / 9.0
    current_ratio = width / float(height)

    if current_ratio > target_ratio:
        # Too wide, crop sides
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = height
    else:
        # Too tall, crop top and bottom (center crop)
        new_height = int(width / target_ratio)
        left = 0
        top = (height - new_height) // 2
        right = width
        bottom = top + new_height

    cropped_img = img.crop((left, top, right, bottom))
    
    # Ensure directory exists for outputs
    os.makedirs(os.path.dirname(output_png_path), exist_ok=True)
    os.makedirs(os.path.dirname(output_webp_path), exist_ok=True)

    # Save 16:9 PNG
    cropped_img.save(output_png_path, format='PNG')
    # Save 16:9 WebP
    cropped_img.save(output_webp_path, format='WEBP', quality=95)
    print(f"Cropped {input_path} ({width}x{height}) -> 16:9 ({cropped_img.width}x{cropped_img.height})")
    print(f"  Saved 16:9 PNG: {output_png_path}")
    print(f"  Saved 16:9 WebP: {output_webp_path}")

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        crop_to_16_9(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: python crop_16_9.py <input> <output_png> <output_webp>")
