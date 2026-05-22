/**
 * 博客文章类型定义
 */
export interface PostFrontmatter {
  /** 文章标题 */
  title: string;
  /** 发布日期 (YYYY-MM-DD) */
  date: string;
  /** 标签列表 */
  tags: string[];
  /** 文章摘要（显示在卡片中） */
  summary: string;
  /** 是否为草稿（草稿不显示） */
  draft?: boolean;
  /** 封面图 URL */
  coverImage?: string;
  /** 作者名 */
  author?: string;
}

export interface Post {
  /** URL 路径 slug */
  slug: string;
  /** Frontmatter 元数据 */
  frontmatter: PostFrontmatter;
  /** 原始 MDX 内容 */
  content: string;
  /** 估算阅读时间（分钟） */
  readingTime: number;
}

export interface PostListItem {
  slug: string;
  frontmatter: PostFrontmatter;
  readingTime: number;
}
