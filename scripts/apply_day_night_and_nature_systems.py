import re

with open('src/pages/island.astro', encoding='utf-8') as f:
    text = f.read()

# 1. 在全域變數區加入日夜循環、天體、星空、雲朵、海洋頂點等變數
var_insert = """
  // ══════════════════════════════════════════════════════════════════════
  // 6 大自然與光影特效系統變數 (Day/Night, Stars, Clouds, Waves, Night Lights)
  // ══════════════════════════════════════════════════════════════════════
  const clock = new THREE.Clock();
  let celestialPivot;          // 日月旋轉軸
  let sunMesh, sunLight, sunGlowSprite;
  let moonMesh, moonLight, moonGlowSprite;
  let starfieldPoints, milkyWayPoints;
  let cloudsGroup;             // 低空慢速雲朵
  let oceanMesh, oceanGeo, oceanInitialPositions;
  let nightGlowMaterial;       // 路燈與窗戶夜間發光材質
  let nightPointLights = [];   // 島嶼夜間暖光
  let isAutoDayNight = true;   // 是否開啟 180s 自動循環
  let targetCycle = 0.25;      // 當前目標時間 (預設正午 0.25)
  let currentCycle = 0.25;     // 插值平滑 cycle
  let manualTimeLock = false;  // 手動選擇時段鎖定
"""

if 'const clock = new THREE.Clock();' not in text:
    pos = text.find('let dirLight, hemiLight, ambientLight;')
    if pos != -1:
        text = text[:pos] + var_insert + "\n  " + text[pos:]
        print("ADDED_NATURE_VARIABLES")

# 2. 升級 init() 流程：加入天體、星空、雲朵、海浪、夜燈初始化
old_init_setup = """    setupLights();
    createCurvedOcean();
    buildIslands();
    buildBridges();
    buildFlowLines();
    spawnWalkers();
    birdFlockData = createBirdFlock();
    setupRaycaster();
    setupUI();"""

new_init_setup = """    createDayNightSystem();   // 1. 太陽月亮 180s 日夜循環
    createStarfieldAndMilkyWay(); // 2. 穹頂星空與銀河微粒
    createLowPolyClouds();    // 3. 漂浮低空慢速白雲
    createCurvedOcean();      // 4. 動態波浪海洋
    buildIslands();           // 5. 24 座微縮島嶼
    buildBridges();           // 6. 連接木橋
    buildFlowLines();         // 7. 跨界光流索
    spawnWalkers();           // 8. 漫步小人
    birdFlockData = createBirdFlock(); // 9. 飛鳥振翅盤旋
    setupNightLights();       // 10. 島嶼路燈與夜間發光窗戶
    setupRaycaster();
    setupUI();"""

text = text.replace(old_init_setup, new_init_setup)
print("UPDATED_INIT_FLOW")

