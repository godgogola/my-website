import os

path = r'src/layouts/Layout.astro'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """    <!-- Google 官方指定網站名稱結構化標籤 (WebSite Structured Data for Google Site Name) -->
    <script type="application/ld+json" set:html={JSON.stringify({
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "黃冠智醫師",
      "alternateName": ["黃冠智醫師個人官方網站", "黃冠智院長", "黃冠智醫師健康指南"],
      "url": "https://drhuanggi.vercel.app/"
    })} />"""

replacement = """    <!-- Google 官方指定網站名稱結構化標籤 (WebSite Structured Data for Google Site Name) -->
    <script type="application/ld+json" set:html={JSON.stringify({
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "黃冠智醫師",
      "alternateName": [
        "黃冠智院長",
        "黃冠智醫師個人官方網站",
        "黃冠智 肝膽腸胃科",
        "台中黃冠智醫師",
        "黃冠智 豐田診所"
      ],
      "url": "https://drhuanggi.vercel.app/"
    })} />

    <!-- Google 官方專科醫師實體結構化資料 (Physician Schema - 確立台中/肝膽腸胃科/豐田診所定位，精準區隔新竹心臟科學弟) -->
    <script type="application/ld+json" set:html={JSON.stringify({
      "@context": "https://schema.org",
      "@type": "Physician",
      "@id": "https://drhuanggi.vercel.app/#physician",
      "name": "黃冠智",
      "alternateName": ["黃冠智 醫師", "黃冠智 院長", "台中黃冠智醫師", "黃冠智 腸胃科醫師"],
      "jobTitle": "豐田診所 院長 / 肝膽腸胃科專科醫師",
      "medicalSpecialty": [
        "https://schema.org/Gastroenterology",
        "DigestiveEndoscopy",
        "BariatricMedicine"
      ],
      "knowsAbout": [
        "肝膽腸胃科",
        "無痛胃鏡",
        "無痛大腸鏡",
        "大腸息肉切除",
        "胃食道逆流",
        "幽門螺旋桿菌",
        "脂肪肝與肝膽防治",
        "代謝減重與肥胖醫學",
        "瘦瘦針與血糖管理"
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
      "url": "https://drhuanggi.vercel.app/",
      "sameAs": [
        "https://www.youtube.com/channel/UC4cCA2pEP_JUQwGpWUR19AQ",
        "https://drhuanggi.vercel.app/"
      ],
      "description": "黃冠智醫師為台中市豐田診所院長、肝膽腸胃專科醫師，前長庚與仁愛醫院主治醫師，專精於消化道內視鏡（無痛胃鏡、大腸鏡檢查與息肉切除）、肝膽疾病防治及代謝減重整合照護。"
    })} />"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Layout.astro updated with Physician Schema")
else:
    # Try normalizing CRLF / LF
    target_lf = target.replace('\r\n', '\n')
    content_lf = content.replace('\r\n', '\n')
    if target_lf in content_lf:
        content_lf = content_lf.replace(target_lf, replacement.replace('\r\n', '\n'), 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content_lf)
        print("SUCCESS (LF): Layout.astro updated with Physician Schema")
    else:
        print("ERROR: target not found")
