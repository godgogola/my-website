import os
from PIL import Image

src_path = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\d0bbff17-1170-46fc-a3b2-5bf2112488d8\v4_cystatin_c_1786163895472.png"
artifact_out = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\d0bbff17-1170-46fc-a3b2-5bf2112488d8\crop169_v4_cystatin_c.png"
drive_out = r"G:\我的雲端硬碟\衛教文章圖片\【Cystatin C】血清胱蛋白 C.png"
public_out = os.path.join(os.getcwd(), "public", "images", "【Cystatin C】血清胱蛋白 C.webp")

img = Image.open(src_path)
w, h = img.size
target_ratio = 16.0 / 9.0
new_h = int(w / target_ratio)
left = 0
top = (h - new_h) // 2
right = w
bottom = top + new_h

cropped = img.crop((left, top, right, bottom))
cropped.save(artifact_out, format="PNG")
cropped.save(drive_out, format="PNG")
cropped.save(public_out, format="WEBP", quality=95)
print(f"Cropped Cystatin C: {cropped.size} saved to all targets successfully!")
