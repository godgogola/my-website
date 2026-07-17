// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // ⚠️ 請將下方的 site 網址改為你的實際網域（build 時需要，才能生成正確的 sitemap.xml）
  // 例如：'https://www.fengtian-clinic.com.tw' 或 'https://你的名字.github.io'
  site: 'https://example.com',
  integrations: [
    sitemap({
      // 可選：排除不想被搜尋引擎索引的頁面
      // filter: (page) => !page.includes('/draft/'),
    }),
  ],
});

