import os
import shutil
from PIL import Image

BRAIN_DIR = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\416ad738-0631-47a6-863e-9aa060628a0c"
GDRIVE_IMG_DIR = r"G:\我的雲端硬碟\衛教文章圖片"
PUBLIC_IMG_DIR = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\public\images"
PUBLIC_OG_DIR = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\public\og-images"

os.makedirs(GDRIVE_IMG_DIR, exist_ok=True)
os.makedirs(PUBLIC_IMG_DIR, exist_ok=True)
os.makedirs(PUBLIC_OG_DIR, exist_ok=True)

ITEMS = [
    {
        "src": "hpylori_second_line_treatment_1792322657954.jpg",
        "primary_name": "【幽門桿菌】【實證】幽門螺旋桿菌 (H. pylori) 第二線治療處方",
        "aliases": ["幽門螺旋桿菌 (H. pylori) 第二線治療處方"],
        "md_path": r"G:\我的雲端硬碟\衛教文章庫\衛教文章庫\胃部疾病\【幽門桿菌】【實證】幽門螺旋桿菌 (H. pylori) 第二線治療處方.md",
        "title": "【幽門桿菌】【實證】幽門螺旋桿菌 (H. pylori) 第二線治療處方"
    },
    {
        "src": "polyps_polypectomy_guide_1792322676904.jpg",
        "primary_name": "【息肉】【實證】胃鏡與大腸鏡息肉切除術全指南",
        "aliases": ["胃鏡與大腸鏡息肉切除術全指南"],
        "md_path": r"G:\我的雲端硬碟\衛教文章庫\衛教文章庫\內視鏡檢查\【息肉】【實證】胃鏡與大腸鏡息肉切除術全指南.md",
        "title": "【息肉】【實證】胃鏡與大腸鏡息肉切除術全指南"
    },
    {
        "src": "neurotransmitters_intro_1792322698254.jpg",
        "primary_name": "01、六大神經傳導物質簡介",
        "aliases": ["六大神經傳導物質簡介", "【大腦的天使特調】六大神經傳導物質簡介"],
        "md_path": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了!\01、六大神經傳導物質簡介.md",
        "title": "01、六大神經傳導物質簡介"
    },
    {
        "src": "dopamine_motivation_engine_1792322846520.jpg",
        "primary_name": "02、多巴胺_動機與渴望的動力引擎",
        "aliases": ["多巴胺_動機與渴望的動力引擎", "【大腦的天使特調】多巴胺_動機與渴望的動力引擎"],
        "md_path": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了!\02、多巴胺_動機與渴望的動力引擎.md",
        "title": "02、多巴胺_動機與渴望的動力引擎"
    },
    {
        "src": "endorphins_painkiller_euphoria_1792322763134.jpg",
        "primary_name": "03、腦內啡_天然止痛劑與極致愉悅感",
        "aliases": ["腦內啡_天然止痛劑與極致愉悅感", "【大腦的天使特調】腦內啡_天然止痛劑與極致愉悅感"],
        "md_path": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了!\03、腦內啡_天然止痛劑與極致愉悅感.md",
        "title": "03、腦內啡_天然止痛劑與極致愉悅感"
    },
    {
        "src": "oxytocin_trust_belonging_1792322827487.jpg",
        "primary_name": "04、催產素_信任與歸屬感的愛的荷爾蒙",
        "aliases": ["催產素_信任與歸屬感的愛的荷爾蒙", "【大腦的天使特調】催產素_信任與歸屬感的愛的荷爾蒙"],
        "md_path": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了!\04、催產素_信任與歸屬感的愛的荷爾蒙.md",
        "title": "04、催產素_信任與歸屬感的愛的荷爾蒙"
    },
    {
        "src": "serotonin_satisfaction_stability_1792322807537.jpg",
        "primary_name": "05、血清素_滿足感與穩定情緒的基石",
        "aliases": ["血清素_滿足感與穩定情緒的基石", "【大腦的天使特調】血清素_滿足感與穩定情緒的基石"],
        "md_path": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了!\05、血清素_滿足感與穩定情緒的基石.md",
        "title": "05、血清素_滿足感與穩定情緒的基石"
    },
    {
        "src": "cortisol_stress_double_edged_1792322788330.jpg",
        "primary_name": "06、皮質醇_應變挑戰與警覺的雙面刃",
        "aliases": ["皮質醇_應變挑戰與警覺的雙面刃", "【大腦的天使特調】皮質醇_應變挑戰與警覺的雙面刃"],
        "md_path": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了!\06、皮質醇_應變挑戰與警覺的雙面刃.md",
        "title": "06、皮質醇_應變挑戰與警覺的雙面刃"
    },
    {
        "src": "testosterone_confidence_amp_1792322743065.jpg",
        "primary_name": "07、睪固酮_自信心與行為傾向的增幅器",
        "aliases": ["睪固酮_自信心與行為傾向的增幅器", "【大腦的天使特調】睪固酮_自信心與行為傾向的增幅器"],
        "md_path": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了!\07、睪固酮_自信心與行為傾向的增幅器.md",
        "title": "07、睪固酮_自信心與行為傾向的增幅器"
    },
    {
        "src": "four_life_foundations_1792322719639.jpg",
        "primary_name": "08、四大生活基底",
        "aliases": ["四大生活基底", "【大腦的天使特調】四大生活基底"],
        "md_path": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\你的人生，他們六個說了!\08、四大生活基底.md",
        "title": "08、四大生活基底"
    },
    {
        "src": "sugar_biology_origin_1792322874621.jpg",
        "primary_name": "01、探索醣類的生物學源頭",
        "aliases": ["探索醣類的生物學源頭", "【90%的病，控糖就會好】探索醣類的生物學源頭"],
        "md_path": r"G:\我的雲端硬碟\讀書筆記庫\讀書筆記\90%的病，控糖就會好\01、探索醣類的生物學源頭.md",
        "title": "01、探索醣類的生物學源頭"
    }
]

