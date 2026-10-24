import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. 調整相機預設位置，更接近示意圖的全景等角斜俯視角
code = re.sub(
    r"camera\.position\.set\([^)]+\);",
    "camera.position.set(0.2, 17.5, 29.8);",
    code
)
code = re.sub(
    r"cameraLookAt\.set\([^)]+\);",
    "cameraLookAt.set(0.2, 1.1, 0);",
    code
)

# 2. 升級 buildBridges() 成為真材實料的木紋拱橋與欄杆
bridges_code = """  // ══════════════════════════════════════════════════════════════════════
  // 8. 系統五：群島實體木棧道拱橋與欄杆 (Connecting Wooden Boardwalks)
  // ══════════════════════════════════════════════════════════════════════
  function buildBridges() {
    const bridgeConnections = [
      ['stomach', 'colon'],
      ['stomach', 'liver'],
      ['liver', 'endoscopy'],
      ['endoscopy', 'ultrasound'],
      ['stomach', 'drugs'],
      ['drugs', 'hypertension'],
      ['hypertension', 'hyperlipidemia'],
      ['hypertension', 'diabetes'],
      ['drugs', 'weight-loss'],
      ['diabetes', 'weight-loss'],
      ['weight-loss', 'nutrition'],
      ['nutrition', 'blood-tests'],
      ['stomach', 'exercise'],
      ['drugs', 'wealth-ladder'],
      ['wealth-ladder', 'six-neuro'],
      ['wealth-ladder', 'random-walk'],
      ['six-neuro', 'glucose-goddess'],
      ['glucose-goddess', 'die-with-zero'],
      ['random-walk', 'investing-pillars'],
      ['die-with-zero', 'investing-pillars'],
      ['die-with-zero', 'sapiens']
    ];

    const deckMat = new THREE.MeshStandardMaterial({
      color: 0x854d0e,
      roughness: 0.75,
      metalness: 0.1
    });
    const railMat = new THREE.MeshStandardMaterial({
      color: 0x451a03,
      roughness: 0.85
    });

    bridgeConnections.forEach(([idA, idB]) => {
      const objA = islandObjectsMap.get(idA);
      const objB = islandObjectsMap.get(idB);
      if (!objA || !objB) return;

      const pA = objA.position.clone().addScaledVector(objA.userData.normal, HEX_HEIGHT - 0.05);
      const pB = objB.position.clone().addScaledVector(objB.userData.normal, HEX_HEIGHT - 0.05);

      const dist = pA.distanceTo(pB);
      if (dist > 5.5) return;

      const mid = new THREE.Vector3().addVectors(pA, pB).multiplyScalar(0.5);
      const bridgeGroup = new THREE.Group();
      bridgeGroup.position.copy(mid);
      bridgeGroup.lookAt(pB);

      // 橋面 (寬度 0.62，微弧度)
      const deckGeo = new THREE.BoxGeometry(0.62, 0.07, dist * 0.76);
      const deckMesh = new THREE.Mesh(deckGeo, deckMat);
      deckMesh.castShadow = true;
      deckMesh.receiveShadow = true;
      bridgeGroup.add(deckMesh);

      // 兩側木質護欄小立柱
      const postCount = 3;
      const postGeo = new THREE.CylinderGeometry(0.02, 0.02, 0.18, 4);
      for (let i = -1; i <= 1; i++) {
        const pz = (i / 1.5) * (dist * 0.32);
        const postL = new THREE.Mesh(postGeo, railMat);
        postL.position.set(-0.29, 0.09, pz);
        bridgeGroup.add(postL);

        const postR = new THREE.Mesh(postGeo, railMat);
        postR.position.set(0.29, 0.09, pz);
        bridgeGroup.add(postR);
      }

      // 頂部扶手欄杆
      const handrailGeo = new THREE.BoxGeometry(0.04, 0.03, dist * 0.74);
      const handL = new THREE.Mesh(handrailGeo, railMat);
      handL.position.set(-0.29, 0.18, 0);
      bridgeGroup.add(handL);

      const handR = new THREE.Mesh(handrailGeo, railMat);
      handR.position.set(0.29, 0.18, 0);
      bridgeGroup.add(handR);

      bridgesGroup.add(bridgeGroup);
    });
  }"""

