from PIL import Image
import os
import shutil
import re

images_info = [
    (
        r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_09_immigration_1793713318979.jpg",
        "09、移民：某些文化可能比其他文化更好.webp",
        "src/content/books/21世紀的21堂課/09-移民某些文化可能比其他文化更好.md",
        r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\21世紀的21堂課\09、移民：某些文化可能比其他文化更好.md"
    ),
    (
        r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_10_terrorism_1793713341985.jpg",
        "10、恐怖主義：切勿恐慌.webp",
        "src/content/books/21世紀的21堂課/10-恐怖主義切勿恐慌.md",
        r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\21世紀的21堂課\10、恐怖主義：切勿恐慌.md"
    ),
    (
        r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_11_war_1793713360760.jpg",
        "11、戰爭：永遠不要低估人類的愚蠢.webp",
        "src/content/books/21世紀的21堂課/11-戰爭永遠不要低估人類的愚蠢.md",
        r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\21世紀的21堂課\11、戰爭：永遠不要低估人類的愚蠢.md"
    )
]

drive_backup_dir = r"G:\我的雲端硬碟\衛教文章圖片"

for src_path, webp_name, md_local, md_vault in images_info:
    # 1. Convert to WebP and save to public/images and public/og-images
    im = Image.open(src_path)
    # Ensure 16:9 ratio resize if needed, standard high quality 1400x781
    target_w, target_h = 1400, 788
    im_resized = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    out_img = os.path.join('public/images', webp_name)
    out_og = os.path.join('public/og-images', webp_name)
    im_resized.save(out_img, 'WEBP', quality=90)
    im_resized.save(out_og, 'WEBP', quality=90)
    print(f"Saved: {out_img} and {out_og}")
    
    # 2. Backup PNG to Drive
    if os.path.exists(drive_backup_dir):
        drive_png = os.path.join(drive_backup_dir, webp_name.replace('.webp', '.png'))
        im.save(drive_png, 'PNG')
        print(f"Backed up to Drive: {drive_png}")
        
    # 3. Update local markdown
    if os.path.exists(md_local):
        with open(md_local, encoding='utf-8') as f:
            c = f.read()
        if 'coverImage:' in c:
            c = re.sub(r'coverImage:.*', f'coverImage: "{webp_name}"', c)
        else:
            c = re.sub(r'^order: (.*)$', f'order: \\1\ncoverImage: "{webp_name}"', c, flags=re.MULTILINE)
        with open(md_local, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated local markdown: {md_local}")
        
    # 4. Update Obsidian vault markdown
    if os.path.exists(md_vault):
        with open(md_vault, encoding='utf-8') as f:
            vc = f.read()
        if 'coverImage:' in vc:
            vc = re.sub(r'coverImage:.*', f'coverImage: "{webp_name}"', vc)
        else:
            # check if has frontmatter
            if vc.startswith('---'):
                vc = re.sub(r'^---', f'---\ncoverImage: "{webp_name}"', vc, count=1)
            else:
                vc = f'---\ncoverImage: "{webp_name}"\n---\n' + vc
        with open(md_vault, 'w', encoding='utf-8') as f:
            f.write(vc)
        print(f"Updated vault markdown: {md_vault}")

print("=== Image processing complete! ===")

