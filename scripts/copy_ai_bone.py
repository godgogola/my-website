import shutil, os

for folder in ['public/images', 'public/og-images']:
    src = os.path.join(folder, 'AI骨密檢查-骨質疏鬆症.webp')
    dst = os.path.join(folder, 'AI骨密檢查.webp')
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {src} -> {dst}")

