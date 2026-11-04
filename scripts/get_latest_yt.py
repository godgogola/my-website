import urllib.request, sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://www.youtube.com/feeds/videos.xml?channel_id=UC4cCA2pEP_JUQwGpWUR19AQ'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read()
root = ET.fromstring(content)
ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015'}

print("Latest YouTube Videos:")
for entry in root.findall('atom:entry', ns):
    title = entry.find('atom:title', ns).text
    vid = entry.find('yt:videoId', ns).text
    published = entry.find('atom:published', ns).text
    print(f"[{published}] {vid} -> {title}")

