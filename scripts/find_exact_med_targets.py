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
        posts.append((category, title, cover, os.path.basename(p)))

# Search exact matches for high-priority clinical conditions
targets = [
    '大腸息肉',
    '糖尿病併發症',
    '高血脂治療',
    '膽結石',
    '要如何防治胃癌根除幽門桿菌',
    '急性腸胃炎'
]

for t in targets:
    found = [p for p in posts if t in p[1] or t in p[3]]
    for f in found:
        print(f"Target: {t} -> Title: '{f[1]}', File: '{f[3]}', Cover: '{f[2]}'")

