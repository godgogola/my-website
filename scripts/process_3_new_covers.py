import os
import sys
import json
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\46071e16-07c4-473d-862f-b2bdb120600c"
gdrive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images = r"public\images"
public_og_images = r"public\og-images"
posts_dir = r"src\content\posts"
mapping_file = r"scripts\cover-mapping.json"

os.makedirs(gdrive_dir, exist_ok=True)
os.makedirs(public_images, exist_ok=True)
os.makedirs(public_og_images, exist_ok=True)

items = [
    {
        "filename": "cover_calcium_nutrient_v2_1788094422641.jpg",
        "title": "【營養素】鈣質_穩固身體架構的隱形鋼筋",
        "md_file": "營養素鈣質_穩固身體架構的隱形鋼筋.md"
    },
    {
        "filename": "cover_lipid_medication_1788094439555.jpg",
        "title": "【2026年健保新制】降血脂藥 (藥物篇)",
        "md_file": "2026年健保新制降血脂藥-藥物篇.md"
    },
    {
        "filename": "cover_lipid_guideline_1788094461647.jpg",
        "title": "【2026年健保新制】降血脂藥",
        "md_file": "2026年健保新制降血脂藥.md"
    }
]

print("=== 開始處理 3 張新封面圖 ===")

# 讀取現有 mapping
mapping = []
if os.path.exists(mapping_file):
    try:
        with open(mapping_file, "r", encoding="utf-8") as f:
            mapping = json.load(f)
            if not isinstance(mapping, list):
                mapping = []
    except Exception as e:
        print(f"讀取 mapping 失敗: {e}")

for idx, item in enumerate(items, 1):
    src_path = os.path.join(brain_dir, item["filename"])
    if not os.path.exists(src_path):
        print(f"[{idx}/3] ❌ 找不到來源圖片：{src_path}")
        continue
    
    title = item["title"]
    md_file = item["md_file"]
    webp_name = f"{title}.webp"
    
    img = Image.open(src_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    # 1. 備份 16:9 原圖 PNG 至 Google 雲端硬碟
    gdrive_png = os.path.join(gdrive_dir, f"{title}.png")
    img.save(gdrive_png, "PNG")
    print(f"[{idx}/3] ✅ 1. 原圖備份 PNG 至 Drive: {gdrive_png}")
    
    # 2. 轉檔 WebP 同時存入 public/images 與 public/og-images
    pub_img_path = os.path.join(public_images, webp_name)
    pub_og_path = os.path.join(public_og_images, webp_name)
    
    img.save(pub_img_path, "WEBP", quality=92, method=6)
    img.save(pub_og_path, "WEBP", quality=92, method=6)
    print(f"       ✅ 2. WebP 發布至 public/images & public/og-images: {webp_name}")
    
    # 3. 更新 Markdown 的 frontmatter (coverImage)
    md_path = os.path.join(posts_dir, md_file)
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
                
                lines = frontmatter.strip().split("\n")
                new_lines = []
                has_cover = False
                for line in lines:
                    if line.startswith("coverImage:"):
                        new_lines.append(f'coverImage: "{webp_name}"')
                        has_cover = True
                    else:
                        new_lines.append(line)
                if not has_cover:
                    new_lines.append(f'coverImage: "{webp_name}"')
                
                new_content = "---\n" + "\n".join(new_lines) + "\n---" + body
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"       ✅ 3. Markdown coverImage 更新完成: {md_file}")
    else:
        print(f"       ⚠️ 找不到 Markdown 檔案: {md_path}")
    
    # 4. 更新 mapping (若已存在則更新，不存在則加入)
    found = False
    for entry in mapping:
        if entry.get("title") == title or entry.get("file") == md_file:
            entry["file"] = md_file
            entry["title"] = title
            entry["coverImage"] = webp_name
            found = True
            break
    if not found:
        mapping.append({
            "file": md_file,
            "title": title,
            "coverImage": webp_name
        })

# 儲存更新後的 mapping
with open(mapping_file, "w", encoding="utf-8") as f:
    json.dump(mapping, f, ensure_ascii=False, indent=4)
print("✅ cover-mapping.json 更新完成！")

print("=== 3 篇新封面圖處理完成！ ===")
