import json

# 定義 24 座島嶼資料
islands = [
    # ── 16 座醫學專科島 ──
    {
        "id": "endoscopy", "realm": "health", "q": -1, "r": 0,
        "name": "內視鏡檢查島", "shortName": "內視鏡島", "icon": "🔬",
        "category": "內視鏡檢查",
        "color": "0x0ea5e9", "roofColor": "0x0369a1", "accentColor": "0x38bdf8",
        "subtitle": "無痛舒眠胃鏡、大腸鏡與早期癌篩檢",
        "desc": "以高解析放大內視鏡、NBI 窄頻影像技術，精準洞察食道、胃部與大腸黏膜微血管，讓息肉與早期病變無所遁形。",
        "landmark": "lighthouse"
    },
    {
        "id": "stomach", "realm": "health", "q": -2, "r": 0,
        "name": "胃部疾病島", "shortName": "胃部島", "icon": "🫄",
        "category": "胃部疾病",
        "color": "0xf59e0b", "roofColor": "0xb45309", "accentColor": "0xfbbf24",
        "subtitle": "胃食道逆流、幽門桿菌與胃潰瘍前瞻處置",
        "desc": "深入探討胃酸抑制劑機轉、胃黏膜保護、功能性消化不良及萎縮性胃炎的完整臨床治療方針。",
        "landmark": "cottage"
    },
    {
        "id": "intestine", "realm": "health", "q": -2, "r": 1,
        "name": "腸道疾病島", "shortName": "腸道島", "icon": "🧬",
        "category": "腸道疾病",
        "color": "0x10b981", "roofColor": "0x047857", "accentColor": "0x34d399",
        "subtitle": "腸躁症、腸漏症、便秘與腸道菌群平衡",
        "desc": "探索人體第二大腦——腸道菌相與免疫系統的互動，提供膳食纖維、益生菌與腸道黏膜修復的最佳解方。",
        "landmark": "gazebo"
    },
    {
        "id": "hepatitis", "realm": "health", "q": -3, "r": 0,
        "name": "肝病特區島", "shortName": "肝病島", "icon": "🫁",
        "category": "肝病特區",
        "color": "0xef4444", "roofColor": "0xb91c1c", "accentColor": "0xf87171",
        "subtitle": "B型肝炎、C型肝炎根治與最新抗病毒藥物",
        "desc": "追蹤 B 肝臨床治癒路徑、口服 DAA 抗病毒藥物、肝硬化逆轉與肝細胞癌早期監測。",
        "landmark": "church"
    },
    {
        "id": "liver-biliary", "realm": "health", "q": -3, "r": 1,
        "name": "肝膽胰疾病島", "shortName": "肝膽胰島", "icon": "🧪",
        "category": "肝膽胰疾病",
        "color": "0xd97706", "roofColor": "0x92400e", "accentColor": "0xfbbf24",
        "subtitle": "脂肪肝、膽囊息肉、膽結石與胰臟病變",
        "desc": "代謝性脂肪肝全方位逆轉策略、膽結石追蹤時機與胰臟囊腫的精準影像鑑別。",
        "landmark": "cottage"
    },
    {
        "id": "lipids", "realm": "health", "q": 0, "r": -1,
        "name": "高血脂島", "shortName": "高血脂島", "icon": "🩸",
        "category": "高血脂",
        "color": "0xe11d48", "roofColor": "0x9f1239", "accentColor": "0xfb7185",
        "subtitle": "LDL-C、ApoB、Lp(a) 與心血管硬化斑塊防治",
        "desc": "超壞膽固醇 sdLDL、PCSK9 抑制劑與進階脂蛋白指標解讀，守護動脈彈性與心血管健康。",
        "landmark": "church"
    },
    {
        "id": "hypertension", "realm": "health", "q": 0, "r": -2,
        "name": "高血壓島", "shortName": "高血壓島", "icon": "💓",
        "category": "高血壓",
        "color": "0xf43f5e", "roofColor": "0xbe123c", "accentColor": "0xfb7185",
        "subtitle": "722 血壓量測法、S-ABCDE 生活調整與靶器官保護",
        "desc": "由心臟、大腦到腎臟，建構多重血管保護網，破除隱形殺手帶來的長期動脈硬化風險。",
        "landmark": "cottage"
    },
    {
        "id": "diabetes", "realm": "health", "q": 0, "r": 0,
        "name": "糖尿病島", "shortName": "糖尿病島", "icon": "🧁",
        "category": "糖尿病",
        "color": "0x8b5cf6", "roofColor": "0x6d28d9", "accentColor": "0xa78bfa",
        "subtitle": "糖化血色素、胰島素阻抗與連續血糖監測",
        "desc": "新世代 SGLT2 抑制劑與 GLP-1 腸泌素，結合個人化飲食策略，達成糖尿病緩解與心腎器官保護。",
        "landmark": "church"
    },
    {
        "id": "weight-loss", "realm": "health", "q": -1, "r": 1,
        "name": "減重島", "shortName": "減重島", "icon": "⚖️",
        "category": "減重",
        "color": "0x14b8a6", "roofColor": "0x0f766e", "accentColor": "0x2dd4bf",
        "subtitle": "瘦瘦針 GLP-1/GIP 雙受體促效劑與體組成優化",
        "desc": "突破體重設定點！科學化劑量遞增、肌少症預防與停藥不復胖管理，找回健康自信體態。",
        "landmark": "gazebo"
    },
    {
        "id": "diet", "realm": "health", "q": -2, "r": 2,
        "name": "健康飲食島", "shortName": "飲食島", "icon": "🥗",
        "category": "健康飲食",
        "color": "0x84cc16", "roofColor": "0x4d7c0f", "accentColor": "0xa3e635",
        "subtitle": "地中海飲食、抗發炎食物與微量營養素指南",
        "desc": "以科學飲食抵禦慢性發炎，從維生素 B 群、鋅、鎂到優質脂肪，用日常餐盤打造長壽體質。",
        "landmark": "cottage"
    },
    {
        "id": "medication", "realm": "health", "q": -1, "r": -1,
        "name": "藥物介紹島", "shortName": "藥物島", "icon": "💊",
        "category": "藥物介紹",
        "color": "0x06b6d4", "roofColor": "0x0e7490", "accentColor": "0x67e8f9",
        "subtitle": "藥物機轉、交互作用與安全用藥常識",
        "desc": "拆解 P-CAB、PPI、解痙劑與各類常用處方藥的藥理機制，讓服藥更安心、效果更卓越。",
        "landmark": "church"
    },
    {
        "id": "health-red", "realm": "health", "q": 1, "r": -2,
        "name": "健檢紅字島", "shortName": "健檢紅字島", "icon": "⚠️",
        "category": "健檢紅字怎麼辦",
        "color": "0xf97316", "roofColor": "0xc2410c", "accentColor": "0xfb923c",
        "subtitle": "肝指數 GOT/GPT、腎功能、尿酸與膽紅素判讀",
        "desc": "健檢紅字不用慌！逐項深入剖析異常指標的真正臨床意義與後續追蹤方針。",
        "landmark": "cottage"
    },
    {
        "id": "health-check", "realm": "health", "q": 1, "r": -1,
        "name": "健檢項目島", "shortName": "健檢項目島", "icon": "📋",
        "category": "健檢項目介紹",
        "color": "0x3b82f6", "roofColor": "0x1d4ed8", "accentColor": "0x60a5fa",
        "subtitle": "腫瘤標記、糞便潛血與預防醫學黃金組合",
        "desc": "精選各年齡層必備健檢組合，釐清高階影像與抽血指標的最佳篩檢效益。",
        "landmark": "gazebo"
    },
    {
        "id": "ultrasound", "realm": "health", "q": -1, "r": -2,
        "name": "超音波檢查島", "shortName": "超音波島", "icon": "📡",
        "category": "超音波檢查",
        "color": "0x6366f1", "roofColor": "0x4338ca", "accentColor": "0x818cf8",
        "subtitle": "腹部超音波、甲狀腺篩檢與即時臨床掃描",
        "desc": "醫師的第三隻眼睛！無輻射、高穿透力，即時偵測肝囊腫、血管瘤、腎結石與甲狀腺結節。",
        "landmark": "lighthouse"
    },
    {
        "id": "exercise", "realm": "health", "q": -2, "r": -1,
        "name": "要活就要動島", "shortName": "運動活力島", "icon": "🏃",
        "category": "要活就要動",
        "color": "0x10b981", "roofColor": "0x047857", "accentColor": "0x34d399",
        "subtitle": "阻力訓練、有氧耐力與肌少症防禦",
        "desc": "運動是最好的天然藥物！增肌減脂、改善胰島素敏感度、活化粒線體能量工廠。",
        "landmark": "gazebo"
    },
    {
        "id": "chronic", "realm": "health", "q": 0, "r": 1,
        "name": "慢性病島", "shortName": "慢性病島", "icon": "🩺",
        "category": "慢性病",
        "color": "0xa855f7", "roofColor": "0x7e22ce", "accentColor": "0xc084fc",
        "subtitle": "慢性腎臟病 CKD、代謝症候群與全人照護",
        "desc": "跨專科整合管理，建立保腎護心長遠防線，享有高品質的樂活晚年。",
        "landmark": "church"
    },

    # ── 8 部讀書名著島 ──
    {
        "id": "wealth-ladder", "realm": "wisdom", "q": 1, "r": 0,
        "name": "《財富階梯》島", "shortName": "財富階梯島", "icon": "🪜",
        "book": "財富階梯",
        "color": "0x8b5cf6", "roofColor": "0x581c87", "accentColor": "0xc084fc",
        "subtitle": "Nick Maggiulli 著｜看清你的財務位階與資產躍遷",
        "desc": "從儲蓄率到資產收益率，解析人生各財富階段的最優決策路徑，擺脫無效努力，穩步晉級。",
        "landmark": "church"
    },
    {
        "id": "random-walk", "realm": "wisdom", "q": 1, "r": 1,
        "name": "《漫步華爾街》島", "shortName": "漫步華爾街島", "icon": "📈",
        "book": "漫步華爾街",
        "color": "0x3b82f6", "roofColor": "0x1e3a8a", "accentColor": "0x60a5fa",
        "subtitle": "Burton Malkiel 著｜半世紀不敗的指數化投資聖經",
        "desc": "隨機漫步假說與效率市場理論，破除技術分析迷思，用低成本廣泛指數基金擁抱全球經濟成長。",
        "landmark": "gazebo"
    },
    {
        "id": "golden-rules", "realm": "wisdom", "q": 2, "r": 0,
        "name": "《投資金律》島", "shortName": "投資金律島", "icon": "🏛️",
        "book": "投資金律",
        "color": "0x0d9488", "roofColor": "0x134e4a", "accentColor": "0x2dd4bf",
        "subtitle": "William Bernstein 著｜理論、歷史、心理學與產業四大投資支柱",
        "desc": "神經外科醫師跨界投資大師！以嚴謹醫學實證精神，建立跨越百年市場風暴的資產配置長城。",
        "landmark": "church"
    },
    {
        "id": "most-important", "realm": "wisdom", "q": 2, "r": -1,
        "name": "《投資前最重要的事》島", "shortName": "最重要事島", "icon": "💡",
        "book": "投資前最重要的事",
        "color": "0xf59e0b", "roofColor": "0xb45309", "accentColor": "0xfbbf24",
        "subtitle": "Ben Carlson 著｜簡單至上、心理防禦與避免代價高昂的錯誤",
        "desc": "專注你能掌控的事！克服群眾狂熱、接納市場常態，用優雅簡約的紀律勝過複雜演算法。",
        "landmark": "cottage"
    },
    {
        "id": "die-with-zero", "realm": "wisdom", "q": 2, "r": 1,
        "name": "《別把你的錢留到死》島", "shortName": "留錢到死島", "icon": "⌛",
        "book": "別把你的錢留到死",
        "color": "0xec4899", "roofColor": "0x9d174d", "accentColor": "0xf472b6",
        "subtitle": "Bill Perkins 著｜人生是體驗的總和，極大化你的生命記憶股息",
        "desc": "在健康、時間與財富的黃金交叉點投資體驗！不要在躺在病床上時才帶著滿手遺憾離開。",
        "landmark": "gazebo"
    },
    {
        "id": "glucose", "realm": "wisdom", "q": 3, "r": 0,
        "name": "《90%的病，控糖就會好》島", "shortName": "控糖生活島", "icon": "🥑",
        "book": "90%的病，控糖就會好",
        "color": "0x10b981", "roofColor": "0x047857", "accentColor": "0x34d399",
        "subtitle": "Jessie Inchauspé 著｜餐序原則、醋水與平穩葡萄糖曲線",
        "desc": "風靡全球的葡萄糖革命！不用嚴格節食，透過調整進食順序與餐後散步，告別疲勞、嗜甜與體重困擾。",
        "landmark": "cottage"
    },
    {
        "id": "brain-neuro", "realm": "wisdom", "q": 2, "r": -2,
        "name": "《你的人生他們六個說了算》島", "shortName": "神經傳導島", "icon": "🧠",
        "book": "你的人生，他們六個說了算!",
        "color": "0x6366f1", "roofColor": "0x3730a3", "accentColor": "0xa5b4fc",
        "subtitle": "多巴胺、血清素、催產素、皮質醇等六大情緒荷爾蒙大腦掌控術",
        "desc": "掌握大腦神經化學物質的規律，調節專注、焦慮、動機與滿足感，做自己心智的真正主人。",
        "landmark": "lighthouse"
    },
    {
        "id": "sapiens", "realm": "wisdom", "q": 3, "r": -1,
        "name": "《人類大歷史》島", "shortName": "人類歷史島", "icon": "🌍",
        "book": "人類大歷史",
        "color": "0xd97706", "roofColor": "0x78350f", "accentColor": "0xfcd34d",
        "subtitle": "Yuval Noah Harari 著｜從認知革命、農業革命到智人的未來",
        "desc": "虛構故事的力量如何凝聚數十億智人，站在宏觀歷史視野反思科技、金錢與人生的終極意義。",
        "landmark": "gazebo"
    }
]

print(f"Total islands: {len(islands)}")
with open('scripts/islands_24_data.json', 'w', encoding='utf-8') as f:
    json.dump(islands, f, ensure_ascii=False, indent=2)
print("Saved scripts/islands_24_data.json successfully")
