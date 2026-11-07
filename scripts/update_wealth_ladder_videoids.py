import os
import re

mapping = {
    '01-順著財富階梯向上而增加消費.md': 'g4dFGcoet7w',
    '02-順著財富階梯向上而增加收入.md': 'nF1YCgAFjEg',
    '03-順著財富階梯向上而增加投資.md': 'xXuEZGbFqu0',
    '04-第-1-階淨資產小於-1-萬美元生存穩定.md': 'xdevp0g6r9M',
    '05-第-2-階淨資產-1-萬10-萬美元雜貨自由.md': 'y6eYcVWpXLY',
    '06-第-3-階淨資產-10-萬100-萬美元餐廳自由.md': 'Ober6p42NBM',
}

base_dir = r'src/content/books/財富階梯'

for fname, vid in mapping.items():
    fpath = os.path.join(base_dir, fname)
    if not os.path.exists(fpath):
        print(f'Not found: {fpath}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'videoId:' in content:
        content = re.sub(r'videoId:\s*"?[^\n"]*"?', f'videoId: "{vid}"', content)
    else:
        content = re.sub(r'(draft:\s*false\n)', f'\\1videoId: "{vid}"\n', content)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {fname} with videoId: {vid}')

