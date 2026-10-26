import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for tab in ['videos', 'shorts']:
    url = f'https://www.youtube.com/@godgogola/{tab}'
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        
        # Match pattern: "videoId":"...", "title":{"runs":[{"text":"..."}]}
        # or title":{"simpleText":"..."}
        pattern = r'"videoId":"([a-zA-Z0-9_-]{11})".*?"title":\{"runs":\[\{"text":"(.*?)"\}\]'
        matches = re.findall(pattern, html)
        print(f"=== {tab.upper()} ===")
        seen = set()
        for vid, title in matches:
            if vid not in seen:
                seen.add(vid)
                print(f"ID: {vid} | Title: {title}")
    except Exception as e:
        print(f"Error fetching {tab}: {e}")
