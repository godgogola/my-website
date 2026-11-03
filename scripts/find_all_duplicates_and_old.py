import re
import os

with open('src/data/videos.ts', encoding='utf-8') as f:
    text = f.read()

# match all objects
matches = list(re.finditer(r'\{\s*id:\s*\'([^\']+)\'[\s\S]*?\n\s*\}', text))
print(f"Total video items: {len(matches)}")

imgs = set(os.listdir('public/images'))

items = []
for m in matches:
    block = m.group(0)
    vid = m.group(1)
    title_m = re.search(r"title:\s*'([^']+)'", block)
    thumb_m = re.search(r"thumbnail:\s*'([^']+)'", block)
    slug_m = re.search(r"articleSlug:\s*'([^']+)'", block)
    cat_m = re.search(r"category:\s*'([^']+)'", block)
    title = title_m.group(1) if title_m else ''
    thumb = thumb_m.group(1) if thumb_m else ''
    slug = slug_m.group(1) if slug_m else ''
    cat = cat_m.group(1) if cat_m else ''
    items.append({
        'id': vid,
        'title': title,
        'thumb': thumb,
        'slug': slug,
        'cat': cat,
        'has_thumb_file': os.path.basename(thumb) in imgs if thumb else False
    })

# Check duplicate slugs or duplicate core keywords
print("\n=== Group by Article Slug to find duplicates ===")
from collections import defaultdict
by_slug = defaultdict(list)
for it in items:
    if it['slug']:
        by_slug[it['slug']].append(it)

for slug, group in by_slug.items():
    if len(group) > 1:
        print(f"\nDuplicate Slug: {slug}")
        for g in group:
            print(f"  ID: {g['id']} | Thumb: {g['thumb']} | Title: {g['title']}")

print("\n=== Videos WITHOUT thumbnail or where thumbnail is missing ===")
no_thumb = [it for it in items if not it['thumb']]
print(f"Total videos without thumbnail field: {len(no_thumb)}")
for it in no_thumb:
    print(f"  ID: {it['id']} | Slug: {it['slug']} | Title: {it['title']}")
