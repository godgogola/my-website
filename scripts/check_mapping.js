import fs from 'fs';

const mapping = JSON.parse(fs.readFileSync('scripts/cover-mapping.json', 'utf-8'));

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

targets.forEach((t, i) => {
  console.log(`[${i+1}] Target: "${t}"`);
  const matches = mapping.filter(m => m.title.includes(t) || m.file.includes(t));
  if (matches.length > 0) {
    matches.forEach(m => console.log(`   Mapping Match: file=${m.file}, title=${m.title}, cover=${m.coverImage}`));
  } else {
    const cleanT = t.replace(/[【】\[\]]/g, '');
    const kwMatch = mapping.filter(m => m.title.includes(cleanT) || m.file.includes(cleanT));
    if (kwMatch.length > 0) {
      kwMatch.forEach(m => console.log(`   Mapping KW Match: file=${m.file}, title=${m.title}, cover=${m.coverImage}`));
    } else {
      console.log('   No mapping match');
    }
  }
});
