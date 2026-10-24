import re

with open('src/pages/island.astro', encoding='utf-8') as f:
    text = f.read()

# 1. 調整島嶼半徑與間隔 (島放大、間隔加大、相機拉開)
old_dim = """  const SPACING = 2.45;       // 六角中心間距
  const HEX_RADIUS = 2.06;    // 六角島嶼半徑
  const HEX_HEIGHT = 0.72;    // 島嶼土壤高度
  const PLANET_RADIUS = 34.0; // 地球星球半徑 (決定地平線弧度的黃金比例)"""

new_dim = """  const SPACING = 3.85;       // 六角中心間距 (間隔加大，留出舒展蔚藍海峽)
  const HEX_RADIUS = 2.85;    // 六角島嶼半徑 (島嶼放大，氣派壯闊)
  const HEX_HEIGHT = 0.85;    // 島嶼土壤高度
  const PLANET_RADIUS = 52.0; // 地球星球半徑 (舒展大弧度)"""

text = text.replace(old_dim, new_dim)

# 調整初始相機與目標飛行距離
text = re.sub(
    r'camera\.position\.set\(2\.1, 18, 22\);',
    'camera.position.set(2.1, 28, 36);',
    text
)
text = re.sub(
    r'let cameraDestPos = new THREE\.Vector3\(2\.1, 17, 21\);',
    'let cameraDestPos = new THREE.Vector3(2.1, 28, 36);',
    text
)
text = re.sub(
    r'controls\.maxDistance = 45;',
    'controls.maxDistance = 85;',
    text
)

