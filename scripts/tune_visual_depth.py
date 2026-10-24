import re

with open('src/pages/island.astro', encoding='utf-8') as f:
    text = f.read()

# 1. 星空與銀河：半徑調大到 75~100，Y > 10，depthTest: true，徹底置於遠景背景
new_starfield = """  // ══════════════════════════════════════════════════════════════════════
  // 系統 2: 璀璨星空與銀河粒子系統 (遠景深度 + 圓形星芒)
  // ══════════════════════════════════════════════════════════════════════
  function createStarfieldAndMilkyWay() {
    const starCanvas = document.createElement('canvas');
    starCanvas.width = 64;
    starCanvas.height = 64;
    const sctx = starCanvas.getContext('2d');
    const sgrad = sctx.createRadialGradient(32, 32, 2, 32, 32, 32);
    sgrad.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');
    sgrad.addColorStop(0.3, 'rgba(255, 255, 255, 0.75)');
    sgrad.addColorStop(0.7, 'rgba(199, 210, 254, 0.25)');
    sgrad.addColorStop(1.0, 'rgba(199, 210, 254, 0.0)');
    sctx.fillStyle = sgrad;
    sctx.fillRect(0, 0, 64, 64);
    const starTexture = new THREE.CanvasTexture(starCanvas);

    // 1. 穹頂星空 (2,500 顆，半徑 75~105，高空遠景)
    const starCount = 2500;
    const starGeo = new THREE.BufferGeometry();
    const starPositions = new Float32Array(starCount * 3);

    for (let i = 0; i < starCount; i++) {
      const radius = 75 + Math.random() * 30;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(0.15 + Math.random() * 0.75); // 只在高空穹頂
      starPositions[i * 3] = radius * Math.sin(phi) * Math.cos(theta) + 2.1;
      starPositions[i * 3 + 1] = radius * Math.cos(phi) + 12; // 確保高於島嶼
      starPositions[i * 3 + 2] = radius * Math.sin(phi) * Math.sin(theta);
    }
    starGeo.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));

    const starMat = new THREE.PointsMaterial({
      map: starTexture,
      color: 0xffffff,
      size: 1.4,
      transparent: true,
      opacity: 0,
      blending: THREE.AdditiveBlending,
      depthTest: true,
      depthWrite: false
    });
    starfieldPoints = new THREE.Points(starGeo, starMat);
    starfieldPoints.visible = false;
    scene.add(starfieldPoints);

    // 2. 銀河拱門微粒帶 (3,500 顆彩色微粒，高空大圓弧)
    const mwCount = 3500;
    const mwGeo = new THREE.BufferGeometry();
    const mwPositions = new Float32Array(mwCount * 3);
    const mwColors = new Float32Array(mwCount * 3);

    const c1 = new THREE.Color(0xc084fc);
    const c2 = new THREE.Color(0xf472b6);
    const c3 = new THREE.Color(0x93c5fd);
    const c4 = new THREE.Color(0xffffff);
    const palette = [c1, c2, c3, c4];

    for (let i = 0; i < mwCount; i++) {
      const t = (Math.random() - 0.5) * Math.PI * 1.5;
      const spread = (Math.random() + Math.random() - 1) * 6.0;
      const radius = 80 + (Math.random() - 0.5) * 8;

      const rawX = Math.cos(t) * radius;
      const rawY = Math.sin(t) * radius * 0.55 + 32; // 高聳銀河拱橋
      const rawZ = spread * 4.0;

      const rot = 0.65;
      mwPositions[i * 3] = (rawX * Math.cos(rot) - rawZ * Math.sin(rot)) + 2.1;
      mwPositions[i * 3 + 1] = Math.max(rawY, 14.0);
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
      size: 1.8,
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
    new_starfield,
    text
)

# 2. 太陽與月亮：斜向軌道 (Radius 30, 斜角公轉)，在天空中清晰可見
new_day_night = """  // ══════════════════════════════════════════════════════════════════════
  // 系統 1: 180 秒日夜循環系統 (太陽 + 月亮 + 天空色彩插值)
  // ══════════════════════════════════════════════════════════════════════
  function createDayNightSystem() {
    celestialPivot = new THREE.Group();
    celestialPivot.position.set(2.1, 0, 0);
    celestialPivot.rotation.x = -0.35; // 傾斜軸，讓太陽從左前天際升起，月亮從右後天際升起
    scene.add(celestialPivot);

    // ── 太陽端 (Radius 28) ──
    const sunGroup = new THREE.Group();
    sunGroup.position.set(-28, 0, 0);

    const sunGeo = new THREE.SphereGeometry(2.0, 24, 24);
    const sunMat = new THREE.MeshBasicMaterial({ color: 0xfff9db });
    sunMesh = new THREE.Mesh(sunGeo, sunMat);
    sunGroup.add(sunMesh);

    // 太陽金色放射日冕 Sprite
    const sunCanvas = document.createElement('canvas');
    sunCanvas.width = 256;
    sunCanvas.height = 256;
    const sctx = sunCanvas.getContext('2d');
    const sgrad = sctx.createRadialGradient(128, 128, 14, 128, 128, 128);
    sgrad.addColorStop(0.0, 'rgba(255, 255, 235, 1.0)');
    sgrad.addColorStop(0.25, 'rgba(254, 215, 170, 0.85)');
    sgrad.addColorStop(0.6, 'rgba(251, 146, 60, 0.35)');
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
    sunGlowSprite.scale.set(18, 18, 1);
    sunGroup.add(sunGlowSprite);

    sunLight = new THREE.DirectionalLight(0xfff7ed, 1.6);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 1;
    sunLight.shadow.camera.far = 75;
    const sd = 25;
    sunLight.shadow.camera.left = -sd;
    sunLight.shadow.camera.right = sd;
    sunLight.shadow.camera.top = sd;
    sunLight.shadow.camera.bottom = -sd;
    sunLight.shadow.bias = -0.0003;
    sunGroup.add(sunLight);
    celestialPivot.add(sunGroup);

    // ── 月亮端 (對立面 180 度，Radius 28) ──
    const moonGroup = new THREE.Group();
    moonGroup.position.set(28, 0, 0);

    const moonGeo = new THREE.SphereGeometry(1.5, 24, 24);
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
    const mgrad = mctx.createRadialGradient(128, 128, 14, 128, 128, 128);
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
    moonGlowSprite.scale.set(14, 14, 1);
    moonGroup.add(moonGlowSprite);

    moonLight = new THREE.DirectionalLight(0xa5b4fc, 0.5);
    moonGroup.add(moonLight);
    celestialPivot.add(moonGroup);

    // 環境基礎光
    ambientLight = new THREE.AmbientLight(0xfff7ed, 0.65);
    scene.add(ambientLight);
    hemiLight = new THREE.HemisphereLight(0xd9f0fc, 0x826d5e, 0.55);
    scene.add(hemiLight);
  }"""

text = re.sub(
    r'  // ══════════════════════════════════════════════════════════════════════\s*// 系統 1: 180 秒日夜循環系統[\s\S]*?scene\.add\(hemiLight\);\s*\}',
    new_day_night,
    text
)

# 3. 雲朵位置調整 (分佈在 Y: 7.5~10.5，Radius 18~26，在相機俯視畫面周圍立體漂浮)
new_clouds = """  // ══════════════════════════════════════════════════════════════════════
  // 系統 3: 低空慢速漂浮白雲 (純白立體蓬鬆雲朵)
  // ══════════════════════════════════════════════════════════════════════
  function createLowPolyClouds() {
    cloudsGroup = new THREE.Group();
    const cloudMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.8,
      flatShading: true,
      transparent: true,
      opacity: 0.94
    });

    // 生成 6 朵分佈在群島視野兩側的白雲
    for (let c = 0; c < 6; c++) {
      const singleCloud = new THREE.Group();
      const puffCount = 5 + Math.floor(Math.random() * 3);
      for (let p = 0; p < puffCount; p++) {
        const radius = 0.85 + Math.random() * 0.65;
        const puff = new THREE.Mesh(new THREE.DodecahedronGeometry(radius, 1), cloudMat);
        puff.position.set(
          (p - puffCount / 2) * 0.95 + (Math.random() - 0.5) * 0.35,
          (Math.random() - 0.5) * 0.4,
          (Math.random() - 0.5) * 0.5
        );
        puff.scale.set(1.2, 0.8, 1.0);
        puff.castShadow = true;
        singleCloud.add(puff);
      }

      const orbitRadius = 18 + (c % 3) * 4.0;
      const angle = (c / 6) * Math.PI * 2;
      const y = 8.5 + (c % 2) * 1.5;
      singleCloud.position.set(Math.cos(angle) * orbitRadius + 2.1, y, Math.sin(angle) * orbitRadius);
      singleCloud.userData = {
        orbitRadius,
        angle,
        speed: 0.08 + (c % 3) * 0.03,
        y
      };
      cloudsGroup.add(singleCloud);
    }
    scene.add(cloudsGroup);
  }"""

text = re.sub(
    r'  // ══════════════════════════════════════════════════════════════════════\s*// 系統 3: 低空慢速漂浮白雲[\s\S]*?scene\.add\(cloudsGroup\);\s*\}',
    new_clouds,
    text
)

with open('src/pages/island.astro', 'w', encoding='utf-8') as f:
    f.write(text)

print("TUNE_DEPTH_SUCCESS")
