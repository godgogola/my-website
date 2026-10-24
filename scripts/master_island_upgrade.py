import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# ─────────────────────────────────────────────────────────────────────────────
# 1. CSS 升級：全 23 島嶼標籤 100% 預設顯示，微縮精緻膠囊徽章
# ─────────────────────────────────────────────────────────────────────────────
new_css = """/* ════════════ 3D 浮動標籤 (CSS2D) ════════════ */
  :global(.island-3d-badge) {
    pointer-events: auto !important;
    cursor: pointer;
    transform: translate(-50%, -100%);
    transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.2s ease, filter 0.2s ease;
    user-select: none;
    opacity: 0.94 !important; /* 全 23 座島嶼標籤 100% 預設顯示 */
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
    font-size: 0.82rem;
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.5));
  }

  :global(.badge-title) {
    font-size: 0.68rem;
    font-weight: 800;
    color: #fbf5ee;
    letter-spacing: 0.2px;
    text-shadow: 0 1px 2px rgba(0,0,0,0.85);
  }

  :global(.badge-pins-count) {
    font-size: 0.6rem;
    font-weight: 800;
    padding: 1px 4px;
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
    border-left: 3.5px solid transparent;
    border-right: 3.5px solid transparent;
    border-top: 4.5px solid rgba(20, 14, 18, 0.95);
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.4));
  }

  :global(.island-3d-badge.labels-hidden) {
    display: none !important;
  }"""

