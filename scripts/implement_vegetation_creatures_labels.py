import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# ─────────────────────────────────────────────────────────────────────────────
# 1. 升級 CSS：讓全 23 座島嶼標籤 100% 預設全部顯示，並具備錯落高低美感
# ─────────────────────────────────────────────────────────────────────────────
new_badge_css = """/* ════════════ 3D 浮動標籤 (CSS2D) ════════════ */
  :global(.island-3d-badge) {
    pointer-events: auto !important;
    cursor: pointer;
    transform: translate(-50%, -100%);
    transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.2s ease, filter 0.2s ease;
    user-select: none;
    opacity: 0.94 !important; /* 23 座島嶼標籤全部 100% 預設清晰可見 */
  }

  :global(.island-3d-badge:hover),
  :global(.island-3d-badge.hover-active),
  :global(.island-3d-badge.focus-active) {
    transform: translate(-50%, -108%) scale(1.08) !important;
    z-index: 70 !important;
    opacity: 1 !important;
    filter: drop-shadow(0 0 10px rgba(246, 200, 134, 0.6));
  }

  :global(.island-3d-badge-inner) {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 2px 5px 2px 7px;
    background: linear-gradient(135deg, rgba(32, 22, 24, 0.95), rgba(15, 12, 16, 0.98));
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 9999px;
    border: 1.2px solid rgba(224, 168, 115, 0.72);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.65), inset 0 1px 1.5px rgba(255, 230, 200, 0.25);
    color: #fcf8f2;
    white-space: nowrap;
    transition: all 0.2s ease;
  }

  :global(.island-3d-badge:hover .island-3d-badge-inner),
  :global(.island-3d-badge.focus-active .island-3d-badge-inner) {
    border-color: #f6c886;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.75), 0 0 12px rgba(246, 200, 134, 0.45);
  }

  :global(.badge-icon) {
    font-size: 0.85rem;
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.5));
  }

  :global(.badge-title) {
    font-size: 0.7rem;
    font-weight: 800;
    color: #fbf5ee;
    letter-spacing: 0.2px;
    text-shadow: 0 1px 2px rgba(0,0,0,0.85);
  }

  :global(.badge-pins-count) {
    font-size: 0.62rem;
    font-weight: 800;
    padding: 1px 5px;
    border-radius: 9999px;
    background: rgba(45, 212, 191, 0.25);
    color: #5eead4;
    border: 1px solid rgba(45, 212, 191, 0.5);
    text-shadow: 0 1px 2px rgba(0,0,0,0.5);
  }

  :global(.island-3d-badge.health .badge-pins-count) {
    background: rgba(239, 68, 68, 0.28);
    color: #fca5a5;
    border-color: rgba(239, 68, 68, 0.5);
  }

  :global(.island-3d-badge.wisdom .badge-pins-count) {
    background: rgba(168, 85, 247, 0.3);
    color: #e9d5ff;
    border-color: rgba(168, 85, 247, 0.5);
  }

  :global(.badge-arrow) {
    width: 0;
    height: 0;
    margin: -1px auto 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid rgba(20, 14, 18, 0.95);
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.4));
  }

  :global(.island-3d-badge.labels-hidden) {
    display: none !important;
  }

  /* ════════════ 左側：島嶼抽屜"""

