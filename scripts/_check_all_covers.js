import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const postsDir = path.join(__dirname, '../src/content/posts');
const imagesDir = path.join(__dirname, '../public/images');
const driveDir = 'G:\\我的雲端硬碟\\衛教文章圖片';

const mdFiles = fs.readdirSync(postsDir).filter(f => f.endsWith('.md'));
const imgFiles = fs.existsSync(imagesDir) ? fs.readdirSync(imagesDir) : [];
const driveFiles = fs.existsSync(driveDir) ? fs.readdirSync(driveDir) : [];

console.log('Total md files:', mdFiles.length);
console.log('Total images in public/images:', imgFiles.length);
console.log('Total images in Drive:', driveFiles.length);

let noCover = [];
let hasCover = [];
let missingPublicWebp = [];
let missingDrivePng = [];

mdFiles.forEach(f => {
  const content = fs.readFileSync(path.join(postsDir, f), 'utf8');
  const coverMatch = content.match(/^coverImage:\s*["']?(.+?)["']?\s*$/m);
  const titleMatch = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  const title = titleMatch ? titleMatch[1] : f;
  if (!coverMatch) {
    noCover.push({ f, title });
  } else {
    const rawCover = coverMatch[1].replace(/^\/images\//, '');
    const webpPath = path.join(imagesDir, rawCover);
    const hasWebp = fs.existsSync(webpPath);
    if (!hasWebp) missingPublicWebp.push({ f, title, cover: rawCover });

    const baseName = rawCover.replace(/\.webp$/, '');
    const hasDrive = driveFiles.some(df => df.startsWith(baseName) || df === `${baseName}.png`);
    if (!hasDrive) missingDrivePng.push({ f, title, baseName });

    hasCover.push({ f, title, cover: rawCover });
  }
});

console.log('\n========================================');
console.log('Posts WITH coverImage declared:', hasCover.length);
console.log('Posts WITHOUT coverImage declared:', noCover.length);
console.log('Missing public/images/*.webp:', missingPublicWebp.length);
console.log('Missing in Drive (G:\\...):', missingDrivePng.length);
console.log('========================================\n');

if (noCover.length > 0) {
  console.log('--- Posts without coverImage ---');
  noCover.forEach(x => console.log(`- [${x.f}] ${x.title}`));
}

if (missingPublicWebp.length > 0) {
  console.log('\n--- Missing WebP in public/images ---');
  missingPublicWebp.forEach(x => console.log(`- [${x.f}] Cover: ${x.cover}`));
}
