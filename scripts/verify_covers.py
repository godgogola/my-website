import os

candidates = [
    ('XfHwQv_rK1M', '【膳食纖維】膳食纖維對便秘的角色.webp', '膳食纖維膳食纖維對便秘的角色', '【膳食纖維】膳食纖維對便秘的角色', '腸道疾病'),
    ('JhMbwCXk6g8', '【肥胖症】肥胖症併發症.webp', '肥胖症肥胖症併發症', '【肥胖症】肥胖症併發症', '健康享瘦'),
    ('WFkqFR6V3E4', '【肥胖症】肥胖症成因.webp', '肥胖症肥胖症成因', '【肥胖症】肥胖症成因', '健康享瘦'),
    ('tOsZg8Ly6m4', '打嗝.webp', '打嗝', '打嗝', '胃部疾病'),
    ('be6aOS4pLTA', '【飲食指南】低普林飲食.webp', '飲食指南低普林飲食', '【飲食指南】低普林飲食', '飲食指南'),
    ('XeQxvq-WvC4', '【瘦瘦針】瘦瘦針停藥復胖原因.webp', '瘦瘦針瘦瘦針停藥復胖原因', '【瘦瘦針】瘦瘦針停藥復胖原因', '健康享瘦'),
    ('58vQDXVfRw8', '【HDL】好膽固醇太高是好事嗎.webp', 'hdl好膽固醇太高是好事嗎', '【HDL】好膽固醇太高是好事嗎', '高血脂'),
    ('s6qsuM_4jmk', '【sdLDL】什麼是超壞膽固醇.webp', 'sdldl什麼是超壞膽固醇', '【sdLDL】什麼是超壞膽固醇', '高血脂'),
    ('KTv_9w5f7UQ', '【飲食指南】腸躁症低 FODMAP.webp', '飲食指南腸躁症低-fodmap', '【飲食指南】腸躁症低 FODMAP', '飲食指南'),
    ('VY5r8liDmB0', '【HDL】好膽固醇偏低的原因.webp', 'hdl好膽固醇偏低的原因', '【HDL】好膽固醇偏低的原因', '高血脂'),
    ('g_oCljiXXoA', '【2026 ACCAHA 】高三酸甘油脂治療臨床指引差異.webp', '2026-accaha-高三酸甘油脂治療臨床指引差異', '【2026 ACCAHA 】高三酸甘油脂治療臨床指引差異', '高血脂'),
    ('3qJZRSpmQ5c', '【痔瘡】症狀與分級.webp', '痔瘡症狀與分級', '【痔瘡】症狀與分級', '腸道疾病'),
    ('xvuK-MCJ-mk', '功能性消化不良.webp', '功能性消化不良', '功能性消化不良', '胃部疾病'),
    ('-gQ2sZLsmbA', '黑腸症.webp', '黑腸症', '黑腸症', '腸道疾病'),
    ('ec2MtIG8ygY', '【大腸癌】大腸鏡與篩檢因子.webp', '大腸癌大腸鏡與篩檢因子', '【大腸癌】大腸鏡與篩檢因子', '腸道疾病'),
    ('lY65SMoxspI', '【地雷食物】胃食道逆流地雷食物.webp', '地雷食物胃食道逆流地雷食物', '【地雷食物】胃食道逆流地雷食物', '胃部疾病'),
    ('ZjiOi4Ez_eM', '【代謝功能障礙相關脂肪肝】盛行率與成因.webp', '代謝功能障礙相關脂肪肝盛行率與成因', '【代謝功能障礙相關脂肪肝】盛行率與成因', '肝膽胰疾病'),
    ('syjGKVpqUQc', '【2025-2030年美國飲食指南】每日飲食指南.webp', '2025-2030年美國飲食指南每日飲食指南', '【2025-2030年美國飲食指南】每日飲食指南', '飲食指南'),
    ('5clwsrdD-tw', '酒精性肝病變.webp', '酒精性肝病變', '酒精性肝病變', '肝膽胰疾病'),
    ('ZBbCRg9-p8c', '【腸鏡前準備】清腸劑(保可淨與耐福力散).webp', '腸鏡前準備清腸劑保可淨與耐福力散', '【腸鏡前準備】清腸劑(保可淨與耐福力散)', '內視鏡檢查')
]

imgs = os.listdir('public/images')
for vid, cover, slug, title, cat in candidates:
    exists = cover in imgs
    print(f"{vid} | {cover} -> exists: {exists}")
    if not exists:
        # find matching
        matched = [f for f in imgs if any(part in f for part in cover.replace('【','').replace('】','').replace('.webp','').split() if len(part)>2)]
        print(f"   closest: {matched[:3]}")

