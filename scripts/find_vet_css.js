import fs from 'fs';

async function main() {
  const content = fs.readFileSync('C:/Users/X1 Yoga Gen7/.gemini/antigravity-ide/brain/f6782200-767d-43c0-9c0c-b4ccca9153df/.system_generated/steps/496/content.md', 'utf8');
  const regex = /href="(\/_next\/static\/chunks\/[^"]+\.css)"/g;
  let match;
  const links = [];
  while ((match = regex.exec(content)) !== null) {
    links.push(match[1]);
  }
  console.log('Total CSS links found:', links.length);

  for (const link of links) {
    try {
      const res = await fetch('https://uupm.cc' + link);
      const text = await res.text();
      if (text.includes('.veterinary-clinic')) {
        console.log('*** Found .veterinary-clinic in:', link);
        fs.writeFileSync('scripts/vet-clinic-exact.css', text);
      }
    } catch (e) {
      console.error('Error fetching', link, e.message);
    }
  }
}

main();
