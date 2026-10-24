import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. 更新島嶼色彩配置，使其精準對齊示意圖的三區域色彩分配：
# - 前排與左側（夕陽受光區）：暖赭金黃、赤陶色、暖杏橘、焦糖褐
# - 中央（過渡區）：高雅皇家紫、深紫羅蘭、絳紅
# - 右側（星夜冷光區）：深海群青藍、孔雀青綠、冷翠綠

color_map = {
    # 常用藥物（中心前哨）
    "'drugs'": ("0xd97736", "0x9a3412", "0xfed7aa"), # 暖金赭黃
    # 胃部疾病（左側前排）
    "'stomach'": ("0xde8235", "0x9c4221", "0xffedd5"), # 赤陶暖橘
    # 腸道疾病（左側前排）
    "'colon'": ("0xc85a17", "0x7c2d12", "0xfed7aa"), # 熟褐金橘
    # 肝膽胰（左側中排）
    "'liver'": ("0xca8a04", "0x854d0e", "0xfef08a"), # 秋香金褐
    # 肝病特區（左側後排）
    "'hepatitis'": ("0xb45309", "0x78350f", "0xfde68a"), # 暖金琥珀
    # 內視鏡檢查（左後方燈塔島）
    "'endoscopy'": ("0x0d9488", "0x134e4a", "0x99f6e4"), # 薄荷青瓷（燈塔基座）
    # 超音波檢查（左側後排）
    "'ultrasound'": ("0x0284c7", "0x075985", "0xbae6fd"), # 湛藍水波
    # 癌症篩檢與隨筆（左側外圍）
    "'cancer-misc'": ("0x7c3aed", "0x4c1d95", "0xddd6fe"), # 暮紫星空
    # 高血壓（中央核心區）
    "'hypertension'": ("0xb91c1c", "0x7f1d1d", "0xfecaca"), # 深石榴赤紅
    # 高血脂（中央核心區）
    "'hyperlipidemia'": ("0x991b1b", "0x6b1212", "0xfecaca"), # 雅致磚紅
    # 糖尿病（中央核心區）
    "'diabetes'": ("0x6d28d9", "0x4c1d95", "0xddd6fe"), # 皇家深紫
    # 減重醫學（中央前排）
    "'weight-loss'": ("0xd97706", "0x92400e", "0xfde68a"), # 暖金天秤
    # 慢性病保腎（中央中排）
    "'chronic'": ("0x4c1d95", "0x2e1065", "0xc4b5fd"), # 神秘深紫
    # 健康飲食（前排中側）
    "'nutrition'": ("0xeab308", "0xa16207", "0xfef08a"), # 金黃蔬果
    # 健檢指標（前排中側）
    "'blood-tests'": ("0x0284c7", "0x0369a1", "0x7dd3fc"), # 青藍檢驗
    # 運動處方（左前排）
    "'exercise'": ("0xd96534", "0x9a3412", "0xffedd5"), # 活力暖陶
    # 財富階梯（右側中央過渡）
    "'wealth-ladder'": ("0x581c87", "0x3b0764", "0xd8b4fe"), # 尊爵深紫
    # 他們六個說了算（右側大腦）
    "'six-neuro'": ("0x7c3aed", "0x5b21b6", "0xe9d5ff"), # 幻紫神經
    # 控糖就會好（右側前中）
    "'glucose-goddess'": ("0xbe123c", "0x881337", "0xfecdd3"), # 玫瑰覆盆莓
    # 別把錢留到死（右側後排）
    "'die-with-zero'": ("0x0369a1", "0x075985", "0xbae6fd"), # 星夜深藍
    # 漫步華爾街（右側花園涼亭）
    "'random-walk'": ("0x0f766e", "0x134e4a", "0x99f6e4"), # 孔雀碧石
    # 投資前最重要的事（右側前排花園）
    "'investing-pillars'": ("0x166534", "0x14532d", "0xbbf7d0"), # 翡翠常青
    # 人類大歷史（右側外圍）
    "'sapiens'": ("0x1e3a8a", "0x172554", "0xbfdbfe"), # 宇宙群青
}

# 替換島嶼色彩
for island_key, (c_main, c_roof, c_acc) in color_map.items():
    # 尋找該 island block
    pattern = rf"(id:\s*{island_key}[\s\S]*?color:\s*)0x[0-9a-fA-F]+([\s\S]*?roofColor:\s*)0x[0-9a-fA-F]+([\s\S]*?accentColor:\s*)0x[0-9a-fA-F]+"
    replacement = rf"\g<1>{c_main}\g<2>{c_roof}\g<3>{c_acc}"
    text = re.sub(pattern, replacement, text)

print("Updated Island Palettes successfully.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)
