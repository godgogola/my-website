import os
import shutil
from PIL import Image

deploy_map = [
    {
        "title": "S-ABCDE 高血壓生活型態調整",
        "src": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\diorama_s_abcde_1794128722126.jpg",
    },
    {
        "title": "最新高血壓診斷分級與 722 量測準則",
        "src": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\diorama_722_measure_v2_1794128747173.jpg",
    },
    {
        "title": "次發性高血壓",
        "src": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\diorama_secondary_htn_1794128730120.jpg",
    },
    {
        "title": "長期血壓控制不良的併發症",
        "src": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\diorama_htn_complications_notext_1794128753685.jpg",
    },
    {
        "title": "高血壓藥物介紹",
        "src": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\diorama_htn_meds_intro_1794128743264.jpg",
    },
    {
        "title": "高血壓藥物在一般族群及共病族群的選擇",
        "src": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\diorama_htn_meds_selection_1794128752393.jpg",
    },
    {
        "title": "高血壓藥物效果",
        "src": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\medical_hypertension_diorama_test_1794063739540.jpg",
    },
]

drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = r"public\images"
public_og_dir = r"public\og-images"

os.makedirs(drive_dir, exist_ok=True)
os.makedirs(public_images_dir, exist_ok=True)
os.makedirs(public_og_dir, exist_ok=True)

for item in deploy_map:
    title = item["title"]
    src = item["src"]
    
    if not os.path.exists(src):
        print(f"❌ Source not found: {src}")
        continue
        
    print(f"\nProcessing: 《{title}》...")
    with Image.open(src) as img:
        img_rgb = img.convert('RGB')
        
        # 1. Backup PNG to Google Drive
        drive_png_path = os.path.join(drive_dir, f"{title}.png")
        img_rgb.save(drive_png_path, "PNG", quality=95)
        print(f"  ✅ Drive PNG: {drive_png_path}")
        
        # 2. Save WebP to public/images/
        web_path = os.path.join(public_images_dir, f"{title}.webp")
        img_rgb.save(web_path, "WEBP", quality=90)
        print(f"  ✅ public/images: {web_path}")
        
        # 3. Save WebP to public/og-images/
        og_path = os.path.join(public_og_dir, f"{title}.webp")
        img_rgb.save(og_path, "WEBP", quality=90)
        print(f"  ✅ public/og-images: {og_path}")

print("\n🎉 All 7 images processed successfully!")

