import urllib.request, re, sys, json
sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def scrape_url(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
        # find ytInitialData
        m = re.search(r'var ytInitialData = ({.*?});</script>', html)
        if m:
            data = json.loads(m.group(1))
            return data, html
        return None, html
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None, ""

# 1. RSS feed gives exact newest 15 entries
import xml.etree.ElementTree as ET
rss_url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UC4cCA2pEP_JUQwGpWUR19AQ'
req = urllib.request.Request(rss_url, headers=headers)
rss_items = []
with urllib.request.urlopen(req) as resp:
    root = ET.fromstring(resp.read())
ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}
for e in root.findall('atom:entry', ns):
    vid = e.find('yt:videoId', ns).text
    title = e.find('atom:title', ns).text
    published = e.find('atom:published', ns).text
    rss_items.append({'id': vid, 'title': title, 'published': published})

print(f"=== RSS Feed ({len(rss_items)} items) ===")
for item in rss_items:
    print(f"{item['id']} | {item['published']} | {item['title']}")

# 2. Check shorts tab
data, html = scrape_url('https://www.youtube.com/channel/UC4cCA2pEP_JUQwGpWUR19AQ/shorts')
short_ids = re.findall(r'/shorts/([a-zA-Z0-9_-]{11})', html)
print(f"\n=== Shorts ({len(short_ids)} found) ===")
seen = set()
for s in short_ids:
    if s not in seen:
        seen.add(s)
        print(s)

# 3. Check videos tab
data, html = scrape_url('https://www.youtube.com/channel/UC4cCA2pEP_JUQwGpWUR19AQ/videos')
vid_ids = re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)
print(f"\n=== Videos ({len(vid_ids)} found) ===")
for v in vid_ids:
    if v not in seen:
        seen.add(v)
        print(v)

