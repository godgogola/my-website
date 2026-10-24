import re

with open('src/pages/island.astro', encoding='utf-8') as f:
    text = f.read()

# 1. 升級 CSS 標籤樣式 (深古銅金邊膠囊)
old_css_match = re.search(r'/\* ════════════ CSS2D 3D 懸浮標籤 ════════════ \*/[\s\S]*?/\* 隱藏標籤狀態 \*/', text)
if old_css_match:
    new_css = """/* ════════════ CSS2D 3D 懸浮標籤 (還原示意圖深古銅金邊膠囊) ════════════ */
  .island-3d-badge {
    position: absolute;
    pointer-events: auto;
    cursor: pointer;
    transform: translate(-50%, -100%);
    transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.3s ease;
  }

  .island-3d-badge:hover {
    transform: translate(-50%, -115%) scale(1.08);
  }

  .island-3d-badge-inner {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 14px;
    border-radius: 9999px;
    background: linear-gradient(135deg, rgba(34, 24, 18, 0.92) 0%, rgba(20, 14, 10, 0.96) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1.5px solid rgba(224, 168, 115, 0.75);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.55), inset 0 1px 2px rgba(255, 215, 175, 0.35);
    white-space: nowrap;
    user-select: none;
    color: #fdfaf6;
  }

  .island-3d-badge.health .island-3d-badge-inner {
    border-color: rgba(248, 165, 120, 0.85);
  }

  .island-3d-badge.wisdom .island-3d-badge-inner {
    border-color: rgba(186, 175, 255, 0.85);
  }

  .badge-icon {
    font-size: 1.15rem;
    line-height: 1;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
  }

  .badge-title {
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.3px;
    color: #ffffff;
    text-shadow: 0 1px 2px rgba(0,0,0,0.7);
  }

  .badge-pins-count {
    font-size: 0.72rem;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 9999px;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: #ffffff;
    box-shadow: 0 2px 6px rgba(217, 119, 6, 0.5);
  }

  .island-3d-badge.wisdom .badge-pins-count {
    background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
    box-shadow: 0 2px 6px rgba(109, 40, 217, 0.5);
  }

  .badge-arrow {
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 6px solid rgba(224, 168, 115, 0.85);
    margin: 0 auto;
    filter: drop-shadow(0 2px 3px rgba(0,0,0,0.45));
  }

  /* 隱藏標籤狀態 */"""
    text = text.replace(old_css_match.group(0), new_css)
    print("CSS_BADGE_STYLE_UPDATED")

# 2. 升級 buildIslands 加入巨石岩壁與拍岸浪花
island_loop_code = """      // 1. 六角島嶼頂層土壤/草皮 (Beveled Hexagon Cylinder)
      const hexGeo = new THREE.CylinderGeometry(HEX_RADIUS, HEX_RADIUS * 1.03, HEX_HEIGHT, 6, 1);
      const topMat = new THREE.MeshStandardMaterial({
        color: island.color,
        roughness: 0.72,
        metalness: 0.05,
        flatShading: true
      });
      const topMesh = new THREE.Mesh(hexGeo, topMat);
      topMesh.position.y = HEX_HEIGHT / 2;
      topMesh.castShadow = true;
      topMesh.receiveShadow = true;
      group.add(topMesh);

      // 2. 六角天然海蝕巨石岩壁 (Rocky Cliff Base) - 徹底取代平滑幾何感
      addRockyCliffBase(group, island);

      // 3. 雙層拍岸白浪花光環
      createShoreFoamRings(group);

      // 4. 島嶼地表微縮村落與專屬地標模型
      populateMiniatureCity(group, island);"""

text = re.sub(
    r'      // 1\. 六角島嶼頂層土壤/草皮[\s\S]*?populateMiniatureCity\(group, island\);',
    island_loop_code,
    text
)

