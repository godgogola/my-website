import re

file_path = r"c:\Users\X1 Yoga Gen7\Desktop\Antigravity_Projects\個人網站\src\pages\island.astro"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 升級 spawnWalkers 與 updateWalkers
new_walkers_code = """  // ══════════════════════════════════════════════════════════════════════
  // 10. 地面漫步小人與小動物 (Autonomous Capsule Walkers & White Animals)
  // ══════════════════════════════════════════════════════════════════════
  function spawnWalkers() {
    const totalWalkers = 18;
    const walkerColors = [0x3b82f6, 0xef4444, 0x10b981, 0xf59e0b, 0x8b5cf6, 0xec4899, 0x06b6d4];

    // 1. 微型膠囊體小人 (頭 + 身體 + 輕微彈跳走路)
    for (let i = 0; i < totalWalkers; i++) {
      const walkerGroup = new THREE.Group();

      // 膠囊身體
      const bodyGeo = new THREE.CylinderGeometry(0.065, 0.085, 0.20, 8);
      const bodyMat = new THREE.MeshStandardMaterial({
        color: walkerColors[i % walkerColors.length],
        roughness: 0.65
      });
      const body = new THREE.Mesh(bodyGeo, bodyMat);
      body.position.y = 0.12;
      body.castShadow = true;
      walkerGroup.add(body);

      // 圓球頭部
      const headGeo = new THREE.SphereGeometry(0.075, 8, 8);
      const headMat = new THREE.MeshStandardMaterial({ color: 0xffedd5, roughness: 0.8 });
      const head = new THREE.Mesh(headGeo, headMat);
      head.position.y = 0.26;
      head.castShadow = true;
      walkerGroup.add(head);

      const island = ISLAND_DATA[i % ISLAND_DATA.length];
      const islandObj = islandObjectsMap.get(island.id);
      if (islandObj) {
        walkerGroup.position.copy(islandObj.position).addScaledVector(islandObj.userData.normal, HEX_HEIGHT);
        walkerGroup.quaternion.copy(islandObj.quaternion);
      }
      walkersGroup.add(walkerGroup);

      walkers.push({
        type: 'human',
        group: walkerGroup,
        baseMesh: body,
        headMesh: head,
        currentIsland: island.id,
        targetPos: walkerGroup.position.clone(),
        speed: 0.012 + Math.random() * 0.012,
        pauseTicks: 0,
        seed: Math.random() * 100
      });
    }

    // 2. 白色小動物 (小羊/小狗，由小方塊與圓球組成，在草地上漫步覓食)
    const animalCount = 14;
    for (let i = 0; i < animalCount; i++) {
      const animalGroup = new THREE.Group();
      const isDog = (i % 2 === 0);

      if (isDog) {
        // 微型小白狗 (方塊身軀 + 小頭 + 翹尾巴)
        const dBody = new THREE.Mesh(
          new THREE.BoxGeometry(0.18, 0.12, 0.12),
          new THREE.MeshStandardMaterial({ color: 0xfef9c3, roughness: 0.85 })
        );
        dBody.position.y = 0.09;
        dBody.castShadow = true;
        animalGroup.add(dBody);

        const dHead = new THREE.Mesh(
          new THREE.BoxGeometry(0.09, 0.09, 0.09),
          new THREE.MeshStandardMaterial({ color: 0xfef08a, roughness: 0.85 })
        );
        dHead.position.set(0.1, 0.15, 0);
        dHead.castShadow = true;
        animalGroup.add(dHead);

        const dTail = new THREE.Mesh(
          new THREE.CylinderGeometry(0.015, 0.015, 0.08, 4),
          new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.9 })
        );
        dTail.position.set(-0.1, 0.14, 0);
        dTail.rotation.z = Math.PI / 4;
        animalGroup.add(dTail);
      } else {
        // 微型小白羊 (圓球蓬鬆身軀 + 黑小臉 + 4細腿)
        const sBody = new THREE.Mesh(
          new THREE.DodecahedronGeometry(0.11, 1),
          new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.95 })
        );
        sBody.position.y = 0.10;
        sBody.castShadow = true;
        animalGroup.add(sBody);

        const sHead = new THREE.Mesh(
          new THREE.SphereGeometry(0.05, 6, 6),
          new THREE.MeshStandardMaterial({ color: 0x27272a, roughness: 0.9 })
        );
        sHead.position.set(0.09, 0.13, 0);
        animalGroup.add(sHead);
      }

      const island = ISLAND_DATA[(i * 3 + 2) % ISLAND_DATA.length];
      const islandObj = islandObjectsMap.get(island.id);
      if (islandObj) {
        animalGroup.position.copy(islandObj.position).addScaledVector(islandObj.userData.normal, HEX_HEIGHT);
        animalGroup.quaternion.copy(islandObj.quaternion);
      }
      walkersGroup.add(animalGroup);

      walkers.push({
        type: isDog ? 'dog' : 'sheep',
        group: animalGroup,
        currentIsland: island.id,
        targetPos: animalGroup.position.clone(),
        speed: 0.008 + Math.random() * 0.008,
        pauseTicks: Math.floor(Math.random() * 60),
        seed: Math.random() * 100
      });
    }
  }

  function updateWalkers() {
    if (!showWalkers) return;
    const time = clock ? clock.getElapsedTime() : 0;

    walkers.forEach((w) => {
      if (w.pauseTicks > 0) {
        w.pauseTicks--;
        // 停駐時微幅左右轉頭或低頭吃草
        if (w.type === 'sheep') {
          w.group.rotation.y += Math.sin(time * 3 + w.seed) * 0.008;
        }
        return;
      }

      const curPos = w.group.position;
      const dist = curPos.distanceTo(w.targetPos);

      if (dist < 0.12) {
        // 到達目標點，停駐片刻後隨機挑選島嶼半徑內新座標
        w.pauseTicks = Math.floor(60 + Math.random() * 140);

        const island = islandObjectsMap.get(w.currentIsland);
        if (island) {
          const origin = island.position;
          const normal = island.userData.normal;
          const tangent = new THREE.Vector3(1, 0, 0).cross(normal).normalize();
          const bitangent = new THREE.Vector3().crossVectors(normal, tangent).normalize();

          const angle = Math.random() * Math.PI * 2;
          const r = 0.35 + Math.random() * 0.95; // 限制在島嶼空地安全半徑範圍內
          w.targetPos.copy(origin)
            .addScaledVector(tangent, Math.cos(angle) * r)
            .addScaledVector(bitangent, Math.sin(angle) * r)
            .addScaledVector(normal, HEX_HEIGHT);
        }
      } else {
        // 朝目標前進，並自動調整朝向
        const dir = new THREE.Vector3().subVectors(w.targetPos, curPos).normalize();
        curPos.addScaledVector(dir, w.speed);
        w.group.lookAt(w.targetPos.clone().add(dir));

        // 輕微上下彈跳感走路動畫 (Walking Bobbing Animation)
        const bounceFreq = (w.type === 'human') ? 8.5 : 10.0;
        const bounceAmp = (w.type === 'human') ? 0.045 : 0.025;
        const bounce = Math.abs(Math.sin(time * bounceFreq + w.seed)) * bounceAmp;

        const island = islandObjectsMap.get(w.currentIsland);
        if (island) {
          // 保持貼合在六角地表高度上並疊加彈跳
          const groundPos = island.position.clone().addScaledVector(island.userData.normal, HEX_HEIGHT + bounce);
          curPos.y = groundPos.y;
        }
      }
    });
  }"""

# 替換原有的 spawnWalkers 和 updateWalkers
walker_pattern = r"// ══════════════════════════════════════════════════════════════════════\s*// 10\. 漫步微型小人[\s\S]*?function updateWalkers\(\) \{[\s\S]*?\}\s*\}\s*\}"

code = re.sub(walker_pattern, new_walkers_code, code)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Upgraded autonomous capsule walkers and white amigurumi animals with walking bounce animation successfully.")
