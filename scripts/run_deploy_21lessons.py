import os
import sys
import shutil
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站"
drive_backup_dir = r"G:\我的雲端硬碟\衛教文章圖片"
obsidian_dir = r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\21世紀的21堂課"
site_books_dir = os.path.join(project_root, "src", "content", "books", "21世紀的21堂課")
public_images = os.path.join(project_root, "public", "images")
public_og_images = os.path.join(project_root, "public", "og-images")
assets_images = os.path.join(project_root, "src", "assets", "images")

items = [
    {
        "jpg": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_01_disillusionment_1793620238220.jpg",
        "title": "01、幻滅：歷史的終結延後了",
        "obsidian_file": "01、幻滅：歷史的終結延後了.md",
        "site_file": "01-幻滅歷史的終結延後了.md"
    },
    {
        "jpg": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_02_work_ai_1793620255463.jpg",
        "title": "02、工作：當你長大，可能沒有工作",
        "obsidian_file": "02、工作：當你長大，可能沒有工作.md",
        "site_file": "02-工作當你長大-可能沒有工作.md"
    },
    {
        "jpg": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_03_liberty_big_data_1793620275794.jpg",
        "title": "03、自由：大數據正在看著你",
        "obsidian_file": "03、自由：大數據正在看著你.md",
        "site_file": "03-自由大數據正在看著你.md"
    },
    {
        "jpg": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_04_equality_data_1793620294389.jpg",
        "title": "04、平等：掌握數據者掌握未來",
        "obsidian_file": "04、平等：掌握數據者掌握未來.md",
        "site_file": "04-平等掌握數據者掌握未來.md"
    },
    {
        "jpg": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_05_community_bodies_1793620255350.jpg",
        "title": "05、社群：人類有身體",
        "obsidian_file": "05、社群：人類有身體.md",
        "site_file": "05-社群人類有身體.md"
    },
    {
        "jpg": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_06_civilisation_one_world_1793620274005.jpg",
        "title": "06、文明：世界上只有一種文明",
        "obsidian_file": "06、文明：世界上只有一種文明.md",
        "site_file": "06-文明世界上只有一種文明.md"
    },
    {
        "jpg": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_07_nationalism_global_answers_1793620293694.jpg",
        "title": "07、民族主義：全球性問題需要全球性解答",
        "obsidian_file": "07、民族主義：全球性問題需要全球性解答.md",
        "site_file": "07-民族主義全球性問題需要全球性解答.md"
    },
    {
        "jpg": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_08_religion_science_state_1793620311363.jpg",
        "title": "08、宗教：上帝現在為國家服務",
        "obsidian_file": "08、宗教：上帝現在為國家服務.md",
        "site_file": "08-宗教上帝現在為國家服務.md"
    }
]

def update_obsidian(md_path, cover_webp_name):
    if not os.path.exists(md_path):
        print(f"Obsidian note not found: {md_path}")
        return
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            if re.search(r'^coverImage:', fm, flags=re.MULTILINE):
                fm = re.sub(r'^coverImage:.*$', f'coverImage: "{cover_webp_name}"', fm, flags=re.MULTILINE)
            else:
                fm = fm.rstrip() + f'\ncoverImage: "{cover_webp_name}"\n'
            new_content = f"---{fm}---{body}"
        else:
            new_content = f'---\ncoverImage: "{cover_webp_name}"\n---\n{content}'
    else:
        new_content = f'---\ncoverImage: "{cover_webp_name}"\n---\n{content}'

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated Obsidian: {os.path.basename(md_path)} -> {cover_webp_name}")

def update_site(md_path, cover_webp_name):
    if not os.path.exists(md_path):
        print(f"Site note not found: {md_path}")
        return
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            if re.search(r'^coverImage:', fm, flags=re.MULTILINE):
                fm = re.sub(r'^coverImage:.*$', f'coverImage: "{cover_webp_name}"', fm, flags=re.MULTILINE)
            else:
                fm = fm.rstrip() + f'\ncoverImage: "{cover_webp_name}"\n'
            new_content = f"---{fm}---{body}"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated Site: {os.path.basename(md_path)} -> {cover_webp_name}")

for item in items:
    jpg_path = item["jpg"]
    title = item["title"]
    if not os.path.exists(jpg_path):
        print(f"Error: missing {jpg_path}")
        continue

    img = Image.open(jpg_path)
    print(f"\nProcessing {title} (Size: {img.size})...")

    # 1. Backup PNG to G-Drive
    png_name = f"{title}.png"
    if os.path.exists(drive_backup_dir):
        gdrive_png = os.path.join(drive_backup_dir, png_name)
        img.save(gdrive_png, "PNG")
        print(f"  Backup PNG saved: {gdrive_png}")

    # 2. WebP to public/images, public/og-images, src/assets/images
    webp_name = f"{title}.webp"
    for dest_dir in [public_images, public_og_images, assets_images]:
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, webp_name)
        img.save(dest_path, "WEBP", quality=90)
        print(f"  WebP saved: {dest_path}")

    # 3. Update Markdown files
    obsidian_file_path = os.path.join(obsidian_dir, item["obsidian_file"])
    site_file_path = os.path.join(site_books_dir, item["site_file"])
    update_obsidian(obsidian_file_path, webp_name)
    update_site(site_file_path, webp_name)

print("\n🎉 All 8 chapters processed and deployed successfully!")