# 3. 建立 6 大系統的完整核心函數
systems_code = """
  // ══════════════════════════════════════════════════════════════════════
  // 系統 1: 180 秒日夜循環系統 (太陽 + 月亮 + 天空色彩插值)
  // ══════════════════════════════════════════════════════════════════════
  function createDayNightSystem() {
    celestialPivot = new THREE.Group();
    celestialPivot.position.set(2.1, 0, 0);
    scene.add(celestialPivot);

    // ── 太陽端 (Radius 36) ──
    const sunGroup = new THREE.Group();
    sunGroup.position.set(36, 0, 0);

    const sunGeo = new THREE.SphereGeometry(1.65, 16, 16);
    const sunMat = new THREE.MeshBasicMaterial({ color: 0xfff3cc });
    sunMesh = new THREE.Mesh(sunGeo, sunMat);
    sunGroup.add(sunMesh);

    // 太陽金色放射日冕 Sprite (Canvas 徑向漸層)
    const sunCanvas = document.createElement('canvas');
    sunCanvas.width = 256;
    sunCanvas.height = 256;
    const sctx = sunCanvas.getContext('2d');
    const sgrad = sctx.createRadialGradient(128, 128, 10, 128, 128, 128);
    sgrad.addColorStop(0.0, 'rgba(255, 250, 220, 1.0)');
    sgrad.addColorStop(0.25, 'rgba(255, 200, 100, 0.7)');
    sgrad.addColorStop(0.6, 'rgba(251, 146, 60, 0.25)');
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
    sunLight = new THREE.DirectionalLight(0xfff7ed, 1.55);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 1;
    sunLight.shadow.camera.far = 85;
    const sd = 25;
    sunLight.shadow.camera.left = -sd;
    sunLight.shadow.camera.right = sd;
    sunLight.shadow.camera.top = sd;
    sunLight.shadow.camera.bottom = -sd;
    sunLight.shadow.bias = -0.0003;
    sunGroup.add(sunLight);
    celestialPivot.add(sunGroup);

    // ── 月亮端 (對立面 180 度，Radius 36) ──
    const moonGroup = new THREE.Group();
    moonGroup.position.set(-36, 0, 0);

    const moonGeo = new THREE.SphereGeometry(1.25, 16, 16);
    const moonMat = new THREE.MeshStandardMaterial({
      color: 0xf3f4f6,
      roughness: 0.85,
      metalness: 0.1
    });
    moonMesh = new THREE.Mesh(moonGeo, moonMat);
    moonGroup.add(moonMesh);

    // 月亮幽藍月暈 Sprite
    const moonCanvas = document.createElement('canvas');
    moonCanvas.width = 256;
    moonCanvas.height = 256;
    const mctx = moonCanvas.getContext('2d');
    const mgrad = mctx.createRadialGradient(128, 128, 10, 128, 128, 128);
    mgrad.addColorStop(0.0, 'rgba(230, 240, 255, 0.95)');
    mgrad.addColorStop(0.35, 'rgba(147, 197, 253, 0.5)');
    mgrad.addColorStop(0.7, 'rgba(99, 102, 241, 0.18)');
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
    moonGlowSprite.scale.set(12, 12, 1);
    moonGroup.add(moonGlowSprite);

    // 微弱月光平行光
    moonLight = new THREE.DirectionalLight(0x818cf8, 0.45);
    moonGroup.add(moonLight);
    celestialPivot.add(moonGroup);

    // 環境基礎光
    ambientLight = new THREE.AmbientLight(0xfff7ed, 0.65);
    scene.add(ambientLight);
    hemiLight = new THREE.HemisphereLight(0xd9f0fc, 0x826d5e, 0.55);
    scene.add(hemiLight);
  }

  // ══════════════════════════════════════════════════════════════════════
  // 系統 2: 璀璨星空與銀河粒子系統 (Starfield & Milky Way)
  // ══════════════════════════════════════════════════════════════════════
  function createStarfieldAndMilkyWay() {
    // 1. 穹頂星空 (3,000 顆星星)
    const starCount = 3000;
    const starGeo = new THREE.BufferGeometry();
    const starPositions = new Float32Array(starCount * 3);
    const starSizes = new Float32Array(starCount);

    for (let i = 0; i < starCount; i++) {
      const radius = 60 + Math.random() * 25;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 0.92); // 偏向上半穹頂
      starPositions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      starPositions[i * 3 + 1] = Math.abs(radius * Math.cos(phi)) + 5;
      starPositions[i * 3 + 2] = radius * Math.sin(phi) * Math.sin(theta);
      starSizes[i] = 0.45 + Math.random() * 0.75;
    }
    starGeo.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
    starGeo.setAttribute('size', new THREE.BufferAttribute(starSizes, 1));

    const starMat = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 0.65,
      transparent: true,
      opacity: 0,
      blending: THREE.AdditiveBlending
    });
    starfieldPoints = new THREE.Points(starGeo, starMat);
    scene.add(starfieldPoints);

    // 2. 銀河高密度微粒帶 (5,000 顆彩色星雲粒子)
    const mwCount = 5000;
    const mwGeo = new THREE.BufferGeometry();
    const mwPositions = new Float32Array(mwCount * 3);
    const mwColors = new Float32Array(mwCount * 3);

    const c1 = new THREE.Color(0xc084fc); // 淡紫
    const c2 = new THREE.Color(0xf472b6); // 星雲粉
    const c3 = new THREE.Color(0x93c5fd); // 淡藍
    const c4 = new THREE.Color(0xffffff); // 亮白
    const palette = [c1, c2, c3, c4];

    for (let i = 0; i < mwCount; i++) {
      // 銀河帶：斜向大圓拱門
      const t = (Math.random() - 0.5) * Math.PI * 1.8;
      const spread = (Math.random() + Math.random() - 1) * 6.5;
      const radius = 68 + (Math.random() - 0.5) * 8;

      const rawX = Math.cos(t) * radius;
      const rawY = Math.sin(t) * radius * 0.72 + 25;
      const rawZ = spread * 4.2;

      // 旋轉 42 度斜跨天際
      const rot = 0.72;
      mwPositions[i * 3] = rawX * Math.cos(rot) - rawZ * Math.sin(rot);
      mwPositions[i * 3 + 1] = Math.max(rawY, 2.0);
      mwPositions[i * 3 + 2] = rawX * Math.sin(rot) + rawZ * Math.cos(rot);

      const col = palette[Math.floor(Math.random() * palette.length)];
      mwColors[i * 3] = col.r;
      mwColors[i * 3 + 1] = col.g;
      mwColors[i * 3 + 2] = col.b;
    }
    mwGeo.setAttribute('position', new THREE.BufferAttribute(mwPositions, 3));
    mwGeo.setAttribute('color', new THREE.BufferAttribute(mwColors, 3));

    const mwMat = new THREE.PointsMaterial({
      vertexColors: true,
      size: 0.85,
      transparent: true,
      opacity: 0,
      blending: THREE.AdditiveBlending
    });
    milkyWayPoints = new THREE.Points(mwGeo, mwMat);
    scene.add(milkyWayPoints);
  }

  // ══════════════════════════════════════════════════════════════════════
  // 系統 3: 低空慢速漂浮白雲 (Low-poly Floating Clouds)
  // ══════════════════════════════════════════════════════════════════════
  function createLowPolyClouds() {
    cloudsGroup = new THREE.Group();
    const cloudMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 0.9,
      flatShading: true,
      transparent: true,
      opacity: 0.9
    });

    // 生成 8 朵雲
    for (let c = 0; c < 8; c++) {
      const singleCloud = new THREE.Group();
      const puffCount = 5 + Math.floor(Math.random() * 4);
      for (let p = 0; p < puffCount; p++) {
        const radius = 0.75 + Math.random() * 0.65;
        const puff = new THREE.Mesh(new THREE.DodecahedronGeometry(radius, 1), cloudMat);
        puff.position.set(
          (p - puffCount / 2) * 0.95 + (Math.random() - 0.5) * 0.4,
          (Math.random() - 0.5) * 0.45,
          (Math.random() - 0.5) * 0.65
        );
        puff.scale.set(1.2, 0.8, 1.0);
        singleCloud.add(puff);
      }

      const orbitRadius = 18 + Math.random() * 14;
      const angle = (c / 8) * Math.PI * 2 + Math.random() * 0.5;
      const y = 8.5 + (c % 3) * 1.8 + Math.random() * 1.2;
      singleCloud.position.set(Math.cos(angle) * orbitRadius, y, Math.sin(angle) * orbitRadius);
      singleCloud.userData = {
        orbitRadius,
        angle,
        speed: 0.08 + Math.random() * 0.06,
        y
      };
      cloudsGroup.add(singleCloud);
    }
    scene.add(cloudsGroup);
  }

  // ══════════════════════════════════════════════════════════════════════
  // 系統 4: 動態波浪海洋 (高反射率 + 頂點海浪動畫)
  // ══════════════════════════════════════════════════════════════════════
  function createCurvedOcean() {
    const oceanRadius = PLANET_RADIUS - 0.18;
    // 96x64 細分度，提供細緻海浪起伏
    oceanGeo = new THREE.SphereGeometry(oceanRadius, 96, 64, 0, Math.PI * 2, 0, Math.PI * 0.48);
    
    // 保存初始頂點位置
    const pos = oceanGeo.attributes.position;
    oceanInitialPositions = new Float32Array(pos.count * 3);
    for (let i = 0; i < pos.count * 3; i++) {
      oceanInitialPositions[i] = pos.array[i];
    }

    const oceanMat = new THREE.MeshStandardMaterial({
      color: 0x184e77,
      roughness: 0.16,
      metalness: 0.52,
      transparent: true,
      opacity: 0.92,
      flatShading: true
    });
    oceanMesh = new THREE.Mesh(oceanGeo, oceanMat);
    oceanMesh.position.copy(PLANET_CENTER);
    oceanMesh.receiveShadow = true;
    scene.add(oceanMesh);
    waterSphere = oceanMesh;
  }

  // ══════════════════════════════════════════════════════════════════════
  // 系統 5: 夜間點燈 (路燈與窗戶發光)
  // ══════════════════════════════════════════════════════════════════════
  function setupNightLights() {
    // 共享發光材質
    nightGlowMaterial = new THREE.MeshStandardMaterial({
      color: 0xffedd5,
      emissive: 0xff9900,
      emissiveIntensity: 0.0,
      roughness: 0.3
    });

    // 在 4 座主要島嶼上方配置夜間微弱暖色點光源
    const majorIslands = ['endoscopy', 'stomach', 'wealth-ladder', 'golden-rules'];
    majorIslands.forEach((id) => {
      const islObj = islandObjectsMap.get(id);
      if (islObj) {
        const pLight = new THREE.PointLight(0xffaa44, 0, 12, 1.8);
        pLight.position.set(0, HEX_HEIGHT + 2.5, 0);
        islObj.add(pLight);
        nightPointLights.push(pLight);
      }
    });
  }

  // ══════════════════════════════════════════════════════════════════════
  // 系統 6: 日夜時序光影插值更新 (在 animate 每幀調用)
  // ══════════════════════════════════════════════════════════════════════
  function updateDayNightCycle(elapsedTime) {
    if (isAutoDayNight && !manualTimeLock) {
      targetCycle = (elapsedTime % 180) / 180;
    }
    // 平滑跟隨 targetCycle (解決點擊按鈕時的突兀跳變)
    let diff = targetCycle - currentCycle;
    if (diff > 0.5) diff -= 1.0;
    if (diff < -0.5) diff += 1.0;
    currentCycle = (currentCycle + diff * 0.05 + 1.0) % 1.0;

    const cycle = currentCycle;

    // 1. 旋轉日月軸 (繞島嶼群斜向旋轉升起與落下)
    if (celestialPivot) {
      celestialPivot.rotation.z = cycle * Math.PI * 2;
      celestialPivot.rotation.x = Math.sin(cycle * Math.PI * 2) * 0.28;
    }

    // 2. 太陽與月亮光照強度切換
    // 白天：0.0~0.5 (正午 ~0.25)；夜晚：0.5~1.0 (午夜 ~0.75)
    const isDay = cycle < 0.5;
    const sunAltitude = Math.sin(cycle * Math.PI * 2); // > 0 為在天空
    const sunIntensity = Math.max(0, sunAltitude) * 1.55;
    const moonIntensity = Math.max(0, -sunAltitude) * 0.45;

    if (sunLight) sunLight.intensity = sunIntensity;
    if (moonLight) moonLight.intensity = moonIntensity;

    // 3. 天空背景色與霧氣平滑插值 (Lerp)
    // 4 個關鍵時段色彩：
    // Noon(0.25): #7dc4e8; Dusk(0.48): #fd5e53; Midnight(0.75): #060919; Dawn(0.02): #fbcfe8
    const noonCol = new THREE.Color(0x7dc4e8);
    const duskCol = new THREE.Color(0xfd5e53);
    const nightCol = new THREE.Color(0x060919);
    const dawnCol = new THREE.Color(0xfbcfe8);

    const curSky = new THREE.Color();
    const curFog = new THREE.Color();

    if (cycle < 0.25) {
      // 晨曦 (0.02) ➔ 正午 (0.25)
      const t = (cycle) / 0.25;
      curSky.lerpColors(dawnCol, noonCol, t);
    } else if (cycle < 0.5) {
      // 正午 (0.25) ➔ 暮霞黃昏 (0.5)
      const t = (cycle - 0.25) / 0.25;
      curSky.lerpColors(noonCol, duskCol, t);
    } else if (cycle < 0.75) {
      // 暮霞黃昏 (0.5) ➔ 深夜 (0.75)
      const t = (cycle - 0.5) / 0.25;
      curSky.lerpColors(duskCol, nightCol, t);
    } else {
      // 深夜 (0.75) ➔ 晨曦 (1.0)
      const t = (cycle - 0.75) / 0.25;
      curSky.lerpColors(nightCol, dawnCol, t);
    }

    scene.background.copy(curSky);
    if (scene.fog) {
      curFog.copy(curSky).multiplyScalar(0.92);
      scene.fog.color.copy(curFog);
    }

    // 4. 星空與銀河透明度 (夜晚淡入，白天淡出)
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
    if (milkyWayPoints) milkyWayPoints.material.opacity = starAlpha * 0.92;

    // 星空緩慢自轉
    if (starfieldPoints) starfieldPoints.rotation.y += 0.0003;
    if (milkyWayPoints) milkyWayPoints.rotation.y += 0.00025;

    // 5. 夜間點燈邏輯 (路燈與發光窗戶)
    const isNightTime = cycle > 0.46 && cycle < 0.96;
    const glowTarget = isNightTime ? 2.0 : 0.0;
    if (nightGlowMaterial) {
      nightGlowMaterial.emissiveIntensity += (glowTarget - nightGlowMaterial.emissiveIntensity) * 0.05;
    }
    nightPointLights.forEach((pl) => {
      pl.intensity += ((isNightTime ? 1.5 : 0.0) - pl.intensity) * 0.05;
    });

    // 6. 海水色彩隨時間過渡
    if (oceanMesh) {
      const dayOcean = new THREE.Color(0x184e77);
      const sunsetOcean = new THREE.Color(0x7c3a2e);
      const nightOcean = new THREE.Color(0x0a192f);
      const curOcean = new THREE.Color();

      if (cycle < 0.4) {
        curOcean.copy(dayOcean);
      } else if (cycle < 0.52) {
        curOcean.lerpColors(dayOcean, sunsetOcean, (cycle - 0.4) / 0.12);
      } else if (cycle < 0.65) {
        curOcean.lerpColors(sunsetOcean, nightOcean, (cycle - 0.52) / 0.13);
      } else {
        curOcean.lerpColors(nightOcean, dayOcean, (cycle - 0.88) / 0.12);
      }
      oceanMesh.material.color.copy(curOcean);
    }
  }

  // ══════════════════════════════════════════════════════════════════════
  // 海浪波動與雲朵位移動畫 (在 animate 每幀調用)
  // ══════════════════════════════════════════════════════════════════════
  function updateWavesAndClouds(elapsedTime) {
    // 1. 動態海浪頂點起伏
    if (oceanGeo && oceanInitialPositions) {
      const pos = oceanGeo.attributes.position;
      const count = pos.count;
      for (let i = 0; i < count; i++) {
        const ox = oceanInitialPositions[i * 3];
        const oy = oceanInitialPositions[i * 3 + 1];
        const oz = oceanInitialPositions[i * 3 + 2];

        // 疊加正弦波
        const wave = Math.sin(ox * 0.35 + elapsedTime * 1.8) * 0.16 +
                     Math.cos(oz * 0.28 + elapsedTime * 1.4) * 0.12 +
                     Math.sin((ox + oz) * 0.2 + elapsedTime * 2.1) * 0.08;

        // 沿法向量方向微幅浮動
        const len = Math.sqrt(ox * ox + oy * oy + oz * oz);
        const nx = ox / len;
        const ny = oy / len;
        const nz = oz / len;

        pos.setXYZ(i, ox + nx * wave, oy + ny * wave, oz + nz * wave);
      }
      pos.needsUpdate = true;
      oceanGeo.computeVertexNormals();
    }

    // 2. 雲朵慢速飄移
    if (cloudsGroup) {
      cloudsGroup.children.forEach((cloud) => {
        const u = cloud.userData;
        if (u) {
          u.angle += u.speed * 0.0018;
          cloud.position.x = Math.cos(u.angle) * u.orbitRadius;
          cloud.position.z = Math.sin(u.angle) * u.orbitRadius;
          cloud.position.y = u.y + Math.sin(elapsedTime * 0.6 + u.orbitRadius) * 0.35;
        }
      });
    }
  }
"""

