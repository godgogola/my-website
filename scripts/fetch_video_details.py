import urllib.request, json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

video_ids = [
    "9njkkBBiDkg",
    "zhBtKjibzkM",
    "VGBp9EIMLLE",
    "3Q9je5AmbEc",
    "upRugOtf4rI",
    "ETbc0F7G35U",
    "vJDWppSFYyI",
    "GEarPGa3Wso",
    "_MFumV4dbgs",
    "HKeYzNAzvLE",
    "PZHOyX4llGI",
    "Q-meLPVXDv4",
    "GqRSeWBpCR8",
    "zp7aeqpjGyw",
    "Dr2M5Yvwlbs",
    "tXlbdUwahMQ",
    "-19NNKlOX8o",
    "Y3G6w7l9Nwg",
    "ibMKsMPdBDg",
    "IgjzEfNrgFk",
    "582aiZM_MeA",
    "YnIuwXuu-MY",
    "fGJFtUTxvC4",
    "sGHNkCItIL8",
]

headers = {'User-Agent': 'Mozilla/5.0'}

results = []
for vid in video_ids:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            title = data.get('title', '')
            results.append({'id': vid, 'title': title})
            print(f"OK: {vid} -> {title}")
    except Exception as e:
        print(f"Error for {vid}: {e}")

with open('scripts/today_24_videos.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Saved scripts/today_24_videos.json")

