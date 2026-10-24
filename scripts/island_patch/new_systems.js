  // ══════════════════════════════════════════════════════════════════════
  // 13. 環湖群山 · 雲海 · 帆船 · 小島 · 鳥瞰 · 拱橋  (Heart-Island 風格升級)
  // ══════════════════════════════════════════════════════════════════════
  const HM_UP = new THREE.Vector3(0, 1, 0);

  // 平面座標 (x,z) + 沿球心外推高度 h → 星球曲面世界座標 (與 hexToPlanet 同一套弧度公式)
  function planetPoint(x, z, h = 0, out = new THREE.Vector3()) {
    const dx = x - PLANET_CENTER.x;
    const dz = z - PLANET_CENTER.z;
    const d = Math.sqrt(dx * dx + dz * dz);
    const a = d / PLANET_RADIUS;
    const k = d > 1e-6 ? Math.sin(a) / d : 0;
    const rr = PLANET_RADIUS + h;
    return out.set(
      PLANET_CENTER.x + dx * k * rr,
      PLANET_CENTER.y + Math.cos(a) * rr,
      PLANET_CENTER.z + dz * k * rr
    );
  }
  function planetNormal(p, out = new THREE.Vector3()) {
    return out.subVectors(p, PLANET_CENTER).normalize();
  }

  // ── 小工具：平滑階梯 / 雜湊雜訊 / 分形雜訊 / 固定種子亂數 ──
  const hmSmooth = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
  const hmHash = (ix, iy) => { const s = Math.sin(ix * 127.1 + iy * 311.7) * 43758.5453; return s - Math.floor(s); };
  function hmNoise(x, y) {
    const ix = Math.floor(x), iy = Math.floor(y);
    const fx = x - ix, fy = y - iy;
    const u = fx * fx * (3 - 2 * fx), v = fy * fy * (3 - 2 * fy);
    const a = hmHash(ix, iy), b = hmHash(ix + 1, iy), c = hmHash(ix, iy + 1), d = hmHash(ix + 1, iy + 1);
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
  }
  function hmFbm(x, y) {
    let s = 0, amp = 0.5, f = 1;
    for (let i = 0; i < 4; i++) { s += amp * hmNoise(x * f, y * f); f *= 2.03; amp *= 0.5; }
    return s;
  }
  function hmRng(seed) {
    let a = seed | 0;
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ══════════════════════════════════════════════════════════════════════
  // 13-1. 環湖群山地形 (群島坐落在一座被山脈環抱的湖心)
  // ══════════════════════════════════════════════════════════════════════
  const MOUNTAIN_CENTER_X = PLANET_CENTER.x;
  let mountainGroup = null;

  // 湖岸半徑隨角度起伏 (不規則湖岸線)
  function shoreRadius(th) {
    return 44 + (hmFbm(Math.cos(th) * 1.8 + 11, Math.sin(th) * 1.8 + 11) - 0.47) * 12;
  }

  const _ts = { h: 0, e: 0 };
  // 取樣地形：h = 沿球心外推高度 (相對海平面)，e = 0..1 相對海拔 (著色用)
  function terrainSample(r, th) {
    const cs = Math.cos(th), sn = Math.sin(th);
    const t = (r - shoreRadius(th)) / 18;
    if (t < 0) {
      _ts.h = -0.55 + Math.max(t, -1.2) * 0.9; // 湖底緩降
      _ts.e = -1;
      return _ts;
    }
    const wx = r * cs, wz = r * sn;
    const base = hmFbm(wx * 0.07 + 3.1, wz * 0.07 + 7.7);
    const ridge = 1 - Math.abs(2 * hmFbm(wx * 0.11 + 20, wz * 0.11 + 4) - 1);
    // 面向鏡頭的前方(sn=+1)山勢較矮，後方與側邊群山高聳，不遮擋群島
    const facing = 0.24 + 0.76 * (1 - sn) / 2;
    const rise = hmSmooth(0, 1.0, t);
    const land = (7 + 13 * base + 9 * ridge * ridge) * facing * rise;
    // 山谷「碗形」補償：抵銷星球曲率造成的下陷，讓山脈像盆地邊緣般環繞升起
    const ang = r / PLANET_RADIUS;
    const bowl = PLANET_RADIUS * (1 - Math.cos(ang)) * 0.55 * hmSmooth(0, 0.9, t);
    const taper = 1 - hmSmooth(76, 104, r) * 0.5;
    _ts.h = (-0.2 + land + bowl) * taper;
    _ts.e = Math.min(1, land / 24);
    return _ts;
  }

  const TERRAIN_STOPS = [
    [-1.0, 0xa9c5b3], [0.0, 0xe4d9ac], [0.06, 0xbdd390],
    [0.35, 0x93b56c], [0.62, 0x749d5a], [0.82, 0x9c9986], [1.0, 0xd0cec0]
  ];
  function terrainColor(e, out) {
    if (e <= TERRAIN_STOPS[0][0]) return out.set(TERRAIN_STOPS[0][1]);
    for (let i = 1; i < TERRAIN_STOPS.length; i++) {
      if (e <= TERRAIN_STOPS[i][0]) {
        const a = TERRAIN_STOPS[i - 1], b = TERRAIN_STOPS[i];
        const t = (e - a[0]) / (b[0] - a[0]);
        return out.set(a[1]).lerp(new THREE.Color(b[1]), t);
      }
    }
    return out.set(TERRAIN_STOPS[TERRAIN_STOPS.length - 1][1]);
  }

  function createMountainRing() {
    mountainGroup = new THREE.Group();
    const rnd = hmRng(20261024);

    // 徑向分層：湖心稀疏、山腳到山腰加密
    const radii = [];
    for (let r = 2; r < 36; r += 6) radii.push(r);
    for (let r = 36; r < 80; r += 1.9) radii.push(r);
    for (let r = 80; r <= 104; r += 3) radii.push(r);
    const NR = radii.length;
    const NA = 192;

    const gridP = [], gridE = [];
    for (let i = 0; i < NR; i++) {
      const rowP = [], rowE = [];
      for (let j = 0; j < NA; j++) {
        const th = (j / NA) * Math.PI * 2;
        const s = terrainSample(radii[i], th);
        rowP.push(planetPoint(MOUNTAIN_CENTER_X + radii[i] * Math.cos(th), radii[i] * Math.sin(th), s.h));
        rowE.push(s.e);
      }
      gridP.push(rowP);
      gridE.push(rowE);
    }

    const pos = [], col = [];
    const tmpC = new THREE.Color();
    const pushTri = (A, B, C, eA, eB, eC) => {
      pos.push(A.x, A.y, A.z, B.x, B.y, B.z, C.x, C.y, C.z);
      terrainColor((eA + eB + eC) / 3, tmpC);
      tmpC.offsetHSL(0, 0, (rnd() - 0.5) * 0.07);
      for (let k = 0; k < 3; k++) col.push(tmpC.r, tmpC.g, tmpC.b);
    };
    for (let i = 0; i < NR - 1; i++) {
      for (let j = 0; j < NA; j++) {
        const j2 = (j + 1) % NA;
        const a = gridP[i][j], b = gridP[i][j2], c = gridP[i + 1][j], d = gridP[i + 1][j2];
        const ea = gridE[i][j], eb = gridE[i][j2], ec = gridE[i + 1][j], ed = gridE[i + 1][j2];
        pushTri(a, b, c, ea, eb, ec);
        pushTri(b, d, c, eb, ed, ec);
      }
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.Float32BufferAttribute(col, 3));
    geo.computeVertexNormals();
    const terrainMat = new THREE.MeshStandardMaterial({ vertexColors: true, flatShading: true, roughness: 0.96, metalness: 0 });
    const terrainMesh = new THREE.Mesh(geo, terrainMat);
    terrainMesh.receiveShadow = false;
    mountainGroup.add(terrainMesh);

    // ── 針葉松林 (InstancedMesh) ──
    const pineA = new THREE.ConeGeometry(0.72, 1.35, 6); pineA.translate(0, 0.95, 0);
    const pineB = new THREE.ConeGeometry(0.52, 1.1, 6); pineB.translate(0, 1.65, 0);
    const trunk = new THREE.CylinderGeometry(0.09, 0.12, 0.5, 5); trunk.translate(0, 0.25, 0);
    const pineGeo = mergeGeometries([pineA, pineB, trunk].map(g => { const n = g.toNonIndexed(); n.deleteAttribute('uv'); return n; }));
    const roundGeo = new THREE.IcosahedronGeometry(0.62, 0); roundGeo.translate(0, 0.95, 0);
    const treeMat = new THREE.MeshStandardMaterial({ color: 0xffffff, flatShading: true, roughness: 0.92 });
    const PINE_MAX = 1500, ROUND_MAX = 320;
    const pines = new THREE.InstancedMesh(pineGeo, treeMat, PINE_MAX);
    const rounds = new THREE.InstancedMesh(roundGeo, treeMat, ROUND_MAX);
    pines.frustumCulled = false; rounds.frustumCulled = false;
    let np = 0, nr = 0;
    const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), qy = new THREE.Quaternion();
    const sc = new THREE.Vector3(), pv = new THREE.Vector3(), nv = new THREE.Vector3();
    const cA = new THREE.Color(0x3d6b43), cB = new THREE.Color(0x628f4a), cC = new THREE.Color(0x8cc05c), cD = new THREE.Color(0xb7d36a), cTmp = new THREE.Color();

    for (let tries = 0; tries < 16000 && (np < PINE_MAX || nr < ROUND_MAX); tries++) {
      const th = rnd() * Math.PI * 2;
      const r = shoreRadius(th) + 0.6 + Math.pow(rnd(), 1.25) * 46;
      if (r > 98) continue;
      const s = terrainSample(r, th);
      if (s.e < 0.025 || s.e > 0.66) continue;
      const wx = r * Math.cos(th), wz = r * Math.sin(th);
      if (hmFbm(wx * 0.17 + 50, wz * 0.17 + 50) < 0.43) continue; // 樹叢聚落
      planetPoint(MOUNTAIN_CENTER_X + wx, wz, s.h - 0.1, pv);
      planetNormal(pv, nv);
      q.setFromUnitVectors(HM_UP, nv);
      qy.setFromAxisAngle(HM_UP, rnd() * Math.PI * 2);
      q.multiply(qy);
      const size = 0.75 + rnd() * 0.95;
      sc.set(size, size * (0.85 + rnd() * 0.5), size);
      m4.compose(pv, q, sc);
      const isRound = s.e < 0.2 && nr < ROUND_MAX && rnd() < 0.3;
      if (isRound) {
        rounds.setMatrixAt(nr, m4);
        rounds.setColorAt(nr, cTmp.copy(cC).lerp(cD, rnd()));
        nr++;
      } else if (np < PINE_MAX) {
        pines.setMatrixAt(np, m4);
        pines.setColorAt(np, cTmp.copy(cA).lerp(cB, rnd()));
        np++;
      }
    }
    pines.count = np; rounds.count = nr;
    pines.instanceMatrix.needsUpdate = true; rounds.instanceMatrix.needsUpdate = true;
    if (pines.instanceColor) pines.instanceColor.needsUpdate = true;
    if (rounds.instanceColor) rounds.instanceColor.needsUpdate = true;
    mountainGroup.add(pines, rounds);

    // ── 山坡紅頂小屋 ──
    const wallMat = new THREE.MeshStandardMaterial({ color: 0xf5ecd7, roughness: 0.8, flatShading: true });
    const roofMat = new THREE.MeshStandardMaterial({ color: 0xd9603b, roughness: 0.7, flatShading: true });
    for (let i = 0, placed = 0; i < 400 && placed < 11; i++) {
      const th = rnd() * Math.PI * 2;
      if (Math.sin(th) > 0.55) continue; // 避開鏡頭前緣
      const r = shoreRadius(th) + 1.5 + rnd() * 9;
      const s = terrainSample(r, th);
      if (s.e < 0.02 || s.e > 0.3) continue;
      const house = new THREE.Group();
      const walls = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.72, 0.8), wallMat);
      walls.position.y = 0.36;
      const roof = new THREE.Mesh(new THREE.ConeGeometry(0.82, 0.62, 4), roofMat);
      roof.rotation.y = Math.PI / 4; roof.position.y = 1.02;
      house.add(walls, roof);
      planetPoint(MOUNTAIN_CENTER_X + r * Math.cos(th), r * Math.sin(th), s.h - 0.05, house.position);
      planetNormal(house.position, nv);
      house.quaternion.setFromUnitVectors(HM_UP, nv).multiply(qy.setFromAxisAngle(HM_UP, rnd() * Math.PI * 2));
      const hs = 0.9 + rnd() * 0.6;
      house.scale.setScalar(hs);
      mountainGroup.add(house);
      placed++;
    }
    scene.add(mountainGroup);
  }

  // ══════════════════════════════════════════════════════════════════════
  // 13-2. 湖心小沙洲與燈塔
  // ══════════════════════════════════════════════════════════════════════
  function createIslets() {
    const rnd = hmRng(777);
    const grp = new THREE.Group();
    const sandMat = new THREE.MeshStandardMaterial({ color: 0xe8dcae, roughness: 0.9, flatShading: true });
    const grassMat = new THREE.MeshStandardMaterial({ color: 0x9fc872, roughness: 0.9, flatShading: true });
    const trunkMat = new THREE.MeshStandardMaterial({ color: 0x7a5a3c, roughness: 0.9 });
    const leafMat = new THREE.MeshStandardMaterial({ color: 0x4f8a45, roughness: 0.9, flatShading: true });
    const redMat = new THREE.MeshStandardMaterial({ color: 0xd9603b, roughness: 0.6, flatShading: true });
    const whiteMat = new THREE.MeshStandardMaterial({ color: 0xf8f4ea, roughness: 0.6, flatShading: true });
    const N = 7;
    for (let i = 0; i < N; i++) {
      const th = (i / N) * Math.PI * 2 + 0.35 + rnd() * 0.3;
      const r = 33.6 + rnd() * 1.9;
      const rad = 1.15 + rnd() * 0.9;
      const g = new THREE.Group();
      const p = planetPoint(MOUNTAIN_CENTER_X + r * Math.cos(th), r * Math.sin(th), 0);
      g.position.copy(p);
      g.quaternion.setFromUnitVectors(HM_UP, planetNormal(p));
      const sand = new THREE.Mesh(new THREE.CylinderGeometry(rad * 0.92, rad * 1.15, 0.8, 7), sandMat);
      sand.position.y = 0.05;
      const grass = new THREE.Mesh(new THREE.CylinderGeometry(rad * 0.78, rad * 0.88, 0.2, 7), grassMat);
      grass.position.y = 0.52;
      g.add(sand, grass);
      if (i === 2) {
        // 紅白燈塔 (夜間點亮)
        const base = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.44, 0.7, 8), whiteMat); base.position.y = 0.95;
        const mid = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.34, 0.6, 8), redMat); mid.position.y = 1.6;
        const top = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.27, 0.5, 8), whiteMat); top.position.y = 2.15;
        const lamp = new THREE.Mesh(new THREE.SphereGeometry(0.2, 10, 10), nightGlowMaterial); lamp.position.y = 2.6;
        const cap = new THREE.Mesh(new THREE.ConeGeometry(0.28, 0.35, 8), redMat); cap.position.y = 2.95;
        g.add(base, mid, top, lamp, cap);
      } else {
        const trees = 1 + Math.floor(rnd() * 3);
        for (let k = 0; k < trees; k++) {
          const a = rnd() * Math.PI * 2, d = rnd() * rad * 0.45;
          const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, 0.4, 5), trunkMat);
          const lf = new THREE.Mesh(new THREE.ConeGeometry(0.34, 0.9, 6), leafMat);
          tr.position.set(Math.cos(a) * d, 0.82, Math.sin(a) * d);
          lf.position.set(Math.cos(a) * d, 1.4, Math.sin(a) * d);
          const s = 0.8 + rnd() * 0.6; tr.scale.setScalar(s); lf.scale.setScalar(s);
          g.add(tr, lf);
        }
      }
      grp.add(g);
    }
    scene.add(grp);
  }

  // ══════════════════════════════════════════════════════════════════════
  // 13-3. 雲海 (飄在群山之上，緩緩生成與消散；刻意避開鏡頭前方以免遮擋島嶼)
  // ══════════════════════════════════════════════════════════════════════
  const CLOUD_ARC_START = -3.0;
  const CLOUD_ARC_LEN = 2.85;
  function createLowPolyClouds() {
    cloudsGroup = new THREE.Group();
    const rnd = hmRng(4242);
    const cloudMat = new THREE.MeshStandardMaterial({
      color: 0xffffff, roughness: 1, transparent: true, opacity: 0.94,
      emissive: 0xffffff, emissiveIntensity: 0.14
    });
    const puffGeo = new THREE.IcosahedronGeometry(1, 2);
    const COUNT = 12;
    for (let c = 0; c < COUNT; c++) {
      const cloud = new THREE.Group();
      const puffs = 5 + Math.floor(rnd() * 4);
      for (let p = 0; p < puffs; p++) {
        const mid = 1 - Math.abs(p - (puffs - 1) / 2) / (puffs / 2);
        const rad = 1.0 + mid * 0.9 + rnd() * 0.4;
        const puff = new THREE.Mesh(puffGeo, cloudMat);
        puff.position.set((p - (puffs - 1) / 2) * 1.55 + (rnd() - 0.5) * 0.5, mid * 0.5 + (rnd() - 0.5) * 0.3, (rnd() - 0.5) * 1.1);
        puff.scale.set(rad * 1.25, rad * 0.78, rad);
        cloud.add(puff);
      }
      cloud.userData = {
        p0: rnd(),
        speed: 0.0030 + rnd() * 0.0030,
        r: 40 + rnd() * 26,
        lift: 5 + rnd() * 9,
        size: 1.0 + rnd() * 0.9
      };
      cloudsGroup.add(cloud);
    }
    scene.add(cloudsGroup);
  }

  const _cloudN = new THREE.Vector3();
  function updateCloudDrift(t) {
    if (!cloudsGroup) return;
    cloudsGroup.children.forEach((cloud) => {
      const u = cloud.userData;
      const p = (u.p0 + t * u.speed) % 1;
      const th = CLOUD_ARC_START + p * CLOUD_ARC_LEN;
      const s = terrainSample(u.r, th);
      const h = Math.max(s.h, 0) + u.lift;
      planetPoint(MOUNTAIN_CENTER_X + u.r * Math.cos(th), u.r * Math.sin(th), h, cloud.position);
      cloud.quaternion.setFromUnitVectors(HM_UP, planetNormal(cloud.position, _cloudN));
      const fade = hmSmooth(0, 0.1, p) * hmSmooth(0, 0.1, 1 - p);
      cloud.scale.setScalar(Math.max(0.001, u.size * fade));
    });
  }

  // ══════════════════════════════════════════════════════════════════════
  // 13-4. 湖上帆船
  // ══════════════════════════════════════════════════════════════════════
  let boatsGroup = null;
  function createBoats() {
    boatsGroup = new THREE.Group();
    const rnd = hmRng(99);
    const hullColors = [0xdb6a41, 0x2a9d8f, 0xf4a261, 0x5b8def, 0xe76f51];
    const sailShape = new THREE.Shape();
    sailShape.moveTo(0, 0); sailShape.lineTo(0.62, 0); sailShape.lineTo(0, 1.15); sailShape.lineTo(0, 0);
    const sailGeo = new THREE.ShapeGeometry(sailShape);
    const sailMat = new THREE.MeshStandardMaterial({ color: 0xfffaf0, side: THREE.DoubleSide, roughness: 0.8 });
    const mastMat = new THREE.MeshStandardMaterial({ color: 0x6b4f3a, roughness: 0.8 });
    for (let i = 0; i < 5; i++) {
      const boat = new THREE.Group();
      const hull = new THREE.Mesh(new THREE.BoxGeometry(1.25, 0.22, 0.46),
        new THREE.MeshStandardMaterial({ color: hullColors[i % hullColors.length], roughness: 0.6, flatShading: true }));
      hull.position.y = 0.11;
      const bow = new THREE.Mesh(new THREE.ConeGeometry(0.23, 0.35, 4), hull.material);
      bow.rotation.z = -Math.PI / 2; bow.rotation.y = Math.PI / 4; bow.position.set(0.8, 0.11, 0);
      const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.03, 1.4, 5), mastMat);
      mast.position.set(0.05, 0.8, 0);
      const sail = new THREE.Mesh(sailGeo, sailMat);
      sail.position.set(0.07, 0.3, 0);
      sail.rotation.y = Math.PI / 2;
      boat.add(hull, bow, mast, sail);
      boat.scale.setScalar(0.85 + rnd() * 0.4);
      boat.userData = {
        r: 37.4 + rnd() * 1.6,
        a: rnd() * Math.PI * 2,
        speed: (0.0007 + rnd() * 0.0006) * (i % 2 ? 1 : -1),
        bob: rnd() * 6
      };
      boatsGroup.add(boat);
    }
    scene.add(boatsGroup);
  }

  const _boatQn = new THREE.Quaternion(), _boatQy = new THREE.Quaternion(), _boatN = new THREE.Vector3();
  function updateBoats(t) {
    if (!boatsGroup) return;
    boatsGroup.children.forEach((boat) => {
      const u = boat.userData;
      u.a += u.speed;
      const x = MOUNTAIN_CENTER_X + u.r * Math.cos(u.a), z = u.r * Math.sin(u.a);
      planetPoint(x, z, 0.03 + Math.sin(t * 1.6 + u.bob) * 0.05, boat.position);
      _boatQn.setFromUnitVectors(HM_UP, planetNormal(boat.position, _boatN));
      const dir = Math.sign(u.speed);
      const fx = -Math.sin(u.a) * dir, fz = Math.cos(u.a) * dir;
      _boatQy.setFromAxisAngle(HM_UP, Math.atan2(-fz, fx));
      boat.quaternion.copy(_boatQn).multiply(_boatQy);
    });
  }

  // ══════════════════════════════════════════════════════════════════════
  // 13-5. 彩色拱橋 (石橋墩 + 拼花橋面 + 雙層漸層護欄 + 夜間路燈)
  // ══════════════════════════════════════════════════════════════════════
  function paintGeo(geo, hex, x = 0, y = 0, z = 0, rotZ = 0) {
    const g = geo.index ? geo.toNonIndexed() : geo.clone();
    g.deleteAttribute('uv');
    if (rotZ) g.rotateZ(rotZ);
    g.translate(x, y, z);
    const c = new THREE.Color(hex);
    const n = g.attributes.position.count;
    const arr = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) { arr[i * 3] = c.r; arr[i * 3 + 1] = c.g; arr[i * 3 + 2] = c.b; }
    g.setAttribute('color', new THREE.BufferAttribute(arr, 3));
    return g;
  }

  function buildArchBridges(pairs) {
    const deckMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.74, metalness: 0.03, flatShading: true });
    const foamMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.5, depthWrite: false });
    const bulbGeo = new THREE.SphereGeometry(0.16, 10, 10);
    const boxGeo = new THREE.BoxGeometry(1, 1, 1);
    const WATER_Y = -(HEX_HEIGHT + 0.06 + 0.18) + 0.08;

    pairs.forEach(([idA, idB]) => {
      const objA = islandObjectsMap.get(idA);
      const objB = islandObjectsMap.get(idB);
      if (!objA || !objB) return;
      const dA = objA.userData.islandData, dB = objB.userData.islandData;
      const pA = objA.position, pB = objB.position;
      const isCross = dA.realm !== dB.realm;

      const mid = new THREE.Vector3().addVectors(pA, pB).multiplyScalar(0.5);
      const radialDir = new THREE.Vector3().subVectors(mid, PLANET_CENTER).normalize();
      const dist = pA.distanceTo(pB);
      mid.copy(PLANET_CENTER).addScaledVector(radialDir, PLANET_RADIUS + HEX_HEIGHT + 0.06);

      const bridgeGroup = new THREE.Group();
      bridgeGroup.position.copy(mid);
      const forward = new THREE.Vector3().subVectors(pB, pA).normalize();
      const right = new THREE.Vector3().crossVectors(radialDir, forward).normalize();
      const realUp = new THREE.Vector3().crossVectors(forward, right).normalize();
      bridgeGroup.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(forward, realUp, right));

      const L = dist * 0.44;
      const W = isCross ? 1.1 : 0.86;
      const rise = Math.min(0.62, 0.2 + L * 0.06);
      const T = 0.17;
      const SEG = 14;
      const archY = (u) => rise * 4 * u * (1 - u);
      const slope = (u) => Math.atan((rise * 4 * (1 - 2 * u)) / L);
      const deckHex = isCross ? 0xf0d48a : 0xece1cc;
      const stripHex = isCross ? 0xd9b968 : 0xcdbb97;
      const colA = new THREE.Color(dA.accentColor), colB = new THREE.Color(dB.accentColor);
      const parts = [];

      // 拱形橋面 (側面輪廓擠出)
      const shape = new THREE.Shape();
      shape.moveTo(-L / 2, archY(0) - T);
      for (let i = 0; i <= SEG; i++) { const u = i / SEG; shape.lineTo((u - 0.5) * L, archY(u)); }
      shape.lineTo(L / 2, archY(1) - T);
      for (let i = SEG; i >= 0; i--) { const u = i / SEG; shape.lineTo((u - 0.5) * L, archY(u) - T); }
      const deckGeo = new THREE.ExtrudeGeometry(shape, { depth: W, bevelEnabled: false, steps: 1 });
      deckGeo.translate(0, 0, -W / 2);
      parts.push(paintGeo(deckGeo, deckHex));

      // 橋面拼花橫條
      const strips = Math.max(4, Math.round(L / 0.34));
      for (let i = 1; i < strips; i++) {
        const u = i / strips;
        parts.push(paintGeo(new THREE.BoxGeometry(0.05, 0.03, W * 0.98), stripHex, (u - 0.5) * L, archY(u) + 0.012, 0, slope(u)));
      }

      // 雙側護欄：漸層彩色立柱 + 白色雙層扶手
      for (const side of [-1, 1]) {
        const z = side * (W / 2 - 0.05);
        for (let i = 0; i <= SEG; i++) {
          const u = i / SEG;
          const c = colA.clone().lerp(colB, u).lerp(new THREE.Color(0xffffff), 0.2);
          parts.push(paintGeo(new THREE.BoxGeometry(0.085, 0.38, 0.085), c, (u - 0.5) * L, archY(u) + 0.19, z));
        }
        for (let i = 0; i < SEG; i++) {
          const u0 = i / SEG, u1 = (i + 1) / SEG;
          const x0 = (u0 - 0.5) * L, x1 = (u1 - 0.5) * L;
          const y0 = archY(u0), y1 = archY(u1);
          const len = Math.hypot(x1 - x0, y1 - y0) + 0.012;
          const ang = Math.atan2(y1 - y0, x1 - x0);
          const xm = (x0 + x1) / 2, ym = (y0 + y1) / 2;
          parts.push(paintGeo(new THREE.BoxGeometry(len, 0.055, 0.065), 0xfff8ee, xm, ym + 0.37, z, ang));
          parts.push(paintGeo(new THREE.BoxGeometry(len, 0.035, 0.045), 0xe9d9bd, xm, ym + 0.19, z, ang));
        }
        // 兩側路燈燈桿 (燈球另用夜間發光材質)
        for (const u of [0.14, 0.86]) {
          parts.push(paintGeo(new THREE.CylinderGeometry(0.035, 0.045, 0.6, 6), 0x2b2b30, (u - 0.5) * L, archY(u) + 0.3, side * (W / 2 + 0.04)));
        }
      }

      // 石橋墩 + 墩帽 + 水面浪花
      const piers = L > 6 ? [0.3, 0.5, 0.7] : [0.3, 0.7];
      const foamParts = [];
      piers.forEach((u) => {
        const x = (u - 0.5) * L;
        const top = archY(u) - T + 0.02;
        const bottom = WATER_Y - 0.6;
        parts.push(paintGeo(new THREE.BoxGeometry(0.42, top - bottom, W * 0.86), 0xb5a994, x, (top + bottom) / 2, 0));
        parts.push(paintGeo(new THREE.BoxGeometry(0.62, 0.1, W * 0.96), 0xdb8a64, x, top + 0.02, 0));
        const ring = new THREE.RingGeometry(0.32, 0.62, 14).toNonIndexed();
        ring.rotateX(-Math.PI / 2);
        ring.scale(1, 1, Math.max(1, W * 1.15));
        ring.translate(x, WATER_Y, 0);
        foamParts.push(ring);
      });

      const deckMesh = new THREE.Mesh(mergeGeometries(parts), deckMat);
      deckMesh.castShadow = true;
      deckMesh.receiveShadow = true;
      bridgeGroup.add(deckMesh);
      bridgeGroup.add(new THREE.Mesh(mergeGeometries(foamParts), foamMat));

      // 夜間發光燈球
      for (const side of [-1, 1]) {
        for (const u of [0.14, 0.86]) {
          const bulb = new THREE.Mesh(bulbGeo, nightGlowMaterial);
          bulb.position.set((u - 0.5) * L, archY(u) + 0.66, side * (W / 2 + 0.04));
          bridgeGroup.add(bulb);
        }
      }
      bridgesGroup.add(bridgeGroup);
    });
  }

  // ══════════════════════════════════════════════════════════════════════
  // 13-6. 鳥瞰模式 (升空俯瞰環湖群山，並緩慢環繞)
  // ══════════════════════════════════════════════════════════════════════
  let isBirdView = false;
  function setBirdView(on) {
    isBirdView = on;
    const btn = document.getElementById('birdViewBtn');
    if (btn) btn.classList.toggle('active', on);
    if (on) {
      activeIsland = null;
      closeDetailCard();
      islandObjectsMap.forEach((obj) => { if (obj.userData.selectionRing) obj.userData.selectionRing.material.opacity = 0; });
      document.querySelectorAll('.sidebar-island-row').forEach(r => r.classList.remove('active'));
      startCameraFlight(new THREE.Vector3(2.1, 78, 24), new THREE.Vector3(2.1, -4, 3), 2200);
    } else {
      controls.autoRotate = false;
      startCameraFlight(new THREE.Vector3(2.1, 28, 48), new THREE.Vector3(2.1, 3.5, 0), 1600);
    }
  }
  function exitBirdViewSilently() {
    if (!isBirdView) return;
    isBirdView = false;
    controls.autoRotate = false;
    const btn = document.getElementById('birdViewBtn');
    if (btn) btn.classList.remove('active');
  }