for item in ITEMS:
    src_file = os.path.join(BRAIN_DIR, item["src"])
    if not os.path.exists(src_file):
        print(f"❌ 找不到來源圖片: {src_file}")
        continue

    img = Image.open(src_file)
    print(f"🖼️ 處理圖片: {item['primary_name']} (尺寸: {img.size})")

    all_names = [item["primary_name"]] + item.get("aliases", [])

    for name in all_names:
        # 1. 存入 GDrive PNG
        gdrive_png = os.path.join(GDRIVE_IMG_DIR, f"{name}.png")
        img.save(gdrive_png, "PNG")

        # 2. 存入 public/images/*.webp
        pub_webp = os.path.join(PUBLIC_IMG_DIR, f"{name}.webp")
        img.save(pub_webp, "WEBP", quality=95)

        # 3. 存入 public/og-images/*.webp
        og_webp = os.path.join(PUBLIC_OG_DIR, f"{name}.webp")
        img.save(og_webp, "WEBP", quality=95)

    print(f"  ✅ 已部署至 GDrive 與 public/images & public/og-images ({len(all_names)} 組檔名別名)")

    # 4. 更新 Markdown Frontmatter
    md_file = item["md_path"]
    if os.path.exists(md_file):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        primary_cover = f"{item['primary_name']}.webp"

        if content.startswith("---"):
            parts = content.split("---", 2)
            fm = parts[1]
            body = parts[2] if len(parts) >= 3 else ""

            # 更新或加入 coverImage
            lines = [l for l in fm.splitlines() if not l.startswith("coverImage:")]
            lines.append(f'coverImage: "{primary_cover}"')
            new_fm = "\n".join(lines).strip()
            new_content = f"---\n{new_fm}\n---" + body
        else:
            new_content = f'---\ntitle: "{item["title"]}"\ncoverImage: "{primary_cover}"\n---\n' + content

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  📝 已綁定 Markdown 封面圖: {os.path.basename(md_file)} ➜ {primary_cover}")
    else:
        print(f"  ⚠️ Markdown 檔案不存在: {md_file}")

print("\n🎉 全部 11 張封面圖已成功轉檔、備份並完成 Markdown 綁定！")
