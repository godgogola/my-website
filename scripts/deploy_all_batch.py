import os
import sys
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站"
BRAIN_DIR = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity\brain\117ed57f-c669-446a-9461-82c68173cca1"
GDRIVE_DIR = r"G:\我的雲端硬碟\衛教文章圖片"

PUBLIC_IMAGES = os.path.join(PROJECT_ROOT, "public", "images")
PUBLIC_OG = os.path.join(PROJECT_ROOT, "public", "og-images")
ASSETS_IMAGES = os.path.join(PROJECT_ROOT, "src", "assets", "images")

BOOKS_SITE_DIR = os.path.join(PROJECT_ROOT, "src", "content", "books")
BOOKS_GDRIVE_DIR = r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記"

targets = [
    # 人類大歷史
    {"pattern": "sapiens_17_industrial_wheels", "title": "17、工業的巨輪", "book": "人類大歷史", "file": "17-工業的巨輪.md"},
    {"pattern": "sapiens_18_permanent_revolution", "title": "18、一場永遠的革命", "book": "人類大歷史", "file": "18-一場永遠的革命.md"},
    {"pattern": "sapiens_19_happiness_meaning", "title": "19、從此過著幸福快樂的日子", "book": "人類大歷史", "file": "19-從此過著幸福快樂的日子.md"},
    {"pattern": "sapiens_20_end_of_sapiens", "title": "20、智人末日", "book": "人類大歷史", "file": "20-智人末日.md"},
    # 人類大命運
    {"pattern": "homo_deus_01_new_agenda", "title": "01、人類的三大新議題", "book": "人類大命運", "file": "01-人類的三大新議題.md"},
    {"pattern": "homo_deus_02_anthropocene", "title": "02、人類世", "book": "人類大命運", "file": "02-人類世.md"},
    {"pattern": "homo_deus_03_human_spark", "title": "03、人類的獨特之處", "book": "人類大命運", "file": "03-人類的獨特之處.md"},
    {"pattern": "homo_deus_04_storytellers", "title": "04、說書人", "book": "人類大命運", "file": "04-說書人.md"},
    {"pattern": "homo_deus_05_odd_couple", "title": "05、一對冤家", "book": "人類大命運", "file": "05-一對冤家.md"},
    {"pattern": "homo_deus_06_modern_covenant", "title": "06、與「現代」的契約", "book": "人類大命運", "file": "06-與「現代」的契約.md"},
    {"pattern": "homo_deus_07_humanist_revolution", "title": "07、人本主義革命", "book": "人類大命運", "file": "07-人本主義革命.md"},
    {"pattern": "homo_deus_08_laboratory_time_bomb", "title": "08、實驗室的定時炸彈", "book": "人類大命運", "file": "08-實驗室的定時炸彈.md"},
]

def update_frontmatter(path, webp_name):
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return False
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False
    fm = parts[1]
    body = parts[2]
    if re.search(r"^coverImage:", fm, flags=re.MULTILINE):
        fm = re.sub(r"^coverImage:.*$", f'coverImage: "{webp_name}"', fm, flags=re.MULTILINE)
    else:
        fm = fm.rstrip() + f'\ncoverImage: "{webp_name}"\n'
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"---{fm}---{body}")
    return True

def run():
    brain_files = os.listdir(BRAIN_DIR) if os.path.exists(BRAIN_DIR) else []
    deployed_count = 0
    pending = []

    for t in targets:
        # 尋找 brain_dir 內符合 pattern 的圖片
        matched = [f for f in brain_files if t["pattern"] in f and (f.endswith(".jpg") or f.endswith(".png"))]
        if not matched:
            pending.append(t["title"])
            continue

        src_file = os.path.join(BRAIN_DIR, sorted(matched)[-1])
        title = t["title"]
        webp_name = f"{title}.webp"
        png_name = f"{title}.png"

        img = Image.open(src_file)

        # 1. 備份到 Google Drive
        if os.path.exists(GDRIVE_DIR):
            gdrive_dest = os.path.join(GDRIVE_DIR, png_name)
            img.save(gdrive_dest, "PNG")
            print(f"[Backup] {png_name} -> {gdrive_dest}")

        # 2. 轉檔 WebP
        for dest_dir in [PUBLIC_IMAGES, PUBLIC_OG, ASSETS_IMAGES]:
            os.makedirs(dest_dir, exist_ok=True)
            webp_dest = os.path.join(dest_dir, webp_name)
            img.save(webp_dest, "WEBP", quality=90)

        # 3. 更新 frontmatter
        site_md = os.path.join(BOOKS_SITE_DIR, t["book"], t["file"])
        gdrive_md = os.path.join(BOOKS_GDRIVE_DIR, t["book"], f"{title}.md")

        if update_frontmatter(site_md, webp_name):
            print(f"[Frontmatter] Updated site: {site_md}")
        if update_frontmatter(gdrive_md, webp_name):
            print(f"[Frontmatter] Updated gdrive: {gdrive_md}")

        deployed_count += 1
        print(f"✅ 成功部署: 《{t['book']}》{title} -> {webp_name}")

    print(f"\n==========================================")
    print(f"已完成部署: {deployed_count} / {len(targets)}")
    if pending:
        print(f"尚在生成中: {len(pending)} 篇 -> {', '.join(pending)}")
    print(f"==========================================")

if __name__ == "__main__":
    run()
