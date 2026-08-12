import fs from 'fs';

const data = JSON.parse(fs.readFileSync('scripts/all_posts_dump.json', 'utf8'));

console.log('--- Search: 腎 ---');
console.log(data.filter(d => d.title.includes('腎') || d.file.includes('腎')));

console.log('--- Search: 麻醉 ---');
console.log(data.filter(d => d.title.includes('麻醉') || d.file.includes('麻醉')));

console.log('--- Search: 眠 ---');
console.log(data.filter(d => d.title.includes('眠') || d.file.includes('眠')));

console.log('--- Search: 藥 ---');
console.log(data.filter(d => d.title.includes('藥') || d.file.includes('藥')));

console.log('--- Search: 超音波 ---');
console.log(data.filter(d => d.title.includes('超音波') || d.file.includes('超音波')));
