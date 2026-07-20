/**
 * sync-sheet.js
 * 
 * 自動把新網站的「文章網址」和「圖片網址」同步到 Google Sheet（次分類工作表）。
 * 需在 GAS 裡面加入 doPost 函數才能運作。
 * 
 * 使用方式：node scripts/sync-sheet.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ── 設定區 ────────────────────────────────────────
const POSTS_DIR         = path.join(__dirname, '../src/content/posts');
const PUBLIC_IMAGES_DIR = path.join(__dirname, '../public/images');
const ASSETS_IMAGES_DIR = path.join(__dirname, '../src/assets/images');
const OG_DIR            = path.join(__dirname, '../public/og-images'); // 穩定網址用的圖片資料夾
const SITE_URL          = 'https://drhuanggi.vercel.app';
const GAS_URL           = 'https://script.google.com/macros/s/AKfycbwrDmeXp0g6DaKrbY6xbRknwFmZlwHrMnJNJFpPm9bKJ_HbESQNMrLDJYL6M2N0v0f3Sg/exec';
// ─────────────────────────────────────────────────

// 建立 og-images 資料夾（如果不存在）
if (!fs.existsSync(OG_DIR)) {
  fs.mkdirSync(OG_DIR, { recursive: true });
}

// 讀取所有文章
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));

let syncCount = 0;
let skipCount = 0;

const articlesToSync = [];

for (const mdFile of mdFiles) {
  const filePath = path.join(POSTS_DIR, mdFile);
  const content  = fs.readFileSync(filePath, 'utf-8');

  // 解析 frontmatter
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) { skipCount++; continue; }
  const fm = fmMatch[1];

  const titleMatch    = fm.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  const slugMatch     = fm.match(/^slug:\s*["']?(.+?)["']?\s*$/m);
  const coverMatch    = fm.match(/^coverImage:\s*["']?(.+?)["']?\s*$/m);
  const categoryMatch = fm.match(/^category:\s*["']?(.+?)["']?\s*$/m);
  const draftMatch    = fm.match(/^draft:\s*(.+?)$/m);

  if (!titleMatch) { skipCount++; continue; }
  if (draftMatch && draftMatch[1].trim() === 'true') { skipCount++; continue; }

  const title    = titleMatch[1].trim();
  const slug     = slugMatch ? slugMatch[1].trim() : path.basename(mdFile, '.md');
  const category = categoryMatch ? categoryMatch[1].trim() : '';
  const cover    = coverMatch ? coverMatch[1].trim() : '';

  const articleUrl = `${SITE_URL}/posts/${slug}`;

  // 處理圖片：複製到 public/og-images/ 以產生穩定網址
  let imgUrl = '';
  if (cover) {
    let srcImg = path.join(PUBLIC_IMAGES_DIR, cover);
    if (!fs.existsSync(srcImg)) {
      srcImg = path.join(ASSETS_IMAGES_DIR, cover);
    }
    if (fs.existsSync(srcImg)) {
      const destImg = path.join(OG_DIR, cover);
      // 永遠覆蓋，確保新圖片能更新 og-images
      fs.copyFileSync(srcImg, destImg);
      imgUrl = `${SITE_URL}/og-images/${encodeURIComponent(cover)}`;
    }
  }

  articlesToSync.push({ title, category, articleUrl, imgUrl });
}

console.log(`\n📋 共找到 ${articlesToSync.length} 篇文章，準備同步至 Google Sheet...\n`);

// 批次 POST 到 GAS（使用 fetch 自動處理 302 重定向）
async function postToGAS(payload) {
  try {
    const res = await fetch(GAS_URL, {
      method: 'POST',
      redirect: 'follow',
      headers: {
        'Content-Type': 'text/plain;charset=utf-8', // GAS 跨域 POST 最佳 Content-Type
      },
      body: JSON.stringify(payload),
    });
    const text = await res.text();
    try {
      return JSON.parse(text);
    } catch {
      return { success: res.ok, raw: text };
    }
  } catch (err) {
    return { success: false, error: err.message };
  }
}

(async () => {
  const BATCH_SIZE = 8; // 每次並行發送 8 筆，速度提升 10 倍
  for (let i = 0; i < articlesToSync.length; i += BATCH_SIZE) {
    const batch = articlesToSync.slice(i, i + BATCH_SIZE);
    await Promise.all(
      batch.map(async (article) => {
        const result = await postToGAS({
          action: 'updateArticleUrl',
          ...article,
        });

        if (result.success) {
          console.log(`✅ [${result.action || '更新'}] "${article.title}" (圖片: ${article.imgUrl ? '有' : '無'})`);
          syncCount++;
        } else {
          console.log(`❌ 同步失敗："${article.title}"`);
          if (result.error) console.log(`   錯誤：${result.error}`);
          skipCount++;
        }
      })
    );
  }

  console.log('\n' + '='.repeat(50));
  console.log(`✅ 成功同步：${syncCount} 篇`);
  console.log(`⏭  略過/失敗：${skipCount} 篇`);
  console.log(`\n🌐 請前往 Google Sheet 確認網址是否已更新！`);
})();
