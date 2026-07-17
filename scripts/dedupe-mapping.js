/**
 * dedupe-mapping.js
 * 找出 cover-mapping.json 中重複的 file 條目，只保留第一筆，移除後續重複
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MAPPING_FILE = path.join(__dirname, 'cover-mapping.json');

const mapping = JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8'));

const seen = new Set();
const duplicates = [];
const deduped = [];

for (const entry of mapping) {
  if (seen.has(entry.file)) {
    duplicates.push(entry);
  } else {
    seen.add(entry.file);
    deduped.push(entry);
  }
}

if (duplicates.length === 0) {
  console.log('✅ 沒有發現重複條目，無需修改。');
  process.exit(0);
}

console.log(`⚠️  發現 ${duplicates.length} 筆重複條目（已移除）：\n`);
for (const d of duplicates) {
  console.log(`  ❌ ${d.file}  →  ${d.coverImage}`);
}

fs.writeFileSync(MAPPING_FILE, JSON.stringify(deduped, null, 2), 'utf8');
console.log(`\n✅ 完成！已從 ${mapping.length} 筆精簡為 ${deduped.length} 筆。`);
