import re

with open('src/pages/island.astro', encoding='utf-8') as f:
    text = f.read()

# 替換 createStarfieldAndMilkyWay 函數：使用圓形羽化星芒貼圖，避免方塊，並由 visible 完全控制
new_starfield_code = """  // ══════════════════════════════════════════════════════════════════════
  // 系統 2: 璀璨星空與銀河粒子系統 (圓形星芒貼圖 + 夜晚淡入)
  // ══════════════════════════════════════════════════════════════════════
  function createStarfieldAndMilkyWay() {
    // 圓形羽化發光星點貼圖
    const starCanvas = document.createElement('canvas');
    starCanvas.width = 64;
    starCanvas.height = 64;
    const sctx = starCanvas.getContext('2d');
    const sgrad = sctx.createRadialGradient(32, 32, 2, 32, 32, 32);
    sgrad.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');
    sgrad.addColorStop(0.3, 'rgba(255, 255, 255, 0.8)');
    sgrad.addColorStop(0.7, 'rgba(199, 210, 254, 0.3)');
    sgrad.addColorStop(1.0, 'rgba(199, 210, 254, 0.0)');
    sctx.fillStyle = sgrad;
    sctx.fillRect(0, 0, 64, 64);
    const starTexture = new THREE.CanvasTexture(starCanvas);

    // 1. 穹頂星空 (2,500 顆星星)
    const starCount = 2500;
    const starGeo = new THREE.BufferGeometry();
    const starPositions = new Float32Array(starCount * 3);

    for (let i = 0; i < starCount; i++) {
      const radius = 55 + Math.random() * 20;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 0.85); // 穹頂分佈
      starPositions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      starPositions[i * 3 + 1] = Math.abs(radius * Math.cos(phi)) + 6;
      starPositions[i * 3 + 2] = radius * Math.sin(phi) * Math.sin(theta);
    }
    starGeo.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));

    const starMat = new THREE.PointsMaterial({
      map: starTexture,
      color: 0xffffff,
      size: 1.1,
      transparent: true,
      opacity: 0,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    starfieldPoints = new THREE.Points(starGeo, starMat);
    starfieldPoints.visible = false; // 白天初始完全隱藏
    scene.add(starfieldPoints);

    // 2. 銀河高密度微粒帶 (3,500 顆彩色微粒)
    const mwCount = 3500;
    const mwGeo = new THREE.BufferGeometry();
    const mwPositions = new Float32Array(mwCount * 3);
    const mwColors = new Float32Array(mwCount * 3);

    const c1 = new THREE.Color(0xc084fc); // 淡紫
    const c2 = new THREE.Color(0xf472b6); // 星雲粉
    const c3 = new THREE.Color(0x93c5fd); // 冰藍
    const c4 = new THREE.Color(0xffffff); // 純白
    const palette = [c1, c2, c3, c4];

    for (let i = 0; i < mwCount; i++) {
      const t = (Math.random() - 0.5) * Math.PI * 1.6;
      const spread = (Math.random() + Math.random() - 1) * 5.0;
      const radius = 60 + (Math.random() - 0.5) * 6;

      const rawX = Math.cos(t) * radius;
      const rawY = Math.sin(t) * radius * 0.65 + 18;
      const rawZ = spread * 3.5;

      const rot = 0.68;
      mwPositions[i * 3] = rawX * Math.cos(rot) - rawZ * Math.sin(rot);
      mwPositions[i * 3 + 1] = Math.max(rawY, 3.0);
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
      size: 1.35,
      transparent: true,
      opacity: 0,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    milkyWayPoints = new THREE.Points(mwGeo, mwMat);
    milkyWayPoints.visible = false;
    scene.add(milkyWayPoints);
  }"""