# 2. 升級 buildBridges：連接 24 座島嶼，並在橋身兩側增加夜間發光小路燈
new_build_bridges = """  // ══════════════════════════════════════════════════════════════════════
  // 連接群島木橋系統 (含橋上夜間發光路燈)
  // ══════════════════════════════════════════════════════════════════════
  function buildBridges() {
    // 24 座主題島嶼相鄰網絡連接
    const BRIDGE_PAIRS = [
      // 醫學專科島內部互連
      ['endoscopy', 'stomach'],
      ['endoscopy', 'intestine'],
      ['endoscopy', 'medication'],
      ['endoscopy', 'ultrasound'],
      ['stomach', 'intestine'],
      ['stomach', 'hepatitis'],
      ['hepatitis', 'liver-biliary'],
      ['stomach', 'liver-biliary'],
      ['intestine', 'weight-loss'],
      ['weight-loss', 'diet'],
      ['weight-loss', 'diabetes'],
      ['weight-loss', 'exercise'],
      ['diabetes', 'lipids'],
      ['lipids', 'hypertension'],
      ['lipids', 'health-red'],
      ['health-red', 'health-check'],
      ['health-red', 'chronic'],
      ['diabetes', 'chronic'],
      // 跨界大天橋 (Grand Cross-Realm Bridges)
      ['diabetes', 'wealth-ladder'],
      ['weight-loss', 'random-walk'],
      ['health-red', 'most-important'],
      // 知識宇宙島互連
      ['wealth-ladder', 'random-walk'],
      ['wealth-ladder', 'golden-rules'],
      ['wealth-ladder', 'most-important'],
      ['random-walk', 'golden-rules'],
      ['random-walk', 'die-with-zero'],
      ['golden-rules', 'most-important'],
      ['golden-rules', 'glucose'],
      ['die-with-zero', 'glucose'],
      ['most-important', 'brain-neuro'],
      ['glucose', 'sapiens'],
      ['brain-neuro', 'sapiens']
    ];

    BRIDGE_PAIRS.forEach(([idA, idB]) => {
      const objA = islandObjectsMap.get(idA);
      const objB = islandObjectsMap.get(idB);
      if (!objA || !objB) return;

      const pA = objA.position;
      const pB = objB.position;
      const isCrossRealm = (objA.userData.islandData.realm !== objB.userData.islandData.realm);

      const mid = new THREE.Vector3().addVectors(pA, pB).multiplyScalar(0.5);
      const radialDir = new THREE.Vector3().subVectors(mid, PLANET_CENTER).normalize();
      const dist = pA.distanceTo(pB);

      mid.copy(PLANET_CENTER).addScaledVector(radialDir, PLANET_RADIUS + HEX_HEIGHT + (isCrossRealm ? 0.22 : 0.12));

      const bridgeGroup = new THREE.Group();
      bridgeGroup.position.copy(mid);

      const forward = new THREE.Vector3().subVectors(pB, pA).normalize();
      const up = radialDir;
      const right = new THREE.Vector3().crossVectors(up, forward).normalize();
      const realUp = new THREE.Vector3().crossVectors(forward, right).normalize();
      const mat4 = new THREE.Matrix4().makeBasis(forward, realUp, right);
      bridgeGroup.quaternion.setFromRotationMatrix(mat4);

      const bridgeLen = dist * 0.44;
      const bridgeWidth = isCrossRealm ? 0.95 : 0.72;

      // 橋面主體
      const archGeo = new THREE.BoxGeometry(bridgeLen, 0.2, bridgeWidth);
      const archMat = new THREE.MeshStandardMaterial({
        color: isCrossRealm ? 0xfcd34d : 0xecdfcc,
        roughness: 0.65,
        metalness: isCrossRealm ? 0.35 : 0.08
      });
      const arch = new THREE.Mesh(archGeo, archMat);
      arch.castShadow = true;
      arch.receiveShadow = true;
      bridgeGroup.add(arch);

      // 橋兩側護欄
      const railGeo = new THREE.BoxGeometry(bridgeLen, 0.14, 0.08);
      const railMat = new THREE.MeshStandardMaterial({ color: 0x6e523e, roughness: 0.8 });
      const railL = new THREE.Mesh(railGeo, railMat);
      railL.position.set(0, 0.16, bridgeWidth / 2 - 0.04);
      bridgeGroup.add(railL);

      const railR = new THREE.Mesh(railGeo, railMat);
      railR.position.set(0, 0.16, -bridgeWidth / 2 + 0.04);
      bridgeGroup.add(railR);

      // 橋上夜間發光小路燈 (橋頭兩側各 2 盞)
      const poleGeo = new THREE.CylinderGeometry(0.035, 0.04, 0.35, 5);
      const poleMat = new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.6 });
      const bulbGeo = new THREE.SphereGeometry(0.09, 8, 8);

      const lampPositions = [
        [-bridgeLen * 0.35, bridgeWidth / 2 + 0.02],
        [-bridgeLen * 0.35, -bridgeWidth / 2 - 0.02],
        [bridgeLen * 0.35, bridgeWidth / 2 + 0.02],
        [bridgeLen * 0.35, -bridgeWidth / 2 - 0.02]
      ];

      lampPositions.forEach(([lx, lz]) => {
        const pole = new THREE.Mesh(poleGeo, poleMat);
        pole.position.set(lx, 0.24, lz);
        bridgeGroup.add(pole);

        const bulb = new THREE.Mesh(bulbGeo, nightGlowMaterial);
        bulb.position.set(lx, 0.44, lz);
        bridgeGroup.add(bulb);
      });

      bridgesGroup.add(bridgeGroup);
    });
  }"""

# 替換 buildBridges 函數
text = re.sub(
    r'  function buildBridges\(\) \{[\s\S]*?bridgesGroup\.add\(bridgeGroup\);\s*\}\);\s*\}',
    new_build_bridges,
    text
)

