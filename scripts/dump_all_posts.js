import fs from 'fs';
import path from 'path';

const postsDir = path.resolve('src/content/posts');
const files = fs.readdirSync(postsDir);

const all = files.map(file => {
  const fullPath = path.join(postsDir, file);
  const content = fs.readFileSync(fullPath, 'utf8');
  const titleMatch = content.match(/^title:\s*["']?(.*?)["']?$/m);
  return {
    file,
    title: titleMatch ? titleMatch[1] : ''
  };
});

fs.writeFileSync('scripts/all_posts_dump.json', JSON.stringify(all, null, 2), 'utf8');
console.log('Total posts:', all.length);
