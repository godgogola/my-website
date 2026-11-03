import re

# 1. Update Layout.astro
layout_path = 'src/layouts/Layout.astro'
with open(layout_path, 'r', encoding='utf-8') as f:
    layout = f.read()

# Replace meta_title default in Layout.astro
layout = re.sub(
    r"meta_title\s*=\s*['\"][^'\"]*['\"]",
    "meta_title = '黃冠智醫師｜豐田診所院長·肝膽腸胃專科｜無痛內視鏡與代謝減重指南'",
    layout,
    count=1
)

# Replace description default in Layout.astro
layout = re.sub(
    r"description\s*=\s*['\"]豐田診所院長黃冠智醫師的官方網站[^'\"]*['\"]",
    "description = '台中豐田診所院長黃冠智醫師官方網站。專精肝膽腸胃專科、無痛內視鏡（胃鏡與大腸鏡息肉切除）、代謝減重門診、三高慢性病整合管理與健康衛教指南。'",
    layout,
    count=1
)

# Update keywords in Layout.astro
layout = re.sub(
    r'<meta name="keywords" content="[^"]*" />',
    '<meta name="keywords" content="黃冠智, 豐田診所院長, 肝膽腸胃專科, 無痛內視鏡, 代謝減重, 胃鏡, 大腸鏡, 胃食道逆流, 腹部超音波, 減重門診, 台中腸胃科, 慢性病管理" />',
    layout,
    count=1
)

with open(layout_path, 'w', encoding='utf-8') as f:
    f.write(layout)
print("Updated Layout.astro")

# 2. Update index.astro
index_path = 'src/pages/index.astro'
with open(index_path, 'r', encoding='utf-8') as f:
    idx = f.read()

idx = re.sub(
    r'meta_title="[^"]*"',
    'meta_title="黃冠智醫師｜豐田診所院長·肝膽腸胃專科｜無痛內視鏡與代謝減重指南"',
    idx,
    count=1
)

idx = re.sub(
    r'title="[^"]*"',
    'title="黃冠智醫師｜豐田診所院長·肝膽腸胃專科｜無痛內視鏡與代謝減重指南"',
    idx,
    count=1
)

idx = re.sub(
    r'description="[^"]*"',
    'description="台中豐田診所院長黃冠智醫師官方網站。專精肝膽腸胃專科、無痛內視鏡（胃鏡與大腸鏡息肉切除）、代謝減重門診、三高慢性病整合管理與健康衛教指南。"',
    idx,
    count=1
)

# Update the inline Physician schema in index.astro
old_schema_pattern = r'<!-- Google 醫師專業結構化標籤 \(JSON-LD\) -->\s*<script type="application/ld\+json" set:html=\{JSON\.stringify\(\{[^<]*?\}\)\} />'
new_schema = '''<!-- Google 醫師專業結構化標籤 (JSON-LD) - 確立豐田診所院長、肝膽腸胃專科、無痛內視鏡與代謝減重權威定位 -->
  <script type="application/ld+json" set:html={JSON.stringify({
    "@context": "https://schema.org",
    "@type": "Physician",
    "@id": "https://drhuanggi.vercel.app/#physician",
    "name": "黃冠智醫師",
    "alternateName": [
      "黃冠智 醫師",
      "黃冠智 院長",
      "豐田診所院長",
      "黃冠智 肝膽腸胃專科",
      "黃冠智 無痛內視鏡與代謝減重",
      "台中黃冠智醫師"
    ],
    "jobTitle": "豐田診所院長 / 肝膽腸胃專科醫師",
    "medicalSpecialty": [
      "https://schema.org/Gastroenterology",
      "https://schema.org/Hepatology",
      "DigestiveEndoscopy",
      "BariatricMedicine"
    ],
    "knowsAbout": [
      "豐田診所院長",
      "肝膽腸胃專科",
      "無痛內視鏡",
      "代謝減重",
      "無痛胃鏡",
      "無痛大腸鏡",
      "大腸息肉切除",
      "胃食道逆流",
      "幽門螺旋桿菌",
      "慢性肝病與脂肪肝防治",
      "肥胖醫學與瘦瘦針管理"
    ],
    "worksFor": {
      "@type": "MedicalClinic",
      "name": "豐田診所",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "建成路1848號",
        "addressLocality": "南區",
        "addressRegion": "台中市",
        "postalCode": "402",
        "addressCountry": "TW"
      },
      "telephone": "+886-4-2285-0066"
    },
    "description": "台中市豐田診所院長黃冠智醫師，專精肝膽腸胃專科、無痛內視鏡（胃鏡與大腸鏡息肉切除）、代謝減重門診與慢性病整合管理。",
    "image": "https://static.wixstatic.com/media/f229cb_5dcb4100d96e46e1bab7ea4cb7062215~mv2.jpg",
    "url": "https://drhuanggi.vercel.app",
    "sameAs": [
      "https://www.youtube.com/channel/UC4cCA2pEP_JUQwGpWUR19AQ",
      "https://drhuanggi.vercel.app/"
    ]
  })} />'''

idx_replaced, n = re.subn(old_schema_pattern, new_schema, idx, flags=re.DOTALL)
if n > 0:
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(idx_replaced)
    print("Updated index.astro schema successfully")
else:
    print("Warning: old schema pattern not found in index.astro, writing title/desc updates only")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(idx)
