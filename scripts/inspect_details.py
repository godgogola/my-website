import re

with open('src/data/videos.ts', encoding='utf-8') as f:
    text = f.read()

# match all objects
matches = re.finditer(r'(\{\s*id:\s*\'([^\']+)\'[\s\S]*?\n\s*\})', text)

print("=== All items in videos.ts ===")
for m in matches:
    block = m.group(1)
    vid = m.group(2)
    title_m = re.search(r"title:\s*'([^']+)'", block)
    thumb_m = re.search(r"thumbnail:\s*'([^']+)'", block)
    slug_m = re.search(r"articleSlug:\s*'([^']+)'", block)
    cat_m = re.search(r"category:\s*'([^']+)'", block)
    title = title_m.group(1) if title_m else ''
    thumb = thumb_m.group(1) if thumb_m else ''
    slug = slug_m.group(1) if slug_m else ''
    cat = cat_m.group(1) if cat_m else ''
    
    # Let's inspect anything related to ADA, 癌症, or duplicates
    if any(k in title for k in ['112年', '十大癌症', 'ADA', 'CKM', '減重途徑', '糖尿病及肥胖', '心腎代謝']):
        print(f"ID: {vid} | Cat: {cat}\n  Title: {title}\n  Thumb: {thumb}\n  Slug: {slug}\n")

