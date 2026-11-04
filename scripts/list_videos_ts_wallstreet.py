import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/data/videos.ts', 'r', encoding='utf-8') as f:
    c = f.read()

vids = re.findall(r"id:\s*['\"]([^'\"]+)['\"].*?title:\s*['\"]([^'\"]+)['\"]", c, re.DOTALL)
for vid, title in vids:
    if '漫步華爾街' in title:
        print(f"videos.ts: {vid} -> {title}")

