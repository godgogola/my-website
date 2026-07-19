/**
 * sync-drive-images.js
 *
 * 📁 從 Google Drive「衛教文章圖片」資料夾自動同步圖片到本機：
 *   1. 複製 Google Drive 圖片 → src/assets/images/
 *   2. 找出同名的草稿文章（draft: true）→ 自動補上 coverImage
 *   3. 把 draft: true 改成 draft: false，讓文章正式上線
 *
 * 圖片命名規則：檔名（不含副檔名）需與文章 title 完全一致
 * 例如：「食道裂孔疝氣的原因.png」→ 配對 title: "食道裂孔疝氣的原因"
 *
 * 使用方式：node scripts/sync-drive-images.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '..');

// ── 設定區 ────────────────────────────────────────────────
// Google Drive 衛教文章圖片資料夾路徑
const DRIVE_IMAGES_DIR = 'G:\\我的雲端硬碟\\衛教文章圖片';

// 本機目標圖片資料夾
const LOCAL_IMAGES_DIR = path.join(PROJECT_ROOT, 'src', 'assets', 'images');

// 文章資料夾
const POSTS_DIR = path.join(PROJECT_ROOT, 'src', 'content', 'posts');

// 支援的圖片副檔名
const IMAGE_EXTS = ['.png', '.jpg', '.jpeg', '.webp'];
// ─────────────────────────────────────────────────────────

let copiedCount  = 0;
let matchedCount = 0;
let skippedCount = 0;

// ── 1. 確認 Google Drive 資料夾是否存在 ─────────────────
if (!fs.existsSync(DRIVE_IMAGES_DIR)) {
  console.log(`\n⚠️  找不到 Google Drive 圖片資料夾：`);
  console.log(`   ${DRIVE_IMAGES_DIR}`);
  console.log(`   請確認 Google Drive 已掛載且資料夾名稱正確。\n`);
  process.exit(0);
}

// ── 2. 確保本機圖片資料夾存在 ───────────────────────────
if (!fs.existsSync(LOCAL_IMAGES_DIR)) {
  fs.mkdirSync(LOCAL_IMAGES_DIR, { recursive: true });
}

// ── 3. 讀取 Google Drive 圖片清單 ───────────────────────
const driveFiles = fs.readdirSync(DRIVE_IMAGES_DIR).filter(f => {
  const ext = path.extname(f).toLowerCase();
  return IMAGE_EXTS.includes(ext);
});

if (driveFiles.length === 0) {
  console.log('\n📂 Google Drive 圖片資料夾目前沒有圖片，跳過同步。\n');
  process.exit(0);
}

console.log(`\n📂 Google Drive 圖片資料夾找到 ${driveFiles.length} 張圖片：`);
console.log(`   來源：${DRIVE_IMAGES_DIR}\n`);

// ── 4. 讀取所有文章，建立 title → 檔名 的對照表 ────────
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));

// 建立 title（normalized）→ md 檔案路徑 的 Map
const titleToPost = new Map();
for (const mdFile of mdFiles) {
  const filePath = path.join(POSTS_DIR, mdFile);
  const content  = fs.readFileSync(filePath, 'utf-8');
  const fmMatch  = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) continue;
  const fm = fmMatch[1];
  const titleMatch = fm.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  if (!titleMatch) continue;
  const title = titleMatch[1].trim();
  titleToPost.set(title, { filePath, content, fm });
}

// ── 5. 逐張圖片處理 ─────────────────────────────────────
for (const imgFile of driveFiles) {
  const srcPath  = path.join(DRIVE_IMAGES_DIR, imgFile);
  const destPath = path.join(LOCAL_IMAGES_DIR, imgFile);
  const titleKey = path.basename(imgFile, path.extname(imgFile));

  // 5a. 複製圖片到本機（若已存在則覆蓋，因可能是更新版）
  fs.copyFileSync(srcPath, destPath);
  copiedCount++;
  console.log(`📥 [複製] ${imgFile}`);

  // 5b. 尋找同名文章
  const post = titleToPost.get(titleKey);
  if (!post) {
    console.log(`   ⚠️  找不到對應文章（標題需完全一致）：「${titleKey}」`);
    skippedCount++;
    continue;
  }

  const { filePath, content, fm } = post;

  // 5c. 若已有 coverImage 且非草稿，不強制覆蓋
  const hasCover = fm.includes('coverImage:');
  const isDraft  = fm.match(/^draft:\s*true\s*$/m);

  if (hasCover && !isDraft) {
    console.log(`   ✅ 「${titleKey}」已有封面圖且已發布，跳過。`);
    skippedCount++;
    continue;
  }

  // 5d. 更新 frontmatter：加 coverImage、改 draft: false
  let newFm = fm;

  // 加 coverImage（如果沒有的話）
  if (!hasCover) {
    newFm = newFm.replace(
      /(^title:.*$)/m,
      `$1\ncoverImage: "${imgFile}"`
    );
  } else {
    // 已有 coverImage，替換成新圖片
    newFm = newFm.replace(
      /^coverImage:\s*["']?.+?["']?\s*$/m,
      `coverImage: "${imgFile}"`
    );
  }

  // 把 draft: true 改成 draft: false
  if (isDraft) {
    newFm = newFm.replace(/^draft:\s*true\s*$/m, 'draft: false');
  }

  const newContent = content.replace(
    /^---\n[\s\S]*?\n---/,
    `---\n${newFm}\n---`
  );

  fs.writeFileSync(filePath, newContent, 'utf-8');
  matchedCount++;

  console.log(`   ✅ 「${titleKey}」→ 配對成功，coverImage 已寫入${isDraft ? '，draft → false（文章正式上線！）' : ''}`);
}

// ── 6. 摘要 ─────────────────────────────────────────────
console.log('\n' + '='.repeat(50));
console.log(`📥 複製圖片：   ${copiedCount} 張`);
console.log(`✅ 成功配對：   ${matchedCount} 篇文章`);
console.log(`⏭  跳過/未配對：${skippedCount} 張`);
console.log('='.repeat(50) + '\n');
