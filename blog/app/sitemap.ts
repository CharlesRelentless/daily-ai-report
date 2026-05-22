/**
 * Sitemap 生成 —— 自动包含所有文章、标签页
 */
import { getAllPosts } from "@/lib/posts";
import { getAllDailyReports } from "@/lib/daily";
import type { MetadataRoute } from "next";

const SITE_URL = "https://blog.aihot.virxact.com";

export default function sitemap(): MetadataRoute.Sitemap {
  const posts = getAllPosts();
  const reports = getAllDailyReports();

  const postUrls: MetadataRoute.Sitemap = posts.map((post) => ({
    url: `${SITE_URL}/posts/${post.slug}`,
    lastModified: new Date(post.frontmatter.date),
    changeFrequency: "weekly",
    priority: 0.8,
  }));

  const dailyUrls: MetadataRoute.Sitemap = reports.map(({ date, updatedAt }) => ({
    url: `${SITE_URL}/daily/${date}`,
    lastModified: updatedAt,
    changeFrequency: "daily",
    priority: 0.9,
  }));

  return [
    { url: SITE_URL, lastModified: new Date(), changeFrequency: "daily", priority: 1 },
    { url: `${SITE_URL}/daily`, lastModified: new Date(), changeFrequency: "daily", priority: 0.9 },
    { url: `${SITE_URL}/tags`, lastModified: new Date(), changeFrequency: "weekly", priority: 0.5 },
    { url: `${SITE_URL}/about`, lastModified: new Date(), changeFrequency: "monthly", priority: 0.3 },
    ...dailyUrls,
    ...postUrls,
  ];
}
