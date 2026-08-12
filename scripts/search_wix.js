import fs from 'fs';
import path from 'path';

function findFiles(dir, matchStr) {
  const results = [];
  function search(curr) {
    if (!fs.existsSync(curr)) return;
    const entries = fs.readdirSync(curr, { withFileTypes: true });
    for (const entry of entries) {
      const full = path.join(curr, entry.name);
      if (entry.isDirectory()) {
        search(full);
      } else if (entry.isFile()) {
        if (entry.name.includes(matchStr)) {
          results.push(full);
        }
      }
    }
  }
  search(dir);
  return results;
}

const terms = ['腎結石', '麻醉', '安眠', 'Erispan', '用藥原則'];
for (const t of terms) {
  console.log(`\n=== Term: ${t} ===`);
  const found = findFiles('G:/我的雲端硬碟/Wix衛教文章', t);
  console.log(found);
}
