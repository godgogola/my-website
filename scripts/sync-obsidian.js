import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 1. 手動讀取 .env 檔案
const projectRoot = path.resolve(__dirname, '..');
const envPath = path.join(projectRoot, '.env');
let obsidianVaultPath = '';

if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  const match = envContent.match(/^OBSIDIAN_VAULT_PATH\s*=\s*(.+)$/m);
  if (match) {
    obsidianVaultPath = match[1].trim().replace(/['"]/g, '');
  }
}

if (!obsidianVaultPath) {
  obsidianVaultPath = path.join(projectRoot, 'obsidian_vault');
}

console.log(`[Sync] Obsidian 來源路徑: ${obsidianVaultPath}`);

const destDir = path.join(projectRoot, 'src', 'content', 'posts');
const publicImagesDir = path.join(projectRoot, 'public', 'images');

if (!fs.existsSync(destDir)) fs.mkdirSync(destDir, { recursive: true });
if (!fs.existsSync(publicImagesDir)) fs.mkdirSync(publicImagesDir, { recursive: true });

function slugify(text) {
  return text.toString().toLowerCase().trim()
    .replace(/\s+/g, '-')
    .replace(/[^\w\u4e00-\u9fff\-]+/g, '')
    .replace(/\-\-+/g, '-');
}

// 頂層根目錄名稱（不應被視為分類的資料夾）
const ROOT_LEVEL_FOLDERS = new Set(['Wix衛教文章', 'Wix衛教文章庫']);

// 遞迴尋找 Markdown 檔案，並記錄每個檔案的資料夾分類
function getFilesRecursively(dir, fileList = [], vaultRoot = '') {
  if (!fs.existsSync(dir)) return fileList;
  if (!vaultRoot) vaultRoot = dir;
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      if (file !== '.obsidian' && file !== '.git' && file !== 'node_modules') {
        getFilesRecursively(filePath, fileList, vaultRoot);
      }
    } else if (file.endsWith('.md')) {
      const parentDir = path.dirname(filePath);
      const parentName = path.basename(parentDir);
      let category;
      // 如果父資料夾是根目錄或庫根目錄（非實際分類資料夾），則用檔名推斷分類
      // 根目錄或根層資料夾的檔案一律跳過，只處理有分類資料夾的文章
      if (parentDir === vaultRoot || ROOT_LEVEL_FOLDERS.has(parentName)) {
        console.log(`[Sync] 跳過根目錄文章（未分類）: ${file}`);
        continue;
      }
      category = parentName;
      fileList.push({ filePath, category });
    }
  }
  return fileList;
}

function inferCategoryFromFilename(filename) {
  const name = filename.replace('.md', '');
  // 肝炎相關
  if (name.includes('B型肝炎') || name.includes('C型肝炎') || name.includes('A型肝炎') || name.includes('肝炎') || name.includes('肝硬化') || name.includes('肝癌')) {
    return '肝病特區';
  }
  // 健檢相關
  if (name.includes('空腹抽血') || name.includes('血液檢查') || name.includes('尿液') || name.includes('健檢') || name.includes('INBODY') || name.includes('惰性')) {
    return '健檢報告判讀';
  }
  // 預設
  return '肝病特區'; // 根目錄大多是肝病相關特殊文章
}

function findImageInVault(vaultPath, imageName) {
  const allFiles = fs.readdirSync(vaultPath);
  for (const file of allFiles) {
    const filePath = path.join(vaultPath, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      if (file !== '.obsidian' && file !== '.git') {
        const found = findImageInVault(filePath, imageName);
        if (found) return found;
      }
    } else if (file.toLowerCase() === imageName.toLowerCase()) {
      return filePath;
    }
  }
  return null;
}