# 替換 createDayNightSystem：調整半徑至 26，讓太陽與月亮隨角度出現在視野中
new_day_night_code = """  // ══════════════════════════════════════════════════════════════════════
  // 系統 1: 180 秒日夜循環系統 (太陽 + 月亮 + 天空色彩插值)
  // ══════════════════════════════════════════════════════════════════════
  function createDayNightSystem() {
    celestialPivot = new THREE.Group();
    celestialPivot.position.set(2.1, 0, 0);
    scene.add(celestialPivot);

    // ── 太陽端 (Radius 25，在視野內清晰可見) ──
    const sunGroup = new THREE.Group();
    sunGroup.position.set(25, 0, 0);

    const sunGeo = new THREE.SphereGeometry(1.8, 20, 20);
    const sunMat = new THREE.MeshBasicMaterial({ color: 0xfff7d6 });
    sunMesh = new THREE.Mesh(sunGeo, sunMat);
    sunGroup.add(sunMesh);

    // 太陽金色放射日冕 Sprite
    const sunCanvas = document.createElement('canvas');
    sunCanvas.width = 256;
    sunCanvas.height = 256;
    const sctx = sunCanvas.getContext('2d');
    const sgrad = sctx.createRadialGradient(128, 128, 12, 128, 128, 128);
    sgrad.addColorStop(0.0, 'rgba(255, 255, 230, 1.0)');
    sgrad.addColorStop(0.2, 'rgba(254, 215, 170, 0.85)');
    sgrad.addColorStop(0.55, 'rgba(251, 146, 60, 0.35)');
    sgrad.addColorStop(1.0, 'rgba(251, 146, 60, 0.0)');
    sctx.fillStyle = sgrad;
    sctx.fillRect(0, 0, 256, 256);
    const sunTexture = new THREE.CanvasTexture(sunCanvas);
    const sunGlowMat = new THREE.SpriteMaterial({
      map: sunTexture,
      blending: THREE.AdditiveBlending,
      transparent: true,
      depthWrite: false
    });
    sunGlowSprite = new THREE.Sprite(sunGlowMat);
    sunGlowSprite.scale.set(16, 16, 1);
    sunGroup.add(sunGlowSprite);

    // 主平行光 (陽光)
    sunLight = new THREE.DirectionalLight(0xfff7ed, 1.6);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 1;
    sunLight.shadow.camera.far = 70;
    const sd = 25;
    sunLight.shadow.camera.left = -sd;
    sunLight.shadow.camera.right = sd;
    sunLight.shadow.camera.top = sd;
    sunLight.shadow.camera.bottom = -sd;
    sunLight.shadow.bias = -0.0003;
    sunGroup.add(sunLight);
    celestialPivot.add(sunGroup);

    // ── 月亮端 (對立面 180 度，Radius 25) ──
    const moonGroup = new THREE.Group();
    moonGroup.position.set(-25, 0, 0);

    const moonGeo = new THREE.SphereGeometry(1.35, 20, 20);
    const moonMat = new THREE.MeshStandardMaterial({
      color: 0xf8fafc,
      roughness: 0.75,
      metalness: 0.1
    });
    moonMesh = new THREE.Mesh(moonGeo, moonMat);
    moonGroup.add(moonMesh);

    // 月亮幽藍月暈 Sprite
    const moonCanvas = document.createElement('canvas');
    moonCanvas.width = 256;
    moonCanvas.height = 256;
    const mctx = moonCanvas.getContext('2d');
    const mgrad = mctx.createRadialGradient(128, 128, 12, 128, 128, 128);
    mgrad.addColorStop(0.0, 'rgba(240, 248, 255, 0.95)');
    mgrad.addColorStop(0.3, 'rgba(165, 180, 252, 0.6)');
    mgrad.addColorStop(0.7, 'rgba(99, 102, 241, 0.2)');
    mgrad.addColorStop(1.0, 'rgba(99, 102, 241, 0.0)');
    mctx.fillStyle = mgrad;
    mctx.fillRect(0, 0, 256, 256);
    const moonTexture = new THREE.CanvasTexture(moonCanvas);
    const moonGlowMat = new THREE.SpriteMaterial({
      map: moonTexture,
      blending: THREE.AdditiveBlending,
      transparent: true,
      depthWrite: false
    });
    moonGlowSprite = new THREE.Sprite(moonGlowMat);
    moonGlowSprite.scale.set(13, 13, 1);
    moonGroup.add(moonGlowSprite);

    // 微弱月光平行光
    moonLight = new THREE.DirectionalLight(0xa5b4fc, 0.5);
    moonGroup.add(moonLight);
    celestialPivot.add(moonGroup);

    // 環境基礎光
    ambientLight = new THREE.AmbientLight(0xfff7ed, 0.65);
    scene.add(ambientLight);
    hemiLight = new THREE.HemisphereLight(0xd9f0fc, 0x826d5e, 0.55);
    scene.add(hemiLight);
  }"""

