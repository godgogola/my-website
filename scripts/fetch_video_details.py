import urllib.request
import re
import json

videos = [
    ('Ober6p42NBM', '06'),
    ('y6eYcVWpXLY', '05'),
    ('xdevp0g6r9M', '04'),
    ('xXuEZGbFqu0', '03'),
    ('nF1YCgAFjEg', '02'),
    ('g4dFGcoet7w', '01'),
]

with open('scripts/video_desc.txt', 'w', encoding='utf-8') as out:
    for vid, ep in videos:
        url = f'https://www.youtube.com/watch?v={vid}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        m = re.search(r'"shortDescription":"(.*?)"', html)
        if m:
            raw = m.group(1)
            # Use json.loads to unescape properly
            desc = json.loads(f'"{raw}"')
            first_line = desc.split('\n')[0].strip()
            out.write(f"=== Ep {ep} ({vid}) ===\n{first_line}\n\n")
            print(f"Done Ep {ep}")
