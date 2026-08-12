import fs from 'fs';

const c = fs.readFileSync('C:\\Users\\X1 Yoga Gen7\\.gemini\\antigravity-ide\\brain\\f6782200-767d-43c0-9c0c-b4ccca9153df\\.system_generated\\steps\\222\\content.md', 'utf8');

const regex = /\.pet-adoption[\s\S]*?(?=\}\.[a-z]|\}\/\*|$)/g;
const matches = c.match(/\.pet-adoption[^{]*\{[^}]+\}/g) || [];
console.log('pet-adoption rules:', matches);

// Also look for color definitions in this file:
const vars = c.match(/--color-[a-z-]+:\s*[^;]+/g) || [];
console.log('Colors in chunk:', [...new Set(vars)]);

const badges = c.match(/\.(badge|btn-|filter-chip|pet-card|motion-card|heart-btn|story-card|shelter-card|stat-number|gradient-text|navbar-adopt)[^{]*\{[^}]+\}/g) || [];
console.log('Component styles:');
badges.forEach(b => console.log(b));