# 3. 實作天然岩壁 addRockyCliffBase、拍岸浪花 createShoreFoamRings、毛線小羊 createAmigurumiSheep
helper_funcs = """
  // ── 天然海蝕巨石岩壁 (還原示意圖真實海島多面切削岩體) ──
  function addRockyCliffBase(group, island) {
    const rockMat1 = new THREE.MeshStandardMaterial({ color: 0x54463a, roughness: 0.95, flatShading: true });
    const rockMat2 = new THREE.MeshStandardMaterial({ color: 0x6e5a4c, roughness: 0.9, flatShading: true });
    const rockMat3 = new THREE.MeshStandardMaterial({ color: 0x3d322a, roughness: 0.95, flatShading: true });
    const mats = [rockMat1, rockMat2, rockMat3];

    // 環繞 14 顆隨機刀削巨石
    for (let i = 0; i < 14; i++) {
      const angle = (i / 14) * Math.PI * 2 + (Math.random() * 0.15 - 0.075);
      const dist = HEX_RADIUS * (0.86 + Math.random() * 0.22);
      const rx = Math.cos(angle) * dist;
      const rz = Math.sin(angle) * dist;
      const ry = -0.42 - Math.random() * 0.38;

      const rockRadius = 0.52 + Math.random() * 0.42;
      const rockGeo = new THREE.DodecahedronGeometry(rockRadius, 0);
      
      // 隨機擾動頂點形成天然海蝕裂紋
      const posAttr = rockGeo.attributes.position;
      for (let p = 0; p < posAttr.count; p++) {
        const vx = posAttr.getX(p) + (Math.random() - 0.5) * 0.12;
        const vy = posAttr.getY(p) * (0.85 + Math.random() * 0.3);
        const vz = posAttr.getZ(p) + (Math.random() - 0.5) * 0.12;
        posAttr.setXYZ(p, vx, vy, vz);
      }
      rockGeo.computeVertexNormals();

      const rockMesh = new THREE.Mesh(rockGeo, mats[i % 3]);
      rockMesh.position.set(rx, ry, rz);
      rockMesh.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
      rockMesh.castShadow = true;
      rockMesh.receiveShadow = true;
      group.add(rockMesh);
    }
  }

  // ── 雙層拍岸白浪花光環 ──
  function createShoreFoamRings(group) {
    const foamMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.42,
      side: THREE.DoubleSide
    });
    const ringGeo = new THREE.RingGeometry(HEX_RADIUS * 1.02, HEX_RADIUS * 1.14, 24);
    const foam = new THREE.Mesh(ringGeo, foamMat);
    foam.rotation.x = -Math.PI / 2;
    foam.position.y = -0.08;
    group.add(foam);
  }

  // ── 可愛毛線小羊 (示意圖專屬生物) ──
  function createAmigurumiSheep(group, x, z, scale = 0.35) {
    const sheepGroup = new THREE.Group();
    sheepGroup.position.set(x, HEX_HEIGHT + 0.12, z);
    sheepGroup.scale.setScalar(scale);

    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xfaf8f5, roughness: 0.95, flatShading: true });
    const faceMat = new THREE.MeshStandardMaterial({ color: 0x221f1d, roughness: 0.8 });

    // 蓬鬆毛線身體
    const body = new THREE.Mesh(new THREE.DodecahedronGeometry(0.38, 1), bodyMat);
    body.position.y = 0.32;
    body.scale.set(1.15, 0.9, 0.9);
    body.castShadow = true;
    sheepGroup.add(body);

    // 黑小臉
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 8), faceMat);
    head.position.set(0.35, 0.42, 0);
    sheepGroup.add(head);

    // 四隻細黑腿
    const legGeo = new THREE.CylinderGeometry(0.03, 0.03, 0.22, 5);
    const legPositions = [
      [0.18, 0.11, 0.16],
      [0.18, 0.11, -0.16],
      [-0.18, 0.11, 0.16],
      [-0.18, 0.11, -0.16]
    ];
    legPositions.forEach(([lx, ly, lz]) => {
      const leg = new THREE.Mesh(legGeo, faceMat);
      leg.position.set(lx, ly, lz);
      sheepGroup.add(leg);
    });

    group.add(sheepGroup);
  }
"""

