import fs from 'fs';
import path from 'path';

const POSTS_DIR = './src/content/posts';
const MAPPING_FILE = './scripts/cover-mapping.json';

if (!fs.existsSync(MAPPING_FILE)) {
  console.error(`Error: ${MAPPING_FILE} does not exist.`);
  process.exit(1);
}

const mapping = JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8'));

// Build a title -> filepath index for all current posts
const titleIndex = {};
const mdFiles = fs.readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'));

for (const mdFile of mdFiles) {
  const filePath = path.join(POSTS_DIR, mdFile);
  const content = fs.readFileSync(filePath, 'utf-8');
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) continue;
  const titleMatch = fmMatch[1].match(/^title:\s*["']?(.+?)["']?\s*$/m);
  if (titleMatch) {
    titleIndex[titleMatch[1].trim()] = { file: mdFile, content, fmMatch };
  }
}

let updatedCount = 0;
let notFoundCount = 0;

for (const entry of mapping) {
  // Skip if image file doesn't exist on disk
  const imagePath = `./public/images/${entry.coverImage}`;
  if (!fs.existsSync(imagePath)) continue;

  // Match by title first, then fallback to filename
  let postData = titleIndex[entry.title];

  if (!postData) {
    const filePath = path.join(POSTS_DIR, entry.file);
    if (fs.existsSync(filePath)) {
      const content = fs.readFileSync(filePath, 'utf-8');
      const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
      if (fmMatch) postData = { file: entry.file, content, fmMatch };
    }
  }

  if (!postData) {
    notFoundCount++;
    continue;
  }

  const { file, content, fmMatch } = postData;
  const frontmatter = fmMatch[1];
  let newFrontmatter = frontmatter;

  if (frontmatter.includes('coverImage:')) {
    newFrontmatter = frontmatter.replace(
      /^coverImage:\s*["']?.*?["']?\s*$/m,
      `coverImage: "${entry.coverImage}"`
    );
  } else {
    newFrontmatter = frontmatter.replace(
      /(^title:.*$)/m,
      `$1\ncoverImage: "${entry.coverImage}"`
    );
  }

  if (newFrontmatter !== frontmatter) {
    const filePath = path.join(POSTS_DIR, file);
    const newContent = content.replace(fmMatch[0], `---\n${newFrontmatter}\n---`);
    fs.writeFileSync(filePath, newContent, 'utf8');
    console.log(`Updated [${entry.title}] -> ${entry.coverImage}`);
    updatedCount++;
  }
}

console.log(`\nMapping applied! Updated: ${updatedCount}, Not found: ${notFoundCount}`);

