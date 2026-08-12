import os
from PIL import Image

brain_dir = r"C:\Users\X1 Yoga Gen7\.gemini\antigravity-ide\brain\f6782200-767d-43c0-9c0c-b4ccca9153df"
for f in os.listdir(brain_dir):
    if f.endswith('.png'):
        p = os.path.join(brain_dir, f)
        img = Image.open(p)
        print(f"{f}: {img.size}, aspect ratio: {img.size[0]/img.size[1]:.4f}")

print("\nSample existing webp in public/images:")
pub_dir = r"public\images"
count = 0
for f in os.listdir(pub_dir):
    if f.endswith('.webp'):
        p = os.path.join(pub_dir, f)
        img = Image.open(p)
        print(f"{f}: {img.size}, ratio: {img.size[0]/img.size[1]:.4f}")
        count += 1
        if count >= 5:
            break
