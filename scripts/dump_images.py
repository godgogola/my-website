import os
import json

images = os.listdir('public/images')

keywords = ['肥胖', '瘦瘦針', '普林', '痛風', 'LDL', 'FODMAP', 'HDL', '三酸甘油脂', '痔瘡', '大腸癌', '脂肪肝', '飲食指南', '清腸', '耐福力', '保可淨', '潛血']
result = {}
for kw in keywords:
    result[kw] = [f for f in images if kw in f]

with open('scripts/matched_images.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Saved matched_images.json")

