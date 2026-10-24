import os
import sys
import shutil
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(project_root, "public", "images")
public_og_images_dir = os.path.join(project_root, "public", "og-images")
assets_images_dir = os.path.join(project_root, "src", "assets", "images")
brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\260dc583-24b5-4191-9bc4-a8d043ef3d41"

items = [
    {
        "brain_img": os.path.join(brain_dir, "invest_philosophy_1792846876405.jpg"),
        "primary": "05、找出你自己的投資哲學",
        "aliases": ["投資前最重要的事-05、找出你自己的投資哲學", "05-找出你自己的投資哲學", "找出你自己的投資哲學"],
        "book_md": "src/content/books/投資前最重要的事/05-找出你自己的投資哲學.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\05、找出你自己的投資哲學.md"
    },
    {
        "brain_img": os.path.join(brain_dir, "invest_wallstreet_1792847977959.jpg"),
        "primary": "06、華爾街的行為",
        "aliases": ["投資前最重要的事-06、華爾街的行為", "06-華爾街的行為", "華爾街的行為"],
        "book_md": "src/content/books/投資前最重要的事/06-華爾街的行為.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\06、華爾街的行為.md"
    },
    {
        "brain_img": os.path.join(brain_dir, "invest_allocation_1792847999318.jpg"),
        "primary": "07、資產配置",
        "aliases": ["投資前最重要的事-07、資產配置", "07-資產配置", "資產配置"],
        "book_md": "src/content/books/投資前最重要的事/07-資產配置.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\07、資產配置.md"
    },
    {
        "brain_img": os.path.join(brain_dir, "invest_plan_1792848017613.jpg"),
        "primary": "08、完整的綜合投資計畫",
        "aliases": ["投資前最重要的事-08、完整的綜合投資計畫", "08-完整的綜合投資計畫", "完整的綜合投資計畫"],
        "book_md": "src/content/books/投資前最重要的事/08-完整的綜合投資計畫.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\08、完整的綜合投資計畫.md"
    },
    {
        "brain_img": os.path.join(brain_dir, "invest_advisor_1792848036745.jpg"),
        "primary": "09、理財專業人士",
        "aliases": ["投資前最重要的事-09、理財專業人士", "09-理財專業人士", "理財專業人士"],
        "book_md": "src/content/books/投資前最重要的事/09-理財專業人士.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\09、理財專業人士.md"
    },
    {
        "brain_img": os.path.join(brain_dir, "invest_conclusion_1792848057033.jpg"),
        "primary": "10、結語：十個投資概念與建議書單",
        "aliases": ["投資前最重要的事-10、結語：十個投資概念與建議書單", "10-結語十個投資概念與建議書單", "結語：十個投資概念與建議書單", "10、結語十個投資概念與建議書單"],
        "book_md": "src/content/books/投資前最重要的事/10-結語十個投資概念與建議書單.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\10、結語十個投資概念與建議書單.md"
    },
    {
        "brain_img": os.path.join(brain_dir, "sapiens_human_1792848077011.jpg"),
        "primary": "01、人類：一種也沒什麼特別的動物",
        "aliases": ["人類大歷史-01、人類：一種也沒什麼特別的動物", "01-人類一種也沒什麼特別的動物", "人類：一種也沒什麼特別的動物", "01、人類一種也沒什麼特別的動物"],
        "book_md": "src/content/books/人類大歷史/01-人類一種也沒什麼特別的動物.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\01、人類：一種也沒什麼特別的動物.md"
    },
    {
        "brain_img": os.path.join(brain_dir, "sapiens_tree_1792848100874.jpg"),
        "primary": "02、知善惡樹",
        "aliases": ["人類大歷史-02、知善惡樹", "02-知善惡樹", "知善惡樹"],
        "book_md": "src/content/books/人類大歷史/02-知善惡樹.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\02、知善惡樹.md"
    },
    {
        "brain_img": os.path.join(brain_dir, "sapiens_adam_eve_1792848122547.jpg"),
        "primary": "03、亞當和夏娃的一天",
        "aliases": ["人類大歷史-03、亞當和夏娃的一天", "03-亞當和夏娃的一天", "亞當和夏娃的一天"],
        "book_md": "src/content/books/人類大歷史/03-亞當和夏娃的一天.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\人類大歷史\03、亞當和夏娃的一天.md"
    },
    {
        "brain_img": os.path.join(brain_dir, "med_hepc_clean_1792848170619.jpg"),
        "primary": "【C型肝炎】【實證】台灣C型肝炎治療最新、微消除政策與長期預後報告 (2025-2026)",
        "aliases": ["c型肝炎治療與微消除政策", "台灣C型肝炎治療最新微消除政策與長期預後報告"],
        "post_md": "src/content/posts/c型肝炎實證台灣c型肝炎治療最新微消除政策與長期預後報告-2025-2026.md",
        "obsidian_md": None
    },
    {
        "brain_img": os.path.join(brain_dir, "med_glp1_1792848196943.jpg"),
        "primary": "【GLP-1】【實證】腸泌素類藥物延伸效益（防癌・抗成癮・防自戕・護腦）",
        "aliases": ["glp-1腸泌素類藥物延伸效益", "腸泌素類藥物延伸效益防癌抗成癮防自戕護腦"],
        "post_md": "src/content/posts/glp-1實證腸泌素類藥物延伸效益防癌抗成癮防自戕護腦.md",
        "obsidian_md": None
    },
    {
        "brain_img": os.path.join(brain_dir, "med_throat_1792848225440.jpg"),
        "primary": "咽喉異物感",
        "aliases": ["咽喉異物感梅核氣"],
        "post_md": "src/content/posts/咽喉異物感.md",
        "obsidian_md": None
    }
]

