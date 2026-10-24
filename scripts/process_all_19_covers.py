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
inbox_dir = os.path.join(project_root, "scripts", "covers_inbox")

os.makedirs(public_images_dir, exist_ok=True)
os.makedirs(public_og_images_dir, exist_ok=True)
os.makedirs(assets_images_dir, exist_ok=True)
os.makedirs(inbox_dir, exist_ok=True)

target_w, target_h = 1400, 781
target_ratio = target_w / target_h

# 19 張封面圖完整清單
items = [
    # === 《財富階梯》昨日未完成 (07～10) ===
    {
        "id": "wl_07",
        "book": "財富階梯",
        "keywords": ["wealth_ladder_lvl4", "wealth_ladder_travel", "07、第 4 階", "第 4 階：淨資產 100 萬～1,000 萬美元（旅行自由 ）.png"],
        "primary": "07、第 4 階：淨資產 100 萬～1,000 萬美元（旅行自由 ）",
        "aliases": [
            "第 4 階：淨資產 100 萬～1,000 萬美元（旅行自由 ）",
            "07、第 4 階：淨資產 100 萬～1,000 萬美元（旅行自由）",
            "第 4 階：淨資產 100 萬～1,000 萬美元（旅行自由）",
            "財富階梯-07、第 4 階：淨資產 100 萬～1,000 萬美元（旅行自由 ）",
            "07-第-4-階淨資產-100-萬1-000-萬美元旅行自由"
        ],
        "book_md": "src/content/books/財富階梯/07-第-4-階淨資產-100-萬1-000-萬美元旅行自由.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\07、第 4 階：淨資產 100 萬～1,000 萬美元（旅行自由 ）.md"
    },
    {
        "id": "wl_08",
        "book": "財富階梯",
        "keywords": ["wealth_ladder_lvl5", "wealth_ladder_housing", "08、第 5 階", "第 5 階：淨資產 1,000 萬～1 億美元（住宅自由）.png"],
        "primary": "08、第 5 階：淨資產 1,000 萬～1 億美元（住宅自由）",
        "aliases": [
            "第 5 階：淨資產 1,000 萬～1 億美元（住宅自由）",
            "財富階梯-08、第 5 階：淨資產 1,000 萬～1 億美元（住宅自由）",
            "08-第-5-階淨資產-1-000-萬1-億美元住宅自由"
        ],
        "book_md": "src/content/books/財富階梯/08-第-5-階淨資產-1-000-萬1-億美元住宅自由.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\08、第 5 階：淨資產 1,000 萬～1 億美元（住宅自由）.md"
    },
    {
        "id": "wl_09",
        "book": "財富階梯",
        "keywords": ["wealth_ladder_lvl6", "wealth_ladder_impact", "09、第 6 階", "第 6 階：淨資產 1 億美元以上（影響力自由）.png"],
        "primary": "09、第 6 階：淨資產 1 億美元以上（影響力自由）",
        "aliases": [
            "第 6 階：淨資產 1 億美元以上（影響力自由）",
            "財富階梯-09、第 6 階：淨資產 1 億美元以上（影響力自由）",
            "09-第-6-階淨資產-1-億美元以上影響力自由"
        ],
        "book_md": "src/content/books/財富階梯/09-第-6-階淨資產-1-億美元以上影響力自由.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\09、第 6 階：淨資產 1 億美元以上（影響力自由）.md"
    },
    {
        "id": "wl_10",
        "book": "財富階梯",
        "keywords": ["wealth_ladder_marathon", "wealth_ladder_time", "10、攀爬財富階梯", "攀爬財富階梯得花多久時間"],
        "primary": "10、攀爬財富階梯得花多久時間？",
        "aliases": [
            "攀爬財富階梯得花多久時間？",
            "10、攀爬財富階梯得花多久時間",
            "攀爬財富階梯得花多久時間",
            "財富階梯-10、攀爬財富階梯得花多久時間？",
            "10-攀爬財富階梯得花多久時間"
        ],
        "book_md": "src/content/books/財富階梯/10-攀爬財富階梯得花多久時間.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\10、攀爬財富階梯得花多久時間？.md"
    },
    # === 《財富階梯》今日新圖 (11～13 + 整合筆記) ===
    {
        "id": "wl_11",
        "book": "財富階梯",
        "keywords": ["wealth_ladder_salt", "wealth_ladder_happiness", "11、金錢能買到幸福嗎", "金錢能買到幸福嗎"],
        "primary": "11、金錢能買到幸福嗎？",
        "aliases": [
            "金錢能買到幸福嗎？",
            "11、金錢能買到幸福嗎",
            "金錢能買到幸福嗎",
            "財富階梯-11、金錢能買到幸福嗎？",
            "11-金錢能買到幸福嗎"
        ],
        "book_md": "src/content/books/財富階梯/11-金錢能買到幸福嗎.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\11、金錢能買到幸福嗎？.md"
    },
    {
        "id": "wl_12",
        "book": "財富階梯",
        "keywords": ["wealth_ladder_amplifier", "wealth_ladder_wealth_types", "12、人生強化器", "人生強化器"],
        "primary": "12、人生強化器",
        "aliases": [
            "人生強化器",
            "財富階梯-12、人生強化器",
            "12-人生強化器"
        ],
        "book_md": "src/content/books/財富階梯/12-人生強化器.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\12、人生強化器.md"
    },
    {
        "id": "wl_13",
        "book": "財富階梯",
        "keywords": ["wealth_ladder_journey", "wealth_ladder_climb", "13、我在財富階梯往上爬的旅程", "我在財富階梯往上爬的旅程"],
        "primary": "13、我在財富階梯往上爬的旅程",
        "aliases": [
            "我在財富階梯往上爬的旅程",
            "財富階梯-13、我在財富階梯往上爬的旅程",
            "13-我在財富階梯往上爬的旅程"
        ],
        "book_md": "src/content/books/財富階梯/13-我在財富階梯往上爬的旅程.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\13、我在財富階梯往上爬的旅程.md"
    },
    {
        "id": "wl_summary",
        "book": "財富階梯",
        "keywords": ["wealth_ladder_taiwan", "台灣版《財富階梯》整合筆記", "台灣版財富階梯整合筆記"],
        "primary": "台灣版《財富階梯》整合筆記",
        "aliases": [
            "台灣版財富階梯整合筆記",
            "財富階梯-台灣版《財富階梯》整合筆記",
            "財富階梯台灣版《財富階梯》整合筆記"
        ],
        "book_md": "src/content/books/財富階梯/台灣版財富階梯整合筆記.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\財富階梯\台灣版《財富階梯》整合筆記.md"
    },
    # === 《投資前最重要的事》今日新圖 (00～10) ===
    {
        "id": "inv_00",
        "book": "投資前最重要的事",
        "keywords": ["investing_simplicity", "00、為何單純代表全新定義的老練", "為何單純代表全新定義的老練"],
        "primary": "00、為何單純代表全新定義的老練？",
        "aliases": [
            "為何單純代表全新定義的老練？",
            "00、為何單純代表全新定義的老練",
            "為何單純代表全新定義的老練",
            "投資前最重要的事-00、為何單純代表全新定義的老練？",
            "00-為何單純代表全新定義的老練"
        ],
        "book_md": "src/content/books/投資前最重要的事/00-為何單純代表全新定義的老練.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\00、為何單純代表全新定義的老練？.md"
    },
    {
        "id": "inv_01",
        "book": "投資前最重要的事",
        "keywords": ["investing_retail_vs_inst", "01、散戶投資人相對機構投資人", "散戶投資人相對機構投資人"],
        "primary": "01、散戶投資人相對機構投資人",
        "aliases": [
            "散戶投資人相對機構投資人",
            "投資前最重要的事-01、散戶投資人相對機構投資人",
            "01-散戶投資人相對機構投資人"
        ],
        "book_md": "src/content/books/投資前最重要的事/01-散戶投資人相對機構投資人.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\01、散戶投資人相對機構投資人.md"
    },
    {
        "id": "inv_02",
        "book": "投資前最重要的事",
        "keywords": ["investing_negative_knowledge", "02、負面知識與成功投資人需具備的特質", "負面知識與成功投資人需具備的特質"],
        "primary": "02、負面知識與成功投資人需具備的特質",
        "aliases": [
            "負面知識與成功投資人需具備的特質",
            "投資前最重要的事-02、負面知識與成功投資人需具備的特質",
            "02-負面知識與成功投資人需具備的特質"
        ],
        "book_md": "src/content/books/投資前最重要的事/02-負面知識與成功投資人需具備的特質.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\02、負面知識與成功投資人需具備的特質.md"
    },
    {
        "id": "inv_03",
        "book": "投資前最重要的事",
        "keywords": ["investing_market_risk", "03、定義市場與投資組合風險", "定義市場與投資組合風險"],
        "primary": "03、定義市場與投資組合風險",
        "aliases": [
            "定義市場與投資組合風險",
            "投資前最重要的事-03、定義市場與投資組合風險",
            "03-定義市場與投資組合風險"
        ],
        "book_md": "src/content/books/投資前最重要的事/03-定義市場與投資組合風險.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\03、定義市場與投資組合風險.md"
    },
    {
        "id": "inv_04",
        "book": "投資前最重要的事",
        "keywords": ["investing_market_myths", "04、市場迷思與市場歷史", "市場迷思與市場歷史"],
        "primary": "04、市場迷思與市場歷史",
        "aliases": [
            "市場迷思與市場歷史",
            "投資前最重要的事-04、市場迷思與市場歷史",
            "04-市場迷思與市場歷史"
        ],
        "book_md": "src/content/books/投資前最重要的事/04-市場迷思與市場歷史.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\04、市場迷思與市場歷史.md"
    },
    {
        "id": "inv_05",
        "book": "投資前最重要的事",
        "keywords": ["investing_philosophy", "05、找出你自己的投資哲學", "找出你自己的投資哲學"],
        "primary": "05、找出你自己的投資哲學",
        "aliases": [
            "找出你自己的投資哲學",
            "投資前最重要的事-05、找出你自己的投資哲學",
            "05-找出你自己的投資哲學"
        ],
        "book_md": "src/content/books/投資前最重要的事/05-找出你自己的投資哲學.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\05、找出你自己的投資哲學.md"
    },
    {
        "id": "inv_06",
        "book": "投資前最重要的事",
        "keywords": ["investing_wall_street", "06、華爾街的行為", "華爾街的行為"],
        "primary": "06、華爾街的行為",
        "aliases": [
            "華爾街的行為",
            "投資前最重要的事-06、華爾街的行為",
            "06-華爾街的行為"
        ],
        "book_md": "src/content/books/投資前最重要的事/06-華爾街的行為.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\06、華爾街的行為.md"
    },
    {
        "id": "inv_07",
        "book": "投資前最重要的事",
        "keywords": ["investing_asset_allocation", "07、資產配置", "資產配置"],
        "primary": "07、資產配置",
        "aliases": [
            "資產配置",
            "投資前最重要的事-07、資產配置",
            "07-資產配置"
        ],
        "book_md": "src/content/books/投資前最重要的事/07-資產配置.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\07、資產配置.md"
    },
    {
        "id": "inv_08",
        "book": "投資前最重要的事",
        "keywords": ["investing_plan", "08、完整的綜合投資計畫", "完整的綜合投資計畫"],
        "primary": "08、完整的綜合投資計畫",
        "aliases": [
            "完整的綜合投資計畫",
            "投資前最重要的事-08、完整的綜合投資計畫",
            "08-完整的綜合投資計畫"
        ],
        "book_md": "src/content/books/投資前最重要的事/08-完整的綜合投資計畫.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\08、完整的綜合投資計畫.md"
    },
    {
        "id": "inv_09",
        "book": "投資前最重要的事",
        "keywords": ["investing_advisors", "09、理財專業人士", "理財專業人士"],
        "primary": "09、理財專業人士",
        "aliases": [
            "理財專業人士",
            "投資前最重要的事-09、理財專業人士",
            "09-理財專業人士"
        ],
        "book_md": "src/content/books/投資前最重要的事/09-理財專業人士.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\09、理財專業人士.md"
    },
    {
        "id": "inv_10",
        "book": "投資前最重要的事",
        "keywords": ["investing_ten_concepts", "10、結語：十個投資概念與建議書單", "十個投資概念與建議書單", "10-結語十個投資概念與建議書單"],
        "primary": "10、結語：十個投資概念與建議書單",
        "aliases": [
            "結語：十個投資概念與建議書單",
            "10、結語十個投資概念與建議書單",
            "結語十個投資概念與建議書單",
            "投資前最重要的事-10、結語：十個投資概念與建議書單",
            "10-結語十個投資概念與建議書單"
        ],
        "book_md": "src/content/books/投資前最重要的事/10-結語十個投資概念與建議書單.md",
        "obsidian_md": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\投資前最重要的事\10、結語：十個投資概念與建議書單.md"
    }
]

