import fs from 'fs';

const html = fs.readFileSync('C:\\Users\\X1 Yoga Gen7\\.gemini\\antigravity-ide\\brain\\f6782200-767d-43c0-9c0c-b4ccca9153df\\.system_generated\\steps\\209\\content.md', 'utf8');
const cssLinks = html.match(/\/(_next\/static\/chunks\/[a-z0-9]+\.css)/g) || [];
console.log('CSS links:', [...new Set(cssLinks)]);
