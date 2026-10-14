/**
 * sync-books.js
 * 
 * 自動掃描「讀書筆記庫」資料夾，將所有書籍與章節筆記同步新增至 Google Sheet 的【讀書筆記】分頁。
 * 
 * 使用方式：node scripts/sync-books.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 讀取 .env
function loadEnv() {
  const envPath = path.join(__dirname, '../.env');
  if (fs.existsSync(envPath)) {
    const lines = fs.readFileSync(envPath, 'utf-8').split('\n');
    for (const line of lines) {
      const match = line.match(/^\s*([\w_]+)\s*=\s*(.*)?\s*$/);
      if (match && !process.env[match[1]]) {
        process.env[match[1]] = (match[2] || '').trim();
      }
    }
  }
}
loadEnv();

const BOOKS_VAULT_PATH = process.env.BOOKS_VAULT_PATH || 'G:/我的雲端硬碟/讀書筆記庫/讀書筆記';
const GAS_URL = 'https://script.google.com/macros/s/AKfycbwrDmeXp0g6DaKrbY6xbRknwFmZlwHrMnJNJFpPm9bKJ_HbESQNMrLDJYL6M2N0v0f3Sg/exec';
const SITE_URL = 'https://drhuanggi.vercel.app';
const PUBLIC_IMAGES_DIR = path.join(__dirname, '../public/images');
const GDRIVE_IMAGES_DIR = 'G:/我的雲端硬碟/衛教文章圖片';

// 中文數字轉阿拉伯數字排序
const CN_NUMS = {
  '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
  '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
  '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
  '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
  '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25,
  '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29, '三十': 30
};

function parseChapterOrder(filename) {
  // 比對「第X章」、「第X節」、「X、」
  const cnMatch = filename.match(/^[第]?([一二三四五六七八九十]+)[章節、. ]/);
  if (cnMatch && CN_NUMS[cnMatch[1]]) {
    return CN_NUMS[cnMatch[1]];
  }
  const numMatch = filename.match(/^[第]?(\d+)[章節、. ]?/);
  if (numMatch) {
    return parseInt(numMatch[1], 10);
  }
  return 999;
}

// 檢查封面圖是否存在
function findCoverImage(chapterTitle, bookTitle) {
  const candidates = [
    `${chapterTitle}.webp`,
    `${bookTitle}-${chapterTitle}.webp`,
    `${chapterTitle}.png`,
    `${bookTitle}.webp`
  ];

  for (const name of candidates) {
    if (fs.existsSync(path.join(PUBLIC_IMAGES_DIR, name))) {
      return `${SITE_URL}/og-images/${encodeURIComponent(name.replace(/\.png$/, '.webp'))}`;
    }
    if (fs.existsSync(path.join(GDRIVE_IMAGES_DIR, name))) {
      return `${SITE_URL}/og-images/${encodeURIComponent(name.replace(/\.png$/, '.webp'))}`;
    }
  }
  return '';
}

async function postToGAS(payload) {
  try {
    const res = await fetch(GAS_URL, {
      method: 'POST',
      redirect: 'follow',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(payload)
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

async function main() {
  console.log('📚 開始同步【讀書筆記】到 Google Sheet...');
  console.log(`📁 讀書筆記路徑: ${BOOKS_VAULT_PATH}\n`);

  if (!fs.existsSync(BOOKS_VAULT_PATH)) {
    console.error(`❌ 找不到資料夾: ${BOOKS_VAULT_PATH}`);
    process.exit(1);
  }

  const entries = fs.readdirSync(BOOKS_VAULT_PATH, { withFileTypes: true });
  const bookFolders = entries.filter(e => e.isDirectory() && !e.name.startsWith('.'));

  if (bookFolders.length === 0) {
    console.log('ℹ️ 未找到任何書籍資料夾。');
    return;
  }

  let totalItems = 0;
  let addedCount = 0;
  let skippedCount = 0;

  for (const folder of bookFolders) {
    const bookTitle = folder.name;
    const bookDir = path.join(BOOKS_VAULT_PATH, bookTitle);
    const mdFiles = fs.readdirSync(bookDir).filter(f => f.endsWith('.md') && !f.startsWith('.'));

    console.log(`📖 書名: 《${bookTitle}》 (共 ${mdFiles.length} 個章節檔案)`);

    // 依章節序號排序
    const chapters = mdFiles.map(file => {
      const chapterTitle = path.basename(file, '.md');
      const sort = parseChapterOrder(chapterTitle);
      const imgUrl = findCoverImage(chapterTitle, bookTitle);
      const slug = chapterTitle.replace(/[、\s]+/g, '-');
      const articleUrl = `${SITE_URL}/books/${encodeURIComponent(bookTitle)}/${encodeURIComponent(slug)}`;
      return { bookTitle, chapterTitle, sort, imgUrl, articleUrl };
    }).sort((a, b) => a.sort - b.sort);

    for (const chapter of chapters) {
      totalItems++;
      const appendPayload = {
        action: 'appendRow',
        sheet: '讀書筆記',
        bookTitle: chapter.bookTitle,
        sort: chapter.sort,
        title: chapter.chapterTitle,
        type: '圖片卡片',
        imgUrl: chapter.imgUrl,
        articleUrl: chapter.articleUrl,
        visible: true
      };

      const res = await postToGAS(appendPayload);
      if (res.action === '新增成功') {
        console.log(`  ✅ [新增成功] ${chapter.chapterTitle} (排序: ${chapter.sort})`);
        addedCount++;
      } else {
        console.log(`  ⭕ [已存在，進行網址與圖片更新] ${chapter.chapterTitle}`);
        skippedCount++;
      }

      // 永遠調用 updateArticleUrl 確保圖片與文章網址更新至最新版
      const updatePayload = {
        action: 'updateArticleUrl',
        sheet: '讀書筆記',
        title: chapter.chapterTitle,
        imgUrl: chapter.imgUrl,
        articleUrl: chapter.articleUrl
      };
      const updateRes = await postToGAS(updatePayload);
      if (updateRes.success) {
        console.log(`    🔗 [網址與圖片已更新] ${chapter.chapterTitle} (圖片: ${chapter.imgUrl ? '有' : '無'})`);
      }

      // 相容舊的中文數字格式標題（如「一、...」）
      const cnTitleMap = {
        '01、漫步華爾街理論': '一、漫步華爾街理論',
        '02、瘋狂的群眾': '二、瘋狂的群眾',
        '03、投機泡沫史': '三、投機泡沫史',
        '04、世紀資產泡沫': '四、世紀資產泡沫'
      };
      if (cnTitleMap[chapter.chapterTitle]) {
        await postToGAS({
          action: 'updateArticleUrl',
          sheet: '讀書筆記',
          title: cnTitleMap[chapter.chapterTitle],
          imgUrl: chapter.imgUrl,
          articleUrl: chapter.articleUrl
        });
      }

      await new Promise(r => setTimeout(r, 300));
    }
    console.log('');
  }

  console.log('='.repeat(50));
  console.log(`🎉 讀書筆記同步完成！`);
  console.log(`📊 總檢查項目: ${totalItems} | 新增: ${addedCount} | 已存在: ${skippedCount}`);
  console.log(`🌐 請重新整理 Google Sheet【讀書筆記】分頁確認！`);
}

main().catch(console.error);
