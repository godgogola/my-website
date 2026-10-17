import os
from PIL import Image

artifacts_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\d56d2cee-ac5a-4d99-bc07-d9eb439bd853"
public_images = r"C:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\public\images"
og_images = r"C:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\public\og-images"
gdrive_dir = r"G:\我的雲端硬碟\衛教文章圖片"

tasks = [
    {
        "src": os.path.join(artifacts_dir, "med_colon_bleeding_1792227283812.jpg"),
        "names": [
            "【下消化道出血】【實證】大腸息肉術後出血處理原則",
            "大腸息肉術後出血處理原則",
            "下消化道出血實證大腸息肉術後出血處理原則"
        ],
        "primary": "【下消化道出血】【實證】大腸息肉術後出血處理原則"
    },
    {
        "src": os.path.join(artifacts_dir, "med_esophagus_junction_1792227303114.jpg"),
        "names": [
            "內視鏡充氣量對食道界線判讀之影響"
        ],
        "primary": "內視鏡充氣量對食道界線判讀之影響"
    },
    {
        "src": os.path.join(artifacts_dir, "med_pcab_ppi_1792227324223.jpg"),
        "names": [
            "【實證】P-CAB vs PPI",
            "實證P-CAB vs PPI",
            "實證p-cab-vs-ppi"
        ],
        "primary": "【實證】P-CAB vs PPI"
    }
]

for t in tasks:
    if not os.path.exists(t["src"]):
        print(f"Not found: {t['src']}")
        continue
    img = Image.open(t["src"])
    resized = img.resize((1400, 781), Image.Resampling.LANCZOS)
    
    for name in t["names"]:
        webp_name = f"{name}.webp"
        resized.save(os.path.join(public_images, webp_name), "WEBP", quality=92)
        resized.save(os.path.join(og_images, webp_name), "WEBP", quality=92)
        print(f"Saved: {webp_name}")
        
    if os.path.exists(gdrive_dir):
        gdrive_png = os.path.join(gdrive_dir, f"{t['primary']}.png")
        gdrive_webp = os.path.join(gdrive_dir, f"{t['primary']}.webp")
        img.save(gdrive_png, "PNG")
        resized.save(gdrive_webp, "WEBP", quality=92)
        print(f"Backed up to GDrive: {t['primary']}")

print("All done!")
