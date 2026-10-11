import fs from 'fs';
import path from 'path';

const titles = [
  '【大腦的天使特調】四大生活基底',
  '【大腦的天使特調】睪固酮_自信心與行為傾向的增幅器',
  '【大腦的天使特調】腦內啡_天然止痛劑與極致愉悅感',
  '【大腦的天使特調】皮質醇_應變挑戰與警覺的雙面刃',
  '【大腦的天使特調】血清素_滿足感與穩定情緒的基石',
  '【大腦的天使特調】催產素_信任與歸屬感的愛的荷爾蒙'
];

const postsDir = path.resolve('src/content/posts');
const postFiles = fs.readdirSync(postsDir);

const results = [];

for (const t of titles) {
  let foundPost = null;
  for (const pf of postFiles) {
    const c = fs.readFileSync(path.join(postsDir, pf), 'utf8');
    if (c.includes(`title: "${t}"`) || c.includes(`title: '${t}'`)) {
      foundPost = pf;
      break;
    }
  }

  results.push({ title: t, postFile: foundPost });
}

const gdriveDir = 'G:/我的雲端硬碟/Wix衛教文章';
function findInDir(dir, pattern) {
  if (!fs.existsSync(dir)) return null;
  const list = fs.readdirSync(dir);
  for (const item of list) {
    const p = path.join(dir, item);
    const stat = fs.statSync(p);
    if (stat.isDirectory()) {
      const res = findInDir(p, pattern);
      if (res) return res;
    } else if (item.includes(pattern)) {
      return p;
    }
  }
  return null;
}

for (const r of results) {
  const shortT = r.title.replace('【大腦的天使特調】', '');
  r.obsidianFile = findInDir(gdriveDir, shortT);
}

console.log(JSON.stringify(results, null, 2));