code = re.sub(
    r"/\* ════════════ 3D 浮動標籤 \(CSS2D\) ════════════ \*/[\s\S]*?/\* ════════════ 左側：島嶼抽屜",
    new_badge_css,
    code
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. 升級標籤位置計算：依前後排（r 座標）智慧錯落高低，避免重疊死角
# ─────────────────────────────────────────────────────────────────────────────
staggered_badge_logic = """      // 7. CSS2D 懸浮標籤 (所有 23 座島嶼 100% 顯示，依前中後排階梯錯落高度，不互相遮擋)
      const badgeDiv = document.createElement('div');
      badgeDiv.className = `island-3d-badge ${island.realm}`;
      badgeDiv.dataset.islandId = island.id;
      badgeDiv.innerHTML = `
        <div class="island-3d-badge-inner">
          <span class="badge-icon">${island.icon}</span>
          <span class="badge-title">${island.shortName}</span>
          <span class="badge-pins-count">${island.articles.length}篇</span>
        </div>
        <div class="badge-arrow"></div>
      `;
      badgeDiv.addEventListener('click', (e) => {
        e.stopPropagation();
        focusIsland(island.id);
      });

      // 依島嶼座標計算錯落高低差：
      // 前排 (r > 0)：高度適度下移 (+2.15)，清晰看到地名不擋後排
      // 中排 (r === 0)：高度 +2.65
      // 後排 (r < 0)：高度上提 (+3.15)，從高處俯瞰清楚浮現
      // 特殊地標島（燈塔、高塔）：額外加高以避開尖頂
      let badgeHeight = HEX_HEIGHT + 2.65;
      if (island.r > 0) badgeHeight = HEX_HEIGHT + 2.15;
      else if (island.r < 0) badgeHeight = HEX_HEIGHT + 3.15;

      if (island.id === 'endoscopy') badgeHeight = HEX_HEIGHT + 3.45; // 避開燈塔
      if (island.id === 'hypertension' || island.id === 'wealth-ladder') badgeHeight = HEX_HEIGHT + 3.35; // 避開鐘樓

      const badgeObj = new CSS2DObject(badgeDiv);
      badgeObj.position.set(0, badgeHeight, 0);
      group.add(badgeObj);
      group.userData.badgeDiv = badgeDiv;
      badgeObjects.push(badgeDiv);"""

code = re.sub(
    r"// 7\. CSS2D 懸浮標籤[\s\S]*?badgeObjects\.push\(badgeDiv\);",
    staggered_badge_logic,
    code
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. 升級第 5 點：豐富植被與花叢 (Lush Vegetation)
# - 蓬鬆多球體樹冠 (Fluffy Cloud Deciduous Trees)
# - 多層圓錐松樹 (Tiered Evergreen Pines)
# - 繽紛彩色花叢球 (Colorful Scatter Flower Tufts)
# ─────────────────────────────────────────────────────────────────────────────
vegetation_funcs = """  // 蓬鬆多球體落葉樹冠 (Fluffy Deciduous Tree)
  function createFluffyTree(x, z, leafColor) {
    const treeGroup = new THREE.Group();
    treeGroup.position.set(x, HEX_HEIGHT, z);

    // 樹幹
    const trunkGeo = new THREE.CylinderGeometry(0.065, 0.095, 0.45, 6);
    const trunkMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.9 });
    const trunk = new THREE.Mesh(trunkGeo, trunkMat);
    trunk.position.y = 0.22;
    trunk.castShadow = true;
    treeGroup.add(trunk);

    // 蓬鬆多球簇樹冠 (3~5 顆不同大小的球體微重疊)
    const folMat = new THREE.MeshStandardMaterial({ color: leafColor || 0x16a34a, roughness: 0.78 });
    const clusters = [
      { x: 0, y: 0.52, z: 0, r: 0.26 },
      { x: -0.12, y: 0.46, z: 0.08, r: 0.19 },
      { x: 0.13, y: 0.47, z: -0.06, r: 0.18 },
      { x: 0.05, y: 0.58, z: 0.08, r: 0.17 },
      { x: -0.06, y: 0.48, z: -0.12, r: 0.16 }
    ];
    clusters.forEach(c => {
      const ball = new THREE.Mesh(new THREE.SphereGeometry(c.r, 7, 7), folMat);
      ball.position.set(c.x, c.y, c.z);
      ball.castShadow = true;
      treeGroup.add(ball);
    });

    return treeGroup;
  }

  // 多層次圓錐松樹 (Tiered Pine Tree)
  function createPineTree(x, z) {
    const pineGroup = new THREE.Group();
    pineGroup.position.set(x, HEX_HEIGHT, z);

    const trunk = new THREE.Mesh(
      new THREE.CylinderGeometry(0.045, 0.075, 0.35, 5),
      new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.9 })
    );
    trunk.position.y = 0.17;
    trunk.castShadow = true;
    pineGroup.add(trunk);

    const pineMat = new THREE.MeshStandardMaterial({ color: 0x065f46, roughness: 0.75 });
    // 3 層疊加錐形樹葉
    [[0.32, 0.42, 0.34], [0.24, 0.34, 0.54], [0.15, 0.26, 0.72]].forEach(([r, h, py]) => {
      const cone = new THREE.Mesh(new THREE.ConeGeometry(r, h, 6), pineMat);
      cone.position.y = py;
      cone.castShadow = true;
      pineGroup.add(cone);
    });

    return pineGroup;
  }

  // 微型繽紛彩色花叢 (Flower Clusters)
  function createFlowerTufts(x, z, seedIdx) {
    const flowerGroup = new THREE.Group();
    flowerGroup.position.set(x, HEX_HEIGHT, z);

    const colors = [0xf43f5e, 0xfbbf24, 0xa855f7, 0x38bdf8, 0xec4899];
    const tuftCount = 3 + (seedIdx % 3);

    for (let i = 0; i < tuftCount; i++) {
      const angle = (i / tuftCount) * Math.PI * 2 + (seedIdx * 0.5);
      const rad = 0.08 + (i % 2) * 0.06;
      const c = colors[(seedIdx + i) % colors.length];

      const tuftMat = new THREE.MeshStandardMaterial({ color: c, roughness: 0.85 });
      const tuft = new THREE.Mesh(new THREE.SphereGeometry(0.075, 6, 6), tuftMat);
      tuft.position.set(Math.cos(angle) * rad, 0.06, Math.sin(angle) * rad);
      tuft.castShadow = true;
      flowerGroup.add(tuft);
    }

    return flowerGroup;
  }
"""

# 在 createAmigurumiSheep 上方插入樹木花叢函數
code = re.sub(
    r"(// 可愛毛線小羊 \(Amigurumi Sheep\))",
    vegetation_funcs + "\n\\1",
    code
)

# 替換 populateMiniatureCity 中的樹木與花叢生成
pop_pattern = r"// 周邊點綴配景：副屋、小樹、花叢、小路燈與可愛綿羊[\s\S]*?group\.add\(flowerCluster\);\s*\}\s*\}\);"

new_pop_logic = """// 周邊點綴配景：副屋、蓬鬆樹木、松樹、花叢、小路燈與可愛綿羊
    const offsets = [
      { x: 0.88, z: 0.45, type: 'house' },
      { x: -0.82, z: 0.65, type: 'tree' },
      { x: 0.68, z: -0.78, type: 'pine' },
      { x: -0.88, z: -0.55, type: 'lamp' },
      { x: 0.45, z: 0.92, type: 'lamp' },
      { x: -0.35, z: 0.95, type: 'sheep' },
      { x: 0.55, z: 0.72, type: 'flowers' },
      { x: -0.65, z: 0.22, type: 'flowers' }
    ];

    offsets.forEach((pos, idx) => {
      if (pos.type === 'house' && island.id !== 'endoscopy') {
        const miniGeo = new THREE.BoxGeometry(0.52, 0.48, 0.52);
        const miniWall = new THREE.MeshStandardMaterial({ color: 0xfef3c7, roughness: 0.7 });
        const miniHouse = new THREE.Mesh(miniGeo, miniWall);
        miniHouse.position.set(pos.x, HEX_HEIGHT + 0.24, pos.z);
        miniHouse.rotation.y = (idx * Math.PI) / 3;
        miniHouse.castShadow = true;
        group.add(miniHouse);

        const miniWinGeo = new THREE.PlaneGeometry(0.15, 0.18);
        const miniWin = new THREE.Mesh(miniWinGeo, nightGlowMaterial);
        miniWin.position.set(pos.x, HEX_HEIGHT + 0.28, pos.z + 0.27);
        group.add(miniWin);

        const miniRoofGeo = new THREE.ConeGeometry(0.42, 0.42, 4);
        const miniRoofMat = new THREE.MeshStandardMaterial({ color: mainRoofColor, roughness: 0.6 });
        const miniRoof = new THREE.Mesh(miniRoofGeo, miniRoofMat);
        miniRoof.rotation.y = miniHouse.rotation.y + Math.PI / 4;
        miniRoof.position.set(pos.x, HEX_HEIGHT + 0.48 + 0.21, pos.z);
        miniRoof.castShadow = true;
        group.add(miniRoof);
      } else if (pos.type === 'tree') {
        // 蓬鬆多球簇樹冠 (微縮落葉樹)
        const tColor = isWisdom ? 0x8b5cf6 : (islandIdx % 2 === 0 ? 0x16a34a : 0x22c55e);
        group.add(createFluffyTree(pos.x, pos.z, tColor));
      } else if (pos.type === 'pine') {
        // 多層北歐圓錐松樹
        group.add(createPineTree(pos.x, pos.z));
      } else if (pos.type === 'lamp') {
        group.add(createMiniStreetLamp(pos.x, pos.z));
      } else if (pos.type === 'sheep') {
        group.add(createAmigurumiSheep(pos.x, pos.z, Math.random() * Math.PI * 2));
      } else if (pos.type === 'flowers') {
        // 散佈彩色微型花球
        group.add(createFlowerTufts(pos.x, pos.z, islandIdx + idx));
      }
    });"""

code = re.sub(pop_pattern, new_pop_logic, code)

# ─────────────────────────────────────────────────────────────────────────────
# 4. 升級第 6 點：動態空中盤旋飛鳥群 (Figure-8 Soaring Birds)
# ─────────────────────────────────────────────────────────────────────────────
birds_logic = """  // ══════════════════════════════════════════════════════════════════════
  // 動態空中盤旋飛鳥群 (8字型/圓形盤旋 + V字拍翅膀)
  // ══════════════════════════════════════════════════════════════════════
  function createBirdFlock() {
    const flockGroup = new THREE.Group();
    const birdMeshes = [];
    const birdCount = 14;

    // 建立微縮 V 字型羽翼幾何體
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

      // 飛鳥參數：8 字雙環盤旋軌跡
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
  }"""

# 替換舊的 createBirdFlock
code = re.sub(
    r"function createBirdFlock\(\) \{[\s\S]*?return \{ group: flockGroup, birds: birdMeshes \};\s*\}",
    birds_logic,
    code
)

# 替換 animate 中的飛鳥飛行更新為 8 字盤旋與振翅
animate_bird_pattern = r"// 飛鳥群煽動翅膀與翱翔[\s\S]*?bird\.rotation\.z = flap;\s*\}\);\s*\}"

new_animate_bird = """// 飛鳥群 8 字型立體盤旋飛行與扇動翅膀
    if (birdFlockData && birdFlockData.birds) {
      birdFlockData.birds.forEach((bird) => {
        const u = bird.userData;
        const t = elapsedTime * u.speed + u.offset;

        // 8 字型軌跡座標
        const x = Math.sin(t) * u.radiusX;
        const z = Math.sin(t * 2) * u.radiusZ;
        const y = u.height + Math.sin(t * 1.5) * 1.2;

        const nextT = t + 0.02;
        const nextX = Math.sin(nextT) * u.radiusX;
        const nextZ = Math.sin(nextT * 2) * u.radiusZ;
        const nextY = u.height + Math.sin(nextT * 1.5) * 1.2;

        bird.position.set(x, y, z);
        bird.lookAt(nextX, nextY, nextZ);

        // 雙翅上下拍動
        const wingFlap = Math.sin(elapsedTime * u.flapSpeed + u.offset) * 0.48;
        u.leftWing.rotation.z = wingFlap;
        u.rightWing.rotation.z = -wingFlap;
      });
    }"""

code = re.sub(animate_bird_pattern, new_animate_bird, code)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Implemented all labels display, lush vegetation, and 8-figure flying birds successfully.")
