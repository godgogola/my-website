import re

path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update initial scene background & fog & camera position in init()
init_old = """    // 1. Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xd7edf6);
    scene.fog = new THREE.FogExp2(0xd7edf6, 0.015);

    // 2. Camera
    const aspect = container.clientWidth / container.clientHeight;
    camera = new THREE.PerspectiveCamera(38, aspect, 0.5, 260);
    camera.position.set(0.5, 20, 26);"""

init_new = """    // 1. Scene
    scene = new THREE.Scene();
    // 移除會泛白沖淡天空的舊霧氣，改用清澈深邃的環境底色
    scene.background = new THREE.Color(0x060919);

    // 2. Camera (設定與示意圖一致的原生 16:9 電影級廣角俯瞰低仰角)
    const aspect = container.clientWidth / container.clientHeight;
    camera = new THREE.PerspectiveCamera(36, aspect, 0.5, 380);
    camera.position.set(0.5, 16.8, 30.5);
    cameraLookAt.set(0.5, 2.3, 0);"""

text = text.replace(init_old, init_new)

# 2. Update controls setup in init()
controls_old = """    // 5. Orbit Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.06;
    controls.maxPolarAngle = Math.PI / 2.15; // 不穿入星球水底
    controls.minDistance = 6;
    controls.maxDistance = 55;
    controls.target.copy(cameraLookAt);"""

controls_new = """    // 5. Orbit Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.06;
    controls.maxPolarAngle = Math.PI / 2.12; // 不穿入星球水底
    controls.minDistance = 8;
    controls.maxDistance = 65;
    controls.target.copy(cameraLookAt);"""

text = text.replace(controls_old, controls_new)

