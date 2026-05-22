/**
 * robots.txt —— 允许所有爬虫，指向 sitemap
 */
import type { MetadataRoute } from "next";

const SITE_URL = "https://blog.aihot.virxact.com";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: "/api/",
    },
    sitemap: `${SITE_URL}/sitemap.xml`,
  };
}
