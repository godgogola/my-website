import glob, os, re

posts = glob.glob('src/content/posts/**/*.md', recursive=True)
missing_cover = []
broken_cover = []
valid_cover = []

for p in posts:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter
    lines = content.split('---')
    if len(lines) >= 3:
        fm = lines[1]
    else:
        fm = content
    
    title_match = re.search(r'title:\s*["\']?([^"\']+)["\']?', fm)
    cover_match = re.search(r'coverImage:\s*["\']?([^"\']+)["\']?', fm)
    
    title = title_match.group(1).strip() if title_match else os.path.basename(p)
    cover = cover_match.group(1).strip() if cover_match else None
    
    if not cover or cover == 'None' or cover == '""' or cover == "''":
        missing_cover.append((title, p))
    else:
        # Check if file exists in public/images
        img_path = os.path.join('public', 'images', cover)
        if not os.path.exists(img_path):
            broken_cover.append((title, cover, p))
        else:
            valid_cover.append((title, cover))

print(f"Total posts: {len(posts)}")
print(f"Valid covers: {len(valid_cover)}")
print(f"Missing cover field: {len(missing_cover)}")
for t, p in missing_cover:
    print(f"  - [MISSING FIELD] {t} ({p})")

print(f"Broken cover path (file missing in public/images): {len(broken_cover)}")
for t, c, p in broken_cover:
    print(f"  - [FILE MISSING] {t} -> {c} ({p})")
