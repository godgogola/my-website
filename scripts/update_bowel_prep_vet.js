import fs from 'fs';

let content = fs.readFileSync('src/pages/bowel-prep.astro', 'utf8');

// Replace any remaining older color tokens with the clean teal palette
content = content
  .replace(/#FAF6F0/gi, '#f8fbfc')
  .replace(/#FDEEE9/gi, '#eef7f9')
  .replace(/#FEF6EC/gi, '#eef5f7');

fs.writeFileSync('src/pages/bowel-prep.astro', content, 'utf8');
console.log('Updated bowel-prep.astro for Veterinary Clinic theme.');
