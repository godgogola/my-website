import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/cover-mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

borrowed = []
for item in mapping:
    title = item.get('title', '')
    cover = item.get('coverImage', '')
    # Check if cover name doesn't match title base
    cover_base = cover.replace('.webp', '').replace('.png', '').replace('.jpg', '')
    # If the cover base is significantly shorter or different
    if cover_base != title and cover_base not in title:
        borrowed.append((title, cover))

print(f"Total mappings: {len(mapping)}")
print(f"Articles borrowing generic/other covers: {len(borrowed)}")
for t, c in borrowed:
    print(f"  - [{t}] -> uses [{c}]")

