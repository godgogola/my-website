import os
import sys
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\60f43c62-0a3f-4d4a-aaa0-9ee8afe03e4a"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")
og_images_dir = os.path.join(os.getcwd(), "public", "og-images")
posts_dir = os.path.join(os.getcwd(), "src", "content", "posts")
vault_dir = r"G:\我的雲端硬碟\Wix衛教文章\Wix衛教文章庫"

os.makedirs(public_images_dir, exist_ok=True)
os.makedirs(og_images_dir, exist_ok=True)

targets = [
    {
        "src_file": "glp1_dual_triple_1791881053113.jpg",
        "title": "【GLP-1】 新藥、二合一與三合一受體促效劑",
        "aliases": ["【GLP-1】新藥、二合一與三合一受體促效劑"],
        "post_file": "glp-1-新藥二合一與三合一受體促效劑.md",
        "vault_file": os.path.join(vault_dir, "藥物介紹", "【GLP-1】 新藥、二合一與三合一受體促效劑.md")
    },
    {
        "src_file": "cancer_registry_report_1791881105808.jpg",
        "title": "112年臺灣癌症登記報告",
        "aliases": [],
        "post_file": "112年臺灣癌症登記報告.md",
        "vault_file": os.path.join(vault_dir, "消化道癌症專區", "112年臺灣癌症登記報告.md")
    }
]

print("=== 開始依最高規格 SOP 處理 2 張全新封面圖 ===")

for idx, item in enumerate(targets):
    src_path = os.path.join(brain_dir, item["src_file"])
    if not os.path.exists(src_path):
        print(f"❌ 找不到來源圖: {src_path}")
        continue

    img = Image.open(src_path)
    w, h = img.size
    print(f"\n[{idx+1}/2] 處理: {item['title']} (原始尺寸: {w}x{h})")

    # 16:9 裁剪 / 調整
    target_ratio = 16.0 / 9.0
    current_ratio = w / h
    if abs(current_ratio - target_ratio) > 0.02:
        new_h = int(w / target_ratio)
        if new_h <= h:
            top = (h - new_h) // 2
            cropped = img.crop((0, top, w, top + new_h))
        else:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            cropped = img.crop((left, 0, left + new_w, h))
    else:
        cropped = img

    final_img = cropped.resize((1400, 781), Image.Resampling.LANCZOS)

    # 1. 備份 PNG 至 Google Drive
    if os.path.exists(drive_dir):
        drive_png_path = os.path.join(drive_dir, f"{item['title']}.png")
        final_img.save(drive_png_path, format="PNG")
        print(f"  💾 Google Drive PNG 備份成功: {item['title']}.png")
        for alias in item["aliases"]:
            alias_png = os.path.join(drive_dir, f"{alias}.png")
            final_img.save(alias_png, format="PNG")
    else:
        print(f"  ⚠️ Google Drive 目錄未掛載")

    # 2. 轉檔 WebP 存入 public/images 與 public/og-images
    webp_name = f"{item['title']}.webp"
    pub_webp = os.path.join(public_images_dir, webp_name)
    og_webp = os.path.join(og_images_dir, webp_name)
    final_img.save(pub_webp, format="WEBP", quality=92)
    final_img.save(og_webp, format="WEBP", quality=92)
    print(f"  🌐 WebP 發布成功: {webp_name}")

    for alias in item["aliases"]:
        alias_webp = f"{alias}.webp"
        final_img.save(os.path.join(public_images_dir, alias_webp), format="WEBP", quality=92)
        final_img.save(os.path.join(og_images_dir, alias_webp), format="WEBP", quality=92)
        print(f"  🌐 別名 WebP 發布: {alias_webp}")

    # 3. 更新 Markdown coverImage
    md_path = os.path.join(posts_dir, item["post_file"])
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'coverImage:' in content:
            content = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{webp_name}"', content, flags=re.MULTILINE)
        else:
            content = re.sub(r'(^title:.*$)', f'\\1\ncoverImage: "{webp_name}"', content, flags=re.MULTILINE)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  📝 網站 Markdown 綁定完成: {item['post_file']}")

    # 4. 更新 Obsidian Vault 檔案中的 coverImage (若存在)
    if os.path.exists(item["vault_file"]):
        with open(item["vault_file"], 'r', encoding='utf-8') as f:
            v_content = f.read()
        if 'coverImage:' in v_content:
            v_content = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{webp_name}"', v_content, flags=re.MULTILINE)
        else:
            v_content = re.sub(r'(^title:.*$)', f'\\1\ncoverImage: "{webp_name}"', v_content, flags=re.MULTILINE)
        with open(item["vault_file"], 'w', encoding='utf-8') as f:
            f.write(v_content)
        print(f"  📝 Obsidian Vault 綁定完成: {os.path.basename(item['vault_file'])}")

print("\n🎉 圖片轉檔、Drive 備份與 Markdown 綁定全部完成！")
