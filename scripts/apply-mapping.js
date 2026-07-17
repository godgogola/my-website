import fs from 'fs';
import path from 'path';

const POSTS_DIR = './src/content/posts';
const MAPPING_FILE = './scripts/cover-mapping.json';

if (!fs.existsSync(MAPPING_FILE)) {
  console.error(`Error: ${MAPPING_FILE} does not exist. Run node scripts/generate-mapping.js first.`);
  process.exit(1);
}

const mapping = JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8'));
let updatedCount = 0;

for (const entry of mapping) {
  const filePath = path.join(POSTS_DIR, entry.file);
  if (!fs.existsSync(filePath)) {
    console.warn(`Warning: Post file not found: ${entry.file}`);
    continue;
  }

  const content = fs.readFileSync(filePath, 'utf8');
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  
  if (!fmMatch) {
    console.warn(`Warning: Invalid frontmatter in file ${entry.file}`);
    continue;
  }

  const frontmatter = fmMatch[1];
  let newFrontmatter = frontmatter;

  // Check if coverImage exists in frontmatter
  if (frontmatter.includes('coverImage:')) {
    // If it exists, update it
    newFrontmatter = frontmatter.replace(
      /^coverImage:\s*["']?.*?["']?\s*$/m,
      `coverImage: "${entry.coverImage}"`
    );
  } else {
    // If it does not exist, insert it below title
    newFrontmatter = frontmatter.replace(
      /(^title:.*$)/m,
      `$1\ncoverImage: "${entry.coverImage}"`
    );
  }

  // Only rewrite if changed
  if (newFrontmatter !== frontmatter) {
    const newContent = content.replace(fmMatch[0], `---\n${newFrontmatter}\n---`);
    fs.writeFileSync(filePath, newContent, 'utf8');
    console.log(`Updated [${entry.title}] → ${entry.coverImage}`);
    updatedCount++;
  }
}

console.log(`\nMapping applied successfully! Total updated files: ${updatedCount}`);
