import os
import re
from PIL import Image

artifact_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\d0bbff17-1170-46fc-a3b2-5bf2112488d8"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")
posts_dir = os.path.join(os.getcwd(), "src", "content", "posts")

items = [
    { "prefix": "v2_hba1c_fasting_high_normal", "title": "【糖化血色素】空腹血糖高但是糖化血色素正常是什麼原因", "file": "糖化血色素空腹血糖高但是糖化血色素正常是什麼原因.md" },
    { "prefix": "v2_hba1c_fasting_normal_hba1c_high", "title": "【糖化血色素】空腹血糖正常但是糖化血色素高是什麼原因", "file": "糖化血色素空腹血糖正常但是糖化血色素高是什麼原因.md" },
    { "prefix": "v2_hba1c_non_dietary_factors", "title": "【糖化血色素】糖化血色素升高的原因_非飲食因素", "file": "糖化血色素糖化血色素升高的原因_非飲食因素.md" },
    { "prefix": "v2_proteinuria_mild_care", "title": "【尿蛋白】輕微尿蛋白怎麼辦", "file": "尿蛋白輕微尿蛋白怎麼辦.md" },
    { "prefix": "v2_hematuria_mild_care", "title": "【尿潛血】輕微尿潛血怎麼辦", "file": "尿潛血輕微尿潛血怎麼辦.md" },
    { "prefix": "v2_anemia_microcytic_macrocytic", "title": "【貧血】小球性與大球性貧血", "file": "貧血小球性與大球性貧血.md" },
    { "prefix": "v2_stomach_cancer_risk_factors", "title": "【胃癌】胃癌的危險因子", "file": "胃癌胃癌的危險因子.md" },
    { "prefix": "v2_sarcopenia_kidney_function_misjudgment", "title": "【腎功能】高齡肌少症與腎功能誤判", "file": "腎功能高齡肌少症與腎功能誤判.md" },
    { "prefix": "v2_ckd_stages_kidney_protection", "title": "【慢性腎臟病】慢性腎臟病各分期保腎措施", "file": "慢性腎臟病慢性腎臟病各分期保腎措施.md" },
    { "prefix": "v3_bilirubin_isolated_high", "title": "【膽紅素】單純膽紅素偏高", "file": "膽紅素單純膽紅素偏高.md" },
    { "prefix": "v2_hypertension_complications", "title": "長期血壓控制不良的併發症", "file": "長期血壓控制不良的併發症.md" },
    { "prefix": "v3_s_abcde_hypertension_lifestyle", "title": "S-ABCDE 高血壓生活型態調整", "file": "s-abcde-高血壓生活型態調整.md" },
    { "prefix": "v2_alt_ast_elevated_liver_enzymes", "title": "【ALT AST】肝功能上升", "file": "alt-ast肝功能上升.md" },
    { "prefix": "v2_albumin_synthesis_hypoalbuminemia", "title": "【Albumin】白蛋白的合成與低下原因", "file": "albumin白蛋白的合成與低下原因.md" },
    { "prefix": "v2_globulin_immune_soldiers", "title": "【Globulin】球蛋白", "file": "globulin球蛋白.md" },
    { "prefix": "v2_ag_ratio_balance", "title": "【AG ratio】", "file": "ag-ratio.md" },
    { "prefix": "v2_cystatin_c_kidney_function", "title": "【Cystatin C】血清胱蛋白 C", "file": "cystatin-c血清胱蛋白-c.md" },
    { "prefix": "v2_hdl_extremely_high_investigation", "title": "【HDL】HDL太高是好事嗎", "file": "hdlhdl太高是好事嗎.md" },
    { "prefix": "v2_gastroparesis_diet_treatment", "title": "【胃輕癱】胃輕癱飲食調整與治療", "file": "胃輕癱胃輕癱飲食調整與治療.md" },
    { "prefix": "v2_gastroparesis_diagnostic_criteria", "title": "【胃輕癱】胃輕癱臨床診斷標準", "file": "胃輕癱胃輕癱臨床診斷標準.md" },
    { "prefix": "v2_gastroparesis_vs_dyspepsia", "title": "【胃輕癱】胃輕癱與消化不良有何不同", "file": "胃輕癱胃輕癱與消化不良有何不同.md" },
    { "prefix": "v2_carbs_fat_accumulation_mechanism", "title": "碳水化合物造成脂肪堆積的機制", "file": "碳水化合物造成脂肪堆積的機制.md" },
    { "prefix": "v2_masld_reversal_exercise", "title": "【代謝異常脂肪肝】逆轉代謝異常脂肪肝", "file": "代謝異常脂肪肝逆轉代謝異常脂肪肝.md" }
]

artifact_files = os.listdir(artifact_dir)

print(f"=== 開始批次處理全數 23 篇 16:9 中心裁切與轉檔 SOP ===")

for idx, item in enumerate(items):
    png_file = next((f for f in artifact_files if f.startswith(item["prefix"]) and f.endswith(".png")), None)
    if not png_file:
        print(f"❌ [{idx+1}] 跳過 {item['title']}: 找不到前綴為 {item['prefix']} 的原圖")
        continue

    src_path = os.path.join(artifact_dir, png_file)
    img = Image.open(src_path)
    w, h = img.size
    
    # 16:9 center crop calculation
    target_ratio = 16.0 / 9.0
    new_h = int(w / target_ratio)
    left = 0
    top = (h - new_h) // 2
    right = w
    bottom = top + new_h

    cropped = img.crop((left, top, right, bottom))

    # 1. 儲存 16:9 PNG 至 Google 雲端硬碟
    drive_png_path = os.path.join(drive_dir, f"{item['title']}.png")
    cropped.save(drive_png_path, format="PNG")

    # 2. 儲存 16:9 WebP 至 public/images/
    webp_name = f"{item['title']}.webp"
    public_webp_path = os.path.join(public_images_dir, webp_name)
    cropped.save(public_webp_path, format="WEBP", quality=95)

    # 3. 儲存 16:9 PNG 副本至 artifact 目錄 (用於展示)
    artifact_crop_path = os.path.join(artifact_dir, f"crop169_{item['prefix']}.png")
    cropped.save(artifact_crop_path, format="PNG")

    # 4. 更新 Markdown frontmatter coverImage 欄位
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

    print(f"[{idx+1}/23] {item['file']} -> 16:9 ({cropped.width}x{cropped.height}) -> Drive PNG & public WebP OK")

print("\n=== ALL 23 POSTS PROCESSED SUCCESSFULLY! ===")
