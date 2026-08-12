import fs from 'fs';
import path from 'path';

const postsDir = path.resolve('src/content/posts');
const files = fs.readdirSync(postsDir);

for (const f of files) {
  if (f.includes('腎') || f.includes('麻醉') || f.includes('安眠')) {
    console.log(f);
  }
}
