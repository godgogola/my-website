import os
import sys
import glob
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\703d4a0c-5c6b-454b-9cf1-020f10074016"
gdrive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images = r"public\images"
public_og_images = r"public\og-images"
posts_dir = r"src\content\posts"

os.makedirs(gdrive_dir, exist_ok=True)
os.makedirs(public_images, exist_ok=True)
os.makedirs(public_og_images, exist_ok=True)

items = [
    {
        "pattern": "cover_vitamin_b12_*.jpg",
        "title": "【營養素】維生素 B12 (鈷胺素)_造血與神經健康的靈魂守護者",
        "md_file": "營養素維生素-b12-鈷胺素_造血與神經健康的靈魂守護者.md"
    },
    {
        "pattern": "cover_vitamin_b9_*.jpg",
        "title": "【營養素】維生素 B9 (葉酸)_胎兒發育與造血的靈魂密碼",
        "md_file": "營養素維生素-b9-葉酸_胎兒發育與造血的靈魂密碼.md"
    },
    {
        "pattern": "cover_vitamin_b7_*.jpg",
        "title": "【營養素】維生素 B7 (生物素)_豐盈秀髮與強韌指甲的晶亮守護者",
        "md_file": "營養素維生素-b7-生物素_豐盈秀髮與強韌指甲的晶亮守護者.md"
    },
    {
        "pattern": "cover_vitamin_b6_*.jpg",
        "title": "【營養素】維生素 B6 (吡哆素)_穩定情緒與細胞代謝的關鍵鎖鑰",
        "md_file": "營養素維生素-b6-吡哆素_穩定情緒與細胞代謝的關鍵鎖鑰.md"
    },
    {
        "pattern": "cover_vitamin_b5_*.jpg",
        "title": "【營養素】維生素 B5 (泛酸)_細胞的組織更新與壓力緩釋劑",
        "md_file": "營養素維生素-b5-泛酸_細胞的組織更新與壓力緩釋劑.md"
    },
    {
        "pattern": "cover_vitamin_b3_*.jpg",
        "title": "【營養素】維生素 B3 (菸鹼素)_能量新陳代謝樞紐",
        "md_file": "營養素維生素-b3-菸鹼素_能量新陳代謝樞紐.md"
    },
    {
        "pattern": "cover_vitamin_b2_*.jpg",
        "title": "【營養素】維生素 B2 (核黃素)_細胞能量代謝與黏膜健康的關鍵",
        "md_file": "營養素維生素-b2-核黃素_細胞能量代謝與黏膜健康的關鍵.md"
    },
    {
        "pattern": "cover_vitamin_b1_*.jpg",
        "title": "【營養素】維生素 B1 (硫胺素)_提神與能量代謝的活氧燃料",
        "md_file": "營養素維生素-b1-硫胺素_提神與能量代謝的活氧燃料.md"
    },
    {
        "pattern": "cover_iron_nutrient_*.jpg",
        "title": "【營養素】鐵質_血液與能量的動力之源",
        "md_file": "營養素鐵質_血液與能量的動力之源.md"
    },
    {
        "pattern": "cover_zinc_nutrient_*.jpg",
        "title": "【營養素】鋅質_細胞分裂與免疫防禦的隱形引擎",
        "md_file": "營養素鋅質_細胞分裂與免疫防禦的隱形引擎.md"
    }
]

print("=== 開始處理 10 張營養素封面圖 ===")

for idx, item in enumerate(items, 1):
    matches = glob.glob(os.path.join(brain_dir, item["pattern"]))
    if not matches:
        print(f"[{idx}/10] 找不到圖片：{item['pattern']}")
        continue
    
    # 取得最新的一張
    matches.sort(key=os.path.getmtime, reverse=True)
    src_path = matches[0]
    title = item["title"]
    md_file = item["md_file"]
    
    img = Image.open(src_path)
    # 確保 RGB
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    # 1. 備份 PNG 到 G 槽雲端硬碟
    gdrive_png = os.path.join(gdrive_dir, f"{title}.png")
    img.save(gdrive_png, "PNG")
    
    # 2. 轉 WebP 存入 public/images 與 public/og-images
    webp_name = f"{title}.webp"
    pub_img_path = os.path.join(public_images, webp_name)
    pub_og_path = os.path.join(public_og_images, webp_name)
    
    img.save(pub_img_path, "WEBP", quality=92, method=6)
    img.save(pub_og_path, "WEBP", quality=92, method=6)
    
    print(f"[{idx}/10] ✅ 完成圖片發布與備份: {title}")
    
    # 3. 更新 Markdown 的 frontmatter (coverImage)
    md_path = os.path.join(posts_dir, md_file)
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 檢查 frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
                
                # 如果已經有 coverImage，替換它；如果沒有，加在 frontmatter 最後
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
                print(f"       ✅ Markdown 封面更新: {md_file}")
    else:
        print(f"       ⚠️ 找不到 Markdown 檔案: {md_file}")

print("=== 全部 10 篇營養素封面圖處理完成！ ===")
