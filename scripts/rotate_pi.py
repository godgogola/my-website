import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 設定旋轉為 Math.PI (180度)，讓 x=1024 (夕陽) 出現在左邊，x=3072 (滿月) 出現在右邊
code = re.sub(
    r"skyDomeMesh\.rotation\.y = 0;",
    "skyDomeMesh.rotation.y = Math.PI;",
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated sky rotation to Math.PI")
