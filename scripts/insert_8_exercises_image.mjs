import fs from 'fs';
import path from 'path';

const userImgPath = 'C:/Users/X1 Yoga Gen7/.gemini/antigravity-ide/brain/1e0665c6-eb1d-49f0-ba20-b3d990a4208b/.user_uploaded/media_1788184254913.jpg';
const targetVaultImg = 'G:/我的雲端硬碟/Wix衛教文章/Wix衛教文章庫/要活就要動/健康力量訓練在家也能做的8個基本動作.jpg';
const targetDriveBackup = 'G:/我的雲端硬碟/衛教文章圖片/健康力量訓練在家也能做的8個基本動作.jpg';
const notePath = 'G:/我的雲端硬碟/Wix衛教文章/Wix衛教文章庫/要活就要動/【2026 ACSM】基礎阻力訓練套餐.md';

console.log('1. Copying image to Obsidian Vault and Drive Backup...');
fs.copyFileSync(userImgPath, targetVaultImg);
if (fs.existsSync('G:/我的雲端硬碟/衛教文章圖片')) {
  fs.copyFileSync(userImgPath, targetDriveBackup);
}
console.log('✅ Image copied successfully.');

console.log('2. Updating Obsidian Note with image embed syntax...');
let noteContent = fs.readFileSync(notePath, 'utf8');

const targetSection = '本套餐嚴格遵循**「先大後小、多關節動作優先」**的科學編排原則。我們先訓練高耗能的多關節大肌群，再以單關節小肌群及核心收尾，能避免局部小肌群過早疲勞而影響了大肌群訓練時的關節穩定度。';

if (noteContent.includes(targetSection)) {
  if (!noteContent.includes('![[健康力量訓練在家也能做的8個基本動作.jpg]]')) {
    noteContent = noteContent.replace(
      targetSection,
      `${targetSection}\n\n![[健康力量訓練在家也能做的8個基本動作.jpg]]\n`
    );
    fs.writeFileSync(notePath, noteContent, 'utf8');
    console.log('✅ Note updated with image syntax.');
  } else {
    console.log('ℹ️ Image syntax already present in note.');
  }
} else {
  console.warn('⚠️ Target section not found in note!');
}