# 替換 createLowPolyClouds：視野內更豐富的 8 朵雲
new_clouds_code = """  // ══════════════════════════════════════════════════════════════════════
  // 系統 3: 低空慢速漂浮白雲 (視野內立體蓬鬆雲朵)
  // ══════════════════════════════════════════════════════════════════════
  function createLowPolyClouds() {
    cloudsGroup = new THREE.Group();
    const cloudMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.85,
      flatShading: true,
      transparent: true,
      opacity: 0.92
    });

    // 生成 7 朵分佈在群島視野周圍的白雲 (Y: 5.5 ~ 8.5)
    for (let c = 0; c < 7; c++) {
      const singleCloud = new THREE.Group();
      const puffCount = 5 + Math.floor(Math.random() * 3);
      for (let p = 0; p < puffCount; p++) {
        const radius = 0.68 + Math.random() * 0.55;
        const puff = new THREE.Mesh(new THREE.DodecahedronGeometry(radius, 1), cloudMat);
        puff.position.set(
          (p - puffCount / 2) * 0.85 + (Math.random() - 0.5) * 0.3,
          (Math.random() - 0.5) * 0.35,
          (Math.random() - 0.5) * 0.45
        );
        puff.scale.set(1.15, 0.75, 0.95);
        puff.castShadow = true;
        singleCloud.add(puff);
      }

      const orbitRadius = 14 + (c % 3) * 4.5 + Math.random() * 2.0;
      const angle = (c / 7) * Math.PI * 2;
      const y = 6.2 + (c % 3) * 1.2;
      singleCloud.position.set(Math.cos(angle) * orbitRadius, y, Math.sin(angle) * orbitRadius);
      singleCloud.userData = {
        orbitRadius,
        angle,
        speed: 0.09 + Math.random() * 0.05,
        y
      };
      cloudsGroup.add(singleCloud);
    }
    scene.add(cloudsGroup);
  }"""

# 替換 updateDayNightCycle 中的星空顯示邏輯
old_star_logic = """    // 4. 星空與銀河透明度 (夜晚淡入，白天淡出)
    let starAlpha = 0;
    if (cycle > 0.48 && cycle < 0.98) {
      // 夜間高原期
      if (cycle >= 0.55 && cycle <= 0.92) {
        starAlpha = 1.0;
      } else if (cycle < 0.55) {
        starAlpha = (cycle - 0.48) / 0.07;
      } else {
        starAlpha = (0.98 - cycle) / 0.06;
      }
    }
    if (starfieldPoints) starfieldPoints.material.opacity = starAlpha;
    if (milkyWayPoints) milkyWayPoints.material.opacity = starAlpha * 0.92;"""

new_star_logic = """    // 4. 星空與銀河透明度 (夜晚淡入，白天隱藏)
    let starAlpha = 0;
    const isNightVisible = cycle > 0.46 && cycle < 0.98;
    if (isNightVisible) {
      if (cycle >= 0.54 && cycle <= 0.92) {
        starAlpha = 1.0;
      } else if (cycle < 0.54) {
        starAlpha = (cycle - 0.46) / 0.08;
      } else {
        starAlpha = (0.98 - cycle) / 0.06;
      }
    }
    if (starfieldPoints) {
      starfieldPoints.visible = starAlpha > 0.02;
      starfieldPoints.material.opacity = starAlpha;
    }
    if (milkyWayPoints) {
      milkyWayPoints.visible = starAlpha > 0.02;
      milkyWayPoints.material.opacity = starAlpha * 0.95;
    }"""

text = re.sub(
    r'  // ══════════════════════════════════════════════════════════════════════\s*// 系統 2: 璀璨星空與銀河粒子系統[\s\S]*?scene\.add\(milkyWayPoints\);\s*\}',
    new_starfield_code,
    text
)

text = re.sub(
    r'  // ══════════════════════════════════════════════════════════════════════\s*// 系統 1: 180 秒日夜循環系統[\s\S]*?scene\.add\(hemiLight\);\s*\}',
    new_day_night_code,
    text
)

text = re.sub(
    r'  // ══════════════════════════════════════════════════════════════════════\s*// 系統 3: 低空慢速漂浮白雲[\s\S]*?scene\.add\(cloudsGroup\);\s*\}',
    new_clouds_code,
    text
)

text = text.replace(old_star_logic, new_star_logic)

with open('src/pages/island.astro', 'w', encoding='utf-8') as f:
    f.write(text)

print("REFINED_NATURE_VISUALS_SUCCESS")
