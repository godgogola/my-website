import os
import sys
import shutil
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站"
drive_backup_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images = os.path.join(project_root, "public", "images")
public_og_images = os.path.join(project_root, "public", "og-images")
assets_images = os.path.join(project_root, "src", "assets", "images")
brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\35cf9a87-4df7-45ec-8c0b-89890e0d09ce"

items = [
    {
        "jpg": os.path.join(brain_dir, "sapiens_flood_1792936636975.jpg"),
        "title": "04、毀天滅地的人類洪水",
        "site_md": "src/content/books/人類大歷史/04-毀天滅地的人類洪水.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\04、毀天滅地的人類洪水.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_wheat_1792936654222.jpg"),
        "title": "05、史上最大騙局",
        "site_md": "src/content/books/人類大歷史/05-史上最大騙局.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\05、史上最大騙局.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_pyramids_1792936672633.jpg"),
        "title": "06、蓋起監獄高牆",
        "site_md": "src/content/books/人類大歷史/06-蓋起監獄高牆.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\06、蓋起監獄高牆.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_memory_1792936695076.jpg"),
        "title": "07、大腦記憶過載",
        "site_md": "src/content/books/人類大歷史/07-大腦記憶過載.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\07、大腦記憶過載.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_hierarchy_1792936715519.jpg"),
        "title": "08、歷史從無正義",
        "site_md": "src/content/books/人類大歷史/08-歷史從無正義.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\08、歷史從無正義.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_unification_1792936735440.jpg"),
        "title": "09、歷史的方向",
        "site_md": "src/content/books/人類大歷史/09-歷史的方向.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\09、歷史的方向.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_money_1792936756168.jpg"),
        "title": "10、金錢的氣味",
        "site_md": "src/content/books/人類大歷史/10-金錢的氣味.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\10、金錢的氣味.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_empire_1792936799708.jpg"),
        "title": "11、帝國的願景",
        "site_md": "src/content/books/人類大歷史/11-帝國的願景.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\11、帝國的願景.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_religion_1792936835513.jpg"),
        "title": "12、宗教的法則",
        "site_md": "src/content/books/人類大歷史/12-宗教的法則.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\12、宗教的法則.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_success_1792936857302.jpg"),
        "title": "13、成敗的祕密",
        "site_md": "src/content/books/人類大歷史/13-成敗的祕密.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\13、成敗的祕密.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_ignorance_1792936887359.jpg"),
        "title": "14、發現自己的無知",
        "site_md": "src/content/books/人類大歷史/14-發現自己的無知.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\14、發現自己的無知.md"
    },
    {
        "jpg": os.path.join(brain_dir, "sapiens_science_1792936910767.jpg"),
        "title": "15、科學與帝國的聯姻",
        "site_md": "src/content/books/人類大歷史/15-科學與帝國的聯姻.md",
        "gdrive_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\15、科學與帝國的聯姻.md"
    }
]

def update_frontmatter(md_path, cover_webp_name):
    if not os.path.exists(md_path):
        print(f"File not found: {md_path}")
        return
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return
    parts = content.split('---', 2)
    if len(parts) < 3:
        return
    fm = parts[1]
    body = parts[2]
    
    if re.search(r'^coverImage:', fm, flags=re.MULTILINE):
        fm = re.sub(r'^coverImage:.*$', f'coverImage: "{cover_webp_name}"', fm, flags=re.MULTILINE)
    else:
        fm = fm.rstrip() + f'\ncoverImage: "{cover_webp_name}"\n'
    
    new_content = f"---{fm}---{body}"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated frontmatter: {md_path} -> {cover_webp_name}")

for item in items:
    jpg_path = item["jpg"]
    title = item["title"]
    if not os.path.exists(jpg_path):
        print(f"Error: missing {jpg_path}")
        continue
    
    img = Image.open(jpg_path)
    
    # 1. Backup PNG to G-Drive
    png_name = f"{title}.png"
    if os.path.exists(drive_backup_dir):
        gdrive_png = os.path.join(drive_backup_dir, png_name)
        img.save(gdrive_png, "PNG")
        print(f"Saved G-Drive backup: {gdrive_png}")
    
    # 2. WebP to public/images, public/og-images, src/assets/images
    webp_name = f"{title}.webp"
    for dest_dir in [public_images, public_og_images, assets_images]:
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, webp_name)
        img.save(dest_path, "WEBP", quality=90)
        print(f"Saved WebP: {dest_path}")
    
    # 3. Update frontmatter
    update_frontmatter(item["site_md"], webp_name)
    update_frontmatter(item["gdrive_md"], webp_name)

print("\nAll 12 chapters deployed successfully!")
