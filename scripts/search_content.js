import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '../src/content/posts');

const targets = [
  "空腹血糖高但是糖化血色素正常是什麼原因",
  "空腹血糖正常但是糖化血色素高是什麼原因",
  "糖化血色素升高的原因_非飲食因素",
  "輕微尿蛋白怎麼辦",
  "輕微尿潛血怎麼辦",
  "小球性與大球性貧血",
  "胃癌的危險因子",
  "高齡肌少症與腎功能誤判",
  "慢性腎臟病各分期保腎措施",
  "單純膽紅素偏高",
  "長期血壓控制不良的併發症",
  "S-ABCDE 高血壓生活型態調整",
  "肝功能上升",
  "白蛋白的合成與低下原因",
  "球蛋白",
  "AG ratio",
  "血清胱蛋白 C",
  "HDL太高是好事嗎",
  "胃輕癱飲食調整與治療",
  "胃輕癱臨床診斷標準",
  "胃輕癱與消化不良有何不同",
  "碳水化合物造成脂肪堆積的機制",
  "逆轉代謝異常脂肪肝"
];

const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
const posts = mdFiles.map(f => {
  const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf-8');
  const titleMatch = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  return {
    file: f,
    title: titleMatch ? titleMatch[1].trim() : f,
    content: content
  };
});

targets.forEach((t, i) => {
  console.log(`\nTARGET ${i+1}: ${t}`);
  // Extract core keywords
  let keywords = [];
  if (t.includes("糖化血色素")) keywords.push("糖化血色素");
  if (t.includes("空腹血糖")) keywords.push("空腹血糖");
  if (t.includes("尿蛋白")) keywords.push("尿蛋白");
  if (t.includes("尿潛血")) keywords.push("尿潛血");
  if (t.includes("貧血")) keywords.push("貧血");
  if (t.includes("胃癌")) keywords.push("胃癌");
  if (t.includes("肌少症")) keywords.push("肌少症");
  if (t.includes("慢性腎臟病")) keywords.push("慢性腎臟病");
  if (t.includes("膽紅素")) keywords.push("膽紅素");
  if (t.includes("血壓")) keywords.push("血壓");
  if (t.includes("S-ABCDE")) keywords.push("S-ABCDE");
  if (t.includes("肝功能") || t.includes("ALT")) keywords.push("肝功能", "ALT");
  if (t.includes("白蛋白") || t.includes("Albumin")) keywords.push("白蛋白", "Albumin");
  if (t.includes("球蛋白") || t.includes("Globulin")) keywords.push("球蛋白", "Globulin");
  if (t.includes("AG ratio")) keywords.push("AG ratio");
  if (t.includes("Cystatin C") || t.includes("血清胱蛋白")) keywords.push("Cystatin", "血清胱蛋白");
  if (t.includes("HDL")) keywords.push("HDL");
  if (t.includes("胃輕癱")) keywords.push("胃輕癱");
  if (t.includes("碳水化合物") || t.includes("脂肪堆積")) keywords.push("碳水化合物", "脂肪");
  if (t.includes("代謝異常脂肪肝")) keywords.push("代謝異常脂肪肝");

  let matches = posts.filter(p => {
    return keywords.some(kw => p.title.includes(kw) || p.file.includes(kw));
  });

  if (matches.length > 0) {
    matches.forEach(m => console.log(`  -> File: ${m.file} | Title: ${m.title}`));
  } else {
    console.log(`  -> NO MATCHES IN EXISTING POSTS`);
  }
});
