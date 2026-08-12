import fs from 'fs';

async function main() {
  const res = await fetch('https://uupm.cc/demo/veterinary-clinic');
  const html = await res.text();
  const cssMatches = Array.from(html.matchAll(/href="(\/_next\/static\/chunks\/[a-zA-Z0-9_-]+\.css)"/g)).map(m => m[1]);
  console.log('Found CSS links:', cssMatches);
  
  for (const link of cssMatches) {
    const cssRes = await fetch('https://uupm.cc' + link);
    const cssText = await cssRes.text();
    if (cssText.includes('veterinary') || cssText.includes('btn-emergency') || cssText.includes('soft-card') || cssText.includes('--color-primary')) {
      console.log('=== CSS from ' + link + ' ===');
      fs.writeFileSync('scripts/vet-clinic.css', cssText);
      console.log('Saved to scripts/vet-clinic.css, length:', cssText.length);
    }
  }
}

main().catch(console.error);