def find_latest_image_for_item(item, search_dirs):
    candidates = []
    for d in search_dirs:
        if not os.path.exists(d):
            continue
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    lower = f.lower()
                    for kw in item['keywords']:
                        if kw.lower() in lower:
                            full_path = os.path.join(root, f)
                            candidates.append((os.path.getmtime(full_path), full_path))
                            break
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]

def process_item(item, img_path):
    primary = item["primary"]
    cover_webp = f"{primary}.webp"
    cover_png = f"{primary}.png"

    print(f"\n📦 處理: [{item['book']}] {primary} <- {os.path.basename(img_path)}")

    img = Image.open(img_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    w, h = img.size
    current_ratio = w / h

    # 16:9 裁剪與縮放到 1400x781
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

    # 2. public/images WebP
    pub_webp_path = os.path.join(public_images_dir, cover_webp)
    final_img.save(pub_webp_path, format="WEBP", quality=92)
    print(f"  ✅ Public WebP: {cover_webp}")
    for alias in item["aliases"]:
        shutil.copyfile(pub_webp_path, os.path.join(public_images_dir, f"{alias}.webp"))

    # 3. public/og-images WebP
    og_webp_path = os.path.join(public_og_images_dir, cover_webp)
    final_img.save(og_webp_path, format="WEBP", quality=92)
    print(f"  ✅ OG WebP: {cover_webp}")
    for alias in item["aliases"]:
        shutil.copyfile(og_webp_path, os.path.join(public_og_images_dir, f"{alias}.webp"))

    # 4. src/assets/images WebP
    assets_webp_path = os.path.join(assets_images_dir, cover_webp)
    final_img.save(assets_webp_path, format="WEBP", quality=92)
    print(f"  ✅ Assets WebP: {cover_webp}")
    for alias in item["aliases"]:
        shutil.copyfile(assets_webp_path, os.path.join(assets_images_dir, f"{alias}.webp"))

    # 5. 更新網站 Markdown frontmatter
    book_md_path = os.path.join(project_root, item["book_md"])
    if os.path.exists(book_md_path):
        with open(book_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                fm_clean = parts[1].strip()
                if 'coverImage:' in fm_clean:
                    fm_clean = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{cover_webp}"', fm_clean, flags=re.MULTILINE)
                else:
                    fm_clean = fm_clean + f'\ncoverImage: "{cover_webp}"'
                new_content = f"---\n{fm_clean}\n---{parts[2]}"
        else:
            new_content = f'---\ntitle: "{primary}"\ncoverImage: "{cover_webp}"\n---\n{content}'
        with open(book_md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ 更新網站筆記 frontmatter: {item['book_md']}")
    else:
        print(f"  ⚠️ 網站筆記不存在: {book_md_path}")

    # 6. 更新 Obsidian 來源筆記 frontmatter
    obs_path = item["obsidian_md"]
    if os.path.exists(obs_path):
        with open(obs_path, 'r', encoding='utf-8') as f:
            obs_content = f.read()
        if obs_content.startswith('---'):
            parts = obs_content.split('---', 2)
            if len(parts) >= 3:
                obs_fm_clean = parts[1].strip()
                if 'coverImage:' in obs_fm_clean:
                    obs_fm_clean = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{cover_webp}"', obs_fm_clean, flags=re.MULTILINE)
                else:
                    obs_fm_clean = obs_fm_clean + f'\ncoverImage: "{cover_webp}"'
                new_obs_content = f"---\n{obs_fm_clean}\n---{parts[2]}"
        else:
            new_obs_content = f'---\ntitle: "{primary}"\ncoverImage: "{cover_webp}"\n---\n{obs_content}'
        with open(obs_path, 'w', encoding='utf-8') as f:
            f.write(new_obs_content)
        print(f"  ✅ 更新 Obsidian 筆記 frontmatter: {os.path.basename(obs_path)}")
    else:
        print(f"  ⚠️ Obsidian 筆記不存在: {obs_path}")

if __name__ == "__main__":
    brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain"
    search_dirs = [inbox_dir, brain_dir]
    
    found_count = 0
    missing_items = []
    
    for item in items:
        found = find_latest_image_for_item(item, search_dirs)
        if found:
            process_item(item, found)
            found_count += 1
        else:
            missing_items.append(f"[{item['book']}] {item['primary']}")
            
    print(f"\n==========================================")
    print(f"✨ 處理完成統計: 已成功對齊部署 {found_count} / {len(items)} 張")
    if missing_items:
        print(f"⏳ 尚缺圖片 ({len(missing_items)} 張):")
        for m in missing_items:
            print(f"   - {m}")
