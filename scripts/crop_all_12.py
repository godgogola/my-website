import os
import glob
from PIL import Image

artifact_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\d0bbff17-1170-46fc-a3b2-5bf2112488d8"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")

items = [
    { "prefix": "hba1c_fasting_high_normal", "title": "【糖化血色素】空腹血糖高但是糖化血色素正常是什麼原因" },
    { "prefix": "hba1c_fasting_normal_hba1c_high", "title": "【糖化血色素】空腹血糖正常但是糖化血色素高是什麼原因" },
    { "prefix": "hba1c_non_dietary_factors", "title": "【糖化血色素】糖化血色素升高的原因_非飲食因素" },
    { "prefix": "proteinuria_mild_care", "title": "【尿蛋白】輕微尿蛋白怎麼辦" },
    { "prefix": "hematuria_mild_care", "title": "【尿潛血】輕微尿潛血怎麼辦" },
    { "prefix": "anemia_microcytic_macrocytic", "title": "【貧血】小球性與大球性貧血" },
    { "prefix": "stomach_cancer_risk_factors", "title": "【胃癌】胃癌的危險因子" },
    { "prefix": "sarcopenia_kidney_function_misjudgment", "title": "【腎功能】高齡肌少症與腎功能誤判" },
    { "prefix": "ckd_stages_kidney_protection", "title": "【慢性腎臟病】慢性腎臟病各分期保腎措施" },
    { "prefix": "bilirubin_isolated_high", "title": "【膽紅素】單純膽紅素偏高" },
    { "prefix": "hypertension_complications", "title": "長期血壓控制不良的併發症" },
    { "prefix": "s_abcde_hypertension_lifestyle", "title": "S-ABCDE 高血壓生活型態調整" }
]

artifact_files = os.listdir(artifact_dir)

for idx, item in enumerate(items):
    png_file = next((f for f in artifact_files if f.startswith(item["prefix"]) and f.endswith(".png")), None)
    if not png_file:
        print(f"Skipping {item['title']}: original png not found")
        continue

    src_path = os.path.join(artifact_dir, png_file)
    img = Image.open(src_path)
    w, h = img.size
    
    # 16:9 crop calculation
    target_ratio = 16.0 / 9.0
    new_h = int(w / target_ratio)
    left = 0
    top = (h - new_h) // 2
    right = w
    bottom = top + new_h

    cropped = img.crop((left, top, right, bottom))

    # Save to Drive as 16:9 PNG
    drive_png_path = os.path.join(drive_dir, f"{item['title']}.png")
    cropped.save(drive_png_path, format="PNG")

    # Save to public/images as 16:9 WebP
    public_webp_path = os.path.join(public_images_dir, f"{item['title']}.webp")
    cropped.save(public_webp_path, format="WEBP", quality=95)

    # Save 16:9 PNG copy in artifact dir for display
    artifact_crop_path = os.path.join(artifact_dir, f"crop169_{item['prefix']}.png")
    cropped.save(artifact_crop_path, format="PNG")

    print(f"[{idx+1}] {item['title']} -> 16:9 cropped ({cropped.width}x{cropped.height}) saved to Drive PNG & public WebP")
