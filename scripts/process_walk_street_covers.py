import os
import sys
import shutil
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

items = [
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_01_theory_1792067851315.jpg",
        "primary": "01、漫步華爾街理論",
        "aliases": ["漫步華爾街01、漫步華爾街理論", "漫步華爾街-01、漫步華爾街理論", "漫步華爾街理論"],
        "book_md": "src/content/books/漫步華爾街/01-漫步華爾街理論.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\01、漫步華爾街理論.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_02_crowds_1792067881999.jpg",
        "primary": "02、瘋狂的群眾",
        "aliases": ["漫步華爾街02、瘋狂的群眾", "漫步華爾街-02、瘋狂的群眾", "瘋狂的群眾"],
        "book_md": "src/content/books/漫步華爾街/02-瘋狂的群眾.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\02、瘋狂的群眾.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_03_bubbles_1792067902197.jpg",
        "primary": "03、投機泡沫史",
        "aliases": ["漫步華爾街03、投機泡沫史", "漫步華爾街-03、投機泡沫史", "投機泡沫史"],
        "book_md": "src/content/books/漫步華爾街/03-投機泡沫史.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\03、投機泡沫史.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_04_century_1792067924647.jpg",
        "primary": "04、世紀資產泡沫",
        "aliases": ["漫步華爾街04、世紀資產泡沫", "漫步華爾街-04、世紀資產泡沫", "世紀資產泡沫"],
        "book_md": "src/content/books/漫步華爾街/04-世紀資產泡沫.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\04、世紀資產泡沫.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f7ca6852-971e-428f-bad2-78f22f668c94\walk_05_analysis_1792067948098.jpg",
        "primary": "05、投資分析解析",
        "aliases": ["漫步華爾街05、投資分析解析", "漫步華爾街-05、投資分析解析", "投資分析解析"],
        "book_md": "src/content/books/漫步華爾街/05-投資分析解析.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\漫步華爾街\05、投資分析解析.md"
    }
]

project_root = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(project_root, "public", "images")
public_og_images_dir = os.path.join(project_root, "public", "og-images")
assets_images_dir = os.path.join(project_root, "src", "assets", "images")

os.makedirs(public_images_dir, exist_ok=True)
os.makedirs(public_og_images_dir, exist_ok=True)
os.makedirs(assets_images_dir, exist_ok=True)

target_w, target_h = 1400, 781
target_ratio = target_w / target_h

print("🚀 開始處理漫步華爾街 01-05 封面圖...")

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

    # 裁剪與縮放到 1400x781
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

    # 1. Google Drive PNG 備份
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

    # 5. 更新 src/content/books Markdown frontmatter
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
        print(f"  ✅ 更新網站筆記 frontmatter: {item['book_md']}")

    # 6. 更新 Obsidian 來源筆記 frontmatter
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
        print(f"  ✅ 更新 Obsidian 筆記 frontmatter: {os.path.basename(obs_path)}")

print("\n🎉 漫步華爾街前五篇文章封面處理全部完成！")
