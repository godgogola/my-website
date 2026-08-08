import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '../src/content/posts');

const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
console.log(`Total MD files: ${mdFiles.length}`);

mdFiles.forEach(f => {
  const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf-8');
  const titleMatch = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  const title = titleMatch ? titleMatch[1] : f;
  console.log(`File: ${f} | Title: ${title}`);
});