# 3. 升級 populateMiniatureCity：在島嶼上新增路燈，並讓建築物窗戶/透光室共用 nightGlowMaterial 開燈
streetlamp_code = """    // ── 5. 島嶼邊緣夜間發光小路燈 (Streetlamps) ──
    const streetlampPoleGeo = new THREE.CylinderGeometry(0.045, 0.055, 0.72, 6);
    const streetlampPoleMat = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.6 });
    const streetlampBulbGeo = new THREE.SphereGeometry(0.12, 8, 8);

    const lampCoords = [
      [HEX_RADIUS * 0.62, HEX_RADIUS * 0.35],
      [-HEX_RADIUS * 0.58, -HEX_RADIUS * 0.42],
      [0.0, -HEX_RADIUS * 0.72]
    ];
    lampCoords.forEach(([lx, lz]) => {
      const pole = new THREE.Mesh(streetlampPoleGeo, streetlampPoleMat);
      pole.position.set(lx, HEX_HEIGHT + 0.36, lz);
      pole.castShadow = true;
      group.add(pole);

      const bulb = new THREE.Mesh(streetlampBulbGeo, nightGlowMaterial);
      bulb.position.set(lx, HEX_HEIGHT + 0.75, lz);
      group.add(bulb);
    });"""

# 在 populateMiniatureCity 末尾加入路燈生成
pos_city_end = text.find('// ── 4. 花圃彩色小圓點 ──')
if pos_city_end != -1:
    pos_brace = text.find('group.add(fMesh);\n    }\n  }', pos_city_end)
    if pos_brace != -1:
        insert_target = 'group.add(fMesh);\n    }\n\n' + streetlamp_code + '\n  }'
        text = text[:pos_brace] + insert_target + text[pos_brace + len('group.add(fMesh);\n    }\n  }'):]
        print("ADDED_STREETLAMPS_TO_ISLANDS")

# 4. 升級星空與銀河：4,000 顆星 + 6,000 顆璀璨銀河 + 星光點點微幅閃爍
super_galaxy = """  // ══════════════════════════════════════════════════════════════════════
  // 系統 2: 璀璨星空與壯闊銀河系統 (夜空星光點點 + 雙重銀河拱門)
  // ══════════════════════════════════════════════════════════════════════
  function createStarfieldAndMilkyWay() {
    const starCanvas = document.createElement('canvas');
    starCanvas.width = 64;
    starCanvas.height = 64;
    const sctx = starCanvas.getContext('2d');
    const sgrad = sctx.createRadialGradient(32, 32, 2, 32, 32, 32);
    sgrad.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');
    sgrad.addColorStop(0.3, 'rgba(255, 255, 255, 0.85)');
    sgrad.addColorStop(0.65, 'rgba(199, 210, 254, 0.35)');
    sgrad.addColorStop(1.0, 'rgba(199, 210, 254, 0.0)');
    sctx.fillStyle = sgrad;
    sctx.fillRect(0, 0, 64, 64);
    const starTexture = new THREE.CanvasTexture(starCanvas);

    // 1. 穹頂璀璨星空 (4,000 顆閃耀星點)
    const starCount = 4000;
    const starGeo = new THREE.BufferGeometry();
    const starPositions = new Float32Array(starCount * 3);
    const starSizes = new Float32Array(starCount);

    for (let i = 0; i < starCount; i++) {
      const radius = 80 + Math.random() * 45;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(0.08 + Math.random() * 0.88);
      starPositions[i * 3] = radius * Math.sin(phi) * Math.cos(theta) + 2.1;
      starPositions[i * 3 + 1] = radius * Math.cos(phi) + 16;
      starPositions[i * 3 + 2] = radius * Math.sin(phi) * Math.sin(theta);
      starSizes[i] = 1.0 + Math.random() * 1.6;
    }
    starGeo.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
    starGeo.setAttribute('size', new THREE.BufferAttribute(starSizes, 1));

    const starMat = new THREE.PointsMaterial({
      map: starTexture,
      color: 0xffffff,
      size: 1.5,
      transparent: true,
      opacity: 0,
      blending: THREE.AdditiveBlending,
      depthTest: true,
      depthWrite: false
    });
    starfieldPoints = new THREE.Points(starGeo, starMat);
    starfieldPoints.visible = false;
    scene.add(starfieldPoints);

    // 2. 壯麗銀河微粒拱門 (6,000 顆彩色高密度星雲帶)
    const mwCount = 6000;
    const mwGeo = new THREE.BufferGeometry();
    const mwPositions = new Float32Array(mwCount * 3);
    const mwColors = new Float32Array(mwCount * 3);

    const c1 = new THREE.Color(0xd8b4fe); // 夢幻星雲紫
    const c2 = new THREE.Color(0xf472b6); // 浪漫玫瑰粉
    const c3 = new THREE.Color(0x93c5fd); // 冰晶寶石藍
    const c4 = new THREE.Color(0xffffff); // 耀眼鑽石白
    const c5 = new THREE.Color(0xfef08a); // 金色微塵
    const palette = [c1, c2, c3, c4, c5];

    for (let i = 0; i < mwCount; i++) {
      const t = (Math.random() - 0.5) * Math.PI * 1.65;
      const spread = (Math.random() + Math.random() - 1) * 7.5;
      const radius = 86 + (Math.random() - 0.5) * 10;

      const rawX = Math.cos(t) * radius;
      const rawY = Math.sin(t) * radius * 0.62 + 36;
      const rawZ = spread * 4.6;

      const rot = 0.62;
      mwPositions[i * 3] = (rawX * Math.cos(rot) - rawZ * Math.sin(rot)) + 2.1;
      mwPositions[i * 3 + 1] = Math.max(rawY, 16.0);
      mwPositions[i * 3 + 2] = rawX * Math.sin(rot) + rawZ * Math.cos(rot);

      const col = palette[Math.floor(Math.random() * palette.length)];
      mwColors[i * 3] = col.r;
      mwColors[i * 3 + 1] = col.g;
      mwColors[i * 3 + 2] = col.b;
    }
    mwGeo.setAttribute('position', new THREE.BufferAttribute(mwPositions, 3));
    mwGeo.setAttribute('color', new THREE.BufferAttribute(mwColors, 3));

    const mwMat = new THREE.PointsMaterial({
      map: starTexture,
      vertexColors: true,
      size: 2.1,
      transparent: true,
      opacity: 0,
      blending: THREE.AdditiveBlending,
      depthTest: true,
      depthWrite: false
    });
    milkyWayPoints = new THREE.Points(mwGeo, mwMat);
    milkyWayPoints.visible = false;
    scene.add(milkyWayPoints);
  }"""

