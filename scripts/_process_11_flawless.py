import os
import sys
import re
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\b15a01ac-3ff4-4121-b08c-539ce5f229d5"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")
posts_dir = os.path.join(os.getcwd(), "src", "content", "posts")

targets = [
    { "prefix": "cover_ag_ratio", "title": "【AG ratio】", "file": "ag-ratio.md" },
    { "prefix": "cover_albumin", "title": "【Albumin】白蛋白的合成與低下原因", "file": "albumin白蛋白的合成與低下原因.md" },
    { "prefix": "cover_cystatin_c", "title": "【Cystatin C】血清胱蛋白 C", "file": "cystatin-c血清胱蛋白-c.md" },
    { "prefix": "cover_bilirubin", "title": "【膽紅素】單純膽紅素偏高", "file": "膽紅素單純膽紅素偏高.md" },
    { "prefix": "cover_globulin", "title": "【Globulin】球蛋白", "file": "globulin球蛋白.md" },
    { "prefix": "cover_hdl", "title": "【HDL】HDL太高是好事嗎", "file": "hdlhdl太高是好事嗎.md" },
    { "prefix": "cover_carbs_fat", "title": "碳水化合物造成脂肪堆積的機制", "file": "碳水化合物造成脂肪堆積的機制.md" },
    { "prefix": "cover_s_abcde", "title": "S-ABCDE 高血壓生活型態調整", "file": "s-abcde-高血壓生活型態調整.md" },
    { "prefix": "cover_gastroparesis_diag", "title": "【胃輕癱】胃輕癱臨床診斷標準", "file": "胃輕癱胃輕癱臨床診斷標準.md" },
    { "prefix": "cover_gastroparesis_vs_dyspepsia", "title": "【胃輕癱】胃輕癱與消化不良有何不同", "file": "胃輕癱胃輕癱與消化不良有何不同.md" },
    { "prefix": "cover_gastroparesis_diet", "title": "【胃輕癱】胃輕癱飲食調整與治療", "file": "胃輕癱胃輕癱飲食調整與治療.md" }
]

brain_files = os.listdir(brain_dir)
print(f"=== 開始處理 11 張最新生成的滿分 16:9 封面圖 ===")

success_count = 0

for idx, item in enumerate(targets):
    # Find matching file in brain directory
    matching_files = [f for f in brain_files if f.startswith(item["prefix"]) and f.endswith(".png")]
    if not matching_files:
        print(f"❌ [{idx+1}] 找不到前綴為 {item['prefix']} 的原圖")
        continue

    # Pick the latest matching file
    matching_files.sort(key=lambda f: os.path.getmtime(os.path.join(brain_dir, f)), reverse=True)
    latest_file = matching_files[0]
    src_path = os.path.join(brain_dir, latest_file)

    img = Image.open(src_path)
    w, h = img.size

    # Check / Crop to exact 16:9
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

    # Resize to standard high-res 1400x781
    final_img = cropped.resize((1400, 781), Image.Resampling.LANCZOS)

    # 1. 備份 16:9 PNG 至 Google Drive (G:\我的雲端硬碟\衛教文章圖片)
    if os.path.exists(drive_dir):
        drive_png_path = os.path.join(drive_dir, f"{item['title']}.png")
        final_img.save(drive_png_path, format="PNG")
        print(f"   💾 Drive PNG 備份成功: {item['title']}.png")
    else:
        print(f"   ⚠️ Drive 目錄未掛載，跳過 Drive 儲存: {drive_dir}")

    # 2. 轉檔為高畫質 WebP 存入 public/images/<Title>.webp
    webp_name = f"{item['title']}.webp"
    public_webp_path = os.path.join(public_images_dir, webp_name)
    final_img.save(public_webp_path, format="WEBP", quality=92)
    print(f"   🌐 WebP 發布成功: {webp_name}")

    # 3. 更新對應 Markdown 檔案中的 coverImage 欄位
    md_path = os.path.join(posts_dir, item["file"])
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'coverImage:' in content:
            content = re.sub(r'^coverImage:\s*["\']?.+?["\']?\s*$', f'coverImage: "{webp_name}"', content, flags=re.MULTILINE)
        else:
            content = re.sub(r'(^title:.*$)', f'\\1\ncoverImage: "{webp_name}"', content, flags=re.MULTILINE)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📝 Markdown 綁定完成: {item['file']}")

    success_count += 1
    print(f"✅ [{idx+1}/11] 完成: {item['title']}\n")

print(f"🎉 全部 11 張封面圖均已順利依 SOP (16:9 / PNG備份 / WebP發布 / MD綁定) 完成！共成功 {success_count} 篇！")
