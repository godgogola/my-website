import os
import re

with open('src/data/videos.ts', encoding='utf-8') as f:
    text = f.read()

imgs = set(os.listdir('public/images'))

# Find all blocks { id: '...', ... }
blocks = re.findall(r'(\{\s*id:\s*\'[^\']+\'[\s\S]*?\n\s*\})', text)
print(f"Total video blocks: {len(blocks)}")

missing_count = 0
for b in blocks:
    id_m = re.search(r"id:\s*'([^']+)'", b)
    thumb_m = re.search(r"thumbnail:\s*'([^']+)'", b)
    title_m = re.search(r"title:\s*'([^']+)'", b)
    vid = id_m.group(1) if id_m else ''
    title = title_m.group(1) if title_m else ''
    if thumb_m:
        thumb = thumb_m.group(1)
        fn = os.path.basename(thumb)
        if fn not in imgs:
            missing_count += 1
            print(f"MISSING: {vid} | {fn} | {title}")
    else:
        # Check if it doesn't have thumbnail
        pass

print(f"Total missing in current file: {missing_count}")

