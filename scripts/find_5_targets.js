import fs from 'fs';
import path from 'path';

const postsDir = path.resolve('src/content/posts');
const files = fs.readdirSync(postsDir);

const queries = [
  '腎結石',
  '麻醉',
  '比較',
  'Erispan',
  '用藥原則'
];

const results = [];

for (const file of files) {
  const fullPath = path.join(postsDir, file);
  const content = fs.readFileSync(fullPath, 'utf8');
  const titleMatch = content.match(/^title:\s*["']?(.*?)["']?$/m);
  const title = titleMatch ? titleMatch[1] : '';
  const coverMatch = content.match(/^coverImage:\s*["']?(.*?)["']?$/m);
  const coverImage = coverMatch ? coverMatch[1] : '';

  for (const q of queries) {
    if (file.includes(q) || title.includes(q)) {
      results.push({ q, file, title, coverImage });
    }
  }
}

console.log(JSON.stringify(results, null, 2));
