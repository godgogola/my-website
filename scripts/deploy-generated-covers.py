import os
from PIL import Image

BRAIN_DIR = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\bfee7289-b515-42c5-aea0-7e7dec669494"
GDRIVE_DIR = r"G:\我的雲端硬碟\衛教文章圖片"
PUBLIC_IMAGES = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\public\images"
PUBLIC_OG = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\public\og-images"

mapping = [
    ("book_cover_15_1792160929204.jpg", "15、華爾街漫步指南"),
    ("book_cover_01_1792160949789.jpg", "01、不入虎穴，焉得虎子"),
    ("book_cover_02_1792160968446.jpg", "02、風險與報酬面面觀"),
    ("book_cover_03_1792161010641.jpg", "03、隨機王國近代史"),
    ("book_cover_04_1792161034235.jpg", "04、完美投資組合"),
    ("book_cover_05_1792161056669.jpg", "05、給成年投資人的資產配置（一）：世界上沒有資產配置精靈"),
    ("book_cover_06_1792161083477.jpg", "06、給成年投資人的資產配置（二）：投資人的年齡"),
    ("book_cover_07_1792161104579.jpg", "07、給成年投資人的資產配置（三）：標準投資組合"),
    ("book_cover_08_1792161127387.jpg", "08、金融時期簡史"),
    ("book_cover_09_1792161153407.jpg", "09、市場頭部浮世繪：狂熱的歷史、病理生理學與診斷"),
    ("book_cover_10_1792161184831.jpg", "10、市場底部浮世繪：有錢人如何變得更有錢"),
]

os.makedirs(GDRIVE_DIR, exist_ok=True)
os.makedirs(PUBLIC_IMAGES, exist_ok=True)
os.makedirs(PUBLIC_OG, exist_ok=True)

print("Starting cover processing...")

for src_file, title in mapping:
    src_path = os.path.join(BRAIN_DIR, src_file)
    if not os.path.exists(src_path):
        print(f"Error: {src_path} not found!")
        continue
    
    with Image.open(src_path) as img:
        # 1. GDrive PNG backup
        png_path = os.path.join(GDRIVE_DIR, f"{title}.png")
        img.save(png_path, "PNG")
        
        # 2. WebP in public/images
        webp_img_path = os.path.join(PUBLIC_IMAGES, f"{title}.webp")
        img.save(webp_img_path, "WEBP", quality=92)
        
        # 3. WebP in public/og-images
        webp_og_path = os.path.join(PUBLIC_OG, f"{title}.webp")
        img.save(webp_og_path, "WEBP", quality=92)
        
        print(f"Processed: {title} ({img.size[0]}x{img.size[1]})")

print("All 11 book covers processed successfully!")
