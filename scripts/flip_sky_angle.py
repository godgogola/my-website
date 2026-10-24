import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 將天球旋轉改為 -Math.PI * 0.08，使左側為金黃夕陽晚霞，右側為銀河星空滿月
code = re.sub(
    r"skyDomeMesh\.rotation\.y = Math\.PI \* [0-9.]+;",
    "skyDomeMesh.rotation.y = -Math.PI * 0.08;",
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated sky rotation to -Math.PI * 0.08")
