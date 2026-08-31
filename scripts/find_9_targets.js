const fs = require('fs');
const path = require('path');
const postsDir = path.join(process.cwd(), 'src', 'content', 'posts');
const files = fs.readdirSync(postsDir);
const targetTitles = [
  '【2026 ACSM】忙碌者高效阻力訓練',
  '【2026 ACSM】進階阻力訓練',
  '【2026 ACSM】基礎阻力訓練套餐',
  '【2026 ACSM】基礎阻力訓練',
  '【瘦瘦針】使用瘦瘦針的副作用',
  '【瘦瘦針】使用瘦瘦針之前一定要常規施行腹部及甲狀腺超音波嗎',
  '【肥胖症】隱性肥胖_亞洲人會比較容易嗎',
  '【肥胖症】肥胖症的原因',
  '【肥胖症】肥胖症的併發症'
];

targetTitles.forEach(target => {
  let found = [];
  const cleanTarget = target.replace(/[【】]/g, '').trim();
  files.forEach(f => {
    const content = fs.readFileSync(path.join(postsDir, f), 'utf-8');
    const titleMatch = content.match(/^title:\s*['"]?(.*?)['"]?$/m);
    const title = titleMatch ? titleMatch[1] : '';
    if (title === target || title.includes(cleanTarget) || f.includes(cleanTarget) || cleanTarget.includes(title)) {
      found.push({ file: f, title: title });
    }
  });
  console.log(JSON.stringify({ target, found }, null, 2));
});