code = re.sub(
    r"/\* ════════════ 3D 浮動標籤 \(CSS2D\) ════════════ \*/[\s\S]*?:global\(\.island-3d-badge\.labels-hidden\) \{\s*display: none !important;\s*\}",
    new_css,
    code
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. 標籤錯落高度：依前後排（r 座標）分層，徹底解決重疊遮擋
# ─────────────────────────────────────────────────────────────────────────────
badge_create_pattern = r"// 7\. CSS2D 懸浮標籤[\s\S]*?badgeObjects\.push\(badgeDiv\);"
new_badge_logic = """// 7. CSS2D 懸浮標籤 (所有 23 座島嶼 100% 顯示，依前中後排階梯錯落高度，不互相遮擋)
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

      // 錯落高度分層：
      // 前排 (r > 0)：高度 +2.15，清晰浮現於前景不擋後排
      // 中排 (r === 0)：高度 +2.65
      // 後排 (r < 0)：高度 +3.15
      // 燈塔與鐘樓地標加高避開尖頂
      let badgeHeight = HEX_HEIGHT + 2.65;
      if (island.r > 0) badgeHeight = HEX_HEIGHT + 2.15;
      else if (island.r < 0) badgeHeight = HEX_HEIGHT + 3.15;

      if (island.id === 'endoscopy') badgeHeight = HEX_HEIGHT + 3.45;
      if (island.id === 'hypertension' || island.id === 'wealth-ladder') badgeHeight = HEX_HEIGHT + 3.35;

      const badgeObj = new CSS2DObject(badgeDiv);
      badgeObj.position.set(0, badgeHeight, 0);
      group.add(badgeObj);
      group.userData.badgeDiv = badgeDiv;
      badgeObjects.push(badgeDiv);"""

code = re.sub(badge_create_pattern, new_badge_logic, code)

# ─────────────────────────────────────────────────────────────────────────────
# 3. 植被升級：蓬鬆多球樹冠 + 多層圓錐松樹 + 繽紛彩色花叢
# ─────────────────────────────────────────────────────────────────────────────
veg_helpers = """  // 蓬鬆多球體落葉樹冠 (Fluffy Cloud Tree)
  function createFluffyTree(x, z, leafColor) {
    const treeGroup = new THREE.Group();
    treeGroup.position.set(x, HEX_HEIGHT, z);

    const trunk = new THREE.Mesh(
      new THREE.CylinderGeometry(0.065, 0.095, 0.45, 6),
      new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.9 })
    );
    trunk.position.y = 0.22;
    trunk.castShadow = true;
    treeGroup.add(trunk);

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

  // 多層次圓錐松樹 (Tiered Evergreen Pine)
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
    [[0.32, 0.42, 0.34], [0.24, 0.34, 0.54], [0.15, 0.26, 0.72]].forEach(([r, h, py]) => {
      const cone = new THREE.Mesh(new THREE.ConeGeometry(r, h, 6), pineMat);
      cone.position.y = py;
      cone.castShadow = true;
      pineGroup.add(cone);
    });

    return pineGroup;
  }

  // 微型彩色花叢球 (Colorful Scatter Flower Tufts)
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

code = re.sub(
    r"(// 可愛毛線小羊 \(Amigurumi Sheep\))",
    veg_helpers + "\n\\1",
    code
)

# 替換 populateMiniatureCity 內的點綴配景
city_pop_pattern = r"// 周邊點綴配景：副屋、小樹、花叢、小路燈與可愛綿羊[\s\S]*?group\.add\(flowerCluster\);\s*\}\s*\}\);"

new_city_pop = """// 周邊點綴配景：副屋、蓬鬆樹木、松樹、花叢、小路燈與可愛綿羊
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
        const tColor = isWisdom ? 0x8b5cf6 : (islandIdx % 2 === 0 ? 0x16a34a : 0x22c55e);
        group.add(createFluffyTree(pos.x, pos.z, tColor));
      } else if (pos.type === 'pine') {
        group.add(createPineTree(pos.x, pos.z));
      } else if (pos.type === 'lamp') {
        group.add(createMiniStreetLamp(pos.x, pos.z));
      } else if (pos.type === 'sheep') {
        group.add(createAmigurumiSheep(pos.x, pos.z, Math.random() * Math.PI * 2));
      } else if (pos.type === 'flowers') {
        group.add(createFlowerTufts(pos.x, pos.z, islandIdx + idx));
      }
    });"""

code = re.sub(city_pop_pattern, new_city_pop, code)

# ─────────────────────────────────────────────────────────────────────────────
# 4. 空中飛鳥 + 地面微型膠囊小人與白色小動物 (走動 + 彈跳動畫)
# ─────────────────────────────────────────────────────────────────────────────
bird_and_creatures = """  // ══════════════════════════════════════════════════════════════════════
  // 動態空中盤旋飛鳥群 (8字型/圓形盤旋 + V字翅膀拍動)
  // ══════════════════════════════════════════════════════════════════════
  let birdFlockData = null;

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

      const leftWingGeo = new THREE.BufferGeometry();
      const lwVerts = new Float32Array([0, 0, 0, -0.38, 0.08, -0.06, -0.28, 0, 0.15]);
      leftWingGeo.setAttribute('position', new THREE.BufferAttribute(lwVerts, 3));
      leftWingGeo.computeVertexNormals();
      const leftWing = new THREE.Mesh(leftWingGeo, wingMat);

      const rightWingGeo = new THREE.BufferGeometry();
      const rwVerts = new Float32Array([0, 0, 0, 0.38, 0.08, -0.06, 0.28, 0, 0.15]);
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

  // ══════════════════════════════════════════════════════════════════════
  // 10. 地面漫步小人與小動物 (Autonomous Capsule Walkers & White Animals)
  // ══════════════════════════════════════════════════════════════════════
  function spawnWalkers() {
    const totalWalkers = 18;
    const walkerColors = [0x3b82f6, 0xef4444, 0x10b981, 0xf59e0b, 0x8b5cf6, 0xec4899, 0x06b6d4];

    // 1. 微型膠囊體小人 (頭 + 身體 + 輕微彈跳走路)
    for (let i = 0; i < totalWalkers; i++) {
      const walkerGroup = new THREE.Group();

      const bodyGeo = new THREE.CylinderGeometry(0.065, 0.085, 0.20, 8);
      const bodyMat = new THREE.MeshStandardMaterial({
        color: walkerColors[i % walkerColors.length],
        roughness: 0.65
      });
      const body = new THREE.Mesh(bodyGeo, bodyMat);
      body.position.y = 0.12;
      body.castShadow = true;
      walkerGroup.add(body);

      const headGeo = new THREE.SphereGeometry(0.075, 8, 8);
      const headMat = new THREE.MeshStandardMaterial({ color: 0xffedd5, roughness: 0.8 });
      const head = new THREE.Mesh(headGeo, headMat);
      head.position.y = 0.26;
      head.castShadow = true;
      walkerGroup.add(head);

      const island = ISLAND_DATA[i % ISLAND_DATA.length];
      const islandObj = islandObjectsMap.get(island.id);
      if (islandObj) {
        walkerGroup.position.copy(islandObj.position).addScaledVector(islandObj.userData.normal, HEX_HEIGHT);
        walkerGroup.quaternion.copy(islandObj.quaternion);
      }
      walkersGroup.add(walkerGroup);

      walkers.push({
        type: 'human',
        group: walkerGroup,
        baseMesh: body,
        headMesh: head,
        currentIsland: island.id,
        targetPos: walkerGroup.position.clone(),
        speed: 0.012 + Math.random() * 0.012,
        pauseTicks: 0,
        seed: Math.random() * 100
      });
    }

    // 2. 白色小動物 (小羊/小狗，由小方塊與圓球組成，在草地上漫步覓食)
    const animalCount = 14;
    for (let i = 0; i < animalCount; i++) {
      const animalGroup = new THREE.Group();
      const isDog = (i % 2 === 0);

      if (isDog) {
        const dBody = new THREE.Mesh(
          new THREE.BoxGeometry(0.18, 0.12, 0.12),
          new THREE.MeshStandardMaterial({ color: 0xfef9c3, roughness: 0.85 })
        );
        dBody.position.y = 0.09;
        dBody.castShadow = true;
        animalGroup.add(dBody);

        const dHead = new THREE.Mesh(
          new THREE.BoxGeometry(0.09, 0.09, 0.09),
          new THREE.MeshStandardMaterial({ color: 0xfef08a, roughness: 0.85 })
        );
        dHead.position.set(0.1, 0.15, 0);
        dHead.castShadow = true;
        animalGroup.add(dHead);

        const dTail = new THREE.Mesh(
          new THREE.CylinderGeometry(0.015, 0.015, 0.08, 4),
          new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.9 })
        );
        dTail.position.set(-0.1, 0.14, 0);
        dTail.rotation.z = Math.PI / 4;
        animalGroup.add(dTail);
      } else {
        const sBody = new THREE.Mesh(
          new THREE.DodecahedronGeometry(0.11, 1),
          new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.95 })
        );
        sBody.position.y = 0.10;
        sBody.castShadow = true;
        animalGroup.add(sBody);

        const sHead = new THREE.Mesh(
          new THREE.SphereGeometry(0.05, 6, 6),
          new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.9 })
        );
        sHead.position.set(0.09, 0.13, 0);
        animalGroup.add(sHead);
      }

      const island = ISLAND_DATA[(i * 3 + 2) % ISLAND_DATA.length];
      const islandObj = islandObjectsMap.get(island.id);
      if (islandObj) {
        animalGroup.position.copy(islandObj.position).addScaledVector(islandObj.userData.normal, HEX_HEIGHT);
        animalGroup.quaternion.copy(islandObj.quaternion);
      }
      walkersGroup.add(animalGroup);

      walkers.push({
        type: isDog ? 'dog' : 'sheep',
        group: animalGroup,
        currentIsland: island.id,
        targetPos: animalGroup.position.clone(),
        speed: 0.008 + Math.random() * 0.008,
        pauseTicks: Math.floor(Math.random() * 60),
        seed: Math.random() * 100
      });
    }
  }

  function updateWalkers() {
    if (!showWalkers) return;
    const time = clock ? clock.getElapsedTime() : 0;

    walkers.forEach((w) => {
      if (w.pauseTicks > 0) {
        w.pauseTicks--;
        if (w.type === 'sheep') {
          w.group.rotation.y += Math.sin(time * 3 + w.seed) * 0.008;
        }
        return;
      }

      const curPos = w.group.position;
      const dist = curPos.distanceTo(w.targetPos);

      if (dist < 0.12) {
        w.pauseTicks = Math.floor(60 + Math.random() * 140);

        const island = islandObjectsMap.get(w.currentIsland);
        if (island) {
          const origin = island.position;
          const normal = island.userData.normal;
          const tangent = new THREE.Vector3(1, 0, 0).cross(normal).normalize();
          const bitangent = new THREE.Vector3().crossVectors(normal, tangent).normalize();

          const angle = Math.random() * Math.PI * 2;
          const r = 0.35 + Math.random() * 0.95;
          w.targetPos.copy(origin)
            .addScaledVector(tangent, Math.cos(angle) * r)
            .addScaledVector(bitangent, Math.sin(angle) * r)
            .addScaledVector(normal, HEX_HEIGHT);
        }
      } else {
        const dir = new THREE.Vector3().subVectors(w.targetPos, curPos).normalize();
        curPos.addScaledVector(dir, w.speed);
        w.group.lookAt(w.targetPos.clone().add(dir));

        const bounceFreq = (w.type === 'human') ? 8.5 : 10.0;
        const bounceAmp = (w.type === 'human') ? 0.045 : 0.025;
        const bounce = Math.abs(Math.sin(time * bounceFreq + w.seed)) * bounceAmp;

        const island = islandObjectsMap.get(w.currentIsland);
        if (island) {
          const groundPos = island.position.clone().addScaledVector(island.userData.normal, HEX_HEIGHT + bounce);
          curPos.y = groundPos.y;
        }
      }
    });
  }"""

walkers_original_pattern = r"// ══════════════════════════════════════════════════════════════════════\s*// 10\. 漫步微型小人[\s\S]*?function updateWalkers\(\) \{[\s\S]*?\}\s*\}\s*\}"

code = re.sub(walkers_original_pattern, bird_and_creatures, code)

# 在 setupLightingAndCelestial 中初始化飛鳥
code = re.sub(
    r"(createMasterpieceSkyDome\(\);)",
    "\\1\n    birdFlockData = createBirdFlock();",
    code
)

# 在 animate 函數中加入飛鳥 8 字盤旋更新
animate_birds_call = """    // 飛鳥群 8 字型立體盤旋飛行與扇動翅膀
    if (birdFlockData && birdFlockData.birds) {
      birdFlockData.birds.forEach((bird) => {
        const u = bird.userData;
        const t = elapsedTime * u.speed + u.offset;

        const x = Math.sin(t) * u.radiusX;
        const z = Math.sin(t * 2) * u.radiusZ;
        const y = u.height + Math.sin(t * 1.5) * 1.2;

        const nextT = t + 0.02;
        const nextX = Math.sin(nextT) * u.radiusX;
        const nextZ = Math.sin(nextT * 2) * u.radiusZ;
        const nextY = u.height + Math.sin(nextT * 1.5) * 1.2;

        bird.position.set(x, y, z);
        bird.lookAt(nextX, nextY, nextZ);

        const wingFlap = Math.sin(elapsedTime * u.flapSpeed + u.offset) * 0.48;
        u.leftWing.rotation.z = wingFlap;
        u.rightWing.rotation.z = -wingFlap;
      });
    }"""

code = re.sub(
    r"(updateWalkers\(\);)",
    animate_birds_call + "\n\n    \\1",
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Master upgrade applied successfully!")
