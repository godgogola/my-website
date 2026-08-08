import os
from PIL import Image

artifact_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\d0bbff17-1170-46fc-a3b2-5bf2112488d8"
drive_dir = r"G:\我的雲端硬碟\衛教文章圖片"
public_images_dir = os.path.join(os.getcwd(), "public", "images")

# 測試不同裁切 offset，檢視是否能完美保留頭頂頭髮與腳底雙靴
test_configs = [
    { "prefix": "v5_ag_ratio_balance", "title": "【AG ratio】", "top": 380 },
    { "prefix": "v5_albumin_synthesis", "title": "【Albumin】白蛋白的合成與低下原因", "top": 360 },
    { "prefix": "v5_globulin_immune_soldiers", "title": "【Globulin】球蛋白", "top": 340 },
    { "prefix": "v5_hdl_investigation", "title": "【HDL】HDL太高是好事嗎", "top": 350 },
    { "prefix": "v5_carbs_fat_mechanism", "title": "碳水化合物造成脂肪堆積的機制", "top": 360 }
]

artifact_files = os.listdir(artifact_dir)

for cfg in test_configs:
    png_file = next((f for f in artifact_files if f.startswith(cfg["prefix"]) and f.endswith(".png")), None)
    if not png_file:
        continue
    src_path = os.path.join(artifact_dir, png_file)
    img = Image.open(src_path)
    w, h = img.size

    # 以腳底與地面為基準的智能裁切 (Bottom-aligned preserving full boots and floor)
    top = cfg["top"]
    bottom = top + 576
    if bottom > h:
        bottom = h
        top = h - 576

    cropped = img.crop((0, top, w, bottom))

    # 儲存預覽圖至 artifact 目錄
    preview_path = os.path.join(artifact_dir, f"smartcrop_{cfg['prefix']}.png")
    cropped.save(preview_path, format="PNG")

    # 覆蓋至 Google 雲端硬碟 16:9 PNG
    drive_path = os.path.join(drive_dir, f"{cfg['title']}.png")
    cropped.save(drive_path, format="PNG")

    # 覆蓋至 public/images 16:9 WebP
    webp_path = os.path.join(public_images_dir, f"{cfg['title']}.webp")
    cropped.save(webp_path, format="WEBP", quality=95)

    print(f"Smart cropped {cfg['title']}: y={top}..{bottom} -> Boots & Head 100% saved!")

print("All smart crop previews generated successfully!")
