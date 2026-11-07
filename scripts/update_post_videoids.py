import os
import re

mapping = {
    '結腸激躁症.md': 'etpG9o7JwrM',
    '急性腸胃炎.md': '96Yq0AUdd8I',
    '要如何防治胃癌根除幽門桿菌.md': 'QeLh0_YZjAY',
    '大腸息肉.md': 'YW3vHlmmumc',
    '膽結石.md': 'h3-nrDgZcXA',
    '胃食道逆流.md': 'XJFqsDupY3k',
    '糖尿病併發症.md': 'jlF3bsMgoCQ',
}

base_dir = 'src/content/posts'

for fname, vid in mapping.items():
    fpath = os.path.join(base_dir, fname)
    if not os.path.exists(fpath):
        print(f"Not found: {fpath}")
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'videoId:' in content:
        content = re.sub(r'videoId:\s*"?[^\n"]*"?', f'videoId: "{vid}"', content)
    else:
        content = re.sub(r'(draft:\s*false\n)', f'\\1videoId: "{vid}"\n', content)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {fname} with videoId {vid}")