code = re.sub(
    r"// ══════════════════════════════════════════════════════════════════════\s*// 8\. 系統五：相鄰六角島嶼實體木棧道與跨星系大橋[\s\S]*?bridgesGroup\.add\(bridgeMesh\);\s*\}\);?\s*\}",
    bridges_code,
    code
)

# 3. 升級 CSS2D 標籤生成邏輯：微縮精巧 + 預設精選常駐
badge_logic_replacement = """      // 7. CSS2D 懸浮標籤 (精巧微型膠囊，預設精選 12 座核心島嶼常駐)
      const isFeatured = FEATURED_ISLANDS.has(island.id);
      const badgeDiv = document.createElement('div');
      badgeDiv.className = `island-3d-badge ${island.realm} ${isFeatured ? 'featured-label' : 'secondary-label'}`;
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

      const badgeObj = new CSS2DObject(badgeDiv);
      badgeObj.position.set(0, HEX_HEIGHT + 2.65, 0);
      group.add(badgeObj);
      group.userData.badgeDiv = badgeDiv;
      badgeObjects.push(badgeDiv);"""

code = re.sub(
    r"// 7\. CSS2D 懸浮標籤[\s\S]*?badgeObjects\.push\(badgeDiv\);",
    badge_logic_replacement,
    code
)

# 4. 更新 CSS 樣式：微縮膠囊、精選標籤常駐、次要標籤在 hover 或展開時顯示
badge_css_pattern = r"/\* ════════════ 3D 浮動標籤 \(CSS2D\) ════════════ \*/[\s\S]*?/\* ════════════ 左側：島嶼抽屜"

new_badge_css = """/* ════════════ 3D 浮動標籤 (CSS2D) ════════════ */
  :global(.island-3d-badge) {
    pointer-events: auto !important;
    cursor: pointer;
    transform: translate(-50%, -100%);
    transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.25s ease;
    user-select: none;
    opacity: 0;
    pointer-events: none;
  }

  :global(.island-3d-badge.featured-label) {
    opacity: 0.95;
    pointer-events: auto;
  }

  :global(.island-3d-badge.show-all-mode) {
    opacity: 0.92;
    pointer-events: auto;
  }

  :global(.island-3d-badge.hover-active),
  :global(.island-3d-badge.focus-active) {
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 60;
    transform: translate(-50%, -108%) scale(1.08);
  }

  :global(.island-3d-badge:hover) {
    transform: translate(-50%, -106%) scale(1.05);
    z-index: 55;
    opacity: 1 !important;
  }

  :global(.island-3d-badge-inner) {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 2.5px 5px 2.5px 8px;
    background: linear-gradient(135deg, rgba(34, 23, 24, 0.94), rgba(16, 12, 16, 0.97));
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 9999px;
    border: 1.2px solid rgba(224, 168, 115, 0.72);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.6), inset 0 1px 1.5px rgba(255, 230, 200, 0.3);
    color: #fcf8f2;
    white-space: nowrap;
    transition: all 0.2s ease;
  }

  :global(.island-3d-badge:hover .island-3d-badge-inner),
  :global(.island-3d-badge.focus-active .island-3d-badge-inner) {
    border-color: #f6c886;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.75), 0 0 12px rgba(246, 200, 134, 0.45);
  }

  :global(.badge-icon) {
    font-size: 0.88rem;
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.4));
  }

  :global(.badge-title) {
    font-size: 0.72rem;
    font-weight: 800;
    color: #fbf5ee;
    letter-spacing: 0.2px;
    text-shadow: 0 1px 2px rgba(0,0,0,0.8);
  }

  :global(.badge-pins-count) {
    font-size: 0.62rem;
    font-weight: 800;
    padding: 1.5px 6px;
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
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid rgba(20, 14, 18, 0.95);
    filter: drop-shadow(0 1px 2px rgba(0,0,0,0.4));
  }

  :global(.island-3d-badge.labels-hidden) {
    opacity: 0 !important;
    pointer-events: none !important;
  }

  /* ════════════ 左側：島嶼抽屜"""

code = re.sub(badge_css_pattern, new_badge_css, code)

# 5. 更新海洋材質為深海皇家湛藍色
code = re.sub(
    r"color:\s*0x144a75,",
    "color: 0x0a335c,",
    code
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Applied refined bridges, camera, ocean, and badges successfully.")
