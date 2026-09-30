import os
import sys
import json
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

title = "打瘦瘦針前要先測身體組成"
file_name = "打瘦瘦針前要先測身體組成.md"
webp_name = f"{title}.webp"

brain_img_path = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\0afe64a2-54c6-470d-ba27-fd45f6391450\cover_body_composition_glp1_1790775039509.jpg"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")
public_og_images_dir = os.path.join(os.getcwd(), "public", "og-images")
posts_dir = os.path.join(os.getcwd(), "src", "content", "posts")
mapping_file = os.path.join(os.getcwd(), "scripts", "cover-mapping.json")

os.makedirs(public_images_dir, exist_ok=True)
os.makedirs(public_og_images_dir, exist_ok=True)

img = Image.open(brain_img_path)
w, h = img.size
print(f"原始尺寸: {w}x{h}")

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
print(f"調整後尺寸: {final_img.size}")

# 1. 備份 16:9 PNG 至 Google Drive
if os.path.exists(drive_dir):
    drive_png_path = os.path.join(drive_dir, f"{title}.png")
    final_img.save(drive_png_path, format="PNG")
    print(f"💾 1. Drive PNG 備份成功: {drive_png_path}")
else:
    print(f"⚠️ Drive 目錄未找到: {drive_dir}")

# 2. 轉檔為 WebP 發布至 public/images 與 public/og-images
pub_img_path = os.path.join(public_images_dir, webp_name)
pub_og_path = os.path.join(public_og_images_dir, webp_name)

final_img.save(pub_img_path, format="WEBP", quality=92)
print(f"🌐 2. WebP 發布成功: {pub_img_path}")
final_img.save(pub_og_path, format="WEBP", quality=92)
print(f"🌐 2. OG-WebP 發布成功: {pub_og_path}")

# 3. 更新 Markdown coverImage
md_path = os.path.join(posts_dir, file_name)
if os.path.exists(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'coverImage:' in content:
        content = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{webp_name}"', content, flags=re.MULTILINE)
    else:
        content = re.sub(r'(^title:.*$)', f'\\1\ncoverImage: "{webp_name}"', content, flags=re.MULTILINE)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📝 3. Markdown coverImage 綁定完成: {file_name}")
else:
    print(f"⚠️ Markdown 檔案不存在: {md_path}")

# 4. 更新 cover-mapping.json
if os.path.exists(mapping_file):
    with open(mapping_file, 'r', encoding='utf-8') as f:
        mapping_data = json.load(f)
    found = False
    for entry in mapping_data:
        if entry.get("title") == title or entry.get("file") == file_name:
            entry["coverImage"] = webp_name
            entry["file"] = file_name
            entry["title"] = title
            found = True
            break
    if not found:
        mapping_data.append({
            "file": file_name,
            "title": title,
            "coverImage": webp_name
        })
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping_data, f, ensure_ascii=False, indent=2)
    print("📑 4. cover-mapping.json 更新成功！")

print("✨ 全部 SOP 步驟執行完畢！")
