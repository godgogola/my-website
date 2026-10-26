import os
import sys
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

img_path = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\117ed57f-c669-446a-9461-82c68173cca1\sapiens_16_capitalist_creed_1792992995109.jpg"
title = "16、資本主義的教條"
webp_name = f"{title}.webp"
png_name = f"{title}.png"

if os.path.exists(img_path):
    img = Image.open(img_path)

    # 1. Backup to G-Drive
    drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
    if os.path.exists(drive_dir):
        img.save(os.path.join(drive_dir, png_name), "PNG")
        print("Saved to G-Drive:", png_name)

    # 2. Save WebP
    for d in ["public/images", "public/og-images", "src/assets/images"]:
        os.makedirs(d, exist_ok=True)
        dest = os.path.join(d, webp_name)
        img.save(dest, "WEBP", quality=90)
        print("Saved to", d, ":", webp_name)

    # 3. Update frontmatter
    def update_fm(path):
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            if re.search(r"^coverImage:", fm, flags=re.MULTILINE):
                fm = re.sub(r"^coverImage:.*$", f'coverImage: "{webp_name}"', fm, flags=re.MULTILINE)
            else:
                fm = fm.rstrip() + f'\ncoverImage: "{webp_name}"\n'
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"---{fm}---{body}")
            print("Updated frontmatter:", path)

    update_fm("src/content/books/人類大歷史/16-資本主義的教條.md")
    update_fm(r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\16、資本主義的教條.md")