text = re.sub(
    r'  // ══════════════════════════════════════════════════════════════════════\s*// 系統 2: 璀璨星空與銀河粒子系統[\s\S]*?scene\.add\(milkyWayPoints\);\s*\}',
    super_galaxy,
    text
)

# 5. 更新夜間點燈邏輯：亮度提高至 2.4，並在夜晚為每座主要島嶼開啟溫暖金色 PointLight
glow_update = """    // 5. 夜間點燈邏輯 (建築物窗戶、島嶼路燈與木橋路燈全數點亮)
    const isNightTime = cycle > 0.46 && cycle < 0.96;
    const glowTarget = isNightTime ? 2.4 : 0.0;
    if (nightGlowMaterial) {
      nightGlowMaterial.emissiveIntensity += (glowTarget - nightGlowMaterial.emissiveIntensity) * 0.06;
      nightGlowMaterial.emissive.set(isNightTime ? 0xffaa33 : 0x000000);
    }
    nightPointLights.forEach((pl) => {
      pl.intensity += ((isNightTime ? 1.8 : 0.0) - pl.intensity) * 0.06;
    });"""

text = re.sub(
    r'    // 5\. 夜間點燈邏輯[\s\S]*?pl\.intensity \+= \(\(isNightTime \? 1\.5 : 0\.0\) - pl\.intensity\) \* 0\.05;\s*\}\);',
    glow_update,
    text
)

with open('src/pages/island.astro', 'w', encoding='utf-8') as f:
    f.write(text)

print("ISLAND_SCALE_AND_LIGHTS_UPGRADE_SUCCESS")
