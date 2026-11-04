import os, sys, shutil, json
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# Source image files from subagent
raw_images = {
    "代謝異常相關脂肪性肝病與大腸腺瘤": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\_1793799516178.jpg",
    "AI骨密檢查-骨質疏鬆症": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\ai_1793799551298.jpg",
    "【幽門桿菌】【實證】2026NEJM幽門螺旋桿菌回顧與臨床前沿": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\2026nejm_1793799570404.jpg"
}

drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images = r"public\images"
public_og = r"public\og-images"

os.makedirs(drive_dir, exist_ok=True)
os.makedirs(public_images, exist_ok=True)
os.makedirs(public_og, exist_ok=True)

for title, src_path in raw_images.items():
    if not os.path.exists(src_path):
        print(f"ERROR: {src_path} does not exist!")
        continue
    
    # 1. Backup to Google Drive
    drive_dest = os.path.join(drive_dir, f"{title}.png")
    img = Image.open(src_path)
    img.save(drive_dest, format="PNG")
    print(f"Backed up to Drive: {drive_dest}")
    
    # 2. Convert to WebP for public/images and public/og-images
    webp_public = os.path.join(public_images, f"{title}.webp")
    webp_og = os.path.join(public_og, f"{title}.webp")
    
    img.save(webp_public, format="WEBP", quality=92)
    img.save(webp_og, format="WEBP", quality=92)
    print(f"Saved WebP to: {webp_public} and {webp_og}")

# 3. Copy article to 肝膽胰疾病
vault_root = r"G:\我的雲端硬碟\衛教文章庫\衛教文章庫"
article_src = os.path.join(vault_root, "代謝異常相關脂肪性肝病與大腸腺瘤.md")
article_dest = os.path.join(vault_root, "肝膽胰疾病", "代謝異常相關脂肪性肝病與大腸腺瘤.md")

if os.path.exists(article_src) and not os.path.exists(article_dest):
    shutil.copy2(article_src, article_dest)
    print(f"Copied {article_src} -> {article_dest}")

# 4. Update cover-mapping.json
mapping_file = "scripts/cover-mapping.json"
with open(mapping_file, 'r', encoding='utf-8') as f:
    mapping = json.load(f)

# Update or insert
updates = {
    "AI骨密檢查-骨質疏鬆症": "AI骨密檢查-骨質疏鬆症.webp",
    "【幽門桿菌】【實證】2026NEJM幽門螺旋桿菌回顧與臨床前沿": "【幽門桿菌】【實證】2026NEJM幽門螺旋桿菌回顧與臨床前沿.webp",
    "代謝異常相關脂肪性肝病與大腸腺瘤": "代謝異常相關脂肪性肝病與大腸腺瘤.webp"
}

found = set()
for item in mapping:
    t = item.get("title", "")
    if t in updates:
        item["coverImage"] = updates[t]
        found.add(t)

for t, cov in updates.items():
    if t not in found:
        mapping.append({
            "file": f"{t}.md",
            "title": t,
            "coverImage": cov
        })

with open(mapping_file, 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print("Updated scripts/cover-mapping.json with dedicated covers!")

