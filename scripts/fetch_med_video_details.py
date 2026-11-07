import urllib.request
import re
import json

videos = [
    ('etpG9o7JwrM', '腸躁症'),
    ('96Yq0AUdd8I', '急性腸胃炎'),
    ('QeLh0_YZjAY', '幽門螺旋桿菌'),
    ('YW3vHlmmumc', '大腸息肉'),
    ('h3-nrDgZcXA', '膽結石'),
    ('XJFqsDupY3k', '胃食道逆流'),
    ('jlF3bsMgoCQ', '糖尿病併發症'),
]

with open('scripts/medical_video_details.txt', 'w', encoding='utf-8') as out:
    for vid, tag in videos:
        url = f'https://www.youtube.com/watch?v={vid}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
            m = re.search(r'"shortDescription":"(.*?)"', html)
            if m:
                raw = m.group(1)
                desc = json.loads(f'"{raw}"')
                first_line = desc.split('\n')[0].strip()
                out.write(f"=== {tag} ({vid}) ===\n{first_line}\n\n")
                print(f"Fetched {tag}")
        except Exception as e:
            print(f"Error {vid}: {e}")

