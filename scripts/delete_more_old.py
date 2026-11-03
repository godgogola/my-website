import re

with open('src/data/videos.ts', encoding='utf-8') as f:
    text = f.read()

more_old_ids = ['qMUTVaZCQQM', 'Cnrj35A6l0w', 'HlLtaJsgbic', '5VG5rwPXSy8', 'hSIqpatHQco']

for vid in more_old_ids:
    pattern = rf"\s*\{{[^{{}}]*?id:\s*'{re.escape(vid)}'[^{{}}]*?\}},?"
    text, n = re.subn(pattern, '', text)
    if n > 0:
        print(f"Deleted old duplicate: {vid}")

with open('src/data/videos.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print("Cleaned up remaining duplicate old items.")

