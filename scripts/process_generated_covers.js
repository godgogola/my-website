import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const artifactDir = 'C:\\Users\\X1 Yoga Gen7\\.gemini\\antigravity-ide\\brain\\d0bbff17-1170-46fc-a3b2-5bf2112488d8';
const driveDir = 'G:\\我的雲端硬碟\\衛教文章圖片';
const publicImagesDir = path.join(process.cwd(), 'public/images');
const postsDir = path.join(process.cwd(), 'src/content/posts');

const items = [
  {
    prefix: 'hba1c_fasting_high_normal',
    title: '【糖化血色素】空腹血糖高但是糖化血色素正常是什麼原因',
    file: '糖化血色素空腹血糖高但是糖化血色素正常是什麼原因.md'
  },
  {
    prefix: 'hba1c_fasting_normal_hba1c_high',
    title: '【糖化血色素】空腹血糖正常但是糖化血色素高是什麼原因',
    file: '糖化血色素空腹血糖正常但是糖化血色素高是什麼原因.md'
  },
  {
    prefix: 'hba1c_non_dietary_factors',
    title: '【糖化血色素】糖化血色素升高的原因_非飲食因素',
    file: '糖化血色素糖化血色素升高的原因_非飲食因素.md'
  },
  {
    prefix: 'proteinuria_mild_care',
    title: '【尿蛋白】輕微尿蛋白怎麼辦',
    file: '尿蛋白輕微尿蛋白怎麼辦.md'
  },
  {
    prefix: 'hematuria_mild_care',
    title: '【尿潛血】輕微尿潛血怎麼辦',
    file: '尿潛血輕微尿潛血怎麼辦.md'
  },
  {
    prefix: 'anemia_microcytic_macrocytic',
    title: '【貧血】小球性與大球性貧血',
    file: '貧血小球性與大球性貧血.md'
  },
  {
    prefix: 'stomach_cancer_risk_factors',
    title: '【胃癌】胃癌的危險因子',
    file: '胃癌胃癌的危險因子.md'
  },
  {
    prefix: 'sarcopenia_kidney_function_misjudgment',
    title: '【腎功能】高齡肌少症與腎功能誤判',
    file: '腎功能高齡肌少症與腎功能誤判.md'
  },
  {
    prefix: 'ckd_stages_kidney_protection',
    title: '【慢性腎臟病】慢性腎臟病各分期保腎措施',
    file: '慢性腎臟病慢性腎臟病各分期保腎措施.md'
  },
  {
    prefix: 'bilirubin_isolated_high',
    title: '【膽紅素】單純膽紅素偏高',
    file: '膽紅素單純膽紅素偏高.md'
  },
  {
    prefix: 'hypertension_complications',
    title: '長期血壓控制不良的併發症',
    file: '長期血壓控制不良的併發症.md'
  },
  {
    prefix: 's_abcde_hypertension_lifestyle',
    title: 'S-ABCDE 高血壓生活型態調整',
    file: 's-abcde-高血壓生活型態調整.md'
  }
];

const artifactFiles = fs.readdirSync(artifactDir);

items.forEach((item, index) => {
  const pngFile = artifactFiles.find(f => f.startsWith(item.prefix) && f.endsWith('.png'));
  if (!pngFile) {
    console.error(`[ERROR] PNG for item ${index + 1} (${item.title}) not found!`);
    return;
  }
  const srcPngPath = path.join(artifactDir, pngFile);
  const drivePngPath = path.join(driveDir, `${item.title}.png`);
  const webpFileName = `${item.title}.webp`;
  const publicWebpPath = path.join(publicImagesDir, webpFileName);

  console.log(`\n=== Processing Item ${index + 1}: ${item.title} ===`);
  
  // 1. 原圖備份 PNG 到 Google 雲端硬碟
  fs.copyFileSync(srcPngPath, drivePngPath);
  console.log(`  ✅ 1. 備份 PNG 至 Drive: ${drivePngPath}`);

  // 2. WebP 轉檔至 public/images/
  // 使用 sharp-cli
  try {
    execSync(`npx sharp-cli -i "${srcPngPath}" -o "${publicWebpPath}"`, { stdio: 'inherit' });
    console.log(`  ✅ 2. WebP 轉檔至 public/images: ${publicWebpPath}`);
  } catch (err) {
    console.error(`  ❌ WebP 轉檔失敗: ${err.message}`);
  }

  // 3. 更新 Markdown coverImage
  const mdPath = path.join(postsDir, item.file);
  if (fs.existsSync(mdPath)) {
    let content = fs.readFileSync(mdPath, 'utf-8');
    if (content.includes('coverImage:')) {
      content = content.replace(/^coverImage:\s*["']?(.+?)["']?\s*$/m, `coverImage: "${webpFileName}"`);
    } else {
      content = content.replace(/(^title:.*$)/m, `$1\ncoverImage: "${webpFileName}"`);
    }
    fs.writeFileSync(mdPath, content, 'utf-8');
    console.log(`  ✅ 3. 更新 Markdown 前言 coverImage: "${webpFileName}"`);
  } else {
    console.error(`  ❌ MD File not found: ${mdPath}`);
  }
});
