/**
 * assign-by-topic.js
 * 對沒有圖片的文章，根據標題關鍵字指派相關主題的現有圖片
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const IMAGES_DIR = path.join(__dirname, '../public/images');
const POSTS_DIR = path.join(__dirname, '../src/content/posts');

// 取得所有現有圖片
const imageFiles = new Set(fs.readdirSync(IMAGES_DIR));

// 關鍵字 → 圖片的對應規則（由長到短，越具體的放越前面）
const KEYWORD_RULES = [
  // B型肝炎系列
  { keywords: ['b型肝炎', 'bepirovirsen', 'b肝', 'tdf', 'hbv', 'e抗原', 's抗原'], image: 'B型肝炎.png' },
  // C型肝炎系列
  { keywords: ['c型肝炎', 'c肝', 'daa', 'sofosbuvir', 'hcv', '全口服抗病毒', 'pi類'], image: 'C型肝炎.png' },
  // A型肝炎
  { keywords: ['a型肝炎', 'a肝'], image: 'A型肝炎.png' },
  // P-CABs
  { keywords: ['p-cabs', 'pcabs', '鉀離子競爭'], image: '【PPI】為什麼要空腹吃.png' },
  // FODMAP
  { keywords: ['fodmap', '腸躁症', '結腸激躁'], image: '結腸激躁症.png' },
  // 減重系列
  { keywords: ['減重', '有氧', '重訓', '瘦瘦', 'saxenda', 'wegovy', 'mounjaro', 'rybelsus', 'contrave', 'bmi', 'inbody', '肌肉量', '復胖', '停藥', '合法減重', 'ada合法'], image: '打瘦瘦針也要健康.png' },
  // 清腸系列
  { keywords: ['清腸', '保可淨', '耐福利散', '耐福利散', '低渣飲食', '清腸劑'], image: '大腸鏡前清腸準備(保可淨).png' },
  // 大腸鏡
  { keywords: ['大腸鏡', '腸鏡', '腸胃鏡', '無痛腸胃鏡', '息肉切除', '難治性幽門'], image: '無痛腸胃鏡.png' },
  // 食道系列
  { keywords: ['巴瑞氏', '食道炎', '食道潰瘍', '食道裂孔', 'barrett', '地雷飲食'], image: '胃食道逆流.png' },
  // 打嗝
  { keywords: ['打嗝', '一直打嗝'], image: '打嗝.png' },
  // 痛風系列
  { keywords: ['痛風', '尿酸'], image: '急性痛風的原因.png' },
  // 幽門桿菌系列
  { keywords: ['幽門桿菌', '幽門螺旋桿菌', '胃癌', '殺菌', '難治性幽門'], image: '幽門桿菌檢測.png' },
  // 胃相關
  { keywords: ['胃肉毒', '胃內縫合', '上消化道潰瘍'], image: '功能性消化不良.png' },
  // 檢查系列
  { keywords: ['血液檢查', '需要空腹', '肝膽功能', '心血管及腎', '內分泌'], image: '一般檢查.png' },
  // 腸胃藥
  { keywords: ['止瀉', '軟便', '腸胃藥', '懷孕', '泌乳', '孕期', '哺乳', '小兒', '促動力'], image: '腸胃促動力藥物.png' },
  // 飲食系列
  { keywords: ['三酸甘油脂', 'ldl', '膽固醇', '哪些食物', '飲食'], image: '高三酸甘油脂治療.png' },
  // 糖尿病系列
  { keywords: ['糖尿病', '胰島素', '降血糖', '控糖', '血糖', 'homa', 'ai骨密', '骨質疏鬆'], image: '胰島素的控糖新觀念.png' },
  // 肝炎總覽
  { keywords: ['肝炎'], image: '肝炎.png' },
  // 豐田診所、設備
  { keywords: ['豐田', 'eluxeo', '6000', '內視鏡系統', '診所', '困難息肉'], image: '無痛腸胃鏡.png' },
  // 台灣B肝措施
  { keywords: ['台灣', 'b肝公衛', '公衛措施', '合法減重藥物', '台灣合法'], image: 'B型肝炎.png' },
  // 平穩血糖
  { keywords: ['平穩血糖', '血糖上升', '飲食與生活'], image: '胰島素及HOMA 指數.png' },
  // 痔瘡全攻略
  { keywords: ['痔瘡全攻略', '全攻略'], image: '痔瘡.png' },
  // 為什麼系列
  { keywords: ['墨綠色大便', '為什麼'], image: '急性腸胃炎.png' },
];

function normalize(str) {
  return str.toLowerCase().replace(/[\s【】\[\]（）()\-_「」]/g, '');
}

// 處理每篇 Markdown
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
let matched = 0, skipped = 0;

for (const mdFile of mdFiles) {
  const filePath = path.join(POSTS_DIR, mdFile);
  const content = fs.readFileSync(filePath, 'utf-8');

  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) continue;
  const frontmatter = fmMatch[1];
  if (frontmatter.includes('coverImage:')) continue;

  const titleMatch = frontmatter.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  if (!titleMatch) continue;
  const title = titleMatch[1].trim();
  const titleNorm = normalize(title);

  let foundImage = null;

  for (const rule of KEYWORD_RULES) {
    const ruleMatches = rule.keywords.some(kw => titleNorm.includes(normalize(kw)));
    if (ruleMatches && imageFiles.has(rule.image)) {
      foundImage = rule.image;
      break;
    }
  }

  if (foundImage) {
    const newFrontmatter = frontmatter.replace(
      /(^title:.*$)/m,
      `$1\ncoverImage: "${foundImage}"`
    );
    const newContent = content.replace(fmMatch[0], `---\n${newFrontmatter}\n---`);
    fs.writeFileSync(filePath, newContent, 'utf-8');
    console.log(`✅ "${title}"`);
    console.log(`   → ${foundImage}\n`);
    matched++;
  } else {
    console.log(`⚠️  "${title}" — 無法自動指派`);
    skipped++;
  }
}

console.log(`\n${'='.repeat(50)}`);
console.log(`✅ 成功指派: ${matched} 篇`);
console.log(`⚠️  無法指派: ${skipped} 篇（顯示漸層佔位圖）`);
