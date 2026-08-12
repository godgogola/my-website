import fs from 'fs';
import path from 'path';

const files = [
  '腹部超音波腎結石及水腎.md',
  '麻醉藥.md',
  '安眠藥安眠藥的比較.md',
  '安眠藥erispan會嗜睡.md',
  '安眠藥用藥原則.md'
];

for (const f of files) {
  const full = path.join('src/content/posts', f);
  console.log(`\n=== File: ${f} ===`);
  const c = fs.readFileSync(full, 'utf8');
  console.log(c.slice(0, 300));
}
