import os
import sys
import shutil
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

items = [
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\155113e7-18b9-4e1b-a1d9-4ac17938d86e\wealth_ladder_spending_1792484971495.jpg",
        "primary": "01、順著財富階梯向上而增加消費",
        "aliases": [
            "順著財富階梯向上而增加消費",
            "財富階梯-01、順著財富階梯向上而增加消費",
            "財富階梯01、順著財富階梯向上而增加消費",
            "01-順著財富階梯向上而增加消費"
        ],
        "book_md": "src/content/books/財富階梯/01-順著財富階梯向上而增加消費.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\01、順著財富階梯向上而增加消費.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\155113e7-18b9-4e1b-a1d9-4ac17938d86e\wealth_ladder_income_1792484993581.jpg",
        "primary": "02、順著財富階梯向上而增加收入",
        "aliases": [
            "順著財富階梯向上而增加收入",
            "財富階梯-02、順著財富階梯向上而增加收入",
            "財富階梯02、順著財富階梯向上而增加收入",
            "02-順著財富階梯向上而增加收入"
        ],
        "book_md": "src/content/books/財富階梯/02-順著財富階梯向上而增加收入.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\02、順著財富階梯向上而增加收入.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\155113e7-18b9-4e1b-a1d9-4ac17938d86e\wealth_ladder_invest_1792485014250.jpg",
        "primary": "03、順著財富階梯向上而增加投資",
        "aliases": [
            "順著財富階梯向上而增加投資",
            "財富階梯-03、順著財富階梯向上而增加投資",
            "財富階梯03、順著財富階梯向上而增加投資",
            "03-順著財富階梯向上而增加投資"
        ],
        "book_md": "src/content/books/財富階梯/03-順著財富階梯向上而增加投資.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\03、順著財富階梯向上而增加投資.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\155113e7-18b9-4e1b-a1d9-4ac17938d86e\wealth_ladder_lvl1_1792485035671.jpg",
        "primary": "04、第 1 階：淨資產小於 1 萬美元（生存穩定）",
        "aliases": [
            "第 1 階：淨資產小於 1 萬美元（生存穩定）",
            "財富階梯-04、第 1 階：淨資產小於 1 萬美元（生存穩定）",
            "財富階梯04、第 1 階：淨資產小於 1 萬美元（生存穩定）",
            "04-第-1-階淨資產小於-1-萬美元生存穩定"
        ],
        "book_md": "src/content/books/財富階梯/04-第-1-階淨資產小於-1-萬美元生存穩定.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\04、第 1 階：淨資產小於 1 萬美元（生存穩定）.md"
    },
    {
        "brain_img": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\155113e7-18b9-4e1b-a1d9-4ac17938d86e\wealth_ladder_lvl2_1792485081858.jpg",
        "primary": "05、第 2 階：淨資產 1 萬～10 萬美元（雜貨自由 ）",
        "aliases": [
            "第 2 階：淨資產 1 萬～10 萬美元（雜貨自由 ）",
            "05、第 2 階：淨資產 1 萬～10 萬美元（雜貨自由）",
            "第 2 階：淨資產 1 萬～10 萬美元（雜貨自由）",
            "財富階梯-05、第 2 階：淨資產 1 萬～10 萬美元（雜貨自由 ）",
            "財富階梯05、第 2 階：淨資產 1 萬～10 萬美元（雜貨自由 ）",
            "05-第-2-階淨資產-1-萬10-萬美元雜貨自由"
        ],
        "book_md": "src/content/books/財富階梯/05-第-2-階淨資產-1-萬10-萬美元雜貨自由.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\05、第 2 階：淨資產 1 萬～10 萬美元（雜貨自由 ）.md"
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

print("🚀 開始處理財富階梯 01-05 封面圖...")

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

print("\n🎉 財富階梯 01-05 封面圖處理全部完成！")
