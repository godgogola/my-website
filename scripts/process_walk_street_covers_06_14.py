import os
import sys
import shutil
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

items = [
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_06_random_1792069330279.jpg",
        "primary": "06、隨機漫步華爾街",
        "aliases": ["漫步華爾街06、隨機漫步華爾街", "漫步華爾街-06、隨機漫步華爾街", "隨機漫步華爾街"],
        "book_md": "src/content/books/漫步華爾街/06-隨機漫步華爾街.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\06、隨機漫步華爾街.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_07_efficient_1792069367706.jpg",
        "primary": "07、效率市場假說",
        "aliases": ["漫步華爾街07、效率市場假說", "漫步華爾街-07、效率市場假說", "效率市場假說"],
        "book_md": "src/content/books/漫步華爾街/07-效率市場假說.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\07、效率市場假說.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_08_portfolio_1792069388008.jpg",
        "primary": "08、現代投資組合",
        "aliases": ["漫步華爾街08、現代投資組合", "漫步華爾街-08、現代投資組合", "現代投資組合"],
        "book_md": "src/content/books/漫步華爾街/08-現代投資組合.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\08、現代投資組合.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_09_risk_1792069411259.jpg",
        "primary": "09、風險與報酬模型",
        "aliases": ["漫步華爾街09、風險與報酬模型", "漫步華爾街-09、風險與報酬模型", "風險與報酬模型"],
        "book_md": "src/content/books/漫步華爾街/09-風險與報酬模型.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\09、風險與報酬模型.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_10_behavior_1792069435598.jpg",
        "primary": "10、行為財務學",
        "aliases": ["漫步華爾街10、行為財務學", "漫步華爾街-10、行為財務學", "行為財務學"],
        "book_md": "src/content/books/漫步華爾街/10-行為財務學.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\10、行為財務學.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_11_technology_1792069458567.jpg",
        "primary": "11、投資新技術",
        "aliases": ["漫步華爾街11、投資新技術", "漫步華爾街-11、投資新技術", "投資新技術"],
        "book_md": "src/content/books/漫步華爾街/11-投資新技術.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\11、投資新技術.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_12_exercises_1792069484950.jpg",
        "primary": "12、個人理財十練習",
        "aliases": ["漫步華爾街12、個人理財十練習", "漫步華爾街-12、個人理財十練習", "個人理財十練習"],
        "book_md": "src/content/books/漫步華爾街/12-個人理財十練習.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\12、個人理財十練習.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_13_predict_1792069512798.jpg",
        "primary": "13、股債報酬預測",
        "aliases": ["漫步華爾街13、股債報酬預測", "漫步華爾街-13、股債報酬預測", "股債報酬預測"],
        "book_md": "src/content/books/漫步華爾街/13-股債報酬預測.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\13、股債報酬預測.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_14_lifecycle_1792069540476.jpg",
        "primary": "14、人生投資規劃",
        "aliases": ["漫步華爾街14、人生投資規劃", "漫步華爾街-14、人生投資規劃", "人生投資規劃"],
        "book_md": "src/content/books/漫步華爾街/14-人生投資規劃.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\14、人生投資規劃.md"
    }
]

project_root = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(project_root, "public", "images")
public_og_images_dir = os.path.join(project_root, "public", "og-images")
assets_images_dir = os.path.join(project_root, "src", "assets", "images")

target_w, target_h = 1400, 781
target_ratio = target_w / target_h

print("🚀 開始處理漫步華爾街 06-14 封面圖...")

for item in items:
    brain_img_path = item["brain_img"]
    primary = item["primary"]
    cover_webp = f"{primary}.webp"
    cover_png = f"{primary}.png"

    print(f"\n📦 處理: {primary}")
    if not os.path.exists(brain_img_path):
        print(f"❌ 找不到來源圖檔: {brain_img_path}")
        continue

    img = Image.open(brain_img_path)
    w, h = img.size
    current_ratio = w / h

    if abs(current_ratio - target_ratio) > 0.01:
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            cropped = img.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            cropped = img.crop((0, top, w, top + new_h))
    else:
        cropped = img

    final_img = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # 1. Google Drive PNG
    if os.path.exists(drive_dir):
        drive_png_path = os.path.join(drive_dir, cover_png)
        final_img.save(drive_png_path, format="PNG")
        print(f"  ✅ Drive PNG: {cover_png}")
        for alias in item["aliases"]:
            shutil.copyfile(drive_png_path, os.path.join(drive_dir, f"{alias}.png"))

    # 2. public/images
    pub_webp_path = os.path.join(public_images_dir, cover_webp)
    final_img.save(pub_webp_path, format="WEBP", quality=92)
    print(f"  ✅ Public WebP: {cover_webp}")
    for alias in item["aliases"]:
        shutil.copyfile(pub_webp_path, os.path.join(public_images_dir, f"{alias}.webp"))

    # 3. public/og-images
    og_webp_path = os.path.join(public_og_images_dir, cover_webp)
    final_img.save(og_webp_path, format="WEBP", quality=92)
    print(f"  ✅ OG WebP: {cover_webp}")
    for alias in item["aliases"]:
        shutil.copyfile(og_webp_path, os.path.join(public_og_images_dir, f"{alias}.webp"))

    # 4. src/assets/images
    assets_webp_path = os.path.join(assets_images_dir, cover_webp)
    final_img.save(assets_webp_path, format="WEBP", quality=92)
    print(f"  ✅ Assets WebP: {cover_webp}")
    for alias in item["aliases"]:
        shutil.copyfile(assets_webp_path, os.path.join(assets_images_dir, f"{alias}.webp"))

    # 5. 更新網站筆記 Markdown
    book_md_path = os.path.join(project_root, item["book_md"])
    if os.path.exists(book_md_path):
        with open(book_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                fm = parts[1]
                body = parts[2]
                if 'coverImage:' in fm:
                    fm = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{cover_webp}"', fm, flags=re.MULTILINE)
                else:
                    fm = fm.strip() + f'\ncoverImage: "{cover_webp}"\n'
                new_content = f"---{fm}---{body}"
        else:
            new_content = f'---\ntitle: "{primary}"\ncoverImage: "{cover_webp}"\n---\n{content}'
        with open(book_md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ 更新網站筆記: {item['book_md']}")

    # 6. 更新 Obsidian 筆記
    obs_path = item["obsidian_md"]
    if os.path.exists(obs_path):
        with open(obs_path, 'r', encoding='utf-8') as f:
            obs_content = f.read()
        if obs_content.startswith('---'):
            parts = obs_content.split('---', 2)
            if len(parts) >= 3:
                fm = parts[1]
                body = parts[2]
                if 'coverImage:' in fm:
                    fm = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{cover_webp}"', fm, flags=re.MULTILINE)
                else:
                    fm = fm.strip() + f'\ncoverImage: "{cover_webp}"\n'
                new_obs_content = f"---{fm}---{body}"
        else:
            new_obs_content = f'---\ntitle: "{primary}"\ncoverImage: "{cover_webp}"\n---\n{obs_content}'
        with open(obs_path, 'w', encoding='utf-8') as f:
            f.write(new_obs_content)
        print(f"  ✅ 更新 Obsidian 筆記: {os.path.basename(obs_path)}")

print("\n🎉 漫步華爾街 06-14 封面處理全部完成！")
