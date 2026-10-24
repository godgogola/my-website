path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines(True)
start_idx = None
end_idx = None

for idx, l in enumerate(lines):
    if "function setupLightingAndCelestial() {" in l and start_idx is None:
        start_idx = idx - 2 # include let declarations
    if "function buildBridges() {" in l and end_idx is None:
        end_idx = idx

print(f"Target block: lines {start_idx+1} to {end_idx}")

new_visual_code = """  let skyDomeMesh, sunMeshGroup, moonMeshGroup;
  let birdFlockData = null;

  function setupLightingAndCelestial() {
    // 1. 全球柔和環境光與半球天光 (確保模型明亮清晰，微縮黏土感十足)
    ambientLight = new THREE.AmbientLight(0xfff7ed, 0.88);
    lightsGroup.add(ambientLight);

    hemiLight = new THREE.HemisphereLight(0xfef08a, 0x1e293b, 0.82);
    lightsGroup.add(hemiLight);

    // 2. 左側金色夕陽主定向光 (溫暖金光傾瀉於左半球群島與海面)
    dirLight = new THREE.DirectionalLight(0xffedd5, 2.1);
    dirLight.position.set(-32, 20, 14);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 5;
    dirLight.shadow.camera.far = 100;
    const d = 32;
    dirLight.shadow.camera.left = -d;
    dirLight.shadow.camera.right = d;
    dirLight.shadow.camera.top = d;
    dirLight.shadow.camera.bottom = -d;
    dirLight.shadow.bias = -0.0003;
    lightsGroup.add(dirLight);

    // 3. 右側銀河明月淡藍紫冷光 (照耀右側名著群島與波光月影)
    moonLight = new THREE.DirectionalLight(0xa5b4fc, 1.15);
    moonLight.position.set(32, 24, 14);
    moonLight.castShadow = false;
    lightsGroup.add(moonLight);

    // 4. 左側 3D 耀眼夕陽主體與金橘色日冕 (固定於左側海平線上方)
    create3DSunOnLeft();

    // 5. 右側 3D 皎潔明月與幽藍月暈 (固定於右上方深邃夜空)
    create3DMoonOnRight();

    // 6. 飛鳥群剪影 (在左側夕陽金光中振翅翱翔)
    birdFlockData = createBirdFlock();

    // 7. 電影級全景天空背景 (左側夕陽霞光 ➔ 右側午夜星空)
    createCinematicSkyDome();
  }

  // 左側 3D 耀眼夕陽主體
  function create3DSunOnLeft() {
    sunMeshGroup = new THREE.Group();
    sunMeshGroup.position.set(-46, 11, -38);

    // 熾熱白金日核
    const sunCore = new THREE.Mesh(
      new THREE.SphereGeometry(3.6, 24, 24),
      new THREE.MeshBasicMaterial({ color: 0xfffae0 })
    );
    sunMeshGroup.add(sunCore);

    // 暖金日冕光暈
    const sunGlow1 = new THREE.Mesh(
      new THREE.SphereGeometry(8.2, 24, 24),
      new THREE.MeshBasicMaterial({
        color: 0xf59e0b,
        transparent: true,
        opacity: 0.5,
        side: THREE.BackSide,
        blending: THREE.AdditiveBlending
      })
    );
    sunMeshGroup.add(sunGlow1);

    // 晚霞紅紫擴散光暈
    const sunGlow2 = new THREE.Mesh(
      new THREE.SphereGeometry(15.5, 24, 24),
      new THREE.MeshBasicMaterial({
        color: 0xdb2777,
        transparent: true,
        opacity: 0.25,
        side: THREE.BackSide,
        blending: THREE.AdditiveBlending
      })
    );
    sunMeshGroup.add(sunGlow2);

    scene.add(sunMeshGroup);
  }

  // 右側 3D 皎潔明月
  function create3DMoonOnRight() {
    moonMeshGroup = new THREE.Group();
    moonMeshGroup.position.set(38, 25, -34);

    // 繪製月球暗斑
    const mCanvas = document.createElement('canvas');
    mCanvas.width = 256; mCanvas.height = 128;
    const mctx = mCanvas.getContext('2d');
    mctx.fillStyle = '#f8fafc'; mctx.fillRect(0, 0, 256, 128);
    mctx.fillStyle = '#94a3b8';
    [[60, 40, 25], [115, 35, 32], [95, 80, 26], [165, 55, 22], [140, 95, 20]].forEach(([cx, cy, cr]) => {
      mctx.beginPath(); mctx.arc(cx, cy, cr, 0, Math.PI * 2); mctx.fill();
    });

    const moonMesh = new THREE.Mesh(
      new THREE.SphereGeometry(4.4, 32, 32),
      new THREE.MeshBasicMaterial({
        map: new THREE.CanvasTexture(mCanvas),
        color: 0xffffff
      })
    );
    moonMeshGroup.add(moonMesh);

    // 外圍柔和幽藍月暈
    const moonGlow = new THREE.Mesh(
      new THREE.SphereGeometry(7.2, 24, 24),
      new THREE.MeshBasicMaterial({
        color: 0x93c5fd,
        transparent: true,
        opacity: 0.38,
        side: THREE.BackSide,
        blending: THREE.AdditiveBlending
      })
    );
    moonMeshGroup.add(moonGlow);

    scene.add(moonMeshGroup);
  }

  // 飛鳥群剪影
  function createBirdFlock() {
    const flockGroup = new THREE.Group();
    const birdGeo = new THREE.BufferGeometry();
    const birdVerts = new Float32Array([
      -0.35, 0.12, 0,
      0, 0, 0.08,
      0.35, 0.12, 0
    ]);
    birdGeo.setAttribute('position', new THREE.BufferAttribute(birdVerts, 3));
    const birdMat = new THREE.LineBasicMaterial({ color: 0x27272a, linewidth: 2.2 });
    
    const birdMeshes = [];
    for (let i = 0; i < 20; i++) {
      const bird = new THREE.Line(birdGeo, birdMat);
      const baseX = -24 - (i % 5) * 3.6 + Math.random() * 2;
      const baseY = 8.8 + (i * 0.42) + Math.random() * 1.5;
      const baseZ = -16 - (i * 1.2);
      bird.position.set(baseX, baseY, baseZ);
      bird.rotation.y = -0.42;
      bird.scale.setScalar(0.72 + (i % 4) * 0.18);
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

  // 全景天空穹頂 Shader (左側夕陽霞光 ➔ 右側午夜星空)
  function createCinematicSkyDome() {
    const skyGeo = new THREE.SphereGeometry(150, 48, 24);
    const skyMat = new THREE.ShaderMaterial({
      side: THREE.BackSide,
      depthWrite: false,
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

        void main() {
          vec3 dir = normalize(vWorldPos);
          
          // 水平因子：左邊夕陽 (-1.0)，右邊星空 (+1.0)
          float side = smoothstep(-0.45, 0.45, dir.x);
          
          // 仰角因子
          float elev = clamp(dir.y + 0.08, 0.0, 1.0);
          
          // 左側夕陽暖金橘粉漸層
          vec3 cSunHorizon = vec3(1.0, 0.86, 0.52); // 海平線金色晨昏線
          vec3 cSunLow     = vec3(0.98, 0.52, 0.28); // 暖橘晚霞
          vec3 cSunMid     = vec3(0.82, 0.32, 0.46); // 暮紫玫瑰霞
          vec3 cSunTop     = vec3(0.25, 0.16, 0.42); // 暮天深紫
          
          vec3 sunCol = mix(cSunHorizon, cSunLow, smoothstep(0.0, 0.18, elev));
          sunCol = mix(sunCol, cSunMid, smoothstep(0.18, 0.52, elev));
          sunCol = mix(sunCol, cSunTop, smoothstep(0.52, 0.95, elev));
          
          // 右側午夜深邃群青星空
          vec3 cNightHorizon = vec3(0.09, 0.16, 0.32); // 深海靛藍
          vec3 cNightMid     = vec3(0.03, 0.06, 0.18); // 午夜群青
          vec3 cNightTop     = vec3(0.015, 0.02, 0.07); // 宇宙深黑
          
          vec3 nightCol = mix(cNightHorizon, cNightMid, smoothstep(0.0, 0.45, elev));
          nightCol = mix(nightCol, cNightTop, smoothstep(0.45, 0.95, elev));
          
          // 左右平滑溶合
          vec3 sky = mix(sunCol, nightCol, side);
          
          // 大氣地平線輕微發光
          float haze = exp(-abs(dir.y + 0.02) * 16.0);
          vec3 hazeCol = mix(vec3(1.0, 0.82, 0.6), vec3(0.18, 0.32, 0.55), side);
          sky = mix(sky, hazeCol, haze * 0.45);
          
          gl_FragColor = vec4(sky, 1.0);
        }
      `
    });
    skyDomeMesh = new THREE.Mesh(skyGeo, skyMat);
    scene.add(skyDomeMesh);
  }

  // ══════════════════════════════════════════════════════════════════════
  // 5. 系統二：額外立體星空與銀河粒子帶 (Starfield & Milky Way)
  // ══════════════════════════════════════════════════════════════════════
  function createCosmicStarfield() {
    // 1. 穹頂星星 (2,400 顆集中在右側夜空)
    const starCount = 2400;
    const starGeo = new THREE.BufferGeometry();
    const starPositions = new Float32Array(starCount * 3);
    const starColors = new Float32Array(starCount * 3);

    for (let i = 0; i < starCount; i++) {
      const theta = Math.PI * 0.1 + Math.random() * Math.PI * 0.9;
      const phi = Math.acos(Math.random() * 0.82 + 0.18);
      const r = 70 + Math.random() * 30;

      starPositions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      starPositions[i * 3 + 1] = r * Math.cos(phi) - 2;
      starPositions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);

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

    // 2. 斜跨天際的高密度璀璨銀河帶 (Milky Way Ribbon: 5,500 顆彩色高斯微粒)
    const mwCount = 5500;
    const mwGeo = new THREE.BufferGeometry();
    const mwPositions = new Float32Array(mwCount * 3);
    const mwColors = new Float32Array(mwCount * 3);

    for (let i = 0; i < mwCount; i++) {
      const t = (Math.random() - 0.5) * 115;
      const u1 = Math.random(), u2 = Math.random();
      const randNorm = Math.sqrt(-2.0 * Math.log(u1 || 0.001)) * Math.cos(2.0 * Math.PI * u2);
      const spread = randNorm * 4.2;
      const depth = (Math.random() - 0.5) * 7;

      const x = t * Math.cos(0.58) - spread * Math.sin(0.58) + 14;
      const y = 45 + Math.cos(t * 0.028) * 14 + depth;
      const z = t * Math.sin(0.58) + spread * Math.cos(0.58) - 28;

      mwPositions[i * 3] = x;
      mwPositions[i * 3 + 1] = y;
      mwPositions[i * 3 + 2] = z;

      const p = Math.random();
      if (p < 0.35) {
        mwColors[i * 3] = 0.96; mwColors[i * 3 + 1] = 0.58; mwColors[i * 3 + 2] = 0.88;
      } else if (p < 0.7) {
        mwColors[i * 3] = 0.72; mwColors[i * 3 + 1] = 0.65; mwColors[i * 3 + 1] = 1.0;
      } else if (p < 0.9) {
        mwColors[i * 3] = 1.0; mwColors[i * 3 + 1] = 1.0; mwColors[i * 3 + 2] = 1.0;
      } else {
        mwColors[i * 3] = 0.45; mwColors[i * 3 + 1] = 0.85; mwColors[i * 3 + 2] = 0.98;
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
  // 6. 系統三：深邃湛藍動態波浪海面 (Deep Sapphire Ocean & Foam)
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

    // 採用深邃皇家湛藍色，折射出波光粼粼的微縮海水質感
    const oceanMat = new THREE.MeshStandardMaterial({
      color: 0x144a75,
      roughness: 0.22,
      metalness: 0.35,
      flatShading: false
    });

    dynamicOceanMesh = new THREE.Mesh(oceanGeo, oceanMat);
    dynamicOceanMesh.position.copy(PLANET_CENTER);
    dynamicOceanMesh.receiveShadow = true;
    scene.add(dynamicOceanMesh);
  }

  // ══════════════════════════════════════════════════════════════════════
  // 7. 系統四：立體海蝕巨石岩壁、石板地磚、小路燈與示意圖經典地標
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

      // 1. 六角島嶼頂層平臺與邊緣厚度
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

      // 2. 基座岩石感：立體多面海蝕天然巨石岩切面 (Sea-Stack Boulders)
      addRockyCliffBase(group, HEX_RADIUS, islandIdx);

      // 3. 雙層拍岸浪花白色光環
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
    }
    // ── 地標 2：心血管島 / 常用藥物島 / 財富階梯之宏偉教堂鐘樓高塔 ──
    else if (island.id === 'hypertension' || island.id === 'drugs' || island.id === 'wealth-ladder') {
      const towerBaseGeo = new THREE.BoxGeometry(0.85, 2.2, 0.85);
      const wallMat = new THREE.MeshStandardMaterial({ color: 0xfffbeb, roughness: 0.65 });
      const towerBase = new THREE.Mesh(towerBaseGeo, wallMat);
      towerBase.position.set(0, HEX_HEIGHT + 1.1, 0);
      towerBase.castShadow = true;
      group.add(towerBase);

      const winGeo = new THREE.PlaneGeometry(0.24, 0.42);
      const win1 = new THREE.Mesh(winGeo, nightGlowMaterial);
      win1.position.set(0, HEX_HEIGHT + 1.4, 0.44);
      group.add(win1);
      const win2 = win1.clone();
      win2.rotation.y = Math.PI;
      win2.position.set(0, HEX_HEIGHT + 1.4, -0.44);
      group.add(win2);

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

      const colGeo = new THREE.CylinderGeometry(0.045, 0.045, 0.85, 8);
      const colMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.4 });
      for (let i = 0; i < 6; i++) {
        const a = (i / 6) * Math.PI * 2;
        const col = new THREE.Mesh(colGeo, colMat);
        col.position.set(Math.cos(a) * 0.72, HEX_HEIGHT + 0.16 + 0.42, Math.sin(a) * 0.72);
        col.castShadow = true;
        group.add(col);
      }

      const domeGeo = new THREE.SphereGeometry(0.85, 12, 12, 0, Math.PI * 2, 0, Math.PI / 2);
      const domeMat = new THREE.MeshStandardMaterial({ color: mainRoofColor, roughness: 0.35, metalness: 0.3 });
      const dome = new THREE.Mesh(domeGeo, domeMat);
      dome.position.set(0, HEX_HEIGHT + 0.16 + 0.85, 0);
      dome.castShadow = true;
      group.add(dome);

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

lines[start_idx:end_idx] = [new_visual_code + "\n"]
new_text = "".join(lines)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_text)

print("Applied 3D Sun, 3D Moon, and Sky Dome successfully!")
