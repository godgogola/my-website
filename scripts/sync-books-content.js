import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');

// 1. 讀取 .env 檔案
const envPath = path.join(projectRoot, '.env');
let booksVaultPath = '';

if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  const match = envContent.match(/^BOOKS_VAULT_PATH\s*=\s*(.+)$/m);
  if (match) {
    booksVaultPath = match[1].trim().replace(/['"]/g, '');
  }
}

if (!booksVaultPath) {
  booksVaultPath = 'G:/我的雲端硬碟/讀書筆記庫/讀書筆記';
}

console.log(`[Sync-Books] 讀書筆記來源路徑: ${booksVaultPath}`);

const destDir = path.join(projectRoot, 'src', 'content', 'books');
const publicImagesDir = path.join(projectRoot, 'public', 'images');
const gdriveImagesDir = 'G:/我的雲端硬碟/衛教文章圖片';

if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });
if (!fs.existsSync(publicImagesDir)) fs.mkdirSync(publicImagesDir, { recursive: true });

function slugify(text) {
  return text.toString().toLowerCase().trim()
    .replace(/[、，,%\s]+/g, '-')
    .replace(/[^\w\u4e00-\u9fff\-]+/g, '')
    .replace(/\-\-+/g, '-')
    .replace(/^-+|-+$/g, '');
}

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

function findCoverImage(chapterTitle, bookTitle) {
  const cleanTitle = chapterTitle.replace(/^\d+[、.\s]+/, '');
  const candidates = [
    `${chapterTitle}.webp`,
    `${chapterTitle}.png`,
    `${cleanTitle}.webp`,
    `${cleanTitle}.png`,
    `${bookTitle}-${chapterTitle}.webp`,
    `${bookTitle}-${chapterTitle}.png`
  ];

  for (const name of candidates) {
    if (fs.existsSync(path.join(publicImagesDir, name))) {
      return name.replace(/\.png$/, '.webp');
    }
    if (fs.existsSync(path.join(gdriveImagesDir, name))) {
      return name.replace(/\.png$/, '.webp');
    }
  }
  return '';
}

function findImageInDir(dir, imageName) {
  if (!fs.existsSync(dir)) return null;
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && entry.name !== '.obsidian' && entry.name !== '.git') {
      const found = findImageInDir(fullPath, imageName);
      if (found) return found;
    } else if (entry.isFile() && entry.name.toLowerCase() === imageName.toLowerCase()) {
      return fullPath;
    }
  }
  return null;
}