# 3. Define the new celestial, sky dome, rugged rocks, sheep, landmarks, and ocean section
new_core_section = """  // ══════════════════════════════════════════════════════════════════════
  // 4. 系統一：全景雙景天空穹頂 (左側金色夕陽晨曦 × 右側銀河明月星空)
  // ══════════════════════════════════════════════════════════════════════
  let skyDomeMesh, detailedMoonMesh, moonAuraMesh, sunFlareMesh;
  let lighthouseBeamMesh = null;
  let birdFlockData = null;

  function setupLightingAndCelestial() {
    // 1. 全球柔和環境光與半球光 (確保陰影面島嶼模型依然清晰可見)
    ambientLight = new THREE.AmbientLight(0xfff5ea, 0.72);
    lightsGroup.add(ambientLight);

    hemiLight = new THREE.HemisphereLight(0xfef08a, 0x1e293b, 0.68);
    lightsGroup.add(hemiLight);

    // 2. 左側金色夕陽主定向光 (溫暖金光傾瀉於左半球群島與海面)
    dirLight = new THREE.DirectionalLight(0xffd59e, 1.85);
    dirLight.position.set(-38, 16, -24);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 5;
    dirLight.shadow.camera.far = 120;
    const d = 34;
    dirLight.shadow.camera.left = -d;
    dirLight.shadow.camera.right = d;
    dirLight.shadow.camera.top = d;
    dirLight.shadow.camera.bottom = -d;
    dirLight.shadow.bias = -0.0004;
    lightsGroup.add(dirLight);

    // 3. 右側銀河明月淡藍紫冷光 (照耀右側名著群島與波光月影)
    moonLight = new THREE.DirectionalLight(0xa5b4fc, 0.95);
    moonLight.position.set(38, 28, -20);
    moonLight.castShadow = false;
    lightsGroup.add(moonLight);

    // 4. 左側夕陽 3D 發光球體與日冕
    const sunGroup = new THREE.Group();
    sunGroup.position.set(-42, 14, -52);
    
    const sunCoreGeo = new THREE.SphereGeometry(3.2, 24, 24);
    const sunCoreMat = new THREE.MeshBasicMaterial({ color: 0xfffae5 });
    const sunCore = new THREE.Mesh(sunCoreGeo, sunCoreMat);
    sunGroup.add(sunCore);

    const sunHaloGeo = new THREE.SphereGeometry(6.4, 24, 24);
    const sunHaloMat = new THREE.MeshBasicMaterial({
      color: 0xfb923c,
      transparent: true,
      opacity: 0.42,
      side: THREE.BackSide
    });
    sunFlareMesh = new THREE.Mesh(sunHaloGeo, sunHaloMat);
    sunGroup.add(sunFlareMesh);
    lightsGroup.add(sunGroup);

    // 5. 右側超精緻 3D 月亮 (程序生成月球暗斑與隕石坑紋理)
    createDetailedMoon();

    // 6. 左側夕陽天空盤旋翱翔的飛鳥群 (Silhouette Bird Flock)
    birdFlockData = createBirdFlock();

    // 7. 建立電影級全景天空穹頂 Shader
    createCinematicSkyDome();
  }

  // 電影級全景天空穹頂 Shader (完美重現示意圖：左側金黃晚霞 × 右側深邃星夜)
  function createCinematicSkyDome() {
    const skyGeo = new THREE.SphereGeometry(180, 48, 32);
    const skyMat = new THREE.ShaderMaterial({
      side: THREE.BackSide,
      depthWrite: false,
      uniforms: {
        time: { value: 0 },
        sunPos: { value: new THREE.Vector3(-42, 14, -52).normalize() },
        moonPos: { value: new THREE.Vector3(42, 32, -45).normalize() },
        cycle: { value: 0.5 }
      },
      vertexShader: `
        varying vec3 vWorldPos;
        void main() {
          vec4 worldPos = modelMatrix * vec4(position, 1.0);
          vWorldPos = worldPos.xyz;
          gl_Position = projectionMatrix * viewMatrix * worldPos;
        }
      `,
      fragmentShader: `
        varying vec3 vWorldPos;
        uniform vec3 sunPos;
        uniform vec3 moonPos;
        uniform float time;
        uniform float cycle;

        void main() {
          vec3 dir = normalize(vWorldPos);
          
          // 水平因子：左邊為夕陽 (-1.0)，右邊為星夜 (+1.0)
          float side = smoothstep(-0.45, 0.45, dir.x);
          
          // 仰角因子 (海平面到天頂)
          float elev = clamp(dir.y + 0.05, 0.0, 1.0);
          
          // ── 左側：金黃燦爛夕陽霞光漸層 ──
          vec3 cSunsetHorizon = vec3(1.0, 0.84, 0.46); // 海平線金黃陽光
          vec3 cSunsetLow     = vec3(0.98, 0.54, 0.26); // 暖橘晚霞
          vec3 cSunsetMid     = vec3(0.82, 0.35, 0.45); // 暮紫玫瑰霞
          vec3 cSunsetSky     = vec3(0.24, 0.16, 0.38); // 暮天高空深紫
          
          vec3 sunsetCol = mix(cSunsetHorizon, cSunsetLow, smoothstep(0.0, 0.16, elev));
          sunsetCol = mix(sunsetCol, cSunsetMid, smoothstep(0.16, 0.48, elev));
          sunsetCol = mix(sunsetCol, cSunsetSky, smoothstep(0.48, 0.95, elev));
          
          // 夕陽太陽光暈輝光擴散
          float sunDist = length(dir - sunPos);
          float sunCorona = exp(-sunDist * 4.8) * 1.8;
          float sunDisc = smoothstep(0.065, 0.03, sunDist) * 2.5;
          sunsetCol += vec3(1.0, 0.92, 0.7) * (sunCorona + sunDisc);
          
          // ── 右側：深邃皇家藍星空夜幕 ──
          vec3 cNightHorizon = vec3(0.08, 0.16, 0.32); // 深海靛藍
          vec3 cNightMid     = vec3(0.03, 0.06, 0.18); // 午夜群青
          vec3 cNightTop     = vec3(0.012, 0.02, 0.07); // 宇宙黑藍
          
          vec3 nightCol = mix(cNightHorizon, cNightMid, smoothstep(0.0, 0.42, elev));
          nightCol = mix(nightCol, cNightTop, smoothstep(0.42, 0.95, elev));
          
          // 月球柔和藍白光暈
          float moonDist = length(dir - moonPos);
          float moonCorona = exp(-moonDist * 4.5) * 1.1;
          nightCol += vec3(0.85, 0.92, 1.0) * moonCorona;
          
          // 左右半球自然平滑無縫溶合
          vec3 sky = mix(sunsetCol, nightCol, side);
          
          // 海平面地球大氣層輕霧朦朧感 (Atmospheric Horizon Haze)
          float haze = exp(-abs(dir.y + 0.02) * 15.0);
          vec3 hazeCol = mix(vec3(1.0, 0.8, 0.58), vec3(0.15, 0.32, 0.55), side);
          sky = mix(sky, hazeCol, haze * 0.42);
          
          gl_FragColor = vec4(sky, 1.0);
        }
      `
    });
    skyDomeMesh = new THREE.Mesh(skyGeo, skyMat);
    scene.add(skyDomeMesh);
  }

  // 3D 程序生成超精緻月亮 (包含月海與隕石坑細節)
  function createDetailedMoon() {
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    
    // 月岩基底
    ctx.fillStyle = '#e2e8f0';
    ctx.fillRect(0, 0, 512, 256);
    
    // 暗色月海 (Lunar Maria)
    ctx.fillStyle = '#94a3b8';
    const maria = [
      { x: 140, y: 100, r: 45 }, { x: 220, y: 80, r: 55 },
      { x: 190, y: 160, r: 50 }, { x: 320, y: 120, r: 40 },
      { x: 270, y: 170, r: 35 }, { x: 110, y: 150, r: 30 }
    ];
    maria.forEach(m => {
      ctx.beginPath();
      ctx.arc(m.x, m.y, m.r, 0, Math.PI * 2);
      ctx.fill();
    });
    
    // 隕石坑 (Craters)
    ctx.fillStyle = '#cbd5e1';
    for (let i = 0; i < 45; i++) {
      const cx = (i * 73) % 512;
      const cy = (i * 47) % 256;
      const cr = 4 + (i % 7) * 3;
      ctx.beginPath();
      ctx.arc(cx, cy, cr, 0, Math.PI * 2);
      ctx.fill();
    }
    
    const moonTex = new THREE.CanvasTexture(canvas);
    const moonGeo = new THREE.SphereGeometry(3.8, 32, 32);
    const moonMat = new THREE.MeshBasicMaterial({ map: moonTex, color: 0xffffff });
    detailedMoonMesh = new THREE.Mesh(moonGeo, moonMat);
    detailedMoonMesh.position.set(42, 32, -45);
    scene.add(detailedMoonMesh);

    // 外圍柔和月暈
    const auraGeo = new THREE.SphereGeometry(5.2, 24, 24);
    const auraMat = new THREE.MeshBasicMaterial({
      color: 0xbfdbfe,
      transparent: true,
      opacity: 0.38,
      side: THREE.BackSide
    });
    moonAuraMesh = new THREE.Mesh(auraGeo, auraMat);
    moonAuraMesh.position.copy(detailedMoonMesh.position);
    scene.add(moonAuraMesh);
  }

  // 飛鳥群 (翱翔於左側夕陽天際的群鳥剪影)
  function createBirdFlock() {
    const flockGroup = new THREE.Group();
    const birdGeo = new THREE.BufferGeometry();
    const birdVerts = new Float32Array([
      -0.35, 0.12, 0,
      0, 0, 0.08,
      0.35, 0.12, 0
    ]);
    birdGeo.setAttribute('position', new THREE.BufferAttribute(birdVerts, 3));
    const birdMat = new THREE.LineBasicMaterial({ color: 0x1f2937, linewidth: 2.2 });
    
    const birdMeshes = [];
    const birdCount = 20;
    for (let i = 0; i < birdCount; i++) {
      const bird = new THREE.Line(birdGeo, birdMat);
      const baseX = -22 - (i % 5) * 3.5 + Math.random() * 2;
      const baseY = 8.5 + (i * 0.45) + Math.random() * 1.5;
      const baseZ = -14 - (i * 1.2);
      bird.position.set(baseX, baseY, baseZ);
      bird.rotation.y = -0.45;
      bird.scale.setScalar(0.7 + (i % 4) * 0.18);
      bird.userData = {
        baseX, baseY, baseZ,
        phase: i * 0.4,
        speed: 0.8 + (i % 3) * 0.3
      };
      flockGroup.add(bird);
      birdMeshes.push(bird);
    }
    scene.add(flockGroup);
    return { group: flockGroup, birds: birdMeshes };
  }

  // ══════════════════════════════════════════════════════════════════════
  // 5. 系統二：璀璨星空與高密度銀河粒子帶 (Starfield & Milky Way)
  // ══════════════════════════════════════════════════════════════════════
  function createCosmicStarfield() {
    // 1. 穹頂星空 (3,500 顆閃耀恆星微粒，集中在天頂與右側星空)
    const starCount = 3500;
    const starGeo = new THREE.BufferGeometry();
    const starPositions = new Float32Array(starCount * 3);
    const starColors = new Float32Array(starCount * 3);

    for (let i = 0; i < starCount; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 0.88 + 0.12);
      const r = 78 + Math.random() * 32;

      const x = r * Math.sin(phi) * Math.cos(theta);
      const y = r * Math.cos(phi) - 2;
      const z = r * Math.sin(phi) * Math.sin(theta);

      starPositions[i * 3] = x;
      starPositions[i * 3 + 1] = y;
      starPositions[i * 3 + 2] = z;

      const tint = Math.random();
      if (tint < 0.5) {
        starColors[i * 3] = 0.98; starColors[i * 3 + 1] = 0.98; starColors[i * 3 + 2] = 1.0;
      } else if (tint < 0.8) {
        starColors[i * 3] = 0.99; starColors[i * 3 + 1] = 0.92; starColors[i * 3 + 2] = 0.72;
      } else {
        starColors[i * 3] = 0.68; starColors[i * 3 + 1] = 0.82; starColors[i * 3 + 2] = 1.0;
      }
    }

    starGeo.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
    starGeo.setAttribute('color', new THREE.BufferAttribute(starColors, 3));

    const starMat = new THREE.PointsMaterial({
      size: 1.25,
      vertexColors: true,
      transparent: true,
      opacity: 0.95,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    });
    starfieldPoints = new THREE.Points(starGeo, starMat);
    scene.add(starfieldPoints);

    // 2. 斜跨天際的高密度璀璨銀河帶 (Milky Way Ribbon: 6,000 顆彩色高斯微粒)
    const mwCount = 6000;
    const mwGeo = new THREE.BufferGeometry();
    const mwPositions = new Float32Array(mwCount * 3);
    const mwColors = new Float32Array(mwCount * 3);

    for (let i = 0; i < mwCount; i++) {
      const t = (Math.random() - 0.5) * 115;
      const u1 = Math.random(), u2 = Math.random();
      const randNorm = Math.sqrt(-2.0 * Math.log(u1 || 0.001)) * Math.cos(2.0 * Math.PI * u2);
      const spread = randNorm * 4.2;
      const depth = (Math.random() - 0.5) * 7;

      // 讓銀河從左中上方延伸劃過右後天際
      const x = t * Math.cos(0.58) - spread * Math.sin(0.58) + 12;
      const y = 46 + Math.cos(t * 0.028) * 14 + depth;
      const z = t * Math.sin(0.58) + spread * Math.cos(0.58) - 28;

      mwPositions[i * 3] = x;
      mwPositions[i * 3 + 1] = y;
      mwPositions[i * 3 + 2] = z;

      const p = Math.random();
      if (p < 0.35) {
        mwColors[i * 3] = 0.96; mwColors[i * 3 + 1] = 0.58; mwColors[i * 3 + 2] = 0.88; // 星雲粉紫
      } else if (p < 0.7) {
        mwColors[i * 3] = 0.72; mwColors[i * 3 + 1] = 0.65; mwColors[i * 3 + 2] = 1.0;  // 夢幻藍紫
      } else if (p < 0.9) {
        mwColors[i * 3] = 1.0; mwColors[i * 3 + 1] = 1.0; mwColors[i * 3 + 2] = 1.0;    // 熾熱白星
      } else {
        mwColors[i * 3] = 0.45; mwColors[i * 3 + 1] = 0.85; mwColors[i * 3 + 2] = 0.98; // 極光冰藍
      }
    }

    mwGeo.setAttribute('position', new THREE.BufferAttribute(mwPositions, 3));
    mwGeo.setAttribute('color', new THREE.BufferAttribute(mwColors, 3));

    const mwMat = new THREE.PointsMaterial({
      size: 1.55,
      vertexColors: true,
      transparent: true,
      opacity: 0.92,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    });
    milkyWayPoints = new THREE.Points(mwGeo, mwMat);
    scene.add(milkyWayPoints);
  }

  // ══════════════════════════════════════════════════════════════════════
  // 6. 系統三：深邃藍海與動態波浪起伏 (Deep Specular Ocean & Foam)
  // ══════════════════════════════════════════════════════════════════════
  let oceanOriginalVertices;

  function createAnimatedOcean() {
    const oceanGeo = new THREE.SphereGeometry(
      PLANET_RADIUS,
      144,
      108,
      0,
      Math.PI * 2,
      0,
      Math.PI * 0.48
    );

    oceanOriginalVertices = new Float32Array(oceanGeo.attributes.position.array);

    // 採用深邃皇家靛藍，高反射度以捕捉左側金陽夕照與右側皎潔月影
    const oceanMat = new THREE.MeshStandardMaterial({
      color: 0x0c2748,
      roughness: 0.12,
      metalness: 0.72,
      flatShading: false
    });

    dynamicOceanMesh = new THREE.Mesh(oceanGeo, oceanMat);
    dynamicOceanMesh.position.copy(PLANET_CENTER);
    dynamicOceanMesh.receiveShadow = true;
    scene.add(dynamicOceanMesh);
  }

  // ══════════════════════════════════════════════════════════════════════
  // 7. 系統四：立體巨石岩壁、石板地磚、路燈與示意圖經典地標
  // ══════════════════════════════════════════════════════════════════════
  function buildIslands() {
    ISLAND_DATA.forEach((island, islandIdx) => {
      const proj = hexToPlanet(island.q, island.r);
      const group = new THREE.Group();
      group.position.copy(proj.position);
      group.quaternion.copy(proj.orientation);
      group.userData = {
        islandId: island.id,
        islandData: island,
        normal: proj.normal,
        worldCenter: proj.position.clone()
      };

      // 1. 六角島嶼頂層平臺與邊緣厚度 (Beveled Hexagon Top Platform)
      const hexGeo = new THREE.CylinderGeometry(HEX_RADIUS, HEX_RADIUS * 1.02, HEX_HEIGHT, 6, 1);
      const topMat = new THREE.MeshStandardMaterial({
        color: island.color,
        roughness: 0.65,
        metalness: 0.08,
        flatShading: true
      });
      const topMesh = new THREE.Mesh(hexGeo, topMat);
      topMesh.position.y = HEX_HEIGHT / 2;
      topMesh.castShadow = true;
      topMesh.receiveShadow = true;
      group.add(topMesh);

      // 2. 基座岩石感：立體不規則天然巨石切面 (Rugged Sea-Stack Boulder Cliffs)
      addRockyCliffBase(group, HEX_RADIUS, islandIdx);

      // 3. 雙層拍岸浪花光環 (Double Concentric Shore Foam Rings)
      createShoreFoamRings(group, HEX_RADIUS, islandIdx);

      // 4. 島嶼表面鋪設微型石板地磚步道
      createWalkwayTiles(group);

      // 5. 按照示意圖配置經典地標建築、小路燈與可愛綿羊
      populateMiniatureCity(group, island, islandIdx);

      // 6. 島嶼選取反白光環 (Selection Beacon Ring)
      const ringGeo = new THREE.RingGeometry(HEX_RADIUS * 1.06, HEX_RADIUS * 1.18, 36);
      const ringMat = new THREE.MeshBasicMaterial({
        color: 0xffffff,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0,
        depthWrite: false
      });
      const ringMesh = new THREE.Mesh(ringGeo, ringMat);
      ringMesh.rotation.x = -Math.PI / 2;
      ringMesh.position.y = HEX_HEIGHT + 0.05;
      group.add(ringMesh);
      group.userData.selectionRing = ringMesh;

      // 7. CSS2D 懸浮標籤 (深古銅金邊膠囊風格，與示意圖 100% 同款)
      const badgeDiv = document.createElement('div');
      badgeDiv.className = `island-3d-badge ${island.realm}`;
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
      badgeObj.position.set(0, HEX_HEIGHT + 2.35, 0);
      group.add(badgeObj);
      badgeObjects.push(badgeDiv);

      islandsGroup.add(group);
      islandObjectsMap.set(island.id, group);
    });
  }

  // 生成立體不規則天然海蝕巨石群 (Sea-Stack Boulder Cliffs)
  function addRockyCliffBase(group, hexRadius, islandIdx) {
    const rockGroup = new THREE.Group();
    const rockCount = 14;
    
    const mat1 = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.92, metalness: 0.12, flatShading: true });
    const mat2 = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.95, metalness: 0.08, flatShading: true });
    const mat3 = new THREE.MeshStandardMaterial({ color: 0x52525b, roughness: 0.88, metalness: 0.15, flatShading: true });
    const rockMats = [mat1, mat2, mat3];

    for (let i = 0; i < rockCount; i++) {
      const angle = (i / rockCount) * Math.PI * 2 + (islandIdx * 0.42);
      const rad = hexRadius * (0.84 + Math.sin(i * 2.3 + islandIdx) * 0.18);
      const x = Math.cos(angle) * rad;
      const z = Math.sin(angle) * rad;
      const y = -0.42 - (i % 3) * 0.24;

      const size = 0.54 + ((i + islandIdx) % 5) * 0.16;
      const rockGeo = new THREE.DodecahedronGeometry(size, 1);
      
      // 隨機擾動頂點製造刀削自然岩切感
      const pos = rockGeo.attributes.position;
      for (let v = 0; v < pos.count; v++) {
        const vx = pos.getX(v), vy = pos.getY(v), vz = pos.getZ(v);
        const j = 1 + Math.sin(vx * 7 + vy * 6 + vz * 5) * 0.16;
        pos.setXYZ(v, vx * j, vy * (j * 0.82), vz * j);
      }
      rockGeo.computeVertexNormals();

      const rock = new THREE.Mesh(rockGeo, rockMats[i % 3]);
      rock.position.set(x, y, z);
      rock.rotation.set(angle * 0.6, i * 1.2, angle * 0.4);
      rock.scale.set(1.15, 1.45, 1.15);
      rock.castShadow = true;
      rock.receiveShadow = true;
      rockGroup.add(rock);
    }
    group.add(rockGroup);
  }

  // 雙層拍岸浪花光環
  function createShoreFoamRings(group, hexRadius, islandIdx) {
    const innerGeo = new THREE.RingGeometry(hexRadius * 1.01, hexRadius * 1.18, 36);
    const outerGeo = new THREE.RingGeometry(hexRadius * 1.14, hexRadius * 1.34, 36);

    const foamMat = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.55,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    });

    const innerFoam = new THREE.Mesh(innerGeo, foamMat);
    innerFoam.rotation.x = -Math.PI / 2;
    innerFoam.position.y = 0.02;
    group.add(innerFoam);

    const outerFoamMat = foamMat.clone();
    outerFoamMat.opacity = 0.35;
    const outerFoam = new THREE.Mesh(outerGeo, outerFoamMat);
    outerFoam.rotation.x = -Math.PI / 2;
    outerFoam.position.y = -0.01;
    group.add(outerFoam);

    shoreFoams.push({ mesh: innerFoam, offset: islandIdx * 0.45 });
    shoreFoams.push({ mesh: outerFoam, offset: islandIdx * 0.45 + 0.8 });
  }

  // 鋪設微型石板地磚步道
  function createWalkwayTiles(group) {
    const tileGeo = new THREE.BoxGeometry(0.24, 0.04, 0.18);
    const tileMat = new THREE.MeshStandardMaterial({
      color: 0xdfd4c4,
      roughness: 0.85,
      metalness: 0.05
    });

    const tileCoords = [
      { x: 0, z: 0.38 }, { x: 0.22, z: 0.52 }, { x: -0.22, z: 0.55 },
      { x: 0.15, z: 0.8 }, { x: -0.15, z: 0.85 }, { x: 0.35, z: 0.95 },
      { x: -0.38, z: 0.98 }, { x: 0, z: 1.15 }
    ];

    tileCoords.forEach((t) => {
      const tile = new THREE.Mesh(tileGeo, tileMat);
      tile.position.set(t.x, HEX_HEIGHT + 0.02, t.z);
      tile.rotation.y = (Math.random() - 0.5) * 0.3;
      tile.receiveShadow = true;
      group.add(tile);
    });
  }

  // 微型金屬路燈模型
  function createMiniStreetLamp(x, z) {
    const lampGroup = new THREE.Group();
    lampGroup.position.set(x, HEX_HEIGHT, z);

    const poleGeo = new THREE.CylinderGeometry(0.025, 0.035, 0.52, 6);
    const poleMat = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.4, metalness: 0.7 });
    const pole = new THREE.Mesh(poleGeo, poleMat);
    pole.position.y = 0.26;
    pole.castShadow = true;
    lampGroup.add(pole);

    const topCapGeo = new THREE.CylinderGeometry(0.08, 0.03, 0.04, 6);
    const topCap = new THREE.Mesh(topCapGeo, poleMat);
    topCap.position.y = 0.53;
    lampGroup.add(topCap);

    const bulbGeo = new THREE.SphereGeometry(0.055, 8, 8);
    const bulb = new THREE.Mesh(bulbGeo, nightGlowMaterial);
    bulb.position.y = 0.5;
    lampGroup.add(bulb);

    return lampGroup;
  }

  // 可愛毛線小羊 (Amigurumi Sheep)
  function createAmigurumiSheep(x, z, rotY) {
    const sheep = new THREE.Group();
    sheep.position.set(x, HEX_HEIGHT + 0.02, z);
    sheep.rotation.y = rotY || 0;
    sheep.scale.setScalar(0.68);

    // 蓬鬆毛線羊身
    const bodyGeo = new THREE.SphereGeometry(0.18, 8, 8);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.95 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 0.15;
    body.castShadow = true;
    sheep.add(body);

    // 黑/棕羊頭
    const headGeo = new THREE.SphereGeometry(0.085, 6, 6);
    const headMat = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.85 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.set(0, 0.19, 0.16);
    head.castShadow = true;
    sheep.add(head);

    // 4 隻黑色小木棍羊腿
    const legGeo = new THREE.CylinderGeometry(0.02, 0.02, 0.11, 4);
    const legMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.8 });
    [[-0.08, 0.07], [0.08, 0.07], [-0.08, -0.07], [0.08, -0.07]].forEach(([lx, lz]) => {
      const leg = new THREE.Mesh(legGeo, legMat);
      leg.position.set(lx, 0.055, lz);
      sheep.add(leg);
    });

    return sheep;
  }

  // 示意圖經典建築配置 (燈塔、教堂尖塔、古典涼亭花園、小屋與綿羊)
  function populateMiniatureCity(group, island, islandIdx) {
    const isWisdom = island.realm === 'wisdom';
    const mainRoofColor = island.roofColor;

    // ── 地標 1：內視鏡島經典白色觀測燈塔 (與示意圖左側同款) ──
    if (island.id === 'endoscopy') {
      const towerBaseGeo = new THREE.CylinderGeometry(0.38, 0.58, 2.3, 12);
      const towerMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.45 });
      const tower = new THREE.Mesh(towerBaseGeo, towerMat);
      tower.position.set(0, HEX_HEIGHT + 1.15, 0);
      tower.castShadow = true;
      group.add(tower);

      // 燈塔觀景台金屬圍欄環
      const railGeo = new THREE.CylinderGeometry(0.62, 0.62, 0.08, 12);
      const railMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.5, metalness: 0.6 });
      const rail = new THREE.Mesh(railGeo, railMat);
      rail.position.set(0, HEX_HEIGHT + 2.3, 0);
      group.add(rail);

      // 燈塔透光室 (發光核心)
      const lanternGeo = new THREE.CylinderGeometry(0.32, 0.32, 0.38, 8);
      const lanternMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });
      const lantern = new THREE.Mesh(lanternGeo, lanternMat);
      lantern.position.set(0, HEX_HEIGHT + 2.5, 0);
      group.add(lantern);

      // 燈塔綠色半球圓頂
      const domeGeo = new THREE.SphereGeometry(0.38, 12, 12, 0, Math.PI * 2, 0, Math.PI / 2);
      const domeMat = new THREE.MeshStandardMaterial({ color: 0x14b8a6, roughness: 0.35, metalness: 0.2 });
      const dome = new THREE.Mesh(domeGeo, domeMat);
      dome.position.set(0, HEX_HEIGHT + 2.68, 0);
      group.add(dome);

      // 燈塔旋轉探照燈光束
      const beamGeo = new THREE.ConeGeometry(2.5, 9.0, 16, 1, true);
      const beamMat = new THREE.MeshBasicMaterial({
        color: 0xfef08a,
        transparent: true,
        opacity: 0.18,
        side: THREE.DoubleSide,
        depthWrite: false,
        blending: THREE.AdditiveBlending
      });
      const beam = new THREE.Mesh(beamGeo, beamMat);
      beam.rotation.x = Math.PI / 2;
      beam.position.set(0, HEX_HEIGHT + 2.5, 4.5);
      const beamPivot = new THREE.Group();
      beamPivot.position.set(0, HEX_HEIGHT + 2.5, 0);
      beamPivot.add(beam);
      group.add(beamPivot);
      lighthouseBeamMesh = beamPivot;
    }
    // ── 地標 2：心血管島 / 常用藥物島 / 財富階梯之宏偉教堂鐘樓高塔 ──
    else if (island.id === 'hypertension' || island.id === 'drugs' || island.id === 'wealth-ladder') {
      const towerBaseGeo = new THREE.BoxGeometry(0.85, 2.2, 0.85);
      const wallMat = new THREE.MeshStandardMaterial({ color: 0xfffbeb, roughness: 0.65 });
      const towerBase = new THREE.Mesh(towerBaseGeo, wallMat);
      towerBase.position.set(0, HEX_HEIGHT + 1.1, 0);
      towerBase.castShadow = true;
      group.add(towerBase);

      // 拱窗發光面
      const winGeo = new THREE.PlaneGeometry(0.24, 0.42);
      const win1 = new THREE.Mesh(winGeo, nightGlowMaterial);
      win1.position.set(0, HEX_HEIGHT + 1.4, 0.44);
      group.add(win1);
      const win2 = win1.clone();
      win2.rotation.y = Math.PI;
      win2.position.set(0, HEX_HEIGHT + 1.4, -0.44);
      group.add(win2);

      // 陡峭紅瓦角錐尖塔
      const roofGeo = new THREE.ConeGeometry(0.72, 1.35, 4);
      const roofMat = new THREE.MeshStandardMaterial({ color: mainRoofColor, roughness: 0.5 });
      const roof = new THREE.Mesh(roofGeo, roofMat);
      roof.rotation.y = Math.PI / 4;
      roof.position.set(0, HEX_HEIGHT + 2.2 + 0.68, 0);
      roof.castShadow = true;
      group.add(roof);
    }
    // ── 地標 3：進步島 / 漫步華爾街古典羅馬圓頂涼亭 (Rotunda Gazebo) ──
    else if (island.id === 'random-walk' || island.id === 'sapiens' || island.id === 'exercise') {
      const basePlat = new THREE.Mesh(
        new THREE.CylinderGeometry(0.95, 1.0, 0.16, 12),
        new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.7 })
      );
      basePlat.position.set(0, HEX_HEIGHT + 0.08, 0);
      group.add(basePlat);

      // 6 根精緻白色古典立柱
      const colGeo = new THREE.CylinderGeometry(0.045, 0.045, 0.85, 8);
      const colMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.4 });
      for (let i = 0; i < 6; i++) {
        const a = (i / 6) * Math.PI * 2;
        const col = new THREE.Mesh(colGeo, colMat);
        col.position.set(Math.cos(a) * 0.72, HEX_HEIGHT + 0.16 + 0.42, Math.sin(a) * 0.72);
        col.castShadow = true;
        group.add(col);
      }

      // 古典青銅/彩瓦穹頂
      const domeGeo = new THREE.SphereGeometry(0.85, 12, 12, 0, Math.PI * 2, 0, Math.PI / 2);
      const domeMat = new THREE.MeshStandardMaterial({ color: mainRoofColor, roughness: 0.35, metalness: 0.3 });
      const dome = new THREE.Mesh(domeGeo, domeMat);
      dome.position.set(0, HEX_HEIGHT + 0.16 + 0.85, 0);
      dome.castShadow = true;
      group.add(dome);

      // 環繞涼亭的紫色與粉色薰衣草花叢
      [[-0.65, 0.65], [0.65, -0.65], [-0.75, -0.4], [0.8, 0.4]].forEach(([bx, bz], bi) => {
        const bush = new THREE.Mesh(
          new THREE.SphereGeometry(0.24, 8, 8),
          new THREE.MeshStandardMaterial({ color: bi % 2 === 0 ? 0xa855f7 : 0xec4899, roughness: 0.85 })
        );
        bush.position.set(bx, HEX_HEIGHT + 0.12, bz);
        group.add(bush);
      });
    }
    // ── 地標 4：知識宇宙名著懸浮魔導水晶 ──
    else if (isWisdom) {
      const bookGeo = new THREE.BoxGeometry(0.72, 0.88, 0.55);
      const bookMat = new THREE.MeshStandardMaterial({ color: mainRoofColor, roughness: 0.4 });
      const bookMesh = new THREE.Mesh(bookGeo, bookMat);
      bookMesh.position.set(0, HEX_HEIGHT + 0.45, 0);
      bookMesh.rotation.y = 0.3;
      bookMesh.castShadow = true;
      group.add(bookMesh);

      const gemGeo = new THREE.OctahedronGeometry(0.28);
      const gemMat = new THREE.MeshStandardMaterial({
        color: island.accentColor,
        roughness: 0.1,
        emissive: island.accentColor,
        emissiveIntensity: 0.55
      });
      const gem = new THREE.Mesh(gemGeo, gemMat);
      gem.position.set(0, HEX_HEIGHT + 1.35, 0);
      gem.userData = { isFloatingGem: true, baseSpeed: 1.5 + (islandIdx % 4) * 0.4 };
      group.add(gem);
    }
    // ── 預設歐洲童話風雙斜屋頂小屋 ──
    else {
      const houseGeo = new THREE.BoxGeometry(0.85, 0.72, 0.72);
      const wallMat = new THREE.MeshStandardMaterial({ color: 0xfffbeb, roughness: 0.7 });
      const house = new THREE.Mesh(houseGeo, wallMat);
      house.position.set(0, HEX_HEIGHT + 0.36, 0);
      house.castShadow = true;
      group.add(house);

      const winGeo = new THREE.PlaneGeometry(0.22, 0.28);
      const winMesh = new THREE.Mesh(winGeo, nightGlowMaterial);
      winMesh.position.set(0, HEX_HEIGHT + 0.42, 0.37);
      group.add(winMesh);

      // 煙囪
      const chimGeo = new THREE.BoxGeometry(0.12, 0.32, 0.12);
      const chimMat = new THREE.MeshStandardMaterial({ color: 0x78716c, roughness: 0.8 });
      const chim = new THREE.Mesh(chimGeo, chimMat);
      chim.position.set(0.26, HEX_HEIGHT + 0.72 + 0.22, 0.1);
      group.add(chim);

      const roofGeo = new THREE.ConeGeometry(0.68, 0.62, 4);
      const roofMat = new THREE.MeshStandardMaterial({ color: mainRoofColor, roughness: 0.6 });
      const roof = new THREE.Mesh(roofGeo, roofMat);
      roof.rotation.y = Math.PI / 4;
      roof.position.set(0, HEX_HEIGHT + 0.72 + 0.31, 0);
      roof.castShadow = true;
      group.add(roof);
    }

    // 周邊點綴配景：副屋、小樹、花叢、小路燈與可愛綿羊
    const offsets = [
      { x: 0.88, z: 0.45, type: 'house' },
      { x: -0.82, z: 0.65, type: 'tree' },
      { x: 0.65, z: -0.85, type: 'tree' },
      { x: -0.88, z: -0.55, type: 'lamp' },
      { x: 0.45, z: 0.92, type: 'lamp' },
      { x: -0.35, z: 0.95, type: 'sheep' },
      { x: 0.68, z: 0.75, type: 'flowers' }
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
        const trunkGeo = new THREE.CylinderGeometry(0.08, 0.12, 0.45, 6);
        const trunkMat = new THREE.MeshStandardMaterial({ color: 0x854d0e, roughness: 0.9 });
        const trunk = new THREE.Mesh(trunkGeo, trunkMat);
        trunk.position.set(pos.x, HEX_HEIGHT + 0.22, pos.z);
        trunk.castShadow = true;
        group.add(trunk);

        const folGeo = new THREE.SphereGeometry(0.38, 8, 8);
        const folMat = new THREE.MeshStandardMaterial({
          color: isWisdom ? 0x8b5cf6 : 0x16a34a,
          roughness: 0.8
        });
        const fol = new THREE.Mesh(folGeo, folMat);
        fol.position.set(pos.x, HEX_HEIGHT + 0.56, pos.z);
        fol.castShadow = true;
        group.add(fol);
      } else if (pos.type === 'lamp') {
        group.add(createMiniStreetLamp(pos.x, pos.z));
      } else if (pos.type === 'sheep') {
        group.add(createAmigurumiSheep(pos.x, pos.z, Math.random() * Math.PI * 2));
      } else if (pos.type === 'flowers') {
        const fMat = new THREE.MeshStandardMaterial({ color: (islandIdx % 2 === 0 ? 0xf43f5e : 0xfbbf24), roughness: 0.8 });
        const flowerCluster = new THREE.Mesh(new THREE.SphereGeometry(0.18, 6, 6), fMat);
        flowerCluster.position.set(pos.x, HEX_HEIGHT + 0.08, pos.z);
        group.add(flowerCluster);
      }
    });

    if (islandIdx % 3 === 0) {
      const pLight = new THREE.PointLight(0xffa726, 0.0, 5.5);
      pLight.position.set(0, HEX_HEIGHT + 1.2, 0);
      group.add(pLight);
      nightPointLights.push(pLight);
    }
  }
"""

