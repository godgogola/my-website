import fs from 'fs';

const c = fs.readFileSync('C:\\Users\\X1 Yoga Gen7\\.gemini\\antigravity-ide\\brain\\f6782200-767d-43c0-9c0c-b4ccca9153df\\.system_generated\\steps\\222\\content.md', 'utf8');

console.log('Length:', c.length);
console.log(c.slice(0, 1000));
