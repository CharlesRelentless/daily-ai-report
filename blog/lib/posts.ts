/**
 * 文章读取模块 —— 从本地 content/posts/ 解析 MDX 文件
 */
import fs from "fs";
import path from "path";
import matter from "gray-matter";
import readingTime from "reading-time";
import type { Post, PostFrontmatter, PostListItem } from "@/types/post";

/** 文章存放目录 */
const POSTS_DIR = path.join(process.cwd(), "content", "posts");

/**
 * 读取所有文章（按日期降序排列，过滤草稿）
 */
export function getAllPosts(): PostListItem[] {
  if (!fs.existsSync(POSTS_DIR)) return [];

  const filenames = fs.readdirSync(POSTS_DIR).filter((f) => f.endsWith(".mdx"));

  const posts = filenames
    .map((filename) => {
      const slug = filename.replace(/\.mdx$/, "");
      const filePath = path.join(POSTS_DIR, filename);
      const raw = fs.readFileSync(filePath, "utf-8");
      const { data, content } = matter(raw);
      const frontmatter = data as PostFrontmatter;

      if (frontmatter.draft) return null;

      return {
        slug,
        frontmatter,
        readingTime: Math.ceil(readingTime(content).minutes),
      };
    })
    .filter((p): p is PostListItem => p !== null)
    .sort(
      (a, b) =>
        new Date(b.frontmatter.date).getTime() -
        new Date(a.frontmatter.date).getTime()
    );

  return posts;
}

/**
 * 按 slug 读取单篇文章（含完整 MDX 内容）
 */
export function getPostBySlug(slug: string): Post | null {
  const filePath = path.join(POSTS_DIR, `${slug}.mdx`);
  if (!fs.existsSync(filePath)) return null;

  const raw = fs.readFileSync(filePath, "utf-8");
  const { data, content } = matter(raw);

  return {
    slug,
    frontmatter: data as PostFrontmatter,
    content,
    readingTime: Math.ceil(readingTime(content).minutes),
  };
}

/**
 * 获取所有文章的标签及其出现次数
 */
export function getAllTags(): { tag: string; count: number }[] {
  const posts = getAllPosts();
  const tagMap = new Map<string, number>();

  for (const post of posts) {
    for (const tag of post.frontmatter.tags) {
      tagMap.set(tag, (tagMap.get(tag) || 0) + 1);
    }
  }

  return Array.from(tagMap.entries())
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag));
}

/**
 * 按标签筛选文章
 */
export function getPostsByTag(tag: string): PostListItem[] {
  return getAllPosts().filter((p) =>
    p.frontmatter.tags.some((t) => t.toLowerCase() === tag.toLowerCase())
  );
}

/**
 * 分页获取文章
 */
export function getPostsPage(
  page: number = 1,
  pageSize: number = 6
): { posts: PostListItem[]; totalPages: number; totalPosts: number } {
  const all = getAllPosts();
  const totalPosts = all.length;
  const totalPages = Math.max(1, Math.ceil(totalPosts / pageSize));
  const safePage = Math.min(Math.max(1, page), totalPages);
  const start = (safePage - 1) * pageSize;
  return { posts: all.slice(start, start + pageSize), totalPages, totalPosts };
}
