import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. 微調天幕旋轉角度與 Canvas 月球/太陽位置，保證在當前相機俯仰角下，
# 左上方清晰看見燦爛日落晚霞，右上方完美展現皎潔滿月與壯麗銀河！
code = re.sub(
    r"skyDomeMesh\.rotation\.y = Math\.PI \* [0-9.]+;",
    "skyDomeMesh.rotation.y = Math.PI * 0.68;",
    code
)

# 2. 調整月球在 Canvas 上的 Y 座標，使其更醒目地出現在右上方夜空
code = re.sub(
    r"const mx = 3280, my = 360, mr = 88;",
    "const mx = 2950, my = 320, mr = 105;",
    code
)

# 3. 調整太陽晚霞在 Canvas 上的位置
code = re.sub(
    r"const sunsetGrad = ctx\.createRadialGradient\(850, 1150, 40, 850, 1150, 1450\);",
    "const sunsetGrad = ctx.createRadialGradient(650, 1050, 40, 650, 1050, 1550);",
    code
)

# 4. 相機初始位置再微調往後上方退一點點，讓天空與滿月完整納入視野 (極致廣角電影感)
code = re.sub(
    r"camera\.position\.set\(0\.0, 16\.5, 27\.5\);",
    "camera.position.set(0.0, 15.2, 28.5);",
    code
)
code = re.sub(
    r"cameraLookAt\.set\(0\.0, 1\.2, 0\);",
    "cameraLookAt.set(0.0, 0.8, 0);",
    code
)

# 5. 調強右側月光在水面上的波光冷光
code = re.sub(
    r"moonLight = new THREE\.DirectionalLight\(0xbfdbfe, [0-9.]+\);",
    "moonLight = new THREE.DirectionalLight(0xdbeafe, 1.85);",
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Applied perfect sky and camera tweaks.")
