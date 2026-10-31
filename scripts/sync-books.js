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
const CONTENT_BOOKS_DIR = path.join(__dirname, '../src/content/books');

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

// 檢查章節專屬封面圖是否存在（嚴格比對章節標題，不抓整本書共用圖，確保新文章在 Sheet 保持 E/F 欄空白）
function findCoverImage(chapterTitle, bookTitle) {
  const cleanTitle = chapterTitle.replace(/^\d+[、.\s]+/, '');
  const noPunctTitle = chapterTitle.replace(/[：:？?！「」『』]/g, '');
  const cleanNoPunct = cleanTitle.replace(/[：:？?！「」『』]/g, '');
  const candidates = [
    `${chapterTitle}.webp`,
    `${chapterTitle}.png`,
    `${noPunctTitle}.webp`,
    `${noPunctTitle}.png`,
    `${cleanTitle}.webp`,
    `${cleanTitle}.png`,
    `${cleanNoPunct}.webp`,
    `${cleanNoPunct}.png`,
    `${bookTitle}-${chapterTitle}.webp`,
    `${bookTitle}-${chapterTitle}.png`,
    `${bookTitle}-${noPunctTitle}.webp`,
    `${bookTitle}-${noPunctTitle}.png`
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

async function postToGAS(payload, retries = 2) {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const res = await fetch(GAS_URL, {
        method: 'POST',
        redirect: 'follow',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(12000)
      });
      const text = await res.text();
      try {
        return JSON.parse(text);
      } catch {
        return { success: res.ok, raw: text };
      }
    } catch (err) {
      if (attempt < retries) {
        await new Promise(r => setTimeout(r, 1000));
        continue;
      }
      return { success: false, error: err.message };
    }
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
  let updatedCount = 0;
  let waitingImageCount = 0;

  for (const folder of bookFolders) {
    const bookTitle = folder.name;
    const bookDir = path.join(BOOKS_VAULT_PATH, bookTitle);
    const mdFiles = fs.readdirSync(bookDir).filter(f => f.endsWith('.md') && !f.startsWith('.'));

    console.log(`📖 書名: 《${bookTitle}》 (共 ${mdFiles.length} 個章節檔案)`);

    // 預先統計該書已有章節序號的最大值 (< 900)
    const bookContentDir = path.join(CONTENT_BOOKS_DIR, bookTitle);
    let maxSort = 0;
    for (const file of mdFiles) {
      const s = parseChapterOrder(path.basename(file, '.md'));
      if (s < 900 && s > maxSort) maxSort = s;
    }
    if (fs.existsSync(bookContentDir)) {
      for (const f of fs.readdirSync(bookContentDir).filter(f => f.endsWith('.md'))) {
        try {
          const c = fs.readFileSync(path.join(bookContentDir, f), 'utf8');
          const m = c.match(/^order:\s*(\d+)/m);
          if (m) {
            const ord = parseInt(m[1], 10);
            if (ord < 900 && ord > maxSort) maxSort = ord;
          }
        } catch (e) {}
      }
    }

    // 依章節序號排序（未編號篇章自動從最後序號接續往下遞增）
    const chapters = mdFiles.map(file => {
      const chapterTitle = path.basename(file, '.md');
      let sort = parseChapterOrder(chapterTitle);
      if (sort >= 900) {
        if (fs.existsSync(bookContentDir)) {
          const slugBase = chapterTitle.replace(/[、\s]+/g, '-');
          const matchedFile = fs.readdirSync(bookContentDir).find(f => f.includes(slugBase));
          if (matchedFile) {
            try {
              const c = fs.readFileSync(path.join(bookContentDir, matchedFile), 'utf8');
              const m = c.match(/^order:\s*(\d+)/m);
              if (m && parseInt(m[1], 10) < 900) sort = parseInt(m[1], 10);
            } catch (e) {}
          }
        }
        if (sort >= 900) {
          sort = ++maxSort;
          console.log(`  🔢 為章節自動接續序號: "${chapterTitle}" [${bookTitle}] → sort: ${sort}`);
        }
      }
      const imgUrl = findCoverImage(chapterTitle, bookTitle);
      const slug = chapterTitle.replace(/[、\s]+/g, '-');
      const articleUrl = `${SITE_URL}/books/${encodeURIComponent(bookTitle)}/${encodeURIComponent(slug)}`;
      return { bookTitle, chapterTitle, sort, imgUrl, articleUrl };
    }).sort((a, b) => a.sort - b.sort);

    for (const chapter of chapters) {
      totalItems++;
      const hasImage = !!chapter.imgUrl;

      // 新文章寫入 Sheet：若尚未生成圖片，E 欄 (圖片網址) 與 F 欄 (文章網址) 留空，僅有 ABCDG 欄
      const appendPayload = {
        action: 'appendRow',
        sheet: '讀書筆記',
        bookTitle: chapter.bookTitle,
        sort: chapter.sort,
        title: chapter.chapterTitle,
        type: '圖片卡片',
        imgUrl: hasImage ? chapter.imgUrl : '',
        articleUrl: hasImage ? chapter.articleUrl : '',
        visible: true
      };

      const res = await postToGAS(appendPayload);
      if (res.action === '新增成功') {
        if (hasImage) {
          console.log(`  ✅ [新增成功] ${chapter.chapterTitle} (排序: ${chapter.sort}) - 已帶圖片與網址`);
        } else {
          console.log(`  📝 [新增成功] ${chapter.chapterTitle} (排序: ${chapter.sort}) - 僅前置 ABCDG 欄（待生圖）`);
          waitingImageCount++;
        }
        addedCount++;
      } else {
        // 已存在於 Sheet：同步更新排序、圖片與網址
        const updatePayload = {
          action: 'updateArticleUrl',
          sheet: '讀書筆記',
          title: chapter.chapterTitle,
          sort: chapter.sort,
          imgUrl: chapter.imgUrl,
          articleUrl: chapter.articleUrl
        };
        const updateRes = await postToGAS(updatePayload);
        if (updateRes.success) {
          if (hasImage) {
            console.log(`  🔗 [一鍵同步完成] ${chapter.chapterTitle} (排序: ${chapter.sort}, 已填入 E/F 欄圖片與網址)`);
            updatedCount++;
          } else {
            console.log(`  ⏳ [已更新排序] ${chapter.chapterTitle} (排序: ${chapter.sort}, 待生圖)`);
          }
        }
      }

      await new Promise(r => setTimeout(r, 200));
    }
    console.log('');
  }

  console.log('='.repeat(50));
  console.log(`🎉 讀書筆記同步處理完成！`);
  console.log(`📊 總檢查項目: ${totalItems} | 新增: ${addedCount} | 更新網址: ${updatedCount} | 待生圖(E/F空白): ${waitingImageCount}`);
  console.log(`🌐 請前往 Google Sheet【讀書筆記】分頁確認！`);
}

main().catch(console.error);