export function syncBooks() {
  if (!fs.existsSync(booksVaultPath)) {
    console.warn(`[Sync-Books] ⚠️ 找不到讀書筆記資料夾: "${booksVaultPath}"。`);
    return;
  }

  const entries = fs.readdirSync(booksVaultPath, { withFileTypes: true });
  const bookFolders = entries.filter(e => e.isDirectory() && !e.name.startsWith('.'));

  if (bookFolders.length === 0) {
    console.log('[Sync-Books] ℹ️ 未找到任何書籍資料夾。');
    return;
  }

  let totalSynced = 0;
  const validFiles = new Set();

  for (const folder of bookFolders) {
    const bookTitle = folder.name;
    const bookDir = path.join(booksVaultPath, bookTitle);
    const bookDestDir = path.join(destDir, bookTitle);
    if (!fs.existsSync(bookDestDir)) fs.mkdirSync(bookDestDir, { recursive: true });

    const mdFiles = fs.readdirSync(bookDir).filter(f => f.endsWith('.md') && !f.startsWith('.'));
    console.log(`[Sync-Books] 📖 書名: 《${bookTitle}》 (共 ${mdFiles.length} 篇章節)`);

    // 預先統計該書已有章節序號的最大值 (< 900)
    let maxBookOrder = 0;
    for (const f of mdFiles) {
      const parsed = parseChapterOrder(path.basename(f, '.md'));
      if (parsed < 900 && parsed > maxBookOrder) maxBookOrder = parsed;
    }
    if (fs.existsSync(bookDestDir)) {
      for (const f of fs.readdirSync(bookDestDir).filter(f => f.endsWith('.md'))) {
        try {
          const c = fs.readFileSync(path.join(bookDestDir, f), 'utf8');
          const m = c.match(/^order:\s*(\d+)/m);
          if (m) {
            const ord = parseInt(m[1], 10);
            if (ord < 900 && ord > maxBookOrder) maxBookOrder = ord;
          }
        } catch (e) {}
      }
    }

    for (const file of mdFiles) {
      const filePath = path.join(bookDir, file);
      const chapterTitle = path.basename(file, '.md');
      let order = parseChapterOrder(chapterTitle);
      const slug = slugify(chapterTitle);
      const outputFileName = `${slug}.md`;
      const outputPath = path.join(bookDestDir, outputFileName);
      validFiles.add(path.join(bookTitle, outputFileName).replace(/\\/g, '/'));

      // 若未包含數字（或為 999 暫存值），先檢查已產生檔案是否已有排序，若無則從最後序號遞增
      if (order >= 900) {
        if (fs.existsSync(outputPath)) {
          try {
            const existC = fs.readFileSync(outputPath, 'utf8');
            const existM = existC.match(/^order:\s*(\d+)/m);
            if (existM) {
              const curO = parseInt(existM[1], 10);
              if (curO < 900) order = curO;
            }
          } catch (e) {}
        }
        if (order >= 900) {
          order = ++maxBookOrder;
          console.log(`[Sync-Books] 🔢 為章節自動接續序號: "${chapterTitle}" [${bookTitle}] → order: ${order}`);
        }
      }

      try {
        let content = fs.readFileSync(filePath, 'utf8');

        // 讀取 Frontmatter（若有）
        const hasFrontmatter = content.startsWith('---');
        let frontmatter = '';
        let body = content;

        if (hasFrontmatter) {
          const parts = content.split('---');
          if (parts.length >= 3) {
            frontmatter = parts[1];
            body = parts.slice(2).join('---');
          }
        }

        // 發布日期
        let publishDate = new Date().toISOString().split('T')[0];
        try {
          const stat = fs.statSync(filePath);
          const fDate = (stat.birthtime && stat.birthtime.getTime() > 0) ? stat.birthtime : stat.mtime;
          publishDate = fDate.toISOString().split('T')[0];
        } catch (e) {}

        let title = chapterTitle;
        let coverImage = findCoverImage(chapterTitle, bookTitle);
        let draft = false;

        if (frontmatter) {
          const titleMatch = frontmatter.match(/^title:\s*(.+)$/m);
          const dateMatch = frontmatter.match(/^publishDate:\s*(.+)$/m);
          const draftMatch = frontmatter.match(/^draft:\s*(.+)$/m);
          const coverMatch = frontmatter.match(/^coverImage:\s*["']?(.+?)["']?\s*$/m);

          if (titleMatch) title = titleMatch[1].replace(/['"]/g, '').trim();
          if (dateMatch) publishDate = dateMatch[1].replace(/['"]/g, '').trim();
          if (draftMatch) draft = draftMatch[1].trim() === 'true';
          if (coverMatch) coverImage = coverMatch[1].trim();
        }

        // 處理圖片嵌入 ![[...]]
        let processedBody = body.replace(/!\[\[([^\]]+)\]\]/g, (match, imageName) => {
          imageName = imageName.trim();
          const originImgPath = findImageInDir(booksVaultPath, imageName);
          if (originImgPath && fs.existsSync(originImgPath)) {
            const ext = path.extname(imageName);
            const nameWithoutExt = path.basename(imageName, ext);
            const destImgName = `${slugify(nameWithoutExt)}${ext}`;
            const destImgPath = path.join(publicImagesDir, destImgName);
            try {
              fs.copyFileSync(originImgPath, destImgPath);
            } catch (e) {}
            return `![${nameWithoutExt}](/images/${destImgName})`;
          }
          return `[圖片: ${imageName}]`;
        });

        const bookSlug = slugify(bookTitle);

        // 處理雙向筆記內部連結 [[...]]
        processedBody = processedBody.replace(/(?<!\!)\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (match, noteTarget, display) => {
          const targetSlug = slugify(noteTarget.trim());
          const displayText = display ? display.trim() : noteTarget.trim();
          return `[${displayText}](/books/${bookSlug}/${targetSlug})`;
        });

        const coverLine = coverImage ? `\ncoverImage: "${coverImage}"` : '';
        const finalFrontmatter = `---\ntitle: "${title}"\nbook: "${bookTitle}"\nbookSlug: "${bookSlug}"\ncategory: "${bookTitle}"\npublishDate: "${publishDate}"\ndraft: ${draft}\nslug: "${slug}"\norder: ${order}${coverLine}\n---\n`;

        fs.writeFileSync(outputPath, finalFrontmatter + processedBody, 'utf8');
        totalSynced++;
      } catch (err) {
        console.warn(`[Sync-Books] ⚠️ 處理筆記出錯: ${file} — ${err.message}`);
      }
    }
  }

  // 清除已刪除的舊章節
  const scanDestFiles = (dir, base = '') => {
    let results = [];
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const e of entries) {
      const rel = path.join(base, e.name).replace(/\\/g, '/');
      const full = path.join(dir, e.name);
      if (e.isDirectory()) {
        results = results.concat(scanDestFiles(full, rel));
      } else if (e.isFile() && e.name.endsWith('.md')) {
        results.push({ rel, full });
      }
    }
    return results;
  };

  const currentDest = scanDestFiles(destDir);
  let deletedCount = 0;
  for (const item of currentDest) {
    if (!validFiles.has(item.rel)) {
      try {
        fs.unlinkSync(item.full);
        console.log(`[Sync-Books] 🗑️ 刪除已被移除的筆記: ${item.rel}`);
        deletedCount++;
      } catch (e) {}
    }
  }

  console.log(`[Sync-Books] 🎉 讀書筆記同步完成！共導入 ${totalSynced} 篇章節至 src/content/books/ (刪除 ${deletedCount} 篇舊檔案)`);
}

// 直接執行時執行 syncBooks
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  syncBooks();
}
