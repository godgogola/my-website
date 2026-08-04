import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '../src/content/posts');

const files = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
const catMap = {};

for (const f of files) {
  const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf-8');
  const catMatch = content.match(/^category:\s*["']?(.+?)["']?\s*$/m);
  const titleMatch = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  const cat = catMatch ? catMatch[1].trim() : '（無分類）';
  const title = titleMatch ? titleMatch[1].trim() : f;
  if (!catMap[cat]) catMap[cat] = [];
  catMap[cat].push(title);
}

const sorted = Object.keys(catMap).sort();
for (const cat of sorted) {
  console.log(`\n【${cat}】 (${catMap[cat].length} 篇)`);
  for (const t of catMap[cat]) {
    console.log(`  - ${t}`);
  }
}
