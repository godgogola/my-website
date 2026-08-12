import fs from 'fs';

const content = fs.readFileSync('C:\\Users\\X1 Yoga Gen7\\.gemini\\antigravity-ide\\brain\\f6782200-767d-43c0-9c0c-b4ccca9153df\\.system_generated\\steps\\209\\content.md', 'utf8');

const styleMatches = content.match(/<style[\s\S]*?<\/style>/g) || [];
console.log('Found styles count:', styleMatches.length);

const varMatches = content.match(/--[\w-]+:\s*[^;]+/g) || [];
console.log('Variables found:');
console.log([...new Set(varMatches)].slice(0, 40));

const colorMatches = content.match(/(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|hsl\([^)]+\))/g) || [];
console.log('Unique colors found:', [...new Set(colorMatches)].slice(0, 30));
