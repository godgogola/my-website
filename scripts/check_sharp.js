import fs from 'fs';
import path from 'path';

console.log('public/images exists:', fs.existsSync('public/images'));
console.log('public/og-images exists:', fs.existsSync('public/og-images'));
if (!fs.existsSync('public/og-images')) {
  fs.mkdirSync('public/og-images', { recursive: true });
  console.log('Created public/og-images');
}

// Check if sharp or sharp-cli is installed
try {
  const sharp = (await import('sharp')).default;
  console.log('sharp is available');
} catch (e) {
  console.log('sharp npm package not directly available:', e.message);
}
