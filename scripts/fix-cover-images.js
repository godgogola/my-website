import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '../src/content/posts');
const PUBLIC_IMAGES_DIR = path.join(__dirname, '../public/images');
const OG_DIR = path.join(__dirname, '../public/og-images');
const MAPPING_FILE = path.join(__dirname, 'cover-mapping.json');

if (!fs.existsSync(OG_DIR)) {
  fs.mkdirSync(OG_DIR, { recursive: true });
}

// 1. 讀取現有 mapping
let mapping = [];
if (fs.existsSync(MAPPING_FILE)) {
  mapping = JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8'));
}
const mapByFile = new Map(mapping.map(m => [m.file, m.coverImage]));

// 2. 取得 public/images 所有圖檔清單
const imageFiles = fs.readdirSync(PUBLIC_IMAGES_DIR);
const imageMap = new Map();
for (const img of imageFiles) {
  const ext = path.extname(img).toLowerCase();
  if (['.png', '.jpg', '.jpeg', '.webp'].includes(ext)) {
    const baseName = path.basename(img, ext);
    imageMap.set(baseName, img);
    imageMap.set(baseName.replace(/\s+/g, ''), img);
  }
}

function getFallbackCover(title) {
  if (title.includes('B型肝炎') || title.includes('b型肝炎')) return 'B型肝炎.png';
  if (title.includes('C型肝炎') || title.includes('c型肝炎')) return 'C型肝炎.png';
  if (title.includes('食道裂孔')) return '胃食道逆流.png';
  if (title.includes('痛風')) return '急性痛風的原因.png';
  if (title.includes('墨綠')) return '急性腸胃炎.png';
  if (title.includes('息肉')) return '大腸息肉.png';
  if (title.includes('ACCAHA') || title.includes('血脂') || title.includes('膽固醇')) return '高血脂治療.png';
  if (title.includes('抽血') || title.includes('檢查')) return '血液檢查.png';
  if (title.includes('ARMA') || title.includes('消融')) return '胃食道逆流.png';
  return null;
}

const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
let updatedCount = 0;

for (const file of mdFiles) {
  const filePath = path.join(POSTS_DIR, file);
  const content = fs.readFileSync(filePath, 'utf8');

  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) continue;

  const frontmatter = fmMatch[1];
  const titleMatch = frontmatter.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  if (!titleMatch) continue;

  const title = titleMatch[1].trim();

  let coverImage = '';
  const coverMatch = frontmatter.match(/^coverImage:\s*["']?(.+?)["']?\s*$/m);
  if (coverMatch) {
    coverImage = coverMatch[1].trim();
  }

  if (!coverImage) {
    if (mapByFile.has(file)) {
      coverImage = mapByFile.get(file);
    }
  }

  if (!coverImage) {
    // 試著從 public/images 找同名或去空格同名
    const cleanTitle = title.replace(/[【\[（(].+?[】\]）)]\s*/g, '').trim();
    if (imageMap.has(title)) coverImage = imageMap.get(title);
    else if (imageMap.has(cleanTitle)) coverImage = imageMap.get(cleanTitle);
    else if (imageMap.has(title.replace(/\s+/g, ''))) coverImage = imageMap.get(title.replace(/\s+/g, ''));
  }

  if (!coverImage) {
    coverImage = getFallbackCover(title);
  }

  if (coverImage) {
    // 確保圖片在 public/images/ 或 public/og-images/ 都有副本
    const srcImg = path.join(PUBLIC_IMAGES_DIR, coverImage);
    if (fs.existsSync(srcImg)) {
      const destOg = path.join(OG_DIR, coverImage);
      if (!fs.existsSync(destOg)) {
        fs.copyFileSync(srcImg, destOg);
      }
    }

    let newFrontmatter = frontmatter;
    if (frontmatter.includes('coverImage:')) {
      newFrontmatter = frontmatter.replace(
        /^coverImage:\s*["']?.*?["']?\s*$/m,
        `coverImage: "${coverImage}"`
      );
    } else {
      newFrontmatter = frontmatter.replace(
        /(^title:.*$)/m,
        `$1\ncoverImage: "${coverImage}"`
      );
    }

    if (newFrontmatter !== frontmatter) {
      const newContent = content.replace(fmMatch[0], `---\n${newFrontmatter}\n---`);
      fs.writeFileSync(filePath, newContent, 'utf8');
      console.log(`[Cover Fixed] ${title} -> ${coverImage}`);
      updatedCount++;
    }
  } else {
    console.warn(`[No Cover] ${title} (${file})`);
  }
}

console.log(`\n🎉 完成！共更新 ${updatedCount} 篇文章的封面圖片。`);