function sync() {
  if (!fs.existsSync(obsidianVaultPath)) {
    console.warn(`[Sync] [警告] 找不到 Obsidian 資料夾: "${obsidianVaultPath}"。`);
    const demoFile = path.join(destDir, 'demo-post.md');
    if (!fs.existsSync(demoFile)) {
      const demoContent = `---\ntitle: "測試衛教文章（請設定 Obsidian 路徑）"\ncategory: "第一孕期"\ndraft: false\npublishDate: "${new Date().toISOString().split('T')[0]}"\nimage: ""\n---\n# 歡迎！\n`;
      fs.writeFileSync(demoFile, demoContent, 'utf8');
    }
    return;
  }

  const mdFiles = getFilesRecursively(obsidianVaultPath, [], obsidianVaultPath);
  console.log(`[Sync] 找到 ${mdFiles.length} 篇 Obsidian 文章。`);

  let syncedCount = 0;

  for (const { filePath, category: folderCategory } of mdFiles) {
    const fileName = path.basename(filePath, '.md');
    let content = fs.readFileSync(filePath, 'utf8');

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

    let title = fileName;
    let category = folderCategory; // 預設使用資料夾名稱
    let publishDate = new Date().toISOString().split('T')[0];
    let draft = false;

    if (frontmatter) {
      const titleMatch = frontmatter.match(/^title:\s*(.+)$/m);
      const catMatch = frontmatter.match(/^category:\s*(.+)$/m);
      const dateMatch = frontmatter.match(/^publishDate:\s*(.+)$/m);
      const draftMatch = frontmatter.match(/^draft:\s*(.+)$/m);

      if (titleMatch) title = titleMatch[1].replace(/['"]/g, '').trim();
      if (catMatch) {
        const fmCategory = catMatch[1].replace(/['"]/g, '').trim();
        // 只有 frontmatter 中有非預設分類才覆蓋
        if (fmCategory && fmCategory !== '衛教文章') {
          category = fmCategory;
        }
      }
      if (dateMatch) publishDate = dateMatch[1].replace(/['"]/g, '').trim();
      if (draftMatch) draft = draftMatch[1].trim() === 'true';
    }

    // 保留已存在目標檔案的 coverImage
    const outputFileName = `${slugify(fileName)}.md`;
    const outputPath = path.join(destDir, outputFileName);
    let coverImage = '';
    if (fs.existsSync(outputPath)) {
      const existingContent = fs.readFileSync(outputPath, 'utf8');
      const coverMatch = existingContent.match(/^coverImage:\s*["']?(.+?)["']?\s*$/m);
      if (coverMatch) coverImage = coverMatch[1].trim();
    }

    const coverLine = coverImage ? `\ncoverImage: "${coverImage}"` : '';
    const finalFrontmatter = `---\ntitle: "${title}"\ncategory: "${category}"\npublishDate: "${publishDate}"\ndraft: ${draft}\nslug: "${slugify(fileName)}"${coverLine}\n---\n`;

    let processedBody = body.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (match, noteTarget, display) => {
      const targetSlug = slugify(noteTarget.trim());
      const displayText = display ? display.trim() : noteTarget.trim();
      return `[${displayText}](/posts/${targetSlug})`;
    });

    processedBody = processedBody.replace(/!\[\[([^\]]+)\]\]/g, (match, imageName) => {
      imageName = imageName.trim();
      const originImgPath = findImageInVault(obsidianVaultPath, imageName);
      if (originImgPath && fs.existsSync(originImgPath)) {
        const ext = path.extname(imageName);
        const nameWithoutExt = path.basename(imageName, ext);
        const destImgName = `${slugify(nameWithoutExt)}${ext}`;
        const destImgPath = path.join(publicImagesDir, destImgName);
        fs.copyFileSync(originImgPath, destImgPath);
        return `![${nameWithoutExt}](/images/${destImgName})`;
      } else {
        return `[圖片: ${imageName}]`;
      }
    });

    fs.writeFileSync(outputPath, finalFrontmatter + processedBody, 'utf8');
    syncedCount++;
  }

  console.log(`[Sync] 同步完成！共導入 ${syncedCount} 篇文章至 src/content/posts/`);

  const categoryStats = {};
  for (const { category } of mdFiles) {
    categoryStats[category] = (categoryStats[category] || 0) + 1;
  }
  console.log('[Sync] 分類統計：');
  for (const [cat, count] of Object.entries(categoryStats).sort()) {
    console.log(`  - ${cat}: ${count} 篇`);
  }
}

sync();
