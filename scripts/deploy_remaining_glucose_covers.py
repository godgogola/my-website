import os
import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

artifact_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\85c255e0-e5ec-45c1-ae43-c407c4c87425"
gdrive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\public\images"
public_og_dir = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\public\og-images"

mapping = [
    ("glucose_under_skin_1792471203141.jpg", "05、探索皮膚底下的情況：找出葡萄糖驟升"),
    ("glucose_three_things_1792471224461.jpg", "06、火車、吐司和俄羅斯方塊：當血糖驟升時，體內發生的三件事"),
    ("glucose_head_to_toe_1792471245286.jpg", "07、從頭到腳：血糖驟升如何讓我們生病"),
    ("glucose_flat_curve_1792471267601.jpg", "08、如何讓血糖曲線平穩？")
]

for src_name, title in mapping:
    src_path = os.path.join(artifact_dir, src_name)
    if not os.path.exists(src_path):
        print(f"File not found: {src_path}")
        continue
    img = Image.open(src_path)
    
    # 1. 備份 PNG 到 Google Drive
    png_path = os.path.join(gdrive_dir, f"{title}.png")
    img.save(png_path, "PNG")
    
    # 2. 轉檔 WebP 到 public/images
    webp_path = os.path.join(public_images_dir, f"{title}.webp")
    img.save(webp_path, "WEBP", quality=92)
    
    # 3. 轉檔 WebP 到 public/og-images
    og_webp_path = os.path.join(public_og_dir, f"{title}.webp")
    img.save(og_webp_path, "WEBP", quality=92)
    
    # 若標題含問號，也生成一份不含問號的備用檔名以防匹配落空
    if "？" in title:
        alt_title = title.replace("？", "")
        img.save(os.path.join(gdrive_dir, f"{alt_title}.png"), "PNG")
        img.save(os.path.join(public_images_dir, f"{alt_title}.webp"), "WEBP", quality=92)
        img.save(os.path.join(public_og_dir, f"{alt_title}.webp"), "WEBP", quality=92)
    
    print(f"✅ 完成部署: {title}")

print("控糖筆記剩餘 4 張封面圖部署完成！")