if 'function addRockyCliffBase' not in text:
    pos = text.find('function populateMiniatureCity(')
    if pos != -1:
        text = text[:pos] + helper_funcs + "\n\n  " + text[pos:]
        print("ADDED_CLIFF_AND_SHEEP_HELPERS")

# 4. 全新升級 populateMiniatureCity (依 landmark 生成燈塔、教堂尖塔鐘樓、圓頂涼亭、童話小屋、小羊、樹木花叢)
new_city_code = """  // 微縮城市建築生成 (完全依示意圖豐富度打造)
  function populateMiniatureCity(group, island) {
    const isWisdom = island.realm === 'wisdom';
    const mainRoofColor = island.roofColor;
    const landmark = island.landmark || (isWisdom ? 'gazebo' : 'cottage');

    const wallMat = new THREE.MeshStandardMaterial({ color: 0xfdfbf7, roughness: 0.65 });
    const darkWoodMat = new THREE.MeshStandardMaterial({ color: 0x5c4033, roughness: 0.85 });

    // ── 1. 核心地標 (Landmark) ──
    if (landmark === 'lighthouse') {
      // 經典白色燈塔 (白色錐柱 + 觀景台 + 透光發光室 + 綠/青圓頂)
      const tower = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.44, 1.65, 8), wallMat);
      tower.position.set(0, HEX_HEIGHT + 0.82, 0);
      tower.castShadow = true;
      group.add(tower);

      const balc = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.08, 8), darkWoodMat);
      balc.position.set(0, HEX_HEIGHT + 1.68, 0);
      group.add(balc);

      const lamp = new THREE.Mesh(
        new THREE.CylinderGeometry(0.24, 0.24, 0.28, 8),
        new THREE.MeshStandardMaterial({ color: 0xfffbeb, emissive: 0xfef08a, emissiveIntensity: 0.9 })
      );
      lamp.position.set(0, HEX_HEIGHT + 1.84, 0);
      group.add(lamp);

      const dome = new THREE.Mesh(
        new THREE.SphereGeometry(0.28, 8, 8),
        new THREE.MeshStandardMaterial({ color: 0x0f766e, roughness: 0.3 })
      );
      dome.position.set(0, HEX_HEIGHT + 2.02, 0);
      group.add(dome);
    } else if (landmark === 'church') {
      // 尖頂教堂鐘樓高塔 (白色方柱 + 雙拱窗 + 陡峭紅瓦斜角錐)
      const tower = new THREE.Mesh(new THREE.BoxGeometry(0.72, 1.45, 0.72), wallMat);
      tower.position.set(0, HEX_HEIGHT + 0.72, 0);
      tower.castShadow = true;
      group.add(tower);

      const roofMat = new THREE.MeshStandardMaterial({ color: mainRoofColor, roughness: 0.5 });
      const spire = new THREE.Mesh(new THREE.ConeGeometry(0.58, 0.95, 4), roofMat);
      spire.rotation.y = Math.PI / 4;
      spire.position.set(0, HEX_HEIGHT + 1.45 + 0.48, 0);
      spire.castShadow = true;
      group.add(spire);

      // 小鐘樓基座台階
      const steps = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.14, 0.95), wallMat);
      steps.position.set(0, HEX_HEIGHT + 0.07, 0);
      group.add(steps);
    } else if (landmark === 'gazebo') {
      // 羅馬古典圓柱涼亭 (6根立柱 + 圓頂 + 薰衣草花圃)
      const baseFloor = new THREE.Mesh(new THREE.CylinderGeometry(0.68, 0.72, 0.1, 8), wallMat);
      baseFloor.position.set(0, HEX_HEIGHT + 0.05, 0);
      group.add(baseFloor);

      const colGeo = new THREE.CylinderGeometry(0.045, 0.045, 0.65, 6);
      for (let i = 0; i < 6; i++) {
        const ca = (i / 6) * Math.PI * 2;
        const col = new THREE.Mesh(colGeo, wallMat);
        col.position.set(Math.cos(ca) * 0.52, HEX_HEIGHT + 0.42, Math.sin(ca) * 0.52);
        group.add(col);
      }

      const domeMat = new THREE.MeshStandardMaterial({ color: island.accentColor || 0x2dd4bf, roughness: 0.35 });
      const dome = new THREE.Mesh(new THREE.SphereGeometry(0.58, 12, 8, 0, Math.PI * 2, 0, Math.PI * 0.5), domeMat);
      dome.position.set(0, HEX_HEIGHT + 0.75, 0);
      group.add(dome);
    } else {
      // 童話小屋 (雙斜屋頂 + 煙囪 + 發光窗戶)
      const house = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.65, 0.75), wallMat);
      house.position.set(0, HEX_HEIGHT + 0.32, 0);
      house.castShadow = true;
      group.add(house);

      const roofMat = new THREE.MeshStandardMaterial({ color: mainRoofColor, roughness: 0.55 });
      const roof = new THREE.Mesh(new THREE.ConeGeometry(0.68, 0.45, 4), roofMat);
      roof.rotation.y = Math.PI / 4;
      roof.scale.set(1.3, 1, 1.15);
      roof.position.set(0, HEX_HEIGHT + 0.65 + 0.22, 0);
      roof.castShadow = true;
      group.add(roof);

      const chimney = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.35, 0.14), darkWoodMat);
      chimney.position.set(0.24, HEX_HEIGHT + 0.95, 0.14);
      group.add(chimney);
    }

    // ── 2. 毛線小羊 (示意圖專屬可愛生物) ──
    createAmigurumiSheep(group, 0.75, 0.55, 0.32);
    if (Math.random() > 0.4) {
      createAmigurumiSheep(group, -0.68, -0.45, 0.28);
    }

    // ── 3. 綠植與樹木 (松樹與多球闊葉樹) ──
    const treeMat1 = new THREE.MeshStandardMaterial({ color: 0x15803d, roughness: 0.8, flatShading: true });
    const treeMat2 = new THREE.MeshStandardMaterial({ color: 0x166534, roughness: 0.85, flatShading: true });
    const trunkMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.9 });

    const treePositions = [
      [-0.85, 0.45],
      [0.85, -0.52],
      [-0.42, 0.95],
      [0.62, 0.88]
    ];
    treePositions.forEach(([tx, tz], idx) => {
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 0.45, 5), trunkMat);
      trunk.position.set(tx, HEX_HEIGHT + 0.22, tz);
      group.add(trunk);

      if (idx % 2 === 0) {
        // 多層聖誕松樹
        const foliage = new THREE.Mesh(new THREE.ConeGeometry(0.38, 0.75, 5), treeMat1);
        foliage.position.set(tx, HEX_HEIGHT + 0.58, tz);
        foliage.castShadow = true;
        group.add(foliage);
      } else {
        // 蓬鬆闊葉球樹
        const foliage = new THREE.Mesh(new THREE.DodecahedronGeometry(0.34, 1), treeMat2);
        foliage.position.set(tx, HEX_HEIGHT + 0.52, tz);
        foliage.castShadow = true;
        group.add(foliage);
      }
    });

    // ── 4. 花圃彩色小圓點 ──
    const flowerColors = [0xf43f5e, 0xfbbf24, 0xa855f7, 0x38bdf8];
    for (let f = 0; f < 6; f++) {
      const fMat = new THREE.MeshBasicMaterial({ color: flowerColors[f % flowerColors.length] });
      const fMesh = new THREE.Mesh(new THREE.SphereGeometry(0.065, 4, 4), fMat);
      const fa = Math.random() * Math.PI * 2;
      const fd = 0.8 + Math.random() * 0.7;
      fMesh.position.set(Math.cos(fa) * fd, HEX_HEIGHT + 0.04, Math.sin(fa) * fd);
      group.add(fMesh);
    }
  }"""

# 替換 populateMiniatureCity
text = re.sub(
    r'  // 微縮城市建築生成[\s\S]*?group\.add\(fMesh\);\s*\}\s*\}',
    new_city_code,
    text
)

with open('src/pages/island.astro', 'w', encoding='utf-8') as f:
    f.write(text)

print("DIORAMA_UPGRADE_COMPLETE_SUCCESS")
