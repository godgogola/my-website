import fs from 'fs';

let content = fs.readFileSync('src/pages/bowel-prep.astro', 'utf8');

content = content
  .replace(/#FAF6EE/gi, '#FAF6F0')
  .replace(/#2F6656/gi, '#E76F51')
  .replace(/#E8F2EE/gi, '#FDEEE9')
  .replace(/#BC8A4A/gi, '#F4A261')
  .replace(/#F7EFE2/gi, '#FEF6EC');

fs.writeFileSync('src/pages/bowel-prep.astro', content, 'utf8');
console.log('Updated bowel-prep.astro colors.');