os.makedirs(public_images_dir, exist_ok=True)
os.makedirs(public_og_images_dir, exist_ok=True)
os.makedirs(assets_images_dir, exist_ok=True)
has_drive = os.path.exists(drive_dir)

def update_frontmatter(file_path, cover_webp):
    if not os.path.exists(file_path):
        print(f"  ⚠️ 檔案不存在: {file_path}")
        return
    with open(file_path, 'r', encoding='utf-8') as f:
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
            new_content = content
    else:
        new_content = f'---\ncoverImage: "{cover_webp}"\n---\n{content}'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  ✅ 更新 Frontmatter: {os.path.basename(file_path)} -> {cover_webp}")

for item in items:
    brain_img = item["brain_img"]
    primary = item["primary"]
    cover_webp = f"{primary}.webp"
    print(f"\n📦 正在處理: {primary}")
    
    if not os.path.exists(brain_img):
        print(f"  ❌ 找不到原始圖: {brain_img}")
        continue
    
    img = Image.open(brain_img)
    
    # 1. Google Drive 備份
    if has_drive:
        drive_png_path = os.path.join(drive_dir, f"{primary}.png")
        img.save(drive_png_path, format="PNG")
        print(f"  ✅ Drive PNG: {drive_png_path}")
        for alias in item.get("aliases", []):
            try:
                shutil.copyfile(drive_png_path, os.path.join(drive_dir, f"{alias}.png"))
            except Exception as e:
                pass

    # 2. public/images
    pub_webp_path = os.path.join(public_images_dir, cover_webp)
    img.save(pub_webp_path, format="WEBP", quality=92)
    print(f"  ✅ Public WebP: {cover_webp}")
    for alias in item.get("aliases", []):
        shutil.copyfile(pub_webp_path, os.path.join(public_images_dir, f"{alias}.webp"))

    # 3. public/og-images
    og_webp_path = os.path.join(public_og_images_dir, cover_webp)
    img.save(og_webp_path, format="WEBP", quality=92)
    print(f"  ✅ OG WebP: {cover_webp}")
    for alias in item.get("aliases", []):
        shutil.copyfile(og_webp_path, os.path.join(public_og_images_dir, f"{alias}.webp"))

    # 4. src/assets/images
    assets_webp_path = os.path.join(assets_images_dir, cover_webp)
    img.save(assets_webp_path, format="WEBP", quality=92)
    print(f"  ✅ Assets WebP: {cover_webp}")
    for alias in item.get("aliases", []):
        shutil.copyfile(assets_webp_path, os.path.join(assets_images_dir, f"{alias}.webp"))

    # 5. 更新網站 Markdown
    target_md = None
    if item.get("book_md"):
        target_md = os.path.join(project_root, item["book_md"])
    elif item.get("post_md"):
        target_md = os.path.join(project_root, item["post_md"])
    
    if target_md:
        update_frontmatter(target_md, cover_webp)

    # 6. 更新 Obsidian 筆記 (如有)
    if item.get("obsidian_md") and os.path.exists(item["obsidian_md"]):
        update_frontmatter(item["obsidian_md"], cover_webp)

print("\n🎉 12 張封面圖全部轉檔、備份與 Frontmatter 綁定完成！")