# Replace the range between line 1714 and line 2223
lines = text.splitlines(True)
start_idx = None
end_idx = None

for idx, l in enumerate(lines):
    if "function setupLightingAndCelestial() {" in l and start_idx is None:
        start_idx = idx
    if "function buildBridges() {" in l and end_idx is None:
        end_idx = idx

print(f"Replacing lines {start_idx+1} to {end_idx}...")

lines[start_idx:end_idx] = [new_core_section + "\n"]
new_text = "".join(lines)

# 4. Update the animate() loop to rotate lighthouse beam & animate flying birds!
anim_hook_old = """    // 6. 漫步微型小人移動更新
    updateWalkers();"""

anim_hook_new = """    // 6. 燈塔探照光束旋轉
    if (lighthouseBeamMesh) {
      lighthouseBeamMesh.rotation.y = elapsedTime * 0.75;
    }

    // 飛鳥群煽動翅膀與翱翔
    if (birdFlockData && birdFlockData.birds) {
      birdFlockData.birds.forEach((bird) => {
        const u = bird.userData;
        bird.position.y = u.baseY + Math.sin(elapsedTime * u.speed + u.phase) * 0.35;
        bird.position.x = u.baseX + Math.cos(elapsedTime * 0.4 + u.phase) * 0.45;
        // 微微拍打雙翅
        const flap = Math.sin(elapsedTime * 6.5 + u.phase) * 0.15;
        bird.rotation.z = flap;
      });
    }

    // 漫步微型小人移動更新
    updateWalkers();"""

new_text = new_text.replace(anim_hook_old, anim_hook_new)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_text)

print("Successfully updated island.astro with cinematic visuals matching reference image!")
