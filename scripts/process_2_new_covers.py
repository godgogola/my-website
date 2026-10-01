import os
import sys
import json
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

targets = [
    {
        "brain_img_path": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\e5245523-e86d-4a53-8065-50cba4f642a3\gi_index_guide_1790856147689.jpg",
        "title": "GI 值大解密",
        "post_file": "gi-值大解密.md",
        "obsidian_file": r"G:\我的雲端硬碟\Wix衛教文章\Wix衛教文章庫\健康飲食\GI 值大解密.md"
    },
    {
        "brain_img_path": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\e5245523-e86d-4a53-8065-50cba4f642a3\protein_portion_guide_v2_1790856180960.jpg",
        "title": "一份蛋白質要怎麼吃",
        "post_file": "一份蛋白質要怎麼吃.md",
        "obsidian_file": r"G:\我的雲端硬碟\Wix衛教文章\Wix衛教文章庫\健康飲食\一份蛋白質要怎麼吃.md"
    }
]

drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")
public_og_images_dir = os.path.join(os.getcwd(), "public", "og-images")
assets_images_dir = os.path.join(os.getcwd(), "src", "assets", "images")
posts_dir = os.path.join(os.getcwd(), "src", "content", "posts")
mapping_file = os.path.join(os.getcwd(), "scripts", "cover-mapping.json")

for d in [public_images_dir, public_og_images_dir, assets_images_dir]:
    os.makedirs(d, exist_ok=True)

# Load existing cover-mapping.json
mapping_data = []
if os.path.exists(mapping_file):
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)

for item in targets:
    title = item["title"]
    img_path = item["brain_img_path"]
    post_file = item["post_file"]
    obsidian_file = item["obsidian_file"]
    cover_name = f"{title}.webp"
    png_name = f"{title}.png"

    print(f"\n--- Processing: {title} ---")
    img = Image.open(img_path)
    w, h = img.size
    target_ratio = 16.0 / 9.0
    current_ratio = w / h

    if abs(current_ratio - target_ratio) > 0.01:
        new_h = int(w / target_ratio)
        if new_h <= h:
            top = (h - new_h) // 2
            cropped = img.crop((0, top, w, top + new_h))
        else:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            cropped = img.crop((left, 0, left + new_w, h))
    else:
        cropped = img

    final_img = cropped.resize((1400, 781), Image.Resampling.LANCZOS)
    print(f"Resized to 1400x781 for {title}")

    # 1. Drive PNG backup
    if os.path.exists(drive_dir):
        drive_png_path = os.path.join(drive_dir, png_name)
        final_img.save(drive_png_path, format="PNG")
        print(f"Saved Drive PNG: {drive_png_path}")

    # 2. Public WebP
    w1 = os.path.join(public_images_dir, cover_name)
    final_img.save(w1, format="WEBP", quality=92)
    print(f"Saved: {w1}")

    # 3. OG WebP
    w2 = os.path.join(public_og_images_dir, cover_name)
    final_img.save(w2, format="WEBP", quality=92)
    print(f"Saved: {w2}")

    # 4. Assets WebP
    w3 = os.path.join(assets_images_dir, cover_name)
    final_img.save(w3, format="WEBP", quality=92)
    print(f"Saved: {w3}")

    # 5. Update Obsidian note frontmatter with coverImage (so future syncs keep it)
    if os.path.exists(obsidian_file):
        with open(obsidian_file, 'r', encoding='utf-8') as f:
            obsidian_content = f.read()
        if obsidian_content.startswith('---'):
            parts = obsidian_content.split('---', 2)
            if len(parts) >= 3:
                fm = parts[1]
                body = parts[2]
                if 'coverImage:' in fm:
                    fm = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{cover_name}"', fm, flags=re.MULTILINE)
                else:
                    fm = fm.strip() + f'\ncoverImage: "{cover_name}"\n'
                obsidian_content = f"---{fm}---{body}"
        else:
            obsidian_content = f'---\ntitle: "{title}"\ncoverImage: "{cover_name}"\n---\n{obsidian_content}'
        with open(obsidian_file, 'w', encoding='utf-8') as f:
            f.write(obsidian_content)
        print(f"Updated Obsidian note frontmatter: {obsidian_file}")

    # 6. Update local post in src/content/posts
    post_path = os.path.join(posts_dir, post_file)
    if os.path.exists(post_path):
        with open(post_path, 'r', encoding='utf-8') as f:
            post_content = f.read()
        if 'coverImage:' in post_content:
            post_content = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{cover_name}"', post_content, flags=re.MULTILINE)
        else:
            post_content = re.sub(r'(^title:.*$)', f'\\1\ncoverImage: "{cover_name}"', post_content, flags=re.MULTILINE)
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(post_content)
        print(f"Updated post frontmatter: {post_path}")

    # 7. Update cover-mapping
    existing_entry = next((e for e in mapping_data if e.get("title") == title or e.get("file") == post_file), None)
    if existing_entry:
        existing_entry["coverImage"] = cover_name
        existing_entry["file"] = post_file
        existing_entry["title"] = title
    else:
        mapping_data.append({
            "file": post_file,
            "title": title,
            "coverImage": cover_name
        })

if os.path.exists(mapping_file):
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping_data, f, ensure_ascii=False, indent=2)
    print("Updated cover-mapping.json successfully!")

print("\n🎉 Both covers processed successfully!")
