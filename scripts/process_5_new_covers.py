import os
import sys
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f6782200-767d-43c0-9c0c-b4ccca9153df"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")
public_og_images_dir = os.path.join(os.getcwd(), "public", "og-images")
posts_dir = os.path.join(os.getcwd(), "src", "content", "posts")

os.makedirs(public_images_dir, exist_ok=True)
os.makedirs(public_og_images_dir, exist_ok=True)

targets = [
    {
        "prefix": "kidney_stone_hydronephrosis",
        "title": "【腹部超音波】腎結石及水腎",
        "file": "腹部超音波腎結石及水腎.md"
    },
    {
        "prefix": "anesthesia_medicine",
        "title": "【麻醉藥】",
        "file": "麻醉藥.md"
    },
    {
        "prefix": "sleeping_pills_comparison",
        "title": "【安眠藥】安眠藥的比較",
        "file": "安眠藥安眠藥的比較.md"
    },
    {
        "prefix": "erispan_somnolence",
        "title": "【安眠藥】Erispan會嗜睡",
        "file": "安眠藥erispan會嗜睡.md"
    },
    {
        "prefix": "sleep_medication_principles",
        "title": "【安眠藥】用藥原則",
        "file": "安眠藥用藥原則.md"
    }
]

brain_files = os.listdir(brain_dir)
print("=== 開始依最高規格 SOP 處理 5 張全新封面圖 ===")

success_count = 0

for idx, item in enumerate(targets):
    matching_files = [f for f in brain_files if f.startswith(item["prefix"]) and f.endswith(".png")]
    if not matching_files:
        print(f"❌ [{idx+1}] 找不到前綴為 {item['prefix']} 的原圖")
        continue

    matching_files.sort(key=lambda f: os.path.getmtime(os.path.join(brain_dir, f)), reverse=True)
    latest_file = matching_files[0]
    src_path = os.path.join(brain_dir, latest_file)

    img = Image.open(src_path)
    w, h = img.size

    # Crop to 16:9
    target_ratio = 16.0 / 9.0
    current_ratio = w / h

    if abs(current_ratio - target_ratio) > 0.02:
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

    # Resize to standard high-res 1400x781
    final_img = cropped.resize((1400, 781), Image.Resampling.LANCZOS)

    # 1. 備份 16:9 PNG 至 Google Drive (G:\我的雲端硬碟\衛教文章圖片)
    if os.path.exists(drive_dir):
        drive_png_path = os.path.join(drive_dir, f"{item['title']}.png")
        final_img.save(drive_png_path, format="PNG")
        print(f"   💾 1. Drive PNG 備份成功: {drive_png_path}")
    else:
        print(f"   ⚠️ Drive 目錄未掛載，跳過 Drive 儲存: {drive_dir}")

    # 2. 轉檔為高品質 WebP 同步發布到 public/images 與 public/og-images
    webp_name = f"{item['title']}.webp"
    public_webp_path = os.path.join(public_images_dir, webp_name)
    public_og_webp_path = os.path.join(public_og_images_dir, webp_name)

    final_img.save(public_webp_path, format="WEBP", quality=92)
    print(f"   🌐 2. WebP 發布成功: {public_webp_path}")

    final_img.save(public_og_webp_path, format="WEBP", quality=92)
    print(f"   🌐 2. OG-WebP 發布成功: {public_og_webp_path}")

    # 3. 更新對應 Markdown 檔案中的 coverImage 欄位
    md_path = os.path.join(posts_dir, item["file"])
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'coverImage:' in content:
            content = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{webp_name}"', content, flags=re.MULTILINE)
        else:
            content = re.sub(r'(^title:.*$)', f'\\1\ncoverImage: "{webp_name}"', content, flags=re.MULTILINE)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📝 3. Markdown coverImage 綁定完成: {item['file']}")
    else:
        print(f"   ⚠️ MD 檔案不存在: {md_path}")

    success_count += 1
    print(f"✅ [{idx+1}/5] 完成: {item['title']}\n")

print(f"🎉 全部 5 張封面圖均已依 SOP 處理完成！共成功 {success_count} 篇！")
