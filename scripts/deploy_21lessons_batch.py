import os
import sys
import shutil
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站"
drive_backup_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images = os.path.join(project_root, "public", "images")
public_og_images = os.path.join(project_root, "public", "og-images")
assets_images = os.path.join(project_root, "src", "assets", "images")

def update_obsidian_markdown(md_path, cover_webp_name):
    if not os.path.exists(md_path):
        print(f"Obsidian note not found: {md_path}")
        return
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            if re.search(r'^coverImage:', fm, flags=re.MULTILINE):
                fm = re.sub(r'^coverImage:.*$', f'coverImage: "{cover_webp_name}"', fm, flags=re.MULTILINE)
            else:
                fm = fm.rstrip() + f'\ncoverImage: "{cover_webp_name}"\n'
            new_content = f"---{fm}---{body}"
        else:
            new_content = f'---\ncoverImage: "{cover_webp_name}"\n---\n{content}'
    else:
        new_content = f'---\ncoverImage: "{cover_webp_name}"\n---\n{content}'

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated Obsidian frontmatter: {md_path} -> {cover_webp_name}")

def update_site_markdown(md_path, cover_webp_name):
    if not os.path.exists(md_path):
        print(f"Site note not found: {md_path}")
        return
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            if re.search(r'^coverImage:', fm, flags=re.MULTILINE):
                fm = re.sub(r'^coverImage:.*$', f'coverImage: "{cover_webp_name}"', fm, flags=re.MULTILINE)
            else:
                fm = fm.rstrip() + f'\ncoverImage: "{cover_webp_name}"\n'
            new_content = f"---{fm}---{body}"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated Site frontmatter: {md_path} -> {cover_webp_name}")

def process_item(image_path, title, obsidian_file, site_file):
    if not os.path.exists(image_path):
        print(f"Error: image not found at {image_path}")
        return False

    img = Image.open(image_path)

    # 1. Backup PNG to G-Drive
    png_name = f"{title}.png"
    if os.path.exists(drive_backup_dir):
        gdrive_png = os.path.join(drive_backup_dir, png_name)
        img.save(gdrive_png, "PNG")
        print(f"Saved G-Drive backup: {gdrive_png}")

    # 2. WebP to public/images, public/og-images, src/assets/images
    webp_name = f"{title}.webp"
    for dest_dir in [public_images, public_og_images, assets_images]:
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, webp_name)
        img.save(dest_path, "WEBP", quality=90)
        print(f"Saved WebP: {dest_path}")

    # 3. Update Markdown files
    update_obsidian_markdown(obsidian_file, webp_name)
    update_site_markdown(site_file, webp_name)
    return True

