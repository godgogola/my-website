import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const POSTS_DIR = path.join(__dirname, '../src/content/posts');

const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));
const posts = mdFiles.map(f => {
  const content = fs.readFileSync(path.join(POSTS_DIR, f), 'utf-8');
  const titleMatch = content.match(/^title:\s*["']?(.+?)["']?\s*$/m);
  return {
    file: f,
    title: titleMatch ? titleMatch[1].trim() : f.replace('.md', '')
  };
});

const userRequests = [
  "【糖化血色素】空腹血糖高但是糖化血色素正常是什麼原因",
  "【糖化血色素】空腹血糖正常但是糖化血色素高是什麼原因",
  "【糖化血色素】糖化血色素升高的原因_非飲食因素",
  "【尿蛋白】輕微尿蛋白怎麼辦",
  "【尿潛血】輕微尿潛血怎麼辦",
  "【貧血】小球性與大球性貧血",
  "【胃癌】胃癌的危險因子",
  "【腎功能】高齡肌少症與腎功能誤判",
  "【慢性腎臟病】慢性腎臟病各分期保腎措施",
  "【膽紅素】單純膽紅素偏高",
  "長期血壓控制不良的併發症",
  "S-ABCDE 高血壓生活型態調整",
  "【ALT AST】肝功能上升",
  "【Albumin】白蛋白的合成與低下原因",
  "【Globulin】球蛋白",
  "【AG ratio】",
  "【Cystatin C】血清胱蛋白 C",
  "【HDL】HDL太高是好事嗎",
  "【胃輕癱】胃輕癱飲食調整與治療",
  "【胃輕癱】胃輕癱臨床診斷標準",
  "【胃輕癱】胃輕癱與消化不良有何不同",
  "碳水化合物造成脂肪堆積的機制",
  "【代謝異常脂肪肝】逆轉代謝異常脂肪肝"
];

userRequests.forEach((req, i) => {
  console.log(`\n=== [${i+1}] ${req} ===`);
  const keywords = req.replace(/[【】\[\]（）()_:\s-]/g, ' ')
                      .split(' ')
                      .filter(w => w.length > 1);
  posts.forEach(p => {
    const pStr = p.file + ' ' + p.title;
    const matchedKws = keywords.filter(kw => pStr.toLowerCase().includes(kw.toLowerCase()));
    if (matchedKws.length >= 1) {
      console.log(`  Match (${matchedKws.length}/${keywords.length} [${matchedKws.join(', ')}]): File=${p.file} | Title=${p.title}`);
    }
  });
});
