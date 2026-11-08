import glob
import os

posts = glob.glob('src/content/posts/**/*.md', recursive=True)
for p in sorted(posts):
    try:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue
    if 'category: "高血壓"' in content or 'category: 高血壓' in content:
        title = ''
        cover = ''
        category = ''
        for line in content.split('\n')[:15]:
            if line.startswith('title:'):
                title = line.split(':', 1)[1].strip().strip('"').strip("'")
            elif line.startswith('coverImage:'):
                cover = line.split(':', 1)[1].strip().strip('"').strip("'")
            elif line.startswith('category:'):
                category = line.split(':', 1)[1].strip().strip('"').strip("'")
        print(f"File: {os.path.basename(p)}")
        print(f"  Title: {title}")
        print(f"  Cover: {cover}")
        print(f"  Category: {category}")
        print("-" * 40)

