import fs from 'fs';
import path from 'path';

const vaultPath = 'G:/我的雲端硬碟/Wix衛教文章';
const driveImagesPath = 'G:/我的雲端硬碟/衛教文章圖片';

console.log('Vault exists:', fs.existsSync(vaultPath));
console.log('Drive images exists:', fs.existsSync(driveImagesPath));

if (fs.existsSync(vaultPath)) {
  function scanDir(dir) {
    let results = [];
    const list = fs.readdirSync(dir, { withFileTypes: true });
    for (const item of list) {
      const full = path.join(dir, item.name);
      if (item.isDirectory()) {
        results = results.concat(scanDir(full));
      } else if (item.name.endsWith('.md')) {
        results.push({ path: full, name: item.name });
      }
    }
    return results;
  }
  const allVaultFiles = scanDir(vaultPath);
  console.log('Total MD files in vault:', allVaultFiles.length);

  const targetTitles = [
    '忙碌者高效阻力訓練',
    '進階阻力訓練',
    '基礎阻力訓練套餐',
    '基礎阻力訓練',
    '使用瘦瘦針的副作用',
    '使用瘦瘦針之前一定要常規施行腹部及甲狀腺超音波嗎',
    '隱性肥胖_亞洲人會比較容易嗎',
    '肥胖症的原因',
    '肥胖症的併發症'
  ];

  targetTitles.forEach(t => {
    const matched = allVaultFiles.filter(f => f.name.includes(t) || f.path.includes(t));
    console.log(`Target "${t}":`, matched);
  });
}
