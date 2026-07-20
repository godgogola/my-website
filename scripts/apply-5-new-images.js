import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '../src/content/posts');
const MAPPING_FILE = path.join(__dirname, 'cover-mapping.json');

const targetMap = {
  '食道裂孔疝氣的原因.md': '食道裂孔疝氣的原因.png',
  '痛風常發作的部位.md': '痛風常發作的部位.png',
  '為什麼會有墨綠色大便.md': '為什麼會有墨綠色大便.png',
  '大腸息肉的分類.md': '大腸息肉的分類.png',
  '大腸息肉切除術後出血.md': '大腸息肉切除術後出血.png'
};

for (const [file, img] of Object.entries(targetMap)) {
  const p = path.join(POSTS_DIR, file);
  if (fs.existsSync(p)) {
    let content = fs.readFileSync(p, 'utf8');
    content = content.replace(/^coverImage:\s*["']?.*?["']?\s*$/m, '');
    content = content.replace(/(^title:.*$)/m, `$1\ncoverImage: "${img}"`);
    fs.writeFileSync(p, content, 'utf8');
    console.log(`✅ Fixed post: ${file} -> ${img}`);
  }
}

if (fs.existsSync(MAPPING_FILE)) {
  let list = JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8'));
  list = list.map(item => {
    if (item.file === '食道裂孔疝氣的原因.md') item.coverImage = '食道裂孔疝氣的原因.png';
    if (item.file === '痛風常發作的部位.md') item.coverImage = '痛風常發作的部位.png';
    if (item.file === '為什麼會有墨綠色大便.md') item.coverImage = '為什麼會有墨綠色大便.png';
    if (item.file === '大腸息肉的分類.md') item.coverImage = '大腸息肉的分類.png';
    if (item.file === '大腸息肉切除術後出血.md') item.coverImage = '大腸息肉切除術後出血.png';
    return item;
  });
  fs.writeFileSync(MAPPING_FILE, JSON.stringify(list, null, 2), 'utf8');
  console.log('✅ Updated cover-mapping.json!');
}
