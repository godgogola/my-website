import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = "src/pages/island.astro"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 確保全域變數中宣告了動畫清單
if "let animatedWindmills = [];" not in content:
    old_vars = "let birdFlockData = null;"
    new_vars = """let birdFlockData = null;
  let animatedWindmills = []; // { mesh, speed }
  let animatedFlags = [];     // { mesh, baseRotY, speed, phase }
  let animatedCampfires = []; // { light, baseIntensity }"""
    content = content.replace(old_vars, new_vars, 1)

# 2. 在 animate() 中加入風車、旗幟與營火的生動動畫
if "animatedWindmills.forEach" not in content:
    target_anim = "updateWalkers();"
    replacement_anim = """updateWalkers();

    // 4b. 中世紀微縮奇幻模型生機動畫 (風車旋轉、旗幟飄揚、營火微光)
    animatedWindmills.forEach((wm) => {
      wm.mesh.rotation.z += (wm.speed || 0.014);
    });
    animatedFlags.forEach((item) => {
      item.mesh.rotation.y = item.baseRotY + Math.sin(elapsedTime * (item.speed || 3.0) + (item.phase || 0)) * 0.22;
    });
    animatedCampfires.forEach((cf) => {
      cf.light.intensity = cf.baseIntensity + (Math.sin(elapsedTime * 8) + Math.cos(elapsedTime * 13)) * 0.15;
    });"""
    content = content.replace(target_anim, replacement_anim, 1)

# 3. 在 buildIslands() 開頭重置動畫清單
if "animatedWindmills = [];" not in content:
    content = content.replace("function buildIslands() {", "function buildIslands() {\n    animatedWindmills = [];\n    animatedFlags = [];\n    animatedCampfires = [];", 1)

# 4. 準備替換 populateMiniatureCity 及其相關舊 prop 函式
# 我們需要精確定位從 createCuteCapsuleProp 到 populateMiniatureCity 結尾的區塊
pattern = re.compile(r'  // ── 藥物島專屬：可愛 3D 雙色大膠囊模型 ──.*?function populateMiniatureCity\(group, island\) \{.*?\n  \}', re.DOTALL)

