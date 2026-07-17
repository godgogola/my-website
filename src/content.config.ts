import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const postsCollection = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: "./src/content/posts" }),
  schema: z.object({
    title: z.string(),
    category: z.string().default('衛教文章'),
    publishDate: z.string().or(z.date()).transform((val) => new Date(val)),
    draft: z.boolean().default(false),
    slug: z.string().optional(),
    // 封面圖檔名（對應 src/assets/images/ 內的檔案，例如 "胃食道逆流.png"）
    coverImage: z.string().optional(),
    // SEO 專用欄位（覆蓋預設 title/description）
    meta_title: z.string().optional(),
    meta_description: z.string().optional(),
  }),
});

export const collections = {
  posts: postsCollection,
};
