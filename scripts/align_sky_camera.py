import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. 確保天幕的旋轉角度精準對齊：夕陽在左 (-X)，滿月在右 (+X)
# 在 createMasterpieceSkyDome 中設定 skyDomeMesh.rotation.y
sky_fix = """    skyDomeMesh = new THREE.Mesh(skyGeo, skyMat);
    skyDomeMesh.rotation.y = Math.PI * 0.98; // 精準校正：夕陽居左，明月居右
    scene.add(skyDomeMesh);"""

code = re.sub(
    r"skyDomeMesh = new THREE\.Mesh\(skyGeo, skyMat\);\s*scene\.add\(skyDomeMesh\);",
    sky_fix,
    code
)

# 2. 擴大相機的視錐遠裁切面，避免天球邊緣被裁切
code = re.sub(
    r"camera = new THREE\.PerspectiveCamera\(36, aspect, 0\.5, 380\);",
    "camera = new THREE.PerspectiveCamera(38, aspect, 0.5, 600);",
    code
)

# 3. 調整相機預設位置，更接近示意圖的俯瞰構圖
code = re.sub(
    r"camera\.position\.set\([^)]+\);",
    "camera.position.set(0.0, 16.5, 27.5);",
    code
)
code = re.sub(
    r"cameraLookAt\.set\([^)]+\);",
    "cameraLookAt.set(0.0, 1.2, 0);",
    code
)

# 4. 提升海洋深邃蔚藍質感與高光
code = re.sub(
    r"color:\s*0x0a335c,",
    "color: 0x114e7e, roughness: 0.22, metalness: 0.3,",
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Applied sky rotation and camera adjustment.")
