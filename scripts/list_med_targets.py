import glob
import os

posts = []
for p in glob.glob('src/content/posts/*.md'):
    with open(p, 'r', encoding='utf-8') as f:
        title = ''
        category = ''
        cover = ''
        for line in f:
            if line.startswith('title:'):
                title = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('category:'):
                category = line.split(':', 1)[1].strip().strip('"')
            elif line.startswith('coverImage:'):
                cover = line.split(':', 1)[1].strip().strip('"')
        if category not in ['指數投資', '投資理財']:
            posts.append((category, title, cover, os.path.basename(p)))

print(f"Total medical posts: {len(posts)}")
# Filter core posts: Diabetes, Lipids, Colon Polyps, H. pylori, Endoscopy, etc.
core_keywords = ['糖尿病', '高血脂', '大腸息肉', '幽門', '膽結石', '便秘', '胃潰瘍', '痛風', '骨質疏鬆']
core_posts = [p for p in posts if any(k in p[1] for k in core_keywords)]
print(f"Core target posts found: {len(core_posts)}")
for cat, title, cover, fname in core_posts[:20]:
    print(f"[{cat}] {title} (file: {fname}, cover: {cover})")

