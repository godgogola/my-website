import fs from 'fs';
import path from 'path';

const medicalVaultPath = 'G:/我的雲端硬碟/衛教文章庫/衛教文章庫';
const booksVaultPath = 'G:/我的雲端硬碟/讀書筆記庫/讀書筆記';
const srcBookRoom = path.join(medicalVaultPath, '診間說書房');

const book1Dir = path.join(booksVaultPath, '你的人生，他們六個說了!');
const book2Dir = path.join(booksVaultPath, '90%的病，控糖就會好');

if (!fs.existsSync(book1Dir)) fs.mkdirSync(book1Dir, { recursive: true });
if (!fs.existsSync(book2Dir)) fs.mkdirSync(book2Dir, { recursive: true });

const mappings = [
  {
    src: '【大腦的天使特調】六大神經傳導物質簡介.md',
    destDir: book1Dir,
    destName: '01、六大神經傳導物質簡介.md',
    title: '01、六大神經傳導物質簡介',
    coverImage: '01、六大神經傳導物質簡介.webp'
  },
  {
    src: '【大腦的天使特調】多巴胺_動機與渴望的動力引擎.md',
    destDir: book1Dir,
    destName: '02、多巴胺_動機與渴望的動力引擎.md',
    title: '02、多巴胺_動機與渴望的動力引擎',
    coverImage: '02、多巴胺_動機與渴望的動力引擎.webp'
  },
  {
    src: '【大腦的天使特調】腦內啡_天然止痛劑與極致愉悅感.md',
    destDir: book1Dir,
    destName: '03、腦內啡_天然止痛劑與極致愉悅感.md',
    title: '03、腦內啡_天然止痛劑與極致愉悅感',
    coverImage: '03、腦內啡_天然止痛劑與極致愉悅感.webp'
  },
  {
    src: '【大腦的天使特調】催產素_信任與歸屬感的愛的荷爾蒙.md',
    destDir: book1Dir,
    destName: '04、催產素_信任與歸屬感的愛的荷爾蒙.md',
    title: '04、催產素_信任與歸屬感的愛的荷爾蒙',
    coverImage: '04、催產素_信任與歸屬感的愛的荷爾蒙.webp'
  },
  {
    src: '【大腦的天使特調】血清素_滿足感與穩定情緒的基石.md',
    destDir: book1Dir,
    destName: '05、血清素_滿足感與穩定情緒的基石.md',
    title: '05、血清素_滿足感與穩定情緒的基石',
    coverImage: '05、血清素_滿足感與穩定情緒的基石.webp'
  },
  {
    src: '【大腦的天使特調】皮質醇_應變挑戰與警覺的雙面刃.md',
    destDir: book1Dir,
    destName: '06、皮質醇_應變挑戰與警覺的雙面刃.md',
    title: '06、皮質醇_應變挑戰與警覺的雙面刃',
    coverImage: '06、皮質醇_應變挑戰與警覺的雙面刃.webp'
  },
  {
    src: '【大腦的天使特調】睪固酮_自信心與行為傾向的增幅器.md',
    destDir: book1Dir,
    destName: '07、睪固酮_自信心與行為傾向的增幅器.md',
    title: '07、睪固酮_自信心與行為傾向的增幅器',
    coverImage: '07、睪固酮_自信心與行為傾向的增幅器.webp'
  },
  {
    src: '【大腦的天使特調】四大生活基底.md',
    destDir: book1Dir,
    destName: '08、四大生活基底.md',
    title: '08、四大生活基底',
    coverImage: '08、四大生活基底.webp'
  },
  {
    src: '【90%的病，控糖就會好】探索醣類的生物學源頭.md',
    destDir: book2Dir,
    destName: '01、探索醣類的生物學源頭.md',
    title: '01、探索醣類的生物學源頭',
    coverImage: '01、探索醣類的生物學源頭.webp'
  }
];

for (const item of mappings) {
  const srcFile = path.join(srcBookRoom, item.src);
  if (!fs.existsSync(srcFile)) {
    console.warn(`[WARN] 來源檔案不存在: ${srcFile}`);
    continue;
  }

  let content = fs.readFileSync(srcFile, 'utf8');
  let body = content;

  if (content.startsWith('---')) {
    const parts = content.split('---');
    if (parts.length >= 3) {
      body = parts.slice(2).join('---').replace(/^\r?\n/, '');
    }
  }

  const newFrontmatter = `---\ntitle: "${item.title}"\ncoverImage: "${item.coverImage}"\n---\n`;
  const destFile = path.join(item.destDir, item.destName);

  fs.writeFileSync(destFile, newFrontmatter + body, 'utf8');
  console.log(`[OK] 已成功寫入: ${destFile}`);

  // 刪除原檔案
  fs.unlinkSync(srcFile);
  console.log(`[OK] 已刪除原檔案: ${srcFile}`);
}

// 檢查原目錄是否已空，若為空則移除
const remaining = fs.readdirSync(srcBookRoom);
if (remaining.length === 0) {
  fs.rmdirSync(srcBookRoom);
  console.log(`[OK] 診間說書房 已清空並移除。`);
} else {
  console.log(`[INFO] 診間說書房 仍有未處理檔案:`, remaining);
}

console.log('🎉 讀書筆記檔案重組與轉移完成！');
