import os, sys, shutil, re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# The 9 generated images
images_map = {
    "12、謙遜：你不是世界的中心": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_12_humility_1793801597998.jpg",
    "13、上帝：不要妄稱上帝的名": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_13_god_1793801616236.jpg",
    "14、世俗主義：承認你的陰影": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_14_secularism_1793801636981.jpg",
    "15、無知：你知道的比你想像的少": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_15_ignorance_1793801653883.jpg",
    "17、後真相：有些假新聞永遠存在": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_17_posttruth_1793801607952.jpg",
    "18、科幻小說：未來不是你在電影裡看到的樣子": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_18_scifi_1793801618702.jpg",
    "19、教育：改變是唯一的常態": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_19_education_1793801638165.jpg",
    "20、意義：人生不是一個故事": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_20_meaning_1793801649288.jpg",
    "21、內觀：僅僅觀察": r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\c917a291-f072-4304-8a6a-e706feb550ad\21lessons_21_meditation_1793801668600.jpg"
}

public_img_dir = "public/images"
public_og_dir = "public/og-images"
drive_img_dir = r"G:\我的雲端硬碟\衛教文章圖片"
books_dir = "src/content/books/21世紀的21堂課"
vault_books_dir = r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\21世紀的21堂課"

os.makedirs(public_img_dir, exist_ok=True)
os.makedirs(public_og_dir, exist_ok=True)
os.makedirs(drive_img_dir, exist_ok=True)

for title, src_jpg in images_map.items():
    if not os.path.exists(src_jpg):
        print(f"Skipping {title}, file not found: {src_jpg}")
        continue
    
    img = Image.open(src_jpg)
    
    # 1. Save PNG to Google Drive
    drive_png = os.path.join(drive_img_dir, f"{title}.png")
    img.save(drive_png, format="PNG")
    print(f"Backed up to Drive: {drive_png}")
    
    # 2. Save WebP to public/images and public/og-images
    webp_name = f"{title}.webp"
    public_webp = os.path.join(public_img_dir, webp_name)
    og_webp = os.path.join(public_og_dir, webp_name)
    
    img.save(public_webp, format="WEBP", quality=92)
    img.save(og_webp, format="WEBP", quality=92)
    print(f"Saved WebP: {public_webp}")
    
    # 3. Update Markdown in src/content/books/21世紀的21堂課
    # Find matching md file
    prefix = title.split('、')[0] # e.g. "12"
    for fname in os.listdir(books_dir):
        if fname.startswith(prefix) and fname.endswith('.md'):
            fpath = os.path.join(books_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'coverImage:' in content:
                content = re.sub(r'coverImage:\s*["\']?[^"\']+["\']?', f'coverImage: "{webp_name}"', content)
            else:
                content = content.replace('---', f'---\ncoverImage: "{webp_name}"', 1)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated frontmatter in {fpath}")
            
    # 4. Also update Obsidian vault if it exists
    if os.path.exists(vault_books_dir):
        for fname in os.listdir(vault_books_dir):
            if fname.startswith(prefix) and fname.endswith('.md'):
                fpath = os.path.join(vault_books_dir, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'coverImage:' in content:
                    content = re.sub(r'coverImage:\s*["\']?[^"\']+["\']?', f'coverImage: "{webp_name}"', content)
                else:
                    content = content.replace('---', f'---\ncoverImage: "{webp_name}"', 1)
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated frontmatter in Vault: {fpath}")

print("All 9 generated images processed and frontmatters updated successfully!")
