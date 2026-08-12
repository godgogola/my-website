import fs from 'fs';
import path from 'path';

function listDir(dir) {
  if (!fs.existsSync(dir)) {
    console.log(`Directory does not exist: ${dir}`);
    return;
  }
  const files = fs.readdirSync(dir);
  console.log(`Files in ${dir} (total ${files.length}):`);
  for (const f of files.slice(0, 30)) {
    console.log(' -', f);
  }
}

listDir('G:/我的雲端硬碟');
listDir('G:/我的雲端硬碟/Wix衛教文章');
listDir('G:/我的雲端硬碟/衛教文章圖片');
