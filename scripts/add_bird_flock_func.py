import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 定義飛鳥群函數與變數
bird_func = """  let birdFlockData = null;

  // ══════════════════════════════════════════════════════════════════════
  // 動態空中盤旋飛鳥群 (8字型立體盤旋 + V字翅膀拍動)
  // ══════════════════════════════════════════════════════════════════════
  function createBirdFlock() {
    const flockGroup = new THREE.Group();
    const birdMeshes = [];
    const birdCount = 14;

    const wingMat = new THREE.MeshStandardMaterial({
      color: 0x18181b,
      roughness: 0.7,
      side: THREE.DoubleSide
    });

    for (let i = 0; i < birdCount; i++) {
      const bird = new THREE.Group();

      // 左翅膀
      const leftWingGeo = new THREE.BufferGeometry();
      const lwVerts = new Float32Array([
        0, 0, 0,
        -0.38, 0.08, -0.06,
        -0.28, 0, 0.15
      ]);
      leftWingGeo.setAttribute('position', new THREE.BufferAttribute(lwVerts, 3));
      leftWingGeo.computeVertexNormals();
      const leftWing = new THREE.Mesh(leftWingGeo, wingMat);

      // 右翅膀
      const rightWingGeo = new THREE.BufferGeometry();
      const rwVerts = new Float32Array([
        0, 0, 0,
        0.38, 0.08, -0.06,
        0.28, 0, 0.15
      ]);
      rightWingGeo.setAttribute('position', new THREE.BufferAttribute(rwVerts, 3));
      rightWingGeo.computeVertexNormals();
      const rightWing = new THREE.Mesh(rightWingGeo, wingMat);

      bird.add(leftWing);
      bird.add(rightWing);

      const scale = 0.65 + Math.random() * 0.45;
      bird.scale.setScalar(scale);

      bird.userData = {
        leftWing,
        rightWing,
        offset: (i / birdCount) * Math.PI * 2,
        speed: 0.28 + (i % 4) * 0.06,
        height: 8.5 + (i % 5) * 1.2,
        radiusX: 13.5 + (i % 3) * 3.5,
        radiusZ: 7.5 + (i % 3) * 2.5,
        flapSpeed: 7.5 + Math.random() * 3.0
      };

      flockGroup.add(bird);
      birdMeshes.push(bird);
    }

    scene.add(flockGroup);
    return { group: flockGroup, birds: birdMeshes };
  }
"""

# 在 setupLightingAndCelestial 之前插入
code = re.sub(
    r"(function setupLightingAndCelestial\(\) \{)",
    bird_func + "\n\\1",
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Added createBirdFlock function successfully.")