# 將 6 大系統函數插入在 buildIslands 前面
insert_idx = text.find('function buildIslands()')
if insert_idx != -1:
    text = text[:insert_idx] + systems_code + "\n\n  " + text[insert_idx:]
    print("ADDED_SYSTEMS_FUNCTIONS")

# 4. 在 animate() 中加入 updateDayNightCycle 與 updateWavesAndClouds
animate_patch = """    // 1. 180s 日夜循環光影與天空星空更新
    updateDayNightCycle(elapsedTime);

    // 2. 動態海浪與慢速漂浮白雲更新
    updateWavesAndClouds(elapsedTime);"""

text = re.sub(
    r'    const elapsedTime = now \* 0\.001;\s*// 1\. 球面水波慢速自轉[\s\S]*?if \(waterSphere\) \{\s*waterSphere\.rotation\.y = Math\.sin\(now \* 0\.0003\) \* 0\.015;\s*\}',
    "    const elapsedTime = now * 0.001;\n\n" + animate_patch,
    text
)

# 5. 更新頂部時序按鈕點擊事件 (晨曦、正午、暮霞、星夜)
time_btn_patch = """      btn.addEventListener('click', () => {
        timeBtns.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        const timeKey = btn.dataset.time;
        manualTimeLock = true;
        isAutoDayNight = false;

        if (timeKey === 'dawn') targetCycle = 0.02;
        else if (timeKey === 'noon') targetCycle = 0.25;
        else if (timeKey === 'dusk') targetCycle = 0.48;
        else if (timeKey === 'night') targetCycle = 0.75;
      });"""

text = re.sub(
    r'      btn\.addEventListener\(\'click\', \(\) => \{\s*timeBtns\.forEach\(\(b\) => b\.classList\.remove\(\'active\'\)\);\s*btn\.classList\.add\(\'active\'\);\s*setTimePreset\(btn\.dataset\.time\);\s*\}\);',
    time_btn_patch,
    text
)

with open('src/pages/island.astro', 'w', encoding='utf-8') as f:
    f.write(text)

print("DAY_NIGHT_AND_NATURE_SYSTEMS_SUCCESSFULLY_APPLIED")
