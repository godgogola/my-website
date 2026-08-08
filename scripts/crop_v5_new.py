import os
import re
from PIL import Image

artifact_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\d0bbff17-1170-46fc-a3b2-5bf2112488d8"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")
posts_dir = os.path.join(os.getcwd(), "src", "content", "posts")

v5_items = [
    { "prefix": "v5_ag_ratio_balance", "title": "【AG ratio】", "file": "ag-ratio.md" },
    { "prefix": "v5_albumin_synthesis", "title": "【Albumin】白蛋白的合成與低下原因", "file": "albumin白蛋白的合成與低下原因.md" },
    { "prefix": "v5_bilirubin_isolated_high", "title": "【膽紅素】單純膽紅素偏高", "file": "膽紅素單純膽紅素偏高.md" },
    { "prefix": "v5_globulin_immune_soldiers", "title": "【Globulin】球蛋白", "file": "globulin球蛋白.md" },
    { "prefix": "v5_hdl_investigation", "title": "【HDL】HDL太高是好事嗎", "file": "hdlhdl太高是好事嗎.md" },
    { "prefix": "v5_carbs_fat_mechanism", "title": "碳水化合物造成脂肪堆積的機制", "file": "碳水化合物造成脂肪堆積的機制.md" }
]

artifact_files = os.listdir(artifact_dir)

for idx, item in enumerate(v5_items):
    png_file = next((f for f in artifact_files if f.startswith(item["prefix"]) and f.endswith(".png")), None)
    if not png_file:
        print(f"Skipping {item['title']}: not found")
        continue

    src_path = os.path.join(artifact_dir, png_file)
    img = Image.open(src_path)
    w, h = img.size
    
    target_ratio = 16.0 / 9.0
    new_h = int(w / target_ratio)
    left = 0
    top = (h - new_h) // 2
    right = w
    bottom = top + new_h

    cropped = img.crop((left, top, right, bottom))

    # 1. Drive PNG
    drive_png_path = os.path.join(drive_dir, f"{item['title']}.png")
    cropped.save(drive_png_path, format="PNG")

    # 2. Public WebP
    webp_name = f"{item['title']}.webp"
    public_webp_path = os.path.join(public_images_dir, webp_name)
    cropped.save(public_webp_path, format="WEBP", quality=95)

    # 3. Artifact PNG
    artifact_crop_path = os.path.join(artifact_dir, f"crop169_{item['prefix']}.png")
    cropped.save(artifact_crop_path, format="PNG")

    # 4. Markdown update
    md_path = os.path.join(posts_dir, item["file"])
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'coverImage:' in content:
            content = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{webp_name}"', content, flags=re.MULTILINE)
        else:
            content = re.sub(r'(^title:.*$)', f'\\1\ncoverImage: "{webp_name}"', content, flags=re.MULTILINE)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"[{idx+1}/6] {item['title']} -> 16:9 crop ({cropped.width}x{cropped.height}) -> Drive PNG & public WebP OK")

print("\n=== V5 CROP & DEPLOY COMPLETE! ===")