new_medieval_code = '''  // ══════════════════════════════════════════════════════════════════════
  // 中世紀奇幻微縮模型 (Medieval Low-Poly / Townscaper 建築群落生成模組)
  // 建築整體比例顯著放大（佔島面積 40%~60%，寬 2.8~3.6，高 2.5~4.8），高低落差極致震撼！
  // ══════════════════════════════════════════════════════════════════════

  // ── 通用輔助：隨風飄動的中世紀燕尾旗幟 ──
  function createMedievalPennant(height, color = 0x2563eb, phase = 0) {
    const flagGroup = new THREE.Group();
    const poleMat = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.8 });
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.025, height, 6), poleMat);
    pole.position.y = height / 2;
    flagGroup.add(pole);

    const tip = new THREE.Mesh(new THREE.SphereGeometry(0.045, 8, 8), new THREE.MeshStandardMaterial({ color: 0xfbbf24, metalness: 0.8, roughness: 0.3 }));
    tip.position.y = height + 0.02;
    flagGroup.add(tip);

    // 雙燕尾剪裁旗面
    const flagShape = new THREE.Shape();
    flagShape.moveTo(0, 0);
    flagShape.lineTo(0.52, -0.06);
    flagShape.lineTo(0.38, -0.16);
    flagShape.lineTo(0.52, -0.26);
    flagShape.lineTo(0, -0.26);
    flagShape.closePath();
    const flagGeo = new THREE.ShapeGeometry(flagShape);
    const flagMat = new THREE.MeshStandardMaterial({ color: color, side: THREE.DoubleSide, roughness: 0.55 });
    const flagMesh = new THREE.Mesh(flagGeo, flagMat);
    flagMesh.position.set(0.02, height, 0);
    flagGroup.add(flagMesh);

    animatedFlags.push({ mesh: flagMesh, baseRotY: 0, speed: 2.8 + Math.random() * 0.8, phase: phase });
    return flagGroup;
  }

  // ── 輔助：低多邊形斜坡瓦屋頂 ──
  function createGabledRoof(width, depth, height, color = 0x991b1b) {
    const roofMat = new THREE.MeshStandardMaterial({ color: color, roughness: 0.55, flatShading: true });
    const roofShape = new THREE.Shape();
    roofShape.moveTo(-width / 2, 0);
    roofShape.lineTo(0, height);
    roofShape.lineTo(width / 2, 0);
    roofShape.closePath();

    const extrudeSettings = { depth: depth, bevelEnabled: false };
    const roofGeo = new THREE.ExtrudeGeometry(roofShape, extrudeSettings);
    roofGeo.center();
    return new THREE.Mesh(roofGeo, roofMat);
  }

  // ══════════════════════════════════════════════════════════════════════
  // 1. 🏰 主城堡要塞生成模組 (Castle & Royal Fortress)
  // ══════════════════════════════════════════════════════════════════════
  function createCastleFortress(group, island, type = 'keep') {
    const stoneMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.72, flatShading: true });
    const stoneDarkMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.8, flatShading: true });
    const woodBeamMat = new THREE.MeshStandardMaterial({ color: 0x5c3d1e, roughness: 0.85 });
    const roofColor = type === 'keep' ? 0x1e3a8a : 0x991b1b;
    const roofConeMat = new THREE.MeshStandardMaterial({ color: roofColor, roughness: 0.55, flatShading: true });

    if (type === 'keep') {
      // ── 內視鏡島（王國主堡） / 財富階梯島 ──
      // 雄偉複合城堡群：佔島面積約 50% (3.4 x 3.4 單位)，高低差達 3.9 單位
      const castleGroup = new THREE.Group();
      castleGroup.position.set(0, HEX_HEIGHT + 0.08, 0);

      // (1) 底部加寬八角粗石基座
      const baseGeo = new THREE.CylinderGeometry(1.85, 2.05, 0.28, 8);
      const baseMesh = new THREE.Mesh(baseGeo, stoneDarkMat);
      baseMesh.position.y = 0.14;
      baseMesh.castShadow = true; baseMesh.receiveShadow = true;
      castleGroup.add(baseMesh);

      // (2) 中央雙層宏偉主堡 (Great Keep)
      const keepLower = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.45, 1.6), stoneMat);
      keepLower.position.set(0, 0.28 + 0.725, 0);
      keepLower.castShadow = true; keepLower.receiveShadow = true;
      castleGroup.add(keepLower);

      // 二樓出挑木石堞樓 (Machicolated Upper Keep)
      const keepUpper = new THREE.Mesh(new THREE.BoxGeometry(1.8, 1.0, 1.8), stoneMat);
      keepUpper.position.set(0, 0.28 + 1.45 + 0.5, 0);
      keepUpper.castShadow = true;
      castleGroup.add(keepUpper);

      // 主堡頂部一圈城垛 (Crenellations / Battlements)
      const batGeo = new THREE.BoxGeometry(0.24, 0.22, 0.14);
      for (let bi = -0.75; bi <= 0.75; bi += 0.5) {
        [-0.85, 0.85].forEach((bz) => {
          const b1 = new THREE.Mesh(batGeo, stoneDarkMat);
          b1.position.set(bi, 0.28 + 1.45 + 1.0 + 0.11, bz);
          castleGroup.add(b1);
        });
        [-0.85, 0.85].forEach((bx) => {
          const b2 = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.22, 0.24), stoneDarkMat);
          b2.position.set(bx, 0.28 + 1.45 + 1.0 + 0.11, bi);
          castleGroup.add(b2);
        });
      }

      // (3) 四個角落高聳圓柱形箭塔 (Corner Watchturrets)
      const turretOffsets = [[-0.95, -0.95], [0.95, -0.95], [-0.95, 0.95], [0.95, 0.95]];
      turretOffsets.forEach(([tx, tz], ti) => {
        const turretTower = new THREE.Mesh(new THREE.CylinderGeometry(0.30, 0.35, 3.2, 10), stoneMat);
        turretTower.position.set(tx, 0.28 + 1.6, tz);
        turretTower.castShadow = true;
        castleGroup.add(turretTower);

        // 塔頂外擴石垛圈
        const ringCorbel = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.30, 0.16, 10), stoneDarkMat);
        ringCorbel.position.set(tx, 0.28 + 3.2 + 0.08, tz);
        castleGroup.add(ringCorbel);

        // 尖長圓錐屋頂 (Cone Spire)
        const spire = new THREE.Mesh(new THREE.ConeGeometry(0.44, 1.35, 10), roofConeMat);
        spire.position.set(tx, 0.28 + 3.2 + 0.16 + 0.675, tz);
        spire.castShadow = true;
        castleGroup.add(spire);

        // 最高塔頂插上微風飄動旗幟
        if (ti === 0 || ti === 3) {
          const flag = createMedievalPennant(0.7, ti === 0 ? 0x2563eb : 0xd97706, ti * 1.5);
          flag.position.set(tx, 0.28 + 3.2 + 0.16 + 1.35, tz);
          castleGroup.add(flag);
        }
      });

      // (4) 連接箭塔之石灰色城牆與步道 (Curtain Walls)
      const wallNS = new THREE.BoxGeometry(0.24, 1.6, 1.25);
      const wallEW = new THREE.BoxGeometry(1.25, 1.6, 0.24);
      [-0.95, 0.95].forEach((wx) => {
        const w1 = new THREE.Mesh(wallNS, stoneMat);
        w1.position.set(wx, 0.28 + 0.8, 0);
        castleGroup.add(w1);
      });
      [-0.95, 0.95].forEach((wz) => {
        const w2 = new THREE.Mesh(wallEW, stoneMat);
        w2.position.set(0, 0.28 + 0.8, wz);
        castleGroup.add(w2);
      });

      // (5) 厚重木造城門與拱門 (Arched Gate & Portcullis)
      const gateWood = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.65, 0.12), woodBeamMat);
      gateWood.position.set(0, 0.28 + 0.325, 0.96);
      castleGroup.add(gateWood);

      // 城門兩側小火炬 (夜間發光)
      [-0.32, 0.32].forEach((tx) => {
        const torch = new THREE.Mesh(new THREE.SphereGeometry(0.045, 6, 6), nightGlowMaterial);
        torch.position.set(tx, 0.28 + 0.65, 1.02);
        castleGroup.add(torch);
      });

      group.add(castleGroup);
    } else {
      // ── 健檢紅字島 / 健檢項目島 / 漫步華爾街島（皇家瞭望鐘樓與修道院） ──
      const watchGroup = new THREE.Group();
      watchGroup.position.set(0, HEX_HEIGHT + 0.08, 0);

      // (1) 高聳石造瞭望大鐘樓 (Watchtower & Belfry, 高達 3.8 單位)
      const tower = new THREE.Mesh(new THREE.CylinderGeometry(0.46, 0.56, 3.6, 8), stoneMat);
      tower.position.set(0.65, 1.8, -0.2);
      tower.castShadow = true;
      watchGroup.add(tower);

      // 鐘樓閣 (Belfry Chamber)
      const belfryCorbel = new THREE.Mesh(new THREE.CylinderGeometry(0.58, 0.46, 0.22, 8), stoneDarkMat);
      belfryCorbel.position.set(0.65, 3.6 + 0.11, -0.2);
      watchGroup.add(belfryCorbel);

      // 金色小大鐘 (Golden Bell)
      const bell = new THREE.Mesh(new THREE.SphereGeometry(0.14, 8, 8), new THREE.MeshStandardMaterial({ color: 0xfbbf24, metalness: 0.85, roughness: 0.25 }));
      bell.position.set(0.65, 3.6 + 0.32, -0.2);
      watchGroup.add(bell);

      // 瞭望塔屋頂尖塔
      const towerRoof = new THREE.Mesh(new THREE.ConeGeometry(0.62, 1.4, 8), roofConeMat);
      towerRoof.position.set(0.65, 3.6 + 0.22 + 0.7, -0.2);
      towerRoof.castShadow = true;
      watchGroup.add(towerRoof);

      // 塔尖微風旗幟
      const towerFlag = createMedievalPennant(0.65, 0xb91c1c, 0.8);
      towerFlag.position.set(0.65, 3.6 + 0.22 + 1.4, -0.2);
      watchGroup.add(towerFlag);

      // (2) 側翼修道院小屋 (Attached Abbey Hall)
      const abbey = new THREE.Mesh(new THREE.BoxGeometry(1.8, 1.45, 1.35), new THREE.MeshStandardMaterial({ color: 0xf5f5f4, roughness: 0.75, flatShading: true }));
      abbey.position.set(-0.35, 0.725, 0.1);
      abbey.castShadow = true;
      watchGroup.add(abbey);

      const abbeyRoof = createGabledRoof(1.5, 1.9, 0.95, 0xb45309);
      abbeyRoof.rotation.y = Math.PI / 2;
      abbeyRoof.position.set(-0.35, 1.45 + 0.475, 0.1);
      abbeyRoof.castShadow = true;
      watchGroup.add(abbeyRoof);

      // 修道院小石煙囪
      const chimney = new THREE.Mesh(new THREE.BoxGeometry(0.24, 0.8, 0.24), stoneDarkMat);
      chimney.position.set(-0.95, 1.45 + 0.6, 0.4);
      watchGroup.add(chimney);

      // 拱形彩繪花窗 (發光)
      const rose = new THREE.Mesh(new THREE.CircleGeometry(0.24, 12), new THREE.MeshStandardMaterial({ color: 0xfbbf24, emissive: 0xfbbf24, emissiveIntensity: 0.6 }));
      rose.position.set(-0.35, 1.05, 0.78);
      watchGroup.add(rose);

      group.add(watchGroup);
    }
  }

  // ══════════════════════════════════════════════════════════════════════
  // 2. ⛪ 中世紀大教堂與煉金工坊生成模組 (Cathedral & Alchemist)
  // ══════════════════════════════════════════════════════════════════════
  function createCathedralOrAlchemy(group, island, type = 'cathedral') {
    if (type === 'cathedral') {
      // ── 慢性病島 / 糖尿病島 / 投資金律島（哥德式大教堂） ──
      // 宏偉十字結構 + 4.8 單位高聳尖塔 + 夜間發光玫瑰窗
      const cathGroup = new THREE.Group();
      cathGroup.position.set(0, HEX_HEIGHT + 0.08, 0);

      const stoneWarmMat = new THREE.MeshStandardMaterial({ color: 0xf5f5f4, roughness: 0.72, flatShading: true });
      const stoneAccentMat = new THREE.MeshStandardMaterial({ color: 0xd6d3d1, roughness: 0.75, flatShading: true });
      const roofSlateMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.55, flatShading: true });

      // (1) 十字形主殿 (Nave, 長 3.2 x 寬 1.4 x 高 1.8)
      const nave = new THREE.Mesh(new THREE.BoxGeometry(1.4, 1.8, 3.2), stoneWarmMat);
      nave.position.set(0, 0.9, 0);
      nave.castShadow = true; nave.receiveShadow = true;
      cathGroup.add(nave);

      const naveRoof = createGabledRoof(1.55, 3.3, 1.05, 0x1e293b);
      naveRoof.position.set(0, 1.8 + 0.525, 0);
      naveRoof.castShadow = true;
      cathGroup.add(naveRoof);

      // (2) 橫向側殿 (Transept, 寬 2.4 x 長 1.2 x 高 1.7)
      const transept = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.7, 1.2), stoneWarmMat);
      transept.position.set(0, 0.85, -0.2);
      transept.castShadow = true;
      cathGroup.add(transept);

      const transeptRoof = createGabledRoof(1.35, 2.5, 0.95, 0x1e293b);
      transeptRoof.rotation.y = Math.PI / 2;
      transeptRoof.position.set(0, 1.7 + 0.475, -0.2);
      transeptRoof.castShadow = true;
      cathGroup.add(transeptRoof);

      // (3) 中央穿雲哥德式尖塔 (Gothic Spire, 直指 4.7 單位)
      const towerBase = new THREE.Mesh(new THREE.BoxGeometry(0.72, 1.2, 0.72), stoneWarmMat);
      towerBase.position.set(0, 1.8 + 0.6, -0.2);
      cathGroup.add(towerBase);

      const spire = new THREE.Mesh(new THREE.ConeGeometry(0.55, 2.3, 8), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.5, flatShading: true }));
      spire.position.set(0, 1.8 + 1.2 + 1.15, -0.2);
      spire.castShadow = true;
      cathGroup.add(spire);

      // (4) 正立面發光圓形玫瑰花窗 (Luminescent Rose Window)
      const rose = new THREE.Mesh(
        new THREE.CircleGeometry(0.38, 16),
        new THREE.MeshStandardMaterial({ color: 0xf59e0b, emissive: 0xf59e0b, emissiveIntensity: 0.85 })
      );
      rose.position.set(0, 1.25, 1.61);
      cathGroup.add(rose);

      // (5) 拱形正門 (Gothic Arch Portal)
      const portal = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.75, 0.08), new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.85 }));
      portal.position.set(0, 0.375, 1.62);
      cathGroup.add(portal);

      // (6) 四座側邊飛扶壁支柱 (Flying Buttress Pinnacles)
      [[-0.85, 0.7], [0.85, 0.7], [-0.85, -1.0], [0.85, -1.0]].forEach(([px, pz]) => {
        const buttress = new THREE.Mesh(new THREE.BoxGeometry(0.22, 1.5, 0.26), stoneAccentMat);
        buttress.position.set(px, 0.75, pz);
        cathGroup.add(buttress);
        const pin = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.5, 4), roofSlateMat);
        pin.position.set(px, 1.5 + 0.25, pz);
        cathGroup.add(pin);
      });

      group.add(cathGroup);
    } else {
      // ── 藥物島 / 神經傳導島（奇幻煉金工坊與巨型藥水瓶） ──
      const alcGroup = new THREE.Group();
      alcGroup.position.set(0, HEX_HEIGHT + 0.08, 0);

      const plasterMat = new THREE.MeshStandardMaterial({ color: 0xfefce8, roughness: 0.75, flatShading: true });
      const timberMat = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.85 });

      // (1) 雙層都鐸式木石煉金小屋 (Tudor Alchemy Workshop)
      const lowerFloor = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.0, 1.4), plasterMat);
      lowerFloor.position.set(-0.35, 0.5, 0);
      lowerFloor.castShadow = true;
      alcGroup.add(lowerFloor);

      const upperFloor = new THREE.Mesh(new THREE.BoxGeometry(1.85, 1.15, 1.6), plasterMat);
      upperFloor.position.set(-0.35, 1.0 + 0.575, 0);
      upperFloor.castShadow = true;
      alcGroup.add(upperFloor);

      // 深色木條筋架裝飾線
      const frame1 = new THREE.Mesh(new THREE.BoxGeometry(1.88, 0.08, 1.62), timberMat);
      frame1.position.set(-0.35, 1.0, 0);
      alcGroup.add(frame1);

      const alcRoof = createGabledRoof(1.7, 2.0, 1.0, 0x15803d);
      alcRoof.rotation.y = Math.PI / 2;
      alcRoof.position.set(-0.35, 1.0 + 1.15 + 0.5, 0);
      alcRoof.castShadow = true;
      alcGroup.add(alcRoof);

      // 歪斜石砌高煙囪
      const chimney = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.22, 1.2, 6), new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.8 }));
      chimney.position.set(-0.95, 2.1, 0.4);
      chimney.rotation.z = -0.08;
      alcGroup.add(chimney);

      // (2) 3 個巨型可愛的「中世紀藥水瓶 (Giant Magic Potions)」
      const potions = [
        { color: 0xef4444, x: 0.82, z: 0.55, r: 0.42, name: 'Health' }, // ❤️ 生命大藥水
        { color: 0x3b82f6, x: 0.88, z: -0.32, r: 0.35, name: 'Mana' },  // 💙 魔力大藥水
        { color: 0x10b981, x: 0.38, z: 0.95, r: 0.28, name: 'Herb' }    // 💚 解毒草藥水
      ];

      potions.forEach((pot) => {
        const bottleGroup = new THREE.Group();
        bottleGroup.position.set(pot.x, 0, pot.z);

        // 半透明圓球瓶身 + 自發光
        const sphereGeo = new THREE.SphereGeometry(pot.r, 16, 16);
        const sphereMat = new THREE.MeshStandardMaterial({
          color: pot.color,
          roughness: 0.15,
          metalness: 0.1,
          transparent: true,
          opacity: 0.85,
          emissive: pot.color,
          emissiveIntensity: 0.45
        });
        const bottleSphere = new THREE.Mesh(sphereGeo, sphereMat);
        bottleSphere.position.y = pot.r;
        bottleSphere.castShadow = true;
        bottleGroup.add(bottleSphere);

        // 深木色軟木塞與圓柱瓶頸
        const neckGeo = new THREE.CylinderGeometry(pot.r * 0.38, pot.r * 0.38, pot.r * 0.45, 10);
        const corkMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.8 });
        const neck = new THREE.Mesh(neckGeo, corkMat);
        neck.position.y = pot.r * 2 + (pot.r * 0.22);
        bottleGroup.add(neck);

        const corkGeo = new THREE.CylinderGeometry(pot.r * 0.45, pot.r * 0.38, pot.r * 0.28, 10);
        const cork = new THREE.Mesh(corkGeo, new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.9 }));
        cork.position.y = pot.r * 2 + (pot.r * 0.50);
        bottleGroup.add(cork);

        alcGroup.add(bottleGroup);
      });

      // (3) 整齊藥草種植木箱 (Herb Garden Planter Boxes)
      const planterMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.85 });
      [-0.45, 0.45].forEach((pz) => {
        const box = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.18, 0.38), planterMat);
        box.position.set(-0.35, 0.09, -0.92);
        alcGroup.add(box);
      });

      group.add(alcGroup);
    }
  }

  // ══════════════════════════════════════════════════════════════════════
  // 3. 🌾 歐風風車村莊與熱鬧市集生成模組 (Windmill & Market Town)
  // ══════════════════════════════════════════════════════════════════════
  function createWindmillOrMarket(group, island, type = 'windmill') {
    if (type === 'windmill') {
      // ── 飲食島 / 腸道島 / 控糖生活島（大型高塔風車與立體小麥田） ──
      const millGroup = new THREE.Group();
      millGroup.position.set(0, HEX_HEIGHT + 0.08, 0);

      // (1) 大型石木混合風車塔 (The Grand Windmill, 佔地寬高達 2.8 單位)
      const stoneBase = new THREE.Mesh(
        new THREE.CylinderGeometry(0.65, 0.80, 1.25, 8),
        new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.65, flatShading: true })
      );
      stoneBase.position.set(-0.45, 0.625, -0.15);
      stoneBase.castShadow = true;
      millGroup.add(stoneBase);

      const woodTower = new THREE.Mesh(
        new THREE.CylinderGeometry(0.48, 0.65, 1.4, 8),
        new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.85, flatShading: true })
      );
      woodTower.position.set(-0.45, 1.25 + 0.7, -0.15);
      woodTower.castShadow = true;
      millGroup.add(woodTower);

      const millRoof = new THREE.Mesh(
        new THREE.ConeGeometry(0.58, 0.65, 8),
        new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.8 })
      );
      millRoof.position.set(-0.45, 1.25 + 1.4 + 0.325, -0.15);
      millRoof.castShadow = true;
      millGroup.add(millRoof);

      // (2) 四片大帆布風車葉片 (持續緩慢旋轉動畫, 展開直徑達 3.2 單位)
      const sailCenterGroup = new THREE.Group();
      sailCenterGroup.position.set(-0.45, 2.35, 0.38);

      const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.14, 8), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.7 }));
      hub.rotation.x = Math.PI / 2;
      sailCenterGroup.add(hub);

      const woodArmMat = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.9 });
      const sailClothMat = new THREE.MeshStandardMaterial({ color: 0xfef08a, roughness: 0.9, side: THREE.DoubleSide });

      for (let s = 0; s < 4; s++) {
        const bladeArm = new THREE.Group();
        bladeArm.rotation.z = (s * Math.PI) / 2;

        const spar = new THREE.Mesh(new THREE.BoxGeometry(0.045, 1.6, 0.03), woodArmMat);
        spar.position.set(0, 0.8, 0);
        bladeArm.add(spar);

        // 帆布葉片
        const cloth = new THREE.Mesh(new THREE.BoxGeometry(0.24, 1.25, 0.015), sailClothMat);
        cloth.position.set(0.13, 0.9, 0.01);
        bladeArm.add(cloth);

        sailCenterGroup.add(bladeArm);
      }
      millGroup.add(sailCenterGroup);
      animatedWindmills.push({ mesh: sailCenterGroup, speed: 0.016 });

      // (3) 周圍鋪設 3 塊金黃色立體小麥田區塊 (3D Golden Wheat Patches)
      const wheatMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.85, flatShading: true });
      const wheatPatch1 = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.16, 0.9), wheatMat);
      wheatPatch1.position.set(0.75, 0.08, -0.6);
      millGroup.add(wheatPatch1);

      const wheatPatch2 = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.14, 0.8), wheatMat);
      wheatPatch2.position.set(0.65, 0.07, 0.65);
      millGroup.add(wheatPatch2);

      // (4) 金黃色乾草捆 (Hay Bales) 與橡木桶
      const hayMat = new THREE.MeshStandardMaterial({ color: 0xeab308, roughness: 0.9 });
      const hay1 = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.36, 10), hayMat);
      hay1.rotation.z = Math.PI / 2;
      hay1.position.set(0.15, 0.18, 0.85);
      millGroup.add(hay1);

      // (5) 旁邊搭配 1 棟都鐸式斜屋頂農莊小屋
      const farmHovel = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.95, 0.95), new THREE.MeshStandardMaterial({ color: 0xfafaf9, roughness: 0.7 }));
      farmHovel.position.set(0.7, 0.475, 0.0);
      farmHovel.castShadow = true;
      millGroup.add(farmHovel);

      const fRoof = createGabledRoof(1.1, 1.3, 0.7, 0x854d0e);
      fRoof.rotation.y = Math.PI / 2;
      fRoof.position.set(0.7, 0.95 + 0.35, 0.0);
      millGroup.add(fRoof);

      group.add(millGroup);
    } else {
      // ── 胃部島 / 肝膽胰島 / 最重要事島（中世紀都鐸市集村莊） ──
      const mktGroup = new THREE.Group();
      mktGroup.position.set(0, HEX_HEIGHT + 0.08, 0);

      const wallMat = new THREE.MeshStandardMaterial({ color: 0xfafaf9, roughness: 0.75 });
      const woodTrim = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.85 });

      // (1) 主酒館 (The Town Inn, 兩層半高，凸肚窗，石煙囪)
      const innMain = new THREE.Mesh(new THREE.BoxGeometry(1.65, 1.35, 1.45), wallMat);
      innMain.position.set(-0.45, 0.675, -0.2);
      innMain.castShadow = true;
      mktGroup.add(innMain);

      // 木筋橫樑
      const timberBand = new THREE.Mesh(new THREE.BoxGeometry(1.68, 0.08, 1.48), woodTrim);
      timberBand.position.set(-0.45, 0.85, -0.2);
      mktGroup.add(timberBand);

      const innRoof = createGabledRoof(1.6, 1.8, 0.95, 0xb91c1c);
      innRoof.position.set(-0.45, 1.35 + 0.475, -0.2);
      innRoof.castShadow = true;
      mktGroup.add(innRoof);

      // 側翼相連矮房 (Townscaper 連棟錯落風格)
      const annex = new THREE.Mesh(new THREE.BoxGeometry(1.1, 1.0, 1.1), wallMat);
      annex.position.set(0.7, 0.5, -0.45);
      annex.castShadow = true;
      mktGroup.add(annex);

      const annexRoof = createGabledRoof(1.2, 1.25, 0.75, 0x1e3a8a);
      annexRoof.rotation.y = Math.PI / 2;
      annexRoof.position.set(0.7, 1.0 + 0.375, -0.45);
      annexRoof.castShadow = true;
      mktGroup.add(annexRoof);

      // (2) 3 座中世紀條紋布棚市集攤位 (Striped Awning Stalls)
      const stalls = [
        { x: 0.55, z: 0.65, rot: 0.2, col: 0xef4444 }, // 紅白條紋水果攤
        { x: -0.55, z: 0.85, rot: -0.3, col: 0x3b82f6 } // 藍白條紋鮮魚麵包攤
      ];

      stalls.forEach((st) => {
        const stallGroup = new THREE.Group();
        stallGroup.position.set(st.x, 0, st.z);
        stallGroup.rotation.y = st.rot;

        // 木造櫃檯
        const counter = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.38, 0.42), woodTrim);
        counter.position.y = 0.19;
        counter.castShadow = true;
        stallGroup.add(counter);

        // 遮陽棚斜頂
        const canopy = new THREE.Mesh(
          new THREE.BoxGeometry(0.76, 0.04, 0.48),
          new THREE.MeshStandardMaterial({ color: st.col, roughness: 0.6 })
        );
        canopy.position.set(0, 0.54, 0.05);
        canopy.rotation.x = 0.22;
        canopy.castShadow = true;
        stallGroup.add(canopy);

        // 4 根木支柱
        for (const px of [-0.32, 0.32]) {
          for (const pz of [-0.18, 0.18]) {
            const pole = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.52, 0.03), woodTrim);
            pole.position.set(px, 0.26, pz);
            stallGroup.add(pole);
          }
        }
        mktGroup.add(stallGroup);
      });

      // (3) 中央石砌營火 (Campfire with glowing logs)
      const firePit = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.28, 0.12, 8), new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.9 }));
      firePit.position.set(0.05, 0.06, 0.45);
      mktGroup.add(firePit);

      const fireGlow = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), new THREE.MeshBasicMaterial({ color: 0xf97316 }));
      fireGlow.position.set(0.05, 0.16, 0.45);
      mktGroup.add(fireGlow);

      const fireLight = new THREE.PointLight(0xf97316, 1.2, 4.5);
      fireLight.position.set(0.05, 0.35, 0.45);
      mktGroup.add(fireLight);
      animatedCampfires.push({ light: fireLight, baseIntensity: 1.2 });

      group.add(mktGroup);
    }
  }

  // ══════════════════════════════════════════════════════════════════════
  // 4. ⛰️ 自然奇觀與騎士競技場生成模組 (Wilderness & Knight Arena)
  // ══════════════════════════════════════════════════════════════════════
  function createArenaOrWilderness(group, island, type = 'arena') {
    if (type === 'arena') {
      // ── 運動活力島（騎士競技場） ──
      // 比武衝刺跑道 + 木造觀禮看台 + 皇家騎士尖頂帳篷 + 彩色三角掛旗
      const arenaGroup = new THREE.Group();
      arenaGroup.position.set(0, HEX_HEIGHT + 0.08, 0);

      const woodMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.85 });

      // (1) 紅土騎士衝刺比武場 (Jousting Tiltyard)
      const track = new THREE.Mesh(
        new THREE.BoxGeometry(3.2, 0.04, 1.4),
        new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.85 })
      );
      track.position.set(0, 0.02, 0);
      track.receiveShadow = true;
      arenaGroup.add(track);

      // 中央騎士木造衝刺分欄 (Tilt barrier rail)
      const tiltRail = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.22, 0.08), woodMat);
      tiltRail.position.set(0, 0.15, 0);
      tiltRail.castShadow = true;
      arenaGroup.add(tiltRail);

      // (2) 皇家觀禮看台 (Spectator Grandstand with striped canopy)
      const stand = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.45, 0.65), woodMat);
      stand.position.set(0, 0.225, -0.92);
      arenaGroup.add(stand);

      const canopy = new THREE.Mesh(
        new THREE.BoxGeometry(2.1, 0.04, 0.75),
        new THREE.MeshStandardMaterial({ color: 0x2563eb, roughness: 0.6 })
      );
      canopy.position.set(0, 0.82, -0.92);
      canopy.rotation.x = 0.12;
      arenaGroup.add(canopy);

      // (3) 圓頂尖頂中世紀騎士大帳篷 (Royal Knight Pavilion Tent)
      const tentGroup = new THREE.Group();
      tentGroup.position.set(1.15, 0, 0.55);

      const tentWall = new THREE.Mesh(
        new THREE.CylinderGeometry(0.55, 0.60, 0.75, 12),
        new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.7 })
      );
      tentWall.position.y = 0.375;
      tentWall.castShadow = true;
      tentGroup.add(tentWall);

      const tentRoof = new THREE.Mesh(
        new THREE.ConeGeometry(0.72, 0.85, 12),
        new THREE.MeshStandardMaterial({ color: 0x991b1b, roughness: 0.55, flatShading: true })
      );
      tentRoof.position.y = 0.75 + 0.425;
      tentRoof.castShadow = true;
      tentGroup.add(tentRoof);

      // 帳頂騎士燕尾旗
      const tentFlag = createMedievalPennant(0.55, 0xfbbf24, 0.5);
      tentFlag.position.set(0, 0.75 + 0.85, 0);
      tentGroup.add(tentFlag);

      arenaGroup.add(tentGroup);

      // (4) 旋轉訓練靶 (Quintain dummy)
      const dummy = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.05, 0.65, 8), woodMat);
      dummy.position.set(-1.05, 0.325, 0.55);
      arenaGroup.add(dummy);

      const targetBoard = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.28, 0.04), new THREE.MeshStandardMaterial({ color: 0xd97706 }));
      targetBoard.position.set(-1.05, 0.48, 0.55);
      arenaGroup.add(targetBoard);

      group.add(arenaGroup);
    } else {
      // ── 減重島 / 超音波島 / 高血壓島 / 高血脂島 / 肝病島 / 人類歷史島 / 留錢到死島 ──
      // 低多邊形巍峨石峰 (高達 3.4 單位) + 晶瑩層疊瀑布 + 神祕巨石陣 + 漂浮奧術水晶
      const wildGroup = new THREE.Group();
      wildGroup.position.set(0, HEX_HEIGHT + 0.08, 0);

      const rockMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.82, flatShading: true });
      const snowMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.6, flatShading: true });
      const waterTransMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.15, transparent: true, opacity: 0.88, flatShading: true });

      // (1) 低多邊形岩石巍峨山峰 (6 塊 Dodecahedron 緊密錯落咬合)
      const crags = [
        { x: -0.45, y: 1.25, z: -0.55, sx: 1.6, sy: 1.8, sz: 1.4, rx: 0.2, ry: 0.5 },
        { x: 0.35, y: 1.55, z: -0.65, sx: 1.4, sy: 2.2, sz: 1.3, rx: -0.1, ry: 1.2 },
        { x: -0.95, y: 0.85, z: -0.25, sx: 1.2, sy: 1.3, sz: 1.1, rx: 0.3, ry: -0.4 },
        { x: 0.75, y: 0.95, z: -0.15, sx: 1.1, sy: 1.4, sz: 1.0, rx: -0.2, ry: 0.8 }
      ];

      crags.forEach((c) => {
        const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(1.0, 0), rockMat);
        rock.scale.set(c.sx, c.sy, c.sz);
        rock.rotation.set(c.rx, c.ry, 0);
        rock.position.set(c.x, c.y, c.z);
        rock.castShadow = true; rock.receiveShadow = true;
        wildGroup.add(rock);
      });

      // 最高峰白雪帽 (Snow Cap)
      const snowCap = new THREE.Mesh(new THREE.DodecahedronGeometry(0.65, 0), snowMat);
      snowCap.scale.set(1.2, 0.7, 1.1);
      snowCap.position.set(0.35, 2.75, -0.65);
      wildGroup.add(snowCap);

      // (2) 立體層疊瀑布 (Cascading Waterfall) 與地面清澈潭水
      const fall = new THREE.Mesh(new THREE.BoxGeometry(0.48, 1.85, 0.15), waterTransMat);
      fall.position.set(-0.15, 0.95, -0.12);
      fall.rotation.x = 0.22;
      wildGroup.add(fall);

      // 地面鵝卵石清潭 (Pond)
      const pool = new THREE.Mesh(new THREE.CircleGeometry(0.85, 16), waterTransMat);
      pool.rotation.x = -Math.PI / 2;
      pool.position.set(-0.10, 0.03, 0.52);
      wildGroup.add(pool);

      // (3) 中世紀神祕巨石陣 (Stonehenge Trilithons)
      const stonehengeMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.9, flatShading: true });
      const trilithonAngles = [-0.6, 0.4];
      trilithonAngles.forEach((ang) => {
        const triGroup = new THREE.Group();
        triGroup.position.set(0.95 * Math.cos(ang), 0, 0.95 * Math.sin(ang) + 0.35);
        triGroup.rotation.y = -ang + Math.PI / 2;

        // 兩根立柱
        [-0.22, 0.22].forEach((px) => {
          const col = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.75, 0.18), stonehengeMat);
          col.position.set(px, 0.375, 0);
          col.castShadow = true;
          triGroup.add(col);
        });

        // 橫跨楣石 (Lintel)
        const lintel = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.18, 0.24), stonehengeMat);
        lintel.position.set(0, 0.75 + 0.09, 0);
        lintel.castShadow = true;
        triGroup.add(lintel);

        wildGroup.add(triGroup);
      });

      // 中央古代神聖祭壇石 + 懸浮奧術水晶
      const altar = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.42, 0.25, 6), stonehengeMat);
      altar.position.set(0.65, 0.125, 0.35);
      wildGroup.add(altar);

      const gem = new THREE.Mesh(
        new THREE.OctahedronGeometry(0.24),
        new THREE.MeshStandardMaterial({ color: 0x8b5cf6, emissive: 0x8b5cf6, emissiveIntensity: 0.65, roughness: 0.1 })
      );
      gem.position.set(0.65, 0.65, 0.35);
      gem.userData = { isFloatingGem: true, baseSpeed: 1.8 };
      wildGroup.add(gem);

      group.add(wildGroup);
    }
  }

  // ══════════════════════════════════════════════════════════════════════
  // 島嶼地標與微縮景觀分發核心
  // ══════════════════════════════════════════════════════════════════════
  function populateMiniatureCity(group, island) {
    const id = island.id;

    // ── 依使用者規格，精準分發 4 大中世紀模組 ──
    if (id === 'endoscopy') {
      createCastleFortress(group, island, 'keep');           // 🏰 王國主堡
    } else if (id === 'health-red' || id === 'health-check' || id === 'wealth-ladder' || id === 'random-walk') {
      createCastleFortress(group, island, 'watchtower');     // 🏰 皇家瞭望鐘樓與修道院
    } else if (id === 'chronic' || id === 'diabetes' || id === 'golden-rules') {
      createCathedralOrAlchemy(group, island, 'cathedral');  // ⛪ 哥德式大教堂
    } else if (id === 'medication' || id === 'brain-neuro') {
      createCathedralOrAlchemy(group, island, 'alchemy');    // ⛪ 煉金術士工坊與巨型藥水瓶
    } else if (id === 'diet' || id === 'intestine' || id === 'glucose') {
      createWindmillOrMarket(group, island, 'windmill');     // 🌾 大型風車與小麥田
    } else if (id === 'stomach' || id === 'liver-biliary' || id === 'most-important') {
      createWindmillOrMarket(group, island, 'market');       // 🌾 中世紀市集村莊與營火
    } else if (id === 'exercise') {
      createArenaOrWilderness(group, island, 'arena');       // ⛰️ 騎士比武競技場
    } else {
      createArenaOrWilderness(group, island, 'wilderness');  // ⛰️ 巍峨石峰瀑布與巨石陣 (減重、超音波、高血壓、高血脂、肝病、人類歷史、留錢到死)
    }

    // ── 可愛低多邊形圓球松樹 (高低錯落點綴島嶼外緣) ──
    const treePositions = [
      { x: -1.25, z: 0.95 },
      { x: 1.15, z: -1.10 },
      { x: -1.10, z: -0.90 }
    ];
    treePositions.forEach((tp, i) => {
      const tree = createCuteToyTree(tp.x, tp.z, 0.95 + (i % 2) * 0.22);
      group.add(tree);
    });

    // ── 隨機點綴 3~5 個微型小人偶 (熱鬧的中世紀小市民) ──
    const figureCount = 3 + (Math.abs(island.q * 2 + island.r) % 3);
    createMiniFigures(group, figureCount);
  }'''

if pattern.search(content):
    content = pattern.sub(new_medieval_code, content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully replaced with modular medieval architecture in island.astro!")
else:
    print("Error: Pattern not found! Let's inspect boundaries.")
