import fs from 'fs';
import path from 'path';

const POSTS_DIR = './src/content/posts';
const PUBLIC_IMAGES = './public/images';
const ASSETS_IMAGES = './src/assets/images';
const DRIVE_DIR = 'G:\\我的雲端硬碟\\衛教文章圖片';

const driveExists = fs.existsSync(DRIVE_DIR);
const driveFiles = driveExists ? fs.readdirSync(DRIVE_DIR) : [];

const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));

console.log(`總共有 ${mdFiles.length} 篇 Markdown 文章。\n`);

const missingCoverProp = [];
const missingCoverFile = [];
const allPosts = [];

for (const f of mdFiles) {
  const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf-8');
  const t = content.match(/^title:\s*["']?(.+?)["']?\s*$/m)?.[1]?.trim();
  const c = content.match(/^category:\s*["']?(.+?)["']?\s*$/m)?.[1]?.trim();
  const d = content.match(/^draft:\s*(.+)$/m)?.[1]?.trim();
  const cover = content.match(/^coverImage:\s*["']?(.+?)["']?\s*$/m)?.[1]?.trim();
  const slug = content.match(/^slug:\s*["']?(.+?)["']?\s*$/m)?.[1]?.trim() || path.basename(f, '.md');

  allPosts.push({ file: f, title: t, category: c, draft: d === 'true', cover, slug });

  if (!cover) {
    missingCoverProp.push({ file: f, title: t, category: c, draft: d === 'true', slug });
  } else {
    const pubExists = fs.existsSync(path.join(PUBLIC_IMAGES, cover));
    const assetExists = fs.existsSync(path.join(ASSETS_IMAGES, cover));
    if (!pubExists && !assetExists) {
      missingCoverFile.push({ file: f, title: t, cover, category: c });
    }
  }
}

console.log(`=== 1. frontmatter 沒有 coverImage 的文章 (${missingCoverProp.length} 篇) ===`);
for (const p of missingCoverProp) {
  console.log(`- [${p.category}] "${p.title}" (draft: ${p.draft}, file: ${p.file})`);
}

console.log(`\n=== 2. frontmatter 有 coverImage 但本機找不到圖檔 (${missingCoverFile.length} 篇) ===`);
for (const p of missingCoverFile) {
  console.log(`- [${p.category}] "${p.title}" -> cover: ${p.cover}`);
}

// 檢查特定 4 篇
console.log('\n=== 3. 檢查截圖中的 4 個空白篇章 ===');
const checkTitles = [
  '【B型肝炎】Bepirovirsen 反義寡核苷酸',
  '【B型肝炎】Bepirovirsen反義寡核苷酸',
  '【PCSK9】高血脂新藥PCSK9抑制劑藥物',
  '【PCSK9】 高血脂新藥PCSK9抑制劑藥物',
  '【GLP-1】新藥、二合一與三合一受體促效劑',
  '【GLP-1】 新藥、二合一與三合一受體促效劑',
  '112年臺灣癌症登記報告'
];

for (const t of checkTitles) {
  const found = allPosts.find(p => p.title === t || p.file.includes(t));
  if (found) {
    console.log(`找到: "${found.title}" | 分類: ${found.category} | 封面: ${found.cover || '無'} | 檔名: ${found.file}`);
  }
}
