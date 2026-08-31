import fs from 'fs';
import path from 'path';

const postsDir = path.join(process.cwd(), 'src', 'content', 'posts');
const files = fs.readdirSync(postsDir);
console.log('Total files in posts:', files.length);

const list = files.map(f => {
  const content = fs.readFileSync(path.join(postsDir, f), 'utf-8');
  const titleMatch = content.match(/^title:\s*['"]?(.*?)['"]?$/m);
  return { file: f, title: titleMatch ? titleMatch[1] : '' };
});

console.log('Sample posts (first 20):', list.slice(0, 20));

// Check keywords
['ACSM', '阻力', '瘦瘦針', '肥胖', '超音波', '隱性'].forEach(kw => {
  const matched = list.filter(item => item.title.includes(kw) || item.file.includes(kw));
  console.log(`Keyword "${kw}":`, matched);
});
