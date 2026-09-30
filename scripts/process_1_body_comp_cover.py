import os
import sys
import json
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

brain_img_path = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\0afe64a2-54c6-470d-ba27-fd45f6391450\cover_body_composition_glp1_1790775039509.jpg"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")
public_og_images_dir = os.path.join(os.getcwd(), "public", "og-images")
assets_images_dir = os.path.join(os.getcwd(), "src", "assets", "images")
posts_dir = os.path.join(os.getcwd(), "src", "content", "posts")
mapping_file = os.path.join(os.getcwd(), "scripts", "cover-mapping.json")

for d in [public_images_dir, public_og_images_dir, assets_images_dir]:
    os.makedirs(d, exist_ok=True)

img = Image.open(brain_img_path)
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
print("Prepared final_img 1400x781")

variants = ["打瘦瘦針前要先測身體組成", "【瘦瘦針】打瘦瘦針前要先測身體組成"]

for name in variants:
    # 1. Drive PNG
    if os.path.exists(drive_dir):
        png_path = os.path.join(drive_dir, f"{name}.png")
        final_img.save(png_path, format="PNG")
        print(f"Saved Drive PNG: {png_path}")
    # 2. Public WebP
    w1 = os.path.join(public_images_dir, f"{name}.webp")
    final_img.save(w1, format="WEBP", quality=92)
    # 3. OG WebP
    w2 = os.path.join(public_og_images_dir, f"{name}.webp")
    final_img.save(w2, format="WEBP", quality=92)
    # 4. Assets WebP
    w3 = os.path.join(assets_images_dir, f"{name}.webp")
    final_img.save(w3, format="WEBP", quality=92)
    print(f"Saved WebP versions for: {name}")

# Update post frontmatter
post_file = "瘦瘦針打瘦瘦針前要先測身體組成.md"
post_path = os.path.join(posts_dir, post_file)
if os.path.exists(post_path):
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'coverImage:' in content:
        content = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', 'coverImage: "【瘦瘦針】打瘦瘦針前要先測身體組成.webp"', content, flags=re.MULTILINE)
    else:
        content = re.sub(r'(^title:.*$)', '\\1\ncoverImage: "【瘦瘦針】打瘦瘦針前要先測身體組成.webp"', content, flags=re.MULTILINE)
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated Markdown frontmatter!")

# Update cover-mapping.json
if os.path.exists(mapping_file):
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)
    mapping_titles = {entry.get("title"): entry for entry in mapping_data}
    
    for name in variants:
        webp_file = f"{name}.webp"
        if name in mapping_titles:
            mapping_titles[name]["coverImage"] = webp_file
            mapping_titles[name]["file"] = post_file
        else:
            mapping_data.append({
                "file": post_file,
                "title": name,
                "coverImage": webp_file
            })
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping_data, f, ensure_ascii=False, indent=2)
    print("Updated cover-mapping.json successfully!")

print("🎉 Complete execution finished!")
